# W2RevengerV1Docstring — v1 counter docstring vs code, hunk by hunk

Seat: revenger (read-only) · Round 36 wave 2 · 2026-10-24 · Scratch: `/fast/scratch/hyaku/tameshi-r36-seats/W2RevengerV1Docstring/`
No subagents spawned; no tools installed (none needed; python3 3.14 + git + bash were sufficient); no lane write besides this file; no pacman.

## Target and provenance

- Attacked: `.ufo/evidence/round-35/c1/c1-measure.py` (v1 counter, frozen), 535 lines, worktree sha256 `d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3` — byte-identical to the frozen v1 sha recorded in `corpus/lessons/round-36-verifier-spotcheck.md` ("v1 counter unchanged (d360a159… at both revs)"). All probes ran against a scratch copy with that same sha.
- Pin cross-check at lane tip `fbb01cf46f8437fd1264c1a3acc053c882fa2164`: worktree `tools/tally-audit-v3.py` = `6188db16…` (= `TOOL_SHA256`), `tools/mutate-and-run.sh` = `a7d3f2dd…` (= `PIN_RUNNER`). Runner at the pre-freeze parent `51d3f08073be65d3475cf0286042fc0dbe4c4a7d` also hashes to `a7d3f2dd…` (`git show 'd16f9b5a^:tools/mutate-and-run.sh' | sha256sum`).
- Freeze reconstruction: `git log --reverse --diff-filter=A` shows the round-35 contract and the tool were first added in the SAME commit `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` (2026-10-23 17:31:25 -0300); `sealed/manifest.json` declares `freeze_rev: d16f9b5a…` — the counter's BOUND-1 gate (freeze = contract first-add, manifest must name it) is coherent with history.
- LSP: no `lsp` device is present in this session's tool inventory (only `xd://ast_edit` and `xd://debug` are exposed), and the target is a standalone evidence script with no language server attached. Recorded per role: semantic navigation used `read`/`grep` as the literal fallback; no grep output is presented as semantic proof — every behavioral claim below is backed by an executed run or probe.

## Mode verification (each documented mode, executed)

Every run: `python3 <v1 counter> --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --work <scratch empty dir> [flags]`.

| # | Mode | REV | Flags | Receipt (last line) | rc | Docstring verdict |
|---|------|-----|-------|----------------------|----|-------------------|
| R1 | deciding (default) | `fbb01cf…` (tip) | `--sealed .ufo/evidence/round-35/c1/sealed` | `C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=fbb01cf… C1_R35_PASS=true` | 0 | ✓ 16 COPY lines (9 pub + 7 ho), kills all `checks=runtime` alone, accepts all `rc=0`; sealed provenance gate silent (passed); reproduces the round-35 deciding receipt (`.ufo/evidence/round-35/after/c1-at-34fa5b0c….stdout`) field-for-field at a new rev. Wall 162.8 s. |
| R2 | control, lane-relative tool | `fbb01cf…` | `--tool tools/tally-audit-v3.py` | `C1_R35_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 … pub_kill=6/6 pub_accept=3/3 … ho_kill=0/0 … C1_R35_CONTROL_PASS=false` | 1 | ✓ Runs to completion with no `--sealed`; label and predicate name switch to `C1_R35_CONTROL`; relative path resolved from REV bytes (`git_show`), matching the historical control receipt shape (rev `5829676d`). Wall 92.5 s. |
| R3 | control, absolute tool | `fbb01cf…` | `--tool /fast/scratch/…/tool.py` (scratch copy, sha `6188db16…`) | byte-identical to R2 | 1 | ✓ Absolute branch (`open()` on disk) behaves identically; matches "lane-relative at REV or absolute". |
| R4b | before, tool absent | `d16f9b5a^` = `51d3f080…` | `--before` | `C1_R35: mode=before tool_present=0 runner_sha_ok=1 rev=51d3f080… C1_R35_PASS=false` | 1 | ✓/✗ scores nothing ✓; reproduces the SCORECARD round-35 before receipt verbatim (same rev, same fields). But see D2: "asserts the tool is absent" is not what the code does. |
| R5b | before, tool PRESENT | `fbb01cf…` | `--before` | `C1_R35: mode=before tool_present=1 runner_sha_ok=1 rev=fbb01cf… C1_R35_PASS=false` | 1 | ✗ see D2 — identical exit/PASS whether the tool is present or not. |
| R4' (accidental, kept as evidence) | deciding, everything missing | `51d3f080…` | none | `mode=deciding tool_present=0 … pub_slots=0 … sealed_after_freeze=1 … C1_R35_PASS=false` | 1 | Demonstrates deciding at a tool-less, panel-less rev: no crash, placeholders, exit 1. |
| R5' (accidental, kept as evidence) | deciding without `--sealed` | `fbb01cf…` | none | `mode=deciding tool_present=1 … pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=0/0 … sealed_after_freeze=1 C1_R35_PASS=false` | 1 | Demonstrates "deciding requires the sealed set" is enforced only by predicate arithmetic (ho counts), not by a setup assert — and prints `sealed_after_freeze=1` although the gate never ran (O2). |

