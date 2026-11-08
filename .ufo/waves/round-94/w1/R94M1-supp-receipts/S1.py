#!/usr/bin/env python3
"""Round-94 successor counter (QUALITY 163-166; fifth attempt).

Fifth attempt at certifying Round-90's fleet-gate mutation case
(scripts/sources-census.sh @ f47ad6ba8d306f8125597401cb2ce45c1297a593 under
its own selftest) against the case note
corpus/knowledge/mutation-case-fleet-sources-census.md.

Successor to .ufo/evidence/round-93/c1/measure-v93.py (frozen, never edited).
Round 92's counter was killed by its own rule: it refused an honest note whose
non-verdict impact table happened to key its ids. This successor changes the
reader on exactly the properties round 92's own routed list demanded:

  * QUALITY 154 - refuse on VERDICT CONTENT, never on id shape. A table is a
    verdict table only when its header row carries a `verdict` cell (GFM: a
    table has one header row and one delimiter row, S321). Rows are keyed only
    inside that table. An id-keyed table that asserts no verdict is not a
    verdict table and does not refuse the note.
  * QUALITY 155 - the `verdict` header is read from the header row only; a
    data cell whose text is exactly `verdict` cannot create a second header.
  * QUALITY 157 - `coverage` grades the LAST corpus/README.md row that names
    the note (an appended denial defeats an earlier assertion); `source`
    requires a located quote that occurs in a committed source snapshot, not
    an id+URL pair.
  * QUALITY 156 - the kill rule and the declared limits of plans/round-94.plan.md
    name the same presentation classes; nothing here is refused on a class the
    plan declares unkeyed.
  * M5 (round 92) - no hand-copied instrument constants: the spec, gate and
    driver digests live in the committed pins.json, whose values this counter
    re-derives from git objects.
  * QUALITY 163 (A3) - the gate identity is anchored in the counter's own
    self-pinned bytes (GATE_COMMIT, GATE_SHA256 constants). If the derived
    identity disagrees the counter dies (setup refusal), never reporting a
    conjunct false while executing a foreign gate.
  * QUALITY 164 (A1) - `coverage` runs through `block_lines` and requires the
    note path as its own cell, not a substring match.
  * QUALITY 165 (A2) - `tables()` returns the delimiter cells; a delimiter
    whose width differs from the header adds a `delim:` finding. Remainder
    rows are padded/truncated per S321: the reader refuses a row whose explicit
    verdict-bearing cells are ambiguous, not a GFM-legal remainder row.
  * QUALITY 166 (M8) - the eight rule-level states from R93M1 are battery
    members, each moving its named rule.

Seal (QUALITY 139, unchanged): every git call carries GIT_NO_REPLACE_OBJECTS=1
plus a scrubbed GIT_*; a non-empty `git replace -l` in the lane repo or the
fleet repo refuses setup (exit 2).

Checks (identical condition in the predicate and the receipt label
C1_R94_PASS=true), in print order:
  selfpin pins spec pin green canary valid0 trivial0 inconclusive0 unstable0
  note verdict_tables ids mismatched0 figure witnessed source coverage n_min

Usage: python3 -I measure-v94.py --repo LANE --rev REV --work EMPTY_DIR
       python3 -I measure-v94.py --conjuncts
Exit: 0 PASS; 1 not PASS; 2 setup refusal.
"""
import argparse, hashlib, html as htmlmod, io, json, os, re, shutil, subprocess, sys, tarfile

SELF_SHA256 = "5bd0f545da072b60bd3f1ea293cc3df6ee7d66b8a403240269f99808428dfd57"
GATE_COMMIT = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
GATE_SHA256 = "3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30"
SELF_PIN_RE = rb'^SELF_SHA256 = "[0-9a-f]{64}"\n'

