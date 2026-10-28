# T55W1CritGate — attack on the round-55 deciding-run gate

Seat: T55W1CritGate (critic, leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Target: `.ufo/evidence/round-55/deciding-run.sh`, sha256
`af11d7551d8af1c75ba647704cbf72911d591c9ab28df060b669fd2549c34e2b` — byte-identical to the freeze
manifest entry `deciding-run.sh`, and **not edited** by this seat. Every fixture below runs that exact
file. No tracked lane file was modified and no mutating git command ran in the lane; the only lane
writes by this seat are its own three deliverables under `.ufo/waves/round-55/w1/`.

All work is a `git clone --shared` of the lane detached at the freeze
`631cd6455e58dce969310b4c0466c3383d9f5108`, with one or more commits added **inside the clone**, under
`/fast/scratch/hyaku/tameshi-r55/T55W1CritGate/` (`fx*` dirs). Each fixture asserts
`git -C <clone> rev-parse --show-toplevel == <clone>` before committing. The driver
(`drv.sh`, copied to `T55W1CritGate-receipts/drv.sh`) only builds fixtures and invokes the frozen script.

Reproduction shape:

```
d=<fixture>; HYAKU_SCRATCH=$S/hs-<tag> bash .ufo/evidence/round-55/deciding-run.sh \
  "$d" <REV> <FREEZE> "$d/.ufo/evidence/round-55/deciding"
```

`HYAKU_SCRATCH` is set per run so the script's `rm -rf "$SCR"` can only touch my own scratch. A run's
`rc=124` in a receipt is **my** `timeout`, not the script's exit; the marker that every refusal was
cleared is `$OUT/frozen.stdout`, which the script writes only after the last refusal
(dirty-tree, line 58) — and no `DECIDING_REFUSED` line in the output.

## Verdict matrix

| # | Refusal path (line) | Verdict | Fixture | Receipt |
|---|---|---|---|---|
| R1 | `LANE must be absolute` (12, exit 2) | **holds** | `b1` | `b1-lane-relative.out` |
| R2 | `cd "$LANE"` (17, exit 2) | holds by inspection (not separately fixtured; same `|| exit 2` shape) | — | — |
| R3 | `REV` unresolvable (18, exit 2) | **holds** | `b2` | `b2-rev-unresolvable.out` |
| R4 | `FREEZE` unresolvable (19, exit 2) | **holds** | `b3` | `b3-freeze-unresolvable.out` |
| R5 | `freeze-integrity` — a manifest-declared file altered (20–43) | **holds** for declared keys | `a1` | `a1-frozen-covered-tamper.out` |
| R6 | `freeze-integrity` — manifest key set | **DEFEATED** → F2 | `a2` | `a2-manifest-keydrop.out` |
| R7 | freeze authority (`FREEZE` argument itself) | **DEFEATED** → F1 | `a5`, `b9` | `a5-selfcert-freeze-eq-rev.out`, `b9-zero-of-zero-receipt.out` |
| R8 | `outdir-missing` (44, exit 3) | **holds** (absent path, and a plain file) | `c1`, `c1b` | `c1-outdir-missing.out`, `c1b-outdir-is-file.out` |
| R9 | `head-is-not-rev` (45, exit 3) | **holds** | `b5` | `b5-head-not-rev.out` |
| R10 | `control-receipt-missing` (48) | **holds** | `a0` | `a0-control-missing.out` |
| R11 | `control-receipt-not-a-blob` (49) | **holds** for trees | `b6` | `b6-receipt-is-tree.out` |
| R12 | `control-receipt-empty` (50) | **holds** for 0 bytes | `a3` | `a3-receipt-empty.out` |
| R13 | receipt content really is the receipt | **DEFEATED** → F3 | `a4`, `a6`, `a10b` | `a4-receipt-onebyte.out`, `a6-symlink-receipts.out`, `a10b-dirty-receipt-assume-unchanged.out` |
| R14 | `control-receipt-not-after-freeze` (52) | **holds** (content genuinely authored pre-freeze) | `a7` | `a7-receipt-before-freeze.out` |
| R15 | receipt exit side / control counts | **DEFEATED** → F4 (no such check exists) | `b8`, `b9` | `b8-controls-exit-ignored.out`, `b9-zero-of-zero-receipt.out` |
| R16 | `second-invocation` (56) | **holds** for a regular marker; **DEFEATED** for a dangling symlink → F6 | `a9`, `a12` | `a9-second-invocation.out`, `a12-second-invocation-dangling-symlink.out` |
| R17 | `dirty-tree` (57–58) | **holds** for ordinary dirt (untracked outside OUTDIR, plain modification); **DEFEATED** by an index flag → F5 | `a8`, `a10a`, `a10b` | `a8-dirty-untracked-outside-outdir.out`, `a10a-dirty-receipt-NO-FLAG.out`, `a10b-…out` |
| R18 | OUTDIR exclusion scope (58) | **DEFEATED** — unanchored prefix → F5b | `a11` | `a11-outdir-prefix-exclusion.out` |
| R19 | `FROZEN_UNCHANGED=0` (66) | prints and continues (no refusal) → F7 | `b7`, `b7b` | `b7-frozen-drift-nonfatal.out`, `b7b-frozen-drift-to-end.out` |

Answers to the specific probes in the item:

- **"a control receipt committed before the freeze (ancestry check)"** — the check works on the
  *path's latest touching commit*: `a7` (receipts in commit X, freeze cut at Y=X+empty commit, REV=X)
  is refused `DECIDING_REFUSED control-receipt-not-after-freeze`. It is defeated in the *other*
  direction: the freeze may be cut *after* the receipts exist (`a5`: `FREEZE == REV`), and it checks
  provenance of the path, not of the bytes (any later touch, even `chmod`, re-dates the receipt).
- **"an empty file that is still a blob"** — refused at 0 bytes (`a3`, `control-receipt-empty`).
  A 1-byte blob passes the size arm and only dies at the working-tree grep (`a4`,
  `controls-a-verdict-missing`) — i.e. the emptiness arm is about the blob, the content arm is about a
  *different file*; `a10b` shows the second file can carry the verdict while the blob stays 1 byte.
- **"a dirty file that matches the outdir exclusion"** — no need for a dirty *file*: an untracked
  directory whose name has OUTDIR as a prefix is excused (`a11`), and any *tracked* file can be dirtied
  invisibly with `update-index --assume-unchanged` (`a10b`).
- **"a `frozen.stdout` that prints MISMATCH but exits 0"** — not reachable as written: the
  freeze-integrity printer exits 1 and is wired to `|| { …exit 3; }` (`a1`); the only other writer is
  line 66, which prints `FROZEN_UNCHANGED=0` and sets `rc=1`. What *is* reachable is the opposite
  hazard: the drift is detected and then ignored for the rest of the run (F7).

## Findings

### F1 (critical) — `FREEZE` is an unauthenticated argument; `FREEZE == REV` is accepted

The gate re-derives the manifest *from the commit the caller names as the freeze*. Nothing ties that
argument to the round's freeze (`BASE` is hardcoded at line 14; the freeze sha is not), and
`git merge-base --is-ancestor FREEZE c` is true when `c == FREEZE`, so a single commit authoring the
manifest, the counters **and** the "pre-registered" receipts satisfies every check at once.

Fixture `fxSelf` — one commit at the freeze adding four control receipts with verdict lines, run with
`FREEZE = REV = 4ef4ad78bd9b52829cc679d1366a0c3fd3568b45`:

```
FREEZE_INTEGRITY: OK files=6 amendments=0
FROZEN_UNCHANGED=1 freeze=4ef4ad78… rev=4ef4ad78…
$OUT: clean-tree-before.txt frozen.stdout no-harm.stdout
```

No `DECIDING_REFUSED`; the run entered `no-harm` (`$OUT/no-harm.stdout` written) and was still running when my timeout fired. The gate's header promises "every pre-registered
control receipt is committed at REV in a commit that descends from FREEZE" — with `FREEZE == REV`
*every* commit descends from the freeze, including the one that wrote the receipts after seeing the
results.

This is live for this round, not hypothetical: the working tree already carries post-freeze counter
bytes (`c2/measure.py` `36ca47d…` vs frozen `9d076812…`, `contract.json` `5de4f37…` vs `2388cb50…`),
so the L1 must either re-point `FREEZE` (making F1 the operative hole) or accept
`FROZEN_UNCHANGED=0` (F7).

Smallest safe correction — pin the freeze exactly as `BASE` is pinned:

```diff
 BASE=0a2010acd1e92e4e332774050825e21bcfc7e079
+FREEZE_SHA=631cd6455e58dce969310b4c0466c3383d9f5108
 …
 FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
+[ "$FREEZE" = "$FREEZE_SHA" ] || { echo "DECIDING_REFUSED freeze-is-not-the-round-freeze"; exit 3; }
+[ "$FREEZE" != "$REV" ] || { echo "DECIDING_REFUSED freeze-is-rev"; exit 3; }
+git merge-base --is-ancestor "$FREEZE" "$REV" || { echo "DECIDING_REFUSED freeze-not-ancestor-of-rev"; exit 3; }
```

### F2 (critical) — the manifest's key set is never compared to the contract

`fr['files']` is iterated as given (lines 24–33). Nothing requires it to cover
`contract.frozen_paths`. Dropping one key reduces coverage silently and the gate still prints `OK`.

Fixture `fxC` — `c1/measure.py` (the counter that decides C1) gets a line appended, and its key is
deleted from `freeze.json`, one commit, `FREEZE = REV`:

```
FREEZE_INTEGRITY: OK files=5 amendments=0
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-55/control/controls-a.stdout
manifest keys: [c2/measure.py, contract.json, controls.sh, deciding-run.sh, no-harm.sh]
tampered c1 tail:  # tampered by critic
```

The gate walked past a tampered C1 counter to the *next* refusal. Contrast `a1`, the same tamper with
the key present: `FREEZE_INTEGRITY: MISMATCH` → `DECIDING_REFUSED freeze-integrity`.

Smallest safe correction:

```diff
 fr = json.loads(...)
+contract = json.loads(subprocess.run(['git','-C',lane,'show','%s:%s/contract.json' % (freeze,E)],
+                     capture_output=True, env=env, check=True).stdout)
+want = set(contract['frozen_paths']) - {'%s/freeze.json' % E}
+if set(fr['files']) != want:
+    bad.append('manifest-keys %s != %s' % (sorted(fr['files']), sorted(want)))
```

### F3 (critical) — receipt *existence* is checked on the blob, receipt *content* on the working tree

Lines 48–50 read the blob at `$REV`; lines 54–55 grep `$LANE/$E/control/…` — the working-tree path.
The two halves describe different objects, so any way of making the working tree disagree with the
blob passes. Two are available without touching the freeze:

**(a) symlink receipts.** Git mode `120000` is a `blob`; `cat-file -s` returns the *target path length*,
so the emptiness arm is satisfied by the link itself. `grep` follows the link.

Fixture `fxLink` (freeze `631cd64`, REV one commit later adding the receipts + a prose file):

```
controls-a.stdout type=blob size=20 content='../../../notes/a.txt'
controls-b.stdout type=blob size=20 content='../../../notes/b.txt'
working-tree read: 2:CONTROLS_A: 4/4 as pre-registered
FREEZE_INTEGRITY: OK files=6 amendments=0
FROZEN_UNCHANGED=1 freeze=631cd64… rev=d8812cde…
```

Gate cleared, run entered `no-harm` and was still running when my timeout fired. The committed "receipt" is a pointer to prose; the receipt body
is never read.

**(b) `assume-unchanged`.** Commit the receipts as one byte of newline, then put the verdict text in the
working tree and hide it from `git status`.

Fixture `fxAssume`, `FREEZE = REV = c213a7db…`:

```
control (no index flag):  M .ufo/evidence/round-55/control/controls-a.stdout   -> DECIDING_REFUSED dirty-tree
with assume-unchanged:    (status empty)
working tree vs blob (a): DIFFERENT
FREEZE_INTEGRITY: OK … FROZEN_UNCHANGED=1 …
```

Same working-tree bytes, opposite verdicts; the flag is what decides.

A third, cheaper variant is already recorded: `a4` shows a 1-byte blob passing lines 48–50 and dying
only at the working-tree grep — the emptiness arm is about the blob, the content arm is not.

Smallest safe correction — read the content from the same object the size from:

```diff
-grep -q '^CONTROLS_A: [0-9]*/[0-9]* as pre-registered' "$LANE/$E/control/controls-a.stdout" 2>/dev/null || { …; }
-grep -q '^CONTROLS_B: [0-9]*/[0-9]* as pre-registered' "$LANE/$E/control/controls-b.stdout" 2>/dev/null || { …; }
+git ls-tree "$REV" -- "$E/control/controls-a.stdout" | grep -q '^100644 ' || { echo "DECIDING_REFUSED control-receipt-not-a-regular-file $f"; exit 3; }
+git show "$REV:$E/control/controls-a.stdout" | grep -q '^CONTROLS_A: [0-9]*/[0-9]* as pre-registered' || { echo "DECIDING_REFUSED controls-a-verdict-missing"; exit 3; }
+git show "$REV:$E/control/controls-b.stdout" | grep -q '^CONTROLS_B: [0-9]*/[0-9]* as pre-registered' || { echo "DECIDING_REFUSED controls-b-verdict-missing"; exit 3; }
```

(`git show` on a symlink prints the target path, so the symlink case then fails the verdict arm too.)

### F4 (high) — the receipts' exit side and the control counts are never read

Lines 48–55 require existence, blob-ness, a positive byte count, ancestry and the literal
`^CONTROLS_[AB]: [0-9]*/[0-9]* as pre-registered`. They never read `controls-*.exit`, never count `^CTL `
lines, and never open `contract.json`'s `claims.C1.controls` / `claims.C2.controls`
(`CTL_0, CTL_SKIP, CTL_FAB, CTL_POS` / `CTL_0, CTL_SKIP, CTL_BREAK, CTL_POS`). "As pre-registered" is
therefore a self-assertion.

Fixture `fxExit` — receipts with `CONTROLS_A: 4/4 as pre-registered`, `CONTROLS_B: 4/4 as
pre-registered`, and both `.exit` blobs containing `1`:

```
committed exit receipts: 1  1
FREEZE_INTEGRITY: OK … FROZEN_UNCHANGED=1 …
```

A control run that failed its own pre-registration is accepted. Fixture `fxZero` — receipts whose entire
body is `CONTROLS_A: 0/0 as pre-registered` (zero `CTL ` lines, no control ran, none failed): also
accepted, `FROZEN_UNCHANGED=1`, `0/0` matched.

Smallest safe correction: require the exit side and bind the counts to the contract:

```diff
+[ "$(git show "$REV:$E/control/controls-a.exit")" = 0 ] || { echo "DECIDING_REFUSED controls-a-exit-nonzero"; exit 3; }
+[ "$(git show "$REV:$E/control/controls-a.stdout" | grep -c '^CTL ') " = "$(git show "$REV:$E/control/controls-a.stdout" | sed -n 's/^CONTROLS_A: \([0-9]*\)\/[0-9]* as pre-registered$/\1/p')" ] || { echo "DECIDING_REFUSED controls-a-count-mismatch"; exit 3; }
```

(and the same for B, plus one `grep -q "CTL $name "` per name in `contract.claims.C*.controls`).

### F5 (high) — the clean-tree guard is weaker than its claim, and its exclusion is unanchored

Line 57 is `git status --porcelain` (default untracked mode, no index-flag audit); line 58 excuses any
untracked path whose name *starts with* the OUTDIR string.

- **index flags**: `a10b` above — a tracked receipt differs from REV and the tree reads clean.
- **prefix**: fixture `fxOutP`, OUTDIR `.ufo/evidence/round-55/deciding`, untracked sibling
  `.ufo/evidence/round-55/decidingX/evil.txt`:

```
status --porcelain: ?? .ufo/evidence/round-55/decidingX/
gate's own filter:  grep -vc "^?? .ufo/evidence/round-55/deciding" -> 0
FREEZE_INTEGRITY: OK … FROZEN_UNCHANGED=1 …
```

Any untracked content can be parked under a sibling name and is invisible to the gate. (Ordinary dirt
is still caught: `a8` untracked outside OUTDIR → `DECIDING_REFUSED dirty-tree`; `a10a` plain receipt
modification → `DECIDING_REFUSED dirty-tree`.)

Smallest safe correction:

```diff
 git status --porcelain > "$OUT/clean-tree-before.txt"
-[ "$(grep -vc "^?? ${OUT#$LANE/}" "$OUT/clean-tree-before.txt")" = 0 ] || { …; }
+[ -z "$(git ls-files -v | grep -vE '^H ')" ] || { echo "DECIDING_REFUSED index-flags"; git ls-files -v | grep -vE '^H '; exit 3; }
+[ "$(grep -vxF "?? ${OUT#$LANE/}/" "$OUT/clean-tree-before.txt")" = "" ] || { echo "DECIDING_REFUSED dirty-tree"; cat "$OUT/clean-tree-before.txt"; exit 3; }
```

### F6 (medium) — the invocation marker follows symlinks and OUTDIR emptiness is never required

Line 56 uses `[ -e "$OUT/$k.start" ]`; `-e` follows symlinks, so a *dangling* link reads as "no previous
invocation". Fixture `fxSecond`: `$OUT/c1.start` and `$OUT/c2.start` are symlinks into
`$S/redir/` that do not exist yet.

```
marker test: [ -e ]=absent [ -h ]=link
FREEZE_INTEGRITY: OK … FROZEN_UNCHANGED=1 …
after the run: markers still symlinks; [ -e ]=no  (a third invocation would also pass)
```

Separately, the usage says OUTDIR must be "existing, EMPTY"; line 44 only checks `-d`, so a pre-used
directory is accepted. And because the script later does `> "$OUT/$k.start"`, a marker that is a symlink
is written *through* to its target (verified separately:
`date -u > c1.start` where `c1.start` is a dangling link keeps the link and creates the target), so the
marker never becomes visible inside OUT.

Smallest safe correction:

```diff
-[ -d "$OUT" ] || { echo "DECIDING_REFUSED outdir-missing"; exit 3; }
+[ -d "$OUT" ] || { echo "DECIDING_REFUSED outdir-missing"; exit 3; }
+[ -z "$(ls -A "$OUT")" ] || { echo "DECIDING_REFUSED outdir-not-empty"; ls -A "$OUT"; exit 3; }
 …
-for k in c1 c2; do [ -e "$OUT/$k.start" ] && { …; }; done
+for k in c1 c2; do { [ -e "$OUT/$k.start" ] || [ -h "$OUT/$k.start" ]; } && { echo "DECIDING_REFUSED second-invocation $k"; exit 3; }; done
```

### F7 (medium) — a detected frozen drift is not a refusal, and it burns the single invocation

Line 66 sets `rc=1` and continues into `no-harm`, the precheck, the census and both counters. Fixture
`fxDrift` (receipts committed, then one post-freeze line appended to `c2/measure.py`), run
`REV=<drifted> FREEZE=<the freeze>`:

```
FREEZE_INTEGRITY: OK files=6 amendments=0
FROZEN_UNCHANGED=0 freeze=b8eb2332… rev=29d19a1b…
 .ufo/evidence/round-55/c2/measure.py | 2 ++
```

No `DECIDING_REFUSED`. Run to my own 280 s wall, the script had by then executed all 15 no-harm
monitors, the cold-read precheck (`COLDREAD_PRECHECK … lost=0 ok`), the census (`CENSUS exit=0`) and the
whole C1 counter (`C1_R55: … total=10 C1_R55_PASS=false`) — i.e. it spent the entire deciding sequence
*knowing* the frozen set had moved. `c1.start`/`c2.start` were then written, so the round cannot be
re-run after the drift is discovered. The final exit would be 1 (`rc=1` on line 66, `exit $rc` on the
last line) — that last step is code reading, not measured, because my wall fired first.

Smallest safe correction: make it a refusal where it is detected (it already runs before the counters):

```diff
-if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 …" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 …" | tee "$OUT/frozen.stdout"; git diff --stat … | tee -a "$OUT/frozen.stdout"; rc=1; fi
+if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 …" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 …" | tee "$OUT/frozen.stdout"; git diff --stat … | tee -a "$OUT/frozen.stdout"; echo "DECIDING_REFUSED frozen-drift"; exit 3; fi
```

### F8 (low) — three duplicate authorities that agree today

Line 69 hardcodes `15` while `contract.no_harm_monitors` is `15`; line 66 hardcodes the seven frozen
paths while `contract.frozen_paths` has the same seven; `contract.deciding_invocations: 1` is never read
(the rule is enforced only through the two marker files). All three agree at `631cd64`
(`freeze.json.files` covers 6 of the 7 contract paths — `freeze.json` itself is excluded by the
manifest's own note), so this is latent drift, not a live mismatch. Correction: read the three values
from `contract.json` at `REV`, as the freeze-integrity block already does for the manifest.

## What I did not do

- Did not edit `deciding-run.sh` or any frozen file, did not run a mutating git command in the lane, did
  not write a lane production file. All commits are in `--shared` clones under my scratch.
- Did not score C1/C2 or re-run the counters to completion (irrelevant to the gate; the four completed
  passing runs above stop in `no-harm` because of *my* timeout, after every refusal had been cleared).
- Did not test `cd "$LANE"` failure (R2) separately: it is the same `|| exit 2` shape as R1/R3/R4 and
  would require an unreadable directory inside my own scratch.

## Axes touched

- **calibration**: the gate is the round's provenance instrument for both counters; F1–F4 mean it can
  certify a fabricated receipt set, which is the axis' failure mode (false provenance).
- **operability**: F6/F7 — the marker and the drift path decide whether a legitimate retry exists.

No tool was installed or upgraded by this seat (`uv tool`/`npx`/binary channels untouched; pacman
paused host-wide). Census at seat start: `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → `ok`, exit 0. Seat-end census in the receipt
`census-end.out`.
