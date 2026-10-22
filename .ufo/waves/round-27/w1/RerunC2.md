# RerunC2 — independent re-run of the C2 counter and the F8 anchor probe, round 27 wave 1

Seat: TameshiR27.RerunC2 (executor, leaf, read-only outside the report file).
Judged on: coverage. Date: 2026-10-22.
Content revision under test: `2227d8338c02aa9a5fd7d95c1a41b76865ad7647`.
Base under test: `91edf9cd82ccc72e10f62f81d37181f549d593b8`.
Tools installed or updated: none. Node `v24.21.0` and Python 3 were already
present (`node --version` → `v24.21.0`).

All commands ran inside private clones `/tmp/RerunC2-r27` (head) and
`/tmp/RerunC2-base` (base), both made with
`git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin …`.
No `jj` command was run. No `git` write command was run in
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; read-only git there used
`GIT_OPTIONAL_LOCKS=0`.

## Verdict

**C2 reproduces. The claim holds as registered; no correction is required for
the claim itself.** The counter reads `classified=4` (exit 0) at the content
revision and `classified=0` (exit 1) at base, exactly the registered
before/target pair, and my probe re-run reproduces the committed receipt's
classifications field for field.

One bounded defect in the *evidence*, not in the claim: six of the receipt's
72 flattened fields differ between my re-run and the committed receipt. All
six are `stdout_sha256` values, and all six differ only because the node
process embeds the temporary witness-tree path in its JSON output. The
classification fields (`class`, `pristine_meets_anchor`,
`mutant_meets_anchor`, exit codes, finding kinds, `witness_facts`, `expect`,
`probe_sha256`, `anchors_sha256`, `node`, blob pin) are identical. I prove
the cause below with two of my own runs of the same survivor.

Residual risk worth the L1's attention (registration ordering, not a claim
failure): the counter amendment and the content change that it authorises
land in the **same** commit `2227d83`, so the amendment's own claim "before
any after-measurement of C2" is asserted inside the commit rather than
attested by a separate earlier commit. The pre-registration commit `70df8d6`
does carry the frozen counter and the contract, and `06a6707` carries the
anchors and the probe before the probe ran, so the anchoring was committed
before its execution; only the amendment's ordering is self-asserted.

## Evidence

### 1. Counter at the content revision — target met

```
$ cd /tmp/RerunC2-r27
$ python3 .ufo/evidence/round-27/c2-measure.py --repo /tmp/RerunC2-r27 --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
  S_OOR_EDGE: anchored-hole pristine_meets=True mutant_meets=False
  S_STRICT: anchored-hole pristine_meets=True mutant_meets=False
  S_USAGE: anchored-hole pristine_meets=True mutant_meets=False
  S_PIN_INCLUDES: anchored-hole pristine_meets=True mutant_meets=False
C2_F8: survivors=4 classified=4 anchored_holes=4 rev=2227d8338c02aa9a5fd7d95c1a41b76865ad7647
EXIT=0
```

Registered target (`contract.json`, claim C2): `classified=4` (exit 0) at the
landed head; `anchored_holes` reported as observed, not targeted. Observed
`anchored_holes=4`. Met.

The counter bytes I ran are the committed bytes at that revision:
`git show 2227d83:.ufo/evidence/round-27/c2-measure.py | sha256sum` →
`fdaa28cb09746117bf12f3523e92bf25cb72417db57fdc0b181a84789206119d`, identical
to the working-tree file, so the working copy is not what moved the number.

### 2. Counter at base — before value reproduced exactly

```
$ python3 .ufo/evidence/round-27/c2-measure.py --repo /tmp/RerunC2-base --rev 91edf9cd82ccc72e10f62f81d37181f549d593b8
  S_OOR_EDGE: UNCLASSIFIED (no anchored expectation; receipt not bound to probe and anchors bytes; F8 entry or mined S012 missing)
  S_STRICT: UNCLASSIFIED (no anchored expectation; receipt not bound to probe and anchors bytes; F8 entry or mined S012 missing)
  S_USAGE: UNCLASSIFIED (no anchored expectation; receipt not bound to probe and anchors bytes; F8 entry or mined S012 missing)
  S_PIN_INCLUDES: UNCLASSIFIED (no anchored expectation; receipt not bound to probe and anchors bytes; F8 entry or mined S012 missing)
C2_F8: survivors=4 classified=0 anchored_holes=0 rev=91edf9cd82ccc72e10f62f81d37181f549d593b8
EXIT=1
```

