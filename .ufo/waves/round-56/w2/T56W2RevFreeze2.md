# T56W2RevFreeze2 — freeze integrity at C0 (wave 2)

**Seat:** T56W2RevFreeze2 (reviewer) · **Round:** 56 · **Wave:** 2
**Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**C0 (content commit):** `c0137451f5b7f22d65f748fc69f1b181f55e1378`
**Base:** `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`
**Freeze named by the item:** `c3e2ca9f020776b3d66c7af854fb82c834674fcf`
**Scratch:** `/fast/scratch/hyaku/tameshi-r56/T56W2RevFreeze2` (removed on exit)
**Receipts:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w2/T56W2RevFreeze2-receipts/`

---

## Verdict

**The item's literal check FAILS as written, but the freeze is NOT voided.**

The item asserts that `git diff c3e2ca9 C0 -- <the eleven instrument paths>` must print
nothing, and that a difference means "an instrument that changed without an amendment voids
the freeze". The diff **does** print (7 files, 190 insertions, 43 deletions). However, every
one of those seven changes landed in **a single, properly-recorded amendment commit**
(`21eb3c63cd0f3190c0deeb8953c6c91c7742cd68`, parent = the freeze `c3e2ca9`), recorded in
`freeze.json` under `amendments[0]` with `prior_freeze: c3e2ca9f…`, and mirrored verbatim in
`contract.json`. The round's own frozen integrity logic accepts it:

```
FREEZE_INTEGRITY: OK files=12 amendments=1     (FREEZE=21eb3c6)
```

So the freeze is intact; **the operative freeze at C0 is `21eb3c6`, not `c3e2ca9`.** The item's
premise that `c3e2ca9` is the freeze is stale, and that staleness is itself the actionable
defect — see **Finding 1**.

**Status at the end of this seat: F1 is fixed** (the L1 re-pinned `build-spec-w3.py` to
`21eb3c6` and recorded the same conclusion in
`.ufo/waves/round-56/integration/freeze-pointer-preflight.stdout`). **F1b and F2 remain live in
`build-spec-w3.py`** — the wave-3 C2 seat task still compares the counter against a `before/`
receipt taken at the *original* freeze (so it reports a false 19/19-vs-14/14 mismatch), and the
wave-3 `FROZEN_UNCHANGED` seat task still checks 11 of the 13 frozen paths.

**Closing state (re-verified after the L1's last edit to `build-spec-w3.py`, mtime 16:45:47):**

| item | state | evidence |
|---|---|---|
| F1 stale freeze pin | **FIXED** — `build-spec-w3.py:14` = `21eb3c6…` | `a10` |
| F1b before-receipt comparison | **LIVE** — line 68 still reads "run it at the freeze `{FREEZE}` and confirm it matches `{E}/before/c2.stdout`" | `a10` |
| F2 frozen path list | **LIVE** — line 95 lists 11 of `contract.frozen_paths`' 13; OMITTED = the two `c2/red-before/round-54-ctl-pos-c1.stdout[.sha256]` | `a10` |

`spec-w3.json` has not been generated yet, so both live items are still correctable before wave 3
dispatches. The L1 has acknowledged both as recorded discrepancies; the decision on whether to
amend the two seat tasks or to re-take `before/c2.stdout` is the L1's, and neither is an edit this
seat may make.

---

## Finding 1 (HIGH) — the wave tooling still pins the pre-amendment freeze `c3e2ca9`, which the deciding run refuses

Every wave-spec generator and every built spec still names `c3e2ca9f020776b3d66c7af854fb82c834674fcf`
as "the frozen instruments":

```
.ufo/waves/round-56/build-spec-w1.py:8   FREEZE = "c3e2ca9f020776b3d66c7af854fb82c834674fcf"
.ufo/waves/round-56/build-spec-w2.py:12  FREEZE = "c3e2ca9f020776b3d66c7af854fb82c834674fcf"
.ufo/waves/round-56/build-spec-w3.py:14  FREEZE = "c3e2ca9f020776b3d66c7af854fb82c834674fcf"
.ufo/waves/round-56/spec-w1.json, spec-w2.json  (same SHA in the context string)
```

`deciding-run.sh` (frozen at C0) pins the freeze to the last commit that touched `freeze.json`
and refuses anything else:

```
deciding-run.sh:92  FREEZE_LAST=$(git log -1 --format=%H "$REV" -- "$E/freeze.json")
deciding-run.sh:93  [ "$FREEZE" = "$FREEZE_LAST" ] || { echo "DECIDING_REFUSED freeze-not-last-manifest-commit $FREEZE"; exit 3; }
```

**Command and output** (real `deciding-run.sh`, real clone at C0; receipt `a5-deciding-run-freeze-gate.txt`):

```
### deciding-run.sh with FREEZE=c3e2ca9 (the pin in build-spec-w1/w2/w3.py, spec-w1.json, spec-w2.json)
FREEZE_INTEGRITY: OK files=10 amendments=0
DECIDING_REFUSED freeze-not-last-manifest-commit c3e2ca9f020776b3d66c7af854fb82c834674fcf
EXIT=3

