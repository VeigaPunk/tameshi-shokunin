# V03 — origin of the sha-only cold-read credit (round 16)

Scope: how the round-16 cold-read credit rule became sha-only, and whether input
drift was considered and dropped. Read at lane tip `98bea7d` (branch master);
round-16 bytes read at `c699c8c`, `05a2247`, `3490708`, `09ee1d0`, `017a2b0`.
Executions in `/tmp/tameshi-r17w1-V03ShaOnlyOrigin-smJ8YL` (clone). No installs,
no lane writes besides this report.

**One-line answer: the rule was born sha-only and never carried an input
dimension. External input drift was named exactly once, in wave 2
(CalibCritic, with RR10's exit-2 witness already in hand), then neither adopted
nor recorded as debt. So it was silently dropped, not weighed and rejected.
Lesson class: `credit-drift`.**

## 1. Instrument lineage (`git log -p -- .ufo/evidence/round-16/measure.py`)

`git log --format='%h %cI %s' -- .ufo/evidence/round-16/measure.py` returns
exactly two commits; `git log -p … | wc -l` = 734.

| Commit | Time (-03) | Change | Credit-relevant |
|---|---|---|---|
| `c699c8c` | 10:49:37 | measure.py created (596 lines) | **rule born here**: sha-keyed, class-conditional, command **count** only |
| `05a2247` | 11:18:08 | box-block parsing fix (`shonen_boxes`), depth guardrail, selftest 33/33 → 38/38 | none: `entry_credit_reason` untouched |
| `3490708` | 11:31:50 | `coldread/ledger.json` landed | data, not rule |
| `09ee1d0` | 11:46:02 | errata re-read folded into the ledger | data; the **measured** commit for C2 |
| `017a2b0` | 11:47:11 | round-16 lesson records the measured claims | claim text |

The credit predicate exists once, at creation, and was never extended. Round
15's `measure.py` (`.ufo/evidence/round-15/measure.py` at `0494c24`) has zero
`coldread`/`box3`/`ledger.json` hits — it counted context-gate claims, not
cold reads. Nothing was dropped from a predecessor design: the cold-read credit
was sha-keyed from its first line.

## 2. What the rule keyed on, and what it discarded

**Report schema v1** (`spec1.json` `context` → `# Interfaces` bullet 1;
identical in `spec2.json`'s `# Cold-read interface`). Required fields:
`seat`, `skill_sha256`, `sections[]` with `start`, `heading`, `class`,
`verdict`, `blocking_gaps`, `wrong_expectations`, `minor_gaps`,
`commands_executed`, `opened`, `scratch`. The context also says: *"List every
opened path in `opened`."* There is **no** `read_rev` and no per-input digest.
The report schema already collected a path-level record of what the seat
opened; the ledger design then dropped it (below).

**Ledger schema v1** (`spec1.json` `context` → `# Interfaces` bullet 3):
entry = `skill_sha256`, `start`, `end`, `heading`, `sha256` (section text),
`class`, `verdict`, `blocking_gaps:int`, `wrong_expectations:int`, `seats`,
`reports`. No `commands_executed` list, no `opened`, no `inputs`, no `read_rev`.
The implemented entry adds `minor_gaps` and `commands_executed_count` (plus
`positions` when a section sha occurs in more than one skill file) — and no
input identity.

Evidence:

- `.ufo/waves/round-16/w1/CRLedger.md:20` — *"Entries keyed by **section
  sha256** (L1 decision 2)"*; `:33` — *"`blocking_gaps`,
  `wrong_expectations`, `minor_gaps`, `commands_executed_count` are sums of the
  seat lists' lengths"*.
- `.ufo/evidence/round-16/coldread/assemble.py:214` — validates `opened` as a
  list; `:409-411` — entry construction keeps only
  `commands_executed_count = sum(len(o["commands_executed"]))`. `opened` is
  validated and then discarded.
- `.ufo/evidence/round-16/coldread/ledger.json`, entry `start=1563` (the
  round-14 recipe bucket): fields are
  `{skill_sha256, start, end, heading, sha256, class, verdict, blocking_gaps,
  wrong_expectations, minor_gaps, commands_executed_count, seats, reports,
  positions}`; `commands_executed_count: 4`, `seats: ["CR26"]`. No input
  identity.
- `.ufo/waves/round-16/w1/CRMeasure.md:24-32` — *"Credit rule per L1
  decision (2)"*: instruction credits on `executed-ok|gap-minor` **with
  `commands_executed_count>0`**; record credits on `verified-record|gap-minor`.
- `measure.py` at `09ee1d0`, `entry_credit_reason()` `:178-215`, section match
  by sha at `:245-252`. Grep over the landed blob for
  `\binputs\b|read_rev|'opened'`: **zero** hits. `box3_full_page` is the
  docstring's "every section's sha256 is covered by a ledger entry credited per
  the L1 rule" (`:18-24`). Its selftest at the same rev
  (`python3 .ufo/evidence/round-16/measure.py --selftest`) → exit 0,
  `MEASURE_SELFTEST: 38/38 pass`; no case names an input path or a rev.

Two origins deserve separation:

1. The w1 **task prompt** (`spec1.json` `items[47].prompt`, CRMeasure) asked
   for a simpler, class-blind rule: sha match + verdict in
   `{executed-ok, verified-record, gap-minor}` + `blocking_gaps==0` +
   `wrong_expectations==0`. That rule had *no* execution evidence at all.
2. The **shipped rule is stricter**, adding the instruction/record split and
   the `commands_executed_count>0` gate. CRMeasure attributes it to "L1
   decision (2)"; the exact decision text is not committed. The class split
   matches CRCritic1's `w1/CRCritic1.md:116-128` finding (the record/instruction
   loophole) — causality is [INFERENCE], the content match is observed.

The net addition over the prompt was a **count of declared commands**. It
records that something ran, never what it ran against. That is the sha-only
shape: identity = section bytes; execution currency = a count.

## 3. The drift, reproduced end to end

Commands run in the /tmp clone; exits quoted.

```
git show <rev>:tools/mutate-and-run.sh | sha256sum
  28aeef4  75ed934dc863…   (the round-13 pin)
  c699c8c  89722ddb3082…
  05a2247  0673d2e5374b…
  09ee1d0  0673d2e5374b…
  017a2b0  0673d2e5374b…
git show 28aeef4:.ufo/evidence/round-13/expected.json → inputs["tools/mutate-and-run.sh"] = 75ed934d…adc5
```

At `28aeef4` (SKILL.md sha `97cf436b` = the round-16 snapshot):

```
python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-14/dispositions.json --json
→ exit 0; status=clean; effective=11, superseded=1, failed=0
```

This is the outcome CR26 recorded at `.ufo/waves/round-16/w1/CR26.md:27-28`
(step 3 = exit 0 clean). Because the gate verifies every pinned input digest
before any predicate runs, CR26's exit 0 is itself proof that the runner bytes
matched the pin at read time.

At the measured commit `09ee1d0`, same command, same section bytes:

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
→ exit 2; id=expected_input_digest_mismatch;
  "tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…"
python3 … --dispositions .ufo/evidence/round-14/dispositions-before.json --json
→ exit 2; id=expected_input_digest_mismatch
```

And the counter at `09ee1d0`:

```
python3 .ufo/evidence/round-16/measure.py --rev HEAD
→ exit 0; calibration_restraint_score 8; coldread 54/54; box3_full_page true
```

(The committed `.ufo/evidence/round-16/measure-09ee1d0.json` agrees.)
The bucket's section sha is byte-identical in all four page versions the ledger
knows: `ledger.json` entry `start=1563` carries `positions` at
`97cf436b/3d8a1edb/e289acec/906fb649`, all `1563-1596`, sha `e8720037…`.

So the counter credits a bucket whose recipe step 3 is **false** at the
measured rev, because the section text never changed while the input it
executes moved. The observed contradiction is structural, not a measurement
error: the credit key (section bytes) is orthogonal to the dependency (input
bytes).

## 4. Was input drift considered and dropped?

### (a) Wave 1 — page-internal drift was considered; external input drift was not

`w1/CRCritic2.md` scoped itself to "the sha-matching rule" and named its
weaknesses (`:169-175`):

- **F11 (`:122`)** — *"The sha rule keeps credit for sections whose line
  anchors went stale."* Simulation: a 2-line insertion changes 1 section sha
  and leaves 50 credited, while 10 of 12 self-anchors point at the wrong text.
- **F12** — append-only errata can never clear a gap under the sha rule.
- `:174` — matching on section sha alone ignores `skill_sha256`/`start`/
  `heading`.
- `:175` — *"No proof of what a seat read."* It proposed requiring each seat to
  report the section sha it computed.

Every one of these is **drift inside the page** (self-anchors, appended
sections) or trust in the seat's declared reads. None names the tool/input
revision axis. The lane did act on F11: `coldread/anchor-check.py` +
`anchor-check.txt` (22/22 anchors), and the repair discipline kept line counts
unchanged (`corpus/lessons/round-16.md` G9). It built an instrument for the
drift it had named and none for the drift it had not.

### (b) Wave 2 — external input drift named exactly, plus a live witness

- `w2/CalibCritic.md:120`: *"…section hashes alone do not validate
  dependencies: changed pointer targets, **tool revisions**, or cross-section
  context can invalidate a byte-identical section's earlier execution."*
  Condition 4 (`:140`): *"…plus dependency and whole-page coherence checks."*
- `w2/RR10.md:11-13` and `:51-63`: *"the effective expectation disposition gate
  at c699c8c returns exit2 `expected_input_digest_mismatch` because wave-1 …
  edited `tools/mutate-and-run.sh` without re-pinning the round-13
  `expected.inputs` entry"*; remediation shape: re-pin or supersede.
- `w3/RX5.md` row 2 corroborates at `05a2247` (`observed 0673d2e5… expects
  75ed934d…`).

So by the end of wave 2 the lane had both the general statement and the
concrete instance, from three independent seats.

### (c) The integration response — the rule did not change; the concern was not recorded

- `corpus/lessons/round-16.md:23` (G6, **admit**) states the carry-over design
  positively: *"every bucket of the final page (54 at the landing sha) has a
  passing entry at its own section sha. **Unchanged buckets carry wave-1
  entries**; buckets repaired after wave 1 were re-read in wave 2…"* It
  asserts the sha rule's behaviour without addressing its dependency.
- `corpus/lessons/round-16.md:63` files the same event under `reference-drift`
  with an **operability** fix: *"Correct fail-closed behaviour. The registry row
  now names the archived-root invocation (`git archive 28aeef4` → exit 0)."*
  A different remedy for a different axis.
- CalibCritic appears in the lesson only at G12 (`--override` validation), not
  in the Mistakes table and not in the wave-2 defect list (`:67-81`). Its
  condition 4 is neither adopted nor listed as open debt. Process disclosures
  `:92-94` do disclose *"the round's runner edit drifts round 15's retained
  integrity pin"* — but framed as round 15's receipt not being re-claimed
  green, not as cold-read credit. The open-debt list (`:99-104`) names
  environment scrubbing, line anchors and page-named files; input keying is not
  among them.
- The rule's history confirms it: no third commit ever added an input
  dimension. Mechanically, the critic's condition never entered the machine
  path either: `assemble-final.stderr:43` records
  `SKIPPED …/w2/CalibCritic.md: json block lacks 'sections'` — the ledger
  assembler only ingests section-carrying seat reports, so a falsifier's
  dependency condition has no intake channel at all.

### (d) Post-round closure

`corpus/lessons/round-16-verifier-spotcheck.md:94-121` re-derives the bucket
failure independently (same command, same observed mismatch), and `:226-229`
routes **R16-C2b**: *"The cold-read credit is sha-only. Bucket credit must also
be invalidated when a surface the bucket executes changes after its read: for
example, record the input digests each instruction entry ran against and
re-verify them at the measured rev. Show the red-before on the round-14
bucket."* Its §4 G6 row (`:165`) records the disagreement: *"the ledger records
the reads faithfully, but sha-only credit is blind to surface drift."*

**Answer.** For wave 2, "considered and dropped" is literally correct: named
with a precise mechanism and a live exit-2 witness, then absent from the
shipped rule and from the debt ledger. There is no committed artifact in which
L1 weighed input keying and rejected it. The nearest positive records are G6's
carry-over sentence (asserts the behaviour, not a tradeoff) and the
`reference-drift` row (same event, operability remedy). The defect is not a
documented tradeoff; it is an unrecorded omission between a named falsifier and
a landing claim that the counter still scored 8.

## 5. Mistake class for the round-17 lesson

**Proposed class: `credit-drift`** (alternatives if the lane prefers the
`stale-*` family: `stale-credit`; mechanism name: `under-keyed-credit`).

Definition: *a credit predicate keys an accepted outcome to one identity (the
page section's sha256) and carries it across revisions, while the outcome
depends on other measured objects (the bytes of the inputs the instruction
reads) that the key never records; drift in the unkeyed dimension leaves the
counter green.*

Why it is distinct from the existing vocabulary:

| Existing class | What moved | Why this case is different |
|---|---|---|
| `reference-drift` (r13/r14/r16) | the pointer/anchor target | here the pointer did not move; the target's **bytes** did |
| `stale-expectation` (r14) | the recorded expectation | the recorded text stayed true **as text**; its observation stopped reproducing |
| `stale-premise` (r16) | a present-tense statement | no statement is false; the credit predicate is incomplete |
| `vacuous` (r16) | evidence was empty/irrelevant | the evidence was real at read time; the key is missing a dimension |

General form for the lesson: **an evidence key must cover every dimension the
credited outcome depends on.** For an executed instruction that includes the
bytes of every input the execution opened, not only the bytes that named them.
Corollary visible in this case: the protocol *already collected* `opened`; the
ledger's key discarded it (`assemble.py:214` vs `:409-411`). Do not let
evidence die between collection and the credit path.

Ready-to-paste row for `corpus/lessons/round-17.md` `## Mistakes` (shape of
`round-16.md`):