`diff` against the committed `.ufo/evidence/round-27/c2-before-amended.stdout`
is empty (`BASE_STDOUT_IDENTICAL_TO_COMMITTED`). The base has no
`corpus/knowledge/oracle-anchored-survivors.md`
(`git cat-file -e 91edf9cd:corpus/knowledge/oracle-anchored-survivors.md` →
`does not exist`), so the three UNCLASSIFIED reasons are each true.

The **frozen** pre-registration counter (`git show 70df8d6:.ufo/evidence/round-27/c2-measure.py`,
saved to `/tmp/RerunC2-c2-frozen.py`) also reads `classified=0` at base, exit 1,
same stdout. So the amendment did not move the before value. At head the
frozen counter reads `classified=0` with reason `F8 entry or mined S012
missing` — the amendment is what lets the amended counter read 4.

### 3. Probe re-run — every ANCHOR line

```
$ cd /tmp/RerunC2-r27
$ python3 .ufo/evidence/round-27/f8/anchor-probe.py \
    --kumitate /home/vgpnk/Projects/shokunin/kumitate-shokunin \
    --anchors .ufo/evidence/round-27/f8/anchors.json \
    --out /tmp/RerunC2-receipt.json
ANCHOR S_OOR_EDGE: anchored-hole pristine=1 mutant=0
ANCHOR S_STRICT: anchored-hole pristine=1 mutant=0
ANCHOR S_USAGE: anchored-hole pristine=64 mutant=65
ANCHOR S_PIN_INCLUDES: anchored-hole pristine=1 mutant=0
ANCHOR_PROBE: ran=4/4 anchored_holes=4
EXIT=0
```

`diff` against the committed `.ufo/evidence/round-27/f8/probe.stdout` is empty
(`PROBE_STDOUT_IDENTICAL_TO_COMMITTED`). Every ANCHOR line is reproduced
verbatim, including the `ANCHOR_PROBE:` summary line.

The pinned blob still hashes as registered:
`git -C kumitate-shokunin show 1205c66:scripts/cite-check.mjs | sha256sum`
→ `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`,
equal to `anchors.json`'s `blob_sha256`.

### 4. Receipt compared field by field

Flattened both JSON documents (72 leaf fields) and compared:

```
TOTAL_FIELDS 72 DIFFS 6
```

The six differing fields, verbatim:

| field | mine | committed |
|---|---|---|
| `/results/0/pristine/stdout_sha256` | `00f96797ca570b2af746902d1a157c577c9bc5626b39b33ab90f1924ce7c057b` | `337362417c0aacf373a77bf36f26920511745a2792f5d771ef9b8cd90c954135` |
| `/results/0/mutant/stdout_sha256` | `ea9b6989e01f562dab63332568fede52863944f19590d9ed31bcb161124d96bb` | `cd7a90860866d5200c305418e8c246ca1cbcb9f12279af40f4b182372e0b8bb7` |
| `/results/1/pristine/stdout_sha256` | `e2ad683cfb4399eb376ca0dd427f9b93ec53d4dee3ad454d87a0ec32d886c64e` | `b4efd53c21d087bc365dbff8fe2c032f0f329213970b6e9a6710b5232783a7ba` |
| `/results/1/mutant/stdout_sha256` | `1a0a9de1cbb4618750839b63bd6fbbc78376340cec0598c84047379b226b5b67` | `a2245b986da6e011a444e0d8a3b9a56f009b33019de94452e37db8dac12ec1c4` |
| `/results/3/pristine/stdout_sha256` | `91b3adf693bbdfb8a8c669e96537053940578890cd6f6fde577c68bc924debd0` | `b5b9e90e3d1079f0f28e8a244cb55397f62710088481dbdad4a6aa8caaffd2c8` |
| `/results/3/mutant/stdout_sha256` | `e125e05fb96a6fd17f7ef8a8f8daaa8647f0289b07792fd9c0166fe428d4fdff` | `751ea5dd3c1612a19ec970e2b7de10c8833fc7adb9bd0bc4847be8154f0be900` |

