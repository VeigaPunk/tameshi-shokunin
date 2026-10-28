# T55W1ExecModeDiscovery — documented-mode inventory vs the frozen C2 counter

- Round 55, wave 1, seat `T55W1ExecModeDiscovery` (executor, mode-discovery blind-spot hunt).
- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base revision `0a2010acd1e92e4e332774050825e21bcfc7e079`; lane HEAD at probe time `631cd6455e58dce969310b4c0466c3383d9f5108` (counter set), worktree dirty (r18).
- Counter under review: `.ufo/evidence/round-55/c2/measure.py` (frozen). Never edited.
- All line numbers below are from the base revision; `tools/registry-check.py` is byte-identical in the worktree (r19), so its lines hold at the content commit too.

## Verdict in one paragraph

**One documented allocating mode is missing from the frozen counter: `registry-check --rev`.** It allocates scratch exactly like the eight measured modes (`tools/registry-check.py:780`, `tempfile.mkdtemp(..., dir=strict_scratch_root())` inside `clone_lane_at_rev`), is documented in the tool's usage/docstring and in `SKILL.md:2180`, and under a set-but-unusable `TMPDIR` it exits 2 with a non-grammar line **on stdout** (`REGISTRY_CHECK: could-not-evaluate (...)`), stderr empty. The documented allocating population is **9**, not 8. The counter's 8/8 grammar arm therefore reads green while a documented mode violates the class the claim is about. Per the brief this is a defect in the frozen counter: reported, not fixed; no frozen file was touched. Seven further documented non-allocating modes are also outside the counter; none allocates (each verdict plus the deciding line below). One boundary case (`bash-witness-study run/rerun`) reaches `$TMPDIR` in a **child** runner (`mktemp` in `tools/mutate-and-run.sh:491`), not through `strict_scratch_root()`.

## 1. Method

For each of the seven tools that call `strict_scratch_root()` (`r02`), I enumerated every invocation the lane documents for it from two sources named by the item:

1. `tools/registry.json` rows whose `argv` names the tool (`r03`, `r04`);
2. the tool's own `--help`/usage text, captured for all seven (`r05-help-<tool>.txt`; every one exits 0).

For each invocation I read the tool to decide whether that path reaches a `tempfile.*(dir=strict_scratch_root())` call (grep of every `tempfile.` use per tool, `r02`, then the enclosing function), and then probed every invocation outside the counter under `TMPDIR=<nonexistent>` (`r07`–`r14`), plus an `strace` run under a usable `TMPDIR` for the one allocating discovery (`r08`). The frozen counter's mode table was imported from the frozen file itself and echoed in `r06b`/JSON (`counter_modes`), so the 13 labels are the counter's, not mine.

## 2. The counter's 13 modes (frozen)

| # | mode (as invoked) | allocating | expected exit |
|---|---|---|---|
| 1 | `repeat-control --selftest` | yes | 0 |
| 2 | `registry-check --selftest` | yes | 0 |
| 3 | `bash-witness-study selftest` | yes | 0 |
| 4 | `pin-disposition --selftest` | yes | 0 |
| 5 | `evidence-disposition --selftest` | yes | 0 |
| 6 | `context-capture --selftest` | yes | 0 |
| 7 | `env-diff --selftest` | yes | 0 |
| 8 | `env-diff --contract` | yes | 0 |
| 9 | `repeat-control --snapshot` | no (lazy) | 0 |
| 10 | `bash-witness-study count` | no (lazy) | 0 |
| 11 | `pin-disposition --read` (= `--manifest … --root …`) | no (lazy) | 0 |
| 12 | `evidence-disposition --json` (= `--root . --dispositions …`) | no (lazy) | 0 |
| 13 | `context-capture --check` (frozen receipt) | no (lazy) | 0 |

8 allocating + 5 lazy = 13. The frozen docstring says the 8 are "the seven self-tests plus `env-diff --contract` — the one other documented mode that allocates scratch".

## 3. Full documented-mode inventory (21 invocable modes + help)

Sources: `U` = tool usage/`--help` (receipt in parentheses), `R` = registry row(s). `ALLOC` = reaches `dir=strict_scratch_root()`.

