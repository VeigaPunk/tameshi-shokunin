# Round 87 — successor counters, frozen before the after-state

Lane author TameshiR87 (attempt 1), 2026-11-05. Base `4a079f6ab57ab2f47b9e502a35eca75ec180cda7`
(round-86 tip). Pre-freeze instruments `a3b4f75d` (counter, census v2, controls, receipts) and
`38c83698` (v2-schema overreach manifest). Freeze `1d5102a1` (`plans/round-87.plan.md`). One
validated v1 wave `r87-w1`, 10 seats. `LOG.md` round 87 is the landing record.

## Gate

Candidates considered:

1. R87-C1 — a successor certification counter for `tools/design-blob-audit.py` that closes the
   round-86 counterfeit classes (path labels, worktree on the candidate, `rstrip` tolerance,
   PATH-inherited git). Admitted as a frozen claim, operability, capability acquisition.
2. R87-C2 — census v2 refuses overreach: tree, symlink, `path:line`, uncited and bare-directory
   pins, with manifest and self-state read from git at the revision. Admitted as a frozen claim,
   calibration (overreach caught; the real 30-row population must stay bound).
3. `considerthese/2026-10-28.md` ideas 1, 2, 3 and 5 — already implemented by committed tools
   (`quoted-line-exists.py`, `arm-liveness.py`, `rekey-cost.py`, `pointer-recheck.py`); not taken.
   Idea 4 (assimilation backlog burn-down) — out of claim scope; refused for this round.
4. Calibration on the round-86 LOG quotes — `quoted-line-exists.py` reports 16 unbacked quotes
   in LOG.md across old rounds (append-only history) and 2 in `corpus/lessons/round-86.md`
   (`resolved=0/2` cited to no receipt; `rows=len(rows)` is code, not a counter line). Refused as
   the round's claim: the LOG population is old append-only history that cannot be honestly moved
   to zero, and a 2-quote claim is bookkeeping. Named as open debt.

Sources opened this round (re-opened for R87-C1; the Gate records URL, access date and located quote):

- **S289** — Git, git-cat-file documentation — `https://git-scm.com/docs/git-cat-file`. Access date
  2026-11-05 (HTTP date `Thu, 05 Nov 2026 07:38:31 GMT`, 79360 B, sha256
  `91180e9f7199b73531900776d4d4adc17b5413f26f7c6a7e2420eb34412d8be7`, snapshot
  `.ufo/evidence/round-87/sources/s289-cat-file.html`). Located quote (snapshot line 2205, 18 words,
  DESCRIPTION): "Output the contents or other properties such as size, type or delta information of one or more objects."
  Grounds R87-C1's expected rows, which read blob contents with `git cat-file blob`.
- **S299** — Python, `shutil` documentation — `https://docs.python.org/3/library/shutil.html`. Access
  date 2026-11-05 (HTTP date `Thu, 05 Nov 2026 07:38:31 GMT`, 120949 B, sha256
  `28dd43b234cad3fbc6dc5dbed2aa971e15398d4e49e0c3f0174c4a364ca88b18`, snapshot
  `.ufo/evidence/round-87/sources/s299-shutil.html`). Located quote (snapshot line 667, 16 words,
  `shutil.which`): "Return the path to an executable which would be run if the given cmd was called."
  Grounds R87-C1's trusted-git resolution (`shutil.which` with `/usr/bin:/bin`, never the caller PATH).

Admitted: the S289 and S299 re-opens as the cited grounds for the two R87-C1 mechanisms above. No
`knowledge/` entry is admitted this round; expansion is not claimed.
Rejected: none new. No new row was appended (the `git-cat-file` and `shutil` URLs are already held).

