# FRoute02 — falsification of Route02 (R18-2 append-only correction, S008 queued vs mined)

Seat: TameshiR19-2.FRoute02 (advisory leaf, w2, 2026-10-21). Read-only: plain git/awk/grep/sha reads
only; measure.py NOT executed (bound); no installs; no production edits; only this report written.
Axes: revision-transfer of Route02's strongest assertion to delivered C1 rev 55e1d312; frozen-harness
conjunct fidelity vs its characterization; arithmetic/attribution reproduction.

## 1. Strongest material assertion (Route02 §2-§3.1)

Commit 21e79329f8bdcf01a62be63b3e46db4a7de6b6f9 appends exactly 12 lines (numstat 12 0) forming
`## Erratum R18-2` on corpus/knowledge/mutation-case-kumitate-sources-check.md, satisfying every
frozen measure.py::source() conjunct, so R18-2 reads corrected; its flagged residual was an
uncommitted worktree entry delta, "not evaluated".

## 2. Verdict: AGREE, with revision-transfer sharpening — assertion survives at 55e1d312

Route02's numbers are stale by construction (pre-delivery observation); the delivered C1 revision is
55e1d312c4e8ac67aefad80099bd27581ff805c9. Re-verified there, 2026-10-21:

- Numstat 7243e7f→55e1d312 -- entry = `18 0` (not 12 0). The delta landed as commit 7af123b
  "round-19: harden correction predicates and preserve current-monitor provenance", appending
  exactly 6 lines (entry lines 278-282 `R18-2 sweep addendum` + blank). Deleted=0 at both hops:
  append-only holds across the transfer (in-place edits would show deletes).
- Line 1 byte-identical at 7243e7f, 21e7932, index, and 55e1d312: sha256 bc99d4b17c268deabb956d
  8283cf2222b3a65157feb913f0fe752cf9f4bedf38 (observed each). `**queued**`/`not yet a mined row`
  retained pre-anchor — the harness's hard requirement.
- Anchor `## Erratum R18-2`: count 1 in blob at 55e1d312 (line 266); addendum (278) is inside the
  note region (everything after first anchor) and adds no conjunct violation.
- Registry at 55e1d312: exactly one `| S008 |` row, 13 cells, cell-9 `mined`, cell-10 `2026-10-19`,
  cell-12 used-by names the entry (split-index 8/9/11 — exactly what source() checks).
- Grounding revision: at REV18 4b7c6823a462f5ea2eafcb262275300a545f3ed7 the S008 row is
  mined/2026-10-19/used-by — the erratum's named revision is accurate (observed).
- Note content (blob lines 268-270): "explicitly supersedes line 1's S008 `queued`" and at REV18
  "S008 is `mined`" — supplies `'line 1' in note and REV18 in note and 'mined' in note` (observed).
- Attribution pins Route02 cited re-verified: .ufo/evidence/round-18/final/audit-1905.stdout:21
  reads `OPEN …sha256=dd405bd36401…bytes=18779` exactly; baseline blob 18779 bytes ✓.

Conjunct-by-conjunct reproduction of measure.py::source() (read, not run): all return true at
55e1d312 ⇒ the frozen ruler reads R18-2=corrected at the delivered revision. Static reading only;
no suite executed, per bound.

## 3. Route02 mischaracterizations (minor, non-material)

- Implies the harness requires anchor uniqueness; source() uses split('## Erratum R18-2', 1) — only
  the FIRST occurrence matters. Uniqueness holds anyway (count 1).
- Its §3.1 couples "numstat 12/0" to frozen-harness satisfaction; source() never reads numstat.
  Append-only was its own C2 addition. Delivered 18 0 is harmless to the harness.
- Cited block line refs :267-268/:269-271 are off by one (supersession sentence is 268-269,
  grounding 269-271). Trivial.

## 4. Stale/missing-correction sweep at delivered revision (assignment item)

The 21e7932-era gap — entry lines 215-219 still asserted "S008 is `queued` with `used-by —`" — is
now superseded by the landed addendum (278-282), which names both stale descriptions (line 1 and
line 215) as historical. No R18-2 correction remains missing at 55e1d312. One wrinkle: the
addendum cites `w1/MetadataDraft.md`; that file exists (.ufo/waves/round-19/w1/MetadataDraft.md,
observed) but is a wave artifact, not corpus-relative — durability nit only, attribution not false.

## 5. Concrete falsifier

Any one of these, if observed, defeats §2: (a) `git diff --numstat 7243e7f… 55e1d312… -- <entry>`
showing deleted>0; (b) `git show 55e1d312…:<entry>` line 1 sha256 ≠ bc99d4b1… (loses `**queued**`
pre-anchor); (c) S008 row at 55e1d312 not unique/13-cell or ≠ mined/2026-10-19/used-by; (d) erratum
not naming REV18 4b7c6823… where registry is already mined. None observed. (L1's authoritative run:
`python3 .ufo/evidence/round-19/measure.py --repo <lane> --rev 55e1d312… --check` expecting
R18-2 corrected; not run here.)

## 6. Residual unknowns

- HEAD has advanced to e7039fdb with 70 dirty paths; verdicts here are pinned to 55e1d312 per the
  frozen-build rule. Harness `--rev` mode reads via `git show rev:path`, so L1's later run at the
  final tip is revision-exact — no drift risk from my stale-worktree basis.
- P-R18-2's C1 pins opened=2026-10-19; the frozen ruler independently pins it immutable
  (selftest case `immutable-opened`, 2026-10-21). Consistent, not contradictory.
- Nothing in scope contradicts C1's numeric calibration 8; no new coverage or cold-read claim found
  in the correction or its addendum.
