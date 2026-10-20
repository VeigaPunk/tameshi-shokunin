# LessonCarryCheck-2 — round-16 routed defects and jj items at `eb7838b`

Seat: LessonCarryCheck-2 · 2026-10-20 · read rev `eb7838b16490ca7ba17ea3242ade76a61f744af2`
(2026-10-20 12:59:15 -0300; parent `2a22ade`, 12:54:21).

Method: fleet-mirror clone of the lane at the read rev, all tools executed from
the clone, never against the live lane root. Live lane was read only (tree,
`.jj/repo/config-id`, `~/.config/jj/repos/...`); no jj/git write in the lane.
No tools installed or upgraded.

```
W=$(mktemp -d /tmp/tameshi-r17w2-LessonCarryCheck-XXXXXX)
mkdir $W/fleet; for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" $W/fleet/; done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2
# C=$W/fleet/tameshi-shokunin ; every command below ran with cwd=$C
```

## Round-16 routed defects (`corpus/lessons/round-16-verifier-spotcheck.md` §6)

| # | Defect | Status at `eb7838b` |
|---|---|---|
| 1 | R16-OP1 operability re-pin | **fixed** — live-tree green 0 clean, red-before reproduced at `98bea7d` (2), round-17 before-manifest 1, historical bytes immutable (`2a22ade`/`eb7838b`) |
| 2 | R16-C2a stale recipe | **fixed (text) / open (ledger half)** — SKILL.md:1581-1586 marked historical with a replay that executes (1 then 0) in `git archive 28aeef4`; the required fresh-seat ledger entry at the new section sha is absent at the read rev (no round-17 ledger; wave-2 reads are untracked/in flight) |
| 3 | R16-C2b sha-only credit | **fixed (machinery) / open (ledger at read rev)** — `measure.py`/`trace-inputs.py`/`assemble.py` and the input-keyed rule are committed and selftest green; red-before on the round-14 bucket is real (`input-drift:tools/mutate-and-run.sh` at `09ee1d0`); `measure.py --rev eb7838b` still returns `box3_full_page:false`, calibration 6 because `eb7838b:.ufo/evidence/round-17/coldread/ledger.json` does not exist |
| 4 | R16-C2c box-3 overclaim | **fixed** — `SHONEN.md:11` correction appended, diff is `1 insertion(+), 0 deletions(-)` vs `98bea7d`; no rewrite |
| 5 | R16-EV1 stale receipt | **fixed** — dated correction appended to `.ufo/evidence/round-16/round-gate/runner-sha256.txt` (diff `4 insertions(+), 0 deletions(-)`, original line 1 intact); the two runner shas the correction names verify |
| 6 | R16-MON1 monitor scope | **fixed** — `tools/registry.json` (schema `tameshi-entry-registry-v1`, 29 rows) + `tools/registry-check.py`; full replay at `eb7838b` is `held=28/28 superseded=1`, exit 0; at `98bea7d` with the same registry it fails (`exit 1`), which is the capability loss it was built to catch |

### 1. R16-OP1 — green/red/before and immutability

```
$ python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-17/dispositions.json          # EXIT=0
EVIDENCE_DISPOSITION: clean exit=0 expected=12 effective=11 superseded=1 passed=11 failed=0 findings=0
HISTORICAL tools/mutate-and-run.sh  rev=4acc607dfd79f19d508bd50cdd06b77269fccd1d sha256=75ed934d…
HISTORICAL tools/pin-disposition.py rev=4acc607dfd79f19d508bd50cdd06b77269fccd1d sha256=29725397…

$ python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-17/dispositions-before.json   # EXIT=1
EVIDENCE_DISPOSITION: failed exit=1 expected=12 effective=12 superseded=0 passed=11 failed=1 findings=1
# (FINDING expected_contains_missing expectation=producer_before)
```

Red-before reproduced independently from a `98bea7d` clone (fresh clone, same tool at that rev):

```
$ python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-14/dispositions.json          # EXIT=2
EVIDENCE_DISPOSITION: could_not_evaluate exit=2 id=expected_input_digest_mismatch
  observed 0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa
  expects  75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
```

Shipped receipt `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt` carries the
same `expected_input_digest_mismatch`/exit 2. The v2 manifest waives only the
two moved instruments, pinned at `4acc607` (`.ufo/evidence/round-17/dispositions.json`:
`supersedes=.ufo/evidence/round-14/dispositions.json`, `historical_inputs` =
`tools/mutate-and-run.sh` + `tools/pin-disposition.py`; `rows` 12). Guard code:
`tools/evidence-disposition.py:581` (`validate_historical_inputs`), `:1461`.

