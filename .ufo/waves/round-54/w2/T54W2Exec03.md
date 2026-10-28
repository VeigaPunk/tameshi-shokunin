# T54W2Exec03 — no-harm monitors at C1 (round 54, wave 2)

Item: run and record the no-harm monitors at C1, paste all 14 lines, classify every RED.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
C1 (fix commit): `99c3bc88d704566197783f66b211ee0a830e0330`
Base: `d33053f7552db4bd290c99a36979760f544c41ad`
Monitor instrument: `.ufo/evidence/round-54/no-harm.sh`
Freeze digest (frozen record, contract `frozen_paths` #6): `no-harm.sh` = `1aa2fa9df9eac9380be0d24d0191a4c25f93030895db8d5fbeba6147920b639a`
Tool installs during this seat: none (no pacman/uv/npx/binary changes).

## 1. Commands run

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/no-harm.sh \
     /home/vgpnk/Projects/shokunin/tameshi-shokunin 99c3bc88d704566197783f66b211ee0a830e0330
```
Run twice on 2026-10-28 (second run after the first, same seat). Both invocations printed byte-identical output; both exited 0.

Provenance of the instrument:
- worktree `.ufo/evidence/round-54/no-harm.sh` sha256 = `1aa2fa9d…` (matches `freeze.json` → `files["no-harm.sh"]`);
- `git show 441c26bec5e4:.ufo/evidence/round-54/no-harm.sh` sha256 = `1aa2fa9d…`;
- `git show 99c3bc88d704:.ufo/evidence/round-54/no-harm.sh` sha256 = `1aa2fa9d…`.
So the 14 lines below come from the frozen script bytes, unchanged from the freeze commit through C1.

## 2. The 14 lines (verbatim)

```
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=6 credited=41 RED
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-134 139 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [M:tools/bash-witness-study.py M:tools/env-diff.py M:tools/evidence-disposition.py M:tools/pin-disposition.py M:tools/registry.json ] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
NOHARM r53-scratch-hygiene tmp_hits=0 ok
NOHARM ledger-not-shrunk base=568 rev=568 ok
NOHARM sources-not-shrunk base=136 rev=139 ok
```

Line count: 14. `ok` lines: 13. `RED` lines: 1 (`coldread-floor`). Overall script exit: 0 (by design — the script only prints; `deciding-run.sh` gates with `grep -q RED`).

## 3. Predicate re-check, line by line

| # | monitor | observed | predicate in the script | verdict |
|---|---------|----------|--------------------------|---------|
| 1 | commandD | recorded_cases=10 depth_score=10 | `depth_score >= 10` | ok |
| 2 | coldread-floor | score=6 credited=41 | `score >= 8 and credited >= 64` | **RED** (6 < 8, 41 < 64) |
| 3 | r45-freshness | population=74 fresh=71 score=9 | `fresh >= 71 and 10*fresh//population >= 9` (10·71//74 = 9) | ok |
| 4 | r45-coverage | rows=2 entries=2 C2_R45_PASS=true | exact string `rows=2 entries=2 C2_R45_PASS=true ` | ok |
| 5 | S160-count | 1 | exactly one S160 row | ok |
| 6 | registry-rows-not-below-134 | 139 | `>= 134` | ok |
| 7 | r46-coverage | rows=3 entries=3 C3_R46_PASS=true | exact string | ok |
| 8 | r47-coverage | rows=3 entries=3 C3_R47_PASS=true | exact string | ok |
| 9 | tools-scope | M: bash-witness-study.py, env-diff.py, evidence-disposition.py, pin-disposition.py, registry.json | every changed `tools/` path in the round-53 allowlist ∪ {env-diff, bash-witness-study, evidence-disposition, pin-disposition, registry.json} | ok |
| 10 | r49-generator-capability | cases=400 violations=0 counterexample=none, class histogram | exact 400-case string with `violations=0` | ok |
| 11 | r50-shrinker-selftest | cases=14 failed=0 | `*" failed=0"` | ok |
| 12 | r53-scratch-hygiene | tmp_hits=0 | `tmp_hits == 0` | ok |
| 13 | ledger-not-shrunk | base=568 rev=568 | `rev >= base` | ok |
| 14 | sources-not-shrunk | base=136 rev=139 | `rev >= base` | ok |

## 4. RED classification — `coldread-floor`

**Verdict: RED, expected (pre-bind state of the C1 fix pass). Not a content regression, not a monitor defect.**

### 4.1 What the monitor measures and what it read

The monitor runs the unchanged round-21 selector over the revision:

```
python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev 99c3bc88d704
```

`calibration_restraint_score` is computed in the frozen round-18 implementation as
`2·(# asserted marks among boxes 1,2,4) + 2·box3`, and `box3` requires full coverage
(`round-18/measure.py:682`: `restraint = 2 * sum(len(marks) >= b and marks[b - 1] == '~' …) + 2 * box3_points`).
It therefore reads 8 only when all 64 sections credit; 6 otherwise (the frozen suite asserts exactly this:
`no-ledger-score-6`, `bytechange-score-6`, `full-ledger-score-8`). The monitor threshold is
`score>=8 and credited>=64`, so the floor cannot be green at any revision with one uncredited section.

Observed at C1: `credited=41 lost=23 score=6`, i.e. 64 sections, 23 uncredited.

The frozen C1 counter at the same revision reports the same state:

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=99c3bc88d704 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=99c3bc88d704 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```
(`python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev 99c3bc88d704 --work EMPTY --explain`)

### 4.2 Why it is expected: the fix pass rewrote section bytes and moved pinned inputs; no re-key has bound yet

Every one of the 23 uncredited sections falls into exactly one of two declared classes, and no other:

- **14 × `no-ledger-entry`** — the ledger is indexed by the section's own `sha256`
  (`round-18/measure.py:602-612`: `by_sha = {}` … `by_sha.setdefault(entry['sha256'], []).append(entry)`,
  then `matches = by_sha.get(sec['sha256'], [])` → `no-ledger-entry`). The C1 fix pass changed `SKILL.md`
  (56 lines, 38 insertions / 25 deletions vs base), so 13 sections now have bytes that no entry pins.
  The 14th, `### Round-26 gate/probe registry — report interop`, was already base-lost and has never had an
  entry pinning its current bytes (its latest entry pins `start=2132`, `skill_sha256=0ef95e1d…`; the C1
  section is `start=2158`, `sha256=cc23587b…`).
- **9 × `input-drift:<path>`** — an entry matching the current section bytes exists, but an input it pins
  moved: `corpus/SOURCES.md`, `corpus/QUALITY.md` and the four tools this round edits
  (`tools/bash-witness-study.py`, `tools/env-diff.py`, `tools/evidence-disposition.py`,
  `tools/pin-disposition.py`, `tools/registry.json`), plus inputs moved by earlier rounds since those
  entries' `read_rev` (e.g. `tools/context-capture.py` round 53 `5b703c6`, `corpus/knowledge/service-limits.md`
  round 53 `a977394`, `tools/mutate-and-run.sh` round 51 `6d8c11e`, `tools/trace-inputs.py` round 21 `370f2df`).

