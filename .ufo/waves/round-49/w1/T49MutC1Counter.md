# T49MutC1Counter — mutation probe of the frozen C1 counter (round 49, wave 1)

Seat item: mutation-test the frozen C1 counter `.ufo/evidence/round-49/c1/measure.py`
(label `C1_R49_PASS`) in scratch with 12+ single-edit mutants and run its `--selftest`
against each; report survivors with the input that would distinguish each. The lane
file was never edited. Scratch root `/fast/scratch/hyaku/tameshi-r49/T49MutC1Counter`
was deleted before this report was finished; all observed outputs are embedded below.

## Method

- Target bytes: `sha256 .ufo/evidence/round-49/c1/measure.py` →
  `a055e9297cc989cc69062ae4a1e5b22c251dc3adfcc073211c5cae3a09346065` (before **and**
  after the probe — restoration evidence; the file was only read, never written).
- Detector: the counter's own `--selftest` (34 cases). Baseline on the pristine copy:
  `C1_R49_SELFTEST: cases=34 failed=0`, exit 0. A mutant is *killed* iff selftest
  exits non-zero (failing case(s) or crash); otherwise *survived*.
- 28 single-edit mutants, each applied by exact-string replacement (unique occurrence
  asserted) to the scratch copy only; one behavioral point per mutant.
- No tools installed (none needed; host pacman transactions are paused — recorded per
  the 2026-10-19 tooling authorization: zero installs, zero upgrades).

## Kill table

Line numbers refer to `.ufo/evidence/round-49/c1/measure.py` at base
`8ca67421111fa354b47b803358391d0b07fc6db9` (bytes `a055e929…`). "Observed" = the
selftest cases that failed under that mutant (or crash), as printed by
`TMPDIR=$S/w python3 -B $S/mutants/<id>.py --selftest` in scratch.

| id | line | category | single edit (old → new) | expected detector | observed | verdict |
|----|------|----------|--------------------------|-------------------|----------|---------|
| M01 | 87 | extractor regex | bare lookbehind `(?<![\w:./-])` → `(?<![./-])` | time-not-pointer | `time-not-pointer,url-port-not-pointer` (cases=34 failed=2) | killed |
| M02 | 85 | extractor regex | CONT drops `:?` continuation form | continuation-colon | `continuation-colon` (failed=1) | killed |
| M03 | 153 | bare-pointer inheritance | `last` → `None` (inheritance dead) | bare-inherits-paragraph-file | `bare-inherits-paragraph-file` (failed=1) | killed |
| M04 | 188 | resolution order | `corpus/` tried before `corpus/knowledge/` | resolve-knowledge | cases=34 failed=0 | **survived** |
| M05a | 299 | range bound check | drop `e <= n` (EOF bound) | range-past-eof | `range-past-eof` (failed=1) | killed |
| M05b | 299 | range bound check | drop `1 <= s` (lower bound) | — | cases=34 failed=0 | **survived** |
| M06 | 81 | excerpt min | `EXCERPT_MIN` 24 → 4 | reads-excerpt-too-short | `reads-excerpt-too-short` (failed=1) | killed |
| M07 | 81 | excerpt max | `EXCERPT_MAX` 400 → 4000 | — | cases=34 failed=0 | **survived** |
| M08 | 203 | excerpt normalization | `\s+` → ` +` (newlines/tabs kept) | norm | `norm,path-sid-absent-ok` (failed=2) | killed |
| M09 | 270 | row matching keys | duplicate rows accepted (`len(hits)==1` → truthy) | reads-duplicate-row | `reads-duplicate-row` (failed=1) | killed |
| M10 | 274–275 | absent rule | drop `pointer_kind == 'path'` condition | unresolved-no-file | cases=34 failed=0 | **survived** |
| M11 | 382 | floor check | `floor_short = 0` | — | cases=34 failed=0 | **survived** |
| M12 | 65 | durability VOLATILE list | drop `corpus/README.md` | — | cases=34 failed=0 | **survived** |
| M13 | 62 | monitor pin check | `MONITOR_SHA` first hex digit corrupted | — | cases=34 failed=0 | **survived** |
| M14 | 402 | total arithmetic | drop `+ res['not_holds']` | — | cases=34 failed=0 | **survived** |
| M15 | 400 | monitor gate | drop `overrides is False` check | — | cases=34 failed=0 | **survived** |
| M16 | 157 | path-pointer dedup | dedup condition → `if True:` | extract-kinds | cases=34 failed=0 | **survived** |
| M18 | 128 | table-row paragraphing | `startswith('|')` branch → `elif False:` | table-row-bare-unresolved | cases=34 failed=0 | **survived** |
| M19 | 115 | extractor regex (parse) | en dash `\u2013` → em dash `\u2014` | en-dash | crash: `ValueError: invalid literal for int() ... '377–378'`, exit 1, no case summary | killed (crash) |
| M20 | 197 | line_count | trailing empty line counted (`if False and …`) | line-count | `line-count` (failed=1) | killed |
| M21 | 208 | pointed_text | `lines[s - 1:e]` → `lines[s:e]` (off-by-one) | pointed-text | `pointed-text,reads-ok,external-ok,path-sid-absent-ok` (failed=4) | killed |
| M23 | 287 | external blob path | `p['file'][3:]` → `p['file']` (keeps `../`) | external-ok | `external-ok` (failed=1) | killed |
| M24 | 282 | fleet_commit regex | `{40}` → `{39}` hex | external-ok | `external-ok` (failed=1) | killed |
| M26 | 304 | verdict set | `!= 'holds'` → `not in ('holds','stale')` | reads-not-holds | `reads-not-holds` (failed=1) | killed |
| M27 | 91 | extractor regex (S-id) | `S\d{3,}` → `S\d{2,}` | extract-kinds | cases=34 failed=0 | **survived** |
| M28 | 90 | extractor regex (path) | drop `:\d` trailing guard | extract-kinds | `extract-kinds` (failed=1) | killed |
| M29 | 79 | floor literal | `TARGETS[0]: 34` → `33` | — | cases=34 failed=0 | **survived** |
| M30 | 401 | total arithmetic | score gate `== 8` → `== 7` | — | cases=34 failed=0 | **survived** |

