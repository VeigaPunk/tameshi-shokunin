# T53W1Read28 — cold read of `### Triggers T1–T3 and the re-pin rule`

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, content commit C\* `a41195dfc13a73958e4c5228ec196b28d03ded03`. Section read from git objects only (`git show C*:SKILL.md`); the working tree was never read for section text.

**Result: 0 findings.** The section holds at C\*. `findings` in `T53W1Read28.json` is `[]`.

## Section identity and split

Split rule reproduced as specified: lines of SKILL.md at C\*, heading = line matching `^#{1,3}(\s|$)` outside ``` fences, section = heading line .. line before next heading, trailing whitespace-only lines stripped, joined with `\n` (no trailing newline), sha256 over UTF-8 with `surrogateescape`.

- `git show C*:SKILL.md | wc -l` → `2178`.
- Splitting the blob: the heading text matches exactly one heading line, at **line 1071**. Only one heading-shaped line in the whole file carries this text.
- Next heading of level 1–3 is at **1094** (`### Six-case confidence statement (round 8, measured)`); line 1093 is blank and therefore stripped.
- Section range: **1071–1092**, 22 lines. Verified by printing 1066–1096 of the blob and confirming the line immediately above 1071 is a blank line inside the previous section and the line after 1092 is blank, followed by the next heading.
- `section_sha256` = `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801`.

## What the section states, and the check on each statement

Every quote below is copied from the section bytes at C\*.

### T1 — rule and the two live instances (lines 1073–1076)

| Statement | Check (read-only) |
|---|---|
| `- **T1 — a case reads `stale`** → re-measure at the live revision, or record the` … `  STALE cell with its reason; **never an edit of the recorded table**. Live` | Rule text; matches the ledger's own discipline (`fleet-kill-rate-ledger.md:170-173`, `:312`, `:352`). No pointer claimed, nothing to resolve. |
| `  instances at round 8 (2026-10-14): tsukuroi `084951be…` (6/10) → `bba6cdf6…`; mado` | Ledger row 3 (`:47`): tsukuroi `084951be…`, 26 cases, **6/10 (60 %)**. ER-2 row 3 (`:301`): recorded pin `084951be…`, live `bba6cdf6…`, clean, `stale`. Both pin and rate hold. |
| `  `d7edaab4…` (4/10) → `90d50cdd…` → `7da4ec50…` (both have moved again since; re-read, never carry).` | Ledger row 4 (`:48`): mado `d7edaab4…`, **4/10 (40 %)**. ER-2 row 4 (`:302`): recorded `d7edaab4…`, live `90d50cdd…`, worktree transient `dc864c6a…`, `stale + drift`. ER-3 row 4 (`:329`): live `7da4ec50…`, clean, `stale`. Chain stated verbatim at `:338` (`d7edaab4` (`eead56b2`) → `c4c1afb7` → `90d50cdd` (`0c20a76`) → `7da4ec50` (`12c8f08`)). The added terminal `7da4ec50…` is the round-8 commit: `git -C mado-shokunin show -s --format='%h %ad' 12c8f08` → `2026-10-14T16:55:09-03:00` (same day), and `git -C mado-shokunin show 12c8f08:tools/mado-verify.sh \| sha256sum` → `7da4ec5013583c91…`. |
| `(both have moved again since; re-read, never carry)` | Still true at C\*: `git -C tsukuroi-shokunin show HEAD:tools/tsukuroi-census.sh \| sha256sum` → `adb1b4ce2325c38d…` (≠ `bba6cdf6…`); `git -C mado-shokunin show HEAD:tools/mado-verify.sh \| sha256sum` → `050efc720599345a…` (≠ `7da4ec50…`). |

### T2 — rule, precedent, runner pins (lines 1077–1082)

