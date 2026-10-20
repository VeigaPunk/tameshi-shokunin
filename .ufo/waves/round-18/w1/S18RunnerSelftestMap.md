# S18 — mutate-and-run.sh leg-8 invariant map

Scope: `tools/mutate-and-run.sh` at `183f87b899e6cae46be98d251cbc87fb5118f6ca`
(1866 lines, blob sha256 `fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a`).
Question: every line that must change so the eighth leg (`js-sources-check`) is
counted everywhere. Line numbers below are from the committed bytes only.

Evidence commands (all from `/tmp`, GIT_* scrubbed, scratch under
`mktemp -d /tmp/tameshi-r18w1-S18RunnerSelftestMap-*`):

```
$ git -C <lane> show 183f87b…:tools/mutate-and-run.sh > /tmp/S18-map.sh
$ sed -n 's/^  local nlegs=\([0-9][0-9]*\) .*/\1/p' /tmp/S18-map.sh      -> 7   (rc=0)
$ grep -cE '^  regression_case_git (js|bash)-' /tmp/S18-map.sh          -> 7
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
    bash $B/mutate-and-run.sh --selftest | tail
  PASS embedded leg specs: seven files written
  PASS leg-count agreement: calls=7 specs=7 nlegs=7 (want 7)
  PASS leg-count agreement: selftest leg tuples=7 (want 7)
  MUTATE_SELFTEST: 95/95 pass ; VERDICT: PASS ; exit 0
```

Positive simulation (stub leg 8: 2-defect spec, `TABLE_SOURCES='S1:KILLED,S2:SURVIVED'`,
tuple `…TABLE_SOURCES:2:1`, all edits listed below): `MUTATE_SELFTEST: 96/96 pass`,
`PASS leg-count agreement: calls=8 specs=8 nlegs=8 (want 8)`, `PASS … tuples=8 (want 8)`,
`PASS embedded leg js-sources-check: spec and recorded table agree`, `VERDICT: PASS`, exit 0.
So +1 selftest check is the expected delta over the 95/95 baseline.

## A. Mechanical checklist — every committed line that must change

`R` = required (a count/list/aggregate that leg 8 perturbs); `D` = documentation in the
same file that the header contract claims must stay true (not asserted by the selftest).

