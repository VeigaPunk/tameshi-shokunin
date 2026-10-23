# Round 35 — the audit predicate widened to the runner's four configs, whole stdout, and comment-blind scans

L1 TameshiR35, attempt 2 (hyaku run-5). Attempt 1 died with the orchestrator session at 18:00-18:03
(OOM): its single v2 wave of 64 seats was dispatched at 18:02 and six of its reports landed uncommitted —
they are now inherited evidence under `.ufo/waves/round-35/w1/` (ExecPristine, RevengerRootShape,
ReviewPanelDistinct, ReviewSealedGate, ScribeReport, SealAcceptCommentBlock) and are cited below.
Attempt 2 re-dispatched the other 58 items as wave 2 (policy v1, band 32-64) against the amended
apparatus. Lane tip at freeze: `51d3f08073be65d3475cf0286042fc0dbe4c4a7d`; contract
`.ufo/evidence/round-35/contract.json` (claims C1/C2, predicates, counters, amendments A1-A6).

## What this round attacked, and why

The round-34 v2 wave left five convergent Holds (`.ufo/evidence/round-34/w1`, 64 seats). Round 35
takes the two that were structural, not measurement-only:

1. **The unswept config hole.** `tools/tally-audit-v2.py` ran the tally block under two of the four
   `(auto,KEEP)` triples — `(0,1)` and `(1,0)`. `(0,0)` (explicit `--workdir`, no `--keep`) and
   `(1,1)` (auto workdir, `--keep`) are real runner states and were never executed. Round-34 seat
   Mutkillvectorarmswap F3 found an accept-set swap gated on `auto == 0 && KEEP == 0`: witness-valid,
   tool-ACCEPTED, runner-selftest-passing, lethal under `--regression --workdir DIR`. That was the one
   accept-side hole that was **not** fail-closed.
2. **Comment text seizing structural scans.** Three false-kill/refusal classes: the twice-only head
   rule counted name SUBSTRINGS (an inert comment naming a leg → KILLED), `regression_body` counted
   braces char-wise (a `}` in a comment closed the function early), and `esac`/`do` in a comment seized
   the case/loop locators (SETUP refusal). Three or more seats corroborated the first.
Plus the OPEN recall class the round-34 correction disclosed: **whole-stdout comparison**. The oracle
compared the first stdout line and the exit code; the runner prints a second `REGRESSION_WORKDIR` line
whose wording and whose `rm` decision both depend on the config.

## The change — `tools/tally-audit-v3.py` (new file; v2 untouched)

- `CONFIGS` now holds all four `(root, auto, KEEP)` triples; the oracle is config-aware and compares
  the **FULL stdout** plus the exit code (`oracle(..., cfg)`; `run_vectors` captures both lines).
- `code_view(text)`: a same-length, quote-aware copy of the text with shell comment text blanked
  (newlines kept), so line-anchored regexes and every offset/slice still index the original bytes.
  `regression_body`, `tally_block`, `head_section`, `leg_names`, `check_head`'s counts,
  `counting_case`, `tally_loop`/`loop_extent` all scan the code view.
- **A4 (pre-data, from inherited seat RevengerRootShape CRITICAL):** the fixed root literals were
  replaced by the runner's real auto root — `root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)`
  (`tools/mutate-and-run.sh:1357-1365`). A copy gating `nfail=0` on that value masked a failing leg
  into PASS under the default `--regression` run while v3 ACCEPTED it. Both the tool and the counter
  now create a real `/tmp/tameshi-r4-2-regression.*` directory for the auto triples; the public panel
  gained `root-keyed-auto-mask` and `root-keyed-auto-zero` (5 kill + 3 accept = 8 copies).
- Selftest grew to 30 cases: the 28 above plus a real-root-gated mask kill seed and a real-root comment
  accept seed. `TALLY_AUDIT_V3_SELFTEST: 30/30 pass`.
- The runner is byte-identical (`a7d3f2dd…2eb9` at base and at every measured revision).

## C1 counter and its controls (frozen before data)

`.ufo/evidence/round-35/c1/c1-measure.py` (final sha256 `d27e6769…052c2`, re-pinned by A4-A6). Ground
truth is behavior computed without the tool: a copy is `kill` only if its tally block produces a
different `(exit, FULL stdout)` under at least one of the four configs; `accept` only if identical under
all four and every vector. A kill specimen must fail exactly the `runtime` check. **A5** hardened the
sealed gate: `manifest.json` is never parsed as a specimen; the freeze is the commit that first added
`contract.json` (not a self-declared field); last-touch must be a strict descendant and the lineage
creation commit must also descend from it; panel and sealed bytes are read at REV, not from the working
tree. **A6** re-pinned the counter's `TOOL_SHA256` to the A4 tool bytes after wave-2 seat
CriticPredicate caught the stale constant (deciding `tool_sha_ok=0` would have made C1 unpassable).

