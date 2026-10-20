#!/usr/bin/env python3
"""Assemble the round-16 cold-read ledger from seat cold-read reports.

Reads seat report markdown files (each ending in a fenced ```json cold-read
block), recomputes section boundaries and per-section sha256 from one or two
SKILL files (the pinned snapshot plus, optionally, a later edited SKILL.md),
merges per-section seat verdicts, applies optional L1 overrides, writes
ledger.json and prints a coverage report. Exits 1 when any section lacks an
entry.

Sectioning rule (L1 interface decision 1): a section runs from a #/##/###
heading line (outside fenced code blocks) through the line before the next such
heading; lines before the first heading form a preamble section (start 1,
heading ""). The section sha256 is over the section's lines joined with "\\n"
AFTER stripping trailing blank (whitespace-only) lines; no trailing newline.
The snapshot produces 51 buckets (50 headings + preamble).

Merging (L1 decision 2): entries are keyed by section sha256 (sections
identical across the two SKILL files share one entry). Per-observation, a seat
verdict of executed-ok or verified-record that lists minor_gaps is downgraded
to gap-minor BEFORE merging; entry verdict = strictest observation (order:
wrong-expectation > gap-blocking > not-executed > gap-minor > verified-record
> executed-ok). class = "instruction" when seats disagree. blocking_gaps,
wrong_expectations, minor_gaps and commands_executed_count are sums of the
seat lists' lengths.

Overrides (L1 decision 3): --override FILE JSON entries resolve to ledger
entries by "sha256" (preferred) or {"start", optional "skill_sha256"}.
  - stricter mode (no "report"): verdict must be strictly stricter than the
    merged verdict; an override can NEVER relax a wave-1 entry at the same sha.
  - replace mode ("report": PATH): the cited wave-2 report must parse, name the
    skill file whose sha covers this entry, and cover that section; the entry's
    verdict/class/gap/command fields are replaced with that observation.
Every applied override is recorded on the entry with its reason.

Multi-skill (L1 decisions 4-5): pass --skill PATH twice (pre then post); each
report is validated against the SKILL file whose sha256 it names, and
ledger.json gains a top-level "skill_pins": {"pre": ..., "post": ...}.

Usage:
  assemble.py [--skill PATH ...] [--out PATH] [--override FILE] [--selftest]
              [REPORT_GLOB ...]

With no REPORT_GLOB, defaults to the round-16 w1/w2 seat-report globs relative
to this file's location. Stdlib only.
"""
import argparse
import contextlib
import glob
import hashlib
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SKILL = os.path.join(HERE, "SKILL.snapshot.md")
DEFAULT_OUT = os.path.join(HERE, "ledger.json")
DEFAULT_GLOBS = [
    os.path.join(HERE, "..", "..", "waves", "round-16", "w1", "*.md"),
    os.path.join(HERE, "..", "..", "waves", "round-16", "w2", "*.md"),
]

SCHEMA = "tameshi-coldread-ledger-v1"
HEADING_RE = re.compile(r"^#{1,3}(?:\s|$)")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
JSON_FENCE_RE = re.compile(r"^`{3,}\s*json\s*$", re.IGNORECASE)
CLASSES = ("instruction", "record")
# Strictness order from the contract; index 0 is strictest.
VERDICTS = [
    "wrong-expectation",
    "gap-blocking",
    "not-executed",
    "gap-minor",
    "verified-record",
    "executed-ok",
]
VERDICT_RANK = {v: i for i, v in enumerate(VERDICTS)}
RELAXING = ("verified-record", "executed-ok")


class AsmError(Exception):
    """Fatal assembly error (heading mismatch, unreadable skill file, ...)."""


# ---------------------------------------------------------------- sections
def sectionize(text):
    """Split file text into sections per the contract rule.

    Returns a list of dicts: {start, end, heading, sha256}. Line numbers are
    1-based; end is inclusive (line before the next heading, or last line).
    sha256 covers the section's lines joined by "\\n" after stripping trailing
    whitespace-only lines (L1 decision 1).
    """
    lines = text.split("\n")
    # A trailing newline produces a final empty element; drop it so `end`
    # points at the last real line.
    if lines and lines[-1] == "":
        lines.pop()
    in_fence = False
    fence_marker = ""
    headings = []  # 1-based line numbers of heading lines
    for i, line in enumerate(lines, 1):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[0]  # '`' or '~'
            elif marker[0] == fence_marker:
                in_fence = False
            continue
        if not in_fence and HEADING_RE.match(line):
            headings.append(i)
    bounds = []
    if not headings:
        if lines:
            bounds.append((1, len(lines), ""))
        return _mksections(lines, bounds)
    if headings[0] > 1:
        bounds.append((1, headings[0] - 1, ""))
    for idx, h in enumerate(headings):
        end = headings[idx + 1] - 1 if idx + 1 < len(headings) else len(lines)
        bounds.append((h, end, lines[h - 1]))
    return _mksections(lines, bounds)


