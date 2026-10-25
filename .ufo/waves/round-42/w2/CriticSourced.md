# CriticSourced — round 42 wave 2 (FALSIFY): does C2 rest on S157; is S158 sound tier A

Seat: L1Tameshi42.CriticSourced (critic, read-only). Accessed 2026-10-25. Lane tip read: `a21845f523b75adbd3e3f7a62af91294db224ad9`.
Every counter run below is a control (`--probe-mutant` / `--tool-file`, label `C2_R42_CONTROL`) at `--rev a21845f…` (pre-run), never the deciding run. Scratch: `/tmp/tameshi-r42w2-CriticSourced-JxN8` (copies of v4 only; deleted before return). No tools installed.

## Findings

### F1 — S157 is load-bearing for the v4 code, but only through `--selftest`. The counter's battery and mutant oracle never exercise it (SURVIVES with a gap)

- The S157-derived step is `tools/write-path-census-v4.py:96-99`: `dest = (longs[0] if longs else options[0]).lstrip('-').replace('-', '_')`. This is §dest at snapshot lines 1504-1514: first double-dash long option, strip the leading `-`, internal `-` becomes `_`.
- Every outflag case the counter checks uses a bare `--out` with no internal dash and no `dest=`: `.ufo/evidence/round-42/census/measure.py:144` (F04), `:160` (F05 `--input`) and `:175` (F06). The one live site, `tools/registry-replay.py:259`, also declares a bare `p.add_argument('--out')`. For a bare `--out`, the dest is simply `out`, with or without S157.
- Ablation mutants, built on scratch copies of v4 (line 98 or the `out_dests` table replaced):

| mutant | `python3 -I <m> --selftest` | `measure.py … --probe-mutant <m>` |
|---|---|---|
| mA: drop `.replace('-', '_')` | exit=1, `FAIL output_dir_param: explicit_out=False, want True` | `probe_outcome=survived` |
| mB: `options[0]`, not first long | exit=1, `FAIL output_dir_param …` | `probe_outcome=survived` |
| mC: dest from flag text | exit=0 | `probe_outcome=survived` |
| mD: argparse-free, hard-coded `{'out','output','out_dir','output_dir'}` table, `add_argument` ignored | exit=1, `FAIL output_flag_direct: explicit_out=False, want True` | `probe_outcome=survived` |

- Full control run on mA, `measure.py --lane … --rev a21845f… --freeze 322b5cd… --tool-file mA.py`:
  `selftest_exit=1 fixtures_pass=10/10 run_errors=0 live_1682_ok=1 live_1685_ok=1 live_123_ok=1 live_unflagged_v4=0 … C2_R42_CONTROL_PASS=false`.
  The unmutated v4 under `--tool-file` gives `selftest_exit=0 fixtures_pass=10/10 …` (tool sha256 `784de4c0…`).
- Reading:
  - S157 is not pure decoration. Without §dest, the selftest cases `output_dir_param` (v4 `:527-541`, `-o --output-dir` → `ns.output_dir`) and `output_flag_direct` (`:542-549`, `dest="target"`) fail, and the predicate requires `selftest_exit=0`.
  - Even an argparse-blind tool (mD) passes all 10 fixtures, all 3 live sites, and the oracle. The kill oracle (`measure.py:311-316`) runs only the battery and the live sites, not `--selftest`.
  - So the measured claim (fixtures, live sites, mutants) never depends on S157. The S157 dependency rests on a single bit: whether the unmutated tool's selftest exits 0.
  - Risk to the deciding run: if seat MutantAuthor writes an outflag mutant aimed at line 98 (dest derivation), it will be `survived`, and C2_R42_PASS will be false.
- Impacted axes: depth (C2 mutant adequacy for the outflag class), and the round's "sourced" gate.

### F2 — The entry's reading of S157 is contradicted by S157's own §default. v4 labels hidden-constant defaults `explicit_out` (BROKEN, fixable)

- The entry states, at `corpus/knowledge/r42-attribute-and-outflag-destinations.md:16-17`: "the destination of a write rooted at `ns.out_dir` is whatever the operator passed on the command line".
- The same snapshot, §default, lines 1209-1211: "The default keyword argument of add_argument() specifies what value should be used if the command-line argument is not present." (18 words). Lines 1220-1221 add that `set_defaults()` supplies the same.
- Counterexample (scratch `cx_default.py`): `ap.add_argument("--out", default="tests/golden")`, then `emit("{}", ns.out)`, which writes to `os.path.join(dest_dir, "expected.json")`.
  - v4 `--file cx_default.py --json` reports line 6 as `explicit_out: True, unflagged: False`, resolved `… argparse --out`.
  - Running the file with no flag tries to open `tests/golden/expected.json`. The `FileNotFoundError` only shows that the write path is the hidden default.
  - `set_defaults(out="tests/golden")` (scratch `cx_setdefaults.py`) gives the same result: `explicit_out: True, unflagged: False`.
