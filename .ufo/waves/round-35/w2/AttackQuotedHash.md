# Round-35 w2 — AttackQuotedHash

Seat: `tameshi-r35-w2-AttackQuotedHash` (leaf mutation tester, godspeed). Lane checkout at
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (detached), **read-only: no commit, no write inside the
checkout**. All scratch under `/tmp/scratch-r35/AttackQuotedHash/` (fallback: `/fast` is at 100%,
2.4G free — see §8). No tool installs; `pacman` untouched.

Slice assigned: **the round-35 comment-blanking (`code_view`) for FALSE NEGATIVES** — a `#` that
bash treats as literal data is blanked as if it were a comment, and a real divergence is hidden.

Pins re-hashed at the tip before and after every run (`git show 7da6e07:<path> | sha256sum` and the
working tree agree; lane `git status --porcelain` = empty):

| artifact | sha256 |
|---|---|
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` |
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` |

---

## 0. Verdict

**CRITICAL — false accept, three specimens SURVIVED.** The round-35 fix #3 ("comment-blind
scanning", `tools/tally-audit-v3.py:150-194`) mis-lexes four reachable shell constructs and blanks
**real code** as comment text. The blinded scan is `check_head` (`:432`), whose twice-only leg-name
rule (`:453`) is the tool's *only* defence against out-of-block masking of a leg status. Three
copies whose runner verdict flips **FAIL→PASS** (exit 1→0) and **SETUP→PASS** (exit 2→0) are
accepted by v3 with `TALLY_AUDIT: PASS`, exit 0. The same mask written in a correctly-lexed
construct is killed — the blanking is load-bearing.

Mirror direction, **also CRITICAL/BOUND**: the same lexer *under*-blanks after an ANSI-C literal
(`$'it\'s'`), so an inert comment naming a leg — the exact round-34 false-kill class the fix claims
to have closed — still kills a behaviorally pristine copy. The frozen counter's own `score_copies`
scores that copy `valid=True, pass=False` (`COPY accept … rc=1 checks=head pass=False`), i.e. this
direction is expressible as a sealed **accept** specimen and would fail C1.

Honest scope note: C1's literal predicate defines a kill specimen by **tally-block** behaviour
(`c1-measure.py:1-20` docstring; `:204-219` `behavior`/`diverge`), so a head-only defect is not a
"kill" by that definition and would score `INVALID` rather than caught (§5.1, reproduced). The
false accept is therefore a hole in the
**tool's** documented `head` guarantee (docstring: "head … Catches out-of-block masking/overwrites
of leg statuses") introduced by fix #3 — and that gap between the tool's stated coverage and the
counter's block-only ground truth is itself part of the finding.

---

## 1. What `code_view` does and where it diverges from bash

`tools/tally-audit-v3.py:150-194` is a flat state machine with one global `quote` variable:

```python
if quote == "'":                       # :165  single quotes: backslash is NOT special here
    if c == "'": quote = None
    ...
if quote == '"':                       # :170  double quotes: only \ and " special
    ...
if c == '\\' and i + 1 < n:            # :178  top-level backslash: skip 2 chars
    i += 2; continue
if c == "'" or c == '"': quote = c     # :182  quote state, global, survives newlines
if c == '#' and (i == 0 or text[i-1] in ' \t\n;|&('):   # :185
    blank to end of line               # :189
```

