# RR7 — residual cold read of input-keyed credit

Axes: **depth + calibration**, specifically verification-fixture craft. This is a cold-read recommendation, not a round judgment or admission.

## Identity and scope

- Read revision: `0ff273448ac4e62893c9b28a4cea7c580712df19`.
- Page: `SKILL.md`, sha256 `de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc`, 1903 lines.
- Assigned bucket: lines **1855–1896**, `## Input-keyed cold-read credit — round 17`.
- Section sha256 after removing trailing newlines: `848d9c594e5e215b1ac28ccf67a35ced111d6b4d9e954a58b256462d37d65482`, matching the assignment. The hash with the range's trailing newlines is `fc11c3a69d570fde148036eb0a400b255a16a1272d1d91e07a82187c860da383`; that difference is not page drift.
- Main fleet-mirror clone, detached at the read revision: `/tmp/tameshi-r17w3-RR7-aWxfZo/fleet/tameshi-shokunin` (`C`). Sibling repositories are symlinks, read-only.
- Historical reproduction, also inside that fleet: `/tmp/tameshi-r17w3-RR7-aWxfZo/fleet/tameshi-history-shokunin` (`H`), detached at `09ee1d099190918ec388019bb79afbb6b93f1ff2`.
- No source changes, lane git/jj writes, tool installations, runtime launches, or sibling writes. Lane writes are this report and its trace receipts only.

## Findings, by severity

**No blocking defect or false outcome found in the assigned text.** The historical correction agrees with the pinned evidence and the reproduced error. The measure selftest exercises the input-keyed decision table and passes **94/94**.

**Non-blocking setup caveat — assembly must be able to find the receipts.** The literal recipe-step-3 command run in the clone rejected the report while the receipts existed only in the required live-lane output directory (receipt 15: `trace-receipt-missing:…/1.json`, child exit 1). The acceptance invocation with `--repo /home/vgpnk/Projects/shokunin/tameshi-shokunin` accepts it (receipt 16: `rejected reports: none`). Keeping execution clone-local also works: copy the receipt files into the same lane-relative paths in `C`, then run assemble against `C` (receipt 26: `rejected reports: none`). Thus this is an output-location prerequisite, not a broken assembler.

**Integration boundary, not a demonstrated score increase.** At the assigned revision, the default committed round-17 ledger is absent. The no-override measurement honestly returns `box3_full_page: false`, score **6**, and `no-ledger` for all 58 buckets (receipt 2). I did not commit a ledger or receipts: that is L1-owned. No claim of an as-committed score 8 is made here.

## Executions and receipts

Receipt prefix: `.ufo/evidence/round-17/coldread/traces/RR7/`. Each number below means `<prefix><number>.json`.

Wrapper used:

`python3 $C/.ufo/evidence/round-17/coldread/trace-inputs.py --root $C --out <absolute-lane-receipt> --cwd <clone-directory> -- <child argv>`

For the runs below, the wrapper returned 0 even when the child failed. **All exits in this table are the receipt's child `exit` value**, not the wrapper's status. Relative child paths below resolve from `C`; historical commands use absolute paths in `H`.

