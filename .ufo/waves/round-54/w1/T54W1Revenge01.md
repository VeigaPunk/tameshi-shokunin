# T54W1Revenge01 — who depended on the old CR47 exit class

Item: find every dependency on the **old** behaviour of the four tools C0 edited
(`tools/env-diff.py`, `tools/bash-witness-study.py`, `tools/evidence-disposition.py`,
`tools/pin-disposition.py`), sweeping SKILL.md, `corpus/`, `tools/*.json`,
`tools/*.py`, `.ufo/evidence/round-52` and `.ufo/evidence/round-53`, and reading
every registry row with `expect.exit` 1 or 2. No lane file was edited.

Revisions: base `d33053f7552d`, C0 `59c38109bf119d0e9d4f878644a82babc937bc1e`,
and — because a fix commit landed **while this seat was working** — the new tip
`99c3bc88d704566197783f66b211ee0a830e0330` ("the env-diff run-path class").
The item is stated against C0; every claim below is labelled with the revision
it holds at.

## Answer

**No row, counter, gate or tool depends on the old class** (rc 1 + `RuntimeError`
traceback on a set-but-unusable `TMPDIR`). The one class of dependency that
exists is not on the *class* but on *editing the waived historical inputs at
all*: an **uncommitted** edit to `tools/pin-disposition.py` or
`tools/bash-witness-study.py` flips the registered row
`evidence-disposition-round18-before` from exit 1 to exit 2
(`historical_input_uncommitted`) — proven in §5.4. C0 committed its edits, and
the tip commit touched only `tools/env-diff.py` (not a waived input), so every
row holds at all three revisions.

Two **defects** were found; both are claim-vs-behaviour divergences created by
C0's new sentences, both are **already fixed at the tip** `99c3bc8`:

| # | where (C0 bytes) | what | state at tip |
|---|---|---|---|
| D1 | `SKILL.md:32-39` standing-rules bullet, "never a traceback, never exit 1" | falsified at C0 by `tools/env-diff.py:80` reached from the `--contract` run path, which still tracebacked with rc 1 | fixed (`99c3bc8` adds the run-path catch); probe now rc 2, no traceback |
| D2 | `corpus/knowledge/scratch-root-contract.md:15` and `:42-44` ("the tool refuses before it allocates … caught at the entry point"), and `corpus/lessons/round-54.md` R53.6 ("the four now … map it to exit 2 with a naming line") | same over-claim: true of env-diff only on the `--selftest` path at C0 | true at tip; lesson text unchanged and now accurate |

Plus one **pre-existing nit still open at tip** (N1, §4.6): the round-53
spot-check's own nit — `tools/context-capture.py:27` still describes the scratch
root as `tempfile.gettempdir()`.

## 1. The class flip itself (what "old behaviour" means)

Receipt: `T54W1Revenge01-receipts/selftest-exit-flip.txt`.
Driver, per revision: `TMPDIR=/nonexistent/round54-probe python3 <clone>/tools/<tool> <selftest-arg>`
on `git clone --shared` copies checked out at each revision.

```
[base] env-diff.py rc=1 traceback_lines=1 stderr_last=RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/round54-probe' (could-not-evaluate)
[base] bash-witness-study.py rc=1 traceback_lines=1 stderr_last=RuntimeError: cannot create clone scratch …
[base] evidence-disposition.py rc=1 traceback_lines=1 stderr_last=RuntimeError: cannot create clone scratch …
[base] pin-disposition.py rc=1 traceback_lines=1 stderr_last=RuntimeError: cannot create clone scratch …
[c0] env-diff.py rc=2 traceback_lines=0 stderr_last=ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch …
[c0] bash-witness-study.py rc=2 traceback_lines=0 stderr_last=WITNESS_STUDY: could-not-evaluate: cannot create clone scratch …
[c0] evidence-disposition.py rc=2 traceback_lines=0 stderr_last=evidence-disposition.py: could-not-evaluate: cannot create clone scratch …
[c0] pin-disposition.py rc=2 traceback_lines=0 stderr_last=pin-disposition.py: could-not-evaluate: cannot create clone scratch …
[c0/usable] env-diff.py rc=0 last=ENVDIFF_SELFTEST: 9/9 pass
[c0/usable] bash-witness-study.py rc=0 last=VERDICT: PASS
[c0/usable] evidence-disposition.py rc=0 last=SELFTEST: PASS (66/66)
[c0/usable] pin-disposition.py rc=0 last=SELFTEST: PASS (19/19)
```

