# R08 — R16-C2a: replacement draft for the round-14 recipe steps 2–3

Seat: `TameshiR17.R08R14RecipeRepair` (reviewer, wave 1, round 17).
Lane tip read: `98bea7da5801f4bc58e4187690ee1687c8a5061f`. Date: 2026-10-20.
Scope: draft and execute only. `SKILL.md` was not edited; no lane instrument was
staged or installed; nothing was installed on the host. This report is the only
write. Scratch root: `/tmp/tameshi-r17w1-R08R14RecipeRepair-bZweIU`.

## 1. Exact draft (8 lines, replacing `SKILL.md:1579-1586`)

```text
1. Read the historical expectations and raw observations before accepting a
   later summary; distinguish twelve expected rows from thirteen pinned inputs.
2. **Historical (was steps 2-3), round 14, runner 75ed934d…:** `--root .`
   returns 2 at this tip. From an extracted `git archive 28aeef4` tree, run
   `python3 tools/evidence-disposition.py --root <tree> --dispositions
   .ufo/evidence/round-14/dispositions-before.json --json` → 1 (producer_before),
   `dispositions.json` → 0. Live from the lane root (`--root . --json`):
3. `.ufo/evidence/round-17/dispositions-before.json` → 1, `.ufo/evidence/round-17/dispositions.json` → 0.
```

Block bytes: 648 (with trailing newline), sha256
`d8201f657fd5af019d783652e9405fb0b003b60623382220c4c78c9b988bc6f9`.
`cat -A` shows no trailing whitespace. Line 1 is byte-identical to the
original `:1579`; line 2 to the original `:1580`.

Content check against the target: round-14 recipe marked historical with the
runner pin `75ed934d…`; working archived invocation (`--root <tree>` at an
extracted `git archive 28aeef4`, run from that tree) -> 1 then 0; the
round-17 live-tree pair from the lane root -> 1 / -> 0.

## 2. Line-count proof

Method: substitute the 8-line region in the tip blob at `1579-1586` (1-based)
with the 8 draft lines.