| Receipt | Child command / purpose | Child exit | Observed result |
|---|---|---:|---|
| 1 | `python3 .ufo/evidence/round-17/measure.py --help` | 0 | Lists the revision, ledger, overlay and selftest options; unknown overlay item keys are forbidden. |
| 2 | `python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19` | 0 | `ledger_present: false`, `sections_covered: 0`, `sections_total: 58`, `box3_full_page: false`, `calibration_restraint_score: 6`, `overrides_used: false`, `trace_gate: strict`. |
| 3 | Nested `trace-inputs.py --root C --out /tmp/rr7-nested-inner.json -- /bin/true` | 2 | `strace -y unusable (probe failed)`; no inner receipt. Nested ptrace refusal, not green. |
| 4 | `printenv HOME` | 0 | Printed `/home/vgpnk`; receipt has no input representing that environment dependency. |
| 5 | `stat -c %n C/SKILL.md` | 0 | Printed the path; receipt `inputs` is empty. Stat-only access was not captured as an opened input. |
| 6, 7 | Initial historical recipe steps 2 and 3 in `/tmp/tameshi-r17w3-RR7-09ee` | 2 each | Both report `expected_input_digest_mismatch`. This first historical clone was outside the required fleet layout; these are supporting receipts only, superseded for the execution set by 23–24 below. |
| 8–10 | `measure.py --rev <read-rev> --inputs-overlay /tmp/rr7-ov{1,2,3}.json` | 0 each | `inputs_overlay_merged: 0`, `no-ledger`: without a base ledger these probes were vacuous. No positive-credit claim is based on them. |
| 11 | Same, overlay containing an extra `bogus` key | 2 | Invalid overlay rejected; no ordinary measurement result. |
| 12 | `sed -n '67,70p;73p' corpus/SOURCES.md` | 0 | S058/S059/S060/S064 rows opened and printed; source file recorded in `inputs`. |
| 13 | `sed -n '1,75p' corpus/knowledge/input-keyed-coldread-credit.md` | 0 | Knowledge entry opened and recorded in `inputs`. |
| 14 | `sed -n '41,122p;214,245p' corpus/lessons/round-16-verifier-spotcheck.md` | 0 | Named lesson §2 and §6 opened and recorded in `inputs`. |
| 15 | `assemble.py --reports /tmp/rr7-reports --out /tmp/rr7-ledger.json` | 1 | Report rejected because receipt paths resolved against `C`, where receipts had not yet been copied; 0-entry ledger, explicit refusal to treat it as success. |
| 16 | `assemble.py --reports <this report> --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --out /tmp/rr7-accept.json` | 1 | **`rejected reports: none`**, 1 entry, coverage 1/58. Exit 1 reflects the other 57 buckets being uncovered, not rejection of this seat's report. This validation reads the live report/receipts, so receipt 16 is validation evidence, not part of the clone-local credited execution set. |
| 17 | `measure.py --rev <read-rev> --ledger-file /tmp/rr7-accept.json` | 0 | Bucket 1855: `trace-missing:…/1.json`. Receipts are not committed at the measured revision. This is not a positive-credit result. |
| 18 | Same plus `--inputs-overlay /tmp/rr7-ov2.json` (SOURCES hash set to 64 zeros) | 0 | Overlay merged 1; `input-drift:corpus/SOURCES.md`; not credited. |
| 19 | Same plus `--inputs-overlay /tmp/rr7-ov3.json` (`inputs: {}`) | 0 | Overlay merged 1; `inputs-unrecorded`; not credited. |
| 20 | `measure.py --rev <read-rev> --ledger-file /tmp/rr7-ledger-veto.json` (failing verdict) | 0 | `verdict:wrong-expectation`, `vetoed: true`. |
| 21 | `python3 C/.ufo/evidence/round-17/measure.py --selftest` | 0 | **`MEASURE_SELFTEST: 94/94 pass`**. Includes committed full-ledger/score-8 fixture, input drift/missing/non-blob, command/trace requirements, live-lane reads and duplicate veto order. These are fixtures, not a score for the actual read revision. |
| 22 | `python3 C/.ufo/evidence/round-17/coldread/trace-inputs.py --selftest` | 1 | **`SELFTEST: 4/27`** under the outer tracer. Nested ptrace is refused; this is explicitly not claimed as a standalone tracer-selftest failure or a green run. |
| 23 | `python3 H/tools/evidence-disposition.py --root H --dispositions H/.ufo/evidence/round-14/dispositions-before.json --json` (cwd `H`, outer root `C`) | 2 | `expected_input_digest_mismatch`: observed runner `0673d2e5…`, expected `75ed934d…`. |
| 24 | Same with `dispositions.json` | 2 | Identical mismatch, confirming historical recipe step 3. |
| 25 | Traced `python3 -c` using `git -C C show <pinned-rev>:SKILL.md` to count only the named historical registry bucket | 0 | `28aeef4`: start 1676, **30** logical lines; `09ee1d0`: start 1676, **31** logical lines; neither file ends with a newline. |
| 26 | `python3 C/.ufo/evidence/round-17/coldread/assemble.py --reports /tmp/rr7-reports --repo C --out /tmp/tameshi-r17w3-RR7-aWxfZo/clone-ledger.json` after copying receipts into `C` | 1 | **`rejected reports: none`**, 1 entry, coverage 1/58; no live-lane reads in this receipt. |

The ledger-file/overlay runs 8–11 and 17–20 are demonstrations and use overrides. None supplies a cited actual-revision score. The only no-override actual-revision score above is receipt 2.