def _mksections(lines, bounds):
    out = []
    for start, end, heading in bounds:
        body_lines = lines[start - 1 : end]
        while body_lines and not body_lines[-1].strip():
            body_lines.pop()
        out.append(
            {
                "start": start,
                "end": end,
                "heading": heading,
                "sha256": hashlib.sha256(
                    "\n".join(body_lines).encode("utf-8")
                ).hexdigest(),
            }
        )
    return out


# ------------------------------------------------------------------ reports
def extract_json_block(text):
    """Return the payload of the LAST ```json fenced block, or None."""
    lines = text.split("\n")
    blocks = []
    i = 0
    while i < len(lines):
        if JSON_FENCE_RE.match(lines[i].strip()):
            j = i + 1
            body = []
            while j < len(lines) and not re.match(r"^`{3,}\s*$", lines[j]):
                body.append(lines[j])
                j += 1
            if j < len(lines):  # found closing fence
                blocks.append("\n".join(body))
                i = j + 1
                continue
        i += 1
    return blocks[-1] if blocks else None


def load_report(path):
    """Parse one report file -> (obs_map, seat, skill_sha).

    obs_map: {start: [observation, ...]} where each observation carries
    _seat and _report. Raises AsmError on malformed blocks.
    """
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        raise AsmError("report %s: unreadable: %s" % (path, e))
    payload = extract_json_block(text)
    if payload is None:
        raise AsmError("no closing ```json block found")
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        raise AsmError("final json block does not parse: %s" % e)
    if not isinstance(data, dict) or "sections" not in data:
        raise AsmError("json block lacks 'sections'")
    seat = data.get("seat")
    if not isinstance(seat, str) or not seat:
        raise AsmError("missing/invalid 'seat'")
    skill_sha = data.get("skill_sha256")
    if not isinstance(skill_sha, str) or not skill_sha:
        raise AsmError("missing/invalid 'skill_sha256'")
    obs = {}
    for s in data["sections"]:
        if not isinstance(s, dict):
            raise AsmError("non-object entry in sections")
        if not isinstance(s.get("start"), int) or isinstance(s.get("start"), bool):
            raise AsmError("section without integer 'start'")
        for k in ("heading", "verdict", "class"):
            if not isinstance(s.get(k), str):
                raise AsmError(
                    "section at start=%s missing string '%s'" % (s.get("start"), k)
                )
        if s["verdict"] not in VERDICT_RANK:
            raise AsmError(
                "start=%s invalid verdict %r" % (s.get("start"), s["verdict"])
            )
        if s["class"] not in CLASSES:
            raise AsmError("start=%s invalid class %r" % (s.get("start"), s["class"]))
        for k in ("blocking_gaps", "wrong_expectations", "minor_gaps",
                  "commands_executed", "opened"):
            v = s.get(k)
            if v is not None and not isinstance(v, list):
                raise AsmError("start=%s '%s' must be a list" % (s.get("start"), k))
        s["_seat"] = seat
        s["_report"] = path
        obs.setdefault(s["start"], []).append(s)
    return obs, seat, skill_sha


def effective_verdict(o):
    """Per-observation verdict after the L1 decision-2 downgrade."""
    if o["verdict"] in RELAXING and o.get("minor_gaps"):
        return "gap-minor"
    return o["verdict"]


# ----------------------------------------------------------------- overrides
def load_overrides(path):
    """Parse an --override FILE -> list of override records.

    Accepted shapes:
      {"overrides": [rec, ...]}   or   [rec, ...]
    rec := {"sha256": SEC_SHA} | {"start": N, "skill_sha256"?: S}
           + "verdict": V + "reason": R            (stricter mode)
           + optional "report": PATH              (replace mode)
    In replace mode "verdict" is optional (taken from the cited report).
    """
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise AsmError("override file %s: %s" % (path, e))
    if isinstance(data, dict):
        data = data.get("overrides", [])
    if not isinstance(data, list):
        raise AsmError("override file %s: expected list or object" % path)
    out = []
    for o in data:
        if not isinstance(o, dict):
            raise AsmError("override file %s: non-object entry" % path)
        has_sha = isinstance(o.get("sha256"), str) and bool(o["sha256"])
        has_start = isinstance(o.get("start"), int) and not isinstance(
            o.get("start"), bool
        )
        if not (has_sha or has_start):
            raise AsmError(
                "override file %s: entry needs 'sha256' or integer 'start'" % path
            )
        if "skill_sha256" in o and not isinstance(o["skill_sha256"], str):
            raise AsmError(
                "override file %s: non-string skill_sha256" % path
            )
        if "report" not in o:
            if o.get("verdict") not in VERDICT_RANK:
                raise AsmError(
                    "override file %s: stricter-mode entry needs a valid "
                    "'verdict'" % path
                )
        else:
            if not isinstance(o["report"], str) or not o["report"]:
                raise AsmError(
                    "override file %s: 'report' must be a path string" % path
                )
            if "verdict" in o and o["verdict"] not in VERDICT_RANK:
                raise AsmError(
                    "override file %s: invalid verdict %r" % (path, o["verdict"])
                )
        if not isinstance(o.get("reason"), str) or not o["reason"].strip():
            raise AsmError(
                "override file %s: entry requires a non-empty 'reason'" % path
            )
        rec = dict(o)
        rec["reason"] = o["reason"].strip()
        out.append(rec)
    return out


