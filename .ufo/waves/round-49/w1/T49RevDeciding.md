# T49RevDeciding — line-by-line review of deciding-run.sh and no-harm.sh (round 49)

Scope: `.ufo/evidence/round-49/deciding-run.sh` (53 lines) and `.ufo/evidence/round-49/no-harm.sh` (27 lines),
read-only, against the frozen bytes (working-tree sha256 of all 13 frozen files + coldread-precheck match
`freeze.json`'s digests; command: `sha256sum <the 14 files>`). No counter was run against the lane; one probe
ran the frozen C2 counter in a scratch shared clone (reported as observed, not a verdict). No tools installed.
Scratch `/fast/scratch/hyaku/tameshi-r49/T49RevDeciding` deleted before this report.

## Verified clean (checked, no defect)

1. **Gate-0 receipt set matches what the harnesses produce.** c1-controls.py writes per-control files into OUT
   and prints `CTL_x exit=…` summary lines (c1-controls.py:139-143); c2-controls.sh writes per-control files and
   prints `C2_CONTROLS ok=` (c2-controls.sh:24-38). All four gate-0 paths exist at tip, last committed by
   6885adb (a child of freeze 14d03ea) — `git log -1 --format='%h %cI %s' HEAD -- .ufo/evidence/round-49/control/c1-controls.stdout` (and the other three).
2. **Receipt order.** `c2.start` precedes the c2 invocation; `c2.exit` then `c2.end` follow; same for c1
   (deciding-run.sh:43-48). Every gate-0 refusal (:14-29) precedes the first write (:30/:33), so a refused run
   leaves no receipts and re-invocation is clean.
3. **Exit-code paths.** 0 all-ok; 1 accumulated failures; 2 usage/`cd`/rev-parse (:14,:19,:20,:21); 3 refusals
   (outdir-missing :22, control-receipt-missing :25, control-receipt-not-after-freeze :27, second-invocation :29).
   Complete except F8's missing-argument path.
4. **Scratch.** HYAKU_SCRATCH-based, never /tmp in either script; `TMPDIR` exported for children (:30);
   c2-controls.sh (c2-controls.sh:20) and coldread-precheck.sh (coldread-precheck.sh:12, with trap) clean their
   own scratch; the counters honor TMPDIR (c1/measure.py:448) or use work/tmp (c2/measure.py:86-91).
5. **Panel mechanics.** The panel is read from REV (:42) and the counter verifies its sha256 against the frozen
   pin (c2/measure.py:47 `PANEL_SHA` = freeze.json `panel_sha256` = d6dd2cf3…); the guard is read from REV blobs
   and sha-checked (c2/measure.py:252-256). Commit-reveal intact; the counter refuses other bytes (probe below).
6. **Counter invocations match the counters' contracts.** c2 gets `--lane/--rev/--work/--panel` with no
   `--generator-path` → default `tools/pbt-staged-id.py` (c2/measure.py:46); c1 omits `--fleet`, whose default is
   `dirname(lane)` (c1/measure.py:582) = the fleet root, matching the value the controls harness passes explicitly.
7. **Nine monitors = round-48's eight + tools-scope, coldread turned into a floor.** Round-48's eight:
   commandD, coldread, r45-freshness, r45-coverage, S160-count, registry-floor, r46-coverage, r47-coverage
   (round-48/no-harm.sh:10-25). Round-49 keeps all eight (two deltas in F11) and adds tools-scope (:26-27).
   All nine read ok at base (control/no-harm-at-base.stdout); base values independently recomputed:
   `git show 8ca67421…:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'` → 128; same with `| S160 ` → 1;
   `git show 8ca67421…:tools/mutate-and-run.sh | python3 -c '<commandD one-liner>'` → `recorded_cases=9 depth_score=9`.
   r45-freshness is immune to this round's SOURCES additions (population capped `id <= S160`,
   round-45/freshness/measure.py docstring).
8. **tools-scope pattern.** `printf 'A\ttools/pbt-staged-id.py\n' | tr '\t\n' ': '` → `A:tools/pbt-staged-id.py `
   matches the case arm at no-harm.sh:27; a second tools entry (`M\ttools/staged-id-guard.py`) yields RED.
