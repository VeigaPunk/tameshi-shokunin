# T48W2CritC1Rows — the 22 restated rows against the committed receipts (C1, attack)

Seat `T48W2CritC1Rows`, wave a2w1, lane `tameshi-shokunin`. Content revision under attack:
`c7586b9a10effc63b4bd327f976edc094c1bdc17` (`SCORECARD.md` section `### Standing self-assessment — re-stated
at round 48`, lines 2324–2356 of the blob at REV). Base `473336d9d789f6081195e7376d17836a24666bc3`;
frozen counter `.ufo/evidence/round-48/calibration/measure.py` (sha256 `572a5670…`), statements
`.ufo/evidence/round-47/calibration/statements.json` (sha256 `924102df…`).

I did not run the long counter. I read the rows out of the REV blob, parsed them with the amendment-3
grammar, and compared every declared scalar against (a) the three observation rounds printed in
`.ufo/evidence/round-48/calibration/emit-15b1521.stdout`, (b) the committed observation receipt
`.ufo/evidence/round-48/calibration/observations/obs2-r47counter-base.emit.stdout` (evidence only, never
attestation), and (c) `git show REV:<sha_file> | sha256sum`. Three cheap `--only … --rounds 1` probes
(partial by construction, `C1_R48_PASS=false`) re-observed 5 of the 22 rows at REV itself.

**Headline: the 22 rows have no grammar, value, sha or deps defect at REV (0 contradictions). One row's
class label is contradicted by a committed receipt and by the lane's own wave-1 evidence — it is
*forced* by amendment 4 and disclosed in prose (F1, tradeoff, not a row defect). One provenance sentence
overreaches for three cells (F2). Attestation under amendment 4 is still open: `after/c1.stdout` does not
exist yet (F5).**

## Findings

### F1 — `six-leg regression ledger` declares `stable` while a committed receipt records the other member at P0 (contradiction count: 1)

* Attacked: `SCORECARD.md:2334` (`| six-leg regression ledger | … runs 3 stable |`), declared
  V = {`REGRESSION: PASS (cases=9 passed=9`, exit 0}.
* Contradicting receipt: `.ufo/evidence/round-48/calibration/observations/obs2-r47counter-base.emit.stdout:6`
  — `PROFILES six-leg regression ledger: P0=REGRESSION: FAIL (cases=9 passed=8|1 …` (that receipt's own
  verdict line, `:67`, is `rev=473336d9d789f6081195e7376d17836a24666bc3`). Lane evidence for the same
  statement at the same tree: `.ufo/waves/round-48/w1/T48ExecObs2.md:64-80` (one seat, one tree, two runs:
  `PASS passed=9|0` and `FAIL passed=8|1` at P0), `.ufo/waves/round-48/w1/T48RevenRegression.md:42,126-127`
  (pinned blob's selftest 4/40 failures at 6-way concurrency; ledger-level 1 FAIL in 2 replays).
* Show it: `sed -n '6p' .ufo/evidence/round-48/calibration/observations/obs2-r47counter-base.emit.stdout`
  and `git -C . show c7586b9a:SCORECARD.md | sed -n '2334p'`.
* Why the row is stuck: amendment 4 attests a member only from the same invocation's P0/P1 (or up to six
  extra P0 observations); a P0 tuple in a committed observation file never attests, and
  `T47ExecObsE.md:151`'s FAIL is a P3 tuple, which amendment 4 excludes. So `stable` is the only row the
  rule permits, and the rule is stated in the section prose (`SCORECARD.md:2328`) — this is a rule-level
  tradeoff the canonical judge owns, not an edit I may make.
* Residual risk that is not disclosed: the deciding run runs this statement's six profiles *concurrently*
  — `measure.py:456-458` submits every `(statement, profile)` to a `ThreadPoolExecutor(max_workers=6)`
  ordered by descending timeout, so `six-leg regression ledger` (timeout 2700) is the first six jobs and
  its P0 competes with its own five variants. That is exactly the concurrency regime the 4/40 failures were
  measured in, and the kill rule converts one such P0 into `total>0`. The emit survived 18 such runs
  (three rounds × six profiles, all PASS), so the exposure is real but unquantified.

### F2 — "every evidence cell … pasted byte-exact" is false for the three axis cells (provenance overreach, low)