Immutability: `git diff --stat 98bea7d..eb7838b -- .ufo/evidence/round-13 .ufo/evidence/round-14`
is empty; across `.ufo/evidence/round-16` the only change is the +4-line append
in `runner-sha256.txt`. The red-before/green receipts are new files, not edits.

### 2. R16-C2a — historical recipe and its replay

`SKILL.md:1581-1586` now says the two round-14 manifests return 2 at `--root .`
and gives the archived replay. Executed exactly as written:

```
$ X=$(mktemp -d); git archive 28aeef4 | tar -x -C $X; cd $X
$ sha256sum tools/mutate-and-run.sh   # 75ed934d… (the runner the recipe names)
$ python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-14/dispositions-before.json --json   # EXIT=1
$ python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-14/dispositions.json --json          # EXIT=0
```

Both outcomes match the text (`→ 1`, failing `producer_before`; `→ 0`). In a
checkout at the read rev both round-14 manifests return 2, as the text says.

Gap: the routed item also requires “re-read the bucket with a fresh seat and
append a ledger entry at the new section sha”. At `eb7838b` the round-14
section (`start 1563`) hashes to
`c121412bd8cf27b0f93b731ae0b43033870c429a5ebe14de77b234a2ada236a7`, and the
round-16 ledger's old entry (`e8720037…`, no `inputs` map) is the only entry
for that bucket. `eb7838b:.ufo/evidence/round-17/coldread/` contains `assemble.py`,
`bucket-commands.json`, `trace-inputs.py` only — no `ledger.json`. Wave-2
receipts exist in the live tree (`.../traces/CR55/…`, `CR57/3-historical-r14-recipe.json`,
551 receipts at observation time) but are untracked and not readable at the rev.
So the text half is closed; the ledger-entry half is open at this rev.

### 3. R16-C2b — input-keyed credit machinery and its red-before

Committed at `2a22ade`/`eb7838b`: `.ufo/evidence/round-17/measure.py` (1499 lines;
credit rule `:33-72`; `coldread()` `:492`), `coldread/trace-inputs.py` (966 lines),
`coldread/assemble.py` (1637 lines). Selftests, run from the clone:

```
$ python3 .ufo/evidence/round-17/measure.py --selftest                  # EXIT=0
MEASURE_SELFTEST: 89/89 pass
$ python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest    # EXIT=0
SELFTEST: 27/27
$ python3 .ufo/evidence/round-17/coldread/assemble.py --selftest        # EXIT=0
SELFTEST: all checks passed
```

Red-before on the round-14 bucket is real and specific (committed receipts):

- `.ufo/evidence/round-17/redbefore/measure-e69b488.json`: section 1563
  `credited:true`, `inputs_overlay_merged:1`, `overrides_used:true`
  (the overlay is `.ufo/evidence/round-17/redbefore/legacy-r14-inputs.json`,
  19 inputs incl. `tools/mutate-and-run.sh: 75ed934d…`).
- `.ufo/evidence/round-17/redbefore/measure-09ee1d0.json` and `…-98bea7d.json`:
  section 1563 `credited:false`, `reason:"input-drift:tools/mutate-and-run.sh"`;
  `digest-diff.txt:19` shows the single drift (`75ed934d…` → `0673d2e5…`).
  These are override/legacy demonstrations, which Gate G6 says are not citable
  scores — consistent with the tool's split (`trace_gate:"legacy"` when overridden).

Open at the read rev: the strict, no-override measurement, which is the form
the page says a cited number must use (`SKILL.md:1889-1891`, `1901`):

```
$ python3 .ufo/evidence/round-17/measure.py --rev eb7838b16490ca7ba17ea3242ade76a61f744af2
# EXIT=0
"coldread": {"box3_full_page": false, "ledger_present": false,
             "sections_covered": 0, "sections_total": 58,
             "reasons": {"no-ledger": 58}}
"calibration_restraint_score": 6
"depth_score": 7
"overrides_used": false
```

Wave 1's own untracked `.ufo/evidence/round-17/c1-measure-eb7838b.json` agrees
(`box3 false`, `calib 6`, `ledger false`, `no-ledger` ×58), so this is not a
tool-version mismatch. The fresh re-read cannot be earned by `--rev eb7838b` at
all: the ledger would have to be committed into that same commit. A descendant
landing can satisfy it; the landing rev named in the wave claim cannot.

### 4. R16-C2c — box-3 correction

