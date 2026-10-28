# T55W1ExecRegistryGate — registry gate after the seven-cell reword + the two tool patches

seat: T55W1ExecRegistryGate (executor, round-55 wave 1)
item: run `tools/registry-check.py --selftest` at base, then in a scratch clone after the seven-cell `scratch_root` reword plus the two tool patches; run `tools/registry-replay.py`'s self-test; report every verdict, name any cell that broke the gate.
base: `0a2010acd1e92e4e332774050825e21bcfc7e079`
integration of record measured: `133b2ce6d4d86d783db38607343c3654350194b8` (C0 integration in parent `9cf0146`; freeze amendment 8 moved the pointer here)
scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1ExecRegistryGate` (`base`, `patchedA`, `patchedB`, `tip` clones; receipts copied to `T55W1ExecRegistryGate-receipts/`)
production files touched: **none.** No lane production file was edited; no mutating git command ran on the lane; no tool was installed.

## 1. Verdict

**No registry-gate regression.** `registry-check --selftest` and `registry-replay --selftest` hold at every state measured, before and after the seven-cell reword and both tool patches, and at the landed integration.

| state | `registry-check.py --selftest` | `registry-replay.py --selftest` | gate rows (`--only`, each) |
|---|---|---|---|
| base `0a2010a` | **rc 0** `SELFTEST: PASS (51 cases)` | **rc 0** `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | — |
| draft A: base + `registry-cells.patch` + `RepPatch/patch.diff` + `CcPatch/context-capture.patch` | **rc 0** `SELFTEST: PASS (51 cases)` | **rc 0** `10/10 pass` | `registry-check-selftest` held 1/1, `registry-replay-selftest` held 1/1 |
| draft B: base + consolidated `T55W1ExecC2Full-receipts/patches.diff` (cells, both tools, SKILL, note) | **rc 0** `SELFTEST: PASS (51 cases)` | **rc 0** `10/10 pass` | each held 1/1 |
| tip `133b2ce` (landed C0 `9cf0146`) | **rc 0** `SELFTEST: PASS (51 cases)` | **rc 0** `10/10 pass` | each held 1/1 |

Receipts: `base-registry-check-selftest.{stdout,stderr,rc}`, `base-registry-replay-selftest.*`, `patchedA-*`, `patchedB-*`, `tip-registry-check-selftest.stdout`, `tip-registry-replay-selftest.stdout`, `tip-gate-*`, `tip-state-and-rc-summary.txt`.

The reword is gate-inert by construction, and the diff proves it changed nothing the gate reads:

```
rows base 56 tip 56 names_equal True
changed 7
  repeat-control-selftest ['scratch_root']
  bash-witness-selftest ['scratch_root']
  pin-disposition-selftest ['scratch_root']
  evidence-disposition-selftest ['scratch_root']
  context-capture-selftest ['scratch_root']
  registry-check-selftest ['scratch_root']
  env-diff-selftest ['scratch_root']
```

(`tip-registry-row-diff.txt`; the same result at draft A and B: 7 changed rows, `scratch_root` only.) `registry_errors()` in `tools/registry-check.py:181-289` validates schema, name, kind, argv, expect, timeout, source, status, tags, `external`, `discriminating` — `scratch_root` is not a validated field, so no cell spelling can fail the gate. No row's `argv` reads the cell either (the only rows whose argv mention `registry`/`scratch` are `registry-check-selftest` and `registry-replay-selftest`, and both run their own self-test). The `--selftest` path is hermetic and builds its own fixture registries, so it never reads `tools/registry.json` at all.

## 2. Commands (exact)

