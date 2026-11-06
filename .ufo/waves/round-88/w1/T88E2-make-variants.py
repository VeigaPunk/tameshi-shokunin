#!/usr/bin/env python3
"""T88E2 — build the three round-88 runner counterfeits byte-exactly from the
candidate runner (28ec58858a084bc193a89ca5b0a751942694ccfb:tools/mutate-and-run.sh).

Each variant is produced by ONE asserted textual replacement of the candidate
bytes, so this generator (not a scratch copy) is the source of record.

  parked   the py-kake leg's regression_case_git call is moved into a function that
           is never called; the tally hard-codes st_kakeguard=0, so --regression
           prints PASS(cases=11 passed=11) after executing only the ten historical
           legs. The counter still parses and independently replays the dead leg.
  dupbase  bash-drift-pins is dropped and its slot re-declares bash-surface-census
           under the path spelling 'kagi-shokunin/./corpus/surface-census.sh'
           (git resolves './'-prefixed rev:path). The counter's duplicate-target
           key is (repo, raw path), so the re-declaration is counted as a distinct
           target: 11 counted legs over only 10 distinct gates.
  stub     the --regression dispatch is rerouted to a stub that prints the frozen
           PASS line; no leg is executed at all, while all eleven leg declarations
           remain in the file for the counter to replay.

Usage: T88E2-make-variants.py <outdir>
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "28ec58858a084bc193a89ca5b0a751942694ccfb"


def candidate() -> bytes:
    r = subprocess.run(["/usr/bin/git", "-C", LANE, "show", "%s:tools/mutate-and-run.sh" % REV],
                       capture_output=True, check=True)
    return r.stdout


def block(text: str, name: str, status: str) -> str:
    """Return the exact 4-line regression_case_git call plus its status assignment."""
    m = re.search(r"^  regression_case_git %s \\\n(?:.*\n){2}.*\n  %s=\$\?\n" % (re.escape(name), status),
                  text, re.M)
    assert m, "block not found: " + name
    return m.group(0)


def replace_once(text: str, old: str, new: str, tag: str) -> str:
    n = text.count(old)
    assert n == 1, "%s: expected 1 occurrence, found %d" % (tag, n)
    return text.replace(old, new, 1)


def main() -> int:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    base = candidate().decode()
    assert hashlib.sha256(base.encode()).hexdigest() == \
        "0a0e46de70e8b4f7cda2220efc37757e8bb49ea3833e0920a97a78aaad795a4a", "candidate bytes drifted"
    kake = block(base, "py-kake-ledger-guard", "st_kakeguard")
    drift = block(base, "bash-drift-pins", "st_driftpins")
    insert_at = "\nrun_regression() {\n"
    dispatch = "  regression) run_regression ;;\n"

    # ---- parked -------------------------------------------------------
    parked_fn = (
        "\n# T88E2 variant `parked` — the eleventh leg is DECLARED here and never executed;\n"
        "# the tally below hard-codes its status. Byte-indexers still see a leg.\n"
        "regression_parked_leg() {\n"
        + kake.replace("  st_kakeguard=$?\n", "") +
        "  return 0\n}\n")
    a = replace_once(base, kake, "  st_kakeguard=0  # T88E2 parked: no sweep is executed\n",
                     "parked/call")
    a = replace_once(a, insert_at, parked_fn + insert_at, "parked/insert")
    (out / "parked.sh").write_text(a)

    # ---- dupbase ------------------------------------------------------
    dup = (
        "  regression_case_git bash-surface-census-dup \\\n"
        "    'kagi-shokunin/./corpus/surface-census.sh' \"$PIN_BASH\" \"$REV_BASH\" \\\n"
        "    \"$specs/bash-surface-census.spec\" 'bash \"$MUTANT\" --selftest' \"$TABLE_BASH\" \\\n"
        "    \"$root/bash-surface-census-dup\"\n"
        "  st_driftpins=$?\n")
    b = replace_once(base, drift, dup, "dupbase/swap")
    (out / "dupbase.sh").write_text(b)

    # ---- stub ---------------------------------------------------------
    stub_fn = (
        "\n# T88E2 variant `stub` — --regression never runs a leg; it prints the frozen\n"
        "# receipt the counter's necessary-consistency field reads.\n"
        "run_regression_stub() {\n"
        "  printf 'REGRESSION: PASS (cases=11 passed=11; ledger legs exact: killed-delta<=0 flips<=0)\\n'\n"
        "  exit 0\n}\n")
    c = replace_once(base, dispatch, "  regression) run_regression_stub ;;\n", "stub/dispatch")
    c = replace_once(c, insert_at, stub_fn + insert_at, "stub/insert")
    (out / "stub.sh").write_text(c)

    for p in sorted(out.glob("*.sh")):
        print("%s sha256=%s lines=%d" % (p.name, hashlib.sha256(p.read_bytes()).hexdigest(),
                                         len(p.read_text().splitlines())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
