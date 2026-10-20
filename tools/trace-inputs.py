#!/usr/bin/env python3
"""tools/trace-inputs.py — record the input-file surface of one lane command.

Runs ARGV under ``strace -f`` tracing only file-open/exec/chdir/dup syscalls,
passes the command's stdout/stderr through, and writes a JSON receipt:

  {"schema": "tameshi-trace-inputs-v1",
   "argv": [...], "cwd": <abs>, "root": <abs>, "rev": <40hex|null>,
   "rev_reason": "not_a_repo|repo_identity_mismatch|rev_unavailable|null",
   "exit": <int>, "tracked_filter": <bool>,
   "env_overrides": {"git_vars_removed": [...], "set": {...}},
   "inputs":    {<lane-relative path>: <sha256>},
   "untracked": {<lane-relative path>: <sha256>},   (only when tracked_filter)
   "external":  {<abs path under fleet root>: <sha256>},
   "live_lane_reads": {<abs path under live lane>: <sha256>},
   "dropped_home_count": <int>}

``inputs`` holds successful opens of regular files under --root that are
tracked at HEAD (``git -C root ls-files -z --cached --full-name``), realpath
resolved, excluding any path with a ``.git`` component. Untracked opens under
root are reported under ``untracked`` and never credited. When root is not a
git repository ``tracked_filter`` is false and every regular-file read under
root lands in ``inputs``.

``external`` is restricted to the fleet root (default
/home/vgpnk/Projects/shokunin) minus ``.git`` components; every other opened
path under /home is counted in ``dropped_home_count`` and never hashed, so
credential files can neither be read nor leaked into a receipt.
``live_lane_reads`` flags opens under the live lane (default
<fleet>/tameshi-shokunin) when --root is somewhere else — a clone run that
reads the live tree is not provenance.

Write-mode opens (O_WRONLY/O_RDWR/O_CREAT/O_TRUNC/O_APPEND/O_TMPFILE, i.e.
every creat(2)), O_DIRECTORY opens, failed opens, non-regular files and
deleted files are never recorded. A path opened write-mode at any point in
the run is removed from every bucket (read-then-rewrite). execve'd files are
recorded like opens, so a script under --root run via execve counts.

The child environment is scrubbed of every GIT_* variable and gets
PYTHONDONTWRITEBYTECODE=1 plus PYTHONPYCACHEPREFIX under a private workdir
outside --root, so a lane module import opens its .py source and never
deposits (or credits) a __pycache__ file. Relative paths are resolved against
the traced process's cwd at open time by the kernel: ``strace -y`` is
required (a failed probe is exit 2), with ``--seccomp-bpf``,
``--kill-on-exit`` and ``--strings-in-hex=non-ascii`` added when supported.
Annotations and quoted paths are C-unescaped, so non-ASCII bytes, quotes and
angle brackets survive. The strace log and cache live in a private mkdtemp
outside --root and are deleted on exit.

Exit 2 unless the root traced process (first pid in the log) executed at
least one successful execve/execveat: a failed strace spawn or a missing
command is a setup failure, not an empty trace. Otherwise 0 (the command's
exit status is in the JSON), 64 on usage. ``--selftest`` runs synthetic
fixtures only, location-independent.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

SCHEMA = "tameshi-trace-inputs-v1"

DEFAULT_FLEET = "/home/vgpnk/Projects/shokunin"
DEFAULT_LANE = os.path.join(DEFAULT_FLEET, "tameshi-shokunin")
DEFAULT_HOME = "/home"

TRACE_SYSCALLS = (
    "open,openat,openat2,creat,"
    "execve,execveat,"
    "chdir,fchdir,"
    "fork,vfork,clone,clone3,"
    "dup,dup2,dup3,close"
)

WRITE_FLAGS_RE = re.compile(r"\bO_(?:WRONLY|RDWR|CREAT|TRUNC|APPEND|TMPFILE)\b")
DIR_FLAG_RE = re.compile(r"\bO_DIRECTORY\b")

LINE_RE = re.compile(r"^\s*(\d+)\s+(.*)$")
CALL_RE = re.compile(r"^(\w+)\((.*)\)\s*=\s*(.*)$")
UNFINISHED_RE = re.compile(r"^(\w+)\((.*)<unfinished \.\.\.>\s*$")
RESUMED_RE = re.compile(r"^<\.\.\.\s+(\w+)\s+resumed>\s*(.*)$")
FD_TOKEN_RE = re.compile(r"^(-?\d+|AT_FDCWD)(?:<(.*)>)?\s*$")
RET_RE = re.compile(r"^(-?\d+)(?:<(.*)>)?\s*$")
EXIT_RE = re.compile(r"^\+\+\+ exited with (-?\d+) \+\+\+$")
KILLED_RE = re.compile(r"^\+\+\+ killed by (SIG[A-Z0-9]+)")
REV_RE = re.compile(r"^[0-9a-f]{40}$")

PATH_CALLS = {"open": 0, "openat": 1, "openat2": 1, "execve": 0,
              "execveat": 1, "chdir": 0, "creat": 0}
DIRFD_CALLS = {"openat": 0, "openat2": 0, "execveat": 0}
FORK_CALLS = {"fork", "vfork", "clone", "clone3"}
DUP_CALLS = {"dup", "dup2", "dup3"}

_SIMPLE_ESC = {"n": b"\n", "t": b"\t", "r": b"\r", "a": b"\a",
               "b": b"\b", "f": b"\f", "v": b"\v", "\\": b"\\",
               '"': b'"', "'": b"'", "?": b"?"}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write("%s: error: %s\n" % (self.prog, message))
        sys.exit(64)


def c_unescape(body):
    """Decode strace C escapes (\\xNN, octal, simple) without quotes.

    Returns str via os.fsdecode (surrogateescape for invalid bytes), or None
    when the text is truncated or malformed.
    """
    buf = bytearray()
    i, n = 0, len(body)
    while i < n:
        c = body[i]
        if c != "\\":
            buf += c.encode("utf-8", "surrogateescape")
            i += 1
            continue
        i += 1
        if i >= n:
            return None
        e = body[i]
        if e == "x":
            j, h = i + 1, ""
            while j < n and len(h) < 2 and body[j] in "0123456789abcdefABCDEF":
                h += body[j]
                j += 1
            if not h:
                return None
            buf.append(int(h, 16))
            i = j
            continue
        if e in "01234567":
            j, o = i, ""
            while j < n and len(o) < 3 and body[j] in "01234567":
                o += body[j]
                j += 1
            buf.append(int(o, 8) & 0xFF)
            i = j
            continue
        if e in _SIMPLE_ESC:
            buf += _SIMPLE_ESC[e]
        else:
            buf += e.encode("utf-8", "surrogateescape")
        i += 1
    return os.fsdecode(bytes(buf))


def _unquote(tok):
    """Decode one strace C-quoted string token. None if not a complete,
    untruncated string."""
    if tok is None:
        return None
    tok = tok.strip()
    if not tok.startswith('"'):
        return None
    body, esc, i, n = [], False, 1, len(tok)
    while i < n:
        ch = tok[i]
        if esc:
            body.append(ch)
            esc = False
        elif ch == "\\":
            body.append(ch)
            esc = True
        elif ch == '"':
            if tok[i + 1:].lstrip().startswith("..."):
                return None  # strace -s truncation: path tail lost
            return c_unescape("".join(body))
        else:
            body.append(ch)
        i += 1
    return None


def decode_annotation(body):
    if body is None:
        return None
    body = body.strip()
    if body.endswith(" (deleted)"):
        return None
    return c_unescape(body)


def split_args(argstr):
    """Split a strace argument string on top-level commas, respecting quoted
    strings and ()[]{} nesting."""
    out, cur, depth, in_q, esc = [], [], 0, False, False
    for ch in argstr:
        if in_q:
            cur.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_q = False
        else:
            if ch == '"':
                in_q = True
                cur.append(ch)
            elif ch in "([{":
                depth += 1
                cur.append(ch)
            elif ch in ")]}":
                depth = max(0, depth - 1)
                cur.append(ch)
            elif ch == "," and depth == 0:
                out.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
    if "".join(cur).strip():
        out.append("".join(cur).strip())
    return out


def fd_token(tok):
    """'AT_FDCWD</cwd>' -> ('AT_FDCWD', '/cwd'); '5</dir>' -> ('5','/dir')."""
    if tok is None:
        return None, None
    m = FD_TOKEN_RE.match(tok.strip())
    if not m:
        return None, None
    return m.group(1), decode_annotation(m.group(2))


def parse_ret(retstr):
    """-> (ok, int_value|None, annotation|None).  '-1 ...' and '?' are not ok."""
    r = retstr.strip()
    if not r or r.startswith("?") or r.startswith("-1"):
        return False, None, None
    m = RET_RE.match(r)
    if not m:
        return False, None, None
    try:
        val = int(m.group(1))
    except ValueError:
        return False, None, None
    if val < 0:
        return False, None, None
    return True, val, decode_annotation(m.group(2))


def under(path, prefix):
    return bool(prefix) and (path == prefix or path.startswith(prefix + os.sep))


def has_git_component(path, base):
    try:
        rel = os.path.relpath(path, base)
    except ValueError:
        return False
    return ".git" in rel.split(os.sep)


class Tracer(object):
    def __init__(self, root, cwd0, tracked, fleet, lane, home):
        self.root = root
        self.cwd0 = cwd0
        self.tracked = tracked
        self.fleet = fleet
        self.lane = lane
        self.home = home
        self.states = {}   # pid -> {"cwd": str, "fds": {fd: path}}
        self.pending = {}  # pid -> (name, partial_argstr)
        self.inputs = set()
        self.untracked = set()
        self.external = set()
        self.lane_reads = set()
        self.writes = set()
        self.dropped_home = 0
        self.first_pid = None
        self.exec_ok = set()
        self.exits = {}

    def st(self, pid):
        s = self.states.get(pid)
        if s is None:
            s = {"cwd": self.cwd0, "fds": {}}
            self.states[pid] = s
        return s

    def record(self, resolved):
        if not resolved:
            return
        if under(resolved, self.root):
            if has_git_component(resolved, self.root):
                return
            if self.tracked is not None and resolved not in self.tracked:
                self.untracked.add(resolved)
            else:
                self.inputs.add(resolved)
        elif self.lane and self.root != self.lane and under(resolved, self.lane):
            self.lane_reads.add(resolved)
        elif under(resolved, self.fleet):
            if not has_git_component(resolved, self.fleet):
                self.external.add(resolved)
        elif under(resolved, self.home):
            # Never hash or name a non-fleet /home path: credentials may live
            # there and this receipt is committed. Count only.
            self.dropped_home += 1

    def fd_path(self, st, tok):
        base, ann = fd_token(tok)
        if ann and ann.startswith("/"):
            return ann
        try:
            return st["fds"].get(int(base))
        except (TypeError, ValueError):
            return None

    def resolve(self, pid, dirfd_base, dirfd_ann, path):
        if not path:
            return None
        if path.startswith("/"):
            return os.path.realpath(path)
        st = self.st(pid)
        base = None
        if dirfd_ann and dirfd_ann.startswith("/"):
            base = dirfd_ann
        elif dirfd_base == "AT_FDCWD" or dirfd_base is None:
            base = st["cwd"]
        else:
            try:
                base = st["fds"].get(int(dirfd_base))
            except ValueError:
                base = None
        if base is None:
            return None
        return os.path.realpath(os.path.join(base, path))

    def call(self, pid, name, argstr, retstr):
        ok, val, ann = parse_ret(retstr)
        st = self.st(pid)
        if name in FORK_CALLS:
            if ok and val and val > 0:
                self.states[val] = {"cwd": st["cwd"], "fds": dict(st["fds"])}
            return
        toks = split_args(argstr)
        if name == "close":
            if ok and toks:
                n, _ = fd_token(toks[0])
                try:
                    st["fds"].pop(int(n), None)
                except (TypeError, ValueError):
                    pass
            return
        if name in DUP_CALLS:
            if ok and val is not None and val >= 0 and toks:
                src = self.fd_path(st, toks[0])
                if src:
                    st["fds"][val] = src
            return
        if name == "chdir":
            if ok and toks:
                p = _unquote(toks[0])
                if p is not None:
                    st["cwd"] = os.path.realpath(
                        p if p.startswith("/") else os.path.join(st["cwd"], p))
            return
        if name == "fchdir":
            if ok and toks:
                src = self.fd_path(st, toks[0])
                if src and src.startswith("/"):
                    st["cwd"] = src
            return
        if name == "creat":
            if not ok or not toks:
                return
            p = _unquote(toks[0])
            resolved = self.resolve(pid, "AT_FDCWD", None, p) if p is not None else None
            if resolved:
                self.writes.add(resolved)
            return
        if name in ("open", "openat", "openat2"):
            idx = PATH_CALLS[name]
            if len(toks) <= idx:
                return
            path = _unquote(toks[idx])
            if path is None or not ok:
                return  # failed opens are not inputs
            tail = ",".join(toks[idx + 1:])
            dbase = dann = None
            if name in DIRFD_CALLS and toks:
                dbase, dann = fd_token(toks[0])
            if ann is not None and ann.startswith("/"):
                resolved = ann
            else:
                resolved = self.resolve(pid, dbase, dann, path)
            if WRITE_FLAGS_RE.search(tail):
                # Any write-mode open disqualifies the path for the whole run,
                # including read-then-rewrite sequences.
                if resolved:
                    self.writes.add(resolved)
                return
            if DIR_FLAG_RE.search(tail):
                return
            self.record(resolved)
            if resolved and val is not None and val >= 0:
                st["fds"][val] = resolved
            return
        if name in ("execve", "execveat"):
            idx = PATH_CALLS[name]
            if len(toks) <= idx:
                return
            path = _unquote(toks[idx])
            if not ok or path is None:
                return
            if name == "execveat" and path == "":
                return  # AT_EMPTY_PATH style: no path component
            dbase = dann = None
            if name == "execveat" and toks:
                dbase, dann = fd_token(toks[0])
            self.record(self.resolve(pid, dbase or "AT_FDCWD", dann, path))
            if pid == self.first_pid:
                self.exec_ok.add(pid)
            return

    def feed(self, line):
        m = LINE_RE.match(line)
        if not m:
            return
        pid = int(m.group(1))
        if self.first_pid is None:
            self.first_pid = pid
        rest = m.group(2).strip()
        if not rest:
            return
        em = EXIT_RE.match(rest)
        if em:
            self.exits[pid] = int(em.group(1))
            self.states.pop(pid, None)
            self.pending.pop(pid, None)
            return
        km = KILLED_RE.match(rest)
        if km:
            sig = 0
            try:
                sig = int(signal.Signals[km.group(1)].value)
            except (KeyError, ValueError):
                sig = 0
            self.exits[pid] = 128 + sig if sig else 128
            self.states.pop(pid, None)
            self.pending.pop(pid, None)
            return
        if rest.startswith("---") or rest.startswith("strace:"):
            return
        if rest.startswith("+++"):
            self.states.pop(pid, None)
            self.pending.pop(pid, None)
            return
        rm = RESUMED_RE.match(rest)
        if rm:
            name, tail = rm.group(1), rm.group(2)
            pend = self.pending.pop(pid, None)
            if pend and pend[0] != name:
                pend = None
            if "<unfinished ...>" in tail:
                frag = tail[: tail.index("<unfinished ...>")]
                self.pending[pid] = (name, (pend[1] if pend else "") + frag)
                return
            if " = " not in tail:
                return
            argpart, ret = tail.rsplit(" = ", 1)
            candidates = [argpart]
            if pend:
                candidates.append(pend[1] + argpart)
            for cand in candidates:
                cs = cand.rstrip()
                if not cs.endswith(")"):
                    continue
                cargs = cs[:-1]
                if name in PATH_CALLS:
                    toks = split_args(cargs)
                    idx = PATH_CALLS[name]
                    ptok = toks[idx] if len(toks) > idx else None
                    if _unquote(ptok) is None:
                        continue
                self.call(pid, name, cargs, ret)
                return
            return
        um = UNFINISHED_RE.match(rest)
        if um:
            self.pending[pid] = (um.group(1), um.group(2))
            return
        cm = CALL_RE.match(rest)
        if cm:
            self.call(pid, cm.group(1), cm.group(2), cm.group(3))
            return


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scrubbed_env(workdir):
    """Child environment: no GIT_* (a stray GIT_DIR rewrites another repo's
    index), no .pyc reads/writes from the tree."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    removed = sorted(k for k in os.environ if k.startswith("GIT_"))
    cache = os.path.join(workdir, "pycache")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPYCACHEPREFIX"] = cache
    return env, removed, cache


