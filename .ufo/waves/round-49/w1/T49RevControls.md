# T49RevControls — control design and committed control receipts (round 49)

Seat: T49RevControls (leaf, no dispatch). Reviewed the round-49 control design (harness code) and the
committed control receipts for C1 (CTL_0/J/K/K2) and C2 (CTL_ABSENT/CTL_FIX/WITNESS) against
`.ufo/evidence/round-49/contract.json` and `freeze.json`. Per seat bounds, c2 mutant names are
withheld and cited as M01..M12 only. No deciding receipts exist yet (`.ufo/evidence/round-49/after/`
is empty), so the ordering check is: controls ran and committed before wave 1, and `deciding-run.sh`
gate 0 enforces receipt-before-run at deciding time. Scratch root
`/fast/scratch/hyaku/tameshi-r49/T49RevControls/` was used for all probes and deleted before this
yield; probe receipts cited below are copied into this wave dir.

## Verification performed (all pass)

1. **Frozen bytes.** All 13 digests in `freeze.json` match on-disk bytes:
   `cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 -c "import json,hashlib; [print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()==w) for p,w in json.load(open('.ufo/evidence/round-49/freeze.json'))['sha256'].items()]"` → all True.
   The receipts embed the counters' self-digests: c1 `self=a055e9297cc9` (freeze `a055e9297cc9…`),
   c2 `self=f4971d02b8b1` (freeze `f4971d02b8b1…`) — command:
   `grep -h 'C1_R49:\|C2_R49:' .ufo/evidence/round-49/control/*.stdout | head`.
   `git diff --stat 14d03ea 6885adb` shows the freeze→controls commit adds only receipt files plus
   wave-1 spec files; no frozen code changed between scoring and commit.

2. **Timeline.** Freeze commit `14d03ea` 2026-10-26 17:15:08-03; `c1-controls.start`/`c2-controls.start`
   2026-10-26T20:15:18Z; `c2-controls.end` 20:17:01Z; `c1-controls.end` 20:19:43Z; controls commit
   `6885adb` 17:19:55-03; wave-1 spec commit `455b2cd` 17:20:13. Both `.exit` files are `0`.
   Command: `git -C . show -s --format='%h %ci' 14d03ea 6885adb 455b2cd` and
   `cat .ufo/evidence/round-49/control/c{1,2}-controls.{start,end,exit}`.
   Gate that will enforce ordering at deciding time: `deciding-run.sh:24-27` requires each control
   receipt's last-touching commit at REV to descend from FREEZE; `:29` refuses a second invocation;
   `:42-51` write start/end receipts around each counter.

3. **C1 harness does what the contract says** (`control/c1-controls.py`):
   - CTL_0 `:151` scores the lane at BASE with the frozen counter, work in `$HYAKU_SCRATCH`.
   - CTL_J `:152-153` clones at BASE (toplevel assert `:47-49`), `add_entries :72-93` appends one
     synthetic `record`-class entry per target section keyed to its **current** section sha with that
     heading's **latest** ledger inputs (records included, SKILL.md excluded, `latest_inputs :95-105`),
     no read rows, no section edits — the round-36 refresh shape.
   - CTL_K/K2 `:156-166`: `pinned_inputs :107-113` re-keys entries to each section's cited
     non-volatile, non-SKILL.md files; `mech_reads :116-134` writes one row per pointer (verdict
     `holds`, excerpt = first 60 collapsed chars of the pointed text; `absent` for file-less pointers;
     fleet HEAD for the external pointer); K2 additionally prefixes `SKILL.md` onto exactly the two
     bare map pointers with a once-only assert `:160-161`. Commits happen in the clones only.

4. **C1 must-fail controls fail for the stated reasons** (`c1-controls.stdout`, row detail in
   `c1-CTL_*.stdout`):
   - CTL_0 exit=1 PASS=false; every number equals the contract "before" line (sections=64 covered=57
     score=6 durable_covered=57/64 pointers=90 unresolved=9 unverified=81 total=105). Reproduced live
     in scratch against a clone at base: `T49RevControls.c1-CTL0-repro.stdout`, identical final line,
     exit 1.
   - CTL_J exit=1 PASS=false: covered=64 score=8 (the sha-refresh games coverage) but
     durable_covered=60/64 — 4 sections lapse under the record-append probe because the refreshed
     entries bind volatile record inputs — plus unverified=81 unresolved=9 → total=94. Fails precisely
     because a refresh without read rows cannot satisfy the pointer predicate.
   - CTL_K exit=1 PASS=false: durable 64/64 (inputs exclude the five volatile records), unverified=0,
     absent=6, unresolved=2 → total=2. Row detail (`c1-CTL_K.stdout`): the 2 unresolved are exactly the
     two bare map line pointers `:1294-1297` (#0) and `:1246-1270` (#1); the 6 absent are the six
     unresolvable bare path pointers (`mutate_driver.py`, `plans/round-N.plan.md`,
     `plans/round-N-record-draft.md`, `dispositions.json`, `verification.json`, `capture-context.py`),
     accepted per the counter's absent rule (`c1/measure.py:272-277`: only `pointer_kind == 'path'`
     may be read `absent`), which matches the contract predicate's "(or `absent` for an unresolvable
     path pointer)".
   - CTL_K2 exit=0 PASS=true total=0: the K→K2 delta is exactly the two prefixed pointers
     (`c1-CTL_K2.stdout:45-46`, both `ok`). The positive control demonstrates the counter's blind spot
     as the contract states: a read row that was never read (excerpt mechanically cut from the pointed
     text) and a pointer re-targeted without semantic checking.

