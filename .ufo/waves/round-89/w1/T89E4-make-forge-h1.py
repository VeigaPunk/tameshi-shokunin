#!/usr/bin/env python3
"""T89E4 / round-89 wave — H1 forgery generator (labrat probe on the L3 boundary).

Hypothesis H1: the witness accepts a runner that runs survivors honestly but
sabotages the defects the ledger records KILLED through process state the trace does
not carry (declared limit L3), e.g. the inherited fd table or the working directory.

Both modes below run the *real* suite on the spec-exact mutant with the leg's exact
argv and environment; they differ only in process state the witness's strace filter
does not record (STRACE_FLAGS traces execve/open/write/rename/.../rlimit, never umask,
and never the cwd):

  umask   prefix `mkdir -p <sandbox dirs under the normal umask>; umask 0777;` and run
          the child with fd 1/fd 2 on /dev/full.  The fd half is L3's enumerated
          "inherited fd table"; the umask is process state L3 does not enumerate.
  delcwd  prefix `dc=$(mktemp -d ...); cd "$dc" && rmdir "$dc";` and fd 1/fd 2 on
          /dev/full — strictly the two L3 instances L3 does enumerate (working
          directory, fd table).

Either way the interpreter still execs the mutant on its spec-exact bytes with the
declared argv and the leg's environment, so W_EXEC / W_CONTENT / W_ENV / W_ORDER stay
clean; the kernel exit is forced non-zero, so W_VERDICT reads the recorded KILLED.
The CONTROL and every SURVIVED-recorded defect run untouched (honest work).

Byte base: `git -C <lane> show 61990f3d8cd99932bfb0575e1c292e03d310b436:tools/mutate-and-run.sh`
(the round-89 plan's base commit). The four patches below are asserted to apply
exactly once each, so the output is byte-exact for a given base and mode.

Usage:
  python3 -I T89E4-make-forge-h1.py <outdir> [umask|delcwd]
      -> <outdir>/forge-h1-<mode>-runner.sh   (mode 0755; the runner to hand to --run)
"""
import hashlib
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE_REV = "61990f3d8cd99932bfb0575e1c292e03d310b436"
BASE_PATH = "tools/mutate-and-run.sh"

OLD_RUN_ONE = '''run_one() { # $1 = artifact under test, $2 = evidence file, $3 = defect id
  local start now
  start=$(date +%s%N)
  MUTANT="$1" TARGET="$TARGET_ABS" PRISTINE="$PRISTINE" WORKDIR="$WORKDIR" DEFECT_ID="$3" \\
    timeout "$TIMEOUT_S" bash -c "$SUITE" </dev/null >"$2" 2>&1
  RC=$?
'''

# mode -> (docstring line, prefix prepended to the suite inside the same `bash -c`)
MODES = {
    "umask": (
        # T89E4 forge (H1/umask): umask clamp + fd 1/fd 2 on /dev/full.
        '  # T89E4 forge (H1): for a defect the ledger records KILLED, the suite string is run\n'
        '  # with a prefix that (a) pre-creates the leg\'s per-defect sandbox dirs under the\n'
        '  # normal umask so the suite\'s own `mkdir -p`/`cd` still succeed, and (b) clamps the\n'
        '  # umask to 0777; fd 1/fd 2 of the child name /dev/full. The exec shape is the honest\n'
        '  # one (no extra shell level, no extra command before `timeout`), so SHLVL and `_`\n'
        '  # match the control\'s environment; argv and the leg\'s environment are untouched.\n'
        '  # Neither umask nor the fd table is in the witness\'s strace filter.\n',
        'mkdir -p \\"$WORKDIR/sandbox-$3/home\\" \\"$WORKDIR/sandbox-$3/tmp\\"; umask 0777; '),
    "delcwd": (
        # T89E4 forge (H1/delcwd): deleted cwd + fd 1/fd 2 on /dev/full.
        '  # T89E4 forge (H1/delcwd): the suite runs with its initial cwd already removed\n'
        '  # and fd 1/fd 2 on /dev/full. The exec shape is the honest one (no extra shell\n'
        '  # level, no extra command before `timeout`), so SHLVL and `_` match the control;\n'
        '  # argv and the leg environment are untouched. Neither the cwd nor the fd table\n'
        '  # is carried by the witness trace.\n',
        'dc=\\$(mktemp -d \\"$WORKDIR/.cwd-$3.XXXXXX\\") || exit 2; cd \\"\\$dc\\" && rmdir \\"\\$dc\\"; '),
}

