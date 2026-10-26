# T48W2RevQuality — review of QUALITY criteria 94-97 appended in round 48

Seat: T48W2RevQuality (a2w1, godspeed). Item: review the four criteria appended at the content
revision `c7586b9a` (`corpus/QUALITY.md:1380-1434`; diff `473336d9..c7586b9a -- corpus/QUALITY.md`,
+57/-0). Each must (a) cite its lesson at an existing `corpus/lessons/round-48.md` line, (b) be new
vs criteria 1-93, (c) be falsifiable, (d) have a committed falsifier receipt under
`.ufo/evidence/round-48/quality/` showing it firing on a fixture and passing on the repaired form;
falsifier scripts re-run in scratch and compared with receipts.

Revisions observed: `15b1521ea2e95d0d708059458c090e9f334adf32` (salvage), `c7586b9a10effc63b4bd327f976edc094c1bdc17`
(content), `17cc5ce141868454d05bf75ef5cd230e35f0cdf4` (tip at review time). Read-only probes only;
no lane file outside this report was written. Scratch `/fast/scratch/hyaku/tameshi-r48/T48W2RevQuality`
deleted before finishing; cited receipt contents are embedded verbatim below.

## Verdict

All four criteria are new, their lesson cites exist and say what the criteria claim, and all four
are falsifiable in form. As landed, however, the block fails its **own** criterion 97: criteria 94
and 95 cite falsifier receipts that exist at **no committed revision**, criterion 96 names no
receipt at all, and criterion 97's green leg ("the same command at the round-48 landing tip exits
0") is **false at every revision observable now**. Block 95 of `falsifiers.sh` is vacuous today
(its input receipt is absent; the script still exits 0), and block 96's stated premise "one
revision" is false for its own inputs.

## Findings

### F1 [high] — criteria 94/95 cite receipts absent at every committed revision; criterion 97's green leg fails at the tip

- `corpus/QUALITY.md:1398` (criterion 94) cites receipt `quality/c94-96-falsifiers.stdout`;
  `corpus/QUALITY.md:1418` (criterion 95) cites `control/c1-controls.stdout`. Both are absent at
  `15b1521e`, `c7586b9a` and the current tip `17cc5ce`:
  `git -C <lane> cat-file -e c7586b9a:.ufo/evidence/round-48/quality/c94-96-falsifiers.stdout` →
  absent (same for the other revision and for `control/c1-controls.stdout`);
  `git log --all --oneline -- <each path>` → empty (never committed).
- These are exactly the two `MISSING` lines the committed red receipt
  (`.ufo/evidence/round-48/quality/pointer-check-red-15b1521.stdout`) flags at `15b1521e` — i.e.
  the defect criterion 97 was written from is still live for the round-48 block itself at its own
  landing revision.
- Probe (scratch copy of `pointer-check.py`, unmodified):
  `python3 pointer-check.py --lane <lane> --rev c7586b9a --file corpus/QUALITY.md --start "## Criteria appended — round 48"`
  → `checked=11 missing=2 skipped=0`, the same two `MISSING` lines, exit 1. Identical result at
  `17cc5ce`. Criterion 97's falsifier claims "the same command at the round-48 landing tip exits
  0" — false at every revision observable now, and no committed green receipt exists (`after/` is
  empty; `quality/` holds only `falsifiers.sh`, `pointer-check.py` and the two red/selftest
  receipts).
- Disclosure state: `LOG.md:2364` (attempt-2 correction) says attempt 2 "runs C1's CTL_A-E with
  the frozen harness before the deciding run; the receipt QUALITY 95 names lands with them" — so
  `c1-controls.stdout` is disclosed-pending. **`c94-96-falsifiers.stdout` is disclosed nowhere**:
  `deciding-run.sh` (read in full, 39 lines) writes only
  `after/{frozen,no-harm,coldread-sections,c2,census,c1,deciding-run}.stdout` — it produces
  neither receipt — and no seat in `.ufo/waves/round-48/a2w1-dispatch.json` is assigned to commit
  `c94-96-falsifiers.stdout` (4 `falsifiers` mentions; the mutation-audit seat runs the script in
  scratch only). Unless the L1 explicitly runs `falsifiers.sh` and commits its output, criterion
  94's receipt pointer never resolves and criterion 97's green leg stays false at the round-48 tip.

### F2 [medium] — block 95 is vacuous as committed, and `falsifiers.sh` exits 0 despite VACUOUS

Probe (scratch copy, `HYAKU_SCRATCH=$S TMPDIR=$S bash falsifiers.sh`), observed output:

```
WEAK-CITE ### Reject — package entry `r8-predictive-test-selection-cost.md`
rejects=1 weak=1
rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
grep: /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/control/c1-controls.stdout: No such file or directory
grep: /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/control/c1-controls.stdout: No such file or directory
CRITERION-95-FALSIFIER-VACUOUS
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-OK
falsifiers exit=0
```

- Block 95 (`falsifiers.sh:32-35`) cannot fire: its only input is the absent
  `control/c1-controls.stdout`; it prints `CRITERION-95-FALSIFIER-VACUOUS`. So criterion 95 has
  **no observable falsifier today** — its red/green evidence is entirely prospective.
