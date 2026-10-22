# SiblingOverlap — round 25, wave 1 (read-only sibling scan)

## Verdict

**No contested scope.** No sibling lane emits mutation-testing-elements (MTE) reports, runs Stryker, or writes a
`mutationScore`. The C2 capability (`tools/mte-interop.py`) is uncontested.

There is one real **adjacency contradiction**, though it is not a scope conflict. Tameshi's `bash-mado-verify` leg
and mado's own `--regression` case use the same ten defect ids (D1–D9, R1) on the same file but at different gate
revisions:

- Tameshi records **4/10 killed** at pin `d7edaab4`.
- Mado records **10/10 killed** at pin `367ff5ec`.

The emitted MTE report keys the file by basename only and carries no lane, revision or pin. A reader of
`bash-mado-verify.mte.json` would therefore see a 40% score for `mado-verify.sh` with nothing to show that mado's
current gate scores 100% on the same ids. The smallest safe correction is to put that provenance in the report
(see Proposed move).

## Axes

- **coverage:** C2 legs conforming, 8/8.
- **adjacency:** no cross-lane misread of a ledger leg; no breakage of downstream consumers.

## Evidence

### 1. No sibling emits MTE reports, runs Stryker, or writes `mutationScore`

These are the per-lane counts of files containing each term. Command, run from the fleet root with
`.git`/`.jj`/`node_modules`/`target` excluded and tameshi skipped:
`rg -l -P '<pattern>' <lane>`.

| term | lanes with hits (files) |
|---|---|
| `mutation-testing-elements` | kagi 2, kama 23, kumitate 10 |
| `mutation-testing-report*`, `mutation-testing-metrics` | revenger 1 |
| `stryker` (case-insensitive) | kagi 2, kaidoku 1, kama 33, kumitate 14, mado 3, mori 11, revenger 1 |
| `mutationScore` | **none** |
| `mutmut`, `cargo-mutants`, `mutants.out`, `pitest`, `mull` | kagi 1240, kama 48, kengaku 3, kotoba 2, kumitate 1, mori 8, revenger 1 |

What each hit actually is:

- **kama:** SOURCES rows only, plus knowledge built on them. The rows are:
  - `kama-shokunin/corpus/SOURCES.md:57` (S045, PIT)
  - `:74` (S062, Stryker states)
  - `:75` (S063, PIT `RUN_ERROR`, rejected as universal)

  The knowledge note is `corpus/knowledge/error-is-not-a-verdict.md:32-35`. The only kama tool is
  `tools/error-verdict-census.py:213,424`, which uses a bespoke `killed`/`survived` outcome for its own grid. It
  has no MTE shape.
- **kumitate:** one SOURCES row, `kumitate-shokunin/corpus/SOURCES.md:36` (S023, Stryker states), cited in
  `corpus/lessons/round-35*.md`. No emitter.
- **kagi:** both Stryker hits are nested copies of one census file,
  `.ufo/waves/round-28/sandboxes/ConnSourcesCensus/shared.tsv:7`. That file lists the Stryker states URL as shared
  by `kumitate,kama,tameshi`.

  The 1,240 tool-name hits are also nested sandbox copies. Excluding `**/sandboxes/**` and `**/retained-probes/**`
  leaves two files:
  - `.ufo/waves/round-25/build/RevOnRelease.md:70`, which says "mutmut releases (S005 cites `main`)" (prose).
  - `.ufo/waves/round-26/build/ClockS027-artifacts/chlog.body`.
- **revenger:** `.ufo/waves/kaika-r1/connector.md:120` cites tameshi's S002 (the report schema) as a "model for
  structured evidence ledgers". This is a handoff note, not an emitter.
- **mori:** scan JSON listing kama and tameshi member paths (`.ufo/waves/round-20/falsify/Live*/scan*.json`).
  Not an emitter.
- **mado, kaidoku, kengaku, kotoba:** wave prose, a vendored third-party file
  (`kaidoku .../libsigrokdecode-0.5.3/.../pnpids.txt`), or a sweep jsonl. No emitter.

No sibling lane produces MTE-shaped JSON. I ran `rg -l '"schemaVersion"'` over every sibling `*.json`, excluding
sandboxes and snapshots, and it returned no files.

The sibling mutation artifacts that do exist each use a bespoke shape. Top-level keys observed:

| artifact | top-level keys |
|---|---|
| `game-dev-3d .../r1/mutation-verdicts.json` | `detected`, `verdict`, … |
| `kagi .../c1-mutation-summary.json` | `rows`, `passed`, … |
| `souji census/round-22/mutation-adequacy-oracle258.json` | `mutants`, `summary`, `schema`, … |
| `kengaku .../final-mutation-witness.json` | `killed`, `mutants`, … |
| `mado .../round-18/evidence/measure-mutants.json` | `mutants`, `schema`, … |
| `tsukuroi .../round-23/measure/l1-mutation.json` | `killed`, `results`, `total`, … |

### 2. Lanes that already emit machine-readable mutation results

These are all hand-seeded, single-lane, non-MTE outputs:

- **mado** (`tools/mado-verify.sh --regression`): line-oriented
  `REGRESSION_TABLE <name>: match=… recorded-killed=… measured-killed=… survived=… inconclusive=… flips=…`
  (`mado-verify.sh:2222`). This is byte-format-identical to tameshi's line (`mutate-and-run.sh:1249`), and mado
  derived it from tameshi.
- **kama** (`tools/error-verdict-census.py --json`): grid JSON (`:366`).
- **souji, kengaku, tsukuroi, kotodama, game-dev-2d/3d, lore, kotoba, kake, mori:** per-wave JSON evidence files,
  each with its own schema.

### 3. Runtime coupling: the C2 legs depend on sibling repos

`mutate-and-run.sh:86-93,1315-1350` shows that all eight ledger legs target sibling-lane files:

| repo | legs | revs |
|---|---|---|
| kumitate | 4 | `175de6ba`, `364f1d59`, `0acb7752` |
| kagi | 2 | `fecee874` |
| tsukuroi | 1 | `165307fe` |
| mado | 1 | `eead56b2` |

The legs are read with `git show rev:path`, behind a repo-identity guard (`:1104-1133`). `mte-interop.py:280-282`
symlinks every sibling that has `.git`.

All four target repos have `.git` and `.jj`. Every pinned commit exists and is reachable from named refs, so a
sibling gc cannot prune it:

```
$ GIT_OPTIONAL_LOCKS=0 git -C <repo> for-each-ref --contains <rev> | wc -l
kumitate 175de6ba refs_containing=156 (refs/heads/master …)
kagi     fecee874 refs_containing=245 (refs/heads/master …)
tsukuroi 165307fe refs_containing=276
mado     eead56b2 refs_containing=324
kumitate 364f1d59 refs_containing=156 (refs/heads/master …)
kumitate 0acb7752 refs_containing=139 (refs/heads/master …)
```

Sibling working-tree edits cannot move these legs.

### 4. Downstream consumer: mado parses tameshi's runner stdout

`mado-verify.sh:2245` runs `tameshi-shokunin/tools/mutate-and-run.sh` read-only. It depends on:

- the `^MUTATE: ` line (`:2154`);
- the `^CONTROL: GREEN ` and `^MUTATE_RESTORE: OK ` lines (`:2207-2208`);
- the `results.tsv` columns `id<TAB>verdict` (`:2172-2174`).

`tsukuroi-census.sh:2174,2468` mentions the runner in comments only.

At the lane revision the runner is unchanged:

```
$ GIT_OPTIONAL_LOCKS=0 git diff --stat 1f73157 c9ff09f -- tools/
 tools/mte-interop.py                               | 376 +++++
 tools/vendor/mutation-testing-metrics-3.9.0.tgz    | Bin 0 -> 32668 bytes
 .../mutation-testing-report-schema-3.9.0.tgz       | Bin 0 -> 11872 bytes
```

So C2 does not break mado. C1's R23-ROUTED-1 multi-token stdout fixture is in the ruler (round-25 evidence files),
not in the runner. If any C1 or C2 integration does touch `mutate-and-run.sh`, those four output tokens are a
cross-lane contract.

The shared line format is guarded on the C2 side. `mte-interop.py:71` would match mado's `REGRESSION_TABLE` lines
too, but `:316-318` fails with SETUP on any leg or table name outside the fixed eight. A foreign
`REGRESSION_TABLE fixture:` line therefore cannot be silently counted.

### 5. Semantic adjacency: score policy

Tameshi's INCONCLUSIVE verdict covers timeout (exit 124) and an unrunnable suite (126/127)
(`mutate-and-run.sh:539-541`). `mte-interop.py:69` maps it to `RuntimeError`, which is invalid and excluded from
the score.

Kama's sourced lane rule (`error-is-not-a-verdict.md:30-35`; S062 versus S063) records that Stryker excludes
runtime errors while PIT counts `RUN_ERROR` as detected. Tameshi's own S001/S087 (`corpus/SOURCES.md:12,96`) state
that MTE counts `Timeout` as detected.