- So a golden-overwriting write that the operator never named passes as "operator names the destination". That is exactly the class F4 exists to catch. The entry's "What is not claimed" list (`:70-73`) does not exclude `default=`, `set_defaults` or `const=`.
- Live impact: none today. The lane's `--out` declarations have no default: `tools/registry-replay.py:259`, `tools/env-diff.py:207` (`type=Path`) and `tools/trace-inputs.py:975`. No wave-1 report raises it: `rg -n -i "default|set_defaults"` over `w1/ScoutArgparse.md`, `w1/ExecV4Tool.md` and `w1/ScribeEntryV4.md` returns only unrelated hits.
- Held correctly: `cx_firstlong.py` with `add_argument("--result", "--out")` and a write via `ns.out` gives `explicit_out: False, unflagged: True`. v4 picks dest `result` per S157 §dest (runtime check: `Namespace(result='d')`), so it does not over-claim there.
- Impacted axes: depth (soundness of the outflag edge class), and source fidelity, because the cited row is read partially.

### F3 — The contract's `sourced` field is stale after P1: C2's sourcing now rests on S157 alone

- `contract.json:48`: "the kill oracle cites the PIT outcome vocabulary row adopted this round".
- `post_freeze_amendments` P1 (`contract.json:71`) withdraws PIT as support. The oracle now rests on `SKILL.md:208-209` and S001, and S001 is a held row re-opened this round, not opened this round.
- The entry agrees: it cites S158 only as the divergent tool (`r42-attribute-and-outflag-destinations.md:61-62`).
- Result: the round's "one claim on a row opened this round" requirement for C2 hangs on S157 only. F1 and F2 bound how much weight S157 carries. No amendment updated the `sourced` field.
- Impacted axis: provenance (false provenance in the contract text).

### F4 — S158 is a sound tier-A row; one anchor gap (SURVIVES)

- Byte identity and pin:
  - `git ls-remote https://github.com/hcoles/pitest HEAD refs/heads/master` returns `f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6` for both refs, so the pin is still master.
  - Fetching `raw.githubusercontent.com/hcoles/pitest/f7fe5adf…/pitest/src/main/java/org/pitest/mutationtest/DetectionStatus.java` gives sha256 `3bf295ad53126560ec284c42b384fc3288f7b2e674da987f38d7380ec5d419c6`, 2988 B, and `cmp` against `.ufo/evidence/round-42/sources/pit-DetectionStatus.java` prints `IDENTICAL`.
- Located content matches the row and the entries:
  - snapshot line 37 is `TIMED_OUT(true),`
  - line 63 is `RUN_ERROR(true),`
  - lines 91-98: `getForErrorExitCode` maps OUT_OF_MEMORY to MEMORY_ERROR, TIMEOUT to TIMED_OUT, and everything else to RUN_ERROR
  - line 108 is `isDetected()`, which returns the `detected` field (line 78)
- Tier: upstream source pinned at a commit, kind `code`. This matches the lane's precedent for tier-A code rows (S005, S087, S106 in `corpus/SOURCES.md:16,96,118`).
- Anchor gap: the row's teaches cell (`SOURCES.md:128`) concludes "so its score counts run errors as detections". `DetectionStatus.java` alone does not show the score. The score lives in `pitest-entry/…/statistics/ScorePrecursor.java:44-45` (`a -> a.getStatus().isDetected()`) and `MutationStatistics.java:84-85` (`getPercentage(getTotalMutations(), getTotalDetectedMutations())`), both fetched at the same commit.
  - The conclusion is true, but it is outside the row's anchor. The lane's own entry concedes the narrower status at `pit-outcome-vocabulary.md:66` ("a source file pinned at one upstream commit, not a documented contract").
  - Fix: extend the anchor to those two files, or soften "so its score counts" to "isDetected() is true for".
- Impacted axis: provenance (minor).

## Smallest safe corrections

1. F2, v4 and entry: refuse `explicit_out` when the matching `add_argument` carries `default=` or `const=`, or when a `set_defaults(<dest>=…)` names the dest. Add one selftest case and one oracle-visible fixture for this. In the entry, add `default=`, `set_defaults` and `const` to "What is not claimed", or narrow line 16-17's sentence to "when the option has no default". Live results do not change, because no live `--out` has a default.
2. F1, battery coverage: the frozen counter cannot be edited. Record in the round-42 lesson that the battery has no dashed or `dest=` output flag, so the S157 step is checked only by `selftest_exit`. MutantAuthor should know that an outflag mutant on `v4:98` will survive the oracle. That is an honest miss, not something to steer around.
3. F3, contract: add a post-freeze disclosure (rule_changed=false) that `claims.C2.sourced` leg 2 is withdrawn by P1, and that C2's this-round row is S157.
4. F4, S158 anchor: extend it to `ScorePrecursor.java:44-45` and `MutationStatistics.java:84-85` at `f7fe5adf`, or reword the teaches cell.

`BROKEN: C2's S157-derived outflag reading — S157 §default (snapshot 1209-1211) contradicts the entry's "whatever the operator passed"; v4 labels default=/set_defaults hidden-constant writes explicit_out, and the counter oracle cannot see the S157 step (4/4 ablations survive). S158 holds as tier A (byte-identical at master f7fe5adf; score claim anchored outside the row).`
