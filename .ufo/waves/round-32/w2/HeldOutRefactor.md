# HeldOutRefactor — round 32, wave 2, held-out author for C1 counter v2

Seat: `HeldOutRefactor`. Assignment: write held-out copies for C1 counter v2 (accept + kill) that are
VALID under the counter's own rules and, if possible, that the frozen tool `tools/tally-audit.py`
(sha256 `9639c458…99ef`) gets WRONG.

## Verdict first

**The frozen tool is unsound on three of the six copies below.** Three of my copies are counter-valid and
the tool mis-handles them:

| copy | set | tool verdict | what the tool did wrong |
|---|---|---|---|
| `HeldOutRefactor-a3` | accept | exit 2 `TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)` | **cannot audit** a correct runner |
| `HeldOutRefactor-a4` | accept | exit 1 `TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)` | **false FAIL** on a correct runner |
| `HeldOutRefactor-k1` | kill | exit 0 `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | **false PASS** on a runner with a real tally defect |

Under the counter's predicate (`c1-measure-v2.py` docstring), a must-accept copy must yield exit 0 +
`TALLY_AUDIT: PASS` and a must-kill copy must yield exit 1 + `TALLY_AUDIT: FAIL`. All six of my copies
are counter-valid (verified below with the counter's own `v2.validate()`), so at any revision that
commits them the predicate `C1_R32V2_PASS` is false. That is the intended outcome of a falsifier seat:
the sealed held-out set exists to catch exactly this, and the tool at `9639c458…99ef` cannot pass it.

The other three copies (`a1`, `a2`, `k2`) are controls: the tool handles them correctly. `k2` is a
control kill copy that the tool *does* catch, so the false negative in `k1` is specific, not a
general "the tool never kills anything" artefact.

## Environment and provenance

* Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, revision `a4f718138bdad20de741faeca57891645e5a64d9`.
* My clone: `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutRefactor/c`, cloned with
  `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin …` then
  `git checkout -q --detach a4f718138bdad20de741faeca57891645e5a64d9` (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE
  unset). No `jj` command was run anywhere; no git write command was run in the lane or the fleet root.
* Base bytes for every copy: `git -C c show e24688b2ff6cca1c9ad20e112f02c629b8597ff8:tools/mutate-and-run.sh`
  written to `pinned.sh`; `sha256sum pinned.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
  = the counter's `PINNED_RUNNER_SHA`. The runner is byte-identical to the pinned base in every copy except
  the single region each `edits` list names.
* Frozen tool used for every run: `c/tools/tally-audit.py`, `sha256sum` =
  `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` = the counter's `TOOL_SHA256`.
* No tooling was installed or upgraded by this seat (no pacman/uv/npm/cargo action), so there is nothing
  to record on the operator tooling channel.

## Validity check (mandatory, per copy)

Run exactly as the assignment specifies — the counter's own `validate()`, never the counter's `main()`:

```
python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutRefactor/validate2.py
```

`validate2.py` imports `c1-measure-v2.py` from my clone, loads the pinned runner, and calls
`v2.validate(ho, pristine, PIN, tmp, witnesses)` for each held-out file. It runs every accept copy twice:
once with an empty witness list and once with a synthetic held-out *block* witness (a faulty tally block
the pinned harness rejects), because the real counter additionally compares each accept copy's harness
verdict against the pinned harness's verdict on every held-out block witness.

Observed output (all six valid, both witness modes):

```
HeldOutRefactor-a1       no-witness           VALID set=accept
HeldOutRefactor-a1       with-block-witness   VALID set=accept
HeldOutRefactor-a2       no-witness           VALID set=accept
HeldOutRefactor-a2       with-block-witness   VALID set=accept
HeldOutRefactor-a3       no-witness           VALID set=accept
HeldOutRefactor-a3       with-block-witness   VALID set=accept
HeldOutRefactor-a4       no-witness           VALID set=accept
HeldOutRefactor-a4       with-block-witness   VALID set=accept
HeldOutRefactor-k1       no-witness           VALID set=kill
HeldOutRefactor-k1       with-block-witness   VALID set=kill
HeldOutRefactor-k2       no-witness           VALID set=kill
HeldOutRefactor-k2       with-block-witness   VALID set=kill
```