The mapping is a deliberate lane policy, and it is consistent with kama's rule. It is already pinned by the
`timeout_as_kill` negative control (`mte-interop.py:380`). All eight recorded tables have zero inconclusive results,
so this does not affect the 8/8 counter. **There is no contradiction here, only shared ground.**

### 6. The contradiction (mado leg)

```
mutate-and-run.sh:603  PIN_MADO=d7edaab4…   :604 REV_MADO=eead56b2…
mutate-and-run.sh:616  TABLE_MADO='D1:KILLED,D2:KILLED,D3:SURVIVED,D4:KILLED,D5:SURVIVED,D6:KILLED,D7:SURVIVED,D8:SURVIVED,D9:SURVIVED,R1:SURVIVED'   (4/10)
mado-verify.sh:2030    PIN_MADO='367ff5ec…'
mado-verify.sh:2033    TABLE_MADO='D1:KILLED,…,D9:KILLED,R1:KILLED'   (10/10)
```

The defect descriptions are identical (`mutate-and-run.sh:782-830` versus `mado-verify.sh:2070-2106`, "T6-1 service
sweep"). Tameshi's leg is the pre-hardening baseline; mado's is the post-hardening re-cut (`mado-verify.sh:1888-1932`).

Both tables are correct for their own revisions. The MTE report built by `leg_report()`, however, erases the
difference:

```
mte-interop.py:138  name = pristine[0].name[len('pristine.target.'):]      # → "mado-verify.sh"
mte-interop.py:159-161  {'schemaVersion':'1', 'thresholds':…, 'framework':{'name':'tameshi mutate-and-run.sh'},
                         'files': {name: {…}}}                               # no lane, rev, or pin
```

The same gap applies to kumitate. Four kumitate legs at three different revisions emit four reports with distinct
basenames, but none of them names the lane or the revision.

## Proposed move (one, bounded)

Record target provenance in each emitted report, using the schema's free-form `config` object. In the vendored
3.9.0 schema, the top-level properties are
`config, files, framework, performance, projectRoot, schemaVersion, system, testFiles, thresholds`. Only
`schemaVersion`, `thresholds` and `files` are required, and `config` is "Free-format object that represents the
configuration used to run mutation testing", `type: object`.

Concretely, `leg_report()` would add the following, with values taken from the runner's `PIN_*`/`REV_*` and leg
target path:

```
'config': {'leg': <leg>, 'repo': '<lane>-shokunin', 'path': '<rel path>', 'rev': REV_<X>, 'target_sha256': PIN_<X>}
```

Optionally, `files` could be keyed by `<lane>-shokunin/<path>` instead of the basename.

- **adjacency (improves):** a reader of `bash-mado-verify.mte.json` can see that the 40% belongs to mado's
  pre-hardening `d7edaab4` gate, not the current 10/10 gate. The same holds for kumitate's four legs at three
  revisions.
- **coverage (no harm):** `config` is schema-legal, so schema validity is unchanged. The metrics library computes
  only from `files[*].mutants[*].status` (S087), so the ledger, per-mutant and score checks are unchanged.
- **Synthesis:** this reuses the pins the runner already guards. It needs no new source of truth and no
  sibling-lane edit.

## Risks

- If the `files` key changes, `location` and `source` stay per-file and are unaffected. However, `--emit` file names
  and any consumer that indexes by basename would change. Keeping `files` keyed by basename and using `config` only
  is the zero-risk variant.
- The `PIN_*`/`REV_*` values must come from the runner's committed bytes, as `recorded_verdicts()` already does at
  `mte-interop.py:314`. They must not come from live sibling working trees, which would reintroduce drift.
- Out of scope: this does not reconcile the two mado tables. Both stand as revision-tied records.

## Verification (for the integrator; not run here)

1. Run `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --emit /tmp/<x>` in a
   `/tmp` clone. Expect `MTE_INTEROP: PASS legs_conforming=8/8`, and expect each `*.mte.json` `config.rev` to equal
   the runner's `REV_*`.
2. Run `python3 tools/mte-interop.py --selftest`. It should stay green. Add one negative control: a report whose
   `config` is a non-object must fail the schema check.
3. Run `grep -c '"rev"' /tmp/<x>/bash-mado-verify.mte.json`; the expected result is 1.

## Tooling

No installs or updates. The scan used the existing `rg`, `git` (read-only, `GIT_OPTIONAL_LOCKS=0`), `python3` and
`tar`. Scratch was `/tmp/so-schema`, an unpacked copy of the vendored schema, which I removed afterwards.
