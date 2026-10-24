# MutateAnsiBranch — round 37 wave 1

Seat: `L1-tameshi-r37-attempt2.MutateAnsiBranch` (leaf; no dispatch).
Lane base observed: `e6185d5f0b63a6963205110cb098f2f1eca27622` (detached).
Assignment: on a disposable copy, remove only the new ANSI-C quote state branch, run the
frozen two-case measure, and report whether the escaped-quote case reverts to FAIL while the
literal-hash case still PASSes.

## Apparatus

- Disposable copy: `git clone --no-hardlinks <lane> /tmp/tameshi-r37-ansi-mutant`.
  Base HEAD `e6185d5…`, clean, `tools/tally-audit-v3.py` sha256
  `da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede`, blob `b0c7d48`.
- Frozen detector, unchanged, invoked as committed:
  `python3 .ufo/evidence/round-37/code-view/measure.py --lane /tmp/tameshi-r37-ansi-mutant --rev REV`
  (it loads `git show REV:tools/tally-audit-v3.py`, execs `code_view`, checks the two frozen
  fixtures plus length/newline preservation).

Pristine baseline (lane-equivalent revision):

```
CASE ansi-c-escaped-quote-trailing-comment PASS
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=1/1 ansi_literal_hash=1/1 tool_sha256=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C2_R37_PASS=true
MEASURE_RC=0
```

## Mutant

Removed exactly the two scanner hunks added for ANSI-C (same blob b0c7d48 introduced by
`ae9b771` / `235608a`), and nothing else:

- `tools/tally-audit-v3.py:172-179` — `if quote == "ansi-c":` state handler.
- `tools/tally-audit-v3.py:191-194` — `if c == '$' and … text[i + 1] == "'"` entry condition.

The ANSI-C docstring paragraph and the selftest `code_view_cases` block were left untouched;
neither is exercised by the frozen detector.

Evidence of minimality: `git diff --numstat` = `0	12` (12 deletions, 0 insertions); the
scanner body from `out = list(text)` through `return ''.join(out)` (35 lines) is diff-empty
against the pre-ANSI revision `d9c496b`, i.e. the mutant is exactly the previous scanner.
Mutant file sha256 `fe44dcd04211e4507df13afe31b8794f14cb3f9229f50894d2342bb5e8ca1600`;
committed only inside the disposable copy as `c2dca7acef28037edf292115f6115c163be21b5d`.

Expected detector behavior: escaped-quote case FAIL, literal-hash case PASS,
`C2_R37_PASS=false`, exit 1.

## Detector output on the mutant

```
CASE ansi-c-escaped-quote-trailing-comment FAIL
  expected=": $'it\\'s'                 \nst_tsu=9\n"
  actual=": $'it\\'s' # inert st_tsu=0\nst_tsu=9\n"
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=0/1 ansi_literal_hash=1/1 tool_sha256=fe44dcd04211e4507df13afe31b8794f14cb3f9229f50894d2342bb5e8ca1600 rev=c2dca7acef28037edf292115f6115c163be21b5d C2_R37_PASS=false
MEASURE_RC=1
```

## Verdict: KILLED

The frozen two-case measure detects removal of the ANSI-C state branch with exactly the
expected discrimination:

- escaped-quote fixture reverts PASS → FAIL: the trailing comment `# inert st_tsu=0` is no
  longer blanked (`actual` equals the input), so the stale `st_tsu=0` leaks into the
  structural view;
- literal-hash fixture stays PASS byte-identical (`"$'literal # data'"` untouched), so the
  kill is specific to the new capability, not to comment blanking in general.

C2's predicate is therefore responsive to this defect: the pre-existing single-quote scanner
does not satisfy the escaped-quote case, so the claim cannot be met vacuously.

## Restoration evidence

`git reset --hard e6185d5…` in the disposable copy, then the same detector:

```
da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede  tools/tally-audit-v3.py
blob=b0c7d48e526bd7aa15775f9358de26794238e1b6
CASE ansi-c-escaped-quote-trailing-comment PASS
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=1/1 ansi_literal_hash=1/1 tool_sha256=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C2_R37_PASS=true
FINAL_RESTORE_RC=0
```

Restored sha256 and blob match the live lane's `HEAD:tools/tally-audit-v3.py`; worktree
clean. The disposable copy is left at pristine `e6185d5` (mutant commits remain in its object
store/reflog for reproduction).

## Auxiliary probe (secondary; not the assigned mutant)

Removing only the 8-line handler while keeping the `$'` entry condition (commit `67acd1a`,
file sha256 `835a0673a8ea71c5db5b6c85d82b18eb689b4123649106ec65079d96502be73d`) makes the
state unreachable-but-set: both cases FAIL (0/1, 0/1, exit 1), with the literal-hash fixture
now blanked to `": $'literal        \nst_tsu=9\n"`. This confirms the entry condition is
behavior-bearing and that handler+trigger form one unit — the assigned full-branch removal is
the minimal shape reproducing the frozen before-state (one of two fixtures passing).

## Integrity and bounds

- Live lane untouched: HEAD `e6185d5…` and tool sha256 `da8c1ef4…` identical before and
  after; no lane git index, jj, `.git`, `.ufo/state`, fleet, sibling-lane, or source-tree
  operations. Only this report was written under `.ufo/waves/round-37/w1/`.
- Concurrent untracked sibling reports appearing in the lane during the probe were not
  touched.
- No contracts widened: nested command substitutions and unquoted backslash-newline
  continuations remain explicit holds and were not mutated. No tool installs or upgrades were
  performed. No build/lint/selftest suite was run; only the frozen two-case measure, as
  tasked.
