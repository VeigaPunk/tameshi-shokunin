# T53W2ScribeReport — round-53 report evidence tables (draft for the L1)

Seat: scribe, wave 2. Lens: calibration. Read-only over the lane; no git/jj
mutation, no counter execution, no product edit. Everything below is read from
git objects or from committed receipts; the two `after/` receipts are marked
PENDING because `.ufo/evidence/round-53/after/` does not exist yet:

```
$ ls .ufo/evidence/round-53/after
ls: cannot access '.ufo/evidence/round-53/after': No such file or directory
```

Revisions read: `6db1d220` (BASE), `cf87276` (freeze), `a7ba4e3`, `b78fb70`,
`f68deea`, `4d352ad`, `e62d997` (amendments 1–5), `a36d3e5` (phase-A
controls), `218bc6b` (fix pass 1), `a41195d` (C*), `ace79e3` (wave-1
dispatch), `5b703c6` (C**), `7d8aaac` (amendment 6 = the freeze), `61b062f`
(wave-2 dispatch), `e98044a` (re-key pass 1), `d008822` (errata revert, lane
tip when this was written). HEAD moved once during the seat
(`e98044a → d008822`); each row names its own rev.

Frozen-file integrity at the tip: the eight files `freeze.json` hashes were
re-hashed in the working tree (identical to HEAD) and every one matched:

```
5fb52e4d2522521036412386a7b1b3da18776533f4c39a31782c2f215b0b7b4c  .ufo/evidence/round-53/contract.json
da89149195b863ad5982dd50c072d0aecffd8eb11593db3d931a409c355fd391  .ufo/evidence/round-53/c1/measure.py
069a680e8d93a07aa1d89cd6e7c09328381378d505051ad9fd972584fe461ea9  .ufo/evidence/round-53/c1/lost-headings.json
1942cd8f9850727066439d317acaf5eb0a8e44458b0355ea4dceaf90e8c82c27  .ufo/evidence/round-53/c2/measure.py
e4e6b7ad803f5f591ceb5f83b3540bc46b0be0de958d17dc74064485ea1e9e6b  .ufo/evidence/round-53/no-harm.sh
585e166d4ab786712d3ebd280fe1617df8bb5b1fa1fcb43967f9320c0eb6c243  .ufo/evidence/round-53/deciding-run.sh
c5a37ca1ecd638093a1f814de8c55581505cf2cc06b45cb70bf59ed031054657  .ufo/evidence/round-53/control/controls.py
c80f5a8ca676e3a179ca53fb2d50b0a43d234c604fdb3cc8398fa8be94ebf4e5  .ufo/evidence/round-53/control/break-fixtures.py
```

## 1. Per-claim before/after

Counter forms are the ones frozen in `contract.json`; the deciding run adds
`--explain` and runs each counter from a `git show` extraction under
`$HYAKU_SCRATCH/tameshi-r53/deciding` with `TMPDIR` bound there
(`deciding-run.sh:16,31,44-56`), never from the working tree.

### C1 — cold-read floor re-key (calibration, axis 8)

| State | Rev | Counter | Verdict (verbatim) | Receipt | Status |
|---|---|---|---|---|---|
| before, do-nothing precheck | `6db1d220` | frozen round-48 precheck | `COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=6db1d220b337 cand_credited=45 lost=19 RED` | `.ufo/evidence/round-53/before/coldread-precheck-at-tip.stdout` + `.exit` (`1`) | OBSERVED, committed at `cf87276` |
| before, do-nothing counter | `6db1d220` | `c1/measure.py --lane LANE --rev REV --work EMPTY_DIR` | `CONTROL CTL_C1_BASE verdict=false PROBLEM lost-headings-missing-at-rev expected=false pass` | `.ufo/evidence/round-53/control/controls.stdout` (exit `0`, `CONTROLS: total=2 pass=2`) | OBSERVED, committed at `a36d3e5` |
| before, post-fix-pass (contract prose) | `218bc6b5` | `c1/measure.py` | `cand_credited=34 lost=30 RED` | **none at `218bc6b5`** — see calibration note N1 | CLAIMED ONLY |
| mid-state, C* | `a41195d` | `c1/measure.py` | `C1_R53: rev=a41195dfc13a credited=34 lost=30 rekeyed=0/30 readers=0/30 total=32 C1_R53_PASS=false` | `.ufo/waves/round-53/w1/T53W1RevCounters.md:9` (committed in `61b062f`); the raw stdout/stderr live only in that seat's scratch and are cited by sha256 in the same file | OBSERVED by a wave-1 seat |
| mid-state, C** | `5b703c6` | `c1/measure.py` | not run in the lane | — | NOT RECEIPTED |
| after, target | deciding `REV` | `c1/measure.py` | expected `C1_R53: rev=… credited=64 lost=0 rekeyed=30/30 readers=30/30 total=0 C1_R53_PASS=true` | `.ufo/evidence/round-53/after/c1.stdout`, `.ufo/evidence/round-53/after/c1.exit` (with `c1.start` / `c1.end` written by `deciding-run.sh`) | **PENDING** |