def git_run(argv, env):
    try:
        return subprocess.run(argv, capture_output=True, timeout=30, env=env)
    except (OSError, subprocess.TimeoutExpired):
        return None


def repo_filter(root, env):
    """-> (tracked_abs_set|None, rev|None, rev_reason|None)."""
    top = git_run(["git", "--no-optional-locks", "-C", root,
                   "rev-parse", "--show-toplevel"], env)
    if top is None or top.returncode != 0:
        return None, None, "not_a_repo"
    toplevel = os.path.realpath(os.fsdecode(top.stdout.strip()))
    if toplevel != root:
        rev, reason = None, "repo_identity_mismatch"
    else:
        head = git_run(["git", "--no-optional-locks", "-C", root,
                        "rev-parse", "--verify", "HEAD"], env)
        head_sha = os.fsdecode(head.stdout.strip()) if head and head.returncode == 0 else ""
        if head_sha and REV_RE.match(head_sha):
            rev, reason = head_sha, None
        else:
            rev, reason = None, "rev_unavailable"
    ls = git_run(["git", "--no-optional-locks", "-C", root,
                  "ls-files", "-z", "--cached", "--full-name"], env)
    if ls is None or ls.returncode != 0:
        return None, rev, reason
    tracked = set()
    for raw in ls.stdout.split(b"\0"):
        if raw:
            tracked.add(os.path.realpath(os.path.join(toplevel, os.fsdecode(raw))))
    return tracked, rev, reason


