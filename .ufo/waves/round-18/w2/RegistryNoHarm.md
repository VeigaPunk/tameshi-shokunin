# RegistryNoHarm — round 18 wave 2 (FALSIFY), operability no-harm monitor

Seat: TameshiR18.RegistryNoHarm (reviewer, leaf). Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
Claim under attack (C2 no-harm): "registry full 32/32 held at e08271a (3 superseded rows)", and no
previously admitted outcome lost relative to `.ufo/evidence/round-17/registry-full-e3827ee.json`.

## Setup

- Clone: `W=/tmp/tameshi-r18w2-RegistryNoHarm-ujQdts`, `C=$W/fleet/tameshi-shokunin` (sibling `*-shokunin`
  symlinks in `$W/fleet`), detached at 01d586dd (`git rev-parse HEAD` = 01d586ddbc5f…).
- Every run used bwrap with the fleet read-only, no network and a private /tmp:
  `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind $W $W --unshare-net --die-with-parent --chdir $C env -i PATH=$PATH HOME=$W/hN TMPDIR=$W/tN GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 tools/registry-check.py …`
- Ruler identity: `tools/registry-check.py` sha256 `e072fd39…2899`; `tools/registry.json` sha256
  `d2d1972e398074d1e4bc1298eb75f6b69e2395b16c81b130a62a377a182ab2ad` at e08271a and 01d586dd. The round-17
  registry, sha256 `98bdc23c…0630`, is byte-identical at e3827ee, 30b0ca8, 183f87b, 93d22aa, aee4f36 and 58e5d53.
  `git log -- tools/registry.json` shows that e08271a is the only round-18 commit that touches it.
- No git writes in the lane. I wrote nothing in the lane except this report. Receipts stay in scratch
  (`$W/out/`); their sha256 values are listed below. No tools were installed or updated.

## Commands, exits, results

