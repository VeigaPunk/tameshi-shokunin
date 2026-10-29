# T57W1CritC1 — falsification of C1 (calibration), round 57

Seat: critic (leaf). Lane base `5e3569969b532310d2b8a3d130901757a3df356b`. Contract not edited.
Scratch: `/fast/scratch/hyaku/tameshi-r57/T57W1CritC1` (clone `--shared`, scripts). Scripts and outputs copied to `T57W1CritC1-receipts/`.
No tools installed. No lane file written. The only lane-tree writes are this report, the JSON beside it and the receipts dir.

## Verdict

C1 as written cannot tell a do-nothing control from honest work. Concretely:

1. One commit that adds a 51-line file, with one keyed excerpt per item, plus a ledger of 51 `fixed` rows, passes every arm once the Planned regex is fixed (S1 needs no fix; S2b and S3 need it). That is 0 real repairs.
2. `open` is a free sink. Naming an id in the newest Planned paragraph is the whole check. Naming all 51 passes all open-arm checks and fails only the fixed floor (S3b).
3. The inherited counter has three defects that make the contract's own target unreachable or false as written:
   - the Planned-id regex is `\bR4\d\.\d+\b`, so no `R5x.y` id is ever recognised as planned; every `open` row for rounds 50–56 fails (S2 inherited: `open_unplanned=17`; S3c: 51);
   - `BASE` defaults to `e3729de8`, so `fixed_this_round` counts real pre-base commits (S6: 7 counted with the default, 0 with the round-57 base);
   - any ledger row whose id is outside the frozen set is counted `extra` and fails the total, so the "49 original rows" can never be kept (S2c: `extra=49`, total 49).
4. The item set the contract names ("about 51") is not what the inherited extractor produces: it yields **41** on rounds 50–56 (round 54 contributes 0, because its items are bold-led paragraphs, which `ITEM_RE` does not match). My adapted extractor yields **51** (`extract57.py`), with two rules the contract does not state (absolute positions for unlabelled items; bold-led paragraphs under every routed heading).
5. The key arm is substring-based and its keys are lane-curated. Keys `open`, `mined`, `/tmp`, `077d431e` each accept an unrelated line. Five real items get a passing `fixed` row in one step each (§4).

Do not run the round-57 counter until the §6 changes 1–5 and 7 are made. Floors are not the defence; mechanical arms can be satisfied by one commit. The defence is the per-row closure sample, which the contract already names as `cannot_see`.

## 1. Do-nothing control (CTL_0 style): can it reach `C1_R57_PASS=true`?

Yes. Harness: `harness.py`, `scen.py` (output `scenarios-do-nothing.txt`; the block after "rerun with lane-curated keys" is the authoritative run). Probe = one new file `corpus/r57-probe.txt`, 51 lines `<key>: covered by the round-57 probe note for <id>, see the routed entry.` Ledger rows point at the probe commit; each excerpt is its own line. Empty-key items (R52.2, R52.6, R55.3, R56.1, R56.7) get their id as the lane-curated key.

| Scenario | Rows | Result (inherited code unless stated) |
|---|---|---|
| S1 51 fixed → probe, base = round-57 base | 51 fixed | **PASS** total=0, fixed_this_round=51 |
| S1b same, BASE default `e3729de8` | 51 fixed | **PASS** total=0 |
| S2 20 fixed + 14 declined + 17 open named | 51 | FAIL `open_unplanned=17` (regex bug) |
| S2b same, regex `R\d\d` | 51 | **PASS** total=0 |
| S2c as S2b, 49 base rows kept | 100 | FAIL `extra=49` (total 49) |
| S3 20 fixed + 31 open named, regex `R\d\d` | 51 | **PASS** total=0 |
| S3b 51 open named in Planned, regex `R\d\d` | 51 | FAIL `fixed_short=20 this_round_short=6` (total 26) |
| S3c 51 open named, inherited regex | 51 | FAIL `open_unplanned=51` |
| S4 51 declined (bulk decline), regex `R\d\d` | 51 | FAIL `declined_over=37 fixed_short=20` (total 63) |
| S6 7 real pre-base commits as fixed, rest declined, floors 0 | 7 fixed | this_round = **0** with the round-57 base; **7** with inherited BASE |

Cost of the cheapest passing tree: one commit (a new 51-line file) and a 51-row ledger, each row one small JSON object written by a script.

