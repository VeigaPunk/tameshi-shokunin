# SourceCensus — round24 `corpus/SOURCES.md` rows S084/S085 (static census, w1)

Target: `corpus/SOURCES.md` at c8c5b88c8e961a929cdc351b95a7074c76958909, diff range
6a1821a8897eea6e7d9669292160ec9593669409..c8c5b88. Read-only; no network fetch, no installs, no
git/jj writes.

## Verdict

**PASS on all four named checks; no defect found.** Rows S084 (`:93`) and S085 (`:94`) each carry 11
cells, use in-vocabulary kind/tier/status values with an allowed `opened`/`recheck`, both `used-by`
paths resolve and actually cite the rows, and no pre-existing row changed: the only commit touching
the file in range is d2eaecd with `9 0` numstat, and the 81 base rows are byte-identical to the
delivered rows minus S084/S085. Two inherited cosmetic nits and two residual unknowns are recorded
below; neither is a defect in these rows.

## Check results (worktree == c8c5b88; blob sha256 `20119ebbc1f153c93ee5338c0072b731a07d3ef3ac633b72c6890c5089a7c2b9`)

| # | Check | Result | Evidence |
|---|---|---|---|
| C1 | 11 cells per new row | HOLDS | `awk -F'\|' 'NR==93\|\|NR==94{print NR": NF="NF}'` → `93: NF=13`, `94: NF=13` (12 pipes = 11 cells); table header `corpus/SOURCES.md:10` declares exactly 11 columns. Whole-file sweep `NF!=13` → empty for all 83 rows. |
| C2 | Allowed kind/tier/status (+opened/recheck) | HOLDS | S084 `kind=docs tier=A status=mined opened=2026-10-21 recheck=on-release`; S085 `kind=own-work tier=A status=mined opened=2026-10-21 recheck=on-change`. Vocabulary from the frozen contract as quoted at `.ufo/waves/round-12/w1/RegistryReview.md:5-14` (status ∈ queued\|mined\|rejected) and the validator command `.ufo/waves/kaika-w3/mori-critic.md:12` (kind ∈ spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work, tier ∈ A\|B\|C). Whole-file sweep: duplicate ids → empty, out-of-enum kind/tier/status → empty, non-13-field rows → empty. |
| C3 | Existing `used-by` paths | HOLDS | Both rows: `corpus/knowledge/replay-projection-hardening.md, corpus/lessons/round-24.md` — both exist (3453 B / 2724 B, mtimes 2026-10-21), repo-relative, no absolute/`home/`/`tmp/` paths anywhere in any `used-by` cell. The knowledge file's header `replay-projection-hardening.md:1` carries `source: S085 — …@6a1821a…:53-104 (routed defects); S084 — https://docs.python.org/3/library/os.path.html#os.path.realpath`; the lesson opens both rows at `round-24.md:31-37` / `:38-41` under `## Gate` (`:15`) with access date and located quotes (S084 16 words, S085 15 words, both ≤25). Whole-file mined sweep: no `mined` row lacks an existing `used-by` path. |
| C4 | No existing row changed base→delivered | HOLDS | `git diff --numstat 6a1821a c8c5b88 -- corpus/SOURCES.md` → `9 0`; `git log 6a1821a..c8c5b88 -- corpus/SOURCES.md` → exactly one commit, d2eaecd, also `9 0`. Independent proof: `git show 6a1821a:corpus/SOURCES.md \| grep '^| S'` = 81 rows; delivered rows minus `^| S084 / ^| S085` diffed against it → no output (byte-identical, same order). Deleted-line grep over the raw diff → none. |

Supporting consistency (same commands, all observed):

- IDs strictly ascending, no duplicates, 83 rows; `Next unused id: S086` (`:307`) is the successor of
  the highest id S085. The earlier `Next unused id: S084` (`:300`, pre-existing at base) is part of
  the file's append-only "next unused" convention (`:258` records that convention).
