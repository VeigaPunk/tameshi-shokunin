# T55W1SentScope — wave-1 write-and-scope audit

Seat `T55W1SentScope` (sentinel, leaf). Round 55 wave 1, item: audit the wave's own
behaviour — every file written under `.ufo/waves/round-55/w1/`, every stray write
elsewhere in the lane or the fleet root, the frozen set and the lane production
files against `git status`, and the lane's git/jj history against new commits,
changed refs and the reflog.

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; base
`0a2010acd1e92e4e332774050825e21bcfc7e079`; frozen counter set
`631cd6455e58dce969310b4c0466c3383d9f5108`. Observation window
2026-10-28 13:59–14:11 -0300 (a live wave: the L1 was writing while I read;
§Limits). I edited no lane production file and no frozen file; all my writes are
`T55W1SentScope.md`, `T55W1SentScope.json` and `T55W1SentScope-receipts/`.

**Bottom line.** No new commit, no ref move, no reflog entry, no staged change and
no worktree of the lane exists after the freeze export at 13:37:22 — the
history-mutation check is clean. The frozen *set*, however, is not: between 13:49
and 14:00 the L1 (`TameshiR55`) edited four frozen paths in the working tree (five
amendments, three hashes in `freeze.json` that no longer match the bytes, and a
`before/c2.stdout` premise receipt cut from 43 lines/2634 B to the single verdict
line). Finding F1–F3 below.

---

## 1. Method (commands and their receipts)

Every command below was run with absolute paths; output is in
`T55W1SentScope-receipts/`.

| receipt | command |
|---|---|
| `lane-git-state.txt` | `git status --porcelain`; `git rev-parse HEAD`; `git for-each-ref --format='%(objectname) %(refname) %(committerdate:iso)' refs/heads refs/remotes/origin/HEAD`; `git reflog -6`; `git symbolic-ref -q HEAD`; `git worktree list` |
| `no-mutating-git-evidence.txt` | `git reflog --all --date=iso`; `git status --porcelain --untracked-files=no`; `git diff --cached --stat`; `stat` of `.git/index .git/HEAD .git/logs/HEAD .git/COMMIT_EDITMSG` |
| `w1-inventory-full.txt` | `find .ufo/waves/round-55/w1 -type f -printf '%TH:%TM:%TS %10s %p\n' \| sort -k4` (all 1108 files) |
| `w1-inventory.txt` | top-level file listing with sizes and mtimes; `git status --porcelain .ufo/waves/round-55` |
| `stray-write-sweep.txt` | `find . -path ./.git -prune -o -path ./.ufo -prune -o -type f -newermt "2026-10-28 13:37:22" -print`; round-55/r55/R55 name search in lane and fleet root; `git -C /home/vgpnk/Projects/shokunin status --porcelain` |
| `frozen-drift-history.txt` | `git diff --stat -- .ufo/evidence/round-55`; parsed amendment counts; per-file sha256 vs `freeze.json`; `stat` mtimes |
| `freeze-manifest-audit.txt` | freeze-manifest hash audit, working tree vs `631cd64` blobs |
| `before-receipt-timeline.txt` | committed vs working-tree `before/c2.stdout`; corroborating seat receipts written before this audit |
| `production-scope.txt` | per-file status table; `git diff --numstat`; parsed-JSON semantic walk; `git diff -U0` hunk headers |
| `object-write-anomaly.txt` | object-count census, samples, reachability check, controlled clone probe |
| `census.txt` | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` |

Census: **exit 0**, `tameshi ok .../corpus/SOURCES.md`; the table now carries
140 `S###` rows (139 + S280 for round 55) — receipt `census.txt`.

---

## 2. What was written under `w1/`

**1150 files in 66 directories** at the final inventory regeneration (14:20);
1108 files at the first (14:17) — the wave is live and seats were still writing.
Of the top level: 50 seat reports (`*.md`), 37 machine-readable `*.json` (mine
included), the L1's `swarm-registry.json`, and 59 `*-receipts/` directories. The
full per-file list with mtimes and sizes is `w1-inventory-full.txt`; seats and
their report paths are named there. Counts per receipt directory are in
`w1-inventory.txt`. Every write is under the wave's own directory; my own
`T55W1SentScope*` entries are the only files this seat added.

