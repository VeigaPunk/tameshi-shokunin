# ColdC01 — independent cold reads, round 32 wave 2

Both sections read at lane revision `a4f718138bdad20de741faeca57891645e5a64d9` from a detached
fleet-mirror clone at `/fast/scratch/hyaku/tameshi-r32-seats/ColdC01/fleet/tameshi-shokunin`
(never the live lane). Every trace ran as `python3 tools/trace-inputs.py --root $R --out <trace> -- <argv>`
with the trace file name literal; all receipts recorded `rev = a4f718138bdad20de741faeca57891645e5a64d9`,
`exit: 0`, and `live_lane_reads` empty. `LOG.md` and `SCORECARD.md` (L1-appended files) were read only via
`git -C $R show a4f718138bdad20de741faeca57891645e5a64d9:<path>` outside the collector and recorded in
`external_inputs`.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdC01", "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a", "read_rev": "a4f718138bdad20de741faeca57891645e5a64d9",
  "sections": [
    {"start": 1380, "heading": "### The map — where a reader enters, artifact by artifact", "class": "record", "verdict": "verified-record",
     "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [
       "Line-level citations inside cited files (e.g. `LOG.md:316-317`, `:1294-1297`) were not re-verified at this revision; only file existence and section-level content were checked.",
       "The phrase 'the completion pack (`plans/completion-evidence.md`, this wave, uncommitted at this write)' describes the state at the section's write time; at read revision a4f718 the file is committed (present in the tree, sha 8e0485655a4801b9070bfa7dd688e774fed1a2e8b1692b046109ad83ebe2a3ef). Its own header confirms it was drafted during the round-11 wave at HEAD 606716f, so the historical claim stands, but the wording could mislead a current reader."
     ],
     "commands_executed": [
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/operator-runbook.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-limits.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/fleet-suite-census.md corpus/knowledge/service-standing-state.md",
       "python3 -c \"import sys\nfor p in sys.argv[1:]:\n    print('==== '+p+' ====')\n    print(open(p).read()[:200000])\" corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/README.md tools/mutate-and-run.sh",
       "python3 -c \"import os,sys; print('plans dir:', sorted(os.listdir('plans'))); [print('==== '+p+' ====', open(p).read()[:12000]) for p in sys.argv[1:]]\" plans/round-10.plan.md plans/round-10-record-draft.md plans/round-11.plan.md plans/completion-evidence.md"
     ],
     "opened": [
       "corpus/knowledge/operator-runbook.md", "corpus/knowledge/fleet-kill-rate-ledger.md",
       "corpus/knowledge/service-limits.md", "corpus/knowledge/service-optin-protocol.md",
       "corpus/knowledge/fleet-suite-census.md", "corpus/knowledge/service-standing-state.md",
       "corpus/knowledge/mutation-case-kumitate-sources-check.md", "corpus/knowledge/mutation-case-mado-verify.md",
       "corpus/knowledge/mutation-case-tsukuroi-census.md", "corpus/knowledge/mutation-case-kumitate-claims.md",
       "corpus/knowledge/mutation-case-kumitate-round-gate.md", "corpus/knowledge/mutation-case-kagi-census.md",
       "corpus/knowledge/mutation-case-kagi-checklist.md", "corpus/knowledge/mutation-case-kimi-census.md",
       "corpus/knowledge/mutation-case-kumitate-cite-check.md", "corpus/README.md",
       "tools/mutate-and-run.sh", "plans/round-10.plan.md", "plans/round-10-record-draft.md",
       "plans/round-11.plan.md", "plans/completion-evidence.md"
     ],
     "inputs": {
       "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
       "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
       "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0",
       "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
       "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
       "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952",
       "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38",
       "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
       "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604",
       "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
       "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
       "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
       "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7",
       "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
       "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
       "corpus/README.md": "c244f8ca2f877411e2d90195503f446a186bd10600664d75edfd0d6d59f14437",
       "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
       "plans/round-10.plan.md": "d130596ac8bc7e91a0895ec8f4980166ce6303f4349b08830936dcf9e794a419",
       "plans/round-10-record-draft.md": "8020f9bda420646936047c49307bce4ec124d18b88fc83b14a15072902fad9fd",
       "plans/round-11.plan.md": "068578f198367b79b14fea95d9db550828908e345e5cbc161cabf0e4bea744f7",
       "plans/completion-evidence.md": "8e0485655a4801b9070bfa7dd688e774fed1a2e8b1692b046109ad83ebe2a3ef"
     },
     "external_inputs": {
       "tameshi-shokunin@a4f718138bdad20de741faeca57891645e5a64d9:LOG.md": "6d013f916985e7714708cf84783ce250c8d8b3f6a15c0a360511dcd87371f829",
       "tameshi-shokunin@a4f718138bdad20de741faeca57891645e5a64d9:SCORECARD.md": "ffb67ddb172f55af771681432264b2124b74715eb5678091c7004708f0900008"
     },
     "traces": [
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC01-3-1.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC01-3-2.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC01-3-3.json"
     ]},
    {"start": 1938, "heading": "### Round-20 gate/probe registry — frozen receipt instruments", "class": "record", "verdict": "verified-record",
     "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [
       "Registry verdict-map cell for `tools/receipt-window.py` reads '64 usage/could-not-evaluate'; in the source, could-not-evaluate exits 2 and 64 is reserved for usage (the round-20 lesson itself notes usage was corrected to 64, not 2) — ambiguous grouping, not a functional misstatement."
     ],
     "commands_executed": [
       "python3 -c \"import sys\nfor p in sys.argv[1:]:\n    print('==== '+p+' ====')\n    print(open(p).read()[:120000])\" corpus/lessons/round-20.md .ufo/evidence/round-20/contract.json .ufo/evidence/round-20/public-cli-cases.json .ufo/evidence/round-20/final/receipts.json",
       "python3 -c \"import sys\nfor p in sys.argv[1:]:\n    print('==== '+p+' ====')\n    print(open(p).read()[:120000])\" tools/receipt-window.py tools/receipt-measure.py .ufo/evidence/round-20/stage/measure.py .ufo/evidence/round-20/coldread/measure.py",
       "python3 -c \"import hashlib, json\npairs = [('tools/receipt-window.py', 'f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc'), ('.ufo/evidence/round-20/stage/measure.py', 'f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d')]\nfor p, want in pairs:\n    h = hashlib.sha256(open(p,'rb').read()).hexdigest()\n    print(p, h, h == want)\ns = open('tools/receipt-measure.py').read()\nprint('runner_sha256 in source:', 'runner_sha256' in s)\nprint('check-spelling handling:', '--check' in s)\nc = open('.ufo/evidence/round-20/coldread/measure.py').read()\nprint('forbidden overrides:', [f for f in ('--ledger-file','--ledger-rev','--inputs-overlay') if f in c])\nprint('SELECTOR_OVERRIDE_FORBIDDEN:', 'SELECTOR_OVERRIDE_FORBIDDEN' in c)\""
     ],
     "opened": [
       "corpus/lessons/round-20.md", ".ufo/evidence/round-20/contract.json",
       ".ufo/evidence/round-20/public-cli-cases.json", ".ufo/evidence/round-20/final/receipts.json",
       "tools/receipt-window.py", "tools/receipt-measure.py",
       ".ufo/evidence/round-20/stage/measure.py", ".ufo/evidence/round-20/coldread/measure.py"
     ],
     "inputs": {
       "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6",
       ".ufo/evidence/round-20/contract.json": "9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715",
       ".ufo/evidence/round-20/public-cli-cases.json": "590df60420a60bec1f6dddad6b5eaf34a5d700cdd86c5cf231b1ef8f5a3b27b2",
       ".ufo/evidence/round-20/final/receipts.json": "4186b44e6f5ef95aeb39768e5b9d8a0e6953283961bcc009733dbbcde48cb5d6",
       "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
       "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa",
       ".ufo/evidence/round-20/stage/measure.py": "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d",
       ".ufo/evidence/round-20/coldread/measure.py": "48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13"
     },
     "external_inputs": {},
     "traces": [
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC01-4-1.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC01-4-2.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC01-4-3.json"
     ]}
  ]}
