# T49ExecR14Cmd — re-execute the round-14 recipe (C1 command re-execution)

Seat: T49ExecR14Cmd (leaf). Base `8ca67421111fa354b47b803358391d0b07fc6db9`; lane head
`455b2cd66fd9f237146a5355ca8bbc84f3071c50`. Section:
`SKILL.md:1563-1608` — `## Effective expectation reconciliation — round 14`; the recipe is
`SKILL.md:1579-1595`. The lane was read-only throughout; no tool was installed.

Deliverable: `.ufo/waves/round-49/w1/T49ExecR14Cmd.json`. Receipts:
`.ufo/waves/round-49/w1/T49ExecR14Cmd/` (`live-before-at-base.json`,
`historical-before-28aeef4.json`, `historical-after-28aeef4.json`, `live-after-at-base.json`,
`live-round18-manifest-at-base.json`, `live-round17-manifest-at-base.json`, `exits.txt`,
`replay-identity.txt`, `pin-movements.txt`, `step4-verification-lineage.txt`,
`step5-capture-context.txt`, `tree-unchanged.txt`, `env.txt`).

Scratch tree A: `git clone --shared` of the lane, checked out at base; `git -C $S/clone
rev-parse --show-toplevel` was asserted equal to the clone before any run, `git status --porcelain`
0 lines before and after. Tree B: `git -C <lane> archive 28aeef4 | tar -x -C $S/h`
(`28aeef498cc070c3183271b709bc79d344ff547a`). Both tools are self-identifying: tree A runs
`evidence-disposition.py r18` (sha256 `39ee5c5e…`), tree B runs `r14` (sha256 `1609a9df…`, exactly
the digest `.ufo/evidence/round-14/verification-final.json` pins for that input).

## Commands and outcomes

| # | tree / manifest | exit | section expectation | match |
|---|---|---|---|---|
| 1 | clone@base, `round-14/dispositions-before.json` | 2 `expected_input_digest_mismatch` (could_not_evaluate) | `SKILL.md:1581-1582` → 2 | yes |
| 2 | archive@28aeef4, `round-14/dispositions-before.json` | 1 failed, one finding `producer_before`/`expected_contains_missing` | `SKILL.md:1583-1584` → 1, "failing the unresolved producer_before assertion" | yes |
| 3 | archive@28aeef4, `round-14/dispositions.json` | 0 clean (11 effective, 1 superseded) | `SKILL.md:1585` → 0 | yes |
| 4 | clone@base, `round-14/dispositions.json` | 2 `expected_input_digest_mismatch` | `SKILL.md:1581` "both manifests now return 2" | yes |
| 5 | clone@base, `round-18/dispositions.json` | 0 clean | `SKILL.md:1586` live-tree pointer "(round-18 manifests since then)" | yes |

Exact argv of every row is in `T49ExecR14Cmd.json:commands[].argv`; exit codes are also in
`T49ExecR14Cmd/exits.txt`. Row 5 was added because row 3's sentence points at a live entry, and that
pointer is live: at base `.ufo/evidence/round-18/dispositions.json` runs clean and declares
`supersedes: .ufo/evidence/round-14/dispositions.json`.

## Findings (per clause)

1. **Step 2, live form — holds.** `T49ExecR14Cmd/live-before-at-base.json`: `exit: 2`,
   `status: could_not_evaluate`, `id/error.kind: expected_input_digest_mismatch`, mismatch line
   `tools/bash-witness-study.py: observed 60575e62a530… expects 49e9e5e20b73f…`. Both round-14
   manifests produce the same object (rows 1 and 4). Command row 1/4.
2. **Step 2, historical replay — holds and is stronger than an exit code.**
   `T49ExecR14Cmd/historical-before-28aeef4.json`: `exit 1`, `status failed`, counts
   `effective 12 / passed 11 / failed 1 / superseded 0`, findings
   `[{"id":"expected_contains_missing","expectation":"producer_before","detail":"producer_before:
   stdout lacks 'summary preserves top-level exposed declaration kind'"}]` — i.e. the declared kind
   assertion, not a bare exit. Command row 2.
