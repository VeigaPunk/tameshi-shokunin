#!/usr/bin/env python3
"""ledger-witness.py — kernel-witnessed audit of `tools/mutate-and-run.sh --regression`.

Round 89 (tameshi). The runner's own `REGRESSION: PASS` line is a figure the subject
prints; rounds 85-88 showed that a counter reading such figures is passed by
counterfeits that print them without doing the work (stub, parked, dupbase). This
witness does not trust what the runner prints. It runs the runner under strace(1)
(`-f`: follow every fork; `-y`: decode each fd to its path) and binds the declared
ledger to what the kernel observed:

  W_PARSE    the runner bytes declare >=1 leg in the ledger call shape; every PIN_/REV_/
             TABLE_ variable and embedded spec a leg names resolves.
  W_TABLE    every recorded table value is KILLED or SURVIVED (round-88 M7).
  W_PATH     every leg path is fleet-relative, its first component a directory name, no
             component '', '.' or '..' (round-88 T88E2 dupbase/fleet-root latent).
  W_DUP      leg names, (repo, path) pairs and blob sha256 pins are pairwise distinct
             (QUALITY 135: distinctness keyed on object identity, never path spelling).
  W_PIN      the witness's own `git cat-file blob REV:PATH` in the leg's repo has the
             declared PIN sha256 (repo must be its own toplevel).
  W_SPEC     the witness's own parse of the leg's embedded spec applies every defect
             exactly once to that blob, and the spec ids equal the table ids.
  W_RUN      the runner exited 0, printed `REGRESSION_CASE <leg>: PASS` once per leg
             and nothing else, and `REGRESSION: PASS (cases=N passed=N` with N = legs.
  W_MAT      the trace shows a successful `git ... show REV:PATH` execve per leg.
  W_CONTROL  the pristine copy was exec'd by the leg's interpreter and exited 0, and
             its bytes equal the pinned blob.
  W_EXEC     every defect's mutant path was exec'd by the leg's interpreter (the path is
             the interpreter's script argument, not merely somewhere in argv).
  W_CONTENT  every mutant file left in the workdir has the sha256 the witness computes
             by applying the spec edit to the pinned blob itself.
  W_ORDER    no write-class syscall (write-open, write/pwrite/ftruncate on an fd decoded
             to the file, rename/link/symlink/truncate naming it) touches a mutant or
             pristine file (exact absolute path; an unanchored relative path is matched by
             basename) after that file's first interpreter exec.
  W_VERDICT  each mutant's interpreter pid exit, as the kernel reported it (exit 0 ->
             SURVIVED; exit n not in {0,124,126,127} -> KILLED; else INCONCLUSIVE),
             equals the recorded table verdict.
  W_EXTRA    no interpreter exec of a mutant/pristine path under the workdir that the
             declared legs do not account for.
  W_ENV      no audited interpreter exec carries a steering variable (NODE_OPTIONS,
             BASH_ENV, LD_PRELOAD, BASH_FUNC_*, ...); each mutant exec's environment equals
             its leg's control exec environment once MUTANT/DEFECT_ID and the sandbox id
             token are normalized; no rlimit is set except by an audited interpreter
             after its own exec. (`--run` starts the runner from a clean, declared env.)

Modes:
  --run    --runner FILE --fleet ROOT --scratch DIR   shadow the runner into
           DIR/fleet/<lane>/tools/ (sibling repos symlinked), run it under strace with
           --workdir DIR/wd, then audit. DIR must be empty or absent.
  --audit  --runner FILE --fleet ROOT --trace T --workdir W --stdout O --rc N
           audit an existing trace (public path of the selftest fixtures).
  --selftest   one fixture arm per check through the public --audit CLI.

Output: `WITNESS_FINDING <check> leg=<name> <detail>` per finding, `WITNESS_LEG <name>
ok|fail`, then `LEDGER_WITNESS: legs=<n> witnessed=<m> findings=<k> checks=<ids|-> PASS|FAIL`.
Exit 0 PASS, 1 FAIL, 2 setup (cannot audit). Known limits (not modelled, declared in
plans/round-89.plan.md): (L1) a process that edits the trace file, the kept workdir after
the run, or the witness itself (same uid); (L2) a MAP_SHARED write mapping of a mutant;
(L3) per-defect steering through process state the trace does not carry: the working
directory, the inherited fd table (e.g. a closed stdout), signal dispositions, or an
rlimit inherited from before the runner started; (L4) a forger that does all the real
work (that is not a counterfeit).
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

CHECKS = ("W_PARSE", "W_TABLE", "W_PATH", "W_DUP", "W_PIN", "W_SPEC", "W_RUN", "W_MAT",
          "W_CONTROL", "W_EXEC", "W_CONTENT", "W_ORDER", "W_VERDICT", "W_EXTRA", "W_ENV")
# Variables that let a process steer an interpreter without touching its argv (preload,
# startup files, exported functions, library injection). Present on any audited
# interpreter exec -> W_ENV.
ENV_DENY = ("NODE_OPTIONS", "NODE_PATH", "BASH_ENV", "ENV", "SHELLOPTS", "BASHOPTS",
            "PYTHONSTARTUP", "PYTHONPATH", "PYTHONHOME", "PYTHONINSPECT", "LD_PRELOAD",
            "LD_AUDIT", "LD_LIBRARY_PATH", "PROMPT_COMMAND")

LEG_RE = re.compile(
    r"^  regression_case_git (\S+) \\\n"
    r"\s+'([^']+)' \"\$(PIN_\w+)\" \"\$(REV_\w+)\" \\\n"
    r"\s+\"\$specs/([^\"]+)\.spec\" '([^']*)' \"\$(TABLE_\w+)\" \\\n"
    r"\s+\"\$root/([^\"]+)\"\n", re.M)
VAR_RE = re.compile(r"^((?:PIN|REV|TABLE)_\w+)=('?)([^'\n]*)\2$", re.M)
SPEC_RE = re.compile(r"^  cat >\"\$d/([^\"]+)\.spec\" <<'EOT'\n(.*?)^EOT$", re.M | re.S)
INTERP_RE = re.compile(r"\b(node|bash|python3)((?:\s+-I)?)\s+\"\$MUTANT\"((?:\s+--?[\w-]+)*)\s*$")
STRACE_FLAGS = ["-f", "-q", "-y", "-v", "-s", "4096", "-e", "signal=none", "-e",
                "trace=execve,execveat,openat,openat2,open,creat,rename,renameat,renameat2,"
                "link,linkat,symlink,symlinkat,truncate,ftruncate,write,pwrite64,writev,"
                "pwritev,pwritev2,fallocate,copy_file_range,sendfile,splice,setrlimit,prlimit64"]
WRITE_FD_CALLS = {"write", "pwrite64", "writev", "pwritev", "pwritev2", "ftruncate",
                  "fallocate"}
PATH_WRITE_CALLS = {"rename", "renameat", "renameat2", "link", "linkat", "symlink",
                    "symlinkat", "truncate", "creat"}
OPEN_CALLS = {"open", "openat", "openat2"}


# ------------------------------------------------------------------ spec parsing
def unescape_spec(s):
    out, i = [], 0
    table = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\"}
    while i < len(s):
        if s[i] == "\\":
            if i + 1 >= len(s) or s[i + 1] not in table:
                raise ValueError("bad escape")
            out.append(table[s[i + 1]])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def parse_spec(text):
    """Return [(id, old_bytes, new_bytes)] or raise ValueError. Independent of the
    runner's helper: same documented format (@defect ID | desc / @old / @new)."""
    defects, cur = [], None
    for line in text.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line == "@defect" or line.startswith("@defect "):
            did = line[len("@defect"):].strip().partition("|")[0].strip()
            if not did or not re.fullmatch(r"[A-Za-z0-9._-]+", did):
                raise ValueError("bad defect id")
            cur = {"id": did}
            defects.append(cur)
        elif line == "@old" or line.startswith("@old "):
            if cur is None or "old" in cur:
                raise ValueError("stray @old")
            cur["old"] = unescape_spec(line[5:] if line != "@old" else "")
        elif line == "@new" or line.startswith("@new "):
            if cur is None or "new" in cur:
                raise ValueError("stray @new")
            cur["new"] = unescape_spec(line[5:] if line != "@new" else "")
        else:
            raise ValueError("unrecognized spec line")
    ids = [d["id"] for d in defects]
    if not defects or len(ids) != len(set(ids)):
        raise ValueError("empty spec or duplicate id")
    for d in defects:
        if "old" not in d or "new" not in d or not d["old"] or d["old"] == d["new"]:
            raise ValueError("defect %s incomplete or no-op" % d["id"])
    return [(d["id"], d["old"].encode(), d["new"].encode()) for d in defects]


