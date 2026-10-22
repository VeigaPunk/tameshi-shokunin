# ReRead07: cold read of "Triggers T1–T3 and the re-pin rule" (SKILL.md:1069)

**Verdict: wrong-expectation.** Class: `record`. Revision read: b1cc95e1fb62532646d74e2863770c4fed0851cc. Page sha256: fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f.

Two claims in the section do not hold against the lane's own records at b1cc95e1: the statement that the mado spec under b56c6e57 "was never re-cut", and the round-8 replay receipt time 19:15:54Z. Most other checkable facts hold. Five minor gaps are listed below and in the JSON.

## Findings, by severity

1. **Wrong expectation, SKILL.md:1078 ("mado under b56c6e57… was never re-cut (U, mutation-case-mado-verify.md:17-23)").** The cited note lines do not say "never". They say the reproduction under b56c6e57 is U (mutation-case-mado-verify.md:22-23; also :199-200 and :230-231). The lane's corpus records a re-run: corpus/knowledge/service-optin-protocol.md:232 reads "SCR-T6 re-ran the spec under b56c6e57…: 4/10, all ten mutant shas identical". plans/round-6-record-draft.md:164-167 records the same run, and its section C.3 (lines 243-262) gives MUTATE_TOOL sha256=b56c6e57…, killed=4 survived=6, kill-rate 40%. The scratch directory /tmp/w6-scr-t6-mado-sweep (plans/round-6-record-draft.md:251) is not retained in the repo, so the run is recorded but has no retained receipt. corpus/knowledge/operator-runbook.md:291-292 and plans/round-8.plan.md:26-29 still cite a re-cut under b56c6e57 as the T2 precedent. The flat negative contradicts these records.
   Smallest correction: say that one re-run by SCR-T6 is recorded (4/10, mutant shas identical, service-optin-protocol.md:232) with its scratch not retained, and that the mado note leaves the reproduction U.

2. **Wrong expectation, SKILL.md:1087 ("The round-8 replay receipt (tool cf41efaa…, four legs; 19:15:54Z, rc 0)").** No file under corpus/, tools/ or plans/ at b1cc95e1 contains "19:15:54". The same four-leg PASS for cf41efaa is retained at 19:14:16Z: corpus/knowledge/fleet-kill-rate-ledger.md:281, corpus/knowledge/mutation-case-kumitate-claims.md:316-317, and plans/round-8-record-draft.md:186 ("runs 4/4 PASS (19:14:16Z, this note's run)"). The 19:58:18Z re-run is at fleet-kill-rate-ledger.md:341. The 19:15:54Z stamp appears only in copies of this section (SKILL.md:1087; .ufo/evidence/round-16/coldread/SKILL.snapshot.md:1087; two skill-versions copies) and in reports that quote it.
   Smallest correction: 19:14:16Z, citing fleet-kill-rate-ledger.md:281 and mutation-case-kumitate-claims.md:316-317.

3. **Minor gaps (non-blocking; full text in the JSON).**
   - MG1: the T1 mado mapping "4/10 -> 90d50cdd" cites the HEAD blob. At the round-8 read the worktree was dirty (dc864c6a, fleet-kill-rate-ledger.md:302). The section does not say so.
   - MG2: 4dc69ef9 and e3f838d4 are working-tree writes (plans/round-8.plan.md:37, 69-74; plans/round-7-record-draft.md:115), not commits. The dates hold. The section does not say two of the four moves were uncommitted.
   - MG3: "both have moved again since" is undated. At the round-9 read tsukuroi's committed blob was still bba6cdf6 (fleet-kill-rate-ledger.md:328). The claim holds now (see below), but it should carry a date.
   - MG4: the paraphrase "A moved pin is never re-interpreted against the new bytes (:811-812)" differs in words from SKILL.md:811-812 ("A moved substrate needs a re-pin, never a re-interpretation of the old table"). Same rule.
   - MG5: the attributions "corrected round 18" and "corrected round 27, seat Read15" were not checked by me.

## What holds (checked against primary records)

