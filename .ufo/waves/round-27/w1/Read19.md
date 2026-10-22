# Read19 cold read: "The service's limits — what tameshi refuses to mutation-test"

**Verdict: gap-minor** (class: record). Read rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95. Section SKILL.md:1246-1271; the next `##` heading is at :1272. No fence is open at :1246.

Every anchor in the ten-row table resolves at 2227d83 and supports its row's core claim. The compact table and the detail note (corpus/knowledge/service-limits.md) carry the same refusals a–j in the same order. Three rows (b, c and g) need a wording or anchor fix (gaps 1–4 below), and the rendering diverges from the detail in a few places that the page says must be recorded. None of this blocks.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read19", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 1246, "heading": "### The service's limits \u2014 what tameshi refuses to mutation-test", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": [
  "Row b (SKILL.md:1259): 'refused before any suite runs' sits beside 'spec/control failures'. Only the spec refusal runs before any suite (tools/mutate-and-run.sh:1588-1593, selftest 'no suite run before refusal'). A red control first runs the suite once on the pristine copy (tools/mutate-and-run.sh:525-531), prints CONTROL: RED, then exits 2 as MUTATE: SETUP.",
  "Row b label: 'MUTATE: SETUP' for a red control is correct per the tool (tools/mutate-and-run.sh:242-245 and :529-531; selftest 'no-exec leg refusal names the red control (exit=126)'), but the cited anchor SKILL.md:843-844 says only 'a red control exits 2'. The label is not supported by the cited line.",
  "Row c (SKILL.md:1260): the label 'a moved substrate without a re-pin' is anchored only to :823-825, which says the service never re-pins. The trigger text is at SKILL.md:811-812 (also corpus/knowledge/service-optin-protocol.md:61-62), and the re-pin rule is at SKILL.md:1083-1086. The detail note cites those; the compact does not.",
  "Row g (SKILL.md:1264): 'outside the defect vocabulary' is not in the cited line corpus/knowledge/fleet-kill-rate-ledger.md:220 ('unmeasured everywhere'). It paraphrases SKILL.md:860-861 ('a rate is bounded by its defect vocabulary'), which the compact does not cite.",
  "Lead (SKILL.md:1248): 'Each refusal carries a measured anchor' overstates for rows a, b, c and e. Their anchors are requirement, design or province text (for example SKILL.md:823-825 and PROVINCE.md:14-18, :20), not measurements. The detail note's own standard (service-limits.md section 0) is 'a quoted file:line or a run output'.",
  "Divergences from the detail of record (corpus/knowledge/service-limits.md section 1), recorded per the page's rule: row a anchors are fleet-suite-census.md:269-275 and :277 in the detail, against :277-286 in the compact (269-275 is the standing offer, verified). Row c label is 'a moved substrate held to the old table' in the detail, against 'without a re-pin' in the compact. Row d's handler-gated sub-case (the-janitor; mutation-case-kagi-census.md:27-29 and :36-38, both verified) is absent from the compact. Row e cites PROVINCE.md:16-18 in the detail and 14-18 in the compact (a superset, no conflict).",
  "Detail-note anchor, outside the compact: service-limits.md section 1 row b cites corpus/knowledge/service-optin-protocol.md:199-201 for the refusal. Those lines state the killed/survived/inconclusive adjudication rule, not a refusal (verified). The refusal is supported by SKILL.md:813-817 and :840-844, and by protocol :80-85 (verified)."
 ],
 "commands_executed": [
  "python3 /tmp/Read19-hvmN/rangeread.py SKILL.md:1246-1271 SKILL.md:813-817 SKILL.md:823-825 SKILL.md:840-844 SKILL.md:879-881 PROVINCE.md:14-18 PROVINCE.md:20",
  "python3 /tmp/Read19-hvmN/rangeread.py corpus/knowledge/service-optin-protocol.md:26-30 corpus/knowledge/service-optin-protocol.md:86-91 corpus/knowledge/service-optin-protocol.md:129-132 corpus/knowledge/service-optin-protocol.md:267-269 corpus/knowledge/fleet-suite-census.md:277-286 corpus/knowledge/fleet-kill-rate-ledger.md:35-36 corpus/knowledge/fleet-kill-rate-ledger.md:156-158 corpus/knowledge/fleet-kill-rate-ledger.md:220",
  "python3 -c 'import sys;[print(open(p,encoding=\"utf-8\").read()) for p in sys.argv[1:]]' corpus/knowledge/service-limits.md",
  "python3 /tmp/Read19-hvmN/rangeread.py tools/mutate-and-run.sh:76-81 tools/mutate-and-run.sh:240-246 tools/mutate-and-run.sh:522-535 tools/mutate-and-run.sh:1580-1606",
  "python3 -c 'import sys;[print(open(p,encoding=\"utf-8\").read()) for p in sys.argv[1:]]' PROVINCE.md",
  "python3 /tmp/Read19-hvmN/rangeread.py corpus/knowledge/service-optin-protocol.md:199-201 corpus/knowledge/service-optin-protocol.md:160-161 corpus/knowledge/service-optin-protocol.md:105 corpus/knowledge/service-optin-protocol.md:80-85 corpus/knowledge/fleet-kill-rate-ledger.md:48 corpus/knowledge/fleet-kill-rate-ledger.md:293 corpus/knowledge/fleet-kill-rate-ledger.md:308 corpus/knowledge/fleet-kill-rate-ledger.md:310 corpus/knowledge/fleet-suite-census.md:269-275 corpus/knowledge/mutation-case-kagi-census.md:27-29 corpus/knowledge/mutation-case-kagi-census.md:36-38 SKILL.md:811-812 SKILL.md:1035 SKILL.md:1083-1086",
  "bash tools/mutate-and-run.sh --selftest",
  "python3 /tmp/Read19-hvmN/rangeread.py tools/trace-inputs.py:1-55 tools/trace-inputs.py:969-1003 SKILL.md:806-810 corpus/knowledge/service-optin-protocol.md:57-63",
  "python3 /tmp/Read19-hvmN/rangeread.py SKILL.md:858-862 SKILL.md:1155-1160"
 ],
 "opened": ["PROVINCE.md", "tools/mutate-and-run.sh", "tools/trace-inputs.py", "corpus/knowledge/service-optin-protocol.md", "corpus/knowledge/fleet-suite-census.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/service-limits.md", "corpus/knowledge/mutation-case-kagi-census.md"],
 "inputs": {
  "PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be",
  "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
  "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
  "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
  "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
  "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
  "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0",
  "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0"
 },
 "external_inputs": {},
 "traces": [
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-1.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-2.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-3.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-4.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-5.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-6.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-7.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-8.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read19-9.json"
 ]}]}
