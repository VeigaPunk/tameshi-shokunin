# W2MTScMetric — mid-round SOURCES.md edit vs. the cold-read monitor (C1 calibration)

Seat: mutation-tester, leaf. Lane: `tameshi-shokunin`, round 36, wave 2.
Lane tip at probe time: `fbb01cf46f8437fd1264c1a3acc053c882fa2164` (all work below in a scratch
clone; the lane was never written).

## What was attacked

C1's instrument, not its bookkeeping: the claim is that the round-36 cold-read refresh restores
calibration credit 6 -> 8, and that the same monitor still *enforces* drift after the refresh.
Mutant: a mid-round record edit **after** the refresh — one blank line appended to
`corpus/SOURCES.md`, committed on top of the refresh commit, then the unchanged monitor re-run at
the new revision. Expected detector: score < 8, with the refreshed section(s) that cite
`corpus/SOURCES.md` re-drifting (`input-drift:corpus/SOURCES.md`).

Frozen artifacts re-hashed before/after the probe (unchanged, byte-identical to the dispatch pins):

| artifact | sha256 |
|---|---|
| `tools/tally-audit-v3.py` | `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354` |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `.ufo/evidence/round-36/c1/c1-measure-v2.py` | `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` |

`.ufo/evidence/round-21/coldread/measure.py` (`657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb`)
and `ledger.json` (`29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`) were
read/executed only, never edited.

## Setup (scratch only)

```
git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r36-seats/W2MTScMetric/clone
git -C .../clone checkout --quiet --detach b455001e2589b3f4f471d94a3de7e5e549b9f54c
```

Detector, identical at every step (cited C1 command, no overrides):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
    --repo /fast/scratch/hyaku/tameshi-r36-seats/W2MTScMetric/clone --rev REV
```

Raw JSON + stderr for every run: `/fast/scratch/hyaku/tameshi-r36-seats/W2MTScMetric/evidence/`
(`baseline.json`, `uncommitted.json`, `mutant2.json`, `restored.json`; first-pass `mutant.json`).

## Actual outputs

1. **Pristine baseline at the refresh commit** `b455001e2589b3f4f471d94a3de7e5e549b9f54c`
   (`evidence/baseline.json`): exit 0, `calibration_restraint_score` **8**,
   `sections_covered` **64/64**, `box3_full_page` true, `trace_gate` strict,
   `overrides_used` false, `ledger_committed` true, `sources.rows` 100 / malformed 0,
   `reasons` `{"credited": 64}`. Baseline passes -> a later miss is a real kill, not inconclusive.
   `corpus/SOURCES.md` at this rev: `16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7` (83,707 B).

2. **Uncommitted-edit control** (same one-line append, worktree only, monitor still at `b455001`):
   exit 0, score **8**, 64/64, `{"credited": 64}`. The frozen monitor reads blobs at an explicit
   commit only (documented `git cat-file`/`git show`, no worktree access), so an *unrecorded* edit
   is invisible. The "mid-round record edit" therefore has to be a recorded commit to be in the
   measured record — this control exists so the kill below is not mis-attributed.

3. **Committed mutant** (mid-round record edit): append one blank line, then
   `git -c user.name=fixture -c user.email=fixture@example.invalid commit -a -m 'fixture mutant: append blank line to corpus/SOURCES.md mid-round (recorded)'`.
   New rev `d642a11a0a3c634d8dd30f8cf11c6d5a5fa95909`; `git diff b455001..d642a11 --numstat` =
   `1  0  corpus/SOURCES.md` (nothing else changed). Mutated file:
   `0c8799b1f1809392612d2ce693daa2259ea0bb8bff11cac0da96d26e713f7d41` (83,708 B).
   Monitor at `d642a11` (`evidence/mutant2.json`): exit 0, score **6**, `sections_covered` **63/64**,
   `box3_full_page` false (`sections_covered != sections_total`), strict, no overrides,
   `sources.rows` still 100 (census unaffected — only the digest moved).
   Exactly **one** section flipped credited -> uncovered (diff of `coldread.sections`):
   `start 131, "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence"`.
   Its reason string is the sorted union of the section's entry failures and contains
   `input-drift:corpus/SOURCES.md`.
   An earlier independent commit of the same one-line edit (`f17851b4d8fc975675781482ac0221ef03499344`,
   `evidence/mutant.json`) reproduced the same 6 / 63 / one-flipped-section result.

4. **Entry-level diagnostic** (frozen `entry_reason`, strict; import of the same frozen module, no
   edits): all four round-36 refresh entries (traces
   `.ufo/evidence/round-36/coldread/traces/L1/source-1..4.json`, starts 131/375/1380/1436) are
   `CREDITED` at `b455001`. At `d642a11`: start **131 -> `input-drift:corpus/SOURCES.md`**;
   starts 375/1380/1436 still `CREDITED`. So the kill is specific: the refreshed recipe entry pins
   `corpus/SOURCES.md` among its 9 inputs and loses credit on exactly that digest; the other three
   refresh entries do not cite the file and correctly do not move.

5. **Restoration**: `git reset --hard b455001e2589b3f4f471d94a3de7e5e549b9f54c` in the scratch
   clone. HEAD = `b455001...`, `corpus/SOURCES.md` = `16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7`
   (equals the pre-mutation hash and the blob at HEAD), `git status --porcelain` empty. Monitor at
   `b455001` again: exit 0, score **8**, 64/64, `{"credited": 64}`, `box3_full_page` true.
   Live lane untouched: HEAD still `fbb01cf`, lane `corpus/SOURCES.md` still `16fae0a1...`, the
   three frozen pins above re-verified identical, lane worktree shows only pre-existing untracked
   wave directories plus this report.

## Coverage finding (not a contract change)

Blast radius, measured entry-by-entry with the frozen `entry_reason` at both revs (497 ledger
entries): 85 entries credit at `b455001`, 84 at `d642a11`; **exactly one entry flips
credit -> fail**, and it is the round-36 refresh entry at start 131 with reason
`input-drift:corpus/SOURCES.md`. Every flipped entry pins `corpus/SOURCES.md` (1/1); no entry
without that pin moved. The remaining 152 SOURCES-pinned entries were already non-crediting at the
baseline (stale older-round digests), which is why the section-level count drops by only one.

Of the 20 section starts whose ledger entries cite `corpus/SOURCES.md` (starts 6, 17, 131, 921,
1069, 1155, 1436, 1479, 1517, 1548, 1563, 1609, 1814, 1846, 1855, 1925, 1938, 1964, 2086, 2104),
the one-line edit uncovers only start 131. The other 19 starts still have at least one crediting
entry at the mutant rev, so the section rule's "some entry credits" disjunction masks the drift
there. "Sections citing SOURCES.md" is therefore not a synonym for "sections that must fail": the
instrument enforces drift per entry, and a section only re-drifts when the drifted entry was its
sole credit path. Also note the observable consequence of the frozen commit-keyed reader: the gate
cannot see a mid-round edit until it is committed, so any C1 re-measurement must name the rev that
contains the edit.

## Verdict

**KILLED** — expected detector output confirmed. Pristine `b455001`: 8 / 64-64 (baseline valid);
committed mid-round `corpus/SOURCES.md` append `d642a11`: 6 / 63-64 with the refreshed recipe
section uncovered and `input-drift:corpus/SOURCES.md` in its reason; restored bytes: 8 / 64-64.
The monitor still enforces drift post-refresh; the mutant was caught, not survived.
