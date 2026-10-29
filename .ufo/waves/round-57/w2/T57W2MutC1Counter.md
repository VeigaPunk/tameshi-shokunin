# T57W2MutC1Counter — mutation test of the amended C1 counter

**Verdict: 13/14 mutants KILLED by the amended counter's `--selftest`; 1 SURVIVED (M10), and the
survivor masks a real, live defect.** A proposed selftest case that kills M10 is staged; with it
the counter kills 14/14.

Machine-readable: `.ufo/waves/round-57/w2/T57W2MutC1Counter.json` (`[{id, old, new, killed_by}]`,
plus `verdict` and, for the survivor, the proposed selftest case).
Receipts: `.ufo/waves/round-57/w2/T57W2MutC1Counter-receipts/`.

## What was mutated, and against which bytes

The item named the counter as
`.ufo/waves/round-57/w2/T57W2ExecC1Selftest/stage/.ufo/evidence/round-57/c1/measure.py` (the
selftest-updated version), falling back to `.ufo/evidence/round-57/c1/measure.py` if it never
appeared. **The staged file appeared at 21:55** and was polled for content change (sha256 watcher,
`receipts/`-adjacent `poll2.log`): it changed at 21:58 (`a1f27ee5…`) and again at 22:00
(`de1b47a0…`), then held `de1b47a0…` stable across eight consecutive 25 s samples. All results
below are against that stable `de1b47a0…` version (a snapshot copy, so a concurrent edit could
not move the bytes under a run).

- Baseline (pristine, staged `de1b47a0…`): `C1_R57_SELFTEST: 95/95 pass`, exit 0.
  Receipt: `receipts/BASELINE.stdout`.
- The lane file `.ufo/evidence/round-57/c1/measure.py` is a **different, older** copy
  (`63a88c25…`, mtime 21:48, still the pre-selftest-rewrite version). Its own selftest fails
  11/45 (the fixture rows lacked `status_at_base`), so a campaign against it would have been
  INCONCLUSIVE throughout; it was not used for any verdict. **The lane file was not modified**
  (mtime unchanged at 21:48:40).

## Method

