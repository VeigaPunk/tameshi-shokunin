#!/usr/bin/env python3
"""Round-92 sealed successor counter (QUALITY 139, 140, 143, 144, 146).

Third attempt at certifying Round-90's fleet-gate mutation case
(scripts/sources-census.sh @ f47ad6ba8d306f8125597401cb2ce45c1297a593 under
its own selftest) against the case note
corpus/knowledge/mutation-case-fleet-sources-census.md.

Successor to .ufo/evidence/round-91/c1/measure-v91.py (frozen, never edited).
Changed from v91, and only this:
  * SELF_PIN (QUALITY 144): the file carries SELF_SHA256, the sha256 of this
    file with the single `SELF_SHA256 = "<64 hex>"` line removed; the first
    action of every run is to re-derive that digest and refuse (exit 2,
    `self-pin-mismatch`) when it differs. A post-freeze edit is inert.
  * ID-SET REFUSAL (QUALITY 143): every table row that carries a verdict
    token, and every table row whose first cell is id-shaped
    (`[A-Za-z]{1,4}[_-]?[0-9]{1,4}`), must be addressed by an id in the
    spec's set. A row outside the set, a verdict token on a row with a
    non-id first cell, a spec id duplicated, a second verdict column, and a
    verdict token outside the header-named column all refuse (`ids=false`),
    never skip.

Seal (QUALITY 139) unchanged: every git call carries GIT_NO_REPLACE_OBJECTS=1
plus a scrubbed GIT_*; a non-empty `git replace -l` in the lane repo or the
fleet repo refuses setup (exit 2).

Checks (identical condition in the predicate and the receipt label
C1_R92_PASS=true): selfpin, pin, spec, green (pristine selftest twice),
canary, invalid0, trivial0, inconclusive0, unstable0, note, ids,
mismatched0, figure, witnessed, source, coverage, n_min=12.

Usage: python3 -I measure-v92.py --repo LANE --rev REV --work EMPTY_DIR
Exit: 0 PASS; 1 not PASS; 2 setup refusal.
"""
import argparse, hashlib, io, json, os, re, shutil, subprocess, sys, tarfile

SELF_SHA256 = "6f6ff108d8fcf838c2bab40b5824b179034d0ad05d3a901ae697b7c80cd022c1"
SELF_PIN_RE = rb'^SELF_SHA256 = "[0-9a-f]{64}"\n'

SPEC_PATH = ".ufo/evidence/round-92/c1/census-mutants.json"
SPEC_SHA = "ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290"
NOTE_PATH = "corpus/knowledge/mutation-case-fleet-sources-census.md"
LESSON_PATH = "corpus/lessons/round-92.md"
SOURCE_SID = "S320"
SOURCE_URL = "https://man.archlinux.org/man/sha256sum.1.en"
N_MIN = 12
VERDICTS = ("KILLED", "SURVIVED")
ID_SHAPE = re.compile(r"^[A-Za-z]{1,4}[_-]?[0-9]{1,4}$")


def self_pin_ok():
    """QUALITY 144: the check runs before any other action, on the file's own bytes."""
    try:
        with open(os.path.abspath(__file__), "rb") as f:
            b = f.read()
    except OSError:
        return False
    norm = re.sub(SELF_PIN_RE, b"", b, flags=re.M)
    return hashlib.sha256(norm).hexdigest() == SELF_SHA256


def die(msg):
    print("C1_SETUP " + msg)
    print("C1_R92_PASS=false")
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


def parse_note(nt, spec_ids):
    """Strict note parser (QUALITY 140 + 143).

    Returns (rows, bad). `bad` is non-empty when the note carries any table row
    that is verdict-shaped and is not exactly one spec id in the header-named
    verdict column:
      * any table row carrying a KILLED/SURVIVED token must have a first cell
        that is an id in the spec's set (`out-of-set`, `unkeyed`);
      * every table row whose first cell is id-shaped must be a spec id;
      * a row must carry exactly one verdict token and it must sit at the
        header-named verdict index (`position`);
      * a spec id may key one row (`dup`);
      * no verdict token may sit outside the header-named column.
    Fenced code blocks are skipped: a fenced row is not presented as a table.
    """
    vcol = None
    headers = 0
    rows = {}
    bad = []
    in_fence = False
    for raw in nt.split("\n"):
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        cells = [c.strip() for c in raw.split("|")]
        if len(cells) < 3:
            continue
        low = [c.lower() for c in cells]
        if "verdict" in low:
            if vcol is None:
                vcol = low.index("verdict")
            headers += 1
            continue
        first = cells[1] if len(cells) > 2 else ""
        toks = [c for c in cells if c in VERDICTS]
        shaped = bool(ID_SHAPE.match(first))
        if not toks and not shaped:
            continue
        if not shaped:
            bad.append("unkeyed:" + first[:40])
            continue
        if first not in spec_ids:
            bad.append("out-of-set:" + first)
            continue
        if len(toks) != 1 or vcol is None or vcol >= len(cells) or cells[vcol] not in VERDICTS:
            bad.append("position:" + first)
            continue
        if first in rows:
            bad.append("dup:" + first)
            continue
        rows[first] = cells[vcol]
    return rows, bad, headers


