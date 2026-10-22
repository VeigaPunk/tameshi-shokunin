# MutateC2Counter — round 27, wave 1

Mutation probe of the C2 counter and the F8 anchor probe. Leaf seat: no dispatch, no
production edit, nothing written outside this report.

## Verdict first

- All four counter mutants of `.ufo/evidence/round-27/c2-measure.py` are **killed**.
  Each one has a repo state where the honest counter reads strictly lower than the
  mutant, so every dropped check is live on this population.
- The probe mutant of `.ufo/evidence/round-27/f8/anchor-probe.py` is **killed only
  conditionally** (the counter sees it while the receipt is stale) and **survives**
  when the receipt is re-bound by re-running the mutated probe: the counter reads
  `classified=4`, exit 0, and no committed artifact notices.
- Two coverage findings fall out of that survival, both about the receipt and not
  about the counter's four checks:
  1. On this population the probe mutation is a **semantic no-op**: the mutant
     receipt carries the same four class labels as the pristine receipt, because every
     witness has a mutant exit that differs from the pristine exit. The committed
     receipt therefore does not show that any survivor was judged against the anchor
     rather than against the pristine run.
  2. The counter **does not validate the receipt's content**. A hand-edited receipt
     (one class label flipped) still reads `classified=4`, exit 0. The digest binding
     protects the probe bytes and the anchors bytes, not the recorded observations.

## Setup

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/MutateC2Counter-r27
git -C /tmp/MutateC2Counter-r27 checkout -q --detach 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
```

Every command below ran inside `/tmp/MutateC2Counter-r27` or `/tmp/MutateC2Counter-mut`.
The source repo was only ever read (`git status`, `git show`, `sha256sum`).

- Baseline, honest counter at the landed head:
  `python3 .ufo/evidence/round-27/c2-measure.py --repo /tmp/MutateC2Counter-r27 --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647`
  → `C2_F8: survivors=4 classified=4 anchored_holes=4`, exit 0.
- Tooling: node v24.21.0 (already present), python3 (already present), git (already
  present). **No package was installed or upgraded in this seat.**

## Part (a) — four counter mutants

The four mutants are copies of the frozen counter with one check removed each. The
pristine counter bytes are `fdaa28cb09746117bf12f3523e92bf25cb72417db57fdc0b181a84789206119d`.

### mA — the probe/anchors digest binding dropped — KILLED

Exact edit (`.ufo/evidence/round-27/c2-measure.py`, the `bound = ...` block):

```diff
-    bound = bool(receipt_b and probe_b and anchors_b) \
-        and receipt.get('probe_sha256') == hashlib.sha256(probe_b).hexdigest() \
-        and receipt.get('anchors_sha256') == hashlib.sha256(anchors_b).hexdigest()
+    # MUTANT A: the receipt/probe/anchors digest binding is dropped entirely.
+    bound = True
```

Mutant bytes `109408099fb31df9a2ac105cf14d6d2a7c101362288e43d8ac7802ee5955e126`.

Discriminating state `st_probe_mut` (`032dcdf9e0cc0251f919a9748548e1d016a609f5`):
the committed `anchor-probe.py` is changed and the receipt is left stale.

- Expected detector: the counter prints `receipt not bound to probe and anchors bytes`
  and exits 1. This is the falsifier written into `corpus/QUALITY.md` item 54.
- Observed, honest counter:

```
  S_OOR_EDGE: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
  S_STRICT: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
  S_USAGE: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
  S_PIN_INCLUDES: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
C2_F8: survivors=4 classified=0 anchored_holes=0
exit=1
```

- Observed, mutant A on the same state: `C2_F8: survivors=4 classified=4 anchored_holes=4`, exit 0.

Honest reads 0, mutant reads 4. **Killed.**

### mB — the contract-quote line check dropped — KILLED

Exact edit (the `contract` branch of the anchor loop):

```diff
                 if an['kind'] == 'contract':
-                    ln = an.get('line', 0)
-                    if not (0 < ln <= len(blob_lines) and norm(an['quote']) in norm(blob_lines[ln - 1])):
-                        why.append('contract quote not on line %s' % ln)
+                    # MUTANT B: the contract-quote line check is dropped.
+                    pass
```

Mutant bytes `a95920d2fcf2ccdaf5771689d1ddf1e3bc256983582014e7b4d6c11e54477846`.

Discriminating state `st_contract` (`6ae26df70b663c5c4f6533757fdb685b15b9eb63`): the
S_STRICT contract anchor in `anchors.json` moves from line 35 to line 36 of the pinned
blob (line 36 does not carry the quote), and the receipt is re-bound by re-running the
**pristine** probe, so the digest binding still holds.

- Expected detector: `contract quote not on line 36` for S_STRICT, `classified=3`, exit 1.
- Observed, honest counter:

```
  S_OOR_EDGE: anchored-hole pristine_meets=True mutant_meets=False
  S_STRICT: UNCLASSIFIED (contract quote not on line 36)
  S_USAGE: anchored-hole pristine_meets=True mutant_meets=False
  S_PIN_INCLUDES: anchored-hole pristine_meets=True mutant_meets=False
