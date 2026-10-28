# T55W1ExecGrammarBreak — C2 grammar-arm sensitivity

Seat: `T55W1ExecGrammarBreak` (executor, leaf). Item: break the C2 grammar three
ways in scratch copies of the patched tool set, score each with the C2 counter,
and show that each break costs exactly one mode on the grammar arm while every
other arm stays put. Report only; no lane production file was touched.

## 1. Instrument and fixture (exactly what was scored)

- Counter: `.ufo/evidence/round-55/c2/measure.py` at its **working-tree** bytes,
  `sha256 d6ca1d851bb0037368c304f4d80254f7dc5bf76b1c3119cdf0f2a64bca95631a`.
  This is the amended counter (the three amendments recorded in the working-tree
  `contract.json`); the freeze-commit counter is `sha256 9d076812d9c0…` and is
  measured separately in §6/F3.
- Fixture: `git clone --shared` of the lane at the freeze commit
  `631cd6455e58dce969310b4c0466c3383d9f5108`, then the lane's **integration
  working-tree diff** of the five round-55 files applied
  (`tools/repeat-control.py`, `tools/context-capture.py`, `tools/registry.json`,
  `corpus/knowledge/scratch-root-contract.md`, `SKILL.md`) and committed as
  `r55-patched = 8a678ac3e3e270fde75add4aee52b974d10c998b` (this is the patch
  state I found at `T55W1ExecRepPatch`/`T55W1ExecCcPatch` time; no
  `T55W1ExecRepPatch` report existed when I started, so I took the integration
  bytes themselves rather than a second-hand patch).
- Tool digests at `r55-patched`: `tools/repeat-control.py`
  `a8fad68fcbb8…`, `tools/context-capture.py` `f1043425085a…`.
- Each break is one commit on top of `r55-patched`, in its own `git worktree`,
  scored by a fresh `measure.py --lane <fixture> --rev <break> --work <empty>`
  run. Every git call named `-C <fixture>`; `git rev-parse --show-toplevel`
  printed the fixture directory before every commit. The lane was never
  mutated, and no counter/contract/freeze byte was edited.
