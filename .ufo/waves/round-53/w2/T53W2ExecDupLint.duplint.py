#!/usr/bin/env python3
"""T53W2ExecDupLint v2 — duplicate-phrase lint over SKILL.md at a git rev.

Axes (defensible: each needs a command-output-backed reason to be a finding):

  K1  the two known fixed patterns named by the seat item
  D1  doubled word in prose ("the the"), excluding CLI metavariable pairs
      (--rev REV) and excluding matches that straddle a code-fence table
      column boundary
  D2  ADJACENT duplicate parenthetical — the same (...) content twice with
      only closing punctuation/whitespace between them (the shape of the
      known-fixed pattern 1: "(ten since round 51) (ten since round 51)")
  D3  duplicate parenthetical on the SAME line, non-adjacent (a copy-paste
      defect rather than a shared attribute of two list items)
  D4  duplicate parenthetical across two DIFFERENT lines of one section
      (reported with both lines so the reader can adjudicate shared-attribute
      vs copy-paste)
  D5  duplicate >=6-word n-gram across two different lines of one section,
      excluding fenced code blocks (mutant-pair tables are deliberate)

Usage:
  python3 duplint2.py --lane LANE --rev REV [--sections FILE]
                      [--json-out F] [--text-out F]
Exit 0 when zero findings, 1 otherwise.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys

HEADING_RE = re.compile(r"^#{1,3}(?:\s|$)")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
META_FLAG = re.compile(r"^--[a-z][a-z0-9-]*$")

# The two known fixed patterns named by the seat item (round 53, wave 2).
# The first is matched by regex too, because at base the first copy carried
# bold markers: "**ten** since round 51) (ten since round 51)".
KNOWN_FIXED_LITERAL = [
    "(ten since round 51) (ten since round 51)",
    "still not embedded at this boundary (both are legs 5-6 since round 10-2",
]
KNOWN_FIXED_REGEX = [
    (r"\(\*\*ten\*\* since round 51\)\s*\(ten since round 51\)",
     "(**ten** since round 51) (ten since round 51)"),
    (r"still not embedded at this boundary\s*\(both are legs 5[–-]6 since round 10-2",
     "still not embedded at this boundary (both are legs 5-6 since round 10-2"),
]


def git_show(lane, rev, path):
    out = subprocess.run(
        ["git", "-C", lane, "show", f"{rev}:{path}"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return out.stdout


def sectionize(text):
    """Split page text into sections per the frozen monitor rule.

    Mirrors .ufo/evidence/round-18/coldread/assemble.py:sectionize.
    """
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    in_fence = False
    fence_marker = ""
    headings = []
    fenced = set()
    for i, line in enumerate(lines, 1):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                in_fence = False
            continue
        if in_fence:
            fenced.add(i)
        if not in_fence and HEADING_RE.match(line):
            headings.append(i)
    bounds = []
    if not headings:
        if lines:
            bounds.append((1, len(lines), ""))
    else:
        if headings[0] > 1:
            bounds.append((1, headings[0] - 1, ""))
        for idx, h in enumerate(headings):
            end = headings[idx + 1] - 1 if idx + 1 < len(headings) else len(lines)
            bounds.append((h, end, lines[h - 1]))
    out = []
    for start, end, heading in bounds:
        body = lines[start - 1 : end]
        while body and not body[-1].strip():
            body.pop()
        out.append({
            "start": start, "end": end, "heading": heading,
            "sha256": hashlib.sha256("\n".join(body).encode("utf-8")).hexdigest(),
            "body": "\n".join(body),
        })
    return out, fenced


def doubled_words(line):
    """Doubled words in prose.

    Excludes two shapes that are not defects:
      * a CLI metavariable pair ("--rev REV"): the second word is the
        placeholder that the flag names;
      * a code-table column boundary ("pin==live live==HEADblob"): the two
        words belong to different columns and are glued by '='.
    """
    out = []
    for m in re.finditer(r"\b([A-Za-z][A-Za-z'-]*)\s+\1\b", line, flags=re.IGNORECASE):
        # the token the match starts inside, extended left over flag
        # characters so "--rev REV" yields "--rev", not "rev".
        start = m.start()
        while start > 0 and (line[start - 1].isalnum() or line[start - 1] in "_-"):
            start -= 1
        tok = line[start : m.start() + len(m.group(1))]
        if META_FLAG.match(tok):
            continue
        # glued to a preceding cell value ("pin==live live==..."): the two
        # words are different columns, not a repeated word.
        if m.start() > 0 and line[m.start() - 1] == "=":
            continue
        out.append((m.start(), m.group(0)))
    return out


def _norm_qualifier(s):
    """Normalize a parenthetical qualifier for equivalence comparison:
    strip markdown emphasis/code marks and collapse whitespace."""
    s = s.strip()
    s = re.sub(r"\*\*|__|\*|`", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.lower()


def parens(line):
    out = []
    depth = 0
    start = None
    for i, ch in enumerate(line):
        if ch == "(":
            if depth == 0:
                start = i
            depth += 1
        elif ch == ")":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    out.append((start, i + 1, line[start + 1 : i]))
                    start = None
    return out


def ngrams(text, n):
    toks = re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-/\.]*", text)
    return [" ".join(toks[i : i + n]) for i in range(len(toks) - n + 1)]


def lint(lane, rev, path, want_sections):
    raw = git_show(lane, rev, path)
    text = raw.decode("utf-8", errors="surrogateescape")
    sections, fenced = sectionize(text)
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    findings = []

    # K1 — known fixed patterns (literal + regex variants).
    for pat in KNOWN_FIXED_LITERAL:
        if pat in text:
            ln = next((i for i, l in enumerate(lines, 1) if pat in l), None)
            findings.append({"axis": "K1", "kind": "known-fixed-pattern-literal",
                             "loc": f"line {ln}", "quote": pat, "detail": ""})
    for rx, label in KNOWN_FIXED_REGEX:
        m = re.search(rx, text)
        if m:
            ln = text[: m.start()].count("\n") + 1
            findings.append({"axis": "K1", "kind": "known-fixed-pattern-regex",
                             "loc": f"line {ln}", "quote": label,
                             "detail": m.group(0)})

    # D1 — doubled word in prose.
    for i, line in enumerate(lines, 1):
        for pos, frag in doubled_words(line):
            findings.append({"axis": "D1", "kind": "doubled-word",
                             "loc": f"line {i} col {pos + 1}", "quote": frag,
                             "detail": line.strip()[:300],
                             "in_fence": i in fenced})

    # D2 — adjacent duplicate parenthetical on one line.
    for i, line in enumerate(lines, 1):
        spans = parens(line)
        for a in range(len(spans)):
            for b in range(a + 1, len(spans)):
                s1, e1, c1 = spans[a]
                s2, e2, c2 = spans[b]
                if c1.strip() == c2.strip() and len(c1.strip()) >= 3:
                    gap = line[e1 : s2]
                    findings.append({
                        "axis": "D2", "kind": "adjacent-duplicate-parenthetical",
                        "loc": f"line {i} col {s1 + 1}",
                        "quote": f"({c1.strip()})",
                        "detail": f"gap={gap!r}; second at col {s2 + 1}",
                    })

    # D6 — the SAME qualifier repeated on ONE item: two equivalent
    # parentheticals attached to a single phrase, separated only by
    # whitespace/punctuation.  This is the exact shape of known fixed
    # pattern 1 ("(**ten** since round 51) (ten since round 51)") — the
    # qualifier is duplicated, not shared by two different items.
    for i, line in enumerate(lines, 1):
        spans = parens(line)
        for a in range(len(spans)):
            for b in range(a + 1, len(spans)):
                s1, e1, c1 = spans[a]
                s2, e2, c2 = spans[b]
                n1, n2 = _norm_qualifier(c1), _norm_qualifier(c2)
                if len(n1) < 3 or n1 != n2:
                    continue
                gap = line[e1:s2]
                if gap.strip(" \t,;:.—–-()[]\"'") == "":
                    findings.append({
                        "axis": "D6", "kind": "duplicate-qualifier-on-one-item",
                        "loc": f"line {i} col {s1 + 1}",
                        "quote": f"({c1.strip()}) ({c2.strip()})",
                        "detail": f"gap={gap!r}",
                    })

    # D3 — duplicate parenthetical on the SAME line, non-adjacent.
    for i, line in enumerate(lines, 1):
        spans = parens(line)
        seen = {}
        for s, e, content in spans:
            c = content.strip()
            if len(c) < 3:
                continue
            if c in seen:
                findings.append({
                    "axis": "D3", "kind": "same-line-duplicate-parenthetical",
                    "loc": f"line {i} col {s + 1}",
                    "quote": f"({c})",
                    "detail": f"first at col {seen[c] + 1}; line: {line.strip()[:300]}",
                })
            else:
                seen[c] = s

    # D4 — duplicate parenthetical across two different lines of one section.
    for sec in sections:
        seen = {}
        for off, line in enumerate(sec["body"].split("\n")):
            abs_line = sec["start"] + off
            for s, e, content in parens(line):
                c = content.strip()
                if len(c) < 3:
                    continue
                if c in seen:
                    findings.append({
                        "axis": "D4", "kind": "cross-line-duplicate-parenthetical",
                        "loc": f"{sec['heading'][:70]!r} lines {seen[c][0]} and {abs_line}",
                        "quote": f"({c})",
                        "detail": f"first at line {seen[c][0]} col {seen[c][1] + 1}",
                    })
                else:
                    seen[c] = (abs_line, s)

    # D5 — duplicate >=6-word n-gram across two different lines of one
    # section, excluding fenced code blocks (mutant-pair tables deliberate).
    for sec in sections:
        seen = {}
        for off, line in enumerate(sec["body"].split("\n")):
            abs_line = sec["start"] + off
            if abs_line in fenced:
                continue
            for g in ngrams(line, 6):
                if g in seen:
                    findings.append({
                        "axis": "D5", "kind": "cross-line-duplicate-ngram",
                        "loc": f"{sec['heading'][:70]!r} lines {seen[g]} and {abs_line}",
                        "quote": g, "detail": "",
                    })
                else:
                    seen[g] = abs_line

    # T1 — "/tmp/" occurrences inside the named sections.
    t1 = []
    wanted = set(want_sections or [])
    if wanted:
        for sec in sections:
            if sec["heading"] not in wanted:
                continue
            for off, line in enumerate(sec["body"].split("\n")):
                if "/tmp/" not in line:
                    continue
                low = line.lower()
                hist = any(k in low for k in ("histor", "reaped", "long since",
                                             "gone", "that volatile path"))
                dated = bool(re.search(r"round (?:7|8|9|10|12|13|14|16|17|18|20|21|26|51)\b",
                                       low))
                t1.append({
                    "heading": sec["heading"],
                    "loc": f"line {sec['start'] + off}",
                    "quote": line.strip()[:500],
                    "history_marked": hist,
                    "dated_round": dated,
                })

    return {
        "rev": rev,
        "path": path,
        "skill_sha256": hashlib.sha256(raw).hexdigest(),
        "sections_total": len(sections),
        "findings": findings,
        "tmp_occurrences": t1,
        "verdict": "PASS" if not findings else "FAIL",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--path", default="SKILL.md")
    ap.add_argument("--sections")
    ap.add_argument("--json-out")
    ap.add_argument("--text-out")
    args = ap.parse_args()

    want = []
    if args.sections:
        with open(args.sections, encoding="utf-8") as fh:
            want = json.load(fh)

    res = lint(args.lane, args.rev, args.path, want)

    lines = []
    lines.append(f"DUPLINT rev={res['rev']} path={res['path']}")
    lines.append(f"skill_sha256={res['skill_sha256']}")
    lines.append(f"sections_total={res['sections_total']}")
    lines.append(f"findings={len(res['findings'])}")
    lines.append(f"verdict={res['verdict']}")
    lines.append("")
    lines.append("=== findings ===")
    if not res["findings"]:
        lines.append("(none)")
    for f in res["findings"]:
        lines.append(f"[{f['axis']}] {f['kind']} @ {f['loc']}\n  quote: {f['quote']}\n  detail: {f['detail']}")
    lines.append("")
    lines.append("=== /tmp/ occurrences in named sections ===")
    if not res["tmp_occurrences"]:
        lines.append("(none)")
    for f in res["tmp_occurrences"]:
        lines.append(f"[T1] {f['heading'][:60]!r} @ {f['loc']} history_marked={f['history_marked']} dated_round={f['dated_round']}\n  {f['quote']}")

    text = "\n".join(lines) + "\n"
    sys.stdout.write(text)
    if args.text_out:
        with open(args.text_out, "w", encoding="utf-8") as fh:
            fh.write(text)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=2)
    return 0 if not res["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
