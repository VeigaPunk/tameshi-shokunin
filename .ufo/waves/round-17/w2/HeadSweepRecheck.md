# HeadSweepRecheck — F1–F3 and new HEAD reads at `eb7838b` (round 17, w2)

Seat: `TameshiR17.HeadSweepRecheck-2` · rev `eb7838b16490ca7ba17ea3242ade76a61f744af2` · 2026-10-20.
Method: detached fleet-mirror clone at the landing (`git clone` + `checkout --detach eb7838b`), all tool execution from the clone; jj 0.45.1 behaviour reproduced in `/tmp` scratch repos only; the shipped functions `check_historical_waiver`, `resolve_historical_rev` and `head_observation` imported from the clone and executed against `/tmp` fixtures; live lane touched by read-only git probes only. No tool installed or upgraded.

## 0. Ground truth: what jj 0.45.1 actually does to git HEAD (executed)

```
$ jj --version                                  → jj 0.45.1-7c41cdeb…
$ jj config get git_head                        → "Config error: Value not found" (default)
$ git init; commit c0 (f=v1); jj git init --colocate; jj new; echo v2 > f
  symbolic-ref -q HEAD                          → exit 1 (DETACHED)
  git rev-parse --short master                  → a96422b   (branch unchanged)
  git rev-list --count master..HEAD             → 1
  git show HEAD:f.txt                           → v2        (the just-snapshotted edit)
  git show master:f.txt                         → v1
  git status --porcelain -- f.txt               → (empty)
  git merge-base --is-ancestor master HEAD      → rc 0
```

So **HEAD is the working-copy parent `@-`**, not `@`: after a snapshot (`jj new`/`jj commit`) it carries the bytes just edited into `@`, one or more commits ahead of the branch, and `porcelain` is empty. Round 17's `@-` wording (`SKILL.md:1033`, `:1819`, every ER-jj) is correct on this host. `S11HeadSweep.md:39`'s naming note ("HEAD names the snapshot `@`") is not reproducible; its operational conclusion — HEAD is not the bookmark — stands.

One correction to the wave-1 mechanism: `drift` is **not** permanently blind. Immediately after a snapshot `porcelain` is empty, but the next edit makes it `" M f.txt"` (observed in the same scratch repo). `SKILL.md:1035`'s hedged wording ("a clean porcelain is not tip evidence") is accurate; "drift cannot fire" overstates it.

Live lane today (read-only): `git -C <lane> rev-parse HEAD` → `eb7838b…`, `symbolic-ref -q HEAD` → exit 1 (detached), `rev-parse --short refs/heads/master` → `eb7838b`, `rev-list --count master..HEAD` → `0`. The divergence is latent, exactly as at `98bea7d`.

## 1. F1 — `pin-disposition.py` live HEAD read — **closed (holds)**

| Site at `eb7838b` | Evidence executed | Result |
|---|---|---|
| `tools/pin-disposition.py:324-370` `detect_branch` | attached HEAD → short name; detached → `refs/remotes/origin/HEAD`, then `master`, `main`, first local branch | mirrors `scripts/hyaku/jj-lane.sh:53-65` |
| `:374-449` `head_observation` | raw `HEAD^{commit}` still read (`:392`) but `commit` is replaced by `refs/heads/<branch>^{commit}` (`:427-430`); blob read as `<tip>:<path>` (`:431-449`); `head_differs_from_branch` recorded (`:430`) | branch-tip bytes |
| docstrings `:42-50` | name the detached/jj case and the degradation (no local branch → raw HEAD, new fields null) | contract text fixed |
| `python3 tools/pin-disposition.py --selftest` | exit 0, `SELFTEST: PASS (19/19)`, `SELFTEST_CASE detached-head-uses-branch-tip PASS` | suite green |
| independent fixture (detached HEAD 1 ahead of `master`, `HEAD:x=v2`, `master:x=v1`) | `head_observation` → `{'branch': 'master', 'commit': <master tip>, 'blob_sha256': <v1 sha>, 'head_differs_from_branch': True}` | reads the tip, not `@-` |

No remaining action on F1.

## 2. F2 — active prose that defines the reading over HEAD

