# SpotRouting2 — round-24 routing items 2–4 at c9ff09f

Judged on: calibration. Revision audited: `c9ff09fb41fb8aac5fc335faf10858ff606bd5df` (tree `48af1936e1aa824bf5b9ca4ada296aa069884803`), read from a detached scratch clone `/tmp/SR2`. Lane HEAD `5b69fb2` is a descendant and was not audited. Source items: `corpus/lessons/round-24-verifier-spotcheck.md:64-66`. Item 1 (`:63`) belongs to C1.

## Verdict

| Item | Status at c9ff09f | Confidence | Why deferred |
|---|---|---|---|
| 2a Ruler output contract registration | **Still open** | High (grep + probe P6) | Registering a contract is a new claim. C1 and C2 do not claim it (`.ufo/evidence/round-25/contract.json`). Lesson routes it forward (`:62`). |
| 2b Replay-bundle row | **Still open** (lesson Erratum L) | High (grep) | Needs a new expected pair and a new frozen before/after. Not claimed this round. |
| 2c MutPins survivors and inconclusive outcomes | **Partly handled elsewhere.** Retained in the round-24 seat report. The ruler still collapses the states. | High (code) / Medium (seat outcomes not re-run at c9ff09f) | Changing the ruler now would invalidate the frozen pair (lesson `:55`). |
| 3a Docstring promises marked at the consumer entrypoint | **Partly handled elsewhere.** SKILL.md carries the correction. The tool docstring is unmarked. | High (read + probes P1, P4) | The lesson asks for marking at the consumer entrypoint, and that is done. Editing the docstring is a production change outside C1/C2. |
| 3b Six declared problems: input validation, surrogate crash, stale-pair atomicity, hooks and out-of-output writes, unbounded and unredacted streams, live-sibling dependency | **Still open.** Each confirmed in code. Items 1–3 reproduced by probe, item 4 by hook probe, items 5–6 by code reading (item 5 also in lesson Erratum E; item 6 disclosed at SKILL.md:2074-2077). | High | Lesson says these are separate declared problems, not one repair (`:65`). Each needs its own predicate. |
| 4a Live and dependency labels versus fully structured revision binding | **Still open.** The distinction is kept in separate fields and disclosed. The structured binding is not built. | High (code) | A new bundle schema is a new claim. |
| 4b Stale consumer locators | **Partly handled.** An append-only correction exists. One table row still cites the old range. One lesson errata is stale. | High | Fix with appended errata, not row rewrites (`:66`). |
| 4c Superseded expectations | **Partly handled.** Disclosed at SKILL.md:2082-2084 and lesson Erratum P. Not fixed. | High (selftest probe) | Superseded rows are historical. Changing one is a registry rewrite. |

Common reason for deferral: the round-25 frozen contract claims only C1 (the three round-23 routed items) and C2 (the mte-interop capability). Items 2–4 sit in neither claim. The contract is `frozen_before_wave: true` and its `non_claims` exclude other work. The lesson routes these items to "the next authorized tameshi round, with new claims rather than retroactive edits" (`:62`). It also says retained tools and counters were not modified after the measured target (`:55`).

## Evidence

### 2a — ruler output contract

- Ruler: `.ufo/evidence/round-24/measure.py`. The docstring (`:1-12`) lists predicates and states no exit map.
- The exit map exists only in code. `measure.py:212` counts `bool(r['discriminated'])`. `measure.py:215` returns `0 if n == len(rows) else 1`.
- Exit 1 also covers an uncaught setup error. `pin_rows` copies the repo at `:122` via `copy_repo` (`:57-59`, `shutil.copytree`). Probe P6 shows a missing repo exits 1. Round-25's `c1-measure.py` documents exit 2 for setup. Round-24 has no such code.
- Stdout is bounded by construction: `measure.py:81` sets `stdout_tail=result['stdout'][-400:]`. Nothing registers that bound.
- No registry row names the ruler. Grep for `round-24/measure|round-24/replay|round-25/c1|c1-measure` over `tools/registry.json`, `tools/registry-check.py` and `SKILL.md` finds only `SKILL.md:2057`, a prose sentence "Frozen ruler: `.ufo/evidence/round-24/measure.py` (eleven predicates)." The gate table has no ruler row. Compare the registry-replay row at `SKILL.md:2052`, which has entry, verdict map, self-invocation, persisted values and write scope.
- Same gap for round 25. `.ufo/evidence/round-25/c1-measure.py` is tracked at c9ff09f and has no registry or SKILL row.

