# T48W2ExecC1ProbeB — C1 probe group B (four standing rows, content revision)

Seat: T48W2ExecC1ProbeB (round 48, a2w1, calibration axis / C1 feed). Read-only on the lane; one
scratch root `/fast/scratch/hyaku/tameshi-r48/T48W2ExecC1ProbeB`, deleted before this report was
finished. No subagent, no install, no mutating git/jj command, no control scoring, no deciding run.

- Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, worktree HEAD `17cc5ce141868454d05bf75ef5cd230e35f0cdf4`
  (dispatch commit on top of the content revision; the diff is `.ufo/` only).
- REV `c7586b9a10effc63b4bd327f976edc094c1bdc17`, BASE `473336d9d789f6081195e7376d17836a24666bc3`.
- Counter `.ufo/evidence/round-48/calibration/measure.py`, sha256
  `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` — equals the freeze-2 digest
  (`freeze-2.json:counters.calibration/measure.py.sha256`), and the counter's own `self_pin=1`.

## The item's four statements and what each attack touches

All four rows are data rows of the one cap table that begins at `SCORECARD.md:2330`
(`| Capability | What it can now do | Evidence pointer | First-working round |`), i.e. kind `cap`
under amendment 6. The standing row is the last row in file order carrying `runs 3`; there is no
later row for any of the four ids (grep for `^| <id>` returns 2334-2337 last).

| # | statement id | row | row declares | attacks |
|---|---|---|---|---|
| 1 | six-leg regression ledger | `SCORECARD.md:2334` | V={`REGRESSION: PASS (cases=9 passed=9`,`0`}, `stable`, sha `a7d3f2dd7d47`, deps `fleet-root,node` | V, class, sha, D, attestation |
| 2 | repeated pristine-control gate | `SCORECARD.md:2335` | V={`SELFTEST: PASS (29 cases)`,`0`}, `stable`, sha `296fe566dc59`, deps `none` | V, class, sha, D |
| 3 | six-leg content-disposition probe | `SCORECARD.md:2336` | V={`SELFTEST: PASS (19/19)`,`0`}, `stable`, sha `331529eadafe`, deps `none` | V, class, sha, D |
| 4 | exposed witness provenance correction | `SCORECARD.md:2337` | V={`SELFTEST: PASS 39/39`,`0`}, `stable`, sha `df3390682a04`, deps `none` | V, class, sha, D |

