# T50ScribeCorrections — receipts

seat: `T50ScribeCorrections`, round-50 w1, base `e3729de862f73ae080d98fcf522a7081ce16e40a`.
All commands run from the lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, read-only.
Outputs are as observed; long lines are not wrapped.

## R1 — base equivalence of every cited file

```
$ git diff --stat e3729de862f73ae080d98fcf522a7081ce16e40a..HEAD -- corpus/ SCORECARD.md LOG.md
 SCORECARD.md | 21 +++++++++++++++++++++
 1 file changed, 21 insertions(+)
$ for f in corpus/lessons/round-40.md corpus/lessons/round-41.md corpus/lessons/round-44.md corpus/lessons/round-46.md corpus/lessons/round-47.md corpus/lessons/round-48.md corpus/QUALITY.md; do a=$(git show e3729de862f73ae080d98fcf522a7081ce16e40a:$f | sha256sum | cut -c1-12); b=$(sha256sum "$f" | cut -c1-12); echo "$f base=$a now=$b"; done
corpus/lessons/round-40.md base=9fcaf9769054 now=9fcaf9769054
corpus/lessons/round-41.md base=fc53bd00718e now=fc53bd00718e
corpus/lessons/round-44.md base=00b6e55f12c8 now=00b6e55f12c8
corpus/lessons/round-46.md base=ddd392eec5bc now=ddd392eec5bc
corpus/lessons/round-47.md base=50b47845be56 now=50b47845be56
corpus/lessons/round-48.md base=e1dfbae2c3d3 now=e1dfbae2c3d3
corpus/QUALITY.md base=2f8c77c9d2ab now=2f8c77c9d2ab
$ git diff e3729de862f73ae080d98fcf522a7081ce16e40a..HEAD -- SCORECARD.md | grep -iE 'R40\.4|R46\.4|R44\.1|R47\.3|correction'
 **Planned (round 50):** a successor C1 counter that caps `absent` and requires evidence for it; the C2 counter's differential-generator blind spot (sandboxed generator, no pristine guard in reach); generator reach (5-cell rows, duplicate map keys, numeric order past the digit boundary); SKILL.md:1503/1509/1555 outside-section corrections; carried items from round 48's list.
```

The only post-base SCORECARD line that matches is the Planned paragraph; it names none of the five
ids and is not a correction.

## R2 — ancestry of the three commits that added the existing corrections

```
$ git merge-base --is-ancestor a3d6c690bcbf8914551d4f4e8e1612784c1c2046 b37ce974 && echo "r41-after-routed_at=yes"
r41-after-routed_at=yes
$ git merge-base --is-ancestor 5891bdb77aba8489683533ae4cdd3b49b5e2626b ea25e0224fc81060414b27301c27bd1344669165 && echo "q87-after-r44-routed=yes"
q87-after-r44-routed=yes
$ git merge-base --is-ancestor 473336d9d789f6081195e7376d17836a24666bc3 50545328e7ac4ba1703d70030e37dacec9362e68 && echo "r48-after-r47-routed=yes"
r48-after-r47-routed=yes
$ git log -S 'the round-40 closure' --format='%H %s' -- corpus/lessons/round-41.md | head -1
b37ce974b6efb8c465626d7346149549a3300a4b round-41: C1 records reconciliation + C2 write-path-census-v3 (sources S153/S154, lesson, amendments A1-A4)
$ git log -S 'Criterion 87' --format='%H %s' -- corpus/QUALITY.md | head -1
ea25e0224fc81060414b27301c27bd1344669165 round-45: records — lesson, QUALITY criteria 86-87 with falsifier receipts, SCORECARD round-45 block (Planned round 46, standing registry 117), LOG entry, README F3 wording; preview receipts
$ git log -S 'C1-R48-1' --format='%H %s' -- corpus/lessons/round-48.md | head -1
50545328e7ac4ba1703d70030e37dacec9362e68 round-48: C2 records - rows S265-S268, snapshots and receipts, re-pointed entries, lesson draft
```

## R3 — R40.1: the round-40 quarantine table and the summary sentence

