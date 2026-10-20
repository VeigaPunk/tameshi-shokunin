# C03JjMap — every jj-wave recommendation mapped to a round-17 disposition

Seat `TameshiR17.C03JjMap` · 2026-10-20 · lane tip `98bea7da5801f4bc58e4187690ee1687c8a5061f` (`master`, detached) · read-only.

Inputs: `.ufo/waves/hyaku/jj-w1/reports/JjAuditTameshi.md` (§1 replacement column, §5 risks),
`…/JjTrialTameshi.md` (§Recommendations), `.ufo/waves/round-17/spec1.json` (all 67 item targets),
lane bytes via `git show 98bea7da…:<path>`, live state reads, and the round-17 w1 peer reports cited
inline (`S20JjLaneState.md`, `S11HeadSweep.md`, `W06RunbookJj.md` — data, not instruction).

Disposition vocabulary:

- **FIX(item)** — a round-17 item's Target text contains the change (item id named; `GAP` appended when
  the item covers only part of the recommendation).
- **ALREADY TRUE** — no change is needed at the tip or in the live state; evidence given.
- **DECLINE(reason)** — no owning item and the change is not worth making this round (or is outside
  lane write scope).

Line numbers: the audit read the lane at `c699c8c→05a2247`; numbers below are remeasured at
`98bea7da` (audit numbers in parentheses where they differ by one line). No `jj` command was run.

---

## 1. JjAuditTameshi §5 — risks