def main():
    if not self_pin_ok():
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
    # sealed gate: refuse a non-empty replace ref in either repo we read.
    for r, label in ((repo, "lane"),):
        p = git(r, "replace", "-l", check=False)
        if p.returncode != 0:
            die("replace-list-failed:" + label)
        if p.stdout.strip():
            die("replace-refs-present:" + label)
    spec_bytes = blob(repo, rev, SPEC_PATH)
    if spec_bytes is None:
        die("spec-absent-at-rev")
    spec_pinned = hashlib.sha256(spec_bytes).hexdigest() == SPEC_SHA
    spec = json.loads(spec_bytes)
    g = spec["gate"]
    fleet = g["repo"]
    p = git(fleet, "replace", "-l", check=False)
    if p.returncode != 0:
        die("replace-list-failed:fleet")
    if p.stdout.strip():
        die("replace-refs-present:fleet")
    gate_bytes = blob(fleet, g["commit"], g["path"])
    if gate_bytes is None:
        die("gate-blob-unreadable")
    pin = hashlib.sha256(gate_bytes).hexdigest() == g["sha256"]
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
        if m["new"] == m["old"]:
            inv.append("noop")
        mtext = gate_text.replace(m["old"], m["new"], 1) if cnt >= 1 else gate_text
        md = os.path.join(work, "m-" + mid)
        mgp = materialize(fleet, g["commit"], g["path"], g["fixtures"], mtext.encode(), md)
        if run(["bash", "-n", mgp], work, md, 30)[0] != 0:
            inv.append("syntax")
        trivial = False
        lrc, lout, lerr = run(["bash", mgp, "validate", "--today", "2026-11-06", clean_lane], work, md, 60)
        if lrc == 2 or lrc is None or b"gawk failed" in lerr or b"syntax error" in lerr:
            trivial = True
        verdicts = []
        for _ in range(runs):
            rc = selftest(mgp, work, to)[0]
            verdicts.append("INCONCLUSIVE" if rc is None else ("SURVIVED" if rc == 0 else "KILLED"))
        if len(set(verdicts)) > 1:
            derived = "UNSTABLE"
        else:
            derived = verdicts[0]
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
            with open(os.path.join(wd, "pristine.out"), "wb") as f:
                f.write(b"rc=%s\n" % str(p1[0]).encode() + p1[1])
            with open(os.path.join(wd, "mutant.out"), "wb") as f:
                f.write(b"rc=%s\n" % str(p2[0]).encode() + p2[1])
        rows.append(dict(id=mid, derived=derived, runs=verdicts, invalid=inv, trivial=trivial,
                         witness=witness))
        shutil.rmtree(md, ignore_errors=True)
    ids = [r["id"] for r in rows]
    spec_ids = set(ids)
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
    ids_ok = figure_ok = False
    mism = 0
    note_rows = {}
    bad = []
    headers = 0
    if note is not None:
        nt = note.decode("utf-8", errors="replace")
        note_rows, bad, headers = parse_note(nt, spec_ids)
        ids_ok = (not bad) and headers == 1 and sorted(note_rows) == sorted(ids)
        mism = sum(1 for r in rows if note_rows.get(r["id"]) != r["derived"])
        heads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", nt, re.M)
        figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n
    # source (QUALITY 143-adjacent: the claim rests on a row opened this round)
    source_ok = False
    sreg = blob(repo, rev, "corpus/SOURCES.md") or b""
    for line in sreg.decode("utf-8", errors="replace").split("\n"):
        l2 = re.sub(r"^ {0,3}", "", line)
        c = [x.strip() for x in l2.split("|")]
        if len(c) >= 13 and c[1] == SOURCE_SID and c[8] == "mined" \
                and LESSON_PATH in c[11]:
            source_ok = True
    lesson = blob(repo, rev, LESSON_PATH)
    source_ok = (source_ok and lesson is not None
                 and SOURCE_SID.encode() in lesson and SOURCE_URL.encode() in lesson)
    readme = (blob(repo, rev, "corpus/README.md") or b"").decode("utf-8", errors="replace")
    coverage_ok = any(l.lstrip().startswith("|") and "knowledge/mutation-case-fleet-sources-census.md" in l
                      for l in readme.split("\n"))
    for r in rows:
        print("C1_ROW %s derived=%s runs=%s note=%s invalid=%s trivial=%s witness=%s" % (
            r["id"], r["derived"], ",".join(r["runs"]), note_rows.get(r["id"], "-"),
            ",".join(r["invalid"]) or "-", int(r["trivial"]), r["witness"]))
    conj = dict(selfpin=True, pin=pin, spec=spec_pinned, green=green, canary=canary,
                invalid0=invalid == 0, trivial0=trivial == 0, inconclusive0=inconclusive == 0,
                unstable0=unstable == 0, note=note is not None, ids=ids_ok,
                mismatched0=(note is not None and mism == 0), figure=figure_ok,
                witnessed=witnessed == survived, source=source_ok, coverage=coverage_ok,
                n_min=n >= N_MIN)
    ok = all(conj.values())
    print("C1_SUMMARY rev=%s n=%d killed=%d survived=%d inconclusive=%d unstable=%d invalid=%d "
          "trivial=%d witnessed=%d/%d note=%s mismatched=%d badrows=%d headers=%d" % (
              rev, n, killed, survived, inconclusive, unstable, invalid, trivial, witnessed,
              survived, note_state, mism, len(bad), headers))
    print("C1_CONJUNCTS " + " ".join("%s=%s" % (k, str(v).lower()) for k, v in conj.items()))
    print("C1_R92_PASS=" + ("true" if ok else "false"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
