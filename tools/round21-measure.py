#!/usr/bin/env python3
"""Maintained public CLI/selftest facade for the frozen round-21 counters.

--claim c1|c2 --repo DIR --rev REV --json delegates the unchanged frozen
counter. --selftest runs literal public-CLI fixture expectations for both
counter packages. It validates bounded measurement logic, not producer
execution authenticity. Exits: 0 clean, 1 failed, 2 could-not-evaluate,
64 usage. All Git writes stay in private fixture repositories. The c2
fixture reads the pinned sibling blobs at the fleet root that the subject
counter itself reads (its `FLEET` literal), so the selftest is fleet-bound,
not hermetic: it passes from a clone anywhere on this host and fails where
that fleet root is absent (round 52, routed defect R51.4).
"""
import argparse
import copy
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / ".ufo/evidence/round-21"
SCRIPTS = {"c1": "c1-survivors.py", "c2": "c2-count.py"}


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               PYTHONDONTWRITEBYTECODE="1")
    return env


def selftest():
    checks = []
    def check(name, ok):
        checks.append(bool(ok))
        print("MEASURE_CASE", name, "PASS" if ok else "FAIL")
    with tempfile.TemporaryDirectory(prefix="tameshi-r21-measure-selftest.") as tmp:
        work = Path(tmp)
        repo, package = work / "repo", work / "package"
        repo.mkdir(); package.mkdir()
        env = clean_env()
        env["HOME"] = str(work)
        def git(*args):
            return subprocess.run(["git", "-C", str(repo), *args], env=env,
                                  capture_output=True, check=True).stdout.decode().strip()
        def put(path, text):
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        def commit():
            git("add", "--all")
            git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                "commit", "-qm", "fixture")
            return git("rev-parse", "HEAD")
        git("init", "-q", "-b", "master")
        for filename in SCRIPTS.values():
            (package / filename).write_bytes((EVIDENCE / filename).read_bytes())
        c1_spec = {"mutants": [{"id": "fixture", "path": "tools/fixture.py",
                               "old": 'VALUE = "good"', "new": 'VALUE = "bad"'}],
                   "selftest_argv": {"tools/fixture.py": ["--selftest"]}}
        def c1spec(spec):
            (package / "c1-mutants.json").write_text(json.dumps(spec))
        put("tools/fixture.py", 'VALUE = "good"\nLABEL = "one"\nraise SystemExit(0 if VALUE == "good" else 1)\n')
        put("tools/env-diff.py", 'print("fixture selftest passed")\n')
        put("corpus/knowledge/hermetic-env-differential.md", "source: S079\nfixture\n")
        put("corpus/SOURCES.md", "| S079 | fixture | docs | A | fixture | fixture | fixture | mined | 2026-10-21 | 365d | corpus/knowledge/hermetic-env-differential.md |\n")
        frozen = json.loads((EVIDENCE / "c2-contract.json").read_text())
        (package / "c2-contract.json").write_text(json.dumps(frozen))
        zero = hashlib.sha256(b"fixture").hexdigest()
        surfaces = []
        fleet = Path(re.search(r'^FLEET = Path\("([^"]+)"\)$',
                               (EVIDENCE / SCRIPTS["c2"]).read_text(), re.M).group(1))
        for surface in frozen["surfaces"]:
            pin = {key: surface[key] for key in ("repo", "rev", "path")}
            data = subprocess.run(["git", "-C", str(fleet / surface["repo"]),
                                   "show", surface["rev"] + ":" + surface["path"]],
                                  env=env, capture_output=True, check=True).stdout
            pin["blob_sha256"] = hashlib.sha256(data).hexdigest()
            surfaces.append({"surface": surface["name"], "pin": pin,
                             "normalization": "none", "classification": "invariant",
                             "sensitive_to": [], "profiles": {
                                 name: {"exit": 0, "stdout_sha256": zero, "stderr_sha256": zero}
                                 for name in frozen["required_profiles"]}})
        receipt = {"schema": frozen["receipt_schema"], "surfaces": surfaces}
        def c2receipt(obj):
            put(frozen["receipt_path"], json.dumps(obj))
        def invoke(claim, rev, extra=()):
            return subprocess.run([sys.executable, str(package / SCRIPTS[claim]),
                                   "--repo", str(repo), "--rev", rev, "--json", *extra],
                                  env=env, capture_output=True, timeout=120)
        c1spec(c1_spec)
        c2receipt(receipt)
        rev = commit()
        p = invoke("c1", rev)
        check("c1-killed", p.returncode == 0 and json.loads(p.stdout)["killed"] == 1)
        alternative = copy.deepcopy(c1_spec)
        alternative["mutants"][0].update(old='LABEL = "one"', new='LABEL = "two"')
        c1spec(alternative)
        p = invoke("c1", rev)
        check("c1-survived", p.returncode == 1 and json.loads(p.stdout)["survived"] == 1)
        alternative["mutants"][0]["old"] = "missing anchor"
        c1spec(alternative)
        p = invoke("c1", rev)
        check("c1-missing-anchor", p.returncode == 1 and json.loads(p.stdout)["inconclusive"] == 1)
        c1spec(c1_spec)
        put("tools/fixture.py", 'VALUE = "good"\nraise SystemExit(1)\n')
        red_rev = commit()
        p = invoke("c1", red_rev)
        check("c1-pristine-red", p.returncode == 1 and json.loads(p.stdout)["inconclusive"] == 1)
        p = invoke("c2", rev)
        check("c2-complete", p.returncode == 0 and json.loads(p.stdout)["classified"] == 9)
        bad = copy.deepcopy(receipt)
        bad["surfaces"][0]["pin"]["rev"] = "0" * 40
        c2receipt(bad); p = invoke("c2", commit())
        check("c2-wrong-pin", p.returncode == 1 and json.loads(p.stdout)["classified"] == 8)
        bad = copy.deepcopy(receipt)
        del bad["surfaces"][0]["profiles"]["tz"]
        c2receipt(bad); p = invoke("c2", commit())
        check("c2-missing-profile", p.returncode == 1 and json.loads(p.stdout)["classified"] == 8)
        bad = copy.deepcopy(receipt)
        bad["surfaces"][0]["classification"] = "env-sensitive"
        c2receipt(bad); p = invoke("c2", commit())
        check("c2-wrong-classification", p.returncode == 1 and json.loads(p.stdout)["classified"] == 8)
        c2receipt(receipt)
        put("corpus/SOURCES.md", (repo / "corpus/SOURCES.md").read_text().replace("| mined |", "| queued |"))
        p = invoke("c2", commit())
        check("c2-unmined-source", p.returncode == 1 and not json.loads(p.stdout)["f5_entry"])
        for claim in ("c1", "c2"):
            p = invoke(claim, "0" * 40)
            check(claim + "-unknown-rev", p.returncode == 2)
            p = invoke(claim, rev, ("--unsupported",))
            check(claim + "-usage", p.returncode == 64)
    passed = sum(checks)
    print(f"ROUND21_MEASURE_SELFTEST: {passed}/{len(checks)} pass")
    return 0 if passed == len(checks) else 1


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(64, "MEASURE_USAGE: " + message + "\n")


def main():
    p = Parser(description=__doc__)
    p.add_argument("--claim", choices=tuple(SCRIPTS))
    p.add_argument("--repo")
    p.add_argument("--rev")
    p.add_argument("--json", action="store_true")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.selftest:
        return selftest()
    if not args.claim or not args.repo or not args.rev:
        p.error("--claim, --repo and --rev are required")
    argv = [sys.executable, str(EVIDENCE / SCRIPTS[args.claim]),
            "--repo", args.repo, "--rev", args.rev]
    if args.json:
        argv.append("--json")
    return subprocess.run(argv, env=clean_env()).returncode


if __name__ == "__main__":
    sys.exit(main())
