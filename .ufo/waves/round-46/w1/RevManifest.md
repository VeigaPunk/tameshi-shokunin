seat: RevManifest

item: reviewed the declared mutant manifest .ufo/evidence/round-46/hardening/mutants.json (15 freshness mutants F01–F15, 10 coverage mutants C01–C10, 6 neutral) against its round-45 audit sources and counters: applicability, syntax, behaviour delta, source-pointer accuracy, pair-distinctness, neutral equivalence at ea25, and whether 23-of-25 is a reachable honest target.

## Method and bounds

- Scratch only: `/tmp/tameshi-r46-RevManifest/` (copies of both round-45 counters, mutated probes, neutral run outputs). Lane writes: this report file only. No git/jj mutating commands; the only git calls were read-only `git -C <lane> show`.
- Counters were run only as `--selftest`, via the seat helper `try-mutants.py` (never a measurement), and as round-45 deciding-command probes `python3 <copy> --lane <lane> --rev ea25e0224fc81060414b27301c27bd1344669165` for the neutral diff (explicitly required by my item; copies ran from scratch, so these are not verdicts).
- No tools installed (stdlib python 3 only); pacman untouched.

## Inventory, applicability, syntax

`python3` script over mutants.json: every non-null `old` occurs **exactly once** in its round-45 source (31/31 checks, count=1); the 2 `old=null` entries (FN1, CN1) are appends. All 31 mutated files **parse and compile** (`ast.parse` + `compile`): `bad=0`. Pins: my copies sha256 = `ba64041f49ff…` (freshness) and `2f321b2c499f…` (coverage), equal to the audit-pinned freeze blobs; `git show 745a5831:.ufo/evidence/round-46/hardening/mutants.json` is byte-identical to the worktree file (sha `bd21304a48a0d1e5…`); both counters at `ea25e022` hash to the same bytes as at the freeze (`ba64041f49ffcf15…`, `2f321b2c499ff432…`).

`try-mutants.py --group <g> --file <scratch copy>` on the **orig** counters (my independent rerun of the frozen receipt before/c2-at-freeze.stdout): pristine `pass VERDICT: PASS` both groups; **all 25 mutants `survived`, all 6 neutrals `survived`, 0 `inapplicable`** — matches the receipt (`declared=25 killed=0 survived=25 inapplicable=0 neutral_killed=0 pristine=1`). Survived (not crash-killed) plus parse+compile proves every mutant is a genuine rule disable, not a syntax error. Driver sanity: `mutate.py --selftest` → `cases=8 failed=0`, `VERDICT: PASS`.

## Behaviour table (mutated copy vs pristine copy)

Deltas demonstrated empirically by importing `grade`/`population`/`review_sets` from mutated scratch copies (probe fixtures under `neutral/*-probe*.py`); the rest from code reading at the cited lines. All 31 rows change nothing else: each `old` is unique and the replacement is local.

