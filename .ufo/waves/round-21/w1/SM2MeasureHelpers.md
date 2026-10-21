# SM2MeasureHelpers — duplicated measurement helpers

**Verdict: done** (read-only inventory + deletion-first consolidation proposal; no lane edits).

**Godspeed axes (this pass):** operability (single place to fix bwrap/GIT leaks), correctness (one envelope semantics), maintainability (delete copies), provenance integrity (frozen ruler bytes untouched), calibration safety (no silent ruler drift).

**Lane snapshot:** `33d03b716d3edcf1d8656d46d6df61801d232c52` (`round-21: freeze C1/C2 contracts, rulers and baselines before dispatch`).

**Tool installs:** none.

---

## Findings

SCORECARD round-18 lists **duplicated measurement helpers** alongside the round-16 `GIT_*` direct-invocation leak (registered wrappers scrub; raw `measure.py` does not). The debt is real: the same five primitives—**SHA-256 digest**, **git-at-rev blob read**, **GIT_* environment scrub**, **private clone + detached checkout**, **bwrap + `env -i` selftest envelope**—are reimplemented with small semantic drift across evidence rulers, live tools, and round-21 counters.

**Already-good pattern (keep, do not “consolidate” by editing):** round-19/20 **coldread selectors** (`importlib` load of frozen `round-18/measure.py`) reuse the credit algorithm without copying ~1.6k LOC of helpers. Round-20 **receipt-measure** delegates counting to staged `measure.py` and only owns runner/fixture helpers.

**Frozen zone (proposal MUST NOT re-byte these):**

| Artifact | SHA-256 | Pin authority |
|---|---|---|
| `.ufo/evidence/round-18/measure.py` | `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` | round-20 `contract.json` → `historical` |
| `.ufo/evidence/round-20/stage/measure.py` | `f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d` | round-20 `contract.json` → `instruments.round20-measure` |
| `.ufo/evidence/round-20/coldread/measure.py` | `48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13` | selector selftest + coldread path |
| `.ufo/evidence/round-21/c1-survivors.py` | `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396` | `c1-before.json` → `ruler_sha256` |
| `.ufo/evidence/round-21/c2-count.py` | `9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2` | baseline receipts at freeze |
| All other `.ufo/evidence/round-{12..20}/**/measure.py` | per-commit | historical round receipts |

---

## Inventory table

Legend: **Y** = pattern present in file body. **Alg** = cold-read credit / counting logic size class, not a helper duplicate.

| File | Lines | Role | sha256 | git scrub | config pins | bwrap | clone | sha helper | env -i | Notes |
|---|---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `round-12/measure.py` | 46 | early blob counter | `b3f60b90323a2913…` | — | — | — | — | — | — | trivial `git show` |
| `round-13/measure.py` | 46 | blob counter | `27f959af9e51dcff…` | — | — | — | — | — | — | |
| `round-14/measure.py` | 48 | blob counter | `a842e03e91d429ed…` | — | — | — | — | Y | — | |
| `round-15/measure.py` | 340 | census ruler | `0669988833e34354…` | — | — | — | — | Y | — | local `git()` subprocess |
| `round-16/measure.py` | 665 | coldread v1 | `03b67f58742a95e8…` | — | Y | — | — | Y | — | selftest sets pins on `env` dict, not inherited scrub |
| `round-17/measure.py` | 1602 | coldread v2 | `d25d3d04cb26ca7c…` | Y† | — | — | — | Y | — | †`GIT_ENV` module constant |
| `round-18/measure.py` | 1659 | coldread v3 (canonical) | `7ca87a7c…` | Y† | — | — | — | Y | — | frozen algorithm source |
| `round-19/measure.py` | 443 | round-19 defect ruler | `7af3e951…` | Y | Y | — | — | Y | — | `clean_env()` |
| `round-19/coldread/measure.py` | 93 | ledger selector | `4c9c74ca…` | Y | Y | — | — | — | — | imports r18; local selftest fixture |
| `round-20/coldread/measure.py` | 113 | ledger selector | `48927bfe…` | Y | Y | — | — | — | — | ~86% line-similar to r19; +override refusal cases |
| `round-20/stage/measure.py` | 268 | receipt instrument | `f34dc233…` | — | — | — | — | Y | — | small `git`/`blob`/`sha256` trio |
| `round-21/c1-survivors.py` | 155 | C1 mutation ruler | `a0ec5547…` | Y | Y | Y | Y | Y | Y | **round-18 detector envelope** |
| `round-21/c2-count.py` | 177 | C2 F5 counter | `9a34f77d…` | Y | Y | Y | Y | Y | Y | duplicates c1 bwrap block in `tool_selftest()` |
| `tools/receipt-measure.py` | 318 | round-20 runner | `a67bffa9…` | Y | Y | — | Y‡ | Y | — | ‡fixture `git init` clone, not lane clone |
| `tools/registry-check.py` | 1920 | live registry gate | `33d0d17c…` | Y | Y | — | Y | Y | — | richest `git_env()` |
| `tools/trace-inputs.py` | 999 | trace gate | `fb1d81f6…` | Y | — | — | — | Y | — | `scrubbed_env(workdir)` + pycache prefix |
| `round-18/defect-probes.py` | 1087 | probe harness | `99297d96…` | Y | Y | Y | — | Y | Y | superset bwrap (fleet bind, `--unshare-pid`) |