# ------------------------------------------------------------------ assembly
def assemble(skill_paths, report_paths, overrides):
    skills = []  # [{path, sha256, text, sections, by_start}]
    for sp in skill_paths:
        try:
            stext = open(sp, encoding="utf-8").read()
        except OSError as e:
            raise AsmError("skill file %s: unreadable: %s" % (sp, e))
        ssha = hashlib.sha256(stext.encode("utf-8")).hexdigest()
        if ssha in {s["sha256"] for s in skills}:
            raise AsmError("duplicate skill file (same sha256): %s" % sp)
        secs = sectionize(stext)
        skills.append(
            {
                "path": sp,
                "sha256": ssha,
                "text": stext,
                "sections": secs,
                "by_start": {s["start"]: s for s in secs},
            }
        )
    skill_by_sha = {s["sha256"]: s for s in skills}

    # Section index keyed by section sha256 (L1 decision 2).
    # sec_index[sec_sha] = {"sha256", "heading",
    #                       "positions": [{skill_sha256, start, end}]}
    sec_index = {}
    sec_order = []
    for s in skills:
        for sec in s["sections"]:
            ent = sec_index.get(sec["sha256"])
            pos = {
                "skill_sha256": s["sha256"],
                "start": sec["start"],
                "end": sec["end"],
            }
            if ent is None:
                sec_index[sec["sha256"]] = {
                    "sha256": sec["sha256"],
                    "heading": sec["heading"],
                    "positions": [pos],
                }
                sec_order.append(sec["sha256"])
            else:
                ent["positions"].append(pos)

    # sec_sha -> list of observations
    merged = {}
    rejected = []  # reports whose skill_sha256 matches no supplied skill
    skipped = []  # reports that failed to parse (warn-skip, non-fatal)
    seats_seen = []
    loaded_reports = []
    for path in report_paths:
        try:
            obs, seat, rsha = load_report(path)
        except AsmError as e:
            skipped.append(path)
            print("SKIPPED %s: %s" % (path, e), file=sys.stderr)
            continue
        skill = skill_by_sha.get(rsha)
        if skill is None:
            rejected.append((path, seat, rsha))
            print(
                "REJECTED %s: seat %s skill_sha256 %s matches no supplied "
                "skill file" % (path, seat, rsha),
                file=sys.stderr,
            )
            continue
        loaded_reports.append(path)
        if seat not in seats_seen:
            seats_seen.append(seat)
        first_line = skill["text"].split("\n", 1)[0] if skill["text"] else ""
        for start, obslist in obs.items():
            sec = skill["by_start"].get(start)
            if sec is None:
                raise AsmError(
                    "report %s: start=%s is not a section boundary in %s"
                    % (path, start, skill["path"])
                )
            for o in obslist:
                # Preamble sections have heading "" in the section model;
                # accept "" or the file's first line from seats.
                want, got = sec["heading"], o["heading"]
                ok = got == want or (
                    want == "" and start == 1 and got in ("", first_line)
                )
                if not ok:
                    raise AsmError(
                        "report %s: heading mismatch at start=%d: report %r "
                        "!= skill %r" % (path, start, got, want)
                    )
            merged.setdefault(sec["sha256"], []).extend(obslist)

    entries = []
    for sec_sha in sec_order:
        secinfo = sec_index[sec_sha]
        obslist = merged.get(sec_sha)
        if obslist is None:
            continue
        best = min(obslist, key=lambda o: VERDICT_RANK[effective_verdict(o)])
        classes = sorted({o["class"] for o in obslist})
        cls = "instruction" if "instruction" in classes else classes[0]
        pos0 = secinfo["positions"][0]
        entry = {
            "skill_sha256": pos0["skill_sha256"],
            "start": pos0["start"],
            "end": pos0["end"],
            "heading": secinfo["heading"],
            "sha256": sec_sha,
            "class": cls,
            "verdict": effective_verdict(best),
            "blocking_gaps": sum(
                len(o.get("blocking_gaps") or []) for o in obslist
            ),
            "wrong_expectations": sum(
                len(o.get("wrong_expectations") or []) for o in obslist
            ),
            "minor_gaps": sum(len(o.get("minor_gaps") or []) for o in obslist),
            "commands_executed_count": sum(
                len(o.get("commands_executed") or []) for o in obslist
            ),
            "seats": [],
            "reports": [],
        }
        if len(secinfo["positions"]) > 1:
            entry["positions"] = secinfo["positions"]
        for o in obslist:
            if o["_seat"] not in entry["seats"]:
                entry["seats"].append(o["_seat"])
            if o["_report"] not in entry["reports"]:
                entry["reports"].append(o["_report"])
        if len(classes) > 1:
            entry["class_votes"] = classes  # diagnostic; instruction won
            print(
                "WARNING section sha=%s...: seats disagree on class %s; "
                "instruction wins" % (sec_sha[:12], classes),
                file=sys.stderr,
            )
        entries.append(entry)

    apply_overrides(entries, overrides)

    missing = [sec_index[s] for s in sec_order if s not in merged]
    result = {
        "schema": SCHEMA,
        "entries": entries,
        "_meta": {
            "skill_files": [
                {"path": s["path"], "sha256": s["sha256"]} for s in skills
            ],
            "sections_total": len(sec_order),
            "sections_covered": len(entries),
            "missing": [
                {
                    "sha256": m["sha256"],
                    "heading": m["heading"],
                    "positions": m["positions"],
                }
                for m in missing
            ],
            "reports_loaded": loaded_reports,
            "reports_rejected": [
                {"report": p, "seat": seat, "skill_sha256": sha}
                for p, seat, sha in rejected
            ],
            "reports_skipped": skipped,
            "seats": seats_seen,
        },
    }
    if len(skills) >= 2:
        result["skill_pins"] = {
            "pre": skills[0]["sha256"],
            "post": skills[-1]["sha256"],
        }
    return result


