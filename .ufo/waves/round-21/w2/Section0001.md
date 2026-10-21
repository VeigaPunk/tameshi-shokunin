partial

# Section 1 review — SKILL.md:1-5 (heading: empty)

## Finding

**Unverifiable current status — `Rank: shonen (probation)` (one blocking gap, zero proven wrong expectations).**

- `shonen` is supported at the pinned revision. `SHONEN.md:3` says promotion to shokunin requires every checklist item; current `SHONEN.md:5-12` has four `[~]` marks and no `[x]`. The checklist remains present, so the rank has not advanced to shokunin.
- The parenthetical `probation` is not established as a current state. The old CR01 report called `SCORECARD.md:4` corroboration, but that line says “Probation rounds 1-3 build the initial measurements”; it is historical, not a statement of current status. `LOG.md:3-4` records the mint and initial probation rule, and `LOG.md:173-174` calls round 3 “probation-completing.” Current fleet `PROTOCOL.md:48-52` says probation is recorded in `rounds[].notes` before the roster row is added. At fleet `master` revision `a28c80cc9a4047420124978a98ae1e5c16d935fc`, `MANIFEST.json:1710-1716` contains the dated round-0 mint note (“Probation >=3 verified rounds; roster row withheld”), and a roster query for `id == tameshi` or `repo == tameshi-shokunin` returns `[]`. That establishes the initial state and current absence of a roster row, but no current record says whether probation persisted after round 3. I therefore cannot certify the suffix; I do not count it as a known-wrong expectation.
- The domain description is accurate: `PROVINCE.md:3-5` defines the domain as “verification-fixture craft” and describes the reusable method. The addition to PROVINCE after line 69 (round-18 and round-21 append material) does not change those cited lines.

The assigned five-line section has no citation ranges or runnable commands, so there are no wrong ranges or obsolete commands in the target section. The previous CR01 finding was content-correct on the domain and shonen rank, but its use of `SCORECARD.md:4` as current probation evidence does not survive this recheck. Treat the “Probation rounds 1-3” statement as dated history, not current status.

## Invalidation and scope

The section text is unchanged: its trimmed frontmatter hash is `1e441b84d5ff7ad1f2c8b66daad304413cfd6157ac98b780279bfdc91d050d74`, matching `.ufo/waves/round-17/w2/CR01.md:3`. The affected-sections manifest records input drift in `PROVINCE.md` and `tools/trace-inputs.py`; the pinned-revision diff shows PROVINCE received later append-only content and `tools/trace-inputs.py` was added after the prior read. Those changes justify revalidation but do not contradict the target's domain or rank text. The current trace tool is provenance infrastructure, not an assertion made by SKILL.md:1-5.

This is a scoped source review, not a blind/independent cold-read and not the separate traced source re-anchor. No mutation recipe, test suite, or runtime check was executed.

## Commands and observed exits

- `git rev-parse HEAD` in the tameshi repo → `790abd2129f153c13b471e381d454186edbde65e` (0).
- `git show 790abd2129f153c13b471e381d454186edbde65e:SKILL.md` with lines 1-16 displayed → 0; the five-line frontmatter matches the assigned range.
- `git show 790abd2129f153c13b471e381d454186edbde65e:PROVINCE.md` and `:SHONEN.md` → 0; source lines cited above.
- `git diff --unified=3 eb7838b16490ca7ba17ea3242ade76a61f744af2 790abd2129f153c13b471e381d454186edbde65e -- tools/trace-inputs.py PROVINCE.md` → 0; showed append-only PROVINCE additions and the trace tool addition.
- Current pinned checklist counter → `boxes=4 checked=0 asserted=4 untouched=0` (0).
- `git diff --quiet eb7838b16490ca7ba17ea3242ade76a61f744af2 790abd2129f153c13b471e381d454186edbde65e -- SHONEN.md SCORECARD.md` → 1, expected: those source files changed. The current sources were inspected directly; round-21 changes do not establish a post-round-3 probation state.
- Fleet repo identity check → branch `master`, revision `a28c80cc9a4047420124978a98ae1e5c16d935fc` (0). Current manifest query for a tameshi roster entry → `[]`.

No tools were installed or updated. The residual gap is limited to whether the probation suffix remains current; the target's domain and shonen claims hold.