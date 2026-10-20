# S11HeadSweep — git HEAD semantics in lane-owned text and code (round 17, w1)

Seat: `TameshiR17.S11HeadSweep` · lane rev `98bea7da5801f4bc58e4187690ee1687c8a5061f` (`master`, detached) · 2026-10-20 · read-only sweep, no edits to lane files.

Scope swept at the rev (bytes read via `git show <rev>:<path>`): `tools/` (7 files), `SKILL.md`, `corpus/knowledge/` (24 `.md`), `corpus/QUALITY.md`, `.ufo/evidence/round-15/verify.py`, `.ufo/evidence/round-16/measure.py`, `.ufo/evidence/round-16/coldread/assemble.py`.
Evidence base: `JjAuditTameshi.md` §1–§3, §5 (R2) and `JjTrialTameshi.md` steps 4–5.

Token set swept as literal regex: `\bHEAD\b`, `@\{u\}`, `--abbrev-ref`, `branch --show-current`. Result: **115 matching lines in scope**, all matching the `HEAD` token; zero `@{u}`, zero `--abbrev-ref`, zero `branch --show-current`. Measured idiom breakdown (`git grep -n`, literal): `rev-parse HEAD` 8 · `rev-parse --short HEAD` 2 · `HEAD^{commit}` 1 · `["rev-parse","HEAD"]` 5 · `show HEAD:`/`HEAD:<path>` 14 · `git archive HEAD` 1 · `merge-base --is-ancestor … HEAD` 3. `corpus/QUALITY.md`, `.ufo/evidence/round-15/verify.py` and `.ufo/evidence/round-16/coldread/assemble.py` are **clean** (0 hits; `assemble.py:68` `HEADING_RE` is a heading regex, not a git token; `verify.py` is wholly rev-addressed).

Per-file census (lines):

```
24 fleet-kill-rate-ledger.md   16 SKILL.md              14 pin-disposition.py
11 operator-runbook.md         10 closeout-r11.md        5 mutate-and-run.sh
 5 verification-patterns-fleet  5 incremental-pin-disp    4 mutation-case-kagi-checklist
 4 fleet-suite-census           3 service-standing-state  3 gates-survey-kagi
 2 self-hardening-r6            1 each: service-optin-protocol, service-limits,
                                mutation-case-{tsukuroi-census,kumitate-round-gate,
                                kumitate-claims,kagi-census}, executor-test-sufficiency,
                                arm-class-matrix, round-16/measure.py
```

## 0. Live HEAD state observed (executed, read-only)

| Probe | Result |
|---|---|
| `git -C tameshi-shokunin symbolic-ref -q HEAD` | exit 1 → **detached** |
| `.git/HEAD` | `98bea7da5801f4bc58e4187690ee1687c8a5061f` (detached sha, not `ref: refs/heads/master`) |
| `git reflog -3` | top entry `98bea7d export from jj` — jj writes HEAD on export |
| `git rev-parse '@{u}'` | `fatal: HEAD does not point to a branch`, exit 128 |
| `git branch --show-current` | empty, exit 0 |
| `git for-each-ref --points-at HEAD refs/heads` | `refs/heads/master` |
| `sha256(git show HEAD:SKILL.md)` vs `sha256(git show refs/heads/master:SKILL.md)` | equal (`906fb649…`) — **today HEAD still equals the branch tip** |
| sibling colocation (`[ -e .jj ]`) | `kaidoku`, `kama`, `mado`, `tameshi` are colocated (audit saw only `mado`) |
| sibling HEAD attachment | `mado` attached (HEAD == master `0ab1ccc`); `kaidoku` **detached** `9011581`, branch `main`; `kama` **detached** `cff9e62`, branch `master` |

So: the lane and two siblings are *already* detached-HEAD repos; the lane's HEAD coincides with the branch tip only because the last jj export landed on the tip. Anything that reads `HEAD` and calls it "the committed branch bytes" is one jj mutation away from being wrong (`JjAuditTameshi.md` §2.1, §2.3).

Naming note for the round's brief: the audit observed HEAD naming the **working-copy snapshot `@`**, not its parent `@-` — `HEAD:file.txt` carried the just-edited `dirty` line while `master:file.txt` did not and `master..HEAD` counted 1 (`JjAuditTameshi.md` §2.3). Either way the operational consequence is identical: **HEAD is not the bookmark**, so `@{u}`/`--abbrev-ref`/`branch --show-current` lose their branch meaning and `git show`/`archive HEAD` may expose bytes that were never committed to the branch.

