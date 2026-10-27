# Round 53 wave 1 — frozen-counter mutation probe

**Verdict summary:** 6 valid C2 counter mutants were exercised against a green pristine fleet-mirror fixture: 5 killed, 1 survived. Three C1 mutants were attempted but are **inconclusive** because the frozen C1 counter's pristine fixture baseline is already red. The real-lane C2 baseline is also red at C* and HEAD due to the CR47 check.

## Fixture and bounded detector

Frozen counters were read from `e62d99711a0dd5d92b83acb96dd53ff22b31cb75` and invoked as `python3 measure.py --lane FIXTURE --rev REV --work RUN --explain`. C1 fixture inputs include the frozen 30-heading list, C* SKILL.md and round-18 sectionizer, matching reader hashes, synthetic rekey ledger/traces, and a green precheck stub. The precheck stub is only a fixture stand-in; it does not validate the real cold-read monitor.

For C2, the fixture uses C* tool and documentation bytes, except for a disclosed fixture-only strict-TMPDIR enabler in `registry-check.py`'s selftest scratch setup. This is necessary to create a green baseline for mutation tests: the actual C* tool does not satisfy the frozen counter's CR47 predicate. Each attack commit is an independent child of the good fixture revision `150f23b1e241` (full fixture commit IDs are in the scratch run record; scratch was removed before handoff).

### Pristine/restored controls

- C2 pristine fixture: `C2_R53: rev=150f23b1e241 tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=1 docs=ok total=0 C2_R53_PASS=true` (exit 0).
- C2 restored-byte rerun printed the same verdict and exit 0.
- C1 pristine and restored fixture both printed `C1_R53: rev=150f23b1e241 credited=64 lost=0 rekeyed=0/30 readers=0/30 total=31 C1_R53_PASS=false` (exit 1). This is a baseline failure, not a mutant kill.

## Mutants

`KILLED` means the green pristine counter detects the targeted bad fixture (mutated counter incorrectly changes its verdict to PASS). `SURVIVED` means the same detector behavior remains correct after the mutation. Hashes below are SHA-256 of each isolated mutated counter file; original source hashes are in Restoration.

| Mutant | Single edit and attack | Expected | Observed counter output | Verdict; mutant SHA-256 |
|---|---|---|---|---|
| M1 (C1) | Rekey completeness gate only fires when heading count is not 30; attack omits one ledger entry (A1). | On green C1 baseline, attack should go FAIL→PASS incorrectly. | Pristine F1 and A1 both exit 1: `rekey-dir-count=0`, `readers=0/30`, `C1_R53_PASS=false`. | **INCONCLUSIVE** (baseline failed); `d2a740f1d49f099438e3bd5b6cedc8d814049bf0dc80af3bf145c168b7989034` |
| M2 (C1) | Reader `section_sha256` equality changed to `equality or True`; attack corrupts one reader hash (A2). | On green C1 baseline, attack should go FAIL→PASS incorrectly. | Pristine F1 and A2 both exit 1: `rekey-dir-count=0`, `readers=0/30`, `C1_R53_PASS=false`. | **INCONCLUSIVE** (baseline failed); `4d2f24105f91be2861cffa074dddb1ed24aa6abf4d94985431b8864f7a3958e6` |
| M3 (C1) | Ancestor condition changed to `False and anc.returncode != 0`; attack rev has the F1 tree but a parent that excludes C0 (A3). | On green C1 baseline, attack should go FAIL→PASS incorrectly. | Pristine F1 and A3 both exit 1: `rekey-dir-count=0`, `readers=0/30`, `C1_R53_PASS=false`. | **INCONCLUSIVE** (baseline failed); `c79a7eb2f97111604ad3b66791e6c4ae7d153f92039335df9f84be5a49e12c94` |
| M4 (C2) | Disable CR47 `REGISTRY_CHECK` stdout-verdict check; A4 prints a verdict line despite unusable scratch. | F1 remains PASS; attack should be rejected by pristine and incorrectly PASS with mutant. | F1 mutant exit 0 / PASS. A4 pristine exit 1 / `PROBLEM cr47-verdict-line`; A4 mutant exit 0 / `cr47=rc=1 docs=ok total=0 C2_R53_PASS=true`. | **KILLED**; `2741db80bee268c6180c3a61cbd5b816e8df488d1dcdd051734276dc49560127` |
| M5a (C2) | Weaken live `git grep` regex to exact `dir="/tmp"`; A5 plants `dir = "/tmp/attack-probe"`. | F1 remains PASS; attack should be rejected by pristine and incorrectly PASS with mutant. | A5 pristine exit 1 / `tmp_hits=1`; A5 mutant exit 0 / `tmp_hits=0 C2_R53_PASS=true`. | **KILLED**; `1917ba30f203776f61db77c09758abd86f0854fff623ec696a2acdac12e34493` |
| M5b (C2) | Mutate module-level `TMP_RE` to a never-matching regex; A5 plants the same spaced hardcode. | If `TMP_RE` is live, mutant would pass the bad fixture; if dead, behavior remains correctly FAIL. | A5 pristine and mutant both exit 1 / `tmp_hits=1 C2_R53_PASS=false`; F1 both exit 0 / PASS. | **SURVIVED** — `TMP_RE` is dead; enforcement uses the separate inline `git grep` regex. `716ecf11f863aebf314a536e1f402ab3a01ac679f7b0c732fc6b027b37c93fc4` |
| M6 (C2) | Empty `FLEET_DOC_PATTERNS` (move the prior pattern literal to an unused `_dead` list); A7 adds `/tmp/tameshi-f5.json` to SKILL.md. | F1 remains PASS; attack should be rejected by pristine and incorrectly PASS with mutant. | A7 pristine exit 1 / `docs=stale-patterns=1`; A7 mutant exit 0 / `docs=ok total=0 C2_R53_PASS=true`. | **KILLED**; `48f618bede1b4adaf343ae9e25a8a96f820f6fdcde12a10fefa4336bba671277` |
| M8 (C2) | Weaken CR47 message regex to any `scratch` mention; A6 has a non-zero selftest with `scratch root unusable for clone` (not the required creation error). | F1 remains PASS; attack should be rejected by pristine and incorrectly PASS with mutant. | A6 pristine exit 1 / `PROBLEM cr47-no-scratch-message`; A6 mutant exit 0 / `cr47=rc=1 docs=ok total=0 C2_R53_PASS=true`. | **KILLED**; `247680b3be4c8b4877c10beadf2dd5ab036da4c90caf67ee0e05d129a8957a80` |
| M9 (C2) | Disable selftest non-zero-exit check; A8 makes `env-diff.py --selftest` exit 1. | F1 remains PASS; attack should be rejected by pristine and incorrectly PASS with mutant. | A8 pristine exit 1 / `envdiff_selftest=[rc=1 fixture selftest failure] total=1 C2_R53_PASS=false`; A8 mutant exit 0 / same rc=1 but `total=0 C2_R53_PASS=true`. | **KILLED**; `095847d6630ca1b1dda108ae50c869e0e82b438d204d3d058f51f11d2a9fb30f` |

