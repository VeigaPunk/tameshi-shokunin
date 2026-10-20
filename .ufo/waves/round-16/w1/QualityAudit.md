# QualityAudit — `corpus/QUALITY.md` criteria 1–17 citation audit (round 16, w1)

Read-only citation audit. No lane file was modified; no tool was run except file reads,
`grep`/`sed`/`git log`/`git status`/`sha256sum`/`cmp`/`ls`. Report target was absent before
this write (`test -e …QualityAudit.md` → `ABSENT`).

## 0. Pin and method

- Lane HEAD: `28aeef498cc070c3183271b709bc79d344ff547a` (`2026-10-20T06:00:06-03:00`,
  round-15 verifier spot-check commit).
- Target: `corpus/QUALITY.md`, 84 lines, sha256
  `534f42f51b16f64e1ee672daac55557b721478c59f1ccfa0e9cf956e1a02a68d`.
- Every criterion 6–17 cites a lesson file and a named row/class; all nine cited lesson
  files exist. Checks below are **literal path:line greps**. No `lsp` device is in this
  seat's tool inventory and Markdown has no answering language server here, so this is the
  text-level fallback, not semantic proof (recorded per the role's no-server rule).
- Verdict vocabulary used here: **grounded** (cited file and named row/class exist and the
  criterion's text is carried by it), **grounded, row-precision minor** (content is in the
  cited lesson file but part of it lives outside the named row), **no lesson anchor**
  (no lesson file/row cites or produced the criterion), **unmarked/candidate** (cannot be
  asserted as fact).

Criterion line map (from `grep -nE "^[0-9]+\. " corpus/QUALITY.md`):
C1:3, C2:4, C3:6, C4:7, C5:8, C6:15, C7:18, C8:21, C9:24, C10:27, C11:34, C12:39,
C13:43, C14:50, C15:61, C16:68, C17:77.

## 1. Verdict table — criteria 1–17

| # | QUALITY line | Cited anchor | What the anchor actually contains (path:line) | Verdict |
|---|---|---|---|---|
| 1 | 3 | none | No lesson row produced it. Captured-by only: `lessons/round-1.md:289` (MK-10) lists ``QUALITY.md` 1/3`. | no lesson anchor (captured-by only) |
| 2 | 4 | none | No lesson row produced it. Captured-by: `lessons/round-1.md:280` (MK-1) lists ``QUALITY.md` 2`. | no lesson anchor (captured-by only) |
| 3 | 6 | none | No lesson row produced it. Captured-by: MK-10 `lessons/round-1.md:289` (`QUALITY.md 1/3`). | no lesson anchor (captured-by only) |
| 4 | 7 | none | No occurrence of criterion 4 in `corpus/lessons/`, `corpus/knowledge/` or `corpus/README.md` (see §5 census). | **no lesson anchor** |
| 5 | 8 | none | No occurrence of criterion 5 in those trees; `round-1-verifier-spotcheck.md:17`'s `QUALITY 5→10 criteria` is a criterion-count, not C5. | **no lesson anchor** |
| 6 | 15 | `lessons/round-1.md` MK-2, MK-3 | `round-1.md:281` MK-2 “Pre-registered prediction wrong, kept only by author habit”; `:282` MK-3 “Same class repeated one round later”; both Fix cells name `QUALITY.md 6`. | grounded |
| 7 | 18 | MK-4 | `round-1.md:283` “Index lags the corpus: knowledge files land without coverage-map rows”; Fix cell `QUALITY.md 7`. Anchor `round-10.md:175-176` re-checked: “`reports/r10-ver-t10.md` absent … 9 rows covering 6 of 16 knowledge notes”. | grounded |
| 8 | 21 | MK-5 | `round-1.md:284` “Executed verification never landed as a report”; Fix cell `QUALITY.md 8`. Re-check: `LOG.md:368` “`reports/r10-ver-t10.md` still absent”, `LOG.md:389` “`reports/r11-ver-t11.md` not landed”; both files still absent (`ls` exit 2). | grounded |
| 9 | 24 | MK-6 | `round-1.md:285` “Evidence retained only under `/tmp`, later lost”; Fix cell `QUALITY.md 9`. Re-check: `knowledge/executor-test-sufficiency.md:14-18` shows `/tmp/tameshi-r3-4-work/`; `ls -d` → `No such file or directory` (exit 2). | grounded |
| 10 | 27 | MK-7 | `round-1.md:286` “Entries admitted without provenance header or recheck cadence”; Fix cell `QUALITY.md 10 (new entries)`. `corpus/SOURCES.md` header (“a row is a claim opened in the round that writes it”) and `S049` at `SOURCES.md:58` exist. | grounded |
| 11 | 34 | `lessons/round-12.md`, vacuous | `round-12.md:50`: “vacuous … one pristine observation per sweep cannot detect changing subsequent controls … Add standalone exact-tuple repeated-control gate; a deterministic changing fixture must defeat the single-control baseline and be refused by the new gate.” The “finite agreement, not a determinism proof” clause is at `round-12.md:155-156`; the “same committed mismatch oracle” red/green clause at `:160-164`. Neither is in row 50. | grounded, row-precision minor |
| 12 | 39 | `lessons/round-12.md`, attribution | `round-12.md:51`: “attribution … declaration partly contaminated … Preserve scalar scores and `[~]` marks, disclose prior exposure, freeze declaration before execution. Declaration integrity must reject changed evidence…”. Two other clauses are elsewhere: “declared defects/0 accidental/16 slots = 14+2” at `:176-178`; “a bash witness reanalysis is a seventh independent gate … same leg” at `:23`. | grounded, row-precision minor |
| 13 | 43 | `round-1-verifier-spotcheck.md`, Adjudication; `round-12.md`, attribution | `round-1-verifier-spotcheck.md:17`: “the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed)”. `round-12.md:51`’s evidence pointer is exactly that line. Both cited anchors exist and carry the promotion-restraint point. | grounded |
| 14 | 50 | `lessons/round-13.md`, reference-drift; outside `round-12-verifier-spotcheck.md` item 3 | `round-13.md:38`: “reference-drift … `summary.json` declaration.kind is null while declaration.json top-level kind is explicit … Add QUALITY14 … same checker rejecting the null-only companion and accepting the kind-only repair.” `round-12-verifier-spotcheck.md:146` item 3 names the null `declaration.kind` repair. | grounded |
| 15 | 61 | `lessons/round-14.md`, stale-expectation; outside `round-13-verifier-spotcheck.md` item 1 | `round-14.md:73`: “stale-expectation … QUALITY15; new disposition checker must fail the unresolved row for absent mechanism assertion and accept only its explicit supersession by checked oracle receipts. Raw historical expectation and observation remain unchanged.” `round-13-verifier-spotcheck.md:179` item 1 says “Do not erase the initial failure or call exit_matches alone mechanism proof.” | grounded |
| 16 | 68 | `lessons/round-14.md`, missing-setup; outside `round-13-verifier-spotcheck.md` item 2; S049 | `round-14.md:74`: “missing-setup … QUALITY16 and S049; prospective receipt records the actual bounded override beside argv/cwd and exact exclusions. Historical setup remains unproven.” `round-13-verifier-spotcheck.md:180` item 2; `SOURCES.md:58` S049 (tier A, status `mined`, opened `2026-10-20`). | grounded |
| 17 | 77 | `lessons/round-15.md`, gate-misclassification + exit-class-ambiguity; outside `round-14-verifier-spotcheck.md` item 5 | `round-15.md:50` “gate-misclassification … QUALITY17; … public --selftest must distinguish old unsupported invocation from new isolated exit/finding cases”; `:51` “exit-class-ambiguity … classify64 could-not-evaluate”; `round-14-verifier-spotcheck.md:160` item 5. Same-round third mined class `fixture-layout` (`round-15.md:151`) is not cited — see F4. | grounded, one same-round class uncited |