NEW_RUN_ONE = '''run_one() { # $1 = artifact under test, $2 = evidence file, $3 = defect id
  local start now
  start=$(date +%s%N)
__COMMENT__  if [[ -n "${RECORDED-}" && "$3" != CONTROL && "$(table_lookup "$RECORDED" "$3")" == KILLED ]]; then
    MUTANT="$1" TARGET="$TARGET_ABS" PRISTINE="$PRISTINE" WORKDIR="$WORKDIR" DEFECT_ID="$3" \\
      timeout "$TIMEOUT_S" bash -c "__PREFIX__$SUITE" </dev/null >/dev/full 2>&1
  else
    MUTANT="$1" TARGET="$TARGET_ABS" PRISTINE="$PRISTINE" WORKDIR="$WORKDIR" DEFECT_ID="$3" \\
      timeout "$TIMEOUT_S" bash -c "$SUITE" </dev/null >"$2" 2>&1
  fi
  RC=$?
'''

OLD_SWEEP_CALL = '''  bash "$SELF" --target "$target" --defects "$spec" --suite "$suite" \\
    --workdir "$cwd" --label "$name" --timeout "$TIMEOUT_S" --tail "$TAIL_N" \\
'''

NEW_SWEEP_CALL = '''  bash "$SELF" --target "$target" --defects "$spec" --suite "$suite" \\
    --workdir "$cwd" --label "$name" --timeout "$TIMEOUT_S" --tail "$TAIL_N" \\
    --recorded "$table" \\
'''

OLD_GLOBAL = "FLEET_ROOT=''   # set by run_regression; regression_case_git resolves repos from it\n"
NEW_GLOBAL = OLD_GLOBAL + "RECORDED=''    # T89E4 forge: the leg's recorded table, read by run_one's KILLED arm\n"

OLD_OPT = '    --tail) need_val "$@"; TAIL_N=$2; shift 2 ;;\n'
NEW_OPT = OLD_OPT + '    --recorded) need_val "$@"; RECORDED=$2; shift 2 ;;   # T89E4 forge (plumbing)\n'


def base_bytes():
    return subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (BASE_REV, BASE_PATH)],
                          capture_output=True, check=True).stdout


def build(mode):
    comment, prefix = MODES[mode]
    patches = [
        ("run_one", OLD_RUN_ONE,
         NEW_RUN_ONE.replace("__COMMENT__", comment).replace("__PREFIX__", prefix)),
        ("sweep-call", OLD_SWEEP_CALL, NEW_SWEEP_CALL),
        ("global", OLD_GLOBAL, NEW_GLOBAL),
        ("option", OLD_OPT, NEW_OPT),
    ]
    text = base_bytes().decode("utf-8")
    for name, old, new in patches:
        n = text.count(old)
        if n != 1:
            raise SystemExit("patch %s: anchor count %d (expected 1)" % (name, n))
        text = text.replace(old, new, 1)
    return text


def main(argv):
    if len(argv) not in (1, 2) or (len(argv) == 2 and argv[1] not in MODES):
        sys.stderr.write(__doc__)
        return 2
    outdir = argv[0]
    mode = argv[1] if len(argv) == 2 else "umask"
    text = build(mode)
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "forge-h1-%s-runner.sh" % mode)
    data = text.encode("utf-8")
    with open(out, "wb") as fh:
        fh.write(data)
    os.chmod(out, 0o755)
    print("MODE  %s" % mode)
    print("WROTE %s bytes=%d sha256=%s" % (out, len(data), hashlib.sha256(data).hexdigest()))
    print("BASE  %s:%s sha256=%s" % (BASE_REV, BASE_PATH,
                                     hashlib.sha256(base_bytes()).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