Set arithmetic (receipt `classification.stdout`): 13 changed sections, all `no-ledger-entry`
(`changed_set_minus_nle = []`), + Round-26 (`nle_minus_changed_set`) + 9 input-drift = **23**; 23 + 41 credited = 64.

Bridge from the contract's "before" measurement (receipt `bridge.stdout`):
`base d33053f credited=57 lost=7` → `C1 credited=41 lost=23`, delta −16. `base_lost ⊆ C1_lost` (the frozen
seven are all still lost), `newly_lost = 16` = 8 sections lost to the fix pass's byte edits + 8 lost to
pinned-input drift. `base_lost_now_credited = []` — nothing recovered, nothing lost for an undeclared reason.

### 4.3 Why it cannot clear yet: no re-key directory exists

```
git ls-tree -r --name-only 99c3bc88d704 -- .ufo/evidence/round-21/coldread/ | grep -c rekey-r54   -> 0
git ls-tree -r --name-only HEAD             -- .ufo/evidence/round-21/coldread/ | grep -c rekey-r54   -> 0
git ls-tree -d --name-only HEAD -- .ufo/evidence/round-21/coldread/
  .ufo/evidence/round-21/coldread/rekey-r53-651773ab9e32
  .ufo/evidence/round-21/coldread/rekey-r53-a41195dfc13a
  .ufo/evidence/round-21/coldread/rekey-r53-a9773948087e
  .ufo/evidence/round-21/coldread/traces
```
(HEAD when checked: `4e2de73`; earlier in the seat `8da3539c` / `097985c` — the L1 is committing during the wave,
and no revision yet carries a `rekey-r54-*` directory.) With `dirs=[]` the counter's arms 3 and 4 can only
report `0/7`. This is the binder-not-yet-run state, exactly what the claim's target describes as needing
"a fresh entry bound under `rekey-r54-<c0>`".

