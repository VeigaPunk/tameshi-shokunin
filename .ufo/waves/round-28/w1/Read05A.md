# Read05A cold read: SKILL.md section at line 1479 — "## Repeated controls and gate registry — round 12"

## Verdict

verified-record. Class: record — the section is an observation/decision table, a
two-row gate/probe registry, a provenance paragraph and a calibration correction,
all stating facts with pointers. It also carries a one-command recipe; that command
was executed verbatim and produced the recorded finding.

Section spans SKILL.md:1479-1516 at b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a
(next ## heading at :1517; no fenced blocks inside). Clone: /tmp/Read05A-ZMoe
(fleet-mirror, detached at the pinned rev; SKILL.md sha256 matches the pinned
value). All nine traced commands have receipts Read05A-1..9; every receipt has
rev=b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a and zero live_lane_reads and zero
external reads.

## What was executed

- Recipe command: `python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read05A-a -- /bin/echo fixture` -> REPEAT_CONTROL: controls_match, exit 0 (Read05A-1). Matches row 1 of the observation table and verdict map "0 clean".
- `repeat-control.py --selftest` -> SELFTEST: PASS (29 cases), exit 0 (Read05A-2); verdicts controls_match/0, controls_mismatch/1, baseline_nonzero/2, command_unavailable/2, snapshot_tampered/2, invalid_usage/64 — consistent with the row's "0 clean; 1 failed; 2 and 64 could-not-evaluate".
- `--snapshot .ufo/evidence/round-12/ControlGate` -> controls_match exit 0; `--snapshot .../mismatch` -> controls_mismatch exit 1 (Read05A-7, -8). Pinned expected.json files exist as listed: expected_id/expected_exit controls_match/0 and controls_mismatch/1 respectively.
- `bash-witness-study.py count` -> exit 0, control exit=0 denominator=16 exercised=14 skipped=2; rows B1-B10 printed, counts killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10 witness_classified=10, unresolved none (Read05A-3). Matches "0 complete classified sample".
- `bash-witness-study.py selftest` -> WITNESS_SELFTEST: 51/51 pass, exit 0 (Read05A-4).
- `bash-witness-study.py check` -> WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=fb91ef76... committed=75ed934d..., exit 1, 96 files covered, no TAMPER line (Read05A-6). `run` refuses before any sweep: CANNOT-EVALUATE (runner-drift ...) exit 2 (Read05A-9). The paragraph's disclosure is exactly right at this revision: the runner pin is stale, count does not read the runner, and the frozen set (declaration, mapping, target, spec, summary; manifest itself not pinned) verifies.

## What was verified as record

- Source line: S004 and S026 rows exist in corpus/SOURCES.md and point at repeated-control-precondition.md; that file exists, reproduces the located excerpts, and states the same bounds (finite match is not determinism; no retry-until-green; unusable baseline -> no verdict).
- Runtime evidence: .ufo/evidence/round-12/verification-final.json records repeat-control-selftest exit 0 with SELFTEST: PASS.
- Non-blind witness claim: declaration.json's disclosure lists recorded aggregate outcomes, a coverage row, a SOURCES row and per-defect KILLED/SURVIVED entries — matches the section's description.
- Stale-pin citation: .ufo/waves/round-27/w1/Read25.md is the report the paragraph cites; its B1/W3 text matches the quoted behavior at round 27 (2227d8338...).
- Calibration correction: `git show 9df9212:SHONEN.md` (the round-12 landing commit) and its parent 18ad5d0 both show box 3 as `[~]` with the scope-bounded qualifier — "carried a scope-bounded [~] at round 12, not [ ]" is accurate. corpus/lessons/round-1-verifier-spotcheck.md states "the box-3 increment is not credited (cold-read covered Appendix A+B only...)" — the exclusion claim holds.
- The three Read25 corrections are landed: write-scope now names /tmp/bash-witness-selftest-private.* (the actual selftest prefix), verdict map says "64 usage only (argparse)", and the frozen-list + stale-pin disclosure is in place. No wrong expectations found.

## Residual / verification gaps

- Kind/Owner cells and the scope sentences cannot be checked from code; both instruments do date to round 12.
- S004/S026 were not re-fetched over the network; only the in-repo rows and knowledge-file excerpts were checked.
- `git show` reads of SHONEN.md at 9df9212, 18ad5d0 and c7986cd ran outside the collector (sibling-revision reads); recorded under external_inputs with blob sha256s.
- Setup plumbing (clone, checkout, file-existence checks, sha256sum) ran outside the collector per fleet precedent and is not listed as a command.

## Tooling

No tool was installed or upgraded. git, python3, sha256sum and the collector's strace were used as found.

```json
{
 "schema": "tameshi-coldread-report-v2",
 "seat": "Read05A",
 "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6",
 "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
 "sections": [
  {
   "start": 1479,
   "heading": "## Repeated controls and gate registry \u2014 round 12",
   "class": "record",
   "verdict": "verified-record",
   "blocking_gaps": [],
   "wrong_expectations": [],
   "minor_gaps": [
    "Kind and Owner registry cells and scope sentences (no seventh gate; registry scope is round-12 instruments) are metadata/scope claims not verifiable from code; both instruments do date to round 12.",
    "External sources S004/S026 were not re-fetched; their registry rows, fetched digests and the knowledge-file located excerpts are consistent internally (recorded unopened-by-network)."
   ],
   "commands_executed": [
    "python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read05A-a -- /bin/echo fixture",
    "python3 tools/repeat-control.py --selftest",
    "python3 tools/bash-witness-study.py count",
    "python3 tools/bash-witness-study.py selftest",
    "python3 -c \"import sys; [print('===== '+p+' =====') or print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/repeated-control-precondition.md .ufo/evidence/round-12/verification-final.json corpus/SOURCES.md corpus/lessons/round-1-verifier-spotcheck.md SHONEN.md .ufo/waves/round-27/w1/Read25.md",
    "python3 tools/bash-witness-study.py check",
    "python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate",
    "python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch",
    "python3 tools/bash-witness-study.py run --timeout 30"
   ],
   "opened": [
    "corpus/knowledge/repeated-control-precondition.md",
    ".ufo/evidence/round-12/verification-final.json",
    "corpus/SOURCES.md",
    "corpus/lessons/round-1-verifier-spotcheck.md",
    "SHONEN.md",
    ".ufo/waves/round-27/w1/Read25.md",
    ".ufo/evidence/round-12/ControlGate/expected.json",
    ".ufo/evidence/round-12/ControlGate/mismatch/expected.json",
    ".ufo/evidence/round-12/BashWitness/declaration.json",
    ".ufo/evidence/round-12/BashWitness/declared.tsv",
    ".ufo/evidence/round-12/BashWitness/manifest.json",
    ".ufo/evidence/round-12/BashWitness/summary.json",
    "tools/repeat-control.py",
    "tools/bash-witness-study.py",
    "tools/trace-inputs.py",
    "tools/mutate-and-run.sh"
   ],
   "inputs": {
    ".ufo/evidence/round-12/BashWitness/bash-surface-census.spec": "d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-run.out": "56ca34615f6c2d84a1305c3435458e6bd0c1732dc11095eb4e8b5291deb1c102",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep.cli.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep.cli.log": "944b82b0727b35eddbd5ed020948c43afadbedd1cce515a9b8cbecf1c81282d8",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/defects.tsv": "0dee2387f756b058cb466577a8893856a4078a7d5946d98af1fbbcb3ecae6342",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B1.out": "4552e10bbd12c7f271f725bf4829c3738e32d4dfe1d7c89881f5f0b7a250eace",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B10.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B2.out": "879b7d8e2cf90d13e4823e02e6130187bb072c77582a55b6bed129244c1675ee",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B3.out": "38737f1f34733faabba3dda448c7e380b90a380157d7a89a757f2d3d660b0868",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B4.out": "cca77bd91adfe019a8ef26e931c98ac21eaf0e13b607faad6b9014bba20e1ff4",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B5.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B6.out": "0691009001b8c808f60cb9a90a9481455d023106a1a14e8eb2197bee32ab37f3",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B7.out": "75ae64703c47896c0e6cc2b1347790c30c511a1f762cda44cd7a38a0af6559f1",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B8.out": "e972da147adbdbe7df0be252e981fdca3b772c972f338abefd8c92c06856beca",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B9.out": "468723a0be9a5bcd716ea6c69fb3bb399b3f9a2a8bbf94267b773abc8f615e75",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/control.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B1.pristine.sh": "1d0e511055a74b11307d827913d264d87f43b93e21fdb679556439d96a4ca3cc",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B10.pristine.sh": "001b757454954cfac740530139d1416dc26e9dc40c2f7cd1c0e51bbbf2354bbd",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B2.pristine.sh": "443ce1fdd35e1a0de2c42ef809d30beef68252ba80972f67c681cc8760a908b3",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B3.pristine.sh": "5efd188121f8e7b9fb100caa27b973cb4603e1b6157fbf13c4b100a86603ba3d",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B4.pristine.sh": "c5f3b2b9d479fbf37aa28216d58f5f97220405cf0a140eef42409e0e97201a72",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B5.pristine.sh": "1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B6.pristine.sh": "627a037aaa27104f286acc9220d176dd45df5fe9e1371fc418962d98af793c54",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B7.pristine.sh": "0c920258f41e6367f0a00b8b51d319372875b1d27b68b8e47a5702a286a31aaa",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B8.pristine.sh": "cce2b52381d0faed40ed7adc8f63f8d9a08d631ed7812357e8aec5ca757b47fa",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B9.pristine.sh": "e1ee079ac2f3db7ed5f57f2b3d33c732f7913880e18dd91d5128f086d63a10ad",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/pristine.pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/results.tsv": "8ec8ea9468ba97b5007e715639b6e2014daf17ac36afd4e6cff55840f5fb3e97",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/spec.copy": "d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741",
    ".ufo/evidence/round-12/BashWitness/declaration-before-run.txt": "d2343ddf7675c09313b02115453095969a285ed7cc3d85abd72b9c1e13b40042",
    ".ufo/evidence/round-12/BashWitness/declaration-hash.txt": "5fcb6d31f50eb4e4f6e09adaa41de20074ef571456dc42e7d930471b91e454ea",
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declare.out": "c9e1c65cf25eeddfea2b078f839516c254ed7d2be59b3d8958dfe474d4994f44",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/manifest.json": "273ffc39308a6c55bdb1c8f7a86bac9f95886ec470773c99b4d1e2db5b25e1cf",
    ".ufo/evidence/round-12/BashWitness/pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/cli.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/cli.log": "bcfce949fee3c64538b50a0b22f41c152732c259fa259fbc662dc398d35420d4",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/defects.tsv": "0dee2387f756b058cb466577a8893856a4078a7d5946d98af1fbbcb3ecae6342",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B1.out": "4552e10bbd12c7f271f725bf4829c3738e32d4dfe1d7c89881f5f0b7a250eace",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B10.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B2.out": "879b7d8e2cf90d13e4823e02e6130187bb072c77582a55b6bed129244c1675ee",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B3.out": "38737f1f34733faabba3dda448c7e380b90a380157d7a89a757f2d3d660b0868",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B4.out": "cca77bd91adfe019a8ef26e931c98ac21eaf0e13b607faad6b9014bba20e1ff4",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B5.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B6.out": "0691009001b8c808f60cb9a90a9481455d023106a1a14e8eb2197bee32ab37f3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B7.out": "e1457e49c311640e1df770783c4ec4ce35028a879bddbfcb2c53a4450a68d3d6",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B8.out": "e972da147adbdbe7df0be252e981fdca3b772c972f338abefd8c92c06856beca",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B9.out": "468723a0be9a5bcd716ea6c69fb3bb399b3f9a2a8bbf94267b773abc8f615e75",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/control.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/manifest.json": "80ae3ea7e5cdf1fa94960b7ed2cc7c7e3bc5e26002d58d7fe22c0a8f57c49d3f",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B1.pristine.sh": "1d0e511055a74b11307d827913d264d87f43b93e21fdb679556439d96a4ca3cc",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B10.pristine.sh": "001b757454954cfac740530139d1416dc26e9dc40c2f7cd1c0e51bbbf2354bbd",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B2.pristine.sh": "443ce1fdd35e1a0de2c42ef809d30beef68252ba80972f67c681cc8760a908b3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B3.pristine.sh": "5efd188121f8e7b9fb100caa27b973cb4603e1b6157fbf13c4b100a86603ba3d",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B4.pristine.sh": "c5f3b2b9d479fbf37aa28216d58f5f97220405cf0a140eef42409e0e97201a72",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B5.pristine.sh": "1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B6.pristine.sh": "627a037aaa27104f286acc9220d176dd45df5fe9e1371fc418962d98af793c54",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B7.pristine.sh": "0c920258f41e6367f0a00b8b51d319372875b1d27b68b8e47a5702a286a31aaa",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B8.pristine.sh": "cce2b52381d0faed40ed7adc8f63f8d9a08d631ed7812357e8aec5ca757b47fa",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B9.pristine.sh": "e1ee079ac2f3db7ed5f57f2b3d33c732f7913880e18dd91d5128f086d63a10ad",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/pristine.pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/results.tsv": "22f229e56dd5b1d65db9aae82a2d7194b4d80a593894b9e28b40235af81e36da",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/spec.copy": "d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-12/BashWitness/selftest.out": "2cd01d5271fc017cdea9e5e62a197952a67fd7e676926ce8f97ddb4590ed461c",
    ".ufo/evidence/round-12/BashWitness/selftest.prefix.out": "51d6cf720fd7ff77f7c399b5c8bbb76149d8ffaeea1d0959f4f1fd529f38878b",
    ".ufo/evidence/round-12/BashWitness/selftest.sha256.txt": "a0aaf77096a5e671810600f31da56e5c0bc416c9a744385bf35525f64666c98c",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    ".ufo/evidence/round-12/BashWitness/sweep/cli.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/BashWitness/sweep/cli.log": "66e9bf5087df815dacfe303e16a73102d82ade1597e439817c556999f818cd76",
    ".ufo/evidence/round-12/BashWitness/sweep/defects.tsv": "0dee2387f756b058cb466577a8893856a4078a7d5946d98af1fbbcb3ecae6342",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B1.out": "4552e10bbd12c7f271f725bf4829c3738e32d4dfe1d7c89881f5f0b7a250eace",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B10.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B2.out": "879b7d8e2cf90d13e4823e02e6130187bb072c77582a55b6bed129244c1675ee",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B3.out": "38737f1f34733faabba3dda448c7e380b90a380157d7a89a757f2d3d660b0868",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B4.out": "cca77bd91adfe019a8ef26e931c98ac21eaf0e13b607faad6b9014bba20e1ff4",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B5.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B6.out": "0691009001b8c808f60cb9a90a9481455d023106a1a14e8eb2197bee32ab37f3",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B7.out": "c76b809c8262c9ba3f715f63e594f5e06a1e4591da8ee8538fb963e1d8736884",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B8.out": "e972da147adbdbe7df0be252e981fdca3b772c972f338abefd8c92c06856beca",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B9.out": "468723a0be9a5bcd716ea6c69fb3bb399b3f9a2a8bbf94267b773abc8f615e75",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/control.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B1.pristine.sh": "1d0e511055a74b11307d827913d264d87f43b93e21fdb679556439d96a4ca3cc",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B10.pristine.sh": "001b757454954cfac740530139d1416dc26e9dc40c2f7cd1c0e51bbbf2354bbd",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B2.pristine.sh": "443ce1fdd35e1a0de2c42ef809d30beef68252ba80972f67c681cc8760a908b3",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B3.pristine.sh": "5efd188121f8e7b9fb100caa27b973cb4603e1b6157fbf13c4b100a86603ba3d",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B4.pristine.sh": "c5f3b2b9d479fbf37aa28216d58f5f97220405cf0a140eef42409e0e97201a72",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B5.pristine.sh": "1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B6.pristine.sh": "627a037aaa27104f286acc9220d176dd45df5fe9e1371fc418962d98af793c54",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B7.pristine.sh": "0c920258f41e6367f0a00b8b51d319372875b1d27b68b8e47a5702a286a31aaa",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B8.pristine.sh": "cce2b52381d0faed40ed7adc8f63f8d9a08d631ed7812357e8aec5ca757b47fa",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B9.pristine.sh": "e1ee079ac2f3db7ed5f57f2b3d33c732f7913880e18dd91d5128f086d63a10ad",
    ".ufo/evidence/round-12/BashWitness/sweep/pristine.pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    ".ufo/evidence/round-12/BashWitness/sweep/results.tsv": "6399660d94162245ef4d5011796e4f52c01ca61767865789049da2c5ee853fb9",
    ".ufo/evidence/round-12/BashWitness/sweep/spec.copy": "d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741",
    ".ufo/evidence/round-12/ControlGate/expected.json": "1b645be04d756c304a1ef5ecc221cf92f82c5f4afbdcfde4b77fe27117684aa1",
    ".ufo/evidence/round-12/ControlGate/mismatch/expected.json": "57f010e99e69a6632869c125229f8bcf0cfdaf866b6dcab9f16ed07ebc8f6771",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stdout": "5223d0557d70eaaa8555c648e04c01d463e4572853f782100b7afb15b3f2b6c8",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stdout": "5223d0557d70eaaa8555c648e04c01d463e4572853f782100b7afb15b3f2b6c8",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stdout": "b52929a30ae03d121fdd499fa74bd6ec58f06ebbc802c53c3b1918e67916b539",
    ".ufo/evidence/round-12/ControlGate/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/run-1.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
    ".ufo/evidence/round-12/ControlGate/run-1.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
    ".ufo/evidence/round-12/ControlGate/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/run-2.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
    ".ufo/evidence/round-12/ControlGate/run-2.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
    ".ufo/evidence/round-12/ControlGate/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/run-3.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
    ".ufo/evidence/round-12/ControlGate/run-3.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
    ".ufo/evidence/round-12/verification-final.json": "9f3d117af3b613d0a00b7d0a623d31136e36f53cb6fcb5626e42cf0c6e022201",
    ".ufo/waves/round-27/w1/Read25.md": "6e6b3cca20d1fa6db9230f2a38a3398a8038b477b98a5edc86783e44f9e3e173",
    "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
    "corpus/SOURCES.md": "a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45",
    "corpus/knowledge/repeated-control-precondition.md": "1339460070d6c2c2d9609915a675b6866f0c42089a39bdb1ecb39b52f1c5fe5b",
    "corpus/lessons/round-1-verifier-spotcheck.md": "f99ef0ae2b3a3e4939c86b9ce5ab1e701733801c1cc1c7063767edf692e0edad",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
    "tools/repeat-control.py": "296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25",
    "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
   },
   "external_inputs": {
    "tameshi-shokunin@9df9212d33dc2dbda133e88f28ad47bb08839a5b:SHONEN.md": "3b1dc52601bc1e5636909764c10f6a2ccfacbb8d9ca7991a0a8f2358a145ac58",
    "tameshi-shokunin@18ad5d050ef4bcd830fe513825baed878f025024:SHONEN.md": "3b1dc52601bc1e5636909764c10f6a2ccfacbb8d9ca7991a0a8f2358a145ac58",
    "tameshi-shokunin@c7986cdf051cbe9d047f02f76f2e1da0b36a84e3:SHONEN.md": "f9bcbe1a24e3ffbcd5de8d7ffb36740d9f8a098e006f2d38bddc4e9a167e3e7b"
   },
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-6.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-7.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-8.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read05A-9.json"
   ]
  }
 ]
}
```

COLDREAD Read05A: verified-record
