# Read33: cold read of "Round-17 gate/probe registry — re-pin and monitor"

Verdict: gap-minor (class record). Section SKILL.md:1846-1854 (next heading at 1855), read at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. Page sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 (receipt read33-21). Nothing in the section is blocking. Four minor gaps are listed below.

## Findings, most important first

No blocking gap. No wrong expectation.

1. **registry-check --selftest is load-sensitive (minor).** Trace read33-5 exited 1 with "SELFTEST: FAIL (1 of 51 cases: timeout-kills-setpgid-pipe)". The case measured elapsed 3.700 s against the 3.5 s bound in tools/registry-check.py:1163-1220 (the case call is at line 1218). That run shared its batch with seven other traced jobs, including the 300-second `--rev` grading (job bg_6918). The same selftest run alone (read33-16) exited 0 with "SELFTEST: PASS (51 cases)" and elapsed 1.535 s. In both runs survivor=False and marker=False, so the failure was timing, not a surviving process. The section gives no expected exit for `--selftest` and no load caveat. Smallest correction: say in the registry-check row that `--selftest` is timing-bounded and belongs on an idle host.

2. **The full `--rev` grading is not receipted (minor).** The registry has 56 rows: 49 active and 7 superseded. The tag `baseline` selects 25 of them (read33-12). The unfiltered `registry-check.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 --json` run was killed at 360 s under load (job bg_7210) and again solo at 360 s (job bg_7284). A `--tag baseline` run printed "REGISTRY_CHECK: held=23/23 superseded=2" before its 300-second kill (job bg_7103). That output has no receipt, so I do not credit it. Under the six-minute rule this command is skipped. Its exit map is covered by four subset runs (read33-17 to read33-20) and by the selftest receipts.

3. **evidence-disposition --selftest was not run (minor).** The round-18 registry table (SKILL.md:1925 onward) says this selftest now needs `jj` on PATH. My bounds forbid any jj command, so the gate's exit 1 (failed expectations) is not observed. Exits 0, 2 and 64 are observed (read33-1, read33-2, read33-3).

4. **A superseded-only run exits 0 (minor).** `registry-check.py --rev REV --only evidence-disposition-round17 --json` exits 0 with "held=0/0 superseded=1", while the row itself reports got=2 (read33-17). The docstring (tools/registry-check.py:30-34) says superseded rows still run and are excluded from N/M. So the exit is consistent with the tool, but the section does not say a superseded-only run exits 0. Smallest correction: one clause in the registry-check row.

## Evidence

All commands ran from the detached clone at 2227d83 under the trace collector. `--only` and `--tag` are documented in the tool docstring (tools/registry-check.py:70-71), not in the section's command column.

| Command (abbreviated) | Exit | Observed | Receipt |
|---|---|---|---|
| evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json | 0 | status clean; effective 11, expected 12, failed 0, findings 0, superseded 1 | read33-1 |
| evidence-disposition.py ... --dispositions .ufo/evidence/round-17/dispositions.json --json | 2 | could_not_evaluate, expected_input_digest_mismatch on tools/bash-witness-study.py. The section's "round-17 manifest now exits 2" holds. | read33-2 |
| evidence-disposition.py (no arguments) | 64 | usage text, which lists --selftest | read33-3 |
| evidence-disposition.py --selftest | not run | needs jj on PATH (finding 3) | none |
| registry-check.py --selftest, under load | 1 | one case failed (finding 1) | read33-5 |
| registry-check.py --selftest, alone | 0 | 51 of 51 cases pass, including one-differs-exit 1, all-held 0, rev-unknown 2, usage-unknown-flag 64 | read33-16 |
| registry-check.py --rev REV --tag fleet-live --json | 0 | held 1/1 (pin-disposition-read) | read33-19 |
| registry-check.py --rev REV --only evidence-disposition-round18 --json | 0 | held 1/1 | read33-18 |
| registry-check.py --rev REV --only mutate-and-run-selftest --json | 0 | held 1/1, 6.6 s | read33-20 |
| registry-check.py --rev REV --only evidence-disposition-round17 --json | 0 | held 0/0, superseded 1, row got=2 (finding 4) | read33-17 |
| bash tools/mutate-and-run.sh --selftest | 0 | MUTATE_SELFTEST 97/97; VERDICT PASS. Includes "--regression refuses --target (exit 64)", "regression pin mismatch is SETUP (exit 2)" and "repo-identity guard ... (exit 2)". | read33-6 |
| bash tools/mutate-and-run.sh --regression | 0 | REGRESSION: PASS (cases=9 passed=9); 231.6 s, inside the bound | read33-10 |
| pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin | 0 | status ok; 6 legs: 1 unchanged, 5 changed, 0 unavailable | read33-7 |
| pin-disposition.py --selftest | 0 | SELFTEST: PASS (19/19) | read33-8 |

