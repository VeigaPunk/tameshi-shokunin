#!/usr/bin/env python3
"""Round-89 wave (seat T89E3): honest runner variants for tools/ledger-witness.py.

Kill rule (c) of R89-C1: an honest variant — all the ledger's real work, the
`regression_case_git` call shape kept — refused for a reason other than a declared
limit kills the claim. The pre-freeze positive controls are honest-rename (the
sweep function renamed) and honest-reorder (the eleventh leg moved to the front).
These two NEW variants differ from the base runner along axes neither control
exercises; every one of them is presentational, ordering, declaration or
environment detail that an honest audit must tolerate:

  vars-renamed    every PIN_/REV_/TABLE_ ledger variable is renamed (JS->KIMI,
                  BASH->SURFACE, ...), the --timeout default is 900 not 300, the
                  --tail default is 12 not 8, the auto work-root template is
                  renamed, an extra stdout line names the variant, and a header
                  comment block carries a fresh nonce.
  legs-swapped    the third leg (bash-tsukuroi-census) and the eighth
                  (js-sources-check) swap places, the embedded specs are written
                  to $root/ledger-specs instead of $root/specs, every suite run
                  gets its own TMPDIR under the case workdir named for the run's
                  defect id, an extra stdout line names the variant, and a header
                  comment block carries a fresh nonce.

Both variants still materialize every pinned blob from git, build every
spec-exact mutant, run each mutant through the leg's interpreter with the
suite's exact argv, and keep the recorded verdict table. They are rebuilt
byte-exactly from the committed base runner

    git -C <lane> show 61990f3d8cd99932bfb0575e1c292e03d310b436:tools/mutate-and-run.sh

so a re-run needs no saved copy of the base.

usage: T89E3-honest-variants.py <outdir> [<nonce>]
       (nonce defaults to a fresh 16-byte hex string; it is printed).
"""
import hashlib
import re
import secrets
import subprocess
import sys
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE_REV = "61990f3d8cd99932bfb0575e1c292e03d310b436"

RENAMES = {
    "JS": "KIMI", "BASH": "SURFACE", "TSUKUROI": "TSUK", "MADO": "MADO",
    "CHECKLIST": "CHKL", "CLAIMS": "CLMS", "ROUNDGATE": "RGATE",
    "SOURCESCHECK": "SRCCHK", "CITECHECK": "CITECHK", "DRIFTPINS": "DRIFTP",
    "KAKEGUARD": "KGUARD",
}


def base_text():
    r = subprocess.run(["git", "-C", LANE, "show", "%s:tools/mutate-and-run.sh" % BASE_REV],
                       capture_output=True, check=True)
    return r.stdout.decode()


def rep(text, old, new, tag):
    n = text.count(old)
    assert n == 1, "%s: expected 1 occurrence, found %d" % (tag, n)
    return text.replace(old, new, 1)


def header(t, label, nonce):
    shebang = "#!/usr/bin/env bash\n"
    assert t.startswith(shebang), "base does not start with the shebang"
    return shebang + ("# nonce: %s\n"
                      "# honest runner variant (%s): it performs every ledger leg's real work;\n"
                      "# only presentation/ordering/declaration/TMPDIR details differ from the base\n"
                      "# runner at %s.\n" % (nonce, label, BASE_REV)) + t[len(shebang):]


def rename_vars(t):
    out = t
    for fam, new in RENAMES.items():
        pat = re.compile(r"\b(PIN|REV|TABLE)_%s\b" % fam)
        n = len(pat.findall(out))
        assert n >= 2, "rename %s: only %d occurrences" % (fam, n)
        out = pat.sub(lambda m: "%s_%s" % (m.group(1), new), out)
    return out


def block(t, name, stvar):
    """The exact call block for one leg, from its `regression_case_git <name>` line
    through its `st_<var>=$?` line."""
    head = "  regression_case_git %s \\\n" % name
    start = t.index(head)
    endmark = "  %s=$?\n" % stvar
    end = t.index(endmark, start) + len(endmark)
    return t[start:end]


