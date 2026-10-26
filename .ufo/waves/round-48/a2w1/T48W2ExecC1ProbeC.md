# T48W2ExecC1ProbeC — C1 probe group C (five restated cap rows)

Seat: `T48W2ExecC1ProbeC`, round 48 attempt 2, wave a2w1, calibration axis / C1 feed.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `473336d9d789f6081195e7376d17836a24666bc3`,
CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`. Read-only on the lane; this report and
`.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeC.stdout` are my only writes (plus `$TMPDIR` scratch, deleted).

Target of attack: the five round-48 standing rows for
`effective expectation reconciliation`, `retained invocation-context gate`,
`hermetic env-differential probe`, `callback-authoritative wave accounting`,
`required-command-receipt-binding` — i.e. whether the row's declared value set V, class,
`tool sha256` prefix and deps set D survive three observation rounds of P0-P5 at CONTENT.
I am not an author of these rows, the counter, or the tools.

## 0. Verdict

**No row is contradicted.** One probe invocation (3 rounds × 6 profiles × 5 statements, 90 runs) and
two further independent single-round invocations at CONTENT all print `total=0` with `MATCH DEPS-OK`
on the five rows, and five direct out-of-counter runs in a fresh clone reproduce the same
(line, exit) tuples. No row in my group is declared `nondeterministic`; each declares `stable` and my
runs saw exactly one member, in every round, with the declared member attested in every round
(`attested_extra=0`). Details, retained evidence and four disclosures below.

## 1. Probe command and label (a probe is never a verdict)

```
S=/fast/scratch/hyaku/tameshi-r48/T48W2ExecC1ProbeC; TMPDIR=$S
python3 .ufo/evidence/round-48/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 \
  --base 473336d9d789f6081195e7376d17836a24666bc3 --work "$S/w" \
  --only "effective expectation reconciliation,retained invocation-context gate,hermetic env-differential probe,callback-authoritative wave accounting,required-command-receipt-binding"
