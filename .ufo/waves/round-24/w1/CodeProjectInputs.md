# CodeProjectInputs — `project()` input-validation review (round24 C1)

Lane: `TameshiR24-2.CodeProjectInputs` (leaf, no dispatch).
Subject: `tools/registry-replay.py` → `project()` (lines 72–113) and its public
`--project` CLI (lines 273–284), plus the consumer it publishes for,
`tools/command-binding.py` → `evaluate()` (lines 62–104).
Reviewed revision of the tool: live tree blob
`9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714`
(identical to the rev blob named in `.ufo/evidence/round-24/replay-command.json`).
Consumer blob: `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d`.

**VERDICT: FAIL.** `project()` is a publisher, not a gate, on six of the seven
input axes I was told to attack. It publishes (exit 0, `bundle.json` +
`expected.json` written) bundles that its own consumer refuses with exit 2, it
crashes with a traceback (exit 1, empty stdout) on a retained stream that is
not valid UTF-8, and it can publish a bundle that binds a required command
which exists in no frozen registry while the consumer reports `CLEAN`
(exit 0, `finding_ids: []`). The eleven frozen predicates do not see any of
this: K7–K9 use well-formed fixtures only
(`.ufo/evidence/round-24/measure.py:170-179`), so the calibration signal is
blind to this class.

Method: byte-identical copies of both tools in `/tmp/r24-projectinputs`
(sha256 verified equal to the repo blobs), every command executed there, never
in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; no repo file, jj state or
Git index was touched; no tool was installed (see "Tooling record").

## Axes (godspeed)

| # | Axis | Question | Result |
|---|---|---|---|
| A1 | Malformed rows | Does a non-dict row / missing `runner_result` refuse? | **PASS** — exit 2 `INVALID_OBSERVATIONS`, no bundle |
| A2 | Non-string streams | Does a non-`str` stdout/stderr refuse? | **PASS** — exit 2, no bundle |
| A3 | Missing requirement name | Missing key → refuse; empty string → ? | **PARTIAL** — missing key refuses (`:83-84`); `name: ""` is published and the consumer answers `INVALID_REQUIREMENT` |
| A4 | Duplicate names | Two rows with the same requirement name | **FAIL** — published; consumer answers `DUPLICATE_REQUIREMENT`; report accounting also wrong (F4) |
| A5 | Non-int `got` | `got` = `"0"` / `True` / absent | **FAIL** — published as receipt `exit`; consumer answers `INVALID_RECEIPT` |
| A6 | Bool `held` | `held: 1`, `held` absent | **PASS** — `:89` uses `is not True`; both refuse with `RUNNER_NOT_HELD` |
| A7 | Crash vs exit 2 | Non-UTF-8-decodable retained stream | **FAIL** — `UnicodeEncodeError` traceback, exit 1, no JSON report (F1) |
| A8 | Frozen provenance | Can `--project` publish a bundle binding a command absent from the frozen registry? | **FAIL** — yes; consumer reports `CLEAN` (F3) |

## Findings

### F1 — HIGH — a retained stream that is not UTF-8 crashes the projector instead of exiting 2

`tools/registry-replay.py:92-96`

```python
for stream in ('stdout', 'stderr'):
    text = result.get(stream, '')
    if not isinstance(text, str):
        return 2, {'finding_ids': ['INVALID_OBSERVATIONS']}, None
    if len(text.encode('utf-8', 'surrogateescape')) > max_bytes:
```

`surrogateescape` only round-trips `U+DC80–U+DCFF`. A lone surrogate from
`U+D800–U+DC7F` (which `json.loads` accepts verbatim from a `"\ud800"` escape)
raises inside `encode`. The `--project` path never catches it, so the process
dies with a traceback.

Observed (`/tmp/r24-projectinputs`, fixture `stdout-lone-surrogate.json`,
`runner_result.stdout = "\ud800"`):

```
project_exit: 1
stdout: ""            <- no report at all
stderr tail:
  File "/tmp/r24-projectinputs/registry-replay.py", line 96, in project
    if len(text.encode('utf-8', 'surrogateescape')) > max_bytes:
UnicodeEncodeError: 'utf-8' codec can't encode character '\ud800' in position 0: surrogates not allowed
```

Consequences: the documented contract ("2 invalid or unavailable input",
module docstring line 27) is violated — exit 1 is the "refused (findings)"
code, and the printed report is empty, so a caller parsing `finding_ids` gets
nothing at all. The runner itself never produces such a stream
(`registry-check.py:717,726` decode with `errors='replace'`), so the defect is
reachable only through the public `--project` CLI, i.e. exactly the surface the
frozen ruler drives.

### F2 — HIGH — twelve inputs publish bundles that the consumer refuses with exit 2