SPEC_PATH = ".ufo/evidence/round-94/c1/census-mutants.json"
PINS_PATH = ".ufo/evidence/round-94/c1/pins.json"
NOTE_PATH = "corpus/knowledge/mutation-case-fleet-sources-census.md"
LESSON_PATH = "corpus/lessons/round-94.md"
SOURCE_ROWS = {
    "S320": ".ufo/evidence/round-94/sources/s320.html",
    "S321": ".ufo/evidence/round-94/sources/s321.html",
    "S322": ".ufo/evidence/round-94/sources/s322.html",
}
N_MIN = 12
VERDICTS = ("KILLED", "SURVIVED")
CONJUNCT_KEYS = ("selfpin", "pins", "spec", "pin", "green", "canary", "valid0", "trivial0",
                 "inconclusive0", "unstable0", "note", "verdict_tables", "ids", "mismatched0",
                 "figure", "witnessed", "source", "coverage", "n_min")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
DELIM_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
DENIAL_TOKENS = ("not admitted", "not-admitted", "uncertified", "withdrawn", "refused",
                 "rejected")


def self_pin_ok():
    """QUALITY 150: the check runs before any other action, on the file's own bytes."""
    try:
        with open(os.path.abspath(__file__), "rb") as f:
            b = f.read()
    except OSError:
        return False
    norm = re.sub(SELF_PIN_RE, b"", b, flags=re.M)
    return hashlib.sha256(norm).hexdigest() == SELF_SHA256


def die(msg):
    print("C1_SETUP " + msg)
    print("C1_R94_PASS=false")
    sys.exit(2)


def sealed_env():
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def git(repo, *a, check=True):
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True, env=sealed_env())
    if check and p.returncode != 0:
        die("git-failed:" + " ".join(a) + ":" + p.stderr.decode(errors="replace").strip()[:200])
    return p


def blob(repo, rev, path):
    p = git(repo, "cat-file", "blob", f"{rev}:{path}", check=False)
    return p.stdout if p.returncode == 0 else None


def env_for(work):
    tmp = os.path.join(work, "tmp")
    os.makedirs(tmp, exist_ok=True)
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": work, "TMPDIR": tmp,
            "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}


def materialize(fleet, commit, gate_path, fixtures, gate_bytes, dest):
    sd = os.path.join(dest, os.path.dirname(gate_path))
    os.makedirs(sd, exist_ok=True)
    arch = git(fleet, "archive", "--format=tar", commit, fixtures).stdout
    with tarfile.open(fileobj=io.BytesIO(arch)) as t:
        t.extractall(dest, filter="data")
    gp = os.path.join(dest, gate_path)
    with open(gp, "wb") as f:
        f.write(gate_bytes)
    os.chmod(gp, 0o755)
    return gp


def run(argv, work, cwd, timeout):
    try:
        p = subprocess.run(argv, cwd=cwd, env=env_for(work), capture_output=True,
                           timeout=timeout, stdin=subprocess.DEVNULL)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return None, b"", b"timeout"


def selftest(gp, work, timeout):
    return run(["bash", gp, "selftest"], work, os.path.dirname(gp), timeout)


def build_witness(d, w):
    lane = os.path.join(d, "w-shokunin")
    if os.path.exists(lane):
        shutil.rmtree(lane)
    os.makedirs(lane)
    if w.get("sources") is not None:
        os.makedirs(os.path.join(lane, "corpus"), exist_ok=True)
        with open(os.path.join(lane, "corpus", "SOURCES.md"), "w", encoding="utf-8") as f:
            f.write(w["sources"])
    for dd in w.get("dirs", []):
        os.makedirs(os.path.join(lane, dd), exist_ok=True)
    for ff in w.get("files", []):
        os.makedirs(os.path.dirname(os.path.join(lane, ff)), exist_ok=True)
        with open(os.path.join(lane, ff), "w") as f:
            f.write("witness file\n")
    return lane


# ---------------------------------------------------------------- note reader
def split_cells(line):
    """GFM cell split: unescaped `|` separates cells; `\\|` is a literal pipe."""
    out, cur, i = [], [], 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "|":
            out.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    out.append("".join(cur).strip())
    if out and out[0] == "":
        out = out[1:]
    if out and out[-1] == "":
        out = out[:-1]
    return out


def norm_cell(c):
    return c.replace("*", "").replace("`", "").strip().lower()


def block_lines(text):
    """(orig_index, text) for every line outside a fenced code block (S322)."""
    vis, fence = [], None
    for idx, raw in enumerate(text.split("\n")):
        m = FENCE_RE.match(raw)
        if fence is None:
            if m:
                fence = (m.group(1)[0], len(m.group(1)))
                continue
            vis.append((idx, raw))
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] \
                    and m.group(2).strip() == "":
                fence = None
            continue
    return vis