| # | Committed line(s) | Kind | Required change |
|---|---|---|---|
| 1 | `14-15` | D | header: "r16 … adds the seventh measured gate" → record r18 adding the eighth (`scripts/sources-check.mjs`). |
| 2 | `81` | D | `--regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven)` → add `r18 eight`. |
| 3 | `85-91` | D | leg ledger table: append `js-sources-check  kumitate-shokunin/scripts/sources-check.mjs  <killed>/10 (<pct> %)`. |
| 4 | `92-103` | D | sources paragraph: add the leg-8 evidence/spec source; `All seven defect specs` (98) → eight; the "leg 7's spec …" provenance sentence (96-103) needs a leg-8 sibling. |
| 5 | `150-155` | D | selftest description "(r16 extends it to seven legs)" → eight. |
| 6 | `202-204` | D | usage leg enumeration `(js-kimi-census, … js-round-gate)` must include `js-sources-check`. |
| 7 | `588-589` | D | expectations comment "leg 7 (js-round-gate) was measured in round 16" → add leg 8 provenance. |
| 8 | after `605` | R | add `PIN_SOURCES=6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` and `REV_SOURCES=0acb7752d19058b953ebbeba253b1e35f6548de5`. |
| 9 | after `612` | R | add `TABLE_SOURCES='<ID:KILLED|SURVIVED,…>'` — must be a **top-level global** (the selftest's `${!ltbl}` indirect expansion runs in the same process). |
| 10 | `640` | D | `regression_specs() { # <dir> — write the seven embedded case specs` → eight (or "the embedded case specs"). |
| 11 | after `1005` (js-round-gate `EOT`) | R | new `cat >"$d/js-sources-check.spec" <<'EOT' … EOT` — the round-16-procedure 10-defect spec, verbatim; **exactly 5-colon-free ids**, one `@defect/@old/@new` per defect. This is the leg-8 spec the tuple's counts are checked against. |
| 12 | `1006-1009` | R | extend the `[[ -s "$d/js-kimi-census.spec" && … ]]` chain with `&& -s "$d/js-sources-check.spec"`. This chain is the only content assertion on the specs: omit it and an unwritten 8th spec still counts in `lfiles`. |
| 13 | `1236` | R | `REGRESSION_EXPECT` format string: append ` js-sources-check=%s/%s` before `\n`. |
| 14 | after `1243` | R | two more printf args: `"$(table_count "$TABLE_SOURCES" KILLED)" "$(table_total "$TABLE_SOURCES")"`. |
| 15 | `1245` | R | `local st_js … st_roundgate` → add `st_sources`. |
| 16 | after `1280` (`st_roundgate=$?`) | R | new `regression_case_git js-sources-check \` + `'kumitate-shokunin/scripts/sources-check.mjs' "$PIN_SOURCES" "$REV_SOURCES" \` + `"$specs/js-sources-check.spec" 'node "$MUTANT" --selftest' "$TABLE_SOURCES" \` + `"$root/js-sources-check"` + `st_sources=$?`. The call line **must start with exactly two spaces and the name must start `js-`** — that is the `lcalls` grep pattern (`1793`). |
| 17 | `1282` | R | `local nlegs=7` → `local nlegs=8`; the line must stay the **only** match for `^  local nlegs=` (the selftest's `sed` at `1795` collects every match; duplicates produce `8\n8` → `arithmetic syntax error`, observed rc=1). |
| 18 | `1283` | R | `for st in …` list: add `"$st_sources"` (see gap G1 — unguarded). |
| 19 | `1776-1782` | D | selftest comment "r16 adds leg 7: the seven embedded legs' specs…" → eight. |
| 20 | `1787` | R | `st 'embedded leg specs: seven files written'` → `eight` (message only; the status comes from `regression_specs`, which passes once #11/#12 land). |
| 21 | `1796` | R | `[[ "$lcalls" -eq 7 && "$lfiles" -eq 7 && "$lnlegs" -eq 7 ]]` → all three `-eq 8`. |
| 22 | `1797` | R | `(want 7)` → `(want 8)` in the agreement `st` message. |
| 23 | after `1805` | R | `lent` tuple: `'js-sources-check:js-sources-check.spec:TABLE_SOURCES:10:<killed>'` — **exactly five `:`-fields** (`IFS=:` into name/spec/table/total/killed); `<killed>` must equal `table_count TABLE_SOURCES KILLED`; `10` must equal the spec's defect count *and* `table_total`. |
| 24 | `1807` | R | `[[ ${#lent[@]} -eq 7 ]]` → `-eq 8`. |
| 25 | `1808` | R | `(want 7)` → `(want 8)` in the tuple `st` message. |

Not required (precedent): `164 VERSION='mutate-and-run.sh r10-2 …'` stayed unchanged when
r16 added leg 7 [observed: lines 14-15 claim r16 eight-leg-era work while VERSION is r10-2].

No change needed (verified dynamic): `1793` c= for call sites, `1794` `find` for spec files,
`1795` sed for nlegs, the `lent` loop body `1809-1826`, `REGESSION_BAND` `1234-1235`,
summary printfs `1291-1310` (they take `$nlegs`), and the `--regression` output map.

## B. Exact strings the L1 should see after installing the staged copy

Staged copy run (any `/tmp` cwd, `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`):

```
PASS embedded leg specs: eight files written
PASS leg-count agreement: calls=8 specs=8 nlegs=8 (want 8)
PASS leg-count agreement: selftest leg tuples=8 (want 8)
PASS embedded leg js-sources-check: spec and recorded table agree
MUTATE_SELFTEST: 96/96 pass        (>=96 if other seats add checks)
VERDICT: PASS                       (exit 0)
```

Runtime (fleet-mirror clone, `/tmp`): `REGRESSION_EXPECT:` line ending
`js-sources-check=<killed>/10`, every leg PASS, and
`REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`.
The selftest cannot prove the spec's `@old` strings occur once — only the leg's own
sweep does (`count==1` is asserted during sweep preparation); **run `--regression`.**

## C. Guard gaps — greps that will not catch a bad staged copy

**G1 (proved).** Dropping `"$st_sources"` from the `for st in` list (`1283`) is invisible:
a copy with the full leg-8 wiring but the 7-entry for-list ran `MUTATE_SELFTEST: 96/96 pass`,
`VERDICT: PASS`, exit 0 — while at runtime it would print `REGRESSION: PASS (cases=8 passed=7 …)`.
The agreement check compares declarations, not the accumulation list. **Grep the staged
copy for `$st_sources` in both `1245` and `1283`**, and check `passed=8` (not just `cases=8`).

**G2 (proved).** `REGRESSION_EXPECT` format/args are unbalanced silently: bash `printf`
reuses the format when args remain (`a=%s/%s` ×2 args → two lines) and emits empty `%s`
when args are short — no exit change. Count the substitutions: 8 legs → 8 `=%s/%s` groups
and 16 args; a stray extra pair prints a duplicate `REGRESSION_EXPECT:` line.

**G3 (proved).** `st_sources=$?` omitted → `set -u` aborts the selftest with
`st_sources: unbound variable` (exit non-zero), so this one self-reports.

**G4.** The tuple check validates **ids, total, KILLED count, SURVIVED count** only
(`1817-1824`); it does not validate verdict values against the recorded case, nor the
predictions in the spec comments. A doctored `TABLE_SOURCES` that keeps the same counts
(e.g. swaps which id is killed) passes `--selftest` and only fails in the real sweep.

**G5.** `TABLE_SOURCES` defined only inside `run_regression` (e.g. `local`) → `${!ltbl}`
is empty → `table_total` prints 0 → `embedded leg js-sources-check: spec and recorded
table agree` FAILs (observed empty-table behaviour: `[[ 0 -eq 10 ]]` false, no hard error).
So a missing global does self-report; a *stale* value would not.

## D. State at mapping time

`.ufo/waves/round-18/staged/` did not exist; `find …/round-18/staged -type f` returned
nothing, so X02RunnerLeg8's staged copy was not written yet when this map was taken.
Diff it against checklist A #8-#25 (the `R` rows) and run §B.

Verdict: built — 16 required and 9 documentation line-changes mapped, positive 8-leg simulation passes 96/96, and two proven silent-failure arms (`$st_sources` for-list, `REGRESSION_EXPECT` arg count) are flagged for manual review of the staged copy.