def resolve_override_target(rec, entries):
    """Map an override record to a ledger entry. Returns entry or raises."""
    if rec.get("sha256"):
        hits = [e for e in entries if e["sha256"] == rec["sha256"]]
    else:
        hits = []
        for e in entries:
            for pos in e.get(
                "positions",
                [{"skill_sha256": e["skill_sha256"], "start": e["start"]}],
            ):
                if pos["start"] != rec["start"]:
                    continue
                if rec.get("skill_sha256") and pos["skill_sha256"] != rec[
                    "skill_sha256"
                ]:
                    continue
                hits.append(e)
                break
        hits = list({id(h): h for h in hits}.values())
    if not hits:
        raise AsmError(
            "override matches no ledger entry (sha256=%s start=%s)"
            % (rec.get("sha256"), rec.get("start"))
        )
    if len(hits) > 1:
        raise AsmError(
            "override start=%s is ambiguous across skill files; add sha256 or "
            "skill_sha256" % rec.get("start")
        )
    return hits[0]


def apply_overrides(entries, overrides):
    if not overrides:
        return
    for rec in overrides:
        entry = resolve_override_target(rec, entries)
        if "report" in rec:
            # Replace mode: the cited wave-2 report must name the skill whose
            # sha covers this entry and cover that section itself.
            rpath = rec["report"]
            try:
                obs, seat, rsha = load_report(rpath)
            except AsmError as e:
                raise AsmError(
                    "override report %s cannot be loaded: %s" % (rpath, e)
                )
            pos = next(
                (
                    p
                    for p in entry.get(
                        "positions",
                        [
                            {
                                "skill_sha256": entry["skill_sha256"],
                                "start": entry["start"],
                                "end": entry["end"],
                            }
                        ],
                    )
                    if p["skill_sha256"] == rsha
                ),
                None,
            )
            if pos is None:
                raise AsmError(
                    "override report %s names skill_sha256 %s, which does not "
                    "cover entry sha=%s" % (rpath, rsha, entry["sha256"][:16])
                )
            robs = obs.get(pos["start"])
            if not robs:
                raise AsmError(
                    "override report %s does not cover section at start=%d"
                    % (rpath, pos["start"])
                )
            rob = robs[0]
            rob["_report"] = rpath  # normalized to the given path
            old = entry["verdict"]
            entry["verdict"] = effective_verdict(rob)
            entry["class"] = rob["class"]
            entry["blocking_gaps"] = len(rob.get("blocking_gaps") or [])
            entry["wrong_expectations"] = len(rob.get("wrong_expectations") or [])
            entry["minor_gaps"] = len(rob.get("minor_gaps") or [])
            entry["commands_executed_count"] = len(
                rob.get("commands_executed") or []
            )
            if seat not in entry["seats"]:
                entry["seats"].append(seat)
            if rpath not in entry["reports"]:
                entry["reports"].append(rpath)
            entry["override"] = {
                "mode": "replace",
                "report": rpath,
                "seat": seat,
                "reason": rec["reason"],
                "merged_verdict": old,
            }
        else:
            # Stricter mode: may only tighten, never relax a same-sha entry.
            new_rank = VERDICT_RANK[rec["verdict"]]
            old_rank = VERDICT_RANK[entry["verdict"]]
            if new_rank >= old_rank:
                raise AsmError(
                    "override at section sha=%s... verdict %r does not make "
                    "the merged verdict %r stricter"
                    % (entry["sha256"][:16], rec["verdict"], entry["verdict"])
                )
            entry["override"] = {
                "mode": "stricter",
                "verdict": rec["verdict"],
                "reason": rec["reason"],
                "merged_verdict": entry["verdict"],
            }
            entry["verdict"] = rec["verdict"]


