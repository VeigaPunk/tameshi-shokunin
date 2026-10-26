# T49Read02 — C1 reader, `## Mutation-sweep recipe`, pointer ordinals 5-9

Seat: T49Read02 (C1 reads, wave 1). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base: `8ca67421111fa354b47b803358391d0b07fc6db9`. Frozen pointers:
`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`.
Contract read first: `.ufo/evidence/round-49/contract.json` (C1 predicate, `reads.json` schema,
section floors — recipe floor 34; ordinals 5-9 are five of the 34).

Deliverable: `.ufo/waves/round-49/w1/T49Read02.rows.json` — 5 rows, one per pointer, each with
heading, ordinal, raw, file, ranges, claim, base_verdict, excerpt, reader, note.

## Method (read-only; no counter invocation)

- Pointer rows extracted, not retyped:
  `python3 -c "import json;d=json.load(open('.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json'));..."`.
- Section text at base: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421111fa354b47b803358391d0b07fc6db9:SKILL.md | sed -n '131,245p'`
  (heading line 131; next heading `## Defect-taxonomy templates` at line 246). Section pointer
  count at base = 34, matching the C1 floor.
- Targets at base: `git -C <lane> show 8ca67421…:corpus/knowledge/mutation-case-kimi-census.md`
  and `…:corpus/knowledge/mutation-case-kagi-census.md`.
- Excerpt acceptance replicated from the frozen counter's own helpers, read only:
  `measure.py:202-208` (`norm` = `re.sub(r"\s+"," ",t).strip()`; `pointed_text` = the pointed
  line ranges joined then normalized), `measure.py:81` (`EXCERPT_MIN, EXCERPT_MAX = 24, 400`),
  `measure.py:304-312`. I did **not** execute `measure.py` (no `--selftest`, `--list` or probe);
  the constant check was reimplemented in a scratch script and every row re-validated for
  (a) `file`/`ranges` equality with the frozen pointer, (b) `24 <= len(excerpt) <= 400`,
  (c) `excerpt` substring of the normalized pointed text. All 5 rows passed (`ALL_OK True`).
- Claims are verbatim SKILL.md clauses; where a clause wraps across lines inside the section the
  line-wrap whitespace is collapsed to one space (noted per row; no wording changed). Each claim
  was asserted to occur in the normalized section text before writing.
- Scratch: `S=/fast/scratch/hyaku/tameshi-r49/T49Read02`, deleted at exit (see bottom).

## Findings — one row per pointer

**1. Ordinal 5 — `mutation-case-kimi-census.md:13-16` — `holds`.**
SKILL.md:150-152 clause "Record: path, full sha256, size, line count, mtime, repo revision, and
`git status --porcelain -- <path>` empty". Target `kimi-census.md:13-16` records sha256
`83016d45…4f426`, `896 lines`, `43273 B`, mtime `2026-10-13 18:53:12`, kumitate repo
`175de6ba…`, and `` `git status --porcelain -- scripts/kimi-census.mjs` empty `` — every listed
element, with the path named in the status clause (bare filename anchored to
`kumitate-shokunin/scripts/kimi-census.mjs` at `kimi-census.md:10`). Lines land exactly on the
pin block; no drift. Excerpt (301 chars) is the whole collapsed range.

**2. Ordinal 6 — `mutation-case-kagi-census.md:13-17` — `holds`.**
SKILL.md:153-154 clause "note that gate's 887th line carries no trailing newline". Target
`kagi-census.md:13-17`: sha256 `275d8294…53009f`, `44212 B`, "886 newlines (the 887th line
carries no trailing newline — `tail -c1` prints `c`)", mtime `2026-10-14 09:47:15 -0300`,
`mode 755`, kagi `HEAD fecee874…`, and `` `git status --porcelain -- corpus/surface-census.sh`
empty ``. The 887th-line caveat is verbatim at `kagi-census.md:14-15`. Line count is expressed
as 886 newlines plus the newline-less 887th line, i.e. 887 lines — the same count the section
asks for, and the section's own parenthetical explains that form. Excerpt 376 chars = whole
collapsed range.