C2_F8: survivors=4 classified=3 anchored_holes=3
exit=1
```

- Observed, mutant B on the same state: `C2_F8: survivors=4 classified=4 anchored_holes=4`, exit 0.

Honest reads 3, mutant reads 4. **Killed.**

### mC — the external-row status/opened check dropped — KILLED

Exact edit (the `external` branch):

```diff
                     row = rows.get(an.get('source'), {})
-                    if not (row.get('status') == 'mined' and row.get('opened') == OPENED
-                            and norm(an['quote']) in norm(row.get('line', ''))):
+                    # MUTANT C: the external row status/opened check is dropped.
+                    if not (norm(an['quote']) in norm(row.get('line', ''))):
```

Mutant bytes `8b9d0ecba7815c0f459a666820873cc5c9f8ec6b766fd5e88e08b9952976b312`.

Discriminating state `st_external` (`6ce2fab2e798c487538af4d456babb1735bd23d2`): the
S090 row in `corpus/SOURCES.md` changes status `mined` to `candidate`; the row text
still carries the quote.

- Expected detector: `external S090 not a mined row opened 2026-10-22 carrying the quote`
  for S_USAGE, `classified=3`, exit 1.
- Observed, honest counter:

```
  S_USAGE: UNCLASSIFIED (external S090 not a mined row opened 2026-10-22 carrying the quote)
C2_F8: survivors=4 classified=3 anchored_holes=3
exit=1
```

- Observed, mutant C on the same state: `C2_F8: survivors=4 classified=4 anchored_holes=4`, exit 0.

Honest reads 3, mutant reads 4. **Killed.**

### mD — any S012 status accepted — KILLED

Exact edit (the `entry_ok` expression):

```diff
     s012 = rows.get('S012', {})
+    # MUTANT D: any S012 status is accepted (the status cell is not checked).
     entry_ok = bool(entry_b) and bool(re.search(r'(?m)^ground: F8\b', entry_b.decode('utf-8'))) \
         and bool(re.search(r'(?m)^source:.*\bS012\b', entry_b.decode('utf-8'))) \
-        and s012.get('status') == 'mined' and ENTRY in s012.get('used_by', '')
+        and ENTRY in s012.get('used_by', '')
```

Mutant bytes `9b7182772ea3bb6132cc4c240c37fdae3ff648131733d9302eab6b1e3f67ea59`.

Discriminating state `st_s012` (`49da225f8bf07a8dda08afd1afaaad279cca19ce`): the
S012 row in `corpus/SOURCES.md` changes status `mined` to `candidate`; the `used-by`
cell is unchanged.

- Expected detector: `F8 entry or mined S012 missing` for all four, `classified=0`, exit 1.
- Observed, honest counter:

```
  S_OOR_EDGE: UNCLASSIFIED (F8 entry or mined S012 missing)
  S_STRICT: UNCLASSIFIED (F8 entry or mined S012 missing)
  S_USAGE: UNCLASSIFIED (F8 entry or mined S012 missing)
  S_PIN_INCLUDES: UNCLASSIFIED (F8 entry or mined S012 missing)
C2_F8: survivors=4 classified=0 anchored_holes=0
exit=1
```

- Observed, mutant D on the same state: `C2_F8: survivors=4 classified=4 anchored_holes=4`, exit 0.

Honest reads 0, mutant reads 4. **Killed.**

### Full matrix (honest counter and the four mutants, one row per state)

```
state              honest                     mA                 mB                 mC                 mD
st_base            4 (exit 0)                 4 (exit 0)         4 (exit 0)         4 (exit 0)         4 (exit 0)
st_probe_mut       0 (exit 1)                 4 (exit 0)  <--    0 (exit 1)         0 (exit 1)         0 (exit 1)
st_probe_regen     4 (exit 0)                 4 (exit 0)         4 (exit 0)         4 (exit 0)         4 (exit 0)
st_contract        3 (exit 1)                 3 (exit 1)         4 (exit 0)  <--    3 (exit 1)         3 (exit 1)
st_external        3 (exit 1)                 3 (exit 1)         3 (exit 1)         4 (exit 0)  <--    3 (exit 1)
st_s012            0 (exit 1)                 0 (exit 1)         0 (exit 1)         0 (exit 1)         4 (exit 0)  <--
```

`<--` marks the state where the honest counter reads strictly lower than that mutant.
Each mutant has exactly one such state, and no state where the mutant reads lower
than the honest counter. The honest counter is never over-reported by any mutant.

## Part (b) — the probe mutant

Exact edit in `.ufo/evidence/round-27/f8/anchor-probe.py`:

```diff
 def meets(obs, expect):
