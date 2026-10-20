# K03HistoricalInputsTamper — critic report on contract A (`historical_inputs`)

Seat: TameshiR17.K03HistoricalInputsTamper (critic, round 17 wave 1). Lane tip 98bea7da5801f4bc58e4187690ee1687c8a5061f.
Axes affected: **operability** (R16-OP1 green-after) and **calibration/quality** (whether a clean exit still means what SCORECARD.md:246 says).

## Method

- The staged v2 tool did not exist yet (`.ufo/waves/round-17/staged/tools/` absent), so I attacked a **contract-A model**: a /tmp copy of `tools/evidence-disposition.py` at 98bea7d. The copy accepts `evidence-dispositions-v2`. For each `historical_inputs` key it enforces the contract's checks: `tools/` prefix, key in expected.inputs, the `show-toplevel` identity guard and 40-hex rev. It then reads the bytes with `git -C root cat-file blob --end-of-options REV:PATH`. Every other behaviour is v1. All results below come from this model. They are counterexamples to the **contract text**. Whether the real staged tool exhibits them is [INFERENCE] until X01's build is re-run against these fixtures.
- Sandbox: fleet-mirror clone at 98bea7d under `/tmp/tameshi-r17w1-K03HistoricalInputsTamper-6edEHB` (siblings symlinked). There were no lane writes except this report.
- Baseline at the tip: the v1 round-14 manifest gives exit 2, `expected_input_digest_mismatch`, `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`. This matches `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt`.

## Facts the objections rest on

| Fact | Command | Observed |
|---|---|---|
| Only one pinned `tools/` input moved | live and HEAD sha256 of the 4 `tools/` keys in `round-13/expected.json` inputs | pin-disposition `297253971dab`, witness-metadata `df3390682a04` and bash-witness-study `49e9e5e20b73` all equal their pins; mutate-and-run `0673d2e5374b` ≠ pin `75ed934dc863` |
| Which **expected** checks name each tool in their receipt argv | parsed `verification.json` and `producer-oracle-repair.json` | pin-disposition: `pin_live`, `pin_selftest`. witness-metadata: `metadata_corrected`, `metadata_old_null`, `metadata_selftest`. bash-witness-study: `producer_after`, `producer_after_oracle`, `witness_check`, `witness_count`. mutate-and-run: `producer_before_oracle` and `producer_after_oracle` (`--runner tools/mutate-and-run.sh`), plus receipt-only `frozen_and_guardrail_unchanged` |
| The runner move changes no replacement receipt | `producer-oracle.py --source {producer-before.py, bash-witness-study.py} --runner {live 0673d2e5, git-show 28aeef4 75ed934d}` | before-oracle: exit 1 under both runners, stdout sha `2125a67b4552` under both, `kind FAIL` present. after-oracle: exit 0 under both, `WITNESS_SELFTEST: 41/41 pass`, `cmp` SAME. Both match the retained receipts (exit 1 / `VERDICT: FAIL`, exit 0 / `VERDICT: PASS`) |
| Revs on master that hold the 75ed934d runner | `git rev-list` over `tools/mutate-and-run.sh` | 606716f (round 10, 2026-10-14) through e69b488, the commit just before c699c8c |
| Revs that hold **all four** tool pins | loop over `git rev-list 98bea7d` | 4acc607 … e69b488 (16 commits). All of them hold expected.json `a016079438e9` |
| X01 is told to waive every tool | `.ufo/waves/round-17/dispatch1.json:449` | "`historical_inputs` for EVERY `tools/` path pinned in … expected.json `inputs`, at one 40-hex commit that is an ancestor of master" |

## Counterexamples (model runs, `--root <clone> --json`)

