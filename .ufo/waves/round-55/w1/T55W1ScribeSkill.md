# T55W1ScribeSkill — C2 rule sentence (`SKILL.md` `## Standing rules`)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (base `0a2010ac`, lane HEAD
`631cd6455e58dce969310b4c0466c3383d9f5108`). Judged on: operability. Milestone:
C2 SKILL.md rule sentence.

Item: read `## Standing rules`, draft the exact old→new replacement for the
round-54 sentence `Measured on each tool's --selftest/selftest path (round-54 C2
counter); other modes are outside that measurement`, keep line length and the
section's citation style, touch nothing else, and quote the section's sha256 at
base so the L1 can prove the drift is one section.

No lane production file was edited by this seat. Every measurement ran in a
scratch clone under `/fast/scratch/hyaku/tameshi-r55/T55W1ScribeSkill` (own git
toplevel, asserted before each commit); nothing was committed in the lane. The
lane working tree changed under this seat while it ran (round-55 integration of
the `registry-check --rev` fix, the note, the registry cells, `SKILL.md`, and the
counter); §3–§4 state which bytes each measurement used.

---

## 1. The replacement

### Old (base blob lines 37–39, verbatim; the tail of the third-arm bullet)

```
  1. Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter);
  other modes are outside that measurement (corpus/knowledge/scratch-root-contract.md;
  the seven registry `scratch_root` cells).
```

### New — two candidates, same claim, different wrap

**(a) As integrated in the lane at 2026-10-28 14:12** (`SKILL.md` sha256
`e0ce89f7866062062f4987358e353c8626c18f56d2eb1589225af99f44d695a6`):

```
  1. Measured on every documented allocating mode — the seven self-tests plus
  `env-diff --contract` and `registry-check --rev` — as one stderr line,
  `<tool>: could-not-evaluate: cannot create clone scratch under the scratch
  root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`, exit
  2; the five non-allocating modes stay lazy (round-55 C2 counter;
  corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root`
  cells).
```

Widths 77, 72, 76, 79, 66, 78, 9. `## Standing rules` sha256 **`acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767`**.
The 70-char grammar marker is split by a line break here, so it is present only
under the counter's whitespace normalization (amendment 2), not in raw bytes.

**(b) Recommended variant — identical claim, marker on one physical line**
(the only differences from (a): `exit 2:` closes the clause, and the code span
breaks after `scratch root:` instead of inside the marker):

```
  1. Measured on every documented allocating mode — the seven self-tests plus
  `env-diff --contract` and `registry-check --rev` — as one stderr line, exit 2:
  `<tool>: could-not-evaluate: cannot create clone scratch under the scratch root:
  TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`; the five
  non-allocating modes stay lazy (round-55 C2 counter;
  corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root`
  cells).
```

Widths 77, 80, 82, 77, 54, 78, 9 (the section's existing prose max is 82, old
line 36; the one intentional long line, line 28, is untouched). Marker present
**raw and normalized**. `## Standing rules` sha256
**`46980026b08a3c5d209d50668485099cd22653fffc678f7da7af82b2af1f5570`**.
Patch against the base blob: `-receipts/variant-b.patch`; the whole edited file is
`-receipts/variant-b.md` (sha256
`38c1ea5b17c8b5c8c36ab22c52ee8d5d1b0885a24a74501818c16ed92576c670`).

Both candidates replace exactly the three old lines (`@@ -34,9 +34,13 @@`) and
differ in nothing else; both are 199384 bytes against the base's 199128 (+256).

### Why each clause is true (evidence in §3)

- "every documented allocating mode — the seven self-tests plus
  `env-diff --contract` and `registry-check --rev`": the only
  `strict_scratch_root()` call sites in the seven tools are the six selftest
  entry points, `env-diff.execute()` (reached by `--selftest` and `--contract`)
  and `registry-check.clone_lane_at_rev()` (reached by `--rev`); the registry
  cells now name the same set. All nine were measured: exit 2, exactly one
  stderr line, frozen grammar, no `RuntimeError`/`Traceback` token. The one
  `TemporaryDirectory()` without `dir=strict_scratch_root()` (`env-diff.py:186`)
  is inside `selftest()` after the probe loop, so the refusal precedes it — and
  the measured stderr is exactly one line, which proves nothing ran before it.
- "as one stderr line … exit 2": nine for nine, one non-blank stderr line each.
- "the five non-allocating modes stay lazy": all five keep exit 0 under an
  unusable `TMPDIR`, with no stderr line, and none of them reaches a
  `strict_scratch_root()` call site.
- The round-54 clause ("other modes are outside that measurement") is false and
  is removed.

## 2. Drift accounting — one section, provable

Round-18 `sectionize` (the function the cold-read ledger keys on), base vs each
candidate (`-receipts/section-drift.txt`, `-receipts/variant-b.txt`):

