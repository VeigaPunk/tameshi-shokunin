# T56W1SentTamper — the gate as an adversary (round 56, wave 1)

Seat: sentinel. Judged on: operability. Milestone: receipt forgery attempts.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`, freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf`.
Target: `tools/receipt-revision-gate.py`, sha256 `1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2`, identical to `freeze.json`'s entry, selftest `14/14 pass` (`T56W1SentTamper-receipts/r01-gate-identity.txt`). **I did not edit the gate or any frozen instrument.**

All receipts cited below are in `T56W1SentTamper-receipts/`. Machine-readable form: `T56W1SentTamper.json`.

---

## Axes

1. **operability** — does the gate's `PASS` mean what the deciding run treats it as meaning at gate 0b and gate 0c?
2. **falsifiability** — does C2 arm 2 (the gate's refusal of the real round-54 receipt) survive an adversary who controls the inputs the gate reads: the receipt body, its sidecar, and the `--paths` file?
3. **residual honesty** — does the claim text this round writes overstate what the gate can prove?

Every move below was kept only if it improved an axis and harmed none: the fixture and the real-receipt runs are read-only against the lane, and the one patch is demonstrated in a scratch clone, not applied.

## Method

One adversary, three inputs:

- **Fixture** `/fast/scratch/hyaku/tameshi-r56/T56W1SentTamper/fix` — `git init`, toplevel asserted before every commit (`git -C "$D" rev-parse --show-toplevel` == `$D`). Commits: `c0`, `c1` (certified; `other.txt` differs from `c0`), `c2` (`surface.txt` differs from `c1`), a `side` branch, a **merge commit whose tree equals `c1`'s tree and whose parents are `c0` and `side`**, a **lightweight tag named `deadbeef`** (hex-shaped), an annotated tag `cafebabe`, an orphan commit with `c1`'s tree.
- **Real receipts** — copies of `.ufo/evidence/round-54/control/controls-b.stdout`, its `CTL_POS_c1` slice, `.ufo/evidence/round-55/after/c2.stdout`, gated with `--lane <lane>` (read-only: the gate reads git objects and the named files only).
- **Invocation shapes** are the lane's own, not invented: gate 0b (`deciding-run.sh:66-74`), gate 0c (`:100-107`), and arm 5 of `c2/measure.py` (`:202-220`).

---

## The seven attacks

| # | attack | gate's answer | safe for the lane's use? | severity |
|---|---|---|---|---|
| A1 | copy the certified `rev=` token into a receipt for a different claim | **PASS** | no | high |
| A2 | forge the `.sha256` sidecar over a tampered receipt | **PASS** (stale sidecar: `RECEIPT_DIGEST_MISMATCH`) | no | medium |
| A3 | `rev=<certified>` in a path or prose, no verdict line | **PASS**; `RECEIPT_REQUIRED_LINE_MISSING` only with a caller regex | no by default | medium |
| A4 | JSON `"rev"` plus a second `rev=` in a comment | same value: **PASS**; differing: `RECEIPT_REV_AMBIGUOUS` | yes | none |
| A5 | name a tag or a tree instead of a commit | tree/blob: `RECEIPT_REV_UNRESOLVABLE`; annotated or hex-named tag: **PASS** | yes (latent) | low |
| A6 | merge commit with the certified tree, different history | with `--paths`: **PASS**; without: `RECEIPT_REV_MISMATCH` | no (content ≠ commit) | medium |
| A7 | `--paths` listing paths that do not exist | **PASS** | no — gate defect | high |

### A1 — the token travels, the claim does not

```
$ cat fix/receipts/a1.txt
CTL CTL_POS_c1 C1_X: rev=e5d1da46de6e… credited=0 lost=64 total=64 C1_X_PASS=false
GATE OK …/a1.txt role=positive revs=e5d1da46de6e…
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
```

On the real round-54 receipt, one substitution:

```
$ sed 's/rev=077d431e6996/rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c/' r54-slice.stdout
CTL CTL_POS_c1 C1_R54: rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c c0=99c3bc88d704 credited=60 lost=4 … C1_R54_PASS=false
GATE OK … role=positive revs=c21081008adbb…
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
```

C2 arm 2's `RECEIPT_REV_CONTENT_DRIFT` refusal becomes `PASS` while the line still says `C1_R54_PASS=false credited=60 lost=4`. **Exploit path:** any receipt passes `role=positive|verdict` if its only token is the certified one; the gate never reads the claim. **Impact:** the lane can cite gate PASS for a control whose own line says it failed — the R55.5 shape with the token made to match. **Smallest remediation (caller):** require a line that carries the value (`:verdict:C2_R56_PASS=true`, not `C2_R56_PASS=`), and cite the control's own `CTL_MATCH`/`CONTROLS_x` line in the report. Receipt: `r03-a1-copied-token.txt`.

### A2 — the sidecar is a checksum, not a signature

```
stale sidecar (64 zeros):  RECEIPT_DIGEST_MISMATCH sidecar=000000000000 got=b4ead2ffea49   exit 3
sidecar recomputed:        GATE OK … codes=none verdict=PASS                                exit 0
no sidecar at all:         GATE OK … codes=none verdict=PASS                                exit 0
```

Real round-54 slice falsified (`credited 60→64`, `lost 4→0`, `C1_R54_PASS false→true`): **PASS** with a recomputed sidecar; `RECEIPT_DIGEST_MISMATCH` with the repo's committed sidecar. **Impact:** body integrity is self-asserted, and — see L3 — the sidecar is absent at every path the round actually gates, so the code never fires on a real receipt. **Smallest remediation:** say in QUALITY/knowledge that the sidecar detects accidental edits only; for tamper evidence gate the committed blob (`git cat-file` at REV), not a working-tree file. Receipt: `r04-a2-sidecar.txt`.

### A3 — a sentence is a receipt

```
Reviewed the lane at rev=e5d1da46de6e…; nothing was measured.        -> PASS
same bytes with :positive:C1_X_PASS=                                 -> RECEIPT_REQUIRED_LINE_MISSING
artifact: out/rev=e5d1da46de6e…/report.txt written                   -> PASS
```

`REV_RE` (line 43) has no notion of a verdict line. **Impact:** gate 0b gates `controls-b` with no regex (`deciding-run.sh:69`), so a controls-b that merely mentions the token passes. **Smallest remediation (caller):** a regex on every positive/verdict receipt, with the value. Receipt: `r05-a3-prose-token.txt`.

### A4 — the ambiguity guard works

Same token twice (`{"rev": …}` and `# rev=…`): **PASS**, and the forger gains nothing (one distinct token, still the certified one). Differing values: `RECEIPT_REV_AMBIGUOUS`, exit 3. No action. Receipt: `r06-a4-json-rev.txt`.

### A5 — a tree cannot pass, a tag can, and a hex-named tag is mutable

```
rev=<tree of c1>        RECEIPT_REV_UNRESOLVABLE
rev=<blob of c1>        RECEIPT_REV_UNRESOLVABLE
rev=cafebabe (annotated tag at c1)   PASS
rev=deadbeef (tag at c0), certified=c0            PASS
git tag -f deadbeef <c2>; same receipt bytes, certified=c0   RECEIPT_REV_MISMATCH
same bytes, certified=c2, --paths                    PASS
```

`resolve()` appends `^{commit}`, so trees and blobs are refused — correct. But a ref whose *name* matches `[0-9a-f]{7,40}` resolves through the ref: the token is a name, not a commit, and identical receipt bytes change verdict when the tag moves. **Impact: latent only** — `git tag` in the lane returns `count=0`, so there is no hex-shaped ref to alias, and the counters print the resolved sha. **Smallest remediation:** policy line — receipts name the 40-hex commit; the report states that `rev=` is resolved through refs. Receipt: `r07-a5-tag-tree.txt`.

### A6 — content identity is not commit identity, and the surface is narrower than the claim

```
merge commit <M>, tree == tree(c1), parents c0+side
  with --paths (surface, other, deep/x):  PASS
  without --paths:                        RECEIPT_REV_MISMATCH
c2 differs from c1 on surface.txt only:
  --paths {other.txt}:                    PASS
  --paths {surface,other,deep/x}:         RECEIPT_REV_CONTENT_DRIFT drift=surface.txt
```

The positive/verdict rule is "same bytes on the declared paths", not "this commit". On the real lane, with the round's own `frozen-surface.paths`:

```
rev=6efd2a19 vs base 981c5e8b: frozen-surface drift=0, total drift=9    -> PASS
rev=fa48c06c vs base 981c5e8b: frozen-surface drift=0, total drift=244  -> PASS
```

**Impact:** the claim the gate supports is "same bytes on these nine paths". The list omits `SCORECARD.md`, `LOG.md`, `corpus/lessons/**`, `.ufo/waves/round-56/**`, `.ufo/evidence/round-56/control/**` — verified: `grep -cxF` returns 0 for each. (T56W1CritC2 found the same omission independently and sharper: a certified revision with a gutted contract and a stubbed `controls.sh` passes gate 0b.) **Smallest remediation:** state the claim as content identity on a named list, and grow the list in a future round to include the claim's products. Receipt: `r08-a6-merge-and-surface.txt`.

### A7 — the path list is a pathspec, and the gate never validates it

```
ghost list (does/not/exist.txt, deep/also-missing.txt), c0 vs certified c1 (real drift on other.txt):
GATE OK … codes=none verdict=PASS
real paths + ":(exclude)other.txt":        PASS   (the drifted path is excluded)
real paths + ":(exclude)*":                PASS   (everything is excluded)
the honest list, same receipt:             RECEIPT_REV_CONTENT_DRIFT drift=other.txt
ghost path beside a real path:             RECEIPT_REV_CONTENT_DRIFT drift=other.txt
empty (comment-only) list:                 RECEIPT_REV_CONTENT_DRIFT "<no --paths given…>"
```

On the real round-54 receipt with the real surface plus one appended line:

```
.ufo/evidence/round-54/c1/measure.py … corpus/SOURCES.md
:(exclude).ufo/evidence/round-21/coldread/ledger.json
GATE OK … role=positive revs=077d431e6996
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
```

where C2 arm 2 requires `RECEIPT_REV_CONTENT_DRIFT`. **This is the one finding I call a defect rather than a residual:** `git diff --name-only A B -- <path>` prints nothing when the path exists at neither revision, and a `:(exclude)…` entry is a pathspec, so `drifted_paths` (lines 73-78) reports "no drift" for a comparison it never made. **Impact:** the gate's content-identity arm is vacuous for any caller who does not hand-write the list; this round is protected only because `frozen-surface.paths` is frozen and `FROZEN_UNCHANGED` (`deciding-run.sh:79-80`) would fail the run — not because the gate checked anything. **Smallest remediation:** the patch below. Receipt: `r09-a7-paths.txt`.

---

## Sweep beyond the seven (an attack that finds nothing shows its sweep)

`r10-sweep.txt`, all on the fixture unless noted:

| probe | answer | safe |
|---|---|---|
| sidecar path is a directory | uncaught `IsADirectoryError`, exit 1, no verdict line | fail-closed, outside the code vocabulary |
| receipt path is a directory | uncaught `IsADirectoryError`, exit 1 | same |
| `--paths` file missing | uncaught `FileNotFoundError`, exit 1 | same; a missing list does not read as empty |
| binary receipt, NUL bytes, token present | **PASS** | no — same class as A3 |
| uppercase hex token | `RECEIPT_REV_ABSENT` | false refusal, never a false pass |
| 41 hex chars after `rev=` | `RECEIPT_REV_ABSENT` | `\b` rejects rather than truncating |
| `role=control` naming the pre-work ancestor | **PASS** | by design; it is why a *positive* control gated as `control` still passes at the freeze — the round-54 class is expressible if the role is chosen wrongly |
| orphan commit with the certified tree, on no ref | **PASS** with `--paths` | no — content identity, no reachability requirement |
| symlinked receipt | **PASS** | no — the gate reads through symlinks |
| receipt path containing a colon | `RECEIPT_MISSING` on a truncated path | fail-closed, misreported (`spec.split(':', 2)`) |
| sidecar with trailing garbage | **PASS** | first token compared |
| `--certified` given as a hex-named tag | **PASS** (resolved at check time) | the certified side is as mutable as the receipt side |

---

## The lane's use: what gate 0b and gate 0c actually certify

### L1 (high) — gate 0b passes a control set in which every control failed

`deciding-run.sh:56-57` accept any `^CONTROLS_A: [0-9]*/[0-9]* as pre-registered` line, so `0/2` matches; `:66-74` then gate `controls-a` as `control` and `controls-b` as `positive`, with no required regex. Reproduced with the round's real `frozen-surface.paths`:

```
CTL CTL_POS_c1 … C1_R56_PASS=false
CTL_MISMATCH CTL_POS_c1 expected=true actual=false
CTL CTL_POS_c2 … C2_R56_PASS=false
CTL_MISMATCH CTL_POS_c2 expected=true actual=false
CONTROLS_B: 0/2 as pre-registered
GATE OK … role=control   GATE OK … role=positive
GATE: receipts=2 ok=2 refused=0 codes=none verdict=PASS   exit 0
```

**Impact:** the deciding run's control gate certifies that the receipts name a revision, not that any control reached its pre-registered verdict; the round-54 `CTL_MISMATCH … actual=false` class survives gate 0. **Smallest remediation (caller):** assert numerator == denominator (`grep -qE '^CONTROLS_B: ([0-9]+)/\1 as pre-registered'`) and refuse any `^CTL_MISMATCH` line in `controls-b`. Receipt: `r11-lane-use-gate0b-0c.txt`.

### L2 (medium) — gate 0c's required line accepts a false verdict

`:102-103` pass `:verdict:C1_R56_PASS=` / `:verdict:C2_R56_PASS=` with no value:

```
C2_R56: rev=c3e2ca9f0207 total=9 C2_R56_PASS=false   ->  GATE OK … verdict=PASS   exit 0
```

The run is saved only by the separate `grep -q "${k^^}_R56_PASS=true"` at `:98`. **Smallest remediation:** pass `…_PASS=true` in the gate spec so the gate's own refusal covers the value.

### L3 (medium) — `RECEIPT_DIGEST_MISMATCH` cannot fire on any receipt the round certifies

`c2/measure.py` copies each receipt into `--work` (`:147,:149,:171,:190,:212-214`) without its `.sha256` sibling; `.ufo/evidence/round-56/control/` contains only `frozen-surface.paths`, so the round's own `controls-a`/`controls-b` have no sidecar at all. The digest arm exists only in the selftest. **Smallest remediation:** copy the sidecar with the receipt, or gate the committed blob.

### L4 (low) — gate 0b reads the list from the working tree before the clean-tree assertion

`:68` passes `"$LANE/$E/control/frozen-surface.paths"` (working-tree bytes); the clean-tree check is at `:76` and `FROZEN_UNCHANGED` at `:80`, both after the gate's verdict. A dirty list aborts the run at `:77` with exit 3, so the ordering is contained — but the gate's verdict is computed against bytes no assertion has yet covered, which is why A7 matters. **Smallest remediation:** feed the gate the bytes at REV, as `c2/measure.py` already does.

### L5 (medium) — the R55.1 class returns with one appended line

The committed round-55 C2 receipt is refused `RECEIPT_REV_ABSENT`; appending `rev=4c04c1d33377e5b6a3636199c5fdda197fc670d5` to the same truncated file makes it **PASS** as `role=verdict`. The refusal is a statement about a token that is one line away from existing; the report must not present it as a property of the file.

### L6 (high) — cross-check of T56W1CritC2's kill-shot: C2 cannot pass this round

Independently measured at the freeze (`r17-c2-arm6-index.txt`):

```
SOURCES.md header: | id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
rows=140  mined_at_index7=113  mined_at_index8=0
c2/measure.py:245:  … and cells[8] == 'mined'
```

`mined` lives in column 7; the counter reads column 8 (the `opened` date), so the note cell can never score, `docs ≤ 3/4`, `total ≥ 1`, and `C2_R56_PASS=true` is unreachable whatever wave 2 writes. I confirm T56W1CritC2's finding from my own bytes. The instrument is frozen: this is the L1's call (amendment or round 57), and the round must not report C2 as pending content work.

---

## The residual risk the gate cannot remove

> The gate binds a **revision token**, not a claim, and not a provenance. It can prove that a receipt file mentions exactly one revision token, that the token resolves to a commit, and that the commit is the certified revision or is content-identical to it on a declared path list. It cannot prove that the receipt was written by the run it describes, that its numbers are the ones the run printed, that its body was not edited afterwards, that its sidecar was written by anyone but the forger, that the path list is honest or complete, or that a control receipt's own verdict is `PASS`.

What it *does* remove, verified here: a receipt naming no revision (`RECEIPT_REV_ABSENT`), naming a revision absent from the repo (`RECEIPT_REV_UNRESOLVABLE`, round-54's `7df0e0426c98`: `fatal: Not a valid object name`), naming two revisions (`RECEIPT_REV_AMBIGUOUS`), and naming a revision whose declared surface differs (`RECEIPT_REV_CONTENT_DRIFT`). Those four round-54/55 classes are now loud, and the three real red-before receipts are refused with their named codes.

What it cannot remove is the seven acceptances above — of which A7 is a defect to fix and the other six are inherent to a token gate.

**How the round's report must say it** (the wording matters more than the finding):

1. State C2 as: *every receipt the lane certifies carries the revision token of the revision it was measured against, and the gate refuses the three real receipts the lane accepted in rounds 54 and 55.* Do not write "receipts are bound to their revision" without the token qualifier.
2. State the negative: *the gate accepts a receipt that names the certified revision whatever it asserts; acceptance is evidence about the token, never about the claim.*
3. Never cite the gate's `verdict=PASS` as evidence that a control passed — cite the control's own `CTL_MATCH` / `CONTROLS_x: N/N` line.
4. Never cite the `.sha256` sidecar as tamper evidence; it is an accidental-edit checksum and it is absent at every path the round gates.
5. Record that the content-identity arm is only as strong as `frozen-surface.paths`, and name what the list omits.
6. Record A7 and L1 as defects routed to a fix (round 57 or amendment), not as residuals the wave accepts.

---

## Proposed patch (not applied — the gate is frozen this round)

`tools/receipt-revision-gate.py` is in `freeze.json` and `contract.frozen_paths`, and `deciding-run.sh:79-80` refuses a run whose frozen bytes differ between FREEZE and REV. Demonstrated in a scratch clone at the freeze (`toplevel` asserted, `head=c3e2ca9f0207`), diff exported to `$S/patch/pathspec-integrity.diff`:

```diff
diff --git i/tools/receipt-revision-gate.py w/tools/receipt-revision-gate.py
index c93c135..3b72112 100755
--- i/tools/receipt-revision-gate.py
+++ w/tools/receipt-revision-gate.py
@@ -74,6 +74,17 @@ def drifted_paths(lane, rev_a, rev_b, paths):
     """Return the listed paths whose bytes differ between two revisions."""
     if not paths:
         return ['<no --paths given: content identity is not checkable>']
+    # A pathspec is a pattern language, not a path list: one `:(exclude)…` line
+    # silently empties the comparison, and a path that exists at neither revision
+    # compares equal. Neither outcome is content identity; both are refusals.
+    for p in paths:
+        if p.startswith(':'):
+            return ['<pathspec-magic %s: content identity is not checkable>' % p]
+    absent = [p for p in paths
+              if any(git(['-C', lane, 'cat-file', '-e', '%s:%s' % (r, p)]).returncode != 0
+                     for r in (rev_a, rev_b))]
+    if absent:
+        return ['<absent %s: content identity is not checkable>' % absent[0]]
     r = git(['-C', lane, 'diff', '--name-only', rev_a, rev_b, '--'] + list(paths))
     return [p for p in r.stdout.decode().splitlines() if p]
 
@@ -193,7 +204,8 @@ def run(argv):
         codes, detail, revs = check(lane, full, path_list, receipt, receipt[1], receipt[2])
         all_codes.extend(codes)
         rows.append({'receipt': receipt[0], 'role': receipt[1], 'revs': revs,
-                     'ok': not codes, 'codes': sorted(set(codes)), 'detail': detail})
+                     'ok': not codes, 'codes': sorted(set(codes)), 'detail': detail,
+                     'paths': None if path_list is None else len(path_list)})
     refused = [r for r in rows if not r['ok']]
     verdict = 'PASS' if not refused else 'REFUSED'
     if as_json:
@@ -201,8 +213,9 @@ def run(argv):
                           'paths': path_list, 'receipts': rows, 'verdict': verdict}, indent=1))
     else:
         for r in rows:
-            print('GATE %s %s role=%s revs=%s%s'
+            print('GATE %s %s role=%s paths=%s revs=%s%s'
                   % ('OK' if r['ok'] else 'REFUSED', r['receipt'], r['role'],
+                     'none' if r['paths'] is None else r['paths'],
                      ','.join(r['revs'] or []) or 'none',
                      (' code=%s %s' % (','.join(r['codes']), r['detail'])) if r['codes'] else ''))
         print('GATE: receipts=%d ok=%d refused=%d codes=%s verdict=%s'
```

Verbatim copy: `T56W1SentTamper-receipts/r15-patch.diff` (sha256 `966b1a956ebd…`, 43 lines; `git diff --stat` → `15 insertions(+), 2 deletions(-)`, `r15-patch.txt`).

Kept the code vocabulary closed (no new code: a non-checkable list is already `RECEIPT_REV_CONTENT_DRIFT`) so the selftest's `codes-closed` case stays true. Demonstrated (`r14-patched-gate.txt`):

```
GATE_SELFTEST: 14/14 pass
ghost paths                 -> REFUSED RECEIPT_REV_CONTENT_DRIFT drift=<absent does/not/exist.txt: …>
pathspec magic              -> REFUSED RECEIPT_REV_CONTENT_DRIFT drift=<pathspec-magic :(exclude)…: …>
real arm 2                  -> REFUSED RECEIPT_REV_CONTENT_DRIFT (unchanged)
real arm 3                  -> REFUSED RECEIPT_REV_UNRESOLVABLE (unchanged)
real arm 4                  -> REFUSED RECEIPT_REV_ABSENT (unchanged)
legitimate positive at PIN  -> PASS, paths=9
copied token / forged sidecar / failing control set -> still PASS (not fixed by this patch)
```

**Does not fix:** A1, A2, A3, A5, A6, L1, L2, L5. Those are caller discipline or inherent.

---

## What I did not test

- A receipt on a FIFO or blocking special file (the gate would block in `read_bytes`; no timeout is reachable).
- A receipt larger than memory (the gate reads the whole body).
- The TOCTOU window after the gate's PASS: the gate re-reads nothing, so an edit after its verdict is invisible to it — and the deciding run's later steps do not re-gate the same file.
- Whether a counter's printed `rev=` is the revision its work used: `c1/c2 measure.py` read only git objects at the rev they are given, so the token derives from the argument, not from a measurement; a caller passing the wrong `--rev` gets a consistent lie. This is the deepest residual and no gate can see it.

## Tooling and hygiene

- **Installed/upgraded: none.** Host `python3 3.14.8`, `git 2.56.0` were sufficient; no pacman transaction (host-wide pause respected), no `~/.local/bin` write.
- Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W1SentTamper` (fixture, receipts, clone, patch). No mutating git command touched the lane: the only commits were in the fixture and the scratch clone, each after asserting `rev-parse --show-toplevel` equals the fixture path.
- Lane writes: this report, `T56W1SentTamper.json`, and `T56W1SentTamper-receipts/` (15 files). No lane production file and no frozen instrument was modified.
- Census at round end: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → `exit=0`, 140 rows (`r16-census-and-tree.txt`).
