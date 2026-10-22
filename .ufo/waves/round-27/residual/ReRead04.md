# ReRead04 — residual cold reads, round 27

Read rev `b1cc95e1fb62532646d74e2863770c4fed0851cc`, SKILL.md sha256 `fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f` (verified on the detached fleet-mirror clone `/tmp/ReRead04-Dfcr/fleet/tameshi-shokunin` before tracing; worktree stayed clean for the whole session). All seven trace receipts carry `rev = b1cc95e1fb62532646d74e2863770c4fed0851cc`.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ReRead04",
  "skill_sha256": "fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f",
  "read_rev": "b1cc95e1fb62532646d74e2863770c4fed0851cc",
  "sections": [
    {
      "start": 827,
      "heading": "### The protocol — ordered, fail-closed",
      "class": "instruction",
      "verdict": "executed-ok",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "git show b58b26fb:tools/mutate-and-run.sh (exit 0; the pin command the section names)",
        "bash -c 'git show b58b26fb:tools/mutate-and-run.sh | wc -l; git show b58b26fb:tools/mutate-and-run.sh | sha256sum; cmp -s <(git show b58b26fb:tools/mutate-and-run.sh) tools/mutate-and-run.sh && echo PINNED-EQUALS-CURRENT || echo PINNED-DIFFERS-FROM-CURRENT' (exit 0; observed: 1001 lines, 597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b, PINNED-DIFFERS-FROM-CURRENT — current path is 2016 lines, fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de)",
        "python3 -c 'import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]' corpus/knowledge/mutation-case-mado-verify.md (exit 0)",
        "bash -c 'git show b58b26fb:tools/mutate-and-run.sh > /tmp/ReRead04-scratch/pinned-mutate-and-run.sh && chmod u+x /tmp/ReRead04-scratch/pinned-mutate-and-run.sh && /tmp/ReRead04-scratch/pinned-mutate-and-run.sh --selftest; echo selftest-exit=$?' (exit 0; observed: PASS sweep exits 0, PASS control green on pristine, PASS kill classified (K), PASS survivor classified (S), PASS kill-rate summary exact, PASS restore line OK, PASS fixture target byte-identical after sweep, PASS duplicate old string refuses (exit 2), PASS refusal is a SETUP verdict, PASS no suite run before refusal, PASS no-op edit refuses, PASS inconclusive run exits 1, PASS timeout classified inconclusive)"
      ],
      "opened": [
        "SKILL.md",
        "tools/trace-inputs.py",
        "tools/mutate-and-run.sh",
        "corpus/knowledge/mutation-case-mado-verify.md"
      ],
      "inputs": {
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3"
      },
      "external_inputs": {
        "tameshi-shokunin@b58b26fbeba8fd972e1d31ac8a9175a81e333b32:tools/mutate-and-run.sh": "597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead04-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead04-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead04-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead04-4.json"
      ]
    },
    {
      "start": 2086,
      "heading": "## Ninth recorded case — round 26",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c 'import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]' corpus/knowledge/mutation-case-kumitate-cite-check.md .ufo/evidence/round-26/cite-check/sweep/sweep.txt .ufo/evidence/round-26/cite-check/regression-worktree.stdout .ufo/evidence/round-26/cite-check/cite-check.defects.spec .ufo/evidence/round-26/cite-check/predictions.json (exit 0)",
        "python3 -c 'import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]' .ufo/waves/round-26/w1/ProbeIntegrations.md .ufo/waves/round-26/w1/ProbeSOOREDGE.md .ufo/waves/round-26/w1/ProbeSSTRICT.md .ufo/waves/round-26/w1/ProbeSUSAGE.md .ufo/waves/round-26/w1/ProbeSPININCLUDES.md .ufo/waves/round-26/w1/CriticEquivalence.md (exit 0)",
        "bash tools/mutate-and-run.sh --regression (exit 0; 223 s; observed: REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10), REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0))"
      ],
      "opened": [
        "SKILL.md",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md",
        ".ufo/evidence/round-26/cite-check/sweep/sweep.txt",
        ".ufo/evidence/round-26/cite-check/regression-worktree.stdout",
        ".ufo/evidence/round-26/cite-check/cite-check.defects.spec",
        ".ufo/evidence/round-26/cite-check/predictions.json",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/control.out",
        ".ufo/evidence/round-26/cite-check/sweep/results.tsv",
        ".ufo/waves/round-26/w1/ProbeIntegrations.md",
        ".ufo/waves/round-26/w1/ProbeSOOREDGE.md",
        ".ufo/waves/round-26/w1/ProbeSSTRICT.md",
        ".ufo/waves/round-26/w1/ProbeSUSAGE.md",
        ".ufo/waves/round-26/w1/ProbeSPININCLUDES.md",
        ".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md",
        ".ufo/waves/round-26/w1/CriticEquivalence.md",
        ".ufo/waves/round-26/w1/ColdreadPilot.md",
        ".ufo/waves/round-26/w1/ConnectorOverlap.md",
        ".ufo/waves/round-26/w1/CriticC1.md",
        ".ufo/waves/round-26/w1/DraftEntry.md",
        ".ufo/waves/round-26/w1/DraftSkillSurvivors.md",
        ".ufo/waves/round-26/w1/DraftSourcesRows.md",
        ".ufo/waves/round-26/w1/OpenCiteCheckPin.md"
      ],
      "inputs": {
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
        ".ufo/evidence/round-26/cite-check/sweep/sweep.txt": "957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893",
        ".ufo/evidence/round-26/cite-check/regression-worktree.stdout": "cf6e07b6d4251c466f1f68d5e406e0300b8daa8614e17edc69b6a0b6906ee6e5",
        ".ufo/evidence/round-26/cite-check/cite-check.defects.spec": "969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208",
        ".ufo/evidence/round-26/cite-check/predictions.json": "f1d26201ffac81fdd7415ac325165807c0f721f841ec5608636ba415879c938e",
        ".ufo/evidence/round-26/cite-check/sweep/evidence/control.out": "30772e087254d8119f9458cc48fe5922dc038016b42f552e96716a1b4de0b145",
        ".ufo/evidence/round-26/cite-check/sweep/results.tsv": "daa25ff90a7982db74f9dd8d1fbde79265b17f4e829ded05b0b621f00a81112d",
        ".ufo/waves/round-26/w1/ProbeIntegrations.md": "ac1b2c47e6a3e39ebadcb4c36cc421007e4e43fd61f836e02b0e2d2c95f1006b",
        ".ufo/waves/round-26/w1/ProbeSOOREDGE.md": "c0cd5194f6162f2f6d91531f0a512eace80cf2028b8f25505d45b8e976af4e04",
        ".ufo/waves/round-26/w1/ProbeSSTRICT.md": "19ef870f885ce37fb9f34570347fe87f034913ba465491df1950a878fea98153",
        ".ufo/waves/round-26/w1/ProbeSUSAGE.md": "d82bb2823e63952fa7614da1bd2ea359e902f1fa719844f5386f75de53a4beeb",
        ".ufo/waves/round-26/w1/ProbeSPININCLUDES.md": "bc297eb2ae9ad42e504cfd2777627147988b146b3ad6cebce122a068bd2d5a5c",
        ".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md": "7be4dc4cf29ee7d62c6a494627cafb33d2035072c174189b00bd52753b96ccd9",
        ".ufo/waves/round-26/w1/CriticEquivalence.md": "575ef324cba9b25c56ad8dd4ea4d251fb2c4941505a11b76b25a777f10d22285",
        ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7",
        ".ufo/waves/round-26/w1/ConnectorOverlap.md": "3ec2c82690d0c08e61f12451d98718158a8df5acaec71c9ab76ecba6e6c0b8e0",
        ".ufo/waves/round-26/w1/CriticC1.md": "8fbcf4e68bb462ebe1cdff11298802f8f047b2bbe158bca702b6c2290bd007df",
        ".ufo/waves/round-26/w1/DraftEntry.md": "cedea99c784f25dc73c0205d4f5e3a5e93f5eafd4ac3924f9e084874c8569a83",
        ".ufo/waves/round-26/w1/DraftSkillSurvivors.md": "71ab6ba336c7e968446455ce8932dccbcce9f241cfa04b3515dbe110f94b96d1",
        ".ufo/waves/round-26/w1/DraftSourcesRows.md": "44a8295ea8cc1dd999ec8c4dce2efb9042d66a4a625fe512eda23c599c86eec5",
        ".ufo/waves/round-26/w1/OpenCiteCheckPin.md": "584bb162baef94ed15716ef19739920b0887b31db929604a3c4f1a4560751f31"
      },
      "external_inputs": {
        "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f",
        "tameshi-shokunin@622d31d90b1fbc55c56e91a2b012bc18d6f1421a:.ufo/evidence/round-26/cite-check/cite-check.defects.spec": "969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208",
        "tameshi-shokunin@622d31d90b1fbc55c56e91a2b012bc18d6f1421a:.ufo/evidence/round-26/cite-check/predictions.json": "f1d26201ffac81fdd7415ac325165807c0f721f841ec5608636ba415879c938e"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead04-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead04-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead04-7.json"
      ]
    }
  ]
}
```

## What I checked

**Section 1 (line 827, `### The protocol — ordered, fail-closed`, instruction).** The section names one runnable command, the pin read `git show b58b26fb:tools/mutate-and-run.sh`, which I executed under the collector (exit 0). Every pin claim held: the pinned tool is 1001 lines with sha256 `597e1419…ff6331b` at commit `b58b26fbeba8fd972e1d31ac8a9175a81e333b32`, and `tools/mutate-and-run.sh` at the read rev holds a later revision (2016 lines, `fb91ef76…`), exactly as the "pin by git show" remark says. I then read the pinned source and checked each of the six steps against it: spec parse with per-defect uniqueness asserted before any suite run and `@new == @old` refused with `MUTATE: SETUP (<reason>)` exit 2; control-first with a red control exiting 2; verdict map SURVIVED (0) / INCONCLUSIVE (124 timeout, 126/127 not runnable) / KILLED (other nonzero); `MUTATE_RESTORE: OK|DRIFT` on target sha before = after; `MUTATE: DONE` exit 0 and DEGRADED exit 1 on any inconclusive, with the evidence dir keeping pristine, every mutant, `evidence/<id>.out`, `results.tsv`, `spec.copy` and printing `MUTATE_EVIDENCE: <dir>`; and `MUTATE_TOOL` printed at the top of every run. To make that more than a source read I executed the pinned tool's own `--selftest` under the collector (writes only under /tmp): all its self-checks passed, covering exactly the behaviors the section lists. The pre-registration claim also holds at the cited anchors: `mutation-case-mado-verify.md:73` says "pre-registration held 10/10 on verdicts and 4/4 on the named kill mechanisms", and `:187-189` records the prediction table written 17:42Z before the sweep with "4/10 killed; same six survivors". Verdict: executed-ok.

