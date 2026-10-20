# SimplifyNewTools — YAGNI review of the round-17 tool set

Seat: `TameshiR17.SimplifyNewTools-2` (wave 2, falsify lane; **advisory only — nothing edited**).
Target rev: `eb7838b16490ca7ba17ea3242ade76a61f744af2` (lane clone; the five reviewed tools are byte-identical to the live worktree, §7).
Scope and size (at the target rev):

| file | lines |
|---|---|
| `tools/registry-check.py` | 1314 |
| `.ufo/evidence/round-17/measure.py` | 1499 |
| `.ufo/evidence/round-17/coldread/trace-inputs.py` | 966 |
| `.ufo/evidence/round-17/coldread/assemble.py` | 1637 |
| `tools/evidence-disposition.py` (v2 path) | 2878 |
| **total** | **8294** |

Method: AST reachability + unused-name scan; `ruff 0.17.1` (`F`, `E9`, `ARG`, `B007`); `vulture 2.16`; option provenance against `tools/registry.json`, `SKILL.md` and the wave-1 dispatch interface at the target rev; direct execution of all five selftests; two targeted divergence probes (sectionizer, lane-path predicate). Every item below is a deletion/simplification **candidate**; none was applied.

## Verdict

The new tools are busy but not hollow: every selftest passes, no imports are dead, and the writer/verifier split between `assemble.py` and `measure.py` is deliberate. The real weight is (a) one unreachable selection branch plus a handful of dead locals/params/classes, (b) **three duplicated authorities that have already drifted** — the sectionizer, the lane-path predicate, and the round-17 ledger-path literal — and (c) roughly 200 lines of selftest-only override surface (`--ledger-file/--ledger-rev/--inputs-overlay`) plus three test-only path-classification options. The drift items are the ones that can silently cost a cold-read bucket credit, so they outrank the pure deletions.

---

## 1. Dead code (confirmed)

| # | Location | What | Evidence | Candidate action | Tradeoff |
|---|---|---|---|---|---|
| A1 | `tools/registry-check.py:534-538` | `if only is not None and not selected:` branch (`--only … is excluded by --tag …`) is unreachable. If `tags` is non-empty and filtering empties `selected`, line 529-533 already returns 2; if `tags` is empty, `selected` cannot be empty after the `only` match at 518-523. | Direct `evaluate(root, reg, only="ok-row", tags=["beta"], …)` → exit 2, `error="--tag ['beta'] selects no registry row"`, `"excluded by --tag" in error == False`. Selftest `only-tag-conflict` (`registry-check.py:1112-1117`) asserts only `returncode == 2`, so it passes through the earlier branch and does not pin the message. | Delete 534-538 (or move the only/tag conflict test before the `tags` block if the specific message matters). | None; no reachable behavior changes. |
| A2 | `tools/registry-check.py:502` + `:273-287` | `load_registry` returns `(rows, data, error)`; the only caller discards `data` (`rows, data, error = …`). `data` exists only as an intermediate for validation. | AST unused-local scan; `grep -n load_registry` shows one caller. | Return `(rows, error)`; keep `data` internal. | Tiny API churn inside one file; no external importer. |
| A3 | `tools/registry-check.py:426` | `clone_lane_at_rev(root, rev, sha)` never reads `rev` (only `sha` is checked out and compared). | `ruff --select ARG` → `ARG001 Unused function argument: 'rev'`; caller at `:1269` passes it. | Drop the parameter and the argument. | None. |
| A4 | `tools/registry-check.py:245` | `discriminating` is schema-validated (`for flag in ("external", "discriminating")`) but never read anywhere, never printed, absent from all 29 registry rows, and absent from the tool docstring and from the wave-1 registry contract. | `grep -n discriminating tools/registry-check.py` → only line 245; `python3 -c` row-key census shows 0 rows with the key; `grep -c discriminating .ufo/waves/round-17/dispatch1.json` → 0. | Delete it from the flag tuple (keep `external`, which is read at `:360`). | Schema narrows; reintroduce only with a consumer. |
| A5 | `.ufo/evidence/round-17/coldread/assemble.py:146-149` | `class AsmError(Exception)` is never raised or caught. | `vulture 2.16 --min-confidence 60` → `unused class 'AsmError' (60% confidence)`; AST name-load count 0; `Reject` is used 35×. | Delete the class; `main` already catches `OSError` only (`:1551-1555`). | None. |
| A6 | `.ufo/evidence/round-17/measure.py:1233` | `noinput_ledger = ledger_json(inputs_mode='none', traces=False)` is never used. | `ruff --select F,E9` → `F841 Local variable 'noinput_ledger' is assigned to but never used` (1 error, exit 1); vulture same. | Delete the assignment (also removes a pointless JSON serialization). | None. |
| A7 | `tools/evidence-disposition.py:1603` | `SELFTEST_V1_DOC = b'{"schema": "evidence-dispositions-v1"}\n'` is never referenced; only `SELFTEST_V1_REL` is used (`:1888`, `:2430…`). | `vulture` → `unused variable 'SELFTEST_V1_DOC' (60% confidence)`; grep shows the definition only. | Delete, or wire it into the intended v1-document fixture (no test currently expects it). | None today. |
| A8 | `.ufo/evidence/round-17/measure.py:796`; `coldread/assemble.py:1580`; `coldread/trace-inputs.py:919` | Unused loop/unpack variables: `start, heading` in `ledger_json`; `sha` in `_finish`; `base` in the selftest tree walk. | `ruff --select B007` → 4 errors, exit 1. | One-line `_`/`text`/`dirs, files` rewrites. | None. |

