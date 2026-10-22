# Read38: cold read of SKILL.md:2086, "## Ninth recorded case — round 26"

Verdict: wrong-expectation. Every measured fact I could check holds at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647: the pin, the 5/10 and 10/10 counts, the pre-registration order, the env -i suite string, the five wave-1 probe verdicts, the S_EMPTY_GUARD equivalence argument, and the K_FENCE_TILDE error pattern. The replay is checked against recorded output only (M1). One justification fails. The parenthetical at SKILL.md:2108 says "Stryker cannot mark equivalents, S089". StrykerJS's current docs say it can, by comment. The bucket should stay uncredited until that clause is fixed. The fix is one clause (see the note).

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read38",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 2086,
      "heading": "## Ninth recorded case \u2014 round 26",
      "class": "record",
      "verdict": "wrong-expectation",
      "blocking_gaps": [],
      "wrong_expectations": [
        "SKILL.md:2108 keeps S_EMPTY_GUARD as a survivor because 'Stryker cannot mark equivalents, S089'. The S089 row (corpus/SOURCES.md:98) says equivalent mutants 'cannot be found or marked automatically'; the section drops 'automatically'. The StrykerJS Disable mutants page (https://stryker-mutator.io/docs/stryker-js/disable-mutants/, read 2026-10-22) documents '// Stryker disable next-line <mutator>: <reason>' (available since Stryker 5.4), which marks a mutant Ignored and keeps it out of the mutation score, with an equivalent-mutant example. The flat claim does not hold for StrykerJS today. Smallest correction: replace the parenthetical with '(Stryker cannot find or mark equivalents automatically, S089; a manual // Stryker disable comment needs an editable source, and kumitate's gate is read-only here)'. The decision to keep S_EMPTY_GUARD as a survivor is not affected."
      ],
      "minor_gaps": [
        "M1 replay not re-run: SKILL.md:2094-2095 was checked against the recorded output .ufo/evidence/round-26/cite-check/regression-worktree.stdout (lines 49-50: REGRESSION_CASE js-cite-check: PASS; REGRESSION: PASS cases=9 passed=9). Its REGRESSION_TOOL sha256 fb91ef76... equals tools/mutate-and-run.sh at this rev (receipt 01). This seat did not start a fresh run: the section is a record, and the host runs at load 16 on 32 cores (receipt 10).",
        "M2 no pointers for the wave-1 claims: SKILL.md:2096-2100 and the table rows name no report. Name .ufo/waves/round-26/w1/ProbeSOOREDGE.md, ProbeSSTRICT.md, ProbeSUSAGE.md, ProbeSPININCLUDES.md, ProbeSEMPTYGUARD.md, ProbeIntegrations.md and CriticEquivalence.md.",
        "M3 sweep runner: sweep/sweep.txt:1 records MUTATE_TOOL sha256 d22c4025... (an earlier runner), not the runner at this rev (fb91ef76...). The replay reproduces the table (regression-worktree.stdout:47, match=10/10), so the counts stand. The Sweep pointer at SKILL.md:2093 does not say which runner produced the file.",
        "M4 scope: 'kills none of the five' (SKILL.md:2098-2100) holds for the live trees as they stood on 2026-10-22 (ProbeIntegrations.md:5-7 and :241 say the trees are mutable). Add that date and scope.",
        "M5 usage row: SKILL.md:2106 gives an unknown flag as the example of what the suite does not pin. The mutated line cite-check.mjs:2512 returns 64 for any error thrown by parseArgs (the catch at :2510-2512), and an unknown argument is one such throw (:270). The example is correct, but it names one of several paths.",
        "M6 timing: 'committed before any mutant ran' (SKILL.md:2091) rests on two self-reported stamps: the git committer date of 622d31d (2026-10-22T07:01:47-03:00, receipt 04) and the runner's MUTATE_DATE (sweep.txt:2, 10:02:07Z). Neither is independently anchored."
      ],
      "commands_executed": [
        "bash -c 'for f in <nine lane files>; do echo $f; sha256sum $f; wc -l < $f; done' (exit 0; receipt Read38-01)",
        "python3 /tmp/Read38-wXX3/scratch/cmp.py (predictions, results.tsv, spec and sweep.txt checks; exit 0; receipt Read38-02)",
        "bash -c 'grep -nE <js-cite-check|js-sources-check|js-round-gate|--regression|REGRESSION_CASE|cases=|env -i> tools/mutate-and-run.sh' (exit 0; receipt Read38-03)",
        "bash -c 'git cat-file -t 622d31d; git show -s 622d31d; git merge-base --is-ancestor 622d31d HEAD; git show --stat 622d31d; sha256 of predictions.json and cite-check.defects.spec at 622d31d; git log -3 on sweep.txt' (exit 0; receipt Read38-04)",
        "bash -c 'git -C ../kumitate-shokunin cat-file -t 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a; git -C ../kumitate-shokunin ls-tree 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a scripts/cite-check.mjs; git -C ../kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > /tmp/Read38-wXX3/scratch/pin-cite-check.mjs; sha256sum; wc -lc' (exit 0; receipt Read38-05)",
        "bash -c 'sha256sum /tmp/Read38-wXX3/scratch/pin-cite-check.mjs; grep -nE <filesScanned, totals.resolved, resolved increments, return 64, return 65, LINE_OOR, startsWith, opts.strict, fence content, R16 repro, insideFence, --integrations, --selftest> on that copy' (exit 0; receipt Read38-06)",
        "python3 /tmp/Read38-wXX3/scratch/probes.py (verdict lines and last lines of the seven wave-1 reports; exit 0; receipt Read38-07)",
        "bash -c 'cat corpus/knowledge/mutation-case-kumitate-cite-check.md' (exit 0; receipt Read38-08)",
        "bash -c 'grep -nE for the S088 and S089 rows in corpus/SOURCES.md' (exit 0; receipt Read38-09)",
        "bash -c 'nproc; cat /proc/loadavg; command -v node git python3 strace uv' (exit 0; receipt Read38-10)",
        "python3 /tmp/Read38-wXX3/scratch/src_read.py (greps and line ranges of the pinned gate; exit 0; receipt Read38-11)",
        "python3 /tmp/Read38-wXX3/scratch/probe_read.py (witness and integration lines of the probe reports; exit 0; receipt Read38-12)",
        "bash -c 'sha256sum and grep -nE over sweep/evidence/K_FENCE_TILDE.out' (exit 0; receipt Read38-13)",
        "bash -c 'sha256sum and wc -l over corpus/SOURCES.md and the seven wave-1 probe and critic reports' (exit 0; receipt Read38-14)",
        "bash -c 'stat birth and modified times, then ls, of the misplaced report path (metadata only; exit 0; receipt Read38-15)",
        "bash -c 'mkdir -p and mv -n of the misplaced report into the lane path, then rmdir of the two fleet-root directories this seat created (exit 0; receipt Read38-16)"
      ],
      "opened": [
        "SKILL.md",
        "tools/trace-inputs.py",
        "tools/mutate-and-run.sh",
        ".ufo/waves/round-26/w1/ColdreadPilot.md",
        ".ufo/evidence/round-26/cite-check/sweep/sweep.txt",
        ".ufo/evidence/round-26/cite-check/sweep/results.tsv",
        ".ufo/evidence/round-26/cite-check/sweep/defects.tsv",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/K_FENCE_TILDE.out",
        ".ufo/evidence/round-26/cite-check/predictions.json",
        ".ufo/evidence/round-26/cite-check/cite-check.defects.spec",
        ".ufo/evidence/round-26/cite-check/regression-worktree.stdout",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md",
        "corpus/SOURCES.md",
        ".ufo/waves/round-26/w1/ProbeSOOREDGE.md",
        ".ufo/waves/round-26/w1/ProbeSSTRICT.md",
        ".ufo/waves/round-26/w1/ProbeSUSAGE.md",
        ".ufo/waves/round-26/w1/ProbeSPININCLUDES.md",
        ".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md",
        ".ufo/waves/round-26/w1/ProbeIntegrations.md",
        ".ufo/waves/round-26/w1/CriticEquivalence.md"
      ],
      "inputs": {
        ".ufo/evidence/round-26/cite-check/cite-check.defects.spec": "969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208",
        ".ufo/evidence/round-26/cite-check/predictions.json": "f1d26201ffac81fdd7415ac325165807c0f721f841ec5608636ba415879c938e",
        ".ufo/evidence/round-26/cite-check/regression-worktree.stdout": "cf6e07b6d4251c466f1f68d5e406e0300b8daa8614e17edc69b6a0b6906ee6e5",
        ".ufo/evidence/round-26/cite-check/sweep/defects.tsv": "ddbfa4f932527afc98ec4f4c86e5789247f3fc0d5fa52a84089b51761fbb812c",
        ".ufo/evidence/round-26/cite-check/sweep/results.tsv": "daa25ff90a7982db74f9dd8d1fbde79265b17f4e829ded05b0b621f00a81112d",
        ".ufo/evidence/round-26/cite-check/sweep/sweep.txt": "957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/K_EMPTY_VERDICT.out": "3848ec7854b9c35a60f8820a17dd4d195f82c7ecb317b35ef9b02d4c952b4ef9",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/K_FENCE_TILDE.out": "7ef8a0cc2aaf6f471010554d4f7d4ccbbed34cc6cbb120f6b33220c7d2384913",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/K_MISSING_WORD.out": "19f16b8f973b43539e54fdd3205a37a91ed13fb9ad1efefd253d34f0d8d84018",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/K_PIN_KIND.out": "79beba1b390a34dda175807453c05cb93205a85af0389e324752c3dd1b82f85d",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/K_UNRESOLVED_SEV.out": "435d26b1fd9bf00962f451743a98f3f3534d1b519192a875d92f460b334e278e",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/S_EMPTY_GUARD.out": "280dfc28d5c84f2506d9795bb1d16731d2a135f209fe9005bee99cbaaf24bc4f",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/S_OOR_EDGE.out": "7a450a0e1b91daa552bc1badd0f664e9ff49fad073f98133cd239427d2c72fc9",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/S_PIN_INCLUDES.out": "da1b07c4860618fc9be12d8b1e3fea068bfe42eccf8348fa2da1c30bf032dbd7",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/S_STRICT.out": "78460de57b070be56e220708cecdee12656dad96b380a120c6755edc6aed73c6",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/S_USAGE.out": "e7c06ea20401d916b61d66f008eadb1b340b9b4e890977793de30d68ef77b58d",
        ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7",
        ".ufo/waves/round-26/w1/CriticEquivalence.md": "575ef324cba9b25c56ad8dd4ea4d251fb2c4941505a11b76b25a777f10d22285",
        ".ufo/waves/round-26/w1/ProbeIntegrations.md": "ac1b2c47e6a3e39ebadcb4c36cc421007e4e43fd61f836e02b0e2d2c95f1006b",
        ".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md": "7be4dc4cf29ee7d62c6a494627cafb33d2035072c174189b00bd52753b96ccd9",
        ".ufo/waves/round-26/w1/ProbeSOOREDGE.md": "c0cd5194f6162f2f6d91531f0a512eace80cf2028b8f25505d45b8e976af4e04",
        ".ufo/waves/round-26/w1/ProbeSPININCLUDES.md": "bc297eb2ae9ad42e504cfd2777627147988b146b3ad6cebce122a068bd2d5a5c",
        ".ufo/waves/round-26/w1/ProbeSSTRICT.md": "19ef870f885ce37fb9f34570347fe87f034913ba465491df1950a878fea98153",
        ".ufo/waves/round-26/w1/ProbeSUSAGE.md": "d82bb2823e63952fa7614da1bd2ea359e902f1fa719844f5386f75de53a4beeb",
        "corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
      },
      "external_inputs": {
        "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-01.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-02.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-03.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-04.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-05.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-06.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-07.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-08.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-09.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-13.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read38-16.json"
      ]
    }
  ]
}
```

## Note (plain English)

Class: record. The section states facts with pointers. Its replay line (SKILL.md:2094) reports an outcome and asks no reader to act.

Setup (step 1, not traced, as the assignment specifies): fleet mirror at /tmp/Read38-wXX3/fleet/tameshi-shokunin, detached at 2227d83. HEAD matched and the SKILL.md sha256 matched 386de44b. The section runs from line 2086 to 2113. The next heading, "### Round-26 gate/probe registry", is at 2114.

What I checked. All 14 receipts show rev 2227d83, exit 0, no untracked inputs and no live-lane reads. Each receipt's argv field holds the exact command. The scratch scripts are in /tmp/Read38-wXX3/scratch.

- Pin (SKILL.md:2088-2089). Receipt 05: kumitate 1205c662 scripts/cite-check.mjs is blob 9770de8c, mode 100755, sha256 40573448...c10c9f, 2537 lines and 126735 bytes.
- Counts (SKILL.md:2090). Receipt 02: 10 predictions, 10 held, no mismatches. Five killed (K_EMPTY_VERDICT, K_FENCE_TILDE, K_MISSING_WORD, K_PIN_KIND, K_UNRESOLVED_SEV) and five survived. sweep/sweep.txt:106 reads "MUTATE: DONE ... killed=5 survived=5".
- Leg and suite (SKILL.md:2090, 2092). tools/mutate-and-run.sh:95 lists js-cite-check at 5/10. Receipt 03: the js-round-gate, js-sources-check and js-cite-check legs (lines 1416, 1421, 1426) share one env -i string ending in node "$MUTANT" --selftest, which matches "cases 7 and 8". The spec header (line 3) says "hermetic group only, 62 cases at the pin". cite-check.mjs:81-82 says --selftest runs the hermetic group only.
- Pre-registration (SKILL.md:2091). Receipt 04: 622d31d is an ancestor of HEAD, committed 2026-10-22T07:01:47-03:00. Its predictions.json and spec blobs equal HEAD's. sweep.txt:2 gives MUTATE_DATE 10:02:07Z.
- Pointers (SKILL.md:2093, 2095). sweep.txt and the entry both exist. The entry (receipt 08) names S_EMPTY_GUARD as equivalent in its section 4 table.
- Replay (SKILL.md:2094-2095). Checked against regression-worktree.stdout lines 49-50 (REGRESSION_CASE js-cite-check: PASS; REGRESSION: PASS cases=9 passed=9). That file's runner sha256 fb91ef76... equals tools/mutate-and-run.sh at this rev (receipt 01). I did not re-run it (M1).
- Wave 1 (SKILL.md:2096-2100). Receipt 07: ProbeSOOREDGE.md:262, ProbeSSTRICT.md:426, ProbeSUSAGE.md:301 and ProbeSPININCLUDES.md:372 end with DISTINGUISHED. ProbeSEMPTYGUARD.md:574 ends with EQUIVALENT. ProbeSSTRICT.md:94 calls its probe "Purely hermetic: temp trees only". The probes drive the public CLI, not --selftest. So "four holes, each with a hermetic witness" holds.
- Integrations (SKILL.md:2098-2100). ProbeIntegrations.md:3-14 and :132: no survivor is killed. The pristine pin is red on the live trees (6 of 9 cases, exit 1). With no live tree it is a green no-op (:301). The sentence holds, with scope gap M4.
- S_EMPTY_GUARD equivalence (the proof behind SKILL.md:2097). cite-check.mjs:1556 increments totals.filesScanned for each document that reads. :1583 is the only increment of totals.resolved, and it sits in the same loop body after that. :1590 is the verdict. Nothing decrements either counter (receipt 11). So resolved > 0 implies filesScanned > 0, and the claim holds for the pinned bytes.
- Table rows (SKILL.md:2104-2108). S_OOR_EDGE: :1312 checks ref.start > n || ref.end > n. The LINE_OOR assertion at :1883-1884 cites :999, and the check at :1943-1944 accepts either REF_OWNER_AMBIG or LINE_OOR for :12. S_STRICT: no selftest check uses strict (receipt 11), and :1589 holds the drift expression. S_USAGE: :2512 is the parse-error return. S_PIN_INCLUDES: :1195 is startsWith. The sweep shows all four survive 62/62, so no hermetic case pins these edges.
- Error pattern (SKILL.md:2110-2112). The named case at cite-check.mjs:1999-2005 compares backtick and tilde results for equality. K_FENCE_TILDE.out:24 shows both as UNRESOLVED/error@line7 under the mutant, so it passes. The two failures are the absolute asserts inside === 0 at :2020-2024 and :2109-2115 (K_FENCE_TILDE.out:27 and :39; receipt 13). The sweep reads 60/62.
- Sources. corpus/SOURCES.md:97-98 (S088, S089) exist (receipt 09). I read the S089 page (stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/) by ordinary fetch today. Its line reads: "There is no definitive way for Stryker to find and ignore them. There is currently also no way yet to mark them to be ignored."

The wrong expectation (SKILL.md:2108). The section says "(Stryker cannot mark equivalents, S089)". The lane's S089 row says "cannot be found or marked automatically", so the section dropped the word "automatically". The StrykerJS Disable mutants page (stryker-mutator.io/docs/stryker-js/disable-mutants/, read today by ordinary fetch) documents "// Stryker disable next-line EqualityOperator: <reason>", available since Stryker 5.4. It says disabled mutants keep the ignored status and do not affect the score, and it gives an equivalent-mutant example. So Stryker can mark an equivalent mutant by hand. The S089 page is stale on this point. The decision still stands for another reason. The mutant is a byte edit to kumitate's read-only gate, and the entry's opening paragraph says "Kumitate owns the gate; tameshi owns the method and this measurement only". No Stryker comment can be placed in that file, and the table is pre-registered.

Smallest correction (SKILL.md:2108). Replace the parenthetical with: (Stryker cannot find or mark equivalents automatically, S089; a manual // Stryker disable comment needs an editable source, and kumitate's gate is read-only here).

Related, outside this section. corpus/knowledge/mutation-case-kumitate-cite-check.md:95-97 repeats the stale sentence "There is currently also no way yet to mark them to be ignored". The L1 should decide whether to correct it at the same time. If the clause above is corrected, I expect the bucket to fall to gap-minor on M1 to M6. A re-read would confirm that.

Minor gaps (non-blocking) are M1 to M6 in the JSON.

Discovery only. Broad greps printed fragments of other lane files: wave dispatch and spec files, earlier round coldread and monitor files, corpus/README.md, two round-26 lessons, and sweep/spec.copy. I relied on none of them, so they are not listed as inputs.

Process incident. My first write used a relative path. It resolved against the session's working directory, which is the fleet root, so the report landed at /home/vgpnk/Projects/shokunin/.ufo/waves/round-27/w1/Read38.md. The stat run (receipt 15) showed that the round-27 and w1 directories were born at the same instant as the file. I moved the file into the lane with mv -n and removed those two directories with rmdir. The fleet-root .ufo/waves directory's modification time changed as a side effect. No other fleet-root path was changed.

Tooling. Nothing was installed or upgraded in this seat. strace, node v24.21.0, git, python3 and uv were already present (receipt 10).

Residual risk and verification gaps.
- The replay was not re-run (M1). The recorded output came from the same runner bytes, so that claim rests on evidence, not on a fresh run.
- The --integrations observations came from mutable live trees on 2026-10-22. I did not re-run that group.
- "No hermetic case cites line n+1" (S_OOR_EDGE) rests on the LINE_OOR greps and on the sweep. I did not read every fixture.
- Both Stryker pages were read today, and their text can change.

COLDREAD Read38: wrong-expectation