Each row is attacked on five axes: (A1) every P0 (line, exit) tuple of three rounds × six profiles is
a member of V; (A2) the class label matches the member count; (A3) the 12-hex tool prefix equals the
blob at REV; (A4) D holds every dependence observed in all three rounds and no dependence observed in
none; (A5) each member is attested by the counter's own P0/P1 observation in this invocation (or an
EXTRA). A sixth axis is the instrument itself: does the counter observe what it prints (re-derived
below, outside the counter's own code).

## The probe (explicitly not a verdict)

```bash
S=/fast/scratch/hyaku/tameshi-r48/T48W2ExecC1ProbeB; export TMPDIR="$S"
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 \
  --base 473336d9d789f6081195e7376d17836a24666bc3 \
  --work "$S/w" \
  --only "six-leg regression ledger,repeated pristine-control gate,six-leg content-disposition probe,exposed witness provenance correction"
```

Wall 18 m 29 s (`start=2026-10-26T13:29:59Z end=2026-10-26T13:48:29Z`), exit 1 — which is the
`--only` path's designed exit (`measure.py:574`: `passed` requires `not only`). stderr empty.
Receipts: `T48W2ExecC1ProbeB.stdout` (sha256 `9a18bfde6e2a7b6e9c8c057f4d61f7e7066059a77202ab7ef3afa8a65cd61974`,
24 lines, byte-identical copy of the run's stdout), `.time`, `.stderr` (0 bytes). Disk guard checked
before the pass (`/fast/scratch/hyaku 23% used, 621 G free`); no ENOSPC.

Verdict line, verbatim:

```
C1_R48_PARTIAL: self_pin=1 stmts_pin=1 statements=4 rounds=3 append_only=1 unpinned=0 total=0 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=1 base=473336d9d789f6081195e7376d17836a24666bc3 rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C1_R48_PASS=false
```

`C1_R48_PASS=false` here is the probe label's arithmetic (`statements=4`, `--only`), never evidence
about the claim; the full-invocation verdict is the L1's deciding run.

## STATEMENT lines, verbatim (all four)

```
STATEMENT cap/six-leg regression ledger: claimed=REGRESSION: PASS (cases=9 passed=9|0 sha=a7d3f2dd7d47 ROUNDS r1=REGRESSION: PASS (cases=9 passed=9|0 r2=REGRESSION: PASS (cases=9 passed=9|0 r3=REGRESSION: PASS (cases=9 passed=9|0 DEPS required=fleet-root,node unstable=bwrap never=env,jj declared=fleet-root,node MATCH DEPS-OK
STATEMENT cap/repeated pristine-control gate: claimed=SELFTEST: PASS (29 cases)|0 sha=296fe566dc59 ROUNDS r1=SELFTEST: PASS (29 cases)|0 r2=SELFTEST: PASS (29 cases)|0 r3=SELFTEST: PASS (29 cases)|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT cap/six-leg content-disposition probe: claimed=SELFTEST: PASS (19/19)|0 sha=331529eadafe ROUNDS r1=SELFTEST: PASS (19/19)|0 r2=SELFTEST: PASS (19/19)|0 r3=SELFTEST: PASS (19/19)|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT cap/exposed witness provenance correction: claimed=SELFTEST: PASS 39/39|0 sha=df3390682a04 ROUNDS r1=SELFTEST: PASS 39/39|0 r2=SELFTEST: PASS 39/39|0 r3=SELFTEST: PASS 39/39|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
```

**No MISMATCH, no DEP-MISMATCH, no UNATTESTED, no OVERSIZE, no UNPARSED, no UNOBSERVABLE.** There is
therefore no row my run contradicts at P0, and no tuple to report under those heads. `attested_extra=0`:
no EXTRA line was printed, because for a single-member V the extras loop is gated on a *missing*
member (`measure.py:531-540`), and every member was observed at P0 in all three rounds.

Fleet state, verbatim summary (four points): `census_sha=3fb7261569f4` at every point,
`lane_clean=1` at every point, `fleet_drift=0`. `sibling_moves=1`: `souji-shokunin` HEAD
`4e56c48b8fc8` (point 1) → `9da5e9a559f7` (point 2) → `4ea897fe95d5` (points 3-4). Disclosed by
amendment 5 as
`sibling_moves`, not drift; the ledger legs replay blob-pinned sources, so a moved sibling HEAD is not
drift.

### Did a `nondeterministic` row see more than one member?

No row in my group is declared `nondeterministic`, so the question is answered per row from the six
profiles of each round:

- Rows 2-4 (the three selftests): exactly one member at all six profiles in all three rounds
  (18 observations each, character-identical).
- Row 1 (six-leg regression ledger): my run saw **two** members — `REGRESSION: PASS (cases=9 passed=9|0`
  at P0, P1, P3 in every round and at P2 in rounds 1-2, and `REGRESSION: FAIL (cases=9 passed=8|1` at
  **P2 of round 3** (round-3 PROFILES line, verbatim, in the receipt):

  ```
  ROUND 3
  PROFILES six-leg regression ledger: P0=REGRESSION: PASS (cases=9 passed=9|0 P1=REGRESSION: PASS (cases=9 passed=9|0 P2=REGRESSION: FAIL (cases=9 passed=8|1 P3=REGRESSION: PASS (cases=9 passed=9|0 P4=REGRESSION: SETUP (cases=9 passed=4|2 P5=REGRESSION: SETUP (cases=9 passed=0|2
  ```

  That FAIL tuple is outside the row's V, but it is a P2 tuple, and the contract constrains P0 tuples
  (and admits P0/P1 for attestation) — so the counter correctly scored it as a dependence, not a
  mismatch: `unstable=bwrap`.

## Findings

### F1 — the row's `stable` is one draw away from falsification, and my probe drew the other member 20 minutes after the row was written

- **Attacks:** `SCORECARD.md:2334` (V = PASS|0 only, class `stable`) vs. the statement's own value
  distribution; the predicate's `mismatches` term.
- **Observed:** 1 of the 12 evaluable leg invocations in my probe printed
  `REGRESSION: FAIL (cases=9 passed=8|1` (P2, round 3, 13:42:27Z per the observation receipt's
  `REGRESSION_DATE`). Evaluable = P0-P3 × 3 rounds = 12; P4/P5 are the deterministic `SETUP` profiles
  in every round. Rate 1/12 = 8.3 %, consistent with the lane's own ~10 % (4/40,
  `.ufo/waves/round-48/w1/T48RevenRegression.md` §1.4).
- **Mechanism in my receipt** (copied here because the scratch dir is deleted), the failing leg block
  of `.ufo/waves/round-48/a2w1`'s run, work dir
  `…/w/round3/P2/obs-six-leg-regression-ledger.stdout`:

  ```
  REGRESSION_SWEEP bash-tsukuroi-census: MUTATE: DONE (target=bash-tsukuroi-census defects=10 killed=7 survived=3 inconclusive=0 kill-rate=70%)
  REGRESSION_DEFECT bash-tsukuroi-census B8: measured=KILLED recorded=SURVIVED
  REGRESSION_TABLE bash-tsukuroi-census: match=9/10 recorded-killed=6 measured-killed=7 survived=3 inconclusive=0 flips=1
  REGRESSION_CASE bash-tsukuroi-census: FAIL (out of band: killed-delta=1 flips=1; log: …/w/round3/P2/regression-wd/bash-tsukuroi-census/sweep.log)
  ```

  and in that leg's `sweep.log`, `CONTROL: GREEN (exit=0 duration-ms=4339 pristine-sha256=084951be50bc…)`,
  then `DEFECT B8: KILLED (exit=1 duration-ms=4735) tsukuroi-census.sh:935` with
  `TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 25 passed, 1 failed)`. One-sided SURVIVED→KILLED flip,
  same leg and same direction as the lane's root-cause report (its mutant index was B7; mine B8 — the
  `sweep.log` for B8 prints only the seven PASS case lines, so I do not name the failing case).
