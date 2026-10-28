# T56W2MutGateOnC0 — the wave-1 gate mutant set re-run at C0

Round 56 / hyaku run 11 / L1 TameshiR56 / wave 2. Leaf seat, no subagent dispatch.
Axis: **operability**. Milestone: **gate mutants against C0**.

Subject: `tools/receipt-revision-gate.py` at the content commit
`C0 = c0137451f5b7f22d65f748fc69f1b181f55e1378`.
sha256 `c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9` (359 lines).

I did not edit the gate, any lane production file, or anything under
`.ufo/evidence/round-56/`. Every mutant is a byte-exact single edit applied to a
**fresh scratch clone** of the lane at C0; the pristine bytes are restored after
each run and the hash re-asserted.

---

## 1. Result — 8/8 KILLED, no survivor in the required set

Baseline on the C0 bytes, before any mutation:

```
$ python3 tools/receipt-revision-gate.py --selftest
CASE matched-positive-accepted PASS
... (19 cases, all PASS) ...
GATE_SELFTEST: 19/19 pass
EXIT=0
```

(receipt `baseline-selftest.stdout`; the suite grew from wave 1's 14 cases to 19
because wave 1's five proposed cases were applied in amendment commit `21eb3c6`.)

Verdict rule: `KILLED` iff the mutated pass count is strictly below the
baseline. Every mutant is **one unified-diff hunk, two changed lines**, and every
mutant's *expected* case is the one that failed — the kill is the intended
assertion, not an unrelated crash.

| # | mutant (one exact edit) | tally after | case that failed | verdict |
|---|---|---|---|---|
| M1 | drop `RECEIPT_REV_ABSENT` | 18/19 (exit 1) | `absent-refused` | **KILLED** |
| M2 | `drifted_paths` returns `[]` (diff-result site) | 18/19 (exit 1) | `content-drift-refused` | **KILLED** |
| M3 | `is_ancestor` always `True` | 18/19 (exit 1) | `control-not-ancestor-refused` | **KILLED** |
| M4 | skip the digest check | 18/19 (exit 1) | `digest-mismatch-refused` | **KILLED** |
| M5 | allow multiple revs in a positive role | 18/19 (exit 1) | `ambiguous-refused` | **KILLED** |
| M6 | skip the required-line check | 18/19 (exit 1) | `required-line-refused` | **KILLED** |
| M7 | treat an empty file as present | 18/19 (exit 1) | `empty-refused` | **KILLED** |
| M8 | drop `RECEIPT_CONTROL_NOT_ANCESTOR` | 18/19 (exit 1) | `control-not-ancestor-refused` | **KILLED** |

Machine record: `mutants.json` (per mutant: exact `old`/`new`, `old_occurrences`,
pristine/mutated/restored sha256, tally, exit, failing cases, verdict).
Exact diffs: `mutant-diffs.md`. Per-mutant stdout/stderr: `mutant-M*.stdout`,
`mutant-M*.stderr`.

**No survivor in the required set.** The C0 suite kills all eight.

### Kill-mechanism notes (the kills are the intended assertion)

- **M1** (`if not revs:` → `if False and not revs:`). The mutant is killed by the
  *case assertion*, not by a named refusal: with `revs` empty the early return
  is gone, the positive branch reaches `full = resolved[revs[0]]` and the child
  dies `IndexError: list index out of range`, exit 1 (`consequence-probe.json`,
  row M1, `mutant_stderr_tail`). The suite pins "not exit 3 with
  `RECEIPT_REV_ABSENT`", which is the property that matters; the mutant is not
  converted into a silent acceptance.
- **M7** (empty file treated as present). The mutant does not accept the empty
  receipt — it refuses it under a *different* code: `RECEIPT_REV_ABSENT`
  ("no rev= token") instead of `RECEIPT_EMPTY` (`consequence-probe.json`, row M7).
  The refusal survives; the named refusal does not, and the case
  `empty-refused` asserts the code, so the mutant is caught.
- **M5** (multiple revs allowed in a positive role). Killed by `ambiguous-refused`.

### Independent behavioural consequence (pristine vs mutant on the same inputs)

`consequence-probe.json` / `probe.py`: for each mutant, one fixture repo, one
receipt, and the **pristine** and the **mutated** gate run on the identical
inputs. "Protection removed" = the pristine gate's *named* refusal is no longer
produced.

| # | pristine | mutant | severity |
|---|---|---|---|
| M1 | exit 3, `RECEIPT_REV_ABSENT` | exit 1, `IndexError` | crash-or-other-exit |
| M2 | exit 3, `RECEIPT_REV_CONTENT_DRIFT` | **exit 0, verdict=PASS** | silent-acceptance |
| M3 | exit 3, `RECEIPT_CONTROL_NOT_ANCESTOR` | **exit 0, verdict=PASS** | silent-acceptance |
| M4 | exit 3, `RECEIPT_DIGEST_MISMATCH` | **exit 0, verdict=PASS** | silent-acceptance |
| M5 | exit 3, `RECEIPT_REV_AMBIGUOUS` | **exit 0, verdict=PASS** | silent-acceptance |
| M6 | exit 3, `RECEIPT_REQUIRED_LINE_MISSING` | **exit 0, verdict=PASS** | silent-acceptance |
| M7 | exit 3, `RECEIPT_EMPTY` | exit 3, `RECEIPT_REV_ABSENT` | degraded-refusal-other-code |
| M8 | exit 3, `RECEIPT_CONTROL_NOT_ANCESTOR` | **exit 0, verdict=PASS** | silent-acceptance |

8/8 remove a protection; six of the eight do it by **silently accepting** a
receipt the pristine gate refuses. The suite's 19 cases pin the behaviour, not
merely the crash.

---

## 2. The six wave-1 survivors are now all killed — the amendment closed them

Wave 1 found six single-edit probes that survived the 14-case suite and proposed
five extra cases. Those cases are in the C0 gate (cases 15–19). Re-running the
identical six probes against C0 (`xprobe.py`, `x-probes.json`):

| probe | wave-1 verdict | C0 verdict | case that now kills it |
|---|---|---|---|
| X1 `CODES` entry swapped for a duplicate | SURVIVED 14/14 | **KILLED 18/19** | `codes-closed` |
| X2 rev regex narrowed to `{40}` | KILLED | KILLED 18/19 | `unresolvable-refused` |
| X3 JSON `rev` tokens dropped | SURVIVED 14/14 | **KILLED 18/19** | `json-rev-parsed` |
| X4 unknown role accepted | SURVIVED 14/14 | **KILLED 18/19** | `unknown-role-refused` |
| X5 zero `--receipt` accepted | SURVIVED 14/14 | **KILLED 18/19** | `zero-receipts-refused` |
| X6 unresolvable `--certified` accepted | SURVIVED 14/14 | **KILLED 18/19** | `unresolvable-certified-refused` |

**0 survivors.** Wave 1's D1 (`RECEIPT_NOT_BLOB` declared but unreachable — a
directory receipt crashed the gate) and D2 (the CLI surface unpinned) are both
closed by cases 15 and 17–19.

