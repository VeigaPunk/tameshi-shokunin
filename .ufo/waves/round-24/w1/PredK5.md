# PredK5 — frozen predicate K5 (`frozen-clean-substitution`) calibration review

Lane: W1 leaf reviewer (no dispatch). Target: frozen counter
`.ufo/evidence/round-24/measure.py` (K5 code path), contract
`.ufo/evidence/round-24/contract.json`, base receipt
`.ufo/evidence/round-24/before.json`, delivered implementation revision
`c8c5b88c8e961a929cdc351b95a7074c76958909`.

## Verdict

**K5 is honest at the delivered revision: it does not pass vacuously, it passes for
the right reason, and it does discriminate the weaker implementation it was routed
against. `before.json` is honest.** No blocking defect found.

One **medium** calibration gap and four **low** residuals are reported below. The
medium gap (F1) does not change today's verdict — the substituted bundle is
content-clean, so today's flip is attributable solely to the pinned digest literal —
but it makes K5's `discriminated` boolean an *over-approximation* that would
mis-report the routed defect class under a plausible future input change.

Verdict is a recommendation only. No producer authentication, no promotion, no
historical R17-CMD-BIND closure and no numeric score uplift is claimed.

## What I checked (and how)

Read-only inspection of the production lane plus one scratch evaluator in `/tmp`.
I did **not** execute the repo's selftest, gates, registry battery or the frozen
counter inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (lane bound: only
items that say "Run" may execute beyond read-only inspection), and I did not execute
them in a clone either; the head-side counter output is consumed as *retained
evidence* produced by another seat (`.ufo/evidence/round-24/after.json`).

1. Frozen counter: `.ufo/evidence/round-24/measure.py:97-135` (`held`, `substitute`,
   `pin_rows`), `measure.py:92-94` (`registry_rows_for`), `measure.py:119-135`.
2. Implementation under test: `tools/command-binding.py:115-127` (`check`: digest
   over raw bundle bytes at line 124, `SNAPSHOT_TAMPERED` at 125-126),
   `tools/command-binding.py:65-108` (`evaluate`), `tools/command-binding.py:209-213`
   (JSON report shape).
3. Holder semantics: `tools/registry-check.py:648-729` (`held = got == expected_exit
   and not missing and cleanup_ok` at 720, `stdout_missing` at 728),
   `tools/registry-check.py:850-873` (`--only` selects exactly one fragment).
4. Registry rows: `tools/registry.json` rows `command-binding-frozen-clean` (superseded,
   unpinned), `command-binding-frozen-clean-pinned` (active, digest-pinned),
   `command-binding-source-read-red{,-pinned}`; base registry at `6a1821a` via
   `git show 6a1821a:tools/registry.json`.
5. Base receipt `.ufo/evidence/round-24/before.json` (full 11 rows parsed) and head
   receipt `.ufo/evidence/round-24/after.json` (11/11, K5 row parsed).
6. Independent re-implementation of `command-binding.evaluate()` written by me in
   `/tmp/predk5/eval.py` (faithful to `tools/command-binding.py:59-110`), applied to
   the three committed bundles; cross-checked against retained round-23 gate
   receipts `.ufo/evidence/round-23/replay-gate-A.json` and
   `.ufo/evidence/round-23/correct-command-gate-A.json`.
7. Counter freeze: `git log -- .ufo/evidence/round-24/measure.py` → single commit
   `e338f1b` ("freeze eleven-predicate hardening claim, ruler and before receipt");
   `sha256sum .ufo/evidence/round-24/measure.py` = `0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64`
   = `before.json.instrument_sha256` = `after.json.instrument_sha256` ⇒ base and head
   were measured by byte-identical counter bytes (no rerouting, no mid-wave edit).
8. Routed defect text: `.ufo/waves/round-23/fresh-adjudication.json:66` — "The
   command-binding-frozen-clean and source-read-red registry rows do not pin
   bundle_sha256 literals, so a regenerated bundle and expected pair would still hold."
   The delivered row's `source` anchor points at exactly that line.

## The decisive K5 chain (why the flip is real and right-reasoned)

K5 in the frozen counter (`measure.py:107-135`):

* `registry_rows_for(root, '.ufo/evidence/round-23/replay/bundle.json')` matches rows
  whose `argv` contains that exact element and whose `status == 'active'`. At
  `c8c5b88` that is exactly one row: `command-binding-frozen-clean-pinned` (the
  round-23 `command-binding-frozen-clean` row is `superseded`).
