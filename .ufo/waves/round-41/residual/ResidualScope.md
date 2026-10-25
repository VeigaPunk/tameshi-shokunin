# ResidualScope — path scope of the landed round-41 diff

Seat: residual reviewer (scope). Read-only; the only write is this file.

Revisions used in every command below:

| label | revision |
|---|---|
| base | `a3d6c690bcbf8914551d4f4e8e1612784c1c2046` |
| measured | `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6` |
| tip | `812ee0d11d267e131be3dc8db0b71253cbae9234` |

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (detached HEAD at tip; `master`
contains tip — the prompt states detached HEAD is the expected state after the first helper
commit, so this is not a finding). Fleet repo: `/home/vgpnk/Projects/shokunin`.

Nothing was installed; no tool was upgraded.

---

## 1. Changed-path classification

```
$ git -C …/tameshi-shokunin diff --stat a3d6c69 812ee0d
89 files changed, 16327 insertions(+), 3 deletions(-)
$ git -C …/tameshi-shokunin diff --name-status a3d6c69 812ee0d | cut -f1 | sort | uniq -c
     84 A
      5 M
```

Every changed path is relative to the lane root; **no path in the diff resolves outside the
lane's own tree**:

```
$ git diff --name-only a3d6c69 812ee0d | grep -vE '^(\.ufo/|corpus/|tools/|LOG\.md$|SCORECARD\.md$)'
(no output)
$ git diff --numstat a3d6c69 812ee0d | awk '$1=="-"{print "BINARY",$3}'
(no output)
# symlink scan over the changed set: no output
```

