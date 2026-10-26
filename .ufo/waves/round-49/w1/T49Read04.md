# T49Read04 — C1 reader, `## Mutation-sweep recipe`, pointer ordinals 15-19

Seat: T49Read04 (C1 reads, wave 1). Lane `tameshi-shokunin`; base `8ca67421111fa354b47b803358391d0b07fc6db9`;
contract `.ufo/evidence/round-49/contract.json` (read, never edited). I decide nothing: this is a base read, and
every verdict below is a `base_verdict` for the L1 to integrate.

## Scope and method

Item: for each pointer of `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` with ordinal
15-19 (frozen in `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`), read the SKILL.md clause at
`skill_line` and the pointed text at base, and decide whether the target supports the clause.

Commands used (all read-only; `--list` is the one sanctioned counter mode, everything else is library calls of the
counter's own `norm()` / `pointed_text()` / `extract()` / `check_reads()`):

```
git -C LANE show 8ca67421111fa354b47b803358391d0b07fc6db9:SKILL.md | sed -n '131,215p'
git -C LANE show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/mutation-case-kimi-census.md | sed -n '29,35p;59,78p'
git -C LANE show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/mutation-case-kagi-census.md | sed -n '27,35p;50,53p;60,120p'
python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list
git -C LANE grep -n 'SELFTEST: FAIL' 8ca67421111fa354b47b803358391d0b07fc6db9 -- corpus/knowledge/mutation-case-kagi-census.md
git -C LANE grep -n 'SELFTEST: FAIL' 8ca67421111fa354b47b803358391d0b07fc6db9 -- .
git -C LANE diff --stat 8ca67421 455b2cd -- corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md
```

(`LANE` = `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.)

Preconditions checked, not assumed:
`--list` at base reproduces the frozen pointer list byte-for-byte (`n=90`, equality `True`), and the section text
at base hashes to `e37cf21e3155bdd39a68ef24a5135f2ad62861bbb5794ec954abf42bb0bd631d` — the sha frozen in the
pointer control (`.ufo/waves/round-49/w1/T49Read04.excerpt-check.txt`, lines 5-6).

## Results — one line of reasoning per pointer

| ord | pointer (raw) | skill line | verdict | reasoning |
|---|---|---|---|---|
| 15 | `mutation-case-kimi-census.md:30-33` | 194 | **holds** | :32-33 says the suite count held — every mutant run enumerated `<n>/43` and the three green runs printed `KIMI_CENSUS_SELFTEST: 43/43 pass` — which is the clause's 43 denominator. |
| 16 | `mutation-case-kagi-census.md:27-35,50-53` | 194 | **holds** | :50-53 says the suite count held (`(<n>/16 cases)` on every run, green runs `SELFTEST: PASS (16 cases)`); the first range :27-35 carries the "skipped cases distinguished" half (:33-35: the counter counts skips as cases). |
| 17 | `mutation-case-kimi-census.md:59-76` | 196 | **holds** | :59 heads "Failing-case labels of the narrow kills" and :61-76 quote the exact bad-case labels per defect with counts — the practice the clause demands. |
| 18 | `mutation-case-kagi-census.md:82-103` | 199 | **stale** | :84 has the `bad-case 05 undeclared-file …` exemplar verbatim, but the quoted summary `SELFTEST: FAIL (1/16 cases)` is not in the range and not in the file at all; the note records that suite line only as `1/16` / FAIL at :67, outside the pointer. |
| 19 | `mutation-case-kagi-census.md:88-91` | 203 | **holds** | :88-91 is exactly B4: `got exit=1` like the wanted one, the symlink fell into the regular-file arm and printed `SURFACE DIVERGED`, "the token assert is what killed it". |

Mechanical check of the five rows against the frozen pointer identities and ranges (counter `check_reads` at base):
`{'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0, 'not_holds': 1, 'absent': 0}` — the single `not_holds` is
ord 18, i.e. the stale row; every other row is `ok` (`T49Read04.excerpt-check.txt`, lines 15-20).

## Finding 1 (stale pointer, ord 18) — the quoted failing summary is not at the cited place

- Clause (`SKILL.md:196-199`): "Bash grammar: `bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got
  exit=0` and summary `SELFTEST: FAIL (1/16 cases)` (mutation-case-kagi-census.md:82-103)."
- The exemplar half is verbatim: `corpus/knowledge/mutation-case-kagi-census.md:84`.
  Shown by `git -C LANE show BASE:corpus/knowledge/mutation-case-kagi-census.md | sed -n '84p'`.
- The summary half is not: `git -C LANE grep -n 'SELFTEST: FAIL' BASE -- corpus/knowledge/mutation-case-kagi-census.md`
  prints nothing. The note records that suite line only in the kill-rate table, as `1/16` / FAIL, at
  `corpus/knowledge/mutation-case-kagi-census.md:67` — outside `:82-103`.
- The literal does exist in the lane, but in the round-1 cold-read capture:
  `.ufo/evidence/kaika-round-1/coldread/appendixB/B1.out:38` (and `B-tool.txt:22`), pattern shown by
  `git -C LANE grep -n 'SELFTEST: FAIL' BASE -- .`. So the quote is true of the gate and mis-sourced by the pointer.
- No line drift is involved: `:82` is still the labels header and `:103` still the last label line, and
  `git -C LANE diff --stat BASE 455b2cd -- <both targets>` is empty. The pointer's lines are right; the sentence
  quotes a line the target does not carry.
- Proposed fix (in `T49Read04.rows.json`, `proposed_fix`), one edit, pointer count unchanged:
  - `skill_old` = "and summary \`SELFTEST: FAIL (1/16 cases)\`\n     (mutation-case-kagi-census.md:82-103)."
  - `skill_new` = "and the failing suite line \`1/16\` / FAIL as the note records it\n     (mutation-case-kagi-census.md:67,82-103)."
  - corrected pointer: file `corpus/knowledge/mutation-case-kagi-census.md`, ranges `[[67,67],[82,103]]`,
    raw `mutation-case-kagi-census.md:67,82-103`.
  - corrected excerpt (150 chars, verified inside the collapsed pointed text of `:67,82-103`):
    `| B1 | wrong \`-eq\` (guard inversion) | scan guard \`-eq 0\` → \`-ne 0\` (\`surface-census.sh:241\`) | 1 | \`1/16\` / FAIL | **killed** | 1 (undeclared-file) |`
- Dry run of the fix on the base section text through the frozen extractor: 34 pointers before, 34 after; 33 of 34
  identical raw/token; ord 18 goes `82-103` → `67,82-103`; heading text unchanged
  (`T49Read04.excerpt-check.txt`, "proposed fix dry run"). After-fix projection through `check_reads`:
  `{'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0, 'not_holds': 0, 'absent': 0}` — this slice then
  contributes 0 to `total`.

## Finding 2 (sharpen-only, no verdict change) — ord 17's range stops mid-bullet

`corpus/knowledge/mutation-case-kimi-census.md:76` ends inside the D1/D3 bullet; its closing lines are `:77-78`
("and no-UNLISTED asserts; each fails because the green fixture itself now drifts. Full lists in
\`evidence/results.json\`."). The clause is fully supported inside `:59-76`, so this is holds, not stale; extending
to `:59-78` would keep the section's 34-pointer count and is optional. Shown by
`git -C LANE show BASE:corpus/knowledge/mutation-case-kimi-census.md | sed -n '74,78p'`.

Likewise ord 15's range opens two lines before its support (`:30-31` are the kill-rate sentence that
`SKILL.md:212` already cites as `:29-31`); the support (`:32-33`) is inside the range, so it resolves as holds.

## Finding 3 (prose defect in the same section, not a pointer)

`SKILL.md:193`: "Both historical sweeps held their enumerated denominators43 and16" — the two numbers have lost
their separating spaces ("denominators 43 and 16"), so the sentence reads `denominators43`. Shown by
`git -C LANE show BASE:SKILL.md | sed -n '193p'`. It does not affect resolution or extraction (the two pointers are
on `:194`), and it is outside my edit scope; flagged for the L1's section edit.

## Bounds / provenance

- Writes: only `.ufo/waves/round-49/w1/T49Read04.rows.json`, `.ufo/waves/round-49/w1/T49Read04.excerpt-check.txt`
  and this report. Lane checkout untouched (`git -C LANE status --porcelain -- corpus/knowledge/ SKILL.md` empty);
  no git or jj mutation anywhere; no fleet-repo write; nothing under `/home/vgpnk/.local/state/` read; the hidden
  C2 panel and the C2 control stdout files were not opened; no model was passed; no `agent://all` message.
- Counter use: `--list` at base (sanctioned) plus in-process calls to `norm`, `pointed_text`, `extract`,
  `target_sections`, `list_pointers`, `check_reads` — no deciding or measuring invocation, so nothing here is a
  verdict on C1.
- Scratch: `/fast/scratch/hyaku/tameshi-r49/T49Read04` (dump of the base SKILL blob, the two base target blobs,
  the row builder and the receipt generator). All citable output copied into `w1/`; the scratch directory is
  deleted before yield. No `/tmp` file was used.
- Tools installed/upgraded: none.
- Known limits: semantic support is my reading of the quoted text; the counter checks only that a quoted excerpt
  occurs at the pointed place, so it cannot and does not endorse these verdicts. Rows carry `base_verdict`
  (and a mirror `verdict`) as read at base; after applying the ord-18 fix the L1 must emit that row as `holds`
  with raw `mutation-case-kagi-census.md:67,82-103` and ranges `[[67,67],[82,103]]` (see `post_fix_verdict`).
- Reports/artifacts: `.ufo/waves/round-49/w1/T49Read04.rows.json` (5 rows),
  `.ufo/waves/round-49/w1/T49Read04.excerpt-check.txt` (excerpt/claim containment + fix dry run),
  this file.

## Summary

- Read the five `## Mutation-sweep recipe` pointers (ordinals 15-19) against their targets at base; frozen
  pointer list reproduced exactly by `--list`, section sha matches the frozen extractor sha.
- Verdicts: 15 holds, 16 holds, 17 holds, 18 **stale**, 19 holds.
- Ord 18 is stale because `SELFTEST: FAIL (1/16 cases)` is absent from `mutation-case-kagi-census.md` (and from the
  cited `:82-103`); the note records that suite line as `1/16` / FAIL at `:67`, outside the pointer.
- Fix supplied: quote the note's recorded form and extend the pointer to `:67,82-103` (34 pointers kept, ordinals
  unchanged); after-fix projection through the counter's own `check_reads` is all-clean.
- Ord 17's range and ord 15's range start/end imprecisely but contain their support: recorded as notes, not stales;
  `SKILL.md:193`'s "denominators43 and16" typo flagged for the L1.
- All five rows pass the mechanical pointer-identity/range/excerpt check at base (`not_holds` 1 = the stale row).
- Receipts: `T49Read04.rows.json`, `T49Read04.excerpt-check.txt`; scratch deleted; no tool installs.
