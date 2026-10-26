# T49ScribeEntryDraft — F10 pilot entry draft (C2 record half)

Seat: T49ScribeEntryDraft (scribe). Lane: tameshi-shokunin at base
`8ca67421111fa354b47b803358391d0b07fc6db9` (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD`).
I did not decide, run or preview the C2/C1 counters, and did not edit any product,
registry, record, generator or guard file.

## 1. Deliverable

`.ufo/waves/round-49/w1/T49ScribeEntryDraft.pbt-generator-pilot.md` — 223 lines, target
path `corpus/knowledge/pbt-generator-pilot.md` (the L1 copies it there).

Shape follows a recent sourced lane entry: `source:` header block, `verified-at`,
`recheck`, `ground: F10`, then a titled body. Head/line conventions taken from
`corpus/knowledge/r42-attribute-and-outflag-destinations.md:1-9` and
`corpus/knowledge/r44-anchor-refresh-rule.md:1-4` (`sed -n 1,9p` on each).

Body sections: `## What the sources state` (four source-stated generator principles, each
quoted and located), `## What the lane built` (generator, its oracle, size control,
twelve recipes, observed distribution, stop-at-first-violation) with a twelve-row class
table, `## How it is measured` (the counter's seven `total` terms, the hidden panel,
differential confirmation, controls), `## What it does not establish` (seven limits),
`## The pointer that was wrong` (S_SB anchor correction), `## Summary`.

## 2. Facts: contract constants vs what I observed

Every number in the draft is either a frozen contract constant, a fetched-source fact, or
marked `@…@`. I ran nothing that scores a claim.

| draft claim | where it comes from |
|---|---|
| seed 4949, 400 cases, class floor 10, kill target 11, 12 classes | `.ufo/evidence/round-49/contract.json` `claims.C2.seed/cases/class_min/panel.kill_target/classes`; `.ufo/evidence/round-49/c2/measure.py:49-53` (`SEED, CASES = 4949, 400`, `CLASS_MIN = 10`, `KILL_TARGET = 11`, `CLASSES`) |
| panel 12 mutants, sha256 `d6dd2cf3…eeda1`, single-site mutants | contract `claims.C2.panel`; `measure.py:47` (`PANEL_SHA`), `measure.py:238-243` (`text.count(m['old']) == 1`) |
| guard sha256 `03a796c5…2dca8`, pinned, not edited | contract `claims.C2.named_gate`; `measure.py:45-46`; my own `sha256sum tools/staged-id-guard.py` in `T49ScribeEntryDraft.guard-receipt.txt` |
| guard exit semantics 0/1/2 as stated | contract `claims.C2.guard_exit_semantics_observed`; code `tools/staged-id-guard.py:471-493` |
| counter terms, oracle, class predicates, confirmation rule | `measure.py:90-150`, `:310-361` (line-anchored in the draft) |
| CTL_ABSENT / CTL_FIX / WITNESS behaviour | contract `claims.C2.controls` |
| `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` / `VERDICT: PASS`, exit 0 | my run at base: `python3 -I tools/staged-id-guard.py --selftest` — receipt |
| generator's CLI/oracle/recipes/`CLASS_MIN = 20`/round-robin/stop-at-first | the wave-1 draft `.ufo/waves/round-49/w1/T49ExecGenerator.pbt-staged-id.py` (module docstring; `CLASSES`, `CLASS_MIN`, `RECIPES`, `case_classes`, `run`) |
| S_QC and S_SB quotations | fetched this session; each span located once — `T49ScribeEntryDraft.quote-check.txt` |

## 3. Open placeholders (the L1's substitutions)

In the entry:

1. `@CLASSES@` — the twelve `CLASS <name>=<n>` counts printed by the deciding run
   (`measure.py:352-354`).
2. `@KILLS@` — confirmed mutants of 12 from the differential replay (`measure.py:331-350`).
3. `@FIXKILLS@` — `CTL_FIX`'s confirmed count (contract `claims.C2.controls.CTL_FIX`).
4. `S_QC` and `S_SB` in the two `source:` lines are placeholder ids, deliberately written
   so the counter's own regex does **not** accept them:
   `^source:\s*(S\d{3,})\b` (`measure.py:277`) finds zero ids in the draft head today
   (`T49ScribeEntryDraft.head-check.txt`). Replacing `S_QC`/`S_SB` with the live ids is
   mandatory before the deciding run, or `records_bad += 1` (`measure.py:277-281`).

