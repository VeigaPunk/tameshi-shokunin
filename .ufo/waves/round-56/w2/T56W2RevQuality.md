# T56W2RevQuality — QUALITY criterion 107 falsifier (round 56, wave 2)

Seat: `T56W2RevQuality` (reviewer). L1: `TameshiR56`.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
C0 (content commit): `c0137451f5b7f22d65f748fc69f1b181f55e1378`
Freeze: `c3e2ca9f020776b3d66c7af854fb82c834674fcf` · Base: `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`

Scope: verify the new `corpus/QUALITY.md` criterion (the highest number at C0) says what
the claim needs and that its falsifier fires — run the exact command the criterion names on
the real receipt, then run it on a receipt that names the certified revision and confirm it
does NOT refuse. Also check the `corpus/lessons/round-56.md` and
`considerthese/2026-10-28.md` (dated) citations.

No lane production file was edited. No mutating git/jj command was run. Fixtures were
created only under `/fast/scratch/hyaku/tameshi-r56/T56W2RevQuality` and removed on exit.

---

## 1. The criterion's number and rule

**Number: 107.** It is the highest criterion number in `corpus/QUALITY.md` at C0.

```
$ git show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/QUALITY.md | grep -n '^### Criterion' | tail -5
1562:### Criterion 103 …
1574:### Criterion 104 …
1584:### Criterion 105 …
1592:### Criterion 106 …
1616:### Criterion 107 — a certified receipt names the revision it was measured against, and the gate refuses the ones that do not
```

C0 added exactly one criterion (`git diff 21eb3c6 c0137451 -- corpus/QUALITY.md | grep -E '^\+### Criterion'`
→ only `+### Criterion 107`).

**Rule, one sentence:** every receipt a round certifies must state in its own bytes the
revision it was measured against, and the lane's certification path must run
`tools/receipt-revision-gate.py` over it — refusing a receipt whose named revision differs in
content on the declared surface (`RECEIPT_REV_CONTENT_DRIFT`), does not resolve
(`RECEIPT_REV_UNRESOLVABLE`), names no revision (`RECEIPT_REV_ABSENT`), or whose path does
not exist (`RECEIPT_MISSING`).

**Enforcement surface confirmed at C0 (the criterion's `docs=4/4` arm):** the gate name and
the `RECEIPT_*` codes are in `corpus/QUALITY.md` (lines 1620–1626, 1639), the sourced
knowledge entry `corpus/knowledge/receipt-revision-binding.md` exists with `source:` /
`verified-at:` / `recheck:` and S281, `SKILL.md`'s `## Standing rules` names the gate, and
`tools/registry.json` carries the gate with 11 of 11 codes. The frozen C2 counter's docs arm
reads `docs=4/4` at C0 and `docs=0/4` at the freeze — matching the criterion's own claim
about the freeze (receipt `06`).

---

## 2. The command, and both outputs

The criterion's fenced block (reproduced verbatim from `corpus/QUALITY.md:1636-1644`):

```
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 "$L/tools/receipt-revision-gate.py" \
  --lane "$L" --certified c21081008adbb6b6fe4e58a0aeec4831b30e318c \
  --paths "$L/.ufo/evidence/round-56/c2/red-before/round-54-surface.paths" \
  --receipt "$L/.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout:positive"
echo "exit=$?"
```

### 2a. On the real receipt — the falsifier FIRES exactly as the criterion states

Run verbatim from `cwd=/tmp` (the criterion says "run from any cwd"). Receipt `01`:

```
GATE REFUSED /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout role=positive revs=077d431e6996 code=RECEIPT_REV_CONTENT_DRIFT rev=077d431e6996 drift=.ufo/evidence/round-21/coldread/ledger.json,.ufo/waves/round-54/w1/T54W1Crit02-receipts/coldread-at-base.json,.ufo/waves/round-54/w1/T54W1Crit02-receipts/coldread-at-c0.json,.ufo/waves/round-54/w1/T54W1ExecC2Counter-receipts/counter-run-B-strace-registry-check.log,.ufo/waves/round-54/w1/T54W1ExecC2Counter-receipts/counter-run-c0-pinned-current.txt,.ufo/waves/round-54/w1/T54W1ExecC2Counter.md
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED
exit=3
```

The criterion requires `code=RECEIPT_REV_CONTENT_DRIFT` on the `GATE REFUSED` line,
`codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED` on the summary line, and exit 3.
**All three are exactly as claimed.** The refused receipt is the real one
(`.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout`); its only `rev=` is
`077d431e6996` (the round-54 freeze) while round 54 certified `c2108100` — confirmed by
`.ufo/evidence/round-54/after/frozen.stdout`
(`FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb…`).

### 2b. On a receipt that names the certified revision — it does NOT refuse

Two independent receipts, receipt `03`:

```
$ python3 "$L/tools/receipt-revision-gate.py" --lane "$L" \
    --certified c21081008adbb6b6fe4e58a0aeec4831b30e318c \
    --paths "$L/.ufo/evidence/round-56/c2/red-before/round-54-surface.paths" \
    --receipt "$L/.ufo/evidence/round-54/after/c1.stdout:positive"
GATE OK …/round-54/after/c1.stdout role=positive revs=c21081008adb
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
exit=0
```

A real round-54 receipt whose `rev=` IS the certified revision is accepted, exit 0.

The criterion's own green case (same receipt, `--certified` set to its own revision
`077d431e69965fa4673cd006ab64f6fc387f9e15`), verbatim, receipt `02`:

```
GATE OK …/round-54-ctl-pos-c1.stdout role=positive revs=077d431e6996
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
exit=0
```

The criterion states this must print `verdict=PASS` and exit 0 "so the refusal is a content
comparison and not a constant". **It does.**

### 2c. The gate also refuses what round 54 accepted (the claim's "real receipts" half)

```
$ … --receipt "$L/.ufo/evidence/round-54/control/controls-b.stdout:positive"
GATE REFUSED … codes=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED
exit=3
```

`7df0e0426c98` (named on `CTL_EXIT0`) does not resolve in the lane
(`git rev-parse --verify 7df0e0426c98^{commit}` → `fatal: Needed a single revision`), and
round 54's deciding run nevertheless exited 0
(`.ufo/evidence/round-54/after/deciding-run.exit` = `DECIDING_RUN_EXIT=0`). The round-56
gate refuses it. `RECEIPT_MISSING` fires for a nonexistent path (receipt `03`).

**Verdict on the criterion's claim: it fires exactly as written.** The criterion's numbers
(`code=RECEIPT_REV_CONTENT_DRIFT`, `codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED`,
exit 3), its red/green pair, and the freeze-state claims (`docs=0/4`, `NO-HIT` for
`receipt-revision-gate|RECEIPT_` in the freeze's `QUALITY.md`, gate + frozen receipt present
at the freeze, `DECIDING_RUN_EXIT=0`) are all reproduced by the commands above.

---

## 3. Findings

Two findings. Neither is a defect in the criterion's rule text or in the gate; one is a
citation that does not resolve, and one is a citation whose *anchor* points at the wrong
lesson section. Per the seat contract I do not edit `SKILL.md` or `corpus/QUALITY.md` —
both are adjudicated by the L1 and deferred to round 57.

### F1 (minor) — the criterion cites a lesson section that does not contain the cited content

The criterion's `Lesson:` line (`corpus/QUALITY.md:1653-1657`) reads:

> Lesson: `corpus/lessons/round-56.md` `## Gate` (the R55.5 disposition — round 55's deciding
> gate could not compare the revision it certifies, and the round-54 control set the old path
> accepted names `077d431e6996` on `CTL_POS_c1` and `7df0e0426c98` on `CTL_EXIT0` while the
> round measured `c2108100`).

