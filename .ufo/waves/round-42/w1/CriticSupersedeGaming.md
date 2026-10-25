# CriticSupersedeGaming — round 42 wave 1

Scope: m10 SUPERSEDE rule in `.ufo/evidence/round-42/calibration/measure.py`
(`receipt_audit`, lines 187–221; `Repo.resolves`, lines 109–110).
Read-only seat: no lane edits except this report. No tools installed.

## Verdict

The supersede mechanism is **mechanically sound against its own frozen letter but
content-blind**: coverage eligibility (measure.py:208–213) requires the superseding
receipt's own `present` assertions to agree with the tree, and agreement is defined as
bare path resolution (`git cat-file -e <rev>:<path>`). Therefore a stale "absent"
claim can be silenced by superseding it with `present=true` for **any** path that
resolves — an empty file, an unrelated stub, even a directory — and m10 never sees it.
A superseder that lies (flips to a value the tree contradicts) IS caught and cannot
cover. Append-supersede is the right structure for an append-only evidence tree; the
defect is the validator, not the append.

## Demonstrated scenarios (scratch clone `/tmp/tameshi-r42-CriticSupersedeGaming-1`, commit `4210a4874`, built `git clone --shared` from lane HEAD 322b5cd; fixtures committed only there)

Run: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/calibration/measure.py --lane /tmp/tameshi-r42-CriticSupersedeGaming-1 --rev HEAD --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
→ `C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=7 m11=0 total=7 records=3 …`.
The 7 counted mismatches: 1 live residual (round-41 `ResidualReceipts.md`), 1 baseline,
2 flip-a, 2 flip-b, 1 flip-c. **The three spoof pairs below produced zero m10 lines.**

| Fixture (in `.ufo/waves/scratch-gaming/`) | Receipt pair | Tree at path | m10 count for the pair |
|---|---|---|---|
| empty/ | r: `present=false` w/empty.md → s: supersedes, `present=true` | w/empty.md exists, **0 bytes** (`git cat-file -s HEAD:w/empty.md` → 0) | **0 (spoof clears the stale claim)** |
| diff/ | r: `present=false` w/stub.md → s: supersedes, `present=true` | w/stub.md exists, 33-byte unrelated placeholder | **0 (spoof clears)** |
| dir/ | r: `present=false` `w/` → s: supersedes, `present=true` | `w/` is a **tree** (`git cat-file -t HEAD:w/` → tree) | **0 (spoof clears)** |
| baseline/ | r: `present=false` w/real.md, no supersede | w/real.md exists, substantive | 1 (stale counted) |
| flip-a/ | r: `present=false` w/flipa.md → s: supersedes, repeats `present=false` | file exists | 2 (both counted) |
| flip-b/ | r: `present=true` w/missing.md → s: supersedes, repeats `present=true` | path absent | 2 (both counted) |
| flip-c/ | r: `present=true` w/right.md (R was **right**) → s: supersedes, flips `present=false` | file exists | 1 (only s counted; R had no mismatch; s cannot cover) |

Controls: `--selftest` passes 9/9 (T2_superseded_clears OK — legitimate repair path works);
base rev `c77c2b7` scores m10=1 (before/c1-at-base.stdout); `c1-do-nothing.stdout` shows
the live residual mismatch persists with records=6.

## What this means

1. **Gaming surface confirmed.** A superseding receipt can silence a stale absent-claim by
   pointing at a vacuous/coincidental path object. The claim "self-assessment records agree
   with observed repo state" is then satisfied at the byte level while the report substance
   is absent. The validator cannot tell "present" from "path resolves".
2. **Lying supersedes are caught.** Flipping to a tree-contradicting value makes the
   superseder itself stale, adds a new m10, and fails to cover (flip-a/b/c). So the escape
   requires the disputed path to *actually resolve*; it is not a free "flip anything" hole.
3. **Superseding a right receipt** is a no-op for m10 when re-assertions stay true
   (R had no mismatch; cover adds nothing), and is caught when the flip is false (flip-c).

## Append vs regenerate

For an append-only evidence tree, **supersede-as-new-receipt is the correct structure**:
regenerating in place would rewrite committed evidence and break provenance (the round-41
residual receipt and the round-42 records pattern depend on immutable prior receipts).
The flaw is not append vs regenerate; it is that cover eligibility validates only path
resolution, never substance or identity.

## Smallest safe correction

Within `measure.py` only (needs a post-freeze amendment since it tightens the m10 letter):
- Resolve "present" as a **non-empty blob**: for every `present=true` assertion, require
  `git cat-file -t <rev>:<path>` == `blob` and `git cat-file -s <rev>:<path>` > 0. Apply
  it consistently to both sides (a receipt's own assertions and the cover-eligibility
  check) so an empty file is neither "present" for coverage nor "absent" for staleness.
  This kills the empty-file and directory spoofs. Cost: a genuinely 0-byte report would
  now flag — acceptable, a 0-byte `.md` cannot substantiate presence.
- The "different but non-empty file" spoof is not closable mechanically without a content
  anchor (e.g. expected sha256 in the receipt). That is a schema/contract change beyond
  the counter; record it as residual risk rather than patch into measure.py.

## Checks not performed

- No run against the lane tip as a measurement (per constraints); only base/freeze revs
  and the scratch clone.
- The other `supersedes` occurrences in the repo are narrative strings in evidence JSON
  (round-12/13/14) or `evidence-disposition.py` rows, not structured wave-receipt pairs;
  `receipt_audit` is the only mechanical validator of this rule.