- **Why this matters for the claim, not just for the row:** the deciding invocation constrains P0
  tuples only (`measure.py:526` reads `observed`, built from P0 cuts at `measure.py:499-500`). This row
  contributes three P0 draws per invocation. At my observed rate the chance that at least one P0 draw
  lands the excluded member is 1-(11/12)^3 = **23 %**; at the documented 10 % it is
  **27 %**. One such draw is one `mismatches` count, i.e. `total>0`, i.e. `C1_R48_PASS=false` — the
  contract's kill rule, and by its own words "a flaky deciding observation outside V is a mismatch,
  not a rerun". Extras cannot rescue it: extras only fire when a *member* is missing.
- **Not a contradiction of the row by my run.** My run's P0 tuples were PASS|0 in all three rounds, so
  the row is unattacked on P0 by me. What I measured is the exposure, live on this host, inside the
  probe window. The SCORECARD prose already discloses the nondeterminism (`SCORECARD.md:2328`); the
  disclosure is honest and the row is letter-compliant — but the letter-compliant row is a ~1-in-4
  liability for the claim it carries.

### F2 — `unstable=bwrap` is flake noise, not a bwrap dependence (instrument reading, no breach)

- **Attacks:** the dependence rule at `measure.py:499-513` (variant tuple ≠ that round's P1 tuple ⇒
  dependence; `required` = intersection over rounds, `never` = names never differing,
  `unstable` = difference).