def variant_vars_renamed(nonce):
    t = base_text()
    t = header(t, "vars-renamed", nonce)
    t = rep(t, "TIMEOUT_S=300\n", "TIMEOUT_S=900\n", "timeout-default")
    t = rep(t, "  --timeout N      seconds per suite run (default: 300)\n",
            "  --timeout N      seconds per suite run (default: 900)\n", "timeout-usage")
    t = rep(t, "TAIL_N=8\n", "TAIL_N=12\n", "tail-default")
    t = rep(t, "  --tail N         output tail lines shown per run (default: 8)\n",
            "  --tail N         output tail lines shown per run (default: 12)\n", "tail-usage")
    t = rep(t, "  root=$(mktemp -d \"${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX\") "
               "|| die_setup 'mktemp -d failed'\n",
            "  root=$(mktemp -d \"${TMPDIR:-/tmp}/tameshi-r89-honest-vars-renamed.XXXXXX\") "
            "|| die_setup 'mktemp -d failed'\n", "auto-root")
    t = rename_vars(t)
    line = ("  printf 'REGRESSION_VARIANT: honest-vars-renamed nonce=%s timeout=%s tail=%s\\n' "
            "\\\n    ") + "'" + nonce + "' " + '\"$TIMEOUT_S\" \"$TAIL_N\"\n'
    t = rep(t, "  printf 'REGRESSION_EXPECT: recorded kill-rates",
            line + "  printf 'REGRESSION_EXPECT: recorded kill-rates", "variant-line")
    t = rep(t, "regression_case_git() {\n",
            "# honest variant: the ledger variables above are renamed (PIN_JS -> PIN_KIMI, ...)\n"
            "# and the defaults differ; the call shape and every leg's work are unchanged.\n"
            "regression_case_git() {\n", "comment-block")
    return t


def variant_legs_swapped(nonce):
    t = base_text()
    t = header(t, "legs-swapped", nonce)
    b_tsu = block(t, "bash-tsukuroi-census", "st_tsu")
    b_src = block(t, "js-sources-check", "st_sourcescheck")
    assert t.count(b_tsu) == 1 and t.count(b_src) == 1
    mark = "\x00SWAP\x00"
    t = t.replace(b_tsu, mark, 1)
    t = t.replace(b_src, b_tsu, 1)
    t = t.replace(mark, b_src, 1)
    t = rep(t, "  specs=\"$root/specs\"\n", "  specs=\"$root/ledger-specs\"\n", "specs-dir")
    t = rep(t, "run_one() { # $1 = artifact under test, $2 = evidence file, $3 = defect id\n"
               "  local start now\n",
            "run_one() { # $1 = artifact under test, $2 = evidence file, $3 = defect id\n"
            "  local start now\n"
            "  # honest TMPDIR difference: each suite run gets its own scratch dir under the\n"
            "  # case workdir, named for the run's defect id (CONTROL for the control run).\n"
            "  mkdir -p \"$WORKDIR/tmp-$3\" || die_setup \"cannot create per-run tmp dir: $WORKDIR/tmp-$3\"\n",
            "tmpdir-mkdir")
    t = rep(t, "  MUTANT=\"$1\" TARGET=\"$TARGET_ABS\" PRISTINE=\"$PRISTINE\" WORKDIR=\"$WORKDIR\" "
               "DEFECT_ID=\"$3\" \\\n",
            "  MUTANT=\"$1\" TARGET=\"$TARGET_ABS\" PRISTINE=\"$PRISTINE\" WORKDIR=\"$WORKDIR\" "
            "DEFECT_ID=\"$3\" TMPDIR=\"$WORKDIR/tmp-$3\" \\\n",
            "tmpdir-env")
    line = ("  printf 'REGRESSION_VARIANT: honest-legs-swapped nonce=%s specs-dir=ledger-specs\\n' "
            "'" + nonce + "'\n")
    t = rep(t, "  printf 'REGRESSION_EXPECT: recorded kill-rates",
            line + "  printf 'REGRESSION_EXPECT: recorded kill-rates", "variant-line")
    t = rep(t, "run_regression() {\n",
            "# honest variant: leg 3 and leg 8 above are swapped, the embedded specs live in\n"
            "# $root/ledger-specs, and every suite run gets a per-defect TMPDIR; the ledger's\n"
            "# work is unchanged.\n"
            "run_regression() {\n", "comment-block")
    return t


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 64
    out = Path(sys.argv[1])
    nonce = sys.argv[2] if len(sys.argv) > 2 else secrets.token_hex(16)
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in (("honest-vars-renamed.sh", variant_vars_renamed),
                     ("honest-legs-swapped.sh", variant_legs_swapped)):
        text = fn(nonce)
        p = out / name
        p.write_text(text, encoding="utf-8")
        p.chmod(0o755)
        print("%s sha256=%s lines=%d" % (p, hashlib.sha256(text.encode()).hexdigest(),
                                         text.count("\n")))
    print("nonce=%s" % nonce)
    return 0


if __name__ == "__main__":
    sys.exit(main())
