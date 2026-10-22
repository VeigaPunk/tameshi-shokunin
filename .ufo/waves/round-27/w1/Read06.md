# Read06 cold read: SKILL.md:405-465, bash vs JS divergence (round 3)

Verdict: wrong-expectation

Section: `## Cross-language divergence — bash vs JS (round 3, measured)`. Class: record. Read at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. Page sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 (matches the brief).

One present-tense claim fails. "Band interiors remain unprobed" (SKILL.md:463) cites mutation-case-kagi-census.md:58-60, which does not say it, and the page records later measured points inside the 50-80 band. Every other cited line range, sibling pin, count and selftest result I checked holds. Four precision items are minor.

## Evidence

**Setup.** Detached mirror at /tmp/Read06-OG2G/fleet/tameshi-shokunin. HEAD verified as 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. Sibling repos are symlinked under /tmp/Read06-OG2G/fleet/. Section bounds: heading at SKILL.md:405, next heading "## No-permissiveness audit recipe" at :466, body :405-465.

**Receipts.** /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-1.json through Read06-17.json. All report rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 and empty live_lane_reads. All exit 0 except Read06-13, which exits 1 because grep found no hunk headers; that is the expected result. commands_executed[i] is the argv of Read06-(i+1).json.

### W1 (wrong expectation): SKILL.md:462-464

Text: "Band interiors remain unprobed (mutation-case-kagi-census.md:58-60)".

- Census lines 58-60 (Read06-5, observed): "`mutation-case-kimi-census.md` (compared in §4). Per `SKILL.md`'s bands the case sits on the 50-80/>80 boundary, so that boundary reading is the worked one, and the survivors table below is attached as the band requires." No statement that band interiors are unprobed.
- Read06-12, observed: `grep -n -i -E "interior|unprobed" corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kimi-census.md; echo "grep_exit=$?"` printed `grep_exit=1`. Neither census note contains either word.
- The page records later measured points inside the band:
  - SKILL.md:684-685: "It diverged: **6/10 killed (60 %)** — the first measurement inside the 50-80 % band".
  - SKILL.md:736-738: "The bands table's 50-80 % row is now the measured one, superseding the 'band interiors unprobed' (U) — >80 % and <50 % stay unprobed".
  - SKILL.md:1104: kumitate `scripts/claims-check.mjs` at 7/10 = 70 %.
- The round-3 note measured only 80 % points, so the sentence was true when written. As written, it is present tense, its citation does not support it, and the page contradicts it. The pilot rules define a wrong expectation as a claim the page makes that does not hold (ColdreadPilot.md:206), and a failing entry fails the bucket (ColdreadPilot.md:219-221).

### Checked and holding

- Round-2 and round-3 figures: kagi 8/10 (kagi :162-170, :176-180); kimi 8/10, the restore pin and the 11-run cost (kimi :29-35). Read06-2, Read06-5, Read06-6.
- Plan anti-claim: plans/round-3.plan.md:8-9. Read06-4.
- Two-lane rule: PROVINCE.md:15-16 ("owns only the reusable craft (a pattern is admitted from evidence in TWO / independent lanes before it is claimed general)"). Read06-4.
- Bash abstention, token-only kill and bad-case labels: kagi :27-35, :82-103, :88-91. Read06-5.
- Exact-string and open-unknown pointers: kagi :181-182; U2 at :197-198; U5 at :203-204. Read06-5.
- F-2 pattern: gates-survey-kagi.md:326-361 (heading :326; bypass-class text :349-356). Read06-7.
- Erratum R21 begins at kagi :261. Read06-17.
- Sibling kagi gate at fecee8743e52eb8fb5fbb40782934cb619a1a96e, file sha256 275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f: 44212 bytes, `wc -l` 886, selftest `SELFTEST: PASS (16 cases)` with ok-case 01-14 and skip-case 15/16 "substrate-absent (handler not on PATH)", exit 0. Read06-8.
- Sibling kimi gate at 175de6ba2e9e904010411b19cab27e0af9aad3d4, file sha256 83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426: 43273 bytes, `wc -l` 896, `KIMI_CENSUS_SELFTEST: 43/43 pass`, `VERDICT: PASS`, exit 0. Read06-9.
- Kimi gate mechanics: fixtureTree writes and chmods real files (:430-455); runGate uses spawnSync (:457-460); DRIFT prefix assert (:498); exact CLEAN (:511-512); `FAIL ${label}` lines (:850); count epilogue (:852). A missing mkfifo returns ok false, so that arm fails rather than skips (:637-639). Read06-10.
- Bash gate mechanics: run_case checks exit plus one token (:747-760); sqlite-unavailable asserts two tokens (:782); skip-case lines (:821-823); FAIL epilogue `SELFTEST: FAIL (%s/%s cases)` (:847). Read06-8, Read06-17.
- PROVINCE.md is unchanged from base: blob 6154fe44c2916027583bd63c4001b1b252819d57 at 91edf9cd82ccc72e10f62f81d37181f549d593b8 and at 2227 (Read06-13, Read06-15); `git diff` printed nothing. The monitor's input-drift:PROVINCE.md flag therefore does not come from an edit inside this range. Lines 15-16 read as the section says.