| # | group | files | class | disposition |
|---|---|---|---|---|
| 1 | `.ufo/evidence/round-41/after/` | 14 | added receipts (C1/C2 at `baa18b7b`, `2ae00eb7`, `b37ce974`) | **in scope** (lane evidence; replays below match byte-for-byte) |
| 2 | `.ufo/evidence/round-41/before/` | 6 | added receipts (C1/C2 at base) | **in scope** (replay matches) |
| 3 | `.ufo/evidence/round-41/control/` | 2 | added receipt (`--control`, exit 1) | **in scope** (replay matches) |
| 4 | `.ufo/evidence/round-41/census/` | 7 | counter `measure.py`, `fixtures.json`, command-D, start/end receipts | **in scope**; start/end pair is defective, see F4 |
| 5 | `.ufo/evidence/round-41/calibration/` | 1 | counter `measure.py` | **in scope** |
| 6 | `.ufo/evidence/round-41/sources/` | 2 | `ast.html`, `pathlib.html` snapshots | **in scope**; vendored CPython docs, precedent: 9 HTML snapshots already tracked (`kaika-round-1/score-semantics`, `round-29/sources`, `round-33/c2`, `round-34/src`) |
| 7 | `.ufo/evidence/round-41/contract.json` | 1 | freeze contract + A1–A5 | **in scope**; all four pins match the bytes, P4 |
| 8 | `.ufo/waves/round-41/w1/` | 41 | 40 seat reports + `swarm-registry.json` | **in scope**; count = registry `members` (40) = settlement receipt `reports_present` (40) |
| 9 | `.ufo/waves/round-41/` (top) | 4 | `spec-w1.json`, `dispatch-w1.json`, `settlement-receipt.json`, `.stdout` | **in scope**; the only absolute path they carry outside the lane is the read-only prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-41.md` (3 hits, no write) |
| 10 | `.ufo/waves/round-41/assimilation/` | 3 | scratch id lists (`collisions`, `reg-ids`, `staged-ids`) | **in scope**; bare S-ids only (0 lines containing `/`) |
| 11 | `corpus/QUALITY.md`, `corpus/README.md` | 2 | append-only additions at EOF (criterion 80; round-41 row) | **in scope** |
| 12 | `corpus/SOURCES.md` | 1 | +7/−1: S153, S154 rows + round-41 block | **in scope**; the one deletion is a `- ` bullet replaced by its expanded form (`git diff -U0`, hunk `@@ -…`), not a row rewrite |
| 13 | `corpus/knowledge/r41-variable-destination-writes.md`, `corpus/lessons/round-41.md` | 2 | new entry + lesson | **in scope** |
| 14 | `tools/write-path-census-v3.py` | 1 | new counter tool (346 L) | **in scope**; `tools/` holds 10 pre-existing tools; sha256 matches the LOG pin `095924a7…` and the contract `claims.C2.tool_sha256` |
| 15 | `SCORECARD.md` | 1 | +94/−1: round-41 capability row appended; the `sources-registry` standing cell restated 103 → 109 rows | **in scope**; the in-place cell edit is the C1 `m6` fix the claim names, and SCORECARD row edits have precedent (rounds 1, 2, 33, 35 each deleted one line) |
| 16 | `LOG.md` | 1 | +95/−2 | **suspicious** — see F2: the two deletions are prior-round entries |

**Out of scope inside the diff: none.** **Suspicious: 1 file (`LOG.md`), 2 lines.**

Complete list (classification = the group number above):

```
.ufo/evidence/round-41/after/c1-at-2ae00eb7.exit                      1
.ufo/evidence/round-41/after/c1-at-2ae00eb7.stdout                    1
.ufo/evidence/round-41/after/c1-at-b37ce974b6ef…a3300a4b.exit         1
.ufo/evidence/round-41/after/c1-at-b37ce974b6ef…a3300a4b.stderr       1
.ufo/evidence/round-41/after/c1-at-b37ce974b6ef…a3300a4b.stdout       1
.ufo/evidence/round-41/after/c1-at-baa18b7b.exit                      1
.ufo/evidence/round-41/after/c1-at-baa18b7b.stdout                    1
.ufo/evidence/round-41/after/c2-at-2ae00eb7.exit                      1
.ufo/evidence/round-41/after/c2-at-2ae00eb7.stdout                    1
.ufo/evidence/round-41/after/c2-at-b37ce974b6ef…a3300a4b.exit         1
.ufo/evidence/round-41/after/c2-at-b37ce974b6ef…a3300a4b.stderr       1
.ufo/evidence/round-41/after/c2-at-b37ce974b6ef…a3300a4b.stdout       1
.ufo/evidence/round-41/after/c2-at-baa18b7b.exit                      1
.ufo/evidence/round-41/after/c2-at-baa18b7b.stdout                    1
.ufo/evidence/round-41/before/c1-at-base.exit                         2
.ufo/evidence/round-41/before/c1-at-base.stderr                       2
.ufo/evidence/round-41/before/c1-at-base.stdout                       2
.ufo/evidence/round-41/before/c2-at-base.exit                         2
.ufo/evidence/round-41/before/c2-at-base.stderr                       2
.ufo/evidence/round-41/before/c2-at-base.stdout                       2
.ufo/evidence/round-41/control/c2-control.exit                        3
.ufo/evidence/round-41/control/c2-control.stdout                      3
.ufo/evidence/round-41/census/command-d.stdout                        4
.ufo/evidence/round-41/census/end.exit                                4
.ufo/evidence/round-41/census/end.stdout                              4
.ufo/evidence/round-41/census/fixtures.json                           4
.ufo/evidence/round-41/census/measure.py                              4
.ufo/evidence/round-41/census/start.exit                              4
.ufo/evidence/round-41/census/start.stdout                            4
.ufo/evidence/round-41/calibration/measure.py                         5
.ufo/evidence/round-41/sources/ast.html                               6
.ufo/evidence/round-41/sources/pathlib.html                           6
.ufo/evidence/round-41/contract.json                                  7
.ufo/waves/round-41/w1/ConnectorSibling.md                            8
.ufo/waves/round-41/w1/CriticAxisName.md                              8
.ufo/waves/round-41/w1/CriticCausalSeparability.md                    8
.ufo/waves/round-41/w1/CriticCrossClaim.md                            8
.ufo/waves/round-41/w1/CriticR40Discharge.md                          8
.ufo/waves/round-41/w1/CriticUniversal.md                             8
.ufo/waves/round-41/w1/ExecC1Base.md                                  8
.ufo/waves/round-41/w1/ExecC2Base.md                                  8
.ufo/waves/round-41/w1/ExecC2Control.md                               8
.ufo/waves/round-41/w1/ExecCensusStart.md                             8
.ufo/waves/round-41/w1/ExecQuarantine.md                              8
.ufo/waves/round-41/w1/ExecRowFormat.md                               8
.ufo/waves/round-41/w1/ExecScratchValidate.md                         8
.ufo/waves/round-41/w1/ExecV3Selftest.md                              8
.ufo/waves/round-41/w1/MutC1Parse.md                                  8
.ufo/waves/round-41/w1/MutConstantClassifier.md                       8
.ufo/waves/round-41/w1/MutFixtureVar.md                               8
.ufo/waves/round-41/w1/ReviewC1Counter.md                             8
.ufo/waves/round-41/w1/ReviewC1DoNothing.md                           8
.ufo/waves/round-41/w1/ReviewC2Predicate.md                           8
.ufo/waves/round-41/w1/ReviewIdLists.md                               8
.ufo/waves/round-41/w1/ReviewLiveSite.md                              8
.ufo/waves/round-41/w1/ReviewScorecardNumbers.md                      8
.ufo/waves/round-41/w1/ReviewScribeEntry.md                           8
.ufo/waves/round-41/w1/ReviewSourceRows.md                            8
.ufo/waves/round-41/w1/ReviewV3Scope.md                               8
.ufo/waves/round-41/w1/ReviewWordLabelled.md                          8
.ufo/waves/round-41/w1/ScoutAstDocs.md                                8
.ufo/waves/round-41/w1/ScoutLiveCensus.md                             8
.ufo/waves/round-41/w1/ScoutMisroot.md                                8
.ufo/waves/round-41/w1/ScoutPathlibDocs.md                            8
.ufo/waves/round-41/w1/ScoutRegistry.md                               8
.ufo/waves/round-41/w1/ScoutV2Miss.md                                 8
.ufo/waves/round-41/w1/ScribeEntry.md                                 8
.ufo/waves/round-41/w1/ScribeLesson.md                                8
.ufo/waves/round-41/w1/ScribeLog.md                                   8
.ufo/waves/round-41/w1/ScribeQuality.md                               8
.ufo/waves/round-41/w1/ScribeReadme.md                                8
.ufo/waves/round-41/w1/ScribeScorecard.md                             8
.ufo/waves/round-41/w1/ScribeSources.md                               8
.ufo/waves/round-41/w1/swarm-registry.json                            8
.ufo/waves/round-41/dispatch-w1.json                                  9
.ufo/waves/round-41/settlement-receipt.json                           9
.ufo/waves/round-41/settlement-receipt.stdout                         9
.ufo/waves/round-41/spec-w1.json                                      9
.ufo/waves/round-41/assimilation/collisions                           10
.ufo/waves/round-41/assimilation/reg-ids                              10
.ufo/waves/round-41/assimilation/staged-ids                           10
corpus/QUALITY.md                                                     11
corpus/README.md                                                      11
corpus/SOURCES.md                                                     12
corpus/knowledge/r41-variable-destination-writes.md                   13
corpus/lessons/round-41.md                                            13
tools/write-path-census-v3.py                                         14
SCORECARD.md                                                          15
LOG.md                                                                16
```

Sibling-lane write check over the changed wave files (a read-only sibling sweep is
expected; a write is not):

```
$ grep -rnE '(>|>>|rm |mv |sed -i|cp )[^|]*/home/vgpnk/Projects/shokunin/(souji|kagi|kengaku|kake|mado|kasegi|kama|mori|chousa|kaidoku|kumitate|tsukuroi|kotoba|kotodama|revenger)' .ufo/waves/round-41/
(no output; exit 1)
$ grep -rl '/home/vgpnk/Projects/shokunin/' .ufo/waves/round-41/ | wc -l
34          # all read references (lane self-paths, prompt path)
```

`ConnectorSibling.md:3` states the scope: "Read-only. No sibling byte was edited; the only
write is this file."

---

## 2. Fleet-repo untracked writes

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 D .scratch/battery.out                                   … (13 tracked .scratch deletions)
 M .ufo/reports/round-22/souji.md
 M .ufo/state/{chousa,kagi,kaidoku,kake,kama,kengaku,kumitate,mado,mori,souji,tameshi,tsukuroi}.report-baseline
 M .ufo/watchdog.log
 M scripts/hyaku/hyaku.env
 M scripts/hyaku/lane-addendum.md
?? .omp/mcp.json
?? .ufo/reports/round-41/tameshi.md
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
```

