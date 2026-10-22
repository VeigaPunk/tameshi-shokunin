# Read04B: cold read of SKILL.md "### Triggers T1–T3 and the re-pin rule" (line 1069)

**Verdict: gap-minor** (class: instruction).

Read rev b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a, detached in the clone
/tmp/Read04B-cENp/fleet/tameshi-shokunin. SKILL.md sha256
c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6 (matches the
served pin). The section runs 1069–1091; the next heading outside fences is
`### Six-case confidence statement (round 8, measured)` at line 1092.

Class: instruction. The section is three trigger → action rules ("re-measure",
"re-run the reproduction under the new revision and record both pins",
"an appended row") plus a stated re-pin rule; two prior cold readers (CR21
round 18, Read15 round 27) also classed it instruction. Its one runnable
command, re-running `bash tools/mutate-and-run.sh --regression` under a new
revision, needs more than 6 minutes (the closest recorded run,
.ufo/waves/round-18/w2/CR21.md, took 529 s before tool setup) and was skipped.
Every cited pointer and record cell was checked instead, under the trace
collector.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read04B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [{"start": 1069, "heading": "### Triggers T1–T3 and the re-pin rule", "class": "instruction", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
    "Instruction not executed: the only command the section names (re-run the reproduction, i.e. tools/mutate-and-run.sh --regression, under the new revision) exceeds the 6-minute cap; recorded duration 529 s plus setup (.ufo/waves/round-18/w2/CR21.md:31). Skipped per the brief; all cited records checked instead.",
    "T1 mado mapping 'd7edaab4… (4/10) → 90d50cdd…' maps onto the HEAD blob; at the round-8 read (ledger :302) the live worktree bytes were dc864c6a with the cell dirty ('stale + drift'). The section does not say so.",
    "T2 'the harness itself moved four times in one day (597e1419 → b56c6e57 → 4dc69ef9 → e3f838d4 → cf41efaa)': two of the four, 4dc69ef9 and e3f838d4, were uncommitted working-tree writes (plans/round-8.plan.md:69-74; plans/round-7-record-draft.md:115), not commits; the section does not distinguish.",
    "'Both have moved again since' is undated; the claim holds (snapshot :1175-1186 and :1406-1417 show tsukuroi af8adf15/10452443 and mado 12c8f08a→93e43f8f; the ledger :331 row records mado 7da4ec50), but carries no read date.",
    "Paraphrase at :811-812: the section writes 'A moved pin is never re-interpreted against the new bytes'; SKILL.md:811-812 reads 'A moved substrate needs a re-pin, never a re-interpretation of the old table'. Same rule, different words (carried from ReRead07 MG4)."
  ],
  "commands_executed": [
    "python3 tools/trace-inputs.py --root /tmp/Read04B-cENp/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read04B-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/waves/round-16/w2/RerunSweep.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/fleet-kill-rate-ledger.md",
    "python3 tools/trace-inputs.py --root /tmp/Read04B-cENp/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read04B-2.json -- bash -c '<sed line-range reads over the files listed in inputs plus grep -n for 0673d2e5/89722ddb and moved-again evidence>'"
  ],
  "opened": [".ufo/evidence/round-16/coldread/SKILL.snapshot.md", ".ufo/waves/round-16/w2/RerunSweep.md", ".ufo/waves/round-16/w3/RX5.md", ".ufo/waves/round-17/w1/C02LessonCarry.md", ".ufo/waves/round-18/w2/CR21.md", ".ufo/waves/round-27/residual/ReRead07.md", ".ufo/waves/round-27/w1/Read15.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/mutation-case-kumitate-claims.md", "corpus/knowledge/mutation-case-mado-verify.md", "corpus/knowledge/service-optin-protocol.md", "corpus/lessons/round-16-verifier-spotcheck.md", "plans/round-6-record-draft.md", "plans/round-7-record-draft.md", "plans/round-8-record-draft.md", "plans/round-8.plan.md"],
  "inputs": {
    ".ufo/evidence/round-16/coldread/SKILL.snapshot.md": "97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580",
    ".ufo/waves/round-16/w2/RerunSweep.md": "8b03036e4942ee5b5b1680c25219f0e4c006a2aa58ef4b8a01bc450df53cdbc1",
    ".ufo/waves/round-16/w3/RX5.md": "b1633f97552696cb974cf9a255e2af3ae4909bda5f7d371f69ba451dcf532f4d",
    ".ufo/waves/round-17/w1/C02LessonCarry.md": "de8a4f2654f17428a07337bd287bcaf9c961924cf009be5b2b8156dc5345150e",
    ".ufo/waves/round-18/w2/CR21.md": "105703f5e6a767d61df7b48378b77955b67165098151ed88cdb790754ccce4f3",
    ".ufo/waves/round-27/residual/ReRead07.md": "683334bbcb3cde4e5a487105e121727c4cef68a7bf92033fbae6b706d1b9c363",
    ".ufo/waves/round-27/w1/Read15.md": "776fb28ef4fa9fffc21a9e00b4c055b38f97919e0b07250fdf538e2c7e67a05f",
    "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
    "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
    "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
    "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
    "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
    "plans/round-6-record-draft.md": "d146cc6171dc3e60b45a130fd29a0501269bd2272e467b0a1faab28c5696315e",
    "plans/round-7-record-draft.md": "9fed2565ca13ea63c5b23e81db01b4458e67db22aeef8791461cc8d3eb72eb2f",
    "plans/round-8-record-draft.md": "20218607d817f7fe456794da677dba2ce83439aa871a83697effc034e724235d",
    "plans/round-8.plan.md": "7e53c9d89b4887a482816639c6678346e8ed500137eefbcae6cac8997cc0358e"
  },
  "external_inputs": {},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read04B-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read04B-2.json"]}]}
```

## What I checked

- **T1**: tsukuroi `084951be…` (6/10) → `bba6cdf6…` and mado `d7edaab4…` (4/10)
  → `90d50cdd…` match the round-8 pin table at ledger :301-302 (dated
  2026-10-14T19:21:00Z) and the later SKILL snapshot rows :1046-1047, :1101-1102.
  "Both have moved again since" is corroborated by the snapshot's later reads
  (:1175-1176, :1406-1407) and the ledger's round-9 row (:331, mado `7da4ec50…`).
- **T2**: `RerunSweep.md:19-23` records the tool at c699c8c as `89722ddb…` and
  says the re-run reproduced the recorded table (10/10 identical verdicts and
  mutant sha256s) — the "reproduced case 7" claim (js-round-gate, ledger leg 7).
  `0673d2e5…` is confirmed as the later regression/selftest runner
  (round-16-verifier-spotcheck.md:61-62; RX5.md:44,53; C02LessonCarry.md:57).
  Attribution "(corrected round 18)" holds: `git log -S 'corrected round 18'`
  shows the marker landed at 9ee1c80 (round-18 wave-2 corrections), and
  "(corrected round 27, seat Read15)" holds (Read15.md documents the pin fix;
  `git log -S '89722ddb'` shows the runner sha entered the line at b1cc95e1).
- **mado re-run**: `service-optin-protocol.md:232` records "SCR-T6 re-ran the
  spec under `b56c6e57…`: 4/10, all ten mutant shas identical";
  `plans/round-6-record-draft.md:164-167,243-262` gives the same run with
  workdir `/tmp/w6-scr-t6-mado-sweep` — a scratch path, nowhere retained in the
  repo, matching "scratch not retained". `mutation-case-mado-verify.md:17-23`
  records "whether the new revision reproduces this table is **U** (§7)" —
  "keeps it U" holds (:199-200, :230-231 same).
- **Four-move chain**: `597e1419` → `b56c6e57` (I1 incident, mado note :17-23)
  → `4dc69ef9` → `e3f838d4` → `cf41efaa` (plans/round-8.plan.md:69-74;
  round-7-record-draft.md:115; ledger :281 names cf41efaa the r7-1 harness).
  Order and dates hold; two were working-tree writes, unrecorded as such here.
- **T3**: ledger :170-173 reads "as an appended row, not an edit of §1–§4" —
  cited range verified verbatim.
- **Re-pin rule**: SKILL.md :811-812 states the same rule the section
  paraphrases; `moved=0 stale=0` completeness and "drift is never manufactured"
  are consistent with the page's own drift-cell handling (:1186-1193).
- **Replay receipt**: ledger :281 verbatim `REGRESSION: PASS (cases=4
  passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, every leg
  `match=10/10 flips=0`; `mutation-case-kumitate-claims.md:316-317` gives
  19:14:16Z and rc 0; `plans/round-8-record-draft.md:186` corroborates the run
  time. The corrected stamp (was 19:15:54Z per ReRead07 finding 2) now matches
  the primary record.

No wrong expectations; the five minor gaps above are inherited precision
issues, two of them (undated "moved again", uncommitted-write ambiguity) first
listed by ReRead07 and still present at this revision.

No tools installed; nothing outside the report and the two trace receipts
written.

COLDREAD Read04B: gap-minor
