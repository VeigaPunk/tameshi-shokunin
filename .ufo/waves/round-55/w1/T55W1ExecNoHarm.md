# T55W1ExecNoHarm — round-55 no-harm monitors at base

Seat: `T55W1ExecNoHarm` (executor, leaf). Item: run the frozen round-55 no-harm monitor set at base
`0a2010acd1e92e4e332774050825e21bcfc7e079`, report every line, confirm 15 `ok` and zero `RED`, and name
(do not fix) any monitor that is `RED` at base.

## 1. Verdict

**15 lines, 15 `ok`, 0 `RED`, script exit 0.** No monitor is RED at base, so the "RED at base is a
monitor defect" branch has nothing to name.

Command actually run (verbatim):

```
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/no-harm.sh \
     /home/vgpnk/Projects/shokunin/tameshi-shokunin 0a2010acd1e92e4e332774050825e21bcfc7e079
```

with `HYAKU_SCRATCH=/fast/scratch/hyaku` (the script's own `SCR=$HYAKU_SCRATCH/tameshi-r55/no-harm`,
exported as `TMPDIR`, `rm -rf` on entry and on `trap EXIT`). Wall time 49 s.
Receipt: `T55W1ExecNoHarm-receipts/noharm-base.rev-0a2010ac.txt` (byte copy), counts in
`noharm-base.counts.txt`:

```
== wc ==            15
== ok ==            15
== RED ==            0
== any RED token ==  0
```

Every line, verbatim:

```
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-139 139 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [] ok
NOHARM registry-row-names-unchanged count=56 ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
NOHARM r53-scratch-hygiene tmp_hits=0 ok
NOHARM ledger-not-shrunk base=591 rev=591 ok
NOHARM sources-not-shrunk base=139 rev=139 ok
```

Monitor set cross-checked against the script, not just the output: the script contains 15
`echo "NOHARM ..."` sites and the 15 names it emits are exactly those (receipt
`noharm-monitor-list.txt`). Nothing was skipped silently.

### The result is a function of frozen bytes and REV content, not of the in-flight worktree

