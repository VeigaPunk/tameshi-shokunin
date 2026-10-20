# LessonScribe — round-12 lesson outline (findings)

Seat: LessonScribe (scribe, leaf). Wave: tameshi-r12-w1. Lane: tameshi-shokunin. Advisory, lane-internal; not independent promotion, admission, or outside authority.

## Result

A draft round-12 lesson outline is written with: a Gate section (sourced claims G1–G4, rejected inferences R1–R3), a Mistakes table extending MK-1…MK-11 with four candidate rows (MK-12…MK-15), a status old→new table for the registry, and a reflection on the prior outside verdict. The outline is **not** the lesson. Nothing is marked passed, landed or independently verified.

## What the outline says (short)

- **C1 and C2 are not yet measured.** `tools/repeat-control.py` is absent; BashWitness output is absent. Both claim lines stay `[PENDING]`.
- **Sourced now (quote present in repo):** S006 baseline verdict; S011 repeated-execution variance; S026 rerun-rate figure; S028 "stdout PASS/FAIL has no significance"; S040 flaky definition.
- **Sourced but unquoted (blocked):** S004 "tests must first pass reliably" (registry `teaches` only); S026 fail-3-in-a-row (`teaches` only).
- **Rejected inference R1:** "N identical green runs prove determinism." Finite sample, flip condition stated. S040 is not attributed with an answer to the rerun question; that is SourceSurvey's to capture.
- **R2:** N=3 is a lane choice matching S026's mitigation convention, not a sourced threshold.
- **R3:** byte-identical stdout/stderr is a lane policy; S028 says exit code decides.

## Prior outside verdict — reflected

Read: reviewer (`.ufo/waves/kaika-w3/tameshi-review.md`, admit with conditions, pin 8), critic (`tameshi-critic.md:11`, reject K1), orchestrator adjudication (`corpus/lessons/round-1.md:474-487`, K1 rejected, pin 6), spot-check (`corpus/lessons/round-1-verifier-spotcheck.md`, discernment "improved").

Disagreements recorded, not smoothed: D1 box-3 increment (lane admitted, critic rejected); D2 discernment token (`improved` vs `unprovable-but-better`, both committed, unreconciled); D3 pin 8 vs 6; D4 whether an orchestrator-dispatched reviewer is outside (`[U]`). The spot-check sample excluded the contested admit (MK-13). Recommendation on D2 is labelled opinion.

## Status fields (old → new)

Committed `18ad5d0`: S004 mined; S006 mined (2 used-by); S011, S026, S028, S040 queued (used-by `—`). Each proposed change is conditional on a knowledge file landing with a `source:` header.

**Risk, not mine to fix:** the worktree `corpus/SOURCES.md` (uncommitted, a sibling's edit) already flips S026 to `mined` with used-by `corpus/knowledge/repeated-control-precondition.md`, which does not exist at capture. The contract census `missing:` check will fail until it lands. S006's worktree used-by adds `corpus/lessons/round-12.md`, which exists only uncommitted. I did not edit either file.

## Risks

1. Worktree registry mid-edit: premature `mined` flip; census fails until the knowledge file lands.
2. `corpus/lessons/round-12.md` exists uncommitted; the outline may diverge from it. L1 reconciles; I did not read or edit it.
3. S004 and S026 verbatim quotes absent from repo; G1 and G3 blocked until captured.
4. S028 vs C1 byte-identity: tension if C1 is framed as a source requirement.
5. `S047` id collision if more than one seat allocates (`corpus/SOURCES.md:133`); only L1 should allocate.
6. Baseline ambiguity: my "old" values are committed `18ad5d0`; worktree differs. L1 must choose one baseline before logging a change.
7. `opened` semantics on seat re-opens are silent in contract v1; left unchanged, flagged `[U]`.

## Exact owned paths (written by this seat)

- `.ufo/evidence/round-12/LessonScribe/outline.md` — the draft outline (sha256 in the write receipt).
- `.ufo/evidence/round-12/LessonScribe/capture.txt` — read-only captures: HEAD, sha256s, committed vs worktree registry rows, used-by existence, anchors, quote presence.
- `.ufo/waves/round-12/w1/LessonScribe.md` — this report (new file; no other report overwritten).

Not written: `corpus/lessons/round-12.md`, `corpus/SOURCES.md`, `corpus/knowledge/*`, `LOG.md`, `SCORECARD.md`, `tools/*`, any sibling's evidence directory.

## Tools

None installed or updated. No network access performed; every quote above was taken from repo files or the sibling's captured round-1 record, and cited by path.

## Checks not run (for the main agent)

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` — after the worktree settles.
- `grep -n discernment corpus/lessons/round-1-verifier-spotcheck.md SCORECARD.md LOG.md` — to confirm D2 is still two tokens.
- `python3 tools/repeat-control.py --selftest` — only after the gate file lands; the outline does not depend on it passing.
- Re-verify S004 and S026 verbatim quotes by re-opening the canonical URLs (ControlKnowledge / SourceSurvey lanes own that).

## Unknowns

- Whether an orchestrator-dispatched verifier counts as outside (D4).
- Whether any finite-rerun source exists that answers the determinism question directly (SourceSurvey's capture).
- Whether the fleet `LEARNING.md` rule on outside verdicts is the one applied in the round-1 spot-check (not in this repo).
