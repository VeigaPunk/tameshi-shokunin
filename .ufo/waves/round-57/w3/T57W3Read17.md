# T57W3Read17: cold read at C0b

Heading: `### Round-21 gate/probe registry — finite environment differential`

- Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`
- Frozen round-18 sectionize: lines **2007–2146**, SHA-256 `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06`.
- Verdict recommendation: **gap-minor** (one reproducible clone-operability gap; no content edited).
- Axes: pinned-section fidelity, command operability, pointer/claim accuracy, non-mutation.

## Findings by severity

### Minor — env-diff entry omits the fleet-root argument needed in a scratch clone

`SKILL.md:2018`; `tools/env-diff.py:227` defaults the fleet root to the invoking tool’s grandparent directory. In the required detached clone this is the reader scratch directory, not the fleet.

Command:
```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/env-diff.py --contract /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-21/c2-contract.json --out /fast/scratch/hyaku/tameshi-r57/T57W3Read17/tameshi-f5.json
```
Exit **1**, stdout:
```text
ENVDIFF: classified=0/9 out=/fast/scratch/hyaku/tameshi-r57/T57W3Read17/tameshi-f5.json
```
The emitted receipt records nine `PIN_UNREADABLE` surfaces, beginning with `tameshi-runner`. Adding `--fleet-root /home/vgpnk/Projects/shokunin` to the same pinned command exits **0**, `ENVDIFF: classified=9/9`. This is missing clone guidance, not failed classification logic. Defer any text change to round 58 as directed.

## Executed sweep and bounds

- All seven public selftests exit 0: env-diff 9/9; route-mix 8/8; round21 facade 13/13; coldread selector 12/12; accounting 8/8 plus 16/16; command-binding 44/44; replay 10/10.
- C1 facade at C0b exits 0 with 18 killed, 0 survived, 0 inconclusive; C2 exits 0 with 9/9 classified using retained historical tuples plus live fleet blobs. This is not independent producer authentication.
- The route entry exits 1 with openai-codex 34/71 above 0.40; this is explicitly anticipated by the section’s final correction, not a new defect. Retained round21 routemix receipt remains ok:true.
- Accounting wrong-count exits 1/TOTAL_MISMATCH and source-read command-binding exits 1/ARGV_MISMATCH as explicitly expected; clean frozen accounting/binding entries exit 0.
- Replay --project over retained round24 observations publishes 43 rows, 41 not-declared-live and two declared-live, matching the section. --run at C0b refuses RUNNER_NOT_HELD for mutate-and-run-regression, sources-census and verify-round15; no new bundle is published. Historical registry expectations and missing sibling layout are not a current 43/43 guarantee. This refusal is retained, not presented as a passing replay.
- Every extracted repository pointer resolves; supplemental named replay/extra-case/coldread ledger pointers resolve. Four frozen C1/C2 scripts/populations match 33d03b7 byte-for-byte. Round20 ledger’s 199 entries exactly match the current ledger prefix. Historical round24 after.json records 11 discriminated predicates and the retained sidecar records the 41/2 split.
- The unchanged frozen C2 counter canonically reads FLEET at lines 19/52; no inference of clone hermeticity from green facade/selftest is made. The section’s later corrections explicitly supersede earlier isolation/write-scope claims.
- Coldread monitor run at C0b exits 0 and reports 46/64, consistent with the assignment; this reader report does not itself bind the eighteen reports or claim 64/64.

## Commands and receipts

All commands ran with cwd `/fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone`, `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read17`, `HYAKU_SCRATCH=/fast/scratch/hyaku/tameshi-r57/T57W3Read17`, and `PYTHONDONTWRITEBYTECODE=1`. Literal `REV`, `REPO`, `OBS`, and `DIR` metavariables were substituted with the pinned revision, detached clone, retained round24 observations, and reader scratch outputs. No fixture claims are inferred from an unrun check.

| Command | Exit | Invocation |
|---|---:|---|
| 01 selftest:tools/wave-route-mix.py | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/wave-route-mix.py --selftest` |
| 02 selftest:tools/env-diff.py | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/env-diff.py --selftest` |
| 03 selftest:tools/registry-replay.py | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/registry-replay.py --selftest` |
| 04 selftest:.ufo/evidence/round-21/coldread/measure.py | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-21/coldread/measure.py --selftest` |
| 05 selftest:tools/round21-measure.py | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/round21-measure.py --selftest` |
| 06 selftest:tools/wave-accounting.py | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/wave-accounting.py --selftest` |
| 07 selftest:tools/command-binding.py | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/command-binding.py --selftest` |
| 08 route-entry | 1 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/wave-route-mix.py --spec /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/waves/round-21/spec1.json --json` |
| 09 replay-plan | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/registry-replay.py --plan --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone --json` |
| 10 accounting-red | 1 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/wave-accounting.py --bundle /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-22/wrong-count-bundle.json --expected /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-22/wrong-count-expected.json --json` |
| 11 binding-entry | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/command-binding.py --bundle /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-23/replay/bundle.json --expected /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-23/replay/expected.json --json` |
| 12 accounting-entry | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/wave-accounting.py --bundle /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-22/bundle.json --expected /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-22/expected.json --json` |
| 13 env-diff-entry | 1 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/env-diff.py --contract /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-21/c2-contract.json --out /fast/scratch/hyaku/tameshi-r57/T57W3Read17/tameshi-f5.json` |
| 14 measure-c2 | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/round21-measure.py --claim c2 --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone --rev adf87899c70d616140a81185a8f9acbbdfb30392 --json` |
| 15 coldread-entry | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-21/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone --rev adf87899c70d616140a81185a8f9acbbdfb30392 --explain` |
| 16 measure-c1 | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/round21-measure.py --claim c1 --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone --rev adf87899c70d616140a81185a8f9acbbdfb30392 --json` |
| 17 binding-source-red | 1 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/command-binding.py --bundle /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-23/source-read-bundle.json --expected /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-23/source-read-expected.json --json` |
| 18 replay-project | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/registry-replay.py --project /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-24/replay/observations.json --out /fast/scratch/hyaku/tameshi-r57/T57W3Read17/projection --json` |
| 19 env-diff-explicit-fleet | 0 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/env-diff.py --contract /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-21/c2-contract.json --fleet-root /home/vgpnk/Projects/shokunin --out /fast/scratch/hyaku/tameshi-r57/T57W3Read17/tameshi-f5-explicit-fleet.json` |
| 20 replay-run | 1 | `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/tools/registry-replay.py --run --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone --rev adf87899c70d616140a81185a8f9acbbdfb30392 --requirements /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-23/requirements.json --registry-baseline /fast/scratch/hyaku/tameshi-r57/T57W3Read17/clone/.ufo/evidence/round-23/registry-baseline.json --out /fast/scratch/hyaku/tameshi-r57/T57W3Read17/run-replay --json` |
| 21 section-pointers-frozen-inputs | 0 | `python3 -c <exact audit snippet retained in receipt>` |
| 22 prefix-population-live-read-audit | 0 | `python3 -c <exact audit snippet retained in receipt>` |