### Minor gaps (non-blocking)

- **M1 (SKILL.md:446-450).** The kill-width bullet cites mutation-case-kagi-census.md:171-175 for the JS half. Lines 173-174 carry the in-memory JS wording that Erratum R21 (:261) retracts. The bash half of 171-175 is correct. The JS claims hold in kumitate scripts/kimi-census.mjs at 175de6ba (lines 430-455, 498, 511-512), but the cited census lines 82-89 cover only the DRIFT prefix and exact CLEAN. Fix: cite kimi-census.mjs:430-460,498,511-512 for the JS half and drop 171-175 from that clause.
- **M2 (SKILL.md:433).** "27/43 pass" is cited only to mutation-case-kagi-census.md:82-103, which has no JS figure. The figure is at mutation-case-kimi-census.md:44 (D1) and :46 (D3); those rows also support "broad predicates affect many cases". Fix: add mutation-case-kimi-census.md:44,46.
- **M3 (SKILL.md:435).** "SELFTEST: FAIL (1/16 cases)" is not in cited lines 82-103. The format is the gate printf at surface-census.sh:847 (sha256 275d8294), and census table row B1 shows 1/16 / FAIL. Fix: cite surface-census.sh:847.
- **M4 (SKILL.md:408).** "886-line" is the newline count (`wc -l` 886). The file has 887 lines when split on newline; the last line is unterminated (last byte `c`). The census artifact paragraph says this. Fix: say "886 newline-terminated lines" or name the counting rule.

### Smallest safe correction

1. SKILL.md:463. Replace "Band interiors remain unprobed (mutation-case-kagi-census.md:58-60);" with a round-scoped sentence and page pointers, for example: "At round 3 the band interiors were unprobed (both measurements at 80 %, SKILL.md:337-339); round 5 measured the 50-80 row at 60 % (SKILL.md:684-685, :736-738);". Then cold-read the section again.
2. Apply M1 to M4. Nothing else needs to change.

### Verification gaps

- I did not re-run the mutant sweeps (kagi B1-B10, kimi D1-D10). I checked the pinned artifacts, the selftest counts and the cited text only.
- U2 and U5 "remain open": consistent with what I saw. The verb cases skip on this host (Read06-8). Page lines SKILL.md:243-244, :770-771 and :1150-1151 still list cross-host stability as unknown. Not re-measured.
- Out of scope, for the L1: SKILL.md:339-340 (bands section) cites PROVINCE.md:16-17 for the same two-lane rule, which starts on line 15.

### Tools, scratch and setup

