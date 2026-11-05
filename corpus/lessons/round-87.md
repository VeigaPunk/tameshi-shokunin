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

## Source curation delta

- `S289` `used-by` old → new: `corpus/knowledge/executor-source-binding.md, corpus/lessons/round-61.md, corpus/lessons/round-64.md, corpus/lessons/round-79.md, corpus/lessons/round-80.md, corpus/lessons/round-81.md, corpus/lessons/round-82.md, corpus/lessons/round-83.md, corpus/lessons/round-85.md` → the same plus `corpus/lessons/round-87.md`. Status `mined` → `mined`; recheck `180d` → `180d`; `opened` `2026-10-30` unchanged (re-open date recorded in the Gate above).
- `S299` `used-by` old → new: `corpus/lessons/round-68.md` → `corpus/lessons/round-68.md, corpus/lessons/round-87.md`. Status `mined` → `mined`; recheck `365d` → `365d`.
- Round-86 note correction (append-only, `corpus/SOURCES.md`): fetch instant corrected to the header's `Thu, 05 Nov 2026 00:45:18 GMT`.
- Registry rows `171` → `171`. Tier histogram unchanged. Next unused id `S312`.
- Census: before `sources-census.sh validate --root … tameshi` exit 0 (`.ufo/evidence/round-87/census-before.txt`, warnings W01/W04 retained); mid-round exit 1 with E11 only while this lesson did not yet exist (the `used-by` paths must resolve); final exit recorded in the report.