Executed shape reproduction (pure git, no jj; scratch `/tmp/tameshi-r17w1-S11HeadSweep-OQ6K1V`): a detached commit carrying working-copy bytes on top of `master` gives
`git show HEAD:f.txt → "committed\ndirty"`, `master:f.txt → "committed"`, `git status --porcelain -- f.txt → (empty)`, `merge-base --is-ancestor master HEAD → exit 0`, `git archive HEAD → committed+dirty`, `git archive master → committed`.
This is exactly the jj `@`-snapshot shape: **the `drift` test goes blind and `current`/`archive` can credit uncommitted bytes.**

## 1. `tools/` — 19 hits

| path:line | site | class | jj colocation changes meaning? | rec |
|---|---|---|---|---|
| `tools/mutate-and-run.sh:107` | comment "their pins are ancestors of HEAD" | prose (comment) | no — historical rationale | keep |
| `tools/mutate-and-run.sh:785` | comment "= kagi HEAD fecee87 blob" | prose (record) | no — names a sibling sha, not a live read | keep |
| `tools/mutate-and-run.sh:1534` | `grev=$(git -C "$grepo" rev-parse HEAD)` | **fixture** (`$root/fleet/fakerepo`, `$root=$(mktemp -d /tmp/tameshi-r4-2-selftest.XXXXXX)`) | no — no `.jj` ancestor | keep |
| `tools/mutate-and-run.sh:1593` | `grev_exec=$(git -C "$grepo" rev-parse HEAD)` | fixture (same repo) | no | keep |
| `tools/mutate-and-run.sh:1628` | `grev_noexec=$(git -C "$grepo" rev-parse HEAD)` | fixture (same repo) | no | keep |
| `tools/pin-disposition.py:6` | docstring "what does the repo's HEAD carry?" | prose | no | keep |
| `tools/pin-disposition.py:42` | docstring: `head` = "current HEAD commit, the sha256 of the path's blob at HEAD" | prose defining an output contract | **yes, silently** — contract text does not admit a snapshot commit | fix (doc) |
| `tools/pin-disposition.py:64` | docstring "Current HEAD may differ from the pinned commit…" | prose | yes, silently | fix (doc) |
| `tools/pin-disposition.py:65` | docstring "…HEAD is reported separately…" | prose | yes, silently | fix (doc) |
| `tools/pin-disposition.py:80` | docstring "…super-repo HEAD" | prose (identity guard) | no | keep |
| `tools/pin-disposition.py:315` | docstring "Resolve current HEAD and the sha256 of <path>'s blob at HEAD" | prose defining behaviour | **yes** — "current HEAD" is ambiguous under colocation | fix (doc + code) |
| `tools/pin-disposition.py:318` | `git rev-parse --verify --quiet --end-of-options HEAD^{commit}` on `repo_real` | **sibling HEAD** (live mode; manifest legs are 6 sibling repos; schema would allow a `tameshi-shokunin` leg) | **yes** — detached `HEAD` = jj working-copy snapshot `@`; `head.commit` may be on no bookmark and `head.blob_sha256` may contain bytes never committed to the branch; `worktree == head` by construction hides drift | **fix** (see F1) |
| `tools/pin-disposition.py:699` | comment "super-repo HEAD" | prose | no | keep |
| `tools/pin-disposition.py:706` | `super_commit = git(fleet, ["rev-parse","HEAD"])` | **fixture** (`tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir="/tmp")`) | no | keep |
| `tools/pin-disposition.py:712` | `kumitate_empty = git(kumitate, ["rev-parse","HEAD"])` | fixture | no | keep |
| `tools/pin-disposition.py:717` | `kumitate_pinned = git(kumitate, ["rev-parse","HEAD"])` | fixture | no | keep |
| `tools/pin-disposition.py:718` | comment "HEAD stays at the pin" (fixture) | prose | no | keep |
| `tools/pin-disposition.py:728` | `kagi_pinned = git(kagi, ["rev-parse","HEAD"])` | fixture | no | keep |
| `tools/pin-disposition.py:733` | `kagi_head = git(kagi, ["rev-parse","HEAD"])` | fixture | no | keep |

Notes: (a) no other tool has a git HEAD token — `bash-witness-study.py` reads an explicit rev, `context-capture.py:1447` is a literal argv string never executed, `evidence-disposition.py` / `repeat-control.py` / `witness-metadata.py` contain zero git calls. (b) Fixture reads **should stay `HEAD`**, not become `refs/heads/<name>`: `mutate-and-run.sh`'s fixture `git init` does not pin `init.defaultBranch` (only `pin-disposition.py` passes `-c init.defaultBranch=main`), so a literal branch name would be less portable than `HEAD`. (c) `mutate-and-run.sh:1000–1035` (rev-addressed `git -C "$repo"`) carries the audit's R1 identity-guard risk, but contains no HEAD token, so it is outside this sweep's classification.

