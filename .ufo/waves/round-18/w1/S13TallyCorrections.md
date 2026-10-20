# S13TallyCorrections — round-17 lesson wording corrections (R17-CMD-BIND)

Seat: `TameshiR18.S13TallyCorrections` (leaf, no dispatch). Read rev:
`183f87b899e6cae46be98d251cbc87fb5118f6ca`. Scratch:
`/tmp/tameshi-r18w1-S13TallyCorrections-TwKfMv` (fleet-mirror clone, every run
under `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`
with cwd inside the clone; no git write outside it). Tool installs: none.
No lane file was edited by this seat.

Target: verify the spot-check's two wording defects in
`corpus/lessons/round-17.md` and supply append-only correction text.

## 1. Defect (a) — G7's K02 pointer is wrong: hole 5 → hole 7

`git show 183f87b:corpus/lessons/round-17.md | nl -ba` → line 24 (verbatim):

```
| G7 | including every seat-opened file (SKILL.md, the ledger) as an input | reject | K02 hole 5: one edit would uncredit the whole page; the bucket is keyed by its own section sha already |
```

Hole numbering in `.ufo/waves/round-17/w1/K02InputCreditHoles.md` (ranked table):

- `:28` — **hole 5**: "Reads of the live lane from a \"clone\" run" (false provenance; live-lane reads are `external`/`.git`, so they cannot uncredit). Unrelated to G7.
- `:30` — **hole 7**: "Over-invalidation by the page itself (and by the ledger and SHONEN)"; the row's demo is exactly "with SKILL.md: 0/54, `input-drift:SKILL.md`". This is the reasoning G7 quotes.
- `:47` — smallest correction 5: "Exclude the page and the ledger from seat-opened inputs."

Corroborating records already committed (no new judgment needed):

- `.ufo/waves/round-17/w2/LessonReview.md:111-119` — F4: "Lesson `:24` (G7, reject) says 'K02 hole 5' … the quoted reasoning is **hole 7**"; substance holds because `IGNORED_INPUTS = frozenset(('SKILL.md', DEFAULT_LEDGER_PATH))`.
- `corpus/lessons/round-17-verifier-spotcheck.md:327` — "Lesson's pointer to K02 hole 5 is wrong: that hole is about live-lane reads; the cited reasoning is hole 7."
- `corpus/lessons/round-17-verifier-spotcheck.md:423-427` (§7.2) — requires "a named correction, not historical evidence rewrites."

Substance anchor at final bytes: `.ufo/evidence/round-17/measure.py:132`
(`IGNORED_INPUTS = frozenset(('SKILL.md', DEFAULT_LEDGER_PATH))`; blob sha256
`d25d3d04cb26ca7c20ef7333baaa181c350c6ee912d58f648927fb835b3ce7f3` at
`e3827ee`, `30b0ca8`, `183f87b`).

**Finding: defect (a) holds.** The candidate and its reasoning stand; only the
hole number is wrong.

## 2. Defect (b) — G5's "(89/89 selftest)" is the wave-1 tally; final is 94/94

`corpus/lessons/round-17.md:22` (verbatim):

```
| G5 | input-keyed credit with class-independent gate, trace binding, veto aggregation | admit | K02 holes 1–4 and R05 F1–F3 closed in `measure.py` (89/89 selftest); red-before on real bytes (credited at `e69b488`, `input-drift` at `09ee1d0`) |
```

Where **89** is recorded (wave 1 → wave-2 no-harm rerun at the same bytes):

| Source | Observation |
|---|---|
| `.ufo/evidence/round-17/registry-full-2a22ade.json`, row `measure-round17-selftest` (`argv: python3 .ufo/evidence/round-17/measure.py --selftest`) | got 0 / expect 0 / held true; `stdout_tail` ends `MEASURE_SELFTEST: 89/89 pass (scratch /tmp/tameshi-r17-MeasureV2-e_orm2vx)` |
| `.ufo/evidence/round-17/registry-full-eb7838b.json`, same row (receipt rev `eb7838b`, exit 0, 28/28) | same tail: `MEASURE_SELFTEST: 89/89 pass` |
| `.ufo/waves/round-17/w2/NoHarmSelftests.md:57` | "`MEASURE_SELFTEST: 89/89 pass`" for the same row at `eb7838b` (baseline tool sha `f348adc3d88a…`, `:80`) |

Where **94** is recorded (final):

| Source | Observation |
|---|---|
| `.ufo/evidence/round-17/registry-full-e3827ee.json` (`rev: e3827ee67d58673e1e9a1141ba1c8333125f4de8`, `rev_resolved: e3827ee67d58`, exit 0, 28/28 held), row `measure-round17-selftest` | got 0 / expect 0 / held true; `stdout_tail` ends `MEASURE_SELFTEST: 94/94 pass (scratch /tmp/tameshi-r17-MeasureV2-5jl1pvgs)` |
| same receipt, measured `measure.py` | sha256 `d25d3d04cb26…`; the spot-check pairs 94/94 with prefix `d25d3d04` (`round-17-verifier-spotcheck.md:306`) |
| `round-17-verifier-spotcheck.md:310-313` | "Its earlier measure tally is 89, not the final 94; those are versioned receipts, not interchangeable counts." |
| `.ufo/waves/round-17/w3/RR7.md:17,52`; `w3/RR8.md:27` | independent 94/94 runs on the later bytes |

