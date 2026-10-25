# ScribeRows — round 43, wave 1

author: seat `L1Tameshi43.ScribeRows` (scribe, leaf member; no dispatch)
date: 2026-10-25
item: draft the two new `corpus/SOURCES.md` rows (S159 Stryker equivalent-mutants docs,
S160 Wikipedia mutation testing) **in the report** — the registry was not edited.

Axes named: (1) row-cell correctness against the 11-column contract, (2) quote location
inside the snapshot bytes, (3) id reconciliation against the live tree.

## 1. Sources opened

Both were opened from the round-43 snapshots (no live refetch; the row cites the snapshot,
not the server). Pins recomputed by me with `sha256sum` + `wc -c`; they equal
`.ufo/evidence/round-43/sources/sha256.txt:1-2` byte for byte.

| doc | URL | snapshot | bytes | sha256 (full) |
|---|---|---|---|---|
| Stryker | https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | `.ufo/evidence/round-43/sources/stryker-equivalent-mutants.html` | 38687 | `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce` |
| Wikipedia | https://en.wikipedia.org/wiki/Mutation_testing | `.ufo/evidence/round-43/sources/wikipedia-mutation-testing.html` | 170793 | `6e4a06c0863ca2b0f68c36a1e29ca1eeeb01d20ae5e1d9ed4534a81406decc43` |

Titles: `Equivalent mutants | Stryker Mutator`; `Mutation testing - Wikipedia`
(revision `oldid=1373580212`, printed by the page footer at snapshot line 1017).
Stryker's page carries no version marker beyond `docs-version-current` (line 1), so the
anchor says "version unstated", the same limit S089 records.

Located quotes (snapshot line numbers; the files are minified, so one line = one block):

- Stryker, `<h1>Equivalent mutants` at line 4; body lines 15-17; closing paragraph line 24.
  - line 15: `Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!`
  - line 16: `It is called equivalent mutant. There is no definitive way for Stryker to find and ignore them. There is currently also no way yet to mark them to be ignored.`
  - line 17: `For now, the only solution is by finding these by hand, which is time consuming ... or accept that you won't make 100%.`
  - line 24: `... don't be scared of not 100% mutation score!`
- Wikipedia, `<h2>Overview` at line 738, paragraph 741; `<h2>Mutation testing overview` at line 762, paragraphs 794 and 796.
  - line 741: `... it can also indicate that the mutation introduces no faults. ... One (common) way a mutant can be valid is that the code that has been changed is "dead code" that is never executed.`
  - line 794: `... there are cases where it is not possible to find a test case that could kill this mutant. The resulting program is behaviorally equivalent to the original one. Such mutants are called equivalent mutants.`
  - line 796: `Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing. The effort needed to check if mutants are equivalent or not can be very high, even for small programs.`

## 2. Draft rows, item-literal ids (S159 Stryker, S160 Wikipedia)

```
| S159 | Equivalent mutants (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | docs | A | supersedes S089's anchor only: the worked 10 ** 0 example, the no-definitive-way and no-marking sentences, and the not-100-percent stance, for the survivor-resolution rule | §Equivalent mutants, body paragraphs at snapshot lines 15-17 and closing paragraph at line 24 @ page fetched 2026-10-25, version unstated (docs-version-current), snapshot .ufo/evidence/round-43/sources/stryker-equivalent-mutants.html 38687 B sha256 79f6501a | supersedes S089's anchor — the page works the 10 ** 0 = 1 case ("we will get the same output each time") and states "There is no definitive way for Stryker to find and ignore them", so an equivalent mutant stays a survivor Stryker neither detects nor lets anyone mark, and only hand analysis argues it away | mined | 2026-10-25 | 180d | corpus/knowledge/r43-survivor-resolution-rule.md |
| S160 | Mutation testing (Wikipedia) — https://en.wikipedia.org/wiki/Mutation_testing | docs | A | the two explanations the page gives for an undetected mutant — an untested fault or a fault-free change, dead code named as the common case — plus the equivalent-mutant definition, for the survivor-resolution rule | §Overview, p id mwPA (snapshot line 741) and §Mutation testing overview, p ids mw-Q and mw-w (lines 794 and 796) @ page fetched 2026-10-25, snapshot .ufo/evidence/round-43/sources/wikipedia-mutation-testing.html 170793 B sha256 6e4a06c0 revid 1373580212 | A mutant surviving the suite usually means the suite cannot locate the faults it represents but "can also indicate that the mutation introduces no faults", with dead code named as the common such case, and such behaviourally equivalent mutants have no test case that could kill them, which the article calls "one of the biggest obstacles" | mined | 2026-10-25 | 180d | corpus/knowledge/r43-survivor-resolution-rule.md |
```