- Tools installed or upgraded: none. strace 7.2, Python 3.14.8, git and node were already present and used as found. RULES.md was not needed because nothing was installed.
- Scratch lives under /tmp/Read06-OG2G (clone, sibling copies, numbered.py helper). The lane was written only under coldread/traces/ and this report.
- Outside the collector, for setup only: the clone build (mktemp, symlinks, git clone --no-hardlinks, git checkout --detach, sha256 of SKILL.md), a tool check (command -v, python3 --version, strace -V), and ls of the live receipt and wave folders. Page lines came from hand reads and search output. The repo-wide search for interior and unprobed scanned the clone tree, which may have read SCORECARD.md, LOG.md and the round-21 ledger.json incidentally. I did not open those three by path or under the collector, and I used no output from them.
- Read06-1 to Read06-3 were first run with stdout discarded and then re-run with stdout shown. The surviving receipts come from the shown runs, with the same argv.
- Sibling reads ran through `sh -c` under the collector. Their receipts show empty external maps because .git reads are excluded, so both sibling artifacts are recorded in external_inputs.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read06", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {"start": 405, "heading": "## Cross-language divergence \u2014 bash vs JS (round 3, measured)", "class": "record", "verdict": "wrong-expectation",
     "blocking_gaps": [],
     "wrong_expectations": [
       "W1 (SKILL.md:462-464): 'Band interiors remain unprobed (mutation-case-kagi-census.md:58-60)'. Census lines 58-60 do not say this, and neither census note contains 'interior' or 'unprobed' (Read06-12, grep_exit=1). The page itself records later measured points inside the 50-80 band: SKILL.md:684-685 (6/10 = 60 %, the first measurement inside the band), SKILL.md:736-738 (superseding the band-interiors-unprobed statement), SKILL.md:1104 (7/10 = 70 %). As written, the present-tense claim does not hold at 2227."
     ],
     "minor_gaps": [
       "M1 (SKILL.md:446-450): the kill-width bullet cites mutation-case-kagi-census.md:171-175 for the JS half. Lines 173-174 carry the in-memory JS wording that Erratum R21 (census line 261) retracts. The bash half of 171-175 is correct. The JS claims hold in kumitate scripts/kimi-census.mjs at 175de6ba (lines 430-455, 498, 511-512), but the cited census lines 82-89 cover only the DRIFT prefix and exact CLEAN. Fix: cite kimi-census.mjs:430-460,498,511-512 for the JS half and drop 171-175 from that clause.",
       "M2 (SKILL.md:433): '27/43 pass' is cited only to mutation-case-kagi-census.md:82-103, which has no JS figure. The figure is at mutation-case-kimi-census.md:44 (D1) and :46 (D3), which also support 'broad predicates affect many cases'. Fix: add mutation-case-kimi-census.md:44,46.",
       "M3 (SKILL.md:435): 'SELFTEST: FAIL (1/16 cases)' is not in cited lines 82-103. The format is the gate printf at surface-census.sh:847 (sha256 275d8294), and census table row B1 shows 1/16 / FAIL. Fix: cite surface-census.sh:847.",
       "M4 (SKILL.md:408): '886-line' is the newline count (wc -l 886). The file has 887 lines when split on newline, with an unterminated last line (last byte c). The census artifact paragraph says this. Fix: say '886 newline-terminated lines' or name the counting rule."
     ],
     "commands_executed": [
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" /tmp/Read06-OG2G/fleet/tameshi-shokunin/PROVINCE.md /tmp/Read06-OG2G/fleet/tameshi-shokunin/plans/round-3.plan.md",
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" /tmp/Read06-OG2G/fleet/tameshi-shokunin/corpus/knowledge/mutation-case-kagi-census.md /tmp/Read06-OG2G/fleet/tameshi-shokunin/corpus/knowledge/mutation-case-kimi-census.md",
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" /tmp/Read06-OG2G/fleet/tameshi-shokunin/corpus/knowledge/gates-survey-kagi.md",
       "python3 /tmp/Read06-OG2G/numbered.py /tmp/Read06-OG2G/fleet/tameshi-shokunin/PROVINCE.md:12-19 /tmp/Read06-OG2G/fleet/tameshi-shokunin/plans/round-3.plan.md:1-13",
       "python3 /tmp/Read06-OG2G/numbered.py /tmp/Read06-OG2G/fleet/tameshi-shokunin/corpus/knowledge/mutation-case-kagi-census.md:27-35,58-60,82-103,162-170,164-166,171-175,176-180,181-182,193-206",
       "python3 /tmp/Read06-OG2G/numbered.py /tmp/Read06-OG2G/fleet/tameshi-shokunin/corpus/knowledge/mutation-case-kimi-census.md:29-37,82-89",
       "python3 /tmp/Read06-OG2G/numbered.py /tmp/Read06-OG2G/fleet/tameshi-shokunin/corpus/knowledge/gates-survey-kagi.md:318-362",
       "sh -c 'GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh > /tmp/Read06-OG2G/kagi-surface-census.sh && sha256sum /tmp/Read06-OG2G/kagi-surface-census.sh && wc -c < /tmp/Read06-OG2G/kagi-surface-census.sh && wc -l < /tmp/Read06-OG2G/kagi-surface-census.sh && timeout 120 bash /tmp/Read06-OG2G/kagi-surface-census.sh --selftest; echo \"selftest_exit=$?\"'",
       "sh -c 'GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs > /tmp/Read06-OG2G/kimi-census.mjs && sha256sum /tmp/Read06-OG2G/kimi-census.mjs && wc -c < /tmp/Read06-OG2G/kimi-census.mjs && wc -l < /tmp/Read06-OG2G/kimi-census.mjs && timeout 120 node /tmp/Read06-OG2G/kimi-census.mjs --selftest; echo \"selftest_exit=$?\"'",
       "sh -c 'GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs > /tmp/Read06-OG2G/kimi-census-10.mjs && sha256sum /tmp/Read06-OG2G/kimi-census-10.mjs && python3 /tmp/Read06-OG2G/numbered.py /tmp/Read06-OG2G/kimi-census-10.mjs:430-460,471-512 && grep -n -E \"FAIL|spawnSync|execFileSync|execSync|spawn\\(|mkdtemp|writeFileSync|mkfifo|symlink|pass\" /tmp/Read06-OG2G/kimi-census-10.mjs'",
       "sh -c 'grep -n -E \"SELFTEST|FAIL|cases\" /tmp/Read06-OG2G/kagi-surface-census.sh | cut -c1-170; echo ===; python3 /tmp/Read06-OG2G/numbered.py /tmp/Read06-OG2G/fleet/tameshi-shokunin/corpus/knowledge/mutation-case-kimi-census.md:40-62'",
       "sh -c 'grep -n -i -E \"interior|unprobed\" corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kimi-census.md; echo \"grep_exit=$?\"; python3 -c \"import sys;d=open(sys.argv[1],\\\"rb\\\").read();print(\\\"kagi gate split-lines=\\\",len(d.split(b\\\"\\\\n\\\")),\\\"last-byte=\\\",repr(d[-1:]),\\\"newlines=\\\",d.count(b\\\"\\\\n\\\"))\" /tmp/Read06-OG2G/kagi-surface-census.sh'",
       "sh -c 'GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read06-OG2G/fleet/tameshi-shokunin cat-file -t 91edf9cd82ccc72e10f62f81d37181f549d593b8 && GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read06-OG2G/fleet/tameshi-shokunin diff --stat 91edf9cd82ccc72e10f62f81d37181f549d593b8 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 -- PROVINCE.md && GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read06-OG2G/fleet/tameshi-shokunin diff -U0 91edf9cd82ccc72e10f62f81d37181f549d593b8 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 -- PROVINCE.md | grep \"^@@\"'",
       "python3 /tmp/Read06-OG2G/numbered.py /tmp/Read06-OG2G/fleet/tameshi-shokunin/.ufo/waves/round-26/w1/ColdreadPilot.md:183-251,304-362",
       "sh -c 'GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read06-OG2G/fleet/tameshi-shokunin rev-parse 91edf9cd82ccc72e10f62f81d37181f549d593b8:PROVINCE.md 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:PROVINCE.md && GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read06-OG2G/fleet/tameshi-shokunin rev-parse 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:SKILL.md && GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read06-OG2G/fleet/tameshi-shokunin rev-parse 2227d8338c02aa9a5fd7d95c1a41b76865ad7647^{tree}'",
       "sha256sum tools/trace-inputs.py .ufo/waves/round-26/w1/ColdreadPilot.md PROVINCE.md",
       "sh -c 'grep -n \"Erratum R21\" corpus/knowledge/mutation-case-kagi-census.md; python3 /tmp/Read06-OG2G/numbered.py /tmp/Read06-OG2G/kagi-surface-census.sh:745-765,776-790'"
     ],
     "opened": ["SKILL.md", "PROVINCE.md", "tools/trace-inputs.py", ".ufo/waves/round-26/w1/ColdreadPilot.md"],
     "inputs": {
       "PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be",
       "plans/round-3.plan.md": "2200c8896b46b583006f4a72a1d7e9b5c4f7b1bfd40e14210727114d73b4552f",
       "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
       "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
       "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
       ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7",
       "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
     },
     "external_inputs": {
       "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
       "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426"
     },
     "traces": [
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-1.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-2.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-3.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-4.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-5.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-6.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-7.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-8.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-9.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-10.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-11.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-12.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-13.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-14.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-15.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-16.json",
       "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read06-17.json"
     ]
    }
  ]
}
```

## Plain-English note

I read the section from a detached clone at the pinned revision and opened its cited files under the trace collector. I then checked each figure I could against those files and against the pinned sibling gates at their pinned revisions. The section is a record. Most of it holds: the kill and case counts, the restore pins, the abstention and token-only examples, the plan lines, the two-lane rule, and the JS and bash gate mechanics. The one real defect is the present-tense band-interiors sentence. Its cited census lines do not say it, and the page itself has since superseded it. The other items are citation precision problems, one of which points at text the note itself retracts. I did not re-run the mutant sweeps.

COLDREAD Read06: wrong-expectation
