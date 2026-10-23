# CalibMonitor — calibration monitor re-run at the tip (round 34 w1)

Seat: `tameshi-r34-w1-CalibMonitor`. Task (spec-w1.json): re-run the calibration monitor at the
tip if runnable; compare boxes/checked/asserted counts against the r33 baseline (64/64 restraint 8;
command C mark census); any drift is a finding.

## Verdict

**The calibration monitor at the tip `0b99d48` measures unchanged from the r33 baseline: 64/64
sections covered, calibration_restraint_score 8, depth_score 9, recorded_cases 9, ledger_guardrail
9/9/9/9, SHONEN boxes 4 / checked 0 / asserted 4 / untouched 0, command C upper bound 8, strict
trace gate, no overrides.** No calibration-axis drift.

Three findings, all with reproducing commands:

1. **F1 — the r33-routed cold-read re-crediting premise is falsified.** The r33 lesson
   (`corpus/lessons/round-33.md:133-134`) and the r34 SCORECARD claim the round's appends
   (lesson/SCORECARD/LOG/SOURCES) "drift monitor sections" and route re-crediting of
   "~19 SOURCES-citing sections + 3 all-four" into the r34 wave. Measured at the tip: per-section
   monitor output is **byte-identical** freeze→tip; **0 recorded ledger inputs newly drifted**
   (no entry recorded the freeze bytes of SOURCES/LOG/SCORECARD — all were already stale at the
   freeze); stale-entry counts identical (246→246 per-section, 399→399 whole-ledger); crediting
   entries identical (89→89 per-section, 90→90 whole-ledger); 0 sections lost credit; all 15
   SOURCES-citing sections retain at least one crediting entry that does **not** cite
   SOURCES.md; the 3 "all-four" sections (17, 131, 1155) have crediting entries citing none of
   SOURCES/LOG/SCORECARD. Coverage holds 64/64 at every commit tested (`732b686`, `5bfa3b5`,
   `6aaad5b3`, `c17e593b`, tip). The re-read is unnecessary to restore or preserve coverage; it
   would refresh stale recorded digests (a pre-existing freshness condition, not caused by the
   r33/r34 appends).
2. **F2 — a new W01 census warning appears at the tip and is undisclosed in the round records.**
   The round-34 census receipt (`.ufo/evidence/round-34/census-end.stdout`) contains
   `tameshi W01 S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md` — the
   **first W01 ever** in this lane's census receipts (all prior committed receipts have 8 W-class
   lines, all W04; round-34 has 9). The lane's own QUALITY MK-7 forbids a tier-C row as sole
   support, and the round-34 lesson (`corpus/lessons/round-34.md:39-40`) states "The round's
   sourced-claim conjunct rests on S101" — a tier-C row. The W01 appears in none of the round-34
   records: lesson, LOG.md, SCORECARD.md, and the knowledge entry each have 0 occurrences of
   "W01", and none discloses S101's tier. Census exit remains 0 (W-class does not fail).
3. **F3 — the `Next unused id:` pointer is stale at the tip.** `corpus/SOURCES.md:393` says
   "Next unused id: S100." while S100 **and** S101 are both occupied Registry rows (max occupied
   id = S101). Round 33 consumed S100 (`732b686`) without appending a fresh pointer; round 34
   consumed S101 (`0b99d48`) without appending one either. The file's own append-only convention
   (see `corpus/SOURCES.md:379-381` and `corpus/QUALITY.md:311-312`) requires a new pointer line
   per consuming round. A round following the pointer literally would write a duplicate S100 row →
   census E03 duplicate id (exit 1), demonstrated below.

## Setup and pinned bytes (exits 0)

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/CalibMonitor
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r34-seats/CalibMonitor/lane     # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                    # exit 0 (HEAD = tip)
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh
sha256sum tool.py pristine.sh
# 7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py   (matches pin)
# a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh (matches pin)
```

Frozen counter/controls receipts verified at the tip blob:
counter `.ufo/evidence/round-33/c1/c1-measure.py` sha256
`f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` at `6aaad5b3` and at the tip
(unchanged); `controls-receipt.json` committed with four controls all `predicate_pass=false`
(`all_false: true`).

## Monitor invocation (same harness as r33 baseline)

As `LedgerAudit.md` (r33 w1) documented: the round-21 cold-read selector delegating to the
round-18 credit algorithm, relocated depth-preserving into scratch:

```
mkdir -p monitor/.ufo/evidence/round-21/coldread monitor/.ufo/evidence/round-18
cp lane/.ufo/evidence/round-21/coldread/measure.py monitor/.ufo/evidence/round-21/coldread/
cp lane/.ufo/evidence/round-18/measure.py monitor/.ufo/evidence/round-18/

