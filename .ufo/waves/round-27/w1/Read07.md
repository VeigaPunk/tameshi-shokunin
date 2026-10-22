# Read07 cold read: "Third case — cross-author confirmation (round 5, measured)"

Verdict: **wrong-expectation**. The section's numbers, pins, mutant sites, case labels and most citations check out against what I opened. Four statements do not: the provenance of rounds 2–3, a third survivor class that no source names, "the only class surviving in all three" (row A in the same table also survives in all three), and a 6-kill plus 4-hole composition attributed to all three rates when only one sweep records it. A record that states these is not verified, so the section stays uncovered.

Scope: SKILL.md lines 668–793 at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 (SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95). Class: record (states facts with pointers; tells no reader to run anything). The section has no sub-heading before line 794.

## Wrong expectations (contradicted by the cited sources or by the section's own table)

1. Provenance of rounds 2–3, SKILL.md:670: "two gates of one lane's craft (kumitate JS, kagi bash)". The sources name two lanes: arm-class-matrix.md:7 ("Substrates kumitate-shokunin + kagi-shokunin"); arm-class-matrix.md:232–234 (section 9, Lanes column, two lanes per admitted class); mutation-case-kimi-census.md:4 ("Substrate: kumitate-shokunin"); mutation-case-kagi-census.md:4 ("Substrate: kagi-shokunin"). SKILL.md:762–763 itself says three authors. Smallest correction: "two gates from two lanes (kumitate JS, kagi bash)".

2. Third survivor class, SKILL.md:772–773: "(unasserted data / unreached arms / unmapped paths)". The word "unmapped" appears in none of the five files I searched (the three case notes, the matrix and PROVINCE.md; trace Read07-8) and nowhere else on SKILL.md. The sources name two classes: unasserted data (mutation-case-kagi-census.md:176–178; arm-class-matrix.md section 5) and unreached arms (arm-class-matrix.md section 6; mutation-case-tsukuroi-census.md:243–249, which files B8 under row E). Smallest correction: drop "/ unmapped paths", or cite the source that defines it.

3. "The only class surviving in all three", SKILL.md:726 (row D). Row A in the same table (SKILL.md:723) lists a survivor under each gate: D2 on the tail (JS), B10 on summary fields (kagi), B9 on roll-line fields (tsukuroi). Smallest correction: "one of two classes (with row A) that survive in all three gates".

4. Composition, SKILL.md:734: "80 / 80 / 60 at compositions 6-kill+4-hole (this case)". The 6 kill-aimed plus 4 hole-aimed split is documented for the 60 % sweep only (mutation-case-tsukuroi-census.md:77–80, :203–205, :275). The kimi and kagi notes record no kill-aimed or hole-aimed split (trace Read07-12 finds no "aimed" in either). The sentence therefore attaches a composition to two rates that the sources do not record. This is a wording error, but as written it is false. Smallest correction: "the 60 % sweep ran at 6 kill-aimed + 4 hole-aimed; the two 80 % sweeps record no such split".

## Minor gaps (wording or citation drift; the underlying fact holds)