R5' also re-confirms at the tip the exact pub surface that round 36 froze as C2 targets: 6 kill + 3 accept slots, 9 distinct bodies.

## Hunk-by-hunk docstring audit

| Docstring claim (location) | Code | Verdict |
|---|---|---|
| Module: kill class — diverges under ≥1 of the four triples, tool kills with `rc 1` and failing check `runtime` alone | `score_copies`: `row['pass'] = bool(div) and rc == 1 and failed == ['runtime']` | ✓ verified in R1 (every kill row `checks=runtime`, `rc=1`) |
| Module: accept class — identical under ALL four triples and every vector, tool `rc 0` | `row['pass'] = (not div) and rc == 0`; `behavior()` runs 271 vectors × 4 configs | ✓ verified in R1 |
| Module: invalid = no-divergence kill / diverging accept / edits not applying exactly `count` times | `apply_edits` count check; `row['valid']` logic | ✓ code-verified; note the code has two MORE invalid subclasses the module list omits: extraction-refused and driver-refused (each documented only in their function docstrings) — underdocumentation, O3 |
| Module: panel public, "committed before the freeze"; sealed read at REV; sealed last-modifying commit must descend from freeze, "first-add is not enough" | `main` loads BOTH pub and sealed via `load_copies_rev` (git ls-tree/show at REV); provenance gate: manifest `freeze_rev` == contract first-add, `rev != first`, ancestry both directions, per-file `last` strictly after `first`, `origin` (with `--follow`) after `first` | ✓ gate passed silently in R1; manifest `freeze_rev` = `d16f9b5a…` = observed first-add |
| Module A7: "the tally-block locator **selects the LAST** `local nlegs=` match" | `tally_block` REFUSES any ambiguity: `SETUP: tally start occurs N times; ambiguous body refused`; the inline comment states a last-match rule is exactly what seat ReviewAttribution CRITICAL-2 defeats | ✗ **D1 — doc/code divergence** (empirical: probe P2) |
| Module A7: "ends at the first depth-0 `}`" | depth scan from the tally start, `end` at first `}` seen at depth 0 | ✓ probe P1 (block excludes the closing brace; head = everything before `local nlegs=`). Sharp edge confirmed, not claimed otherwise: the brace fence is quote-blind — P4 shows `: '}'` cuts the block mid-line (the driver-refusal path acknowledges this) |
| Module A7: specimen reassigning `root` or adding `rm -rf` "invalid, never executed for scoring" | `unsafe_block` runs BEFORE `behavior()`/`run_tool` in `score_copies` | ✓ order verified; but gate wording is broader than the docstring (D3) |
| Module Modes: "deciding (default) tool = tools/tally-audit-v3.py **at REV**; requires the sealed set" | tool bytes via `git_show` at REV; sha gate `tool_sha == TOOL_SHA256`; sealed required only via ho-count arithmetic | ✓ R1; "requires" is predicate-enforced, not setup-asserted (R5') |
| Module Modes: "control — `--tool PATH` (lane-relative at REV or absolute); never needs sealed" | `if a.tool:` branch; relative → `git_show(lane, rev, path)`, absolute → `open()`; whole sealed block skipped when omitted | ✓ R2/R3 |
| Module Modes: "before — **asserts the tool is absent** at REV and scores nothing" | before-branch: prints `tool_present=%d` and `return 1` unconditionally; never compares `tool_present` to anything | ✗ **D2 — doc/code divergence** (R4b vs R5b: identical exit 1 with tool absent AND present; the "assertion" is left to the human reader of the line) |
| Module: "The tool carries the same four triples" (CONFIGS lockstep) | counter `CONFIGS` literal byte-identical to tool `tools/tally-audit-v3.py:390-391` (probe P7) | ✓ |
| Module: "Prints one line per copy and the predicate line. Exit 0 iff the predicate is true" | R1: 16 COPY lines + predicate line, exit 0; R2/R3/R4b/R5b/R5' exit 1 | ✓ |
| `auto_root` docstring: real runner shape `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, six alphanumerics | generates exactly 6 chars from `[A-Za-z0-9]`, atexit cleanup | ✓ (shape witness; exercised by every R1–R3 run) |
| `code_view`: "Same-length copy with shell comment text blanked (quote-aware)" | quote-aware scanner blanks `#`-to-EOL only after ` \t\n;|&(` | ✓ probe P6 (commented `# st_b=$?` not matched as a leg) |
| `unsafe_block` docstring: "adds another `rm -rf`" | gate flags ANY `\brm\b` segment lacking `$root` | ✗ **D3 — wording narrower than code** (probe P5: plain `rm /tmp/other` also invalid) |
| `load_copies_rev` docstring (BOUND-4 story) | reads committed bytes; `manifest.json` excluded as specimen | ✓ |
| `load_copies` docstring ("Panel copies from disk") | function is NEVER called — dead since BOUND-4 moved the pub read to REV | O1 (dead weight in a frozen file) |
| Module: kill class "the runner's four `(auto,KEEP)` triples" | triples are (root, auto, KEEP); two vary the real auto root, and the R1 kills `root-keyed-*` diverge precisely on the root axis | O4 (shorthand undersells the root axis the counter itself added) |

## Divergences and observations (final)

- **D1 (real, certain).** Module docstring A7 hunk claims the locator "selects the LAST `local nlegs=` match"; the frozen code refuses any ambiguity (`SETUP: tally start occurs 2 times; ambiguous body refused` — probe P2 on a here-doc decoy). A last-match rule is precisely what the inline comment says must not exist (ReviewAttribution CRITICAL-2). The stale sentence also propagated verbatim into the v2 successor's docstring (`diff` v1↔v2: docstring otherwise the claimed header/label/predicate-only delta). Doc should read: "refuses any ambiguous tally start; selects the single `local nlegs=` match".
- **D2 (real, certain).** `before` is documented to "assert the tool is absent at REV"; it only REPORTS `tool_present=0|1` and returns 1 with `PASS=false` in both cases (R4b vs R5b — same exit, same verdict). Scores nothing: true. An actual absence assert would have to branch on the bit; it never does.
- **D3 (real, minor).`unsafe_block` docstring exemplifies "adds another `rm -rf`"; the gate invalidates any `rm` whose target segment lacks `$root` (probe P5: `rm /tmp/other` flagged). Code stricter than doc.
- **D4 (underdocumentation, certain).** The docstring's predicate description omits the sealed-side minimums `ho_kill_total >= 4 and ho_accept_total >= 2` (plus `ho_invalid == 0`, `sealed_ok`, `runner_ok`, `tool_sha_ok`). These are load-bearing: a sealed set under 4 kill / 2 accept fails the predicate even with a perfect score; the historical sealed set (4 kill + 3 accept) sits exactly on the minimum.
- **O1.** `load_copies` (:266) is dead code — the working-tree read path that BOUND-4 removed; retained in a file pinned by "no counter edit after freeze" rules. Note for a future round, not an edit.
- **O2.** With `--sealed` omitted the final line still prints `sealed_after_freeze=1` (gate skipped, `sealed_ok` initialized True) — R5' shows `ho_kill=0/0 … sealed_after_freeze=1 PASS=false`. The field is vacuously true in sealed-less receipts; misleading to a receipt reader, harmless to the predicate.
- **O3.** Module "invalid" enumeration omits the extraction-refused and driver-refused invalid subclasses (each documented only locally). The v2 docstring inherits the same gap.
- **O4.** "(auto,KEEP) triples" shorthand: the four triples also vary `root` (the RevengerRootShape axis); R1 kill rows `div=(1,0),(1,1)` / `div=(0,0)` are root- or cfg-keyed. Wording only.
- Vacuous-accept confirmation (context for C2, not re-run by this seat): v1's `ok` term `pub_kill == pub_kill_slots` is self-referential against the manifest; the committed receipts `.ufo/evidence/round-36/control/v1-at-emptypanel.stdout` and `.ufo/waves/round-36/w1/RevengerEmptyPanel.md` show v1 printing `pub_kill=0/0 … C1_R35_PASS=true` on an emptied-panel mutant — matching the code read here.

## Exact commands run

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c1/c1-measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev fbb01cf46f8437fd1264c1a3acc053c882fa2164 \
  --work /fast/scratch/hyaku/tameshi-r36-seats/W2RevengerV1Docstring/w-dec \
  --sealed .ufo/evidence/round-35/c1/sealed                       # R1 deciding, exit 0
# same with --work .../w-ctlr --tool tools/tally-audit-v3.py       # R2 control-rel, exit 1
# same with --work .../w-ctla --tool /fast/scratch/hyaku/tameshi-r36-seats/W2RevengerV1Docstring/tool.py  # R3 control-abs, exit 1
# same with --rev 'd16f9b5a18945ede3852ec3df7eb4ee4b0afbafc^' --work .../work-before --before   # R4b, exit 1
# same with --work .../work-before-head2 --before                  # R5b, exit 1
# same with --rev 'd16f9b5a…^' (no flags)                          # R4', exit 1
# same with (no --sealed)                                          # R5', exit 1
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 'd16f9b5a18945ede3852ec3df7eb4ee4b0afbafc^:tools/mutate-and-run.sh' | sha256sum
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --reverse --diff-filter=A -- .ufo/evidence/round-35/contract.json tools/tally-audit-v3.py
diff -u .ufo/evidence/round-35/c1/c1-measure.py .ufo/evidence/round-36/c1/c1-measure-v2.py
# + synthetic probes P1–P7 on the scratch copy (tally_block/unsafe_block/leg_names/CONFIGS literals)
```

All scratch output stayed under `/fast/scratch/hyaku/tameshi-r36-seats/W2RevengerV1Docstring/`; the counter's own writes went only to those `--work` dirs and its atexit-cleaned `/tmp/tameshi-r4-2-regression.*` auto roots. Frozen artifacts untouched; the only lane write is this report.

## Verdict

**VERDICT: the v1 counter's executable behavior matches its docstring in all three modes where it matters (deciding reproduces `C1_R35_PASS=true` exit 0 at the tip; control runs sealed-less in both path flavors; before scores nothing) — with two certain doc/code divergences (D1: docstring claims a last-match tally locator that the code replaced with ambiguity refusal; D2: `before` reports rather than asserts tool absence, failing identically either way) and two minor wording/underdocumentation items (D3, D4); no code defect found in the frozen file.**
