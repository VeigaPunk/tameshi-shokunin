# T53W2ExecR523B — independent re-derivation of the R52.3 "8 over-count" verdict, and confirm/overturn of T53W1ExecR523's eight verdicts

Seat: `T53W2ExecR523B` (executor, wave 2). Lane `tameshi-shokunin`. Item: read `T53W1ExecR523`'s report,
apply **its** written counting rule myself from scratch (scratch clone at `7ff81a5`), and confirm or
overturn each of its **8 record verdicts** (records `01, 02, 06, 09, 10, 11, 12, 13` — the eight the
round-52 non-author review labelled *over*), with any disagreement cited against the counting-rule clause.

Read-only on the lane. This file is the only lane write. No git/jj mutation anywhere. No tools installed
(`git`, `python3`, `sed`, `nl`, `fold` already present), so no tool/version/channel row is owed.

**Bottom line: all eight of T53W1ExecR523's record verdicts are CONFIRMED** under both readings of its
rule. Two of its per-finding classifications differ from mine (Corr06 F13, and the Corr12 `holds@sha`
family) without changing any record verdict; one of mine was wrong and is corrected here on comparison
(Corr10 F2). The prior coordination message I sent while its report was unwritten was answered by the
report itself, which landed at `24927` bytes and is now the base of record.

---

## 0. The target: T53W1ExecR523's report (present, read in full)

```
$ stat -c '%s %y %n' .../.ufo/waves/round-53/w1/T53W1ExecR523.md
24927 2026-10-27 11:27:43.224234640 -0300 .../w1/T53W1ExecR523.md
```