Bash does not have one quote register: `$'…'` processes backslash escapes *inside* the string,
`$(…)`/backticks restart quoting inside themselves, and `\`+newline is removed before tokenisation.
The machine below therefore steps out of (or into) a string at the wrong offset. Both the tool and
the frozen counter carry the same machine (`c1-measure.py:95-131`; semantically identical, only
docstring/formatting differ — verified by AST source extraction + `difflib`).

Probe (`work/probe_cv.py`, both modules give the same column):

| construct (bash: `#` is DATA) | bash proof (exit 0) | `code_view` | `st_tsu` visible? |
|---|---|---|---|
| `: $'don\'t reorder # '; st_tsu=0` | `st=0` | blanks `# '; st_tsu=0` | **no** |
| `: "note $(printf %s "n # 1")x"; st_tsu=0` | `st=0` | blanks `# 1")x"; st_tsu=0` | **no** |
| `printf '%s' foo\`⏎`#bar; st_tsu=0` | prints `foo#bar` | blanks `#bar; st_tsu=0` | **no** |
| `: ${X:-$'a\'b # '}; st_tsu=0` | `D st=0` | blanks `# '}; st_tsu=0` | **no** |
| `: $'it\'s' # st_tsu comment` (real comment) | comment inert | does **not** blank | yes (leak) |
| `: 'x # y'; st_tsu=0` | `st=0` | not blanked (correct) | yes |
| `: "x # y"; st_tsu=0` | `st=0` | not blanked (correct) | yes |
| `: "x" # st_tsu comment` (real comment) | comment inert | blanked (correct) | no |

Bash evidence, verbatim: `bash -c ': $'"'"'don\'"'"'t reorder # '"'"'; st=0; echo "st=$st"'` → `st=0`;
`bash -c 'st=1; : "note $(printf %s "n # 1")x"; st=0; echo "st=$st"'` → `st=0`;
`printf 'bash -c "printf %s foo\\\n#bar"\n' | bash` → `foo#bar`; `bash d.sh` → `D st=0`.
(Full transcript reproduced in §9.)

---

## 2. Specimens

Every specimen is the pinned runner plus **one inserted physical line** in
`run_regression`'s head, after `st_citecheck=$?` (runner line 1430), before `local nlegs=9`.
`bash -n` clean; extracted **tally block bytes are identical to pristine in every specimen**
(sha256 `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`, verified with the tool's
own `regression_body`/`tally_block`; `work/blockcmp.py`).

| specimen | inserted line | sha256 |
|---|---|---|
| pristine | — | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| A_ansiC | `  : $'don\'t reorder the legs # '; st_tsu=0` | `24b14bba7d24e062caaf3ea562da150ea8c95a539abeabb1845c5e78969f1aa8` |
| B_nesteddquote | `  : "note $(printf %s "n # 1")x"; st_tsu=0` | `771c26697032c46c3591cc7f53ea4e2548b3a2774201b18b2d08e4b42d51d71a` |
| C_linecont | `  printf '%s' foo\` ⏎ `#bar >/dev/null; st_tsu=0` | `5ed1ae2fb7ac3bdc1b41c3ea6e88107bfc51af17cbbd01924a86fae52248d2ba` |
| D_parambranch | `  : ${X:-$'a\'b # '}; st_tsu=0` | `6c8f9a574d7fb6ef292c3698386edc713cdc99b6fa52237ba32d58bf7f646d5c` |
| E_singlequote (control) | `  : 'x # y'; st_tsu=0` | `e01855a2f9fcbd61b0aa961ab9dbfb09ef6e310291852b5862af1d6c00e57cb2` |
| H_plainmask (control) | `  : "x"; st_tsu=0` | `ab62800c3b54e28b271dc3523fc630ae4e70a08a2e30c5167236779d2865042e` |
| K1_plaincomment (control) | `  : "x" # st_tsu is counted by the loop below` | `dfb5ea8a46869c3b8838e6bf6dfe1b8c8862e8972e783bdb1c6ff6d03364b376` |
| K2_quoteleak (control) | `  : $'it\'s' # st_tsu is counted by the loop below` | `f201e1bb4d57344a3b50e851d125fb3e05abfcb7f48a132ae95b7c768330ea52` |

A/B/C/D hide an executed `st_tsu=0`; E/H hide the *same* executed mask but in a correctly-lexed
(or no-) quote context; K1/K2 add an **inert** comment (they do not mask anything).

---

## 3. Detector 1 — the tool itself (same command for every specimen)

```
$ cd <lane> && python3 tools/tally-audit-v3.py --runner <specimen>
```

