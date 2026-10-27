# T51W2ExecTool01 — C3 registry row falsification: `tools/bash-witness-study.py` at CAND

Seat: T51W2ExecTool01, wave 2 (falsify), round 51. Item: independently audit the canonical
round-51 registry row for `tools/bash-witness-study.py` at candidate
`6d8c11e378aa90b12650808e1b79270742935f15`; run the row's exact backticked self-test and the
`--r51-no-such-flag` usage probe from a `git clone --shared` at CAND with scratch TMPDIR and stdin
`/dev/null`; check every row field against the tool's source. Read-only on the lane and fleet; I
wrote only this report and `T51W2ExecTool01/` under `.ufo/waves/round-51/w2/`. Nothing installed,
nothing repaired. Scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool01` deleted before yield.

Clone: `git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin cand`;
`git -C cand rev-parse --show-toplevel` → the clone; `checkout --detach 6d8c11e3…` → HEAD
`6d8c11e378aa90b12650808e1b79270742935f15`. Base clone `base` likewise at `9962033f…`.

## 0. The row under audit

`SKILL.md:2142`, inside `#### Gate/probe registry — round 51` (heading line 2138). Eight cells:

| # | cell |
|---|---|
| name | bash declared-witness study |
| kind | `probe` |
| entry | `python3 tools/bash-witness-study.py check` (add --evidence DIR to grade another copy of the frozen evidence) |
| verdict map | 0 clean; 1 failed (tamper, digest drift, summary/raw mismatch, unresolved sweep); 2 could-not-evaluate (missing input, pin mismatch, runner SETUP); 64 could-not-evaluate (usage) |
| self-test | `python3 tools/bash-witness-study.py selftest` → VERDICT: is the last line, preceded by WITNESS_SELFTEST: 51/51 pass |
| pinned | `.ufo/evidence/round-12/BashWitness/declaration.json` (frozen target, spec and runner sha256), `.ufo/evidence/round-12/BashWitness/declared.tsv` (…sha pinned in declaration.json), `…/summary.json`, `…/manifest.json`, `tools/mutate-and-run.sh` (pinned runner digest, the spec is extracted from its heredoc); the DECLARED_WITNESSES rows are literals in the tool |
| write scope | caller-chosen --evidence DIR for declare, run and rerun plus the extended manifest; check and count read-only; selftest writes a private fixture tree under a hardcoded /tmp (TMPDIR ignored); sibling kagi object store read-only |
| owner | tameshi |

The tool is the round-12 declared-witness study: five modes `declare|run|rerun|count|check|selftest`
(`tools/bash-witness-study.py:1762-1779`), exit constants `0/1/2/64` (`:119`).

## 1. The predicate path — measured, and it holds

Commands run from the CAND clone, `TMPDIR=$S/tmp`, stdin `/dev/null`:

| probe | exit | wall | last stdout line | receipts |
|---|---|---|---|---|
| `python3 tools/bash-witness-study.py selftest` | **0** | 122 ms | `VERDICT: PASS` (preceded by `WITNESS_SELFTEST: 51/51 pass`) | `selftest.stdout/.stderr/.meta` |
| `python3 tools/bash-witness-study.py --r51-no-such-flag` | **64** | 54 ms | (stdout empty; stderr `bash-witness-study.py: error: …`) | `usage-probe.*` |

- 51 stdout lines: 51 `  check … ok` lines, **0** failing checks; the checks cover the git canary
  (inherited `GIT_*`, pinned global/system config), then the manifest/summary tamper paths, and the
  run ends `check private root is removed ok`. The string `FAIL` appears once, inside a check *name*
  (`check FAIL without denominator is inconclusive, not a crash ok`, line 30) — not a failure.
- Row's self-test cell claims `VERDICT:` is the last line, preceded by `WITNESS_SELFTEST: 51/51 pass`:
  both are literal, tool-emitted (`tools/bash-witness-study.py:1711` `WITNESS_SELFTEST: {n}/{n} pass`;
  `:1713` `VERDICT: PASS`; `:1715` `VERDICT: FAIL` → exit 1). The marker is a real verdict of 51
  assertions, not argparse help text; this is exactly the defect wave-1 found in forged rows
  (`--help --selftest`), absent here.