* `substitute()` (`measure.py:107-117`) overwrites the replay bundle with the bytes of
  `.ufo/evidence/round-23/correct-command-bundle.json` and regenerates
  `expected.json` with the new sha256 (self-consistent substitution).
* `held()` (`measure.py:97-105`) runs `tools/registry-check.py --only <row> --json`
  in the copy and reads `rows[0]['held']`.

Facts I verified independently:

| item | value | source |
|---|---|---|
| sha256 of pristine `round-23/replay/bundle.json` | `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9` | my computation; equals the literal pinned in `tools/registry.json` (`command-binding-frozen-clean-pinned.expect.stdout_contains[1]`) and equals `round-23/replay/expected.json.bundle_sha256` |
| `evaluate(pristine replay bundle)` | exit 0, findings `[]` | my independent evaluator; matches retained `round-23/replay-gate-A.json` stdout `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": [], …}` |
| sha256 of `round-23/correct-command-bundle.json` (the substitution source) | `90dc14bf5ca6e2d6e935fc9664246b8335e2240b68c81c8afc94fdadb3aed277` | my computation |
| `evaluate(correct-command bundle)` | exit 0, findings `[]` | my independent evaluator; matches retained `round-23/correct-command-gate-A.json` stdout `{"bundle_sha256": "90dc14bf…", "exit": 0, "finding_ids": [], …}` |

Therefore, in the substituted state the row's command emits

```
{"bundle_sha256": "90dc14bf5ca6e2d6e935fc9664246b8335e2240b68c81c8afc94fdadb3aed277", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}
```

(`tools/command-binding.py:209-213`; `check()` returns the digest of the *bundle
bytes* at line 124, and `evaluate()` is clean, and the regenerated `expected.json`
matches so no `SNAPSHOT_TAMPERED`).

Against the pinned row's two needles:

* `"finding_ids": []` → **present** (the substituted bundle is clean);
* `"bundle_sha256": "3d6c99b7…"` → **absent** (the digest moved to `90dc14bf…`).

So `missing == {the pinned digest literal}` and `held = False` for exactly one
reason: **the registry row's pinned digest literal no longer matches the bundle**.
The content-cleanliness needle still holds, so the failure is not a content artefact.
The retained head receipt agrees: `after.json` → K5 `control: {…pinned: true}`,
`substituted: {…pinned: false}`, `discriminated: true`, `discriminated 11/11`.

## Vacuity analysis

K5 cannot pass vacuously at this revision:

* No active row → `pin_rows` records `reason: 'no-active-row'`, `discriminated=False`
  (`measure.py:127-130`).
* Registry-check error → `held()` returns `None` → `all(v[0] is True …)` is False →
  not discriminated (`measure.py:133-134`).
* A row pinned to a *wrong* literal (e.g. the sha of `expected.json`, or of an
  unrelated file) would fail the **control** (the tool prints the bundle digest), so
  `discriminated=False`. The control therefore *proves* the pinned literal is the
  pristine bundle's sha256 — it is not an arbitrary string that happens to be absent
  after substitution.
* `held` requires `got == expected_exit and not missing and cleanup_ok`
  (`registry-check.py:720`); the tool exits 0 and spawns no children, so no
  spurious `cleanup_ok`/`got` path can fake the flip.
* `--only` yields exactly one fragment (`registry-check.py:851-856`), so `rows[0]` is
  the requested row — the helper's `rows[0]` assumption is currently safe.

## Does K5 discriminate a plausible weaker implementation?

The routed weaker implementation is the round-23 state: the row asserts cleanliness
but pins no `bundle_sha256` literal. Base receipt `before.json` shows exactly that
state and the expected outcome:

* base registry (`git show 6a1821a:tools/registry.json`): `command-binding-frozen-clean`,
  `status: active`, `expect.stdout_contains == ["\"finding_ids\": []"]` (no digest literal);
* `before.json` K5 row: `rows: ["command-binding-frozen-clean"]`, `control: true`,
  `substituted: true`, `discriminated: false` — i.e. the self-consistent substitution
  still held at base, which is the defect;
* at `c8c5b88` the same substitution flips the pinned row to `false`
  (`after.json` K5 row) ⇒ the fix is discriminated by the same counter bytes.

So the routed defect class is discriminated in the intended direction (before 0 → after 1).

## Is `before.json` honest?

Yes, on every check I could make without executing the counter:

* `instrument_sha256` = the current `measure.py` sha256 (`0a7f6daa…`), i.e. the base
  run used the same frozen counter bytes as the head run — not a different or edited
  instrument.
* The base run's recorded K4 row is internally consistent with the *base* tree: the
  recorded mutant `stdout_tail` ends `COMMAND_BINDING_SELFTEST: 37/38 pass` and the
  control shows `38/38 pass`, which is exactly the base tool's case count
  (17 base cases + 19 `round-23/extra-cases.json` + `tampered` + `duplicate-json-key` = 38;
  the head tool adds 6 `round-24` cases → 44, which is what the new active row
  `command-binding-selftest-r24` expects). A fabricated head-derived receipt would not
  carry the base-only 38-case tail.
* `before.json` records `revision 6a1821a…`, `cwd /tmp/tameshi-r24-before-YdP3/lane`,
  `exit 1`, `stderr ""`; `discriminated 1/11` with the single `true` on K4, and the
  recorded K5/K6 row names match the base registry's *unpinned* active row names
  (`command-binding-frozen-clean`, `command-binding-source-read-red`) — i.e. the receipt
  was produced against the base registry, not the head one.
* `measure.py` did not exist at the base revision (`git show 6a1821a:.ufo/evidence/round-24/measure.py`
  → "exists on disk, but not in …"), which is expected and legitimate: the frozen
  counter is a harness run against a clone of the old code, as
  `contract.json.counter` prescribes.

Residual honesty caveat: when I began this review, `after.json` and
`noharm-c8c5b88.json` were untracked working-tree files written by another seat
(`git status --porcelain` → `?? .ufo/evidence/round-24/after.json`,
`?? .ufo/evidence/round-24/noharm-c8c5b88.json`); they were committed during the
review as `04657a6` ("round-24: retain replacement-L1 after receipt (11/11) and
no-harm receipt at c8c5b88"). That commit adds only those two evidence files — no
file under `tools/`, `corpus/` or `SKILL.md` — so the implementation revision under
test remains `c8c5b88` and the receipt's `revision` field matches it.

## Findings by severity

### F1 — MEDIUM — K5 records no failure reason: `discriminated` is an over-approximation

`pin_rows` records only booleans (`measure.py:132-135`); it never inspects which
needle failed, although `registry-check.py` already exposes exactly that
(`stdout_missing`, `registry-check.py:728`).

**Concrete counterexample** (derived from the code paths cited above; two edits to a
scratch copy of the delivered tree, both outside the frozen counter):

1. Make the substitution source dirty — edit only
   `.ufo/evidence/round-23/correct-command-bundle.json` so a receipt no longer
   matches its requirement (my independent evaluator confirms such an edit yields
   `exit 1, ['ARGV_MISMATCH']`).
2. Re-introduce the routed defect class — drop the
   `"bundle_sha256": "3d6c99b7…"` needle from the active row
   `command-binding-frozen-clean-pinned`, leaving only `"finding_ids": []`
   (this is exactly the base-round-23 row).

Then the frozen counter's K5 path yields: control `true` (pristine bundle is clean and
matches the reduced needle); after substitution the dirty bundle yields
`finding_ids: ["ARGV_MISMATCH"]`, so the `"finding_ids": []` needle is missing, the row
is not held, and **K5 reports `discriminated: true` for the unpinned (defective)
implementation**. The counter would be measuring "some needle failed", not "the digest
pin fired".

**Why this does not change today's verdict:** the committed substitution source is
clean (verified above: `evaluate → 0, []`), so today's single missing needle is the
pinned digest literal and today's flip is pin-attributable. F1 is a *robustness*
defect of the predicate, not a misreport in the current receipts.

### F2 — LOW — K5 alone does not kill a "trust the commitment file" implementation

A tool that reported `expected['bundle_sha256']` instead of `sha256(bundle_bytes)`
(`tools/command-binding.py:124`) would still make K5 flip (the row would still see a
changed digest) and K5 would report `discriminated: true`. That implementation is
nevertheless wrong — it cannot detect `SNAPSHOT_TAMPERED`. It *is* killed elsewhere:
the public selftest's `tampered` case expects `exit 2 / ['SNAPSHOT_TAMPERED']`
(`tools/command-binding.py:176-178`), so the aggregate counter's K1-K4 control
(`control_exit == 0`, `measure.py:73-79`) fails and the wave cannot reach 11/11. K5 in
isolation therefore has less power than its name suggests; the wave's aggregate is
what carries it. The delivered tool does hash the bundle bytes (line 124), so this is
a boundary statement, not a defect in the delivered revision.

