# LedgerMatrixAppend — round-16 appended blocks, statement-by-statement

Seat: `TameshiR16.LedgerMatrixAppend` (wave 2, falsify; lane axes depth + calibration).
Lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; every file read at
`c699c8c36d6e4eca4b796b81a8247904aa145ec8` (`git show <rev>:<path>`); sibling reads
read-only via `git -C <repo> show`. `SKILL.md` sha256 at that commit =
`3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` (verified first,
`git show c699c8c:SKILL.md | sha256sum`). No installs; no background jobs; no subagents.

Attacked: (a) the append-only claim for the two files between `28aeef4` and `c699c8c`;
(b) every number, line/section reference and correction in the two appended blocks —
ledger `:403-413`, matrix `:527-547`; (c) the underlying evidence (`results.tsv`, per-defect
outputs, `sweep.log`, runner receipts, `predictions.json`, the pinned `round-gate.mjs`).

Two minor notes only (label/imprecision), no false claim found.

---

## 1. Append-only discipline — HOLDS (byte-prefix proof, not just numstat)

```
git diff 28aeef4 c699c8c --numstat -- corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/arm-class-matrix.md
23  1  corpus/knowledge/arm-class-matrix.md
13  1  corpus/knowledge/fleet-kill-rate-ledger.md
```

The two `1` deletions are **not** content deletions: both pre-append files ended without a
trailing newline, so the append rewrites the final line only to terminate it with `\n`.
Exact-byte proof, per file:

```
git show 28aeef4:$f > old ; git show c699c8c:$f > new
olds=$(stat -c%s old)
cmp -n "$olds" old new      # exit 0 → old bytes are an exact prefix of new bytes
```

| file | old lines/bytes (wc -l; old EOF unterminated) | new lines/bytes | old sha256 (16) | new sha256 (16) | net |
|---|---|---|---|---|---|
| fleet-kill-rate-ledger.md | 400 / 38 339 | 413 / 39 159 | `8f6daa81b3d86352` | `918a56d9c9ffb57b` | +12 lines |
| arm-class-matrix.md | 524 / 38 531 | 547 / 39 783 | `631873232e46f914` | `3580b23669b391d7` | +22 lines |

`git diff` flags the artifact explicitly:

```
\ No newline at end of file          (twice, once per file)
^--re-sweep and produces no new kill-rate or recorded case.        (ledger, old last line)
^--`knowledge/mutation-case-kimi-census.md` (E2 there).            (matrix, old last line)
```

The new files terminate with `\n` (`tail -c 2 | od -c` → `. \n`). Old bytes prefix-identical ⇒
nothing above the append was edited, only the EOF terminator added. **Holds.**

---

## 2. Ledger block (`corpus/knowledge/fleet-kill-rate-ledger.md:403-413`) — every claim