`SHONEN.md:11` appends the round-17 correction (the round-14 bucket was
sha-only, its runner moved, its recipe exited 2), pointing at
`.ufo/evidence/round-17/coldread/ledger.json`. `git diff 98bea7d..eb7838b -- SHONEN.md`
= `1 insertion(+), 0 deletions(-)`. Box 3 remains `[~]` (lane assertion), which
is what the item asked for; no `[x]` is claimed.

### 5. R16-EV1 — receipt correction

`.ufo/evidence/round-16/round-gate/runner-sha256.txt:1` is still
`89722ddb… tools/mutate-and-run.sh`; lines 2-5 are the dated correction.
Diff vs `98bea7d`: `4 insertions(+), 0 deletions(-)`. Verified the correction's
content directly:

```
$ for r in 05a2247 09ee1d0 017a2b0 98bea7d 4acc607; do
    git show $r:tools/mutate-and-run.sh | sha256sum; done
05a2247 0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa
09ee1d0 0673d2e5…      017a2b0 0673d2e5…      98bea7d 0673d2e5…
4acc607 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
```

The rev list in the correction is true; the original line was not rewritten.

### 6. R16-MON1 — registered-entry monitor

`tools/registry.json:197,224,250,267` registers the live re-pin row
(`evidence-disposition-round17`, argv includes `--root .`), its before-row,
and the superseded round-14 row (`superseded_by: evidence-disposition-round17`).
Replayed in the clone:

```
$ python3 tools/registry-check.py --rev eb7838b16490ca7ba17ea3242ade76a61f744af2 \
      --registry tools/registry.json --tag baseline                # EXIT=0
ROW evidence-disposition-round17 expect=0 got=0 held
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
REGISTRY_CHECK: held=23/23 superseded=1

$ # same call, no --tag (every registered row)
REGISTRY_CHECK: held=28/28 superseded=1                            # EXIT=0
```

Grading the harm the monitor missed, with the round-17 registry against
`98bea7d` (JSON rerun): `exit 1`, `held=22/23 superseded=1`; the two differing
rows are `evidence-disposition-round17` and `evidence-disposition-round14-superseded`,
both `got=2` (could-not-evaluate) against the recorded 0. The old round-14
command is reported as `superseded`, not silently dropped, and still runs
(`got=2`). This is exactly the “disposition capability differs at 98bea7d”
claim; it holds.

## jj items (`JjAuditTameshi.md` §5; `JjTrialTameshi.md` Recommendations)

| Item | Status at `eb7838b` |
|---|---|
| §5 R1 repo-identity guard in `mutate-and-run.sh` | **fixed** — `tools/mutate-and-run.sh:1042-1054` (`git rev-parse --show-toplevel` compared to `realpath "$repo"`, SETUP `repo_identity_mismatch`); selftest arms `:1707-1721`; `--selftest` 95/95 pass |
| §5 R2 HEAD-vs-branch (`pin-disposition.py:317`, SKILL.md:1033) | **fixed** — `detect_branch()` `tools/pin-disposition.py:324-362`, tip read `:379-426` (`refs/heads/<branch>^{commit}`, `branch`, `head_differs_from_branch`); selftest case `detached-head-uses-branch-tip` `:1299` passes, `SELFTEST: PASS (19/19)`; SKILL.md:1027-1035 now reads the branch tip |
| §5 R3 jj-lane helper `commit` lacks fail-closed auto-track check | **declined** in Gate G9 (`corpus/lessons/round-17.md:26`, not lane scope). Lane half verified fixed: `.jj/repo/config-id` = `900fa08b5e426ae84a97`, and `~/.config/jj/repos/900fa…/config.toml` (mtime 12:07) carries `[snapshot] auto-track = "none()"`. The helper half was still open at the landing time [INFERENCE: `git blame` puts the check in fleet commit `14df5b9`, 13:05, after `eb7838b` 12:59]; that commit now checks `snapshot.auto-track = "none()"` in `cmd_commit` (`scripts/hyaku/jj-lane.sh:518-521`) |
| §5 fourth, inert: hooks/attribute-filter bypass and index reset | **holds (still inert)** — no `.gitattributes` anywhere at the rev; `.git/hooks` contains only `*.sample`; no lane tool executes jj (`jj ` occurs only in `tools/pin-disposition.py` comments), so no lane call site can be affected |
| Rec 1 keep `snapshot.auto-track="none()"` | **holds** — config `900fa…` carries it (external state read; not in the commit) |
| Rec 2 add `.gitignore` `.ufo/state/` + `.ufo/watchdog.log` | **fixed** — `.gitignore:2-3`, added in `2a22ade` |
| Rec 3 lane tooling needs no changes | **not adopted as stated** — true for colocation transparency, but JjAudit §5 R1/R2 required and got tool changes at `2a22ade` (`tools/mutate-and-run.sh` +146/-19, `tools/pin-disposition.py` +158/-16); the blanket “no changes” is superseded by the audit |
| Rec 4 cite the helper's pushed hash, never `committed` | **adopted** — `corpus/knowledge/operator-runbook.md:514` (ER-R3: “cited hashes are the helper's landed/pushed hash”) and SKILL.md:1035 drift reading / `:1843` branch-tip read |
| Rec 5 no per-lane jj config beyond `init` | **holds** — the live repo config contains exactly the init triad (`trunk()` alias, `snapshot.auto-track`, `user.name/email`); nothing extra |

