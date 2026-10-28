# T56W1ExecNoHarm — no-harm monitor liveness (round 56, wave 1)

Item: dry-run `.ufo/evidence/round-56/no-harm.sh` at the freeze `c3e2ca9f`, report every line, then prove
monitors can turn RED by mutating a scratch clone: (a) drop one recorded ledger case, (b) shrink SOURCES.md
by one row, (c) add a `/tmp` literal under `tools/`. Flag any monitor that cannot turn RED by construction.

Seat: leaf executor, no lane production file and no frozen instrument touched. Scratch clone only.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (HEAD == freeze at run time, unmodified by this seat)
- Freeze / instrument revision: `c3e2ca9f020776b3d66c7af854fb82c834674fcf`
- Base: `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`
- Scratch: `$HYAKU_SCRATCH=/fast/scratch/hyaku`, `S=/fast/scratch/hyaku/tameshi-r56/T56W1ExecNoHarm`
- Receipts: `.ufo/waves/round-56/w1/T56W1ExecNoHarm-receipts/` (14 `noharm-*.stdout`, 0 bytes on every `.stderr`)
- Machine-readable matrix: `.ufo/waves/round-56/w1/T56W1ExecNoHarm.json` (derived from the receipts, not hand-typed)
- Tools installed: none (nothing was needed; no `pacman`, no `uv`, no `npx`).

## 0. Commands

```
# freeze dry run
bash .ufo/evidence/round-56/no-harm.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin \
     c3e2ca9f020776b3d66c7af854fb82c834674fcf            # -> noharm-freeze.stdout, 33.6 s, exit 0

# clone (never the lane)
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/clone
git -C $S/clone checkout --detach c3e2ca9f020776b3d66c7af854fb82c834674fcf
git -C $S/clone rev-parse --show-toplevel     # asserted == $S/clone before every commit

# one commit per mutant on its own branch from the freeze, then
HYAKU_SCRATCH=$S/h-mut-<x> bash .ufo/evidence/round-56/no-harm.sh $S/clone <mutant-rev>
```

`HYAKU_SCRATCH` was re-pointed per run (`$S/h-<name>`), so no two concurrent runs share
`tameshi-r56/no-harm` and none of them touches another seat's scratch.

## 1. Freeze integrity — the instrument I ran is the frozen one

`sha256sum` of all ten paths in `freeze.json` reproduces `freeze.json` exactly (`freeze-and-lane.txt`),
including `no-harm.sh = a13ba1a8433752c8e2d928c129dc4889181f34caa917099d4aaa96ec1d33e3b4`.
The lane was not modified: `git status --porcelain` at run time shows only untracked round-56 evidence
and wave directories owned by other seats.

## 2. Dry run at the freeze — every line

15 lines, 14 `ok`, 1 `RED`; exit status 0 (`noharm-freeze.stdout`, stderr empty):

| # | monitor | observed at `c3e2ca9f` | status | expected before the re-key? |
|---|---|---|---|---|
| 1 | commandD | `recorded_cases=10 depth_score=10` | ok | yes — 10 recorded cases, depth 10 |
| 2 | **coldread-floor** | `score=6 credited=46` | **RED** | **yes — the C1 obligation**: the 18 headings are unbound at the freeze, so credited=46 < 64 and score=6 < 8 |
| 3 | r45-freshness | `population=74 fresh=71 score=9` | ok | yes, but exactly at the floor (§4 F3) |
| 4 | r45-coverage | `rows=2 entries=2 C2_R45_PASS=true` | ok | yes |
| 5 | S160-count | `1` | ok | yes |
| 6 | registry-rows-not-below-140 | `140` | ok | yes |
| 7 | r46-coverage | `rows=3 entries=3 C3_R46_PASS=true` | ok | yes |
| 8 | r47-coverage | `rows=3 entries=3 C3_R47_PASS=true` | ok | yes |
| 9 | tools-scope | `[A:tools/receipt-revision-gate.py ]` | ok | yes — the round's one new tool is the one admitted addition |
| 10 | registry-rows-not-shrunk | `base=56 rev=56` | ok | yes |
| 11 | r49-generator-capability | `PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31` | ok | yes — matches the frozen string byte for byte |
| 12 | r50-shrinker-selftest | `SHRINK_SELFTEST: cases=14 failed=0` | ok | yes |
| 13 | r53-scratch-hygiene | `tmp_hits=0` | ok | yes, but the predicate has **zero hits at the freeze** (§4 F1) |
| 14 | ledger-not-shrunk | `base=591 rev=591` | ok | yes |
| 15 | sources-not-shrunk | `base=140 rev=140` | ok | yes |