## 2. `SKILL.md` — 16 hits

| path:line | site | class | jj colocation changes meaning? | rec |
|---|---|---|---|---|
| `SKILL.md:1033` | rule: `current` = `git show HEAD:<path>` sha256 == pin | **prose, active rule** | **yes** — in a colocated repo this can credit jj-snapshot bytes | fix (append) |
| `SKILL.md:1034` | rule: `stale` = recorded rev ancestor of HEAD ∧ live blob differs | prose, active rule | yes — "ancestor of HEAD" stays true for a snapshot commit (reproduced: exit 0) | fix (append) |
| `SKILL.md:1035` | rule: `drift` = worktree ≠ HEAD (`status --porcelain`, live sha ≠ HEAD blob) | prose, active rule | **yes** — post-snapshot `porcelain` is empty and worktree == HEAD, so drift is unobservable | fix (append) |
| `SKILL.md:1043` | table header "recorded rev  live HEAD  relation" | prose (dated record) | no | keep |
| `SKILL.md:1048` | cell `HEAD (r8)` | prose (dated record) | no | keep |
| `SKILL.md:1049` | cell `HEAD (r8)` | prose (dated record) | no | keep |
| `SKILL.md:1057` | narrative: live sha vs "HEAD blob" | prose (dated observation) | no | keep |
| `SKILL.md:1172` | table header "recorded-rev live-HEAD" | prose (dated record) | no | keep |
| `SKILL.md:1183` | narrative "their repos' committed HEAD" | prose (dated observation) | no | keep |
| `SKILL.md:1185` | narrative "(HEAD `72b038da`)… (HEAD `12c8f08a`)" | prose (dated record) | no | keep |
| `SKILL.md:1204` | narrative "worktree … vs its HEAD blob" | prose (dated observation) | no | keep |
| `SKILL.md:1403` | table header "live-HEAD" | prose (dated record) | no | keep |
| `SKILL.md:1414` | narrative "their repos' committed HEAD blobs" | prose (dated observation) | no | keep |
| `SKILL.md:1415` | narrative "(HEAD …)" | prose (dated record) | no | keep |
| `SKILL.md:1417` | narrative "(HEAD …)" | prose (dated record) | no | keep |
| `SKILL.md:1536` | recipe step: "Retain stdout with its sibling HEAD commits…" | prose, **active recipe** | yes — "HEAD commits" may be snapshot commits; a reader cannot tell | fix (append a detachment field) |

## 3. `corpus/knowledge/` — 79 hits (all prose; 6 are runnable recipes)