| | start | end | sha256 | bytes |
|---|---|---|---|---|
| base `0a2010ac` | 17 | 40 | `61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc` | 199128 |
| integrated (14:12) | 17 | 44 | `acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767` | 199384 |
| variant (b) | 17 | 44 | `46980026b08a3c5d209d50668485099cd22653fffc678f7da7af82b2af1f5570` | 199384 |

`changed_headings=['## Standing rules']`; no heading added or removed; 64
sections before and after. Whichever candidate ships, the ledger re-key is that
single section sha and nothing else.

## 3. Measurements

**Mode sweep, unusable `TMPDIR`, post-fix working tree** (`-receipts/mode-sweep.json`;
snapshot inputs in `-receipts/inputs.sha256`, probe at rev `9de7deac0d72`):

| mode | rc | stderr lines | frozen GRAMMAR | `RuntimeError`/`Traceback` |
|---|---|---|---|---|
| env-diff --selftest | 2 | 1 | 1 | no |
| env-diff --contract | 2 | 1 | 1 | no |
| repeat-control --selftest | 2 | 1 | 1 | no |
| registry-check --selftest | 2 | 1 | 1 | no |
| registry-check --rev | 2 | 1 | 1 | no |
| bash-witness-study selftest | 2 | 1 | 1 | no |
| pin-disposition --selftest | 2 | 1 | 1 | no |
| evidence-disposition --selftest | 2 | 1 | 1 | no |
| context-capture --selftest | 2 | 1 | 1 | no |
| repeat-control --snapshot | 0 | 0 | – | no |
| bash-witness-study count | 0 | 0 | – | no |
| pin-disposition --read | 0 | 0 | – | no |
| evidence-disposition --json | 0 | 0 | – | no |
| context-capture --check | 0 | 0 | – | no |

Per-tool prefixes: `ENVDIFF_SETUP`, `repeat-control`, `registry-check`,
`WITNESS_STUDY`, `pin-disposition.py`, `evidence-disposition.py`,
`context-capture.py` — all inside the grammar's
`[A-Za-z][A-Za-z0-9_.-]*(\.py)?`.

**Counter, integrated-content snapshot** (`-receipts/c2-integrated.out`,
`-receipts/c2-integrated-receipts.json`). Snapshot = lane HEAD + the working-tree
`SKILL.md`, `tools/repeat-control.py`, `tools/context-capture.py`,
`tools/registry-check.py`, `tools/registry.json`,
`corpus/knowledge/scratch-root-contract.md`; seat commit
`08d64e946006a7fc631c5787879d1cd4f83ae7bd`; counter bytes pinned by copying them
to the seat scratch (sha256
`36ca47d36c4befc1148a911600c1a5c79efae5e4811f27fa2f9698c17b1ae786`):

