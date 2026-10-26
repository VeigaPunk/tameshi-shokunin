# T50ScribeAppendOnly — append-only rule for landed seat reports (QUALITY criterion 100)

Seat: `T50ScribeAppendOnly` (scribe, wave 1). Item: the ask recorded in SCORECARD
`**Planned (round 49), amended:**` — "an append-only rule for landed seat reports (round-47
conformance defect 2)" — routed as one key of compound item R48.4
(`.ufo/evidence/round-50/c1/defects.json`, `keys` includes `append-only rule`).

Deliverables (all mine, all under `.ufo/waves/round-50/w1/`):

- `T50ScribeAppendOnly.md` — this note: the criterion text, its motivation pointers, the falsifier spec.
- `T50ScribeAppendOnly.census.txt` — the independent pairwise census of rounds 43-50 (read-only git).
- `T50ScribeAppendOnly.tool-runs.txt` — five runs of the executor's checker on retained lane bytes,
  with its sha256 and true exit codes.

I did not edit `corpus/QUALITY.md`, any tool, counter, contract or control, and I made no git write;
the criterion below is for the L1 to append. No tool was installed or upgraded (pacman is paused;
nothing needed a package manager). Reading tip: `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`.

## 1. The criterion text (next free number: 100 — `corpus/QUALITY.md` ends at line 1464 with criterion 99)

The check sentence is written against the artifact the executor seat actually builds
(`.ufo/waves/round-50/w1/T50ExecAppendOnly/seat-report-append-only.py`, sha256 `cee1a2dddf6ed7a1…`,
7954 bytes), not against a proposed tool: a criterion that names a tool that does not exist cannot
pass criterion 97 at its own landing tip.

```markdown
### Criterion 100 — a landed wave artifact grows; it never changes

Every file under `.ufo/waves/round-<N>/` — a seat report, a wave spec, a dispatch list or a registry —
is append-only once committed. The comparison is the lane's checker
`.ufo/waves/round-50/w1/T50ExecAppendOnly/seat-report-append-only.py LANE FROM TO`: for every
`round-*/` path present at FROM, its bytes at TO must begin with its bytes at FROM; a path absent at TO
is `deleted`, a TO blob that does not begin with the FROM blob is `prefix-lost`, and a side that is not
a blob is `type-change`. Both sides are read as blobs (`git ls-tree -r -z`, `git cat-file --batch`),
never as decoded lines, so an edit inside one long line cannot hide behind an unchanged line count.
FROM is the commit that added each artifact (`git log --diff-filter=A --format=%H -1 -- <path>`), not
the round's base: a window that begins before the artifact exists leaves it unchecked, so its clean
answer is vacuous. TO is the round's landing tip. The append-only rule binds round 50 and later;
earlier rounds are measured, not repaired — all 22 consecutive-commit pairs on the 1165 wave files of
rounds 43-50 are non-prefix pairs, across 20 files (`.ufo/waves/round-50/w1/T50ScribeAppendOnly.census.txt`).
A correction to a landed artifact is appended at its end under a dated `## Erratum — YYYY-MM-DD` heading
naming the false text and its replacement (criterion 35's erratum form); the checker reads bytes only,
so the truth of an erratum stays a spot-check item.

Check that can fail: at closure, for each distinct adding commit `A` among the round's wave artifacts,
run `python3 .ufo/waves/round-50/w1/T50ExecAppendOnly/seat-report-append-only.py LANE A <landing tip>`.
The run fails on exit 1, with one `REWRITTEN<TAB><path><TAB><reason>` line per rewritten artifact and
`SUMMARY<TAB>checked=<n><TAB>rewritten=<m>`; it passes on exit 0 with `rewritten=0`; a setup refusal
(bad arguments, a non-repository LANE, an unresolvable revision, a git failure) is exit 2 with an
`ERROR: …` line on stderr — every nonzero exit classified, and `checked=0` is a refusal-shaped result,
not a pass. Each committed run names the FROM and TO it compared and the checker sha256, in the
receipt or in a sibling `.revs` beside it (`.ufo/waves/round-50/w1/T50ExecAppendOnly/receipts/00-toolchain.txt`
carries the sha of the bytes run). The discrimination is a pair of runs over one rewrite: `LANE 487b8f0 5891bdb` prints
`checked=2819 rewritten=0` and exits 0 although nine round-43 artifacts were rewritten inside that
window, while `LANE c5335c70 83beaf98` prints `checked=2856 rewritten=9` and exits 1 — the first is
vacuous for every artifact added after its FROM, which is why FROM is the adding commit
(`.ufo/waves/round-50/w1/T50ScribeAppendOnly.tool-runs.txt`). Out of scope, named: a rewrite committed
inside the artifact's own adding commit; a rewrite a later commit undoes (the comparison is net over the
window); an uncommitted worktree edit, which the closure's clean-tree check refuses before this one runs;
paths outside `.ufo/waves/round-*/`; and the truth of an appended erratum.