| # | mode | tool | documented by | ALLOC? | deciding code (base lines) | in counter? |
|---|---|---|---|---|---|---|
| 1 | `--contract FILE --out FILE [--fleet-root] [--jobs]` | env-diff | U:4 (`r05-help-env-diff.txt`) | **yes** | `env-diff.py:80` `TemporaryDirectory(…, dir=strict_scratch_root())` in `execute()`; reached via `surface_result:192 -> probe:170 -> execute:70`; only after contract parse and after `bwrap` is found (`:78`) | yes |
| 2 | `--selftest` | env-diff | U:5; R `env-diff-selftest` | **yes** | same `:80` via `probe()`; the selftest's own pin fixture `:186` deliberately uses the default temp dir | yes |
| 3 | `--runs N --out DIR -- COMMAND [ARG…]` | repeat-control | U:141-145; `SKILL.md:2181` | no | `:240 run_mode -> :326 run_controls -> :329 os.makedirs(out_dir, exist_ok=False)`; `strict_scratch_root` only at `:611` (`selftest`) | **no** |
| 4 | `--snapshot DIR` | repeat-control | U:143; R `…snapshot-clean/mismatch` | no | `:463 snapshot_mode` (read-only) | yes |
| 5 | `--selftest` | repeat-control | U:144; R `repeat-control-selftest` | **yes** | `:611 mkdtemp(…, dir=strict_scratch_root())` | yes |
| 6 | `[--root DIR] …` (live run) | registry-check | U:118-122 (`r05-help-registry-check.txt`); docstring Interface 11-15 | no | `:1909 work = None`, `:1910 if rev is not None:`; live branch `:1943 root = os.path.abspath(...)` never clones | **no** |
| 7 | `[--root DIR] --rev REV …` | registry-check | U:119; docstring:12; `SKILL.md:2180` (`r16`) | **YES** | `:780 work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir=strict_scratch_root())` in `clone_lane_at_rev` (`:770`), called from `:1927` under `:1910`, after `resolve_rev` (`:1918`) | **no — BLIND SPOT** |
| 8 | `--selftest` | registry-check | U:120; R `registry-check-selftest` | **yes** | `:930-931 mkdtemp(…, dir=strict_scratch_root())` | yes |
| 9 | `declare` | bash-witness-study | docstring modes; argparse `:1766-1777` | no | `:865 cmd_declare`; the only `mkdtemp` in the file is `:1259-1260` in `cmd_selftest` (`:1247`) | **no** |
| 10 | `run [--timeout N] [--tail N]` | bash-witness-study | docstring; argparse `:1766-1777` | no¹ | `:1029 cmd_run -> _execute_sweep` | **no** |
| 11 | `rerun [--timeout N] [--tail N]` | bash-witness-study | docstring; argparse | no¹ | `:1037 cmd_rerun -> _execute_sweep` | **no** |
| 12 | `count` | bash-witness-study | docstring; R `bash-witness-count` | no | `:1070 cmd_count` | yes |
| 13 | `check` | bash-witness-study | docstring; argparse | no | `:1147 cmd_check` | **no** |
| 14 | `selftest` | bash-witness-study | docstring; R `bash-witness-selftest` | **yes** | `:1259-1260 mkdtemp(…, dir=strict_scratch_root())` | yes |
| 15 | `--manifest PATH --root FLEET` | pin-disposition | U:148-150; R `pin-disposition-read` | no | only `:725` (`selftest`) calls `strict_scratch_root` | yes |
| 16 | `--selftest` | pin-disposition | U:149; R | **yes** | `:725` | yes |
| 17 | `--root LANE --dispositions FILE [--json]` | evidence-disposition | U:167-168; R (5 rows) | no | only `:2370` (`selftest`) calls `strict_scratch_root` | yes |
| 18 | `--selftest` | evidence-disposition | U:168; R | **yes** | `:2370` | yes |
| 19 | `--check [--json]` (frozen receipt) | context-capture | U:271-272 Modes block; R `context-capture-frozen` | no | `strict_scratch_root` referenced only at `:1638-1639` inside `class SelftestHarness` (`:1636`); check writes nothing (docstring `:9`, `:19`) | yes |
| 20 | `--check --receipt FILE --expected FILE [--json]` | context-capture | U:271-272; R `context-capture-missing-env`, `…-mapping-suffix` | no | same `:1636-1639` only | **no** |
| 21 | `--selftest` | context-capture | U:272; R | **yes** | `:1638-1639` | yes |
| — | `-h`/`--help` (each tool) | all seven | each `--help` exits 0 (`r05-*`); `context-capture.py:266 KNOWN_ARGUMENTS` | no | handled before scratch: `registry-check.py:1861-1863` returns before `work` (`:1909`); `repeat-control.py:897-901` dispatch `-h` before `run_mode`; `context-capture.py:266` | **no** |

