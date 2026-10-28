# T56W1RevInherited — inherited-state audit (round 56, wave 1)

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`.
Receipts: `.ufo/waves/round-56/w1/T56W1RevInherited-receipts/` (15 files, named per §6).
Machine-readable lists: `.ufo/waves/round-56/w1/T56W1RevInherited.json`.

**Verdict.** (a) holds: all 244 files the sweep added are this lane's round-55 wave evidence, every one under
`.ufo/waves/round-55/`, every seat directory in the round-55 roster; nothing is misrooted and no added file is
another lane's deliverable. (b) does **not** hold as stated: the sweep reverted **34** tracked entries, not 23,
and the revert was not free — it left two committed receipts without any producer command in the tree, and it
restored a provenance pin that contradicts the sibling README and the seat's own report. (c) holds: round-55's
frozen counter bytes, contract, controls and receipts are intact at their paths (freeze manifest 7/7 OK).

The number **23 appears nowhere in the tree**; the pre-revert working copy is recoverable and carries 17 modified
+ 17 deleted. See §2.2.

---

## 1. (a) The untracked round-55 files committed at round start

### 1.1 What the two commits actually contain

```
$ git log -1 --format='%H %P%n%ci%n%s' 6efd2a19
6efd2a19d35f457eb49daa82a6c5944fb22baa1f fa48c06c3669355fd80e8722eb733c1d6dfdd2f8
Wed Oct 28 15:23:19 2026 -0300
round-56: inherited round-55 seat deliverables swept at round start (R55.6); post-tip closure rewrites reverted to branch bytes (R55.7)
$ git show --name-status --format='' 6efd2a1 | awk '{print $1}' | sort | uniq -c
    235 A
$ git show --name-status --format='' 981c5e8b | awk '{print $1}' | sort | uniq -c
      9 A
```
(receipt `01-commits-and-tallies.txt`)

Both commits are **pure additions** — 235 + 9 = **244 files**, 0 modified, 0 deleted. The 9 at `981c5e8b`
(receipt `01`, and sizes in §1.4) are 8 monitor dumps of ~3 MB plus `w3-results.json`.

### 1.2 The "96" is a porcelain count, not a file count — confirmed

`git status --porcelain` collapses a wholly-untracked directory into one entry. Reproducing that collapse over
the 244 paths (for each path, the child of the deepest ancestor directory that exists at `fa48c06c`) gives
exactly 96 entries:

```
added files: 244
collapsed porcelain entries: 96
```
(receipt `03-porcelain-collapse-96.txt`)

So the item's "96 untracked round-55 files" and the commits' 244 files are the same set counted two ways. The
L1 should state 244 files / 96 porcelain entries, because the round's own record will otherwise be read as
"96 files were swept" when 244 landed.

### 1.3 Every added path is this lane's round-55 evidence

- **Location.** All 244 paths begin `.ufo/waves/round-55/`; the empty check below shows nothing was added
  outside it (receipt `07`):
  ```
  $ git diff --name-status fa48c06c 981c5e8b -- . ':!.ufo/waves/round-55'
  (empty)
  ```
- **Roster.** Every seat directory among the 244 resolves to a seat in *this lane's* round-55 specs:
  ```
  roster seats (w1+w2+w3): 141
  unmatched seat dirs: 0
  results-level paths (no seat dir): 3
    .ufo/waves/round-55/w1-results.json
    .ufo/waves/round-55/w2-results.json
    .ufo/waves/round-55/w3-results.json
  ```
  (receipt `04-seat-membership.txt`)
- **Content scan for another lane.** Absolute paths inside the added bytes (receipt `05-content-scan-other-lanes.txt`):
  ```
     8043 /home/vgpnk/Projects/shokunin
      112 /home/vgpnk/Projects/shokuknow
        9 /home/vgpnk/Projects/ufo-fsd-alpha
        7 /home/vgpnk/Projects/kimi-shokunin
  ```
  Every non-`shokunin` hit and the 8043 fleet-root hits are **read paths inside cold-read monitor ledgers**
  (`coldread-HEAD.json`, `coldread-at-base.json`, `ExecRekeyPrep/{base,cand,floor,rekey}.json`,
  `ScoutColdread-receipts/inputs.json`), which record the files the fleet-wide monitor read, e.g.
  `"…/ufo-fsd-alpha/crates/ufo-core-runtime/src/gate.rs": "b4e433fd…"`. They are references, not copies; no
  added file *is* another lane's artifact.
- **Lane identity fields.** `"lane": "tameshi"` in the wave results/ready files. The only foreign lane token,
  `"lane": "mado"` (2 hits), is quoted *data* inside a stray-writes audit
  (`w2/T55W2SentStrayWrites-receipts/02-untracked-content-markers.txt:28`), auditing a
  `.scratch/closure-mado-r50.json` artifact it found. Not this lane's identity, not a copied deliverable.

**What "lane-authored" can and cannot mean here.** Authorship is not provable from git; what is shown is
location, roster membership, artifact class and identity field. The 244 are wave deliverables (`.md`), results
(`w*-results.json`), receipts (`.stdout/.out/.txt/.meta/.rc/.tsv/.diff`) and reproducers (`.py/.sh`).

### 1.4 The second commit's message is imprecise

`981c5e8b` says "monitor dumps (>1 MiB, skipped by the directory sweep) named as files". Eight of its nine files
are 2.9–4.0 MB monitor dumps; the ninth, `.ufo/waves/round-55/w3-results.json`, is **209,693 B** — a wave
results file, not a monitor dump and not >1 MiB. Low severity (commit prose, no claim depends on it), but the
round's LOG/lesson must not repeat the message as fact.

---

## 2. (b) The tracked files reverted to branch bytes

### 2.1 The requested diff cannot show them — and that is the finding

```
$ git diff fa48c06c 981c5e8b --stat
 244 files changed, 203004 insertions(+)