3. **Replay identity.** After normalising only the top-level `root` key, the replay JSON equals the
   stdout stored in `.ufo/evidence/round-14/verification-final.json` for both checks:
   `unresolved_before` 5,366 B frozen vs 5,367 B replay (trailing newline) and `resolved_after`
   5,977 vs 5,978 — `equal_after_root_norm True` for both (`T49ExecR14Cmd/replay-identity.txt`).
4. **Step 3 — holds.** `T49ExecR14Cmd/historical-after-28aeef4.json`: `exit 0`, `status clean`,
   `superseded 1`, and the superseded row keeps
   `raw_check`/`raw_receipt`/`raw_mismatches`/`raw_retained: true` with both replacements
   (`producer_before_oracle` exit 1, `producer_after_oracle` exit 0) effective passes — the "only
   repair is that row's explicit supersession, keeping raw receipt/check and both passing
   replacements" clause. Command row 3.
5. **Step 4 — holds.** `.ufo/evidence/round-14/verification-final.json`: `disposition_selftest`
   exit 0 expected 0, last stdout line `SELFTEST: PASS (34/34)`; `unresolved_before` exit 1
   expected 1 with the producer_before finding; `resolved_after` exit 0 expected 0 clean;
   `supersedes` scopes the repair to "verification.json disposition_selftest failure only".
   `.ufo/evidence/round-14/verification.json`: `disposition_selftest` exit 1 expected 0 with
   `SELFTEST: FAIL (18/34 failed: …)` retained — the claimed "initial 18-of-34 fixture failures"
   survive verbatim. "The revision measured is recorded separately": `measured_commit`
   `0c6e36d0…` (initial) and `64314783…` (final), and
   `.ufo/evidence/round-14/verification-verdict.json` records
   `initial_failed_selftest_retained: "verification.json"`. Detail:
   `T49ExecR14Cmd/step4-verification-lineage.txt`.
