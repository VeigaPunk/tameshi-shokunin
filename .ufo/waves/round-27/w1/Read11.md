# Read11 cold read: SKILL.md leg ledger section (line 921)

Verdict: gap-minor. Class: record. Read revision 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. Page sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read11",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 921,
      "heading": "## The leg ledger \u2014 replay, receipt, and how it is read (round 7, measured)",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Round-18 pointer names no revision. The span 597-620 (SKILL.md:929) is exact only at 58e5d53, the round-18 build landing: PIN_JS is line 597 and the eighth TABLE line is 620. At 606716f, which SKILL.md:1396-1398 calls the round-18 replay tool, the six TABLE lines are 554-559 and lines 597-620 are kimi defect-spec text. Name 58e5d53 in the sentence.",
        "Ledger count is ambiguous and one row behind the tool. 'eight rows since its round-18 block' can be read as eight rows added after that block; the ledger holds eight rows in all, the eighth appended in that block (corpus/knowledge/fleet-kill-rate-ledger.md:424-437). The tool at 2227d embeds nine legs (tools/mutate-and-run.sh:83 header; TABLE lines 621-629). The ninth leg, js-cite-check (round 26), has no ledger row, and corpus/knowledge/mutation-case-kumitate-cite-check.md:123-126 says the ledger still lists cite-check as a 1/4 probe. Say 'eight rows in all, the last appended in round 18'.",
        "'Four legs at that revision' has an unclear antecedent. The nearest antecedent is each leg's pinned original revision, and those are four different commits (175de6ba, fecee874, 165307fe, eead56b2). The intended revision is the tool at 9f1d3c3 (tool sha256 cf41efaa...), named only later in the same sentence. Name the tool revision in that clause.",
        "Section boundary: the stated rule ends the section at line 932, just before '### Using the ledger' (933). The subsections at 933 and 965 are separate sections and this read does not cover them."
      ],
      "commands_executed": [
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] corpus/knowledge/fleet-kill-rate-ledger.md",
        "python3 -c import sys,re;L=open(sys.argv[1],encoding='utf-8').read().split('\\n');[print(i+1,l) for i,l in enumerate(L) if (71<=i<=109) or re.match(r'(PIN_|REV_|TABLE_)',l) or 'cite-check' in l or 'REGRESSION:' in l] tools/mutate-and-run.sh"
      ],
      "opened": [
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "tools/mutate-and-run.sh",
        "tools/trace-inputs.py",
        "corpus/README.md",
        "corpus/SOURCES.md",
        "corpus/knowledge/closeout-r11.md",
        "corpus/knowledge/incremental-pin-disposition.md",
        "corpus/knowledge/mutation-case-kagi-checklist.md",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md",
        "corpus/knowledge/mutation-case-kumitate-claims.md",
        "corpus/knowledge/operator-runbook.md",
        "corpus/knowledge/service-limits.md",
        "corpus/knowledge/service-standing-state.md",
        "corpus/lessons/round-18-verifier-spotcheck.md",
        "corpus/lessons/round-18.md",
        "corpus/lessons/round-20.md"
      ],
      "inputs": {
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "corpus/README.md": "33915658d9ef1ed3b93ed0cf58ba5b341bc58facc5d1ff73574e6ddd297dcb79",
        "corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a",
        "corpus/knowledge/closeout-r11.md": "cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265",
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
        "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
        "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
        "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0",
        "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952",
        "corpus/lessons/round-18-verifier-spotcheck.md": "3cfda4e1f64131a290c04278fb60c4402ffd58dd477ca2178eac4e2a00364fef",
        "corpus/lessons/round-18.md": "88b17f6df3290cf61d886bab322add21e863177003e1725df4f928c44b7d3159",
        "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6"
      },
      "external_inputs": {
        "tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75",
        "tameshi-shokunin@58e5d53d6a638fb72042d1f6607b24018aa299a8:tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b",
        "tameshi-shokunin@606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
        "tameshi-shokunin@44947154c23772f766f9f5439090fb5c7ad76e46:tools/mutate-and-run.sh": "b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read11-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read11-2.json"
      ]
    }
  ]
}
```

Note (plain English)

- Setup: I cloned the lane to /tmp/Read11-FjQK/fleet/tameshi-shokunin and detached it at 2227d8338c02. The clone is clean, and its SKILL.md hashes to the page sha256 above.
- Boundary: under the stated rule the section is lines 921 to 932. Line 933 starts "### Using the ledger" and line 965 starts "### Reading a receipt"; this read does not cover them.
- Class: record. The section states facts with pointers and tells no reader to run a command.
- Traced reads: Read11-1 read the cited ledger (437 lines). Read11-2 read tools/mutate-and-run.sh at 2227d. Its header (line 83) names r7-1, r10-2 six legs, r16 seven, r18 eight and r26 nine, and it has nine TABLE lines (621-629).
- Sibling reads by git show (listed in external_inputs): at 9f1d3c3 the header (lines 75-78) lists the four legs and their rates, and lines 511-522 hold their PIN, REV and TABLE values. The four TABLE lines give 8/10, 8/10, 6/10 and 4/10 kills, so the section's pointers are exact. At 4494715 there are two TABLE lines, which fits the two-case self-check. At c699c8c (round 16) there are seven, and at 58e5d53 (round 18) there are eight.
- Round-18 pointer: the 24-line block at 597-620 in 58e5d53 is exactly PIN_JS through the eighth TABLE line. At 606716f the same lines are defect-spec text.
- Ledger: eight rate rows in all. Rows 1-4 are at lines 45-48, rows 5-6 at 276-277, row 7 at 410 with its receipt at 412-413, and row 8 at 432 with its receipt at 435-436. The ledger's rates match the four legs (lines 45-48 and 134-135).
- Citation claim: a grep of corpus/ found the ledger's file name in the records listed in inputs. This is presence only; I did not count or read every citing record.
- Not checked: the case notes' own tables, and whether any recorded case lies outside the nine legs. I did not run --regression or --selftest, because the section only records them.
- Installs: none. strace 7.2 and python 3.14.8 were already present. No jj command ran; git ran only read-only against the lane or inside my own clone.

COLDREAD Read11: gap-minor