Not dead (checked, deliberately kept):
- `trace-inputs.py:266` `Tracer.__init__` and `registry-check.py:1183` `_sigterm` are referenced indirectly (constructor / `signal.signal`), not by call.
- `evidence-disposition.py` `_setup_hist_*` fixture builders are all reachable: 12 definitions, 16 `git_setup=` uses (`_setup_hist_clean` reused 5×, the other eleven once each).
- `check_lines(..., stream=...)` in `registry-check.py:639` *is* used with `stream="stderr"` at `:1165` (I initially suspected it; it is not a finding).

---

## 2. Duplicated helpers — and the drift already present

| # | Helpers | Locations | State | Recommendation / tradeoff |
|---|---|---|---|---|
| B1 | Sectionizer | `measure.py:198-256` vs `assemble.py:153-208` | **Independent implementations of the same ledger key; already divergent** (§2.1). Body similarity 0.23. On the current page both return 58 sections with identical starts/shas (0 `~~~` fences, 0 indented fences in `SKILL.md`), so today's ledger verifies. | Highest-value duplication fix: share one implementation, or add one shared vector table (page snippet → expected `start`/`heading`/sha) to both selftests. Do **not** merge writer and verifier by importing `assemble` from `measure` without keeping `measure` standalone: its selftest copies only `measure.py` into a fixture tree (`measure.py:1291-1297`). |
| B2 | Lane-relative path predicate | `measure.py:292-307` (`canonical_lane_path`), `assemble.py:381-399` (`canonical_path_reason`), `evidence-disposition.py:255-274` (`canonical_relative`) | **Three policies; drift proven** (§2.2). Consequence: `assemble` can emit a ledger entry whose `inputs` key `measure` then refuses as `input-not-blob:<p>`, and `evidence-disposition` accepts `.git` components the other two reject. | Single policy + shared vectors. Keep the different *error shapes* (bool / reason string / exception) if callers need them, but the accept/reject predicate must be one list. |
| B3 | Round-17 ledger path literal | `measure.py:104` `DEFAULT_LEDGER_PATH` + `:125` `IGNORED_INPUTS`; `assemble.py:125-128` `DROPPED_INPUT_KEYS` hardcodes `.ufo/evidence/round-17/coldread/ledger.json` | Must agree or the writer drops a key the verifier still checks (or vice versa). They agree today. | Add a cross-tool assertion (e.g. `assemble`'s selftest asserts its dropped key equals `measure.DEFAULT_LEDGER_PATH`), or move the literal into one documented constant that both copy with a test. |
| B4 | `GIT_*` scrub | `measure.py:133` (constant), `registry-check.py:132-150`, `assemble.py:211-220`, `trace-inputs.py:509-518`, `evidence-disposition.py:364-384` | Five implementations with different hardening (config null, locks, replace/graft, pycache). Each difference is defensible for its actor, but no single statement of the policy exists. | Keep the code; add one SKILL/README sentence or a shared test vector (each tool must drop `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`). |
| B5 | Rev resolution | `measure.py:148-160`, `assemble.py:235-240`, `registry-check.py:409-424`, `evidence-disposition.py:441-456` | Four variants with different strictness (option-like rejection, 40-hex, exact-id, ancestor check). The strictness is purpose-driven; the duplication is the unstated contract. | Pin with vectors; do not collapse into one helper unless the strictness is unified deliberately. |
| B6 | Digest-map validation | `evidence-disposition.py:563-578` (`validate_inputs`) vs `:741-753` (`validate_expected`) | Same loop: canonical path, duplicate check, 64-hex check, differing only in error id and label. | One `_digest_map(raw, label, error_id)` helper. No behavior change. |
| B7 | Path-hygiene walk | `evidence-disposition.py:276-309` (`safe_file`, raises) vs `:491-509` (`live_regular_bytes`, returns `None`) | Same component-wise `lstat`/symlink walk; different failure channel and one read. | Parameterize the failure policy; keep both call sites' messages/finding ids. |
| B8 | SHA-256 readers | `registry-check.py:290-295` (slurp), `trace-inputs.py:501-507` (stream), `evidence-disposition.py:200-201` (slurp), plus inline `hashlib.sha256` in `measure.py:238,336` and `assemble.py:202,296,312` | Low-priority; the stream/slurp split is about file size, not policy. | Leave; mention only so the list is complete. |

### 2.1 Sectionizer drift (reproduced)

`measure.sectionize` toggles on `line.strip().startswith('```')` (`measure.py:215`); `assemble.sectionize` uses `FENCE_RE` with marker matching (`assemble.py:115,163-176`). Two page shapes already disagree:

````
# tilde fence
page: '# Top\n\n~~~text\n# not-a-heading-in-tilde-fence\n~~~\n\n## Real section\n\nbody\n'
measure: [(1,'# Top'), (4,'# not-a-heading-in-tilde-fence'), (7,'## Real section')]
assemble: [(1,'# Top'), (7,'## Real section')]

# 4-space-indented backtick fence
page: '# Top\n\n    ```\n# in-indented-fence\n    ```\n\n## After\n'
measure: [(1,'# Top'), (7,'## After')]
assemble: [(1,'# Top'), (4,'# in-indented-fence'), (7,'## After')]
````

Both also count a heading inside a nested 3-backtick block opened by a 4-backtick fence (shared simplification, not a divergence). Today's `SKILL.md` has 0 `~~~` fences and 0 indented fences (`grep -c '^~~~'` = 0; `grep -c '^```'` = 20), so the current 58-section ledger is stable. A page edit introducing either shape desynchronizes writer and verifier with no error until a bucket loses credit.