# freeze (r33 baseline rev f6d8a891):
python3 monitor/.ufo/evidence/round-21/coldread/measure.py \
  --repo /fast/scratch/hyaku/tameshi-r34-seats/CalibMonitor/lane \
  --rev f6d8a891f1d966c5c3cdda385090da3a6e804675 \
  > monitor-r33freeze.json 2> monitor-r33freeze.err; echo $? > monitor-r33freeze.exit   # 0
# -> JSON equality with committed baseline: True
#    (monitor-r33freeze.json == .ufo/evidence/round-33/dev/monitor-at-freeze.stdout)

# tip:
python3 monitor/.ufo/evidence/round-21/coldread/measure.py \
  --repo /fast/scratch/hyaku/tameshi-r34-seats/CalibMonitor/lane \
  --rev 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7 \
  > monitor-tip.json 2> monitor-tip.err; echo $? > monitor-tip.exit                   # 0
```

### Monitor comparison: r33 baseline vs tip

| Field | r33 baseline (f6d8a891) | tip (0b99d48) |
|---|---|---|
| coldread.sections_covered / sections_total | 64 / 64 | 64 / 64 |
| coldread.reasons | {credited: 64} | {credited: 64} |
| coldread.missing / uncovered_headings | [] / [] | [] / [] |
| coldread.box3_full_page | true | true |
| calibration_restraint_score | 8 | 8 |
| depth_score | 9 | 9 |
| recorded_cases | 9 | 9 |
| ledger_guardrail (header_legs / lists_agree / regression_calls / selftest_tuples / unique_recorded_gates) | 9 / true / 9 / 9 / 9 | 9 / true / 9 / 9 / 9 |
| shonen boxes / checked / asserted / untouched | 4 / 0 / 4 / 0 | 4 / 0 / 4 / 0 |
| shonen box3_ledger_link | true | true |
| trace_gate | strict | strict |
| overrides_used | false | false |
| ledger_source / ledger_committed | rev / true | rev / true |
| sources.rows | 96 | 98 |
| sources.tiers | A 87 / B 7 / C 2 | A 88 / B 7 / C 3 |
| sources.status | mined 68 / queued 22 / rejected 6 | mined 70 / queued 22 / rejected 6 |

The only deltas (`sources` rows 96→98, tiers A +1, C +1, mined +2) are fully explained by the two
new Registry rows since the freeze: S100 (round 33, tier A, mined) and S101 (round 34, tier C,
mined). `per-section explain output freeze vs tip: True` (byte-identical, incl. per-section
credited/vetoed/reasons).

### Command C mark census (SCORECARD.md:75) at freeze and tip

```
git show "$REV:SHONEN.md" | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" untouched="+str(m.count(" "))+" asserted_mark_upper_bound="+str(min(8,2*m.count("~"))))'
# f6d8a891… : boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8   (exit 0)
# 0b99d48…  : boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8   (exit 0)
```

## F1 detail — re-crediting premise falsified (evidence + commands)

The r33 lesson (`corpus/lessons/round-33.md:133-134`) and r34 lesson holds route
"Cold-read re-crediting of the drift monitor sections … LedgerAudit sized ~19 SOURCES-citing
sections + 3 all-four". Repro of the sizing with LedgerAudit's containment method gives exactly
19 SOURCES-citing sections and 3 all-four (starts 17, 131, 1155) at **both** the freeze and the
tip — the sizing itself is stable. But the monitor outcome does not drift:

```
# 0 sections lost crediting entries, 0 sections lost all credit (freeze vs tip)
# stale entries freeze/tip: 246 / 246 (per-section matched); 399 / 399 (whole ledger)
# crediting entries freeze/tip: 89 / 89 (per-section sum); 90 / 90 (whole ledger)
# recorded inputs that matched freeze bytes but not tip bytes (newly drifted): 0
# sections whose STALE-entry count grew freeze->tip: 0
# net: monitor output byte-identical at every commit tested
```

Root cause: the round-21 ledger blob is byte-identical at the freeze and tip
(`fc16d21a…` at both). Every SOURCES/LOG/SCORECARD-citing entry records older digests — none
recorded the freeze bytes (0 of 152 SOURCES-citing entries; 0 of 3 LOG/SCORECARD-citing entries).
So the r33/r34 appends changed nothing about staleness: those entries were already failing the
input gate before the appends existed, and each affected section keeps credit via separate entries
whose recorded digests still verify. The routed re-read is therefore unnecessary for coverage; at
most it would refresh pre-existing stale recorded digests.

## F2 detail — W01 (evidence + commands)

- Census reproduction against the tip SOURCES.md (live fleet tree SOURCES.md == tip blob sha
  `595c7fa531226d65570d1e3a64e27ae177731b8612a8db5caacaad10b8c62af7`):
```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --today 2026-10-23 --root /home/vgpnk/Projects/shokunin tameshi > census-tip-repro2.stdout \
  2> census-tip-repro2.stderr; echo $? > census-tip-repro2.exit
