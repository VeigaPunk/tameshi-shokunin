# Residual seat — count audit of the round-41 report

seat: `L1Tameshi41.ResidualCounts` · role: reviewer · date 2026-10-25
lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, tip `812ee0d11d267e131be3dc8db0b71253cbae9234`,
measured commit `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6`, base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`.
Report read: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/tameshi.md`. Records read as committed
blobs (`git show 812ee0d:LOG.md`, `:SCORECARD.md`), because the worktree carried sibling edits while this
seat ran. Read-only: this file is the only write.

## Verdict table

| # | Number as reported | Verdict | Command (revision) |
|---|---|---|---|
| 1 | 40 seats in wave 1, "exactly one batched `task` call" | **AGREE** | `python3` over `dispatch-w1.json` / `spec-w1.json` / `w1/swarm-registry.json` @tip; `ls .ufo/waves/round-41/w1/*.md \| wc -l` |
| 2 | role mix connector 1, scout 6, executor 8, scribe 7, reviewer 10, critic 5, mutation-tester 3; "attack roles 18/40 = 45 %" | **AGREE** (all seven counts exact) | same registry command @tip |
| 3 | "Round total 48 seats, inside the 32–128 band" | **AGREE on the number and the band; the 8 residual seats have no committed artefact** (finding F2) | `git ls-tree --name-only 812ee0d .ufo/waves/round-41/`; `git ls-files \| grep round-41/residual`; `scripts/hyaku/lane-addendum.md:42,58` |
| 4 | registry 109 rows / 81 mined / 22 queued / 6 rejected at the tip | **AGREE** | `./scripts/sources-census.sh census --root … tameshi`; `git show 812ee0d:corpus/SOURCES.md` awk @tip |
| 5 | quote word counts 15 and 16 | **AGREE** (both labels equal the token count of the quoted sentence, and both sentences are present in the committed snapshots at the stated digests) | `python3` tokenizer + tag-strip over `.ufo/evidence/round-41/sources/{ast,pathlib}.html` @tip |
| 6 | depth 9 (command D) | **AGREE** at base, measured commit and tip | canonical command D @`a3d6c69`, `2ae00eb`, `812ee0d` |
| 7 | calibration 6 | **AGREE** at base, measured commit and tip; the same monitor run prints `depth_score 9` and `boxes 4 / checked 0 / asserted 4` | `python3 .ufo/evidence/round-21/coldread/measure.py --rev …` @`a3d6c69`, `2ae00eb`, `812ee0d` |
| 8 | `boxes=4 checked=0 asserted=4` | **AGREE** on the four values at all three revisions; the cited receipt is mislabelled and non-verbatim (finding F1) | canonical command C @`a3d6c69`, `2ae00eb`, `812ee0d` |

No number in scope is contradicted by the artefacts. One cited receipt does not carry the revision it is
cited for (F1), one total is half unevidenced (F2), one row count is not in the file it is cited against (F3).

## Commands and outputs

### 1–2. Seats, role mix, report presence (tip)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 -c "
import json,collections,os,re
d=json.load(open('.ufo/waves/round-41/w1/swarm-registry.json')); m=d['members']
c=collections.Counter(v['role'] for v in m.values()); print('ROLES',dict(sorted(c.items())),'sum',sum(c.values()))
files=[f[:-3] for f in os.listdir('.ufo/waves/round-41/w1') if f.endswith('.md')]
print('reports',len(files)); print('reg-only',sorted(set(m)-set(files)),'file-only',sorted(set(files)-set(m)))"
```

```
ROLES {'connector': 1, 'critic': 5, 'executor': 8, 'mutation-tester': 3, 'reviewer': 10, 'scout': 6, 'scribe': 7} sum 40
kinds Counter({'spawn': 40})
reports 40
in registry not reported []
reported not in registry []
name prefixes {'Connector': 1, 'Critic': 5, 'Exec': 8, 'Mut': 3, 'Review': 10, 'Scout': 6, 'Scribe': 7}
prefix/role mismatches []
attack roles 18 / 40 0.45
```

Cross-check that seats mean one dispatch and one report set:

```
python3 -c "… taskCall names vs spec items vs registry …"
40 40 40 40
taskCall==spec True spec==registry True registry==taskCall True
role in spec vs registry equal True
```
`dispatch-w1.json` (`counts`) → `{"spawn": 40, "resume": 0, "total": 40}`, `note` = "Issue exactly one
batched task call … never split a wave". Report sizes: 40 files, 495610 bytes, smallest `ExecC2Base.md`
3154 B, no empty file (`find … -size -20c` → no output). The registry holds no `planner` role, matching the
report's "the L1 holds the canonical planner seat".

### 3. Round total 48

```
git ls-tree --name-only 812ee0d .ufo/waves/round-41/
  .ufo/waves/round-41/assimilation
  .ufo/waves/round-41/dispatch-w1.json
  .ufo/waves/round-41/settlement-receipt.json
  .ufo/waves/round-41/settlement-receipt.stdout
  .ufo/waves/round-41/spec-w1.json
  .ufo/waves/round-41/w1
