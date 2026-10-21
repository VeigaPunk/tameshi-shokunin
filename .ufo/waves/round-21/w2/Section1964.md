# Section1964 — Round-21 gate/probe registry (finite environment differential)

**Verdict:** `no-blocking-gaps`  
**read_rev:** `790abd2129f153c13b471e381d454186edbde65e`  
**SKILL range:** lines 1964–1987 (`### Round-21 gate/probe registry — finite environment differential`)

## Axes (godspeed)

| Axis | Result |
|---|---|
| Factual accuracy (tools, exits, frozen bytes, counts) | Holds at `read_rev` |
| Citation precision (lessons/knowledge/contracts) | Holds; two shorthand/jargon mismatches only |
| Operator clarity (entry commands vs persisted paths) | One ambiguous receipt path shorthand |
| Prose weight (duplicate authorities) | Deletion candidates identified; behaviour unchanged if table kept |

## Scope read

Pinned section text via `git show 790abd2129f153c13b471e381d454186edbde65e:SKILL.md` (lines 1964–1987). Cross-read cited/implied sources at the same revision (no mutation recipes, no F5 `--contract` run, no blind cold-read). One narrow live check: `.ufo/evidence/round-21/coldread/measure.py --selftest` → exit 0, `SELECTOR_SELFTEST: 12/12 pass` (confirms registry/row selftest claim).

## Source re-anchors (agreements)

### Provenance lines 1966–1971

- **`corpus/lessons/round-21.md`:** QUALITY43 at line 79 (`wave-route-mix`, max share 0.40, round20 refuse / round21 accept narrative); QUALITY44 at line 80 (R02 re-anchor). Matches section source line.
- **`corpus/knowledge/hermetic-env-differential.md`:** line 1 cites mined **S079** and reopened **S028** (also documents S081; section does not over-claim S081-only mining).
- **Frozen C1/C2 scripts:** `git diff 33d03b7 790abd2129f153c13b471e381d454186edbde65e -- .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/c2-count.py .ufo/evidence/round-21/c2-contract.json` is empty → “unchanged from 33d03b7” holds (editorial spacing: `from33d03b7` in SKILL is a typo, not a wrong rev).

### Registry table (lines 1973–1978)

| Row | Agreement evidence |
|---|---|
| **`tools/env-diff.py`** | Docstring exits 0/1/2/64 (`tools/env-diff.py:11–12`). `PROFILES` has seven names (`:29`). Selftest cases: invariant, tz, locale, home, columns, repeat, missing-bwrap, timeout, pin-mismatch-public-cli → 9 (`:148–195`), matching `tools/registry.json` `ENVDIFF_SELFTEST: 9/9`. Scratch prefix `tameshi-r21-envdiff.` (`:61`). Contract at pin: 9 surfaces, 7 profile keys, `receipt_path` `.ufo/evidence/round-21/f5/receipt.json`. |
| **`tools/wave-route-mix.py`** | Exits 0/1/2/64 (`:12–13`); default `--max-share 0.40` (`:97`). Selftest 8 cases (`:76–90`); registry `ROUTEMIX_SELFTEST: 8/8`. Example spec `.ufo/waves/round-21/spec1.json` exists with 71 seats (lessons QUALITY43 “28/71”). Round20/round21 spec paths exist; acceptance/refusal is **historical retained observation** (lessons), not selftest-enforced — consistent with “Persisted values” wording. |
| **`tools/round21-measure.py`** | Facade delegates to `c1-survivors.py` / `c2-count.py` (`:23–24`, `:154–158`). Exits 0/1/2/64 per docstring (`:7–8`). Selftest defines 13 checks (`:94–131`); registry `ROUND21_MEASURE_SELFTEST: 13/13`. `--claim c2` drives F5 counter (`c2-count.py` header). |
| **`.ufo/evidence/round-21/coldread/measure.py`** | Selects `LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'` (`:22`). Forbids override flags (`:24`, `:105–108`). Selftest 12 outcomes (`:72–98`); executed 12/12 on host. Main measure returns 0 on successful JSON observation (`round-18/measure.py:1649–1655`); exit 2 setup errors; wrapper exit 64 on forbidden overrides — matches “0 observed; 2 could-not-evaluate; 64 usage/forbidden override”. |