The four prefixes differ (`ENVDIFF_SETUP:`, `WITNESS_STUDY:`,
`evidence-disposition.py:`, `pin-disposition.py:`), each line names the value and
the class — the C2 claim's wording ("one naming could-not-evaluate line") holds.
The usable-root arm is unchanged from base, so nothing that runs these
self-tests under a normal `TMPDIR` can observe the change.

## 2. Registry rows — the whole ledger

Receipt: `T54W1Revenge01-receipts/row-ledger.txt`.

`tools/registry.json` at C0: 56 rows — **48 × `expect.exit` 0, 8 × 1, 0 × 2**.
The new exit class is therefore **pinned by no row** (see §6 risk note). Every
row with `expect.exit` 1 or 2, read in full:

```
exit=1 repeat-control-snapshot-mismatch        active      repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch
exit=1 evidence-disposition-round17-before     superseded  evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json
exit=1 evidence-disposition-round18-before     active      evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json
exit=1 context-capture-missing-env             active      context-capture.py --check --receipt …/context-missing-env/receipt.json --expected …/expected.json
exit=1 context-capture-mapping-suffix          active      context-capture.py --check --receipt …/mapping-suffix/receipt.json --expected …/expected.json
exit=1 wave-accounting-wrong-count-entry       active      wave-accounting.py --bundle … --expected … --json
exit=1 command-binding-source-read-red         superseded  command-binding.py --bundle … --expected … --json
exit=1 command-binding-source-read-red-pinned  active      command-binding.py --bundle … --expected … --json
count exit=2 rows: 0
```

Eleven rows name one of the four edited tools. All eleven were replayed through
`python3 tools/registry-check.py --root . --only <row>` in a clone at each
revision (cwd = clone, `TMPDIR` usable). `got` is identical at base, C0 and tip:

| row | expect | got base | got C0 | got tip |
|---|---|---|---|---|
| bash-witness-count | 0 | 0 held | 0 held | 0 held |
| bash-witness-selftest | 0 | 0 held | 0 held | 0 held |
| pin-disposition-read | 0 | 0 held | 0 held | 0 held |
| pin-disposition-selftest | 0 | 0 held | 0 held | 0 held |
| evidence-disposition-round17 (superseded) | 0 | 2 | 2 | 2 |
| evidence-disposition-round17-before (superseded) | 1 | 2 | 2 | 2 |
| evidence-disposition-round18 | 0 | 0 held | 0 held | 0 held |
| evidence-disposition-round18-before | 1 | 1 held | 1 held | 1 held |
| evidence-disposition-round14-superseded (superseded) | 0 | 2 | 2 | 2 |
| evidence-disposition-selftest | 0 | 0 held | 0 held | 0 held |
| env-diff-selftest | 0 | 0 held | 0 held | 0 held |

The three `got ≠ expect` rows are **superseded** rows and already differed at
base; the live one is documented in SKILL as "round 17's now exits 2". **No row
sees a different exit code or a different message because of C0.** Not a defect.
The registry schema has no stderr needle (`expect` = `exit` + `stdout_contains`
only), so no row could depend on the old traceback text even in principle.

The seven `scratch_root` cells added at C0 sit in rows `repeat-control-selftest`,
`bash-witness-selftest`, `pin-disposition-selftest`,
`evidence-disposition-selftest`, `context-capture-selftest`,
`registry-check-selftest`, `env-diff-selftest` (`tools/registry.json` lines
44, 87, 135, 333, 424, 620, 862). They are prose, not executable expectations;
`registry-check` runs those rows under the **caller's** `TMPDIR`, so with a
healthy root all seven pass whether or not the class holds.

## 3. Sentences that name the class — verdicts

Quotes are byte-exact from the C0 blob (`git show 59c3810:…`).

### 3.1 D1 — `SKILL.md:32-39`, standing rules (DEFECT at C0, fixed at tip)

