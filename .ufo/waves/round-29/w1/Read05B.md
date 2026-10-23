# Read05B cold read — SKILL.md 1517, "Pin disposition and provenance correction — round 13"

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read05B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1517, "heading": "## Pin disposition and provenance correction — round 13", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
    "recipe step 2 hard-codes --root /home/vgpnk/Projects/shokunin (live fleet root); the disposition it emits is a reading of the live sibling worktrees, not of the read_rev clone — expected, since it is explicitly a dated observation, but the printed stdout cannot reproduce a historical receipt",
    "the live run observed counts 6 legs / 1 unchanged / 5 changed / 0 unavailable versus the committed round-13 receipt's 3 unchanged / 3 changed — consistent with later sibling drift and with the 'dated reading' rule, not an error",
    "SOURCES.md S048 (object-neutral precision on S047's item-4 pronoun, added round-13) is not restated in the heading sources line; S047/S041 rows exist as cited",
    "committed .ufo/evidence/round-13/expected.json pins pin_selftest 'SELFTEST: PASS (18/18)' while the current tools/pin-disposition.py emits '19/19' — the expected record is dated round-13 evidence, not a current claim; observed only because the registry's pinned-values column advertises expected.json"
  ],
  "commands_executed": [
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-1.json -- python3 -c 'import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]' corpus/knowledge/incremental-pin-disposition.md corpus/SOURCES.md",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-2.json -- python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin/",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-3.json -- python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-4.json -- python3 -c '<read corpus/lessons/round-12-verifier-spotcheck.md Routed defects item 3 and dump round-13 receipts>'",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-5.json -- python3 -c '<inspect summary.json/declaration.json kind,disclosure,exposure fields>'",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-6.json -- python3 -c '<dump witness-metadata.json original_nested/expected/scope/frozen_bytes_rewritten>'",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-7.json -- python3 -c '<diff witness-metadata-old-null.json vs witness-metadata.json>'",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-8.json -- python3 tools/pin-disposition.py --selftest",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-9.json -- python3 -c '<check rerun-20261020T035435Z/summary.json declaration.kind and expected.json verdicts>'",
    "python3 tools/trace-inputs.py --root $R --out <T>/Read05B-10.json -- python3 tools/witness-metadata.py --selftest"
  ],
  "opened": [
    "corpus/knowledge/incremental-pin-disposition.md",
    "corpus/SOURCES.md",
    "corpus/README.md",
    "corpus/lessons/round-12-verifier-spotcheck.md",
    ".ufo/evidence/round-13/pin-manifest.json",
    ".ufo/evidence/round-13/witness-metadata.json",
    ".ufo/evidence/round-13/witness-metadata-old-null.json",
    ".ufo/evidence/round-13/expected.json",
    ".ufo/evidence/round-13/pin-dispositions.json",
    ".ufo/evidence/round-13/claims.json",
    ".ufo/evidence/round-13/verification-verdict.json",
    ".ufo/evidence/round-13/producer-oracle-repair.json",
    ".ufo/evidence/round-12/BashWitness/summary.json",
    ".ufo/evidence/round-12/BashWitness/declaration.json",
    ".ufo/evidence/round-12/BashWitness/declared.tsv",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
    "tools/pin-disposition.py",
    "tools/witness-metadata.py",
    "tools/bash-witness-study.py",
    "tools/trace-inputs.py"
  ],
  "inputs": {
    "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
    "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
    "corpus/README.md": "91c782f6803a30f26734793f73733e58bb6afc117965e06cbe4c625b88fd3c67",
    "corpus/lessons/round-12-verifier-spotcheck.md": "6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30",
    ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
    ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
    ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    ".ufo/evidence/round-13/pin-dispositions.json": "210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",
    ".ufo/evidence/round-13/claims.json": "ba187b01459ea6a038a29bc038d7945033854c123a20330c7e1992abe5b8be5f",
    ".ufo/evidence/round-13/verification-verdict.json": "1d128a44e0417eb29ca75195bc7f97b8d0ceae246f520710faf67c397ef35a4c",
    ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
    "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
  },
  "external_inputs": {
    "tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
    "tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:.ufo/evidence/round-13/pin-dispositions.json": "210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",
    "tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:.ufo/evidence/round-13/claims.json": "ba187b01459ea6a038a29bc038d7945033854c123a20330c7e1992abe5b8be5f",
    "tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:.ufo/evidence/round-13/verification-verdict.json": "1d128a44e0417eb29ca75195bc7f97b8d0ceae246f520710faf67c397ef35a4c",
    "kagi-shokunin@899c50b42634a3a4ad0b28ab7509786315e2fc2b:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
    "kagi-shokunin@899c50b42634a3a4ad0b28ab7509786315e2fc2b:corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
    "kumitate-shokunin@28e29bbea5f7f138214dd8e7e6d8d448ba925d40:scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
    "kumitate-shokunin@28e29bbea5f7f138214dd8e7e6d8d448ba925d40:scripts/kimi-census.mjs": "0f9c5a4c361316e111d0b2636780da5b8d848ccaa5c41507e8f8357ab6090075",
    "mado-shokunin@8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122:tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
    "tsukuroi-shokunin@58cc2e0bfaa4580d47f6817537c8d5c82dbe9c92:tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e"
  },
  "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-6.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-7.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-8.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-9.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05B-10.json"
  ]}]
}
```

## What I checked

- Read the section (lines 1517–1547, before "### Round-13 gate/probe registry" at 1548) in a detached clone at 9f3084bc60ad56aac01e4556ef4c7653df2f65e5; SKILL.md sha256 matches c46ec02e. Section class: instruction — recipe steps 2 and 3 name runnable commands.
- Ran recipe step 2 verbatim: `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0, six legs, observed `unchanged 1 / changed 5 / unavailable 0`, per-leg `result_reuse=not_established`, `not_compared` list includes mode/exec-bit, suite command, env, deps, timeouts. Matches the table row ("recorded bytes = worktree → unchanged; mode/deps/env/runner unmeasured") and step 2's "observes only hashes and git metadata" / "executes no sibling gate".
- Ran recipe step 3 verbatim: `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` → `metadata_consistent`, exit 0. Read-only mode confirmed by the tool's header docstring and the receipt's input set (all reads, no writes).
- Table row "Frozen summary kind null but top-level declaration explicit → retain bytes, add checked normalized companion": `.ufo/evidence/round-12/BashWitness/summary.json#declaration.kind` is literally null; `declaration.json` top-level `kind` is `"declared-witness mapping (not a blind preregistration)"` with a long `disclosure`. The companion `witness-metadata.json` carries that exact top-level kind byte-equal plus `disclosure_sha256`, `prior_exposure=true`, `blind=false`, `frozen_bytes_rewritten=false`, `original_nested` preserved as null-as-history, and `scope` marking the rerun summary's null as `named-residual-uncorrected` / `sha256-anchored-and-reverified`. Old-null companion differs only in `kind: null`. The `--check` gate accepts the corrected companion; expected.json names the old-null case exit 1 `normalized_kind_null` — verified by the `--selftest` 39/39 which exercises old-null-red, tamper, symlink, missing, wrong-kind and blind-upgrade cases.
- Recipe step 4's "producer's wrong-nesting bug is fixed separately ... its regression selftest asserts the exact top-level exposed kind": `tools/bash-witness-study.py:797` now reads `declaration.get("kind")` (top level), and the selftest block at :1680 asserts `qsummary["declaration"]["kind"] == "declared-witness mapping (not a blind preregistration)"`. `producer-oracle-repair.json` records the single_delta "build_summary kind getter nested declared.kind -> top-level kind" with the literal regression check retained.
- Sources line: S003 (SOURCES.md:14) and S047 (:56) exist; S041 (:50) retained as historical with S047 declared its supersede; S048 (:57) is a further same-URL clarification not named in the heading. `corpus/knowledge/incremental-pin-disposition.md` header lists S003/S041/S047/S048 and the §6 receipt-invariant list, consistent with the section. `corpus/lessons/round-12-verifier-spotcheck.md` Routed defects item 3 exists and is the routed defect the section repairs ("Disclose/repair the already named nested `declaration.kind=null` metadata defect only through new evidence without rewriting the frozen declaration").
- `tools/pin-disposition.py --selftest` → 19/19 PASS, covering unchanged, changed-head, dirty/missing worktree, missing repo, foreign-repo-toplevel, pinned-blob/commit missing, symlink, malformed manifest, detached-head-uses-branch-tip — exercises the "Report `unavailable` with reason" and "never silently borrow the enclosing fleet repo" rows.
- Committed receipt `.ufo/evidence/round-13/pin-dispositions.json` observed_at 2026-10-20T04:59:26Z shows 3 unchanged / 3 changed at baseline; today's live run shows 1/5 — consistent drift in sibling worktrees (e.g. checklist-run.sh still pinned-equal, kimi-census.mjs changed), matching the step-2 caveat to keep stdout with branch-tip commits.
- Cross-checked one sibling leg by hand: `sha256sum /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh` = `7e5ec98b9e1d…` exactly the manifest pin — tool agrees.

Smallest safe correction: none required — the section's commands run as written and the cited facts hold at 9f3084bc60ad56aac01e4556ef4c7653df2f65e5. The four minor_gaps are observational notes, not corrections.

COLDREAD Read05B: executed-ok