Requirements the replacement rows must meet, from the counter's own check
(`measure.py:284-286`): the row must sit at 0–3 leading spaces, have **exactly 11 cells**,
`cells[7] == mined`, `cells[8] == 2026-10-26`. Additionally the counter needs a
`corpus/README.md` line carrying both `F10` and `held (round 49)` (`measure.py:287-291`);
at base the F10 row still reads `open` — `grep -n F10 corpus/README.md` → `87:| F10 | PBT
generators for gate fixtures | S018, S019, S020, S021 | open | …`.

## 4. Findings

1. **The merge's S183 anchor does not resolve — corrected in the draft.**
   `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:37` (and
   `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r4-quickcheck-primary-correction.md:3`)
   anchor "good test data generators, that fit the program at hand" at **§4.1, p. 44**.
   In the row's own URL, fetched 2026-10-26 (`sha256 eaee48f9…44ac08`, 1,269,821 B), the
   sentence is in **§2.10 "Generating Test Data", printed p. 34 (PDF p. 39)**; §4.1 of the
   thesis is "A Parallel Correctness Criterion", and printed p. 44 opens §3.4 "shr:
   Problems with Partiality" (both lines in
   `T49ScribeEntryDraft.smallbone-receipt.txt`, produced by `grep -n` and a page split of
   the `pdftotext -layout` output). The draft states the corrected anchor and its
   `## The pointer that was wrong` section records why.

2. **The two staged merge rows cannot be copied into `corpus/SOURCES.md` verbatim: they
   have 13 and 14 cells, not 11.** Their `recheck` cells carry unescaped `|` characters.
   Command: cell-count loop over `SOURCES.append.md` lines 36–37 printed in
   `T49ScribeEntryDraft.smallbone-receipt.txt` ("cell counts" section). Consequence: the
   L1 must rewrite both rows (pipe-free or escaped recheck) or the counter's records check
   fails on cell count (`measure.py:285`). The draft's own `recheck:` line also contains
   pipes inside backticks — fine in an entry, **not** copyable into a registry row.

3. **Guard docstring exit-1 wording is narrower than the code — recorded, not edited.**
   `tools/staged-id-guard.py:39` ("exit 1 = the map is not admissible") against
   `:157` (`refused = bool(unmapped) or bool(cascade)`) and `:473`/`:493`
   (`verdict='refused'` → `return 1`). The draft states the observed semantics and cites
   both sides; the guard stays pinned.

4. **The generator draft is live and its line numbers move.** First read this session it
   was 896 lines with `RECIPES` at 652; a re-check minutes later it was 956 lines with
   `RECIPES` at 710 and `CLASS_MIN = 20` at 66 (`wc -l`;
   `grep -n "^RECIPES\|^CLASS_MIN\|^def case_classes"`).
   The draft therefore cites **symbols, not line numbers** for that file, and says so. Any
   L1 line-cite into `T49ExecGenerator.pbt-staged-id.py` must be re-derived at REV.

