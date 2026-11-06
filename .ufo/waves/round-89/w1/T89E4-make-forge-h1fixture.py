#!/usr/bin/env python3
"""T89E4 / round-89 wave — H1 *false-verdict* fixture generator.

The accepted H1 runner (T89E4-make-forge-h1.py, mode umask) coerces the exit of every
defect the ledger records KILLED, but on the real 11-leg ledger those defects also die
honestly, so it does not by itself show a *false* KILLED row passing. This generator
turns the same coercion into a decisive counterfeit: one fixture leg whose A1 mutation
is cosmetic (the gate exits 0 on the mutant when run honestly) and whose recorded table
says A1:KILLED. The runner manufactures the KILLED row through process state only --
umask 0777 + fd 1/fd 2 on /dev/full -- with no per-defect environment variable, no
planted file and no content change to the mutant.

  <out>/fleet/fleetrep/gate.sh   fixture gate: writes a scratch file and reads it back;
                                 exits 4 when the file it created is unreadable (umask
                                 0777), else 0. Neither mutation can move the exit code.
  <out>/forge-h1fixture-runner.sh  the accepted umask-mode forgery with its 11 legs
                                 replaced by this one fixture leg (table A1:KILLED,
                                 A2:SURVIVED; suite `bash "$MUTANT" --selftest`).

Byte chain (both steps are byte-exact):
  1. python3 -I T89E4-make-forge-h1.py <dir> umask        -> <dir>/forge-h1-umask-runner.sh
  2. python3 -I T89E4-make-forge-h1fixture.py <dir>/forge-h1-umask-runner.sh <out>

Usage:
  python3 -I T89E4-make-forge-h1fixture.py <umask-runner> <outdir>
"""
import hashlib
import os
import shutil
import subprocess
import sys

GATE = """#!/usr/bin/env bash
# T89E4 H1 fixture gate: writes a scratch file and reads it back. Under a normal umask
# it exits 0; under umask 0777 the file it creates is mode 000 and the read-back fails.
TMPF="${TMPDIR:-/tmp}/gate.$$"
printf 'x\\n' > "$TMPF" || exit 3
v=$(cat "$TMPF") || exit 4
rm -f "$TMPF"
[[ "$v" == x ]] || exit 5
LABEL_A=alpha
LABEL_B=beta
printf '%s %s\\n' "$LABEL_A" "$LABEL_B"
exit 0
"""

LEG_SPEC = """@defect A1 | cosmetic label edit (cannot change the exit code)
@old LABEL_A=alpha
@new LABEL_A=alpha1

@defect A2 | cosmetic label edit (cannot change the exit code)
@old LABEL_B=beta
@new LABEL_B=beta2
"""

OLD_SPEC_HEAD = ('regression_specs() { # <dir> \u2014 write the eleven embedded case specs\n'
                 '  local d=$1\n')
NEW_SPEC_HEAD = OLD_SPEC_HEAD + '  cat >"$d/leg-a.spec" <<\'EOT\'\n' + LEG_SPEC + 'EOT\n'

LEG_BLOCK_START = ('  local st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate '
                   'st_sourcescheck st_citecheck st_driftpins st_kakeguard\n')
LEG_BLOCK_END = '  st_kakeguard=$?\n'

NEW_LEG_BLOCK = (
    '  regression_case_git leg-a \\\n'
    "    'fleetrep/gate.sh' \"$PIN_A\" \"$REV_A\" \\\n"
    '    "$specs/leg-a.spec" \'bash "$MUTANT" --selftest\' "$TABLE_A" \\\n'
    '    "$root/leg-a"\n'
    '  st_fx=$?\n')


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def make_fixture_repo(fleet):
    repo = os.path.join(fleet, "fleetrep")
    os.makedirs(repo)
    run(["git", "-C", repo, "init", "-q"])
    top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(repo), (top, repo)
    gate = os.path.join(repo, "gate.sh")
    with open(gate, "w", encoding="utf-8") as fh:
        fh.write(GATE)
    os.chmod(gate, 0o644)
    run(["git", "-C", repo, "add", "gate.sh"])
    run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
         "commit", "-q", "-m", "fixture gate"])
    rev = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
    blob = subprocess.run(["git", "-C", repo, "show", "%s:gate.sh" % rev],
                          check=True, capture_output=True).stdout
    return rev, hashlib.sha256(blob).hexdigest()


def build(text, pin, rev):
    assert text.count(OLD_SPEC_HEAD) == 1, "spec anchor"
    text = text.replace(OLD_SPEC_HEAD, NEW_SPEC_HEAD, 1)
    i, j = text.find(LEG_BLOCK_START), text.find(LEG_BLOCK_END)
    assert i != -1 and j > i and text.count(LEG_BLOCK_START) == 1, "leg block"
    text = text[:i] + NEW_LEG_BLOCK + text[j + len(LEG_BLOCK_END):]
    for name, old, new in (
            ("nlegs", "  local nlegs=11 npass=0 nfail=0 nsetup=0 st\n",
             "  local nlegs=1 npass=0 nfail=0 nsetup=0 st\n"),
            ("tally",
             '  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" '
             '"$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck" '
             '"$st_driftpins" "$st_kakeguard"; do\n',
             '  for st in "$st_fx"; do\n'),
            ("vars", "PIN_JS=",
             "PIN_A=%s\nREV_A=%s\nTABLE_A='A1:KILLED,A2:SURVIVED'\nPIN_JS=" % (pin, rev))):
        assert text.count(old) == 1, name
        text = text.replace(old, new, 1)
    return text


def main(argv):
    if len(argv) != 2:
        sys.stderr.write(__doc__)
        return 2
    src, out = argv
    with open(src, encoding="utf-8") as fh:
        text = fh.read()
    out = os.path.abspath(out)
    os.makedirs(out, exist_ok=True)
    fleet = os.path.join(out, "fleet")
    for p in (fleet, os.path.join(out, "forge-h1fixture-runner.sh")):
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)
    os.makedirs(fleet, exist_ok=True)
    rev, pin = make_fixture_repo(fleet)
    data = build(text, pin, rev).encode("utf-8")
    runner = os.path.join(out, "forge-h1fixture-runner.sh")
    with open(runner, "wb") as fh:
        fh.write(data)
    os.chmod(runner, 0o755)
    print("WROTE %s bytes=%d sha256=%s" % (runner, len(data), hashlib.sha256(data).hexdigest()))
    print("FIXTURE rev=%s pin=%s" % (rev, pin))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
