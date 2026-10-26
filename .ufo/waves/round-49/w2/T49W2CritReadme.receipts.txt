# T49W2CritReadme receipts — all reads at candidate f181a961ae44061af486f600e5ea257d2baf78f8
# unless a different rev is named. Every command ran read-only (`git -C <lane> show` / grep /
# python3 parse of a shown blob). No counter was run; no scratch dir was created; no tools
# installed (none needed).

## R1 — README frontier rule + F10 row + round-49 section
$ git show f181a961:corpus/README.md | awk 'NR>=68 && NR<=76'
68:## Frontier
70:Ground not yet held. Zero-hit sweep (non-author ART dossier,
72:`4eb4cf3`): all 12 patterns → `files=0 lines=0`. A ground moves to
73:`held` only through an admitted `knowledge/` entry with a `source:`
74:header citing a `mined` `SOURCES.md` row.
76:| id | ground | candidate sources | status | next falsifiable move (before → after) |
$ git show f181a961:corpus/README.md | awk 'NR>=105 && NR<=125'
105:## Frontier — status correction (fleet round 1, post-review, appended)
107:The `## Frontier` table above marks F1 and F2 `held (round 1)`;
109:superseded here (orchestrator adjudication, 2026-10-19) — both are
111:partly held:
120:A ground reads `held` only when its next move in the table is
121:measured.
$ git show f181a961:corpus/README.md | sed -n '599p'   (file is 599 lines; section at 593)
599:F10 (PBT generators for gate fixtures): open → **held (round 49)** for its stated next move, "one generator against a named fixture gate", conditioned on the round-49 deciding receipt `.ufo/evidence/round-49/after/c2.stdout` printing `C2_R49_PASS=true`; if it does not, this line is void and an erratum below says so. The frontier table row above stays as written (append-only); F10's next move is now a second gate, or shrinking.
$ git show f181a961:corpus/README.md | sed -n '597p'
597:| `knowledge/pbt-generator-pilot.md` | One generator, `tools/pbt-staged-id.py`, against `tools/staged-id-guard.py` through its CLI only, with its own oracle written from the guard's documented contract, twelve printed distribution classes, a seed and a case count; measured by a twelve-mutant panel hidden from its author (differential confirmation) against a fixture-replay control; the limits (one gate, no shrinking, a counter blind to a differential generator) | S269, S270 |

## R2 — F10 table row byte-identical base → candidate; lines 60-100 unchanged
$ git show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/README.md | grep -n '^| F10'
87:| F10 | PBT generators for gate fixtures | S018, S019, S020, S021 | open | no PBT fixture method → one generator against a named fixture gate |
$ git show f181a961:corpus/README.md | grep -n '^| F10'
87:| F10 | PBT generators for gate fixtures | S018, S019, S020, S021 | open | no PBT fixture method → one generator against a named fixture gate |
$ diff <(git show 8ca67421:corpus/README.md | sed -n '60,100p') <(git show f181a961:corpus/README.md | sed -n '60,100p') && echo ROWS-60-100-IDENTICAL
ROWS-60-100-IDENTICAL
$ git show f181a961:corpus/README.md | wc -l
599

## R3 — append-only declaration (coverage-map addendum, before line 68)
$ git show f181a961:corpus/README.md | grep -n 'Appended, not inserted'
(matched once, in "## Coverage map — addendum (fleet round 1, appended 2026-10-19)":
 "Appended, not inserted: the rows above keep their line numbers." — located above the
 `## Frontier` heading at 68; see also `## Frontier — status correction` 105 "appended")

## R4 — PROVINCE.md (whole file head)
$ git show f181a961:PROVINCE.md | head -47
7:**Owns:** the method, documented from the fleet's existing gates as primary
12:Also: this lane's own corpus and gates.
14:**Refuses:** product domains — every lane's gate remains its own; tameshi
15:owns only the reusable craft (a pattern is admitted from evidence in TWO
16:independent lanes before it is claimed general). Never edits a sibling's
40:**Frontier** — F1–F10 in `corpus/README.md` `## Frontier`; ground moves
41:to Core only through an admitted, source-headed `knowledge/` entry
42:whose `source:` cites a `mined` `SOURCES.md` row.

## R5 — SOURCES.md rows S269/S270 (mined, opened 2026-10-26; 11 cells)
$ git show f181a961:corpus/SOURCES.md | grep -n '^ *| *S26[89]\|^ *| *S270'
144:| S269 | QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs (Claessen, Hughes; ICFP 2000; DOI 10.1145/351240.351266) — https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf | paper | A | ...
145:| S270 | Property-based testing for functional programs (Smallbone; Chalmers University of Technology Technical Report 76L, ISSN 1652-876X, 2011) — https://smallbone.se/papers/lic.pdf | paper | B | ...
$ git show f181a961:corpus/SOURCES.md | python3 -c '<parse: cells = row.strip().strip("|").split("|")>'
S269: 11 cells | c7= mined | c8= 2026-10-26
S270: 11 cells | c7= mined | c8= 2026-10-26
$ git show f181a961:corpus/SOURCES.md | sed -n '494p'
494:- Round 49: two rows added by document from the shokuknow `corpus-expansion-1` package (theme F10), S269 (QuickCheck, ICFP 2000, ...; staged S182) and S270 (Smallbone, Chalmers TR 76L, 2011; staged S183), re-opened 2026-10-26 with snapshots under `.ufo/waves/round-49/w1/T49ScribeRows.src/`; ...

