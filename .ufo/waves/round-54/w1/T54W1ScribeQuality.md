# T54W1ScribeQuality — QUALITY criteria 105/106, drafted

Seat `T54W1ScribeQuality`, round 54 (hyaku run 11, L1 TameshiR54a2), lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `d33053f7`, content commit
C0 `59c38109bf11`. Item: read QUALITY.md's last ten criteria and round-53's
QUALITY 104, draft criterion 105 (a counter arm is proven on a positive control)
and one further criterion the C0 changes justify, each with a falsifier a command
decides, and name the number and landing spot. No edits to QUALITY.md.

## 1. Answer in one block

| # | heading | lands at |
|---|---|---|
| 105 | a counter arm is proven on a positive control, not only on the do-nothing tree | `corpus/QUALITY.md:1584`, inside `## Criteria appended — round 54 (2026-10-28)`. Already written in the worktree and **uncommitted** (`git status --porcelain corpus/QUALITY.md` → ` M corpus/QUALITY.md`). My draft keeps the body and repairs the falsifier's receipt pointers (§3). |
| 106 | a could-not-evaluate outcome prints no verdict token, and the arm asserts the absence | `corpus/QUALITY.md:1592` — the file ends at 1590 today, so it appends directly after 105 inside the same round-54 section. |
| 107 | held, not proposed this round: a standing count of callers is derived from the code, not listed | named with its receipt in §4; round 55 candidate. |

Numbering follows the corpus convention (next free integer after 104, one appended
section per round). Both proposed criteria are command-decidable; neither is
satisfied by prose alone.

## 2. What I opened (every read named)

- `corpus/QUALITY.md:1440-1590` — criteria 96-105, the round-46 to round-54
  append sections, and the landing convention used at 1582-1590.
- `corpus/QUALITY.md:1574-1580` — criterion 104's landed form (round 53).
- `corpus/lessons/round-53.md:107-116` — 104 as drafted in its lesson; same
  structure (body, falsifier) the 105 draft follows.
- `corpus/lessons/round-54.md:78-86` — 105 as drafted in this round's lesson.
- `corpus/QUALITY.md:1584-1590` — 105 as it currently stands (uncommitted).
- `.ufo/evidence/round-54/contract.json`, `freeze.json`,
  `deciding-run.sh:1-60` (the `CONTROLS=` refusal is line 48),
  `control/controls.sh:100-171` — the control order, the CTL_POS/CTL_EXIT0
  definitions, and the receipts `deciding-run.sh` demands at REV.
- `.ufo/evidence/round-54/c1/measure.py:160-250` — the rekey arm and the reader
  arm (arm 3 reads with `git ls-tree -r … '.ufo/evidence/round-21/coldread/'` at
  :172-173).
- `.ufo/evidence/round-54/c2/measure.py:1-201` — the whole C2 counter, including
  the hardcoded `TOOLS` list (:43-51), the refusal arm (:113-124), and the usable
  arm with its **amendment-2** comment (:129-144: the rc is the plain run, the
  traced run supplies only the mkdir census).
- `git show 88afa9415454:.ufo/evidence/round-53/c1/measure.py` — lines 93-100,
  the pathspec that returns the directory itself (`ls-tree --name-only`, no
  `-r`, no trailing slash).
- `.ufo/evidence/round-54/control/controls-a.stdout`,
  `r53-counter-at-88afa941.stdout` — the recorded control lines.
- `corpus/knowledge/scratch-root-contract.md:1-60` — C0's three-arm table, the
  "no verdict may be printed" sentence (:34-36), and the falsifier paragraph.
- `SKILL.md:32-38` at C0 (`git show 59c3810:SKILL.md`) — the three-arm standing
  bullet.
- `tools/env-diff.py:32-48` at C0 — `ScratchRootUnusable`, `strict_scratch_root()`
  (`if t:` at :43), and the entry-point mapping.
