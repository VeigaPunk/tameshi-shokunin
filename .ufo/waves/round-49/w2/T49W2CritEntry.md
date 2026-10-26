# T49W2CritEntry — attack on `corpus/knowledge/pbt-generator-pilot.md` at `f181a961ae44061af486f600e5ea257d2baf78f8`

Seat: T49W2CritEntry (wave-2 critic, coverage). Milestone: pilot entry attack.
Attacked: `corpus/knowledge/pbt-generator-pilot.md` at `f181a961ae44061af486f600e5ea257d2baf78f8` (candidate content revision; not authored by this seat).
Method: every quoted passage re-located in the pinned snapshots (extracted from the candidate rev into `/fast/scratch/hyaku/tameshi-r49/T49W2CritEntry/pdf/`, now deleted); every measured number traced to a committed receipt or to the frozen counter/generator code at the candidate bytes. Probes are observations, never verdicts (the deciding run is the L1's). Forbidden files (`control/c2-WITNESS.stdout`, `c2-CTL_FIX.stdout`, `c2-CTL_ABSENT.stdout`) were not opened; from `control/c2-controls.stdout` (the file the entry itself cites, not on the forbidden list) only the three `CTL_`/`WITNESS` summary lines were read, no MUTANT detail lines.

## 1. Source sentences — every QuickCheck/Smallbone sentence matches a located passage

Commands (per quote): `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961:.ufo/waves/round-49/w1/T49ScribeRows.src/<pdf> > scratch/<pdf>; pdftotext scratch/<pdf> -` then substring search after whitespace folding. Snapshot digests recomputed: `quick.pdf` sha256 `bfddcaa648f836e5…` and `smallbone.pdf` sha256 `eaee48f930ba20a0…` — both match the entry's `source:` header and the rows `corpus/SOURCES.md:144-145`.

| Entry quote | Claimed anchor | Observed |
|---|---|---|
| "Properties are described as Haskell functions, and can be automatically tested on random input" | S269 Abstract (p. 268) | verbatim, PDF p.1 = printed 268 ✓ |
| "QuickCheck provides support for the programmer to define his or her own test data generators, with control over the distribution of test data" | S269 §2.4 (p. 270) | verbatim (the PDF's fi-ligature; pdftotext prints "de ne"), `quick.txt:291-294`, inside §2.4 (heading :227, §2.5 :295), PDF p.3 = printed 270 ✓ |
| "The combinator collect … print out a histogram of these values." | S269 §2.4 (p. 270) | verbatim, `quick.txt:248`, inside §2.4, PDF p.3 ✓ |
| "the false sense of security that can be engendered when one's program passes a large number of tests in trivial cases" | S269 §5.1.4 (p. 274) | verbatim, `quick.txt:717`, 4 lines under heading "5.1.4 A False Sense of Security" (:713), PDF p.7 = printed 274 ✓ |
| sized "generates an a by passing the current size bound to its parameter" | S269 §3.2 (p. 271) | verbatim, `quick.txt:454` region, inside §3.2 (heading :380, §3.3 :487), PDF p.4 = printed 271 ✓ |
| "It is then up to the programmer to interpret the size bound…" | S269 §3.2 (p. 271) | verbatim, `quick.txt:454`, same page/section ✓ |
| "the quality of the test data determines the quality of the generated equations" | S270 §2.10, printed p. 34 | verbatim, PDF p.39, printed page number "34" present, heading "2.10 Generating Test Data" on that page ✓ |
| "it is important to provide good test data generators, that fit the program at hand" | S270 §2.10, printed p. 34 | verbatim, PDF p.39 ✓ (recheck grep count = 1, observed) |
| "creating custom generators is sometimes necessary to get correct results" | S270 §2.10, printed p. 34 | verbatim, PDF p.39 ✓ |

All four bolded summary sentences (property vs generator artefact; distribution observed not assumed; size as the tester's knob; generator must fit the program) are supported by the quotes beneath them. Nothing about QuickCheck/Smallbone is fabricated. `quick.pdf` carries no printed page numbers in its extracted text, so p. 268/270/271/274 rest on the Crossref "journal pp. 268-279" mapping (PDF page N → 267+N); every section lands on the claimed page under that mapping, and the scribe receipts `quick-p1-abstract.txt` / `quick-p3-2.4-monitoring.txt` use the same mapping.

## 2. Measured numbers — pending vs asserted, correct

- Deciding-run values: the entry states "Measured values live in the deciding receipt `.ufo/evidence/round-49/after/c2.stdout`, never in this text" — no panel kill count, no class counts, no violations figure is asserted anywhere in the entry. The path is absent at the candidate (`git cat-file -e f181a961:.ufo/evidence/round-49/after/c2.stdout` fails; the `after/` tree is empty) — pending by design (criterion 86 order; `corpus/README.md:599` carries the same conditioned reference). It must resolve at the landing tip.
- Control numbers, asserted with citation, match the committed receipt: "confirms 6 of the 12" ← `git show f181a961:.ufo/evidence/round-49/control/c2-controls.stdout` line 2 `CTL_FIX … confirmed=6 … panel=12`; "a hand-made witness set confirms all 12" ← line 3 `WITNESS … witness_confirmed=12`. Both are pre-deciding control receipts scored at freeze bytes — correct to assert, not pending.
- Requirement numbers are the frozen counter's, not measurements: `SEED, CASES = 4949, 400`, `CLASS_MIN = 10`, `KILL_TARGET = 11`, `PANEL_SHA = d6dd2cf3…` at `.ufo/evidence/round-49/c2/measure.py:47-51` — the entry's "at least 10 cases each at seed 4949, 400 cases" restates the counter's constants exactly.

## 3. Overclaim — none found; the three named risks are all bounded in the entry

- F10 'held': the entry never says held. "What this does not establish" bounds it to "F10's 'one generator against a named fixture gate' move, not a method shown across the fleet's gates." The conditioned `held (round 49)` wording lives in `corpus/README.md:599`, void-tied to `C2_R49_PASS=true` — not in this entry.
- No shrinking: disclaimed ("a counterexample is the first failing case, not a minimal one"); `grep -c shrink` on `tools/pbt-staged-id.py` at the candidate = 0 — consistent.
- Panel size 12: disclaimed ("Twelve mutants are a small panel; a kill count is a measurement of this panel, not a mutation score of the guard").
- The counter-blindness disclosure (differential generator indistinguishable) cites wave-1 critic F1 and is a fair paraphrase: `.ufo/waves/round-49/w1/T49CritC2Contract.md:33-76` ("a generator with no property and no oracle passes every leg"; differential against a reachable pristine reference). The entry's promised wave-2 evidence ("an access trace and oracle-mutation results in the round-49 wave-2 reports") is a forward reference in words, allowed as pending; this seat's source inspection supports it — `grep -n 'getcwd\|__file__\|staged-id-guard\|git\|os\.environ' tools/pbt-staged-id.py` at the candidate matches only the docstring's title line (line 2), no reachable-reference read.

## 4. Defects (all minor; none voids the entry, each is falsifiable as stated and fails against the code)

- **D1 — "ids of 3-5 digits" is false at the top end.** Entry, "What the lane built". The `id_4_plus_digits` recipe draws `digits = rnd.randint(4, 6)` and builds `'S%d' % number` (`tools/pbt-staged-id.py:472-475` at the candidate); every other id is `'S%03d'`. Probe over 500 seeds × 13 recipes: id digit widths seen `{3, 4, 5, 6}`. Six-digit ids occur; five is not the maximum. Smallest correction: "ids of 3 or 4-6 digits" (or "up to six digits") via an appended dated erratum (criterion 35 — the original bytes stay).
- **D2 — "(0-8 rows)" is false at the low end.** Same paragraph. Measured over 6500 recipe draws: combined data rows per case = 2..8 (per table 1..4, after excluding the 2-line HEAD at `tools/pbt-staged-id.py:70-72`). Zero-row tables never occur; every recipe plants at least one structural row per table. Smallest correction: "2-8 rows" via the same erratum.
- **D3 — `source:` header cites two anchors the S269 row does not declare.** The entry's S269 line advertises §3.2 (p. 271) and §5.1.4 (p. 274); row S269's anchor column (`corpus/SOURCES.md:144`, col 5) declares only "Abstract, first paragraph (p. 268) and §2.4 Monitoring Test Data (p. 270)". The lane's precedent binds an entry's cited anchors to its row's declared anchors: S006's row anchors == `witness-scoped-kill-verdict.md`'s source line, S097's == `witness-equivalence-rule.md`'s (`corpus/SOURCES.md:17,106`). Both overrun quotes are genuine (verified in the pinned snapshot, §1), so this is a registry-shape defect under criterion 10's "enters through a SOURCES.md row", not fabrication. Smallest correction: an append-only SOURCES erratum extending S269's anchor to §3.2 (p. 271) and §5.1.4 (p. 274), or trimming the entry's two overrun quotes. Note the row's `teaches` column (col 6) does carry the histogram/classify point, so only §3.2/§5.1.4 overrun.

## 5. Remaining entry claims verified sound (anchors)

- Guard identity: sha256 at candidate `03a796c5726c…` == contract pin; `git log --oneline 8ca67421..f181a961 -- tools/staged-id-guard.py` is empty — "never edited" holds. Docstring names exit 1 only for inadmissible map (guard `:32-35`); the imprecision is recorded in `corpus/lessons/round-49.md:104` as the entry says.
- Oracle-from-docstring list: census 0-3 spaces, collisions `sorted(..., key=id_number)` (`tools/staged-id-guard.py:135`), form-insensitive document keys, naive map + cascade, map-validation rules — all present in the guard's docstring/selftest.
- "the guard's own 14 selftest fixtures": `git show f181a961:.ufo/evidence/round-49/control/c2-fixed-fixtures.json | python3 -c 'json.load'` → list of 14 (no mutant tokens). The guard's selftest has 23 case() assertions over those fixtures; "14 fixtures" is the fixture count, correct.
- Generator behaviour: `random.Random(seed)` (`pbt-staged-id.py:785`); per-case CLI subprocess `-I` (`:762`; `sys.executable`, equivalent-or-stronger to the entry's "python3 -I"); no import/exec of guard code (imports at `:45-54`); dump `{index, registry, staged, map}` (`:802-805`); stop at first violation (`:813-814`); last line `PBT_STAGED_ID: cases=… violations=… counterexample=… classes=…` (`:829-832`); all twelve frozen classes producible (probe: none missing; class list == `contract.json claims.C2.classes`).
- Counter description: frozen class predicates recomputed from the dump (`measure.py:118`), differential confirmation of counterexamples (docstring `:24-26`), oracle agreement on analysis-mode cases (`:21-22`, `:317-325`) — the entry's "How it is measured" matches the frozen counter.
- Coverage-map row same round (criterion 7): `corpus/README.md:597`.
- `recheck:` runnable: both commands observed printing `1` (smallbone: 'that fit the program at hand'; quick: 'print out a histogram of these values').

## 6. Observations (no action required)

- The witness sentence ("confirms all 12, so no panel mutant is equivalent") carries its anchor only by paragraph adjacency; the receipt line exists (`c2-controls.stdout:3`). Naming the receipt path inline would satisfy criterion 2 letter-perfectly — nit, not a defect, since the paragraph's citation covers it.
- The generator enforces its own `CLASS_MIN = 20` ("this seat's observed distribution floor (contract: 10)", `pbt-staged-id.py:66`) — stricter than the counter's 10 and undisclosed in the entry; harmless (harder, not easier, to pass).
- The entry's "0-8 rows"/"3-5 digits" style — round-number ranges for code facts — is exactly what D1/D2 show to be fragile; measured ranges, never hand-written ranges, are the lane's own rule (criterion 87's family).

## 7. Applicable QUALITY criteria (walk)

1 ✓ (every claim falsifiable with anchor). 2 — two claims fail their own anchor (D1, D2); all others anchored. 3 ✓ (observation/inference/unknown separated; "What this does not establish"). 4, 5 n/a. 7 ✓ (`README.md:597`). 10 ✓ header complete, rows opened same round, tiers A/B, no tier-C sole support — with D3's anchor-scope tension. 34 ✓ (contract.json cited by JSON key; F1 by heading). 91-spirit ✓ (all quotes byte-located in the pinned snapshots). 97 — `after/c2.stdout` pending-by-design, named as the deciding receipt; resolves at the landing tip. 87 n/a (no quote-length labels). 99 n/a.

## Summary

- All nine QuickCheck/Smallbone quotes verified verbatim at their cited sections and pages in the pinned snapshots; digests match entry and SOURCES rows.
- Deciding-run numbers correctly deferred to `after/c2.stdout` (absent at candidate by design); the asserted control numbers (6/12 CTL_FIX, 12/12 witness) match `control/c2-controls.stdout:2-3`; requirement numbers match the frozen counter's constants.
- No overclaim: F10 'held' never stated in the entry, no-shrinking and panel-size-12 both explicitly bounded; the counter-blindness disclosure accurately cites wave-1 F1.
- D1 (minor): "ids of 3-5 digits" false — code generates 3 or 4-6 digit ids (`pbt-staged-id.py:472-475`); probe saw widths {3,4,5,6}.
- D2 (minor): "(0-8 rows)" false at the low end — measured combined range 2..8; zero-row tables never occur.
- D3 (minor, shape): entry's S269 line cites §3.2/§5.1.4, which row S269's anchor column (`corpus/SOURCES.md:144`) does not declare; sibling precedent (S006, S097) binds entry anchors to row anchors. Quotes themselves are genuine.
- Smallest corrections: one appended dated erratum in the entry fixing D1+D2 wording; one append-only SOURCES erratum (or entry trim) for D3. Nothing found that voids the entry or the claim it supports.