**Rewritten in place (closed):**
- `SKILL.md:1033-1035` — `current`/`stale`/`drift` now resolve `refs/heads/<branch>`; `:1033` says "never a jj working-copy `HEAD` (`@-`), which no remote has".
- `SKILL.md:1536` — recipe step 2 now says "sibling branch-tip commits"; `:1844` step 4 — "never at `HEAD`".
- `corpus/knowledge/operator-runbook.md:49-53` — recipe uses `<tip>` and `merge-base --is-ancestor <REV> <tip>`; `:281-283` table rewritten to branch tip; ER-R3 at `:514`.

**Errata-only (literal line unchanged; one appended ER-jj carries the rule):**

| path:line | literal text still there | errata |
|---|---|---|
| `fleet-kill-rate-ledger.md:290-291`, `:320` | `show HEAD:<path>`, `status --porcelain`, `merge-base … HEAD` | ER-jj `:420` |
| `service-limits.md:48` | "`drift` (worktree differs from HEAD)" | ER-jj `:279` |
| `incremental-pin-disposition.md:117`, `:264` | "HEAD blob, tree clean"; "each repo's current HEAD commit" | ER-jj `:386` |
| `verification-patterns-fleet.md:82` (F3) | "Baseline freeze via `git archive HEAD`" | ER-jj `:309` |

Census: `SKILL.md` HEAD-token lines 16 → 18; `corpus/knowledge` 79 → 81 lines in 24 → 25 files (each ER-jj is one long line; `operator-runbook` lost three HEAD lines to in-place rewrites). The errata explicitly enumerates every instruction it overrides (`show HEAD:<path>`, ancestor of HEAD, worktree vs HEAD, `git archive HEAD`) and cites the canonical rule — this matches `S11HeadSweep.md` F2's "append-only qualifier, one wording, one place of record". Residual is a copy-paste trap only: executing the literal line yields the wrong bytes. Non-blocking.

## 3. F3 — `git archive HEAD` baseline freeze — **errata-only**

`corpus/knowledge/verification-patterns-fleet.md:82` still instructs `git archive HEAD`; the ER-jj at `:309` says it now means the branch tip. Same pattern as F2, so it holds under the lane's append-only convention; the literal command was not qualified in place. Non-blocking; qualify on next touch.

## 4. New HEAD reads introduced by round-17 tools

`tools/` swept by the literal token set (`\bHEAD\b`, `@{u}`, `--abbrev-ref`, `branch --show-current`, `symbolic-ref`, `for-each-ref`): 9 files, **90 HEAD-token lines across 7 files**, and 0 uses of `@{u}`, `--abbrev-ref` or `branch --show-current`. Round-17 evidence trees (`.ufo/evidence/round-17/measure.py`, `coldread/trace-inputs.py`, `coldread/assemble.py`, `jj/head-vs-branch.sh`) swept the same way.

### 4.1 `tools/evidence-disposition.py:518` (G2) and `:450` (G3) — **new, misread-capable** (the finding)

v1 had zero git calls (`S11HeadSweep.md` §4); v2 adds both, and both run on the **live lane** (`--root .`, `SKILL.md:1835`, `:1850`).

Executed, snapshot-shaped `/tmp` repo (`HEAD` detached 1 ahead of `master`, `HEAD:x=v2`, `master:x=v1`, worktree `v2`, `porcelain` empty — byte-for-byte the jj `@-` shape reproduced in §0):

```
check_historical_waiver(repo, "tools/x.sh", sha256("v1\n")) → ACCEPTED (no finding)
control: HEAD=master attached, worktree dirty v2           → historical_input_uncommitted
G3, HEAD behind the branch (jj-edit-like fixture):
  resolve_historical_rev(repo, <branch tip>) → historical_input_unavailable:
  "rev 85156eb… is not an ancestor of HEAD"
```