a. SKILL.md:725 labels row C "holds". mutation-case-tsukuroi-census.md:229 labels it "confirm, plus the boundary amendment". Use the note's label.
b. SKILL.md:672–673 says the matrix's round-5 errata block "carries ... the JS 'unreached' wording scope". arm-class-matrix.md:498–525 carries the chmod enumeration fix (E3, lines 506–522). The wording scope is only a pointer at :524–525 to mutation-case-kimi-census.md (E2). The cited range is correct. Lane-file defect outside this section: arm-class-matrix.md:498 joins the "## Errata (round 5)" heading onto the end of the previous sentence, so it does not start a line. The same join appears at the end of the kimi census (U6 line).
c. SKILL.md:713–716 cites mutation-case-tsukuroi-census.md:74–75 for the pre-registration sentence. It is at :75–76; line 74 is the cost bullet.
d. SKILL.md:736 cites mutation-case-tsukuroi-census.md:295–299 for E3. E3 spans :296–300.
e. SKILL.md:682 cites :63–66 for the structural guards. That range holds the summary and the grammar. The guards are described at mutation-case-tsukuroi-census.md:52–54 and sit in the sibling file at :735–741 (fixture hash) and :771–772 (host-read guard), both checked at 9bcd1627.
f. SKILL.md:684–685 says "the first measurement inside the 50–80 % band". SKILL.md:324 says the two 80 % points "sit on the 50-80/>80 boundary", and mutation-case-tsukuroi-census.md:205–206 says all three "sit in the 50–80 band". The claim holds only under the page's boundary reading. Say which reading is meant.
g. SKILL.md:753–757 and :790–792 call "aae45531" a revision. It is the sha256 prefix of the hardened bytes, committed at tsukuroi-shokunin da952909 (blob aae45531…07df6, verified). The bytes are right; the word is loose.
h. SKILL.md:779–780 "the author axis now has three points, the language axis one" is unclear. It appears to mean one JS gate.

## What I verified (against what I opened)

- Pins. tools/tsukuroi-census.sh at commit 9bcd1627072f7d8def172eed3b7a702ff218e71e has sha256 084951be…c78c5 and 976 newlines (977 lines), matching SKILL.md:675–677. The same blob is at 165307fe4746a8807b02ec4a7d7ecac0368454a6, the pin named at mutation-case-tsukuroi-census.md:10–13. The hardened bytes are the blob of commit da952909584bcad9c643e842c41d6025d732fb56 (sha256 aae45531…07df6, 1032 lines). `git diff --numstat 9bcd1627… da952909… -- tools/tsukuroi-census.sh` gives 56 insertions and 0 deletions, and no other commit touches the file between them. This matches SKILL.md:687–694 and the "+56 lines, zero deletions" claim.
- Kill table, replicated in a scratch copy of the pinned bytes (sweep, trace Read07-10). Control: PASS 26/26, exit 0. B1: 24 pass / 2 fail, exit 1. B2: 23 / 3, exit 1. B3: 25 / 1, exit 1. B4: 25 / 1, exit 1. B5: 25 / 1, exit 1. B6: 5 / 21, exit 1. B7, B8, B9, B10: 26 / 0, exit 0. Every count, exit code and survivor set matches SKILL.md:696–711. The failing-case labels match the suite's own labels, for example "healthy: nvidia present and answering", "blocked: nvidia hardware, driver offline", "healthy: rc=1 backup-only sample is not a defect", "degraded: Qkk sample drift", "blocked: sample probe error", "blocked: empty ring is not a clean bill", "degraded: journal boot errors at entry level", "degraded: enabled timer not armed (drift)".
- Mutant sites, read in the pinned copy: :160 (SAMPLE_N default 8), :210 (worse()), :281 (rc tolerance), :473 (nvidia guard), :434–452 (empty-ring block), :487–493 (PCI-unreadable branch), :578 (kernel classifier), :615 (drift +1), :935 (usage exit 2), :967 (roll printf args). All match the section's table.
- Section 6 replay on the committed hardened bytes (sweep2, trace Read07-13). Control 35/35, exit 0. B7, B8, B9: 35/35, exit 0 (survive). B10: exit 1, one fail, "blocked: unreadable PCI inventory is not a pass (D19)". This matches SKILL.md:693–694 and the replay text in mutation-case-tsukuroi-census.md:306–321.
- Lane citations checked by line. PROVINCE.md:15–16 ("TWO independent lanes"). plans/round-5.plan.md:9–10 (the anti-claim, quoted exactly). mutation-case-tsukuroi-census.md:9–35 (incident), :63–79 (control, kill rate, pre-registration), :86–102 (kill table), :200–266 (section 4), :282–287 (E1 method sentence), :305–320 (section 6). arm-class-matrix.md:498–525 (errata range).
- Matrix hold table (SKILL.md:721–729). Each cell matches the kimi table, the kagi table, the matrix section 0 table and the tsukuroi section 4 rows, except the row C label (minor a). Checked cells include: kimi D2 and D10 survive, D8 killed, D1/D6/D7 killed, D3/D9 killed, D4/D5 reached and killed; kagi B5 and B10 survive, B8 killed (2 cases), B2 and B7 killed, B1/B3/B6/B9 killed; tsukuroi B3 killed, B5 killed, B8 survives, B9 survives, B10 survives.
- Calibration claim (SKILL.md:713–716). The tsukuroi note reports 10/10 on verdicts and 10/10 on counts. The kimi E1 (miss on D7) and kagi E1 (counts 6/10) support "first of the three sweeps with no miss".

