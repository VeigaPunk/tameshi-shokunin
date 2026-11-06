#!/usr/bin/env python3
"""T89C2 — crafted-input probes for the trace parser of tools/ledger-witness.py (frozen).

Builds a two-leg fixture (real git repos + workdir) in the round-89 selftest shape and
perturbs ONE trace feature per case; every case goes through the PUBLIC `--audit` CLI.

Rendering is strace-faithful, measured on this host (strace 6.x, `-f -q -y -v -s 4096`):
  * quoted strings: `\\` and `"` C-escaped, `<`/`>` raw, newline `\\n`;
  * `-y` fd annotations: `\\`, `"`, `<`, `>`, newline escaped -- `>` is `\\076`, `<` `\\074`
    (minimal-but-unambiguous octal, so `g>123` prints `g\\076123`);
  * a string longer than -s prints `"<first 4096 chars>"...`;
  * a syscall that is still running prints `execve(...) <unfinished ...>` and is closed by
    `<... execve resumed>)            = 0` (result padding included);
  * `write` on an fd whose inode moved is annotated with the path *at print time*
    (verified: rename of an ancestor directory changes the annotation).

    python3 -I T89C2-driver.py            # build under scratch, audit, save fixtures
    python3 -I T89C2-driver.py --only C6  # one case
    python3 -I T89C2-driver.py --replay   # re-audit the saved fixtures from their bytes

Fixture text (runner.sh / trace.txt / stdout.txt, KiB each) is copied to
T89C2-fixtures/<case>/; the wd tree and the two git repos are rebuilt deterministically.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

WITNESS = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/ledger-witness.py"
HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "T89C2-fixtures")
SCRATCH = "/fast/scratch/hyaku/tameshi-r89/T89C2/cases"

SPEC_A = "@defect A1 | a1\n@old exit 0\n@new exit 1\n\n@defect A2 | a2\n@old echo a\n@new echo A"
SPEC_B = "@defect B1 | b\n@old echo b\n@new echo B"
BLOB_A = b"echo a\necho b\nexit 0\n"
BLOB_B = b"echo b\n"

RUNNER = """\
PIN_A={pa}
REV_A={ra}
TABLE_A='{ta}'
PIN_B={pb}
REV_B={rb}
TABLE_B='B1:SURVIVED'
regression_specs() {{
  local d=$1
  cat >"$d/leg-a.spec" <<'EOT'
{sa}
EOT
  cat >"$d/leg-b.spec" <<'EOT'
{sb}
EOT
}}
run_regression() {{
  regression_case_git leg-a \\
    'repoa/a.sh' "$PIN_A" "$REV_A" \\
    "$specs/leg-a.spec" 'bash "$MUTANT" --selftest' "$TABLE_A" \\
    "$root/{ca}"
  regression_case_git leg-b \\
    'repob/b.sh' "$PIN_B" "$REV_B" \\
    "$specs/leg-b.spec" 'bash "$MUTANT" --selftest' "$TABLE_B" \\
    "$root/{cb}"
}}
"""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def q(s):
    """strace's quoted-string rendering."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def ann(s):
    """strace's `-y` fd-annotation rendering (inside <...>)."""
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == ">":
            out.append("\\076")
        elif ch == "<":
            out.append("\\074")
        elif ch == "\n":
            out.append("\\n")
        else:
            out.append(ch)
    return "".join(out)