The single RED is the round's own claim, not a regression: `.ufo/evidence/round-56/before/c1.stdout`
records the same base state (`cand_credited=46 lost=18 RED`) and `c1/lost-headings-at-base.json` names the
18 headings. The monitor's predicate (`score>=8 and credited>=64`) is the C1 target's own floor, so
`coldread-floor` must stay RED until the re-key lands in C0 and the deciding REV contains it.

## 3. Liveness — 15 of 15 monitors were made to turn RED

Each mutant is one commit on its own branch from the freeze, in `$S/clone`. `mut-a/b/c` are the item's
three required mutations; `mut-d`…`mut-m` exist to cover the remaining monitors and to size the one
bypass found.

| monitor | mutation | observed at the mutant | receipt |
|---|---|---|---|
| commandD | **mut-a** drop one recorded case (`tools/mutate-and-run.sh`, `#   bash-drift-pins …` line) | `recorded_cases=9 depth_score=9 RED` | `noharm-mut-a.stdout` |
| sources-not-shrunk | **mut-b** drop one SOURCES.md row (S280) | `base=140 rev=139 RED` | `noharm-mut-b.stdout` |
| registry-rows-not-below-140 | **mut-b** (same) | `139 RED` | `noharm-mut-b.stdout` |
| r53-scratch-hygiene | **mut-c** add `def resolve_scratch(dir = "/tmp"):` to `tools/registry-check.py` | `tmp_hits=1 RED` | `noharm-mut-c.stdout` |
| r53-scratch-hygiene | **mut-d** three `/tmp` spellings the regex misses | `tmp_hits=0 ok` — **evasion** (§4 F1) | `noharm-mut-d.stdout` |
| ledger-not-shrunk | **mut-e** drop one round-21 cold-read ledger entry (591→590) | `base=591 rev=590 RED` | `noharm-mut-e.stdout` |
| S160-count | **mut-f** duplicate the S160 row verbatim (141 rows, population unchanged) | `2 RED` | `noharm-mut-f.stdout` |
| registry-rows-not-shrunk | **mut-g** drop one `tools/registry.json` row (56→55) | `base=56 rev=55 RED` | `noharm-mut-g.stdout` |
| r45-freshness | **mut-h** drop one round-45 review (`reviews.json`, 73→72) | `population=74 fresh=70 score=9 RED` | `noharm-mut-h.stdout` |
| r49-generator-capability | **mut-i** make `tools/staged-id-guard.py` admit everything (real regression) | `cases=1 violations=1 counterexample=0 … RED` | `noharm-mut-i.stdout` |
| r50-shrinker-selftest | **mut-j** `tools/shrink-case.py` reports `runs+1` (dishonest count) | `SHRINK_SELFTEST: cases=14 failed=1 RED` | `noharm-mut-j.stdout` |
| r45-coverage | **mut-k** S256 status `mined`→`queued` | `rows=1 entries=1 C2_R45_PASS=false RED` | `noharm-mut-k.stdout` |
| r46-coverage | **mut-l** S258 status `mined`→`queued` | `rows=2 entries=2 C3_R46_PASS=false RED` | `noharm-mut-l.stdout` |
| r47-coverage | **mut-m** S261 status `mined`→`queued` | `rows=2 entries=2 C3_R47_PASS=false RED` | `noharm-mut-m.stdout` |
| tools-scope | **mut-a** (`M:tools/mutate-and-run.sh`), **mut-i** (`M:tools/staged-id-guard.py`), **mut-j** (`M:tools/shrink-case.py`) | `[M:… ] RED` | those three receipts |
| coldread-floor | already RED at the freeze; it is *sensitive*, not stuck: `credited` 46→29 under mut-a and 46→45 under mut-e | `score=6 credited=29 RED` / `credited=45 RED` | `noharm-mut-a.stdout`, `noharm-mut-e.stdout` |

