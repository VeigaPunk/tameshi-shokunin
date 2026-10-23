# ColdB03 — round 32 wave 2 cold read

Section 1 of SKILL.md at a4f718138bdad20de741faeca57891645e5a64d9 (SKILL.md sha256 2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a). Read from a fresh fleet-mirror clone at /fast/scratch/hyaku/tameshi-r32-seats/ColdB03/fleet/tameshi-shokunin, detached at the pinned rev. Trace receipt written under the frozen collector; input digests match the receipt.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ColdB03",
  "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a",
  "read_rev": "a4f718138bdad20de741faeca57891645e5a64d9",
  "sections": [
    {
      "start": 131,
      "heading": "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Step 7 quotes the verbatim summary `SELFTEST: FAIL (1/16 cases)` and attributes it to mutation-case-kagi-census.md:82-103; that string appears nowhere in the kagi note (only `SELFTEST: PASS (16 cases)` at lines 34/43/52). The string is nevertheless verified at the same rev in `.ufo/evidence/kaika-round-1/coldread/appendixB/B1.out:38` (bad-case line `bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got exit=0` at :6), so the fact holds but the pointer is wrong.",
        "Intro claim \"round 16's full-page cold-read executed it end to end (two seats; Errata — round 16)\" — the full-page cold-read is confirmed to exist (corpus/lessons/round-16.md), but the \"two seats\" detail is not anchored by any opened source (no path cited), so it stays partially unverifiable from opened inputs.",
        "Step 4 says each defect carries a pre-registered `expect: killed|survived`; the cited manifest ranges (mutation-case-kimi-census.md:41-53, :155-166) show the kill-rate table and driver spec without an `expect:` field. Pre-registration evidence lives in E1 (mutation-case-kimi-census.md:183-191, cited separately), not in the quoted manifest ranges."
      ],
      "commands_executed": [
        "python3 tools/trace-inputs.py --root /fast/scratch/hyaku/tameshi-r32-seats/ColdB03/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB03-1-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/gates-survey-kumitate.md corpus/knowledge/gates-survey-kagi.md corpus/README.md",
        "awk 'NR>=36&&NR<=100{printf \"%d: %s\\n\", NR, $0}' corpus/knowledge/mutation-case-kimi-census.md",
        "awk 'NR>=150&&NR<=210{printf \"%d: %s\\n\", NR, $0}' corpus/knowledge/mutation-case-kimi-census.md",
        "awk 'NR>=80&&NR<=130{printf \"%d: %s\\n\", NR, $0}' corpus/knowledge/mutation-case-kagi-census.md",
        "awk 'NR>=245&&NR<=260{printf \"%d: %s\\n\", NR, $0}' corpus/knowledge/mutation-case-kagi-census.md",
        "awk 'NR>=180&&NR<=196{printf \"%d: %s\\n\", NR, $0}' corpus/knowledge/mutation-case-kagi-census.md",
        "grep -n 'SELFTEST' corpus/knowledge/mutation-case-kagi-census.md",
        "git grep -n 'SELFTEST: FAIL' HEAD -- ':!corpus/lessons/round-32.md'",
        "grep -nE 'bad-case 05|SELFTEST: FAIL' .ufo/evidence/kaika-round-1/coldread/appendixB/B1.out",
        "grep -n -i 'cold-read|coldread' corpus/lessons/round-16.md",
        "grep -n 'G-R2-1' corpus/README.md",
        "awk 'NR>=545&&NR<=575{printf \"%d: %s\\n\", NR, $0}' corpus/knowledge/gates-survey-kagi.md",
        "awk 'NR>=15&&NR<=35{printf \"%d: %s\\n\", NR, $0}' corpus/knowledge/gates-survey-kumitate.md",
        "awk 'NR>=17&&NR<=33{printf \"%d: %s\\n\", NR, $0}' SKILL.md"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/knowledge/gates-survey-kumitate.md",
        "corpus/knowledge/gates-survey-kagi.md",
        "corpus/README.md",
        "corpus/lessons/round-16.md",
        ".ufo/evidence/kaika-round-1/coldread/appendixB/B1.out"
      ],
      "inputs": {
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
        "corpus/knowledge/gates-survey-kumitate.md": "3dca7a1a5c621bf0ec75948d0836839dec98651673bb2987861d9aa122579b0e",
        "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
        "corpus/README.md": "c244f8ca2f877411e2d90195503f446a186bd10600664d75edfd0d6d59f14437",
        "corpus/lessons/round-16.md": "46642f0c0bf1cdb263f15af46bdd238f65c04e3105e5cf4d3136a35e0defe298",
        ".ufo/evidence/kaika-round-1/coldread/appendixB/B1.out": "4552e10bbd12c7f271f725bf4829c3738e32d4dfe1d7c89881f5f0b7a250eace"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB03-1-1.json"
      ]
    }
  ]
}
```

Checked: the section is a record (numbered recipe that states facts with pointers). Every cited lane file was opened under the trace collector (one receipt, rev matches, exit 0, argv matches). All substantive claims verified against the pinned bytes: control greens (KIMI_CENSUS_SELFTEST: 43/43 pass / VERDICT: PASS, exit 0 at kimi:20-21; SELFTEST: PASS (16 cases), 14 executed +2 skipped at kagi:33-35,42-43), artifact pins (sha256/size/lines/mtime/rev/clean git status at kimi:13-16, kagi:13-17 incl. the 887th no-trailing-newline line), driver `--check` `all unique` gate (kimi:22-25, kagi:44-47), timeouts (300 s round 2, 280 s round 3), kill rates 8/10 with 11 runs in 7.0 s / 11.0 s (kimi:29-31, kagi:50-53), D2/D10 and B5/B10 survivor probes (kimi:82-99, kagi:111-114,118-122,251-253), B4 token-only kill (kagi:88-91), both E1 errata (kimi:183-191, kagi:184-191), the G-R2-1 dirty-pin story (corpus/README.md:11 and gates-survey-kagi.md:554-566), the kumitate n/m + VERDICT gate formats (gates-survey-kumitate.md:19-31), the Standing-rules scratch namespace (SKILL.md:25-27), and the self-reference SKILL.md:377-378. Minor gaps listed above; none change the section's substantive record.

COLDREAD ColdB03: gap-minor