### deciding-run.sh with FREEZE=21eb3c6 (the last commit touching freeze.json at C0)
FREEZE_INTEGRITY: OK files=12 amendments=1
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-56/control/controls-a.stdout
EXIT=3
```

With the pinned `c3e2ca9` the deciding run dies at gate 0 on the freeze pointer, before the
counters ever run — and `deciding_invocations: 1` in the contract means that first, refused
invocation is a spent invocation. With `21eb3c6` it proceeds to the *next* gate
(`control-receipt-missing`, which is expected — the control receipts are wave-3's to produce).

The same stale pin is baked into the wave-3 seat task text (receipt `a8-stale-pin-downstream.txt`):

```
build-spec-w3.py:95  "Check FROZEN_UNCHANGED at PIN: git -C {LANE} diff {FREEZE} {PIN} -- ... must print nothing"
```

Against `c3e2ca9` that diff prints the 7-file amendment diff, so the seat would report a
false "instruments changed without an amendment" against a legitimately amended freeze.

**The fix is one line per generator**: `FREEZE = "21eb3c63cd0f3190c0deeb8953c6c91c7742cd68"`.
This is in `.ufo/waves/` (untracked, not a lane production file), so it is the L1's to change;
I did not edit it.

**STATUS UPDATE (L1 has since acted):** `build-spec-w3.py:14` now reads
`FREEZE = "21eb3c63cd0f3190c0deeb8953c6c91c7742cd68"` (file mtime 16:40:34, after my first
message), and `.ufo/waves/round-56/integration/freeze-pointer-preflight.stdout` independently
records the same conclusion:

```
deciding-run freeze precondition at C0: last=21eb3c63cd0f3190c0deeb8953c6c91c7742cd68 old=c3e2ca9f020776b3d66c7af854fb82c834674fcf old_matches=false updated=21eb3c63cd0f3190c0deeb8953c6c91c7742cd68 updated_matches=true
```

**F1 is therefore closed for wave 3.** `build-spec-w1.py:8` and `build-spec-w2.py:12` still carry
the old SHA, but both waves are already dispatched (spec-w1.json / spec-w2.json exist and were
built from them), so those two generators are historical — they do not produce wave-3's spec and
cannot re-poison the deciding run. **F1b and F2 below are still live in `build-spec-w3.py`.**

### 1b (MEDIUM) — `before/c2.stdout` is stale against the amended gate

`before/c2.stdout` was taken at the *original* freeze with the 14-case gate and is committed at
C0. After amendment 1 the gate's selftest is 19 cases, so the same counter at the same revision
no longer reproduces that receipt. Verified byte-exactly by diffing the counter's own output
against the committed receipt:

```
c2/measure.py @ c3e2ca9  vs before/c2.stdout  ->  diff lines: 0   (byte-identical)
c2/measure.py @ 21eb3c6  vs before/c2.stdout  ->  diff lines: 8
  1c1
  < EXPLAIN arm1-selftest exit=0 14/14
  ---
  > EXPLAIN arm1-selftest exit=0 19/19
  6c6
  < C2_R56: rev=c3e2ca9f0207 selftest=14/14 ... total=2 C2_R56_PASS=false
  ---
  > C2_R56: rev=21eb3c63cd0f selftest=19/19 ... total=2 C2_R56_PASS=false