**No monitor is unfireable by construction.** Each of the 15 was observed RED under a mutation, except
`coldread-floor`, which is RED at the freeze itself and whose observed `credited` value moves under two
independent mutations (so it is neither stuck-ok nor stuck-RED by construction — it is measuring).

Mutation inventory (branch, short rev, one-line diffstat): `mutants.txt`.
Freeze dry-run and every mutant run printed exactly 15 `NOHARM` lines; every `.stderr` is empty.

## 4. Findings

### F1 — `r53-scratch-hygiene` is live but evadable, and its predicate has zero hits at the freeze
The predicate is `git grep -c -E "dir\s*=\s*[\"']/tmp"`. At `c3e2ca9f` it matches **0** of the **60**
lines under `tools/` that contain `/tmp` (`r53-sweep.txt`): the existing literals are
`${TMPDIR:-/tmp}` fallbacks, sandbox paths (`/tmp/w`, `/tmp/w8-…`), doc strings and registry prose.
So the monitor is a forward guard, not an invariant over the current tree. Three realistic spellings
pass it silently (`mut-d`, `tmp_hits=0 ok`):

```python
SCRATCH_ROOT = "/tmp"
FALLBACK = os.environ.get("TMPDIR", "/tmp")
PATH_ROOT = Path("/tmp")
```

It is not unfireable — `mut-c` fires it (`tmp_hits=1 RED`) — but a tool that hardcodes `/tmp` in any
spelling other than `dir = "/tmp"` is invisible to it. **Good news for this round:** the one new tool,
`tools/receipt-revision-gate.py`, contains no `/tmp` literal at all (`r53-sweep.txt`, last block).

### F2 — the script's exit status is 0 with RED lines present
Observed on every run (`EXIT_mut-a=0 … EXIT_mut-m=0`, and the freeze run with `coldread-floor … RED`).
`no-harm.sh` ends on an `echo`, so RED never propagates to `$?`. `deciding-run.sh` compensates correctly:
`grep -q RED "$OUT/no-harm.stdout" && rc=1` plus `grep -c '^NOHARM .* ok$' = 15`. Any other caller that
checks only the exit status would read a RED sweep as a pass. Not a defect in the round's gate, but the
monitor's contract should say "parse the lines, never the exit code".

### F3 — `r45-freshness` has zero slack and its population is capped at S160
`fresh=71` against a floor of `fresh>=71`; `score=9` against `>=9`. One verified row losing its review
flips it (`mut-h`: `fresh=70 RED`) even though the underlying round-45 counter still reads
`C1_R45_PASS=true` (its own `TARGET=50`). Headroom is only on the score side:
`10*71//p >= 9` holds up to `p=78` (`freshness-headroom.txt`).
Population is `status == mined and id <= MAX_ID(160) and url` (`measure.py:95-97,60-61`), so the C0
content's new source row (S281+) **cannot** move this monitor; an edit to any S001–S160 row's status,
URL or presence can.

### F4 — `coldread-floor` is also a pinned-input drift monitor
Deleting one line from `tools/mutate-and-run.sh` (`mut-a`) dropped `credited` 46→29 while the score
stayed 6: 372 ledger entries pin that file, and the credit algorithm un-credits an entry whose pinned
input digest moved. Consequence for C1: the 18 re-keyed entries must pin the input digests **as they are
at C0/REV**; any late edit to a pinned input silently costs credit even though nothing was un-read.

### F5 — the monitors read their *code* from the working tree, their *data* from REV
`no-harm.sh` does `cd "$LANE"` and then `python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV"`;
only `git show "$REV:…"` calls (commandD, S160-count, registry rows, ledger, SOURCES, pbt/shrink blobs)
are REV-bound. A dirty working tree would let uncommitted counter bytes score a committed revision.
`deciding-run.sh` closes this with `clean-tree-before` (`DECIDING_REFUSED dirty-tree`), so the gate is
sound — but no-harm.sh alone is not hermetic, and the deciding run must keep that check ahead of it.

