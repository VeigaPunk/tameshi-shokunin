# Wave 1 — Controls review (round 42)

Seat: L1Tameshi42.ReviewControls. Read-only lane checkout; only this report written.
Scope: `control/` (c1-do-nothing, c2-v3-in-slot, c2-junk, junk-tool.py) and `before/` base receipts.
Freeze `322b5cd32b4319a05340d249ae752d12a9e6b19f`, REV `c77c2b7e64d2e356381441ecf94abac03e984606`.

## Findings

### 1. c2-junk re-run — byte-identical to receipt, exit 1 (control valid)
Command (from fleet root):

```
python3 .ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c77c2b7e64d2e356381441ecf94abac03e984606 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f --tool-file .ufo/evidence/round-42/control/junk-tool.py
```

Rerun: exit 1, stdout `diff`-identical to `control/c2-junk.stdout`, stderr empty.
Profile: FAIL F01–F09 + all three live sites; `fixtures_pass=1/10`, `selftest_exit=0`,
`live_unflagged_v3=3`, `live_unflagged_v4=0`, `C2_R42_CONTROL_PASS=false`.
`tool_sha256=99424c38…` == sha256(junk-tool.py) (verified by hashing). Junk prints every site
not-unflagged/not-explicit → the vacuous "all clean" tool fails the frozen predicate, as the
contract specifies (F02/F03/F05/F06/F07/F08/F09 plus F01/F04 and the live sites).

### 2. c2-v3-in-slot re-run — byte-identical to receipt, exit 1 (control valid)
Command:

```
python3 .ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c77c2b7e64d2e356381441ecf94abac03e984606 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f --tool-file tools/write-path-census-v3.py --text-mode
```

Rerun: exit 1, stdout `diff`-identical to `control/c2-v3-in-slot.stdout`, stderr empty.
Profile: FAIL F01, F04 + the three live sites; `selftest_exit=1`, `fixtures_pass=8/10`,
`live_unflagged_v4=3`, `C2_R42_CONTROL_PASS=false`. v3 bytes placed in the v4 slot skip the
claimed work (no attr-bound/outflag resolution) and fail the frozen predicate.

Note on `selftest_exit=1`: it is a harness artifact, not a v3 defect. v3's selftest resolves
its fixtures relative to `__file__` (`FIXTURE_REL = '.ufo/evidence/round-41/census/fixtures.json'`,
`tools/write-path-census-v3.py:44`), so the temp copy at `work/v4.py` raises FileNotFoundError.
Reproduced: copying v3 to `/tmp/…/v4.py` and running `python3 -I ./v4.py --selftest` exits 1 with
traceback; the in-place `python3 -I tools/write-path-census-v3.py --selftest` exits 0.

### 3. C1 controls — skip the claimed work and fail the frozen predicate
- `before/c1-at-base` reproduced exactly: `--rev c77c2b7e… --freeze 322b5cd…` → exit 1,
  `m10=1 records=3 sources_rows=109 C1_R42_PASS=false` (identical to receipt).
- Freeze-state check (allowed `--rev`): `--rev 322b5cd…` → same failure (`m10=1 records=3`).
  HEAD == freeze; the residual receipt still asserts `present=false` for
  `.ufo/waves/round-41/residual/ResidualReceipts.md` while the tree holds the file (`git show
  HEAD:.ufo/waves/round-41/residual/receipt.json`). A scan of every tracked `.ufo/waves/*.json`
  at HEAD finds no covering `supersedes` receipt (only round-21 `original-outcomes2-corrected.json`,
  whose supersedes value is not a receipt path). So m10 cannot clear without the claimed work.
- `control/c1-do-nothing` (records=6, m10=1, all other classes 0, PASS=false): matches contract
  `do_nothing_control` scenario 2 (scratch clone adds the three round-42 records but no superseding
  receipt → m10 stays 1). Reproduced on a scratch clone
  (`git clone --shared` + only the three record sections committed as `aa24bd73b5ac280ee0f8a4e22580b4ec298957c3`):
  identical profile, exit 1. **Provenance gap**: the receipt's `rev=5e74a8cbd555b2589c64c5f92eb4baf8679fbb1b`
  is unresolvable in the lane repo (`git cat-file -t 5e74a8cb…` fails; HEAD is the freeze) and in
  the fleet repo — consistent with a deleted scratch clone, so the exact original commit cannot be
  re-verified. The scenario itself is confirmed (see reproduction).

### 4. Cheaper controls
- C1: the cheapest valid do-nothing is the at-base run (`before/c1-at-base`) — exists and
  reproduces. The counter's selftest T2_* cases (`calibration/measure.py` selftest) already encode
  the "records added without supersede → m10 stays" and "bad supersede → m10>=1" behaviors
  deterministically, so `control/c1-do-nothing` adds no coverage beyond at-base + T2 while costing a
  clone+commits and leaving an unverifiable rev. If the records-added variant is kept, the producing
  clone's commit hash should be recorded in the receipt so it is checkable.
- C2: `--tool-file tools/write-path-census-v3.py --text-mode` is already the cheapest real-tool
  control (reuses a tracked file, no new artifact). `junk-tool.py` is justified for the contract's
  dangerous case (a tool asserting every site flagged/resolved); a minimal alternative that prints
  `{"sites": []}` would yield a different profile (`expected-value sites=0` across all fixtures) and
  would not exercise that protection, so no materially cheaper equivalent fulfills the intent. Nit:
  `junk-tool.py:2` hardcodes the absolute path to the *live* v3 instead of REV's v3; benign today
  because live v3 sha == V3_SHA == `095924a7…` (verified).

## Residual risk / verification gaps
- `control/c1-do-nothing` original rev `5e74a8cb…` unverifiable (not in lane or fleet); content and
  semantics confirmed by reproduction on scratch clone `aa24bd73…`.
- `census/mutants.json` is not present at REV (glob of `round-42/census/` shows only `measure.py`),
  so the deciding C2 predicate cannot pass yet — orthogonal to controls.
- No tools installed; no cleanup pending (scratch clone and temp rerun captures deleted).
