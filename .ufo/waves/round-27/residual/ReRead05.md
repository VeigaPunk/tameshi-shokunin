# ReRead05: cold read of "### The boundaries — what a service run is not"

Verdict: gap-minor (class: record). No blocking gap and no wrong expectation. Seven minor gaps, listed below, most severe first. The two blocking gaps that Read09 found at revision 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 are gone at b1cc95e1fb62532646d74e2863770c4fed0851cc. The new wording checks out against the tool source and the cited spans.

Scope. Claim served: C1 (cold-read credit for this one section). Read revision b1cc95e1fb62532646d74e2863770c4fed0851cc, in the detached clone /tmp/ReRead05-yUql/fleet/tameshi-shokunin. Every receipt shows this rev, no live-lane read, and no external read. SKILL.md sha256 is fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f (receipt 7). The section runs from SKILL.md:858 (heading, verbatim) to SKILL.md:882 (blank). The next heading is SKILL.md:883, "### The report shape — what the opting-in lane receives". No code fence lies inside 858-882. Class is record: the section states facts with pointers and tells no reader to run anything. The monitor's no-ledger-entry reason is for the L1 to clear once it appends my entry. I did not touch the ledger, the scorecard, or the log.

## Findings, most severe first (none blocking)

1. M7, SKILL.md:866. The parenthetical "(corrected in round 27 after the cold read of seat Read09)" sits after the mado pointer. Round 27 did rewrite the whole bullet (receipt 12), and Read09's record exists in the tree (receipt 18), so the provenance is true. But corpus/knowledge/mutation-case-mado-verify.md has no round-27 commit (receipts 11 and 17; its last commit is 4494715), and the pointer range 57-59 was already there before the rewrite. A reader will think the mado lines changed.
2. M1, SKILL.md:881. Bullet 7 cites mutation-case-mado-verify.md:229-230. The words "whether the gate's verdicts" are on :228 (receipt 6), and :230 begins U3. The span starts one line late. Read09 raised this at 2227d83, and it is still open at b1cc95e.
3. M3, SKILL.md:860-861. "matrix row F" names no file and no line. Row F is corpus/knowledge/arm-class-matrix.md:44, and the prose at :259-260 says the same (receipt 16). The page's own row is SKILL.md:728 (receipt 1). Still open from Read09.
4. M5, SKILL.md:867. "A survivor is a gap named with its class" has no pointer and is not in the span the bullet cites. SKILL.md:308 supports it: "Shared survivor classes across the two cases, named" (receipt 15). Still open from Read09.
5. M4, SKILL.md:861. "a rate is bounded by its defect vocabulary" has no pointer. SKILL.md:248 supports it ("The classes are the injection vocabulary; read which class the suite can see."), and SKILL.md:1264 says the same about coordinated edits (receipt 15). Still open from Read09.
6. M2, bare file names at SKILL.md:863, 866, 869, 871, 874, 878, and 881. The names fleet-suite-census.md and mutation-case-mado-verify.md omit the corpus/knowledge/ directory. Each name matches exactly one file in the clone, so this is a readability gap only.
7. M6, SKILL.md:868. "a low kill rate is a report, not a service failure (SKILL.md:335)". Line 335 reads "Bands are a report convention, not a pass/fail gate." The gist holds, and "service failure" is a paraphrase.

## Evidence, bullet by bullet

Receipts are ReRead05-1 to ReRead05-19 in coldread/traces. The reader is my scratch script /tmp/ReRead05-yUql/rd.py, which prints numbered line ranges or matches a regex in the files named.

Bullet 1, SKILL.md:860-861 (single-edit mutants; coordinated rewrites unmeasured, matrix row F; rate bounded by defect vocabulary). Holds, with M3 and M4.
- tools/mutate-and-run.sh:33-35 (receipt 2): "# Inputs: a target file, a defect spec file, and a suite command. For each", "# defect: if this one exact edit were present in the target, would the suite go", "# red? Per-defect verdicts: KILLED (suite exit != 0) | SURVIVED (suite exit 0) |".
- corpus/knowledge/arm-class-matrix.md:44 (receipt 16): "| F | Coordinated edits | U1 unprobed | U1 unprobed | agree only that the method stops here — unknown (§7) |". Lines 259-260: "U1 — coordinated multi-edit rewrites ... are unmeasured in both cases (row F)."
- SKILL.md:728 (receipt 1): "| F coordinated edits | unprobed | unprobed | unprobed (10 single edits) | **unknown in all three** (U1 each) |".
- Defect vocabulary: SKILL.md:248 and SKILL.md:1264 (receipt 15), quoted under M4.