# ------------------------------------------------------------------ runner parsing
def parse_runner(text):
    """Return (legs, problems). Each leg: dict name, rel, pin, rev, spec_text, suite,
    interp, interp_flag, table(list of (id, verdict)), case."""
    vars_ = {m.group(1): m.group(3) for m in VAR_RE.finditer(text)}
    specs = {m.group(1): m.group(2) for m in SPEC_RE.finditer(text)}
    legs, problems = [], []
    for m in LEG_RE.finditer(text):
        name, rel, pinv, revv, specn, suite, tabv, case = m.groups()
        leg = {"name": name, "rel": rel, "suite": suite, "case": case}
        for key, var in (("pin", pinv), ("rev", revv), ("table_raw", tabv)):
            if var not in vars_:
                problems.append(("W_PARSE", name, "unresolved %s" % var))
            leg[key] = vars_.get(var)
        leg["spec_text"] = specs.get(specn)
        if leg["spec_text"] is None:
            problems.append(("W_PARSE", name, "no embedded spec %s" % specn))
        im = list(INTERP_RE.finditer(suite))
        if not im:
            problems.append(("W_PARSE", name, "suite names no interpreter for \"$MUTANT\""))
            leg["interp"] = None
        else:
            leg["interp"], leg["interp_flag"] = im[-1].group(1), im[-1].group(2).strip()
            leg["tail"] = im[-1].group(3).split()
        table = []
        for pair in (leg.get("table_raw") or "").split(","):
            if pair:
                did, _, v = pair.partition(":")
                table.append((did, v))
        leg["table"] = table
        legs.append(leg)
    if not legs:
        problems.append(("W_PARSE", "-", "no ledger leg declared"))
    return legs, problems


