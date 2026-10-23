# ColdA03 — cold read of SKILL.md section 5 at a4f718138bdad20de741faeca57891645e5a64d9

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdA03", "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a", "read_rev": "a4f718138bdad20de741faeca57891645e5a64d9",
  "sections": [{"start": 2104, "heading": "## Ninth recorded case — round 26", "class": "record", "verdict": "gap-minor",
    "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["The section's replay claim (`bash tools/mutate-and-run.sh --regression` -> `REGRESSION_CASE js-cite-check: PASS`, `cases=9 passed=9`) was not observed live: the full nine-leg replay exceeds the 6-minute per-command allowance; a collector-wrapped attempt (timeout 330, workdir /fast/scratch/hyaku/tameshi-r32-seats/ColdA03/rg-5) was cut at 300 s after leg 1 (js-kimi-census PASS, match=10/10) and produced no receipt, so it is not credited or listed. The claim's mechanics were verified instead: the runner header documents leg 9 js-cite-check (kumitate scripts/cite-check.mjs, 5/10), its pre-registration commit 622d31d and the 10:02Z sweep; the embedded selftest leg tuple 'js-cite-check:js-cite-check.spec:TABLE_CITECHECK:10:5' matches the sweep table exactly (10 defects, 5 KILLED); and the knowledge entry records the landed replay stdout ('REGRESSION_TABLE js-cite-check: match=10/10')."],
    "commands_executed": [
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-26/cite-check/sweep/sweep.txt",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kumitate-cite-check.md",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/mutate-and-run.sh",
      "python3 -c \"import hashlib,sys,os;p=sys.argv[1];b=open(p,'rb').read();print(hashlib.sha256(b).hexdigest(),b.count(b'\\n'),len(b),oct(os.stat(p).st_mode&0o7777))\" /fast/scratch/hyaku/tameshi-r32-seats/ColdA03/kumitate-clone/scripts/cite-check.mjs",
      "git -C /fast/scratch/hyaku/tameshi-r32-seats/ColdA03/fleet/tameshi-shokunin show --stat --format=fuller 622d31d90b1fbc55c56e91a2b012bc18d6f1421a",
      "sha256sum .ufo/evidence/round-26/cite-check/sweep/sweep.txt corpus/knowledge/mutation-case-kumitate-cite-check.md tools/mutate-and-run.sh",
      "grep -rn -e --integrations .ufo/waves/round-26/w1"
    ],
    "opened": [".ufo/evidence/round-26/cite-check/sweep/sweep.txt", "corpus/knowledge/mutation-case-kumitate-cite-check.md", "tools/mutate-and-run.sh", ".ufo/waves/round-26/w1/ProbeIntegrations.md", ".ufo/waves/round-26/w1/DraftSkillSurvivors.md"],
    "inputs": {
      ".ufo/evidence/round-26/cite-check/sweep/sweep.txt": "957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893",
      "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
      "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
      ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7",
      ".ufo/waves/round-26/w1/ConnectorOverlap.md": "3ec2c82690d0c08e61f12451d98718158a8df5acaec71c9ab76ecba6e6c0b8e0",
      ".ufo/waves/round-26/w1/CriticC1.md": "8fbcf4e68bb462ebe1cdff11298802f8f047b2bbe158bca702b6c2290bd007df",
      ".ufo/waves/round-26/w1/CriticC2.md": "82709522d6986dac9437e0ac653a50c1f5cc3a188931c0b2c64345054e87f266",
      ".ufo/waves/round-26/w1/CriticEquivalence.md": "575ef324cba9b25c56ad8dd4ea4d251fb2c4941505a11b76b25a777f10d22285",
      ".ufo/waves/round-26/w1/DraftEntry.md": "cedea99c784f25dc73c0205d4f5e3a5e93f5eafd4ac3924f9e084874c8569a83",
      ".ufo/waves/round-26/w1/DraftLesson25Correction.md": "73ea22832c0b0c9e053e1345eb71c1bf122e59b9528c1689cab94deb2b80f465",
      ".ufo/waves/round-26/w1/DraftLesson26.md": "ee0f14109eae62f6d7776c33aa2b2ea7d351b5bb8ae714d186220e166d99c0b8",
      ".ufo/waves/round-26/w1/DraftProvinceReadme.md": "862125d20762614aa651db01c5b3a1def80f29f88ae378aae0afca63fdc78897",
      ".ufo/waves/round-26/w1/DraftScorecard.md": "6a1b00388fb929a4bde9788548cae4db44d4bd0c453a30b3d13cc5b875d6866d",
      ".ufo/waves/round-26/w1/DraftSkillSurvivors.md": "71ab6ba336c7e968446455ce8932dccbcce9f241cfa04b3515dbe110f94b96d1",
      ".ufo/waves/round-26/w1/DraftSourcesRows.md": "44a8295ea8cc1dd999ec8c4dce2efb9042d66a4a625fe512eda23c599c86eec5",
      ".ufo/waves/round-26/w1/InteropCheck.md": "0b4f90f50ed303588b345a1238cbb2c3f49beab125c2eeda18f14eda887c94aa",
      ".ufo/waves/round-26/w1/MtGuardGapsRecheck.md": "e4b4ff0bb12a4bf26f59a791beb68e10324f4b595fdc477a998650f8b06b225d",
      ".ufo/waves/round-26/w1/MutateC1Counter.md": "ed0f5fcbfece1e733bc80f8ca30b7db757a93f1b4ba9594770a5668d3e702043",
      ".ufo/waves/round-26/w1/MutateC2Counter.md": "0eea9bbbc0ddc9298af73696956cb09c93bcd1b5eb9d5def369ed4d46464be80",
      ".ufo/waves/round-26/w1/MutateInteropLegSet.md": "a65d1a1400253ad8111d8a2e22bba8ff2f48ded24e3f87068f14fa1bb4c3224e",
      ".ufo/waves/round-26/w1/MutateRunnerSelftest.md": "ee7fceffba282d25e729f41044ebc9b2f224508b621146d8e25836437bfdad6e",
      ".ufo/waves/round-26/w1/OpenCiteCheckPin.md": "584bb162baef94ed15716ef19739920b0887b31db929604a3c4f1a4560751f31",
      ".ufo/waves/round-26/w1/OpenEquivalentSource.md": "72d508e5ccf94e0602bb2b0c6b06dd75bb48d5d55b690fdb5ac2b2a9a5527ce7",
      ".ufo/waves/round-26/w1/OpenStrykerMutators.md": "d9a563152d0bb8496e1fc6a90ae8e2b74c736c531c9075139332e570ce1351ff",
      ".ufo/waves/round-26/w1/ProbeIntegrations.md": "ac1b2c47e6a3e39ebadcb4c36cc421007e4e43fd61f836e02b0e2d2c95f1006b",
      ".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md": "7be4dc4cf29ee7d62c6a494627cafb33d2035072c174189b00bd52753b96ccd9",
      ".ufo/waves/round-26/w1/ProbeSOOREDGE.md": "c0cd5194f6162f2f6d91531f0a512eace80cf2028b8f25505d45b8e976af4e04",
      ".ufo/waves/round-26/w1/ProbeSPININCLUDES.md": "bc297eb2ae9ad42e504cfd2777627147988b146b3ad6cebce122a068bd2d5a5c",
      ".ufo/waves/round-26/w1/ProbeSSTRICT.md": "19ef870f885ce37fb9f34570347fe87f034913ba465491df1950a878fea98153",
      ".ufo/waves/round-26/w1/ProbeSUSAGE.md": "d82bb2823e63952fa7614da1bd2ea359e902f1fa719844f5386f75de53a4beeb",
      ".ufo/waves/round-26/w1/RegistryCheck.md": "90b85240dc539e6b5fbeeccee4cfea0f3299278b3efc9d44e66acdbb8619d0f2",
      ".ufo/waves/round-26/w1/ReplicateSweep.md": "82395cf5072b8286ddff98e5089cd4006eccc60394416a526bed94485420609f",
      ".ufo/waves/round-26/w1/ReviewMonitorHarm.md": "84df4274f65e88df5ca7707a0cdb880e1ecb6ba8f4b435781890772a964bb4b4",
      ".ufo/waves/round-26/w1/ReviewMteLeg9.md": "f8ef5739244a6bc51d74627a5f4528b57a08e4f6797499c07bfb7014ab006af0",
      ".ufo/waves/round-26/w1/ReviewPredictions.md": "1f4b1dcd4f5722049f56c90dca2a0c53c7bde58336fc780a69eaad3bd37bf1ae",
      ".ufo/waves/round-26/w1/ReviewPreregTiming.md": "5d72c861750383dd315faf0da53401d31d626651823280749a43d7f314352e48",
      ".ufo/waves/round-26/w1/ReviewRunnerDiff.md": "9fbece7c8bbdc52dd5019983ef7253e569f0ed79b64f7cf597275d060a010c19",
      ".ufo/waves/round-26/w1/ReviewSkillRows.md": "d6feab693dc16ac39066e3e54e69090da22edcac127d8f8145ea280022ab3907",
      ".ufo/waves/round-26/w1/ScoutFrontier.md": "d5b688ecb73b186234a4b62b575e7a0e8713fc23335f0d78eb22e0dfa326f0ac",
      ".ufo/waves/round-26/w1/ScoutJjBounds.md": "c6da12b68f77dcad07a69f6d154cc3e649770046891e9e891c47f7473b22f304",
      ".ufo/waves/round-26/w1/ScoutRoutedOpen.md": "1b3566d728c442f3c7a49e2c7db76931198831c955e2f30a52a9c8c26e832e0a",
      ".ufo/waves/round-26/w1/swarm-registry.json": "e039956a50bf10a005bbb1a51179e7be0ba72fc3e9568616115a9b4ff02382f9"
    },
    "external_inputs": {"kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA03-5-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA03-5-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA03-5-3.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA03-5-4.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA03-5-5.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA03-5-7.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA03-5-8.json"]}]
}
```

## What I checked

Section 5 (lines 2104–2131, ending before the `### Round-26 gate/probe registry — report interop` heading) is a **record**: it states round-26 results with pointers. Verified in a detached clone at a4f7181 (SKILL.md sha256 matches the pinned page hash), never touching the live lane:

- **Target pin**: kumitate `scripts/cite-check.mjs` at `1205c662…` — hashed my own kumitate clone checked out at that rev: sha256 `40573448…c10c9f`, 2537 lines, 126,735 bytes, mode 0755. All four claims match exactly.
- **5/10 killed, 10/10 verdict predictions held**: `sweep.txt` shows exactly the ten defects of the section's table — K_UNRESOLVED_SEV, K_PIN_KIND, K_FENCE_TILDE, K_MISSING_WORD, K_EMPTY_VERDICT KILLED; S_OOR_EDGE, S_STRICT, S_EMPTY_GUARD, S_USAGE, S_PIN_INCLUDES SURVIVED — `defects=10 killed=5 survived=5`, `MUTATE_RESTORE: OK`, control `62/62 cases passed (hermetic)`, `MUTATE_DATE 2026-10-22T10:02:07Z`.
- **Pre-registration before mutants**: commit `622d31d…` in the lane, committed 10:01:47Z, carries `cite-check.defects.spec` (57 lines) and `predictions.json` — 20 seconds before the sweep stamp. The runner header repeats the same leg-9 provenance.
- **Survivor classification**: the knowledge entry's §4 table names the same four holes with hermetic witnesses and S_EMPTY_GUARD as equivalent; the "non-hermetic `--integrations` group kills none of the five" sentence is backed by `.ufo/waves/round-26/w1/ProbeIntegrations.md` ("Verdict: NO…") and appears verbatim in `DraftSkillSurvivors.md`.
- **Replay claim**: see minor gap in the JSON — the live nine-leg replay exceeds the 6-minute allowance (attempt cut at 300 s in leg 2, no receipt, uncredited); mechanism verified from the runner's embedded `TABLE_CITECHECK` leg tuple (10 defects / 5 killed), the sweep table agreement, and the entry's recorded replay stdout.
- **Runner identity**: the clone's `tools/mutate-and-run.sh` hashes to `a7d3f2dd…12eb9` (the C1-pinned runner), so the section was read against byte-identical runner bytes.

The four L1-appended files (SCORECARD.md, LOG.md, ledger.json, corpus/lessons/round-32.md) were never opened. All seven receipts carry `rev` = a4f7181…, exit 0, and argv equality.

COLDREAD ColdA03: gap-minor