`receipts/mutate.py` (copied from scratch): for each mutant it copies the pristine counter into a
fresh scratch dir, applies **exactly one** single-edit substitution (asserting the old string
occurs **exactly once** — all 14 verified unique), writes the mutant to its own copy, and runs the
same bounded behavioural detector `python3 measure.py --selftest --work DIR` on pristine and
mutated bytes. The pristine source is never written to: only copies are mutated. Each mutant gets
its own fixture repo (the counter's selftest builds a fresh git fixture per run), so no mutant
sees another mutant's state.

- KILLED = baseline green and the mutant's selftest fails (exit 1, `n/95 < 95`).
- SURVIVED = baseline green and the mutant's selftest still passes (`95/95`).
- INCONCLUSIVE = baseline red (not the case here; baseline was green throughout).

Per-mutant stdout: `receipts/M01-…stdout` … `receipts/M14-…stdout`; the full machine summary:
`receipts/mutation-summary.json` (post-proposed-case) and
`receipts/mutation-summary-pre-proposed-case.json` (the campaign as run against the counter as
staged).

## Results (14 single-edit mutants of the amendment-1 code)

| id | mutation | verdict | killed by (selftest case names) |
|----|----------|---------|----------------------------------|
| M01 | key token regex loses the whole-token look-arounds | **KILLED** | 7 key-token cases (`key token: hyphen after`, `underscore after`, `hyphen before`, `letter after`, `letter before`, `BACKTICK in BACKTICK_RE excerpt`, `TICK_RE in BACKTICK_RE excerpt`) — 87/95 |
| M02 | `introduced` check removed (excerpt need not be absent at the commit's first parent) | **KILLED** | `introduced: excerpt already at the first parent refused` — 94/95 |
| M03 | item-tie check removed (commit message / item text need not tie to the item) | **KILLED** | 3 cases (`forgery: excerpt quoted into a new file under an unrelated message refused`, `message naming R50.12 / xR50.1 / v1.R50.1 does not name R50.1`, +1) — 92/95 |
| M04 | `names_id` regex loosened (message-id match loses its boundary look-arounds) | **KILLED** | `message naming R50.12 / xR50.1 / v1.R50.1 does not name R50.1` — 94/95 |
| M05 | newest-`Planned (round N)` selection `>=` → `<` | **KILLED** | 51 cases, incl. `good ledger passes`, `good verdict line fields` — 44/95 |
| M06 | base-status coherence removed (`status_at_base='fixed'` no longer forces `status='fixed'`) | **KILLED** | `fixed at base but open now refused`, `fixed at base but declined now refused` — 93/95 |
| M07 | `(sab == 'fixed') != is_ancestor(commit, base)` flipped | **KILLED** | 57 cases, incl. `good ledger passes` — 38/95 |
| M08 | panel content pin no longer checked | **KILLED** | `panel pin mismatch: panel_pin=1, panel=pin`, `cli default panel pin (PANEL_SHA256) is a miss: exit 1, panel=pin` — 93/95 |
| M09 | panel disagreement allowance `>` → `>=` | **KILLED** | 5 cases, incl. `panel exactly allowed disagreements passes`, `panel one over allowed: panel_over=1`, `panel over counts the excess only` — 90/95 |
| **M10** | **panel verdict lookup defaults to `'fixed'` when the panel omits an id** | **SURVIVED** | — (still 95/95) |
| M11 | HARD path list shortened (`freeze.json` dropped) | **KILLED** | `hard path refused: freeze.json` — 94/95 |
| M12 | old49 comparison weakened (count only, not canonical equality with BASE bytes) | **KILLED** | `rewritten old row counted (old49 arm)` — 94/95 |
| M13 | BASE-ancestor setup guard removed | **KILLED** | `BASE not an ancestor of REV is setup` — 94/95 |
| M14 | this-round floor off by one | **KILLED** | 3 cases, incl. `fix older than base is not this round`, `this-round floor counted` — 93/95 |

## The survivor (M10) is a real defect, not an equivalent mutant

**Mutation.** In `measure()`, the panel arm's disagreement list:

```python
dis = [d['id'] for d in defects if (by_id.get(d['id']) or {}).get('status_at_base') != verdicts.get(d['id'])]
```
becomes
```python
dis = [d['id'] for d in defects if (by_id.get(d['id']) or {}).get('status_at_base') != verdicts.get(d['id'], 'fixed')]
```

**Why it matters.** `panel.json` is the *blind* arm: a panel of seats that never saw the ledger
rows. If the panel file omits a verdict for an id, that id has not been independently adjudicated
— the counter must treat it as a disagreement. With the mutation, a missing verdict silently
becomes the verdict `'fixed'`. For any row whose own `status_at_base` is `'fixed'`, the row's own
claim is echoed back at it and the disagreement **disappears**: `panel_over` stays 0 and the
counter prints `C1_R57_PASS=true`.

**Proof** (`receipts/M10-probe.txt`, harness `receipts/probe_m10.py`): a fixture repo with one
new row `{status: fixed, status_at_base: fixed, commit: <the fix>}` and a panel file
`{"verdicts": {"R50.9": "open"}}` — no verdict for `R50.1`.

```
counter  : snapshot2-measure.py                       (pristine)
verdict  : C1_R57: self=c6a05b48dc5e rev=89a2cb40461a rows=1/1 agree=1/1 old49=ok fixed=1 declined=0 thisround=0 panel=1/0 spot=ok total=1 C1_R57_PASS=false
notes    : [('panel-disagree', 'R50.1')]
RESULT   : REFUSED (defect caught)

counter  : probe/mutant-M10.py                        (mutated)
verdict  : C1_R57: self=c59ca01e5d91 rev=89a2cb40461a rows=1/1 agree=1/1 old49=ok fixed=1 declined=0 thisround=0 panel=0/0 spot=ok total=0 C1_R57_PASS=true
notes    : []
RESULT   : PASS (defect masked)
```

Same fixture, same revision, same ledger: the pristine counter refuses the panel, the mutant
passes it. The amendment-1 arm the L1 added is exactly the arm this defeats — the blind panel is
supposed to be the check that a row's `status_at_base` claim is corroborated; with the mutation a
`fixed` claim is self-certifying whenever the panel is silent.

**Why the shipped selftest misses it.** The staged counter has
`case('panel without a verdict for an id disagrees', ...)` (line 761) — but that fixture omits
`R50.3`, whose row claims `status_at_base='declined'`. Under M10 the missing verdict becomes
`'fixed'`, which still ≠ `'declined'`, so the disagreement survives and the case still passes. The
surviving hole is exactly the row whose claim is `'fixed'`.

## Proposed selftest case (staged)

Staged at
`.ufo/waves/round-57/w2/T57W2MutC1Counter/stage/.ufo/evidence/round-57/c1/measure.py`
(sha256 `3bf1dd7185b85a2276e942dac75e06f17e1b91b0be2010b579d2512208e40d79`), which is the
selftest seat's staged `de1b47a0…` **plus one added case and nothing else** (diff: 7 added lines
after `row status_at_base against panel verdict disagrees`):

```python
# (5b) blind-panel arm: a MISSING panel verdict must be a disagreement even when the row
# itself claims status_at_base='fixed' -- a defaulted verdict lookup must not echo the row's
# own claim back at it (M10, wave-2 seat T57W2MutC1Counter).
counts, _, total, kv, _ = run(variant(lambda r: r[0].update(status_at_base='fixed')), base=fix,
                              panel={'R50.2': 'open', 'R50.3': 'declined'}, allowed=0, **NF)
case('panel without a verdict for a fixed-at-base id disagrees', counts['panel_over'] == 1
     and total == 1 and kv['panel'] == '1/0')
```

`base=fix` puts BASE at the fixing commit so the row is coherent (`sab='fixed'` + commit ancestor
of BASE); `**NF` (`floor=0, trf=0`) keeps the refused row from also tripping the fixed /
this-round floors, so the case measures the panel arm alone.

**Verified in both directions** (receipts `selftest-with-proposed-case.txt`,
`selftest-M10-mutant-with-proposed-case.txt`):

- staged counter + proposed case → `C1_R57_SELFTEST: 96/96 pass`, exit 0 (no regression);
- staged counter + proposed case + M10 → `C1_R57_SELFTEST: 95/96 pass`, exit 1, the new case
  FAILs (`panel without a verdict for a fixed-at-base id disagrees`).

Re-running the whole 14-mutant campaign against the counter **with** the proposed case
(`receipts/mutation-summary.json`) gives **14/14 KILLED**, every other mutant still killed by the
same case names as before — the addition kills M10 and regresses nothing.

## Notes and limits

- This seat mutates the *detector*, not the contract. The surviving mutant is reported as a
  coverage finding with a proposed case; no change to the counter's semantics is proposed or made.
- The campaign covers the amendment-1 code the item enumerated (14 single edits over the key-token
  regex, the introduced / item-tie / names_id checks, planned-by-round selection, base-status
  coherence, the panel pin / allowance / verdict lookup, the HARD path list, the old49 comparison,
  the BASE-ancestor guard and the this-round floor). It is a sample, not exhaustive: the C1
  counter's other arms (spot-check sha, `extra`/`duplicate`/`missing` row bookkeeping, evidence
  resolution, the declined-reason length) were exercised by the counter's own fixtures and by the
  selftest seat's 32-mutant sweep, not re-attacked here.
- The L1's `PANEL_SHA256` is still the pending marker in the staged copy, so the CLI's default
  panel pin is a designed miss; M08/M09 were killed on the pin and allowance arms, which the
  selftest drives through an explicit `panel_pin`.
- No lane file was edited. Everything I wrote lives under my seat's `w2/` paths and my scratch
  (`/fast/scratch/hyaku/tameshi-r57/T57W2MutC1Counter`, removed on exit by the session trap).
- **Tools: none installed** (no pacman / uv / npm / cargo action was needed; Python 3.14 and git
  were already present).
