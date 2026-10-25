seat: T46RevSeparable
item: AXES.md causal separability of C1/C2/C3 — experimental remove-one-claim tests in scratch clones of CONTENT 6f2168e028ce7ff6e82ac92093ac05dd1f147c32, plus counter path-constant audit.

Clause under test: AXES.md:31 "**causally separable** — each verifiable without the others having landed". I did not author any of the artifacts under attack. All runs below are scratch observations in `/tmp/tameshi-r46-T46RevSeparable/` (clone `lane` at CONTENT, clones `exp1`/`exp2`/`exp3` each carrying exactly one removal commit made with throwaway identity `t46revsep@scratch` after `git rev-parse --show-toplevel` verification); the deciding runs remain the L1's. No tools installed; nothing in the lane checkout, fleet repo, sibling lanes, or the read-only package was modified besides this report file.

## Baseline at CONTENT (pristine clone `lane`, rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32)

- `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` (worktree of the CONTENT clone) → `== A rows\n120` … `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0.
- `python3 .ufo/evidence/round-46/coverage/measure.py --lane lane --rev 6f2168e…` → `C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 C3_R46_PASS=true`.
- `python3 .ufo/evidence/round-45/freshness/measure.py --lane lane --rev 6f2168e…` → `C1_R45: … population=73 fresh=71 score=9 C1_R45_PASS=true`.
- `python3 .ufo/evidence/round-46/hardening/mutate.py --lane /tmp/tameshi-r46-T46RevSeparable/lane --rev 6f2168e… --targets hardened` → `C2_R46: self_pin=1 targets=hardened declared=25 killed=25 survived=0 inapplicable=0 neutral_killed=0 pristine=1 equivalence=1 C2_R46_PASS=true` (EQUIVALENCE freshness 1, coverage 1; all 18+13 manifest mutants judged, 6 neutrals survived). NB: the `--lane` had to be absolute — see finding F2.

## Experiment 1 — delete C2 artifacts (exp1 rev dbcca07417810e24058241b32b75d1d684380da6)

Removal: `rm .ufo/evidence/round-46/hardening/freshness-counter.py .ufo/evidence/round-46/hardening/coverage-counter.py` in the clone worktree (the two hardened counters — the artifacts wave 1 produced; driver `mutate.py`, `mutants.json` and the seat helpers are pre-data/frozen material and were left). Committed `exp1: drop C2 hardened counters`.

- `python3 exp1/.ufo/evidence/round-46/coverage/measure.py --lane exp1 --rev dbcca07…` → `C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 C3_R46_PASS=true` — **unchanged**.
- Cheap C1 statement `sources-registry` (argv `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh`, cwd clone): at exp1 worktree → `== A rows\n120`, `SOURCES_CENSUS: CLEAN`, exit 0 — identical to baseline (`rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, the value the standing row states).
- `python3 exp1/.ufo/evidence/round-46/calibration/measure.py --selftest` → `C1_R46_SELFTEST: cases=18 failed=0`, `VERDICT: PASS` (selftest builds toy lanes; repo-independent).
- Static check on all 22 C1 statements (`statements.json` argv/cwd/sha_file dump): none touches `.ufo/evidence/round-46/hardening/` or any `round-46` path; the only `round-46`/`hardening` matches inside the invoked tools (`tools/mutate-and-run.sh`, `tools/evidence-disposition.py`) are comments about the old r6 hardening, not file reads. → no C1 statement touches the deleted artifacts, so all 22 statements would observe the same values.

Result: C1→C2 and C3→C2 directions separable. **Confirmed.**

## Experiment 2 — delete the three entries and rows S258/S259/S260 (exp2 rev 884aa510b31521858c55dd4e808b8f50b68ecc3a)

