# T53W1ExecR523 — the round-52 wave-2 "8 over-count" verdict, re-derived under one written rule

Seat: T53W1ExecR523 (wave-1 executor, judged on operability).
Item: re-derive the round-52 wave-2 review's "8 over-count" verdict over the correction records
01, 02, 06, 09-13, under ONE written counting rule, and say whether
`corpus/lessons/round-52.md`'s statement needs correction.

## 0. Bottom line

Under the rule **as written** — a correction record over-counts *iff every one of its quoted
findings is reader-marked holds/hist* — the verdict set is:

* **over-counted: 1 record — Corr02.**
* **exact: 19 records** (01, 03-20 except 02).
* **under-counted: 0 records.**

So the "8 over-count" does **not** reproduce under the stated rule. It reproduces only as *the label
wave-2 assigned* (verified: the five `T52W2RevCorr*.md` files label exactly 01, 02, 06, 09, 10, 11, 12,
13 "over"). Under the counting rule wave-2 actually applied — *over-counted iff at least one quoted
finding is reader-marked holds/hist* — the set is **7 records: 01, 02, 05, 06, 09, 11, 12**, i.e. Corr05
joins and Corr10 and Corr13 leave.

`corpus/lessons/round-52.md` therefore needs correction on three counts (§5): the numeral "11 records
are exact" (its own enumeration lists 12, and 8+12=20 is the record total), the "8 over-count" figure
(not reproducible under the stated rule; 7 under the counting reading, with different membership), and
the Corr12 example "0 of 14 findings … marked as not holding" (the reader marks 2 of 14 "drift", which
its own legend defines as "false/stale at CAND", and 4 more carry a live CAND non-holding qualifier).

The lesson's "73 findings" and "No reviewer found a missed failure" both reproduce (§5.4).

## 1. Corpus and method

