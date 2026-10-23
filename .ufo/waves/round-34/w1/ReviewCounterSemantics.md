# ReviewCounterSemantics — semantic review of amendment-6 `ho_witness_ok` (round-33 C1 counter)

Seat: tameshi-r34-w1 / ReviewCounterSemantics · 2026-10-23 · Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ReviewCounterSemantics/`
Claim under attack: C1 (operability, `tools/tally-audit-v2.py`) MEASURED TRUE at `c17e593b51802dd4ed568da3265f21c6d00c4273`; deciding-run receipt on disk at `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` (exit `c1-deciding-run.exit` = `0`). Verdicts below are observations against the *routed gate rule*, not against the landed measurement: the deciding run stands.

## Byte provenance and verification commands

All verification against lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (read-only clone):

```
git clone -q --no-hardlinks <fleet>/tameshi-shokunin $SCRATCH/lane           # exit 0 (setup.exit)
git -C $SCRATCH/lane checkout -q --detach 0b99d48ed…97a7f68b7               # exit 0
git -C lane show 0b99d48…:tools/tally-audit-v2.py > tool.py                 # sha256 7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  ✓ pin
git -C lane show 0b99d48…:tools/mutate-and-run.sh  > pristine.sh            # sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  ✓ pin
git -C lane show 6aaad5b389e7eed426ec3b452617bcbf9bf7f35a:.ufo/evidence/round-33/c1/c1-measure.py > counter-amended.py
sha256sum counter-amended.py                                               # f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c ✓ = live frozen file (amendment-6 bytes)
```

Counter functions exercised by **module import only** (`validate_ho`, `apply_edits`, `tally_block_of`, `ho_witness_ok`, `block_run`, `run_tool_sandboxed`); no default-mode run anywhere. Every verdict run is `python3 verdict.py <COPY>` (or `verdict2.py`, direct `tool.py`), artifacts in `$SCRATCH/exp/out-*.json` + `exp/rc-*`. Exit codes: `rc-PROBE=A=B=C=D=F=G=B2=0`, `rc-Cdirect=1` (expected FAIL), first attempt rc=1s were my own non-unique `old` anchor (`#!/usr/bin/env bash\n` occurs 7× via selftest fixtures), relaunched clean.

## Line-by-line: implemented rule vs routed rule

`ho_witness_ok` at `c1-measure.py:184-218` (the pin's true numbers; assignment's "176-210" is off by a few):

| routed rule (lessons round-33.md:121-124; RevengerWitness.md patch; amendment docstring :27-34; `contract-amendments.json` `"amendment": 6` :36-38) | implementation | faithful? |
|---|---|---|
| kill+head = leg-assignment-line diff **+ identical block** | :191-207 — head differs, `mb != pb → head-with-block-edit`, else A/X multiset diff on `head_of` → `head-leg-assignment` | yes, verbatim from the routed patch (A/X regexes `st_[A-Za-z0-9_]+` over `head_of`, `:196-207`) |
| accept+head = identical block | :191-197,211 — head differs + `mb == pb` → `(True,'head')` | yes |
| accept+vector = a==b + bytes changed | :213-215 — `a == b and mutated != pristine` → `vector-equivalence` | yes |
| kill+vector = a!=b + len 9 | `pb == mb → block-identical`, else `a != b` → `vector` (:216-218); len-9 in `validate_ho` :122-124 for **all** vector witnesses (broader than "kill+vector"; consistent with routed intent) | yes |

The implementation is the routed RevengerWitness patch verbatim (modulo hoisting `mb` to the top). **The holes below are in the routed rule itself** — all four demonstrate that a sealed copy validates under its declared set while the pinned tool's correct verdict contradicts that set, i.e. `ho_invalid == 0` with a `ho_*` miss → `C1_R33_PASS=false` with a blameless tool. Same voidability class as Q3/Q3b; amendment 6 closed it only on the `kind=head` leg-surface.

### Checked surface anatomy (why the gate's spans ≠ the tool's audit spans)