```
# base
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/base
git -C $S/base checkout --detach 0a2010acd1e92e4e332774050825e21bcfc7e079
cd $S/base && python3 tools/registry-check.py --selftest   # rc 0, SELFTEST: PASS (51 cases)
cd $S/base && python3 tools/registry-replay.py --selftest  # rc 0, REGISTRY_REPLAY_SELFTEST: 10/10 pass

# draft A (three named drafts, latest of each kind)
git apply .ufo/waves/round-55/w1/T55W1ExecCells-receipts/registry-cells.patch
git apply .ufo/waves/round-55/w1/T55W1ExecRepPatch-receipts/patch.diff
git apply .ufo/waves/round-55/w1/T55W1ExecCcPatch-receipts/context-capture.patch
# draft B (consolidated)
git apply .ufo/waves/round-55/w1/T55W1ExecC2Full-receipts/patches.diff

# each clone
python3 tools/registry-check.py --selftest                   # rc 0, 51 cases
python3 tools/registry-replay.py --selftest                  # rc 0, 10/10
python3 tools/registry-check.py --root <clone> --registry tools/registry.json --only registry-check-selftest
python3 tools/registry-check.py --root <clone> --registry tools/registry.json --only registry-replay-selftest

# tip
git clone --shared ... $S/tip && git -C $S/tip checkout --detach 133b2ce6d4d86d783db38607343c3654350194b8
python3 tools/registry-check.py --selftest                   # rc 0, 51 cases
python3 tools/registry-replay.py --selftest                  # rc 0, 10/10
```

Both patched clones apply cleanly (`patchedA-diffstat.txt` = 3 files, 30 insertions; `patchedB-diffstat.txt` = 5 files, 117 insertions) and `json.load` accepts the reworded `tools/registry.json` in both.

## 3. Findings — no cell broke the gate; four cells misstate what their tool prints

The gate cannot see these (unvalidated field, marker-only docs arm), so they are reported with the command and the observed bytes. `TMPDIR` is a nonexistent path in every probe; cwd is the tip clone; full nine-mode matrix in `tip-mode-matrix.txt`.

| cell | quoted in the cell | actually printed on stderr | stdout |
|---|---|---|---|
| `repeat-control-selftest` | `repeat-control.py: could-not-evaluate: …` | `repeat-control: could-not-evaluate: …` | **`REPEAT_CONTROL: setup_error`** |
| `registry-check-selftest` | `registry-check.py: could-not-evaluate: …` | `registry-check: could-not-evaluate: …` | empty |
| `bash-witness-selftest` | `bash-witness-study.py: could-not-evaluate: …` | `WITNESS_STUDY: could-not-evaluate: …` | empty |
| `env-diff-selftest` | `env-diff.py: could-not-evaluate: …` | `ENVDIFF_SETUP: could-not-evaluate: …` | empty |
| `pin-disposition-selftest` | `pin-disposition.py: …` | `pin-disposition.py: …` | empty |
| `evidence-disposition-selftest` | `evidence-disposition.py: …` | `evidence-disposition.py: …` | empty |
| `context-capture-selftest` | `context-capture.py: …` | `context-capture.py: …` | empty |

Observed lines and cell strings: `tip-cell-prefix-evidence.txt`. All nine allocating modes (the seven self-tests, `env-diff --contract`, `registry-check --rev`) exit 2 with a grammar-matching stderr line at tip (`tip-mode-matrix.txt`), so the frozen grammar's `[A-Za-z][A-Za-z0-9_.-]*(\.py)?` prefix admits every actual label — which is exactly why no counter arm can catch the three misquoted literals.

**F1 — `repeat-control-selftest` (highest): stdout carries a setup token.** The round's integration item 1 requires "stdout carries no setup error". At tip:

```
$ env TMPDIR=$S/no-such-tmpdir python3 tools/repeat-control.py --selftest
rc=2
stdout: REPEAT_CONTROL: setup_error
stderr: repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root:
        TMPDIR is not a usable directory: '<…>' (could-not-evaluate)
```

The cell also quotes prefix `repeat-control.py:` while the tool prints `repeat-control:`. The frozen C2 grammar arm passes anyway: it checks `rc == 2`, a grammar-matching stderr line, and the absence of `RuntimeError`/`Traceback` — it does not read stdout. The fix already exists on disk in `T55W1ExecC2Full-receipts/patches.diff` (13:55) and was measured in draft B: stdout empty, prefix `repeat-control.py`, rc 2. The landed tree still carries the stdout-emitting version (`tools/repeat-control.py` sha256 `a8fad68f…`; `T55W1ExecRepPatch-receipts/patch.diff` is the stdout-emitting draft).

