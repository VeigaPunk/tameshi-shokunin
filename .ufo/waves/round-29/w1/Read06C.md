# Cold read — SKILL.md section `### Round-13 gate/probe registry` (lines 1548-1562) at 9f3084b

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read06C", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1548, "heading": "### Round-13 gate/probe registry", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["Pinned .ufo/evidence/round-13/expected.json records pin_selftest 'SELFTEST: PASS (18/18)' from the round-13 baseline (pinned tool sha 29725397...); the current pinned tool (sha 331529ea..., header 'r17') emits 'SELFTEST: PASS (19/19)'. Exit map and pass verdict unchanged; the registry row pins the exit map, not the historical count."],
    "commands_executed": ["python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json", "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin", "python3 tools/pin-disposition.py --selftest", "python3 tools/witness-metadata.py --selftest"],
    "opened": [".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-12/BashWitness/summary.json", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/witness-metadata.json", "corpus/SOURCES.md", "corpus/knowledge/incremental-pin-disposition.md", "corpus/lessons/round-13-verifier-spotcheck.md", "corpus/lessons/round-13.md", "tools/bash-witness-study.py", "tools/pin-disposition.py", "tools/trace-inputs.py", "tools/witness-metadata.py"],
    "inputs": {
      ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
      ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
      ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
      ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
      ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
      ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
      ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
      "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
      "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
      "corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420",
      "corpus/lessons/round-13.md": "93614bf4298026565955d703cea639bd07aac10e98c35fbfc0efc09ae47c24f6",
      "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
      "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
      "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
      "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"},
    "external_inputs": {
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
      "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
      "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "0f9c5a4c361316e111d0b2636780da5b8d848ccaa5c41507e8f8357ab6090075",
      "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06C-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06C-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06C-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06C-4.json"]}]}
```

Checked in a detached clone at 9f3084b (`/tmp/Read06C-wjnP`, SKILL.md sha256 matches the pinned value). The section runs lines 1548-1562 and is an instruction: it names an entry command and a self-test command per registry row.

Observed under `tools/trace-inputs.py` (all receipts rev=9f3084b, exit=0, no live-lane reads):

- `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` → exit 0, `metadata_consistent reason=ok` — matches verdict map "0 metadata_consistent/clean". The selftest covers exit 1 (`metadata_inconsistent`, e.g. `normalized_kind_null`) and exit 2 (`input_unavailable`/`snapshot_tampered`) cases exactly as mapped; argparse usage errors exit 2, consistent with "including usage".
- `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0, JSON with 6 legs (1 unchanged, 5 changed, 0 unavailable) — matches verdict map "0 observations, including changed/unavailable". Selftest exercises the exit-2 invalid-input classes (malformed digest, duplicate/missing leg, malformed/missing manifest, invalid root) — matches "2 invalid input/could-not-evaluate". Selftest itself exits 0 with `SELFTEST: PASS (19/19)`; exit 1 is the failure mapping as stated.
- `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`; git writes (`add`/`commit`/`checkout`) appear only inside isolated mkdtemp fixtures, matching the write-scope column ("selftest isolated temp repos only"). Probe normal mode used only read-only opens per the receipt.
- `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exercising the same exit-1/exit-2 classes.

Pinned-values columns verified: `pin-manifest.json` exists with exactly the six recorded legs (kumitate/kagi/tsukuroi/mado repos, pinned commits and digests, `result_reuse` semantics noted in its `note`); witness tool carries literal pinned digests for summary/declaration/declared plus expected kind/disclosure and the companion's `metadata_consistent`/exit-0 verdict; `expected.json` exists and its frozen check table is self-consistent.

Prose paragraph verified: "six recorded cases" = the six manifest legs; the historical summary's producer sha256 `249d9dcd…` (summary.json#/tool, companion `producer`) differs from the current `tools/bash-witness-study.py` bytes `60575e62…`, matching "the producer that actually ran, not the repaired current producer". SOURCES.md rows 56-57 back "S048 supersedes S047's object-specific paraphrase" and the retained distinction "item 4 is prioritisation, not a reuse skip" with no pronoun resolution. No old evidence hash was regenerated: all four pinned round-12 files hash exactly as pinned in the companion and tool literals.

No install performed. No git write commands in the lane; read-only `sha256sum`/`git log` in the clone only.
COLDREAD Read06C: executed-ok