6. **Step 5 — holds; not executed.** `find . -name capture-context.py -not -path './.git/*'` →
   `.ufo/evidence/round-14/capture-context.py` only. Source read: output
   `.ufo/evidence/round-14/context-receipt.json` (`capture-context.py:58`, docstring `:23` "no other
   path is written"); `write_receipt` `:583-602` does mkstemp → fsync → `chmod 0o644` →
   `os.replace` onto that path; and the write happens on the `invalid_input` branch (`:617-627`,
   write at `:622`) as well as after `decide()` (`:629-643`, write at `:632`) — only the usage error
   returns 64 first (`:613`). So "its historical output path replaces that frozen receipt" is exact,
   and the receipt is pinned: current bytes sha256 `05cb55b8…`, the digest pinned at `SKILL.md:1680`
   and `tools/context-capture.py:152-153`. `[INFERENCE]` from `decide()`'s
   `runner source digest …` branch (`:575`) plus the moved pins below: a re-run today would decide
   mismatch/1 and still overwrite the receipt, so it could not reproduce what it destroys. The
   maintained gate the step points at is `tools/context-capture.py --check` (docstring `:12`
   "writes nothing"). `SKILL.md:1632-1640` already marks step 5 archive-only. Detail:
   `T49ExecR14Cmd/step5-capture-context.txt`.
7. **Step 1, supporting.** The historical run reports `counts.expected_checks 12` and
   `len(expected_inputs_verified) 13` over `len(rows) 12` — the "twelve expected rows from thirteen
   pinned inputs" shape.

## Mismatches

**M1 — `SKILL.md:1581-1582`, the parenthetical cause is narrower than the observed error.**
The exit and kind are right, but the error names `tools/bash-witness-study.py`, not the runner.
Evidence: `T49ExecR14Cmd/live-before-at-base.json` (message), `.ufo/evidence/round-13/expected.json:11`
(the pin `49e9e5e2…`), and the movement history —
`git log --oneline 28aeef4..8ca67421 -- tools/bash-witness-study.py` → `58e5d53` (round 18) and
`370f2df` (round 21); `git log --oneline 28aeef4..98bea7d -- tools/mutate-and-run.sh` → `05a2247`
(round 16, the runner did move there); `git log --oneline 28aeef4..8ca67421 -- tools/pin-disposition.py`
→ `2a22ade` (round 17). At base **three** of the 13 pins differ
(`pin-disposition.py` `331529ea…`, `bash-witness-study.py` `60575e62…`, `mutate-and-run.sh`
`a7d3f2dd…`) and the tool prints only the first in sorted key order — see
`T49ExecR14Cmd/pin-movements.txt`. Also `git rev-parse 75ed934d` → `fatal: ambiguous argument`,
so the backticked `75ed934d…` reads like a commit id but is a sha256 (the runner's). The registry
rows disagree about the cause: `SKILL.md:1601` says of the round-17 manifest "bash-witness moved",
while `SKILL.md:1681` says of the round-14 command "since round 16 … because the runner input
moved" — yet that same round-14 command prints the bash-witness line
(`T49ExecR14Cmd/live-before-at-base.json`), and the round-17 manifest prints it too
(`T49ExecR14Cmd/live-round17-manifest-at-base.json`, exit 2, same message). Fix shape: name the
input the error actually names, or drop the cause clause, and label the digest `sha256 75ed934d…`.

**M2 — `SKILL.md:1589` typography:** `initial18-of34` is missing its space; the numbers are correct
(`SELFTEST: FAIL (18/34 failed: …)`, `.ufo/evidence/round-14/verification.json`).

## Bare names — real repo paths

| bare name in the section | real path | disambiguation |
|---|---|---|
| `dispositions.json` (`:1585`) | `.ufo/evidence/round-14/dispositions.json` | name shared with `.ufo/evidence/round-17/` and `-18/`; the round-14 file is sha256 `77faac58…`, equal to the pin in `verification-final.json`; the round-18 file is the live entry the same sentence names |
| `verification.json` (`:1588`) | `.ufo/evidence/round-14/verification.json` | `grep -rl "18/34" --include='*.json' .ufo` → only this path |
| `capture-context.py` (`:1593`) | `.ufo/evidence/round-14/capture-context.py` | single file of that name; sha256 `7313e9a2…`; not the maintained `tools/context-capture.py` |

## Risks and limits

- Rows 1/4 cannot distinguish "which pin moved" beyond the first sorted mismatch; that is the tool's
  report order, not the section's error.
- Row 5 shows the step-3 live pointer works at base; it does not re-verify the round-17 re-pin
  section's own claims. The extra probe of `.ufo/evidence/round-17/dispositions.json` (exit 2, same
  bash-witness line) only checks the attribution `SKILL.md:1601` gives that manifest.
- Step 5's re-run verdict is a code-read `[INFERENCE]`; the script was not run (bounds and
  `SKILL.md:1592-1596`).
- One clone plus one extraction, both deleted; `diff -r` between the run tree and a fresh extraction
  was empty and the clone stayed clean (`T49ExecR14Cmd/tree-unchanged.txt`), so nothing was written
  into anything this seat read.

## Summary

- Recipe exits reproduce: live 2 / archive-before 1 / archive-after 0; the other live leg is 2; round-18 manifest 0.
- The historical replay equals `verification-final.json`'s frozen stdout after normalising only `root`.
- Step 3 keeps raw receipt/check plus both passing replacements; step 4 shows 34/34 PASS and retained 18/34 FAIL.
- `capture-context.py` = `.ufo/evidence/round-14/capture-context.py`; writes only the pinned `context-receipt.json`, on failure paths too; not run.
- M1: `SKILL.md:1582` blames the runner's round-16 move, but the printed mismatch names `tools/bash-witness-study.py` (round 18/21); three pins differ at base.
- M2: `SKILL.md:1589` prints `initial18-of34` (missing space); the numbers are correct.
- Lane untouched, clone clean, archive tree identical to a fresh extract, scratch deleted, no tool installs.