- `tools/context-capture.py`, `tools/repeat-control.py` — refusal-path prints.
- `tools/registry.json` — 56 rows, 7 of them carrying a `scratch_root` cell.
- `corpus/SOURCES.md:152-154` — S277-S279 rows; the S278 snapshot at C0 lines
  163-165 read `for envname in 'TMPDIR', 'TEMP', 'TMP':` / `dirname = …` /
  `if dirname: dirlist.append(dirname)`, matching the note's located quote.

## 3. Criterion 105 — draft as it should land

Body (kept verbatim from the landed, uncommitted text at `QUALITY.md:1584-1586`,
because it is right):

> ### Criterion 105 — a counter arm is proven on a positive control, not only on the do-nothing tree
>
> A counter arm that reads a directory, a revision or a manifest is proven by a
> positive control in which that arm must fire: the receipt records the arm's own
> non-zero count at a tree where the round's work is present. The do-nothing tree
> cannot prove an arm live — it fails for other reasons, so a dead arm (a
> pathspec that matches nothing, a key that never appears) looks healthy there.
> The check that can fail: a positive-control receipt in which the arm's own
> counter reads zero, or a control run that pre-registers the arm's value without
> a tree that carries it.

Delta — the falsifier's two receipts. Landed text:

> Falsifier that must fail: the round-53 C1 counter's rekey arm prints
> `rekeyed=0/30` at its own final content revision `88afa941` (the pathspec
> `git ls-tree --name-only REV .ufo/evidence/round-21/coldread` returns the
> directory itself), while the round-54 counter's arm prints `rekeyed=7/7` on its
> positive control; the two receipts are `.ufo/evidence/round-53/c1/measure.py`
> run at `88afa941` and `.ufo/evidence/round-54/control/controls-b.stdout`.

Two pointer defects, both command-decidable (finding F1):

1. The left side names a **script**, not a receipt. The line `rekeyed=0/30` lives
   in `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`, which is
   untracked at C0.
2. The right side names `.ufo/evidence/round-54/control/controls-b.stdout`,
   which does not exist — not at C0, not in the worktree. It is a phase-B
   artifact (`controls.sh` phase `b`, CTL_POS_c1), and `deciding-run.sh:48`
   refuses without it, so it is *expected*; but a criterion that lands before it
   is written violates criterion 97 ("a record's evidence pointers resolve at the
   revision that lands it").

Proposed replacement falsifier (byte-ready):

> Falsifier that must fail: the round-53 C1 counter prints `rekeyed=0/30` at
> `88afa941` (receipt `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`,
> `PROBLEM rekey-dir-count=0` on the next line), while the round-54 C1 counter's
> rekey arm prints `rekeyed=7/7` in its CTL_POS_c1 line on the repaired tree
> (receipt `.ufo/evidence/round-54/control/controls-b.stdout`, written in control
> phase B and committed before the deciding run; `deciding-run.sh` refuses with
> `DECIDING_REFUSED control-receipt-missing` otherwise); a commit that lands the
> criterion without both receipts is refused by criterion 97 before this
> falsifier is read.

Soundness check on the criterion's premise (so the draft is not defending a
claim the round cannot meet): the round-54 arm really does read the re-key
directory correctly — `c1/measure.py:172-173` is
`git(['-C', lane, 'ls-tree', '-r', '--name-only', rev, '.ufo/evidence/round-21/coldread/'], check=False)`
— and `controls-a.stdout` shows the do-nothing tree at base printing
`rekeyed=0/7`, i.e. the do-nothing tree proves nothing, exactly as the criterion
says. The round-53 side reproduces: `rekeyed=0/30`, `PROBLEM rekey-dir-count=0`.

## 4. Criterion 106 — the one further criterion C0 justifies

C0's own note states a rule the C2 counter does not enforce:

> gate did not run, so no verdict may be printed and the exit class is
> could-not-evaluate (2), never 1 (a verdict of "differs"/"failed") and never a
> traceback. (`corpus/knowledge/scratch-root-contract.md:34-36`)

At C0 one of the seven tools prints a verdict token on that arm anyway
(`context-capture`: `SELFTEST: FAIL (setup error: …`, rc 2), and the C2 counter
scores it green (`unusable_exit2=7`). The exit class is right and the vocabulary
is wrong; a reader or a wrapper that greps the verdict token reads a failed
selftest where the gate never ran. That is criterion 82's distinction (a crash is
not a kill) one level up, at a setup refusal, and it is decidable by exit code
plus a token scan.

### Criterion 106 — a could-not-evaluate outcome prints no verdict token, and the arm asserts the absence

A tool that refuses before it measures prints, on the refusal path, the
could-not-evaluate class and the input value it saw, and no verdict token: no
`PASS`, `FAIL` or `MISMATCH` anywhere in the line, and no traceback. The class is
carried by the class word, never by a verdict word with a parenthetical excuse. A
counter arm that credits such a refusal reads all three — exit code, class word,
value — and asserts the fourth: the absence of verdict vocabulary, printed as its
own count. A shared-helper contract that fixes the exit code but leaves the
vocabulary to each caller is half a contract: the exit code decides what a script
does, the words decide what the next reader believes.

Check that can fail: for each tool that calls the shared refusal helper, run its
self-test with `TMPDIR` set to a path that is not a writable directory and
require `rc=2`, the class word, the value, and an empty token scan:

```
UNUSABLE=$SCR/unusable; mkdir -p "$SCR"
cd CLONE && for spec in registry-check:--selftest env-diff:--selftest \
  bash-witness-study:selftest evidence-disposition:--selftest \
  pin-disposition:--selftest context-capture:--selftest repeat-control:--selftest; do
  n=${spec%%:*}; a=${spec##*:}
  out=$(TMPDIR=$UNUSABLE python3 tools/$n.py "$a" 2>&1); rc=$?
  tok=$(printf '%s\n' "$out" | grep -Eo 'PASS|FAIL|MISMATCH' | sort -u | tr '\n' ',' )
  printf '%-22s rc=%s verdict_token=%s\n' "$n" "$rc" "${tok:-none}"
done
```

Pass is seven lines of `rc=2 verdict_token=none`; the counter must print the
matching numerator beside its existing one (`unusable_exit2=7 class_only=7`). A
counter that prints `unusable_exit2=7` while one line carries a token is the
defect this criterion exists to stop.

Falsifier that must fail: at C0 the sweep prints
`context-capture rc=2 verdict_token=FAIL,` and six `verdict_token=none` lines, and
the frozen C2 counter prints `unusable_exit2=7` over that same set — the token
sweep is 6/7 while the counter's arm is 7/7
(`T54W1ScribeQuality-receipts/F5-refusal-vocabulary.txt`, `c2-at-c0-alone.stdout`).
After the fix the same sweep is 7/7 `none` and the counter's `class_only` count
is 7.

Lesson: `corpus/knowledge/scratch-root-contract.md:34-36` (C0 stating the rule)
against `tools/context-capture.py`'s refusal line; criterion 82's crash-versus-kill
precedent.

Where it lands: appended at `corpus/QUALITY.md:1592`, after 105, inside
`## Criteria appended — round 54 (2026-10-28)`. It binds round 55 onward; C0 does
not satisfy it (the falsifier above fires at C0), which is why it is filed as a
criterion plus a defect, not as a claim that C0 is clean.

### Held for round 55 (named, not proposed): 107 — a standing count of callers is derived from the code, not listed

