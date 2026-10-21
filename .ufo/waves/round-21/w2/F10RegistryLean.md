# F10RegistryLean — tools/registry.json vs SKILL round-21 registry

**Verdict:** done (read-only audit at `790abd2129f153c13b471e381d454186edbde65e`; no production edits)

**Agent:** TameshiR21.F10RegistryLean  
**Base:** `790abd2129f153c13b471e381d454186edbde65e`  
**Installs:** none

## Godspeed axes

| Axis | Question |
|---|---|
| Count fidelity | Do active/superseded totals match the wave claim? |
| Round-21 delta | Exactly four new public selftests, anchored to `370f2df:1975–1978`? |
| Anchor integrity | Does every `source` resolve to a blob and in-range line? |
| Path hygiene | Duplicates, superseded obsolete paths, absent argv/fixture blobs? |
| SKILL ↔ registry | Does the maintained SKILL table match registered rows (without erasing history)? |

## Commands (exit codes)

```text
git rev-parse HEAD → 790abd2129f153c13b471e381d454186edbde65e (0)
git rev-parse 370f2df → 370f2dffe66f00c3c7412c962bf3e8fcbe75dfdb (0)
git merge-base --is-ancestor 370f2df 790abd… → 0
diff -q <(git show 790abd…:tools/registry.json) tools/registry.json → 0 (identical)
python3 registry audit script (json parse, blob/line checks, diff 370f2df→790abd) → 0
```

Full `registry-check.py --rev 790abd…` replay **not run** (out of scope vs full battery).

## Count claim: 40 active + 4 historical superseded

**Agree.** At `790abd…`, `tools/registry.json` has **44** rows: **40** `status: active`, **4** `status: superseded`, **0** duplicate `name` keys.

| Metric | `370f2df` | `790abd…` | Δ |
|---|---:|---:|---|
| Total rows | 40 | 44 | +4 |
| Active | 36 | 40 | +4 |
| Superseded | 4 | 4 | 0 |
| `kind: selftest` | 21 | 25 | +4 |

The four added active rows are exactly the round-21 selftests (see below). Superseded set unchanged.

**Note:** SKILL.md does not prose-enumerate “40 active”; the maintained table at `SKILL.md:1964–1978` documents four round-21 **instruments** (public CLI + self-invocation column). The wave assignment count is **derived from** `registry.json`, not quoted verbatim in SKILL.

## Four new public selftests (round 21)

**Agree** with assignment framing: four **new registry rows** tagged `new-r21`, each a `--selftest` entry aligned to one SKILL table row.

| Registry row | `source` anchor | SKILL line (`370f2df` = `790abd…`) | `stdout_contains` | Static case count in tool |
|---|---|---|---|---|
| `env-diff-selftest` | `SKILL.md@370f2df:1975` | 1975 `tools/env-diff.py` | `ENVDIFF_SELFTEST: 9/9 pass` | 9 checks (`tools/env-diff.py:148–192`) |
| `wave-route-mix-selftest` | `SKILL.md@370f2df:1976` | 1976 `tools/wave-route-mix.py` | `ROUTEMIX_SELFTEST: 8/8 pass` | 8 cases (`tools/wave-route-mix.py:76–85`) |
| `round21-measure-selftest` | `SKILL.md@370f2df:1977` | 1977 `tools/round21-measure.py` | `ROUND21_MEASURE_SELFTEST: 13/13 pass` | 13 checks (`tools/round21-measure.py:94–131`) |
| `round21-coldread-selector-selftest` | `SKILL.md@370f2df:1978` | 1978 `.ufo/evidence/round-21/coldread/measure.py` | `SELECTOR_SELFTEST: 12/12 pass` | 12 outcomes (`…/coldread/measure.py:72–94`) |

Each anchor line contains the instrument path and a `` `--selftest` `` self-invocation string (**line_match true** for all four).

**Pattern (not a defect):** Round-21 **public** probe/gate commands from the SKILL table are **not** separate `registry.json` gate/probe rows—only the selftests are registered. Same pattern as round 19 (`new-r19` ×2) and round 20 (`new-r20` ×3): LOG.md:1256 notes adding public selftests without expanding full gate replay.

## Source anchor integrity

**Agree:** no anchor points to an absent blob.

- All **44** `source` fields parse as `PATH@commit[:line]`.
- `git cat-file -e commit:PATH` succeeds for every referenced commit/path pair.
- Referenced line numbers (including ranges like `SKILL.md@58e5d53:1923-1932`) fall within file length (**0** out-of-range).
- All registry **argv** script paths and embedded `.ufo/…` fixture paths exist at `790abd…` (**0** missing).

Abbreviation check: `370f2df` → `370f2dffe66f00c3c7412c962bf3e8fcbe75dfdb`; registry uses the **full** hash for round-21 anchors (consistent with round-19 rows).

## Superseded / duplicate / obsolete paths

**Historical superseded (preserved, not deletable evidence):**

| Row | Superseded by | Path note |
|---|---|---|
| `evidence-disposition-round17` | `evidence-disposition-round18` | same script, older dispositions fixture |
| `evidence-disposition-round17-before` | `evidence-disposition-round18-before` | same |
| `evidence-disposition-round14-superseded` | `evidence-disposition-round18` | round-14 fixture retained |
| `trace-inputs-round17-selftest` | `trace-inputs-selftest` | **obsolete path:** `.ufo/evidence/round-17/coldread/trace-inputs.py` → active `tools/trace-inputs.py` |

**Duplicate names:** none.

**Intentional multi-row scripts (not obsolete duplicates):** shared `argv[1]` with distinct row names/flags (e.g. three `tools/repeat-control.py --snapshot` gates, six `tools/evidence-disposition.py --root` rows across active+superseded). These are fixture variants, not copy-paste registry drift.

**Kind labeling drift (cosmetic, pre-round-21):**

- `assemble-round16-selftest`: name contains `selftest`, `kind` is `gate` (runs `--selftest` argv).
- `reattribute-round16-selftest`: `kind` is `probe` though argv is `--selftest`.

No missing `superseded_by` on superseded rows.

## Disagreements / limits (calibration)

1. **“Four new public selftests” vs 25 selftests total:** The registry holds **25** selftest rows lifetime; round 21 adds **4**. Wording is correct if “four new” means the round-21 delta, not total selftest inventory.

2. **SKILL table vs registry coverage:** Four round-21 instruments are documented in SKILL; only selftests are registry-monitored. **Agree** this matches prior rounds; **disagree** with any reading that expects F5/C1 facade **public** CLIs (`env-diff --contract`, `round21-measure --claim`, etc.) to appear as replay rows—they do not at `790abd…`.

3. **Runtime hold not exercised:** Static audit only. Whether `registry-check.py --rev 790abd…` would print `held=40/40 superseded=4` was **not** observed this seat.

## Summary calibration

| Claim | Verdict |
|---|---|
| 40 active + 4 superseded at `790abd…` | **Agree** |
| +4 round-21 selftests since `370f2df` | **Agree** |
| Anchors `370f2df:1975–1978` match SKILL + registry | **Agree** |
| No source anchor → absent blob | **Agree** |
| Obsolete path retained only under `superseded` | **Agree** (`trace-inputs-round17-selftest`) |
| Full registry replay at pin | **Unrun** |

---

Trailer: `.ufo/waves/round-21/w2/F10RegistryLean.md`