5. **C2 harness does what the contract says** (`control/c2-controls.sh:16-24`): runs the frozen counter
   at `--rev FREEZE` three times (absent / `--generator-path` stub / `--witness`) and greps the
   expected verdicts (PASS=false twice, `witness_confirmed=12`) into its rc.
   - The counter enforces the named gate and panel identity: `materialize()` refuses a guard whose
     sha ≠ GUARD_SHA (`c2/measure.py:253`, GUARD_SHA `:45` = freeze.json's guard digest);
     `load_panel()` refuses panel bytes whose sha ≠ PANEL_SHA (`:232`, PANEL_SHA `:47` = freeze.json
     `panel_sha256`). So `panel_valid=1` in all three c2 receipts proves the hidden panel used is the
     pre-registered one without this seat reading it.
   - CTL_ABSENT exit=1 PASS=false: `generator=absent` (no generator blob in the freeze tree), all 12
     classes SHORT, `records-missing`, total=25 = absent 1 + classes_short 12 + (11−0) + records_bad 1.
     Matches the contract "before" state.
   - CTL_FIX exit=1 PASS=false: pristine run clean (exit 0, cases=400 violations=0 dump=400,
     oracle_disagree=0) but classes_short=4 (`indent_4_plus`, `id_4_plus_digits`, `no_collision`,
     `url_form_variant` = 0 — the stub's 14 fixtures never exercise them) and confirmed=6 < target 11
     → total=10. Fails for the stated reason ("confirm fewer than 11 mutants"), plus class coverage.
   - Stub verified (`control/c2-fixed-gen.py`): interface-compliant (`--guard/--seed/--cases/--dump`,
     last line `PBT_STAGED_ID: …`, exit 0/1), deterministic, runs the guard only via subprocess (no
     import/exec of guard code), 14 fixtures = the guard selftest's 4 analysis fixtures + 10 map cases
     (count: `python3 -c "import json;print(len(json.load(open('.ufo/evidence/round-49/control/c2-fixed-fixtures.json'))))")` → 14).
     Replay probe on current bytes: 400 cases violations=0 exit 0 (`T49RevControls.stub-replay.stdout`).
   - WITNESS exit=0 `witness_confirmed=12` over 11 cases (indices 0..10): the counter's kill path —
     generator exit 1 naming a counterexample whose dumped case makes pristine and mutant differ under
     `comparable()` (`c2/measure.py:329-349`) — is reachable. `comparable()` deliberately ignores the
     registry/staged sha fields (selftest `comparable-ignores-shas`), so only semantic differences
     confirm.
   - `--generator-path` is a counter flag used only by the controls (`c2/measure.py:433`);
     `deciding-run.sh:44` does not pass it, so the deciding run reads `tools/pbt-staged-id.py` from REV.

6. **Selftest receipts** (committed at freeze): c1 34 cases failed=0 exit 0; c2 11 cases failed=0
   exit 0. Re-run on current bytes, identical results:
   `T49RevControls.c1-selftest-repro.stdout`, `T49RevControls.c2-selftest-repro.stdout`
   (command: `python3 -B .ufo/evidence/round-49/c{1,2}/measure.py --selftest`).

7. **no-harm-at-base.stdout**: 9 `NOHARM … ok` lines — matches the contract's "9 monitors, all ok".

8. **Deciding gate matches the contract kill rule and the round-48 fixes**: gate 0 presence+ancestry
   (`deciding-run.sh:24-27`), second-invocation refusal (`:29`), start-before/end-after per counter
   (`:42-51`), frozen-path diff check (`:32-34`), no-harm 9-ok-lines requirement, census, coldread
   precheck. The C1 counter's `--fleet` default (`c1/measure.py:582`, dirname of lane) equals the
   harness's explicit `--fleet`, so the deciding run omitting `--fleet` (`deciding-run.sh:47`) is
   equivalent.

9. **Guard docstring mismatch is pre-registered, not new**: the docstring says "exit 1 = the map is
   not admissible" (`tools/staged-id-guard.py:38-39`) while observed exit 1 also covers analysis
   refusal; contract `C2.guard_exit_semantics_observed` already records this "for the lesson, not
   edited". Confirmed; no action.

## Findings

No blocking defects. Minor findings:

- **F1 (low, design gap — C1 control verdicts are not self-asserted).** `c1-controls.py`'s `score()`
  (`:138-149`) prints verdicts but accumulates no rc; the harness exits 0 even if CTL_0 printed
  PASS=true or CTL_K2 PASS=false. `c2-controls.sh` greps its expected verdicts (`:22-24`) but the c1
  harness does not, and `deciding-run.sh` gate 0 (`:24-27`) checks only presence + ancestry of the
  four receipt files, never their content (it does not even require `c1-controls.exit=0`). A
  wrong-verdict or corrupted c1 receipt would pass the gate silently. Mitigation: the receipts are
  committed (`6885adb`) and this review verifies each verdict against the contract. Command:
  `grep -n "rc" .ufo/evidence/round-49/control/c1-controls.py` (no rc accumulation);
  `sed -n '22,27p' .ufo/evidence/round-49/deciding-run.sh`.
- **F2 (low — receipt content integrity is not hash-checked by the gate).** Gate 0 takes the last
  commit touching each receipt (`git log -1 --format=%H "$REV" -- "$f"`, `deciding-run.sh:26`); a
  receipt edited after `6885adb` would still descend from FREEZE and pass. Content correctness rests
  on review (this seat) and public history. Command: `sed -n '24,27p' .ufo/evidence/round-49/deciding-run.sh`.
- **F3 (informational — second-invocation refusal is OUTDIR-state-based).** `deciding-run.sh:29`
  refuses only when `$OUT/$k.start` exists; emptying OUTDIR between attempts would defeat it.
  Receipts-only commit discipline makes any such deletion visible in history. Command:
  `sed -n '29p' .ufo/evidence/round-49/deciding-run.sh`.
- **F4 (informational — CTL_J durable arithmetic).** `durable_covered=60/64` means 4 of 64 sections
  lapse under the record-append probe because the refreshed entries bind volatile record inputs; that
  is the round-36 shape the control mimics, so the number is expected and not a counter defect.
  Command: `tail -1 .ufo/evidence/round-49/control/c1-CTL_J.stdout`.
- **F5 (informational — stub env isolation).** `c2-fixed-gen.py` `main()` runs the guard with plain
  `subprocess.run` without its own TMPDIR (inherits the counter's `env_for(work)`); cosmetic, no
  effect on the control's discrimination. Command:
  `grep -n "subprocess.run" .ufo/evidence/round-49/control/c2-fixed-gen.py`.
- **F6 (informational — witness case reuse).** The 12 confirmations come from 11 distinct cases; two
  mutants are confirmed by cases already used by other mutants. Consistent with the contract's
  "11 hand-made cases confirm all 12 panel mutants"; noted so the count is not misread. Command:
  `cat .ufo/evidence/round-49/control/c2-WITNESS.stdout` (case indices only; mutant names withheld
  per seat bounds).

## Residual risk and verification gaps

- The hidden panel bytes were never read by this seat (per bounds); panel identity rests on the
  counter's PANEL_SHA check (`c2/measure.py:232`) plus `panel_valid=1` in all three c2 receipts.
- The C2 counter was not re-run end-to-end (it needs the hidden panel); CTL_ABSENT/CTL_FIX/WITNESS
  verdicts are verified from receipts + code reading + the stub replay probe.
- Gate 0 content checks (F1/F2) remain convention-level; this review is the current enforcement.
- The deciding run has not happened; all ordering checks here are pre-deciding (`after/` empty; gate 0
  will enforce at run time).

## Tooling record

No tools installed or upgraded (none needed); pacman untouched. Lane untouched except this report and
the four probe-receipt copies in this wave dir; no scratch remains.

## Summary

- All 13 freeze.json digests match on-disk bytes; receipts embed matching counter self-digests; the
  freeze→controls commit diff touches only receipts + wave-1 spec files.
- Timeline holds: freeze commit 17:15:08-03 < controls start 20:15:18Z < ends 20:17:01Z/20:19:43Z <
  controls commit 17:19:55-03; no deciding receipts exist yet and gate 0 enforces ordering at run time.
- C1: CTL_0 fails matching the contract "before" line exactly (reproduced live in scratch); CTL_J
  fails as the round-36 refresh shape (durable 60/64, 81 unverified); CTL_K fails on exactly the two
  bare map line pointers; CTL_K2 passes with total=0 — the positive control isolates the counter's
  documented blind spot.
- C2: CTL_ABSENT fails with generator absent (total=25); CTL_FIX fails with confirmed=6 < 11 and 4
  classes short (stub verified: interface-compliant, subprocess-only, 14 fixtures, replay probe clean);
  WITNESS confirms 12/12 mutants over 11 cases, proving the kill path reachable.
- Panel identity is enforced by the counter's PANEL_SHA check; panel_valid=1 in all c2 receipts.
- Findings: no blocking defects; F1/F2 (low): c1 control verdicts and receipt content are not
  self-asserted/hash-checked by any gate — enforcement is this review; F3-F6 informational.