| # | statement | verdict | evidence |
|---|---|---|---|
| L1 | “Round 16 — seventh row appended (2026-10-20)” | holds | rows 1–4 are ledger `:45-48` (§1); rows 5–6 are ER-2 `:276-277`; next is 7. Date: commit `c699c8c` = `2026-10-20 10:49:37 -0300`; pre-registration `e69b488` = `2026-10-20 10:39:59 -0300`. |
| L2 | “The row for kumitate `round-gate.mjs` in the §5 queue said `unmeasured`.” | holds in substance; label note | Literal cell: ledger §3 `:109`, round-gate row — suite 60, pin `f890e277af83a78f`, state `unmeasured; hermetic` (identical at `28aeef4`). Census §5 “Tameshi's standing service offer” queue `:277-286`, round-gate row `:283`; census `:70-71` states the five remain unmeasured and “§5 is tameshi's standing offer to close them”. The ledger's own §5 (`:160-177`) has no queue, so “§5 queue” reads as the census §5 pointer that ledger §3 itself makes (“order per census §5 / R.4”). Minor note, not a false number. |
| L3 | leg `js-round-gate` | holds | `tools/mutate-and-run.sh@c699c8c`: `:91` (7/10 rate table), `:570` `TABLE_ROUNDGATE='A1:KILLED,…E1:SURVIVED'`, `:905` embedded spec, `:1219-1222` `regression_case_git js-round-gate`, `:1667` `js-round-gate:…:10:5`. |
| L4 | `--selftest`, 60 checks | holds | 60 `check('` registrations in the pinned mjs (`grep -c "    check('"` → 60). Executed pinned bytes: `ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS`, rc 0, empty stderr (control.out agrees: `[60/60] … 14 kinds observed`). |
| L5 | under the `env -i` guard | holds | `.ufo/evidence/round-16/round-gate/suite.txt` = `… exec env -i PATH="$PATH" HOME=… TMPDIR=… LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=… node "$MUTANT" --selftest`; identical string in `predictions.json.suite` and tool `:1221`. |
| L6 | **5/10 (50 %)** | holds | `sweep/results.tsv`: 10 rows, 5 `KILLED`, 5 `SURVIVED`; `runner-regression.txt`: `REGRESSION_SWEEP js-round-gate: … defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%`. |
| L7 | 5 kill-aimed / 5 hole-aimed | holds | `predictions.json.composition` = `{kill_aimed:5, hole_aimed:5}`; measured kill-aimed 5/5 killed (A1,A3,B1,E3,C1060), hole-aimed 0/5 (C1059,A2,B2,CKIND,E1). |
| L8 | 10/10 predictions held | holds | `results.tsv` predicted = measured for all ten; `REGRESSION_TABLE js-round-gate: match=10/10 … flips=0`. |
| L9 | survivors C1059, A2, B2, CKIND, E1 | holds | `results.tsv` rows C1059/A2/B2/CKIND/E1 = `SURVIVED` exit 0; description strings match `(:167)`, `(:617)`, `(:527)`, `(:175)`, `(:163)`. |
| L10 | CKIND “equivalent for gate behaviour” | holds | `FINDING_KINDS` has exactly two readers in the pinned file: `:171` (definition) and `:1488` (meta-check filter). Dropping `TREE_DIRTY` changes no output path; CKIND out: 60/60, exit 0. |
| L11 | E1 `UFO_SRC` set-value | holds | results row E1 `SURVIVED`, exit 0, 60/60; desc `unreached arm: UFO_SRC set-value branch resolves the canonical candidate instead (:163)`. |
| L12 | sweep `2026-10-20T13:40:15Z` | holds | `sweep/sweep.log`: `MUTATE_DATE: 2026-10-20T13:40:15Z`. |
| L13 | runner `75ed934d…` | holds | `sweep.log`: `MUTATE_TOOL: …/tools/mutate-and-run.sh sha256=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`. That is exactly `git show 606716f:tools/mutate-and-run.sh \| sha256sum` — i.e. the pre-landing committed tool. |
| L14 | rev `364f1d5` | holds | full `364f1d5954158ef8844bca4a5fef57b05d2f2ca5`; `predictions.json.rev`; `REGRESSION_PIN js-round-gate: rev=364f1d5…`; also the last-touching commit of `scripts/round-gate.mjs` (`git log -1 -- <path>`). |
| L15 | sha256 `f890e277…d3e9` | holds | full `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`; 1 511 lines / 80 415 B; git blob `1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3`; blobs at `175de6ba`, `1770305`, `364f1d5` all identical. |
| L16 | detail of record `mutation-case-kumitate-round-gate.md` | holds | file present at `c699c8c`; its §0/§2/§5 rows reproduce every ledger cell above. |
| L17 | Receipt `REGRESSION: PASS (cases=7 passed=7 …)` | holds | `runner-regression.txt` exact: `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)`, `rc=0`; `REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`. |
| L18 | at runner `89722ddb…` | holds | `runner-sha256.txt`: `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594  tools/mutate-and-run.sh`; `c699c8c:tools/mutate-and-run.sh` hashes to the same value. Both “runner” shas are real and belong to different revisions: sweep ran the `606716f` blob (`75ed934d…`), the receipt ran the landing blob (`89722ddb…`); `c699c8c` is precisely the commit that adds leg 7 (diff `+7/−2` … `+TABLE_ROUNDGATE`), and the timestamps run 13:40:15Z → 13:41:49Z. |

Ledger block: **18/18 hold**. Only note is L2's “§5” label (referent is census §5; the literal
`unmeasured` cell is ledger §3 `:109`).

---

## 3. Matrix errata (`corpus/knowledge/arm-class-matrix.md:527-547`) — every assertion