* CAND1 = `7ff81a5b0ab0` (`7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`, "round-52: wave-2 fix-reads
  applied in-line (59) …").
* Working clone: `git clone --shared` of the lane at 7ff81a5 under the seat scratch; `git rev-parse HEAD`
  = `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135` before any read.
* Records: `.ufo/waves/round-52/w1/T52W1CorrNN.json` (20 files, each with `heading`, `reader`,
  `read_rev`, `wrong_expectations`, `findings[]`).
* Reader evidence: `.ufo/evidence/round-51/coldread/reads/T51W2ReadNN.md` (20 files, each with a JSON
  block carrying per-pointer `verdict` plus `findings` / `text_findings` / `strongest_*` registers).
* Review artefacts: `.ufo/waves/round-52/w2/T52W2RevCorr{0104,0508,0912,1316,1720}.md`.
* Lesson: `corpus/lessons/round-52.md` (C2 section, lines 25-28).
* All reads are `git -C <clone> show` / `git cat-file` / `jq` / `nl` over committed bytes; no working
  tree of the lane was read or written, no git or jj mutation was run anywhere outside the seat clone.

Total findings across the 20 records: **73** (`jq -s 'map(.findings|length)|add'`), matching the lesson.

## 2. The counting rule (one rule, as written, operationalised)

> **Rule R (stated).** A quoted finding `f` of record `R` is **reader-marked holds/hist** iff the reader
> file at CAND1 marks the surface `f` quotes with a hold-family disposition. `R` **over-counts** iff
> every one of its quoted findings is reader-marked holds/hist (exclude holds-hist rows per each
> record's own section 3).

Operational definition, applied per finding only from the reader's own words:

**H — reader-marked holds/hist** when the reader's disposition for the quoted surface is one of:

1. a hold-family verdict token: `holds`, `holds-hist`, `holds-as-history`, `holds-as-disclosed`,
   `holds-at-pinned-sha[+modifier]`, `holds@sha`, `holds-hist-stale-at-cand`, `holds+understates-at-cand`;
2. an explicit non-defect: a scope note recorded as *not a defect*, an item *prior-dispositioned*,
   *unadjudicable from repo bytes*, *"no falsifier" / unverifiable from the cited ranges*, *tick-scoped*,
   *correctly scoped*, *"the page itself flags"*, or a residual/`residual_unverified_prose` item that is
   not in the reader's findings register.

**Q — qualifying** otherwise: the reader asserts the quoted statement/surface does not hold —
`absent`, `absent-at-range`, `moved`, `drift`, `stale`, `FALSIFIED`, `false`, `overstates`,
`understates-at-CAND`, `off-by-one` at the section's own governed sha — or registers it in its findings
register (`findings[]`, `text_findings`, an "Adversarial summary — Unsupported/incomplete premises
found", a "Findings by severity" bullet, a numbered F-list).

**Record verdicts.**

* **over-counted** iff `N ≥ 1` and `H = N` (the empty-findings records Corr04/14/17 are exact, not
  vacuously over-counted);
* **under-counted** iff a reader-registered failure of the section is covered by no finding;
* **exact** otherwise (`H < N`, no omission).

Empty-set guard and "holds-hist exclusion" note: only Corr12 states a §3 exclusion rule
(`T52W1Corr12.json` §3: rows marked `holds`, `holds-hist`, `holds-as-disclosed` are excluded). Under
Rule R those rows are already classified H, so the exclusion removes nothing further; it is recorded here
because the item requires the check.

**Sensitivity axis R′ (reported for completeness, not the rule).** The counting rule the wave-2 review
actually applied is `over-counted iff H ≥ 1` (it labelled Corr01 over on 1 of 3, Corr06 over on 2 of 14,
Corr13 over on 2 of 6). Both readings are reported side by side so the L1 can see which numeral the
lesson is quoting.

## 3. Per-finding classification

21 of 73 findings are reader-marked holds/hist (H); 52 qualify (Q). The 21 H findings, each with the
reader's own token (byte-verbatim):

| # | record · finding | reader surface | reader's own disposition |
|---|---|---|---|
| 1 | Corr01 F3 | `Read01.residual_unverified_prose` | "the claimed report path does not exist in the CAND tree, so that historical attribution was not independently verified. It is not needed to support the adjacent SKILL.md:377-378 endpoint-identity statement." (not in `findings[]`; that array holds only the two stale anchors) |
| 2 | Corr02 F1 | Read02 P8 (SCORECARD.md:16) | verdict `holds`; "**holds**, one scope note"; "Recorded as a scope note, not a defect: the cited line says what the section claims it says." |
| 3 | Corr05 F2 | Read05 P2 (`:597-620`) | verdict `holds`; "Historically holds at round 18, but it is not a current-CAND line pointer. The qualifier is essential"; calibration: "correct as a round-18 historical pointer" |
| 4 | Corr06 F14 | Read06 T6 | "T6 weak anchor: 'enumerated, executed and skipped counts distinguished' — no skip concept in the runner …; convention lives in uncited knowledge-note manifests"; `holds_summary` excepts only T1, T2, T3 |
| 5 | Corr09 F2 | Read09 `findings[0]` clause | "'four embedded legs' superseded by ten (r51 tenth leg); **tick-scoped historical statement**, anchor stale"; `no_impact_checks`: "superseded only as a present-tense description of the harness" |
| 6 | Corr09 F3 | Read09 `findings[1]` | "prior-dispositioned as two independent runs; unadjudicable from repo bytes" |
| 7 | Corr09 F8 | Read09 `findings[6]` | "… ER-4's addendum records the 20:02Z continuation with different then-current shas, **which the page itself flags**" |
| 8 | Corr11 F2 | Read11 P13 | "held at governed sha; superseded at CAND by the TMPDIR change"; severity: "Currency (made stale by this round, **correctly scoped** by the section's own 'the sha governs' rule)" |
| 9 | Corr11 F3 | Read11 P16 | "record stands; format anchors verified; shape superseded at CAND" |
| 10 | Corr12 F2 | Read12 P3 | `holds-at-pinned-sha-imprecise+moved` |
| 11 | Corr12 F3 | Read12 P4 | `holds-at-pinned-sha+moved` |
| 12 | Corr12 F4 | Read12 P5 | `holds-at-pinned-sha-partial+moved` |
| 13 | Corr12 F5 | Read12 P6 | `holds-at-pinned-sha+moved` |
| 14 | Corr12 F6 | Read12 P7 | `holds-at-pinned-sha-partial+moved` |
| 15 | Corr12 F8 | Read12 P11 | `holds-at-pinned-sha+moved+extended` |
| 16 | Corr12 F9 | Read12 P13 | `holds-at-pinned-sha+moved` |
| 17 | Corr12 F10 | Read12 P14 | `holds-at-pinned-sha-exact+moved` |
| 18 | Corr12 F11 | Read12 P16 | `holds-hist-stale-at-cand` |
| 19 | Corr12 F12 | Read12 P17 | `holds-hist-stale-at-cand` |
| 20 | Corr12 F13 | Read12 P18 | `holds-at-pinned-sha; half-stale-at-cand` |
| 21 | Corr12 F14 | Read12 P28 | `holds+understates-at-cand` |

The 52 Q findings, by the reader evidence that grounds them:

* **Corr01 F1, F2** — Read01 P13/P23 verdict `absent/stale anchor; claim holds elsewhere`, and both are
  the reader's registered low-severity finding ("Two stale line anchors in tools/mutate-and-run.sh").
* **Corr03 F1** — Read03 P7 verdict `FALSIFIED (standing; documented round-27 Read08, never fixed …)`.
* **Corr05 F1** — Read05 `strongest_possible_falsifier_checked`: "Thus the section's progression is
  stale/incomplete at CAND: it omits the tenth round-51 leg."
* **Corr06 F1-F9** — Read06 P0-P5, P7 verdict `absent`; **F10** T1 `falsified+executed`; **F11** T2
  `stale`; **F12** T3 `stale`; **F13** T5 "minor: 'validates mode/SHA' — sha validated; mode read+mirrored,
  never compared to a recorded mode" (the section's wording does not hold; this is the one item where the
  wave-2 review and this seat differ, §4).
* **Corr07 F1** — reader finding 1 "STALE-AT-CAND — the N chain (ordinal 2), made false by the tenth
  leg"; **F2** finding 3 "ABSENT pointer, known-dead since round 16 and still carried (ordinal 3)" and
  P3 verdict `absent`; **F3** finding 2 "STALE-AT-CAND — the selftest tally (ordinal 6)".
* **Corr08 F1** — "Current-engine self-test count is stale…"; **F2** "Potential taxonomy gap (strongest
  falsifier checked)".
* **Corr09 F1** — P0 verdict `moved` + `findings[0]` "pointer tools/mutate-and-run.sh:511-518 moved at
  CAND → now 614-633"; **F4** `findings[2]` "'the same regression receipt' (1201) still overstates
  identity at CAND"; **F5** `findings[3]` "overstates identity: … the committed 7da4ec50… blob is
  131 612 B — a later commit superseded it"; **F6** `findings[4]` "'six minutes later' (1186) is 5 min
  15 s (19:15:14Z → 19:20:29Z, SKILL.md:1041/1055)"; **F7** `findings[5]` "stated without its [I] label".
* **Corr10 F1** — P0 verdict `absent-at-range (anchor rot; content moved)` + severity "anchor rot";
  **F2** reader claim-check 4: "Runner-side clause **is superseded** … so 'still not embedded' is false of
  the runner at CAND … the section still carries no supersession pointer", listed in the reader's verdict
  summary as one of "two known-class residuals".
* **Corr11 F1** — P5 verdict `off-by-one at its own governed sha; absent at range at CAND` + severity
  "Minor (anchor precision, pre-existing): `list tools/mutate-and-run.sh:85-89` is one line short at its
  own governed sha".
* **Corr12 F1** — P2 verdict `drift`; **F7** P10 verdict `drift` (legend line 50: "**drift** =
  false/stale at CAND").
* **Corr13 F1-F6** — `findings[0]` "False at CAND: map's runbook/runner/mutation-case prose says nine
  cases since round 26"; `findings[1]` "False at CAND: the map describes one row per measured gate …";
  `findings[2]` "Stale cited detail: runbook §7's default `/tmp` scratch statement …"; `findings[3]`
  "Qualified unsupported premise: README's tenth-note row is under a different table schema …".
* **Corr15 F1** — P8 verdict `stale-at-cand`; "**One stale statement (the re-key edit this section
  needs):** the leg-count progression … stops at nine."
* **Corr16 F1-F4** — "Unsupported/incomplete premises found (all pre-existing …): P2 omits its selftest-1
  exit and silently defaults `--repo`; P4 omits argparse exit 2; P3's '(round 17)' tag is imprecise
  provenance."
* **Corr18 F1** — P2 verdict `absent`.
* **Corr19 F1** — P6 verdict `stale (see falsifier)`.
* **Corr20 F1-F7** — P1 `ABSENT/STALE`, P2 "the 9/9 row itself is now unsatisfiable (see HIGH-2)",
  P13 `STALE (MED-1)`, P26 `STALE (MED-2)`, P18 `LOW-1`, P7 `LOW-2`, P12 `LOW-3`; reader verdict
  summary: "2 HIGH + 2 MED stale-by-tenth-leg/TMPDIR findings, 3 LOW prose/literal drifts".

## 4. Per-record verdicts

`N` = record's own count, `H` = reader-marked holds/hist findings, `Q` = qualifying. Rule R = the rule as
written (over iff H=N≥1). Rule R′ = counting reading (over iff H≥1). "wave-2" = the label in the
`T52W2RevCorr*` files.

| record | N | H | Q | Rule R | Rule R′ | wave-2 | wave-2's own spurious count |
|---|---|---|---|---|---|---|---|
| Corr01 | 3 | 1 | 2 | exact | over | over | 1 of 3 |
| Corr02 | 1 | 1 | 0 | **over-counted** | over | over | 1 of 1 |
| Corr03 | 1 | 0 | 1 | exact | exact | exact | — |
| Corr04 | 0 | 0 | 0 | exact | exact | exact | — |
| Corr05 | 2 | 1 | 1 | exact | over | exact | **diverges** |
| Corr06 | 14 | 1 | 13 | exact | over | over | 2 of 14 (this seat: 1 of 14) |
| Corr07 | 3 | 0 | 3 | exact | exact | exact | — |
| Corr08 | 2 | 0 | 2 | exact | exact | exact | — |
| Corr09 | 8 | 3 | 5 | exact | over | over | 7 of 8 (this seat: 3 of 8) |
| Corr10 | 2 | 0 | 2 | exact | exact | over | **diverges (2 of 2 valid)** |
| Corr11 | 3 | 2 | 1 | exact | over | over | 3 of 3 (this seat: 2 of 3) |
| Corr12 | 14 | 12 | 2 | exact | over | over | 14 of 14 (this seat: 12 of 14) |
| Corr13 | 6 | 0 | 6 | exact | exact | over | **diverges (6 of 6 valid)** |
| Corr14 | 0 | 0 | 0 | exact | exact | exact | — |
| Corr15 | 1 | 0 | 1 | exact | exact | exact | — |
| Corr16 | 4 | 0 | 4 | exact | exact | exact | — |
| Corr17 | 0 | 0 | 0 | exact | exact | exact | — |
| Corr18 | 1 | 0 | 1 | exact | exact | exact | — |
| Corr19 | 1 | 0 | 1 | exact | exact | exact | — |
| Corr20 | 7 | 0 | 7 | exact | exact | exact | — |
| **total** | **73** | **21** | **52** | **1 over / 19 exact / 0 under** | **7 over / 13 exact / 0 under** | **8 over / 12 exact** | |

**Under-count check (0 records).** For every record, each reader-registered failure of the section is
carried by a quoted finding: Corr09's 7 `findings` items are covered by its 8 quotes (item 1 split into
F1+F2); Corr06's 9 absent rows + T1/T2/T3/T5 are all present; Corr12's 14 findings are exactly the 14
non-`holds` reader rows (P2, P3, P4, P5, P6, P7, P10, P11, P13, P14, P16, P17, P18, P28); Corr13's 4
`findings` items are covered by F1-F6; Corr11's single residual (the off-by-one anchor) is F1; Corr20's
7 = 2 HIGH + 2 MED + 3 LOW. No record omits a registered failure. This reproduces the lesson's
"No reviewer found a missed failure".