git ls-files | grep -i "round-41/residual"   → (no output)
git show 812ee0d:LOG.md | awk '/^## 2026-10-25 — round 41/{f=1} /^## /{if(f && !/round 41/) f=0} f' | grep -n residual
  → (no match; exit 1 — the committed round-41 section never says "residual", though LOG.md has 18 hits elsewhere)
```

40 is committed and countable; the second 8 exists only as report prose (`tameshi.md:44-46`). The shape rule
does not require a receipt: `scripts/hyaku/lane-addendum.md:58` — "Residual checks (… or leftovers after the
waves) go into one ordinary `task` call of ≤8 reviewer/critic seats, counted in the round total (≤128); say so
in the report." The round says so, and 8 ≤ 8, so the total 48 is compliant, not falsified. `:42` declares the
"32–128 seats in total" band; `dispatch-w1.json.policy` declares `waveMinLanes 32 / waveMaxLanes 64`, and 40
sits inside it. The band sentence is therefore true on the committed and declared artefacts:
48 ∈ [32,128].

### 4. Registry rows and statuses (tip)

```
cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi
tameshi	rows	109
tameshi	tier.A	97
tameshi	tier.B	9
tameshi	tier.C	3
tameshi	status.mined	81
tameshi	status.queued	22
tameshi	status.rejected	6
… FLEET rows 109 …
exit=0
```

Independent recount from the blob at each revision (status cell is field 9 of the 13-field pipe row,
`corpus/SOURCES.md:10` header: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`):

```
for R in 812ee0d a3d6c69; do git show $R:corpus/SOURCES.md | awk -F'|' 'NF==13 && $2 ~ /S[0-9]/ {s=$9; gsub(/^[ \t]+|[ \t]+$/,"",s); c[s]++; n++} END{…}'; done
== 812ee0d ==  mined=81 queued=22 rejected=6 rows=109
== a3d6c69 ==  mined=79 queued=22 rejected=6 rows=107
```

`git status --porcelain -- corpus/SOURCES.md` and `git diff --stat 812ee0d -- corpus/SOURCES.md` are both
empty, so the worktree file the census reads is the tip file. The round-21 monitor's own `sources` block
agrees at all three revisions (`mined 81, queued 22, rejected 6` at `2ae00eb` and `812ee0d`; `79/22/6` at
`a3d6c69`). The report's contextual base figures "79 mined / 22 queued / 6 rejected" (sum 107) and "107 rows"
also hold at `a3d6c69`.

### 5. Quote word counts 15 and 16

```
python3 - <<'EOF'   # tokenizer on the two sentences as printed at lessons/round-41.md:17,21
q1="The ast module helps Python applications to process trees of the Python abstract syntax grammar."
q2="Open the file pointed to in text mode, write data to it, and close the file:"
EOF
15 'The ast module helps Python ap'
16 'Open the file pointed to in te'
```

Located in the committed snapshots (tag-strip + entity unescape + whitespace fold, then substring test):

```
== ast.html ==      bytes 362029 sha256 183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317
                    quote_present True tokens 15
== pathlib.html ==  bytes 271189 sha256 0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093
                    quote_present True tokens 16
```