def print_coverage(result, skills):
    meta = result["_meta"]
    print(
        "coverage: %d/%d sections covered"
        % (meta["sections_covered"], meta["sections_total"])
    )
    skill_names = [os.path.basename(s["path"]) for s in skills]
    for e in result["entries"]:
        tag = ""
        if "override" in e:
            ov = e["override"]
            tag = " [override:%s %s -> %s]" % (
                ov["mode"],
                ov["merged_verdict"],
                e["verdict"],
            )
        print(
            "  %5d-%-5d %-16s %-18s %s%s"
            % (
                e["start"],
                e["end"],
                e["class"],
                e["verdict"],
                (e["heading"] or "(preamble)")[:72],
                tag,
            )
        )
    if meta["missing"]:
        print("missing sections:")
        for m in meta["missing"]:
            for pos in m["positions"]:
                print(
                    "  start=%d end=%d (%s) %s"
                    % (
                        pos["start"],
                        pos["end"],
                        os.path.basename(
                            next(
                                (
                                    s["path"]
                                    for s in skills
                                    if s["sha256"] == pos["skill_sha256"]
                                ),
                                "?",
                            )
                        ),
                        m["heading"] or "(preamble)",
                    )
                )
    else:
        print("missing sections: none")


# ------------------------------------------------------------------- selftest
def _selftest():
    import io

    fence = "```"
    failures = []

    def check(name, cond, detail=""):
        status = "ok" if cond else "FAIL"
        if not cond:
            failures.append(name)
        print("  [%s] %s %s" % (status, name, detail))

    def mkreport(seat, sha, secs):
        block = {"seat": seat, "skill_sha256": sha, "sections": secs}
        return (
            "# report prose\n\n" + fence + "json\n"
            + json.dumps({"unrelated": True})
            + "\n" + fence + "\nmore prose\n" + fence + "json\n"
            + json.dumps(block)
            + "\n" + fence + "\ntrailing prose\n"
        )

    skill_pre = (
        "preamble line 1\n"
        "preamble line 2\n"
        "## Alpha\n"
        "body a\n"
        + fence + "\n# not a heading\n" + fence + "\n"
        "## Beta\n"
        "body b\n"
        "### Beta.one\n"
        "body b1\n"
        "\n"  # trailing blank inside last section -> stripped for hash
    )
    # Post skill: Alpha body edited (new sha), an extra line inserted before
    # Beta (Beta keeps its sha but gains a new start), Beta.one unchanged.
    skill_post = (
        "preamble line 1\n"
        "preamble line 2\n"
        "## Alpha\n"
        "body a EDITED\n"
        "extra alpha line\n"
        + fence + "\n# not a heading\n" + fence + "\n"
        "## Beta\n"
        "body b\n"
        "### Beta.one\n"
        "body b1\n"
        "\n"
    )
    sha_pre = hashlib.sha256(skill_pre.encode()).hexdigest()
    sha_post = hashlib.sha256(skill_post.encode()).hexdigest()
    secs_pre = sectionize(skill_pre)
    secs_post = sectionize(skill_post)

    check("pre sections", len(secs_pre) == 4, "got %d" % len(secs_pre))
    check("post sections", len(secs_post) == 4, "got %d" % len(secs_post))
    check("preamble start=1 heading=''", secs_pre[0]["start"] == 1
          and secs_pre[0]["heading"] == "")
    check("alpha start=3", secs_pre[1]["start"] == 3
          and secs_pre[1]["heading"] == "## Alpha")
    check("alpha spans fenced #", secs_pre[1]["end"] == 7)
    check("beta start=8 pre", secs_pre[2]["start"] == 8)
    check("beta.one start=10 pre", secs_pre[3]["start"] == 10)
    check("beta start=9 post", secs_post[2]["start"] == 9)
    check("beta.one start=11 post", secs_post[3]["start"] == 11)
    check(
        "unchanged sections share sha across skills",
        secs_pre[2]["sha256"] == secs_post[2]["sha256"]
        and secs_pre[3]["sha256"] == secs_post[3]["sha256"]
        and secs_pre[1]["sha256"] != secs_post[1]["sha256"],
    )
    expect_sha = hashlib.sha256(
        ("## Alpha\nbody a\n" + fence + "\n# not a heading\n" + fence).encode()
    ).hexdigest()
    check("alpha sha256 (pre)", secs_pre[1]["sha256"] == expect_sha)
    # Trailing blank stripped before hashing:
    expect_last = hashlib.sha256(
        "### Beta.one\nbody b1".encode()
    ).hexdigest()
    check("trailing blank stripped", secs_pre[3]["sha256"] == expect_last)

    with tempfile.TemporaryDirectory(prefix="assemble-selftest-") as td:
        sk_pre = os.path.join(td, "SKILL.snapshot.md")
        sk_post = os.path.join(td, "SKILL.md")
        open(sk_pre, "w").write(skill_pre)
        open(sk_post, "w").write(skill_post)
        heads = {s["start"]: s["heading"] for s in secs_pre}
        heads_post = {s["start"]: s["heading"] for s in secs_post}

        def sec(start, verdict, cls="record", heading=None, post=False, **kw):
            want = (heads_post if post else heads)[start]
            return {
                "start": start,
                "heading": heading if heading is not None else want,
                "class": cls,
                "verdict": verdict,
                "blocking_gaps": kw.get("blocking_gaps", []),
                "wrong_expectations": kw.get("wrong_expectations", []),
                "minor_gaps": kw.get("minor_gaps", []),
                "commands_executed": kw.get("commands_executed", []),
                "opened": kw.get("opened", []),
                "scratch": td,
            }

        ra = os.path.join(td, "seatA.md")
        open(ra, "w").write(
            mkreport(
                "SeatA",
                sha_pre,
                [
                    sec(1, "verified-record", commands_executed=["c1"]),
                    sec(3, "executed-ok", "instruction"),
                ],
            )
        )
        rb = os.path.join(td, "seatB.md")
        open(rb, "w").write(
            mkreport(
                "SeatB",
                sha_pre,
                [
                    sec(3, "gap-blocking", "record", blocking_gaps=["g1"]),
                    sec(8, "verified-record", minor_gaps=["m1"]),
                    sec(10, "wrong-expectation", "instruction",
                        wrong_expectations=["w1"]),
                ],
            )
        )
        # w2 report against the post skill: covers edited Alpha at new sha.
        rw2 = os.path.join(td, "seatW2.md")
        open(rw2, "w").write(
            mkreport(
                "SeatW2",
                sha_post,
                [sec(3, "verified-record", "instruction", post=True)],
            )
        )
        bad = os.path.join(td, "seatBad.md")
        open(bad, "w").write(
            mkreport("SeatBad", "0" * 64, [sec(1, "executed-ok")])
        )
        garbage = os.path.join(td, "seatG.md")
        open(garbage, "w").write("# ledger note\nno json block here\n")

        out = os.path.join(td, "ledger.json")
        buf = io.StringIO()
        with contextlib.redirect_stderr(io.StringIO()):
            code = main(
                [
                    "--skill", sk_pre,
                    "--skill", sk_post,
                    "--out", out,
                    os.path.join(td, "seat*.md"),
                ],
                stdout=buf,
            )
        check("two-skill run exit 0", code == 0, "got %d" % code)
        led = json.load(open(out))
        check("ledger schema", led["schema"] == SCHEMA)
        check("skill_pins", led.get("skill_pins") == {"pre": sha_pre,
                                                    "post": sha_post})
        # Unique section shas: preamble, alpha-pre, alpha-post, beta, beta.one
        check("5 entries (sha-keyed merge)", len(led["entries"]) == 5,
              "got %d" % len(led["entries"]))
        bysha = {e["sha256"]: e for e in led["entries"]}
        e_alpha_pre = bysha[secs_pre[1]["sha256"]]
        e_alpha_post = bysha[secs_post[1]["sha256"]]
        check(
            "strictest wins (gap-blocking>executed-ok)",
            e_alpha_pre["verdict"] == "gap-blocking",
        )
        check(
            "class disagreement -> instruction",
            e_alpha_pre["class"] == "instruction",
            e_alpha_pre["class"],
        )
        check(
            "commands_executed_count sums",
            bysha[secs_pre[0]["sha256"]]["commands_executed_count"] == 1,
        )
        check(
            "minor_gaps downgrade verified-record -> gap-minor",
            bysha[secs_pre[2]["sha256"]]["verdict"] == "gap-minor",
        )
        check(
            "wrong-expectation + counts",
            bysha[secs_pre[3]["sha256"]]["verdict"] == "wrong-expectation"
            and bysha[secs_pre[3]["sha256"]]["wrong_expectations"] == 1,
        )
        check(
            "post-sha entry from w2 report",
            e_alpha_post["verdict"] == "verified-record"
            and e_alpha_post["seats"] == ["SeatW2"],
        )
        check(
            "multi-seat merge",
            e_alpha_pre["seats"] == ["SeatA", "SeatB"],
            str(e_alpha_pre["seats"]),
        )
        check(
            "bad-sha report rejected",
            len(led["_meta"]["reports_rejected"]) == 1
            and led["_meta"]["reports_rejected"][0]["seat"] == "SeatBad",
        )
        check(
            "non-report glob hit skipped",
            len(led["_meta"]["reports_skipped"]) == 1
            and led["_meta"]["reports_skipped"][0].endswith("seatG.md"),
        )
        check("coverage line", "coverage: 5/5" in buf.getvalue())

        # Missing coverage -> exit 1.
        rc = os.path.join(td, "seatC.md")
        open(rc, "w").write(
            mkreport("SeatC", sha_pre, [sec(1, "executed-ok")])
        )
        buf2 = io.StringIO()
        code2 = main(
            ["--skill", sk_pre, "--out", out, rc], stdout=buf2
        )
        check("incomplete coverage exits 1", code2 == 1, "got %d" % code2)
        check("missing list printed", "missing sections:" in buf2.getvalue()
              and "start=3" in buf2.getvalue())

        # Heading mismatch -> error (exit 2).
        rm = os.path.join(td, "seatM.md")
        open(rm, "w").write(
            mkreport(
                "SeatM", sha_pre,
                [sec(3, "executed-ok", "instruction", heading="## WRONG")],
            )
        )
        code3 = main(["--skill", sk_pre, "--out", out, rm],
                     stdout=io.StringIO())
        check("heading mismatch exits 2", code3 == 2, "got %d" % code3)
        os.remove(rm)  # keep the mismatch fixture out of later glob runs

        # Override: relaxing a same-sha entry is rejected.
        ov_relax = os.path.join(td, "ov_relax.json")
        json.dump(
            {"overrides": [
                {"sha256": secs_pre[1]["sha256"], "verdict": "verified-record",
                 "reason": "attempt to relax"}
            ]},
            open(ov_relax, "w"),
        )
        code4 = main(
            ["--skill", sk_pre, "--skill", sk_post, "--out", out,
             "--override", ov_relax, os.path.join(td, "seat*.md")],
            stdout=io.StringIO(),
        )
        check("relaxing override rejected (exit 2)", code4 == 2,
              "got %d" % code4)

        # round-16 w2 MutateAssemble survivors: executed-ok with minor gaps
        # downgrades; an equal-rank "stricter" override is rejected.
        check("minor_gaps downgrade executed-ok -> gap-minor",
              effective_verdict({"verdict": "executed-ok",
                                 "minor_gaps": ["x"]}) == "gap-minor")
        ov_equal = os.path.join(td, "ov_equal.json")
        json.dump(
            {"overrides": [
                {"sha256": secs_pre[1]["sha256"], "verdict": "gap-blocking",
                 "reason": "equal rank is not stricter"}
            ]},
            open(ov_equal, "w"),
        )
        code4b = main(
            ["--skill", sk_pre, "--skill", sk_post, "--out", out,
             "--override", ov_equal, os.path.join(td, "seat*.md")],
            stdout=io.StringIO(),
        )
        check("equal-rank override rejected (exit 2)", code4b == 2,
              "got %d" % code4b)

        # Override: stricter mode applies.
        ov_strict = os.path.join(td, "ov_strict.json")
        json.dump(
            {"overrides": [
                {"sha256": secs_post[1]["sha256"],
                 "verdict": "gap-blocking",
                 "reason": "L1: W2 read missed a blocking gap"}
            ]},
            open(ov_strict, "w"),
        )
        code5 = main(
            ["--skill", sk_pre, "--skill", sk_post, "--out", out,
             "--override", ov_strict, os.path.join(td, "seat*.md")],
            stdout=io.StringIO(),
        )
        check("stricter override exit 0", code5 == 0, "got %d" % code5)
        led2 = json.load(open(out))
        e2 = {e["sha256"]: e for e in led2["entries"]}[secs_post[1]["sha256"]]
        check(
            "stricter override recorded",
            e2["verdict"] == "gap-blocking"
            and e2["override"]["merged_verdict"] == "verified-record"
            and e2["override"]["mode"] == "stricter",
        )

        # Override: replace mode cites the w2 report at the new sha.
        ov_rep = os.path.join(td, "ov_replace.json")
        json.dump(
            {"overrides": [
                {"sha256": secs_post[1]["sha256"], "report": rw2,
                 "reason": "L1: authoritative W2 re-read"}
            ]},
            open(ov_rep, "w"),
        )
        code6 = main(
            ["--skill", sk_pre, "--skill", sk_post, "--out", out,
             "--override", ov_rep, os.path.join(td, "seat*.md")],
            stdout=io.StringIO(),
        )
        check("replace override exit 0", code6 == 0, "got %d" % code6)
        led3 = json.load(open(out))
        e3 = {e["sha256"]: e for e in led3["entries"]}[secs_post[1]["sha256"]]
        check(
            "replace override recorded",
            e3["override"]["mode"] == "replace"
            and e3["override"]["report"] == rw2
            and e3["verdict"] == "verified-record",
        )

        # Replace citing a report at the wrong sha is rejected.
        ov_badrep = os.path.join(td, "ov_badrep.json")
        json.dump(
            {"overrides": [
                {"sha256": secs_pre[1]["sha256"], "report": rw2,
                 "reason": "wrong-sha cite"}
            ]},
            open(ov_badrep, "w"),
        )
        code7 = main(
            ["--skill", sk_pre, "--skill", sk_post, "--out", out,
             "--override", ov_badrep, os.path.join(td, "seat*.md")],
            stdout=io.StringIO(),
        )
        check("wrong-sha replace rejected (exit 2)", code7 == 2,
              "got %d" % code7)

        # Preamble heading tolerance: seat may send "" or the first line.
        rp = os.path.join(td, "seatP.md")
        open(rp, "w").write(
            mkreport(
                "SeatP", sha_pre,
                [sec(1, "verified-record", heading="preamble line 1"),
                 sec(3, "executed-ok", "instruction"),
                 sec(8, "executed-ok"),
                 sec(10, "executed-ok", "instruction")],
            )
        )
        code8 = main(
            ["--skill", sk_pre, "--out", out, rp], stdout=io.StringIO()
        )
        check("preamble first-line heading tolerated", code8 == 0,
              "got %d" % code8)

    if failures:
        print("SELFTEST: FAIL (%d checks)" % len(failures))
        return 1
    print("SELFTEST: all checks passed")
    return 0