Exit codes the section states that I saw only as assertions inside the tools' own selftests, not as live runs: mutate-and-run regression 1 (FAIL) and 2 (SETUP), registry-check 2 (invalid registry), and pin-disposition 2 (invalid input). The selftests assert these, and I did not re-derive them.

Counts from the tag histogram (read33-12): 56 rows; the new-r17 tag covers 5 rows, including registry-check-selftest.

## Smallest safe correction (suggested, not applied)

- registry-check row: add that `--selftest` is timing-bounded (a 3.5 s bound on a case that runs in about 1.5 s), so run it on an idle host; and add that a superseded row's red outcome does not change the exit, so a superseded-only run exits 0 with held 0/0.
- evidence-disposition row: add that `--selftest` needs `jj` on PATH (see the round-18 row).

## Residual risk and verification gaps

- Row subprocesses of `--rev` run inside a private /tmp clone, outside the collector root. Their file reads do not appear in receipts read33-17 to read33-20. Those receipts show only registry-check's own opens, plus the live sibling reads in read33-19 (external).
- `mutate-and-run.sh --regression` reads sibling git objects through `.git`, which the collector does not record (read33-10: external empty, dropped_home_count 5529). I recorded the nine pinned blob hashes the tool printed as external_inputs.
- pin-disposition reads live sibling worktrees by design (tag fleet-live). At observation time 5 of 6 legs read changed, which the round-13 row allows.
- Untraced helper commands: the clone build, `command -v strace`, `ls`, `git rev-parse`, and early `sha256sum` checks. Each hash I report also has a traced receipt (read33-13, read33-15, read33-21). These helpers are not in commands_executed.
- Killed runs with no receipt: job bg_6918 (`--rev`, first batch, 300 s), bg_7103 (`--tag baseline`, 300 s), bg_7210 (full `--rev`, 360 s), bg_7284 (full `--rev` solo, 360 s). None is credited or listed in commands_executed.
- I opened the live-lane wave report .ufo/waves/round-27/w1/Read31.md outside any trace, only to match the JSON shape. It is not an input and is not credited.
- No tool was installed or upgraded. No jj command was run anywhere.

## Report