`project()` validates only the runner-result shape (`:83-84`), the held flag
(`:86-91`) and the stream type (`:92-95`). Everything the consumer's
`evaluate()` treats as structural is unchecked, yet the projector writes
`bundle.json` **and** an `expected.json` that pins the digest of the invalid
bundle, so the consumer cannot even report tampering — it reports a shape
failure on a correctly pinned artifact.

Observed (each row: projector exit / bundle written / `command-binding.py`
exit / findings):

| fixture | projector | bundle | consumer | consumer findings |
|---|---|---|---|---|
| control (clean) | 0 | yes | 0 | `[]` (baseline) |
| `got: "0"` (non-int) | **0** | **yes** | **2** | `INVALID_RECEIPT` |
| `got: true` (bool) | **0** | **yes** | **2** | `INVALID_RECEIPT` |
| `got` absent | **0** | **yes** | **2** | `INVALID_RECEIPT` |
| two rows, same requirement name | **0** | **yes** | **2** | `DUPLICATE_REQUIREMENT` |
| `requirement.name: ""` | **0** | **yes** | **2** | `INVALID_REQUIREMENT` |
| `requirement` without `expect` | **0** | **yes** | **2** | `INVALID_REQUIREMENT` |
| `requirement` with an extra key | **0** | **yes** | **2** | `INVALID_REQUIREMENT` |
| `requirement.argv: "gate"` (not a list) | **0** | **yes** | **2** | `INVALID_REQUIREMENT` |
| `observations.revision: "abc"` | **0** | **yes** | **2** | `INVALID_BUNDLE` |
| `observations.cwd: "relative/path"` | **0** | **yes** | **2** | `INVALID_BUNDLE` |
| row without `argv` | **0** | **yes** | **2** | `INVALID_RECEIPT` |
| row without `cwd` | **0** | **yes** | **2** | `INVALID_RECEIPT` |

Published artifact for the `got: "0"` case (`out/got-string-out/bundle.json`):

```json
"receipts": [ { "argv": ["gate","--check"], "cwd": "/fixture/clone",
                "exit": "0", "name": "one", ... } ],
"requirements": [ { "argv": ["gate","--check"],
                    "expect": {"exit": 0, "stdout_contains": ["OK"]}, "name": "one" } ]
```

`"exit": "0"` is what `result.get('got')` produced at
`tools/registry-replay.py:103`; `command-binding.py:88` requires
`type(row.get('exit')) is not int` → `INVALID_RECEIPT`. The projector printed
`{"bundle_sha256": "968078…", "finding_ids": [], "rows": 1, …}` and returned 0:
a "successful publication" of an artifact its own reader refuses.

Note on the live path: the real runner sets `got` to a **string** on three
failure branches (`registry-check.py:667` `"non-hermetic"`, `:686`
`"unavailable"`, `:701` `"timeout"`), but all three also set `held = False`,
so `--run` never reaches publication with a non-int `got`. The defect is
therefore confined to the synthetic `--project` surface, which is the surface
the ruler treats as the hardening gate (K7–K11) and the surface a
tampered/stale `observations.json` would arrive on.

### F3 — HIGH — `--project` can publish a bundle binding a command that exists in no frozen registry, and the consumer calls it `CLEAN`

`project()` reads only `schema`, `rows`, `revision`, `cwd` from the
observations (`:74-76`). It ignores the provenance fields `--run` writes into
`observations.json` — `registry_sha256` and `source_requirements_revision`
(`:178-179`) — and the `--project` CLI has no `--requirements` /
`--registry-baseline` option at all (`main`, `:273-284`; the frozen-set check
lives only in `run_replay`, `:137-146`). The published bundle therefore
reproduces whatever requirement set the input file declares.

Observed (`out/synthetic-requirement-out/`): a single row whose requirement is
`{"name": "not-in-registry", "argv": ["echo","hello"], "expect": {"exit": 0,
"stdout_contains": ["hello"]}}` with `runner_result {got: 0, held: true,
stdout: "hello\n"}`:

```
project_exit: 0   bundle_written: true
consumer: {"bundle_sha256": "f10f8105…", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}
```

`"finding_ids": []` — the consumer reports a clean binding of a command that
no frozen registry declares and that was never executed by any runner row of
that registry. The bundle is indistinguishable in shape from the genuine
`.ufo/evidence/round-24/replay/bundle.json` (which is clean for real, see
`.ufo/evidence/round-24/replay-gate.json`, exit 0), so nothing downstream can
tell the two apart without the observations file.

