## Round 55 - round-54 record corrections

Each entry records the round-54 non-author spot-check's routed defect
(`corpus/lessons/round-54-verifier-spotcheck.md`, R54.1-R54.10) with the value
DERIVED from the tree, the byte-exact old text it replaces, and the command that
re-derives it. `Old`/`New` pairs below are verbatim: the quoted line is the
report's own line, and `New` differs from it only in the digest named.

**ER-R54-4 - a stale counter digest.**

`R54.4` - the "Bind and decide" paragraph named the wrong `c2` blob while calling
it the frozen counter's own bytes at the deciding revision. `Old`, verbatim from
the fleet report `.ufo/reports/round-54/tameshi.md:122` (the report lives at the
fleet root, not in this lane):

```
  The frozen counter's own bytes at the deciding revision are the freeze-manifest digest `d7749f84…` (c1) and `49280fe5…` (c2) — cite those, not the C1 blobs, which predate amendments 1–5.
```

`New` (byte-identical except the `c2` digest):

```
  The frozen counter's own bytes at the deciding revision are the freeze-manifest digest `d7749f84…` (c1) and `8528ee85…` (c2) — cite those, not the C1 blobs, which predate amendments 1–5.
```

Derived, not chosen: `8528ee85` is the first eight hex digits of the digest
`.ufo/evidence/round-54/freeze.json` pins for `c2/measure.py` -
`8528ee8555da068519af4159f5f9e0efac8b29de88a53534a7043d7ec007e790`.
`49280fe5` is the pre-amendment-4 blob: amendment 2's bytes (present at `19c7558`
and `7e533b1`, census regex `mkdir(?:at)\(`), which amendment 4 (`fe70474`)
replaced when it widened the census regex to `mkdir(?:at)?\(` and re-hashed the
manifest. The bytes at the deciding revision `c2108100` hash to the pinned digest.
Re-derive both halves with:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 0a2010acd1e92e4e332774050825e21bcfc7e079:.ufo/evidence/round-54/freeze.json \
 | python3 -c 'import json,sys; print(json.load(sys.stdin)["files"]["c2/measure.py"])'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c21081008adbb6b6fe4e58a0aeec4831b30e318c:.ufo/evidence/round-54/c2/measure.py | sha256sum
```

Receipts: `.ufo/waves/round-55/w1/T55W1Er04-receipts/` (`derive-freeze-digest.txt`,
`blob-attribution.txt`, `amendment4-diff.txt`, `c1-row-flip.txt`).
