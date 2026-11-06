#!/usr/bin/env python3
"""T88R1 (round-88 w1) probe — re-executable corroboration for the correctness review
of the frozen counter (.ufo/evidence/round-88/measure.py) and the leg-11 wiring in
tools/mutate-and-run.sh at 28ec58858a084bc193a89ca5b0a751942694ccfb.

Static: prereg sha chain (worktree spec == spec@6998726f == runner-embedded heredoc ==
measure.py PREREG_SHA), gate pin/mode/lines, counter LEG_RE parse of the candidate
runner, leg-11 suite byte-equality to measure.py's SUITES python entry, @old count==1
against the pinned kake blob.
Live: control + all 10 prereg mutants under the exact sandboxed py suite (env -i,
python3 -I, per-defect sandbox), verdicts mapped by measure.py's verdict() rule and
compared to TABLE_KAKEGUARD extracted from the runner bytes.

Read-only on the fleet; writes only under /fast/scratch/hyaku/tameshi-r88/T88R1/ and
the optional --out file.
usage: python3 -I T88R1-probe.py [--out FILE]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
KAKE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
CAND = "28ec58858a084bc193a89ca5b0a751942694ccfb"
GATE_REV = "e8d3a924249983972e5163d160cf236487986c55"
GATE_REL = "scripts/ledger_append_guard.py"
PREREG_SHA = "724beed385222b6342dc6d3af5ad19ae605bca8101f983f3ce58da905492689e"
SCRATCH = Path("/fast/scratch/hyaku/tameshi-r88/T88R1")

SANDBOX = ('h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i '
           'PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C ')
PY_SUITE = (SANDBOX + 'GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" '
            'python3 -I "$MUTANT" --selftest')

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
        if s[i] == "\\":
            out.append(ESC[s[i + 1]])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def blob(repo: str, rev: str, path: str) -> bytes:
    r = subprocess.run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (rev, path)],
                       capture_output=True)
    if r.returncode != 0:
        raise SystemExit("cat-file failed: %s:%s in %s" % (rev, path, repo))
    return r.stdout


def parse_spec(text: str) -> list[dict]:
    defects, cur = [], None
    for line in text.split("\n"):
        if line == "" or line.startswith("#"):
            continue
        if line.startswith("@defect"):
            cur = {"id": line[len("@defect"):].lstrip(" ").partition("|")[0].strip()}
            defects.append(cur)
        elif line.startswith("@old "):
            cur["old"] = unescape(line[5:])
        elif line.startswith("@new "):
            cur["new"] = unescape(line[5:])
    return defects


def verdict(rc: int) -> str:
    if rc == 0:
        return "SURVIVED"
    if rc in (124, 126, 127):
        return "INCONCLUSIVE"
    return "KILLED"


def run_suite(suite: str, mutant: Path, pristine: Path, workdir: Path, did: str) -> int:
    env = dict(os.environ)
    env.update(MUTANT=str(mutant), TARGET=str(pristine), PRISTINE=str(pristine),
               WORKDIR=str(workdir), DEFECT_ID=did)
    try:
        r = subprocess.run(["bash", "-c", suite], stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           cwd=str(workdir), env=env, timeout=120)
        return r.returncode
    except subprocess.TimeoutExpired:
        return 124


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    res: dict = {}

    spec_file = Path(LANE, ".ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec").read_bytes()
    spec_ctl = blob(LANE, "6998726ff2fc554b399007cd3a8a92e8178f7da5",
                    ".ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec")
    cand = blob(LANE, CAND, "tools/mutate-and-run.sh").decode("utf-8")
    gate = blob(KAKE, GATE_REV, GATE_REL)
    text = cand

    specs = {m.group(1): m.group(2) for m in SPEC_RE.finditer(text)}
    vars_ = {}
    for m in VAR_RE.finditer(text):
        k, v = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        vars_.setdefault(k, v)
    res["sha_chain"] = {
        "worktree_spec": hashlib.sha256(spec_file).hexdigest(),
        "spec_at_6998726f": hashlib.sha256(spec_ctl).hexdigest(),
        "embedded_heredoc": hashlib.sha256(specs["py-kake-ledger-guard"].encode()).hexdigest(),
        "PREREG_SHA": PREREG_SHA,
        "all_equal": len({hashlib.sha256(spec_file).hexdigest(),
                          hashlib.sha256(spec_ctl).hexdigest(),
                          hashlib.sha256(specs["py-kake-ledger-guard"].encode()).hexdigest(),
                          PREREG_SHA}) == 1,
    }
    ls = subprocess.run(["git", "-C", KAKE, "ls-tree", GATE_REV, "--", GATE_REL],
                        capture_output=True, text=True).stdout.split()
    res["gate"] = {"sha256": hashlib.sha256(gate).hexdigest(),
                   "pin_in_runner": vars_.get("PIN_KAKEGUARD"),
                   "mode": ls[0] if ls else "?", "lines": gate.count(b"\n"),
                   "pin_match": hashlib.sha256(gate).hexdigest() == vars_.get("PIN_KAKEGUARD")}
    legs = {m.group(1): m.groups() for m in LEG_RE.finditer(text)}
    res["legs_parsed"] = sorted(legs)
    leg11 = legs.get("py-kake-ledger-guard")
    res["leg11_suite_eq_measure_py_entry"] = bool(leg11) and leg11[5] == PY_SUITE
    defects = parse_spec(specs["py-kake-ledger-guard"])
    res["n_defects"] = len(defects)
    res["old_counts"] = {d["id"]: gate.count(d["old"].encode()) for d in defects}
    table = dict(p.split(":", 1) for p in vars_["TABLE_KAKEGUARD"].split(",") if ":" in p)
    res["table_ids_eq_spec_ids"] = set(table) == {d["id"] for d in defects}

    lw = SCRATCH / "probe-run"
    lw.mkdir(parents=True, exist_ok=True)
    pristine = lw / "pristine.ledger_append_guard.py"
    pristine.write_bytes(gate)
    pristine.chmod(0o755)
    runs = {"CONTROL": {"rc": run_suite(PY_SUITE, pristine, pristine, lw, "CONTROL"),
                        "expected": "SURVIVED"}}
    for d in defects:
        old, new = d["old"].encode(), d["new"].encode()
        assert gate.count(old) == 1, d["id"]
        m = lw / ("mutant-%s.ledger_append_guard.py" % d["id"])
        m.write_bytes(gate.replace(old, new, 1))
        m.chmod(pristine.stat().st_mode & 0o777)
        runs[d["id"]] = {"rc": run_suite(PY_SUITE, m, pristine, lw, d["id"]),
                         "expected": table[d["id"]]}
    for did, r in runs.items():
        r["verdict"] = verdict(r["rc"])
        r["match"] = r["verdict"] == r["expected"]
    res["replay"] = runs
    res["replay_all_match"] = all(r["match"] for r in runs.values())

    ok = (res["sha_chain"]["all_equal"] and res["gate"]["pin_match"] and res["gate"]["mode"] == "100755"
          and res["leg11_suite_eq_measure_py_entry"] and all(v == 1 for v in res["old_counts"].values())
          and res["table_ids_eq_spec_ids"] and res["replay_all_match"])
    res["PROBE_PASS"] = ok
    out = json.dumps(res, indent=1)
    print(out)
    if a.out:
        Path(a.out).write_text(out + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