# ------------------------------------------------------------------ strace parsing
def c_unescape(s):
    out = bytearray()
    i = 0
    simple = {"n": 10, "t": 9, "r": 13, "v": 11, "f": 12, "\\": 92, '"': 34, "a": 7, "b": 8}
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n in simple:
                out.append(simple[n])
                i += 2
            elif n == "x":
                out.append(int(s[i + 2:i + 4], 16))
                i += 4
            elif n in "01234567":
                j = i + 1
                while j < len(s) and j < i + 4 and s[j] in "01234567":
                    j += 1
                out.append(int(s[i + 1:j], 8) & 0xFF)
                i = j
            else:
                out.append(ord(n))
                i += 2
        else:
            out.extend(c.encode("utf-8"))
            i += 1
    return out.decode("utf-8", "surrogateescape")


STR_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


def _str_array(args, i):
    """Parse `["a", "b", ...]` starting at args[i] == '['; return (list, end) or (None, i)."""
    if not args.startswith("[", i):
        return None, i
    i += 1
    out = []
    while i < len(args):
        if args[i] == "]":
            return out, i + 1
        if args.startswith(", ", i):
            i += 2
            continue
        if args.startswith("...", i):
            i += 3
            continue
        sm = STR_RE.match(args, i)
        if not sm:
            return None, i
        out.append(c_unescape(sm.group(1)))
        i = sm.end()
    return None, i


def exec_strings(args):
    """Tokenize `"file", ["a0", ...], ["K=V", ...]|0x.. /* n vars */` (execveat: a dirfd
    first): return ([file, a0, a1, ...], env list or None) honouring quotes and escapes."""
    m = STR_RE.search(args)
    if not m:
        return [], None
    out = [c_unescape(m.group(1))]
    i = m.end()
    if not args.startswith(", ", i):
        return out, None
    argv, i = _str_array(args, i + 2)
    if argv is None:
        return out, None
    env = None
    if args.startswith(", ", i):
        env, _ = _str_array(args, i + 2)
    return out + argv, env


LINE_RE = re.compile(r"^(\d+) +(.*)$")
CALL_RE = re.compile(r"^([a-z0-9_]+)\((.*)$", re.S)
EXIT_RE = re.compile(r"^\+\+\+ (exited with (\d+)|killed by (\S+)).*\+\+\+$")
FDPATH_RE = re.compile(r"^\d+<([^>]*)>")


def parse_trace(path):
    """Yield events in file order: (idx, pid, kind, data).
    kind 'exec': data=(filename, argv); 'exit': data=('code', n)|('signal', name);
    'write': data=[paths] (paths a write-class syscall touches)."""
    pending = {}
    events = []
    with open(path, encoding="utf-8", errors="surrogateescape") as fh:
        for raw in fh:
            raw = raw.rstrip("\n")
            m = LINE_RE.match(raw)
            if not m:
                continue
            pid, body = int(m.group(1)), m.group(2)
            if body.endswith("<unfinished ...>"):
                pending[pid] = body[: -len("<unfinished ...>")]
                continue
            rm = re.match(r"^<\.\.\. ([a-z0-9_]+) resumed>(.*)$", body)
            if rm:
                body = pending.pop(pid, rm.group(1) + "(") + rm.group(2)
            em = EXIT_RE.match(body)
            if em:
                if em.group(2) is not None:
                    events.append((len(events), pid, "exit", ("code", int(em.group(2)))))
                else:
                    events.append((len(events), pid, "exit", ("signal", em.group(3))))
                continue
            cm = CALL_RE.match(body)
            if not cm:
                continue
            call, rest = cm.group(1), cm.group(2)
            res = rest.rsplit(" = ", 1)
            if len(res) != 2:
                continue
            args, result = res
            if result.startswith("-1") or result.startswith("?"):
                continue
            if call in ("execve", "execveat"):
                strs, env = exec_strings(args)
                if not strs:
                    continue
                events.append((len(events), pid, "exec", (strs[0], strs[1:], env)))
            elif call in ("setrlimit", "prlimit64"):
                parts = [x.strip() for x in args.split(", ")]
                setting = (call == "setrlimit") or (len(parts) >= 3 and parts[2] != "NULL")
                if setting:
                    events.append((len(events), pid, "rlimit", args[:120]))
            elif call in OPEN_CALLS:
                flags = args
                if re.search(r"O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND", flags):
                    paths = anchored_paths(args)
                    fm = re.search(r"<([^>]*)>\s*$", result)
                    if fm:
                        paths.append(os.path.normpath(c_unescape(fm.group(1))))
                    events.append((len(events), pid, "write", paths))
            elif call in PATH_WRITE_CALLS:
                events.append((len(events), pid, "write", anchored_paths(args)))
            elif call in WRITE_FD_CALLS or call in ("copy_file_range", "sendfile", "splice"):
                fds = re.findall(r"(?:^|, )\d+<([^>]*)>", args)
                if call in ("copy_file_range", "splice") and len(fds) >= 2:
                    fds = fds[1:2]
                elif call == "sendfile" and fds:
                    fds = fds[0:1]
                elif fds:
                    fds = fds[0:1]
                events.append((len(events), pid, "write", [os.path.normpath(c_unescape(x)) for x in fds]))
    return events


DIRSTR_RE = re.compile(r'(?:(?:AT_FDCWD|-?\d+)<([^>]*)>, )?"((?:[^"\\]|\\.)*)"')


