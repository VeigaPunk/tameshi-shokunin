# T55W2RevNoHarm — no-harm monitors at C0, and the seven tools' self-tests

Seat: T55W2RevNoHarm (reviewer, axis **freshness**, milestone "no-harm at C0").
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
Base `0a2010acd1e92e4e332774050825e21bcfc7e079`; freeze `e2979f277138da503af27b263b783f626f109be4`;
content commit C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.
All figures below are from my own runs at 2026-10-28 14:34–14:44, not from a peer report.
Receipts: `.ufo/waves/round-55/w2/T55W2RevNoHarm-receipts/` (this directory) and the runnable
probe script `monitor-probes.sh` in it.

## 1. The invocation and every line it printed

```
$ bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/no-harm.sh \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=6 credited=46 RED
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-139 140 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [M:tools/context-capture.py M:tools/registry-check.py M:tools/registry.json M:tools/repeat-control.py ] ok
NOHARM registry-row-names-unchanged count=56 ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
NOHARM r53-scratch-hygiene tmp_hits=0 ok
NOHARM ledger-not-shrunk base=591 rev=591 ok
NOHARM sources-not-shrunk base=139 rev=140 ok
EXIT=0
```

Receipt: `no-harm-at-c0.stdout`. Run twice (14:34 and 14:41) with byte-identical output — the RED is
reproducible, not a flake.

**Count: 15 lines, 14 `ok`, 1 `RED`, script exit `0`.** The item's premise ("confirm 15 ok, zero RED")
is therefore **falsified**: `coldread-floor` is RED at C0. The script's own header is honest that each
line carries its own verdict; but see §5.3 — the *script* exit code is 0 with a RED line.

## 2. What each monitor means, in one clause

| Monitor | Observed | Meaning in one clause |
|---|---|---|
| `commandD` | `recorded_cases=10 depth_score=10` | The mutation runner's header ledger still records ≥10 `js-/bash-` legs (depth score capped at 10). |
| `coldread-floor` | `score=6 credited=46` **RED** | The round-21 cold-read ledger still credits **every** SKILL.md section at this rev (`score>=8` ⇔ box-3 full page, `credited>=64`). |
| `r45-freshness` | `population=74 fresh=71 score=9` | The round-45 freshness cohort keeps ≥71 fresh rows and a ≥9/10 score. |
| `r45-coverage` | `rows=2 entries=2 C2_R45_PASS=true` | Round-45's two coverage rows still have their ledger entries and the counter verdict holds. |
| `S160-count` | `1` | `corpus/SOURCES.md` carries exactly one S160 row (no duplicate/loss of that pinned row). |
| `registry-rows-not-below-139` | `140` | The source registry never drops below the absolute floor of 139 rows. |
| `r46-coverage` | `rows=3 entries=3 C3_R46_PASS=true` | Round-46's three coverage rows/entries and its PASS verdict hold. |
| `r47-coverage` | `rows=3 entries=3 C3_R47_PASS=true` | Round-47's three coverage rows/entries and its PASS verdict hold. |
| `tools-scope` | `[M:context-capture.py M:registry-check.py M:registry.json M:repeat-control.py]` | Between base and this rev, only allow-listed tool/registry files changed. |
| `registry-row-names-unchanged` | `count=56` | The registry's row **names** are the same set as at base (cells may change, rows may not). |
| `r49-generator-capability` | `cases=400 violations=0 …` | The staged-id generator still produces 400 cases with zero invariant violations and the exact class census. |
| `r50-shrinker-selftest` | `cases=14 failed=0` | The case shrinker's own suite still reports zero failures. |
| `r53-scratch-hygiene` | `tmp_hits=0` | No `tools/` file still hardcodes `dir = "/tmp"`. |
| `ledger-not-shrunk` | `base=591 rev=591` | The round-21 ledger still has at least as many entries as at base. |
| `sources-not-shrunk` | `base=139 rev=140` | The source registry is not smaller than at base (this round added S280). |

## 3. The one RED: classification

**Verdict: a real, correct RED — the round's declared re-key obligation — but the round has mis-sized
it by 17 sections. It is neither a stale monitor nor a defective monitor. It is not a harm to
operability (no tool behaviour changed); it is a real gap in the lane's evidence currency, and it is
the gate that must go green before the round can claim its calibration axis.**

