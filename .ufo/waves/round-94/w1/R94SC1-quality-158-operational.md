# R94SC1 — draft block 2: a QUALITY.md criterion for QUALITY 158's operational half

**For:** TameshiR94 (L1), for integration into `corpus/QUALITY.md`.
**Lane mode:** read-only; this seat wrote nothing under `corpus/`.

## Where the criterion goes

`corpus/QUALITY.md` ends with criterion **167** under the section
`## Criteria appended — round 94` (line 2631 opens the section; 167 is at line 2668).
The next free number is **168**; the L1 owns the final number and the placement.

The item asks for "QUALITY 158's operational half — a conjunct-disposition manifest is a
claim about the instrument and must be audited by a checker that can fail, citing
`.ufo/evidence/round-93/c1/controls-v94.py` and `.ufo/evidence/round-94/conjunct-disposition-v94.py`".

**Two paths in the item do not exist; this draft cites the real ones.** Verified:

| item's path | status | real path used here |
|---|---|---|
| `.ufo/evidence/round-93/c1/controls-v94.py` | **does not exist** | `.ufo/evidence/round-94/c1/controls-v94.py` (the round-94 battery driver) |
| `.ufo/evidence/round-94/conjunct-disposition-v94.py` | **exists** | same (the round-94 checker) |

## Why a new criterion and not an edit to 160

Criterion **160** (round 93) already states the operational half: the manifest is audited
by a checker that can fail, and the counts are part of the claim. Criterion **166**
(round 94) already states the reason test: an `unfalsifiable` reason must name a
concrete battery state or a pin digest.

**Neither covers the binding this round's own wave found.** The round-94 checker
audits a manifest — but *which* manifest it audits is a constant in the checker
(`MANIFEST = …`), and round 94's first two checker revisions named the **round-93**
manifest path. The reason test therefore ran against the wrong bytes: the round-94
manifest's `canary` and `unstable0` reasons were never examined, and the run reported
`findings=0` on the round-93 manifest — a green line about a file the round never
claimed. The plan's amendment A1 records the repair ("rev 1/2 read
`tools/conjunct-disposition.json`, the round-93 manifest, so the reason test ran on the
wrong bytes"); the criterion is missing because no criterion states the binding.

The gap is not yet covered anywhere in `corpus/QUALITY.md`: a search for
`wrong manifest`, `default manifest`, `another round`, `names the manifest`,
`manifest it read` and `which manifest` returns nothing.

### The defect, re-derived by this seat

At the frozen instrument revision `7084358c` the checker's own bytes say:

```
COUNTER  = ".ufo/evidence/round-94/c1/measure-v94.py"
MANIFEST = "tools/conjunct-disposition.json"          # the round-93 manifest
RECEIPTS = ".ufo/evidence/round-94/pre-freeze/controls"
```

The two candidate manifests are different files with different digests at that
revision:

```
tools/conjunct-disposition.json              sha256 2882a42d20977916d81817098caa918e44ac723e63712f53ea8164fbb8db6b13   (round-93)
.ufo/evidence/round-94/conjunct-disposition.json  sha256 81e4a14bf939c8e8a371d3a9c1fb42f4165fa312bc33d9a0341eed0d1f7d81db   (round-94)
```

and the rev-1 checker run against each prints a **byte-identical receipt**
(`R94SC1-manifest-binding.out`, saved beside this file):

```
rev1  + r93man  exit=0  DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0
rev1  + r94man  exit=0  DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0
REV1_RECEIPT_IDENTICAL_ACROSS_MANIFESTS true
REV1_RECEIPT_MENTIONS_MANIFEST 0
```

The receipts are identical because the receipt names the counter's sha256 and the
conjunct keys, and **never names the manifest it read** (`grep -ci manifest` on the
receipt → `0`, for rev 1 and rev 3 alike). Two different manifests, one
indistinguishable green line.

The two manifests are not interchangeable, and only one of them is this round's claim.
The **round-94** checker (rev 3) rejects the round-93 manifest with `findings=2` and
rejects the mechanism-word cheat with `findings=20`; the **round-93** checker (rev 1)
accepts the same cheat manifest with `findings=0`, so only the `--min-falsifiable 17`
floor rejected it:

```
rev3  + r93man  exit=1  DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=2
rev3  + r94man  exit=0  DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0
rev3  + cheat   exit=1  DISPOSITION rows=19 falsifiable=0 unfalsifiable=19 findings=20
rev1  + cheat   exit=1  DISPOSITION rows=19 falsifiable=0 unfalsifiable=19 findings=1
```

--- BEGIN INTEGRATION TEXT ---

## Criteria appended — round 94