**Section 2 (line 2086, `## Ninth recorded case — round 26`, record).** All pointer-backed claims check out against primary receipts. The kumitate gate at `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` is mode 100755, 2537 lines, sha256 `40573448…c10c9f` (git-object reads recorded in external_inputs). The sweep log `.ufo/evidence/round-26/cite-check/sweep/sweep.txt` shows `MUTATE_DATE 2026-10-22T10:02:07Z`, `CONTROL: GREEN` with pristine sha `40573448…`, five `KILLED` (exit 1) / five `SURVIVED` (exit 0) DEFECT lines, `MUTATE_RESTORE: OK`, and `MUTATE: DONE (… killed=5 survived=5 inconclusive=0 kill-rate=50%)`; `results.tsv` matches; `control.out` reads `62/62 cases passed (hermetic)` / `VERDICT: PASS`. `predictions.json` (10 predictions, 5 KILL-aimed / 5 SURVIVE-aimed) matches the measured verdicts 10/10, and both spec and predictions were committed in lane commit `622d31d90b1fbc55c56e91a2b012bc18d6f1421a` at 10:01:47Z — 20 seconds before the sweep stamp — and are byte-identical at the read rev. The recorded regression receipt shows `REGRESSION_CASE js-cite-check: PASS` and `REGRESSION: PASS (cases=9 passed=9)`, and I reproduced it live: `bash tools/mutate-and-run.sh --regression` at the read rev under the collector exited 0 in 223 s with exactly those two lines. The survivor story is backed wave-1: ProbeSOOREDGE/SSTRICT/SUSAGE/SPININCLUDES each conclude "DISTINGUISHED by a hermetic, off-suite input/probe" (four holes, hermetic witness each), ProbeSEMPTYGUARD and CriticEquivalence carry the equivalence argument (structural proof + 316/316 differential), and ProbeIntegrations concludes "the `--integrations` group kills none of the five survivors" and "is red at the pristine pin" on live trees (6 of 9 cases pass, exit 1), so the leg stays hermetic-only — matching the section's wording, which traces to wave-1 `DraftSkillSurvivors.md:327`. The K_FENCE_TILDE error-pattern paragraph matches entry §3. I also fetched the S089 source (https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/, 38 687 bytes, sha256 `bc57267629e20668a6542c5c225d1da9e6fef8de466cbab1337df3ff7c42e04d`) by ordinary means: both quoted sentences ("no definitive way for Stryker to find and ignore", "no way yet to mark them to be ignored") appear verbatim; the URL is not a schema-shaped external_inputs key, so it is recorded here in prose only. Verdict: verified-record.

**Method notes.** One fresh fleet-mirror clone, detached at the read rev before any tracing; the live lane was never read during traces (every receipt's `live_lane_reads` is empty). No git write commands, no `jj`, no edits to production files; the only writes were the seven trace receipts and this report. No tools were installed (none needed).

COLDREAD ReRead04: executed-ok, verified-record
