# CriticCrossClaim — do C1 and C2 survive each other's removal?

Seat: `L1Tameshi41.CriticCrossClaim` (critic, read-only). The lane checkout was never written; all
runs happen in `/tmp/tameshi-r41-criticcross-*`. Only this report was written into the lane. No
tool was installed or upgraded (pacman untouched per the host-wide pause).

## Answer in one line

**Asymmetric, literal-path coupling.** C1 **fails** in a tree with the C2 tool and entry removed
(`m8=2`, exit 1); C2 **passes** with every C1 SCORECARD/lesson/LOG edit removed
(`C2_R41_PASS=true`, exit 0). The coupling is only through C1's class m8, which resolves the
backticked paths the round-41 *records* cite — not through any predicate. It is not fatal for a
single deciding revision where both land, but two live pre-run conditions must hold or C1 fails
while its own classes m6/m7/m9 are already clean.

## Exact inputs (they moved while I measured)

The worktree changed under every seat while this wave settled. I pinned a snapshot and re-ran the
same two experiments on the amended counters; the result is identical in both counter revisions.

| input | sha256 | note |
|---|---|---|
| `74c2388` "landed round-41 worktree snapshot" (copy of the live worktree, `git add -A`, committed in `/tmp/tameshi-r41-criticcross-live`) | — | includes C1 lesson/SCORECARD/LOG edits, S153/S154 rows (109 rows), C2 tool, snapshots, amended contract A1–A3 |
| `676f185` S0b = `74c2388` + current live `calibration/measure.py` + live `contract.json` overlaid | — | the state I ran C1 against |
| `tools/write-path-census-v3.py` | `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` | unchanged through the round |
| `census/measure.py` | `83268eff97048cd4223a6f015b901c5efbde15d7b0d506bd40e5611b373ce94c` | matches contract pin |
| `census/fixtures.json` | `20b6254d39a75fb9b09b783131a7cdcaf360c36642e39424343166515aa26329` | matches contract pin |
| `calibration/measure.py` A4 content | `8bc9b4221c59c7b380892b7f97885e9b8ada1f5d82b0703effa166f0519ce11c` | **== contract pin after A4** |
| `calibration/measure.py` on disk at 03:46:05-03:00 | `9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd` | **≠ contract pin** (see Finding 3) |

## Experiment 1 — C1 with the C2 tool and entry removed

Tree `/tmp/tameshi-r41-criticcross-live` at `676f185` (landed records intact). Then:

1. `rm tools/write-path-census-v3.py`
2. delete the C2 capability row `| write-path census destination resolution | ... |` from the
   SCORECARD round-41 block (the "entry")
3. commit → `6ac48f5`

Command (also re-run with the A4-pinned counter `8bc9b42` overlaid → `5758168`; same output):

```
python3 /tmp/tameshi-r41-criticcross-live/.ufo/evidence/round-41/calibration/measure.py \
  --lane /tmp/tameshi-r41-criticcross-live \
  --rev 6ac48f577f95f7b47ed5ac6f85e5ac2b87ba6cbf
```

stdout (verbatim):

```
MISMATCH m8 tools/write-path-census-v3.py cited but does not resolve at 6ac48f577f95f7b47ed5ac6f85e5ac2b87ba6cbf
MISMATCH m8 tools/write-path-census-v3.py cited but does not resolve at 6ac48f577f95f7b47ed5ac6f85e5ac2b87ba6cbf
C1_R41: m6=0 m7=0 m8=2 m9=0 total=2 records=3 sources_rows=109 rev=6ac48f577f95f7b47ed5ac6f85e5ac2b87ba6cbf C1_R41_PASS=false
```

exit `1`. The two m8 hits are the two *records* that still cite the path, not two paths:
`SCORECARD.md:1910` (C2 claim row) and `LOG.md:2120`. The cap-ability row removed at
`SCORECARD.md:1916` was the third citation. The lesson cites the tool zero times.

**Do-nothing control for the coupling itself — same tree, citations stripped** → `5495e333`:

```
C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=5495e3339dee8dde8490e7ee6477510092a67cc2 C1_R41_PASS=true
```

exit `0`. So C1's own classes (m6 count, m7 id status, m9 correction) do **not** need C2; only m8's
literal-path rule does, and it is load-bearing: the record must not claim an artifact that is not
in the measured revision.

## Experiment 2 — C2 with every C1 record edit removed, C2 landed

Tree rebuilt at `676f185`, then `SCORECARD.md` and `LOG.md` restored from
`d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937` (no `## Round 41` block, no round-41 LOG entry) and
`corpus/lessons/round-41.md` deleted → commit `8046850`. The C2 tool, fixtures, counters and
contract all present.