9. **No frozen drift so far.** `git diff --name-only 14d03ea4…..HEAD` lists only control receipts, wave-1
   helpers/specs, SCORECARD.md, SKILL.md (the claim's legitimate surfaces); no FROZEN path appears.

## Defects and fixes

### F1 (high) — the deciding run executes working-tree code and never verifies the checkout against REV
deciding-run.sh:44 and :47 run `python3 "$E/c2/measure.py"` / `python3 "$E/c1/measure.py"` — relative paths
resolved after `cd "$LANE"` (:19), i.e. the working-tree copies, not REV blobs; same for coldread-precheck (:38)
and for the round-21/45/46/47 measures inside no-harm.sh (:12,:14,:16,:22,:24). The frozen check (:33) compares
only *committed* bytes FREEZE→REV, so uncommitted edits to any executed file change deciding behavior while
`FROZEN_UNCHANGED=1` prints. Partial mitigations exist: no-harm.sh itself is extracted from REV (:34);
c1/measure.py pins the round-21+round-18 monitor bytes in the live lane (c1/measure.py:369-371); c2/measure.py
reads guard and generator from REV blobs (c2/measure.py:252-256). Residual exposure: c1/measure.py and
c2/measure.py themselves, coldread-precheck.sh, and the four r45/46/47 measures.
**Fix:** extend the existing extraction pattern to everything executed — `git show "$REV:<path>" > "$SCR/<name>"`
for both counters and coldread-precheck, and have no-harm extract the four measures it runs; or, cheaper, gate 0
asserts `git rev-parse HEAD` = REV and `git status --porcelain --untracked-files=no` empty.

### F2 (medium-high) — panel-reveal failure is not a refusal; it burns the single deciding invocation on a doomed run
:42 `git show "$REV:$E/c2/panel.json" > "$SCR/panel.json" || { echo "PANEL_NOT_REVEALED"; rc=1; }` sets rc=1 and
continues; the c2 counter then runs against an empty panel file and fails in setup. Probe (scratch clone,
observed): `python3 .ufo/evidence/round-49/c2/measure.py --lane <clone> --rev HEAD --work $S/w --panel <empty>` →
stderr `C2_R49: setup=panel sha256 mismatch`, exit 2. Start/exit receipts are written (:43-45), so the
second-invocation refusal (:29) blocks any re-run — the round is spent on a run that could never pass. The
message also lacks the `DECIDING_REFUSED` prefix every other refusal uses.
**Fix:** make it gate 0: `git cat-file -e "$REV:$E/c2/panel.json" 2>/dev/null || { echo "DECIDING_REFUSED panel-not-revealed"; exit 3; }` before any receipt is written (the extraction at :42 stays, now infallible).

### F3 (medium) — pre-counter verification failures set rc=1 and continue, spending the kill-ruled invocation on a run already known to have failed
Frozen drift (:33), no-harm RED/count (:36-37), coldread-precheck (:39), census (:41) only accumulate rc; the
counters still run (:43-48) and write start receipts, so a fixable failure cannot be repaired and re-run (a
second invocation is a miss by the kill rule). Round-48's burn (attempt-3 salvage, commits 8f2922b/c6295cb) is
the precedent.
**Fix:** promote these to gate-0 refusals (exit 3, nothing written, re-invocation allowed) — at minimum frozen
drift and no-harm RED, which are preconditions for a meaningful run. Tradeoff: the failed-attempt receipts are
lost (the refusal message names the cause); the L1 decides.

### F4 (medium) — gate 0's "descends from FREEZE" admits the freeze commit itself, and REV's descent from FREEZE is never asserted
:27 `git merge-base --is-ancestor "$FREEZE" "$c"` exits 0 when `$c` == `$FREEZE` (demonstrated:
`git merge-base --is-ancestor 14d03ea4… 14d03ea4…; echo $?` → 0). Receipts committed *in* the freeze commit pass
gate 0, but they cannot have been scored at the frozen bytes (the freeze commit did not exist when they were
produced) — the round-48 defect class this gate exists to refuse. Also nothing asserts REV descends from FREEZE;
a REV on a divergent line would still diff-equal on the frozen paths while breaking the
controls-scored-at-freeze → deciding-run-at-REV chain. Observed state is clean (all four receipts last touched
by 6885adb, a child of 14d03ea), so this is laxness, not an active failure.
**Fix:** `[ "$c" != "$FREEZE" ] || { echo "DECIDING_REFUSED control-receipt-at-freeze $f"; exit 3; }` and
`git merge-base --is-ancestor "$FREEZE" "$REV" || { echo "DECIDING_REFUSED rev-not-after-freeze"; exit 3; }`.

### F5 (medium) — gate 0 checks receipt existence and commit order, never content; c1-controls.py's exit receipt is not a verdict
:24-28 only `git cat-file -e` + ancestry; a committed receipt contradicting the contract (controls printing
PASS=true, a truncated run) passes. Asymmetry: c2-controls.sh self-checks its labels and exits rc
(c2-controls.sh:31-38: greps `C2_R49_PASS=false` twice and `witness_confirmed=12`, `exit $rc`), but
c1-controls.py only prints and always exits 0 (c1-controls.py:139-143 `score()` prints; the script ends after
`shutil.rmtree`) — c1-controls.exit is 0 even if every control misbehaves.
**Fix:** gate 0 greps the committed receipts for the frozen expectations — `^CTL_0 exit=1 .*C1_R49_PASS=false`,
`^CTL_J exit=1 .*false`, `^CTL_K exit=1 .*false`, `^CTL_K2 exit=0 .*true`, `^CTL_ABSENT exit=1 .*C2_R49_PASS=false`,
`^CTL_FIX exit=1 .*false`, `witness_confirmed=12`, `^C2_CONTROLS ok=true` — refusing on any miss; optionally give
c1-controls.py the same self-check+rc discipline. Today's receipts carry exactly those labels
(control/c1-controls.stdout, control/c2-controls.stdout), so the check would pass.

### F6 (medium) — the second-invocation refusal is keyed to the OUTDIR filesystem only
:29 `[ -e "$OUT/$k.start" ]`. A re-invocation with a fresh OUTDIR runs the counters again; after the
receipts-only commit, a re-run at the new tip with a different OUTDIR is likewise uncaught — the kill rule's
"second invocation is a miss" is unenforced across OUTDIRs.
**Fix:** also refuse when REV already carries deciding receipts:
`git cat-file -e "$REV:$E/after/c1.start" 2>/dev/null && { echo "DECIDING_REFUSED receipts-already-at-rev"; exit 3; }`
(at the legitimate run `$E/after` is not in git — verified: `git ls-tree --name-only HEAD .ufo/evidence/round-49/after/` prints nothing at tip).

### F7 (medium) — the frozen path list omits code the deciding run depends on
FROZEN (:32) is code and contract only, no receipt dirs ✓, but omits: `.ufo/evidence/round-48/quality/coldread-precheck.sh`
— executed at :38 and digest-pinned in freeze.json (3b07847a…), yet a FREEZE→REV edit would not trip :33; and
`.ufo/evidence/round-45/freshness/measure.py`, `.ufo/evidence/round-45/coverage/measure.py`,
`.ufo/evidence/round-46/coverage/measure.py`, `.ufo/evidence/round-47/coverage/measure.py` — executed by no-harm
(:14,:16,:22,:24) and pinned nowhere (absent from freeze.json too), so committed edits silently change no-harm's
verdicts. The rest is right: round-18/measure.py belongs (round-21's measure imports it,
round-21/coldread/measure.py:16-19; c1/measure.py:31-33 pins both shas); panel.json is correctly absent
(revealed post-freeze); the generator is correctly absent (created this round). Also the list is never validated
for existence — a mistyped path diffs vacuously (all 13 verified present at FREEZE:
`git cat-file -e 14d03ea4…:<path>` per path → OK ×13, so no active typo).
**Fix:** add the five paths to FROZEN plus an existence loop (`git cat-file -e "$FREEZE:$f"` per path); freeze.json's
digest map can only grow by amendment since freeze.json is itself frozen.

### F8 (low) — argument/usage handling
:12-13 has no argument-count check; fewer than 4 args dies on `set -u` with a bash diagnostic and exit status 1,
not the documented 2/3. OUTDIR is documented "existing, EMPTY directory inside LANE" (:4) but :22 checks only
existence: no containment check (receipts could land outside the lane — unciteable per the scratch rule), no
emptiness check (stale files ride into the receipts-only commit; verdicts unaffected since every receipt name is
overwritten). :18: a relative `HYAKU_SCRATCH` resolves SCR inside the lane after `cd "$LANE"` (:19) — scratch
written into the read-only lane.
**Fix:** `[ $# -eq 4 ] || { echo "usage: deciding-run.sh LANE REV FREEZE OUTDIR"; exit 2; }`;
`[ -z "$(ls -A "$OUT")" ]` + `case "$(cd "$OUT" && pwd -P)" in "$LANE"/*) ;; *) refuse;; esac` (or pin OUT to
`$E/after` per the contract's tip rule); `case "$SCR" in /*) ;; *) exit 2;; esac`.

### F9 (low) — scratch hygiene
:30 `mkdir -p "$SCR"` never cleans pre-existing scratch: an aborted earlier attempt (killed before any start
receipt, so re-invocation is allowed) leaves stale `$SCR/c1`, `$SCR/c2`, `panel.json`, `no-harm.sh`; the
counters' `--work` is contractually EMPTY_DIR. c2-controls.sh does it right (`rm -rf "$SCR"; mkdir -p "$SCR"`,
c2-controls.sh:20).
**Fix:** `rm -rf "$SCR"` before mkdir, plus `trap 'rm -rf -- "$SCR"' EXIT` for signal-interrupted runs
(coldread-precheck.sh:12 uses exactly that trap).

### F10 (low) — no-harm.exit is not a verdict
no-harm.sh has no rc accumulation; its last line is an echo, so it always exits 0 — deciding-run.sh:35 records
no-harm.exit=0 even when monitors RED; the verdict lives only in stdout (:36-37). A receipts-only reader of the
.exit files would conclude no-harm passed.
**Fix:** accumulate rc in no-harm.sh and exit it (the c2-controls.sh pattern), keeping the greps as belt-and-braces.

### F11 (low, documentation) — two further deltas vs round-48 that the header does not state
The nine monitors do match round-48's eight + tools-scope with the coldread floor, but:
- the registry floor was raised 124→128 (no-harm.sh:21 vs round-48/no-harm.sh:21 `[ "$R" -ge 124 ] …
  "registry-rows-not-below-124"`). Round-48's header documented its raise ("registry floor raised to 124");
  round-49's header (:3-5) does not mention this one. Verified legitimate: base count is exactly 128 and the
  monitor reads `registry-rows-not-below-128 128 ok` at base (control/no-harm-at-base.stdout:7).
  **Fix:** one header line noting the raise.
- the coldread monitor's observed field changed from `box3_full_page` (round-48/no-harm.sh:12-13, equality
  `score=6 box3_full_page=False`) to `credited` (sections_covered). Necessary, not cosmetic:
  `box3_full_page = sections_covered == sections_total` (round-18/measure.py:655), which flips True exactly at
  C1's target (64/64) — keeping the round-48 equality would RED a successful round. The floor (score>=6,
  credited>=57, no-harm.sh:13) matches the base values (no-harm-at-base.stdout:2: `score=6 credited=57 ok`).
  No fix needed; record for calibration.