5. **S_QC's fetch route is a provenance caveat.** `aaron papers fetch 10.1145/351240.351266
   --mode auto` returned `tier=scihub`, `meta={"mirror": "https://sci-hub.ee", "pdfUrl":
   "https://sci.bban.top/pdf/10.1145/351240.351266.pdf", "pdfBytes": 313371}`, 67,519 chars
   of markdown. Recorded in `T49ScribeEntryDraft.quickcheck-receipt.txt`, not smoothed. If
   the L1 pins a different route, re-run `T49ScribeEntryDraft.quote-check.py` against the
   new copy: the draft quotes de-spaced spans, which survive reflow but not a different
   edition.

6. **The S_QC copy is OCR-damaged; the draft keeps the damage instead of repairing it.**
   The fetched text splits words (`prop erties`, `p ossible`, `b ound`) and loses ligatures
   (`dene`, `de ne`, `ma jor`, one `0x0e` byte inside `su?ciently`). Repaired quotes cannot
   be re-located in the snapshot, so every quote in the draft is verbatim-with-artifacts,
   and the entry says so before the first bullet. All 12 quotation spans were de-spaced and
   located exactly once. The entry carries 12 quoted spans; the verifier's table holds
   the 11 substantive ones (the 12th is the section title `2.4 Monitoring Test Data`),
   and it prints `QUOTE_CHECK: spans=11 mismatched=0` —
   `T49ScribeEntryDraft.quote-check.txt`.

7. **Class coverage is designed, and the oracle is a second reading of one docstring.**
   `measure.py:315-327` compares the counter's oracle with the guard only for cases with
   `map is None`; a `--map` case is scored by class membership and by the panel only. The
   generator's twelve recipes are one per class, scheduled round-robin
   (`run()`: `RECIPES[order[index % len(order)]]`), so the printed histogram partly
   measures the schedule. Both are in the entry's "what it does not establish" as limits.

8. **The contract's control text says "the guard's own 14 selftest fixtures"; the guard
   has 5 literal fixture tables and 24 assertions.** Commands:
   `python3 -I tools/staged-id-guard.py --selftest` → `cases=24 failed=0`;
   `grep -c "    case(" tools/staged-id-guard.py` → 24;
   `grep -c "^SELFTEST_[A-Z_]* =" tools/staged-id-guard.py` → 5. The entry therefore cites
   the observed 24 and does not repeat "14". Flagged for the L1 in case the CTL_FIX receipt
   wording is compared against it (contract text was not mine to change).

9. **A `held (round 49)` README line and the SOURCES rows are outstanding (L1 scope).**
   Both are counter inputs (`measure.py:284-291`), not entry content, so they stay out of
   the draft. A suggested index-row text is in §6 below.

## 5. What the draft deliberately does not claim

No run of the generator, no panel result, no kill count, no class count, no mutation score,
no second gate, no shrinking, no coverage-of-input-space claim, and no statement that the
guard's docstring is correct. Placeholders carry every unfilled number.

## 6. Suggested L1 record texts (not written anywhere)

- SOURCES row for S_QC: anchor "§Abstract; §1; §2.4; §3.2; §6.6; §7", `status=mined`,
  `opened=2026-10-26`, recheck **without pipes**.
- SOURCES row for S_SB: anchor "§2.10 \"Generating Test Data\", p. 34" (not §4.1/p. 44).
- README index row: `corpus/knowledge/pbt-generator-pilot.md` — one generator against one
  named gate, measured by a hidden panel; frontier row F10 `open → held (round 49)`.

## 7. Bounds, provenance, tooling

- Wrote only `tameshi-shokunin/.ufo/waves/round-49/w1/T49ScribeEntryDraft*` (deliverable +
  five receipts + one verifier script). No edit to the lane checkout, the fleet repo, sibling
  lanes, `shokuknow`, jj state or the Git index; no `git`/`jj` mutating command for library
  work (only `rev-parse`, `sha256sum`, `sed`, `grep` reads).
- Read nothing under `~/.local/state/`, and none of `c2-WITNESS.stdout`,
  `c2-CTL_FIX.stdout`, `c2-CTL_ABSENT.stdout`.
- Scratch: `/fast/scratch/hyaku/tameshi-r49/T49ScribeEntryDraft/` — removed before yield
  (`rm -rf`), so no cited path lives there; every cited output was copied into `w1` first.
  The verified source bytes went with it, so both URLs were re-fetched afterwards and pinned
  by sha256 in the receipts (PDF unchanged; the QuickCheck text identical at 67,519 chars),
  and the verifier passes against the re-fetch.
- Tooling: no installs and no upgrades. `aaron` was already present at
  `~/.local/bin/aaron`; `curl`, `pdftotext`, `python3` were already present.

## 8. Receipts (all in `.ufo/waves/round-49/w1/`)

- `T49ScribeEntryDraft.pbt-generator-pilot.md` — the draft (223 lines).
- `T49ScribeEntryDraft.quote-check.py` + `.quote-check.txt` — de-spaced relocation of every
  quoted span, with its section (S_QC) or PDF/printed page (S_SB); `mismatched=0`.
- `T49ScribeEntryDraft.smallbone-receipt.txt` — fetch, size, sha256, page/anchor evidence,
  staged-row cell counts.
- `T49ScribeEntryDraft.quickcheck-receipt.txt` — fetch metadata and route caveat, markdown
  heading map, abstract bytes, ligature-loss counts.
- `T49ScribeEntryDraft.guard-receipt.txt` — guard sha256, `--selftest` output, assertion and
  fixture counts, docstring-vs-code exit lines.
- `T49ScribeEntryDraft.head-check.txt` — the draft head parsed with the counter's own
  regexes: zero ids (placeholders), two source lines, three `@…@` tokens.

## Summary

The F10 pilot entry is drafted at `.ufo/waves/round-49/w1/T49ScribeEntryDraft.pbt-generator-pilot.md`
(223 lines, house head, target `corpus/knowledge/pbt-generator-pilot.md`): four sourced generator
principles quoted and located, the twelve-class table, the counter's seven `total` terms, seven limits.
Placeholders: `@CLASSES@`, `@KILLS@`, `@FIXKILLS@`, plus ids `S_QC`/`S_SB`, which the counter rejects
until replaced by 11-cell `mined` `2026-10-26` rows. The draft corrects a live pointer — Smallbone's
sentence is §2.10 p. 34, not the merge's §4.1 p. 44 — and both staged merge rows are 13/14 cells, so
neither can be copied into the registry. All 12 quotation spans re-locate exactly once in the fetched
bytes. Nothing here is a C2 verdict: a draft is a seat's output, not a claim decision.