Re-key state already landed upstream of the deciding rev (wave-1-clean half):

```
$ git show --stat --format='' e98044a
 .ufo/evidence/round-21/coldread/ledger.json        | 2101 +++++++++++++++-----
 .../rekey-r53-a41195dfc13a/refresh-receipts.json   |   92 +
 .../rekey-r53-a41195dfc13a/traces/section-01.json  |  115 ++
 .../rekey-r53-a41195dfc13a/traces/section-03.json  |  187 ++
 .../rekey-r53-a41195dfc13a/traces/section-05.json  |   97 +
 .../rekey-r53-a41195dfc13a/traces/section-17.json  |  173 ++
 .../rekey-r53-a41195dfc13a/traces/section-18.json  |  183 ++
 .../rekey-r53-a41195dfc13a/traces/section-23.json  |   59 +
 .../rekey-r53-a41195dfc13a/traces/section-24.json  |  109 +
 .../rekey-r53-a41195dfc13a/traces/section-27.json  |   61 +
 .../rekey-r53-a41195dfc13a/traces/section-28.json  |  207 ++
 11 files changed, 2929 insertions(+), 455 deletions(-)
```

The nine `section-*.json` traces are the nine wave-1-clean headings; their
`argv` tails name the sections:

```
## Context gate classification and explicit exit classes — round 15
## Live-tree re-pin and entry-command monitor — round 17
## Pin disposition and provenance correction — round 13
### Round-18 gate/probe registry — routed-defect closure
### Round-21 gate/probe registry — finite environment differential
### The receipt at this boundary
### The service's limits — what tameshi refuses to mutation-test
### The tick, executed
### Triggers T1–T3 and the re-pin rule
```

`c1/measure.py` at the freeze accepts 1..N `rekey-r53-<12 hex>` directories
(amendment 6), so this pass-1 directory does not satisfy the arm alone: the
verdict must still read `rekeyed=30/30 readers=30/30`.

### C2 — `tools/` scratch hygiene (operability)

