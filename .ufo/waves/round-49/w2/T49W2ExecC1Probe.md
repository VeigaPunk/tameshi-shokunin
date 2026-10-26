# T49W2ExecC1Probe — frozen C1 counter, probe run at candidate f181a961

Seat: executor probe (leaf). Item: run the frozen C1 counter once at the candidate into an empty scratch
work dir, report the `C1_R49` line, every non-`ok` `PTR` line and the `UNCOVERED_*` lines. **This is a
probe, not the deciding run; nothing below is a verdict.**

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, candidate `f181a961ae44061af486f600e5ea257d2baf78f8`
(base `8ca67421111fa354b47b803358391d0b07fc6db9`). Counter frozen at `a055e9297cc989cc69062ae4a1e5b22c251dc3adfcc073211c5cae3a09346065`,
matching `.ufo/evidence/round-49/freeze.json` (`sha256[".ufo/evidence/round-49/c1/measure.py"]`); the blob at the
candidate has the same digest (`git -C … cat-file blob f181a961…:.ufo/evidence/round-49/c1/measure.py | sha256sum` →
`a055e929…`).

## 1. The run

```
S=/fast/scratch/hyaku/tameshi-r49/T49W2ExecC1Probe
TMPDIR="$S" python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-49/c1/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev f181a961ae44061af486f600e5ea257d2baf78f8 --work "$S/w"
```

Observed: `exit=0`, wall 24.7 s, stdout 102 lines (94 `PTR` + 7 `SECTION` + 1 `C1_R49`), stderr empty.
Receipt: `.ufo/waves/round-49/w2/T49W2ExecC1Probe.stdout` (sha256 `42bcdb6c43aca92dae48540216573b8d4dfa1164b7ed3a8dda93c00635384ed3`).

`C1_R49` line (stdout line 102), verbatim:

```
C1_R49: self=a055e9297cc9 rev=f181a961ae44061af486f600e5ea257d2baf78f8 sections=64 covered=64 score=8 durable_covered=64/64 headings=7/7 pointers=94 floor_short=0 unresolved=0 unverified=0 excerpt_miss=0 not_holds=0 absent=3 total=0 C1_R49_PASS=true
```

Monitor receipts copied unchanged from the run's work dir: `T49W2ExecC1Probe.monitor-rev.json`
(sha256 `c3c5e720…`) and `T49W2ExecC1Probe.monitor-durable.json` (sha256 `a1170490…`); both show
`sections_total=64, sections_covered=64, calibration_restraint_score=8, trace_gate="strict", overrides_used=false`,
empty uncovered list — i.e. 64/64 both at the candidate and at the synthetic one-line-append commit the counter
builds on top of it.

## 2. `PTR` lines that are not `ok`

Exactly three, all `absent`, no `unresolved` / `unverified` / `excerpt_miss` / `not_holds` anywhere
(`grep '^PTR' T49W2ExecC1Probe.stdout | grep -v ' ok$'`):

```
T49W2ExecC1Probe.stdout:45  PTR ## Restore discipline — before/after ide #8 mutate_driver.py -> None None absent
T49W2ExecC1Probe.stdout:59  PTR ### The map — where a reader enters, art #11 plans/round-N.plan.md -> None None absent
T49W2ExecC1Probe.stdout:61  PTR ### The map — where a reader enters, art #13 plans/round-N-record-draft.md -> None None absent
```

All three are path pointers the lane does not hold, and the section prose says so at the same place, so the
contract's `absent` arm applies (`contract.json` C1 predicate: "or `absent` for an unresolvable path pointer"):

- `SKILL.md:398` (restore): "`mutate_driver.py` (one-off and not in-tree; `SCORECARD.md:16`)" — no such file in
  the tree (`git ls-tree -r --name-only f181a961… | grep mutate_driver` → no match). Read row: `reads.json`
  restore ordinal 8, `verdict: absent`, reader `T49Read09`.
- `SKILL.md:1393` (the map): "`plans/round-N.plan.md` (latest `plans/round-11.plan.md`), `plans/round-N-record-draft.md` …
  `N` is a placeholder, not a file" — the concrete files exist for rounds 2–11 only. Read rows: map ordinals 11
  and 13, `verdict: absent`, readers `T49Read11` / `T49Read12`.