### F6 — three coverage monitors and `r49` are exact-string comparisons
`r45/r46/r47-coverage` require the literal token strings `rows=N entries=N Cx_R4y_PASS=true`, and
`r49-generator-capability` requires the full class-count string byte for byte. All fire on real
regressions (`mut-k/l/m`, and `mut-i` where the fuzz caught a weakened guard on case 1 with
`violations=1`), so they are live — but they also RED on a legitimate improvement (a new PBT class, a
new row) that changes the string. Treat a RED here as "the value moved", then read the observed value.

## 5. Collateral map (attribution aid for the deciding run)

Every mutant run carried the baseline `coldread-floor … RED`, as expected. Beyond the target monitor,
these also fired and are *consequences of the same mutation*, not independent findings:

- `mut-a`: `tools-scope` (`M:tools/mutate-and-run.sh` not admitted) and `coldread-floor credited=29`.
- `mut-i`, `mut-j`: `tools-scope` (the mutated tool is not on the allowlist).
- `mut-b`: both SOURCES monitors fire together by design.
- `mut-e`: the ledger reformat in that commit also moved `coldread-floor credited` 46→45 (one entry is
  one credit).

## 6. What this means for C0 and the deciding REV

1. The deciding run needs **15 `ok` lines and no RED**. At C0/REV the only thing that can keep
   `coldread-floor` RED is an incomplete re-key; it is the C1 verdict in miniature.
2. The C2 content is safe for no-harm as specified: a new `corpus/knowledge/*.md`, a QUALITY criterion, a
   SKILL `## Standing rules` line and a `tools/registry.json` cell touch nothing the monitors measure
   (`M:tools/registry.json` is admitted by `tools-scope`; `registry-rows-not-shrunk` only forbids shrinking).
3. The C2 content's SOURCES row must not be a re-key of an S001–S160 row: that is the only edit path
   into `r45-freshness` (F3). S281+ is inert to it.
4. The re-key must pin inputs at the final C0 bytes (F4), and no seat may leave the tree dirty when the
   deciding run starts (F5).
5. If the L1 wants the `r53` bypass closed, the fix belongs in a later round's instrument (this one is
   frozen): widen the predicate to `/tmp` occurrences that are not `${TMPDIR:-/tmp}` fallbacks, or assert
   `tmp_hits` equals a declared census of the tree. Proposed as a routed defect, not applied.

## 7. Not done (bounds respected)

- No lane production file, no `.ufo/evidence/round-56/**` instrument, no fleet-root tracked file touched.
- No mutating git command anywhere except inside `$S/clone` (toplevel asserted before each commit);
  the lane's HEAD is still `c3e2ca9f` and its tracked tree is clean.
- No subagent dispatch; no `agent://all` message.
- Scratch `$S` was left in place so the receipts can be re-derived; it holds only the clone, per-mutant
  `HYAKU_SCRATCH` dirs and `mut-revs.txt`.

## Receipts index (`.ufo/waves/round-56/w1/T56W1ExecNoHarm-receipts/`)

| file | content |
|---|---|
| `noharm-freeze.stdout` / `.stderr` | the 15-line dry run at `c3e2ca9f` (stderr empty) |
| `noharm-mut-a.stdout` … `noharm-mut-m.stdout` | 13 mutant runs, 15 lines each |
| `freeze-and-lane.txt` | 10/10 freeze sha256 + lane HEAD + lane status |
| `mutants.txt` | clone path, toplevel assertion, 13 mutant commits with diffstat |
| `r53-sweep.txt` | 0 regex hits vs 60 `/tmp` lines under `tools/`, the unmatched lines, the new tool's clean scan |
| `r53-evasion.txt` | mut-d bytes and the no-match grep |
| `freshness-headroom.txt` | `fresh=71` against population 74…81 |
