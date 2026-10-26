# T50ScribeEntryDraft — F6 knowledge-entry draft (round 50, wave 1)

Seat: T50ScribeEntryDraft (scribe). Lane read-only except the three deliverables below. No claim was
decided; no counter was run (not even `--selftest`); the hidden C2 panel was neither read nor listed.
Scratch `/fast/scratch/hyaku/tameshi-r50/T50ScribeEntryDraft` was deleted before this report was
finalised (the two snapshots I cite are copied into the wave directory, not left in scratch).

## Deliverables

| Path | What it is |
|---|---|
| `.ufo/waves/round-50/w1/T50ScribeEntryDraft.fixture-shrinking-pilot.md` | the F6 entry draft, target `corpus/knowledge/fixture-shrinking-pilot.md` (10864 B) |
| `.ufo/waves/round-50/w1/T50ScribeEntryDraft.receipts.md` | every command I ran and its observed output (source fetches, digests, shrinker probes, control lines) |
| `.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/delta-debugging.pdf` | snapshot of the new Zeller & Hildebrandt row (247738 B, sha256 `7ed0c812…e1c8aa`) |
| `.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/ecoop2020-abstract.txt` | extracted ECOOP 2020 abstract (S022), 2404 B |
| this file | claims ↔ source pointers, completion checklist for the L1, findings |

## Behavior observed

- The shrinker the entry describes exists only at `.ufo/waves/round-50/w1/T50ExecShrinker.shrink-case.py`
  (629 lines, 28590 B, mode 755); `tools/shrink-case.py` is still absent from the lane
  (`ls tools/shrink-case.py .ufo/waves/round-50/w1/ | grep -i shrink` → only the w1 file).
- Its `--selftest` exits 0 in both layouts I could stage: 14 cases with only the generator beside it
  (`SHRINK_SELFTEST: cases=14 failed=0`, real-guard leg skipped), 21 cases in a scratch fixture where
  `staged-id-guard.py` and the round-49 panel sit beside it (`SHRINK_SELFTEST: cases=21 failed=0`).
  The frozen counter copies only the generator beside the tool (`.ufo/evidence/round-50/c2/measure.py:227-230`),
  so the measured selftest is the 14-case run.
- The positive control at freeze reaches the whole panel with the counter's reference shrinker:
  `C2_R50: … mutants=20 ok=20 units_before=164 units_after=43 … C2_R50_PASS=true`
  (`.ufo/evidence/round-50/control/c2-CTL_REF.stdout`, last line). The counter's own selftest receipt is
  `C2_R50_SELFTEST: cases=9 failed=0` (`.ufo/evidence/round-50/control/c2-selftest.stdout`).
- Source checks: the Zeller & Hildebrandt PDF fetched this round yields both quoted sentences
  (`removing any single input entity would cause the failure to disappear` → 1 match;
  `139 automated test runs, or 35 minutes on a 500 MHz PC`); the ECOOP abstract yields the validity
  sentence; the S024 snapshot yields `every character contained is required to produce the error` after
  tag stripping (1 match). Commands and outputs: `T50ScribeEntryDraft.receipts.md` §1-§3.

## Claims in the draft and their source pointers

Line numbers are for the bytes I read today (lane tip `4afb060`), as the entry's own house style
requires the pointer, not the number.

