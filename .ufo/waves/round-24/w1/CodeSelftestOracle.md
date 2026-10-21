# CodeSelftestOracle — literal-oracle independence of `tools/registry-replay.py --selftest` and the round-24 fixtures in `tools/command-binding.py --selftest`

Seat: TameshiR24-2.CodeSelftestOracle (reviewer, leaf member — no subagent dispatch).
Revision inspected: delivered `c8c5b88c8e961a929cdc351b95a7074c76958909` (base `6a1821a8897eea6e7d9669292160ec9593669409`).
Axis: calibration. Question assigned: **do the expected outcomes derive from the code under test?**

## Verdict

**Independence: yes. Adequacy: no.**

1. **No expected outcome in either selftest is derived from the implementation under test.** Every
   expected exit code, finding-ID list, live-dependent list and revision-pinned count is a literal
   written in the test, not a value computed by calling the tool. The one derived value
   (`plan-realpath`) is derived from the *fixture environment* with stdlib `os.path.realpath`, not
   from the tool (`tools/registry-replay.py:236,239-240`).
2. **No shipped defect in the oracle itself.** I independently re-derived all six round-24 fixture
   expectations from the binding semantics (not from `evaluate()`); all six are exactly right, each
   isolating exactly one deviating field. The delivered selftests are green at the delivered
   revision (44/44 and 10/10; independently recorded by `RunSelftests` in a `/tmp` clone at
   `c8c5b88`), and I re-derived both case counts from source: 44 = 17 inline + 19 round-23 + 6
   round-24 + 2 tail; 10 = 9 + 1 plan.
3. **But the literal oracle of `tools/registry-replay.py` is materially under-specified, and five
   concrete weakenings survive `REGISTRY_REPLAY_SELFTEST: 10/10 pass`.** Two of them also survive
   the frozen eleven-predicate ruler. The largest hole (F1) sits on the round's central handoff
   invariant: nothing in the round asserts that the published `bundle.json` bytes are the bytes the
   published `expected.json` commits to.

Consequence for calibration: the round may claim *"the selftest's expectations are literal and
independent"* (true) but not *"the selftest shows the tool can fail"* for the F1–F5 properties
below. The corpus/registry wording should not be read as "the selftest certifies the tool".

## Evidence