### 2b — replay-bundle row

- Frozen registry pins only round-23 bundles. `tools/registry.json:973-974` pins `.ufo/evidence/round-23/replay/bundle.json`, and `:983-984` pins the round-23 source-read bundle. No row names `.ufo/evidence/round-24/replay/`.
- Lesson Erratum L states this gap and routes it forward: `corpus/lessons/round-24.md:156-159`.
- `registry-replay-selftest` (`tools/registry.json:991-994`, expects `10/10`) is a selftest row, not a bundle pin.

### 2c — MutPins survivors and inconclusive outcomes

- Retained in `.ufo/waves/round-24/w1/MutPins.md`. Verdict lines `:5-7`: drop-token and reactivate mutants survive direct `--only` and are caught only by K5/K6. One-hex mutants are caught by direct `--only`, and their K5/K6 control is false, so the substitution test is inconclusive. Table `:73-80`. Counterexample `:95-97`. Consumer recommendation `:912`: "Treat `--only` as row compliance, not a detector of removal/rollback of the row's own contract; retain K5/K6 beside it."
- The ruler still collapses the states. K5/K6 `pin_rows` (`.ufo/evidence/round-24/measure.py:119-136`) sets only `control`, `substituted` and a boolean `discriminated`. The only `reason` it sets is `'no-active-row'` (`:125-126`). K1–K4 `mutant_rows` (`:73-74`) do set `reason='inconclusive'`. So K5/K6 has no inconclusive state. `main()` reads only the boolean (`:212`) and the aggregate exit (`:215`).
- Consumer docs are silent. `SKILL.md`, `SCORECARD.md` and `corpus/knowledge/replay-projection-hardening.md` contain no statement that `--only` is row compliance on pins. The limit lives in `MutPins.md:912` and the lesson at `:56`, which says these outcomes "must remain explicit."

### 3a — docstring promises at the consumer entrypoint

- Marked at the consumer entrypoint: `SKILL.md:2061-2072`. It says the write-scope and exit-map cells are "not reliable safety promises," that the stream limit "bounds bundle publication only," and that a stale pair survives a refused run. It also covers malformed observations, unavailable-input exit 1, and "neither the clone nor this gate is a sandbox." `SKILL.md:2074-2077` marks `revision_pinned=41` as "not declared live, not self-contained." `SKILL.md:2082-2084` marks the superseded row and points to Errata E–P.
- Not marked in the tool file itself. `tools/registry-replay.py:9` still says "each retained stdout/stderr is bounded by --max-stream-bytes." `:18` still says "Writes only under --out." `:27-28` still says exit 2 for "invalid or unavailable input." Probes P1 and P4 exit 1, which contradicts `:27-28`.

### 3b — the six declared problems

