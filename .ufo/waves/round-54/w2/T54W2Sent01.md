# T54W2Sent01 — sentinel attack: forge a reader report

Seat: `T54W2Sent01` (sentinel, axes operability + calibration), wave 2, round 54 attempt 2.
Scope: abuse the frozen C1 counter's reader arm (`c1/measure.py` arm 4) at a scratch clone; do not touch any lane production file.

**Instrument attacked** — `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py`,
sha256 `d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812`, which is the digest
`freeze.json` pins for `c1/measure.py` and the current tree's blob (`git show HEAD:c1/measure.py`).
Note the round amended this file during wave 2: amendment 3 (commit `4e2de73`, 12:00:39) widened arm 4
from `w1/` only to `WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')`; amendment 4
(`fe70474`) touched only `c2/measure.py`. Every decisive run below used the sha `d7749f84…` file; the
first exploratory run at 11:57 used the pre-amendment C1 blob (sha256 `6a39b387…`), whose arm 3 is
byte-identical to the amended one (amendment 3 changed only arm 4's directory tuple).

## Verdict (short)

- **The forged reader report is refused. The verdict stays false.** With a hand-bound ledger entry that
  credits (arm 3 `7/7`), the forged report — correct heading, correct `cand`, a `section_sha256` guessed
  without reading the section — placed at a scanned reader path yields
  `arm4-readers 6/7 … total=1 C1_R54_PASS=false` (stage E). Swapping the genuine bytes into the *same*
  path yields `readers=7/7 … total=0 C1_R54_PASS=true` (stage F). There is no path from a guessed sha to
  arm-4 credit.
- **No arm-4 defect found.** Arm 4 is an exact byte pin: `d['cand'] == c0` and
  `d['section_sha256'] == sha256(section bytes at rev)`. A guessed sha cannot satisfy it, whether the
  report sits in `w1/` or (post-amendment-3) `w2/`; the path regex `/T54W\d+.*Read.*\.json$/` is applied
  to every scanned path.
- **Secondary instrument finding F1 (calibration, blocking for the claim if the deciding ledger comes
  straight from the binder):** the binder's own output leaves `.ufo/evidence/round-21/coldread/ledger.json`
  among the bound entry's inputs. That file contains the entry, so its digest changes when the ledger is
  written, and the frozen arm-3 gate (`r18.entry_reason(..., True)`) reads
  `input-drift:.ufo/evidence/round-21/coldread/ledger.json`. A binder-only state with 23 clean readers
  therefore prints `rekeyed=6/7 … total=1 C1_R54_PASS=false` against the current counter (stage A). The
  round-21 monitor (arm 2) still credits 64/64 because it ignores its own ledger; the two arms disagree
  and only arm 3 blocks.
- **Incident (disclosed):** the L1's bulk commit `077d431` swept the forged JSON into lane history before
  my delete step. Details and remediation under "Incident" below.

## Fixture

All git mutation happened in `$HYAKU_SCRATCH/tameshi-r54/T54W2Sent01/clone`, a `git clone --shared` of
the lane, checked out at C1 `99c3bc88d704566197783f66b211ee0a830e0330`; before every commit the fixture
asserted `git -C "$CL" rev-parse --show-toplevel` equals the clone. The lane itself was only read
(`git show`, `git ls-tree`, `git log`, `git status`, `sha256sum`, file reads). Reproducer:
`T54W2Sent01-receipts/commands.sh`.

Fixture commits (in order):

| stage | commit | content | counter verdict |
|---|---|---|---|
| A | `8bb6ba6` | 23 clean reader reports at C1 + `binder.py LANE C1 C1 rekey-r54-99c3bc88d704` committed (23 REKEY, 0 SKIP) | `rekeyed=6/7 … total=1 C1_R54_PASS=false` |
| B | `0537d77` | hand-bind: drop the self-referential round-21 ledger input from the bound Mutation-sweep entry and its trace | `rekeyed=7/7 readers=7/7 … total=0 C1_R54_PASS=true` |
| C | `395995b` | forged bytes at scanned `w1/T54W2Read07.json` (plus a copy under `w2/`) | `readers=6/7 … total=1 C1_R54_PASS=false` |
| D | `bd1bdc8` | genuine bytes restored at `w1/`, forged copy left only under `w2/` | `readers=7/7 … total=0 C1_R54_PASS=true` |
| E | `5ec0630` | forged bytes at scanned `w2/T54W2Read07.json` (no Standing-rules report in `w1/`) | `readers=6/7 … total=1 C1_R54_PASS=false` |
| F | `640a2cd` | genuine bytes at the same `w2/T54W2Read07.json` (control) | `readers=7/7 … total=0 C1_R54_PASS=true` |

The 23 report files are synthetic clean reads (`"findings": []`) built from
`reader-section.py LANE C1 "<heading>"`; they simulate the expected wave-2 outcome and are not evidence
about the sections' quality. The ledger entries bound to them are real binder output from the lane's
real ledger at C1.

## Exact bytes

Forged report written under the seat's write scope and then deleted from the lane worktree (bytes kept
in `T54W2Sent01-receipts/forged-reader.json`):

