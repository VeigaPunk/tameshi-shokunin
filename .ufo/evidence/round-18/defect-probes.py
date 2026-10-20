#!/usr/bin/env python3
"""Measure the eleven round-17 survivor defects at one lane revision.

Every child runs under bwrap 0.13.1 with this envelope:
  bwrap --ro-bind / / --dev /dev --proc /proc --bind W W
    --bind W /mnt --ro-bind FLEET /mnt/source --tmpfs /tmp --bind W/tmp /tmp
    --unshare-pid --unshare-net --die-with-parent --chdir /mnt/<cwd>
    env -i PATH=/usr/bin:/bin HOME=/mnt/home XDG_CONFIG_HOME=/mnt/xdg
    XDG_CACHE_HOME=/mnt/home/.cache TMPDIR=/tmp
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 JJ_CONFIG=
    GIT_TERMINAL_PROMPT=0 LC_ALL=C PYTHONDONTWRITEBYTECODE=1
`/tmp` is an alias of W/tmp, so tool selftest temp files stay under W. P10's
checker and escaped descendants share the PID namespace; the supervisor checks
the unique marker immediately after checker exit and kills any survivor.

Usage:
    python3 .ufo/evidence/round-18/defect-probes.py --rev REV [--json]
        [--only P01..P11]
    python3 .ufo/evidence/round-18/defect-probes.py --selftest

Exits: 0 measured (any open/closed mix); 2 could-not-evaluate; 64 usage.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

sys.dont_write_bytecode = True

SCHEMA = "tameshi-defect-probes-v1"
PROBE_IDS = tuple("P%02d" % n for n in range(1, 12))
LANE_ROOT = Path(__file__).resolve().parents[3]
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
SANDBOX_ROOT = None
SANDBOX_FLEET_ROOT = None
JJ_COMMAND = shutil.which("jj")

# Literal implementation guards, not selftest snippets. Each OLD byte string
# was counted in the pinned landing before the mutation is applied.
GUARD_SPECS = {
    "P01": {
        "path": "tools/evidence-disposition.py",
        "line": 445,
        "old": b"if proc.returncode != 0 or resolved != rev:",
        "new": b"if False:",
        "description": "G3 exact commit-object identity guard",
    },
    "P02": {
        "path": "tools/evidence-disposition.py",
        "line": 552,
        "old": b"if kind != \"blob\" or mode not in TREE_MODES:",
        "new": b"if kind != \"blob\":",
        "description": "G5 regular-blob mode guard",
    },
    "P03": {
        "path": "tools/registry-check.py",
        "line": 466,
        "old": b'["git", "-C", clone_root, "checkout", "-q", "--detach", sha]',
        "new": b'["git", "-C", clone_root, "reset", "-q", "--hard", sha]',
        "description": "detached-checkout operation",
    },
    "P04": {
        "path": "tools/registry-check.py",
        "line": 96,
        "old": b"^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$",
        "new": b"^[^@]+@[0-9a-f]{1,40}:[0-9]+(-[0-9]+)?$",
        "description": "source-revision minimum-length regex",
    },
    "P05": {
        "path": None,
        "line": 82,
        "old": b"WRITE_FLAGS_RE = re.compile(r\"\\bO_(?:WRONLY|RDWR|CREAT|TRUNC|APPEND|TMPFILE)\\b\")",
        "new": b"WRITE_FLAGS_RE = re.compile(r\"\\bO_(?:WRONLY|CREAT|TRUNC|APPEND|TMPFILE)\\b\")",
        "description": "O_RDWR write-mode exclusion",
    },
    "P06": {
        "path": None,
        "line": 516,
        "old": b'env["PYTHONPYCACHEPREFIX"] = cache',
        "new": b'env["PYTHONPYCACHEPREFIX"] = "."',
        "description": "private PYTHONPYCACHEPREFIX setting",
    },
    "P07": {
        "path": None,
        "line": 644,
        "old": b"if tracer.first_pid is None or tracer.first_pid not in tracer.exec_ok:",
        "new": b"if tracer.first_pid is None:",
        "description": "successful root execve requirement",
    },
}


class ProbeError(Exception):
    """The requested probe could not be evaluated reliably."""


class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(64, "%s: error: %s\n" % (self.prog, message))

def assert_under_work(path, label):
    if SANDBOX_ROOT is None:
        raise ProbeError("sandbox root is not initialized")
    base = os.path.realpath(SANDBOX_ROOT)
    target = os.path.realpath(path)
    try:
        common = os.path.commonpath((base, target))
    except ValueError:
        common = ""
    if common != base:
        raise ProbeError("%s is outside private W: %s" % (label, path))
    return Path(target)


def mapped_path(value):
    if SANDBOX_ROOT is None:
        raise ProbeError("sandbox root is not initialized")
    root = os.path.abspath(str(SANDBOX_ROOT))
    value = os.fspath(value)
    if not os.path.isabs(value):
        return value
    absolute = os.path.abspath(value)
    if absolute == root:
        return "/mnt"
    if absolute.startswith(root + os.sep):
        return "/mnt" + absolute[len(root):]
    if SANDBOX_FLEET_ROOT is not None:
        fleet = os.path.abspath(str(SANDBOX_FLEET_ROOT))
        if absolute == fleet:
            return "/mnt/source"
        if absolute.startswith(fleet + os.sep):
            return "/mnt/source" + absolute[len(fleet):]
    return value


def child_environment(extra=None):
    if SANDBOX_ROOT is None:
        raise ProbeError("sandbox root is not initialized")
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": "/mnt/home",
        "XDG_CONFIG_HOME": "/mnt/xdg",
        "XDG_CACHE_HOME": "/mnt/home/.cache",
        "TMPDIR": "/tmp",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "JJ_CONFIG": "",
        "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    if extra:
        for key, value in extra.items():
            if key.startswith("GIT_") and key not in (
                    "GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM",
                    "GIT_TERMINAL_PROMPT", "GIT_DIR", "GIT_WORK_TREE"):
                raise ProbeError("unapproved GIT_* child environment variable: " + key)
            env[key] = os.fspath(value)
    return env


def scrubbed_env(extra=None):
    """Construct an env -i child environment; inherited process state is ignored."""
    return child_environment(extra)


def sandbox_argv(argv, cwd, env):
    work = assert_under_work(SANDBOX_ROOT, "sandbox W")
    cwd_host = assert_under_work(cwd, "child cwd")
    mapped_cwd = mapped_path(str(cwd_host))
    mapped_env = {key: mapped_path(value) for key, value in env.items()}
    mapped_command = [mapped_path(os.fspath(arg)) for arg in argv]
    env_assignments = ["%s=%s" % (key, value)
                       for key, value in sorted(mapped_env.items())]
    wrapped = [
        "bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
        "--unshare-pid", "--unshare-net", "--die-with-parent",
        "--bind", str(work), str(work),
        "--bind", str(work), "/mnt",
    ]
    if SANDBOX_FLEET_ROOT is not None:
        fleet = Path(SANDBOX_FLEET_ROOT)
        if os.path.commonpath((str(work), str(fleet))) != str(work):
            wrapped.extend(["--ro-bind", str(fleet), "/mnt/source"])
    wrapped.extend([
        "--tmpfs", "/tmp", "--bind", str(work / "tmp"), "/tmp",
        "--chdir", mapped_cwd,
        "env", "-i", *env_assignments, *mapped_command,
    ])
    return wrapped


def initialize_sandbox(work, fleet_root=None):
    global SANDBOX_ROOT, SANDBOX_FLEET_ROOT
    SANDBOX_ROOT = Path(work).resolve()
    SANDBOX_FLEET_ROOT = Path(fleet_root).resolve() if fleet_root else None
    for name in ("home", "home/.cache", "xdg", "tmp", "source"):
        path = SANDBOX_ROOT / name
        assert_under_work(path, "sandbox directory")
        path.mkdir(parents=True, exist_ok=True)


def run_bytes(argv, cwd, env=None, timeout=60):
    """Run a bounded command inside the read-only bwrap envelope."""
    child_env = scrubbed_env() if env is None else dict(env)
    wrapped = sandbox_argv(argv, cwd, child_env)
    try:
        proc = subprocess.run(
            wrapped, cwd=str(SANDBOX_ROOT),
            env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        if isinstance(stdout, str):
            stdout = stdout.encode("utf-8", "replace")
        if isinstance(stderr, str):
            stderr = stderr.encode("utf-8", "replace")
        return subprocess.CompletedProcess(wrapped, None, stdout, stderr), True
    except OSError as exc:
        raise ProbeError("cannot launch bwrap child for %r: %s" %
                         (list(argv), exc)) from exc
    return proc, False


def text(raw):
    return (raw or b"").decode("utf-8", "replace")


def excerpt(proc, limit=220):
    lines = [line.strip() for line in (text(proc.stdout) + "\n" + text(proc.stderr)).splitlines()
             if line.strip()]
    if not lines:
        return "no output"
    last = lines[-1]
    return last if len(last) <= limit else last[:limit] + "..."


def replace_once(raw, old, new, label):
    count = raw.count(old)
    if count != 1:
        raise ProbeError("%s anchor count=%d, expected exactly 1" % (label, count))
    return raw.replace(old, new, 1)


def git_call(args, cwd, timeout=30):
    proc, timed_out = run_bytes(["git"] + list(args), cwd, timeout=timeout)
    if timed_out:
        raise ProbeError("git command timed out: %r" % (list(args),))
    if proc.returncode != 0:
        raise ProbeError("git command failed (%d): %s" %
                         (proc.returncode, text(proc.stderr).strip()))
    return proc.stdout


def resolve_revision(root, rev, work):
    out = git_call(["-C", str(root), "rev-parse", "--verify", "--quiet",
                    "--end-of-options", rev + "^{commit}"], work)
    sha = text(out).strip()
    if not HEX40_RE.fullmatch(sha):
        raise ProbeError("revision did not resolve to a full commit id: %r" % sha)
    return sha


def clone_lane_at(root, rev_sha, work):
    """Build the required fleet-mirror clone; only the clone is checked out."""
    root = Path(root).resolve()
    fleet_source = root.parent
    fleet = work / "fleet"
    source_links = work / "source"
    assert_under_work(fleet, "fleet-mirror directory")
    assert_under_work(source_links, "fleet source-link directory")
    fleet.mkdir()
    source_links.mkdir(exist_ok=True)
    try:
        siblings = sorted(fleet_source.iterdir(), key=lambda path: path.name)
    except OSError:
        siblings = []
    for sibling in siblings:
        if (sibling.name.endswith("-shokunin")
                and os.path.realpath(sibling) != str(root)):
            source_link = source_links / sibling.name
            if not source_link.exists() and not source_link.is_symlink():
                assert_under_work(source_link, "read-only sibling source link")
                source_link.symlink_to(sibling)
            link = fleet / sibling.name
            if not link.exists() and not link.is_symlink():
                assert_under_work(link, "fleet-mirror sibling link")
                link.symlink_to(Path("..") / "source" / sibling.name)
    clone_root = fleet / root.name
    assert_under_work(clone_root, "lane clone")
    proc, timed_out = run_bytes(
        ["git", "-c", "core.hooksPath=/dev/null", "clone", "-q",
         "--no-hardlinks", str(root), str(clone_root)],
        work, timeout=120,
    )
    if timed_out or proc.returncode != 0:
        raise ProbeError("git clone failed: %s" % excerpt(proc))
    proc, timed_out = run_bytes(
        ["git", "-c", "core.hooksPath=/dev/null", "-C", str(clone_root),
         "checkout", "-q", "--detach", rev_sha],
        clone_root, timeout=60,
    )
    if timed_out or proc.returncode != 0:
        raise ProbeError("detached checkout failed: %s" % excerpt(proc))
    observed = text(git_call(["-C", str(clone_root), "rev-parse", "HEAD"], clone_root)).strip()
    if observed != rev_sha:
        raise ProbeError("clone HEAD %s does not equal resolved revision %s" %
                         (observed, rev_sha))
    probe_copy = clone_root / ".ufo" / "evidence" / "round-18" / "defect-probes.py"
    assert_under_work(probe_copy, "clone-local probe copy")
    probe_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).resolve(), probe_copy)
    return clone_root


def trace_tool(root):
    promoted = root / "tools" / "trace-inputs.py"
    if promoted.is_file():
        return promoted
    historical = root / ".ufo" / "evidence" / "round-17" / "coldread" / "trace-inputs.py"
    if historical.is_file():
        return historical
    raise ProbeError("trace collector not found at either supported lane path")


def run_selftest(tool, root, timeout=240):
    proc, timed_out = run_bytes([sys.executable, str(tool), "--selftest"],
                                root, timeout=timeout)
    if timed_out:
        raise ProbeError("%s --selftest timed out after %ss" % (tool, timeout))
    if proc.returncode not in (0, 1):
        raise ProbeError("%s --selftest could not be evaluated (exit=%s): %s" %
                         (tool, proc.returncode, excerpt(proc)))
    return proc


def guard_probe(probe_id, root):
    spec = dict(GUARD_SPECS[probe_id])
    if spec["path"] is None:
        tool = trace_tool(root)
        rel = tool.relative_to(root).as_posix()
        target = "%s:%d" % (rel, spec["line"])
        candidates = (
            root / "tools" / "trace-inputs.py",
            root / ".ufo" / "evidence" / "round-17" / "coldread" / "trace-inputs.py",
        )
        checked = []
        for candidate in candidates:
            if candidate.is_file():
                count = candidate.read_bytes().count(spec["old"])
                if count != 1:
                    raise ProbeError("%s anchor count=%d, expected exactly 1" %
                                     (candidate.relative_to(root).as_posix(), count))
                checked.append(candidate.relative_to(root).as_posix())
    else:
        tool = root / spec["path"]
        target = "%s:%d" % (spec["path"], spec["line"])
        checked = [spec["path"]]
    if not tool.is_file():
        raise ProbeError("target tool is missing: %s" % tool)
    assert_under_work(tool, "guard target")
    pristine = tool.read_bytes()
    mutant = replace_once(pristine, spec["old"], spec["new"], target)
    pristine_proc = run_selftest(tool, root)
    if pristine_proc.returncode != 0:
        raise ProbeError("%s pristine selftest failed (exit=%d): %s" %
                         (target, pristine_proc.returncode, excerpt(pristine_proc)))
    try:
        tool.write_bytes(mutant)
        mutant_proc = run_selftest(tool, root)
    finally:
        tool.write_bytes(pristine)
    status = "open" if mutant_proc.returncode == 0 else "closed"
    detail = ("%s pristine_exit=%d mutant_exit=%d; anchors=%s; mutant=%r -> %r; %s" %
              (spec["description"], pristine_proc.returncode, mutant_proc.returncode,
               ",".join(checked), spec["old"].decode("utf-8"),
               spec["new"].decode("utf-8"), excerpt(mutant_proc)))
    return {"id": probe_id, "status": status, "target": target,
            "detail": detail, "pristine_exit": pristine_proc.returncode,
            "mutant_exit": mutant_proc.returncode, "old": spec["old"].decode("utf-8"),
            "new": spec["new"].decode("utf-8"), "checked_paths": checked}


def import_disposition_fixture_tool(path):
    name = "_tameshi_r18_disposition_fixture_%s" % uuid.uuid4().hex
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ProbeError("cannot load evidence-disposition fixture helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    needed = ("_build_lane", "_rows", "_dispositions_v2", "_write_bytes",
              "SELFTEST_TOOL_V2", "SELFTEST_V1_REL")
    missing = [key for key in needed if not hasattr(module, key)]
    if missing:
        raise ProbeError("disposition fixture helpers unavailable: " + ", ".join(missing))
    return module


def jj_call(args, cwd, env, timeout=45):
    if JJ_COMMAND is None:
        raise ProbeError("jj is not on the caller's PATH")
    proc, timed_out = run_bytes([JJ_COMMAND] + list(args), cwd, env=env, timeout=timeout)
    if timed_out or proc.returncode != 0:
        raise ProbeError("jj %s failed%s: %s" %
                         (" ".join(args), " (timeout)" if timed_out else "",
                          excerpt(proc)))
    return text(proc.stdout).strip(), text(proc.stderr).strip()


def fixture_commit_id(jj_env, lane):
    value, _ = jj_call(["log", "-r", "@-", "--no-graph", "-T", "commit_id"],
                       lane, jj_env)
    if not HEX40_RE.fullmatch(value):
        raise ProbeError("jj @- is not a full commit id: %r" % value)
    return value


def git_value(lane, *args):
    return text(git_call(["-C", str(lane)] + list(args), lane)).strip()


def run_disposition(tool, lane, manifest):
    proc, timed_out = run_bytes(
        [sys.executable, str(tool), "--root", str(lane),
         "--dispositions", str(manifest), "--json"],
        lane, timeout=60,
    )
    if timed_out:
        raise ProbeError("evidence-disposition timed out in jj fixture")
    try:
        payload = json.loads(text(proc.stdout))
    except ValueError as exc:
        raise ProbeError("evidence-disposition emitted non-JSON output: %s" % excerpt(proc)) from exc
    ids = sorted(item.get("id") for item in payload.get("findings", []))
    return proc.returncode, payload, ids


def probe_jj_head_vs_bookmark(root, scratch):
    """Exercise G2 then G3 with jj's @- held while master moves independently."""
    disposition_tool = root / "tools" / "evidence-disposition.py"
    if not disposition_tool.is_file():
        raise ProbeError("evidence-disposition.py is missing from the clone")
    fixture = scratch / "p08-jj-colocated"
    marker = scratch / "p08-marker"
    assert_under_work(fixture, "P08 jj fixture")
    assert_under_work(marker, "P08 receipt marker")
    module = import_disposition_fixture_tool(disposition_tool)
    try:
        fx = module._build_lane(fixture, marker, {})
    except Exception as exc:
        raise ProbeError("cannot build disposition fixture: %s: %s" %
                         (type(exc).__name__, exc)) from exc

    jj_home = scratch / "p08-home"
    jj_xdg = scratch / "p08-xdg"
    assert_under_work(jj_home, "P08 jj HOME")
    assert_under_work(jj_xdg, "P08 jj XDG_CONFIG_HOME")
    jj_home.mkdir()
    jj_xdg.mkdir()
    jj_env = scrubbed_env({"HOME": str(jj_home), "XDG_CONFIG_HOME": str(jj_xdg)})
    jj_call(["git", "init", "--colocate"], fixture, jj_env)
    git_call(["-C", str(fixture), "config", "core.hooksPath", "/dev/null"], fixture)
    jj_call(["config", "set", "--repo", "user.name", "Tameshi probe"], fixture, jj_env)
    jj_call(["config", "set", "--repo", "user.email", "probe@invalid"], fixture, jj_env)
    jj_call(["commit", "-m", "pinned A"], fixture, jj_env)
    rev_a = fixture_commit_id(jj_env, fixture)
    pinned = git_call(["-C", str(fixture), "show", rev_a + ":tools/pinned-tool.py"], fixture)
    if pinned != module.SELFTEST_TOOL_V1:
        raise ProbeError("jj A does not contain the expected pinned tool bytes")
    jj_call(["bookmark", "set", "master", "--revision", rev_a], fixture, jj_env)

    tool_path = fixture / fx["tool_rel"]
    assert_under_work(tool_path, "P08 committed tool")
    module._write_bytes(tool_path, module.SELFTEST_TOOL_V2)
    jj_call(["commit", "-m", "HEAD B changes the pinned tool"], fixture, jj_env)
    rev_b = fixture_commit_id(jj_env, fixture)
    if git_call(["-C", str(fixture), "show", rev_b + ":tools/pinned-tool.py"], fixture) != module.SELFTEST_TOOL_V2:
        raise ProbeError("jj B does not contain the changed tool bytes")

    # A side-branch commit D has the live B bytes, but is not descended from A.
    # Moving master to A first distinguishes G2; moving it to D then isolates G3.
    jj_call(["new", "root()"], fixture, jj_env)
    module._write_bytes(tool_path, module.SELFTEST_TOOL_V2)
    jj_call(["commit", "-m", "side D has B tool bytes"], fixture, jj_env)
    rev_d = fixture_commit_id(jj_env, fixture)
    jj_call(["new", rev_b], fixture, jj_env)
    if fixture_commit_id(jj_env, fixture) != rev_b:
        raise ProbeError("jj @- moved away from B while restoring the working copy")

    manifest_path = fixture / ".ufo" / "evidence" / "round-13" / "p08-dispositions.json"
    assert_under_work(manifest_path, "P08 dispositions manifest")
    try:
        document = module._dispositions_v2(
            fx, module._rows(fx),
            historical={fx["tool_rel"]: {
                "rev": rev_a,
                "reason": "round-18 synthetic jj-colocated G2/G3 fixture",
            }},
            supersedes_rel=module.SELFTEST_V1_REL,
        )
        module._write_bytes(manifest_path, module._json_bytes(document))
    except Exception as exc:
        raise ProbeError("cannot build v2 disposition manifest: %s: %s" %
                         (type(exc).__name__, exc)) from exc

    def check_pair(bookmark, wanted_id, case_name):
        jj_call(["bookmark", "set", "master", "--revision", bookmark,
                 "--allow-backwards"], fixture, jj_env)
        head = git_value(fixture, "rev-parse", "HEAD")
        branch = git_value(fixture, "rev-parse", "refs/heads/master")
        at_minus = fixture_commit_id(jj_env, fixture)
        if head != rev_b or branch != bookmark or at_minus != rev_b or head == branch:
            raise ProbeError(
                "%s fixture identity mismatch: HEAD=%s master=%s @-=%s" %
                (case_name, head, branch, at_minus)
            )
        rc, payload, ids = run_disposition(disposition_tool, fixture, manifest_path)
        if rc == 0 and payload.get("status") == "clean":
            return {"name": case_name, "status": "open", "head": head,
                    "master": branch, "at_minus": at_minus, "ids": ids}
        if rc == 2 and ids == [wanted_id]:
            return {"name": case_name, "status": "closed", "head": head,
                    "master": branch, "at_minus": at_minus, "ids": ids}
        raise ProbeError(
            "%s produced unexpected verdict exit=%s status=%r findings=%r" %
            (case_name, rc, payload.get("status"), ids)
        )

    g2 = check_pair(rev_a, "historical_input_uncommitted", "G2-live-bytes")
    g3 = check_pair(rev_d, "historical_input_unavailable", "G3-ancestor")
    status = "open" if g2["status"] == "open" or g3["status"] == "open" else "closed"
    details = []
    for case in (g2, g3):
        details.append("%s %s HEAD=%s master=%s @-=%s findings=%s" %
                       (case["name"], case["status"], case["head"],
                        case["master"], case["at_minus"], case["ids"] or "[]"))
    return {"id": "P08", "status": status,
            "target": "tools/evidence-disposition.py: G2 518-539; G3 450-455",
            "detail": ("jj git init --colocate A=%s B=%s D=%s historical_rev=A; " %
                       (rev_a, rev_b, rev_d)) + "; ".join(details)}


