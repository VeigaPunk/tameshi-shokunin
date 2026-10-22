# Read22: cold read of "### The six-leg regression — usage and this round's receipt"

Verdict: **gap-minor**, class **record**. Section: SKILL.md:1302-1364 at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 (checked in the detached clone /tmp/Read22-zVif/fleet/tameshi-shokunin).

## Verdict and scope

The section is a correct record of tool revision 75ed934d (commit 606716f, 1642 lines). I replayed that exact tool, and its selftest (80/80) and six-leg regression (cases=6) reproduce the section's stated results; the dates and scratch paths differ, as expected. At the cold-read revision the tool has grown to nine legs, so the section's anchors and counts describe 75ed934d and not the head. The header says this; the bullets do not repeat it. The gaps are minor: one off-by-one anchor, two misquotes, a VERSION string that cannot tell the two revisions apart, and one evidence directory that no longer exists.

## Evidence

1. Pinned bytes. `git show 606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh` hashes to 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5, with 1642 lines. Commit 606716f is an ancestor of 2227d83. (external_inputs)

2. Replay of the 606716f tool. I copied those bytes into the clone as an untracked file, tools/mutate-and-run.r75.sh. Receipts Read22-10 and Read22-11 record its sha256 as 75ed934d.
   - `bash tools/mutate-and-run.r75.sh --selftest` printed `MUTATE_SELFTEST: 80/80 pass` and `VERDICT: PASS`, exit 0. This matches the section.
   - `bash tools/mutate-and-run.r75.sh --regression --keep` printed REGRESSION_EXPECT with six rates. It printed match=10/10 for legs 1-4 and 6, match=15/15 for leg 5, and flips=0 inconclusive=0 for each. The closing line was `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`, exit 0. This matches the section.
   - Each REGRESSION_PIN line carries mode=. The six digests (for example mado d7edaab4..., checklist 7e5ec98b...) equal my independent `git show | sha256sum` values in external_inputs.

3. Section anchors checked against the 606716f bytes. Sources :90-97 match. The mode-mirror comment :104-106 matches. The exit map :115-117 matches. Pins and tables :550-559 match. Leg-5 and leg-6 spec openers :766 and :841 match. The git show and mode-mirror block :932-960 matches (:938-960 is the mirror). Registrations :1132-1141 are legs 5 and 6 (leg 4 ends at :1130-1131). The exec-bit selftest arms :1488-1527 match. One anchor is off by one: the leg list is :84-89, because js-kimi-census is on line 84, and the section cites :85-89. The VERSION line is :157: `VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'`.

4. Cleanup and exit logic at 606716f (lines :1088-1094 and :1156-1168). The default mktemp root sets auto=1. --workdir leaves auto=0. FAIL exits 1 before any cleanup. SETUP prints `(kept)` and exits 2. PASS runs `rm -rf` only when auto=1 and KEEP=0. This matches "removed on PASS unless --keep; kept on FAIL/SETUP; never removed when --workdir was given".

5. Head 2227d83, tool sha256 fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de, 2016 lines (Read22-1, -2, -4, -5, -6).
   - The usage line at :196 is `mutate-and-run.sh --regression [--workdir DIR] [--keep]`, unchanged. The cleanup at :1453-1455 has the same logic. VERSION at :175 is the same string.
   - `bash tools/mutate-and-run.sh --selftest` printed `MUTATE_SELFTEST: 97/97 pass`, exit 0.
   - `bash tools/mutate-and-run.sh --regression --keep` ran nine legs and printed `REGRESSION: PASS (cases=9 passed=9; ...)`, exit 0, in 275.9 s. Legs 1-6 reproduce their recorded rates and pins (match=10/10, 15/15, flips 0).
   - At the head, the section's anchors point at other text. The leg list is at :87-95. :115-119 is r7-1 materialization comment. :550-559 is the sweep restore check. :1132-1141 is an S_USAGE defect spec. :1488-1527 is fixture setup.