def tables(text):
    """GFM tables: header row + delimiter row, broken at the first blank/non-pipe line.

    Grounded in S321: "The table is broken at the first empty line, or beginning of
    another block-level structure." and the header/delimiter cell-count rule.
    QUALITY 165: the delimiter cells are returned so the caller can check the
    delimiter against the header (S321: "The header row must match the delimiter
    row in the number of cells.").
    """
    vis = block_lines(text)
    out, i = [], 0
    while i < len(vis):
        oi, raw = vis[i]
        if i + 1 < len(vis) and vis[i + 1][0] == oi + 1 and DELIM_RE.match(vis[i + 1][1]) \
                and "|" in raw:
            header = split_cells(raw)
            delim_cells = split_cells(vis[i + 1][1])
            rows, j = [], i + 2
            while j < len(vis) and vis[j][0] == vis[j - 1][0] + 1:
                txt = vis[j][1]
                if txt.strip() == "" or "|" not in txt:
                    break
                if DELIM_RE.match(txt):
                    rows.append((vis[j][0], split_cells(txt), True))
                else:
                    rows.append((vis[j][0], split_cells(txt), False))
                j += 1
            out.append((oi, header, delim_cells, rows))
            i = j
            continue
        i += 1
    return out


def parse_note(nt, spec_ids):
    """Content-keyed note reader (QUALITY 154/155).

    A table is keyed only when its HEADER ROW carries a `verdict` cell. Inside
    that table: header width == delimiter width, one verdict column, and every
    data row carries exactly one spec id as its first cell and exactly one
    verdict token, in the verdict column. Outside the verdict table no
    pipe-delimited line may carry a verdict token at all (content, not shape):
    a pseudo-table paragraph is a presented verdict row even when it has no
    delimiter row. Id-keyed rows that assert no verdict are not verdict rows
    and are never refused.
    """
    bad, rows, vtables = [], {}, []
    consumed = set()
    for oi, header, delim_cells, drows in tables(nt):
        low = [norm_cell(c) for c in header]
        vcols = [k for k, c in enumerate(low) if c == "verdict"]
        if vcols:
            consumed.add(oi)
            consumed.update(ln for ln, _, _ in drows)
            vtables.append((oi, header, delim_cells, drows, vcols))
    # One rule, one place: every block line outside the verdict table that carries
    # a verdict token and at least two pipes is a presented verdict row - whether
    # it sits in another table or in a pseudo-table paragraph.
    for oi, raw in block_lines(nt):
        if oi in consumed or raw.count("|") < 2:
            continue
        toks = [c for c in split_cells(raw) if c in VERDICTS]
        if toks:
            bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))
    for oi, header, delim_cells, drows, vcols in vtables:
        if len(vcols) != 1:
            bad.append("verdict-cols:%d:%d" % (oi + 1, len(vcols)))
            vcol = vcols[0]
        else:
            vcol = vcols[0]
        # QUALITY 165: the delimiter is checked against the header (S321).
        if len(delim_cells) != len(header):
            bad.append("delim:%d:header=%d,delimiter=%d" % (oi + 1, len(header), len(delim_cells)))
        for ln, cells, isdelim in drows:
            if isdelim:
                continue
            if len(cells) != len(header):
                # S321 remainder rows may vary in cell count: missing cells are
                # empty and excess are ignored. Refuse only when the row's
                # verdict-bearing cells are ambiguous: if the row carries more
                # than one verdict token, or its token is not in the verdict
                # column, it is not a GFM-legal remainder row for this reader.
                toks = [c for c in cells if c in VERDICTS]
                if len(toks) != 1 or vcol >= len(cells) or cells[vcol] not in VERDICTS:
                    bad.append("width:%d:cells=%d" % (ln + 1, len(cells)))
                    continue
                # GFM-legal remainder: pad with empties to header width
                if len(cells) < len(header):
                    cells = cells + [""] * (len(header) - len(cells))
                else:
                    cells = cells[:len(header)]
            first = cells[0]
            toks = [c for c in cells if c in VERDICTS]
            if not toks:
                bad.append("no-verdict:%d:%s" % (ln + 1, first[:24]))
                continue
            if first not in spec_ids:
                bad.append("out-of-set:%d:%s" % (ln + 1, first[:24]))
                continue
            if len(toks) != 1 or vcol >= len(cells) or cells[vcol] not in VERDICTS:
                bad.append("position:%d:%s" % (ln + 1, first))
                continue
            if first in rows:
                bad.append("dup:%d:%s" % (ln + 1, first))
                continue
            rows[first] = cells[vcol]
    info = dict(verdict_tables=len(vtables), badrows=len(bad), bad=bad)
    return rows, bad, info


