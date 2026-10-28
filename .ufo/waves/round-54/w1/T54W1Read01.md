# T54W1Read01 — cold read of `## Standing rules` at C0

Seat T54W1Read01, tameshi round 54, wave w1. Reader item: no lane file, counter, contract, freeze, ledger or wave spec was edited; every lane read was of git objects at C0.

- heading: `## Standing rules`
- cand (C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- section_sha256: `164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7`
- span: `reader-section.py` prints start 17, end 40. The section body is SKILL.md lines 17-39 at C0 (the next heading `## Source notes` sits at line 41). Recomputed independently over `git show C0:SKILL.md`: lines 17-39 joined with `\n`, no trailing newline = 1943 bytes, sha256 `164390276b45…43f7`, equal to the reader's sha.
- sha-producing command (scratch `TMPDIR` set to the seat tree):

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && \
python3 .ufo/waves/round-54/reader-section.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  59c38109bf119d0e9d4f878644a82babc937bc1e "## Standing rules"
```

All section reads below are of `git show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md`, never of the working tree.

## Findings (1)

### F1 — the unusable-`TMPDIR` exit class is stated tool-wide; a documented env-diff path prints a traceback and exits 1

Byte-exact quote (SKILL.md:35-37 at C0):

```
set but unusable →
  exit 2, could-not-evaluate, naming the value — never a silent `/tmp` fallback,
  never a traceback, never exit 1
```

Why: the bullet's subject is "A tool that allocates scratch through `strict_scratch_root()`" and the unusable arm is stated unconditionally ("never a traceback, never exit 1"), but at C0 one of the seven such tools, `tools/env-diff.py`, reaches `strict_scratch_root()` from its own documented `--contract/--out` mode outside the `--selftest` try/except and dies with an uncaught `ScratchRootUnusable` traceback and exit 1; the note the bullet cites limits the measured class to the self-test path.

Evidence, three independent legs:

1. The cited note states the scope limit. `corpus/knowledge/scratch-root-contract.md:51-53` (at C0): "The counter's blind spot is stated in the contract: it sees the self-test path, not every branch a tool might use to allocate scratch." The round-54 contract's C2 `cannot_see` repeats it: "whether a tool's self-test exercises the branch that allocates scratch on its real path".
2. The code: `tools/env-diff.py` at C0 catches `ScratchRootUnusable` only in the `--selftest` branch (`main`, line 234-236); the normal run path wraps the run in `except (OSError, ValueError, KeyError, TypeError)` only (line 263-265), and `execute()` calls `tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir=strict_scratch_root())` (line 80).
3. The run (receipt, exit code read):

```
$ S=/fast/scratch/hyaku/tameshi-r54/T54W1Read01
$ git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/probe/lane-c0"
$ git -C "$S/probe/lane-c0" checkout -q 59c38109bf119d0e9d4f878644a82babc937bc1e
$ git -C "$S/probe/lane-c0" rev-parse HEAD
59c38109bf119d0e9d4f878644a82babc937bc1e
$ cd "$S/probe/lane-c0"
$ TMPDIR=/nonexistent-t54-xyz python3 tools/env-diff.py \
    --contract "$S/probe/arms/envdiff-contract.json" \
    --out "$S/probe/arms/envdiff-out.json" --fleet-root "$S/probe"