## R6 — pilot entry header and limits (corpus/knowledge/pbt-generator-pilot.md)
$ git show f181a961:corpus/knowledge/pbt-generator-pilot.md | head -5
1:source: S269 — https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf — §Abstract (p. 268), §2.4 Monitoring Test Data (p. 270), §3.2 Generators for User-Defined Types (p. 271), §5.1.4 A False Sense of Security (p. 274) — Claessen & Hughes, ICFP 2000, DOI 10.1145/351240.351266; snapshot sha256 bfddcaa6, opened 2026-10-26
2:source: S270 — https://smallbone.se/papers/lic.pdf — §2.10 Generating Test Data, printed p. 34 — Smallbone, Chalmers TR 76L, 2011; snapshot sha256 eaee48f9, opened 2026-10-26
3:verified-at: 2026-10-26
4:recheck: 365d — ...
5:ground: F10 (PBT generators for gate fixtures)
$ git show f181a961:corpus/knowledge/pbt-generator-pilot.md | awk 'NR>=60 && NR<=69'
62:- One generator against one lane-owned gate: F10's "one generator against a named fixture gate" move, not a method
63:  shown across the fleet's gates.
65:- The counter cannot tell a property-based generator from a differential one that compares the mutant with a copy of
66:  the pristine guard (wave-1 critic, `.ufo/waves/round-49/w1/T49CritC2Contract.md` F1); the evidence that this one is
67:  property-based is outside the counter: its code (CLI calls only, its own oracle), an access trace and oracle-mutation
68:  results in the round-49 wave-2 reports.

## R7 — frozen C2 counter records check (substring F10/held; mined/2026-10-26 cells)
file .ufo/evidence/round-49/c2/measure.py (frozen at 14d03ea4; read from lane working tree)
277:    ids = re.findall(r'^source:\s*(S\d{3,})\b', head, re.M)
283:        hit = [ln for ln in rows if re.match(r'^ {0,3}\|\s*' + sid + r'\s*\|', ln)]
285:        if len(cells) != 11 or cells[7] != 'mined' or cells[8] != '2026-10-26':
288:    if not any('F10' in ln and 'held (round 49)' in ln for ln in readme.decode('utf-8', 'replace').splitlines()):
290:        notes.append('readme-no-F10-held')

## R8 — contract tip rule and schedule (frozen contract, never edited)
.ufo/evidence/round-49/contract.json (freeze 14d03ea4)
:48  C2 predicate: "... the pilot entry cites a row opened 2026-10-26 and README marks F10 held (round 49): C2_R49_PASS=true."
:60  kill_rule: "exactly one deciding invocation at REV by deciding-run.sh after control receipts are committed"
:73  no_harm.tip: "after REV only receipt files under .ufo/evidence/round-49/after/ and wave reports land; ..."
:81  schedule: [... "wave 2 (falsify) against the candidate", "fixes, final REV, panel reveal commit", "one deciding run; receipts-only commit"]

## R9 — LOG.md round-49 entry
$ git show f181a961:LOG.md | sed -n '2383p;2387p;2390p;2391p'
2383:## 2026-10-26 — round 49: reading-bound cold-read refresh (calibration) + F10 property-based generator (coverage)
2387:... F10 was still `open` with no generator method (`corpus/README.md:87`).
2390:- C2: `tools/pbt-staged-id.py` (wave-1 seat T49ExecGenerator, built blind to the hidden panel); rows S269, S270 (...); entry `corpus/knowledge/pbt-generator-pilot.md`; README F10 line conditioned on the deciding receipt.
2391:- Frontier: mistake mined and fixed with a falsifier (...); assimilation theme F10 (two rows admitted, two entries refused, one deferred); ...

## R10 — QUALITY admission bar
$ git show f181a961:corpus/QUALITY.md | sed -n '3,8p;15,19p;27,30p'
3:1. Every claim falsifiable or marked opinion.
7:4. Errata are append-only blocks.
15:6. A pre-registered prediction carries its executed outcome in the same
16:   entry; a miss is an errata row naming the discriminator, never a
17:   silent drop. (MK-2, MK-3)
18:7. A knowledge file lands with its coverage-map row in the same round,
27:10. A new `knowledge/` entry opens with `source:`, `verified-at:` and
28:    `recheck:`; an external source enters through a `SOURCES.md` row
29:    opened in the round that writes it ...

## R11 — lesson Gate (row admission; entry provenance)
corpus/lessons/round-49.md
:18-29  Gate rows S269/S270 with URLs, access dates, quotes, shas
:44-49  "Admit — staged S182 → S269" / "Admit — staged S183 → S270" (anchor corrected)
:50-61  Reject r4-quickcheck-primary-correction.md; Reject pbt-generator-craft-author.md; Deferred pbt-generator-as-fixture.md