Counter's allowance for this arm: `.ufo/evidence/round-49/c1/measure.py:274`
(`if p.get('pointer_kind') == 'path' and row is not None and row.get('verdict') == 'absent' …`).

## 3. `UNCOVERED_*` lines

None. `grep -n '^UNCOVERED' T49W2ExecC1Probe.stdout` → no output; the `for h in mon['uncovered']` /
`dur['uncovered']` loop emitted nothing, consistent with `covered=64` and `durable_covered=64/64`.

## 4. Determinism of the probe

A second run into a second empty work dir (`"$S/w2"`, same lane/rev, same `TMPDIR`) produced
**byte-identical stdout**: `T49W2ExecC1Probe-run2.stdout` sha256 `42bcdb6c…` = run 1, `exit=0`.
Both runs are disclosed here; neither is the deciding run.

## 5. Cross-checks on the state the probe measured

Commands are run from the lane root at the candidate unless noted; all are read-only.

**(a) Pointer counts vs base.** `--list` at the candidate vs the base listing
`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`: base 90 pointers, candidate 94. Per section
(`SECTION` lines in the stdout): recipe 36 (floor 34), restore 11 (10), map 18 (17), promotion 5 (5), round-12 5 (5),
round-13 9 (9), round-14 10 (10) — no section below its floor. Observed delta:

- recipe +2 net: new `tools/mutate-and-run.sh:425`, new `tools/mutate-and-run.sh:569-574` (both read by the L1
  itself, see (c)); `mutation-case-kagi-census.md:82-103` re-numbered to `:67,82-103`; `:111-114, :118-122, :251-253`
  extended to `:252-254`.
- restore +1: new `SCORECARD.md:16` (the row note records "pointer count 10 -> 11, so the floor (10) still holds");
  `mutation-case-kimi-census.md:4-7` extended to `:4-7, :172`.
- map +1: new `plans/round-11.plan.md`; two bare pointers gained the `SKILL.md:` prefix (`:1294-1297`, `:1246-1270`).
- round-14: 0 net (three bare pointers re-prefixed to `.ufo/evidence/round-14/…`).

Observation for the L1: the contract predicate says "each section keeping its base pointer count", while the
frozen counter enforces `counts[h] < FLOORS[h]` (`measure.py:382`), i.e. **one-sided** — a section may grow and
still pass. Three sections did grow (+2/+1/+1). Both readings are defensible from the frozen text (`floors` are
named as base counts); the wording gap is recorded, not adjudicated here. The growth is covered: all 94 pointers
have a read row (below).

**(b) `reads.json` integrity at the candidate.** `.ufo/evidence/round-49/c1/reads.json`
(`schema tameshi-r49-reads-v1`): 94 rows for 94 pointers, **no duplicate `(heading, ordinal, raw)` key**, verdicts
`{holds: 91, absent: 3}`, zero rows without a `reader`. The counter's own excerpt gate (`EXCERPT_MIN=24`,
`measure.py` `check_reads`) reported `excerpt_miss=0`, so every `holds` excerpt is a verbatim (whitespace-normalised)
substring of the pointed range at the candidate.

**(c) Two read rows are self-read by the L1.** `reads.json:213` and `reads.json:408`
(`grep -n '"reader": "L1' <(git cat-file blob f181a961…:.ufo/evidence/round-49/c1/reads.json)`) are the two
recipe pointers the correction introduced (`tools/mutate-and-run.sh:425`, `:569-574`), each carrying
`reader: "L1 TameshiR49 (pointer introduced by correction from T49SecRecipe)"`. Independent (wave-1 seat) coverage
is therefore 92/94; the counter cannot distinguish who read. Flagged as an independence limit, not a failure —
both rows' excerpts are verbatim at the pointed ranges.

