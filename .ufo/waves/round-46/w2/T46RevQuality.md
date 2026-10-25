seat: T46RevQuality
item: review QUALITY criteria 88-90 (corpus/QUALITY.md:1287-1351) and re-run their falsifiers (falsifiers.sh at a6892b196f923efbed242ce9ea599a3f745b2138), gate selftests, lesson cites, overlap vs criteria 66-69/83-87, and vacuity demos.

Scratch: /tmp/tameshi-r46-T46RevQuality/ (falsifiers.out, f88-demo.sh, f88-only.sh, f89-demo.sh, f89-only.sh, f90-demo.sh). Lane writes: this file only. No git/jj mutations; all counter runs were read-only `--selftest` or `--rev` runs printed to scratch, never verdicts.

# What was attacked

`corpus/QUALITY.md` `## Criteria appended — round 46` (lines 1287-1351): criterion 88 (no_harm monitors green at base, gate `quality/no-harm-gate.py`), 89 (neutral mutants beside declared survivors, `hardening/mutate.py` `neutral_killed=`), 90 (seat-name uniqueness across concurrent lanes, `quality/seat-name-check.py`), their shared falsifier `quality/falsifiers.sh`, and the committed receipt `quality/c88-90-falsifiers.stdout`.

# Falsifier rerun (as assigned, observed output)

`bash .ufo/evidence/round-46/quality/falsifiers.sh a6892b196f923efbed242ce9ea599a3f745b2138` (cwd /tmp, 41 s, exit 0), full output in scratch `falsifiers.out`:

- block 88: `WHY r44-record-agreement exit 1; missing token 'C2_R44_PASS=true'` / `NO_HARM_GATE_PASS=false` for the synthetic r44-only monitors file; `monitors=6 ok=6 red=0` / `NO_HARM_GATE_PASS=true` for `no-harm.sh` at base; `c88 red_monitor_exit=1 real_list_exit=0` → `CRITERION-88-FALSIFIER-OK`.
- block 89: `CTL_E_selftest_pins_own_bytes rc=1 … killed=21 survived=4 neutral_killed=6 pristine=1 equivalence=0 C2_R46_PASS=false`; hardened run `killed=25 survived=0 inapplicable=0 neutral_killed=0 pristine=1 equivalence=1 rev=a6892b1… C2_R46_PASS=true` → `CRITERION-89-FALSIFIER-OK`.
- block 90: two `COLLISION MutC1Counter` lines (kaidoku round-28/a2, round-29/w1 registries — both replayed under `--hours 100000`), `SEAT_NAME_CHECK seats=37 collisions=0` for the T46-prefixed spec → `c90 shared_names_exit=1 unique_names_exit=0` → `CRITERION-90-FALSIFIER-OK`.

`diff falsifiers.out .ufo/evidence/round-46/quality/c88-90-falsifiers.stdout`: identical except my trailing `exit=0` line — the committed receipt is byte-reproduced.

# Gate selftests (as assigned)

- `python3 quality/no-harm-gate.py --selftest` → 20 lines `SELFTEST <case> rc=<n> want=<n> PASS`, `SELFTEST: 20/20 passed`, `VERDICT: PASS`, exit 0 (cwd /tmp).
- `python3 quality/seat-name-check.py --selftest` → `PASS shared name found` / `PASS own lane ignored` / `PASS unique names clean` / `PASS old registry ignored by the window`, `SEAT_NAME_SELFTEST: cases=4 failed=0`, exit 0.

# Lesson citations — does each cited path show the failure the criterion prevents?