Notes on verification limits: the jj repo-config hash for the live path is not
reproducible by the common hash variants I tried, so I read the lane's own
`.jj/repo/config-id` (mode 600, untracked) and the addressed file rather than
running jj in the lane. `JjAuditTameshi.md` §5's own residual says the audit
did not execute selftests; I ran them here in a clone.

## Claims under attack

**C1 calibration — does not hold at `eb7838b` as stated.** The strict command
`python3 .ufo/evidence/round-17/measure.py --rev eb7838b…` returns
`box3_full_page:false` and `calibration_restraint_score:6` (not 8): the
round-17 ledger is not in the tree (`git ls-tree eb7838b .ufo/evidence/round-17/coldread/`
lists only the three tools). Wave 1's own untracked measurement says the same.
The machinery, selftests, and red-before are real; the “true / 6→8” result is
not reachable at this rev and would require a descendant commit carrying the
assembled ledger (or an amend, which would break the cited landing hash).

**C2 operability — holds at `eb7838b`.** Baseline `held=23/23 superseded=1`,
exit 0; full registry `held=28/28 superseded=1`, exit 0; the round-14 command
is reported superseded and still runs (`got=2`); at `98bea7d` the same
round-17 registry gives `exit 1` with both disposition rows at `got=2`. One
transient observation, not reproduced and not used as evidence: the first
`98bea7d` full run returned 21 `unavailable` rows in 1.6 s (Popen OSError
after `repeat-control-selftest`); the JSON rerun ran normally (132 s,
22/23 + 1 superseded).

## Incidental findings

- **Page exit map for `measure.py` is wrong for the missing-default-ledger
  case.** `SKILL.md:1901` says `2 rev, blob or ledger missing`; measured:
  `measure.py --rev eb7838b…` with the default ledger absent exits **0** and
  reports `no-ledger` (strict mode), while an explicit
  `--ledger-file /tmp/nonexistent` exits **2** `ledger-file-unreadable`.
  The page's command form (`--rev REV`) implies the former. This is how a
  missing ledger can silently yield a valid-looking 6 instead of a
  could-not-evaluate, which is precisely the failure mode C1 ran into.
- **The round-16 ledger has no `inputs` map for the round-14 bucket**
  (`eb7838b:.ufo/evidence/round-16/coldread/ledger.json`, entry start 1563:
  sha `e8720037…`, no `inputs`), confirming why the red-before needs the
  `legacy-r14-inputs.json` overlay and why the old credit was sha-only.
- **`evidence-disposition` v2 waiver scope matches its reason text**: only the
  two moved `tools/` paths are waived, both at `4acc607`, and no evidence path
  is waived; the manifest's own `historical_inputs` reasons name the round-16
  and round-17 moves.

## Verdict

At `eb7838b` the six R16 defects have their landing-side fixes (OP1 green/red/
before + immutable bytes; C2a text + executable archive recipe; C2b machinery +
real input-drift red-before; C2c/EV1 append-only corrections; MON1 28/28),
but the fresh-seat cold-read ledger required by C2a/C2b is not in the rev, so
C1's `box3_full_page true / 6→8` is false at the landing commit (measured
false/no-ledger, calib 6) while C2's operability claim holds (23/23 baseline,
28/28 full, superseded=1; `98bea7d` differs at exit 2); all three jj audit
risks are fixed (R1/R2 in-lane, selftests 95/95 and 19/19) or declined for lane
scope with the lane's config verified `none()` and the helper half now fixed
fleet-side at `14df5b9` — verdict: **C2 holds; C1 falls at this rev; two jj
risks fixed, R3 correctly declined and externally closed after landing.**