def anchored_paths(args):
    """Absolute, normalized paths for each path string in a path syscall: absolute
    strings as given, relative ones joined to their `-y`-decoded dirfd; a relative
    string with no decoded anchor stays `REL:<string>` (matched by basename)."""
    out = []
    for m in DIRSTR_RE.finditer(args):
        s = c_unescape(m.group(2))
        if s.startswith("/"):
            out.append(os.path.normpath(s))
        elif m.group(1) is not None:
            out.append(os.path.normpath(os.path.join(c_unescape(m.group(1)), s)))
        else:
            out.append("REL:" + s)
    return out


# ------------------------------------------------------------------ helpers
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    try:
        with open(p, "rb") as fh:
            return sha256_bytes(fh.read())
    except OSError:
        return None


def git_blob(repo, rev, path):
    """Return blob bytes, or (None, reason). Repo must be its own toplevel."""
    if not os.path.isdir(repo):
        return None, "repo dir missing"
    try:
        top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, "git unavailable: %s" % e
    if top.returncode != 0 or os.path.realpath(top.stdout.strip()) != os.path.realpath(repo):
        return None, "repo is not its own toplevel"
    r = subprocess.run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (rev, path)],
                       capture_output=True, timeout=60)
    if r.returncode != 0:
        return None, "cat-file failed"
    return r.stdout, None


def path_ok(rel):
    if rel.startswith("/") or "//" in rel:
        return False
    parts = rel.split("/")
    if len(parts) < 2:
        return False
    return all(p not in ("", ".", "..") for p in parts) and re.fullmatch(r"[A-Za-z0-9._-]+", parts[0]) is not None


def interp_match(filename, argv, interp, flag, target, tail):
    """True when this exec is the leg's declared interpreter (same file as the one the
    witness's PATH resolves) running `target` as its script with the suite's exact argv."""
    base = os.path.basename(filename)
    if not (base == interp or (interp == "python3" and re.fullmatch(r"python3(\.\d+)?", base))):
        return False
    want = shutil.which(interp)
    if want is None or os.path.realpath(filename) != os.path.realpath(want):
        return False
    expect = ([flag] if flag else []) + [target] + list(tail)
    return list(argv[1:]) == expect