### 0. Provenance and identity checks (read-only)

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -3
c8c5b88 round-24: append fifteen actual traced source re-anchors preserving prior ledger
bd38c02 round-24: retain refusing replay run and binding verdict
d2eaecd round-24: add refusing registry replay, fixture kills, pinned registry successors and sourced entry
```

`git diff 496d212 c8c5b88 -- tools/command-binding.py` shows the **only** change to the binding
tool is the fixture loader (`tools/command-binding.py:164-172`); `evaluate()` is byte-identical, so
every round-23 expectation still holds.

```
$ sha256sum .ufo/evidence/round-23/replay/bundle.json .ufo/evidence/round-23/source-read-bundle.json
3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9  .ufo/evidence/round-23/replay/bundle.json
db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf  .ufo/evidence/round-23/source-read-bundle.json
```

Both match the literal `bundle_sha256` expectations of the two new pinned registry rows
(`tools/registry.json`, rows `command-binding-frozen-clean-pinned`,
`command-binding-source-read-red-pinned`) — the pinned literals are not derived from the tool's
output at read time; they are file digests and they are correct.

Delivered replay artifact is internally consistent (so F1 is a *coverage* hole, not a shipped
defect):

```
$ sha256sum .ufo/evidence/round-24/replay/bundle.json
4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6
$ jq -r .bundle_sha256 .ufo/evidence/round-24/replay/expected.json
4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6
```

(the same digest is echoed in `.ufo/evidence/round-24/replay-gate.json` stdout.) The retained
replay also agrees with its own observations: 43 rows, 2 `external` rows
(`pin-disposition-read`, `verify-round15`), `revision_pinned` 41.

### 1. Independence — what I checked and found independent

**`tools/registry-replay.py`** (`selftest()` at `:190`):

* Expected outcomes are literals in the case table `:197-206`
  (`('stream', obs(stderr='e' * 9), ('--max-stream-bytes', '8'), 1, ['STREAM_LIMIT'], False)` etc.).
  Nothing calls `project()` or `plan()` to compute an expectation.
* The only non-literal expectation is the plan case: `real = os.path.realpath(fleet)` (`:236`)
  compared against `value.get('fleet_root')`/`value.get('siblings')` (`:239-240`). `realpath` is
  stdlib, so the expectation is a property of the *fixture*, not of the tool. It still discriminates:
  an `os.path.abspath`-style implementation would yield the alias path, not `real`.
* The fixtures are built by a local helper `obs()` (`:192-198`) that constructs the observation
  document; it does not import anything from the implementation under test.

**`tools/command-binding.py`** (`selftest()` at `:132`):

* Inline expectations are literals (`:134-163`, e.g. `changed('stderr-cannot-supply-token',
  lambda b: b['receipts'][0].update(stdout='', stderr='CLEAN'), 1, 'STDOUT_MISMATCH')`).
* The supplemental expectations come from JSON literals:
  `.ufo/evidence/round-24/extra-cases.json` → `expected_exit` / `finding_ids` are hand-written
  values with a `why` rationale per case; the loader copies them verbatim
  (`tools/command-binding.py:166-169`).
* The only reuse of the module's own code is `decode()` (`:167`), used to *parse* the expectation
  file. That is fail-closed, not a laundering path: a `decode()` failure raises inside the `try`
  and returns `1` with `COMMAND_BINDING_SELFTEST: fixture-unavailable` (`:170-172`), so a broken
  parser cannot turn an expectation into a pass.
* The commitment digest is computed from the **fixture bytes**, not from the tool's output
  (`:181-183`): `digest = sha256(raw)`, `expected_path.write_text(...digest)`,
  `bundle_path.write_bytes(raw + (b' ' if name == 'tampered' else b''))`. The `tampered` case
  tampers *after* the digest is taken, so `SNAPSHOT_TAMPERED` is a real expectation, not a
  self-fulfilling one. No circularity.

**My independent re-derivation of the six round-24 fixtures** (semantics, not `evaluate()`):
each bundle is the same two-requirement base; each case deviates in exactly one field, and all
other fields still satisfy the documented contract (exact argv per name, canonical cwd, equal
revision, integer exit, required stdout token present in `stdout`):

| case | single deviation | independent expectation | matches fixture |
|---|---|---|---|
| `argv-swapped-between-names` | receipt argv transposed between the two names | exactly `["ARGV_MISMATCH"]`, exit 1 | ✔ |
| `argv-case-only` | `['gate','--Check']` vs `['gate','--check']` | exactly `["ARGV_MISMATCH"]`, exit 1 | ✔ |
| `argv-padded-token` | `' --check'` (leading space) | exactly `["ARGV_MISMATCH"]`, exit 1 | ✔ |
| `argv-repeated-flag` | `['gate','--check','--check']` | exactly `["ARGV_MISMATCH"]`, exit 1 | ✔ |
| `negative-exit-mismatch` | receipt exit `-9` vs declared `0` | exactly `["EXIT_MISMATCH"]`, exit 1 | ✔ |
| `negative-exit-declared-match` | declared `-15`, receipt `-15` | no findings, exit 0 | ✔ |

No expectation is wrong; the round-24 fixtures are a well-aimed, independent oracle for K1/K2/K3.

### 2. Findings — coverage of the literal oracle

#### F1 (Medium–High) — the publish contract is asserted nowhere: the selftest checks only that `bundle.json` *exists*

`tools/registry-replay.py:219-220` is the whole publication oracle:

```python
ok = (r.returncode == code and rep.get('finding_ids') == findings
      and (out / 'bundle.json').exists() == written)