Bullet 2, SKILL.md:862-863 (hermetic suites only; no substrate-drift claim; per-revision and per-host; census §5 scope). Holds.
- corpus/knowledge/fleet-suite-census.md:288-291 (receipt 4): "**Scope of the offer, stated so it is not over-claimed:** single-edit mutants only (coordinated edits are unmeasured everywhere, matrix §7); hermetic suites only (no substrate-drift claim, matrix U5); results are per-revision and per-host (no cross-host stability claim, matrix U5)."
- Headings at :249 ("## 5. Tameshi's standing service offer") and :293 ("## 6. Boundary — beyond the six") (receipt 9). Lines 288-291 sit inside section 5, as the bullet says.

Bullet 3, SKILL.md:864-866 (Read-only). Holds after the round-27 rewrite. The old text is gone (receipt 12 diff).
- Target sha before equals after (MUTATE_RESTORE). tools/mutate-and-run.sh:555-564 (receipt 13): the code compares the target and pristine sha before and after. A mismatch prints "MUTATE_RESTORE: DRIFT (...)" at :559 and stops with a setup failure. Otherwise :563 prints "MUTATE_RESTORE: OK (target-sha256 before=%s after=%s pristine-sha256=%s)".
- The tool emits no tree-clean check. Receipt 14 (pattern (?i)clean|porcelain|dirty|status) finds no printed line that reports a tree state. Its porcelain and status calls sit in the selftest canary (:1885 and :1897). The name git_clean is a wrapper that scrubs GIT_* variables (:268-277). The comments at :1154-1155 say a drifted or dirty tree cannot move a replay. Receipt 19 lists every line that names git in lowercase, or matches diff-index, ls-files, diff --, or rev-parse (pattern \bgit\b|diff-index|ls-files|diff --|rev-parse). The calls sit at :260-297 (wrapper and fixture commit), :1174-1228 and :1352-1353 (regression materialization and precondition), and :1727-1905 (selftests). Between :298 and :1151 the only matches are comments (:600, :602, :916, :1096). So the sweep path makes no git call.
- Porcelain-clean is an opt-in precondition at open (SKILL.md:808-809, receipt 1): "1. **A pinned revision** — committed bytes of the gate with sha256, size, line count, mtime, and a porcelain-clean sibling tree at open."
- "The target is never written" (tools/mutate-and-run.sh:36-38, receipt 2): line 36 ends "The target is", and line 37 begins "never written: every mutant is a fresh byte copy of the pinned pristine copy,". Line 38 reads "and the target's sha256 before/after is the restore proof." The quote wraps across :36-37.
- Fingerprints prove endpoint identity, not that no transient write occurred (SKILL.md:377-378, receipt 1): "Before/after fingerprints establish endpoint" / "identity, not that no transient write occurred."
- Sha pair (corpus/knowledge/mutation-case-mado-verify.md:57-59, receipt 6): line 58 reads "MUTATE_RESTORE: OK (target-sha256 before=d7edaab4…d0e13 after=d7edaab4…d0e13", and line 59 reads "pristine-sha256=d7edaab4…d0e13)".
- The parenthetical after the pointer: see M7.

Bullet 4, SKILL.md:867-871 (findings kept, never smoothed). Holds, with M5 and M6.
- "A survivor is a gap named with its class": see M5.
- "a low kill rate is a report, not a service failure (SKILL.md:335)": see M6. Line 335 (receipt 1) reads "- **Bands are a report convention, not a pass/fail gate.** An 8/10 admits, and so".
- "Mado's 40 % is the first point below the 50-80 band (corpus/knowledge/mutation-case-mado-verify.md:175-176)": receipt 6, line 175 reads "Headline sequence: **80 % (JS r2) · 80 % (kagi bash r3) · 60 % (tsukuroi bash r5) · 40 %", and line 176 reads "(mado bash r6). The fourth point is the first below the 50–80 band, and its cause is composition:". Holds.
- "reads as composition (4 in-surface + 6 out-of-surface, measured 4/4 and 0/6), not as a suite regression (mutation-case-mado-verify.md:66-72)": receipt 6, lines 66-72 state the composition before the run, the measured 4/4 and 0/6, and "The 40 % rate is composition, not a regression of the suite". Holds.