Spot-check: pending the non-author closure. The round's own wave seats are the lane (LEARNING.md),
so they do not count as the outside check.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | fixture-shape drift: a selftest fixture tracked no directory (git does not track empty directories) and an arm's path sat inside a cited directory token, so two arms failed for fixture reasons, not for the rule they name | `.ufo/evidence/round-87/mistakes/M1-red-selftest.txt` (13/15, `uncited-pin-refused` and `tree-pin-refused` FAIL) against `.ufo/evidence/round-87/mistakes/green-selftest.txt` (15/15) | none — round-86's census selftest had no tracked-tree arm | a tracked file under the subdirectory; the uncited arm uses a path outside every cited token; each arm asserts its reason token. Shown able to fail: the red file above |
| M2 | pin binding by object type: `git cat-file -t` reports a symlink's blob as `blob`, so a symlink named by a row binds. Round-86's census used `git cat-file -e` (any object), the same gap in a different form | `.ufo/evidence/round-87/mistakes/M2-red-selftest.txt`: `symlink-pin-refused` FAIL with `bound=yes`; `tree-pin-refused` FAIL | partly: QUALITY criterion 85 covers receipt files, not census pins | mode-aware tree listing: a pin binds only a regular blob entry (100644/100755); a tree prefix is refused as `not-blob:tree`; a symlink as `not-regular:120000`; the symlink arm is added. Shown able to fail: the red file above |
| M3 | schema-tag drift in a copied population: the overreach manifest copied from round 86 kept the v1 schema tag, so census v2 refused it as a setup error and no before→after pair existed on identical rows | `.ufo/evidence/round-87/pre-freeze/c2/v2-overreach-schema-refusal.txt` (`setup refusal manifest-schema:'tameshi-capability-census-v1'`, exit 2) → commit `38c83698` | none | a derived copy with only the schema field changed; the 30 rows are identical (`r86-cited-tree-manifest-v2schema.json`); both files committed |
| M4 | inherited from round-86 closure defect 3: the S305 round-86 note carried a fetch instant (`00:41:59 GMT`) that contradicts its own header (`00:45:18 GMT`) | `.ufo/evidence/round-86/sources/s305.headers`; `corpus/SOURCES.md` round-86 note | none | appended correction line in `corpus/SOURCES.md` (append-only); the row and sha256 stand |
| M5 | inherited from round-86 M3: a certification counter's arm classes were disclosed by path labels, and its fixture worktree coincided with the candidate tree | `.ufo/evidence/round-86/attacks/c1-label-worktree-oracle.out` (8/8 for a counterfeit) | QUALITY criterion 111 (cheat family) — did not model a label-plus-worktree oracle | this round's counter uses opaque per-run labels and forces the worktree to the receipt revision; the counterfeit control `ctl-att3b-label-worktree` scores 0/8 and `ctl-cn1-oracle-worktree` 1/8 at `a3b4f75d` (`.ufo/evidence/round-87/pre-freeze/c1/`) |
| M6 | pre-freeze control set omitted two counterfeit classes the wave then found: a population read from the fixture worktree (`cf-c`, 8/8) and a committed-diff oracle (`cf-d`, 8/8). The fixture also commits the declared bytes at design_base, contrary to the receipt marker `uncommitted at design_base`, so no control could test the real premise | `.ufo/waves/round-87/w1/T87E1.md` (kill candidates `cf-c`, `cf-d`; extra check: `cf-a` `different` against `cf-d` `carried` on a premise-faithful fixture) | none: criterion 132 was drafted after the freeze; criterion 111 does not model either class | successor freeze: premise-faithful fixture (declared bytes absent at design_base), worktree-population and diff-oracle controls committed before freezing. Shown able to fail: the premise-faithful extra check separates `cf-a` from `cf-d` |
| M7 | a reviewer finding graded `note` was the kill. `parse_rows` absorbs post-table prose into the last row's citation text, so a pin named only in that prose binds | `.ufo/evidence/round-87/kill-c2/probe-prose-absorbed.txt` (`selftest-text pin … bound=yes reason=pin:tools/selfstate-freshness.json@d10a9c66d618`, exit 0, 30/30 bound on the real rows); `control-prose-path-removed.txt` (same manifest, path removed from the prose: `pin-not-cited`, 29/30); `.ufo/waves/round-87/w1/T87R1.md` finding C4; `T87E3.md` | none: the reviewer saw the absorption and no selftest or population arm exercised it | successor parser ends a row at the table's end (first non-table line) and an arm binds a prose-cited uncited pin as refused. Shown able to fail: the probe/control pair flips on exactly the prose path |
| M8 | the frozen census docstring describes checks the code does not make: a `git cat-file -t` pin check (code: ls-tree mode and type), exact-token citation only (code: directory-token and whole-word forms), and `shutil.which("git")` (code: trusted directories `/usr/bin:/bin`) | `tools/capability-census-v2.py` lines 14–29 at 1d5102a1 against `pin_state`, `is_cited` and `resolve_git`; `.ufo/waves/round-87/w1/T87CN1.md` overlap line; `T87R1.md` finding C1 | none: no criterion ties a self-description to the code it describes | not amended (frozen bytes). Successor docstring matches the code, and a docstring-versus-code row is counted in the successor |
| M9 | the census selftest is weak: 7 of 20 single-edit mutants survive its 15 arms (C03, C05, C12, C17, C18, C19, C20). C12 is caught only by the real population (20/30 bound) | `.ufo/waves/round-87/w1/T87M1.md` census table | none | successor selftest gains an arm for each survivor, including the M7 prose arm |