def registry_text(timeout_literal, source_rev):
    return (
        '{"schema":"tameshi-entry-registry-v1","rows":[{'
        '"name":"timeout-nonfinite","kind":"probe",'
        '"argv":["/usr/bin/true"],"expect":{"exit":0},'
        '"timeout_s":' + timeout_literal + ',"source":'
        + json.dumps("tools/registry-check.py@%s:1" % source_rev)
        + ',"status":"active"}]}'
    )


def probe_nonfinite_timeouts(root, scratch, rev_sha):
    tool = root / "tools" / "registry-check.py"
    observations = []
    open_case = False
    for literal in ("NaN", "Infinity"):
        registry = scratch / ("p09-%s.json" % literal.lower())
        assert_under_work(registry, "P09 registry fixture")
        registry.write_text(registry_text(literal, rev_sha), encoding="utf-8")
        proc, timed_out = run_bytes(
            [sys.executable, str(tool), "--root", str(root),
             "--registry", str(registry)],
            root, timeout=12,
        )
        out = text(proc.stdout) + "\n" + text(proc.stderr)
        rejected = (not timed_out and proc.returncode == 2 and "timeout_s" in out
                    and "timeout-nonfinite" in out and "Traceback" not in out)
        if not rejected:
            open_case = True
        observations.append("%s:%s exit=%s%s %s" %
                            (literal, "closed" if rejected else "open",
                             "timeout" if timed_out else proc.returncode,
                             " timeout_s_named" if "timeout_s" in out else "",
                             excerpt(proc)))
    return {"id": "P09", "status": "open" if open_case else "closed",
            "target": "tools/registry-check.py:221-227 (timeout_s validation)",
            "detail": "literal JSON values " + "; ".join(observations)}