| # | assertion | verdict | evidence |
|---|---|---|---|
| M1 | “§13 was a projection (`no mutant was cut`, `:300-303`; PU1 `:475`)” | holds | `:302` contains “no mutant was cut”; `:475` is `- PU1 — all of §13 is static; the interval statement (13.4) is a hypothesis until a mutant lane cuts it.` |
| M2 | “Round 16 cut ten mutants on the same bytes (`f890e277…d3e9`, rev `364f1d5`)” | holds | §13's pin at `:301` is `f890e277…a834d3e9` (kumitate `175de6ba`); blobs at `175de6ba`/`1770305`/`364f1d5` are identical; sweep `defects=10` at the same sha. |
| M3 | “§13.2 full-line vs prefix pins (A1 and A3 killed, rt8 green under A3)” | holds | A1 `KILLED`; A3 `KILLED` — `A3.out` FAILs `[52]` rt1 full-line and `[53]` rt2 full-line, while `[59]` rt8 PASSes with the swapped tail (`… checked=2 warnings=0 errors=0`); rt8 is the prefix regex at `:1481`. |
| M4 | “§13.3 species asymmetry (B1 killed, B2 survived)” | holds | B1 `KILLED` (`[32]` fcA, `[45]` jFc); B2 `SURVIVED` exit 0, 60/60. |
| M5 | “§13.4 interval [26,1059] (1059 survived, 1060 killed)” | holds | C1059 `SURVIVED` 60/60; C1060 `KILLED` — `[8]` fails with `kinds=[REPORT_THIN,REPORT_ROUND_MISMATCH]`. Fixture arithmetic independently confirmed: `fxMentions(10,'round-1')` = **1059 B**; `fxThin(5)` = **25 B**. |
| M6 | “§13.4 one-sided meta-check (CKIND survived)” | holds | CKIND exit 0, 60/60; enum readers only `:171`/`:1488` (see L10). |
| M7 | “§13.5 #1 detail tail (A2 survived)” | holds as measurement | A2 exit 0, 60/60. (See residual note R2 about §13.5 #1's wording.) |
| M8 | “§13.6 #5 `UFO_SRC` (E1 survived)” | holds | E1 exit 0, 60/60; spec edit at `:163`. |
| M9 | “The ten pre-registered predictions all held.” | holds | `results.tsv` all 10 match; runner table `match=10/10`. |
| M10 | “meta-check equality is at `:1490` (block `:1487-1493`), not `:1489`” | holds | `:1490` = `ok: missing.length === 0,`; `:1489` = `return {`; block `:1487` `check('every declared finding kind…` … `:1493` `});`. §13.4 `:408` indeed cites the equality at `:1489`, so the correction is valid. |
| M11 | “§13.6 omits five arms that no fixture reaches: `:401`, `:425`, `:436`, `:477`, and the main-external citation branch `:377-378`” | holds | None of those refs appear in §13.6 (`:434-456`). Fixture-set proof from the pinned mjs: (a) `fxLaneRepo` writes `SCORECARD.md` and `LOG.md` unconditionally (`:761-762`), so `readText` cannot be null ⇒ `:401`/`:425` never fire; no fixture unlinks them (only `rmSync` is `:1495`, tmp teardown). (b) Every lane repo commits (`:763-771`); `commit:false` is never passed ⇒ `git log` (`:434`) succeeds ⇒ `:436` never fires. (c) `fxCloseFixture` writes the report inside `main/.ufo/reports/…` (`:813-818`) and every `--close` call uses `closeArgs()` on such a fixture; `rt6` is `--tracked`, hitting `:546-547`, not `:477`. (d) Citation tokens resolve lane (`r23` side branch), origin (`r24`, derived `rn`/`rl`, derived-none), or unresolved (`r22` `deadbeef1234`); no main-only token ⇒ `probe('main')` at `:377-378` unreached. |
| M12 | “§13.1's ‘every arm statically covered’ for REPORT_UNTRACKED is false (`:477`)” | holds | §13.1 lists the five arms at `:350` (`:477`, `:481`, `:495`, `:547`, `:551`) and claims at `:353-354` “every arm statically covered”. Coverage: `:481` ← r28, `:495` ← r29, `:547` ← rt6, `:551` ← rt2; `:477` (close-mode outside) has no fixture (M11c). |
| M13 | “`:370` is false: rt3 (`:1436`) pins the NO_FILED_REPORTS detail tail.” | holds | `:370` reads “the detail tail is unread except fcE's `exit 128` probe”. `rt3` asserts the token at `:1435` **and** `/filed=1 round-<N>\/kumitate\.md/` at `:1436`; control output `[54/60]` prints `… FAIL-CLOSED (NO_FILED_REPORTS) filed=1 round-<N>/kumitate.md under …`, i.e. the tail is read. |
| M14 | “`:445-446` is false: `parseArgs` (`:630`) runs before the selftest dispatch (`:635`), so the nested `KUMITATE_LANE` does reach env validation.” | holds | `main()` `:630` `opts = parseArgs(process.argv.slice(2));`, then `:635` `if (opts.selftest) return selfTest();`; env-lane validation is inside `parseArgs` (`:275-281`). The nested run sets `KUMITATE_LANE: 'not-a-lane'` (`:1389`) and passes no `--lane`. Executed proof (below): an invalid env lane with `--selftest` exits 64 with the env-validation message, so validation does run before selftest; with `--lane` supplied, env validation is bypassed and the suite runs. |