# ------------------------------------------------------------------ audit
def audit(runner_text, fleet, trace, workdir, stdout_text, rc):
    findings = []

    def f(check, leg, detail):
        findings.append((check, leg, detail))

    legs, problems = parse_runner(runner_text)
    for p in problems:
        f(*p)
    try:
        events = parse_trace(trace)
    except OSError as e:
        return None, "cannot read trace: %s" % e
    workdir = os.path.realpath(workdir)

    # W_RUN
    case_pass = re.findall(r"^REGRESSION_CASE (\S+): (\S+)", stdout_text, re.M)
    names = [l["name"] for l in legs]
    passed = [n for n, v in case_pass if v == "PASS"]
    other = [n for n, v in case_pass if v != "PASS"]
    summ = re.search(r"^REGRESSION: PASS \(cases=(\d+) passed=(\d+)[;)]", stdout_text, re.M)
    if rc != 0:
        f("W_RUN", "-", "runner exit %s" % rc)
    if not summ or int(summ.group(1)) != len(legs) or int(summ.group(2)) != len(legs):
        f("W_RUN", "-", "summary is not PASS(cases=%d passed=%d)" % (len(legs), len(legs)))
    if sorted(passed) != sorted(set(names)) or len(passed) != len(names) or other:
        f("W_RUN", "-", "per-leg PASS lines %d for %d legs (non-PASS %d)" % (len(passed), len(names), len(other)))

    # W_DUP (names, (repo,path), pins)
    seen_name, seen_rp, seen_pin = {}, {}, {}
    for l in legs:
        for key, store in ((l["name"], seen_name), (l["rel"], seen_rp), (l.get("pin"), seen_pin)):
            if key in store:
                f("W_DUP", l["name"], "duplicates leg %s" % store[key])
            else:
                store[key] = l["name"]

    expected_paths = {}
    leg_state = {}
    for l in legs:
        name = l["name"]
        st = {"ok_path": True, "blob": None, "defects": []}
        leg_state[name] = st
        bad_table = [(d, v) for d, v in l["table"] if v not in ("KILLED", "SURVIVED")]
        for d, v in bad_table:
            f("W_TABLE", name, "defect %s recorded %r" % (d, v))
        st["bad_ids"] = {d for d, _ in bad_table}
        if not path_ok(l["rel"]):
            f("W_PATH", name, "leg path %r" % l["rel"])
            st["ok_path"] = False
            continue
        if not l.get("pin") or not l.get("rev") or l.get("spec_text") is None or not l.get("interp"):
            continue
        repo_dir, path = l["rel"].split("/", 1)
        blob, why = git_blob(os.path.join(fleet, repo_dir), l["rev"], path)
        if blob is None:
            f("W_PIN", name, why)
            continue
        st["blob"] = blob
        if sha256_bytes(blob) != l["pin"]:
            f("W_PIN", name, "blob sha256 %s != PIN %s" % (sha256_bytes(blob)[:12], l["pin"][:12]))
        try:
            spec = parse_spec(l["spec_text"])
        except ValueError as e:
            f("W_SPEC", name, "spec: %s" % e)
            continue
        if [d for d, _, _ in spec] != [d for d, _ in l["table"]]:
            f("W_SPEC", name, "spec ids != table ids")
        verdict_of = dict(l["table"])
        base = "target." + os.path.basename(path)
        cdir = os.path.join(workdir, l["case"])
        prist = os.path.join(cdir, "pristine." + base)
        expected_paths[prist] = (name, "pristine", None)
        for did, old, new in spec:
            if blob.count(old) != 1:
                f("W_SPEC", name, "defect %s old-count=%d" % (did, blob.count(old)))
                exp = None
            else:
                exp = sha256_bytes(blob.replace(old, new, 1))
            mp = os.path.join(cdir, "mutant-%s.%s" % (did, base))
            expected_paths[mp] = (name, "mutant", did)
            st["defects"].append((did, mp, exp, verdict_of.get(did)))
        st["prist"] = prist
        # W_MAT
        want = "%s:%s" % (l["rev"], path)
        if not any(k == "exec" and os.path.basename(d[0]) == "git" and "show" in d[1] and want in d[1]
                   for _, _, k, d in events):
            f("W_MAT", name, "no `git show %s` exec observed" % want)

    # exec index: first interpreter exec per expected path; exit per pid after it
    first_exec = {}
    exec_env = {}
    interp_of = {l["name"]: (l.get("interp"), l.get("interp_flag", ""), l.get("tail", []))
                 for l in legs}
    exits = {}
    for idx, pid, kind, data in events:
        if kind == "exit":
            exits.setdefault(pid, []).append((idx, data))
    unaudited_cases = {l["case"] for l in legs if not leg_state[l["name"]].get("prist")}
    for idx, pid, kind, data in events:
        if kind != "exec":
            continue
        fn, argv, env = data
        if os.path.basename(fn).split(".")[0] not in ("node", "bash", "python3"):
            continue
        rest = [a for a in argv[1:] if a != "-I"]
        if not rest:
            continue
        tgt = rest[0]
        if tgt in expected_paths and tgt not in first_exec:
            ip, fl, tail = interp_of[expected_paths[tgt][0]]
            if ip and interp_match(fn, argv, ip, fl, tgt, tail):
                first_exec[tgt] = (idx, pid)
                exec_env[tgt] = env
        # W_EXTRA: an interpreter exec of a mutant/pristine-shaped path under workdir
        if tgt.startswith(workdir + "/") and re.match(r"^(mutant-[^/]+|pristine)\.target\.", os.path.basename(tgt)):
            case_dir = os.path.relpath(tgt, workdir).split("/", 1)[0]
            if tgt not in expected_paths and not (case_dir in unaudited_cases and "/" in os.path.relpath(tgt, workdir)):
                f("W_EXTRA", "-", "undeclared interpreter exec of %s" % os.path.relpath(tgt, workdir))

    # W_ENV: no steering variable on an audited exec; each mutant's exec environment
    # equals its leg's control environment once the per-run tokens (defect id, the
    # file under test) are normalized; no rlimit is set outside an audited interpreter.
    def norm_env(env, did, path):
        """MUTANT must name the file under test and DEFECT_ID the run's id; elsewhere the
        id is normalized only as a path-component token (the suites' sandbox-<id> dirs)."""
        if env is None:
            return None
        out = {}
        tok = re.compile(r"(?<=[-/_])%s(?=/|$)" % re.escape(did))
        for kv in env:
            k, _, v = kv.partition("=")
            if k == "MUTANT" and v == path:
                v = "<FILE>"
            elif k == "DEFECT_ID" and v == did:
                v = "<ID>"
            else:
                v = tok.sub("<ID>", v)
            out[k] = v
        return out
    for l in legs:
        st = leg_state[l["name"]]
        if not st.get("prist") or st["prist"] not in first_exec:
            continue
        cenv = norm_env(exec_env.get(st["prist"]), "CONTROL", st["prist"])
        runs = [(st["prist"], "CONTROL")] + [(mp, did) for did, mp, _, _ in st["defects"]]
        for path, did in runs:
            if path not in first_exec:
                continue
            raw = exec_env.get(path) or []
            bad = sorted({kv.partition("=")[0] for kv in raw
                          if kv.partition("=")[0] in ENV_DENY or kv.startswith("BASH_FUNC_")})
            if bad:
                f("W_ENV", l["name"], "%s exec carries %s" % (did, ",".join(bad)))
            if did != "CONTROL" and cenv is not None and norm_env(exec_env.get(path), did, path) != cenv:
                f("W_ENV", l["name"], "defect %s exec environment differs from the control's" % did)
    audited_pids = {pid: idx for idx, pid in first_exec.values()}
    for idx, pid, kind, data in events:
        if kind == "rlimit" and not (pid in audited_pids and idx > audited_pids[pid]):
            f("W_ENV", "-", "rlimit set outside an audited interpreter: pid %d %s" % (pid, data))

    def exit_after(pid, idx):
        for eidx, data in exits.get(pid, []):
            if eidx > idx:
                return data
        return None

    # W_ORDER: exact absolute path; an unanchored relative path falls back to basename
    # against every audited file (conservative: any same-named file counts).
    exec_idx_by_path = {os.path.normpath(p): ei for p, (ei, _) in first_exec.items()}
    reported = set()
    for idx, pid, kind, data in events:
        if kind != "write":
            continue
        for p in data:
            if p.startswith("REL:"):
                b = os.path.basename(p[4:])
                hits = [q for q in exec_idx_by_path if os.path.basename(q) == b]
            else:
                hits = [p] if p in exec_idx_by_path else []
            for q in hits:
                if idx > exec_idx_by_path[q] and q not in reported:
                    reported.add(q)
                    f("W_ORDER", expected_paths[q][0],
                      "write-class syscall on %s after its exec" % os.path.basename(q))

    witnessed = 0
    for l in legs:
        name = l["name"]
        st = leg_state[name]
        before = len([x for x in findings if x[1] == name])
        if st["ok_path"] and st.get("prist"):
            # W_CONTROL
            fe = first_exec.get(st["prist"])
            if fe is None:
                f("W_CONTROL", name, "pristine never exec'd by %s" % l["interp"])
            else:
                ex = exit_after(fe[1], fe[0])
                if ex != ("code", 0):
                    f("W_CONTROL", name, "pristine exit %s" % (ex,))
            if st["blob"] is not None and sha256_file(st["prist"]) != sha256_bytes(st["blob"]):
                f("W_CONTROL", name, "pristine bytes != pinned blob")
            for did, mp, exp, rec in st["defects"]:
                fe = first_exec.get(mp)
                if fe is None:
                    f("W_EXEC", name, "defect %s mutant never exec'd by %s" % (did, l["interp"]))
                if exp is not None:
                    got = sha256_file(mp)
                    if got != exp:
                        f("W_CONTENT", name, "defect %s mutant sha256 %s != expected %s" % (
                            did, (got or "missing")[:12], exp[:12]))
                if fe is not None and did not in st["bad_ids"] and rec is not None:
                    ex = exit_after(fe[1], fe[0])
                    if ex is None:
                        obs = "INCONCLUSIVE"
                    elif ex[0] == "signal":
                        obs = "INCONCLUSIVE"
                    elif ex[1] == 0:
                        obs = "SURVIVED"
                    elif ex[1] in (124, 126, 127):
                        obs = "INCONCLUSIVE"
                    else:
                        obs = "KILLED"
                    if obs != rec:
                        f("W_VERDICT", name, "defect %s observed %s recorded %s" % (did, obs, rec))
        if len([x for x in findings if x[1] == name]) == before and st["ok_path"] and st.get("prist"):
            witnessed += 1
    return (legs, witnessed, findings), None