```

The wave-3 seat task (`build-spec-w3.py:68`) still reads "Then run it at the freeze `{FREEZE}` and
confirm it matches `{E}/before/c2.stdout`". With `FREEZE` now correctly pinned to `21eb3c6`,
that comparison **fails on the very line the seat is told to check** (`selftest=19/19` vs the
receipt's `14/14`), so the seat will report a false mismatch against a correct receipt. The
comparison must name the revision the before-receipt was taken at (`c3e2ca9`) — the correct
semantic is "the before receipt reproduces at the original freeze" — or `before/c2.stdout` must
be re-taken. Both are L1 decisions on a committed receipt; I did not edit it.

**This is now sharper than when I first reported it:** before the L1's pin fix the seat would
have compared 19/19 against a receipt taken at the original freeze (same false mismatch); after
the fix the comparison is at least against the right freeze, but the receipt still says 14/14.
Either way the seat task as written cannot pass.

---

## Finding 2 (no defect — the manifest is honest) — all 12 digests re-derive at C0

`freeze.json` at C0 carries 12 file digests and 1 amendment. Re-derived from the C0 bytes with
the canonical key mapping (`tools/…` and `.ufo/evidence/round-21|48/…` verbatim, everything
else relative to `.ufo/evidence/round-56/`), **12/12 match** (receipt `a4-freeze-digest-rederivation.txt`):

```
OK    c1/lost-headings-at-base.json                    expect=dcfc9f800b8bc7b2 got=dcfc9f800b8bc7b2
OK    c1/measure.py                                    expect=048122cf1c7c65d2 got=048122cf1c7c65d2
OK    c2/measure.py                                    expect=915580190cb1d5c3 got=915580190cb1d5c3
OK    c2/red-before/round-54-ctl-pos-c1.stdout          expect=3310ff60802af889 got=3310ff60802af889
OK    c2/red-before/round-54-ctl-pos-c1.stdout.sha256   expect=2491775e3a6b2f75 got=2491775e3a6b2f75
OK    c2/red-before/round-54-surface.paths              expect=95ead282432b1bde got=95ead282432b1bde
OK    contract.json                                    expect=254dd0983735ae61 got=254dd0983735ae61
OK    control/frozen-surface.paths                     expect=46c93f105b61d825 got=46c93f105b61d825
OK    controls.sh                                      expect=65b4b5105668786f got=65b4b5105668786f
OK    deciding-run.sh                                  expect=a644123e764a568f got=a644123e764a568f
OK    no-harm.sh                                       expect=a13ba1a8433752c8 got=a13ba1a8433752c8
OK    tools/receipt-revision-gate.py                   expect=c60772ceb0ce3f51 got=c60772ceb0ce3f51
---
ALL_FREEZE_JSON_DIGESTS_REDERIVE_AT_C0 = True
```

Confirmed independently by the round's own frozen generator (receipt `a6-freeze-gen.txt`):

```
$ python3 .ufo/waves/round-56/freeze-gen.py --lane … --rev c0137451f5b7f22d65f748fc69f1b181f55e1378 --explain
FREEZE_GEN_SET regenerated=12 manifest=12 amendments=1
FREEZE_GEN: files=12 ok
exit=0
```

And by the deciding run's own freeze-integrity heredoc (receipt `a7-amendment-record.txt`):
`FREEZE_INTEGRITY: OK files=12 amendments=1`, rc=0.

---

## Finding 3 (no defect) — the amendment is well-formed and honest

* **Exactly one** commit touches the frozen surface between the freeze and C0
  (`21eb3c6`, parent = `c3e2ca9`); nothing after it touches any frozen path.
* `git rev-list --count C0 -- .ufo/evidence/round-56/freeze.json` = **2** = `len(amendments)+1` = 2,
  which is exactly the shape `deciding-run.sh:64-77` enforces.
* `contract.json.amendments == freeze.json.amendments` (byte-identical) — the check at
  `deciding-run.sh:78`.
* Every changed file is covered by the amendment's `what` text (a)–(f): `c2/measure.py` (a),
  `controls.sh` (b), `deciding-run.sh` (c), `tools/receipt-revision-gate.py` (d),
  `control/frozen-surface.paths` (e), and the two newly-manifested red-before files (f).
* **The amendment's truth claims check out where I could test them:**
  * (a) "arm6 read SOURCES' status column at index 8 (the opened date) … now `cells[7]`" — the
    SOURCES header is `id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`,
    so `cells[7]`=status, `cells[8]`=opened. `cells[8]=='mined'` was unreachable; `cells[7]=='mined'`
    is the status column. Correct.
  * (a) "the suite is 19 cases" — `GATE_SELFTEST: 19/19 pass`, exit 0.
  * (d) "`drifted_paths` reports paths unresolvable at both revisions" — implemented at
    `tools/receipt-revision-gate.py:74-79`.
* **Denominators and predicates are unchanged**, as the amendment claims: `c2/measure.py` has the
  same 6 arm markers, the same 10 `total += 1` sites and the same `docs != 4` at both revisions.
  The counter was made *reachable*, not *easier* — the previously-unreachable docs cell now scores.
* The amendment did not touch any content file: `SKILL.md`, `corpus/QUALITY.md`,
  `corpus/SOURCES.md`, `corpus/knowledge/receipt-revision-binding.md`, `corpus/lessons/round-56.md`
  and `tools/registry.json` were changed by **C0**, not by the amendment.
* No deciding invocation and no control score existed before the amendment: at C0 the only file
  under `.ufo/evidence/round-56/control/` is `frozen-surface.paths` — `controls-a.stdout`,
  `controls-b.stdout` and their `.sha256` sidecars are **absent**, and there is no deciding-run
  output anywhere. The amendment's "before any control score and before any deciding invocation"
  claim holds.

---

## Finding 4 (no defect) — the frozen surface is byte-identical to C0 *from the operative freeze*

The item's eleven paths, diffed against the **operative** freeze `21eb3c6`, print nothing
(receipt `a3-item-diff-amended-freeze-to-C0.txt`, **0 bytes**):

```
$ git diff 21eb3c63cd0f3190c0deeb8953c6c91c7742cd68 c0137451f5b7f22d65f748fc69f1b181f55e1378 -- <the eleven paths>
(no output — 0 bytes)
```

Per-path status between the item's named freeze `c3e2ca9` and C0 (receipt `a2-item-diff-stat.txt`):

| path | c3e2ca9 → C0 |
|---|---|
| `.ufo/evidence/round-56/c1/measure.py` | UNCHANGED |
| `.ufo/evidence/round-56/c1/lost-headings-at-base.json` | UNCHANGED |
| `.ufo/evidence/round-56/c2/red-before/round-54-surface.paths` | UNCHANGED |
| `.ufo/evidence/round-56/no-harm.sh` | UNCHANGED |
| `.ufo/evidence/round-56/c2/measure.py` | changed (amendment (a)) |
| `.ufo/evidence/round-56/contract.json` | changed (amendment record) |
| `.ufo/evidence/round-56/control/frozen-surface.paths` | changed (amendment (e)) |
| `.ufo/evidence/round-56/controls.sh` | changed (amendment (b)) |
| `.ufo/evidence/round-56/deciding-run.sh` | changed (amendment (c)) |
| `.ufo/evidence/round-56/freeze.json` | changed (amendment record) |
| `tools/receipt-revision-gate.py` | changed (amendment (d)) |

The item's eleven-path list also **omits two paths that are now on the frozen surface** —
`.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout` and its `.sha256` sidecar. Both
were committed *at* the freeze `c3e2ca9` but were in **no manifest** there (wave-1's H3 finding);
amendment (f) put them in both `contract.frozen_paths` and `freeze.json`. Both are byte-unchanged
between `c3e2ca9` and C0, so omitting them hides nothing — but the item's list is not the
contract's surface (13 paths, not 11) and should be re-derived from `contract.frozen_paths`.

**STILL LIVE in wave 3.** The wave-3 seat task's path list (`build-spec-w3.py:95`) is the same
11-path list; parsing it against the contract gives:

```
seat task list (11) vs contract.frozen_paths (13)
OMITTED from the seat task: ['.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout.sha256',
                             '.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout']