## Record verification

1. **Sources and knowledge pointer agree.** `corpus/SOURCES.md` has the cited S058/S059/S060/S064 rows with the same verifying-trace, cache-key and opened-file limitations stated by the page. The knowledge entry exists and describes the same rule. This checks the retained source records; I did not refetch the external websites or PDF.
2. **Round-16 correction agrees.** The pinned round-16 ledger at `09ee1d099190918ec388019bb79afbb6b93f1ff2` has 75 entries. Its round-14 bucket entry (`start: 1563`, seat CR26, `skill_sha256: 97cf436b…`, `sha256: e8720037…`, `commands_executed_count: 4`, verdict `gap-minor`) has no input/trace fields. The historical expected manifest pins runner `75ed934d…`; the actual historical runner is `0673d2e5…`. Recipe steps 2 and 3 both reproduced exit 2 (23–24). The lesson's inference about step 2 is therefore independently exercised here.
3. **Registry count correction agrees exactly: 30 → 31 logical lines.** Receipt 25 resolves the apparent earlier `wc -l` discrepancy: `28aeef4` has 1705 logical lines but only 1704 newline characters. An earlier 29-line slice accidentally omitted the unterminated final line. That arithmetic was discarded; no defect is alleged on that basis.
4. **Receipt-shape claim agrees.** Receipts contain `inputs`, `untracked`, `external`, and `live_lane_reads`. The three named record-file reads are now explicitly traced (12–14), not credited merely for hand opening them.
5. **Decision table agrees with exercised behavior.** The committed full-ledger fixture passes in 21; direct probes show missing committed receipts (17), drift (18), absent inputs (19), and veto (20). The selftest also passes the non-blob, live-lane and duplicate-entry fixtures. Do not confuse the fixture's full coverage with coverage of the actual revision.
6. **Limits remain explicit.** Environment/stat-only probes were invisible as dependencies (4–5). Historical git-object reads and the historical clone's files are not captured in the current-root `inputs` maps (23–25); their pinned hashes are recorded as `external_inputs`, never credited as current-revision inputs. Inherited-descriptor and network blind spots were not independently probed.

## Residual risk and protocol disclosures

- Recipe step 4's commit is intentionally unperformed by this seat. Until L1 commits the ledger and receipts together, committed-revision credit and a score increase remain unverified.
- The first non-raw read exposed boundary context outside 1855–1896; it was not used as bucket evidence. A broad filename-discovery grep also searched forbidden report trees and returned filenames; no other seat's report text was displayed or used. These are cold-read hygiene deviations, disclosed rather than hidden.
- Initial historical clone receipts 6–7 used a non-fleet scratch clone. The reproduction was repeated in the fleet layout as 23–24. The JSON execution set uses 23–24; the old historical input hashes are retained as pinned external evidence.
- Receipt 16's acceptance validation necessarily reads this live report and its receipts; it is excluded from the clone-local execution set rather than passed off as revision-bound evidence. Receipt 26 exercises assembly entirely from `C` after receipt copies are supplied. Final acceptance validation is separate from the credited bucket execution set, avoiding a report/receipt self-reference.
- Actual page-wide calibration and C2 registry claims outside this bucket are not independently judged by this seat. No unrelated runtime, route, saturation, or resume claim was tested.
- No tools were installed or updated.

