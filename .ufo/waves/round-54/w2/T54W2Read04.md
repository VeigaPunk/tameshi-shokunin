# T54W2Read04 — cold read at C1

**Seat:** T54W2Read04 (reader, round 54 wave 2; leaf member, no subagent dispatch).
**Section:** `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`
**Candidate:** `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
**Span:** start 932, end 945 → **13 lines / 1105 bytes**, `section_sha256` = `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993` (matches `reader-section.py`).

Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku`; tree `/fast/scratch/hyaku/tameshi-r54/T54W2Read04/`; `TMPDIR` set to that tree. No lane production file, counter, contract, freeze, ledger or wave spec was modified; no git/jj mutation was run anywhere (`git show`/`git log`/`rev-parse`/`cat-file`/`merge-base --is-ancestor` only).

## Findings

### 1. Dated-milestone chain starts at seven, so the four→seven jump is undated

**Quote (byte-exact substring of the section):**

```
dated milestones: seven from round 16, eight from round 18, nine from
round 26, ten from round 51
```

**Why:** the parenthetical reads as *the* dated milestone chain of the leg count, yet it begins at seven — the sentence has just said "Round 7 recorded four legs at r7-1", so the reader is left without the date of the fifth/sixth legs and cannot reconcile four with seven; the runner the paragraph itself cites carries the missing stage.

**Receipt — the milestone chain in the cited artifact:**

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ git show 99c3bc88d704:tools/mutate-and-run.sh | sed -n '84p'
# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten) — the fleet's
```

**Receipt — six legs at the r10-2 revision named by that header:**

```
$ git show 606716f:tools/mutate-and-run.sh | grep -n "^VERSION="
157:VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'
$ git show 606716f:tools/mutate-and-run.sh | grep -cE '^  regression_case_git (js|bash)-'
6
$ git log -1 --format='%h %ad %s' --date=short 606716f
606716f 2026-10-14 probation round 10 (training r9): see LOG
```

**Receipt — the same six-leg state dated elsewhere in the same SKILL.md:**

```
$ sed -n '1328p' SKILL.md    # (C1 blob of SKILL.md)
uncommitted worktree file at this write), `--regression` replays **six** in r10-2 (**ten** since round 51)
```

**Verdict:** genuine (one finding). Every milestone that *is* listed resolves, so the listed cells are not stale; the defect is the missing `r10-2 six legs` stage the cited runner records, which makes the enumeration read as complete while skipping one dated step.

**Defence against the "it is only a partial list" reading:** the text is labelled "dated milestones", is the only dating the section gives for leg growth, and the immediately preceding clause names the four-leg state — so the list is what a cold reader uses to date the count. `SKILL.md:1328` and `tools/mutate-and-run.sh:84` both date six to r10-2, so the chain as printed contradicts the artifact it cites.

## What resolved clean (evidence, so the finding is not padded)

| Claim in the section | Check | Result |
|---|---|---|
| "`--regression` from the tool's two-case self-check" | `git show 9f1d3c3^:tools/mutate-and-run.sh` header: "`--regression (r4-2) — this tool's own gate: re-runs BOTH worked cases`"; `grep -c '^  regression_case'` = 2 pre-r7-1 | holds |
| "Round 7 recorded four legs at r7-1" | `git show 9f1d3c3:tools/mutate-and-run.sh` → `VERSION='mutate-and-run.sh r7-1 …'`, `grep -cE '^  regression_case_git (js|bash)-'` = **4**; `git show 9f1d3c3:tools/mutate-and-run.sh \| sed -n '927p;932p;937p;942p'` = js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify | holds |
| `eight from round 18` | `git show 58e5d53:tools/mutate-and-run.sh` legs = 8; `4b7c682` same blob `fd1a63a…` | holds |
| `nine from round 26` | `git show a08e85c:tools/mutate-and-run.sh` legs = 9 | holds |
| `ten from round 51` | `git show 6d8c11e:tools/mutate-and-run.sh` legs = 10 | holds |
| `(r2, killed 8/10 = 80 %)` js-kimi-census | `TABLE_JS` at 9f1d3c3 (`:519`): D2 and D10 SURVIVED ⇒ 8 killed | holds |
| `bash-surface-census (r3, 8/10 = 80 %)` | `TABLE_BASH` (`:520`): B5, B10 SURVIVED ⇒ 8 killed | holds |
| `bash-tsukuroi-census (r5, 6/10 = 60 %)` | `TABLE_TSUKUROI` (`:521`): B7–B10 SURVIVED ⇒ 6 killed | holds |
| `bash-mado-verify (r6, 4/10 = 40 %)` | `TABLE_MADO` (`:522`): D3,D5,D7,D8,D9,R1 SURVIVED ⇒ 4 killed | holds |
| `tools/mutate-and-run.sh@9f1d3c3:72-109` | `sed -n '72p'` = `# --regression (r4-2; r7-1 leg ledger) — the fleet's recorded mutation cases,`; `sed -n '109p'` = `#` (block terminator); 72–108 is the whole `--regression` contract incl. the four kill-rates at 75–78 | resolves |
| `:511-522` (same file@9f1d3c3) | `sed -n '511p'` = `PIN_JS=83016d45…`; `sed -n '522p'` = `TABLE_MADO='D1:KILLED,…'` — exactly the four legs' pins (`511-518`) + tables (`519-522`) | resolves |
| `at round 18 (runner 4b7c682) the recorded tables sit at :597-620` | at `4b7c682`: `sed -n '597p'` = `PIN_JS=…`; `sed -n '620p'` = `TABLE_SOURCESCHECK='K_KIND:KILLED,…'`; within 597–620 there are 8 `TABLE_*` lines and 16 `PIN_/REV_` lines (the eight-leg pin+table block) | resolves |
| `eight ledger rows — six in the §1/ER-2 table plus the round-16 and round-18 appends` | `fleet-kill-rate-ledger.md` at C1: numbered rate rows 1–4 (`:45-48`, §1) + 5–6 (`:276-277`, ER-2) = six; round-16 append row (`:410`) + round-18 append row (`:432`) = 8 total | holds |
| `the ninth and tenth cases, cite-check and drift-pins, are recorded in their own notes, not as ledger rows` | ledger has no rate row for either: `grep -n '1205c662\|K_PIN_KIND'` = no hit; drift-pins appears only in the Round-52 §3-supersession bullet (`:441`), not as a row; both notes exist at C1 (`corpus/knowledge/mutation-case-kumitate-cite-check.md`, `…-kagi-drift-pins.md`) | holds |
| `corpus/knowledge/fleet-kill-rate-ledger.md` exists | `git cat-file -e 99c3bc88d704:corpus/knowledge/fleet-kill-rate-ledger.md` (via `git show`) | resolves |

