# T54W2Sent04 — sentinel attack: the deciding script's control gate

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, round 54 wave 2, L1 `TameshiR54a2`.
Item under test (verbatim): *"Sentinel attack: abuse the control gate. run the deciding script in a
scratch clone BEFORE committing your own control receipt (or with a missing one) and show
`DECIDING_REFUSED control-receipt-missing` with nothing executed; then show `DECIDING_REFUSED
second-invocation` on a second run. Never touch the lane's own files. Report the verdict lines and
the exact bytes."*

Everything below ran against pinned commit hashes; this seat never wrote the lane. The lane's HEAD
moved while this seat ran (the L1 landed `8da3539`, then `4e2de73`); the attacked revs are hashes,
so the receipts stay valid. Witness at the end.

## Verdict — the two required refusals

Both required refusals fire, exit 3, and execute nothing.

| # | state | command result | bytes on stdout | side effects |
|---|-------|----------------|-----------------|--------------|
| 1 | `REV=C1 99c3bc8`, no control receipt committed at `REV` | `rc=3` in **5 ms** | ``DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-54/control/controls-a.stdout`` + `\n` (90 B, sha256 of the file `be7e168c…`) | outdir 0 files; `$HYAKU_SCRATCH` work dir never created; clone tree clean |
| 2 | real first invocation completed (6 markers in the outdir), identical command re-run | `rc=3` in **21–22 ms** | ``DECIDING_REFUSED second-invocation c1`` + `\n` (38 B, sha256 of the file `d2892d7d…`) | outdir file-set+size sha **unchanged** (`dc8173d4…`); `c1.start`/`c2.start` mtimes untouched (11:58:32 / 11:59:09 -0300); second-run scratch root never created |

Exact first-run state that made arm 2 a *second* run (the genuine invocation, 281 s, rc=1):
`c1.start=2026-10-28T14:58:32Z`, `c1.end=…14:59:09Z`, `c2.start=…14:59:09Z`, `c2.end=…15:02:13Z`,
`frozen.stdout=FROZEN_UNCHANGED=1 freeze=441c26bec5e4… rev=f2a45fb5a655…`,
`DECIDING_RUN_EXIT=1`. Its rc=1 is **expected and not a finding**: the fixture tree is C1 with no
re-key ledger entries (`C1_R54: … rekeyed=0/7 readers=0/7 … C1_R54_PASS=false`) and with the
pre-amendment counters (`C2_R54: … usable_ok=6 … C2_R54_PASS=false`); it is cited only to prove the
gate opened and both counters ran exactly once.

## Bytes and revs under attack

| role | rev | `deciding-run.sh` sha256 |
|------|-----|--------------------------|
| C1 (the wave-2 fix commit) and the freeze `441c26be` | `99c3bc88d704566197783f66b211ee0a830e0330` | `8a26856a81b6c8505b6f076a227b62c31fb04b179bd74aae706e70d8c7e44194` |
| shipped tip at the start of this seat | `097985c18b9a186c310bd35890b95b733cbb7f5b` | `42fb069da6ab01dcac448889eada7437012061bc48bc86731d514360e1e6ab92` |
| live tip after the L1's amendment 3 | `4e2de731b52dbf1bfc0e8fac8fe4fe2cf5bb2bf3` | `42fb069d…` (unchanged) |

The control-gate block is lines 22–28 of the C1/freeze bytes (`8a26856`) and lines 49–55 of the shipped bytes (`42fb069`, which prepends the freeze-digest block at 20–46):
`CONTROLS="$E/control/controls-a.stdout $E/control/controls-a.exit $E/control/controls-b.stdout $E/control/controls-b.exit"`;
`git cat-file -e "$REV:$f" || DECIDING_REFUSED control-receipt-missing $f`;
`c=$(git log -1 --format=%H "$REV" -- "$f"); git merge-base --is-ancestor "$FREEZE" "$c" || DECIDING_REFUSED control-receipt-not-after-freeze $f`;
`for k in c1 c2; do [ -e "$OUT/$k.start" ] && { echo "DECIDING_REFUSED second-invocation $k"; exit 3; }; done`.
The counters are extracted **after** these gates (`git show "$REV:$E/$f" > "$SCR/code/$f"`, line 31 at C1 / line 58 at the tip), so a refusal cannot have run one.

## Receipts