Totals: 28 mutants — 14 killed, 14 survived. Mutant file hashes (first 12 hex) were
recorded per mutant; all differ from the pristine hash.

## Survivors — the selftest case each lacks (probe-confirmed)

Seven survivors are behavioral; each was probed on a scratch fixture repo against both
pristine and mutant modules (observed outputs embedded; probes are not verdicts):

- **M04 (line 188, resolution order).** Distinguishing input: a lane where `n.md`
  exists as both `corpus/n.md` and `corpus/knowledge/n.md` (no root copy). Observed:
  pristine `resolve → ('corpus/knowledge/n.md', 'line', None)`; M04
  `('corpus/n.md', 'line', None)`. A reads row excerpted from the other file's text
  then flips ok↔excerpt_miss. Missing case: `resolve-shadowed-path` — assert
  `resolve(repo, rev, 'n.md')[0] == 'corpus/knowledge/n.md'` in a repo holding both.
- **M05b (line 299, lower range bound).** Distinguishing input: pointer `f3.md:0-3`
  on a 3-line file with a `holds` row excerpted from the last line. Observed: pristine
  `{unresolved: 1}`; M05b all-zero (bound passes; `pointed_text` reads
  `lines[-1:3]` = the last line, so the excerpt matches). Verdict-level false pass:
  unresolved (+1) becomes ok (+0). Missing case: `range-zero-start` — assert
  `unresolved == 1` for a `:0-3` pointer.
- **M07 (line 81, excerpt max).** Distinguishing input: a `holds` row whose excerpt is
  450 chars and occurs verbatim in the pointed text. Observed: pristine
  `{excerpt_miss: 1}`; M07 all-zero. Missing case: `reads-excerpt-too-long`.
- **M10 (lines 274–275, absent rule).** Distinguishing input: an unresolvable **line**
  pointer (`gone/x.py:4`, file=None) with a row `verdict='absent', file=null`.
  Observed: pristine `{unresolved: 1}`; M10 `{absent: 1}`. Verdict-level false pass:
  `absent` is not a term of `total` (lines 401–402), so unresolved (+1) becomes
  absent (+0). Missing case: `absent-on-unresolved-line-pointer`.
- **M16 (line 157, path dedup).** Distinguishing input: a section citing the same path
  token twice, e.g. ``see `a.md` then `a.md` twice``. Observed: pristine one path
  pointer `['a.md']`; M16 `['a.md', 'a.md']` — ordinals shift, so reads rows keyed
  heading+ordinal+raw mismatch → unverified. Missing case: `path-dedup` — assert one
  path pointer for a repeated token.
- **M18 (line 128, table-row paragraphing).** Distinguishing input: a table row
  directly after a prose line holding a file pointer (`See a.md:3\n| t | (`:9`) |`).
  Observed: pristine `(':9', token=None)` (own paragraph, unresolved); M18
  `(':9', token='a.md')` (inherits across the table boundary). Missing case:
  `table-row-after-prose` — assert the bare pointer in the row stays unresolved.
