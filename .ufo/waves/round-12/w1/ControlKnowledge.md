# ControlKnowledge — round 12, wave 1 (C1 knowledge note)

Seat: leaf executor (ControlKnowledge). Assigned write: the C1 knowledge note
only. Advisory lane-internal report — **NOT independent non-author
promotion/admission**. No gate was run by this seat; no production code, no
registry/scorecard/lesson file, and no sibling gate was written or touched.

## 1. Files written (exact owned paths)

| Path | Status | Bytes |
|---|---|---|
| `corpus/knowledge/repeated-control-precondition.md` | new | 13,041 |
| `.ufo/evidence/round-12/ControlKnowledge/README.md` | new | 2,943 |
| `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv` | new | 3,972 |
| `.ufo/waves/round-12/w1/ControlKnowledge.md` | new (this report) | — |

Full fetched bodies are scratch (`/tmp/tameshi-r12-ck/fetch/`), not committed,
per the wave's evidence rule; the digests below pin them.

## 2. Sources re-opened (source / verified-at / recheck trio)

Both re-opened 2026-10-20T02:13:47Z with `curl -fsSL` (observed host date
2026-10-20, not the dispatch prompt's calendar date):

| id | URL | accessed (UTC) | bytes | sha256 (fetched body) |
|---|---|---|---|---|
| S004 | https://mutants.rs/using-results.html | 2026-10-20T02:13:47Z | 29,579 | `5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334` |
| S026 | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | 2026-10-20T02:13:47Z | 236,385 | `ca1145fbe56de30b43b66baf7372206a38abe08a55b3db13f6c7a0114d7a6c8c` |

Recheck commands, **ran** 2026-10-20T02:17:02Z:

```
curl -fsSL https://mutants.rs/using-results.html | grep -c 'passes reliably when copied to a temporary directory'   → 1
curl -fsSL https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | grep -c 'hardly a perfect solution'   → 2
```

S026's page serves its post body **twice** (`text/template` copy at
`S026.html:1095-1102`, `<noscript>` copy at `:1124-1137`), so the healthy count
is 2, not 1 — 0 is drift. This is recorded in the note's `recheck:` line and in
the evidence README.

## 3. Located quotes (≤25 words) — for the round gate table

The lesson draft's gate table (`corpus/lessons/round-12.md:11`, S026 row)
currently records "Opened by L1; reader omitted the article body. No article
quotation is credited from that partial view." This seat read the body; the
following quotes are located and may be folded in:

- **S004** — https://mutants.rs/using-results.html — accessed 2026-10-20 —
  §Tests fail in an clean tree?, `S004.html:187` (23 words):
  > Fix this first: cargo-mutants can’t do anything until you have a tree where cargo test passes reliably when copied to a temporary directory.

- **S026** — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html — accessed 2026-10-20 — post body (John Micco, 2016-05-27), `S026.html:1130` (21 words):
  > We define a "flaky" test result as a test that exhibits both a passing and a failing result with the same code.

- **S026** (retry clause, 24 words), `S026.html:1136`:
  > This reduces false positives, but encourages developers to ignore flakiness in their own tests unless their tests start failing 3 times in a row

Ten further located excerpts with line anchors are in
`.ufo/evidence/round-12/ControlKnowledge/quotes.tsv` (Q1–Q10).

## 4. Behavior documented in the note (contract, not measurement)

[O] At this write (2026-10-20T02:14Z, rev `18ad5d0`) `tools/repeat-control.py`
is **not in the tree** (`ls tools/` → `mutate-and-run.sh` only). The note
therefore documents the assigned interface as contract only — it claims no
runtime check — and routes run evidence to §5 of the note:

- `python3 tools/repeat-control.py --runs N --out DIR -- COMMAND ARG...`; exact
  argv, stdin `/dev/null`, numbered stdout/stderr + exit per run, **no byte
  normalization**.