### 4.4 What clears it (and what would falsify this classification)

Clearing condition: run the binder over the 23 headings in
`.ufo/evidence/round-54/c1/lost-headings-at-c0.json` (set-equal to the 23 lost at C1; verified:
`c0-headings == C1-lost: True`, `union with lost-headings-at-base.json = 23`). The binder's `HEADINGS`
is exactly that union, so the committed binder already targets 23, not only the seven in the frozen list.
After binding + committing wave-2 reader reports, arm 1 must print `cand_credited=64 lost=0 ok`, arm 2
`covered=64 score=8`, arms 3/4 `7/7`.

Falsifiers I checked and did not find:
- a section lost for a third reason (reasons are only `no-ledger-entry` ×14 and `input-drift` ×9);
- a section that was credited at base and lost for a cause unrelated to this round's own edits
  (all 16 newly-lost sections trace to the C1 `SKILL.md` rewrite or to pinned inputs whose current values
  were written by round 51–54 commits — see `bridge.stdout`);
- a monitor/monitor-input disagreement (the no-harm line and the frozen C1 counter agree: credited=41, score=6);
- non-determinism (two runs byte-identical).

## 5. Advisories for the L1 (outside the monitor verdict; recorded because they gate the deciding run)

These are observations on the current tree, not findings against the monitors or the claim authors. Evidence is
read-only and reproducible.

1. **Counter arm 4 now scans both wave dirs, the binder still scans only w1.** Current
   `c1/measure.py:54` is `WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')` (amendment 3),
   but `integrate/binder.py:48` (committed at `19c7558`; worktree copy in flight) is still
   `WAVE = '.ufo/waves/round-54/w1'` and globs `Path(LANE, WAVE, '*.json')` (`:94` committed, `:99` in the
   uncommitted worktree copy, which adds only a `resolutions.json` findings allowance).
   Wave-2 deliverables are written to `.ufo/waves/round-54/w2/`
   (spec `reportDir`), where at the time of this check there were 20 `Read*.json` files and 0 `T54W2*` files under w1.
   [INFERENCE] Run as committed with `C0=99c3bc88d704`, the binder would see only the 23 wave-1 reports
   (pinned at the pre-fix commit, so `d.cand != c0` and stale `section_sha256` for the 13 changed sections)
   and skip every heading as `no-clean-reader`, leaving arms 3/4 at 0/7. Either the binder's `WAVE` gains w2
   or the invocation must stage the wave-2 JSON **and its sibling `.md`** where the binder globs
   (the binder rejects `reader-md-missing`).
2. **Re-key directory name must equal the commit the readers read.** Arm 3 resolves `c0` from the
   directory name (`^rekey-r54-([0-9a-f]{12})$`) and arm 4 requires `d['cand'] == c0` (full hash) and
   `d['section_sha256'] == <section sha at the deciding rev>` (`c1/measure.py:241`). Wave-2 readers record
   `cand = 99c3bc88d704566197783f66b211ee0a830e0330`, so the directory must be
   `rekey-r54-99c3bc88d704` and the binder must be invoked with `C0 = 99c3bc88d704…`; a directory named
   after the pre-fix content commit `59c3810…` would leave arm 4 at 0/7 even with perfect reports.
   The comparison is string equality against the full 40-hex hash, and all 23 committed-format wave-1 reports
   carry the 12-char prefix (`cand = "59c38109bf11"`, 23/23), which would never equal `resolve(prefix)` —
   wave-2 readers must write the full hash the template shows. All 20 wave-2 reports on disk at check time
   carry the full `cand = "99c3bc88d704566197783f66b211ee0a830e0330"`.
   Also: exactly one `rekey-r54-*` directory may exist (`len(rekey_dirs) == 1`), and `SKILL.md` must not
   change after C1, or the readers' pinned section shas stop matching the deciding revision.
