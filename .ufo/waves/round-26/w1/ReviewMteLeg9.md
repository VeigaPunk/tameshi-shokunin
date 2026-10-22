# ReviewMteLeg9 — mte-interop.py js-cite-check report construction

Seat: reviewer, leaf member (no dispatch). Scope: `tools/mte-interop.py` — language for `.mjs`,
location from the unique `@old` string, status mapping, and whether the leg's pinned revision
appears anywhere in the emitted report (routed item 4). All paths relative to
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Sources opened this session 2026-10-22.

## Verdict first

- Routed item 4 is **confirmed**: the emitter names its target by bare filename and records no
  lane and no revision pin anywhere in the emitted JSON. For the ninth leg the emitted report
  keys the file as `cite-check.mjs`; neither `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` (rev)
  nor `4057344…` (blob sha256) appears in it.
- Language mapping, `@old`-derived location, and status mapping are correct for this leg; no
  defect found in those three.

## Findings by severity

### F1 [main] — emitted reports carry no lane or revision pin (routed item 4)

Emitter evidence, `tools/mte-interop.py`:

- `:139` — `name = pristine[0].name[len('pristine.target.'):]` — the `files` key is the bare
  pristine basename. The runner names the pristine copy after the basename only
  (`tools/mutate-and-run.sh:489` — `PRISTINE="$WORKDIR/pristine.$(basename "$TARGET_ABS")"`),
  so leg 9 yields the key `cite-check.mjs` with no `kumitate-shokunin/` prefix.
- `:160-162` — the report dict is exactly `schemaVersion`, `thresholds`, `framework`
  (`'name': 'tameshi mutate-and-run.sh'`, constant string), `files`. No other field exists.
- `:336-342` — `--emit` writes `<leg>.mte.json`, `<leg>.spec`, `official-metrics.json`; the
  leg name is only in the filename, never inside the JSON, and no rev travels with it.
- The runner holds the pins — `tools/mutate-and-run.sh:619-620`
  (`PIN_CITECHECK=4057344…c10c9f`, `REV_CITECHECK=1205c662…0b3a`) — and passes them only to
  `regression_case_git` (`:1424-1427`). `mte-interop.py` reads only the leg workdir
  (`spec.copy` `:140`, `results.tsv` `:142-143`, pristine bytes `:138`) and the runner's
  stdout TABLE lines (`:314`); the pins never reach the emitter.

Observed on committed bytes — all eight round-25 emitted reports
(`.ufo/evidence/round-25/mte-reports/*.mte.json`): every `files` key is a bare basename
(e.g. `js-sources-check.mte.json` → `sources-check.mjs`), every `framework` is the constant
runner name, and no 40-hex revision string appears in any of them. Two reports mention lane
names (`mado-shokunin`, `tsukuroi-shokunin`) only inside the embedded `source` bytes, i.e.
incidental target content, not a pin.

Observed for the ninth leg by a `/tmp` probe (code run only under `/tmp/leg9probe`; lane files
read read-only): built a leg dir from the pinned blob
(`git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c662…:scripts/cite-check.mjs`)
plus the committed `sweep/spec.copy` and `sweep/results.tsv`, then ran the real `leg_report`:

```
files keys: ['cite-check.mjs']   top-level: ['files','framework','schemaVersion','thresholds']
framework: {'name': 'tameshi mutate-and-run.sh'}   languages: {'cite-check.mjs': 'javascript'}
40-hex pins in emitted text: none
blob 4057344 in emitted text: False
rev 1205c662 in emitted text: False
kumitate mentioned: True   # only inside the target's own header comment, emitted JSON line 187
```

Impact: an emitted report copied out of its emit directory is not attributable to the pinned
bytes it was built from — the exact routed defect. The full source is embedded, so a consumer
could hash `files[*].source`, but nothing tells them which revision that hash should equal.

Smallest safe correction (recommendation only; I edited nothing):
- Zero-runner-change option: at emit time, read the pristine sha256 the runner already
  produces (`CONTROL: GREEN|RED (exit=… duration-ms=… pristine-sha256=…)`,
  `tools/mutate-and-run.sh:529`, written next to the leg's other evidence; the committed
  round-26 sweep dir shows `control.out` at leg-dir top level) and put it in
  `framework.version` (free-form string per the vendored schema), plus key `files` by the
  repo-relative path. The runner change to also surface the git rev needs a runner→interop
  channel (e.g. a pins line the runner already prints in `REGRESSION_EXPECT`) and is the
  follow-up if the rev pointer (not just the content pin) is wanted.
