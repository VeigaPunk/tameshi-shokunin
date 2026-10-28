# T55W2SentScope2 — scope audit of C0

**Item:** audit the C0 diff `0a2010acd1e92e4e332774050825e21bcfc7e079..9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`:
every changed path, frozen/sibling/`.ufo/state`/out-of-lane containment, `tools/registry.json`'s semantic diff,
the three tools' diff surface, the worktree for stray writes, and whether anything under
`.ufo/waves/round-55/` moved after the wave-1 dispatch marker.

**Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (HEAD at audit time `133b2ce6d4d86d783db38607343c3654350194b8`,
freeze amendment 8; the audited commit is C0 = `9cf0146`).
**Scratch:** `/fast/scratch/hyaku/tameshi-r55/T55W2SentScope2` (all probes; lane never mutated — every git call read-only).
**Receipts:** `T55W2SentScope2-receipts/` — reproducible by one command:

```
bash .ufo/waves/round-55/w2/T55W2SentScope2-receipts/receipts.sh
```

Axes: (A) path-list completeness, (B) frozen/out-of-scope containment, (C) registry semantic-diff precision,
(D) tool-diff minimality, (E) stray-write / post-marker evidence.

---

## Verdict summary

| question | verdict |
|---|---|
| every changed path listed and inside the lane | **PASS** — 1285 paths, 0 outside the lane, 0 gitlinks, 0 symlinks, 0 `..`/absolute |
| any frozen file changed | **PASS** — freeze..C0 ∩ `contract.frozen_paths` = ∅; the 8 frozen paths appear in base..C0 only as `A` (added by the freeze commit `e2979f2`), and none is dirty in the worktree |
| sibling repo / `.ufo/state/` / `.ufo/watchdog.log` touched | **PASS** — none |
| `registry.json` semantic diff is only the seven cells | **PASS** (7 value diffs, 56→56 rows, key order identical) — **but the file was re-serialized end-to-end** (indent 2→1): 1275+/1026- lines for 7 cells. Finding **F2** |
| the three tools' diffs touch only the scratch refusal (+ the `--rev` handler) | **PASS** — 4/3/4 hunks, all in `ScratchRootUnusable` / `strict_scratch_root` / one refusal handler / `--rev` handler; proof below |
| worktree free of stray writes | **FAIL (outside scope-owner)** — 196 paths dirty at 17:27Z: 148 `??`, 38 `M`, 10 `D`, all under `.ufo/`; production surfaces and frozen files clean, but the round's base receipt is **truncated** (F3) and the frozen evidence dir gained untracked files (F4) |
| nothing under `.ufo/waves/round-55/` edited after the wave-1 dispatch marker | **spec/marker bytes: PASS**; **literal invariant: FAIL** — 368 files under `w1/` are newer than the marker. C0 was cut while wave-1 seats were still writing (F5) |
| census `validate` | **PASS** — exit 0, 140 rows |

---

## A. Every changed path

```
$ git -C LANE diff --name-only 0a2010ac..9cf0146 | wc -l        -> 1285
$ git -C LANE diff --name-only e2979f27..9cf0146 | wc -l        -> 1273   (what C0 itself landed)
$ ... | grep -c '^\.ufo/waves/round-55/w1/'                      -> 1254
```

Full listing: `T55W2SentScope2-receipts/01b-changed-paths-full.txt` (name-status, 1289 lines incl. 4 summary lines).

The 19 paths C0 touched outside `w1/` (`receipts/01-path-inventory.txt`):

```
M  .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md     A  .ufo/waves/round-55/w1.ready
A  .ufo/waves/round-55/build-spec-w1.py               A  .ufo/waves/round-55/w1.ready.dispatched
A  .ufo/waves/round-55/spec-w1.json                   M  LOG.md
A  .ufo/waves/round-55/w1-dispatch.json               M  SCORECARD.md
A  .ufo/waves/round-55/w1-run.err                     M  SKILL.md
M  corpus/QUALITY.md                                  M  corpus/knowledge/scratch-root-contract.md
M  corpus/SOURCES.md                                  M  corpus/lessons/round-54.md
A  corpus/lessons/round-55.md                         M  tools/context-capture.py
M  tools/registry-check.py                            M  tools/registry.json
M  tools/repeat-control.py
```

