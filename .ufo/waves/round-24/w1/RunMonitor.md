# RunMonitor — round-24 W1 coldread measure at c8c5b88

## Verdict

PASS, no defect found. The assigned coldread measure ran clean (exit 0), reproduced byte-identically across a repeat run and a fresh no-hardlinks clone, and every headline metric was independently recomputed from the revision's blobs and matches the tool. One calibration observation (not a defect of this item): the round-21 coldread ruler is **flat across the wave** — base `6a1821a8897e` and delivered `c8c5b88c8e96` both measure 62/62 sections, restraint 8, depth 8, strict — because both revisions are fully credited under their respective committed ledgers. This ruler measures corpus cold-read credit, not the round-24 command-binding surface. No numeric-uplift claim is made or derivable from this ruler.

## Run (exact)

- argv: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c8c5b88c8e961a929cdc351b95a7074c76958909`
- cwd: `/tmp/RunMonitor-r24` (private clone, `git checkout --detach c8c5b88c8e961a929cdc351b95a7074c76958909`, HEAD verified)
- exit: `0` (wall ≈ 10.2 s)

## Requested metrics (decisive output lines of the assigned run)

```json
"calibration_restraint_score": 8,
"depth_score": 8,
"overrides_used": false,
"trace_gate": "strict",
"sections_covered": 62,
"sections_total": 62,
"ledger_source": "rev",
"revision": "c8c5b88c8e961a929cdc351b95a7074c76958909",
"recorded_cases": 8,
"ledger_committed": true
```

(`coldread.box3_full_page: true`, `coldread.inputs_overlay_merged: 0`, `coldread.missing: []`, `coldread.reasons: {"credited": 62}`, `sources.rows: 83`, `ledger_guardrail.lists_agree: true`.)

## Falsification — what I attacked and what I saw

1. **Determinism.** Re-ran the exact argv; full JSON output identical (`r1 == r2: True`).
2. **Revision addressing.** Same argv with `--repo /tmp/RunMonitor-r24` (fresh clone, detached at the same rev): full JSON identical to the main-repo run. The script reads all measured blobs via `git cat-file`/`git show` at REV only (round-18 docstring + source); the run left no new paths in the main repo (`git status --porcelain` shows only pre-existing/sibling wave artifacts, below).
3. **Independent metric recomputation from `git show REV:` blobs** — all match:
   - `recorded_cases`: regex `^#   ((?:js|bash)-\S+)\s+\S+\s+\d+/\d+` over `tools/mutate-and-run.sh` → 8, legs exactly the tool's `ledger_legs` (js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, bash-checklist-run, js-claims-check, js-round-gate, js-sources-check). `depth_score = min(10, 8) = 8` ✓
   - SHONEN first four boxes = `~,~,~,~`; box-3 block contains `.ufo/evidence/round-21/coldread/ledger.json` → restraint `= 2·3 + 2·1 = 8` ✓ (box3_full_page=true per tool)
   - SKILL.md section count (preamble + `#`/`##`/`###` outside ``` fences) → 61 headings → 62 sections = `sections_total` ✓
   - `corpus/SOURCES.md` rows `^\|\s*S[0-9]{3,}\s*\|` → 83 = `sources.rows` ✓
   - `.ufo/evidence/round-21/coldread/ledger.json` blob exists at REV; `ledger_present`/`ledger_committed` true ✓
4. **Non-vacuity / calibration across the wave.** Same command at base rev `6a1821a8897e`: exit 0, sections 62/62, restraint 8, depth 8, strict — identical scores. Base→rev diff: SKILL.md +18 (adds no heading — 61 headings at base too → 62 sections), corpus/SOURCES.md +9, `.ufo/evidence/round-21/coldread/ledger.json` +727 (source-refresh re-anchor entries), SHONEN.md and tools/mutate-and-run.sh byte-identical. Both states are fully credited under their own ledgers, so this ruler does not discriminate the round-24 delta. Observation only.
5. **Selector selftest** (`measure.py --selftest`): `SELECTOR_SELFTEST: 12/12 pass`, exit 0 — configures the round-21 ledger default, refuses `--ledger-file`/`--ledger-rev`/`--inputs-overlay` including abbreviations (`SELECTOR_OVERRIDE_FORBIDDEN`, exit 64), and proves the no-historical-ledger-fallback case (0/62, restraint 6), so the ruler is not vacuous by construction.
6. **Executed-algorithm identity.** The selector loads the round-18 implementation from the **live worktree** (`ROOT/.ufo/evidence/round-18/measure.py`), not from REV. Both executed files verified byte-identical to their REV blobs (sha256 prefixes `657f009bdf1cc89a…` selector, `7ca87a7c98196d87…` implementation). Caveat for future runs: a drifted worktree would change the algorithm while REV stays fixed.

## Smallest safe correction

None required — no counterexample found.

## Environment notes

- No tools installed or updated (nothing needed; pacman transactions are paused host-wide and were not touched).
- Writes confined to `/tmp/RunMonitor-r24` and this report file. Main-repo untracked paths `.ufo/evidence/round-24/after.json`, `.ufo/evidence/round-24/noharm-c8c5b88.json`, `.ufo/waves/round-24/` are sibling-wave artifacts, not created by this seat's read-only runs.
- No producer-authentication, promotion, R17-CMD-BIND closure, or score-uplift claims made.