Runner `pristine.sh` (2080 lines): `run_regression() {` at :1345; START (`  local nlegs=9 npass=0 nfail=0 nsetup=0 st`) at :1432; function-closing `}` at :1471; `selftest()` at :1475; harness anchors `local tblock tgot tvec ti tj` :1992, `tblock_full` :2035, `tblock=$tblock_full` :2040; file end :2080.

- counter `head_of` = **lines 1-1431** (whole file before START — shebang, file vars, usage/git_clean/etc., run_regression's preamble incl. the 9 `st_*=$?` at :1390-1430).
- counter `tally_block_of` = **lines 1432-1471** (START .. first `\n}\n`).
- **counter tail = lines 1472-2080 — inspected by NEITHER helper.** Includes all of `selftest()`, main dispatch, and the `st_rg=$?` lines at :1631-1928.
- tool audit body = `run_regression` body only (`regression_body`, brace-matched: :1345-1471). Tool `head_section` = **1345-1431** — the counter's head is a strict superset (1-1344 is invisible to the tool's head/static checks).
- tool `tally_block` = START .. `rfind('}')` in body (same 1432-1471 region on pristine).
- tool `check_harness` = the tool's only whole-file probe: `harness_section(text)` searches the full text for `local tblock` … `tblock=$tblock_full`, then `run_harness` splices `tblock=$AUDIT_INJECT` **after the last** `tblock=$(awk …)` line and runs the runner's own harness on the reference + 34 faults.

---

## Findings (severity order; every hole carries a riding copy JSON + observed verdicts)

### F1 — accept+vector "equivalence" is sampled on ONE author-chosen vector; any lethal block diff ties it  `[HIGH]`

`:213-215` runs exactly one witness vector through the counter's `block_run`. The tool sweeps 15 158 vectors/stress runs (`CHECK runtime vectors=15158`, `out-Cdirect.txt`). A copy whose block is lethal but ties on the author's vector validates as must-accept; the tool correctly fails it.

COPY-C (`exp/out-C.json`, rc=0):
```json
{"id":"RVW-C","author":"ReviewCounterSemantics-r34","set":"accept",
 "witness":{"vector":[0,0,0,0,0,0,0,0,0]},
 "edits":[{"old":"      1) nfail=$((nfail + 1)) ;;\n",
           "new":"      1) nfail=$((nfail + 1)) ;;\n      2) npass=$((npass + 1)) ;;\n"}]}
```
- `validate_ho` valid; `ho_witness_ok` → `(True, 'vector-equivalence')` (both sides `(0,'REGRESSION: PASS (…passed=9…)')` on [0]*9).
- `run_tool_sandboxed` on the copy: `ACCEPT→KILL`, rc=1, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)`.
- Direct `python3 tool.py --runner tool-C/copy.sh` (`out-Cdirect.txt`, rc=1): `CHECK runtime FAIL … mismatched=1800; first: cfg(0,1) statuses 2 0 0 0 0 0 0 0 0: got (0,'…PASS (cases=9 passed=9…)'), want (2,'…SETUP (cases=9 passed=8 cannot-verify=1)')` — the gate's tie on [0]*9 hides 1800 divergent vectors.
- **Impact:** a sealed must-accept authored this way rides the gate (`ho_invalid=0`) and then misses (`ho_a < ho_at`) — claim voided by sealed-copy construction with a blameless tool. This is Q3b's ride-along, reopened through the vector branch: "behavioral equivalence" on one vector is not equivalence.

### F2 — accept+head admits the tool's own head-kill surface (no leg-surface exclusion)  `[HIGH]`

The routed patch gives kill+head an A/X scan but gives accept+head **nothing** — any head diff validates (:211 `return True,'head'`). `check_head`'s kill surface (nonbare assignment, count≠1, twice-only — tool.py `check_head`, and its own selftest fault `head_overwrite` at tool.py:620 which expects this exact edit to FAIL `head`) lives entirely inside the tool's head span. Relabel any canonical head-kill as `accept`:

COPY-G (`exp/out-G.json`, rc=0):
```json
{"id":"RVW-G","author":"ReviewCounterSemantics-r34","set":"accept",
 "witness":{"kind":"head"},
 "edits":[{"old":"  st_claims=$?\n","new":"  st_claims=$?\n  st_claims=0\n"}]}