Cell audit (contract = 11 columns; validator counts `NF==13` with the two border empties):

- `awk -F'|' ... NF=13` for both rows; no cell contains `|` (10 separators, 11 cells).
- `kind=docs` is in the validator enum (`spec|docs|paper|code|tool|dataset|talk|book|community|own-work`).
- `status=mined`, `opened=2026-10-25` (past/present), `recheck=180d`, `used-by` a single
  relative repo path — all four match the item's assignment exactly.
- Every `teaches` is one sentence and each of its quoted fragments is ≤11 words and located
  in the snapshot at the cited line.

## 3. Id conflict — reported verbatim, not resolved by me

The item's id assignment does **not** match the tree. Both statements are facts, so the
canonical judge gets them unedited:

1. `corpus/SOURCES.md:98` (HEAD) already holds the identical Stryker URL as **S089**,
   opened 2026-10-22:
   > `| S089 | Equivalent mutants (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | docs | A | Stryker's own statement that equivalent mutants cannot be found or marked automatically | page body after the `10 ** 0` example @ page fetched 2026-10-22 (version unstated; html sha256 bc572676…e04d) | an equivalent mutant stays a survivor in the score; calling a survivor a test-suite hole needs an off-suite witness or an explicit equivalence argument | mined | 2026-10-22 | 180d | corpus/knowledge/mutation-case-kumitate-cite-check.md, corpus/knowledge/r43-survivor-resolution-rule.md |`
2. The working tree (dirty against freeze `17f6ef0`) already carries **S159 = Wikipedia**
   at `corpus/SOURCES.md:129`, plus this block:
   - `corpus/SOURCES.md:453`: "Round 43: one row added, S159 (Wikipedia, Mutation testing) ... The Stryker equivalent-mutants document was NOT added: the census W04 warning showed S089 already holds that URL, so this round re-opened S089 and cites it instead".
   - `corpus/SOURCES.md:456`: "Next unused id: S160."
3. The consumer note agrees with the tree, not the item — `corpus/knowledge/r43-survivor-resolution-rule.md:3`:
   > `source: S089 (held, re-opened), S159 (new); S155 (held), S158 (held)`

Counts: HEAD `17f6ef0` = **113** registry rows, max id **S158** (`grep -cE '^\| S[0-9]{3} \|'`;
`grep -oE '^\| S[0-9]{3}' | tail -3` → S156 S157 S158). Either labeling lands at **115** rows.

**Landable labeling** (only id cell changes; every other cell identical to §2):

- Stryker anchor-extension row: id cell `S160`; every other cell exactly as §2 row 1.
- Wikipedia row: id cell `S159`; every other cell exactly as §2 row 2.

(No truncated row is reproduced here on purpose: a partially written `| S### |` line is an
`E01` failure if pasted, so the id swap is stated in prose and the full rows live in §2 only.)

The Wikipedia row is already appended as S159, so the only free id for the Stryker
anchor extension is S160. If the judge instead prefers the item's literal numbering, the
already-appended Wikipedia row must be renumbered — a registry edit this seat may not make.

Contract reading for the Stryker row: because the scope differs from S089's, a second row
for the same URL is **W04 (warning, exit 0), not E04** — E04 needs same URL *and* same scope
with no "supersedes S###" in `teaches` (`scripts/sources-census.sh:644-649`). The row is
therefore legal; it is also redundant next to re-opening S089, which is what the tree chose.
My draft marks the dependency in both cells (`scope` and `teaches` say "supersedes S089").

## 4. Gates run (all read-only)

Scratch trees: `/tmp/tameshi-r43-ScribeRows-validate/{A2,B2}`, each `corpus/SOURCES.md` plus
symlinks to the lane's real `corpus/knowledge`, `corpus/lessons`, `tools` so `E11` resolves
against real used-by targets (`--file` derives its root from the file's parent,
`scripts/sources-census.sh:498-504`).

1. **Variant A2** — freeze-rev registry (`git show HEAD:corpus/SOURCES.md`) + the two rows at
   the item's literal ids. Validator:
   ```
   ./scripts/sources-census.sh validate --file /tmp/tameshi-r43-ScribeRows-validate/A2/corpus/SOURCES.md
   file	W04	S159 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
   file	ok	/tmp/tameshi-r43-ScribeRows-validate/A2/corpus/SOURCES.md
   exit=0
   ```
   Code tally: `1 ok, 1 W01, 10 W04`, **zero E codes**. 9 W04 are pre-existing (S047 S048 S075
   S076 S077 S078 S081 S092 S104, identical to the live baseline run below); the 10th is mine.
