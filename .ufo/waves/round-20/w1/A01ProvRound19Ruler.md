# A01 — Round-19 ruler wave-1 provenance (sha 96a68b60…)

Seat: TameshiR20-3.A01ProvRound19Ruler · Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin · 2026-10-21 · Read-only; no production, Git/JJ, or sibling writes. No installs performed.

## Axes

1. **Hash identity** at the assigned path `.ufo/evidence/round-19/measure.py`.
2. **Provenance completeness** — all reachable commits, full object DB, all tree entries.
3. **Label exactness** — is `round19-ruler-wave1` (contract.json:39) an exact name for these bytes?
4. **Reproducibility** — every claim below carries command + observed output.

## Result (one line)

**No reachable commit carries `.ufo/evidence/round-19/measure.py` hashing to 96a68b60…; the object does not exist in the repo at all. The bytes are exactly lines 53–376 (324 lines) of `.ufo/waves/round-19/w1/ReceiptDesign.md` (git blob `bcf455eac80f531d1636491ba80697bab780e1f8`), i.e. a fence-slice containing the wave-1 ruler script: a read-only, revision-pinned audit of the five frozen R18 corrections (R18-1…R18-5).**

## Method and observed outputs

All commands run with cwd `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

### 1. Path history (assignment's first command)

```
$ git log --all --format=%H -- .ufo/evidence/round-19/measure.py
040d18263b652ccea1db1bd596089520d303582f
329b6ddb826b16b1814b4ca87425f766c87e853d
887d03051875f981396e160a71697ac939fd3310
92e0512e996114599ed07fd5ea4e3b1000541880
cedfda86e71115863e0af053eafac19ff31aa1ec
f517611103ed97286c73f08e2cc7446d04680e0a
33ca2983d2c50551a3da3b213c6142afdd54c682
b3e3e5b0e6a28811bd70d9bdd2ec672940bd7272
eedbc95f232cde4a5aabd6e4e34fc2e78a1a5626
f1da8ba1e6e592d19b08ea3abe021271924349fb
296baf9bd03aaccf68d8f37af3bc5ddd533eb2fd
4c7b18aa77e2759d2999f834ceaaa68fb11e6572
c9fc98b1a413715a134cdb49877868578afac478
361cce05258623f5322f19d5159df92b2a4d0384
7af123b0e068cd5e6b651aab31a813cc170d70a2
aaf72dc6149116022f251136683be5fcea19ad8d
b2d6df8a7f160661323f95854cba3c25f223f31c
21e79329f8bdcf01a62be63b3e46db4a7de6b6f9
61491cf6295fd18382c6938fd6a698ec6dd6f16d
```

19 reachable revisions touch the path.

### 2. Blob digest at every touching revision

```
$ git log --all --format=%H -- .ufo/evidence/round-19/measure.py | while read r; do
    printf '%s ' "$r"; git show "$r:.ufo/evidence/round-19/measure.py" | sha256sum; done | sort -k2
```

| revisions | blob sha256 at path |
|---|---|
| 296baf9b, 4c7b18aa, c9fc98b1 | `fac15f7bb70ac8dc60c55e087c67c6da1f1d30c790d20057017f28508b8b853d` |
| 361cce05, 7af123b0, aaf72dc6, b2d6df8a | `e9b44cad15a01c5ba7b80ba569de6de2eb533d5d5a8929cb2775044fd00c5359` |
| 21e79329, 61491cf6 | `c538c33d6d80c9299183b6ff08a21da6f557fa66f99712f38820fdce1473e18e` |
| 33ca2983, b3e3e5b0, eedbc95f, f1da8ba1 | `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053` |
| cedfda86 | `8b6eb1fed52e11ea00d198f0987c6add258ee6c2c27b24fa2067ad18068e3cb9` |
| 040d1826, 329b6ddb, 887d0305, 92e0512e | `7af3e951bf67f7671954dee33aaa4dc183a642fce85cbc2d9d782085f856cf72` |
| f5176111 | `3f19a16b778242a1f83ba5a92b4b69798e56876003727757aa5497773a2e590f` |

7 distinct digests, none `96a68b60…`. **Zero revisions carry the target hash at that path.**

### 3. Object DB and tree scans (assignment extended)

```
$ git cat-file --batch-all-objects --batch-check='%(objectname) %(objecttype) %(objectsize)' \
    | grep 96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef
NO_SUCH_OBJECT          (no match — the object is absent, reachable or unreachable)
```

```
$ git rev-list --all | wc -l
224
$ git rev-list --all | while read r; do git ls-tree -r "$r" \
    | grep 96a68b60538504… | sed "s|^|$r |"; done
