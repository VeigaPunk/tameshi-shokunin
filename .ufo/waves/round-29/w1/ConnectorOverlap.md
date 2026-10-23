# ConnectorOverlap — sibling scan for F6 reducers, shrinkers and survivor-probe fixtures

## Verdict

Four real sibling overlaps, no code to absorb, and one bounded move worth adopting (it comes from the round-29 cache, not from a sibling).

- **Mechanical reducer:** exactly one sibling lane holds a working reducer — `kake-shokunin` round 35 `difftest.py:326-388` (`minimize_case`), greedy unit deletion capped by `MAX_MINIMIZATION_ATTEMPTS = 160` (`:30`), with the honest limit stated in its report (`kake-shokunin/.ufo/waves/round-35/w1/ExecDifferentialGenerator.md:17`: "not a global byte-level minimizer").
- **One-unit deletion harness:** `kotoba-shokunin/verifiers/box_proof_case_deletion.py:459-546` — control first, then delete exactly one manifest entry and re-run; refuses to measure when the intact control is not clean. Same primitive as F6's `one_min` loop, with unit = manifest case instead of one TSV line.
- **Survivor-kill conventions:** `kagi-shokunin` lands survivor-killing cases in the production fixture and names the seat (`corpus/rendered-text-v1.py:140-143`), with a three-stage exit table pristine → mutant → restored (`0 → 1 → 0`) at `.ufo/waves/round-24/build/MutNormalizer.md:41-45`; `kumitate-shokunin/scripts/gate-mutants.mjs:9-11,148-150,521-522,932-940` holds the fleet's most explicit killed/survived/drift/unstable state machine.
- **Not found anywhere:** any sibling fixture minimizer for tameshi's substrate (line-unit TSV plus materialized `host/` tree), any 1-minimality assertion, any ddmin implementation in a sibling lane. Searches for `ddmin`, `delta debug`, `creduce`, `1-minimal`, `one-minimal`, `test-case reduction` over all 20 sibling lanes returned only false positives (`c1-minimal.py`, `fixture-r21-minimal.md`).

Tameshi absorbs nothing mechanically. The single move below is report-only and does not change the counter, the contract, or the predicate.

## Scope, method and bounds

- Scanned read-only: `/home/vgpnk/Projects/shokunin/{audio,chousa,game-dev-2d,game-dev-3d,kagi,kaidoku,kake,kama,kasegi,kengaku,kotoba,kotodama,kumitate,lore,mado,mori,revenger,souji,tabi,tsukuroi}-shokunin`. Never `tameshi-shokunin` for overlap evidence, never the fleet root.
- Read the round-29 cache (contract, `c2-measure-v2.py`) as the only source of the F6 definition; that is the canonical assignment surface, not an overlap source.
- No command was run in a sibling repository, no file written outside this report, no gate, selftest or sweep executed anywhere, no install or update.

## Overlaps, path by path

### 1. kake — a real reducer (greedy, retained output, disclosed limit)

- `kake-shokunin/.ufo/waves/round-35/evidence/w1-tools/difftest.py:326-388` — `minimize_case()` deletes one `Asset` at a time while `preserves(candidate)` keeps the target differential, then reduces HTML content in tokenizer chunks; attempt cap at `:30`; a `complete` flag is returned with the result.
- `kake-shokunin/.ufo/waves/round-35/w1/ExecDifferentialGenerator.md:5-6` — "Comparator/minimizer: lines 216-385"; `:13` — "All three minimized reproducers retained `complete:true`; their HTML contains only two nonempty `og:url` meta tags"; `:17` — "greedy over manifest page entries and HTML tokenizer chunks, not a global byte-level minimizer".
- Difference from F6: kake's loop stops at a greedy fixed point and never asserts single-unit irreducibility; F6's counter both matches its own frozen ddmin output (`c2-measure-v2.py:264`) and tests every single-unit removal (`:267-271`). Kake's reducer is the sibling precedent for the *retained minimized artifact plus a stated limit*; nothing about it transfers as code.
- Whether tameshi absorbs: **no** (different substrate, no 1-minimal claim). The one transferable element is a sentence shape, not a mechanism — the F6 entry should state the reducer's own limit the way kake's report does.

### 2. kotoba — the same one-unit deletion primitive, already test-harnessed

- `kotoba-shokunin/verifiers/box_proof_case_deletion.py:459-467` — the intact control must exit 0, else "case coverage is not measurable" and exit 2.
- `:476-491` — `attempt()` "Delete one manifest entry (only the entry) and re-run. The fixture directories are never touched": `reduced["cases"] = [c for c in manifest["cases"] if ...]`.
- `:546` — exit 1 unless the pinned denominator (`killed == 6`) is met.
- This is the F6 `one_min` loop with a different unit type. The convergence is useful evidence that the counter's shape (control first, delete one unit, require the verdict to flip) is the established fleet primitive, not an invention of this round.
- Whether tameshi absorbs: **no** — tameshi's counter already implements it (`c2-measure-v2.py:164-181`, `:267-271`).