```
- gate → `(True,'head')` (head differs, block identical — the gate never checks what the head diff *is*).
- tool → `KILL` rc=1 `TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)` — v2's own `head overwrite` class.
- **Impact:** same void direction as F1, zero bash needed.

### F3 — kill+head "leg-assignment" surface is scanned over the whole-file prefix, not the audited head  `[HIGH]`

`head_of` returns text[:START] = lines 1-1431; v2's `check_head` scans only the body preamble 1345-1431. Any `st_*` assignment-line diff inside lines 1-1344 (file-level code, `usage()`, `git_clean()`, `regression_specs()`, …) satisfies the gate while every tool check is blind to it.

COPY-A (`exp/out-A.json`, rc=0):
```json
{"id":"RVW-A","author":"ReviewCounterSemantics-r34","set":"kill",
 "witness":{"kind":"head"},
 "edits":[{"old":"VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'\n",
           "new":"VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'\nst_decoy=$?\n"}]}
```
- gate → `(True,'head-leg-assignment')` (A/X multisets gain `st_decoy` — the regexes accept **any** `st_[A-Za-z0-9_]+` name, not only the 9 legs).
- tool → `ACCEPT` rc=0 `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` — the line is outside `regression_body`; the audit never executes the copy whole, so the file-level line is not even run.
- **Impact:** a validated must-kill the correct tool passes → `ho_k < ho_kt` → claim voided. Sub-question from the assignment: a *comment* line cannot match A/X (`^[ \t]*st_` is line-anchored) — but *data* lines can: `st_x=$?` inside a heredoc/quoted string in the head region matches identically (both gate and tool regexes are text-level; the hole is the span, which COPY-A demonstrates on the simplest site).

### F4 — the counter's tail (after first `\n}\n`) is a permanent blind spot; rides both head branches and vector  `[MED-HIGH]`

`tally_block_of` cuts at the first `\n}\n` (:140-145); `head_of` stops at START (:147-151). Lines 1472-2080 — including the tool's only whole-file audit surface (`local tblock` :1992 → `tblock=$tblock_full` :2040) — are uninspected. The routed patch's declared residual (RevengerWitness tail note) covered `--regression`-visible *head* behavior only; the tail is worse.

COPY-B2 (`exp/out-B2.json`, rc=0):
```json
{"id":"RVW-B2","author":"ReviewCounterSemantics-r34","set":"accept",
 "witness":{"kind":"head"},
 "edits":[{"old":"#!/usr/bin/env bash\n# mutate-and-run.sh — generic mutation runner (tameshi-shokunin, r10-2, TAMESHI-T10-2).\n",
           "new":"#!/usr/bin/env bash\n# mutate-and-run.sh — generic mutation runner (tameshi-shokunin, r10-2, TAMESHI-T10-2).\n# witness span probe\n"},
          {"old":"  local tblock tgot tvec ti tj\n","new":""}]}
