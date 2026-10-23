# AttackPerIndexParse — span-shift attack on the tally-audit-v3 block extractor

Seat: `L1tameshi35.AttackPerIndexParse`, tameshi round 35, wave 2.
Lane tip / measured apparatus: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.
Object under test (frozen, never edited):
`tools/tally-audit-v3.py` sha256 `ef98fc5367cdb12c71b8b0ddf5b83835100831f545f6510437dc84014865885`.

**Verdict: CRITICAL — v3 prints `TALLY_AUDIT: PASS` (exit 0) for a runner copy whose real
`local nlegs=` line is 41 lines later than the span the tool audits, and whose real tally
block flips `SETUP`→`PASS` on a status-4 leg. The audited span is a here-doc *data* body that
the tool executes as code. The copy is `bash -n` clean, is 106/106 green in the runner's own
`--selftest`, and is also accepted by the v2 control.**

Everything below is reproducible from the scratch tree
`/fast/scratch/hyaku/tameshi-r35-seats/AttackPerIndexParse/` (lane clone + `mutants/` + `out/`).

---

## 1. Setup and baseline

```
mkdir -p /fast/scratch/hyaku/tameshi-r35-seats/AttackPerIndexParse
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin .../AttackPerIndexParse/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach 7da6e076...
```
- lane `rev-parse HEAD` = `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (exit 0)
- lane `status --porcelain` = 0 lines after all work (exit 0) — the lane checkout is read-only and untouched
- `sha256sum lane/tools/tally-audit-v3.py` = `ef98fc53…5885` (matches pin)
- `sha256sum lane/tools/mutate-and-run.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches pin)

Baseline detector run (the detector is the tool itself; the object under test):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py \
        --runner /fast/scratch/hyaku/tameshi-r35-seats/AttackPerIndexParse/work/pristine.sh
```
exit **0**, output (byte-stable across two runs):
```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```
`pristine.sh` sha256 `a7d3f2dd…2eb9` — byte copy of the pinned runner. Baseline is green, so a
mutant that also exits 0 is an **accepted divergent copy**, not a baseline artefact.

## 2. The extractor logic under attack (all pointers to `tools/tally-audit-v3.py`)

| element | line | behaviour |
|---|---|---|
| `code_view()` | 150–193 | blanks **comments only**; here-doc bodies, `'…'`, `"…"` are left intact |
| `regression_body()` | 196–212 | brace depth counted on `code_view` (quotes are *not* stripped) |
| `START_RE` | 226 | `^[ \t]*local nlegs=` — **any** indentation, **first** match in the body |
| `tally_block()` | 229–238 | `body[first START_RE match : cv.rfind('}')]` (line 234) |
| `head_section()` | 240–244 | `body[: first START_RE match]` |
| `brace_depth_at()` | 215–224 | **defined and never called** (`grep -c brace_depth_at` = 1, the `def` line only) |

There is no check that the extracted start sits at brace depth 1, that the start line is code
rather than here-doc data, or that exactly one `local nlegs=` exists in the body. The whole
audit (head/static/runtime/harness) is computed on whatever span `START_RE` happens to hit.

## 3. CRITICAL — M9: here-doc decoy shifts the start 41 lines; tool accepts

**Construction** (`mutants/m9_heredoc_4sp.sh`, sha256 `7ff85219da720f4acd5272812a6ccc8dda293d40d01edbc3c272aae38769cd0d`,
`bash -n` exit 0). Between `st_citecheck=$?` and the real tally block, inside
`run_regression()`, insert:

```sh
  # printable copy of the tally logic for --explain (here-doc data; never executed)
  cat >"$root/tally-reference.txt" <<'TALLY_REF'
<the pristine tally block, each line indented +4 spaces>
TALLY_REF
```

and add the defect `      4) npass=$((npass + 1)) ;;` to the **real** block's `case`.
The decoy is indented with 6 spaces so the runner's own two locators — which hard-code exactly
two spaces — do not see it:

* `sed -n 's/^  local nlegs=\([0-9][0-9]*\) .*/\1/p' "$SELF"` (`mutate-and-run.sh:1954`) → `9`
* `awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} …'` (`mutate-and-run.sh:1994`) →
  the **real** block, sha256 `68a3ee59498faeac73600f38dab8e8567b51a84bc7dfa035a9e053015bc114ff`

while `START_RE`'s `[ \t]*` matches it.

