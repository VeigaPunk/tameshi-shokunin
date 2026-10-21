done — Independent F5 reproduction completed for `tameshi-runner`; no actionable falsification finding. Producer classification, clean success, and every raw tuple were reproduced. This is author-side advisory evidence, not outside admission.

# ProfileTameshiRunner — round-21 FALSIFY

## Findings, ordered by severity

No actionable defect found in the assigned producer observation. All seven independent executions exited 0, emitted 96 individual `PASS` lines and no `FAIL` lines, and ended with:

```text
MUTATE_SELFTEST: 96/96 pass
VERDICT: PASS
```

The full raw stdout/stderr hashes agree across all seven fresh sandboxes and agree exactly with the producer's corresponding tuples. This is successful suite execution, not a uniform usage/setup failure classified as capability.

Axes: **coverage** — all 7/7 frozen profiles, including the independent fresh clean repeat; **freshness** — newly executed full-repository/revision/path pin with freshly materialised bytes and matching receipt/contract hashes. No numeric expertise or global saturation claim is made.

## Pin, source anchors, and freshness

Observed repository HEAD during setup: `790abd2129f153c13b471e381d454186edbde65e` (`master` checkout supplied by the assignment).

Frozen contract `.ufo/evidence/round-21/c2-contract.json` at that revision:

- Lines 9–16 define the seven environments.
- Lines 18–22 define raw tuple comparison and classification precedence.
- Line 25 pins repository `tameshi-shokunin`, revision `08175c62d661fddf052ed10abc91313dec8eb77d`, path `tools/mutate-and-run.sh`, interpreter `bash`.
- Contract SHA-256: `5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd`, identical to producer receipt line 14.

The materialised pin is 97,200 bytes / 1,940 lines:

- Git blob object: `fd1a63a3493b5a2fb2723f2fb1baae9ee7480fba`.
- Blob SHA-256: `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`.
- This computed byte hash matches the producer's declared pin SHA-256 at `.ufo/evidence/round-21/f5/receipt-final-production.json:90–95`.
- Important limitation: contract line 25 itself has **no** `blob_sha256` field. Therefore a separate frozen-contract SHA declaration could not be checked; the full commit/path identifies the blob, and its computed SHA-256 was checked against the producer receipt. This is not reported as a missing revision pin or as a falsification of the measured tuple.

Producer source anchors at `790abd2129f153c13b471e381d454186edbde65e`: receipt lines 83–95 give argv, `invariant`, `normalization: none`, and pin; lines 97–152 give all seven successful tuples; lines 154–155 give `sensitive_to: []` and surface identity. The producer's recorded execution interval is lines 22–25: `2026-10-21T12:25:25.257578+00:00` through `2026-10-21T12:26:07.396003+00:00`.

Independent raw capture files were written between `2026-10-21T12:42:11.569092+00:00` and `2026-10-21T12:42:11.740034+00:00`. These are observed file-write timestamps, **not** an invented execution-start/end interval.

`receipt.json` and `receipt-final-production.json` both have SHA-256 `9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264`. The live instrument checksum was also observed to match receipt line 21 (`e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead`); the instrument was neither invoked nor imported, and its helpers were not read/reused.

## Actual commands and exits

The read-only setup compound command ran with repository cwd `/home/vgpnk/Projects/shokunin/tameshi-shokunin` and exited 0. Its materialisation/check fragments were:

```sh
git cat-file -t 08175c62d661fddf052ed10abc91313dec8eb77d
git log -1 --format='PIN_COMMIT %H %ci %s' 08175c62d661fddf052ed10abc91313dec8eb77d
git rev-parse 08175c62d661fddf052ed10abc91313dec8eb77d:tools/mutate-and-run.sh
git cat-file blob 08175c62d661fddf052ed10abc91313dec8eb77d:tools/mutate-and-run.sh > /tmp/tameshi-r21-ProfileTameshiRunner-s1/target.sh
sha256sum /tmp/tameshi-r21-ProfileTameshiRunner-s1/target.sh
wc -lc /tmp/tameshi-r21-ProfileTameshiRunner-s1/target.sh
git rev-parse HEAD
```

The independent measurement was executed exactly as:

```sh
python3 /tmp/tameshi-r21-ProfileTameshiRunner-s1/f5_independent.py; echo "RUNNER_EXIT=$?"
```

Observed `RUNNER_EXIT=0`; seven child bwrap exits were each 0. The independent implementation uses only Python standard-library modules. It was written separately from the producer and implements the supplied subprocess recipe directly. Its SHA-256 is `123e69ed7d3237f24a0703e29f072ca420974f4a4da635e7af1ea9402731fddf`; an unchanged copy of the executed script is retained with evidence.

Each child executed this command shape, with the concrete `R` named in the table below and the complete argv retained in the JSON:

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind R /tmp/w --unshare-net --die-with-parent --chdir /tmp/w \
  bash /tmp/w/target.sh --selftest
