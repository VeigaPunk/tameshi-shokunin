# T48A2ExecC1Selftest — both frozen counter selftests from the CONTENT tree vs the committed receipts

seat: T48A2ExecC1Selftest (executor, leaf) · round 48 / a2w1 / hyaku run 8 attempt 2
item: run `--selftest` of `.ufo/evidence/round-48/calibration/measure.py` and
`.ufo/evidence/round-48/freshness/measure.py` from a `git clone -q --shared` of the lane at CONTENT
`c7586b9a10effc63b4bd327f976edc094c1bdc17`, `TMPDIR` inside scratch, and compare stdout + exit
byte-for-byte against `.ufo/evidence/round-48/selftest/{c1,c2}-r48-selftest.{stdout,exit}`; any
difference is a finding, the diff pasted.
milestone: counter selftests vs committed receipts · judged axes: calibration (C1), freshness (C2)
scratch: `/fast/scratch/hyaku/tameshi-r48/T48A2ExecC1Selftest/` (deleted before this report was returned)

**Bottom line.** C2 reproduces byte-for-byte, three ways (receipt, run 1, run 2) — exit, stdout, stderr.
C1 does **not**: 71 of its 78 stdout lines differ from the receipt, and the difference is of two kinds —
**F1** fixture commit shas (inherent; maskable; present in every run) and **F2** a live-fleet field,
`sibling_moves`, which made run 2 differ from the receipt *and from run 1* after masking (one line).
Both tallies and both exits are identical to the receipts (`76/0` + `VERDICT: PASS`, `43/0`, `0`), so
neither finding is a verdict on C1 or C2, and neither contradicts `freeze-2.json`. Both findings are
about what a committed selftest receipt can be used as: C2's is a byte target; C1's is one-execution
evidence.

## 1. Pins verified before running (content rev clone)

Clone `$S/lane` at `c7586b9a10effc63b4bd327f976edc094c1bdc17` (detached; `rev-parse HEAD` re-checked after
every run, unchanged). Counter bytes identical to `freeze-2.json`, to the freeze commit `755298415f8c` and
to the live worktree (`git rev-parse <rev>:<path>` / `git hash-object` agree):

| file | blob (all three revs) | sha256 | == freeze-2 |
|---|---|---|---|
| `.ufo/evidence/round-48/calibration/measure.py` | `7cb3ebb0d5cc…` | `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` | yes |
| `.ufo/evidence/round-48/freshness/measure.py` | `dd3ad9dfdd44…` | `faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f` | yes |

The four receipts are tracked at CONTENT (`git ls-tree c7586b9 .ufo/evidence/round-48/selftest/` lists
exactly the four) and each is byte-identical to the lane worktree copy (`git show c7586b9:… | cmp -`), so
"the committed receipt" is unambiguous:

| receipt | bytes | lines | sha256 |
|---|---|---|---|
| `selftest/c1-r48-selftest.stdout` | 26111 | 78 | `3081b49c9434fcf0ca7765d54311bfb4003397349d0be0067d3d53983b82489c` |
| `selftest/c1-r48-selftest.exit` | 2 (`0\n`) | 1 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `selftest/c2-r48-selftest.stdout` | 1589 | 44 | `359f17e7e7452f6f5662ef951df0024c5cb61e7b3f8a1b83e650517d663ab11a` |
| `selftest/c2-r48-selftest.exit` | 2 (`0\n`) | 1 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |

## 2. Commands (exactly as run)

```sh
S=/fast/scratch/hyaku/tameshi-r48/T48A2ExecC1Selftest; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"
git -C "$S/lane" checkout -q c7586b9a10effc63b4bd327f976edc094c1bdc17
cd "$S/lane"
python3 .ufo/evidence/round-48/calibration/measure.py --selftest >"$S/c1out/stdout"  2>"$S/c1out/stderr";  echo $?   # 284 s
python3 .ufo/evidence/round-48/freshness/measure.py   --selftest >"$S/c2out/stdout"  2>"$S/c2out/stderr";  echo $?   #   8 s
# second execution of each, same clone, same TMPDIR (determinism control):
python3 .ufo/evidence/round-48/calibration/measure.py --selftest >"$S/c1out2/stdout" 2>"$S/c1out2/stderr"; echo $?   # 291 s
python3 .ufo/evidence/round-48/freshness/measure.py   --selftest >"$S/c2out2/stdout" 2>"$S/c2out2/stderr"; echo $?   #   4 s
cmp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/selftest/<receipt> "$S/<run>/stdout"
diff -u <receipt> "$S/c1out/stdout"
```