### 2.2 Lane-path predicate drift (executed matrix)

```
path          measure  assemble  disposition
'a/b'         True     True      True
'a/.git/x'    False    False     True      <- disposition accepts .git
'a/./b'       False    True      False     <- assemble accepts dot component
'a\\b'        True     True      False     <- disposition rejects backslash
'.git'        False    False     True
'./a','a/','a//b','..','a/../b',''  -> all reject
```

Sources: `measure.py:292-307`, `assemble.py:381-399`, `evidence-disposition.py:255-274`. The `a/./b` row is the live hazard: `assemble` writes it into a ledger entry, `measure` reports `input-not-blob:a/./b`, so the bucket cannot credit.

---

## 3. Options no registered command or SKILL recipe uses

Provenance sources: `tools/registry.json` at the rev (rows below), `SKILL.md:1829-1903`, the wave-1 dispatch interface (`.ufo/waves/round-17/dispatch1.json`), and the tools' own docstrings/USAGE.

| Tool | Option(s) | Used by a registered row? | Used by a SKILL recipe/table? | Other committed caller | Actually used where | Note |
|---|---|---|---|---|---|---|
| `registry-check.py` | `--only` | No (row `registry-check-selftest`, `registry.json:558-577`, passes only `--selftest`) | No (`SKILL.md:1851` lists `--rev`, `--registry`, `--tag`, `--json`, `--selftest`) | none | selftest children `:1102-1122`; USAGE `:101-102`; docstring `:64-66` | Debug seam. Its dedicated conflict message is the dead branch A1. |
| `registry-check.py` | `--root` | No (same row) | No | none | selftest children (`:716,752,782,…`); live mode `main:1291-1295` | Required by the selftest's fixture lanes; SKILL only tells readers to use `--rev`. |
| `measure.py` | `--ledger-file`, `--ledger-rev`, `--inputs-overlay` | No (row `measure-round17-selftest`, `registry.json:579-598`, passes only `--selftest`) | **Explicitly excluded** from the cited form (`SKILL.md:1890-1891`) | none | selftest `:1199-1275`; main `:1385-1492`; overlay merge `:529-546` | Biggest YAGNI surface: ≈200 lines plus the `strict` parameter threaded through `coldread`/`entry_reason`/`trace_reason` and four output fields (`overrides_used`, `trace_gate`, `ledger_source`, `ledger_committed`). Keep only if a future round still needs a constructed red-before; otherwise this is the cleanest deletion. |
| `measure.py` | `--repo` | No for round-17 (the `--repo` in `measure-round16-rev` targets the round-16 copy) | No | none | selftest `call_measure:850`, `:1308` | The only way the selftest can measure its `/tmp` fixture repo; also the general “measure another checkout” knob. Keep. |
| `trace-inputs.py` | `--cwd` | No (row `trace-inputs-round17-selftest`, `registry.json:600-619`, only `--selftest`) | No (`SKILL.md:1885,1902` omit it) | Yes: wave cold-read wrapper (`dispatch1.json` task text: `--root DIR [--cwd DIR] --out FILE -- ARGV…`) | `run_trace:604-607`; selftest `:912` | Operational for this wave; keep and add it to the SKILL line if it stays. |
| `trace-inputs.py` | `--fleet-root`, `--live-lane`, `--home-prefix` | No | No | none | selftest wrapper `:785-787`; defaults `:70-72` used in every production call | Pure test seams so the selftest can build a synthetic fleet under `/tmp`; keep, or derive them from `--root`'s parent to shrink the CLI. |
| `assemble.py` | `--repo` | No (row `assemble-round17-selftest`, `registry.json:621-640`, only `--selftest`) | No (`SKILL.md:1903` lists `--reports`, `--out`, `--expect-skill-sha`, `--selftest`) | none | selftest `:1078,1136,1170,1198,…` | Fixture-repo selector; keep. |
| `assemble.py` | `--expect-skill-sha` | No | **Yes, tool table** `SKILL.md:1903`; not used by recipe step 3 (`:1888`) | none | selftest only | Caller-pinned coverage gate; keep if the flag is part of the published interface, otherwise drop with its `uncovered` branch. |

