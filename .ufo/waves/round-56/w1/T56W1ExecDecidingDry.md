# T56W1ExecDecidingDry — deciding-run refusal matrix (dry runs)

**Item:** prove `.ufo/evidence/round-56/deciding-run.sh` refuses before it runs anything, in a scratch clone at `c3e2ca9f020776b3d66c7af854fb82c834674fcf`, for (a) tampered freeze manifest, (b) `REV != HEAD`, (c) missing control receipt, (d) dirty tree, (e) second invocation, (f) control receipts not descending from the freeze, (g) a refusing receipt-binding gate — each with exit code and the exact refusal line, noting any refusal that cannot fire.

**Result: all seven demanded refusals fire, exit 3, before any counter/no-harm/precheck/census work — plus six sibling refusals fired and two real escape hatches found** (a manifest-entry deletion is accepted; a dirty-tree exclusion prefix-match lets an untracked file through). One reachability defect: `control-receipt-not-after-freeze` cannot be exercised from a `REV` whose tree lacks the script (exit 127); the faithful instance is a merge.

## Method

- `git clone --shared` of the lane → `$HYAKU_SCRATCH/tameshi-r56/T56W1ExecDecidingDry/clone`; `git rev-parse --show-toplevel` asserted equal to the clone before every fixture commit; all fixture commits, branches and the merge exist only in the clone. No git mutation anywhere else.
- `checkout --detach c3e2ca9f…`; the worktree `deciding-run.sh` is byte-identical to the frozen manifest's digest `6a63f505…` (receipt `00-clone.txt`), so the script under test is the frozen instrument.
- Per arm: fresh empty `OUT=$CLONE/.ufo/evidence/round-56/dryout`, per-arm `HYAKU_SCRATCH`, capture exit + output + OUT listing + SCR existence + canary files (`c1.stdout`, `c2.stdout`, `no-harm.stdout`, `coldread-precheck.stdout`, `census.stdout`, `frozen.stdout`). Arms that pass every pre-run gate run under `setsid` and are killed by process group after a bound (`d0`, `d3`, `d3b`).
- Drivers (reproducible): `T56W1ExecDecidingDry-receipts/driver.sh`, `driver2.sh`. Per-arm receipts: `T56W1ExecDecidingDry-receipts/<arm>.txt` (input state + output + artifacts); raw stdout+stderr: `<arm>.raw`.
- Control-receipt fixtures: four files under `$E/control/` (a.stdout/a.exit/b.stdout/b.exit) with `CONTROLS_A: 2/2 as pre-registered` / `CONTROLS_B: 1/1 as pre-registered`, `rev=` naming the freeze — accepted by the binding gate at `REV=fix-d` because `frozen-surface.paths` is byte-identical between the freeze and `fix-d` (d0 proves the fixture is gate-clean end to end).

## Refusal matrix