It states the rule as written — *"A quoted finding `f` of record `R` is reader-marked holds/hist iff the
reader file at CAND1 marks the surface `f` quotes with a hold-family disposition. `R` over-counts iff
**every one** of its quoted findings is reader-marked holds/hist (exclude holds-hist rows per each
record's own section 3)"* — and reports **two** roll-ups:

* **Rule R (as written, `H = N`)**: `over-counted: 1 record — Corr02`; `exact: 19`; `under-counted: 0`.
* **Rule R′ (the "any-of" reading wave-2 actually used, `H ≥ 1`)**: **7 over** — `01, 02, 05, 06, 09, 11,
  12`; 13 exact; 0 under.

Its per-record numbers for my eight records, and its per-finding register (21 H of 73), are reproduced
verbatim in §4 below for the comparison.

---

## 1. Counting rule I applied (verbatim source, then operationalised)

**Source 1 — wave-1 dispatch item (`spec-w1.json` → items[name=T53W1ExecR523]):**

> "… under ONE written counting rule: a correction record over-counts iff every one of its quoted findings
> is reader-marked holds/hist at CAND1 `7ff81a5b0ab0` (exclude holds-hist rows per each record's own
> section 3)."

**Source 2 — closure routing, R52.3 (`corpus/lessons/round-52-verifier-spotcheck.md:85`):**

> "Re-derive the '8 over-count' verdict for records 01, 02, 06, 09–13 under one written counting rule
> (reader-marked drift at CAND; exclude `holds-hist` rows per the record's own §3) …"

**R-53-a (applied, per finding):**

1. A finding **qualifies (Q)** iff the reader file named by that record, at CAND1, records the underlying
   **section statement** as not holding at CAND — reader token in `FALSIFIED` / `false` / `**drift**` /
   "stale at CAND" / "absent"/"absent-at-range" / `moved` / "off-by-one at its own governed sha" /
   "overstates identity" / "understates at CAND" / "half stale at CAND", or an unsupported premise the
   reader registers in its own findings register (`findings[]`, "Findings by severity", an F-list).
2. It is **reader-marked holds/hist (H)** where the reader marks the same statement `holds`, `holds@sha`,
   `holds-hist`, `holds-as-disclosed`, or scopes it out as historical-and-accurate, "prior-dispositioned",
   "unadjudicable", "no falsifier"/unverifiable, a scope note ("not a defect"), *"correctly scoped"*,
   *tick-scoped*, *"the page itself flags"*, or residual/unverified prose.
3. `holds-hist` rows are **excluded per each record's own §3** (only Corr12 wrote such a rule —
   `T52W1Corr12.md:44-48`, `:89-100`; under clause 2 those rows are H already, so the exclusion removes
   nothing further — wave-1 reaches the same conclusion independently).
4. **Record verdicts**, reported under both readings because the dispatch text is ambiguous:
   * **R (as written)** — *over-counted* iff `N ≥ 1` and `H = N` (empty-findings records are exact, not
     vacuously over-counted); *exact* otherwise;
   * **R′ (any-of)** — *over-counted* iff `H ≥ 1`; *exact* otherwise; *under-counted* iff the reader
     registered a failure no finding carries (0 records under either reading).

I apply **R-53-a = R/R′ on wave-1's own operationalisation**, because the literal "every one" clause in
Source 1 cannot be the operative one for a re-derivation whose object is a *set of records labelled over*
— it fires on one record only. Presenting both is the honest form; wave-1 does the same.

---

## 2. Evidence base (verified before classification)

```
$ S=/fast/scratch/hyaku/tameshi-r53/w2/T53W2ExecR523B
$ git clone --shared -q /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/repo && cd $S/repo
$ git checkout -q 7ff81a5b0ab0
$ git rev-parse --show-toplevel     # /fast/scratch/hyaku/.../T53W2ExecR523B/repo   (asserted: my clone)
$ git rev-parse HEAD                # 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135
$ git diff --stat 02ec217c4d0afabe727fde2e261b7951d28fb4e9 7ff81a5b0ab0 -- .ufo/evidence/round-51/coldread/reads
(empty)   # reader files byte-identical at CAND1 and at the readers' read_rev
```

All 51 record findings of the eight records were located byte-exactly in the reader files at CAND1
(quote→line map; every quote matched a single line, no truncation fallback). Reader files opened in full
for 09/10/11/12/13 and in the relevant sections for 01/02/06. Section bytes and governed-revision bytes
re-read from git objects, never the worktree:

```
$ git show 02ec217c…:SKILL.md | sed -n '1164,1211p;1212,1229p;1272,1364p;1380,1395p'
$ git show 606716f7:tools/mutate-and-run.sh | sed -n '80,90p;540,560p;1108,1142p;1085,1092p;115,120p;1486,1490p;1525,1530p'
```

Governed-revision (`606716f7` = tool sha `75ed934d…`) anchors independently re-verified for every
pointer finding I classify: the six-leg list sits at `:84-89` (so the section's `:85-89` misses leg 1);
pins at `:542-553`, tables at `:554-559` (so cited `:550-559` excludes legs 1-4 pins); the six-leg
registry at `:1112-1141` (so cited `:1132-1141` covers legs 5-6 only); `:104-106` is the mode-mirror
comment; `:115-117` is the exit map; `:1488`/`:1527` are the first/last exec-bit selftest arms.

---

## 3. Per-record re-derivation (from scratch) — with the two calls I changed on comparison

### Corr01 — `## Mutation-sweep recipe …` / T51W2Read01 — 3 findings

| F | quote at | reader mark | class |
|---|---|---|---|
| F1 | Read01:9 | pointer row `:39` "absent/stale anchor; claim holds elsewhere"; registered in `findings[]` `:67` ("Two stale line anchors …") | Q |
| F2 | Read01:10 | pointer row `:49` "absent/stale anchor" | Q |
| F3 | Read01:65 | `residual_unverified_prose`; pointer row `:56` for `SKILL.md:377-378` = **holds**; not in `findings[]` | H |

`N=3, H=1, Q=2` → **R: exact / R′: over-counted.** Identical to wave-1 (H=1).

### Corr02 — `## Restore discipline …` / T51W2Read02 — 1 finding

| F | quote at | reader mark | class |
|---|---|---|---|
| F1 | Read02:162 | P8 verdict `:150` "**holds**, one scope note"; `:166` "Recorded as a scope note, **not a defect**"; section verdict `:265` "holds"; no `findings` key in the reads.json row | H |

`N=1, H=1, Q=0` → **R: OVER-COUNTED / R′: over-counted.** Identical to wave-1.

### Corr06 — `### Using the ledger` / T51W2Read06 — 14 findings

Reader §2 pointer table `:65-74`: rows 1-8 and 10 **absent**, row 9 (`:83-108`) **holds**; §3 T1
`**FALSIFIED (executed)**`, T2/T3 `**stale**`, T5 "**minor wording**", T6 "**weak anchor** … **no
falsifier**".

| F | quote at | reader mark | class |
|---|---|---|---|
| F1-F9 | Read06:65-72,74 | pointer rows 1-8, 10 = **absent** (row 9 holds correctly omitted) | Q ×9 |
| F10 | Read06:78 | T1 "**FALSIFIED (executed).**" | Q |
| F11 | Read06:83 | T2 "**stale**" (`cases=10`) | Q |
| F12 | Read06:86 | T3 "**stale**" (nine dispatches → ten) | Q |
| F13 | Read06:91 | T5 "**minor wording**": "the sha is validated … the mode is read and mirrored, **never compared against a recorded mode**" — the section's `validates mode` does not hold | **Q — changed on comparison** (I first called this H because the reader affirms the sha; wave-1 calls it Q and its reading is better: the quoted claim is `validates mode/SHA`) |
| F14 | Read06:92 | T6 — "Unverifiable from the cited ranges alone; **no falsifier**" | H |

`N=14, H=1, Q=13` → **R: exact / R′: over-counted.** Matches wave-1 exactly (H=1). Wave-2's count
(2 spurious) still overstates by one.

### Corr09 — `### The tick, executed` / T51W2Read09 — 8 findings

Reader `findings` array `:87-94` (7 bullets; record split bullet 1 into F1+F2); section self-scope
`SKILL.md:1188-1189` "timestamped observation … never carried as a standing claim".

| F | quote at | reader mark | class |
|---|---|---|---|
| F1 | Read09:88a | pointer row `:28` verdict **moved** (`:511-518` now run_sweep loop; PIN block `:614-633`) | Q |
| F2 | Read09:88b | pointer row `:29` "'Four embedded legs' is **tick-scoped** (true at the r7-1 tool …)"; prose `:124`; `no_impact_checks` `:99` | H |
| F3 | Read09:89 | "prior-dispositioned as two independent runs; **unadjudicable from repo bytes**" | H |
| F4 | Read09:90 | "'the same regression receipt' (1201) **still overstates identity at CAND**"; prose `:132-133` | Q |
| F5 | Read09:91 | prose §4 `:135-136` "**Minor, prior-known wording defects re-confirmed at CAND:** 'committed as `7da4ec50…`' overstates byte identity" | Q |
| F6 | Read09:92 | prose §4 `:136` "'six minutes later' is 5 min 15 s" (19:15:14Z→19:20:29Z at `SKILL.md:1038`/`:1055`; independent arithmetic) | Q |
| F7 | Read09:93 | prose §4 `:136-137` "the owners-editing attribution drops its [I] label" (ledger:356 carries `[I]`) | Q |
| F8 | Read09:94 | "… **which the page itself flags**"; section `:1207-1208` discloses the addendum; pointer row `:64` = **holds** | H |

`N=8, H=3, Q=5` → **R: exact / R′: over-counted.** Identical H count to wave-1 (3); wave-2's "1 of 8"
is overturned.

### Corr10 — `### The receipt at this boundary` / T51W2Read10 — 2 findings

| F | quote at | reader mark | class |
|---|---|---|---|
| F1 | Read10:108 | pointer ordinal 0 "**absent-at-range (anchor rot; content moved)**"; severity "Minor (known class, deepened by this round): anchor rot on `tools/mutate-and-run.sh:733-791`" | Q |
| F2 | Read10:80 | severity `:115-119`: "**Minor (known class, still unamended): superseded present-tense narration.** 'Cases 5–6 are still not embedded' **is false of the runner at CAND** … no supersession pointer has been added since … the re-key would credit the sentence as-is" | **Q — my call was wrong; corrected on comparison.** I first classed it H on the reader's closing line "the two stale items above are anchor/narration **currency, not record errors**". That line classifies *record errors* (the receipt values), not whether the sentence holds at CAND; the reader registers the unamended defect in its own severity list. The discriminator against Corr11 F2 is reader-authored: Read10 says "**still unamended … no supersession pointer has been added since**"; Read11 says "**correctly scoped** by the section's own 'the sha governs' rule" |

`N=2, H=0, Q=2` → **R: exact / R′: exact.** Matches wave-1 exactly (H=0). Wave-2's "over (1 of 2)" is
overturned.

### Corr11 — `## The operator's runbook and the six-leg regression …` / T51W2Read11 — 3 findings

| F | quote at | reader mark | class |
|---|---|---|---|
| F1 | Read11:71 | pointer row 5 "**off-by-one at its own governed sha; absent at range at CAND**"; severity `:112-115` "**is one line short at its own governed sha** — the six-entry list sits at :84-89 there". Verified at `606716f7` (`:84` js-kimi-census … `:89` js-claims-check) | Q |
| F2 | Read11:78 | pointer row 13 "held at governed sha; superseded at CAND by the TMPDIR change"; severity `:116-120` "**Currency … correctly scoped** by the section's own 'the sha governs' rule" | H |
| F3 | Read11:85 | reader concludes `:88-90` "The section's 'six' statements remain true only as records of `75ed934d…` … so **this is currency, not error**" | H |

`N=3, H=2, Q=1` → **R: exact / R′: over-counted.** Identical H count to wave-1 (2); wave-2's "0 of 3" is
overturned.

### Corr12 — `### The six-leg regression …` / T51W2Read12 — 14 findings

Reader legend `:49-50`: "**holds** = true at CAND; **holds@sha** = true at the governing sha, moved/stale
at CAND; **holds-hist** = historical record, corroborated; **drift** = false/stale at CAND." Reader §4
note `:100`: anchors "**were already imprecise at the governing sha** (list `:84-89` not `:85-89`; pins
`:542-553` outside the cited `:550-559`; registry `:1112-1141` not `:1132-1141`)".

| F | row (line) | reader mark | wave-1 | me |
|---|---|---|---|---|
| F1 | P2 (55) | **drift** (+ §3 F1 "Drift confirmed") | Q | Q |
| F2 | P3 (56) | holds@sha **(imprecise)** + moved — imprecise at the governed sha, verified `:84-89` | H | **Q** |
| F3 | P4 (57) | holds@sha + moved — sources `:90-97` exact at the sha | H | H |
| F4 | P5 (58) | holds@sha **(partial)** + moved — pins `:542-553`/tables `:554-559` vs cited `:550-559`, verified | H | **Q** |
| F5 | P6 (59) | holds@sha + moved — specs `:766`/`:841` exact at the sha | H | H |
| F6 | P7 (60) | holds@sha **(partial)** + moved — registry `:1112-1141` vs cited `:1132-1141`, verified | H | **Q** |
| F7 | P10 (63) | **drift** (+ §3 F2 "Drift confirmed") | Q | Q |
| F8 | P11 (64) | holds@sha + moved/**extended** (+ §3 F7 exit map "**Drift confirmed**", r30 clause) | H | **Q** |
| F9 | P13 (66) | holds@sha + moved — comment `:104-106` exact at the sha | H | H |
| F10 | P14 (67) | holds@sha + moved — arms `:1488-1527` exact at the sha | H | H |
| F11 | P17 (70) | **holds-hist**, stale at CAND → H by clause 2 and by Corr12 §3 | H | H |
| F12 | P18 (71) | **holds-hist**, stale at CAND | H | H |
| F13 | P19 (72) | holds@sha; **half stale at CAND** (+ §3 F8 "Drift confirmed", ten rates) | H | **Q** |
| F14 | P29 (82) / §4 note (102) | "holds, **understates at CAND**" — "no ledger registry row exists and the registry is ten legs" | H | **Q** |

`N=14`: **wave-1 `H=12, Q=2`; me `H=6, Q=8`.** Both give **R: exact / R′: over-counted** — the verdict is
identical; only the "how much" number differs. The delta is one classification question: whether
`holds-at-pinned-sha` rows that also carry `imprecise` / `partial` / `half stale` / `understates` /
`moved+extended` are H (wave-1) or Q (me). The reader's own §4 names the imprecision a defect *at the
governing sha the section pins* (`:84-89` not `:85-89`, verified in the governed blob) and its §3
confirms drift for the exit map and the ten-rate EXPECT, so I count those six as Q. Under either split,
wave-2's "0 of 14" is refuted: at minimum F1 and F7 are literal `**drift**` rows.

### Corr13 — `### The map — where a reader enters, artifact by artifact` / T51W2Read13 — 6 findings

Reader `findings` array `:37-40` records four not-holding statements; the six findings map onto them
(bullet 1 supplies F1, F4, F5).

| F | quote at | reader mark | class |
|---|---|---|---|
| F1 | Read13:16 | `findings[0]` "**False at CAND:** map's runbook/runner/mutation-case prose says nine cases since round 26; runner and matching corpus files now contain ten (round 51)" | Q |
| F2 | Read13:16 | `findings[2]` "**Stale cited detail:** runbook §7's default `/tmp` scratch statement does not account for runner's CAND TMPDIR honoring" | Q |
| F3 | Read13:18 | `findings[1]` "**False at CAND:** the map describes one row per measured gate but the tenth drift-pins sweep is present …" | Q |
| F4 | Read13:24 | "The map's `nine since round 26` count is **stale at CAND** (case 10 was added in round 51)" | Q |
| F5 | Read13:25 | "The map's nine-leg endpoint is **false at CAND**" | Q |
| F6 | Read13:26 | `findings[3]` "**Qualified unsupported premise** …" | Q |

`N=6, H=0, Q=6` → **R: exact / R′: exact.** Matches wave-1 exactly (H=0). Wave-2's "over (2 of 6)" is
overturned.

---

## 4. Result: confirm/overturn of wave-1's eight verdicts

| record | N | wave-1 H | my H | wave-1 Q | my Q | wave-1 R | my R | wave-1 R′ | my R′ | **confirm?** |
|---|---|---|---|---|---|---|---|---|---|---|
| Corr01 | 3 | 1 | 1 | 2 | 2 | exact | exact | over | over | **CONFIRM both** |
| Corr02 | 1 | 1 | 1 | 0 | 0 | **over** | **over** | over | over | **CONFIRM both** |
| Corr06 | 14 | 1 | 1 | 13 | 13 | exact | exact | over | over | **CONFIRM both** (I changed F13 to Q on comparison) |
| Corr09 | 8 | 3 | 3 | 5 | 5 | exact | exact | over | over | **CONFIRM both** |
| Corr10 | 2 | 0 | 0 | 2 | 2 | exact | exact | exact | exact | **CONFIRM both** (I changed F2 to Q on comparison) |
| Corr11 | 3 | 2 | 2 | 1 | 1 | exact | exact | over | over | **CONFIRM both** |
| Corr12 | 14 | 12 | 6 | 2 | 8 | exact | exact | over | over | **CONFIRM both**; H-count differs (§3) |
| Corr13 | 6 | 0 | 0 | 6 | 6 | exact | exact | exact | exact | **CONFIRM both** |

* **Verdict-level disagreements: none.** All eight of wave-1's verdicts reproduce under both readings.
* **Classification-level differences (no verdict effect):** Corr06 F13 (wave-1 Q, my first pass H → I
  adopt Q) and Corr12's `holds@sha`+`imprecise/partial/half-stale/understates/extended` rows (wave-1 H,
  me Q → `H=12` vs `H=6`; the record is over-counted under R′ either way).
* **My own correction:** Corr10 F2 — I first called it H on the reader's closing "currency, not record
  errors" line; wave-1 calls it Q and is right, because that line classifies the receipt *values*, while
  the reader registers the narration as "still unamended … no supersession pointer has been added since".
  Both of us now score Corr10 `H=0, Q=2`.
* **Under-counted: 0** under both readings. I walked every reader `findings` register for the eight
  records against the record findings; none omits a reader-registered failure (Corr09's seven bullets =
  F1-F8; Corr12's 14 findings = the 14 non-`holds` rows; Corr13's four bullets cover F1-F6; Corr06's nine
  absent rows + T1-T3 = F1-F12 with row 9 and the T4 dating note correctly excluded). This reproduces the
  lesson's "No reviewer found a missed failure".

**What that does to the "8 over-count" figure.** Both wave-1 and I reach the same place: the 8-record set
is exactly the **label** the five `T52W2RevCorr*.md` files assigned; it is **not** the output of the rule
as written (that fires on Corr02 alone), and under the uniform any-of reading it is **7 over / 13 exact**
over all 20 records — `01, 02, 05, 06, 09, 11, 12` — with different membership (Corr05 in; Corr10 and
Corr13 out). Within the eight-record scope of this seat the any-of set is **6 over** (`01, 02, 06, 09, 11,
12`) **+ Corr10 and Corr13 exact.**

---

## 5. `corpus/lessons/round-52.md` — corrections (agreed with wave-1, independently derived)

1. **`:26` "11 records are exact (03, 04, 05, 07, 08, 14-20)" — the numeral is wrong: 12.** The
   parenthetical enumerates 12 records (5 + 7). 8 over + 12 exact = 20 = the record total, and the
   wave-2 files label those same 12 exact. Fix: "12 records are exact".
2. **`:27` "8 over-count (01, 02, 06, 09-13)" reproduces only as a label, not as a rule result.** Under
   the rule as written only Corr02 qualifies; under the uniform any-of reading the count is 7 with
   different membership. Fix: state it as the review's label and, if a rule result is wanted, print the
   any-of set (`01, 02, 05, 06, 09, 11, 12`).
3. **`:27` the Corr12 example — "0 of 14 findings to be statements the reader marked as not holding" — is
   false.** Read12:50 defines `**drift** = false/stale at CAND`; Read12:55 (P2) and Read12:63 (P10) are
   literal `**drift**` rows and Read12:88-90 print "**Drift confirmed.**" three times. At minimum 2 of 14
   qualify (I derive 8, wave-1 derives 2 — both refute 0). Fix: "… where 12 of 14 findings rest on
   surfaces the reader marked holds/hist (2 are `drift`)" or drop the example.
4. **Two items in the same paragraph do reproduce** and need no change: "73 findings" (verified by
   `jq -s 'map(.findings|length)|add'` over the 20 records) and "No reviewer found a missed failure".

---

## 6. Findings (each with the counting-rule clause cited)

**F1 — wave-2's Corr12 count ("0 of 14") violates clause 1.** `**drift**` is defined by the reader's own
legend as "false/stale at CAND" (Read12:50), and P2/P10 carry it (Read12:55, :63) with "Drift confirmed"
at :88-90. Confirmed by wave-1 independently; only the qualifying *count* differs (2 vs 8).

**F2 — wave-2's Corr11 count ("0 of 3") violates clause 1.** Read11:71 registers "off-by-one at its own
governed sha"; the reviewer's stated reason ("the anchor is correct as the stated historical pin governs
it") is refuted by the governed blob: `git show 606716f7:tools/mutate-and-run.sh | sed -n '80,90p'` puts
js-kimi-census at `:84`, so the cited `:85-89` is one line short at `75ed934d…` itself. This is the
"selectively truncated citation" class R52.3 named. Wave-1 finds the same (H=2 of 3).

**F3 — wave-2's Corr09 count ("1 of 8") under-reads the reader's own CAND register.** Read09:135 heads
"**Minor, prior-known wording defects re-confirmed at CAND:**" and the record's F4-F7 quote exactly those
items. Verdict (`over`) unaffected; count corrected to 3 H / 5 Q (identical to wave-1).

**F4 — the wave-2 Corr09 entry contradicts itself.** `T52W2RevCorr0912.md:9` heads "**Over-counted (6):**
record findings 3–8" while `:58` prints "Corr09: over-counted 7" and `:12` "1 qualifying finding vs 8
recorded". A rule that yields 6 and 7 for one record has not been written down. Wave-1 records the same
defect (its §4.1).

**F5 — wave-2's Corr13 `over` verdict violates clause 1.** Corr13 F1's `skill_statement` is the map cell
carrying "the lane has held nine cases since round 26", and Read13 `findings[0]` says "**False at CAND:**
map's runbook/runner/mutation-case prose says nine cases since round 26". The reviewer excluded it by
keying on the cell's *historical* half instead of the quoted reader text. Confirmed independently by
wave-1 (H=0 of 6 → exact).

**F6 — `corpus/lessons/round-52.md:26` arithmetic.** "11 records are exact (03, 04, 05, 07, 08, 14-20)"
enumerates 12 records. Decidable without any reader file; wave-1 reaches the same reading.

**F7 — the rule as dispatched is ambiguous, and both seats had to report two readings.** "over-counts iff
**every one** of its quoted findings is reader-marked holds/hist" (spec-w1 item) fires on Corr02 alone,
while the round-52 review it re-derives used "any one". Wave-1 publishes both roll-ups (§0) and so do I
(§1.4). The L1 owns the choice; the lesson row should not be corrected against one reading while the
other is live.

**F8 — my earlier coordination message to T53W1ExecR523 is superseded.** Sent while its report was
unwritten, it said the artefact was absent. The report landed (`24927` B) and is the base of §0 and §4;
the absence was a timing artefact, not a defect in the seat.

---

## 7. Bounds, cleanup, disclosure

- Writes: this report only. Everything else read-only (`git show`/`cat-file` from the lane's object store;
  `ls`/`grep`/`sed` on `.ufo/waves/round-52/{w1,w2}/`, `.ufo/evidence/round-51/coldread/reads/`,
  `corpus/`, `.ufo/waves/round-53/w1/`).
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2ExecR523B/` (clone + one 4 KB extraction), **deleted
  before yield**; nothing written to `/tmp`; `TMPDIR` never relied on.
- Git: one `git clone --shared` and one `git checkout --detach` inside my own clone; `rev-parse
  --show-toplevel` asserted before any use. No commit, push, fetch, or jj anywhere.
- No tools installed or upgraded (uv/npm/cargo/pacman untouched; pacman is paused host-wide).
- No counter run as a verdict; no claim decided; `.ufo/evidence/` and `.ufo/waves/round-52/` read only.
- LSP: not mounted for revision-pinned Markdown, so no symbol-level check was available; every verdict
  here is a direct byte comparison of reader text and git objects.

## 8. Summary

- Read `T53W1ExecR523.md` (24 927 B), took its written rule (H = reader-marked holds/hist; exclude
  `holds-hist` per each record's own §3), and re-derived all eight records from scratch at `7ff81a5` with
  reader files verified byte-identical to `read_rev 02ec217c` (so no CAND1/read_rev drift can explain a
  disagreement).
- **All eight of wave-1's verdicts CONFIRM under both readings of its rule** (R: only Corr02
  over-counted; R′: 01, 02, 06, 09, 11, 12 over, 10 and 13 exact). No verdict-level disagreement.
- Two classification deltas with no verdict effect: Corr06 F13 (wave-1 Q; I adopt Q), and Corr12's
  `holds@sha` family (wave-1 H=12; me H=6, Q=8 — the record is over-counted under R′ either way).
- **I correct one of my own calls**: Corr10 F2 is Q (reader: "still unamended … no supersession pointer
  has been added since"), so Corr10 is exact `2/2`; my first pass classed it H on the reader's closing
  "currency, not record errors" line, which speaks to the receipt values, not to whether the sentence
  holds at CAND. The reader-authored discriminator against Corr11 F2 is "correctly scoped".
- **Lesson:** three corrections (11 → 12 exact; "8" is the review's label, not a rule result — any-of set
  is 7 with different membership; the Corr12 "0 of 14" example is false), plus two items that reproduce
  (73 findings; no missed failure).
- **Under-counted: 0.** No record omits a reader-registered failure of its section.
- No scratch left; no lane mutation; no installs.
