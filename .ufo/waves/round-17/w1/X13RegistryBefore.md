# X13RegistryBefore — independent before-measurement for C2 (operability)

Measured rev: `98bea7da5801f4bc58e4187690ee1687c8a5061f` (lane tip at dispatch).
Method: fleet-mirror clone `git clone` + `checkout` at that rev under
`/tmp/tameshi-r17w1-X13-a4vypf/fleet/tameshi-shokunin`, siblings symlinked
beside it; every registered **entry command** and registered **self-test
command** from the SKILL.md registries (rounds 12, 13, 15, 16 tables at
`SKILL.md:1499`, `:1548`, `:1676`, `:1806`; the round-14 table is marked
"historical — superseded" / "not an entry point", excluded) plus the
SCORECARD `## Capabilities` evidence commands (`SCORECARD.md:240-247`).
Run sequentially, `cwd` = clone root, stdin /dev/null, per-command capture.
Full row evidence: `.ufo/evidence/round-17/registry-before-manual.json`
(22 rows: argv, registered outcome quote, exit, key stdout, elapsed).

## Results

| Row | argv | Registered outcome (quoted) | Exit | Key stdout | s |
|---|---|---|---|---|---|
| r12-repeat-control-entry | `python3 tools/repeat-control.py --runs 3 --out $W/r12-controls -- bash -c 'printf controls-match'` | "0 clean; 1 failed; 2 and 64 could-not-evaluate" | 0 | `REPEAT_CONTROL: controls_match` | 0.03 |
| r12-repeat-control-snapshot | `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` | same (second registered form `--snapshot DIR`) | 0 | `SNAPSHOT_OBSERVED id=controls_match exit=0` / `controls_match` | 0.02 |
| r12-repeat-control-selftest | `python3 tools/repeat-control.py --selftest` | selftest cmd; SCORECARD: "PASS (29 cases), exit 0" | 0 | `SELFTEST: PASS (29 cases)` | 0.71 |
| r12-witness-count | `python3 tools/bash-witness-study.py count` | "0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage" | 0 | `counts killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10` / `unresolved none` | 0.04 |
| r12-witness-selftest | `python3 tools/bash-witness-study.py selftest` | selftest cmd of same row | 0 | `WITNESS_SELFTEST: 41/41 pass` | 0.05 |
| r13-pin-disposition-entry | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | "0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate" | 0 | `"status": "ok"`, `unchanged:3 changed:3 unavailable:0` | 0.06 |
| r13-pin-disposition-selftest | `python3 tools/pin-disposition.py --selftest` | SCORECARD: "18/18 PASS0" | 0 | `SELFTEST: PASS (18/18)` | 0.69 |
| r13-witness-metadata-check | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | "0 metadata_consistent/clean" | 0 | `WITNESS_METADATA: metadata_consistent reason=ok exit=0` | 0.03 |
| r13-witness-metadata-selftest | `python3 tools/witness-metadata.py --selftest` | SCORECARD: "selftest39/39 PASS0" | 0 | `SELFTEST: PASS 39/39` | 1.30 |
| r15-context-capture-check | `python3 tools/context-capture.py --check` | "0 clean (`context_consistent`)" | 0 | `CONTEXT: OK (id=context_consistent receipt=…/context-receipt.json sha256=05cb55b8… exit=0 findings=0)` | 0.03 |
| r15-context-capture-selftest | `python3 tools/context-capture.py --selftest` | selftest cmd of same row | 0 | `SELFTEST: PASS (49/49)` | 1.24 |
| **r15-disposition-entry-as-written** | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | cell: "`--root .` returns 2 `expected_input_digest_mismatch` by design" | **2** | `"kind": "expected_input_digest_mismatch"` | 0.03 |
| r15-disposition-entry-archived-root | `python3 tools/evidence-disposition.py --root $W/archive-28aeef4 --dispositions .ufo/evidence/round-14/dispositions.json --json` | cell: "`--root` on `git archive 28aeef4` extracted to /tmp → 0 clean" | 0 | `"expected_inputs_verified": ["tools/pin-disposition.py"…]` | 0.03 |
| r15-disposition-selftest | `python3 tools/evidence-disposition.py --selftest` | SCORECARD: "PASS34/34 exit0" | 0 | `SELFTEST: PASS (34/34)` | 0.90 |
| r16-mutate-selftest | `bash tools/mutate-and-run.sh --selftest` | "selftest 0 pass"; SCORECARD: "`MUTATE_SELFTEST: 80/80 pass`, exit 0" | 0 | `MUTATE_SELFTEST: 83/83 pass` + `VERDICT: PASS` | 5.17 |
| r16-mutate-regression | `bash tools/mutate-and-run.sh --regression` | "regression 0 PASS"; SCORECARD: "`REGRESSION: PASS (cases=6 …)`" | 0 | `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)` | 114.91 |
| r16-measure-rev | `python3 .ufo/evidence/round-16/measure.py --rev 98bea7da…` | "0 measured" | 0 | `"calibration_restraint_score": 8, "depth_score": 7, "rows": 55` | 0.04 |
| r16-measure-selftest | `python3 .ufo/evidence/round-16/measure.py --selftest` | same row | 0 | `MEASURE_SELFTEST: 38/38 pass` | 0.75 |
| r16-assemble-selftest | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | "0 every bucket covered" | 0 | `SELFTEST: all checks passed` | 0.03 |
| cap-sources-census | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | "exit 0, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`" | 0 | `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | 0.06 |
| cap-context-verify | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4d…` | "exit0 … selftest49/49, frozen0, missing-env1, tamper2, usage64" | 0 | all lines `…: PASS`, incl. `sources-census: PASS exit=0` | 1.75 |
| info-disposition-before *(historical recipe, not registered)* | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json` | r14 recipe step 2: "must fail … exit1" | **2** | `"kind": "expected_input_digest_mismatch"` | 0.03 |

SCORECARD Capabilities rows for `mutation sweep runner`, `six-leg regression
ledger`, `repeated pristine-control gate`, `six-leg content-disposition
probe`, `exposed witness provenance correction`, `effective expectation
reconciliation` cite selftest argv identical to rows above — covered, not
re-run (identical argv → identical run).

## Held / total

**21/21 registered rows held** (informational historical row excluded from
the count; see finding 3). Every registered entry command returned an exit
inside its registered verdict map, including the disposition row returning
**2 `expected_input_digest_mismatch` exactly as the updated round-15 cell
prescribes** (the r16 harm), and its maintained route via `--root` on an
extracted `git archive 28aeef4` returning **0 clean**.

## Findings for the L1

1. **C2's "as-written" brokenness is real but already registered:** the
   r15 disposition row *as written* (`--root .`) exits 2
   `expected_input_digest_mismatch` — the registered cell now prescribes
   exactly that, so the row "holds" against its updated registration while
   remaining inoperable at `--root .`. The maintained route (archive root)
   gives 0 clean. R16-OP1's v2 manifest plan should make `--root .` → 0.
2. **Stale SCORECARD quotes (wording drift, not outcome drift):**
   `MUTATE_SELFTEST: 80/80` is now **83/83**; `REGRESSION: PASS (cases=6`
   is now **`cases=7`** (seventh leg `js-round-gate`, band exact). Both
   still exit 0/PASS. The Capability cells quote obsolete counts.
   Likewise `dispositions-before.json` recipe exit is now 2 not 1 (below).
3. **`dispositions-before.json` unreachable at `--root .` too:** the r14
   recipe's step-2 command (`--dispositions dispositions-before.json`)
   exits 2 `expected_input_digest_mismatch`, not the recipe's "exit 1".
   Contract A's new `.ufo/evidence/round-17/dispositions-before.json`
   expects "1 failed, producer_before unresolved" — note the r14 file at
   `--root .` currently cannot reach the row check at all; input pinning
   fails first.
4. **r16 measure already prints `calibration_restraint_score: 8,
   depth_score: 7`** at the dispatch rev (`--rev 98bea7da` against the
   committed `.ufo/evidence/round-16/coldread/ledger.json`).

## Environment / evidence

- Runner: `/tmp/tameshi-r17w1-X13-a4vypf/runner.py` (sequential, stdlib);
  raw capture `/tmp/tameshi-r17w1-X13-a4vypf/results.jsonl`.
- `git archive 28aeef4` extracted to `/tmp/tameshi-r17w1-X13-a4vypf/archive-28aeef4`.
- Total wall 127.9 s; no timeouts; no tool installs needed.
- Live lane left untouched (clone-only execution; `--out`/`mkdtemp` targets
  inside `/tmp/tameshi-r17w1-X13-a4vypf`).

Verdict: **holds** — 21/21 registered commands return their registered
outcome at the branch tip; the harmed row is registered-as-broken (2 by
design) with the archive-root route working.
