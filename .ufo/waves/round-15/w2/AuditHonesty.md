# AuditHonesty — round 15, wave 2 (tameshi-r15-w2)

Seat: `TameshiR15.AuditHonesty` (leaf audit; no subagent dispatch).
Scope: report trend, no-harm, SHONEN authority, and outside admission state for the round-15 integration artifacts, with current missing evidence stated plainly.

**Execution boundary:** static review only. No gate, selftest, build, test, formatter, probe, runner, `git` command, hash computation, or sibling read was executed. Tools used: `read`, `glob`, `grep`, `write`. Tool installs/updates: **none**. `~/.omp/agent/RULES.md` was read; no helper was needed. Not read: `~/.omp/agent/agent.db*`, credential or auth files. No message was sent to `TameshiR15`: none of the findings below is an implementation-critical defect (see §6).

Snapshot caveat: wave-2 sibling seats were still writing when this was read. Everything below is the state at read time, not a final state.

---

## 1. Verdict summary

| Area | Status at read time | Basis |
|---|---|---|
| Report (six sections, trend verdicts) | **Missing, pending L1** | No lane or fleet-root round-15 report exists. |
| Trend verdicts (six axes) | **Missing, pending L1** | No per-axis verdict in lesson, LOG, or SKILL round-15 text. Only `calibration 6→6` (capability, no points). |
| No-harm (historical bytes, sibling reads, writes) | **Bounded agreement by static reading; byte proof pending L1** | Code, SKILL, and round-14 receipt agree on the pinned hashes. I did not hash anything. |
| SHONEN authority | **Agreement: four boxes remain `[~]`; no promotion claimed** | `SHONEN.md:5,7,9,11`; LOG and SKILL state no SHONEN change. |
| Outside admission | **Agreement: pending a separate non-author closure** | Lesson, LOG, SKILL, S051 own-work row, and w1 `OutsideAuthority.md`. No round-15 spot-check file exists. |
| Runtime receipts (selftest, frozen replay, retained check) | **Absent, pending L1 by design** | Not counted as defects. |
| Process disclosures | **Partial in LOG** | Present in the lesson; the round-15 LOG entry omits them (§4.4). |

No counterexample to a *claimed* property was found in the delivered text. Findings are gaps, pending items, and wording that over-reaches the code. None is a proven defect.

---

## 2. Source read (exact)

Repo-internal, read-only:

- `AGENTS.md` (whole file; one-line rule: every change appends a LOG entry with motivating evidence).
- `corpus/lessons/round-14-verifier-spotcheck.md`: lines 1–173 (claim table 117–128; trends 148–152; routed defects 154–162; dispatch digest 164–173).
- `corpus/lessons/round-15.md`: lines 1–94 (whole file).
- `LOG.md`: 828–946. Round-14 closure 834–923; round-15 entry 925–946.
- `SKILL.md`: 1563–1607 (round-14 appendix, for comparison), 1608–1691 (round-15 appendix and registry), raw line 1680–1681 (context and disposition rows).
- `SHONEN.md`: lines 1–12.
- `corpus/SOURCES.md`: rows S049–S051 (lines 58–60), census note (131), source-id list (169–172).
- `corpus/QUALITY.md`: 74–84 (QUALITY17).
- `reports/` listing: `round-1-calibration.md` and `round-1-kaika-coldread.md` exist (SHONEN citation targets).
- `.ufo/evidence/round-15/`: `claims.json` (16 lines, whole), `integration-decisions.json` (13 lines, whole), `sources-before.json` (8 lines, whole), `measure.py` (lines 1–15 header, 182–339 `main`; 16–181 helpers not read in full).
- `tools/context-capture.py` (2123 lines):
  - 1–800 read in full;
  - 804–1363 read in part (environment, runs, verdict, expected, `run_check`, parser ranges);
  - 1364–1733 read in part (selftest harness and first cases);
  - 1728–2002 enumerated by grep (`harness.check_case(`, `harness.usage_case(`);
  - 2020–2116 read (CLI `parse_argv`, `main`);
  - whole file grepped for `subprocess`, `open(`, write modes, `os.replace`, `sys.exit`, `return 64`, finding-ID literals, and `snapshot`.