- S085's anchor claim `routed_not_executed lines53–104` resolves exactly: the array opens at
  `.ufo/waves/round-23/fresh-adjudication.json:48` and closes at `:105`; the eight `defect` strings
  sit at `:53, :59, :66, :74, :81, :87, :93, :104`. JSON parses; `len(routed_not_executed) == 8`.
- The lesson's S085 located quote is a verbatim substring of `fresh-adjudication.json:66`
  ("…do not pin bundle_sha256 literals, so a regenerated bundle and expected pair would still
  hold.").
- New lines carry no trailing whitespace/CR; file ends with `\n`; the worktree blob equals the
  c8c5b88 blob (sha256 above).

## Counterexamples attempted (fresh falsification)

Attacked what could falsify each check, not just re-read the rows: a literal `|` inside a cell would
inflate NF to 14 (none in any row); a silent rewrite/retrofit of an existing row would produce a
deleted line in `git diff` (zero); a duplicated or retired-id reuse would appear in the dup sweep
(none; S038–S039 are the only retired ids); a `mined` row pointing at a nonexistent or
absolute-path `used-by` would appear in the path sweep (none); a status outside the vocabulary would
appear in the enum sweep (none); an intermediate flip-and-revert would show as a second commit
touching SOURCES (only d2eaecd).

## Nits (inherited, not defects — do not fix in this wave)

- N1: glued tokens `revision6a1821a…` in S085's anchor cell (`:94`) repeat the S082/S083 house form
  (`revision51d49d58…`, `revision28cae179…`); `rowS083` at `:298` is the same style.
- N2: S085's range starts at `:53` (first `defect` string), not `:48` (array opening); the range
  therefore covers exactly the eight defect strings, which matches the row's title "routed critic
  defects".

## Residual unknowns

- U1: `SOURCES-CONTRACT-v1.md` is still not present in the repo (`corpus/SOURCES.md:4` names it bare;
  `find`/glob over the lane finds no such file; `.ufo/waves/round-12/w1/RegistryReview.md:67` R6
  recorded the same). The enum check above therefore rests on the contract rules quoted in round-12
  plus the validator command used by kaika-w3, not on the contract artifact itself. If the frozen
  contract's `kind` list differs, only C2's kind test is affected — and `docs`/`own-work` are
  long-standing values in this file (30 `docs` rows, 6 `own-work` rows, all A tier).
- U2: S084's external quote and the "non-strict mode may still leave links or loops" wording were not
  verified against docs.python.org in this seat (static census, no fetch). Its URL and `#os.path.realpath`
  anchor in the knowledge header are well-formed; S085's quote was verified in-tree as above.

## Smallest safe correction

None needed for S084/S085 — leave both rows untouched. If the lane wants the contract resolvable,
the minimal change is outside this row set: restore or repoint `SOURCES-CONTRACT-v1.md` (the pointer
at `corpus/SOURCES.md:4`), which is a documentation fix, not a registry edit.

## Commands run (read-only, `GIT_OPTIONAL_LOCKS=0`)

```
git diff --numstat 6a1821a..c8c5b88 -- corpus/SOURCES.md        -> 9  0
git log --format='%h %s' 6a1821a..c8c5b88 -- corpus/SOURCES.md  -> d2eaecd (only)
git show 6a1821a:corpus/SOURCES.md | grep '^| S' | wc -l        -> 81
diff <base rows> <delivered rows minus S084/S085>               -> empty
awk -F'|' 'NR==93||NR==94{print NR": NF="NF}'                   -> 13, 13
awk enum/tier/status sweep + duplicate-id sweep                 -> empty
mined-row used-by path existence loop                           -> no MISSING / NO-EXISTING
python3 -c json.load(fresh-adjudication.json)                   -> 8 routed entries
sha256sum corpus/SOURCES.md vs git show c8c5b88:corpus/SOURCES.md -> identical
```

Tooling: nothing installed or upgraded; no network fetch; no writes outside this report.
