# ColdA05 — cold reads of SKILL.md sections 13, 14, 15 at bb681566

Read rev `bb681566b18211adf8ae9c28df91e17678e3f545` in a detached fleet-mirror
clone (`/tmp/ColdA05-CZiG/fleet/`, sibling lanes symlinked, tameshi a real
`git clone --no-hardlinks`). SKILL.md sha256 verified
`c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6`. Every trace
receipt reports `rev = bb681566…`, `live_lane_reads = {}`.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdA05", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
 "sections": [
{"start": 1281, "heading": "### The operator's runbook — `corpus/knowledge/operator-runbook.md`", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": ["The cited pinned blob e1e349b6... is not the content at read_rev (the runbook has grown to 516 L / 33 515 B, sha 8b2e185f..., via later append-only edits in commits 2a22ade and 58e5d53). The claim is explicitly scoped 'the sha governs'; the exact bytes exist in history at commit 606716f and verify word-perfect (511 L / 31 416 B, sha256 e1e349b69d798acb1d037db9c437709f8b679fd46ac32c441304a9c26a05914c), so this is declared drift, not an error."],
 "commands_executed": ["python3 -c \"import sys,hashlib;[(lambda d:print(p,hashlib.sha256(d).hexdigest(),len(d)))(open(p,'rb').read()) for p in sys.argv[1:]]\" corpus/knowledge/operator-runbook.md corpus/knowledge/service-limits.md"],
 "opened": ["corpus/knowledge/operator-runbook.md", "corpus/knowledge/service-limits.md"],
 "inputs": {"corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859", "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0"},
 "external_inputs": {"tameshi-shokunin@606716f703f7699af458476a31fc78ddc9bf552c:corpus/knowledge/operator-runbook.md": "e1e349b69d798acb1d037db9c437709f8b679fd46ac32c441304a9c26a05914c"},
 "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA05-13-1.json"]},
{"start": 1302, "heading": "### The six-leg regression — usage and this round's receipt", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": ["Anchor ranges sit one line off the material on the pinned bytes (verified at 606716f:tools/mutate-and-run.sh = 75ed934d...): the six-leg list occupies lines 84-89 vs cited 85-89; sources 90-96 vs 90-97; the regression exit map is at :115-119 as cited but the workdir/scratch lines run to :125.", "The tool at read_rev is drifted per the page's own convention: tools/mutate-and-run.sh is now a7d3f2dd... (2,080 L, nine-leg registry; r16/r18/r26 legs appended). The section's claims are scoped to 75ed934d... ('the sha governs'), whose bytes exist at commit 606716f and reproduce the claimed receipt exactly (see note).", "A first run of each --regression was killed at the 300 s job deadline mid-replay (all completed legs PASSed exact) and produced no receipt; both were re-run with an 840 s timeout to completion and those receipts are the ones listed."],
 "commands_executed": ["timeout 330 bash tools/mutate-and-run.sh --selftest", "timeout 330 bash tools/mutate-and-run.sh --regression", "python3 -c \"import sys,hashlib;[(lambda d:print(p,hashlib.sha256(d).hexdigest(),len(d)))(open(p,'rb').read()) for p in sys.argv[1:]]\" corpus/knowledge/fleet-kill-rate-ledger.md", "timeout 330 bash /tmp/pinned-fleet/tameshi-shokunin/tools/mutate-and-run.sh --selftest", "timeout 330 bash /tmp/pinned-fleet/tameshi-shokunin/tools/mutate-and-run.sh --regression", "timeout 840 bash tools/mutate-and-run.sh --regression", "timeout 840 bash /tmp/pinned-fleet/tameshi-shokunin/tools/mutate-and-run.sh --regression"],
 "opened": ["tools/mutate-and-run.sh", "corpus/knowledge/fleet-kill-rate-ledger.md"],
 "inputs": {"tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e"},
 "external_inputs": {"tameshi-shokunin@606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5"},
 "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA05-14-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA05-14-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA05-14-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA05-14-6.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA05-14-7.json"]},
{"start": 1380, "heading": "### The map — where a reader enters, artifact by artifact", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": ["corpus/README.md has drifted since the section's write (it now carries a Round-30 section at :449+); the 'coverage map — one row per note, holds + sources' shape it describes is unchanged.", "fleet-kill-rate-ledger.md carries no literal string 'byte-frozen'; the claim is a fair paraphrase of the ledger's own rule (its Errata section is titled 'append-only', ER-4 states 'No §1–§4 cell is edited', and operator-runbook.md quick start says 'never edit §1–§4').", "The LOG.md:316-317 cite lands on the right statement: line 317 carries 'ARE the wave record (no .ufo/waves/tameshi-r11-* directory)'."],
 "commands_executed": ["python3 -c \"import sys,hashlib;[(lambda d:print(p,hashlib.sha256(d).hexdigest(),len(d)))(open(p,'rb').read()) for p in sys.argv[1:]]\" corpus/README.md corpus/knowledge/operator-runbook.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-limits.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/fleet-suite-census.md corpus/knowledge/service-standing-state.md corpus/knowledge/closeout-r11.md corpus/knowledge/mutation-case-*.md tools/mutate-and-run.sh plans/round-*.plan.md plans/round-*-record-draft.md plans/completion-evidence.md"],
 "opened": ["corpus/README.md", "corpus/knowledge/operator-runbook.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/service-limits.md", "corpus/knowledge/service-optin-protocol.md", "corpus/knowledge/fleet-suite-census.md", "corpus/knowledge/service-standing-state.md", "corpus/knowledge/closeout-r11.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/knowledge/mutation-case-kagi-checklist.md", "corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kumitate-cite-check.md", "corpus/knowledge/mutation-case-kumitate-claims.md", "corpus/knowledge/mutation-case-kumitate-round-gate.md", "corpus/knowledge/mutation-case-kumitate-sources-check.md", "corpus/knowledge/mutation-case-mado-verify.md", "corpus/knowledge/mutation-case-tsukuroi-census.md", "tools/mutate-and-run.sh", "plans/round-2.plan.md", "plans/round-3.plan.md", "plans/round-4.plan.md", "plans/round-5.plan.md", "plans/round-6.plan.md", "plans/round-7.plan.md", "plans/round-8.plan.md", "plans/round-9.plan.md", "plans/round-10.plan.md", "plans/round-11.plan.md", "plans/round-4-record-draft.md", "plans/round-5-record-draft.md", "plans/round-6-record-draft.md", "plans/round-7-record-draft.md", "plans/round-8-record-draft.md", "plans/round-9-record-draft.md", "plans/round-10-record-draft.md", "plans/completion-evidence.md"],
 "inputs": {"corpus/README.md": "636b716e7891f09cc3eb4a2c47bcf3a5120460c356dcfc07f5d8ba9b63259909", "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e", "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0", "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e", "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f", "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952", "corpus/knowledge/closeout-r11.md": "cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265", "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0", "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7", "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548", "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e", "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9", "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec", "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38", "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3", "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604", "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9", "plans/round-2.plan.md": "8eccbbfdf0d8c2bd76ced8c9d58c40c17ea48dfeb564f598c315ea835360ccec", "plans/round-3.plan.md": "2200c8896b46b583006f4a72a1d7e9b5c4f7b1bfd40e14210727114d73b4552f", "plans/round-4.plan.md": "4e63256474d56ba09a3d1e27298dc67cc45c3a60bc5daf70638a6f7b584d9e42", "plans/round-5.plan.md": "5ade0413bc9a8d891df774156e597f893617ff80a49b4fe274adc204b8a63582", "plans/round-6.plan.md": "ec5b8236a1f12f57a83b45d24f77fbd9313894ae1305623404e2a9c4b7d86907", "plans/round-7.plan.md": "49cd55fd0efaf892c281ec90538310cd5691af2af4ab1270c9945146fdc0fcec", "plans/round-8.plan.md": "7e53c9d89b4887a482816639c6678346e8ed500137eefbcae6cac8997cc0358e", "plans/round-9.plan.md": "230ed6b61e4c89d9a0ad8c693dbf35a4368f137060f6ac0d3d8863433020da6a", "plans/round-10.plan.md": "d130596ac8bc7e91a0895ec8f4980166ce6303f4349b08830936dcf9e794a419", "plans/round-11.plan.md": "068578f198367b79b14fea95d9db550828908e345e5cbc161cabf0e4bea744f7", "plans/round-4-record-draft.md": "c142ccca8a44902e8dad9cefe5714c7255cc35dab80b17b5b3bb940361ac0cf9", "plans/round-5-record-draft.md": "176d0d909898749a99b2cb71e061c594536b12da493d4e36f2ffc42c8df4a5e5", "plans/round-6-record-draft.md": "d146cc6171dc3e60b45a130fd29a0501269bd2272e467b0a1faab28c5696315e", "plans/round-7-record-draft.md": "9fed2565ca13ea63c5b23e81db01b4458e67db22aeef8791461cc8d3eb72eb2f", "plans/round-8-record-draft.md": "20218607d817f7fe456794da677dba2ce83439aa871a83697effc034e724235d", "plans/round-9-record-draft.md": "0ca3094d0dc885022dcdf3c2b3e261188473d8e1633697ee65b17fdc56621ac7", "plans/round-10-record-draft.md": "8020f9bda420646936047c49307bce4ec124d18b88fc83b14a15072902fad9fd", "plans/completion-evidence.md": "8e0485655a4801b9070bfa7dd688e774fed1a2e8b1692b046109ad83ebe2a3ef"},
 "external_inputs": {"tameshi-shokunin@bb681566b18211adf8ae9c28df91e17678e3f545:LOG.md": "d603864623685c9b0a7bee7a2ea00aeb93e266cc4f6641617bd6b0070fb79db7", "tameshi-shokunin@bb681566b18211adf8ae9c28df91e17678e3f545:SCORECARD.md": "9ba015ca568db27e71dd35322884952c18f7be0e306667f35391da7174fd920a"},
 "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA05-15-1.json"]}
]}
```

What I checked, per section:

**Section 13 (1281, the operator's runbook).** Record. The sha governs, and the
claimed bytes exist: `git show 606716f:corpus/knowledge/operator-runbook.md`
hashes to exactly `e1e349b6…`, 511 lines / 31 416 bytes as stated. On those
pinned bytes the section map is verbatim — §0 quick start, §1 service, §2
tool, §3 six-case ledger, §4 opt-in, §5 limits, §6 cadence (T1–T3), §7
regression, §8 full loop, §9 receipts, §10 unknowns, append-only errata. The
"anchored source governs" rule sits at its lines 10-11; §9's receipts are
pinned to tool `cf41efaa…` (r7-1, four legs); errata ER-R1/ER-R2 record the
r10-2 in-flight edit and name the T2 remedy. At read_rev the file has two
later appends (ER-R3, ER-jj2), all append-only. `verified-record`.

**Section 14 (1302, the six-leg regression).** Instruction — it names
`bash tools/mutate-and-run.sh --regression`. I ran both revisions:

- The pinned tool `75ed934d…` (materialized at `/tmp/pinned-fleet/` so its
  `dirname³($SELF)` fleet resolution works): `--selftest` → `MUTATE_SELFTEST:
  80/80 pass` / `VERDICT: PASS` rc 0, and `--regression` → `REGRESSION: PASS
  (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)` rc 0, every
  leg `match` exact (10/10 ×5, 15/15 checklist), `flips=0 inconclusive=0`,
  `REGRESSION_PIN` lines carrying `mode=` and git-sourced rev/sha exactly as
  the receipt claims (534 s). This reproduces the section's recorded receipt
  byte-for-byte.
- The tool at read_rev `a7d3f2dd…`: `--selftest` → `106/106 pass` rc 0;
  `--regression` → `REGRESSION: PASS (cases=9 passed=9)` rc 0 (719 s) — the
  drifted nine-leg registry also holds.

Static claims verified on the pinned blob: leg table rates and target paths
match the header and the embedded `PIN_*/REV_*/TABLE_*` block; the exec-bit
mirror (`:932-960`), the usage line, default scratch, and exit map are as
described; ledger `:85-88` still reads "cases 1 and 2 only" and ER-2 (`:272`,
block running through `:281`+) records the four-leg supersession; SKILL.md's
own anchors `:925-929`, `:1218-1228`, `:965-1008` resolve. `executed-ok`.

**Section 15 (1380, the artifact map).** Record. All eleven table rows check
out: every named artifact exists with the described role; nine
`mutation-case-*.md` files (claim "nine since round 26"); the tool row's
nine-leg claim matches the observed registry; the plans convention holds
(plans for rounds 2-11, record drafts only for 4-10, no round-11 record file);
`plans/completion-evidence.md` and `corpus/knowledge/closeout-r11.md` exist
and match their descriptions; `LOG.md` line 317 carries the "ARE the wave
record" statement; `SCORECARD.md` does carry move-log rows with counting
commands (both via `git show`, recorded as external inputs since they are
L1-appended). `verified-record`.

No tools were installed; no fleet or lane writes beyond the trace receipts and
this report; all scratch lived under `/tmp/ColdA05-*` and `/tmp/pinned-fleet`,
and no processes I started remain running.

COLDREAD ColdA05: verified-record, executed-ok, verified-record
