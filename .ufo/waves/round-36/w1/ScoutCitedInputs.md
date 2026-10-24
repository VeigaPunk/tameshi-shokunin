# ScoutCitedInputs — round-36 w1

**Attacked:** the four round-36 cold-read ledger entries appended by the refresh commit — the last four entries (index 493–496 of 497) of `.ufo/evidence/round-21/coldread/ledger.json`:

| idx | start–end | heading | inputs |
|---|---|---|---|
| 494 | 131–245 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | 9 |
| 495 | 375–404 | `## Restore discipline — before/after identity, not continuous non-write proof` | 3 |
| 496 | 1380–1395 | `### The map — where a reader enters, artifact by artifact` | 4 |
| 497 | 1436–1448 | `### Where to enter — four readers` | 2 |

Entry 493 (round-32 remnant on the same 375 heading, traces `round-32/...`) confirms the tail boundary: exactly four round-36 entries. All four carry `read_rev: e423c41ba253357ab8c8513f0376dad9d38ab248`, `seats: ["L1 TameshiR36 author source re-anchor"]`, trace receipts `.ufo/evidence/round-36/coldread/traces/L1/source-{1..4}.json`, and `reports: [.ufo/evidence/round-36/coldread/refresh-receipts.json]`.

**Revisions:**
- r35 tip: `796e08b888849308d0c4d5e932e56833600a139f` (contract `claims.C1.before.rev`)
- round-36 content commit: `e423c41ba253357ab8c8513f0376dad9d38ab248`
- refresh commit (ledger entries appended): `b455001e2589b3f4f471d94a3de7e5e549b9f54c` — verified via `git diff --name-only e423c41b b455001e`, which touches only the ledger + round-36 coldread specs/receipts/traces.

## List 1 — enumerated input paths, existence + hash at refresh commit `b455001e`

Union of the four entries' `inputs` keys: **9 distinct paths**. Verification mirrors `.ufo/evidence/round-18/measure.py` `input_failures`: `git ls-tree b455001e -- <path>` (exists, blob mode) + `sha256(git cat-file blob b455001e:<path>)` vs recorded value. **All 9 exist as blobs and hash equal — zero drift, zero missing:**

| path | mode | sha256 | status |
|---|---|---|---|
| `SKILL.md` | 100644 | `2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a` | OK |
| `LOG.md` | 100644 | `a2223dc239aaa37ca9347e274084dc51426d741a1d2398eafa93c420d9340534` | OK |
| `SCORECARD.md` | 100644 | `1b0124a79a81c75bd5ddf345fcc2e41f8a3d9693f6a60c4261311419bfaddb56` | OK |
| `corpus/QUALITY.md` | 100644 | `f7382e201ba34f2786f18eae114ff5d896356f083e9fd10d09a9c93f8af58782` | OK |
| `corpus/README.md` | 100644 | `7c0fe513ac1999d1c489d0c0e6b0aa57c648c8b2855d0e4a28fd617dcbc2619f` | OK |
| `corpus/SOURCES.md` | 100644 | `16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7` | OK |
| `corpus/knowledge/closeout-r11.md` | 100644 | `f0894bf65aee32d81fde3f9233b8f35968e200bc7906d0035a786d3df94d1fd7` | OK |
| `corpus/knowledge/survivor-fixture-minimization.md` | 100644 | `116b56236bc468c84da4a3d2d97aa4e8cd84de2ca396ab202dfa1fd835802a86` | OK |
| `tools/mutate-and-run.sh` | 100755 | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | OK — byte-pinned artifact, recorded hash = frozen pin |

No path-hash conflicts between entries (identical recorded sha wherever a path repeats). `SKILL.md` is in `IGNORED_INPUTS` for the monitor's own gate but remains a recorded cited input and verifies identically.

## List 2 — inputs touched by the round-36 record commits (`git diff 796e08b..b455001e -- <union>`)

Touched — **4 of 9** (all in content commit `e423c41`; refresh commit `b455001e` touched none of them):

- `LOG.md`
- `SCORECARD.md`
- `corpus/QUALITY.md`
- `corpus/SOURCES.md`

Untouched across both commits — **5 of 9**: `SKILL.md`, `corpus/README.md`, `corpus/knowledge/closeout-r11.md`, `corpus/knowledge/survivor-fixture-minimization.md`, `tools/mutate-and-run.sh`.

**[INFERENCE]** The recorded hashes for the four touched paths are their post-edit `e423c41` bytes (unchanged through `b455001e`): the refresh re-anchored the citations to current content at `read_rev` `e423c41`, consistent with the C1 kill rule that the ledger entries + trace receipts are the only control→refresh delta.

## Commands run

```sh
git log --format='%H %s' -6                                    # rev identification
git show -s e423c41ba253357ab8c8513f0376dad9d38ab248
git diff --name-only 796e08b888849308d0c4d5e932e56833600a139f b455001e2589b3f4f471d94a3de7e5e549b9f54c -- <9 paths>
git diff --name-only e423c41b b455001e -- <9 paths>            # refresh commit alone: none
git diff --name-only 796e08b e423c41b -- <9 paths>             # content commit alone: the 4
git ls-tree b455001e -- <path>; git cat-file blob b455001e:<path> | sha256
python3 (read ledger.json, union inputs, verify loop)
```

Semantics source: `.ufo/evidence/round-18/measure.py` (inputs = lane-relative blob paths; `input-missing` / `input-not-blob` / `input-drift`; sha256 over `git cat-file blob` bytes; `IGNORED_INPUTS = {SKILL.md, round-17 ledger, default ledger}`).

**Verdict:** CITED-INPUTS VERIFIED — all 9 distinct input paths exist at refresh commit `b455001e` and sha256-match their recorded values; 4 of 9 (LOG.md, SCORECARD.md, corpus/QUALITY.md, corpus/SOURCES.md) were touched by the round-36 record commits, all by content commit `e423c41`, none by the refresh commit itself.