def proc_state(pid):
    try:
        raw = Path("/proc") .joinpath(str(pid), "stat").read_text(encoding="ascii")
    except (OSError, UnicodeError):
        return None
    close = raw.rfind(")")
    if close < 0:
        return None
    fields = raw[close + 1:].strip().split()
    return fields[0] if fields else None


def marker_pids(marker):
    token = ("TAMESHI_R18_ESCAPE_MARKER=" + marker).encode("ascii")
    found = []
    try:
        entries = os.scandir("/proc")
    except OSError:
        raise ProbeError("/proc is unavailable for descendant observation")
    with entries:
        for entry in entries:
            if not entry.name.isdigit():
                continue
            pid = int(entry.name)
            try:
                env = Path("/proc").joinpath(entry.name, "environ").read_bytes()
            except OSError:
                continue
            if token in env.split(b"\0") and proc_state(pid) not in (None, "Z", "X"):
                found.append(pid)
    return found


def stop_marker_processes(marker, pids=None):
    if pids is None:
        pids = marker_pids(marker)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        except PermissionError:
            pass
    deadline = time.monotonic() + 1.0
    while time.monotonic() < deadline:
        still = [pid for pid in pids if proc_state(pid) not in (None, "Z", "X")]
        if not still:
            return
        time.sleep(0.05)
    for pid in pids:
        if proc_state(pid) not in (None, "Z", "X"):
            try:
                os.kill(pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass


def timeout_row(argv, source_rev, name):
    return {
        "name": "timeout-" + name,
        "kind": "probe",
        "argv": list(argv),
        "expect": {"exit": 0},
        "timeout_s": 1,
        "source": "tools/registry-check.py@%s:1" % source_rev,
        "status": "active",
    }


def timeout_supervisor(tool, root, registry, marker, escape_kind):
    """Observe and clean an escaped row child inside its shared bwrap PID namespace."""
    child_env = {key: value for key, value in os.environ.items()
                 if not key.startswith("GIT_")}
    child_env.update({
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
    })
    child_env["TAMESHI_R18_ESCAPE_MARKER"] = marker
    proc = subprocess.Popen(
        [sys.executable, tool, "--root", root, "--registry", registry],
        cwd=root, env=child_env, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
    )
    timed_out = False
    try:
        try:
            stdout, stderr = proc.communicate(timeout=16)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                stdout, stderr = proc.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                stdout, stderr = proc.communicate()
        survivors = marker_pids(marker)
        combined = text(stdout) + "\n" + text(stderr)
        row_timed_out = ("ROW timeout-%s expect=0 got=timeout differs" %
                         escape_kind) in combined
        if survivors:
            status = "open"
        elif not timed_out and proc.returncode == 1 and row_timed_out:
            status = "closed"
        else:
            raise ProbeError(
                "checker_exit=%r outer_timeout=%s row_timeout=%s output=%s" %
                (proc.returncode, timed_out, row_timed_out,
                 excerpt(subprocess.CompletedProcess(proc.args, proc.returncode,
                                                     stdout, stderr)))
            )
        result = {
            "status": status,
            "checker_exit": proc.returncode,
            "outer_timeout": timed_out,
            "row_timeout": row_timed_out,
            "survivors": survivors,
            "output": excerpt(subprocess.CompletedProcess(
                proc.args, proc.returncode, stdout, stderr)),
        }
        print(json.dumps(result, sort_keys=True))
        return 0
    finally:
        stop_marker_processes(marker)


def run_timeout_fixture(tool, root, scratch, source_rev, escape_kind, argv):
    marker = uuid.uuid4().hex
    registry = scratch / ("p10-%s.json" % escape_kind)
    assert_under_work(registry, "P10 registry fixture")
    registry.write_text(json.dumps({
        "schema": "tameshi-entry-registry-v1",
        "rows": [timeout_row(argv, source_rev, escape_kind)],
    }), encoding="utf-8")
    supervisor = root / ".ufo" / "evidence" / "round-18" / "defect-probes.py"
    assert_under_work(supervisor, "P10 supervisor")
    proc, timed_out = run_bytes(
        [sys.executable, str(supervisor), "--_timeout-supervisor",
         str(tool), str(root), str(registry), marker, escape_kind],
        root, timeout=20,
    )
    if timed_out:
        raise ProbeError("P10 %s supervisor exceeded its 20s bound" % escape_kind)
    try:
        outcome = json.loads(text(proc.stdout))
    except ValueError as exc:
        raise ProbeError("P10 %s supervisor emitted invalid JSON: %s" %
                         (escape_kind, excerpt(proc))) from exc
    if proc.returncode != 0 or "error" in outcome:
        raise ProbeError("P10 %s supervisor failed: %s" %
                         (escape_kind, outcome.get("error", excerpt(proc))))
    detail = ("%s checker_exit=%s outer_timeout=%s row_timeout=%s survivors=%s" %
              (escape_kind,
               "timeout" if outcome["checker_exit"] is None else outcome["checker_exit"],
               outcome["outer_timeout"], outcome["row_timeout"],
               outcome["survivors"]))
    return outcome["status"], detail


def probe_timeout_descendants(root, scratch, rev_sha):
    tool = root / "tools" / "registry-check.py"
    cases = (
        ("setsid", ["/bin/sh", "-c",
                    "setsid sh -c 'exec sleep 40 </dev/null >/dev/null 2>&1' "
                    "</dev/null >/dev/null 2>&1 & sleep 40"]),
        ("setpgid", ["/bin/sh", "-c",
                      "python3 -c 'import os,time; os.setpgid(0,0); time.sleep(40)' "
                      "</dev/null >/dev/null 2>&1 & sleep 40"]),
    )
    results = []
    for kind, argv in cases:
        status, detail = run_timeout_fixture(tool, root, scratch, rev_sha, kind, argv)
        results.append((kind, status, detail))
    overall = "open" if any(item[1] == "open" for item in results) else "closed"
    return {"id": "P10", "status": overall,
            "target": "tools/registry-check.py:306-322, 385-387 (kill/communicate after timeout)",
            "detail": "timeout_s=1; " + "; ".join(item[2] for item in results)}


def file_snapshot(root):
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs
                         if not os.path.islink(os.path.join(base, name)))
        for name in sorted(files):
            path = os.path.join(base, name)
            if os.path.islink(path):
                result[os.path.relpath(path, root)] = "symlink:" + os.readlink(path)
                continue
            try:
                digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
            except OSError as exc:
                result[os.path.relpath(path, root)] = "unreadable:" + str(exc)
            else:
                result[os.path.relpath(path, root)] = digest
    return result