| # | Claim in the draft | Pointer | Command that shows it |
|---|---|---|---|
| 1 | New row is Zeller & Hildebrandt, IEEE TSE 28(2):183-200, Feb 2002, opened from the Purdue course mirror | `tameshi-shokunin/.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/delta-debugging.pdf` (247738 B, sha256 `7ed0c812…`); venue/anchor as staged in `shokuknow/merge/tameshi/SOURCES.append.md:21` (read-only) | `curl -fsSL 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf' \| sha256sum` |
| 2 | "fed with a failing test case, which it simplifies by successive testing" + the 1-minimality sentence (§I) | PDF §I, extracted lines 67-71 of `pdftotext delta.pdf` | `pdftotext .ufo/waves/round-50/w1/T50ScribeEntryDraft.src/delta-debugging.pdf - - \| grep -n 'removing any single input entity'` |
| 3 | "The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC" | PDF §Abstract/§I, extracted lines 13-15 | `pdftotext … - - \| grep -n '139 automated'` |
| 4 | S022 title, DOI, validity sentence | `drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13`; extracted abstract at `.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/ecoop2020-abstract.txt` | `curl -fsSL <url> \| grep -c 'test-case validity problem'` → 3 |
| 5 | S024 "Its result is 1-minimal, meaning that every character contained is required to produce the error" | `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html` (sha256 `3abede35…e99`) | `sed 's/<[^>]*>//g' … \| tr -s ' \n' ' ' \| grep -c 'every character contained is required to produce the error'` → 1 |
| 6 | Guard pinned, never edited | `tools/staged-id-guard.py` sha256 `03a796c5…` = `.ufo/evidence/round-50/c2/measure.py:53`; described as never edited in `corpus/knowledge/pbt-generator-pilot.md:8` | `sha256sum tools/staged-id-guard.py` |
| 7 | Generator frozen at `7d3d977f`, sha256 `0cbee392…` | `.ufo/evidence/round-50/c2/measure.py:50-51` | `git show 7d3d977f:tools/pbt-staged-id.py \| sha256sum` |
| 8 | Interfaces, units, sub-case, kill, exit codes, stdlib-only | `.ufo/evidence/round-50/contract.json:54` (`claims.C2.shrinker_interface`) | `sed -n '54p' .ufo/evidence/round-50/contract.json` |
| 9 | Method: ddmin chunks → complement → refine → single-unit fixpoint; verdict cache; every invocation counted | `.ufo/waves/round-50/w1/T50ExecShrinker.shrink-case.py:100-149` (ddmin), `:152-178` (Shrinker), `:180-215` (shrink) | `sed -n '100,150p;180,215p' …/T50ExecShrinker.shrink-case.py` |
| 10 | Selftest: synthetic predicates, stub CLI, real-guard M02 leg | `…/T50ExecShrinker.shrink-case.py:414-605`; summary line `:605` | `python3 -I …/T50ExecShrinker.shrink-case.py --selftest` (14/21 cases, exit 0) |
| 11 | "It edits neither guard" | write sites only at `…/T50ExecShrinker.shrink-case.py:272` (OUT), `:308` (temp case dir), `:332` (`.runs` in selftest), `:455-460`, `:550-556` (temp copies) | `grep -n "open(.*['\"]w\|shutil.copy\|unlink" …/T50ExecShrinker.shrink-case.py` |
| 12 | The kill is the generator's oracle on both guards | `.ufo/evidence/round-50/c2/measure.py:157-160`; oracle `tools/pbt-staged-id.py:296-299`; guard driver `:756-770` | `sed -n '153,161p' .ufo/evidence/round-50/c2/measure.py` |
| 13 | Setup refusals count as oracle agreement | `tools/pbt-staged-id.py:304-309` (exit 2 requires `verdict=setup_refusal` with a reason) | `sed -n '296,310p' tools/pbt-staged-id.py` |
| 14 | Units = registry lines + staged lines + `map['map']` entries; other map fields fixed | `.ufo/evidence/round-50/c2/measure.py:98-108` (units/map_entries), `:130-143` (sub-case) | `sed -n '98,108p;130,144p' .ufo/evidence/round-50/c2/measure.py` |
| 15 | Counter re-checks 1-minimality itself over every single-unit removal | `.ufo/evidence/round-50/c2/measure.py:111-124` (removals), `:299` | `sed -n '111,124p;299p' .ufo/evidence/round-50/c2/measure.py` |
| 16 | Cost check: stated `runs` = instrumented guard invocations; unit counts re-derived | `.ufo/evidence/round-50/c2/measure.py:62-64` (instrumentation), `:281-284` (logged), `:300-302` | `sed -n '62,64p;281,284p;300,302p' .ufo/evidence/round-50/c2/measure.py` |
| 17 | Panel: 12 public + 8 hidden = 20; hidden digest pinned | `.ufo/evidence/round-50/contract.json:50,55,56`; public panel ids M01-M12, sha256 `d6dd2cf3…` | `python3 -c "import json;print([m['id'] for m in json.load(open('.ufo/evidence/round-49/c2/panel.json'))['mutants']])"` |
| 18 | At least 19 of 20 ok, and the ok mutants shrink in total | `.ufo/evidence/round-50/c2/measure.py:313-314` | `sed -n '312,315p' .ufo/evidence/round-50/c2/measure.py` |
| 19 | Records: README line with F6 + `held (round 50)`; entry new since base citing a mined row opened 2026-10-26 | `.ufo/evidence/round-50/c2/measure.py:325-354` (parsing `^ {0,3}\|\s*(S\d{3,})\s*\|`, `cells[7]=='mined'`, `cells[8]=='2026-10-26'`) | `sed -n '325,354p' .ufo/evidence/round-50/c2/measure.py` |
| 20 | Counter selftest drives `measure()` end to end on a fixture repo | `.ufo/evidence/round-50/c2/measure.py:421-520`; receipt `control/c2-selftest.stdout` | `cat .ufo/evidence/round-50/control/c2-selftest.stdout` |
| 21 | A plain greedy-to-fixpoint shrinker meets the bar (positive control) | `.ufo/evidence/round-50/contract.json:59`; `control/c2-CTL_REF.stdout` last line | `tail -1 .ufo/evidence/round-50/control/c2-CTL_REF.stdout` |
| 22 | Round-29 attempt: "ddmin made 171 oracle tests and kept nothing, because no subset kills" | `corpus/knowledge/survivor-fixture-minimization.md:53-54` | `sed -n '53,54p' corpus/knowledge/survivor-fixture-minimization.md` |
| 23 | Round-49 gap: "No shrinking: a counterexample is the first failing case, not a minimal one" | `corpus/knowledge/pbt-generator-pilot.md:69` | `sed -n '69p' corpus/knowledge/pbt-generator-pilot.md` |
| 24 | Generator cases are tiny (two to eight rows across the pair) | `corpus/knowledge/pbt-generator-pilot.md:45` | `sed -n '45p' corpus/knowledge/pbt-generator-pilot.md` |
| 25 | Measured values live in the deciding receipt, not the entry | `.ufo/evidence/round-50/deciding-run.sh:45-47` (writes `c2.stdout` into `OUTDIR`) | `sed -n '43,48p' .ufo/evidence/round-50/deciding-run.sh` |
| 26 | The counter's tool dir holds only the tool + generator | `.ufo/evidence/round-50/c2/measure.py:219-240` | `sed -n '219,240p' .ufo/evidence/round-50/c2/measure.py` |
| 27 | F6's current frontier row and the append-only precedent | `corpus/README.md:83` (row F6, `open`, next move), `:599` (F10 `held (round 49)` paragraph added rather than rewriting the row) | `sed -n '83p;599p' corpus/README.md` |