| specimen | tool output tail | exit | verdict |
|---|---|---|---|
| pristine | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 0 | baseline PASS (not inconclusive) |
| **A_ansiC** | same PASS line | **0** | **SURVIVED (false accept)** |
| **B_nesteddquote** | same PASS line | **0** | **SURVIVED (false accept)** |
| **C_linecont** | same PASS line | **0** | **SURVIVED (false accept)** |
| **D_parambranch** | `TALLY_AUDIT: SETUP (run_regression() has unbalanced braces)` | 2 | **fail-closed refusal** (not an accept; see §4.2) |
| H_plainmask | `CHECK head FAIL legs=9; leg st_tsu appears 3 times in the head (want exactly 2: …)` → `TALLY_AUDIT: FAIL (head=fail …)` | 1 | KILLED |
| E_singlequote | identical head FAIL | 1 | KILLED |
| K1_plaincomment | `TALLY_AUDIT: PASS` | 0 | accepted (correct — fix's target class) |
| **K2_quoteleak** | `CHECK head FAIL … leg st_tsu appears 3 times …` | **1** | **FALSE KILL (inert comment)** |

Logs: `work/audit-pristine-A.log`, `work/audit-B-C.log`, `work/audit-controls.log`,
`work/audit-K.log` (+ the D run quoted above). Each non-pristine run re-ran
`runtime` (the tool's own `vectors=30316`: 30,244 vector runs across the four configs + 72 operand
stress runs) and `harness` (9 cases, 34/34 faults): both PASS on A/B/C, because they are untouched —
the divergence lives in the head.

Cause isolated without the tool's CLI (`work/headly.py`): `check_head` with the shipped view vs. the
same function with `code_view` replaced by identity (pre-round-35 behaviour):

| specimen | shipped `code_view` | identity view |
|---|---|---|
| pristine | PASS | PASS |
| A / B / C | **PASS** | FAIL — `leg st_tsu appears 3 times in the head` |
| H / E | FAIL | FAIL |

So the only reason A/B/C survive is the blanking; the pre-fix scan would have killed all three.

---

## 4. Detector 2 — behaviour: the copies really diverge

### 4.1 Witness shim (`work/witness.sh`)

Runs the copy's **own** `run_regression` source (head + tally block, extracted verbatim by brace
range) with the nine leg commands replaced by a stub returning injected statuses; nothing else is
altered. Same driver for pristine and mutants.

```
$ WIT_WD=<fixed dir> bash witness.sh <specimen> 0 0 1 0 0 0 0 0 0     # leg 2 (tsu) fails
pristine   RC=1 REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
A_ansiC    RC=0 REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
$ WIT_WD=<fixed dir> bash witness.sh <specimen> 0 0 0 0 0 0 0 0 0     # all pass
pristine   RC=0 … PASS …      A_ansiC RC=0 … PASS …        (identical)
$ WIT_WD=<fixed dir> bash witness.sh <specimen> 2 2 2 2 2 2 2 2 2     # all setup
pristine   RC=2 REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)
A_ansiC    RC=2 REGRESSION: SETUP (cases=9 passed=1 cannot-verify=8)
$ WIT_WD=<fixed dir> bash witness.sh <specimen> 0 0 255 0 0 0 0 0 0   # tsu status 255
pristine   RC=2 SETUP (cases=9 passed=8 cannot-verify=1)
A_ansiC    RC=0 PASS  (cases=9 passed=9 …)
$ WIT_WD=<fixed dir> bash witness.sh <specimen> 1 0 1 0 0 0 0 0 0     # two failing legs
pristine   RC=1 FAIL (cases=9 passed=7 failed=2 setup=0)
A_ansiC    RC=1 FAIL (cases=9 passed=8 failed=1 setup=0)
```

That is the round-34/round-35 kill-rate-masking class: a failing leg and a cannot-verify leg
**disappear** (exit 1→0, exit 2→0). All-pass is bit-identical, so A/B/C are not merely noisy.

### 4.2 The `${…}` variant (D) is fail-closed, and says why