```
{"heading": "## Standing rules", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "section_sha256": "b90c1f799d0ce42a9fbb04b156ce9d5b4bb7395235b2fc9ca4b426669feb9927", "findings": []}
```

- sha256 of that file: `749abcdbf960fff9f4ee4fb448312cae604527208dbdb4870392bfc7b84faa7f`
- guessed sha: `sha256(b"forged-r54-sent01: never read the section bytes")` — derived from a fixed
  string, never from the section bytes.
- genuine section sha at C1 (`reader-section.py`, receipt
  `reader-section-standing-rules.json`):
  `{"heading": "## Standing rules", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 17, "end": 40, "section_sha256": "61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc"}`
- The forged `cand` is the *correct* full C1 commit (guessable from the rekey directory name), so the
  only wrong field is the byte pin — the strongest form of the forgery.

## Receipts (command → output → verdict)

Counter command shape (fresh empty `--work` per run):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py \
  --lane "$CL" --rev <commit> --work "$S/work<stage>" --explain
```

**Stage A — binder output only (F1).** Receipt `stageA-binder-only-6of7.out`.

```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=8bb6ba6b520f cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor exit=0 covered=64 score=8
EXPLAIN arm3-rekey dirs=['rekey-r54-99c3bc88d704'] c0=99c3bc88d704566197783f66b211ee0a830e0330
EXPLAIN arm4-readers 7/7
C1_R54: rev=8bb6ba6b520f c0=99c3bc88d704 credited=64 lost=0 rekeyed=6/7 readers=7/7 monitor=8/64 unstable=0 total=1 C1_R54_PASS=false
```

Verdict: false, and the sole failing arm is arm 3. The failing heading is `## Mutation-sweep recipe —
numbered steps; bounded cold-read evidence`; calling the frozen `r18.entry_reason(lane, rev, entry, True)`
on its bound entry returns `'input-drift:.ufo/evidence/round-21/coldread/ledger.json'`. The binder
(`integrate/binder.py:49`) drops `LOG.md`, `SCORECARD.md`, `SKILL.md` but not the round-21 ledger, and
`r18`'s `IGNORED_INPUTS` (`r18:134-136`) covers only `SKILL.md`, the round-17 and the round-18 ledgers.
The entry and its trace record the ledger:

```
.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/traces/section-04.json:3499:
  ".ufo/evidence/round-21/coldread/ledger.json": "3a086406768ec09c16595795ba536c3cba82a1799d641dc5090fe2cb6571930e",
```

This cannot converge by re-running the binder at a later PIN: the recorded digest is of the file that
contains the entry, so each pass rewrites the ledger and changes its own recorded digest. Smallest
remediation: add `.ufo/evidence/round-21/coldread/ledger.json` to the binder's `DROP` tuple (the gate is
frozen and cannot take it), or hand-drop it from the one affected entry (stage B). Impact: with the
current binder, a perfect wave-2 read floor still yields `C1_R54_PASS=false`.

**Stage B — hand-bound entry credits.** Receipt `stageB-handbound-true.out`.

```
C1_R54: rev=0537d77dfedc c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

The hand-bind diff (one input line removed from the trace and the entry) is in `hand-bind.diff.txt`.

**Stage C — forged at a scanned `w1/` path.** Receipt `stageC-w1-forged.out`.

