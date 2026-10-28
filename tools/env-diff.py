#!/usr/bin/env python3
"""Run pinned selftests under the finite F5 environment profiles.

Usage: env-diff.py --contract FILE --out FILE [--fleet-root DIR] [--jobs N]
       env-diff.py --selftest

A classified surface is not a proof of universal hermeticity. The clean
control must pass; a changed repeated clean tuple is nondeterminism, not
attributable environment sensitivity. Raw streams are hashed, never normalized.
Exit 0 all surfaces classified, 1 unavailable surface, 2 setup/input error,
64 usage. Only scratch sandboxes and the requested output file are written.
"""
import argparse
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time

SCHEMA = "tameshi-env-diff-receipt-v1"
PROFILES = ("host", "clean", "clean_repeat", "tz", "locale", "home", "columns")


class ScratchRootUnusable(RuntimeError):
    """A set-but-unusable TMPDIR: could-not-evaluate (exit 2), never a traceback."""


def strict_scratch_root():
    """Scratch root for mkdtemp: TMPDIR when set (must be a usable directory —
    round 53: a set-but-unusable TMPDIR is could-not-evaluate, never a silent
    fallback to /tmp, preserving CR47 semantics), else the platform default.
    An empty TMPDIR is unset (round 54, corpus/knowledge/scratch-root-contract.md)."""
    import os as _os
    t = _os.environ.get("TMPDIR")
    if t:
        if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
            raise ScratchRootUnusable(
                "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
        return t
    return tempfile.gettempdir()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def parent_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def profile_env(name):
    if name == "host":
        return parent_env()
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "HOME": "/tmp/w/home", "TMPDIR": "/tmp/w/tmp",
           "LANG": "C", "LC_ALL": "C", "TZ": "UTC"}
    if name == "tz":
        env["TZ"] = "Pacific/Chatham"
    elif name == "locale":
        env.update(LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8")
    elif name == "home":
        env["HOME"] = "/nonexistent"
    elif name == "columns":
        env.update(COLUMNS="20", LINES="5", TERM="dumb")
    return env


def execute(payload, interp, profile, timeout=600, bwrap=None):
    bwrap = bwrap or shutil.which("bwrap")
    if not bwrap:
        return {"exit": None, "error": "BWRAP_UNAVAILABLE"}
    with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir=strict_scratch_root()) as tmp:
        root = Path(tmp)
        (root / "home").mkdir()
        (root / "tmp").mkdir()
        target = root / ("target.mjs" if interp == "node" else "target.sh")
        target.write_bytes(payload)
        target.chmod(0o755)
        argv = [bwrap, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
                "--tmpfs", "/tmp", "--bind", tmp, "/tmp/w", "--unshare-net",
                "--die-with-parent", "--chdir", "/tmp/w",
                interp, "/tmp/w/" + target.name, "--selftest"]
        start = time.monotonic()
        try:
            proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    env=profile_env(profile), start_new_session=True)
        except OSError as exc:
            return {"exit": None, "error": "EXEC_UNAVAILABLE", "detail": str(exc)}
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = proc.communicate()
            return {"exit": None, "error": "TIMEOUT", "seconds": round(time.monotonic() - start, 3),
                    "stdout_sha256": digest(stdout), "stderr_sha256": digest(stderr)}
        return {"exit": proc.returncode, "stdout_sha256": digest(stdout),
                "stderr_sha256": digest(stderr), "seconds": round(time.monotonic() - start, 3),
                "stdout_tail": stdout[-1600:].decode("utf-8", "replace"),
                "stderr_tail": stderr[-1600:].decode("utf-8", "replace")}


def tuple_of(row):
    return row.get("exit"), row.get("stdout_sha256"), row.get("stderr_sha256")


def classify(profiles):
    if any(not isinstance(profiles[p].get("exit"), int) for p in PROFILES):
        return "unavailable", []
    if profiles["clean"]["exit"] != 0:
        return "unavailable", []
    clean = tuple_of(profiles["clean"])
    if tuple_of(profiles["clean_repeat"]) != clean:
        return "nondeterministic", []
    changed = sorted(p for p in PROFILES if tuple_of(profiles[p]) != clean)
    return ("env-sensitive", changed) if changed else ("invariant", [])


def probe(payload, interp):
    profiles = {name: execute(payload, interp, name) for name in PROFILES}
    classification, sensitive = classify(profiles)
    return {"normalization": "none", "profiles": profiles,
            "classification": classification, "sensitive_to": sensitive}


def read_surface(fleet, surface):
    repo = fleet / surface["repo"]
    proc = subprocess.run(["git", "-C", str(repo), "show",
                           surface["rev"] + ":" + surface["path"]],
                          env=parent_env(), capture_output=True, timeout=30)
    if proc.returncode:
        raise ValueError("PIN_UNREADABLE: " + surface["name"])
    actual = digest(proc.stdout)
    if surface.get("blob_sha256", actual) != actual:
        raise ValueError("PIN_MISMATCH: " + surface["name"])
    return proc.stdout, actual