Execution ladder on committed bytes (observed this seat; clone at each rev,
`measure.py --selftest`, all exits 0):

| rev | SELFTEST line |
|---|---|
| `2a22ade` (wave-1 build landing) | `MEASURE_SELFTEST: 89/89 pass` |
| `fad9e95` (wave-2 landing) | `MEASURE_SELFTEST: 93/93 pass` |
| `0ff2734` (live-lane binding) | `MEASURE_SELFTEST: 94/94 pass` |
| `183f87b` (lane tip, this read rev) | `MEASURE_SELFTEST: 94/94 pass` |

So 89/89 was true when the G5 row was written (and at the wave-2 no-harm
rerun); the round's final committed receipt and current bytes say 94/94.
`corpus/lessons/round-17.md` never records 94.

**Finding: defect (b) holds** — a dated tally presented as the round's current
one; the correction is a tally note, not a rewrite of the admission.

## 3. Guard rail for the corrective sweep

`corpus/lessons/round-17.md:57` also contains "89/95" — that is the
`tools/mutate-and-run.sh` canary-mutant count (scrub-removed mutant 89/95,
landed 95/95), a different instrument and must not be swept. A blob-wide grep
at `183f87b` shows `89/89` only at `corpus/lessons/round-17.md:22`, and `94/94`
only at `corpus/lessons/round-17-verifier-spotcheck.md:306`.

## 4. Proposed append-only correction (drop-in)

Placement: append at end of `corpus/lessons/round-17.md` after line 96 (the
file currently ends there — `wc -l` = 96; no `## Errata` section exists).
Lines 22 and 24 stay byte-identical (`corpus/QUALITY.md:7`).

````markdown
## Errata (append-only)

Entries go below this line; nothing above is edited (`corpus/QUALITY.md:7`).

### ER-r17-1 — G7's K02 hole pointer (:24): hole 5 is hole 7 (2026-10-20)

Line 24 (G7, reject) cites "K02 hole 5". The pointer is wrong; the quoted
reasoning — one edit uncredits the whole page, the bucket is keyed by its own
section sha — is **K02 hole 7**, "Over-invalidation by the page itself (and by
the ledger and SHONEN)" (`.ufo/waves/round-17/w1/K02InputCreditHoles.md:30`;
smallest correction 5 at `:47`). K02 hole 5 (`:28`) is the unrelated live-lane-
read hole. The rejected candidate and its reasoning stand: `IGNORED_INPUTS =
frozenset(('SKILL.md', DEFAULT_LEDGER_PATH))`
(`.ufo/evidence/round-17/measure.py:132` at `30b0ca8`). Recorded by W2
`LessonReview.md:111-119` (F4) and confirmed by
`round-17-verifier-spotcheck.md` §5 (`:327`).

### ER-r17-2 — G5's selftest tally (:22) is the wave-1 count; final is 94/94 (2026-10-20)

Line 22 (G5, admit) records "(89/89 selftest)". That is the wave-1 build
receipt: `registry-full-2a22ade.json` and `registry-full-eb7838b.json`, row
`measure-round17-selftest`, print `MEASURE_SELFTEST: 89/89 pass`, and W2
NoHarmSelftests re-ran the same bytes at `eb7838b` and recorded 89/89
(`.ufo/waves/round-17/w2/NoHarmSelftests.md:57`). Wave-2 hardening raised the
count; the final full receipt `registry-full-e3827ee.json` (rev `e3827ee`,
exit 0, 28/28 rows held) records `MEASURE_SELFTEST: 94/94 pass` for `measure.py`
sha256 `d25d3d04…`, still the blob at `30b0ca8` and `183f87b`. The counts are
versioned receipts, not interchangeable
(`round-17-verifier-spotcheck.md:310-313`). This corrects the tally only; the
separate breadth of G5's "K02 holes 1–4 closed" remains routed as R17-CMD-BIND
(`round-17-verifier-spotcheck.md` §5, §7.2).
````

## 5. Residual and inference

- [OBS] The intermediate 93/93 at `fad9e95` exists only as my clone execution
  (no committed registry receipt; `.ufo/waves/round-17/w1/X07MeasureV2.md:252`
  records an in-flight 93/93). The proposed errata deliberately omit it so
  every sentence in the correction has a committed anchor.
- [INF] The 4→1 case growth between `fad9e95` and `0ff2734` is inferred from
  the counts; no case-name diff was taken here.
- Whether the L1 mirrors the same two entries into `round-18.md` is a routing
  choice, not a finding. The correction does not discharge the command-binding
  half of R17-CMD-BIND (spot-check §5, §7.2).
- No harness install was needed; no lane bytes were written by this seat.

Verdict: **holds** — both wording defects confirmed at `round-17.md:24` and
`:22`, with 89 anchored in `w2/NoHarmSelftests.md:57` plus the two early
registry receipts and 94 in `registry-full-e3827ee.json`; append-only erratum
text supplied above.
