# PredK7 — frozen predicate K7 (`runner-not-held-refused`) falsification

**Verdict: K7 is NOT vacuous, but it UNDER-DISCRMINATES.** The delivered
implementation (`tools/registry-replay.py` @ `c8c5b88`) satisfies K7 and is
correct on every probe I ran — I found **no defect in the shipped K7 code
path**. The defect is in the *predicate*: five plausible weaker
implementations of the projection pass the frozen K7 check while violating the
rule the wave documents
(`corpus/knowledge/replay-projection-hardening.md`: "`held` is not `true` …
refuses to publish a bundle"). `before.json` is **honest and byte-reproducible**
(verified below).

Lane: leaf member, no subagents dispatched. All execution was confined to
`/tmp/predk7/**` (fresh `git archive` exports of the lane and the base
revision, plus mutated copies of the tool there). Nothing in
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` was written except this
report; no git/jj write command was issued; the registry battery, gates and
selftests were never run inside the lane itself (only inside `/tmp` copies).

---

## 1. What the frozen predicate actually asserts

`.ufo/evidence/round-24/measure.py:147-180` (`replay_rows`):

* fixture (`obs`, line 147-156): **one** row, `external: False`,
  `runner_result = {got: 0, held: True|False, stdout: 'OK\n', stderr: ''}`,
  `requirement.expect = {exit: 0, stdout_contains: ['OK']}`;
* helper `project()` (line 158-168) runs
  `registry-replay.py --project FIXTURE --out OUT --json` and returns
  **`(out / 'bundle.json').exists()`** as its "bundle" signal (line 168);
* `control_ok` (line 170) = control exits 0 **and** `finding_ids == []`
  **and** `out/bundle.json` exists;
* K7 verdict (line 172 + 179-180):
  `control_ok and exit == 1 and 'RUNNER_NOT_HELD' in finding_ids and not bundle`.

So K7 asserts exactly: *for a one-row observation whose `runner_result.held`
is literally `False`, the CLI exits 1, names `RUNNER_NOT_HELD`, and leaves no
file named `bundle.json` in `--out`.* Everything else is outside its scope.

## 2. Positive controls — the predicate is not vacuous

Two deliberate weakenings of the delivered tool, run through a faithful
replica of `replay_rows` (control + K7 + extra probes):

| variant | one-line change | K7 verdict | observed |
|---|---|---|---|
| **vF** positive control | `elif result.get('held') is not True:` → `elif False:` | **discriminated = false** | exit 0, `bundle.json` written |
| **vG** positive control | `project()` returns the bundle even when `findings` (so `publish` writes it) | **discriminated = false** | exit 1, `finding_ids=[RUNNER_NOT_HELD]`, **bundle written** |

So K7 really does fail for "ignores the `held` flag" and for "refuses but
still publishes the bundle" — the two headline defects it is meant to catch.
It is **not** a free pass, and `control_ok` (line 170) correctly suppresses
K7-K10 whenever the control case misbehaves.

## 3. Counterexamples — plausible weaker implementations that K7 accepts

All variants are one-line edits of the delivered `tools/registry-replay.py`.
"K7 verdict" is the frozen counter's own boolean, computed by my replica of
`measure.py:147-180` (identical control, identical fixture, identical
`bundle_written = (out/'bundle.json').exists()`).

### F1 (high) — single-row fixture ⇒ no row-generality is pinned

```diff
-        elif result.get('held') is not True:
+        elif not receipts and result.get('held') is not True:   # only the first row
```

* **K7 verdict: `discriminated = true`** (the fixture has one row, so row 0 is
  still checked).
* Counterexample the predicate cannot see: a **two-row** observation whose
  *second* row is not held → the weakened tool exits **0** and writes
  `bundle.json`, `expected.json`, `live-dependent.json`:

  `K7_two_row_second_not_held: exit 0, findings [], bundle true`.

* Undetected wave-wide: the tool's own selftest is 10 single-row cases →
  `vA --selftest` = `REGISTRY_REPLAY_SELFTEST: 10/10 pass` (exit 0). The
  43-row real replay had `held=True` on every row, so no live evidence
  exposes the gap either.

### F2 (medium-high) — “`held` is not `true`” is documented, only “`held` is `false`” is tested

```diff
-        elif result.get('held') is not True:
+        elif result.get('held') is False:
```

* **K7 verdict: `discriminated = true`** (fixture uses `held: False`).
* Counterexample the predicate cannot see: `held: null` (a runner that died
  before setting the flag, or an older/incorrect producer) → the weakened
  tool exits **0** and publishes the bundle:
  `K7_held_null: exit 0, findings [], bundle true`.
* The documented rule in `corpus/knowledge/replay-projection-hardening.md`
  (“Fails when `held` is not `true`”) and the delivered code
  (`tools/registry-replay.py:89`, `is not True`) are *stricter* than what K7
  freezes. This one **is** caught elsewhere (`vB --selftest` =
  `CASE held-missing FAIL`, `9/10 pass`, and the active registry row
  `registry-replay-selftest` expects `10/10`), but **not by the frozen
  ruler** — so the 11/11 score does not evidence the documented rule.

### F3 (medium) — “writes no bundle” is a filename-scoped assertion

```diff
-    if findings:
-        return 1, report, None
+    bundle = {...}                     # built even when findings
+    if findings:
+        return 1, report, bundle
-    (out / 'bundle.json').write_bytes(raw)
+    (out / ('bundle.json' if code == 0 else 'rejected-bundle.json')).write_bytes(raw)
```

* **K7 verdict: `discriminated = true`** — `out/bundle.json` is absent, so
  `not bundle` holds, while a **complete `command-binding-v1` bundle document
  is written on refusal**:
  `K7 out_files: ["expected.json", "live-dependent.json", "rejected-bundle.json"]`.
* Undetected wave-wide: `vC --selftest` = `10/10 pass` (the selftest also
  probes `bundle.json` only, `tools/registry-replay.py:220`).
* Same hole in miniature: refusing while writing `expected.json` /
  `live-dependent.json` (variant vD) is also accepted by K7.

### F4 (medium) — external rows are exempt in a plausible design, and K7 cannot see it

```diff
-        elif result.get('held') is not True:
+        elif not row.get('external') and result.get('held') is not True:
```

* **K7 verdict: `discriminated = true`** (fixture row is `external: False`).
* Counterexample: an observation with one `external: true` row whose
  `held` is `False` → exit **0**, bundle published:
  `K7_external_not_held: exit 0, findings [], bundle true`.
* Undetected wave-wide: `vE --selftest` = `10/10 pass` (the selftest's
  `external` case has `held=True`). Live relevance is small but real: the
  actual replay has two `external` rows (`pin-disposition-read`,
  `verify-round15`, `replay/live-dependent.json`), both `held=True` today.

### F5 (low, realism) — the K7 fixture is unreachable from the real runner

`tools/registry-check.py:718-720` computes
`held = got == expected_exit and not missing and cleanup_ok`, with
`missing = [n for n in needles if n not in stdout_text]`. The K7 fixture has
`expect.exit 0`, `got 0`, `stdout 'OK\n'` containing the expected token
`'OK'`, and no `cleanup_error` ⇒ a *real* runner must emit `held=True`.
The K7 observation is therefore hand-made, and K7 pins only the projection's
reaction to a *declared* flag, never the flag's meaning.

Concretely: weakening the **producer** of the flag
(`registry-check.py:720` → `fragment["held"] = got == expected_exit`,
dropping `not missing and cleanup_ok`) leaves **K7 `discriminated = true`**.
The frozen ruler does fall to **9/11** on that tree, but only because **K5/K6**
flip (the bundle pins stop holding) — not because K7 noticed anything. The
mitigation for this class lives in the binding gate
(`tools/command-binding.py` re-derives argv/exit/stdout from the published
bundle, verified by the real gate receipt `replay-gate.json`: exit 0,
`finding_ids: []`), not in K7.

### F6 (low) — the ruler never runs the tool's own selftest

`measure.py` runs `tools/command-binding.py --selftest` for K1-K4, but for
K7-K11 it drives the CLI directly and **never invokes
`tools/registry-replay.py --selftest`**, whose 10 cases (held-missing,
cleanup precedence, stream-at-limit, invalid, plan-realpath) partly cover the
gap F2. The 11/11 number is therefore not a summary of the tool's own gate
coverage; the two instruments overlap but are not identical.

## 4. Is `before.json` honest? — yes, verified by reproduction

| check | result |
|---|---|
| `sha256sum .ufo/evidence/round-24/measure.py` | `0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64` = `before.json.instrument_sha256` (**match**) |
| base export `git archive 6a1821a8` → `tools/registry-replay.py` | **absent** ⇒ K7-K11 `tool-absent` is structurally forced, not a convenience |
| `python3 .ufo/evidence/round-24/measure.py --repo /tmp/predk7/base` (fresh export of `6a1821a8`) | `discriminated 1 / 11`, per-row verdicts **identical** to `before.json`; the parsed stdout is **byte-identical** (`recorded == mine` → `True`) |
| K4 at base | `discriminated = true`, `failing_cases: ["CASE all-of-tokens FAIL"]` — exactly as the receipt and the note state; K1-K3 mutants survive the 38-case base selftest |
| same ruler on the delivered revision | `--repo /tmp/predk7/head` (export of `c8c5b88`) → **11/11** (K1 argv-swapped-between-names, K2 argv-case-only, K3 negative-exit-mismatch, K4 all-of-tokens, K5/K6 pinned-substitution, K7-K11 CLI) |

`before.json` is truthful, reproducible with the frozen instrument, and its
"1/11" is correctly explained (K4 is the pre-existing control). The number is
honest but weak as a *defect* measure: five of the eleven predicates fail at
base only because the artifact did not exist yet, which the lesson and
contract already state ("capability checks, not historical defects").

## 5. Delivered implementation — no defect found in the K7 path

`tools/registry-replay.py` (sha256 `9fcd2dbb…`, byte-identical at
`c8c5b88` and at the replayed revision `d2eaecd`, and identical to the
`instrument_sha256` recorded in `replay-command.json`):

* `project()` line 89 uses `result.get('held') is not True` (strict, handles
  `False`/`None`/missing);
* `publish()` (line 116-124) returns **before** `out.mkdir()` when
  `bundle is None`, so a refusal leaves the `--out` directory entirely
  uncreated (probe: `out_files: []`) — not merely "no `bundle.json`";
* probe results for the delivered tool: control → exit 0, `bundle.json` +
  `expected.json` + `live-dependent.json`; `held=False` → exit 1,
  `RUNNER_NOT_HELD`, no files; `held=null` → exit 1, `RUNNER_NOT_HELD`, no
  files; two-row with second row not held → exit 1, no files; external row
  not held → exit 1, no files. **All correct.**

Minor, not a K7 defect: `result.get('cleanup_error')` is a truthiness test
(`tools/registry-replay.py:86`), so an empty-string `cleanup_error` is
treated as absent.

## 6. Residual risk and verification gaps

1. The actual replay (`.ufo/evidence/round-24/replay/`, `replay-command.json`,
   exit 0, 43 rows, `bundle_sha256 4f424023…`, gated by
   `replay-gate.json` exit 0 / `finding_ids: []`) contains **no not-held row**,
   so the refusal path has **no real-world instance**; the K7 evidence is
   entirely synthetic, as the contract's bounds admit.
2. The counter exercises `--project`; the production path is `--run`
   (which shares `project()`/`publish()` but additionally writes
   `out/observations.json` before projecting). A bug confined to `--run`
   would be invisible to K7 and to the actual replay (which refused nothing).
3. F1/F3/F4 are undetected by *both* the frozen ruler and the tool's own
   selftest; only a multi-row fixture and a refusal-time bundle-content
   assertion would expose them.
4. The K7 verdict is shared-gated by `control_ok` with K8-K10: one control
   regression silently suppresses four predicates (conservative, but it means
   a broken control turns "discriminated" into `false` for reasons unrelated
   to the predicate under test).
5. Wave-level (not K7): the after measurement is not yet recorded anywhere —
   `SCORECARD.md:1145-1146` ("Measured results are recorded below only after
   execution.") and `corpus/lessons/round-24.md:53` ("The after measurement is
   recorded below once executed.") both defer it, and
   `.ufo/evidence/round-24/` contains no `after.json` at `c8c5b88`. My own
   run against a fresh export of `c8c5b88` gives 11/11, but it is not a
   retained lane receipt.

## 7. Smallest safe correction (recommendation, not applied)

Keep the frozen ruler as-is (it is the frozen contract) and **add** to the
tool's own selftest — which is already a gated registry row — the two cases
the frozen predicate cannot express, i.e. in `tools/registry-replay.py`
`selftest()`:

* a **two-row** observation whose *second* row has `held=False` → expect exit
  1, `['RUNNER_NOT_HELD']`, no bundle (kills F1);
* an **external** row with `held=False` → expect exit 1, `['RUNNER_NOT_HELD']`,
  no bundle (kills F4);
* assert that a refusal leaves `--out` **empty** (not merely
  `bundle.json` absent) — kills F3 for the out-dir case;
* keep the existing `held-missing` case (kills F2) and make the registry row
  `registry-replay-selftest` require the new case count (e.g.
  `13/13 pass`) so the strengthening is itself pinned.

If the frozen ruler is ever re-cut (a new round), the K7 fixture should be
multi-row, should use `held: null` as a second case, and should assert the
absence of any `command-binding-v1` document rather than the absence of the
literal file name `bundle.json`.

---

### Reproduction (all inside `/tmp/predk7`, nothing written in the lane)

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
mkdir -p /tmp/predk7/base /tmp/predk7/head
GIT_OPTIONAL_LOCKS=0 git archive 6a1821a8897eea6e7d9669292160ec9593669409 | tar -x -C /tmp/predk7/base
GIT_OPTIONAL_LOCKS=0 git archive c8c5b88c8e961a929cdc351b95a7074c76958909 | tar -x -C /tmp/predk7/head
python3 .ufo/evidence/round-24/measure.py --repo /tmp/predk7/base   # -> 1/11, identical to before.json
python3 .ufo/evidence/round-24/measure.py --repo /tmp/predk7/head   # -> 11/11
# weakened variants vA..vG = one-line edits of head/tools/registry-replay.py,
# scored by /tmp/predk7/k7probe.py (replica of measure.py:147-180)
```

### Tooling

No package was installed or upgraded for this lane (the review needed only
`python3`, `git` and `tar` already present on the host). No pacman/uv/npm
transaction was performed.