| id | behaviour change | evidence |
|---|---|---|
| F01 snapshot-absent reason | **yes** (reason-only on ordinary inputs) | `grade` L141–142: absent snapshot → `raw = b''` → falls into sha check; T9 asserts state only so it survives orig. Can flip state only if an entry carries `raw_sha256 == sha256(b'')` AND verdict `drifted`; never reaches `verified` (6–25-token quote can't sit in empty text). Probe corner noted; audit S9's kill = assert `why`. |
| F02 quote upper bound 25 | **yes** | Probe: 26-token quote present in snapshot with overlap 2 → pristine `('invalid','quote length 26')`, mutant `('verified','ok')`. |
| F03 quote present | **yes** | Probe: absent 9-token quote sharing {score, equals, detected} → pristine `('invalid','quote absent')`, mutant `('verified','ok')`. |
| F04 population needs URL | **yes** | Probe on one 4-row input: population delta +{S159} (mined, id≤160, `url=None` admitted). |
| F05 duplicate refusal | **yes** (measure-level) | `measure()` L241: duplicate ids no longer forced invalid; `--selftest` never calls `measure()` → structural survivor (receipt + my try-mutants run). Kill = fixture-repo measure run (audit S4 / MutC1Counter-2 T23). |
| F06 review non-author | **yes** | Probe: self-review (who==author) with report naming reviewer+id, author in seats → pristine `agreed=∅`, mutant `agreed={S001}`. (My first probe reproduced the audit's double-masking: with ExecA absent from seats/text the delta is invisible — exactly why S5 survived round-45.) |
| F07 seat output non-empty | **yes** | `wave_seats` L189: whitespace-only output (`'   '`) becomes a seat. Distinct from MutC1Reviews #8, which dropped the whole conjunct and was KILLED; F07 (strip-only) survives — confirmed by the frozen receipt and my run. Manifest correctly cites MutC1Counter S6 only. |
| F08 report path prefix | **yes** | L206: readable out-of-prefix reports admitted; fixture masks it (both out-of-prefix reports unreadable via `reports.get`) → survivor. Kill: readable report outside `.ufo/waves/round-45/` naming id+reviewer (audit S7/Reviews 3). |
| F09 report names reviewer | **yes** | Probe: report `S002 rechecked today` (id named, reviewer absent), non-author seat → pristine `agreed=∅`, mutant `agreed={S002}`. |
| F10 dispute sinks agree (measure) | **yes** (measure-level) | L254 `fresh = len(agreed)` keeps disputed rows in fresh; unexercised under `--selftest`. Kill: measure run with agree+dispute row (audit S10/Reviews 7, T25). |
| F11 self_pin in predicate | **yes** | L256: `passed` drops the self_pin conjunct. Discriminator from F12: `self_pin=0 ∧ fresh≥50` passes F11-mutant only. Kill needs a ≥50-fresh fixture repo (heaviest case; audit S11/T24). |
| F12 target 50 in predicate | **yes** | L256: `fresh >= 0` vacuous. Discriminator from F11: `self_pin=1 ∧ fresh<50` passes F12-mutant only. Cheap kill. |
| F13 only agree counts | **yes** | Probe: verdict `fine` review → pristine `agreed=∅`, mutant `agreed={S001}`. |
| F14 population status mined | **yes** | Probe: delta +{S005} (`retired` row admitted; `!= 'queued'`). Registry has held/retired rows, so visible at REV data too. |
| F15 id bound inclusive | **yes** | Probe: delta −{S160} (mined S160+URL dropped). Only visible at S160 — the item's own example; kill = mined S160 row with URL. |
| FN1/FN2/FN3 | **equivalent** | Deciding-command runs at ea25 (mutated scratch copy vs pristine copy): all output lines identical except the `self_pin=`/`_PASS=` tail (mutated copy pins 0 by construction — the artifact `mutate.mask`/`equivalence()` canonicalizes); FN2 is `13`→`0xD`; FN3 a comment. FN1 initially mis-probed by me (ran pristine bytes); rerun with the append applied: masked-identical, `all other lines identical: True`. |
| C01 googletest URL pin | **yes** | L35: `GT_RE` becomes `…(github\.com\|raw\.githubusercontent\.com)/` — any github path passes (audit M01; kill = github-non-googletest row, `rows=0`→`rows=2`). |
| C02 snapshot prefix round-45 pin | **yes** | L36: admits `round-4[45]` paths (audit M03; kill = round-44 snapshot rows). |
| C03 missing snapshot skips row | **yes** | L83: `data = b''` → row survives with empty text when the anchor hex is `e3b0c442…`; `rows` count flips, entries still can't quote empty text (audit M04). |
| C04 source: prefix line 1 | **yes** | L98: provenance line-1 prefix no longer required (audit M06; kill = ids on a non-`source:` line 1). |
| C05 recheck: line 3 | **yes** | L103: line 3 unchecked (audit M08). |
| C06 README full-path form | **yes** | L129: full-path disjunct dropped → full-path-only README gives `indexed=0` (audit M12). |
| C07 rows≥2→≥1 | **yes** | L135 conjunct; kill = T6 fixture with `want='C2_R45_PASS=false'` (pristine rows=1→false, mutant→true). |
| C08 entries≥2→≥1 | **yes** | Same site, `entries` conjunct; kill = T3 fixture with PASS-false want. |
| C09 indexed==entries→≥1 | **yes** | Same site, `indexed` conjunct; kill = T7 fixture (indexed=1, entries=2) with PASS-false want. |
| C10 self_pin==1→>=0 | **yes** | L135: pin vacuous; kill = build variant writing foreign SELF_PATH bytes (audit M14). |
| CN1/CN2/CN3 | **equivalent** | Same protocol as FN*: masked-identical at ea25; CN2 `0xD==13`; CN3 a comment. |

## Pair-distinctness (double counting)

No two mutants make the same behavioural change:

- F04/F14/F15: disjoint deltas **on one shared probe input** (+{S159}, +{S005}, −{S160}) — proven, not argued.
- F11 vs F12 touch the same line but different conjuncts; each has a discriminator input the other fails (above).
- F06 vs F09: different gates (author vs reviewer-in-text), each with an isolating fixture (probes).
- F02 vs F03: different grade stages; T5' (26-token, present) kills F02 only — F03 keeps the length check so it still returns `invalid 'quote length 26'`; T4' kills F03 only.
- C07/C08/C09: three different count variables of the same printed predicate; each has a boundary fixture with `want='C2_R45_PASS=false'` that pristine passes and exactly one of them flips.
- F01, F05, F07, F08, F10, F13, F14, C01–C06, C10 each disable a rule no other entry disables.

So one kill case cannot legitimately retire two declared mutants; counting toward 23 is per-mutant honest.

## Source pointers

All 31 `source` fields checked against `.ufo/waves/round-45/w1/MutC1Counter.md`, `w1/MutC2Counter.md`, `w2/MutC1Reviews.md`: every cited entry (S1–S12, M01/M03/M04/M06/M08/M12/M13/M14, Reviews 1/3/5/6/7/9/10) exists, is a **survivor** in its audit, and describes the same replacement. Two findings worth recording:

1. **MutC1Reviews #8 vs F07**: the Reviews audit reports the L189 site KILLED — but its mutation drops the whole conjunct (`and str(x.get('output') or '').strip()`), admitting empty-output seats; F07 removes only `.strip()`. Different mutations, both real; the manifest cites S6 (strip-only, SURVIVED) and the frozen receipt confirms `F07 survived` on orig. No defect — but a reader comparing audits sees an apparent contradiction that is actually two mutants at one site.
2. All freshness survivors cited from MutC1Counter (S1–S12) and all coverage survivors from MutC2Counter (M01–M14 minus killed M02/M05/M07/M09/M10/M11) match the manifest's old/new byte-for-byte in intent; nothing cites a killed-only audit entry.

## Verdict: is 23-of-25 reachable and honest?

**Reachable: yes, with margin. Honest: yes.**

- All 25 are applicable today (inapplicable=0 in the receipt and in my runs) and assemble.py preserves applicability by construction: its only edits are the SELF_PATH line, the selftest tally print, and insertion before `def main():` — none of the 31 anchors intersects those three needles (anchor lines 35/36/40/61/74/83/97/103/129/135/142/151/157/189/204/206/209/211/241/254/256 freshness, 35/36/40/74/83/98/103/129/135 coverage; needles elsewhere).
- All 25 kills are constructible inside the existing harnesses: 7 freshness kills were demonstrated empirically in round-45 (S1–S3, S5–S8: fixture-only PASS + mutant FAIL); my probes add demonstrated flips for F02, F03, F04, F06, F09, F13, F14, F15; F01/F05/F10/F11/F12 have concrete case designs (S9 assert-why; MutC1Counter-2's T23/T24/T25 measure-run fixtures — F11's is the only heavyweight, needing a ≥50-row fixture repo). Coverage: all 10 kills are one-line additions to the existing `build()` case table per the M-audit recipes.
- Honest: no pair duplicates, no syntax-error entries, no already-killed entries (killed=0 on orig, receipt + my rerun), and the counter's arithmetic (`mutate.py`: `killed >= MIN_KILLED`, `neutral_killed == 0`, `pristine`, `equivalence`) counts only applicable, genuinely-flipped mutants; an inapplicable mutant counts as not killed. The equivalence=1 gate is non-vacuous: my pristine runs at ea25 print `C1_R45_PASS=true fresh=71` and `C2_R45_PASS=true rows=2 entries=2 indexed=2`, so the orig side of `equivalence()` passes.

## Residual risks and verification gaps

1. The hardened counters (`freshness-counter.py`, `coverage-counter.py`) do not exist yet — reachability is analysis + probes + audit demonstrations, not a `--targets hardened` run; the deciding run is the L1's.
2. If an `extra_*` addition quotes an anchor string verbatim (e.g. `if quote not in text:` inside a comment), `apply()` sees count=2 and that mutant becomes inapplicable (= not killed). Still honest, just costs a kill; hardening seats should keep case text free of anchor literals.
3. Kill quality: `judge` scores a crash as killed. On the orig targets nothing crashed (all survived + parse), but on hardened targets seats should read the tail column and confirm FAIL-lines, not tracebacks.
4. F01's kill couples the selftest to the exact reason string `snapshot absent` — intended (that is the declared rule), but it makes the hardened selftest stricter than the round-45 one by design.
5. Unrun by me: a full 23-kill rehearsal on assembled hardened copies (out of my scope; RevengerR70/HardMeasure lanes own the tightening), and `mutate.py --lane --rev` at the freeze/base revs (L1's deciding runs).