All nine cited lesson files exist (line counts): `round-1.md` 490, `round-12.md` 207,
`round-1-verifier-spotcheck.md` 17, `round-13.md` 146, `round-12-verifier-spotcheck.md` 160,
`round-14.md` 186, `round-13-verifier-spotcheck.md` 196, `round-15.md` 223,
`round-14-verifier-spotcheck.md` 173. No cited `## Mistakes` heading or numbered routed
item is missing or misnumbered.

## 2. Findings by severity

### F1 (moderate, not admission-blocking) — criteria 4 and 5 have no lesson behind them; 1–3 only have a captured-by link

`LEARNING.md:59`: “Thin at mint; **every criterion cites the lesson that produced it**.”
`LEARNING.md:35` (discernment): harmed when “a criterion is added with no lesson behind it”.

- C4 (`QUALITY.md:7`, errata append-only) has **zero** references anywhere in
  `corpus/lessons/`, `corpus/knowledge/` or `corpus/README.md`; C5 (`:8`, rejections kept)
  has one string occurrence, `round-1-verifier-spotcheck.md:17`'s “QUALITY 5→10 criteria”,
  which is a criterion-count, not a criterion-5 anchor (census in §5). They were minted
  with the file at round 0 (`git show 40f8e1f:corpus/QUALITY.md` prints the same heading
  and five criteria as lines 1–8; compared by eye, not `cmp`), predating the lesson rule.