1. **Input validation: still open.** `project()` checks top-level shape and row shape (`tools/registry-replay.py:74-84`) and stream types (`:94-95`). It does not check revision or cwd format, or requirement values. Probe P3 publishes a one-character revision (exit 0). `command-binding.py` then exits 2 with `INVALID_BUNDLE`. Probe P5 prints a plan for a missing repo and exits 0.
2. **Surrogate crash: still open.** `registry-replay.py:96`, `text.encode('utf-8','surrogateescape')`, is not caught. Probe P1 exits 1 with `UnicodeEncodeError: … surrogates not allowed`. The documented exit for invalid input is 2.
3. **Stale-pair and publication atomicity: still open.** `publish()` returns early without clearing `--out` (`:117-118`). It then writes three files in sequence (`:122-127`). Probe P2: a refused run exits 1, but the earlier pair survives, and `command-binding.py` on that pair exits 0 with `finding_ids: []`. Lesson Erratum O (`round-24.md:191-196`) reports the same.
4. **Hooks and out-of-output writes: still open.** The replay clone is made with plain `git clone` and a detached `checkout` (`registry-replay.py:153-154`), with no `core.hooksPath` override. The runner's `--rev` clone passes `-c core.hooksPath=/dev/null` (`tools/registry-check.py:786-788`). Hook probe H1 vs H2 (below) shows the difference. Rows run in the replay clone (`registry-replay.py:170`) and reach live siblings through symlink mirrors (`:160-161`). The docstring admits "not write-isolated" (`:19-20`).
5. **Unbounded and unredacted streams: still open.** `--run` writes complete streams to `observations.json` before any limit check (`registry-replay.py:181-183`). `project()` runs afterward (`:184`). The rows retain complete streams (`:170`, and `registry-check.py:724-726` with `retain_streams`). `STREAM_LIMIT` refuses publication only (`:96-98`). No redaction exists. Lesson Erratum E (`round-24.md:86-90`) and Erratum K (`:147-149`) agree.
6. **Live-sibling dependency: still open in code, disclosed.** Sibling mirrors are created at `registry-replay.py:160-161`. The live label comes only from a declared `external` flag or the runner's `non_hermetic_argv` (`:99-100`). The runner flags only absolute argv tokens under the live fleet root (`tools/registry-check.py:632-645`). A row that reads a sibling store through a relative path is therefore counted as revision-pinned (`registry-replay.py:107`). Disclosed at `SKILL.md:2074-2077`. Lesson Erratum H (`round-24.md:125-127`, `:182-185`) gives the wider scope.

Handled items inside the same list:
- Realpath identity. `plan()` uses realpath (`registry-replay.py:63-69`). Probe P5 shows the realpath of the given path.
- Runner digest from the clone copy. `registry-replay.py:162-163` hashes the clone's runner. There is no predicate for it, per `corpus/knowledge/replay-projection-hardening.md:71`.
- Not-held and cleanup refusal. `registry-replay.py:86-91` and `:109-110`. The stale pair (probe P2) persists after these refusals.

### 4a — live labels versus structured binding

- The bundle dict (`registry-replay.py:111-112`) carries `revision` as a string and `cwd` as a mkdtemp clone path. It has no live field.
- Live labels go only to `live-dependent.json` (`publish`, `:125-127`). `expected.json` binds only the bundle digest (`:123-124`). The runner and registry digests appear only in `observations.json` (`:177-179`) and are not bound to the bundle.
- The knowledge entry states the consequence: "the receipt schema still carries no live marker (sidecar `live-dependent.json`, not digest-covered)" (`corpus/knowledge/replay-projection-hardening.md:70`).
- Registry pins are free-text stdout needles: `tools/registry.json:974` and `:984` each carry a `bundle_sha256` substring. MutPins drop-token survivors (`MutPins.md:75-76`) follow from that.

### 4b — stale consumer locators

- `SCORECARD.md:1156` says "bounded by lesson Errata E–L." An append-only correction at `SCORECARD.md:1172-1173` says "bounded by all lesson Errata E–P." `SKILL.md:2083-2084` cites E–P. `LOG.md:1635-1636` says SCORECARD and SKILL "now cite all lesson Errata E–P." The lesson has Errata E–P at `corpus/lessons/round-24.md:86-213`.
- Lesson Erratum P (`round-24.md:211`) says `registry-replay-selftest` is absent from SKILL.md. That is stale. `SKILL.md:2052` and `:2078-2079` name it.
- Locators checked and current at c9ff09f: `tools/registry.json:974,984` (cited by MutPins), `:944-945` and `:976` (the supersession edits cited by MutPins; status superseded at 944 and active at 976), and `.ufo/evidence/round-24/measure.py` (`SKILL.md:2057`).