- Findings/exits: `controls_match` 0 clean · `controls_mismatch` 1 failed ·
  `baseline_nonzero` 2 could-not-evaluate · `command_unavailable` 2
  could-not-evaluate · invalid usage 64 could-not-evaluate · `--snapshot DIR`
  tamper → 2 `snapshot_tampered`. `--selftest` must emit exactly these on
  isolated fixtures. The mutation runner is not edited (pin verified
  `75ed934d…`, six legs `tools/mutate-and-run.sh:84-89`).

The sourced distinction the note lands (F3):

- Byte-stream agreement is a **stronger requirement than pass/fail stability**
  — identical stdout/stderr plus identical exit — and both describe only the
  runs actually taken; determinism across all runs stays unestablished, so
  `controls_match` is stability evidence, never a determinism proof.
- **No retry repairs**: S026's own verdict on its retry / fail-3-in-a-row
  family is "reduces false positives … hardly a perfect solution" (and delays
  detection: 45 minutes for a 15-minute test). The gate therefore must not
  retry a mismatch into a match; a mismatch is the finding.
- Unusable baseline ⇒ no verdict: S004's "Fix this first … passes reliably" and
  its `unviable` = "inconclusive about test coverage" match the exit-2
  could-not-evaluate classes and the lane's existing red-control rule
  (`SKILL.md:148-149`). `baseline_nonzero` covers only identical nonzero
  tuples; differing tuples are `controls_mismatch` first. `--snapshot` only
  validates saved observations and never executes the recorded argv.

## 5. Risks / limits (named, not smoothed)

1. **Unnormalized bytes vs volatile output** — a gate whose selftest prints
   durations/timestamps would report `controls_mismatch` on an honest repeat.
   Unmeasured for all six recorded gates; the gate's first real run resolves it
   per gate.
2. **Contract presumes a zero-exit control** — a gate whose healthy control
   exits nonzero by design lands in `baseline_nonzero`
   (could-not-evaluate). Honest but limiting; named in the note as a contract
   limit, not a defect.
3. **Line anchors are revision-bound** — S026's duplicate body copy means a
   template change moves `:1095-1102` without moving `:1124-1137`; quotes.tsv
   records both locations.
4. **Sibling registry flip is already in the worktree** — `corpus/SOURCES.md`
   is modified: S004 `used-by` (`:15`) and S026 `mined` + `used-by` (`:37`)
   now point at this note, which did not exist when the flip was drafted
   (flagged premature in `.ufo/evidence/round-12/LessonScribe/outline.md:72`).
   It is consistent now that the file exists; if L1 drops the file, those
   `used-by` paths dangle and the contract census `missing:` check fails.
5. **Coverage-map row still missing** — `corpus/README.md` is unmodified
   (`git status --porcelain corpus/README.md` → empty at 2026-10-20T02:20Z);
   `QUALITY.md` 7 debt, owner L1 integration / registry scribe.
6. **Contract transcription risk** — the §3 block in the note is transcribed
   from the dispatch/spec; if the landed gate differs in flag names, the
   baseline rule or snapshot exit semantics, the note must be corrected at
   integration against the gate's own contract text.

## 6. Blockers

None. No gate run was attempted (out of this seat's scope); nothing in the
assignment was left unreachable.

## 7. Tooling

No tool installed, upgraded or invoked beyond `curl`, `grep`, `sha256sum` and
the repo's own file tools. No package-manager calls, so no version/channel
record is owed.

## 8. Revision (L1 request, 2026-10-20)

The note was trimmed from 237 to 60 lines at L1's request: the corpus-rate
hypothetical arithmetic and the flakiness-negation framing were removed in
favour of stream-agreement-is-stronger-than-pass/fail-stability language; the
draft/gate-absent/pending/debt sections were replaced with the §5 evidence
line ("Runtime receipts live under `.ufo/evidence/round-12/`; the round-12
lesson distinguishes run evidence from source facts"); the gate section now
states that `baseline_nonzero` covers only identical nonzero tuples (differing
tuples are `controls_mismatch` first), that `--snapshot` validates saved
observations only and never executes the recorded argv, and that there is no
timeout semantics, the run count is caller-supplied, and neither N=3 nor the
byte policy is source-prescribed. The source trio and located quotes are
unchanged; no runtime check is claimed.