The lesson's `## Gate` section (heading at `corpus/lessons/round-56.md:15`, running to
`## Mistakes` at `:38`) is the **sources-opened table** (S281 / DSSE / S282). It contains none
of the cited content:

```
$ sed -n '/^## Gate (sources opened this round)/,/^## Mistakes/p' corpus/lessons/round-56.md \
    | grep -n -E 'R55|deciding|rev=|077d431e|7df0e0426c98|c2108100'
NO-HIT: '## Gate' contains none of the cited content
```

The R55.5 disposition actually lives in a different section — `## Round-55 routed defects —
dispositions (this round)` (`corpus/lessons/round-56.md:91`, row at `:99`) — and the lesson
never mentions two of the three revisions the criterion attributes to it:

```
$ for t in 077d431e 7df0e0426c98 c2108100; do printf '%s: ' "$t"; grep -c "$t" corpus/lessons/round-56.md; done
077d431e: 1
7df0e0426c98: 0
c2108100: 0
```

The single `077d431e` hit is at `corpus/lessons/round-56.md:117`
(`rev=077d431e6996 credited=99 lost=0` → `verdict=PASS`), in `## What the counters cannot
see` — a different section again, and a different point than the one cited.

This is criterion 34's failure mode (an anchored citation that does not carry the quoted
content): the paragraph anchor names a heading, but the named heading is not the one that
holds the claim. The *facts* the criterion states are true of the tree — `CTL_POS_c1` does
name `077d431e6996`, `CTL_EXIT0` does name `7df0e0426c98`, and round 54 did measure
`c2108100` (`.ufo/evidence/round-54/after/c1.stdout`:
`C1_R54: rev=c21081008adb … C1_R54_PASS=true`) — so the defect is the anchor, not the claim.

**Flip / fix (for the L1, deferred to round 57):** re-anchor the `Lesson:` line to
`## Round-55 routed defects — dispositions (this round)` (or to a quoted sentence that
actually carries the R55.5 disposition). Do not rewrite the quoted facts.

### F2 (minor) — the criterion's scope-gap receipt pointer does not resolve at C0

The criterion's scope paragraph cites
`.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`.
Criterion 97 requires every backticked lane path a QUALITY block cites as evidence to exist
in the tree of the round's landing tip. The lane's own criterion-97 checker over the
round-56 QUALITY block at C0 reports it missing and exits 1:

```
$ python3 .ufo/evidence/round-48/quality/pointer-check.py --lane "$L" \
    --rev c0137451f5b7f22d65f748fc69f1b181f55e1378 --file corpus/QUALITY.md \
    --start "## Criteria appended — round 56"
MISSING .ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt
POINTERS: file=corpus/QUALITY.md checked=6 missing=1 skipped=0 rev=c0137451f5b7f22d65f748fc69f1b181f55e1378
exit=1
```

The file exists on disk (wave-1 output) but the whole `.ufo/waves/round-56/` tree is
uncommitted (`git ls-files .ufo/waves/round-56` → `0`; `git status --porcelain
.ufo/waves/round-56` → `?? .ufo/waves/round-56/`). This is an ordering fact of the round,
not a defect in the criterion's prose: once the wave-1 receipts are committed by the L1, the
pointer resolves. It is reported because the criterion text is already committed at C0 and
its scope claim is carried by that path.

I reproduced the scope gap the criterion declares, so the claim itself is sound: a receipt
naming the certified revision whose printed numbers are fabricated still passes.

```
$ printf 'CTL CTL_POS_c1 C1_R54: rev=077d431e6996 c0=99c3bc88d704 credited=99 lost=0 …\n' > fabricated.stdout
$ python3 "$L/tools/receipt-revision-gate.py" --lane "$L" \
    --certified 077d431e69965fa4673cd006ab64f6fc387f9e15 \
    --paths "$L/.ufo/evidence/round-56/c2/red-before/round-54-surface.paths" \
    --receipt …/fabricated.stdout:positive
GATE OK … role=positive revs=077d431e6996
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
exit=0
```