¹ `run`/`rerun` create scratch **in a child**, not through `strict_scratch_root()`: `_execute_sweep` runs `tools/mutate-and-run.sh`, which does `WORKDIR=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-run.XXXXXX")` at `tools/mutate-and-run.sh:491`. Boundary note D3, outside the frozen surface ("the seven tools that call `strict_scratch_root()`").

Totals: **21 documented invocable modes, 9 allocating, 12 non-allocating**, plus the usage mode. The counter covers 13 (8 allocating + 5 lazy).

## 4. The difference (8 documented modes outside the counter) and verdicts

| mode | ALLOC verdict | line of code | probe (unusable `TMPDIR`) |
|---|---|---|---|
| `repeat-control --runs N --out DIR -- COMMAND` | **does not allocate** | `repeat-control.py:329 os.makedirs(out_dir, exist_ok=False)`; no `strict_scratch_root` outside `:611` | `r09`: rc 0, `REPEAT_CONTROL: controls_match` |
| `registry-check` live run (`--root`, no `--rev`) | does not allocate | `registry-check.py:1909-1910`, live branch `:1943`; clone only under `:1910` | `r12`: rc 1 (`ROW repeat-control-selftest … differs` — its *child* honours TMPDIR); no class line from registry-check |
| **`registry-check --rev REV`** | **ALLOCATES** | `registry-check.py:780` (`clone_lane_at_rev`, `:770`) via `:1927` | `r07`: rc 2, stderr **empty**, stdout `REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '…' (could-not-evaluate))`; `r06b`: frozen `GRAMMAR` match on stderr = 0. `r08` (usable TMPDIR + `strace`): `mkdir("<TMPDIR>/tameshi-registry-check-…", 0700) = 0` |
| `bash-witness-study declare` | does not allocate | `:865 cmd_declare`; only `:1259-1260` (`cmd_selftest`) | `r11b`: rc 1 `declared.tsv already exists — declarations are frozen` |
| `bash-witness-study run` | no (strict class) ¹ | `:1029 cmd_run` | `r11c`: rc 2 runner-drift before any sweep |
| `bash-witness-study rerun` | no (strict class) ¹ | `:1037 cmd_rerun` | `r11d`: rc 2 runner-drift before any sweep |
| `bash-witness-study check` | does not allocate | `:1147 cmd_check` | `r11a`: rc 1 `WITNESS_CHECK: DRIFT` |
| `context-capture --check --receipt F --expected F` | does not allocate | `:1636-1639` (`SelftestHarness`) only | `r10`: rc 1 `CONTEXT: MISMATCH (id=missing_injected_environment …)` |

Only one of the eight allocates: **`registry-check --rev`**. The other seven are safe lazily (none reaches the scratch root at all), and none is currently measured.

## 5. Findings

### D1 — the frozen counter's allocating denominator is 8, the documented population is 9 (counter defect; reported, not fixed)