Containment sweeps (`01-path-inventory.txt`):

```
$ git -C LANE ls-tree -r 9cf0146 | awk '$1=="160000"||$1=="120000"'   -> (nothing)
$ git -C LANE diff --name-only 0a2010ac..9cf0146 | grep -E '^/|(^|/)\.\./'  -> (nothing)
$ ... sibling-lane segments ∩ {shokuknow,kagi,mado,kama,kumitate,tsukuroi,souji,merge} -> NONE
```

Top-level buckets are `.ufo`, `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus`, `tools` — nothing else.
The only non-ASCII-awkward entry is mode `100755` on 20 newly added scripts under
`.ufo/waves/round-55/**` and `.ufo/evidence/round-55/{c1/measure.py,c2/measure.py,controls.sh,deciding-run.sh,no-harm.sh}`
— mode changes on *new* files, no permission mutation of an existing file.

**One out-of-round path:** `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` (prior-round wave report) receives an
appended `**SUPERSEDED (round 55, ER-R54-8).**` block. It is additive (327 unchanged, +13 lines, original text kept),
it is not a frozen path, and it withdraws a round-54 claim the round-55 ledger re-keys. Noted as intentional, not a
containment breach — but it is a round-54 artifact modified by a round-55 commit, so the round-54 wave directory is no
longer byte-stable across rounds.

---

## B. Frozen files

```
$ git -C LANE diff --name-only e2979f27..9cf0146  ∩  contract.frozen_paths        -> NONE
$ git -C LANE diff --name-only e2979f27..9cf0146  ∩  freeze.json files{}          -> NONE
$ git -C LANE status --porcelain -- <the 8 frozen paths>                          -> (empty)
```

In `base..C0` all 8 frozen paths appear, each with status **`A`** — they did not exist at `0a2010ac` and were added by
the freeze commit `e2979f2`; C0 does not touch them:

```
A .ufo/evidence/round-55/contract.json      A .ufo/evidence/round-55/c2/measure.py
A .ufo/evidence/round-55/freeze.json        A .ufo/evidence/round-55/no-harm.sh
A .ufo/evidence/round-55/c1/measure.py      A .ufo/evidence/round-55/deciding-run.sh
A .ufo/evidence/round-55/c1/staged-at-freeze.txt   A .ufo/evidence/round-55/controls.sh
```