- C1, C2, C3 appear only as **captured-by** in the round-1 `## Mistakes` table
  (`round-1.md:280` MK-1 → C2; `:289` MK-10 → C1/C3), not as produced-by.
- Mitigation already in the file: `QUALITY.md:13` says “Criteria 1–5 are unchanged”,
  so the omission is disclosed, not concealed.

Bounded recommendation: add one provenance line under the round-1 preamble (or in the
round-16 lesson) stating “C1–C5 are the round-0 mint bar, written before lesson mining;
MK-1/MK-10 record C1–C3 as capturing criteria; C4–C5 have no lesson anchor.” Do **not**
invent a lesson row for C4/C5 to close the gap — that would manufacture the very
discernment the rule protects.

### F2 (minor) — C12's citation covers only one of its three rules

C12 packs three distinct rules:
(a) frozen declaration prior-exposure/integrity → carried by the cited `round-12.md:51`;
(b) “Report all declared defects, unresolved denominators and accidental kills” → carried
by `round-12.md:176-178` (“ten declared defects: 8 killed-on-witness, 0 accidental,
2 survived, 0 inconclusive; 16 printed control slots = 14 exercised + 2 skipped”);
(c) “reanalyzing an existing artifact is not a new gate” → carried by the Gate reject at
`round-12.md:23` (“Reject ‘a bash witness reanalysis is a seventh independent gate.’ Same
artifact/spec remains the same leg.”).

The cited “attribution mistake” row does not contain (b) or (c), so the citation is
row-precise only for (a). Recommendation: append the two exact anchors to C12's parenthesis
or split (b)/(c) into their own rows. This is the same reference-drift class C14 codifies;
leaving it unmarked weakens C14's own standard.

### F3 (minor) — C11's finite-sample and counterexample clauses are body-only

C11 says a clean verdict “names its finite sample and compares raw exit/stdout/stderr
tuples; it never proves determinism”, and that the counterexample must “trigger the same
committed mismatch oracle after the repair”. Row `round-12.md:50` only says the fixture
must be “refused by the new gate”. The finite-sample/determinism-proof wording is at
`round-12.md:155-156` (“Three pristine bash controls matched on raw streams and zero exits;
this is finite agreement, not a determinism proof”); the same-oracle red/green evidence is
at `round-12.md:160-164` (“the oracle exits 1 (`controls_match`, wrong expected finding);
restoring the loop makes that same oracle exit 0 (`controls_mismatch`, correct finding)”).
Recommendation: cite `round-12.md:148-165` in addition to the row; no text change to the
criterion.