```
python3 /tmp/tameshi-r41-criticcross-live/.ufo/evidence/round-41/census/measure.py \
  --lane /tmp/tameshi-r41-criticcross-live \
  --rev 804685013c1a88212426727f756e6ddd78dd1929
```

stdout (verbatim):

```
C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1 var_expected=1 symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=0 v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=811 live_var_resolved_v3=1 live_var_scratch_v3=1 live_var_sites_v2=1 live_var_expected_v2=0 live_symlink_lineno=820 live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1 mutant_symlink_arg_killed=1 rev=804685013c1a88212426727f756e6ddd78dd1929 C2_R41_PASS=true
```

exit `0`. Same tree, C1 is `m6=1 m9=1 total=2 C1_R41_PASS=false` (records absent) — C2 does not
read one byte of C1's surface.

Evidence from the code: `.ufo/evidence/round-41/census/measure.py:25-29` is the complete read set
(`TOOL`, `V2`, `FIXTURES`, `CONTRACT`, `LIVE`) and `:151-154` is every `git show`; none of
`SCORECARD.md`, `LOG.md`, `corpus/lessons/` appears. `.ufo/evidence/round-41/calibration/measure.py:46`
(`PATH_PREFIXES`), `:181` (`path_tokens`), `:241` (m8 emit) is the whole of the C1→C2 edge.

## Findings, severity order

1. **C1 is satisfiable without C2, the round's records are not. `[HIGH for independence, not for
   the pass bit]`** The landed records cite the v3 tool (`SCORECARD.md:1910` in snapshot `676f185`,
   `:1911` after the 03:47 edit; `LOG.md:2120`) and the two source snapshots
   (`corpus/lessons/round-41.md:16`, `:20`). Under the contract's single
   measurement revision that is self-consistent. Read as "C1 verifies independently of C2" it is
   false: m8 makes C1 fail the moment the C2 artifact is absent. The claim text does not say C1 is
   independent, so the pass bit stands — but the round should state the edge, not let a reader
   infer separability.

2. **Snapshot citations: observed blocking, then discharged by the landing commit. `[was HIGH]`**
   At 03:46:05 `git status` showed `?? .ufo/evidence/round-41/sources/`; the lesson cites both files
   at `corpus/lessons/round-41.md:16` and `:20` and neither was in `git ls-files`. Receipt — same
   landed tree, tool present, snapshots removed from the revision → `c627e2c`:

   ```
   MISMATCH m8 .ufo/evidence/round-41/sources/ast.html cited but does not resolve at c627e2c...
   MISMATCH m8 .ufo/evidence/round-41/sources/pathlib.html cited but does not resolve at c627e2c...
   MISMATCH m8 .ufo/evidence/round-41/sources/ast.html cited but does not resolve at c627e2c...
   C1_R41: m6=0 m7=0 m8=3 m9=0 total=3 C1_R41_PASS=false
   ```

   `m8` resolves with `git cat-file -e REV:path` (`measure.py:111-120`), so only a committed
   snapshot counts. **Discharged:** landing commit `b37ce97` carries both files
   (`git ls-tree -r --name-only b37ce97 .ufo/evidence/round-41/sources/` → 2). The condition is
   still the requirement for any later revision: snapshots must be in the tree m8 reads.

3. **C1 counter pin: observed mismatched at HEAD, closed by the pending A5. `[was HIGH]`**
   At 2026-10-25T03:46:05-03:00 the disk counter was `9aaa99ac...` while
   `claims.C1.counter_sha256` was `8bc9b42...` (A4's pin). The extra edit derives the m9 expected
   words from the round-40 table instead of hardcoding `'six refused'` / `'ten present'`.
   **State now:** commit `b37ce97` commits counter `9aaa99ac` with contract pin `8bc9b42` — the
   committed claim's pin does not describe its committed counter. The worktree carries amendment
   A5 re-pinning to `9aaa99ac` (`git diff .ufo/evidence/round-41/contract.json`), so the next commit
   closes it. Do not name `b37ce97` as the measured commit while that mismatch is in it. The
   durable point stands regardless: **no code consults `claims.C1.counter_sha256`** — C1 does not
   hash itself and C2 pins only the tool — so the pin is enforced by a reader, never by the run.
   The L1's new instrument-limits paragraph in `SCORECARD.md` and the lesson's `## Holds (instrument
   limits)` now say this; it remains a disclosure, not a check.

4. **The before receipt and the after measurement are different C1 binaries. `[LOW]`**
   ExecC1Base's before run used `f00917dd` (freeze); A1 replaced m7's `cells[9]`→`cells[8]`, so the
   after run uses `5ccb42d8`/`8bc9b42`. I reproduced A1's defect independently on the frozen counter
   before A1 landed: two trees agreeing that any cited id read `status=2026-10-25` — e.g.
   `C1_R41: m6=1 m7=2 m8=0 m9=0 total=3` at `18afe638` and `m6=0 m7=2 ...` at `7ab83789`. The
   amendment is real; the counter changed *because* the rule stayed fixed. No predicate moved.
   (A3's lesson rephrase and A4's `exists`/slash fix are likewise rule-preserving.)

5. **Not a finding, resolved before this seat: m6 107 vs 109.** The wave plan's scorecard brief
   says "107 rows"; the round lands S153/S154, so the registry is 109. The landed
   `SCORECARD.md` standing row says `109 rows at round 41`, and C1 at `676f185` prints `m6=0
   sources_rows=109`. Had the brief been followed literally, m6 would have fired (`m6=1` at
   `18afe638`, before the row was corrected).

## Status when this report closed (2026-10-25T03:47:47-03:00)

- HEAD `b37ce97` — the landing commit: C1 lesson, SCORECARD round-41 block, LOG entry, SOURCES
  S153/S154, both snapshots, amended contract (A1–A4), amended C2 counter + fixtures.
- Uncommitted in the worktree: `contract.json` (A5 re-pin to `9aaa99ac`), `SCORECARD.md`,
  `corpus/SOURCES.md`, `corpus/lessons/round-41.md` (the instrument-limits disclosure).
- C1, run in the snapshot whose content equals the landed records with the currently pinned counter
  (`676f185`, counter `9aaa99ac`): `m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109
  C1_R41_PASS=true`, exit 0 — **with C2 present**.
- C2, run with every C1 record edit removed (`8046850`): `C2_R41_PASS=true`, exit 0.
- The L1's new disclosures (`SCORECARD.md` "C1's own instrument limits"; lesson
  `## Holds (instrument limits)`) cover the missing self-pin, m7/m8 vacuity and m8's path scope.
  They do **not** cover the cross-claim edge in Finding 1: that m8 makes C1's pass depend on C2's
  tool and on the scout snapshots being committed at the measured revision. That sentence is still
  the smallest correction this seat asks for.