# ---------------------------------------------------------------- materialize
def materialize(caseid, wdname="wd", ca="leg-a", cb="leg-b", link_a=False, precreate=True):
    root = os.path.join(SCRATCH, caseid)
    if os.path.exists(root):
        shutil.rmtree(root)
    fleet = os.path.join(root, "fleet")
    wd = os.path.join(root, wdname)
    blobs = {"repoa": ("a.sh", BLOB_A), "repob": ("b.sh", BLOB_B)}
    revs = {}
    for repo, (fn, data) in blobs.items():
        d = os.path.join(fleet, repo)
        os.makedirs(d)
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), (top, d)
        with open(os.path.join(d, fn), "wb") as fh:
            fh.write(data)
        subprocess.run(["git", "-C", d, "add", fn], check=True)
        cenv = dict(os.environ, GIT_AUTHOR_DATE="2000-01-01T00:00:00 +0000",
                    GIT_COMMITTER_DATE="2000-01-01T00:00:00 +0000")
        subprocess.run(["git", "-C", d, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
                        "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fx"],
                       check=True, env=cenv)
        revs[repo] = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                                    capture_output=True, text=True, check=True).stdout.strip()
    runner = RUNNER.format(pa=sha(BLOB_A), ra=revs["repoa"], ta="A1:KILLED,A2:SURVIVED",
                           pb=sha(BLOB_B), rb=revs["repob"], sa=SPEC_A, sb=SPEC_B, ca=ca, cb=cb)
    os.makedirs(wd)
    ctx = {"root": root, "fleet": fleet, "wd": wd, "revs": revs, "ca": ca, "cb": cb,
           "bash": shutil.which("bash"), "real": {}}
    with open(os.path.join(root, "runner.sh"), "w", encoding="utf-8") as fh:
        fh.write(runner)
    defs = {"leg-a": [("A1", b"exit 0", b"exit 1"), ("A2", b"echo a", b"echo A")],
            "leg-b": [("B1", b"echo b", b"echo B")]}
    ctx["paths"] = {}
    for case, name, fn, blob in ((ca, "leg-a", "a.sh", BLOB_A), (cb, "leg-b", "b.sh", BLOB_B)):
        if link_a and name == "leg-a":
            real = os.path.join(root, "prep", "leg-a")
            os.makedirs(real)
            os.symlink(real, os.path.join(wd, case))
            ctx["real"][name] = real
            cdir, stored = real, os.path.join(wd, case)
        else:
            cdir, stored = os.path.join(wd, case), os.path.join(wd, case)
            if precreate:
                os.makedirs(cdir)
        if not precreate:
            ctx["paths"][name] = {"prist": os.path.join(stored, "pristine.target." + fn),
                                  "stored": stored}
            for did, old, new in defs[name]:
                ctx["paths"][name][did] = os.path.join(stored, "mutant-%s.target.%s" % (did, fn))
            continue
        with open(os.path.join(cdir, "pristine.target." + fn), "wb") as fh:
            fh.write(blob)
        for did, old, new in defs[name]:
            with open(os.path.join(cdir, "mutant-%s.target.%s" % (did, fn)), "wb") as fh:
                fh.write(blob.replace(old, new, 1))
        ctx["paths"][name] = {"prist": os.path.join(stored, "pristine.target." + fn),
                              "stored": stored}
        for did, old, new in defs[name]:
            ctx["paths"][name][did] = os.path.join(stored, "mutant-%s.target.%s" % (did, fn))
    return ctx


# ---------------------------------------------------------------- trace model
def ienv(path, did, extra=()):
    return ["PATH=/usr/bin:/bin", "MUTANT=%s" % path, "DEFECT_ID=%s" % did] + list(extra)


def envstr(env):
    if env is None or isinstance(env, int):
        return "0x7ffd2c4a1b30 /* 3 vars */"
    vals = []
    for v in env:
        vals.append(q(v) + "..." if len(v) > 4096 else q(v))
    return "[%s]" % ", ".join(vals)


