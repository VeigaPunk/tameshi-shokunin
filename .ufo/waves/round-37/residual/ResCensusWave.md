# ResCensusWave — residual falsification, round 37 attempt 3 (census + wave accounting)

Seat: reviewer/critic (read-only). Lane tip verified `ba3c35fb6c9582fcf2351c59c61661dd7a8e7400`;
`refs/heads/master` == `refs/remotes/origin/master` == `ba3c35f…` (`git show-ref`), working HEAD
detached at the same commit, `git status --porcelain` = 0 lines.

## Verdict: ALL ASSIGNED CLAIMS SURVIVE — no defect found (0 BLOCKER / 0 MAJOR / 0 MINOR)

Every claim was attacked with executed commands at both revisions; none broke.

## 1. Round accounting — VERIFIED

### 1.1 Census receipts exit 0
- `.ufo/evidence/round-37/census/start.exit` = `0`; `start.stdout` ends
  `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` + `EXIT_CODE=0`.
  Committed at `32826f3` ("round-37: resolve r36 control provenance and mode").
- `.ufo/evidence/round-37/census/end-attempt3.exit` = `0`; `end-attempt3.stdout` ends
  `tameshi ok …/corpus/SOURCES.md` + `EXIT_CODE=0`; stderr empty. Committed at tip `ba3c35f`
  (`git log --name-status -- .ufo/evidence/round-37/census/`: end-attempt3.* added by `ba3c35f`,
  end.* by `e6185d5`, start.* by `32826f3`).
- The older `end.exit`/`end.stdout` pair (commit `e6185d5`) also exits 0, and
  `diff end.stdout end-attempt3.stdout` → IDENTICAL.

### 1.2 Census re-run at the live tip (read-only)
```
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin tameshi
→ exit=0, stderr empty, stdout byte-IDENTICAL (diff clean) to the committed
  end-attempt3.stdout: 8 pre-existing W04 duplicate-url rows (S047, S048, S075, S076,
  S077, S078, S081, S092), W01 S101 tierC note, plus the W04 S104 duplicate-url warning
  for the new row (shared bashref.texi URL base with S097), then the ok line.
```
Command chosen from the canonical record `LOG.md:1986-1987` (`sources-census.sh validate`).
Script audited before running: writes exist only in `selftest` mode (temp fleet) and behind
`--out`; without `--out`, `emit` prints to stdout — no lane or fleet write.

### 1.3 Frozen row-count 100 → 101
```
git show d9c496b:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  → 100
git show ba3c35f…:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  → 101
grep -cE … corpus/SOURCES.md   (clean tree == tip)                                        → 101
```
- `d9c496b` resolves to `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`, the exact
  `contract.json` `before.rev` / `frozen_control_input.source_revision`.
- At `d9c496b` the string `S104` appears only at line 422 (`- Next unused id: S104.`) — no table
  row. At tip, the S104 row is `corpus/SOURCES.md:113` and the pointer reads "Next unused id:
  S105" (`:423`). 100 → 101 is exactly one added row, S104.

## 2. Wave accounting — VERIFIED

### 2.1 Wave 1: 33 seats, 27 reports, claimed-missing set exact
- `spec-w1.json` enumerates **33** items (`grep -c '"name"'` → 33);
  `w1/swarm-registry.json` enumerates **33** spawn members.
- `find .ufo/waves/round-37/w1 -maxdepth 1 -name '*.md' | wc -l` → **27**.
- Per-seat loop over all 33 spec names against `w1/<Name>.md`: 27 PRESENT, 6 MISSING, and the
  missing set is exactly {CriticClaimSeparation, CriticMonitorDrift, ExecCodeViewSuite,
  ReviewC1Claim, ReviewNoHarm, SimplifyReplayAdapter} — the claimed six, no more, no less.

### 2.2 Wave 2: 33 seats, 0 reports
- `spec-w2.json` enumerates **33** items; `w2/swarm-registry.json` enumerates **33** spawn
  members; `find .ufo/waves/round-37/w2 -maxdepth 1 -name '*.md' | wc -l` → **0**
  (directory holds only `swarm-registry.json`).