Untracked files whose content names tameshi **and** round 41 — exactly one:

| path | size / mtime | content evidence |
|---|---|---|
| `.ufo/reports/round-41/tameshi.md` | 16762 B, 244 lines, `2026-10-25 03:57:23` | line 1 `# tameshi — round 41`; line 3 `lane: tameshi-shokunin · round: 41 · attempt 2 · date: 2026-10-25` |

```
$ grep -niE 'tameshi|round.?41|r41' .ufo/reports/round-41/tameshi.md | head -3
1:# tameshi — round 41
3:lane: tameshi-shokunin · round: 41 · attempt 2 · date: 2026-10-25
18:  `.ufo/evidence/round-41/calibration/measure.py`, …
```

The other untracked entries do not: `.omp/mcp.json` (11 lines, operator harness `rea` MCP
entry, `enabled:false`), and the three new `.report-baseline` files (one line each,
`<round> e3b0c442…b855`, rounds 68/69/68). A scan including ignored paths finds nothing else:

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --ignored=matching | grep -i 'round-41\|r41'
?? .ufo/reports/round-41/tameshi.md
```

Nothing was deleted by this seat.

---

## 3. Findings

### F1 — DEFECT (high): the round-41 tameshi report never landed in the fleet repo

Evidence — the prompt makes the fleet commit mandatory and last (`prompt:323-328`: "Fleet-repo
commits stay on git, only through the serialized helper, which pushes origin: … The report lands
last and cites the pushed lane hash"), yet the file is untracked and absent from fleet HEAD:

```
$ git -C /home/vgpnk/Projects/shokunin cat-file -e HEAD:.ufo/reports/round-41/tameshi.md
fatal: path '.ufo/reports/round-41/tameshi.md' exists on disk, but not in 'HEAD'
$ git -C /home/vgpnk/Projects/shokunin log --oneline -8 -- .ufo/reports/round-41
65cf5b73 round-41: mori report
b0b681d5 round-41: report erratum — committed-tip vs pinned-revision counter scope
a54d40c8 round-41: chousa report + l0 question
0122b211 round-41: kake report
1914377d round-41: kumitate report (attempt 2; lane fb7046ca)
31baf5cb fleet backlog commit: rounds 33-42 .ufo/kotodama reports + …
```

Four sibling lanes' round-41 reports are committed; tameshi's is the only one left on disk.
The report's mtime (`03:57:23`) is 61 s after the lane tip (`03:56:22`), so it was written
after the landing that it cites and was never swept.

### F2 — DEFECT (medium): the round-41 commits rewrote two prior-round LOG entries in place

```
$ git -C …/tameshi-shokunin diff -U0 a3d6c69 812ee0d -- LOG.md
@@ -2069 +2069,10 @@
-- Command D at the measured commit: `recorded_cases=9 depth_score=9`. No axis harmed.
+- Command D at the measured commit: `recorded_cases=9 depth_score=9` and command C `boxes=4
+  checked=0 asserted=4 untouched=0`, both in `.ufo/evidence/round-41/census/command-d.stdout`; …
+- Receipts after the deciding runs: `.ufo/evidence/round-41/after/` … (9 more lines)
@@ -2079 +2088,10 @@
      (the same 10 lines, byte-identical: verified programmatically, `block0 == block1: True`)
