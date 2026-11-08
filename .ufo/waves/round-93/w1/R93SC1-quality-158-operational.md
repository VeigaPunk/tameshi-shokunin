# R93SC1 — draft block 2: a QUALITY.md criterion for QUALITY 158's operational half

**For:** TameshiR93 (L1), for integration into `corpus/QUALITY.md`.
**Lane mode:** read-only; this seat wrote nothing under `corpus/`.

## Where the criterion goes

`corpus/QUALITY.md` ends with criterion **158** (round 92, lines 2585-2592), whose
current text is the *declarative* half — "every conjunct of a counter is falsifiable by a
committed battery state, or it is declared unfalsifiable with the reason at the freeze".
Round 93's C2 claim is the **operational** half: the declaration is turned into a
machine-readable manifest, and the manifest is audited by a checker that can fail.

The house style appends a new numbered criterion at the end of the file, in a
`## Criteria appended — round 93` section (the file's own precedent: round 92 appended
`150.`–`158.` as a bare numbered list under the round-92 section, with the same
`Able to fail:` trailer form). The next free number is **159**. The L1 owns the final
numbering and section placement; the text below is drafted as `159.` with the round-93
header the file's precedent implies.

**Two criteria, not one.** Criterion 158 as written is satisfied by a manifest that
declares *every* conjunct unfalsifiable, each with a reason that names a mechanism — the
declaration is present, and no conjunct is silently unstated. Round 93's checker closes
that hole with the *count* predicate, and the honest lesson is that **the per-row audit
alone does not close it**. The draft therefore splits the requirement in two: 159 is the
audit-of-the-manifest rule (the checker must exist and must be able to fail), and the
count is carried by the claim's own frozen predicate (`falsifiable=17`, `unfalsifiable=2`,
`findings=0`) — which is already in `plans/round-93.plan.md` and `.ufo/waves/round-93/claims.json`.
The draft text below states both, so a reader of QUALITY.md alone learns that the
manifest's *shape* is checked per row and its *bulk* is checked by count.

--- BEGIN INTEGRATION TEXT ---

## Criteria appended — round 93

159. A counter's own statement of what it measures is a claim about the instrument, and
    a claim about an instrument is audited by a checker that can fail — not by a
    self-assessment that is read and believed. When a round declares which of a
    counter's conjuncts are falsifiable by a committed battery state and which are
    unfalsifiable, that declaration is committed as a **manifest**, and the manifest is
    checked by a committed checker against the counter's own conjunct-key list read from
    the pinned instrument revision, so that a key the counter prints and the manifest
    omits, a key the manifest names and the counter does not print, a receipt that does
    not move its conjunct, and an unfalsifiable row whose reason is too short or names
    no seal, pin or mechanism are each **findings**, not remarks. The checker is itself
    proven able to fail on a case that must produce a finding and to produce none on the
    clean case, and its six-case selftest is a committed receipt. The manifest's *bulk*
    is a separate obligation from its per-row soundness: a manifest that declares every
    conjunct unfalsifiable, each reason naming a mechanism, satisfies every per-row
    rule and is still a false self-assessment, so the count of falsifiable rows is part
    of the claim's frozen predicate and not a report line — the all-unfalsifiable
    manifest is rejected by the frozen count (`falsifiable=17` of 19), not by the
    per-row checker, and the receipt that shows it is kept beside the clean one.
    Able to fail: `tools/conjunct-disposition.py --selftest`
    (`.ufo/evidence/round-93/pre-freeze/c2-selftest.out`,
    `DISPOSITION_SELFTEST: 6/6 pass`, exit 0 — the `missing-row`, `no-flip`,
    `reason-too-short`, `unknown-key` and `no-receipt` cases each produce a finding and
    the `clean` case produces none); the all-unfalsifiable manifest
    (`.ufo/evidence/round-93/pre-freeze/c2-cheat-all-unfalsifiable.out`:
    `DISPOSITION rows=19 falsifiable=0 unfalsifiable=19 findings=0`, exit 0 from the
    checker, refused by the frozen count); the base refusal
    (`.ufo/evidence/round-93/pre-freeze/c2-nowork-base.out`,
    `DISPOSITION_SETUP counter-absent-at-rev`, exit 2, at base `4a7e259b`); and the
    per-row audit over the committed battery receipts produced by
    `.ufo/evidence/round-93/c1/controls-v93.py`
    (`DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`, exit 0, over the
    35 receipts in `.ufo/evidence/round-93/pre-freeze/controls/`).