| Class | Evidence pointer | Captured-by | Fix and falsification |
|---|---|---|---|
| credit-drift | `round-16-verifier-spotcheck.md` §2 (`:94-121`) + §6.3 (`:226-229`); reproduced here: same gate command exit 0 at `28aeef4` and exit 2 `expected_input_digest_mismatch` at `09ee1d0`; round-16 `measure.py` still 54/54, score 8; ledger entry `start=1563` has `commands_executed_count:4` and no input identity. Wave-2 consideration: `w2/CalibCritic.md:120,140`; live witness `w2/RR10.md:11-13,51-63`. | CalibCritic condition 4 named it in wave 2 and the round neither adopted it nor recorded it as debt (lesson mentions CalibCritic only at G12); no QUALITY criterion covered key completeness; the non-author closure re-routed it. | Input-keyed credit (round-17 interface C): per-entry `read_rev` + `inputs{path:sha256}`; an entry with `commands_executed_count>0` credits only if every recorded input's blob at the measured rev still hashes to its digest (`inputs-unrecorded` / `input-missing:<path>` / `input-drift:<path>`); external inputs reported, not credited. Red-before: round-14 bucket at `09ee1d0` — v1 8 (54/54) vs input-keyed 6 (53/54, runner recorded `75ed934d…`, measured `0673d2e5…`). Falsification: measure-v2 selftest must uncredit an otherwise-credited bucket on a drifted input and reject `commands>0` with empty `inputs`. |

