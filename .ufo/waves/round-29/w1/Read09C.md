# Cold-read report — Read09C

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read09C", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1814, "heading": "## Live-tree re-pin and entry-command monitor \u2014 round 17", "class": "instruction", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["recipe step 3 (python3 tools/registry-check.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5) did not finish inside the 6-minute per-command bound: it was still cloning-and-replaying the 56-row registry when killed at 300 s, so the trailing `REGISTRY_CHECK: held=N/M superseded=K` line was verified only from the tool's printed contract (tools/registry-check.py:48-52 output shape, :52 exit map, :30-37 run semantics) rather than from a completed run"],
    "commands_executed": [
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json",
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json",
      "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-16-verifier-spotcheck.md corpus/SOURCES.md"
    ],
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
      ".ufo/evidence/round-17/dispositions-before.json",
      ".ufo/evidence/round-17/dispositions.json",
      ".ufo/evidence/round-18/dispositions-before.json",
      ".ufo/evidence/round-18/dispositions.json",
      "corpus/SOURCES.md",
      "corpus/lessons/round-16-verifier-spotcheck.md",
      "tools/bash-witness-study.py",
      "tools/evidence-disposition.py",
      "tools/mutate-and-run.sh",
      "tools/pin-disposition.py",
      "tools/registry-check.py",
      "tools/registry.json",
      "tools/witness-metadata.py"
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
      ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
      ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
      ".ufo/evidence/round-16/measure.py": "03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",
      ".ufo/evidence/round-17/dispositions-before.json": "79f0b397b727152b260df90e3ba9aa886d20eb7b5e5a43f6c3d03c7d3ee32354",
      ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
      ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
      ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
      "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
      "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
      "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
      "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
      "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
      "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
      "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
      "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
      "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
    },
    "external_inputs": {},
    "traces": [
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09C-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09C-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09C-3.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09C-4.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09C-5.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09C-7.json"
    ]}]}
```

Checked SKILL.md lines 1814-1845 (`## Live-tree re-pin and entry-command monitor — round 17`, ending just before `### Round-17 gate/probe registry` at :1846) in a detached clone at 9f3084bc (sha256 c46ec02e… matches the pin).

What I verified by executing, under `tools/trace-inputs.py` with receipts Read09C-1/2/3/4/5/7 (all `rev=9f3084bc…`):

- Recipe step 1: `--dispositions .ufo/evidence/round-18/dispositions-before.json --json` → `"status": "failed"`, `"counts.failed": 1`, the one finding is `"expectation": "producer_before"` (`expected_contains_missing`); child exit 1. Matches the recipe.
- Recipe step 2: `dispositions.json --json` → `"status": "clean"`, `"counts": {"failed": 0, "effective": 11, "superseded": 1}`; child exit 0. Matches the recipe exactly.
- Text mode of the same command printed `EVIDENCE_DISPOSITION: clean` plus the ROW lines and exactly one `HISTORICAL <path> rev=<40-hex> sha256=<sha>` per waived instrument (3: bash-witness-study.py, mutate-and-run.sh, pin-disposition.py, all at rev 4acc607d…). Matches.
- The parenthetical "round 17's two now exit 2": both `.ufo/evidence/round-17/dispositions-before.json` and `dispositions.json` exit 2 `expected_input_digest_mismatch` (observed 60575e62… vs expected 49e9e5e2… on tools/bash-witness-study.py). Matches.
- Sources line: `corpus/lessons/round-16-verifier-spotcheck.md` carries the operability analysis in §3 and the routed list in §6 including R16-OP1 and R16-MON1. SOURCES.md rows S061 (jj colocated → Git HEAD detached), S062 (`--show-toplevel`), S063 (upward repo discovery + GIT_* env) all exist and carry the scopes the section names; S076's later anchor correction to S061 is consistent with the section text.

What I verified by reading code/registry at the same rev:

- Table claim "the tool sets `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null` and scrubs inherited `GIT_*` (`tools/evidence-disposition.py:368-390`)": `GIT_ENV_OVERRIDES` sits at :371-375 and `git_environment()` strips every `GIT_*` at :387-390 — inside the cited span. Both named selftests exist and expect exit 0 (`v2-historical-replace-ref` :2910, `v2-gitdir-env` :2925). Graft case is disclosed as code-reading-only, which the code honors (graft file forced to /dev/null).
- Waiver-rev guards: exit-2 paths for non-commit ids (G3, :529-544), non-ancestor (`merge-base --is-ancestor`), dangling (`v2-historical-dangling` selftest), and shallow repo (:440-444) all present; `historical_input_unneeded` (:606), `historical_input_uncommitted` (:613-631), `historical_input_forbidden` (:689) all exist with exit 2 semantics.
- Round-18 anchor is `refs/heads/<lane.branch>` not HEAD (:48-57, :462-525, `lane.branch` config + symbolic-ref resolution). `tools/pin-disposition.py` head rows carry `branch` and `head_differs_from_branch` per its own contract doc (:42-51).
- `tools/registry-check.py` contract prints `ROW … held|differs`, `ROW … superseded …`, `REGISTRY_CHECK: held=<N>/<M> superseded=<K>` (:48-50); exits 0/1/2/64 as stated; every active and superseded row runs (:30-31); `superseded_by` must name an active row (:277-297). tools/registry.json has 49 active + 7 superseded rows; all 7 superseded rows carry `superseded_by` naming active rows. The tool clones under /tmp and symlinks `*-shokunin` siblings (:61-64, :773-782) — matching the recipe's description.
- `tools/mutate-and-run.sh` regression leg emits `SETUP (repo_identity_mismatch: …)` (:1189) and selftest asserts the refusal (:1856-1866). `tools/bash-witness-study.py` scrubs `GIT_*` (:336-338). `.ufo/evidence/round-16/measure.py` contains no `GIT_*` environment scrub — consistent with the section's warning to run it only through `registry-check`.

One additional run, `python3 tools/registry-check.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5` under the collector, exceeded the 6-minute bound and was killed at 300 s (receipt Read09C-6 never materialized; that argv is therefore omitted from `commands_executed`, and the unverified tail is listed as a minor gap rather than a defect — the recipe itself warns rows are replayed in a scratch clone, and 56 rows do not fit the cold-read time box).

No wrong expectations found; every stated outcome I could reach was byte-exact. Verdict `gap-minor` solely for the step-3 completion line proven by code contract rather than live run.

COLDREAD Read09C: gap-minor