- Usage code 64 is declared in the cell ("64 could-not-evaluate (usage)") and produced by the
  custom `UsageParser.error` (`:1719-1724`), which also covers subparser errors: measured
  `check --r51-no-such-flag` → 64, `selftest --r51-no-such-flag` → 64.
- **Frozen counter's own row logic** (`drive_row.py` imports `.ufo/evidence/round-51/c3/measure.py`
  from the CAND clone and calls its `registry_rows`, `row_reason`, `run_row` against this clone):
  `row_reason(line 2142) -> why=None`; `run_row(line 2142) -> rc=None last='VERDICT: PASS'`.
  → this row **covers** the tool under the frozen C3 predicate. Same driver shows the older row at
  `SKILL.md:1504` fails: `run_row(line 1504) -> rc='finding-id-not-in-row (VERDICT:)'`, i.e. the
  round-51 row is a genuine improvement over the base row on the marker rule.
  Receipt `c3-row-logic.stdout`.
- **Not the known row-16 blocker.** `.ufo/evidence/round-51/c3/tools-base.json` index 16 is
  `tools/round21-measure.py`; this tool is index 1. Contrast measured in the same clone:
  `python3 tools/round21-measure.py --selftest` → **exit 1**, traceback ending
  `git -C /fast/…/T51W2ExecTool01/tameshi-shokunin show 08175c62…:tools/mutate-and-run.sh … exit
  status 128` (it reaches for a sibling worktree that a clone does not have). This tool's selftest
  never needs a sibling: it passed with no `kagi-shokunin` beside the clone. Receipt
  `contrast-round21-measure-selftest.stdout`.

## 2. Row fields against source — where the row is true

- **Kind enum** `probe` is a legal cell (`.ufo/evidence/round-51/c3/measure.py:119-120`) — see F1 for
  the semantic problem.