## Verification gaps and residual risk

- Not verified: the concurrent S5-1 lane's 23-defect table and the "8/9" overlap (E4). The note quotes them; the table is not in the repo.
- Timings (1.77 s, 19.6 s, 7.0 s, 11.0 s) were not reproduced. My runs under strace took 3.2–4.6 s each, so they cannot be compared with the note.
- The monitor's input-drift flags (PROVINCE.md and mutation-case-kagi-census.md). I did not read the earlier recorded hashes (the ledger is excluded). At 2227d83 the current hashes are b2875fe2…34c28be and d3190a99…d0bb0. I cannot say what changed.
- "The first case that amends a row" and other "first" claims were checked against the E1 entries by name, not against every calibration line in rounds 2–3.
- Residual risk: the sibling file has moved since 9bcd1627. The newest commit touching it (70fede2) has 2679 lines. The section's sibling facts hold at the pinned commits only; anyone who re-runs the sweep must pin 9bcd1627.

## Tooling

No installs or upgrades. Tools present and used: strace 7.2 (/usr/bin/strace), python3 3.14.8 (/usr/bin/python3), git 2.56.0. The pacman guard was not touched.

## Process notes

- One numbered read of mutation-case-tsukuroi-census.md ran outside the collector by mistake. I repeated it under the collector (Read07-6). Only the traced run is cited.
- Receipt Read07-9 was never written. This is a numbering gap, not a missing run.
- To find the traces directory I listed two lane directories with ls, outside any trace: .ufo/evidence/round-27/coldread/ and .ufo/waves/round-27/w1/. I opened no file in them and did not open any other seat's receipt.
- Untraced helper commands: ls, sha256sum, cat -n, git log, git show, git diff, git rev-parse, and a bare clone of tsukuroi-shokunin into /tmp for read-only sibling access. Their outputs agree with the receipt hashes. Sibling reads are recorded in external_inputs. One local JSON syntax parse of the block below ran after drafting; it is a syntax check on this report, not evidence, and has no receipt.
- The scratch replication scripts (sweep.py and sweep2.py) ran only under /tmp/Read07-13Rr, under the collector. Nothing in the lane or the sibling was written.

## Smallest corrections (for the L1 to apply; I changed no lane file)

- SKILL.md:670: "two gates from two lanes (kumitate JS, kagi bash)".
- SKILL.md:772–773: drop "/ unmapped paths", or name the source.
- SKILL.md:726: "one of two classes (with row A) that survive in all three gates".
- SKILL.md:734: give the 6+4 composition for the 60 % sweep only.
- SKILL.md:725: "confirm, plus the boundary amendment".
- SKILL.md:713: :74–75 becomes :75–76. SKILL.md:736: :295–299 becomes :296–300. SKILL.md:682: add :52–54.
- SKILL.md:672–673: "carries the chmod fix and points to the JS wording-scope erratum at :524–525".
- SKILL.md:684: "the first measurement strictly inside the 50–80 % band; the two 80 % points sit on its boundary".
- SKILL.md:753–757 and :790: "file revision aae45531 (sha256 prefix, committed at da95290)".
- SKILL.md:779–780: say what "the language axis one" counts.

