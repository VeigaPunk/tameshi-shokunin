# ReRead02: round-27 residual cold reads, two SKILL.md sections at b1cc95e

Verdicts: line 405 gap-minor; line 1905 gap-minor. Neither section is blocked, and I found no wrong expectation. Every number, hash and output format I could test matches its source, and the rules rest on the cited cases. The defects are pointer and wording errors, listed here by consequence. The clone is /tmp/ReRead02-gKi4/fleet/tameshi-shokunin, detached at b1cc95e, and SKILL.md hashes to fce54977...1924f.

## Minor gaps, line 405 (class record)

1. Stale pointer, most consequential. The clause "JS uses filesystem fixtures/subprocesses, DRIFT prefix checks and an exact CLEAN assertion" cites mutation-case-kagi-census.md:171-175. Lines 172-174 there say the JS suite "shares in-memory fixtures and asserts exact verdict lines". The R21 erratum in the same file (lines 261-270) retracts that reading, and the section does not cite it. The clause itself holds at kumitate scripts/kimi-census.mjs at 175de6ba: fixture writes at lines 431-455, mkdtempSync at 472, spawnSync at 458, DRIFT prefix assert at 498, exact CLEAN assert at 512. Smallest fix: cite census lines 261-270 and kimi-census.mjs lines 430-515 for this clause.
2. Ambiguous bare pointer. "verb-path U2 and host-stability U5 remain open (:193-206)" follows SKILL.md pointers, so a reader opens SKILL.md:193-206. That range is the adjudication rule block and holds no U2 or U5 text. The text is mutation-case-kagi-census.md:193-206 (section 6; U2 at 197-198, U5 at 203-204). Smallest fix: name the file.
3. Unqualified summary string. "SELFTEST: FAIL (1/16 cases)" is attributed to mutation-case-kagi-census.md:82-103, which does not contain it. The format is correct: kagi corpus/surface-census.sh at fecee874 line 847 prints it. Smallest fix: cite line 847 or the kill table at census line 67. The same pointer sits at SKILL.md:198-199, outside this section.
4. "27/43 pass" sits under a bash-only citation. The JS example is mutation-case-kimi-census.md:44, and kimi-census.mjs line 852 prints the format. Smallest fix: add the kimi pointer.
5. Omitted nuance. Kimi census lines 215-238 (errata E2) say the 6-or-more-findings region of D2 is also fixture-unreached, while classing D2 as assert-caused. The section's split (JS survivors are unasserted values; B5 is the unreached-arm class) follows E2's classing but does not say so. Smallest fix: add "per E2, kimi census lines 215-238".
6. Unmarked inference. "B5's shape matches the F-2 bypass-class hole pattern" is an analogy. B5 is a non-adversarial fixture-absent arm (kagi census lines 107-116). F-2 concerns claim-ledger.sh refusal paths that executors bypassed (gates-survey-kagi.md lines 326-363). Smallest fix: mark the sentence (I).

## Minor gaps, line 1905 (class record)

1. Table row 3, second cell "detail text", does not describe S_DUP_LINE. That mutant changes the reported finding line (index + 1 becomes index + 2, sources-check.defects.spec lines 43-46), and the entry says no case asserts the line (entry lines 137-139). Smallest fix: name the finding line for S_DUP_LINE and the positive entriesWithSource count for S_ENTRY_COUNT.
2. "seat Read34" is present only as a string in round-26 wave files at b1cc95e (.ufo/waves/round-26/dispatch-w2.json, spec-w2.json, w2/swarm-registry.json). Its link to the js-cite-check run was not checked, so treat that parenthetical as unverified.

## Residual risk and verification gaps