`${X:-$'a\'b # '}` puts `{` before the misparsed `#` and `}` after it, so the view keeps an
unmatched `{`; `regression_body` (`:196`) stops one brace short and the tool exits 2 with
`SETUP (run_regression() has unbalanced braces)` — a refusal, not a false accept. Its behaviour
still diverges (witness: RC 1→0 and `passed=1 cannot-verify=8`), so the construct is a real
divergence that the tool *cannot audit* rather than accepts. Any attempt to rebalance the braces
either ends the body early or blanks both braces (net zero), which is the A-class again — so the
`${…}` shape does not widen the false-accept class. **BOUND (fail-closed).**

### 4.3 Whole runner, no shim

Both copies in sibling layouts (`sib-pristine/tools/`, `sib-mutantA/tools/`), invoked identically
with `--regression --workdir <same>` so `SELF` and `FLEET_ROOT` resolve identically:

```
$ diff sib-pristine.out sib-mutantA.out
1c1
< REGRESSION_TOOL: …/sib-pristine/tools/mutate-and-run.sh sha256=a7d3f2dd…912eb9
---
> REGRESSION_TOOL: …/sib-mutantA/tools/mutate-and-run.sh sha256=24b14bba…1aa8
14c14
< REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)
---
> REGRESSION: SETUP (cases=9 passed=1 cannot-verify=8)
```

Both exit 2; every `REGRESSION_CASE` line identical; full stdout differs in the tally line, which
is a divergence under the tool's own round-35 full-stdout rule. (The `REGRESSION_TOOL` line differs
by path+sha, which is the specimen's byte identity, not behaviour.)

---

## 5. Detector 3 — the frozen counter's view of these specimens

### 5.1 Ground truth is block-only

`c1-measure.py:204` `behavior()` = `tally_block` + `leg_names` + `run_block`; `diverge()` compares
those tuples. Imported the frozen counter and scored the mutant bytes directly (`work/ctr.py`):

```
A_ansiC          diverged_configs=[] (counter ground truth)
B_nesteddquote   diverged_configs=[]
C_linecont       diverged_configs=[]
H_plainmask      diverged_configs=[]
```

**BOUND (measurement coverage):** a head-side kill cannot be a valid sealed kill specimen — the
counter computes divergence on the block only, and the block bytes are identical. The tool's `head`
guarantee is therefore *unmeasured* by C1 as frozen; the deciding run can be green while this hole
is open.

### 5.2 The false-kill direction *is* measurable

`c1-measure.py:285` `score_copies` with an **accept** copy built from K2's edit and a **kill** copy
from A's edit, tool = frozen v3 (`work/ctrscore.py`):

```
COPY accept K2-accept-inert-comment-after-ansic ? div=- rc=1 checks=head pass=False
COPY kill  A-head-mask-ansic                 ? div=- rc=0 checks=-    pass=False
  INVALID: kill copy without behavioral divergence
valid flags: [('K2-…', True, False), ('A-…', False, False)]
```

K2 (`valid=True` = behaviourally identical, block bytes shared with pristine) is **failed by the
tool** (`rc=1`, check `head`). Under the sealed rule that is a legitimate accept specimen, and the
after-target (`ho_accept=a/a`) would miss it.

---

## 6. Cause, ranked

### CRITICAL-1 — `$'…'` escape, nested `$( )` quotes, and `\`+newline blank real code; head masking becomes invisible
`code_view`'s single-quote branch (`:165-169`) ignores `$'…'` backslash escaping (`\'` closes the
string in the view, not in bash); its double-quote branch (`:170-177`) closes the string on a quote
that bash treats as opening a nested string inside `$(…)`; its top-level `\` branch (`:178-180`)
skips the newline but leaves it as the "previous character", so `#` after a continuation is judged a
word start. Any of the three makes the rest of a physical line vanish from `check_head`. A
one-line insertion (`st_tsu=0` after the literal `#`) then masks a failing/setup leg with the tool
reporting `TALLY_AUDIT: PASS`, exit 0 (A/B/C). Fix #3's premise ("comment text is never code")
is applied as "blanked text is never code" — false for literal data.