+    # MUTANT (b): the finding kind is ignored, and the mutant run is compared
+    # with the pristine run instead of the anchored expectation.
     if obs['exit'] != expect['exit']:
         return False
-    k = expect.get('kind')
-    return k is None or k in obs['error_warn_kinds']
+    return True
@@
             r['pristine_meets_anchor'] = meets(r['pristine'], s['expect'])
-            r['mutant_meets_anchor'] = meets(r['mutant'], s['expect'])
+            # MUTANT (b): the mutant run is compared with the pristine run, not with the anchor.
+            r['mutant_meets_anchor'] = meets(r['mutant'], r['pristine'])
```

Pristine probe bytes `2d9308ba950c96671d0b50855f4d171ea256f07eace18fa39d7755e7a557648d`;
mutated probe bytes in the repo state `a7962f61ad724060ef40087345755659af1a5ada62796146bdab305b37d1d7da`.

### State `st_probe_mut` — mutated probe, receipt left stale (`032dcdf…`)

- The counter notices, through the digest binding only:

```
  S_OOR_EDGE: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
  ... (all four unclassified)
C2_F8: survivors=4 classified=0 anchored_holes=0
exit=1
```

- No committed artifact notices the semantic change either, but the entry file
  `corpus/knowledge/oracle-anchored-survivors.md` records the probe digest prefix
  `2d9308ba950c…`, which no longer matches the committed probe. Nothing checks that
  line automatically.

Verdict here: **killed**, but only by the binding check, not by anything that looks at
the probe's meaning.

### State `st_probe_regen` — mutated probe, receipt regenerated by that probe (`1476402…`)

- The mutated probe is run at the pinned blob and its receipt is committed next to it,
  so `receipt.probe_sha256` names the mutated probe and the binding holds.
- Honest counter output:

```
  S_OOR_EDGE: anchored-hole pristine_meets=True mutant_meets=False
  S_STRICT: anchored-hole pristine_meets=True mutant_meets=False
  S_USAGE: anchored-hole pristine_meets=True mutant_meets=False
  S_PIN_INCLUDES: anchored-hole pristine_meets=True mutant_meets=False