### 4.1 The three records where this seat's verdict differs from wave-2

**(a) Corr05 — this seat: over-counted on the counting reading (1 of 2); wave-2: exact.**
F2's quote is Read05 `additional_checks[2]`: "At candidate runner :597-620 the historical round-18
pointer has moved; current TABLE_* assignments are :634-643. Treating the shorthand as an unqualified
CAND pointer would be stale. The historical qualifier was verified against the round-18 runner." The
reader's structured verdict for that surface is `holds`, and its notes/calibration say the citation "is
correct as a round-18 historical pointer" and "the qualifier is essential". The section's own statement
is the scoped one ("at round 18 the recorded tables sit at `:597-620`"), and the reader verified it true
at that scope — so the finding rests on a hold-family disposition (H). Wave-2 counted the
`additional_checks` sentence as a falsifier statement; that is the only basis for its "exact".
Note this is structurally the same evidence class wave-2 accepted as *qualifying* in Corr09 F1 (a runner
line range that no longer holds the cited content at CAND) and as *non-qualifying* here; the two calls are
not mutually consistent.

**(b) Corr10 — this seat: exact (2 of 2 valid); wave-2: over (1 of 2).**
F2 rests on the reader's own claim-check 4, which it labels a "split verdict": the ledger half "holds at
CAND", and "Runner-side clause **is superseded** … so 'still not embedded' is false of the runner at
CAND … the section still carries no supersession pointer". The reader lists it in its verdict summary as
one of "two known-class residuals". The reader registered a live not-holding of the section's
present-tense sentence; wave-2 excluded it on the `it narrates the r9 boundary, where it was true`
clause, but the reader itself treats the missing supersession pointer as an unamended defect.
Also note wave-2's stated reason for Corr09 F6 — that the reader "compares elapsed time using a different
pair of timestamps … than section lines 1186-1187 (20:00:34Z → 20:0…)" — is factually wrong: lines
1186-1187 contain no `20:00:34Z`; `20:00:34Z` is at :1166 (the round-9 pin read), while the sentence at
:1186 refers to the round-8 pair, whose timestamps are :1038 `19:15:14Z` and :1055 `19:20:29Z` — 5 min
15 s, exactly as the reader states. So Corr09 F6 is reader-backed.

