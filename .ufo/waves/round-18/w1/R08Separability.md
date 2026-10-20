# C1 / C2 separability review

Axes: **depth (C1, scored)** and **operability (C2, monitored/unscored)**. Scope: committed tree `183f87b899e6cae46be98d251cbc87fb5118f6ca`, inspected in a `/tmp` clone. No lane code was changed. The requested revision predates `.ufo/evidence/round-18/defect-probes.py`, so its wrapper cannot be audited from that tree; probe behavior below is limited to Contract A and the existing owning tools/selftests.

## Finding — C2's registry no-harm result is coupled to C1 (one-way)

C1's SCORECARD command D is a comment-ledger count: `SCORECARD.md:72-73` runs a regex over `git show "$REV:tools/mutate-and-run.sh"`. At the requested revision, the exact command returned exit 0 and `recorded_cases=7 depth_score=7`. The runner's seven baseline legs and their pinned replay behavior are in `tools/mutate-and-run.sh:84-89, 1236-1280`; its regression exit is based on the per-leg tables (`:1144-1152, 1291-1311`). The implemented regression path contains no registry reference (literal search of `tools/mutate-and-run.sh` for `registry` returned no matches); it materializes the listed sibling-repo targets and runs their suites. Thus neither command D nor C1's `--regression` reads `tools/registry.json` or invokes the C2 tools.

The reverse edge is real in C2's registry monitor. `tools/registry.json:384-423` defines two **active** rows:

- `mutate-and-run-selftest` → `bash tools/mutate-and-run.sh --selftest`, expected exit 0, timeout 180s (`:384-402`);
- `mutate-and-run-regression` → `bash tools/mutate-and-run.sh --regression`, expected exit 0 and stdout containing `REGRESSION: PASS`, timeout 900s (`:406-423`).

For `--rev`, `tools/registry-check.py:1252-1299` clones the requested revision, defaults the registry to that clone's `tools/registry.json`, and evaluates it. `evaluate()` runs the selected rows (`:517-540`) and returns exit 0 only if every active row is held (`:541-551`). A runner regression mismatch/setup error can therefore make its registry row fail; a timed-out row is explicitly unheld (`:382-393`). Consequently, the C2 **registry no-harm** result (`registry-check.py --rev REV --json`) re-executes both C1 runner checks. If the new C1 leg or its updated selftest/table is incorrect, C2's aggregate “stays held” result can fail even when all P01-P11 defect probes close. This is a one-way measurement dependency, not evidence that the defect-probe count itself is contaminated. Registry output retains per-row results, so attribution is possible, but the aggregate C2 no-harm claim is joint with C1.

## Probe/selftest boundary; no reverse dependency found

The distinction is between `registry-check.py --selftest` and the full registry evaluation. The selftest's `row()` helper creates argv `[sys.executable, "-c", code] (`tools/registry-check.py:620-637`), with scratch registry data; its fixture rows do not call the runner. Likewise, the existing `bash-witness-study.py --selftest` uses a synthetic runner string (`:1230-1251`), while its active registry row is `count`; `cmd_count` checks frozen evidence/summary rows (`:1041-1115`) rather than invoking or pinning the live runner. The actual runner launch in that tool is in its operational sweep path (`:594-606`), not the registered `count`/`selftest` paths. The trace collector selftest is scratch-fixture based (`.ufo/evidence/round-17/coldread/trace-inputs.py:702-703`) and a literal search found no `mutate-and-run` reference. `evidence-disposition.py` states that it never executes receipt argv (`:174-175`), and its selftest invokes only its own CLI via subprocess (`:2081-2105`); a literal runner search found no reference. These source checks support no runner call from the existing owning selftests; the future round-18 probe wrapper is absent at this revision.

## Exercised evidence

- `git show 183f87b899e6cae46be98d251cbc87fb5118f6ca:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'` — exit 0; `recorded_cases=7 depth_score=7`.
- Registry JSON census via Python — exit 0; 29 rows, including the two active `mutate-and-run-*` rows above. `tools/registry-check.py:541-551` confirms all active rows contribute to the aggregate held count.
- Materialized `kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs` in `/tmp`; SHA-256 was `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`. One `node ... --selftest` run exited 0 with `SOURCES_SELFTEST: 46/46 pass` (0.683s). This confirms the pinned target's per-run selftest scale, not the full eight-leg regression duration or the final registry outcome.
- No LSP device/status route was exposed in the supplied tool inventory; literal source searches were used only as a fallback, not as semantic proof. The positive coupling finding is grounded in the row argv plus registry-check execution/aggregation code above.

## Residual risk / verification gap

I did not run the full registry check or full `--regression`; this was a static separability review at the requested revision. The final `defect-probes.py` implementation and final post-landing registry result are not present at this revision, so the exact eventual probe subprocess graph and whether every C1 registry row remains held still require review at the landing revision. No independent evidence shows that C1's regression reads C2 inputs.

**Verdict: falls — C1 and C2 are only partially separable: C1 does not depend on C2, but C2's registry no-harm measurement re-runs C1.**