Everything in `evidence-disposition.py` (`--root`, `--dispositions`, `--json`, `--selftest`) is used by a registered row and SKILL (`SKILL.md:1835,1850`; `registry.json:197,224,273`). `measure.py --rev` and `trace-inputs.py --root/--out` are used by the SKILL recipe even though no registry row calls them.

---

## 4. Preserved contract (what a deletion must not touch)

- `registry-check.py`: report schema `tameshi-registry-check-report-v1`, the `ROW …`/`REGISTRY_CHECK: held=N/M superseded=K` lines, exits 0/1/2/64, superseded rows still run, tag OR-selection, `--rev` clone layout, `non_hermetic_argv` gating.
- `measure.py`: JSON field names/values (`recorded_cases`, `depth_score`, `ledger_legs`, `shonen`, `coldread`, `calibration_restraint_score`, `sources`, and the override diagnostics), the score formula (`2*boxes 1,2,4` + box-3 full-page), and `overrides_used=false` for the cited form.
- `trace-inputs.py`: receipt schema `tameshi-trace-inputs-v1` and the `inputs`/`external`/`lane_reads`/`untracked`/`dropped_home_count` fields; the three path classes must keep their current meaning.
- `assemble.py`: ledger schema `tameshi-coldread-ledger-v2`, rejection reasons (`page-sha-mismatch`, `trace-*`, `noncanonical-input`, `external-input-lane`, …), fail-closed grouping, and the strictest-verdict merge.
- `evidence-disposition.py`: result schema `evidence-disposition-result-v1`, finding ids, the v1/v2 manifest split, `supersedes` lineage checks and the historical-waiver refusal classes (`historical_input_unneeded`, `historical_input_uncommitted`, …).
- Writer/verifier independence (`assemble` builds, `measure` re-checks) is load-bearing; keep the two implementations independent **but pinned by shared vectors** for the sectionizer and path predicate (B1/B2). The trace-receipt checks are intentionally re-implemented in `measure.trace_reason` (`:361-411`) and `assemble.load_trace_receipt` (`:422-467`); that duplication is the point and should stay.

---

## 5. What I checked that held (negative findings)

- All five registered selftests pass at the rev from the clone: `registry-check` 34/34 (exit 0), `measure` 89/89 (exit 0), `trace-inputs` 27/27 (exit 0), `assemble` “all checks passed” (exit 0), `evidence-disposition` 56/56 (exit 0).
- No dead imports in any of the five files (AST import/load scan).
- No unreachable top-level function besides the class/param/local items above (call-graph from `main`/`selftest`/module-level; indirect references — `signal.signal`, constructors, `git_setup=` tables, JSON hooks — accounted for).
- No `if False`, `if 0:`, or `NotImplemented` stubs.
- The v2 path in `evidence-disposition.py` is live: both `.ufo/evidence/round-17/dispositions.json` and `…-before.json` carry `schema=evidence-dispositions-v2`, `supersedes` and `historical_inputs`; running the tool at the clone returned `status=clean`, exit 0, with `expected_inputs_historical` and `historical_text` populated. This is not a judgment on C1/C2, only evidence that the v2 code is exercised.
- `measure.py --rev eb7838b… --repo <clone>` returned `score 6`, `box3_full_page False`, `ledger_present False`, `overrides_used False` (exit 0): no round-17 ledger exists at the target rev, so the default-ledger path currently takes the no-ledger branch — relevant to why the override flags have no committed caller yet.
- `--json` for `registry-check` and `--tag baseline` are both used by SKILL/claim paths, not YAGNI candidates.