```
exit 1, wall 81 s; full stdout (28 lines) at
`.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeC.stdout` (sha256 `ca15d6270f0204de255a277798b3cc9d2ab7e99e7b1ec01df3d632381fec62d5`).

Last line verbatim:

```
C1_R48_PARTIAL: self_pin=1 stmts_pin=1 statements=5 rounds=3 append_only=1 unpinned=0 total=0 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=1 base=473336d9d789f6081195e7376d17836a24666bc3 rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C1_R48_PASS=false
```

`C1_R48_PARTIAL` / `C1_R48_PASS=false` is the designed seat-probe label (`measure.py:59`, `:578`); nothing
here is a claim about the deciding run. Two extra one-round invocations (`--rounds 1 --only <same five>`,
fresh empty work dirs `$S/x1`, `$S/x2`, 67 s) printed the same five `STATEMENT` lines and
`total=0 … rounds=1 … C1_R48_PASS=false`.

## 2. STATEMENT lines, verbatim (main probe, rounds r1/r2/r3)

```
STATEMENT cap/effective expectation reconciliation: claimed=SELFTEST: PASS (66/66)|0 sha=39ee5c5effd9 ROUNDS r1=SELFTEST: PASS (66/66)|0 r2=SELFTEST: PASS (66/66)|0 r3=SELFTEST: PASS (66/66)|0 DEPS required=jj unstable=none never=bwrap,env,fleet-root,node declared=jj MATCH DEPS-OK
STATEMENT cap/retained invocation-context gate: claimed=SELFTEST: PASS (49/49)|0 sha=7e4519d9a0ea ROUNDS r1=SELFTEST: PASS (49/49)|0 r2=SELFTEST: PASS (49/49)|0 r3=SELFTEST: PASS (49/49)|0 DEPS required=fleet-root unstable=none never=bwrap,env,jj,node declared=fleet-root MATCH DEPS-OK
STATEMENT cap/hermetic env-differential probe: claimed=ENVDIFF_SELFTEST: 9/9 pass|0 sha=e8b47ab7cf23 ROUNDS r1=ENVDIFF_SELFTEST: 9/9 pass|0 r2=ENVDIFF_SELFTEST: 9/9 pass|0 r3=ENVDIFF_SELFTEST: 9/9 pass|0 DEPS required=bwrap,node unstable=none never=env,fleet-root,jj declared=bwrap,node MATCH DEPS-OK
STATEMENT cap/callback-authoritative wave accounting: claimed=ACCOUNTING_SELFTEST: 8/8 pass|0 sha=96b3038a77f8 ROUNDS r1=ACCOUNTING_SELFTEST: 8/8 pass|0 r2=ACCOUNTING_SELFTEST: 8/8 pass|0 r3=ACCOUNTING_SELFTEST: 8/8 pass|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT cap/required-command-receipt-binding: claimed=COMMAND_BINDING_SELFTEST: 44/44 pass|0 sha=9230c68e53a5 ROUNDS r1=COMMAND_BINDING_SELFTEST: 44/44 pass|0 r2=COMMAND_BINDING_SELFTEST: 44/44 pass|0 r3=COMMAND_BINDING_SELFTEST: 44/44 pass|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
```

No `MISMATCH`, `DEP-MISMATCH`, `UNATTESTED`, `UNPARSED`, `OVERSIZE` or `UNOBSERVABLE` line appears for
any of the five; `attested_extra=0` (no row needed an extra P0 observation, so each declared member was
attested by an in-invocation P0 or P1 tuple in all three rounds — `measure.py:530-531`).

## 3. P0-P5 per round (identical in r1, r2, r3)

| statement | P0 | P1 | P2 (no bwrap) | P3 (no jj) | P4 (no node) | P5 (decoy fleet root) |
|---|---|---|---|---|---|---|
| effective expectation reconciliation | `SELFTEST: PASS (66/66)`,0 | same,0 | same,0 | **`-`** (unobservable) | same,0 | same,0 |
| retained invocation-context gate | `SELFTEST: PASS (49/49)`,0 | same,0 | same,0 | same,0 | same,0 | same, **exit 1** |
| hermetic env-differential probe | `ENVDIFF_SELFTEST: 9/9 pass`,0 | same,0 | `2/9 pass`,1 | `9/9 pass`,0 | `8/9 pass`,1 | `9/9 pass`,0 |
| callback-authoritative wave accounting | `ACCOUNTING_SELFTEST: 8/8 pass`,0 | same,0 | same,0 | same,0 | same,0 | same,0 |
| required-command-receipt-binding | `COMMAND_BINDING_SELFTEST: 44/44 pass`,0 | same,0 | same,0 | same,0 | same,0 | same,0 |

Dependence observation: P0 == P1 for all five, so `env` is never a dependence here; the required sets
fall out exactly as the rows declare (`measure.py:501-510`).

## 4. Independent triangulation (outside the counter instrument)

`git clone -q --shared` at CONTENT into scratch, then each row's own command under my live host env
(P0-like), capturing the statement's own observation regex:

```
effective expectation reconciliation => LINE[SELFTEST: PASS (66/66)] EXIT[0]
retained invocation-context gate => LINE[selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)] EXIT[0]
hermetic env-differential probe => LINE[ENVDIFF_SELFTEST: 9/9 pass] EXIT[0]
callback-authoritative wave accounting => LINE[ACCOUNTING_SELFTEST: 8/8 pass] EXIT[0]
required-command-receipt-binding => LINE[COMMAND_BINDING_SELFTEST: 44/44 pass] EXIT[0]
```

(The `retained invocation-context gate` line is quoted at source form; the counter's `pick_line`
(`measure.py:255`) returns its capture group `SELFTEST: PASS (49/49)`, which is the row's member.)

Tool pins recomputed from the lane at CONTENT (`git show REV:<path> | sha256sum`), matching the rows'
`tool sha256` prefixes:

```
39ee5c5effd9 tools/evidence-disposition.py        (row 2338)
7e4519d9a0ea .ufo/evidence/round-15/verify.py     (row 2339)
e8b47ab7cf23 tools/env-diff.py                    (row 2340)
96b3038a77f8 tools/wave-accounting.py             (row 2341)
9230c68e53a5 tools/command-binding.py             (row 2342)
```

`append_only=1` re-checked independently: `git show c7586b9a:SCORECARD.md` starts with
`git show 473336d:SCORECARD.md` (base 248 883 B, rev 263 506 B). Rows under attack:
`SCORECARD.md:2338-2342`.

Retained per-profile outputs of all 90 runs exist under `$S/w/round{1,2,3}/P{n}/obs-*.stdout` in scratch;
the cited lines are reproduced here:

* `P3/obs-effective-expectation-reconciliation.stdout`: `SELFTEST: FAIL (3/66 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip, v2-jj-without-lane-branch; fixtures kept at /tmp/tameshi-r14-…)` — the `jj` dependence is a hard one (the tool loses three jj cases and its `SELFTEST: PASS` line entirely without `jj`).
* `P5/obs-retained-invocation-context-gate.stdout`: `selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)` … `sources-census: FAIL exit=7 (expected 0)` … `sources-census-ok-line: FAIL ok line absent`; exit 1. So `deps fleet-root` is carried by the census leg against the decoy root, exactly as declared.
* `P2/obs-hermetic-env-differential-probe.stdout`: `ENVDIFF_SELFTEST: 2/9 pass` (exit 1); `P4/…`: `ENVDIFF_SELFTEST: 8/9 pass` (exit 1). P0/P1 stay `9/9 pass`, exit 0.
* `P0/obs-callback-authoritative-wave-accounting.stdout`: `ACCOUNTING_SELFTEST: 8/8 pass` and `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass` (the row cites only the frozen eight; the 16 supplemental cases also passed, `tools/wave-accounting.py:188,192`).

Descriptive-cell spot checks (the restated rows' prose, not their C1 values):

* `SCORECARD.md:2340` "eight `invariant` and one `nondeterministic` (`js-round-gate`)": `.ufo/evidence/round-21/f5/receipt-initial.json` has 9 `surfaces`, classifications 8 × `invariant` + 1 × `nondeterministic`, the latter `scripts/round-gate.mjs` (kumitate); `profiles` has the seven keys `clean, clean_repeat, columns, home, host, locale, tz`. Consistent with the cell's "nine … under seven explicit profiles".
* `SCORECARD.md:2341` "reject mismatched totals and digest tampering": the frozen eight cases plus the 16 supplemental fixtures read `raw`/`nested_arrays` bundles with a pinned `bundle_sha256` expectation and assert the finding id on mismatched totals/tampering (`tools/wave-accounting.py:143-190`). Not refuted.

## 5. Findings

**Contradictions of the five rows: none.** No row is a finding; the five hold at CONTENT on four
independent invocations (3+1+1 counter rounds, plus five direct runs).

Disclosures and risks (not row contradictions, and not mine to remediate):

1. **Row provenance is attempt 1's content revision.** `SCORECARD.md:2326` says every evidence cell in
   the round-48 section is pasted from `--emit` at `15b1521ea2e95d0d708059458c090e9f334adf32`
   (`.ufo/evidence/round-48/calibration/emit-15b1521.stdout`), not at CONTENT `c7586b9a`. `git diff
   15b1521 c7586b9a -- tools` is empty and `-- SCORECARD.md corpus/QUALITY.md corpus/lessons/round-48.md`
   is all that moved, so the five tool pins and the five tuples cannot differ; my runs confirm they do
   not. The same is *not* established here for the other 17 rows (out of my item).
2. **`effective expectation reconciliation` leaks fixtures into `/tmp`.** `tools/evidence-disposition.py:2351`
   builds its selftest scratch with `tempfile.mkdtemp(prefix="tameshi-r14-evidence-disposition-selftest.", dir="/tmp")`
   — a hard-coded `/tmp` (`:181` documents it), so it ignores the profile `TMPDIR` the counter sets
   outside `/tmp`. Every jj-less (P3) run leaves a ~6.7 MB directory; `/tmp` now holds 13 of them
   (e.g. `/tmp/tameshi-r14-evidence-disposition-selftest._6lwo0ym` 10:30:56, `.b85i1fo0` 10:30:57,
   `.d0khgzm9` 10:31:25 — inside my probe window; later ones at 10:34 belong to sibling probes).
   This does not affect the row (P0 is observed), but a full 22-statement deciding run will deposit
   ~20 MB per invocation into `/tmp`, against the round-48 "scratch never in `/tmp`" rule, and the
   counter cannot prevent it. I did not delete them: sibling seats' P3 runs create the same prefix in
   the same window and a sibling receipt may cite a specific path.
3. **`pass` in a failing line; PASS line with a failing exit.** `hermetic env-differential probe`
   prints `ENVDIFF_SELFTEST: 2/9 pass` / `8/9 pass` with exit 1, and `retained invocation-context gate`
   prints `SELFTEST: PASS (49/49)` while exiting 1 under the decoy fleet root. Both rows are *correct*
   because the declared member carries the exit code (amendment 3), but the text token alone does not
   discriminate pass from fail — worth knowing for anyone reading a receipt without its exit.
4. **A `deps` member can rest on UNOBSERVABLE.** `measure.py:501-507` treats "variant tuple ≠ P1 tuple"
   as "dependence observed", and `dep_key` maps a missing line to `('UNOBSERVABLE', note)`. For
   `effective expectation reconciliation` the declared `jj` is therefore carried by a *total* P3
   failure (`SELFTEST: FAIL (3/66 failed: …)`), not by a graded value change. Correct for this tool
   (the three failing cases are the jj ones) and implemented as the contract's docstring says, but a
   row could equally satisfy a `deps` name through an unrelated crash. Instrument note only.

Fleet state during my probe (`FLEET` lines, 4 points): `census_sha=3fb7261569f4 lane_clean=1` at all
four; `fleet_drift=0`; one disclosed `sibling_moves=1` (`souji-shokunin` 4e56c48b8fc8 → 9da5e9a559f7
between points 2 and 3), which amendment 5 counts as a disclosure, not drift.

## 6. Hygiene

* Scratch `$S=/fast/scratch/hyaku/tameshi-r48/T48W2ExecC1ProbeC` (154 MB: clones, 90 per-profile obs
  files, two extra work dirs) created with `mktemp`-equivalent `mkdir -p`, `TMPDIR` confined to it, and
  deleted before this report; no clone, work dir or temp file of mine survives.
* `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` read before the heavy pass
  (`/fast/scratch/hyaku` 23 %, 620 G free); no ENOSPC. `/tmp` usage added by my probe is the tool's own
  leak (finding 2), not scratch I keep.
* No tool installed or upgraded (nothing needed). No `git` state-mutating command in the lane (only
  `git show/clone/checkout` in my own scratch clone); no `jj` command at all. No sibling lane, fleet
  repo or `corpus/`, `tools/`, `SCORECARD.md` write.