Bullet 5, SKILL.md:872-874 (recommendations only). Holds. Receipt 6: line 237 reads "- U6 — whether mado accepts any §8 recommendation is a decision of mado's lane; this note", and line 238 reads "records the findings unabsorbed." Line 240 is "## 8. Recommendation to the owner (mado) — recommendations only, no patch", with seven items through line 260.

Bullet 6, SKILL.md:875-878 (harness pinned per run; re-pin b56c6e57). Holds. Receipt 6: line 17 reads "**Incident I1 — the harness itself moved mid-round, by a concurrent lane.**"; line 21 reads "Re-pin at 17:46:15Z: sha256 `b56c6e57…2bcb`"; lines 22-23 read "Every number in this note is tied to `597e1419…`" and "Recorded, not smoothed; nothing was repaired."

Bullet 7, SKILL.md:879-881 (sensitivity, not truth). Holds in substance, with M1. Receipt 6, lines 226-262: line 228 reads "- **U2** — suite sensitivity ≠ gate truth: nothing here measures whether the gate's verdicts"; line 229 reads "against the *real* config planes are right; only what its suite can detect."; line 230 begins "- **U3** — tool drift (I1)".

Read09 cross-check (receipt 18 is Read09's record at 2227d83):
- Fixed at b1cc95e: the blocking gap on the porcelain-clean clause (now SKILL.md:808-809, plus the tool evidence above); the blocking gap on the provable-negative clause (removed); the minor gap on the "first point below the band" pointer (now :175-176); and the minor gap on the "service failure" pointer (now :335).
- Still open at b1cc95e: M1 (bullet 7 range), M3 (matrix row F), M4 (vocabulary pointer), and M5 (survivor-class pointer).

## Smallest safe correction (recommendation only; I edited no production file)

1. SKILL.md:881: change "mutation-case-mado-verify.md:229-230" to "corpus/knowledge/mutation-case-mado-verify.md:228-229" (M1).
2. SKILL.md:866: move the parenthetical to the end of the bullet and say the bullet was corrected, for example "this bullet corrected in round 27 after the cold read of seat Read09" (M7).
3. SKILL.md:860-861: change "(matrix row F)" to "(row F: corpus/knowledge/arm-class-matrix.md:44)", and add "(SKILL.md:248)" after "defect vocabulary" (M3, M4).
4. SKILL.md:867: add "(SKILL.md:308)" after "named with its class" (M5).
5. Optional: prefix corpus/knowledge/ on the first mention of each bare file name (M2), and quote the words of SKILL.md:335 (M6).

Items 1 to 4 close every pointer gap. After them the section should be read again by a fresh seat. That is a recommendation for the L1, not an admission.

## Residual risk and verification gaps

- No sweep or replay ran. The section is a record. I checked its claims against source text and committed files read under the collector, and I did not run the tool.
- The no-tree-check finding rests on greps (receipts 3, 14, and 19) and on the lines they return. Receipt 19 lists every line that names git in lowercase, which covers git-based checks. A call made through a variable, or a check that used neither git nor the words clean, dirty, status, or porcelain, would not show in these greps. I did not read all 2017 lines of the tool.
- The harness at b1cc95e has sha256 fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de (receipts 2, 3, 13, 14, 19). The mado note names the run's tool as 597e1419… and records a re-pin to b56c6e57…. The section does not claim that either hash is current, so this is not a gap for it. A reader who looks for the current hash in the mado note will not find it.
- Git-object reads (receipts 5, 10, 11, 12, and 17) do not appear in inputs, because the tracer excludes .git components. I use them only for history and for the round-27 diff. Every claim that depends on file bytes has a file receipt.
- The round-27 provenance rests on the diff (receipt 12) and on Read09's record (receipt 18). I did not audit Read09's own receipts.
- Scope: this is one section's verdict. I did not run c1-measure.py or c2-measure.py. Nothing here is a calibration or score claim.

## Setup, probes, and tools (outside the collector; none is in commands_executed; no claim relies on them)

- Clone and detached checkout (assignment step 1). The sibling symlinks were created and never read.
- Before tracing, git rev-parse HEAD and sha256sum of SKILL.md matched b1cc95e1… and fce54977…. Receipts 1 and 7 repeat both under the collector.
- Read /home/vgpnk/.omp/agent/RULES.md. Version probes: strace 7.2 (/usr/bin/strace), Python 3.14.8 (/usr/bin/python3), git 2.56.0 (/usr/bin/git). No tool was installed or upgraded, so no channel was used.
- ls -la of two lane directories (coldread/ and waves/round-27/) to find write targets. Listings only.
- An untraced git show --stat of b1cc95e. Receipt 10 is the traced repeat, and I relied only on that one.
- Read and grep tool calls on the clone's SKILL.md and tools/trace-inputs.py (by hand). A glob of the clone for the cited file names gave one match each for the census and mado files. Reads of my own receipts (outputs, not evidence).
- Write targets: this report and receipts ReRead05-1 to ReRead05-19 only. No production file was edited. No jj command ran. No git write ran in the lane. No trace read the live lane.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ReRead05", "skill_sha256": "fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f", "read_rev": "b1cc95e1fb62532646d74e2863770c4fed0851cc",
 "sections": [{"start": 858, "heading": "### The boundaries \u2014 what a service run is not", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
   "minor_gaps": [
     "M7 SKILL.md:866 parenthetical '(corrected in round 27 after the cold read of seat Read09)' follows the mado pointer. Round 27 rewrote the whole bullet in b1cc95e (receipt 12) and followed Read09's record (receipt 18), so the provenance is true. But corpus/knowledge/mutation-case-mado-verify.md has no round-27 commit (receipts 11 and 17; last commit 4494715), so a reader will think the mado lines changed. Fix: move the parenthetical to the end of the bullet and say the bullet was corrected.",
     "M1 SKILL.md:881 cites mutation-case-mado-verify.md:229-230, but the words 'whether the gate's verdicts' sit on :228 (receipt 6) and :230 begins U3. Read09 raised this at 2227d83; still open at b1cc95e. Fix: cite :228-229.",
     "M3 SKILL.md:860-861 'matrix row F' names no file or line. Row F is corpus/knowledge/arm-class-matrix.md:44 with prose at :259-260 (receipt 16); the page's own row is SKILL.md:728 (receipt 1). Still open from Read09. Fix: name the file and line.",
     "M5 SKILL.md:867 'A survivor is a gap named with its class' has no pointer and is not in the cited span; SKILL.md:308 supports it (receipt 15). Still open from Read09. Fix: add the pointer.",
     "M4 SKILL.md:861 'a rate is bounded by its defect vocabulary' has no pointer; SKILL.md:248 supports it (receipt 15), and SKILL.md:1264 says the same about coordinated edits. Still open from Read09. Fix: add the pointer.",
     "M2 SKILL.md:863, 866, 869, 871, 874, 878, 881 use bare file names (fleet-suite-census.md, mutation-case-mado-verify.md) without the corpus/knowledge/ directory. Each name matches exactly one file in the clone. Fix: prefix the first mention.",
     "M6 SKILL.md:868 'a low kill rate is a report, not a service failure (SKILL.md:335)': line 335 says 'Bands are a report convention, not a pass/fail gate'. The gist holds; 'service failure' is a paraphrase. Fix: quote the line's own words."
   ],
   "commands_executed": [
     "python3 /tmp/ReRead05-yUql/rd.py SKILL.md:858:882 SKILL.md:806:826 SKILL.md:333:337 SKILL.md:374:380 SKILL.md:668:793 (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py tools/mutate-and-run.sh:30:46 (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py --grep 'MUTATE_RESTORE|porcelain|never written|git status|tree-clean|clean tree|worktree|dirty|status --' tools/mutate-and-run.sh (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py corpus/knowledge/fleet-suite-census.md:280:296 (exit 0)",
     "git --no-optional-locks -C /tmp/ReRead05-yUql/fleet/tameshi-shokunin log --format=%h%x20%ad%x20%s --date=short -n 15 -- SKILL.md corpus/knowledge/mutation-case-mado-verify.md (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py corpus/knowledge/mutation-case-mado-verify.md:14:24 corpus/knowledge/mutation-case-mado-verify.md:55:75 corpus/knowledge/mutation-case-mado-verify.md:172:178 corpus/knowledge/mutation-case-mado-verify.md:226:262 (exit 0)",
     "sha256sum SKILL.md tools/trace-inputs.py (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py --grep '.' .ufo/waves/round-26/w1/ColdreadPilot.md (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py --heads corpus/knowledge/fleet-suite-census.md (exit 0)",
     "git --no-optional-locks -C /tmp/ReRead05-yUql/fleet/tameshi-shokunin show --stat --format=%H%x20%s b1cc95e1fb62532646d74e2863770c4fed0851cc (exit 0)",
     "git --no-optional-locks -C /tmp/ReRead05-yUql/fleet/tameshi-shokunin show --format=COMMIT%x20%h -U0 b1cc95e1fb62532646d74e2863770c4fed0851cc -- corpus/knowledge/mutation-case-mado-verify.md (exit 0; no output)",
     "git --no-optional-locks -C /tmp/ReRead05-yUql/fleet/tameshi-shokunin show --format=COMMIT%x20%h -U0 b1cc95e1fb62532646d74e2863770c4fed0851cc -- SKILL.md (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py tools/mutate-and-run.sh:540:570 tools/mutate-and-run.sh:1148:1160 (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py --grep '(?i)clean|porcelain|dirty|status' tools/mutate-and-run.sh (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py --grep 'vocabulary|bounded by|survivor class|named with its class|gap named|survivor taxonomy' SKILL.md (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py --grep 'coordinated|row F|^\\| F' corpus/knowledge/arm-class-matrix.md (exit 0)",
     "git --no-optional-locks -C /tmp/ReRead05-yUql/fleet/tameshi-shokunin log -1 --format=%h%x20%s -- corpus/knowledge/mutation-case-mado-verify.md (exit 0; 4494715 probation round 6 (training r5): see LOG)",
     "python3 /tmp/ReRead05-yUql/rd.py --grep '.' .ufo/waves/round-27/w1/Read09.md (exit 0)",
     "python3 /tmp/ReRead05-yUql/rd.py --grep '\\bgit\\b|diff-index|ls-files|diff --|rev-parse' tools/mutate-and-run.sh (exit 0)"
   ],
   "opened": ["SKILL.md", "tools/trace-inputs.py"],
   "inputs": {
     "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
     "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
     "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
     "corpus/knowledge/arm-class-matrix.md": "bd4f4a02eb66f4e25e67a1518108d1f11c45b4edf2355d1901ec54ce55359088",
     ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7",
     "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
     ".ufo/waves/round-27/w1/Read09.md": "09a451900ef046840dedd799449521b0449b8b9a88c4bc94d9a5d868cf8e0f2e"
   },
   "external_inputs": {},
   "traces": [
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-1.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-2.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-3.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-4.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-5.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-6.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-7.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-8.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-9.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-10.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-11.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-12.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-13.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-14.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-15.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-16.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-17.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-18.json",
     "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead05-19.json"
   ]}]}
```

Plain-English note. I read the section at b1cc95e under the trace collector and checked each of its seven bullets against the cited spans and the tool source. Round 27's rewrite of the Read-only bullet (receipt 12) removed the two claims that Read09 found blocking, and the new wording holds. The sha pair, the restore line, the no-write comment, and the porcelain precondition all check out, and no git call sits on the sweep path. What remains is pointer work: one off-by-one range, two claims with no pointer, an unnamed matrix row, bare file names, and a parenthetical that reads as if the mado note changed. I found no false claim, so the verdict is gap-minor. I edited nothing in the lane.

COLDREAD ReRead05: gap-minor