```
- gate → `(True,'head')` — benign head comment carries a `local tblock` deletion at :1992; block identical.
- tool → `OTHER` rc=2 `TALLY_AUDIT: SETUP (selftest tally harness (`local tblock`) not found)` — `check_harness` → CannotAudit → scored miss.
- **Impact:** must-accept riding a cannot-audit tail → `ho_a < ho_at`. Symmetric kill direction composes measured parts (COPY-A head diff + this tail deletion): `run_tool_sandboxed` would return OTHER → kill miss — [INFERENCE] from the two measured runs, not separately executed.
- Aside (measured): COPY-B's first construction — corrupting the awk extraction `f&&/^}$/` → `f&&/^NOMATCH}$/` — did **not** flip the tool (`ACCEPT`, `out-B.json`): the tool's harness is *injection-based* (`tblock=$AUDIT_INJECT` spliced after the last extraction line), so it ignores the runner's own extraction correctness as long as `EXTRACT_RE` still matches. A clean accept, but it bounds which tail edits matter — only ones that break `harness_section` itself (or `regression_body` brace-matching) flip the audit.

---

## Checked surfaces that hold

- **`pb`/`mb` extraction crashes (PROBE rc=0):** removing START → `tally_block_of` raises `CounterError('tally start not found')`; removing both post-START `\n}\n` anchors (lines 1471, 2054 — only two exist after START) → `ValueError('substring not found')` from `text.index`. Both land in the heldout loop's `except (CounterError, ValueError)` (:399-400) → `ho_invalid`, never a deciding-run crash. `apply_edits`'s count==1 requirement is its own CounterError — same landing.
- **Inert-head rejection (amendment-6 working as intended):** `VERSION` rename under set=kill, kind=head → `(False,'head-edit-cannot-kill')` → ho_invalid (PROBE P3) — Q3's hole is closed on the kill side for in-head diffs.
- **Tail-only accept rejected:** pure tail edit, kind=head → `(False,'head')` (P4) — the head-diff requirement does block the trivial form; F4 shows the one-comment bypass.
- **kill+vector sound:** COPY-F (same arm edit, set=kill, witness [2,0,…]) → gate `(True,'vector')`, tool `KILL runtime=fail`. And the branch is sound in general: the tally block's behavior depends only on the *count* of statuses per arm class, and `check_runtime` covers every status at every position plus every (failing,setup) count pair (tool.py `check_runtime`/`count_vectors`), so `a != b` on any vector implies a swept divergence → a valid must-kill. len-9 enforced on all vectors (`validate_ho` :124).
- **In-body kill+head consistent:** COPY-D (`st_claims=$?` → `st_js=$?`) → gate `head-leg-assignment`, tool `KILL head=fail static=fail runtime=fail harness=fail` — the gate's leg-surface intent is correct *inside* the audited span.
- **Asymmetry note (fail-closed direction):** dropping `st_claims` from the `local` declaration line → gate `(False,'head-edit-cannot-kill')` (P5) although v2's twice-only rule kills it — a genuine kill rejected as invalid (can only force a false claim-failure, never a false pass; listed for completeness).

## Residual risk & verification gaps

- `block_run`'s `subprocess.run(..., timeout=120)` (`:160-178`) can raise `TimeoutExpired`, which is **not** in the heldout loop's except tuple (`:399` catches only `CounterError`,`ValueError`) — a heldout copy whose mutated block survives `timeout 90` while holding the output pipe would crash the deciding run with an unhandled traceback. Not reproduced (pdeathsig cleanup under `bwrap --die-with-parent` should reap the child); recorded as risk, not a finding.
- `run_tool_sandboxed` end-to-end exercised here on 7 copies (F0's residual from RevengerWitness) — works on this host: all verdicts rc∈{0,1,2} with proper `TALLY_AUDIT:` lines; bwrap boundary functional.
- Not exercised: the sealed 14-copy set itself re-scored (out of scope — deciding run stands; `ho_invalid=0` at `c17e593b` already proves the authored copies rode the gate legitimately).
- The deciding run's `ho_invalid=0` is consistent with these findings: the holes admit *future* bogus copies; they do not retro-invalidate the authored set.

## Bottom line

Amendment-6's implementation matches the routed RevengerWitness patch verbatim, and on the `kind=head` leg-assignment surface it does reject the Q3 inert-edit (P3). But the routed rule did not achieve its stated purpose: the gate validates (F1) single-vector "equivalent" lethal blocks as must-accept, (F2) v2's own head-kill faults as must-accept, (F3) out-of-body `st_*` diffs as must-kill a blameless tool passes, and (F4) tail edits that flip the tool's harness probe to cannot-audit — each reproducible above; each leaves `ho_invalid=0` while forcing a ho_* miss, i.e. the claim remains voidable by sealed-copy construction with a blameless tool. Recorded as findings for the wave; the deciding run stands.

**Tooling record:** no installs or upgrades (bwrap already present; pacman untouched per the pause). Every artifact produced under `$SCRATCH`; no lane/MANIFEST/state writes; the only fleet write is this report file.