- 88 → `corpus/lessons/round-45-verifier-spotcheck.md:85`: routed defect 1 is exactly the cited failure — `after/c-r44-at-content.stdout: m11=1 m12=1 total=2 C2_R44_PASS=false`, "Fix the counter … before it is named in another contract's `no_harm`". VERIFIED. `corpus/lessons/round-46.md:115` (Mistakes row 1) repeats it and names criterion 88 + the gate; `before/no-harm-at-base.stdout` is the green-at-base receipt the criterion requires. The criterion's "Measured" line (`the round-44 counter at base 683eedde prints C2_R44_PASS=false`) is independently demonstrated by falsifier block 88's `exit 1; missing token 'C2_R44_PASS=true'`.
- 89 → `control/controls-at-freeze.stdout:5` `CTL_E_selftest_pins_own_bytes rc=1 … killed=21 … neutral_killed=6 … C2_R46_PASS=false` — matches the criterion text verbatim (21/25 + all 6 neutral). `w1/RevManifest.md` exists and explicitly verifies all 6 neutrals are behaviour-preserving (line 8: "all 25 mutants survived, all 6 neutrals survived, 0 inapplicable" on orig + probe fixtures under `neutral/`). VERIFIED.
- 90 → `corpus/lessons/round-45.md:164`: dead-seat row names wave-2 `ScribeScorecard` whose results entry carried mori round-47 output, no tameshi report exists. `.ufo/waves/round-46/w1-results.json` `MutC1Counter` output carries `report: .ufo/waves/round-55/w1/MutC1Counter.md` (kake lane) and `ScribeQuality` carries `.ufo/waves/round-45/w2/ScribeQuality.md` — the criterion's stated paths match byte-for-byte. `corpus/lessons/round-46.md:116` Mistakes row repeats it. VERIFIED.

# Able-to-fail demonstrations (one-input changes in scratch copies; all three print -VACUOUS)

- 88 — `/tmp/…/f88-only.sh`: block 88 with the bad-side `--monitors-file "$T/r44.json"` replaced by `"$E/no-harm.sh"`. Observed: `red_monitor_exit=0 real_list_exit=0` → `CRITERION-88-FALSIFIER-VACUOUS`. The refusal half is load-bearing (112.9 s).
- 89 — `/tmp/…/f89-only.sh`: `mutate.py --rev "$REV"` → `--rev "$BASE"`. Observed: `C2_R46: refused: manifest absent at 683eedde…` then `CRITERION-89-FALSIFIER-VACUOUS` (9.8 s). The hardened-revision pin is load-bearing; a rev without the manifest is refused by the counter itself (exit 2).
- 90 — `/tmp/…/f90-demo.sh`: `--hours 100000` → `--hours 0.00001` on the bad side. Observed: `shared_names_exit=0` → `CRITERION-90-FALSIFIER-VACUOUS`. The scan window is load-bearing: with a 36 ms window every historical registry is excluded and no collision is found.

Additionally (not a demo, a live check): `seat-name-check.py spec-w1.json` at the default `--hours 3` prints 6 `COLLISION` lines against kake round-55/w1+round-56/w1, mori round-47/w1+round-48/w1, exit 1 — the gate would have refused the wave-1 spec as dispatched, in its default window, had it existed then (registries written 2026-10-25 16:03-19:13 vs check run 19:23).

# Overlap / contradiction check (criteria 66-69, 82-87)

Read `corpus/QUALITY.md:752-798` (66-70) and `:1023-1351` (82-90). No contradiction found:

- 67 (`--regression` requires `--workdir` under the seat's scratch; kill only own processes): different axis (resource containment vs artifact correctness). No interaction with 88-90.
- 68 (re-dispatch after dead seats requires a committed task-text comparison): checks for duplicated *items* in the same lane's re-dispatch; 90 checks for colliding *seat names* across concurrent lanes. Related (both touch wave dispatch) but disjoint rules; no conflict.
- 66 (dispatch provenance — a seat can't be a "non-author" of its own lane): orthogonal to 90 (90 does not assert independence, just unique keys). No conflict.
- 69 (binding conditions frozen as executable code before data dispatch): 88 is compatible — the gate IS frozen executable code run before the freeze; 88 adds a verdict requirement on monitors at base, 69 adds a timing requirement on the gate itself.
- 86 (receipts bind measured rev): 88's receipt (`before/no-harm-at-base.stdout` committed with the freeze) measures BASE, not the freeze commit — consistent with 86, no self-measurement.
- 83 (survivors classified): 89's `survived`/`inapplicable`/`neutral_killed` accounting doesn't relabel anything; neutrals are a manifest `kind`, not a survivor verdict. No conflict.
- 82 (a kill is a completed run with a failed check, a crash is not a kill): `mutate.py` `judge()` counts any non-pass selftest — including a syntax-error crash — as `killed`. In tension with 82's letter, though consistent for this manifest: RevManifest verified all 31 mutated copies ast.parse+compile (crash-free), so the shortcut cannot have produced a fake kill this round. INFO.
- 84, 87: unrelated patterns (registry grep pattern; measured quote lengths). 89's unmeasured claim "a digest would kill 25 of 25" is deductive, not measured — every mutant is an old→new byte replacement so a digest pin must kill all; CTL_E (byte-LENGTH pin) is the measured case at 21/25. INFO, not a defect.

# Findings

- LOW — criterion 88 / `no-harm-gate.py`: shell-mode `--monitors-file` skips the contract-phrase check entirely (`gate()` line 294 returns before `contract_phrase` handling; falsifier output confirms `contract_phrases` absent from the shell-mode tally line, present as `contract_phrases=0/0` in JSON mode). The `contract-phrase-drift` selftest (PASS) exercises only the default mapping. Consequence: a contract that drops e.g. the `fresh=71` phrase while `no-harm.sh` still runs and prints `ok` passes the gate in the mode falsifier block 88 actually uses. The criterion text does not promise phrase parity, so the tool over-delivers in default mode and under-delivers in shell mode — honest, but the drift protection is mode-dependent and the drift case is the incident class criterion 88 exists to catch. Fix candidate: name-keyed phrase check in shell mode, or run the default mapping's phrase check regardless of mode. Severity LOW (the exploit needs a contract edit pre-freeze; the monitors still ran green).
- INFO — criterion 89 / `mutate.py:79`: `judge` counts `timeout`, `fail`-by-crash and `fail`-by-check identically as `killed`; a mutant that renders the counter uncompilable would be scored killed (criterion-82-adjacent sloppiness). Not reachable with the frozen manifest (RevManifest: all 31 copies parse+compile, `inapplicable=0`, killed=25 on the hardened run).
- INFO — falsifier block 90 requires `--hours 100000` to reproduce the incident: the colliding registries span 2026-10-20 to 2026-10-25 while the gate's real-time window is 3 h. Correct for replay; I verified the 3 h default also fires on the still-young kake/mori registries today. Residual: a pre-dispatch check cannot see a sibling lane's wave that starts inside the same window AFTER the check ran (registry is written at dispatch) — TOCTOU, mitigated by the T46-prefix fix itself, which makes names structurally unique rather than time-uniquely checked.
- INFO — `seat-name-check.py` LANE is derived from the script's own path (`__file__` → 4 levels up → basename); a copy of the script outside `*/.ufo/evidence/round-46/quality/` silently checks the wrong lane. FLEET is hard-coded `/home/vgpnk/Projects/shokunin` (overridable). Acceptable for a lane-resident tool.
- INFO — `members()` stringifies `m.get('name')` for dict members, so a registry entry without a `name` key contributes the literal `'None'`; harmless (no lane will name a seat `None`).
- Wave-2 spec verified compliant with the criterion's fix: `spec-w2.json` has 35 seats, ALL names start `T46` (`non-T46: []`); a fleet scan for other lanes' `T46*` members found none, so the T46-unique good-side of block 90 is not vacuous by luck.
- Receipt verified: `quality/c88-90-falsifiers.stdout` is byte-identical to my fresh run modulo my trailing `exit=0`. `falsifiers.sh` sha256 `543b4ce4abf50f7b…`, committed at `e630ae7` (records 2) — before the deciding revision `6f2168e`; the script is content of the round it gates, consistent with criterion 69's freeze-before-data rule.
- Unrun-by-design: I did not re-run `mutate.py` on mutants individually or the round-44 counter directly; block 88's observed `exit 1; missing token` line is the gate's own report.

# Verdicts

- Criterion 88: ADOPT-WITH-FIXES — rule is correct, lesson is the exact incident class, gate selftest 20/20, falsifier fails when the bad side is made green and refuses the real failure case; the LOW shell-mode phrase-gap should be closed or the criterion text should scope the drift claim to the default mapping.
- Criterion 89: ADOPT — neutral mutants are the cheapest-cheat discriminator (CTL_E measured 6/6 neutral kills), the driver enforces `neutral_killed == 0` as a pass conjunct, manifest carries exactly 6 neutrals + 25 declared as claimed, hardened run shows `neutral_killed=0 killed=25`. The digest "25 of 25" remark is deductive but sound.
- Criterion 90: ADOPT — gate fires on the real collision in its default window, selftest 4/4, the T46 fix is verified in spec-w2 and collision-free fleet-wide; falsifier proves the window is load-bearing.

# Bounds / tools

Read-only on the lane except this report; scratch under /tmp/tameshi-r46-T46RevQuality. No installs; no pacman. `seat:`/`item:` lines above; report path `.ufo/waves/round-46/w2/T46RevQuality.md`.
