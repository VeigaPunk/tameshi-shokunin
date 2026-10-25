# RevQualityFalsifiers — criteria 83/84 falsifiers, wave 2 (falsify)

Seat: L1Tameshi43.RevQualityFalsifiers. Scope: run the falsifier commands in
`corpus/QUALITY.md` criteria 83 and 84 in scratch
`/tmp/tameshi-r43-w2-RevQualityFalsifiers-/`, report exit codes and decisive
lines, state for each whether the falsifier FAILS as the criterion promises.

Note on "as written": while this seat ran, the L1 landed freezes A11–A14
(HEAD moved e20cf89 → bb36f80 → 6b83a11), and `corpus/QUALITY.md` gained an
appended "Criterion 83/84 — falsifier correction" block (QUALITY.md:1107+).
Both the original falsifiers (QUALITY.md:1067–1079, 1099–1104) and the
corrected ones (QUALITY.md:1115–1126, 1135–1148) were executed. The original
criterion-83 command pins `--rev/--freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef`;
per the assignment and the permitted-revision rule the freeze of record
`3aee2c078f8976499b587086af3577fc94dc8cf1` was substituted for every
measurement run. The criterion's `cp .ufo/evidence/round-43/mutants/measure.py`
copies the mutable working tree; for attributable results the counter bytes
pinned by the freeze contract (`git show 3aee2c0:...` = sha256 `0d0f81bd…`)
were used, with working-tree runs reported separately.

## Criterion 83 — survivor classified, never relabelled

Verdict: **the falsifier FAILS as the criterion promises.** Flipping F12's
declared class does not relabel the dead-code survivor `killed`.

Commands as written (edit verified: exactly line 245
`{'expected': False, …}` → `{'expected': True, …}`, one diff line; first
`s.replace` is the no-op marker the correction notes):

```
python3 /tmp/…/m83-frozen.py --lane . --rev 3aee2c0… --freeze 3aee2c0…   → exit 1
```

Decisive line (full receipt `c83-frozen.stdout` in scratch):

```
fixtures_pass=11/12 run_errors=0 live_ok=3/3 live_unflagged_v4=0
mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0
dead_code_names=method_fold_several_returns
dead_code_cases=F12_method_two_returns dead_code_arg_ok=1
kill_fixture_reachable=1 … C1_R43_PASS=false
```
Load-bearing-gate check (the corrected falsifier,
`s.replace("if mf and reachable_fails:", "if mf:", 1)`, one match in every
counter version): all three counter generations measured at the freeze print
the flattering line — frozen `0d0f81bd`: `mutants_killed=6 dead_code_only=0`
(exit 1); A12 `3d1ff3dc`: `mutants_killed=6 dead_code_only=0` (exit 1);
A14 `601c1840`: `mutants_killed=6 dead_code_only=0` (exit 1). The gate is
load-bearing, not decorative. Control reproduction of the flattering line:
the pre-A5 counter at `17f6ef0c` (`ad7ecf8c`, `if mf: killed`, no gate) with
the same F12 edit, measured at the freeze → `mutants_killed=6 dead_code_only=0`.


Unmodified pinned counter at the freeze (baseline): exit 0,
`self_pin=1 … fixtures_pass=12/12 … mutants_killed=5 dead_code_only=1 …
C1_R43_PASS=true` (receipt `c83-frozen-unmod.stdout`).

### Findings

- **F-83a (operability, stale pin):** the original command pins
  `--rev/--freeze 17f6ef0c` — a pre-freeze A2/A3 commit, neither the base nor
  the freeze of record, so the falsifier as literally written is unrunnable
  under the round's permitted revisions. The appended correction pins
  `3aee2c0`. Also, `cp` of the working-tree counter makes output depend on
  when the copy happens: observed counter bytes moved `0d0f81bd` (freeze) →
  `b56a34d7` → `3d1ff3dc` → `601c1840` during the seat; a b56a34d7-byte run
  printed `mutants_killed=5 dead_code_only=1` but `mutants_sha_ok=0` because
  the `3aee2c0` contract predates the A11 `mutants_sha256` field — mixed
  counter/contract generations print `C1_R43_PASS=false` regardless of the
  falsifier's decisive fields.
