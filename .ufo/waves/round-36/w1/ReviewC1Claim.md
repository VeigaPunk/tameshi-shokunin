# ReviewC1Claim — adversarial review of C1 (calibration cold-read refresh)

Round 36, wave 1, leaf seat. Scope: C1 causality only.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Commits under attack: content `e423c41ba253357ab8c8513f0376dad9d38ab248` → refresh
  `b455001e2589b3f4f471d94a3de7e5e549b9f54c` → receipts `d9c496b` (lane tip at review time)
- Contract: `.ufo/evidence/round-36/contract.json` (C1, frozen pre-data)

**VERDICT: C1 HOLDS.** (full statement at the end; record-level defects below do not
defeat the claim)

---

## 1. What I attacked

The four questions in the assignment, plus every invariant the answer depends on:

1. Was `control/monitor-at-e423c41b.*` genuinely produced at the **content** commit, not
   the refresh commit?
2. Is the refresh commit's parent the content commit?
3. Does a monitor run at the refresh commit equal the committed after receipt?
4. Did any **cited input** of the four re-anchored sections change between content and
   refresh (`git diff <content> <refresh> -- <paths>`)?

Because the credit is a function of ledger bytes, I also checked: monitor bytes unchanged
across the before/control/after revs, ledger bytes unchanged between before and control,
the recorded input digests against real blobs at both revs, the calibration formula, and
whether the refresh commit is the *only* delta that can move the score.

## 2. Exact commands run (all read-only; revisions named)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git rev-list --parents -n 2 b455001                       # b455001 -> e423c41
git rev-parse b455001^                                    # e423c41ba253357…
git diff --name-status e423c41 b455001                    # 8 paths: ledger M + 7 coldread A
git diff --stat e423c41 b455001 -- SKILL.md LOG.md SCORECARD.md corpus/QUALITY.md \
  corpus/README.md corpus/SOURCES.md corpus/knowledge/closeout-r11.md \
  corpus/knowledge/survivor-fixture-minimization.md tools/mutate-and-run.sh   # empty
git diff --numstat 796e08b e423c41 -- SCORECARD.md LOG.md corpus/SOURCES.md  # 47/0, 46/0, 3/1
for rev in 796e08b e423c41 b455001 d9c496b; do
  git cat-file blob $rev:.ufo/evidence/round-21/coldread/measure.py | sha256sum
  git cat-file blob $rev:.ufo/evidence/round-18/measure.py        | sha256sum
  git cat-file blob $rev:tools/trace-inputs.py                    | sha256sum
