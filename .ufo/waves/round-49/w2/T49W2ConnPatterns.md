# T49W2ConnPatterns — cross-wave pattern finder (wave 1 → integration at `f181a961`)

Seat: T49W2ConnPatterns (connector, leaf, wave 2). Lane: `tameshi-shokunin`. Base `8ca67421…`,
integration candidate `f181a961ae44061af486f600e5ea257d2baf78f8` (= REV candidate), contract frozen
`14d03ea4270c6904064022b62b6faf467e5c0968` (read-only). I decide no claim; no counter was run in any
mode; all findings below are from reading wave-1 reports, the integration diff, and the integrated
artifacts. Tooling installed/upgraded: none (reads + `git show`/`grep`/`python3` json only; pacman
paused and untouched).

## Method (commands that show the evidence base)

- All 53 wave-1 reports + receipts under `.ufo/waves/round-49/w1/` read in full (every `T49*.md`,
  plus the `*.rows.json` / `*.findings.json` deliverables).
- `git -C … diff 8ca67421111fa354b47b803358391d0b07fc6db9 f181a961… --stat` → 461 files; content
  files: `SKILL.md` (92 lines touched), `tools/pbt-staged-id.py` (988, new), `corpus/knowledge/pbt-generator-pilot.md`,
  `corpus/lessons/round-49.md`, `corpus/{SOURCES,README,QUALITY}.md`, `LOG.md`, `SCORECARD.md`.
- `git show f181a96:SKILL.md` diff hunks vs base (all seven target sections, line-neutral).
- `python3` over `.ufo/evidence/round-49/c1/corrections.json` (44 corrections), `c1/reads.json`
  (94 rows), `round-21/coldread/ledger.json` tail (7 new entries), `coldread/refresh-receipts.json`.
- `sha256sum tools/pbt-staged-id.py` = `0cbee392…` = the `T49ExecGenerator` deliverable byte-exact.
- `wc -l` on base vs REV SKILL.md (both 2136 — no line drift; kengaku PROVINCE citations unmoved).
- `corpus/lessons/round-4{0..8}-verifier-spotcheck.md` for the recurring-class comparison.

## 1. The integration at a glance

