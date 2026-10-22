# R23-REATTACK MembershipExact (round 25, w1, leaf reviewer)

**Verdict: AGREE.** At lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`, `tools/command-binding.py` gives the exact verdict on every membership case the item names: unknown-extra receipts with full coverage, zero receipts, missing-first, duplicate receipts, and clean reorder. I found no input that returns a clean verdict (exit 0) when membership is wrong. None of the residuals below changes an exit code on the current tool. The most important one is a gate gap (F1): no retained fixture pins zero receipts, so a regression that false-cleans that case passes every retained gate I ran.

## 1. Target and revision

- Item: the round-23 prompt for MembershipExact (`.ufo/waves/round-23/spec2.json`, entry `MembershipExact`) matches the re-attack target text. The round-23 seat died and produced no output (see F5).
- Binding under attack: `tools/command-binding.py`, `evaluate()` at `:65-113`. Receipt structural pass `:86-92`; duplicate short-circuit `:94-97`; membership `:99-100`.
- Revision facts (read-only git, `GIT_OPTIONAL_LOCKS=0`):
  - `tools/command-binding.py` sha256 at c9ff09f = HEAD `5b69fb2` = lane worktree: `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d`.
  - `git diff c9ff09f HEAD -- tools .ufo/evidence/round-23 .ufo/evidence/round-24 SKILL.md` is empty.
  - Round-23 file (commit `496d212`) sha256 `d533dc1ef114234a8ca1d6a8155f052c9b8f5001f2f4918b3eb6a3f3f59af954`. A `diff` against the current file shows one hunk, at lines 164-169 (the selftest fixture loader, which now also reads the round-24 fixtures). `evaluate()` and `check()` are unchanged since round 23.
  - Frozen artifacts (worktree equals c9ff09f; sha256 prefixes): round-23 `extra-cases.json` `87bffdc8…`; round-24 `extra-cases.json` `6ad7842f…`; round-23 `measure.py` `81274963…`; round-23 replay `bundle.json` `3d6c99b7…` and `expected.json` `0831c9c8…`; source-read `bundle.json` `db620668…` and `expected.json` `70f357e3…`.

## 2. Supersession (`tools/registry.json` at c9ff09f)

- `command-binding-selftest` (line 928, expects `38/38`) is superseded by `command-binding-selftest-r24` (line 961, active, expects `44/44`).
- `command-binding-frozen-clean` (939) is superseded by `command-binding-frozen-clean-pinned` (971, active, requires bundle sha `3d6c99b7…`).
- `command-binding-source-read-red` (950) is superseded by `command-binding-source-read-red-pinned` (981, active, requires bundle sha `db620668…`).
- The round-23 rows are not active. Their active successors were run below and pass. `SKILL.md:2019` (gate row) and `SKILL.md:2054-2056` (supersession) agree with this.

## 3. Commands run (scratch only; the lane was not executed)

Snapshot: `GIT_OPTIONAL_LOCKS=0 git -C <lane> archive c9ff09fb41fb8aac5fc335faf10858ff606bd5df | tar -x -C /tmp/rmex/c9ff`. Copies of the round-23 tool and of the current file live under `/tmp/rmex/r23` and `/tmp/rmex/cur`.

- `python3 tools/command-binding.py --selftest` (snapshot) → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0.
- `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` → `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": []}`.
- `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/source-read-bundle.json --expected .ufo/evidence/round-23/source-read-expected.json --json` → exit 1, `finding_ids: ["ARGV_MISMATCH"]`, `bundle_sha256` `db620668…`.
- `python3 .ufo/evidence/round-23/measure.py --repo /tmp/rmex/c9ff` → `discriminated 10 / 10`, `tool_sha256 9230c68e…`.
- `python3 .ufo/evidence/round-24/measure.py --repo /tmp/rmex/c9ff` → 11 of 11 rows discriminated (K1-K11; not membership-specific).
- `python3 /tmp/rmex/replay2.py <tool> <root>`: serial replay of all 25 retained cases (19 round-23 + 6 round-24), each with a fresh temp dir. The c9ff09f tool has 0 mismatches; the round-23 tool has 0 mismatches.
- `python3 /tmp/rmex/probe.py <tool>` (one fresh temp dir per bundle, serial). Identical output on the c9ff09f tool and the round-23 tool:

