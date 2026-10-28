# T55W2MutC2 — mutation probe of the round-55 C2 counter (wave 2, falsify)

Seat: mutation tester. One claim under attack: **the frozen C2 counter at
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` is a real detector of the C2
operability class** (one stderr line, one exit class, control of docs/note/skill,
nine allocating modes).

Verdict in one line: all six assigned mutations are **KILLED** by a planted
defect tree, so every clause named in the tasking is load-bearing; but the probe
also found that **nothing pins the allocating-mode inventory to nine** — the
`note` arm's expectation is computed from the very list under test — and that
the verdict line hardcodes `note=%d/9`.

Work is in scratch clones only (`/fast/scratch/hyaku/tameshi-r55/T55W2MutC2`);
no lane production file, no frozen file and no wave spec was edited (see
*Restoration evidence*).

---

## 1. Target bytes

| thing | value |
|---|---|
| lane | `/home/vgpnk/Projects/shokunin/tameshi-shokunin` |
| rev under test (C0) | `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` |
| counter | `.ufo/evidence/round-55/c2/measure.py` at C0 |
| counter sha256 at C0 | `36ca47d36c4befc1148a911600c1a5c79efae5e4811f27fa2f9698c17b1ae786` |
| my byte-identical copy | `T55W2MutC2-receipts/counters/pristine.py` (same sha) |
| baseline receipt quoted | `.ufo/evidence/round-55/before/c2.stdout` (base `0a2010ac`: `grammar 6/9`, `total=21`) |

The lane's freeze **pointer** has since moved to `133b2ce` (amendment 8), whose
only change to the counter is the aggregate line:

```
-        + (len(table) - empty_ok) + (len(table) - usable_ok) \
-        + tmp_total + (7 - docs) + (8 - note) + (1 - skill)
+        + (len(cheap) - empty_ok) + (len(cheap) - usable_ok) \
+        + tmp_total + (7 - docs) + (len(allocating) - note) + (1 - skill)
```

so the C0 bytes carry a known **aggregate bias**: the empty/usable terms compare
`len(table)`=14 against counters that only ever run the 13 `cheap` modes (+2), and
the note term compares against a ceiling of 8 while the note arm's want is 9 (−1)
— net +1 on an all-green tree (measured below: the green tree at C0 reads
`total=1 C2_R55_PASS=false` with an empty `bad` map). Mutants
are built on the **C0 bytes as assigned**; one supplementary pair (§6, last) scores the
same mutation class against the amendment-8 bytes, because that is the counter a
later reader will actually run.

## 2. Detector semantics used here (stated, so the verdicts can be checked)

The counter is the code under test. The **detector** is a tree that carries one
planted defect which the muted clause is supposed to flag. A run passes the
detector iff the counter's `bad` map contains the defect's key (the `EXPLAIN`
line reads `FAIL`).

* **KILLED** = the mutant's output on the defect tree differs from the pristine
  counter's (the mutated clause is load-bearing; the detector notices the
  mutation). Killed *loudly* if the exit code / `C2_R55_PASS` also flips.
* **SURVIVED** = byte-identical verdict and `bad` map on the defect tree (the
  mutation is unobservable through this detector).

Every mutant is scored twice, as assigned: (a) at C0
(`--rev 9cf0146b94dd…`, the lane itself as `--lane`), (b) on a tree where its
defect exists. The pristine counter is scored on the same trees — a baseline
failure would be inconclusive, and there is none.

## 3. Fixtures (scratch clones; disposable, never in the lane)

Each tree is `git clone --shared` of the lane, `checkout -B <branch> C0`, one
edit, one commit. `git -C "$D" rev-parse --show-toplevel` was asserted equal to
the fixture dir before the commit in each case.

| tree | rev | planted defects | diff |
|---|---|---|---|
| `D_all` | `79329521e068137b7dea9a1cf288eff55b435441` | six, one per arm | `T55W2MutC2-receipts/trees/D_all.diff` |
| `D_rev` | `ae30c3f7c75055d77942ad1285ed5a6304582253` | only the `registry-check --rev` grammar defect | `…/trees/D_rev.diff` |
| `D_rc1` | `c3a2873a9ab48d8540059884756ac045b95502af` | only an exit-class drift (`repeat-control` exits 1 with the grammar intact) | `…/trees/D_rc1.diff` |

`D_all` defects (`…/trees/D_all.diff`, 6 files, 7+/6−):

1. `tools/repeat-control.py` — `could_not_evaluate()` returns `1` instead of
   `EXIT_BY_ID["setup_error"]` (exit-class drift; stderr line still correct).
2. `tools/context-capture.py` — the new `ScratchRootUnusable` handler writes the
   correct stderr line **and** still leaks
   `SELFTEST: FAIL (setup error: RuntimeError: …)` on stdout (a partial fix: one
   inserted line). A pure revert of the `raise` line cannot discriminate this
   clause, because the pre-C0 text fails the grammar match as well as the
   `RuntimeError` clause — that is why the partial fix is the right probe.
3. `tools/pin-disposition.py` — `sys.stderr.write` → `sys.stdout.write` for the
   grammar line (right text, wrong stream).
4. `corpus/knowledge/scratch-root-contract.md` — both occurrences of the label
   `registry-check --rev` renamed to `registry-check rev` (nine modes documented,
   one of them no longer named by its measured label).
5. `tools/registry.json` — the `pin-disposition-selftest` `scratch_root` cell
   says "under **its** scratch root": the marker phrase is gone from one of the
   seven cells.
6. `tools/registry-check.py` — `strict_scratch_root()` raises `RuntimeError`
   again (the `--rev` path then prints a JSON refusal on stdout, rc 2, no
   grammar line).

`D_rc1` defect (`…/trees/D_rc1.diff`), the same edit as `D_all` #1, alone — the
refusal line stays byte-perfect and only the exit class moves:

```
-    return EXIT_BY_ID["setup_error"]
+    return 1
```

## 4. The six mutants (one hunk each; diffs in `…/counters/*.diff`)

| id | edit to the counter | sha256 |
|---|---|---|
| M1 `grammar_accepts_rc1` | `ok = rc == 2 and …` → `ok = rc in (1, 2) and …` | `8729ed6a…c857a` |
| M2 `no_runtimeerror_clause` | drop `and "RuntimeError" not in err + out and "Traceback" not in err + out` | `cfb58635…fe97b` |
| M3 `grammar_stdout_and_stderr` | `for l in err.splitlines()` → `for l in (err + "\n" + out).splitlines()` | `1ec5499c…63e33` |
| M4 `note_counts_labels_always` | `note_names = [m for m in allocating if m[0] in note_txt]` → `note_names = [m[0] for m in allocating]` | `17be2b64…11963` |
| M5 `docs_accepts_any_cell` | `docs = sum(1 for row in cells if MARKER in row["scratch_root"])` → `docs = len(cells)` | `6bf0c550…7107b` |
| M6 `allocating_list_eight` | delete the `registry-check --rev` entry from `modes()` (the docstring's "8 allocating modes") | `f7fcda00…f3cdc` |

Each mutant compiles (`py_compile`) and differs from the pristine copy in exactly
one hunk (see the `.diff` files).

## 5. Runs

Every run is the counter as-is with `--explain` on an empty `--work`:

```
python3 <counter> --lane <lane-or-tree> --rev <rev> --work <empty dir> --explain
```

(`T55W2MutC2-receipts/drive.py` is the wrapper that records wall/cpu/rc; the raw
stdout of every run is in `T55W2MutC2-receipts/runs/<run>.out`, the counter's own
`c2-receipts.json` in `<run>.receipts.json`.)

| run | counter | tree@rev | grammar | lazy | empty | usable | docs | note | skill | total | PASS | rc | `bad` keys |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `P0` | pristine | C0 | 9/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 1 | false | 1 | — |
| `M1C0` | M1 | C0 | 9/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 1 | false | 1 | — |
| `M2C0` | M2 | C0 | 9/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 1 | false | 1 | — |
| `M3C0` | M3 | C0 | 9/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 1 | false | 1 | — |
| `M4C0` | M4 | C0 | 9/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 1 | false | 1 | — |
| `M5C0` | M5 | C0 | 9/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 1 | false | 1 | — |
| `M6C0` | M6 | C0 | 8/8 | 5/5 | 13/13 | 13/13 | 7/7 | 8/8 | 1/1 | **0** | **true** | **0** | — |
| `P_D` | pristine | `D_all` | 5/9 | 5/5 | 13/13 | 13/13 | 6/7 | 8/9 | 1/1 | 7 | false | 1 | repeat-control, context-capture, pin-disposition, registry-check --rev, docs, note |
| `M1D` | M1 | `D_all` | 6/9 | 5/5 | 13/13 | 13/13 | 6/7 | 8/9 | 1/1 | 6 | false | 1 | P_D − repeat-control |
| `M2D` | M2 | `D_all` | 6/9 | 5/5 | 13/13 | 13/13 | 6/7 | 8/9 | 1/1 | 6 | false | 1 | P_D − context-capture |
| `M3D` | M3 | `D_all` | 6/9 | 5/5 | 13/13 | 13/13 | 6/7 | 8/9 | 1/1 | 6 | false | 1 | P_D − pin-disposition |
| `M4D` | M4 | `D_all` | 5/9 | 5/5 | 13/13 | 13/13 | 6/7 | **9/9** | 1/1 | 6 | false | 1 | P_D − note |
| `M5D` | M5 | `D_all` | 5/9 | 5/5 | 13/13 | 13/13 | **7/7** | 8/9 | 1/1 | 6 | false | 1 | P_D − docs |
| `M6D` | M6 | `D_all` | **5/8** | 5/5 | 13/13 | 13/13 | 6/7 | 8/8 | 1/1 | 4 | false | 1 | P_D − registry-check --rev |
| `P_rev` | pristine | `D_rev` | 8/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 2 | false | 1 | registry-check --rev |
| `M6_rev` | M6 | `D_rev` | 8/8 | 5/5 | 13/13 | 13/13 | 7/7 | 8/8 | 1/1 | **0** | **true** | **0** | — |
| `C0_P_rc1` | pristine | `D_rc1` | 8/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 2 | false | 1 | repeat-control --selftest |
| `C0_M1_rc1` | M1 | `D_rc1` | **9/9** | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 1 | false | 1 | — |
| `A_P` | amended pristine | `D_rc1` | 8/9 | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | 1 | false | 1 | repeat-control --selftest |
| `A_M1` | amended M1 | `D_rc1` | **9/9** | 5/5 | 13/13 | 13/13 | 7/7 | 9/9 | 1/1 | **0** | **true** | **0** | — |

The `note` column is the `EXPLAIN` arm's `got/want`, where `want` is
`len(allocating)`; the **verdict line** prints a hardcoded `note=%d/9`, so the
`M6*` rows read `note=8/9` in the raw output while the arm is 8/8 (F3).

Read the table with §2 in mind: for M1–M5 the escape shows up as *one key missing*
from `bad`, so the exit code stays 1 through the remaining keys (the printed
`total` also carries the fixed bias of §1); **M6 is the only mutant whose escape
turns a defect tree into a fully green verdict** (`C2_R55_PASS=true`, exit 0).

Wall/cpu: each full run is one counter invocation (9 grammar modes, 5 lazy, 13
empty + 13 usable + 13 `strace` censuses, 7 registry cells, note, SKILL.md).
Measured wall 2.7–7.2 min per run (3–5 concurrent, load average 60–75 from the
other wave-2 seats), peak RSS ≈ 70 MB for the counter process; 20 runs total.
Cost is dominated by the counter's own `git clone --shared` + checkout of the
14 GB fleet per measured mode: the first run, wrapped in bash `time`, reported
128 CPU-min for the whole subtree (the wrapper's `RUSAGE_CHILDREN` sees the
counter process only, ≈ 4.5 CPU-min).

## 6. Per-mutant verdicts

`P_D` is the shared reference — the pristine C0 counter flags all six planted
defects:

```
EXPLAIN grammar repeat-control --selftest          rc=1  FAIL
EXPLAIN grammar pin-disposition --selftest         rc=2  FAIL
EXPLAIN grammar context-capture --selftest         rc=2  FAIL
EXPLAIN grammar registry-check --rev               rc=2  FAIL
EXPLAIN docs                                      6/7 FAIL
EXPLAIN note                                      8/9 FAIL
C2_R55: rev=79329521e068 grammar=5/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=6/7 note=8/9 skill=1/1 total=7 C2_R55_PASS=false
```

### M1 — accept rc 1 on the grammar arm → **killed** (grammar arm)

*Expected arm:* grammar (the `rc == 2` clause). *Did it:* yes.

```
$ diff -u pristine.py M1_grammar_accepts_rc1.py
-        ok = rc == 2 and any(GRAMMAR.match(l) for l in err.splitlines()) \
+        ok = rc in (1, 2) and any(GRAMMAR.match(l) for l in err.splitlines()) \

$ ... M1_grammar_accepts_rc1.py --lane D_all --rev 79329521e068 ... --explain
EXPLAIN grammar repeat-control --selftest          rc=1  ok      <-- pristine said FAIL
C2_R55: rev=79329521e068 grammar=6/9 ... total=6 C2_R55_PASS=false
```

`bad` = `P_D` minus `repeat-control --selftest`; every other arm keeps its key,
so the escape is exactly the muted clause. C0-tree run `M1C0`: `grammar=9/9`,
`bad` empty — the mutation does not perturb the green tree.

On a tree whose only defect is that drift, the C0 aggregate **masks** the escape
(the counter stays red for the wrong reason):

```
$ ... pristine.py --lane D_rc1 --rev c3a2873a9ab4 ... --explain      # C0_P_rc1
C2_R55: rev=c3a2873a9ab4 grammar=8/9 ... total=2 C2_R55_PASS=false      rc=1
$ ... M1_grammar_accepts_rc1.py --lane D_rc1 --rev c3a2873a9ab4 ...   # C0_M1_rc1
C2_R55: rev=c3a2873a9ab4 grammar=9/9 ... total=1 C2_R55_PASS=false      rc=1
```

all nine arms read `ok`, `bad` is empty, and the process still exits 1 only
because `total` is biased +1 (amendment 8's erratum). The escape is visible only
in the arity (`grammar 9/9` where the tree has a defect) — see §6 supplementary
for what the same mutant does once the bias is removed.

### M2 — drop the `RuntimeError`/`Traceback` clause → **killed** (grammar arm)

*Expected arm:* grammar (the token clause). *Did it:* yes.

```
$ diff -u pristine.py M2_no_runtimeerror_clause.py
-        ok = rc == 2 and any(GRAMMAR.match(l) for l in err.splitlines()) \
-            and "RuntimeError" not in err + out and "Traceback" not in err + out
+        ok = rc == 2 and any(GRAMMAR.match(l) for l in err.splitlines())

$ ... M2_no_runtimeerror_clause.py --lane D_all --rev 79329521e068 ... --explain
EXPLAIN grammar context-capture --selftest         rc=2  ok      <-- pristine said FAIL
C2_R55: rev=79329521e068 grammar=6/9 ... total=6 C2_R55_PASS=false
```

On that tree `context-capture --selftest` prints the frozen line on stderr (so
`GRAMMAR` matches) *and* `SELFTEST: FAIL (setup error: RuntimeError: …)` on
stdout; only the token clause separates the two. C0-tree run `M2C0`: green,
`bad` empty.

### M3 — match the grammar on stdout+stderr → **killed** (grammar arm)

*Expected arm:* grammar (the stream the line is read from). *Did it:* yes.

```
$ diff -u pristine.py M3_grammar_stdout_and_stderr.py
-        ... for l in err.splitlines())
+        ... for l in (err + "\n" + out).splitlines())

$ ... M3_grammar_stdout_and_stderr.py --lane D_all --rev 79329521e068 ... --explain
EXPLAIN grammar pin-disposition --selftest         rc=2  ok      <-- pristine said FAIL
C2_R55: rev=79329521e068 grammar=6/9 ... total=6 C2_R55_PASS=false
```

The planted defect is the *right text on the wrong stream* (`sys.stdout.write`);
the pristine counter reports `grammar rc=2 stderr=[]`. C0-tree run `M3C0`: green.

### M4 — count labels without the note → **killed** (note arm)

*Expected arm:* note. *Did it:* yes.

```
$ diff -u pristine.py M4_note_counts_labels_always.py
-    note_names = [m for m in allocating if m[0] in note_txt]
+    note_names = [m[0] for m in allocating]

$ ... M4_note_counts_labels_always.py --lane D_all --rev 79329521e068 ... --explain
EXPLAIN note                                      9/9 ok      <-- pristine said 8/9 FAIL
C2_R55: rev=79329521e068 grammar=5/9 ... docs=6/7 note=9/9 ... total=6 C2_R55_PASS=false
```

The mutant keeps the `note_txt` read and ignores it: a note that never names one
of the measured modes is accepted. C0-tree run `M4C0`: green.

### M5 — the docs arm accepts any cell → **killed** (docs arm)

*Expected arm:* docs. *Did it:* yes.

```
$ diff -u pristine.py M5_docs_accepts_any_cell.py
-    docs = sum(1 for row in cells if MARKER in row["scratch_root"])
+    docs = len(cells)

$ ... M5_docs_accepts_any_cell.py --lane D_all --rev 79329521e068 ... --explain
EXPLAIN docs                                      7/7 ok      <-- pristine said 6/7 FAIL
C2_R55: rev=79329521e068 grammar=5/9 ... docs=7/7 note=8/9 ... total=6 C2_R55_PASS=false
```

The `len(cells) != 7` guard survives in the mutant, so the mutation is "the cell
exists" rather than "the cell states the contract" — exactly the weaker reading
the tasking named. C0-tree run `M5C0`: green.

### M6 — shrink the allocating list to eight → **killed, and it flips the exit code**

*Expected arm:* grammar, through the **inventory** of measured modes. *Did it:*
yes, and this is the sharpest result of the probe.

```
$ diff -u pristine.py M6_allocating_list_eight.py
-    out.append(("registry-check --rev",
-                ["python3", "tools/registry-check.py", "--rev", "HEAD"], 0, True, False))

$ ... M6_allocating_list_eight.py --lane D_all --rev 79329521e068 ... --explain
EXPLAIN grammar registry-check --rev               (line absent)
C2_R55: rev=79329521e068 grammar=5/8 ... docs=6/7 note=8/9 ... total=4 C2_R55_PASS=false
```

`registry-check --rev` is not measured at all, so its planted defect is invisible;
the grammar denominator silently becomes 8 and the note expectation shrinks with
it (`want = len(allocating)`). On a tree whose **only** defect is that mode the
mutant returns a fully green verdict where the pristine counter fails:

```
$ ... pristine.py  --lane D_rev --rev ae30c3f7c750 ... --explain     # P_rev
C2_R55: rev=ae30c3f7c750 grammar=8/9 ... total=2 C2_R55_PASS=false      rc=1

$ ... M6_allocating_list_eight.py --lane D_rev --rev ae30c3f7c750 ... # M6_rev
C2_R55: rev=ae30c3f7c750 grammar=8/8 ... docs=7/7 note=8/9 ... total=0 C2_R55_PASS=true   rc=0
```

**A tree that does not satisfy C2 is reported green, with exit 0.**

### Supplementary: same mutation class against the amendment-8 bytes

The lane's freeze pointer now names `133b2ce`, whose total line is the only
difference from the C0 bytes. To keep the arithmetic honest, the same M1 edit was
applied to those bytes (`…/counters/amended_M1_accepts_rc1.py`) and scored on a
tree whose only defect is the exit-class drift (`D_rc1`):

```
$ ... amended_pristine.py --lane D_rc1 --rev c3a2873a9ab4 ... --explain      # A_P
EXPLAIN grammar repeat-control --selftest          rc=1  FAIL
C2_R55: rev=c3a2873a9ab4 grammar=8/9 ... total=1 C2_R55_PASS=false      rc=1

$ ... amended_M1_accepts_rc1.py --lane D_rc1 --rev c3a2873a9ab4 ... --explain # A_M1
EXPLAIN grammar repeat-control --selftest          rc=1  ok
C2_R55: rev=c3a2873a9ab4 grammar=9/9 ... total=0 C2_R55_PASS=true       rc=0
```

Under the counter the freeze now points at, every escape of the class probed here
is a **false green with exit 0**, not merely a missing `bad` key. (Measured for
M1; the same substitution is mechanical for M2–M5 because each removes its own
key while `bad` becomes empty, which is the condition for `total == 0`.)

## 7. Findings

**F1 (coverage, sharpest). Nothing pins the allocating-mode inventory to nine.**
`note`'s expectation is `len(allocating)` — computed from the very list under
test — and `docs` counts registry cells, not modes; the prose "Nine allocating
modes" in `corpus/knowledge/scratch-root-contract.md` is not enforced by any arm.
Measured: `M6C0` (the ninth mode deleted) is clean — `grammar=8/8`, `bad` empty,
`PASS=true` at C0; `M6_rev` returns green on a defective tree. A documented
allocating mode can leave the table and the counter still reports a pass.
Amendment 8 does not address this (it changed the denominators to
`len(allocating)` as well), so the gap survives at the freeze pointer.

**F2 (consequence of F1). The only class that flips the exit code.** With the C0
aggregate bias an escaped arm on a single-defect tree still leaves `total`
non-zero, so the process stays red even when every arm reads `ok` — measured,
`C0_M1_rc1`: `grammar=9/9`, `bad` empty, `total=1`, exit 1. M6 removes the bias (`(8 - note)` becomes 0) and is
the only mutant that returns exit 0 on a defective tree (`M6_rev`). Under the
amendment-8 bytes the bias is gone, so *every* escape flips to a green verdict
(§6 supplementary: `A_M1` `total=0 PASS=true rc=0`).

**F3 (measured defect in the verdict line). `note=%d/9` is a literal.** The
verdict printer hardcodes the `/9` (and `/7`, `/1`) denominators while the code
compares against `len(allocating)`. Measured with `M6C0`:
`… note=8/9 skill=1/1 total=0 C2_R55_PASS=true` — a line that reads like a failed
note arm next to a pass. A reader of the receipt cannot distinguish "8 of 9 modes
named" from "8 of 8". (Same line at C0 with the pristine counter, where the
literal happens to be right.)

**F4 (baseline, already in the record). The C0 aggregate reads `total=1` with an
empty `bad` map on a green tree** — reproduced independently here (`P0`,
`M1C0`…`M5C0`: `grammar=9/9 … total=1 C2_R55_PASS=false`, exit 1). Amendment 8
documents and fixes it; quoted only because it is the frame for F2 and because
five of my six C0-tree scores inherit it.

**F5 (positive result, no action).** The six clauses attacked are all
load-bearing against a plausible single-defect tree, and each mutant escaped
*exactly* its own key and no other (M1D/M2D/M3D/M4D/M5D/M6D in §5). The arms are
not decorative and the note/docs arms are not satisfied by the same mechanism:
the note arm needs the *label text in the note*, the docs arm needs the *marker
in each of seven registry cells*, and the grammar arm needs *the right text on
the right stream at the right exit code with no exception token*.

## 8. Restoration evidence

* The lane was only ever *read* (`git show`, `git diff`, `git log`, and the
  counter's own `git clone --shared` from it). No editor, no `git` write command,
  no checkout ran in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
  `git diff --stat 9cf0146 -- <the seven target paths>` currently shows peer
  wave-2 edits (`measure.py` = amendment 8's bytes, plus sibling seats' work);
  none of them is mine, and the counter bytes at C0 still hash
  `36ca47d3…` (`git show 9cf0146:.ufo/evidence/round-55/c2/measure.py | sha256sum`).
* The three defect trees live only under `/fast/scratch/hyaku/tameshi-r55/
  T55W2MutC2/trees/` (disposable scratch, removed at the end of this seat); their
  revs and diffs are preserved under `…-receipts/trees/`.
* The six mutants are copies under `…-receipts/counters/`, not lane files.
* Census (read-only): `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → `tameshi ok`, exit 0.

## 9. Artifacts opened

* `.ufo/evidence/round-55/c2/measure.py` at `9cf0146` (read in full, 292 lines)
  and at `133b2ce` (diffed against the C0 bytes; only the total line differs).
* `.ufo/evidence/round-55/before/c2.stdout` (base receipt at `0a2010ac`:
  `grammar 6/9 … total=21`).
* `tools/repeat-control.py`, `tools/context-capture.py`,
  `tools/registry-check.py`, `tools/pin-disposition.py`, `tools/env-diff.py`,
  `tools/registry.json`, `corpus/knowledge/scratch-root-contract.md`,
  `SKILL.md` — all at `9cf0146` (the tools via `git show`; the registry and the
  note also through the counter's own clone).
* `git log --oneline` of the lane (C0, freeze, amendment 8).

## 10. Receipt index (`T55W2MutC2-receipts/`)

```
counters/pristine.py                       byte-identical copy of the C0 counter + .sha256
counters/M1..M6*.py, *.diff                the six mutants and their one-hunk diffs
counters/amended_pristine.py               counter at 133b2ce (sha 0458f632…)
counters/amended_M1_accepts_rc1.py, .diff  M1 applied to the amendment-8 bytes
trees/D_all.diff  trees/D_all.rev          79329521e068… six-arm defect tree
trees/D_rev.diff  trees/D_rev.rev          ae30c3f7c750… rev-only defect tree
trees/D_rc1.diff  trees/D_rc1.rev          c3a2873a9ab4… exit-class-only defect tree
drive.py                                   the runner used for every row of §5
runs/<run>.out                             full --explain stdout of every run
runs/<run>.receipts.json                   the counter's own c2-receipts.json
```

Reproduce any row with:

```
python3 T55W2MutC2-receipts/drive.py <run-name> \
    T55W2MutC2-receipts/counters/<counter>.py <lane-or-tree> <rev>
```