`no-harm.sh` worktree sha256 = `d93469db5a55632c...` = the sha at `631cd64` = the `freeze.json`
manifest entry, i.e. the script I ran is the frozen one (receipt `noharm-run-metadata.txt`). Monitored
content is read from `$REV` via `git show`/`git grep`; the only worktree inputs are the five measure
scripts the script invokes in place (`round-21/coldread`, `round-45/freshness`, `round-45/coverage`,
`round-46/coverage`, `round-47/coverage`), and none of them is dirty vs HEAD — the worktree's in-flight
edits (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**.py`, round-55 evidence) are not
monitor inputs (receipt `noharm-inputs-clean.txt`). So 15/15 `ok` at base is reproducible while the wave
edits land, and re-running it after the content commit measures only the content commit.

### Supplementary (declared, not the assigned run): same script at the freeze commit

`HYAKU_SCRATCH=/fast/scratch/hyaku/T55W1ExecNoHarm/privroot bash .../no-harm.sh ... 631cd6455e58dce969310b4c0466c3383d9f5108`
→ also **15 `ok`, 0 `RED`, exit 0** (`noharm-freeze.rev-631cd64.txt`). Identical lines to the base run,
so the freeze commit (evidence-only) does not move any monitor.

## 2. Axis I am judged on: freshness — measured, and at its floor

`r45-freshness` full output at base and at the freeze commit (receipt `r45-freshness.base-and-freeze.txt`):

```
DISPUTED S048
DISPUTED S093
C1_R45: self_pin=1 population=74 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 \
unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=0a2010acd1e92e4e332774050825e21bcfc7e079 C1_R45_PASS=true
```

identical at `631cd64`. The monitor's gate is **both** `fresh>=71` and `10*fresh//population>=9`
(`no-harm.sh:19`), so at base:

- `fresh=71` is **exactly the floor — margin 0**. One row losing its counted review, or one new
  `DISPUTED` row (`fresh = len(agreed - disputed)`, `round-45/freshness/measure.py:254`), makes
  `fresh=70` → `RED` (71−70 = 1 < 71). The two disputed rows today are `S048` and `S093`.
- `population=74` → `10*71//74 = 9`. The score arm holds while `population<=78` (`710//78=9`,
  `710//79=8`), i.e. **the wave may add at most 4 SOURCES rows to the population** with fresh unchanged
  (a new row only raises `population`; a row counts as fresh only once a counted non-author review
  agrees, `measure.py:199-215`).
- `SOURCES` row count is 139 at base and at the freeze commit (`registry-rows-not-below-139`,
  `sources-not-shrunk`), and the round-start census conforms: `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → **exit 0**, `ok .../corpus/SOURCES.md`
  (`sources-census-at-round-start.txt`; the W04 duplicate-url and one W01 used-by lines it prints are
  warnings, not failures).

Consequence for the L1: the round adds one `SOURCES` batch; adding ≤4 rows keeps the score arm, and
freshness must not lose a single one of the 71 woke rows.

## 3. Monitor margins at base (so the content commit does not spend them blind)

| monitor | base | gate | headroom |
|---|---|---|---|
| `coldread-floor` | `score=8 credited=64` (`sections_covered=64`, `sections_total=64`, `missing=[]`) | `score>=8 and credited>=64` | **zero** — 64 is the gate value |
| `r45-freshness` | `fresh=71`, `population=74`, `score=9` | `fresh>=71 and 10*f/p>=9` | **zero** on fresh; `population<=78` |
| `ledger-not-shrunk` | `591` at base and rev | `rev>=base` | re-key adds, never removes |
| `tools-scope` | `[]` at base | allowlist: `registry.json`, `registry-check.py`, `env-diff.py`, `bash-witness-study.py`, `context-capture.py`, `evidence-disposition.py`, `pin-disposition.py`, `repeat-control.py` (M only) | the round's three tools touch `repeat-control.py`, `context-capture.py`, `registry.json` — already inside the allowlist; a fourth tool or a non-M status is `RED` |
| `registry-row-names-unchanged` | 56 names | set equality base vs rev | rewording cells is fine, renaming a row is not |
| `r53-scratch-hygiene` | `tmp_hits=0` | `=0` | the round's code must not add `dir="/tmp"`-style literals under `tools/` |

### The `SKILL.md` edit will trip `coldread-floor` unless re-keyed — measured, not asserted

`round-18/measure.py` credits a section only when a ledger entry's `sha256` equals the sha256 of the
section's bytes (`measure.py:609-618`; a ledger entry's `skill_sha256` is *not* consulted — coverage is
section-text bound). Round item 4 edits the `## Standing rules` section, whose text becomes a new sha256
with no matching entry → the section reports `no-ledger-entry`.

Reproduced on a fixture clone of the lane at base (fixture commit `6720d907`, toplevel asserted before
commit; scratch removed afterwards), receipt `coldread-drift-fixture-demo.txt`:

```
## control: base 0a2010ac in fixture
score=8 covered=64 total=64 missing=[]
## drifted: fixture commit 6720d907 (Standing rules edited, ledger untouched)
score=6 covered=63 total=64 missing=[{'heading': '## Standing rules', 'reason': 'no-ledger-entry', 'start': 17}]
uncovered_headings= ['## Standing rules'] n= 1
```

`63 < 64` and `6 < 8` → the `coldread-floor` arm goes **RED** at the content commit until the re-key
lands. The re-key obligation is therefore exactly "one entry bound to the new `## Standing rules`
sha256 at `start=17`", and only that one section is in play (`sections_total` stays 64 while the edit
rewrites an existing section rather than adding one).

## 4. Findings (reported, not fixed)

### F1 — `.ufo/evidence/round-55/before/c2.stdout` no longer matches the freeze commit, and changed twice mid-wave

Not a no-harm monitor input (`no-harm.sh` never reads a `before/` path — grep: no match), so it does
not affect §1. It is the premise receipt the round cites for C2, so it matters to the L1.

```
-- c1.stdout   worktree bytes=2276 lines=19 mtime=2026-10-28 13:47:55   | commit bytes=2276 lines=19
-- c2.stdout   worktree bytes= 139 lines= 1 mtime=2026-10-28 13:59:44   | commit bytes=2634 lines=43
freeze commit 631cd64 committed 2026-10-28T13:37:22-03:00
```

- At 13:47:55 the worktree file read `... usable=12/13 ... total=19`; at 13:59:44 it read
  `... usable=13/13 ... total=18`. The committed copy at `631cd64` reads `usable=13/13 total=18` **plus
  the 43 per-mode `EXPLAIN` lines**; the worktree copy is the single summary line only.