---

## 6. Evidence (commands, exits, key lines)

All runs were from the clone `C=<mktemp>/fleet/tameshi-shokunin` at the target rev; no lane root was used as a tool root.

```
ruff 0.17.1 (uv tool) --select F,E9  -> exit 1
  .ufo/evidence/round-17/measure.py:1233:5: F841 Local variable `noinput_ledger` is assigned to but never used

ruff --select ARG -> exit 1
  tools/registry-check.py:426:29: ARG001 Unused function argument: `rev`
  tools/evidence-disposition.py:2386:33: ARG005 Unused lambda argument: `fx`   (selftest fixture signature; ignore)

ruff --select B007 -> exit 1 (4 errors)
  assemble.py:1580:13 sha not used; trace-inputs.py:919:9 base not used;
  measure.py:796:13 start not used; measure.py:796:20 heading not used

vulture 2.16 --min-confidence 60 -> exit 3
  assemble.py:147 unused class 'AsmError' (60% confidence)
  measure.py:1233 unused variable 'noinput_ledger' (60% confidence)
  evidence-disposition.py:1603 unused variable 'SELFTEST_V1_DOC' (60% confidence)
```

```
python3 tools/registry-check.py --selftest          -> SELFTEST: PASS (34 cases), exit 0
python3 .ufo/evidence/round-17/measure.py --selftest -> MEASURE_SELFTEST: 89/89 pass, exit 0
python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest -> SELFTEST: 27/27, exit 0
python3 .ufo/evidence/round-17/coldread/assemble.py --selftest -> SELFTEST: all checks passed, exit 0
python3 tools/evidence-disposition.py --selftest     -> SELFTEST: PASS (56/56), exit 0
```

```
# dead branch probe (imported evaluate from the clone)
evaluate(root, reg, only='ok-row', tags=['beta'], None, None, None, True)
  -> exit 2; error='--tag [\'beta\'] selects no registry row'
     'excluded by --tag' in error == False
```

```
# sectionizer probe (imported both modules from the clone)
tilde fence:   measure 3 sections incl. heading at line 4; assemble 2 sections
indented fence: measure 2 sections;               assemble 3 (heading at line 4)
current SKILL: measure 58 == assemble 58, 0 differing (start, sha256) pairs
```

```
# lane-path matrix (executed functions)
'a/b' T/T/T ; 'a/.git/x' F/F/T ; 'a/./b' F/T/F ; 'a\\b' T/T/F ; '.git' F/F/T
```

---

## 7. Tooling installed and tree integrity

- Installed `ruff 0.17.1` and `vulture 2.16` via `uv tool install` (official PyPI; pacman transactions paused per host ruling), to run the dead-code scan. No other tool changes. No `pacman`/`-Sy`/`-Syu`.
- Scratch clone: `/tmp/tameshi-r17w2-SimplifyNewTools-2-kh4e3G/fleet/tameshi-shokunin` at `eb7838b…`; all executions ran there (or in `/tmp` fixtures created by the selftests).
- Shared-tree check: lane `HEAD` = `eb7838b16490ca7ba17ea3242ade76a61f744af2`; the five reviewed files hash identically in the live worktree and at the rev (`registry-check.py e05cff92…`, `measure.py 4aa01c36…`, `trace-inputs.py ae8310de…`, `assemble.py efa85e08…`, `evidence-disposition.py 22315cc6…`). This report is the only write. Pre-existing untracked wave-2 evidence files in the lane belong to other seats and were not touched.

Trailer: `.ufo/waves/round-17/w2/SimplifyNewTools.md`.

**Verdict:** the round-17 tools hold functionally, but the YAGNI attack lands on duplicated authority (sectionizer and lane-path predicate have already drifted, and the ledger-path literal is duplicated) plus one unreachable branch, one dead class, one dead schema field, and a ≈200-line selftest-only override surface — all advisory; the highest-value deletion is the override surface only if red-before construction is not still needed, and the highest-value non-deletion is pinning the two drifted predicates with shared test vectors.