3. **Freeze/control interop.** `git diff --name-only 441c26bec5e4 HEAD -- <contract frozen_paths>`
   currently names 5 files (`c1/measure.py`, `c2/measure.py`, `contract.json`, `deciding-run.sh`,
   `freeze.json`) after the amendment 3 re-freeze; `git diff --name-only 4e2de73 HEAD` is empty. The
   deciding script's frozen gate is `git diff --quiet "$FREEZE" "$REV" -- $FROZEN` and refuses nothing but
   prints `FROZEN_UNCHANGED=0` + `rc=1` if `FREEZE=441c26bec5e4` is passed against a post-amendment REV.
   Separately, the control receipts are committed at `19c7558` and `controls-b.{stdout,exit}` do not exist
   yet, while the gate requires all four files committed at REV in commits descending from `$FREEZE`
   (`git merge-base --is-ancestor "$FREEZE" "$c"`), so a freeze commit later than `19c7558` would refuse
   with `control-receipt-not-after-freeze` unless the controls are re-committed after it.

## 6. Side-effect audit (monitor run is no-harm to the tree)

- `git status --porcelain` immediately after the two monitor runs: only the pre-existing untracked wave
  artifacts (`?? .ufo/waves/round-54/w1-run.out`, `?? .ufo/waves/round-54/w1/`, `?? .ufo/waves/round-54/w2-run.out`,
  `?? .ufo/waves/round-54/w2.ready.dispatched`, `?? .ufo/waves/round-54/w2/`). No tracked modification at that point.
- Later in the seat the lane gained `M .ufo/evidence/round-54/integrate/binder.py` and
  `?? .ufo/evidence/round-54/integrate/resolutions.json` from another writer (a concurrent L1/seat edit to the
  binder — `git diff --numstat` = `15 3` — appearing after my monitor runs). I did not touch either; my writes
  are confined to the two paths named below.
- No `__pycache__` newer than 30 min anywhere in the lane (the selector sets `sys.dont_write_bytecode`).
- No `/tmp` residue (`find /tmp -maxdepth 1 -name '*tameshi*' -newermt '-30 minutes'` → empty).
- The script's own scratch `$HYAKU_SCRATCH/tameshi-r54/no-harm` is removed by its `trap` (absent after both runs).
- I wrote only under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w2/`
  (this report and `T54W2Exec03-receipts/`).

## 7. Artifacts opened / receipts written

Opened (read-only): `.ufo/evidence/round-54/no-harm.sh`; `.ufo/evidence/round-54/contract.json`;
`.ufo/evidence/round-54/freeze.json`; `.ufo/evidence/round-54/deciding-run.sh`;
`.ufo/evidence/round-54/c1/measure.py`; `.ufo/evidence/round-54/c1/lost-headings-at-base.json`;
`.ufo/evidence/round-54/c1/lost-headings-at-c0.json`; `.ufo/evidence/round-48/quality/coldread-precheck.sh`;
`.ufo/evidence/round-21/coldread/measure.py`; `.ufo/evidence/round-18/measure.py`;
`.ufo/evidence/round-54/integrate/binder.py`; `.ufo/waves/round-54/spec-w2.json`;
`.ufo/waves/round-54/` listings; git objects at `d33053f`, `59c3810`, `99c3bc8`, `441c26b`, `19c7558`,
`097985c`, `8da3539`, `4e2de73`.

Receipts written:
- `T54W2Exec03-receipts/no-harm-c1.stdout` — the 14 lines of the recorded run.
- `T54W2Exec03-receipts/no-harm-determinism.txt` — second run identical.
- `T54W2Exec03-receipts/precheck-c1.stdout` — frozen precheck at C1: 23 `LOST` lines + summary, exit 1.
- `T54W2Exec03-receipts/c1-measure-c1.stdout` — the C1 counter's 5 lines, exit 1.
- `T54W2Exec03-receipts/classification.stdout` — reason decomposition (13 changed / Round-26 / 9 input-drift).
- `T54W2Exec03-receipts/bridge.stdout` — 57→41 bridge, base-lost subset, 16 newly lost.

## 8. Result

- 14/14 monitor lines printed from the frozen script (`1aa2fa9d…`), deterministic across two runs.
- 13 `ok`, 1 `RED`.
- `coldread-floor score=6 credited=41 RED` is classified **expected / pre-bind**: the C1 fix pass changed
  13 section bodies and moved pinned inputs, so 23 sections are uncredited until the binder writes
  `rekey-r54-<c0>` entries (none exist at C1 or at HEAD), which is precisely the state the C1 claim's
  target requires to be closed before the deciding revision.
- No monitor defect, no non-coldread regression, no tree side effects.