```
C2_R55: rev=08d64e946006 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0
        docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

`bad={}` — **every arm is green and the counter still prints `PASS=false`**; see
F1. Exit status 1 (`return 0 if total == 0 and not bad else 1`).

**Counter, pre-amendment-6 bytes, earlier content** (`-receipts/c2-demo.out`,
8 allocating modes, counter sha `d6ca1d851bb0037368c304f4d80254f7dc5bf76b1c3119cdf0f2a64bca95631a`
recorded before that run; the file's next write was the 14:12 amendment, `seat
commit 9de7deac0d72`): `grammar=8/8 … total=0 C2_R55_PASS=true` — the same
tree family passed before the table grew a ninth mode and the bookkeeping with it.

**Marker predicates** (`-receipts/skill-arm-both-matchers.txt`): integrated text
raw `False`, normalized `True`; variant (b) raw `True`, normalized `True`. So
(a) needs amendment 2 to score `skill=1`; (b) does not.

## 4. Findings — reported, not fixed

**F1 (blocking, frozen counter bookkeeping; the round's C2 cannot print PASS at
all-green).** With amendment 6 the counter's table is 14 modes, 9 allocating,
13 `cheap` (only `registry-check --rev` is excluded from the empty/usable arms),
and the note denominator became `len(allocating)`. The totals were not updated
with them (`.ufo/evidence/round-55/c2/measure.py`):

```
218:  for ... in cheap:                       # empty/usable arms iterate 13
261:  ("note", note, len(allocating))         # 9
271:  total = (len(allocating) - grammar_ok) + (len(lazy) - lazy_ok) \
272:      + (len(table) - empty_ok) + (len(table) - usable_ok) \
273:      + tmp_total + (7 - docs) + (8 - note) + (1 - skill)
```

At the target state this evaluates to `0 + 0 + (14-13) + (14-13) + 0 + 0 +
(8-9) + 0 = 1`, so a fully green run scores `total=1`, `PASS=false` (measured
above). Minimal amendment that makes the arithmetic agree with the loops it
already runs: line 272 → `(len(cheap) - empty_ok) + (len(cheap) - usable_ok)`,
line 273 → `(len(allocating) - note)`; then `total = 0`. (The alternative —
running `--rev` through the empty and usable arms too — would add minutes per arm
to every run.) This is a contract amendment, so it is the L1's call; I did not
touch the file.

**F2 (resolved mid-run, recorded for the record).** At 14:01 `registry-check --rev`
was a documented allocating mode outside the 13-mode table and emitted the class
on **stdout** (`REGISTRY_CHECK: could-not-evaluate (...)`, rc 2, stderr empty).
The working tree now fixes it (`ScratchRootUnusable` + a stderr grammar line in
`main`), the registry cell reads `Allocating modes: selftest, --rev`, and the note
names nine modes; the sweep above measures the fixed behaviour, and amendment 6
adds it to the counter's grammar arm. Consequence for this sentence: the phrase
"every documented allocating mode" became true only with that fix, and it now
rests on (i) the cell/note enumeration and (ii) the counter measuring `--rev` on
the grammar arm only — both true at snapshot `08d64e94`.

**F3 (minor, adjacent).** `repeat-control --selftest` still writes
`REPEAT_CONTROL: setup_error` to stdout on the refusal path
(`-receipts/mode-sweep.json`). The frozen grammar arm reads exit code, stderr
shape and the `RuntimeError`/`Traceback` tokens only, so it passes; a stricter
reading of the round's "stdout carries no setup error" would want the token gone.
The sentence drafted here makes no stdout claim.

**F4 (process, unexplained).** The seat scratch tree
`/fast/scratch/hyaku/tameshi-r55/T55W1ScribeSkill` was removed by something other
than this seat twice while it ran (once between 13:53 and 13:54, once before the
integrated-snapshot run completed); sibling seat trees in the same parent were
untouched. Both times the measurements were rebuilt from the lane and re-run; all
receipts cited here come from complete runs on the files they name.

**F5 (no action).** Sources census `validate --root /home/vgpnk/Projects/shokunin
tameshi` exits 0 (`-receipts/census-validate.txt`). `corpus/SOURCES.md` now has
140 `| S### |` rows, S001–S280; S280 is the round's own row (SOURCES.md:155 and
the round-55 footer note), so the brief's "139 rows (S001–S279)" is the
round-start state.

## 5. Integration notes for the L1

1. Keep candidate (a) as integrated → re-key `## Standing rules` to
   `acfb671a…`. Switch to candidate (b) → re-key to `46980026…`. Nothing else in
   `SKILL.md` drifts either way (§2).
2. C2 cannot reach `PASS=true` until F1 is amended; the arms are already 9/9,
   5/5, 13/13, 13/13, 7/7, 9/9, 1/1 with `bad={}`.
3. If the ledger re-key is taken at the content commit, take the section sha from
   the committed bytes, not from this report — both candidate shas here are
   computed from working-tree bytes at 14:12–14:15.

## 6. Out of scope / not verified by this seat

`SCORECARD.md` corrections, `LOG.md`, `QUALITY.md`, `corpus/lessons/round-55.md`,
the cold-read ledger re-key itself, the deciding run, the no-harm monitors, and
the `registry.json` reformat (copied as-is and hashed only). No tool was installed
or upgraded; system `python3`, `git`, `strace` sufficed (pacman is paused
host-wide and was not touched).

## 7. Receipts

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/`

| file | what |
|---|---|
| `variant-b.patch`, `variant-b.txt`, `variant-block.txt` | candidate (b): diff against the base blob, its facts, and the earlier 8-line draft for reference |
| `skill-after.md`, `skill-section.patch` | the earlier 8-mode candidate as committed in the seat clone (`9de7deac`) |
| `section-drift.txt` | base vs 8-mode draft: one-section-changed proof, shas, widths |
| `mode-sweep.json` | 14 modes under unusable `TMPDIR`: rc, stderr line count, grammar match, tokens, plus the input sha256s |
| `skill-arm-both-matchers.txt` | marker under the raw (HEAD-frozen) and normalized predicates |
| `c2-integrated.out`, `.err`, `.rc`, `c2-integrated-receipts.json`, `c2-integrated-verdict.txt` | the pinned-counter run on the integrated snapshot: verdict line, `bad={}`, arm counts, and the arithmetic that yields `total=1` |
| `c2-demo.out`, `c2-demo-receipts.json`, `c2-measure.sha256` | the earlier 8-mode run (`total=0`) and the counter bytes pinned for the integrated run |
| `demo-commit.txt`, `inputs.sha256`, `integ-inputs.sha256` | seat-clone commits and the exact working-tree bytes copied into each snapshot |
| `census-validate.txt` | census `validate` exit 0 and row accounting |
| `RECEIPTS.sha256` | sha256 of the receipt files above |