def surface_result(fleet, surface):
    row = {"surface": surface["name"], "pin": {k: surface[k] for k in ("repo", "rev", "path")},
           "argv": [surface["interp"], "/tmp/w/target." +
                    ("mjs" if surface["interp"] == "node" else "sh"), "--selftest"]}
    try:
        payload, actual = read_surface(fleet, surface)
        row["pin"]["blob_sha256"] = actual
        row.update(probe(payload, surface["interp"]))
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        row.update(classification="unavailable", sensitive_to=[], error=str(exc))
    return row


def selftest():
    checks = []
    def check(name, ok):
        checks.append((name, bool(ok)))
        print("ENVDIFF_CASE", name, "PASS" if ok else "FAIL")
    for name, script, expected in (
        ("invariant", "printf 'stable\\n'", "invariant"),
        ("tz", "printf '%s\\n' \"${TZ-unset}\"", "env-sensitive"),
        ("locale", "printf '%s\\n' \"${LC_ALL-unset}\"", "env-sensitive"),
        ("home", "printf '%s\\n' \"${HOME-unset}\"", "env-sensitive"),
        ("columns", "printf '%s\\n' \"${COLUMNS-unset}\"", "env-sensitive"),
        ("repeat", "printf '%s\\n' \"$BASHPID\"", "nondeterministic"),
    ):
        row = probe(("#!/bin/bash\n" + script + "\n").encode(), "bash")
        ok = row["classification"] == expected
        if name in ("tz", "locale", "home", "columns"):
            ok = ok and name in row["sensitive_to"]
        check(name, ok)
    missing = execute(b"exit 0\n", "bash", "clean", bwrap="/nonexistent/tameshi-bwrap")
    check("missing-bwrap", missing.get("error") == "EXEC_UNAVAILABLE")
    timed = execute(b"sleep 5\n", "bash", "clean", timeout=0.02)
    check("timeout", timed.get("error") == "TIMEOUT" and timed["exit"] is None)
    # Public CLI refusal: a local fixture repository pins wrong bytes. No
    # external surface is written and no fixture target is executed.
    with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff-pin.") as tmp:
        root = Path(tmp)
        repo = root / "fixture"
        repo.mkdir()
        (repo / "target.sh").write_text("exit 0\n")
        git_env = parent_env()
        git_env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        def git(*args):
            return subprocess.run(["git", "-C", str(repo), *args], check=True,
                                  env=git_env, capture_output=True).stdout
        git("init", "-q")
        git("add", "target.sh")
        git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "fixture")
        rev = git("rev-parse", "HEAD").decode().strip()
        contract = {"surfaces": [{"name": "wrong-pin", "repo": "fixture", "rev": rev,
                     "path": "target.sh", "interp": "bash", "blob_sha256": "0" * 64}]}
        cp, op = root / "contract.json", root / "receipt.json"
        cp.write_text(json.dumps(contract))
        child = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                "--contract", str(cp), "--out", str(op), "--fleet-root", tmp],
                               capture_output=True, timeout=30, env=parent_env())
        receipt = json.loads(op.read_text()) if op.exists() else {}
        records = receipt.get("surfaces", [])
        check("pin-mismatch-public-cli", child.returncode == 1 and len(records) == 1
              and "PIN_MISMATCH" in records[0].get("error", "")
              and records[0].get("classification") == "unavailable")
    passed = sum(ok for _, ok in checks)
    print(f"ENVDIFF_SELFTEST: {passed}/{len(checks)} pass")
    return 0 if passed == len(checks) else 1


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(64, "ENVDIFF_USAGE: " + message + "\n")


def main(argv=None):
    p = Parser(description=__doc__)
    p.add_argument("--contract", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--fleet-root", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--jobs", type=int, default=3)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)
    if a.selftest:
        try:
            return selftest()
        except ScratchRootUnusable as exc:
            print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
            return 2
    if not a.contract or not a.out or not 1 <= a.jobs <= 3:
        p.error("--contract and --out are required; --jobs must be 1..3")
    try:
        raw = a.contract.read_bytes()
        contract = json.loads(raw)
        surfaces = contract["surfaces"]
        if not isinstance(surfaces, list) or not surfaces:
            raise ValueError("surfaces must be a nonempty list")
        started_at = datetime.now(timezone.utc).isoformat()
        with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
            rows = list(pool.map(lambda s: surface_result(a.fleet_root, s), surfaces))
        report = {"schema": SCHEMA, "contract_sha256": digest(raw),
                  "host": {"uname": platform.platform(), "python": platform.python_version()},
                  "profiles": {name: ("inherited minus GIT_*" if name == "host" else profile_env(name))
                               for name in PROFILES}, "surfaces": rows}
        report["instrument_sha256"] = digest(Path(__file__).read_bytes())
        report["measurement_interval"] = {
            "start": started_at, "end": datetime.now(timezone.utc).isoformat()
        }
        report["argv"] = [sys.executable, *sys.argv]
        for command in ("node", "bash"):
            version = subprocess.run([command, "--version"], capture_output=True,
                                     env=parent_env(), timeout=10)
            report["host"][command] = version.stdout.decode("utf-8", "replace").splitlines()[0]
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    except ScratchRootUnusable as exc:
        print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("ENVDIFF_SETUP:", exc, file=sys.stderr)
        return 2
    done = sum(r.get("classification") != "unavailable" for r in rows)
    print(f"ENVDIFF: classified={done}/{len(rows)} out={a.out}")
    return 0 if done == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