| Probe (membership-relevant) | exit | finding_ids |
|---|---|---|
| control, clean | 0 | `[]` |
| unknown extra, full coverage (clean copy; `One`; `one\u00a0`; bad fields) | 1 | `MEMBERSHIP_MISMATCH` (all four) |
| zero receipts, requirements kept | 1 | `MEMBERSHIP_MISMATCH` |
| zero requirements, with or without zero receipts | 2 | `INVALID_BUNDLE` |
| receipts key absent / null | 2 | `INVALID_BUNDLE` |
| missing first / missing last / missing first plus extra | 1 | `MEMBERSHIP_MISMATCH` (all three) |
| undeclared receipt (its requirement row removed) | 1 | `MEMBERSHIP_MISMATCH` |
| duplicate clean / duplicate bad argv / duplicate bad exit first | 1 | `DUPLICATE_COMMAND` (all three) |
| duplicate plus unknown extra | 1 | `DUPLICATE_COMMAND` |
| duplicate masking an argv mismatch on another name | 1 | `DUPLICATE_COMMAND` |
| duplicate then malformed / malformed then duplicate | 2 | `INVALID_RECEIPT` (both) |
| reorder receipts / reorder requirements / reorder both | 0 | `[]` (all three) |
| requirement duplicate then malformed | 2 | `DUPLICATE_REQUIREMENT` |
| requirement malformed then duplicate | 2 | `INVALID_REQUIREMENT` |

- Expected-file probes: unknown key in `expected` → exit 2 `INVALID_EXPECTED` (`check()` `:120`, `:123`). Expected file missing → exit 2 `INVALID_INPUT`. Zero receipts pinned to their own digest → exit 1 `MEMBERSHIP_MISMATCH`.

## 4. Gate sensitivity (scratch mutants of the c9ff09f file, `/tmp/rmex/mutants.py`; production untouched)

| Mutant (one-line change) | selftest | frozen 25-case replay | round-23 ruler | zero receipts |
|---|---|---|---|---|
| ZR-SKIP-EMPTY-RECEIPTS: `if receipts and set(receipts) != set(requirements):` | **44/44 pass** | **0 mismatches** | **10/10** | **exit 0, `[]` (false clean)** |
| NO-MEMBERSHIP: membership finding removed | 41/44 | 1 mismatch | 8/10 | exit 0 |
| DUP-FIRST-WINS: duplicate `return` replaced by `continue` | 43/44 | 0 | 9/10 | exit 1 |
| MISSING-ONLY: check only `requirements - receipts` | 43/44 | 1 | 10/10 | exit 1 |
| EXTRA-ONLY: check only `receipts - requirements` | 43/44 | 0 | 9/10 | exit 0 |
| ORDER-SENSITIVE: compare name lists in order | 43/44 | 1 | 10/10 | exit 1 |

Reading: every membership mutant except ZR-SKIP is caught by the selftest. ZR-SKIP changes only the empty-receipts case, and it returns a false clean there. No retained gate I ran catches it.

## 5. Findings

**F0 (verdict level): none.** Every membership case in section 3 gives the exact verdict. Reorder stays clean, and missing, extra, zero-receipt and duplicate cases fail with exit 1 and a membership or duplicate finding. Malformed inputs exit 2 and never reach a clean verdict.

**F1 (residual, medium; gate gap): zero receipts is unpinned.**
- No retained fixture has `receipts: []` with nonempty requirements. The selftest `missing` case (`:151`) pops one receipt, and `unknown` (`:153`) renames one.
- Pure missing-first (no extra receipt) also has no retained fixture. My probe shows exit 1. The selftest `unknown` case covers the first requirement missing only together with an extra receipt.
- Evidence: mutant ZR-SKIP passes the 44/44 selftest, the 25-case replay and the 10/10 ruler, and returns exit 0 on zero receipts. I did not run the round-24 ruler against this mutant; its rows are not membership-targeted.
- Smallest safe correction (production change; not made here): add a new round-25 fixture file (leave the frozen round-23 and round-24 files untouched) with two cases: zero receipts → exit 1 `MEMBERSHIP_MISMATCH`, and first requirement absent with no extra → exit 1 `MEMBERSHIP_MISMATCH`. Extend the selftest loader at `:164-169`, and supersede the active `command-binding-selftest-r24` row with the new count.