| path:line | site | class | jj colocation changes meaning? | rec |
|---|---|---|---|---|
| `fleet-kill-rate-ledger.md:52,65,74,83,102,113,183,184,185,261,276,277` | sibling HEAD records (kumitate/kagi/tsukuroi/mado) | prose records | no — dated, shas still name objects | keep |
| `fleet-kill-rate-ledger.md:290,291` | ER-3 recipe: `git show HEAD:<path>`, `status --porcelain -- <path>` | prose, **active command set** (cited by SKILL.md:1031-1036 and operator-runbook:51) | **yes** — recipe's `current`/`drift` rows inherit the snapshot blindness | fix (append caveat) |
| `fleet-kill-rate-ledger.md:293` | readings definition: `current`/`stale`/`drift` over HEAD | prose, active definition | **yes** | fix (append) |
| `fleet-kill-rate-ledger.md:297,324,337,338,358,359,379,381` | reading tables / "Observed owner HEAD = worktree SHA256" | prose records | no — dated (`observed_at` 2026-10-20T04:59:26Z); mado was attached at that read | keep |
| `fleet-kill-rate-ledger.md:320` | ER-4 tick paragraph with `show HEAD:<path>` + `merge-base --is-ancestor <rev> HEAD` | prose, **active command set** | **yes** | fix (append caveat) |
| `operator-runbook.md:30` | "Tameshi HEAD at this write: `b8eb96e`" | prose record (lane-own) | no — dated | keep |
| `operator-runbook.md:51,52,53` | Quick-start recipe: `show HEAD:<path>`, `status --porcelain`, `merge-base --is-ancestor <REV> HEAD` (sibling) | prose, **active recipe** | **yes** | fix (precheck line) |
| `operator-runbook.md:281,282,283` | reading-rule table `current`/`stale`/`drift` | prose, active definition | **yes** | fix (append) |
| `operator-runbook.md:316,326,336` | executed tick table / narrative | prose records | no | keep |
| `operator-runbook.md:493` | ER-R1 "vs HEAD `b8eb96e`" (lane-own) | prose record | no — dated | keep |
| `closeout-r11.md:39,323,324,358,360,361,393` | lane-own/sibling HEAD records (`606716f`, `af8adf1`, `f7bfc9f`) | prose records | no — closed round | keep |
| `closeout-r11.md:167,168,169` | command set: `show HEAD:<path>`, `status --porcelain`, `merge-base … HEAD` | prose, **runnable recipe in a closed record** | yes if re-run today | keep record + append caveat (low priority) |
| `verification-patterns-fleet.md:82` | lesson: "Baseline freeze via `git archive HEAD`, tracked files only" | prose, **active method statement** | **yes** — `archive HEAD` snapshots jj working-copy bytes (reproduced) | **fix (append)** |
| `verification-patterns-fleet.md:185,254,278,279` | game-dev-2d records (`rev-parse HEAD`) | prose records | no — sibling not colocated | keep |
| `incremental-pin-disposition.md:117` | "recorded pin = live file = HEAD blob, tree clean" | prose, method definition | yes, silently | fix (append) |
| `incremental-pin-disposition.md:241` | "between `fecee87` and HEAD" (kagi) | prose record | no | keep |
| `incremental-pin-disposition.md:264` | invariant: receipt "records … each repo's current HEAD commit" | prose, **active receipt contract** | yes — a snapshot commit satisfies the letter, not the intent | fix (append "and whether HEAD is a branch tip") |
| `incremental-pin-disposition.md:279,341` | falsifier prose / "recorded HEAD digests" | prose | no | keep |
| `mutation-case-kagi-checklist.md:23,24,25,270` | kagi HEAD records (`fecee87`) | prose records | no | keep |
| `fleet-suite-census.md:40,88,336` | kumitate HEAD records (`175de6b`) | prose records | no | keep |
| `fleet-suite-census.md:369` | Appendix A: `cd kumitate-shokunin; git rev-parse --short HEAD` | prose, **recorded command** | no — kumitate not colocated; a re-run after colocation would drift | keep |
| `service-standing-state.md:164,165` | sibling records (`fac745b`, `de22dfd`, `merge-base --is-ancestor`) | prose records | no | keep |
| `service-standing-state.md:220` | "[O] tameshi HEAD `b8eb96e`" (lane-own) | prose record | no — dated | keep |
| `gates-survey-kagi.md:5,7,560` | kagi survey revision records (`4e48b77`, `fecee87`) | prose records | no | keep |
| `self-hardening-r6.md:13,18` | lane-own `git show HEAD:tools/mutate-and-run.sh` hashes identical | prose record (lane-own) | **yes, conditionally** — reproduces today (HEAD == tip) but not after a jj snapshot | keep (dated claim; do not replay) |
| `service-optin-protocol.md:13` | "tameshi HEAD `4494715`, mado HEAD `c8f6667`, tsukuroi HEAD …" | prose record (lane-own + siblings) | no — dated | keep |
| `service-limits.md:48` | policy: `drift` = "worktree differs from HEAD" | prose, **active policy** | **yes** | fix (append) |
| `mutation-case-tsukuroi-census.md:11` | tsukuroi HEAD `165307fe` | prose record | no | keep |
| `mutation-case-kumitate-round-gate.md:17` | kumitate HEAD record | prose record | no | keep |
| `mutation-case-kumitate-claims.md:15` | kumitate HEAD `175de6ba` + `show HEAD:` | prose record | no | keep |
| `mutation-case-kagi-census.md:16` | kagi HEAD `fecee874` | prose record | no | keep |
| `executor-test-sufficiency.md:47` | `git -C kumitate-shokunin rev-parse HEAD` → `175de6b` | prose record | no | keep |
| `arm-class-matrix.md:490` | `git -C kumitate-shokunin rev-parse --short HEAD` → `175de6ba` | prose record | no | keep |

`corpus/QUALITY.md`: **0 hits** — no change.

## 4. Gate scripts

| path:line | site | class | jj effect | rec |
|---|---|---|---|---|
| `.ufo/evidence/round-16/measure.py:435` | `git_in(repo,'rev-parse','HEAD')` inside `selftest()`, `repo = tmp/synrepo` with `HOME=tmp` | **fixture** | none — no `.jj` ancestor | keep |
| `.ufo/evidence/round-15/verify.py` | zero `HEAD`/branch-symbolic tokens; every read is `git show <rev>:<path>` / `rev-parse <rev>^{commit}`, REV is a required CLI arg | revision-addressed | none | keep |
| `.ufo/evidence/round-16/coldread/assemble.py` | zero git invocations; `HEADING_RE` (line 68) is a markdown-heading regex | not a git token | none | keep |