rc=1  traceback_lines=1  stdout_bytes=0
```

stderr (full stream: `T54W1Read01-receipts/nonself-envdiff.err`), last three lines:

```
    raise ScratchRootUnusable(
        "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
ScratchRootUnusable: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-t54-xyz' (could-not-evaluate)
```

stdout is empty: no `could-not-evaluate` verdict line, and the exit class is 1, not 2.

Verdict: at C0 the quoted sentence is false for one of the seven tools on a documented invocation; the rule needs the self-test-path scope (or env-diff needs the entry-point mapping it has only for `--selftest`).

The finding is scoped, not a blanket failure: the same tool's self-test path and the other six tools' self-tests do conform (see "Checks that held"), and `registry-check`'s non-selftest `--rev` path also conforms (rc 2, one naming line).

## What I opened (all at C0 unless stated)

1. `SKILL.md` at C0, lines 17-39 — the section itself; byte and sha recomputation above.
2. `corpus/SOURCES.md` rows S277, S278, S279 (lines 152-154) — S277 POSIX.1-2024 TMPDIR, S278 CPython 3.12.7 `Lib/tempfile.py` `_candidate_tempdir_list :163-165`, S279 Python docs `tempfile` search order; each is `tier A`, `mined`, `opened 2026-10-28`, `used-by corpus/knowledge/scratch-root-contract.md`; the round-54 changelog line 514 says the three rows were added this round. All three resolve.
3. `.ufo/evidence/round-54/assimilation/S278-tempfile.py` lines 156-165 — line 163 `for envname in 'TMPDIR', 'TEMP', 'TMP':`, 164 `dirname = _os.getenv(envname)`, 165 `if dirname: dirlist.append(dirname)`. The cited range `S278:163-165` resolves byte-for-byte and supports "an empty candidate is skipped".
4. `corpus/knowledge/scratch-root-contract.md` (60 lines) — three-arm table at :11-15, empty-arm justification at :17-30, the uniform-class section at :32-43, the counter scope at :45-53, falsifier at :55-60. The blind-spot sentence at :51-53 is the scope limit the bullet does not repeat.
5. `tools/registry.json` at C0 — 56 rows, exactly 7 carry a `scratch_root` cell: `repeat-control-selftest`, `bash-witness-study-selftest`, `pin-disposition-selftest`, `evidence-disposition-selftest`, `context-capture-selftest`, `registry-check-selftest`, `env-diff-selftest`. The "seven tools and their registry `scratch_root` cells" clause resolves (7 cells, 7 tools).
6. The seven `strict_scratch_root()` definitions at C0 — `tools/{registry-check,env-diff,bash-witness-study,evidence-disposition,pin-disposition,context-capture,repeat-control}.py`; all seven bodies are the same three-arm shape (`t = os.environ.get("TMPDIR")`; falsy → `tempfile.gettempdir()`; set but not a writable dir → raise with the value and `(could-not-evaluate)`; else return `t`). Four of the seven raise the `ScratchRootUnusable` subclass (`env-diff`, `bash-witness-study`, `evidence-disposition`, `pin-disposition`); the other three still raise bare `RuntimeError` but their entry points map it to exit 2.
7. `.ufo/evidence/round-54/c2/measure.py` — exists at C0; its `TOOLS` list is the same seven; arms 1-5 match the note. `.ufo/evidence/round-54/contract.json` — C2 target is self-test-scoped (`7/7 self-tests exit 2 …`), and its `cannot_see` names the real-path gap.
8. `PROVINCE.md` at C0 (118 lines) — exists at the lane root; `grep -i 'write|surface'` finds no write-surface declaration (only "read-only … surfaces"), so the first rule's exception clause is vacuous, not contradicted.
9. `corpus/knowledge/mutation-case-kimi-census.md:4-7` and `corpus/knowledge/mutation-case-kagi-census.md:4-6` — both say every mutant is a copy under `/tmp/tameshi-r2-1-work/` and `/tmp/tameshi-r3-1-work/`; the "in the original `/tmp` namespace" parenthetical resolves.
10. `## Errata — round 16 full-page cold-read` at SKILL.md:1733-1779 — the block says "The page edits are in-place repairs, and so are this table's own cells: a later row's corrections of an earlier row stay visible in git … not as appended rows", so the errata bullet's "the block says so" resolves and the append-only rule is reconciled with the in-place repairs it names.
11. Round-53 lineage for the bracketed note: `w1/T53W1Read07.json` (3 findings on this heading), `w2/T53W2Read04.json` (1), `w2r/T53W2R4.json` (the "last committed occurrences are rounds 25-36" finding) and `w2r3-results.json`; `SKILL.md` at C5 `651773a` carried the "rounds 25-36" clause and C6 `7c10fa7` replaced it. The bracket "round 53 correction of the round-53 'rounds 25-36' overstatement, seat T53W2R4" resolves.
12. `.ufo/evidence/round-18/measure.py` `sectionize()` and `.ufo/evidence/round-54/c1/measure.py` arms 3-4 (heading / cand / section_sha256 binding) — to confirm the deliverable's three binding fields are the ones the counter reads.

## Checks that held

- Nine claims in the section were checked against their artifacts; the unusable arm's tool-wide exit class is the only one that fails.
- Seven callers: `git ls-tree` + grep at C0 finds `strict_scratch_root` in exactly 7 tool files (`tools/registry-check.py`, `env-diff.py`, `bash-witness-study.py`, `evidence-disposition.py`, `pin-disposition.py`, `context-capture.py`, `repeat-control.py`), matching "the seven tools".
- Unusable arm, self-test path: 7/7 exit 2, one `could-not-evaluate` line naming `/nonexistent-t54-xyz`, zero `Traceback` lines (`selftest-arms.txt` lines under "arm 1").
- Empty arm (`TMPDIR=""`): 7/7 exit 0, zero `could-not-evaluate` lines, zero tracebacks (`selftest-arms.txt` lines under "arm 2") — the "empty → unset" arm holds.
- Registry cells: 7 rows carry `scratch_root`, and every cell names TMPDIR, the empty-string arm and the could-not-evaluate class (`tools/registry.json`).
- Scratch-form counts in the namespace bullet: per round `r` in 48..52, `git grep -c -E "tameshi-r$r/" C0 -- ".ufo/waves/round-$r/**"` summed gives 294/533/1737/1957/158 (thousands of the slash form); `git grep -n -E '(/tmp|/var/tmp)/tameshi-r(4[89]|5[0-2])-' C0 -- '.ufo/**'` returns nothing, and the 16 dash-form strings in those rounds are schema/tool names (`tameshi-r49-reads-v1`, `tameshi-r51-c1-selftest-`), i.e. quoted text, not seat trees. "0 dash-form seat trees across rounds 48-52" resolves.
- `S278:163-165` and `S279` resolve as cited; `corpus/knowledge/scratch-root-contract.md` and the seven registry cells exist at C0; the round-54 C2 counter blob exists at C0.

## Receipts (under `T54W1Read01-receipts/`)

- `probe-arms.sh` — rerunnable driver: clone `--shared` the lane, assert HEAD = C0, run both self-test arms for the seven tools and both non-self-test paths.
- `selftest-arms.txt` — the driver's log: 7×`unusable-* rc=2 traceback_lines=0 could_not_evaluate_lines=1`; 7×`empty-* rc=0`; `registry-check --rev rc=2`; `env-diff --contract rc=1 traceback_lines=1`.
- `unusable-*.err` (7 files) — the one naming line each tool prints on the unusable arm (`unusable-context-capture.err` is empty because that tool prints the line on stdout).
- `nonself-envdiff.err` (2572 B), `nonself-envdiff.out` (0 B) — the finding's traceback and empty stdout.
- `nonself-registry-check.out` — the conforming non-selftest path (`REGISTRY_CHECK: could-not-evaluate (… '/nonexistent-t54-xyz' …)`), the contrast case.
- `envdiff-contract.json` — the fixture contract used (surface `lane-envdiff`, rev C0, path `tools/env-diff.py`, `blob_sha256` `ab193692…fe56` = sha256 of `git show C0:tools/env-diff.py`; `repo` is the clone's directory name, `--fleet-root` its parent).

## Limits

- The receipt needs `bwrap` on the host (observed `bubblewrap 0.13.1`, `/usr/bin/bwrap`); without it `execute()` returns `EXEC_UNAVAILABLE` before allocating scratch, so the traceback is host-dependent.
- I did not run the C2 counter end to end (its own seat owns it); the three arms were measured directly, per tool, at C0.
- Scratch tree `/fast/scratch/hyaku/tameshi-r54/T54W1Read01` was removed on exit; the clone lived there, so the receipt names how to rebuild it.
- No tool was installed or upgraded; no mutating git command was run against the lane or any repo (only `git clone --shared` into scratch and a detached `checkout` inside that clone, HEAD asserted).