`bash -n` accepts all six copies. The runner's own `--selftest` passes 106/106 on the pinned runner and on
every accept copy (`a1`–`a4`), which confirms the accept copies are behaviour-preserving for the runner
itself; `k2` fails its own selftest 103/106, as a real defect should. `k1` also passes the runner's own
selftest 106/106 — the defect is invisible to the runner's own harness too, which is precisely why it is
worth handing to the audit tool.

## Tool runs

Two independent runs per copy: directly, and under the counter's exact `bwrap` sandbox command
(`c1-measure-v2.py:run_sandboxed`, reproduced in `runsandbox.sh`). **Both runs agree on every copy**, so
the results below are what the counter will observe.

Command form (direct):

```
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutRefactor/c/tools/tally-audit.py \
  --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutRefactor/copies/<k>.sh
```

| id | set | validity | tool exit | TALLY_AUDIT line | defeats the tool? |
|---|---|---|---|---|---|
| `HeldOutRefactor-a1` | accept | valid (accept) | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | no — tool correct |
| `HeldOutRefactor-a2` | accept | valid (accept) | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | no — tool correct |
| `HeldOutRefactor-a3` | accept | valid (accept) | 2 | `TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)` | **yes — cannot audit** |
| `HeldOutRefactor-a4` | accept | valid (accept) | 1 | `TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)` | **yes — false FAIL** |
| `HeldOutRefactor-k1` | kill | valid (kill) | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | **yes — false PASS** |
| `HeldOutRefactor-k2` | kill | valid (kill) | 1 | `TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)` | no — tool correct (control) |

Full sandbox transcript (exit codes as the counter records them):

```
[pristine] exit=0
[HeldOutRefactor-a1] exit=0
[HeldOutRefactor-a2] exit=0
[HeldOutRefactor-a3] exit=2
[HeldOutRefactor-a4] exit=1
[HeldOutRefactor-k1] exit=0
[HeldOutRefactor-k2] exit=1
```

The failing detail lines, verbatim from the tool:

```
[HeldOutRefactor-a3] TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)
[HeldOutRefactor-a4] CHECK runtime FAIL vectors=349 mismatched=18; first: stress dup operand 0:
  got (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)'),
  want (2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=10)')
[HeldOutRefactor-k1] CHECK runtime PASS vectors=349 mismatched=0
[HeldOutRefactor-k2] CHECK runtime FAIL vectors=349 mismatched=17; first: statuses 1 0 0 0 0 0 0 0 0:
  got (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=2 setup=0)'),
  want (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')
```

Note the tool's own `--selftest` passes 11/11 (`TALLY_AUDIT_SELFTEST: 11/11 pass`) and the tool PASSes the
pristine runner, so the three failures above are properties of the copies, not a broken tool binary.

## The three defects in the tool, with mechanism

### 1. `k1` — false PASS: the runtime sweep never drives exit status 5 into a non-first leg

`k1` makes a leg whose status is 5 count as a *failure* (`nfail`) rather than *cannot-verify* (`nsetup`)
for every leg after the first. On the witness vector `[0,0,0,5,0,0,0,0,0]` the copy prints
`REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` where the pinned runner prints
`REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)` — a real defect in the tally, and the counter
accepts the vector witness (the two blocks print different first lines and exits).

The tool misses it because of how it builds its status sweep (`tools/tally-audit.py:check_runtime`):

```
vectors = [[0] * n]
for s in range(1, 256):
    vectors.append([s] + [0] * (n - 1))     # status s in the FIRST leg only
for pos in range(n):
    for s in (1, 2, 3, 4, 126, 127, 255):   # per-position statuses: 5 is NOT in this list
```

So the exhaustive 1..255 sweep only ever puts the varying status in leg 0, and the per-position sweep
only covers statuses {1,2,3,4,126,127,255}. Status 5 in leg 1..8 is never driven. `k1`'s gate is
`ti > 1`, so it is invisible precisely in the region the sweep misses. The tool's runtime check reported
`vectors=349 mismatched=0` — it never saw the defect.