Whole-tree confirmatory sweep (1296 files at the rev): `@{u}` 0, `--abbrev-ref` 0, `symbolic-ref` 0; one `branch --show-current` — `.ufo/evidence/round-12/ReportScribe/probe-capture.txt:5`, a captured transcript (with `git rev-parse HEAD` at `:3`), i.e. evidence prose, not active code. Keep.

## 5. Recommendations, ordered

**F1 — `tools/pin-disposition.py:318` (only live-HEAD code site; sibling; already declared as C2's "branch-tip resolution").**
Keep `HEAD^{commit}` (it always resolves; `@{u}` exits 128 — executed). Add detachment visibility rather than substituting a hardcoded branch:
- `git symbolic-ref -q HEAD` → `head_ref` (string) or null; `head_on_branch` bool.
- when detached: `git for-each-ref --points-at HEAD --format='%(refname)' refs/heads` → `head_branches` (may be empty; today `refs/heads/master` for tameshi, `refs/heads/main` for kaidoku).
- Never hardcode `master`: kaidoku's branch is `main` (observed).
- When `head_on_branch` is false, label `head.blob_sha256` as snapshot bytes: a jj `@` may carry working-copy content, and `worktree == head` then makes drift unobservable (reproduction §0).
- Update docstrings `:42,:64,:65,:315` to name the snapshot case. Per QUALITY 20 this lands as a staged copy, not an in-place edit during the wave.

**F2 — active prose that defines the reading over HEAD (highest leverage).** Append-only qualifier at `SKILL.md:1033-1035`, `SKILL.md:1536`, `operator-runbook.md:281-283` and its recipe `:51-53`, `fleet-kill-rate-ledger.md:290-293,:320`, `service-limits.md:48`, `incremental-pin-disposition.md:117,:264`:
> In a colocated jj repo, HEAD may be the working-copy snapshot `@`, not the branch tip. Resolve `refs/heads/<branch>` (or the pushed remote tip) for `current`/`stale`, and treat `git status --porcelain`/worktree-vs-HEAD equality as uninformative: jj snapshots the worktree into `@`, so `drift` cannot fire.

One wording, one place of record, then cite it from the others (the round-16 append pattern).

**F3 — `verification-patterns-fleet.md:82`.** `git archive HEAD` in a colocated repo archives jj-snapshot bytes (reproduced: archive HEAD has the "dirty" line, archive master does not). Qualify the baseline-freeze instruction to resolve the branch tip.

**F4 — keep everything else.** All 62 record lines and all fixture/selftest HEAD reads are correct as written; do not churn them. `closeout-r11.md:167-169` and `fleet-suite-census.md:369` are closed records: append a caveat only if re-run.

**Timing constraint for the L1:** do not land F2/F3 while wave-2 cold-read seats hold `skill_sha256`/`inputs` pins — an append changes the page digest and, under C1's input-keyed rule, uncredits in-flight `commands_executed` entries (`input-drift:<path>`). Land after the cold-read set closes, or accept re-reads.

## 6. Residual unknowns / not run

- I did not run `jj` in the live lane or any sibling (contract: read-only only when the Target says so; this Target does not). The snapshot behaviour is taken from `JjAuditTameshi.md` §2.1/§2.3 and reproduced with plain git in `/tmp/tameshi-r17w1-S11HeadSweep-OQ6K1V` (§0). `[INFERENCE]` the first mutating jj command in tameshi (`jj commit`/`jj new`/`jj edit`) moves HEAD off `refs/heads/master`; read-only `jj log`/`jj st` did not detach in the audit.
- I did not execute any in-scope tool's `--selftest`. The fixture-HEAD classification is static (path of `$root`/`tmp`) plus the fact that `mktemp -d /tmp` has no `.jj` ancestor.
- `kaidoku` has no `refs/heads/master` (only `main`, observed), so any future fix that assumes `master` would fail there; that sibling is not a manifest leg today.
- Live sibling state is timestamped: `mado` was attached at this read (`HEAD == master == 0ab1ccc`), so today's live `pin-disposition` run is unaffected; kagi/tsukuroi/kumitate are still git-only, so F1 is latent for the six manifest legs and live only if a leg names a colocated repo.

**Verdict: built** — 115 in-scope HEAD-token sites classified; 1 live code fix (F1), 7 active-prose groups (F2), 1 method lesson (F3); 0 lane-own code reads that are wrong today, and 0 uses of `@{u}`/`--abbrev-ref`/`branch --show-current` in active code.