```
- **The scratch root has three arms.** A tool that allocates scratch through
  `strict_scratch_root()` honours `TMPDIR`: unset → the platform default; empty
  (`TMPDIR=""`) → unset, because the resolver skips an empty candidate
  (S278:163-165) and falls through the documented list (S279); set but unusable →
  exit 2, could-not-evaluate, naming the value — never a silent `/tmp` fallback,
  never a traceback, never exit 1 (corpus/knowledge/scratch-root-contract.md; the
  seven tools and their registry `scratch_root` cells, measured by the round-54 C2
  counter).
```

The subject is *the tool*, not the self-test path. At C0 `tools/env-diff.py:80`
(`with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir=strict_scratch_root()) as tmp:`)
is reached from the `--contract` run path; the run path's only setup catch is
`tools/env-diff.py:263` (`    except (OSError, ValueError, KeyError, TypeError) as exc:`),
which does not include the new `RuntimeError` subclass, so the class escaped as a
traceback with rc 1. Receipt: `T54W1Revenge01-receipts/envdiff-runpath.txt`
(fixture repo + contract with the **correct** pin, so the run really reaches
`execute()`):

```
# env-diff --contract RUN path (non-selftest), valid fixture pin, TMPDIR=/nonexistent/round54-probe
[base] rc=1 traceback=1 out_written=no stderr_lines=37
   last_two_stderr: …|RuntimeError: cannot create clone scratch … (could-not-evaluate)|
[c0]   rc=1 traceback=1 out_written=no stderr_lines=37
   last_two_stderr: …|ScratchRootUnusable: cannot create clone scratch … (could-not-evaluate)|
```

So at C0 the bullet's "never a traceback, never exit 1" was false **and** the
traceback's final token changed (`RuntimeError:` → `ScratchRootUnusable:`), the
only message change C0 produced on a non-self-test path. **Defect, fixed at tip**
(`99c3bc8` adds `    except ScratchRootUnusable as exc:` before line 263; the
probe at tip returns `rc=2 traceback=0 stderr_lines=1`, same receipt file).

### 3.2 `SKILL.md:2001`, the env-diff entry row (stale at base and C0, true at tip)

Cell fragment: `0 all surfaces classified; 1 incomplete/failed measurement; 2 could-not-evaluate; 64 usage`.
With an unusable `TMPDIR` the run path returned **1** (rc 1, §3.1) — the cell's
"2 could-not-evaluate" did not describe that arm at base either, so this is not a
C0 regression; it is the cell the new bullet leaned on, and it is true at tip.
Not reported as a C0 defect.

### 3.3 `SKILL.md:2168`, the bash-witness-study row (not a defect)

Cell fragment: `2 could-not-evaluate (missing input, pin mismatch, runner SETUP)`.
At C0 `bash-witness-study.py` maps the class on **every** mode (the wrap is on
the dispatch, `tools/bash-witness-study.py:1788` inside C0), so the arm list is
now incomplete — the class is right (2) and the exit code is unchanged. This is
exactly what R53.6 asked for ("make the mapping uniform or narrow the claim's
parenthetical"); the remap was chosen and the parenthetical was not widened.
Nit, not a defect: it cannot mislead a caller into a wrong exit code.

### 3.4 D2 — `corpus/knowledge/scratch-root-contract.md:15` and `:42-44` (DEFECT at C0, fixed at tip)

```
| unusable | a path that is not a writable directory | the tool refuses before it allocates: the value is named, the class is printed, nothing falls back to `/tmp` | **2, could-not-evaluate** |
```

```
subclass raised by the helper and caught at the entry point, printing one line
that names the value and the class.

```

"caught at the entry point" was true of three of the four at C0 and of env-diff
only in its `--selftest` branch. The note's own blind-spot sentence (`:51-53`,
"it sees the self-test path, not every branch a tool might use to allocate
scratch") excuses **the counter**, not the per-arm table row, which states the
tool's behaviour. Same probe as §3.1. Fixed by the tip commit's run-path catch.

### 3.5 `corpus/lessons/round-54.md` R53.6 entry (same over-claim at C0, true at tip)

```

```

At C0 the mapping was not universal (env-diff run path); the sentence is true at
tip. Covered by D2 rather than counted separately.

### 3.6 `corpus/lessons/round-53-verifier-spotcheck.md:83` (NOT a defect — historical record)

> `6. **R53.6 — CR47 exit-class mapping incomplete in 4 of 7 tools.** bash-witness-study, env-diff, evidence-disposition, pin-disposition raise an uncaught RuntimeError (rc=1) on set-but-unusable TMPDIR instead of the declared could-not-evaluate exit 2`

This is the round-53 spot-check's record of the round-53 tip, where it was true
(reproduced at base, §1). The lane's own precedent is that such lines stay: the
round-54 lesson's R53.8 entry says "The round-53 lesson's own line is left as the
historical record (errata are append-only)", and R53.6 is marked FIXED in the
round-54 lesson. Leaving it is consistent; it is not a defect, and no gate reads
it.

**N1 (nit, still open at tip).** The same sentence ends:
`Nit: `tools/context-capture.py:27` docstring still mentions the old gettempdir() path.`
At tip, `tools/context-capture.py:27` still reads
`      / the scratch root (tempfile.mkdtemp(dir=tempfile.gettempdir())), pinning literal expected ids and`
while the code below it (`:300` `strict_scratch_root()`) refuses an unusable
`TMPDIR`. `tools/context-capture.py` is outside C0's edit set, so this is the
round-53 nit surviving, not a C0 dependency: no exit code changes, only a
docstring that mis-describes the root.

## 4. Helpers, consumers, and re-executed gates

Receipts: `consumer-sweep.txt`, `r53-counter-rerun.txt`, `waiver-dependency.txt`.

1. **Exception type is a subclass.** `ScratchRootUnusable(RuntimeError)` keeps
   every `except RuntimeError` working. The only `except RuntimeError` sites in
   the tool tree are `tools/registry-check.py:1847` and `:1928`, both wrapping
   registry-check's own failures (registry-check was not edited; its helper still
   raises plain `RuntimeError`). The four edited tools contain no
   `except RuntimeError` at all. No dependency.