| # | Attack | Model exit / id | v1 would say | Hidden? |
|---|---|---|---|---|
| T1 | **Blanket waiver hides live tamper.** v2 marks all 4 `tools/` keys historical at 28aeef4, then 1 line is appended to the live `tools/pin-disposition.py` (`git status`: ` M tools/pin-disposition.py`) | **0 clean** | 2 `expected_input_digest_mismatch` (`observed 754081cb… expects 297253971dab`). The same tamper under a minimal (runner-only) v2 also gives 2 | **yes**. 3 un-moved instruments that are the argv of 9 expected checks lose live verification, for zero operability gain |
| A1 | Rev not an ancestor: a dangling `commit-tree` of 28aeef4's tree, "forged: not on master" (`merge-base --is-ancestor` → 1, `branch -a --contains` → none) | **0 clean** | n/a | the bytes are genuine, so this is **false provenance**: the payload would state `expected_inputs_historical: {runner: <unreachable commit>}` |
| A2 | Rev is a **tree** id (40-hex `a3c19c7b…`, `cat-file -t` → tree) | **0 clean** | n/a | false provenance, because "rev" is not a commit at all |
| A3 | Rev predates the evidence epoch: 606716f (round 10; `round-13/expected.json` absent there) | **0 clean** | n/a | false provenance. Nothing binds the rev to the round whose receipts the gate reconciles |
| A4 | `git replace 98bea7d <fake>`, where fake is the HEAD tree with the runner swapped to the 75ed blob. Rev claimed = HEAD. `is-ancestor` → 0 (true) | **0 clean** | n/a | **yes**: the tip's real runner is 0673d2e5, but the payload attests that the tip held 75ed934d. With `GIT_NO_REPLACE_OBJECTS=1` → 2 `expected_input_digest_mismatch` |
| A4b | `.git/info/grafts` lists `98bea7d <dangling>`. The A1 commit becomes an "ancestor" (`is-ancestor` → 0) **even with `--no-replace-objects`**. Only `GIT_GRAFT_FILE=/dev/null` restores the correct answer (exit 1). git 2.56.0 still honours grafts and only prints a deprecation hint | n/a | n/a | defeats a naive ancestry guard |
| A5 | Environment `GIT_DIR=<foreign>/.git GIT_WORK_TREE=<lane>`. A foreign repo with a commit `36c60511…` holding the genuine 75ed bytes; the lane does not have that object | **0 clean**; `show-toplevel` prints the lane path, so the identity guard **passes** | n/a | the identity guard is defeated by environment. Without that environment: 2 `historical_input_unavailable` |
| A6 | Forged bytes at a rev (foreign commit; runner bytes + `#forged`) | 2 `expected_input_digest_mismatch` (`observed 264b768f…`) | — | **no**. sha256 against the expected.json pin defends the content |
| ctrl | Minimal v2 (runner only, rev 28aeef4): `dispositions` / `dispositions-before` | 0 clean / 1 failed | — | this is the intended green-after/red-before, reproduced |

The direct answers to the Target follow from these runs:
- **Choose a rev with forged bytes?** No. The sha256 pin holds (A6).
- **Rev not an ancestor of master?** Accepted (A1, A2, A3). The rev field is unverified provenance, and replace refs, grafts and `GIT_DIR` let it lie even for ancestors (A4, A4b, A5).
- **A `tools/` path whose live bytes are what actually ran?** Yes, and this is the real tamper hole (T1). The waiver is not limited to moved instruments. The dispatch instructs exactly the blanket form.

## Does the gate still mean SCORECARD.md:246 "effective expectation reconciliation"?

- The row's claim, "account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession", concerns retained receipts. The tool's own docstring (`tools/evidence-disposition.py:10-13`) says it never re-executes argv and "does not prove that any recorded command was rerun". So re-pinning the runner to its round-13 git bytes **preserves the meaning, for the runner only**.
  - The runner is never the evaluated subject. It is copied as a fixture by `producer-oracle.py:18`.
  - The two receipts that name it reproduce byte-identically under both runners (Facts table, row 3).
- With the blanket waiver (T1) the meaning **changes**. A clean exit no longer implies that the shipped `pin-disposition.py`, `witness-metadata.py` and `bash-witness-study.py` are the bytes behind the 9 expected checks they produced. v1 guaranteed that at every clean run (`:1180-1192`). That is a lost guarantee, and AXES treats a trade anywhere as not an improvement.
- The payload's only new disclosure is `expected_inputs_historical`. The text mode prints one summary line plus ROW/FINDING lines (`:1093-1119`), and nothing there says that a waiver applied. A registry row that greps stdout for `clean` cannot tell "live-verified" from "historical-waived".
- The spotcheck's complaint (§3, bullet 1) was that the gate "cannot tell this by-design mismatch from tampering". Contract A as written still cannot. It reads git for the runner and **never looks at the live runner**, so an uncommitted working-tree edit of `tools/mutate-and-run.sh` is as invisible as the committed 05a2247 move [INFERENCE from the contract text: the live path is skipped for historical keys].

## Comparison with the closure's options (spotcheck §6 item 1)

