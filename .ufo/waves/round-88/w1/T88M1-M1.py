#!/usr/bin/env python3
"""tameshi round-88 C1 counter — the fleet mutation ledger's governed sibling gates,
counted by an INDEPENDENT replay of every declared leg (the runner's own output is
never the count).

Question: at revision REV of the lane, how many ledger legs declared in
`tools/mutate-and-run.sh` are (a) a sibling lane's committed gate, (b) pinned to the
bytes their recorded sha256 names, (c) run through an allow-listed suite whose
interpreter matches the gate's language, and (d) reproduced verdict-for-verdict by
this counter's own control + mutant replay? And is one of them the round-88
pre-registered Python leg?

Population: every `regression_case_git` call in the runner bytes at REV (read with
`git cat-file blob REV:tools/mutate-and-run.sh` — never the worktree). For each call the
counter resolves the leg's PIN_/REV_/TABLE_ variables and its embedded spec heredoc
from the same bytes, then:

  1. repo  = FLEET/<first path component>; it must be its own git toplevel, must not be
             the lane repo, and its directory must not be `tameshi-shokunin`;
  2. rev   = a commit whose author email does not contain `tameshi`, reachable from a
             remote-tracking ref of that repo (`refs/remotes/origin/*`);
  3. pin   = sha256(git show rev:path) equals the recorded PIN_;
  4. suite = byte-equal to one of SUITES below, and the suite's interpreter matches the
             target extension (.mjs node, .sh bash, .py python3);
  5. spec  = parses under spec format v1; >= 10 defects; ids unique; the recorded TABLE_
             carries exactly the spec's ids;
  6. replay: the pristine (control) run exits 0; every mutant (one exact edit,
             count==1, no-op refused) gets KILLED (exit not in {0,124,126,127}) or
             SURVIVED (exit 0); INCONCLUSIVE fails the leg; every verdict equals the
             recorded TABLE_; at least one KILLED;
  7. distinct (repo, path) target.

A leg that meets 1-7 is `counted`. The Python leg must additionally carry the
pre-registered spec bytes (sha256 PREREG_SHA, committed before any mutant ran).

Runner consistency (necessary, never sufficient): the REV runner, extracted into a
scratch fleet whose sibling dirs are symlinks to the real repos, runs `--regression`;
its exit and final `REGRESSION:` line are recorded.

Output:
  C1_LEG <name> lang=<l> target=<rel>@<rev12> counted=<yes|no> agree=<a>/<n> killed=<k> reason=<r>
  C1_R88 rev=<REV> declared=<d> legs=<counted> python_legs=<p> prereg=<ok|absent|mismatch> runner=<state> C1_R88_PASS=<true|false>

Frozen predicate (plans/round-88.plan.md): declared=11 legs=11 python_legs=1 prereg=ok
runner=PASS(cases=11 passed=11) — and only then C1_R88_PASS=true.
Exit: 0 PASS true, 1 PASS false, 2 setup refusal (no summary line).
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PREREG_SHA = "724beed385222b6342dc6d3af5ad19ae605bca8101f983f3ce58da905492689e"
TARGET_LEGS = 11
SANDBOX = ('h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i '
           'PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C ')
SUITES = {
    'node "$MUTANT" --selftest': "node",
    'bash "$MUTANT" --selftest': "bash",
    SANDBOX + 'GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest': "node",
    SANDBOX + 'bash "$MUTANT" --selftest': "bash",
    SANDBOX + 'GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" python3 -I "$MUTANT" --selftest': "python3",
}
LANG_OF_EXT = {".mjs": ("js", "node"), ".sh": ("bash", "bash"), ".py": ("py", "python3")}
TIMEOUT_S = 120


class Setup(Exception):
    pass


def trusted_git() -> str:
    for d in ("/usr/bin", "/bin"):
        p = os.path.join(d, "git")
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    raise Setup("no git in /usr/bin:/bin")


GIT = None


def git(repo, *args, check=True) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    r = subprocess.run([GIT, "-C", str(repo), *args], capture_output=True, env=env)
    if check and r.returncode != 0:
        raise Setup("git %s failed in %s: %s" % (" ".join(args), repo, r.stderr.decode(errors="replace").strip()))
    return r


LEG_RE = re.compile(
    r"^  regression_case_git (\S+) \\\n"
    r"\s+'([^']+)' \"\$(PIN_\w+)\" \"\$(REV_\w+)\" \\\n"
    r"\s+\"\$specs/([^\"]+)\.spec\" '([^']*)' \"\$(TABLE_\w+)\" \\\n"
    r"\s+\"\$root/([^\"]+)\"\n", re.M)
VAR_RE = re.compile(r"^((?:PIN|REV)_\w+)=([0-9a-f]+)$|^(TABLE_\w+)='([^']*)'$", re.M)
SPEC_RE = re.compile(r"^  cat >\"\$d/([^\"]+)\.spec\" <<'EOT'\n(.*?)^EOT\n", re.M | re.S)
ESC = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\"}


def unescape(s: str) -> str:
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            if i + 1 >= len(s) or s[i + 1] not in ESC:
                raise ValueError("bad escape")
            out.append(ESC[s[i + 1]])
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def parse_spec(text: str) -> list[dict]:
    defects, cur = [], None
    for line in text.split("\n"):
        if line == "" or line.startswith("#"):
            continue
        if line.startswith("@defect"):
            rest = line[len("@defect"):].lstrip(" ")
            did = rest.partition("|")[0].strip()
            if not re.fullmatch(r"[A-Za-z0-9._-]+", did) or any(d["id"] == did for d in defects):
                raise ValueError("bad/duplicate id %r" % did)
            cur = {"id": did}
            defects.append(cur)
        elif line == "@old" or line.startswith("@old "):
            if cur is None or "old" in cur:
                raise ValueError("stray @old")
            cur["old"] = unescape(line[5:])
        elif line == "@new" or line.startswith("@new "):
            if cur is None or "new" in cur:
                raise ValueError("stray @new")
            cur["new"] = unescape(line[5:])
        else:
            raise ValueError("unrecognized line %r" % line[:60])
    for d in defects:
        if not d.get("old") or "new" not in d or d["old"] == d["new"]:
            raise ValueError("defect %s incomplete or no-op" % d["id"])
    return defects


def run_suite(suite: str, mutant: Path, pristine: Path, workdir: Path, did: str) -> int:
    env = dict(os.environ)
    env.update(MUTANT=str(mutant), TARGET=str(pristine), PRISTINE=str(pristine),
               WORKDIR=str(workdir), DEFECT_ID=did)
    try:
        r = subprocess.run(["bash", "-c", suite], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, cwd=str(workdir), env=env, timeout=TIMEOUT_S)
        return r.returncode
    except subprocess.TimeoutExpired:
        return 124


def verdict(rc: int) -> str:
    if rc == 0:
        return "SURVIVED"
    if rc in (124, 126, 127):
        return "INCONCLUSIVE"
    return "KILLED"


def replay_leg(leg, fleet: Path, lane_real: str, work: Path, seen: set) -> dict:
    name, rel = leg["name"], leg["rel"]
    out = {"name": name, "rel": rel, "rev12": leg["rev"][:12], "lang": "?", "counted": False,
           "agree": 0, "n": 0, "killed": 0, "reason": "", "spec_sha": leg["spec_sha"]}
    ext = os.path.splitext(rel)[1]
    if ext not in LANG_OF_EXT:
        out["reason"] = "unknown-extension"
        return out
    out["lang"], interp = LANG_OF_EXT[ext]
    top, _, path = rel.partition("/")
    repo = fleet / top
    if not repo.is_dir():
        out["reason"] = "not-a-sibling-repo"
        return out
    real = os.path.realpath(repo)
    if real == lane_real:
        out["reason"] = "lane-repo"
        return out
    tl = git(repo, "rev-parse", "--show-toplevel", check=False)
    if tl.returncode != 0 or os.path.realpath(tl.stdout.decode().strip()) != real:
        out["reason"] = "repo-identity"
        return out
    rev = leg["rev"]
    if git(repo, "cat-file", "-t", rev, check=False).stdout.decode().strip() != "commit":
        out["reason"] = "rev-not-commit"
        return out
    email = git(repo, "log", "-1", "--format=%ae", rev).stdout.decode().strip()
    if "tameshi" in email.lower():
        out["reason"] = "lane-authored-rev"
        return out
    refs = git(repo, "for-each-ref", "--format=%(refname)", "--contains", rev, "refs/remotes/origin/").stdout.decode().split()
    if not refs:
        out["reason"] = "rev-not-on-remote"
        return out
    blob = git(repo, "show", "%s:%s" % (rev, path), check=False)
    if blob.returncode != 0:
        out["reason"] = "path-not-in-rev"
        return out
    if hashlib.sha256(blob.stdout).hexdigest() != leg["pin"]:
        out["reason"] = "pin-mismatch"
        return out
    key = (real, path)
    if key in seen:
        out["reason"] = "duplicate-target"
        return out
    if SUITES.get(leg["suite"]) != interp:
        out["reason"] = "suite-not-allowed"
        return out
    try:
        defects = parse_spec(leg["spec"])
    except ValueError as e:
        out["reason"] = "spec-invalid:" + re.sub(r"\s+", "_", str(e))[:40]
        return out
    table = dict(p.split(":", 1) for p in leg["table"].split(",") if ":" in p)
    if len(defects) < 10 or set(table) != {d["id"] for d in defects} or len(table) != len(leg["table"].split(",")):
        out["reason"] = "spec-table-ids"
        return out
    mode = git(repo, "ls-tree", rev, "--", path).stdout.decode().split()
    lw = work / name
    lw.mkdir(parents=True)
    base = "target." + os.path.basename(path)
    pristine = lw / ("pristine." + base)
    pristine.write_bytes(blob.stdout)
    if mode and mode[0] == "100755":
        pristine.chmod(0o755)
    if run_suite(leg["suite"], pristine, pristine, lw, "CONTROL") != 0:
        out["reason"] = "control-red"
        return out
    out["n"] = len(defects)
    for d in defects:
        old, new = d["old"].encode(), d["new"].encode()
        if blob.stdout.count(old) != 1:
            out["reason"] = "old-count-%s" % d["id"]
            return out
        m = lw / ("mutant-%s.%s" % (d["id"], base))
        m.write_bytes(blob.stdout.replace(old, new, 1))
        m.chmod(pristine.stat().st_mode & 0o777)
        v = verdict(run_suite(leg["suite"], m, pristine, lw, d["id"]))
        if v == "KILLED":
            out["killed"] += 1
        if v == table[d["id"]]:
            out["agree"] += 1
        elif not out["reason"]:
            out["reason"] = "flip-%s:%s->%s" % (d["id"], table[d["id"]], v)
    if out["agree"] == out["n"] and out["killed"] >= 1:
        out["counted"] = True
        out["reason"] = "ok"
        seen.add(key)
    elif not out["reason"]:
        out["reason"] = "no-kill"
    return out


def main() -> int:
    global GIT
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--fleet", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    try:
        GIT = trusted_git()
        lane = Path(a.repo).resolve()
        fleet = Path(a.fleet).resolve()
        work = Path(a.work)
        if work.exists() and any(work.iterdir()):
            raise Setup("--work must be empty or absent")
        work.mkdir(parents=True, exist_ok=True)
        rev = git(lane, "rev-parse", "--verify", a.rev + "^{commit}").stdout.decode().strip()
        runner = git(lane, "cat-file", "blob", "%s:tools/mutate-and-run.sh" % rev).stdout
        text = runner.decode("utf-8")
        vars_: dict[str, str] = {}
        for m in VAR_RE.finditer(text):
            k, v = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            if k in vars_:
                raise Setup("duplicate variable %s" % k)
            vars_[k] = v
        specs = {}
        for m in SPEC_RE.finditer(text):
            if m.group(1) in specs:
                raise Setup("duplicate spec %s" % m.group(1))
            specs[m.group(1)] = m.group(2)
        legs = []
        for m in LEG_RE.finditer(text):
            name, rel, pv, rv, sname, suite, tv, _ = m.groups()
            if pv not in vars_ or rv not in vars_ or tv not in vars_ or sname not in specs:
                raise Setup("leg %s references an undefined variable or spec" % name)
            legs.append({"name": name, "rel": rel, "pin": vars_[pv], "rev": vars_[rv], "suite": suite,
                         "table": vars_[tv], "spec": specs[sname],
                         "spec_sha": hashlib.sha256(specs[sname].encode()).hexdigest()})
        if not legs:
            raise Setup("no regression_case_git legs parsed")
        if len({l["name"] for l in legs}) != len(legs):
            raise Setup("duplicate leg name")
    except (Setup, UnicodeDecodeError) as e:
        print("C1_R88 SETUP %s" % e, file=sys.stderr)
        return 2

    seen: set = set()
    results = [replay_leg(l, fleet, str(lane), work / "replay", seen) for l in legs]
    for r in results:
        print("C1_LEG %s lang=%s target=%s@%s counted=%s agree=%d/%d killed=%d reason=%s" % (
            r["name"], r["lang"], r["rel"], r["rev12"], "yes" if r["counted"] else "no",
            r["agree"], r["n"], r["killed"], r["reason"]))
    counted = [r for r in results if r["counted"]]
    py = [r for r in counted if r["lang"] == "py"]
    if not py:
        prereg = "absent"
    elif len(py) == 1 and py[0]["spec_sha"] == PREREG_SHA:
        prereg = "ok"
    else:
        prereg = "mismatch"

    # Runner consistency: the REV runner in a scratch fleet (symlinked siblings).
    sf = work / "fleet"
    (sf / "tameshi-shokunin" / "tools").mkdir(parents=True)
    rp = sf / "tameshi-shokunin" / "tools" / "mutate-and-run.sh"
    rp.write_bytes(runner)
    rp.chmod(0o755)
    for top in sorted({l["rel"].partition("/")[0] for l in legs}):
        if top != "tameshi-shokunin" and (fleet / top).is_dir() and not (sf / top).exists():
            (sf / top).symlink_to(fleet / top)
    env = dict(os.environ)
    env["TMPDIR"] = str(work)
    rr = subprocess.run(["bash", str(rp), "--regression", "--workdir", str(work / "runner")],
                        capture_output=True, env=env, cwd=str(work))
    last = [ln for ln in rr.stdout.decode(errors="replace").splitlines() if ln.startswith("REGRESSION: ")]
    m = re.match(r"REGRESSION: PASS \(cases=(\d+) passed=(\d+);", last[-1]) if last else None
    if rr.returncode == 0 and m and m.group(1) == m.group(2):
        runner_state = "PASS(cases=%s passed=%s)" % (m.group(1), m.group(2))
    else:
        runner_state = "FAIL(exit=%d)" % rr.returncode
    ok = (len(legs) == TARGET_LEGS and len(counted) == TARGET_LEGS and len(py) == 1 and prereg == "ok"
          and runner_state == "PASS(cases=%d passed=%d)" % (TARGET_LEGS, TARGET_LEGS))
    print("C1_R88 rev=%s declared=%d legs=%d python_legs=%d prereg=%s runner=%s C1_R88_PASS=%s" % (
        rev, len(legs), len(counted), len(py), prereg, runner_state, "true" if ok else "false"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