2. **Message-token consumers.** `grep -rn "RuntimeError:"` over `tools/`,
   `.ufo/evidence/round-52..54`, `round-53/c2`, `round-53/control` and the new
   contract note returns **no match** — nothing parses the token that changed on
   the env-diff run path. `grep -rn "Traceback"` finds only *absences-asserted*
   checks (`tools/witness-metadata.py:1169`, `tools/context-capture.py:1723`,
   `:1766`, and the new `.ufo/evidence/round-54/c2/measure.py:114`), all of which
   C0 satisfies better than base. No dependency.
3. **`tools/witness-metadata.py` names `tools/bash-witness-study.py` but does not
   hash it live**: `"checked_live": False` and the note "the gate does not
   live-hash tools/bash-witness-study.py" (`:120-176`). C0's edit to that file is
   invisible to it. No dependency.
4. **`tools/context-capture.py:146 PROBE_REL = "tools/pin-disposition.py"`** —
   its `--check` mode recomputes digests from the frozen receipt/expected payload
   and explicitly "does not read live lane inputs" (`:11-29`), so editing
   pin-disposition cannot move it. Confirmed by replay: rows
   `context-capture-missing-env` / `context-capture-mapping-suffix` give got=1
   (held) at base, C0 and tip.
5. **`tools/evidence-disposition.py` waiver — the one real coupling (pre-existing,
   not caused by the class).** `tools/pin-disposition.py` and
   `tools/bash-witness-study.py` are declared `historical_inputs` (rev
   `4acc607dfd79f19d508bd50cdd06b77269fccd1d`) in
   `.ufo/evidence/round-18/dispositions.json`; the gate compares **live worktree
   bytes** with the tip blob. Control on a C0 clone:

   ```
   dirty:  M tools/pin-disposition.py
   ROW evidence-disposition-round18-before expect=1 got=2 differs
   primary exit: 2
   status: could_not_evaluate | exit: 2 | error: {"kind": "historical_input_uncommitted", "message": "tools/pin-disposition.py: live bytes differ from HEAD:tools/pin-disposition.py"}
   restored_clean=0
   ```

   So **an uncommitted edit to either waived tool flips a registered gate row
   from 1 to 2**. C0 committed its edits (rows hold at base/C0/tip), and the tip
   commit edited only `tools/env-diff.py`, which is not waived. Answer to the
   item's question in one line: *the only thing that changes an exit code here is
   leaving the tool edit uncommitted, and nothing in the lane relies on the old
   rc 1.*