| # | command (from `$C`) | exit | REGISTRY_CHECK | receipt sha256 (`$W/out/runN.json`) |
|---|---|---|---|---|
| 1 | `--rev 01d586dd… --json` | 0 | held=32/32 superseded=3 | 678b1413…6c7e |
| 2 | `--rev 01d586dd… --tag baseline --json` | 0 | held=23/23 superseded=2 | c2eeb093…3966 |
| 3 | `--rev 183f87b8… --registry $C/tools/registry.json --tag baseline --json` | 1 | held=22/23 superseded=2 | 4c721c09…fc53 |
| 4 | `--rev 01d586dd… --registry <183f87b:tools/registry.json> --json` (new rev, OLD registry) | 1 | held=26/28 superseded=1 | 833bec29…fbd1 |
| 5 | `--rev 183f87b8… --registry $C/tools/registry.json --json` (old rev, full NEW registry) | 1 | held=26/32 superseded=3 | 8a28f3e4…5fcd |
| 6 | `--rev e08271ae… --json` (the claim's own rev) | 0 | held=32/32 superseded=3 | 7247ab87…4bd6 |

Runs 1–3 are the assigned commands. I added runs 4–6 for the lost-outcome question and to reproduce the claim at its own rev.
- The `--rev` mode reports these `rev_resolved` values: 01d586dd (runs 1, 2, 4), 183f87b (runs 3, 5) and e08271a (run 6).
- The registry sha256 is d2d1972e in every run except run 4, which reports 98bdc23c.
- The slowest row in every run was `mutate-and-run-regression`, at 116–270 s against a 900 s timeout. No other row came close to its timeout.

### Every differs row

- Run 1, run 2 and run 6 have no differs rows.
- Run 3 has one: `ROW evidence-disposition-round18 expect=0 got=2 differs`.
  - stdout `"kind": "dispositions_missing", "message": ".ufo/evidence/round-18/dispositions.json"`.
  - The file does not exist at 183f87b, so this is expected.
- Run 4 has two:
  - `ROW evidence-disposition-round17 expect=0 got=2 differs`
  - `ROW evidence-disposition-round17-before expect=1 got=2 differs`
  - Both stdout tails are `could_not_evaluate` / `expected_input_digest_mismatch`: `tools/bash-witness-study.py: observed 8dfaa25a… expects 49e9e5e2…`.
- Run 5 has six. Each is the old rev missing a file that round 18 adds:
  - `evidence-disposition-round18` got=2 (`dispositions_missing`)
  - `evidence-disposition-round18-before` got=2 (`dispositions_missing`)
  - `trace-inputs-selftest`, `measure-round18-selftest`, `assemble-round18-selftest` and `defect-probes-selftest` all got=2. Each stderr reads `python3: can't open file …: [Errno 2] No such file or directory`.

### The three superseded rows: got values

| row (tools/registry.json) | superseded_by | got @01d586dd (run 1) | got @e08271a (run 6) | got @183f87b (run 5) |
|---|---|---|---|---|
| `evidence-disposition-round17` (:196-223) | evidence-disposition-round18 | 2 | 2 | 0 (admitted outcome, needles present) |
| `evidence-disposition-round17-before` (:224-250) | evidence-disposition-round18-before | 2 | 2 | 1 (admitted outcome) |
| `evidence-disposition-round14-superseded` (:305-327) | evidence-disposition-round18 (retargeted from round17) | 2 | 2 | 2 |

- At the two new revs (01d586dd and e08271a), all three rows fail the same way: `"status": "could_not_evaluate"`, `"id": "expected_input_digest_mismatch"` on `tools/bash-witness-study.py`, observed 8dfaa25a, expected 49e9e5e2.
- At 183f87b, the round-14 row fails on `tools/mutate-and-run.sh` instead (observed fb6d86d5, expected 75ed934d). It got the same value, 2, at round 17 (e3827ee receipt).

### Claim reproduction

- Run 6 (e08271a) and run 1 (01d586dd) match the L1 receipt `.ufo/evidence/round-18/registry-full-e08271a.json` row for row. I compared status, got and held for all 35 rows, and both comparisons came out identical (`True`).
- `run1.stderr` and `run6.stderr` are byte-identical (sha256 `cf9e1bf9…790e`).
- **Result:** the claim "registry full 32/32 held at e08271a (3 superseded rows)" reproduces, and it also holds at the read rev.

## Was any previously admitted outcome lost? (vs `.ufo/evidence/round-17/registry-full-e3827ee.json`, held=28/28 superseded=1)

**Registry diff, 98bdc23c → d2d1972e:**
- No row was removed.
- Six rows were added: evidence-disposition-round18, evidence-disposition-round18-before, trace-inputs-selftest, measure-round18-selftest, assemble-round18-selftest, defect-probes-selftest.
- Exactly three rows changed, and only in status or superseded_by:
  - round17 and round17-before went from active to superseded.
  - round14-superseded's `superseded_by` went from round17 to round18.
- No row has a changed argv, `expect.exit`, `stdout_contains` or `timeout_s`.

**The 26 round-17 rows that are still active:**
- All hold at 01d586dd under the new registry (run 1) and under the old registry (run 4).
- All hold at 183f87b under the new registry (runs 3 and 5). The new registry therefore did not move the goalposts for any old row.
- After normalising /tmp paths, the stdout tails are either identical or show non-decreasing counts:

| row | round 17 | 01d586dd |
|---|---|---|
| `bash-witness-selftest` | WITNESS_SELFTEST 41/41 | 43/43 |
| `evidence-disposition-selftest` | SELFTEST: PASS (56/56) | (63/63) |
| `mutate-and-run-selftest` | MUTATE_SELFTEST 95/95 | 96/96 |
| `mutate-and-run-regression` | REGRESSION: PASS cases=7 passed=7 | cases=8 passed=8 |
| `measure-round16-rev` | recorded_cases 7 | 8 |
| `registry-check-selftest` | 34 cases | 46 cases |

  `measure-round17-selftest` stays at 94/94.

**The two round-17 rows that were superseded:**
- Run 4 shows that, strictly, these outcomes no longer reproduce at the new rev under the round-17 registry. The reason is a by-design byte change to `tools/bash-witness-study.py` (49e9e5e2 → 8dfaa25a), which is the C2 P11 GIT_* scrub fix landed in 58e5d53.
- Their outcomes are carried in substance by the round-18 replacement rows. Evidence:
  - The dispositions manifests differ only by one added `historical_inputs` entry: `.ufo/evidence/round-18/dispositions.json:20-23` (and the same in `dispositions-before.json`) pins `tools/bash-witness-study.py` to rev `4acc607dfd79…`. Round 17 already used this mechanism for `mutate-and-run.sh` and `pin-disposition.py` (`:12-19`). I checked with `diff` over the `json.tool --sort-keys` output of both files, for both pairs.
  - The pin is truthful:
    - `git show <rev>:tools/bash-witness-study.py | sha256sum` gives 49e9e5e2 at 4acc607d, e3827ee and 183f87b, and 8dfaa25a at 58e5d53 and 01d586d.
    - 4acc607d is an ancestor of 01d586d (`merge-base --is-ancestor` succeeded).
    - The expected digest is `.ufo/evidence/round-13/expected.json:11` (49e9e5e2…).
  - Full outputs compared field by field: I ran round-17 dispositions at 183f87b and round-18 dispositions at 01d586dd, for both the clean pair and the before pair.
    - The 12 output rows are identical in name, state, outcome, expected and observed exits, mismatches and expectation.
    - `counts`, `findings`, `inputs_verified`, `expected_inputs_verified`, `informational`, `supersedes` and `expected_file` are all identical.
    - Only three fields differ: `expected_inputs_historical` (one extra entry), `tool_sha256` (f8f05c7a → 66655a3a) and the dispositions path.
    - Exits were 0/1 at round 17 and 0/1 at round 18.
  - Falsification of the re-pin in a scratch clone at 01d586dd, using `tools/evidence-disposition.py --root . --dispositions <variant> --json`:

| variant | exit | result |
|---|---|---|
| control (unmodified round-18 file) | 0 | `clean` |
| pin moved to 58e5d53d… | 2 | `expected_input_digest_mismatch` |
| bash-witness entry dropped | 2 | `expected_input_digest_mismatch` (the round-17 failure) |
| rev `000…0` | 2 | `historical_input_unavailable` |

    The waiver discriminates; it is not a blanket bypass.

**Answer:** no previously admitted outcome was lost in substance. Two round-17 rows were retired with a lossless and falsification-checked carry. Every other admitted round-17 outcome still holds with unchanged expectations.

## Findings (by severity)

No critical or high findings. Nothing changes held/total.

1. **Minor (ruler verification gap): the `non_hermetic_argv` guard is blind to the real fleet when the monitor runs from a clone.** Wave seats are instructed to run it that way.
   - Under `--rev`, `fleet_root = os.path.dirname(os.path.realpath(root_requested))` (`tools/registry-check.py:1861`). `_argv_outside_fleet` then does a string-prefix compare against that root (`tools/registry-check.py:625-638`).
   - Probe: a two-row scratch registry, run from `$C` with `--rev 01d586dd` (exit 1, `$W/out/probe-hermetic.json` sha256 `f3866ac3…69e5`):
     - `ROW live-fleet-path expect=0 got=0 held`. Its argv names `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry.json`, it has no `external` flag, and `non_hermetic_argv` is absent.
     - `ROW mirror-fleet-path expect=0 got=non-hermetic differs`. Its argv names the `/tmp/…/fleet` mirror path.
   - A corollary for the receipts: the L1 receipts (e3827ee and e08271a) record `non_hermetic_argv: ["/home/vgpnk/Projects/shokunin"]` for `pin-disposition-read`. My clone-run run 1 does not, so additive fields differ between L1 runs and seat runs.
   - No current impact. A static scan of all 35 argv vectors finds exactly one absolute path, on `pin-disposition-read` (`tools/registry.json:105-130`), and that row is declared `external: true`. For future rows, though, the guard does not protect clone-based reproductions.
2. **Minor (new-row strength): `assemble-round18-selftest` is exit-only.**
   - Its expect is `{"exit": 0}` with no `stdout_contains` (`tools/registry.json:739-756`, expect at `:747-749`).
   - Its round-16 and round-17 siblings require `SELFTEST: all checks passed`.
   - The tool prints a usable trailer, `SELFTEST: 80/80 pass` (run 1 stdout tail).
   - As written, any exit-0 path holds the row, including a selftest that runs zero checks.

## Residual risk and verification gaps

- **Pre-existing, not new harm:** two rows expect exit 1 with no needle: `repeat-control-snapshot-mismatch` (`tools/registry.json:23-41`) and `context-capture-mapping-suffix` (`:396-417`). A Python crash would also exit 1. Today their stdout shows the intended failure (`REPEAT_CONTROL: controls_mismatch`; `CONTEXT: MISMATCH (id=mapping_mismatch …)`), so the held result is genuine at 01d586dd.
- **Rev-insensitive rows:** two rows are declared external: `pin-disposition-read` (`:105-130`, `--root /home/vgpnk/Projects/shokunin`) and `verify-round15` (`:590-612`).
  - `pin-disposition-read` grades the live fleet, not the graded rev. It held at both 183f87b and 01d586dd, and its stdout shows a live sibling head (`c68945c2…`).
  - Its held result is therefore not evidence about either rev, and it can flip with sibling-lane activity.
- **Not reproduced:**
  - I did not run from the live lane; the contract forbids it. So I could not reproduce the L1's live-lane `non_hermetic_argv` annotation.
  - Receipts are scratch-only (`$W/out`), cited by sha256. Nothing was copied into the lane.
- **Sandbox and concurrency:**
  - All six runs were sandboxed: read-only fleet, `--unshare-net`, private /tmp. Every row held exactly as in the L1 receipts, so the sandbox introduced no deltas and no row needs network or writes outside its clone.
  - Runs 1–3 and 4–5 ran concurrently. Timeout margins stayed ≥3× (regression 116–270 s against 900 s).
- **Other scratch receipts:**

| file | sha256 |
|---|---|
| `$W/out/ed17-at-183f87b.json` | e1be6392… |
| `$W/out/ed17b-at-183f87b.json` | eae51541… |
| `$W/out/ed18-at-01d586d.json` | 53c74092… |
| `$W/out/ed18b-at-01d586d.json` | 159d91c8… |
| `$W/out/probe-p1-rev-moved.json` | 298a7170… |
| `$W/out/probe-p2-entry-dropped.json` | 298a7170… |
| `$W/out/probe-p3-rev-bogus.json` | 70205d69… |

  The p1 and p2 probes produce the same message, so their files are byte-identical.

Verdict: **holds**. Registry 32/32 with 3 superseded rows reproduces at e08271a and at 01d586dd. No admitted round-17 outcome was lost in substance; the two retired disposition rows carry over losslessly and the carry is falsification-checked. There are two minor ruler gaps: the hermetic guard is blind under clone runs, and `assemble-round18-selftest` is exit-only.