C0's SKILL bullet closes over a literal seven ("the seven tools and their registry
`scratch_root` cells, measured by the round-54 C2 counter", `SKILL.md:37-39`) and
`c2/measure.py:43-51` hardcodes the same seven. The code carries exactly seven
callers at C0, so the statement is true today and a new caller is invisible
tomorrow. Demonstrated: a fixture at C0 plus one eighth caller
(`tools/scratch-consumer.py`, rc 1 **with a traceback** on a set-but-unusable
`TMPDIR` — the exact residue C0 removed) leaves every C2 arm count identical
(`tools=7 unusable_exit2=7 naming=7 empty_ok=7 docs=7`) and changes no verdict
(receipt `T54W1ScribeQuality-receipts/c106-fixture.stdout`, driver
`c106-driver.sh`). The rule would read: the counter derives its population with
`git grep -l 'strict_scratch_root(' REV -- 'tools/*.py'` and refuses when its
list differs, printing the extra/missing names. Held because this round's item
allows one further criterion and 106's evidence is a live contradiction inside
C0's own change set; 107 is a scope question about the counter.

## 5. Findings

### F1 — 105's falsifier cites two receipts that do not resolve at C0

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ for p in .ufo/evidence/round-54/control/controls-b.stdout \
           .ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout; do
    git cat-file -e "59c38109bf11:$p" 2>/dev/null && echo "AT-C0=yes $p" || echo "AT-C0=no $p"; done
AT-C0=no .ufo/evidence/round-54/control/controls-b.stdout
AT-C0=no .ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout
$ git ls-files .ufo/evidence/round-54/control/
.ufo/evidence/round-54/control/controls.sh
$ git status --porcelain corpus/QUALITY.md .ufo/evidence/round-54/control/
 M corpus/QUALITY.md
?? .ufo/evidence/round-54/control/controls-a.exit
?? .ufo/evidence/round-54/control/controls-a.stdout
?? .ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout
```

Verdict: the criterion's body is sound and its falsifier's *values* are the ones
the receipts carry (`rekeyed=0/30`; CTL_POS needs the full C1 PASS, which implies
`rekeyed=7/7`), but the falsifier names one script and one unwritten file. Criterion
97 decides the fix: commit both receipts (and `controls-a.*`, which
`deciding-run.sh:48` also requires) before or in the commit that lands 105, and
name the files rather than the script. This is a pointer/timing defect, not a
false claim.

### F2 — the round-54 lesson's 105 falsifier is inverted against the landed criterion

```
$ sed -n '78,86p' corpus/lessons/round-54.md
- **105. A counter arm that reads a directory by pathspec is proven on a tree
  where the arm must fire (the positive control), not only on the do-nothing
  tree. Falsifier: a control receipt in which the arm's own counter reads a
  non-zero value; a pathspec that returns the directory itself is a defect even
  when the overall verdict is false for another reason.**
$ sed -n '1586p' corpus/QUALITY.md   # landed body, same sentence
… The check that can fail: a positive-control receipt in which the arm's own
counter reads zero, or a control run that pre-registers the arm's value without a
tree that carries it.
```

Verdict: the lesson (C0 content) makes "reads a non-zero value" the falsifier —
i.e. it names the criterion's own pass condition as the failure. QUALITY.md:1586
has it right ("reads zero"). The criterion's `Lesson:` pointer therefore points
at a sentence that contradicts it. Suggested byte fix in the lesson: replace
"reads a non-zero value" with "reads zero", preserving the rest of the line.

### F3 — the C2 `usable_ok` arm is load-sensitive (and my first reading of it was wrong)

Correction first, because it is the honest record: I initially read only
`c2/measure.py:122-136` and concluded the arm credits the *traced* run's exit
code. The frozen bytes carry **amendment 2** at `:129-144` — `rc_plain, _ =
run_tool(…, str(usable))` and `usable_ok += (rc_plain == 0 and hits == 0)` — with
the comment "under `strace -f` one tool's own timeout tests fail (tracer
overhead), so a traced rc measured the tracer". The traced rc never enters
`usable_ok`. My contamination claim is withdrawn.

What the tracer pair does establish is that one tool's self-test is
timing-sensitive, and that is what matters for the counter's stability. Same
clone, same `TMPDIR`, same interpreter:

```
rev 59c38109bf11, tools/registry-check.py blob 96d762ea6829ede011c1d80a7d5b1a0d8d818b8b
without: TMPDIR=usable python3 tools/registry-check.py --selftest            rc=0  SELFTEST: PASS (51 cases)
with:    TMPDIR=usable strace -f -e trace=mkdir,mkdirat -o LOG python3 tools/registry-check.py --selftest
                                                                            rc=1  SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)
