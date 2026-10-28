# T55W3RevGateReady — is the deciding run ready at the freeze `133b2ce`?

**Verdict: NO — the deciding run would refuse today, on four independent gates.** Nothing here
needs a judgement call: every check below is a read-only replay of `deciding-run.sh`'s own gate
lines against the committed bytes. Receipts:
`.ufo/waves/round-55/w2/T55W3RevGateReady-receipts/` (`gate-mirror.txt`,
`frozen-list-and-manifest.txt`, `prereq-and-census.txt`, `control-receipt-provenance.txt`,
`before-receipts-by-rev.txt`). No lane production file, frozen file or wave spec was touched; no
deciding invocation was run (`deciding_invocations: 1`).

## The five asked checks

| # | Check | Result |
|---|---|---|
| 1 | both control receipts exist as non-empty blobs at the freeze | **FAIL** — no control receipt has *ever* been committed |
| 2 | they carry `CONTROLS_A/B: n/n as pre-registered` | **FAIL** — the only surviving text is one `CTL CTL_0_c1` line |
| 3 | their `.exit` files read 0 | **FAIL** — no `.exit` file exists anywhere |
| 4 | `freeze.json` re-derives | **PASS** — 7/7 hashes at `133b2ce` (and 7/7 at `4f7a704`) |
| 5 | `deciding-run.sh`'s `FROZEN` list equals the contract's `frozen_paths` | **FAIL at the freeze** (7 vs 8); passes only on post-freeze bytes |

## 1–3. Control receipts: absent from git, and the one file on disk cannot open anything

```
$ git ls-tree -r -l 133b2ce -- .ufo/evidence/round-55/control/        # (also at 9cf0146 and 4f7a704)
(no output)
$ git log --all --oneline -- .ufo/evidence/round-55/control/
(no output)                                            # never committed on any ref
$ git status --porcelain -- .ufo/evidence/round-55/control/
?? .ufo/evidence/round-55/control/
$ stat -c '%n size=%s mtime=%y' .ufo/evidence/round-55/control/controls-a.stdout
.ufo/evidence/round-55/control/controls-a.stdout size=120 mtime=2026-10-28 14:40:00.954262630 -0300
$ cat .ufo/evidence/round-55/control/controls-a.stdout
CTL CTL_0_c1 C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
$ grep -c '^CONTROLS_A: [0-9]*/[0-9]* as pre-registered' .ufo/evidence/round-55/control/controls-a.stdout
0            # rc=1
```

Replaying the gate line for line over three candidate REVs:

```
$ for f in controls-a.stdout controls-a.exit controls-b.stdout controls-b.exit; do git cat-file -e "$REV:.ufo/evidence/round-55/control/$f"; done
-- REV=9cf0146 (C0)     ABSENT ×4 -> DECIDING_REFUSED control-receipt-missing
-- REV=133b2ce (freeze) ABSENT ×4 -> DECIDING_REFUSED control-receipt-missing
-- REV=4f7a704 (HEAD)   ABSENT ×4 -> DECIDING_REFUSED control-receipt-missing
```