def runner_rev(path):
    raw = path.read_text(encoding="utf-8")
    match = re.search(r"^REV_BASH=([0-9a-f]{40})$", raw, re.M)
    if match is None:
        raise ProbeError("bash-witness-study runner has no exact REV_BASH pin")
    return match.group(1)


def ensure_kagi_clone(root, scratch, witness_tool):
    fleet = root.parent
    source = fleet / "kagi-shokunin"
    if not source.is_dir():
        raise ProbeError("read-only kagi-shokunin source is unavailable for the P11 fixture")
    clone = scratch / "p11-kagi-copy"
    assert_under_work(clone, "P11 kagi clone")
    proc, timed_out = run_bytes(
        ["git", "-c", "core.hooksPath=/dev/null", "clone", "-q",
         "--no-hardlinks", "--no-checkout", str(source), str(clone)],
        scratch, timeout=180,
    )
    if timed_out or proc.returncode != 0:
        raise ProbeError("cannot make the scratch kagi fixture clone: %s" % excerpt(proc))
    rev = runner_rev(witness_tool.parent / "mutate-and-run.sh")
    check, timed_out = run_bytes(
        ["git", "-C", str(clone), "cat-file", "-e", rev + "^{commit}"],
        clone, timeout=30,
    )
    if timed_out:
        raise ProbeError("kagi fixture revision check timed out")
    if check.returncode != 0:
        fetch, timed_out = run_bytes(
            ["git", "-c", "core.hooksPath=/dev/null", "-C", str(clone),
             "fetch", "-q", "--no-tags", str(source), rev],
            clone, timeout=120,
        )
        if timed_out or fetch.returncode != 0:
            raise ProbeError("pinned kagi revision unavailable in scratch clone: %s" % excerpt(fetch))
    return clone, rev


