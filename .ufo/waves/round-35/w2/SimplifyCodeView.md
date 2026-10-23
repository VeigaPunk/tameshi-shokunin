# Round-35 w2 — SimplifyCodeView

Seat: `L1tameshi35.SimplifyCodeView` (leaf simplifier, godspeed). Lane pin at dispatch:
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Lane cloned read-only to
`/fast/scratch/hyaku/tameshi-r35-seats/SimplifyCodeView/lane`; all work in `…/work/`.
Frozen pins re-verified in the clone (`sha256sum`): tool `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`,
predecessor `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`,
runner `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`,
c1 counter `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`,
c2 counter `67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc` — all match contract.json.
`git status --porcelain` in the clone: empty; `/home/vgpnk/Projects/shokunin/tameshi-shokunin` never written except this report.
No installs (nothing needed; pacman untouched).

## Assignment and result

> Propose the minimal `code_view` that preserves every verdict: enumerate its states/branches,
> delete any unreachable one, prove equivalence by re-running the public panel + the v3 selftest
> with the simplified function in a COPY of the tool. Report byte delta and verdict tally.

**Result: a reduced `code_view`, −207 B (43,730 → 43,523), sha `ef98fc53…65885` →
`55d37285f2d0ad722a8625881fed0cd934ab88e46050d599179bce5979c28576`, with ZERO states or
branches deleted — every state and every branch of the machine is reachable and load-bearing;
the removable weight was per-branch duplication, not dead branches.** Verdict tally identical
before/after at all three measured levels (function differential, 8-copy public panel,
30-case selftest).

## State/branch enumeration (`tools/tally-audit-v3.py:150-194`)

`quote` ∈ {`None`, `'`, `"`} — 3 states, all reachable:

| branch | reachable witness | removable? |
|---|---|---|
| `quote == "'"` loop + `c == "'"` exit | `'x#y'` | no — `'`-strings exist; `#` inside must stay literal |
| `quote == '"'` + inner `\` skip (`"a\"b"`) | `"a\"b" #c` | no — removes `#`-after-escaped-quote from comment set |
| `quote == '"'` + `c == '"'` exit | `"x" #c` | no |
| unquoted `\` skip | `\#x`, `x\`+`\n`+`#y` | no — `\#` is literal `#` in bash |
| `c in ("'", '"')` → enter quote | `'`, `"` | no |
| `#` comment start, `i == 0` arm | any file starting `#!`/`#` (the runner itself, `mutate-and-run.sh:1` = `#!`) | no — needed semantically *and* guards `text[-1]` wraparound |
| `#` comment start, `text[i-1]` arm | `x # y` | no |
| `if j < 0: j = n` (comment runs to EOF) | `x # tail` with no trailing newline | no — else `find` returns −1 → `out[i:-1]` would blank wrongly / `i = -1` loops |
| `i + 1 < n` guards on both `\` branches | text ending in `\` | semantically inert (`i += 2` past end terminates identically) but cheap clarity; kept |
| `for k in range(i, j)` blank loop | any comment | reformulated as slice-assign (see below) |

Deleting any of the nine reachable arms changes output on a reachable input; that is the
"no unreachable state/branch" finding, and each witness is in the differential corpus below.

### The simplification (applied to `…/work/simpl/tally-audit-v3.py` only)

1. The two quote-state branches (`'` and `"`) merge into one `if quote:` block; the only
   state-dependent difference — `\` skips inside `"` — becomes `if c == '\\' and quote == '"'`.
2. `out[k] = ' '` loop → slice assign `out[i:j] = ' ' * (j - i)`.
3. `c == "'" or c == '"'` → `c in '\'"'`; init folded to `i, n, quote = 0, len(text), None`.
4. Docstring kept verbatim (routed provenance — round-34/35 rationale; not touched).

