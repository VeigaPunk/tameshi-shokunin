# T57W3Read14 — cold-read certification

## Scope and result

Heading: `## Live-tree re-pin and entry-command monitor — round 17`.
Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`.
Frozen round-18 `sectionize` returns **1857–1888**, SHA256
`6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac`.
Read end to end from a shared scratch clone detached at that candidate.
Axes: section truth, runnable recipes, pointer integrity, immutable evidence.

**Recommendation: verified-record. No false section statement or unexpected recipe outcome found.** This is section certification, not admission or a claim that every registry row holds.

## Executed sweep

Full commands, working directory, exit status and unabridged output are in the adjacent `T57W3Read14-receipts/command-N.json` files; the JSON report indexes all twelve.
All tool, manifest and Git paths in actual invocations were absolute. Recipe-relative paths below describe the equivalent clone-root invocation.

| Receipt | Command / scope | Observed output |
|---|---|---|
| 1 | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json` | exit 1, `status: failed`, `expectation: producer_before`, expected_contains_missing |
| 2 | same with `.ufo/evidence/round-18/dispositions.json` | exit 0, clean, effective 11, superseded 1 |
| 3 | same clean manifest, text mode | exit 0, three HISTORICAL lines, one each for bash-witness-study.py, mutate-and-run.sh, pin-disposition.py |
| 4 | `python3 tools/registry-check.py --rev adf87899c70d616140a81185a8f9acbbdfb30392` | exit 1, held=49/53 superseded=7 before sibling symlinks were supplied |
| 5 | same replay with `--json`, after read-only sibling symlinks | exit 1, held=51/53 superseded=7; sources-census and verify-round15 differ |
| 6 | `python3 tools/evidence-disposition.py --selftest` | exit 0, `SELFTEST: PASS (66/66)` |
| 7 | `git -C <absolute clone> rev-parse --show-toplevel` | exit 0, exact scratch clone path |
| 8 | `git -C <absolute clone> show refs/remotes/origin/master:tools/pin-disposition.py` | exit 0, 60304 characters of committed tip source |
| 9 | importlib loads the lane's frozen round-18 measure.py; `git -C <absolute lane> show <C0b>:SKILL.md`; calls `m.sectionize(raw)` | exit 0, `1857 1888 6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac` |
| 10 | local pointer/source-ID sweep (exact Python command retained) | exit 0, every named file and S061/S062/S063 RESOLVES |
| 11–12 | both round-17 disposition manifests, JSON | exit 2, expected_input_digest_mismatch for moved bash-witness-study.py, as the section states |

The nonzero before/round-17 outcomes are the advertised results, not failures of the recipe. Registry exit 1 is explicitly defined by the section when a row differs; no all-green result or fixed N/M is promised.

## Claim and pointer review

- `corpus/lessons/round-16-verifier-spotcheck.md` §3 and §6 resolve and identify the operability harm, R16-OP1 and R16-MON1.
- `tools/evidence-disposition.py:385–395,406–420` set replacement/graft overrides and scrub Git environment before invoking Git. `:479–544` implements the exact branch/bound/detached anchor distinction cited by the section. `:620–652` rejects unneeded/uncommitted waivers. `:2790–2956` declares the cited provenance and replacement/environment controls; all ran in receipt 6, including the cited `:2910–2915` detached-anchor selftest.
- The fixture docstring at `:2275` says detached harness clone anchors at HEAD, not its later remote tip. Historical manifests pin ancestor bytes and the observed three HISTORICAL lines reproduce those pins.
- `tools/registry-check.py:149–165,648–730,774–838` corroborates scrubbed row execution, differing-outcome classification, and detached replay cloning with sibling symlinks. Superseded rows appear in both replay outputs and still run.
- `tools/mutate-and-run.sh:1253–1265,1924–1945` implements the repository-identity guard and its regression selftest. The registry replay holds mutate-and-run-selftest and, after sibling setup, mutate-and-run-regression.
- `tools/bash-witness-study.py:354–369` scrubs inherited Git variables; `tools/pin-disposition.py:226–238` does likewise, and its head rows retain branch/head_differs_from_branch. Registry holds their selftests.
- Primary references resolve: https://git-scm.com/docs/git-rev-parse and https://docs.jj-vcs.dev/latest/git-compatibility/ . S061's historical paragraph-anchor correction remains recorded by S076; this section does not reproduce the stale paragraph number.
- Related SKILL references at 1624–1628, 1644, 1724, 1893–1896 and 1974–1975 consistently identify round-18 as the live manifest and round-17 as superseded.

## Residual risk and verification gaps

The registry is **not all green**: sources-census and verify-round15 differ at C0b. Receipt 5 retains their outputs and missing marker. This is an observable residual operability issue, not a contradiction of this section's documented exit-1 behavior. No claim of whole-tree certification follows from this seat.

`xd://lsp` is unavailable (No such tool); literal searches and direct source inspection are fallback evidence, not semantic references. Grafts were code-read only, matching the section's disclosed limitation. No independent historical incident reconstruction was attempted. No resume, same-identity rerouting, or saturation claim appears in scope.

## Integrity and self-evaluation

No tool installs/upgrades; no lane content or frozen evidence edits; no staged fixes. Only assigned reports/receipts and private scratch were written. No subagents or alternate agent runtimes invoked.

Accuracy 4/5: exact commands/output retained; historical incident causality not independently reconstructed. Completeness 4/5: all section recipes and pointers covered; grafts remain code-only. Clarity 4/5: receipt indexing keeps long outputs out of prose. Actionability 5/5: complete receipt paths and row names identify residual issues. Conciseness 4/5: detailed claim mapping is retained for auditability. Overall 4.2/5. Improvement: separately investigate the two registry rows if broader operability is assigned. User-agreement self-check: the verdict is deliberately bounded to this section.