| Statement | Check (read-only) |
|---|---|
| `  re-run the reproduction under the new revision and record both pins. Precedent` | Rule text; the same rule is stated at `fleet-kill-rate-ledger.md:310` and `SKILL.md:811-812`. |
| `  (corrected round 18): round 16's RerunSweep under runner `89722ddb…` (`RerunSweep.md:19-23`; `0673d2e5…` is the later regression/selftest runner; corrected round 27, seat Read15) reproduced case 7;` | (a) `RerunSweep.md:19-23` = `.ufo/waves/round-16/w2/RerunSweep.md:19-23`: `- Tool: `worktree/tools/mutate-and-run.sh` at c699c8c → sha256` / `  `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` (runner-sha256.txt`. `git show c699c8c:tools/mutate-and-run.sh \| sha256sum` → `89722ddb3082abd6…` — exact. (b) "later": c699c8c is `2026-10-20T10:49:37-03:00`; 05a2247 is `2026-10-20T11:18:08-03:00` and its blob is `0673d2e5374b94c6…`; `.ufo/evidence/round-16/round-gate/runner-sha256.txt:2-5` says in terms that `05a2247` moved the runner and that `runner-regression.txt`/`runner-selftest.txt` were re-run on it and carry `0673d2e5…` — both receipts confirmed at C\*. (c) "reproduced case 7": `RerunSweep.md:98-101` — `**C1's measured table holds**: re-running §1-§2 of` `corpus/knowledge/mutation-case-kumitate-round-gate.md` … `exactly — 5/10 killed, 10/10 predictions.`; the round-gate case is case/leg 7 (`c699c8c` subject `round-16: land js-round-gate case 7`; ledger `:410` leg `js-round-gate`). (d) "corrected round 18": `git show 9ee1c80 -- SKILL.md` adds exactly the `(corrected round 18)` wording, replacing the earlier false "the mado spec re-cut" precedent — the provenance claim is true. |
| `  mado under `b56c6e57…` was re-run once by SCR-T6, 4/10, scratch not retained (`service-optin-protocol.md:232`; the mado note keeps it U, `mutation-case-mado-verify.md:17-23`; seat ReRead07); the harness itself moved four times in` | `service-optin-protocol.md:232` = `\| second seat \| … \| SCR-T6 re-ran the spec under `b56c6e57…`: 4/10, all ten mutant shas identical \|`. "scratch not retained" is carried by `plans/round-6-record-draft.md:204-209`: `Scribe verification (this draft, TAMESHI-SCR-T6, re-run 2026-10-14; scratch` / `/tmp/w6-scr-t6-*): … independent mado re-sweep against the pinned` / `d7edaab4` bytes …` / `tool → 4/10, verdicts and all ten mutant shas identical to T6-1's table;` — an uncommitted /tmp scratch, consistent with "not retained". "the mado note keeps it U": `mutation-case-mado-verify.md:22-23` — `**Every number in this note is tied to `597e1419…`**; whether the new` / `revision reproduces this table is **U** (§7).` |
| `  one day (`597e1419…` → `b56c6e57…` → `4dc69ef9…` → `e3f838d4…` → `cf41efaa…`) [round 52: `4dc69ef9…` and `e3f838d4…` were working-tree writes, not commits (`plans/round-8.plan.md:69-74`, 15:27:40 and 15:28:38); the day's committed chain is `d8abee52…` (created 13:01) → `597e1419…` (13:57) → `b56c6e57…` (15:17) → `cf41efaa…` (16:06) → `75ed934d…` (18:28, r10-2 — `RerunSweep.md:93`) — four moves]` | Commit-dated blob enumeration over every commit touching the tool: `53e74a8` 2026-10-14T13:01:03 → `d8abee522efbf27c`; `b58b26f` 13:57:18 → `597e141989065e03`; `4494715` 15:17:26 → `b56c6e57f1b7ae91`; `9f1d3c3` 16:06:31 → `cf41efaa8be5f52d`; `606716f` 18:28:23 → `75ed934dc86360f5`. Exactly four committed moves that day, all five timestamps as stated. `4dc69ef9…` and `e3f838d4…` appear at **no** commit (same enumeration, full history); their times and sizes are at `plans/round-8.plan.md:69-74` (`15:27:40, 1247 L / 56518 B`, `15:28:38,` `61305 B`). `RerunSweep.md:93` = `durations, and the tool sha (75ed934d → 89722ddb, the commit-expected r16 tool —`; the `r10-2` label is the tool's own header at that blob (`git show 606716f:tools/mutate-and-run.sh`, line 2: `# mutate-and-run.sh — generic mutation runner (tameshi-shokunin, r10-2, TAMESHI-T10-2).`) and is repeated at `RerunSweep.md:22` (`(r10-2, pre-ledger-embedding)`). The outer chain keeps four arrows for four moves, and the bracket states the four committed moves — no count contradiction. |
| `  and no recorded table was re-interpreted for it.` | Historical statement of the round-8 window; `plans/round-8.plan.md:38-39` records the same fact (`the case tables measured under the earlier revision were not re-run by the` / `moving lane`), and the ledger states the rule at `:310`. |