6. Pointers into the ledger and SKILL.md at 2227d83 (Read22-3, Read22-7).
   - fleet-kill-rate-ledger.md:85-88 still reads "cases 1 and 2 only". Line :281 sits inside the ER-2 entry that starts at :272. The ER-4 caveat (a) is at :350.
   - SKILL.md:965 is the "Reading a receipt" heading, and the next heading is at :1010. SKILL.md:1218-1222 shows cases=4. SKILL.md:1227-1228 reads "still not embedded: their rows carry no REGRESSION line — named debt, not smoothed"; the section quotes it shortened to "still not embedded — named debt".
   - SKILL.md:925 reads "Four legs at that revision". The section quotes "Four legs at this revision".

7. operator-runbook.md:345-407 (Read22-8) is section 7, and it renders the same command. ✓

8. Evidence directories. `/tmp/w10-t10-4-ev` and `/tmp/w9-tameshi-t93` do not exist on this host (Read22-9). The section names /tmp/w10-t10-4-ev/ as the kept regression workdir and does not say it is gone.

## Smallest safe correction (recommendation only; I edited no production file)

1. Change `tools/mutate-and-run.sh:85-89` to `:84-89`.
2. Correct the two quotations to the source text: "Four legs at that revision" (SKILL.md:925) and "still not embedded: their rows carry no REGRESSION line — named debt, not smoothed" (SKILL.md:1227-1228).
3. Add one sentence under the header: "At read revision 2227d83 the tool is fb91ef76… (2016 lines, nine legs, --selftest 97/97); the anchors and the six-leg and 80/80 expectations hold only at 75ed934d. VERSION is identical at both revisions, so identify the tool by sha."
4. Note that /tmp/w10-t10-4-ev/ no longer exists, and that a replay of 606716f on 2026-10-22 reproduces the receipt.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read22", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 1302, "heading": "### The six-leg regression \u2014 usage and this round's receipt", "class": "record", "verdict": "gap-minor",
  "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
   "Scope: every anchor and count in the section is for tool 75ed934d (commit 606716f). At read revision 2227d83 the tool is fb91ef76... (2016 lines, nine legs, --selftest 97/97). The anchors :85-89, :90-97, :550-559, :766, :841, :1132-1141, :115-119, :104-106, :932-960 and :1488-1527 point to other text there, and the six-leg and 80/80 expectations do not hold at the head. The header states the 75ed934d scope and says the sha governs; the bullets do not repeat it.",
   "Off-by-one: the leg list is tools/mutate-and-run.sh:84-89 at 75ed934d (js-kimi-census is line 84), not :85-89.",
   "Misquotes: SKILL.md:925 reads 'Four legs at that revision' (the section quotes 'this revision'); SKILL.md:1227-1228 reads 'still not embedded: their rows carry no REGRESSION line — named debt, not smoothed' (the section quotes 'still not embedded — named debt').",
   "Revision identity: the VERSION string is 'mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)' at both 606716f (line 157) and 2227d83 (line 175), so it cannot tell the revisions apart; the sha256 is the only identifier.",
   "Missing evidence path: /tmp/w10-t10-4-ev/ (named as the kept regression workdir) does not exist on this host, and the section does not say so. The 606716f replay reproduces the receipt instead.",
   "Registry anchor: :1132-1141 holds legs 5 and 6 only (the leg 4 registration ends at :1130-1131); the section does not say so.",
   "Not checkable from this lane: 'the owner's own run at the same revision, 21:00:24Z, closes identically' is another lane's run."
  ],
  "commands_executed": [
   "python3 -c <numbered line-range printer> tools/mutate-and-run.sh:1-40 tools/mutate-and-run.sh:84-98 tools/mutate-and-run.sh:102-120 tools/mutate-and-run.sh:548-562 tools/mutate-and-run.sh:764-768 tools/mutate-and-run.sh:839-843 tools/mutate-and-run.sh:930-962 tools/mutate-and-run.sh:1130-1143 tools/mutate-and-run.sh:1486-1530",
   "bash -c 'sha256sum tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/operator-runbook.md; wc -l tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/operator-runbook.md'",
   "python3 -c <numbered line-range printer> corpus/knowledge/fleet-kill-rate-ledger.md:80-92 corpus/knowledge/fleet-kill-rate-ledger.md:276-286 SKILL.md:921-931 SKILL.md:963-968 SKILL.md:1212-1229",
   "bash tools/mutate-and-run.sh --selftest",
   "bash tools/mutate-and-run.sh --regression --keep",
   "python3 -c <regex line printer> 'KEEP|keep|rm -rf|mktemp|ROOT=|VERSION|die_setup\\(\\)|exit [0-2]|--regression\\)|--workdir|usage' tools/mutate-and-run.sh",
   "python3 -c <regex line printer> 'ER-[0-9]|cases 1 and 2 only|§7|^#{1,4} |ER-4' corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/operator-runbook.md SKILL.md",
   "python3 -c <numbered line-range printer> corpus/knowledge/operator-runbook.md:345-407",
   "bash -c 'ls -d /tmp/w10-t10-4-ev /tmp/w9-tameshi-t93 2>&1; echo \"ls-rc=$?\"'",
   "bash tools/mutate-and-run.r75.sh --selftest",
   "bash tools/mutate-and-run.r75.sh --regression --keep",
   "sha256sum tools/trace-inputs.py tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/operator-runbook.md"
  ],
  "opened": ["SKILL.md", "tools/mutate-and-run.sh", "tools/trace-inputs.py", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/operator-runbook.md"],
  "inputs": {
   "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
   "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
   "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
   "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859"
  },
  "external_inputs": {
   "tameshi-shokunin@606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
   "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
   "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
   "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
   "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
   "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
   "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
   "kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs": "f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9",
   "kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs": "6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f",
   "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"
  },
  "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-1.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-2.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-3.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-4.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-5.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-6.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-7.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-8.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-9.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-10.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-11.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read22-12.json"
  ]}]}