base d33053f, same blob: without rc=0 PASS (51 cases); with rc=1 FAIL (2 of 51, same two cases)
strace 7.2, kernel 7.2.11-arch1-1
```

The plain run is not stable either when the host is busy. Two full C2 runs that
overlapped each other (my own two invocations) read:

```
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
```

A third full run, started after those finished and left alone, reads:

```
$ cat /proc/loadavg  → 14.79 32.36 27.24 …(32 CPUs)
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
rc=0   (99 s)
```

Direct plain runs of the same blob, same `TMPDIR`, same cwd: PASS (51 cases) 4/4
(two at C0, two at base). `unusable_exit2`, `naming`, `empty_ok`, `tmp_mkdirs`,
`docs`, `note`, `sources` are identical in all three full runs; only
`usable_ok` moves, and only when two counters run at once.

Verdict: **not** a C0 defect and **not** tracer contamination — C0 is green in
isolation (`total=0`, `PASS=true`). It is a reproducibility property the deciding
run must respect: `registry-check --selftest` carries two timeout cases that fail
under load or under a tracer, so a deciding run that overlaps another counter can
print `usable_ok=6` and `C2_R54_PASS=false` spuriously. The base control's
recorded `usable_ok=7` is reproducible only in isolation, which is how it was
produced. Receipts: `c2-at-c0.stdout` (concurrent), `c2-at-c0-alone.stdout`
(isolated), `registry-check-strace-{c0,c0-rerun,base}.out`,
`registry-check-{direct-base,plain-c0,usable-direct}.out`, `F3-verdict-pair.txt`.

### F4 — the refusal-arm vocabulary gap (basis of 106)

```
$ for each of the seven: TMPDIR=<non-writable> python3 tools/<t>.py <selftest>
registry-check         rc=2 verdict_token=none
env-diff               rc=2 verdict_token=none
bash-witness-study     rc=2 verdict_token=none
evidence-disposition   rc=2 verdict_token=none
pin-disposition        rc=2 verdict_token=none
context-capture        rc=2 verdict_token=FAIL,   | SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch … (could-not-evaluate))
repeat-control         rc=2 verdict_token=none   | REPEAT_CONTROL: setup_error
count with a verdict token: 1
```

Verdict: 1/7 prints a verdict token on a could-not-evaluate line, while the note
forbids it (`scratch-root-contract.md:34-36`) and the C2 arm still reads 7/7
because it tests exit code, class word, value and "no traceback" — not the token.
Not a C2 claim failure (the claim never mentions vocabulary); it is the gap 106
closes. Receipt: `F5-refusal-vocabulary.txt`.

### F5 — the population is a literal (basis of held 107)

```
$ git grep -l 'strict_scratch_root(' 59c38109bf11 -- 'tools/*.py' | wc -l
7
$ # fixture: the same tree plus tools/scratch-consumer.py (an eighth caller, rc 1 with traceback)
$ c106-driver.sh LANE 59c38109bf11 SCRATCH
eighth-caller rc=1 (contract requires 2, could-not-evaluate, no traceback)
grep-callers=8
c2-exit=1
C2_R54: rev=c457c0264879 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
```

Verdict: the eighth caller violates the contract in the same revision and every
arm count is byte-identical to the seven-caller C0 run taken under the same
concurrent conditions (`c2-at-c0.stdout`); only the revision id differs. The
counter cannot see a population it does not list. (The `usable_ok=6` in both runs
is F3's load sensitivity, not the fixture.)

## 6. What I checked and did not find

- The three-arm semantics in the note and SKILL: empty `TMPDIR` is treated as
  unset by `if t:` in the helpers (`tools/env-diff.py:43` as the template); no
  helper builds a path from `""`. No defect found.
- S277-S279: all three rows exist (`corpus/SOURCES.md:152-154`), the note cites
  them, and the S278 snapshot at C0 holds `if dirname: dirlist.append(dirname)`
  at lines 163-165 — the located quote is accurate. No defect found.
- The registry cells: 56 rows, exactly the 7 selftest rows carry `scratch_root`,
  and each cell names `TMPDIR`, `empty` and `could-not-evaluate` — matching the
  counter's `docs=7`. No defect found.
- The round-54 C1 rekey arm uses `ls-tree -r` with a trailing slash (the round-53
  defect is not repeated) and the do-nothing tree reads `rekeyed=0/7`. No defect
  found.
- The frozen C2 counter at C0 read in isolation: `total=0 C2_R54_PASS=true`,
  rc 0 — the C2 claim's target is met by the C0 bytes when nothing else runs.
- Findings 1-5 are the only ones I can defend; no reader-style byte finding was
  invented for any SKILL section (not this seat's item).

## 7. Bounds, scratch, tooling

- No edits to `corpus/QUALITY.md`, SKILL.md, tools, `tools/registry.json`, the
  counters, contract, freeze, ledger, wave spec, or any lane file. Writes are
  confined to this report and `T54W1ScribeQuality-receipts/`.
- Scratch: `HYAKU_SCRATCH=/fast/scratch/hyaku`, tree
  `/fast/scratch/hyaku/tameshi-r54/T54W1ScribeQuality` (clones `rc-clone`,
  `base-clone`, three c2 work dirs, the `c106-fixture.*` temp tree), removed at
  exit; no tree left behind. Fixtures were `git clone --shared` copies with
  `git rev-parse --show-toplevel` asserted before any commit.
- No tool installed or upgraded. Toolchain observed for the receipts: `strace
  7.2`, kernel `7.2.11-arch1-1`, 32 CPUs; `/proc/loadavg` recorded at the start
  and end of the isolated counter run so F3's load claim is attributable.
- Census at report time: `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → exit 0, `ok …/corpus/SOURCES.md`
  (duplicate-url advisories only, pre-existing).

