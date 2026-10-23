```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ColdA01",
  "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a",
  "read_rev": "a4f718138bdad20de741faeca57891645e5a64d9",
  "sections": [
    {
      "start": 131,
      "heading": "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "I did not rerun the complete 10-mutant historical sweeps: their case notes describe an unversioned scratch mutate_driver.py. I ran the recipe's named sha256 checks against both pinned git blobs, and both full digests match the notes. The maintained ledger replay was separately attempted under section 2 but exceeded the six-minute bound."
      ],
      "commands_executed": [
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' corpus/knowledge/mutation-case-kimi-census.md",
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' corpus/knowledge/mutation-case-kagi-census.md",
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' corpus/knowledge/gates-survey-kumitate.md",
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' corpus/knowledge/gates-survey-kagi.md",
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' corpus/README.md",
        "bash -c 'sha256sum <(git -C ../kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs)'",
        "bash -c 'sha256sum <(git -C ../kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh)'"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/knowledge/gates-survey-kumitate.md",
        "corpus/knowledge/gates-survey-kagi.md",
        "corpus/README.md"
      ],
      "inputs": {
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
        "corpus/knowledge/gates-survey-kumitate.md": "3dca7a1a5c621bf0ec75948d0836839dec98651673bb2987861d9aa122579b0e",
        "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
        "corpus/README.md": "c244f8ca2f877411e2d90195503f446a186bd10600664d75edfd0d6d59f14437"
      },
      "external_inputs": {
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-1-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-1-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-1-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-1-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-1-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-1-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-1-7.json"
      ]
    },
    {
      "start": 375,
      "heading": "## Restore discipline — before/after identity, not continuous non-write proof",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "The maintained --regression replay was attempted with timeout 360 and the required scratch workdir, but the trace call exceeded its 380-second tool deadline and left no receipt for that invocation. Partial observed evidence: js-kimi-census passed 10/10 (8 killed, 2 survived); bash-surface-census control passed and B1–B9 completed (B5 survived), but B10 and the remaining legs were not completed. No overall regression PASS is claimed. The separately traced sha256sum command below matched the pinned runner hash."
      ],
      "commands_executed": [
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' corpus/knowledge/mutation-case-kimi-census.md",
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' corpus/knowledge/mutation-case-kagi-census.md",
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' corpus/README.md",
        "python3 -c 'import sys;print(open(sys.argv[1]).read()[:200000])' tools/mutate-and-run.sh",
        "sha256sum tools/mutate-and-run.sh"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/README.md",
        "tools/mutate-and-run.sh",
        "SCORECARD.md"
      ],
      "inputs": {
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
        "corpus/README.md": "c244f8ca2f877411e2d90195503f446a186bd10600664d75edfd0d6d59f14437",
        "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"
      },
      "external_inputs": {
        "tameshi-shokunin@a4f718138bdad20de741faeca57891645e5a64d9:SCORECARD.md": "ffb67ddb172f55af771681432264b2124b74715eb5678091c7004708f0900008",
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-2-1.json",
-        "/home/vgpnk/Projects/shokunin/tameshi-r32-seats/ColdA01/../tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-2-2.json",
+        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-2-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-2-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-2-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdA01-2-5.json"
      ]
    }
  ]
}
```

Checked both sections and their cited notes, surveys, and README evidence at the pinned revision. Pinned Kimi and Kagi artifact hashes matched the historical records; SCORECARD.md:13 and its digest were read with git show. The maintained regression replay did not complete within the six-minute limit, so its partial results are not reported as an overall pass.

COLDREAD ColdA01: gap-minor, gap-minor