Removal: `rm corpus/knowledge/r5-undetected-flaky-failures.md r6-flaky-failures-cluster.md r9-false-red-rate.md` and the three `| S258 |`, `| S259 |`, `| S260 |` lines in `corpus/SOURCES.md` (commit `884aa51 exp2: drop C3 entries and rows S258-S260`, 4 files changed, 156 deletions). Snapshots, package copies, README index lines and `corpus/lessons/round-46.md` left in place (the item's removal set is "the three entries/rows").

- `python3 exp2/.ufo/evidence/round-46/hardening/mutate.py --lane /tmp/tameshi-r46-T46RevSeparable/exp2 --rev 884aa51… --targets hardened` → `PRISTINE freshness pass`, `EQUIVALENCE freshness 1`, 15 mutants killed, 3 neutrals survived; `PRISTINE coverage pass`, `EQUIVALENCE coverage 1`, 10 killed, 3 neutrals survived; `C2_R46: self_pin=1 declared=25 killed=25 survived=0 inapplicable=0 neutral_killed=0 pristine=1 equivalence=1 C2_R46_PASS=true` — **byte-for-byte the same field values as the CONTENT baseline**. (Expected: C2 reads only `hardening/*`, the round-45 counter blobs and the pinned data rev `ea25e0224fc81060414b27301c27bd1344669165`, all untouched.)
- Census statement under the removal: `== A rows\n117`, `SOURCES_CENSUS: CLEAN` — the count moved 120 → 117 while the standing row states `rows=120` (finding F1).
- Freshness axis statement under the removal: `C1_R45: self_pin=1 population=73 entries=73 verified=73 … fresh=71 score=9 C1_R45_PASS=true` — unchanged, because `population()` (`round-45/freshness/measure.py:95-97`) caps at `MAX_ID=160`; S258-S260 never entered the denominator.
- Own-direction sanity: `python3 exp2/.ufo/evidence/round-46/coverage/measure.py --lane exp2 --rev 884aa51…` → `self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- C3_R46_PASS=false` — C3's own claim correctly dies on removal of its own artifacts.

Result: C2→C3 separable. C1→C3: the counter still verifies honestly but the `sources-registry` claim's stated value is data-coupled to C3's rows (F1). No C1 statement touches `corpus/knowledge/` or `coverage/` paths other than through the census row count and the freshness population (cap-shielded); `coldread` axis reads no corpus path (grep of `round-21/coldread/measure.py`: no `corpus|SOURCES|knowledge` matches).

## Experiment 3 — revert the SCORECARD round-46 block (exp3 rev 683e75dd95af4b7d834a4689db559447d8106fd2)

Removal: `git show 683eedde…:SCORECARD.md > SCORECARD.md` in the clone (the only SCORECARD change between base and CONTENT is the appended round-46 block; diff confirmed). Committed `exp3: revert SCORECARD to base`.

- `python3 exp3/.ufo/evidence/round-46/hardening/mutate.py --lane /tmp/tameshi-r46-T46RevSeparable/exp3 --rev 683e75d… --targets hardened` → `C2_R46: … killed=25 survived=0 neutral_killed=0 pristine=1 equivalence=1 C2_R46_PASS=true` — **unchanged**.
- `python3 exp3/.ufo/evidence/round-46/coverage/measure.py --lane exp3 --rev 683e75d…` → `C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 C3_R46_PASS=true` — **unchanged**.
- (Own-direction: at this rev C1 would print `append_only=1` (reverted file equals base, still a prefix) but all 22 standing rows absent → `unparsed=22`; the SCORECARD block is C1's own stated surface, not a sibling artifact.)

Result: C2→C1 and C3→C1 separable. **Confirmed.**

## Dependency matrix (artifact reads)

`grep -n 'round-4[56]'` over the three counters: C1's `measure.py` references only `calibration/measure.py` + `calibration/statements.json`; C2's `mutate.py` references only `hardening/mutate.py`, `hardening/mutants.json`, `hardening/{freshness,coverage}-counter.py` plus the manifest's round-45 orig paths and `DATA_REV=ea25e022…` (round-45 inputs, cross-round not cross-claim); C3's `measure.py` references only `coverage/sources/` and `assimilation/package/` plus `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/README.md`. No counter opens another claim's wave-1 artifact.

| claim being verified \ claim removed | C1 artifacts (SCORECARD r46 block) | C2 artifacts (hardened counters) | C3 artifacts (rows+entries) |
|---|---|---|---|
| C1 counter outcome | own surface | same values (exp1) | `sources-registry` stated `rows=120` vs observed `rows=117` → would print total=1 (F1); other 21 statements unaffected |
| C2 counter outcome | PASS=true unchanged (exp3) | own surface | PASS=true unchanged (exp2) |
| C3 counter outcome | PASS=true unchanged (exp3) | PASS=true unchanged (exp1) | own surface |

## Findings

- **F1 — LOW (confirmed data-level coupling, the example the item named).** C1's `sources-registry` standing claim states `rows=120 SOURCES_CENSUS: CLEAN`, i.e. it embeds C3's three appended rows. Measured: baseline `== A rows\n120`; after deleting S258-S260, `== A rows\n117` (still `SOURCES_CENSUS: CLEAN`, exit 0 — the census itself stays honest because used-by paths vanish with their rows). So `C1_R46_PASS=true` at CONTENT is true only because C3's rows exist; remove C3 and the same counter honestly reports a mismatch. The coupling is visible and falsifiable, not hidden inside the counter (the counter reads only SCORECARD+statements); it lives in the re-stated census value. Freshness axis is shielded (`MAX_ID=160`, verified `population=73` at both revs); no other C1 statement reads corpus. Severity LOW: the separability clause concerns independent verifiability and C1 remains verifiable in both worlds — the stated literal just happens to count a sibling's output, and any removal is loudly reported rather than masked.
- **F2 — LOW (counter fragility, invocation-dependent false negative).** `hardening/mutate.py:89-101` `equivalence()` writes each counter to a `tempfile.TemporaryDirectory` and re-executes it with `cwd=d` but forwards `--lane` verbatim. With a **relative** `--lane` (as the contract's `--lane LANE` template invites), `git -C lane …` inside the tempdir fails, the orig counter's stdout lacks `_PASS=true`, and the check early-returns 0 with no diagnostic: measured `--lane lane --rev 6f2168e…` → `EQUIVALENCE freshness 0 / coverage 0`, final `equivalence=0 C2_R46_PASS=false` at the identical pristine CONTENT revision where `--lane /tmp/tameshi-r46-T46RevSeparable/lane` prints `equivalence=1 C2_R46_PASS=true`. No false-pass direction exists (orig must print `_PASS=true` before its lines are compared). `deciding-run.sh` forwards `"$LANE"` verbatim to mutate.py, so a deciding run invoked with a relative LANE argument would print a false-negative `C2_R46_PASS=false` whose only visible symptom is `EQUIVALENCE 0` — recommend the L1 pass an absolute lane path (or patch equivalence to `os.path.abspath(lane)` before chdir; `measure()` itself is unaffected since it runs before any cwd change).
- **F3 — INFO.** C2's counter reads round-45 orig counter blobs and `DATA_REV=ea25e0224fc81060414b27301c27bd1344669165` — shared pre-round-46 inputs, legitimate and identical for orig and hardened targets; not a cross-claim read.
- **F4 — INFO.** Self-containment of deletions verified: no other `SOURCES.md` row's used-by cites r5/r6/r9 (`SOURCES_CENSUS: CLEAN` at exp2), and the C3 counter's self_pin stays 1 at all three mutant revs (counter byte-identical at every tested commit).

## Verdict

Causal separability **holds as designed** for all six ordered pairs at the counter-verdict level: each of C1/C2/C3 is verifiable — and verifies identically — with any sibling claim's wave-1 artifacts absent (exp1: C3 PASS + C1 values unchanged without C2; exp2: C2 PASS unchanged without C3; exp3: C2 and C3 PASS unchanged without C1's restated tables). The single real entanglement is F1: C1's `sources-registry` stated literal `rows=120` counts C3's three rows, so the claim's truth (and its pass) borrows C3's landing — honestly detected by the counter, severity LOW. F2 is an orthogonal invocation footgun in the shared counter tooling, severity LOW.
