# MutC2m10Superseder — m10 superseder attack (round 43, wave 2)

Seat: mutation-tester. Lane: `tameshi-shokunin`. Read-only on the lane; the only lane
write is this file. Counters were run only at `--rev 487b8f0d` (base) and
`--rev 3aee2c07` (freeze) / at scratch commits. **No run at `c5335c70`** — the deciding
run stays the L1's.

## Verdict

**`m10` counts B, not A.** In the assigned two-receipt scratch repo the frozen counter
prints `m10=1` and the single hit is B. A's stale `present:false` is dropped, and it is
dropped although B never re-asserts A's claim: B asserts a different path. So the
supersede rule **is a blanket amnesty** for the superseded receipt.

The superseder is **not** above the rule: B's own false `present:true` is graded and
counted. Amendment A6 ("the superseding receipt's own claims were excluded from m10")
holds under test.

The amnesty is claim-blind, and that is exploitable to a green `C2_R43_PASS=true` with
false presence claims in the tree (fixtures v3–v6 below). The live record set does not
currently exploit it.

## Fixture v1 — the assigned pair

Scratch repo `/tmp/tameshi-r43-w2-MutC2m10Superseder-/v1`, commit
`2b61bddf6407f688841bd356be2ff67f40da6e43`.

`A.json` (sha256 `69d9b4f92f6a4b87…`) — the file it denies is in the tree:

```json
{ "receipt": "A", "report": ".ufo/waves/round-43/A.md", "present": false }
```

`.ufo/waves/round-43/A.md` exists (verified with `git ls-tree -r`).

`B.json` (sha256 `66ee582e6b845512…`) — supersedes A, and asserts a false presence:

```json
{ "receipt": "B", "supersedes": ".ufo/waves/round-43/A.json",
  "report": ".ufo/waves/round-43/B-missing.md", "present": true }
```

`.ufo/waves/round-43/B-missing.md` is absent. Command (counter copied byte-identical
into the scratch repo at `.ufo/evidence/round-43/calibration/measure.py`; contract pinned
to its sha256 `97609511…`):

```
python3 <scratch>/.ufo/evidence/round-43/calibration/measure.py \
    --lane <scratch> --rev 2b61bdd --freeze 2b61bdd
```

Output (exit 1):

```
C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=1 m11=0 m12=0 m13=0 total=1 records=2
sources_rows=2 standing=2 receipts=2 revisions=0 ... C2_R43_PASS=false
first=m10:.ufo/waves/round-43/B.json_present=true_.ufo/waves/round-43/B-missing.md
```

`receipts=2` proves both receipts were parsed; only B was graded. A's contradiction is
discarded at `measure.py:281` (`if receipt in superseded: continue`) with no test that
any superseder re-asserted `.ufo/waves/round-43/A.md`. B never does.

## The amnesty is unconditional (v2–v6)

Same counter, same construction; only the receipts change. `m10` is the count printed by
the frozen counter; `PASS` is `C2_R43_PASS`.

| fixture | commit | modelled defect | m10 | PASS |
|---|---|---|---|---|
| v1 | `2b61bdd` | assigned pair: stale A + false B | 1 (B) | false |
| v2 | `fdfff4e` | identical to v1 but `supersedes` names `A.md`, not `A.json` | 2 (A and B) | false |
| v3 | `5e49adc` | A carries two false claims; B re-asserts only the first, truthfully | 0 | **true** |
| v4 | `48619ca` | A false, B false (`present:true` for a missing file); C supersedes B and asserts nothing | 0 | **true** |
| v5 | `634fbf1` | one receipt listing **itself** in `supersedes`, with a false `present:true` | 0 | **true** |
| v6 | `b9bdad7` | A and B mutually name each other, both asserting false `present:true` | 0 | **true** |

* v3 is the exact "blanket amnesty" reading: B re-asserts `.ufo/waves/round-43/A.md` as
  `present:true` (true) and says nothing about `docs/never-asserted.md`; A's false claim on
  the second path vanishes with A. `receipts=3`, `m10=0`.