```
(receipt `01`) — only additions. A revert *to branch bytes* produces no diff against the branch, so the 34
reverted entries are invisible in `fa48c06c..981c5e8b` by construction. The item's instruction to list them from
that diff cannot succeed; the list has to come from the pre-revert working copy.

### 2.2 Recovering the pre-revert state (read-only, no jj command)

The lane is a jj-backed checkout (`store/type` = `gitextra`, 1,704 `refs/jj/keep/*`). The sweep's jj change
`nrwospytssrypyknouwqszqyuzzlqptx` was snapshotted twice before it was committed, and those snapshots are
reachable by ref and readable with plain `git`:

```
$ git diff --name-status fa48c06c 2dc8633ab0d6853bd8ede3750646b1ec2716cba3
     17 M
     17 D
$ git diff --name-status 0253bf9e9450bf18d9d811b2eec7eb465dd8e3ce^ 0253bf9e   # 15:01:57 snapshot
     14 D
     17 M
```
(receipts `06-prerevert-34-delta.txt`, `14-jj-snapshots.txt`)

`2dc8633a` (15:04:06, parent `fa48c06c`, same change-id as `6efd2a1`) is the last pre-revert state. It holds
**17 modified + 17 deleted = 34** tracked entries. The sweep restored all 34 (`6efd2a1` has 0 M/0 D), so the
count is 34, and no snapshot in the sweep window yields 23 (the 15:23:19 snapshots are 17 D, 2 A + 17 D, 235 A).

The 34, with disposition (full list and per-file reasoning in `T56W1RevInherited.json` → `reverted.rows`):

| # | path (under `.ufo/`) | kind | disposition |
|---|---|---|---|
| 1 | `evidence/round-55/after/c2.stdout` | M | closure rewrite; **revert correct** (see §2.3) |
| 2 | `waves/round-55/w1/T55W1MutC2-receipts/counter-under-test.sha256` | M | **revert reintroduces a contradiction** (B2) |
| 3–11 | `…/T55W1MutC2-receipts/mutants/m1..m9.diff` | D | first-pass receipts; README keeps them → restore required |
| 12–13 | `…/T55W1MutC2-receipts/P-base.{meta,stdout}` | D | same |
| 14 | `…/T55W1MutC2-receipts/counter-bytes.txt` | D | same |
| 15–16 | `…/T55W1MutC2-receipts/fixed-tree-line-*.txt` | D | same |
| 17 | `waves/round-55/w2/T55W3R16-receipts/selftest-tally-audit-v2.out` | M | +7 lines incl. `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`; no committed record cites 22/22 → not claim substance |
| 18–27 | `waves/round-55/w2/T55W3SentReaders-receipts/{01,02,03,05,06,07,quotes.py,run-receipts.sh,run.log,shas.py}` | M | **run-receipts.sh revert orphans two receipts** (B1); the rest are post-tip reruns whose branch bytes the committed report cites |
| 28–30 | `waves/round-55/w2/T55W3SentReaders-receipts/{09-c0-read-evidence.txt, binder-crash-with-HEAD-resolutions.out, resolutions-at-HEAD.json}` | D | `09-…` is cited by the committed `T55W3SentReaders.md` → restore required; the other two uncited |
| 31–33 | `waves/round-55/w3/T55W3CritRekeyLoop-receipts/{argv-replay.out, ritual-measure.out, run.sh}` | M | run.sh steps 9/10 lost (B3); ritual-measure keeps the original fixture rev |
| 34 | `waves/round-55/w3/T55W3SentReaders.md` | M | post-tip reviewer rewrite; branch bytes are what the round's record cites |

### 2.3 `after/c2.stdout` is the truncated original — confirmed at all three revisions

```
$ for r in fa48c06c 6efd2a1 981c5e8b; do git show $r:.ufo/evidence/round-55/after/c2.stdout | sha256sum; done
89e9e978068b9831396200209e605aaa3900151941d27fe1fcff7245c385814b  -   (x3, identical)
$ git show 981c5e8b:…/after/c2.stdout | wc -l          → 28
$ … | tail -1                                          → EXPLAIN usable repeat-control --selftest          rc=0  ok
$ … | grep -c 'C2_R55'                                 → 0
```
(receipt `08-c2stdout-truncated-original.txt`)

The discarded post-tip rewrite added 16 lines, ending in
`C2_R55: rev=4c04c1d33377 … total=0 C2_R55_PASS=true`. That line is gone from the tree, as it must be: it is
the closure's post-tip fabrication, not lane evidence (round-55 spot-check R55.7). Consequence for round 56:
the lane has **no committed C2 verdict at the revision round-55 certifies** — that is the round-55 defect, and
the revert neither caused nor cured it.

### 2.4 B1 (medium) — two committed receipts lost their only producer

At base `981c5e8b`, these receipts are committed:

```
09-reader-selection.txt   7639 B
11-c0-read-evidence.txt   1926 B
```

The committed `run-receipts.sh` produces neither:

```
$ git show 981c5e8b:…/T55W3SentReaders-receipts/run-receipts.sh | grep -n '09-reader-selection\|11-c0-read-evidence'
(no hits — its only tee target is 02-deliverable-audit.json, line 22)
$ git grep -n '09-reader-selection\|11-c0-read-evidence' 981c5e8b -- '*.sh' '*.py'
(no hits anywhere in the tree)
$ git ls-tree -r --name-only 981c5e8b | grep -E 'select\.py|read_evidence\.py'
.ufo/evidence/round-30/coldread/bind-select.py        (unrelated, round 30)
```

The version the sweep reverted **did** produce them (receipt `10-orphan-receipts-sentreaders.txt`):

```
$ git show 2dc8633a:…/run-receipts.sh | grep -n '09-reader-selection\|11-c0-read-evidence'
142:python3 "$S/select.py" "$LANE" "$C0" | tee "$R/09-reader-selection.txt"
164:python3 "$S/read_evidence.py" "$LANE" "$C0" | tee "$R/11-c0-read-evidence.txt"
```

The sweep committed the two outputs (untracked) and reverted the script section that names their command
(tracked). `select.py`/`read_evidence.py` lived in the seat's scratch and are gone, so the receipts now carry
**no producer at all** — not even a command line. This matters to this round directly: `11-c0-read-evidence.txt`
is the `seat | report | shows a git read of SKILL.md | names C0` table, i.e. round-55's attempt at exactly the
question C1 cannot see (does a reader actually read its section). If C1 or the lesson cites either receipt, the
only recorded producer is `2dc8633a:142/164`.

**Disposition proposed (not applied — the L1 integrates):** either re-run the two commands at the round-55 C0
from the `2dc8633a` heredocs into fresh receipts under a new name, or mark the two receipts
`PRODUCER-UNRECORDED` in the round-56 lesson's R55.6 row. Do not silently cite them.

### 2.5 B2 (medium) — the counter pin now contradicts its own directory

```
$ git show 981c5e8b:…/T55W1MutC2-receipts/counter-under-test.sha256
d6ca1d851bb0037368c304f4d80254f7dc5bf76b1c3119cdf0f2a64bca95631a  …/pristine-measure.py
$ git show 981c5e8b:…/T55W1MutC2-receipts/superseded-d6ca1d8/README.txt
… the scored set is ../mutants-133b2ce/, ../verdicts/, ../verdict-lines.txt and
  ../counter-under-test.sha256 (0458f632... at rev 133b2ce).
$ git show 981c5e8b:.ufo/waves/round-55/w1/T55W1MutC2.md | sed -n '12p'
| counter under test | `.ufo/evidence/round-55/c2/measure.py`, sha256 `0458f632…` = the bytes at rev `133b2ce…`
$ git show 981c5e8b:.ufo/evidence/round-55/freeze.json | grep c2/measure.py
  ".ufo/evidence/round-55/c2/measure.py": "0458f632087f665fbafc07efc6920d32febf7551d9fc5964d0c87fa0e139476b",
```
(receipt `09-counter-under-test-pin.txt`)

The committed pin names `d6ca1d85` — the pre-amendment first-pass counter the README says was abandoned and
"NOT scored". The seat's report and the freeze both name `0458f632` (the frozen `c2/measure.py` at `133b2ce`).
The post-tip working-tree value was `0458f632`, i.e. the one that agrees with the README and the report; the
revert restored the stale one. The mutation-test directory therefore ships a pin for a counter its own verdicts
were not produced with.

**Disposition proposed:** the pin is a receipt, not a claim input, so this does not touch round-55's claim
substance — but it must not be inherited as if consistent. Either correct the pin to `0458f632` in C0 (with the
README line as the receipt) or state in the round-56 lesson that the round-55 mutation-test pin is stale. Note
this is a *pre-existing* round-55 defect, not created by the sweep; the sweep merely removed the working-tree
correction.

### 2.6 B3 (low) — `run.sh` no longer reproduces two committed receipts

`T55W3CritRekeyLoop-receipts/adjudicator.out` (1608 B) and `recency.out` (2394 B) are committed; the base
`run.sh` ends at step 8, while the reverted version added:

```
say "9. the adjudicator built on top of the binder picks the quietest file"
say "10. the carried entry is not the newest by date (hash-order selection)"
```
(receipt `11-runsh-steps-9-10.txt`). `recency.py` *is* committed beside the receipts, so both are reconstructible
by hand; the reproducer simply no longer runs them. Low: same class as B1, one notch less severe because the
script survives.

### 2.7 Non-losses (checked, so the L1 need not re-check)

- `ritual-measure.out`: branch `fixture-rev=207447d2…`, discarded `fixture-rev=33497b69…`; both read
  `score 8 / covered 64 / 64 / box3 True`. The revert kept the fixture the committed report cites.
- `selftest-tally-audit-v2.out`: the discarded 7-line append ends `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`; the
  base file ends at `CASE harness position 8 skipped PASS`. No committed record cites `22/22` (the only
  `22/22` hits in the tree are round-18 cold-read trace filenames), so no claim depends on the missing tally.
- The discarded `T55W3SentReaders.md` revision carried a new finding **F6** ("one clean reader is unbindable:
  `w2/T55W3R16.json` has no `.md`"). The base tree does not corroborate it: `w2/T55W3R16.md` exists (16,955 B)
  and `w3/T55W3R16.md` exists (4,010 B). The loss is a discarded finding the bytes contradict, not verified
  signal. (Round 56's C1 should still be alert to a clean reader whose companion file is missing — the binder
  gate is real — but it cannot lean on F6 as evidence.)
- `09-c0-read-evidence.txt` (deleted in the working tree) is cited by the committed `T55W3SentReaders.md`;
  restoring it was required and happened.
- The 11 first-pass `T55W1MutC2-receipts` files deleted in the working tree are kept as tracked siblings by the
  seat's own README; restoring them was required and happened. `superseded-d6ca1d8/` correctly holds only
  `README.txt` (no duplicate bytes).

---

## 3. (c) Round-55 claim substance is intact at the round-55 evidence paths

```
$ git show 981c5e8b:.ufo/evidence/round-55/freeze.json   → 7 frozen files
$ python3 : sha256 of each listed path at 981c5e8b
OK       .ufo/evidence/round-55/contract.json
OK       .ufo/evidence/round-55/c1/measure.py
OK       .ufo/evidence/round-55/c2/measure.py
OK       .ufo/evidence/round-55/no-harm.sh
OK       .ufo/evidence/round-55/deciding-run.sh
OK       .ufo/evidence/round-55/controls.sh
OK       .ufo/evidence/round-55/c1/staged-at-freeze.txt
```
(receipt `12-round55-freeze-recompute.txt`) — **7/7 OK**, and `git diff fa48c06c 981c5e8b -- .ufo/evidence/round-55`
is empty (receipt `07`): no evidence file was edited, added or deleted by the sweep.

The evidence tree is complete at base: `contract.json`, `freeze.json`, `c1/{measure.py,lost-headings-at-c0.json,
staged-at-freeze.txt}`, `c2/measure.py`, `controls.sh`, `no-harm.sh`, `deciding-run.sh`,
`before/{c1,c2}.stdout`, `after/{c1,c2}.stdout`, `control/controls-a.stdout`, `assimilation/*`,
`integrate/{adjudicate.py,binder.py,resolutions.json}`.

Verdict lines as committed (receipt `13-round55-verdicts-and-controls.txt`):

```
before/c1.stdout      C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
after/c1.stdout       C1_R55: rev=4c04c1d33377 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
before/c2.stdout      C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false
control/controls-a    CTL_0_c1 / CTL_0_c2 / CTL_SKIP_c1 / CTL_FAB_c1 / CTL_SKIP_c2 (all false as designed); CONTROLS_A: 5/5 as pre-registered
after/c2.stdout       (no verdict line; truncated original, §2.3)
```

So the counter bytes, the contract, the controls and the C1 verdict at `4c04c1d33377` all survive; the only
missing round-55 verdict is C2's, which was never committed — the pre-existing R55.1/R55.5 defect.

---

## 4. Findings by severity

| id | sev | finding | evidence |
|---|---|---|---|
| B1 | medium | Sweep committed `09-reader-selection.txt` and `11-c0-read-evidence.txt` but reverted the only script section that produces them; their producer scripts were never committed. Two receipts now carry no command anywhere in the tree. | `10-orphan-receipts-sentreaders.txt` |
| B2 | medium | `counter-under-test.sha256` at base pins `d6ca1d85` while the sibling `superseded-d6ca1d8/README.txt`, `T55W1MutC2.md:12` and round-55 `freeze.json` all say the scored counter is `0458f632`. The revert restored the stale value. | `09-counter-under-test-pin.txt` |
| A1 | low | The round-start count "96 untracked files" is a porcelain entry count; 244 files were committed. The round's record must say 244 (or 96 entries → 244 files). | `03-porcelain-collapse-96.txt` |
| B3 | low | `T55W3CritRekeyLoop-receipts/run.sh` lost steps 9–10; `adjudicator.out`/`recency.out` are committed without a reproducer in the script. | `11-runsh-steps-9-10.txt` |
| A2 | low | `981c5e8b`'s message calls all nine files ">1 MiB monitor dumps"; `w3-results.json` is 209,693 B and is a results file. | `01-commits-and-tallies.txt` |
| A3 | info | The item's/L1's "23 tracked files reverted" is unsupported: the pre-revert snapshot carries 34 (17 M + 17 D), and the revert restored all 34. | `06-prerevert-34-delta.txt` |
| — | info | No added file is misrooted or another lane's deliverable; sibling-lane paths occur only as read paths inside monitor ledgers. | `05-content-scan-other-lanes.txt` |

No finding against round-55's claim substance: (c) is clean.

## 5. Residual risk and verification gaps

1. **Authorship is not proven.** Roster membership + artifact class + identity field is the strongest check git
   supports; a byte-identical copy of another lane's receipt placed under a round-55 seat directory would pass
   all three. No such copy was found, but the check is structural, not cryptographic.
2. **The jj op store is deeper than the exported snapshots.** 2,741 operations exist; only commits exported to
   `refs/jj/keep` are readable without invoking jj (which this seat is barred from). A rewrite that was never
   snapshotted would be invisible; the 15:04:06 snapshot is the last pre-revert state observed, and the 15:23:19
   snapshots show only the sweep's own intermediate trees, so nothing later than 15:04:06 can have been lost.
3. **The 23 is unexplained.** It is not 34, not 31 (the 15:01:57 snapshot), and not any count in the round-55
   record. If the L1's round-start notes carry 23, they should be corrected to 34 with this receipt, or the L1
   should name the source of 23 — the round-56 LOG will otherwise restate a number no receipt carries (R55.2's
   class).
4. **B1/B2 are corrections the sweep declined, not errors it introduced in claim inputs.** The round-55 C1/C2
   verdicts do not depend on either file; round 56 should record them as inherited defects, not as round-56
   work, unless C2's receipt-revision gate is pointed at them.
5. **`git status --porcelain` at base** names no path outside round 56: `git status --porcelain -- .ufo/evidence/round-55 .ufo/waves/round-55`
   is empty and `git status --porcelain | grep -v round-56` is empty, i.e. the round-55 dirt is genuinely closed
   — R55.6's disposition holds for the tracked tree.

## 6. Receipts (command → file)

| file | commands it holds |
|---|---|
| `01-commits-and-tallies.txt` | `git log -1 --format` and `git show --name-status/--stat` for `6efd2a1`, `981c5e8b` |
| `02-added-244-paths.txt` | the 244 added paths, sorted |
| `03-porcelain-collapse-96.txt` | 244 files → 96 porcelain entries |
| `04-seat-membership.txt` | added seat dirs vs round-55 spec-w1/w2/w3 |
| `05-content-scan-other-lanes.txt` | `git grep` for `/home/vgpnk/Projects/*` and `"lane":` fields |
| `06-prerevert-34-delta.txt` | `git diff --name-status/--numstat fa48c06c 2dc8633a` |
| `07-revert-no-diff-outside-wave.txt` | `git diff fa48c06c 981c5e8b -- . ':!.ufo/waves/round-55'` (empty) + tallies |
| `08-c2stdout-truncated-original.txt` | sha256/`wc -l`/`tail`/`grep -c` at three revs + the discarded rewrite diff |
| `09-counter-under-test-pin.txt` | pin diff, README, `T55W1MutC2.md:12`, freeze entry |
| `10-orphan-receipts-sentreaders.txt` | `run-receipts.sh` greps at both revs, producer lines, receipt sizes, script absence |
| `11-runsh-steps-9-10.txt` | `run.sh` steps at both revs, citations of the two receipts, `ritual-measure.out` diff |
| `12-round55-freeze-recompute.txt` | round-55 `freeze.json` + recomputed sha256 (7/7 OK) + evidence tree |
| `13-round55-verdicts-and-controls.txt` | the four committed verdict/control lines |
| `14-jj-snapshots.txt` | the sweep-window jj snapshots, parents, change-ids, per-snapshot tallies |
| `15-round55-tree-clean.txt` | `git status --porcelain` restricted to round-55 paths (empty) and unfiltered |

No lane production file and no frozen instrument was edited; no mutating git/jj command was run. No tool was
installed or upgraded.