EXTRA in the seat task   : []
```

So the wave-3 `FROZEN_UNCHANGED` seat checks 11 of the 13 frozen paths. The two omitted files are
byte-unchanged between the freeze and C0, so this does not produce a false failure — but the
seat's check would not catch a post-freeze mutation of either red-before file, and it is not the
check `deciding-run.sh` itself performs (that one derives `FROZEN` from `contract.frozen_paths`
and so covers all 13).

---

## Finding 5 (LOW) — the item's own premise is stale, not a defect in the tree

The item says the frozen instruments are `c3e2ca9f020776b3d66c7af854fb82c834674fcf`. That was
true when the item was written (wave 1) but is not true at C0: the freeze moved once, by a
recorded amendment, to `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68`. The freeze.json `prior_freeze`
field is the round's own mechanism for exactly this, and it is populated correctly. The residual
risk is that a reader who takes the item's SHA literally will conclude the freeze was voided when
it was not, and (separately) that the deciding run must be invoked with a SHA it refuses.

---

## Verification gaps / residual risk

* I did **not** run the deciding run to completion: at C0 the control receipts
  (`controls-a.stdout`, `controls-b.stdout`) do not exist yet, so the run stops at
  `control-receipt-missing` even with the correct freeze. The gate reached is real evidence, not
  a proxy — receipt `a5-deciding-run-freeze-gate.txt`.
* I did not verify the `FROZEN_UNCHANGED=1` result at a post-bind PIN; at C0 the equivalent check
  against the operative freeze is `FROZEN_UNCHANGED=1` (I ran the deciding run's own
  `git diff --quiet "$FREEZE" "$REV" -- $FROZEN` with `FREEZE=21eb3c6`, `REV=C0` → identical).
* The amendment's claims (c) and (e) I checked structurally (the code paths and the added surface
  entries exist at C0); I did not re-execute every wave-1 finding that motivated them — those are
  wave-1 seats' scope.
* `build-spec-w3.py` has not been run yet (`spec-w3.json` does not exist), so Finding 1 is still
  cheap to fix — after the fix, the wave-3 spec will carry the right SHA.

## Census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
… W04 duplicate-url warnings …
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
validate EXIT=0
```

