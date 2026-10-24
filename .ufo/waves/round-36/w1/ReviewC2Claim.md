# ReviewC2Claim — C2 kill-rule review (exactly one deciding v2 run; no post-freeze counter edit)

Seat: leaf reviewer, read-only. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Lane tip at review: `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`. Measurement commit under review:
`b455001e2589b3f4f471d94a3de7e5e549b9f54c`. Frozen counter commit:
`e423c41ba253357ab8c8513f0376dad9d38ab248`. Base: `796e08b888849308d0c4d5e932e56833600a139f`.
Scratch: `/fast/scratch/hyaku/tameshi-r36-seats/ReviewC2Claim/` (counter copy only; no lane writes
beyond this report). Tools installed: none. Subagents: none (leaf seat).

## What I attacked

Contract C2 kill rule (`.ufo/evidence/round-36/contract.json`, verbatim):
`exactly one default-mode (deciding) v2 run at the measurement commit; v1 and v2 mutant-demo runs
are controls; no counter edit after this freeze`.

Three falsifiers, each independent:
1. more than one default-mode v2 run at `b455001e` (extra deciding run);
2. any post-freeze byte change to `.ufo/evidence/round-36/c1/c1-measure-v2.py`
   (frozen sha256 `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`);
3. a deciding receipt that does not correspond to the counter's actual output for
   `b455001e` (forged/mutated receipt) or a rerouted measurement (different tree/pins).

## Verdict

**PASS — kill rule not defeated.** Exactly one deciding v2 run exists at `b455001e`; the executed
counter bytes equal the frozen `9eb8944c…` at every commit and on disk; the committed receipt is
internally consistent with the counter's print contract and with the frozen inputs at that revision.
No HIGH or MEDIUM finding. Four LOW findings and residual risks below.

## Evidence

### 1. Counter hash chain (no post-freeze edit)

- `sha256sum .ufo/evidence/round-36/c1/c1-measure-v2.py` →
  `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` = contract
  `claims.C2.counter_sha256`.
- Same hash recomputed from the blob at every revision:
  `git show e423c41:… | sha256sum`, `git show b455001:… | sha256sum`, `git show d9c496b:… | sha256sum`,
  and `git hash-object` of the disk file vs `git rev-parse <rev>:<path>` (blob
  `5f1c2047ce533182a8938cb2b44d73938a54c153` at all three; disk matches).
- `git log --all --format='%h %ci %s' -S'C1_R36V2'` returns only the counter's first-add
  (`e423c41` 03:14:00 and its jj-export duplicates `3cbd764`/`ef37d72`, same tree
  `966d0fcb…`) and the receipts commit (`d9c496b` and duplicate `12edb47`, same tree —
  `git diff 12edb47 d9c496b` empty). No later commit anywhere in `--all` (843 `refs/jj/keep`
  included) modifies the counter.
- `git log --oneline -- .ufo/evidence/round-36/c1/c1-measure-v2.py` → one authoring commit
  (`e423c41`) plus jj duplicates only. `git log --oneline 796e08b..d9c496b --
  .ufo/evidence/round-35/c1/panel .ufo/evidence/round-35/c1/sealed tools/tally-audit-v3.py
  tools/mutate-and-run.sh` is empty: the panel, sealed set, tool and runner were untouched this
  round.
- L1 session record (`history://L1-tameshi-r36`) shows all edits to the counter at transcript
  lines 229–245, followed by `python3 -m py_compile` and the contract write (line 250–255,
  "v2 is frozen at sha256 `9eb8944c…`"). No `edit`/`write` call on the counter appears after the
  freeze. The compile-time `__pycache__` header records source mtime `1792821913` and size
  `24639`, matching the current source (file mtime 03:05:13, pre-freeze; contract written
  03:06:10; freeze commit 03:14:00).
- `git reflog --date=iso` is a linear `export from jj` sequence with no reset/amend/force event;
  no stash.

### 2. Exactly one deciding run