# ----------------------------------------------------------------------- main
def main(argv=None, stdout=None):
    out = stdout or sys.stdout
    p = argparse.ArgumentParser(
        description="Assemble tameshi cold-read ledger.json from seat reports."
    )
    p.add_argument(
        "--skill",
        action="append",
        metavar="PATH",
        help="SKILL file to section; repeat for pre/post (default: pinned "
        "SKILL.snapshot.md next to this script)",
    )
    p.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help="ledger output path (default: ledger.json next to this script)",
    )
    p.add_argument(
        "--override",
        metavar="FILE",
        help="JSON file of L1 verdict overrides "
        "([{sha256|start, verdict, reason, report?}, ...])",
    )
    p.add_argument(
        "--selftest",
        action="store_true",
        help="run built-in synthetic self-test and exit",
    )
    p.add_argument(
        "reports",
        nargs="*",
        metavar="REPORT_GLOB",
        help="report files/globs (default: round-16 w1/*.md and w2/*.md)",
    )
    a = p.parse_args(argv)

    if a.selftest:
        return _selftest()

    overrides = []
    if a.override:
        try:
            overrides = load_overrides(a.override)
        except AsmError as e:
            print("ERROR: %s" % e, file=sys.stderr)
            return 2

    patterns = a.reports or DEFAULT_GLOBS
    paths = []
    for pat in patterns:
        hits = sorted(glob.glob(pat))
        if not hits and os.path.exists(pat):
            hits = [pat]
        paths.extend(hits)
    seen = set()
    paths = [
        p2
        for p2 in paths
        if os.path.isfile(p2) and not (p2 in seen or seen.add(p2))
    ]

    skill_paths = a.skill or [DEFAULT_SKILL]
    try:
        result = assemble(skill_paths, paths, overrides)
    except AsmError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    tmp = a.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    os.replace(tmp, a.out)

    skills = [
        {"path": m["path"], "sha256": m["sha256"]}
        for m in result["_meta"]["skill_files"]
    ]
    with contextlib.redirect_stdout(out):
        print(
            "ledger written: %s (%d entries)" % (a.out, len(result["entries"]))
        )
        print_coverage(result, skills)
    return 0 if not result["_meta"]["missing"] else 1


if __name__ == "__main__":
    sys.exit(main())
