#!/usr/bin/env python3
"""Round-55 C2 counter (operability): one line, one exit class, every mode.

Round 54 made a set-but-unusable `TMPDIR` exit 2 (could-not-evaluate) in the
self-test of each of the seven tools that call `strict_scratch_root()`. It left
two gaps this counter measures:

  * the CLASS is not one line: `repeat-control` and `context-capture` print the
    raw exception type (`setup: RuntimeError:` / `SELFTEST: FAIL (setup error:
    RuntimeError:`) and `context-capture` prints it on stdout, so a caller cannot
    parse the class uniformly; and
  * only the self-test was measured, so `env-diff --contract` (the one other
    documented mode that allocates scratch) was outside the contract.

Arms (frozen):

  grammar  8 allocating modes (the seven self-tests + `env-diff --contract`):
           with TMPDIR set to a nonexistent path, exit 2, at least one STDERR
           line matching GRAMMAR, and no `RuntimeError`/`Traceback` on either
           stream;
  lazy     5 non-allocating modes keep their expected exit under the same
           unusable TMPDIR (scratch is allocated lazily, never at parse time);
  empty    13 modes with TMPDIR="" (declared unset) exit their expected code;
  usable   13 modes with a fresh TMPDIR exit their expected code, and the eight
           allocating modes issue no mkdir under /tmp (strace census);
  docs     the seven registry `scratch_root` cells carry the GRAMMAR marker;
  note     `corpus/knowledge/scratch-root-contract.md` states the grammar and
           names all eight allocating modes;
  skill    `SKILL.md` carries the grammar marker.

Verdict line:
`C2_R55: rev=... grammar=N/8 lazy=N/5 empty=N/13 usable=N/13 tmp_mkdirs=N docs=N/7 note=N/8 skill=N/1 total=N C2_R55_PASS=true|false`
Exit 0 iff PASS, 1 on a failed arm, 2 on setup error. --work must be empty; the
clone, arm scratch and receipts live under it.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

MARKER = "could-not-evaluate: cannot create clone scratch under the scratch root"
GRAMMAR = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone "
    r"scratch under the scratch root: TMPDIR is not a usable directory: '.+' "
    r"\(could-not-evaluate\)$")
FIXTURE = ".ufo/evidence/round-12/BaselineControl/fixtures/target.sh"
CONTRACT = ".ufo/evidence/round-55/c2/fixture-contract.json"
NOTE = "corpus/knowledge/scratch-root-contract.md"
SEVEN = ("env-diff", "repeat-control", "registry-check", "bash-witness-study",
         "pin-disposition", "evidence-disposition", "context-capture")
TIMEOUT = 900


class Setup(Exception):
    pass


def env_with(tmpdir):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    if tmpdir is None:
        env.pop("TMPDIR", None)
    else:
        env["TMPDIR"] = tmpdir
    return env


def git(cwd, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True,
                          text=True, env=env)


def modes(work, clone):
    """(id, argv, expected_exit, allocating, cheap) -- benches run with cwd=clone.

    `allocating` modes must carry the grammar on a set-but-unusable TMPDIR.
    `cheap` modes also run the empty/usable arms: `registry-check --rev` builds a
    full fleet clone (minutes), so it is measured on the grammar arm only and its
    usable path stays covered by the tool's own self-test (amendment 6)."""
    out = []
    selftests = (
        ("repeat-control", ["python3", "tools/repeat-control.py", "--selftest"]),
        ("registry-check", ["python3", "tools/registry-check.py", "--selftest"]),
        ("bash-witness-study", ["python3", "tools/bash-witness-study.py", "selftest"]),
        ("pin-disposition", ["python3", "tools/pin-disposition.py", "--selftest"]),
        ("evidence-disposition", ["python3", "tools/evidence-disposition.py", "--selftest"]),
        ("context-capture", ["python3", "tools/context-capture.py", "--selftest"]),
    )
    for tool, argv in selftests:
        # The label is the mode AS INVOKED: bash-witness-study takes a subcommand,
        # not a --selftest flag (amendment 3).
        label = "%s selftest" % tool if tool == "bash-witness-study" else "%s --selftest" % tool
        out.append((label, argv, 0, True, True))
    out.append(("env-diff --selftest", ["python3", "tools/env-diff.py", "--selftest"], 0, True, True))
    out.append(("env-diff --contract",
                ["python3", "tools/env-diff.py", "--contract", CONTRACT,
                 "--out", str(work / "envdiff-out.json"), "--fleet-root", str(clone)],
                0, True, True))
    out.append(("registry-check --rev",
                ["python3", "tools/registry-check.py", "--rev", "HEAD"], 0, True, False))
    out += [
        ("repeat-control --snapshot",
         ["python3", "tools/repeat-control.py", "--snapshot",
          ".ufo/evidence/round-12/ControlGate"], 0, False, True),
        ("bash-witness-study count",
         ["python3", "tools/bash-witness-study.py", "count"], 0, False, True),
        ("pin-disposition --read",
         ["python3", "tools/pin-disposition.py", "--manifest",
          ".ufo/evidence/round-13/pin-manifest.json",
          "--root", "/home/vgpnk/Projects/shokunin"], 0, False, True),
        ("evidence-disposition --json",
         ["python3", "tools/evidence-disposition.py", "--root", ".",
          "--dispositions", ".ufo/evidence/round-18/dispositions.json", "--json"], 0, False, True),
        ("context-capture --check",
         ["python3", "tools/context-capture.py", "--check", "--json"], 0, False, True),
    ]
    return out