Both digests and both byte sizes equal the values written in `corpus/lessons/round-41.md:15-22`. The labels
read 15 and 16 in all three places that state them (lesson `:17`, `:21`; entry
`corpus/knowledge/r41-variable-destination-writes.md:12`, `:19`), and the lesson's own
`count-label-drift` row (`:75`) records the pre-fix labels 16/17 — the corrected values are the measured ones.

### 6. Depth 9

Canonical command D, verbatim from `SCORECARD.md:72-73`:

```
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
== 812ee0d11d267e131be3dc8db0b71253cbae9234 ==  recorded_cases=9 depth_score=9
== 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 ==  recorded_cases=9 depth_score=9
== a3d6c690bcbf8914551d4f4e8e1612784c1c2046 ==  recorded_cases=9 depth_score=9
```

`git diff --stat a3d6c69 812ee0d -- tools/mutate-and-run.sh` is empty, so 9 → 9 holds by construction as well
as by measurement: no ledger leg was added. The committed receipt `.ufo/evidence/round-41/census/command-d.stdout`
line 2 also reads `recorded_cases=9 depth_score=9`.

### 7. Calibration 6

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 .ufo/evidence/round-21/coldread/measure.py --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046 | grep -n "restraint\|depth_score\|asserted\|boxes\|checked"
2:  "calibration_restraint_score": 6,
1800:  "depth_score": 9,
1826:    "asserted": 4,
1830:    "boxes": 4,
1831:    "checked": 0,
-- and the same at 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 --
2:  "calibration_restraint_score": 6,
-- and at the tip 812ee0d11d267e131be3dc8db0b71253cbae9234 --
2:  "calibration_restraint_score": 6,
1800:  "depth_score": 9,
1826:    "asserted": 4,
1830:    "boxes": 4,
1831:    "checked": 0,
```
All three runs exit 0. The report's "prints `calibration_restraint_score: 6` at the base and at the round commit"
is reproduced. `SHONEN.md` is byte-identical base → tip (`git diff --stat a3d6c69 812ee0d -- SHONEN.md` empty),
so "No box was promoted this round" holds structurally.

### 8. `boxes=4 checked=0 asserted=4`

Canonical command C, verbatim from `SCORECARD.md:74-75`:

```
git show "$REV:SHONEN.md" | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" untouched="+str(m.count(" "))+" asserted_mark_upper_bound="+str(min(8,2*m.count("~"))))'
== 812ee0d ==  boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8
== 2ae00eb ==  boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8
== a3d6c69 ==  boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8
```

All four reported values reproduce at every revision.

## Findings

### F1 — MEDIUM: `census/command-d.stdout` is a `b37ce974` receipt cited as the measured-commit receipt, and its command-C line is not the canonical output

`head -2 .ufo/evidence/round-41/census/command-d.stdout`:

```
# command D at b37ce974b6efb8c465626d7346149549a3300a4b
recorded_cases=9 depth_score=9
boxes=4 checked=0 asserted=4 untouched=0
coldread score at a3d6c690 = 6
coldread score at b37ce974 = 6
```

Three records cite this single file for guardrails "at the measured commit"
`2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6`:

- report `tameshi.md:119` — "**Numeric guardrails at the measured commit** (`.ufo/evidence/round-41/census/command-d.stdout`)";
- `LOG.md:2168` (committed blob @tip) — "Command D at the measured commit: … and command C … both in `.ufo/evidence/round-41/census/command-d.stdout`";
- `SCORECARD.md:1928` (committed blob @tip) — "Receipts: `.ufo/evidence/round-41/census/command-d.stdout`".

Defects inside the file:

1. Its header names `b37ce974b6efb8c465626d7346149549a3300a4b`, not `2ae00eb…` — it is a pre-landing receipt
   re-cited as the measured-commit receipt.
2. Its command-C line stops at `untouched=0`. The canonical command at `SCORECARD.md:74-75` prints a sixth
   field; run at `b37ce974` it yields `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`
   (`SHONEN.md` is byte-identical `b37ce974` → `812ee0d`), so the receipt is a trimmed copy, not raw command
   output.
3. Its two coldread lines are `a3d6c690` and `b37ce974`, while `tameshi.md:121-123` reads them as "at the base
   and at the round commit". The round-commit value (6) is true — I measured it at `2ae00eb` — but this file
   does not evidence it.

Impact on the audited numbers: none — I reproduced command D 9/9 and command C 4/0/4 at all three revisions,
so the values are revision-invariant. The defect is citation fidelity: a reader following the report's
pointer lands on a receipt that cannot support the label it is given. Repair: re-run C and D at `2ae00eb`
(the tip) and store the untrimmed output, or drop "at the measured commit" from the three citations.

### F2 — LOW: the residual 8 seats of the round total exist only as report prose

No committed artefact enumerates them: `git ls-tree --name-only 812ee0d .ufo/waves/round-41/` lists only
`assimilation/`, `dispatch-w1.json`, `settlement-receipt.{json,stdout}`, `spec-w1.json`, `w1/`;
`git ls-files | grep round-41/residual` is empty; the committed round-41 LOG section and the committed
`SCORECARD.md` Round 41 sections (`:1895-1986`, 0 `grep -c residual`) never mention the residual call — the
`residual` lines in `SCORECARD.md` at `:690 :721 :1173 :1371 :1376 :1687 :1720 :1769 :1830 :1843` all belong to
earlier rounds. `settlement-receipt.json` covers wave 1 only (`registry_members 40`), so the 48 is
40 evidenced + 8 asserted. This is inside the addendum's own requirement ("say so in the report"), so I do not
call the number wrong — but a successor seat cannot recompute 48 from the lane. Repair: commit the residual
call's seat list (8 names with roles) beside `dispatch-w1.json`.

### F3 — LOW: "107 rows" is cited against a receipt that prints no row count

Report `§Sources` — "Round start: exit 0, 107 rows, 9 × W04 + 1 × W01, zero E codes
(`.ufo/evidence/round-41/census/start.stdout`)". `start.stdout` in `validate` mode prints exactly the ten
warning lines and the `ok` line:

```
tameshi	W04	S047 … | S048 | S075 | S076 | S077 | S078 | S081 | S092 | W01 S101 | W04 S104
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

