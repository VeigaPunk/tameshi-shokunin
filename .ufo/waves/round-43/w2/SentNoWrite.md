# SentNoWrite — round-43 commit-scope audit (wave 2)

Audited range: `487b8f0da89fa0e2b8bea6930068accbf36e70a9..c5335c70bff750218b3a6db0a92daae76509a0de`
(8 commits). Method: `git log` + `git diff-tree --name-status` per commit; `git show` /
`git cat-file -p` for content pins; the frozen counters re-run **only** at the permitted revs
(base not needed, freeze `3aee2c0`); lane read-only except this file.
HEAD moved twice during this audit (jj export): `e20cf89 → b510ad1 (A11, 08:03:09) → bb36f80
(A12, 08:05:44)`; both later commits are reported where they bear on scope.

## 1. Per-commit classification

| commit | subject | paths | in expected set? |
|---|---|---|---|
| `697d2f17` | freeze — contract, 3 counters, guard tool | `contract.json`, 3 `measure.py`, `tools/staged-id-guard.py` | yes |
| `f0f26367` | A1 — C2 extraction rules | contract + C2 counter | yes |
| `17f6ef0c` | A2/A3 — control battery, tool-file | contract, C1+C3 counters | yes |
| `5cd2154f` | A4/A5 | contract, `control/c2-round42-counter.stdout`, C1+C3 counters, guard tool | yes (see F8) |
| `114ffacd` | A6/A7 | contract, C2+C3 counters, guard tool | yes |
| `53cb32bc` | A8 | contract only | yes |
| `273c0471` | A9 | contract, C1+C3 counters, guard tool | yes |
| `c5335c70` | records | `.ufo/evidence/round-43/{before,census-sources,control,prerun,sources}` (24 files), `.ufo/waves/round-43/{build-spec.py,dispatch-w1.*,spec-w1.json,w1/*}` (35 files), `LOG.md`, `SCORECARD.md`, `corpus/{QUALITY,README,SOURCES}.md`, `corpus/knowledge/r43-…md`, `corpus/lessons/round-43.md` | yes |

**Paths outside the lane's own tree or outside the expected set (contract, three counters,
guard tool, records, evidence, waves): NONE.** No `/home/vgpnk/Projects/shokuknow/…` or
sibling-lane path appears in any commit; the assimilation package is untouched in git.

**`tools/write-path-census-v4.py`: touched by ZERO commits** in `base..c5335c7` (and zero in
`base..bb36f80`). Worktree and HEAD blob sha256 = `784de4c0…f5` = the contract's
`frozen_tools` pin. The pin is inherited, not re-measured this round.

**Delete record: NONE anywhere.** `git log --diff-filter=D` over `base..c5335c7` and
`base..bb36f80` is empty; no `D`, `R`, or `C` status in any commit.

## 2. Findings

### F1 — the records commit names three different "freezes", and all three are wrong or stale (HIGH)
- `SCORECARD.md:2053` (blob `c5335c7`): "frozen at `17f6ef0c…`". That is the A2/A3 freeze;
  five more freeze commits (`5cd2154f, 114ffacd, 53cb32bc, 273c0471`, then `3aee2c0`) changed
  the contract, two counters and the guard tool after it. All three counting commands in the
  same block (`SCORECARD.md:2059-2061`) pass `--freeze 17f6ef0c…`.
- `.ufo/evidence/round-43/contract.json:7` (`frozen_before`): "the freeze of record is
  `114ffacd`" — two freezes stale at `c5335c7`, four stale at HEAD (`bb36f80`). A8/A10/A11/A12
  never re-corrected it; this is the second consecutive provenance-narration defect (A8 fixed
  the same field once already).
- The actual freeze of record per the wave-2 brief is `3aee2c0`.
- Repro (all three documented commands can never print the target line — self_pin=0 because
  the contract at `17f6ef0c` pins older counter bytes):
  - `python3 .ufo/evidence/round-43/calibration/measure.py --lane … --rev 3aee2c0… --freeze 17f6ef0c…` → `self_pin=0 … C2_R43_PASS=false`, exit 1.
  - `…/guard/measure.py … --freeze 17f6ef0c…` → `self_pin=0 tool_sha_ok=0 … C3_R43_PASS=false`, exit 1.

### F2 — all three claim rows cite a receipts directory and a subsection that do not exist (HIGH)
- `SCORECARD.md:2059–2061`: every Evidence cell names `.ufo/evidence/round-43/after/` and
  every Verdict cell says "see the after subsection".
- `git ls-tree -r --name-only c5335c7 -- .ufo/evidence/round-43/after` → empty;
  `git log -- .ufo/evidence/round-43/after` → empty: the directory has **no content in any
  commit**. On disk it exists only as an empty untracked dir (mtime 07:47, before the freeze).
- No `### …after` subsection exists in the Round-43 block (2081-line file; last `###` heading
  for round 43 is none — the block ends at the standing row).
