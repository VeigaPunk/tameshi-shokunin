# Read16 — cold read of SKILL.md:1092 "### Six-case confidence statement (round 8, measured)" at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read16", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [{"start": 1092, "heading": "### Six-case confidence statement (round 8, measured)", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [
      "The anchor mutation-case-kumitate-claims.md:285-291 covers only the D8 half of the sentence (those lines are the note's §5 E2, the assert-blind-threshold erratum); the D7 slice(0, 6)-reproduction support sits elsewhere in the same note (:142-149 and :230-234), which does confirm the claim.",
      "The two round-8 scratch dirs (/tmp/w8-tameshi-t81/sweep and /tmp/w8-t8-2-claims/work) no longer exist on this host, so the run-location claim cannot be re-run now; both paths are corroborated by the notes' recorded invocations (checklist note :285 '--workdir /tmp/w8-tameshi-t81/sweep', claims note :373 '--workdir /tmp/w8-t8-2-claims/work')."
    ],
    "commands_executed": [
      "python3 tools/trace-inputs.py --root /tmp/Read16-OGrJ/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read16-1.json -- python3 -c \"\nimport sys\nfor i,p in enumerate(sys.argv[1:]):\n    b=open(p,'rb').read()\n    open('/tmp/Read16-OGrJ/dump%d.bin'%i,'wb').write(b)\n    print(p, len(b))\n\" corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/fleet-kill-rate-ledger.md",
      "python3 tools/trace-inputs.py --root /tmp/Read16-OGrJ/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read16-2.json -- python3 -c \"\nimport sys\nfor i,p in enumerate(sys.argv[1:]):\n    b=open(p,'rb').read()\n    open('/tmp/Read16-OGrJ/row%d.bin'%i,'wb').write(b)\n    print(p, len(b))\n\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-tsukuroi-census.md corpus/knowledge/mutation-case-mado-verify.md",
      "python3 tools/trace-inputs.py --root /tmp/Read16-OGrJ/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read16-3.json -- python3 -c \"\nimport sys, hashlib\nfor p in sys.argv[1:]:\n    print(p, hashlib.sha256(open(p,'rb').read()).hexdigest())\n\" corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-tsukuroi-census.md corpus/knowledge/mutation-case-mado-verify.md"
    ],
    "opened": [
      "corpus/knowledge/mutation-case-kagi-checklist.md",
      "corpus/knowledge/mutation-case-kumitate-claims.md",
      "corpus/knowledge/fleet-kill-rate-ledger.md",
      "corpus/knowledge/mutation-case-kimi-census.md",
      "corpus/knowledge/mutation-case-kagi-census.md",
      "corpus/knowledge/mutation-case-tsukuroi-census.md",
      "corpus/knowledge/mutation-case-mado-verify.md"
    ],
    "inputs": {
      "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7",
      "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
      "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
      "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
      "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
      "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604",
      "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3"
    },
    "external_inputs": {
      "kumitate-shokunin@f86b8ed0e03d6b627e5e56f87384b315a2eeba52:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
      "kumitate-shokunin@e4044311333cb8216fa98598c61638f53ffa99a8:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
      "kagi-shokunin@587fda0470f2b8144618068839997756c65ddde2:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "tsukuroi-shokunin@9bcd1627072f7d8def172eed3b7a702ff218e71e:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
      "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13"
    },
    "traces": [
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read16-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read16-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read16-3.json"
    ]}]}