### 3. kagi — survivor-killing cases, exercised and then committed

- `kagi-shokunin/.ufo/waves/round-24/build/MutNormalizer.md:41-45` — "Exact additional case that kills each survivor — exercised, not conjectured": survivor id, input bytes, pristine/restored expectation, mutant output, assertion exits `0 → 1 → 0`; exact witness argv at the cited `P/mutated.json:165-176,204-215,243-254`.
- `kagi-shokunin/corpus/rendered-text-v1.py:140-143` — the three killing cases landed in the production fixture with the seat named in the source comment: `# round-24 wave-1 mutation lane (MutNormalizer): three survivors killed`.
- `kagi-shokunin/.ufo/waves/round-23/falsify/RevCensusCases.md:188-193` — survivor list split into deletion and semantic classes with the killed set; `kagi-shokunin/corpus/QUALITY.md:106` (QM19) — "A timeout, setup/policy refusal, truncation or unaccounted row is invalid, never a surviving mutant."
- Whether tameshi absorbs: **partly, and not where it looks like it should.** The kagi convention of naming the seat *inside the fixture file* cannot transfer into F6's fixture: every line of `census.tsv`, `shapes.tsv`, `baseline.tsv` and `host.tsv` is a removable unit under `one_min`, so a comment row added to the fixture is a unit whose removal does not lose the kill and would break 1-minimality. Seat attribution belongs in `corpus/knowledge/survivor-fixture-minimization.md` and the lesson line, not in the fixture bytes. This is the one place a sibling convention actively conflicts with F6's predicate.

### 4. kumitate — the kill/survivor state machine

- `kumitate-shokunin/scripts/gate-mutants.mjs:9-11` — "An evaluable run that is not killed is SURVIVED; a disagreeing second run is UNSTABLE (exit-2 class)"; `:148-150` — exit map 0 all killed, 1 survived or drift, 2 "setup, nomatch, crash, unstable kill, timeout, control failure"; `:521-522` — drift versus killed; `:932-940` — `k43-exit-zero-with-verdict-fail-is-survived` and `k43-kill-confirmed-by-second-run` (`confirm=same`); frozen survivor ids that must be killed at `:221-231`.
- Whether tameshi absorbs: **no**. F6's oracle is deterministic (frozen gate bytes, materialized tree, fixed `PATH`/`HOME`/`LC_ALL`/`TZ` at `c2-measure-v2.py:157-161`), so second-run confirmation buys nothing; the divergence should be stated in the entry, not closed. The invalid-versus-survived split is mirrored by the counter returning exit 2 when pins or gate bytes are unresolvable (`:227-238`).

## False friends and adjacent-but-not-overlapping material

- `mori-shokunin` "minimization" is privacy and retention minimization of committed material (`corpus/lessons/round-18.md:32-33,55`; `corpus/lessons/round-17-verifier-spotcheck.md:392-394`), not fixture reduction. No overlap.
- `tsukuroi-shokunin/corpus/claim-ledger.sh:394-397` — "the file's *membership* is the invariant, not its length"; the round-12 mutation lane showed an equal-count path swap and a missing-final-newline off-by-one slipping a length rule; `:463-465` — a blank line is a setup error, not silent shrinkage. This is a shrink guard on a pin set. The transferable lesson is a residual class: **1-minimality is removal-only**. A one-for-one swap of a unit for another unit that still kills is not excluded by F6's predicate. The contract bound already says "1-minimal says nothing about bytes inside a line"; it does not say the swap class is open, and the entry should state the removal-only scope.
- `audio-shokunin/corpus/knowledge/2026-10-13-sox-act-autodetect-predicate.md:63-66` ("Fixture-authoring rule (fragility, now pinned): … file 256 = payload byte 188 = sample 94 LSB") and `2026-10-14-sox-autodetect-preemptor-ordering.md:95-97` (a payload signature at 16-24 or 65-68,128-131 reroutes detection regardless of byte 256). Same idea as F6 at byte granularity — the smallest edit that flips the verdict — on a WAV substrate. No absorption.
- `kagi-shokunin/corpus/lessons/round-16.md:67` — `--falsify` copies appended to files with no trailing newline, so "3 of 5 mutations merged into the last row and silently no-opped". This is the sibling class "fixture shape silently voids a line-granular mutation". Checked against F6: `lines_of()` pops only a trailing empty element (`c2-measure-v2.py:72-75`) and `materialize()` writes one `\n` per unit (`:114-121`), so a missing final newline cannot merge two units. The class does not reach the counter; a blank line inside a fixture file *is* enumerated as a unit and would be named as removable by `one_min`, so the fixture must not be padded.
- `kagi-shokunin/corpus/knowledge/adjacency-breadth.md:157-161,268-271` and `scope-gate.sh --falsify` (18 data mutations, catch required) are data-mutation suites against a gate; they are the inverse direction of F6 (F6 needs data that makes a *mutant* gate diverge). Adjacent vocabulary, no reduction.

