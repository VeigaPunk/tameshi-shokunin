# Round-35 w2 — ConnectorFirstLine (cross-lane scan: how sibling gates assert a transcript)

Seat: `tameshi-r35-w2-ConnectorFirstLine` (leaf connector, godspeed, adjacency-judged). Lane pin at
dispatch `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Frozen bytes re-verified at the pin in the
scratch clone (`/fast/scratch/hyaku/tameshi-r35-seats/ConnectorFirstLine/lane/`, read-only):

```
sha256sum tools/tally-audit-v3.py tools/tally-audit-v2.py tools/mutate-and-run.sh \
          .ufo/evidence/round-35/c1/c1-measure.py .ufo/evidence/round-35/c2/c2-measure.py
ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885  tools/tally-audit-v3.py
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tools/tally-audit-v2.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  tools/mutate-and-run.sh
515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8  .ufo/evidence/round-35/c1/c1-measure.py
67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc  .ufo/evidence/round-35/c2/c2-measure.py
```

All five match contract.json `frozen_artifacts` (exit 0). Setup note: the clone directory already
existed from attempt 1 parked at `d16f9b5a` (the C2 receipt rev); the pinned dispatch commit was
brought in with `git fetch` (read-only against the origin worktree) + `git checkout -q --detach
7da6e076…` → `git rev-parse HEAD` = `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`, `git status
--porcelain` empty. Sibling lanes were read READ-ONLY under `/home/vgpnk/Projects/shokunin/`; the
only write in the lane tree is this report. No installs, no `pacman`, no subagents, no labrat.

---

## 1. What I attacked

The class round 35 closed in tameshi: the runtime oracle compared only the FIRST stdout line plus
the exit code, so a defect confined to any later line (the REGRESSION_WORKDIR contract) was
invisible. v3 closes it — docstring fix 2 (`tools/tally-audit-v3.py:19-22`) and the code itself:
`tools/tally-audit-v3.py:385` ("the sweep must run under all four, and compare the FULL stdout
(round 35)"), `:392-398` (records the whole block stdout with newlines round-tripped through
`\x1f`), `:402` ("Expected (exit, FULL stdout) for one run under one config").

Fleet question: which SIBLING gates still assert a replayed/recorded command's transcript by a
PARTIAL projection — first stdout line only, exit code only, or any one-line/one-field/substring
reduction — instead of whole-transcript equality?

Method: inventoried every sibling's gate-bearing dirs (tools/, scripts/, corpus/*.sh,
verifiers/, corpus/fixtures/, corpus/instruments/, plans/ across all 21 sibling lanes), then
swept each gate file for the comparison shapes (`head -n 1`, `tail -n 1`, `split('\n')[0]`,
`splitlines()[0]`, `firstLine`, `NR==1`, `returncode ==`/`status ===` with and without a stdout
term), then read every hit in context to separate ASSERTIONS (`ok:`/verdict/PASS conditions)
from display truncation (`detail:` strings). A fleet-wide filename `find` timed out at 300 s
(bg job killed); compensated by the exhaustive per-lane directory listings plus the targeted
sweeps — bounded negative, disclosed.

## 2. Found — four sibling gates assert a transcript by a partial projection (all BOUND, none CRITICAL)

No sibling gate compares only the FIRST stdout line (that exact shape is tameshi-v2's, retired
with v2), and none asserts exit-code-only on a replayed transcript. What exists is the same
blindness family with different projections:

### BOUND-1 — kagi `corpus/claim-ledger.sh` `verify`/`cells`: exit equality + ERE on the LAST non-empty output line
Exact comparison (production path):
- `kagi-shokunin/corpus/claim-ledger.sh:593-595` — each claim row's recorded command re-run as
  `out=$(cd "$ROOT" && … timeout -k 5 "$tmo" bash -o pipefail -c "$cmd" 2>&1) || rc=$?` (stderr
  MERGED into the compared stream).
- `:612-614` — `if [[ $rc -ne $want ]]` → FAIL (exit equality required).
- `:616` — `last=$(printf '%s\n' "$out" | grep -v '^[[:space:]]*$' | tail -n 1 || true)` — the
  single last non-empty line.
- `:621-623` — PASS iff `[[ $last =~ $expect ]]`. Everything above the last line is never
  compared.
Selftest mirror of the same rule: `:1574-1575` `if [[ $rc -eq $want_rc && $last == "$want_line" ]]`.
Documented rationale (docstring `:26-30`): "the exit code equals the expected one AND the
expected ERE matches the LAST non-empty output line… a verdict is a summary line by
construction." Fail-closed in the verdict-then-fails direction; open to intermediate-line drift
and to stderr noise shaping the compared line (tameshi's r32 review ruled the opposite pole:
stderr never enters the compared string, `tally-audit-v3.py:64`).

### BOUND-2 — kumitate `scripts/counter-rerun.mjs`: exit + byte-equality of the FINAL summary line only
- `kumitate-shokunin/scripts/counter-rerun.mjs:129-138` — `finalSummary()` = last non-empty
  stdout line (bytes, one trailing CR removed); everything before it ignored by design.
- `:220-226` — a run DISAGREEs if it `exited non-zero` (:221-223) or if
  `Buffer.compare(r.summary, first) !== 0` (:224) — the ONLY stdout comparison is that one line.
- `:210` records `stdout_bytes=`/`stderr_bytes=` per run but never compares them.
Self-documented claim boundary (`:36-42`): "FINAL-SUMMARY-LINE AGREEMENT ONLY… It does NOT claim
full-output agreement… An AGREE verdict here therefore means 'this counter's headline number
reproduced', never 'this counter's whole output reproduced'." (The inherited round-47 A2 reruns
read `held=3/5` three different ways with the same final line — their own example.)

### BOUND-3 — tabi `scripts/check-measurement-binding.mjs --reproduce`: exit 0 + one count field of a one-line JSON stdout
- `tabi-shokunin/scripts/check-measurement-binding.mjs:546-553` — reproduction arm refuses on
  signal/timeout and on `result.status !== 0` (`:550`), then requires stdout to be exactly ONE
  JSON line (`:551-553`, "stdout is not a single JSON line").
- `:652-656` — the ONLY content assertion is `arm.parsed[counter.countField] !== expected` →
  `countNotReproduced`. Every other JSON field the counter prints is never compared; the
  manifest records counts, not the transcript.
Counter bytes themselves are pinned (sha256 at measured and target revs, `:580-595`; worktree
bytes refused unless they equal the recorded blob, `:623-632`), so this is projection-narrowing
over a byte-pinned instrument — fail-closed on the counter, blind on its output fields.

### BOUND-4 — game-dev-2d `corpus/fixtures/run_battery.py`: exit + signature substring (+ banned markers)
- `game-dev-2d-shokunin/corpus/fixtures/run_battery.py:2607-2608` — `classify_process` returns
  `code == expected_exit and error is None and signature in output and not unrelated_errors and
  "SCRIPT ERROR:" not in output and "Parse Error:" not in output`; `classify_streams`
  (`:2610-2616`) additionally requires the signature on stdout and pins allowed stderr lines.
  Whole-stdout equality is never asserted; the pin is a substring predicate.
- The gate DOCUMENTS its own blindness at `:1896-1902`: "the verdict-level pin is a substring
  predicate (`signature in output`), so a foreign line appended before/inside/after the pinned
  span, or an extra PASS-line, is invisible at the verdict layer (r100-critic F1 family)" — and
  compensates with the receipt-shape META gate (`:2046` anchors = each signature's first line;
  PASS-line grammar floor `:1993-1996`) evaluated over the stored per-row stdout records.
- Single-lane: no `run_battery.py` exists in audio-shokunin or game-dev-3d (fixtures dirs
  listed; their probes are per-case test_*.py / .c / .gd files).

All four are documented, fail-closed-in-their-declared-direction design bounds — no sibling
claim is false today because of them; each narrows WHICH bytes of a transcript carry the
verdict, which is exactly the axis tameshi's round-35 fix 2 widened for its own oracle.

## 3. What I could NOT break (the class is already closed in these lanes — proof pointers)

- `kama-shokunin/tools/instrument-agreement.py:25-26` — "A run's digest =
  sha256(exit code, 0x00, normalized stdout, 0x00, normalized stderr)"; computed at `:64-66`
  over the FULL captured streams with only declared volatile-field normalization; agreement =
  all runs share the digest (`:74-75`). Whole-transcript, both streams, exit included.
- `kake-shokunin/scripts/receipt_replay.py` — C2 re-runs the revision's validator and compares
  `{"exit": done.returncode, "result": <full parsed stdout>}` (`:515-524`) against the recorded
  `audit.json` with deep equality `same_json` (`:465-466`, recursion `:135-139`). Full
  transcript + exit.
- `chousa-shokunin/tools/research-gate.sh` `--pin`/`--drift` — "re-runs the same invocation,
  normalizes with the CURRENT rules and byte-compares against the baseline body" (`:231-236`,
  usage `:550-553`). Whole-capture byte compare with an explicit declared volatile contract.
- `kotoba-shokunin/verifiers/compare_harness_independent.py` — joins BOTH instruments' whole
  payloads; every published channel parsed and cross-checked, divergent/shadowed values are
  loud errors (`:29-38`, compare `:709-730`); duplicate/shadow keys fail closed.
- `mado-shokunin/tools/mado-verify.sh` `--regression` — replays a recorded mutation verdict
  TABLE (measured vs recorded per-row verdicts, control line, restore proof; selftest arms
  R1-R9 at `:517-597`), not a single-line projection.
- `tsukuroi-shokunin/tools/run-receipt.py:106-114` — receipts capture the tool's FULL stdout
  lines + exit + timed_out + stderr tail, so downstream readers are not record-side blinded
  (`check-report-receipts.py` asserts citation/anchoring, not output equality).
- Display-only truncations are NOT assertions: kumitate `round-gate.mjs`'s `firstLine()` helper
  (`:218-220`) appears only in `detail:`/error strings — zero hits for `ok:.*firstLine` across
  `scripts/*.mjs`; the `split('\n')[0]` hits in `bind-oracle.mjs:128`, `cite-check.mjs:2360`
  etc. are all detail strings. The residual `head -1` uses in mori/kengaku/souji tools are
  single-value producers (git rev-parse output, a sha256 field, a shebang, `.git` gitdir line),
  not transcript comparisons.

## 4. HYGIENE (tameshi-side, observed while grounding the closure claim — free, no action beyond disclosure)

`tools/tally-audit-v3.py:77` — the docstring's `Checks: runtime` summary still reads "Exact
stdout first line and exit code compared", contradicting fix 2 in the same docstring
(`:19-22`) and the code (`:385`, `:392-402`, which compares the FULL stdout under every
config). Doc-only; the counters and the oracle are unaffected. The frozen-artifact pin means
this cannot be edited this round — record it for the round-36 tool successor's docstring
(keep the `Checks` list in lockstep with the fixes list).

## 5. P-set decision: `corpus/knowledge/verification-patterns-fleet.md` needs a BOUND on P3, not a new pattern row

P3 (`:32-35`) currently claims "Byte-identity / exact-id equality is the top verdict class;
volatile fields are scrubbed by an explicit list". The scan shows the precise fleet fact P3
misses: identity is asserted over a LANE-CHOSEN PROJECTION of the transcript (last line / final
summary line / one count field / signature substring), and whole-transcript equality is the
closure class, now evidenced in ≥2 independent lanes. The census's own generality bar
("`a pattern is called general only with evidence from two independent lanes`",
`verification-patterns-fleet.md:16`, quoting PROVINCE.md:15-16) is met by BOTH halves:

- projection-narrowing: kagi (BOUND-1), kumitate (BOUND-2), tabi (BOUND-3), game-dev-2d
  (BOUND-4) — four lanes;
- whole-transcript closure: tameshi r35 fix 2 (`tally-audit-v3.py:19-22,385-402`), kama
  (`instrument-agreement.py:25-26`), kake (`receipt_replay.py:465,524,135-139`), chousa
  (`research-gate.sh:231-236`) — four lanes.

Why a bound and not a new P11: P3 already owns identity-verdict semantics, so a new row would
fragment that scope; the game lane's machinery-level statement already lives in the D-block
(D4 spoof resistance, D7 field-tuple fence), and the g2d citation belongs there. The bound is
the minimal append that makes P3's claim safe to reuse.

### Proposed move (one bounded proposal; corpus-owner/L1 to land — this seat writes only this report)

Append an errata-style block to `corpus/knowledge/verification-patterns-fleet.md` (append-only,
same convention as the round-2/round-4 Errata blocks; nothing above it rewritten):

> **P3 bound (round 35, 2026-10-23; routed from tameshi r35 w2 ConnectorFirstLine).** P3's
> byte-identity holds at the verdict layer only over a lane-chosen PROJECTION of the
> transcript, and lanes differ in which bytes carry the verdict: kagi claim-ledger
> `verify`/`cells` = exit equality + ERE on the LAST non-empty output line, stderr merged
> (`kagi-shokunin/corpus/claim-ledger.sh:593-595,612-614,616,621-623`; rationale :26-30);
> kumitate counter reproduction = exit + byte-equality of the FINAL summary line only
> (`kumitate-shokunin/scripts/counter-rerun.mjs:129-138,220-226`; claim boundary :36-42);
> tabi measurement reproduction = exit 0 + one count field of a one-line JSON stdout
> (`tabi-shokunin/scripts/check-measurement-binding.mjs:546-553,652-656`); game-dev-2d battery
> = exit + signature substring with banned-marker screens (`game-dev-2d-shokunin/corpus/
> fixtures/run_battery.py:2607-2616`), self-documented at :1896-1902 with the receipt-shape
> META gate (:2046) as compensation. Whole-transcript equality is the closure class: tameshi
> r35 fix 2 (`tools/tally-audit-v3.py:19-22,385-402`, full stdout × all four (auto,KEEP)
> triples, stderr excluded by r32 rule :64), kama digest over (exit, full stdout, full stderr)
> (`tools/instrument-agreement.py:25-26,64-66`), kake deep-JSON equality of {exit, full parsed
> stdout} (`scripts/receipt_replay.py:465,524,135-139`), chousa whole-capture byte-compare
> (`tools/research-gate.sh:231-236`). RULE a lane that narrows the compared projection must
> either document the boundary in the gate's own contract (kagi :26-30, kumitate :32-42, g2d
> :1896-1902) or compensate with a shape-meta gate over the stored records (g2d :2046); a
> projection-narrowing with neither is a P3 violation. Line anchors are as of 2026-10-23; cite
> gate+function if lines drift (V-R4-2 precedent).

This is NOT a round-35 contract amendment (kill_rule: no post-data rule change) — it is a
corpus-knowledge append for the corpus owner / round-36; no counter, frozen artifact, or
measurement surface is touched.

**Affected axes:** adjacency (primary — a routed, two-lane-evidenced fleet pattern refinement
carrying tameshi's closure to the sibling lanes that still narrow the projection); depth
(secondary — names whole-transcript equality as the fleet standard the r35 fix instantiated).
No harm: calibration/freshness/operability untouched (no records rewritten, append-only),
C1/C2 measurement surfaces untouched.

**Risks:** (i) the census file is append-only — the bound must land as an appended block
citing this round, never a rewrite of P3's body (Errata convention :200-206); (ii) BOUND-1/2/4
are documented design bounds with declared rationale — the row records the projection and its
rationale, it must not be read as flagging those lanes' claims false; (iii) line-anchor drift
(the file's own V-R4-2/V-R4-3 history) — mitigated by naming gate+function beside every
path:line; (iv) two-lane rule is satisfied with margin (4+4 lanes), so the generality claim is
safe against single-lane revision.

**Verification for the owner/L1 after landing:** every path:line above re-resolves on the
current sibling trees; `grep -c "P3 bound" corpus/knowledge/verification-patterns-fleet.md`
→ 1; the bytes above the appended block hash-identical to pre-append (same proof shape as the
TAMESHI-R2-4 lane-end note at :198); `git -C tameshi-shokunin status --porcelain` shows only
the intended writes.

## 6. Bounds honored / installs

Cross-lane scan read-only; the only lane write is this report. Scratch: the lane clone under
`/fast/scratch/hyaku/tameshi-r35-seats/ConnectorFirstLine/` (fetch-into-clone only; origin
worktree untouched). No tool installs or upgrades needed this seat (recorded per the operator
2026-10-19 directive: none). No `pacman`. Depth 3 leaf: no subagents, no labrat probe (not in
this seat's item).
