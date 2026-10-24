# Mutation probe — r37 append-only correction marker (C1 calibration)

Round 37, wave 1. Leaf member; no subagent dispatch. Live lane checkout was read-only throughout.

## Target and detector

- Behavior-bearing point: the literal erratum heading checked by the r37 calibration counter.
  - `.ufo/evidence/round-37/calibration/measure.py:9`
    `ERRATUM_MARKER = "### Round 36 control-input erratum (round 37)"`
  - `.ufo/evidence/round-37/calibration/measure.py:48` `correction = ERRATUM_MARKER.encode() in scorecard`
  - `.ufo/evidence/round-37/calibration/measure.py:90` `old_unresolved_superseded = old_commit.returncode != 0 and correction and manifest_ok and receipts_ok`
- Detector (unchanged, bounded, three-phase):
  `python3 .ufo/evidence/round-37/calibration/measure.py --lane <COPY> --rev <REV>`
- Mutation: delete exactly the 1-line marker heading at `SCORECARD.md:1778`; the erratum body prose, the other two r37 errata, and every commit object stay identical.

## Baseline (pristine)

Lane `HEAD = e6185d5f0b63a6963205110cb098f2f1eca27622`, worktree clean for tracked files.
`SCORECARD.md` blob `d359a8ba6a8684081bc8816ec77df9dec1b07674`, bytes
`sha256=a5d6f2fddee51732594fb759bd6680283714157453d8c07e0e0a902a28929e6f`, marker count 1.

```
$ python3 .ufo/evidence/round-37/calibration/measure.py --lane . --rev HEAD
C1_R37: unresolved_control_inputs=0 old_mutant_resolves=0 correction=1 manifest_ok=1 receipts_ok=1 rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C1_R37_PASS=true
exit=0
$ python3 .ufo/evidence/round-37/calibration/measure.py --lane . --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d
C1_R37: unresolved_control_inputs=1 old_mutant_resolves=0 correction=0 manifest_ok=0 receipts_ok=0 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R37_PASS=false
exit=1
```

Disposable copy built by object fetch (same commit ids, no lane write):
`git init /tmp/r37-marker-mutant && git fetch <lane> HEAD && git checkout FETCH_HEAD` →
`copy_head=e6185d5f0b63a6963205110cb098f2f1eca27622`, identical blob/bytes, clean status.
Pristine-copy control run at `e6185d5` also `C1_R37_PASS=true` (copy integrity, not lane state).

## Mutation 1 — marker removed in a child commit (history untouched)

```
$ git diff --numstat        # mutant worktree vs e6185d5
0	1	SCORECARD.md
mutant_rev=7dfd52aeb0d9cc0a5b39da354fe0a1eb3d41ceb0
parent=e6185d5f0b63a6963205110cb098f2f1eca27622     # pre-existing commit hashes unchanged
mutant_bytes_sha=e812055862e06a94e42f7c290480d3aab0b8330fc1f5e2cfcff9ec3c50010261
$ python3 .ufo/evidence/round-37/calibration/measure.py --lane /tmp/r37-marker-mutant --rev 7dfd52aeb0d9cc0a5b39da354fe0a1eb3d41ceb0
C1_R37: unresolved_control_inputs=1 old_mutant_resolves=0 correction=0 manifest_ok=1 receipts_ok=1 rev=7dfd52aeb0d9cc0a5b39da354fe0a1eb3d41ceb0 C1_R37_PASS=false
exit=1
```

## Mutation 2 — same commit id, marker-only tree (strict "commits identical")

Replacement ref in a second disposable copy maps `e6185d5` to a synthetic commit with the
same tree except `SCORECARD.md`, same parent `034fa2a`; `git rev-parse HEAD` still returns `e6185d5`.

```
mutant_blob=3db2196d8e81a2afd6160db4ec502468900d736a
mutant_tree=e639e89dddf276f208f46da8881fe89f1fb31354
synthetic_commit=8fafb820e3ab19aa3496430ec25b43d00514b037
resolved_rev=e6185d5f0b63a6963205110cb098f2f1eca27622
replaced_bytes_sha=e812055862e06a94e42f7c290480d3aab0b8330fc1f5e2cfcff9ec3c50010261
no_replace_bytes_sha=a5d6f2fddee51732594fb759bd6680283714157453d8c07e0e0a902a28929e6f
$ python3 .ufo/evidence/round-37/calibration/measure.py --lane /tmp/r37-marker-samecommit --rev e6185d5f0b63a6963205110cb098f2f1eca27622
C1_R37: unresolved_control_inputs=1 old_mutant_resolves=0 correction=0 manifest_ok=1 receipts_ok=1 rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C1_R37_PASS=false
exit=1
```

## Verdict

**KILLED — the marker is load-bearing.** In both mutants `manifest_ok=1` and `receipts_ok=1`
(the committed empty-panel spec at `.ufo/evidence/round-37/control/empty-panel/manifest.json`
and the `replay-at-final-control.stdout` receipt still resolve), yet `correction=0` alone forces
`unresolved_control_inputs=1` → `C1_R37_PASS=false`, exit 1. The heading string is the sole
differentiator, not redundant with the substantive evidence.

Coverage observation (not a contract change): the gate is one literal SCORECARD.md heading.
Deleting only that line while retaining the full erratum body and every commit flips the verdict,
so the correction term evidences prose presence, not a machine-checkable supersession record.
Whether that suffices is a reviewer/contract question.

## Restoration evidence

- Mutation 1 copy, revert commit `1f8c035b44a3500558648ab69cda9facb16af0c4`:
  `restored_blob=d359a8ba6a8684081bc8816ec77df9dec1b07674`,
  `restored_bytes_sha=a5d6f2fddee51732594fb759bd6680283714157453d8c07e0e0a902a28929e6f`,
  `git diff --stat e6185d5 HEAD` empty, status clean →
  `C1_R37: ... correction=1 manifest_ok=1 receipts_ok=1 ... C1_R37_PASS=true`, exit=0.
- Mutation 2 copy: `git replace -d e6185d5…` → `replace_refs=[]`, bytes `a5d6f2fd…` →
  `C1_R37_PASS=true`, exit=0.
- Live lane after all runs: `HEAD=e6185d5f0b63a6963205110cb098f2f1eca27622`,
  `HEAD:SCORECARD.md=d359a8ba6a8684081bc8816ec77df9dec1b07674`, bytes `a5d6f2fd…`;
  tracked-status empty (only sibling scout reports untracked). No lane index, `.git`, `jj`,
  `.ufo/state`, or source-tree write by this probe.

Scratch dirs `/tmp/r37-marker-mutant` and `/tmp/r37-marker-samecommit` are disposable and outside
the lane. No tool installs or updates were performed.