- `.ufo/evidence/round-14/context-receipt.json`: top-level and `environment` keys (grep; the rest not read).
- `.ufo/waves/round-15/`: `failures.json`, `spec2.json`, `dispatch2.json` (head 1–24, `policy`/`counts`/`compaction`/`note`), `assignments2.json`, `record2.json` (head), `w2/swarm-registry.json` (head).
- `.ufo/waves/round-15/w1/`: `OutsideAuthority.md`, `ReportContract.md`, `GateClassification.md`, `Mistake.md`, `SourcePrimary.md`, `FrozenEvidence.md`, and `SiblingOverlap.md` (whole, although that seat is in the failure list).
- Fleet-root `/home/vgpnk/Projects/shokunin/.ufo/reports/round-14/tameshi.md` (whole) for the report format and round-14 trend/SHONEN precedent.
- Fleet-root `/home/vgpnk/Projects/shokunin/.ufo/reports/round-15/`: listing only (`tsukuroi.md`, `mado.md`, `kaidoku.md`, `kotodama.md`; no `tameshi.md`).

---

## 3. Trend (report) audit

**What exists.** `claims.json` declares one C1 capability, `calibration`, `6→6 bounded capability, no promotion points` (`claims.json:9–11`). `LOG.md:925–946` states "scalar6 unchanged" and "earns no SHONEN points". `corpus/lessons/round-15.md` has Gate, Mistakes, Routed-item disposition, Dispatch, and Process disclosures sections.

**What is missing (pending L1 / closure):**