Calibration caveat for any repair: the frozen ruler's own control fixture is
synthetic (`measure.py:161-168`, requirement `"one"`, argv `["gate","--check"]`),
and K10 expects `--project` to exit 0 and write a bundle for it
(`measure.py:181-183`). A repair that makes `--project` refuse any
non-frozen requirement set would break K10 and the control. The safe shapes
are (a) an explicit opt-in frozen-set check (new flag) used by `--run`, or
(b) the projection refusing to *publish* when the observations carry no
`registry_sha256`, with the ruler updated accordingly — the frozen ruler file
itself is part of the contract and should not be edited to accommodate a new
behaviour.

### F4 — MEDIUM — duplicate requirement names corrupt the report's own accounting

`tools/registry-replay.py:99-108`: `live` is a **list** of names but
`revision_pinned` subtracts `len(set(live))` from `len(receipts)`.

Observed:

| fixture | rows | `live_dependent` | `revision_pinned` | truth |
|---|---|---|---|---|
| one external row | 1 | `["one"]` | 0 | 0 pinned ✔ |
| two rows, same name, both external | 2 | `["one","one"]` | **1** | 0 pinned ✘ |
| two rows, same name, one external | 2 | `["one"]` | **1** | 1 pinned ✔ (by luck) |

So a duplicate-name observation makes the report claim that one row is
"revision-pinned" when no row is, and the same duplicate is listed twice in
`live_dependent`. The knowledge entry claims live rows are "listed in
`live_dependent` instead of being silently reported as revision-pinned"
(`corpus/knowledge/replay-projection-hardening.md:19`) — under duplicate names
that invariant is false.

### F5 — LOW — the exit-2 report has a different shape from every other report

`:77` and `:84` return `{'finding_ids': ['INVALID_OBSERVATIONS']}` with no
`schema` key, while the normal path returns
`{'schema': 'registry-replay-report-v1', …}` (`:105-108`). The same one-key
shape is printed by the JSON-parse failure branch in `main` (`:279`). A
consumer that switches on `report['schema']` sees a `KeyError` exactly in the
invalid-input case.

### F6 — MEDIUM (calibration) — the selftest oracle and the ruler cannot see any of F1–F4

`selftest()` (`:199-206`) has nine `--project` cases plus the plan case
(`10/10`), and none of them exercises a malformed requirement, a non-int
`got`, a duplicate name, an empty name, or a non-UTF-8 stream. The registry
row pins that literal: `tools/registry.json:994`
`"expect": {"exit": 0, "stdout_contains": ["REGISTRY_REPLAY_SELFTEST: 10/10 pass"]}`.
The frozen ruler's replay predicates (`measure.py:170-183`) likewise feed only
well-formed fixtures. So `1/11 → 11/11` can be true while every defect above
is live — which is exactly what the round-24 lesson's own gate demands of
future repairs ("repaired only when it can fail", `corpus/lessons/round-24.md:1`).

## Counterexamples (exact commands, observed output)

Probe: `/tmp/r24-projectinputs/probe.py` (fixtures written by me, copies of
both tools, nothing in the repo executed).

```
$ cd /tmp/r24-projectinputs && python3 probe.py
{"bundle_written": true, "case": "control", "gate_exit": 0, "gate_findings": [],
 "project_exit": 0, "report": {"bundle_sha256": "5c9aaf71…", "finding_ids": [], …}}
{"bundle_written": true, "case": "got-string", "gate_exit": 2, "gate_findings": ["INVALID_RECEIPT"],
 "project_exit": 0, "report": {"bundle_sha256": "96807853…", "finding_ids": [], …}}
{"bundle_written": true, "case": "dup-names", "gate_exit": 2, "gate_findings": ["DUPLICATE_REQUIREMENT"],
 "project_exit": 0, "report": {"bundle_sha256": "b10d5f5e…", "finding_ids": [], "rows": 2, …}}
{"bundle_written": true, "case": "empty-name", "gate_exit": 2, "gate_findings": ["INVALID_REQUIREMENT"],
 "project_exit": 0, …}
{"bundle_written": false, "case": "stdout-lone-surrogate", "gate_exit": null,
 "project_exit": 1, "project_stderr_tail": "UnicodeEncodeError: 'utf-8' codec can't encode character '\\ud800' …"}
{"bundle_written": false, "case": "stdout-int", "gate_exit": null, "project_exit": 2,
 "report": {"finding_ids": ["INVALID_OBSERVATIONS"]}}
{"bundle_written": true, "case": "synthetic-requirement", "gate_exit": 0, "gate_findings": [],
 "project_exit": 0, …}
```

Summary table printed by the probe:

```
project_exit=0 bundle=True gate=0 -> control, synthetic-requirement
project_exit=0 bundle=True gate=2 -> got-string, got-bool-true, got-missing, dup-names,
        empty-name, req-missing-expect, req-extra-key, req-argv-string, revision-short,
        cwd-relative, row-missing-argv, row-missing-cwd
project_exit=1 bundle=False gate=None -> stdout-lone-surrogate, held-int-one, held-missing
project_exit=2 bundle=False gate=None -> stdout-int, row-not-dict, row-missing-runner-result
```