def probe_flags(strace_bin, workdir, true_bin):
    """Pick the strongest supported flag set; -y is mandatory."""
    candidates = [
        ["-y", "--seccomp-bpf", "--kill-on-exit", "--strings-in-hex=non-ascii"],
        ["-y", "--strings-in-hex=non-ascii"],
        ["-y"],
    ]
    for n, flags in enumerate(candidates):
        log = os.path.join(workdir, "probe-%d.log" % n)
        try:
            rc = subprocess.call(
                [strace_bin] + flags + ["-e", "trace=none", "-o", log, "--", true_bin],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            return None
        if rc == 0:
            return flags
    return None


def make_workdir(root):
    """A private directory that is NOT inside root and not equal to it."""
    cands = [tempfile.gettempdir(), "/var/tmp", "/dev/shm",
             os.path.expanduser("~/.cache"), "/tmp"]
    seen = set()
    for cand in cands:
        if not cand or cand in seen:
            continue
        seen.add(cand)
        try:
            real = os.path.realpath(cand)
        except OSError:
            continue
        if not os.path.isdir(real):
            continue
        if real == root or real.startswith(root + os.sep):
            continue
        try:
            return tempfile.mkdtemp(prefix="trace-inputs-run-", dir=real)
        except OSError:
            continue
    return None


def run_trace(ns):
    root = os.path.realpath(ns.root)
    if not os.path.isdir(root):
        sys.stderr.write("trace-inputs: root not a directory: %s\n" % root)
        return 2
    cwd = os.path.realpath(ns.cwd if ns.cwd else root)
    if not os.path.isdir(cwd):
        sys.stderr.write("trace-inputs: cwd not a directory: %s\n" % cwd)
        return 2
    strace_bin = shutil.which("strace")
    if not strace_bin:
        sys.stderr.write("trace-inputs: strace not found in PATH\n")
        return 2
    workdir = make_workdir(root)
    if workdir is None:
        sys.stderr.write("trace-inputs: no temp directory outside root\n")
        return 2
    try:
        env, removed_git, pycache = scrubbed_env(workdir)
        true_bin = shutil.which("true") or "/usr/bin/true"
        flags = probe_flags(strace_bin, workdir, true_bin)
        if flags is None:
            sys.stderr.write("trace-inputs: strace -y unusable (probe failed)\n")
            return 2

        fleet = os.path.realpath(ns.fleet_root)
        lane = os.path.realpath(ns.live_lane)
        home = os.path.realpath(ns.home_prefix)
        tracked, rev, rev_reason = repo_filter(root, env)

        log = os.path.join(workdir, "trace.log")
        strace_argv = ([strace_bin, "-f", "-q", "-z", "-s", "4096", "-o", log,
                        "-e", "trace=" + TRACE_SYSCALLS] + flags + ["--"] + list(ns.cmd))
        try:
            proc = subprocess.run(strace_argv, cwd=cwd, env=env)
        except OSError as exc:
            sys.stderr.write("trace-inputs: strace launch failed: %s\n" % exc)
            return 2

        tracer = Tracer(root, cwd, tracked, fleet, lane, home)
        if os.path.exists(log):
            with open(log, "r", encoding="utf-8", errors="surrogateescape") as fh:
                for line in fh:
                    tracer.feed(line)
        # A trace is only meaningful if the root process actually executed.
        if tracer.first_pid is None or tracer.first_pid not in tracer.exec_ok:
            sys.stderr.write(
                "trace-inputs: no successful execve for the root process "
                "(strace setup failure or missing command)\n")
            return 2
        cmd_exit = tracer.exits.get(tracer.first_pid, proc.returncode)

        def digest(paths):
            out = {}
            for path in sorted(paths):
                if path in tracer.writes or not os.path.isfile(path):
                    continue
                out[path] = sha256_file(path)
            return out

        rel = lambda p: os.path.relpath(p, root)  # noqa: E731
        inputs = {rel(p): h for p, h in digest(tracer.inputs).items()}
        untracked = {rel(p): h for p, h in digest(tracer.untracked).items()}
        external = digest(tracer.external)
        lane_reads = digest(tracer.lane_reads)

        payload = {
            "schema": SCHEMA,
            "argv": list(ns.cmd),
            "cwd": cwd,
            "root": root,
            "rev": rev,
            "rev_reason": rev_reason,
            "exit": cmd_exit,
            "tracked_filter": tracked is not None,
            "env_overrides": {
                "git_vars_removed": removed_git,
                "set": {
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONPYCACHEPREFIX": pycache,
                },
            },
            "inputs": inputs,
            "untracked": untracked,
            "external": external,
            "live_lane_reads": lane_reads,
            "dropped_home_count": tracer.dropped_home,
        }
        out_dir = os.path.dirname(os.path.abspath(ns.out))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(ns.out, "w") as fh:
            json.dump(payload, fh, indent=2)
            fh.write("\n")
        return 0
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _which(name):
    return shutil.which(name) or name


def selftest():
    tmp = tempfile.mkdtemp(prefix="trace-inputs-selftest-")
    fleet = os.path.join(tmp, "fleet")
    lane = os.path.join(fleet, "tameshi-shokunin")
    homeprefix = os.path.join(tmp, "homecases")
    os.makedirs(lane)
    os.makedirs(homeprefix)
    root = os.path.join(tmp, "root")
    os.makedirs(os.path.join(root, "sub"))
    os.makedirs(os.path.join(root, ".git"))
    scratch = os.path.join(tmp, "scratchtmp")
    os.makedirs(scratch)

    def put(base, rel, data, mode=0o644):
        path = os.path.join(base, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data)
        os.chmod(path, mode)
        return path

    put(root, "a.txt", "alpha\n")
    put(root, "s.sh", "SOURCED=1\n")
    put(root, "sub/c.txt", "child\n")
    put(root, "rw.txt", "rw\n")
    put(root, "rwread.txt", "before\n")
    put(root, ".git/secret", "git-internal\n")
    put(root, "target.txt", "tgt\n")
    put(root, "run.sh", "#!/bin/sh\nexit 0\n", 0o755)
    put(root, "mod.py", "X = 1\n")
    put(root, "imp.py", "import mod, mod\n")
    put(root, "h\u00e9llo.txt", "h\n")
    put(root, "we\"ird.txt", "w\n")
    put(root, "ang<le>.txt", "a\n")
    os.symlink("target.txt", os.path.join(root, "link_in"))
    outside = os.path.join(tmp, "outside.txt")
    put(tmp, "outside.txt", "outside\n")
    os.symlink(outside, os.path.join(root, "link_out"))
    ext = put(fleet, "other/ext.txt", "fleet-external\n")
    live = put(lane, "live.txt", "live-lane\n")
    homefile = put(homeprefix, "user/creds-like.txt", "not-hashed\n")

    # Isolated git fixture: the selftest harness itself must never leak a
    # GIT_* variable into a repository operation (N01 F1).
    fixture_env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    fixture_env.update({
        "HOME": os.path.join(tmp, "home"),
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
    })
    os.makedirs(fixture_env["HOME"])

    def git(*args, cwd):
        return subprocess.run(["git", "-C", cwd] + list(args), env=fixture_env,
                              capture_output=True, text=True)

    gitroot = os.path.join(tmp, "gitroot")
    os.makedirs(os.path.join(gitroot, "sub"))
    git("init", "-q", cwd=gitroot)
    put(gitroot, "tracked.txt", "tracked\n")
    put(gitroot, "sub/tracked.txt", "subtracked\n")
    git("add", ".", cwd=gitroot)
    git("commit", "-q", "-m", "init", cwd=gitroot)
    put(gitroot, "untracked.txt", "untracked\n")
    head_sha = git("rev-parse", "HEAD", cwd=gitroot).stdout.strip()

    tool = os.path.abspath(__file__)
    PY = _which("python3")
    SH = _which("bash")
    counter = [0]
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    def trace(argv, use_root=None, env=None, capture=False, cwd_opt=None,
              extra=None):
        counter[0] += 1
        outp = os.path.join(tmp, "out-%d.json" % counter[0])
        cmd = [sys.executable, tool,
               "--root", use_root or root,
               "--fleet-root", fleet,
               "--live-lane", lane,
               "--home-prefix", homeprefix,
               "--out", outp]
        if cwd_opt:
            cmd += ["--cwd", cwd_opt]
        if extra:
            cmd += list(extra)
        cmd += ["--"] + list(argv)
        run_env = dict(os.environ)
        run_env["TMPDIR"] = scratch
        if env:
            run_env.update(env)
        proc = subprocess.run(cmd, env=run_env,
                              stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        data = None
        if os.path.exists(outp):
            with open(outp, encoding="utf-8") as fh:
                data = json.load(fh)
        return proc.returncode, data, (proc.stdout or b"").decode("utf-8", "replace")

    rc, d, _ = trace([PY, "-c", "open('a.txt').read()"])
    check("python-read-input", rc == 0 and d and d["inputs"].get("a.txt"))

    rc, d, _ = trace([SH, "-c", "source s.sh"])
    check("bash-source-input", rc == 0 and d and "s.sh" in d["inputs"])

    rc, d, _ = trace([SH, "-c", "cd sub && cat c.txt"])
    check("cd-relative-input", rc == 0 and d and "sub/c.txt" in d["inputs"])

    rc, d, _ = trace([PY, "-c", "open('w.txt','w').write('x')"])
    check("write-open-excluded", rc == 0 and d and "w.txt" not in d["inputs"])
    rc, d, _ = trace([PY, "-c",
                      "import os; fd=os.open('rw.txt', os.O_RDWR); os.close(fd)"])
    check("rdwr-open-excluded", rc == 0 and d and "rw.txt" not in d["inputs"])


    rc, d, _ = trace([PY, "-c",
                      "open('rwread.txt').read(); open('rwread.txt','w').write('after')"])
    check("read-then-rewrite-excluded", rc == 0 and d and "rwread.txt" not in d["inputs"])

    rc, d, _ = trace([PY, "-c", "open(%r).read()" % ext])
    check("fleet-external", rc == 0 and d and ext in d["external"])

    rc, d, _ = trace([PY, "-c", "open(%r).read()" % live])
    check("live-lane-flagged",
          rc == 0 and d and live in d["live_lane_reads"]
          and live not in d["external"])

    rc, d, _ = trace([PY, "-c", "open(%r).read()" % homefile])
    check("non-fleet-home-counted",
          rc == 0 and d and d["dropped_home_count"] == 1
          and homefile not in d["external"]
          and not any("creds-like" in k for k in d["inputs"]))

    rc, d, _ = trace([PY, "-c", "open(%r).read()" % outside])
    check("non-home-outside-dropped",
          rc == 0 and d and outside not in d["external"]
          and not d["inputs"] and d["dropped_home_count"] == 0)

    rc, d, _ = trace([PY, "-c", "open('a.txt').read()"],
                     env={"PATH": "/nonexistent-ti-dir"})
    check("missing-strace-exit2", rc == 2 and d is None)

    rc, d, _ = trace(["./no-such-command-xyz"])
    check("missing-command-exit2", rc == 2 and d is None)
    fake_strace = put(
        tmp, "fakebin/strace",
        "#!/bin/sh\n"
        "while [ \"$#\" -gt 0 ]; do\n"
        "  if [ \"$1\" = \"-o\" ]; then shift; log=$1; fi\n"
        "  shift\n"
        "done\n"
        "printf '%s\\n' '12345 openat(AT_FDCWD, \"a.txt\", O_RDONLY) = 3' > \"$log\"\n"
        "exit 0\n",
        0o755)
    old_path = os.environ.get("PATH")
    fakebin = os.path.dirname(fake_strace)
    os.environ["PATH"] = fakebin + (os.pathsep + old_path if old_path else "")
    try:
        rc, d, _ = trace([PY, "-c", "pass"])
    finally:
        if old_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = old_path
    check("root-exec-required", rc == 2 and d is None)


    rc, d, _ = trace([PY, "-c", "open('.git/secret').read()"])
    check("dotgit-excluded", rc == 0 and d and ".git/secret" not in d["inputs"])

    rc, d, _ = trace([PY, "-c", "open('link_in').read()"])
    check("symlink-in-resolves",
          rc == 0 and d and "target.txt" in d["inputs"] and "link_in" not in d["inputs"])

    rc, d, _ = trace([PY, "-c", "open('link_out').read()"])
    check("symlink-out-not-input", rc == 0 and d and "link_out" not in d["inputs"])

    rc, d, _ = trace([PY, "-c", "open('nope.txt').read()"])
    check("failed-open-excluded", rc == 0 and d and "nope.txt" not in d["inputs"])

    rc, d, _ = trace(["./run.sh"])
    check("execve-script-input", rc == 0 and d and "run.sh" in d["inputs"])

    rc, d, _ = trace([PY, "-c", "import os; os.listdir('.')"])
    check("directory-open-excluded", rc == 0 and d and "." not in d["inputs"])

    rc, d, _ = trace([PY, "-c", "import sys; sys.exit(3)"])
    check("command-exit-recorded", rc == 0 and d and d["exit"] == 3)

    rc, d, _ = trace([PY, "-c", "pass"])
    check("nongit-root-unfiltered",
          rc == 0 and d and d["rev"] is None and d["rev_reason"] == "not_a_repo"
          and d["tracked_filter"] is False and "imp.py" not in d["inputs"])

    rc, d, _ = trace([PY, "-c",
                      "open('tracked.txt').read(); open('untracked.txt').read()"],
                     use_root=gitroot)
    check("git-tracked-filter",
          rc == 0 and d and "tracked.txt" in d["inputs"]
          and "untracked.txt" in d["untracked"] and "untracked.txt" not in d["inputs"]
          and d["tracked_filter"] is True and d["rev"] == head_sha)

    rc, d, _ = trace([PY, "-c", "open('tracked.txt').read()"],
                     use_root=os.path.join(gitroot, "sub"))
    check("subdir-root-rev-null",
          rc == 0 and d and d["rev"] is None
          and d["rev_reason"] == "repo_identity_mismatch"
          and d["tracked_filter"] is True and "tracked.txt" in d["inputs"])

    rc, d, out = trace([SH, "-c", "env"], capture=True, env={"GIT_DIR": os.path.join(tmp, "bogus")})
    lines = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
    check("env-scrubbed",
          rc == 0 and d and "GIT_DIR" not in lines
          and lines.get("PYTHONDONTWRITEBYTECODE") == "1"
          and lines.get("PYTHONPYCACHEPREFIX")
          and "GIT_DIR" in d["env_overrides"]["git_vars_removed"]
          and d["env_overrides"]["set"].get("PYTHONDONTWRITEBYTECODE") == "1")
    pycache = d["env_overrides"]["set"].get("PYTHONPYCACHEPREFIX") if d else None
    check("pycache-prefix-private",
          rc == 0 and d
          and lines.get("PYTHONPYCACHEPREFIX") == pycache
          and pycache and os.path.isabs(pycache)
          and not under(pycache, root))


    rc, d, _ = trace([SH, "-c", "python3 imp.py && python3 imp.py"])
    check("double-import-keeps-py",
          rc == 0 and d and "mod.py" in d["inputs"]
          and not any("__pycache__" in k for k in d["inputs"]))

    names = ["h\u00e9llo.txt", "we\"ird.txt", "ang<le>.txt"]
    rc, d, _ = trace([PY, "-c",
                      "[open(n).read() for n in %r]" % (names,)])
    check("escaped-names-recorded",
          rc == 0 and d and all(n in d["inputs"] for n in names))

    rc, d, _ = trace([PY, "-c", "open('c.txt').read()"],
                     cwd_opt=os.path.join(root, "sub"))
    check("cwd-option-input", rc == 0 and d and "sub/c.txt" in d["inputs"])

    leftover = os.listdir(scratch)
    check("temp-workdirs-deleted", leftover == [])

    tree_names = []
    for base, dirs, files in os.walk(root):
        tree_names += dirs + files
    check("no-artifacts-inside-root",
          not any(n.startswith("trace-inputs-run-") for n in tree_names)
          and "__pycache__" not in tree_names)

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        sys.stdout.write("%s %s\n" % ("PASS" if ok else "FAIL", name))
    sys.stdout.write("SELFTEST: %d/%d\n" % (passed, len(checks)))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if passed == len(checks) else 1


def main(argv):
    p = Parser(prog="trace-inputs.py",
               description="Record the regular files a command opens, keyed under --root.")
    p.add_argument("--root", metavar="DIR", help="lane root the inputs are relative to")
    p.add_argument("--cwd", metavar="DIR", help="command working directory (default: --root)")
    p.add_argument("--out", metavar="FILE", help="JSON receipt output path")
    p.add_argument("--fleet-root", metavar="DIR", default=DEFAULT_FLEET,
                   help="fleet prefix for external inputs (default: %s)" % DEFAULT_FLEET)
    p.add_argument("--live-lane", metavar="DIR", default=DEFAULT_LANE,
                   help="live lane prefix flagged when --root is elsewhere")
    p.add_argument("--home-prefix", metavar="DIR", default=DEFAULT_HOME,
                   help="home prefix counted (never hashed) outside the fleet")
    p.add_argument("--selftest", action="store_true", help="run synthetic self-checks")
    p.add_argument("cmd", nargs=argparse.REMAINDER, help="-- ARGV to trace")
    ns = p.parse_args(argv)

    if ns.selftest:
        return selftest()

    cmd = list(ns.cmd)
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not ns.root:
        p.error("--root is required")
    if not ns.out:
        p.error("--out is required")
    if not cmd:
        p.error("an ARGV after -- is required")
    ns.cmd = cmd
    return run_trace(ns)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