- Pins and T1 rows. tsukuroi 165307fe blob 084951be; aa136d69 and 72b038da blobs bba6cdf6. mado eead56b2 blob d7edaab4; 0c20a76f blob 90d50cdd. The six-case rows read 6/10 (SKILL.md:1101) and 4/10 (SKILL.md:1102). Ledger rows 301-302 match the round-8 readings.
- "Both have moved again since", as of 2026-10-22. tsukuroi HEAD b13e991f has blob d17d32a3 (worktree identical, clean). mado HEAD 8e5d9369 has blob 050efc72 (worktree identical, clean). The page's own later table gives tsukuroi af8adf15 blob 10452443 (SKILL.md:1406).
- T2 precedent. RerunSweep.md:19-20 gives the tool at c699c8c as sha256 89722ddb3082…; git history confirms c699c8c36d6e (2026-10-20T10:49:37-03:00) has blob 89722ddb. 0673d2e5 is the later runner: commit 05a224754db3 (2026-10-20T11:18:08-03:00) has blob 0673d2e5, and corpus/lessons/round-16-verifier-spotcheck.md:61-62 gives 0673d2e5 for the regression and selftest receipts. "Reproduced case 7" matches the RerunSweep target (round-gate) and the c699c8c subject "land js-round-gate case 7".
- T3 pointer. fleet-kill-rate-ledger.md:170-173 says the embedding line and case count change "as an appended row, not an edit of §1–§4".
- Re-pin pointer. SKILL.md:811-812 says "A moved substrate needs a re-pin, never a re-interpretation of the old table" (wording differs; see MG4).
- Four harness moves on 2026-10-14. Commits touching tools/mutate-and-run.sh: 597e1419 at 13:57:18 -03:00, b56c6e57 at 15:17:26, cf41efaa at 16:06:31. 4dc69ef9 and e3f838d4 appear as writes in plans/round-8.plan.md:69-74 (15:27:40 and 15:28:38) and plans/round-7-record-draft.md:115 (61305 B at 15:28:38).
- Receipt text. "REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)" and "every leg match=10/10 flips=0" match fleet-kill-rate-ledger.md:281 and mutation-case-kumitate-claims.md:317. The "tool cf41efaa…, rc 0" part holds at 19:14:16Z.
- Policy sentences. "moved=0 stale=0 is a complete outcome" is recorded in plans/round-8.plan.md:123, corpus/knowledge/service-limits.md:86, closeout-r11.md:187 and operator-runbook.md:296. The ledger rule "old tables stand at their revisions" holds (fleet-kill-rate-ledger.md:318).

## Evidence (commands run under the collector, with observed output)

Every command below ran through tools/trace-inputs.py from the clone at b1cc95e1. Receipts are ReRead07-1 to ReRead07-25 in the traces directory named in the JSON. A sample of receipts (ReRead07-7, -8, -22, -23, -24) shows rev b1cc95e1, exit 0 and no live-lane reads.