### CRITICAL-2 / BOUND — under-blanking after `$'it\'s'` reopens the round-34 false-kill class
Because the `$'…'` branch closes early, the *next* quote (the `'` of an apostrophe-containing word)
re-opens a quote that bash never opened, and the machine stays inside it **across newlines**
(`:182`, no per-line reset). Every subsequent real comment is left visible. K1 (plain inert comment
naming `st_tsu`) is accepted; K2 (the same inert comment after `  : $'it\'s'`) is killed with
`leg st_tsu appears 3 times in the head`. Both are behaviourally pristine (witness identical on
`0 0 1 …` and `2 2 2 …`; block sha identical). This falsifies the docstring sentence "so inert
comment text cannot kill or refuse a behaviorally pristine copy" (`:158-159`) and is directly
scored `pass=False` by the frozen counter (§5.2). Fail-closed, hence BOUND rather than claim-breaking
— but it is the *same* bug and it is expressible in the sealed set.

### BOUND — the counter duplicates the lexer
`c1-measure.py:95-131` is the same machine (AST-extracted sources differ only in docstring and
formatting; both blank the same four probe lines, §1). Today the counter's ground truth is
behavioural, so no measurement is affected; any future use of its `tally_block`/`leg_names` as a
gate (it is already used for head/block cutting at `:132-152`) inherits the blind spot.

### HYGIENE — the fix's selftest cannot see either direction
`selftest()` (`:729`) seeds exactly one head-masking case, `('head masked', '  st_kagi=$(($? & 127))', 1, 'head')`
(`:762`) — a *visible* line-initial rewrite — and three inert-comment accepts in plain form
(`:782-786`) plus `('comment names real root', …)` (`:790`). No seed places a literal `#` in code
and no seed exercises `$'…'`, `$( )`-nested quotes or a line continuation, so both findings are
outside the tool's own test space. Recommended (not performed): add adversarial accept/kill seeds for
the five constructs of §1 and make `code_view` model `$'…'`, `$"…"`, `$(…)`/backtick/`${…}` nesting
and `\`+newline removal.

---

## 7. What I could NOT break (with proof)

- **Plain single quotes and plain double quotes** hold `#` as data and the view agrees:
  `: 'x # y'; st_tsu=0` and `: "x # y"; st_tsu=0` stay visible → the mask is KILLED (E; H for the
  unquoted control). Blanking a real comment is correct (`: "x" # st_tsu …` → blanked, K1 accepted).
- **The word-start set is operationally correct.** `code_view` omits `)`, `<`, `>` from
  `' \t\n;|&('`; bash probes show none of them starts a comment: `echo $(true)#abc` prints `#abc`
  (one word), `{ echo a; }#abc` and `echo hi >#f` / `<#f` are syntax errors (the `#` is a comment
  *only* because the redirect then lacks its target — i.e. `>#` cannot occur in a valid runner).
  So no over-capture false kill is reachable through those characters.
- **No block-level divergence can hide behind the blanking.** `tally_block` returns raw bytes
  (`:229-237`); `runtime` executes them verbatim, and all specimens' block bytes are identical to
  pristine. Extraction tricks are fail-closed: hiding the final `}` is impossible (it is alone on
  its line), hiding a `{` shifts `regression_body` and yields `SETUP`/`CannotAudit` (D is the live
  example: exit 2), and a decoy `local nlegs=` inside a string/heredoc makes `head_section`/`static`
  inconsistent (`nlegs` is read from raw text at `:474`). I did not find a spanning trick that both
  parses and diverges.
- **A4/A5 apparatus** was not the object of this probe; the root-keyed and sealed-provenance
  classes were left to their own seats. The A4 real-auto-root sweep is unaffected: A/B/C diverge
  identically under the explicit `--workdir` runs of §4.3 (no root gate involved).

---

## 8. Environment notes, restoration, reproduction