- **G2 is permissive under jj.** A waived tool whose bytes live only in `@-` — on no branch, on no remote — satisfies "live bytes equal `HEAD:<path>`". The page's own canonical rule (`SKILL.md:1033`) rejects exactly those bytes for the pin reading ("never a jj working-copy `HEAD` (`@-`), which no remote has"). The contract row `SKILL.md:1826` documents `HEAD:<path>` literally and says "A worktree edit is tampering" — true only in the window between an edit and the next jj snapshot; any jj command closes it and the gate returns 0. So the v2 waiver guard means "recorded somewhere in jj's local history", not "committed to the branch".
- **G3 is HEAD-relative, not branch-relative.** It fails closed (exit 2, never a false pass), but whenever HEAD is not on the branch lineage (`jj edit` of an older change, a rebase of `@-`, a checkout behind the branch) a valid pinned rev is refused and the gate cannot evaluate.
- Current manifests are unaffected today: `.ufo/evidence/round-17/dispositions.json` waives `tools/mutate-and-run.sh` and `tools/pin-disposition.py` at `4acc607d…`; `git merge-base --is-ancestor 4acc607d HEAD` → rc 0; `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json` in the clone → exit 0, `"failed": 0, "findings": 0, "passed": 11, "superseded": 1`. The weakness is invisible in a clone because the clone's HEAD **is** the requested rev.
- Fix belongs to the L1: compare live bytes to `refs/heads/<branch>:<path>` (reuse `detect_branch`/`head_observation`), or carry `head_on_branch`/`head_branch` in the payload and amend `SKILL.md:1826` to name `@-` and define "committed".

### 4.2 `assemble.py:847-850` — HEAD fallback — helper only

`resolve_expected_page` scans observed `read_rev`s then `HEAD`; a page resolved on the fallback records `"rev": "HEAD"` (symbolic, not 40-hex). Coverage is sha-keyed (`coverage()` uses `(sha, start)`), so no false credit — the label is just non-reproducible. gap-minor: resolve the fallback to a 40-hex or drop it.

### 4.3 `trace-inputs.py:538` — receipt `rev` = root HEAD — safe in the prescribed root

`rev-parse --verify HEAD` of `--root`; the prescribed root is the clone (`HEAD` → `eb7838b…`, `symbolic-ref` exit 1), so `rev` == the requested read rev. There is no guard against pointing it at a jj lane root, where `rev` would be `@-`; the cold-read interface forbids that root. gap-minor.

### 4.4 `measure.py` — `--rev HEAD` accepted, labeled — not a misread

`main()` requires `--rev` (`parser.error('--rev is required')`), so there is no implicit HEAD; the selftest `revision-40hex` accepts the symbolic input but requires the output to be 40-hex and `rev_input == "HEAD"`. A symbolic read is self-describing.

### 4.5 `registry-check.py` / `registry.json` — jj-safe in `--rev` mode, conditional live

`registry-check.py:477` checks the clone's HEAD and `:656` is a selftest fixture. With `--rev`, rows are re-rooted into `git clone` + `checkout -q --detach <sha>` (`:453`, `:466`, `:1269`), so clone HEAD == the requested rev — jj-safe. The only HEAD row of 29 is `registry.json:426-434` `measure-round16-rev` (`--rev HEAD --repo .`, tag `baseline`); it would read the lane's `@-` only in the warned-against live mode (`:1287-1294`; page rule `SKILL.md:1841`: run with `--rev`, never live). Conditional and documented, not a misread.

### 4.6 `mutate-and-run.sh` — no new live HEAD read

`:286` is `fixture_commit` (selftest fixture), `:1742-1747` the selftest canary's HEAD/refs assertions, `:107`/`:826` prose. Round-17's `git_clean` + repo-identity guard add no HEAD dependency.

## 5. Residual unknowns / not run

- I did not run `jj` against the lane or any sibling (contract) and did not run `registry-check.py` end-to-end (C2 seats' claim).
- `@-` measured on jj 0.45.1, default config. `git_head` is configurable; `git_head = "@"` would put the live worktree bytes in HEAD and make every live HEAD read strictly worse.
- The G2/G3 hazard is latent today (HEAD == master); it activates with the next jj snapshot before landing.

**Verdict: partial** — F1 is closed (selftest 19/19 plus an independent detached fixture); F2/F3 hold by append-only errata with literal copy-paste traps left in place; and one genuinely new misread-capable HEAD read landed in round 17 — `evidence-disposition.py` G2 accepts jj `@-` bytes as "committed" and G3 refuses branch-tip revs when HEAD is off the branch — latent until the lane's HEAD next moves off `master`.
