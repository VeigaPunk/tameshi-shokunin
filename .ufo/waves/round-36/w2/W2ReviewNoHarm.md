# W2ReviewNoHarm — tameshi round 36, wave 2 (reviewer, leaf seat)

Axis judged: **calibration**. Assignment: falsify the no-harm assertion — the refresh
commit must not regress any owned-axis surface (no `tools/` edit, no `SHONEN` box flip, no
`QUALITY` criterion deletion). Read-only seat; no production edits.

Revisions in play (all lane commits, `/home/vgpnk/Projects/shokunin/tameshi-shokunin`):

| Name | Rev |
|---|---|
| r35 tip (before rev, contract) | `796e08b888849308d0c4d5e932e56833600a139f` |
| round-36 content / do-nothing control | `e423c41ba253357ab8c8513f0376dad9d38ab248` |
| round-36 cold-read refresh (the commit under attack) | `b455001` |
| receipts | `d9c496b` |
| lane tip | `fbb01cf` |

## What I attacked

1. The assigned path-restricted stat over `SKILL.md`, `PROVINCE.md`, `QUALITY.md`,
   `SHONEN.md`, `tools/`, r35 tip → refresh commit.
2. Byte-level identity of every owned surface (git tree/blob ids, not just diffstat).
3. Whether any `QUALITY` criterion was deleted or renumbered (append-only check).
4. Whether the +2 calibration credit was bought by a surface edit rather than by ledger
   data — i.e. whether an unchanged monitor yields 8 from unchanged `SHONEN.md`/`SKILL.md`.
5. The refresh's own ledger delta: append-only or rewrite (verdict/class/gate tampering).
6. Strict trace gate on the four new entries (schema, input subset, external, live-lane).
7. Veto behaviour per refreshed section (a clean entry must never launder a failing one).

## The assigned stat

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat \
    796e08b..b455001 -- SKILL.md PROVINCE.md QUALITY.md SHONEN.md corpus/QUALITY.md tools/
 corpus/QUALITY.md | 12 ++++++++++++
 1 file changed, 12 insertions(+)
