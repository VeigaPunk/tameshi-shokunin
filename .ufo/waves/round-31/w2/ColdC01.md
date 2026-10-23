# ColdC01 — independent cold read, Tameshi round 31 wave 2

Read at lane revision 2da841bd9913a2037d2bf612793382e572c9d205 (detached clone
/fast/scratch/hyaku/tameshi-r31-seats/ColdC01/fleet/tameshi-shokunin).
SKILL.md sha256 2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ColdC01",
  "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a",
  "read_rev": "2da841bd9913a2037d2bf612793382e572c9d205",
  "sections": [
    {
      "start": 1380,
      "heading": "### The map — where a reader enters, artifact by artifact",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c \"import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]\" corpus/knowledge/operator-runbook.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-limits.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/fleet-suite-census.md corpus/knowledge/service-standing-state.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md corpus/knowledge/closeout-r11.md tools/mutate-and-run.sh corpus/README.md plans/round-11.plan.md plans/completion-evidence.md"
      ],
      "opened": [
        "corpus/README.md",
        "corpus/knowledge/closeout-r11.md",
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "corpus/knowledge/fleet-suite-census.md",
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/knowledge/mutation-case-kagi-checklist.md",
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md",
        "corpus/knowledge/mutation-case-kumitate-claims.md",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md",
        "corpus/knowledge/mutation-case-kumitate-sources-check.md",
        "corpus/knowledge/mutation-case-mado-verify.md",
        "corpus/knowledge/mutation-case-tsukuroi-census.md",
        "corpus/knowledge/operator-runbook.md",
        "corpus/knowledge/service-limits.md",
        "corpus/knowledge/service-optin-protocol.md",
        "corpus/knowledge/service-standing-state.md",
        "plans/completion-evidence.md",
        "plans/round-11.plan.md",
        "tools/mutate-and-run.sh"
      ],
      "inputs": {
        "corpus/README.md": "0b68064b9d65a93eb8abfbcd86736cff927f827894d643449e413b3aa7212cbd",
        "corpus/knowledge/closeout-r11.md": "cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
        "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
        "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7",
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
        "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
        "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38",
        "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
        "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604",
        "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
        "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0",
        "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
        "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952",
        "plans/completion-evidence.md": "8e0485655a4801b9070bfa7dd688e774fed1a2e8b1692b046109ad83ebe2a3ef",
        "plans/round-11.plan.md": "068578f198367b79b14fea95d9db550828908e345e5cbc161cabf0e4bea744f7",
        "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"
      },
      "external_inputs": {
        "tameshi-shokunin@2da841bd9913a2037d2bf612793382e572c9d205:LOG.md": "de531eccb30c13348447ebe84ada25afbed5df3bf98f15dd69d77aaa7f2ac3b2",
        "tameshi-shokunin@2da841bd9913a2037d2bf612793382e572c9d205:SCORECARD.md": "dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC01-3-1.json"
      ]
    },
    {
      "start": 1517,
      "heading": "## Pin disposition and provenance correction — round 13",
      "class": "instruction",
      "verdict": "executed-ok",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /fast/scratch/hyaku/tameshi-r31-seats/ColdC01/fleet",
        "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin",
        "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
        "python3 -c \"import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]\" corpus/knowledge/incremental-pin-disposition.md corpus/lessons/round-12-verifier-spotcheck.md corpus/SOURCES.md .ufo/evidence/round-12/BashWitness/summary.json .ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/witness-metadata.json .ufo/evidence/round-13/expected.json"
      ],
      "opened": [
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        "corpus/SOURCES.md",
        "corpus/knowledge/incremental-pin-disposition.md",
        "corpus/lessons/round-12-verifier-spotcheck.md",
        "tools/pin-disposition.py",
        "tools/witness-metadata.py"
      ],
      "inputs": {
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741",
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "corpus/lessons/round-12-verifier-spotcheck.md": "6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
      },
      "external_inputs": {
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "0f9c5a4c361316e111d0b2636780da5b8d848ccaa5c41507e8f8357ab6090075",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC01-4-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC01-4-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC01-4-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC01-4-4.json"
      ]
    },
    {
      "start": 1548,
      "heading": "### Round-13 gate/probe registry",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c \"import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]\" .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/witness-metadata.json .ufo/evidence/round-13/expected.json tools/pin-disposition.py tools/witness-metadata.py corpus/SOURCES.md corpus/knowledge/incremental-pin-disposition.md",
        "python3 tools/pin-disposition.py --selftest",
        "python3 tools/witness-metadata.py --selftest"
      ],
      "opened": [
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        "corpus/SOURCES.md",
        "corpus/knowledge/incremental-pin-disposition.md",
        "tools/pin-disposition.py",
        "tools/witness-metadata.py"
      ],
      "inputs": {
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741",
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC01-5-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC01-5-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC01-5-3.json"
      ]
    }
  ]
}
```

Plain-English note:

Section 3 (record, the map): opened every listed artifact and the two exception
lane files (LOG.md, SCORECARD.md) via `git show` at rev, outside the collector.
Verified: runbook §0/§2-§7/§10 headings exist; ledger states one row per gate
with suite/rate/survivors/last-sweep/pin; service-limits standalone note exists
and SKILL.md:1246-1270 is exactly the compact-rendering pointer; opt-in protocol
carries request shape, re-pin rule, read-only guarantees, report shape and
boundaries; suite census carries offer and surveyed-but-unmeasured queue;
standing-state carries SC1-SC3 and handoff conditions; nine mutation-case notes
exist ("nine since round 26"); mutate-and-run.sh has `--selftest`/`--regression`
and nine embedded legs (js-cite-check last, r26); corpus/README.md is a coverage
map with Holds+Sources per row; plans round-4..10 plan+record-draft pairs exist,
round-11.plan.md exists and no round-11-record-draft.md exists; LOG.md:316-317
confirms the wave deliverables are the round-11 record; completion-evidence.md is
tracked at rev (the row's "uncommitted at this write" describes the round-11
writing-time state). All claims in the table checked out.

Section 4 (instruction, recipe): executed the named commands under the trace
collector. `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` (as written, live fleet root) exited 0, emitted six dated rows, observed only hashes and git metadata (receipt external = the six sibling worktree files only; no live-lane reads), result_reuse=not_established, not_compared list present — at 2026-10-23T09:40:11Z the dated read was 1 unchanged / 5 changed / 0 unavailable. `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` exited 0 metadata_consistent. Step 1's manifest note and NOT_COMPARED were read first; step 4 verified: canonical summary and rerun summary both keep declaration.kind=null, the companion covers only the canonical summary and records the rerun null as named-residual-uncorrected, and expected.json pins the producer before/oracle/after selftests. Step 5 (no sibling-gate rerun) was respected; no gate was executed beyond these two read-only tools. I also made a first attempt with the mirror fleet root (symlink farm), which the tool correctly rejects (all six legs repo_symlink/unavailable); the executed-as-written run with the fleet root is the credited one.

Section 5 (record, registry): opened the manifest, companion, expected.json and both tool sources; ran both selftests under the collector (pin SELFTEST: PASS 19/19; witness SELFTEST: PASS 39/39, exit 0). Verified the rows: pin-disposition exit semantics 0 observations / 2 invalid input / selftest 1 failed match the source; canonical six-leg mapping matches the manifest legs and tool order; witness-metadata exit semantics 0 clean / 1 inconsistent / 2 input_unavailable or snapshot_tampered (including usage, argparse exit 2) match the source and the 39 selftest cases; pinned digests in the tool match the companion and expected.json byte for byte; S048 supersedes S047's paraphrase with "item 4 is prioritisation, not a reuse skip" exactly as the row states; producer SHA in the companion equals summary.json's /tool hash (249d9dcd...) and the runner 75ed934d..., consistent with "producer that actually ran, not the repaired current producer"; no row changes rank/SHONEN authority/the six recorded cases. No finding.

All seven trace receipts are at rev 2da841bd9913a2037d2bf612793382e572c9d205, exit 0, with empty live_lane_reads; the trace calls executed tools/trace-inputs.py directly with `--out` naming each trace file literally.

COLDREAD ColdC01: verified-record, executed-ok, verified-record