## Machine-readable record

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read07", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 668, "heading": "## Third case \u2014 cross-author confirmation (round 5, measured)", "class": "record", "verdict": "wrong-expectation",
 "blocking_gaps": [],
 "wrong_expectations": [
  "SKILL.md:670 says rounds 2-3 measured two gates of one lane's craft (kumitate JS, kagi bash). The sources name two lanes: arm-class-matrix.md:7 (Substrates kumitate-shokunin + kagi-shokunin), arm-class-matrix.md:232-234 (section 9 Lanes column, two per admitted class), mutation-case-kimi-census.md:4 (Substrate: kumitate-shokunin), mutation-case-kagi-census.md:4 (Substrate: kagi-shokunin). SKILL.md:762-763 says three authors.",
  "SKILL.md:773 names a third survivor class, unmapped paths. The word occurs in none of the five files searched (trace Read07-8: three case notes, the matrix, PROVINCE.md) or elsewhere on SKILL.md. The sources name two classes: unasserted data (mutation-case-kagi-census.md:176-178; arm-class-matrix.md section 5) and unreached arms (arm-class-matrix.md section 6; mutation-case-tsukuroi-census.md:243-249 files B8 under row E).",
  "SKILL.md:726 (row D) says the only class surviving in all three gates. Row A in the same table (SKILL.md:723) lists a survivor under each gate: D2 on the tail, B10 on summary fields, B9 on roll-line fields.",
  "SKILL.md:734 says 80 / 80 / 60 at compositions 6-kill+4-hole (this case). The 6 kill-aimed + 4 hole-aimed split is documented for the 60 % sweep only (mutation-case-tsukuroi-census.md:77-80, :203-205, :275). mutation-case-kimi-census.md and mutation-case-kagi-census.md record no kill-aimed or hole-aimed split (trace Read07-12)."
 ],
 "minor_gaps": [
  "SKILL.md:725 labels row C holds; mutation-case-tsukuroi-census.md:229 labels it confirm, plus the boundary amendment.",
  "SKILL.md:672-673 says the matrix round-5 errata block carries the JS unreached wording scope. arm-class-matrix.md:498-525 carries the chmod enumeration fix (:506-522); the wording scope is a pointer at :524-525 to mutation-case-kimi-census.md E2. The cited range is right. Lane-file defect outside the section: arm-class-matrix.md:498 joins the Errata (round 5) heading to the end of the previous sentence.",
  "SKILL.md:713-716 cites mutation-case-tsukuroi-census.md:74-75 for the pre-registration sentence; it is at :75-76 (line 74 is the cost bullet).",
  "SKILL.md:736 cites mutation-case-tsukuroi-census.md:295-299 for E3; E3 spans :296-300.",
  "SKILL.md:682 cites :63-66 for the structural guards; that range holds the summary and grammar. The guards are described at mutation-case-tsukuroi-census.md:52-54 and sit in the sibling at :735-741 and :771-772 (checked at 9bcd1627).",
  "SKILL.md:684-685 says the first measurement inside the 50-80 % band. SKILL.md:324 says the two 80 % points sit on the 50-80/>80 boundary; mutation-case-tsukuroi-census.md:205-206 says all three sit in the band. True only under the page's boundary reading.",
  "SKILL.md:753-757 and :790-792 call aae45531 a revision. It is the sha256 prefix of the hardened bytes, committed at tsukuroi-shokunin da952909 (blob aae45531...07df6, verified).",
  "SKILL.md:779-780 'the author axis now has three points, the language axis one' is unclear; it appears to mean one JS gate."
 ],
 "commands_executed": [
  "python3 -c \"import sys;[print(open(p,encoding='utf-8').read()) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-tsukuroi-census.md",
  "python3 -c \"import sys;[print(open(p,encoding='utf-8').read()) for p in sys.argv[1:]]\" corpus/knowledge/arm-class-matrix.md",
  "python3 -c \"import sys;[print(open(p,encoding='utf-8').read()) for p in sys.argv[1:]]\" PROVINCE.md plans/round-5.plan.md",
  "python3 -c \"import sys;[print(open(p,encoding='utf-8').read()) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kagi-census.md",
  "python3 -c \"import sys;[print(open(p,encoding='utf-8').read()) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md",
  "python3 -c \"import sys\nfor f in sys.argv[1:]:\n    for i,l in enumerate(open(f,encoding='utf-8').read().split('\\n'),1): print(i,l)\" corpus/knowledge/mutation-case-tsukuroi-census.md",
  "python3 -c \"import sys\nL=open('PROVINCE.md',encoding='utf-8').read().split('\\n')\n[print('PROVINCE',i,l) for i,l in enumerate(L,1) if i<=40]\nM=open('corpus/knowledge/arm-class-matrix.md',encoding='utf-8').read().split('\\n')\n[print('MATRIX',i,l) for i,l in enumerate(M,1) if 470<=i<=535]\"",
  "grep -n -i -e unmapped -e 'one lane' -e 'same lane' -e 'different lane' -e 'one author' -e 'same author' -e 'three authors' -e 'two lanes' -e 'compositions' -e 'first measurement' -e 'inside the' -e 'only class' corpus/knowledge/mutation-case-tsukuroi-census.md corpus/knowledge/arm-class-matrix.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md PROVINCE.md",
  "python3 /tmp/Read07-13Rr/sweep.py",
  "grep -n -e 'Substrate' -e 'Lanes' -e 'Admission status' -e 'two-lane' corpus/knowledge/arm-class-matrix.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md",
  "grep -n -i -e aimed -e composition corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-tsukuroi-census.md corpus/knowledge/arm-class-matrix.md",
  "python3 /tmp/Read07-13Rr/sweep2.py"
 ],
 "opened": ["SKILL.md", "corpus/knowledge/mutation-case-tsukuroi-census.md", "corpus/knowledge/arm-class-matrix.md", "PROVINCE.md", "plans/round-5.plan.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/knowledge/mutation-case-kimi-census.md", "tools/trace-inputs.py"],
 "inputs": {
  "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604",
  "corpus/knowledge/arm-class-matrix.md": "bd4f4a02eb66f4e25e67a1518108d1f11c45b4edf2355d1901ec54ce55359088",
  "PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be",
  "plans/round-5.plan.md": "5ade0413bc9a8d891df774156e597f893617ff80a49b4fe274adc204b8a63582",
  "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
  "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
  "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
 },
 "external_inputs": {
  "tsukuroi-shokunin@9bcd1627072f7d8def172eed3b7a702ff218e71e:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
  "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
  "tsukuroi-shokunin@da952909584bcad9c643e842c41d6025d732fb56:tools/tsukuroi-census.sh": "aae45531fc393579b9e575683eaca0e7f337004c19713eb9a6a213e961207df6"
 },
 "traces": [
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-1.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-2.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-3.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-4.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-5.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-6.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-7.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-8.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-10.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-11.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-12.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read07-13.json"
 ]}]}
```

What I checked, in plain English: I cold-read SKILL.md lines 668–793 at 2227d83 and classed the section as a record. I opened every lane file the section cites under the trace collector (receipts Read07-1 to Read07-8, and the keyword sweeps Read07-11 and Read07-12), and read the collector source by hand. For the sibling tool I extracted the pinned bytes with git and checked the sha256, the line count, the ten mutant sites and the case labels. Two scratch replications ran under the collector (Read07-10 and Read07-13). The first matched the section's kill table in all eleven runs, and the second matched the section 6 replay on the committed hardened bytes. The section still fails on four statements: it calls rounds 2–3 one lane's work when the sources name two lanes; it names an unmapped-paths survivor class that no source has; it calls row D the only class that survives in all three gates while row A does too; and it attaches the 6+4 composition to all three rates when only one sweep records it. Those four make the verdict wrong-expectation. The rest is citation drift and label wording. I changed no lane file.

COLDREAD Read07: wrong-expectation
