# AUD-T9 — verdict table: audit of the round-9 cadence tick (ledger ER-4 + addendum)

Audit run 2026-10-14 19:57–20:23Z by lane AUD-T9 (round-9 32-lane wave; lane
scratch `/tmp/w9-aud-t9-{work,evidence}/`). **Read-only: no fleet file was
written or edited by this audit.** The tameshi tree, the instrument
(`tools/mutate-and-run.sh`) and all four sibling repos were read only; the
instrument's own `--selftest`/`--regression` runs write only into `/tmp`
workdirs. No substrate-mutating command was run against a fleet repo; no secret
file read; no external site contacted. The assignment was "do NOT edit" — my
only fleet write is this report (a new file), per the r7/r8 audit precedent
(`reports/r7-aud-t7.md`, `reports/r8-aud-t8.md`).

## 0. What was audited

Round 9's tick receipt as landed by T9-1: **ER-4** ("the cadence fires its
first scheduled tick", ledger `:318-353`) and its **addendum** (post-tick
continuation, `:356-363`), plus the claimed reproduction (`--regression`) and
the append-only property of the ledger.

Bound revisions (this lane's reads; the frozen pair the verdicts bind to):

| artifact | pre-round (`c611d5d`) | round-9 frozen (20:19–20:22Z) |
|---|---|---|
| `corpus/knowledge/fleet-kill-rate-ledger.md` | 315 `wc -l` / 28 503 B / `71bc15e365a3574f…` | 363 / 36 169 B / `2f25c51e3e0a7851…` |
| `SKILL.md` | 1 152 L / 77 612 B / `6753b1b224f4bd18…` | 1 269 L / 85 320 B / `ee09c3bddb6cc705…` |
| `tools/mutate-and-run.sh` | `cf41efaa8be5f52d…`, 1 341 L / 61 632 B, mtime 15:29:01 −03:00 | identical — **held** |

Observed in-flight revisions of the append (my poll, 60 s cadence; corroborated
by VER-T9's 15 s poll): `e94633cc…` (351 L / 34 591 B, 20:01:18Z) → `dce68463…`
(353 L / 34 593 B, ~20:01:55Z) → `5ccf95c2…` (353 L / 34 593 B, stable
20:02:10–20:02:55Z; byte-equal to T9-1's `/tmp/w9-tameshi-t91/ledger-pre-addendum.md`)
→ `2f25c51e…` (363 L / 36 169 B, stable from 20:04:18Z).

## 1. My re-runs (the instrument, re-executed by this lane)

I ran the instrument myself, from the repo copy, workdirs in my scratch — no
producer log was trusted for these cells:

- `--selftest` (20:02–20:03Z) → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 (log `selftest-mine.log`) — reproduces ER-4's selftest receipt.
- `--regression` #1, `REGRESSION_DATE 2026-10-14T19:59:20Z`, 46.6 s, rc 0 (log `regression-baseline.log`).
- `--regression` #2 (close), `REGRESSION_DATE 2026-10-14T20:14:13Z`, 45.6 s, rc 0 (log `regression-close.log`).

Both runs, identical: every leg git-materialized at its recorded revision, per
leg `CONTROL: GREEN` on the pinned bytes, `match=10/10 … flips=0`,
`MUTATE_RESTORE: OK` (before = after = the pin), closing
`REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`:

| leg | materialized rev | pin sha256 | sweep | table | restore |
|---|---|---|---|---|---|
| js-kimi-census | `175de6ba…` | `83016d45…` | 8/10 (80 %) | match=10/10 flips=0 | OK before=after=pin |
| bash-surface-census | `fecee874…` | `275d8294…` | 8/10 (80 %) | match=10/10 flips=0 | OK before=after=pin |
| bash-tsukuroi-census | `165307fe…` | `084951be…` | 6/10 (60 %) | match=10/10 flips=0 | OK before=after=pin |
| bash-mado-verify | `eead56b2…` | `d7edaab4…` | 4/10 (40 %) | match=10/10 flips=0 | OK before=after=pin |

This reproduces ER-4's regression table cell-for-cell (its `REGRESSION_DATE
19:58:18Z`, same four legs, same numbers) and the tool's held revision: the
instrument did not move in round 9 (my `sha256sum` ×3 across the window, all
`cf41efaa8be5f52d…`).

## 2. The drift events recorded — checked against the repos' states (O)

ER-4's "*Drift events recorded*" section names two chains. I re-derived each
cell from the repos' own git object stores (read-only), then read the live
files myself at 20:00:07Z:

| case | recorded pin @ rev | chain (content sha256 @ commit, commit date) | my live read, 20:00:07Z |
|---|---|---|---|
| tsukuroi-census | `084951be…` @ `165307fe` | `084951be`(`165307fe`) → `aae45531`(`da95290`, r5, 17:33:30Z) → `bba6cdf6`(`aa136d6`, r7, 19:06:31Z) | `bba6cdf6f5b7a737…`, = HEAD blob `72b038d`, clean |
| mado-verify | `d7edaab4…` @ `eead56b2` | `d7edaab4`(`eead56b2`) → `c4c1afb7`(`c8f6667`, r6, 18:17:26Z) → `90d50cdd`(`0c20a76`, r7, 19:06:31Z) → `7da4ec50`(`12c8f08`, r8, 19:55:09Z) | `7da4ec5013583c91…`, = HEAD blob `12c8f08a`, clean |

Every chain cell matches: `git show <rev>:<path> | sha256sum` reproduces the
recorded content shas (`084951be50bcbfee…`, `d7edaab4bf108625…` and the links);
`git merge-base --is-ancestor 165307fe HEAD` and `… eead56b2 HEAD` both rc 0;
both round-8 commits are stamped `2026-10-14T15:55:09 −03:00` = 19:55:09Z
(ER-4's claim); mado's round-8 commit carries the gate edit
(`git show --stat 12c8f08` → `tools/mado-verify.sh +1150/−10`), tsukuroi's does
not (its gate path was last moved by round 7 `aa136d6`, +462/−12). The tick's
six-cell table itself (4 `current` · 2 `stale` · 0 `drift`, tool held) is what I
read independently at 20:00:07Z across all six cases — same cells, same
ancestry results (rc 0 ×6; `merge-base` per case).

The addendum's continuation cells are uncommitted worktree transients; I
captured the same files concurrently:

| gate | addendum cell (TZ-stamped) | my captures (sha, size) |
|---|---|---|
| tsukuroi | `5d16378d…` 1 535 L / 79 432 B, mtime 20:02:42Z | `84e0a2b2…` 1 535 L / 79 432 B (~20:02:5x); `c4f6db71…` (20:03:05); `b54f5732b0dff297…` (20:03:23 and 20:03:34) |
| mado | `5b6ace8e…` 3 076 L / 141 461 B, mtime 20:02:38Z | `62f81516…` 3 076 L / 141 461 B (~20:02:5x); `cbc0f5f7…` (20:03:05); `31364115b021c24c…` (20:03:34) |

The sizes agree cell-for-cell at the labeled moments; the shas move because the
owners' own round-9 lanes were writing those files in those seconds
(` M tools/…` on both trees throughout). One same-second cross-check: the SKILL
append, independently, cites "20:03:34Z … tsukuroi's worktree `b54f5732…` …
mado's `31364115…`" — byte-equal to my capture at 20:03:34Z. At my close read
(20:21:02Z) both were still dirty (`c396662e…` / `93e43f8f…`, HEADs unchanged).
Uncommitted transient bytes cannot be re-derived after the fact (U1).

## 3. The ledger append is append-only — the mechanical proof

1. **Byte-prefix identity (decisive).** `head -c 28503
   corpus/knowledge/fleet-kill-rate-ledger.md | cmp <pre-round copy>` →
   identical at every check (last at 20:22:16Z). The pre-round bytes are
   preserved in place, byte for byte. Same check at the ER-4 boundary:
   `head -c 34593 … | cmp <T9-1's ledger-pre-addendum.md>` → identical (the
   ER-4 state was not re-cut by the addendum).
2. **Diff is append-only.** My own `diff <pre-round> <final>` → a single append
   hunk `315a316,363` (+48 lines, 0 deletions, 0 modification hunks) —
   byte-identical hunk header to VER-T9's independent run (`r9-ver-t9.md` §0:
   "48 added lines, 0 deleted, 0 changed"). (GNU diff's line model folds the
   pre-round file's unterminated final line — the errata marker — into the
   matching unterminated final marker of the appended file; the byte-prefix
   check above is the stronger statement.)
3. **ER-4 region stability.** The 38-line ER-4 block (its header through the
   line before the addendum header) hashed `d1676898c084d0b1…` at 20:04:51Z and
   again at 20:20Z — unchanged while the addendum landed below it; the addendum
   region hashes `28515d589a64c051…` at freeze.
4. **Process note (recorded, not smoothed).** The first observed state
   (`e94633cc…`, 351 L / 34 591 B, 20:01:18Z) carried ER-4's header on the same
   line as the pre-round final marker; by the second stable state
   (`5ccf95c2…`, 353 L / 34 593 B, from 20:02:10Z) two `\n` bytes had been
   inserted inside the appended region. The pre-round bytes (0–28 502) were
   never touched at any stored state (prefix check). The refinement is a
   rendering fix inside the new block, not an edit of §1–§4.
5. Supporting (not required): `SKILL.md` is a pure append too — its first
   77 612 bytes byte-equal the round-8 revision, byte 77 613 begins `\n\n## The
   cadence's first scheduled tick…`, +7 707 B appended.

## 4. Verdict table

| # | claim audited | verdict |
|---|---|---|
| 1 | The instrument was **held** at `cf41efaa…` (1 341 L / 61 632 B) through the tick and this audit | **CONFIRMED** (my hashes ×3; mtime 15:29:01 −03:00) |
| 2 | ER-4's `--regression` receipt reproduces: 4 legs, `match=10/10 flips=0`, killed 8/8/6/4, `MUTATE_RESTORE: OK`, `PASS (cases=4 passed=4)`, rc 0 | **CONFIRMED** (my two independent runs, 19:59:20Z / 20:14:13Z) |
| 3 | ER-4's `--selftest` receipt: 67/67, PASS, rc 0 | **CONFIRMED** (my run) |
| 4 | The tick's pin-read table (6 cells: live sha, =HEAD-blob, clean, recorded-rev ancestor) | **CONFIRMED** (my independent six-case read 20:00:07Z = same cells; ancestry rc 0 ×6) |
| 5 | Drift event **row 3** (tsukuroi-census chain + live `bba6cdf6…` @ HEAD `72b038d`) | **CONFIRMED** (re-derived from tsukuroi's git store + live read) |
| 6 | Drift event **row 4** (mado-verify chain + live `7da4ec50…` @ HEAD `12c8f08`) | **CONFIRMED** (re-derived from mado's git store + live read) |
| 7 | Addendum continuation: both gates worktree-dirty again at 20:02–20:03Z, cells timestamped | **CONFIRMED as timestamped observations** (same sizes at same moments; one same-second cross-cite match; transient shas uncommitted → U1) |
| 8 | The ledger append is **append-only** (pre-round bytes untouched; ER-4 preserved; +48/−0/−0) | **CONFIRMED** (byte-prefix cmp ×2 boundaries; single append diff hunk; ER-4 region hash stable) |
| 9 | `SKILL.md` round-9 section landed as a pure append | **CONFIRMED** (byte-prefix identical; +`\n`+7 707 B) |
| 10 | Leg 2 (re-sweeps of the two `stale` cases) is claimed landed anywhere | **NOT CLAIMED — honestly open** (no ER-5; ER-4 and the addendum name them follow-on rows "open at this write"; the record draft renders leg 2 OPEN) |
| 11 | This audit wrote nothing but this report; substrates read-only | **CONFIRMED** (all commands read-only or `/tmp`-scoped) |

Not audited (named, not claimed): the falsifier pair (T9-3's doctored-pin
script, `/tmp/w9-tameshi-t93/falsifier/`) — read as context only; the
`service-limits.md` refusal rows and their anchors (T9-2's artifact; the
limits leg is not the tick); the leg-2 re-sweep itself (not run by any lane
observed — outside this audit's object, and nothing claims it).

## 5. Spot-checks (three, re-runnable)

- **SC1 — append-only.** `head -c 28503 tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md | sha256sum` → `71bc15e365a3574f…`; `cmp` vs `git show c611d5d:corpus/knowledge/fleet-kill-rate-ledger.md` → identical.
- **SC2 — pins.** `git -C tsukuroi-shokunin show 165307fe:tools/tsukuroi-census.sh | sha256sum` → `084951be50bcbfee…`; `git -C mado-shokunin show eead56b2:tools/mado-verify.sh | sha256sum` → `d7edaab4bf108625…`; both recorded revs ancestor of HEAD (rc 0); live reads at 20:00:07Z = `bba6cdf6f5b7a737…` / `7da4ec5013583c91…` (= HEAD blobs then; both moved since — timestamped).
- **SC3 — instrument.** `bash tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir /tmp/w9-aud-t9-evidence/regression-close` → `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0 (full log retained).

## 6. Unknowns

- **U1 — uncommitted transients.** `5d16378d…`, `5b6ace8e…`, `84e0a2b2…`, `62f81516…`, `c4f6db71…`, `cbc0f5f7…`, `b54f5732…`, `31364115…`, `c396662e…`, `93e43f8f…` lived only in moving worktrees; they cannot be re-derived, only attested by size/mtime/numstat at labeled times.
- **U2 — freeze vs commit.** The round-9 LOG/SCORECARD rows and the round-9 commit had not landed at this audit's freeze (LOG 307 L, SCORECARD 21 L, HEAD `c611d5d`). Verdicts bind to the frozen revisions in §0.
- **U3 — leg 2 OPEN.** The re-sweeps (case 3/4 at their live revisions) were not run by any lane observed in this window; recorded as open by the round itself, never as landed.
- **U4 — single host** (hostname `plazir27`), 2026-10-14; no cross-host reading for any cell.
- **U5 — timestamped cleanliness.** The tick's `clean`/`stale` cells were true at 19:58–20:00Z; both gates were dirty again by 20:02Z (recorded). A later reader must re-read, never quote.
- **U6 — regression coverage.** My re-runs cover the 4 embedded legs; cases 5/6 carry no `REGRESSION` line at `cf41efaa…` (named debt, not re-cut).
- **U7 — scratch volatility.** All evidence lives under `/tmp/w9-aud-t9-{work,evidence}/`.

## 7. Errata (append-only)

(none yet — new entries go below this line, never edits above)