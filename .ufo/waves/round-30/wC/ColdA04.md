# ColdA04 — cold reads, SKILL.md sections 10–12 at bb681566

Clone: `/tmp/ColdA04-udCE/fleet/tameshi-shokunin` detached at
`bb681566b18211adf8ae9c28df91e17678e3f545`; `SKILL.md` sha256
`c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6` (verified).
Sibling lanes symlinked into the mirror; the read `rev` on every receipt equals
`read_rev`. No tools installed (strace, python3 already present).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdA04", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
  "sections": [
    {"start": 1212, "heading": "### The receipt at this boundary", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": ["The `tools/mutate-and-run.sh:733-791` anchor for 'git-materialized' is stale at bb681566b18211adf8ae9c28df91e17678e3f545: that range now holds embedded defect-spec heredocs; the git-materialization code moved to roughly :1180-1230. The mechanism claim itself is confirmed — six legs' REGRESSION_PIN lines showed `source=git` with matching rev/path/mode/sha256 in my interrupted replay."],
     "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-optin-protocol.md tools/mutate-and-run.sh"],
     "opened": ["corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/service-optin-protocol.md", "tools/mutate-and-run.sh"],
     "inputs": {"corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e", "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e", "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"},
     "external_inputs": {}, "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA04-10-1.json"]},
    {"start": 1246, "heading": "### The service's limits — what tameshi refuses to mutation-test", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [],
     "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" PROVINCE.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/service-limits.md corpus/knowledge/fleet-suite-census.md corpus/knowledge/fleet-kill-rate-ledger.md"],
     "opened": ["PROVINCE.md", "corpus/knowledge/service-optin-protocol.md", "corpus/knowledge/service-limits.md", "corpus/knowledge/fleet-suite-census.md", "corpus/knowledge/fleet-kill-rate-ledger.md"],
     "inputs": {"PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be", "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e", "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0", "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e"},
     "external_inputs": {}, "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA04-11-1.json"]},
    {"start": 1272, "heading": "## The operator's runbook and the six-leg regression (round 10, measured)", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": ["Every tools/mutate-and-run.sh line anchor in the section is 'as read at 75ed934d…' and drifts at bb681566b18211adf8ae9c28df91e17678e3f545 (the embedded leg list is now nine entries at :87-95, not six at :85-89; pins/tables sit at :605-631). The section itself flags this ('the sha governs'), so it is qualified drift, not an error.", "The replay is nine legs at this revision, not six — the section is explicitly an r10-2 record and rounds 16/18/26 added legs 7-9.", "A complete `--regression` replay exceeds the 6-minute bound on this host: my own run reached six legs in ~300 s before the timeout cut it (legs 1-6 all PASS, match=N/N, flips=0)."],
     "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/operator-runbook.md tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md", "bash tools/mutate-and-run.sh --selftest"],
     "opened": ["corpus/knowledge/operator-runbook.md", "tools/mutate-and-run.sh", "corpus/knowledge/fleet-kill-rate-ledger.md"],
     "inputs": {"corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859", "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e"},
     "external_inputs": {}, "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA04-12-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA04-12-2.json"]}
  ]}
```

What I checked, in plain English. Section 10 (the round-9 receipt): the ledger
line at `fleet-kill-rate-ledger.md:282` really does say cases 5/6 carried no
`REGRESSION` line and names the same debt; `:350` records the 4-leg
`cases=4 passed=4` run with `67/67` selftest at `cf41efaa…`; the re-pin rule it
quotes at `service-optin-protocol.md:59-62` is verbatim ("A moved substrate
needs a re-pin, never a re-interpretation of the old table"); the T1 rule at
SKILL.md:1069-1090 matches. The 19:58:49Z/19:58:59Z timestamps and `/tmp`
log paths are a 2026-10-14 historical claim I cannot re-verify (logs are gone;
the ledger's corroborating run at `:341` is a different T9 run) — consistent
with the record. One stale anchor (`:733-791`), listed as a minor gap.

Section 11 (the refusal table): all ten rows' anchors re-resolve at
bb681566 — optin `:26-30`, `:86-91`, `:129-132`, `:267-269`; census `:277-286`;
PROVINCE `:14-18`/`:20`; ledger `:35-36`, `:156-158`, `:220` (U2); self-anchors
`:813-817`, `:823-825`, `:840-844`, `:879-881`. `corpus/knowledge/service-limits.md`
carries rows a–j with matching refusals and richer anchors — no divergence.

Section 12 (runbook + six-leg regression): `operator-runbook.md` exists with
§0–§10 + append-only errata exactly as mapped (516 L / 33 515 B at this rev —
grown past the recorded 511 L / 31 416 B by appended ER-R3/ER-jj2 errata, which
the file's own rule allows); §7's embedding-status line and §9's receipts are
`cf41efaa…`-era as claimed; ER-R1/ER-R2 name the T2 remedy. All six table rows
match the embedded `REV_*`/`TABLE_*` constants at bb681566 exactly
(8/10, 8/10, 6/10, 4/10, 7/15, 7/10 killed at revs `175de6ba`/`fecee874`/
`165307fe`/`eead56b2`/`fecee874`/`175de6ba`). The documented command runs:
`--selftest` under the collector → `MUTATE_SELFTEST: 106/106 pass` /
`VERDICT: PASS`, rc 0 (the section's `80/80` is the r10-2 count; arms were
added since). I also ran the full `bash tools/mutate-and-run.sh --regression`
under the collector: it completed legs 1–6 — all `PASS`, `match=10/10` or
`15/15`, `flips=0`, blobs git-materialized at the recorded revs with matching
sha256 and `mode=100755` from the mirrored sibling repos — before the 300 s
deadline cut it during leg 7; the timeout killed the collector before a
receipt was written, so that run has no trace file (kept receipt files:
ColdA04-12-1 record-read, ColdA04-12-2 selftest). Its leftover process tree
and `/tmp/tameshi-r4-2-regression.HYeQRI` scratch were killed/removed; nothing
else I started remains.

COLDREAD ColdA04: gap-minor, verified-record, gap-minor