```

Plain-English note:

- Section 3 (lines 1380–1395, "### The map — where a reader enters, artifact by artifact") is a record: a table of artifact pointers. I opened every cited lane path under the trace collector: the six knowledge notes (operator-runbook, fleet-kill-rate-ledger, service-limits, service-optin-protocol, fleet-suite-census, service-standing-state), all nine `mutation-case-*.md` files (consistent with the "nine since round 26" count), `corpus/README.md`, `tools/mutate-and-run.sh` (sha at this rev a7d3f2dd…912eb9; contains `--selftest` and `--regression` with nine embedded legs, `nlegs=9`), and the plans directory (rounds 4–10 each have plan + record-draft; `round-11.plan.md` exists; no `round-11-record-draft.md` — consistent with "no separate round-11 record file"; `completion-evidence.md` exists, committed at this rev, whose own header confirms it was uncommitted when written). `LOG.md` and `SCORECARD.md` were read via `git show` outside the collector and recorded in `external_inputs` (sha 6d013f91… / ffb67ddb…). Minor gaps: deep line-level citations inside cited files were not re-verified, and the "uncommitted at this write" wording for the completion pack is historical (the file is committed at this read revision). Verdict: verified-record.
- Section 4 (lines 1938–1963, "### Round-20 gate/probe registry — frozen receipt instruments") is a record: a frozen-instrument registry. I opened `corpus/lessons/round-20.md`, `.ufo/evidence/round-20/contract.json`, `public-cli-cases.json`, `final/receipts.json`, `tools/receipt-window.py`, `tools/receipt-measure.py`, `.ufo/evidence/round-20/stage/measure.py`, and `.ufo/evidence/round-20/coldread/measure.py`. Verified claims: `tools/receipt-window.py` sha equals the contract's frozen/installed sha (f03ae7e9…); `.ufo/evidence/round-20/stage/measure.py` sha equals the frozen ruler sha (f34dc233…); `tools/receipt-measure.py` delegates to the unchanged staged ruler and implements `runner_sha256` (its own sha a67bffa9… appears in `final/receipts.json` as `runner_sha256`); the unsupported `--check` spelling is not accepted (selftest asserts refusal); the coldread selector contains the three forbidden overrides and the `SELECTOR_OVERRIDE_FORBIDDEN` refusal path (exit 64, abbreviations and equals forms covered); the gate uses `edit_interval` (not the planning annotation `install_window`), classifies historical identities without a freshness floor, and the frozen ruler hardcodes the six predicates. Minor gap: the verdict-map cell "64 usage/could-not-evaluate" is an ambiguous grouping (could-not-evaluate is 2 in the source). Verdict: verified-record.
- Trace-credit logistics: all six traces executed `tools/trace-inputs.py` with literal `--out` names, exit 0, argv matching the receipt, rev a4f718138bdad20de741faeca57891645e5a64d9, no live-lane reads. The first attempt at trace 3-2 failed on a Python one-liner syntax error and was redone in the same call shape; only the successful run produced the credited receipt (ColdC01-3-2.json).

COLDREAD ColdC01: verified-record, verified-record