Evidence, my own measurements (receipt `coldread-summary.txt` / `.json`):

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo <lane> --rev <REV>
base   0a2010acd1e92e4e332774050825e21bcfc7e079: score=8 covered=64/64 box3=True  uncovered=0
freeze e2979f277138da503af27b263b783f626f109be4: score=8 covered=64/64 box3=True  uncovered=0
C0     9cf0146b94ddba12d454ebf7288ce6e5c5d535bb: score=6 covered=46/64 box3=False uncovered=18
```

So the monitor is **not stale**: it reads green at both the base and the frozen counter commit, and it
fires only on C0.

The 18 uncovered sections at C0 are:

* **1 by section bytes** — `## Standing rules` (start line 17), reason `no-ledger-entry`: the section's
  sha256 changed, so no ledger entry matches it. This is the drift the round declares.
* **17 by `input-drift`** — sections whose *bytes* are unchanged but whose ledger entry records, as
  `inputs`, files C0 edited:

```
$ git -C <lane> diff --name-status 0a2010acd1e92e4e332774050825e21bcfc7e079 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb -- tools corpus
M corpus/QUALITY.md
M corpus/SOURCES.md
M corpus/knowledge/scratch-root-contract.md
M corpus/lessons/round-54.md
A corpus/lessons/round-55.md
M tools/context-capture.py
M tools/registry-check.py
M tools/registry.json
M tools/repeat-control.py
```

`input_failures()` / `input_reason()` in `.ufo/evidence/round-18/measure.py` (defs at lines 330 / 353)
hash each recorded input at REV and return `input-drift:<path>` on any mismatch; `coldread()` (def at
549, credit decision at 636–641) credits a section only when some same-sha entry passes, so every
section whose live entry lists one of those files loses credit.

**Attribution proof (counterfactual, receipt `coldread-counterfactual-skillmd-only.json`).** In a
`git clone --shared` of the lane at C0 I checked out the seven non-SKILL files C0 touched
(`corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/knowledge/scratch-root-contract.md`,
`tools/registry.json`, `tools/registry-check.py`, `tools/context-capture.py`,
`tools/repeat-control.py`) back to base and committed (`610749e7bf0b43717716ca8004b9387a1664ac10`):

```
counterfactual score=6 covered=63/64
uncovered: [(17, '## Standing rules', 'no-ledger-entry')]
```

i.e. the SKILL.md edit alone costs exactly **one** section (63/64 — the value wave 1 predicted in
`T55W1ExecRekeyPrep.md`), and C0's other seven file edits cost the other **17**.

**Consequence for the round (this is the actionable finding).** `coldread-floor` requires
`credited>=64`. Re-keying only `## Standing rules` (the plan stated in the wave context and in
`T55W1ExecNoHarm.md` §"fix list") lands at 63/64 → the arm stays RED, and `box3_full_page` stays false
so `score` stays 6. The re-key obligation is **18 sections**: one new-shape entry for start 17, plus 17
entries whose `inputs` must be re-recorded at C0 (their section bytes are unchanged, so their `sha256`
key still matches — only the `inputs`/`read_rev` need to be re-bound, and the entry must still carry a
credit-eligible class/verdict and a trace receipt under strict mode).

I do **not** fix this (report only, per item). Wave-3's re-key readers need this number before they run.

## 4. Can each monitor fail? Falsification probes (receipt `monitor-probes.stdout`)

Every probe is a commit in a scratch clone at C0 (`git rev-parse --show-toplevel` asserted equal to the
clone before any commit); each then runs the monitor line **verbatim** from `no-harm.sh`.

| Probe | Mutation | Monitor line result | Reads |
|---|---|---|---|
| A | delete the round's only new row `S280` | `S160-count 1 ok` / `registry-rows-not-below-139 139 ok` / `sources-not-shrunk base=139 rev=139 ok` | **three blind arms** |
| B | rename one registry row | `registry-row-names-unchanged count=56 RED` | fires |
| C | append a comment to `tools/shrink-case.py` (outside the allowlist) | `tools-scope [... M:tools/shrink-case.py] RED` | fires |
| D | keep 591 ledger entries, replace every entry with `{}` | `ledger-not-shrunk base=591 rev=591 ok` **and** `coldread-floor score=6 credited=0 RED` | count-only; caught by the floor |
| E | delete the `S160` row | `S160-count 0 RED` | fires |

**Probe A is a real monitor defect (not dead weight, but blind in the direction this round moves).**
The absolute floor is `-139` = the *base* count, while the tree now has 140; and `sources-not-shrunk`
compares against the same base (139). So dropping S280 — the one source row this round adds — leaves
all three source monitors `ok`. A round whose whole source contribution can be deleted with zero
monitor response is not monitored on that surface. Do not fix here; the repair is the floor (140, or
compare against the freeze/tip) — one seat's finding, not a wave action.