No counter was run in any other mode; nothing in the lane was written (`git -C "$S/lane" status --porcelain`
empty after every run); `disk-guard.sh status` read before the pass (`/fast` 603 G free, 25 % used).

## 3. Result table

| comparison | exit | stdout | stderr |
|---|---|---|---|
| C1 receipt vs run 1 | `0` vs `0\n` — **identical** | **differs**: 71 of 78 lines (below) | both 0 B |
| C1 receipt vs run 2 | `0` vs `0\n` — **identical** | **differs**: 71 lines, of which 1 survives masking (F2) | both 0 B |
| C1 run 1 vs run 2 | identical | differs on the same 71 lines; after masking, 1 line (F2) | both 0 B |
| C2 receipt vs run 1 | `0` vs `0\n` — **identical** | **byte-identical** (`cmp` clean) | both 0 B |
| C2 receipt vs run 2 | `0` vs `0\n` — **identical** | **byte-identical** | both 0 B |
| C2 run 1 vs run 2 | identical | **byte-identical** | both 0 B |

Tallies, all three C1 streams and both C2 streams: `C1_R48_SELFTEST: cases=76 failed=0` + `VERDICT: PASS`
(76 `PASS` / 0 `FAIL`, case-name set identical to the receipt's after `awk '{print $2}' | sort`);
`C2_R48_SELFTEST: cases=43 failed=0` (43 `SELFTEST …: PASS`, no `VERDICT` line by design — the C2 selftest
returns before the verdict printer). Nothing in either selftest failed on any execution.

Run sha256: C1 run 1 `d2572fbf305963e49dfd9b23899c5b40519937f699c70a3a2ca2194cf88e19e9`,
C1 run 2 `3ebc4d8fd92746c698affa7e40c97e1f288c21fcd5192ab69dc6cfacde0b0d22`,
C2 runs 1 and 2 `359f17e7…` (= the C2 receipt).

## 4. F1 (low — C1's stdout is not byte-reproducible: fixture commit shas)

71 line-pairs of the raw diff, at lines 2–70 and 72–73; lines 1, 71 (`T61_emit_rows_reparse`) and 74–78
(`T63`, `T64`, `T65`, tally, verdict) are identical. **Every differing line carries `base=<40 hex>` and
`rev=<40 hex>`, and nothing else differs**: 0 differing lines lack those fields, and masking both fields
makes the diff empty for run 1.

```sh
diff -u <receipt> "$S/c1out/stdout"        # 71 '<' + 71 '>' lines  (full copy: T48A2ExecC1Selftest.c1-receipt.diff)
sed -E 's/base=[0-9a-f]{40}/base=<sha>/g; s/rev=[0-9a-f]{40}/rev=<sha>/g' <receipt> > a
sed -E 's/base=[0-9a-f]{40}/base=<sha>/g; s/rev=[0-9a-f]{40}/rev=<sha>/g' "$S/c1out/stdout" > b
diff a b                                   # exit 0, 0 bytes
```

Representative pair (line 2, receipt then run 1 — every other differing line has this shape):

```
-PASS T02_value_mismatch got=C1_R48: … sibling_moves=0 base=0320ded58fb8f1d6f238d31b80f8f0a39a78046b rev=83e12beba1e7174a011588abb15bcde28e451ec9 C1_R48_PASS=false
+PASS T02_value_mismatch got=C1_R48: … sibling_moves=0 base=ec86d5c6aadea4b063235bbbe21d4ab55cb1a6f3 rev=212c337688855271a90f5507c6c0d90b6bdb1277 C1_R48_PASS=false
```
(`…` elides `self_pin=1 stmts_pin=1 statements=3 rounds=3 append_only=1 unpinned=0 total=1 mismatches=1
unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0`, identical
in both.)

Cause, named to file:line: the selftest builds a throwaway fixture repo per case and commits to it with
`git -c user.name=t -c user.email=t@t commit -qm base` (`.ufo/evidence/round-48/calibration/measure.py:943`)
and `… -qm rev` (`:970`) **without pinning `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE`**, then reads the hashes
back and prints them in the label (`:577`, `base=%s rev=%s …`). Committer time = wall clock ⇒ different sha
every execution, and the two fields are independent per case, so both differ.

What this means, precisely: `.ufo/evidence/round-48/selftest/c1-r48-selftest.stdout` is evidence of **one
execution**, not a byte target a later seat can reproduce. It still evidences the substance it was
committed for — `cases=76 failed=0`, `VERDICT: PASS`, the case inventory and every non-hash field — and it
agrees with `freeze-2.json`'s recorded claim (76/0). Nothing in the contract or in amendments 1–10 requires
selftest bytes to be stable (amendment 8 pins FROZEN_UNCHANGED over the counters, `statements.json`, the
contract and the C2 snapshots — not over selftest receipts), so F1 is a receipt-quality defect, not a
predicate miss. It is the round-48 confirmation of the pattern `T48W2RevSelftestReceipts.md` §4 F3 and w1
`T48ExecSelftestReceipts.md` D5 recorded for the round-47 C1 counter.

## 5. F2 (low–medium — `--selftest` is not hermetic: it samples live sibling-lane HEADs)

Run 2 differs from the receipt **after masking**: exactly one line, and it is not a fixture hash.

```diff
40c40
< PASS T27_undeclared_env_dependence got=C1_R48: … dep_mismatch=1 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=0 base=<sha> rev=<sha> C1_R48_PASS=false
---
> PASS T27_undeclared_env_dependence got=C1_R48: … dep_mismatch=1 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=1 base=<sha> rev=<sha> C1_R48_PASS=false
```

`SELFTEST` case outcome unaffected (T27 wants `dep_mismatch=1`; it passed, as did all 76). The field is the
amendment-5 disclosure counter, and the selftest computes it against the **live fleet**:

- `fleet_state()` (`.ufo/evidence/round-48/calibration/measure.py:371`) lists `FLEET=/home/vgpnk/Projects/shokunin`
  (`:85`) for `*-shokunin` directories and runs `git rev-parse HEAD` in each (`:384-387`);
- `measure()` appends one such state before each round and one after the last (`:470`) and derives
  `sibling_moves` from them (`:472`), printing it in the label (`:577`);
- the selftest substitutes a fake fleet **only for the three fixture cases** that pass `fleet=`
  (`:760`, `:762`, `:764` → `fake_fleet`, `:883`); the wiring is
  `ff = fleet_fn or (fleet_state if observe_fn is None else (lambda _l, _r: ('fake', 1, ())))` (`:432`), so
  the **31 real-fixture cases** (fixture `git init` + real profile runs, no `observe_fn`) read the live fleet
  4 times each — 31 of the receipt's 71 label lines carry a live field.

Causal chain, verified: run 2 covered 10:47:15–10:52:26 (`stdout` mtime 10:52:26, wall 290.75 s) and
`/home/vgpnk/Projects/shokunin/mori-shokunin` exported a new HEAD inside that window —
`git -C …/mori-shokunin reflog --date=iso`: `bae8656e HEAD@{2026-10-26 10:52:00 -0300}: export from jj`
(and `756d5b1a HEAD@{10:54:21}` after it). Run 1 (10:42:34–10:47:18) and the receipt's capture (07:18) both
fell after mori's previous move at `09:31:37`, so both printed `sibling_moves=0` on every real-fixture line.
Re-check now: `sibling_moves=1` appears exactly on line 40 and on line 52 in run 2 (line 52 is the
intended `T33e_sibling_move_is_disclosed_not_drift` fixture, present in the receipt too); the receipt has
`=1` only on line 52.

Consequence and blast radius: on any host where a sibling lane commits during a 284–291 s selftest run, the
C1 selftest stdout changes non-deterministically, in a field the contract does not freeze. It cannot flip a
verdict — `sibling_moves` is disclosure, not drift (amendment 5), and `fleet_drift` stayed 0 on that line —
but it means the C1 receipt is not reproducible even after masking fixture shas, and a future seat
comparing bytes on a busy fleet will see a difference it cannot attribute from the receipt alone. This is
the only difference this run found that is not F1's fixture-hash churn, and it is the reason the item's
byte-comparison cannot be turned into a green/red gate as written.

## 6. C2 — byte-identical, no finding

`python3 .ufo/evidence/round-48/freshness/measure.py --selftest` printed 1589 bytes, 44 lines, exit 0, empty
stderr, on two independent executions, and `cmp` against
`.ufo/evidence/round-48/selftest/c2-r48-selftest.stdout` is clean for both; run 1 and run 2 are also
identical to each other. The 43 case lines are `SELFTEST <n>_<name>: PASS`, the tally
`C2_R48_SELFTEST: cases=43 failed=0` matches `freeze-2.json`, and no fixture path, hash, temp dir or fleet
field appears in the output, which is why it is stable. Its scratch lives in
`tempfile.mkdtemp(prefix='c2-r48-selftest-'` (`:662`) under my `TMPDIR` and is removed in `finally`
(`:845`) — after both runs, `ls -d "$S"/c2-r48-*` = 0 entries.

## 7. Hygiene observations (measured, not assumed)

- `TMPDIR` is honoured by both counters: `scratch_root()` refuses a scratch root under `/tmp`
  (`measure.py:106-116`), and `/tmp` gained 0 entries during my 665 s of selftest time
  (`find /tmp -maxdepth 1 -newermt '-40 minutes'` = 0 while run 2 was in flight).
- No leftover scratch: after both runs `ls -d "$S"/c1-r48-*` = 0 and `"$S"/c2-r48-*` = 0 — each case's
  `mkdtemp(prefix='c1-r48-', dir=root)` (`:842`) is `finally: shutil.rmtree`'d (`:847`). This is unlike the
  round-47 `run-controls.py` leak (`T48W2RevSelftestReceipts.md` §4 F4), which these two counters do not
  share.
- The clone stayed clean: `git -C "$S/lane" status --porcelain | wc -l` = 0 after all four runs, HEAD still
  `c7586b9…`.
- Scratch peak 156 MB (clone + per-case dirs), no ENOSPC; `/fast` 603 G free at the start of the pass.

## 8. Limits — what this does and does not show

- `--selftest` is fixture-only, no network, no real lane run. **Nothing here is a verdict on C1 or C2**, on
  the standing rows, on the C2 snapshots, or on any control; a probe is never a verdict.
- I did not re-verify the frozen counters' semantics, the 22 statements, the four superseded rows or the
  `C2-QUOTE` lines; other seats own those, and the counters were treated as opaque subjects under test.
- Byte comparison is only as strong as the receipt's own reproducibility. For C1 it is not reproducible
  (F1, F2); for C2 it is (three-way).
- I did not attempt to regenerate the receipt's exact fixture hashes (that would need the original
  committer timestamps). F1 therefore reports the mask-equality result, not a byte target.

## 9. Tooling record

No tool was installed, upgraded or fetched — `git`, `python3`, `bash`, `sed`, `awk`, `cmp`, `diff`, `find`,
`du` sufficed. No pacman transaction was attempted (host-wide pause respected). Scratch
`/fast/scratch/hyaku/tameshi-r48/T48A2ExecC1Selftest/` deleted before this report was returned.

## 10. Files written by this seat

- `.ufo/waves/round-48/a2w1/T48A2ExecC1Selftest.md` (this report)
- `.ufo/waves/round-48/a2w1/T48A2ExecC1Selftest.c1-receipt.diff` (raw `diff` of C1 run 1 vs the receipt,
  146 lines: 71 `-`/`+` pairs, all `base=`/`rev=` only)
- `.ufo/waves/round-48/a2w1/T48A2ExecC1Selftest.c1-run2-masked.diff` (the 4-line masked diff of C1 run 2
  vs the receipt — the complete F2 evidence)

Nothing else in the lane was written; `corpus/`, `tools/`, `SCORECARD.md` untouched.