## Impacted axes

- **calibration (C1)** — the pass bit is attainable only with C2's tool and the scout snapshots
  committed in the same revision; m8 is the single coupling surface, at
  `calibration/measure.py:46,181,241`.
- **depth (C2)** — unaffected: `C2_R41_PASS=true` with C1's whole record surface absent, including
  the amended third mutant (`mutant_symlink_arg_killed=1`).

## Smallest safe correction

Do not touch either predicate — m8 is behaving as specified, and C2's read set is already minimal.

1. **Snapshots + tool in the measured tree — done, keep it:** `b37ce97` already carries
   `.ufo/evidence/round-41/sources/` (2 files) and the v3 tool; any later commit that the deciding
   run reads must keep both (`git ls-tree -r --name-only REV .ufo/evidence/round-41/sources/` → 2).
2. **Close the C1 pin: done in the worktree, awaiting commit.** Amendment A5 re-pins
   `claims.C1.counter_sha256` to `9aaa99ac`, the committed counter's sha; commit it before citing a
   measured commit, so the claim's pin describes the bytes that ran (Finding 3). Optionally record
   the counter sha in the after receipt itself — the counter will never check it.
3. **One disclosure sentence** in the C1 lesson `## Holds` (or the contract's C1 `classes` for m8):
   "m8 resolves the round-41 records' own citations at the measured revision, so C1's pass requires
   the round's own census tool and opened-source snapshots to be committed there; this is a record
   consistency check, not evidence that C1 is independent of C2." That converts the hidden
   dependency in Finding 1 into a stated tradeoff, which is the honest reading of the two
   experiments.

## Scratch inventory (for re-running)

- `/tmp/tameshi-r41-criticcross-live` — `74c2388` landed snapshot, `676f185` S0b,
  `6ac48f5` tool+entry removed (`m8=2`), `5758168` same with A4 pin (`m8=2`), `5495e333` stripped
  citations (`PASS=true`), `8046850` C1 edits removed (`C2_R41_PASS=true`), `c627e2c` snapshots
  uncommitted (`m8=3`).
- `/tmp/tameshi-r41-criticcross-a` — earlier synthetic reconstruction against the freeze counter:
  `b15e8d8f` C1 pass with C2 present, `b2a02cde` tool+entry removed (`m8=2`), `fea7e698` tool
  absent/no citation (`PASS=true`).
- `/tmp/tameshi-r41-criticcross-c` — `18afe638` wave-plan-literal standing 107 (`m6=1`).
- `/tmp/tameshi-r41-criticcross-amend/` — pinned copies used for the diffs.

Report: .ufo/waves/round-41/w1/CriticCrossClaim.md