## Contradictions between the prose contract and the operative counter (state, do not smooth)

1. The contract says units are "one line of census.tsv, shapes.tsv or baseline.tsv or one file under host/". The counter's units are the lines of four files including `host.tsv` (`FILES` at `c2-measure-v2.py:56-57`, `to_units` at `:103-104`); a host file is removed by removing its `host.tsv` line. Operationally equivalent, textually not identical.
2. The predicate says the fixture is "reduced by the counter's own ddmin to a committed 1-minimal fixture". The counter implements this as **exact ordered equality** of the `(file, line)` sequence between its ddmin output and the committed `minimized/` (`:264`). A differently ordered or differently partitioned but semantically equivalent fixture fails `ddmin_match`. Contract prose understates the strength; builders must treat the counter as the operative artifact.
3. `anchored` (`:249-251`) requires `original/census.tsv` byte-equal to the pinned kagi declaration, but accepts *subsets* for `original/shapes.tsv` and `original/baseline.tsv` (`set(...) <= set(...)`). Because `ddmin_match` is computed over the *committed original*, trimming those two files shrinks the search space and makes the ddmin match strictly easier. This is the one measurable weakening I found in the frozen F6 predicate.

## Proposed move (one, bounded, report-only)

**Obtain `minimized/` from the counter's own frozen `ddmin()` in the builder's scratch clone, and commit `original/shapes.tsv` and `original/baseline.tsv` as full copies of the pinned kagi declarations rather than subsets.**

Why this is the non-obvious move rather than a restatement of "build the fixture":

- It makes `ddmin_match` true by construction. The counter's reducer is frozen and importable (`c2-measure-v2.py:183-199`, complement form of S024's `DeltaDebuggingReducer`); calling it over `to_units(original)` with `Oracle.kills` (`:164-181`) produces exactly the sequence `:264` compares. Hand-reduction must otherwise reproduce a frozen greedy fixed point, order included — a much larger search than people expect.
- It closes the subset loophole by construction: full pinned copies of `shapes.tsv` and `baseline.tsv` put the ddmin search over the declaration the counter actually anchors, so `ddmin_match` measures reduction, not prior trimming.
- It is the cheapest use of the one sibling reducer shape that exists (kake's `minimize_case`: greedy deletion, retained output, stated cap). The counter's `ddmin` also caches oracle results by unit-key, so the cost is bounded by distinct subsets, not by raw calls.
- It adds no file beyond the fixture the claim already requires, touches no counter, contract or predicate, and changes no number.

Affected axes: **coverage (F6) improves** — stronger method evidence for the same predicate, with a cheaper path to it. **Calibration unchanged** — no counter, contract or predicate edit; the counter remains the authority. **Adjacency improves** — the sibling precedents (kake reducer, kotoba deletion harness) are named, and the seat-naming convention is routed to the entry instead of the fixture. **Operability unchanged** — no new tool, no new gate. **Freshness unchanged** — the pinned declaration and S024 snapshot are untouched. **Depth unchanged.**

## Risks

- Importing the counter in a builder's scratch clone executes the counter's `Oracle.run` with its fixed environment and `cwd=work` (`:157-161`) and reads the live kagi repo through the default `--kagi` path (`:216`). Both are read-only, but the builder must run it only inside its own clone and `/tmp` or `/fast/scratch/hyaku`, never in the lane.
- `ddmin` cost is O(n log n) oracle runs, each two `bash` invocations over a materialized tree; the census is 54 lines, so bounded, but a pathological oracle that always returns false walks the full complement schedule.
- The equal-count swap residual is not closed by any of this. If the entry claims more than removal-minimality, the claim overstates the predicate.
- If the build seat commits `minimized/` first and `original/` second, an intermediate run can print `ddmin_match=0` legitimately; that is a staging artifact, not a defect, and must not be reported as a falsifier.

## Verification (for the integrator, not run here)

In the build seat's clone at its candidate revision:

1. `python3 .ufo/evidence/round-29/c2-measure-v2.py --repo <clone> --rev <rev>` should print `fixture=present anchored=1 kill_original=1 ... ddmin_match=1 kill=1 one_minimal=1` and `PREDICATE: C2_F6_V2_PASS=true`.
2. Negative control at the base revision: the same command prints `fixture=absent` and `PREDICATE: C2_F6_V2_PASS=false`.
3. Anchor check: `cmp <clone>/.ufo/evidence/round-29/f6/original/shapes.tsv <kagi>/corpus/state-shape.tsv` and the same for `baseline.tsv` versus `<kagi>/corpus/drift-baseline.tsv` must be silent (full copies, not subsets).
4. If `ddmin_match=0`, the printed `not-minimal:` lines (`:271`) name removable units; they are the reducer's own output, not a hand judgement.

## Report-only disclosure

I edited no sibling file, ran no sibling command, installed or updated no tool, and wrote only this report. The F6 fixture directory did not exist at scan time, so every statement about the counter is a read of the frozen cache, not a run.