### 2. `a4` — false FAIL: the stress test rewrites the wrong loop

`a4` adds one output-neutral first pass over the same leg statuses (`for leg in "$st_js" …; do
legs_counted=$((legs_counted + 1)); done`) before the unchanged tally loop. The runner's behaviour is
identical (its own selftest passes 106/106) and the counter's accept rules accept it, but the tool's
`tally_loop` (`tools/tally-audit.py`) returns the **first** `for … in …` loop whose operands are all leg
statuses — which is now the auxiliary pass, not the tally loop. The tool's stress phase then duplicates
or drops an operand of the auxiliary loop and expects the *tally* to notice, so it reports 18 mismatches
(the 9 dup + 9 drop stress cases), all of which mutate the wrong loop. The static check passed
(`legs=9 operands=9 nlegs=9`) precisely because the auxiliary loop happens to list the same nine
operands, so the tool's operand accounting is right while its stress target is wrong. This is a false
FAIL on a runner whose tally is provably unchanged.

### 3. `a3` — cannot audit: the harness-extraction anchor is stricter than the runner needs

`a3` adds a second, deeper-indented extraction of the same tally block in the selftest harness
(`    tblock=$(awk '…' "$SELF")` next to the existing `  tblock=$(awk '…' "$SELF")`). Both assign the same
value, so behaviour is unchanged (selftest 106/106) and the counter's accept rules accept it.

The tool refuses to audit it. Its `harness_section` insists the extraction line appear **exactly once**:

```
EXTRACT_RE = re.compile(r'^[ \t]*tblock=\$\(awk .*"\$SELF"\)[ \t]*\n', re.M)
...
if len(EXTRACT_RE.findall(sec)) != 1:
    raise CannotAudit('harness block extraction line not found exactly once')
```

`EXTRACT_RE` accepts any leading whitespace, so the four-space copy matches too and the count is 2 → the
tool exits 2 with `TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)`. The
counter's own anchor is stricter about indentation but laxer about count
(`EXTRACT = re.compile(r'^  tblock=\$\(awk .*"\$SELF"\)\n', re.M)`, `if len(EXTRACT.findall(sec)) != 1`)
and accepts the copy. The tool's `EXTRACT_RE` also requires `[ \t]*` before the newline, so a
trailing-whitespace variant of the *original* line would likewise trip it.

## Why these shapes were chosen (not v1 families)

The v1 families are the frozen kill set `T08 N05 H03 H04 H05 N01 N02 N03 D01` plus their generated
variants, and the frozen accept set `B0-B5` + `gB6 gB7` (pristine, T07 guard, reversed operands, decoy
comments, cosmetic edit, harness variable renamed, permuted operands, nonce comments). None of my six
copies is one of those:

* `a1` — the per-status classification moves into a **helper function** called once per leg (v1's accept
  set has no helper-function extraction; `B5` renames a harness *variable*, not a call structure).
* `a2` — the workdir local is **renamed and re-bound** (`local rtdir=$root`), the case subject is
  **quoted**, and the three guards become **arithmetic tests** `(( nfail > 0 ))` instead of `[[ ]]`.