- **Observed:** my run printed `unstable=bwrap` for row 1 solely because round 3's P2 tuple was the
  race FAIL. `bwrap` is not on this statement's path: the FAIL is inside the pinned
  `bash-tsukuroi-census` sweep, and the only leg-shaped consumer of `bwrap` in the lane is
  `tools/env-diff.py`, which is a different statement. Counter-check inside my own receipt: P3
  (`jj` dropped) was PASS in round 3, so the same round's other variant was clean.
- **Consequence:** none for the predicate — the contract lets a row declare or omit an `unstable`
  dependence, and `DEPS-OK` is correct here. The residual risk is the other direction: a dependence
  can only enter `required` by differing in all three rounds (≈0.1³ per name), so the declared set is
  robust; but a reader of the STATUS line may read `unstable=bwrap` as evidence about bwrap. It is
  evidence about the host.

### F3 — the dep vocabulary cannot name the dependence that actually moves this statement

- **Attacks:** `measure.py:87` `DEP_NAMES = ('bwrap','env','fleet-root','jj','node')` against the
  contract's "D contains every dependence observed in all 3 rounds" (`contract.json:86`).
- **Observed:** the dependence that produces the FAIL member is host state read at observation time
  by a pinned fleet leg. In my receipt the surrounding case text of the same sweep shows
  host-sensitive assertions (`FAIL degraded: enabled timer not armed (drift): plane evidence missing:
  '^PLANE journal: DEGRADED .*timer_drift=1 .*\(ai-usage\.timer=inactive\)'; got: PLANE … (ai-usage.timer=inactive)`)
  and `.ufo/waves/round-48/w1/T48ExecObs2.md:§"Where the six-leg flake lands"` records
  `nvidia-smi`/plane-evidence reads in the same leg. `env` here means only "P0 differs from P1"; host
  state is identical across all six profiles, so it is invisible to every name in the vocabulary.
- **Consequence:** the row's D is complete *relative to a closed five-name alphabet*, and incomplete
  as a description of what the statement depends on. Letter-compliant (there is no sixth name to
  declare), and it is the reason F1's member can appear without any D change.

### F4 — for a single-member V the amendment-4 extras never fire, so this row's support is 6 observations, not 12

- **Attacks:** the honesty arithmetic in amendment 4 (`contract.json:31`: "attested with probability
  1-(1-p)^12 (6 P0/P1 round runs + 6 extras)") as applied to `SCORECARD.md:2334`.
- **Observed:** `extras` are computed only for `missing = [m for m in claim['members'] if m not in
  observed and m not in p1_seen]` (`measure.py:531`); for a one-member V whose member is observed,
  `missing` is empty and `while missing and len(extras) < MAX_EXTRA` never runs. My run:
  `attested_extra=0`, no `EXTRA` line. The rows' support is therefore exactly 3 P0 + 3 P1 tuples.
- **Consequence:** the 12-sample disclosure belongs to rows that declare a rare second member. For
  this row the honest statement is 6 samples, and the mismatch-side arithmetic of F1 (3 P0 draws) is
  the one that governs the claim.

### F5 — `declared=` renders empty for the `none` set (cosmetic, three rows)

- **Attacks:** `measure.py:555-560` STATUS rendering.
- **Observed:** rows 2-4 print `declared= MATCH DEPS-OK` — `parse_deps('none')` returns `frozenset()`
  (`measure.py:185-195`) and the join of an empty set is the empty string. An empty rendering sits one
  glance away from `declared=-`, which the code uses for *unparsed*. `DEPS-OK` disambiguates, so no
  misreading is forced; recorded only so a future reader does not take `declared=` for a parse failure.

### F6 — independent (out-of-counter) confirmation of the four sha claims and the row grammar

- **Attacks:** A3 (tool prefix) and A2/A1's premise (that the rows parse as the amendment-3 grammar
  says). If the counter minted its own evidence, these would disagree.