- The replay receipt ReRead02-6 records dropped_home_count 5529. Home-directory accesses are therefore absent from its inputs.
- The replay ran once, at b1cc95e, with exit 0 and a wall time of 223.75 s. Its workdir is /tmp/ReRead02-gKi4/replay-work, kept outside the lane.
- Not re-run: the round-18 runner (cases=8), the four survivor probes other than S_KIND, and the standalone sweeps (only the replay's copies ran).
- Outside this section, SKILL.md:339-340 cites PROVINCE.md:16-17 for the two-lane bar. The bar sits at PROVINCE.md:15-16. This is for the L1.
- Setup and metadata commands ran outside the collector: clone and symlink creation, ls, wc, glob, sha256sum and git show on sibling objects, git metadata on the clone (cat-file, show -s, show --stat, merge-base, ls-tree, rev-parse), git grep of tools and round-26 paths, and one untraced numbered read of the two census files, which ReRead02-2 repeats over the same bytes. I also read my own receipts by hand to copy hashes. The sibling git show bytes are the external_inputs; the rest are not cited inputs.
- SCORECARD.md, LOG.md and .ufo/evidence/round-21/coldread/ledger.json were not opened by path or under the collector.
- No tool was installed or upgraded, so there is nothing to record. No git write, jj command, sibling write or seat spawn was run. The only lane writes are the eight receipts and this report. One early write landed at the fleet root by mistake (a relative path). I moved it into the lane with MV, and the fleet-root copy no longer exists.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ReRead02",
  "skill_sha256": "fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f",
  "read_rev": "b1cc95e1fb62532646d74e2863770c4fed0851cc",
  "sections": [
    {
      "start": 405,
      "heading": "## Cross-language divergence \u2014 bash vs JS (round 3, measured)",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Stale pointer, most consequential: the clause that JS uses filesystem fixtures and subprocesses, DRIFT prefix checks and an exact CLEAN assertion cites mutation-case-kagi-census.md lines 171-175. Lines 172-174 there say the JS suite shares in-memory fixtures and asserts exact verdict lines. The R21 erratum in the same file (lines 261-270) retracts that reading and is not cited. The clause itself holds at kumitate scripts/kimi-census.mjs at 175de6ba: fixture writes at lines 431-455, mkdtempSync at 472, spawnSync at 458, DRIFT prefix assert at 498, exact CLEAN assert at 512. Smallest fix: cite census lines 261-270 and kimi-census.mjs lines 430-515 for this clause.",
        "Ambiguous bare pointer: 'verb-path U2 and host-stability U5 remain open (:193-206)' follows SKILL.md pointers, so a reader opens SKILL.md lines 193-206, which is the adjudication rule block and holds no U2 or U5 text. The text is mutation-case-kagi-census.md lines 193-206 (section 6; U2 at 197-198, U5 at 203-204). Smallest fix: name the file.",
        "Unqualified summary string: 'SELFTEST: FAIL (1/16 cases)' is attributed to mutation-case-kagi-census.md lines 82-103, which do not contain it. The format is correct: kagi corpus/surface-census.sh at fecee874 line 847 prints it. Smallest fix: cite line 847 or the kill table at census line 67. The same pointer sits at SKILL.md lines 198-199, outside this section.",
        "'27/43 pass' sits under a bash-only citation; the JS example is mutation-case-kimi-census.md line 44, and kimi-census.mjs line 852 prints the format. Smallest fix: add the kimi pointer.",
        "Omitted nuance: kimi census lines 215-238 (errata E2) say the 6-or-more-findings region of D2 is also fixture-unreached, while classing D2 as assert-caused. The section's split (JS survivors are unasserted values; B5 is the unreached-arm class) follows E2's classing but does not say so. Smallest fix: add 'per E2, kimi census lines 215-238'.",
        "Unmarked inference: 'B5's shape matches the F-2 bypass-class hole pattern' is an analogy. B5 is a non-adversarial fixture-absent arm (kagi census lines 107-116). F-2 concerns claim-ledger.sh refusal paths that executors bypassed (gates-survey-kagi.md lines 326-363). Smallest fix: mark the sentence (I)."
      ],
      "commands_executed": [
        "python3 tools/trace-inputs.py --root <clone> --out <lane>/.ufo/evidence/round-27/coldread/traces/ReRead02-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" plans/round-3.plan.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/gates-survey-kagi.md PROVINCE.md",
        "python3 tools/trace-inputs.py --root <clone> --out <lane>/.ufo/evidence/round-27/coldread/traces/ReRead02-2.json -- python3 -c \"\nimport sys\nfor a in sys.argv[1:]:\n    p, _, r = a.partition(':')\n    lo, hi = ((int(x) for x in r.split('-')) if r else (1, 10**9))\n    print('=== ' + a)\n    for i, l in enumerate(open(p, encoding='utf-8'), 1):\n        if lo <= i <= hi:\n            print(str(i) + '\\t' + l.rstrip('\\n'))\n\" corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kimi-census.md",
        "python3 tools/trace-inputs.py --root <clone> --out <lane>/.ufo/evidence/round-27/coldread/traces/ReRead02-3.json -- python3 -c \"\nimport sys\nfor a in sys.argv[1:]:\n    p, _, r = a.partition(':')\n    lo, hi = ((int(x) for x in r.split('-')) if r else (1, 10**9))\n    print('=== ' + a)\n    for i, l in enumerate(open(p, encoding='utf-8'), 1):\n        if lo <= i <= hi:\n            print(str(i) + '\\t' + l.rstrip('\\n'))\n\" plans/round-3.plan.md PROVINCE.md:1-30 corpus/knowledge/gates-survey-kagi.md:318-368"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/gates-survey-kagi.md",
        "plans/round-3.plan.md",
        "PROVINCE.md"
      ],
      "inputs": {
        "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
        "plans/round-3.plan.md": "2200c8896b46b583006f4a72a1d7e9b5c4f7b1bfd40e14210727114d73b4552f",
        "PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be"
      },
      "external_inputs": {
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead02-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead02-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead02-3.json"
      ]
    },
    {
      "start": 1905,
      "heading": "## Eighth recorded case \u2014 round 18",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Table row 3, second cell 'detail text', does not describe S_DUP_LINE. That mutant changes the reported finding line (index + 1 becomes index + 2, sources-check.defects.spec lines 43-46), and the entry says no case asserts the line (entry lines 137-139). Smallest fix: name the finding line for S_DUP_LINE and the positive entriesWithSource count for S_ENTRY_COUNT.",
        "'seat Read34' is present only as a string in round-26 wave files at b1cc95e (.ufo/waves/round-26/dispatch-w2.json, spec-w2.json, w2/swarm-registry.json). Its link to the js-cite-check run was not checked, so treat that parenthetical as unverified."
      ],
      "commands_executed": [
        "python3 tools/trace-inputs.py --root <clone> --out <lane>/.ufo/evidence/round-27/coldread/traces/ReRead02-4.json -- python3 -c \"\nimport sys\nfor a in sys.argv[1:]:\n    p, _, r = a.partition(':')\n    lo, hi = ((int(x) for x in r.split('-')) if r else (1, 10**9))\n    print('=== ' + a)\n    for i, l in enumerate(open(p, encoding='utf-8'), 1):\n        if lo <= i <= hi:\n            print(str(i) + '\\t' + l.rstrip('\\n'))\n\" corpus/knowledge/mutation-case-kumitate-sources-check.md .ufo/evidence/round-18/sources-check/suite.txt .ufo/evidence/round-18/sources-check/control.txt .ufo/evidence/round-18/sources-check/predictions.json .ufo/evidence/round-18/sources-check/sources-check.defects.spec tools/mutate-and-run.sh:1-80",
        "python3 tools/trace-inputs.py --root <clone> --out <lane>/.ufo/evidence/round-27/coldread/traces/ReRead02-5.json -- python3 -c \"\nimport re, sys\npat = re.compile(r'js-sources-check|js-cite-check|REGRESSION|--regression|mkdir|open\\(|write|rm -rf|kumitate|sibling|LANE|-C |/\\.\\./|git -C|git --git-dir|\\bcp\\b|sed -i|> ')\nfor a in sys.argv[1:]:\n    p, _, r = a.partition(':')\n    lo, hi = ((int(x) for x in r.split('-')) if r else (1, 10**9))\n    print('=== ' + a)\n    for i, l in enumerate(open(p, encoding='utf-8'), 1):\n        if lo <= i <= hi and (r or pat.search(l)):\n            print(str(i) + '\\t' + l.rstrip('\\n')[:260])\n\" tools/mutate-and-run.sh",
        "python3 tools/trace-inputs.py --root <clone> --out <lane>/.ufo/evidence/round-27/coldread/traces/ReRead02-6.json -- bash tools/mutate-and-run.sh --regression --workdir /tmp/ReRead02-gKi4/replay-work",
        "python3 tools/trace-inputs.py --root <clone> --out <lane>/.ufo/evidence/round-27/coldread/traces/ReRead02-7.json -- python3 -c \"\nimport sys, os\nfor d in sys.argv[1:]:\n    print('=== DIR ' + d)\n    for root, dirs, files in os.walk(d):\n        for f in sorted(files):\n            print(os.path.join(root, f) + '\\t' + str(os.path.getsize(os.path.join(root, f))))\nprint('=== FILE .ufo/evidence/round-18/sources-check/control/repeat-hashes.json')\nprint(open('.ufo/evidence/round-18/sources-check/control/repeat-hashes.json', encoding='utf-8').read()[:4000])\nprint('=== FILE .ufo/evidence/round-18/sources-check/control/repeat-control.stdout')\nprint(open('.ufo/evidence/round-18/sources-check/control/repeat-control.stdout', encoding='utf-8').read()[:600])\n\" .ufo/evidence/round-18/sources-check/survivor-probes .ufo/evidence/round-18/sources-check/sweep",
        "python3 tools/trace-inputs.py --root <clone> --out <lane>/.ufo/evidence/round-27/coldread/traces/ReRead02-8.json -- python3 -c \"\nimport sys\nfiles = [\n '.ufo/evidence/round-18/sources-check/sweep/sweep.txt',\n '.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-help.txt',\n '.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-help.txt',\n '.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-check.json',\n '.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-check.json',\n '.ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/transcript.txt',\n]\nfor p in files:\n    print('=== ' + p)\n    for i, l in enumerate(open(p, encoding='utf-8'), 1):\n        print(str(i) + '\\t' + l.rstrip('\\n')[:300])\n\""
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kumitate-sources-check.md",
        ".ufo/evidence/round-18/sources-check/suite.txt",
        ".ufo/evidence/round-18/sources-check/control.txt",
        ".ufo/evidence/round-18/sources-check/predictions.json",
        ".ufo/evidence/round-18/sources-check/sources-check.defects.spec",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/sources-check/control/repeat-control.stdout",
        ".ufo/evidence/round-18/sources-check/control/repeat-hashes.json",
        ".ufo/evidence/round-18/sources-check/sweep/sweep.txt",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-check.json",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-check.json",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-help.txt",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-help.txt",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/transcript.txt"
      ],
      "inputs": {
        ".ufo/evidence/round-18/sources-check/control.txt": "74061bdf3d1f6bfe5a066c5c454678ae8647d2c5d123f6d4bea182093158d1a0",
        ".ufo/evidence/round-18/sources-check/predictions.json": "5749a27a92c862278a2c77307496f2b80b3c6619c6125def0ea0066b7252d35f",
        ".ufo/evidence/round-18/sources-check/sources-check.defects.spec": "c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91",
        ".ufo/evidence/round-18/sources-check/suite.txt": "6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b",
        "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        ".ufo/evidence/round-18/sources-check/control/repeat-control.stdout": "7e5e646eb8dc41348425540104ae84d399158b768c5e05b89902556ef12390e3",
        ".ufo/evidence/round-18/sources-check/control/repeat-hashes.json": "79d94d2756a9639cd2999c741af200f16237969a11e8869d4106b79e7bf6bb37",
        ".ufo/evidence/round-18/sources-check/sweep/sweep.txt": "4ba2a595668439e6ca77bdb26fb462e71e88fe9079a50a77ea9e7d7ff2586097",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-check.json": "4666ccc69425289143cb81156fc382ddaffdc42f98a61ef5596ebd12d1f617a0",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-check.json": "4666ccc69425289143cb81156fc382ddaffdc42f98a61ef5596ebd12d1f617a0",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/mutant-help.txt": "55b9fc15f833c6c5d4aa0982e2b6f05a8c3ae63e428b6eb97ee4feb5c97e7578",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/pristine-help.txt": "f1d41678d8478f08089abc6650be113aae3271151ae72ee632a4250e23949bb1",
        ".ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/transcript.txt": "3b74a6c85a033315774871891f7a54e8ecde9dfcb29fba8cb2caca194226f175"
      },
      "external_inputs": {
        "kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs": "6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead02-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead02-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead02-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead02-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead02-8.json"
      ]
    }
  ]
}
```

## Note: what I checked

- Line 405. I checked the sizes and hashes of both pinned artifacts against git show (kagi surface-census.sh at fecee874, kimi-census.mjs at 175de6ba), the 8/10 headline, the 11-run costs, the restore hashes, the calibration counts, and the output grammar in both source files. I confirmed the ESM imports, the plan's anti-claim lines, the PROVINCE two-lane rule, the SKILL.md band lines, and the round-5 60 % line. The R21 erratum was checked against the pinned JS source. That source supports the section's fixture clause, while the cited census lines contradict it.
- Line 1905. I checked the pinned sources-check.mjs hash, line count and mode. I checked the pre-registration commit 93d22aa: its committer time is 2026-10-20T16:40:21-03:00 (19:40:21Z), before the first mutant run at 19:41:29Z. I checked the control hashes (eight identical runs), the leg's presence at b1cc95e, the five survivor probe directories, the S_KIND outputs (corpus output hashes match; help output differs by the 16-byte token), and the READ_FAILED fixture path through sources-check.mjs lines 344-356 and 790. I ran the regression replay in the /tmp clone under the collector. It passed with cases=9 passed=9, and the js-sources-check leg matched 10/10.
- Not verified: the seat name Read34, beyond its presence in round-26 files. The round-18 runner's 8/8 figure is historical and was not re-run.
- Note on receipts: ReRead02-1 to -8 each report rev b1cc95e and exit 0. Hashes in inputs come from those receipts. In commands_executed, <clone> means /tmp/ReRead02-gKi4/fleet/tameshi-shokunin and <lane> means /home/vgpnk/Projects/shokunin/tameshi-shokunin.

COLDREAD ReRead02: gap-minor, gap-minor
