# ScribeScorecard — round-41 SCORECARD draft + number audit

Seat: L1Tameshi41.ScribeScorecard (scribe, axis calibration).
Read-only on the lane; the only lane write is this report. Scratch:
`/tmp/tameshi-r41-scribe-scorecard/` (tree, tree-final, tree-b2, tree-final-107, block.md, block2.md).
No tool installed or upgraded: the task needed none (pacman untouched, no network fetch).

State observed: tip `b37ce97` ("round-41: C1 records reconciliation + C2 write-path-census-v3"),
deciding receipts already written at `.ufo/evidence/round-41/after/` (mtime 03:46, **untracked**),
`SCORECARD.md` 1946 lines with a live round-41 block at `:1895-1946`, and the worktree still
dirty (`SCORECARD.md`, `corpus/SOURCES.md`, `corpus/lessons/round-41.md`, `contract.json`).

**Closed by later landings — see "Closure" at the end.** The findings below are the state at
`b37ce97`; F1 (C1 false on m8) and F4 (stale C1 pin) were both repaired at `2ae00eb`/`0c8e1be`,
and the tip when this note was added is `812ee0d`.

## Findings, in severity order

### F1. The decision is already made, and C1 failed — on one m8 mismatch

    .ufo/evidence/round-41/after/c1-at-b37ce974b6efb8c465626d7346149549a3300a4b.stdout
    MISMATCH m8 .ufo/waves/round-41/w1/swarm-registry.json cited but does not resolve at b37ce974b6efb8c465626d7346149549a3300a4b
    C1_R41: m6=0 m7=0 m8=1 m9=0 total=1 records=3 sources_rows=109 rev=b37ce974b6efb8c465626d7346149549a3300a4b C1_R41_PASS=false
    (exit file: 1)

Cause: `LOG.md:2149` cites `.ufo/waves/round-41/w1/swarm-registry.json`, which is **not in the
landing commit** (`git ls-tree -r --name-only b37ce97 -- .ufo/waves/round-41/` lists only
`assimilation/{collisions,reg-ids,staged-ids}`, `dispatch-w1.json`, `spec-w1.json`; the `w1/`
directory is `??`). `LOG.md:2111` is the round-41 section header, and
`grep -c "swarm-registry.json" corpus/lessons/round-41.md SCORECARD.md` → 0, 0, so the LOG is the
only citing record. m6 and m9 are cleared; the residue is a commit, not a record edit. Rev mode
resolves with `git cat-file -e <rev>:<path>`
(`.ufo/evidence/round-41/calibration/measure.py:111-116`), so the fix is committing **the file** —
a committed directory is not enough.

C2 passed on the same run:

    .ufo/evidence/round-41/after/c2-at-b37ce974b6efb8c465626d7346149549a3300a4b.stdout
    C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1 var_expected=1
    symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=0
    v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=811 live_var_resolved_v3=1
    live_var_scratch_v3=1 live_var_sites_v2=1 live_var_expected_v2=0 live_symlink_lineno=820
    live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0
    mutant_resolve_killed=1 mutant_symlink_killed=1 mutant_symlink_arg_killed=1
    rev=b37ce974… C2_R41_PASS=true      (exit file: 0)

The live block at `SCORECARD.md:1910` meanwhile reads C1 **"improved (measured)"**
(`awk 'NR==1910{...}'` → verdict cell ` improved (measured) `). Record and receipt contradict
each other inside one file: the receipt says `C1_R41_PASS=false`, `total=1`.

### F2. Numeric calibration is 6, not 8 — at base and at the landing commit

`SCORECARD.md:1537` defines the calibration score as the strict cold-read monitor's
`calibration_restraint_score`. Run now (58 s each, `--repo` the lane):

    python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046
    python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev b37ce974b6efb8c465626d7346149549a3300a4b

