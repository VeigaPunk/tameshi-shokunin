# ReviewAttempt1-7 — re-verification of attempt-1 landed commits (round-30 wave A)

Seat: TameshiR30A2.ReviewAttempt1-7. 2026-10-23. Item: re-verify dcdf2d08, e59728df,
8a8d2540; check counter sha256 pins; re-run c1-measure-v3.py at base rev and compare
line by line with c1v3-at-base.stdout; check commit order.

## Verdict

**Every receipt reproduces. No counter pin fails. Commit order is correct.** One LOW,
record-keeping-only finding (document-clock vs git-committer-clock skew); it does not
affect any pin, any receipt content, or the commit-graph order.

## Axes

1. Counter integrity — do the frozen sha256 pins match the landed bytes?
2. Reproduction fidelity — does the v3 base receipt reproduce bit-for-bit?
3. Ordering/provenance — contract before amendment 1 before controls before amendment 2?

## 1. Counter sha256 pins — ALL MATCH

Clone: `S=/fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.ReviewAttempt1-7/clone`,
detached at f09d3425258403a51422c9959e25340807982947. For each doc I read the pin from
the blob **at its landing commit**, hashed the counter blob at that commit and at tip
(`git show`), and compared full doc text landing-vs-tip.

| Landing commit | Doc (pin source) | Counter file | Pin | counter@landing | counter@tip |
|---|---|---|---|---|---|
| dcdf2d08 | contract.json (claims[0].counter_sha256) | c1-measure.py | cecac1b1…02c87 | MATCH | MATCH |
| e59728df | contract-amendment-1.json | c1-measure-v2.py | 5ed4e663…0c8719 | MATCH | MATCH |
| 8a8d2540 | contract-amendment-2.json | c1-measure-v3.py | 3188d4f8…6144f8 | MATCH | MATCH |
| f09d3425 | contract-amendment-3.json | c1-measure-v4.py | cccae0bd…30a5f07 | MATCH | MATCH |

Full hashes observed (counter@landing == counter@tip == pin in all four rows):
`cecac1b14df607dbfcaad091b47322b1e50c5b60742026d026370bc758202c87`,
`5ed4e663ff16556d0bfef68a9fc1e3cf820ab8bc2b620169e800da914f0c8719`,
`3188d4f80e928d1d8b45734ac8f6b253b799c6755abfafc3090b7aa9e76144f8`,
`cccae0bd984a7c67c22d83a1e67d19e3ebc76c015094106a1370d330030a5f07`.
All four docs are full-text stable since landing (landing blob == tip blob).

## 2. v3 reproduction at base — REPRODUCES

Command (per item, run against my clone only):

```
timeout 1500 python3 .ufo/evidence/round-30/c1-measure-v3.py \
  --repo $S/clone --rev 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 --jobs 4
```

Observed: exit=1, wall 104.8s, empty stderr. Unified diff vs
`.ufo/evidence/round-30/c1v3-at-base.stdout`: **all 48 content lines identical** —
the pristine row, 13 family rows (D1–D9, A1–A4), 4 rewrite rows (E1–E4), 12 held-out
rows (H01–H12), 4 held-out equiv rows (HE1–HE4), 8 insert rows (I01–I08), 4 insert
equiv rows (IE1–IE4), the summary
`C1_R30: rev=9ed6db84… pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4 insert_killed=0/8 insert_equiv=4/4`,
and `PREDICATE: C1_R30_PASS=false`.

The receipt's 49th line, `exit=1`, is not emitted by the counter
(`grep 'exit=|PREDICATE' c1-measure-v3.py` shows only ROW/summary/PREDICATE prints;
exit codes are `return`ed, v3 script lines 375/379/300). It is recorder-appended
metadata, and my observed process exit code is 1 — matching. Not a mismatch.

## 3. Commit order — CORRECT

`git log --format="%h %cI %s" 9ed6db840…f09d342525` (read-only, GIT_OPTIONAL_LOCKS=0)
shows exactly four commits, in order:

```
dcdf2d0 2026-10-23T01:56:43-03:00 freeze C1 contract and counter … with base receipts
e59728d 2026-10-23T01:59:47-03:00 C1 counter v2 … before any control or data
8a8d254 2026-10-23T02:12:39-03:00 C1 counter v3 after control CtlK7Keyed met v2 … control receipts so far; reachability witness
f09d342 2026-10-23T02:37:05-03:00 C1 counter v4 … after CtlK8NoRun met v3 … control receipts
```

Contract (dcdf2d0) < amendment 1 (e59728d) < controls+amendment 2 (8a8d254) < amendment
3 (f09d342). First-appearance check (`git log --diff-filter=A`): c1-at-base.stdout in
dcdf2d0; c1v2-at-base.stdout and contract-amendment-1.json in e59728d; c1v3-at-base.stdout,
ctl/CtlK7Keyed.stdout, ctl/CtlK7Keyed-v3-rescore-by-L1.stdout, witness/c1v3-at-witness-1fed832d.stdout
and contract-amendment-2.json all in 8a8d254; ctl/CtlK8NoRun.stdout and
contract-amendment-3.json in f09d342. Author dates order identically to committer dates.

## Findings by severity

**LOW (record-keeping, no effect on pins/receipts/order).** Document clocks and the git
committer clock disagree by 13s–7m21s. contract.json declares `frozen_at_utc`
2026-10-23T04:58Z but landed at committer time 04:56:43Z (77s earlier); amendment-1
declares 05:00Z, landed 04:59:47Z (13s earlier); amendment-2 declares `written_at_utc`
05:20Z but landed at 05:12:39Z (7m21s earlier); amendment-3 is consistent (05:37Z vs
05:37:05Z). Under a strict git-clock reading amendment-2's text would predate its own
commit, so the two clocks are simply offset; the substantive order (CtlK7Keyed scored →
amendment 2 written → both landed together) is what the amendment's reason text and the
co-landing in 8a8d254 show. Note the controls co-land **with** amendment 2 in one commit
rather than in a strictly earlier commit — the "before" is attested by the amendment
text and declared times, not by an earlier commit.

## Residual risk and verification gaps

- Sealed-set pins (amendment 3 `sealed_sha256` 44116804…, `sealed_block_sha256`
  e163133c…) **not checked**: the sealed set lives under /fast/scratch/hyaku/tameshi-r30a2,
  which this seat is forbidden to open; v4/c1-sealed.json is not present at tip. Out of scope by bounds.
- Did not re-run the v1/v2 counters at base (item names only the v3 run); their receipts
  were verified only as landing-commit contents matching their pins' docs.
- Did not re-score any control seat (out of item).
- No `lsp` device is available in this session's tool inventory; all checks above are
  git-blob/hash and byte-diff evidence, which is the appropriate method for receipts.
- Bounds compliance: nothing under /fast/scratch/hyaku/tameshi-r30a2 opened; production
  repo touched only by read-only git with GIT_OPTIONAL_LOCKS=0; the v3 run executed
  against my own clone; no jj commands; no tool installs were needed (directive recorded: none performed).