### F4 (minor) — C17 does not carry the same round's `fixture-layout` class although that row claims C17 captured it

`round-15.md:151` is a third mined class in the “Observed integration failure” table:
“fixture-layout … `<scratch>/candidate.py` … maintained tool's two-parent root therefore
becomes `/tmp` … **QUALITY17 isolated public-CLI rule** … Place the byte-identical old/new
candidates at the same `<scratch>/lane/tools/candidate.py`, preserving the actual maintained
tool's layout; retain first run…”. C17 (`QUALITY.md:77-83`) states public isolated
self-invocation, literal exits, stable finding IDs and helper-only disqualification, but
says nothing about preserving the real layout or retaining the first failed run.

Either C17 implicitly covers it (defensible reading of “isolated public-CLI”), or the
criterion is incomplete. Recommendation: do **not** rewrite C17 (`LEARNING.md:60-61`:
“Criteria are superseded by new rows that name the row they replace, never rewritten”).
If incomplete, append a new row after 18/19 that names C17 and adds the layout/first-run
clause; if implicit coverage is accepted, record that decision in the round-16 Gate.

### F5 — superseded-but-unmarked criteria: none found; the one status marker is ambiguous, not proven stale

- `grep -n "supersed" corpus/QUALITY.md` → **one hit, line 61**, inside C15's own text
  (“explicitly effective or superseded by named, checked replacement evidence”). No
  criterion names an earlier row as replaced.
- No later lesson names a QUALITY criterion as replaced (`grep -rniE
  "supersed[^|]{0,80}QUALITY|QUALITY ?[0-9]+[^|]{0,80}supersed|replaces? QUALITY"`
  over `corpus/`, `plans/`, `reports/` → no matches).
- Conclusion: **no criterion can be reported as superseded on evidence**. The
  `LEARNING.md:60-61` supersession mechanism has not been exercised in 17 criteria. If the
  round intends C1–C5's broad rules to be replaced by 6–17's specificity, that is an
  unmarked supersession and must name the rows; absent that, the additive reading stands.
- File-title qualifier: `QUALITY.md:1` “Admission bar (probation draft)” conflicts with
  `plans/round-4-record-draft.md:224` (“probation completed at round 3”) but is consistent
  with `SKILL.md:3` (“Rank: shonen (probation)”) and `SHONEN.md`'s all-`[~]` boxes. This is
  a status ambiguity for L1, not a proven stale marker, and not an admission blocker.

### F6 — where criteria 18 (misattribution) and 19 (misroot/landing) belong

**Primary placement: a new `## Criteria appended — round 16` section appended after
`QUALITY.md:84`, numbered 18 then 19, with C17 left byte-identical.** Rationale: every
post-11 round appends its own section (`QUALITY.md:32` round 12, `:48` round 13,
`:59` round 14, `:75` round 15); both are round-16 mined classes; `LEARNING.md:60-61`
forbids rewriting earlier rows. `grep -cE "^1[89]\. " corpus/QUALITY.md` → `0`, so the
numbers are free.

Draft (derived only from the routed defect and the artifact, not from any sibling draft):

```
## Criteria appended — round 16

18. A finding ID or verdict read from a tool's output is taken from the
    terminal structured verdict for the executed argv, never from the first
    `id=`/marker in help or usage text. Every checked row that claims an
    attribution asserts its expected ID; a null `expected_id` on such a row
    is not a pass. A repaired extractor is shown able to fail on the output
    that exposed the defect: the old misattribution is recorded red, the
    corrected finding green on the same fixture/argv, and a negative fixture
    with the terminal verdict removed must fail the check. The correction is
    appended beside the frozen receipt, never rewritten.
    (`lessons/round-16.md`, `## Mistakes`, attribution row (a); outside
    `lessons/round-15-verifier-spotcheck.md`, Routed defects item 2)