`census` subcommand: `tameshi rows 142` (tier.A 127, tier.B 12, tier.C 3; mined 114, queued 21,
rejected 7). Base was **140** rows; C0 adds **S281 and S282** = 142. The assignment's "141 rows
after this round's one new row" does not match the tree: this round added **two** rows, and the
census reports 142. Exit code 0 as required.

## Tooling

No installs. Host tools used: `git`, `python3` (3.14), `bash`, `sha256` (via `hashlib`),
`mktemp`, `clone --shared`. No mutating git/jj command ran against the lane; every fixture was a
`git clone --shared` + `git checkout --detach` in a scratch dir with
`git rev-parse --show-toplevel` asserted equal to that dir before any write.

## Commands run (summary)

1. `git diff c3e2ca9 C0 -- <item's eleven paths>` → non-empty (7 files). → `a1`, `a2`
2. `git diff 21eb3c6 C0 -- <item's eleven paths>` → empty (0 bytes). → `a3`
3. sha256 re-derivation of all 12 `freeze.json` digests from C0 bytes. → `a4`
4. `deciding-run.sh` at C0 with `FREEZE=c3e2ca9` vs `FREEZE=21eb3c6`. → `a5`
5. `freeze-gen.py --rev C0` and `--rev 21eb3c6`. → `a6`
6. deciding run's freeze-integrity heredoc at both candidates; `git log`/`rev-list` on the frozen
   surface; amendment-record shape and mirroring. → `a7`
7. stale-pin sweep over `build-spec-w{1,2,3}.py`; `c2/measure.py` at both freezes vs
   `before/c2.stdout`. → `a8`
8. `sources-census.sh validate` + `census`. → `a9`
