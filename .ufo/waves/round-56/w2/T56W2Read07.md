# T56W2Read07 — `## Standing rules` re-read at C0

- **Heading:** `## Standing rules`
- **Candidate:** `c0137451f5b7f22d65f748fc69f1b181f55e1378` (round-56 C0 — "receipt-binding rule (SKILL standing rules), QUALITY criterion 107, knowledge entry receipt-revision-binding, SOURCES S281-S282, lesson round-56, registry cell, before/ receipts, assimilation + census-start evidence")
- **Section:** `SKILL.md` lines **17–57** at C0 (next heading `## Source notes` at :58), 3292 bytes
- **`section_sha256`:** `28bde4663c463ad40eba050dc9e5a97c6ed68148414cdfaf6d36789db5160bcc`
  - computed with the **FROZEN** round-18 sectionize (`.ufo/evidence/round-18/measure.py`, loaded by `importlib`, run over `git show c0137451:SKILL.md`) → `start=17 end=57`, same digest;
  - cross-checked by an independent byte-level recomputation of lines 17–57 with trailing blank lines stripped → same digest. Receipt `r07-section-hash.txt`.
- **Verdict:** **`gap-minor`** — 3 findings (F1, F2, F3), all measured at C0 with a command and its output.
- **Seat:** T56W2Read07, wave-2 cold-read reader, milestone *cold-read re-read 7/18*, axis *calibration*.

## Environment

- Lane read-only at `c0137451f5b7f22d65f748fc69f1b181f55e1378` via `git show` / `git grep` / `git ls-tree`; **no** lane production file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`) and **no** frozen instrument under `.ufo/evidence/round-56/` was edited.
- Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W2Read07/` — a `git clone --shared` of the lane with `git checkout --detach c0137451f5b7f22d65f748fc69f1b181f55e1378`; `git -C <clone> rev-parse --show-toplevel` asserted equal to the clone dir before any write there. **No mutating git/jj command was run anywhere.**
- No tool was installed or upgraded (none needed); no `pacman` transaction.

## Commands run

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md | sed -n '17,57p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -n -E 'hyaku/tameshi-r55-[A-Za-z0-9_]+|/tmp/tameshi-r55-grammarbreak' c0137451f5b7f22d65f748fc69f1b181f55e1378 -- .
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -o -h -E '(var/)?tmp/tameshi-r[0-9]+-[A-Za-z0-9_]+' c0137451f5b7f22d65f748fc69f1b181f55e1378 -- . | sed -E 's/.*tameshi-(r[0-9]+)-.*/\1/' | sort | uniq -c
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:.ufo/waves/round-55/w1/T55W1ExecNoHarm.md | sed -n '186,191p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:.ufo/waves/round-55/w1/T55W1ExecFooterPaths-receipts/06-tmp-scratch.txt | sed -n '1,14p'
cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && python3 tools/receipt-revision-gate.py --lane /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone --certified c21081008adbb6b6fe4e58a0aeec4831b30e318c --paths /fast/scratch/hyaku/tameshi-r56/T56W2Read07/gate/r54surface.paths --receipt /fast/scratch/hyaku/tameshi-r56/T56W2Read07/gate/r54slice.stdout:verdict
cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && python3 tools/receipt-revision-gate.py --lane /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone --certified c21081008adbb6b6fe4e58a0aeec4831b30e318c --receipt /fast/scratch/hyaku/tameshi-r56/T56W2Read07/gate/r54slice.stdout:verdict
cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r56/T56W2Read07/no-such-tmpdir python3 tools/bash-witness-study.py selftest
cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r56/T56W2Read07/no-such-tmpdir python3 tools/env-diff.py --selftest
cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && python3 tools/receipt-revision-gate.py --selftest
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c0137451f5b7f22d65f748fc69f1b181f55e1378 --work /fast/scratch/hyaku/tameshi-r56/T56W2Read07/r55c2work --explain
cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Receipts: `.ufo/waves/round-56/w2/T56W2Read07-receipts/` (r01–r12).

## The section at C0 (verbatim, lines 17–57)