- Committed receipt cardinality across every ref: the only `round-36` v2 receipt files are
  `after/c1v2-at-b455001e.{stdout,stderr,exit}` (one deciding set) and
  `control/v2-at-emptypanel.{stdout,stderr,exit}` (the mutant-demo control). No other
  `c1v2*`/`v2-at*` path exists in any commit (`git log --all --name-only -- '*c1v2*' '*v2-at*'`),
  and no deletion of such a path exists (`--diff-filter=D` empty).
- Receipt: `after/c1v2-at-b455001e.stdout` (17 lines, 16 `COPY` + 1 predicate),
  `EXIT=0`, empty stderr; predicate line
  `C1_R36V2: mode=deciding … pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9
  ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1
  rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c C1_R36V2_PASS=true`.
- Exactly one deciding work directory exists for round 36:
  `/tmp/tameshi-r36-c1decide-1/work` (parent created 03:16:55.86; `tool.py` written 03:16:55.89;
  copy dirs `b1…b31` and `copy2.sh…copy32.sh` created 03:16:56 → 03:19:07; stdout receipt
  mtime 03:19:15.44; exit 03:19:15.45). Exactly 16 copy dirs — matching the 16 `COPY` lines
  (9 public + 7 sealed) and the receipt's set counts.
  A sweep `find /fast/scratch /tmp -name tool.py -newermt '2026-10-24 03:00' ! -newermt
  '2026-10-24 03:25'` finds only that directory and the two control work dirs
  (`/tmp/tameshi-r36-ctl-2/work1`, `work2`). No `c1decide-2` or second deciding work dir exists.
  The counter refuses a non-empty `--work` (`SETUP work_not_empty`, exit 2), so a second deciding
  run would require a fresh directory; none exists.
- L1 session record contains exactly one invocation of
  `python3 .ufo/evidence/round-36/c1/c1-measure-v2.py` against the lane (transcript line 375:
  `mkdir -p /tmp/tameshi-r36-c1decide-1/work && cd … && python3 .ufo/evidence…`), one `tail -3`
  check of that receipt (line 394), and one invocation against the mutant clone
  (`--lane /tmp/tameshi-r36-ctl-2/lane --rev 91373d5…`, line 400). No v2 invocation after the
  receipts commit; no rerun in the report-writing tail (lines 412–447).

### 3. Receipt is a real run's output, not a reroute or a forged line

- Counter output format checked against the code (`main()` print, lines ~546–552): field order,
  `pub_slots = pub_kill_slots + pub_accept_slots = 9`, `rev` full sha, `%s_PASS` label all match
  exactly. The receipt's 16 `COPY` set/class/file triples are exactly the committed
  panel (9 files) + sealed (7 files) at `b455001e` (set-compared programmatically; true/true).
- Independent re-derivation at `b455001e` with the counter's own functions (scratch import of a
  byte-copy; no lane writes): public slots kill=6/accept=3 (9 copies), `pub_distinct=9`;
  sealed kill=4/accept=3 (7 copies), `distinct=7` — exactly the printed values. Panel/sealed
  JSONs at that revision were counted directly: 6+3 public, 4+3 sealed.
- Inputs are revision-pinned: the counter reads runner/tool/panel/sealed via `git show <rev>:…`
  (code review), so the measurement is content-addressed, not working-tree-dependent. Pins at
  `b455001e`: runner `a7d3f2dd…`, tool `6188db16…` — both as frozen; the receipt prints
  `runner_sha_ok=1 tool_sha=6188db16 tool_sha_ok=1`. Counter executed was the worktree file whose
  blob equals the committed frozen blob (above).
- The 16 `COPY` rows are byte-identical to the round-35 deciding receipt
  (`history`-checked against `.ufo/evidence/round-35/after/c1-at-34fa5b0c…stdout`); the predicate
  line differs only in `rev` and the new `pub_slots/pub_distinct` fields. This is the expected
  deterministic reproduction of the same frozen 16-copy panel under the same pinned tool — the
  fresh work dir (16 copy dirs, 03:16:56–03:19:07) and the transcript's single launch show it is
  an execution, not a copied receipt.