**(d) Re-key ledger entries are trace-bound to the cited non-record files.** The seven latest entries in
`.ufo/evidence/round-21/coldread/ledger.json` (the ledger the unchanged round-21 monitor selects) all have
`read_rev = 9b9b2a01…`, `sha256` equal to the section's sha at `f181a961…` (**sha_match=True for all 7**),
`commands_executed_count=1`, `class="record"`, `verdict="verified-record"`. Set comparison of each entry's
`inputs` (minus the ignored `SKILL.md`) against the non-record files its section points at:

```
recipe: cited-not-in-inputs none | inputs-not-cited none
restore: none | none
map: none | none
promotion: none | none
round-12: none | none
round-13: none | none
round-14: none | none
```

Record files (`LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`) stay out of
`inputs`, and `SKILL.md` is in the implementation's `IGNORED_INPUTS` (`.ufo/evidence/round-18/measure.py:135`), so
the input gate sees only cited non-record bytes.

**(e) Durability semantics actually exercised.** The counter appends one line at **end of file** to each of the five
volatile records (`VOLATILE` / `PROBE_LINE`, `measure.py`; `durability_commit`), then re-runs the monitor on that
synthetic commit: 64/64, score 8 (receipt above). Limit worth naming: the restore section now carries a **record**
line pointer, `SCORECARD.md:16` (inside the round-3 operability row); an EOF append preserves it, an append that
inserts lines above 16 would not. That is inside the frozen predicate ("one line is appended to each of the five
record files"), so the probe reports it as a scope note, not a miss.

**(f) Refresh receipts name a rev one commit behind the tested one.** `.ufo/evidence/round-49/coldread/refresh-receipts.json:2`
records `"candidate": "9b9b2a016adcf2fab2e0cb1ef89ef78f454b8ec6"`, and the seven ledger entries carry
`read_rev: 9b9b2a01…`. `git rev-list --count 9b9b2a01…..f181a961…` → `1`, and `SKILL.md` has the same sha
(`be660dc26d64d9e3e399cd622161b672c69183f72bf923b00af8b3665be79fc7`) at both commits, so the receipts still
describe the tested SKILL.md byte-for-byte (consistent with the `sha_match=True` in (d)); the mismatch is in the
`candidate` label, not in the bound bytes.

**(g) Lane left untouched.** `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain` after the
runs shows only other seats' `w1`/`w2` files (plus my two `.stdout` copies and this report under `w2/`); no tracked
mutation and no change to the index. The counter writes only under `--work`; its durability step runs
`git clone --shared --no-checkout <lane> <work>/dur` and `commit-tree`s into that clone
(`git -C <clone> rev-parse --show-toplevel` is asserted equal to the clone by the counter itself).

## 6. Tooling

No tool installed or upgraded (none needed; pacman is paused host-wide regardless). Environment: Python 3.14.8,
git 2.56.0, scratch root `/fast/scratch/hyaku/tameshi-r49/T49W2ExecC1Probe` (deleted before this report was
returned; only the copied receipts in `w2/` are cited).

## Summary

- Probe at `f181a961` exit 0: `total=0 absent=3 … C1_R49_PASS=true` (stdout:102), sections 64/64, score 8,
  durable 64/64, headings 7/7, pointers 94.
- Only three non-`ok` `PTR` lines, all `absent` path pointers whose section text explicitly says the file is not
  in-tree / `N` is a placeholder (SKILL.md:398, SKILL.md:1393); no `UNCOVERED_*` lines (stdout:45,59,61).
- Two independent runs produce byte-identical stdout (`42bcdb6c…`); counter bytes equal the freeze digest.
- 94 read rows for 94 pointers, no duplicate keys, verdicts holds 91 / absent 3, excerpts verified by the counter.
- Ledger: 7 entries sha-match the candidate's sections, `cmds=1`, inputs exactly equal each section's cited
  non-record files (no missing, no extras); record files and SKILL.md stay out of the input gate.
- Notes for the L1, not verdicts: sections grew +2/+1/+1 against one-sided floors (`measure.py:382`) while the
  contract says "keeping its base pointer count"; two rows (reads.json:213,408) are L1 self-reads; the durability
  probe appends at EOF only, and the restore section now carries a record line pointer (`SCORECARD.md:16`);
  refresh receipts label the candidate as the parent commit `9b9b2a0` with identical SKILL.md bytes.