Anchor resolution test for all three pinned revisions: `git cat-file -t 9f1d3c3` → `commit`; `git cat-file -t 4b7c682` → `commit`; both `merge-base --is-ancestor <rev> 99c3bc88d704…` → yes.

## Quality scan (QUALITY 104 classes)

Ran over the exact section bytes (`sec.txt`, 1105 B):

* **Duplicate parenthetical:** none — 8 parentheticals, all distinct (counted by set).
* **Self-contradicting sentence:** none found beyond the finding above (the four→seven gap is an omission, recorded there).
* **Run-together / missing space:** none. Parens balanced 9/9; backticks balanced 20 (even); no tab; no trailing whitespace; no double space.
* **Citation receipt check:** each of the three citations in the paragraph was opened at the revision it names and establishes its clause (table above). No citation points at a range that does not carry the named content.

Scratch scan script: `/fast/scratch/hyaku/tameshi-r54/T54W2Read04/scan.py`; output `scan.txt`. Line widths: 71–78 for the prose lines, with `:942` at 136 and `:944` at 242 — long-line use is file-wide convention (53 prose lines >150 chars elsewhere), so not scored.

## Artifacts opened

Lane (read-only):

* `SKILL.md` @ `99c3bc88d704566197783f66b211ee0a830e0330` (whole blob → `SKILL_C1.md`, 2197 lines; read `:932-945`) and @ `59c38109bf11` for the C0 comparison (`SKILL_C0.md`).
* `tools/mutate-and-run.sh` @ `9f1d3c3` (`:1-16`, `:70-135`, `:508-528`), @ `4b7c682` (`:596-621`), @ `6d8c11e`, `a08e85c`, `58e5d53`, `c699c8c`, `606716f`, and @ `99c3bc88d704` (`:1-130`, whole 2159-line file).
* `corpus/knowledge/fleet-kill-rate-ledger.md` @ `99c3bc88d704` (whole file, 443 lines).
* `corpus/knowledge/mutation-case-kumitate-cite-check.md` @ `99c3bc88d704` (`:1-20`).
* `corpus/QUALITY.md` @ `99c3bc88d704` (criterion 103, criterion 104, criterion 105 tails).
* `.ufo/waves/round-54/reader-section.py` (instrument, to match the sha protocol).

## Commands run (in order, abridged to the load-bearing ones)

```
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 99c3bc88d704566197783f66b211ee0a830e0330 "## The leg ledger — replay, receipt, and how it is read (round 7, measured)"
git -C … show 99c3bc88d704:SKILL.md > SKILL_C1.md ; wc -l ; sed -n '932,945p'
git -C … cat-file -t 9f1d3c3 ; git -C … cat-file -t 4b7c682
git -C … show 9f1d3c3:tools/mutate-and-run.sh | sed -n '72,109p'
git -C … show 9f1d3c3:tools/mutate-and-run.sh | sed -n '511,522p'
git -C … show 4b7c682:tools/mutate-and-run.sh | awk 'NR>=596&&NR<=621'
git -C … show 606716f:tools/mutate-and-run.sh | grep -n "^VERSION="   # r10-2
git -C … show 606716f:tools/mutate-and-run.sh | grep -cE '^  regression_case_git (js|bash)-'   # 6
for c in c699c8c a08e85c 6d8c11e 58e5d53 4b7c682; do … grep -cE '^  regression_case_git (js|bash)-'; done  # 7,9,10,8,8
git -C … show 99c3bc88d704:corpus/knowledge/fleet-kill-rate-ledger.md | grep -nE '^\| *[0-9]+ *\|'
git -C … show 99c3bc88d704:tools/mutate-and-run.sh | sed -n '84p'    # r10-2 six legs; r16 seven; …
python3 scan.py                                                     # QUALITY-104 classes
python3 -c 'sha256 over lines 932..944 joined by \n'                # 430dd86f… (matches reader-section)
```

## Provenance / scope

* Read-only everywhere: fleet root outside the lane, sibling lanes, `.ufo/state/`, watchdog log, all lane files. Wrote only `.ufo/waves/round-54/w2/T54W2Read04.json`, `.ufo/waves/round-54/w2/T54W2Read04.md` and scratch under `/fast/scratch/hyaku/tameshi-r54/T54W2Read04/`.
* `/tmp`: unused (scratch under `/fast/scratch`).
* Tools installed/upgraded: none (python3, git, bash, coreutils already present; pacman transactions paused host-wide and not needed).
* Out of scope by seat: no edit to SKILL.md, counters, contract, freeze, ledger, wave specs; no commit/push/fetch/reset/add anywhere; no subagents.
