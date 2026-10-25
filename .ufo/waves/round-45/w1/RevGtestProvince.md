seat: RevGtestProvince

# Round 45 — per-entry PROVINCE/QUALITY gate for the package's three GoogleTest entries

Item: gate `r8-gtest-order-and-seed.md`, `r8-gtest-primer-independence.md`,
`r8-gtest-generator-contract.md` (in
`/home/vgpk Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/` — exact
paths below) against `PROVINCE.md` (Owns/Refuses/Adjacent) and
`corpus/QUALITY.md` (criteria list), check every quoted sentence against the
committed snapshots `.ufo/evidence/round-45/coverage/sources/googletest-{advanced,primer,testing}.md`,
and flag inference presented as observation. Bounds honored: read-only on lane and
package except this report; scratch in `/tmp/tameshi-r45-RevGtestProvince/`; no
counter executed (only read); no tool installs.

## 0. The province question first: craft or generic test-framework material?

**Decision: verification-fixture craft — for entries 1 and 2 as packaged. Entry 3
as packaged drifts toward generic test-framework material and is refused.**

Deciding PROVINCE lines:

- `PROVINCE.md:3-6` (Domain): "verification-fixture craft — the reusable method of
  honest checks: hermetic suites, mutation testing, fail-closed arms, verdict-line
  discipline, no-permissiveness audits, before/after proof." Entries 1 and 2 bind
  upstream statements to exactly these: entry 1 to F3/F5 (run identity must be
  excluded and published — hermetic-harness discipline), entry 2 to F3/F2 (fixture
  lifecycle as the independence mechanism; ASSERT/EXPECT as a verdict scoped to the
  witness — "verdict-line discipline" verbatim). The framework's statements are
  mined as evidence for the lane's own grounds; nothing of the framework's product
  surface is absorbed.
- `PROVINCE.md` Refuses: "product domains — every lane's gate remains its own …
  Out of province → report, never absorb." Not triggered: no gate code, no product
  clause absorbed; the `Refuses` line's engine-specific nondeterminism clause is
  not triggered either because the entries take GoogleTest's *documented method*,
  not engine behavior. Precedent for external non-fleet method sources: bash manual
  rows S097/S104 and QuickCheck row S120 are already held the same way.
- `corpus/README.md:70-73` (Frontier admission rule): "A ground moves to `held`
  only through an admitted `knowledge/` entry with a `source:` header citing a
  `mined` `SOURCES.md` row." So GoogleTest is admissible *through* rows S256/S257
  and no other way — which is also why entry 3 (source S204, no row declared this
  round) cannot land now.
