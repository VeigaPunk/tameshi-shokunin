#!/usr/bin/env python3
"""Round-88 control generator: derive a runner variant from the base runner bytes by
adding ONE ledger leg (vars, spec heredoc, call, nlegs, tally loop operand). Used for the
pre-freeze forgery controls; every control is this script + a named variant.

usage: make-runner.py <base-runner> <out> <variant> [--spec FILE]

Variants (each a cheat that must NOT reach C1_R88_PASS=true):
  comment      ledger comment row only, no leg
  trivial      py leg, suite `true`, table all SURVIVED
  cmp          py leg, suite `cmp -s "$MUTANT" "$PRISTINE"`, table all KILLED
  lanetarget   leg whose target is a tameshi tool (sibling check)
  dup          an 11th leg that re-declares kimi-census under a new name
  doctored     py leg, real suite + pre-registered spec, every predicted verdict inverted
  forged       doctored leg + run_regression prints PASS cases=11 and exits 0 at once
  unprereg     py leg, real suite, spec with one comment byte changed, predicted table
"""
import sys

KAKE_REL = "kake-shokunin/scripts/ledger_append_guard.py"
KAKE_PIN = "0c12838e3d4ea441eb750fd4c6af2398cfa704e5077f6c58b053d535f8514067"
KAKE_REV = "e8d3a924249983972e5163d160cf236487986c55"
PY_SUITE = ('h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i '
            'PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 '
            'GIT_CEILING_DIRECTORIES="$h" python3 -I "$MUTANT" --selftest')
IDS = ["K_CUT_WHOLE", "K_STARTSWITH", "K_FILES_EQ", "K_GLOB", "K_SHOW_RC",
       "S_HEAD_SHORT", "S_OFFSET_EQ", "S_OK_ALL", "S_VACUOUS", "S_RED_FILES"]
PREDICTED = {i: ("KILLED" if i.startswith("K_") else "SURVIVED") for i in IDS}
INV = {"KILLED": "SURVIVED", "SURVIVED": "KILLED"}


def table(m):
    return ",".join("%s:%s" % (i, m[i]) for i in IDS)


def once(t, old, new):
    assert t.count(old) == 1, old[:60]
    return t.replace(old, new, 1)


def add_leg(t, name, var, rel, pin, rev, suite, tbl, spec):
    t = once(t, "TABLE_DRIFTPINS='", "PIN_%s=%s\nREV_%s=%s\nTABLE_%s='%s'\nTABLE_DRIFTPINS='" % (
        var, pin, var, rev, var, tbl))
    anchor = "@new     *) printf 'drift-pins: unknown argument: %s\\\\n' \"$1\" >&2; exit 0 ;;\nEOT\n"
    t = once(t, anchor, anchor + "  cat >\"$d/%s.spec\" <<'EOT'\n%sEOT\n" % (name, spec))
    call = ("  regression_case_git %s \\\n    '%s' \"$PIN_%s\" \"$REV_%s\" \\\n"
            "    \"$specs/%s.spec\" '%s' \"$TABLE_%s\" \\\n    \"$root/%s\"\n  st_x%s=$?\n") % (
        name, rel, var, var, name, suite, var, name, var.lower())
    t = once(t, "  local nlegs=10 npass=0 nfail=0 nsetup=0 st\n",
             call + "\n  local nlegs=11 npass=0 nfail=0 nsetup=0 st\n")
    t = once(t, '"$st_driftpins"; do', '"$st_driftpins" "$st_x%s"; do' % var.lower())
    return t


def main():
    base, out, variant = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = open(sys.argv[5]).read() if len(sys.argv) > 5 and sys.argv[4] == "--spec" else None
    t = open(base).read()
    py = lambda suite, tbl, sp: add_leg(t, "py-kake-ledger-guard", "KAKEGUARD", KAKE_REL, KAKE_PIN,
                                       KAKE_REV, suite, tbl, sp)
    if variant == "comment":
        t = once(t, "#   bash-drift-pins       kagi-shokunin/corpus/drift-pins.sh          2/10 (20 %)\n",
                 "#   bash-drift-pins       kagi-shokunin/corpus/drift-pins.sh          2/10 (20 %)\n"
                 "#   py-kake-ledger-guard  kake-shokunin/scripts/ledger_append_guard.py 5/10 (50 %)\n")
    elif variant == "trivial":
        t = py("true", table({i: "SURVIVED" for i in IDS}), spec)
    elif variant == "cmp":
        t = py('cmp -s "$MUTANT" "$PRISTINE"', table({i: "KILLED" for i in IDS}), spec)
    elif variant == "lanetarget":
        t = add_leg(t, "py-lane-receipt-exists", "LANETOOL", "tameshi-shokunin/tools/receipt-exists.py",
                    KAKE_PIN, KAKE_REV, PY_SUITE, table(PREDICTED), spec)
    elif variant == "dup":
        t = add_leg(t, "js-kimi-census-again", "KIMIAGAIN", "kumitate-shokunin/scripts/kimi-census.mjs",
                    "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
                    "175de6ba2e9e904010411b19cab27e0af9aad3d4", 'node "$MUTANT" --selftest',
                    "D1:KILLED,D2:SURVIVED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:KILLED,D8:KILLED,D9:KILLED,D10:SURVIVED",
                    t.split("  cat >\"$d/js-kimi-census.spec\" <<'EOT'\n", 1)[1].split("\nEOT\n", 1)[0] + "\n")
        t = t.replace('"$specs/js-kimi-census-again.spec"', '"$specs/js-kimi-census-again.spec"')
    elif variant == "doctored":
        t = py(PY_SUITE, table({i: INV[PREDICTED[i]] for i in IDS}), spec)
    elif variant == "forged":
        t = py(PY_SUITE, table({i: INV[PREDICTED[i]] for i in IDS}), spec)
        t = once(t, "run_regression() {\n",
                 "run_regression() {\n  printf 'REGRESSION: PASS (cases=11 passed=11; ledger legs exact: "
                 "killed-delta<=0 flips<=0)\\n'; exit 0\n")
    elif variant == "unprereg":
        t = py(PY_SUITE, table(PREDICTED), spec.replace("# Safety:", "# Safety :", 1))
    else:
        sys.exit("unknown variant " + variant)
    open(out, "w").write(t)


if __name__ == "__main__":
    main()