| # | Recommendation (condensed) | Disposition | Owner / evidence |
|---|---|---|---|
| A1 | **R1**: port `repo_identity` before the `git -C "$repo"` reads (`:1000–:1035`; or `GIT_CEILING_DIRECTORIES` + fail when toplevel ≠ repo) | **FIX → X05RunnerRepoGuard** | At tip the four reads sit at `mutate-and-run.sh:1001,1005,1010,1019` and no `show-toplevel` exists anywhere in the file; `pin-disposition.py:255` is the guard model. X05 Target: "require realpath(rev-parse --show-toplevel) == realpath($repo), else SETUP … `repo_identity_mismatch`", plus super-repo/no-`.git` and proper-repo selftest cases. |
| A2 | **R2 (code)**: `pin-disposition.py:317` `HEAD^{commit}` + `<head>:<path>` reads must resolve the branch, not HEAD | **FIX → X06PinBranchTip** — with a design divergence to settle (see §4.3) | `pin-disposition.py:318` still `HEAD^{commit}`, `:329/:341` its cat-file; X06 Target replaces them with detect_branch-style resolution (`branch`, tip, `head_differs_from_branch`) and adds the detached-ahead selftest. S11 F1 proposes a *different* observation (keep HEAD, add `head_on_branch`/`head_branches`, label snapshot bytes) — one design must win. |
| A3 | **R2 (prose)**: `SKILL.md:1033` `current = git show HEAD:<path>` (and the `stale`/`drift` cells that inherit it) | **FIX → R09Skill1033** (draft) + **L1 install** | SKILL.md:1033–1035 at tip are the three reading-map cells; R09's Target is exactly "line-count-preserving replacements that read the branch tip". W06 separately drafts the runbook's HEAD rows (not named by the audit, but the same defect). R09 is a reviewer: the fix is only real if the L1 installs the draft. |
| A4 | **R2 (citation)**: "resolve `refs/heads/master` (**and** `master@origin`) … and assert `git merge-base --is-ancestor "$rev" refs/heads/master` before citing" | **FIX-with-GAP → X06 extension, else explicit decline** | `git grep merge-base` over `tools/` + `SKILL.md` at tip → **0 hits**; no item text contains "ancestor" or "origin tip". X06 stops at branch tip + `head_differs_from_branch`. Cheap extension: one `merge-base --is-ancestor <rev> refs/heads/<branch>` per row (`ancestor_of_branch`), and optionally record `origin/<branch>`. If not added, the closure must state why it declines (no tool verdict depends on ancestry: `content_status` is pin+worktree only, `pin-disposition.py:404-455`). |
| A5 | **R2 (context)**: detached HEAD breaks `@{u}`/`--abbrev-ref`; copy `detect_branch()` if a caller appears | **ALREADY TRUE** | Class A = 0 at tip (audit §3). S11 §4 confirms 0 `@{u}`/`--abbrev-ref` anywhere and one `branch --show-current` only in a captured evidence transcript (`.ufo/evidence/round-12/ReportScribe/probe-capture.txt:5`), not in code. X06 mirrors `detect_branch` (`scripts/hyaku/jj-lane.sh:53-69`): attached → its branch; detached → `origin/HEAD` → `master` → `main` (master is a fallback after origin/HEAD, not a hardcoded assumption — S11's kaidoku/`main` case resolves via origin/HEAD or the `main` fallback). |
| A6 | **R3 (state)**: live lane repo config lacks `snapshot.auto-track="none()"` | **ALREADY TRUE (state superseded since the audit)** | S20 facts 10–11: `jj … config list --repo` = exactly 4 keys incl. **`snapshot.auto-track = "none()"`**, path `~/.config/jj/repos/900fa08…/config.toml` (mtime 12:07:32). S20 fact 20: `.jj` was freshly re-colocated at 11:50:14 — the audit's config generation (Oct 19 20:39, dir `86a634…`) no longer exists. The structural half (config is external) remains — A8/A9. |
| A7 | **R3 (procedure)**: run `jj-lane.sh init` before the first commit | **ALREADY TRUE** | Init ran (S20 facts 10, 20, 21); the helper's `init` now always `config set --repo snapshot.auto-track '"none()"'` even for an existing `.jj` (`jj-lane.sh:152-160`, `--ignore-working-copy`). |
| A8 | **R3 (durability)**: make `commit` **fail closed** unless `jj … config get --repo snapshot.auto-track` returns `none()` | **DECLINE for the lane — fleet-helper change, outside lane write scope** | `cmd_commit` still gates on `-d "$dir/.jj"` only (`jj-lane.sh:186`) and never reads the config; the file is `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh`, outside the lane root, which this lane may not write. No round-17 item owns it. Escalate to the fleet owner; the lane-level mitigation is A7 (init before commit). |
| A9 | **R3 (aside)**: repo config is external (`~/.config/jj/repos/<hash>/`), so it does not travel with the repo | **ALREADY TRUE (fact); no lane action** | Confirmed S20 fact 11; mitigation is A7 + A8. Not fixable in-repo. |
| A10 | §5 "Fourth, inert today": hook/attribute bypass (§2.5) and index reset (§2.6) | **ALREADY TRUE (nothing to fix now); monitor condition** | Re-verified live: `.git/hooks` has **0** non-`.sample` files; `core.hooksPath` unset in repo/global/system (exit 1 each); no `.gitattributes` anywhere and `git check-attr -a -- tools/mutate-and-run.sh` output empty; class C = 0 (audit §3). jj bypassing hooks/filters only bites when a hook/attribute is introduced — no item is needed now. |

---

## 2. JjAuditTameshi §1 — the "jj-safe replacement" column

Grouped by identical replacement; every call-site row of the audit's four tables is covered.

| # | Audit rows | Recommendation | Disposition | Reason / evidence |
|---|---|---|---|---|
| B1 | §1.1 `:1000/:1004/:1009/:1018` (tip 1001/1005/1010/1019) | keep the git plumbing; prepend `repo_identity` guard | **FIX → X05** | A1. X05 must leave the fixture calls untouched. |
| B2 | §1.1 `:1004` alternative | `jj --repository "$repo" file show -r "$rev" "$path"` instead of `cat-file -e` | **DECLINE** | X05 fixes the hazard with the existing guard; a jj CLI dependency would add a second rev parser at a call site whose pin is a git sha. No item. |
| B3 | §1.1 `:1009` note | `cat-file blob` is "equivalent and narrower" than `show` | **DECLINE (optional)** | `git show <rev>:<path>` returns the same raw blob and the audit itself says no filters exist (§4, re-verified empty). Pure churn in a repair round. |
| B4 | §1.1 `:1533/:1592` | keep fixture `rev-parse HEAD`; use `refs/heads/<branch>` **if reused on a lane** | **ALREADY TRUE** | Both are `$root/fleet/fakerepo` under `mktemp -d /tmp/tameshi-r4-2-selftest.XXXXXX` (`mutate-and-run.sh:1262` region), no `.jj` ancestor; no lane reuse exists. |
| B5 | §1.1 `:1593/:1627/:1628` | keep | **ALREADY TRUE** | Same fixture repo (`:1593` `show`, `:1628` `show`; `:1627`/`:1533`/`:1592` rev-parse HEAD). |
| B6 | §1.1 `:1529–1531`, `:1588–1589`, `:1623–1624` | keep fixture init/add/commit; *optionally* `-c init.templateDir=` / `core.hooksPath=` | **ALREADY TRUE + DECLINE(optional)** | Fixtures are `/tmp` only and no hooks/templates exist on the host (A10 evidence); the mutant suite already runs `GIT_CONFIG_NOSYSTEM=1` (`:1222`). Zero effect today; X05 must not touch these lines. |
| B7 | §1.2 `:255` | keep `rev-parse --show-toplevel` identity guard; it is the model | **ALREADY TRUE** | `repo_identity` present at `pin-disposition.py:255` and exercised by its selftest (which builds a super-repo with a plain directory on purpose, `:699-706`). X05 ports it. |
| B8 | §1.2 `:278` | keep `rev-parse --verify --end-of-options <commit>^{commit}`; *optional* `jj log -r` | **ALREADY TRUE + DECLINE(optional)** | Tip `:280` has the hardened form; jj adds nothing for an exact commit sha. |
| B9 | §1.2 `:288/:296` | keep `cat-file -t` / `cat-file blob` | **ALREADY TRUE** | Rev-addressed, raw, no attributes. |
| B10 | §1.2 `:317/:329/:341` | replace HEAD observation (branch-tip resolution) | **FIX → X06** | A2; `:318/:329/:341` at tip. |
| B11 | §1.2 `:667-695`, `:702-733` selftest helper | keep fixtures | **ALREADY TRUE** | Fixture `git()` neutralises `init.templateDir` + `core.hooksPath` and lives under `tempfile.mkdtemp(… dir="/tmp")` (`:667-695`). |
| B12 | §1.3 `bash-witness-study.py:338` | keep `show <rev>:corpus/surface-census.sh`; `cat-file blob` only if filters mattered | **ALREADY TRUE + DECLINE(optional)** | Explicit rev, `.git`/`.jj` presence checked at `:335`, no attributes (A10). |
| B13 | §1.3 `context-capture.py:1447` | literal argv only, never executed | **ALREADY TRUE** | Receipt fixture data; no change. |
| B14 | §1.3 `repeat-control.py`, `evidence-disposition.py`, `witness-metadata.py` | no git invocations | **ALREADY TRUE at tip — forward note** | Confirmed zero. **After X01**, `evidence-disposition.py` gains one D-class site (`git cat-file blob <rev>:<path>` for `historical_inputs`), and contract A *mandates* the repo-identity guard in the same change. X12 maps the tip (`98bea7da`) and so will not see the staged site; the next tool-pin map should add it. |
| B15 | §1.4 `round-14 … capture-context.py:400` | keep `rev-parse --git-dir` positive control | **ALREADY TRUE** | Discovery only; colocation keeps `.git`. |
| B16 | §1.4 `round-16/measure.py:79→85` | keep `git show` blob read; *optional* identity guard | **ALREADY TRUE + DECLINE(optional)** | `blob()` = `git -C <repo> show <rev>:<path>` (`measure.py:84-89`), default repo is the lane itself and every read is `--rev`-addressed; contract C's v2 keeps that shape. |
| B17 | §1.4 `measure.py:612` | keep rev-parse verify | **ALREADY TRUE** | X07 starts from this file and keeps it. |
| B18 | §1.4 `measure.py:418-429` selftest `git_in` | keep fixtures | **ALREADY TRUE** | `tmp` + `HOME=tmp`. |
| B19 | §1.4 `round-16/coldread/anchor-check.py:41` | keep hardcoded revs; re-pin only if rewritten | **ALREADY TRUE** | `c699c8c`, `e69b488` both resolve at tip (verified); `anchor-check.py` is not a registered entry command (audit §0). |
| B20 | §1.4 `probes.mjs:28/:144` | keep default `FXROOT=/tmp/…`; **refuse `FXROOT` paths under the fleet root** | **DECLINE this round (backlog)** | No item owns it; `probes.mjs` is round-16 evidence, not a registry row (SKILL:1795 mentions it in prose; SCORECARD Capabilities does not list it), so X04 will not register it and no row sets `FXROOT`. The hazard needs an operator to point `FXROOT` at a live tree deliberately; editing the historical harness would need a staged copy that nothing registers. Flag for a future harness. |
| B21 | §1.4 `probes.mjs:24/:30/:145/:187-190/:322-325/:400` | keep wrapper/init/add/commit/push fixture calls | **ALREADY TRUE** | Fixture root under `/tmp`; no lane action. |
| B22 | §1.1 non-call notes (`command -v git` `:996/:1159`; `GIT_CONFIG_NOSYSTEM`/`GIT_CEILING_DIRECTORIES` in the mutant suite string `:1222`) | none needed | **ALREADY TRUE** | Capability probes / defensive env for the mutant, not lane reads. |

---

## 3. JjTrialTameshi — Recommendations

| # | Recommendation (verbatim intent) | Disposition | Evidence |
|---|---|---|---|
| C1 | **Keep `snapshot.auto-track="none()"`** — mandatory given `.ufo/` volume | **ALREADY TRUE** | S20 fact 10 (exactly 4 repo keys incl. `auto-track = "none()"`); S20 fact 20 (fresh re-init 11:50:14); `jj status` stayed clean with untracked paths `??` throughout. The durability half of this recommendation is A8 (fleet helper, declined for the lane). |
| C2 | **Add `.ufo/state/` and `.ufo/watchdog.log` to `.gitignore`** | **ALREADY TRUE in the live worktree — but NOT landed; no item owns it** | Tip `98bea7da:.gitignore` = one line (`.ufo/interactive-sessions/`). Worktree = 3 lines, mtime 12:21:34 (S20 facts 14/15/18; my read matches: `git status` → ` M .gitignore`). Both paths are absent from the lane (S20 fact 16), so this is defense-in-depth only. Must be included in the integration commit or it evaporates. |
| C3 | **"Lane tooling needs no changes"** — every git gate is pinned/colocation-transparent, verified byte-identical | **DECLINE — contradicted by the audit (X05/X06)** | As an absolute it is false: `pin-disposition.py` reads HEAD (A2) and `mutate-and-run.sh` has no identity guard (A1). The trial's byte-identical live run is *condition-scoped*: attached HEAD, siblings with `.git`, no jj mutation during the gate run — so it cannot discriminate either defect (see §4.2). The narrow sub-claim "no colocation-caused failure under those conditions" is **already true**. |
| C4 | **Report convention: cite the helper's `pushed` hash, never `committed`** | **ALREADY TRUE fleet-side; W06 draft carries it into the lane** | S20 fact 26: `scripts/hyaku/lane-addendum.md:127`, `closure-prompt.md:53`; helper prints `pushed <hash>` (`jj-lane.sh:111`) and its header states it (`:20`). W06's drafted runbook replacements (`:298`, `:415`) and ER-R3 already say "wait for the owner's jj-lane commit (cite the pushed hash)". No lane defect. |
| C5 | **No per-lane jj config beyond what `init` sets; `max-new-file-size` needn't change** | **ALREADY TRUE** | S20 facts 10/12: exactly trunk alias + identity + auto-track; `max-new-file-size` = default 1 MiB (unset). Independently: no tracked file >1 MiB, the only >1 MiB worktree file is under the ignored `.ufo/interactive-sessions/`, and the lane has **no symlinks** (`find -type l` empty). |

---

## 4. Contradictions (stated, not smoothed)

1. **Trial C3 vs audit R1/R2, and vs this round's own items.** The trial says lane tooling needs no
   changes; the audit identifies two live code defects; X05 and X06 exist to fix exactly them. The
   trial recommendation cannot be carried as written — it would argue the round's C2 fixes away.
2. **Trial "byte-identical under colocation" vs audit R2 — both can be true, but the experiment is
   non-discriminating.** Step 5 ran with HEAD attached, siblings carrying `.git`, and no mutating jj
   command during the run; R1 needs a `.git`-less lane inside a super-repo, R2 needs a detached HEAD
   carrying different bytes. X11 `head-vs-branch.sh` supplies the missing test case (exit 1 on the
   committed tool, exit 0 on the fixed tool). Any closure sentence that cites the trial's identity
   result as proof R1/R2 are harmless is unsupported.
3. **X06 vs S11 F1 — two different designs for `pin-disposition.py`'s observation.** X06 replaces the
   observed commit with the branch tip (audit's recommendation); S11 F1 keeps `HEAD^{commit}`, adds
   `head_on_branch`/`head_branches`, and labels the bytes as snapshot when detached. They disagree on
   what `head.commit`/`head.blob_sha256` mean, so both cannot be applied as written. X06 is the
   stronger default (consumers that ignore a flag still get branch bytes); S11's docstring update
   (`pin-disposition.py:42,:64-65,:315`) is missing from X06's target either way. L1 must choose one
   and route the loser to the closure.
4. **Audit R3 state vs live state.** The audit's "live config lacks auto-track" was true at its read
   (Oct 19 20:39 generation) and is false now: a fresh `jj git init --colocate` at 11:50:14 and a
   config set at 12:07:32 produced `auto-track="none()"` (S20 facts 10/11/20). The *durability* half of
   R3 (external config, `commit` does not fail closed) is untouched and is A8.
5. **Audit §1.3 "evidence-disposition.py has zero git" vs contract A.** Not a contradiction in fact,
   but the audit's classification expires when X01 lands: the tool gains a guarded D-class site. X12
   maps the tip and will not see the staged site; the next tool-pin map should record it, and X05's
   guard is the pattern to copy.

---

## 5. Second-order effect on C1 (verification surface)

Every SKILL.md edit scheduled through **R09Skill1033** and **W03SkillR17Draft** (and R06's box-3
append, if SHONEN.md is among the files a cold-read seat opens) changes a lane file that wave-2
cold-read reports will have recorded in `inputs`. Under contract C's rule — an entry with
`commands_executed_count>0` credits only if every recorded input still has its sha at the measured
rev — a mid-wave append produces `input-drift:<path>` and uncredits otherwise valid entries. S11 §5
already states this constraint ("do not land F2/F3 while wave-2 cold-read seats hold pins"). **No
round-17 item sequences the doc changes against the cold-read/measure window** (spec scan: `freeze`,
`wave 2`, `input-drift` appear only inside X07/X09/X10's own contract text). Recommendation to L1:
install doc edits either before the cold-read set starts or after `measure.py --rev` has been run at
the cold-read rev; do not land them between the two.

---

## 6. Gaps — recommendations/clauses with no owning item

| # | Gap | Why it matters | Cheapest close |
|---|---|---|---|
| G1 | R2's `master@origin` + `merge-base --is-ancestor` assertion (A4) | The audit's replacement sentence has three clauses; X06 covers only "branch tip". Without it, "the recorded rev is an ancestor" (SKILL:1034, runbook:282) stays a prose claim no tool checks. | Extend X06 with one `merge-base` field per row + optional `origin/<branch>` tip, or record an explicit decline in the closure. |
| G2 | `probes.mjs` `FXROOT` guard (B20) | `FXROOT` pointed at a live tree makes `fresh()` `rmSync` it. Only reachable by operator-set env; not a registered entry. | Backlog: guard in any future harness; no round-17 edit of round-16 evidence. |
| G3 | `.gitignore` additions (C2) | Present only as an uncommitted worktree modification; the branch tip still has the 1-line file. | Include `.gitignore` in the integration commit (pathspec-limited helper commit). |
| G4 | `jj-lane.sh commit` fail-closed auto-track check (A8) | Structural: a lane whose external config is lost or never init'd commits under default `auto-track=all()` (82-file snapshot in the trial). | Fleet-owner change in `scripts/hyaku/jj-lane.sh`; outside lane write scope. |
| G5 | X06-adjacent doc surfaces: `pin-disposition.py` docstrings `:42,:64-65,:315` ("current HEAD", "HEAD is reported") and `SCORECARD.md:244` ("committed-HEAD … observations") | After X06 the emitted `head` means branch tip; both texts become false. No item names them (W05 covers README, W03 a new section, R09 SKILL only). | Fold into X06's staged edit (docstrings) and an L1 SCORECARD line update; or record as known-stale. |
| G6 | Cold-read/measure sequencing (§5) | A doc append between a cold-read report and measurement uncredits it (`input-drift`), directly attacking C1's `6→8` claim. | L1 sequencing rule; no code change. |

---

## 7. Appendix — trial colocation hazards (not in §Recommendations; mapped for completeness)

| Hazard | Where covered / action |
|---|---|
| 1 `.ufo/` hot untracked surface | C1 (`auto-track=none()` holds); no action. |
| 2 ignored 1.8 MB jsonl + `--include-ignored` on named files | Helper pathspec discipline (`jj-lane.sh:200-216`); lane practice, no lane file. |
| 3 no symlinks/nested `.git`/hooks/attributes/LFS | Re-verified true (A10). |
| 4 detached HEAD is permanent | A5 + A2/X06 + B10. |
| 5 `git add` staging absorbed by jj | W06 draft (commit via helper) — land per §5 sequencing. |
| 6 jj dangling objects / `refs/jj/keep` in `--all` walks | Not an audit recommendation; S20 fact 23 (64 commits, empty-subject `63a13c6`). Any census must use explicit refs. No round-17 item; adjacent revenger rec. |
| 7 `jj file track <dir>` honours `.gitignore` | Helper behaviour (`:200-209`); no action. |
| 8 `.ufo/state/`/`.ufo/watchdog.log` never-commit surface | C2 (.gitignore, unlanded) + helper pathspec blocklist (`jj-lane.sh:183-184`). |

Out of scope by instruction (adjacent revenger items, not in either report's recommendations):
`immutable_heads()` alias absent (S20 fact 13), dirty-index guard, `refs/jj/keep` filtering.

---

## 8. Verification log (commands, exits, key lines)

```
git -C <lane> rev-parse refs/heads/master refs/remotes/origin/master
  → 98bea7da5801f4bc58e4187690ee1687c8a5061f  (both)
git -C <lane> symbolic-ref -q HEAD            → (no output), exit 1   [detached]
git -C <lane> merge-base --is-ancestor HEAD refs/heads/master → exit 0
git -C <lane> rev-list --count refs/heads/master..HEAD → 0
git -C <lane> show 98bea7da…:.gitignore       → `.ufo/interactive-sessions/` (1 line)
git -C <lane> status --porcelain              → ` M .gitignore`, ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt`, 5 `??`
git -C <lane> diff -- .gitignore              → +.ufo/state/  +.ufo/watchdog.log   (mtime 12:21:34)
git -C <lane> show 98bea7da…:tools/mutate-and-run.sh | grep -n 'git -C "$repo"'
  → 1001, 1005, 1010, 1019 (no show-toplevel in the file)
git -C <lane> show 98bea7da…:tools/pin-disposition.py | grep -n 'rev-parse|cat-file'
  → guard :255; pinned :280/:288/:296; HEAD :318/:329/:341
git grep -n 'merge-base' 98bea7da… -- tools SKILL.md → no matches
git -C <lane> rev-parse --verify --quiet c699c8c… / e69b488… → both resolve
ls .git/hooks | grep -vc '\.sample$' → 0 ; git config --get core.hooksPath → exit 1
  ; git config --global/--system --get core.hooksPath → exit 1 both
git check-attr -a -- tools/mutate-and-run.sh → empty, exit 0
find . -name .gitattributes -not -path './.git/*' → none ; .git/info/ = exclude, refs (no attributes)
find . -type l (excluding .git/.jj) → none
find . -type f -size +1M → only .ufo/interactive-sessions/…jsonl, `git check-ignore` → ignored
git ls-files | xargs stat → no tracked file >1 MiB
~/.config/jj/repos/*/metadata.binpb grep 'tameshi-shokunin/.jj/repo' → 900fa08… (mtime 12:07:32,
  auto-track="none()", 4 keys) and stale efc406… (Oct 19 18:31, trunk only); audit's 86a634… absent
S20JjLaneState.md facts 10/11/20/26 (authoritative jj read); S11HeadSweep.md §4/§5 (HEAD census, F1);
W06RunbookJj.md draft (runbook lines, ER-R3 "cite the pushed hash")
spec1.json scan: 'ancestor' / 'merge-base' / 'origin tip' / 'freeze' / 'input-drift' in item Targets
  → no owner for A4, G3, G6
```

Not run: any `jj` command (Target does not authorise it; S20 is the round's authoritative jj reader);
no lane selftests (read-only mapping); no writes outside this report.

**Verdict: built** — 37 recommendation rows mapped (10 §5 risk clauses, 22 §1 replacement groups,
5 trial recommendations): **6 FIX rows** (X05 owns A1/B1; X06 owns A2/B10, with A4's ancestry clause
needing an explicit target extension; R09 owns A3's SKILL draft, L1 installs it), **26 ALREADY TRUE**
(4 of them carry an optional sub-clause that is declined), **5 DECLINE** (A8 fleet helper; B2/B3
plumbing alternatives; B20 FXROOT; C3's absolute "no changes"), plus **6 gaps** where the round's
item text does not cover the recommendation it would otherwise be credited with.