- **Entry names the tool**: cell contains `tools/bash-witness-study.py`.
- **Verdict map**: all four codes the tool can return (0, 1, 2, 64 from `:119`) are declared, and
  each measured class matches: `check` → 1 on drift and on tamper (`check.stdout`,
  `check-tampered-copy.stderr` `TAMPER declared.tsv sha256=ac0291… committed=0def0d…`); `declare` →
  1 on its own frozen-declaration refusal (`.stderr`: `declared.tsv already exists — declarations are
  frozen`, source `:849-851`); missing evidence dir → 2 (`:510-513`, `load_declaration` raises
  `Cannot("missing … — run declare first")`, measured as
  `CANNOT-EVALUATE (missing …/declaration.json)`); `run`/`rerun` → 2 on runner drift (`:566-570`);
  usage → 64. No fifth code found (argparse is overridden to 64 at `:1719-1724`; uncaught paths exit
  1 as Python does, which the map's `1 failed` already covers).
- **Pinned-value paths all exist at CAND** (counter's `PATHISH` check passes): declaration.json,
  declared.tsv, summary.json, manifest.json, tools/mutate-and-run.sh.
- **Pins are load-bearing, not decorative**: `declared.tsv` sha `0def0d3b…` equals
  `declaration.declared.sha256`; the spec heredoc still extracts to `d2ad3f29…` which equals
  `declaration.inputs.spec.sha256` at **both** base and CAND (the round's C2 leg addition to the
  runner did not touch the `bash-surface-census.spec` heredoc); `DECLARED_WITNESSES` is a literal
  tuple in the tool (`:126`). See F3 for the one pin that is stale.
- **Write scope, as far as it goes, is accurate.** `check` and `count` are read-only: a 96-file
  sha256 snapshot of `.ufo/evidence/round-12/BashWitness/` is byte-identical after running both
  (`check` exit 1, `count` exit 0), and `git status --porcelain` in the clone shows no lane-tree
  write. The selftest **does** use a hardcoded `/tmp` and ignores TMPDIR — `bash-witness-study.py:1240-1241`
  `tempfile.mkdtemp(prefix="bash-witness-selftest-private.", dir="/tmp")` — proven by
  `TMPDIR=/nonexistent-tmpdir-xyz` → still exit 0, `VERDICT: PASS` (`tmpdir-ignored.stdout`); the
  private root is removed (`check private root is removed ok`) and no `/tmp/bash-witness-selftest*`
  was left behind. The sibling kagi store is only read (`git -C <kagi> show`, `:349-352`).

## 3. Falsification findings

### F1 — `kind: probe` contradicts §Gate standard; the tool can and does fail
`PROTOCOL.md:377-379`: "A **gate** is a committed, re-runnable verdict script a lane owns: it reads
surfaces, compares them against expected values persisted in its own repo, and returns a verdict. A
tool that cannot fail is a **probe**, and is registered as one." This tool reads the frozen evidence
tree, compares it against expected digests persisted in the lane repo (`declaration.json`), and
returns 0/1/2/64 — and it fails: measured exit 1 twice at CAND (drift; tamper). So `probe` is the
wrong side of the lane's own definition. This is not hypothetical in this lane: the round-15
appendix performed exactly this correction on a sibling instrument ("Verdict behavior over persisted
expectations is a **gate** under §Gate standard, not a probe", `.ufo/evidence/round-16/coldread/SKILL.snapshot.md:1629-1631`).
Pre-existing (base row `SKILL.md:1504` and the round-18 table `SKILL.md:1932` also say probe), but
the round-51 row re-asserts it as new conformant material, and it is one of the fields the frozen
predicate's `cannot_see` names (contract.json C3.cannot_see: "That a row's kind, write scope and
pinned-value description are true of the tool"). Class: semantic kind mismatch, counter-invisible.

### F2 — the row's Entry command is RED at the revision it documents
`python3 tools/bash-witness-study.py check` at CAND:

```
WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
WITNESS_CHECK: FAIL (1 problems; 96 files covered)
exit=1
```

The row's `0 clean` class is therefore unreachable at CAND: every covered file and the extracted
spec still match; the single problem is the runner-digest pin. Facts that bound the finding:

- Not caused by round 51 alone: the same drift exists at base (`base-check.stdout`: `sha256=a7d3f2dd… committed=75ed934d…`, exit 1).
- The round did move the drifted value: base `a7d3f2dd…` → CAND `977de470…` (C2's tenth leg in
  `tools/mutate-and-run.sh`), and `run`/`rerun` now refuse at CAND with
  `CANNOT-EVALUATE (runner-drift …)` exit 2 (`run-mode.stderr`) — they refuse at base too.
- The round-51 row **switched** the Entry command from the base row's `count` (green: `count` exits
  0 at CAND, `count.stdout`, and at base) to `check` (red). So the registry now advertises the one
  mode that is guaranteed to report failure.
- Under `PROTOCOL.md:411-413` "a red gate is a conformance defect recorded in the round notes and
  routed to its owner" — a row whose declared entry is red is at least a routed defect for the
  operability axis.

### F3 — one pinned value is stale, and the row presents it as a live pin
`declaration.json:44` pins `inputs.runner.sha256 = 75ed934d…`. Actual bytes:
`tools/mutate-and-run.sh` at CAND `977de470…`, at base `a7d3f2dd…`. So the runner pin has matched
neither the base nor the candidate tree for many rounds (the round-12 declaration is frozen and the
runner legitimately evolved), and the tool's `check` (exit 1) and `run`/`rerun` (exit 2) enforce it.
Meanwhile the other pins *are* live: `declared.tsv` `0def0d3b…` == `declaration.declared.sha256`,
extracted spec `d2ad3f29…` == `declaration.inputs.spec.sha256` at base and CAND. The row's pinned
cell is thus true about *which* files are pinned and load-bearing, but the runner digest it names is
unsatisfiable at REV — the operative consequence is F2.

### F4 — the same condition is exit 1 or exit 2 depending on mode; the map does not say so
Runner-pin mismatch → `check`: `problems.append("DRIFT …")` then `return EXIT_FAIL` (`:1149-1157`,
`:1220-1222`) = **1 failed**; `run`/`rerun`: `raise Cannot("runner-drift …")` (`:566-570`) =
**2 could-not-evaluate**. The row lists "digest drift" under 1 and "pin mismatch" under 2 without
attributing either to a mode. Both branches were measured (`check.stderr/stdout`, `run-mode.stderr`),
so no code is undeclared — this is a readability ambiguity, not a missing mapping.

### F5 — write scope understates the default target
`EVIDENCE_DEFAULT = REPO/.ufo/evidence/round-12/BashWitness` (`:95`), and the writers use it when
`--evidence` is absent: `declare` writes `declared.tsv`/`declaration.json`/target/spec (`:877`,
`:915`), `run` writes `summary.json` + `manifest.json` into the evidence dir (`:998-999`, `:945-946`),
`rerun` writes `rerun-<stamp>/` **and re-anchors `manifest.json` at the evidence dir** (`:1033`). The
row says "caller-chosen --evidence DIR for declare, run and rerun plus the extended manifest" — true
only when the caller chooses; with no flag the write target is the lane's own committed evidence
tree. At CAND the harm does not materialise because `run`/`rerun` refuse first on runner drift
(exit 2, `git status` clean), but the registry text hides the default.

### F6 — two rows, two entry commands, one counter-red
`SKILL.md:1504` (the round-12 `### Gate/probe registry` row) still says Entry `… count`, verdict map
"0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage only
(argparse)", pinned only three files — and it fails the frozen counter (`finding-id-not-in-row
(VERDICT:)`, §1). The round-51 row says Entry `… check`. The counter scans every `^#{2,4}
Gate/probe registry` section and takes the best row, so C3 is unaffected; a human reader of the page
now sees two different entry commands for one instrument.

## 4. Field-by-field verdict

| field | verdict | basis |
|---|---|---|
| name | true | mode set matches the tool |
| kind `probe` | **wrong** (F1) | tool fails; PROTOCOL §Gate standard |
| entry `check` | **runnable but red at REV** (F2) | exit 1, runner-digest drift; base row used green `count` |
| verdict map 0/1/2/64 | **accurate on classes** (F4) | every code measured; mode attribution missing |
| self-test command + marker | **true** | exit 0, `VERDICT: PASS` last, `WITNESS_SELFTEST: 51/51 pass` above it, 0/51 failing checks |
| pinned values | paths true & load-bearing; runner pin stale (F3) | declaration.json:44 vs sha256 at CAND/base |
| write scope | true for `check`/`count`/selftest; incomplete default (F5) | digest-equal tree, hardcoded `/tmp` proven, `:95`, `:998-999`, `:1033` |
| owner tameshi | true | lane's own tool |

## 5. Risks and blockers

- **Not a counter blocker.** Under the frozen C3 predicate this row is covered (counter's own
  `row_reason`/`run_row` at line 2142 return no reason). F1–F6 are truth-of-field defects that the
  predicate's `cannot_see` names; they do not flip `C3_R51_PASS`, and I did not repair anything.
- **Operability judgement:** a reader following the registry row runs `check`, gets exit 1 with
  `WITNESS_CHECK: FAIL`, and reads the row's own `1 failed (… digest drift …)`; the row is honest
  about the code but registers a permanently-red entry. The green read-only sibling mode `count`
  (exit 0, recomputes and matches the committed summary) is the one the base row advertised.
- The full 30-row counter run exceeded this seat's 300 s wall (other tools' selftests dominate); the
  per-row verdict above comes from invoking the frozen counter's own `registry_rows`/`row_reason`/
  `run_row` against the frozen clone — the same code path the counter uses per row.
- Turn-taking note: `bash-witness-study.py`'s selftest writes to host `/tmp` regardless of TMPDIR
  (row-disclosed); the counter's per-command TMPDIR isolation does not bind this tool, and with 6
  worker threads the shared `/tmp` is the only shared surface. No residue was observed.

## 6. Retained evidence (`T51W2ExecTool01/`)

`selftest.{stdout,stderr,meta}`, `usage-probe.*`, `check.*`, `count.*`, `run-mode.*`, `declare.*`,
`check-tampered-copy.*`, `base-check.stdout`, `base-count.stdout`, `base-selftest.stdout`,
`tmpdir-ignored.stdout`, `c3-row-logic.stdout` (+ `drive_row.py`), `digests.txt`,
`contrast-round21-measure-selftest.stdout`, `c3-full-run-aborted.stdout` (300 s wall, partial; see §5).

No tool was installed or updated; no lane, fleet or sibling repo was written; scratch deleted.