| State | Rev | Counter | Verdict (verbatim) | Receipt | Status |
|---|---|---|---|---|---|
| before, grep surface | `6db1d220` | `git grep -n -E 'dir\s*=\s*["'"'"']/tmp' REV -- tools/` | 9 hits in 7 files (`bash-witness-study.py:1241`, `context-capture.py:27,1625`, `env-diff.py:61`, `evidence-disposition.py:2351`, `pin-disposition.py:706`, `registry-check.py:766,917`, `repeat-control.py:597`) | reproduced read-only for this table | OBSERVED |
| before, do-nothing counter | `6db1d220` | `c2/measure.py --lane LANE --rev REV --work EMPTY_DIR` | `CONTROL CTL_C2_BASE verdict=false T: 9/9 pass] cr47=rc=0 docs=stale-patterns=4 total=4 C2_R53_PASS=false expected=false pass` | `.ufo/evidence/round-53/control/controls.stdout` | OBSERVED, committed at `a36d3e5` |
| mid-state, C* | `a41195d` | `c2/measure.py` | `C2_R53: rev=a41195dfc13a tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=0 docs=ok total=2 C2_R53_PASS=false` | `.ufo/waves/round-53/w1/T53W1RevCounters.md` (committed in `61b062f`) | OBSERVED by a wave-1 seat |
| mid-state, C* CR47 arm | `a41195d` | extracted `registry-check.py --selftest` with missing `TMPDIR` | `CHECK3 registry-check --selftest, missing TMPDIR: FAIL (exit 0, expected non-zero; no scratch message; no REGISTRY_CHECK verdict line printed)` | `.ufo/waves/round-53/w1/T53W1ExecTmpVerify-receipts/VERDICT.txt` | OBSERVED by a wave-1 seat |
| mid-state, C** | `5b703c6` | — | the fix pass claims `strict TMPDIR scratch-root helper in 7 tools (CR47: set-but-unusable TMPDIR is could-not-evaluate, never a silent /tmp fallback)` | commit subject only; no C2 counter receipt at `5b703c6` | CLAIMED ONLY |
| after, target | deciding `REV` | `c2/measure.py` | expected `C2_R53: rev=… tmp_hits=0 … cr47=rc=<non-zero> docs=ok total=0 C2_R53_PASS=true` | `.ufo/evidence/round-53/after/c2.stdout`, `.ufo/evidence/round-53/after/c2.exit` (with `c2.start` / `c2.end`) | **PENDING** |

The `cr47` cell is the one that must change between C* (`rc=0`, the defect)
and the deciding rev (`rc≠0` naming scratch creation). It is also the only C2
sub-check with no post-fix receipt anywhere in the lane.

### Gates around the after receipts (`deciding-run.sh`, `contract.json` kill_rule)

| Gate | Predicate in the frozen bytes | Receipt it writes | Pre-state |
|---|---|---|---|
| control receipts committed at REV in a commit descending from FREEZE | `git cat-file -e "$REV:$f"` + `merge-base --is-ancestor` for `control/controls.{stdout,exit}` (`deciding-run.sh:22-27`) | — | **REFUSES at the tip** — see N0 |
| FROZEN_UNCHANGED | `git diff --quiet "$FREEZE" "$REV" -- $FROZEN` (12 paths) | `after/frozen.stdout` | hashes match at the tip (above) |
| clean tree | `git status --porcelain`, tolerating only untracked paths under OUTDIR | `after/clean-tree-before.txt`, `after/clean-tree-after.txt` | wave-2 reports must be committed before the run |
| one invocation per counter | refusal if `after/c1.start` or `after/c2.start` exists | `after/{c1,c2}.start` | none |
| no-harm | 12 monitors, all `NOHARM <name> … ok` | `after/no-harm.stdout`, `.exit` | `grep -c 'echo "NOHARM'` = 12 |
| cold-read precheck | last line `cand_credited=64 lost=0 ok`, exit 0 | `after/coldread-precheck.stdout`, `.exit` | base receipt RED (before/) |
| census | `scripts/sources-census.sh validate --root FLEET tameshi` exit 0 | `after/census.stdout`, `.stderr`, `.exit` | `census-start.exit` = 0 |
| claim verdicts | `grep -q "${k^^}_R53_PASS=true"` on each counter stdout | `after/c1.stdout`, `after/c2.stdout` | PENDING |

## 2. Landed changes — `git log --oneline 6db1d220..d008822` mapped to LOG.md

LOG.md's round-53 entry is `## 2026-10-27 — round 53, attempt 2 (this round)`
at line 2465 and is byte-unchanged since C* (`git diff --stat a41195d d008822 --
LOG.md` is empty). Its last sentence declares the rest pending.