- `/fast` at 100% (2.4G free, `df -h /fast`). The pre-created lane at
  `/fast/scratch/hyaku/tameshi-r35-seats/AttackQuotedHash/lane` was **unusable**: `git checkout
  7da6e07` failed with `fatal: unable to read tree (7da6e07…)` (partial clone). Per the lane bounds
  I fell back to `/tmp` (92G free): `git clone --no-hardlinks <lane> /tmp/scratch-r35/AttackQuotedHash/lane`
  → `CLONE_OK`, detached at `7da6e07`, all four pins match (§0 table). No `/fast` writes beyond the
  stale clone (untouched, 176M).
- **Restoration:** nothing outside `/tmp/scratch-r35/AttackQuotedHash/` and this report was written.
  The lane checkout is byte-clean after all runs (`git status --porcelain` → 0 lines; pins re-hashed
  identical). The pristine specimen is a byte copy of the pinned runner; the mutants are separate
  files. There is no mutated shared source to restore.
- No installs; no `pacman`; no mutating `git`/`jj` command; no subagent dispatch.
- Reproduce (absolute paths):

```bash
L=/tmp/scratch-r35/AttackQuotedHash
cd $L/lane
python3 tools/tally-audit-v3.py --runner $L/work/pristine-mutate-and-run.sh          # PASS, exit 0
python3 tools/tally-audit-v3.py --runner $L/work/mutants/A_ansiC.sh                 # PASS, exit 0  (hole)
python3 tools/tally-audit-v3.py --runner $L/work/mutants/B_nesteddquote.sh          # PASS, exit 0  (hole)
python3 tools/tally-audit-v3.py --runner $L/work/mutants/C_linecont.sh              # PASS, exit 0  (hole)
python3 tools/tally-audit-v3.py --runner $L/work/mutants/D_parambranch.sh           # SETUP, exit 2 (fail-closed)
python3 tools/tally-audit-v3.py --runner $L/work/mutants/H_plainmask.sh             # head FAIL, exit 1
python3 tools/tally-audit-v3.py --runner $L/work/mutants/K2_quoteleak.sh            # head FAIL, exit 1 (false kill)
cd $L/work
bash witness.sh $PWD/pristine-mutate-and-run.sh 0 0 1 0 0 0 0 0 0                  # RC=1 FAIL
bash witness.sh $PWD/mutants/A_ansiC.sh          0 0 1 0 0 0 0 0 0                 # RC=0 PASS
python3 blockcmp.py                                                                # block_same=True for every specimen
python3 headly.py                                                                  # shipped view PASS / identity view FAIL (A,B,C)
python3 ctr.py                                                                     # counter diverge() = [] for A,B,C,H
python3 ctrscore.py                                                                # accept K2: valid=True, pass=False
```

Scratch artefacts: `work/{pristine-mutate-and-run.sh, mutants/, witness.sh, probe_cv.py, probe_ws.py,
blockcmp.py, headly.py, ctr.py, ctrscore.py, audit-*.log, run-*.out, sib-*/, specimen-sha.txt}`.

---

## 9. Verbatim bash-semantics transcript (the five named constructs)

```
$ bash -c 'x=$'"'"'don\'"'"'t reorder # '"'"'; echo "[$x]"'        -> [don't reorder # ]
$ bash -c ': $'"'"'don\'"'"'t reorder # '"'"'; st=0; echo "st=$st"' -> st=0
$ bash -c 'st=1; : "note $(printf %s "n # 1")x"; st=0; echo "st=$st"' -> st=0
$ printf 'bash -c "printf %s foo\\\n#bar"\n' | bash               -> foo#bar
$ bash d.sh                                                       -> D st=0        (${X:-$'a\'b # '})
$ bash -c 'st=1; : '"'"'x # y'"'"'; st=0; echo "st=$st"'          -> st=0          (control: plain '…')
$ bash -c 'st=1; : "x" # st=0
           echo "st=$st"'                                         -> st=1          (control: real comment)
```

In every one of the first four, `#` is data to bash and the following `; st=0` executes; the fifth
and sixth are the two "no blanking / correct blanking" controls.
