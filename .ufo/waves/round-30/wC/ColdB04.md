# ColdB04 — cold reads, sections 11–13 of SKILL.md at bb681566b18211adf8ae9c28df91e17678e3f545

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdB04", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
  "sections": [
    {"start": 1246, "heading": "### The service's limits — what tameshi refuses to mutation-test", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [],
     "commands_executed": [
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/service-optin-protocol.md corpus/knowledge/fleet-suite-census.md PROVINCE.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-limits.md",
       "grep -n \"control run on the pristine copy is red\" tools/mutate-and-run.sh"
     ],
     "opened": ["corpus/knowledge/service-optin-protocol.md", "corpus/knowledge/fleet-suite-census.md", "PROVINCE.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/service-limits.md", "tools/mutate-and-run.sh"],
     "inputs": {
       "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
       "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
       "PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be",
       "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
       "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0",
       "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"
     },
     "external_inputs": {},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB04-11-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB04-11-2.json"]},

    {"start": 1272, "heading": "## The operator's runbook and the six-leg regression (round 10, measured)", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [],
     "commands_executed": [
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/operator-runbook.md",
       "git log --follow --format=%H:%ad:%s --date=short -- corpus/knowledge/operator-runbook.md",
       "bash -c 'grep -n \"embedding, not a re-cut\\|cases 5/6\\|r10-2\" tools/mutate-and-run.sh | head -20'",
       "grep -n \"gap is named\\|runbook\\|entry point\" plans/round-10.plan.md"
     ],
     "opened": ["corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/operator-runbook.md", "tools/mutate-and-run.sh", "tools/registry.json", "plans/round-10.plan.md", "plans/round-9.plan.md"],
     "inputs": {
       "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
       "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
       "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
       "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
       "plans/round-10.plan.md": "d130596ac8bc7e91a0895ec8f4980166ce6303f4349b08830936dcf9e794a419",
       "plans/round-9.plan.md": "230ed6b61e4c89d9a0ad8c693dbf35a4368f137060f6ac0d3d8863433020da6a"
     },
     "external_inputs": {},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB04-12-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB04-12-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB04-12-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB04-12-4.json"]},

    {"start": 1281, "heading": "### The operator's runbook — `corpus/knowledge/operator-runbook.md`", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [],
     "commands_executed": [
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/operator-runbook.md corpus/knowledge/service-limits.md",
       "bash -c 'git show 606716f703f7699af458476a31fc78ddc9bf552c:corpus/knowledge/operator-runbook.md | tee /dev/stderr | sha256sum; git show 606716f703f7699af458476a31fc78ddc9bf552c:corpus/knowledge/operator-runbook.md | wc -lc'"
     ],
     "opened": ["corpus/knowledge/operator-runbook.md", "corpus/knowledge/service-limits.md"],
     "inputs": {
       "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
       "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0"
     },
     "external_inputs": {"tameshi-shokunin@bb681566b18211adf8ae9c28df91e17678e3f545:corpus/knowledge/operator-runbook.md": "e1e349b69d798acb1d037db9c437709f8b679fd46ac32c441304a9c26a05914c"},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB04-13-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB04-13-2.json"]}
  ]
}
```

## What I checked

**Section 11 (`### The service's limits`, lines 1246–1270).** Record. I opened all five
cited lane files and re-resolved every anchor at bb681566. Row a: "offer, not a schedule …
no-opt-in line" is verbatim in `service-optin-protocol.md:26-30`; the queue table is
`fleet-suite-census.md:277-286`. Row b: `SKILL.md:813-817` is the hermetic-suite contract,
`:840-844` covers spec-parse `MUTATE: SETUP` exit 2 and the red-control exit 2; the tool
emits `MUTATE: SETUP (…)` for a red control (`tools/mutate-and-run.sh:533`, via
`die_setup` at `:245`). Row c: `:823-825` is the never-edits sentence. Row d:
`service-optin-protocol.md:129-132` is the no-live-substrate/PATH-stub rule. Row e:
`PROVINCE.md:16-18` names credential material (→ kagi) and endpoint health (→ kama);
`:20` is "Out of province → report, never absorb." Row f: `SKILL.md:879-881` +
`fleet-kill-rate-ledger.md:156-158` carry sensitivity ≠ truth. Row g:
`fleet-kill-rate-ledger.md:220` is U2 verbatim. Row h:
`service-optin-protocol.md:267-269` is U4 verbatim. Row i: `fleet-kill-rate-ledger.md:35-36`
is the directed-repair rule verbatim. Row j: `service-optin-protocol.md:86-91` records the
mado run removing only its own 8 scratch dirs. The standalone note
`corpus/knowledge/service-limits.md` carries the same a–j rows as detail of record with
the verbatim quotes (§1–§2), as the section claims; its table is richer but agrees.

**Section 12 (`## The operator's runbook and the six-leg regression`, lines 1272–1280).**
Record. "Round 7 made `--regression` the ledger's replay gate": `SKILL.md:921-925` ("the
leg ledger — replay, receipt, and how it is read (round 7, measured)") and the tool header
`:83` agree. "the registry ran four legs with cases 5–6 'still not embedded — named debt'
(`:1226-1228`)": `:1226-1228` reads "Cases 5–6 are still not embedded: their rows carry no
`REGRESSION` line — named debt, not smoothed"; ledger `:281` confirms four legs at
`cf41efaa…` and `:282` names cases 5/6 unembedded. "the operator … had no single entry
point": `git log --follow` shows `corpus/knowledge/operator-runbook.md` first appears in
commit `606716f` ("probation round 10"), and `plans/round-10.plan.md:167` names the gap
explicitly. "the leg cut resolves as an embedding of cases 5–6 (T10-2), never a re-cut":
the tool header reads "resolves the round-8 leg cut — cases 5/6 … embedded as the fifth
and sixth legs" and "resolved here as an embedding, not a re-cut"
(`tools/mutate-and-run.sh:12-14`, `:27`); legs 1–4 pins are unchanged (`:583-601`).

**Section 13 (`### The operator's runbook`, lines 1281–1301).** Record. The `e1e349b6…`
blob is real: `git show 606716f:corpus/knowledge/operator-runbook.md` sha256s to
`e1e349b69d798acb1d037db9c437709f8b679fd46ac32c441304a9c26a05914c`, `wc -lc` = 511 / 31 416
(the committed file at bb681566 is a later revision, as the section's "uncommitted
worktree file" qualifier anticipates). The runbook's header states the single
operator-facing role and "the anchored source governs" rule verbatim (`operator-runbook.md:1-11`).
The §0–§10 + append-only errata map matches the file's real headings (`:35,65,93,131,180,
243,269,345,408,438,462,481`). "Adds no gate measurement" is stated at `:8-9` and `:459`.
Receipts executed at `cf41efaa…` (r7-1, four legs): §7's executed receipt
(`:378-397`, four legs `cases=4 passed=4`) and embedding-status line (`:374-376`,
"cases 5/6 are not embedded — named debt"), §9's receipts (`:444-452`). ER-R1/ER-R2
(`:486-512`) record the in-flight r10-2 tool edit and name the T2 remedy — re-run
`--selftest` and `--regression` under the new revision and record both pins.

No discrepancies found; all three sections are records that check out.

COLDREAD ColdB04: verified-record, verified-record, verified-record