```python
def code_view(text):
    """<docstring unchanged>"""
    out = list(text)
    i, n, quote = 0, len(text), None
    while i < n:
        c = text[i]
        if quote:
            if c == '\\' and quote == '"' and i + 1 < n:
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
        elif c == '\\' and i + 1 < n:
            i += 2
        elif c in '\'"':
            quote = c
            i += 1
        elif c == '#' and (i == 0 or text[i - 1] in ' \t\n;|&('):
            j = text.find('\n', i)
            if j < 0:
                j = n
            out[i:j] = ' ' * (j - i)
            i = j
        else:
            i += 1
    return ''.join(out)
```

## Equivalence proof — three levels

### L1. Function-level differential (exit 0, 0 diffs)

`python3 /fast/scratch/hyaku/tameshi-r35-seats/SimplifyCodeView/work/diff.py`, exit `0`:
`orig` vs `simpl` `code_view` compared on **43 directed** edge strings, **16,105 exhaustive**
strings over the alphabet `#\'" \n;|&()` (length ≤ 4), **300,000** seeded random strings over a
wider alphabet, and the **full bytes** of `mutate-and-run.sh` (169 KB) and `tally-audit-v3.py`:
`DIFFS: 0`. Also asserts output length == input length on every string.

### L2. Public panel — frozen counter in CONTROL mode (the deciding harness's own scorer)

```
python3 .ufo/evidence/round-35/c1/c1-measure.py --lane . --rev 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b \
  --work …/work/panel-{orig,simpl} --tool <abs path to tool>        (cwd = lane clone)
```

| tool | COPY rows (all 8) | tally | exit |
|---|---|---|---|
| orig `ef98fc53…` | kill cfg00-accept-swap div=(0,0) rc=1 runtime ✔; kill cfg11-pass-mask div=(1,1) rc=1 runtime ✔; kill root-keyed-auto-mask div=(1,0),(1,1) rc=1 runtime ✔; kill root-keyed-auto-zero div=(1,0),(1,1) rc=1 runtime ✔; kill workdir-branch-swap div=(1,0),(0,0) rc=1 runtime ✔; accept comment-brace/-esac/-names-leg div=- rc=0 ✔ | `pub_kill=5/5 pub_accept=3/3 pub_distinct=8` | 1 (`CONTROL_PASS=false` — ho_*=0 by construction without `--sealed`, expected) |
| simpl `55d37285…` | **byte-identical eight rows** | `pub_kill=5/5 pub_accept=3/3 pub_distinct=8` | 1 |

The counter's reported `tool_sha=55d37285f2d0ad72` equals my `sha256sum` of the copy — the
panel scored exactly the simplified bytes. (Verdict rows are identical up to the tool-sha field.)

### L3. `--selftest` — 30/30 on both, identical case lines

```
cd …/lane/tools            && python3 tally-audit-v3.py --selftest    → TALLY_AUDIT_V3_SELFTEST: 30/30 pass
cd …/work/simpl            && python3 tally-audit-v3.py --selftest    → TALLY_AUDIT_V3_SELFTEST: 30/30 pass
```
All 30 `CASE <name> PASS (exit N)` lines identical between the two runs (incl. the three
comment-accept cases and the real-root kill). `…/work/simpl/mutate-and-run.sh` is a byte copy
of the pinned runner (selftest reads `mutate-and-run.sh` beside the tool).

## Findings (ranked) — code_view's real edges, all fail-closed

Each witness is a copy of the pinned runner plus one insertion, scored by BOTH tools and by
the frozen counter's own `behavior()` oracle (ground truth, `work/witness.py`; copy bytes under
`work/wit/<name>/copy.sh`). All six give **identical orig/simpl output**, so none of these
bound the simplification — they bound the (shared, frozen) apparatus.