**Which fields differ:** exactly the six `stdout_sha256` values of survivors
`S_OOR_EDGE` (index 0), `S_STRICT` (index 1) and `S_PIN_INCLUDES` (index 3),
pristine and mutant. `S_USAGE` (index 2) does not differ at all: its stdout is
empty, so the digest is the empty-string digest
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` in both
receipts.

**Every other field is identical**, including: `schema`, `probe_sha256`,
`anchors_sha256`, `node` (`v24.21.0`), `target.repo/rev/path/blob_sha256`,
and per survivor `id`, `witness_facts`, `expect`, `class`,
`pristine_meets_anchor`, `mutant_meets_anchor`, `pristine.exit`,
`pristine.error_warn_kinds`, `pristine.json`, `pristine.stderr_head`,
`mutant.exit`, `mutant.error_warn_kinds`, `mutant.json`,
`mutant.stderr_head`.

**Cause, proved rather than asserted.** The differing digests are path-
dependent, not content-dependent. The node JSON output carries the witness
tree's absolute path in its top-level `src`, `self` and `fleet` fields. Two
independent runs of the same survivor:

```
run 1 raw_sha 5ef2d014104f20c9 norm_sha 0004635817c743b1
run 2 raw_sha a6b2abdd8dfa0ddb norm_sha 0004635817c743b1
raw digests equal? False
normalized digests equal? True
normalized texts equal? True
path-bearing top-level keys: {'src': '<ROOT>/src', 'self': '<ROOT>/self', 'fleet': '<ROOT>/fleet'}
```

The same test over all four survivors confirms the pattern: raw digests vary
run to run for `S_OOR_EDGE`, `S_STRICT` and `S_PIN_INCLUDES` (the three that
emit JSON), while path-normalised digests are stable; `S_USAGE` emits nothing
on stdout, so its raw digest is stable and matches the committed one. A
sample of the raw stdout shows the embedded path directly:

```
{
  "schema": "kumitate-cite-check-v1",
  "src": "/tmp/tmpuni9ypxv/t/src",
  "self": "/tmp/tmpuni9ypxv/t/self",
  "fleet": "/tmp/tmpuni9ypxv/t/fleet",
  ...
```

So: **the six differing stdout digests differ only because node output embeds
paths**, which is the permitted case. Nothing else in the receipt moved. The
counter does not read `stdout_sha256` at all (it checks `class`,
`pristine_meets_anchor`, `mutant_meets_anchor` and the two digest bindings),
so the claim's measurement does not rest on these fields.

### 5. The digest binding the counter enforces

```
$ sha256sum .ufo/evidence/round-27/f8/anchor-probe.py .ufo/evidence/round-27/f8/anchors.json
2d9308ba950c96671d0b50855f4d171ea256f07eace18fa39d7755e7a557648d  .ufo/evidence/round-27/f8/anchor-probe.py
780e1009fc484d364222fa32ee2bd960ccccd885d818b1deb44e4fdd82bd5eea  .ufo/evidence/round-27/f8/anchors.json
```

These equal the `probe_sha256` and `anchors_sha256` recorded in the committed
receipt, and equal `git show 2227d83:…` of the same two paths. The receipt is
therefore bound to the bytes that produced it, and my re-run receipt carries
the same two digests (`probe_sha256 2d9308ba…`, `anchors_sha256 780e1009…`).

### 6. The anchors are anchored outside the mutated code (checked, not assumed)

Pinned blob `1205c66:scripts/cite-check.mjs`, 2538 lines.

| survivor | `@old` at line | contract anchor lines | anchor present on its line |
|---|---|---|---|
| S_OOR_EDGE | 1312 | 61, 69 | yes, both |
| S_STRICT | 1589 | 35, 69 | yes, both |
| S_USAGE | 2512 | 71 | yes |
| S_PIN_INCLUDES | 1195 | 38 | yes |

Each `@old` occurs exactly once in the blob and the `@new` string occurs zero
times, so the probe's "exactly one occurrence" precondition holds and the
mutation is unambiguous. The contract anchors sit in the header comment
(lines 35–71); the mutated statements are code lines (1195–2512), so no
survivor edit can move an anchor line.

The arithmetic anchor for `S_OOR_EDGE` holds on the witness bytes: the probe
writes 20 newline-terminated lines and the doc cites `scripts/real.mjs:21`.

```
newline_count 20 len_lines_split 20
SKILL.md cites: Edge citation: `scripts/real.mjs:21`.
```

Line 21 does not exist; `LINE_OOR` is the right finding, and the anchored
expectation (exit 1, `LINE_OOR`) matches the pristine.

### 7. The SOURCES rows the external anchors rely on

At `2227d83`, `corpus/SOURCES.md`:

```
S012 status=mined  opened=2026-10-19  used_by=corpus/knowledge/oracle-anchored-survivors.md
S090 status=mined  opened=2026-10-22  used_by=corpus/knowledge/oracle-anchored-survivors.md
S091 status=mined  opened=2026-10-22  used_by=corpus/knowledge/oracle-anchored-survivors.md
```

Both external anchor quotes are present in their cited rows (whitespace
normalised): `S090 quote_in_row True`, `S091 quote_in_row True`.

### 8. The amendment is substantively justified

`contract-amendment-1.json` changes check 3 from "S012 `mined` with `opened`
2026-10-22" to "S012 `mined` with the entry path in `used-by`". The
justification is CORPUS.md SOURCES contract rule 2 (`CORPUS.md:116`, at the
fleet root):

> 2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change
>    is logged old→new in the round lesson.

S012's `opened` cell is `2026-10-19` and the row's other immutable cells are
untouched, so the frozen check could only have passed by a contract breach.
The `used-by` change is logged in `corpus/lessons/round-27.md` §Gate
("Status `queued` → `mined`; used-by `—` →
`corpus/knowledge/oracle-anchored-survivors.md`; opened and recheck cells
unchanged"). The amendment leaves the target `classified=4` unchanged, and
the amended counter still reads 0 at base (section 2). The amendment is
within the rules.

Note: `corpus/lessons/round-27.md` is untracked in the lane working copy at
the time I read it; it is not part of revision `2227d83`. That does not affect
the counter (it reads only `corpus/SOURCES.md`, the entry, and the two
digest-bound files) but the L1 should confirm the lesson is committed with
the landing.

## Smallest safe correction

For the **claim**: none. C2 measures as registered at both ends of the
interval and the probe reproduces the committed classifications exactly.

For the **evidence** (one bounded item, the only defect I found):

1. Make the probe's stdout digest path-independent. In
   `.ufo/evidence/round-27/f8/anchor-probe.py`, the `run()` helper computes
   `stdout_sha256` over raw stdout, and the raw stdout embeds the temporary
   witness-tree path. Replace the raw digest with a digest over the stdout
   after substituting the witness root path with a fixed placeholder (the
   same normalisation I applied in section 4), or record both a raw and a
   normalised digest and let the receipt carry the normalised one. Then
   regenerate `.ufo/evidence/round-27/f8/receipt.json` and
   `probe.stdout` so the receipt is byte-reproducible by any later re-run.
   This changes no classification, no anchor and no counter reading; it only
   makes a receipt field checkable. The counter does not read this field, so
   the fix is not required for `classified=4` — it is required for the
   receipt to be re-checkable by digest, which is the receipt's own stated
   purpose. I did not make this edit: it touches a committed evidence file
   outside my write scope.

2. If the L1 wants the amendment's ordering independently attested rather
   than self-asserted, the smallest form is a note in the round-27 lesson
   recording that the amended counter was run against base
   (`c2-before-amended.stdout`, exit 1) before the content revision was
   measured, with the command and its timestamp. The measurement itself
   already exists in the tree and reproduces byte-identically for me.

## Risks and blockers

- **Risk (low, evidence only):** the receipt's `stdout_sha256` fields are not
  reproducible across runs, so a future reader cannot byte-compare a fresh
  receipt to the committed one. Mitigated by the fact that no claim depends on
  them and by the fact that the path-normalised content is stable.
- **Risk (low, registration):** amendment 1 and the content it authorises
  land in one commit, so "before any after-measurement" is asserted inside
  the commit rather than attested by an earlier one. The frozen counter at
  `70df8d6` and the anchors+probe at `06a6707` are separately committed
  before use, so the anchoring itself was not back-fitted.
- **Risk (informational):** `corpus/README.md:85` still reads F8 `open`;
  the appended round-27 section supersedes that status cell and says so.
  `corpus/lessons/round-27.md` was untracked when I read it.
- **Note on concurrent lane state (informational, does not affect this
  report):** while I was measuring, a sibling wave seat (CriticAnchors /
  MutateC2Counter) edited `corpus/knowledge/oracle-anchored-survivors.md` in
  the lane working copy. I did not touch that file. Every number in this
  report was taken from committed bytes at `2227d83` in my own clone, so it
  is unaffected; a re-run after that edit lands will need a fresh counter
  reading, which is the L1's post-integration gate, not mine.
- **Blockers:** none for C2. The claim is reproducible at head and base from a
  clean clone with the committed counter bytes.