## Residual risk and verification gaps
- Neither script was executed end-to-end (the deciding run is the L1's). Gate-0 refusal paths and receipt
  ordering are verified by reading plus targeted probes, not by a live refusing invocation; a fixture-tree
  rehearsal (the round-48 fix standard, "shown able to fail on a fixture tree") would confirm F2/F3's refusal
  promotion.
- F1 assumes an uncommitted-edit threat model; the L1's discipline may make it moot, but the extraction fix is cheap.
- Fixes to the two frozen scripts require a freeze amendment (both are digest-pinned in freeze.json and listed in
  FROZEN); contract.json's `amendments` array is empty and available for that.

## Summary
- Reviewed deciding-run.sh (53 ln) and no-harm.sh (27 ln) at frozen bytes; all 13 frozen digests match freeze.json; no frozen path drifted since 14d03ea.
- Gate-0 receipt set, receipt order (start→run→exit→end), and the 0/1/2/3 exit-code map are correct; refusals write nothing, so re-invocation after a refusal stays clean.
- Nine monitors verified = round-48's eight + tools-scope with the coldread floor; all nine ok at base with base values recomputed (registry 128, S160 1, recorded_cases 9).
- High: the run executes working-tree counter/precheck/measure code without checkout verification (F1) — extract from REV or assert clean tree at REV.
- The panel-reveal failure burns the single invocation on a doomed run instead of refusing (F2, probe-confirmed `setup=panel sha256 mismatch`); frozen-drift/no-harm/coldread/census failures likewise spend the invocation (F3).
- Gate 0 admits receipts committed in the freeze commit itself and never asserts REV descends from FREEZE (F4); it never checks receipt content, and c1-controls.py always exits 0 (F5).
- Second-invocation refusal is OUTDIR-keyed only (F6); FROZEN omits coldread-precheck.sh and the r45/46/47 measures no-harm executes (F7); minor usage/scratch/exit-receipt findings (F8-F10) and two undocumented-but-verified monitor deltas (F11).
- Fixes to the frozen scripts need a freeze amendment; contract.json `amendments` is empty and available.