### 4. Mutant controls are genuine (supporting, not the kill rule)

- `/tmp/tameshi-r36-ctl-2/lane` HEAD `91373d55…`, parent `b455001e`; the mutant commit deletes
  exactly the 9 panel JSONs (135 deletions, no other path). v1 counter there hashes
  `d360a159…` = the lane's frozen v1 (last changed `5829676`, round-35, not this round); v2
  counter `9eb8944c…`; tool/runner pinned as above.
- Sealed provenance at the mutant rev: contract first-add `d16f9b5a…` = manifest `freeze_rev`;
  each sealed file's last-modifying commit `691bb512…` descends from the freeze and precedes the
  rev — so `sealed_after_freeze=1` in both control receipts is honest.
- v1 predicate is the vacuous one (`pub_kill == pub_kill_slots` only; read at
  `.ufo/evidence/round-35/c1/c1-measure.py:516-521`), so `C1_R35_PASS=true` on a zero-slot panel
  is exactly the demonstrated defect; v2's added `==6/==3/==9` targets are present at
  `c1-measure-v2.py:540-545`.

## Findings by severity

- **HIGH: none.**
- **MEDIUM: none.**
- **LOW-1 (label conflation, observable contract).** The empty-panel control was run without
  `--tool`, so the counter labels it `C1_R36V2: mode=deciding` (not `C1_R36V2_CONTROL`), e.g.
  `control/v2-at-emptypanel.stdout:8`. The corpus therefore contains two lines matching
  `mode=deciding` for v2. The kill rule remains satisfied because the contract classifies
  mutant-demo runs as controls and the revs differ (`b455001e…` vs `91373d5…`), but a text-only
  audit keyed on `mode=` would over-count. Fix belongs to a future counter freeze (print the panel
  origin or require an explicit mode for mutant runs), not this round.
- **LOW-2 (attested, not enforced).** The counter has no run-once guard or run ledger: `--work`
  must be empty, but any fresh directory qualifies. "Exactly one deciding run" is therefore
  attested by artifacts (single receipt set, single work dir, L1 transcript) rather than enforced
  by the apparatus; a second run in a fresh later-deleted directory that reproduced identical
  output would be invisible in committed evidence. No such run is evidenced by any source checked.
- **LOW-3 (control state not archived).** Mutant commit `91373d5…` exists only in the scratch clone
  `/tmp/tameshi-r36-ctl-2/lane` (`git cat-file -t 91373d5…` fails in the lane). The before/after
  mutant receipts are committed, but the mutant tree is not; reproduction is the documented,
  trivial `git rm` of the 9 panel JSONs at `b455001e` plus the exact commands. Archiving the
  mutant diff (or the emptied panel manifest) would make the control self-contained.
- **LOW-4 (wording).** Committed records call the v2 run "the full deciding re-run"
  (`SCORECARD.md` C2 row; `.ufo/reports/round-36/tameshi.md` "the full 16-copy deciding re-run").
  Context makes clear this means the successor predicate run over the whole 16-copy panel, but
  beside a kill rule about "exactly one deciding run" the word "re-run" invites a misreading.
  Recommend "the full 16-copy deciding run" in future records.

## Residual risk and verification gaps

- The L1 transcript truncates long tool-call signatures at 512 bytes, so the deciding command's
  full flag list is not verbatim recoverable (`--lane/--rev/--work/--sealed` are reconstructed from
  the receipt's fields, the surviving work dir, and the contract's counting command). Nothing
  contradicts the reconstruction; the receipt's `sealed_after_freeze=1` and 7 sealed copy rows prove
  `--sealed` was supplied, and `rev=b455001e…` proves `--rev`.