```
$ sed -n '73p' corpus/lessons/round-40.md | grep -oE 'S1[0-9]{2}' | tr '\n' ' '; echo
S109 S131 S137 S140 S141 S143
$ grep -nE '^\| S(109|131|137|140|141|143) ' corpus/lessons/round-40.md | grep -ci 'refuse'
6
$ grep -ci 'the prose class is stale' corpus/lessons/round-40.md
3
$ grep -nE '^\| S(113|123|134) ' corpus/lessons/round-40.md | cut -d'|' -f1,2
58:| S113 
61:| S123 
67:| S134 
$ awk '/^### Quarantine/{f=1;next} f&&/^\| S[0-9]/{n++} END{print n}' corpus/lessons/round-40.md
17
$ grep -n '^| S109 ' corpus/lessons/round-40.md
56:| S109 | payload-absent | absent — the landing page carries no abstract body; the linter's ABSENT is mechanically correct. Refuse | `ScoutQ109` |
```

(The capital-`Refuse` form alone counts 5; `S131` writes "refuse as pinned", so the case-insensitive
count is 6.)

## R4 — R40.4: the S152 label and the re-count

```
$ python3 -c "import re;s='drawbacks such as fragility and lack of context can lead to false positives';print(len(s.split()), len(re.findall(r'[A-Za-z0-9]+', s)))"
13 13
$ grep -n 'Quote (11 words)' corpus/lessons/round-40.md
14:- Quote (11 words), English abstract: "drawbacks such as fragility and lack of context can lead to false positives".
$ grep -n 'The quote is 11 words' corpus/knowledge/r6-snapshot-practice-corpus.md
10:S152 is the UFMG thesis PDF. The English abstract, in the committed excerpt, says snapshot tests are easy to implement and that drawbacks such as fragility and lack of context can lead to false positives. The quote is 11 words: "drawbacks such as fragility and lack of context can lead to false positives".
$ sed -n '75p' corpus/lessons/round-41.md | cut -c1-200
| count-label-drift | this round's first draft of `corpus/knowledge/r41-variable-destination-writes.md` labelled the S153 quote "16 words" and the S154 quote "17 words"; the token counts are 15 and 16
```

## R5 — R44.1: the Stryker quote and criterion 87

```
$ python3 -c "import re;s='Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!';print(len(s.split()), len(re.findall(r'[A-Za-z0-9]+', s)))"
28 22
$ sed -n '26p' corpus/lessons/round-44.md
  - line 15, 20 words: “Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!”
$ grep -n "Criterion 87\|A label that disagrees\|Lesson: \`corpus/lessons/round-44.md:26\`\|its own parenthetical" corpus/QUALITY.md
1223:### Criterion 87 — a quote's length is measured, never written by hand
1229:for it. A label that disagrees with the measured count is a record defect fixed append-only
1235:Lesson: `corpus/lessons/round-44.md:26` labels the Stryker quote "20 words"; measured, it is 28
1242:grounding quote was compliant, and its own parenthetical "24 letter/digit words" is itself
$ sed -n '158p' corpus/lessons/round-45.md | cut -c1-330
| number-drift | `corpus/lessons/round-44.md:26` labels the Stryker line-15 quote "20 words"; measured `whitespace_tokens=28 letter_digit_words=22`, and the round-45 C1 counter grades that quote `('invalid', 'quote length 28')` (`.ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout`); the 20 was inherited from `corpus/le
$ cat .ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout
lesson label: "20 words"; quote='Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!'
whitespace_tokens=28 letter_digit_words=22
C1 grade on the round-44 label quote: ('invalid', 'quote length 28')
$ git log -S 'number-drift' --format='%H %s' -- corpus/lessons/round-45.md | head -1
ea25e0224fc81060414b27301c27bd1344669165 round-45: records — lesson, QUALITY criteria 86-87 with falsifier receipts, SCORECARD round-45 block (Planned round 46, standing registry 117), LOG entry, README F3 wording; preview receipts
$ git merge-base --is-ancestor 5891bdb77aba8489683533ae4cdd3b49b5e2626b ea25e0224fc81060414b27301c27bd1344669165 && echo yes
yes
```

## R6 — R46.4: the S259 Gate quote is still folded in the committed lesson

```
$ sed -n '40,43p' corpus/lessons/round-46.md
- Located quote, 18 tokens (the abstract appears three times on the page, so the folded text holds
  the string three times): “We found that, across all projects, undetected flaky failures account
  for 9.8 %-16.3 % of failed pipeline runs.”
- Decision: **admit**. Craft: a rerun inside the same job is both the detection mechanism and its
$ python3 -c "
for i,l in enumerate(open('corpus/lessons/round-46.md',encoding='utf-8'),1):
    if '9.8 %' in l: print(i, [hex(ord(c)) for c in l if c in '\u2013\u2014-'])