def build_records(ctx):
    recs, pid = [], [100]

    def nxt():
        pid[0] += 1
        return pid[0]

    for name, repo, fn, blob, defs in (
            ("leg-a", "repoa", "a.sh", BLOB_A, [("A1", 1), ("A2", 0)]),
            ("leg-b", "repob", "b.sh", BLOB_B, [("B1", 0)])):
        p = nxt()
        recs.append({"kind": "exec", "tag": "git:" + name, "pid": p, "fn": "/usr/bin/git",
                     "argv": ["git", "-C", os.path.join(ctx["fleet"], repo), "show",
                              "%s:%s" % (ctx["revs"][repo], fn)], "env": None})
        recs.append({"kind": "exit", "pid": p, "code": 0})
        pth = ctx["paths"][name]
        recs.append({"kind": "open", "pid": nxt(), "path": pth["prist"],
                     "resolved": ctx["real"].get(name, pth["stored"]) + "/pristine.target." + fn})
        p = nxt()
        recs.append({"kind": "exec", "tag": "ctl:" + name, "pid": p, "fn": ctx["bash"],
                     "argv": ["bash", pth["prist"], "--selftest"], "env": ienv(pth["prist"], "CONTROL")})
        recs.append({"kind": "exit", "pid": p, "code": 0})
        for did, code in defs:
            mp = pth[did]
            wp = nxt()
            recs.append({"kind": "open", "pid": wp, "path": mp,
                         "resolved": ctx["real"].get(name, pth["stored"]) + "/" + os.path.basename(mp)})
            recs.append({"kind": "write", "pid": wp, "path": mp,
                         "resolved": ctx["real"].get(name, pth["stored"]) + "/" + os.path.basename(mp)})
            p = nxt()
            recs.append({"kind": "exec", "tag": "mut:" + did, "pid": p, "fn": ctx["bash"],
                         "argv": ["bash", mp, "--selftest"], "env": ienv(mp, did)})
            recs.append({"kind": "exit", "pid": p, "code": code})
    return recs


def render(r):
    k = r["kind"]
    if k == "raw":
        return r["text"]
    if k in ("exec", "exec_unfinished"):
        body = "execve(%s, [%s], %s)" % (
            q(r["fn"]), ", ".join(q(a) for a in r["argv"]), envstr(r["env"]))
        if k == "exec_unfinished":
            return "%d %s <unfinished ...>" % (r["pid"], body[:-1])
        return "%d %s = 0" % (r["pid"], body)
    if k == "resumed":
        return "%d <... %s resumed>)            = %s" % (r["pid"], r["call"], r["result"])
    if k == "execveat":
        return "%d execveat(%s, %s, [%s], %s, %d) = 0" % (
            r["pid"], r.get("dirfd", "AT_FDCWD</x>"), q(r["fn"]),
            ", ".join(q(a) for a in r["argv"]), envstr(r["env"]), r.get("flags", 0))
    if k == "exit":
        if r.get("signal"):
            return "%d +++ killed by %s +++" % (r["pid"], r["signal"])
        return "%d +++ exited with %d +++" % (r["pid"], r["code"])
    if k == "open":
        return "%d openat(AT_FDCWD</x>, %s, O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3<%s>" % (
            r["pid"], q(r["path"]), ann(r.get("resolved", r["path"])))
    if k == "write":
        return "%d write(1<%s>, \"x\", 1) = 1" % (r["pid"], ann(r.get("resolved", r["path"])))
    if k == "rename":
        return "%d rename(%s, %s) = 0" % (r["pid"], q(r["src"]), q(r["dst"]))
    if k == "truncate":
        return "%d truncate(%s, 0) = 0" % (r["pid"], q(r["path"]))
    raise SystemExit("bad kind %r" % k)


def stdout_text():
    return ("REGRESSION_CASE leg-a: PASS (band: exact)\n"
            "REGRESSION_CASE leg-b: PASS (band: exact)\n"
            "REGRESSION: PASS (cases=2 passed=2; ledger legs exact)\n")


def find(recs, tag):
    for r in recs:
        if r.get("tag") == tag:
            return r
    raise SystemExit("no record tagged %r" % tag)


# ---------------------------------------------------------------- cases
CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def C0_base(ctx):
    """control: the unperturbed fixture must PASS."""
    return build_records(ctx)