### 4c — superseded expectations

- `tools/registry.json:931` expects `COMMAND_BINDING_SELFTEST: 38/38 pass` on the superseded row `command-binding-selftest`. Its status is superseded (`:933`) and its successor is `command-binding-selftest-r24` (`:934`). The active successor (`:964`) expects `44/44`.
- Probe S0 (below) shows the tool prints `44/44`. The superseded needle `38/38 pass` cannot match.
- Superseded rows still run (`tools/registry-check.py:30-34`). They are excluded from the held tally, as lesson Erratum P states (`round-24.md:203-206`). The disclosure is at `SKILL.md:2082-2084`.

## Commands and observed output

All probes ran in `/tmp/SR2` (detached at c9ff09f) or in `/tmp/sr2-probes` and `/tmp/sr2-hooks`. The fixture is one observations row: requirement `{name:'one', argv:['gate'], expect:{exit:0}}`, `got:0`, `held:true`, `stdout:'ok'`, plus a top-level revision and cwd. Each probe changes one field.

| Probe | Command | Observed |
|---|---|---|
| P1 | `python3 tools/registry-replay.py --project p1.json --out p1-out --json` (row stdout `"\ud800"`) | exit 1; last stderr line `UnicodeEncodeError: 'utf-8' codec can't encode character '\ud800' in position 0: surrogates not allowed` |
| P2a | same fixture, clean, `--out D` | exit 0; `finding_ids: []`; bundle_sha256 `f737e6bc…` |
| P2b | `held:false` fixture, same `--out D` | exit 1; `finding_ids: ["RUNNER_NOT_HELD"]`; `D/bundle.json` still present |
| P2c | `python3 tools/command-binding.py --bundle D/bundle.json --expected D/expected.json --json` | exit 0; `finding_ids: []` |
| P3a | fixture with revision `'b'` (top level and row), `--project` | exit 0; bundle published |
| P3b | `python3 tools/command-binding.py` on the P3a pair | exit 2; `finding_ids: ["INVALID_BUNDLE"]` |
| P4 | `python3 tools/registry-replay.py --run --repo /tmp/SR2 --rev HEAD --requirements /tmp/sr2-probes/nope.json --registry-baseline /tmp/sr2-probes/nope2.json --out p4-out` | exit 1; `FileNotFoundError` (documented exit 2). No row ran. |
| P5 | `python3 tools/registry-replay.py --plan --repo /tmp/sr2-probes/no-such-shokunin --json` | exit 0; `{"fleet_root": "/tmp/sr2-probes", "repo": "/tmp/sr2-probes/no-such-shokunin", "siblings": []}` |
| P6 | `python3 .ufo/evidence/round-24/measure.py --repo /tmp/sr2-probes/no-such-repo` | exit 1; `FileNotFoundError` from `pin_rows` copy (`measure.py:122`) |
| S0 | `python3 tools/command-binding.py --selftest` | exit 0; `COMMAND_BINDING_SELFTEST: 44/44 pass` |
| S0b | `python3 tools/registry-replay.py --selftest` | exit 0; `REGISTRY_REPLAY_SELFTEST: 10/10 pass` |
| H1 | Scratch `HOME` whose `.gitconfig` sets `[init] templateDir = /tmp/sr2-hooks/template`. A template `post-checkout` appends to `marker.txt`. `GIT_*` variables stripped as `registry-replay.py:57-60` does. Then `git clone --quiet --no-hardlinks /tmp/SR2 X` and `git -C X checkout --quiet --detach <rev>` (the replay's own sequence, `:153-154`) | marker lines: 2 (clone and checkout both ran the hook) |
| H2 | Same environment, `git clone -q --no-hardlinks -c core.hooksPath=/dev/null /tmp/SR2 Y` (the runner's `--rev` clone, `registry-check.py:786-788`) | marker lines added: 0 |

## Smallest safe corrections (none applied; no production file edited)

- **2a.** Append a SKILL.md gate-table row or errata line for `.ufo/evidence/round-24/measure.py`. Exit 0 means every row discriminated (`:215`). Exit 1 means any row not discriminated or an uncaught exception (P6). There is no exit 2. The K1–K4 `stdout_tail` is capped at 400 characters (`:81`). Documentation only.
- **2b.** Keep Erratum L. Add no pin this round. A pin needs its own expected pair and is a new claim.
- **2c.** Append to the SKILL.md registry section the `MutPins.md:912` limit: `--only` is row compliance, keep K5/K6 beside it, and a control-false run is inconclusive, not a kill. Keep `MutPins.md` as the record. A tri-state field in the ruler is a new claim.
- **3a.** In the next authorized round, add a one-line pointer at `registry-replay.py:9`, `:18` and `:27-28` to `SKILL.md:2061-2072`. That is a production docstring edit and is not done here.
- **3b.** Each is a new claim with its own before/after predicate:
  - (a) validate revision, cwd and requirement values before publish;
  - (b) map the `UnicodeEncodeError` path to exit 2;
  - (c) write to a temp directory and rename, or clear the pair before publish;
  - (d) add `-c core.hooksPath=/dev/null` to the replay clone at `:153`, as `registry-check.py:787` already does;
  - (e) bound or redact `observations.json` and the retained streams;
  - (f) carry a live marker in the bundle and bind it, and count `revision_pinned` only for rows with no sibling reads.
- **4a.** A structured binding object (repo, rev, tree, clean flag, registry_sha256, runner_sha256) in a new bundle schema, with its own frozen pair. New claim.
- **4b.** Append an errata line to SCORECARD saying E–P is the current pointer, without rewriting `:1156`. Append a lesson errata line saying Erratum P's "absent from SKILL.md" is stale.
- **4c.** No edit. Keep `SKILL.md:2082-2084` as the disclosure.

## Gaps and residual risk

- Not re-run at c9ff09f: the full round-24 ruler, `registry-check --only` on the pins, and the K5/K6 inconclusive results. The K5/K6 outcomes are taken from `MutPins.md` at c8c5b88, plus code reading at c9ff09f. I did not diff `measure.py` between c8c5b88 and c9ff09f.
- Not run: `registry-replay.py --run`, which would execute the 43 rows. The stream-retention finding rests on code (`:181-183`) and Erratum E.
- Lesson-reported and not probed: the two-sibling collision crash (Erratum G), the unusable-`--out` traceback (Erratum O), the `--tag new-r23` vacuity (Erratum P, round17 F5), and the security notes (Erratum K).
- Hook probe H1 used a template hook under a scratch HOME. Operator global hooks were not checked, and the seat's `CodePublish` probe was not re-run.
- Reading of "bounded output contract": I took it to mean the ruler's stdout schema plus its exit map. The lesson does not define it further.
- Adjacent: round-25's `c1-measure.py` is also unregistered at c9ff09f. If C1 registers its own counter, that narrows the gap for round 25 only. The round-24 ruler stays unregistered.
- Calibration: the "partly handled" verdicts for 3a and 4b depend on reading "at the consumer entrypoint" as SKILL.md. If the main agent reads it as the tool docstring, 3a becomes "still open" and the marking is a production edit.

## Tooling record

Tool installs or updates: none. Writes: this report only. Scratch paths outside the lane: `/tmp/SR2` (detached at c9ff09f, kept for reproduction), `/tmp/sr2-probes`, `/tmp/sr2-hooks`.