def make_canary(path):
    assert_under_work(path, "P11 canary repo")
    path.mkdir()
    seed = path / "marker.txt"
    assert_under_work(seed, "P11 canary marker")
    seed.write_text("round-18 P11 canary\n", encoding="utf-8")
    proc, timed_out = run_bytes(
        ["git", "-c", "core.hooksPath=/dev/null", "-C", str(path), "init", "-q"], path)
    if timed_out or proc.returncode != 0:
        raise ProbeError("cannot initialize P11 canary repo: %s" % excerpt(proc))
    proc, timed_out = run_bytes(["git", "-C", str(path), "add", "marker.txt"], path)
    if timed_out or proc.returncode != 0:
        raise ProbeError("cannot stage P11 canary: %s" % excerpt(proc))
    proc, timed_out = run_bytes(
        ["git", "-c", "core.hooksPath=/dev/null", "-C", str(path),
         "-c", "user.name=P11 probe", "-c", "user.email=p11@invalid",
         "-c", "commit.gpgsign=false", "commit", "-q", "-m", "canary"], path,
    )
    if timed_out or proc.returncode != 0:
        raise ProbeError("cannot commit P11 canary: %s" % excerpt(proc))


def probe_bash_witness_git_env(root, scratch):
    tool = root / "tools" / "bash-witness-study.py"
    if not tool.is_file():
        raise ProbeError("tools/bash-witness-study.py is missing from the clone")
    kagi_clone, rev = ensure_kagi_clone(root, scratch, tool)
    canary = scratch / "p11-canary"
    make_canary(canary)
    before = file_snapshot(canary)

    clean_evidence = scratch / "p11-clean-evidence"
    assert_under_work(clean_evidence, "P11 clean evidence directory")
    clean_proc, clean_timeout = run_bytes(
        [sys.executable, str(tool), "--evidence", str(clean_evidence),
         "--kagi", str(kagi_clone), "declare"],
        root, env=scrubbed_env(), timeout=90,
    )
    clean_declared = (not clean_timeout and clean_proc.returncode == 0
                      and "WITNESS_DECLARE: wrote" in text(clean_proc.stdout))
    if not clean_declared:
        raise ProbeError("P11 clean fixture did not declare successfully: %s" %
                         excerpt(clean_proc))
    if before != file_snapshot(canary):
        raise ProbeError("P11 clean baseline unexpectedly touched its canary")

    evidence = scratch / "p11-evidence"
    assert_under_work(evidence, "P11 evidence directory")
    extra = {
        "GIT_DIR": str(canary / ".git"),
        "GIT_WORK_TREE": str(canary),
    }
    proc, timed_out = run_bytes(
        [sys.executable, str(tool), "--evidence", str(evidence),
         "--kagi", str(kagi_clone), "declare"],
        root, env=scrubbed_env(extra), timeout=90,
    )
    changed = before != file_snapshot(canary)
    declared = (not timed_out and proc.returncode == 0
                and "WITNESS_DECLARE: wrote" in text(proc.stdout))
    status = "closed" if declared and not changed else "open"
    detail = ("rev=%s clean_exit=%s clean_declared=%s; canary GIT_DIR/GIT_WORK_TREE "
              "tainted_exit=%s timeout=%s canary_changed=%s declared=%s %s" %
              (rev, clean_proc.returncode, clean_declared,
               "timeout" if timed_out else proc.returncode, timed_out,
               changed, declared, excerpt(proc)))
    return {"id": "P11", "status": status,
            "target": "tools/bash-witness-study.py:337-344 (materialize_target git show)",
            "detail": detail}