```
`--numstat` for the same pathspec: `12  0  corpus/QUALITY.md` — **0 deletions**.
Same result across the wider range `796e08b..fbb01cf` (lane tip, includes receipts and
spot-check commits).

Full diff for context, `796e08b..b455001`: `24 files, +46215 −40187`.

### Path-resolution caveat (report-shaped trap, not a defect)

There is **no root `QUALITY.md`**. `git ls-tree --name-only 796e08b | grep -E
'^(SKILL|PROVINCE|QUALITY|SHONEN)\.md$'` prints only `PROVINCE.md`, `SHONEN.md`,
`SKILL.md`. The live quality corpus is `corpus/QUALITY.md`. Running the literal assigned
pathspec `... -- SKILL.md PROVINCE.md QUALITY.md SHONEN.md tools/` therefore prints an
empty diff — which would look like "everything untouched" while missing the one file that
did change. Both runs are reported above so the stat cannot be read either way.

## Byte-level identity (all at r35 tip vs lane tip)

```
git ls-tree -r 796e08b tools/ | sha256sum   -> 66c2e00c8cb29c82fc1841d739a0bac072cdefef31625d199aa03863ab0cea0e
git ls-tree -r fbb01cf tools/ | sha256sum   -> 66c2e00c8cb29c82fc1841d739a0bac072cdefef31625d199aa03863ab0cea0e
git diff --name-only 796e08b..fbb01cf -- tools/ | wc -l  -> 0
```
Tree hash equality over all 24 tracked paths under `tools/` is conclusive: no tool file was
added, removed, or edited — including both frozen tools.

| Owned surface | blob @ `796e08b` | blob @ `fbb01cf` | verdict |
|---|---|---|---|
| `SKILL.md` | `0b44815ce04e` | `0b44815ce04e` | identical |
| `PROVINCE.md` | `6154fe44c291` | `6154fe44c291` | identical |
| `SHONEN.md` | `253f3c05d5a7` | `253f3c05d5a7` | identical (`diff` of both blobs: empty) |
| `corpus/QUALITY.md` | `124e34e21a71` | `ca7ed9be88ae` | +12 / −0 |
| `tools/` (24 paths) | tree `66c2e00c…` | tree `66c2e00c…` | identical |

Frozen artifacts re-verified at the refresh commit **and** at lane tip (sha256 of
`git show <rev>:<path>`), both equal to the contract pins:

| Artifact | sha256 @ `b455001` = @ `fbb01cf` | Contract pin |
|---|---|---|
| `tools/tally-audit-v3.py` | `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354` | match |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | match |
| `.ufo/evidence/round-36/c1/c1-measure-v2.py` | `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` | match |
| `.ufo/evidence/round-35/c1/c1-measure.py` (v1) | `d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3` | absent from the diff (unchanged) |

Repo-wide deletion count: `git diff --name-status 796e08b..b455001 | awk '$1=="D"'` → **0**;
same for `796e08b..fbb01cf` → **0**. There is no deletion anywhere between r35 tip and the
lane tip, so the SHONEN box-flip and QUALITY-deletion attacks cannot have landed even off
the owned paths.

## QUALITY criteria: append-only, no deletion

```
grep -oE '^[0-9]+\.' <(git show 796e08b:corpus/QUALITY.md)  -> 71 criteria
grep -oE '^[0-9]+\.' <(git show fbb01cf:corpus/QUALITY.md)  -> 72 criteria
continuity check on the after list -> 1..72 contiguous, no gap, max 72
```
Criterion 71 (round-31 standing-row rule) is byte-identical and immediately precedes the new
criterion 72 (round 36, LOG-citation-exists rule, with its `Captured by:` and `Falsifier:`).
The diff is a single hunk, `@@ -843,2 +843,14 @@`, 12 insertions, 0 deletions.

## SHONEN box flip: impossible

`SHONEN.md` is byte-identical at r35 tip and lane tip. Box states (unchanged, all `~`):
`box 1` line 5, `box 2` line 7, `box 3` line 9 ("Instructions executable by an agent without
oral context"), `box 4` line 11. The monitor's box-3 block and its ledger link are therefore
untouched as well.

## Credit attribution: the +2 came from ledger data, not from a surface edit

`round-18/measure.py:24-27` defines the score:
`2 * count(boxes 1,2,4 marked ~) + 2 * (box3 is ~ AND box3_full_page AND box-3 block names the ledger)`.
With `SHONEN.md` byte-identical, `2*3 = 6` is fixed; the lift is exactly the `box3_full_page`
term flipping true because coverage reached 64/64. The monitor is unchanged: `git diff --stat
796e08b..fbb01cf -- .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-35/c1/c1-measure.py`
is empty.

Committed receipts (L1's runs, read as evidence, not re-executed by me):

| Run | covered | score | box3_full_page | exit |
|---|---|---|---|---|
| before @ `796e08b` | 60/64 | 6 | False | 0 |
| control (content, no refresh) @ `e423c41b` | 60/64 | 6 | False | 0 |
| after @ `b455001` | 64/64 | 8 | True | 0 |

`credits/…`: per-section records for starts 131/375/1380/1436 are
`credited=False vetoed=False reason=input-drift:…` before and at the control commit, and
`credited=True vetoed=False reason=credited` after. So the four sections were **stale by
input drift**, not verdict-failing (no veto), and the control commit cannot restore credit —
the do-nothing control holds.

## Ledger delta: strictly append-only (0 rewritten entries)

`ledger.json` at `796e08b` vs `b455001`: 3,633,498 B → 3,489,570 B; diffstat
`40709 insertions(+), 40186 deletions(-)`. That churn is formatting, not semantics: the
file was reserialized from `indent=2` to `indent=1` (line 2 changes from `  "schema"` to
` "schema"`). Parsed comparison:

```
entries: 493 -> 497
parsed-entry multiset: removed/edited = 0, added = 4
key-frequency per entry: identical key sets (no key lost)
added entries: class=record, verdict=gap-minor, commands_executed_count=1,
               blocking_gaps=0, wrong_expectations=0, minor_gaps=0,
               traces=1 each, >=1 non-ignored input each