2. **Variant B2** — working tree + the Stryker row as S160: `exit=0`, `W04 S160 duplicate url
   stryker-mutator.io/...`, `1 ok, 1 W01, 10 W04`, zero E codes.
3. **Live baseline** (`./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`)
   → `exit=0`, 9 W04 + 1 W01, `ok` on the lane registry; 113 rows at HEAD.
4. **Row census** on A2 and B2: `rows 115` each; `tier.A 103 tier.B 9 tier.C 3`, `status.mined 87
   status.queued 22 status.rejected 6`, `FLEET.missing 0`.
5. **Quote-in-snapshot** (criterion 79 style): 10/10 quotes found in stripped snapshot text
   (`quote_in_snapshot=1` each); two negative controls a tampered quote must fail:
   `negative_control_stryker=0`, `negative_control_wiki=0` (expected 0).
   `wiki_revid_present=1`; `stryker bytes=38687`, `wiki bytes=170793`.
6. **Note-claim check** (supports `r43-survivor-resolution-rule.md:30-32`): the Wikipedia page
   uses `survivor` 0, `unkilled` 0, `unreachable` 0 times; line 741 names dead code as *one way
   a mutant can be valid* (i.e. fault-free), so the page does **not** separate the lane's D from
   its E — the note's claim holds against the bytes.

## 5. Touched surfaces / out of scope

- Wrote **only** this file. `corpus/SOURCES.md` not edited; no `corpus/knowledge/*` or
  `corpus/lessons/*` edit; no git/jj mutation (reads only: `git ls-files`, `git status`,
  `git show HEAD:…`, `git rev-parse`); no counter run (C1/C2/C3 untouched); `tools/staged-id-guard.py`
  not executed; assimilation package read only (`merge/tameshi/SOURCES.append.md:13-14`, where
  `staged:S159`/`S160` are the two PIT pages already held here as S155/S156 — so those staged
  rows dedupe by document and supply no id for either new document).
- Scratch `/tmp/tameshi-r43-ScribeRows-*` deleted after the receipts above were captured.
- Tooling: nothing installed or upgraded.

## 6. Findings and limits

- **F1 (conflict, verbatim above).** The item names S159 = Stryker, but S089 held that
  document since 2026-10-22 and the working tree has already appended S159 = Wikipedia. The
  report supplies both labelings so the judge can rule; this seat did not renumber anything.
- **F2.** The working-tree Wikipedia row (`corpus/SOURCES.md:129`) is materially weaker than
  the source: it cites only `mw-Q`/`mw-w` and so cannot support a dead-code survivor class;
  the passage that does — `§Overview` line 741, "can also indicate that the mutation introduces
  no faults" + `"dead code" that is never executed` — is omitted. Its `teaches` also says
  "primary obstacle" where the page says "one of the biggest obstacles". My draft supplies the
  missing anchor and keeps the page's own wording.
- **F3 (defect in the tree's prose).** `corpus/SOURCES.md:453` calls the round-43 snapshots
  "a committed snapshot", but at the freeze rev they are untracked: `git status --porcelain`
  → `?? .ufo/evidence/round-43/sources/`, and `git ls-files .ufo/evidence/round-43/sources`
  → empty. Criterion 79 (`corpus/QUALITY.md:944-950`) is therefore **unmet** for both rows
  until the appending seat commits both snapshots (38687 B / 170793 B) in the same commit.
- **F4 (E11 risk).** `used-by corpus/knowledge/r43-survivor-resolution-rule.md` also exists
  only as `??` at the freeze rev; at `REV=17f6ef0` the append raises `E11` for both rows. The
  note must land in the same commit (`scripts/sources-census.sh:561-567`).
- **F5 (limits).** I did not refetch either URL, so this report says nothing about live drift;
  I did not verify the Docusaurus build id; I did not run the guard, the counters, or any
  mutation battery; and the `supersedes S089` reading is the census contract's (E04 escape +
  W04 warning), not a lane ruling on whether an anchor-extension row is worth its row count.
- **F6 (what the appending seat still owes, not done here).** Row count line (113 → 115, or
  114 → 115 if only the Stryker row lands), the round-43 block at `:453-456`, `Next unused id:
  S161`, the `## Id allocation` entry for the new ids, and the commit of
  `.ufo/evidence/round-43/sources/` + `corpus/knowledge/r43-survivor-resolution-rule.md`.