- Why entry 3 is the generic-material case: its content is a C++ API reference
  table (`docs/reference/testing.md`), its ground F10 never touches a lane gate
  fixture (F10's own next move in `corpus/README.md` remains "no PBT fixture
  method → one generator against a named fixture gate"), and the entry itself
  concedes the relation to held S120 "is not reconciled here"
  (`r8-gtest-generator-contract.md:50-53`). A reference table plus an unreconciled
  mapping is survey material, not craft evidence a gate can be checked against.

## 1. Findings by severity

### HIGH-1 — Entry 1 rests on a false description of the lane's own instrument

`r8-gtest-order-and-seed.md:31-37` (What is inferred): "The lane's instrument
excluded clock stamps and scratch paths from the compared output … and round 7's
receipt recorded the exclusion in its own `normalization` field … `env-diff.py`
excludes the seed-equivalent artefacts but does not write them anywhere a reader
can find them."

The lane's committed instrument does not exclude anything:

```
$ grep -n 'never normalized\|normalization' tools/env-diff.py | head
8:  control must pass; a changed repeated clean tuple is nondeterminism, not
9:  attributable environment sensitivity. Raw streams are hashed, never normalized.
113:        return {"normalization": "none", "profiles": profiles,
```

`tools/env-diff.py:8-9,113`: raw streams hashed, never normalized,
`"normalization": "none"`. The clock/scratch exclusion exists only in un-landed
instrument copies (package row S201: `env-diff-runid.py`, "a copy of the lane's
tools/env-diff.py whose compared output excludes the clock stamp and the scratch
path"), and the package's own later entries say so explicitly:
`r10-measurement-reproduces-tool-unfixed.md:22-24` ("`tools/env-diff.py` still
declaring `"normalization": "none"` with no run-identity exclusion present") and
`r13-f5-run-identity-exclusion-port.md:14-17`. So within the package itself, the
r8 entry contradicts r10/r13: sentence 1 is true only of the round-7 staged copy
but reads as the lane's instrument, and sentence 2 attributes the exclusion to
`env-diff.py` flatly. QUALITY criterion 1/2 (falsifiable, anchored): the claim is
falsifiable and false, and carries no path:line anchor. **Gate condition: at
re-grounding, correct to "the round-7 instrument copy (S201) excluded them; the
committed `tools/env-diff.py` still declares `normalization: none` (line 113)".**
The publish-the-seed improvement inference survives in corrected form.

### HIGH-2 — Entry 3's "observed" table is a paraphrase presented as the upstream table, and miscounts it

`r8-gtest-generator-contract.md:11-25`: "The upstream reference document's
generator table names five generators and states, for each, exactly what it
yields:" followed by a table whose yield column ("a bounded arithmetic sequence",
"the fixed set it is given", "the elements of a container", "the two-element
sequence `{false, true}`", "the cartesian product, as tuples") is none of the
upstream wording. Every string fails to exist in the snapshot:

```
TST :: bounded arithmetic sequence :: 0     TST :: fixed set :: 0
TST :: elements of a container :: 0         TST :: two-element sequence :: 0
TST :: cartesian product :: 0
```

Upstream (`googletest-testing.md:100-113`) says e.g. "`Range(begin, end [, step])`
| Yields values `{begin, begin+step, begin+step+step, ...}`. The values do not
include `end`. `step` defaults to 1." and `Bool()` | "Yields sequence
`{false, true}`." — and the table has **six** rows, not five: `ConvertGenerator<T>(g)`
is a sixth generator the entry omits. Generator names themselves verify
(`grep -cF` = 1 each for Range/Values/ValuesIn/Combine, 3 for Bool). QUALITY
admission bar 2 and 3 (source-anchored, observation/inference separate) and the
round-40 snapshot-quote criterion: an observed table must be verbatim or marked
as paraphrase, and "five generators" is false as stated. **Refuse** (see MEDIUM-2
for the other independent refusal ground).

### MEDIUM-1 — Entry 1 has no counter-reachable located quote (content is verbatim; format is fatal)

All of entry 1's quoted sentences ARE in the snapshot verbatim under whitespace
folding (multi-line wraps): checked `grep -cF` for single-line spans and a
folded check for wrapped spans — all located=True, e.g. "Remember that the test
order is undefined, so your code can't depend on a test" (snapshot line 896),
"This helps to reveal bad dependencies between tests." (line 1977, in the
`--gtest_shuffle` paragraph as the entry claims), "the random seed value, such
that you can reproduce an order-related test failure later" (lines 1980-1982),
`--gtest_random_seed=SEED`. BUT every double-quoted span in the entry crosses a
line break, and the counter's regex cannot match that:

```
QUOTE_RE = re.compile(r'"([^"\n]{10,400})"|“([^”\n]{10,400})”')   # measure.py:38
```

The only single-line quoted spans are ≤ 5 tokens ("Reveal bad dependencies
between tests" = 5 < 6). Simulating `entry_ok` (measure.py:93-112) on the staged
entry: `no located quote`. **Gate condition: re-ground with one single-line
6-25-token double-quoted span from the snapshot** (e.g. the seed sentence, 13
tokens folded). Entry 2 already passes this clause: "succeeds or fails as a
result of other tests" — 9 tokens, located (primer.md:14-16). All of entry 2's
quotes verified verbatim folded, including "GoogleTest always deletes a test
fixture before it creates the next one" (line 251), "does **not** reuse the same
test fixture for multiple tests" (line 252, `grep -cF` = 1), and the full
ASSERT/EXPECT sentence (lines 108-110).

### MEDIUM-2 — Entry 3 refused for this round on two independent grounds

1. No admitted row: the contract's id_map declares exactly staged S202→S256 and
   S203→S257; `guard-map.json` verdict "admitted" covers the collision map with
   `map_floor: S256`, and S204/`docs/reference/testing.md` is in no declared map.
   A third row now would be a post-score population change, forbidden by C1's
   kill rule and not declared by C2.
2. No located quote at all: the entry's only quote-shaped string is the
   single-quoted `'Combine(g1, g2, ..., gN)'` in its recheck line (4 tokens, and
   single quotes are not QUOTE_RE matches anyway) → `no located quote`.
Route: re-submit in a later round with its own guard-admitted row, a verbatim
table, and a 6-25-token quote. Refusal of entry 3 does not endanger C2 (needs
entries ≥ 2 from S256/S257).

### MEDIUM-3 — All three entries as staged fail the C2 counter's provenance clauses (admission condition, not a landing blocker)

`measure.py:40` `MIN_VERIFIED = '2026-10-25'`; all three entries carry
`verified-at: 2026-10-24` (line 3 of each) → `verified-at` refusal
(measure.py:100-102; T3 in the selftest proves 2026-10-24 is refused). Line 1 of
each cites staged ids S202/S203/S204; the guard refuses identity maps, so the
landed entries must cite S256/S257 (S204 has no landed id — see MEDIUM-2). Each
landed entry must additionally be listed in its cited row's used-by cell
(measure.py:105-107) and appear backticked in `corpus/README.md`
(measure.py:129-130, `indexed == entries`). Landing reshape note: the package's
staged rows have a 12-content-cell layout whose cell[6] is a section reference,
not the lane's 11-cell layout (snapshot cell[6], status cell[8], used-by
cell[11]); and only S202 carries the sha256 (`05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2`,
which equals the committed advanced snapshot's hash) — the S203/S204 staged rows
carry no sha256 prefix, so the landed rows must add snapshot path + sha prefix or
`gt_rows` (measure.py:60-75) drops them.

### LOW-1 — Entry 1: interpretation inside "What was observed"

`r8-gtest-order-and-seed.md:24-28`: "**The two facts are the same fact.** The
seed is the run's identity; excluding it … is exactly the discipline the lane
arrived at independently in rounds 6–8…" — that is inference (criterion 3:
observation, inference, unknown stay separate), and it is also the entry's
weakest step generality-wise: one upstream practitioner + the lane; PROVINCE's
own bar for claiming a pattern general is evidence from TWO independent lanes, so
"instance of a settled upstream practice" should stay scoped to "GoogleTest's
design and the lane's independently, not yet a cross-lane pattern."

### LOW-2 — Entry 1's ground line is over-broad

`r8-gtest-order-and-seed.md:5`: "ground: F3 … and F5 …; also F7" — nothing in the
entry touches F7 (incremental re-sweep granularity); the tag carries no anchor
(criterion 2). Drop it at re-grounding.

### LOW-3 — Entry 2: minor placement

`r8-gtest-primer-independence.md:26`: "GoogleTest enforces it structurally" is
inference phrasing inside the observed section (the supporting quote is real:
primer.md:14-17). The git-history and 404 observations (entry lines 7-18) were
re-verified live today (see §2) but are not reproducible from the document
snapshot alone — they are recorded in staged row S203's own cell, which lands
with the row; acceptable, noted for the falsify wave.

## 2. Live grounding performed (2026-10-25, from `/tmp/tameshi-r45-RevGtestProvince/`)

- All three committed snapshots are byte-identical to upstream at the pinned
  commit today:
  `curl -fsSL …/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/{advanced,primer,reference/testing}.md`
  → sha256 `05546ed6…`, `03d756ab…`, `44c56c61…` — equal to
  `sha256sum` of the three committed snapshots.
- Entry 2's dead-target observation re-confirmed:
  `docs/gtest_for_dummies.md` → HTTP 404 at `master`, at `main`, and at the
  pinned commit.
- Entry 2's rename chain re-confirmed via GitHub API:
  `de47b0d30c1d` = 2018-06-11 "Rename \"Primer.md\" to \"primer.md\"…";
  `1f87a0970dc0` = 2015-08-25 "Move everything in googletest into
  googletest/googletest" — matching entry lines 17-18.
- advanced.md→testing.md link claim verified: `reference/testing.md#param-generators`
  links at `googletest-advanced.md:1103,1118,1141`, inside the `## Value-Parameterized
  Tests` section (line 1030) — entry 3's pointer observation is correct even
  though its table is not.

## 3. Verdicts

| entry | source → landed id | verdict | deciding province line / quality criterion |
|---|---|---|---|
| `r8-gtest-order-and-seed.md` | S202 → S256 | **ADMIT, conditional** — craft (F3/F5); conditions: correct env-diff description (HIGH-1), single-line 6-25-token quote (MEDIUM-1), verified-at 2026-10-25, cite S256, used-by, README index, drop F7 tag, move seed-is-identity to inferred | `PROVINCE.md:3-6` Domain; `README.md:70-73`; QUALITY 1, 2, 3, 10 |
| `r8-gtest-primer-independence.md` | S203 → S257 | **ADMIT, conditional** — craft (F3/F2, verdict-line discipline); conditions: verified-at 2026-10-25, cite S257, used-by, README index (quote clause already passes); soften "enforces it structurally" | same lines; QUALITY 3, 10 |
| `r8-gtest-generator-contract.md` | S204 → none | **REFUSE this round** — no admitted row (contract id_map has only S256/S257) and no located quote; content is generic test-framework reference material as packaged (paraphrased table, miscount, unreconciled with S120, no lane-gate binding) | `PROVINCE.md` Refuses (report, never absorb); `README.md:70-73` (row-required); QUALITY 2, 3, 10 |

## 4. Residual risk and verification gaps

- I did not run either counter (bounds): the `entry_ok` outcomes above are a local
  re-implementation from `measure.py:93-112` as committed at the freeze; the ONE
  deciding run is the L1's.
- The landed S256/S257 rows and re-grounded entries are being produced by the
  coverage executor concurrently; these verdicts bind the package entries as
  staged. Each listed condition is individually checkable at the deciding
  revision with `measure.py --rev 3310e7be803516ca5934b4e949d91bcec824b179`.
- Upstream `main` can move after today's byte-identity check; risk is bounded to
  the recheck commands since all pins name the commit.
- Entry 2's 404/tag-history probes are live observations, not committed lane
  evidence; the falsify wave should re-run them or accept the staged row's cell
  as the record.
- Tooling record: no tool installed or upgraded (pacman transactions are paused
  host-wide; nothing was needed — curl, git, python3 already present).
