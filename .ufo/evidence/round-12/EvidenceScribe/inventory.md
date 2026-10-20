# Round 12 — EvidenceScribe evidence inventory (notes only)

Seat: EvidenceScribe · Wave: tameshi-r12-w1 · Lane: tameshi-shokunin
Anchors: **O** = observed by this seat (read-only, listed command); **I** = inference; **U** = unknown.
No command below was executed as a test by this seat. Where a recorded prior value is quoted it is labelled with its source file. No verdict in this file is a pass.

## 0. Start state (O)

| Item | Value | Command / source |
|---|---|---|
| HEAD at read time | `18ad5d050ef4bcd830fe513825baed878f025024` | `git rev-parse HEAD` — matches the assigned start HEAD |
| Worktree | `?? .ufo/waves/round-12/` and `?? .ufo/evidence/round-12/` (other seats' dirs) | `git status --short` |
| Python | 3.14.7 | `python3 --version` |
| shellcheck | `/usr/bin/shellcheck` present | `which shellcheck` |
| jq | `/home/vgpnk/.local/bin/jq` present | `which jq` |
| `tools/repeat-control.py` | **absent** at read time (ControlGate owns creation) | `ls tools/repeat-control.py` → no such file (U: it may land later in this wave) |

Tool installs by this seat: none. (Rules read: `~/.omp/agent/RULES.md`, tooling directive; nothing needed for this scope.)

## 1. Claim A — source census validate exit 0 (C-SRC)

### 1.1 What the claim is anchored to (O)

- Registry under test: `corpus/SOURCES.md` — sha256 `6b34e8991f56d78d561512d71c7eaeaf4f548f1d7f12eec8eb2b896bf6d72827`; 44 rows matched by `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at read time.
- Last commit touching it: `01b358c30ba484e766c281823c5b0f89ecff0840` (2026-10-19T19:34:41-03:00).
- Validator: `.ufo/evidence/kaika-round-1/sources-census-v2.sh` — sha256 `b9b754713c9c359823e85106e0177e6678bd95b567d1c897fd7f3464945a2bc3`. Header: "run from the lane root"; reads `corpus/SOURCES.md` with a relative path, so it must be run from the tameshi repo root. Part A = contract-v1 census (exit 1 on violation); Part B = H4 extensions (B1 informational, B2 must print nothing).
- Recorded prior run: `.ufo/evidence/kaika-round-1/sources-census-v2.txt` — sha256 `b97f509a7885d01ed510a6b973a894b22c9329271dd9fb26cb58633731651430`, committed in `121696b` (2026-10-19T19:22:35-03:00). Content: `A rows 44`, `A malformed 0`, tiers `A=37 B=5 C=2`, status `mined=12 queued=29 rejected=3`, empty dup/enum/missing sections, `B1 count=25` (informational), empty B2, final line `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`.
- **Exit code is NOT recorded in that file.** The CLEAN line implies exit 0 only if `bad=0`; the exit must be captured fresh.

### 1.2 Commands the L1 integrator should run (not run by this seat)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git rev-parse HEAD                       # expect 18ad5d050ef4bcd830fe513825baed878f025024 (start HEAD)
sha256sum corpus/SOURCES.md .ufo/evidence/kaika-round-1/sources-census-v2.sh
bash .ufo/evidence/kaika-round-1/sources-census-v2.sh > .ufo/evidence/round-12/<SEAT>/sources-census-v2.run1.txt 2>&1; echo "exit=$?" >> .ufo/evidence/round-12/<SEAT>/sources-census-v2.run1.txt
# compare live output section-by-section with sources-census-v2.txt (expected identical counts: 44 / 0 / A=37 B=5 C=2 / mined=12 queued=29 rejected=3)
```

Expected verdict if the validator holds: last line `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit `0`. This is the **prior** recorded expectation, not an observed result of this round.

Replay evidence rule (QUALITY 9): copy the captured run output into the round-12 evidence dir before any commit cites it; `/tmp` scratch is not evidence.

### 1.3 Risks for claim A (O unless marked)

1. **Stale recorded run.** `sources-census-v2.txt` (`121696b`, 19:22:35) predates the latest `SOURCES.md` commit `01b358c` (19:34:41). Row counts agree (44) but the content may not; a fresh run is required, and the old file must not be cited as current.
2. **Contract file missing.** `corpus/SOURCES.md:4` cites `SOURCES-CONTRACT-v1.md`. A filesystem search (`find / -xdev -name 'SOURCES-CONTRACT*'`) returns nothing. The "contract v1" rules exist only as comments/logic in the validator. Any claim wording "contract v1 clean" rests on a missing document (U: whether a copy exists outside the xdev set).
3. **Wrong census artifacts.** `sources-census.txt` (sha `551d76b7…`) is an older 37-row run from another worktree path (`.tower/worktrees/kaika/...`) — stale, do not cite. `sources-census-final.txt` (sha `17265934…`) is the earlier H4 no-id-cite listing with no VERDICT line and must not be cited as CLEAN.
4. **B1 is not a gate.** `B1 count=25` (no-id-cite for `S031`–`S037` in several used-by files) is informational by script design. A report that says "B1 clean" would be false.
5. **Exit-code capture.** The validator's pass condition is `exit $bad` with `bad` set by Part A and B2 only; capture `$?` in the same shell line as the run.
6. **Sibling tree dependency.** The validator path is a kaika-round-1 artifact. If L1 wants round-12 evidence to be self-contained, copy the script into the round-12 evidence dir with its sha recorded (decision for L1; not done here).
7. **Row-level claims not checked.** The validator checks shape, enums, tier inflation, used-by path existence and id-cite. It does not verify that the `anchor` or `teaches` cell is true, nor that `opened` matches `sources-opened.tsv` (its last section is `TSV fetch records per external row`, which is not in v2). Do not cite it as source-truth verification.

## 2. Claim B — repeat-control calibration gate (C1), evidence inventory

Interface under test (from the wave contract): `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`, stdin DEVNULL, numbered stdout/stderr and exit saved per run, bytes not normalized. Finding IDs and exits: `controls_match` 0 · `controls_mismatch` 1 · `baseline_nonzero` 2 · `command_unavailable` 2 · invalid usage 64 (could-not-evaluate). `--selftest` isolated fixtures; `--snapshot DIR` validates committed input digests, tamper → exit 2 `snapshot_tampered`.

Required evidence (to be produced by the owning seat, ControlGate, in `.ufo/evidence/round-12/ControlGate/`; not by this seat):

| # | Artifact | Command | Expected (contract, not observed) |
|---|---|---|---|
| C1-1 | selftest transcript | `python3 tools/repeat-control.py --selftest; echo exit=$?` | exit 0; stable, output-mismatch, stderr-mismatch, exit-mismatch, nonzero-baseline, command-unavailable, invalid-run-count cases each produce the exact ID/exit |
| C1-2 | negative: mismatch | a fixture command whose output varies per run, `--runs 3` | exit 1, `controls_mismatch`; numbered per-run stdout/stderr/exit present |
| C1-3 | positive: stable | a fixture command that is byte-identical, `--runs 3` | exit 0, `controls_match`; three identical triples |
| C1-4 | nonzero baseline | a fixture exiting 1 on all runs | exit 2, `baseline_nonzero` (could-not-evaluate, not fail) |
| C1-5 | unavailable command | a nonexistent argv[0] | exit 2, `command_unavailable` |
| C1-6 | invalid usage | `--runs 0` / missing `--` | exit 64 |
| C1-7 | snapshot pass | `python3 tools/repeat-control.py --snapshot <committed DIR>; echo exit=$?` | exit as the snapshot's expected exit |
| C1-8 | snapshot tamper | copy snapshot, flip one byte, rerun | exit 2, `snapshot_tampered` |
| C1-9 | tool identity | `sha256sum tools/repeat-control.py`, `python3 --version`, argv and cwd of each run | recorded alongside every run directory |

Per-run artifact layout to require: `DIR/run-1/{stdout,stderr,exit}`, `run-2/...`, `run-3/...`, plus a summary file with the finding ID. Bytes are compared raw; no newline or whitespace normalization may be applied before comparison (verify by a fixture that differs only in a trailing newline → must be `controls_mismatch`).

Scope limits to state in any report (QUALITY 3, C1 contract): N=3 identical runs is a calibration precondition, not proof of determinism; a pass does not establish that the command is flake-free; no flakiness is cured by the gate.

### 2.1 Risks for claim B

1. The tool does not exist at read time; every row above is an unobserved expectation.
2. Stdin DEVNULL and no normalization must be evidenced by a fixture, not by reading the source.
3. "Could-not-evaluate" exit 2 must never be reported as a pass; the L1 report needs the exact ID per run.
4. Repeat-control is independent of the mutation runner (`tools/mutate-and-run.sh`, unchanged); its evidence must not be counted as a seventh mutation leg.

## 3. Claim C — bash-surface-census declared-witness split (C2), evidence inventory

Target gate: kagi `corpus/surface-census.sh` (pin `275d8294…53009f`, per `corpus/knowledge/mutation-case-kagi-census.md`; read-only). Recorded per-defect table: see `mutation-case-kagi-census.md` §1 (not reproduced here). Recorded selftest: `SELFTEST: PASS (16 cases)` exit 0.

Required evidence (owned by BashWitness, `.ufo/evidence/round-12/BashWitness/`, script `tools/bash-witness-study.py`):

| # | Artifact | Requirement |
|---|---|---|
| C2-1 | per-defect witness declaration TSV (B1–B10, label or NONE) | written and sha256-hashed BEFORE any mutant run; its mtime precedes the run log's first entry |
| C2-2 | pre-run read record | which files were read before declaration (selftest and spec only) and the explicit disclaimer about historical outcomes |
| C2-3 | per-mutant run log | exact edit, fresh /tmp copy, exit, token/witness that killed it, `k_witness` vs `k_accidental` vs survived |
| C2-4 | substrate pin before/after | `sha256sum` and `git -C kagi-shokunin status --porcelain` before and after; both unchanged |
| C2-5 | selftest transcript on pristine | `bash <kagi>/corpus/surface-census.sh --selftest; echo exit=$?` → expected `SELFTEST: PASS (16 cases)` exit 0 (prior record) |

Expected split arithmetic, stated as a prior expectation: witness-scoped split of the 8 recorded kills must sum to 8 (`k_witness + k_accidental = 8`, per `corpus/knowledge/witness-scoped-kill-verdict.md` F2 wording). Any reanalysis of the existing six legs is recorded as reanalysis and is never counted as a seventh independent gate.

### 3.1 Risks for claim C

1. Witness declarations written after reading historical kill outcomes are contaminated; the TSV hash and mtime ordering is the only evidence of blindness, and it is partial (per the prior F2 record).
2. The "existing 6 recorded gate legs unchanged" constraint means the study must not rewrite `mutation-case-*` notes.
3. A split that yields `k_accidental > 0` must be reported as an accidental kill, not folded into witness kills.

## 4. Cross-claim commands for L1 (collect, do not run here)

- `git rev-parse HEAD` (start state check)
- `git status --short` (expect only round-12 wave/evidence dirs or intended new files)
- the three blocks above (A: census; B: repeat-control; C: witness study + kagi substrate pins)
- `python3 tools/repeat-control.py --selftest` and `--snapshot` only after the file exists; do not run before ControlGate lands it
- Exit codes captured with `; echo exit=$?` on the same line as each run

## 5. Not claimed

- No pass, no determinism, no independent authority is claimed here. Nothing in this file is an observed round-12 result.
- No product code, gate, corpus registry, or sibling tree was edited. Only this file and the wave report were written.
- No installs or upgrades were made.