---

## 3. FINDING — one coverage hole survives in the 19-case suite (M2b)

**The finding.** `drifted_paths()` has two refusal sites. The wave-1 mutant M2
kills the *diff-result* site (`return [p for p in ...] + gone`), which the suite
pins. The **other** site — the `<no --paths given: content identity is not
checkable>` early return — is **not pinned by any case**. A single exact edit
that replaces it with `[]` **survives the whole 19-case suite**.

```
MUTANT M2b — drifted_paths(): the "<no --paths given>" refusal replaced by []
one exact edit, old occurrences in C0 gate = 1

COMMAND: python3 M2b-gate.py --selftest
STDOUT:
... 19 CASE lines, all PASS ...
GATE_SELFTEST: 19/19 pass
EXIT: 0
VERDICT: SURVIVED — the 19-case suite does not pin the "<no --paths given>" branch.
```

**Why it matters (the consequence, measured).** That branch is the gate's
refusal for a receipt whose `rev=` is *not* the certified revision when the
declared surface is empty. With the branch neutered the gate accepts a receipt
whose content was never checked:

```
COMMAND (pristine): receipt-revision-gate.py --lane REPO --certified 1282acaddb9d \
                    --paths EMPTY.paths --receipt r.txt:positive
  exit 3
  GATE REFUSED .../r.txt role=positive revs=446c2576ad29 \
        code=RECEIPT_REV_CONTENT_DRIFT rev=446c2576ad29 drift=<no --paths given: content identity is not checkable>
  GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED

COMMAND (mutant M2b): same, on M2b-gate.py
  exit 0
  GATE OK .../r.txt role=positive revs=446c2576ad29
  GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS

The receipt names rev=446c2576ad29 while the certified revision is 1282acaddb9d:
a real content mismatch.  PRISTINE refuses; MUTANT accepts.
```

This is precisely the failure class the gate exists for (the round-54/55 defect:
a receipt certified against a revision it was not measured against), reached
through an empty `--paths` file.

