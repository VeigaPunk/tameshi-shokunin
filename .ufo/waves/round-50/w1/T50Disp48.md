# T50Disp48 — C1 disposer, round-48 spot-check items R48.1 … R48.6

Seat: `T50Disp48` (C1 disposer, spot-check round 48). Item: decide, against the lane tree at base
`e3729de862f73ae080d98fcf522a7081ce16e40a`, whether what each of the six items routed by
`corpus/lessons/round-48-verifier-spotcheck.md` (lines 114-119, added by `8ca67421111fa354b47b803358391d0b07fc6db9`) asked for now
exists, and emit the ledger rows. Deliverables: `T50Disp48.rows.json` (6 rows, schema of the context), this file,
`T50Disp48.explain.stdout` (the counter probe receipt). I did not edit the lane, SCORECARD, the ledger, any counter, or the
contract; the only lane files I wrote are the three named above.

Dispositions: **4 fixed, 1 open, 1 declined**.

| id | ask (short) | status | commit |
|---|---|---|---|
| R48.1 | cold-read credit for rounds 12/13/14 restored or withdrawn; QUALITY 98 precheck on every candidate before freezing | fixed | `6db4b93132de790dc9626a66b3305161a758f1e5` |
| R48.2 | deciding script writes start/exit receipts before any output is read; receipt dirs out of the frozen path list | fixed | `14d03ea4270c6904064022b62b6faf467e5c0968` |
| R48.3 | every control scored at freeze before any deciding run; declare any `--only` preview | fixed | `14d03ea4270c6904064022b62b6faf467e5c0968` |
| R48.4 | the six carried items (`brace_depth_at`, round-47 counter survivors, S205/F7, six-leg pinned leg or class, located-name check, append-only seat-report rule) | **open** | — |
| R48.5 | append a correction to SCORECARD's "pasted byte-exact" sentence | fixed | `6db4b93132de790dc9626a66b3305161a758f1e5` |
| R48.6 | SHONEN boxes still `[~]`; promotion operator-owned | **declined** | — |

## R48.1 — cold-read credit and the precheck discipline (fixed)