- I schema-tested the variant in a `/tmp` probe (`uv run --no-project --with
  jsonschema==4.25.1`): `framework.version` set to the rev+blob string and the files key
  changed to `kumitate-shokunin/scripts/cite-check.mjs` produce **no schema errors**. (A top
  level `system` string does NOT validate — the schema types it as an object; do not use that
  field as the pin.) The unmodified emitted leg-9 report itself also validates with no errors.

### F2 [info, no defect] — language for `.mjs`

`:70` maps `.mjs → javascript` (with `.js`, `.sh → shell`, `.py → python`); `:159` applies
`LANGUAGE.get(Path(name).suffix, 'plaintext')`. The vendored schema types `language` as a
plain string oriented to Prism highlighting (no enum), so `javascript` and the `plaintext`
fallback are schema-valid; the probe observed `{'cite-check.mjs': 'javascript'}` and a clean
schema validation. Only note: `plaintext`/`shell` are cosmetic Prism ids, not correctness
issues.

### F3 [info, no defect] — location from the unique `@old` string

`:150-152` — fail-closed: `@old` missing or `source.count(d['old']) != 1` raises `Setup`
(surfaces as `MTE_INTEROP: SETUP`, exit 2, via the handler at `:322`); `:152` then indexes
safely. `:127-131` — `position()` computes 1-based line (newline count + 1) and 1-based
column; end offset is `start + len(old)` (end-exclusive). The selftest pins expected
locations at `:438-441` (`CASE emitter-locations`), including a multi-line `@old`
(`D2 → (2,1,3,9)`) and a mid-line `@old` (`D3 → (3,5,3,9)`).

Real-leg check: extracted the 10 `@old` strings from
`.ufo/evidence/round-26/cite-check/sweep/spec.copy` and counted each in the pinned blob —
every occurrence count is 1 (including the two visually similar `verdict` lines, whose full
strings differ and are each unique). So the uniqueness assert cannot fire for leg 9 and the
locations are well-defined. Probe-observed locations are sane, e.g. `K_MISSING_WORD → line 2519, col 81-135` (single mid-line span), while
`K_EMPTY_VERDICT` and `S_EMPTY_GUARD` both map to the same line 1590 span, col 1-94.

### F4 [info, no defect] — status mapping

`:69` — `KILLED→Killed`, `SURVIVED→Survived`, `INCONCLUSIVE→RuntimeError`. All three targets
are members of the vendored schema's status enum (observed: `['Killed','Survived',
'NoCoverage','CompileError','RuntimeError','Timeout','Ignored','Pending']`), and the probe
report validates. The `RuntimeError` choice is what keeps the ledger equality
`official['totalInvalid'] == recorded['inconclusive']` (`:254`) exact, since the official
metrics count RuntimeError as invalid. An unknown verdict string fails closed twice over:
`STATUS[verdicts[id]]` at `:157` raises KeyError caught at `:322` (SETUP exit 2), and
`per_mutant` (`:257`) uses `STATUS.get(v)` → `None` → mismatch → leg FAILS.

## Residual risk

- `:138/:140/:142` use `read_text()` with the locale-default encoding; the hermetic suite pins
  `LC_ALL=C` only for the node mutant runs, not for the interop process. A non-UTF-8 locale
  could raise or mangle the `source` field. Today's targets are ASCII/UTF-8, so latent.
- Leg 9's report has not been emitted into the lane yet: `glob **/*.mte.json` finds only the
  eight round-25 reports under `.ufo/evidence/round-25/mte-reports/`. My leg-9 emit
  observation is a `/tmp` probe of the same emitter code, not committed lane bytes.
- `:146` requires spec defect order to equal `results.tsv` row order; both committed copies
  agree today (K_ ids then S_ ids in the same order), but a reorder of either file turns into
  a SETUP, not a silent wrong attribution — fail-closed.

## Verification gaps

- I did not run the official-metrics node step or a live regression (out of scope for this
  seat; the leg dir layout of a *kept* regression workdir is inferred from
  `mte-interop.py:330` reading `workdir/<leg>/sweep.log` and the committed sweep dir layout,
  since PASS removes the workdir, `:344-345`).
- Tooling record: no permanent installs; `jsonschema 4.25.1` pulled into an ephemeral
  `uv run --no-project --with` environment (official PyPI channel) solely for the `/tmp`
  schema probes, because the pacman channel is paused.