- **F-83b (operability, incomplete corrected falsifier):** the corrected
  block's second command probes `/tmp/m83-applied.py`, which nothing in the
  block creates. Verbatim: `C1_R43_PROBE: verdict=runtime_error … errors=15
  first=["F01_attr_scratch exit=2 … can't open file '/tmp/m83-applied.py'…"]`,
  exit 1 — not the promised `dead_code_only`. Manufacturing it by applying
  the round-42 declaration (`if len(returns) != 1:` → `< 1:`) to
  `tools/write-path-census-v4.py` at `3aee2c0` gives
  `verdict=dead_code_only failures=1 reachable_failures=0` on both frozen and
  A14 counters, exit 1 (the probe returns 0 only for `killed`).

## Criterion 84 — self-assessment count uses the accepted pattern

Verdict: **the falsifier FAILS as the criterion promises** on its stated
mechanism; the newest standing command is census-valid and does not
under-count the indented mirror.

Commands as written (mirror in scratch, `| S001 |` → `  | S001 |`):

```
grep -cE '^\| S[0-9]{3} \|' /tmp/…/mirror-SOURCES.md        → 113, exit 0
grep -cE '^ {0,3}\| S[0-9]{3} \|' /tmp/…/mirror-SOURCES.md  → 114, exit 0
```

Decisive line: the lane's newest standing command
(SCORECARD.md:2081, round-43 block)
`grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` → **114** on the
indented mirror, equal to the census count N; the column-zero form prints
N−1 = 113. The superseded round-42 row (SCORECARD.md:2020) still prints the
column-zero command → 113 on the mirror, but it is labelled "the counter
reads the last standing row". Corrected block verbatim: prints
`column0=113 census=114`, `CRITERION-84-FALSIFIER-OK`, exit 0. Pristine
`corpus/SOURCES.md` (identical at `3aee2c0` and HEAD): 114 under both
patterns — the mirror is what makes the pattern load-bearing.

### Findings

- **F-84a (latent miscount, "same pattern" clause still falsified):** the
  standing pattern `^ {0,3}\| S[0-9]{3} \|` is narrower than the census
  parser in two dimensions the falsifier never exercises. Census parser
  `scripts/sources-census.sh:615-619` strips `^ {0,3}` then matches
  `^\|[ \t]*S[0-9]{3,}[ \t]*\|`. Mirrors built in scratch:
  - `|  S001 |` (two spaces after the pipe): standing command **113**,
    census-equivalent `grep -cE '^ {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|'` **114**.
  - `| S1001 |` (≥4-digit id): standing **113**, census-equivalent **114**.
  Registry ids already reach S159, so 4-digit ids are imminent. Today every
  row is `| S### |` and all patterns print 114 — latent, not active.
- **F-84b (which census pattern is "the contract's"):** CORPUS.md:135 prints
  the column-zero command `^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|` while
  CORPUS.md:152 says the maintained parser accepts 0–3 leading spaces — the
  contract text carries both readings; the standing command is equal to
  neither exactly.
- **F-84c (scope note):** the corrected-84 assertion only checks that the two
  *patterns* differ on the mirror; it never applies the standing command
  itself, so a future reversion of the standing row to column-zero is
  invisible to it — that check is delegated to C2 class m13.

## Retained evidence (scratch, deleted on cleanup)

`/tmp/tameshi-r43-w2-RevQualityFalsifiers-/`: `m83.py` (b56a34d7+flip),
`m83-frozen.py` (0d0f81bd+flip), `m83-preA5.py` (ad7ecf8c+flip),
`m83-ablate-{3aee2c0,HEAD,A14}.py`, `m83-applied.py` (built mutant),
`c83*.stdout/stderr`, `counter-{3aee2c0,HEAD,A14}.py`, `mutants.json`,
`tool-pristine.py`, `mirror-SOURCES.md`, `mirror-inner.md`,
`mirror-4digit.md`, `/tmp/mirror-SOURCES.md`.

## Tooling

No installs; pacman paused per directive, none needed (python3/grep/git only).

## Risks / blockers

- Lane drift during the seat (HEAD e20cf89→bb36f80→6b83a11; counter bytes and
  contract amended). All verdicts are stated against sha-anchored counter
  bytes at the permitted freeze; working-tree runs are labelled.
- `/tmp` scratch deleted on return; all decisive lines reproduced inline.