Note for the L1: the committed scope-gap receipt file records only the gate's `GATE OK` /
`verdict=PASS` / `exit=0` lines; the fabricated input itself lives only in wave-1's scratch
(`/fast/scratch/hyaku/tameshi-r56/T56W1ScribeQuality/fabricated.stdout`), outside the repo.
`grep -c 'credited=99'` on the committed receipt returns `0`. The criterion quotes the
receipt as showing "exit 0 on `rev=077d431e6996 credited=99 lost=0`"; the committed file
does not itself carry the `credited=99 lost=0` text. The claim is true and I reproduced it,
but the quoted numbers live in the scratch input, not in the committed receipt.

---

## 4. Notes (not findings)

- **The criterion's rule text covers one code the gate can also emit.** The criterion's rule
  sentence names `RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_REV_UNRESOLVABLE`,
  `RECEIPT_REV_ABSENT` and `RECEIPT_MISSING`. Run without `--paths`, the same receipt is
  refused `RECEIPT_REV_MISMATCH` instead (the gate's `paths is None` branch,
  `tools/receipt-revision-gate.py:149-152`). That is correct behaviour for a strict
  comparison with no declared surface, and the criterion's rule text is scoped to the
  surface-declared case, so this is not a mismatch. Worth knowing for any reader who
  invokes the gate without `--paths`.
- **The content-identical clause in the rule text is real and is not exercised by the
  criterion's own red/green pair.** The rule says a receipt whose named revision is
  content-identical to the certified revision "on the surface the round declares with
  `--paths` is accepted even when the two shas differ". My fixture (two commits differing
  in `other.txt` only, `--paths` file listing `surface.txt`) confirms the gate does this:
  different sha + unchanged surface → `GATE OK … verdict=PASS`, exit 0; changed surface →
  `code=RECEIPT_REV_CONTENT_DRIFT`, exit 3 (receipt `04`).
- **The criterion's named red/green pair does not by itself discriminate a content-comparing
  gate from a sha-equality-only gate.** A mutant that replaces the content comparison with
  "sha differs ⇒ drift" passes BOTH of the criterion's named commands unchanged (receipt
  `05`: red still `codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED` exit 3; green still
  `verdict=PASS` exit 0). It is killed only by the tool's own `--selftest`
  (`CASE content-identical-positive-accepted FAIL`, `GATE_SELFTEST: 18/19 pass`,
  `REAL_EXIT=1`) — which the frozen C2 counter's arm 1 does run
  (`EXPLAIN arm1-selftest exit=0 19/19`). The tool is therefore covered; the criterion's
  *named* falsifier is weaker than the tool's coverage. Not a defect in the criterion's
  claims (it never asserts the pair isolates content comparison from sha comparison), but
  a reader should not treat the red/green pair as proof that the comparison is
  content-based. This mirrors the lane's criterion-29 "a guard is covered only when its
  removal makes the owning `--selftest` exit nonzero" reading, which the tool satisfies.
- The gate's `--selftest` at C0 prints `GATE_SELFTEST: 19/19 pass`, exit 0. The gate blob
  changed between the freeze and C0 (freeze `c93c1357…` → C0 `c77e91a2…`), and that
  amendment is recorded in `freeze.json` amendment 1, which names the gate and states the
  repair was made before any control score or deciding invocation. Working-tree bytes
  match the C0 blob (`sha256 c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9`).
- **Census:** `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` exits **0**. The census reports `rows 142` for
  `tameshi` — 140 at base `981c5e8b` + the round's two new rows `S281` and `S282` added at
  C0. The seat brief stated "141 rows after this round's one new row"; the round in fact
  adds two rows (`S281` mined, `S282` rejected-but-kept), so the count is 142, not 141. The
  validate gate exits 0 either way; flagging the number so the L1 does not write 141 into
  the lesson or closure.

---

## 5. Commands run