**What the tool audits vs what runs** (`span_probe.py`, imports the frozen tool read-only and
calls its own `regression_body` / `head_section` / `tally_block`):

```
mutants/m9_heredoc_4sp.sh
  audited body      : lines 1345..1515 (8768 bytes)
  audited head ends : line 1434
  audited span      : line 1434 .. 1514  sha256=0bb43c8eed26c4d2e56cd2fdea7cd70a57befe2e11407ad01babb1c9f1fa7550
  audited first line: '      local nlegs=9 npass=0 nfail=0 nsetup=0 st'
  REAL span         : line 1475 .. 1514  sha256=68a3ee59498faeac73600f38dab8e8567b51a84bc7dfa035a9e053015bc114ff
  SAME_BYTES=False
```
(pristine, same prober: audited span lines 1432..1470, sha256 `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`, `SAME_BYTES=True`.)

The audited span begins inside the here-doc, so the here-doc *content* becomes top-level code in
the tool's driver: it is a byte-copy of the pristine block, therefore behaviourally identical to
the oracle for every vector, and its trailing `exit 0`/`exit 1`/`exit 2` terminates each vector's
subshell before the real (defective) block is reached.

**Detector on M9 — the tool accepts:**

```
timeout 600 python3 .../tools/tally-audit-v3.py --runner .../mutants/m9_heredoc_4sp.sh
```
exit **0**, twice, byte-identical (`out/m9.audit.1` == `out/m9.audit.2`):
```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

**Ground truth that the copy diverges** (`probe.py` — selects the *real* block by the LAST
`  local nlegs=9 …` line through the next `^}$`, i.e. a rule the tool does not use, and compares
pristine-block vs candidate-block on (exit, FULL stdout) over the four (root, auto, KEEP)
triples: `('tally-audit',0,1)`, `('/tmp/tally-audit-work',1,0)`, `('tally-audit-explicit',0,0)`,
`('/tmp/tally-audit-work-keep',1,1)`):

```
python3 probe.py work/pristine.sh mutants/m9_heredoc_4sp.sh   # exit 3
DIVERGE cfg(0,1) one-4@0  pristine=(2,'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) | REGRESSION_WORKDIR: tally-audit (kept)')
                          candidate=(0,'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0) | REGRESSION_WORKDIR: tally-audit (kept)')
… (one-4 at each of the 9 positions, all 4 triples)
vectors_compared=84 divergent=36
VERDICT_BEHAVIOR: DIVERGENT
```
84 = 21 vectors (all-zero, one-4 ×9, one-255 ×9, two mixed) × 4 triples; the 36 divergent
comparisons are exactly one-4 ×9 ×4 triples — a **verdict flip SETUP(2) → PASS(0)** at every leg
position. `probe.py` on pristine-vs-pristine: `vectors_compared=84 divergent=0`,
`VERDICT_BEHAVIOR: IDENTICAL`, exit **0** (self-check of the prober).

**The copy is green in the runner's own guard too:**

```
bash mutants/m9_heredoc_4sp.sh --selftest      # exit 0
MUTATE_SELFTEST: 106/106 pass
VERDICT: PASS
```
(pristine: exit 0, 106/106 — same.) The v2 control tool also accepts it:
`python3 tools/tally-audit-v2.py --runner mutants/m9_heredoc_4sp.sh` → exit **0**,
`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, so the class predates v3.

**Why this falsifies C1.** C1's predicate is "the v3 tool kills every kill specimen (divergent
behaviour under at least one of the four configs; failing check exactly `runtime`)". M9 is a kill
specimen by that definition (divergent on all four configs, check that should fail: `runtime`)
and v3 returns PASS. None of the four round-35 fixes touch it: the four-config sweep ran all
four triples (`vectors=30316 mismatched=0`), the full-stdout compare was applied, `code_view`
blanked comments (`# printable copy…` is inert) and the auto triples ran under the runner's real
auto root (`CONFIGS` roots are `None` at `tally-audit-v3.py:349-350`, materialised as
`tempfile.mkdtemp(prefix='tameshi-r4-2-regression.', dir='/tmp')` by `auto_root()` at
`:355-366`; the observed witness line is `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.7mx213bt`
in `out/m4_quoted_string.audit`). The defect sits upstream of all four: **which span is audited**.