@case
def C0_real(ctx):
    """ground truth: a REAL strace run of a lite honest runner (`real_trace`)."""
    return None


@case
def C1_split_same(ctx):
    """execve split across <unfinished ...>/<... execve resumed>, faithful shape."""
    recs = build_records(ctx)
    r = find(recs, "ctl:leg-a")
    i = recs.index(r)
    recs[i:i + 1] = [{"kind": "exec_unfinished", "pid": r["pid"], "fn": r["fn"],
                      "argv": r["argv"], "env": r["env"]},
                     {"kind": "resumed", "pid": r["pid"], "call": "execve", "result": "0"}]
    return recs


@case
def C2_split_other_name(ctx):
    """the resume line names a DIFFERENT syscall than the pending execve."""
    recs = build_records(ctx)
    r = find(recs, "ctl:leg-a")
    i = recs.index(r)
    recs[i:i + 1] = [{"kind": "exec_unfinished", "pid": r["pid"], "fn": r["fn"],
                      "argv": r["argv"], "env": r["env"]},
                     {"kind": "resumed", "pid": r["pid"], "call": "openat", "result": "0"}]
    return recs


@case
def C3b_resume_without_half(ctx):
    """a resume line for a pid whose pending half is a never-completed execve of the
    mutant (pid exited, later reused): the stale half must not become an exec."""
    recs = build_records(ctx)
    r = find(recs, "mut:A1")
    i = recs.index(r)
    p = r["pid"]
    j = i + 1
    assert recs[j]["kind"] == "exit" and recs[j]["pid"] == p
    recs[i:j + 1] = [
        {"kind": "exec_unfinished", "pid": p, "fn": r["fn"], "argv": r["argv"], "env": r["env"]},
        {"kind": "exit", "pid": p, "code": None, "signal": "SIGKILL"},
        {"kind": "resumed", "pid": p, "call": "write", "result": "1"},
        {"kind": "exit", "pid": p, "code": 1},
    ]
    return recs


@case
def C4_weird_strings(ctx):
    """argv[0] and env values carry `]`, `, `, `"`, ` = `; every path carries `]`, `, `
    and `"`; fd annotations carry the real escapes."""
    return build_records(ctx)


@case
def C5_truncated_string(ctx):
    """`-s 4096` truncation `"value..."...` on a non-steering env value."""
    recs = build_records(ctx)
    for r in recs:
        if r.get("tag") in ("ctl:leg-a", "mut:A1", "mut:A2"):
            r["env"] = r["env"] + ["BIGBLOB=" + "x" * 5000]
    return recs


@case
def C5b_array_abbrev(ctx):
    """array-level `...` (strace abbreviation): a steering variable follows the dots."""
    recs = build_records(ctx)
    r = find(recs, "mut:A1")
    mp = ctx["paths"]["leg-a"]["A1"]
    r["env"] = ["PATH=/usr/bin:/bin", "MUTANT=%s" % mp, "DEFECT_ID=A1",
                "BASH_ENV=/dev/null"]
    recs[recs.index(r)] = {"kind": "raw", "text":
        '%d execve(%s, [%s], ["PATH=/usr/bin:/bin", "MUTANT=%s", "DEFECT_ID=A1", ...]) = 0'
        % (r["pid"], q(r["fn"]), ", ".join(q(a) for a in r["argv"]), mp)}
    return recs


@case
def C6_write_after_exec_gt_case(ctx):
    """post-exec fd write on the mutant, ledger case name containing `>` (faithfully
    rendered as `\\076` in the -y annotation)."""
    recs = build_records(ctx)
    r = find(recs, "mut:A1")
    p = ctx["paths"]["leg-a"]["A1"]
    recs.insert(recs.index(r) + 1, {"kind": "write", "pid": r["pid"], "path": p,
                                    "resolved": p})
    return recs