The genuine evidence is unaffected: `.ufo/evidence/round-24/replay-gate.json`
records the consumer at exit 0 with `"finding_ids": []` on the real
`.ufo/evidence/round-24/replay/bundle.json`, and the replay run itself
(`.ufo/evidence/round-24/replay-command.json`) shows every active row held.

## Residual risk and verification gaps

- **Unchanged by this review:** the `--run` path, the runner, the real replay
  artifact and the eleven frozen predicates. I did not execute the registry
  battery, the gates or the selftests in the repo (lane bound), so I did not
  re-measure K1–K11; my copies reproduce the same `project()` code path the
  ruler drives, but I make no claim about the ruler's numbers.
- **Not probed:** Windows/non-UTF-8 locale behaviour, `--max-stream-bytes` at
  its default 1 MiB with a >1 MiB surrogate stream (same F1 path), `--plan`
  validation (out of my lane), and the `command-binding.py` side of the pair
  (another lane owns it; I only used it as the consumer oracle).
- **Open question I did not settle:** whether `--project` is *intended* to
  accept arbitrary synthetic requirement sets (the ruler's K10 control needs
  that) or only projections of `--run` observations. The module docstring
  ("replay frozen registry requirements and project a binding bundle", line 2)
  and the tool's own `--requirements/--registry-baseline` options (used only
  by `--run`) point both ways; F3's severity depends on which reading holds.
  My finding stands under either reading: with no provenance check, a bundle
  that binds an undeclared command is published and consumed as `CLEAN`.
- **Residual:** F2's twelve inputs and F1/F3 are all reachable through a
  public, unauthenticated CLI that writes into `--out`; anyone able to run the
  tool can mint an "accepted" bundle without a runner.

## Smallest safe correction

1. **F1 (one line + one branch).** Measure the retained stream with a
   surrogate-safe encoding and treat an undecodable stream as invalid input:
   wrap `text.encode('utf-8', 'surrogateescape')` in `try/except
   UnicodeEncodeError` → `return 2, {'finding_ids': ['INVALID_OBSERVATIONS']},
   None`. Do not change the byte bound's meaning for valid text.
2. **F2/F3 (one authority, no second copy of the shape rules).** After
   assembling the candidate bundle, run the *consumer's own* structural
   predicate on it before publishing — import
   `tools/command-binding.py`'s `evaluate()` (it is import-safe; `main()` is
   guarded) and map its result: `2` → refuse with exit 2
   `INVALID_OBSERVATIONS` (no bundle), `1` → refuse with exit 1 and those
   finding ids, `0` → publish. This keeps one authority for the bundle shape,
   keeps the ruler's synthetic control clean (its fixture satisfies
   `evaluate()`: 40-hex revision, canonical cwd, matching argv, `exit == 0`),
   and closes F2, F3's *shape* half and the duplicate-name case in one place.
   If a frozen-set check is wanted for F3's provenance half, add it as an
   opt-in flag used by `--run` — do not silently break K10.
3. **F4 (one line).** Count rows, not names: keep a per-row `live` flag and
   set `revision_pinned` from the row count; publish `live_dependent` as
   `sorted(set(live))`.
4. **F5 (one line).** Give the exit-2 report the same
   `'schema': 'registry-replay-report-v1'` key as the success report.
5. **F6 (test + registry bookkeeping).** Add one selftest case per named axis
   (non-int `got`, bool `got`, duplicate name, empty name, missing `expect`,
   extra requirement key, non-int revision, non-canonical cwd, missing row
   `argv`/`cwd`, lone-surrogate stream). **Consequence to handle:** the
   selftest prints `REGISTRY_REPLAY_SELFTEST: N/N pass`, and the active row
   `tools/registry.json:991-999` pins the literal `10/10` — the count change
   requires the append-only supersession the knowledge entry describes
   (`corpus/knowledge/replay-projection-hardening.md:23-26`): mark the current
   row `status: superseded` with `superseded_by`, and add a new active row
   carrying the new literal. Re-run the frozen ruler afterwards to confirm
   K7–K11 still discriminate (the ruler file is contract; do not edit it).

## Tooling record

No package was installed, upgraded or removed in this lane; the review needed
only the Python 3.14.8 interpreter already present
(`/usr/bin/python3`, `python3 -V` → `Python 3.14.8`). The `godspeed` skill
(`skill://godspeed`) was read and applied; no other skill applied. The pacman
guard was respected: no pacman transaction was attempted.