Driver: `T54W2Sent04-receipts/attack-control-gate.sh` → `attack-control-gate.out`
(sha256 `cd095fa2b87f89bc66e922d6461e097512b168cc44b486eba3cc4aec2242f709`). It clones
`git clone --shared` into `$TMP`, asserts `git rev-parse --show-toplevel` equals the clone, and every
git call names `-C "$D"`. `second-run-after-real-first.sh` reproduces the real first/second run and was executed end to end
(`second-run-after-real-first.out`, sha256 `ae91e497c89227530b8680cac207de8698c1ac9d903ee2e606f0bbabf59517fc`):
`first rc=1 elapsed_s=244`, six markers written, `FROZEN_UNCHANGED=1`, then
`second rc=3 elapsed_ms=21` → `DECIDING_REFUSED second-invocation c1`, outdir file-set+size sha
unchanged, second-run scratch root not created. Captured artifacts: `genuine-first-run/` (the
outdir's 18 receipt files plus the first-run and second-run logs), `live-tip-4e2de73/`,
`predicates.txt`.

```
### 0. object census
+ git -C LANE log --all --oneline -- .ufo/evidence/round-54/control/controls-a.stdout .ufo/…/controls-b.stdout
19c7558 round-54: re-freeze (amendment 2 …), base receipts, phase-A control receipts, …
7e533b1
revs carrying controls-b.stdout: 0

### 1. C1, no receipts, HEAD==REV, empty outdir
rc=3
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-54/control/controls-a.stdout
outdir-files=0
scratch-root-exists=NO
clean-tree-after: []

### 2. same state, second invocation
rc=3
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-54/control/controls-a.stdout
outdir-files=0
scratch-root-exists=NO

### 3. four receipts committed (a bytes from 097985c, b fabricated), clean tree, witness file
fixture HEAD=df1db6f16dd2e43117fcfbaee88a084efd86a996
  controls-a.stdout type=blob sha=7c9c666568c26b17a8d7a04673015dcad1145c68
  controls-a.exit   type=blob sha=573541ac9702dd3969c9bc859d2b91ec1f7e6e56
  controls-b.stdout type=blob sha=105cdf63b8f5380052407809ce9cf3614420d827
  controls-b.exit   type=blob sha=573541ac9702dd3969c9bc859d2b91ec1f7e6e56
rc=3
DECIDING_REFUSED dirty-tree
?? FIXTURE_DIRTY
outdir-files=1
scratch-root-exists=NO          <-- the control gate OPENED; the next gate refused

### 4. identical invocation after a prior c1.start marker
rc=3
DECIDING_REFUSED second-invocation c1
outdir-files=1
scratch-root-exists=NO
outdir: c1.start

### 5. marker at c2.start
rc=3
DECIDING_REFUSED second-invocation c2
outdir-files=1
scratch-root-exists=NO

### 6. four ZERO-BYTE blobs as receipts
  controls-a.stdout type=blob size=0
  controls-a.exit   type=blob size=0
  controls-b.stdout type=blob size=0
  controls-b.exit   type=blob size=0
rc=3
DECIDING_REFUSED dirty-tree       <-- the control gate OPENED on empty receipts

### 6b. four TREE objects at the same paths
  controls-a.stdout type=tree cat-file-exit=0
  controls-a.exit   type=tree cat-file-exit=0
  controls-b.stdout type=tree cat-file-exit=0
  controls-b.exit   type=tree cat-file-exit=0
rc=3
DECIDING_REFUSED dirty-tree       <-- and OPENED again: the check is `cat-file -e`, not "is a receipt"

### 7. shipped tip 097985c, FREEZE=the recorded freeze 441c26be
rc=3
FREEZE_INTEGRITY: OK files=7 amendments=0
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-54/control/controls-b.stdout
outdir-files=0
scratch-root-exists=NO

### 8. shipped tip as its own FREEZE
rc=3
FREEZE_INTEGRITY: OK files=10 amendments=2
DECIDING_REFUSED control-receipt-not-after-freeze .ufo/evidence/round-54/control/controls-a.stdout
outdir-files=0
scratch-root-exists=NO

### 9. the script's own predicate over the 11 frozen paths (predicates.txt)
git diff --quiet 441c26be..C1      -> rc=0 FROZEN_UNCHANGED=1
git diff --quiet 441c26be..097985c -> rc=1 FROZEN_UNCHANGED=0
git diff --quiet 19c7558..097985c  -> rc=1 FROZEN_UNCHANGED=0
git diff --quiet 441c26be..4e2de73 -> rc=1 FROZEN_UNCHANGED=0
git diff --quiet 4e2de73..4e2de73  -> rc=0 FROZEN_UNCHANGED=1
```

Live tip `4e2de73` (the L1's amendment-3 commit), both freeze arguments:

```
FREEZE=441c26bec5e4 -> rc=3  FREEZE_INTEGRITY: OK files=7 amendments=0
                             DECIDING_REFUSED control-receipt-missing …/controls-b.stdout
FREEZE=4e2de73      -> rc=3  FREEZE_INTEGRITY: OK files=10 amendments=3
                             DECIDING_REFUSED control-receipt-not-after-freeze …/controls-a.stdout
```

Byte-exactness: the refusal lines are the whole stdout; `run1.log` is 1 line / 90 bytes,
sha256 `be7e168cc2669b26a534c6b4bc141eccc71e0d23e296280bf2fb20790fe60858`;
`second-run.log` sha256 `d2892d7d5509815f6c5a4935e86fe7fd90ce8e689a44f644901a94ec944e9a1f`;
genuine first-run log sha256 `20c1cc0d8efaa1ec7a0cff33a067aabd511847080bf508c831e7832b57b5aaf0`;
live-tip logs `bbba8a1e…` (441c26be) and `5b0d1f9b…` (4e2de73).

## Findings

### F1 — missing-receipt refusal: no defect (verified)
Severity: none. Exploit path attempted: run the deciding script with no receipt committed in the
rev's tree. Evidence: arm 1/7. It refuses at line 24, exit 3, in 5 ms, before the work dir is created
(line 31 at C1 / line 58 at the tip), so no no-harm/precheck/census/counter byte is produced. Impact: none. Remediation: none.
The 5 ms is itself proof of the gate's ordering (a full invocation took 281 s when it did run).

### F2 — second-invocation refusal: no defect (verified)
Severity: none. Exploit path attempted: re-run the identical command against an outdir the first run
had already written. Evidence: arm 2 and the real-first-run receipt. Exit 3, 22 ms, outdir
file-set+size sha identical, `c1.start`/`c2.start` mtimes unchanged, new scratch root never created.
Impact: none. Remediation: none.
Scope note (not a defect): the marker is written at line 45, so the guard protects the counter phase
only; a first invocation killed during no-harm/precheck/census leaves no marker and a re-invocation
would run them again. That re-runs monitors, never a counter twice, so it does not break
`deciding_invocations: 1`.

### F3 — the control gate checks existence, not content: four zero-byte files open it
Severity: **medium** (the controls are the anti-fabrication layer; an empty receipt satisfies it).
Exploit path: commit four zero-byte files at the four receipt paths. `git cat-file -e` (line 24) and
`git log -- path` (line 25) succeed; the ancestry arm passes because the commit descends from the
freeze. Evidence: arm 6 — `type=blob size=0` for all four paths, gate opened, next gate was
`dirty-tree`, scratch never created. `git cat-file -e` also accepts non-blob objects: arm 6b puts four **tree** objects at the same paths
(`cat-file-exit=0` for each) and the same gate opens — the existence check does not type-check.
Impact: a deciding run can proceed while the `CONTROLS_A: n/n` / `CONTROLS_B: n/n` verdicts are
absent — precisely the layer that is supposed to catch a fabricated counter (CTL_FAB). It cannot by
itself turn a failing counter claim green, but it removes the pre-registration substance the gate
exists to enforce.
Smallest remediation: in the loop, require `[ "$(git cat-file -t "$REV:$f")" = blob ] &&
[ "$(git cat-file -s "$REV:$f")" -gt 0 ]`, and for the two `.stdout` receipts require the phase
line `grep -q '^CONTROLS_\(A\|B\): [0-9]\+/[0-9]\+'` in the committed bytes.

### F4 — the recorded freeze and the shipped instrument bytes have diverged: no FREEZE value satisfies both the manifest and the receipt-ancestry arm at the tip
Severity: **medium** (it can only force a refusal or `rc=1`, never a false PASS, but it blocks the
deciding run as specified and the `FREEZE_INTEGRITY: OK` line then certifies superseded bytes).
Facts (commands in `predicates.txt` and the live-tip logs):
- `freeze.json` at the round's recorded freeze `441c26be` holds **7 files / 0 amendments**; at the
  tip it holds **10 files / 3 amendments** (`19c7558` = 2, `4e2de73` = 3). With
  `FREEZE=441c26be`, the new gate prints `FREEZE_INTEGRITY: OK files=7 amendments=0` — it validates
  the pre-amendment manifest while the counters are extracted from `REV` (line 58 at the tip), i.e. it certifies
  bytes that are not the bytes that will run.
- `git diff --quiet 441c26be..4e2de73 -- <the 11 frozen paths>` → **rc=1** (5 paths moved:
  `c1/measure.py`, `c2/measure.py`, `contract.json`, `deciding-run.sh`, `freeze.json`), so
  `FROZEN_UNCHANGED=0` → `DECIDING_RUN_EXIT=1` at any post-amendment revision.
  `19c7558..097985c` is also rc=1 (`deciding-run.sh` and `freeze.json` moved again).
- The only FREEZE with `FROZEN_UNCHANGED=1` at the tip is the tip itself, and then
  `FREEZE_INTEGRITY: OK files=10 amendments=3` is followed by
  `DECIDING_REFUSED control-receipt-not-after-freeze …/controls-a.stdout`: the phase-A receipts were
  committed at `19c7558`, an ancestor of the tip, so they are "before the freeze".
- The round record still pins the original freeze: `corpus/lessons/round-54.md:5` "Claims frozen at
  `441c26be`", and `.ufo/waves/round-54/w1-registry.json` `"freeze": "441c26bec5e4…"`.
- The deciding revision cannot be C1: at the C1 tree the pre-amendment C2 counter reads
  `usable_ok=6` with `EXPLAIN usable registry-check rc=1` — the failure amendment 2 describes — so a
  deciding run at C1 cannot reach 7/7; the amended counter requires `REV ≥ 19c7558` (and the latest
  C1 counter, `d7749f84…`, requires `REV ≥ 4e2de73`). C1's contract also declares
  `amendments: 0`, so a deciding run at C1 would execute counters whose wave-1 defects are not
  disclosed in the tree being decided.
[INFERENCE] Consequence: at the tip, no single `FREEZE` both validates the live manifest and keeps
the phase-A receipts after the freeze. The L1 must either pass `441c26be` and accept
`FROZEN_UNCHANGED=0`/`DECIDING_RUN_EXIT=1`, or pass the latest freeze and re-commit (touch) the
phase-A receipt bytes after it when committing the phase-B receipts.
Smallest remediation: after the last instrument edit, commit all four receipts in one commit, pass
that commit as `FREEZE` (both gates then hold), and update the freeze pin in
`corpus/lessons/round-54.md`, the wave specs and the registry.

## Witness — this seat wrote only its w2 report and receipts

- Writes by this seat: only `.ufo/waves/round-54/w2/T54W2Sent04.md` and
  `.ufo/waves/round-54/w2/T54W2Sent04-receipts/**`.
- Every git mutation ran with `-C "$TMP/cloneN/lane"` after
  `git rev-parse --show-toplevel` printed that clone; `git clone --shared` only reads the lane.
- Lane reads only: `git show`, `git ls-tree`, `git log`, `git rev-list`, `git cat-file`,
  `git diff --quiet|--stat`, `git rev-parse`, `git merge-base --is-ancestor`.
- HEAD moved under me mid-seat (`097985c` → `8da3539` → `4e2de73`, the L1's wave-1 correction and
  amendment-3 commits); the predicates were re-run at `4e2de73` and are reported separately from the
  earlier `097985c` run.
- Two tracked lane files were modified by concurrent work while this seat ran:
  `.ufo/evidence/round-21/coldread/ledger.json` (mtime 12:07:12) and
  `.ufo/evidence/round-54/integrate/binder.py` (mtime 12:06:22). They are not this seat's writes: no
  command here names either path for writing, and the diffs carry no `T54W2Sent04` reference. The
  ledger diff adds entries whose `read_rev` is `99c3bc88…` (the C1 reads) and the binder diff makes
  `WAVE_DIRS` scan `w1` and `w2` — [INFERENCE] concurrent L1/integrator work, not this seat.

## Tooling

None installed or upgraded (no `uv tool`, `npx`, pacman or binary fetch). Tools used: bash, git,
python3, coreutils/sha256sum, find.