## 3. Stray writes elsewhere — lane

`git status --porcelain` at 14:16 (receipt `lane-git-state.txt`):

```
 M .ufo/evidence/round-55/before/c2.stdout          <-- FROZEN, finding F3
 M .ufo/evidence/round-55/c1/measure.py             <-- FROZEN, finding F1/F2
 M .ufo/evidence/round-55/c2/measure.py             <-- FROZEN, finding F1/F2
 M .ufo/evidence/round-55/contract.json             <-- FROZEN, finding F1/F2
 M .ufo/evidence/round-55/freeze.json               <-- FROZEN, finding F1/F2
 M .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md   <-- round-54 seat file, F4
 M LOG.md  M SCORECARD.md  M SKILL.md
 M corpus/QUALITY.md  M corpus/SOURCES.md  M corpus/knowledge/scratch-root-contract.md
 M corpus/lessons/round-54.md
 M tools/context-capture.py  M tools/registry-check.py  M tools/registry.json
 M tools/repeat-control.py
?? .ufo/evidence/round-55/assimilation/
?? .ufo/waves/round-55/            (the wave's own directory)
?? corpus/lessons/round-55.md
```

All sanctioned round-55 deliverables are present and scoped as the assignment
states (`production-scope.txt`):

| deliverable | status | scope check |
|---|---|---|
| `tools/repeat-control.py`, `tools/context-capture.py` | M | grammar-line edits only (+22 / −11 lines) |
| `tools/registry.json` | M | semantic delta is exactly the **7** `rows/*/scratch_root` cells; the 1275/1026-line diff is a whole-file reformat (F4b) |
| `corpus/knowledge/scratch-root-contract.md` | M | has `## One line, every mode (round 55)` at line 71, the 8 allocating and 5 lazy modes |
| `SKILL.md` | M | one hunk at `@@ -37,3 +37,6 @@`, the `## Standing rules` paragraph only — no other section touched |
| `SCORECARD.md` | M | corrections section at `+2620,83` plus five in-place line fixes |
| `LOG.md` | M | one new entry at `+2521,33` plus two in-place corrections |
| `corpus/QUALITY.md` | M | one criterion (`Falsifier that must fail`, round-54 C2 line) |
| `corpus/SOURCES.md` | M | S280 row + round-55 log line (S281 refused as held document, not appended) |
| `corpus/lessons/round-55.md` | new | present |

Two lane writes are **outside** the enumerated deliverables (F4):
`tools/registry-check.py` and `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`.

## 4. Stray writes — fleet root

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (`stray-write-sweep.txt`):
` M .scratch/goal-20261028-hyaku-run11.md` plus pre-existing untracked strays
(`o.bin`, `oldrep1.out`, `oldrep2.out`, `.ufo/reports/round-38/souji.md`, …).
The goal file is the **orchestrator's** run-11 log (its `## Run log` section was
appended at 13:41 and 14:03; no seat id is attached and no seat receipt claims
it). No round-55-named file exists outside the lane except the orchestrator's
own tracked prompt `.ufo/prompts/tameshi-round-55.md` (unchanged, 13:26). The
untracked strays predate the wave (mtimes 09:10 and 2026-10-27).

## 5. History: no mutating git/jj in the lane

- `HEAD = 631cd645…`, **detached** (jj export leaves a detached HEAD); `master`
  and `origin/HEAD` both `631cd645…`; the two side branches still at their
  Oct-21 commits. No branch was created or moved (`lane-git-state.txt`).
- `git reflog -6`: top entry `631cd645… HEAD@{0}: export from jj` at
  **13:37:22**, i.e. *before* the wave's dispatch (`swarm-registry.json` at
  13:40:22). Nothing since (`no-mutating-git-evidence.txt`; `reflog --all` shows
  the same three exports of the day).