| Commit | Subject (trimmed) | Touched | LOG.md entry |
|---|---|---|---|
| `cf87276` | freeze — C1 cold-read re-key repair + C2 tools scratch hygiene | 14 files: `contract.json`, `c1/{measure.py,lost-headings.json}`, `c2/measure.py`, `no-harm.sh`, `deciding-run.sh`, `control/{controls.py,break-fixtures.py}`, `before/*`, `census-start.*` | § round 53 names the freeze only as `e62d9971` — see N2 |
| `a7ba4e3` | amendment 1 — c1 counter NUL-byte syntax repair; re-freeze | `c1/measure.py`, `control/controls.{stderr,stdout}`, `freeze.json` | covered by "amendments 1–5, all disclosed in `freeze.json`" |
| `b78fb70` | amendment 2 — c1 counter fails soft on absent round-53 evidence | `c1/measure.py`, `freeze.json` | same line |
| `a36d3e5` | phase-A controls scored at freeze bytes (2/2 as pre-registered) | `control/controls.stdout`, `control/controls.exit` | none (no LOG line for the phase-A control scoring) |
| `218bc6b` | fix pass — 21 T52 reader findings resolved in SKILL.md; `tools/` /tmp hardcodes honour TMPDIR; recipe+registry scratch docs name HYAKU_SCRATCH | `SKILL.md`, 7 `tools/*.py` | "21 T52W3 reader findings fixed L1-inline (`218bc6b5`)" |
| `f68deea` | amendment 3 — c2 doc patterns bound to stale /tmp forms | `c2/measure.py`, `freeze.json` | covered by the amendments-1–5 line |
| `4d352ad` | amendment 4 — c2 git-grep arm handles the no-match exit | `c2/measure.py`, `freeze.json` | same line |
| `e62d997` | amendment 5 — re-key scope extended to 30 headings; re-freeze | `c1/lost-headings.json`, `c1/measure.py`, `contract.json`, `freeze.json` | same line (and this is the pointer LOG.md calls the freeze) |
| `a41195d` | **C\*** content commit — fix pass, S275/S276 assimilation, round-53 lesson, QUALITY 104, LOG r52+r53 entries, README F7 note | `LOG.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/change-aware-resweep-cadence.md` (A), `corpus/lessons/round-53.md` (A) | the round-53 entry itself (this commit) plus "assimilation of `change-aware-resweep-cadence.md` (S275/S276 …); considerate proposal 1 mined as `.ufo/evidence/round-53/verify-freeze.sh` …; QUALITY 104" |
| `ace79e3` | wave-1 spec + dispatch (44 seats) + ready marker | `.ufo/waves/round-53/{spec-w1.json,w1-dispatch.json,w1-run.out,w1.ready,w1.ready.partial,w1/swarm-registry.json}` | none — "Waves and deciding receipts to follow under this entry" |
| `5b703c6` | **C\*\*** fix pass 2 — 40 wave-1 reader findings resolved; strict TMPDIR scratch-root helper in 7 tools | `SKILL.md`, the same 7 `tools/*.py` | none — see N2 |
| `7d8aaac` | amendment 6 — c1 multi-rekey-dir + sha-only reader binding; re-freeze before wave 2 | `c1/measure.py`, `freeze.json`, plus 200 assimilation evidence files | none, and it is the current freeze — see N2 |
| `61b062f` | fix pass 2 commit + amendment 6 + wave-2 spec/dispatch (40 seats) + ready marker | `.ufo/waves/round-53/{spec-w2.json,w1.ready.dispatched,w2*}` and the whole committed wave-1 corpus (`T53W1*.md/json` + `T53W1ExecTmpVerify-receipts/*`) | none |
| `e98044a` | re-key (pass 1) — 9 wave-1-clean sections trace-bound at C*; 21 re-fixed await wave-2 readers | `ledger.json`, `rekey-r53-a41195dfc13a/{refresh-receipts.json,traces/section-0{1,3,5,7}…}`, 11 files | none |
| `d008822` | revert the errata-table row edit | `SKILL.md` (1 line) | none — see N3 |

## 3. Calibration notes (each with its command-output backing)

**N0 — the deciding run refuses at gate 0 as the lane stands (blocking).**
Gate 0 requires each control receipt's last-touching commit to descend from
the freeze. The receipts were last touched at `a36d3e5`, the freeze is now
`7d8aaac` (amendment 6), and no commit after the freeze touches either path:

```
$ git log --oneline -- .ufo/evidence/round-53/control/controls.stdout
a36d3e5 round-53: phase-A controls scored at freeze bytes (2/2 as pre-registered), before wave 1
a7ba4e3 round-53: amendment 1 — c1 counter NUL-byte syntax repair (no predicate/target/control change); re-freeze
$ git log --oneline -- .ufo/evidence/round-53/control/controls.exit
a36d3e5 round-53: phase-A controls scored at freeze bytes (2/2 as pre-registered), before wave 1
$ FREEZE=7d8aaac676cbcb6379f57659e7c3c4c12150a815
$ for f in .ufo/evidence/round-53/control/controls.{stdout,exit}; do
    c=$(git log -1 --format=%H HEAD -- "$f")
    git merge-base --is-ancestor $FREEZE $c || echo "REFUSE $f last-touch=$c"
  done
REFUSE .ufo/evidence/round-53/control/controls.stdout last-touch=a36d3e514d6565f6dbcb14bf0f70ecc379521ecb
REFUSE .ufo/evidence/round-53/control/controls.exit last-touch=a36d3e514d6565f6dbcb14bf0f70ecc379521ecb
```

The gate would print `DECIDING_REFUSED control-receipt-not-after-freeze` and
exit 3 with nothing run. This is structural, not a wave-2 regression: every
re-freeze from amendment 3 (`f68deea`) onward moved the freeze past the
receipts' commits, and re-freezing alone cannot repair it — the receipts must
be *re-committed* after the freeze with bytes that differ from the committed
ones (a re-run producing an identical `controls.stdout` would leave the path
untouched and keep gate 0 failing). The L1 decides the repair; this seat only
records that the after receipts cannot be produced until it lands.

**N1 — the C1 "before" carries one unreceipted number.**
`contract.json` `before` (line 15) reads:

> `cand_credited=45 lost=19 RED at base 6db1d220; cand_credited=34 lost=30 RED at the post-fix-pass candidate 218bc6b5 (the round's own edits, repaired by the same re-key) (before/coldread-precheck-at-tip.stdout, exit 1)`

but the cited receipt records only the base run:

```
$ tail -1 .ufo/evidence/round-53/before/coldread-precheck-at-tip.stdout
COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=6db1d220b337 cand_credited=45 lost=19 RED
$ grep -rln 'lost=30' .ufo/evidence/round-53/
.ufo/evidence/round-53/contract.json
$ grep -rn 'lost=30' .ufo/evidence/round-53/ | grep -vc contract.json
0
$ grep -n 'lost=30' .ufo/waves/round-53/w1/T53W1RevCounters.md
9:  `C1_R53: rev=a41195dfc13a credited=34 lost=30 rekeyed=0/30 readers=0/30 total=32 C1_R53_PASS=false`
```

So the only 34/30 records in the lane are the C* wave-1 ones; there is no
receipt at `218bc6b5`.

The report must therefore print that row as *contract prose, no receipt*, and
may cite the C* row instead. `contract.json` is frozen and was not edited by
this seat. (Wave-1 already filed this as F10; it is still uncorrected at the
tip.)

**N2 — LOG.md's freeze pointer is stale.**
LOG.md line 2468:

> `limit; nothing to inherit. Base `6db1d220`; freeze `e62d9971` (amendments`

versus `freeze.json`, which lists six amendments and whose commit is
`7d8aaac` (`git log --oneline -1 7d8aaac` →
`round-53: amendment 6 — c1 multi-rekey-dir + sha-only reader binding; re-freeze before wave 2`).
LOG.md has not been touched since C* (`git diff --stat a41195d d008822 -- LOG.md`
prints nothing), so amendment 6, the C** fix pass, the wave-1 and wave-2
dispatch/results, re-key pass 1 and the errata revert are all absent (C*'s own
work is described by the entry that C* commits). The report's freeze cell must
read `7d8aaac6`, and LOG.md needs the line before close. The "waves … to
follow" sentence covers the waves, not the freeze pointer or `d008822`.

**N3 — the errata revert is what keeps both sha bindings valid.**
`## Errata — round 16 full-page cold-read` section sha256 (frozen round-18
`sectionize`, first 16 hex):