### Footer lines 1980–1987 (current claims)

- **C1 guard kills (child-env / command-pin / not malicious hooks):** Supported by mutant ids MB03–MB10 (env scrub, `core.hooksPath` pins) and lessons `round-21.md:92–94`. **Synthetic process identities:** R05/R07 in `c1-mutants.json:98–108` (registry-check child/starttime guards), not PID-reuse demos — matches “not demonstrated malicious hooks or PID reuse”.
- **C2 repeat / nine classified:** `env-diff.py:classify` treats `clean != clean_repeat` as `nondeterministic` (`:104–106`); `c2-count.py` validates tuple rules including repeat (`:73–82`). “Nine classified ≠ nine deterministic selftests” matches lessons `round-21.md:99–101` and env-diff docstring.
- **Frozen counter scope:** `c2-count.py:4–12` (pins, tuples, `tool_selftest`, `f5_entry`; not producer authenticity). **199-entry prefix:** `ledger.json` has `"entries"` length 199 at `read_rev` (`python` on `git show …:coldread/ledger.json`). **Label authorship / not blind cold-read:** aligns with lessons bounds `round-21.md:113–117` and round-20 coldread row convention (lines 1951–1952).

## Wrong expectations (non-blocking, count 2)

1. **Receipt path shorthand (line 1975, Persisted values):** Table says raw tuples live in `f5/receipt.json`. Frozen contract declares `receipt_path`: `.ufo/evidence/round-21/f5/receipt.json` (`c2-contract.json`). Lessons use the same short form (`round-21.md:99`). Operators must infer repo-relative prefix; not a tool bug.
2. **Exit 2 label “could-not-evaluate” (rows 1975–1977, 1978):** Native docstrings say “setup/input error” / “unreadable spec/config” (`env-diff.py:12`, `wave-route-mix.py:13`, `c1-survivors.py:13–14`, `c2-count.py:11–12`). Numeric exits match; wording follows round-20 registry jargon (SKILL 1947–1951), not stderr tokens.

## Blocking gaps

None. All four tools exist at `read_rev`; registry selftest rows at `tools/registry.json:855–892` cite ancestor commit `370f2df…` whose SKILL gate table matches this section (`git diff 370f2df 790abd2 -- SKILL.md` empty).

## Obsolete / duplicated prose (simplifier — do not edit in this seat)

Deletion candidates that preserve verified behaviour if the **table + one-line scope** remain authoritative:

- **Lines 1980–1987:** Near-duplicate of `corpus/lessons/round-21.md` executed-evidence and bounds (§92–97, §108–117). Keep one authority (lessons + knowledge); SKILL table already encodes machine-facing registry.
- **Lines 1966–1971:** Partial overlap with `hermetic-env-differential.md` header and lessons QUALITY rows; could collapse to `Source: corpus/lessons/round-21.md (QUALITY43–44); corpus/knowledge/hermetic-env-differential.md`.
- **Dual registry:** Four selftest argv/exit summaries duplicate `tools/registry.json` active rows (`env-diff-selftest`, `wave-route-mix-selftest`, `round21-measure-selftest`, `round21-coldread-selector-selftest`). Retain JSON for automation; SKILL table is human index — optional cross-link only, not second copy of expect strings.

## Editorial defects (not counted as wrong expectations)

Missing spaces in SKILL at 1968 (`from33d03b7`), 1976 (`max-share0.40`), 1978 (`selftest0`), 1986 (`the199-entry`) — formatting only.

## Installs

None.

## Evidence artifact

`.ufo/waves/round-21/w2/sections/1964.json`