- 44 corrections landed (`.ufo/evidence/round-49/c1/corrections.json`), every one carrying its
  raising seat; all line-neutral; lesson (`corpus/lessons/round-49.md` §"C1 — what the reading
  found") says "Forty-five" — see Finding P6 (count label off by one).
- reads.json: 94 rows (91 holds / 3 absent) = 90 base pointers re-keyed + 2 new pointers the
  SecRecipe fixes introduced (`tools/mutate-and-run.sh:425`, `:569-574`, rows keyed by the L1) +
  2 rows for the Read09/Read11 added pointers + the re-aimed ord 24.
- 7 new ledger entries (round-21 ledger 497 → 504), inputs exclude all five record files; the
  fabricated digest path (`context-missing-env.json`) is NOT among them (RevengerLapse's "must not
  copy it" honored).
- C2: generator byte-exact from `T49ExecGenerator`; pilot entry landed with placeholders filled,
  citing **S269/S270**; README F10 line landed; rows S269/S270 landed with the S183 anchor corrected
  to §2.10 p. 34.
- QUALITY criterion 99 = the T49ScribeMistake text (not T49ScribeConsider's — see Contradiction 2).

## 2. Master table — finding → raised by → integrated? → where

### 2a. C1 pointer reads (18 reader seats; base census 80 hold / 2 stale / 5 unresolved / 3 absent)

| Finding | Raised by | Integrated? | Where (show with) |
|---|---|---|---|
| ord 18 stale: `SELFTEST: FAIL (1/16 cases)` not in kagi note; real line is `1/16`/FAIL at :67; fix re-aims to `:67,82-103` | T49Read04 | **yes** | corrections.json `T49Read04`; SKILL.md:198-199 at REV |
| ord 2 stale: restore `cp -p` literal at kimi:172, not :4-7; pointer extended to `:4-7, :172` | T49Read08 | **yes** | corrections.json `T49Read08`; SKILL.md:382-384 |
| ord 7 `mutate_driver.py` absent-by-design + new `SCORECARD.md:16` record pointer | T49Read09 | **yes** | corrections.json `T49Read09`; SKILL.md:397-399 (10→11 pointers) |
| ords 0-1 unresolved bare `:1294-1297` / `:1246-1270` → prefixed `SKILL.md:` | T49Read10 | **yes** | corrections.json `T49Read10` ×2; SKILL.md:1384,1386 |
| ord 11 `plans/round-N.plan.md` absent + resolvable `plans/round-11.plan.md` instance | T49Read11 | **yes** | corrections.json `T49Read11`; SKILL.md:1393 (17→18 pointers) |
| ord 12 `plans/round-N-record-draft.md` absent + placeholder clarification | T49Read12 | **yes** | corrections.json `T49Read12`; SKILL.md:1393 |
| ord 4 `dispositions.json` → `.ufo/evidence/round-14/dispositions.json` | T49Read17 | **yes** | corrections.json `T49Read17`; SKILL.md:1585 |
| ord 6 `verification.json` → `.ufo/evidence/round-14/verification.json` | T49Read18 | **yes** | corrections.json `T49Read18`; SKILL.md:1588 |
| ord 7 `capture-context.py` → `.ufo/evidence/round-14/capture-context.py` | T49Read18 | **yes** | corrections.json `T49Read18`; SKILL.md:1593-1595 |
| ord 24 third range `:251-253`→`:252-254` (line 251 blank; paragraph is 252-254) | T49ScoutRecipeLines + T49Read05 (+ noted by T49SecRecipe) | **yes, once** | corrections.json `T49ScoutRecipeLines`; SKILL.md:221; reads.json row 26 carries merged attribution "T49Read05 (excerpt); range corrected by T49ScoutRecipeLines" |
| kagi `:251-253` identical finding (independent) | T49Read05 / T49SecRecipe | yes — see previous row | (same) |
| All other base pointers hold (incl. external `../PROTOCOL.md:63–68` at fleet HEAD) | T49Read01-03,05-07,13-16,18 | n/a (rows landed) | reads.json, one row per pointer, `reader` field set |
| `verdict` vs `base_verdict` reads-assembly hazard (14 rows would score not_holds) | T49Read07 (+T49Read10) | **yes** | handled by `c1/merge-reads.py:45-46` + L1 assembly; reads.json uses `verdict` |
| kimi-census:207 fused `## Errata` heading (file defect, outside seven sections) | T49Read01 | **no** | not a SKILL.md target; no seat owned the file |
| `service-limits.md:10-11` inner anchor cites `SKILL.md:1230-1249` (drifted; body is 1256-1267) | T49Read10 | **no** | out-of-scope file; not a C1 target |
| boundary/precision notes (ords 15/17 ranges; "print the count" implied; 300 s sweep-vs-per-run; LOG.md "rows" wording; SCORECARD "counting commands" wording; `--regression` live-number risk; S048 narrowing sits in the `###` block) | T49Read03,04,05,06,11,12,16 | no (recorded as notes) | each seat's `.md`; none proposed a counter-effecting edit |

### 2b. C1 section-critic findings (7 seats; 12 false / 6 unverifiable / 62 true total)

| Finding | Raised by | Integrated? | Where |
|---|---|---|---|
| `:142-144` false — two of six gates print `n/m cases passed` | T49SecRecipe | **yes** | corrections.json; SKILL.md:143 |
| `:224-225` false — step 9 drops two of step 2's seven cells | T49SecRecipe | **yes** | corrections.json; SKILL.md:224 |
| `:171-174` unverifiable — printed-count claim | T49SecRecipe | **yes** (count half dropped; maintained driver cited) | corrections.json; SKILL.md:171-173 |
| `:176-177` ambiguous "that particular round-2 guard" | T49SecRecipe | **yes** | corrections.json; SKILL.md:176-177 |
| `:210-211` unverifiable — inconclusive-denominator rule | T49SecRecipe | **yes** (labelled design choice; driver contrast cited) | corrections.json; SKILL.md:210-213 |
| 6 fused-token repairs (`exit0`, `bash16`, `denominators43 and16`, `Round2:7.0s for11`, `round3:11.0s…a280s`, `U5 at204-205`) | T49SecRecipe | **yes** (9 whitespace rows incl. Read04/08/09/ExecR14 overlaps) | corrections.json `whitespace`; SKILL.md:146,147,193,241-244 |
| `:396` false — "reran from scratch" vs retained-scratch re-runs | T49SecRestore | **yes** | corrections.json; SKILL.md:397-398 |
| `:377` "All edits must stay in scratch" overbroad | T49SecRestore | **yes** ("substrate edits") | corrections.json; SKILL.md:377 |
| `:383-384` "lane namespace" undefined | T49SecRestore | **yes** ("scratch outside the lane") | corrections.json; SKILL.md:382-384 |
| `:387/:389` fused hash/size/mtime strings | T49SecRestore (+T49Read08/09) | **yes** | corrections.json; SKILL.md:387-390 |
| map `:1393` "uncommitted at this write" stale; `:1385` ledger "one row per gate" false (9 gates, 8 rows); "the row is the standing receipt" false; `:1387` protocol "boundaries" + missing §3; `:1390` "reproduce sections" (3 of 9 none); `:1392` README "one row per note" (63/58, 1 uncarried); runbook six-case currency | T49SecMap | **yes — 6 corrections; but the *ledger append* (the seat's preferred repair for the two ledger cells) was NOT done** | corrections.json `T49SecMap`; SKILL.md:1384-1393; `fleet-kill-rate-ledger.md` still has no round-26 row |
| promotion `:1467` `#box-1` scope false | T49SecPromotion | **yes** | corrections.json; SKILL.md:1467 |
| promotion undated `[~]` since → `c7986cd`; undated "fresh" → (2026-10-15); erratum reconciliation sentence | T49SecPromotion | **yes** (3 rows) | corrections.json; SKILL.md:1472,1474,1476 |
| promotion "historical training closeout" unverifiable | T49SecPromotion | **no — withdrawn by the seat** | seat: both repairs cost a pointer/line shift; L1's call |
| r12 `:1483` "six-leg runner" stale (nine legs) | T49SecR12 (+T49Read14 F3) | **yes** ("…of round 12") | corrections.json; SKILL.md:1483 |
| r12 `:1488` mixed-availability precedence (`command_unavailable` wins) | T49SecR12 + T49ExecR12Cmd (two independent probes, N=3 and N=4) | **yes** (joint credit) | corrections.json `T49SecR12+T49ExecR12Cmd`; SKILL.md:1488 |
| r12 `:1489` "Could not evaluate baseline" names no printed id | T49ExecR12Cmd | **yes** (`baseline_nonzero`/`command_unavailable`, exit 2) | corrections.json; SKILL.md:1489 |
| r12 `:1487` bound drops "on this host in this environment" | T49ExecR12Cmd | **yes** | corrections.json; SKILL.md:1487 |
| r13 `:1530` frozen-summary kind misattribution | T49SecR13 | **yes** | corrections.json; SKILL.md:1530 |
| r13 `:1534` "source-backed scope" names nothing | T49SecR13 | **yes** | corrections.json; SKILL.md:1534 |
| r14 cause parenthetical names the runner; base error names `bash-witness-study.py` (3 pins differ) | T49ExecR14Cmd (severity "mismatch"; T49SecR14 called the same fact a "precision note") | **yes** (cause clause rewritten) | corrections.json `T49ExecR14Cmd`; SKILL.md:1581-1582 |
| r14 `initial18-of34` fused | T49ExecR14Cmd + T49Read18 | **yes** | corrections.json; SKILL.md:1589 |
| promotion structural flag: evidence is a mutable non-record audit; the 5-file durability probe cannot cover its lapse class | T49SecPromotion | **no** (flag for L1; predicate unchanged) | seat report §Headline |
| recipe "round 16 executed it end to end" counterexample | T49SecRecipe | n/a — attacked and survived (40 true) | seat report |

### 2c. Out-of-range true-but-stale sentences (both explicitly deferred by the L1)

| Finding | Raised by | Integrated? | Where |
|---|---|---|---|
| `SKILL.md:1508-1509` "never a seventh independently measured gate" (seven exist) | T49SecR12 (OUT OF RANGE) | **no — deferred** | `corpus/lessons/round-49.md` §C1 names it: "Not applied: two true-but-stale sentences outside the seven sections (SKILL.md:1509, 1555)… routed" |
| `SKILL.md:1555` "six recorded cases" (nine at base) | T49SecR13 (F2, adjacent `###` block) | **no — deferred** | same lesson sentence |
| r12 S026 → S265 re-anchor (S265 supersedes S026's anchor/quote) | T49SecR12 + T49Read14 F1 | **no** | SKILL.md:1481 still `S004/S026`; S026 still resolves and is `mined` — currency swap left undone |
| `SKILL.md:1503` `/tmp/tameshi-r12-*` registry glob overlaps the recipe example path | T49ExecR12Cmd M3 | **no** | registry block is outside the C1 target sections |
| cited note's own stale pins (`repeated-control-precondition.md:35,58`) | T49ExecR12Cmd cross-ref + T49Read14 F2 | **no** | the note is not one of the seven targets |
| r13 registry advisories (`:1552` pinned 18/18 vs live 19/19; round-13 measure IndexError; S048-pointer cost) | T49SecR13, T49ExecR13Cmd M2/M3 | **no** | advisories; `expected.json` left as historical receipt |

### 2d. C2 build, sources, records

| Finding | Raised by | Integrated? | Where |
|---|---|---|---|
| `tools/pbt-staged-id.py` (988 lines, sha `0cbee392…`) | T49ExecGenerator | **yes — byte-exact** | `sha256sum tools/pbt-staged-id.py` = w1 deliverable |
| pilot entry draft with placeholders | T49ScribeEntryDraft | **yes** — `@CLASSES@/@KILLS/@FIXKILLS@/S_QC/S_SB` all resolved; cites S269/S270 | `corpus/knowledge/pbt-generator-pilot.md:1-2`; zero placeholder hits (`grep -n '@CLASSES@\\|S_QC'` empty) |
| S269/S270 row texts (11 cells, pipe-free recheck, `mined`, `2026-10-26`) | T49ScribeRows | **yes — verbatim** | `corpus/SOURCES.md:142-143` |
| id proposal S269/S270 | T49ScoutSrcHypothesis + T49ScribeRows | **yes** | lesson §Assimilation; SOURCES notes |
| id proposal S271/S272 (S156→S269, S157→S270, S182→S271, S183→S272, whole-package map) | T49ExecIdGuard | **no — overridden** (see Contradiction 1); its consequences: "next unused id S265" fixed (`SOURCES.md:493`), reserved-block note amended, quarantine findings recorded in lesson §Gate |
| S183 staged anchor "§4.1 p. 44" false → §2.10 p. 34; presence-only check blind | T49ExecSrcSmallbone + T49ScribeRows + T49ScribeEntryDraft (+ T49ScribePkgQuickCheckCorr F3) | **yes** | S270 anchor cell; lesson §Gate "with its anchor corrected" |
| S182 staged location understates F10 material (§2.4/§3.2/§5.1.4/§6.3); DOI route 403, mirror carrier | T49ExecSrcQuickCheck + T49ScribePkgQuickCheckCorr | **yes** | S269 anchor names §Abstract/§2.4/§3.2/§5.1.4; lesson §Gate carrier caveat |
| guard docstring exit-1 vs observed exit-1-for-refused-analysis | T49ExecGenerator F1 + T49RevGuardExit (confirmed) + T49ScribeEntryDraft F3 | **routed, not edited** (pinned guard) | contract `guard_exit_semantics_observed`; lesson "Found this round" item 5 |
| README F10 `open` → `held (round 49)` + knowledge-table row | T49ScribeEntryDraft §6 suggestion + contract | **yes** | `corpus/README.md:593-599` (status conditioned on the deciding receipt) |
| SCORECARD C2 controls cell repeats "the guard's own 14 selftest fixtures" | contract wording; T49ScribeEntryDraft F8 measured 24 assertions/5 fixture tables | **contract wording kept** (legitimate quote; the measured fact stays in w1) | SCORECARD round-49 C2 row |
| assimilation triage: admit S182/S183, reject `r4-quickcheck-primary-correction.md`, reject `pbt-generator-craft-author.md` | T49ScribePkgQuickCheckCorr, T49ScribePkgCraftAuthor (+T49ScribePkgAsFixture) | **yes — as lesson Gate decisions** | `corpus/lessons/round-49.md` §Assimilation (2 admits, 2 rejects with decisive criteria, 1 deferral with flip) |
| `pbt-generator-as-fixture.md` narrow admit + 2 more rows (JOSS S271, Zenn S272) | T49ScribePkgAsFixture | **no — deferred by L1** | lesson §Assimilation "Deferred — … Flip: a round that opens and appends those two rows and lands the nine edits" |
| staged rows are 13/14 cells, not 11 | T49ScribeEntryDraft F2 | **yes** (rewritten, not copied) | S269/S270 pass `measure.py:285` shape |
| QuickCheck copy OCR damage kept verbatim; quotes de-spaced and re-located | T49ScribeEntryDraft F6 | **yes** | entry quotes + `T49ScribeEntryDraft.quote-check.txt` |
| generator cites by symbol not line (file was moving in-wave) | T49ScribeEntryDraft F4 | **yes** | entry cites symbols |
| class floors measure the round-robin schedule; map cases unscored by the counter's oracle leg | T49ScribeEntryDraft F7 | **routed** | lesson "Found this round" item 1 ("F3; the round's dump has 393 distinct cases of 400") |

### 2e. Counter/deciding-script critiques (frozen artifacts — integration = routing only)

| Finding | Raised by | Integrated? | Where |
|---|---|---|---|
| C2 counter cannot tell PBT from differential (pristine guard sits in the generator's cwd during mutant runs; a no-oracle diff generator is `confirmed`) | T49CritC2Contract F1-F2 (probe receipts) | **routed, counter unchanged** | lesson item 1; wave-2 access-trace assigned |
| class floors count dump lines, not distinct cases/run-bound cases | T49CritC2Contract F3 | **routed** | lesson item 1 |
| `oracle_disagree` checks the guard, not the generator; skips map cases; tolerates exit-1 | T49CritC2Contract F4 | **not in lesson** (routed nowhere visible) | w1 report only |
| `--generator-path` substitution invisible; gate 0 checks existence not verdict; records leg lexical | T49CritC2Contract F5-F7 | **not in lesson** | w1 report only |
| no sandbox; hidden panel reachable from the lane at REV | T49CritC2Contract F2 | **routed** (inside item 1) | lesson |
| C1 `absent` uncapped → cheaper-than-CTL_K ghost control reaches `total=0` (CTL_G demonstrated); `absent` already covers 3 existing files; durability probe is a 5-file sample; extractor census misses 21 forms; absent rows carry no evidence; empty trace inputs pass | T49CritC1Contract F1-F10 (probe receipts) | **no — and NOT in the lesson's routed list** (largest un-integrated block; all fixes need a contract amendment; `amendments: []`) | w1 report + `ghost_ctl.py`/`k2_record.py` receipts |
| C1 selftest never calls `measure()` — 14/28 mutants survive, incl. dropping `not_holds` from `total` (false PASS) | T49MutC1Counter | **routed** | lesson item 2 |
| C2 selftest survivors (9/15; sort-lex, comparable-staged-sha are real tested-code gaps) | T49MutC2Counter | **not in lesson** | w1 report only |
| deciding-run.sh executes working-tree code; panel-reveal failure burns the single run; pre-counter failures accumulate rc; gate 0 laxness (freeze-commit reflexivity, no REV-descent check, content never checked, OUTDIR-keyed one-invocation); FROZEN omits 5 executed paths; usage/scratch/exit-receipt nits | T49RevDeciding F1-F11 | **F1/F2 routed** in lesson item 3 ("taken only on a clean tree… panel sha checked"); F3-F11 fixes **not integrated** (frozen script) | w1 report; lesson |
| gate 0 able-to-fail: 3 refusal shapes exercised | T49ExecMistakeGate (+T49ScribeMistake d6) | **yes** (receipts integrated; criterion 99's falsifier cites them) | `w1/T49ExecMistakeGate/`; QUALITY criterion 99 |
| gate-strength limits (commits not scoring; reflexivity; per-OUTDIR; counters gate-free) | T49ExecMistakeGate | **no** (recorded limits) | w1 report §"Gate-strength findings" |
| lapse archaeology: 36 pairs, record-file drift recurs 31-38/48 rounds; re-key must bind non-record inputs; 94-entry survival table | T49RevengerLapse | **yes — drove the design** | lesson §C1; refresh.py reads records via blobs; new ledger inputs verified record-free |
| one ledger entry records a fabricated digest (`context-missing-env.json`) | T49RevengerLapse | **not copied into the new entries** (verified) | new ledger tail (7 entries, inputs enumerated); old entry "left as written" per lesson |

### 2f. Records, criteria, cross-claim

| Finding | Raised by | Integrated? | Where |
|---|---|---|---|
| 3 `## Mistakes` rows (landing/scope/reference-drift) | T49ScribeMistake | **yes** | `corpus/lessons/round-49.md` §Mistakes |
| Criterion 99 (control scored+committed before deciding; script refuses) | T49ScribeMistake | **yes** | `corpus/QUALITY.md:1443-1461` |
| Criterion 99 (a tally is evidence only as a committed receipt; recurrent class closed by a check) + Q88 self-reference amendment + falsifier | T49ScribeConsider | **no — deferred** | lesson §considerthese: "a recurrence criterion is left for a round that can give it a falsifier over all nine spot-checks"; the 44-defect/26-class analysis IS integrated there |
| recurrence tracker grounding (proposal 3 mined) | T49ScribeConsider | **yes** | lesson §considerthese |
| QUALITY criterion proposal "witness-bound measured claims" | T49ConnCrossClaim | **no** | w1 report only |
| C1↔C2 separability + README-F10/SID-collision interference checks (clean) | T49ConnCrossClaim | n/a (verified clean; risks R1-R4 recorded) | w1 report |
| sibling patterns P1-P4 (blob-read re-key, stale-audit scan-set, re-derive-at-close, avoid pinned in-text forms) | T49ConnSiblingColdread | **honored** (re-key via blobs; no pinned-form corrections landed) | process-level; the `--list` probe receipt stands |
| kengaku PROVINCE.md:318-319 cites tameshi SKILL.md:1929/1975 — impending drift on line-count change | T49ConnSiblingColdread | **not triggered** — all 44 corrections line-neutral; SKILL.md stays 2136 lines | `wc -l` base vs REV |
| no sibling PBT ground; F10 uncontested | T49ConnSiblingPBT | n/a (confirms the move) | w1 report |
| no-harm coldread floor `credited>=57` vs contract sentence "must still credit 64/64" | T49ScribeMistake F4 | **no** (frozen harness; "the L1 owns whether 57 is the intended floor") | w1 report |
| no currently-credited section lapses on a one-line record append (0 exposure at base) | T49ScoutVolatile | **yes — design constraint** | new ledger entries exclude all five record files (verified) |
| round-48 SCORECARD "pasted byte-exact" false for 3 axis rows (ok=19 mismatch=3) | T49ScribeMistake row 3 | **yes** | SCORECARD.md:2382-2384 appended correction |
| r48 routed fixes: precheck on candidate, start/exit receipts, receipt dirs out of FROZEN | round-48 spotcheck → T49RevDeciding verification | **yes** | deciding-run.sh at freeze; lesson Mistakes row 1-2 |

## 3. Contradictions between seats (stated, not smoothed)

1. **Row-id assignment for the two F10 rows.** T49ExecIdGuard recommended staged S182→**S271**,
   S183→**S272** (package row order: S156→S269, S157→S270; guard-admitted mapB), consequence "the
   pilot entry must cite S271/S272". T49ScoutSrcHypothesis §3 and T49ScribeRows chose **S269/S270**
   (registry tail order). T49ScribePkgAsFixture wanted **S271/S272** for different documents (JOSS,
   Zenn). The L1 integrated **S269=QuickCheck, S270=Smallbone** and grounded it in the lesson
   ("two non-colliding rows need no map; the guard's whole-package map rule applies only to adopting
   colliding rows") — a defensible scoping decision (2 rows, not the 4-row map ExecIdGuard premised),
   but ExecIdGuard's stated consequence 1 ("the pilot cites S271/S272… correct only if the map above
   is the one adopted") is left standing against the integrated artifact, and its package-order rule
   ("fresh ids issued in the package's own row order, lines 10, 11, 36, 37") is silently overridden.
2. **Two different "criterion 99"s.** T49ScribeConsider proposed 99 = "a tally is evidence only as a
   committed receipt; a recurrent class is closed by a check" (+ Q88 amendment). T49ScribeMistake
   proposed 99 = "a control is scored and committed before the deciding run it discriminates". The
   number collided; the L1 integrated **ScribeMistake's** text (QUALITY.md:1443) and deferred
   ScribeConsider's ("left for a round that can give it a falsifier over all nine spot-checks").
3. **Same sentence, different verdicts.** T49Read01 graded pointer ord 2 (`gates-survey-kumitate.md:19-31`)
   **holds** ("the `n/m pass` + `VERDICT:` form line 143 requires"); T49SecRecipe graded the SKILL.md
   sentence at :142-144 **false** (two of six rows print `n/m cases passed`). Both are right at their
   layer: the pointer resolves and its target is the right table; the sentence's generalization was
   wrong. The L1 kept the read row and applied the text fix — consistent handling, but a wave-2
   re-read seat should not read the pair as a seat error.
4. **Same fact, different severity.** SKILL.md:1581-1582's cause parenthetical: T49SecR14 filed it as
   "precision note, not a falsehood" (no edit); T49ExecR14Cmd filed it as **M1** ("the parenthetical
   cause is narrower than the observed error", fix shape named). Integrated as correction #39 in
   ExecR14Cmd's shape. T49SecR14's milder framing is not represented in corrections.json.
5. **Fleet tip for `../PROTOCOL.md:63–68`.** T49Read13 read fleet HEAD `d1e70ce6`; T49CritC1Contract F7
   cited tip `94ab3129` ("has moved this round-adjacent"). Same lines, same content, different
   observation commits — no material conflict, but the external pointer's `fleet_commit` row in
   reads.json pins one of them; the contract's F7 fix (pin `fleet_commit` to the freeze-recorded fleet
   commit) was not taken.
6. **Double-raised fix and the lesson's count.** The `:252-254` repair was raised independently by
   T49ScoutRecipeLines, T49Read05, and noted by T49SecRecipe; integrated once (scout credited;
   reads.json row 26 merged). The lesson then says "Forty-five corrections landed" where
   corrections.json carries **44** (lesson: "…8 precision edits"; the file has 7 — see P6).

## 4. Recurring defect classes (vs `corpus/lessons/round-4*-verifier-spotcheck.md`)

T49ScribeConsider's mine of the nine closures (rounds 40-48) is the taxonomy: 44 defects, 26 classes,
10 recurring (24 rows); measured-rule criteria (Q87 label-count, Q91 quote-fold) show 0 recurrences;
filing-rule criteria kept failing. Round-49 wave-1 maps onto it as follows:

| Class (rounds 40-48 history) | Round-49 instance | How this round closed it |
|---|---|---|
| pointer-unresolvable (40,41,48 — recurred under Q72/81/97) | 2 stale + 5 unresolved + 3 absent at base | **closed by check**: frozen extractor + reads.json rows; 10 pointer repairs landed pre-REV |
| record-drift (40,47,48) | the C1 lapse itself (88/94 entries record-bound, median survival 1 round) | **closed by design**: re-key binds non-record inputs only; records read via git blobs |
| coldread-credit-loss (48) | routed defect 1 | C1 itself |
| order-of-scoring / receipt-not-committed (48; 45→46→47 recurrence, no criterion) | gate 0 + criterion 99 (ScribeMistake) | **closed by gate**: freeze-commit receipts, three refusal shapes exercised |
| monitor-false-red (45,48) | FROZEN_UNCHANGED red / receipt dirs in frozen list | fixed in round-49 deciding script; RevDeciding verified |
| reference-drift (48 defect 5) | SCORECARD "pasted byte-exact" | appended correction + verbatim checker (ok=19 mismatch=3) |
| id-collision (41,42) | staged S153-S160 vs held rows | **closed by tool** (round-43 guard; lesson §Gate re-verifies) |
| label-count (40,44) | quote-word counts in rows/entry | held this round (all counts measured with the lane fold); **but see P6** |
| quote-fold (46) | Smallbone hyphenation, QuickCheck ligatures | held (de-hyphenation/de-spacing receipts; damage declared, not repaired) |
| wave-shape (45,47) | r47's 32-seat wave never dispatched | w1 dispatched 40+ seats, all landed |
| instrument-defect / instrument-limit (41,42) | CritC1/CritC2/MutC1/MutC2 counter critiques | **behaves like the failing class**: routed by note, no check can fail — the frozen counter + empty `amendments` make it structurally note-closed; lesson routes 5 out of 9 finding-groups |
| attribution-salvage (48) | — | none this round (single attempt so far) |

**New micro-class this round (not in the 40-48 taxonomy): fused-token rendering damage** —
`denominators43 and16`, `exit0`, `bash16`, `Round2:7.0s for11 runs, nodev24.21.0`,
`initial18-of34`, `hash83016d45…4f426,43273B`, `unchanged09:47:15` — flagged independently by ≥6 seats
(T49SecRecipe page-level note, T49Read04 F3, T49Read08 F2, T49Read09 F1, T49ExecR14Cmd M2,
T49Read18 F3), root-caused to the `8eaae28` round-21 rewrite. 9 whitespace repairs landed; the
class deserves a tracker row (it will recur wherever that rewrite touched).

## 5. Second-order checks I ran (with commands)

- `python3 -c` over corrections.json → category histogram: 12 false / 9 whitespace / 6 unverifiable /
  3 unresolved-bare-file / 2 stale / 2 unresolved-bare-pointer / 2 absent-pattern / 2 undated / 1
  each (absent-path, currency, reconcile, decision-cell, bound, narrow-cause) = **44**, vs the
  lesson's "45 … 8 precision edits" (7 in file). **P6: the integrated lesson's own count label is
  off by one — the exact class Q87 guards.**
- reads.json row tally by `reader`: all 18 readers present (T49Read11:7, T49Read09/10:6, 12 seats:5,
  T49Read06/07/16:4) + 2 L1 rows for the SecRecipe-introduced pointers + 1 merged row = 94; verdicts
  91 holds / 3 absent; the 3 absent rows are the Read09/11/12 pattern pointers — matches the lesson's
  "80 hold, 2 stale, 5 unresolved, 3 absent **at base**" (the 2 stale and 5 unresolved became holds
  only via the corrected text + re-keyed raws, as designed).
- New ledger entries (ledger.json 497→504): one per section, inputs record-free; `context-missing-env.json`
  absent from all seven (fabricated digest not re-keyed).
- `git show f181a96:SKILL.md | wc -l` = 2136 = base → all corrections line-neutral; the two bare-map
  pointer qualifications and the two new record pointers change pointer counts (map 17→18, restore
  10→11, recipe 34→36) — each gained its read row.
- `grep -n '@CLASSES@\\|@KILLS@\\|@FIXKILLS@\\|S_QC\\|S_SB' corpus/knowledge/pbt-generator-pilot.md`
  → empty; entry cites S269/S270.
- `grep -c 'F10.*held (round 49)'`-style check on README:599 status line present, conditioned on the
  deciding receipt printing `C2_R49_PASS=true`; the frontier table row at README:87 stays `open`
  (append-only) — consistent with CritC2Contract's C2-F7 note.
- Not re-run: any counter, any control, any probe — this seat reads patterns only.

## Risks / limits of this report

- "Integrated?" is judged from the diff and the integrated files at `f181a961`; a finding marked "no"
  may still be deliberately routed (the lesson's "Found this round… routed, not claimed as fixed" list)
  — I have marked which is which, and the un-routed residue (CritC1Contract F1-F10, CritC2Contract
  F4-F7, MutC2Counter, ConnCrossClaim's criterion, ScribeMistake F4) is the wave-2/closure exposure.
- Correction indices in corrections.json are cited by `source_seat` + `why`, not positional numbers,
  because the file has no stable ids.
- I did not open the three forbidden C2 control stdouts or anything under `~/.local/state/`.

## Summary

- 44/45 wave-1 C1 corrections landed (corrections.json, every one seat-attributed, all line-neutral); the 2 stale + 5 unresolved + 3 absent base pointers were all repaired or legitimately absented; reads.json 94 rows cover every REV pointer incl. the 4 new ones.
- Explicit deferrals: SKILL.md:1509/1555 (would lapse a credited section), r12 S026→S265 re-anchor, ExecR12Cmd M3, the ledger-append half of SecMap's repair (cell fallback landed instead; the ledger still lacks its round-26 row).
- Largest un-integrated block: the frozen-counter critiques (CritC1Contract F1-F10 entirely absent from the lesson's routed list; CritC2Contract F4-F7 and MutC2Counter also unrouted) — note-closed by structure, matching the tracker class that kept recurring in rounds 40-48.
- Seat contradictions, stated not smoothed: S269/S270 vs S271/S272 id assignment (ExecIdGuard overridden, its consequence 1 left standing); two different "criterion 99"s (ScribeMistake integrated, ScribeConsider deferred); Read01-holds vs SecRecipe-false on the same sentence (layer difference, both kept); SecR14 "precision note" vs ExecR14Cmd "M1" (integrated in the harsher shape).
- Recurring-class ledger: pointer-unresolvable, record-drift, order-of-scoring, reference-drift, monitor-false-red all closed by check/design this round; id-collision stayed tool-closed; label-count/quote-fold held — except the lesson's own "45 corrections" count vs the 44-row file (off-by-one, the Q87 class in the integrated artifact itself).
- New micro-class for the tracker: fused-token rendering damage from the 8eaae28 rewrite (≥6 seats, 9 repairs landed).
- Verified second-order: generator byte-exact (0cbee392), new ledger entries record-free and fabricated-digest-free, SKILL.md line counts unchanged (kengaku drift warning not triggered), pilot entry placeholder-free citing S269/S270.
- No counters run, no claim decided; deciding runs remain the L1's.