- **Claim under test.** `c2/measure.py` docstring lines 12-13 and 17: "only the self-test was measured, so `env-diff --contract` (the one other documented mode that allocates scratch) was outside the contract", and "grammar  8 allocating modes (the seven self-tests + `env-diff --contract`)". Contract target: "8/8 allocating modes".
- **Fact.** `registry-check --rev` is documented (`r05-help-registry-check.txt`; `SKILL.md:2180` explicitly says "selftest **and --rev** fixture trees via mkdtemp under the scratch root (`$TMPDIR`; a set-but-unusable TMPDIR is could-not-evaluate…)") and allocates at `registry-check.py:780`. Runtime proof: `r08` shows 63 `mkdir`/`mkdirat` calls naming the scratch root, the first being `mkdir("$TMPDIR/tameshi-registry-check-rkgcok0n", 0700)`.
- **Class behaviour.** On the counter's unusable-`TMPDIR` arm (`r07`): exit 2, **zero stderr lines**, one stdout line `REGISTRY_CHECK: could-not-evaluate (…)`. The frozen `GRAMMAR` regex requires a *stderr* line of the form `<tool>: could-not-evaluate: cannot create clone scratch …: '<value>' (could-not-evaluate)`; the paren form and the stdout channel both fail it. `r06b` scores the nine allocating modes: the counter's eight → 6 grammar matches at base (repeat-control and context-capture fail, as the base receipt says), the ninth → **0**, `stderr_lines=0`.
- **Signature consequence.** A complete counter would read `grammar=6/9` at base, and could only reach 9/9 if `tools/registry-check.py` were edited to emit the frozen line on stderr — an edit the round's integration list does **not** contain (item 1 names only `repeat-control.py` and `context-capture.py`). As frozen, `C2_R55_PASS=true` is fully reachable while a documented allocating mode still violates the class. That is the blind spot this seat was sent to find.
- **The paren/stdout shape is pinned, not incidental.** The tool's own selftest exercises `--rev` in its `--rev cases` block (`registry-check.py:1640-1646`): `rev-unknown` is recorded with `check_lines(proc, ["REGISTRY_CHECK: could-not-evaluate"])`, i.e. the selftest asserts the non-grammar stdout text. Aligning `--rev` with the frozen grammar would therefore also require editing that selftest assertion. The counter's grammar arm runs only `--selftest`, which reaches `strict_scratch_root` at `:930` **before** the `--rev cases` block, so the mode is never observed by the measured arm.
- **Not fixed.** `c2/measure.py`, `contract.json`, `freeze.json`, `no-harm.sh`, `deciding-run.sh`, `controls.sh` untouched. No counter recalculated the denominator.

### D2 — the round's own docs inherit the short count (L1-owned; reported, not edited)

- `corpus/knowledge/scratch-root-contract.md` (worktree, `r20`): "**Eight allocating modes** carry it — `env-diff --selftest`, `env-diff --contract`, `repeat-control --selftest`, `registry-check --selftest`, `bash-witness-study selftest`, `pin-disposition --selftest`, `evidence-disposition --selftest`, `context-capture --selftest`" — `registry-check --rev` absent. Line 66-67 also claims "the round-55 counter measures every documented allocating mode, not the self-test only", which is false for `--rev`. Lines 94-97 locate the remaining blind spot "outside the registry and the usage text"; the actual hole is **inside** the usage text (and `SKILL.md:2180`).
- `tools/registry.json` worktree cell `registry-check-selftest`: "Allocating modes: **selftest**." — understated; it is `selftest, --rev`.
- Adding the ninth name does **not** endanger the frozen counter: the note arm counts only that its eight labels appear, and the docs arm only needs the `MARKER` substring. Truthful docs are compatible with the frozen pass condition; only the grammar arm cannot see the ninth mode.

### D3 — boundary: `bash-witness-study run/rerun` reach TMPDIR through a child (recorded, not scored)

`cmd_run`/`cmd_rerun` (`:1029`, `:1037`) never call `strict_scratch_root`; they run `tools/mutate-and-run.sh`, whose `mktemp -d "${TMPDIR:-/tmp}/…"` (`:491`) would create scratch under `$TMPDIR` and fail with the runner's SETUP message, not the frozen grammar. At base the drift precondition stops both before the sweep (`r11c`, `r11d`), so this is code-read only. It is outside the frozen surface ("the seven tools that call `strict_scratch_root()`"), so it is not counted as a counter defect — but a caller who grades `bash-witness-study run` on a bad TMPDIR also sees an unparseable class line.

### O1/O2 — frozen artifacts that disagree with their own anchors (report only; nothing edited)

Observed at 13:57-13:58, lane HEAD `631cd645`:

- **O1 — the base C2 receipt is empty in the worktree.** `.ufo/evidence/round-55/before/c2.stdout` is 0 bytes; the committed file at HEAD carries 43 lines ending `C2_R55: rev=0a2010acd1e9 grammar=6/8 … total=18 C2_R55_PASS=false` (`r22`, recovered read-only with `git show HEAD:…`; `git diff --stat` shows `43 deletions`). The base line quoted in the brief exists only at HEAD. I re-derived the same grammar count independently in `r06b` (6/8 for the counter's eight), so no finding here depends on the emptied file — but the lane's own before-receipt is gone.
- **O2 — the freeze manifest pins hashes that neither HEAD nor the worktree carries**, and its amendment list is one behind the contract's:

  | pinned path | pin | worktree | HEAD |
  |---|---|---|---|
  | `contract.json` | `ed6871e1…` | `0b99dd8c…` MISMATCH | `2388cb50…` MISMATCH |
  | `c2/measure.py` | `ab3ae751…` | `d6ca1d85…` MISMATCH | `9d076812…` MISMATCH |
  | `c1/measure.py`, `no-harm.sh`, `deciding-run.sh`, `controls.sh` | — | MATCH | MATCH |

  `contract.json` carries **4** amendments (the fourth is the strace/exit-code repair shown in `r23`); `freeze.json` carries **3**. The amended `c2/measure.py` is therefore outside its own manifest. `r24-freeze-pin-vs-tree.txt` has the full comparison against both worktree and HEAD.
  **The tree is still moving under the wave.** A second snapshot at `2026-10-28T14:00:26-03:00` (`r24b-freeze-pin-recheck.txt`) reads: `contract.json` `5de4f37b…` (contract now has **5** amendments), `c1/measure.py` `711507e7…` (it matched the pin at 13:58 and now does not), `c2/measure.py` unchanged at `d6ca1d85…`; `no-harm.sh`/`deciding-run.sh`/`controls.sh` still match. So three of six pinned files currently disagree with the manifest, and the amendment counts are 5 (contract) vs 3 (freeze). This may be an L1 integration in flight, but at probe time the manifest does not cover the counters it names, and the "frozen counter set" revision the brief names (`631cd645`) is not what the worktree holds. Reported per the brief; not fixed, and none of these files was written by this seat.

## 6. Sweep actually run (every command, every receipt)

All paths under the lane receipts dir `.ufo/waves/round-55/w1/T55W1ExecModeDiscovery-receipts/`. Clone: `git clone --shared <lane> $S/base && git -C $S/base checkout --detach 0a2010ac…` (asserted `rev-parse --show-toplevel` = `$S/base`, `r01`).

- `r01-base-rev.txt` — clone HEAD = `0a2010acd1e92e4e332774050825e21bcfc7e079`.
- `r02-strict-scratch-root-callers.txt` — every `strict_scratch_root` reference in the seven tools: `env-diff:36,80`; `repeat-control:148,611`; `registry-check:757,780,931`; `bash-witness:209,1260`; `pin-disposition:165,725`; `evidence-disposition:195,2370`; `context-capture:300,1639`. Exactly seven files.
- `r03-registry-rows-seven.txt`, `r04-registry-scratch-cells-base.txt` — registry rows per tool (19 rows → 13 modes) and the seven round-54 `scratch_root` cells at base.
- `r05-help-<tool>.txt` ×7 — `--help`/`-h` all exit 0 with the usage blocks quoted above.
- `r06b-grammar-check-nine-allocating-modes.txt` — the frozen `GRAMMAR` regex applied to all nine allocating modes under `TMPDIR=<nonexistent>`.
- `r07-registry-check-rev-unusable.txt` — `TMPDIR=<nonexistent> python3 tools/registry-check.py --rev 0a2010ac… --only repeat-control-selftest` → rc 2, stderr empty, stdout paren class line.
- `r08-registry-check-rev-usable.txt` + `r08-registry-check-rev-usable.strace` — same mode, usable `TMPDIR`, `strace -f -e trace=mkdir,mkdirat` → scratch-root `mkdir` at `$TMPDIR/tameshi-registry-check-…`.
- `r08b-registry-check-selftest-unusable.txt` — the counter's own arm for the same tool → rc 2, stderr line matches `GRAMMAR`.
- `r09-repeat-control-run-unusable.txt` — run mode, rc 0 `controls_match`.
- `r10-context-capture-explicit-unusable.txt` — explicit `--receipt/--expected`, rc 1 `missing_injected_environment`.
- `r11a…e-bash-witness-*-unusable.txt` — `check` rc 1, `declare` rc 1, `run` rc 2, `rerun` rc 2, `count` rc 0; none a scratch class line.
- `r12-registry-check-live-unusable.txt` — live run, rc 1 (child row differs), no scratch class from registry-check.
- `r13-pin-disposition-run-unusable.txt`, `r14-evidence-disposition-run-unusable.txt` — rc 0 each under unusable `TMPDIR`.
- `r16-skill-md-registry-check-rev-doc.txt` — base `SKILL.md:2180` documenting `--rev` mkdtemp under the scratch root and could-not-evaluate.
- `r17-census-validate.txt` — `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → **rc 0**, last line `tameshi ok …/corpus/SOURCES.md`.
- `r18-lane-state.txt`, `r19-registry-check-unchanged-in-worktree.txt` — lane HEAD/status; `git diff 0a2010ac -- tools/registry-check.py` is empty.
- `r20-current-note-claims.txt` — the worktree note's "Eight allocating modes" claim.
- `r21-registry-check-selftest-rev-case-assertion.txt` — the selftest `--rev cases` block asserting the paren/stdout class text.
- `r22-before-c2-committed.txt` — the 43-line base C2 receipt as committed at HEAD (worktree copy is empty; O1).
- `r23-c2-measure-worktree-vs-head.diff` — worktree counter differs from HEAD only by the four recorded amendments; `modes()` and `GRAMMAR` identical.
- `r24-freeze-pin-vs-tree.txt` — freeze pins vs worktree and HEAD (O2).
- `r24b-freeze-pin-recheck.txt` — second snapshot at 14:00:26 showing the live churn (3/6 mismatch, contract 5 amendments vs freeze 3).

Reproduce the decisive pair exactly:

```bash
S=/fast/scratch/hyaku/tameshi-r55/<seat>; git clone --shared <lane> "$S/base"
git -C "$S/base" checkout --detach 0a2010acd1e92e4e332774050825e21bcfc7e079
cd "$S/base"
TMPDIR="$S/no-such" python3 tools/registry-check.py --rev 0a2010acd1e92e4e332774050825e21bcfc7e079 --only repeat-control-selftest; echo rc=$?
# -> rc=2, stdout: REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch ...); stderr empty
mkdir -p "$S/tmp-ok"
TMPDIR="$S/tmp-ok" strace -f -e trace=mkdir,mkdirat -o "$S/t.strace" \
  python3 tools/registry-check.py --rev 0a2010acd1e92e4e332774050825e21bcfc7e079 --only repeat-control-selftest
grep -c "$S/tmp-ok" "$S/t.strace"   # -> 63 mkdir/mkdirat under the scratch root
```

## 7. Files changed / behavior / risks / blockers

**Production files changed by this seat: none.** Writes are limited to this report, `T55W1ExecModeDiscovery.json` (machine-readable inventory + difference + findings), and the receipts dir above. No frozen file, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**` was touched; no mutating git/jj command was run in the lane; fixture git use was confined to the scratch clone (`-C`, toplevel asserted).

**Behavior observed (base, `TMPDIR` set-but-unusable).** 9 documented modes allocate scratch; 8 of them print the frozen one-line grammar (or will after the round-55 edits to `repeat-control`/`context-capture`); `registry-check --rev` prints a paren-form class line on stdout with empty stderr. 12 documented modes do not allocate and stay lazy (7 measured as lazy by the counter, 5 not measured).

**Risks.**
- If the L1 treats the frozen "8/8" as the whole population, the round ships a note, seven registry cells and a SKILL sentence that are false in exactly the way the round is about (`registry-check --rev` omitted). The cheap correction (add `registry-check --rev` to the note and to the `registry-check-selftest` cell) is compatible with the frozen counter; the counter itself cannot be repaired by this seat and its grammar arm cannot reach 9/9 without a `registry-check.py` edit that the integration list does not authorise.
- A caller that parses the class by prefix gets `REGISTRY_CHECK: could-not-evaluate (` — a different token shape from every other tool (`<tool>.py: could-not-evaluate: …`). Documented as-is; not fixed.
- Scratch instability: my first scratch tree under `/fast/scratch/hyaku/tameshi-r55/` was removed mid-run (all seat dirs recreated at 13:54); receipts were therefore written into the lane's wave dir as they were produced. Nothing was lost except disposable clone copies.

**Blockers: none.** Everything the item asks for is measured or read; the only unresolved item is the L1 decision on D1/D2, which is explicitly not mine to make.

**Tooling.** No installs or upgrades. Python 3, git, strace and bwrap 0.13.1 (`/usr/bin/bwrap`) were already present; no pacman transaction was attempted.

Report: .ufo/waves/round-55/w1/T55W1ExecModeDiscovery.md
