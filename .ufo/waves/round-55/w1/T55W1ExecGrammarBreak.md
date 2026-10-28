# T55W1ExecGrammarBreak — C2 grammar-arm sensitivity

Seat: `T55W1ExecGrammarBreak` (executor, leaf). Item: break the C2 grammar three
ways in scratch copies of the patched tool set, score each with the C2 counter,
and show that each break costs exactly one mode on the grammar arm while every
other arm stays put. Report only; no lane production file was touched.

## 1. Instrument and fixture (exactly what was scored)

- Counter: `.ufo/evidence/round-55/c2/measure.py`, `sha256 0458f632…`
  (amendment 8, frozen at `133b2ce`; a copy of those exact bytes is what every
  run in §2 executed — `counter-run-sha.txt`). The freeze manifest now verifies
  against the disk for all seven frozen files (checked file-by-file), and the
  content has not moved since the C0 commit: `git diff --stat 9cf0146 HEAD --
  tools/ SKILL.md SCORECARD.md corpus/ LOG.md` is empty.
- Fixture: `git clone --shared` of the lane, branch `r55-patched` at the C0
  content commit `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`, then one
  `git worktree` + one commit per break. Tool digests at the base commit:
  `tools/repeat-control.py a8fad68f…`, `tools/context-capture.py f1043425…`.
  Every git call named `-C <fixture>`; `git rev-parse --show-toplevel` printed
  the fixture directory before every commit. The lane was never mutated.
- Receipts: `T55W1ExecGrammarBreak-receipts/` — `<run>.out` (full `--explain`
  stream), `<run>.receipts.json` (the counter's own receipt), `diff-*.patch`,
  `grammar-vs-token.{py,out}`, `counter-run-sha.txt`, `status-final.txt`.
  Two earlier instrument generations are kept, not deleted, under
  `superseded-preamendment-8modes/` and `superseded-total-bug-36ca47d3/`
  (see §5).

## 2. Verdict lines, side by side (the receipt the closure asks for)

| run | rev | verdict (`C2_R55: …`) | exit |
|---|---|---|---|
| baseline | `9cf0146b94dd` | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true` | 0 |
| break 1 — prefix removed | `bab75e5db270` | `grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false` | 1 |
| break 2 — `RuntimeError` appended | `0951af66951a` | `grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false` | 1 |
| break 3 — exit 0 instead of 2 | `1eb2cb46333a` | `grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false` | 1 |
| extra 2b — token inside a still-matching line | `ad10185bddde` | `grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false` | 1 |
| extra 4 — context-capture prefix removed | `017781471c9d` | `grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false` | 1 |

Each break costs exactly one grammar mode and nothing else: the other eight
grammar modes, all five lazy modes, both 13-mode arms, the `tmp_mkdirs` census
and the three documentation arms stay at their denominators, and `total` moves
0 → 1. Baseline is `total=0`, so the instrument is not uniformly red.

## 3. The breaks (exact diffs, one commit each)

Break 1 — remove the `could-not-evaluate:` prefix (`diff-mut1-no-prefix.patch`):

```
-    emit_err(f"repeat-control: could-not-evaluate: {message}")
+    emit_err(f"repeat-control: {message}")
```

Break 2 — append `RuntimeError` to the line (`diff-mut2-token.patch`):

```
-    emit_err(f"repeat-control: could-not-evaluate: {message}")
+    emit_err(f"repeat-control: could-not-evaluate: {message} RuntimeError")
```

Break 3 — return 0 instead of 2 (`diff-mut3-exit0.patch`):

```
     emit_err(f"repeat-control: could-not-evaluate: {message}")
     emit("REPEAT_CONTROL: setup_error")
-    return EXIT_BY_ID["setup_error"]
+    return 0
```

Extra 2b (`diff-mut2b-token-inside.patch`) — same token, placed inside the
quoted value so the regex still matches; this isolates the token predicate from
the shape predicate:

```
-    emit_err(f"repeat-control: could-not-evaluate: {message}")
+    emit_err("repeat-control: could-not-evaluate: " + message.replace(
+        "directory: '", "directory: 'RuntimeError ", 1))
```

Extra 4 (`diff-mut4-cc-no-prefix.patch`) — the same prefix break on the other
tool the round repaired:

```
-        sys.stderr.write("context-capture.py: could-not-evaluate: {}\n".format(exc))
+        sys.stderr.write("context-capture.py: {}\n".format(exc))
```

## 4. Which mode each break costs, and why

Each run's `bad` map has exactly one non-`tmp_mkdirs` key, naming the mode:

| run | failing mode | recorded stderr line |
|---|---|---|
| break 1 | `repeat-control --selftest` | `repeat-control: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)` |
| break 2 | `repeat-control --selftest` | `repeat-control: could-not-evaluate: … '<value>' (could-not-evaluate) RuntimeError` |
| break 3 | `repeat-control --selftest` | grammar-shaped line, but `rc=0` |
| extra 2b | `repeat-control --selftest` | `repeat-control: could-not-evaluate: … 'RuntimeError <value>' (could-not-evaluate)` |
| extra 4 | `context-capture --selftest` | `context-capture.py: cannot create clone scratch under the scratch root: … (could-not-evaluate)` |

Predicate split (`grammar-vs-token.py` re-applies the counter's GRAMMAR regex
and the token check to each recorded line):

```
mut1-no-prefix     rc=2 grammar_match=False token=False
mut2-token         rc=2 grammar_match=False token=True
mut2b-token-inside rc=2 grammar_match=True  token=True
mut3-exit0         rc=0 grammar_match=True  token=False
mut4-cc-no-prefix  rc=2 grammar_match=False token=False
```

The three clauses have independent teeth: shape (breaks 1, 2, extra 4), the
`RuntimeError` token (extra 2b is the only case whose line still matches), and
the exit code (break 3). Break 2 trips shape and token together, which is why
extra 2b exists.

## 5. Method notes (and three instrument generations)

- **`--work` must not live under `/tmp`.** My first pass put the counter's
  `--work` under `/tmp`; the `tmp_mkdirs` census counts every `mkdir` whose path
  starts `/tmp`, so the usable-arm TMPDIR was counted 2043 times and that arm
  read `total=2043`. Those receipts were discarded and the scored pass uses
  `--work` under `/fast/scratch/…` (`tmp_mkdirs=0`). My error, not a counter
  defect — but worth knowing for any seat that runs the counter.
- **The counter moved three times while this seat worked.** Generation 1
  `d6ca1d85` (8 allocating modes, pre-amendment) — my first sensitivity result.
  Generation 2 `36ca47d3` (nine allocating modes, amendment 6) — its totals
  arithmetic still mixed `len(table)` with the measured 13-mode arms, so an
  all-green tree read `total=1`: that receipt
  (`superseded-total-bug-36ca47d3/baseline.out`, `bad={}` with every arm full)
  is kept as evidence of why amendment 8 exists. Generation 3 `0458f632`
  (amendment 8) is what §2 reports. Each generation was re-scored, not
  reinterpreted: the verdict lines in §2 are measurements, and the sensitivity
  conclusion (one mode per break, everything else stable) held in all three.
- Reproduction of one run:

```
python3 <counter-bytes>/.ufo/evidence/round-55/c2/measure.py \
  --lane <fixture> --rev <break-commit> --work <empty-dir> --explain