```
## Standing rules

- Read-only substrates unless PROVINCE.md declares a write surface;
  detection-and-report for operator-owned remediation.
- Secrets shape-only, never content-read.
- Every claim: measured anchor (path:line, command output, evidence id).
  Observation / inference / unknown stay separate.
- Errata append-only: new errata entries are appended and prior entries never
  rewritten; a documented correction may supersede an entry's content and the
  block says so (the round-16 errata block, `## Errata — round 16 full-page
  cold-read`, discloses its own in-place repairs). Rejections kept.
- **Scratch namespace is `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)/`<lane>-r<round>/<sub>/`** (host scratch directive of 2026-10-25: `/tmp` is for files under 50 MB only; a seat deletes its tree on exit; the shape every landed round since 48 uses (w1/w2 occurrence counts: 0 dash-form seat trees across rounds 48-52, thousands of the slash form; the dash form survives only in run artifacts and quoted text of rounds 37-52, not as a live convention [round 53 correction of the round-53 'rounds 25-36' overstatement, seat T53W2R4]))
  (in the original `/tmp` namespace: both mutation lanes kept every mutant + evidence there —
  mutation-case-kimi-census.md:4-7; mutation-case-kagi-census.md:4-6). The
  substrate tree is never a mutation target.
- **The scratch root has three arms.** A tool that allocates scratch through
  `strict_scratch_root()` honours `TMPDIR`: unset → the platform default; empty
  (`TMPDIR=""`) → unset (the resolver skips an empty candidate, S278:163-165; the
  documented list follows, S279); set but unusable → exit 2, could-not-evaluate,
  naming the value — never a silent `/tmp` fallback, never a traceback, never exit
  1. Measured on every documented allocating mode — the seven self-tests plus
  `env-diff --contract` and `registry-check --rev` — as one stderr line,
  `<tool>: could-not-evaluate: cannot create clone scratch under the scratch root:
  TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`, exit 2; the
  five non-allocating modes stay lazy (round-55 C2 counter;
  corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root`
  cells).

- **A receipt is evidence only for the revision it names.** A verdict or a
  positive-control receipt is bound to the revision it certifies by
  `tools/receipt-revision-gate.py --lane LANE --certified REV`: a receipt that
  names another revision is refused with a named code, never re-read as if it
  had been measured at the certified one (round-56 C2; ER-R54-1, R55.5).

  | situation | rule | code |
  |---|---|---|
  | a verdict receipt names another revision | refused unless its bytes equal the certified revision on the declared `--paths` surface | `RECEIPT_REV_MISMATCH` |
  | a positive control was scored at the freeze | refused: the freeze predates the work it certifies and drifts on the frozen surface | `RECEIPT_REV_CONTENT_DRIFT` (no `--paths`: `RECEIPT_REV_MISMATCH`) |
  | a control set's CTL lines name a revision absent from the repo | refused: the revision cannot be resolved, so nothing is certified | `RECEIPT_REV_UNRESOLVABLE` |
  | a receipt names no revision at all | refused: nothing is bound | `RECEIPT_REV_ABSENT` |
```

## Findings (3)

### F1 — the dash-form clause's end boundary (37-52) is stale at C0, and one of its halves is contradicted

**Quote.** "the dash form survives only in run artifacts and quoted text of rounds 37-52, not as a live convention [round 53 correction of the round-53 'rounds 25-36' overstatement, seat T53W2R4])"

**Why.** The dash form survives past 52 in round-55 objects, and one of them is a **live dash-form seat tree under the default base** — a seat's actual scratch root, not a quotation and not a run artifact of rounds 37-52:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:.ufo/waves/round-55/w1/T55W1ExecNoHarm.md | sed -n '186,191p'
- My seat scratch root `/fast/scratch/hyaku/tameshi-r55/T55W1ExecNoHarm` disappeared mid-wave (between
  two of my own calls); `c2/measure.py` contains no `rmtree`, so a peer's cleanup of the shared
  `tameshi-r55` scratch root is the plausible cause. Nothing in the deliverables was lost — receipts
  live in this directory, not in scratch. I re-rooted later scratch at
  `/fast/scratch/hyaku/tameshi-r55-noHarmC2/` and removed it on completion.
```

Two more live dash-form trees from the same round sit under `/tmp`:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:.ufo/waves/round-55/w1/T55W1ExecFooterPaths-receipts/06-tmp-scratch.txt | sed -n '1,14p'
COMMAND: find /tmp -maxdepth 1 -name '*tameshi-r55*'; du -sh matching trees
--- strict tameshi-r55 match ---
2026-10-28 14:02 /tmp/tameshi-r55-grammarbreak
2026-10-28 14:19 /tmp/tameshi-r55-grammarbreak2
--- sizes ---
1.5G	/tmp/tameshi-r55-grammarbreak
68K	/tmp/tameshi-r55-grammarbreak/integration.patch
261M	/tmp/tameshi-r55-grammarbreak/patched
20K	/tmp/tameshi-r55-grammarbreak/receipts
250M	/tmp/tameshi-r55-grammarbreak/wt-1
250M	/tmp/tameshi-r55-grammarbreak/wt-2
250M	/tmp/tameshi-r55-grammarbreak/wt-2b
250M	/tmp/tameshi-r55-grammarbreak/wt-3
250M	/tmp/tameshi-r55-grammarbreak/wt-4
```

The full dash-form census over every committed blob at C0, bucketed by the round that **owns** the object, puts hits beyond the 47 run-artifact range at r53 (12) and r55 (20); rounds 48–52 have no entry at all:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -o -h -E '(var/)?tmp/tameshi-r[0-9]+-[A-Za-z0-9_]+' c0137451f5b7f22d65f748fc69f1b181f55e1378 -- . | sed -E 's/.*tameshi-(r[0-9]+)-.*/\1/' | sort | uniq -c
   37: 18   38: 7   39: 152   40: 162   41: 211   42: 150   43: 243   44: 113
   45: 1700  46: 586  47: 380   53: 12    55: 20
```

**Checked and not filed:** the 12 `r53` hits all live inside `.ufo/evidence/round-17/coldread/traces/CR53/*.json`, objects committed by `fad9e95` (round-17 wave-2 landing); their `r53` token is a cold-read case id, not the owning round, so round 53 is not a dash-form round.

**Provenance:** this is round 55's wave-2 reader finding at r55's C0 (`.ufo/waves/round-55/w2/T55W2Read01.json` finding 2). Round 55 was rejected-harmed, so the repair never landed and the round-56 C0 page still carries the stale boundary.

**Clause halves that DO hold at C0** (not disputed): "0 dash-form seat trees across rounds 48-52" (0 hits of any kind, over both the `/tmp` and the default base) and "thousands of the slash form" (r48=305 r49=638 r50=4822 r51=2258 r52=160 r53=581 r54=6153 r55=4512).

**Smallest correction (not applied — the L1 defers text fixes to round 57):** extend the range to cover round 55, or drop the "not as a live convention" half, or scope the clause to the run-artifact range it actually measures.

---

### F2 — the receipt code table keys codes to the receipt's *role*; the tool keys them to `--paths`

**Quote.** Row 1 `| a verdict receipt names another revision | refused unless its bytes equal the certified revision on the declared --paths surface | RECEIPT_REV_MISMATCH |` and row 2 `| a positive control was scored at the freeze | ... | RECEIPT_REV_CONTENT_DRIFT (no --paths: RECEIPT_REV_MISMATCH) |`.

**Why.** `tools/receipt-revision-gate.py` takes `positive` and `verdict` in **one branch**; the code is chosen by whether `--paths` was declared and whether the named surface drifted. Measured on the **real** round-54 receipt at C0, the same bytes give identical codes as either role:

```
$ cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && python3 tools/receipt-revision-gate.py --lane /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone --certified c21081008adbb6b6fe4e58a0aeec4831b30e318c --paths /fast/scratch/hyaku/tameshi-r56/T56W2Read07/gate/r54surface.paths --receipt /fast/scratch/hyaku/tameshi-r56/T56W2Read07/gate/r54slice.stdout:verdict
GATE REFUSED ... role=verdict revs=077d431e6996 code=RECEIPT_REV_CONTENT_DRIFT rev=077d431e6996 drift=.ufo/evidence/round-21/coldread/ledger.json,.ufo/waves/round-54/w1/T54W1Crit02-receipts/coldread-at-base.json,...
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED
exit=3
```

The same receipt as `role=positive` gives the identical `codes=RECEIPT_REV_CONTENT_DRIFT`; the same receipt **without** `--paths` gives the mismatch code:

```
$ cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && python3 tools/receipt-revision-gate.py --lane /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone --certified c21081008adbb6b6fe4e58a0aeec4831b30e318c --receipt /fast/scratch/hyaku/tameshi-r56/T56W2Read07/gate/r54slice.stdout:verdict
GATE REFUSED ... role=verdict revs=077d431e6996 code=RECEIPT_REV_MISMATCH rev=077d431e6996 certified=c21081008adb
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_MISMATCH verdict=REFUSED
exit=3
```

So row 1's code cell (`RECEIPT_REV_MISMATCH`) is **not** what a verdict receipt naming another revision yields on the declared `--paths` surface that row 1's own rule cell names. The lane's own sourced entry says so: `corpus/knowledge/receipt-revision-binding.md:34` — "identical to `positive` (the code takes the two roles in one branch)". The round-56 C2 counter gates the very same receipt as `role=positive` **with** `--paths` and expects `RECEIPT_REV_CONTENT_DRIFT` (arm `red54`, `.ufo/evidence/round-56/c2/measure.py:153-160`) — the counter and the page disagree about which situation carries which code. A reader who gates a verdict receipt on a drifted surface and expects `RECEIPT_REV_MISMATCH` per row 1 will misread the refusal.

**Rows 3 and 4 re-measured and hold.** A control set naming an absent revision → `RECEIPT_REV_UNRESOLVABLE` (exit 3); a receipt naming no revision at all → `RECEIPT_REV_ABSENT` (exit 3). Also measured: the round-54 control set gated as `role=control` **or** `role=positive` both give `RECEIPT_REV_UNRESOLVABLE` — again the role is not the discriminator.

**Smallest correction (not applied):** re-key the table's `situation` column on `--paths`/drift rather than on the receipt's role, so one code owns one situation.

---

### F3 — the quoted stderr byte-shape names `<tool>:`, but three of the nine measured modes print another token

**Quote.** "Measured on every documented allocating mode — the seven self-tests plus `env-diff --contract` and `registry-check --rev` — as one stderr line, `<tool>: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`, exit 2".

**Why.** The prefix is the tool's own token, and for two tools it is not the tool's name:

```
$ cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r56/T56W2Read07/no-such-tmpdir python3 tools/bash-witness-study.py selftest
WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r56/T56W2Read07/no-such-tmpdir' (could-not-evaluate)
exit=2

$ cd /fast/scratch/hyaku/tameshi-r56/T56W2Read07/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r56/T56W2Read07/no-such-tmpdir python3 tools/env-diff.py --selftest
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r56/T56W2Read07/no-such-tmpdir' (could-not-evaluate)
exit=2
```

`env-diff --contract` prints `ENVDIFF_SETUP:` as well. So 3 of the 9 modes the sentence names (`bash-witness-study selftest`, `env-diff --selftest`, `env-diff --contract`) break a reader who matches the line by the tool's name. The **class half of the rule holds 9/9**: every mode exits 2 with exactly one stderr line, no `RuntimeError` and no `Traceback` token, and the value is named — this is a defect of the quoted shape only, not of the tools.

The lane has already adjudicated the identical defect in the sibling artifact the page cites in the same breath. Round-55 adjudication **W2-TOOLDIFF-F3** accepted that "the seven registry cells quoted `<tool>.py` while repeat-control prints `repeat-control:`, bash-witness prints `WITNESS_STUDY:` and env-diff prints `ENVDIFF_SETUP:` — 4/7 cells false" and fixed each cell to quote the token its tool actually prints. At C0 the registry cells are fixed; this page's copy of the shape is not:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:tools/registry.json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(r['name'],'->',r['scratch_root'].split('the token this tool actually prints: ')[-1][:70]) for r in d['rows'] if r.get('scratch_root')]"
repeat-control-selftest -> "repeat-control: could-not-evaluate: cannot create clone scratch under
bash-witness-selftest -> "WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under
pin-disposition-selftest -> "pin-disposition.py: could-not-evaluate: cannot create clone scratch u
evidence-disposition-selftest -> "evidence-disposition.py: could-not-evaluate: cannot create scra
context-capture-selftest -> "context-capture.py: could-not-evaluate: cannot create clone scratch
registry-check-selftest -> "registry-check: could-not-evaluate: cannot create clone scratch under
env-diff-selftest -> "ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the
receipt-revision-gate-selftest -> Read-only on the lane: the receipt form ...
```

The same shape is quoted in the frozen note `corpus/knowledge/scratch-root-contract.md` ("One line, every mode (round 55)"), which the page cites.

**Provenance:** round 55's wave-2 reader finding at r55's C0 (`T55W2Read01` finding 1); never landed, because round 55 was rejected-harmed.

## Holds (verified at C0)

| claim | how it was verified at C0 | result |
|---|---|---|
| `PROVINCE.md` exists and declares the lane's write scope | `git cat-file -e c0137451:PROVINCE.md`; read the file | present; "Also: this lane's own corpus and gates", "Out of province → report, never absorb" |
| the round-16 errata block named in the page exists and discloses its own in-place repairs | `SKILL.md:1750` heading `## Errata — round 16 full-page cold-read`; `SKILL.md:1758` | present; "The page edits are in-place repairs, and so are this table's own cells" |
| census anchors `mutation-case-kimi-census.md:4-7`, `mutation-case-kagi-census.md:4-6` | read both ranges at C0 | kimi: "every mutant is a copy under `/tmp/tameshi-r2-1-work/`"; kagi: "every mutant is a copy under `/tmp/tameshi-r3-1-work/`" |
| S278:163-165 and S279 | fetched CPython v3.12.7 `Lib/tempfile.py` → sha256 `fb44155f430fac1923d3d7b6af1a0210edcfb580291d664e66f338491d68b62b` (the sha SOURCES records); lines 163-165 are the `for envname in 'TMPDIR','TEMP','TMP'` / `if dirname: dirlist.append(dirname)` block; fetched `docs.python.org/3/library/tempfile.html` → the list begins "The directory named by the TMPDIR environment variable" | both resolve exactly |
| three arms of the scratch root | `TMPDIR` unset → `pin-disposition --selftest` exit 0; `TMPDIR=""` → `repeat-control --selftest` and `env-diff --selftest` exit 0; `TMPDIR=<unusable>` → exit 2 + one naming line, no traceback, for all nine allocating modes | holds |
| every documented allocating mode measured; five non-allocating modes lazy; no `/tmp` fallback | `python3 .ufo/evidence/round-55/c2/measure.py --lane … --rev c0137451f5b7f22d65f748fc69f1b181f55e1378 --work <empty dir> --explain` → `C2_R55: rev=c0137451f5b7 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true`; plus an independent `strace -f -e trace=mkdir,mkdirat` sweep (0 hits under `/tmp` for each of the eight cheap allocating modes, including `env-diff --contract`) | holds |
| the gate's own suite | `python3 tools/receipt-revision-gate.py --selftest` | `GATE_SELFTEST: 19/19 pass`, exit 0 |
| the gate refuses the real round-54 control (ER-R54-1) | gate run on `.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout` at `c2108100` | `RECEIPT_REV_CONTENT_DRIFT`, exit 3, drift names `.ufo/evidence/round-21/coldread/ledger.json` |
| `RECEIPT_REV_UNRESOLVABLE` and `RECEIPT_REV_ABSENT` rows | control set naming `7df0e0426c98`; receipt with no `rev=` | refused with the stated codes, exit 3 each |

## Notes (improvements / observations — not findings)

1. The page quotes the gate as `tools/receipt-revision-gate.py --lane LANE --certified REV`, but that form alone exits 1 with a usage error — `--receipt PATH:ROLE[:REGEX]` is mandatory. The complete form is in `corpus/knowledge/receipt-revision-binding.md` and in the registry cell; naming it (or pointing at the note) would save a reader the usage error.
2. At C0 the registry carries **eight** rows with a `scratch_root` cell (the seven tool rows plus the new `receipt-revision-gate-selftest` row the C0 commit itself added). The page's "the seven registry `scratch_root` cells" is right in the sense the counter measures (the seven tools that call `strict_scratch_root()`; the round-55 counter's docs arm reads `docs=7/7` at C0), but a reader grepping `registry.json` for `scratch_root` at C0 counts eight. Worth naming the scope.
3. "the seven self-tests plus `env-diff --contract` and `registry-check --rev`" = nine allocating modes, matching the frozen note's nine-mode list and the counter's 9/9 grammar arm at C0 — correct as written.
4. Lane-level, outside this section: the census validator exits 0 as required, but the tameshi row count is **142** at C0, not 141 — the C0 commit added two source rows (S281 and S282) to the 140 present at base `981c5e8b`. Flagged for the L1.
5. `PROVINCE.md` never uses the phrase "write surface"; it declares ownership and write scope in other words. The rule is about a declaration existing, not about a phrase — nothing in the tree contradicts it (same judgement as round 55's reader, `T55W2Read01` item 4c).
6. No `SKILL.md`, corpus, tools, registry or evidence file was edited by this seat; no git or jj mutation was run anywhere. No tool was installed or upgraded (none needed); no `pacman` transaction.

## Deliverables

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w2/T56W2Read07.json`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w2/T56W2Read07.md` (this file)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w2/T56W2Read07-receipts/` (r01–r12)
- Scratch `/fast/scratch/hyaku/tameshi-r56/T56W2Read07/` (clone + work dirs) removed before yield.
