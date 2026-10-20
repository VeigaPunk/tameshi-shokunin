# FrontierBoundary — round 15 wave 2 (static review)

Seat: `TameshiR15.FrontierBoundary` (leaf; no subagent dispatch). Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Target: C1 sourced-capability connection to the same-ground frontier; no row-count expansion, whole-F7 completion, or successor-sweep claim.
Mode: static review only. No gate, selftest, census validator, build, or test was executed. Reads, `grep`/`awk` counts, and `sha256sum` only.

## 0. Verdict

- **No frontier overclaim found in delivered text.** Every occurrence of "successor sweep", "whole-F7", "seventh case", "promotion", and "expansion" in the round-15 additions is a negation or an explicit open item. No frontier row, knowledge entry, PROVINCE, or SCORECARD text moved.
- **Row count moved 48 → 49** (S051 added). This is own-work source growth, not expansion under SOURCES rule 4. No text in the round claims expansion from it.
- **Four frontier-boundary defects, none implementation-critical:**
  - F1: S051 anchor has no commit or digest pin.
  - F2: lesson says "demonstrated CLI capability" before any run.
  - F3: SKILL cites `.ufo/evidence/round-15/verification.json`, which does not exist yet.
  - F4: S051 grounding quote does not cover the "public-CLI self-invocation" half of its `teaches` cell.
- **Two lower-severity items:** a docstring wording tension (F5) and an open contract-path pointer (F6).
- **Implementation-critical defects: none found.** No message was sent to TameshiR15.

## 1. Exact sources read (static; hashes at read time)

The working tree changed during this read. SKILL.md and the round-15 lesson each differed between my first and last reads, so the hashes below are the final read.

| Path | sha256 | Notes |
|---|---|---|
| `tools/context-capture.py` | `0ed784e0076b3de5ec5000c3862a771a3e3e2eb83241da347a6cf3f2f2c61edc` | 85159 B, untracked (`??`), 2116 lines |
| `.ufo/evidence/round-14/capture-context.py` | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` | matches the historical digest cited in SKILL and the w1 report |
| `.ufo/evidence/round-14/context-receipt.json` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` | equals `FROZEN_RECEIPT_SHA256` (tool line 137–139) |
| `.ufo/evidence/round-14/context-missing-env.json` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` | equals the SKILL-cited negative fixture digest |
| `corpus/SOURCES.md` | `a8bf4cd67734c12b5615d6b50ea59d24f1859bb4489e631c713be3109aed69e9` | diff vs `a9cf4da` read in full |
| `corpus/lessons/round-15.md` | `889da646b70e8eff3164aa449c3cfaf4eeafaef5d24305e21b8636a4661fdd43` | Gate, Mistakes, Dispatch read |
| `SKILL.md` | `032368fbb681c158a6ddd1130ff9fa044b3980dc0fa39c37e43f41e4b12c2cf1` | round-15 section ~1608–1700 and registry |
| `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md` | working-tree diffs | round-15 additions only |
| `CORPUS.md` §Sources (lines 86–112), `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (lines 19–60) | read | anchor, tier, own-work, and rule 1/2/4 text |
| `.ufo/evidence/round-15/` (listing) | read | `claims.json`, `integration-decisions.json`, `measure.py`, `sources-before.json` only |
| `git status --porcelain` / `git diff --stat` | read | 5 modified tracked files; untracked `tools/context-capture.py`, `corpus/lessons/round-15.md`, `.ufo/evidence/round-15/`, `.ufo/waves/round-15/` |

Not read: `~/.omp/**`, credential or auth files, sibling trees, or any sibling gate.

## 2. Static checks on the delivered tool (agreement)

Each check is a counterexample test against a frontier-facing claim.

