# Read11B — cold read, SKILL.md:1814 "## Live-tree re-pin and entry-command monitor — round 17"

Verdict: `executed-ok` (class `instruction`; the recipe's steps 1–3 run as written at b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a, and every table claim I could check is true).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read11B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [{"start": 1814, "heading": "## Live-tree re-pin and entry-command monitor — round 17", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": ["Recipe step 3's full `registry-check.py --rev` replay (all 56 registry rows, scratch clone plus run time) was not exercised end to end inside the 6-minute-per-command budget; it was verified on one row via `--only evidence-disposition-round18`, which exercised the scratch-clone path, the detached checkout at the named rev, and the `REGISTRY_CHECK: held=N/M superseded=K` output."],
  "commands_executed": [
    "python3 tools/trace-inputs.py --root $PWD --out $T/Read11B-1.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
    "python3 tools/trace-inputs.py --root $PWD --out $T/Read11B-2.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
    "python3 tools/trace-inputs.py --root $PWD --out $T/Read11B-3.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json",
    "python3 tools/trace-inputs.py --root $PWD --out $T/Read11B-4.json -- python3 tools/registry-check.py --rev b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a --only evidence-disposition-round18",
    "python3 tools/trace-inputs.py --root $PWD --out $T/Read11B-5.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-16-verifier-spotcheck.md",
    "python3 tools/trace-inputs.py --root $PWD --out $T/Read11B-6.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json"
  ],
  "opened": ["SKILL.md", "corpus/lessons/round-16-verifier-spotcheck.md", "corpus/SOURCES.md", ".ufo/evidence/round-16/measure.py", ".ufo/evidence/round-17/dispositions.json", ".ufo/evidence/round-18/dispositions-before.json", ".ufo/evidence/round-18/dispositions.json", "tools/evidence-disposition.py", "tools/registry-check.py", "tools/registry.json", "tools/pin-disposition.py", "tools/bash-witness-study.py", "tools/mutate-and-run.sh", "tools/trace-inputs.py"],
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
    ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
    ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
    ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
    "corpus/SOURCES.md": "a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45",
    "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
    "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
    "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
    "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
    "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
  },
  "external_inputs": {},
  "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read11B-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read11B-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read11B-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read11B-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read11B-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read11B-6.json"
  ]}]}
```

## What I checked

Read from a detached `--no-hardlinks` clone at b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a (SKILL.md sha256 matched the given c46ec02e…). The section is SKILL.md:1814–1845; class `instruction` because its "Recipe" list tells the reader to run specific commands.

- Recipe step 1 (`evidence-disposition.py --dispositions .ufo/evidence/round-18/dispositions-before.json --json`): ran, exit 1, `status: "failed"`, exactly one finding `{"expectation": "producer_before", "id": "expected_contains_missing"}` (counts `failed: 1`). Matches the claim "1 `failed`, the `producer_before` expectation unresolved".
- Same command on `.ufo/evidence/round-17/dispositions.json` (the "round 17's two now exit 2" parenthetical): exit 2, `status: "could_not_evaluate"`. Confirmed for one of the two round-17 files.
- Recipe step 2 (`dispositions.json`, JSON and text modes): exit 0, `status: "clean"`, counts `effective: 11, superseded: 1`; text mode printed one `HISTORICAL <path> rev=<rev> sha256=<sha>` line per waived instrument (three lines: `tools/bash-witness-study.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`, all at rev 4acc607d…). Matches.
- Recipe step 3 (`registry-check.py --rev <rev>`): exercised on one row, `--only evidence-disposition-round18`, at the same rev — it built the scratch clone (siblings symlinked), checked out detached, and printed `ROW evidence-disposition-round18 expect=0 got=0 held` plus `REGISTRY_CHECK: held=1/1 superseded=0`. The `--only` mechanism is documented in `tools/registry-check.py:70`. Full 56-row replay left as a minor gap (time budget).
- Recipe step 4 (`pin-disposition.py` head rows): docstring at `tools/pin-disposition.py:42-51` confirms rows carry `branch` and `head_differs_from_branch`, resolved like `scripts/hyaku/jj-lane.sh` `detect_branch` (:53-65), with raw `HEAD` never substituted for the branch tip.
- Table claims verified in code: `tools/evidence-disposition.py:368-390` sets `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null`, and drops inherited `GIT_*` (`git_environment()`); selftests `v2-historical-replace-ref` (:2910) and `v2-gitdir-env` (:2925) expect exit 0; `historical_input_unneeded` / `historical_input_uncommitted` / `historical_input_forbidden` are real exit-2 ids (:35-38, :606-631, :689); `tools/bash-witness-study.py:335-338` scrubs `GIT_*`; `.ufo/evidence/round-16/measure.py:412-416` still builds `env = dict(os.environ, GIT_…)` without scrubbing — matches "run it only through `registry-check`, which scrubs"; `tools/mutate-and-run.sh:1179-1191` implements the `repo_identity_mismatch` SETUP refusal returning 2 (registry row `mutate-and-run-regression` expects `REGRESSION: PASS`).
- Cited lesson `corpus/lessons/round-16-verifier-spotcheck.md` §3 ("Operability: harmed" — the round-14 live verdict loss) and §6 items 1 (`R16-OP1`) and 6 (`R16-MON1`) match the section's routing claim. SOURCES rows S061/S062/S063 exist at corpus/SOURCES.md:70-72 with the described content (S076 at :85 supersedes S061's paragraph anchor only — section's use of S061 stays accurate).
- No lane file named by the exception list was opened; nothing in this section cites SCORECARD.md, LOG.md, the round-21 ledger, or `corpus/lessons/round-28.md`.

No installs or tool updates were needed (all stdlib python3/git already present).

COLDREAD Read11B: executed-ok