* v4 shows transitivity: a claim-less successor launders every claim of its predecessor.
  The superseded false `present:true` is not even in the count.
* v5 shows the game is one field: a receipt can exempt **itself** by naming its own path.
  No second file is needed.
* v6 shows the same without self-reference: two receipts launder each other, and because
  each re-asserts a *different* path, even a re-assertion-aware rule would catch it — a
  blanket one cannot.

## Live lane: the rule is load-bearing exactly once, and legitimately

Forensic re-run of `m10_receipts` over the real tree at base and freeze (read-only,
`git ls-tree`/`git show` only). Both revs: 17 presence claims, 3 top-level `supersedes`
declarations, 3 superseded receipt paths, `m10=0`, and **one** suppressed contradiction:

```
.ufo/waves/round-41/residual/receipt.json  present=false
    .ufo/waves/round-41/residual/ResidualReceipts.md      # file IS in the tree
superseded by .ufo/waves/round-42/supersede/round-41-residual-receipt.json
```

That suppression is legitimate: the superseder's `reason` names this exact seat and it
re-asserts all eight seats, `ResidualReceipts` as `present:true`, which agrees with the
tree. The second live superseder (`.ufo/waves/round-42/supersede/round-20-outcomes.json`
→ `.ufo/waves/round-20/outcomes.json`) adds no `present` claims, so it suppresses nothing.
The third declaration (`.ufo/waves/round-21/original-outcomes2-corrected.json`) carries a
prose string in `supersedes`; it resolves to no tree path and is inert.

So at base and freeze, `m10=0` is not hiding a contradiction in this record set. The gap
below is latent, not materialised.

## Defect

`measure.py:269-282` (`m10_receipts`):

```
269    # Only the superseded receipt is history. The superseding receipt's own
270    # claims are the authority and are checked like any other (F1).
...
279            # A receipt named in another receipt's `supersedes` is history: the
280            # superseding receipt re-asserts its claims against the tree.
281            if receipt in superseded:
282                continue
```