168. A disposition checker is bound to the manifest of the round it audits, and its
    receipt names the manifest it read. A checker that audits *a* manifest is not a
    checker that audits *this round's* manifest: the audited path is a constant in the
    checker's own bytes, so a wrong constant makes the audit run over another round's
    rows while printing the same green line, and the reason test never examines the
    rows the claim froze. Round 94's checker revisions 1 and 2 named
    `tools/conjunct-disposition.json` — the round-93 manifest — so the
    round-94 manifest's `canary` and `unstable0` reasons were never audited and the run
    reported `findings=0` over the wrong file. The receipt must therefore carry the
    audited manifest's path and digest, so that a receipt for one manifest cannot be
    byte-identical to a receipt for another, and the checker's default manifest path
    must be the round's own. Able to fail: the same rev-1 checker bytes
    (`8ec7924ea1d57997bdba1770317a6ff44d6c3bacbb55d15e4a4742292c00b6eb`) print a
    **byte-identical** receipt `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2
    findings=0` (exit 0) against
    `.ufo/evidence/round-94/conjunct-disposition.json` (sha256 `81e4a14b…`) and against
    `tools/conjunct-disposition.json` (sha256 `2882a42d…`), while the round-94 checker
    (rev 3, sha256 `6d4d270644b036cdd7106a5ab24be05b5d05ed01919f7f9ce24090977bdf9b7e`)
    rejects the same round-93 manifest with `findings=2` and the mechanism-word cheat
    with `findings=20`
    (`.ufo/evidence/round-94/pre-freeze/c2-cheat-mechanism-word.out`); the witness is
    `.ufo/evidence/round-94/c1/controls-v94.py`, whose receipts
    (`.ufo/evidence/round-94/pre-freeze/controls/`) are what the checker audits, and
    `.ufo/evidence/round-94/conjunct-disposition-v94.py`, which must read that round's
    own manifest. (`lessons/round-94.md` M4; `plans/round-94.plan.md` A1.)

--- END INTEGRATION TEXT ---

## Facts the draft rests on (each re-derived by this seat)

| Fact | Evidence | How observed |
|---|---|---|
| The frozen rev-1 checker's default manifest is the round-93 file | `git cat-file blob 7084358c:.ufo/evidence/round-94/conjunct-disposition-v94.py` line 37 → `MANIFEST = "tools/conjunct-disposition.json"` | read |
| The rev-3 checker's default is the round-94 file | `git show HEAD:.ufo/evidence/round-94/conjunct-disposition-v94.py` line 37 → `MANIFEST = ".ufo/evidence/round-94/conjunct-disposition.json"` | read |
| The two manifests are different bytes | digests `2882a42d…` (tools/) vs `81e4a14b…` (round-94) at `7084358c` | `git cat-file blob … \| sha256sum` |
| Rev 1 gives a byte-identical receipt for either manifest | `R94SC1-manifest-binding.out` | re-ran the rev-1 blob with `--manifest` set to each path; `diff` empty |
| The receipt never names the manifest | `grep -ci manifest` on the receipt → `0` | counted |
| The round-93 manifest is *not* interchangeable with the round-94 one | rev-3 checker on `tools/conjunct-disposition.json` → `findings=2`, exit 1 | re-ran |
| The mechanism-word cheat is refused by rev 3 | `c2-cheat-mechanism-word.out` → `findings=20` (19 reason findings + the floor) | read at HEAD |
| Rev 1 accepted the same cheat | `c2-cheat-mechanism-word.rev1.out` → `findings=0` | read at HEAD |
| No criterion covers the binding | `grep -nE 'wrong manifest\|default manifest\|another round\|names the manifest\|manifest it read\|which manifest' corpus/QUALITY.md` → no match | searched the committed file |

### Two limits this draft states rather than hides

1. **The receipt naming is a proposal, not a repair.** Rev 3 (the operative checker)
   still prints `DISPOSITION_INSTRUMENT sha256=…` — the counter's digest — and still
   does not name the manifest. The draft therefore states the binding as a rule for the
   next revision; it does **not** claim the operative checker satisfies it. The
   criterion's "Able to fail" witness is therefore drawn from rev 1 and rev 3's *outputs*
   (which are committed), not from a hypothetical repair.

2. **The floor is a second line of defence, not the fix.** Rev 1 with the mechanism-word
   cheat manifest prints `findings=0` and is rejected only by `--min-falsifiable 17`
   (`falsifiable=0 < 17`). A floor rejects a manifest that declares nothing falsifiable;
   it cannot tell whether the rows it audited were this round's. The criterion is about
   the binding, and the floor stays where criterion 166 put it.

## What the L1 should decide

- **The number.** Drafted as `168`; the L1 owns the final number and whether it lands
  under `## Criteria appended — round 94` or a new section.
- **Whether 160 or 166 should be amended instead.** This draft adds a third statement
  of QUALITY 158's operational half rather than editing either. The L1 may prefer to
  fold the binding sentence into 160 (which is the criterion that owns the operational
  half) and leave the number sequence alone.
- **The citation the item asked for.** `.ufo/evidence/round-93/c1/controls-v94.py` does
  not exist; the draft cites `.ufo/evidence/round-94/c1/controls-v94.py`. The L1 should
  confirm the intended path — the item's path is a round-93 directory holding a
  round-94 filename.

VERDICT: drafted
TOOLS: none