```json
{"schema": "tameshi-coldread-report-v2", "seat": "read33", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [{"start": 1846, "heading": "### Round-17 gate/probe registry \u2014 re-pin and monitor", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [
      "registry-check --selftest is load-sensitive: trace read33-5 (same batch as seven other traced jobs, including the 300 s --rev grading) exited 1 with one failed case, timeout-kills-setpgid-pipe, at elapsed 3.700 s against the 3.5 s bound (tools/registry-check.py:1163-1220). The same selftest run alone (read33-16) exited 0 with SELFTEST: PASS (51 cases) at elapsed 1.535 s. The section gives no expected exit for --selftest and no load caveat.",
      "The unfiltered 56-row registry-check --rev REV --json grading exceeded the 6-minute bound (killed at 360 s under load, and again solo at 360 s). It has no receipt, so it is not credited and is not listed in commands_executed. The row exit map is covered by subset runs read33-17 to read33-20 and the selftest receipts.",
      "evidence-disposition --selftest was not run: the round-18 registry table (SKILL.md:1925 onward) says it needs jj on PATH, and this seat may not run any jj command. Exit 1 (failed expectations) is therefore not observed; exits 0, 2 and 64 are observed (read33-1, read33-2, read33-3).",
      "A superseded-only run exits 0: registry-check --rev REV --only evidence-disposition-round17 --json returns exit 0 with held=0/0 superseded=1 while the row itself reports got=2 (read33-17). The docstring (tools/registry-check.py:30-34) excludes superseded rows from N/M, so this is consistent with the tool, but the section does not state it."
    ],
    "commands_executed": [
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json",
      "python3 tools/evidence-disposition.py",
      "python3 tools/registry-check.py --selftest",
      "python3 tools/registry-check.py --selftest",
      "python3 tools/registry-check.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 --only evidence-disposition-round17 --json",
      "python3 tools/registry-check.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 --only evidence-disposition-round18 --json",
      "python3 tools/registry-check.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 --tag fleet-live --json",
      "python3 tools/registry-check.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 --only mutate-and-run-selftest --json",
      "bash tools/mutate-and-run.sh --selftest",
      "bash tools/mutate-and-run.sh --regression",
      "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin",
      "python3 tools/pin-disposition.py --selftest",
      "sha256sum SKILL.md",
      "sha256sum tools/*",
      "bash -c find tools/vendor -type f -exec sha256sum {} +",
      "python3 -c import json,collections;r=json.load(open('tools/registry.json'));rows=r['rows'];print('rows',len(rows));print('tags',dict(collections.Counter(t for x in rows for t in x.get('tags',[]))));print('status',dict(collections.Counter(x.get('status') for x in rows)));print('names',[x['name'] for x in rows])",
      "python3 -c import json;r=json.load(open('tools/registry.json'));[print(x['name'],'|',x['status'],'|',x.get('timeout_s'),'|',x.get('tags'),'|',' '.join(x['argv'])) for x in r['rows'] if 'new-r17' in x.get('tags',[]) or x['name'].startswith('evidence-disposition') or x['name'].startswith('mutate-and-run') or x['name'].startswith('pin-disposition') or x.get('status')=='superseded']"
    ],
    "opened": [
      ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-12/BashWitness/summary.json",
      ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/producer-before.py", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-13/producer-oracle.py", ".ufo/evidence/round-13/verification.json", ".ufo/evidence/round-13/witness-metadata-old-null.json", ".ufo/evidence/round-13/witness-metadata.json",
      ".ufo/evidence/round-14/dispositions.json", ".ufo/evidence/round-17/dispositions.json", ".ufo/evidence/round-18/dispositions.json",
      "tools/bash-witness-study.py", "tools/command-binding.py", "tools/context-capture.py", "tools/env-diff.py", "tools/evidence-disposition.py", "tools/mte-interop.py", "tools/mutate-and-run.sh", "tools/pin-disposition.py", "tools/receipt-measure.py", "tools/receipt-window.py", "tools/registry-check.py", "tools/registry-replay.py", "tools/registry.json", "tools/repeat-control.py", "tools/round21-measure.py", "tools/trace-inputs.py", "tools/vendor/mutation-testing-metrics-3.9.0.tgz", "tools/vendor/mutation-testing-report-schema-3.9.0.tgz", "tools/wave-accounting.py", "tools/wave-route-mix.py", "tools/witness-metadata.py"
    ],
    "inputs": {
      ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
      ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
      ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
      ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
      ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
      ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
      ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
      ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
      ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
      ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
      ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
      ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
      ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
      ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
      ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
      "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
      "tools/command-binding.py": "9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d",
      "tools/context-capture.py": "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726",
      "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
      "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
      "tools/mte-interop.py": "193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4",
      "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
      "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
      "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa",
      "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
      "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
      "tools/registry-replay.py": "9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714",
      "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
      "tools/repeat-control.py": "296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25",
      "tools/round21-measure.py": "eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d",
      "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
      "tools/vendor/mutation-testing-metrics-3.9.0.tgz": "ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548",
      "tools/vendor/mutation-testing-report-schema-3.9.0.tgz": "adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280",
      "tools/wave-accounting.py": "96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e",
      "tools/wave-route-mix.py": "1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782",
      "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
    },
    "external_inputs": {
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
      "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
      "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "7818970b80d4951b8edf15dcc8c5a16efe57f457f956a5ce019f049068538156",
      "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e",
      "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
      "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
      "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
      "kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs": "f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9",
      "kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs": "6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f",
      "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"
    },
    "traces": [
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-3.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-5.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-6.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-7.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-8.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-10.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-12.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-13.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-14.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-15.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-16.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-17.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-18.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-19.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-20.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read33-21.json"
    ]}]}
```

## Plain-English note

I cloned tameshi at 2227d83, detached, and confirmed the page hash. I read lines 1846-1854, the four-row table. I classed it as a record, because it names tools, commands and exit codes. I ran every command the table names except the evidence-disposition selftest, which needs jj. Every stated exit code was seen on a real run or in the tool's own selftest, except evidence-disposition exit 1. The full 56-row `--rev` grading exceeded the six-minute bound, so I ran four subsets and the selftests instead. Every receipt matches the read revision, and none records a live-lane read. The four inputs the monitor names (evidence-disposition.py, mutate-and-run.sh, registry-check.py and registry.json) were opened under the collector and hashed at this revision.

COLDREAD Read33: gap-minor