— nine W04 and one W01 as stated, exit 0 (`.exit` = `0`), but no `rows` field. The 107 itself is true
(`git show a3d6c69:corpus/SOURCES.md` → 107 rows); the citation is incomplete, not false. The census `census`
mode is the command that prints rows (item 4 above). `end.stdout` likewise matches its 109-row claim by the
same accounting.

## Residual risk

- The lane worktree was dirty during this audit: `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-41.md`,
  `.ufo/waves/round-41/w1/ReviewScorecardNumbers.md` and `ScribeScorecard.md` modified, plus an untracked
  `.ufo/waves/round-41/residual/`. Every record sentence I quote was taken from the committed blob at
  `812ee0d`, and every number was recomputed from `git show <rev>:…` where the file is revision-addressable.
  A sibling is appending to the same records, so the line numbers cited here may shift.
- `command-d.stdout` is the only committed guardrail receipt; my C/D replays are not committed. If the
  replayed values ever diverge from that file, nothing in the lane would notice (F1's repair closes this).
- Rows 4's tip reading trusts that `corpus/SOURCES.md` has no worktree edit; I checked that directly
  (`git diff --stat 812ee0d -- corpus/SOURCES.md` empty), and the same check would have to be repeated for any
  later audit that reads the census instead of the blob.

## Verification gaps

- None of the eight numbers is unverifiable except the half of item 3 noted in F2: the 8 residual seats have
  no committed registry, spec or receipt, and the hub session log is not a committed lane artefact.
- I did not run the two round counters (`.ufo/evidence/round-41/{calibration,census}/measure.py`); C1/C2
  predicate agreement is another seat's scope (`ResidualReplayC1`, `ResidualReplayC2`). The coldread monitor
  and commands C and D were run, at the three revisions named per item.
- Tool installs this round: none (nothing was needed; pacman is paused host-wide and was not invoked).

## Recommendation

The eight audited numbers stand as reported. F1 is the one item worth closing before the round is read as
receipted: the guardrail receipt must either be regenerated at `2ae00eb` untrimmed or the three "at the
measured commit" citations reworded. F2 and F3 are evidence hygiene that cost one commit each.