- `git diff --cached --stat` is empty — nothing staged. `.git/index` is unchanged
  since 13:48:03 (size 1872944). `git worktree list` shows the one worktree only;
  `.git/worktrees` does not exist; `.git/COMMIT_EDITMSG` is from 2026-10-20.
- Commits: 1708 commit objects, 1700 reachable, 8 unreachable — and every
  unreachable one is dated 2026-10-20 (`author … 1792453155/1792502510/1792510173`),
  none from this wave (`object-write-anomaly.txt`).
- jj: `.jj/repo/op_heads/heads/` and the newest `.jj/**` file are at
  **13:37:24.9**, 2.5 s after the freeze export and before dispatch; no jj
  operation ran during the wave.

**No seat ran a mutating git/jj command against the lane's history.** The one
caveat is the object-DB churn in F5.

---

## 6. Findings

### F1 — CRITICAL — the frozen contract/counters were edited during the wave; amendment 5 amends the C1 counter *after* a wave-1 seat finding

**Seat: `TameshiR55` (L1).** Evidence of authorship: the amendment records are in
the L1's voice and self-attribute ("Found by the L1 dry run"), and A5 names the
wave-1 seat whose finding triggered it. No w1 seat receipt claims any write to
`.ufo/evidence/round-55/`; the seats that noticed the drift wrote it down as
observed, not mine (`T55W1Er01-receipts/frozen-set-worktree-state.txt`,
`T55W1Er05-receipts/frozen-drift-observed.txt` and `T55W1Er05.md` §7,
`T55W1Er02.md` §11, `T55W1Er08-receipts/frozen-window-diff.patch`).

`$ git diff --stat -- .ufo/evidence/round-55` (`frozen-drift-history.txt`):

```
 .ufo/evidence/round-55/before/c2.stdout |  43 ----
 .ufo/evidence/round-55/c1/measure.py    |  25 +
 .ufo/evidence/round-55/c2/measure.py    |  32 +-
 .ufo/evidence/round-55/contract.json    |  23 +-
 .ufo/evidence/round-55/freeze.json      |  19 +-
```

The committed contract at `631cd64` carries `amendments: []`; the working tree
carries **five** (mtimes 13:49:59–14:00:09). A1–A4 are discovery plumbing for the
C2 ruler. **A5 is different**: "c1/measure.py's stale scan was line-scoped … and
read three record files; wave-1 seat T55W1Er01 found a falsehood the window could
not see … The predicate is unchanged and now stricter". That is a change to the
C1 *measurement ruler*, made in response to a seat that ran under the frozen
ruler, in the same wave whose C1 verdict the ruler decides. The round's own
premise (`premise=10/10 stale=4 total=10`, receipt `before/c1.stdout`) was
produced by the weaker scan; the target `total=0` will be produced by the
stricter one. A stricter after-ruler cannot manufacture a false pass, but the
before/after numbers are not the same measurement, and the round must say so
(A5 says only "the predicate is unchanged").

**Impact.** The contract's defining property — frozen *before any seat ran* — is
false in the working tree. Any reader comparing the L1's wave numbers with the
`631cd64` contract sees two different rulers. The deciding-run script cannot see
this: gate 0 hashes the frozen files **at the `FREEZE` commit**
(`deciding-run.sh:20-40`), and `FROZEN_UNCHANGED` compares `FREEZE`..`REV`
(`:66`) — it never reads the working tree, so pointing `FREEZE` at a commit that
contains the amendments makes both checks pass and silently re-anchors the
freeze after the wave.