Exact argv strings, complete stdout/stderr and exits are in `T57W3Read17.json` and numbered `T57W3Read17-receipts/*.json`. Those receipts also retain both environment-probe outputs and the refused replay rows. The section text is retained in `T57W3Read17-receipts/section.txt`. Metadata receipt `section-pointers-frozen-inputs` loads the prescribed frozen round-18 module and feeds raw `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md` bytes into `m.sectionize`; it prints the section start, end and hash. The initial string-vs-bytes setup error was corrected before the recorded measurement.

## Residual risk / verification gaps

- LSP unavailable: read xd://lsp returned No such tool. Text/source inspection and executable receipts were used instead; no grep result is asserted as semantic caller proof.
- Live fleet Git objects, host tools and operator role routes remain external inputs. Green retained-receipt counters are not fresh execution authentication; the replay refusal is not a passing replay.
- Earlier isolation/write-scope overstatements are explicitly corrected later in this same section; they were not reported again as new defects.
- One section was reread; no full-page 64/64 or wave admission claim is made. L1 must bind the eighteen independent reports.
- No installs, no staged text edits, no lane/fleet Git mutations. Outputs are only the assigned reports/receipts and reader-owned scratch. No runtime-admission, saturation, same-identity rerouting, or resume_continuity_v1 change is in this section’s scope.

## Self-evaluation

Accuracy 4/5 (one environment-dependent clone invocation, fully reproduced); completeness 4/5 (all seven selftests and every documented command form exercised, but no provider-authentication proof claimed); clarity 4/5 (long exact command table retained for auditability); actionability 5/5 (reproducer and successful explicit-fleet discriminator included); conciseness 4/5 (full streams live in JSON receipts). Overall 4.2/5. Improvement: add the clone `--fleet-root` guidance in round 58. No tools installed or updated.
