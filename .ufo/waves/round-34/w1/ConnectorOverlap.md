# ConnectorOverlap — round 34, wave 1

**Overlap scan: no cross-lane ownership conflict (as expected). One bounded proposal follows:**
the round's own 8-case witness-probe battery is blind to forced-verdict mutants in both vector
arms of the amended gate — two one-line gate mutants outside the six dispatched MutCounter
operators survive it 8/8 and agree with the true gate on all 14 sealed copies, and their
forced-false duals survive it too. Proposal: add three polarity-closing cases to the dev battery
(kill+vector positive, kill+vector behavioral-negative, accept+vector negative) as an r35
pre-data, dev-only item; all four forced-verdict mutants are then killed, verified by execution.
No C1 verdict, integration, or admission is asserted.

Axes: this seat addresses **adjacency** (it connects the 6 MutCounter seats, the 14 copy seats,
the 8-probe battery, and the r35 Holds into one checkable claim). The proposed battery extension
supports **quality** (calibration of the dev witness battery) and **expansion** (two new probe
cases + two new mutant operators as corpus ground). C1 **operability** and **discernment** are
not re-measured here; the deciding run stands.

## 1. Setup and pins (verified before any run)

Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ConnectorOverlap/`. Lane clone detached at tip
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (`git -C lane rev-parse HEAD` → same, exit 0).

```
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py     # exit 0
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh # exit 0
sha256sum tool.py pristine.sh
```

| artifact | sha256 | pin | match |
|---|---|---|---|
| `tool.py` (tally-audit-v2.py) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (mutate-and-run.sh) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| `lane/.ufo/evidence/round-33/c1/c1-measure.py` (amend-6 counter) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | same | YES |

Full receipt file: `/fast/scratch/hyaku/tameshi-r34-seats/ConnectorOverlap/receipts.sha256`.

## 2. Sibling-overlap scan

Scan scope per assignment: fleet `.ufo/reports/round-34/` and fleet `.ufo/waves/` (read-only).

**(a) Fleet lane reports `.ufo/reports/round-34/`** — keyword scan
`grep -i -c "tally-audit\|heldout\|held-out\|bwrap\|sandbox\|witness" *.md` (exit 0):

```
chousa.md:0  kaidoku.md:2  kake.md:3  kotodama.md:0  kumitate.md:0  mori.md:0  tsukuroi.md:0  tameshi.md:26
```

`tameshi.md` is this lane's own report (the round-34 artifacts under test are its C1 evidence).
The kaidoku/kake hits are unrelated bytes, quoted for the record: kaidoku.md:62,104 say each seat
had "its own sandbox clone" (a wave-mechanics statement); kake.md:45,47,121 say "Sandbox only,
not landed" / "sandbox-only evidence" (kake's own lane evidence). No lane report seats a worker
on tally-audit, witness semantics, sealed held-out sets, or bwrap sandboxes.

**(b) Fleet waves `.ufo/waves/`** — recursive `grep -rl tally-audit` (exit 0) finds exactly one
file: `hyaku/PHASE4.md:247`, the orchestrator's round-32 closure record
("Tameshi r32 landed; … C1 capability (tools/tally-audit.py) MISSED on frozen counter v2 …").
Historical; no current seat.

**(c) This lane's own wave `.ufo/waves/round-34/w1/`** — 35 seat reports landed at scan time
(list captured in `sibling-reports.txt`): 13 Mut* copy attacks, 6 MutCounter gate mutations,
3 Residue* r35 probes, 7 review/cold-read receipt seats, SentinelToolPin, QualityGate,
WaveSpecAudit, ScribeFrontier, CensusRecheck, SrcRecheckS101, LedgerDepth, MisrootSweep. Every
one is a seat of this lane's dispatch (`.ufo/waves/round-34/dispatch-w1.json`, 64 seats);
each names the same pinned artifacts.

**Ownership verdict: no transfer suggested (none expected).** This lane's round-34 artifacts
(the frozen tool, the amend-6 counter, the sealed 14, the controls receipt, the bwrap boundary)
are owned exclusively by this wave's seats; no other lane's report or wave touched them this
session. Sibling experiments were read, not rerun (the one exception is my own adequacy check in
§3, which is not any sibling's assigned experiment).

## 3. The bounded proposal and its evidence

### 3.1 Finding: two one-line gate mutants survive the 8-probe battery

The amendment-6 dev battery (`.ufo/evidence/round-34/dev/witness-probes.json`, 8 cases) covers
the voidability analysis: one positive accept+vector equivalence case, both head-kill arms
(positive and inert-negative), both accept+head arms, and the kill+vector block-identical
refusal. Its committed expected tuples contain **no positive kill+vector case** (nothing expects
`(True, 'vector')`) and **no negative accept+vector case** (nothing expects `(False, ...)` from
a behavioral-differ). So a mutant that forces either vector-arm verdict to True flips no probe.

I reconstructed the 8 probes (constructions in `probe_adequacy.py`; each probe's witness/edit
chosen to hit the committed tuple), ran them against the true gate via module import, and got an
exact 8/8 match to the committed tuples (`adequacy.stdout`, sha256
`10dbed20309a67a2334a6fa30c3adb2e2edf9e359b033f06e3ba6f06026b0a3f`). I then built two
single-line gate mutants — each a one-hunk diff, verified by `diff -u` (`mutants.diff`;
`diff` exit 1 = differences present, 2 changed lines per mutant):

- **M1** (`mut/.../c1-measure.py`, sha256 `fe6f4087…35174`): kill+vector tail
  `return a != b, 'vector'` → `return True, 'vector'` (all refusal clauses above kept).
- **M2** (`mut/.../c1-measure-av.py`, sha256 `d8104acd…d459`): accept+vector
  `return a == b and mutated != pristine, 'vector-equivalence'` → `return True, 'vector-equivalence'`.

Both are outside the six dispatched MutCounter operators (set-branch flip, len-9 relaxation,
block-identical refusal removal, head-block-check removal, leg-regex weakening,
equivalence-bytes removal — dispatch-w1.json). Running the battery against each:

```
M1-kv-force-true probe flips: 0 (survives battery)
M2-av-force-true probe flips: 0 (survives battery)
SUMMARY true=8/8 M1_flips=0 M2_flips=0        # adequacy.stdout, harness exit 0
```

Cross-check on the real sealed set (`sealed_crosscheck.py`, exit 0; `crosscheck.stdout`, sha256
`518ef505…ed29`): both mutants agree with the true gate on **all 14** sealed-copy witness
verdicts (M1=0/14 diffs, M2=0/14 diffs). So neither the battery nor the landed copies can
distinguish these mutants from the true gate; only the committed bytes (sha-pinned in the
controls receipt) actually exclude them today.

Threat reading: this does **not** void C1. The deciding run executed the true gate bytes
(receipt attests `f6b8868c…a07f28c`); the tool is the scored instrument; and both mutants only
loosen the pre-data witness screen, whose backstop is the per-copy real-tool authoring receipt
(lesson round-34 Mistakes #1). The exposure is to **future** gate work: if r35 amends the gate
and validates the amendment with only these 8 probes, a forced-True regression in either vector
arm ships undetected.

### 3.2 Proposed move (one, bounded)

Add three cases to the witness-probe battery as a **round-35 pre-data dev item**
(measurement-only this wave; the counter is frozen and is not edited), so both vector arms carry
both verdict polarities. All flip-targets verified by execution against reconstructed
forced-verdict mutants (receipts below):

1. **KV-positive** — a kill+vector copy whose block genuinely changes the tally tuple at the
   witness vector (`a != b`); expect `(True, 'vector')`. Kills the forced-false kill+vector
   mutant (`return False, 'vector'` → verified flip, `duals.stdout` sha256 `38c7382c…c7b6`).
   (The 6 landed kill+vector copies are living instances, e.g. `ho-kill-vector-arm-swap.json`.)
2. **KV-behavioral-negative** — a kill+vector copy whose block is byte-changed but tally-
   equivalent at the witness vector (`a == b`); expect `(False, 'vector')`. Kills M1 (verified
   flip to `(True, 'vector')`, `anchors.stdout` sha256 `261a55eb…ef86`).
3. **AV-negative** — an accept+vector copy whose block behaviorally differs at the witness vector
   (bytes changed, `a != b`); expect `(False, 'vector-equivalence')`. Kills M2 (verified flip to
   `(True, 'vector-equivalence')`, same receipt).

The fourth combination needs no new case: the forced-false accept+vector mutant
(`return False, 'vector-equivalence'`) is already killed by the existing Q1 probe (verified
flip, `duals.stdout`). Together with the existing KV-block-identical structural negative, both
vector arms then have positive and negative expectations, and all four forced-verdict mutants of
the two vector-arm tails flip ≥1 probe. Each new case is itself a refusal/acceptance the amended
rule already justifies (a kill must demonstrate a fault; an accept must demonstrate equivalence),
so the extension documents the existing semantics rather than inventing new ones.

## 4. Second-order effects and contradictions

- **Runtime:** the added probes are dev-battery cases; they add no invocation to the frozen tool
  or runner and consume no kill-rule runs (all checks here were module imports in scratch).
- **Contract:** `.ufo/evidence/round-33/contract-amendments.json` (amendment 6) fixes the gate;
  the battery extension does not amend the predicate, drop rows, lower thresholds, or authorize
  another counter run. Post-data rule changes remain barred (kumitate r42); the extension rides
  to r35 under the freeze-before-data discipline, same as the Residue* Holds.
- **Scope of the claim, stated plainly:** the three added cases do not prove the gate "correct" —
  they make the battery's adequacy *measurable* in both vector arms: M1 (kill forced True) is
  killed only by KV-behavioral-negative, its forced-false dual only by KV-positive, M2 (accept
  forced True) only by AV-negative, and its forced-false dual by the existing Q1 probe — all four
  flips verified in this seat's scratch. A forced-verdict mutant in a THIRD clause (e.g. the
  head-arm `return True, 'head'` tail) would need its own anchor; the general r35 step is to run
  the full single-clause edit set of `ho_witness_ok` against the extended battery and record
  killed/survived, rather than sampling six operators. Until then, the landed measurement's
  protection is the sha-pinned gate bytes in the controls receipt, not the battery.
- **Substrate:** scratch-only; no sibling paths, no new tools, no network. No installs (python3 +
  bwrap only). No lane writes except this report.
- **Verification:** the L1 can reproduce §3.1 with the commands in `probe_adequacy.py` /
  `sealed_crosscheck.py` (sha256s in `receipts.sha256`); expected outputs committed in
  `adequacy.stdout` / `crosscheck.stdout`. The 6 dispatched MutCounter seats independently
  probe their own operators; two of those (relaxlen9, dropequivalencebytes) look no-op-prone
  against this battery by construction (all 8 probes use length-9 vectors, and the caller's
  `edits do not change the runner` check makes the bytes-changed conjunct unreachable) — their
  seats own those reports; this is an observation, not a re-run.

## 5. Risks

Reconstructed probes are construction-independent (only the verdict tuples are asserted), but
the L1 should re-derive them when landing the r35 item. The coverage map certifies probe
adequacy, not gate correctness; gate correctness against the landed measurement rests on the
sha-pinned bytes, untouched here. No seat's scope is duplicated: the MutCounter seats own their
six operators; this seat adds four forced-verdict mutant operators (two arms × two polarities)
+ the adequacy framing, all verified against reconstructed scratch mutants.

Only discovery reads, four scratch harness runs (module import, kill rule not consumed),
read-only Git commands, and this report were produced. No production edits, no Git/jj writes,
no tests/linters run, no model calls, no other agent runtime invoked. All started commands
completed; no owned process remains. Tools installed or updated: none.

Report: .ufo/waves/round-34/w1/ConnectorOverlap.md