def report(result):
    legs, witnessed, findings = result
    for check, leg, detail in findings:
        print("WITNESS_FINDING %s leg=%s %s" % (check, leg, detail))
    bad = {leg for _, leg, _ in findings}
    for l in legs:
        print("WITNESS_LEG %s %s" % (l["name"], "fail" if l["name"] in bad else "ok"))
    checks = sorted({c for c, _, _ in findings}, key=CHECKS.index)
    ok = not findings and witnessed == len(legs) and len(legs) > 0
    print("LEDGER_WITNESS: legs=%d witnessed=%d findings=%d checks=%s %s" % (
        len(legs), witnessed, len(findings), ",".join(checks) or "-", "PASS" if ok else "FAIL"))
    return 0 if ok else 1


def arg(argv, name, default=None):
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return default


def setup(msg):
    print("LEDGER_WITNESS: SETUP (%s)" % msg)
    return 2


def main_audit(argv):
    need = ["--runner", "--fleet", "--trace", "--workdir", "--stdout", "--rc"]
    vals = {k: arg(argv, k) for k in need}
    if any(v is None for v in vals.values()):
        return setup("--audit needs %s" % " ".join(need))
    try:
        runner = open(vals["--runner"], encoding="utf-8").read()
        out = open(vals["--stdout"], encoding="utf-8", errors="replace").read()
        rc = int(vals["--rc"])
    except (OSError, ValueError) as e:
        return setup(str(e))
    if not os.path.isfile(vals["--trace"]):
        return setup("trace missing")
    res, err = audit(runner, vals["--fleet"], vals["--trace"], vals["--workdir"], out, rc)
    if err:
        return setup(err)
    return report(res)


def main_run(argv):
    runner, fleet, scratch = arg(argv, "--runner"), arg(argv, "--fleet"), arg(argv, "--scratch")
    lane = arg(argv, "--lane", "tameshi-shokunin")
    if not (runner and fleet and scratch):
        return setup("--run needs --runner --fleet --scratch")
    if shutil.which("strace") is None:
        return setup("strace missing")
    if os.path.exists(scratch) and os.listdir(scratch):
        return setup("scratch not empty: %s" % scratch)
    try:
        text = open(runner, encoding="utf-8").read()
    except OSError as e:
        return setup(str(e))
    scratch = os.path.realpath(scratch)
    os.makedirs(os.path.join(scratch, "fleet", lane, "tools"), exist_ok=True)
    os.makedirs(os.path.join(scratch, "tmp"), exist_ok=True)
    shadow = os.path.join(scratch, "fleet", lane, "tools", "mutate-and-run.sh")
    shutil.copyfile(runner, shadow)
    legs, _ = parse_runner(text)
    repos = set()
    for l in legs:
        first = l["rel"].split("/", 1)[0]
        if path_ok(l["rel"]):
            repos.add(first)
    for r in sorted(repos):
        link = os.path.join(scratch, "fleet", r)
        if not os.path.exists(link):
            os.symlink(os.path.join(os.path.realpath(fleet), r), link)
    wd = os.path.join(scratch, "wd")
    trace = os.path.join(scratch, "trace.txt")
    outp = os.path.join(scratch, "runner.out")
    # A clean, declared starting environment: any steering variable an audited exec
    # carries was introduced by the runner itself (W_ENV), never inherited.
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/"),
           "LC_ALL": "C.UTF-8", "TMPDIR": os.path.join(scratch, "tmp")}
    with open(outp, "wb") as fh:
        p = subprocess.run(["strace"] + STRACE_FLAGS + ["-o", trace, "bash", shadow,
                                                        "--regression", "--workdir", wd],
                           stdout=fh, stderr=subprocess.STDOUT, env=env)
    print("WITNESS_RUN: runner_sha256=%s rc=%d trace=%s" % (sha256_file(runner), p.returncode, trace))
    out = open(outp, encoding="utf-8", errors="replace").read()
    res, err = audit(text, os.path.join(scratch, "fleet"), trace, wd, out, p.returncode)
    if err:
        return setup(err)
    return report(res)


