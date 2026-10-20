# S15 — R17-INCIDENT recovery routing

Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Targets read: `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh` (711 lines),
`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (68 lines, read-only).
No installs; no git/jj writes; no file edits outside this report.

Grounding: live `jj-lane.sh` sha256
`3369dc27b4909a9d1c2def774b128fb4a8cb71953ac9b12de4c8519b9024e421` equals
`git -C /home/vgpnk/Projects/shokunin show HEAD:scripts/hyaku/jj-lane.sh`
(fleet HEAD `ae12f33`); lane tip for this round is
`183f87b899e6cae46be98d251cbc87fb5118f6ca`. Line numbers below are that committed
helper, not a dirty tree.

## Question 1 — does a helper-owned HEAD/index recovery procedure exist?

**No.** Observed:

- The helper exposes exactly four subcommands: `init`, `commit`, `push`, `state`
  (usage `jj-lane.sh:52-59`; dispatch `jj-lane.sh:705-709`). There is no
  `recover`/`restore`/`repair`/`doctor` subcommand.
- The only code named “recovery” is push-lease recovery:
  `recover_remote_move` (`:280-342`), reachable only from `do_push` on a
  lease-classified rejection (`:346-364`, call at `:354-357`), plus
  `reanchor_wc` (`:265-275`), which re-anchors an **empty** jj working copy and
  returns untouched when `@` has content or already sits on the tip. Neither
  restores a detached git HEAD or a rewritten git index.
- `state` is read-only pure git (`:155-180`). It reports
  `head=attached|detached` (`:175`) with the branch/local/remote hashes, but it
  never prints HEAD’s commit and never compares HEAD to `refs/heads/<branch>`.
  Since colocated lanes are normally detached after the first helper commit
  (`scripts/hyaku/lane-addendum.md:170-175`: “git HEAD is detached after the
  first helper commit”), `head=detached` carries no incident signal — the
  round-17 spot-check had to read `reflog` and `cat-file` by hand
  (`corpus/lessons/round-17-verifier-spotcheck.md:57-60`).
- The helper’s protections are preventive, not restorative: `cmd_commit` refuses
  a non-tip working-copy base with content rather than re-homing it
  (`:580-594`), and `push_preflight` refuses foreign author/committer identities
  already in the push range (`:218-228`). They stop propagation; they do not put
  HEAD/index back.
- `scripts/hyaku/jj-lane-selftest.sh` covers recovery only for push leases —
  `g fetch-rebase-recovery`, `h immutable-alias-recovery`, `z9-protocol-committer-recovery`
  (`:194-224`, `:457`). No selftest case restores a stray HEAD/index.
- Fleet tooling has no such helper either: over `/home/vgpnk/Projects/shokunin/scripts/`
  and `templates/`, `read-tree`/`--no-deref` appear nowhere; the only
  `update-ref` uses are fixture manipulations inside `jj-lane-selftest.sh:342,353,698`.
  `PROTOCOL-APPENDIX.md` has no recovery row.

The incident repair was ad hoc L1 plumbing, by the L1’s own disclosure:
`git read-tree 98bea7d` + `git update-ref --no-deref HEAD 98bea7d`
(`.ufo/reports/round-17/tameshi.md:109`; reflog-restore at 12:36:43 confirmed in
`corpus/lessons/round-17-verifier-spotcheck.md:57`). The incident itself: at
2026-10-20 12:29:33 a seat ran `GIT_DIR=<live lane>/.git bash tools/mutate-and-run.sh
--selftest` from a `/tmp` clone; fixture commits moved HEAD
`98bea7d → f8832ef → 0559c60 → e16adb7` and rewrote `.git/index`
(`.ufo/waves/round-17/w1/N01TraceGitSafety.md:18`; `corpus/lessons/round-17.md:57`).
`refs/heads/master` never moved (`round-17-verifier-spotcheck.md:58`), and the
index/worktree were restored (`:60`).

The lane contract makes ad hoc repair non-operable for seats: `lane-addendum.md:170-175`
forbids `git reset`/`checkout`/`switch` and every mutating jj command, and names
the helper the only writer. So today the only recovery path is L1/operator
(non-lane) plumbing, exactly what round 17 routed: “A safe helper-owned recovery
procedure is fleet/operator tooling scope; tameshi must route that need, never
normalize ad hoc Git plumbing” (`round-17-verifier-spotcheck.md:452-454`), with
“Fleet/operator owns the recovery helper and its moving line anchors”
(`:456-460`).

Recovery invariants a helper would have to assert (observed set from the
incident’s independent check, `round-17-verifier-spotcheck.md:57-63`):
restore HEAD to the branch tip with a named reflog message; restore the index to
that tip (`diff --cached --quiet HEAD`); leave `refs/heads/<branch>` and
`refs/remotes/origin/<branch>` untouched; keep fixture objects unreachable
(`merge-base --is-ancestor` false, no branch contains them); leave on-disk
worktree bytes alone. `jj undo`/`op restore` is **not** a candidate for a plain-git
stray write — jj only imports refs at snapshot/transaction time [INFERENCE from jj
semantics; not executed], and the helper forbids mutating jj anyway.

## Question 2 — has any lane already asked?

**No.** Observed:

- The fleet queue (`.ufo/l0-questions.md`, 68 lines) contains no line about
  HEAD/index recovery, a recovery helper, `read-tree`/`update-ref`, or the
  round-17 incident. `grep -nEi "recover|restore|stray|HEAD|index|GIT_DIR|incident|reflog"`
  hits only unrelated lines (kasegi’s stalled rebase, host package recovery,
  kaidoku routing); `grep -nEi "jj-lane|helper|plumbing"` hits only souji
  round-17 `jj util gc` (line 66) — adjacent helper maintenance, not recovery.
- `tameshi` has one queue line only, round-1 (`:27`); no `tameshi | round-17` or
  `round-18` line (`grep -c "^tameshi | round-18"` = 0).
- Lane-local queues `lore-shokunin/l0-questions.md` and
  `tsukuroi-shokunin/.ufo/l0-questions.md` contain no such line.
- Queue history: `git log -S"recovery" -- .ufo/l0-questions.md` returns only
  kaidoku routing-incident commits (`a6f51df`, `e5b87e1`); `-S"restore HEAD"`
  returns nothing; `-S"jj-lane"` returns only souji’s round-17 questions
  (`23efcab`). The need is routed in the tameshi lesson (§7.8), but no lane has
  filed it as an L0 question.

## Draft L0 line (not appended)

One line, in the queue’s `<lane> | round-<N> | <question>` form:

```
tameshi | round-18 | Fleet/operator recovery-helper decision (round-17 live-Git incident): should scripts/hyaku/jj-lane.sh gain a helper-owned recovery subcommand (e.g. `recover <lane-dir>`) that restores a lane's detached git HEAD to the resolved branch tip, restores the index with `read-tree <tip>`, verifies refs/remotes and that fixture objects stay unreachable, and writes a named reflog message, instead of leaving repair to ad hoc L1/operator plumbing? Observed: the helper's only subcommands are init/commit/push/state (jj-lane.sh:52-59,705-709); its only recovery code is push-lease rebase (recover_remote_move :280-342) and empty-@ reanchor (:265-275); `state` (:155-180) reports head=attached|detached but never HEAD-vs-branch-tip, so the normal detached lane hides a stray HEAD; lane seats are contractually barred from git reset/checkout/switch/update-ref writes (scripts/hyaku/lane-addendum.md:170-175). On 2026-10-20 12:29:33 a GIT_DIR leak moved live HEAD through f8832ef/0559c60/e16adb7 and rewrote the index; the L1 restored it at 12:36:43 with `git read-tree 98bea7d` + `git update-ref --no-deref HEAD 98bea7d` (.ufo/reports/round-17/tameshi.md:109; corpus/lessons/round-17-verifier-spotcheck.md:57-60), and round-17 §7.8 routes a safe helper-owned recovery procedure to fleet/operator scope (round-17-verifier-spotcheck.md:452-454). No L0 line has asked this yet. Please decide: add the helper subcommand (with a red-before selftest case), name another owned procedure, or rule ad hoc L1 plumbing the accepted path.
```

## Remaining unknowns

- Whether the operator wants recovery inside `jj-lane.sh` or a separate fleet
  helper (e.g. `scripts/hyaku/lane-recover.sh`); both are fleet/operator paths,
  and deciding is the L0 question, not this seat’s.
- The exact helper signature/exit map is unconstrained by any existing contract;
  `jj-lane.sh`’s documented exit map is 0/1/3/64 (`:57`), and a recovery
  subcommand would need its own entry.
- The round-17 report does not record whether `git update-ref --no-deref HEAD`
  was followed by a reflog-independent index check inside the same command; the
  spot-check re-verified it later (`:60`).

## Verdict

built — no helper-owned HEAD/index recovery procedure exists (jj-lane.sh exposes
only init/commit/push/state; recovery code is push-lease only), no lane has yet
filed the need on the L0 queue, and a one-line `tameshi | round-18 | ...` routing
question is drafted above and deliberately not appended.