```

Every R contained newly created `home/`, `tmp/`, and the materialised `target.sh`; no sandbox was reused. All seven independent children ran concurrently. Root was read-only, the scratch bind was writable, `/tmp` was private, and networking was unshared. No production gate, fleet mutation, or full battery was run.

Environments:

- `host`: invoking environment with every `GIT_*` entry removed. The captured removed names were `GIT_EDITOR`, `GIT_PAGER`, `GIT_TERMINAL_PROMPT`.
- `clean`: empty environment plus inherited `PATH`, `HOME=/tmp/w/home`, `TMPDIR=/tmp/w/tmp`, `LANG=C`, `LC_ALL=C`, `TZ=UTC`.
- `clean_repeat`: same environment, a different fresh R.
- `tz`: clean with `TZ=Pacific/Chatham`.
- `locale`: clean with `LANG=en_US.UTF-8`, `LC_ALL=en_US.UTF-8`.
- `home`: clean with `HOME=/nonexistent`.
- `columns`: clean with `COLUMNS=20`, `LINES=5`, `TERM=dumb`.

Additional observed commands: `sha256sum receipt.json receipt-final-production.json` exited 0 with identical hashes; `wc -lc .../raw/*.stdout .../raw/*.stderr` exited 0 and reported 98 lines / 4,515 stdout bytes and zero stderr bytes for each profile.

Existing versions, no installations or updates: bubblewrap 0.13.1; GNU bash 5.3.20(1)-release; Node v24.21.0; Python 3.14.8; Linux 7.2.11-arch1-1.

## Measured raw tuples and producer agreement

**No normalization operations were applied.** The common raw tuple for each row is:

```text
exit = 0
stdout_bytes = 4515
stdout_sha256 = a438399e78d0fa6ef53c487d7d500b4b0341fcef3f5f90c9ef0128d8d6e8d55b
stderr_bytes = 0
stderr_sha256 = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

All scratch names below are beneath `/tmp/tameshi-r21-ProfileTameshiRunner-s1/`.

| Profile | Actual fresh R | Exit | Seconds | Individual PASS/FAIL lines | Producer exit/stdout/stderr agreement |
| --- | --- | ---: | ---: | --- | --- |
| host | R-host-5v1tg80q | 0 | 5.481 | 96 / 0 | all agree |
| clean | R-clean-1v2vtr1e | 0 | 5.311 | 96 / 0 | all agree |
| clean_repeat | R-clean_repeat-rjpo5j4q | 0 | 5.311 | 96 / 0 | all agree |
| tz | R-tz-gnzkquj3 | 0 | 5.311 | 96 / 0 | all agree |
| locale | R-locale-97erd4nf | 0 | 5.333 | 96 / 0 | all agree |
| home | R-home-zpcbw9_y | 0 | 5.311 | 96 / 0 | all agree |
| columns | R-columns-cd3zgez0 | 0 | 5.309 | 96 / 0 | all agree |

Result: `clean == clean_repeat`; all other tuples equal clean; classification **`invariant`**, `sensitive_to: []`. All 21 compared tuple components match the producer. There is no classification or clean-exit disagreement.

### Random-path question and capability check

No raw random-path variation was observed for this surface. All full stdout files are identical by SHA-256 and none contains a literal `/tmp/` path. This is consistent with the verified pinned source `tools/mutate-and-run.sh@08175c62d661fddf052ed10abc91313dec8eb77d`:

- Line 1391 creates a randomly named selftest root inside the sandbox's private `/tmp`.
- Lines 1396–1403 increment actual case counters and print fixed PASS/FAIL labels.
- Lines 1906–1910 print the counted summary, print PASS, remove the selftest fixture root, and exit 0 when no case failed.
- Lines 1912–1913 print the random scratch path only on the failed selftest branch.
- Lines 1928 and 1935–1939 route `--selftest` to the real selftest rather than usage output.

The 98-line stdout contains 96 individual PASS records, followed by the 96/96 summary and PASS verdict. The eight embedded-leg checks in that output check embedded specification/table consistency; this reproduction is not a claim that all eight fleet regression suites were replayed.

The pinned fixture helper at lines 262–272 scrubs inherited GIT variables; lines 280–291 create fixture-local history and pin commit identity (`user.name=tameshi`, `user.email=tameshi@selftest`, `commit.gpgsign=false`). Its writes occur in the isolated selftest fixtures, not production repositories.

## Residual risk and verification gaps

1. The contract's tameshi-runner row lacks a separately declared SHA-256. The full revision/path pin and producer-declared SHA were verified; no absent field was invented.
2. Evidence is limited to this pinned runner's real 96-case selftest, these seven environment profiles, and this host. It does not prove universal hermeticity, full fleet regression coverage, other F5 surfaces, canonical rerouting/resume behavior, or saturation. Root remains readable and PATH is inherited as required by the protocol.
3. The invoked process's PATH value was captured by the implementation but not separately serialized; its recipe and actual executed script are retained. This does not affect the observed byte hashes or successful clean-repeat comparison.
4. The `lsp` device is unavailable: attempting `read xd://lsp` returned `No such tool` with no mounted LSP device. Consequently references/definition/diagnostics could not be obtained. The source anchors above use literal read/grep fallback and are not presented as semantic LSP proof.

Preserved non-measurement failure: an initial reviewer receipt-inspection probe used `s['name']` and exited 1 with `KeyError: 'name'`. The contract uses `name`, whereas the receipt uses `surface`; the successful independent comparison explicitly selects `surface == 'tameshi-runner'`. This probe error is not a producer defect and is not relabelled a passed check. The missing LSP device observation is also retained in JSON.

Production tools, contracts, ledgers, corpus, Git index/refs, and routing were not edited. Writes were confined to this item's scratch, report, and item-named evidence.

## Deliverables

- Independent result: `.ufo/waves/round-21/w2/surfaces/tameshi-runner.json`.
- Executed independent implementation and all seven raw stdout/stderr pairs: `.ufo/waves/round-21/w2/surfaces/tameshi-runner-evidence/`.
- Scratch originals: `/tmp/tameshi-r21-ProfileTameshiRunner-s1/`.

Report: .ufo/waves/round-21/w2/ProfileTameshiRunner.md