# ------------------------------------------------------------------ selftest
FIX_RUNNER = """\
PIN_A=%(pa)s
REV_A=%(ra)s
TABLE_A='%(ta)s'
PIN_B=%(pb)s
REV_B=%(rb)s
TABLE_B='B1:SURVIVED'
regression_specs() {
  local d=$1
  cat >"$d/leg-a.spec" <<'EOT'
%(sa)s
EOT
  cat >"$d/leg-b.spec" <<'EOT'
@defect B1 | b
@old echo b
@new echo B
EOT
}
run_regression() {
  regression_case_git leg-a \\
    '%(pathA)s' "$PIN_A" "$REV_A" \\
    "$specs/leg-a.spec" 'bash "$MUTANT" --selftest' "$TABLE_A" \\
    "$root/leg-a"
  regression_case_git leg-b \\
    'repob/b.sh' "$PIN_B" "$REV_B" \\
    "$specs/leg-b.spec" 'bash "$MUTANT" --selftest' "$TABLE_B" \\
    "$root/leg-b"
}
"""
SPEC_A = "@defect A1 | a1\n@old exit 0\n@new exit 1\n\n@defect A2 | a2\n@old echo a\n@new echo A"


def build_fixture(root, arm):
    """Materialize a two-leg fixture under root; return audit argv. One perturbation
    per arm; every other check stays satisfied."""
    fleet = os.path.join(root, "fleet")
    wd = os.path.join(root, "wd")
    blobs = {"repoa": ("a.sh", b"echo a\necho b\nexit 0\n"), "repob": ("b.sh", b"echo b\n")}
    if arm == "W_DUP":
        blobs["repob"] = ("b.sh", b"echo a\necho b\nexit 0\n")
    revs = {}
    for repo, (fn, data) in blobs.items():
        d = os.path.join(fleet, repo)
        os.makedirs(d)
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True,
                             text=True, check=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d)
        with open(os.path.join(d, fn), "wb") as fh:
            fh.write(data)
        subprocess.run(["git", "-C", d, "add", fn], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=fx", "-c", "user.email=fx@fx.invalid",
                        "commit", "-q", "-m", "fx"], check=True)
        revs[repo] = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True,
                                    text=True, check=True).stdout.strip()
    ba, bb = blobs["repoa"][1], blobs["repob"][1]
    spec_a = SPEC_A
    table_a = "A1:KILLED,A2:SURVIVED"
    if arm == "W_TABLE":
        table_a = "A1:KILLED,A2:MAYBE"
    if arm == "W_SPEC":
        spec_a = SPEC_A.replace("@old echo a", "@old echo zz")
    pin_a = sha256_bytes(ba)
    if arm == "W_PIN":
        pin_a = "0" * 64
    if arm == "W_PARSE":
        pin_a = None
    path_a = "repoa/a.sh" if arm != "W_PATH" else "repoa/./a.sh"
    runner = FIX_RUNNER % {"pa": pin_a or "x", "ra": revs["repoa"], "ta": table_a,
                           "pb": sha256_bytes(bb), "rb": revs["repob"], "sa": spec_a, "pathA": path_a}
    if arm == "W_PARSE":
        runner = runner.replace("PIN_A=x\n", "")
    os.makedirs(wd)
    lines, pid = [], [100]

    def nextpid():
        pid[0] += 1
        return pid[0]

    def q(s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

    bash = shutil.which("bash")

    def execl(p, fn, argv, env=None):
        envs = "0x7ffd /* 3 vars */" if env is None else "[%s]" % ", ".join(q(e) for e in env)
        lines.append("%d execve(%s, [%s], %s) = 0" % (p, q(fn), ", ".join(q(a) for a in argv), envs))

    def ienv(path, did, extra=()):
        return ["PATH=/usr/bin:/bin", "MUTANT=%s" % path, "DEFECT_ID=%s" % did] + list(extra)

    legs = [("leg-a", "repoa", "a.sh", ba, [("A1", b"exit 0", b"exit 1", 1), ("A2", b"echo a", b"echo A", 0)]),
            ("leg-b", "repob", "b.sh", bb, [("B1", b"echo b", b"echo B", 0)])]
    out = []
    for name, repo, fn, blob, defs in legs:
        cdir = os.path.join(wd, name)
        os.makedirs(cdir)
        base = "target." + fn
        p = nextpid()
        if not (arm == "W_MAT" and name == "leg-a"):
            execl(p, "/usr/bin/git", ["git", "-C", os.path.join(fleet, repo), "show", "%s:%s" % (revs[repo], fn)])
        lines.append("%d +++ exited with 0 +++" % p)
        prist = os.path.join(cdir, "pristine." + base)
        with open(prist, "wb") as fh:
            fh.write(blob)
        lines.append('%d openat(AT_FDCWD</x>, %s, O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3<%s>' % (nextpid(), q(prist), prist))
        p = nextpid()
        if not (arm == "W_CONTROL" and name == "leg-b"):
            execl(p, bash, ["bash", prist, "--selftest"], ienv(prist, "CONTROL"))
        lines.append("%d +++ exited with 0 +++" % p)
        for did, old, new, code in defs:
            mp = os.path.join(cdir, "mutant-%s.%s" % (did, base))
            data = blob.replace(old, new, 1) if blob.count(old) == 1 else blob
            if arm == "W_CONTENT" and did == "B1":
                data = blob
            with open(mp, "wb") as fh:
                fh.write(data)
            wp = nextpid()
            lines.append('%d openat(AT_FDCWD</x>, %s, O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3<%s>' % (wp, q(mp), mp))
            lines.append('%d write(3<%s>, "x", 1) = 1' % (wp, mp))
            p = nextpid()
            argv, fn_ = ["bash", mp, "--selftest"], bash
            extra = ()
            if arm == "W_EXEC:argv" and did == "A2":
                argv = ["bash", mp, "--bogus"]
            if arm == "W_EXEC:interp" and did == "A2":
                fn_ = os.path.join(root, "fakebin", "bash")
            if arm == "W_ENV" and did == "A1":
                extra = ("BASH_ENV=/dev/null",)
            if arm == "W_ENV:diff" and did == "A1":
                extra = ("HOME=/elsewhere",)
            if arm == "W_ENV:rlimit" and did == "A1":
                lines.append("%d prlimit64(0, RLIMIT_AS, {rlim_cur=1024, rlim_max=1024}, NULL) = 0" % p)
            if not (arm == "W_EXEC" and did == "A2"):
                execl(p, fn_, argv, ienv(mp, did, extra))
            if arm == "W_VERDICT" and did == "A1":
                code = 0
            lines.append("%d +++ exited with %d +++" % (p, code))
            if arm == "W_ORDER" and did == "A1":
                lines.append('%d write(3<%s>, "y", 1) = 1' % (wp, mp))
        out.append("REGRESSION_CASE %s: PASS (band: exact)" % name)
    if arm == "W_EXTRA":
        ghost = os.path.join(wd, "leg-z", "mutant-Z1.target.z.sh")
        execl(nextpid(), bash, ["bash", ghost, "--selftest"])
    if arm != "W_RUN":
        out.append("REGRESSION: PASS (cases=2 passed=2; ledger legs exact)")
    for fname, content in (("runner.sh", runner), ("trace.txt", "\n".join(lines) + "\n"),
                           ("stdout.txt", "\n".join(out) + "\n")):
        with open(os.path.join(root, fname), "w", encoding="utf-8") as fh:
            fh.write(content)
    return ["--audit", "--runner", os.path.join(root, "runner.sh"), "--fleet", fleet,
            "--trace", os.path.join(root, "trace.txt"), "--workdir", wd,
            "--stdout", os.path.join(root, "stdout.txt"), "--rc", "0"]


def selftest():
    base = os.environ.get("TMPDIR") or tempfile.gettempdir()
    tmp = tempfile.mkdtemp(prefix="ledger-witness-selftest.", dir=base)
    arms = (["BASE"] + list(CHECKS) + ["W_EXEC:argv", "W_EXEC:interp", "W_ENV:diff",
                                       "W_ENV:rlimit", "SETUP"])
    passed = 0
    try:
        for arm in arms:
            root = os.path.join(tmp, arm)
            os.makedirs(root)
            av = build_fixture(root, "BASE" if arm == "SETUP" else arm)
            if arm == "SETUP":
                os.remove(os.path.join(root, "trace.txt"))
            p = subprocess.run([sys.executable, "-I", os.path.abspath(__file__)] + av,
                               capture_output=True, text=True, env=dict(os.environ, TMPDIR=tmp))
            fired = set(re.findall(r"^WITNESS_FINDING (\S+)", p.stdout, re.M))
            if arm == "BASE":
                ok = p.returncode == 0 and not fired and "legs=2 witnessed=2" in p.stdout
            elif arm == "SETUP":
                ok = p.returncode == 2 and "SETUP" in p.stdout
            else:
                ok = p.returncode == 1 and fired == {arm.split(":")[0]}
            passed += ok
            print("SELFTEST_ARM %s rc=%d fired=%s %s" % (arm, p.returncode, ",".join(sorted(fired)) or "-",
                                                        "ok" if ok else "FAIL"))
            if not ok:
                sys.stdout.write(p.stdout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("LEDGER_WITNESS_SELFTEST: %d/%d pass" % (passed, len(arms)))
    return 0 if passed == len(arms) else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--audit" in argv:
        return main_audit(argv)
    if "--run" in argv:
        return main_run(argv)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
