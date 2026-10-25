# CriticSeparability — causal separability of C1 (calibration) and C2 (depth), round 42

**Verdict.** Coupling is **one-directional and textual**: C1's pass depends on C2's
files being committed (via m8, exactly the round-41 one-way coupling), while C2's pass
depends on nothing C1 lands. No C2 file is audited by C1's m10 or m11. Landing order that
keeps each verifiable without the other: **land all C2 deliverables first, then C1's
records + superseding receipt, decide both at one final revision** (details in §4).

---

## 1. Findings

### F1 — C1 m8 makes C1's pass depend on C2 files being committed (YES)

Mechanism: m8 extracts backticked repo-relative path tokens from the six records (the
round-41/42 lesson, SCORECARD sections, LOG sections) and requires each to resolve via
`git cat-file -e REV:<path>` (`.ufo/evidence/round-42/calibration/measure.py:109-110,244-247`,
`path_tokens` :162-172). The counter never opens a C2 artifact; the dependency lives in
the record text.

Representative round-42 records citing the contract's own C2 paths (v4 tool, census
counter, mutants.json, knowledge entry) were simulated in scratch clones under
`/tmp/tameshi-r42-CriticSeparability-{a,b}` (deleted after the runs):

- **SIM A** — records cite C2 paths, C2 files absent:
  ```
  MISMATCH m8 corpus/knowledge/r42-attribute-and-outflag-destinations.md cited in corpus/lessons/round-42.md does not resolve
  MISMATCH m8 tools/write-path-census-v4.py cited in corpus/lessons/round-42.md does not resolve
  MISMATCH m8 tools/write-path-census-v4.py cited in SCORECARD.md ## Round 42 does not resolve
  MISMATCH m8 .ufo/evidence/round-42/census/mutants.json cited in LOG.md ## 2026-10-25 — round 42 does not resolve
  MISMATCH m8 tools/write-path-census-v4.py cited in LOG.md ## 2026-10-25 — round 42 does not resolve
  C1_R42: self_pin=1 m6=0 m7=0 m8=5 m10=0 m11=0 total=5 records=6 sources_rows=109 … C1_R42_PASS=false
  ```
  m10 was already cleared by a superseding receipt in the sim; the only remaining failure
  is m8 on C2-owned paths. So C1 cannot pass while records cite C2 paths and those files
  are uncommitted.
- **SIM B** — identical records, C2 files present (stubs at the same paths):
  ```
  C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=109 … C1_R42_PASS=true
  ```

Baseline at the freeze commit (allowed rev, `322b5cd…`) confirms the counter itself is
healthy: `m6=0 m7=0 m8=0 m10=1 m11=0 total=1 records=3` — the only mismatch is the known
m10 residual receipt, and round-41 records are otherwise clean.

### F2 — no C2 file is audited by C1 m10 or m11 (NO)

- **m10** walks tracked JSON under `.ufo/waves` looking for `report`/`path`+`present`
  pairs (`receipt_audit`, measure.py:175-221). A full scan of every tracked JSON in
  `.ufo/waves` finds exactly one file with such pairs: `.ufo/waves/round-41/residual/receipt.json`,
  asserting 8 paths — all round-41 wave reports (`.ufo/waves/round-41/residual/*.md`).
  None is a C2 file (v4 tool, census counter, mutants.json, knowledge entry are not
  report paths in any receipt). The round-42 receipts will assert seat reports, not tools.
- **m11** ranges over 40-hex revision citations inside the six records
  (measure.py:249-257). C2 files are never records; m11 can only see a C2 *commit hash if
  a record cites it, which is a citation check (reachable from REV / fleet commit), not an
  audit of a C2 file.

### F3 — C2 is unconditionally independent of C1's files (confirmed)

Sim C: deleted `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`, `corpus/lessons/round-41.md`
from a scratch clone; C2 counter output is byte-identical to the freeze baseline:
```
C2_R42: tool_absent=1 v3_sha_ok=1 v2_sha_ok=1 live_unflagged_v3=3 rev=… freeze=322b5cd… C2_R42_PASS=false
```
C2 consumes only its own artifacts (`tools/write-path-census-v4.py` absent ⇒ `tool_absent=1`,
v3/v2 SHAs, `mutants.json`, FIXTURES, LIVE sites) plus the frozen contract pin and the
lane's `tools/*.py` — never SCORECARD/LOG/lesson/SOURCES/receipts. C1 lands nothing under
`tools/`, so C2 cannot even be perturbed by C1's artifacts.

### F4 — secondary coupling: m7 ties C1 to the registry landing (shared ground, not a C2 file)

Round-42 records will cite adopted S-ids (S155/S156/S157, incl. the C2-sourced S157
argparse row); m7 (measure.py:236-243) requires those rows present with status `mined` in
`corpus/SOURCES.md`. This couples C1 to the assimilation/registry batch that lands with
C2's knowledge entry — a shared-registry dependency, not a dependency on any C2 *file*.

---

## 2. Counterexample tested (strongest available)

The claim under attack: “C1 and C2 are causally separable — each verifiable without the
other.” Counterexample = SIM A: leave every C1 artifact intact, withhold only C2's files,
and C1 falls to `total=5` with every mismatch on a C2-owned path. The fix (SIM B: commit
the C2 files) restores `total=0`. So the pair is *not* separable in the C1←C2 direction;
it is separable in the C2←C1 direction (SIM C). The coupling can only fail C1, never
manufacture a pass for either claim.

## 3. Commands used (all permitted; no default-mode deciding run at the lane tip)

- `python3 .ufo/evidence/round-42/calibration/measure.py --lane <lane> --rev 322b5cd32b4319a05340d249ae752d12a9e6b19f --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f` → `m10=1 records=3` (baseline).
- `python3 .ufo/evidence/round-42/census/measure.py --lane <lane> --rev 322b5cd… --freeze 322b5cd…` → `tool_absent=1 live_unflagged_v3=3` (baseline).
- Scratch clones: `git clone --shared <lane> /tmp/tameshi-r42-CriticSeparability-{a,b,c}`, local commits only; deleted before return. No tools installed or upgraded.

## 4. Landing order that keeps each verifiable without the other

1. **Land C2 deliverables first**: `tools/write-path-census-v4.py`, `.ufo/evidence/round-42/census/measure.py`, `.ufo/evidence/round-42/census/mutants.json` (and the verified fixtures/controls), `corpus/knowledge/r42-attribute-and-outflag-destinations.md`, plus the SOURCES rows S155–S157 (status `mined`).
2. **Then land C1's records**: round-42 lesson, SCORECARD `## Round 42` section, LOG `## 2026-10-25 — round 42` section, and the superseding receipt for the round-41 residual receipt (must re-assert all 8 residual paths with tree-consistent values; otherwise m10 stays, selftest T2_*).
3. **Decide both counters at the final measurement revision containing everything** — C1 then passes if its records are clean (m8 resolves), and C2 passes iff v4 genuinely works. C2 may also be decided earlier (right after step 1), since it reads nothing C1 lands. Deciding C1 *before* step 1 fails with m8 (SIM A).

Carry-forward rule from round 41 (§6 of `.ufo/waves/round-41/w1/CriticCausalSeparability.md`):
every backticked path cited in records must be **committed** at the measurement REV, not
merely on disk — `resolves()` uses `git cat-file` at REV.

## 5. What I could not check

The actual round-42 record text does not exist yet (the lesson file is absent and wave 1
is in flight), so SIM A/B used representative citations matching the file names the
contract itself names for C2. If the scribes choose to cite C2 paths that differ from
these, the m8 mechanism (not the specific counts) still applies.