- I re-ran the counter myself at base with the amended `c2/measure.py` and an empty `--work`
  (361 s): **`C2_R55: ... grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8
  skill=0/1 total=18 C2_R55_PASS=false`**, exit 1 — i.e. the `total=18` premise reproduces
  (`c2-base-rerun.explain.txt`). Diff against the committed receipt is **only** the three
  `bash-witness-study --selftest` → `bash-witness-study selftest` labels that amendment 3 declares
  (`c2-before-receipt-diff.txt`). So the 13:47 `total=19`/`usable=12/13` reading is not reproducible with
  the amended counter.
- `freeze.json` pins `contract.json`, `c1/measure.py`, `c2/measure.py`, `no-harm.sh`, `deciding-run.sh`,
  `controls.sh` — all six worktree hashes match the manifest — but it does not pin anything under
  `before/` (`freeze-provenance.txt`). The premise receipt is therefore unpinned and was rewritten after
  the freeze; any seat citing it cites a moving target.

No repair attempted: the counters, contract, freeze manifest, no-harm and deciding-run scripts are frozen
and out of my scope. If the L1 wants the per-mode evidence readable in the worktree, restoring the file
from `631cd64` is a one-command act for the integrator — not something I did.

### F2 — no RED monitor at base

Nothing to name. The `RED` branch of the item ("a RED monitor is a monitor defect") is unexercised; the
sweep that establishes it is the full 15-line output plus `grep -c RED` = 0 above.

## 5. Constraints this hands to the L1

1. `coldread-floor`: re-key `## Standing rules` (start 17) with a ledger entry bound to the new section
   sha256, or the content commit is RED (§3, measured 64→63 / 8→6).
2. `r45-freshness`: `fresh` must stay ≥ 71 and `population` ≤ 78; a third `DISPUTED` row or a lost
   counted review is RED at margin 0.
3. `tools-scope`: only `M` on the eight allowlisted paths; `registry.json` may be reworded but not
   re-rowed (56 names, set equality).
4. `r53-scratch-hygiene`: no `/tmp` literal scratch under `tools/` (`tmp_hits=0` today).
5. `ledger-not-shrunk`: 591 entries; a re-key adds, never removes.

## 6. Environment / hygiene notes

- My seat scratch root `/fast/scratch/hyaku/tameshi-r55/T55W1ExecNoHarm` disappeared mid-wave (between
  two of my own calls); `c2/measure.py` contains no `rmtree`, so a peer's cleanup of the shared
  `tameshi-r55` scratch root is the plausible cause. Nothing in the deliverables was lost — receipts
  live in this directory, not in scratch. I re-rooted later scratch at
  `/fast/scratch/hyaku/tameshi-r55-noHarmC2/` and removed it on completion.
- No lane production file was edited by this seat; every write is this report, its receipts, and scratch.
  The only git mutation was one commit inside the fixture clone (toplevel asserted equal to the fixture
  dir first); the lane got no `add`/`commit`/`checkout`/`jj`.
- No tool was installed or upgraded (nothing was needed); no `pacman` was touched.

## 7. Receipt index (`T55W1ExecNoHarm-receipts/`)

| file | what it is |
|---|---|
| `noharm-base.rev-0a2010ac.txt` | byte copy of the assigned 15-line run at base |
| `noharm-base.counts.txt` | 15 lines / 15 ok / 0 RED |
| `noharm-freeze.rev-631cd64.txt` | same script at the freeze commit (15 ok) |
| `noharm-run-metadata.txt` | command lines, script sha256 vs manifest, exit codes |
| `noharm-monitor-list.txt` | the script's 15 monitor names |
| `noharm-inputs-clean.txt` | no `before/` dependence; measure scripts clean vs HEAD |
| `r45-freshness.base-and-freeze.txt` | full freshness output, both revisions |
| `coldread-at-base.json` | full coldread measure output at base |
| `coldread-floor-summary.txt` | 64/64 covered, score 8, depth 10 |
| `coldread-drift-fixture-demo.txt` | measured 64→63 / 8→6 on an un-re-keyed drift |
| `c2-base-rerun.explain.txt` | my 43-line rerun of the C2 counter at base (total=18) |
| `c2-before-receipt-diff.txt` | committed vs rerun vs worktree `before/c2.stdout` |
| `freeze-provenance.txt` | manifest hashes vs worktree vs `631cd64`; `before/` unpinned |
| `sources-census-at-round-start.txt` | `sources-census.sh validate ... tameshi` exit 0 |