- The script has no aggregate status: it exits 0 even with a VACUOUS block, so a consumer
  scripting on the exit code sees success. (Blocks print OK/VACUOUS lines only.)
- Fragility, contingent until the receipt lands: block 95 requires ` total=0 ` with a trailing
  space (`falsifiers.sh:35`); that holds only while `total=` is followed by another field (`rev=`)
  on the CTL line, per the round-47 line shape (`round-48.md:156`). If a future CTL line ends at
  `total=0`, the check silently vacuouses. The `^CTL_B .*C1_R48(_PARTIAL)?: ` and ` total=[1-9]`
  patterns otherwise match `run-controls.py`'s documented output (`CTL_<X> C1_R48: ...`,
  `run-controls.py:12-22`, printed at `:415-420`).

### F3 [medium] — block 96's premise "one revision" is false for its own inputs

- `falsifiers.sh:36` comment: "one statement, one revision, one counter: only the --work placement
  differs"; criterion 96 (`corpus/QUALITY.md:1425-1426`) says the two receipts "print different P1
  tuples for the same statement and revision". Both are wrong about the inputs:
  `.ufo/evidence/round-47/before/c1-at-freeze.stdout:45` → `rev=9acfbe21435e1976636a276448dee1d5e7155915`
  (the round-47 **freeze** commit), `.ufo/evidence/round-47/after/c1.stdout:45` →
  `rev=8b0e15d25ea598c0bf908d183fb410a085bf3a18` (the round-47 **content** revision). The block
  compares across two revisions and prints OK regardless (it never checks revision equality).