- **Before** at base `51d3f08`: `tool_present=0 … C1_R35_PASS=false`, exit 1 (`before/c1-at-base.stdout`).
- **Control** (do-nothing: keep v2, same panel): `pub_kill=0/6 pub_accept=0/3 PASS=false`, exit 1
  (`control/c1-v2-control.stdout`) — v2 accepts all six kill copies (both root-keyed copies and the
  shape-6 one) and kills/refuses all three accept copies. The control cannot reach the target.
- **A7** (pre-data, wave-2 seats): the block locator now takes the LAST `local nlegs=` match and ends at
  the first depth-0 `}` (seat AttackPerIndexParse: a here-doc decoy carrying a pristine block copy was
  audited instead of the real block, and a status-4 mask passed); the head rule flags any leg-name
  mention outside the `local` declaration and its bare `$?` assignment (seat SealKillHeadRead's
  `read` second write); the counter refuses to execute a specimen whose block reassigns `root` or adds
  an `rm -rf` (seat SentinelSandbox: specimen-derived bash could delete outside `--work`); the auto root
  now has the runner's six-alphanumeric mktemp SHAPE and the explicit triples carry one relative and one
  absolute `--workdir` root (seat ScoutRunnerConfigs). Tool selftest 33/33.

## C2 — self-assessment conformance (measured)

`.ufo/evidence/round-35/c2/c2-measure.py` (sha256 `67bb7118…9cc`), six classes counted over committed
bytes: header trio (m1), README index (m2), stranded seat file at the fleet root (m3), frozen contract
tool pin (m4), round-34 authoring receipt disagreement (m5), SCORECARD standing row count (m6).
Before at base: `m1=8 m2=3 m3=1 m4=1 m5=1 m6=1 total=15`, exit 1. After at `d16f9b5a`:
`m1=0 m2=0 m3=0 m4=0 m5=0 m6=0 total=0 C2_R35_PASS=true`, exit 0.

The repairs: header trios on `closeout-r11.md`, `survivor-fixture-minimization.md` (verified-at +
recheck), `witness-equivalence-rule.md`; three README index rows; the stranded
`.ufo/waves/round-34/w1/ReviewDevReceipts.md` copied byte-exact into the lane (`cmp` equal, sha
`ff532da3…b3c2`) and deleted from the fleet root; a pin-reconciliation record for the round-33
contract's stale tool digest; a `# ROUND-35 ADJUDICATION` block appended to
`.ufo/evidence/round-34/dev/authoring.stdout`; the standing sources-registry row's count replaced by a
re-derivable command and the observed value.

## Gate