def norm_text(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def located_quotes(lesson_text):
    """sid -> list of quoted spans of <=25 words on a line naming that sid."""
    out = {sid: [] for sid in SOURCE_ROWS}
    for line in lesson_text.split("\n"):
        quoted = re.findall(r'"([^"\n]{3,300})"', line)
        if not quoted:
            continue
        for sid in SOURCE_ROWS:
            if sid in line:
                for q in quoted:
                    if 1 <= len(q.split()) <= 25:
                        out[sid].append(q)
    return out


def main():
    if "--conjuncts" in sys.argv:
        if not self_pin_ok():
            die("self-pin-mismatch")
        print("C1_CONJUNCT_KEYS " + " ".join(CONJUNCT_KEYS))
        print("C1_R94_PASS=keys-only")
        sys.exit(0)
    selfpin = self_pin_ok()
    if not selfpin:
        die("self-pin-mismatch")
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    repo = os.path.realpath(a.repo)
    rev = a.rev
    work = os.path.realpath(a.work)
    if os.path.isdir(work) and os.listdir(work):
        die("work-not-empty-dir")
    os.makedirs(work, exist_ok=True)
    for r, label in ((repo, "lane"),):
        p = git(r, "replace", "-l", check=False)
        if p.returncode != 0:
            die("replace-list-failed:" + label)
        if p.stdout.strip():
            die("replace-refs-present:" + label)
    spec_bytes = blob(repo, rev, SPEC_PATH)
    if spec_bytes is None:
        die("spec-absent-at-rev")
    try:
        spec = json.loads(spec_bytes)
    except Exception:
        die("spec-unparsable")
    g = spec.get("gate") or {}
    fleet = g.get("repo", "")
    p = git(fleet, "replace", "-l", check=False)
    if p.returncode != 0:
        die("replace-list-failed:fleet")
    if p.stdout.strip():
        die("replace-refs-present:fleet")
    gate_bytes = blob(fleet, g.get("commit", ""), g.get("path", ""))
    if gate_bytes is None:
        die("gate-blob-unreadable")
    gate_sha = hashlib.sha256(gate_bytes).hexdigest()
    pin = gate_sha == g.get("sha256")
    # PIN: no hand-copied constants (round-92 M5) - the committed pins.json must
    # declare exactly the values derived from the objects this run reads.
    pins_ok = False
    pins_bytes = blob(repo, rev, PINS_PATH)
    if pins_bytes is not None:
        try:
            pins = json.loads(pins_bytes)
        except Exception:
            pins = None
        if isinstance(pins, dict):
            derived = {"spec_sha256": hashlib.sha256(spec_bytes).hexdigest(),
                       "gate_commit": g.get("commit"), "gate_path": g.get("path"),
                       "gate_sha256": gate_sha, "fixtures": g.get("fixtures")}
            pins_ok = all(pins.get(k) == v for k, v in derived.items())
    # QUALITY 163 (A3): externally anchor the gate identity in the counter's own
    # self-pinned bytes. If the derived identity disagrees, die: never execute a
    # foreign gate while reporting the pin conjuncts true (R93SN1 F1).
    if g.get("commit") != GATE_COMMIT or gate_sha != GATE_SHA256:
        die("gate-identity-mismatch: expected %s/%s" % (GATE_COMMIT, GATE_SHA256[:16]))
    ids = [m.get("id") for m in spec.get("mutants", [])]
    spec_ids = set(ids)
    spec_ok = (len(spec.get("mutants", [])) == N_MIN and len(spec_ids) == N_MIN
               and all(isinstance(i, str) and i for i in ids)
               and bool(re.match(r"^[0-9a-f]{64}$", str(g.get("sha256", "")))))
    gate_text = gate_bytes.decode("utf-8")
    to = float(spec.get("timeout_s", 180))
    runs = int(spec.get("runs_per_verdict", 2))
    pr = os.path.join(work, "pristine")
    gp = materialize(fleet, g["commit"], g["path"], g["fixtures"], gate_bytes, pr)
    green_runs = [selftest(gp, work, to) for _ in range(2)]
    green = all(r[0] == 0 and b"selftest ok" in r[1] for r in green_runs)
    cn = os.path.join(work, "canary")
    lines = gate_text.split("\n")
    canary_text = "\n".join(lines[:1] + ["exit 97"] + lines[1:])
    cgp = materialize(fleet, g["commit"], g["path"], g["fixtures"], canary_text.encode(), cn)
    canary = selftest(cgp, work, to)[0] == 97
    clean_lane = os.path.join(pr, g["fixtures"], "root", "c-shokunin")
    rows = []
    for m in spec["mutants"]:
        mid = m["id"]
        cnt = gate_text.count(m["old"])
        inv = []
        if cnt != 1:
            inv.append("count")
        if m.get("new") == m.get("old"):
            inv.append("noop")
        mtext = gate_text.replace(m["old"], m["new"], 1) if cnt >= 1 else gate_text
        md = os.path.join(work, "m-" + mid)
        mgp = materialize(fleet, g["commit"], g["path"], g["fixtures"], mtext.encode(), md)
        if run(["bash", "-n", mgp], work, md, 30)[0] != 0:
            inv.append("syntax")
        trivial = False
        lrc, lout, lerr = run(["bash", mgp, "validate", "--today", "2026-11-06", clean_lane],
                              work, md, 60)
        if lrc == 2 or lrc is None or b"gawk failed" in lerr or b"syntax error" in lerr:
            trivial = True
        verdicts = []
        for _ in range(runs):
            rc = selftest(mgp, work, to)[0]
            verdicts.append("INCONCLUSIVE" if rc is None else ("SURVIVED" if rc == 0 else "KILLED"))
        derived = "UNSTABLE" if len(set(verdicts)) > 1 else verdicts[0]
        w = m.get("witness")
        witness = "none"
        if w:
            wd = os.path.join(work, "w-" + mid)
            os.makedirs(wd, exist_ok=True)
            lane = build_witness(wd, w)
            wargv = [w["mode"], "--today", w.get("today", "2026-11-06"), lane]
            p1 = run(["bash", gp] + wargv, work, wd, 60)
            lane = build_witness(wd, w)
            p2 = run(["bash", mgp] + wargv, work, wd, 60)
            witness = "differs" if (p1[0], p1[1]) != (p2[0], p2[1]) else "same"
        rows.append(dict(id=mid, derived=derived, runs=verdicts, invalid=inv, trivial=trivial,
                         witness=witness))
        shutil.rmtree(md, ignore_errors=True)
    n = len(rows)
    killed = sum(r["derived"] == "KILLED" for r in rows)
    survived = sum(r["derived"] == "SURVIVED" for r in rows)
    inconclusive = sum(r["derived"] == "INCONCLUSIVE" for r in rows)
    unstable = sum(r["derived"] == "UNSTABLE" for r in rows)
    invalid = sum(bool(r["invalid"]) for r in rows)
    trivial = sum(r["trivial"] for r in rows)
    witnessed = sum(r["derived"] == "SURVIVED" and r["witness"] == "differs" for r in rows)
    note = blob(repo, rev, NOTE_PATH)
    note_state = "present" if note is not None else "absent"
    note_rows, bad, info = {}, [], dict(verdict_tables=0, badrows=0, bad=[])
    mism = 0
    if note is not None:
        nt = note.decode("utf-8", errors="replace")
        note_rows, bad, info = parse_note(nt, spec_ids and spec_ids or set(ids))
        mism = sum(1 for r in rows if note_rows.get(r["id"]) != r["derived"])
        block = "\n".join(t for _, t in block_lines(nt))
        heads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", block, re.M)
        figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n
    else:
        figure_ok = False
    ids_ok = (note is not None and not bad and set(note_rows) == spec_ids)
    vtables_ok = info["verdict_tables"] == 1
    # source (QUALITY 157): a mined row, the lesson naming it, and a located quote
    # that OCCURS in the committed snapshot - not an id+URL pair.
    sreg = (blob(repo, rev, "corpus/SOURCES.md") or b"").decode("utf-8", errors="replace")
    lesson_b = blob(repo, rev, LESSON_PATH)
    lesson = lesson_b.decode("utf-8", errors="replace") if lesson_b is not None else ""
    quotes = located_quotes(lesson)
    source_ok = lesson_b is not None
    source_detail = []
    for sid, snap in SOURCE_ROWS.items():
        row_ok = False
        for line in sreg.split("\n"):
            c = [x.strip() for x in re.sub(r"^ {0,3}", "", line).split("|")]
            if len(c) >= 13 and c[1] == sid and c[8] == "mined" and LESSON_PATH in c[11]:
                row_ok = True
                break
        snap_b = blob(repo, rev, snap)
        text = norm_text(snap_b.decode("utf-8", errors="replace")) if snap_b else ""
        quote_ok = any(norm_text(q) in text for q in quotes.get(sid, []))
        source_detail.append("%s=row:%d,quote:%d" % (sid, row_ok, quote_ok))
        source_ok = source_ok and row_ok and quote_ok
    # coverage (QUALITY 157 as narrowed by QUALITY 164): the LAST corpus/README.md
    # row (outside a fenced block, S322) whose own cells name the note; an appended
    # denial defeats an earlier assertion. Fenced rows are literal (A1).
    readme = (blob(repo, rev, "corpus/README.md") or b"").decode("utf-8", errors="replace")
    last_row = None
    for oi, raw in block_lines(readme):
        cells = split_cells(raw)
        # QUALITY 164: the path must be its own cell (backtick-delimited cell whose
        # first token is the path), not a substring of a longer filename.
        def _names_note(cell):
            c = cell.strip().strip("`").strip()
            # first whitespace-delimited token
            first = c.split()[0].strip("`") if c.split() else ""
            return first == "knowledge/mutation-case-fleet-sources-census.md"
        if cells and any(_names_note(c) for c in cells):
            # require a pipe-delimited row (a table row), not prose naming the path
            if raw.count("|") >= 2:
                last_row = raw
    coverage_ok = last_row is not None and not any(
        t in last_row.lower() for t in DENIAL_TOKENS)
    for r in rows:
        print("C1_ROW %s derived=%s runs=%s note=%s invalid=%s trivial=%s witness=%s" % (
            r["id"], r["derived"], ",".join(r["runs"]), note_rows.get(r["id"], "-"),
            ",".join(r["invalid"]) or "-", int(r["trivial"]), r["witness"]))
    conj = dict(selfpin=selfpin, pins=pins_ok, spec=spec_ok, pin=pin, green=green, canary=canary,
                valid0=invalid == 0, trivial0=trivial == 0, inconclusive0=inconclusive == 0,
                unstable0=unstable == 0, note=note is not None, verdict_tables=vtables_ok,
                ids=ids_ok, mismatched0=(note is not None and mism == 0), figure=figure_ok,
                witnessed=witnessed == survived, source=source_ok, coverage=coverage_ok,
                n_min=n >= N_MIN)
    ok = all(conj.values())
    print("C1_SUMMARY rev=%s n=%d killed=%d survived=%d inconclusive=%d unstable=%d invalid=%d "
          "trivial=%d witnessed=%d/%d note=%s mismatched=%d badrows=%d verdict_tables=%d" % (
              rev, n, killed, survived, inconclusive, unstable, invalid, trivial, witnessed,
              survived, note_state, mism, len(bad), info["verdict_tables"]))
    if bad:
        print("C1_BADROWS " + " ".join(bad[:40]))
    print("C1_SOURCE " + " ".join(source_detail))
    print("C1_CONJUNCTS " + " ".join("%s=%s" % (k, str(v).lower()) for k, v in conj.items()))
    print("C1_R94_PASS=" + ("true" if ok else "false"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
