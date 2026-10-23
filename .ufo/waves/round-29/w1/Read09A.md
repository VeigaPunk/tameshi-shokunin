# Read09A — cold read: `## Live-tree re-pin and entry-command monitor — round 17` (SKILL.md:1814)

Seat `TameshiR29.Read09A` (leaf; no subagents). Lane SKILL.md sha256 at read_rev
`9f3084bc60ad56aac01e4556ef4c7653df2f65e5`: `c46ec02e…36d6` (matches assignment).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read09A", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1814, "heading": "## Live-tree re-pin and entry-command monitor — round 17", "class": "instruction", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["recipe step 3: the full `python3 tools/registry-check.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5` replay of all 56 registry rows could not finish inside the 6-minute bound (aborted by `timeout` at ~300s before the final REGISTRY_CHECK line, scratch clone work left in /tmp and killed), so the step-3 terminal-line claim `REGISTRY_CHECK: held=N/M superseded=K` was verified only on the row-subset run `python3 tools/registry-check.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --tag new-r17`, which ended `REGISTRY_CHECK: held=3/3 superseded=2` exit 0"],
    "commands_executed": [
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json",
      "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin",
      "python3 tools/registry-check.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --tag new-r17",
      "bash -c 'for f in \"$@\"; do echo \"=== $f\"; head -c 200000 \"$f\"; done' _ corpus/lessons/round-16-verifier-spotcheck.md .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-16/measure.py tools/mutate-and-run.sh tools/registry.json",
      "bash -c 'for f in \"$@\"; do echo \"=== $f\"; head -c 200000 \"$f\"; done' _ tools/registry-check.py tools/evidence-disposition.py tools/trace-inputs.py .ufo/evidence/round-18/dispositions.json .ufo/evidence/round-18/dispositions-before.json",
      "bash -c 'for f in \"$@\"; do echo \"=== $f\"; head -c 200000 \"$f\"; done' _ corpus/SOURCES.md corpus/QUALITY.md corpus/README.md corpus/knowledge/input-keyed-coldread-credit.md .ufo/evidence/round-17/measure.py .ufo/evidence/round-17/coldread/assemble.py"],
    "opened": [
      ".ufo/evidence/round-12/BashWitness/declaration.json",
      ".ufo/evidence/round-12/BashWitness/declared.tsv",
      ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
      ".ufo/evidence/round-12/BashWitness/summary.json",
      ".ufo/evidence/round-13/expected.json",
      ".ufo/evidence/round-13/pin-manifest.json",
      ".ufo/evidence/round-13/producer-before.py",
      ".ufo/evidence/round-13/producer-oracle-repair.json",
      ".ufo/evidence/round-13/producer-oracle.py",
      ".ufo/evidence/round-13/verification.json",
      ".ufo/evidence/round-13/witness-metadata-old-null.json",
      ".ufo/evidence/round-13/witness-metadata.json",
      ".ufo/evidence/round-14/dispositions-before.json",
      ".ufo/evidence/round-14/dispositions.json",
      ".ufo/evidence/round-16/measure.py",
      ".ufo/evidence/round-17/coldread/assemble.py",
      ".ufo/evidence/round-17/measure.py",
      ".ufo/evidence/round-18/dispositions-before.json",
      ".ufo/evidence/round-18/dispositions.json",
      "corpus/QUALITY.md",
      "corpus/README.md",
      "corpus/SOURCES.md",
      "corpus/knowledge/input-keyed-coldread-credit.md",
      "corpus/lessons/round-16-verifier-spotcheck.md",
      "tools/bash-witness-study.py",
      "tools/evidence-disposition.py",
      "tools/mutate-and-run.sh",
      "tools/pin-disposition.py",
      "tools/registry-check.py",
      "tools/registry.json",
      "tools/trace-inputs.py",
      "tools/witness-metadata.py"],
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
      ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
      ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
      ".ufo/evidence/round-16/measure.py": "03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",
      ".ufo/evidence/round-17/coldread/assemble.py": "8bcce2eafe37e5ca11e1a145e4c6c826071eca55917ddb464a1b6da190f6ccd1",
      ".ufo/evidence/round-17/measure.py": "d25d3d04cb26ca7c20ef7333baaa181c350c6ee912d58f648927fb835b3ce7f3",
      ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
      ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
      "corpus/QUALITY.md": "069ef729b7738927585f487afa3c26b4912b9d568cb9f0c69b00c3f172538e07",
      "corpus/README.md": "91c782f6803a30f26734793f73733e58bb6afc117965e06cbe4c625b88fd3c67",
      "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
      "corpus/knowledge/input-keyed-coldread-credit.md": "0c45dccb4dfa78cdfd2dfddc59132d1e636ed0d548abcb9528d1b1aa21fd0636",
      "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
      "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
      "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
      "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
      "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
      "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
      "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
      "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
      "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"},
    "external_inputs": {
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
      "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
      "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "0f9c5a4c361316e111d0b2636780da5b8d848ccaa5c41507e8f8357ab6090075",
      "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e"},
    "traces": [
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09A-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09A-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09A-3.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09A-4.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09A-5.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09A-6.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09A-7.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09A-8.json"]}]}
```

## What I checked

Section bounds: SKILL.md:1814–1845 (ends before `### Round-17 gate/probe registry — re-pin and monitor` at line 1846; the next `##` heading is at 1847). Class `instruction`: its recipe tells the reader to run four commands with stated outcomes.

Clone: `git clone --no-hardlinks` of the lane to `/tmp/Read09A-3WW0/fleet/tameshi-shokunin`, detached at `9f3084bc…` (SKILL.md sha256 verified `c46ec02e…`). All runs under `tools/trace-inputs.py --root $R` with receipts Read09A-1 through Read09A-8.

Recipe step 1 ran verbatim: exit 1, `status: failed`, findings carry `"expectation": "producer_before"` — exactly as stated (also confirms the parenthetical: the superseded round-17 `before` manifest now exits 2 in the registry, seen in step 3's rows). Step 2 ran verbatim: exit 0 `clean`, `"effective": 11`, `"superseded": 1`. The text-mode claim ("one `HISTORICAL <path> rev=<rev> sha256=<sha>` line per waived instrument") was verified with a separate non-`--json` run: exactly three HISTORICAL lines for the three `historical_inputs` waivers. Step 3: see minor gap — full 56-row replay exceeds the 6-minute bound; a tag-subset run (`--tag new-r17`, 5 rows incl. 2 superseded rows that still ran) ended `REGISTRY_CHECK: held=3/3 superseded=2`, matching the claimed terminal-line shape and confirming "a row leaves `active` only as `superseded` with `superseded_by`, and still runs" (superseded `evidence-disposition-round17-before` graded expect=1 got=2, `trace-inputs-round17-selftest` graded expect=0 got=1 — both run despite `superseded`). Step 4: the literal probe ran clean (exit 0, 6 legs); every leg reports `head.branch`/`head_differs_from_branch` resolved via `refs/heads/<branch>` — the six external sibling paths it opened are recorded in `external_inputs`.

Table-row claims verified against code: `historical_input_unneeded`/`historical_input_forbidden`/`historical_input_uncommitted` exist at evidence-disposition.py:606/689/613-631; `GIT_ENV_OVERRIDES` at lines 368-390 scrubs `GIT_*` and sets `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null` as claimed (selftests `v2-historical-replace-ref`, `v2-gitdir-env` at lines 2910/2925 both expect exit 0); `repo_identity_mismatch` SETUP guard is in mutate-and-run.sh:1189/1856; `.ufo/evidence/round-16/measure.py` indeed does not scrub `GIT_*` (line 412 passes `os.environ` through unmodified); `registry-check.py` prints `differs` per row (lines 48, 903) and exits 1 on any differs (docstring line 52).

Disclosure: before tracing, I ran the identical `--rev --tag new-r17` registry-check argv once *outside* the collector with `--json` as a smoke test (~23 s, held=3/3 superseded=2); it is deliberately not in `commands_executed` because it has no receipt — it adds no evidence beyond the traced run.

COLDREAD Read09A: gap-minor