## 8. Receipts

All under `.ufo/waves/round-54/w1/T54W1ScribeQuality-receipts/`:

| file | what it holds |
|---|---|
| `c2-at-c0.stdout` | the C2 counter at C0 under concurrent load: `usable_ok=6 … C2_R54_PASS=false` |
| `c2-at-c0-alone.stdout` | the same counter alone at C0: `usable_ok=7 … total=0 C2_R54_PASS=true`, rc 0 |
| `F3-verdict-pair.txt` | registry-check PASS unwrapped / FAIL wrapped, at base and C0, with blob, strace and kernel |
| `registry-check-strace-c0.out`, `registry-check-strace-c0-rerun.out`, `registry-check-strace-base.out` | the three wrapped runs (2/51 failing cases each) |
| `registry-check-usable-direct.out`, `registry-check-direct-base.out`, `registry-check-plain-c0.out` | the unwrapped controls (PASS 51 cases) |
| `F5-refusal-vocabulary.txt` | the seven-tool refusal sweep (6/7 `none`, context-capture `FAIL`) |
| `context-capture-unusable.out`, `repeat-control-unusable.out` | the raw refusal lines |
| `c106-driver.sh`, `scratch-consumer.py`, `c106-fixture.stdout` | the eighth-caller fixture, its driver, and the counter's unchanged output |
