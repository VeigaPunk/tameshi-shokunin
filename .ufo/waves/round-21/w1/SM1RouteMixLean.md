# SM1RouteMixLean — YAGNI review of `tools/wave-route-mix.py`

**Verdict: done** — behaviour-identical lean patch delivered (−230 bytes, 128→121 lines).

## Axes (Godspeed)

| Axis | Assessment |
|------|------------|
| **Size** | Improved: 5385 → 5155 bytes (−4.3%), 7 fewer lines |
| **Operability** | Unchanged: 8/8 selftest, r20 refusal exit 1 + matching stderr |
| **Correctness** | Unchanged: JSON byte-identical on r20 spec; exit 64/2 paths match |
| **Maintainability** | Neutral/slight gain: merged parse branches; no second convention |

## Findings

### Dead / redundant (removed in proposal)

1. **`DEFAULT_CONFIG` constant** — single use; inlined into `--config` default (same path).
2. **Duplicate selftest pass** — list comprehension plus print loop folded into one loop.
3. **`res["roles"]` on stderr-only runs** — `Counter(roles)` now runs only when `--json` (JSON output unchanged).
4. **Docstring round-20 narrative** — historical context lives in SCORECARD/LOG; trimmed exit-line wording only (behaviour docs preserved).

### Not deleted (reasons)

| Candidate | Why kept |
|-----------|----------|
| Indent-based section tracking in `parse_routes` | Live `~/.omp/agent/config.yml` nests `agentModelOverrides` under `task:` while `modelRoles` is top-level; indent gate is required. |
| Comment / blank-line skip | Harmless guard for annotated configs; no size win without behaviour risk on odd YAML. |
| Quote-tolerant regex | Real roles use `provider/model:tag` colons; regex is already minimal for selftest + live config. |
| `seen` set in `provider_of` | Required by `alias-cycle-unrouted` selftest case. |
| `sorted(set(unrouted))` | Dedup affects stderr when duplicate unrouted roles appear. |
| Eight selftest cases | Assignment contract; none are redundant at runtime (each guards a distinct failure mode). |
| `dict(per.most_common())` | stderr share order is count-descending; plain `dict(per)` would change r20 line ordering. |

### Parse simplification (kept behaviour)

- Section headers unified: one `line in (...)` branch sets `ovr` vs `alias`.
- Key/value capture: single `if m and section:` with dict target selection (replaces parallel `elif` arms).

No alternate parser (stdlib YAML, etc.) — would add dependency and violate “never writes / stdlib only” operability.

## Evidence

**Patch:** `.ufo/waves/round-21/w1/patches/SM1RouteMixLean.patch`  
**Scratch copy:** `/tmp/tameshi-r21-SM1RouteMixLean-x/wave-route-mix-lean.py`

### Commands (exit codes)

```text
# baseline (lane file, read-only)
python3 tools/wave-route-mix.py --selftest                    → 0
python3 tools/wave-route-mix.py --spec .ufo/waves/round-20/spec1.json → 1

# lean scratch (identical stdout/stderr on these paths)
python3 /tmp/tameshi-r21-SM1RouteMixLean-x/wave-route-mix-lean.py --selftest → 0
python3 /tmp/.../wave-route-mix-lean.py --spec .../spec1.json → 1
python3 /tmp/.../wave-route-mix-lean.py                       → 64
python3 /tmp/.../wave-route-mix-lean.py --spec /nonexistent   → 2
diff --json outputs on r20 spec                                 → identical
```

### Selftest output (lean scratch, matches baseline)

```text
ROUTEMIX_CASE parse-overrides ok
ROUTEMIX_CASE parse-aliases ok
ROUTEMIX_CASE balanced-ok ok
ROUTEMIX_CASE concentrated-fails ok
ROUTEMIX_CASE boundary-equal-ok ok
ROUTEMIX_CASE unrouted-fails ok
ROUTEMIX_CASE empty-fails ok
ROUTEMIX_CASE alias-cycle-unrouted ok
ROUTEMIX_SELFTEST: 8/8 pass
```

### Round-20 refusal stderr (lean scratch, matches `.ufo/evidence/round-21/routemix-r20-spec1.stderr`)

```text
ROUTEMIX: REFUSE seats=72 max_share=0.4 openai-codex=35/72 zai=20/72 anthropic=13/72 google-antigravity=4/72 over=['openai-codex']
```

## Tool installs

None (stdlib only; no pacman/uv/cargo/npm).

## Tradeoff

Docstring no longer cites “Round 20 lost 35/72…” inline — operability for dispatch is unchanged; historians use SCORECARD / routemix evidence files.