- Identity (ReRead07-1, -2). `git rev-parse HEAD` printed b1cc95e1fb62532646d74e2863770c4fed0851cc. `git show b1cc95e…:SKILL.md | sha256sum` printed fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f. The heading is line 1069; the next heading, "### Six-case confidence statement", is line 1092.
- Section text (ReRead07-2, ReRead07-25). Line 1078 reads "mado under `b56c6e57…` was never re-cut (U, `mutation-case-mado-verify.md:17-23`); the harness itself moved four times in". Line 1087 reads "The round-8 replay receipt (tool `cf41efaa…`, four legs; 19:15:54Z, rc 0):".
- Anchor lines (ReRead07-2, -3, -4, -5). SKILL.md:811-812 has the re-pin sentence. ledger:170-173 has the appended-row sentence. mado note:17-23 has "Re-pin at 17:46:15Z: sha256 b56c6e57…2bcb" and "whether the new revision reproduces this table is U (§7)". RerunSweep.md:19-20 has "Tool: worktree/tools/mutate-and-run.sh at c699c8c → sha256 89722ddb…".
- Receipt time (ReRead07-8, -10, -25). `git grep -n -e 19:15:54 HEAD -- corpus tools plans` printed nothing. Across all tracked files it matched SKILL.md:1087, the round-16 snapshot copies at line 1087, and reports quoting the line. `git grep` for 19:14:16 and 19:58:18 in corpus/tools/plans matched fleet-kill-rate-ledger.md:281 and :341, mutation-case-kumitate-claims.md:316 and :359, and plans/round-8-record-draft.md:186.
- Mado re-run (ReRead07-4, -10, -15, -16, -18, -19, -20). mutation-case-mado-verify.md:199-200 reads "re-verification under the current b56c6e57… is U". :230-231 reads "reproduction under the current harness revision b56c6e57… is unmeasured". service-optin-protocol.md:232 and plans/round-6-record-draft.md:164-167 and :243-262 record the SCR-T6 run (quoted in Finding 1). `git grep -n -e w6-scr-t6 -e scr-t6- HEAD` returned only plans/round-6-record-draft.md:205, :230, :249, :251, :266. Those are scratch-path references; no retained receipt file exists.
- T1 pins (ReRead07-7, -22). `git -C tsukuroi-shokunin show 165307fe…:tools/tsukuroi-census.sh | sha256sum` gave 084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5. The aa136d69 and 72b038da revisions gave bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55. `git -C mado-shokunin show eead56b2…:tools/mado-verify.sh` gave d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13. The 0c20a76f revision gave 90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd. The 12c8f08a revision gave 7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f.
- Current heads (ReRead07-7, -22, -24). tsukuroi HEAD b13e991fb96972b423b868ba122187f75357368c, blob d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e, `git status --porcelain` empty. mado HEAD 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122, blob 050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1, status empty. The worktree files had the same sha256.
- T2 precedent (ReRead07-5, -6, -21). The commit list (ReRead07-6) has c699c8c36d6e 2026-10-20T10:49:37-03:00 blob 89722ddb3082 "round-16: land js-round-gate case 7" and 05a224754db3 2026-10-20T11:18:08-03:00 blob 0673d2e5374b "round-16: wave-2 repairs".
- Harness chain (ReRead07-6, -17). Commits on 2026-10-14: b58b26fb (597e1419) 13:57:18; 44947154 (b56c6e57) 15:17:26; 9f1d3c33 (cf41efaa) 16:06:31; 606716f7 (75ed934d) 18:28:23. None is 4dc69ef9 or e3f838d4.
- Policy phrase (ReRead07-14). `git grep -n -e 'moved=0 stale=0' -e 'moved=0' HEAD -- corpus tools plans` returned the four notes listed under "What holds".

## Smallest safe correction (recommendation to the owner; not applied)

- SKILL.md:1087: replace "19:15:54Z" with "19:14:16Z", citing corpus/knowledge/fleet-kill-rate-ledger.md:281 and corpus/knowledge/mutation-case-kumitate-claims.md:316-317.
- SKILL.md:1078: replace "mado under `b56c6e57…` was never re-cut (U, `mutation-case-mado-verify.md:17-23`)" with: "mado under `b56c6e57…` has one recorded re-run by SCR-T6 (4/10, all ten mutant shas identical; `corpus/knowledge/service-optin-protocol.md:232`; scratch not retained), and the mado note leaves the reproduction U (`mutation-case-mado-verify.md:17-23`, `:199-200`, `:230-231`)".
- SKILL.md:1079: add that 4dc69ef9… and e3f838d4… were working-tree writes (`plans/round-8.plan.md:69-74`), not commits.
- Optional: date "(both have moved again since)" with the 2026-10-22 heads above.

## Residual risk and verification gaps

- LOG.md, SCORECARD.md and .ufo/evidence/round-21/coldread/ledger.json were not opened by path or under the collector. Every search excluded them by pathspec. LOG.md could hold a later receipt or note that bears on Finding 2 or Finding 1. Absence in corpus/, tools/ and plans/ does not prove absence from those three files.
- Searches covered tracked files at b1cc95e1 only (git grep over HEAD). Untracked files were not searched.
- The SCR-T6 figures are unverified: their scratch directory is not in the repo.
- The sibling heads are live reads from 2026-10-22 and can move.
- I ran no reproduction, no regression run and no sweep. The section names no command, so the record class applies.
- The attributions in MG5 were not checked.

## Tooling

No tools were installed or upgraded. python3 3.14.8, git 2.56.0 and strace 7.2 were already present. No pacman, uv or npm transaction ran.

## Disclosures

