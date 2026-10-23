# ReviewRepairs — round 32 (reviewer seat)

Seat: `TameshiR32.ReviewRepairs` (reviewer). Lane: `tameshi-shokunin`. Review anchor: lane commit
`24a5a5bb598ae919546715267d76f814efaf8912`. Target: routed repairs of `corpus/lessons/round-31-verifier-spotcheck.md`
items 1, 2, 4 (item 3 is C1), the receipt checker, the wave-1/2 reports, and the lane census v2.

Work was done only in `/fast/scratch/hyaku/tameshi-r32-seats/ReviewRepairs/` (sandbox clone made with
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks <lane> clone`, checked out at
24a5a5bb; worktree clean). No git write or jj command ran in the lane/fleet repo; production files were
read-only. No tool installed or upgraded (stock `git`, `python3` 3.14.8, `bash`); nothing to record under
the tooling directive.

## Verdicts per item

| Item | Artifact at 24a5a5bb | Verdict |
|---|---|---|
| 1 (predicate identity) | `.ufo/evidence/round-32/repair/c1-r31-measure-v2.py` | **PASS** — exists; diff vs frozen `.ufo/evidence/round-31/c1-measure.py` is exactly the two intended condition changes plus a docstring (3 hunks, 11 insertions / 3 deletions, no other byte differs); `.ufo/evidence/round-32/contract.json:40` quotes the exact selector condition. Control caveat carried below (CtlHeaderV2) |
| 2 (append-only byte prefix) | same file | **PASS** — condition is now a raw-byte `git show REV:SCORECARD.md` prefix with both `git show` returncodes required 0 |
| 4 (base monitor receipt) | `repair/c1monitor-at-r31-base-36c1d393.{stdout,stderr,exit}` | **PASS** — exists, pins rev `36c1d3933f680125aeefc447f07db0f03004901a`, `covered=64/64 restraint=8 box3_mismatch=0 depth_score=9`, exit 0, stderr empty |
| 4 (command D exit receipts) | `repair/commandD-at-r31-67c0e013.{stdout,stderr,exit}`, `repair/commandD-at-r31-final-08125328.{stdout,stderr,exit}` | **PASS** — both exist; `recorded_cases=9 depth_score=9`, exit 0, stderr empty |
| receipt checker | `.ufo/evidence/round-32/receipt-check.py` | **PASS on exercised paths** — `--selftest` 6/6 exit 0; scan of `.ufo/evidence/round-32` `missing_exit=0 files=8` exit 0. Two inherited findings carried below |
| wave-1/2 reports | `w1/RunCounterV2.md`, `w1/CtlHeaderV2.md`, `w1/ReviewRepairReceipts.md`, `w2/ReviewReceiptCheck.md` | **EXIST** at 24a5a5bb and their content is consistent with the artifacts |
| census v2 | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` at 24a5a5bb | **CLEAN**, exit 0, **A rows = 96** |

## Evidence (exact commands / observed output)

All paths relative to the sandbox clone at 24a5a5bb.

**Presence.** `git ls-tree -r --name-only 24a5a5bb .ufo/evidence/round-32 .ufo/waves/round-32` lists all of:
`round-32/repair/c1-r31-measure-v2.py`, `repair/c1monitor-at-r31-base-36c1d393.{stdout,stderr,exit}`,
`repair/commandD-at-r31-67c0e013.{stdout,stderr,exit}`, `repair/commandD-at-r31-final-08125328.{stdout,stderr,exit}`,
`round-32/receipt-check.py`, `w1/RunCounterV2.md`, `w1/CtlHeaderV2.md`, `w1/ReviewRepairReceipts.md`,
`w2/ReviewReceiptCheck.md`.

**Hashes** (`sha256sum` on the worktree at 24a5a5bb):

```
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  .ufo/evidence/round-31/c1-measure.py
e49b00de184ecb4c3a94b49b9d89a13650b13bc8ca6cd57c1a5f68c971f713b7  .ufo/evidence/round-32/repair/c1-r31-measure-v2.py
3a82410750846f8be3a3493f61f0a7ea901a06b89a007a4e1f21e40cddf88a44  .ufo/evidence/round-32/receipt-check.py
```

v1 hash equals `round-31/contract.json` `counter_sha256` (same value at 24a5a5bb). v2 hash equals the blob
RunCounterV2 pinned at the round-32 freeze commit `c318149` (that seat's evidence) — confirmed here as committed
content at 24a5a5bb.

**Diff (item 1+2).** `git show 24a5a5bb:.ufo/evidence/round-31/c1-measure.py` vs
`git show 24a5a5bb:.ufo/evidence/round-32/repair/c1-r31-measure-v2.py`, `diff -u`:

```
1 file changed, 11 insertions(+), 3 deletions(-)
-        elif len(header) > 1 and header[1].startswith('Score'):
+        elif len(header) > 1 and header[1] == 'Score (0–10)':
-    append_only = int(rev_sc.stdout.startswith(base_sc.stdout))
+    base_b = subprocess.run(['git', '-C', a.lane, 'show', a.base + ':SCORECARD.md'], capture_output=True, env=env())
+    rev_b = subprocess.run(['git', '-C', a.lane, 'show', rev + ':SCORECARD.md'], capture_output=True, env=env())
+    append_only = int(base_b.returncode == 0 and rev_b.returncode == 0 and rev_b.stdout.startswith(base_b.stdout))
```

plus a docstring paragraph stating exactly these two changes and that the output label stays `C1_R31` (repair
instrument, not a round-32 claim counter). No other byte differs. Dash bytes: the v2 condition, `contract.json:40`,
the lesson's routed item 1, and every committed `SCORECARD.md` axis header (lines 64, 1488, 1534) all use
U+2013 EN DASH (`e2 80 93`); the frozen round-31 contract prose writes the ASCII hyphen form — on this data both
readings select the same rows (RunCounterV2 §4).

**Monitor receipt (item 4).** `repair/c1monitor-at-r31-base-36c1d393.stdout`:

```
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=36c1d3933f680125aeefc447f07db0f03004901a
```

exit 0, stderr 0 B. This is the base reading the round-31 report stated but never receipted; it pins rev
36c1d393 (round-31 base).

**Command D receipts (item 4).** Both `repair/commandD-at-r31-67c0e013.stdout` and
`repair/commandD-at-r31-final-08125328.stdout`:

```
recorded_cases=9 depth_score=9
```

exit 0, stderr 0 B, at round-31 measurement revision `67c0e013…` and final head `08125328…`. The round-31
`after/commandD-at-final.stdout` still has no `.exit` sibling; the contract explicitly does not reconstruct it
(“its exit was not recorded and is not reconstructed”, `contract.json:42`) — no silent backdate.

**Receipt checker.** `timeout 300 python3 .ufo/evidence/round-32/receipt-check.py --selftest` →

```
case empty-tree             ok
case complete-pair          ok
case missing-exit           ok
case sibling-is-same-dir    ok
case non-stdout-ignored     ok
case multiple-missing       ok
RECEIPT_CHECK_SELFTEST: cases=6 failed=0
exit=0
```

`timeout 300 python3 .ufo/evidence/round-32/receipt-check.py .ufo/evidence/round-32` →

```
RECEIPT_CHECK: missing_exit=0 files=8
exit=0
```

**Census v2.** `timeout 300 bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` (from clone root at
24a5a5bb):

```
== A rows
96
== A malformed (must be 0)
0
== A tiers
A=87 B=7 C=2
== A status
mined=68 queued=22 rejected=6
== A dup ids (must print nothing)
== A enum/tier-inflation (must print nothing)
== A mined used-by missing (must print nothing)
== B1 strict id-cite (informational)
no-id-cite: S031 … (25 lines)
== B2 id-or-path cite (must print nothing)
== VERDICT
SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)
exit=0
```

Verdict CLEAN, exit 0; **A-row count 96** (A=87, B=7, C=2; mined=68, queued=22, rejected=6; malformed 0;
dup ids 0; mined used-by missing 0; B2 id-or-path violations 0; B1 informational 25 no-id-cite).

## Findings by severity

1. **[MEDIUM] The item-1 control did not establish the expected all-reject v2 pattern.** Wave-1 seat
   CtlHeaderV2 (committed report) shows: Shape A (appended `Score` cell) v2 FAIL is confounded — its sole
   mismatch is a regression-leg result, not an axis row; Shape B (appended `Score (0-10)`, ASCII hyphen)
   **SURVIVED v2** (PASS); Shape C and D are killed by the byte-prefix check; pristine and restored controls
   pass both counters. Root cause stated there: v2 ignores unrecognized-header tables, and an already-eligible
   canonical axis table exists at head, so a malformed appended table is never selected. The repaired counter is
   faithful to the routed text; the defect is in the control design or its expected result. Smallest correction:
   fix the control (e.g. make the post-base canonical table ineligible before appending), do not broaden v2 into
   rejecting noncanonical tables.
2. **[LOW] receipt-check fail-open on unreadable trees contradicts its documented exit 2** (w2
   ReviewReceiptCheck finding 2): `os.walk` silently yields nothing → `files=0 missing=0`, exit 0, on an
   unreadable root/subdir. Smallest correction: root probe + `OSError` handling + two selftest fixtures.
3. **[INFO] Round-31 scan lists four legacy `ctl/bind-v5-*.stdout` captures** beyond the mined command-D gap
   (w2 finding 1); the lesson should disclose them or the checker gain a scope/exclusion mechanism. The round-32
   scan under review is clean (0/8), so this does not affect the round-32 evidence.
4. **[INFO] Output label stays `C1_R31`** on the v2 repair instrument (intentional, documented in its docstring
   and by RunCounterV2); if round 32 wants a claim label for the repaired instrument, that is an L1 decision,
   not a defect.

## Residual risk / verification gaps

- I verified committed bytes at 24a5a5bb (ls-tree, `git show` diffs, hashes, full reads, fresh execution of
  receipt-check and census). The ~9-minute counter runs (v1/v2 at base and head) and the monitor/command-D
  reruns were not re-executed by me; they are attested by wave-1 seats with receipts in their scratch
  (RunCounterV2: v1 vs v2 stdout byte-identical at both revisions, verdicts equal; ReviewRepairReceipts: all
  seven receipts rerun byte-identical, exits equal).
- En-dash vs ASCII-hyphen prose drift between the frozen round-31 contract and the code/SCORECARD.md bytes is
  recorded (RunCounterV2 §4); it is inert on this data.