**3. Ordinal 7 — `mutation-case-kagi-census.md:44-45` — `holds`.**
SKILL.md:159-160 clause "the bash lane additionally `cmp`-verified its copy". Target
`kagi-census.md:44-45`: "each defect = ONE exact-string replacement applied to a fresh copy of
`pristine.sh` (a `cp -p` byte copy, `cmp`-verified)". That is the cmp re-verification of the
copy. The clause's shared `sha256sum` half is not on these two lines (the kagi restore proof
carries the before/after sha256 at `kagi-census.md:54-56`), but the pointer is attached to the
cmp clause after the dash and those lines state it exactly. Lines 44-45 are the cmp clause; no
drift. Excerpt 121 chars.

**4. Ordinal 8 — `mutation-case-kimi-census.md:41-53, :155-166` — `holds`.**
SKILL.md:165-166 clause "the JS 10-defect manifest is the shape". Target range 41-53 is the
kill-rate table — header with a `Defect class` column, control row, then D1-D10 each with a
killed/survived verdict; range 155-166 is the fenced driver spec listing D1-D10 as one exact
edit each, including D4's three-line block deletion (`kimi-census.md:159`), i.e. the "single
block deletion" form. Ten defects, one row each: the manifest shape the section cites. The
pre-registered `expect:` record is **not** in these ranges — the section cites that separately as
E1 (ordinal 9) — so the claim recorded for this row is the manifest-shape claim these lines
support, not a pre-registration claim. Second range is a bare `:155-166` in the raw pointer,
resolved to the same kimi file by the frozen extractor and consistent with the SKILL parenthetical
at line 166. No drift. Excerpt 373 chars = table header + control + D1 row.

**5. Ordinal 9 — `mutation-case-kimi-census.md:183-191` — `holds`.**
SKILL.md:168-169 clause "E1: the author's D7 expectation was wrong and is kept". Target
`kimi-census.md:183-191` is §5 `## 5. Calibration and errata (append-only)` E1: "the author's
pre-run expectation held for 9/10 defects; it was **wrong on D7**", quotes the filed expectation
and its reasoning, gives the measured outcome, and closes "Recorded as a calibration miss" — the
expectation is wrong and kept, in an append-only section. Lines 183-191 land exactly on E1; no
drift. Excerpt 255 chars (heading plus the wrong-on-D7 sentence and the filed expectation).

## Verdict counts

`holds` 5, `stale` 0, `unresolved` 0, `absent` 0. No `proposed_fix` rows are emitted, so no
`skill_old`/`skill_new` edits are proposed for this section by this seat. The section's base
pointer count (34) is untouched by this seat.

## Known limits / out of scope

- Base verdicts only; the deciding run and any REV-time resolution are the L1's. This seat did not
  run `.ufo/evidence/round-49/c1/measure.py` in any mode and did not score a control.
- Semantic support was judged for the clause each pointer is attached to, not for neighbouring
  pointers (ordinals 0-4, 10-33 are other seats' rows).
- Rounding caveat, not a defect: ordinal 6's count is recorded as 886 newlines + a newline-less
  887th line rather than the integer "887"; the pointed text states this explicitly and the
  section repeats the caveat, so it is not stale under the drift rule.
- No tool installed or upgraded this session (pacman paused host-wide; nothing was needed).
- No counter stdout, no hidden C2 panel path, and no `round-49/control/c2-*.stdout` file was read.
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read02` removed before yield; nothing written under
  `/tmp` beyond small transient files.

## Summary

- Five recipe rows read at base (ordinals 5-9); all five `holds`, none stale/unresolved/absent.
- Pin rows (kimi:13-16, kagi:13-17) carry every recorded field, including the kagi 887th-line caveat.
- The kagi cmp re-verification is exactly at kagi:44-45; the sha256 half lives in the same note's restore proof.
- The kimi 10-defect manifest (table 41-53 + edit spec 155-166) is the shape the section cites; `expect:` is cited separately as E1 (183-191).
- E1 is wrong-on-D7 and kept, under an append-only heading — lines land exactly on it.
- Excerpts auto-cut from the pointed text and re-validated against `measure.py`'s own norm/length rules (24-400, substring) — 5/5 pass.
- No fix proposed for this section; base pointer count 34 and the recipe floor of 34 are unaffected.
- Deliverable: `.ufo/waves/round-49/w1/T49Read02.rows.json`.