def run(argv, cwd, env):
    try:
        p = subprocess.run(argv, cwd=str(cwd), env=env, capture_output=True,
                           text=True, timeout=TIMEOUT)
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"


def trace(argv, cwd, env, log):
    try:
        p = subprocess.run(["strace", "-f", "-e", "trace=mkdir,mkdirat",
                            "-o", str(log), *argv],
                           cwd=str(cwd), env=env, capture_output=True, text=True,
                           timeout=TIMEOUT)
        return p.returncode
    except subprocess.TimeoutExpired:
        return 124


def tmp_mkdirs(log):
    if not log.exists():
        return None
    hits = 0
    for line in log.read_text(errors="replace").splitlines():
        if "mkdir" in line and '"/tmp' in line:
            hits += 1
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--explain", action="store_true")
    a = ap.parse_args()
    lane, work = Path(a.lane).resolve(), Path(a.work)
    if not (lane / ".git").exists():
        raise Setup("lane is not a git repository: %s" % lane)
    if not work.exists() or any(work.iterdir()):
        raise Setup("--work must be an existing empty directory: %s" % work)
    for exe in ("git", "python3", "strace"):
        if not shutil.which(exe):
            raise Setup("required executable missing: %s" % exe)
    clone = work / "clone"
    r = git(work, "clone", "--shared", "--no-checkout", str(lane), str(clone))
    if r.returncode:
        raise Setup("clone failed: %s" % r.stderr.strip())
    # The clone's HEAD is put on a local branch, not detached: one measured mode
    # (evidence-disposition --root .) classifies a detached HEAD as
    # historical_input_unavailable, so a detached checkout would score the clone's
    # shape instead of the tool. Amendment 1, before any deciding invocation.
    r = git(clone, "checkout", "-q", "-B", "r55-rev", a.rev)
    if r.returncode:
        raise Setup("checkout of %s failed: %s" % (a.rev, r.stderr.strip()))
    if not (clone / FIXTURE).exists():
        raise Setup("fixture missing at %s: %s" % (a.rev, FIXTURE))
    fixture_sha = hashlib.sha256((clone / FIXTURE).read_bytes()).hexdigest()
    # The contract is materialized from these frozen bytes into the clone, so the mode is
    # measurable at every revision (the round's own files do not exist at the base tree).
    (clone / CONTRACT).parent.mkdir(parents=True, exist_ok=True)
    (clone / CONTRACT).write_text(json.dumps({"surfaces": [
        {"name": "stable", "repo": ".", "rev": "HEAD", "path": FIXTURE,
         "interp": "bash"}]}, indent=1) + "\n")

    table = modes(work, clone)
    allocating = [m for m in table if m[3]]
    lazy = [m for m in table if not m[3]]
    cheap = [m for m in table if m[4]]
    bad = {}

    unusable = str(work / "no-such-tmpdir")
    for name, argv, _exp, _alloc, _cheap in allocating:
        rc, out, err = run(argv, clone, env_with(unusable))
        ok = rc == 2 and any(GRAMMAR.match(l) for l in (err + "\n" + out).splitlines()) \
            and "RuntimeError" not in err + out and "Traceback" not in err + out
        if not ok:
            bad[name] = "grammar rc=%s stderr=%r" % (rc, err.strip().splitlines()[:2])
        if a.explain:
            print("EXPLAIN grammar %-34s rc=%-2s %s" % (name, rc, "ok" if ok else "FAIL"))

    for name, argv, exp, _alloc, _cheap in lazy:
        rc, out, err = run(argv, clone, env_with(unusable))
        ok = rc == exp
        if not ok:
            bad["lazy:" + name] = "rc=%s expected=%s" % (rc, exp)
        if a.explain:
            print("EXPLAIN lazy %-37s rc=%-2s %s" % (name, rc, "ok" if ok else "FAIL"))

    empty_ok = usable_ok = 0
    (work / "tmp-usable").mkdir()
    for arm, tmpdir in (("empty", ""), ("usable", str(work / "tmp-usable"))):
        for name, argv, exp, alloc, _cheap in cheap:
            rc, _out, _err = run(argv, clone, env_with(tmpdir))
            if arm == "usable" and alloc:
                # The census run supplies ONLY the /tmp mkdir count: under
                # `strace -f` a tool's own timing cases can fail from tracer
                # overhead (round 54's amendment 2, re-learned here by the base
                # receipt: registry-check rc 1 under the tracer alone), so the
                # exit code is the plain run's (amendment 4).
                log = work / ("strace-%s.log" % re.sub(r"[^a-z0-9]+", "-", name.lower()))
                trace(argv, clone, env_with(tmpdir), log)
                n = tmp_mkdirs(log)
                if n is None:
                    bad["strace:" + name] = "no trace log"
                elif n:
                    bad["tmp_mkdirs:" + name] = "%d mkdir under /tmp" % n
            ok = rc == exp
            if arm == "empty":
                empty_ok += 1 if ok else 0
            else:
                usable_ok += 1 if ok else 0
            if not ok:
                bad["%s:%s" % (arm, name)] = "rc=%s expected=%s" % (rc, exp)
            if a.explain:
                print("EXPLAIN %-6s %-34s rc=%-2s %s" % (
                    arm, name, rc, "ok" if ok else "FAIL"))

    reg = json.loads((clone / "tools/registry.json").read_text())
    cells = [row for row in reg["rows"]
             if row.get("scratch_root") and any(t in " ".join(row.get("argv", []))
                                                for t in ("tools/%s.py" % t for t in SEVEN))]
    docs = sum(1 for row in cells if MARKER in row["scratch_root"])
    if len(cells) != 7:
        bad["docs"] = "expected 7 scratch_root cells, found %d" % len(cells)
    # The marker and the mode ids are matched against whitespace-normalized text:
    # both documents are hard-wrapped near 78 columns, so a line break inside the
    # grammar is a typographic fact, not a missing statement (amendment 2).
    def norm(text):
        return " ".join(text.split())

    note_txt = norm((clone / NOTE).read_text()) if (clone / NOTE).exists() else ""
    note_names = [m for m in allocating if m[0] in note_txt]
    note = len(note_names)
    skill = 1 if MARKER in norm((clone / "SKILL.md").read_text()) else 0
    for arm, got, want in (("docs", docs, 7), ("note", note, len(allocating)), ("skill", skill, 1)):
        if got != want:
            bad.setdefault(arm, "%d/%d" % (got, want))
        if a.explain:
            print("EXPLAIN %-6s %-34s %d/%d %s" % (
                arm, "", got, want, "ok" if got == want else "FAIL"))

    grammar_ok = sum(1 for m in allocating if m[0] not in bad)
    lazy_ok = sum(1 for m in lazy if "lazy:" + m[0] not in bad)
    tmp_total = sum(int(v.split()[0]) for k, v in bad.items() if k.startswith("tmp_mkdirs:"))
    total = (len(allocating) - grammar_ok) + (len(lazy) - lazy_ok) \
        + (len(table) - empty_ok) + (len(table) - usable_ok) \
        + tmp_total + (7 - docs) + (8 - note) + (1 - skill)
    receipts = {"rev": a.rev, "fixture_sha256": fixture_sha, "bad": bad,
                "grammar": grammar_ok, "lazy": lazy_ok, "empty": empty_ok,
                "usable": usable_ok, "docs": docs, "note": note, "skill": skill,
                "allocating": [m[0] for m in allocating], "note_names": note_names}
    (work / "c2-receipts.json").write_text(json.dumps(receipts, indent=1, sort_keys=True) + "\n")
    print("C2_R55: rev=%s grammar=%d/%d lazy=%d/%d empty=%d/%d usable=%d/%d "
          "tmp_mkdirs=%d docs=%d/7 note=%d/9 skill=%d/1 total=%d C2_R55_PASS=%s" % (
              a.rev[:12], grammar_ok, len(allocating), lazy_ok, len(lazy),
              empty_ok, len(cheap), usable_ok, len(cheap), tmp_total, docs, note,
              skill, total, "true" if total == 0 and not bad else "false"))
    return 0 if total == 0 and not bad else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("C2_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
        sys.exit(2)