## Completion checklist for the L1 (the draft is not committable as-is by design)

1. **Replace `S_ZH` with the real row id — which is `S271`, not the package's `S167`.** The lane's
   `corpus/SOURCES.md:495` reads "Next unused id: S271 (staged ids S161-S255 stay reserved by document
   for the package)"; the round-49 precedent for adding package rows `S269`/`S270` from staged
   `S182`/`S183` is `corpus/SOURCES.md:494`. The staged id `S167` exists only in the merge package
   (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:21`), and `S167` is free but inside
   the document-reserved `S161-S255` range.
2. **Append the row with the counter's column shape**: 11 cells with status at `cells[7] = mined` and
   `cells[8] = 2026-10-26`, or `measure.py:352` never sets `records.entry`. If the row writes
   `used-by corpus/knowledge/fixture-shrinking-pilot.md`, that file must already exist or the census
   raises `E11` (`scripts/sources-census.sh:567`).
3. **Add the README line** containing both `F6` and the literal `held (round 50)` (`measure.py:329-330`);
   follow the F10 paragraph precedent at `corpus/README.md:599` and leave the frontier table row at
   `corpus/README.md:83` as written.
4. **Do not commit the entry before `tools/shrink-case.py` exists** (copy byte-exact from
   `.ufo/waves/round-50/w1/T50ExecShrinker.shrink-case.py`); its first paragraph names the tool at that
   path. My probes ran the w1 copy, not the lane copy.
5. **Keep the snapshot path in the header true**: the PDF currently lives at
   `.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/delta-debugging.pdf`; if it is moved (the round-49
   convention put snapshots under `.ufo/waves/round-49/w1/T49ScribeRows.src/`), update the header.
6. **Reconcile the anchor with the sourcing seat's receipt** (T50ExecSrcZeller) if that seat records a
   different page or a different mirror; the words quoted are verified against the copy I fetched.
7. **Optionally add the index row** for the new entry in the knowledge table (`corpus/README.md:597` is
   the F10 pattern). Nothing monitors the lagging-index debt in this round's no-harm script
   (`grep -n 'knowledge\|README' .ufo/evidence/round-50/no-harm.sh` → no match), but the debt count is
   tracked at `corpus/README.md:43`.

## Findings

1. **The id must be re-pointed by document, not copied from the package.** `corpus/SOURCES.md:495`
   reserves `S161-S255` and names `S271` next; `grep -c '^| S167 |' corpus/SOURCES.md` → `0`, so the
   package id is free but reserved. The draft uses `S_ZH` so the substitution is a single edit.
2. **S022 is `queued` in the lane** (`corpus/SOURCES.md:33`), S024 is `mined` (`:35`). No census code
   fires for citing a queued row (`scripts/sources-census.sh:24-30` lists E01-E12 and no such rule —
   inference from the legend, not from a run), but flipping S022 to `mined` obliges a `used-by` path
   that exists (`sources-census.sh:567`). S024's `used-by` currently names only
   `corpus/knowledge/survivor-fixture-minimization.md` (`SOURCES.md:35`).
3. **The counter's measured selftest is the 14-case run with the real-guard leg skipped** — the tool
   skips it unless `staged-id-guard.py` and `pbt-staged-id.py` both sit beside it
   (`.ufo/waves/round-50/w1/T50ExecShrinker.shrink-case.py:518-520`), and the counter's tool dir holds
   only the generator (`measure.py:227-230`). Observed: 14 cases in that layout, 21 in a fixture layout
   with the guard present. The draft records this as a limit rather than as an unqualified "selftest
   covers the real guard".
4. **The kill criterion is oracle agreement, not admission.** `measure.py:157-160` plus
   `tools/pbt-staged-id.py:304-309`: a case the pristine guard refuses at setup can be a legal pristine
   side; the draft states this in its limits instead of writing "passes the pristine guard" without
   qualification.
5. **The round-29 failure mode is the reason the round-49 generator's case is the starting point.**
   `corpus/knowledge/survivor-fixture-minimization.md:53-54` ("no subset kills"), and round 49's own
   limit line (`corpus/knowledge/pbt-generator-pilot.md:69`). The draft's opening paragraph names that
   gap; no measured value is asserted there.
6. **The entry asserts nothing measured.** All numbers it carries are source quotes or the freeze-time
   control (164 → 43, 20/20), each labeled and pointered; the round's own numbers are deferred to the
   deciding receipt (`deciding-run.sh:45-47`). This keeps the entry invulnerable to a different
   deciding outcome and satisfies "measured values live in the receipt" (the round-49 entry's rule,
   `pbt-generator-pilot.md:12`).
7. **Assimilation theme F6's second file was triaged, not cited.** `r7-ieice-mutant-abstraction-authority.md:5,47`
   reports a *manual* survivor-set abstraction (five survivors → one, 69 generated, 16 merged, 11
   killed) — a different operation from input minimization, and the lane has no SOURCES row for the
   report (grep for `IEICE|段階的` in `corpus/SOURCES.md` → no match; its staged id `S197` belongs to
   the merge package). The draft cites only the three rows it can point at; folding IEICE in would need
   its own row first.
8. **My entry cites the S024 book sentence only up to the missing noun.** The snapshot's text reads
   "removing any (as seen in tests #27 and #29, above) no longer makes the test fail" — the book omits
   the noun it refers to, so the draft quotes the clause before it, verified verbatim.

## Out of scope / not done

- No counter invocation of any kind (not `--selftest`, not `--explain`); no claim decided.
- The hidden panel (`.ufo/evidence/round-50/c2/panel-hidden.json`, digest pinned in the contract) and
  everything under `/home/vgpnk/.local/state/` were not read or listed.
- No lane write beyond the four deliverable paths in this wave directory; no git/jj mutation anywhere;
  no edits to `corpus/README.md`, `corpus/SOURCES.md`, `tools/`, or the contract.
- The shrinker's method/efficiency was not evaluated; only its selftest was run as a probe, and the
  draft claims the capability plus stated cost, not a search result.
- `r7-ieice-mutant-abstraction-authority.md` was read for triage only.

## Artifacts

- `.ufo/waves/round-50/w1/T50ScribeEntryDraft.fixture-shrinking-pilot.md`
- `.ufo/waves/round-50/w1/T50ScribeEntryDraft.receipts.md`
- `.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/delta-debugging.pdf`
- `.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/ecoop2020-abstract.txt`

## Summary

- Draft: `.ufo/waves/round-50/w1/T50ScribeEntryDraft.fixture-shrinking-pilot.md` — PBT header form, `S_ZH` placeholder, tested `recheck` pipelines, `ground: F6`.
- Body: 1-minimality, cost in test runs, the validity problem; the shrinker over the round-49 killing cases (units, kill, method, cost, selftest); the counter's four re-checks per mutant, its 9-case selftest and the greedy positive control; seven limits.
- Every assertion is pointered in the claims table; all three source quotes verified against bytes fetched or snapshotted today; no measured value is asserted in the entry.
- L1's edits: id `S271`; 11-cell row with `mined`/`2026-10-26`; README line carrying `F6` and `held (round 50)`; copy the tool to `tools/` before committing the entry.