@case
def C6b_write_after_exec_plain_case(ctx):
    """same post-exec fd write, ordinary case name (control for C6)."""
    recs = build_records(ctx)
    r = find(recs, "mut:A1")
    p = ctx["paths"]["leg-a"]["A1"]
    recs.insert(recs.index(r) + 1, {"kind": "write", "pid": r["pid"], "path": p,
                                    "resolved": p})
    return recs


@case
def C6c_truncate_after_exec_gt_case(ctx):
    """post-exec modification through a path syscall with `>` in the case name."""
    recs = build_records(ctx)
    r = find(recs, "mut:A1")
    recs.insert(recs.index(r) + 1, {"kind": "truncate", "pid": r["pid"],
                                    "path": ctx["paths"]["leg-a"]["A1"]})
    return recs


@case
def C7_execveat(ctx):
    """the leg's interpreter exec reported as execveat(AT_FDCWD, abs path, ...)."""
    recs = build_records(ctx)
    for tag in ("ctl:leg-a", "mut:A1"):
        find(recs, tag)["kind"] = "execveat"
    return recs


@case
def C7b_execveat_dirfd_relative(ctx):
    """execveat(3<case dir>, "pristine.target.a.sh", ...): a dirfd-relative pathname."""
    recs = build_records(ctx)
    r = find(recs, "ctl:leg-a")
    r["kind"] = "execveat"
    r["dirfd"] = "3<%s>" % ann(os.path.dirname(ctx["paths"]["leg-a"]["prist"]))
    r["fn"] = os.path.basename(ctx["paths"]["leg-a"]["prist"])
    return recs


@case
def C8_exit_before_other_pid_exec(ctx):
    """leg-a's control exit line moved in front of every leg-b line."""
    recs = build_records(ctx)
    r = find(recs, "ctl:leg-a")
    ex = recs[recs.index(r) + 1]
    assert ex["kind"] == "exit" and ex["pid"] == r["pid"]
    del recs[recs.index(r) + 1]
    first_b = next(i for i, x in enumerate(recs) if x.get("tag") == "git:leg-b")
    recs.insert(first_b, ex)
    return recs


@case
def C9_pid_reuse_after_exit(ctx):
    """the mutant exec reuses the pid of a process that already exited."""
    recs = build_records(ctx)
    ctl = find(recs, "ctl:leg-a")
    mut = find(recs, "mut:A1")
    i = recs.index(mut)
    assert recs[i + 1]["kind"] == "exit"
    mut["pid"] = ctl["pid"]
    recs[i + 1]["pid"] = ctl["pid"]
    return recs


@case
def C10_pointer_env(ctx):
    """env printed as a bare pointer (`0x... /* N vars */`): env invisible to W_ENV."""
    recs = build_records(ctx)
    for tag in ("ctl:leg-a", "mut:A1", "mut:A2"):
        find(recs, tag)["env"] = 3
    return recs


@case
def C11_execveat_quoted_dirfd(ctx):
    """execveat with a -y dirfd whose decoded path contains a `"` (`\\"` in the trace)."""
    recs = build_records(ctx)
    r = find(recs, "ctl:leg-a")
    r["kind"] = "execveat"
    r["dirfd"] = '3<%s>' % ann(os.path.dirname(ctx["paths"]["leg-a"]["prist"]) + '/q"x')
    return recs


@case
def C12_symlinked_case_dir(ctx):
    """the ledger case dir is a symlink; the post-exec fd write is annotated with the
    RESOLVED path (real strace behaviour), the exec argv keeps the spelling."""
    recs = build_records(ctx)
    r = find(recs, "mut:A1")
    p = ctx["paths"]["leg-a"]["A1"]
    real = os.path.join(ctx["real"]["leg-a"], os.path.basename(p))
    recs.insert(recs.index(r) + 1, {"kind": "write", "pid": r["pid"], "path": p,
                                    "resolved": real})
    return recs