6. **Frozen round-53 C2 counter re-run** (it extracts `tools/env-diff.py` at the
   revision and runs `--selftest`, and its CR47 arm requires a nonzero
   scratch-refusal exit and the `cannot create (clone )?scratch` text):

   ```
   C2_R53: rev=d33053f7552d … envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=2 docs=ok total=0 C2_R53_PASS=true
   C2_R53: rev=59c38109bf11 … envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=2 docs=ok total=0 C2_R53_PASS=true
   ```

   Identical verdicts; the counter accepts rc 2 and its docs patterns
   (`/tmp/tameshi-f5.json`, `/tmp/tameshi-r21-envdiff`,
   `mkdir -p /tmp/<lane>-r<round>`, ``Scratch for a sweep: `/tmp/``) do not fire
   on the new SKILL bullet. No dependency.
7. **Write-path census** (`tools/write-path-census.py --census`, 21 gate tools
   including all four): `gates=21/21 live_write_sites=99 live_unflagged=0
   missing=0` at base and at C0 — identical counts; only the per-gate `sha256`
   line of an edited tool moves. The three added lines per tool are a class, a
   `raise` and stderr writes, none of which `WRITE_RE` matches. No dependency.
8. **Sources census** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
   validate --root /home/vgpnk/Projects/shokunin tameshi` → `tameshi ok
   …/corpus/SOURCES.md`, exit 0 (run at seat start and at seat end).

## 5. Defects, with the sentence to change (report-only, nothing edited)

| id | severity | where | finding | fix at tip? |
|---|---|---|---|---|
| D1 | medium | `SKILL.md:32-39` (`never a traceback, never exit 1`) | the new universal claim was falsified by `tools/env-diff.py:80` + `:263` at C0; an env-diff `--contract` run with an unusable `TMPDIR` tracebacked rc 1 | yes (`99c3bc8`) |
| D2 | medium | `corpus/knowledge/scratch-root-contract.md:15`, `:42-44`; `corpus/lessons/round-54.md` R53.6 | "caught at the entry point" / "the tool refuses … 2" over-claimed for env-diff's run path at C0 | yes, same commit (text itself unchanged and now accurate) |
| N1 | nit | `tools/context-capture.py:27` | docstring still says `tempfile.mkdtemp(dir=tempfile.gettempdir())` while `:300` enforces three arms; the round-53 spot-check's own nit, unfixed | **no** |

Not defects, with reasons: `SKILL.md:2001` (stale at base too, true at tip);
`SKILL.md:2168` (class correct, arm list incomplete); `round-53-verifier-spotcheck.md:83`
(historical record, errata are append-only); all 11 rows (identical got at three
revisions); the frozen round-53 counter, the write-path census and the sources
census (identical verdicts).

## 6. Risk note (no action requested)

No registry row pins exit 2, so `registry-check` cannot observe a regression of
this class: it runs rows under the caller's `TMPDIR`, and with a healthy root the
four self-test rows pass whether the class is 2 or 1. The class is pinned only by
the round-54 C2 counter. That matches the frozen contract (the claim is carried
by the `scratch_root` cells plus the counter), so it is stated, not filed.

## Receipts

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1Revenge01-receipts/`

- `selftest-exit-flip.txt` — base vs C0 `/ --selftest` under unusable and usable `TMPDIR`
- `envdiff-runpath.txt` — env-diff `--contract` run path, base vs C0 (`RuntimeError:` → `ScratchRootUnusable:`)
- `row-ledger.txt` — 11 rows replayed at base and C0 through `registry-check --only`, plus the exit-1/exit-2 row list
- `consumer-sweep.txt` — `RuntimeError:`/`Traceback` greps, write-path census base vs C0, sources census
- `r53-counter-rerun.txt` — frozen `.ufo/evidence/round-53/c2/measure.py` at base and C0
- `waiver-dependency.txt` — dirty waived input → `historical_input_uncommitted`, exit 2, then restore

Fixtures: `git clone --shared` copies at `$HYAKU_SCRATCH/tameshi-r54/T54W1Revenge01/{base,c0,tip}`,
fixture repo `…/fixture` (`git init` + one commit), contracts `…/contract2.json`.
All git calls named `-C <dir>` with the toplevel asserted; no mutating command in
the lane, no commit/push/fetch/reset/add anywhere except the fixture clone's own
`checkout`/`git init`/`commit`. No tool installed (nothing was needed; the paused
pacman channel was not touched). Scratch tree removed on exit.
