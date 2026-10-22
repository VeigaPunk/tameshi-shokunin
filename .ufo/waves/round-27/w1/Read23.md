# Read23 cold read: SKILL.md:1380 "### The map — where a reader enters, artifact by artifact"

Verdict: gap-minor (class: record). Pinned rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95. The section is the table at SKILL.md:1380-1395. It ends before `### Boundary readings, executed by this lane` at :1396.

Receipts are /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-1.json to Read23-34.json. "Read23-N" below means receipt N. All 34 receipts show rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, exit 0, no untracked reads and no live-lane reads.

## Why class record

The section names artifacts, says what each holds, and says when to read it. It does not tell a reader to run a command. Its one command-like line is advice to use tools/mutate-and-run.sh for "any sweep or replay", so it is a record.

## What checks out

- Existence. Every path in the table exists at the pinned rev: the nine mutation-case notes, the 34 knowledge notes that corpus/README.md names, operator-runbook.md, fleet-kill-rate-ledger.md, service-limits.md, service-optin-protocol.md, fleet-suite-census.md, service-standing-state.md, closeout-r11.md, tools/mutate-and-run.sh, plans/completion-evidence.md and plans/round-11.plan.md. Read23-8, -11, -13, -14, -15, -28.
- Runbook. The headings for §0, §2, §3 ("six-case ledger"), §4, §5, §6 ("the cadence"), §7 and §10 match the row. The title carries T10-1. The renderer rule is at operator-runbook.md:8-10 and points to SKILL.md:1249-1254. The row's pointer SKILL.md:1294-1297 holds the same rule. Read23-1, Read23-21, and a read of SKILL.md.
- Compact refusals table. SKILL.md:1246-1270 has rows a to j. service-limits.md:46-55 carries the same ten rows. Read23-3, and a read of SKILL.md.
- Ledger. fleet-kill-rate-ledger.md:4-5 and §0 at :21-40 give the row columns: suite, kill-rate with composition, survivors, hardened, last sweep and pin. Read23-2, Read23-20.
- Ledger byte freeze. The §1-§4 block, taken between the "## 1." and "## 5." headings, has digest d2ae445332ddc36a in all nine commits that touch the file, from 9f1d3c3 (2026-10-14) to 9ee1c80 (2026-10-20). Read23-27, and the external_inputs entries. The file's own rule is "never as an edit of §1–§4" (:312). The words "byte-frozen" are the section's paraphrase, and the history supports them.
- Protocol. service-optin-protocol.md has §1 request shape (the re-pin rule is at :62), §2 read-only guarantees and §4 report shape. Read23-4.
- Census and standing state. fleet-suite-census.md §5 is the standing offer and its queue (Read23-5). service-standing-state.md §0-§3 cover fleet-visible, lane-owned and handoff conditions, and §4 holds SC1 to SC3 (Read23-6).
- Mutation notes. Round placement matches the row. kimi-census (round 2), kagi-census (round 3), tsukuroi-census (round 5), mado-verify (round 6), kagi-checklist (round 8) and kumitate-claims (round 8) make six. kumitate-round-gate (round 16), kumitate-sources-check (round 18) and kumitate-cite-check (round 26) bring the count to nine (Read23-8, Read23-9). Each note has a verdict table of 13 to 54 table rows (Read23-17) and a survivor section (Read23-8).
- Tool. tools/mutate-and-run.sh:2004-2005 parse --selftest and --regression (Read23-10). The header at :83 reads "r10-2 six legs; r16 seven; r18 eight; r26 nine". The regression registry has nine entries at :1386-1426, and regression_specs at :657 writes "the nine embedded case specs" (Read23-10, Read23-24). Replay materializes blobs from git (:9-10, :116, :1152-1156).
- Eighth leg. The case-8 errata ER8-1 (corpus/knowledge/mutation-case-kumitate-sources-check.md:226-231) records the leg installed since 58e5d53. That commit is dated 2026-10-20 (Read23-27). This matches "eight since round 18".
- Plans. Record drafts exist for rounds 4 to 10, plans exist for rounds 2 to 11, and no round-11 record file exists (Read23-11). completion-evidence.md has "## One line per round" (:27) and "## Debts" (:68) (Read23-12).
- LOG.md:316-317 reads "discharge. Same dispatch shape as rounds 1–10 — the lane deliverables in / this repo ARE the wave record (no `.ufo/waves/tameshi-r11-*` directory);". This matches the row's "wave deliverables are the record". Checked by git show; recorded in external_inputs.
- SCORECARD.md:5 says axes "will be pinned with their counting commands". The move log has 13 rows at lines 12-24 (git show; external_inputs).