Manifest self-consistency at C0: `freeze.json` has 7 entries, all in `contract.frozen_paths`, and its `note` declares
the exclusion of `freeze.json` itself. So the audited commit is frozen-clean. (`HEAD` `133b2ce` = amendment 8 *does*
modify `c2/measure.py`, `contract.json` and `freeze.json` — that is the recorded amendment, outside this audit's rev.)

---

## C. `tools/registry.json` — 7 cells, but a full re-serialization

Semantic diff of the parsed JSON (`receipts/03-registry-semantic.txt`):

```
rows: 56 -> 56   schema: tameshi-entry-registry-v1 -> tameshi-entry-registry-v1
rows carrying scratch_root: 7 -> 7
semantic diffs: 7
  VAL /rows[2]/scratch_root    repeat-control-selftest
  VAL /rows[4]/scratch_root    bash-witness-selftest
  VAL /rows[6]/scratch_root    pin-disposition-selftest
  VAL /rows[14]/scratch_root   evidence-disposition-selftest
  VAL /rows[18]/scratch_root   context-capture-selftest
  VAL /rows[27]/scratch_root   registry-check-selftest
  VAL /rows[40]/scratch_root   env-diff-selftest
```

No `KEYS`/`KEY-ORDER`/`LEN`/`TYPE` diff anywhere in 113 dicts: every row keeps its keys, its key order and its
values. Names remain unique, 56 rows.

**But the file was rewritten wholesale:**

```
$ git -C LANE diff --numstat e2979f27..9cf0146 -- tools/registry.json
1275    1026    tools/registry.json
freeze: 28902 bytes, 1028 newlines, first indent 2
C0    : 27999 bytes, 1277 newlines, first indent 1
C0 bytes == json.dumps(freeze_object_with_7_cells_patched, indent=1) + "\n"  -> True
```

The last line is the proof that the churn is *purely* formatting: the C0 file is bit-exactly the freeze object with the
seven cells patched, re-dumped at `indent=1`. Nothing else moved. (`indent=1` is a lane convention — `spec-w1.json`
is `indent=1` too — so this is defensible style, not corruption.)

**Finding F2 (low, scope/noise):** a 2301-line textual diff for a seven-cell change. Any future `git log -p` or
byte-level review of `registry.json` sees a rewrite where seven strings changed; no lane tool hashes these bytes
(`c2/measure.py:244` loads it with `json.loads`), so nothing breaks — it just makes the commit unreadable at the line
level and defeats the "diff shows exactly what changed" property for this one file. Cause: `json.dump(..., indent=1)`
instead of a targeted in-place edit.

---

## D. The three tools: diff surface and the refusal's reachability

`receipts/04-tool-diff-surface.txt`.

| tool | numstat | hunks | functions |
|---|---|---|---|
| `repeat-control.py` | 21+/1- | 4 | `class ScratchRootUnusable`, `raise` swap in `strict_scratch_root`, new `could_not_evaluate()`, `except` in `main` |
| `context-capture.py` | 10+/1- | 3 | class, `raise` swap, `except` in `run_selftest` |
| `registry-check.py` | 13+/1- | 4 | class, `raise` swap, `except` in `main` (selftest branch), `except` in `main` (`--rev` branch) |

No other line of any of the three tools changes — no altered grammar text, no changed exit constants, no touched
`classify`/`emit`/`snapshot`/clone logic.

**Reachability of every scratch call site** (AST map in the receipt):

- `repeat-control.py` — call `@629` in `selftest()`; that line sits *before* `selftest`'s own `try` (its
  `except Exception` is at 893), so the new exception escapes to `main`'s handler at 925. Confirmed dynamically.
- `context-capture.py` — call `@1643` in `SelftestHarness.__init__`; its only construction site is `@2214`, *inside*
  `run_selftest`'s `try` whose `except ScratchRootUnusable` is at 2217. Covered.
- `registry-check.py` — calls `@784` (`clone_lane_at_rev`, reached only from the `--rev` call at 1934, handler 1935) and
  `@935` (`selftest`, handler 1851). `ScratchRootUnusable` subclasses `RuntimeError`, so the `except OSError` wrap at
  786 cannot swallow it. Covered.

**The `--rev` handler is load-bearing, not decoration.** The pre-existing fallback printed the verdict on *stdout*:

```
1938  except RuntimeError as exc:
1939      report = {...}
1941      if as_json: emit(json.dumps(report, indent=2, sort_keys=True))
1943      else:       emit(f"REGISTRY_CHECK: could-not-evaluate ({exc})")
```

which is exactly the base defect the contract's C2 `before` names. The new `except ScratchRootUnusable` ahead of it is
what moves the line to stderr.

**Dynamic probe** (clone at C0, `TMPDIR=/nonexistent-probe-<name>`, `receipts/05-refusal-probe.txt`):

```
repeat-control           rc=2 stderr_lines=1 RuntimeError=0 Traceback=0
context-capture          rc=2 stderr_lines=1 RuntimeError=0 Traceback=0
registry-check           rc=2 stderr_lines=1 RuntimeError=0 Traceback=0
bash-witness-study       rc=2 stderr_lines=1 RuntimeError=0 Traceback=0
pin-disposition          rc=2 stderr_lines=1 RuntimeError=0 Traceback=0
evidence-disposition     rc=2 stderr_lines=1 RuntimeError=0 Traceback=0
env-diff                 rc=2 stderr_lines=1 RuntimeError=0 Traceback=0
context-capture --check  rc=0 stderr_lines=0        (non-allocating mode stays lazy)
```