- **Observed:** `git show REV:<path> | sha256sum | cut -c1-12` gives, for the rows in order,
  `a7d3f2dd7d47`, `296fe566dc59`, `331529eadafe`, `df3390682a04` — equal to the rows' claims; the same
  four blobs are byte-identical at BASE (empty diff, base→REV), so a moving tool cannot be the source
  of the match. A twelve-line parser I wrote against amendment 3 (not importing the counter) prints:

  ```
  ROW six-leg regression ledger              SCORECARD.md:2334  cells=4 members=[('REGRESSION: PASS (cases=9 passed=9', '0')] sha=a7d3f2dd7d47 deps=fleet-root,node cls=stable membercount=1
  ROW repeated pristine-control gate         SCORECARD.md:2335  cells=4 members=[('SELFTEST: PASS (29 cases)', '0')] sha=296fe566dc59 deps=none cls=stable membercount=1
  ROW six-leg content-disposition probe      SCORECARD.md:2336  cells=4 members=[('SELFTEST: PASS (19/19)', '0')] sha=331529eadafe deps=none cls=stable membercount=1
  ROW exposed witness provenance correction  SCORECARD.md:2337  cells=4 members=[('SELFTEST: PASS 39/39', '0')] sha=df3390682a04 deps=none cls=stable membercount=1
  ```

  `cells=4` for each row: the grammar's `cells[2]` is the evidence cell, and the first cell equals the
  statement id exactly (no whitespace or case drift). The three selftest rows' deps cell is literally
  `none`; the ledger row's is the sorted list `fleet-root,node`.

## Risk to the claim (read this before the deciding verdict)

C1's pass/fail at REV is not decided by my probe, but this probe bounds one term of it: with rows 2-4
showing 54/54 identical observations and no plausible dependence, essentially all of C1's remaining
risk sits in row 1, whose own excluded member appeared at 1/12 in my window and whose P0-only exposure
is ~23-27 % per invocation. If the L1 wants that term out of the claim, the tool-free move is a
pinned-leg successor that removes the one-sided race (already listed as a round-49 candidate at
`SCORECARD.md:2367`), not a rerun of the counter.

## Method notes and bounds observed

- Counter modes used: `--only` (this item's probe) only. No `--selftest`, no `--emit`, no deciding
  invocation, no control scoring, no verdict claim.
- No file in `corpus/`, `tools/`, `SCORECARD.md` was written; my only lane writes are the three
  receipt copies and this report under `.ufo/waves/round-48/a2w1/`. Lane worktree `lane_clean=1` at
  all four FLEET points of my own run confirms it, measured by the counter, not by me.
- Scratch: every clone and work dir lived under
  `/fast/scratch/hyaku/tameshi-r48/T48W2ExecC1ProbeB` (`--work "$S/w"`, `TMPDIR=$S`); the directory
  was removed after the receipts were copied here; nothing was written to `/tmp` by this seat.
- No tool was installed or upgraded (nothing was needed); `pacman` untouched.
- The three cited excerpts above (round-3 P2 observation lines, the `sweep.log` control/defect lines,
  and the observation receipt's `REGRESSION_DATE`) were copied verbatim into this report before the
  scratch dir was deleted, as the lane's evidence dir holds no copy of them.

## Evidence index

| file | content |
|---|---|
| `.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeB.stdout` | the run's stdout, 24 lines, sha256 `9a18bfde6e2a7b6e9c8c057f4d61f7e7066059a77202ab7ef3afa8a65cd61974` |
| `.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeB.stderr` | 0 bytes |
| `.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeB.time` | `start=2026-10-26T13:29:59Z end=2026-10-26T13:48:29Z exit=1` |
| `.ufo/evidence/round-48/calibration/measure.py` | counter under test (sha256 in freeze-2) |
| `.ufo/evidence/round-48/calibration/emit-15b1521.stdout` | the L1's emit the rows were pasted from; its `PROFILES` lines agree with my P0/P1 tuples and differ only in the round-3 P2 draw |
| `.ufo/waves/round-48/w1/T48RevenRegression.md` | root cause and 4/40 rate of the one-sided race |
| `.ufo/waves/round-48/w1/T48ExecObs2.md` | the same FAIL member observed at P0 on the base tree; host-state reading of the leg |