C2_F8: survivors=4 classified=4 anchored_holes=4
exit=0
```

  The counter does not notice. The four counter mutants do not notice either.
- Committed artifacts: the mutated probe's stdout is **byte-identical** to the committed
  `.ufo/evidence/round-27/f8/probe.stdout` (diff empty), and the entry's `recheck:` line
  quotes the same string `ANCHOR_PROBE: ran=4/4 anchored_holes=4`. No artifact notices.

Verdict: **survives.** The probe that never consults the anchor is accepted, and the
counter still reports the claim as met.

### Why it survives: the population cannot tell the two comparisons apart

The mutated receipt and the pristine receipt carry the **same** class labels and the
same `pristine_meets_anchor` / `mutant_meets_anchor` flags for all four survivors. The
only differences between the two receipt files are `probe_sha256` and the
`stdout_sha256` fields (the cite-check JSON embeds the absolute `--src`, `--self` and
`--fleet` root paths, and the probe builds every witness under a fresh temp directory,
so those digests change between runs of the pristine probe as well).

The reason is visible in the committed observations: for every survivor the mutant exit
differs from the pristine exit (`0` vs `1`, `0` vs `1`, `65` vs `64`, `0` vs `1`). A
comparison against the pristine run therefore produces the same verdict as a
comparison against the anchor. The four committed witnesses cannot separate "judged
against the anchor" from "judged against the pristine run".

### Extra probe — a receipt edited by hand (`st_fabricated`, `427df13…`)

The S_STRICT class label in `receipt.json` is flipped to `mutant-meets-anchor` with
`mutant_meets_anchor` set to true. The probe bytes and the anchors bytes are untouched,
so the binding still holds.

- Honest counter: `C2_F8: survivors=4 classified=4 anchored_holes=3`, exit 0. The counter
  does not notice. The four counter mutants read the same.
- The committed `probe.stdout` still says `anchored_holes=4`, so the artifact and the
  counter disagree, but no automated check compares them.

Verdict: **survives.** The counter reads a receipt's class labels and flags but never
re-derives them, and never checks that they agree with the recorded observations.

## Coverage findings

1. The counter's four checks (digest binding, contract quote on its line, external row
   status and opened date, S012 mined with the entry in `used-by`) are all exercised by
   this population. Each mutant that removes one of them is caught by a repo state.
2. The claim "classified against an independently anchored expectation" rests on the
   receipt's class labels, and this population cannot show that the anchor was used:
   a probe that compares the mutant with the pristine run produces an identical
   receipt. The digest binding shows that the receipt came from the committed probe
   bytes; it does not show that those bytes judge against the anchor.
3. The receipt's content is unvalidated. Its recorded observations and its class
   labels can be edited by hand, and the counter still reports the claim as met.
4. The receipt is not byte-reproducible. Two runs of the pristine probe differ only in
   the `stdout_sha256` fields, because the cite-check JSON embeds the absolute root
   paths and the probe uses a fresh temp directory per run. The receipt therefore
   cannot be re-derived and compared byte for byte from a re-run. Any re-execution
   check has to compare the classification, not the file bytes.

## Smallest safe correction (recommended, not applied)

1. In `c2-measure.py`, re-derive each class from the receipt's own recorded
   observations instead of trusting `class` and the two `*_meets_anchor` flags: require
   `pristine` and `mutant` observation records, compare them with the `expect` record
   in `anchors.json` the way `anchor-probe.py` does, and treat a mismatch as an absent
   receipt. This closes finding 3 with about ten lines and no new inputs.
2. Cross-check the receipt's per-survivor class and exit columns against the committed
   `.ufo/evidence/round-27/f8/probe.stdout`, which is already committed. This makes the
   hand-edited receipt visible to the counter.
3. For finding 2, only a re-execution binds the claim to the anchor: the counter (or a
   companion check) can run the committed probe at the measured revision and compare
   its classification with the committed receipt. The digest binding alone cannot do it,
   and `corpus/QUALITY.md` item 54 should say so: a receipt that names the tool bytes
   is not the same as a receipt that a run of those bytes produced.
4. A witness that separates the two comparisons would repair the population: one whose
   mutant exit equals the pristine exit but whose finding kind differs. Then the
   pristine-relative comparison and the anchor comparison disagree, and the receipt
   would show which one was used.

## States built (all in the scratch clone only)

| branch | commit | what it changes |
|---|---|---|
| `st_probe_mut` | `032dcdf9e0cc0251f919a9748548e1d016a609f5` | probe mutated, receipt stale |
| `st_probe_regen` | `147640275a3b2af78455efd14650f26f42b06265` | probe mutated, receipt regenerated by that probe |
| `st_contract` | `6ae26df70b663c5c4f6533757fdb685b15b9eb63` | S_STRICT contract anchor moved to line 36, receipt re-bound by the pristine probe |
| `st_external` | `6ce2fab2e798c487538af4d456babb1735bd23d2` | S090 status `mined` to `candidate` |
| `st_s012` | `49da225f8bf07a8dda08afd1afaaad279cca19ce` | S012 status `mined` to `candidate` |
| `st_fabricated` | `427df13aede1a51dba9f583a7b5b3b90c9f1e32e` | receipt class label for S_STRICT flipped by hand |

## Restoration evidence

- Source repo `/home/vgpnk/Projects/shokunin/tameshi-shokunin` was never written to.
  `GIT_OPTIONAL_LOCKS=0 git status --short` there lists only untracked round-27 work
  from other seats (`?? .ufo/evidence/round-27/after/`, `?? .ufo/evidence/round-27/coldread/`,
  `?? .ufo/waves/round-27/`, `?? corpus/lessons/round-27.md`); no tracked file is
  modified, HEAD is still `2227d8338c02aa9a5fd7d95c1a41b76865ad7647`, and the key file
  digests are unchanged from the base commit:

```
fdaa28cb09746117bf12f3523e92bf25cb72417db57fdc0b181a84789206119d  .ufo/evidence/round-27/c2-measure.py
2d9308ba950c96671d0b50855f4d171ea256f07eace18fa39d7755e7a557648d  .ufo/evidence/round-27/f8/anchor-probe.py
780e1009fc484d364222fa32ee2bd960ccccd885d818b1deb44e4fdd82bd5eea  .ufo/evidence/round-27/f8/anchors.json
6198c0339cc0b21cead997a795220c4b01272ff286b4e9a0ebde015a1f192a68  .ufo/evidence/round-27/f8/receipt.json
0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a  corpus/SOURCES.md
```

- Scratch clone `/tmp/MutateC2Counter-r27` is detached at the base revision with a
  clean working tree and byte-identical files to the base commit (`diff` of the
  working `receipt.json` against `git show 2227d83:...` is empty). The six crafted
  states stay on their own local branches and are reachable by `git branch`.

## Bounds honoured

- No production file was edited; the only file written in the lane is this report.
- No git write command was run in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, and
  no `jj` command was run anywhere.
- The kumitate repo was read only (`git show` of the pinned blob), and the probe ran
  entirely inside `/tmp`.