All seven match the grammar shape and exit class; `context-capture --check` does not allocate and does not refuse.

### Finding F1 (medium, calibration) — four of the seven registry cells quote a tool token no run emits

The cells quote the line in double quotes as if it were a transcript. Measured against the tree:

| row | documented token | emitted token | |
|---|---|---|---|
| `repeat-control-selftest` | `repeat-control.py` | `repeat-control` | **MISMATCH** |
| `bash-witness-selftest` | `bash-witness-study.py` | `WITNESS_STUDY` | **MISMATCH** |
| `pin-disposition-selftest` | `pin-disposition.py` | `pin-disposition.py` | ok |
| `evidence-disposition-selftest` | `evidence-disposition.py` | `evidence-disposition.py` | ok |
| `context-capture-selftest` | `context-capture.py` | `context-capture.py` | ok |
| `registry-check-selftest` | `registry-check.py` | `registry-check` | **MISMATCH** |
| `env-diff-selftest` | `env-diff.py` | `ENVDIFF_SETUP` | **MISMATCH** |

The counter cannot see this: the docs arm tests one substring only —

```
c2/measure.py:46  MARKER = "could-not-evaluate: cannot create clone scratch under the scratch root"
c2/measure.py:248 docs = sum(1 for row in cells if MARKER in row["scratch_root"])
```

— while the runtime arm's regex tolerates any token (`^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: ...`).
So `docs=7/7` passes with four cells whose literal prefix exists nowhere. `corpus/knowledge/scratch-root-contract.md`
(line 75) and `SKILL.md` (39-40) use the `<tool>:` placeholder and are therefore correct; only the registry cells
over-literalize. This is the record disagreeing with the tree on the exact surface C2 claims to have documented, and it
is precisely the blind spot the contract admits ("whether a caller parses the grammar by prefix or by the whole line"):
a caller that keys on the prefix gets four tools wrong.

Smallest remediation: change those four cells to the emitted token (or to the `<tool>:` placeholder the note uses),
and make the docs arm assert the token, not just the marker.

---

## E. Worktree: stray writes

Snapshot `2026-10-28T17:27:27Z`, HEAD `133b2ce` (`receipts/06-worktree-status.txt`):

```
$ git -C LANE status --porcelain | awk '{print $1}' | sort | uniq -c
    148 ??
     10 D
     38 M
```

All 196 paths are under `.ufo/`. Exactly four are outside `.ufo/waves/round-55/`:

```
  .ufo/evidence/round-55/before/c2.stdout        (M)
  .ufo/evidence/round-55/c1/lost-headings-at-c0.json   (??)
  .ufo/evidence/round-55/control/                (??)
  .ufo/evidence/round-55/integrate/              (??)
```

Clean and therefore *not* a defect: `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `SKILL.md`, `MANIFEST.json`,
`.ufo/state/`, `.ufo/watchdog.log`, and all eight frozen files. No write crossed into a sibling lane (the lane holds no
symlinks at C0, so no path in it can resolve outside).

### Finding F3 (medium, evidence integrity) — the base receipt cited by C2's `before` is truncated in the worktree

```
$ git -C LANE diff --stat -- .ufo/evidence/round-55/before/c2.stdout
 .ufo/evidence/round-55/before/c2.stdout | 16 ----------------
 1 file changed, 16 deletions(-)