- **M27 (line 91, S-id digits).** Distinguishing input: a two-digit id in prose
  (`also S12 and S999 here`). Observed: pristine sids `['S999']`; M27
  `['S12', 'S999']` — `S12` becomes a pointer, resolves to no SOURCES row →
  unresolved. Missing case: `sid-two-digit-not-pointer`.

Seven survivors are structural: `--selftest` never calls `measure()` — inside the
selftest span (lines 416–544) there are zero references to `measure`/`run_monitor`/
`durability_commit`/`FLOORS`/`VOLATILE`/`MONITOR_SHA` (shown by
`sed -n '416,544p' measure.py | grep -n -e measure( -e run_monitor …` → no match;
those names occur only at lines 15, 25, 62, 65, 78, 319, 336, 349, 368–402, 583):

- **M11/M29 (lines 382/79, floor).** Input: a target section whose pointer count
  dropped below its frozen floor (e.g. recipe 34 → 33). Pristine: `floor_short=1`,
  total>0; mutant: 0 → can false-pass a section that lost pointers.
- **M12 (line 65, VOLATILE).** Input: a monitor credit that depends on the
  `corpus/README.md` record line. Pristine appends the probe to all five records at
  the durability commit D; mutant leaves `corpus/README.md` unchanged at D, so a
  record-bound credit would lapse and `durable_covered` would drop — the mutant
  weakens exactly the durability gate (b) the counter exists to enforce.
- **M13 (line 62, monitor pin).** Input: any real `measure()` run. The mutant makes
  every invocation raise `Setup('monitor pin mismatch')` exit 2 — a denial mutant;
  selftest cannot see it because it never validates the pins.
- **M14 (line 402, total arithmetic).** Input: a tree with exactly one `not_holds`
  row and everything else clean. Pristine: total=1 → `C1_R49_PASS=false`; mutant:
  total=0 → **false PASS**. This is the highest-value survivor: a single-edit defect
  in the verdict sum flips the claim while selftest stays green.
- **M15 (line 400, monitor gate).** Input: monitor output with
  `overrides_used=true` (non-strict path used). Pristine: bad_mon +1 → false; mutant:
  ignored → can false-pass an override-assisted credit.
- **M30 (line 401, score gate).** Input: monitor printing
  `calibration_restraint_score 7`. Pristine: +1 → false; mutant: gate passes →
  false PASS at the wrong score.

## Findings

1. The counter's `--selftest` is a real detector for the extractor/resolution/read-row
   surface: 14/28 single-edit mutants killed (13 by failing case, 1 by crash).
2. Coverage finding (survivors, not contract changes): the selftest has no case for
   (a) shadowed resolution order, (b) zero-start ranges, (c) over-long excerpts,
   (d) `absent` rows on non-path pointers, (e) repeated path tokens, (f) table rows
   adjacent to prose, (g) two-digit S-ids — and no case at all reaches `measure()`
   (pins, durability VOLATILE, floors, score gate, total arithmetic). The
   `absent`-not-in-total interaction (M10) and the `not_holds` term (M14) are the two
   survivors that flip the verdict label on plausible inputs.
3. M19 is caught only by crash (`ValueError` in `parse_ranges`), not by a case —
   detection exists but of the crudest kind; a graceful wrong-parse en-dash mutant
   would be worth adding to the selftest alongside the seven missing cases above.

## Summary

- 28 single-edit mutants of the frozen C1 counter run under its own `--selftest` in scratch: 14 killed, 14 survived; lane file untouched (sha256 `a055e929…` before = after).
- Killed cleanly: bare lookbehind, continuation `:?`, inheritance, EOF bound, excerpt min, normalization, duplicate rows, line_count, pointed_text off-by-one, external path/commit checks, stale verdict, path trailing guard; en-dash killed by crash.
- 7 behavioral survivors probe-confirmed with distinguishing inputs: resolution order (shadowed path), `:0-3` lower bound, >400-char excerpt, `absent` on line pointers, path dedup, table-row adjacency, 2-digit S-ids.
- 7 structural survivors: selftest never calls `measure()` — pins, VOLATILE durability, floors, overrides gate, score gate, and the total sum (incl. dropping `not_holds` → false PASS) are invisible to it.
- Highest-value finding: M14 (total arithmetic) and M10 (absent rule, `absent` not a total term) flip `C1_R49_PASS` on plausible inputs while selftest stays green.
- Recommended selftest additions (for the L1 to weigh, not a contract change): `resolve-shadowed-path`, `range-zero-start`, `reads-excerpt-too-long`, `absent-on-unresolved-line-pointer`, `path-dedup`, `table-row-after-prose`, `sid-two-digit-not-pointer`, plus one measure()-level case.
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49MutC1Counter` deleted; no tools installed (pacman paused).