**Not a C0 regression.** The same edit survives the wave-1 gate too
(`w1-M2b.py --selftest` → `GATE_SELFTEST: 14/14 pass`, exit 0). Wave 1's
amendment fixed the six named holes and did not reach this one.

**Is it reachable in this round's own use?** Not by the round's own receipts:
both path files the C2 counter feeds the gate are non-empty
(`.ufo/evidence/round-56/c2/red-before/round-54-surface.paths`, 7 lines;
`.ufo/evidence/round-56/control/frozen-surface.paths`, 16 lines), and the gate
raises `RECEIPT_REV_MISMATCH` when `--paths` is omitted entirely (a different,
pinned path). So this is a **hole in the gate's own test suite**, not a live
defect in the round's evidence. Report-only: the gate is a frozen instrument and
the L1 integrates; a one-case addition (an empty `--paths` file must be refused)
would close it.

Full evidence: `09-M2b-coverage-hole.txt`.

---

## 4. Mutant parity with wave 1 — two anchors had to be re-expressed

The C0 gate is **not** the wave-1 gate. Amendment commit `21eb3c6` added five
selftest cases, a `RECEIPT_NOT_BLOB` refusal, JSON `rev` parsing and a
`<unresolvable-path:…>` drift finding. Concretely:

| | wave-1 gate (`c3e2ca9`) | C0 gate (`c013745`) |
|---|---|---|
| sha256 | `1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2` | `c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9` |
| lines | 331 | 359 |
| selftest | 14 cases | 19 cases |
| wave-1 `old` string occurrences in the C0 gate | M1 → 0, M2 → 0, M3–M8 → 1 each | — |