- Outside the collector, as step 1 prescribes or as setup: the clone commands (fleet mirror, detached at b1cc95e1); `mkdir -p` for the traces directory in the live lane; `command -v strace`, `strace -V`, `python3 --version` and `git --version`; an early `git rev-parse HEAD` and `git status --porcelain` in the clone (0 entries); an early `sha256sum SKILL.md` in the clone (fce54977…, which ReRead07-2 repeats through git show under the collector).
- Tool reads before the collector: `_read` of tools/trace-inputs.py and ColdreadPilot.md, and early reads of the ledger, the mado note and RerunSweep. An unscoped `_grep` over the clone worktree ran before I knew the three-file exclusion list, so it may have read the bytes of LOG.md, SCORECARD.md or the round-21 ledger.json. Its output did not show their contents, and I quote none of them.
- After the traces, I read my own receipts with the read tool (`?q=` queries on ReRead07-1, -7, -8, -22, -23, -24). That was not during a trace.
- An unscoped `git grep` over HEAD displayed matched lines from other seats' wave reports and page copies (for example .ufo/waves/round-27/w1/Read15.md, .ufo/waves/round-17/w3/RR2.md, .ufo/waves/round-18/w2/CR21.md, and the round-16 snapshot). Those lines were displayed to me before I checked each claim. I did not open those files by path, and every finding above rests on the primary record named.
- No `jj` command ran. No git write command ran in any repository. The receipts and this report are the only files I wrote in the live lane.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ReRead07",
  "skill_sha256": "fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f",
  "read_rev": "b1cc95e1fb62532646d74e2863770c4fed0851cc",
  "sections": [
    {
      "start": 1069,
      "heading": "### Triggers T1\u2013T3 and the re-pin rule",
      "class": "record",
      "verdict": "wrong-expectation",
      "blocking_gaps": [],
      "wrong_expectations": [
        "WE1 (line 1078, T2): 'mado under b56c6e57... was never re-cut (U, mutation-case-mado-verify.md:17-23)' does not hold. The cited lines say only that the reproduction is U; lines 199-200 and 230-231 say the same. The lane corpus records a re-run: corpus/knowledge/service-optin-protocol.md:232 says 'SCR-T6 re-ran the spec under b56c6e57...: 4/10, all ten mutant shas identical'; plans/round-6-record-draft.md:164-167 and section C.3 (lines 243-262) record the same run with killed=4 survived=6. Its scratch /tmp/w6-scr-t6-mado-sweep is not retained in the repo, so the run is recorded but has no retained receipt.",
        "WE2 (line 1087): the round-8 replay receipt is dated 19:15:54Z. No file under corpus/, tools/ or plans/ at b1cc95e1 contains that time. The same four-leg PASS for tool cf41efaa is retained at 19:14:16Z: corpus/knowledge/fleet-kill-rate-ledger.md:281, corpus/knowledge/mutation-case-kumitate-claims.md:316-317 and plans/round-8-record-draft.md:186. The 19:58:18Z re-run is at corpus/knowledge/fleet-kill-rate-ledger.md:341."
      ],
      "minor_gaps": [
        "MG1 (line 1074, T1 mado instance): the section maps mado d7edaab4 (4/10) to 90d50cdd. At the round-8 read the mado worktree was dirty (dc864c6a, corpus/knowledge/fleet-kill-rate-ledger.md:302); 90d50cdd is the HEAD blob. The section does not say it cites the HEAD blob.",
        "MG2 (line 1079, four moves): 4dc69ef9 and e3f838d4 were working-tree writes (plans/round-8.plan.md:37 and 69-74; plans/round-7-record-draft.md:115), not commits. Commits touching tools/mutate-and-run.sh on 2026-10-14 are 597e1419 (13:57:18 -03:00), b56c6e57 (15:17:26) and cf41efaa (16:06:31); no commit has 4dc69ef9 or e3f838d4. The dates hold; the section does not say two moves were uncommitted.",
        "MG3 (lines 1074-1077, both have moved again since): undated. At the round-9 read tsukuroi's committed blob was still bba6cdf6 (corpus/knowledge/fleet-kill-rate-ledger.md:328). As of 2026-10-22: tsukuroi HEAD b13e991f has blob d17d32a3, and mado HEAD 8e5d9369 has blob 050efc72 (worktrees clean); SKILL.md:1406 records tsukuroi blob 10452443 at af8adf15. The claim holds now and should carry a date.",
        "MG4 (line 1083, re-pin rule): 'A moved pin is never re-interpreted against the new bytes (:811-812)' paraphrases SKILL.md:811-812, which says 'A moved substrate needs a re-pin, never a re-interpretation of the old table'. Same rule, different words.",
        "MG5 (provenance): the attributions 'corrected round 18' and 'corrected round 27, seat Read15' were not checked; those seats' records were not used as evidence."
      ],
      "commands_executed": [
        "ReRead07-1: bash -c 'git rev-parse HEAD; git ls-files | grep -E (names only: SCORECARD.md, LOG.md, round-21 coldread ledger.json); git ls-files | wc -l' (exit 0)",
        "ReRead07-2: bash -c 'git show b1cc95e...:SKILL.md | sha256sum; same blob | cat -n | sed -n 806,816p;1067,1092p; same blob | cat -n | grep bash-tsukuroi-census or bash-mado-verify' (exit 0)",
        "ReRead07-3: bash -c 'cat -n corpus/knowledge/fleet-kill-rate-ledger.md | sed -n 166,176p;280,340p' (exit 0)",
        "ReRead07-4: bash -c 'cat -n corpus/knowledge/mutation-case-mado-verify.md | sed -n 14,26p; grep -n for re-cut, recut, b56c6e57, identical and section headings' (exit 0)",
        "ReRead07-5: bash -c 'cat -n .ufo/waves/round-16/w2/RerunSweep.md | sed -n 1,4p;17,25p; sha256sum tools/mutate-and-run.sh; wc -c -l tools/mutate-and-run.sh' (exit 0)",
        "ReRead07-6: python3 -c: git log --format over commits touching tools/mutate-and-run.sh, sha256 of each committed blob (exit 0; 10 commits)",
        "ReRead07-7: python3 -c: git -C sibling show of six pinned blobs with sha256; sibling HEAD rev and blob sha; git status --porcelain of the sibling census and verify files (exit 0)",
        "ReRead07-8: bash -c: git grep -l over HEAD for 19:15:54, b56c6e57, 4dc69ef9, e3f838d4, 0673d2e5, 597e1419, 89722ddb, pathspec excluding LOG.md, SCORECARD.md and round-21 ledger.json; git grep -n for 19:15:54 (exit 0)",
        "ReRead07-9: bash -c: git grep -n for 4dc69ef9 and e3f838d4 in corpus, tools, plans; git grep -l for both over HEAD with excludes; git grep -n for 0673d2e5 in corpus, tools, plans, .ufo/waves/round-16 (exit 0)",
        "ReRead07-10: bash -c: git grep -n for 19:15:54 in corpus, tools, plans (no hits); for 19:14:16 and 19:58:18; for b56c6e57 (exit 0)",
        "ReRead07-11: bash -c: cat -n RerunSweep.md | sed -n 25,60p; grep -n -o for runner, round-gate and case 7 tokens (exit 0)",
        "ReRead07-12: bash -c: cat -n mutation-case-mado-verify.md | sed -n 196,202p;228,234p; cat -n fleet-kill-rate-ledger.md | sed -n 338,350p (exit 0)",
        "ReRead07-13: bash -c: cat -n corpus/knowledge/mutation-case-kumitate-claims.md | sed -n 312,320p (exit 0)",
        "ReRead07-14: bash -c: git grep -n for SCR-T6 over HEAD in corpus, tools, plans, .ufo with excludes; git grep -n for moved=0 stale=0 and moved=0 in corpus, tools, plans (exit 0)",
        "ReRead07-15: bash -c: cat -n corpus/knowledge/service-optin-protocol.md | sed -n 122,130p;218,236p (exit 0)",
        "ReRead07-16: bash -c: cat -n plans/round-6-record-draft.md | sed -n 108,111p;162,168p (exit 0)",
        "ReRead07-17: bash -c: cat -n plans/round-8.plan.md | sed -n 26,38p;58,74p; cat -n plans/round-8-record-draft.md | sed -n 184,188p; cat -n plans/round-7-record-draft.md | sed -n 113,116p (exit 0)",
        "ReRead07-18: bash -c: cat -n corpus/knowledge/operator-runbook.md | sed -n 288,294p (exit 0)",
        "ReRead07-19: bash -c: cat -n plans/round-6-record-draft.md | sed -n 230,262p (exit 0)",
        "ReRead07-20: bash -c: git grep -n for w6-scr-t6 and scr-t6- over HEAD with excludes; git grep -n for 4/10 in .ufo/evidence/round-6 and .ufo/waves/round-6; git ls-tree -d for round-5 and round-6 evidence dirs (exit 0)",
        "ReRead07-21: bash -c: cat -n corpus/lessons/round-16-verifier-spotcheck.md | sed -n 58,68p;230,240p (exit 0)",
        "ReRead07-22: python3 -c: git -C sibling show of nine pinned or HEAD blobs with full sha256 (exit 0)",
        "ReRead07-23: sha256sum of the fourteen lane files listed under inputs (exit 0)",
        "ReRead07-24: sha256sum of the two live sibling worktree files through the fleet mirror (exit 0)",
        "ReRead07-25: bash -c: cat -n fleet-kill-rate-ledger.md | sed -n 169,173p;281p;296,304p;324,331p;341p; git show b1cc95e...:SKILL.md | cat -n | sed -n 1078p;1087p (exit 0)"
      ],
      "opened": [
        "SKILL.md",
        "tools/trace-inputs.py",
        "tools/mutate-and-run.sh",
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "corpus/knowledge/mutation-case-mado-verify.md",
        "corpus/knowledge/mutation-case-kumitate-claims.md",
        "corpus/knowledge/service-optin-protocol.md",
        "corpus/knowledge/operator-runbook.md",
        "corpus/lessons/round-16-verifier-spotcheck.md",
        "plans/round-6-record-draft.md",
        "plans/round-7-record-draft.md",
        "plans/round-8.plan.md",
        "plans/round-8-record-draft.md",
        ".ufo/waves/round-16/w2/RerunSweep.md",
        ".ufo/waves/round-26/w1/ColdreadPilot.md"
      ],
      "inputs": {
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
        "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
        "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
        "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
        "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
        "plans/round-6-record-draft.md": "d146cc6171dc3e60b45a130fd29a0501269bd2272e467b0a1faab28c5696315e",
        "plans/round-7-record-draft.md": "9fed2565ca13ea63c5b23e81db01b4458e67db22aeef8791461cc8d3eb72eb2f",
        "plans/round-8.plan.md": "7e53c9d89b4887a482816639c6678346e8ed500137eefbcae6cac8997cc0358e",
        "plans/round-8-record-draft.md": "20218607d817f7fe456794da677dba2ce83439aa871a83697effc034e724235d",
        ".ufo/waves/round-16/w2/RerunSweep.md": "8b03036e4942ee5b5b1680c25219f0e4c006a2aa58ef4b8a01bc450df53cdbc1",
        ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7"
      },
      "external_inputs": {
        "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
        "tsukuroi-shokunin@aa136d69e0e4666b86782152cd1d1fa00f90a0b3:tools/tsukuroi-census.sh": "bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55",
        "tsukuroi-shokunin@72b038da9b2b1da2a37d35e3cce2d1d7650f70be:tools/tsukuroi-census.sh": "bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55",
        "tsukuroi-shokunin@af8adf15a2f5ea0be458ebc2144ca40ba4469e08:tools/tsukuroi-census.sh": "1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11",
        "tsukuroi-shokunin@b13e991fb96972b423b868ba122187f75357368c:tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e",
        "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
        "mado-shokunin@0c20a76fa5ff985047c8ca2d455c75179c3dd0d1:tools/mado-verify.sh": "90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd",
        "mado-shokunin@12c8f08a35537b7d53b8e0252459dec16e550079:tools/mado-verify.sh": "7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f",
        "mado-shokunin@8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122:tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.gitignore": "65e9a6838b253022bd43ee70918dcf5f6d920cb9c2e80b91ccfb15e8e54ee027",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.gitignore": "d949e4ef14286bcc34282c15538a4a023a6c74d436cba3dae0f5155239d8f817"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-13.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-16.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-17.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-18.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-19.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-20.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-21.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-22.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-23.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-24.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead07-25.json"
      ]
    }
  ]
}
```

Plain-English note. I read the section and each pointer it cites (SKILL.md:811-812, fleet-kill-rate-ledger.md:170-173, mutation-case-mado-verify.md:17-23, RerunSweep.md:19-23) under the trace collector at the clone pinned to b1cc95e1. I classed the section as a record: it names no command to run, and its checkable content is dated facts with pointers. I then checked each dated fact against the sibling git objects, the harness commit history, and the lane's own notes and plans. Most facts hold: the pins, the six-case rows, the RerunSweep precedent and its runner, the T3 and re-pin pointers, the four harness moves on 2026-10-14, and the PASS line text. Two claims do not hold: the mado "never re-cut" statement and the 19:15:54Z receipt time. I did not open LOG.md, SCORECARD.md or the round-21 coldread ledger by path or under the collector, and I did not run the regression harness or any sweep.

COLDREAD ReRead07: wrong-expectation
