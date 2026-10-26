# T50RevDeciding — line-by-line review of round-50 deciding-run.sh and no-harm.sh

Scope: `.ufo/evidence/round-50/deciding-run.sh` (55 lines) and `.ufo/evidence/round-50/no-harm.sh` (35 lines),
read-only, against working-tree copies verified byte-equal to the frozen bytes (`git status --porcelain` shows
no tracked modification to them; `git diff --quiet cdbf24c0 HEAD -- <15 FROZEN paths>` is quiet at the current
tip 4afb060c, re-verified in a scratch clone). One live execution: `bash .ufo/evidence/round-50/no-harm.sh
/home/vgpnk/Projects/shokunin/tameshi-shokunin e3729de862f73ae080d98fcf522a7081ce16e40a` (output pasted below).
One fixture probe in a shared scratch clone (toplevel asserted) demonstrates F1. The deciding run itself was
NOT executed (it is the L1's single invocation). No tools installed. Scratch
`/fast/scratch/hyaku/tameshi-r50/T50RevDeciding` deleted before this report.

## Verified clean (checked, no defect)

1. **Gate 0 mechanics and observed receipts.** The gate checks exactly the four files the harnesses write
   (deciding-run.sh:23), existence at REV (:25 `git cat-file -e "$REV:$f"`) and that each receipt's
   last-touching commit descends from FREEZE (:26-27). At the current tip all four are committed by f87910f,
   a child of freeze cdbf24c0 (`git merge-base --is-ancestor cdbf24c0 f87910f; echo $?` → 0). Contents carry
   the frozen expectations: CTL_0/OPEN/PLANOPEN/DECLINE/FAB all `exit=1 … C1_R50_PASS=false` (CTL_FAB reaches
   fixed=40 but `fixed_this_round=2` → `this_round_short=3`, total=5 — the after-base floor is what refuses
   it, exactly as the contract's cannot_see predicts), `C1_CONTROLS: expected_false_all=true`;
   CTL_ABSENT/CTL_IDENTITY `C2_R50_PASS=false`, CTL_REF `exit=0 … C2_R50_PASS=true`,
   `C2_CONTROLS: expected_false_all=true`.
2. **Second-invocation refusal precedes all effects.** :29 checks `$OUT/{c1,c2}.start` before scratch
   creation (:30) and before the first receipt write (:37), so a refused or killed pre-receipt run re-invokes
   cleanly.
3. **Committed-bytes execution for the counters, no-harm itself, the precheck, and both panels** (the T49
   RevDeciding F1/F2 fixes): c1/measure.py, c2/measure.py, no-harm.sh extracted from REV blobs (:31),
   precheck (:32), hidden panel with a proper `DECIDING_REFUSED hidden-panel-not-revealed` exit-3 gate (:33 —
   T49 F2 fixed), public panel from REV (:34); all executed from `$SCR/code` (:38,:41,:46,:49). The c2
   counter digest-verifies both panels against the contract pins (c2/measure.py:56-57, :210-218;
   HIDDEN_SHA256 `5c14e9a6…` equals contract `hidden_panel_sha256`), digest-pins the frozen generator at
   GEN_REV 7d3d977f (:194-197; blob present in the lane) and the guard (guard_pin term fails closed with a
   BASE fallback, :202-205). Hidden-panel custody intact today: not at HEAD, not on disk
   (`git cat-file -e HEAD:.ufo/evidence/round-50/c2/panel-hidden.json` fails; `ls` shows only measure.py).
4. **Receipt order.** c2.start :45 before the c2 invocation :46, c2.end :47 after; c1.start :48, run :49,
   c1.end :50; each `.exit` is the command's own `$?`. c2 runs before c1 — no contract constraint between
   them.
5. **Exit map complete.** 0 all-ok; 1 accumulated (:37,:39-40,:41-42,:43-44,:51-52); 2 usage/cd/rev-parse/
   extraction (:14,:19,:20,:21,:31,:32,:34); 3 refusals (:22,:25,:27,:29,:33). Every refusal precedes the
   first receipt write.
6. **Scratch discipline.** HYAKU_SCRATCH-based scratch (:18,:30; no-harm.sh:10-12 with EXIT trap; precheck
   scratch with trap), TMPDIR exported for children (:30), no `/tmp` literal in any of the three scripts
   (`grep -n '/tmp' <the three scripts>` → only the "never /tmp" comment). The c2 counter creates its work
   dir, requires it empty, and points child TMPDIR at it (c2/measure.py:190-193) — compatible with the
   deciding run's fresh `--work "$SCR/c2"` (:46). c1's tempfile use is selftest-only (c1/measure.py:311).
7. **Ten monitors, right floors, verified live.** Round 49's nine with the cold-read floor raised to
   score>=8 / credited>=64 (no-harm.sh:16; base observed 8/64), the registry floor raised to 130 (:24;
   observed exactly 130), commandD `recorded_cases=9 depth_score=9` (:13-14), r45-freshness
   population=73/fresh=71, r45/46/47 coverage equality strings, S160-count=1, tools-scope allowing only
   `A:tools/shrink-case.py` and `M:tools/pbt-staged-id.py` (:30, matching the contract's tools scope), plus
   the r49 generator capability line whose hardcoded expected string (:34) was reproduced byte-equal by the
   live BASE run. All monitor pipelines are fail-closed (a failed child yields an empty/short capture that
   fails the string compare → RED), and the `NOHARM_OK_COUNT=10` gate (:40) catches a crashed no-harm.
   Header documents both floor raises (no-harm.sh:3-4).
8. **Frozen path list sane today.** All 15 entries exist at FREEZE (`git cat-file -e cdbf24c0:<path>` →
   OK ×15; no vacuous diffs). Correctly excludes the ledger (corpus/routed-defects.json), both C2 panels
   (revealed post-freeze, digest-pinned), the control receipts (committed after freeze by design), and wave
   dirs; includes the executed code and the C2 target guard; the precheck omission T49 F7 flagged is fixed.
   `__pycache__` under `.ufo/evidence/round-50/c2/` is gitignored (.gitignore:4), not committed.

## Findings (severity order)

### F1 (medium — repeats T49RevDeciding F1+F7, fix partial): five no-harm children and the precheck's child still execute working-tree bytes; the header's cleanliness claim is unenforced
- `no-harm.sh:15,17,19,25,27` run `python3 .ufo/evidence/round-21/coldread/measure.py`,
  `.ufo/evidence/round-45/freshness/measure.py`, `.ufo/evidence/round-45/coverage/measure.py`,
  `.ufo/evidence/round-46/coverage/measure.py`, `.ufo/evidence/round-47/coverage/measure.py` — relative
  paths resolved against cwd=$LANE (no-harm.sh:11), i.e. working-tree copies, although no-harm.sh itself runs
  from REV bytes (deciding-run.sh:31,:38). `coldread-precheck.sh:14-15` likewise executes
  `.ufo/evidence/round-21/coldread/measure.py` from the working tree inside a REV-bytes component.
- deciding-run.sh:8-9 claims "the counters, no-harm and the precheck run from the bytes committed at REV …
  never from the working tree; the working tree must be clean" — false on both halves: no
  `git status --porcelain` or `git rev-parse HEAD` check exists anywhere in deciding-run.sh, and four of the
  five (r45 freshness/coverage, r46/47 coverage) are absent from FROZEN (:36), so even *committed* drift to
  them would not trip :37 (T49 F7 repeat).
- Probe (shared clone, `git clone -q --shared`, toplevel asserted): honest monitor input
  `rows=3 entries=3 C3_R47_PASS=true`; after an *uncommitted* replacement of the working-tree
  round-47/coverage/measure.py, input becomes `rows=999 entries=999 C3_R47_PASS=false` while
  `git diff --quiet cdbf24c0 HEAD -- <15 FROZEN paths>` stays quiet. The mechanism is direction-symmetric: an
  edit printing the expected ok line forces the monitor green. Monitor verdicts — which feed rc (:39-40) —
  are therefore controlled by uncommitted bytes.
- Fix: extend the :31 extraction pattern to the five measures (deciding-run extracts them; no-harm/precheck
  take their directory via env or `$0`-relative resolution), or gate 0 asserts
  `git -C LANE rev-parse HEAD = REV` plus `git -C LANE status --porcelain --untracked-files=no` empty; add
  the four r45/46/47 paths to FROZEN.

### F2 (medium — repeats T49 F3): pre-counter verification failures spend the kill-ruled invocation
FROZEN drift (:37), no-harm RED/ok-count (:39-40), precheck (:41-42) and census (:43-44) only accumulate rc;
the counters still run (:45-50) and write `.start` receipts, so a repairable failure cannot be repaired — a
second invocation is a miss by the kill rule (round-48's attempt-3 burn is the precedent). Fix: promote
frozen drift and no-harm RED to exit-3 refusals before receipts are written; keep the honest-stop receipts
for the rest.

### F3 (low — repeats T49 F4): gate 0 admits receipts committed in the freeze commit; REV descent from FREEZE unasserted
:27 `git merge-base --is-ancestor "$FREEZE" "$c"` is true when `$c` == `$FREEZE` (receipts inside the freeze
commit cannot have been scored at the frozen bytes), and nothing asserts REV descends from FREEZE (:20-21).
Observed clean today: receipts last touched by f87910f, a child of cdbf24c0.
Command: `git merge-base --is-ancestor cdbf24c0 f87910f; echo $?` → 0.

### F4 (low — repeats T49 F5): gate 0 never checks receipt content; `.exit` receipts are not verdicts
:24-28 checks existence + ancestry only; a committed receipt set with CTL_REF missing or controls printing
PASS=true passes the gate. The `.exit` files record harness rc, not verdicts — observed
`control/c1-controls.exit` = 0 while every CTL line inside `c1-controls.stdout` says exit=1. Observed
contents are correct (see Verified clean 1). Fix: grep the committed receipts for the frozen expectation
lines before running.

### F5 (low — repeats T49 F6): second-invocation refusal is OUTDIR-keyed only
:29 `[ -e "$OUT/$k.start" ]` — a re-invocation with a fresh OUTDIR is uncaught, and there is no
receipts-already-at-REV check. The kill rule's "second invocation is a miss" remains an honor-system gate
across OUTDIRs.

### F6 (low): FROZEN list is never validated for existence
A mistyped path diffs vacuously. All 15 verified present at FREEZE today (`git cat-file -e cdbf24c0:<path>`
per path → OK ×15), so no active typo — but the guard is one `git cat-file -e` loop away.

### F7 (low — partial repeat of T49 F9): no EXIT trap in deciding-run.sh
The pre-scratch refusals are clean, but exits after :30 (extraction failures :31,:32,:34 exit 2; hidden-panel
refusal :33 exit 3) and signal interruptions leak `$SCR`; cleanup happens only at :53. The T49 F9 main fix
(`rm -rf "$SCR"` before mkdir, :30) landed; no-harm.sh:12 has the trap — deciding-run.sh does not.

### F8 (low — repeats T49 F8): argument/OUTDIR/scratch handling
No argument-count check (:13; fewer than 4 args dies on `set -u` with status 1, not the documented 2/3).
OUTDIR is documented "existing, EMPTY directory inside LANE" (:4) but :22 checks only `-d`: no emptiness, no
containment. A relative `HYAKU_SCRATCH` (:18) resolves SCR inside the lane after `cd "$LANE"` (:19),
writing scratch into the read-only lane.

### F9 (low — repeats T49 F10): no-harm.exit is not a verdict
no-harm.sh has no rc accumulation; its last statement is an echo (:35), so it always exits 0 and
`no-harm.exit` is always 0 even with RED monitors. The verdict lives only in stdout (:39-40); a
receipts-only reader of the `.exit` files would conclude no-harm passed.

### F10 (info, documentation): two label drifts
deciding-run.sh:5 says "Carried from round 49 (QUALITY 99)" while contract.json's no_harm line says
"QUALITY 98 precheck". The deciding run's census receipts are named `census.*` (:43-44) while the contract's
census clause names `census-start.*` — the deciding census is the contract's *end* census, and committed
census-start.* receipts exist at cdbf24c0; behavior is correct, the contract wording just names only the
start pair.

## Live no-harm output (command: `bash .ufo/evidence/round-50/no-harm.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin e3729de862f73ae080d98fcf522a7081ce16e40a`; exit 0)

```
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-130 130 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
```

## Residual risk and verification gaps
- The deciding run was not executed; gate-0 refusal paths and receipt ordering are verified by reading plus
  targeted probes, not a live refusing invocation. A fixture rehearsal of a refusing invocation would
  exercise F2's promotion.
- The capability line's byte-equality is confirmed only at REV=BASE; at the real REV the monitor depends on
  the generator's seeded determinism (observed once).
- The C1/C2 counters themselves were not run (their seats' instruments); receipt contents are quoted from
  the committed files, not re-derived.
- F1's probe used REV=BASE; the provenance property is REV-independent (FROZEN quiet FREEZE→HEAD before and
  after the tamper).

## Summary
- Reviewed deciding-run.sh (55 ln) and no-harm.sh (35 ln) at bytes equal to the freeze; all 15 FROZEN entries exist at cdbf24c0 and no frozen path has drifted to the current tip.
- T49 F2 fixed (hidden-panel reveal is a DECIDING_REFUSED exit-3 gate); counters/no-harm/precheck/panels run from REV blobs; receipts, exit map, scratch discipline, and both panel digest pins verified correct.
- Live no-harm at BASE: ten monitors, ten `ok`, exit 0; floors as documented (coldread 8/64, registry 130, commandD 9); capability line byte-equal to the hardcoded string.
- Medium F1: five no-harm children + the precheck's child still execute working-tree bytes; "working tree must be clean" is unenforced and four measures are absent from FROZEN — probe shows an uncommitted edit flips a monitor verdict.
- Medium F2: frozen-drift/no-harm/precheck/census failures burn the single invocation instead of refusing.
- Low F3-F9 repeat known laxness: freeze-commit receipts admitted, receipt content unchecked, OUTDIR-keyed second-invocation refusal, FROZEN unvalidated, no EXIT trap, usage/OUTDIR gaps, no-harm.exit always 0; F10 two doc label drifts.
- No tools installed; scratch deleted; the deciding run itself left untouched for the L1.