Line 280 and the module docstring (`measure.py:22-23`, "the superseding receipt carries
the claims") assert a re-assertion relation. Nothing in the function checks it: the test
is receipt identity alone (line 281), one flag for every claim in the file. Any receipt
naming another — itself included (v5), or naming it and asserting nothing (v4) — deletes
that receipt's entire claim set from the audit.

The contract licenses this verbatim, so the code matches its sentence and **the sentence
is the weaker artifact** (`contract.json`, `claims.C2.classes.m10`):

> "no presence receipt under .ufo/waves asserts present/absent contrary to the tree; only
> a receipt named in another receipt's `supersedes` is skipped, and the superseding
> receipt is graded"

The first clause is a universal about the tree; the second clause authorises dropping
claims the superseder never restates. v3–v6 satisfy the written sentence and falsify the
first clause at the same time (`m10=0` with false `present` claims in the tree, and v4–v6
with `C2_R43_PASS=true`). This is a calibration finding against the class sentence, not an
execution bug against the sentence as frozen.

Secondary, over-count direction (no amnesty, but a reproducibility hazard): v2 gives
`m10=2` when `supersedes` names the report `.md` instead of the receipt `.json`. The key
is compared byte-for-byte against the ls-tree path (only a leading `./` is normalised,
`measure.py:271-273`), so the same intent recorded in the obvious other spelling turns the
amnesty off. No live receipt uses that spelling.

## Mutation probe

Two mutants of the frozen bytes, run against v1–v6 and the live lane at base/freeze. The
detector is the frozen sentence's expected output: v1 must give `m10=1` and v3 must give
`m10=0`; a mutant that moves either is killed *against the frozen rule*.

| tool | sha256 (prefix 16) | v1 | v2 | v3 | v4 | v5 | v6 | lane-freeze |
|---|---|---|---|---|---|---|---|---|
| pristine | `97609511bb77e970` | 1 | 2 | 0 | 0 | 0 | 0 | 0 (receipts=17) |
| M1 drop the skip (`:281-282`) | `6640243b56114a62` | 2 | 2 | 2 | 2 | 1 | 2 | **1** |
| M2 skip only on per-claim re-assertion | `a909680c5a77dec3` | 2 | 2 | 1 | 2 | 0 | 2 | 0 |

* **M1, killed** (v1 2≠1, v3 2≠0). M1 is also the measurement of what the amnesty hides in
  the live lane: exactly one contradiction surfaces at the freeze (the round-41 residual
  claim), and it is the one the superseder legitimately corrected.
* **M2, killed against the frozen rule but it is the candidate repair.** It skips only a
  claim whose path a superseder actually re-asserts, and it makes v1=2, v3=1, v4=2, v6=2
  while leaving the live lane at 0 — i.e. it flags every modelled falsehood except v5.
* **M2 survives v5.** With `A → A` self-reference, the author is its own superseder, so
  the claim counts as re-asserted. A repair needs `author != superseded receipt` as well.
  Recorded as a survival, not as a licence to change the contract.
* M2's lane-freeze `0` is the control that the live suppression is honest under a
  per-claim rule too.
* Neither mutant is proposed as shipped bytes; the frozen pin stays `97609511…`.

## Severity

* C2 as delivered is **not falsified at the deciding rev** by this probe: `m10=0` at base
  and freeze, and the single suppressed claim is correctly superseded on inspection.
* The class is **not load-bearing against the hazard it names**: a one-field edit
  (self-`supersedes`, or a successor with no claims) produces `C2_R43_PASS=true` over false
  `present` claims (v4, v5, v6), and a superseder that restates only part of a receipt
  silently covers the rest (v3). Any future round's `m10=0` must therefore be read as
  "agrees modulo every supersede chain", not as the class sentence's universal.
* Recommended direction for a later round (not this one, no contract change here): key the
  skip on (receipt, re-asserted path) with self-reference excluded, and state the class as
  "a receipt's claim is skipped only when another receipt re-asserts that same path".

## Reproduction

```
# scratch repos were built at /tmp/tameshi-r43-w2-MutC2m10Superseder-/{v1..v6}
python3 <scratch>/v1/.ufo/evidence/round-43/calibration/measure.py \
    --lane <scratch>/v1 --rev 2b61bddf6407f688841bd356be2ff67f40da6e43 \
    --freeze 2b61bddf6407f688841bd356be2ff67f40da6e43
# live, permitted revs only
python3 .ufo/evidence/round-43/calibration/measure.py --lane . \
    --rev 3aee2c078f8976499b587086af3577fc94dc8cf1 \
    --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1
```

## Restoration / cleanliness evidence

* Lane counter bytes never touched: sha256
  `97609511bb77e97022d355c309a7bdc9ff7a2c74c48ac9622de600d1d28ef8d0`, equal to the
  contract pin, re-read after every probe run.
* No lane write except this report; no `git add/commit/stash/checkout/switch/reset/pull/push`
  and no mutating jj command in the lane. Lane reads were `git ls-tree` / `git show` only.
* Scratch root `/tmp/tameshi-r43-w2-MutC2m10Superseder-` was deleted after the fixtures,
  mutant shas and outputs above were captured (no scratch bytes remain).
* Tooling: nothing installed or upgraded (pacman paused host-wide; no other channel used).

## Incidental (out of this item's scope, for the L1's ledger)

At the freeze rev the frozen counter exits 1 with `m7=1`,
`first=m7:corpus/lessons/round-43.md_unknown_S160` — the round-43 lessons cite `S160`,
which is not a registry row at `3aee2c07`. I did not evaluate the deciding rev. This is
reported because it is a live `C2_R43_PASS=false` on a permitted rev; another seat likely
owns it.