**(c) Corr13 — this seat: exact (6 of 6 valid); wave-2: over (2 of 6).**
Wave-2 excludes finding 1 as "the historical runbook six-case statement". But F1's quote is
Read13 `findings[0]`: "False at CAND: map's runbook/runner/mutation-case prose says nine cases since round
26; runner and matching corpus files now contain ten (round 51)." The reader registers the map's own
nine-count prose as false at CAND, and F1's `skill_statement` is precisely the cell that carries that
count ("§3 the six-case ledger (six rows; the lane has held nine cases since round 26)"). The *six-case
table* being historical is a different object from the *nine-since-round-26 count*, which the reader marks
false. Wave-2's exclusion keys on the skill_statement's historical half instead of on the quoted
reader text. Finding 2 likewise rests on `findings[2]` "Stale cited detail: runbook §7's default `/tmp`
scratch statement does not account for runner's CAND TMPDIR honoring", which the reader registered.

Additional wave-2 artefact defect: `T52W2RevCorr0912.md:9` says "**Over-counted (6):** record findings
3–8" while `:58` says "Corr09: over-counted 7" and `:12` says "1 qualifying finding vs 8 recorded" — the
file contradicts itself on its own count (6 vs 7).

## 5. Does `corpus/lessons/round-52.md` need correction? Yes — three items.