* Attacked: `SCORECARD.md:2326` ("Every evidence cell below is the counter's own `--emit` output, pasted
  byte-exact").
* Observed: the 19 cap cells are byte-identical to the emit's `EMIT_CAP … | <evidence> |` fields (0
  differences). The three axis cells at `SCORECARD.md:2354-2356` are not: the emit printed
  `see the evidence pointer in the round-48 SCORECARD block, tool sha256 `a7d3f2dd7d47`, deps `none`, runs 3 stable`
  (and the `657f009bdf1c` / `ba64041f49ff` twins) — a self-referential placeholder — while the pasted
  prefixes are the round-47 counting-rule prose. Only the tail (`tool sha256 …`, `deps …`, `runs 3 stable`)
  is emit text.
* Show it: `grep '^EMIT_AXIS' .ufo/evidence/round-48/calibration/emit-15b1521.stdout` versus
  `git -C . show c7586b9a:SCORECARD.md | sed -n '2354,2356p'`.
* Mitigating: the next sentence of the same paragraph (`SCORECARD.md:2326`) already says the axis
  counting-rule prose is "carried unchanged from the round-47 rows", and the scalars the grammar reads
  (score, sha, deps, class) are emit-exact. Net effect on the predicate: none. Net effect on provenance:
  the universal quantifier is wrong for 3 of 22 cells.
* Smallest safe correction: one clause — restrict "pasted byte-exact" to the cap cells (e.g. "*every cap
  evidence cell …; the axis cells carry the emit tail on the round-47 counting-rule prose*"). It can only
  be made in a revision after REV, so it is routed, not applied here.

### F3 — `sources-registry` value tracks C2's row additions; checked, not a contradiction

`SCORECARD.md:2332` declares `rows=128`; the committed observation receipt at base records `rows=124`
(`obs2-…:1`). That is the four C2 rows (S265–S268) and not a defect: `corpus/SOURCES.md` is byte-identical
at the emit revision and at REV (`git -C . diff --stat 15b1521e c7586b9a -- corpus/SOURCES.md` is empty),
and a probe at REV printed `P0=rows=128 …` for this statement. The contract's separability note ("its value
tracks C2's row additions") is therefore true but *satisfied*: the emit rev already carried the rows.

### F4 — the `freshness` axis row is the only row whose value is re-derived from the live network at the deciding run

`SCORECARD.md:2356` declares 9, emitted at 15b1521e; the statement is `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV`,
which re-verifies held rows against live bytes each invocation (`measure.py:254-256`: `fresh=len(agreed-disputed)`,
`score=(10*fresh)//len(pop)`, population from the frozen `round-45/freshness/ledger.json` at REV). C2's new
rows cannot move it (the numerator is ledger members, not registry rows), but an unreachable page at the
deciding run lowers `fresh` and turns the row into a mismatch. No row change is warranted; this is a note
that this axis row's stability is external-environment-bound, not tree-bound. I did not probe it (a 73-page
live verification during a deciding-run window would add load without adding evidence).

### F5 — attestation is still open: `after/c1.stdout` is not committed

`.ufo/evidence/round-48/after/` does not exist as of this report (`ls .ufo/evidence/round-48/after` →
`No such file or directory`). Under amendment 4 the emit and observation receipts cannot attest, so the
"every declared member appears in a P0 tuple observed at REV in this invocation" check can only be closed
on the deciding receipt. The exact acceptance check once it lands:

```
awk -F'P0=' '/^PROFILES /{print $1, $2}' .ufo/evidence/round-48/after/c1.stdout   # 22 statement lines × 3 rounds
grep -c '^STATEMENT ' .ufo/evidence/round-48/after/c1.stdout                     # 22
tail -1 .ufo/evidence/round-48/after/c1.stdout                                   # total=0 fleet_drift=0 C1_R48_PASS=true
```

and the row-by-row criterion is the table below: each declared member must appear as the P0 tuple in all
three `ROUND` blocks or in one of the `EXTRA …: xN=…` lines, with no `EXTRA` tuple outside V
(`measure.py:478-500`).

## Row-by-row result (22/22)