```

The 16 deleted lines are the tail: the whole `EXPLAIN usable …` block, the three doc arms, and the verdict line
`C2_R55: rev=0a2010acd1e9 grammar=6/9 … total=21 C2_R55_PASS=false`. The worktree file now ends at
`EXPLAIN usable repeat-control --selftest rc=0 ok` — an evidence receipt with no verdict.

The committed blob is intact at both C0 and HEAD (`git show C0:…` and `HEAD:…` are byte-identical, verdict line
present), so the deciding run at a rev is unaffected; only a worktree-reading reviewer is misled. Still, the lane's
cited base receipt exists in two different states, and the worktree copy is the one a careless reader opens.
`receipts/09-base-receipt-drift.txt`.

### Finding F4 (low-medium, evidence-directory closure) — untracked writes inside `.ufo/evidence/round-55/`

```
.ufo/evidence/round-55/c1/lost-headings-at-c0.json
.ufo/evidence/round-55/control/controls-a.stdout
.ufo/evidence/round-55/integrate/binder.py
.ufo/evidence/round-55/integrate/resolutions.json
```

None is in `contract.frozen_paths`, so this is not a frozen-file edit — but the round's evidence directory is no longer
a closed, commit-recorded set: enumerating it yields files no revision contains, and `.ufo/evidence/round-55/control/`
sits beside the frozen `controls.sh` that is supposed to own that role. Severity is low because nothing reads these by
glob today (checked: the two counters open named paths only, `c1/measure.py:171`, `c2/measure.py:52`), but a future
`--rev`-independent recount that walks the directory would pick them up.

Also: 10 committed wave-1 receipts were deleted from the worktree
(`T55W1ExecGrammarBreak-receipts/{baseline,freeze-counter-9d0768,grammar-vs-token,…}` and
`T55W1ScribeNote-receipts/eight-allocating-modes.txt`). All blobs survive at C0; the deletions match the round's own
amendment 6 (8→9 allocating modes) and are not evidence loss at the revision level.

---

## F. Post-dispatch-marker edits

Marker, committed at C0 (`receipts/07-post-dispatch-writes.txt`):

```
$ git -C LANE show C0:.ufo/waves/round-55/w1.ready.dispatched | head -1
2026-10-28T14:16:09
```

**The dispatch artefact itself is immutable:**

```
file                                    C0==HEAD  C0==worktree   mtime
build-spec-w1.py                        yes       yes           13:39:49
spec-w1.json                            yes       yes           13:39:49
w1-dispatch.json                        yes       yes           13:40:22
w1.ready                                yes       yes           13:40:27
w1.ready.dispatched                     yes       yes           14:16:09
w1-run.err                              yes       yes           13:40:22
```

**The literal invariant fails, and cannot hold:**

```
files under .ufo/waves/round-55/ newer than 14:16:09 : 719
  w1/ 368      w2/ 338      w3/ 1
```

Wave-1 seats were still writing 8 minutes after the marker — that is what a dispatched wave does. What matters is the
consequence for C0: **C0 was cut mid-flight** (`14:16:39`, 30 s after dispatch), and 10 committed wave-1 report files
have been rewritten since:

```
M T55W1CritC1.{md,json}      M T55W1ScribeLog.md        M T55W1LabEmpty.json
M T55W1Er10.md               M T55W1ScribeNote.md       M T55W1ScribeCells.json
M T55W1ExecGrammarBreak.md   M T55W1ScribeNote-receipts/draft-section.md
M T55W1ScribeSkill.md
```

so the wave-1 record a reader gets at C0 is not the wave-1 state the seats finished at. Every one of these paths is
owned by a seat named in the wave-1 roster (`T55W1ScribeCells`, `T55W1ExecCensusAfter`, `T55W1CritGate`,
`T55W1ExecFooterPaths`, `T55W1SentConfig`, `T55W1CritSourcedClaim` all appear in `w1.ready.dispatched`), i.e. these
are wave-1 seats still running, not wave-2 seats writing outside their `w2/` scope.

I found no evidence of a wave-2 seat writing under `w1/`: every dirty `w1/` path belongs to a seat directory whose name
is in the wave-1 roster, and every wave-2 seat's receipts so far sit under `w2/`.

---

## G. Census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
CENSUS_EXIT=0
$ grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md
140
```