| Option | Verdict | Why |
|---|---|---|
| (a) appended superseding pin for `tools/mutate-and-run.sh` via the lane's pinning path | weaker for this gate | A pin of `0673d2e5` attached to round-13 receipts that were produced with `75ed934d` is false provenance, unless the two oracle checks are re-run under the live runner and retained as new receipts. That has become cheap: the outputs are byte-identical (Facts row 3). But it adds a second receipt authority beside `producer-oracle-repair.json`, which is a duplicate-authority risk. |
| (b) read the historical runner from git (contract A) | **correct choice, if guarded** | The bytes are provably genuine (sha256, A6) and the receipts stay immutable. The defects are scope (T1) and provenance (A1–A5), and both are fixable inside the tool. |

## Required guards (smallest safe correction, all inside the v2 code path; v1 untouched)

1. **G1 `historical_input_unneeded` (exit 2).** Read the live file as v1 does. If its sha256 equals the pin, the key must not be waived. This blocks T1 and makes the waiver set derived from facts, not from author choice. **Correct X01's manifest instruction** (`dispatch1.json:449`): only `tools/mutate-and-run.sh` qualifies at 98bea7d.
2. **G2 the move must be committed.** For a waived key:
   - The live bytes must equal `HEAD:<path>` (no working-tree drift).
   - `git log --format=%H <rev>..HEAD -- <path>` must be non-empty. Otherwise exit 2, as `historical_input_uncommitted` or `historical_input_unavailable`.
   - This is the piece that actually separates "instrument moved by a lane commit" from tampering (spotcheck §3).
3. **G3 rev is a commit, reachable, in the evidence epoch.**
   - `git cat-file -t <rev>` must be `commit` (A2).
   - `git merge-base --is-ancestor <rev> HEAD` must hold (A1).
   - `<rev>:<expected_file>` and every v1 `inputs` path that exists at rev must hash to their pins (A3). This binds the rev to a commit that already carried the frozen evidence. For the round-17 manifest, prefer `64314783836bb0d05ad06a774d7310fd3a23b5bd`, the capability row's "executable measurement6431478", which holds all pins.
4. **G4 hermetic git.** Run every git call with every `GIT_*` variable removed from the environment and with:
   - `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` (A4, A4b);
   - `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`;
   - `--no-optional-locks`.

   Refuse with exit 2 if `refs/replace/*` exists or `rev-parse --is-shallow-repository` is true. Additionally require `realpath(rev-parse --absolute-git-dir) == realpath(root)/.git`, not only `show-toplevel` (A5). This reuses the lane's own GIT_DIR lesson (SKILL.md, round-14 table, row 5).
5. **G5 tree-entry mode.** `git ls-tree <rev> -- <path>` must be a 100644 or 100755 blob, not a symlink or gitlink. Cheap, and it closes the remaining "not a regular file" asymmetry with `safe_file`.
6. **G6 disclosure.** Text mode must print `HISTORICAL <path> rev=<rev> live=<sha> pin=<sha> named_by=<expected checks>` lines. The JSON payload must carry the same, plus `status_basis: "historical_inputs"`. The registry row (contract B) for the v2 manifest must assert `stdout_contains` on that line, so that "clean" cannot be read as live verification.
7. **G7 `supersedes` is not merely informational.** Rows and `expected_file` must equal the superseded v1 manifest's parsed rows. v1 `inputs` must be a subset of v2 `inputs`, with equal digests. Otherwise exit 2. Without this, the declared lineage is unchecked text.

Selftest cases the builder must add, each red on the plain contract model and green with the guards:
- T1 (blanket waiver plus a live edit of an un-moved tool → 2);
- A1, A2, A3 (rev guards → 2);
- A4 and A4b (replace refs and grafts → 2);
- A5 (`GIT_DIR` environment → 2);
- a working-tree edit of the waived tool (G2 → 2);
- the control (minimal waiver → 0; before → 1).

Recommended evidence: retain the runner-parity replay (Facts row 3) as a round-17 receipt. It is the measured basis for calling the runner move behaviour-neutral for this gate.

## Tooling

No installs or updates. Used git 2.56.0, python3 and coreutils already on the host.

Verdict: **falls** — contract A as written lets `historical_inputs` hide live tampering of un-moved instruments (T1, which the X01 dispatch's "EVERY `tools/` path" instruction would ship) and accept false rev provenance (A1–A5); with guards G1–G7 (G1–G4 required) it holds and preserves the SCORECARD:246 meaning for the one moved runner.