**F2/F3/F4 — `registry-check-selftest`, `bash-witness-selftest`, `env-diff-selftest` quote a prefix their tool never prints.** An operator copying the cell's literal line into a matcher fails on these three; the class line itself is correct. Minimal fix (L1 applies; not mine to edit): swap the four quoted labels to `repeat-control:`, `registry-check:`, `WITNESS_STUDY:`, `ENVDIFF_SETUP:` respectively, or state "the tool's own label, e.g. `ENVDIFF_SETUP`" instead of a `*.py` literal.

**F5 — the seven cells do not name the allocating set (integration item 2).** Each tip cell ends `Allocating modes: selftest.` (`registry-check-selftest`: `selftest, --rev`; `env-diff-selftest`: `selftest, --contract`). No cell lists the class's allocating modes, whereas item 2 asks the seven cells to state the grammar **and the eight allocating modes**; the drafts (`T55W1ExecCells-receipts/registry-cells.patch`) did list all eight in every cell and the landed cells dropped that. The C2 `docs` arm only checks the marker substring, so it reads 7/7 either way. Suggested append to each cell: `The class covers every allocating mode: env-diff --selftest, env-diff --contract, repeat-control --selftest, registry-check --selftest, registry-check --rev, bash-witness-study selftest, pin-disposition --selftest, evidence-disposition --selftest, context-capture --selftest.`

**Draft pairing (attack that found nothing at the gate, but found a docs lie).** Draft A pairs the `T55W1ExecCells` cells (which say "nothing on stdout") with the 13:55 standalone `RepPatch/patch.diff` (which emits the stdout token): measured in clone A, `repeat-control --selftest` → `stdout='REPEAT_CONTROL: setup_error\n'`, so draft A's cell text is false. Draft B's consolidated patch pairs the same cell family with the stdout-free handler and measures true. If the two drafts are used together verbatim, `repeat-control-selftest` is the cell that breaks; if the consolidated patch is used, nothing does.

## 4. Reported, not fixed: brief vs landed frozen set

The seat brief states the frozen grammar over **eight** allocating modes (`grammar=6/8`, `note=0/8`). The landed contract (`.ufo/evidence/round-55/contract.json`, amended, freeze pointer `133b2ce`) and the amended counter are over **nine** (`registry-check --rev` added by freeze amendment 6; `grammar=6/9`, `note=0/9`). My tip measurement supports the landed denominator: all nine allocating modes print the grammar line (`tip-mode-matrix.txt`). Both the frozen commit `631cd64` and the amended worktree freeze.json are internally consistent (every pinned sha256 matches its file; measured 14:22). Nothing was edited; this is recorded because the brief and the frozen set disagree on 8 vs 9.

## 5. Limits

- The decisive gate run here is `--only` on the two registry rows plus both full self-tests; a full 56-row `--rev` run was not needed because the semantic row diff shows no argv/expect/status/source/timeout change and no row reads a `scratch_root` cell.
- `registry-check --selftest` is hermetic and fixture-only: it cannot prove the cell prose, only that the reword breaks nothing mechanical. The prefix/stdout mismatches above come from direct mode probes, not from the gate.
- The lane was moving during the seat (HEAD read `631cd64` at start, `133b2ce` at the end, C0 landing in between); all tip statements are anchored to `133b2ce` and the sha256 set in `tip-state-and-rc-summary.txt`.

## 6. Receipts

`T55W1ExecRegistryGate-receipts/`: base/draft A/draft B/tip self-test stdout+stderr+rc; `mode-matrix.txt` (8 modes × A/B/worktree), `tip-mode-matrix.txt` (9 modes at tip), `tip-registry-row-diff.txt`, `tip-cell-prefix-evidence.txt` (cell strings + observed lines), `tip-gate-*.{out,err}`, `patched{A,B}-gate-*`, `patched{A,B}-diffstat.txt`, `tip-state-and-rc-summary.txt`, `worktree-*` probes, `census-validate.txt` (`sources-census.sh validate` → rc 0, 139-row floor; only W04 duplicate-url warnings).