1. **Report file.** No `tameshi.md` exists for round 15 at either root. Round 14 lives at the **fleet root** (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-14/tameshi.md`; the lesson, round-14 closure, and `git log -- .ufo/reports/round-14/tameshi.md` all use that root). The w1 `ReportContract.md:130` (§8 item 10) instead points at the *lane-relative* `.ufo/reports/round-15/tameshi.md`. **This is a location ambiguity.** L1 must choose the root explicitly, and round-14 precedent points to the fleet root. Not a defect yet; the report simply does not exist.
2. **Six report sections.** The round-14 precedent has Work performed, Landed changes, Before→after measurements, Sources & frontier, Trend verdicts, and SHONEN. Round 15 has no artifact in that shape. The w1 `ReportContract` map is a recommendation only.
3. **Per-axis trend verdicts.** Round 14 recorded verdicts for all six axes (`round-14/tameshi.md:99–103`, 65). Round 15 has none for depth, coverage, operability, freshness, adjacency, or expansion/quality/discernment. The lesson has no "Learning trends" section. LOG round 15 gives only the calibration scalar. Any "improved" wording for round 15 has no artifact behind it yet.
4. **SCORECARD.** No round-15 row. Grep of `SCORECARD.md` for `round.15|R15|S051|context-capture` returns no round-15 hit.
5. **Before→after measurement.** `.ufo/evidence/round-15/measure.py` exists but has not been run (no `before.json`/`after-committed.json` for round 15). `sources-before.json` exists. There is no `sources-after.json`.

**Counterexample check on trend wording (static):** `SKILL.md:1618–1620` and `LOG.md:945` say "no seventh case, no successor sweep, no promotion". Consistent with the code: the gate has no mutation-case path, and the six-leg mapping is unchanged from round 14. No trend claim beyond "calibration 6→6" is made in any delivered artifact, so none is contradicted.

**measure.py reads as proxies, not proof.** `measure.py:223–228, 280–286` decides `context_standalone_selftest_present` from the substring `SELFTEST: PASS` in source text and from `sys.executable` appearing on a line with `selftest`. Its header (`measure.py:260–261`) disclaims "no gate or selftest execution, no runtime proof". Trend text must not cite these counts as capability evidence.

---

## 4. Honesty findings (claim vs code vs artifact)

### 4.1 Gate behavior is as claimed (bounded agreement, static)

- **Mode surface.** `parse_argv` (`tools/context-capture.py:2023–2080`) accepts only `--check`, `--selftest`, `--json`, `--receipt`, `--expected`, `-h/--help`. There is **no** `--snapshot` and **no** prospective-capture mode. `SKILL.md:1638–1639` states the active use is "retained-receipt replay, not a new live experiment".
- **No writes in check mode.** `open(` sites are `tool_sha256()` (302, read of `SELF`), `read_regular` (342, read), and selftest-only writes (1622, 1634, inside `SelftestHarness.check_case`, under `mkdtemp`). `os.replace` does not appear. Matches `tools/context-capture.py:11–12`.
- **Never executes stored argv or probe.** `subprocess` appears only at 1603 (selftest `run`). Matches `SKILL.md:1646–1647` and `S051` row (`SOURCES.md:60`).
- **Exit map.** `main` returns 64 on `UsageError` (2093) and writes `id=usage_error` to stderr; `run_check` emits 2 for `CouldNotEvaluate` kinds; `emit` returns the recomputed exit (1 for findings, 0 for clean). Matches `SKILL.md:1681` (`0 clean; 1 failed; 2 and 64 could-not-evaluate`).
- **`snapshot_tampered` is implemented** as a receipt-digest pin mismatch (`run_check` 1324–1333, exit 2). It is not a separate snapshot directory. Acceptable under the lesson's admit criterion ("persisted snapshot bytes are digest-checked before interpreting their retained verdict"). It does mean the w2 spec's "digest-bound snapshot mode if needed" has been realised as a receipt pin, not as a new mode (see §4.3).
- **Pins.** `FROZEN_RECEIPT_SHA256 = 05cb55…899c1a` (`tools/context-capture.py:137–139`), `FROZEN_TOOL_SHA256 = 7313e9…7d89` (140–142). The same literals appear in `SKILL.md:1633` and `SKILL.md:1656` (receipt), and the tool digest also appears in the round-14 receipt (`context-receipt.json:4`). **Three sources agree; I did not hash the files.**
- **Import surface.** Stdlib only (`copy, hashlib, json, os, re, shutil, stat, subprocess, sys, tempfile`). The archived script is not imported (matches `FrozenEvidence` reconstruction).
- **Round-14 key sets.** Top-level keys of `context-receipt.json` (19) match `RECEIPT_KEYS` (19) by name, and its 10 `environment` keys match `ENVIRONMENT_KEYS`. I did not check the `runs`, `comparison`, `positive_control`, `mapping`, or `sources` sub-keys against the validator; they are L1 concerns.

### 4.2 Over-broad wording in the tool docstring (not implementation-critical)

- `tools/context-capture.py:9–11` says the tool "does not read live lane inputs". Frozen mode reads `FROZEN_RECEIPT_REL` under `DEFAULT_LANE_ROOT` (`run_check` 1301–1302), and `SKILL.md:1639` says so.
- `tools/context-capture.py:27–28` says for `--selftest`: "No live lane path is read or written". Every selftest child still reads its own script file (`SELF`) and `make_result()` calls `tool_sha256()`, which opens `SELF` (302, 1227). The interpreter must read the script. This is an unavoidable self-read, but the literal sentence is inaccurate.
- The **SKILL row is accurate**: `SKILL.md:1681` says "check reads receipt/expected bytes and its own source for a reported digest". Trend and no-harm text should quote the SKILL wording, not the docstring.

### 4.3 Declared scope vs delivered behavior

- **Prospective capture is not delivered.** `spec2.json` "Integration interface" says "Normal prospective capture writes round15 only; never overwrite round14." The delivered tool has no capture path. `.ufo/evidence/round-15/integration-decisions.json:4–5` records "Promote a maintained retained-receipt gate, not a second live environment experiment" and "check-only cutover". `SKILL.md:1638–1639` discloses this. **`LOG.md:935–936` does not** (it says only "public isolated CLI self-invocation and retained-receipt replay"), and `corpus/lessons/round-15.md` does not mention it. The decision is recorded in one JSON file, not in the lane's audit trail. Closure should state it in LOG and the report.
- **Legitimate reading of QUALITY17.** `QUALITY.md:80–82` says "retain the unsupported old invocation alongside the same-command repaired result". No round-15 artifact retains the old invocation (`capture-context.py --selftest` → exit 64 per `capture-context.py:605–613`). **Pending L1** (`Mistake.md` C4).

### 4.4 Disclosure completeness

- The lesson (`round-15.md:75–94`) discloses: ten failed build seats (nine scouts, one connector; `failures.json` lists the same ten identities), routing change then supersession (m_flash → m_fast/m_haiku/m_swe/m_sol), mid-flight disclosures by SpecClean, SpecMismatch, SpecTypes, and SpecEnvironment, and that none of their outputs are credited as C1 evidence. **Good.**
- **`LOG.md:925–946` discloses none of these.** Per `AGENTS.md:3`, LOG is the change record. This is a documentation gap that closure must fill.
- **Failed-seat artifact present.** `failures.json` lists `TameshiR15.SiblingOverlap` as failed (no replacement). `w1/SiblingOverlap.md` nevertheless exists and is a substantial report. Its `failures.json` status is "partial reports uncredited advisory". Treat it as **uncredited**. It also proposes names that the delivered tool does **not** have (`--check-receipt`, `mismatch_normalized`, `control_ineffective`, `source_pin_mismatch`, `missing_input`, `usage_error`-as-only-usage); see §4.5 item 2.
- The `w1` seats that completed (`ReconNames`, `ReconTimestamp`, `ReconEnvironment`, plus the reports listed in `OutsideAuthority.md` and others) are advisory only (`OutsideAuthority.md:3–5`, `Mistake.md:3`).

### 4.5 Advisory conflicts (reported verbatim per scribe rule)

1. **Exit 64 classification.**
   - `w1/FrozenEvidence.md:30`: "do not relabel this harness's 64 as could-not-evaluate… Registry rows must name the context command's 64 class explicitly."
   - `corpus/lessons/round-15.md:50–51` and `claims.json:10`: "Both active registry maps explicitly classify 64 could-not-evaluate."
   - `SKILL.md:1669–1671, 1681`: "2 and 64 could-not-evaluate (…; 64 `usage_error`)".
   - **Delivered artifacts follow the lesson and PROTOCOL** (every nonzero code maps to clean/failed/could-not-evaluate). The `FrozenEvidence` advice is superseded; no artifact should cite it as support for "64 usage, not could-not-evaluate".
2. **Proposed stable IDs and flags.** `w1/SiblingOverlap.md:79–80` and `§7` cite `--check-receipt`, `mismatch_normalized`, `control_ineffective`, `source_pin_mismatch`, `missing_input`. The delivered tool uses `--check --receipt/--expected`, and the stable IDs in `tools/context-capture.py:58–86` (for example `comparison_mismatch`, `positive_control_ineffective`, `receipt_structure_invalid`). **Do not cite the w1 names.**
3. **`-h/--help` exit 0** is undeclared. `w1/Mistake.md` M13 and `R2` asked for a declaration. `main` returns 0 (`tools/context-capture.py:2094–2096`), and `SKILL.md:1681` says `0 clean (context_consistent)`. Gate-standard reading: a consumer that treats exit 0 as pass would pass on `--help`. Not a violation of the lesson's admit criterion ("maps name every nonzero class"), but open. Residual; not critical.

### 4.6 Coverage of the pinned selftest (static, not executed)

- Static count of selftest records: 36 case invocations (31 `check_case` + 5 `usage_case`) + 2 hermetic checks = **38** `SELFTEST_CASE` sites. The number printed at run time is an L1 fact; it is not claimed anywhere in the delivered text (good).
- Declared finding IDs with **no selftest case** (static): `environment_delta_mismatch`, `environment_baseline_git_dir`, `run_argv_mismatch`, `run_cwd_mismatch`, `run_env_delta_mismatch`, `tool_declaration_mismatch` (frozen-only path, which selftest never runs), `receipt_unreadable`, `expected_unreadable`, `internal_error`. The lesson (`round-14-verifier-spotcheck.md:162`) says not every emitted ID needs its own fixture, so this is a bounded coverage note, not a violation.
- The **default frozen replay** (`--check` with no args, the SKILL entry command) has no selftest case. Its correctness rests on the L1 run of the committed clean receipt. Pending.
- Selftest counts and literal expected pairs are present in code (`check_case` takes `expected_id`/`expected_exit` literals, and `usage_case` requires `id=usage_error`). The "computed from code under test" risk the w1 seats raised does not apply to the literals as written.

---

## 5. No-harm audit

| Item | Evidence read | Status |
|---|---|---|
| Historical `capture-context.py` bytes preserved | `SKILL.md:1633` (sha `7313e9…`); `FROZEN_TOOL_SHA256` (`tools/context-capture.py:140–142`); `context-receipt.json:4` (`tool_sha256`) | **Three-source agreement; byte proof pending L1** |
| Round-14 receipts preserved, no round-15 write to round-14 | No write path in check mode (§4.1); `SKILL.md:1640` "read-only inputs, never regenerated" | Bounded agreement; `git diff` proof pending L1 |
| Frozen clean receipt pinned | `FROZEN_RECEIPT_SHA256` (`:137–139`), `SKILL.md:1656`, `:1681` | Three-source agreement; file hash pending L1 |
| No sibling reads/execution | Tool imports stdlib only; the only path reads in check mode are the frozen receipt under the lane root and the explicit `--receipt`/`--expected` arguments (`run_check` 1298–1313); `SKILL.md:1689–1690` "no sibling gate is registered or executed". Sibling paths were not separately grepped. | Bounded agreement by static reading of the sections listed in §2 |
| No credential or agent-db reads | No such path observed in the sections of the tool and artifacts read; none cited | Bounded agreement (partial read of tool) |
| Writes limited to tameshi tree | Lane-relative paths only in tool and artifacts | Bounded agreement; `git status` pending L1 |
| SHONEN/PROVINCE unchanged | `SHONEN.md:5,7,9,11` `[~]`; no PROVINCE edit cited anywhere in round-15 artifacts | Bounded agreement; diff pending L1 |
| Sibling/round-12..14 evidence trees unchanged | No delivered artifact claims a change there; `measure.py` `HISTORICAL_EVIDENCE_DIRS` would detect it | **Pending L1 run of `measure.py --rev`** |

No counterexample found. Every row is either a bounded agreement across two or more sources or a pending L1 byte proof.

---

## 6. SHONEN authority

- `SHONEN.md:5,7,9,11` are `[~]` (four boxes), and the citations resolve (`reports/round-1-calibration.md`, `reports/round-1-kaika-coldread.md` exist).
- `SKILL.md:1689` (no change to SHONEN authority), `LOG.md:945` ("earns no SHONEN points"), and `corpus/lessons/round-15.md:44` (outside sample is separate) agree.
- The round-15 SKILL registry row is a gate declaration, not a box evidence claim (`SKILL.md:1617`: "entry commands here are declarations, not an outside admission").
- **Note (historical):** `LOG.md:283–291` (round 3) describes `[x]` marks that the current `SHONEN.md` does not carry (all `[~]`). The current state is the authority; this is informational only.
- Box-level evidence still missing for round 15: the L1 gate run (box 2), write-scope statement (box 4), and a cold read of the new registry row (box 3, unscored per round-14 precedent). All remain `[~]`.

---

## 7. Outside admission pending

- `corpus/lessons/round-15.md:44`: "admission remains the separate closure duty". `LOG.md:946`: "Same-lane reviewers advise; only separate non-author closure admits." `SKILL.md:1617, 1686–1688`: selftest green is "capability only", and the frozen replay is "neither … an outside-admission sample". `claims.json` has no admission field. `w1/OutsideAuthority.md:5, 16`: self-dispatched reviews are lane-internal.
- **No round-15 non-author closure exists.** `corpus/lessons/round-15-verifier-spotcheck.md` is absent (glob of `corpus/lessons/round-15*` returns only `round-15.md`). Consistent with the round-14 precedent, where the closure file is authored by a non-author integrator.
- **S051 is own-work (A tier), not an outside source.** `corpus/SOURCES.md:60`: "own-work | A | Byte-pinned retained context-receipt verdict replay… not live command execution or authentication". Its claim column restates the tool's own behavior; it cannot prove the C1 "after" state. The "after" state is proven only by L1 runs, not by S051.
- **Agreement:** no artifact claims admission, sampling, or `[x]`.

---

## 8. Missing evidence (current, honest, not defects yet)

| # | Missing item | Who creates it | Blocks |
|---|---|---|---|
| M-1 | Round-15 report (fleet-root vs lane-root location to be chosen) | L1 | Report, trend, SHONEN sections |
| M-2 | `.ufo/evidence/round-15/verification.json` (SKILL `:1616` pre-declares it as the runtime-observation location) | L1 | "retained runtime observations" wording; SKILL sentence is in present tense and must be true at closure or reworded |
| M-3 | `--selftest` run transcript (exit and `SELFTEST: PASS (n/m)`) | L1 | C1 capability; QUALITY17 |
| M-4 | Frozen replay (`--check`) run and retained output | L1 | Clean retained evidence claim in SKILL `:1680–1681` |
| M-5 | `--check --receipt … --expected …` run on the negative fixture `context-missing-env.json` (expected id `missing_injected_environment`, exit 1) | L1 | Discriminator claim in SKILL `:1651–1655` |
| M-6 | Retained old-invocation receipt (`capture-context.py --selftest` → 64) | L1 | QUALITY17 "retain the unsupported old invocation" |
| M-7 | `measure.py --rev` before/after and `sources-after.json` | L1 | Trend numeric section; no-harm byte proof |
| M-8 | Byte proof of historical bytes (`sha256sum`, `git diff` on round-14 paths) | L1 | No-harm |
| M-9 | LOG round-15 disclosures (failed seats, mid-flight disclosures, check-only cutover) | Closure | Audit trail (`AGENTS.md:3`) |
| M-10 | SCORECARD round-15 row | Closure | Scalar/trend record |
| M-11 | Trend verdicts for six axes | Closure / report | Trend claim |
| M-12 | Non-author outside spot-check (`corpus/lessons/round-15-verifier-spotcheck.md`) | Separate non-author closure | Admission (not an L1 precondition) |
| M-13 | Explicit `--help` exit 0 classification in the registry | Tameshi (non-critical) | Gate-standard completeness |

Items M-1 to M-8 are L1 work after the wave returns. None is a proven defect, and none should be marked as proven until the L1 run retains its output.

---

## 9. Messages

No message was sent. None of the findings is implementation-critical:
- §4.2 (docstring wording) and §4.5.3 (`--help` registry) are documentation or registry items;
- §4.3 and §4.4 are closure and LOG items;
- §4.6 coverage gaps are bounded by the lesson, not by a gate requirement.

If L1 finds that the frozen replay (`--check`) fails on the committed round-14 receipt, that would be implementation-critical and should be sent to `TameshiR15` at that time.

---

## 10. Recommended wording for the closure report (bounded, not predicted)

- "Calibration capability C1: the maintained retained-receipt gate exists (`tools/context-capture.py`). Its selftest and frozen replay were run by L1 on <date>; exits and finding IDs are in `<path>`." Use only after M-3 and M-4 exist.
- "No prospective capture is provided; the round-14 live experiment is not rerun (`SKILL.md:1638–1639`)."
- "Outside admission: pending separate non-author closure (M-12)."
- "SHONEN: all four boxes remain `[~]`; no promotion claimed."
- "Scalar 6→6 (capability, no promotion points)."

Do not use: "frozen digest-bound retained run completed" (until M-4), "independent admission" (until M-12), any w1 flag or ID name (§4.5.2), or the `measure.py` string-presence counts as capability evidence (§3).

---

Tool installs/updates: none.
Files written: this report only.