## Verdicts — both frozen claims killed (honest stop)

| claim | axis | verdict | evidence |
|---|---|---|---|
| R87-C1 | operability (capability acquisition) | **killed.** Three non-correct counterfeits reach `passed=8/8`: `cf-c` (population from the fixture worktree, `.ufo/waves/round-87/w1/T87E1.md`), `cf-d` (committed-diff oracle, same file), and `cf-oid` (object-id equality; wrong `carried` on a well-formed wrong sha, `T87C1.md` A2). Frozen counter and controls untouched. A correct git-backed counterfeit (`cf-a`) also reaches 8/8 and is not a kill | `T87E1.md`, `T87C1.md`, `.ufo/evidence/round-87/measure.py` (frozen) |
| R87-C2 | calibration (lowest scored axis) | **killed.** The frozen overreach population is refused (`bound=0`, predicate (b) met), and the real population stays bound (`30/30`, predicate (a) met). The kill rule still fires: a pin to a file no row cites, `tools/selfstate-freshness.json`, is bound through prose absorbed into the last table row (`selftest-text pin`). A causal control removes only that prose path and flips the row to `pin-not-cited` | `.ufo/evidence/round-87/kill-c2/`, `.ufo/waves/round-87/w1/T87E3.md` |

Admission: none. No capability row enters `SCORECARD.md` `## Capabilities` (C1 is not verified). Scores unchanged: depth 10, calibration 8, freshness 9.

## Routed to round 88 (successors; each needs its own freeze)

1. R87-C1 successor: premise-faithful fixture (declared bytes absent at design_base); committed controls for `cf-c`, `cf-d` and `cf-oid`; a case with a 64-hex sha that differs from the blob (expect `different`); a per-blob worktree-difference assertion (R1 M2). Kill rule unchanged.
2. Census v3: a row ends at the first non-table line (M7); arms for prose-absorbed pins and for mutants C03, C05, C17, C18, C19, C20 (M9); docstring equals code (M8); exit 2 for non-dict manifest or self-state (R1 C7); the `live` branch's id check and the `None`-id hole (R1 C2) closed; the `empty-table-cell` token reachable (R1 C6).
3. Calibration counter: count docstring-versus-code mismatches as the lane's self-description (M8), and count live rows whose figures do not match at REV (T87C1 C2e: an overreach manifest with `live` relabels binds 18/30).


## Source curation delta

- `S289` `used-by` old → new: `corpus/knowledge/executor-source-binding.md, corpus/lessons/round-61.md, corpus/lessons/round-64.md, corpus/lessons/round-79.md, corpus/lessons/round-80.md, corpus/lessons/round-81.md, corpus/lessons/round-82.md, corpus/lessons/round-83.md, corpus/lessons/round-85.md` → the same plus `corpus/lessons/round-87.md`. Status `mined` → `mined`; recheck `180d` → `180d`; `opened` `2026-10-30` unchanged (re-open date recorded in the Gate above).
- `S299` `used-by` old → new: `corpus/lessons/round-68.md` → `corpus/lessons/round-68.md, corpus/lessons/round-87.md`. Status `mined` → `mined`; recheck `365d` → `365d`.
- Round-86 note correction (append-only, `corpus/SOURCES.md`): fetch instant corrected to the header's `Thu, 05 Nov 2026 00:45:18 GMT`.
- Registry rows `171` → `171`. Tier histogram unchanged. Next unused id `S312`.
- Census: before `sources-census.sh validate --root … tameshi` exit 0 (`.ufo/evidence/round-87/census-before.txt`, warnings W01/W04 retained); mid-round exit 1 with E11 only while this lesson did not yet exist (the `used-by` paths must resolve); final exit recorded in the report.

## Learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | No `knowledge/` entry, no capability row, no frontier move; SOURCES rows 171 → 171 (`sources-census.sh validate` exit 0 before and after). |
| quality | unchanged | No admitted entry changed. Both successor instruments were killed by their own rules, and the rules now carry criteria 132–133. |
| discernment | unchanged | The gate froze two claims whose kill classes the wave then found (M6, M7), the same pattern as round 86 (kill by wave, not by the freeze gate). A reviewer finding was graded `note` and was the kill (M7). No claim was admitted wrongly, so the trend is unchanged and not improved. The operator may rule `harmed` on the M7 grading miss. |