```

## Note: what I checked

- I read the section from the detached clone at 2227d83 and took it to be a record. Every command I ran under the trace collector wrote a receipt with rev 2227d83, exit 0, rev_reason null, and no live-lane reads. Receipt Read22-5 is the head regression run and Read22-11 is the 606716f replay.
- The divergence at the head (nine legs, selftest 97/97, shifted anchors) is recorded under minor gaps, not wrong_expectations. The section scopes its expectations to 75ed934d in its header, and its "Reading a receipt" bullet says that on a differing revision the tool bytes and the run executed govern. Its usage bullet, "Command, unchanged", still holds at the head: the usage line, the flags and the cleanup rule are the same.
- I did not check the owner's 21:00:24Z run, and I could not read /tmp/w10-t10-4-ev/ because it is gone.
- Un-traced commands, all by design or setup: the step-1 clone; the materialization `git show 606716f:tools/mutate-and-run.sh > tools/mutate-and-run.r75.sh` inside my clone; read-only `git status`; sibling `git rev-parse` and `git show` reads, all recorded in external_inputs; and version checks. None of them wrote into the lane.
- Lane writes: receipts Read22-1 to Read22-12 under coldread/traces and this report. I read the live lane only after the last trace had finished (I read receipts, never during a run).
- Tooling: no install or upgrade. strace 7.2, git and python3 were already present. I read RULES.md and did not use the install channel.
- Kept scratch for cleanup: /tmp/Read22-zVif (clone and fleet mirror), /tmp/tameshi-r4-2-regression.kDjqQe (head run), and /tmp/tameshi-r4-2-regression.iUBjjf (replay). The receipts' dropped_home_count values (237, 5529, 105, 1848) count /home paths outside the fleet root that the collector never hashes; I did not inspect them, and the section does not cite them.

COLDREAD Read22: gap-minor