All six C2 mutants M4, M5a, M5b, M6, M8, M9 were also run on good F1; each returned PASS, as expected. Attack fixtures were checked with pristine counter bytes before comparing mutant behavior.

## Findings affecting interpretation

1. **C1 detector baseline defect:** the frozen source calls `git ls-tree --name-only REV .ufo/evidence/round-21/coldread` and matches each output against `rekey-r53-<12hex>`. On both the synthetic fixture and the real C* tree, this command returns the path entry `.ufo/evidence/round-21/coldread`, not its child names. Consequently C1 reports `rekey-dir-count=0`, leaves `c0` unset, and reports all readers missing. This makes M1–M3 inconclusive under the required baseline rule; I did not use a shim to alter git behavior.
2. **C2 CR47 counter/tool mismatch at real C* and HEAD:** the frozen counter on real C* printed `C2_R53: rev=a41195dfc13a tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=0 docs=ok total=2 C2_R53_PASS=false`, with `PROBLEM cr47-zero-exit` and `PROBLEM cr47-no-scratch-message`. At HEAD `ace79e3df612`, it likewise printed `cr47=rc=0 ... total=2 C2_R53_PASS=false`. C*..HEAD had no tool diff and no intervening registry-check edit. Independently, `TMPDIR=<scratch>/definitely-missing python3 -c 'import tempfile; print(tempfile.gettempdir())'` returned `/tmp`. Thus the real C* tool silently falls back to `/tmp` rather than producing the failure the frozen counter requires. The strict-TMPDIR fixture enabler above is solely to isolate and mutation-test the counter's CR47 checks; it is not evidence that real C* satisfies the predicate.

## Restoration evidence

Frozen source SHA-256 before/after the probe (git object bytes and retained pristine scratch copies agree):

- C1 `067c1685eeda8177a47fec5806a8367ebde4b99737394dd4a68068fe5d949955`
- C2 `1942cd8f9850727066439d317acaf5eb0a8e44458b0355ea4dceaf90e8c82c27`

Mutants were separate scratch files; neither frozen source copy was overwritten. The final restored C2 run exactly reproduced the initial green F1 verdict; restored C1 reproduced the initial baseline-red verdict. Scratch fixture and scripts were removed before handoff. No tools were installed or updated.
