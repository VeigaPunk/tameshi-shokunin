# CritTrends — independent expansion / quality / discernment verdicts, round 43

Scope: build my own trend verdicts from **committed bytes only** and say which of
the L1's likely verdicts die if the trend-verdicts section is written without a
named non-author check. No counter was run at the records commit; every number
below is a grep/sha256/jq over committed bytes or the read-only staged package.

Commits judged: records `c5335c7` through HEAD `b510ad1` (freeze A11). The lane
moved during my run (A11 landed mid-audit); everything below is stated at HEAD.

## My verdicts

| Trend | Verdict | Short reason |
|---|---|---|
| **expansion** | **harmed** | One net-new admitted entry on genuinely new ground and one capability row exist — but the admitted entry fails the bar it was admitted under (QUALITY criterion 10: no `verified-at:`/`recheck:`), which is LEARNING.md's own `harmed` clause. |
| **quality** | **unchanged** | No existing entry was re-verified, deepened, or superseded; the stale-anchor correction did prevent harm but a correction is not an improvement. |
| **discernment** | **unchanged** | Two lesson-backed criteria landed, but the outside spot-check of this round's admits/rejects does not exist (`corpus/lessons/round-43-verifier-spotcheck.md` absent); the round-1..17..42 chain of verdict files is broken. `improved` is unavailable to the lane. |

## Expansion — harmed (the strongest counterexample wins over a clean map)

What goes right, from committed bytes:

- Net-new admitted entry `corpus/knowledge/r43-survivor-resolution-rule.md`
  (105 lines) on ground the map did not hold — `corpus/README.md:544-555` adds the
  coverage row in the same commit and states the move ("F1's outcome vocabulary
  gains the survivor side … the equivalence problem itself").
- `source:` line cites S089 (mined), S159 (mined), S155 (mined), S158 (mined) —
  all four rows carry `mined` in `corpus/SOURCES.md`. LEARNING.md's citation
  requirement is met.
- One capability admitted to `SCORECARD.md` ("staged-id adoption guard",
  line 2074) — the second expansion observable.
- New kind of source: S159 is the registry's first Wikipedia row
  (`grep -c wikipedia corpus/SOURCES.md` → 1, the new row itself).

What defeats `improved` — an admitted entry fails the bar it was admitted under:

**F1 — `corpus/knowledge/r43-survivor-resolution-rule.md` has no `verified-at:`
and no `recheck:` lines.** QUALITY criterion 10 (`corpus/QUALITY.md:27-29`) is
live and never superseded: "A new `knowledge/` entry opens with `source:`,
`verified-at:` and `recheck:`". Repro:

```
$ grep -cE '^(verified-at|recheck):' corpus/knowledge/r43-survivor-resolution-rule.md
0
$ for f in $(ls -t corpus/knowledge/*.md | head -8); do
    printf '%s va=%s rc=%s\n' "$f" "$(grep -c '^verified-at:' $f)" "$(grep -c '^recheck:' $f)"; done
# r43 … va=0 rc=0 ; every one of the 7 preceding entries va=1 rc=1
```

The entry's own `source:` line is also the weakest of the round: bare S-ids with
no anchor, where r42's entries name the snapshot and sha256 per source
(`r42-attribute-and-outflag-destinations.md:1-4`).

**F2 — the admitted capability's pinned bytes are superseded and its receipt
does not exist.** `SCORECARD.md:2074` describes the A7/A10 tool ("dedupe … under
any URL form", "every fresh target at or above the safe floor") but pins
`tools/staged-id-guard.py` @ `8140945a…`. That sha is the 697d2f1 freeze's blob;
the pinned bytes at the freeze of record are `2e8f2e89…`
(`contract.json` `frozen_tools`). Repro:

```
$ for c in $(git log --format=%h -- tools/staged-id-guard.py); do
    printf '%s ' $c; git show $c:tools/staged-id-guard.py | sha256sum | cut -c1-8; done
# 3aee2c0 2e8f2e89   ← freeze of record
# 273c047 e219007f
# 114ffac 365bf958
# 5cd2154 efa5f129
# 697d2f1 8140945a   ← the pin the capability row cites
$ git ls-tree -r --name-only HEAD -- .ufo/evidence/round-43/after/   # (empty)
```

The row's evidence pointer is "deciding receipt `C3_R43: … C3_R43_PASS=true` at
the round-43 measured commit" — no file under `.ufo/evidence/round-43/after/` is
committed at HEAD, so the admission is asserted before its evidence exists. The
deciding run is legitimately still ahead, but a capability row whose cited
receipt does not resolve is not yet "admitted" in the observable sense.

So the round's own records answer the LEARNING.md `harmed` clause twice:
the entry fails criterion 10 outright, and the capability's pinned bytes do not
implement the behaviors the row claims. `improved` would have been reachable
with a two-line field addition and a repin — the smallest correction is
mechanical.

## Quality — unchanged

The observable is entries re-verified, deepened, or superseded, plus
`verified-at` freshness. Committed evidence:

- Nothing re-verifies, deepens, or supersedes an existing knowledge entry. The
  S089 **registry** row was re-opened (`corpus/lessons/round-43.md:39-47`), but a
  SOURCES row is not a knowledge entry, and its `recheck:` interval was left
  unchanged. `verified-at` on every pre-existing entry is untouched
  (`grep '^verified-at:' corpus/knowledge/*.md` — only the older dates).
- Harm was *prevented*, not produced: `ScribeLessonGate.md` D1 caught the
  lesson's "byte-identical to S089's anchor" sentence while the snapshot is
  `79f6501a…` and the anchor is `bc572676…`; A11 (`b510ad1`) fixed both the
  lesson (`corpus/lessons/round-43.md:44-47`, now "drifted") and the knowledge
  entry. A wave-1 self-correction is evidence the instrument works, not a
  quality gain.
- The S089 anchor staleness is left *marked and deferred*, not unmarked —
  the lesson names it and routes it to round 44, so LEARNING.md's `harmed`
  clause is not tripped on the stale digest.

Nothing moved up; nothing was left falsely marked down → `unchanged`.

## Discernment — unchanged; `improved` unprovable

- Criteria 83 (survivor classified, never relabelled) and 84 (self-assessment
  count uses the census pattern) are appended (`corpus/QUALITY.md:1048-1105`),
  each citing `corpus/lessons/round-43.md` and each carrying a falsifier. That
  clears LEARNING.md's "criterion with no lesson" hazard.
- But the outside spot-check the trend is judged by does not exist in committed
  bytes: `corpus/lessons/round-43-verifier-spotcheck.md` is absent (`ls
  corpus/lessons/ | grep 43` → only `round-43.md`), and the round-43 `## Gate`
  carries no spot-check line at all — not even the "NOT performed" recording
  round 1 left (`corpus/lessons/round-1.md:132-137`). The convention is an
  unbroken `round-38..42-verifier-spotcheck.md` chain; this round breaks it.
- The wave-1 and wave-2 seats that produced A4–A11 are lane-dispatched — "a
  subagent the lane dispatched is still the lane" (LEARNING.md §Discernment is
  checked from outside). Their agreement cannot substitute.
- Nothing is left unlearned: the one *outside* disagreement available (the
  ScribeLessonGate drift finding, lane-internal) was already converted into
  corrected records; the mistakes table is grounded. `unchanged`, not `harmed`.

## Which L1 verdicts are unprovable without a named non-author check

Written with none, the following are dead on arrival:

1. **`discernment: improved`** — definitionally unprovable. LEARNING.md admits
   it "only through this gate: a named non-author reviewer judging the change
   better, with reasons on record." Round 42's own `improved` verdict stood on
   exactly such a file (`round-42-verifier-spotcheck.md:86-98`, non-author
   `hyaku closure (non-author integrator, @m_flash)`). Without a committed
   `round-43-verifier-spotcheck.md` or operator record, the lane may write
   `unchanged` at best.
2. **Any `unprovable-but-better` line** — same clause: admitted only through the
   named non-author judgment. Unprovable by construction.
3. **`quality: improved`, if claimed via wave-1/wave-2 reviewer findings** —
   those reviewers are lane-dispatched; their fixes cannot carry the verdict.
   Provable only on committed bytes, and committed bytes (above) support
   `unchanged`, not `improved`.

What does **not** need the non-author: `expansion` and `quality` verdicts in
their own right are observable from committed bytes — but expansion's honest
verdict is `harmed` (F1/F2), so the non-author check is not what saves or kills
it.

## Load-bearing record defects (evidence for all three verdicts)

| # | Defect | Evidence | Repro |
|---|---|---|---|
| D1 | Knowledge entry missing `verified-at:`/`recheck:` (QUALITY criterion 10, unsuperseded) | `corpus/knowledge/r43-survivor-resolution-rule.md:1-3` | `grep -cE '^(verified-at|recheck):' …` → 0 vs 1 on all prior entries |
| D2 | Capability row pins superseded tool bytes; deciding receipt absent | `SCORECARD.md:2074` (`8140945a…` = 697d2f1 blob; pinned `2e8f2e89…`) | `git log --format=%h -- tools/staged-id-guard.py` + `sha256sum`; `git ls-tree HEAD -- .ufo/evidence/round-43/after/` empty |
| D3 | All three published counting commands name the superseded A2/A3 freeze | `SCORECARD.md:2059-2061` `--freeze 17f6ef0c…` | at that freeze, `running` (on-disk, now `b56a34d7/97609511/ae66342d`) ≠ pins (`ad7ecf8c/092c76cd/6278edcd`) → `self_pin=0`; the commands as printed cannot produce the target line |
| D4 | Contract narration again names a stale freeze of record | `contract.json:7` "the freeze of record is 114ffacd…" with chain ending at A6/A7 | `python3 -c 'json.load(...)["amendments"][-1]["id"]'` → `A11`; the same defect class A8 was created to fix has recurred |
| D5 | LOG repeats the stale freeze and a superseded amendment count | `LOG.md:2221-2225` "Contract frozen at `17f6ef0c…` (`amendments` A1–A3 … A4 …)" | `grep -n 17f6ef0c LOG.md` vs `contract.json` amendments A1–A11 |
| D6 | Two committed records give different collision/held counts | `corpus/SOURCES.md:454` "6 collisions S153–S158, 2 held" vs `corpus/lessons/round-43.md:82-85` "7 collisions S153–S159, 3 held" | independent recount over committed bytes + read-only staged package: 7 ids, 3 held (S153→S105, S154→S106, S159→S155) — the lesson is right, SOURCES mixes pre-append numbers into a post-append sentence |
| D7 | The deciding-run receipts the claims' own evidence cells name are absent | `SCORECARD.md:2059-2061` "see the after subsection"; `.ufo/evidence/round-43/after/` empty at HEAD | `git ls-tree HEAD -- .ufo/evidence/round-43/after/` |

D3 and D6 are the calibration point: the round's own C2 claim measures
record-vs-tree agreement in seven classes, and none of the seven can see a
stale counting command or two records that disagree with each other — the two
defects this very round committed.

## Impacted axes and smallest safe correction

- **calibration** (C2): the records agree with the tree in the seven measured
  classes, but the class set is narrower than the claim's own wording; D3–D6 are
  live record defects a C2-class reader finds by inspection.
- **depth** (C1): unaffected by these verdicts; the counter pins and the kill
  binding are the deciding run's problem, not the trend section's.
- **operability** (C3): the capability row's stale pin (D2) is a record defect
  on the admission, not on the tool.

Smallest safe corrections, all mechanical: add `verified-at:`/`recheck:` to the
knowledge entry (restores `expansion: improved`); repin `SCORECARD.md:2074` to
`2e8f2e89…` and the counting commands to the freeze of record (`b510ad1`, A11);
re-correct `contract.json:7` for A8–A11; restate `corpus/SOURCES.md:454` as
post-append 7/3; then hold `discernment` at `unchanged` in the report and let
the non-author spot-check land its own file. If any of those go unrepaired
before the deciding run, the honest trend line is
`expansion: harmed; quality: unchanged; discernment: unchanged` — and
`discernment: improved` is unprovable in every case without a named non-author.