- `LOG.md` at `c5335c7` carries no "Deciding run" line for round 43 (last such line is
  round 42's, `LOG.md:2217`); the round-43 entry starts at `LOG.md:2221` and records targets
  only. The commit message's "receipts" list covers `before/ census-sources/ control/
  prerun/ sources/` — `after/` is silently absent.
- Direct falsification of the records commit: the counter's own m8 class flags it.
  Running the **frozen** C2 counter (blob `97609511`, copied to `/tmp/tameshi-r43-w2-
  SentNoWrite-c2/measure.py`, sha matches the `3aee2c0` contract pin) at the permitted rev:
  `python3 measure.py --lane … --rev 3aee2c0… --freeze 3aee2c0…` →
  `m7=5 m8=3 total=8 C2_R43_PASS=false`, exit 1, `first=m7:corpus/lessons/round-43.md_unknown_S160`.
  Full hit list (computed with the module's own functions at `3aee2c0`):
  - m8: `SCORECARD.md#round-43:.ufo/evidence/round-43/after/`,
    `corpus/lessons/round-43.md:.ufo/waves/...`, `corpus/lessons/round-43.md:tools/*.py`
    (the lesson cites glob/ellipsis strings that `path_cites` treats as paths).
  - m7: `S160, S166, S256, S259` unknown in `corpus/lessons/round-43.md`, `S256` unknown in
    `LOG.md#round-43` — the records' own prose (next-free and safe-floor numbers) trips the
    counter's unknown-id class because the mask only covers `staged:S###` and the exact
    `Next unused id:` form.
  So the records commit's C2 target (`total=0`) is unreachable **at the freeze of record**
  with the records it committed — `m6=0 m10=0 m11=0 m12=0 m13=0` hold.

### F3 — the freeze of record `3aee2c0` cannot pass C1 at all (HIGH)
- The C1 predicate (`mutants/measure.py:562,638`) requires `mutants_sha_ok=1`, computed from
  `contract.claims.C1.mutants_sha256` — **a key the A10 contract does not contain** (verified:
  `claims.C1` keys at `3aee2c0` lack `mutants_sha256`; it appears only at `b510ad1`/A11).
- Run at the permitted rev: `python3 .ufo/evidence/round-43/mutants/measure.py --lane …
  --rev 3aee2c0… --freeze 3aee2c0…` → `mutants_killed=5 dead_code_only=1 unresolved=0
  mutants_sha_ok=0 … C1_R43_PASS=false`, exit 1 (self_pin read 0 at run time because the live
  worktree counter was mid-edit; see F5).
- The declared target (`contract.json` claims.C1.target, `SCORECARD.md:2059`) does not even
  name `mutants_sha_ok`: the declared target is not the predicate.

### F4 — the capability row cites the superseded first-freeze tool blob (MEDIUM)
- `SCORECARD.md:2074`: `tools/staged-id-guard.py @
  8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762` — that sha is the blob
  added in `697d2f17`, the first (A4-refuted) version. The same commit's `contract.json`
  pins `e219007f…`; the freeze of record pins `2e8f2e89…`. One commit, three versions of the
  truth; the published capability pin is the bytes the lane's own A4 narration says were
  defective.

### F5 — the lane is still mutating its frozen surface during wave 2 (MEDIUM)
- Two jj-exported commits landed mid-audit: `b510ad1` (A11: contract + C1 counter +
  `corpus/knowledge/r43-…md` + `corpus/lessons/round-43.md`) and `bb36f80` (A12: contract +
  C1 counter + C3 counter + `corpus/QUALITY.md`). Counter pins moved: C1 `0d0f81bd→b56a34d7`,
  C3 `ae66342d→47a6afce`.
- Consequences: (a) the records committed at `c5335c7` are edited post-records without a new
  records commit; (b) my C1 run at `3aee2c0` printed `self_pin=0` solely because the worktree
  counter's live bytes were being rewritten (`sha256` observed at `b56a34d7`, then `3d1ff3dc`
  — the A11/A12 blobs — while HEAD advanced), so every seat's `self_pin`/`counter_sha256`
  field is racy until the counter bytes stop moving; (c) `prerun/c{1,2,3}-at-A12.stdout` exist
  on disk uncommitted — the L1 is already re-recording receipts against A12.
- 9 wave-1 seat reports are modified-but-uncommitted in the worktree (`CritC2Vacuum … 
  ScribeQuality`), i.e. wave-1 evidence published at `c5335c7` is being rewritten in place.

### F6 — "every wave-1 seat report" is false (MEDIUM)
- The records commit message claims all wave-1 reports and receipts. Two wave-1 reports are
  absent from the tree and still untracked at HEAD: `.ufo/waves/round-43/w1/CritC1Overfit.md`,
  `.ufo/waves/round-43/w1/RevC1Counter.md`. (`spec-w2.json`, `dispatch-w2.json` untracked is
  expected — wave 2 is live.)

### F7 — ignored build artefacts inside the frozen evidence tree (LOW)
- `.ufo/evidence/round-43/{mutants,calibration,guard}/__pycache__/measure.cpython-314.pyc`
  exist on disk, gitignored (`.gitignore:4`). The frozen counters compile into the evidence
  tree on every run; a `*.pyc` blob is a non-receipt artefact sitting inside the receipt
  namespace — a directory-based audit can't distinguish it from evidence.

### F8 — a freeze commit carries a receipt (LOW)
- `5cd2154f` adds `.ufo/evidence/round-43/control/c2-round42-counter.stdout` inside the A4/A5
  freeze. Freezes are therefore not content-free: provenance must be checked file-by-file,
  not by commit kind. (Content is a control receipt and pre-deciding — flagged for the audit
  rule, not as an integrity defect.)

## 3. Bottom line

Scope-clean: every committed path lands in the expected set; `tools/write-path-census-v4.py`
untouched (`784de4c0` = pin); zero deletes.

Scope-unsafe: the records commit publishes verdict-less claim rows pointing at an `after/`
tree that exists in no commit, numbers a freeze (`17f6ef0c`) that none of its three counters
can self-pin under, pins the guard tool at the A4-refuted first blob, and omits two wave-1
reports. At the permitted freeze `3aee2c0` the frozen counters reproduce `C2_R43_PASS=false`
(total=8) and `C1_R43_PASS=false` (`mutants_sha_ok=0`, a predicate field absent from both the
contract and the declared target) — i.e., two of the three claims are unprovable at the
freeze of record with the records committed. The lane then kept amending counters and record
files post-records (A11/A12), which supersedes the audited state without a new records commit.