```

- The lane advanced past the scored tree while this seat worked (`133b2ce`,
  `c31cdd9`, then uncommitted edits to `tools/context-capture.py`,
  `tools/registry-check.py`, `tools/registry.json` and the note). The
  uncommitted edits harden the emission call sites (a refusing stderr stream
  must not change the class) but leave the emitted line byte-identical — checked
  by grepping the three anchor strings in `repeat-control.py`,
  `context-capture.py` and `registry-check.py` — so the sensitivity result
  transfers to the final revision; only the scored tree is pinned in §1.

## 6. Findings for the L1 (reported, not fixed)

F1 — **the frozen break control cannot match the integrated line.** Frozen
`controls.sh` (phase b, `CTL_BREAK_c2`) rewrites
`emit_err(f"repeat-control: could-not-evaluate: {exc}")` and asserts
`src.count(old) == 1`. The integrated `tools/repeat-control.py:233` names the
parameter `message`:

```
$ python3 - <<'EOF'
src = open('tools/repeat-control.py').read()
print(src.count('emit_err(f"repeat-control: could-not-evaluate: {exc}")'))
print(src.count('emit_err(f"repeat-control: could-not-evaluate: {message}")'))
EOF
0
1
```

The assertion then raises, `git add -A` stages nothing, `gitcommit` fails and
`controls.sh b` exits 2 before printing `CONTROLS_B: … as pre-registered`;
`deciding-run.sh` refuses with `DECIDING_REFUSED controls-b-verdict-missing`.
`controls.sh` is frozen (`7c0cacb5…`, unchanged through all eight amendments),
so the only fix available to the round is in the tool: name the parameter
`exc` at the anchor line. Status when I finished: phase A had recorded only
`CTL_0_c1`, so this has not fired yet.

F2 — **stale prose inside the frozen counter.** `c2/measure.py`'s docstring
still says `grammar 8 allocating modes`, `names all eight allocating modes`,
and prints the contract as `grammar=N/8`, while the code measures nine
allocating modes and prints `N/9` (and the note names nine). Cosmetic, but it
is a frozen file that now describes a denominator it does not use; the frozen
`controls.sh` and the note both say nine.

F3 — **scratch purge during the wave.** At ~13:54 my
`/fast/scratch/hyaku/tameshi-r55/T55W1ExecGrammarBreak` tree lost its clone and
its receipts mid-run (a sibling's `T55W1ExecCensus-final.sh` in the same parent
vanished within a minute of being listed). Everything was re-run, and final
receipts live in the lane, not only in scratch. Reported because it can
silently eat another seat's evidence.

F4 — **fix history, for the record.** At the start of this seat the
working-tree `freeze.json` did not pin the working-tree bytes
(`contract ed6871e1…` vs `0b99dd8c…`; `c2/measure ab3ae751…` vs `d6ca1d85…`),
and `deciding-run.sh` requires `FROZEN_UNCHANGED=1` between FREEZE and REV, so
the amended counters could not be both committed and frozen. The L1's
amendments 1-8 (`e2979f2`, `133b2ce`) re-froze on the amended bytes; the
manifest now verifies file-by-file and `git diff 133b2ce HEAD -- <frozen set>`
is empty. No action needed; recorded so the earlier observation is not read as
a live defect.

F5 — observation only, now superseded: the base receipt re-measured before
amendment 1 showed `lazy=5/5 empty=13/13 usable=13/13` with a detached clone,
so amendment 1's stated symptom did not reproduce from that receipt at base.
Not claiming the amendment is wrong — only that this seat could not reproduce
it from the committed base receipt.

## 7. Not done / out of scope

- No lane production file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`,
  `tools/**`) and no frozen counter byte was edited; I scored the bytes I found
  and report the apparatus defects above instead of repairing them.
- No build/lint/test run: the wave forbids it for leaf seats and the C2 counter
  is the instrument this item names.
- The C1 counter was not exercised (not this item).