**Smallest remediation.** Either (a) restore all five frozen paths from
`631cd64` before the content commit, or (b) if the amendments are kept, commit
them in a commit that is explicitly labelled a *post-wave amendment* and pass
`FREEZE` = that commit while recording in the report that the freeze was
re-anchored mid-wave (A5 specifically: "the premise receipt was produced by the
weaker scan"), and add to the deciding-run gate a `git status --porcelain
.ufo/evidence/round-55` check so working-tree drift of the frozen set cannot
ride along. I propose; the L1 integrates.

### F2 — CRITICAL — the freeze manifest does not verify its own set

`freeze.json` pins `contract.json` = `ed6871e1…`, `c1/measure.py` =
`77abe1e9…`, `c2/measure.py` = `ab3ae751…`; the working-tree bytes are
`5de4f37b…`, `711507e7…`, `d6ca1d85…` respectively — **three of six hashed
files DRIFT** (`frozen-drift-history.txt`, `freeze-manifest-audit.txt`). The
manifest still carries **3** amendments while the contract carries **5**, so the
two frozen records disagree about their own history. `no-harm.sh`,
`deciding-run.sh` and `controls.sh` are unchanged and OK.

The amended bytes are pinned nowhere: they are not in git (the `631cd64` blobs
are the originals) and the manifest hash does not match them. The seats measured
with `d6ca1d85` (C2, `T55W1ExecCountersAtBase`) and `711507e7` (C1) — bytes that
exist only in the working tree until they are committed, while the deciding run
copies the counters from `REV` (`deciding-run.sh:76-79`).

**Impact.** No independent byte-verification of the ruler the round reports is
possible. Either the deciding run uses the *committed* counter (9d0768/77abe1e9
— the versions A1–A5 declare defective) or the L1 commits the amendments and
re-points `FREEZE`, at which point "frozen before any seat ran" is an assertion
about an unverified past.

**Smallest remediation.** Regenerate `freeze.json` from the bytes actually
committed, keep its amendment list identical to the contract's, and make the
report state which commit is the freeze and which ruler each quoted number came
from.

### F3 — HIGH — the frozen C2 base premise receipt was rewritten three times in the working tree

`before/c2.stdout` at `631cd64` is 43 lines / 2634 B (`EXPLAIN` per mode plus the
verdict line). The working-tree copy is **139 B**, the verdict line only, mtime
13:59:44 (`before-receipt-timeline.txt`). Its retained content is

```
C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false
```

The rewrite history is already on record from seats that read it before this
audit: `T55W1ExecCountersAtBase.md` **F4** — "139 B with `usable=12/13 total=19`
at 13:47; 0 B at 13:50 (truncated in place); 139 B with `usable=13/13 total=18`
at 13:59" — and `T55W1ScribeLog-receipts/before-receipt-drift.txt` — the earlier
139 B read `total=19`, i.e. a **different measurement** was briefly the premise
receipt. `T55W1ScribeLog` records the writer as the L1 ("observed before the L1
re-ran it"); no seat receipt claims the write.

**Impact.** The C2 premise receipt the assignment cites (`grammar=6/8 … total=18`)
is a moving target in the lane; it no longer shows *which two* grammar classes
failed, and a mid-write `cmp` reads 0 B. The gate does not hash it (it is not in
`frozen_paths`), so nothing detects the truncation.

**Smallest remediation.** Restore `before/c2.stdout` from `631cd64`; if the L1
wants the fresh run kept, write it beside the frozen one (e.g.
`before/c2-rerun.stdout`) instead of over it.

### F4 — MEDIUM — two writes outside the enumerated deliverables; one whole-file reformat

- `tools/registry-check.py` (+10/−1): adds `class ScratchRootUnusable(RuntimeError)`
  and two `except ScratchRootUnusable` handlers. Not required by any deliverable:
  the base grammar arm already printed the frozen line and exited 2 through the
  generic `except RuntimeError` branch (`before/c2.stdout` line 2 is
  `registry-check --selftest rc=2 ok`). It is also at odds with the note's own
  honest position that the class is a line grammar, not a shared Python type.
  Inert for the counter (the behaviour is unchanged); unnamed in the round's
  change list.
- `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` (+13): a `SUPERSEDED
  (round 55, ER-R54-8)` block. Defensible under C1's R54.8 ("the seat file
  marked superseded") but it edits a prior wave's seat report; if kept, the
  corrections section should say the edit was made in round 55.
- `tools/registry.json`: `git diff --numstat` = **1275/1026 lines**, but a
  parsed-JSON walk against `631cd64` finds **exactly 7 semantic differences**,
  all `rows/*/scratch_root` (receipt `production-scope.txt`). The content is
  correct and scoped; the churn is a whole-file reformat that makes the
  seven-cell claim expensive to audit.

**Smallest remediation.** Drop the `registry-check.py` edit (or name it); keep
the superseded block and name it; re-emit `registry.json` with its original
formatting so the diff is the seven cells.

### F5 — LOW / unresolved — an unattributed writer repeatedly writes fixture-tree objects into the lane's object DB

`find .git/objects -type f -newermt "2026-10-28 13:40:00" | wc -l` → **5250**
(8266 loose total, `count-objects`). The objects are blobs and trees of *fixture*
directories (`subset/`, `tools/`, `PROVINCE.md`, `SKILL.md`, and a
`.ufo/waves/` snapshot with `round-12`…`round-18`,
`fleet-round-1-interactive`); several are re-written minutes apart (one tree's
mtime moved 14:03:45 → 14:05:40; the buckets 13:56 / 14:03 / 14:05 / 14:07–14:08
grow while the loose total stays constant). No ref, reflog, index, HEAD,
worktree or reachable-commit changed (§5). A controlled probe — `git clone
--shared --no-checkout` of the lane, checkout at `631cd64`, `git add -A`, `git
commit` — left the lane's object count at 8277 → 8277 → 8277, so the ordinary
shared-clone staging path is *not* the writer.

**Impact.** Dangling objects do not alter history and the deciding-run gates do
not see `.git/objects`, so this is not a claim-integrity defect; it is an
unattributed process with write access to the frozen repo's object store during
the wave, and it means object-count/mtime forensics on the lane are unreliable
for any later auditor.

**Smallest remediation.** Identify the writer (likely a seat command that
exported `GIT_DIR`/`GIT_OBJECT_DIRECTORY` into a lane tool's selftest fixture;
the tools themselves scrub `GIT_*`, so a seat-level export is the suspect), and
run the deciding run with an isolated object environment. Recorded, not fixed.

### F6 — INFO — fleet-root writes

`M .scratch/goal-20261028-hyaku-run11.md` (orchestrator run log; mtime 13:41 at
my first read, **14:07:11** at my last, diff +17/−4 including its `## Run log`
section) only; no seat-named fleet write. No round-55-named file exists outside
the lane except the orchestrator's own tracked prompt
`.ufo/prompts/tameshi-round-55.md` (unchanged, 13:26). The untracked strays
predate the wave (mtimes 09:10 and 2026-10-27). Nothing to fix.

---

## 7. Limits

- The wave is live: `tools/registry-check.py` was still unmodified at my first
  status read (13:59) and modified at 14:16, and the contract grew from
  amendments 1–3 (13:48) to 1–5 (14:00) while I read. All statements are
  point-in-time with the mtimes above; a later snapshot may show more.
- Attribution of F1–F3 rests on (a) the amendment records' own voice and their
  naming of the L1, (b) the `T55W1ScribeLog` receipt naming the L1 as the
  re-runner, and (c) the absence of any seat receipt claiming the writes. No
  shell trace of the L1's commands was available to me, so I name the L1 as the
  writer on that evidence, not on a captured command line.
- F5 is reported as unresolved: I could not attribute the object writes, and I
  did not try to make them happen (I ran the shared-clone probe only, which wrote
  nothing to the lane).

## 8. What the main agent should check

1. `git -C LANE diff --stat -- .ufo/evidence/round-55` — should be empty at the
   content commit, or the amendments explicitly re-anchored per F1(b)/F2.
2. `python3 -c "import json,hashlib; …"` over `freeze.json` — all six pins must
   match the committed bytes (F2).
3. `git -C LANE show <FREEZE>:.ufo/evidence/round-55/before/c2.stdout | wc -lc`
   → `43 2634` (F3).
4. `git -C LANE reflog -3` — top entry still the freeze export (no seat mutation).
5. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin tameshi` → exit 0 (re-ran at 14:17: exit 0).