```

## What I checked

Class: the section states measured facts with pointers and commands nobody is told to run, so I read it as a `record` and read its citations under the trace collector (two reader runs, plus a hashing run so every executed collector command has a receipt; all three receipts carry `rev` 2227d83… and my hand-computed sha256sums match them).

Table rows 1–6 against the notes at this revision: suites 43/16/26/28/34/39 (kimi axes table "`n/43 pass` + `FAIL` labels"; kagi "`SELFTEST (n/16)`"; tsukuroi control "`TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`"; mado "`MADO_SELFTEST: 28/28 assertions passed`"; checklist "`CHECKLIST_SELFTEST: PASS (34 cases)`" at note :49/:261; claims "`CLAIMS_SELFTEST: 39/39 pass`" at :53/:62). Rates and compositions: 8/10 with 10 kill-aimed twice; tsukuroi 6/10 with "6 kill-aimed + 4 hole-aimed" (note :275); mado 4/10 with the note's "4 in-surface + 6 out-of-surface, measured 4/4 and 0/6" (note :177) — the section's "4 in + 6 out"; checklist `MUTATE: DONE (defects=15 killed=7 survived=8 … kill-rate=47%)` (note :263-264), i.e. 7 kill + 8 hole with the eight survivors exactly the eight-row probe table; claims "kill rate 7/10 (70 %)" with 6/6 kill-aimed plus 1/4 hole-aimed (D10 enforced) and survivors D7/D8/D9 (note :63, :72-76). All six rows match.

Round-8 run claims: `MUTATE_RESTORE: OK` in both notes (checklist :199, claims :69), tool `cf41efaa…` full sha `cf41efaa8be5…c75` in both (checklist :32, claims :23), and the claims note's E3 (:292-297) names the ledger-row/`--regression` embedding follow-up exactly as the section says.

Diversity paragraph: I resolved all six 8-hex pins as sha256 prefixes of exact bytes in the sibling repos' histories (read-only `git`, `GIT_OPTIONAL_LOCKS=0`, through the fleet mirror) — each pin matches the full sha256 listed in `external_inputs`, and `mado-verify.sh` even resolves at the tick's own recorded commit `eead56b2…`, with the checklist note's truncated tail "…76bf" and the mado note's "…d0e13" reproduced exactly. Shebangs read from those pinned bytes: `#!/usr/bin/env node` twice, `#!/usr/bin/env bash` four times, as claimed. The five gate-grammar families are visible in those same pinned bytes: `KIMI_CENSUS_SELFTEST: n/m pass` / `CLAIMS_SELFTEST: n/m pass` with FAIL rows (one family over kumitate's two node gates), kagi census `ok-case`/`bad-case … got …` + `SELFTEST:`, kagi checklist `checklist-selftest: FAIL …` + `CHECKLIST_SELFTEST:`, tsukuroi `PASS/FAIL <label>` from `check()` taking `LABEL WANT_RC WANT_VERDICT`, mado `n/n assertions`. Four author lanes holds by the table's own author column. Ledger §2 is titled "Adjacent measured — not fleet sweeps" and carries the harness meta-sweep as its own row, so the section's "boundary item, not a case" reading is the ledger's own.

Pointers: checklist note :180-194 is exactly the probe table — `C1` (`UNMATCHED-ITEM`) and `F2` (`--only C1` … `failed=0`) as class (a), six more class-(b) unreached inputs, with the "six of the eight are unreached" reading line inside the range. Claims note :249-254 is exactly Row E — D9 the unreached-arm class's first JS instance, quoting the tsukuroi reading "two bash instances, still zero JS instances" — and the page's own round-5 statement (SKILL.md :727 and :769) says the same, so the amendment is real. Claims note :285-291 is E2, the D8 threshold erratum; the D7 half of that sentence is supported at :142-149 and :230-234 (same note), which is why I list the anchor as a minor gap rather than a defect. The band "40 / 47 / 60 / 70 / 80 / 80" is the sorted rate column of the table itself, and the arithmetic holds (7/15 rounds to 47 %).

Method and hygiene: fleet-mirror clone at `/tmp/Read16-OGrJ`, detached at 2227d83… with SKILL.md sha256 verified `386de44b…`; clone porcelain-clean; all writes confined to this report, the three trace receipts, and /tmp scratch; the live lane never read during traces; sibling repos touched only through read-only git; no `jj` anywhere; no tools installed.

COLDREAD Read16: verified-record