Matrix errata: **14/14 hold**.

---

## 4. Executed anchors (commands, exits, key lines)

1. Pinned bytes, hermetic selftest (`/tmp` copy of `git show 364f1d5:scripts/round-gate.mjs`, sha256 `f890e277…d3e9`):
   ```
   env -i PATH=… HOME=… TMPDIR=… LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=… \
     node round-gate.mjs --selftest
   ```
   → `rc=0`; tail `PASS [60/60] every declared finding kind fires in at least one fixture — 14 kinds observed`, `ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS`; stderr 0 bytes.
2. Env-validation ordering (M14):
   ```
   env -i … KUMITATE_LANE='bad lane' node round-gate.mjs --selftest
   ```
   → `rc=64`, stderr: `round-gate: KUMITATE_LANE must match ^[A-Za-z][A-Za-z0-9-]*$ (got "bad lane")`.
   ```
   env -i … KUMITATE_LANE='bad lane' node round-gate.mjs --selftest --lane kumitate
   ```
   → `rc=0`, `ROUND_GATE_SELFTEST: 60/60 pass` / `VERDICT: PASS` (env path bypassed by the flag).
3. Check count: `grep -c "    check('" round-gate.mjs` → 60.
4. Fixture sizes: Python evaluation of the exact template strings → `fxMentions(10,'round-1')` = 1059 B, `fxThin(5)` = 25 B (M5).
5. Evidence files read at `c699c8c`: `sweep/results.tsv`, `sweep/sweep.log`, `sweep/spec.copy`, `sweep/evidence/{control,A1,A3,B1,B2,C1059,C1060,CKIND,E1,A2}.out`, `predictions.json`, `round-gate.defects.spec`, `suite.txt`, `runner-{sha256,regression,selftest}.txt`.
6. Spec pin: `sha256(round-gate.defects.spec)` = `sha256(sweep/spec.copy)` = `e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4`, equal to `predictions.json.spec_sha256`.
7. Pre-registration ordering: `e69b488` committer date `2026-10-20 10:39:59 -0300` (13:39:59Z), sweep `13:40:15Z`; `e69b488` is an ancestor of `c699c8c` (`merge-base --is-ancestor` exit 0).

---

## 5. Minor notes / residual risk (none falsifies an appended claim)

- **R1 — “§5 queue” label (L2).** The ledger's own §5 is the instrument section, which has no
  queue; the literal `unmeasured` cell is §3 `:109`. The census §5 standing-offer queue
  (`fleet-suite-census.md:283`) is the queue the ledger §3 points at, and the unmeasured status
  is stated at census `:70-71`, not in the row itself. Substance holds; the section label is
  ambiguous. One-word fix for a future append: “§3 queue” (ledger) or “census §5 queue”.
- **R2 — §13.5 #1 retains the `:370` falsehood, uncorrected.** Matrix `:422-423` still says
  “the path/detail remainder and the stderr line are read by nothing”; `rt3` reads the
  NO_FILED_REPORTS remainder (M13). The errata cites §13.5 #1 only as a *measurement*
  (“A2 survived”), which is true, and its `:370` bullet supplies the counterexample — so no
  assertion in the append is false — but a reader can take the measured line as leaving
  §13.5 #1 intact. Recommend a one-line appended correction in the next wave; not blocking.
- **R3 — truncation style.** `f890e277…d3e9` is a 4-hex suffix of a sha256 whose last 8 are
  `a834d3e9`; unambiguous against the full hash and consistent with `mutation-case-kumitate-round-gate.md`.
  No collision risk observed.
- **R4 — two “runner” identities are both correct.** `75ed934d…` is the pre-landing committed
  tool (`606716f` blob), `89722ddb…` is the landing tool (`c699c8c` blob); the ledger names each
  in its own context (sweep vs receipt) and both hash checks passed. Not a contradiction, but a
  reader comparing the two cells must not flatten them.

Not done: the ten-mutant sweep was not re-run (verdicts were re-read from the recorded
per-defect outputs and runner receipts at the same bytes); no sibling gate was executed or
edited; other seats' reports were not opened.

**Verdict: holds** — append-only is a byte-exact prefix append (the two −1 lines are EOF-newline
rewrites), and all 18 ledger statements and 14 matrix-errata assertions check out against the
repo and sibling evidence; two minor notes (R1 label, R2 residual uncorrected wording), neither
a false claim.