```

`bundle.json` is never read; `expected.json` (`:123-124`) and `live-dependent.json` (`:125-127`)
are never even mentioned by the selftest. The digest handoff — `expected.json.bundle_sha256` must
be the digest of the published `bundle.json` bytes, which is exactly what
`tools/command-binding.py` enforces with `SNAPSHOT_TAMPERED` — is therefore unasserted by the
tool's own gate **and** by the frozen ruler (`measure.py` K7–K10 only test
`(out / 'bundle.json').exists()`).

Counterexample (mutant, one line): `tools/registry-replay.py:122`

```python
(out / 'bundle.json').write_bytes(raw)          # pristine
(out / 'bundle.json').write_bytes(raw + b'\n')   # mutant
```

* every selftest case still passes → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0 (existence
  only; no file content is inspected);
* the frozen ruler still reports 11/11 (K7–K10 test `finding_ids` + bundle *existence*);
* the *next* real replay publishes a bundle whose bytes no longer match the digest committed in
  `expected.json`, so the downstream binding gate
  `python3 tools/command-binding.py --bundle …/bundle.json --expected …/expected.json --json`
  returns `2 / ["SNAPSHOT_TAMPERED"]` instead of clean.

An equivalent-content mutant (dropping `requirements` from the published bundle) is equally
invisible and would yield `INVALID_BUNDLE` at the gate.

Today the delivered bytes are correct (see §0), so this is a **coverage hole, not a shipped
defect** — but it is the hole that matters most, because the published bundle is the round's
product and the "bundle published" claim is the tool's headline success path.

#### F2 (Medium) — the tool's advertised self-invocation never exercises `--run`, so both substitution guards are untested

`SKILL.md:2052` registers `tools/registry-replay.py` as a gate whose entry is
`--project … ; --run --repo LANE --rev REV --requirements FILE --registry-baseline FILE --out DIR ; --plan …`
and names `python3 tools/registry-replay.py --selftest` as its self-invocation. That selftest
spawns only `--project` (`:210-215`) and `--plan` (`:230-237`).

Both substitution guards live in the untested mode:

```python
tools/registry-replay.py:139-141   if sha256(raw_registry) != frozen['registry_sha256']: return 2
tools/registry-replay.py:144-146   if requirements != frozen['requirements']: return 2
```

Neither the selftest nor the frozen ruler reaches them: `measure.py` K7–K11 use `--project` and
`--plan` only, and K5/K6 use `tools/registry-check.py`. The only evidence that the guards hold is
*positive* — the retained run at `d2eaecd` succeeded (`.ufo/evidence/round-24/replay-command.json`).
By the round's own stated standard ("routed hardening is repaired only when it can fail",
`corpus/lessons/round-24.md`), a guard that has never been observed to fail is not yet shown able
to fail. A mutant that removes either guard (or that checks the wrong field of the frozen
document) is invisible to every oracle in this round.

#### F3 (Medium) — the `STREAM_LIMIT` branch is covered on one stream only

The over-limit selftest case is **stderr**-only (`tools/registry-replay.py:202`,
`obs(stderr='e' * 9)` at limit 8), and the stdout case sits exactly *at* the limit
(`:203`, `obs(stdout='12345678')` at limit 8 → not over). The loop under test is
`for stream in ('stdout', 'stderr'):` (`:92`).

Mutant: `for stream in ('stderr',):` — the stdout half of the bound is never enforced.

* every selftest case still passes (10/10): no stdout stream in the suite ever exceeds the bound;
* the frozen ruler *does* catch it (K9 uses a 67-byte stdout at limit 16, `.ufo/evidence/round-24/measure.py:175`),
  so the round's *predicate* survives — but the tool's persistent regression gate, which the
  registry battery re-runs (active row `registry-replay-selftest`, argv
  `python3 tools/registry-replay.py --selftest`), does not.

This is distinct from `MutProject` M03 (whole bound deleted → killed by the stderr case) and from
`LabStreamBytes` (bytes vs characters). It is a *branch*-coverage gap, and it is closed by the
same one-line addition that would close `MutProject` M04's ASCII-only gap (a multibyte over-limit
stdout case would cover both).

#### F4 (Medium–Low) — refusal attribution (`refused_rows`) is emitted but asserted nowhere

`tools/registry-replay.py:106` publishes `refused_rows: sorted(set(refused))` — the per-row
attribution of *which* row was refused, populated at `:88`, `:91`, `:98`. The selftest asserts
`finding_ids`, `live_dependent` and `revision_pinned` only (`:219-224`); the ruler asserts
`finding_ids` and "no bundle" only (`measure.py:170-179`). Mutant: delete the three
`refused.append(name)` calls → the projection still refuses with the right finding IDs, the
selftest still reports 10/10, the ruler still reports 11/11, and the refusal report loses the one
field that tells an operator which row to fix.

#### F5 (Low) — the plan case does not assert the normalised `repo` field

`tools/registry-replay.py:239-240` asserts `fleet_root` and `siblings` but not `repo`, although
`plan()` normalises all three (`:63-70`) and the docstring claims "the fleet root and sibling
identities are realpath-normalised". Mutant `return {'repo': repo, …}` (un-normalised alias path)
→ 10/10 PASS; the frozen K11 does assert `repo` (`measure.py:184-187`), so the wave measurement
catches it and the persistent gate does not. Same family as F3.

#### F6 (Low) — invalid-observation reports have no schema, and the shape difference is unasserted

For `INVALID_OBSERVATIONS` the printed report is `{'finding_ids': [...]}` only
(`tools/registry-replay.py:74-76` and `main()`'s `--project` branch), whereas every other report
carries `schema: registry-replay-report-v1` (`:105`). The selftest asserts `finding_ids` only, so
a consumer cannot rely on `schema` being present, and `SKILL.md:2052` lists "2 invalid/unavailable
input" without naming `INVALID_OBSERVATIONS`. No correction is required for this wave unless a
consumer parses the report by schema; noted so the shape is not mistaken for uniform.

#### F7 (Low, provenance — corroborates `CodeFixtureLoader` M3) — the new expectation file is the one unpinned input

`.ufo/evidence/round-24/extra-cases.json` (sha256 `6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35`)
is the only load-bearing input of the new oracle that no digest ledger pins. The round-24 source
ledger pins the round-23 fixture and the tool:

```
$ jq -r '[.entries[] | (.inputs // {}) | keys[]] | unique[]' .ufo/evidence/round-24/source-refresh-entries.json | grep -E "round-2[34]|tools/"
.ufo/evidence/round-23/extra-cases.json      87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00
tools/command-binding.py                      9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d
```

and the round-24 fixture digest appears only in wave reports, not in a ledger. Because the
expectations live outside the tool, they can be edited to agree with an implementation without any
ledger evidence of the edit. The frozen ruler bounds the damage (an expectation edited to match a
mutant *removes* discrimination instead of manufacturing a false pass, so the ruler would report
< 11/11), but the traceability is asymmetric with round-23 and the file is the oracle's only
external input.

### 3. Confirmations — checked, no defect found

* Both selftests green at the delivered revision, in a private clone: `command-binding.py --selftest`
  → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0; `registry-replay.py --selftest` →
  `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0 (`RunSelftests`, clone at `c8c5b88`). My
  independent source-level counts (44 and 10) match the literals pinned in the active registry
  rows `command-binding-selftest-r24` and `registry-replay-selftest`, so no stale count.