```

## Evidence

Setup, outside the collector as step 1 prescribes: `git clone --no-hardlinks` from the lane, then `checkout --detach 2227d83`. HEAD is 2227d83, `git status --porcelain` is empty, and `sha256sum SKILL.md` gives 386de44b…51e95. Scratch files live only in /tmp/Read19-hvmN.

Receipts Read19-1 to Read19-9 are under `.ufo/evidence/round-27/coldread/traces/`. Each has `rev` 2227d83, `exit` 0, empty `external`, empty `live_lane_reads`, and empty `untracked`. The `inputs` hashes equal `git show 2227d83:<path> | sha256sum` for all eight lane files.

Row checks (observed text, path:line):
- a: `service-optin-protocol.md:26-30` says the queue "(fleet-suite-census.md:277-286) is an offer, not a schedule" and that "a round with no opt-in records the no-opt-in line". The census lines 277-286 are the queue table. Holds.
- b: `SKILL.md:813-817` is opt-in request item 2, "A one-command hermetic suite"; `service-optin-protocol.md:63` is the same item. `SKILL.md:840-844`: "Any spec failure is `MUTATE: SETUP (<reason>)`, exit 2 — no headline" and "a red control exits 2". Tool: `tools/mutate-and-run.sh:242-245` (die_setup prints `MUTATE: SETUP (...)` and exits 2); `:525-531` (control run, then `CONTROL: RED`, then die_setup). Self-test, `bash tools/mutate-and-run.sh --selftest` (receipt 7): `MUTATE_SELFTEST: 97/97 pass`, `VERDICT: PASS`, exit 0, 7.44 s. Passing asserts include "duplicate old string refuses (exit 2)", "refusal is a SETUP verdict", "no suite run before refusal", and "no-exec leg refusal names the red control (exit=126)". Holds, with gap 1 and gap 2.
- c: `SKILL.md:823-825`: "The service never edits, repairs or re-pins the gate; a needed change is a recommendation to the owner". The tool also refuses a pin mismatch in regression mode as SETUP, exit 2 (receipt 7, selftest line 30: "regression pin mismatch is SETUP (exit 2)"). Holds, with gap 3.
- d: `service-optin-protocol.md:129-132`: "No live substrate read … a PATH-level stub, never the session". Holds.
- e: `PROVINCE.md:18`: "Credential material (→ kagi), endpoint health (→ kama)."; `:20`: "**Out of province → report, never absorb.**" Full file read (receipt 5): lines 1-20 are unchanged per the file's own append note, and the later appended sections keep the same rule. Holds.
- f: `SKILL.md:879-881` ("Sensitivity, not truth") and `fleet-kill-rate-ledger.md:156-158`. Holds.
- g: `fleet-kill-rate-ledger.md:220`: "U2 — coordinated multi-edit rewrites unmeasured everywhere". Holds, with gap 4.
- h: `service-optin-protocol.md:267-269`: "a named future, not a measurement". Holds.
- i: `fleet-kill-rate-ledger.md:35-36`: "a **directed repair**, not an independent rate". Holds.
- j: `service-optin-protocol.md:86-91`: the mado run "kept exactly its own 8, and removed exactly those paths". Holds.
- Lead text: "The cadence applies this table at intake" is consistent with `SKILL.md:1158-1159` ("an intake decision needs beside it: what tameshi refuses to mutation-test"). The standalone note exists and carries a–j with a trigger column (§1), verbatim quotes (§2), and the intake-precondition check (§3). The trailing "Anchors re-resolved 2026-10-14" is a dated claim I could not check. The anchors do resolve at 2227d83, so the page's re-resolve rule is met at this revision.

Monitor reasons:
- input-drift:PROVINCE.md. PROVINCE.md is 118 lines at 2227d83 (sha b2875fe2…). The detail note pinned 20 lines (sha f5e28bf1…). Lines 14-18 and 20 still carry the cited text. The growth is appended sections only.
- input-drift:tools/mutate-and-run.sh. The tool is 2016 lines at 2227d83 (sha fb91ef76…), while the SKILL's own pin at `SKILL.md:1304-1305` says 1642 lines. Its VERSION line still reads `r10-2` (`tools/mutate-and-run.sh:175`). The cited refusal lines and the self-test asserts hold, and the self-test passes 97/97.

## Findings by severity

- Blocking: none.
- Wrong expectations: none. Gap 1's wording gets the control outcome right (exit 2 as MUTATE: SETUP), but it misplaces the suite run.
- Minor: the seven items in `minor_gaps`.

Smallest safe corrections, recommendation only (no production file edited):
1. Row b: say the spec refusal runs before any suite, and that a red control runs once and then exits 2 as MUTATE: SETUP.
2. Row b anchor: add `tools/mutate-and-run.sh:242-245,529-531`, or add the MUTATE: SETUP label to SKILL.md:843-844.
3. Row c anchor: add `SKILL.md:811-812`.
4. Row g: add `SKILL.md:860-861` to the anchor, or drop "outside the defect vocabulary".
5. Lead: replace "a measured anchor" with "an anchor (a quoted file:line or a run output)".
6. Divergences: align the compact row a range, the row c label, the row d handler-gated sub-case, and the row e range, or record each one on the page.
7. Detail note: replace `service-optin-protocol.md:199-201` in row b with `:80-85`.

## Residual risk

- Every anchor is pinned to 2227d83. Since the detail note's 2026-10-14 pins, PROVINCE.md grew from 20 to 118 lines. The tool was 1341 lines at the detail's pin (cf41efaa), 1642 at the SKILL's pin (75ed934d), and is 2016 now, with its VERSION line still reading r10-2. The ledger and the kagi census note have moved since the detail's pins; the protocol and census pins still match. The compact anchors hold now, but a later edit can move them.
- The compact's tool claims depend on the tool's current labels. The compact cites SKILL line anchors, not the tool. Gap 2 shows the label is in the tool and not in the cited line.

## Verification gaps

- No lsp device is exposed to this seat, so no caller or definition claim was checked semantically. Text grep and line reads were the only tools, and no conclusion rests on grep alone.
- I did not follow sub-citations inside anchored lines, for example `plans/round-6.plan.md:23-25` inside SKILL.md:823-825. I also did not open these detail-only anchors: `fleet-suite-census.md:288-289` (row g), the row e anchors (AGENTS.md:4-5, SKILL.md:21, gates-survey-kagi.md, mutation-case-kagi-checklist.md:185 and :221-223), and the row d mado anchors (mutation-case-mado-verify.md:10-11 and :161-163).
- I checked the anchors as they resolve now, not the 2026-10-14 re-resolution event.
- I did not run `--regression`. It needs sibling repos, and that is outside a record read.
- In receipt 7 the self-test counted 237 opens under /home outside the fleet root (`dropped_home_count`). They are counted and never hashed. I did not inspect them.

## Process disclosure

- A tree-wide grep (pattern `service-limits|T9-2`, path = the clone root) ran by hand, outside the collector. It walked the clone tree, which holds the committed 2227d83 copies of SCORECARD.md, LOG.md, and .ufo/evidence/round-21/coldread/ledger.json (the three L1-appended files), so it may have read them. I did not open those three by path or under the collector, and I used nothing from them. The first page of its output showed only other evidence files (round-12, round-16, round-17, fleet-round-1, kaika-round-1). The remaining 222 or more matching files were never displayed. No receipt covers that scan, and it is not in `inputs`. L1 should decide whether it matters.
- Setup commands outside the collector are not listed in `commands_executed`, because they are not trace inputs. They are the clone and checkout, `git status`, the `git show … | sha256sum` cross-checks, and writing the scratch reader /tmp/Read19-hvmN/rangeread.py. Reader output and selftest output went to /tmp.
- SKILL.md was read by hand and under receipts 1, 6, 8, and 9. It is excluded from `inputs` by rule. Both tool files have receipts: tools/mutate-and-run.sh in receipts 4 and 7, tools/trace-inputs.py in receipt 8.
- I read my own receipts back from the live lane's traces directory after the runs, never during a trace.

## Tooling

No tool was installed or updated. I read /home/vgpnk/.omp/agent/RULES.md first. strace 7.2 (/usr/bin/strace) and Python 3.14.8 were already present and used as found.

COLDREAD Read19: gap-minor