**Repo-wide pattern counts (Python, lane tree):** dict-comprehension GIT scrub **4** files; `if not key.startswith("GIT_")` filter **10** files; module-level `GIT_ENV` **2** (r17+r18 measure); explicit `bwrap` **3** (c1, c2, defect-probes; future `tools/env-diff.py` will add a fourth).

**Semantic drift hotspots (operability risk):**

1. **Scrub depth:** `scrubbed_env()` (drop GIT_* only) vs `git_env()` / `clean_env()` (drop GIT_* **plus** `GIT_CONFIG_*`, locks, pager, optional `PYTHONDONTWRITEBYTECODE`) vs r16 selftest (pins on full `os.environ` copy).
2. **bwrap profiles:** C1/C2 share one envelope; defect-probes adds `--unshare-pid`, fleet `--ro-bind`, path mapping; F5 contract (build-spec) adds `--chdir /tmp/w` and seven env profiles—must not collapse into one “generic bwrap” without named profiles.
3. **Clone layout:** c1 fleet mirror + symlinks; registry-check `clone_lane_at_rev`; c2 single-lane clone; receipt-measure synthetic `git init` fixture—same primitive, four layouts.

---

## Deletion-first consolidation proposal

**Principle:** delete duplicate *live* implementations; **never rewrite bytes** of pinned historical rulers. New shared code serves **tools/** and **post-round-21** evidence only; frozen files stay as archival references (hashes in contracts/receipts remain valid).

### Step 0 — Name two envelopes (avoid over-unification)

| Profile ID | Authority | Intended use |
|---|---|---|
| `parent-scrub` | drop inherited `GIT_*` only | mutation rulers spawning bwrap (c1/c2 pattern) |
| `git-child-pinned` | scrub + `GIT_CONFIG_GLOBAL=/dev/null` + `GIT_CONFIG_NOSYSTEM=1` + locks/pager | registry-check, receipt runners, trace-inputs |
| `bwrap-r18-detector` | c1-survivors `selftest()` argv template | C1, tool selftests counted under mutation |
| `bwrap-f5-surface` | round-21 build-spec / c2-contract | env-diff receipts (seven profiles) |
| `bwrap-probe` | defect-probes `sandbox_argv` | round-18 probe harness only (keep local unless probes move) |

### Step 1 — Add one live module (new file, no historical edits)

Create **`tools/tameshi_measure_lab.py`** (stdlib-only, `--selftest` proving envelopes match today’s c1 argv and registry-check `git_env()` JSON-serializable keys):

- `sha256_bytes(data: bytes) -> str` — replace ~12 one-liner copies in **tools/** only.
- `scrub_git_environ(*, pins: bool = False) -> dict` — unifies `scrubbed_env` / `env` / `clean_env` call sites in **tools/**.
- `git_show_bytes(repo, rev, path, env=None) -> bytes | None` — shared by future counters and env-diff pin verification.
- `clone_detached(src: Path, dst: Path, rev: str, *, shared: bool = False, env=None) -> None` — shared by registry-check (refactor caller), env-diff, future rulers.
- `fleet_mirror_workdir(fleet_root: Path, lane_name: str) -> tuple[Path, Path]` — `(work, lane_clone_root)` with sibling symlinks (c1 layout).
- `bwrap_run(work: Path, chdir: Path, inner_argv: list[str], profile: str, *, timeout: int, parent_env: dict) -> CompletedProcess` — dispatches named profiles above.

**Deletion targets in tools/ (after lab selftest green):**

| Remove / inline away | Lines saved (approx.) | Callers retargeted to lab |
|---|---:|---|
| duplicate `sha256_bytes` in `context-capture`, `repeat-control`, `pin-disposition`, `evidence-disposition`, `bash-witness-study` | ~40 | import lab |
| `git_env` / `git_clean_env` / `scrubbed_env` variants in `registry-check`, `pin-disposition`, `evidence-disposition`, `bash-witness-study`, `trace-inputs`, `receipt-measure` | ~80 | `scrub_git_environ(pins=…)` |
| `clone_lane_at_rev` body overlap with c1 `clone()` | ~35 | `clone_detached` + `fleet_mirror_workdir` |

Do **not** delete `registry-check.clone_lane_at_rev` name until call sites move—wrap lab then delete inner duplicate (deletion-first, not alias forever).

### Step 2 — Future rulers import lab; frozen copies stay

| When | Action |
|---|---|
| Round ≥22 new evidence script | `from tameshi_measure_lab import …` only; no pasted bwrap argv |
| `tools/env-diff.py` (C2) | implement F5 using `bwrap-f5-surface` + `git_show_bytes`; must not edit `c2-count.py` after freeze |
| round-19/20 coldread selectors | **no change** (importlib → frozen r18 is the consolidation) |
| round-18/17/16 measure.py | **no change** (historical + SCORECARD GIT_* leak documented; fix is wrapper-only, already receipt-measure / coldread path) |

### Step 3 — Optional doc-only linkage (zero byte change to rulers)

Add **`corpus/knowledge/measure-lab-envelopes.md`** (round ≥22) documenting profile IDs and which frozen SHA used which ad-hoc copy—helps cold-read without touching pinned files.

### Step 4 — Explicit non-goals

- **No merge of round-17 ↔ round-18 measure.py** (~57-line algorithm diff); frozen independently.
- **No retrofit of c1/c2** to import lab (would change `ruler_sha256`); duplication there is **accepted cost of freeze**.
- **No single mega-bwrap** for defect-probes + C1 + F5 without profile parameter (would harm correctness axis).

**Estimated net deletion (tools/ only, once env-diff lands):** ~150–220 LOC removed, one maintained envelope implementation, operability win on the path SCORECARD named.

---

## Commands run

| Command | Exit |
|---|---:|
| `glob` / `grep` / `read` on paths under `tameshi-shokunin/` | 0 |
| `wc -l` + `diff -q` r17 vs r18 measure, r19 vs r20 coldread | 0 (files differ) |
| Python feature matrix + pattern counts + SHA-256 listing | 0 |
| `git -C …/tameshi-shokunin rev-parse HEAD` | 0 → `33d03b716d3edcf1d8656d46d6df61801d232c52` |

---

## Evidence paths

- This report: `.ufo/waves/round-21/w1/SM2MeasureHelpers.md`
- Debt citation: `SCORECARD.md` (round-18 open work, ~L685)
- Frozen pins: `.ufo/evidence/round-20/contract.json`, `.ufo/evidence/round-21/c1-before.json`, `c2-contract.json`
- Primary duplicate sources read: `c1-survivors.py`, `c2-count.py`, `receipt-measure.py`, `round-{16..20}/**/measure.py`, `registry-check.py`, `round-18/defect-probes.py`

---

## Tradeoffs

- **Freeze vs dedupe:** round-21 rulers intentionally duplicate ~30 lines so receipts stay hash-stable; consolidation applies forward, not backward.
- **Profile proliferation vs one helper:** named profiles cost API surface but prevent the F5/C1/probe semantic collapse that would break counting.
- **importlib pattern vs shared lab:** coldread selectors already avoid copying the big algorithm; lab targets *small* primitives that tools re-copy every round.
