# Round-35 w2 — AttackArithHash

Seat: `tameshi-r35-w2-AttackArithHash` (leaf mutation-tester, godspeed). Lane pin at dispatch and at
every command below: **`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`** (clean `git status`, re-cloned in
scratch after the pre-existing lane was found stale at `d16f9b5a`).

Slice assigned: **`code_view`'s word-start rule** — does a `#` after `=`, `((`, `[[`, `${{`/`${`, or a
backslash behave as bash does? Build runner copies (two inert, two divergent) at those positions and
report, per copy, bash's reading vs `code_view`'s blanking vs the tool verdict.

Frozen bytes used (sha256, verified before and after; the lane was never written):

| artifact | sha256 |
|---|---|
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` |

Environment: bash `5.3.20(1)-release`, Python `3.14.8`, linux `7.2.11-arch1-1`. All scratch under
`/fast/scratch/hyaku/tameshi-r35-seats/AttackArithHash/` (`lane/` read-only; copies in `copies2/`;
findings prose in `out/`, probes in `work/`). No installs, no `pacman`, no git/jj mutation, no writes
under `/home/vgpnk/Projects/shokunin/` except this report.

---

## 1. What the rule is, and what it is not

`tools/tally-audit-v3.py:150-190` (`code_view`), delimiter test at **line 185**:

```python
if c == '#' and (i == 0 or text[i - 1] in ' \t\n;|&('):
```

The docstring claims the POSIX word-start set: *"at the beginning of the text or after whitespace or
one of `;|&(`"*. The actual POSIX/bash word-start condition is *not* a fixed set of characters: a `#`
begins a comment only when it is at the start of a **token**, and token starts are decided by the
lexer's current context — including `)` (metacharacter after a complete compound command), `>`/`<`,
arithmetic context inside `(( ))`/`$(( ))`, `${...}` offset arithmetic, and quote/escape state.

The rule drives every structural scan: `regression_body` (brace counting), `tally_block`,
`head_section`/`leg_names`, `counting_case`/`tally_loop`, and `check_head`'s substring counts
(`check_head` at line 432; `cnt = head_code.count(nm)` at line 459). The frozen C1 counter duplicates
this function **behaviorally identically**
(`.ufo/evidence/round-35/c1/c1-measure.py:95-129`, delimiter at **line 121**; 20,000-input
differential fuzz, 0 mismatches — §5).

## 2. Method

1. **Lexical matrix against real bash** (`work/lexprobe2.py`, exit 0 → `out/lexmatrix2.txt`): each
   snippet is executed under bash, then passed through the tool's own `code_view`; the first `#` is
   classified bash-comment vs bash-code and blanked vs not.
2. **Ten runner copies** (`work/build_copies.py`, exit 0 → `out/copies2-build.txt`): every copy is one
   minimal edit to the pinned runner; `bash -n` exit 0 for all; the builder is deterministic and its
   hashes match the copies that were measured.
3. **Independent behavioural detector** (`work/behave.py`, exit 0 → `out/behave.txt`):
   - *head detector*: extracts `run_regression`'s head and executes it with stubbed helpers
     (`regression_case_git(){ return 0; }`, etc.), printing all nine captured leg statuses;
   - *block detector*: extracts the tally block and runs it under **all four (auto,KEEP) triples**
     with a real `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` auto root, over 41 vectors
     (all-zero; 1/2/3/255 at each of 9 positions; four mixed), comparing `(exit, FULL stdout)`.
4. **Tool verdict** (`python3 lane/tools/tally-audit-v3.py --runner <copy>`, exact exits below).

Baseline: pristine `TALLY_AUDIT: PASS`, **exit 0**, `runtime vectors=30316 mismatched=0`
(`out/verdict-mutate-and-run.out`). The detector is not trivially failing.

## 3. Per-copy results

| copy | sha256 (short) | position | bash's reading | `code_view` blanking | behaviour (independent) | tool verdict |
|---|---|---|---|---|---|---|
| **A** `inert-paren-comment` | `2d59c667…` | `)` | `( : )# st_js …` — `#` after a complete subshell starts a word → **comment** (inert) | **kept** (`# st_js …` survives; `head_cv_st_js=3`) | head identical to pristine (all legs 0); block sha identical | **FAIL exit 1** `CHECK head FAIL … leg st_js appears 3 times` |
| **A2** `inert-paren-space-comment` | `78ca85bf…` | `)` control | same comment after a space → comment (inert) | blanked (`head_cv_st_js=2`) | identical | **PASS exit 0** |
| **B** `inert-eq-literal` | `bb642233…` | `=` | `local hnote=#abc` — literal value (inert) | **kept** (correct) | identical | **PASS exit 0** |
| **C** `divergent-backslash-hides-assign` | `6811269b…` | `\` | `X=1\`⏎`#; st_mado=1` — continuation joins to `X=1#; st_mado=1`; `#` mid-word **literal**, `;` executes `st_mado=1` | **blanked** (cv line all spaces) | **head DIFF: `mado=1`** vs pristine 0; block sha identical | **PASS exit 0** |
| **C2** `inert-backslash-space` | `a2039799…` | `\` control | `X=1 \`⏎`#; st_mado=1` joins to `X=1 #…` → comment (inert) | blanked (correct) | head identical (`mado=0`) | **PASS exit 0** |
| **D** `divergent-arith-guard-inverted` | `d9497de0…` | `((` | guard `!=` → `==`: all-zero flips PASS→SETUP mismatch | n/a (raw block executed) | **block DIFF**: `0 PASS` → `2 SETUP` on all-zero | **FAIL exit 1** `runtime 112 mismatched` |
| **E** `divergent-bracket-fail-threshold` | `17496eb0…` | `[[` | `$nfail -gt 0` → `-gt 1`: one failing leg falls through to PASS | n/a | **block DIFF**: `1 FAIL` → `0 PASS` on every `one-1@pos` | **FAIL exit 1** `runtime 3276 mismatched` |
| **F** `inert-brace-dead-quoted` | `d443befd…` | `${` | dead `: "${x: #lit}"` — never evaluated (inert) | kept (quote-aware, correct) | identical | **PASS exit 0** |
| **G** `inert-brace-dead-unquoted` | `bac1ef53…` | `${` | dead `: ${x: #lit}` — never evaluated (inert) | **blanks `#lit}` incl. the closing brace** → unbalanced | identical | **SETUP exit 2** `run_regression() has unbalanced braces` (39 ms) |
| **H** `divergent-visible-head-overwrite` | `79184d02…` | (control for C) | `st_claims=$?` then `st_claims=0` — overwrite is visible code | kept (code) | **head DIFF: `claims=0`** vs pristine `claims=1` when the claims case is stubbed to fail | **FAIL exit 1** `CHECK head FAIL … non-bare … assigned 2 times … appears 3 times` |

Copy edits (exact, from `out/copies2-build.txt`):

```
A  +  ( : )# st_js is captured above
A2 +  ( : ) # st_js is captured above
B  +  local hnote=#abc
C  +  X=1\            (line ends at the backslash)
   +#; st_mado=1      (column 0)
C2 +  X=1 \           (space before backslash)
   +#; st_mado=1      (column 0)
D  -  if (( npass + nfail + nsetup != nlegs )); then
   +  if (( npass + nfail + nsetup == nlegs )); then
E  -  if [[ $nfail -gt 0 ]]; then
   +  if [[ $nfail -gt 1 ]]; then
F  +  if false; then
   +    : "${x: #lit}"
   +  fi
G  +  if false; then
   +    : ${x: #lit}
   +  fi
H  +  st_claims=0        (immediately after `  st_claims=$?`)
```

## 4. Findings

### CRITICAL-1 — false-accept: a head-level leg rewrite hidden by backslash-newline blanking (copy C)

A kill specimen is **accepted** (`TALLY_AUDIT: PASS`, exit 0).

- **bash's reading** (verified three ways): the isolated snippet prints `ST_MADO=1`, the head detector
  on the real copy prints `LEGS … mado=1 …` (pristine 0), and `bash -n` accepts the copy. The line
  continuation removes `\`⏎ without inserting whitespace, so `#` follows `1` mid-word and is literal;
  the following `;` terminates the assignment, then `st_mado=1` executes *after* the capture.
- **`code_view`'s reading**: it skips the backslash and newline and then tests the *raw* previous
  character — `\n` — so it blanks `#; st_mado=1`. `CHECK head` sees only `  st_mado=$?` (bare,
  two occurrences) and passes.
- **Why the tool cannot notice otherwise**: the block bytes are identical to pristine
  (`block_sha e163133c0f54bb0c…`, verified by both the tool's cutter and the counter's cutter), and the
  `runtime` oracle executes **only the block**. Head semantics are covered by the static head check
  alone, so hiding code from `code_view` is sufficient.
- **The same defect made visible is killed** (executed control, copy H): `st_claims=$?` followed by a
  plain `st_claims=0` is rejected with `CHECK head FAIL … non-bare leg assignment(s) … assigned 2
  times … appears 3 times`, **exit 1**. Its behavioural divergence is real — with the claims case
  stubbed to fail, pristine yields `claims=1` and H yields `claims=0` (same head detector, one stub
  changed). C is the identical status rewrite with the `st_mado=1` line hidden from `code_view`, and it
  is accepted (exit 0). This also matches the tool's own `head overwrite` selftest seed
  (`tally-audit-v3.py:768`, expected exit 1, check `head`).
- **The deciding measurement shares the blind spot**: `c1-measure.py`'s behavioural ground truth
  (`run_block`) also executes only the block and its `code_view` is behaviourally identical, so it
  would label C an accept — matching the tool's accept. The false accept is invisible to the C1
  measurement, not just to the tool.
- Minimal pair **C2** (space before the backslash) joins to `X=1 #…`, a real comment: head `mado=0`,
  tool PASS. The only difference is the lexer rule that a continuation joins flush.

### CRITICAL-2 — false-kill: a comment introduced immediately after `)` is counted as code (copy A)

A behaviourally identical copy is **FAILed** (`CHECK head FAIL`, exit 1).

- bash: `)` closing a complete subshell command is a metacharacter; `# st_js …` starts a word and is a
  comment. Head detector on copy A is byte-identical to pristine (all legs 0); `bash -n` clean.
- `code_view`: `)` is not in `' \t\n;|&('`, so the comment text survives and
  `head_code.count('st_js') == 3`; `CHECK head` fails with *"leg st_js appears 3 times in the head"*.
- The tool's own accept seed `comment names a leg` (line 782) asserts this exact comment is inert when
  introduced after whitespace. Minimal pair **A2** (space before `#`) is blanked, passes `check_head`,
  and the tool verdict is **PASS exit 0** — the delimiter is the sole cause.
- The same class is reachable from an arithmetic-command close (`(( … ))#…`: probe row
  *arithmetic close then hash*, bash rc 0 comment, `code_view` keeps it).
- This is the round-34 false-kill class the round-35 fix claims to close; it reopens through `)`.

### CRITICAL-3 (fail-closed) — refusal of an inert copy via `${…}` offset arithmetic (copy G)

Copy G (`if false; then : ${x: #lit}; fi`) is behaviourally identical — `bash -n` clean, branch never
executed, head detector identical, block identical — but:

- `code_view` treats `#` after a space as a comment **ignoring that the text is inside `${…}` offset
  arithmetic**, where bash does not recognise comments (if evaluated, bash reports
  `x: #lit: arithmetic syntax error`). It blanks `#lit}` **including the closing brace**;
  `regression_body` then reports `unbalanced braces`.
- Tool: `TALLY_AUDIT: SETUP (run_regression() has unbalanced braces)`, exit 2. The contract's
  C1 falsifier list includes *"an accept specimen the tool kills or refuses (rc != 0)"*, so the literal
  predicate is false; the direction is fail-closed (no defect passes), which is why this ranks below
  -1/-2 in consequence. The frozen counter's own `tally_block` raises the identical SETUP on the same
  bytes (verified), so a G-like sealed copy would **abort the deciding measurement** rather than be
  scored.
- Minimal pair **F** (quoted `"${x: #lit}"`) shows the quote-aware half is sound: `code_view` leaves it
  alone and the tool PASSes (exit 0). Only the unquoted arithmetic context is misread.

### BOUND — `>` / `<` / `<<<` are missing from the set, but no valid runner can exploit it

`printf 'X\n' >#c` and `<#c` and `cat <<<#c` are bash **syntax errors** (rc 2, "unexpected token
`newline`"): bash treats the `#` as a comment after the redirection operator, leaving no target. Since
valid bash cannot carry a bare `>#comment`, the divergence (`code_view` keeps the text) cannot move a
verdict on a valid copy. Recorded as a real but unreachable gap.

The arithmetic false-blank (`(( n = 1 # C … ))`: bash arithmetic error, `code_view` blanks) is likewise
limited to code that errors in bash when evaluated; the only weaponisable form is a dead branch, which
lands in the CRITICAL-3 refusal class, not a false accept.

### HYGIENE — the rule is duplicated in the frozen counter

`tools/tally-audit-v3.py:185` and `.ufo/evidence/round-35/c1/c1-measure.py:121` carry the same
delimiter set; the bodies differ only in docstring/style (differential fuzz below). Any fix must be
applied to both files or the tool and the ground truth diverge. Note also that the counter's ground
truth never executes the head, which is precisely why CRITICAL-1 is invisible to the measurement.

## 5. What I could NOT break (with the proof)

- **Pristine baseline**: `TALLY_AUDIT: PASS`, exit 0, `vectors=30316 mismatched=0` (`out/verdict-mutate-and-run.out`).
- **`=` position** — agrees: copy B (`local hnote=#abc`) is inert and **PASS exit 0**; probe rows
  `x=#lit` → bash `X=#lit`, `a=#lit` → `X=a=#lit`, `x=1 #C` → comment; `code_view` matches in all three.
- **`[[` position** — agrees on word-start: `[[ foo == #* ]]` (bash: `#` starts a comment, swallows
  `]]`, rc 2; `code_view` blanks), `[[ foo ==#foo ]]` (bash: operator token, rc 2; `code_view` keeps),
  `[[ -n x && #c ⏎ -n y ]]` (both comment, rc 0). Divergent copy **E** is correctly killed
  (`runtime`, 3276 mismatches, exit 1), so the `[[` axis is both read correctly and defended.
- **`${{`/`${` positions** — agrees except the unquoted offset form: `${{#}}` (bash bad substitution,
  `code_view` keeps), `${#x}` → 3, `${x#a}` → bc, `${x/#a/Z}` → Zbc, `${unset:-#lit}` → `#lit`
  (all `code_view`-keeps, bash-code). Quoted `${x: #lit}` (copy F) accepted, PASS exit 0.
- **`((` position** — valid arithmetic agrees: `$((2#101))` → 5, `code_view` keeps. Divergent copy
  **D** is correctly killed (`runtime`, 112 mismatches, exit 1).
- **Backslash escapes** — agrees: `\#esc` → `#esc`, `a\#b` → `a#b` (`code_view` keeps); continuation
  with a space before the backslash (copy C2) → both comment, head `mado=0`, PASS exit 0.
- **`#` after `)` inside a word** — agrees: `x=$(echo hi)#tail` → bash `X=hi#tail` (the `#` continues
  the same word), `code_view` keeps it. Only a `)` that *closes a command* (subshell / arithmetic
  command) begins a word — exactly the CRITICAL-2 case.
- **Runtime oracle depth**: both correctly-killed divergent copies fail under `runtime` as the *only*
  failing check, satisfying the contract's "failing check exactly `runtime`"; 30,316 vectors × 4
  triples, with a real `/tmp/tameshi-r4-2-regression.XXXXXX` auto root.
- **Rule equivalence tool↔counter**: 20,000 random inputs over an alphabet containing `# \ ' " ; | & ( ) { } = $ : < >` and
  multi-char tokens (`16#ff`, `\⏎`, `) #`, `${{`, `[[ `): **0 mismatches**.
- **Copy C's counter-side blindness** (proof, not inference): `c1-measure.tally_block` on A, C and
  pristine returns block sha `e163133c0f54bb0c…` for all three; on G it raises
  `SETUP: unbalanced run_regression braces`.
- **Pinned bytes / restoration**: before and after every run,
  `sha256sum lane/tools/tally-audit-v3.py lane/tools/mutate-and-run.sh` =
  `ef98fc53…` / `a7d3f2dd…`; `git -C lane status --porcelain` = 0 lines; the lane was never mutated —
  each mutant is a separate file under `copies2/`, so "restoration" is the untouched pristine lane
  plus the recorded copy hashes above.

## 6. Exact commands and exits

| command | exit |
|---|---|
| `git clone --no-hardlinks … lane && git -C lane checkout -q --detach 7da6e076…` | 0 |
| `python3 work/lexprobe2.py` (matrix → `out/lexmatrix2.txt`) | 0 |
| `python3 work/build_copies.py` (ten copies, `bash -n` all rc 0 → `out/copies2-build.txt`) | 0 |
| `python3 work/probe_copies.py` (cv facts + `check_head`/`check_static` → `out/probe-copies.txt`) | 0 |
| `python3 work/behave.py` (head + 41 vectors × 4 triples → `out/behave.txt`) | 0 |
| `python3 lane/tools/tally-audit-v3.py --runner lane/tools/mutate-and-run.sh` | 0 |
| `… --runner copies2/A-inert-paren-comment.sh` | 1 |
| `… --runner copies2/A2-inert-paren-space-comment.sh` | 0 |
| `… --runner copies2/B-inert-eq-literal.sh` | 0 |
| `… --runner copies2/C-divergent-backslash-hides-assign.sh` | **0** |
| `… --runner copies2/C2-inert-backslash-space.sh` | 0 |
| `… --runner copies2/D-divergent-arith-guard-inverted.sh` | 1 |
| `… --runner copies2/E-divergent-bracket-fail-threshold.sh` | 1 |
| `… --runner copies2/F-inert-brace-dead-quoted.sh` | 0 |
| `… --runner copies2/G-inert-brace-dead-unquoted.sh` | 2 |
| `… --runner copies2/H-divergent-visible-head-overwrite.sh` | 1 |
| `python3 work/claims_stub.py` (claims leg stubbed to fail; pristine vs H → `out/claims-stub.txt`) | 0 (claims 1 vs 0) |
| differential `code_view` fuzz (20,000 inputs) | 0 mismatches |

Per-copy tool output is preserved at `out/verdict-<copy>.out`; the aggregate table at `out/verdicts.txt`.

## 7. Verdict on the claim

The round-35 fix's stated guarantee — *"all structural scans run on a quote-aware code view with
comments blanked"*, so *"inert comment text cannot kill or refuse a behaviorally pristine copy"* and a
divergent copy cannot hide — is **false** beyond its simulated delimiter set:

- a kill specimen is **accepted** (C: `PASS`, exit 0; head leg forced to 1 while the tool sees a clean
  head) — the exact silent-defect-masking direction the tool exists to prevent;
- an inert copy is **killed** (A: `FAIL`, exit 1) via comment text counted as code;
- an inert copy is **refused** (G: `SETUP`, exit 2), the fail-closed variant of the same
  context-blindness.

The `=` and `[[` positions, escaped `#`, `${#…}`/`${x#…}`/`${x/#…/…}`/`${x:-#…}`, valid base-`#`
arithmetic, and quoted `${…}` all behave correctly and are proven so above. The failure is not the
quote/escape state machine (sound) nor the runtime oracle (kills D and E exactly as required); it is
the claim that a fixed character set plus quoting is a complete model of "start of a word" — bash's
token start is contextual (compound-command close, `${…}` arithmetic, line continuation), and the
duplicated frozen counter inherits every miss.