| item | arm | condition | exit | exact line | runs nothing? |
|---|---|---|---|---|---|
| (a) | a1 | freeze.json digest for `no-harm.sh` := 64 zeros (new freeze commit) | 3 | `DECIDING_REFUSED freeze-integrity` (after `FREEZE_MISMATCH no-harm.sh a13ba1a84337 != 000000000000`) | yes — OUT empty, SCR absent |
| (a) | a2 | `no-harm.sh` bytes changed at the freeze commit, manifest untouched | 3 | `DECIDING_REFUSED freeze-integrity` (`…5aa2dcbe40cf != a13ba1a84337`) | yes |
| (a) | a3 | `deciding-run.sh` entry **deleted** from `files{}` | 3 | `DECIDING_REFUSED control-receipt-missing …` — **`FREEZE_INTEGRITY: OK files=9`**: escape, see F-1 | yes |
| (b) | b | HEAD=`c3e2ca9f`, `REV`=`981c5e8b` | 3 | `DECIDING_REFUSED head-is-not-rev` | yes |
| (c) | c1missing | `REV`=`HEAD`=freeze — receipts genuinely absent at the freeze | 3 | `DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-56/control/controls-a.stdout` | yes |
| (c) | c2tree | `controls-b.stdout` committed as a directory | 3 | `DECIDING_REFUSED control-receipt-not-a-blob …` | yes |
| (c) | c3empty | `controls-b.stdout` committed as a 0-byte blob | 3 | `DECIDING_REFUSED control-receipt-empty …` | yes |
| (d) | d0 | **positive control:** gate-clean fixture, clean tree, empty OUT | bounded kill @45s | **no refusal** — `FREEZE_INTEGRITY OK`, `GATE … verdict=PASS`, `FROZEN_UNCHANGED=1`, no-harm runs, `coldread-precheck.stdout` created | (proceeds — expected) |
| (d) | d1 | ` M corpus/SOURCES.md` | 3 | `DECIDING_REFUSED dirty-tree` + porcelain dump | yes — counters/no-harm/precheck canary all absent; only `receipt-gate.*`+`clean-tree-before.txt` in OUT (gate 0b ran by design) |
| (d) | d2 | untracked file outside OUT (`?? …/dirty-canary.txt`) | 3 | `DECIDING_REFUSED dirty-tree` | yes |
| (d) | d3b | untracked file `?? .ufo/evidence/round-56/dryout-extra.txt` (extends OUT's rel path `…/dryout`) | bounded kill @8s | **no `dirty-tree` refusal** — `clean-tree-before.txt` contains the foreign `??` line; run proceeds into no-harm. Escape, see F-2 | no (runs!) |
| (e) | e1 | `OUT/c1.start` present | 3 | `DECIDING_REFUSED second-invocation c1` | yes — SCR absent |
| (e) | e2 | `OUT/c2.start` present | 3 | `DECIDING_REFUSED second-invocation c2` | yes |
| (e) | e3 | both start files | 3 | `DECIDING_REFUSED second-invocation c1` | yes |
| (f) | f2 | receipts committed on base-rooted `fix-f` (freeze **not** ancestor), merged `--no-ff` into freeze-rooted `fix-f2` → `REV`=`dc01c2fb…` descends from freeze, receipt's touching commit `3b215e57…` does not | 3 | `DECIDING_REFUSED control-receipt-not-after-freeze .ufo/evidence/round-56/control/controls-a.stdout` | yes |
| (f) | f | same intent, plain base-rooted `REV` (no merge) | 127 | `bash: …/deciding-run.sh: No such file or directory` — the script does not exist in `fix-f`'s tree; see F-7 | n/a (cannot start) |
| (g) | g1 | `controls-b.stdout` = the real round-54 set (`rev=7df0e0426c98` absent) | 3 | `DECIDING_REFUSED receipt-binding GATE: receipts=2 ok=1 refused=1 codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED` (`receipt-gate.exit`=3) | yes — refused before counters |
| (g) | g2 | `controls-b.stdout` = real round-54 `CTL_POS_c1` line (`rev=077d431e6996`) | 3 | `DECIDING_REFUSED receipt-binding GATE: … codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED` | yes |
| (g) | g4 | `controls-a.stdout` names `fix-f` (resolvable, not an ancestor) | 3 | `DECIDING_REFUSED receipt-binding GATE: … codes=RECEIPT_CONTROL_NOT_ANCESTOR verdict=REFUSED` | yes |
| extra | outdir | `OUT` nonexistent | 3 | `DECIDING_REFUSED outdir-missing` | yes |
| extra | va | worktree `controls-a.stdout` lacks `CONTROLS_A:` | 3 | `DECIDING_REFUSED controls-a-verdict-missing` | yes |
| extra | vb | worktree `controls-b.stdout` lacks `CONTROLS_B:` | 3 | `DECIDING_REFUSED controls-b-verdict-missing` | yes |

Order verified from receipts: freeze-integrity → outdir-missing → head-is-not-rev → control-receipt loop (missing → not-a-blob → empty → not-after-freeze) → verdict greps → second-invocation → `SCR` build → gate 0b (`receipt-binding`) → dirty-tree → run. "Runs nothing" is literal through second-invocation; after that point `SCR` exists and gate 0b has run (that *is* the (g) check) but no counter/no-harm/precheck/census work happens before a refusal.

## Refusals that cannot fire — and what fires instead

- No `DECIDING_REFUSED` line in the script is unreachable: all 10 distinct refusal strings were fired (freeze-integrity, outdir-missing, head-is-not-rev, control-receipt-{missing,not-a-blob,empty,not-after-freeze}, controls-{a,b}-verdict-missing, second-invocation, receipt-binding, dirty-tree).
- `control-receipt-not-after-freeze` is unreachable from a `REV` whose tree lacks the script — a side-branch `REV` that predates the freeze exits 127 at the shell, not a refusal (arm `f`). Faithful reachability needs a merge-shaped `REV` (arm `f2`). For the real round this is harmless: the real `REV` will descend from the freeze.
- `receipt-binding` via gate exit 2 (unresolvable certified rev) cannot fire here — `REV` is `rev-parse --verify`'d earlier, so the gate always gets a resolvable `--certified`.
- Non-refusal failures (the exit-2 family: relative LANE, unresolvable REV/FREEZE, `git show` failures at the SCR-copy step) were not exercised; they precede the run by construction.
- `NOHARM_OK_COUNT!=15`, `FROZEN_UNCHANGED=0`, precheck/census/counter failures are post-refusal scoring, not refusals — out of matrix scope.

## Findings (instrument defects — reported, never edited)

- **F-1 freeze.json is self-referential (a3):** deleting `deciding-run.sh` from `files{}` yields `FREEZE_INTEGRITY: OK files=9` — the manifest pins everything except itself, and the only other check (`git diff $FREEZE $REV -- $FROZEN`) treats `FREEZE` as the baseline. A freeze commit carrying a manifest with dropped entries is accepted. Mitigation the L1 may consider in *content*: keep freeze.json itself inside `contract.frozen_paths` scrutiny (it is there) **and** have a peer seat independently count `files{}` = 10 at the freeze.
- **F-2 dirty-tree exclusion is an unanchored, unescaped grep prefix match** (`grep -vc "^?? ${OUT#$LANE/}"`, deciding-run.sh:77): any untracked path whose name extends OUT's relative path (`dryout-extra.txt` vs OUT `dryout/`) is excluded; the run proceeds with a dirty tree (d3b `clean-tree-before.txt` shows the foreign `??` line while `no-harm.stdout` was already being written). Fix direction (report only): exclude `^?? <rel>/` (trailing slash) or `git status --porcelain -- . ':(exclude)<rel>/**'`.
- **F-3 receipt inputs are read from the worktree, not `REV`:** gate 0b passes `$LANE/$E/control/controls-{a,b}.stdout` and the verdict greps read the same worktree files, while the loop checks committed blobs at `REV`; both run *before* dirty-tree. A dirty worktree receipt is judged by the gate (and passes/fails on uncommitted bytes) before the tree check refuses the run (d1/va/vb show the ordering). In a clean tree the two sources agree, so the residual risk is only the F-2 escape widening it.
- **F-4 second-invocation is per-OUT:** a second invocation into a different OUTDIR is not refused — the contract's `deciding_invocations: 1` is a wave rule the script cannot enforce globally.
- **F-5 `[ -d "$OUT" ]` accepts a non-empty OUT** despite the usage comment promising EMPTY; only `c1.start`/`c2.start` are probed.
- **F-6 `amendments` in freeze.json is counted but never validated** (printed `amendments=0`; a nonzero value would pass silently).
- **F-7 reachability:** `control-receipt-not-after-freeze` cannot be demonstrated from a `REV` lacking the script (arm `f`, exit 127) — only via a merge (arm `f2`) or a `REV` that re-adds the script. Worth a note in the lesson: the refusal's threat model is "receipts committed off-freeze then merged", which is exactly what `f2` builds.
- Positive note: every refusal prints on stderr/stdout *before* any `OUT` artifact is created for arms that refuse before the SCR build; `rm -rf "$SCR"`+`mkdir` happens only after second-invocation, so a refused run leaves zero scratch residue and zero `OUT` artifacts (a1,b,c*,e*,f2,outdir,va,vb receipts confirm `SCR absent`, `OUT` empty or containing only the planted `c*.start`).

## Lane hygiene / discipline

- No lane production file, no frozen instrument, no fleet-root file modified; lane diff untouched (`git status` on the lane shows only pre-existing `?? .ufo/evidence/round-56/before/` and `?? .ufo/waves/round-56/`). All commits/branches/merges live in the `--shared` scratch clone; the lane object store was only *read* (alternates) — no `gc`/`prune` run.
- Bounded arms used `setsid` + process-group kill in scratch only; no stray processes left (each receipt records `STILL_RUNNING_AFTER` and post-run OUT/SCR state).
- Installs/updates: none. Tools used: system `git`, `bash`, `python3` (stdlib), `sha256sum`, `grep` — all pre-installed.
- Peer traffic: one stray `DISALLOWED` from `C2Floor` (kaidoku lane, different round); clarified and ignored — no bearing on this seat.

## Files

- This report: `.ufo/waves/round-56/w1/T56W1ExecDecidingDry.md`
- Machine-readable matrix: `.ufo/waves/round-56/w1/T56W1ExecDecidingDry.json`
- Receipts: `.ufo/waves/round-56/w1/T56W1ExecDecidingDry-receipts/` — `driver.sh`, `driver2.sh`, `00-clone.txt` (clone/toplevel/digest evidence), `01-fixtures.txt` + `02-f2-graph.txt` (fixture SHAs and ancestry proof), `f2-merge.log`, `<arm>.txt` / `<arm>.raw` for all 21 arms.