19. Every accepted seat output sits at its declared lane-root path. A bare-id
    write is a misroot even when its bytes are correct: retain the stray
    artifact under a named evidence path with its sha256 and class, do not
    overwrite an existing assigned report, re-deliver through the contracted
    `agent://<id>` channel, and have round closure list the tracked
    fleet-root misroots it found (read-only) with a nonzero exit on any.
    (`lessons/round-16.md`, `## Mistakes`, misroot row (b); evidence copy
    `.ufo/evidence/round-16/<artifact>` per C9; source
    `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/TameshiR15`,
    sha256 b413df98…7236469, 605 B)
```

Ownership boundary:
- **18 is lane-owned.** `round-15-verifier-spotcheck.md:160` routes the repair to
  “Tameshi: repair usage finding attribution in the integration verifier”, and the
  criterion extends C2/C8 (measured anchor; report lands in-repo) to finding-level
  attribution. It does not duplicate C17: C17 classifies the instrument, 18 governs how a
  finding is read from it.
- **19 splits.** The landing/retention half is lane-owned and extends C8/C9. The
  `agent://<id>` address grammar and stray-file behavior are harness/operator-owned — the
  lane cannot enforce how `write` routes a bare id. If L1 judges QUALITY to be
  knowledge-admission only, keep the landing/retention half as 19 and route the addressing
  clause to the fleet contract/PROTOCOL; either way, name the choice in the round-16 Gate.
- **Evidence mechanics (implementation-critical).** The misroot artifact is at the fleet
  root, not the lane: `ls -l` → 605 B, mtime `2026-10-20 05:06`; `sha256sum` →
  `b413df980b7781b8c4b904770e968391c2664c908e327d4231c4727f7f236469`; tracked in the fleet
  repo at commit `ac0a7fc`; `git status --porcelain` on its directory → empty.
  `cmp` against the lane's real
  `tameshi-shokunin/.ufo/waves/round-15/w1/Frontier.md` → `differ: char 1, line 1`,
  exit 1. The misroot is **not** a copy of that report, so criterion 19 must not demand a
  byte-identical copy onto the assigned path; copy it into lane `.ufo/evidence/round-16/`
  (C9) and disclose both hashes. The lane's round-15 lesson and spot-check contain no
  “misroot” mention (`grep -rni misroot` on both → no matches), so the incident is
  currently undisclosed in-repo; criterion 19 would be its first lane record.

## 3. Residual risk and verification gaps