* The `cleanup` expectation (`['RUNNER_CLEANUP_FAILED']` only, not both IDs) is a deliberate
  `elif` consequence (`:86-91`); the fixture pins it literally and it matches the docstring
  ("refuses … when any runner row did not hold **or** reported a cleanup failure"). Not a defect.
* The `held-missing` case (`held=None`) is a meaningful case: it distinguishes
  `result.get('held') is not True` (`:89`) from a `held is False` reading, which the `not-held`
  case alone would not.
* The `duplicate-json-key` case is not a tautology: `raw.replace(b'"schema":', …)` hits the
  top-level `schema` key (the only occurrence), and the expected digest is computed over the
  *mutated* bytes (`:181-183`), so the observed `INVALID_INPUT` can only come from the duplicate
  key check. A mutant that removed duplicate detection would decode the last value, evaluate the
  bundle as clean, and fail the case.
* `stderr-cannot-supply-token` and `all-of-tokens` (round-23) jointly pin that stdout tokens are
  matched with `all()` against `receipt['stdout']` — a token-sourcing mutant (`stderr`) or an
  `any()` mutant is caught.
* No expectation anywhere is recomputed by executing the implementation under test, and no
  expectation is a copy of that implementation's output captured at authoring time (the fixtures
  carry hand-written `why` rationales, and the two pinned registry digests are file digests, not
  tool outputs).

### 4. Residual risk and verification gaps

* **My item carries no "Run" token**, so per the wave bounds I executed no command beyond
  read-only inspection: the F1–F5 mutant-survival claims are derived by static reading of each
  mutant's effect on every case, not by re-running the mutants. `MutProject`'s retained harness
  shows the same detector behaviour for the neighbouring mutants (its M03 — whole bound deleted —
  is killed by the stderr case; my F3 mutant keeps stderr checking and so survives), which is
  consistent with my derivation but does not execute it. A one-line harness run per mutant would
  convert F1–F5 from derivation to observation.
