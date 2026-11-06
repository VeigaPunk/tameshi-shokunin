#!/usr/bin/env python3
"""T89E4 / round-89 wave — H2 probe generator (per-defect environment variable).

Hypothesis H2: the W_ENV comparison can be evaded by a per-defect variable whose value
differs only by the defect id as a path token.

The witness normalizes, per audited interpreter exec, MUTANT (to <FILE>) and DEFECT_ID
(to <ID>) when they equal the run's path/id, and elsewhere rewrites the id only where it
sits as a path component:

    tok = re.compile(r"(?<=[-/_])%s(?=/|$)" % re.escape(did))

so `SANDBOX_ROOT=<workdir>/sb-A1` (defect A1) and `SANDBOX_ROOT=<workdir>/sb-CONTROL`
(control) both normalize to `sb-<ID>` and the two environments compare equal.

This generator builds the *real* machinery, not a synthetic trace:

  <out>/fleet/fleetrep/          a one-file fixture git repo (gate.sh), identity ctl
  <out>/forge-h2-runner.sh       the frozen base runner with
                                   - one fixture leg declared in the ledger call shape
                                     (`fleetrep/gate.sh`, cosmetic spec, table A1/A2),
                                   - `SANDBOX_ROOT="$h"` in the leg's suite (the
                                     per-defect variable), and
                                   - the runner planting `poison` in the A1 sandbox.
  gate.sh exits 1 iff `$SANDBOX_ROOT/poison` exists; its own logic is independent of
  both mutations, so A1 would SURVIVE honestly. The runner plants the poison only for
  A1, so the kernel exit is 1 and the recorded KILLED matches -- while the only
  per-defect difference visible to the witness is a path token it normalizes.

Byte base: `git -C <lane> show 61990f3d8cd99932bfb0575e1c292e03d310b436:tools/mutate-and-run.sh`.

Usage:
  python3 -I T89E4-make-forge-h2.py <outdir>
      -> <outdir>/fleet/fleetrep (fixture repo), <outdir>/forge-h2-runner.sh
"""
import hashlib
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE_REV = "61990f3d8cd99932bfb0575e1c292e03d310b436"
BASE_PATH = "tools/mutate-and-run.sh"

GATE = """#!/usr/bin/env bash
# T89E4 H2 fixture gate. Its exit code depends only on the sandbox the environment
# names: 1 iff $SANDBOX_ROOT/poison exists, else 0. Neither mutation below can move it.
LABEL_A=alpha
LABEL_B=beta
if [[ -z "${SANDBOX_ROOT:-}" ]]; then printf 'gate: SANDBOX_ROOT unset\\n'; exit 2; fi
if [[ -e "$SANDBOX_ROOT/poison" ]]; then printf 'gate: poisoned sandbox\\n'; exit 1; fi
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

# The suite is the only place the per-defect variable appears. It is single-quoted in
# the leg call (the witness's LEG_RE shape), so it may not contain a single quote.
SUITE = ('h="$WORKDIR/sb-$DEFECT_ID"; mkdir -p "$h" || exit 2; '
         'if [[ "$DEFECT_ID" == A1 ]]; then : >"$h/poison"; fi; '
         'exec env -i PATH="$PATH" SANDBOX_ROOT="$h" bash "$MUTANT" --selftest')

OLD_SPEC_HEAD = ('regression_specs() { # <dir> \u2014 write the eleven embedded case specs\n'
                 '  local d=$1\n')
NEW_SPEC_HEAD = OLD_SPEC_HEAD + '  cat >"$d/leg-a.spec" <<\'EOT\'\n' + LEG_SPEC + 'EOT\n'

LEG_BLOCK_START = '  local st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck st_driftpins st_kakeguard\n'
LEG_BLOCK_END = '  st_kakeguard=$?\n'

NEW_LEG_BLOCK = (
    '  regression_case_git leg-a \\\n'
    "    'fleetrep/gate.sh' \"$PIN_A\" \"$REV_A\" \\\n"
    '    "$specs/leg-a.spec" \'' + SUITE + '\' "$TABLE_A" \\\n'
    '    "$root/leg-a"\n'
    '  st_fx=$?\n')


def base_bytes():
    return subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (BASE_REV, BASE_PATH)],
                          capture_output=True, check=True).stdout


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


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


def build(pin, rev):
    text = base_bytes().decode("utf-8")
    # spec block
    assert text.count(OLD_SPEC_HEAD) == 1
    text = text.replace(OLD_SPEC_HEAD, NEW_SPEC_HEAD, 1)
    # leg block
    i = text.find(LEG_BLOCK_START)
    j = text.find(LEG_BLOCK_END)
    assert i != -1 and j != -1 and j > i and text.count(LEG_BLOCK_START) == 1
    text = text[:i] + NEW_LEG_BLOCK + text[j + len(LEG_BLOCK_END):]
    # tally
    for name, old, new in (
            ("nlegs", "  local nlegs=11 npass=0 nfail=0 nsetup=0 st\n",
             "  local nlegs=1 npass=0 nfail=0 nsetup=0 st\n"),
            ("tally-loop",
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
    if len(argv) != 1:
        sys.stderr.write(__doc__)
        return 2
    out = os.path.abspath(argv[0])
    os.makedirs(out, exist_ok=True)
    fleet = os.path.join(out, "fleet")
    for p in (fleet, os.path.join(out, "forge-h2-runner.sh")):
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)
    os.makedirs(fleet, exist_ok=True)
    rev, pin = make_fixture_repo(fleet)
    text = build(pin, rev)
    runner = os.path.join(out, "forge-h2-runner.sh")
    data = text.encode("utf-8")
    with open(runner, "wb") as fh:
        fh.write(data)
    os.chmod(runner, 0o755)
    print("WROTE %s bytes=%d sha256=%s" % (runner, len(data), hashlib.sha256(data).hexdigest()))
    print("FIXTURE rev=%s pin=%s" % (rev, pin))
    print("RUN python3 -I %s/tools/ledger-witness.py --run --runner %s --fleet %s --scratch <empty>"
          % (LANE, runner, fleet))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