The ask: restore credit for the three lapsed headings (rounds 12, 13 and 14) through a successor ledger or cold-read refresh,
or declare them withdrawn; and from then on run QUALITY 98's precheck on every candidate content revision before freezing it.
The tree carries both halves. The round-49 C1 deciding receipt prints the three headings as credited at the deciding
revision — `git show e3729de8:.ufo/evidence/round-49/after/c1.stdout | sed -n '99,101p'` gives
`SECTION ## Repeated controls and gate registry — round 12 pointers=5 floor=5 present`,
`SECTION ## Pin disposition and provenance correction — rou pointers=9 floor=9 present` and
`SECTION ## Effective expectation reconciliation — round 14 pointers=10 floor=10 present`, and line 102 closes with
`covered=64 score=8 durable_covered=64/64`. The restore itself is receipted:
`git show e3729de8:.ufo/evidence/round-49/quality/coldread-precheck-cand.stdout` (added by `5f597fa8`) is the single line
`COLDREAD_PRECHECK floor=8ca67421111f floor_credited=57 cand=master cand_credited=64 lost=0 ok`, i.e. 57 → 64 with nothing
lost, and its sibling `coldread-precheck-fc5ac743.stdout` repeats it at the same candidate. The claim sentence sits at
`git show e3729de8:SCORECARD.md | sed -n '2392p'` (`| C1 the seven lapsed cold-read sections … C1_R49_PASS=true`), added by
`6db4b93132de790dc9626a66b3305161a758f1e5` ("C1 corrections to the seven lapsed SKILL.md sections … SCORECARD
pre-registration and round-48 correction"). The second half is now mechanical rather than a promise: the round-50 deciding
script runs the precheck at the revision before either counter (`.ufo/evidence/round-50/deciding-run.sh:41`), and Criterion
99 makes "scored and committed before the deciding run" a standing rule (`corpus/QUALITY.md:1446`). Row: evidence
`c1.stdout:99-101`, `SCORECARD.md:2392`, `coldread-precheck-cand.stdout:1`, commit `6db4b931`. Status: **fixed** (both asks).

## R48.2 — deciding-script receipts and the frozen path list (fixed)

The ask: write start and exit receipts before any output is read, and drop receipt directories from the frozen path list.
`.ufo/evidence/round-49/deciding-run.sh:9` states "* every counter gets a start receipt BEFORE it runs and an exit receipt
after; no output is read before both", line 10 "* the frozen path list names code and contract only, never a receipt
directory", and the code does it: `date -u … > "$OUT/c2.start"` at :43, the counter at :44, its exit receipt at :44 and
`.end` at :45, the same quartet for C1 at :46-48, and the first read of either output (`tail -1`) only at :49-50. `FROZEN`
at :32 enumerates code and contract files and names no `$E/control` or `$E/after` directory. Round 50 keeps the shape
(`.ufo/evidence/round-50/deciding-run.sh:5-7`, start receipts at :45 and :48, `FROZEN` at :36). Row: evidence
`round-49/deciding-run.sh:9-10` and `round-50/deciding-run.sh:5-7`, commit `14d03ea4`. Status: **fixed**.

## R48.3 — controls before the deciding run, and declaration of previews (fixed, with a reading limit)

The ask has two parts. (1) Score every control at freeze, before any deciding run: gate 0 in
`.ufo/evidence/round-49/deciding-run.sh:6-8` refuses with exit 3, starting no counter, unless each pre-registered control
receipt is committed at REV in a commit that descends from `FREEZE`, and refuses a second invocation when a start receipt
already exists; the enforcement is at :24-29. Round 50 commits the control receipts at
`f87910fee11644bde9cf591391cf01c06f4a5938` ("control receipts and counter selftest receipts scored at freeze cdbf24c0
(before any seat)") and its script repeats the refusal (`.ufo/evidence/round-50/deciding-run.sh:25-27`). (2) Declare any
`--only` previews at the content revision in the contract and the report: this landed as a standing criterion rather than a
contract sentence — `corpus/QUALITY.md:1446` (Criterion 99), whose body at :1452-1453 reads "(one deciding invocation). Any
other invocation of a claim counter at the deciding revision (a partial or probe mode, a seat preview) is listed in the
report with its revision and verdict line", with the round-48 defects-2-3 lesson as its lesson line (:1457). The `--only`
mode itself no longer exists in the counters (`grep -n add_argument .ufo/evidence/round-50/c1/measure.py` →
`--lane --rev --work --explain --selftest`; `.ufo/evidence/round-50/c2/measure.py:530-535` likewise), so a preview of the
round-48 shape cannot be run silently. Reading limit, stated for the closure: `.ufo/evidence/round-50/contract.json` has no
`preview`/`--only` sentence (`grep -ni 'preview\|--only' …` → no match), so if "declare in the contract" is read as a
required contract field, the second half is carried only by Criterion 99 and gate 0. I read the tree that way (a standing,
falsifier-bearing rule plus the removal of the offending mode) and mark the row fixed. Row: evidence
`round-49/deciding-run.sh:6-7` and `corpus/QUALITY.md:1452-1453`, commit `14d03ea4`.

## R48.4 — the carried-item bundle (open)

The ask is compound: six items from SCORECARD `Planned (round 49)`, and the context makes a compound item fixed only when
every ask is met. None is met at base.

1. *Dead `brace_depth_at` helpers deleted or re-pinned.* Both are still defined:
   `git show e3729de8:tools/tally-audit-v2.py | sed -n '135p'` → `def brace_depth_at(text, offset):`;
   `git show e3729de8:tools/tally-audit-v3.py | sed -n '234p'` → the same line. `git log --oneline 8ca67421..e3729de8 -- tools/`
   lists only `9b9b2a0` (which adds `tools/pbt-staged-id.py`), so no delete and no re-pin landed.
2. *Selftest cases for the round-47 C1/C3 counter survivors.* No case names a survivor:
   `git show e3729de8:.ufo/evidence/round-49/c1/measure.py | grep -ni 'survivor\|MutC1\|T47'` prints nothing, and
   `corpus/lessons/round-49.md` has no "survivor" line (`grep -ni survivor` → no match).
3. *The S205 / F7 package candidates.* `git grep -c 1810.05286 e3729de8 -- corpus/SOURCES.md` → `0`; the package entry
   `r8-predictive-test-selection-cost.md` is still refused (`corpus/lessons/round-48-verifier-spotcheck.md:101`).
4. *A pinned-leg successor or a declared nondeterministic class for `six-leg regression ledger`.*
   `tools/mutate-and-run.sh` is untouched since routing (`git log --oneline 8ca67421..e3729de8 -- tools/mutate-and-run.sh` →
   no commit), and the standing row still reads `runs 3 stable` (`SCORECARD.md:2334`); the known FAIL member lives only in
   prose (`SCORECARD.md:2328`, `corpus/lessons/round-48.md:381-382`), not in the row's class.
5. *A located-name (entry-author) check.* `git grep -n -i 'located-name' e3729de8` returns the planned lines and the two
   spot-checks only (`SCORECARD.md:2312`, `:2380`, `corpus/lessons/round-47-verifier-spotcheck.md:107`), and nothing under
   `tools/` or `scripts/`.
6. *An append-only rule for landed seat reports.* `corpus/QUALITY.md` criterion 4 makes errata append-only (:7) and
   criterion 77 makes a seat report live in the lane repo (:916); no criterion or rule covers rewriting a landed seat report.

Row: evidence `SCORECARD.md:2367` (the carried list itself), `tools/tally-audit-v2.py:135`, `tools/tally-audit-v3.py:234`,
`SCORECARD.md:2380`. Status: **open**. `fix_plan` (in the row): not this round as a whole — the bundle is six asks, and the
cheapest single one (deleting the two unreferenced helpers and appending the two standing-row sha256 re-pins they force)
still leaves the id open on five, so the honest move is to split it into `R48.4a`-`R48.4f` next round. **L1 action needed:**
the row only scores if `R48.4` is named in the newest `**Planned (round` paragraph (see the probe section below).

## R48.5 — the "pasted byte-exact" correction (fixed)

The ask: SCORECARD's sentence should say that axis rows carry the emitted clause after lane prose; append the correction,
do not rewrite. `git show e3729de8:SCORECARD.md | sed -n '2382p'` → `### Round 48 — correction (appended in round 49)`, and
:2384 reads "The round-48 standing section says every evidence cell is the counter's `--emit` output "pasted byte-exact". That
holds for the 19 capability rows. The 3 axis rows (depth, calibration, freshness) carry lane prose followed by the emitted
`tool sha256 … runs 3 stable` clause, because the emit prints a placeholder for axis rows." It is an appended block under a
new heading (the round-48 section above it is unchanged), added by `6db4b93132de790dc9626a66b3305161a758f1e5`, whose message
names "SCORECARD pre-registration and round-48 correction". Row: evidence `SCORECARD.md:2384` and `:2382`, commit
`6db4b931`. Status: **fixed**.

## R48.6 — SHONEN promotion (declined)

The ask is an observation: all four boxes remain `[~]`, none is fully checkable by a non-author, promotion stays
operator-owned. `git show e3729de8:SHONEN.md | sed -n '5,12p'` shows the four `[~]` boxes with "lane assertion, no
independent promotion verifier" pointers, and nothing about them can be closed by a lane commit — promotion is the
operator's act. Status: **declined**, reason recorded in the row (271 characters): the boxes are lane assertions, an
independent verifier does not exist in the lane, and the lane cannot promote itself, so there is no action to land.

## Counter probe (scratch, non-deciding)

Scratch root `/fast/scratch/hyaku/tameshi-r50/T50Disp48` (removed before yielding); one `git clone -q --shared` of the lane;
`git -C "$S/lane" rev-parse --show-toplevel` printed the clone root before the one scratch commit (identity
`T50Disp48 <t50d48@scratch.invalid>`, commit `2763e4db0f53b871ed5ae76bee7e2109a86ae8f1`, adding only
`corpus/routed-defects.json`). Command:

```
python3 .ufo/evidence/round-50/c1/measure.py --lane "$S/lane" --rev HEAD --explain
```

Observed (`T50Disp48.explain.stdout`, exit 1):

```
EXPLAIN open-unplanned R48.4
C1_R50: self=ceee320c9ad8 rev=2763e4db0f53b871ed5ae76bee7e2109a86ae8f1 defects=49 rows=6 fixed=4 open=1 declined=1
  fixed_this_round=0 missing=43 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0
  key_miss=0 fixed_bad=0 open_unplanned=1 declined_bad=0 fixed_short=16 declined_over=0 this_round_short=5 total=65
  C1_R50_PASS=false
```

Every EXPLAIN line naming one of my ids, explained:

- `EXPLAIN open-unplanned R48.4` — the only one. The counter reads the last `**Planned (round` paragraph of SCORECARD.md,
  which at base and at tip is `SCORECARD.md:2410` (`**Planned (round 50):** … carried items from round 48's list.`), and that
  paragraph contains no `R4\d\.\d+` id. **The L1 must add `R48.4` to the newest Planned paragraph**; because the counter
  takes the last such paragraph, a new `**Planned (round 50), amended:**` block is only safe if it re-names every open id
  the ledger relies on, not just this one.
- The 43 `EXPLAIN missing R4x.y` lines are the other rounds' items (R40.\*, R41.\*, R42.\*, R43.\*, R44.\*, R45.\*, R46.\*,
  R47.\*, R49.\*), which my slice does not cover; expected.
- `fixed_short=16`, `this_round_short=5` likewise count rows other seats own. Note `fixed_this_round=0` is correct for my
  six rows: all four fixes are round-49 commits (`6db4b93`, `14d03ea4`), both ancestors of the round-50 base, so they cannot
  feed the `fixed_after_base_min=5` floor. The floor has to come from items fixed during round 50 by other seats.

## Limits and residual risk

- Line numbers were verified at base `e3729de8` and re-verified at tip `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`
  (`diff <(git show e3729de8:SCORECARD.md | sed -n '2360,2410p') <(git show 4afb060:SCORECARD.md | sed -n '2360,2410p')`
  → empty, so SCORECARD is still append-only there). If any wave-2 seat edits SCORECARD above line 2392, re-check 2367, 2380,
  2382, 2384 and 2392.
- Cited evidence that must stay unchanged to `REV`: `SHONEN.md:5-8`, `tools/tally-audit-v2.py:135`,
  `tools/tally-audit-v3.py:234`, `.ufo/evidence/round-49/after/c1.stdout:99-101`,
  `.ufo/evidence/round-49/quality/coldread-precheck-cand.stdout:1`, `corpus/QUALITY.md:1452-1453`,
  `.ufo/evidence/round-49/deciding-run.sh:6-10`. `.ufo/evidence/round-50/deciding-run.sh` is in the round-50 `FROZEN` list
  (:36), so it is frozen by the lane's own gate.
- The rows carry an extra `fix_plan` key on R48.4. The counter ignores unknown row keys (the probe above scored the row with
  the key present and reported no unknown-key term), but the ledger schema v1 in the contract does not name it — drop it when
  pasting if the L1 wants the literal schema.
- The counter cannot see semantic support; these are my readings of the tree, and the R48.3 contract-wording nuance above is
  the one place where a stricter reading would flip the status.

## Out of scope (untouched)

No edits to the lane checkout, `corpus/routed-defects.json`, SCORECARD, any counter, the contract, `/.ufo/evidence/round-50/`,
any fixture outside my scratch, the fleet repo, any sibling lane, or `shokuknow`; no git add/commit in the lane; no mutating jj
command; nothing read under `/home/vgpnk/.local/state/`; no mutant names quoted from `control/c2-*.stdout`. No tool was
installed or upgraded (nothing needed; pacman, uv and npx unused).

## Summary

R48.1 fixed: round-49 re-credited the round-12/13/14 headings (`c1.stdout:99-101`, `coldread-precheck-cand.stdout` 57→64) and
runs the precheck at REV before the counters. R48.2 and R48.3 fixed by `14d03ea4`: start/exit receipts around each counter,
code-only `FROZEN` list, gate 0 refusing unless the control receipts are committed at REV after `FREEZE`, plus Criterion 99.
R48.5 fixed by `6db4b93`: the "pasted byte-exact" correction is appended at `SCORECARD.md:2382-2384`. R48.6 declined:
promotion is operator-owned. R48.4 stays open — all six carried asks are still unmet at base, and the bundle needs splitting.
Probe: `fixed=4 open=1 declined=1`, `evidence_bad=0 key_miss=0 fixed_bad=0`, one EXPLAIN line of mine:
`open-unplanned R48.4`, which the L1 closes by naming `R48.4` in the newest Planned paragraph. Guardrail: `fixed_this_round=0`
from these six rows — the after-base floor must come from other seats.