@case
def C13_renamed_ancestor(ctx):
    """the case dir is renamed (leg-a -> leg-a2) around a post-exec fd write, so the
    annotation names the moved path; the dir is renamed back before the audit."""
    recs = build_records(ctx)
    r = find(recs, "mut:A1")
    p = ctx["paths"]["leg-a"]["A1"]
    wd = ctx["wd"]
    moved = os.path.join(wd, "leg-a2", os.path.basename(p))
    i = recs.index(r) + 1
    recs[i:i] = [{"kind": "rename", "pid": 150, "src": os.path.join(wd, "leg-a"),
                  "dst": os.path.join(wd, "leg-a2")},
                 {"kind": "write", "pid": r["pid"], "path": p, "resolved": moved},
                 {"kind": "rename", "pid": 150, "src": os.path.join(wd, "leg-a2"),
                  "dst": os.path.join(wd, "leg-a")}]
    return recs


# ---------------------------------------------------------------- real-trace control
FLAGS = ["-f", "-q", "-y", "-v", "-s", "4096", "-e", "signal=none", "-e",
         "trace=execve,execveat,openat,openat2,open,creat,rename,renameat,renameat2,"
         "link,linkat,symlink,symlinkat,truncate,ftruncate,write,pwrite64,writev,"
         "pwritev,pwritev2,fallocate,copy_file_range,sendfile,splice,setrlimit,prlimit64"]

LITE = """\
W={wd}; F={fleet}; P={prep}
run() {{
  local h="$W/sandbox-$2"; mkdir -p "$h/home" "$h/tmp"
  ( cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C \\
      bash "$1" --selftest )
}}
leg() {{
  local name=$1 repo=$2 file=$3 rev=$4 case=$5
  local d="$W/$case"; mkdir -p "$d"
  git -C "$F/$repo" show "$rev:$file" > "$d/pristine.target.$file"
  run "$d/pristine.target.$file" CONTROL
  for f in "$P/$case"/mutant-*; do
    local b; b=$(basename "$f")
    cp "$f" "$d/$b"
    run "$d/$b" "$(printf '%s' "$b" | sed -E 's/^mutant-([^.]*)\\..*/\\1/')"
  done
  printf 'REGRESSION_CASE %s: PASS (band: exact)\\n' "$name"
}}
leg leg-a repoa a.sh {ra} {ca}
leg leg-b repob b.sh {rb} {cb}
printf 'REGRESSION: PASS (cases=2 passed=2; ledger legs exact)\\n'
"""


def real_trace(ctx):
    """Produce the trace with a REAL strace run of a lite honest runner (ground truth
    for the fixture shape: git show, redirect writes, env -i sandbox, exit codes)."""
    prep = os.path.join(ctx["root"], "prep")
    os.makedirs(prep, exist_ok=True)
    for name in ("leg-a", "leg-b"):
        d = os.path.join(prep, name)
        os.makedirs(d)
        blob = BLOB_A if name == "leg-a" else BLOB_B
        pairs = ([("A1", b"exit 0", b"exit 1"), ("A2", b"echo a", b"echo A")]
                 if name == "leg-a" else [("B1", b"echo b", b"echo B")])
        for did, old, new in pairs:
            with open(os.path.join(d, "mutant-%s.target.%s" % (did, "a.sh" if name == "leg-a" else "b.sh")), "wb") as fh:
                fh.write(blob.replace(old, new, 1))
    lite = os.path.join(ctx["root"], "lite.sh")
    with open(lite, "w", encoding="utf-8") as fh:
        fh.write(LITE.format(wd=ctx["wd"], fleet=ctx["fleet"], prep=prep,
                             ra=ctx["revs"]["repoa"], rb=ctx["revs"]["repob"],
                             ca=ctx["ca"], cb=ctx["cb"]))
    env = {"PATH": "/usr/bin:/bin", "HOME": ctx["root"], "LC_ALL": "C.UTF-8",
           "TMPDIR": ctx["root"]}
    trace = os.path.join(ctx["root"], "trace.txt")
    with open(os.path.join(ctx["root"], "stdout.txt"), "wb") as fh:
        p = subprocess.run(["strace"] + FLAGS + ["-o", trace, "bash", lite],
                           stdout=fh, stderr=subprocess.STDOUT, env=env)
    return p.returncode