* F2 cannot be closed by a static argument at all: the `--run` path needs an executed negative
  case.
* I did not check the fleet-wide consumers of `registry-replay-report-v1` (only this lane's
  `SKILL.md:2052` and `corpus/knowledge/replay-projection-hardening.md` reference the tool), so the
  blast radius of F6 is unmeasured.
* I did not review whether `corpus/lessons/round-24.md` / `CorpusScorecard.md` over-read the
  selftest as tool certification (other lanes own those files); F1–F5 are the facts such a reading
  would need.
* Not claimed anywhere in this report: producer authentication, promotion, historical
  R17-CMD-BIND closure, numeric score uplift, or general mutation adequacy.

### 5. Smallest safe correction (ordered, cheapest first)

All five are **additive assertions in the test files**; none changes `evaluate()`, `project()` or
`publish()` semantics, so the frozen ruler and the frozen predicate set stay valid.

1. **F1** — in the `clean` case of `tools/registry-replay.py:219-224`, assert
   `json.loads((out/'expected.json').read_bytes())['bundle_sha256'] ==
   sha256((out/'bundle.json').read_bytes()).hexdigest()` and that `bundle.json`'s `requirements`
   and `receipts` equal the fixture's; in the refusal cases assert `expected.json` and
   `live-dependent.json` are absent. One file, no production change.
2. **F4** — assert `rep.get('refused_rows') == ['one']` in the `not-held`, `cleanup` and `stream`
   cases. One line per case.
3. **F3** — add one stdout-over-limit case (ASCII is enough for the branch; a multibyte payload
   would also close `MutProject` M04's byte/char gap). One case.
4. **F5** — assert `value.get('repo') == os.path.join(real, 'lane-shokunin')` in the plan case. One
   line.
5. **F2** — add one `--run` case over a synthetic frozen `requirements` + `registry-baseline` pair
   in `/tmp` whose digest/requirements disagree with the source registry, asserting exit 2 and no
   published bundle. This is the only correction that needs new fixture material.
6. **F7** — pin `.ufo/evidence/round-24/extra-cases.json` (`6ad7842f…`) in the round-24 source
   ledger, using the coordinator's ledger convention (one ledger row).

**Consequence to plan for:** corrections 1–5 change the selftest case counts (10 → ≥14 for
`registry-replay.py`; 44 → ≥45 for `command-binding.py`), so the two active registry rows
(`registry-replay-selftest` expecting `10/10 pass`, `command-binding-selftest-r24` expecting
`44/44 pass`) would need append-only superseding rows with the new literals, in the same
`status: superseded` + `superseded_by` pattern already used this round (`tools/registry.json`).

### 6. Axes

* **Independence (literal oracle):** holds in both tools — no expectation is computed from the
  implementation under test; the only derived expectation comes from the fixture environment via
  stdlib `os.path.realpath`.
* **Correctness of expectations:** holds — all six round-24 fixture expectations independently
  re-derived and correct; counts 44 and 10 consistent with the pinned registry literals.
* **Discriminating power (calibration):** partly fails for `tools/registry-replay.py` — F1–F5;
  `tools/command-binding.py`'s inline oracle is materially stronger (peer `MutFixtures` found three
  surviving mutants there: token-prefix argv match, abs-exit, truthy-exit).
* **Fail-closed behaviour:** holds — fixture-load failure, parse failure and duplicate keys all
  fail closed rather than launder an expectation.
* **Provenance / traceability:** fails asymmetrically — F7 (new expectation file unpinned by any
  ledger).

### 7. Tooling and bounds

No tools were installed or upgraded (nothing beyond stock `python3`/`git`/`jq`/`sha256sum` was
needed), so there is no install record to report.

Bounds compliance: only read-only inspection was performed (`git log`/`git diff` with
`GIT_OPTIONAL_LOCKS=0`, `sha256sum`, `jq`, `grep`, file reads). No selftest, gate, registry
battery or ruler was executed in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; no `--run`
replay was performed; no git/jj write command was run against any repo; no sibling lane, lane jj
state or Git index was touched; no subagent was dispatched. The only file written is this report:
`.ufo/waves/round-24/w1/CodeSelftestOracle.md`.