```

Both deleted lines sit in **prior** rounds' sections — base `LOG.md:2061` is
`## 2026-10-24 — round 39` and `LOG.md:2071` is `## 2026-10-24 — round 40` — and each is
replaced by an identical block of round-41 receipt prose. The round-41 LOG block and the
contract's `amendments` (A1–A5: counter parsers, fixtures, lesson text) declare no LOG edit,
so the change is unannounced:

```
$ for c in $(git log --format=%h -- LOG.md); do d=$(git show --numstat --format= $c -- LOG.md | awk '{print $2}' | head -1); [ "${d:-0}" -gt 0 ] && echo "$c del=$d"; done
baa18b7 del=4
$ git log --format=%h -- LOG.md | wc -l
90
```

Across 90 commits touching `LOG.md`, `baa18b7` (round 41) is the only commit that ever
deletes lines in it. `SCORECARD.md` has such precedent (rounds 1, 2, 33, 35), so the
standing-cell edit at `SCORECARD.md` is routine; the LOG rewrite is not. Two effects a
reader cannot undo: the round-39/40 entries now cite round-41 receipts, and the original
"No axis harmed." sentence is gone from both.

### F3 — DEFECT (medium): two lane wave files are dirty after the landed tip, unlanded and unnamed

```
$ git -C …/tameshi-shokunin status --porcelain
 M .ufo/waves/round-41/w1/ReviewScorecardNumbers.md
 M .ufo/waves/round-41/w1/ScribeScorecard.md
?? .ufo/waves/round-41/residual/          # this residual wave's own dir, not the landed round

$ git log -1 --format='%ci'   → 2026-10-25 03:56:22   (HEAD = tip 812ee0d)
$ stat -c '%y' .ufo/waves/round-41/w1/ScribeScorecard.md        → 04:00:17
$ stat -c '%y' .ufo/waves/round-41/w1/ReviewScorecardNumbers.md → 04:00:40
```

