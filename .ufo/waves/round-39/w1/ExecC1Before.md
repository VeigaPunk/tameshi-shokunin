# ExecC1Before — C1 control at base rev 50aadd1b (do-nothing must stay false)

## Command and result

Exactly the frozen `C1.counting_command` with `LANE` and `REV` substituted:

```
python3 .ufo/evidence/round-39/guard/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 50aadd1bbd94e43cd3fcfb81459414394db2dc35
```

```
C1_R39: guard_absent=1 live_d=9/9 strip_d=0/0 live_agree=0 stripped_agree=0 r38_regex_hits=0 mismatches=1 rev=50aadd1bbd94e43cd3fcfb81459414394db2dc35 C1_R39_PASS=false
```

**exit code 1.** stderr empty. Three consecutive runs are byte-identical
(stdout sha256 prefix `eb87e3d08ce9df59` each time); absolute and relative
`--lane` produce the same line.

This is the control, not a deciding run. It reproduces the contract's frozen
`C1.before` exactly: `C1_R39_PASS=false guard_absent=1 mismatches=1 at
50aadd1bbd94e43cd3fcfb81459414394db2dc35` (contract.json:14). Doing nothing
cannot reach `PASS=true`.

## Independent corroboration of each number

All reads are `git show REV:path` at 50aadd1b; nothing was checked out.

| quantity | how | value |
|---|---|---|
| canonical command D | contract one-liner (`no_harm_guard.depth_command_d`, contract.json:36) on `tools/mutate-and-run.sh` | `recorded_cases=9 depth_score=9` |
| D hit lines | regex over blob | 9, at `tools/mutate-and-run.sh:87-95` (5 js, 4 bash) — matches SCORECARD.md:1536 ("87-95, nine legs") |
| ledger-stripped copy | drop lines where command D matches | 2071 of 2080 lines kept, 0 remaining D hits |
| r38 `^\s*leg` | `re.findall(r'^\s*leg', blob, re.M)` | 0 hits (vacuous control holds) |
| contract at base | `git show REV:.ufo/evidence/round-39/contract.json` | **absent** (rc≠0) → `guard_absent=1` branch taken |

The counter itself is absent at the base rev
(`git cat-file -e 50aadd1b:.ufo/evidence/round-39/guard/measure.py` → no), so
the control necessarily runs the working-tree counter against base-rev data.
That is safe here: the working tree, `HEAD:...measure.py`, and the contract pin
`counter_sha256` are all `324df4ca6134821bb56ce8bd6573f1ab02f6bce7c7cfe9392d9859ace026eb11`
(contract.json:19; HEAD = `233077f88d7a8d142eff329202a120457a5d5258`).

## Depth: what the counter can and cannot be fooled by

Reachability and negative controls were exercised on a throwaway lane in
`/tmp/tameshi-r39-ExecC1Before/lane` (git repo, base-rev runner bytes copied,
contract variants committed). `measure.py --lane <lab> --rev <commit>`:

| contract regex planted | rc | live_guard | strip_guard | verdict |
|---|---|---|---|---|
| `A` canonical D pattern | 0 | 9/9 | 0/0 | `PASS=true` — the predicate is reachable, not stuck false |
| `B` r38 `^\s*leg` | 1 | 0/0 | 0/0 | `live_agree=0`, `mismatches=1` → false |
| `D` `^#` (superset) | 1 | 313/10 | 304/10 | false on both legs |
| `E3` nine distinct **non-ledger** lines, anchored whole-line | 1 | 9/9 | 9/9 | `live_agree=1` but `stripped_agree=0` → false |
| malformed rev | 2 | — | — | `runner_unreadable=1` on stderr |

E3 is the contract's "constant 9" attack realized: a guard that fabricates
9 hits on the live runner still dies on the ledger-stripped copy (9 vs 0). The
stripped leg is load-bearing, not decorative.

Structural reason, derived from `measure.py:38-40` (`strip_ledger` removes
exactly the lines `COMMAND_D.match` accepts) and confirmed by the matrix: to
satisfy `stripped_agree`, the guard must match **zero** lines of the stripped
text, so every line the guard matches must be a line the stripper removed,
i.e. a command-D line. With `live_d=9` and `depth_score=min(10,n)`, a passing
guard must hit all 9. No vacuous, constant, or offset-count guard passes; the
`min(10,n)` cap does not open a hole because the subset constraint is applied
to both legs.

## Residual risks (reported, not acted on)

1. **Canonical is hardcoded, not read from the contract.** `measure.py:17`
   compiles its own `COMMAND_D`; the contract's
   `no_harm_guard.depth_command_d_regex` is loaded only as the *guard*
   (`load_regex`, measure.py:44-55). Today all three literals are byte-equal
   (`SCORECARD.md:73` = `measure.py` COMMAND_D = contract), so "canonical
   command D" is honest. If SCORECARD's pattern were ever edited, the counter
   would keep scoring the old pattern and the guard would be compared against
   a stale canonical. The field name invites the confusion.
2. **`guard_absent` is a weak before-state.** Because the contract is missing
   at the base rev, the control asserts only that a missing contract cannot
   pass; it never exercises a *present but wrong* guard at the base rev. The
   guard-validity evidence comes from the matrix above, not from the control.
3. `mismatches=1` is hardcoded in the `guard_absent` branch (measure.py:83)
   rather than computed; it happens to agree with the two agreement flags
   (both 0). No impact on the control, but it is not independent arithmetic.

No predicate, contract, or counter edit was made. Lane checkout unmodified
(`git status --porcelain` before and after: ` M corpus/QUALITY.md` plus the
pre-existing untracked `.ufo/waves/round-39/*` files, all present at start).

## Tooling

No installs or upgrades. Commands used: `git show`/`git cat-file`,
`python3` stdin counts, and `measure.py` on the /tmp lab only.