**F2 (residual, low; diagnostic only): a duplicate short-circuits the other finding IDs.**
- `:95-96` returns `1, ['DUPLICATE_COMMAND']` before membership (`:99-100`) and the per-name checks. Probes: duplicate plus unknown extra gives only `DUPLICATE_COMMAND`; duplicate plus an argv mismatch on another name gives only `DUPLICATE_COMMAND`. Exit is 1 in both.
- The knowledge doc documents only "stable finding ID" (`corpus/knowledge/required-command-binding.md:24`). No retained fixture pins a mixed duplicate-plus-other finding list. That the early return is intended is [INFERENCE].
- Smallest safe correction: document `DUPLICATE_COMMAND` as terminal, or collect duplicate and membership IDs before returning. The verdict is unaffected either way.

**F3 (residual, low; finding IDs only, exit stable): the requirements side is row-order dependent.**
- `:81` (`INVALID_REQUIREMENT`) and `:82-83` (`DUPLICATE_REQUIREMENT`) run in one loop. `[duplicate, malformed]` gives `DUPLICATE_REQUIREMENT`, and `[malformed, duplicate]` gives `INVALID_REQUIREMENT`. Both exit 2.
- The receipts side was repaired so the structural pass finishes first (`:86-92` before `:94-96`). That is the round-23 repair described in `corpus/lessons/round-23.md:79-83`. The requirements side was not repaired.
- Smallest safe correction: run a full requirements structural pass before the duplicate check, mirroring the receipts side.

**F4 (scope note, documented; not a defect): membership is relative to the bundle's declared requirements.** The docstring (lines 1-16) says the gate does not establish "complete page coverage" and does not prove producer authenticity. A bundle that declares fewer requirements than the registry is clean. "Full coverage" in this report means full coverage of the declared set.

**F5 (provenance): the round-23 seat left no usable output.**
- `.ufo/evidence/round-23/accounting/bundle.json:1495-1499` records `status: failed`, `replaced: false`.
- `.ufo/waves/round-23/original-outcomes2.json`, entry at `:1142`: `report_file: null`, `final_output_chars: 0`, and a `death_basis` saying the parent session ended and the child transcript ends without `session_exit`.
- The transcript that entry names (`.../TameshiR23/TameshiR23.MembershipExact.jsonl`, sha256 `8bcc2fda…`) is absent. `.../TameshiR23/TameshiR23.MembershipExact.md` exists but is 0 bytes (sha256 `e3b0c442…`, the empty-input hash).
- `.ufo/waves/round-23/w2/MembershipExact*` does not exist.
- So there is no earlier membership result to confirm or rebut. This report is the first executed attack on these artifacts.

## 6. Does the round-23 finding still apply at c9ff09f?

No counterexample reproduces. Round 23 produced no finding, because the seat never reported, so nothing from round 23 is confirmed or refuted. The membership claims hold identically on the round-23 tool and at c9ff09f. The active successors of the round-23 registry rows pass. The membership logic is unchanged since round 23.

## 7. Process disclosures

- Tool installs or updates: none. Used python3, git (read-only), sha256sum, tar and grep, all already present.
- Lane writes: none by me. One early lane command ran `git status --porcelain` without `GIT_OPTIONAL_LOCKS=0`. The lane `.git/index` mtime is `2026-10-22 05:19:39 -0300`, which may be that call's optional index refresh. Peers are also active in this lane, so I cannot attribute it with certainty. Every later git call used `GIT_OPTIONAL_LOCKS=0`.
- Two early parallel batches shared scratch filenames (`/tmp/rmex/b.json`, `/tmp/rmex/e.json`). Their outputs were discarded. Every number above comes from a serial rerun or a fresh temp dir.
- Lane state observed with the guarded `git status`: modified `tools/mte-interop.py`; untracked round-25 evidence and wave files. I touched none of them.
- No subagents spawned.

## 8. Verification gaps

- The mutant table covers six hand-written mutants. It is a sensitivity probe, not an exhaustive one.
- Producer authenticity and independent cold reads are out of scope, as the tool's docstring says.
- The dead seat's transcript is absent, so I cannot verify what it did before it died.
- `registry-check.py` was not run. The three active command-binding rows were run with their own argv in the snapshot.

## 9. Smallest safe correction (summary)

1. Add zero-receipt and first-requirement-only-missing fixtures in a new round-25 file, extend the selftest loader, and supersede the 44/44 row. This closes F1.
2. Optional: move the requirement duplicate check after a full structural pass (F3), and document the duplicate short-circuit (F2).

R23-REATTACK MembershipExact: AGREE