- Receipts: `T55W1ExecGrammarBreak-receipts/` — `<run>.out` (full `--explain`
  stream), `<run>.receipts.json` (the counter's own receipt), `diff-*.patch`
  (each break), `grammar-vs-token.{py,out}` (predicate split),
  `freeze-counter-9d0768.out`, `status-fast.txt`.

Reproduction of one run:

```
python3 <lane>/.ufo/evidence/round-55/c2/measure.py \
  --lane <fixture> --rev <break-commit> --work <empty-dir> --explain
```

## 2. Verdict lines, side by side

| run | rev | verdict (`C2_R55: …`) | exit |
|---|---|---|---|
| baseline (`r55-patched`) | `8a678ac3e3e2` | `grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=0 C2_R55_PASS=true` | 0 |
| break 1 — prefix removed | `bac1e007b8b4` | `grammar=7/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=1 C2_R55_PASS=false` | 1 |
| break 2 — `RuntimeError` appended | `e5668b2bb8bc` | `grammar=7/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=1 C2_R55_PASS=false` | 1 |
| break 3 — exit 0 instead of 2 | `eb92cbb1bae0` | `grammar=7/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=1 C2_R55_PASS=false` | 1 |
| extra 2b — token inside a still-matching line | `fb18f37aabf9` | `grammar=7/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=1 C2_R55_PASS=false` | 1 |
| extra 4 — context-capture prefix removed | `f79535b9ef5e` | `grammar=7/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=1 C2_R55_PASS=false` | 1 |

Reading: the repaired tree is `total=0` under this instrument, and each of the
three required breaks costs exactly one grammar mode and nothing else — the
other seven grammar modes, all five lazy modes, both 13-mode arms, the
`tmp_mkdirs` census and the three documentation arms stay at their
denominators, and `total` moves 0 → 1.

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

Extra 2b (`diff-mut2b-token-inside.patch`) — same token, placed **inside** the
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

Each run's `bad` dict has exactly one non-`tmp_mkdirs` key, naming the mode:

| run | failing mode | recorded stderr line |
|---|---|---|
| break 1 | `repeat-control --selftest` | `repeat-control: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)` |
| break 2 | `repeat-control --selftest` | `repeat-control: could-not-evaluate: … '<value>' (could-not-evaluate) RuntimeError` |
| break 3 | `repeat-control --selftest` | (grammar-shaped) `repeat-control: could-not-evaluate: … '<value>' (could-not-evaluate)` with `rc=0` |
| extra 2b | `repeat-control --selftest` | `repeat-control: could-not-evaluate: … 'RuntimeError <value>' (could-not-evaluate)` |
| extra 4 | `context-capture --selftest` | `context-capture.py: cannot create clone scratch under the scratch root: … (could-not-evaluate)` |

Predicate split (`grammar-vs-token.py` re-applies the counter's regex and the
token check to the recorded line):

```
mut1-no-prefix    grammar_match=False token=False rc=2
mut2-token        grammar_match=False token=True  rc=2
mut2b-token-inside grammar_match=True  token=True  rc=2
mut3-exit0        grammar_match=True  token=False rc=0
mut4-cc-no-prefix grammar_match=False token=False rc=2
```

So the arm's three clauses have independent teeth: shape (breaks 1, 2, extra 4),
token (extra 2b — the only case where the shape still matches), and exit code
(break 3). Break 2 trips shape and token together, which is why extra 2b exists.

## 5. Notes on method

- The first scoring pass put `--work` under `/tmp`; the counter's `tmp_mkdirs`
  census counts every `mkdir` whose path starts `/tmp`, so the usable-arm
  TMPDIR (`/tmp/…/work-*/tmp-usable`) was counted 2043 times and poisoned that
  arm (`total=2043` in the discarded pass; those receipts were overwritten).
  The scored pass uses `--work` under `/fast/scratch/…` and reads
  `tmp_mkdirs=0`. This was my error, not a counter defect, and the counter's
  own contract (`--work` scratch under it) is what made it visible.

## 6. Findings for the L1 (reported, not fixed)

F1 — **the frozen break control cannot match the integrated line.** Frozen
`controls.sh` phase b rewrites
`emit_err(f"repeat-control: could-not-evaluate: {exc}")` and asserts
`src.count(old) == 1`; the integrated `tools/repeat-control.py` names the
parameter `message`, so the count is 0:

```
$ python3 - <<'EOF'   # against the lane working tree
src = open('tools/repeat-control.py').read()
print(src.count('emit_err(f"repeat-control: could-not-evaluate: {exc}")'))
print(src.count('emit_err(f"repeat-control: could-not-evaluate: {message}")'))
EOF
0
1
```

With count 0 the heredoc's `assert` raises, `git add -A` stages nothing,
`gitcommit` fails and `controls.sh b` exits 2 before printing
`CONTROLS_B: … as pre-registered`; `deciding-run.sh` then refuses with
`DECIDING_REFUSED controls-b-verdict-missing`. The parameter must be named
`exc` (or the anchor must be the code's exact current string) before phase B
is run. The seat item for the patch said "anchor the emit line EXACTLY as …
`{exc}`"; the integrated code diverges from that.

F2 — **the working-tree freeze manifest does not pin the working-tree bytes.**
`freeze.json` records `contract.json` `ed6871e1…` and `c2/measure.py`
`ab3ae751…`; the bytes on disk are `0b99dd8c…` and `d6ca1d85…`
(`--rev`-independent check, command in §1). `freeze.json`'s mtime
(13:49:59) precedes both files' (13:50:08). At the freeze **commit** the
manifest is self-consistent (`2388cb50…` / `9d0768…` both match), so the
drift is confined to the uncommitted amendment. As it stands, "the frozen C2
counter" is not identifiable by the manifest digest.

F3 — **the deciding run cannot use the amended counter.** `deciding-run.sh`
extracts both counters from `REV` and gate 0 requires
`git diff --quiet FREEZE REV -- …c2/measure.py` (`FROZEN_UNCHANGED=0` sets
`rc=1`). Committing the amended counter at `REV` therefore fails the gate;
leaving it uncommitted fails the clean-tree gate. Measured on the same
repaired tree with the freeze-commit counter (`9d0768…`, the bytes
`deciding-run.sh` would extract if `FREEZE == 631cd64`):

```
C2_R55: rev=8a678ac3e3e2 grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=7/8 skill=0/1 total=2 C2_R55_PASS=false
```

(`note` loses `bash-witness-study selftest` → the freeze counter's label is
`bash-witness-study --selftest`; `skill` loses the marker because `SKILL.md`
wraps it across a newline and the freeze counter matches raw text — amendments
2 and 3 made exactly that fix and it is uncommitted.) Resolution is the L1's:
either amend the freeze commit (and re-run phase A at the new freeze bytes;
`.ufo/evidence/round-55/control/` does not exist yet, so phase A has not been
recorded) or accept that C2 cannot reach `total=0` under the freeze bytes.

F4 — **scratch purge during the wave.** At ~13:54 my `/fast/scratch/hyaku/tameshi-r55/T55W1ExecGrammarBreak`
tree lost its clone and its `receipts/` directory mid-wave (a sibling's
`T55W1ExecCensus-final.sh` in the same parent also vanished within a minute of
being listed); the first baseline run's output was lost with it. I re-ran
everything with the fixture under `/tmp` and only the counter's `--work`
directories under `/fast/scratch`, and receipts now live in the lane
(`T55W1ExecGrammarBreak-receipts/`), not only in scratch. No verdict in §2 comes
from the purged pass; the purge is reported because it can silently eat other
seats' evidence.

F5 — observation only: the committed base receipt
`.ufo/evidence/round-55/before/c2.stdout` shows `lazy=5/5 empty=13/13
usable=13/13` under the **freeze** counter at base, i.e. with the detached
checkout amendment 1 replaced; amendment 1's symptom ("the lazy and empty arms
measured the clone instead of the tool") does not reproduce from that receipt.
Not claiming the amendment is wrong — only that this seat could not reproduce
it at base.

## 7. Not done / out of scope

- No lane production file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`,
  `tools/**`) was edited; the five-file integration state I scored is the bytes
  I found, not authored here.
- No build/lint/test run: the wave forbids it for leaf seats and the counter is
  the instrument this item names.
- The C1 counter was not exercised (not this item).