REAL = {"C0_real"}


# ---------------------------------------------------------------- driver
EXPECT = {
    "C0_base": ("PASS", "control"),
    "C0_real": ("PASS", "real strace trace of an honest-shaped run"),
    "C1_split_same": ("PASS", "split exec recognised"),
    "C2_split_other_name": ("FAIL", "resume names another syscall: must not count"),
    "C3b_resume_without_half": ("FAIL", "never-completed execve must not exist"),
    "C4_weird_strings": ("PASS", "quoting must round-trip"),
    "C5_truncated_string": ("PASS", "-s truncation, both sides alike"),
    "C5b_array_abbrev": ("FAIL", "steering var follows the array dots"),
    "C6_write_after_exec_gt_case": ("FAIL", "post-exec write on the mutant"),
    "C6b_write_after_exec_plain_case": ("FAIL", "post-exec write on the mutant"),
    "C6c_truncate_after_exec_gt_case": ("FAIL", "post-exec truncate on the mutant"),
    "C7_execveat": ("PASS", "execveat is an exec"),
    "C7b_execveat_dirfd_relative": ("FAIL", "dirfd-relative target: conservative"),
    "C8_exit_before_other_pid_exec": ("PASS", "per-pid pairing"),
    "C9_pid_reuse_after_exit": ("PASS", "per-pid pairing"),
    "C10_pointer_env": ("FAIL", "env not decoded: W_ENV cannot see steering"),
    "C11_execveat_quoted_dirfd": ("PASS", "exec must be recognised despite the quote"),
    "C12_symlinked_case_dir": ("FAIL", "post-exec write on the mutant"),
    "C13_renamed_ancestor": ("FAIL", "post-exec write on the mutant"),
}

OPTS = {
    "C4_weird_strings": {"wdname": 'wd] x, "y"'},
    "C6_write_after_exec_gt_case": {"ca": "x>y"},
    "C6c_truncate_after_exec_gt_case": {"ca": "x>y"},
    "C12_symlinked_case_dir": {"link_a": True},
    "C0_real": {"precreate": False},
}