(no output — zero tree entries across all 224 reachable commits reference the hash)
```

Since the blob object is absent from the entire object DB, no tree anywhere (including unreachable) can verifiably carry it. Closure is total.

### 4. What the bytes actually are — fence-slice of ReceiptDesign.md

```
$ git rev-parse c144dcd807166dfc275c1ac2936fd2fa4b678bda:.ufo/waves/round-19/w1/ReceiptDesign.md
bcf455eac80f531d1636491ba80697bab780e1f8
$ git rev-parse 6fd220bce3705498d1d1054e99e3cae73c203751:.ufo/waves/round-19/w1/ReceiptDesign.md
bcf455eac80f531d1636491ba80697bab780e1f8
```

```
$ git show <REV>:.ufo/waves/round-19/w1/ReceiptDesign.md | sed -n '53,376p' | sha256sum
96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef   ← at c144dcd (baseline)
96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef   ← at 6fd220bc (contract)
96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef   ← at b3e3e5b0
96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef   ← at eedbc95f
```

Exact at **all four** revisions carrying blob `bcf455ea`; the slice is byte-stable across the whole history of the document. Byte-boundary check (python, /tmp sandbox): lines 53–376 joined with trailing newline → `96a68b60…` exact; same lines without trailing newline → `34e4dd7a91d7f6fff997b2e75a93141a7444cf991553d34a628075bb20fd17fc` (so the fence-slice convention is inclusive, newline-terminated — reproducible only with the trailing newline).

### 5. Slice header — what the ruler measures

First lines of the 324-line slice (document lines 53–72):

```python
#!/usr/bin/env python3
"""Read-only, revision-pinned audit for the five frozen R18 corrections."""
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
BASELINE = '7243e7f163f08978c8fd9b6c1ef67a2fefe7d190'
R18_BASE = '183f87b899e6cae46be98d251cbc87fb5118f6ca'
R18_TIP  = '4b7c6823a462f5ea2eafcb262275300a545f3ed7'
PROBE_REV = '921ef8077440f90d092aab4b9fdc750a45de1224'
MEASURE_OLD_REV = 'a85f7107c4167cd9968248722256fcaf617fc30c'
```

It pins baseline `7243e7f1`, `R18_BASE 183f87b8`, `R18_TIP 4b7c682` (plus probe/old-measure revs) and reads round-18 final evidence (`.ufo/evidence/round-18/final/checks.json`, `probes.stdout`, `measure-final-60.json`) and round-19 witness receipts (`bash-witness-selftest-complete.*`). Carrier document header: `# ReceiptDesign — round 19 attempt 1`, advisory-only, frozen population = R18-1…R18-5, "reports only those IDs and does not invent a calibration score."

### 6. Contract mapping (context)

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/contract.json:38-42`:

```json
"historical": {
  "96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef": "round19-ruler-wave1",
  ...
```

Distinctness: the current worktree/HEAD `.ufo/evidence/round-19/measure.py` is `7af3e951…` (HEAD = `6fd220bc`, worktree file hash identical → clean at that path); `.ufo/evidence/round-19/coldread/measure.py` is `4c9c74ca…`. Neither is the ruler sha; no conflation is possible once the mapping above is used.

## Findings by severity

- **F1 (medium, wording/provenance — no calibration impact):** The contract's historical key `96a68b60…` → `round19-ruler-wave1` is **content-exact but git-unresolvable at any path**: the sha identifies a 324-line fence-slice (`sed -n '53,376p'`, trailing newline) of `.ufo/waves/round-19/w1/ReceiptDesign.md` @ blob `bcf455ea`, not any committable file blob. A verifier following the label to `.ufo/evidence/round-19/measure.py` finds 7 other digests, never this one. Recommendation for the round-20 record (contract is frozen; not edited here): when receipts name historical instruments, state the derivation — `sha256(git show <rev>:.ufo/waves/round-19/w1/ReceiptDesign.md | sed -n '53,376p') = 96a68b60… @ bcf455ea` — instead of implying a standalone script. This supports the standing rider to name each historical instrument sha precisely.
- **F2 (info):** The ruler's function, per its own header: a **read-only, revision-pinned audit of the five frozen R18 corrections (R18-1…R18-5)** against baseline `7243e7f1`, R18 window `183f87b8..4b7c682`, consuming round-18 final checks/probes/measure evidence and round-19 bash-witness receipts. It is a measurement *specification with code*, embedded in the wave-1 design document — hence "ruler".
- **F3 (info):** The assignment's premise ("locate the reachable commit that contains a .ufo/evidence/round-19/measure.py blob hashing to 96a68b60…") is **falsified**: no such commit exists, and the object is absent from the object DB entirely. The correct carrying location is the ReceiptDesign.md slice.

## Agree/disagree

- **Agree with TameshiR20-3.E07GitProvenance** on all their claims, independently reproduced: no reachable commit carries the blob at the path (19-rev walk, 7 distinct digests, none match); full batch-all-objects scan shows zero such blobs; slice `sed -n '53,376p'` of ReceiptDesign.md @ `bcf455ea` → `96a68b60…` exact, identical at c144dcd and 6fd220bc.
- **Extension beyond E07:** slice verified identical at **all four** commits carrying `bcf455ea` (adds b3e3e5b0, eedbc95f); zero tree entries across all **224** reachable commits; boundary convention pinned to trailing-newline-inclusive lines 53–376.

## Frozen-fact verification status

- Baseline `c144dcd` and contract `6fd220bc` both exist and carry `bcf455ea` for ReceiptDesign.md — **verified**.
- `96a68b60…` = round19-ruler-wave1 mapping — **verified as content-identity**, with the derivation caveat in F1.

## Residual risk and verification gaps

- The "5,892 objects" total is E07's count; my independent check confirms the sha's absence from `--batch-all-objects` output but I did not recount the total (irrelevant to the closure argument).
- Walk scope is `--all` per assignment; reflog-only/unregistered refs were not separately enumerated. The object-DB absence makes this immaterial: no ref, reachable or not, can carry a blob that does not exist.
- The /tmp scratch original E07 mentions was not used; all evidence here is recomputed from git objects only.