done
git show e423c41:.ufo/evidence/round-21/coldread/ledger.json > /fast/scratch/.../ledger-content.json
git show b455001:.ufo/evidence/round-21/coldread/ledger.json > /fast/scratch/.../ledger-refresh.json
# independent re-runs of the frozen monitor (wrapper, no overrides):
python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev {e423c41…|b455001…|796e08b…|d9c496b} > /fast/scratch/.../rerun-<rev>.json
sha256sum rerun-*.json .ufo/evidence/round-36/{control/monitor-at-e423c41b.stdout,after/monitor-at-b455001e.stdout,after/monitor-at-796e08b.stdout}
git fsck --unreachable --no-reflogs      # searched for an earlier measured refresh state
git reflog --date=iso                    # lane is jj-exported ("export from jj")
```

Analyzer for the ledger comparison: a throwaway Python read of the two `git show` blobs
(dict-equality per entry, plus digest recomputation via `git cat-file blob <rev>:<path>`).
Nothing in the lane was written except this report.

## 3. Answers

### Q1 — control genuinely at the content commit: YES

- Receipt `.ufo/evidence/round-36/control/monitor-at-e423c41b.stdout` carries
  `"revision": "e423c41ba253357…"` and `"rev_input": "e423c41ba253357…"`,
  `ledger_source: "rev"`, `ledger_committed: true`, `overrides_used: false`,
  `trace_gate: "strict"`, score 6, 60/64.
- The monitor only reads blobs at an explicit commit: `.ufo/evidence/round-18/measure.py:9-10`
  ("Reads blobs via `git cat-file`/`git show` at an explicit commit only (no worktree
  access)"), implemented at `:173-196`; the round-21 wrapper forbids
  `--ledger-file/--ledger-rev/--inputs-overlay` (`.ufo/evidence/round-21/coldread/measure.py:23-33`,
  exit 64), so the ledger and inputs cannot be substituted.
- Wall-clock corroboration: `e423c41` exported 03:14:00, control receipt written
  03:14:58, `b455001` exported 03:16:09 — the control predates the refresh commit by 71 s
  and postdates the content commit. It *cannot* have measured the refresh tree.
- Independent re-run at `e423c41` is **byte-identical** to the receipt:
  sha256 `b49c84b1599369e4ee61cd87367e73734768cd509cd298af6e78d3023458a44c` for both.
  A run at `b455001` yields 8/64-64, so the recorded 6 is not producible from refresh
  state (and vice versa).

### Q2 — refresh commit's parent is the content commit: YES

`git rev-list --parents -n 1 b455001` → `b455001e… e423c41ba2…`; no merge, single parent.

### Q3 — monitor at the refresh commit equals the receipt: YES, byte-identical

Re-run at `b455001` has the same sha256 as
`.ufo/evidence/round-36/after/monitor-at-b455001e.stdout`:
`6b287d9e793aaa116528d91596f4f35ab94f29feb65626f75c99ee5241cab46d`
(score 8, `sections_covered 64/64`, `missing: []`, `box3_full_page: true`,
`revision == rev_input == b455001…`). The before receipt `after/monitor-at-796e08b.stdout`
likewise reproduces exactly (`7685a1306b06acd7…`, 6, 60/64).

Saturation is honest: `restraint = 2·|asserted boxes 1,2,4| + 2·box3_points`
(`round-18/measure.py:681-682`); the four-box scorecard is `['~','~','~','~']`, so 8 is the
axis maximum and the 6→8 delta is exactly the `box3_full_page` pair of points. No other
component moved (`shonen` identical before/control/after; `SHONEN.md` untouched).

### Q4 — cited input changed between content and refresh: NO

The explicit diff over the union of cited inputs (from `affected-sections.json` and the
four new entries) is empty:

```
SKILL.md LOG.md SCORECARD.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md
corpus/knowledge/closeout-r11.md corpus/knowledge/survivor-fixture-minimization.md
tools/mutate-and-run.sh            → no changes (exit 0)
```

Whole-commit delta content→refresh is the refresh itself: `M ledger.json` plus
`A affected-sections.json, refresh-receipts.json, refresh-specs.json, traces/L1/source-{1..4}.json`.
No product file, no SKILL.md byte, no monitor byte.

Independent digest check of entry 493 (all nine inputs) at **both** revs: every recorded
sha256 equals the `git cat-file blob` hash at `e423c41` and at `b455001`
(e.g. `SKILL.md 2381873162fc21db…`, `LOG.md a2223dc239aaa37c…`,
`SCORECARD.md 1b0124a79a81c75b…`, `tools/mutate-and-run.sh a7d3f2dd7d47511a…` — the
frozen runner pin). This is the exact mechanism: the monitor's input gate runs at the
**measured** rev, not at the entry's `read_rev` (`round-18/measure.py:353-359`), so a
re-anchor credits precisely because the cited bytes did not move between `e423c41` and
`b455001` — the diff I was asked to run.

## 4. Corroborating invariants

- **Monitor frozen.** `round-21/measure.py` = `657f009bdf1cc89a…` and
  `round-18/measure.py` = `7ca87a7c98196d87…` at `796e08b`, `e423c41`, `b455001`,
  `d9c496b`. No instrument drift across before/control/after.
- **Control isolates record edits.** Ledger bytes are identical at `796e08b` and
  `e423c41` (`git diff --stat 796e08b e423c41 -- ledger.json` empty). The only difference
  between before and control is record text (`LOG +46/-0`, `SCORECARD +47/-0`,
  `SOURCES +3/-1`, QUALITY, lesson, waves). Both print 6/60 with the **same four missing
  headings** — record edits alone demonstrably do not restore credit.
- **Ledger delta is four appends, nothing else.** 493 → 497 entries; the first 493 are
  dict-identical in order and content; `schema`, `carried_from`, `provenance`,
  `round21_provenance` identical. Only entries with `read_rev = e423c41` are the four new
  ones. Each new entry's input set equals the refresh spec's path list exactly plus
  `SKILL.md`; the spec section hashes equal the entry slice hashes (`e37cf21e…`,
  `13d489ad…`, `d4600d2f…`, `441858d2…`); the spec paths are exactly the union of the
  inputs named in the four sections' failing-entry drift reasons.
- **Trace instrument pinned.** `tools/trace-inputs.py` is `f59c9312c56eb458…` at all four
  revs and equals `instrument_sha256` in `refresh-receipts.json`; the four trace JSONs
  declare `rev = e423c41…`, `live_lane_reads {}`, `external {}`, `untracked {}`.
- **S103 snapshot** (`src/s103-git-hash-object.html`) hashes `dd826dae…6100` at every
  rev, matching the receipt's `cited_source` row.
- **Kill rule.** Delta content↔refresh = ledger entries + trace/spec/receipt evidence;
  monitor and ledger algorithm untouched; SCORECARD change is purely additive (no rubric
  line removed). Credit also survives at HEAD `d9c496b` (re-run: 8, 64/64) because the
  receipts commit adds only `control/` and `after/` files, none of them cited inputs.

## 5. Findings, by severity

### MEDIUM — dangling "round-36 report" in three records

`LOG.md:1919` ("hash named in the round-36 report …"), `SCORECARD.md:1743`
("… and the round-36 report") and `corpus/lessons/round-36.md:85` ("the round report
itemizes the 78 prepared-but-undispatched seats") all cite a round-36 report. No such
artifact exists at `e423c41`, `b455001` or `d9c496b` (`git ls-tree -r --name-only` finds
none; `.ufo/waves/round-36/` holds only `spec-w{1,2}.json`, `dispatch-w{1,2}.json`,
`validate-*`, `w1/`). This is the same defect class as the round-35 routed defect 1 that
this round repairs, re-introduced in the round's own record.

Impact is bounded: the measured commit is still resolvable from the receipt filename
`monitor-at-b455001e.stdout` (8-hex) and from the receipt's internal 40-hex `revision`, so
the claim's commit binding survives; the seat-itemization referent does not.

### LOW — control receipt name drift (already peer-flagged)

`LOG.md:1918` cites `.ufo/evidence/round-36/control/monitor-at-content-commit.*`; the
committed receipts are `control/monitor-at-e423c41b.{exit,stdout,stderr}`. The path as
written matches nothing. Same artifact set, same commit; label only. (Peers
RevengerContractFreeze, SimplifierSCORECARDRow, LabratControlGenuine raised this; recorded
here for completeness, not duplicated as new.) Related cosmetic note: the *before* receipt
`monitor-at-796e08b.*` lives in `after/`, and was regenerated at 03:21 (rev-addressed, so
valid; no chronology claim rests on its mtime).

### LOW — the four new entries' verdict/label fields are internally inconsistent

Each new entry records `verdict: "gap-minor"` **and** `minor_gaps: 0`. Of 378
`gap-minor` entries in the ledger, 374 record at least one minor gap; the only four
exceptions are exactly these new entries. `record` class also has `verified-record`
available (`round-18/measure.py:127`, `:505-508`), which would be consistent with zero
gaps. Also, `skill_sha256` in the new entries equals the section slice hash (identical to
`sha256`), whereas the 493 retained entries carry a page-level value
(`skill_sha256 != sha256`).

Credit-neutral: the monitor never validates `minor_gaps` against the verdict and never
reads `skill_sha256` except as an overlay key (`:588`, `:593`). But a reader of the claimed
evidence is told a minor gap exists that no field records, and the page-identity field is
convention-inconsistent with the rest of the ledger.

### LOW — SCORECARD prose asserts the measurement before any state can produce it

The round-36 SCORECARD block, exported inside `e423c41` (export 03:14:00), states under
"Numeric axes, measured": "the strict cold-read monitor prints … and `8, 64/64` at the
refresh commit". The refresh commit was exported 03:16:09 and the after receipt written
03:16:45. No commit in the object database — including the eight unreachable commits found
by `git fsck --unreachable --no-reflogs`, none of which is a round-36 refresh — contains a
497-entry ledger before 03:16:09. So either the 8 was measured in an uncommitted scratch
lane (the same `/tmp` copy pattern the refresh receipts disclose for the trace collector),
or the text is a prediction written in the past tense. `LOG.md` hedges correctly ("target
8, 64/64"); the SCORECARD paragraph does not.

Not a numeric defect — I reproduced 8/64-64 byte-identically — but it is a provenance
defect in the record of a calibration claim: the committed receipt postdates the sentence
that reports it.

### LOW — the ledger diff is a whole-file reserialization

The refresh rewrites the 3.6 MB ledger (indent 2→1, 3,633,498 → 3,489,570 bytes);
`git diff` reports 40,304 insertions / 40,186 deletions for a four-entry append. I verified
the retained 493 entries are dict-identical (same order, same fields) and the non-entry
top-level fields are unchanged, so the rewrite is semantically a no-op — but it makes the
diff unauditable by inspection and is not disclosed in the round record. A future auditor
must repeat the semantic comparison to see that nothing else moved.

### LOW — refresh receipts' `stdout_sha256` binds uncommitted bytes

`refresh-receipts.json` records `stdout_sha256` and a `/tmp/tameshi-r36-refresh-*/lane`
run root; neither the collector stdout nor the instrument run root is committed. The
committed trace JSONs are sufficient — their digests are independently verifiable and I
verified them — but the stdout hashes themselves prove nothing in-repo.

## 6. Residual risk (what the claim does not show)

- **It is a ledger refresh, not a document or reading repair.** SKILL.md is byte-identical
  across `796e08b`/`e423c41`/`b455001`/`d9c496b`; the four sections were never edited and
  were not independently re-read. The scope line ("L1-author input-keyed source reads
  only; not independent/blind cold-read, recipe re-execution or required-command
  coverage") is carried verbatim in `refresh-receipts.json` — the claim is honest only if
  read with that scope.
- **Append semantics erase the drift signal without deleting it.** A section is credited
  if any matching entry passes and no matching entry is vetoed
  (`round-18/measure.py:610, 630-638`); input drift is not a veto. The four sections now
  carry 13 / 16 / 13 / 2 matching entries, the drifted ones still present but invisible in
  the score. Credit can be restored indefinitely by re-recording digests; the mechanism
  cannot distinguish "sources re-read now" from "digests re-stamped now".
- **Trace provenance is self-declared.** The collector declares `rev = e423c41` for a
  `/tmp` lane copy; the binding that matters is digest equality at the measured rev, which
  I verified independently, not the trace's declared rev.
- **The control proves credit stability, not causal necessity of the four entries
  specifically**: because the append protocol credits on any passing entry, a single
  passing entry per section is enough; the four entries are sufficient, and the before /
  control pairing shows the record edits are not.

## 7. Verification gaps

- No LSP server applies to these artifacts (markdown/JSON evidence and git blobs); the
  credit logic was checked by reading the frozen implementation and by executing it, not
  by text grep. Semantic claims about the monitor are backed by its code paths and by
  three independent, byte-identical replays.
- I did not run the round-21 selector `--selftest` or the round-18 `--selftest`; they are
  not on C1's path (the wrapper's override refusal and the module's credit path were
  exercised directly by the replays).
- The scratch copies of both ledger revisions and the four replay outputs are at
  `/fast/scratch/hyaku/tameshi-r36-seats/ReviewC1Claim/`. No tools were installed or
  upgraded.
- Risk of unknown-unknowns: I did not attempt to prove that no uncommitted `/tmp` lane was
  ever used for an earlier preview measurement (that is the one unfalsifiable branch of the
  SCORECARD-ordering finding above).

---

**VERDICT: C1 HOLDS.** The do-nothing control is genuinely a run at the content commit
`e423c41` (rev-addressed by construction, time-ordered before the refresh commit, and
byte-identical under independent replay); the refresh commit `b455001`'s parent is the
content commit; a replay at the refresh commit equals the committed after receipt
byte-for-byte (8, 64/64, axis maximum); and no cited input of the four re-anchored sections
changed between content and refresh — the only delta is the ledger re-anchor plus its
trace/spec evidence. The claim's numbers, causality and saturation survive; the defects
above are record-level (dangling "round-36 report", misnamed control path, entry-label and
prose-provenance inconsistencies, unauditable ledger rewrite) and should be repaired
append-only, not treated as claim failures.