### F3 — LOW — the pin is review-enforced, not chained

K5 holds only within a revision. A commit that re-pins the registry literal together
with the bundle defeats it. `contract.json:62` discloses this ("a later commit
changing both row and bundle chooses a new contract"), and no committed artefact
pins `tools/registry.json`'s own sha (the `a8f255f1…` occurrences in
`.ufo/evidence/round-24/source-traces/*.json` are read receipts, not pins). Residual
risk, accepted by the contract.

### F4 — LOW — false-negative direction in row selection

`registry_rows_for` (`measure.py:92-94`) matches the bundle path by exact `argv`
element equality and `status == 'active'`. A row that names the bundle by absolute
path, or via a different spelling, is silently skipped → `reason: 'no-active-row'` →
K5 reports "not discriminated" instead of raising. This fails safe (no false
discrimination), but it would mask a registry edit that moved the row.

### F5 — LOW — `held()` does not verify which row fragment it read

`held()` (`measure.py:97-105`) reads `rows[0]['held']` without checking
`rows[0]['name'] == name`. Safe today (`--only` yields exactly one fragment,
`registry-check.py:851-856`), but a future change to `registry-check`'s report shape
would silently turn K5 into a no-op rather than an error.

## Residual risk and verification gaps

* F1 is the only actionable gap; it is conditional on a committed input
  (`.ufo/evidence/round-23/correct-command-bundle.json`) that a future commit may
  change without any counter change. A later commit could therefore make K5 report a
  false discrimination while the pinned digest literal is absent from the row.
* Head-side counter evidence (`after.json`) is committed as of `04657a6` (evidence-only
  commit; implementation revision unchanged at `c8c5b88`). No further retention gap
  remains for the 11/11 number itself.
* I did not execute the counter, the registry battery or the selftest (lane bound);
  the head-side numbers cited here are consumed from another seat's retained receipt,
  and the K5 flip attribution is derived from the code paths plus an independent
  re-implementation of `evaluate()`. A seat permitted to run the battery should
  confirm the substituted run's `stdout_missing` set equals exactly
  `{'"bundle_sha256": "3d6c99b7…"'}` (one command, on a scratch clone).
* K5 says nothing about the *source-read* row's semantics beyond its own predicate
  (K6); and it says nothing about producer authenticity, continuous checkout
  identity or page coverage — no such claim is made here.

## Smallest safe correction

Do **not** edit the frozen counter: `before.json` and `after.json` both pin
`measure.py` at `0a7f6daa…`, so any byte change invalidates the frozen before/after
pair and would require re-running both plus a contract revision. The smallest safe
correction is therefore additive and out-of-band:

1. Add a *new* predicate (e.g. `K5b`, "pin-fire-attribution") in a future round that
   requires the substituted row's `registry-check` fragment to have
   `stdout_missing == {the pinned digest literal}` and `stdout_tail` still containing
   `"finding_ids": []` with `got == expect.exit` — i.e. assert the *reason*, not just
   the flip. Reuse the fragment already produced by `registry-check.py:728`; the
   change is ~5 lines in the new counter and requires no production-file change.
2. Until then, record the F1 caveat in the round-24 lesson so no later reader treats
   K5's boolean as proof that the digest pin specifically fired.

No production file change is required or recommended by this review.

## Bounds compliance

* Wrote exactly one file: `.ufo/waves/round-24/w1/PredK5.md` (this report). No
  production file, registry row, corpus file or evidence file was created, edited or
  deleted.
* No git/jj write command (add/commit/checkout/reset/stash/push/fetch, mutating jj)
  was run in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; only read-only git
  (`show`, `log`, `status`, `diff`) with `GIT_OPTIONAL_LOCKS=0`.
* No registry battery, gate, selftest or frozen-counter run was executed inside the
  production lane (nor in a clone); the counter's head-side output was consumed as
  retained evidence from `.ufo/evidence/round-24/after.json`. My only executed code
  was my own scratch evaluator at `/tmp/predk5/eval.py` (outside the lane) and
  read-only JSON/sha256 inspection of lane files.
* No subagent dispatch (leaf member). No tools installed or upgraded (pacman is
  paused host-wide; nothing was needed for this review).
* No claim of producer authentication, promotion, historical R17-CMD-BIND closure or
  numeric score uplift.
