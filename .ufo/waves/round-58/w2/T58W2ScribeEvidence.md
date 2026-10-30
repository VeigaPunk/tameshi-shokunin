# Round 58 — evidence table

Seat `T58W2ScribeEvidence`. Axes: calibration, provenance, completeness.
Base `2a32aa8228d5f86a85c81a923a3148bf792a9538`; C0 `8063d0a551fc5b3cb5a2d397da7353af53444534`. Required `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -3` observed C0, `0fdb71d2`, `1d1f70d8` in order. Evidence-only work: no scoring, attack, selftest or census reruns.

## Claims and counting commands

`LANE` and `EMPTY_ABSOLUTE_DIR` below are absolute paths; `REV` is the measured revision, not automatically C0. Commands are recorded recipes; this scribe counted artifacts/Git objects only.

| Claim | Exact counting recipe | Observed baseline | Observed candidate / limit |
|---|---|---|---|
| C1 | `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c1/measure.py --lane LANE --rev REV --work EMPTY_ABSOLUTE_DIR --explain` | Instrument-only overlay `25480068647a`: rows=0/51, total=154, PASS=false | C0 integration probe: rows=51/51, fixed=37, open=13, declined=1, thisround=8, panel=4/5, total=0, PASS=true. Independent W2 ExecDry records C0 exit 0. Not canonical admission. |
| C2 | `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c2/measure.py --lane LANE --rev REV --work EMPTY_ABSOLUTE_DIR --explain` | Same overlay: refusal element shortfall=2, total=2, PASS=false | Committed W1 honest receipt measures **0fdb71d26fab**, total=0, PASS=true, not C0. **Not admitted**: bent runner makes frozen counter pass without executing rows. |
| C3 | Contract recipe: `grep -rl '2406.09843' corpus/knowledge` piped to `wc -l`, then `grep -cE '^ {0,3}\| S(286|287|288) ' corpus/SOURCES.md` | Git-object count: 0 matching entries, 0 new rows; 145 source rows | C0 Git-object count: 1 matching entry, S286/S287/S288 present; 148 source rows. Census/content presence is not semantic source approval. |

Exact executed counting expressions, definitions and outputs: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2ScribeEvidence-receipts/observations.json`. Snapshotted receipt text and per-artifact commit provenance: `receipt-snapshot.json` beside it. Full paths are retained in facts JSON.

## Gates and source census

- Baseline source census: exit **0**, 15 W04 warnings + 1 W01 warning; `tameshi ok`. Scratch after-append census: exit **0**, 16 W04 + 1 W01; extra W04 is S288's duplicate Atlassian URL. This is **scratch after**, not final candidate/round-close census.
- Final required census command, from deciding-run.sh: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`. Original baseline/scratch full argv is not recorded in those receipts. Final close census result **not observed**.
- Content precheck at `0fdb71d26fab`: floor=64, candidate=47, lost=17 **RED**. Contract requires restoration; intent is not restoration evidence.
- Final 18-monitor no-harm and deciding-run receipt: **not observed**. Counter selftests 110/110 and 23/23 are lesson-reported instrument tests, not claim execution or close-gate evidence.
- C0 integration probe is present in the working tree but `git show C0:<probe-path>` exits **128**; it is not silently called committed evidence. W2 ExecDry is likewise concurrent W2 evidence.

## Waves and empty/dead-seat calibration

Committed W1 handoff: **67 rows, 52 nonempty terminal outputs, 15 empty outputs**. Keys are only `name`, `agent`, `output`, `note`: no callback status or agent id. Thus completed/dead totals and provider error text are **unknown**, not 52 completed / 15 dead and not zero errors.

Empty identities: `T58W1ScoutCT`, `T58W1ScoutReg`, `T58W1ScoutKagi`, `T58W1ScoutPin`, `T58W1CritClaims`, `T58W1CritDisc`, `T58W1CritBlind`, `T58W1CritC1`, `T58W1CritC2`, `T58W1Mut01`, `T58W1Mut02`, `T58W1Mut03`, `T58W1Sent01`, `T58W1Sent02`, `T58W1CritC3`. No matching MD/JSON reports were present for these identities when counted. No credit assigned to them.

W1 role counts: reviewer 18, executor 32, scout 4, connector 1, critic 6, revenger 1, mutation-tester 3, sentinel 2. W2 registry: **40 members** (reviewer 27, critic 3, mutation-tester 2, sentinel 2, executor 3, connector 1, scout 1, scribe 1). Combined registered **107**; this is not a terminal outcome total. W2 completion/death counts unavailable at snapshot.

## Finding: verbatim conflict for canonical judge

Lesson §Wave-1 decisive falsifiers says: **“The real executor on the same fixture yields only `held=1/3`.”** Wave-1 JSON repeats 1/3. But committed `T58W1RevengerC2-receipts/attack-b-out.txt` says:

```text
ROW c2-fx-ok expect=0 got=3 differs
ROW c2-fx-drift expect=3 got=3 held
ROW c2-fx-unresolvable expect=2 got=2 held
```

Executed receipt-count expression `sum(x.endswith(' held') for x in rows), len(rows)` yields **2, 3**. Preserve this discrepancy; do not repeat 1/3 as observed fact. The attack still falsifies admission: its frozen-counter output is `held=3/3 mutants=3/3 total=0 C2_R58_PASS=true`, while the honest executor rejects the acceptance row. Recorded attack command is `python3 attack.py`; not rerun by this scribe. Driver and original stdout are committed W1 evidence.

## Scope and artifacts

Touched only this seat's MD, JSON and receipts directory. No production/fleet/prior-evidence edits, git mutation, judge, dispatch, install, commit, push, publish or deployment. No scratch created; none remains. No tool installations.

Facts: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2ScribeEvidence.json`. Receipts: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2ScribeEvidence-receipts/` (`observations.json`, `counts.json`, `receipt-snapshot.json`). Self-evaluation in facts JSON: 4/5 per axis; missing final gates and authoritative terminal callbacks explicitly bound this report.