Which numbers need real work? **None of the three floors does.**
- fixed ≥ 20: satisfied by 20 probe rows (S2b, S3). No commit-per-row or excerpt-semantics check exists.
- declined ≤ 14: a cap, not a floor. It costs nothing to stay under (reason ≥ 40 chars is length-only). A bulk decline of all 51 (S4) fails the cap, so bulk decline is not itself the route; the route is 14 declines + open.
- this-round ≥ 6: satisfied by the same single probe commit. With the inherited BASE, real pre-base commits also count (S6), so this floor measures the wrong thing.

Open-row sink: S3 shows 31 open rows cost one line each and pass. The contract puts no cap on open. Open is the cheapest bucket and is effectively unbounded (up to N − fixed_floor = 31).

### Honest triage: how many items could I close in 20 minutes? [INFERENCE: time estimate, not timed]

Triage evidence: `triage-existing-commit-candidates.txt`, `five-items-cheapest-fixed-row.txt`, and the read-only `git show`/`grep`/`merge-base` checks in §7.

- Honest, verifiable closure in ~20 min, one file each: **R50.3** (superseding note for README F6/F10; README is pinned by the no-harm monitor, so it costs cold-read credit), **R51.6** (supersession note at `fleet-kill-rate-ledger.md:119`; knowledge entry, pinned), **R56.3** (19/19 recheck line + README index; pinned). **3 closable.**
- Already closed in history and verifiable: **R53.9** (`d33053f`: the six untracked round-53 files are now tracked; routed_at `2ef0a5ad` is an ancestor of `d33053f`), **R52.4** (`6db1d22` tracks `w3.ready`, `w3/`, `build-readers.py`; routed_at `c1d49d76` is an ancestor). **2 closed by history.**
- Not verifiable as closed: R52.5 (the cited commit `51d1f0eb` is a round-55 C1 fix and does NOT add the `fallback to /tmp` line; see §4); R52.2 (a round-52 LOG entry exists at `LOG.md:2449`, but the fixing commit is not identified).
- Cannot close in 20 minutes: **46** items. Examples: R51.1 (registry row + scope monitor + committed receipt), R51.4 (counter amendment + mutation attack), R53.1 (counter pathspec + re-run + receipts), R54.1 (controls re-run), R55.1 (C2 verdict at the measured revision), R56.1 (25-section anchor re-key), R50.2 (two SKILL/registry rows with verdict maps), R52.1 (re-key pipeline), R53.6 (uniform exit class across 4 tools with tests).

Recommended floors, not lowered after scoring: fixed ≥ 20 (kept, but each fixed row must introduce its excerpt, §6), declined ≤ 14 (kept), **open ≤ 17** (new). With open ≤ 17, fixed + declined ≥ 34 is forced, so the minimal honest-bucket route is fixed ≥ 20 with declined ≤ 14. Those numbers are a judgement, not a measurement; I cannot justify 20 from the lane's capacity beyond the triage above.

## 2. Is `open → id named in the newest Planned paragraph` forgeable?

Yes, by naming. Evidence: S3b (51 open rows, all ids named in a new `**Planned (round 58):**` paragraph appended to SCORECARD) passes every open-arm check. The `planned_ids` function:
- takes the **last** line starting `**Planned (round` in the file (position, not round number);
- collects the paragraph up to the first blank line;
- matches `\bR\d\d\.\d+\b` (after the fix) against the whole paragraph, so `R51.1 is fixed` or any prose mention counts.

Nothing checks that the paragraph is the current round's, that the id is a real open item, or that the paragraph does not also list the id as fixed. Combined with the uncapped open bucket (S3: 31 open), an open row is a sentence in SCORECARD.

Fix: order by round number, not file position; require the paragraph's round to equal the round that scores; cap open ≤ 17 (§1).

## 3. Universal-clause and gap attack on the target sentence

Target sentence (contract `before`/`target`), clause by clause:

- "every item of the frozen set … has exactly one ledger row": `exactly one` is enforced (`duplicate`, `missing`). "every item" is over a set the contract never enumerates (N is not stated; "about 51" in the lane notes). The inherited extractor gives 41 (§5). Duplicated ids in `defects.json` are not detected: `measure()` checks each defect against the same row, so an item merged into another is silently not checked. Observed in my first adapted run of the "position among unlabelled items" rule: round 51 emitted seven ids and `R51.1` absorbed the text of item 2. Fixed rule: absolute 1-based positions.
- "every row agrees with the tree": the universal runs over *all* rows, so every base row counts `extra`. This directly contradicts "the 49 original rows byte-identical to base" (S2c fails with `extra=49`). **No code checks byte-identity of the 49 rows**; the sentence is unenforced as written.
- "every evidence item … resolves": enforced.
- "fixed → a post-routing commit": implemented as `not is_ancestor(commit, routed_at)`, which is weaker than "a descendant of routed_at". I did not find a case where it matters (`ff2a821`, R54.6's sweep commit, is an ancestor of `650987a0` and is correctly refused, `fixed_bad=1`, see §4 and receipts). It is a definitional gap, not a demonstrated exploit.
- "and whose excerpt is absent there at routing time": checked by `show(routed_at, path)`; a file created after routing counts as absent. A commit need not introduce the excerpt (R52.5, §4).
- "a keyed evidence path … keyed": keys are substring matches (`k.lower() in excerpt.lower()`), and `path.endswith(k)`. Demonstrated cheap keys (§4): `open` (a status word, and a substring of "opened"), `mined`, `/tmp`, `077d431e`.
- "declined → reason ≥ 40 chars": length only; in S4 every row passed the reason check (`declined_bad=0`) and only the cap failed.
- "newest `**Planned (round` paragraph": position, not round (§2).
- "among the N new rows fixed ≥ 20 … at least 6 fixes carried by commits after the base": `base or BASE` defaults to `e3729de8` in `main()`, which the inherited code leaves in place. "after the base" is undefined in the target; I measured the default (S6: 7 vs 0).
- "C1_R57_PASS=true with total=0": the counter also needs the keys frozen. The pin covers `defects.json`, so keys are frozen only if that file is frozen after the keys are chosen. The contract does not say that.

Proposed target (replaces the current one):

> `C1_R57_PASS=true` with total=0 over the frozen set `.ufo/evidence/round-57/c1/defects.json` (51 items, R50.1–R56.7, sha256 pinned; ids are `R<round>.<label>` when the item's bold lead carries that label, else `R<round>.<absolute 1-based position in the routed list>`; each item's keys are frozen in that file): each of the 51 items has exactly one ledger row; no ledger row has an id outside the set except the 49 rows of rounds 40–49, which must be byte-identical to their bytes at base `5e3569969b53`; each of the 51 rows agrees with the tree at REV: every evidence item resolves (a lane path, 1 ≤ a ≤ b ≤ len, b−a ≤ 30, excerpt of 15–400 characters present in lines a..b, and a key matched as a whole token or a whole path, never as a substring); a `fixed` row names a full-hash commit that is an ancestor of REV, is not an ancestor of the item's routed_at, touches a keyed evidence path, and introduces its excerpt (absent in that path at the commit's first parent, present at the commit); an `open` row names its id in the paragraph of the highest-numbered `**Planned (round N)` block of SCORECARD.md at REV, and at most 17 rows are open; a `declined` row gives a reason of at least 40 characters; the totals are fixed ≥ 20, declined ≤ 14, and at least 6 fixes landed by commits that are ancestors of REV and not of the round-57 base; the seven spot-check files are byte-equal to their frozen digests.

Proposed kill sentence:

> The counter prints `C1_R57_PASS=false` and names the failing arm whenever any frozen item lacks exactly one row, any row fails a rule above, any row's key fails the token rule, or any floor is short; a refused row is a miss, not a removed item; the item set, the keys, the floors and the regexes are not changed after the first scoring run.

## 4. Attack evidence (cheap closures on real items)

`five-items-cheapest-fixed-row.txt` (single-row runs; all other rows declined with a real existing excerpt; floors 0). Each row below passes the `fixed` arm with no new commit and no repair:

| Item | Commit (existing) | Evidence path: excerpt (existing line) | Why it passes |
|---|---|---|---|
| R50.1 | `877eedee3` | `corpus/SOURCES.md:515`: "Round 52: one tier-A row added … opened and r…" | key `mined` (a status word from the item's backticks; substring of the excerpt) |
| R50.3 | `a41195dfc` | `corpus/README.md:618`: "\| F3 \| determinism precondition…\| open — README.md:589 …" | key `open` (status word present in the excerpt's own status cell) |
| R52.5 | `51d1f0eb9` | `tools/registry-check.py:764`: "fallback to /tmp, preserving CR47 semantics)…" | key `/tmp`; **commit does not add this line** (`git show 51d1f0eb -- tools/registry-check.py \| grep -c '^+.*fallback to /tmp'` → 0) |
| R53.9 | `d33053f75` | `.ufo/waves/round-53/w1/T53W1ExecR523.md:345`: "Write scope respected…" | path key; this one is a real closure (the item's own commit) |
| R54.1 | `2fec07ec5` | `SCORECARD.md:2569`: "`077d431e`** (5 amendments), which the deciding run uses…" | key `077d431e`, a commit hash in an unrelated pointer; the excerpt does not concern CTL_POS_c1 |

Triage search (`triage.py`, `triage-existing-commit-candidates.txt`): 7 of 51 items have a post-routing commit touching a keyed file with a passing excerpt, using path-like keys only. Basename-only keys (e.g. `T54W2Sent03.md`) were not searched, so this undercounts.

Keys that match too much: `keys_of` on the spot-check prose also yields line-anchor fragments: `R54.1` → `:162`, `R54.2` → `:157`, `R54.5` → `:79,100`. Each is a substring of any text containing that anchor. (Checked: `:162` occurs once in the round-54 spot-check, and the rule would accept any excerpt containing `:162`.)

## 5. Inherited code, bug-for-bug (round-50 `measure.py` and `extract-defects.py`, read at base, not edited)

- `planned_ids`: regex `\bR4\d\.\d+\b` (line 111). R5x ids never match (verified: `re.findall` on `R51.1 R53.2 R56.7` → `[]` with the R4 regex; receipt `planned-regex.txt`).
- `main()` calls `measure(...)` without `base`, so `BASE=e3729de8…` is used for `fixed_this_round` (line 254).
- `measure()` counts rows outside the frozen set as `extra` and fails the total (line 183).
- `extract-defects.py` run on rounds 50–56 (its `ROUNDS` changed, nothing else): `ITEM_RE` only matches `N. ` and `- `, so round 54's bold-led items are not found. Result: **41** items (round 54: 0), receipt `extractor-count.txt` / `inherited-extract.json`.
- Selftest: the round-50 selftest uses only `R40.x` ids, so none of the three bugs is caught by it.

## 6. Recommendations (for the L1; the contract is not edited)

1. Fix the Planned regex to `\bR\d\d\.\d+\b` and select the newest block by round number.
2. Pass `base=<round-57 base>` (`5e3569969b53…`) explicitly. Do not inherit `BASE`.
3. Replace the `extra` rule for the 49 base rows with a byte-identity check (rows compared by id against `git show BASE:corpus/routed-defects.json`), and drop `extra` only for those ids.
4. Fixed rows must introduce their excerpt (absent at the commit's first parent, present at the commit). This rejects R52.5 with `51d1f0eb`.
5. Keys are matched as whole tokens or whole paths, never as substrings; a status word such as `open` or `mined` is not a key. Freeze the keys in `defects.json` before scoring.
6. Floors: fixed ≥ 20, declined ≤ 14, open ≤ 17, this-round ≥ 6 against the round-57 base. The numbers are judgement; the arms are what matter.
7. Re-check the extractor: absolute positions for unlabelled items, bold-led paragraphs, every routed heading. Expected count 51. `extract57.py` produces `defects57.json` (51 items, unique ids).
8. Keep the contract's `cannot_see` line. A do-nothing control passes these arms, so the closure sample of support is the real defence; say so in the report.

## 7. Sweep commands run (lane read-only; fixtures in a scratch clone)

- `git -C <lane> show 5e3569…:<path>` for the contract, `measure.py`, `extract-defects.py`, `routed-defects.json`, the seven spot-checks, `SCORECARD.md`, `SOURCES.md`.
- `python3 extract57.py <lane> 5e3569…` → 51 items (`defects57.json`); `extract50-as-is.py` (`ROUNDS=range(50,57)`) → 41 items (`inherited-extract.json`).
- `python3 scen.py` (S1–S6, `scenarios-do-nothing.txt`); `python3 triage.py` (`triage.json`); `python3 five.py` (`five-items-cheapest-fixed-row.txt`).
- Ancestry: `git -C <lane> merge-base --is-ancestor` for `6db1d22`/`c1d49d76`, `d33053f`/`2ef0a5ad`, `ff2a821`/`650987a0` (both directions); `51d1f0eb` diff grep for `fallback to /tmp` (0 added lines); `git ls-files` for the round-52 and round-53 files.
- Not run: the round-57 counter (not in the lane at base); no mutation of the counter; no timing of real repairs.

## 8. What I could not falsify

- Whether the 51-item extraction matches a reviewer's eye-read (recall). My extractor is my own; I did not re-read all seven files by eye.
- Whether a `fixed` row's excerpt semantically supports the fix. I show it does not need to.
- Whether a `measure.py` at `round-57/c1` (not yet in the lane) corrects these. I attacked the inherited round-50 code the contract names.