* `a3` — a **second harness extraction** at a different indentation.
* `a4` — an **auxiliary loop over the leg statuses** before the tally loop.
* `k1` — **position-gated** status-5 misclassification (v1's `T08` family is a flat `4) npass` arm; mine
  is gated on the loop counter, which is why the tool's per-position sweep misses it).
* `k2` — an **off-by-one in the reported failed count** (`$((nfail + 1))` in the FAIL line), a shape absent
  from v1 (whose kill set is arm/guard/harness/loop/position families).

## Held-out files

Files are at `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutRefactor/heldout/HeldOutRefactor-<k>.json`.
Each `old` anchor occurs exactly once in the pinned runner at its turn (the counter's `apply_edits`
enforces this and accepted all six). The `witness` key is present only on the kill copies. The blocks
below are pasted verbatim from the validated files.

HELDOUT-FILE HeldOutRefactor-a1

```json
{
  "id": "HeldOutRefactor-a1",
  "author": "HeldOutRefactor",
  "set": "accept",
  "edits": [
    {
      "old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n",
      "new": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  tally_classify() {\n    case $1 in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  }\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    tally_classify \"$st\"\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n"
    }
  ],
  "rationale": "Semantics-preserving refactor: the per-status classification moves into a local helper called once per leg, so the counts, the REGRESSION lines and the exit status are byte-identical to the pinned runner."
}
```

HELDOUT-FILE HeldOutRefactor-a2

```json
{
  "id": "HeldOutRefactor-a2",
  "author": "HeldOutRefactor",
  "set": "accept",
  "edits": [
    {
      "old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n",
      "new": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  local rtdir=$root\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case \"$st\" in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if (( nfail > 0 )); then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$rtdir\"\n    exit 1\n  fi\n  if (( nsetup > 0 )); then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$rtdir\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$rtdir\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if (( auto == 1 && KEEP == 0 )); then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$rtdir\"\n    rm -rf \"$rtdir\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$rtdir\"\n  fi\n  exit 0\n"
    }
  ],
  "rationale": "Semantics-preserving refactor: the workdir local is renamed and re-bound from the original, the case subject is quoted and the three guards become arithmetic tests on the same integers, so every REGRESSION line and exit status is unchanged."
}
```

HELDOUT-FILE HeldOutRefactor-a3

```json
{
  "id": "HeldOutRefactor-a3",
  "author": "HeldOutRefactor",
  "set": "accept",
  "edits": [
    {
      "old": "  local tblock tgot tvec ti tj\n",
      "new": "  local tblock tgot tvec ti tj\n    tblock=$(awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f' \"$SELF\")\n"
    }
  ],
  "rationale": "Semantics-preserving refactor: the selftest harness extracts the tally block a second time with the same awk program, so the harness verdicts and the runner output are unchanged."
}
```

HELDOUT-FILE HeldOutRefactor-a4

```json
{
  "id": "HeldOutRefactor-a4",
  "author": "HeldOutRefactor",
  "set": "accept",
  "edits": [
    {
      "old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n",
      "new": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  # r32: count the leg statuses once before tallying them.\n  local legs_counted=0\n  for leg in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    legs_counted=$((legs_counted + 1))\n  done\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n"
    }
  ],
  "rationale": "Semantics-preserving refactor: a first pass counts the leg statuses into a separate local before the unchanged tally loop, so the counts, the REGRESSION lines and the exit status are identical to the pinned runner."
}
```

HELDOUT-FILE HeldOutRefactor-k1

```json
{
  "id": "HeldOutRefactor-k1",
  "author": "HeldOutRefactor",
  "set": "kill",
  "edits": [
    {
      "old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n",
      "new": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  local ti=0\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    ti=$((ti + 1))\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      5) if (( ti > 1 )); then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n"
    }
  ],
  "rationale": "Real tally defect: a leg whose exit status is 5 is counted as a failure (nfail) instead of cannot-verify (nsetup) for every leg after the first, so the runner prints REGRESSION: FAIL where the pinned runner prints REGRESSION: SETUP.",
  "witness": {
    "vector": [
      0,
      0,
      0,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  }
}
```

HELDOUT-FILE HeldOutRefactor-k2

```json
{
  "id": "HeldOutRefactor-k2",
  "author": "HeldOutRefactor",
  "set": "kill",
  "edits": [
    {
      "old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n",
      "new": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$((nfail + 1))\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n"
    }
  ],
  "rationale": "Real tally defect: the REGRESSION: FAIL line reports one more failed leg than was counted, so the reported failed= field disagrees with the tally and with the exit status.",
  "witness": {
    "vector": [
      1,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ]
  }
}
```

### sha256 of the held-out JSON files

```
f5e2c2a4293cc000c9304f5624200ec6248199b4468382dabb08259c46cbafc3  HeldOutRefactor-a1.json
f5156ebd6abea83c8f418a76ea0f65afbad24c7ec51cf7aa629edb847b044180  HeldOutRefactor-a2.json
ce0e14e97da6f20426996dcf570a55ea6a8dbc349332bfc27087959916dffdce  HeldOutRefactor-a3.json
32d05283bd50bcc62773fc6b275f05c4038aa3de00fb460283430bfa946c4ba4  HeldOutRefactor-a4.json
b390f0e47a019fff13cc5049451456ff4bf7a60a5f8dbc0bb69203d8413ddc03  HeldOutRefactor-k1.json
6f4a96799700ec6927f74b0f14e1651c3bc21355740d0a3bb0401eaa2facf7ab  HeldOutRefactor-k2.json
```

### sha256 of the generated runner copies

```
d26e730d9e0d51e8bc2fd4296009ef5249500743905811ffdd8a4ee1d849f5ac  HeldOutRefactor-a1.sh
b79df45a003bf9212db827c60d61f6c163345da36121c0d439ee892b3d476458  HeldOutRefactor-a2.sh
2dd918c8ede34e467a1e1ad356e95c026ff4c135155c18958a6ea65e705d26ae  HeldOutRefactor-a3.sh
f3888bd134c3d44e4c822505761001bc68d88a23daf1f609ee5bce0719b9d102  HeldOutRefactor-a4.sh
d55d0c5e772fc43f120f036a266a75c94837a27eff120283e069869f949bb5b1  HeldOutRefactor-k1.sh
e5dbf0104c20186cb072bb9efa4123329b5a38780549e3cefb378ea6cbf67b3e  HeldOutRefactor-k2.sh
```

## Smallest safe correction (for the tool author, not applied by me)

I did not edit the tool or the runner. If the tool is to be re-frozen, the three minimal changes are:

1. `check_runtime`: drive the full 1..255 status set at **every** leg position, not only at leg 0 — e.g.
   replace the `{1,2,3,4,126,127,255}` per-position list with `range(1, 256)`. That closes the `k1`
   false negative (the tool's own fault panel already contains a `status-3-passes` fault, so status-5
   coverage is the same class of gap).
2. `tally_loop` / `with_operands`: pick the loop the tally actually uses rather than the first leg-status
   loop — e.g. select the loop whose body contains the `case $st in` classification, or the **last**
   leg-status loop in the block — and rewrite the operand list of that same loop in the stress phase.
   That closes the `a4` false positive.
3. `harness_section`: tolerate more than one `tblock=$(awk …)` extraction (or anchor on the last one, or
   require at most one rather than exactly one), so a redundant extraction does not make the tool
   refuse to audit. That closes the `a3` "cannot audit" case.

With those three changes the tool would reach: `a1` PASS, `a2` PASS, `a3` PASS, `a4` PASS, `k1` FAIL,
`k2` FAIL — i.e. it would satisfy the C1 predicate on this held-out set.

## Risks and blockers

* **No blocker.** Every copy is written, counter-valid, and its tool behaviour is measured twice (direct
  and sandboxed) with identical results.
* **Residual risk on the held-out set as a whole:** the L1 commits every file returned, unedited. My three
  defeating copies make `C1_R32V2_PASS` false at any revision that contains them. That is the point of a
  sealed held-out set, but it means the wave cannot be closed by re-freezing the current tool — the tool
  needs the three corrections above (or the counter's rules need to be tightened to exclude these
  shapes, which I do not recommend: the shapes are legitimate semantics-preserving refactors and a real
  tally defect).
* **Tool-freeze coupling:** the counter's `TOOL_SHA256` is `9639c458…99ef`, the sha256 of the tool in the
  clone at `a4f7181`. If the tool is re-frozen after this wave, the held-out files stay valid (they are
  built from the pinned *runner* bytes, which do not change), but the tool sha256 recorded in the counter
  must be updated to match.
* **Not verified here:** the counter's *aggregate* run (`main()`) was never executed by this seat, by
  instruction. My claim is about the per-copy tool outcomes and the counter's per-copy `validate()`
  verdicts, both measured directly; the aggregate `C1_R32V2_PASS` line is inferred from the counter's
  documented outcome mapping (accept ⇒ exit 0 + `TALLY_AUDIT: PASS`; kill ⇒ exit 1 + `TALLY_AUDIT: FAIL`).
* **Scope discipline:** I ran no gate, selftest or sweep inside the lane itself; every runner execution
  happened in my own scratch clone, and the tool was run on my own copies only. No process trees are left
  running (all commands completed and returned).