```
git show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/QUALITY.md            # criterion number + text
git diff 21eb3c6 c0137451 -- corpus/QUALITY.md                                  # C0 added criterion 107 only
git ls-tree / git show <rev>:corpus/QUALITY.md                                  # freeze-state NO-HIT check
git ls-tree <rev> tools/receipt-revision-gate.py .ufo/evidence/round-56/c2/red-before/
git -C "$L" rev-parse --verify 7df0e0426c98^{commit}                          # unresolvable
git -C "$L" show <rev>:.ufo/evidence/round-54/after/{c1.stdout,deciding-run.exit,frozen.stdout}
sha256sum tools/receipt-revision-gate.py

python3 "$L/tools/receipt-revision-gate.py" --lane "$L" --certified c2108100… --paths … \
    --receipt …/round-54-ctl-pos-c1.stdout:positive          # RED  (exit 3, drift code)
python3 "$L/tools/receipt-revision-gate.py" --lane "$L" --certified 077d431e… --paths … \
    --receipt …/round-54-ctl-pos-c1.stdout:positive          # GREEN (exit 0, PASS)
python3 "$L/tools/receipt-revision-gate.py" --lane "$L" --certified c2108100… --paths … \
    --receipt "$L/.ufo/evidence/round-54/after/c1.stdout:positive"   # real certified-rev receipt (PASS)
python3 "$L/tools/receipt-revision-gate.py" --lane "$L" --certified c2108100… \
    --receipt "$L/.ufo/evidence/round-54/control/controls-b.stdout:positive"  # UNRESOLVABLE
python3 "$L/tools/receipt-revision-gate.py" … --receipt "$L/nope.stdout:positive"  # RECEIPT_MISSING
python3 "$L/tools/receipt-revision-gate.py" … --receipt … (no --paths)            # RECEIPT_REV_MISMATCH
python3 "$L/tools/receipt-revision-gate.py" --selftest                     # GATE_SELFTEST: 19/19 pass
python3 "$L/.ufo/evidence/round-56/c2/measure.py" --lane "$L" --rev <freeze|C0> --work <empty> --explain
python3 "$L/.ufo/evidence/round-48/quality/pointer-check.py" --lane "$L" --rev <C0> \
    --file corpus/QUALITY.md --start "## Criteria appended — round 56"
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Mutation probe (scratch copy of the gate, not the lane): the content-comparison branch
replaced by "sha differs ⇒ drift"; both criterion commands re-run against it; the tool's
`--selftest` re-run against it.

Receipts: `.ufo/waves/round-56/w2/T56W2RevQuality-receipts/`
(`00-context.txt`, `01-criterion107-red-verbatim.txt`, `02-criterion107-green-verbatim.txt`,
`03-real-receipts-and-codes.txt`, `04-content-identical-clause.txt`, `05-mutant-probe.txt`,
`06-freeze-state-falsifier.txt`, `07-citation-anchors.txt`).

## 6. Tooling

No tool was installed or upgraded for this seat. Everything used (`git`, `python3` stdlib,
`sed`, `grep`, `mktemp`) was already present. The `sed`/`grep` uses are literal text
searches over receipt/citation text, not structural code search.

## 7. Residual risk / verification gaps

- The round-55 and round-56 receipt sets were exercised only on the two receipts the
  criterion names plus the round-54 pair; the gate's other nine refusal codes
  (`RECEIPT_EMPTY`, `RECEIPT_NOT_BLOB`, `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_CONTROL_NOT_ANCESTOR`,
  `RECEIPT_DIGEST_MISMATCH`, `RECEIPT_REQUIRED_LINE_MISSING`) were exercised by the tool's own
  `--selftest`, not by me independently against the lane.
- F1 and F2 are text-level defects in `corpus/QUALITY.md`. I did not edit it; per the seat
  contract a text fix costs eighteen re-reads, so both are for L1 adjudication and deferral
  to round 57, named in the lesson.
- The census row count is 142, not the 141 the seat brief expected (see Notes); if the L1's
  closure text asserts 141 it will be wrong.