# exit 0; stdout contains:
#   tameshi  W01  S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
#   tameshi  ok   /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```
  This output is line-for-line identical to the committed receipt
  `.ufo/evidence/round-34/census-end.stdout` (exit 0).
- First-ever W01: every committed census receipt before round 34 has exactly 8 W-class lines, all
  W04 (checked r22–r33 receipts); round-34 has 9 lines including the W01.
- W01 rule (`sources-census.sh:670`): `tier=="C" && status=="mined" && usedby!="—"`. S101:
  tier C, status mined, used-by `corpus/knowledge/witness-equivalence-rule.md`.
- Undisclosed: `grep -c W01` in `corpus/lessons/round-34.md`, `LOG.md`, `SCORECARD.md`, and
  `corpus/knowledge/witness-equivalence-rule.md` all return 0. The lesson's own sentence
  (`corpus/lessons/round-34.md:39-40`): "The round's sourced-claim conjunct rests on S101." —
  against QUALITY MK-7 (`corpus/QUALITY.md:30`): "a tier-C row is never sole support". (S089,
  tier A, already covers equivalent mutants in the registry.)

## F3 detail — stale pointer (evidence + commands)

```
grep "Next unused id" corpus/SOURCES.md | tail -1
# - Next unused id: S100.
grep -oE '^\| S[0-9]{3} ' corpus/SOURCES.md | tr -d '| ' | sort | tail -1
# S101
grep -c '^| S100 ' corpus/SOURCES.md     # 1 (S100 occupied)
grep -c '^| S101 ' corpus/SOURCES.md     # 1 (S101 occupied)
# => pointer names S100 while S100 and S101 are both occupied; correct next unused is S102
```

Pointer history: `a4f7181` (r32) appended "Next unused id: S100." when that was correct (max
S099). `732b686` (r33) consumed S100 without appending a fresh pointer; `0b99d48` (r34) consumed
S101 without appending one either. Consequence (demonstrated): inserting a second S100 row and
re-running the census produces `E03 S100 duplicate id` and exit 1:

```
cp lane/corpus/SOURCES.md e03/SOURCES.md   # insert duplicate S100 row after S099
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-23 \
  --file e03/SOURCES.md > e03/dup.stdout 2> e03/dup.stderr; echo $? > e03/dup.exit
# exit 1; stdout contains: file  E03  S100 duplicate id
```

## Scope / bounds compliance

- Read-only on the lane clone; the only writes were inside
  `/fast/scratch/hyaku/tameshi-r34-seats/CalibMonitor/` and this report file.
- No git/jj write command ran anywhere; the lane worktree remained clean (`git status
  --porcelain` empty).
- No tool installs were needed (stdlib + existing scripts only); RULES.md tooling directive not
  triggered.
- The C1 default-mode counter was never run; the counter was only inspected as committed blobs for
  pin verification.

## Risks / notes for L1

- W01 (F2) does not fail the census (exit 0) — it is a disclosed-in-receipt but undisclosed-in-
  records warning that a tier-C row is load-bearing for the round's sourced claim under MK-7.
- The pointer (F3) is a bookkeeping defect, not gate-enforced (`sources-census.sh` has no check
  for "Next unused id"); only a future allocator following it hits E03.
- The r33-routed re-crediting item (F1) is not needed for coverage; if the intent was to refresh
  stale recorded digests, the stale set (49 of 64 sections carry ≥1 stale entry at both revs) is
  pre-existing and unchanged by this round.