So `deciding-run.sh` stops at its first control loop (`git cat-file -e "$REV:$f"`), before the
`controls-a-verdict-missing` / `controls-b-verdict-missing` greps, which would also fail: the only
file on disk carries 1 of the 5 pre-registered phase-A controls (`CTL_0_c1`; missing `CTL_0_c2`,
`CTL_SKIP_c1`, `CTL_SKIP_c2`, `CTL_FAB_c1`) and no verdict line. Its mtime is **14:40:00**, i.e.
eight seconds after amendment 9 landed (`4f7a704` 14:39:49) — a partial phase-A run against
post-freeze bytes, not the phase-A set the contract says was decided on ("the phase-A set decided
on is the one at this freeze", amendment 8).

**Missing to open this gate:** a complete `controls.sh a LANE 133b2ce 0a2010ac OUTDIR` run
(`CONTROLS_A: 5/5 as pre-registered`, exit 0), both stdout and `.exit` committed at REV in a
commit that descends from FREEZE; likewise `controls.sh b` at the final content revision for
`CONTROLS_B`. **Phase B cannot exist yet and correctly does not**: it scores `CTL_POS_c1/c2` and
`CTL_BREAK_c2` *at the revision it certifies* (the final content revision, per `controls.sh`'s own
header), so it is by construction a post-wave-1 artefact. Its absence is not a defect; the
absence of phase A is.

## 4. `freeze.json` re-derives — PASS

```
$ python3  # re-hash every manifest entry from the bytes at FREEZE, as deciding-run's gate 0 does
OK   .ufo/evidence/round-55/c1/measure.py          5e8f50d1815309e8
OK   .ufo/evidence/round-55/c1/staged-at-freeze.txt 921ad4196b76a43a
OK   .ufo/evidence/round-55/c2/measure.py          0458f632087f665f
OK   .ufo/evidence/round-55/contract.json          fe5f90501a02cf2a
OK   .ufo/evidence/round-55/controls.sh            7c0cacb56c679155
OK   .ufo/evidence/round-55/deciding-run.sh        af11d7551d8af1c7
OK   .ufo/evidence/round-55/no-harm.sh             d93469db5a55632c
FREEZE_INTEGRITY: OK files=7 amendments=8
```

The manifest is also internally consistent: it covers all 8 `contract.frozen_paths` entries except
`freeze.json` itself, as its own `note` declares, and its amendment count (8) equals the contract's
at that rev. Re-run at HEAD it is still OK (`7/7`, `amendments=9`, `deciding-run.sh 28d4fa8aaacf`).

## 5. `FROZEN` list vs the contract's `frozen_paths` — FAIL at the freeze, PASS only after it

```
$ git show 133b2ce:.ufo/evidence/round-55/deciding-run.sh | grep -o 'FROZEN="[^"]*"'
FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py $E/c2/measure.py $E/no-harm.sh $E/deciding-run.sh $E/controls.sh"

$ git show 133b2ce:.ufo/evidence/round-55/contract.json | jq -r '.frozen_paths[]'   # 8 entries, incl.
.ufo/evidence/round-55/c1/staged-at-freeze.txt                                       # <-- not in FROZEN

$ git show 4f7a704:.ufo/evidence/round-55/deciding-run.sh | grep -o 'FROZEN="[^"]*"'
FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py $E/c1/staged-at-freeze.txt $E/c2/measure.py $E/no-harm.sh $E/deciding-run.sh $E/controls.sh"
```

Set comparison, expanded to absolute paths:

```
$ # freeze 133b2ce
SET_EQUAL=0 missing_from_FROZEN: .ufo/evidence/round-55/c1/staged-at-freeze.txt
$ # HEAD 4f7a704
SET_EQUAL=1 entries=8
```

7 vs 8 at the pinned freeze; 8 vs 8 only at `4f7a704` (amendment 9). The freeze manifest pins
`deciding-run.sh` at `af11d755…`, while the fixed script's bytes hash to `28d4fa8a…`, so **the fix
is unreachable at the pinned freeze**: using the fixed script makes gate 0 print
`FREEZE_MISMATCH .ufo/evidence/round-55/deciding-run.sh`, and using the frozen script keeps the
staged-count receipt rewritable. Amendment 9 has no freeze of its own.

## New blocker the item did not ask about: the freeze ordering breaks `FROZEN_UNCHANGED`

`133b2ce`'s parent is **C0 `9cf0146`** — the freeze was minted *after* the content commit — and the
frozen bytes were then edited twice more (`c31cdd9` F4, `4f7a704` F5):

```
$ git merge-base --is-ancestor 133b2ce 9cf0146 && echo yes || echo no
no                                    # 9cf0146 IS an ancestor of 133b2ce
$ git diff --stat 133b2ce 4f7a704 -- $FROZEN   # both the 7-item and the 8-item list
 .ufo/evidence/round-55/c1/measure.py   | 14 +++++++++++---
 .ufo/evidence/round-55/contract.json   |  8 ++++++--
 .ufo/evidence/round-55/deciding-run.sh |  2 +-
 .ufo/evidence/round-55/freeze.json     | 12 ++++++++----
```

`deciding-run.sh` sets `rc=1` whenever that diff is not quiet, so **any REV at or after F5 fails the
deciding run at `FROZEN_UNCHANGED=0`**, after burning the single invocation. The only self-consistent
freeze is `4f7a704` (its `freeze.json` re-derives at HEAD, verified above); the pointer recorded in
`.ufo/evidence/round-55/integrate/resolutions.json` (`"freeze pointer moved to 133b2ce6"`) is stale.

## 6. Other prerequisites (all currently green, one red)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
… (16 per-row W04/W01 warnings) …
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
census_exit=0
$ grep -c '^| S[0-9]' corpus/SOURCES.md
140

precheck script at 133b2ce / at HEAD : present / present   (.ufo/evidence/round-48/quality/coldread-precheck.sh)
no_harm_monitors                     : 15  (matches the script's `= 15` assertion)
second-invocation markers            : 0   (no c1.start / c2.start anywhere)
after/ dir                           : none

$ git status --porcelain | wc -l
231                     # 52 tracked modifications/deletions + untracked wave reports
```

The last one is a blocker: the gate runs
`git status --porcelain` and only excludes `OUTDIR`, so it prints `DECIDING_REFUSED dirty-tree` with
231 entries. Every wave artefact (all three waves' reports and receipts) must be committed, and the
tree clean, before the deciding invocation.

## What is still missing (ordered)

1. **Mint a freeze that contains its own repairs.** Re-freeze at `4f7a704` or later (manifest
   already re-derives there), or amend `freeze.json` at `133b2ce` — otherwise the run cannot have
   both a `FROZEN` list equal to the contract's and a passing `FREEZE_INTEGRITY`.
2. **Run phase A to completion at the freeze bytes** and commit `controls-a.stdout` +
   `controls-a.exit` (`CONTROLS_A: 5/5 as pre-registered`, exit 0). Delete or supersede the
   partial 14:40 file — it is evidence of a run that never finished and cannot be cited.
3. **Commit the whole wave** so the deciding gate sees a clean tree.
4. **Then** run phase B at the final content revision (`CONTROLS_B: 3/3`), commit its two receipts,
   and only then `deciding-run.sh`. Phase B legitimately does not exist yet.

## Residual risk (not blockers)

- **`before/` is outside the frozen set.** Neither before receipt is in `FROZEN` (`grep -c 'before/'`
  on the script = 0), yet both changed after the freeze: `before/c1.stdout` (+20 lines, F5's
  re-measure) and `before/c2.stdout` (3 lines, total `21 -> 20`). A REV can therefore rewrite the
  claim's *premise* evidence and still print `FROZEN_UNCHANGED=1`. The freeze-pinned contract's C2
  `before` value (`total=21`) agrees with the freeze-time receipt and disagrees with the HEAD
  receipt (`total=20`); F4's correction is real but lives outside the freeze.
- **The verdict greps read the working tree** (`"$LANE/$E/control/controls-a.stdout"`), not the REV
  blob, and run before the clean-tree check. A dirty receipt could satisfy the grep while the blob
  at REV has no verdict — but the later dirty-tree gate refuses that state, so it is not exploitable
  today; it becomes exploitable only if the receipt path ever lands in the `OUTDIR` exclusion.
- The wave assignment states the freeze carries **7 amendments** and that both control receipts
  "exist as non-empty blobs at the freeze". Neither is true of the bytes: `contract.json` and
  `freeze.json` at `133b2ce` both carry **8** amendments, and no control receipt exists at any rev.
  Read the freeze from `.ufo/evidence/round-55/{contract,freeze}.json`, not from the brief.