- `dispatch-w1.exit` = 0 and `dispatch-w2.exit` = 0 (both dispatches returned; zero w2 reports
  is consistent with the attempt-2 provider rate wall recorded in the round context — cause not
  re-verified, absence verified directly).

## 3. Read-only rule spot-check (5 of 27 w1 reports) — NO VIOLATIONS

| report | isolation claimed | lane-write claim |
|---|---|---|
| `w1/MutatePanelManifest.md` | disposable clone `/tmp/r37-mut-panel-1792846812`; per-mutant `git reset --hard`/`git commit` executed **in the clone**; restoration evidence (pristine sha256 reproduced) | "The live lane was only ever read … no lane index, jj, `.git` or `.ufo/state` write was issued" |
| `w1/MutatePanelContent.md` | scratch clone `/tmp/tameshi-r37-mut-panel`; mutant built with `GIT_INDEX_FILE=/tmp/tameshi-r37-mut-index` plumbing; scratch deleted after restore | "No lane index/`.git`/jj/`.ufo/state` writes; lane HEAD and panel tree re-verified unchanged" |
| `w1/ExecCounterRepin.md` | independent `--no-checkout` clone `/tmp/r37-repin-exec/lane-clone` | "nothing in the live lane was touched except this report file" |
| `w1/ScribeRoundLesson.md` | audited the already-committed lesson instead of writing it | "Wrote: this report only" |
| `w1/ReviewToolPin.md` | read-only git + sha256sum | "Live lane checkout untouched" |

Sweeps over all 27 reports:
- Regex for `(i edited|i committed|i modified|i wrote to|edited the lane|…|git commit|jj commit|jj new|sq write|…)`: the only `git commit`/`commit-tree`/`reset --hard` hits are the scratch-clone/temp-index commands quoted above, plus one benign "cgit commit page" match in `ScoutBashSource.md:16`.
- Regex for redirects into the lane (`(>>?|tee …) */home/vgpnk/Projects/shokunin/tameshi-shokunin`): **no matches**.
- The only report aiming a tool at the live lane path is `ExecCalibrationCounter.md` (`measure.py --lane /home/vgpnk/…`), a read-only counting command.
- Independent ground truth: `git status --porcelain` at tip = **0 lines** — no live-lane mutation materialized anywhere in the working tree.

## 4. Observations (informational, not defects)

1. `start.stdout` is space-separated (`W04 S047 …`) while `end`/`end-attempt3` stdout are
   tab-separated — cosmetic formatting drift between the attempt-1-era start receipt and the end
   receipts; the census semantics (findings + `ok` + `EXIT_CODE=0`) are identical. No assigned
   claim depends on the formatting.
2. `start.stderr` does not exist; the receipt pair is `start.exit` + `start.stdout` only. The
   claim "start.* exit 0" is satisfied by the files present; nothing asserts a start stderr.
3. Working HEAD is detached at `ba3c35f` (normal for this jj-colocated lane), but
   `refs/heads/master` and `refs/remotes/origin/master` both point at `ba3c35f`, so "lane tip
   ba3c35f (branch master)" holds exactly.

## 5. Residual risk / verification gaps

- The census was re-run only at the live tip (clean tree == `ba3c35f`). Re-running it against the
  `d9c496b` content would require mutating the live working tree, which is forbidden for this
  seat; the 100-row state is instead pinned by the frozen row-count command at `d9c496b` (→ 100)
  and the committed `start.exit` = 0 receipt (committed at `32826f3`, bytes trusted as committed).
- Spot-check coverage was 5 of 27 reports read line-by-line, plus the mechanical redirect/phrase
  sweeps and the porcelain-clean check across all 27; the remaining 22 reports were not
  line-by-line audited for write claims.
- The cause of w2's zero reports (provider rate wall) was not independently reproduced; only the
  absence of reports under `w2/` was verified.
