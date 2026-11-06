#!/usr/bin/env python3
"""Round-90 C1 counter: an independent re-execution of the case note's table.

Claim R90-C1 (coverage): tameshi holds a reproducible mutation case on the fleet's
own registry gate, scripts/sources-census.sh @ f47ad6ba (the first fleet-root gate
the lane has measured; every earlier leg is a sibling-lane gate). The counter does
NOT read tools/mutate-and-run.sh or any lane-printed figure. It derives every verdict
itself from git objects:

  pin       the gate blob at the spec's fleet commit hashes to the spec's sha256
  spec      the spec at REV hashes to SPEC_SHA (frozen constant below)
  green     the pristine copy's own `selftest` exits 0 and prints `selftest ok`, twice
  canary    the pristine copy with `exit 97` after line 1 exits 97 (the copy is what runs)
  valid     per mutant: old string occurs exactly once, new != old, `bash -n` passes
  trivial   per mutant: `validate` on the fixtures' clean lane c neither exits 2 nor
            prints `gawk failed`/`syntax error` (a mutant that only breaks the program
            is not a measurement)
  verdict   per mutant: selftest in a fresh copy, run twice; rc 0 = SURVIVED,
            rc != 0 = KILLED, timeout = INCONCLUSIVE, two runs differ = UNSTABLE
  witness   per mutant: the spec's witness registry run under pristine and mutant on the
            same directory; `differs` iff (rc, stdout) differ. Every SURVIVED row must
            differ (a survivor proven non-equivalent)
  note      corpus/knowledge/mutation-case-fleet-sources-census.md at REV: one table row
            per spec id (`| Cnn | ... | KILLED|SURVIVED | ...`), each verdict equal to
            the derived one; exactly one line `measured: K/N killed` equal to the
            derived counts
  source    the note's `source:` line cites an S-id > S315 whose SOURCES.md row at REV
            is `mined` and lists the note in `used-by`
  coverage  corpus/README.md at REV has a table row naming the note

C1_R90_PASS=true iff every conjunct holds and n >= 10. There is no override:
every control is a committed state of a scratch clone, read through this same path.

Usage: python3 -I measure.py --repo LANE --rev REV --work EMPTY_DIR
Exit: 0 PASS; 1 not PASS; 2 setup refusal.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tarfile, io

SPEC_PATH = ".ufo/evidence/round-90/c1/census-mutants.json"
SPEC_SHA = "ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290"
NOTE_PATH = "corpus/knowledge/mutation-case-fleet-sources-census.md"
N_MIN = 10
BASE_MAX_SID = 315


def die(msg):
    print("C1_SETUP " + msg)
    print("C1_R90_PASS=false")
    sys.exit(2)


def git(repo, *a, check=True):
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    repo = os.path.realpath(a.repo)
    work = os.path.realpath(a.work)
    if not os.path.isdir(work) or os.listdir(work):
        die("work-not-empty-dir")
    rev = git(repo, "rev-parse", "--verify", a.rev + "^{commit}").stdout.decode().strip()
    spec_bytes = blob(repo, rev, SPEC_PATH)
    if spec_bytes is None:
        die("spec-absent-at-rev")
    spec_pinned = hashlib.sha256(spec_bytes).hexdigest() == SPEC_SHA
    spec = json.loads(spec_bytes)
    g = spec["gate"]
    fleet = g["repo"]
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
    n = len(rows)
    killed = sum(r["derived"] == "KILLED" for r in rows)
    survived = sum(r["derived"] == "SURVIVED" for r in rows)
    inconclusive = sum(r["derived"] == "INCONCLUSIVE" for r in rows)
    unstable = sum(r["derived"] == "UNSTABLE" for r in rows)
    invalid = sum(bool(r["invalid"]) for r in rows)
    trivial = sum(r["trivial"] for r in rows)
    witnessed = sum(r["derived"] == "SURVIVED" and r["witness"] == "differs" for r in rows)

    # note
    note = blob(repo, rev, NOTE_PATH)
    note_state = "present" if note is not None else "absent"
    ids_ok = figure_ok = source_ok = False
    mism = 0
    note_rows = {}
    dup = False
    if note is not None:
        nt = note.decode("utf-8", errors="replace")
        for line in nt.split("\n"):
            mm = re.match(r"^\|\s*(C\d\d)\s*\|(.*)\|\s*$", line)
            if not mm:
                continue
            cells = [c.strip() for c in mm.group(2).split("|")]
            vs = [c for c in cells if c in ("KILLED", "SURVIVED")]
            if len(vs) != 1:
                continue
            if mm.group(1) in note_rows:
                dup = True
            note_rows[mm.group(1)] = vs[0]
        ids_ok = (not dup) and sorted(note_rows) == sorted(ids)
        mism = sum(1 for r in rows if note_rows.get(r["id"]) != r["derived"])
        heads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", nt, re.M)
        figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n
        src = [l for l in nt.split("\n") if l.startswith("source:")]
        cited = set(re.findall(r"\bS(\d{3,})\b", src[0])) if len(src) == 1 else set()
        sreg = blob(repo, rev, "corpus/SOURCES.md") or b""
        for sid in sorted(cited):
            if int(sid) <= BASE_MAX_SID:
                continue
            for line in sreg.decode("utf-8", errors="replace").split("\n"):
                l2 = re.sub(r"^ {0,3}", "", line)
                c = [x.strip() for x in l2.split("|")]
                if len(c) >= 13 and c[1] == "S" + sid and c[8] == "mined" and NOTE_PATH in c[11]:
                    source_ok = True
    readme = (blob(repo, rev, "corpus/README.md") or b"").decode("utf-8", errors="replace")
    coverage_ok = any(l.lstrip().startswith("|") and "knowledge/mutation-case-fleet-sources-census.md" in l
                      for l in readme.split("\n"))

    for r in rows:
        print("C1_ROW %s derived=%s runs=%s note=%s invalid=%s trivial=%s witness=%s" % (
            r["id"], r["derived"], ",".join(r["runs"]), note_rows.get(r["id"], "-"),
            ",".join(r["invalid"]) or "-", int(r["trivial"]), r["witness"]))
    conj = dict(pin=pin, spec=spec_pinned, green=green, canary=canary, invalid0=invalid == 0,
                trivial0=trivial == 0, inconclusive0=inconclusive == 0, unstable0=unstable == 0,
                note=note is not None, ids=ids_ok, mismatched0=(note is not None and mism == 0),
                figure=figure_ok, witnessed=witnessed == survived, source=source_ok,
                coverage=coverage_ok, n_min=n >= N_MIN)
    ok = all(conj.values())
    print("C1_SUMMARY rev=%s n=%d killed=%d survived=%d inconclusive=%d unstable=%d invalid=%d "
          "trivial=%d witnessed=%d/%d note=%s mismatched=%d" % (
              rev, n, killed, survived, inconclusive, unstable, invalid, trivial, witnessed,
              survived, note_state, mism))
    print("C1_CONJUNCTS " + " ".join("%s=%s" % (k, str(v).lower()) for k, v in conj.items()))
    print("C1_R90_PASS=" + ("true" if ok else "false"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