def run_probe(probe_id, root, scratch, rev_sha):
    if probe_id in GUARD_SPECS:
        return guard_probe(probe_id, root)
    if probe_id == "P08":
        return probe_jj_head_vs_bookmark(root, scratch)
    if probe_id == "P09":
        return probe_nonfinite_timeouts(root, scratch, rev_sha)
    if probe_id == "P10":
        return probe_timeout_descendants(root, scratch, rev_sha)
    if probe_id == "P11":
        return probe_bash_witness_git_env(root, scratch)
    raise ProbeError("unknown probe id %r" % probe_id)


def emit_results(results, rev, as_json):
    counts = {"open": 0, "closed": 0}
    for result in results:
        counts[result["status"]] += 1
    if as_json:
        for result in results:
            print("PROBE %s %s target=%s %s" %
                  (result["id"], result["status"], result["target"], result["detail"]),
                  file=sys.stderr)
        payload = {
            "schema": SCHEMA,
            "rev_resolved": rev,
            "probes": results,
            "open": counts["open"],
            "closed": counts["closed"],
            "total": len(results),
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for result in results:
            print("PROBE %s %s target=%s %s" %
                  (result["id"], result["status"], result["target"], result["detail"]))
        print("DEFECT_PROBES: open=%d closed=%d total=%d" %
              (counts["open"], counts["closed"], len(results)))


def selftest():
    scratch = Path(tempfile.mkdtemp(
        prefix="tameshi-r18w1-X03DefectProbes-", dir="/tmp"))
    initialize_sandbox(scratch)
    checks = []

    def record(name, passed, detail):
        checks.append((name, bool(passed), detail))
        print("SELFTEST_CASE %s %s (%s)" %
              (name, "PASS" if passed else "FAIL", detail))

    try:
        once = replace_once(b"left GUARD right", b"GUARD", b"MUTANT", "fixture")
        record("replace-one-anchor", once == b"left MUTANT right", "one exact replacement")
        missing_rejected = False
        try:
            replace_once(b"nothing here", b"GUARD", b"MUTANT", "missing")
        except ProbeError:
            missing_rejected = True
        duplicate_rejected = False
        try:
            replace_once(b"GUARD GUARD", b"GUARD", b"MUTANT", "duplicate")
        except ProbeError:
            duplicate_rejected = True
        record("reject-nonunique-anchor", missing_rejected and duplicate_rejected,
               "missing and duplicate anchors refused")

        env = scrubbed_env()
        deliberate = scrubbed_env({"GIT_DIR": "/tmp/canary/.git",
                                   "GIT_WORK_TREE": "/tmp/canary"})
        safe_git_keys = {
            key for key in env if key.startswith("GIT_")
        }
        record("scrub-inherited-git",
               safe_git_keys == {"GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM",
                                 "GIT_TERMINAL_PROMPT"}
               and deliberate.get("GIT_DIR") == "/tmp/canary/.git"
               and deliberate.get("GIT_WORK_TREE") == "/tmp/canary",
               "env -i omits inherited repo selectors; explicit canary is retained")
        literal = registry_text("NaN", "0" * 40)
        record("preserve-nonfinite-json-literal", '"timeout_s":NaN' in literal,
               "NaN remains an unquoted JSON token")

        marker = uuid.uuid4().hex
        token = ("TAMESHI_R18_ESCAPE_MARKER=" + marker).encode("ascii")
        record("unique-process-marker", token.count(marker.encode("ascii")) == 1,
               "one unique marker for P10 process observation")

        record("probe-id-domain", PROBE_IDS == tuple("P%02d" % n for n in range(1, 12)),
               "eleven stable probe ids")
    finally:
        assert_under_work(scratch, "selftest scratch cleanup")
        shutil.rmtree(scratch, ignore_errors=True)
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        print("SELFTEST: FAIL (%d/%d; %s)" %
              (len(checks) - len(failed), len(checks), ", ".join(failed)))
        return 1
    print("SELFTEST: PASS (%d cases)" % len(checks))
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] == "--_timeout-supervisor":
        if len(argv) != 6:
            print(json.dumps({"error": "internal supervisor needs five arguments"}))
            return 64
        try:
            return timeout_supervisor(*argv[1:])
        except Exception as exc:
            print(json.dumps({"error": "%s: %s" % (type(exc).__name__, exc)}))
            return 2

    parser = UsageParser(prog="defect-probes.py")
    parser.add_argument("--rev", metavar="REV")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--only", metavar="ID", choices=PROBE_IDS)
    parser.add_argument("--selftest", action="store_true")
    ns = parser.parse_args(argv)
    if ns.selftest:
        if ns.rev is not None or ns.only is not None or ns.json:
            parser.error("--selftest cannot be combined with --rev, --only, or --json")
        return selftest()
    if ns.rev is None:
        parser.error("--rev is required unless --selftest is given")

    work = None
    try:
        source_root = LANE_ROOT
        if not source_root.is_dir():
            raise ProbeError("lane root is unavailable: %s" % source_root)
        work = Path(tempfile.mkdtemp(
            prefix="tameshi-r18w1-X03DefectProbes-", dir="/tmp"))
        initialize_sandbox(work, source_root.parent)
        resolved = resolve_revision(source_root, ns.rev, work)
        clone_root = clone_lane_at(source_root, resolved, work)
        selected = [ns.only] if ns.only else list(PROBE_IDS)
        results = []
        errors = []
        for probe_id in selected:
            try:
                results.append(run_probe(probe_id, clone_root, work, resolved))
            except Exception as exc:
                errors.append((probe_id, "%s: %s" % (type(exc).__name__, exc)))
        if errors:
            for result in results:
                print("PROBE %s %s target=%s %s" %
                      (result["id"], result["status"], result["target"], result["detail"]),
                      file=sys.stderr if ns.json else sys.stdout)
            for probe_id, detail in errors:
                print("PROBE %s error %s" % (probe_id, detail),
                      file=sys.stderr if ns.json else sys.stdout)
            print("DEFECT_PROBES: could-not-evaluate (%d probe error(s))" % len(errors),
                  file=sys.stderr if ns.json else sys.stdout)
            return 2
        emit_results(results, resolved, ns.json)
        return 0
    except ProbeError as exc:
        print("DEFECT_PROBES: could-not-evaluate (%s)" % exc, file=sys.stderr)
        return 2
    finally:
        if work is not None:
            assert_under_work(work, "probe scratch cleanup")
            shutil.rmtree(work, ignore_errors=True)
if __name__ == "__main__":
    raise SystemExit(main())