- Historical quantities inside lesson rows (MK-7's “19/19” header census; MK-4's “9 rows /
  6 of 16”) were **not** re-measured at their base commit; only row existence and several
  concrete anchors were re-checked (MK-2 `mutation-case-kimi-census.md:185`, MK-3
  `mutation-case-kagi-census.md:186`, MK-4 `round-10.md:175-176`, MK-5's two absent
  reports, MK-6's absent `/tmp` path, S049).
- Citation checks are text-level. No language server answers Markdown here, so a renamed
  file that still matches the literal path would evade the check; the reverse (a valid file
  reported missing) cannot happen with `test -f`.
- This audit covers citation integrity only, not whether rounds comply with 1–17.
- I did not read `SCORECARD.md` or `LOG.md` in full; the probation-status comparison is
  limited to the cited lines.
- After my findings were formed, a wave-directory grep surfaced
  `.ufo/waves/round-16/w1/MistakeScribe.md` (another seat's 18/19 draft). It is **not**
  used as evidence here; my 18/19 draft is derived from
  `round-15-verifier-spotcheck.md:160` and the artifact itself. Disclosed for transparency.

## 4. Commands and exits (key)

- `git rev-parse HEAD` → `28aeef4…` (exit 0); `sha256sum corpus/QUALITY.md` → `534f42…`
  (exit 0).
- `for f in <9 cited lessons>; do test -f ...; wc -l; done` → all present (exit 0).
- `grep -n "^## Mistakes"` → `round-1.md:266`, `round-12.md:46`, `round-13.md:34`,
  `round-14.md:69`, `round-15.md:46` (exit 0).
- `grep -nE '^\| (vacuous|attribution|reference-drift|stale-expectation|missing-setup|gate-misclassification|exit-class-ambiguity) '` → `round-12.md:50-52`, `round-13.md:38,39,41`,
  `round-14.md:73-76`, `round-15.md:50-51` (exit 0).
- `grep -nE "^[0-9]+\. \*\*"` on the four spot-checks → r12:144-147, r13:179-183,
  r14:156-160, r15:159-163 (exit 0).
- `ls reports/r10-ver-t10.md reports/r11-ver-t11.md` → both `No such file or directory`
  (exit 2). `ls -d /tmp/tameshi-r3-4-work` → same (exit 2).
- `grep -n S049 corpus/SOURCES.md` → `:58` (exit 0).
- `grep -n "supersed" corpus/QUALITY.md` → only `:61` (exit 0).
- `grep -cE "^1[89]\. " corpus/QUALITY.md` → `0` (exit 1, expected no-match).
- Misroot: `sha256sum` → `b413df98…`; `cmp` → exit 1 (differ char 1); `git log --oneline`
  → `ac0a7fc`; `git status --porcelain` → empty; `grep -rni misroot
  corpus/lessons/round-15*.md` → no matches.

## 5. Criterion-link census (C1–C5)

`grep -rnoE "QUALITY(\.md)? ?[1-5]\b" corpus/lessons corpus/knowledge corpus/README.md`
(all exit 0) returns only:
`round-12.md:50` (range 1–3), `:51` (3), `:52` (2), `:174` (range 1–3);
`round-13.md:38,39,40,41,127` (2 or 2–3); `round-14.md:73-75` (2), `:76` (1–2);
`round-15.md:50` (2); `round-1-verifier-spotcheck.md:17` (`QUALITY 5→10 criteria`, a count);
plus the two round-1 captured-by rows `:280` (C2), `:289` (C1/C3).
No line references criterion 4; the only “QUALITY 5” string is the criterion-count at
`round-1-verifier-spotcheck.md:17`, not a criterion-5 anchor.

## 6. Opened

- `corpus/QUALITY.md` (full, numbered)
- `corpus/SOURCES.md` (lines 1–20, 58)
- `corpus/lessons/round-1.md` (266–290, 403; 280–286 raw)
- `corpus/lessons/round-1-verifier-spotcheck.md` (full, 17 lines)
- `corpus/lessons/round-10.md` (173–178)
- `corpus/lessons/round-12.md` (3, 20–25, 40–60, 96–116, 148–180)
- `corpus/lessons/round-12-verifier-spotcheck.md` (140–151)
- `corpus/lessons/round-13.md` (30–50, 120–140 via grep)
- `corpus/lessons/round-13-verifier-spotcheck.md` (175–187)
- `corpus/lessons/round-14.md` (65–92)
- `corpus/lessons/round-14-verifier-spotcheck.md` (154–164)
- `corpus/lessons/round-15.md` (42–62, 139–170)
- `corpus/lessons/round-15-verifier-spotcheck.md` (157–190)
- `corpus/knowledge/mutation-case-kimi-census.md` (183–188)
- `corpus/knowledge/mutation-case-kagi-census.md` (184–188)
- `corpus/knowledge/executor-test-sufficiency.md` (12–20)
- `LOG.md` (171–176, 366–392; grep for probation/promotion)
- `SHONEN.md` (1–20)
- `SKILL.md` (line 3 via grep only)
- `plans/round-4-record-draft.md` (line 224 via grep only)
- `.ufo/waves/round-16/w1/` directory listing; `MistakeScribe.md` (grep hits only,
  disclosed in §3)
- `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/TameshiR15` (read + hash + cmp)
- `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/` directory listing
- `LEARNING.md` at the fleet root (full)
- fleet git metadata for the misroot path (`git log`, `git status`; read-only)

No tool installs or updates. No write outside this report and no write outside the lane root.