Both edits are seat closure addenda that name the tip (`"## Closure (added after the
reviewer's re-check; tip `812ee0d`)"`, `"Addendum — re-check after the deciding run
(`b37ce97` → `2ae00eb`)"`), written 3–4 minutes after the last commit. The prompt's inherited-
state rule (`prompt:329-331`: uncommitted lane-authored leftovers must be committed under
this round's entry or reverted, and named in the report) is unmet in both halves: they are
neither committed nor reverted, and the report — mtime `03:57:23`, i.e. *before* both writes —
cannot name them (`grep -n "ReviewScorecardNumbers\|ScribeScorecard\|addendum" .ufo/reports/
round-41/tameshi.md` → no output). The landed tip therefore does not contain the closure text
of two of its own seats.

### F4 — DEFECT (low): the census start/end receipts are byte-identical and carry no row count

```
$ wc -c .ufo/evidence/round-41/census/start.stdout .ufo/evidence/round-41/census/end.stdout
1015 …/start.stdout
1015 …/end.stdout
$ diff -u .ufo/evidence/round-41/census/start.stdout .ufo/evidence/round-41/census/end.stdout && echo start==end
start==end
$ cat .ufo/evidence/round-41/census/start.exit .ufo/evidence/round-41/census/end.exit
0
0
```

The claim in `SOURCES.md`/`LOG.md` — "exit 0 at round start (107 rows …) and exit 0 at round
end (109 rows, same warning set)" — is *true* but not receipted: `scripts/sources-census.sh
validate` prints only the warning matrix and an `ok` line, never a count, so the two committed
files cannot distinguish 107 rows from 109. The counts themselves are independently true:

```
$ git show a3d6c69:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|'   → 107
$ grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' corpus/SOURCES.md                      → 109
```

A verifier reading only the receipts sees one state, not a delta.

### F5 — DEFECT (low): the tameshi report baseline digest is the empty-content digest

```
$ git -C /home/vgpnk/Projects/shokunin diff -- .ufo/state/tameshi.report-baseline
-23 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
+41 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

`e3b0c442…b855` is sha256 of zero bytes, while `.ufo/reports/round-41/tameshi.md` is 16762 B.
The round counter advanced to 41, the digest did not. The same empty digest appears for
`kagi` (28), `kotoba` (68), `kotodama` (69) and `revenger` (68), and `souji` (22) carries a
real digest, so the convention is not stated anywhere I can read; attribution to round 41 is
therefore unresolved, and I record it as an observation that the baseline cannot detect report
content at round 41 — not as a lane-41 write I can source.

### PASS items (commands and outputs)

P1 — all 89 changed paths live inside the lane tree; no binaries, no symlinks, no fleet-root
or operator path in the diff (section 1 commands, empty outputs).

P2 — the counters are byte-identical at the measured commit and at the tip, so a replay runs
the landed bytes:

```
$ for rev in a3d6c69 2ae00eb 812ee0d; do printf '%s ' $rev; git show $rev:.ufo/evidence/round-41/calibration/measure.py | sha256sum | cut -c1-16; done
a3d6c69 e3b0c44298fc1c14   # absent (hash of empty stdin)
2ae00eb 9aaa99ac5a5abd16
812ee0d 9aaa99ac5a5abd16
# census:  2ae00eb 83268eff97048cd4 · 812ee0d 83268eff97048cd4
# v3 tool: 2ae00eb 095924a7a165be96 · 812ee0d 095924a7a165be96
```

P3 — every replay reproduces its committed receipt. Commands (revision stated per run):

```
$ python3 .ufo/evidence/round-41/calibration/measure.py --lane … --rev 2ae00eb
C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=2ae00eb… C1_R41_PASS=true   exit 0
  | diff -u .ufo/evidence/round-41/after/c1-at-2ae00eb7.stdout -  → MATCH
$ … --rev 812ee0d
C1_R41: … rev=812ee0d1… C1_R41_PASS=true   exit 0
$ … --rev a3d6c69
MISMATCH m6 SCORECARD standing row says 103 rows, SOURCES.md has 107
MISMATCH m9 round-40 quarantine summary says (1, 7, 9), its table counts (1, 6, 10) (no round-41 correction)
C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 … C1_R41_PASS=false   exit 1
  | diff -u .ufo/evidence/round-41/before/c1-at-base.stdout -  → MATCH
$ python3 .ufo/evidence/round-41/census/measure.py --lane … --rev 2ae00eb
C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 … mutant_symlink_arg_killed=1 C2_R41_PASS=true  exit 0
  | diff -u .ufo/evidence/round-41/after/c2-at-2ae00eb7.stdout -  → MATCH
$ … --rev 812ee0d   → C2_R41_PASS=true, exit 0 (only `rev=` differs from the measured receipt)
$ … --control      → C2_R41_CONTROL: … C2_R41_CONTROL_PASS=false, exit 1  = committed control receipts
$ python3 .ufo/evidence/round-41/census/measure.py … --rev a3d6c69
C2_R41: tool_absent=1 var_expected=0 symlink_expected=0 rev=a3d6c69… C2_R41_PASS=false  exit 1 = before receipt
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
exit 0; 9 × W04 + 1 × W01 warnings, `tameshi ok …/corpus/SOURCES.md`; byte-identical to census/end.stdout
$ python3 tools/write-path-census-v3.py --selftest
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0   exit 0
```

P4 — the contract's four pins match the committed bytes, and `v2_sha256` correctly addresses
`tools/write-path-census-v2.py` (a distinct file from `tools/write-path-census.py`), so there
is no pin drift behind the `v2_sha_ok=1`:

```
contract claims.C1.counter_sha256 = 9aaa99ac…  = sha256 .ufo/evidence/round-41/calibration/measure.py
contract claims.C2.counter_sha256 = 83268eff…  = sha256 .ufo/evidence/round-41/census/measure.py
contract claims.C2.tool_sha256    = 095924a7…  = sha256 tools/write-path-census-v3.py
contract claims.C2.fixtures_sha256= 20b6254d…  = sha256 .ufo/evidence/round-41/census/fixtures.json
contract claims.C2.v2_sha256      = 4022853…   = sha256 tools/write-path-census-v2.py
tools/write-path-census.py        = bc8c660c…   (unchanged since base; the round-39 pin)
```

P5 — the two source snapshots are the bytes their registry rows cite:

```
$ stat -c '%s' .ufo/evidence/round-41/sources/ast.html .ufo/evidence/round-41/sources/pathlib.html
362029
271189          # SOURCES.md S153/S154 claim 362029 B / 271189 B
$ sha256sum …/ast.html …/pathlib.html | cut -c1-12
183a4f8c3d59    # S153 sha256 183a4f8c…
0044cae699c5    # S154 sha256 0044cae6…
```

P6 — wave-file accounting is internally consistent: 40 `w1/*.md` = registry `members` (40) =
`settlement-receipt.json.reports_present` (40). The receipt's `tool_verdict: UNSETTLED` is a
written classification, not a silent pass.

P7 — no sibling lane was written from this lane; the only absolute paths in the wave package
point at the read-only prompt file (section 1 greps).

---

## 4. Residual risk and verification gaps

- **F1 is the load-bearing one.** The round's only durable artifact outside the lane is still
  a working-tree file. Until `fleet-commit.sh --as tameshi -m "round-41: tameshi report" --
  .ufo/reports/round-41/tameshi.md` runs, the report can be lost by any fleet-repo checkout,
  and the "report lands last and cites the pushed lane hash" requirement is unmet.
- **F2 needs a policy answer, not a code fix**: either the round-41 stanza is moved into its
  own section (restoring the round-39/40 bullets) or the edit is declared as an erratum in
  `QUALITY.md`-style form. I did not edit — this seat is read-only.
- **F3's closure text is unlanded prose**; a later round that commits it will silently attach
  post-hoc seat findings to a landed tip.
- I did not re-derive the *content* of the 40 seat reports, the lesson's claims, the scorecard
  numbers, or the coldread score (`6` in `command-d.stdout`) — those belong to the sibling
  residual seats. My evidence bounds the *paths* and the counter/receipt fidelity.
- `@`-prefixed or abbreviated revs were never used: every counter run received a full 40-hex
  revision, and `--control` runs carry no revision by design.
- Fleet-repo `.scratch/*` deletions, `.ufo/watchdog.log`, `scripts/hyaku/*` and the twelve
  modified baselines are *ambient* fleet state with no round-41 tameshi content in the diff
  hunks I read (`git diff -- .scratch` = 13 whole-file deletions of operator goal scratch). I
  could not attribute them to this lane; I name them rather than edit them.