Source opened this round: **S102** — POSIX.1-2024 Shell Command Language, §2.3 Token Recognition,
https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html (opened 2026-10-23 UTC;
357,953 bytes; sha256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`; committed
snapshot `.ufo/evidence/round-35/src/s102-posix-chap02.html`). Located quote (25 words, HTML `<tt>` tags
stripped): "If the current character is a '#', it and all subsequent characters up to, but excluding,
the next <newline> shall be discarded as a comment." (wave-2 seat ScoutCorpusRows caught the earlier
copy's inserted space before the comma — 26 tokens and not the page's bytes.) The `gnu.org` Bash manual Comments page timed out at 60 s (the same failure
r32 and r34 recorded); no row was written for it.

## Mistakes

1. **class:** a seat resolved a lane-relative report path from the fleet root. **evidence:** round-34
   seat ReviewDevReceipts wrote `.ufo/waves/round-34/w1/ReviewDevReceipts.md` into the FLEET repo
   (untracked; flagged by the mori misroot seat and by this round's own C2 m3 class). **captured-by:**
   C2 m3 (a counter class written this round: untracked `.ufo/waves/**` files whose content names
   tameshi). **fix:** copied byte-exact into the lane (`cmp` equal), fleet copy deleted; m3 1 → 0 on
   the same counter. Shown able to fail: the before receipt records `m3=1` at the base revision.
2. **class:** an evidence pointer inverted on a later correction. **evidence:** round-34 lesson
   `## Mistakes` §1 named `dev/authoring-receipts.json` as the *first* generation; it is the corrected
   one (PanelSeed4 F1). **captured-by:** the C2 m5 class (stdout `all_as_expected=False` vs JSON
   all-true, unreconciled). **fix:** adjudication block appended to the stdout and an append-only
   correction to the lesson; m5 1 → 0.
3. **class:** a pre-data amendment commit whose patch silently no-opped in one of the two files.
   **evidence:** the A4 commit `7267738` carries the tool with `cfg_root(...)` but the counter's
   `run_block` still read `root_s, auto_s, keep_s = cfg` (`git show 7267738:.ufo/evidence/round-35/c1/c1-measure.py`
   line 165), so the control scored the root-keyed copies as non-divergent (`div=-`) and interpolated
   `local root=None`. **captured-by:** the control run's per-copy `div=` column (both root-keyed
   copies printed `div=-`, i.e. a divergence-free "kill" copy — exactly the INVALID line) and the
   receipt stdout; that first receipt was superseded by the re-run, so the durable pointer is the
   pre-fix line 165 in commit `7267738` and the `div=(1,0),(1,1)` in the re-run receipt. **fix:** patch
   `cfg_root` into the counter's `run_block`, re-pin (A6), re-run before + control from the final bytes;
   the receipts at `68f2557` show `pub_kill=0/5` (control) and the two copies marked `div=(1,0),(1,1)`.
   Shown able to fail: the pre-fix commit's line 165 is still readable in history.
4. **class:** a counter whose parser silently discarded half of every record. **evidence:**
   `c1-measure.py` parsed `run_vectors` output with `str.splitlines()`, which splits at U+001E, the
   record separator used for embedded newlines — the first self-run against the pristine runner
   reported `30316/30316` mismatched, all of them phantom. **captured-by:** the counter's own pristine
   comparison (the oracle and the runner must agree on an unmutated block). **fix:** separator changed
   to U+001F and parsing to `split('\n')`; the frozen counter now reports `mismatched=0` on the
   pristine runner. Receipt: `.ufo/evidence/round-35/lessons/c1-splitlines-mutation.*` (the mutated
   parser loses the second line and the pristine comparison fails again).

## Holds (routed to round 36)

- **Head-side masks outside the block oracle** (wave-2 seat AttackQuotedHash, 3 specimens): an
  ANSI-C quoted `$'...'` string, a nested `"$(...)"`, and a backslash-newline continuation all hide an
  executed `st_tsu=0` from `code_view`, and the tool ACCEPTS the copy. The counter cannot express the
  class at all (its ground truth is the extracted block; `diverged_configs=[]`), so it can neither kill
  nor admit it — the head rule needs a real shell lexer, which is a round-36 successor, not a patch.
  The same weak lexer also under-blanks after `$'it\'s'` and false-kills an inert comment (K2).
- **stderr is outside the compared tuple** (wave-2 seat AttackStderrScope): a copy that adds a stderr
  line or moves `die_setup`'s message to stdout passes, even though the runner's own `--selftest`
  fails on it (`mutate-and-run.sh:2004-2006` merges the streams). BOUND-1, recorded.
- **The removed-workdir side effect is not compared** (same seat, M5): dropping `rm -rf "$root"` keeps
  exit and stdout identical while the directory stays; the header calls removal contract, the tuple
  cannot see it.
- ~~The witness shim's config fidelity (six round-34 seats).~~ Closed by A4 + A7 (value and shape):
  the sweep now carries a real `/tmp/tameshi-r4-2-regression.*` directory and the panel kills both
  root-keyed copies. Residue: the audited region is the tally BLOCK, so a copy that rewrites the root
  CONSTRUCTION outside it, or gates on `HOME`/`TMPDIR`/`PWD` values the harness still fixes, remains
  outside the sweep — the harness's env is a fixture, not the runner's real env.
- The tail region: `tally_block` ends at the function's last brace, and the harness is audited by its
  own panel — a defect in `run_regression`'s tail (between the tally block and the closing brace) is
  inspected by nothing.
- Preamble seeding, helper-function scope, name-assembled masks (`printf -v "st_$n" 0`),
  per-index record parsing: still open recall classes (round-34 Holds, measurement-only).
- Panel design: the public panel is now 6 distinct bodies; the deciding seed question is gone (v3 has
  no seed) but the panel is small — the sealed set is the discriminating surface.
- The C2 counter's m1 scope is time-relative (entries first added after `284ab0f0`); if the lane
  rewrites history or the baseline moves, re-derive the scope rather than trusting the constant.