"
42 ['0x2d']
81 ['0x2013', '0x2d', '0x2d', '0x2013', '0x2014']
$ grep -o '9\.8 %–16\.3 %' .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html | wc -l
3
$ grep -o '9\.8 %-16\.3 %' .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html | wc -l
0
$ diff corpus/lessons/round-46.md .ufo/evidence/round-47/quality/round46-lesson-dash-restored.md
42c42
<   for 9.8 %-16.3 % of failed pipeline runs.”
---
>   for 9.8 %–16.3 % of failed pipeline runs.”
$ diff corpus/lessons/round-46.md .ufo/evidence/round-47/quality/round46-lesson-dash-restored.md >/dev/null; echo "diff_exit=$?"
diff_exit=1
$ python3 .ufo/evidence/round-47/quality/lesson-quote-check.py corpus/lessons/round-46.md; echo exit=$?
LQ PASS arxiv-2504.16777-abs.html 'finding that 75% of flaky tests across all projects belong t'
LQ FAIL tum-portal-flaky-failures.html 'We found that, across all projects, undetected flaky failure'
LQ PASS google-flaky-feed-6277555988217606236.json 'about 84% of the transitions we observe from pass to fail in'
LESSON_QUOTE_CHECK: file=corpus/lessons/round-46.md blocks=3 quotes=3 bad=1 unbound=1
exit=1
$ python3 -c "print(len('We found that, across all projects, undetected flaky failures account for 9.8 %-16.3 % of failed pipeline runs.'.split()))"
18
```

The checker is read-only on a lesson argument; its only `open(..., 'w')` is line 131, inside the
`--selftest` tempdir.

## R7 — grep sweep for any existing correction of these items

Long lines cut with `cut -c1-140` (or `-110`/`-150` where noted); the finding never depends on the cut
tail, and the full lines were read separately where it does.

```
$ grep -rn -i "correction\|errata" corpus/lessons/round-4[5-9].md | cut -c1-140
corpus/lessons/round-45.md:161:| scope | `.ufo/waves/round-45/w1/RevGtestProvince.md` HIGH-1: the adopted entry draft said the lane's `env-d
corpus/lessons/round-46.md:115:Wave 2 (35 seats, `T46`-prefixed) attacked the content revision `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`. F
corpus/lessons/round-48.md:94:a correction is a new row that supersedes, never a second copy): `.ufo/waves/round-48/w1/T48ScoutPackage.md` t
corpus/lessons/round-48.md:102:(correction C1-R48-2 below). Flip: a lane-opened row for that paper tied to an own-leg F7 re-sweep decision.
corpus/lessons/round-48.md:106:## Corrections to earlier lessons (append-only)
corpus/lessons/round-48.md:108:## Correction C1-R48-1 — the round-47 dependence sets (unreceipted freeze-time observation)
corpus/lessons/round-48.md:121:The two sets this correction is about are `six-leg regression ledger` {fleet-root, node} and `hermetic env-di
corpus/lessons/round-48.md:176:### Correction (appended; `corpus/lessons/round-47.md` is never rewritten)
corpus/lessons/round-48.md:207:## Correction C1-R48-2 — the refusal of `r8-predictive-test-selection-cost.md` (wrong decisive cite)
corpus/lessons/round-48.md:266:### Correction (appended)
corpus/lessons/round-48.md:286:## Bounds of the two corrections
corpus/lessons/round-48.md:288:- `corpus/lessons/round-47.md`, `SCORECARD.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `T47RevProvince.md` and t
corpus/lessons/round-48.md:290:- Drafted by wave-1 seats `T48ScribeLessonCorrection` (`.ufo/waves/round-48/w1/T48ScribeLessonCorrection.draf
corpus/lessons/round-48.md:384:## Attempt 3 (L1 TameshiR48a3) — deciding run, errata, mined mistake
corpus/lessons/round-48.md:404:| `scope` — a claim's own record edits moved a pre-registered no-harm monitor, and the first check that cou
corpus/lessons/round-49.md:53:- **Reject — `r4-quickcheck-primary-correction.md`.** Decisive reason (QUALITY 2, the claim must be true): t
corpus/lessons/round-49.md:71:section critics audited 135 non-pointer statements (`T49Sec*.findings.json`): 113 true, 15 false, 7 unverifiab
corpus/lessons/round-49.md:75:Forty-five wave-1 corrections landed (`.ufo/evidence/round-49/c1/corrections.json`: 44 under `corrections`, 1 
corpus/lessons/round-49.md:76:`corrections_pass2`; each with its seat and reason; all line-neutral, so no SKILL.md line pointer moved): 12 f
corpus/lessons/round-49.md:92:| 3 | reference drift: SCORECARD's round-48 standing section said every evidence cell was the `--emit` output 
$ ls corpus/lessons/round-50.md 2>&1
ls: cannot access 'corpus/lessons/round-50.md': No such file or directory
$ grep -rn "S259" corpus/ SCORECARD.md LOG.md | cut -c1-110
corpus/knowledge/r5-undetected-flaky-failures.md:1:source: S259 — https://portal.fis.tum.de/en/publications/
corpus/lessons/round-45.md:74:  are different documents wearing held ids and move: S155→S258, S156→S259, S
corpus/lessons/round-46.md:9:from the read-only package `shokuknow/merge/tameshi` as new rows S258/S259/S260, 
corpus/lessons/round-46.md:32:### Admit — S259 (new row): *An Empirical Study of Detected and Undetected Fla
corpus/lessons/round-46.md:75:adopted S195→S258 (the same document), S190→S259 (by work: the staged row's 
corpus/lessons/round-46.md:82:  retired shokuknow id that names no lane row; flip: cite S259 (the entry now do
corpus/lessons/round-46-verifier-spotcheck.md:20:Conformance defects (status-neutral): none material. Two note
corpus/lessons/round-46-verifier-spotcheck.md:48:Committed deciding line (`after/c3.stdout`): `rows=3 entries=
corpus/lessons/round-46-verifier-spotcheck.md:54:- Each of the three entries has `source: S258|S259|S260`, `ve
corpus/lessons/round-46-verifier-spotcheck.md:83:| S259 TUM portal record (TSE 2026) | admit | live portal URL
corpus/lessons/round-46-verifier-spotcheck.md:86:| Reject (a): r6's “S140 round 5” cross-reference | rejec
corpus/lessons/round-46-verifier-spotcheck.md:89:Result: the spot-check agrees with the gate on 3 admits and 2
corpus/lessons/round-46-verifier-spotcheck.md:102:4. **Lesson quote fidelity.** Print the S259 gate quote with
corpus/SOURCES.md:134:| S259 | An Empirical Study of Detected and Undetected Flaky Test Failures in Real-World
corpus/SOURCES.md:487:Round 46: three rows added, S258 (arXiv 2504.16777, Systemic Flakiness), S259 (the TUM p
corpus/README.md:574:| `knowledge/r5-undetected-flaky-failures.md` | A same-job rerun is both the detection me
corpus/README.md:577:Frontier F3 (determinism precondition, flaky-aware verdicts) gains two published measurem
SCORECARD.md:2208:| C3 three flaky-failure documents enter as rows S258/S259/S260, each cited by a re-grounded
LOG.md:2323:- Claim C3 (coverage, sourced, assimilation). Before `rows=0 entries=0`. Rows S258/S259/S260 adopt
$ grep -rln "S152" --include=*.md . | grep 'lessons/round-4[2-9]'; echo "rc=$?"
rc=1
$ grep -n "9\.8" SCORECARD.md LOG.md; echo "rc=$?"
rc=1
$ grep -rn "tum-portal\|en dash" corpus/lessons/round-4[7-9].md | cut -c1-150
corpus/lessons/round-47.md:105:| reference-drift + vacuous | `corpus/lessons/round-46.md:42` prints `9.8 %-16.3 %`; the snapshot holds `9.8 %–16.3 %
```

No round-42+ lesson carries a named correction for R40.4 or R46.4; the only later record that mentions
the S259 dash is `round-47.md:105` (the Mistakes row analysed in R6). `corpus/lessons/round-50.md` does
not exist. The id sweep returns no corpus correction (R10).

## R8 — R47.3: the existing named correction

```
$ grep -n "C1-R48-1\|Corrections to earlier lessons" corpus/lessons/round-48.md | head
106:## Corrections to earlier lessons (append-only)
108:## Correction C1-R48-1 — the round-47 dependence sets (unreceipted freeze-time observation)
178:- **C1-R48-1 (corrects `corpus/lessons/round-47.md:117-118`; the file is never rewritten).**
$ sed -n '176,189p' corpus/lessons/round-48.md
### Correction (appended; `corpus/lessons/round-47.md` is never rewritten)

- **C1-R48-1 (corrects `corpus/lessons/round-47.md:117-118`; the file is never rewritten).**
  The round-47 lesson's "observed dependence sets" — `six-leg regression ledger` {fleet-root, node},
  `hermetic env-differential probe` {env, node} — are the **freeze-time** emission
  (`.ufo/evidence/round-47/before/c1-at-freeze.stdout:5,17` =
  `control/emit-observed-pre-freeze.out:5,17`), printed there without receipt, revision or round.
  The round-47 standing rows, which restate the content-revision emission, declare
  {env, fleet-root, node} (`SCORECARD.md:2270`) and {bwrap, node} (`SCORECARD.md:2276`); the
  deciding run at `8b0e15d2…` observed {fleet-root, node} and {bwrap, node} and scored the
  `six-leg` row `DEPS-MISMATCH` (`.ufo/evidence/round-47/after/c1.stdout:5,17`, verdict
  `total=2 … dep_mismatch=1 … C1_R47_PASS=false`). Both statements are the two the round-47
  disclosure names as unstable across runs under host load (`SCORECARD.md:2314`).
  **Rule for later rounds:** a dependence set is restated only from the deciding `--emit`, with
  that receipt's path and revision named beside it; a freeze-time set is labelled as the freeze
```

## R9 — sibling row for R40.4 (for the L1's cross-check, not a verdict)

```
$ python3 -c "
import json
d=json.load(open('.ufo/waves/round-50/w1/T50Disp40.rows.json'))
rows=d['rows'] if isinstance(d,dict) and 'rows' in d else d
for r in rows:
    if r.get('id')=='R40.4': print(json.dumps(r,indent=1))
"
{
 "id": "R40.4",
 "status": "fixed",
 "evidence": [{"path": "corpus/lessons/round-41.md", "lines": "75-75",
  "excerpt": "the round-40 closure's routed defect 4 (a quote labelled \"11 words\" that has 13 tokens)"}],
 "commit": "b37ce974b6efb8c465626d7346149549a3300a4b",
 "seat": "T50Disp40",
 "note": "erratum states the true count (13; `printf '%s' '<quote>' | wc -w` prints 13) against round-40.md:14's 'Quote (11 words)' label; the closed file is not rewritten, per the round-40 routing's own convention for item 1",
 "fix_plan": null
}
```

## R10 — id sweep, SCORECARD Planned check, and the sibling rows

```
$ grep -rn "R40\.4\|R46\.4" --include=*.md --include=*.json --include=*.py . | grep -v 'round-50/c1/defects.json' | grep -v 'verifier-spotcheck' | cut -c1-110
./.ufo/evidence/round-50/c1/keys.json:5: "R40.4": ["S152", "13 tokens", "11 words"],
./.ufo/evidence/round-50/c1/keys.json:30: "R46.4": ["S259", "en dash"],
./.ufo/evidence/round-50/control/c1-CTL_FAB.ledger.json:32:  "id": "R40.4",
./.ufo/evidence/round-50/control/c1-CTL_FAB.ledger.json:324:  "id": "R46.4",
./.ufo/waves/round-50/w1/T50Disp40.rows.json:64:   "id": "R40.4",
./.ufo/waves/round-50/w1/T50Disp40.receipts.md:77:# R40.4 numeric truth
./.ufo/waves/round-50/w1/T50Disp40.md:60:## R40.4 — the S152 quote was labelled "11 words"; it has 13 tokens
./.ufo/waves/round-50/w1/T50Disp40.md:138:- R40.4 fixed: erratum `corpus/lessons/round-41.md:75` gives the tru
./.ufo/waves/round-50/w1/T50Cross46.json:74:   "id": "R46.4",
./.ufo/waves/round-50/w1/T50Cross46.json:77:   "doubt": "Checked corpus/lessons/round-46.md:42: the S259 Gate 
./.ufo/waves/round-50/w1/T50Cross46.md:35:## R46.4 — lesson quote fidelity (S259 en dash / fold at the quote
./.ufo/waves/round-50/w1/T50Cross46.md:54:- R46.4 declined: round-46 lesson:42 still hyphen; fold only in entr
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:22:| R40.4 | implicit only (a Mistakes-table antecedent, not 
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:24:| R46.4 | **no** | — | — | **C1-R50-1** |
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:70:## R40.4 — implicit erratum only; no named correction
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:87:records R40.4 `fixed` on `round-41.md:75`
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:135:## R46.4 — missing; the committed lesson still prints t
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:203:## Cross-seat conflict on R46.4 (recorded, not resolved h
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:207:- `.ufo/waves/round-50/w1/T50Cross46.md:35` — "R46.4 �
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:210:- `.ufo/waves/round-50/w1/T50Disp46.rows.json` (id `R46.4
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:234:### Correction C1-R50-1 — R46.4: the S259 Gate quote is
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:274:### Correction C1-R50-2 — R40.4: the S152 quote is 13 t
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:354:  C1-R50-1's fold declaration satisfies R46.4's "in the l
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:359:- R46.4 has no correction: `round-46.md:42` still prints 
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:362:- C1-R50-1 is the append-only fold declaration; C1-R50-2 
./.ufo/waves/round-50/w1/T50ScribeCorrections.md:365:- R40.4 implicit only at `round-41.md:75`; live `r6-snaps
./.ufo/waves/round-50/w1/T50ScoutPlanned.md:65:Spot-check ids with **no planned counterpart** (the ledger need
./.ufo/waves/round-50/w1/T50ScoutPlanned.md:66:labels; R40.1 and R40.4 were noted as corrected by `corpus/less
./.ufo/waves/round-50/w1/T50ScoutPlanned.md:71:`round-44.md`), R44.2, R45.1 (`round-46.md:121`), R45.3 (`round
./.ufo/waves/round-50/w1/T50Disp46.rows.json:87:   "id": "R46.4",
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/recurrence-walk.json:41:   "id": "R40.4",
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/recurrence-walk.json:242:    "R40.4"
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/recurrence-walk.json:346:   "id": "R46.4",
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/build_table.py:7: "R40.4": ("r41 corpus/lessons/round-41.md
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/build_table.py:23: "R44.1": ("r45 corpus/lessons/round-45.m
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/build_table.py:32: "R46.4": ("r47 corpus/lessons/round-47.m
./.ufo/waves/round-50/w1/T50ScribeCorrections.receipts.md:67:## R4 — R40.4: the S152 label and the re-count
./.ufo/waves/round-50/w1/T50ScribeCorrections.receipts.md:94:## R6 — R46.4: the S259 Gate quote is still fol
./.ufo/waves/round-50/w1/T50ScribeCorrections.receipts.md:189:No round-42+ lesson carries a named correction f
./.ufo/waves/round-50/w1/T50ScribeCorrections.receipts.md:218:## R9 — sibling row for R40.4 (for the L1's cr
./.ufo/waves/round-50/w1/T50ScribeCorrections.receipts.md:226:    if r.get('id')=='R40.4': print(json.dumps(r,
./.ufo/waves/round-50/w1/T50ScribeCorrections.receipts.md:229: "id": "R40.4",
./.ufo/waves/round-50/w1/T50Disp46.md:33:## R46.4 — open
./.ufo/waves/round-50/w1/T50Disp46.md:49:1. Rows only, on a scratch clone at lane tip: `EXPLAIN open-unplanned
./.ufo/waves/round-50/w1/T50Disp46.md:50:2. The same rows plus a probe-only `**Planned (round 50), amended:**`
./.ufo/waves/round-50/w1/T50Disp46.md:52:Explain every line naming a R46 id: the only two are `open-unplanned 
./.ufo/waves/round-50/w1/T50Disp46.md:63:- R46.4 open: `corpus/lessons/round-46.md:42` still prints the hyphen
./.ufo/waves/round-50/w1/T50RevengerRecur.md:37:| R40.4 | r41 corpus/lessons/round-41.md:75 | 10 | **open** | 
./.ufo/waves/round-50/w1/T50RevengerRecur.md:53:| R44.1 | r45 corpus/lessons/round-45.md:158 | 6 | **open** | 
./.ufo/waves/round-50/w1/T50RevengerRecur.md:62:| R46.4 | r47 corpus/lessons/round-47.md:105 | 1 | r47 | class
./.ufo/waves/round-50/w1/T50RevengerRecur.md:92:open with carried >= 2: R40.2(10) R40.3(10) R40.4(10) R42.2(8)
./.ufo/waves/round-50/w1/T50RevengerRecur.md:103:  re-classified as disclosed or operator-owned* (R40.4, R44.1
./.ufo/waves/round-50/w1/T50RevengerRecur.md:135:| label-count (R40.4, R44.1) | **Q87** (`:1223`, r45) | 0 —
./.ufo/waves/round-50/w1/T50RevengerRecur.md:136:| quote-fold (R46.4) | **Q91** (`:1355`, r47) | 0 — r48 re-
./.ufo/waves/round-50/w1/T50RevengerRecur.md:165:Weaker relations worth naming: R40.2 ≈ R41.2 (pointer/recei
./.ufo/waves/round-50/w1/T50RevengerRecur.md:185:   * **R40.4**: `corpus/lessons/round-40.md:14` still reads "
./.ufo/waves/round-50/w1/T50RevengerRecur.md:250:selftest). It does **not** reach R40.4/R44.1's uncorrected in
./.ufo/waves/round-50/w1/T50RevengerRecur.md:287:The long tail is not lapsed fixes but items never given one: 
./.ufo/waves/round-50/w1/T50RevengerRecur.md:291:Four duplicate chains carry 18 of the 49 rows (SHONEN alone i
./.ufo/waves/round-50/build-spec-w1.py:70:     "For the lesson-correction items R40.1, R40.4, R44.1, R46.4, R4
$ grep -c 'R46\.4' SCORECARD.md; echo "rc=$?"
0
rc=1
$ grep -n 'Planned (round' SCORECARD.md | tail -1
2410:**Planned (round 50):** a successor C1 counter that caps `absent` and requires evidence for it; the C2 counter's differential-generator blind spot (sandboxed generator, no pristine guard in reach); generator reach (5-cell rows, duplicate map keys, numeric order past the digit boundary); SKILL.md:1503/1509/1555 outside-section corrections; carried items from round 48's list.
$ sed -n '2410p' SCORECARD.md | grep -c 'R46\.4'
0
$ sed -n '64,67p' .ufo/waves/round-50/w1/T50ScoutPlanned.md
(blank line)
Spot-check ids with **no planned counterpart** (the ledger needs no Planned entry unless open): R40.1-R40.4 (typos/
labels; R40.1 and R40.4 were noted as corrected by `corpus/lessons/round-41.md:53` and :75), R40.5 (depth guard:
SCORECARD.md:1859 is the r39 guard-agreement C1, but R40.5's routed_at is `a3d6c69`, after it, so the keyed excerpt
$ sed -n '35,40p' .ufo/waves/round-50/w1/T50Cross46.md | fold -w 200 -s
## R46.4 — lesson quote fidelity (S259 en dash / fold at the quote): DECLINED

`corpus/lessons/round-46.md:42` still prints the hyphen form (`for 9.8 %-16.3 % of failed pipeline runs.`); no fold statement sits at the quote. The en-dash fold is disclosed only in 
`corpus/knowledge/r5-undetected-flaky-failures.md:25-32`, which does not satisfy "in the lesson itself". The verifier spot-check file is byte-pinned (`sha256sum` = 
`104c609956cb75dda3214fa179ffa36472696fd3e47500e6893ebbba44b823a0` at both routed_at and base). The lane judged the fold wording-only (recorded at `round-46-verifier-spotcheck.md:20`) and declined to 
rewrite the landed lesson record; no Planned paragraph names R46.4 → declined (≥40-char reason), not open.
$ sed -n '37p;53p;62p' .ufo/waves/round-50/w1/T50RevengerRecur.md | cut -c1-200
| R40.4 | r41 corpus/lessons/round-41.md:75 | 10 | **open** | class: label-count (r44 spot-check:73), then Q87 held (0 after r45) | label-count | R44.1 |
| R44.1 | r45 corpus/lessons/round-45.md:158 | 6 | **open** | class: label-count, no recurrence after Q87 | label-count | R40.4 |
| R46.4 | r47 corpus/lessons/round-47.md:105 | 1 | r47 | class: quote-fold, no recurrence after Q91 | quote-fold | — |
```

The id sweep's own-file lines are this seat's two files (written before the sweep was taken); every
other hit is a wave-50 seat, an evidence pin, or the build spec — no `corpus/` correction. Later edits
to this deliverable shifted its own line numbers, so the stable form of the same sweep excludes them:

```
$ grep -rn "R40\.4\|R46\.4" --include=*.md --include=*.json --include=*.py . | grep -v 'round-50/c1/defects.json' | grep -v 'verifier-spotcheck' | grep -v 'T50ScribeCorrections' | cut -c1-110
./.ufo/evidence/round-50/c1/keys.json:5: "R40.4": ["S152", "13 tokens", "11 words"],
./.ufo/evidence/round-50/c1/keys.json:30: "R46.4": ["S259", "en dash"],
./.ufo/evidence/round-50/control/c1-CTL_FAB.ledger.json:32:  "id": "R40.4",
./.ufo/evidence/round-50/control/c1-CTL_FAB.ledger.json:324:  "id": "R46.4",
./.ufo/waves/round-50/w1/T50Disp40.rows.json:64:   "id": "R40.4",
./.ufo/waves/round-50/w1/T50Disp40.receipts.md:77:# R40.4 numeric truth
./.ufo/waves/round-50/w1/T50Disp40.md:60:## R40.4 — the S152 quote was labelled "11 words"; it has 13 tokens
./.ufo/waves/round-50/w1/T50Disp40.md:138:- R40.4 fixed: erratum `corpus/lessons/round-41.md:75` gives the tru
./.ufo/waves/round-50/w1/T50Cross46.json:74:   "id": "R46.4",
./.ufo/waves/round-50/w1/T50Cross46.json:77:   "doubt": "Checked corpus/lessons/round-46.md:42: the S259 Gate 
./.ufo/waves/round-50/w1/T50Cross46.md:35:## R46.4 — lesson quote fidelity (S259 en dash / fold at the quote
./.ufo/waves/round-50/w1/T50Cross46.md:54:- R46.4 declined: round-46 lesson:42 still hyphen; fold only in entr
./.ufo/waves/round-50/w1/T50ScoutPlanned.md:65:Spot-check ids with **no planned counterpart** (the ledger need
./.ufo/waves/round-50/w1/T50ScoutPlanned.md:66:labels; R40.1 and R40.4 were noted as corrected by `corpus/less
./.ufo/waves/round-50/w1/T50ScoutPlanned.md:71:`round-44.md`), R44.2, R45.1 (`round-46.md:121`), R45.3 (`round
./.ufo/waves/round-50/w1/T50Disp46.rows.json:87:   "id": "R46.4",
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/recurrence-walk.json:41:   "id": "R40.4",
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/recurrence-walk.json:242:    "R40.4"
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/recurrence-walk.json:346:   "id": "R46.4",
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/build_table.py:7: "R40.4": ("r41 corpus/lessons/round-41.md
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/build_table.py:23: "R44.1": ("r45 corpus/lessons/round-45.m
./.ufo/waves/round-50/w1/T50RevengerRecur.receipts/build_table.py:32: "R46.4": ("r47 corpus/lessons/round-47.m
./.ufo/waves/round-50/w1/T50Disp46.md:33:## R46.4 — open
./.ufo/waves/round-50/w1/T50Disp46.md:49:1. Rows only, on a scratch clone at lane tip: `EXPLAIN open-unplanned
./.ufo/waves/round-50/w1/T50Disp46.md:50:2. The same rows plus a probe-only `**Planned (round 50), amended:**`
./.ufo/waves/round-50/w1/T50Disp46.md:52:Explain every line naming a R46 id: the only two are `open-unplanned 
./.ufo/waves/round-50/w1/T50Disp46.md:63:- R46.4 open: `corpus/lessons/round-46.md:42` still prints the hyphen
./.ufo/waves/round-50/w1/T50RevengerRecur.md:37:| R40.4 | r41 corpus/lessons/round-41.md:75 | 10 | **open** | 
./.ufo/waves/round-50/w1/T50RevengerRecur.md:53:| R44.1 | r45 corpus/lessons/round-45.md:158 | 6 | **open** | 
./.ufo/waves/round-50/w1/T50RevengerRecur.md:62:| R46.4 | r47 corpus/lessons/round-47.md:105 | 1 | r47 | class
./.ufo/waves/round-50/w1/T50RevengerRecur.md:92:open with carried >= 2: R40.2(10) R40.3(10) R40.4(10) R42.2(8)
./.ufo/waves/round-50/w1/T50RevengerRecur.md:103:  re-classified as disclosed or operator-owned* (R40.4, R44.1
./.ufo/waves/round-50/w1/T50RevengerRecur.md:135:| label-count (R40.4, R44.1) | **Q87** (`:1223`, r45) | 0 —
./.ufo/waves/round-50/w1/T50RevengerRecur.md:136:| quote-fold (R46.4) | **Q91** (`:1355`, r47) | 0 — r48 re-
./.ufo/waves/round-50/w1/T50RevengerRecur.md:165:Weaker relations worth naming: R40.2 ≈ R41.2 (pointer/recei
./.ufo/waves/round-50/w1/T50RevengerRecur.md:185:   * **R40.4**: `corpus/lessons/round-40.md:14` still reads "
./.ufo/waves/round-50/w1/T50RevengerRecur.md:250:selftest). It does **not** reach R40.4/R44.1's uncorrected in
./.ufo/waves/round-50/w1/T50RevengerRecur.md:287:The long tail is not lapsed fixes but items never given one: 
./.ufo/waves/round-50/w1/T50RevengerRecur.md:291:Four duplicate chains carry 18 of the 49 rows (SHONEN alone i
./.ufo/waves/round-50/build-spec-w1.py:70:     "For the lesson-correction items R40.1, R40.4, R44.1, R46.4, R4
```