## Findings, by severity (all minor; no blocking gap; no wrong expectation)

1. Reproduce wording. Six of the nine case notes have a "Reproduce" heading: kagi-census :208, kagi-checklist :275, kimi-census :148, kumitate-claims :347, mado-verify :262 and tsukuroi-census :344. The three newest notes, kumitate-round-gate, kumitate-sources-check and kumitate-cite-check, have no such heading and no fenced blocks (Read23-18, Read23-19). Each gives its replay route in prose instead. The suite command is in §0 (round-gate.md:21, sources-check.md:23, cite-check.md:21-22). The tool's --regression leg is named in round-gate.md:119, in sources-check.md:3 and in cite-check.md:3, with cite-check.md:59-62 also describing the replay. The row should name that route for cases 7 to 9 (Read23-25, -29, -31, -33, -34).
2. Case-8 body text superseded by errata, unflagged. mutation-case-kumitate-sources-check.md:150-163 still reads "non-equivalence PENDING". Line 174 still reads "not installed at base". ER8-1 (:226-231) records the install, and ER8-2 (:232-240) records the off-suite probes for all five survivors. The content is held. The row does not say the body is superseded (Read23-8, -26, -30, -31, -32).
3. Runbook body is round-10 text. operator-runbook.md:173 and :374 say the regression harness carries four legs and that cases 5 and 6 are not embedded. At this rev the tool embeds nine legs (see Tool above). corpus/README.md:98 already lists "Operator runbook four-leg lines" as still open. The row's renderer rule covers divergence in general but does not warn about these lines (Read23-7, -21, -22, -10, -24).
4. "One row per note" is approximate. All 34 notes are named (Read23-15). Five notes have a second appended row: gates-survey-kumitate (corpus/README.md:7 and :10), gates-survey-kagi (:8 and :11), verification-patterns-fleet (:9 and :12), witness-scoped-kill-verdict (:61 and :128) and incremental-pin-disposition (:152 and :185). The rows sit in appended tables from :5 to :422, not in one table (Read23-15, Read23-16).
5. "Boundaries" has no section behind it in the protocol row. service-optin-protocol.md has no boundaries heading. The word "boundary" appears only at :168, :177 and :178 (Read23-23). The page's own boundaries section is SKILL.md:858.
6. "With their counting commands" holds for some rows only. Of the 13 SCORECARD move-log rows at lines 12-24, five carry a backticked grep, wc, python3 or git command. Counted over git show output. The other rows state counts in prose.
7. Dating. plans/completion-evidence.md:16 says the pack is "uncommitted at this write". That was true at round 11. At 2227d83 the file is tracked (Read23-28 hashes the checked-out copy). The parent heading dates the row, so this is a note rather than an error.

## Outside this item (observed, not scored)

- Compact versus detail anchors. SKILL.md:1258 (compact row a) cites fleet-suite-census.md:277-286. service-limits.md:46 (detail row a) cites :269-275 and :277. Compact row e cites PROVINCE.md:14-18, while the detail cites PROVINCE.md:16-18. SKILL.md:1253-1254 says a divergence between the two is "the finding, never smoothed". Read23-3, and a read of SKILL.md:1256-1267.
- tools/mutate-and-run.sh:175 still sets VERSION to "mutate-and-run.sh r10-2" while nine legs are embedded (Read23-10).
- service-standing-state.md:61 says "currently 9 rows covering 6 of 16 knowledge notes". That is a round-10 figure. corpus/README.md now names all 34 notes (Read23-6, Read23-15).

## Smallest safe correction (for the L1; nothing was edited)

1. In the mutation-case row, after "reproduce sections", add: "(cases 7-9 give their replay as tools/mutate-and-run.sh --regression in the header or §5, not under a Reproduce heading)".
2. In the runbook row, add: "round-10 snapshot; its §2 and §7 four-leg lines predate the nine-leg tool (corpus/README.md:98)".
3. In the protocol row, replace "boundaries" with "read-only guarantees and owner-hardens rules (§2-§3)".

## Residual risk

A reader who does not read the errata or the tool header could take the runbook's four-leg text or the case-8 PENDING text as current. The table's pointers themselves resolve.

## Verification gaps

- I did not run --selftest or --regression. I read the flags and the embedded legs, and I did not replay them.
- The case notes were checked by headings, table-row counts, keyword searches and the specific lines cited. I did not read each verdict table or survivor analysis in full.
- Runbook §1, §5, §6, §8, §9 and §10 were checked only by heading.
- The README rows were checked by note name and by listing the rows, not by their content.
- The "Read it when" column is advice and was not scored.
- LOG.md and SCORECARD.md were read only through git show, as the brief requires. The SCORECARD count covers lines 12-24 only.
- The ledger check covers only the block between "## 1." and "## 5.".