```
All four appended entries are the refresh sections, at `read_rev=e423c41ba253`, section
`start/end` and `sha256` exactly equal to `refresh-specs.json`; every spec path is present in
the entry's `inputs` (plus `SKILL.md`, which the monitor ignores for the input gate). Every
recorded input hash re-verifies at `e423c41` and still verifies at `b455001`, `d9c496b`,
`fbb01cf`.

Class-gaming check: `EXEC_VERDICTS = {executed-ok, gap-minor}`,
`REC_VERDICTS = {verified-record, gap-minor}` (`round-18/measure.py:125-129`), and the
commands gate (gate 3) requires `commands_executed_count>0` for both classes. With verdict
`gap-minor` and `cmds=1`, `instruction` and `record` credit identically — so the
`instruction → record` class on section 1436 (all priors `instruction`) is **score-neutral**,
not a laundering move.

Strict trace gate (gate 5), checked independently for each of the four traces:

```
schema = tameshi-trace-inputs-v1 ; exit = 0 ; external = {} ; live_lane_reads = {}
trace inputs ⊆ entry inputs, all digests equal (no trace-input-drift)
SKILL.md digest in trace == sha256(blob e423c41:SKILL.md) == 2381873162fc…d35a
```
No `external` path under the live lane root; nothing reads the live lane.

## Findings by severity

**No HIGH or MEDIUM finding. The no-harm assertion survives every attack I could mount.**

**LOW-1 — the refresh rewrote all 40,186 ledger lines for a 4-entry append.**
`b455001` reserializes `ledger.json` from indent 2 to indent 1, so the commit reads as
`+40709/−40186` and every pre-existing entry's line range changes. Semantically inert
(parsed multiset: 0 edited, 4 added), but it destroys line-level blame/history for the whole
calibration ledger at that commit and makes "the refresh entries are the only delta" a
property only structural comparison can confirm — a human reading `git diff` cannot. Suggest
the next ledger touch preserve the file's existing indentation. Evidence:
`git diff --stat 796e08b..b455001 -- .ufo/evidence/round-21/coldread/ledger.json`.

**LOW-2 — commit message `b455001` claims "refresh specs+receipts citing S103"; only the
receipts cite it.** `grep -rn "S103\|s103" .ufo/evidence/round-36/coldread/` hits
`refresh-receipts.json` only (lines 32/60/88/116, plus `cited_source_row: "S103"`);
`refresh-specs.json` contains no S103 reference, and no refresh entry lists the S103
snapshot (`.ufo/evidence/round-36/src/s103-git-hash-object.html`) among its `inputs`. The
contract's `new_source_row` intentionally requires only a `SOURCES.md` row, so this is a
wording overstatement in the commit message, not a missing artifact.

**LOW-3 — the SCORECARD round-36 block states the after measurement one commit before that
commit exists.** The block lands in the content/control commit `e423c41`, and its prose reads
"The strict cold-read monitor prints `calibration_restraint_score: 6, sections_covered 60/64`
at base `796e08b` and `8, 64/64` at the refresh commit" — but the refresh commit `b455001` is
its child, and `measure.py` measures by `--rev`, so `8` could not have been observed when
that tree was written. The block's table cell does say "target", so the value is honest and
the later receipt (`d9c496b`) confirms 8/64/64; only the prose tense/chronology is
overstated. A reader diffing `e423c41` alone would see an unearned present tense.

**NOTE — the four new entries omit `external_inputs`** (493/497 other entries carry it). The
monitor aggregates but does not gate on it, so credit is unaffected; recorded here because
the ledger is the calibration surface and this round's external source (S103) is attested
only at the receipt layer.

## Residual risk and verification gaps

- I did **not** re-execute the monitor (outside this seat's assignment; the receipts are the
  L1's). My independent layer is structural: gates 1–4 satisfied by field inspection,
  gate 5 verified by re-hashing traces/inputs at their revs, gate 6 supported by the
  per-section `vetoed=False` records in all three receipts plus `input-drift`-only reasons.
  A monitor-level re-run at `fbb01cf` would close the remaining gap; note that the pinned
  measurement commit is the refresh commit by design, and no post-refresh commit in this lane
  touched any cited input, so the drift rule does not fire at the tip either (all four
  entries' input hashes still verify at `fbb01cf`).
- `SKILL.md` being byte-identical means C1 restored credit **without** editing the appraised
  surface — the refresh is a ledger/trace action. That is what the contract's kill rule
  requires, and it is the strongest single fact for no-harm: no owned-axis surface was
  touched to buy the score.
- C2 (`c1-measure-v2.py`) is byte-pinned and untouched by this review; its predicate and
  deciding run are other seats' scope.

## Tooling

No installs or upgrades were needed or performed. All checks used the system `git 2.x`,
`python3 3.14`, `sha256sum`, `grep`.

## Verdict

**PASS — no-harm assertion holds.** r35 tip → refresh commit touches exactly one owned-axis
file, `corpus/QUALITY.md`, with **12 insertions and 0 deletions** (criterion 72 appended after
an intact criterion 71). `tools/` is tree-identical (`66c2e00c…`, 0 changed paths) with both
frozen tools matching their contract pins; `SHONEN.md` is blob-identical, so no box flipped;
`SKILL.md` and `PROVINCE.md` are blob-identical, so the calibration lift was not bought by an
edit to the appraised surface; zero deletions exist anywhere in either range. The ledger
delta is strictly append-only (0 rewritten entries, 4 appended, traces and input hashes
re-verify). Three LOW hygiene/honesty findings above, none of which regress credit or
invalidate C1.