(`receipts/08-census.txt`.)

---

## Findings, with severity

| id | severity | finding | smallest remediation |
|---|---|---|---|
| **F1** | medium (calibration) | 4/7 `registry.json` cells quote a literal tool token (`repeat-control.py:`, `bash-witness-study.py:`, `registry-check.py:`, `env-diff.py:`) that no run emits; `docs` arm only matches the `could-not-evaluate:` marker, so `docs=7/7` passes anyway | replace the four tokens with the emitted ones, or with the note's `<tool>:` placeholder; assert the token in the docs arm |
| **F2** | low | `tools/registry.json` re-serialized end-to-end (`indent=1`) for a seven-cell change: 1275+/1026-, 1028→1277 lines. Semantically lossless (proved byte-exactly) | patch the seven strings in place next time; if a reformat is wanted, do it in its own commit |
| **F3** | medium (evidence) | `.ufo/evidence/round-55/before/c2.stdout` truncated in the worktree (−16 lines, verdict `C2_R55: … total=21` gone); committed blob intact at C0/HEAD | `git -C LANE checkout -- .ufo/evidence/round-55/before/c2.stdout` (owner: whoever rewrote it) |
| **F4** | low-medium | untracked writes in the frozen evidence dir: `c1/lost-headings-at-c0.json`, `control/controls-a.stdout`, `integrate/{binder.py,resolutions.json}` | move to `w2/<seat>-receipts/` or commit deliberately |
| **F5** | informational | C0 (`14:16:39`) was cut 30 s after the w1 marker (`14:16:09`); 10 wave-1 reports were rewritten afterwards, 368 `w1/` files are newer than the marker | read wave-1 claims from the seats' final files, not from C0's snapshot |
| **F6** | informational | `repeat-control.py`'s refusal also emits `REPEAT_CONTROL: setup_error` on **stdout**; `context-capture`/`registry-check` emit nothing on stdout | harmless under the frozen grammar (stderr-only), but the three tools are not uniform |

Not findings (checked, clean): no frozen-file edit by C0; no `.ufo/state/`, `.ufo/watchdog.log`, sibling-lane, absolute
or `..` path; no gitlink/symlink; no production file dirty in the worktree; `registry.json` rows/keys/order unchanged;
`--rev` refusal genuinely fixed (old fallback printed the verdict on stdout); every allocating mode exits 2 with exactly
one stderr line and no `RuntimeError`/`Traceback`; `context-capture --check` stays lazy.

## Artifacts opened

- `git` objects: `.ufo/evidence/round-55/{contract.json,freeze.json}` at C0; `tools/{registry.json,repeat-control.py,context-capture.py,registry-check.py}` at freeze and C0; `.ufo/waves/round-55/{w1.ready,w1.ready.dispatched,spec-w1.json}`; `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` diff; `.ufo/evidence/round-55/before/c2.stdout` (C0, HEAD, worktree).
- `.ufo/evidence/round-55/c2/measure.py` (grammar regex line 47, marker line 46, docs arm line 248), `.ufo/evidence/round-55/c1/measure.py` (lines 155, 171).
- Worktree: `corpus/SOURCES.md`, `corpus/knowledge/scratch-root-contract.md`, `SKILL.md`, `.ufo/evidence/round-55/{control/,integrate/}`, `.ufo/waves/round-55/**` mtimes.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (validate run only).
- Scratch clone `/fast/scratch/hyaku/tameshi-r55/T55W2SentScope2/c0-probe` at C0 (probes only).

## Tooling

No tool installed or upgraded for this seat (nothing was needed; all checks ran on git, python3 and coreutils already
present). No `pacman` transaction was attempted.

## Report

`.ufo/waves/round-55/w2/T55W2SentScope2.md` (this file) + `.ufo/waves/round-55/w2/T55W2SentScope2-receipts/`.