Note the tool's own selftest lists this exact defect as must-kill — case `('status 4 passes', …,
1, 'runtime')` (`tally-audit-v3.py:763-764`) — and it does kill it when no decoy precedes the
block (`mutants/m7_plain_defect.sh` → `CHECK runtime FAIL … mismatched=3348`, exit 1). The
extractor, not the oracle, is what fails.

Reproduce in one line:
```
python3 tools/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-seats/AttackPerIndexParse/mutants/m9_heredoc_4sp.sh; echo $?   # 0
```

## 4. BOUND — the other span-shift shapes are fail-closed (with proof)

| # | shape | copy sha256 | tool output | exit |
|---|---|---|---|---|
| M2 | nested function `tally_reference() { … }` holding the pristine copy, before the defective real block | `0352dc9c…57afb` | `TALLY_AUDIT: SETUP (tally driver failed (exit 1, 0/7561 results): … local: can only be used in a function / st_js: unbound variable)` | 2 |
| M5 | subshell `( … )` decoy before the defective real block | `627e0d6f…2c6d` | `TALLY_AUDIT: SETUP (tally driver failed (exit 2, 0/7561 results): … syntax error near unexpected token ')'` | 2 |
| M3 | `}` **inside a double-quoted string in CODE** after the block (`printf '%s\n' "}" >/dev/null`), no defect | `6cbb8151…496` | `TALLY_AUDIT: SETUP (tally driver failed (exit 2, 0/7561 results): … unexpected EOF while looking for matching '"')` | 2 |
| M3b | same `}` shift + the same status-4 defect | `05e1ab25…e25` | same SETUP (unterminated quote in the truncated span) | 2 |
| M4 | multi-line **single-quoted string** decoy + defect | `1c24c536…88b` | `TALLY_AUDIT: FAIL (head=fail static=pass runtime=fail harness=pass)` — leg names counted 3× in the head, defect also caught at runtime | 1 |
| M8 | here-doc decoy placed **before the leg assignments** (2-space indent) + defect | `2dc874bb…b3e` | `TALLY_AUDIT: FAIL (head=fail static=fail runtime=fail harness=fail)` — `legs=0 (none found)` | 1 |

Mechanism of the refusals, so they are not luck: M2/M5 leave a stray `}`/`)` in the extracted
span at brace/paren depth 0 → bash cannot parse the driver → `run_vectors` raises
`CannotAudit('tally driver failed …')` → `TALLY_AUDIT: SETUP`, exit 2 (fail-closed). M3/M3b cut
the span mid-quote in `regression_body`/`rfind('}')` → unterminated quote → same SETUP. M4's
quoted-string decoy lands in the **head** (quotes are not blanked by `code_view`), so the
twice-only leg-name rule fires before the runtime check. M8 removes every `st_x=$?` from the
head, so `names` is empty and all four checks fail. **The one shape bash can parse — a here-doc
body — is the one that is accepted.**

`probe.py` confirms M2/M4/M5 are behaviourally divergent too (`exit 3`, `DIVERGENT`,
`divergent=36` each), so these are genuine kill specimens that were refused rather than missed.

## 5. What I could NOT break (bounded negatives, with proof)

- **Comment decoys.** `# the tally block begins with the same local nlegs=9 line…` before a
  defective block (`mutants/m6_comment_decoy.sh`, sha `7e4bd285…b6b6`): `code_view` blanks it, the
  real block is audited, e.g. `CHECK runtime FAIL … mismatched=3348`, `TALLY_AUDIT: FAIL`, exit 1.
  The round-35 comment-blind fix holds for this attack.
- **A plain status-4 defect with no decoy** (`mutants/m7_plain_defect.sh`, sha `12ad1d90…27b`):
  `CHECK runtime FAIL vectors=30316 mismatched=3348; first: cfg(1,0) statuses 4 0 0 0 0 0 0 0 0:
  got 0 'REGRESSION: PASS …', want 2 'REGRESSION: SETUP …'`, exit 1.
- **End-side truncation that alters behaviour.** `rfind('}')` (line 234) always takes the last
  brace of the body, so nothing after the block can be excluded while the block stays parseable;
  the only truncations available land inside a quoted string and are refused (M3/M3b). I did not
  find any parseable end-shift.
- **The harness check.** M9's `CHECK harness PASS reference cases=9; faults rejected=34/34` shows
  the runner's own tally harness is driven with an injected reference block
  (`run_harness` splices `tblock=$AUDIT_INJECT` after the last extraction line, lines 519–536),
  so the harness check cannot see the container the block sits in — it was never a candidate
  defence here, and it is not a defect of that fix.
