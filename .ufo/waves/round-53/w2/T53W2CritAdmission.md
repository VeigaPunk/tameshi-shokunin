# T53W2CritAdmission — pre-closure admission audit (round 53, wave 2)

Seat: T53W2CritAdmission (critic, calibration). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Snapshot basis: lane HEAD `651773ab9e3295777a087c033e620ea81b9717b6` (C5, "six-leg/using-ledger
anchor re-derivation, standing-rules scratch-shape wording"), content line C* `a41195df` → C**
`5b703c6f` → C*** `ceb372c` → C4 `a977394` → C5 `651773a`. Freeze of record: `9e09db2`
(amendment 7, disclosed in `freeze.json` with `prior_freeze 7d8aaac676cbcb6379f57659e7c3c4c12150a815`
— the freeze named in the seat assignment, amendments 1-6). All commands run read-only over git
objects / fleet; counters run from freeze bytes extracted to seat scratch.

**Bottom line: NOT ADMISSIBLE AS THE TREE STANDS. One fatal frozen-counter defect
(F-1) makes C1_R53_PASS unprintable at any revision, and one kill-rule gate item
(F-2) would make the deciding run refuse before any counter runs. C2 verifies clean
now; census is clean; no-harm is 11/12 with the coldread floor RED pending the re-key.**

---

## F-1 (FATAL, OPEN) — frozen c1 counter's rekey-dir arm can never see a rekey dir → `rekey-dir-count=0` at every revision → C1_R53_PASS structurally unreachable

Frozen `c1/measure.py` (sha `da891491…`, byte-identical freeze→HEAD) lists rekey dirs with:

```
git -C <lane> ls-tree --name-only <rev> .ufo/evidence/round-21/coldread
rekey_dirs = [n for n in ... if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n)]
```

`git ls-tree --name-only <rev> <path>` **without a trailing slash returns only the directory
entry itself** (`.ufo/evidence/round-21/coldread`), never its children — so `rekey_dirs` is
empty at every revision and `problems.append('rekey-dir-count=0')` fires unconditionally
(measure.py lines 95-100). One problem ⇒ `total ≥ 1` ⇒ `C1_R53_PASS=false` no matter what the
re-key produces.

Evidence:

1. Ran the frozen c1 at C5: `C1_R53: rev=651773ab9e32 credited=36 lost=28 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false` (exit 1), with `PROBLEM rekey-dir-count=0` in the output despite the rekey dir `rekey-r53-a41195dfc13a` existing at C5 (`git ls-tree --name-only 651773a .ufo/evidence/round-21/coldread/` shows it; 9 ledger entries reference it).
2. Fixture proof (scratch repo, dir `a/b/rekey-r53-deadbeefc0de` with content present): the exact counter command `git ls-tree --name-only <rev> a/b` prints `'a/b\n'`; regex hits `[]`. The trailing-slash form lists the child but as a full path (`a/b/rekey-r53-deadbeefc0de`), which still fails the bare-name `fullmatch`. Both forms fail; the arm is dead code either way.
3. Corroborated by wave-2 peer `T53W2MutCounter.md` ("pristine already fails … mutant merely removes one diagnosed problem").

Impact: the deciding run greps `C1_R53_PASS=true` from `c1.stdout`; with this arm the frozen
counter can only ever print `false`. **The counter must be amended (amendment 8) — e.g.
trailing-slash `ls-tree` plus basename matching — and re-frozen; no content-side re-key can
compensate.** Wave-1 seat T53W1LabLint (A2/A3) and the phase-A controls (2 BASE negatives only)
did not exercise this arm positively, so the freeze pipeline missed it.

## F-2 (OPEN, kill-rule gate 0) — control receipts do not descend from the freeze

Deciding run gate: `git log -1 -- <controls.stdout|controls.exit>` → `a36d3e5` (phase-A,
"scored at freeze bytes"), then requires `merge-base --is-ancestor <FREEZE> a36d3e5`.
`a36d3e5` is an ancestor of freeze `9e09db2`, not a descendant ⇒ the gate prints
`DECIDING_REFUSED control-receipt-not-after-freeze` and exits 3 before anything runs.
Verified directly against freeze `9e09db2`. The receipts must be re-committed (re-affirmed or
re-scored) in a commit descending from the final freeze. (Round 51 needed exactly this
repair after its re-freeze; the mechanism is established.) Note: with F-1 unfixed, re-scored
receipts would still only re-prove the two BASE negatives.

## F-3 (OPEN) — phase-B break-one controls are defined but have no receipts

`control/break-fixtures.py` defines `CTL_C1_NOTRACE / BADREADER / WRONGREV`, `CTL_C2_TMP /
CR47` plus a positive probe, but `control/` contains only `controls.{stdout,exit,stderr,py}`;
no phase-B receipts exist, and `.ufo/evidence/round-53/after/` does not exist. The LOG/report
narrative describing re-key, deciding, and phase-B results in the past tense is aspirational
as of this snapshot. The positive probe necessarily fails on C1 until F-1 is fixed.

---

## Acceptance requirements, item by item

| # | Requirement | Status | Evidence |
|---|---|---|---|
| 1 | C1 verifies on frozen counter at final rev | **OPEN — F-1 (fatal)**; also re-key itself pending (rekeyed=0/30, readers=25/30 at C5; `integrate/rekey.py` modified, `resolutions.json` untracked, w2r3 final re-reads at C5 dispatched) | frozen c1 run at C5 (above); fixture proof (above) |
| 2 | C2 verifies on frozen counter | **HOLDS at C5** | `C2_R53: rev=651773ab9e32 tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=2 docs=ok total=0 C2_R53_PASS=true`, exit 0 (frozen bytes, TMPDIR=seat scratch) |
| 3 | No axis harmed — no-harm.sh, every line | **11/12 ok; `coldread-floor` RED pending re-key** — per-line output below | runs at C**, C***, C5 |
| 4 | Frozen coldread precheck GREEN (64/64, exit 0) | **OPEN** — at C5: `ECHECK floor=ef19d8e1e7ba floor_credited=64 cand=651773ab9e32 cand_credited=36 lost=28 RED` | c1 embedded precheck output |
| 5 | Control receipts committed ≥ freeze | **OPEN — F-2** | `merge-base --is-ancestor 9e09db2 a36d3e5` fails |
| 6 | Phase-B break-one receipts | **OPEN — F-3** | `control/` lacks them; none committed |
| 7 | FROZEN_UNCHANGED=1 | **HOLDS now** — `git diff 9e09db2..651773a -- <11 frozen paths>` empty; note freeze moved 7d8aaac→9e09db2 (amendment 7, properly disclosed: no-harm.sh syntax fix + tools-scope widened to the 7 C2 tool patches, `prior_freeze` chain intact, embedded hashes match HEAD blobs) | git diff (empty); freeze.json |
| 8 | Working tree clean at measured rev | **OPEN (in-flight)** — lane dirty: `M integrate/rekey.py`, `M LOG.md`, `M` 4 wave reports, `D w2r.ready.partial`, untracked `resolutions.json`, `w1/T53W1LabLint.md`, 5 w2 reports, `w2r*` markers | `git status` at HEAD |
| 9 | Exactly one deciding invocation per counter | PENDING — no `after/` dir | `ls .ufo/evidence/round-53/after/` → absent |
| 10 | Fleet source census exit 0 | **HOLDS** | `scripts/sources-census.sh validate --root <fleet> tameshi` → exit 0; only 4 pre-existing W04 duplicate-url warnings; tameshi row `ok` |
| 11 | LOG entries | r52 entry **HOLDS** (names bcba892→f1a3246 + wrap-up). r53 entry exists; closure append in working tree — written in past tense about re-key/deciding/phase-B that have not happened yet; must only be committed once true | `git diff LOG.md` |
| 12 | Report sections incl. per-box SHONEN (R52.6) | **DRAFT ONLY** — `.ufo/reports/round-53/tameshi.md` (fleet root, untracked) has the required headings (Work performed / Landed changes / Before → after / Sources & frontier / Trend verdicts / SHONEN / continuation) but every content section is "(to be completed)"; SHONEN is not per-box yet; "wave 2 (32 attack seats)" conflicts with the 40-seat dispatch + w2r/w2r2/w2r3 residuals and must be reconciled; "all pushed" must be true at filing | read of draft |
| 13 | Push scope | **HOLDS so far** — HEAD==origin/master==651773a; remote is the lane's own repo; no fleet-root tracked file touched by tameshi | `git rev-parse HEAD origin/master`; fleet `git status` |
| 14 | Misroot sweep | **HOLDS for tameshi** — no tameshi writes outside the lane + its report draft; fleet-root untracked tameshi file is only `.ufo/reports/round-53/tameshi.md` (expected); `/tmp` has only `/tmp/hyaku` (orchestrator-level, not seat litter); sibling-lane untracked files (`.scratch/closure-mado-r50.json`, `.ufo/reports/round-56/mori.md`) noted, outside this lane's scope | fleet + lane status; `ls /tmp` |
| 15 | Wave accounting | IN PROGRESS — w1 settled (74 files, 44 seats per spec-w1); w2 at 59 files (21 re-readers + reviewers/scouts/executors/critics/scribe/connector/mutation-tester per 40-seat dispatch); residuals w2r (R1,R4 landed), w2r2 (3 seats), w2r3 (3 seats, "FINAL residual re-read" at C5). One wave-1 report (`w1/T53W1LabLint.md`, the A2/A3 findings) is still uncommitted | `ls` of wave dirs; dispatch JSONs |

## no-harm.sh, every line (amended monitor, freeze bytes)

At C** `5b703c6f` (also C5 `651773a`; identical except coldread line: C** credited=33, C5 credited=36, C*** credited=38):

```
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=6 credited=33 RED        ← only RED; needs 64 after re-key
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-134 136 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [M:tools/bash-witness-study.py M:tools/context-capture.py M:tools/env-diff.py M:tools/evidence-disposition.py M:tools/pin-disposition.py M:tools/registry-check.py M:tools/registry.json M:tools/repeat-control.py M:tools/round21-measure.py] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none ...] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
NOHARM r53-scratch-hygiene tmp_hits=0 ok
```

Context on the monitor itself: the pre-amendment-7 frozen `no-harm.sh` (sha `e4e6b7ad…`) died at
line 40 (`bash -n`: "unexpected EOF while looking for matching `'`") after printing only 11
lines — I reproduced this at C*** with the original bytes. Wave-1 `T53W1LabLint` filed it (A2)
plus the tools-scope allow-list miss (A3); amendment 7 (`9e09db2`) fixed both and is verified
working above (12 lines print). That amendment is also why the freeze of record is no longer
the seat-assignment freeze.

## Closure checklist (exact remaining work, in order)

1. Amend + re-freeze c1/measure.py rekey-dir listing (F-1); the re-freeze resets the receipt-descent clock, so re-commit control receipts **after** the final freeze (F-2), then score phase-B break-one receipts (F-3) — whose positive probe needs the fixed counter.
2. Land the re-key of all 30 sections at the final content revision (w2r3 re-reads at C5 are the last inputs), bringing `cand_credited` to 64 (precheck/no-harm coldread-floor).
3. Commit the working tree (rekey.py, LOG.md append — only once its past-tense claims are true, wave stragglers incl. `T53W1LabLint.md`, resolutions.json, w2r markers).
4. Deciding run with the final FREEZE; produce `after/`; 12/12 no-harm; census exit 0; both counters print PASS from receipts.
5. Finish the report: real Landed changes, Before→after from deciding receipts, per-box SHONEN lines, trend verdicts in the allowed vocabulary, corrected wave accounting (w1 44 / w2 40 + residuals), accurate push claims; commit it to the fleet repo under the lane identity (lands last, cites final HEAD).
6. Push the lane; keep the fleet-root report commit within tameshi's own paths.

Tool installs this seat: none (host tools sufficed; pacman guard respected; pacman not run).
Scratch: everything under `/fast/scratch/hyaku/tameshi-r53/w2/T53W2CritAdmission`, deleted on yield.