So the wave-1 mutant set could not be replayed verbatim: **M1** and **M2**'s
anchor text no longer exists in the C0 gate (M1 gained a `detail = detail or
'no rev= token'` line; M2's return gained `+ gone`). I re-expressed both as the
same *semantic* single edit against the C0 bytes:

- **M1**: `    if not revs:\n        codes.append('RECEIPT_REV_ABSENT')` →
  `    if False and not revs:\n        codes.append('RECEIPT_REV_ABSENT')`
  — identical effect (the wave-1 edit spanned three lines, the C0 equivalent
  spans two because the third line moved).
- **M2**: `    return [p for p in r.stdout.decode().splitlines() if p] + gone` →
  `    return []` — the same diff-result site, with C0's `+ gone` suffix.

M3–M8 replay **byte-identically** (their wave-1 `old` strings occur exactly once
in the C0 gate and were used unchanged). The re-anchored M1 and M2 were checked
against both gates: wave-1's own `02-mutants.json` shows M1 killed by
`absent-refused` and M2 by `content-drift-refused`, which is what the re-anchored
edits reproduce at C0.

**Additional check** (scope confirmation, not a new mutant): the wave-1 exact M8
form (`codes.append(...)` → `pass`) was re-run against C0 → 18/19, killed by
`control-not-ancestor-refused` — identical to my M8.

---

## 5. Supporting operability evidence (not my claim to certify)

The C2 counter run read-only at C0, `--work` an empty scratch dir:

```
$ python3 .ufo/evidence/round-56/c2/measure.py --lane LANE \
      --rev c0137451f5b7f22d65f748fc69f1b181f55e1378 --work EMPTY --explain
EXPLAIN arm1-selftest exit=0 19/19
EXPLAIN arm2-red54 exit=3 codes=RECEIPT_REV_CONTENT_DRIFT old-gate-accepted=True
EXPLAIN arm3-red54b exit=3 codes=RECEIPT_REV_UNRESOLVABLE
EXPLAIN arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT
EXPLAIN arm6-docs 4/4
C2_R56: ... own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false
```

The gate's own arms all behave as the contract wants: its selftest is 19/19, and
the three real red-before receipts are refused with their **named** codes
(`RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_REV_UNRESOLVABLE`, `RECEIPT_REV_ABSENT`).

`arm5` fails as `own-receipts-missing`: at C0 the tree carries only
`.ufo/evidence/round-56/control/frozen-surface.paths` — the round's own
`controls-a.stdout` / `controls-b.stdout` receipts do not exist yet, because
`controls.sh` has not run at this revision. That is expected pre-bind state for
this revision, not a gate defect, and it is not my claim to certify (the
executor seat owns the controls run).

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tameshi` → `CENSUS_EXIT=0` (with the pre-existing W04 duplicate-URL warnings),
`07-census.txt`.

Freeze integrity at C0: all 12 `freeze.json` file pins re-computed from the C0
tree, **0 mismatches** — including `tools/receipt-revision-gate.py` =
`c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9`.

---

## 6. Method (reproducible)

Scratch `S=/fast/scratch/hyaku/tameshi-r56/T56W2MutGateOnC0` (removed on exit;
`trap 'rm -rf -- "$S"' EXIT`). Drivers archived as receipts: `driver.py`
(mutants), `probe.py` (behavioural consequence), `xprobe.py` (wave-1 survivors).

1. Eight **fresh** clones: `git clone --shared "$LANE" "$S/mN"` then
   `git -C "$S/mN" checkout --detach c0137451f5b7f22d65f748fc69f1b181f55e1378`.
   Each clone's `git rev-parse HEAD` was asserted `== C0` and
   `git rev-parse --show-toplevel` `== $S/mN` before any edit.
2. Baseline `--selftest` on the pristine clone → `19/19 pass`, exit 0.
3. For each mutant: assert the `old` string occurs **exactly once** in the C0
   gate bytes; apply the one replacement; run `--selftest` on the mutated copy
   (the selftest re-invokes `Path(__file__)`, so the mutated code is what runs);
   record tally, exit, failing case names and stderr; rewrite the pristine bytes
   and assert the sha256 matches again.
4. Verdict rule: `KILLED` iff the pass count is strictly below baseline.

The suite is hermetic for this purpose — it runs in `tempfile.TemporaryDirectory`
with `HOME=tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`. It was
re-run with `GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent` as well and still
reports `19/19 pass`.

## 7. Restoration and non-interference

- Gate sha256 in the lane before and after: `c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9`
  (both). `git status --porcelain -- tools/ SKILL.md SCORECARD.md LOG.md corpus/`
  → empty.
- Every clone's gate file was restored to the pristine bytes after its mutant
  run; `restored_exact: true` for all eight (`mutants.json`, `00-hashes.txt`).
- No mutating git or jj command was run anywhere: only `clone`, `rev-parse`,
  `checkout --detach`, `show`, `status --porcelain`, and `merge-base
  --is-ancestor` inside the gate's own fixture repos. No commit was created
  anywhere except inside the gate's own `TemporaryDirectory` fixture.
- Nothing under `.ufo/evidence/round-56/` was written. My only writes are
  `.ufo/waves/round-56/w2/T56W2MutGateOnC0.md`,
  `.ufo/waves/round-56/w2/T56W2MutGateOnC0.json` and
  `.ufo/waves/round-56/w2/T56W2MutGateOnC0-receipts/`.
- Tooling: no install or upgrade was needed. The seat ran on the host `python3`
  3.14.8 and `git` 2.56.0 as found; no new tool was added, so nothing to record
  against the operator's tooling directive.

## 8. Receipts

`T56W2MutGateOnC0-receipts/`:
`00-hashes.txt` (C0/lane/freeze pins), `baseline-selftest.stdout` /
`.stderr`, `mutants.json` (the 8 mutants, machine record), `mutant-diffs.md`
(the 8 exact diffs), `mutant-M{1..8}.stdout` / `.stderr` (per-mutant runs),
`consequence-probe.json` (pristine-vs-mutant behaviour), `x-probes.json`
(wave-1 survivors re-run), `09-M2b-coverage-hole.txt` (the surviving probe and
its consequence), `07-census.txt`, and the three drivers `driver.py`,
`probe.py`, `xprobe.py`.

## 9. Summary for the L1

- The required set: **8/8 KILLED** at C0, each by its expected case, each one
  exact edit. No survivor in the required set.
- Wave 1's six survivors: **all six now killed** by the amendment's new cases;
  wave 1's D1 and D2 are closed.
- **One new finding (report-only, not a contract change):** the
  `<no --paths given>` refusal inside `drifted_paths()` is unpinned — a single
  exact edit neutering it survives the 19-case suite and makes the gate
  **accept** a receipt whose revision differs from the certified one. It is
  reachable only through an empty `--paths` file, which the round's own
  receipts never use, so the round's evidence is unaffected. A one-case
  addition (an empty `--paths` file must be refused with
  `RECEIPT_REV_CONTENT_DRIFT`) would close it; that belongs to round 57, since
  the gate is a frozen instrument and the L1 integrates.
- The C2 counter's gate arms behave correctly at C0 (selftest 19/19; the three
  real red-before receipts refused with their named codes). `arm5` is
  `own-receipts-missing` because `controls.sh` has not run at this revision —
  pre-bind state, owned by the executor seat.