- **Config dependence.** The decoy reproduces the pristine byte behaviour, so all four triples
  agree; nothing in the new sweep can catch it (30316/0 mismatched on M9).

## 6. Corollary — HYGIENE, and why the class is reachable in practice

1. **Dead defence already present.** `brace_depth_at()` (`tally-audit-v3.py:215–224`) computes
   exactly the quantity that would reject M9 (`depth == 1` at the start offset) and is called
   from nowhere. One `if brace_depth_at(body, m.start()) != 1: raise CannotAudit(…)` in
   `tally_block`/`head_section` closes this whole family. Not applied here (attack seat).
2. **The auditor and the repo's own locator disagree on the anchor.** The runner pins the tally
   line at exactly two spaces (`mutate-and-run.sh:1954` sed, `:1994` awk); the auditor accepts
   `[ \t]*` (`tally-audit-v3.py:226`). The looser side is the one that can be moved by data.
3. **A 2-space decoy is caught only by a side channel.** M1 (`mutants/m1_heredoc_ref.sh`, sha
   `13af38d9…383a`) — same construction, decoy at the runner's own 2-space indent — is also
   accepted by v3 (exit **0**, same PASS block) and diverges (`probe.py` exit 3, `divergent=36`),
   but the runner's `--selftest` fails 1/106 on `leg-count agreement: calls=9 specs=9 nlegs=9`
   because `lnlegs` now returns two values. So the *runner* noticed by accident; the auditor did
   not. M9's 6-space indent defeats that side channel and is 106/106 green.
4. Neither the tool nor the runner validates that the here-doc body is *data*; `code_view`'s
   docstring claims "comment text is data, never code" (line 26–28) but here-doc bodies and quoted
   strings are neither blanked nor isolated, so "data" is executed as code by the runtime oracle.

## 7. Restoration / integrity trail

- No write outside `/fast/scratch/hyaku/tameshi-r35-seats/AttackPerIndexParse/` and this report.
  The lane checkout was never written (`git -C …/lane status --porcelain` → empty, exit 0).
- Frozen artifacts re-hashed **after** all work, unchanged:
  - `tally-audit-v3.py` `ef98fc5367cdb12c71b8b0ddf5b83835100831f545f6510437dc84014865885`
  - `tally-audit-v2.py` `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`
  - `mutate-and-run.sh` `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
- Specimens (all under `.../AttackPerIndexParse/mutants/`, `bash -n` clean):
  `m1_heredoc_ref 13af38d9…383a`, `m2_nested_fn 0352dc9c…57afb`,
  `m3_brace_in_quote 6cbb8151…496`, `m3b_brace_in_quote_defect 05e1ab25…e25`,
  `m4_quoted_string 1c24c536…88b`, `m5_subshell 627e0d6f…2c6d`,
  `m6_comment_decoy 7e4bd285…b6b6`, `m7_plain_defect 12ad1d90…27b`,
  `m8_heredoc_before_head 2dc874bb…b3e`, `m9_heredoc_4sp 7ff85219…cd0d`.
  `work/pristine.sh a7d3f2dd…2eb9` (pristine control, byte copy of the pin).
- Detector/prober sources in the same scratch dir: `probe.py` (independent real-span selector +
  four-triple comparison), `span_probe.py` (prints the tool's own chosen span), `gen.py`
  (mutant generator).
- Tooling installs: none (all tools used were already present; no pacman, no uv/npx).

## 8. Ranked summary

| rank | item | evidence |
|---|---|---|
| **CRITICAL** | v3 audits a here-doc *data* body as the tally block; a defective real block (`4) npass`) is accepted: `TALLY_AUDIT: PASS`, exit 0, twice byte-identical; behaviour flips SETUP→PASS on 36/84 comparisons; audited span `0bb43c8e…` vs real `68a3ee59…` | §3 |
| **BOUND** | Nested-function, subshell, `}`-in-quoted-CODE and quoted-string shifts are refused (SETUP exit 2 / FAIL exit 1), and a decoy before the head fails all four checks | §4 |
| **HYGIENE** | `brace_depth_at()` is dead code that would close the hole; the auditor's anchor is looser than the runner's own (`[ \t]*` vs two spaces); the runner's selftest catching M1 only via `lnlegs` line-counting is incidental, not a defence | §6 |