| Fact | Command | Observed |
|---|---|---|
| Tip page lines | `git show 98bea7da…:SKILL.md \| wc -l` | `1812` |
| Draft lines | `wc -l /tmp/r08-draft.txt` | `8` |
| Region replaced | `SKILL.md` lines `1579-1586` | `8` lines |
| Candidate lines | `wc -l` on the reconstructed page | `1812` (delta 0) |
| Candidate bytes | `wc -c` | `127762` vs tip `127712` (+50) |
| Diff hunk | `diff candidate SKILL.md` | only `1581,1586c1581,1586` (step 1's two lines untouched) |
| Section count / sha | round-16 `measure.py:sectionize` on both pages | `54` sections each; exactly one sha changes: `## Effective expectation reconciliation — round 14`, `e8720037…` -> `ab0e307a…` |

The pre-edit section sha `e8720037…` is identical at `28aeef4` and at the tip
(page sha `97cf436b…` at `28aeef4`, `906fb649…` at the tip), i.e. the bucket
text is the round-14 text CR26 credited. Candidate page sha is `029b6226…`
(not authoritative: other wave writes will move the page; this section's shas
`ab0e307a…` is independent as long as no other seat edits this section).

## 3. Archived invocation executed (acceptance)

Setup inside my scratch root:

```
git -C <lane> archive 28aeef4 | tar -x -C /tmp/tameshi-r17w1-R08R14RecipeRepair-bZweIU
```

Runs, exactly the drafted command with `W` substituted for `<tree>` and cwd
inside that tree:

```
cd $W
python3 tools/evidence-disposition.py --root "$W" --dispositions .ufo/evidence/round-14/dispositions-before.json --json
  -> exit 1; status "failed"; counts expected_checks 12, effective 12,
     passed 11, failed 1, superseded 0; finding expected_contains_missing,
     expectation producer_before, detail "producer_before: stdout lacks
     'summary preserves top-level exposed declaration kind'"
python3 tools/evidence-disposition.py --root "$W" --dispositions .ufo/evidence/round-14/dispositions.json --json
  -> exit 0; status "clean"; counts expected_checks 12, effective 11,
     passed 11, failed 0, superseded 1; findings []
```

Both runs wrote 0 bytes to stderr. The archived tool and the tip tool are the
same bytes: sha256 `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95`
for both. Only the pinned input moved (`tools/mutate-and-run.sh`:
`75ed934d…` at `28aeef4`, `0673d2e5…` live).

Path-resolution check that makes the "run from there" wording load-bearing:
`cd /tmp; python3 $W/tools/evidence-disposition.py --root "$W" --dispositions
.ufo/evidence/round-14/dispositions.json --json` -> exit 2 `dispositions_missing`,
message `.ufo/evidence/round-14/dispositions.json`. `--dispositions` is read
against cwd, not `--root`.

## 4. Live red-before (executed; independently reproduced)

| Command (`--root .` from the lane root) | Exit | Finding |
|---|---|---|
| `.ufo/evidence/round-14/dispositions-before.json` | 2 | `expected_input_digest_mismatch`: `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…` |
| `.ufo/evidence/round-14/dispositions.json` | 2 | byte-identical |

This is the claim line 3 records ("`--root .` returns 2 at this tip"). It stays
true after the v2 install: the round-13 `expected.json` remains pinned at
`75ed934d…` and only the round-17 manifests may read a historical rev.
Cross-check, not a substitute: `S09R14RecipeOutcomes.md` reports the same
table (live 2/2; `git archive 28aeef4` 1/0; a fleet-mirror clone at `28aeef4`
identical modulo `root`).

## 5. Round-17 live pointer: manifests landed; real pair run on the staged v2 tool

The two manifests landed during this seat (`12:24` / `12:25`) and match
contract A's shape:

- `schema` is `evidence-dispositions-v2`; `expected_file` is
  `.ufo/evidence/round-13/expected.json`; `supersedes` names the round-14
  counterpart and is itself pinned in `inputs`;
- `inputs` holds the three round-13 pins plus the superseded manifest;
- rows: before `12` effective / `0` superseded, after `11` effective / `1`
  superseded (the round-14 row graph);
- `historical_inputs` names all four `tools/` paths pinned by `expected.json`,
  all at `4acc607d…`.

I re-derived the rev proof rather than trusting `historical-rev.txt`: for each
of the four `tools/` pins, `git cat-file blob 4acc607d:<path> | sha256sum`
equals the pin. Only `tools/mutate-and-run.sh` differs live
(`0673d2e5…` vs pinned `75ed934d…`), so a correct v2 read substitutes exactly
the one moved input.

Row pre-check (executed; a fixture, not the v2 tool): from a
`git archive 98bea7d…` tree I copied the two lane manifests, downgraded the
copies to `evidence-dispositions-v1` (dropping `supersedes` and
`historical_inputs`), and replaced the four `tools/` files with their
`4acc607d` blobs. The committed tool then reported:

| Manifest copy | Exit | Status | Counts |
|---|---|---|---|
| before | 1 | `failed` | 12 expected / 12 effective / 11 passed / 1 failed / 0 superseded; finding `expected_contains_missing` on `producer_before` |
| after | 0 | `clean` | 12 / 11 / 11 / 0 / 1 |

The only remaining variable was X01's implementation of `historical_inputs`.
The staged v2 tool landed while this report was being written
(`.ufo/waves/round-17/staged/tools/evidence-disposition.py`, sha256
`fab4cf7392fe75ba74d811b5a0722ebc6f9ed3923146495284019e71c2c7941f`, `12:33`).
Running it against the lane manifests from the lane root:

| Manifest | Exit | Status | Counts |
|---|---|---|---|
| before | 1 | `failed` | 12 expected / 12 effective / 11 passed / 1 failed / 0 superseded; finding `expected_contains_missing` on `producer_before` |
| after | 0 | `clean` | 12 / 11 / 11 / 0 / 1 |

Both payloads report `expected_inputs_historical` with all four `tools/` paths
at `4acc607d…`, so the historical read is the only substitution. This also
ran while the lane `HEAD` was detached at the incident commit (§7) and still
resolved `4acc607d` correctly, i.e. the read is rev-explicit, not
`HEAD`-based. The staged file was being edited at that timestamp; the
installed bytes are authoritative, so before this page is committed the L1
must run the real pair from the lane root:

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json  # require 1, producer_before unresolved
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json        # require 0 clean, 11 effective + 1 superseded
```

If either differs, line 3 must be corrected before landing. Contract A's
acceptance and W03's step 5 both state these exact outcomes.

## 6. Residual risk and verification gaps

1. The real round-17 pair was executed against the staged v2 bytes
   (`fab4cf73…`), not the installed `tools/evidence-disposition.py`. Re-run
   after install; row outcomes otherwise match contract A exactly.
2. The original step-2 warning "a matching exit1 is insufficient" is
   compressed to the `(producer_before)` tag. The exact expectation is still
   named, but the caution sentence is gone; with 8 lines fixed there is no
   budget for both.
3. Wave 2 must re-read this bucket at the new section sha (`ab0e307a…` at this
   candidate) and append the ledger entry; the round-16 credit at
   `e8720037…` no longer matches the page.
4. Line 3 gives `--root . --json` and both lane-relative paths but does not
   spell `--dispositions` there; it is reconstructible, and the round-17
   section carries the full entry command.
5. `producer_before` at `28aeef4` exits 1 because the retained check's stdout
   lacks the declared marker (`expected_contains_missing`), which is the
   round-14 documented "failed expectation, not mechanism proof" case. The
   draft states only the exit and its expectation, not a mechanism claim.

## 7. Lane-state incident observed (not this seat's write)

At `12:29:33-03:00`, after my evidence runs, three commits by
`tameshi <tameshi@selftest>` landed in the live lane (`f8832ef`, `0559c60`,
`e16adb7`; messages `selftest-fixture`, `-exec`, `-noexec`), leaving HEAD
detached at `e16adb7` and the index holding only `exec.sh`/`noexec.sh`/
`target.sh`; `master` remains `98bea7d` and every worktree byte this report
read is intact. I wrote no git state (read-only git only) and did not restore
it (the contract forbids lane git writes); the L1 was messaged with the
evidence. All commands in this report used explicit revs (`git show
98bea7d…`, `git archive 28aeef4`/`98bea7d`) or worktree bytes, so the
findings stand. Until HEAD is restored, any HEAD-based check (`measure.py`
`read_rev`, `trace-inputs.py` `rev`, `registry-check --rev`) resolves the
fixture commit.

## 8. Verdict

**built** — 8-for-8 line replacement proven (1812-line page unchanged, one
hunk, one section sha); archived invocation executed to exit 1
(`producer_before`) then 0 (clean) exactly as drafted; the round-17 live half
executed at 1 then 0 against the staged v2 tool (sha `fab4cf73…`) with the
declared historical reads, pending only a re-run on the installed bytes.
