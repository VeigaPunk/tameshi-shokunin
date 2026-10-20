# S09 — Round-14 recipe steps 2–3, three ways (C2a red-before fact)

Seat: `TameshiR17.S09R14RecipeOutcomes` (scout, wave 1, round 17). Lane tip
read: `98bea7da5801f4bc58e4187690ee1687c8a5061f`. Date run: 2026-10-20.
Scope: execute the round-14 recipe steps 2–3 from `SKILL.md:1578-1586`
(step 2 at `:1581-1583`, step 3 at `:1584-1586`) under three roots and record
exits and finding IDs. No lane instrument was edited. Scratch root:
`/tmp/tameshi-r17w1-S09R14RecipeOutcomes-0Ps7UY` (ephemeral).

Commands under test (cwd = lane root; `--dispositions` path lane-relative):

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json   # step 2
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json          # step 3
```

## Outcome table (observed)

| Root | Step 2 exit / finding id | Step 3 exit / finding id |
|---|---|---|
| Live lane, `--root .` at `98bea7da` | **2** / `expected_input_digest_mismatch` | **2** / `expected_input_digest_mismatch` |
| `git archive 28aeef4` extracted to /tmp, `--root .` from that dir | **1** / `expected_contains_missing` (expectation `producer_before`) | **0** / clean, `findings: []` |
| Fleet-mirror clone at `28aeef4`, `--root .` from clone | **1** / `expected_contains_missing` (expectation `producer_before`) | **0** / clean, `findings: []` |

Matches the acceptance expectation (live 2/2; archived 1/0). The clone at
`28aeef4` reproduces the archive exactly.

## Evidence

| Fact | Command | Observed |
|---|---|---|
| Lane tip and pre-run tree state | `git -C <lane> rev-parse HEAD; git status --porcelain` | `98bea7da5801f4bc58e4187690ee1687c8a5061f`; only untracked dirs (`.ufo/evidence/round-16/__pycache__/`, `.ufo/evidence/round-17/`, `.ufo/waves/round-17/`) |
| Live step 2 | command above, cwd lane root | exit 2; `{"error":{"kind":"expected_input_digest_mismatch","message":"tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…"},"exit":2,"findings":[{"id":"expected_input_digest_mismatch","detail":"tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…","expectation":null}],"status":"could_not_evaluate"}`; no `counts`/`rows` (integrity gate runs first) |
| Live step 3 | command above, cwd lane root | exit 2; byte-identical finding and detail (only the `dispositions` argument differs) |
| Archive build | `git -C <lane> archive 28aeef4 \| tar -x -C $W/archive` | 1069 regular files; no `.git` directory; `tools/evidence-disposition.py` and both round-14 dispositions present |
| Archive step 2 | same command, cwd `$W/archive` | exit 1; `status:"failed"`; counts `expected_checks 12, effective 12, passed 11, failed 1, superseded 0`; finding `expected_contains_missing`, `expectation:"producer_before"`, detail `producer_before: stdout lacks 'summary preserves top-level exposed declaration kind'` |
| Archive step 3 | same command, cwd `$W/archive` | exit 0; `status:"clean"`; counts `expected_checks 12, effective 11, passed 11, failed 0, superseded 1`; superseded row `producer_before`, `raw_retained:true`, replacements `producer_before_oracle` + `producer_after_oracle` |
| Clone build | `git clone` lane → `$W/fleet/tameshi-shokunin`, siblings symlinked, `git checkout -q 28aeef4` | `HEAD=28aeef498cc070c3183271b709bc79d344ff547a` |
| Clone step 2 / step 3 | same commands, cwd clone root | exit 1 then 0, same finding IDs as archive |
| Archive ≡ clone | normalize each result JSON by removing `root`, compare | `identical_modulo_root=True` for both the before and the after result |
| Same tool bytes at both revs | `sha256sum tools/evidence-disposition.py` vs `git show 28aeef4:tools/evidence-disposition.py \| sha256sum` | both `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95`; every run reports tool `evidence-disposition.py r14 (tameshi-shokunin, 2026-10-20)` |
| Only pinned input that moved | `git diff --stat 28aeef4 98bea7da -- tools/evidence-disposition.py tools/mutate-and-run.sh` | `tools/evidence-disposition.py` unchanged; `tools/mutate-and-run.sh \| 145 +++---` (121 insertions, 24 deletions) |
| Pin equals the 28aeef4 runner | `sha256sum` live / `git show 28aeef4:tools/mutate-and-run.sh \| sha256sum`; `expected.json.inputs["tools/mutate-and-run.sh"]` | live `0673d2e5…`; at `28aeef4` `75ed934d…`; `expected.json` pins `75ed934d…` |
| Registry-row wording | `git show 98bea7da:SKILL.md` line 1681 | `(since round 16 the runner input moved, so --root . returns 2 expected_input_digest_mismatch by design; use --root on git archive 28aeef4 extracted to /tmp → 0 clean)` |

## The red-before fact (C2a)

At tip, recipe steps 2–3 as written (`--root .`) are **unsatisfiable**: both
exit 2 `expected_input_digest_mismatch`, not 1 then 0, because
`tools/evidence-disposition.py` verifies every `expected.json` input digest
before any predicate, and `tools/mutate-and-run.sh` moved from `75ed934d…`
(pinned by `.ufo/evidence/round-13/expected.json`) to `0673d2e5…` (the
round-16 jj-fix guard; `git diff --stat 28aeef4 98bea7da` shows only this
file moved among the two instruments).

The same two commands against the historical tree do reproduce the recipe:
`git archive 28aeef4` → step 2 exit 1 with `expected_contains_missing` on
`producer_before`, step 3 exit 0 clean with the one explicit supersession
(`raw_retained:true`). A fleet-mirror clone at `28aeef4` gives the byte-equal
result modulo the reported `root`.

This converts the round-16 spot-check's open inference into an executed fact:
`corpus/lessons/round-16-verifier-spotcheck.md` §2 says of step 2 "This one is
[INFERENCE] from reading the code; I did not execute the gate." Both live
exits are now observed 2, and the archived invocation is observed 1/0, which
is exactly the by-design sentence already appended at `SKILL.md:1681`.

Scope note on step 2's archived finding: `expected_contains_missing` records
that the pinned receipt's stdout lacks the declared `contains` marker; the
round-14 after-manifest's supersession reason (retained in step 3's output)
documents that the raw exit 1 came from a path-layout `FileNotFoundError`
before the assertion, i.e. the documented "failed expectation, not mechanism
proof" pattern, and supplies the oracle pair
(`producer_before_oracle` fails, `producer_after_oracle` passes). I record
the observed finding; I do not reinterpret it.

## Caveats

- Live runs are read-only over lane evidence and printed stdout only. During
  the wave other seats changed `.gitignore`, appended to
  `.ufo/evidence/round-16/round-gate/runner-sha256.txt`, and added untracked
  round-15 files; none of these are this seat's writes, and the gate's live
  input `tools/mutate-and-run.sh` was re-hashed as `0673d2e5…` after the runs,
  so the live result reflects the same bytes that produced the finding.
- The archive tree has no `.git`; the r14 tool needs none (it reads pinned
  tree bytes), which is why `--root` on the extraction works.
- `28aeef4` is a round-15 verifier spot-check commit; its tree is the
  revision the round-15 registry row names for the working invocation.

Verdict: **holds** — live `--root .` 2/2 (`expected_input_digest_mismatch`), `git archive 28aeef4` 1/0 (`expected_contains_missing` → clean), fleet-mirror clone at `28aeef4` identical to the archive; C2a red-before is measured, not inferred.