- **BOUND-1 — comment-start delimiter set is narrower than bash's.** Bash starts a comment
  after any operator, including `)`, `>`, `<` (verified: `( true )# x` runs clean; `echo hi >#f`
  errors `syntax error near unexpected token 'newline'` because `#f` was comment-eaten).
  `code_view`'s set is `' \t\n;|&('`. An inert `)`-adjacent comment is kept as CODE in the view.
  Witness `w-paren-comment` — head insertion `  ( : )# inert comment … stray }`: kept `}`
  truncates `regression_body` → **both tools rc=2 `SETUP (tally start … not found)`**, and the
  counter oracle itself exits `SETUP: tally start not found` — the copy is *unmeasurable* by
  the deciding counter, not just refused by the tool.
- **BOUND-2 — quoted text is kept (by design) and pollutes structural scans.** `}`/`esac`/`st_*`
  inside quotes are data to bash, code to the view (required — operand extraction needs
  `"$st_x"`). Witness `w-quoted-brace` (`echo "}" >/dev/null` in the head): rc=2 on both tools,
  oracle SETUP — an inert string false-refuses a pristine copy.
- **BOUND-3 — heredocs unmodeled.** Body is data to bash (`P4-ok` in probe), code to the view.
  Witness `w-heredoc-brace` (`cat <<'EOFHD' \n } \n EOFHD` in head): rc=2 both, oracle SETUP.
- **BOUND-4 — `\<newline>` inside a comment extends the comment in bash, not in the view.**
  Probe: `# cmt \`+`\n`+`x=HIDDEN` — bash EXECUTES `x=HIDDEN` (P7 printed `x=HIDDEN`). Witness
  `w-cmt-cont`: a comment line ending in `\` makes bash swallow the next line (`st_js=0`,
  div=`none` — behaviorally pristine) while the view keeps it → **head FAIL, rc=1, both tools**
  (`leg st_js appears 3 times … want exactly 2`). False-refusal of an accept-behavior copy.
- **BOUND-5 — `\<newline>` before `#` glues `#` into a word in bash; view blanked it.**
  Probe: `echo a\`+`\n`+`#b` → bash prints `a#b`. Witness `w-glue-divergent` (`st_js=$?\`+`\n`+`#x`):
  bash binds `st_js=$?#x` (word-internal `#` — NOT a comment), so leg capture is broken in
  reality: counter `div=(1,0),(1,1),(0,1),(0,0)` — divergent on ALL FOUR configs. The tool
  kills it, but `failed=['head','static','runtime','harness']` ≠ the required exactly-
  `['runtime']`, so the C1 counter scores it `pass=False` — a *real* divergence demoted to a
  dirty/miscounted kill. Fail-closed; never accepted.
- **HYGIENE-1 — two hand-synced `code_view` copies exist** (tool 150-194 vs frozen counter
  `c1-measure.py:95-129`; the counter's is already tighter — `j = n if j < 0 else j`,
  `c in ("'", '"')`). The duplication is *deliberate*: the oracle must not import the object
  under test (`c1-measure.py:50-51`). Not deletable; my simplified body could replace the
  counter's identically-semantics copy at the next unfrozen revision.
- **Control `w-plain-comment`** (`# plain comment mentioning st_js and a stray }`): div=`none`,
  rc=0 PASS on both tools — the blanking mechanism itself is sound for the plain case.
- **No CRITICAL.** Every lexical divergence found between the view and bash only *keeps* code
  bash discards (fail-closed pollution) or *blanks* a comment-tail bash would glue — and the
  glue form leaves its `\` visible to the line-anchored scans, so it cannot hide a defect from
  the checks. No false-accept path via `code_view` was constructible; all six witness classes
  degrade to rc∈{1,2} or a misattributed kill.

## What I could NOT break (with proof)

- **No unreachable/deletable state or branch exists**: every arm has a witness input where its
  removal changes `code_view`'s output (table above); L1 differential 0 diffs over 316K+ inputs.
- **Verdict equivalence held at every level measured**: panel `5/5 + 3/3, distinct=8`, per-copy
  `div=`/`rc=`/`failed=` rows identical; selftest `30/30` ×2 identical; six edge witnesses
  identical orig-vs-simpl on both tool verdict AND counter oracle.
- **Byte delta**: file 43,730 B → 43,523 B (**−207 B**); function 150–194 (45 lines incl.
  docstring) → 150–186 (37 lines). Sha256 before `ef98fc53…` (frozen pin), after
  `55d37285f2d0ad722a8625881fed0cd934ab88e46050d599179bce5979c28576`.
- Lane clone untouched (`git status --porcelain` empty; tool still `ef98fc53…`); nothing
  written outside `…/work/` and this report.