Quoted at CAND1 (`git show 7ff81a5b0ab0:corpus/lessons/round-52.md`, lines 25-28):

> "The 20 correction records carry 73 findings … The wave-2 non-author review (T52W2RevCorr*) re-graded
> them:
> - 11 records are exact (03, 04, 05, 07, 08, 14-20).
> - 8 over-count (01, 02, 06, 09-13). Example: Corr12, where the reviewer found 0 of 14 findings to be
> statements the reader marked as not holding.
> - No reviewer found a missed failure."

**5.1 "11 records are exact (03, 04, 05, 07, 08, 14-20)" — the numeral is wrong: 12.**
The enumeration lists 03, 04, 05, 07, 08, 14, 15, 16, 17, 18, 19, 20 = **12** records, and 8 over + 12
exact = 20 = the record total. The wave-2 files themselves label those same 12 exact. So the word "11"
is an off-by-one; it should read "12 records are exact (03, 04, 05, 07, 08, 14-20)". (Under this seat's
Rule R′ the exact set is 13 records — the 12 above plus Corr13, minus Corr05; under the literal Rule R it
is 19.)

**5.2 "8 over-count (01, 02, 06, 09-13)" — reproduces only as a label, not as a rule result.**
The 8-record set is exactly what the five `T52W2RevCorr*.md` files assert (Corr01/02 in RevCorr0104,
Corr06 in RevCorr0508, Corr09-12 in RevCorr0912, Corr13 in RevCorr1316), so the sentence is a faithful
summary *of the review's labels*. It is not a result of the stated rule: "over-counts iff **every one** of
its quoted findings is reader-marked holds/hist" fires only on Corr02 (H=1=N=1). The 8 is only reachable
under the weaker any-of reading, and even then it is 7 with different membership (Corr05 in; Corr10 and
Corr13 out). Recommendation: replace the rule-claim with a label-claim, e.g. "the wave-2 review labelled
8 of 20 records over-counted (01, 02, 06, 09, 10, 11, 12, 13); under a uniform 'any quoted finding the
reader marked holds/hist' rule the count is 7 (01, 02, 05, 06, 09, 11, 12)".