1. **Check mode reads only three files.** `open`/`read_regular` call sites: tool line 302 (the tool's own bytes, for `tool_sha256`), line 1213 (the expected pin), and line 1318 (the receipt). The only receipt path in check mode is `DEFAULT_LANE_ROOT` + `FROZEN_RECEIPT_REL` (line 1302) when no `--receipt` is given. No other lane file is opened. **Agrees** with README "without … reading sibling trees" and with the SKILL statement that it never opens a recorded root path.
2. **Check mode never executes retained argv.** The only `subprocess` use is the selftest harness at line 1603. **Agrees** with S051 "does not execute retained argv".
3. **Writes.** Writes occur only at selftest lines 1622 and 1634, under `tempfile.mkdtemp` (line 1581), removed by `shutil.rmtree` in `finish()` (1717) and in `run_selftest`'s finally (2017). `sys.dont_write_bytecode = True` (line 119). **Agrees** with "check mode writes nothing".
4. **Selftest is public-CLI self-invocation.** `check_case` runs `[sys.executable, "-I", SELF, "--check", "--receipt", …, "--expected", …, "--json"]` (1638–1640). `usage_case` runs the same shape with `-I SELF` (1686). Literal expected ids and exits are passed as strings in `run_selftest_cases` (for example 1737, 1741–1744, 1759–1761). The check compares `observed_id == expected_id` and `returncode == expected_exit` (1653–1656). **Agrees** with QUALITY17 and the lesson's "helper-only is not standalone" rule. No helper-only substitution was found.
5. **Usage class 64.** `main` returns 64 only on `UsageError` (2093). Four usage cases pin 64 (1996–2002). **Agrees** with the SKILL registry's "64 could-not-evaluate (`usage_error`)".
6. **Selftest env isolation.** `SELFTEST_ENV` (1572–1576) sets a poisoned `GIT_DIR`, and `hermetic-no-lane-path` / `hermetic-temp-only` cases assert no lane-root leak and no stray temp entries (1700–1716). The default frozen path is not reached by any selftest case, because every `check_case` passes an explicit receipt and expected file. **Agrees** with "no live lane path is read or written" in selftest mode.

No code claim was contradicted by the tool. The defects below are in prose, pins, and provenance.

## 3. Frontier and source-row checks

### 3.1 Row count and census (static counts over committed working-tree text)

Counts from `corpus/SOURCES.md` rows matching `^| S###`, read with awk:

| Measure | Round start (`sources-before.json`, `a9cf4da`) | Now (working tree) |
|---|---|---|
| Rows | 48 | **49** (S051 added) |
| Tier A / B / C | 41 / 5 / 2 | **42** / 5 / 2 |
| Status mined / queued / rejected | 21 / 24 / 3 | **22** / 24 / 3 |
| Next unused id | S051 | **S052** |

- Change per SOURCES rule 2 (append-only) holds. The S049 change is limited to `used-by`, logged in the lesson's Gate. The Id-allocation bullet and "Next unused id" line updated together. Search-log entry present.
- `corpus/lessons/round-15.md` says "Source-row count alone is not expansion." **Agrees** with rule 4. No knowledge entry was added (`git status` shows no `corpus/knowledge/` change). Expansion is therefore unchanged. No text claims a row increase as expansion.
- `.ufo/evidence/round-15/sources-after.json` does **not** exist. The w1 pointer P2 is still open. L1 must record the after-census or state the counts in the report's `## Sources & frontier`.

### 3.2 Whole-F7, successor sweep, seventh case, promotion

Searched all round-15 additions in `SKILL.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/README.md`, and `corpus/lessons/round-15.md` for: `sweep`, `F7`, `frontier`, `expansion`, `coverage`, `seventh`, `promot`, `complete`, `closes`.

Every hit is one of:
- a negation: "adds no successor sweep, seventh recorded case, promotion credit" (SKILL, round-15 section); "does not complete whole-F7 result reuse, F1 interop or a successor mutation sweep" (README round-15 block, lines ~206–207);
- an open item: "remain open" (LOG; lesson lines 7–8, 58–60);
- a frontier note that moves nothing.

No positive claim of whole-F7 completion, successor-sweep execution, or a seventh recorded case was found. The frontier table in `corpus/README.md` (lines 68–84; F7 "open") is unchanged. The round-15 additions there are appended below it. PROVINCE.md and SCORECARD.md are unchanged.

### 3.3 S051 and the same-ground boundary

S051 (`corpus/SOURCES.md:60`) is own-work, tier A, `mined`, `on-release`, `used-by corpus/lessons/round-15.md`. Its `teaches` cell is grounded to a known own-work precedent. The row does not advance any F-row, and no `knowledge/` entry cites it. **Bounded agreement** that the capability is same-ground, not a new uncovered-coverage claim.

## 4. Defects (frontier boundary; none implementation-critical)

### F1 — S051 anchor is not commit- or digest-pinned (moderate, provenance)

- Row anchor: `r15 docstring lines9–14 and Modes lines16–28; opened2026-10-20`.
- Contract `anchor` (`CORPUS.md` line 99; `SOURCES-CONTRACT-v1.md` line 32): "exact section / heading / page / line plus revision (version, commit, or publication date)." `r15` is a version label, not a commit.
- Precedent: S050 is `at measured commit 6431478`. S031 is `@ 4eb4cf3 (sha256 …)`. S051 has neither commit nor sha256.
- Counterexample: the tool is untracked and its bytes are still changing in this wave (`0ed784e0…`). The line anchors **do** match the current bytes (file lines 9–14 are the module overview; 16–28 are the Modes block; 28 is "path is read or written; fixtures are removed in a finally block"). Any edit that shifts lines silently breaks the row with no row change.
- Bounded action: when the gate freezes, commit it and re-anchor S051 as `tools/context-capture.py @ <commit> (sha256 <digest>)`. Until then, record the sha256 in the row or state explicitly that the anchor is pre-commit.

### F2 — "demonstrated CLI capability" before any run (moderate, overclaim)

- `corpus/lessons/round-15.md:30`: "It supports bounded data-only replay and demonstrated CLI capability, not historical experiment authentication."
- The same round's SKILL section says "Nothing below was executed for this write". The lesson's own Gate says "actual runtime evidence is separate from documentation." No selftest or frozen run has executed in this wave (static seat; L1 runs once after integration).
- Bounded action: replace "demonstrated" with "implemented and declared"; state that selftest and frozen replay are pending the integrated L1 run.

### F3 — SKILL cites a verification file that does not exist (moderate, forward reference)

- `SKILL.md:1616`: "Runtime observations are retained separately in `.ufo/evidence/round-15/verification.json`."
- `ls .ufo/evidence/round-15/` shows `claims.json`, `integration-decisions.json`, `measure.py`, `sources-before.json` only. No `verification.json`.
- Bounded action: either the L1 run writes it before the lane closes, or the sentence says "to be retained by L1 integration; not present at this write."

### F4 — S051 grounding quote covers only the write-scope half of its teaches cell (low, grounding)

- Contract rule 1 (`SOURCES-CONTRACT-v1.md` lines 36–41; `CORPUS.md` equivalent): the round `## Gate` records, per new row, the URL/anchor, access date, and a ≤25-word quote with location **grounding `teaches`**.
- S051 `teaches`: "Byte-pinned retained context-receipt verdict replay with isolated public-CLI self-invocation, not live command execution or authentication."
- The one quote in the lesson Gate ("Check mode writes nothing; the only writes are --selftest fixtures under mkdtemp.", 13 words) grounds the write-scope half only. The "public-CLI self-invocation" half is grounded only by location (file lines 26–28), not by a recorded quote. Candidate quote, 10 words: "Run the real CLI by subprocess against isolated synthetic fixtures".
- The lesson's quote joins a line-wrapped sentence (file lines 11–12) without disclosing the wrap. S050's precedent discloses wraps. A literal `grep` for the quoted string fails against the file. Disclose the wrap.
- Bounded action: add the second quote with its location to the lesson Gate, and note the wrap.

### F5 — docstring says "does not read live lane inputs" (low, wording)

- Tool line 11: "does not read live lane inputs." But frozen default mode reads `DEFAULT_LANE_ROOT/.ufo/evidence/round-14/context-receipt.json` (line 1302). Line 13 of the docstring qualifies this ("Frozen mode reads only the archived round-14 receipt"), so the unqualified sentence is a counterexample.
- Bounded action: "reads no lane input except the pinned archived receipt in frozen mode." Wording only; no code change.

### F6 — SOURCES.md contract pointer still bare (low, carried from w1 P7)

- `corpus/SOURCES.md` line 4: "Contract: `SOURCES-CONTRACT-v1.md`". This does not resolve from `corpus/`. The contract is `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` and `CORPUS.md` §SOURCES.md. Prose-only fix; no row edit.

### Carried from w1 (status now)

| w1 ID | Status at this read |
|---|---|
| P1 tool missing | **Closed** (tool exists; untracked; digest above) |
| P2 census after-artifact | **Open** (`sources-after.json` absent) |
| P3 claims.json S### pointer | **Partly closed** (C1 `source` string names S051 and S049; no structured `sources` key) |
| P4 S051 allocation | **Allocated** (option a); anchor pinning open → F1 |
| P5 census before→after in report | **Open** (report not yet written; counts in §3.1) |
| P6 SKILL registry row, 64 explicit | **Closed** (SKILL round-15 registry row present, 64 explicit) |
| P7 SOURCES line-4 pointer | **Open** → F6 |
| P8 drift | Recorded (§1 hashes) |

## 5. Checks L1 should run once after integration (not run here)

1. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`. Expected: exit 0; W04 pair for S047/S048; no E-codes; 49 rows.
2. Diff `corpus/SOURCES.md` against `a9cf4da78f2514c7bedd91a850a88590009d7df0`. Allowed: S049 `used-by`, search-log entry, S051 row, S051 Id-allocation bullet, "Next unused id" S052.
3. Pin the tool digest and commit it, then re-anchor S051 (F1).
4. Record the after-census (`sources-after.json`) and the report's `## Sources & frontier` (P2, P5).
5. Confirm `.ufo/evidence/round-15/verification.json` exists before SKILL §1616 is read as present (F3), or edit the sentence.

## 6. Non-claims (this seat)

- No gate or selftest was run. The selftest and frozen replay are unexecuted in this seat, so no pass or fail is asserted.
- No row was written, edited, or allocated by this seat.
- No sibling tree was read. No credential, auth, or `~/.omp/agent` file was read.
- No frontier, PROVINCE, SCORECARD, or knowledge file was edited.

## 7. Tool installs and updates

None. (`sha256sum`, `grep`, `awk`, `git status`, `git diff --stat`, `ls` were already present.)

## 8. Authority

Advisory, lane-internal, leaf seat. Not an independent admission sample. It does not replace the separate non-author closure duty.