```
EXPLAIN arm4-readers 6/7
C1_R54: rev=395995b776f8 c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=6/7 monitor=8/64 unstable=0 total=1 C1_R54_PASS=false
```

**Stage D — genuine restored, forged copy present only under `w2/`.** Receipt
`stageD-w2-copy-genuine.out`.

```
C1_R54: rev=bd1bdc855256 c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

**Stage E — forged at the scanned `w2/` reader path (the seat item as written).** Receipt
`stageE-w2-forged.out`.

```
EXPLAIN arm4-readers 6/7
C1_R54: rev=5ec0630e84a3 c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=6/7 monitor=8/64 unstable=0 total=1 C1_R54_PASS=false
```

Arm 3 is `7/7` here: the hand-bound entry for `## Standing rules` credits, so the false is caused only by
the forged reader. `w2/` is a scanned directory after amendment 3 (`WAVE_DIRS`), which stage F confirms.

**Stage F — control, genuine bytes at the same `w2/` path.** Receipt `stageF-w2-genuine.out`.

```
EXPLAIN arm4-readers 7/7
C1_R54: rev=640a2cdbd99c c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

E→F is the exact A/B: same path, same heading, same `cand`, only the `section_sha256` differs. The
guessed sha is the single cause of the false.

**Stage G — the live lane at `077d431` (observation, not a claim about the deciding revision).** Receipt
`lane-head-077d431.out`.

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=077d431e6996 cand_credited=60 lost=4 RED
EXPLAIN arm2-monitor exit=0 covered=60 score=6
EXPLAIN arm3-rekey dirs=['rekey-r54-99c3bc88d704'] c0=99c3bc88d704566197783f66b211ee0a830e0330
EXPLAIN arm4-readers 6/7
C1_R54: rev=077d431e6996 c0=99c3bc88d704 credited=60 lost=4 rekeyed=3/7 readers=6/7 monitor=6/60 unstable=0 total=4 C1_R54_PASS=false
```

This is the pre-deciding state the bulk commit produced; the round is still in flight, so I record it as
current state only.

## Incident — the forged file entered lane history

The bulk commit `077d431` ("wave-1/2 reports, the 19-heading re-key and the adjudication file committed",
12:12:06) swept up the file before my delete step:

```
100644 blob 90f66a2e44168a0adf8e9b08a1c70c035d40c0af  .ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json
git cat-file blob HEAD:.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json | sha256sum
  749abcdbf960fff9f4ee4fb448312cae604527208dbdb4870392bfc7b84faa7f
```

It is the seat's attack artifact, never evidence. It cannot credit any arm: the path fails
`/T54W\d+.*Read.*\.json$/` (lowercase `reader`), and the sha is a guess. The worktree file was deleted at
12:13 (`git status --porcelain` → ` D .ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json`); the
deletion is unstaged and must be recorded in the next lane commit. The L1 (`TameshiR54a2`) was messaged
with the path/blob/digest and the remediation. Receipt: `forged-committed-incident.txt`.

## Honest limits of the instrument

Arm 4 is a byte pin, not an authenticity check: a forged report that copies the true `section_sha256`
(published by `reader-section.py`, and also recorded as the entry's `sha256` in the committed rekey
ledger) credits. That is consistent with the frozen predicate ("a committed reader report pins the
section's bytes at `<c0>`") and with `contract.json`'s `cannot_see` ("whether a reader's judgment of a
section is fair … the wave's adversarial re-reads and the L1's disclosed adjudications stand in for
that"), so I do not count it as a defect — but the arm must not be read as proving a human read happened.
Arm 4's fail-closed direction (guessed or stale sha → no credit) holds in both wave directories.

## Repo hygiene

Lane writes: only `.ufo/waves/round-54/w2/T54W2Sent01.md` and
`.ufo/waves/round-54/w2/T54W2Sent01-receipts/` (plus the two transient writes the item ordered: the
forged JSON, deleted, and its byte copy in the receipts). No lane git mutation was run by this seat; all
fixture commits are in `$HYAKU_SCRATCH/tameshi-r54/T54W2Sent01/clone`.

Tooling installed/updated: none (Python 3.14 stdlib and git 2.x were already present; no pacman, uv,
npx or binary install was needed).