Legend: `C128`/`C124` = `rows=128`/`rows=124 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0;
`R-PASS9` = `REGRESSION: PASS (cases=9 passed=9`, exit 0; `R-FAIL8` = `REGRESSION: FAIL (cases=9 passed=8`,
exit 1; `WCV2`/`WCV3` = the `WRITE_CENSUS_V2/V3_SELFTEST` lines. `sha@REV` is `git show REV:<sha_file> |
sha256sum` truncated to 12 hex; every one of the 22 matched. `deps=required` is the emit's own
`DEPS required=…` field, re-derived independently from the `PROFILES` lines with
`VARIANTS=(bwrap:P2, jj:P3, node:P4, fleet-root:P5)` and `env = (P0 ≠ P1)` (`measure.py:89,501-513`) — the
two computations agree for all 22.

| row | statement | class | declared V | emit P0 r1,r2,r3 | sha@REV | deps=required | P0∉V | obs P0 contradicts |
|---|---|---|---|---|---|---|---|---|
| 2332 | sources-registry | stable | `C128`/0 | `C128`/0 `C128`/0 `C128`/0 | `b9b754713c9c` | `none` | 0 | `C124`/0 (base rev, F3) |
| 2333 | mutation sweep runner | stable | `MUTATE_SELFTEST: 106/106 pass`/0 | same ×3 | `a7d3f2dd7d47` | `none` | 0 | no |
| 2334 | six-leg regression ledger | stable | `R-PASS9`/0 | `R-PASS9`/0 ×3 | `a7d3f2dd7d47` | `fleet-root,node` | 0 | **`R-FAIL8`/1** (F1) |
| 2335 | repeated pristine-control gate | stable | `SELFTEST: PASS (29 cases)`/0 | same ×3 | `296fe566dc59` | `none` | 0 | no |
| 2336 | six-leg content-disposition probe | stable | `SELFTEST: PASS (19/19)`/0 | same ×3 | `331529eadafe` | `none` | 0 | no |
| 2337 | exposed witness provenance correction | stable | `SELFTEST: PASS 39/39`/0 | same ×3 | `df3390682a04` | `none` | 0 | no |
| 2338 | effective expectation reconciliation | stable | `SELFTEST: PASS (66/66)`/0 | same ×3 | `39ee5c5effd9` | `jj` | 0 | no |
| 2339 | retained invocation-context gate | stable | `SELFTEST: PASS (49/49)`/0 | same ×3 | `7e4519d9a0ea` | `fleet-root` | 0 | no |
| 2340 | hermetic env-differential probe | stable | `ENVDIFF_SELFTEST: 9/9 pass`/0 | same ×3 | `e8b47ab7cf23` | `bwrap,node` | 0 | no |
| 2341 | callback-authoritative wave accounting | stable | `ACCOUNTING_SELFTEST: 8/8 pass`/0 | same ×3 | `96b3038a77f8` | `none` | 0 | no |
| 2342 | required-command-receipt-binding | stable | `COMMAND_BINDING_SELFTEST: 44/44 pass`/0 | same ×3 | `9230c68e53a5` | `none` | 0 | no |
| 2343 | refusing-registry-replay | stable | `REGISTRY_REPLAY_SELFTEST: 10/10 pass`/0 | same ×3 | `9fcd2dbba737` | `none` | 0 | no |
| 2344 | mutation report interop | stable | `MTE_SELFTEST: 17/17 pass`/0 | same ×3 | `193ea6e32f89` | `node` | 0 | no |
| 2345 | tally-audit-v2 runner audit | stable | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`/0 | same ×3 | `7b11ba25aead` | `none` | 0 | no |
| 2346 | tally-audit-v3 runner audit | stable | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`/0 | same ×3 | `da8c1ef4b30c` | `none` | 0 | no |
| 2347 | bounded ANSI-C code_view | stable | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`/0 | same ×3 | `da8c1ef4b30c` | `none` | 0 | no |
| 2348 | write-path-census-v2 | stable | `WCV2`/0 | same ×3 | `402285329588` | `none` | 0 | no |
| 2349 | write-path census destination resolution | stable | `WCV3`/0 | same ×3 | `095924a7a165` | `none` | 0 | no |
| 2350 | staged-id adoption guard | stable | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`/0 | same ×3 | `03a796c5726c` | `none` | 0 | no |
| 2354 | depth | stable | `9` | `9` `9` `9` | `a7d3f2dd7d47` | `none` | 0 | no |
| 2355 | calibration | stable | `6` | `6` `6` `6` | `657f009bdf1c` | `none` | 0 | no |
| 2356 | freshness | stable | `9` | `9` `9` `9` | `ba64041f49ff` | `none` | 0 | no (F4) |

Counts: 22 rows parsed in the amendment-3 grammar (0 unparsed, 0 oversize; 22 `stable` × 1 member, 0
`nondeterministic`); 22/22 declared members observed as P0 in all three emit rounds *and* at P1; 0 observed
P0 tuples outside V; 22/22 deps clauses equal the emit's `required` set and my independent recomputation;
22/22 sha prefixes equal the REV blob; 19/19 cap cells byte-identical to `EMIT_CAP`, 3/3 axis cells differ
in their prefix (F2).

Post-structural checks also passed: every one of the 22 ids' **last** row in `SCORECARD.md` at REV is the
round-48 row (amendment 6; earlier occurrences, e.g. `required-command-receipt-binding` at :1057/:1524,
are superseded), the round-48 block is a pure append over the base SCORECARD
(`append_only=1`, also printed by the probes), and the two corpus files the content revision does change
(`corpus/QUALITY.md`, `corpus/lessons/round-48.md`) are read by none of the 22 statement paths (cap
statements are tool selftests over fixtures and pinned blobs; the only `corpus/` references in
`tools/mutate-and-run.sh` are other lanes' blob pins and comment anchors). The emit's `fleet_drift=1`
(`emit-15b1521.stdout` FLEET points 2–4, `lane_clean=0`) is disclosed at `SCORECARD.md:2328` and cannot
taint the observed values: `setup_profile` (`measure.py:304-322`) clones the lane and checks out REV per
profile per round, so each observation reads committed bytes at REV. A probe now reports `lane_clean=1`,
so a clean deciding run has `fleet_drift=0` available.

## Probes run (probes, never verdicts)

All at `--rev c7586b9a… --base 473336d9…`, `--rounds 1`, `--work` an empty dir under my scratch; each
printed `C1_R48_PARTIAL … C1_R48_PASS=false` by construction:

| probe | result |
|---|---|
| `--only sources-registry --rounds 1` | `P0=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0` — MATCH, `fleet_drift=0` |
| `--only calibration --rounds 1` | `P0=6` — MATCH (the SCORECARD rewrite did not move the cold-read score) |
| `--only depth,write-path-census-v2,staged-id adoption guard --rounds 1` | `9` / `WCV2` / `STAGED_ID_GUARD … failed=0` — all MATCH |

Command form:
`python3 .ufo/evidence/round-48/calibration/measure.py --lane $PWD --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 --base 473336d9d789f6081195e7376d17836a24666bc3 --work "$S/probeN" --only <id> --rounds 1`.
I did **not** probe `six-leg regression ledger`: a concurrent replay is the exact load that turns its
`pipefail`/SIGPIPE race red, and the deciding run was expected in this window — reproducing the FAIL then
could have caused the miss it is supposed to detect. The w1 evidence already carries it.

## Axes impacted

* calibration (C1): F1 is the one place `C1_R48_PASS` can fail for reasons outside the tree; F2 is cosmetic
  to the predicate; F5 is the open gate. No row edit proposed — C1's row set is exactly what the frozen
  counter's `--emit` produced, byte for byte for 19 of 22 cells.
* freshness (C2): F4 only (an axis row of C1, not C2's own predicate).
* depth: untouched (its row re-observes at REV; `tools/mutate-and-run.sh` is byte-identical at both revs).

## Smallest safe corrections

1. F2 (provenance wording, after REV): restrict "pasted byte-exact" at `SCORECARD.md:2326` to the cap
   cells. Nothing else.
2. F1: no row correction is possible under amendment 4 — either the rule admits a declared-but-unobserved
   member for a statement whose second member is on record, or the section keeps the prose disclosure and
   accepts that one flaky deciding observation is a miss by design. That choice is the canonical judge's;
   my report only records that the row is currently `stable` *by rule*, against a receipt that says
   otherwise.
3. F5: close attestation on `after/c1.stdout` with the command above before any verdict is read.

## Bounds, scratch, tooling

Read-only on the lane; the only file I wrote is this report (`.ufo/waves/round-48/a2w1/`, untracked and
outside `corpus/`, `tools/`, `SCORECARD.md`, so `lane_clean` stays 1). No mutating git/jj command, no
`agent://all`. Scratch `/fast/scratch/hyaku/tameshi-r48/T48W2CritC1Rows` removed before this report was
finished (`rm -rf`), no file under `/tmp`, disk guard checked before the probes (`/fast/scratch/hyaku` 26 %
used, 602 G free). No tool was installed or upgraded.