Both print `"calibration_restraint_score": 6`, `"box3_full_page": false`,
`"shonen": {"boxes": 4, "checked": 0, "asserted": 4, "box3_points": false, "marks": ["~","~","~","~"]}`.
So the block must read **calibration 6 → 6**, not 8 → 8. Command C's
`asserted_mark_upper_bound=8` is labelled at `SCORECARD.md:74` "mark census only; … awards no
evidence/authority credit", and box 3's two points need `box3_full_page`, which is false.
Seat `ReviewScorecardNumbers` reached the same conclusion independently and measured 6 at `5641ed84`
(round-40's measured commit) and at `e118024`, with 8 only at `ae9b771` and in
`.ufo/evidence/round-36/after/monitor-at-b455001e.stdout:2`. The `8` in the round-32 (`:1598`),
round-39 (`:1864`, measured `233077f8`), round-40 (`:1891`, measured `5641ed84`) and round-41
(`:1926`) rows is not reproduced at the revisions measured here; recorded here as 6, not
re-adjudicated. The contract's "calibration (8) is the lowest non-retired axis" changes
number only — calibration is still the lowest axis, so the C1 axis choice stands.

### F3. The brief's "107 rows" is the base/freeze count; the round-41 registry holds 109

    base   a3d6c69: 107 rows — 79 mined / 22 queued / 6 rejected — max id S152
    freeze d4ee4e6: 107 rows — 79 mined / 22 queued / 6 rejected — max id S152
    landing b37ce97 + tree: 109 rows — 81 mined / 22 queued / 6 rejected — max id S154
    bash .ufo/evidence/kaika-round-1/sources-census-v2.sh → "== A rows 109",
      "mined=81 queued=22 rejected=6", SOURCES_CENSUS: CLEAN, exit 0

m6 compares the LAST `| sources-registry |` line's first `N rows` with the registry at the
measured revision. Restating to 107 makes C1 false, measured on a scratch copy of the live
tree with my block (`/tmp/tameshi-r41-scribe-scorecard/tree-final-107`):

    MISMATCH m6 SCORECARD standing row says 107 rows, SOURCES.md has 109
    C1_R41: m6=1 m7=0 m8=0 m9=0 total=1 records=3 sources_rows=109 C1_R41_PASS=false   exit 1

Same tree at 109: `C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 … C1_R41_PASS=true`, exit 0.
The live `:1851` row was meanwhile restated to 109 by another seat, so m6 is already cleared
at the landing commit — the draft keeps the restated row inside the round block so the number
travels with the claim.

### F4. The C1 counter pin is stale at the landing commit

    sha256sum .ufo/evidence/round-41/calibration/measure.py      → 9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd
    git show b37ce97:.ufo/evidence/round-41/calibration/measure.py | sha256sum → 9aaa99ac… (same)
    contract claims.C1.counter_sha256                            → 8bc9b4221c59c7b380892b7f97885e9b8ada1f5d82b0703effa166f0519ce11c
    contract amendments A4.new_sha256                           → 8bc9b422…

A4 recorded `8bc9b422…` as the re-pinned bytes, but the committed bytes are `9aaa99ac…`.
C1 does not self-verify its sha, so no predicate fails; the provenance claim does. C2's pins
match exactly (`83268eff…` counter, `20b6254d…` fixtures, `095924a7…` tool).

### F5. Untracked artifacts are a standing m8 hazard

`.ufo/waves/round-41/w1/` and `.ufo/evidence/round-41/after/` are untracked
(`git status --porcelain` → `?? .ufo/waves/round-41/w1/`, `?? .ufo/evidence/round-41/after/`).
Any record citing them fails m8 at a committed revision. This is F1's cause and also the
precondition for my draft (which cites the after receipts as its evidence): commit the
**individual files** — `w1/swarm-registry.json` and each cited `after/*.stdout` — before the
measured revision. Rev mode needs the file path in the tree, so committing a directory alone
does not clear m8.

### F6. m7 forbids staged ids in round-41 records; m9 needs the table's own words

- `S185`, `S189`, `S137` are not registry rows (`grep -cE '^\| S185 \|' corpus/SOURCES.md` → 0;
  same for S189 and S137). A lesson naming them yields
  `m7 … cited but absent from the registry` under both the pre-A1 and A1 blobs — measured on
  `/tmp/tameshi-r41-scribe-scorecard/tree-scite`: `m6=0 m7=3 … total=3` (A1 blob) and
  `… m7=5 … total=5` (pre-A1 blob). Told to `L1Tameshi41.ScribeLesson`; their draft carries no
  S-id literal (confirmed by them and by the green run).
- m9 derives the required words from the round-40 table (`.ufo/evidence/round-41/calibration/measure.py:246-260`):
  the lesson must contain `round-40`, `six refused` and `ten present`. The live lesson does.
- A1's bug is real: the pre-A1 blob reads `cells[9]` (the `opened` date) as status, so a record
  citing two mined ids yields four m7 mismatches (`m6=0 m7=4 … total=5`) on the same stub where
  the A1 blob gives `m7=0`.

### F7. C2 has no work mode

`python3 .ufo/evidence/round-41/census/measure.py --lane … --rev work` →
`C2_R41: tool_absent=1 … C2_R41_PASS=false`, exit 1: the counter resolves everything through
`git show`, and `git show work:…` fails. A pre-run C2 check needs a scratch git repo (as seat
`MutConstantClassifier` builds). Do not read that line as "tool absent at the measured revision".

### F8. `--rev work` green does not imply rev-mode green

Work mode resolves with `os.path.exists` (`.ufo/evidence/round-41/calibration/measure.py:113`);
a real revision needs the cited files committed. My scratch work-mode run is green while the
same text at `b37ce97` is red for exactly this reason (F1).

## The draft block (paste-ready; validated)

Replaces the live block if the L1 prefers a receipt-bearing form. It carries the two measured
cells from the L1's own receipts, the corrected calibration (6 → 6), and the 109-row standing
row. Precondition: `.ufo/evidence/round-41/after/` and `.ufo/waves/round-41/w1/` must be
committed in the measured revision (F5), otherwise the after-receipt citations themselves fail m8.

```markdown

## Round 41 — self-assessment reconciliation (calibration, C1) + variable-destination write census v3 (depth, C2) (2026-10-25)

L1 fresh L1, attempt 2 (attempt 1 died with the orchestrator; inherited state:
none — the lane was clean at attempt-2 start). Two claims, distinct axes.
Calibration is the lowest non-retired axis and carries C1. The stagnation
nudge does not fire: a capability entered the table at round 40, inside the
window N=2. Neither claim is exploratory. Contract
`.ufo/evidence/round-41/contract.json`, frozen before any seat scored and
before the deciding run (base `a3d6c690`, freeze `d4ee4e63`); its pre-data amendments
A1 (the m7 status column index), A2 (the symlink fixture root plus a third mutant),
A3 (a record rephrasing) and A4 (m8 work-mode directory resolution) are recorded there,
none after a deciding run. Numeric depth stays 9. Numeric calibration stays 6.

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 the lane's self-assessment records agree with observed repo state: the standing sources-registry count matches the registry, no round-41 record cites an unmined S-id or an unresolvable repo path, and the round-40 quarantine-summary contradiction is corrected in the round-41 lesson | calibration (lowest axis) | `C1_R41: m6=1 m7=0 m8=0 m9=1 total=2` at `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`, `C1_R41_PASS=false`, exit 1 — m6 the standing row said 103 vs 107 registry rows, m9 the round-40 summary said 7 refused / 9 present vs its table's 6 / 10 | `C1_R41: m6=0 m7=0 m8=1 m9=0 total=1 records=3 sources_rows=109` at `b37ce974b6efb8c465626d7346149549a3300a4b`, `C1_R41_PASS=false`, exit 1 — m6 and m9 cleared, and the single surviving mismatch is m8: `.ufo/waves/round-41/w1/swarm-registry.json` cited at LOG.md:2149 and not committed at the measured revision | two mismatches cleared, one remains; the residue is a commit, not a record edit | `python3 .ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV` | `b37ce974b6efb8c465626d7346149549a3300a4b` | before `.ufo/evidence/round-41/before/c1-at-base.stdout`, after `.ufo/evidence/round-41/after/c1-at-b37ce974b6efb8c465626d7346149549a3300a4b.stdout` | not met (measured false) |
| C2 `tools/write-path-census-v3.py` resolves a write destination held in a variable (`open`, `write_text`/`write_bytes`, `os.replace`/`os.rename`, the `os.symlink` destination) where v2 matches only a literal on the same line | depth (capability) | `C2_R41: tool_absent=1 var_expected=0 symlink_expected=0` at `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`, `C2_R41_PASS=false`, exit 1 | `C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1 var_expected=1 symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=0 v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=811 live_var_resolved_v3=1 live_var_scratch_v3=1 live_var_sites_v2=1 live_var_expected_v2=0 live_symlink_lineno=820 live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1 mutant_symlink_arg_killed=1` at `b37ce97`, `C2_R41_PASS=true`, exit 0 — the receipt additionally carries `live_var_sites_v2`, `live_var_lineno`, `live_symlink_lineno` and `rev`, which are outside the contract target; all 22 target fields are present with matching values | a resolution v2 cannot make, on two live sites (`tools/repeat-control.py:811` and `:820`), with v2 blind to both expected-value destinations; numeric depth stays 9 | `python3 .ufo/evidence/round-41/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV` | `b37ce974b6efb8c465626d7346149549a3300a4b` | before `.ufo/evidence/round-41/before/c2-at-base.stdout`, control `.ufo/evidence/round-41/control/c2-control.stdout`, after `.ufo/evidence/round-41/after/c2-at-b37ce974b6efb8c465626d7346149549a3300a4b.stdout`; tool sha256 `095924a7`, v2 pin `40228532` | improved (measured); the depth score does not move |

Do-nothing controls, receipted before the deciding run: C1 at `a3d6c690` is
`m6=1 m7=0 m8=0 m9=1 total=2` — an edit that touches neither the standing row nor
the round-40 correction cannot reach `total=0`. C2 at `a3d6c690` is
`tool_absent=1`. The embedded v2 patterns on the same planted fixtures are
`C2_R41_CONTROL: v2_var_expected=0 v2_symlink_sites=0`,
`C2_R41_CONTROL_PASS=false` — v2 resolves neither new planted class. The v3
selftest run from the lane root is
`WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`,
exit 0.

Numeric axes. **depth 9 → 9**: command D prints `recorded_cases=9 depth_score=9`
at `a3d6c690` and at `b37ce97`; round 41 adds no ledger leg. **calibration
6 → 6**: the strict cold-read monitor (`python3 .ufo/evidence/round-21/coldread/measure.py
--repo LANE --rev REV`) prints `calibration_restraint_score: 6` with
`box3_full_page=false` and `shonen.box3_points=false` at both `a3d6c690` and
`b37ce97`, on `shonen.boxes=4 checked=0 asserted=4`. Command C's
`asserted_mark_upper_bound=8` is a mark census only and awards no box-3 credit
(`SCORECARD.md:74`), so it is not the score. No axis harmed. The 8 recorded in the
round-36, round-37 and round-40 rows is not reproduced at either revision; it is
stated here as 6 and not re-adjudicated.

Capabilities table — row admitted this round:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| write-path-census-v3 | resolve a write destination held in a variable — `open`, `write_text`/`write_bytes`, `os.replace`/`os.rename` and the `os.symlink` destination — through assignment, `os.path.join`, `+`, `/` and f-strings to depth four, and classify the resolved text as an expected-value or scratch destination; v2 sees only a same-line literal | `.ufo/evidence/round-41/after/c2-at-b37ce974b6efb8c465626d7346149549a3300a4b.stdout` → `C2_R41_PASS=true`, exit 0; selftest `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`; `tools/write-path-census-v3.py` sha256 `095924a7` | round 41 |

Standing row, restated (the standing row this block supersedes said 103 rows):

| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; row count from the re-derivable command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 109 rows at round 41 (81 mined / 22 queued / 6 rejected; highest id 154, S-prefixed in the registry), re-derived 2026-10-25; the 107-row count held at the base and freeze revisions, before round 41 opened its two docs rows; `corpus/SOURCES.md` | fleet round 1 (kaika) |

**Planned (round 42):** carry the uncommitted wave artifacts into the measured
revision before any further C1 run — the m8 residue is a commit, not a text
change; the `cmp` and `git diff --exit-code` comparator lattices stay unmeasured;
v3's declared scope limit stands — aliases, closures over reassigned names,
attribute reassignment, conditional assignment and any path computed by a
non-folding call are not resolved.
```

Validation of the block above (work mode, scratch `/tmp/tameshi-r41-scribe-scorecard/tree-b2`
= live tree with the live block cut and this block appended, live lesson + live LOG, the
before/control/after receipts and `w1/swarm-registry.json` copied in):

    C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=work C1_R41_PASS=true   exit 0

Per-token citation audit of the block alone (work = present in the lane, landing = present in
`b37ce97`): every token resolves in work mode; the two `.ufo/evidence/round-41/after/*.stdout`
citations and the `w1/swarm-registry.json` mention resolve only in work mode — i.e. they need
the commits named in F5.

## Live-block defects (SCORECARD.md as observed; block at :1895-1946)

1. `:1910` — C1 verdict `improved (measured)` contradicts the after receipt at `b37ce97`
   (`C1_R41_PASS=false`, `total=1`). Must read `not met (measured false)`, or gain an after
   subsection whose line is the receipt.
2. `:1926` — "**calibration 8 → 8**" is not reproducible (F2: monitor prints 6 at both revs).
   The same unsupported 8 is inherited at `:1598` (round 32), `:1864` (round 39, measured
   `233077f8`), `:1891` (round 40, measured `5641ed84`) and `:1545`'s round-31 table row.
3. `:1900-1903` — "three pre-data amendments … (A1, A2, A3)": the contract carries **four**
   (`python3 -c "import json;print([a['id'] for a in json.load(open('.ufo/evidence/round-41/contract.json'))['amendments']])"`
   → `['A1','A2','A3','A4']`).
4. `:1909`, `:1910` — Measured commit cells still read "see the after subsection below"; no
   such subsection exists, and the after receipts are now available to cite by path.
5. `:1909` — the m7/m8 class descriptions are fine, but the C1 row should name the surviving
   class (m8) and its object, as in the draft, so the failure is legible in the table.

## Numbers re-checked (agree)

v3 `095924a7…`; v2 `40228532…`; C2 counter `83268eff…`; fixtures `20b6254d…`;
depth `recorded_cases=9 depth_score=9` at base and at `b37ce97` (command D);
`shonen.boxes=4 checked=0 asserted=4`, `asserted_mark_upper_bound=8` (command C, mark census only);
registry 109 at landing/tree (81/22/6, max id 154), 107 at base and freeze (79/22/6, max id S152).
Disagreeing with my draft's first version and corrected here: calibration 8 → 8 (F2).

## Behaviour / gates / touched surfaces

- Produced: this audit plus two block revisions; the paste-ready one is inlined above
  (`/tmp/tameshi-r41-scribe-scorecard/block2.md` is the same text).
- Gates exercised: C1 at the base rev and in work mode on scratch trees (labelled pre-run
  checks), C2 at the base rev, `--control`, v3 `--selftest`, `sources-census-v2.sh`, commands C
  and D at base and at `b37ce97`, the round-21 cold-read monitor at base and at `b37ce97`.
  **No deciding run of either counter was performed by this seat**; the deciding receipts are
  the L1's own, read from `.ufo/evidence/round-41/after/`.
- Touched surfaces: lane — this report only. No edit to `SCORECARD.md`, `LOG.md`, `corpus/`,
  `tools/`, the contract, the counters, the fixtures, the jj state or the Git index.
- Out of scope / not claimed: re-adjudicating the round-36/37/40 calibration rows; the C2
  mutant and challenger receipts (their seats own them); any commit, push or publish.

## Closure (added after the reviewer's re-check; tip `812ee0d`)

Every finding above was re-checked read-only at the tip. F1 and F4 are **closed**; F2 and F3
stand corrected in the landed record; F5–F8 are procedural notes with no live residue.

- **C1 is true at the measured revision.** `.ufo/evidence/round-41/after/c1-at-baa18b7b.stdout`
  (read by me at `812ee0d`) → `C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109
  rev=baa18b7bdd637ff175255e82b6bee3c85df0881e C1_R41_PASS=true`. The m8 object is committed:
  `git cat-file -e 812ee0d:.ufo/waves/round-41/w1/swarm-registry.json` → present (F1 closed; the
  fix was committing the file, as predicted).
- **The C1 pin now matches its bytes** (F4 closed): contract `claims.C1.counter_sha256` =
  `sha256sum` of the committed counter = `9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd`.
- **All five cited paths resolve at the tip** via `git cat-file -e 812ee0d:<path>`:
  `after/c1-at-baa18b7b.stdout` (`… PASS=true`), `after/c1-at-baa18b7b.exit` (`0`),
  `after/c2-at-baa18b7b.stdout`, `census/command-d.stdout`, `w1/swarm-registry.json`.
- **F2 is corroborated inside the lane's own receipt**:
  `.ufo/evidence/round-41/census/command-d.stdout` reads `recorded_cases=9 depth_score=9`,
  `boxes=4 checked=0 asserted=4 untouched=0`, `coldread score at a3d6c690 = 6`,
  `coldread score at b37ce974 = 6`.
- **Rows and verdicts:** the round-41 C1/C2 rows sit at `SCORECARD.md:1912` and `:1913` at the
  tip, and both verdicts are now measured-true (`improved (measured)` / `improved (capability)`);
  at `b37ce97` they were `:1909`/`:1910` with the C1 verdict contradicting its receipt.
- **Residual, cosmetic (no number error):** the After cells at `:1912`/`:1913` still print the
  literal `target …` string while the measured line lives in the after subsection. If the cell is
  meant to be the result, prefix it `measured:` with the receipt path; if it is meant to be the
  target, the wording is fine. The C1 receipt carries `records=3`, `sources_rows=109` and `rev=`
  beyond the target string; the C2 receipt was re-derived token-by-token against all 22 target
  fields by seat `ReviewScorecardNumbers` and matches.
- **Finding ids differ between the two reports.** In this report F1 is the C1 m8 failure and F4
  is the stale counter pin; in `ReviewScorecardNumbers` the calibration number is F1 and the pin
  is F5. The substance agrees finding for finding; compare by content, not by id.
- **One deciding run stands.** The measurement revision is `baa18b7b`: one default-mode run of
  each counter, per the contract's kill rule. Tip `812ee0d` was read here for receipts and path
  resolution only — it is **not** a second measurement, and nothing in this Closure should be
  read as one.
- **Attribution:** seat `ReviewScorecardNumbers` re-derived the same numbers independently at
  `2ae00eb` and closed their audit; they also re-ran the cold-read monitor at `812ee0d`, `2ae00eb`
  and `baa18b7b` and report `6` each time (60/64, `box3_full_page` false, `shonen.box3_points`
  false), and confirmed registry 109 / 81-22-6 / S154, depth 9, v2 `40228532…`, v3 `095924a7…`
  and `claims.C1.counter_sha256 = 9aaa99ac…`. Their addendum is
  `.ufo/waves/round-41/w1/ReviewScorecardNumbers.md`.

Report path: `.ufo/waves/round-41/w1/ScribeScorecard.md`