**5.3 The Corr12 example is false as stated.**
"0 of 14 findings to be statements the reader marked as not holding" is contradicted by Read12's own
legend at line 50: "**holds-hist** = historical record, corroborated; **drift** = false/stale at CAND."
Corr12 findings F1 (P2, "--regression replays six embedded legs") and F7 (P10, "default scratch
`mktemp -d /tmp/…`") rest on rows the reader marks `drift` — i.e. statements the reader *did* mark as not
holding. Four more (F11 P16, F12 P17 `holds-hist-stale-at-cand`; F13 P18 `half-stale-at-cand`; F14 P28
`understates-at-cand`) carry a live CAND non-holding qualifier. Correct statement: "Corr12, where 12 of
14 findings rest on surfaces the reader marked holds/hist (2 are `drift`)". The example's *conclusion*
— that wave-2 found Corr12 wholly spurious — is not what the reader's bytes support.

**5.4 Two items in the same paragraph that DO reproduce.**
"73 findings" — verified by `jq` over the 20 records. "No reviewer found a missed failure" — verified:
0 under-counted records under both readings (§4).

## 6. Evidence commands

```sh
# clone at the frozen candidate (seat scratch, --shared; no mutation anywhere else)
D=/fast/scratch/hyaku/tameshi-r53/w1/T53W1ExecR523
mkdir -p "$D" && cd "$D"
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin repo
git -C repo rev-parse HEAD                      # 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135
git -C repo rev-parse --show-toplevel           # .../repo   (asserted before any fixture work)

# record corpus + finding count
for n in $(seq -w 1 20); do jq -c '{n:(.findings|length),r:.reader,we:.wrong_expectations}' \
  repo/.ufo/waves/round-52/w1/T52W1Corr$n.json; done
jq -s 'map(.findings|length)|add' repo/.ufo/waves/round-52/w1/T52W1Corr*.json   # 73

# reader verdicts (per-pointer tokens + findings registers)
python3 - <<'PY'
import re,json,glob
for p in sorted(glob.glob("repo/.ufo/evidence/round-51/coldread/reads/T51W2Read*.md")):
    t=open(p,encoding="utf-8",errors="surrogateescape").read()
    r=json.loads(re.findall(r"```json\n(.*?)\n```",t,re.S)[0])
    print(p[-6:-3],[ (str(x.get("raw"))[:40],x.get("verdict")) for x in r.get("pointers",[]) ])
    for k in ("findings","text_findings","verdict","holds_summary"): 
        if k in r: print("  ",k,json.dumps(r[k],ensure_ascii=False)[:400])
PY

# Read12 legend and the two drift rows (the lesson's example)
grep -n 'holds-hist.*=\|drift.*=' repo/.ufo/evidence/round-51/coldread/reads/T51W2Read12.md
grep -n '"verdict": "drift"' repo/.ufo/evidence/round-51/coldread/reads/T51W2Read12.md

# wave-2 labels (the "8")
grep -nE "^## |Verdict: \*\*(over|exact)|^\*\*Over-counted" repo/.ufo/waves/round-52/w2/T52W2RevCorr*.md
sed -n '9p;12p;58p' repo/.ufo/waves/round-52/w2/T52W2RevCorr0912.md      # 6 vs 7 self-contradiction

# the lesson statement under test
git -C repo show 7ff81a5b0ab0:corpus/lessons/round-52.md | nl -ba | sed -n '24,30p'

# Corr09 F6 counter-evidence (wave-2's mis-cited lines)
git -C repo show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | sed -n '1166p;1186,1188p;1038p;1055p'
```

## 7. Limits and residual risk

* The rule's per-finding step is a *reading* of the reader's disposition, not an arithmetic check. The
  two decisions that move a record between buckets are: (i) whether a reader's "currency"-style note
  (correctly scoped / tick-scoped / prior-dispositioned) is a hold (H) — I take it as H, which is what
  produces Corr05- and Corr11-shaped results; and (ii) whether a pointer row whose verdict is a bare
  `holds` but whose nearby prose registers a defect counts as Q — I take the register as governing
  (Corr13, Corr16, Corr20's LOW items). Both decisions are documented per finding in §3.
* Corr12's own §3 is self-contradictory (it counts rows marked "moved/imprecise/partial" while excluding
  rows marked `holds`/`holds-hist`), which is why its 14 findings include 12 hold-family rows. The
  exclusion clause was applied as written and changed nothing.
* Two records (Corr04, Corr14, Corr17) have zero findings; they are exact by the empty-set guard, not by
  a vacuous reading of "every one".
* This seat did not re-execute any runner or gate; all evidence is committed bytes at CAND1 and at the
  readers' `read_rev` `02ec217c4d0afabe727fde2e261b7951d28fb4e9`.

## 8. Seat hygiene

* Write scope respected: only `.ufo/waves/round-53/w1/T53W1ExecR523.md` (this file) was written under the
  lane. No edit to `SKILL.md`, `corpus/`, `tools/`, `MANIFEST.json` or `.ufo/evidence/`.
* No git/jj mutation outside the seat clone; no commit, push, fetch or prune anywhere.
* No tool install was needed (python3 + jq + git were already present); nothing was recorded.
* Scratch: `git clone --shared` under `/fast/scratch/hyaku/tameshi-r53/w1/T53W1ExecR523/`, deleted at the
  end of the seat (`trap 'rm -rf -- "$S"' EXIT` pattern); `/tmp` was not used.