```
base 6db1d220 290e75a411fb643b   fix-pass-1 218bc6b5 290e75a411fb643b
C* a41195d    290e75a411fb643b   C** 5b703c6        f251e76c4d89560a
pass-1 e98044a f251e76c4d89560a  d008822            290e75a411fb643b
```

i.e. fix pass 2 changed that section's bytes and `d008822` restored them, so
a measured rev of `5b703c6` would have carried the drifted bytes into the
precheck while `d008822` restores the credited ones. No reader is bound to
that section either way: the heading is in neither the 30-entry
`c1/lost-headings.json` nor the 21 wave-2 re-read heads. Both binding sets are
safe at `d008822`:

```
C** vs d008822 drifted headings: 1  (the errata section only)
drifted ∩ wave-2 re-read headings (21): none
drifted ∩ lost-headings (30): none
9 pass-1 re-keyed headings, sha at C*/C**/d008822: identical for all 9
```

Consequence for the tables: a wave-2 reader JSON is valid at any rev whose
`SKILL.md` equals `d008822`'s; the L1 should freeze the measured rev's
`SKILL.md` against it rather than assume "C** is the tip".

**N4 — frozen prose that its own frozen code contradicts.** These are
byte-locked (`.ufo/evidence` is not editable this round) and the
FROZEN_UNCHANGED gate does not read prose, so they are declared limits, not
fixes.

`c1/measure.py:24` says:

```
Verdict line: 'C1_R53: rev=... credited=... lost=... rekeyed=K/19 readers=R/19 total=N C1_R53_PASS=true|false'
```

but the print uses `%d/%d` fed from `len(headings)`, and the frozen
`c1/lost-headings.json` has 30 entries
(`python3 -c "import json;print(len(json.load(open('.ufo/evidence/round-53/c1/lost-headings.json'))))"`
→ `30`).

`c1/measure.py:11-12` says:

```
  2. rekey   — at REV, find the unique .ufo/evidence/round-21/coldread/
               directory 'rekey-r53-<c0>'; <c0> must resolve to a commit that
```

while the code builds `rekey_dirs = [n for n in … if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n)]`
and loops over every one — amendment 6.

`c2/measure.py:18` says:

```
               no 'tameshi-f5.json', no 'tameshi-r21-envdiff.*', and the
```

while `FLEET_DOC_PATTERNS` are `/tmp/tameshi-f5\.json` and
`/tmp/tameshi-r21-envdiff` — amendment 3, so a `$HYAKU_SCRATCH` invocation is
not a hit (SKILL.md at C** does name `$HYAKU_SCRATCH/tameshi-f5.json`).

`control/controls.py:12` says:

```
                (do-nothing control: the two inherited dir="/tmp" hardcodes)
```

while BASE has 9 such hits in 7 files (C2 before row above).

**N5 — `after/` is empty by construction.** `deciding-run.sh` takes OUTDIR as
`$4` and refuses unless it exists and is empty; nothing in the lane creates it.
Both after receipts therefore have to be produced in one invocation, and their
paths are the ones in `contract.json`'s kill_rule
(`… from the deciding receipts under .ufo/evidence/round-53/after/`).

## 4. What these tables do not establish

- No counter was executed by this seat; the two `after` rows are the target
  predicates, not observations. They are also unreachable until N0 is repaired:
  the deciding run exits 3 at gate 0 as the lane stands.
- The `34/30` at `218bc6b5` (N1) and the C** tool fix (C2 mid-state row) have
  no receipt anywhere in the lane.
- The `after` rows say nothing about the wave-2 findings' semantic fairness
  (contract C1 `cannot_see`) or about TMPDIR isolation beyond what the
  selftests cover (contract C2 `cannot_see`).
- The gate table is read from `deciding-run.sh` bytes; whether each gate
  passes is the deciding run's own output.

## Provenance

All reads were `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show
<rev>:<path>` or `git grep`/`git log`; section hashes came from the frozen
`.ufo/evidence/round-18/measure.py` `sectionize` loaded from its committed
bytes. Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2ScribeReport`
(removed before yield). No tool installed or updated; no git/jj mutation; no
file written outside this report path.