--- END INTEGRATION TEXT ---

## Facts the draft rests on (each re-derived by this seat)

| Fact | Evidence | How observed |
|---|---|---|
| The checker's selftest is 6/6 and each failing case produces a finding | `.ufo/evidence/round-93/pre-freeze/c2-selftest.out` | re-run: `python3 -I tools/conjunct-disposition.py --selftest` → `DISPOSITION_SELFTEST: 6/6 pass`, exit 0 |
| The clean run over the committed receipts is `rows=19 falsifiable=17 unfalsifiable=2 findings=0`, exit 0 | the same command at `--rev 9bf52b03` (the manifest's own commit) | re-run; exit 0 |
| The base refuses at setup | `.ufo/evidence/round-93/pre-freeze/c2-nowork-base.out` | re-run at base `4a7e259b`: `DISPOSITION_SETUP counter-absent-at-rev`, exit 2 |
| The all-unfalsifiable manifest passes the per-row checker | `.ufo/evidence/round-93/pre-freeze/c2-cheat-all-unfalsifiable.out` (`falsifiable=0 ... findings=0`) | re-derived independently in `R93SC1-disposition-probe.py` case D: `findings=0`, `report()` exit 0 |
| The receipts the manifest names are the ones the battery driver wrote | `.ufo/evidence/round-93/pre-freeze/controls/C1-summary.txt` (35 rows, all `MATCH`) | read; each `state` row's receipt exists under `.ufo/evidence/round-93/pre-freeze/controls/` and prints the conjunct `false` |

### Two limits the draft states rather than hides

1. **The per-row checker alone accepts the all-unfalsifiable manifest.** Probe case D
   (`R93SC1-disposition-probe.out`): 3 of 3 rows `unfalsifiable`, each reason naming a
   mechanism, `findings=0`, `report()` exit 0. That is why the criterion's last sentence
   puts the count in the frozen predicate instead of leaving it to the checker.
2. **The checker binds a manifest row to the conjunct VALUE in a receipt, not to the
   receipt's provenance.** Probe case C: a receipt whose `counter_sha=` is all zeros and
   whose `clone_rev=` is a deadbeef digest is still accepted (`findings=0`), because
   `check()` reads only the receipt's `C1_CONJUNCTS` line. The receipts' own provenance
   is bound by the *driver* (which writes `counter_sha=` and `clone_rev=` into every
   receipt) and by the committed `.ufo/evidence/round-93/pre-freeze/controls/C1-summary.txt`,
   not by the disposition checker. The draft does not claim the checker verifies
   provenance; a future criterion may.

### The `--rev` the counting command must use

The frozen plan's C2 counting command is
`python3 -I tools/conjunct-disposition.py --lane <lane> --rev REV`. The manifest
(`tools/conjunct-disposition.json`) was committed at `9bf52b03`, **after** the instrument
revision `855f0c1c`, so `--rev 855f0c1c` prints `DISPOSITION_SETUP manifest-absent-at-rev`
and exits 2. The revision that yields the frozen line is `9bf52b03` or later (`978f04bc`,
`d5bcf1db` — verified: all three print `rows=19 falsifiable=17 unfalsifiable=2
findings=0`, exit 0). The counter blob the checker reads is byte-identical at
`9bf52b03` and at `855f0c1c` (sha256 `18903602aa040b7e…`), so the conjunct key list is
the frozen one either way; what differs is only the presence of the manifest. **The L1
should record the revision the C2 receipt was produced at**, or amend the plan's
counting command to name it.

VERDICT: drafted
TOOLS: none