- Mitigating facts (verified): the counter blob `.ufo/evidence/round-47/calibration/measure.py`
  (`5ffb7ca6bbb7ef29…`) and the measured tool `tools/env-diff.py` (`3a48aeccc55bc5ea…`) are
  byte-identical at both revisions (`git ls-tree` at both revs), so the material variables are
  held; and the properly controlled same-revision pair the criterion demands **does exist** —
  `.ufo/waves/round-47/w1/T47ExecObsC.md:54,85` ran both placements at one rev with one counter
  (per `.ufo/waves/round-48/w1/T48RevenEnvDiff.md` §2: "Time, load and rev are held fixed; only
  the path string moves"). But block 96 does not run that pair; its OK is not evidence of "varies
  that cause alone" by the criterion's own standard.
- Also: neither round-47 receipt stamps its `--work` placement (`grep -i work` over both → no
  lines), so the parentheticals "(--work under `/tmp`)" / "(`/var/tmp`)" rest on
  `T48RevenEnvDiff.md`'s reconstruction (round-47 `deciding-run.sh:19` default), not on the
  receipts; the block cannot detect a placement mislabel.

### F4 [low] — criterion 94's falsifier is form-only, its bad fixture synthetic, and the historical refusal is outside `reject_check`'s domain

- `reject_check` (`falsifiers.sh:7-17`) scans `### Reject` blocks of a lessons file only. The
  historical mis-cited refusal was a wave-report **table row**
  (`.ufo/waves/round-47/w1/T47RevProvince.md:30`, cite cell `PROVINCE.md:14-18`, criteria "10, 2",
  no `Flip:`) — `reject_check` would never see it, so the falsifier does not (and cannot) replay
  the historical defect; it demonstrates the rule on a constructed fixture
  (`falsifiers.sh:23-27`).
- `falsifiers.sh:22` comment calls that fixture "the round-47 form" — inaccurate: the round-47
  refusal also carried criteria "10, 2" and lived in a different artifact class.
- The criterion discloses the limitation itself (`corpus/QUALITY.md:1398`: "The check reads the
  form, not the truth of the cited reason; the reason stays a spot-check item"), so this is a
  precision note, not a hidden gap.

### F5 [low] — criterion 97 overlaps criterion 72 without citing it, and "waits for them" is ambiguous against 72's write-time rule

- Criterion 72 (`corpus/QUALITY.md:846-852`, round 36) already requires a LOG.md entry's evidence
  file to exist **at write time**, re-resolved before the entry commits. Criterion 97 extends the
  check to SCORECARD/LOG/QUALITY/lesson blocks at the **landing tip** and allows a record drafted
  before its receipts to "wait for them" — for LOG.md entries, if "waits" is read as "lands now,
  resolves at the tip", it contradicts 72; if read as "the record is not landed until the receipts
  exist", it is consistent. The criterion cites 88 and 94-96 but not 72.
- Not a restatement: 97's new content is the revision-anchored check (`git cat-file -e TIP:path`),
  the broader scope, and "a pointer that resolves only in a later round … is a landing defect".
  But the 72 relationship should be stated in the criterion.

## Verified OK

- **Lesson cites exist and support the criteria.** 94 → `corpus/lessons/round-48.md:98-102`
  (`### Reject (re-stated)` for `r8-predictive-test-selection-cost.md`: `PROVINCE.md:14-18` named
  the weak reason, QUALITY 10 decisive) + `corpus/lessons/round-47-verifier-spotcheck.md:90`
  (`reason partly` row, §Discernment at `:81`). 95 → `round-48.md:320` ("the input CTL_B must
  refuse"), `:345` ("Row 1's fix is the R=3 counter and its control CTL_B"), `:354` (9/9 and 2/9
  under P1, `SCORECARD.md:2314` disclosed limit) + spotcheck `:102` (routed defect 1: "N ≥ 3 per
  profile, or a declared nondeterministic class"). 96 → `round-48.md:350-354` (`## Mistakes`
  attribution row). 97 → `round-48.md:356-360` (prospective-record row, salvage `15b1521e`, two
  absent receipts — matching F1's two paths exactly).
- **Novelty (grep over 1-93 at `c7586b9a`).** 94: no earlier criterion governs refusal-citation
  form (`decisive|weaker|mis-cit` below `:1382` → only criterion 22's "weaker rule", a different
  subject — attribution-repair selftests). 95: complements 11 (finite sample, never proves
  determinism — cited in the criterion), 71 (changed tool → new row), 76 (count equals committed
  tree), 84 (count pattern), 92 (deps clause — explicitly reconciled: "neither fixes the
  observation count"). 96: criteria 5/6/18/22's "attribution" concern finding attribution/repair,
  not observation causality. 97: extends 72 (see F5).
- **Falsifiability, observed.** 94 fires: `WEAK-CITE` + exit 1 on the bad fixture; passes:
  `rejects=2 weak=0` + exit 0 on the real lesson (both `### Reject` blocks carry the required
  cite + `Flip:` — `round-48.md:91-96` CORPUS.md rule 2, `:98-102` QUALITY 10). 96 fires: the two
  P1 tuples differ (`2/9 pass|1` vs `9/9 pass|0`) and `under_tmp` is present
  (`calibration/measure.py:101,395`). 97's red leg reproduced byte-exact against the committed
  receipt (diff clean for the QUALITY portion; the receipt additionally transcripts the LOG.md
  run, `checked=8 missing=0`), and the selftest reproduced exactly (`SELFTEST-MATCH`).
- **`under_tmp` behavior is attested, not just spelled**: committed selftest receipt
  `.ufo/evidence/round-48/selftest/c1-r48-selftest.stdout:74` — `PASS T63_work_under_tmp_refused
  work under /tmp refused without writing rc=2` (tracked at `c7586b9a`).
- **Committed receipts reproduced in scratch** (probe copies, unmodified scripts):
  `pointer-check.py --selftest` → 4 PASS + `POINTER_CHECK_SELFTEST: cases=4 failed=0`, exit 0 =
  `pointer-check-selftest.stdout`; red run at `15b1521e` → the receipt's QUALITY portion verbatim.

## Item-requirement scorecard (committed falsifier receipt, red on fixture + green on repaired)

| criterion | receipt cited at | committed? | red observed? | green observed? |
|---|---|---|---|---|
| 94 | `quality/c94-96-falsifiers.stdout` (`QUALITY.md:1398`) | **no** (absent at all 3 revs; no disclosed producer) | yes — my probe (`WEAK-CITE`, exit 1) | yes — my probe (`rejects=2 weak=0`, exit 0) |
| 95 | `control/c1-controls.stdout` (`QUALITY.md:1418`; note: not under `quality/`) | **no** (disclosed-pending, `LOG.md:2364`) | no — block VACUOUS today | no |
| 96 | none named in the criterion | **no** | yes — my probe (P1 tuples differ) | yes — my probe (OK) |
| 97 | `pointer-check-red-15b1521.stdout` + `pointer-check-selftest.stdout` (committed) + green at tip (uncommitted) | red+selftest **yes** | yes — reproduced byte-exact | **no — false at every observable revision** (2 MISSING at `c7586b9a` and `17cc5ce`) |

## Residual risk / verification gaps

- `c1-controls.stdout` is pending (L1 runs CTL_A-E before the deciding run per `LOG.md:2364`).
  When it lands, re-run `falsifiers.sh` and confirm block 95 prints OK (CTL_B `total>0`, CTL_E
  `total=0`, and the ` total=0 ` trailing-space match of F2).
- `c94-96-falsifiers.stdout` has no disclosed producer (F1). If the L1 does not commit it, the
  criteria block keeps violating criterion 97 at its own landing tip.
- The deciding run is in flight and may change the tree state described here; every observation
  above is stamped with the revision it was taken at.
- Block 95's CTL_B expectation depends on the six-leg leg's flake not failing in all three
  control rounds (P(fail)≈4/40 per round per `round-48.md:380-382`) — near-certain to fire, but
  not guaranteed; a `CTL_B total=0` would make the criterion's falsifier vacuous on that run.

## Tooling

No tools installed or upgraded (none needed); pacman untouched.

## Scratch

`/fast/scratch/hyaku/tameshi-r48/T48W2RevQuality` deleted before finishing (probe copies of
`falsifiers.sh`/`pointer-check.py`, the extracted `QUALITY.md` blob, and probe outputs lived only
there; all cited content is embedded above).