- The deciding run (03:16:55–03:19:15) overlapped the v1 mutant control (03:18:29–03:19:29). The
  runs use distinct work dirs and distinct random `/tmp/tameshi-r4-2-regression.*` auto roots; no
  shared mutable path was found in the counter, so I do not treat this as contamination, but it is
  a schedule observation an auditor should know.
- The v1 control receipt prints no self-hash; its provenance rests on the surviving scratch clone's
  v1 bytes (`d360a159…`) and the lane's v1 history (untouched since `5829676`). If `/tmp` is
  cleaned, that cross-check is no longer directly reproducible.
- Filesystem mtimes used above (work dirs, receipt writes) are ephemeral; the committed receipt
  blobs and the git/jj history are the durable evidence.

## Commands run (revisions named)

All lane-relative; `cd /home/vgpnk/Projects/shokunin/tameshi-shokunin` first.

```
sha256sum .ufo/evidence/round-36/c1/c1-measure-v2.py
git show e423c41:.ufo/evidence/round-36/c1/c1-measure-v2.py | sha256sum   # also b455001, d9c496b
git hash-object .ufo/evidence/round-36/c1/c1-measure-v2.py
git rev-parse b455001e:.ufo/evidence/round-36/c1/c1-measure-v2.py
git log --all --format='%h %ci %s' -S'C1_R36V2'
git log --all --name-only -- '*c1v2*' '*v2-at*'
git log --all --diff-filter=D --name-only -- '.ufo/evidence/round-36/*' '.ufo/evidence/round-35/c1/*'
git log --oneline -- .ufo/evidence/round-36/c1/c1-measure-v2.py
git log --oneline 796e08b..d9c496b -- .ufo/evidence/round-35/c1/panel .ufo/evidence/round-35/c1/sealed tools/tally-audit-v3.py tools/mutate-and-run.sh
git reflog --date=iso -30
git diff --stat 12edb47 d9c496b ; git rev-parse e423c41^{tree} 3cbd764^{tree} ef37d72^{tree}
git show b455001e:tools/mutate-and-run.sh | sha256sum      # a7d3f2dd…
git show b455001e:tools/tally-audit-v3.py | sha256sum      # 6188db16…
git show b455001e:corpus/...  # (panel/sealed JSONs listed and counted: 6+3 public, 4+3 sealed)
git cat-file -t 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f    # not in lane
git -C /tmp/tameshi-r36-ctl-2/lane log --oneline -4        # 91373d5 (mutant) -> b455001e
git -C /tmp/tameshi-r36-ctl-2/lane show --stat 91373d5     # 9 panel JSONs deleted, only path
sha256sum /tmp/tameshi-r36-ctl-2/lane/.ufo/evidence/round-36/c1/c1-measure-v2.py   # 9eb8944c…
sha256sum /tmp/tameshi-r36-ctl-2/lane/.ufo/evidence/round-35/c1/c1-measure.py      # d360a159…
find /tmp /fast/scratch -name tool.py -newermt '2026-10-24 03:00' ! -newermt '2026-10-24 03:25'
find /tmp/tameshi-r36-c1decide-1/work -mindepth 1 -maxdepth 1 -type d | wc -l       # 16
python3 (scratch import of byte-copy c1-measure-v2.py): load_copies_rev + distinct_bodies at
        b455001e  -> pub 6/3 slots, pub_distinct=9 ; sealed 4/3, distinct=7
python3 (pyc header): recorded source mtime 1792821913 / size 24639 vs disk source (match)
jj --ignore-working-copy op log --no-graph --limit 18 -T '…'   # linear ops 03:14/03:16/03:21
history://L1-tameshi-r36 (grep + reads at lines 200-262, 360-412, 412-447)
```

**Verdict: PASS — C2 kill rule not defeated; counter sha256 recomputes to
`9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` at `e423c41`, `b455001e`,
`d9c496b` and on disk, and exactly one deciding v2 receipt/run at `b455001e` is evidenced across
committed artifacts, filesystem work dirs, and the L1 session record.**