Process aggravator, if the scribe wants it named: the wave-2 falsifier was
acknowledged only as an override-validation note (G12), so the landing record
has no line saying the dependency condition was deferred. That is a
disposition-record defect, not the same class; fold "record adopted/rejected
falsifier conditions explicitly" into the fix column unless the lane wants a
separate `unrecorded-disposition` class.

## 6. Confidence and limits

- Observed directly: the two-commit history and full source of
  round-16 `measure.py`; the ledger entry fields/positions at `09ee1d0`; runner
  shas at five revs; the round-13 pin; gate exits 0 / 2 / 2; measure 54/54 and
  score 8 at `09ee1d0`; the quoted spec/report/lesson text.
- [INFERENCE]: the exact wording of "L1 decision 2" (not committed; content
  reconstructed from `CRMeasure.md:24-32` + `CRLedger.md:20-34`); causality
  from CRCritic1's loophole finding to the class split; that CR26's run
  preceded the `c699c8c` runner landing (its exit 0 proves the read-time input
  state regardless of wall-clock order).
- Not done: no lane instrument executed in the lane worktree; no `jj`; no
  installs; round-17 instruments were not built or attacked here.

**Verdict: holds — the sha-only rule was born sha-only; wave-2 named input
drift precisely and dropped it unrecorded; lesson class `credit-drift`.**