def run_case(fn):
    name = fn.__name__
    ctx = materialize(name, **OPTS.get(name, {}))
    rc = 0
    if name in REAL:
        rc = real_trace(ctx)
    else:
        recs = fn(ctx)
        if name == "C4_weird_strings":
            for r in recs:
                if r.get("tag") in ("ctl:leg-a", "mut:A1", "mut:A2"):
                    r["argv"] = ['bash]x, "y" = z'] + r["argv"][1:]
                    r["env"] = r["env"] + ['ODD=]a, b"c = d', 'ODD2=1 = 2, [3]']
        with open(os.path.join(ctx["root"], "trace.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(render(r) for r in recs) + "\n")
        with open(os.path.join(ctx["root"], "stdout.txt"), "w", encoding="utf-8") as fh:
            fh.write(stdout_text())
    p = subprocess.run([sys.executable, "-I", WITNESS, "--audit",
                        "--runner", os.path.join(ctx["root"], "runner.sh"),
                        "--fleet", ctx["fleet"],
                        "--trace", os.path.join(ctx["root"], "trace.txt"),
                        "--workdir", ctx["wd"],
                        "--stdout", os.path.join(ctx["root"], "stdout.txt"),
                        "--rc", str(rc)], capture_output=True, text=True)
    exp, why = EXPECT[name]
    fired = re.findall(r"^WITNESS_FINDING (\S+) leg=(\S+) (.*)$", p.stdout, re.M)
    led = [l for l in p.stdout.splitlines() if l.startswith("LEDGER_WITNESS:")]
    obs = "PASS" if p.returncode == 0 else ("FAIL" if p.returncode == 1 else "SETUP")
    dst = os.path.join(FIXTURES, name)
    os.makedirs(dst, exist_ok=True)
    for f in ("runner.sh", "trace.txt", "stdout.txt"):
        shutil.copyfile(os.path.join(ctx["root"], f), os.path.join(dst, f))
    with open(os.path.join(dst, "meta.txt"), "w", encoding="utf-8") as fh:
        fh.write("opts=%s\nexpect=%s\nwhy=%s\nobserved=%s\nrunner_rc=%d\naudit_rc=%d\n" % (
            json.dumps(OPTS.get(name, {})), exp, why, obs, rc, p.returncode))
        fh.write((led[0] if led else "no LEDGER_WITNESS line") + "\n")
        fh.write("".join("FINDING %s %s %s\n" % f for f in fired))
    print("%-32s expect=%-4s observed=%-4s rc=%d findings=%s" % (
        name, exp, obs, p.returncode, ",".join(sorted({c for c, _, _ in fired})) or "-"))
    for c, leg, d in fired:
        print("    %s leg=%s %s" % (c, leg, d))
    if led:
        print("    " + led[0])
    return {"case": name, "expect": exp, "observed": obs, "rc": p.returncode,
            "checks": sorted({c for c, _, _ in fired}), "ledger": led[0] if led else None}


def main(argv):
    global SCRATCH, WITNESS
    if "--witness" in argv:                       # audit with a candidate fix, not the frozen file
        WITNESS = argv[argv.index("--witness") + 1]
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    os.makedirs(FIXTURES, exist_ok=True)
    if "--replay" in argv:
        return replay()
    if not only:
        for d in os.listdir(FIXTURES):
            if os.path.isdir(os.path.join(FIXTURES, d)):
                shutil.rmtree(os.path.join(FIXTURES, d))
    os.makedirs(SCRATCH, exist_ok=True)
    rows = []
    for fn in CASES:
        if only and only not in fn.__name__:
            continue
        rows.append(run_case(fn))
    with open(os.path.join(HERE, "T89C2-results.tsv"), "w", encoding="utf-8") as fh:
        for r in rows:
            verdict = "MISPARSE" if r["expect"] != r["observed"] else "ok"
            fh.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (r["case"], r["expect"], r["observed"],
                                                   r["rc"], ",".join(r["checks"]) or "-", verdict))
    print("\nwrote %s" % os.path.join(HERE, "T89C2-results.tsv"))
    return 0


def replay():
    """Re-audit each saved fixture from its committed trace bytes."""
    rows = []
    for name in sorted(os.listdir(FIXTURES)):
        d = os.path.join(FIXTURES, name)
        if not os.path.isdir(d):
            continue
        meta = open(os.path.join(d, "meta.txt"), encoding="utf-8").read()
        opts = json.loads(re.search(r"^opts=(.*)$", meta, re.M).group(1))
        rc = re.search(r"^runner_rc=(\d+)$", meta, re.M).group(1)
        if name in REAL:
            opts.pop("precreate", None)   # the real run's wd is rebuilt, not re-run
        ctx = materialize(name, **opts)
        p = subprocess.run([sys.executable, "-I", WITNESS, "--audit",
                            "--runner", os.path.join(d, "runner.sh"),
                            "--fleet", ctx["fleet"],
                            "--trace", os.path.join(d, "trace.txt"),
                            "--workdir", ctx["wd"],
                            "--stdout", os.path.join(d, "stdout.txt"), "--rc", rc],
                           capture_output=True, text=True)
        led = [l for l in p.stdout.splitlines() if l.startswith("LEDGER_WITNESS:")]
        print("%-32s rc=%d %s" % (name, p.returncode, led[0] if led else "no LEDGER line"))
        rows.append((name, p.returncode))
    return 0 if rows else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