Lesson: `corpus/lessons/round-43-verifier-spotcheck.md:12` and `:64` (R43.2, routed at `506e99c7`): the
round-43 closure found the committed wave-1 note `.ufo/waves/round-43/w1/RevC2Classes.md` modified in
the worktree and called it "an unrelated dirty worktree change"; the edit was committed in round 44 as
`83beaf98`, and the adding-commit run `c5335c70 83beaf98` reports it `prefix-lost` along with eight
sibling reports. `corpus/lessons/round-47-verifier-spotcheck.md:22` (conformance defect 2): `03facb22`,
an orchestrator commit after the round's report, rewrote `.ufo/waves/round-47/w1/T47ConnCross.md`
(+228/-214), reported `prefix-lost` by `edd4ca44 03facb22`. Both were status-neutral because no rule
compared a wave artifact with its own earlier bytes; criterion 35 makes corrections append-only for
corpus prose and criterion 26 for a stale receipt line, and neither reads `.ufo/waves/`.

Falsifier that must fail: the checker's fixture driver
(`.ufo/waves/round-50/w1/T50ExecAppendOnly/receipts/fixture-driver.sh`, 11 cases) prints
`PASS` for every case and `FAIL` for none — append exit 0 with `SUMMARY checked=2 rewritten=0`, and
in-place, deleted, truncated and renamed each exit 1 naming the right path and reason, with the three
setup cases exit 2; the adding-commit runs `c5335c70 83beaf98`, `edd4ca44 03facb22`,
`6b5ea3b1 03facb22` and `9b9b2a01 fc5ac743` each exit 1 while the round-base run `487b8f0 5891bdb`
exits 0 with `rewritten=0`; and each of three staged checker mutants prints a `FAIL ` line under the
driver — prefix test replaced by `len(new) >= len(old)`, the `deleted` branch removed, scope widened
past `.ufo/waves/round-*/`; and the entry point
`.ufo/waves/round-50/w1/T50ExecAppendOnly/receipts/c100-falsifier.py` prints `CRITERION-100-FALSIFIER-OK`
and exits 0 (receipt `.ufo/waves/round-50/w1/T50ExecAppendOnly/receipts/quality/c100-falsifiers.stdout`).
```

## 2. Motivation pointers

| # | Pointer | What it shows | Command that shows it |
|---|---|---|---|
| 1 | `SCORECARD.md:2380` | the ask's own routing line: "an append-only rule for landed seat reports (round-47 conformance defect 2)" | `grep -n 'append-only rule for landed seat reports' SCORECARD.md` |
| 2 | `corpus/lessons/round-43-verifier-spotcheck.md:12` | conformance defect, status-neutral: `RevC2Classes.md` modified in the worktree at closure, "not round code … not clean" | `grep -n RevC2Classes corpus/lessons/round-43-verifier-spotcheck.md` |
| 3 | `corpus/lessons/round-43-verifier-spotcheck.md:64` | routed defect R43.2 (`routed_at` `506e99c7b73c85711f066895984d501fcf7539cd`, key `RevC2Classes.md`) | `python3 -c "import json;d=json.load(open('.ufo/evidence/round-50/c1/defects.json'));print([x for x in d['defects'] if x['id']=='R43.2'])"` |
| 4 | `83beaf98` on `.ufo/waves/round-43/w1/RevC2Classes.md` | the dirty edit was committed, not reverted: 13322 of 13664 already-landed bytes replaced (+61/-46) | `git diff --numstat 83beaf98^ 83beaf98 -- .ufo/waves/round-43/w1/RevC2Classes.md` |
| 5 | `corpus/lessons/round-47-verifier-spotcheck.md:22` | conformance defect 2: `03facb22` rewrites `T47ConnCross.md` (+228/-214) after the round's report; "Neither changes a counted surface" | `git diff --numstat 03facb22^ 03facb22 -- .ufo/waves/round-47/w1/T47ConnCross.md` |
| 6 | `T50ScribeAppendOnly.census.txt`, `T50ScribeAppendOnly.tool-runs.txt` | population (22 pairs / 20 files / 1165 files) and the five checker runs with true exits | census script inline in the first receipt; second receipt is the checker's own output |
| 7 | `corpus/QUALITY.md:262-279` (35), `:150-152` (26), `:7` (4) | the append-only mechanics this reuses; 35 checks `git diff --numstat` deleted *lines* over corpus prose, 26 one receipt line, 4 the admission bar | `sed -n '7p;150,152p;262,279p' corpus/QUALITY.md` |
| 8 | `corpus/QUALITY.md:1428-1435` (97), `:236-250` (33), `:127-136` (23) | pointer resolution and the vacuity discipline the FROM rule implements | `sed -n '127,136p;236,250p;1428,1435p' corpus/QUALITY.md` |
| 9 | `corpus/QUALITY.md:176-189` (29), `:1371-1379` (93) | kill discipline: a killed mutant is a nonzero exit printing `FAIL ` | `sed -n '176,189p;1371,1379p' corpus/QUALITY.md` |
| 10 | `corpus/QUALITY.md:153-175` (27), `:217-235` (32) | every lane git caller scrubs `GIT_*` and proves it on a `GIT_DIR` canary | `sed -n '153,175p;217,235p' corpus/QUALITY.md` |

Why the rule is not already covered: criterion 35's check is `git diff --numstat REV_OLD REV_NEW --
<append-only file>` over corpus prose, and it counts deleted *lines*, so a rewrite confined to one line
passes it; criterion 26 covers one receipt line; criterion 4 states the bar. No criterion compares a
`.ufo/waves/` artifact with its own earlier blob (`grep -n 'waves/' corpus/QUALITY.md` → every hit is a
citation of a wave file as evidence, none states such a comparison), so both motivating rewrites passed
closure as status-neutral.

## 3. Measured population and the checker's behaviour on retained bytes

### 3.1 Population (`.ufo/waves/round-50/w1/T50ScribeAppendOnly.census.txt`)

- rounds 43-50, every file under `.ufo/waves/round-<N>/`: 1165 files, 20 multi-commit, 22 pairs —
  **all 22 pairs are non-prefix**, across 20 files.
- `*.md` seat reports alone: 422 files, 12 multi-commit, 14 pairs, 14 non-prefix, 12 files.
- round 43, `c5335c70 -> 3c4003f6` ("records corrections"): 9 pairs over 9 files, `RevC2Classes.md`
  losing 15250 of 15342 bytes; round 43→44 `3c4003f6 -> 83beaf98` again 13322 of 13664.
- round 47: `T47ConnCross.md` `edd4ca44 -> 03facb22` losing 31456 of 31648; `T47CritC1Control.md` twice
  (`6b5ea3b1 -> 8b0e15d2` lost 5777; `8b0e15d2 -> edd4ca44` lost 21758); `build-spec.py` `9acfbe21 -> 8b0e15d2`.
- round 49: `T49RevengerLapse.md` `9b9b2a01 -> fc5ac743` losing 6262 of 26775; `build-spec.py`,
  `build-spec-w2.py`, `spec-w1.json`, `w1-dispatch.json`, `w1/swarm-registry.json` at
  `6885adb4 -> 455b2cd6` / `9b9b2a01 -> 5f597fa8`.

### 3.2 The checker on retained bytes (`.ufo/waves/round-50/w1/T50ScribeAppendOnly.tool-runs.txt`)

| FROM → TO | output (tab-collapsed) | exit |
|---|---|---|
| `c5335c70 83beaf98` | 9 × `REWRITTEN … prefix-lost`; `SUMMARY checked=2856 rewritten=9` | 1 |
| `edd4ca44 03facb22` | `REWRITTEN .ufo/waves/round-47/w1/T47ConnCross.md prefix-lost`; `SUMMARY checked=3193 rewritten=1` | 1 |
| `6b5ea3b1 03facb22` | `REWRITTEN .ufo/waves/round-47/build-spec-w2-draft.txt deleted`; `REWRITTEN .ufo/waves/round-47/build-spec.py prefix-lost`; `REWRITTEN .ufo/waves/round-47/w1/T47CritC1Control.md prefix-lost`; `SUMMARY checked=3186 rewritten=3` | 1 |
| `9b9b2a01 fc5ac743` | `REWRITTEN .ufo/waves/round-49/build-spec-w2.py prefix-lost`; `REWRITTEN .ufo/waves/round-49/w1/T49RevengerLapse.md prefix-lost`; `SUMMARY checked=3787 rewritten=2` | 1 |
| `487b8f0 5891bdb` | `SUMMARY checked=2819 rewritten=0` | 0 |

The last row is the reason FROM must be the adding commit: `487b8f0` is the round-42 spot-check, so no
round-43 artifact exists at FROM and none of the nine rewrites is examined. The executor seat reported
this row as "0 rewritten"; it is vacuous, not clean.

## 4. Falsifier spec for `T50ExecAppendOnly`

The checker and its receipts already exist; this section says what the criterion needs from them and what
is still missing, so the seat does not have to re-derive the requirements.

### 4.1 What the artifact already does (observed at sha256 `cee1a2dd…`, 7954 bytes)

- CLI `LANE FROM TO`; scope `^\.ufo/waves/round-[^/]+/`; blob-level prefix test; `REWRITTEN`/`SUMMARY`
  grammar; exits 0 / 1 / 2 (`ERROR: …` on stderr for refusals); read-only plumbing only
  (`rev-parse`, `ls-tree -r -z`, `cat-file --batch`) — confirmed by reading the source and by the runs
  in §3.2, which touched no lane state.
- `receipts/fixture-driver.sh`: 11 fixture cases in a `mktemp -d` repo whose toplevel is asserted equal
  to the fixture dir, with per-case `.stdout`/`.stderr`/`.exit` receipts and `judge` assertions
  (append 0; edit-in-place, deleted, truncated, renamed 1; non-round file ignored 0; identical 0;
  bad-rev, missing-arg, non-repo, missing-lane 2).
- `receipts/clone-driver.sh`: scale proof on a `git clone --shared` of the lane at `487b8f0` —
  append → `checked=2819 rewritten=0`, exit 0; probe rewrite of
  `.ufo/waves/round-42/w1/MutC1M10.md` → `prefix-lost`, exit 1.
- `receipts/00-toolchain.txt` names the checker sha256, its byte size and the lane tip.

### 4.2 What the seat has delivered (read at 19:23-19:24, checker sha256 `cee1a2dd…`)

1. **Assertion output committed.** `receipts/fixture/results.txt` and `receipts/fixture/driver.stdout`
   are 599 bytes each with 16 `PASS` lines and no `FAIL`; `receipts/clone-scale/results.txt` is 200
   bytes with 4 `PASS` lines (append exit 0; probe rewrite exit 1 naming
   `.ufo/waves/round-42/w1/MutC1M10.md prefix-lost`).
2. **Adding-commit receipts, all exit 1, each with a `.revs` sibling** carrying
   `tool=`, `tool_sha256=cee1a2dd…`, `from`/`to` in full 40-hex, `exit=` and `summary=`:
   `receipts/lane/addcommit-r43wave1-r44repair.*` (`c5335c70..83beaf98`, nine reports,
   `checked=2856 rewritten=9`), `addcommit-r47deciding-wrapup.*` (`edd4ca44..03facb22`, one,
   `checked=3193`), `addcommit-r47inflight-wrapup.*` (`6b5ea3b1..03facb22`, three, `checked=3186`),
   `addcommit-r49content-r49rekey.*` (`9b9b2a01..fc5ac743`, two, `checked=3787`).
   `receipts/lane/crosscheck.stdout` records the four windows with `git name-status` beside the
   checker's verdict, and `timing.stdout` records two ranges at 27-31 ms.
3. **Mutation proof.** `receipts/c100-falsifier.py` stages three broken copies (prefix→length,
   drop-deleted, widen-scope); its receipt `receipts/quality/c100-falsifiers.stdout` shows pristine
   4/4 `PASS`, three `FAIL mutant=…` lines, `mutants recognised as wrong: 3/3`, then
   `CRITERION-100-FALSIFIER-OK`, exit `0`; `receipts/mutation/mutations.txt` holds the three diffs.
4. **No live closure run.** Round-50 wave-1 artifacts are uncommitted at HEAD
   (`git ls-tree -r --name-only HEAD .ufo/waves/round-50/w1/` → empty), so the closure run belongs to
   the L1 at the landing tip; the seat's green is the fixture and clone pair.

### 4.3 Receipt naming: a defect found here and repaired within the wave

As first written, the four `lane/addcommit-*.stdout` receipts named neither their FROM nor their TO and
carried no checker sha256 (`grep -l 'c5335c70\|edd4ca44\|6b5ea3b1\|9b9b2a01\|83beaf98\|03facb22\|fc5ac743\|cee1a2dd'
receipts/lane/addcommit-*` returned nothing), and three names misdescribed their window — the receipt
then named `addcommit-r47-wave1-to-tip` carried the nine **round-43** rewrites at `checked=2856`, and
`addcommit-r47base-to-wrapup` ran from `edd4ca44`, not the round-47 base `0b5b7cd2`. Repaired by the
seat, and verified here: each run now has a `.revs` sibling with `tool=`, `tool_sha256=cee1a2dd…`,
full-hex `from`/`to`, `exit=` and `summary=`, and the four windows are renamed
`addcommit-r43wave1-r44repair`, `addcommit-r47deciding-wrapup`, `addcommit-r47inflight-wrapup`,
`addcommit-r49content-r49rekey`; the nine older `lane/*` receipts carry `.revs` too
(`cat receipts/lane/addcommit-r49content-r49rekey.revs`). The defect is recorded rather than dropped,
which is what criterion 100 asks of a corrected artifact.

### 4.4 Bounds for the seat while it builds this

Fixture repos stay under its scratch root (`/fast/scratch/hyaku/tameshi-r50/T50ExecAppendOnly`), each
created as `D=$(mktemp -d -p "$S") && git -C "$D" init -q` with `git -C "$D" rev-parse --show-toplevel`
asserted equal to `$D` before any commit; the lane is read-only, and the checker's own `GIT_*` handling
is exercised by running it from a shell whose `GIT_DIR` names a canary (criterion 32's proof belongs to
the tool, not to the driver).

## 5. Landing order and the C1 ledger excerpt

1. `T50ExecAppendOnly` commits the checker, drivers, receipts and the falsifier entry point. They are
   written and verified (§4.2) but still untracked at this reading — `git status -s
   .ufo/waves/round-50/w1/T50ExecAppendOnly` reports `?? ./`.
2. The L1 appends criterion 100 verbatim from §1 after `corpus/QUALITY.md:1464`, in a commit that
   touches `corpus/QUALITY.md`; the criterion cites the checker and the receipts, so step 1 must precede
   it (criterion 97).
3. The L1 runs, at the landing tip, the checker once per distinct adding commit of round 50's wave
   artifacts and commits the output as the round's closure receipt; `rewritten=0`, exit 0 is the green.

R48.4 is compound (`brace_depth_at`, `S205`, `six-leg regression ledger`, `located-name`,
`append-only rule`); a compound item is met only when every ask exists in the tree, so this criterion
closes one of five. For the ledger row, the excerpt I verified against the counter's evidence rules:

- excerpt (88 chars after whitespace collapse, contains key `append-only rule`):
  `The append-only rule binds round 50 and later; earlier rounds are measured, not repaired`
- absent at R48.4's `routed_at` `8ca67421111fa354b47b803358391d0b07fc6db9`:
  `git show 8ca67421:corpus/QUALITY.md | grep -c 'append-only rule'` → `0` (that revision is 1442 lines;
  the criterion is new text).
- the cited lines carry none of the counter's forbidden strings (`planned`, `carried`, `still open`,
  `not worked`, `stay(s) open`, `remain(s) open`, `routed to round`, `not fixed`, `unfixed`,
  `not landed`), and the criterion-append commit touches the file, as `fixed` requires.

## 6. Limits and findings

- The checker's scope is broader than "seat reports": it examines every `round-*/` file, so the
  criterion's subject is stated as every file under `.ufo/waves/round-<N>/`. A narrower `.md` subject
  would make the criterion fail on artifacts it does not describe (`6b5ea3b1 03facb22` reports
  `build-spec.py` and `build-spec-w2-draft.txt`).
- Finding, found and repaired in-wave (§4.3): the four `lane/addcommit-*.stdout` receipts named
  neither FROM/TO nor the checker sha, and three names misdescribed their window. They now carry
  `.revs` siblings with tool sha and full-hex revisions, and are renamed for their real windows. Two
  earlier gaps are likewise closed: the fixture assertion output is committed
  (`receipts/fixture/results.txt`, 16 `PASS`, 0 `FAIL`), and the three mutants print `FAIL ` lines with
  `CRITERION-100-FALSIFIER-OK` at exit 0.
- Finding (FROM choice): the executor's cross-check `487b8f0..5891bdb → checked=2819 rewritten=0` is
  vacuous, not a pass — nine round-43 artifacts were rewritten inside that window
  (`tool-runs.txt`, `c5335c70 83beaf98` → `rewritten=9`, exit 1). The criterion makes the adding commit
  the FROM, which is the only choice under which that window reports its rewrites.
- Declared blind spots of the comparison: rewrite inside the adding commit; rewrite undone by a later
  commit; uncommitted worktree edits (the closure's clean-tree check owns those); paths outside
  `.ufo/waves/round-*/`; the truth of an appended erratum.
- The 22 historical pairs are measured only. No report is repaired, and none should be: criterion 35
  forbids rewriting landed bytes to look clean.
- Tooling: none installed or upgraded by this seat. The only lane files I wrote are the three above;
  scratch `/fast/scratch/hyaku/tameshi-r50/T50ScribeAppendOnly` was removed before this note was yielded.

## Summary

Criterion 100 is drafted verbatim in §1 for appending after `corpus/QUALITY.md:1464`, written against the executor's real artifact (`seat-report-append-only.py`, `LANE FROM TO`).
Rule: every file under `.ufo/waves/round-<N>/` keeps its adding-commit bytes as a prefix of its landing-tip bytes; `REWRITTEN`/exit 1 fails, exit 2 is setup refusal, `checked=0` is refusal-shaped.
FROM is the adding commit, not the round base: `487b8f0..5891bdb` prints `rewritten=0` while `c5335c70..83beaf98` prints `rewritten=9` over the same rewrite.
Motivated by R43.2 (`round-43-verifier-spotcheck.md:12,64`; committed later as `83beaf98`) and round-47 conformance defect 2 (`round-47-verifier-spotcheck.md:22`; `03facb22` on `T47ConnCross.md`).
Population: all 22 multi-commit pairs on 1165 wave files of rounds 43-50 are non-prefix, across 20 files.
Verified in the executor's tree: fixture 16 `PASS`/0 `FAIL`, clone 4 `PASS`, three mutants each `FAIL ` with `CRITERION-100-FALSIFIER-OK` exit 0, `.revs` siblings naming tool sha and full FROM/TO.
Landing: commit the untracked round-50 artifacts, append criterion 100, then the L1's closure green at the landing tip.
R48.4 stays open — one of its five asks is met by this note; the other four belong to other seats.
