# ReviewMinimality — round-15 C1 retained replay source scope (wave 2)

Author-side advisory. Static review only: no checks, builds, tests, gate runs, hashing, installs, pacman, or subagent dispatch. No message sent to TameshiR15, because no implementation-critical defect was found (F1–F5 are wording/scope precision).

## Source read (exact)

- `tools/context-capture.py` — **the file moved during review**: 2116 lines at first read, 2123 at mtime 05:21:21, 2129 at last read. Citations are to the 2129-line state. L1 must re-anchor before quoting. Read: docstring 1–33 and 99–106; `SELF`/`DEFAULT_LANE_ROOT` 121–123; `NOT_COMPARED_LIMITS` 170–174; `KNOWN_ARGUMENTS` 251 and `USAGE` 255–265; `tool_sha256` 303–305; `read_regular` 333–345; `make_result` 1225–1230; `load_expected` 1215–1216; `run_check` 1301–1321; environment predicates 830–873; `recompute_sources` 1020–1038; selftest harness 1582–1726 (`run` 1606–1609, `check_case` child 1648, `usage_case` child 1696, `finish` lane-leak 1710–1716); selftest cases 1731–2025; `parse_argv` 2032–2093.
- `SKILL.md` round-15 section 1609–1691 (negative fixture 1653; registry row 1680).
- `corpus/SOURCES.md:60` (S051); `corpus/lessons/round-15.md` 9–14, 26–41; `.ufo/evidence/round-15/claims.json` (scope field); `corpus/README.md` 195–209; `corpus/QUALITY.md` 75–84; `LOG.md` 925–938.
- Static greps over the tool: `subprocess` occurs only at 1607, 1648, 1696. `open(` occurs at 305 (`SELF`), 345 (`read_regular`), and 1626/1641/1644 (selftest writes under `mkdtemp`). `read_regular` is called only at 1216 (`load_expected`) and 1321 (receipt). `tool_sha256` is called only at 1230. Rate, reuse, and live wording appears only in `NOT_COMPARED_LIMITS` 171 (`kill-rate outcomes`) and in the `result_reuse = not_established` fields.
- Existence only (by `ls`, not hashed): `.ufo/evidence/round-14/context-receipt.json` and `context-missing-env.json` exist.

## Verdict on the target

**Bounded agreement.** No broad live capture, result reuse, or new rate claim was found in the C1 source or registry.

- No capture or execution path: subprocess is confined to the selftest harness. Check mode opens the receipt (1321), an explicit expected pin (1316 → 1216), and the tool's own bytes (305, via 1230). It does not open recorded root paths or run argv.
- Result reuse is pinned to `not_established` (validation near 500–505; fixture 1566/1980). `NOT_COMPARED_LIMITS` (170–174) disclaims kill-rate outcomes, suite environment, and concurrent sibling movement.
- Every C1 surface disclaims a new live experiment, reuse, or rate: docstring 10–14 and 99–104; `SKILL.md:1653`, `1680`, and the closing paragraph; `SOURCES.md:60`; lesson 36–41 (reject list); `README.md` 205–209 ("not … whole-F7 result reuse"); `QUALITY.md` 75–84; `LOG.md` 925–938; `claims.json` scope ("archived live-capture experiment is not rerun").
- The 05:21 edit that added `KNOWN_ARGUMENTS` (251, guard 2065–2068) introduced no new `open`, `subprocess`, or read site (grep unchanged at 305, 345, 1607, 1648, 1696). It does not change the scope analysis.

## Findings (none implementation-critical)

**F1 — registry says check "reads receipt bytes only" (low, wording).** `SKILL.md:1680`. Counterexample: explicit mode also reads the expected pin (1316 → `load_expected` 1216 → `read_regular` 333–345), and every emitted result reads the tool's own bytes (1230 → `tool_sha256` 303–305). Fix: "reads the receipt, its expected pin, and the tool's own bytes; never a recorded root path or argv."

**F2 — "No live lane path is read or written" is literally false (low–medium, selftest isolation wording).** Docstring 26–28. Every selftest child is `[sys.executable, "-I", SELF, …]` (1648, 1696). `SELF` is the live lane file (122), and it is opened on every result (305). The enforced check (`hermetic-no-lane-path`, 1710–1716) only scans child stdout/stderr for `DEFAULT_LANE_ROOT`. It does not prove that no lane path was read, so the case name overstates. Fix: "no lane data path is read or written; the tool's own file is executed; outputs are scanned for the lane root."

**F3 — source-digest predicates bind only receipt-internal strings (low, scope precision; most relevant to target).** `recompute_sources` 1020–1038 compares stored strings: `probe.sha256` vs `probe.declared_sha256` (1022), `runner.sha256` vs `runner.manifest_declared_sha256` (1031). It also requires stored flags to be literal True (1026–1029, 1035–1038). No live probe, runner, or manifest bytes are hashed. The only byte binding is the receipt digest pin (`FROZEN_RECEIPT_SHA256` / `expected.receipt_sha256`). Concrete consequence: a pinned receipt whose declared digests agree still returns `context_consistent` exit 0 after `tools/pin-disposition.py` on disk has changed. The docstring (99–100) says the digest pin is the integrity authority, but `SKILL.md` 1680, the §retained-check paragraph, S051, and the lesson say "re-derives each predicate from the stored raw fields" without stating that source predicates are not a live source binding. Fix: add "source-digest predicates compare retained declarations only; no current probe/runner/manifest bytes are hashed."

**F4 — "stored booleans never trusted" is literally false (low, doc accuracy).** Docstring 38 and `USAGE` 265 say stored derived or summary booleans are never trusted. The code requires them: `env_delta_matches_declared` (833, cross-checked at 837), `baseline_has_GIT_DIR` literal False (841), `poison_path_exists` literal False (849), `argv_equal` (865), `cwd_equal` (873), and the source flags (1026–1038). These flags can only add findings. A pass also needs recomputed equality, so no pass-forging counterexample was found. Fix: "stored booleans must be consistent and can never supply a pass."

**F5 — registry cites a negative pin that is not committed (low–medium).** `SKILL.md:1653` says `context-missing-env.json` is "passed with a caller-committed expected pin (schema `tameshi-context-expected-v1`) naming `missing_injected_environment` and exit1". The schema string appears only in `tools/context-capture.py`. No pin file exists under `.ufo/evidence`, `corpus`, or `tools`. The fixture is referenced only in `SKILL.md` and `.ufo/evidence/round-14/guardrails.json:26`, which is a historical helper output. "passed with" also reads as an observed pairing. The section does state that entry commands are declarations, so no live claim is made. Fix: commit the pin with its L1-observed run, or reword to "a caller-supplied pin is required; none is committed in this lane."

**Residual (no action required).** The file name `context-capture.py` and the `capture` token may suggest live capture. The docstring (10–11) disclaims it, so this is reader-risk only. The fixture digests (`1ee9d09…`, `05cb55b…`) are declared, not recomputed here.

## Verification gaps

- No execution performed: selftest, `--check`, frozen replay, and digest comparisons are all unrun. Every claim above is a static reading.
- Digests of `context-receipt.json`, `context-missing-env.json`, and the tool are not recomputed here.
- Line numbers may shift again as the tool is edited. L1 must re-anchor against the final bytes.
- Tool installs or updates by this seat: none.