**Probe D** shows `ledger-not-shrunk` is count-only and cannot see content neutering — but the paired
`coldread-floor` catches it in the same run (`credited=0`), so it is a cheap partial duplicate rather
than dead weight. Note the asymmetry: it would stay `ok` if *entries* were destroyed but a re-key
restored the credit; harmless.

**Probe B/C/E** show the three guards this wave leans on (registry row identity, tool scope, S160
uniqueness) each fire on a one-line mutation — they are live.

## 5. Other observations on the monitor set (reported, not fixed)

1. **`tools-scope` allow-list is wider than the diff**: it permits changes to `tools/env-diff.py`,
   `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, none of
   which changed. Harmless (an allow-list is a ceiling), but it means "tools-scope ok" does not mean
   "only the four expected tools changed".
2. **`coldread-floor` measures with the working tree's `measure.py`** (`python3
   .ufo/evidence/round-21/coldread/measure.py` from `cd "$LANE"`), not `REV:`'s copy. The lane worktree
   has uncommitted wave-1 report edits; `measure.py` itself is unchanged, so the reading is valid today,
   but the monitor is not hermetic against a worktree edit of the counter.
3. **The script exits `0` while a line is `RED`.** `EXIT=0` with `coldread-floor … RED` on line 2: the
   only aggregate a caller can see is per-line text. `if bash no-harm.sh …; then` (or `set -e`) passes
   on a RED arm. That is a genuine fail-open at the script level (the header documents the line format,
   not an exit contract, so this is a defect of omission, not a lie).
4. `2>/dev/null` on the cold-read measure blanks stderr; a crashing measure yields an empty `CR` and
   therefore an uninformative RED (fails safe, but the reason line is lost).

## 6. The seven tools' own self-tests at C0

Scratch clone: `git clone --shared <lane> clone && git -C clone checkout 9cf0146b…` — toplevel asserted
to be the clone. `TMPDIR` set to a dir under my seat scratch (never `/tmp`). Receipts:
`selftests-at-c0/<tool>.out|.err`.

| # | Tool (mode) | rc | Last line |
|---|---|---|---|
| 1 | `python3 tools/repeat-control.py --selftest` | **0** | `SELFTEST: PASS (29 cases)` |
| 2 | `python3 tools/registry-check.py --selftest` | **0** | `SELFTEST: PASS (51 cases)` |
| 3 | `python3 tools/bash-witness-study.py selftest` | **0** | `VERDICT: PASS` |
| 4 | `python3 tools/pin-disposition.py --selftest` | **0** | `SELFTEST: PASS (19/19)` |
| 5 | `python3 tools/evidence-disposition.py --selftest` | **0** | `SELFTEST: PASS (66/66)` |
| 6 | `python3 tools/context-capture.py --selftest` | **0** | `SELFTEST: PASS (49/49)` |
| 7 | `python3 tools/env-diff.py --selftest` | **0** | `ENVDIFF_SELFTEST: 9/9 pass` |

Seven of seven exit 0, every suite reports a full pass count, no stderr. This corroborates C2's
allocating-mode surface at this rev from the tools' own side (not from the frozen counter).

## 7. Census (round bound)

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
… 
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
CENSUS_EXIT=0
```

Exit 0 with the registry at 140 rows at C0 (`git show 9cf0146…:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'`
→ `140`); the four `W04 duplicate url` warnings (S266, S267, S268, S274) are carried rows, none of them
this round's S280. Receipt: `census-validate.stdout`.

## 8. Residual risk and verification gaps

- I did not re-derive the internals of `r45-freshness`, `r45/r46/r47-coverage`, or
  `r49-generator-capability`; I reproduced their lines twice and observed the classes they print, no more.
  Their own counters were not falsified by me.
- Probe A's blind spot is proven for *row deletion at C0*; I did not test partial rewrites of S280's
  cells (that surface is the sources-verifier seats' item).
- No `lsp` device is mounted in this session (`lsp` is absent from the tool inventory), so caller/
  definition checks were done by reading the git blobs of `.ufo/evidence/round-18/measure.py`
  (`input_reason`, `input_failures`, `coldread`, `entry_is_stale`) and `…/round-21/coldread/measure.py`
  at their revs; that is text evidence, not semantic proof.
- Tooling: no installs or upgrades were made; scratch was `export HYAKU_SCRATCH=/fast/scratch/hyaku`
  with `S=$HYAKU_SCRATCH/tameshi-r55/T55W2RevNoHarm`, and only that seat directory is removed.
- I touched no lane file, no frozen file, no `~/.local/bin`, no fleet-root tracked file; writes are
  confined to this report, its receipts directory, and my scratch clone.