**Verdict: holds with non-blocking integration/setup and cold-read-hygiene gaps; no wrong expectation found in the assigned bucket.**

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "RR7",
  "skill_sha256": "de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc",
  "read_rev": "0ff273448ac4e62893c9b28a4cea7c580712df19",
  "sections": [
    {
      "start": 1855,
      "heading": "## Input-keyed cold-read credit — round 17",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Step 4's commit is L1-owned; no ledger exists at the read revision, so actual no-override measurement is box3_full_page false, score 6, not a demonstrated score increase.",
        "Assembler needs receipt paths to resolve: bare clone invocation rejected absent receipt copies (15); explicit live --repo accepted (16), and clone-local receipt copies also accepted (26).",
        "Nested tracer selftest was honestly non-green: exit 1, SELFTEST 4/27 (22); nested tracer invocation exits 2 (3).",
        "Cold-read hygiene: non-raw boundary context was exposed and a broad filename grep searched report trees; no other report text was displayed or used. Initial historical runs 6-7 were outside fleet layout and were repeated in fleet as 23-24.",
        "Positive committed coverage is established only in the measure selftest's fixtures, not for this seat's new uncommitted receipts."
      ],
      "commands_executed": [
        "python3 .ufo/evidence/round-17/measure.py --help",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19",
        "python3 C/.ufo/evidence/round-17/coldread/trace-inputs.py --root C --out /tmp/rr7-nested-inner.json -- /bin/true",
        "printenv HOME",
        "stat -c %n C/SKILL.md",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --inputs-overlay /tmp/rr7-ov1.json",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --inputs-overlay /tmp/rr7-ov2.json",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --inputs-overlay /tmp/rr7-ov3.json",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --inputs-overlay /tmp/rr7-ov4.json",
        "sed -n '67,70p;73p' corpus/SOURCES.md",
        "sed -n '1,75p' corpus/knowledge/input-keyed-coldread-credit.md",
        "sed -n '41,122p;214,245p' corpus/lessons/round-16-verifier-spotcheck.md",
        "python3 .ufo/evidence/round-17/coldread/assemble.py --reports /tmp/rr7-reports --out /tmp/rr7-ledger.json",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --ledger-file /tmp/rr7-accept.json",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --ledger-file /tmp/rr7-accept.json --inputs-overlay /tmp/rr7-ov2.json",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --ledger-file /tmp/rr7-accept.json --inputs-overlay /tmp/rr7-ov3.json",
        "python3 .ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --ledger-file /tmp/rr7-ledger-veto.json",
        "python3 C/.ufo/evidence/round-17/measure.py --selftest",
        "python3 C/.ufo/evidence/round-17/coldread/trace-inputs.py --selftest",
        "python3 H/tools/evidence-disposition.py --root H --dispositions H/.ufo/evidence/round-14/dispositions-before.json --json",
        "python3 H/tools/evidence-disposition.py --root H --dispositions H/.ufo/evidence/round-14/dispositions.json --json",
        "python3 -c <pinned git-show historical registry logical-line count; receipt 25 retains exact argv>",
        "python3 C/.ufo/evidence/round-17/coldread/assemble.py --reports /tmp/rr7-reports --repo C --out /tmp/tameshi-r17w3-RR7-aWxfZo/clone-ledger.json"
      ],
      "opened": [
        "corpus/SOURCES.md",
        "corpus/knowledge/input-keyed-coldread-credit.md",
        "corpus/lessons/round-16-verifier-spotcheck.md",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-16/coldread/ledger.json",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/expected.json"
      ],
      "inputs": {
        "corpus/SOURCES.md": "ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5",
        "corpus/knowledge/input-keyed-coldread-credit.md": "1fad5a57c56ea059ebfecedf37edb8256739d94382f89cf302d49d319ab9e57c",
        "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
        ".ufo/evidence/round-17/measure.py": "d25d3d04cb26ca7c20ef7333baaa181c350c6ee912d58f648927fb835b3ce7f3",
        ".ufo/evidence/round-17/coldread/trace-inputs.py": "521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070",
        ".ufo/evidence/round-17/coldread/assemble.py": "8bcce2eafe37e5ca11e1a145e4c6c826071eca55917ddb464a1b6da190f6ccd1"
      },
      "external_inputs": {
        "tameshi@28aeef498cc070c3183271b709bc79d344ff547a:SKILL.md": "97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:SKILL.md": "906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397",
        "tameshi@34907080f6adda2b18ea13eff23822671cc6930e:SKILL.md": "906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-16/coldread/ledger.json": "b84151a35f0cefa0716f3dd200a183dee5badc7be09ba1bac11d61283f70623c",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:.ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:tools/bash-witness-study.py": "49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:tools/evidence-disposition.py": "1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95",
        "tameshi@09ee1d099190918ec388019bb79afbb6b93f1ff2:tools/mutate-and-run.sh": "0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa"
      },
      "traces": [
        ".ufo/evidence/round-17/coldread/traces/RR7/1.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/2.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/3.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/4.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/5.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/8.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/9.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/10.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/11.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/12.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/13.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/14.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/15.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/17.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/18.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/19.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/20.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/21.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/22.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/23.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/24.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/25.json",
        ".ufo/evidence/round-17/coldread/traces/RR7/26.json"
      ]
    }
  ]
}
```