### T3 and the re-pin rule (lines 1083–1092)

| Statement | Check (read-only) |
|---|---|
| `- **T3 — an owner lane records a re-run at a new revision** → an appended row;` / `  §1–§4 are never edited (`fleet-kill-rate-ledger.md:170-173`).` | Ledger `:170-173` verbatim ends `row, not an edit of §1–§4.` — supports the appended-row rule. |
| `  (`fleet-kill-rate-ledger.md:310`, ER-3; `:318`, ER-4). The old table stays; the moved case lands at its newest revision` | `:310` is ER-3 trigger 3: `3. **On substrate drift.** The pin read above reads stale or drift. A moved substrate needs a **re-pin**, never a re-interpretation of the old table …`. `:318` is the ER-4 block, which states `… a moved pin is never re-interpreted.` Both pointers land on bytes that carry the rule. |
| `  with both shas and the delta, appended. `moved=0 stale=0` is a complete` / `  outcome, recorded as such — drift is never manufactured by re-cutting cases.` | `:312`: `… `moved=0` is recorded, never manufactured.`; `:352`: `a tick that read `stale=0` would be as complete.` Both halves supported. |
| `  The round-8 replay receipt (tool `cf41efaa…`, four legs; 19:14:16Z, rc 0, `fleet-kill-rate-ledger.md:281`; seat ReRead07):` | `:281` carries `carries **four** materialized legs`, `(O: T8-2's run 2026-10-14T19:14:16Z`, and the PASS string. `rc 0` is not on `:281`; it is recorded at `mutation-case-kumitate-claims.md:316-317` (`at 19:14:16Z, tool `cf41efaa…` →` / `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0,`). The claim holds at C\*; only the pointer is narrower than the clause (same observation the round-52 fix record logged as M1 and left unedited, so it is not raised here as a finding). |
| `  `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0` / `  flips<=0)`, every leg `match=10/10 … flips=0` — the recorded tables hold at` / `  their own pinned blobs regardless of the live drift above.` | Ledger `:281` contains that PASS string byte-identically and `every leg `match=10/10 flips=0``; `:281` also states the tsukuroi and mado tables `now ARE re-verified by the harness's own `--regression`` at their recorded pins under `cf41efaa…`, and that the candidates' live revisions are not what the legs replay. |

## Deltas at C\* relative to the round-52 fix commit

The round-52 fix (`CAND0` `bcba892…`) verified this section as "30 hold, 1 fixed". The section text at C\* differs from CAND0 in exactly three lines (section-level diff: old 1069–1090, new 1071–1092). Each delta was checked:

1. mado T1 chain gained the terminal `→ `7da4ec50…`` — verified (ledger `:329`, `:338`; mado commit `12c8f08` dated 2026-10-14T16:55:09-03:00, blob `7da4ec50…`).
2. The round-52 bracketed annotation on the harness chain is present and its contents are verified above (working-tree writes; committed chain; four moves).
3. The re-pin pointer `(:811-812)` was replaced by `(`fleet-kill-rate-ledger.md:310`, ER-3; `:318`, ER-4)` — both new anchors verified above; the replaced anchor also holds (`SKILL.md:811-812` carries the same rule), so the change is an addition of receipt, not a loss.

## Scratch posture of the section

The section states no scratch directive of its own and cites no `/tmp` path as a place for a seat to write; its single `/tmp` reference (`scratch not retained`, backed by the uncommitted `/tmp/w6-scr-t6-*` in `plans/round-6-record-draft.md:205`) is a historical record of a round-6 seat's scratch, not a directive. No scratch-directive violation to report.

## Findings

None. Every pointer named in the section resolves at C\* to bytes that carry the claim; the counts (`four moves`, `four legs`, `6/10`, `4/10`, `10/10`) are each confirmed by a command output; the only imprecision found (`rc 0` not on ledger `:281`) is a pointer-width issue on a claim that is true elsewhere at C\*, already on record as a minor observation, and is therefore not counted as a failing statement.

## Seat hygiene

All work ran in `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read28/` (SKILL.md copy at C\*, split script, section dump); the tree was removed before this report. No git/jj mutation, no writes outside `.ufo/waves/round-53/w1/`, no tool installs (nothing was needed: `git`, `python3`, `sha256sum`, `diff` sufficed).