## Tooling

No installs or updates. strace 7.2 (/usr/bin/strace) and Python 3.14.8 were already present. Checked with `command -v strace`, `strace -V` and `python3 --version`. No pacman, uv or npm action was taken.

Untraced commands, disclosed: git show of LOG.md, SCORECARD.md and the nine ledger revisions (sanctioned reads, hashed into external_inputs); a count of the SCORECARD move-log rows over git show output; a summary of my own receipts; and a check that the JSON block below matches my receipts.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read23",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 1380,
      "heading": "### The map \u2014 where a reader enters, artifact by artifact",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Reproduce wording: six of nine mutation-case notes have a Reproduce heading (kagi-census :208, kagi-checklist :275, kimi-census :148, kumitate-claims :347, mado-verify :262, tsukuroi-census :344). Cases 7-9 (kumitate-round-gate, kumitate-sources-check, kumitate-cite-check) have no such heading and no fenced blocks; they give the suite command in section 0 and the tool --regression leg in a header or section 5 (round-gate.md:119, sources-check.md:3, cite-check.md:3 and :59-62). The row should name that route.",
        "Case-8 body text superseded by appended errata but not flagged: mutation-case-kumitate-sources-check.md:150-163 still reads non-equivalence PENDING and :174 reads not installed at base; ER8-1 (:226-231) records the install and ER8-2 (:232-240) records the off-suite probes. The content is held; the row does not say the body is superseded.",
        "Runbook body is round-10 text: operator-runbook.md:173 and :374 say the regression harness carries four legs with cases 5/6 not embedded, while the tool embeds nine legs (tools/mutate-and-run.sh :83, :657, registry :1386-1426) and corpus/README.md:98 lists the runbook four-leg lines as still open. The renderer rule covers divergence in general but not these lines.",
        "One row per note is approximate: all 34 notes are named in corpus/README.md, but gates-survey-kumitate (:7, :10), gates-survey-kagi (:8, :11), verification-patterns-fleet (:9, :12), witness-scoped-kill-verdict (:61, :128) and incremental-pin-disposition (:152, :185) each have a second appended row, and the rows sit in appended tables from :5 to :422.",
        "Boundaries in the protocol row has no section behind it: service-optin-protocol.md has no boundaries heading and the word boundary appears only at :168, :177 and :178. The page's own boundaries section is SKILL.md:858.",
        "With their counting commands holds for some rows only: of the 13 SCORECARD move-log rows at lines 12-24, five carry a backticked grep, wc, python3 or git command; the rest state counts in prose.",
        "Dating: plans/completion-evidence.md:16 says uncommitted at this write, which was true at round 11; at 2227d83 the file is tracked. The parent heading dates the row."
      ],
      "commands_executed": [
        "grep -n -E '^#|six-case|nine-case|T10-1|anchored source' corpus/knowledge/operator-runbook.md",
        "grep -n -E '^#|byte-frozen|one row|appended' corpus/knowledge/fleet-kill-rate-ledger.md",
        "grep -n -E '^#|^\\| *[a-j] *\\||T9-2|trigger' corpus/knowledge/service-limits.md",
        "grep -n -E '^#|re-pin|read-only|report shape|request shape' corpus/knowledge/service-optin-protocol.md",
        "grep -n -E '^#|offer|queue|surveyed' corpus/knowledge/fleet-suite-census.md",
        "grep -n -E '^#|SC[1-3]|fleet-visible|lane-owned|handoff' corpus/knowledge/service-standing-state.md",
        "grep -n -E '^#|^\\*\\*|^- \\*\\*|^[A-Za-z].{0,80}$' corpus/README.md",
        "grep -n -E '^#' corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md",
        "grep -n -m 3 -E '[Rr]ound [0-9]+' corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md",
        "grep -n -E 'VERSION|--selftest|--regression|git show|git cat-file|git archive|materiali' tools/mutate-and-run.sh",
        "ls plans",
        "grep -n -E '^#|per-round|debt|uncommitted' plans/completion-evidence.md",
        "grep -n -E '^#' corpus/knowledge/closeout-r11.md",
        "grep -n -E '^#' plans/round-11.plan.md",
        "python3 -c 'import os\nr=open('\"'\"'corpus/README.md'\"'\"',encoding='\"'\"'utf-8'\"'\"').read()\nnotes=sorted(f for f in os.listdir('\"'\"'corpus/knowledge'\"'\"') if f.endswith('\"'\"'.md'\"'\"'))\nprint('\"'\"'knowledge_notes'\"'\"', len(notes))\nprint('\"'\"'readme_table_rows'\"'\"', sum(1 for l in r.splitlines() if l.startswith('\"'\"'|'\"'\"')))\nprint('\"'\"'notes_not_named_in_readme'\"'\"', [n for n in notes if n not in r])'",
        "grep -n '^|' corpus/README.md",
        "grep -c '^|' corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md",
        "grep -n -i reproduc corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md",
        "grep -c '^```' corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md",
        "sed -n 1,40p corpus/knowledge/fleet-kill-rate-ledger.md",
        "sed -n 1,12p corpus/knowledge/operator-runbook.md",
        "grep -n -i -E 'nine|four|ER-R3' corpus/knowledge/operator-runbook.md",
        "grep -n -i boundar corpus/knowledge/service-optin-protocol.md",
        "grep -n -m 6 specs tools/mutate-and-run.sh",
        "python3 -c 'spec=[('\"'\"'corpus/knowledge/mutation-case-kumitate-round-gate.md'\"'\"',15,33),('\"'\"'corpus/knowledge/mutation-case-kumitate-sources-check.md'\"'\"',17,46),('\"'\"'corpus/knowledge/mutation-case-kumitate-cite-check.md'\"'\"',15,32)]\nfor p,a,b in spec:\n    L=open(p,encoding='\"'\"'utf-8'\"'\"').read().splitlines()\n    print('\"'\"'=='\"'\"',p,a,b)\n    for i in range(a-1,b): print(i+1, L[i][:200])'",
        "python3 -c 'L=open('\"'\"'corpus/knowledge/mutation-case-kumitate-sources-check.md'\"'\"',encoding='\"'\"'utf-8'\"'\"').read().splitlines()\nfor i in range(149,168): print(i+1, L[i][:200])\nprint('\"'\"'PENDING_hits'\"'\"', [i+1 for i,l in enumerate(L) if '\"'\"'PENDING'\"'\"' in l])'",
        "python3 -c 'import subprocess, hashlib\np = '\"'\"'corpus/knowledge/fleet-kill-rate-ledger.md'\"'\"'\nlog = subprocess.run(['\"'\"'git'\"'\"', '\"'\"'log'\"'\"', '\"'\"'--format=%h %ad'\"'\"', '\"'\"'--date=short'\"'\"', '\"'\"'--'\"'\"', p], capture_output=True, text=True).stdout.splitlines()\nprint('\"'\"'commits_touching_ledger'\"'\"', len(log))\nprev = None\nfor line in reversed(log):\n    h, d = line.split('\"'\"' '\"'\"', 1)\n    t = subprocess.run(['\"'\"'git'\"'\"', '\"'\"'show'\"'\"', h + '\"'\"':'\"'\"' + p], capture_output=True, text=True).stdout\n    a = t.find('\"'\"'## 1. Measured'\"'\"'); b = t.find('\"'\"'## 5. The instrument'\"'\"')\n    blk = t[a:b] if (a >= 0 and b > a) else None\n    dig = hashlib.sha256(blk.encode()).hexdigest()[:16] if blk else '\"'\"'NO-BLOCK'\"'\"'\n    print(h, d, dig, '\"'\"'same'\"'\"' if dig == prev else '\"'\"'CHANGED'\"'\"')\n    prev = dig'",
        "sha256sum corpus/knowledge/operator-runbook.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-limits.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/fleet-suite-census.md corpus/knowledge/service-standing-state.md corpus/knowledge/closeout-r11.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md corpus/README.md tools/mutate-and-run.sh tools/trace-inputs.py plans/completion-evidence.md plans/round-11.plan.md",
        "sed -n 117,133p corpus/knowledge/mutation-case-kumitate-round-gate.md",
        "sed -n 165,184p corpus/knowledge/mutation-case-kumitate-sources-check.md",
        "grep -n -i install corpus/knowledge/mutation-case-kumitate-sources-check.md",
        "sed -n 221,240p corpus/knowledge/mutation-case-kumitate-sources-check.md",
        "sed -n 54,62p corpus/knowledge/mutation-case-kumitate-cite-check.md",
        "grep -n -i regression corpus/knowledge/mutation-case-kumitate-cite-check.md"
      ],
      "opened": [
        "corpus/knowledge/operator-runbook.md",
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "corpus/knowledge/service-limits.md",
        "corpus/knowledge/service-optin-protocol.md",
        "corpus/knowledge/fleet-suite-census.md",
        "corpus/knowledge/service-standing-state.md",
        "corpus/knowledge/closeout-r11.md",
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/knowledge/mutation-case-kagi-checklist.md",
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md",
        "corpus/knowledge/mutation-case-kumitate-claims.md",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md",
        "corpus/knowledge/mutation-case-kumitate-sources-check.md",
        "corpus/knowledge/mutation-case-mado-verify.md",
        "corpus/knowledge/mutation-case-tsukuroi-census.md",
        "corpus/README.md",
        "tools/mutate-and-run.sh",
        "tools/trace-inputs.py",
        "plans/completion-evidence.md",
        "plans/round-11.plan.md"
      ],
      "inputs": {
        "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0",
        "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
        "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
        "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952",
        "corpus/knowledge/closeout-r11.md": "cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265",
        "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
        "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7",
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
        "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
        "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38",
        "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
        "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604",
        "corpus/README.md": "33915658d9ef1ed3b93ed0cf58ba5b341bc58facc5d1ff73574e6ddd297dcb79",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "plans/completion-evidence.md": "8e0485655a4801b9070bfa7dd688e774fed1a2e8b1692b046109ad83ebe2a3ef",
        "plans/round-11.plan.md": "068578f198367b79b14fea95d9db550828908e345e5cbc161cabf0e4bea744f7"
      },
      "external_inputs": {
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:LOG.md": "b28a2118a43b1ae50057b7a0239569ceeeda9781fa885eb92151dc0dd194ab9a",
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:SCORECARD.md": "a7aa9ab587fd19fd7af51381f2698d63019e7c3a513f57e5918e0d2003510c64",
        "tameshi-shokunin@9ee1c8046295baf6c133c8d43b8315d562498aea:corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "tameshi-shokunin@58e5d53d6a638fb72042d1f6607b24018aa299a8:corpus/knowledge/fleet-kill-rate-ledger.md": "1c06c6ba1eee45dd2aed540c9d70e2e361d05d9f82acc43afe64c8964ef38611",
        "tameshi-shokunin@2a22adeb7d1de5e7189e62ce41ac679d71a97b44:corpus/knowledge/fleet-kill-rate-ledger.md": "ac7f69d928e5ba0fb687821c2a2c0900e1375a8454901a285874735e35c21033",
        "tameshi-shokunin@34907080f6adda2b18ea13eff23822671cc6930e:corpus/knowledge/fleet-kill-rate-ledger.md": "8c8844c50aeac39f4c6d521c1f9e2a027cb55edc6c9d5a3d4242403f8f02a7fe",
        "tameshi-shokunin@c699c8c36d6e4eca4b796b81a8247904aa145ec8:corpus/knowledge/fleet-kill-rate-ledger.md": "918a56d9c9ffb57b1c2caf395955bc320878d2107165d7d5d711ebbd89799f22",
        "tameshi-shokunin@4acc607dfd79f19d508bd50cdd06b77269fccd1d:corpus/knowledge/fleet-kill-rate-ledger.md": "8f6daa81b3d86352e88f3f029a9875aa38bb5b1f4fa415a67365aa0f0501f257",
        "tameshi-shokunin@b8eb96e1d0333a9878e57d834c6213121d5575b9:corpus/knowledge/fleet-kill-rate-ledger.md": "2f25c51e3e0a7851d2c6ece35ef9107aff3d36ad4bedd069ac921e1efddbd432",
        "tameshi-shokunin@c611d5d52d1dfe9bf1184768ba4aef4e414a4a0f:corpus/knowledge/fleet-kill-rate-ledger.md": "71bc15e365a3574f48d22c70cdb6d32f6511d5532187886770006e4c6f7b9302",
        "tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:corpus/knowledge/fleet-kill-rate-ledger.md": "e08efe79bb58c85002c37db486a0b88ff85e51c5fb664a6c41f108839dc05cc5"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-13.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-16.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-17.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-18.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-19.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-20.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-21.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-22.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-23.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-24.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-25.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-26.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-27.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-28.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-29.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-30.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-31.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-32.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-33.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read23-34.json"
      ]
    }
  ]
}
```

Plain-English note. I cloned the lane at 2227d83 into /tmp, read the section, and ran 34 traced commands. Each one wrote a receipt with the pinned rev, exit 0 and no live-lane reads. I checked every named artifact for existence, headings, counts, round placement and the specific lines the row cites. My confidence is high on existence, headings, counts and round placement, and high that the runbook body is stale. It is medium on how strictly "reproduce sections" should be read, because cases 7 to 9 give their replay as a command rather than as a heading. The section is a record with pointers, and most of it holds. Three wording points need fixing, so the verdict is gap-minor rather than verified-record.

COLDREAD Read23: gap-minor
