# ScoutC1DataWalk — r36 control-receipt baseline walk (C1, calibration)

Scope: locate the exact assertion carrying the unreachable scratch revision
`91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`, and re-run the old-hash reachability
command. Read-only; no lane edits.

## 1. The unreachable revision lives in two committed evidence assertions

The hash `91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` appears in the `rev=` field of
the two round-36 empty-panel control receipts — the only committed places the
r36 evidence itself asserts that revision:

- `.ufo/evidence/round-36/control/v1-at-emptypanel.stdout:8`
  `C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 … pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 … sealed_after_freeze=1 rev=91373d55557fe26c431e9e3dd9e8fa4a00d7b57f C1_R35_PASS=true`
  (`v1-at-emptypanel.exit` = `V1_EXIT=0`)
- `.ufo/evidence/round-36/control/v2-at-emptypanel.stdout:8`
  `C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 … pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 … sealed_after_freeze=1 rev=91373d55557fe26c431e9e3dd9e8fa4a00d7b57f C1_R36V2_PASS=false`
  (`v2-at-emptypanel.exit` = `V2_EXIT=1`)

Both runs were made in a throwaway scratch clone (`/tmp/tameshi-r36-ctl-2/lane`,
documented in `.ufo/waves/round-36/w1/ReviewC2Claim.md:113,141-142`); the mutant
commit (9 panel JSONs deleted off `b455001e`) never entered the lane object DB.

## 2. Self-assessment assertions that cite the pair (propagating the pointer)

- `LOG.md:1926-1928` — r36 entry presents the v1/v2 pair as the C2
  before-demonstration on "the same mutant" (receipt paths named, hash embedded
  only inside the receipts).
- `SCORECARD.md:1744` — r36 C2 row, before-column quotes both receipts including
  `C1_R35_PASS=true` / `C1_R36V2_PASS=false` (again via receipt paths).
- Retrospective disclosures/errata (all post-r36, already in the lane):
  `corpus/lessons/round-36-verifier-spotcheck.md:90` (non-author spot-check,
  status-neutral minor: "not reachable from the lane repo"),
  `SCORECARD.md:1780` (erratum `### Round 36 control-input erratum (round 37)` —
  explicitly states the `rev=91373d55…` input "is not an object in this lane"),
  `SCORECARD.md:1784` (mode erratum — receipts mislabeled `mode=deciding`),
  `SCORECARD.md:1786-1788` (control-pointer errata),
  `corpus/lessons/round-37.md:16` (`class: reference-drift`).

So the frozen "one live evidence/self-assessment mismatch" resolves to: the two
`.stdout` line-8 `rev=` assertions (plus the LOG/SCORECARD before-demonstration
prose that vouches for them) citing a revision the lane cannot resolve.

## 3. Old-hash reachability re-run (lane object DB)

```
$ git cat-file -t 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f
fatal: git cat-file: could not get object info        (exit 128)
$ git cat-file -e '91373d55557fe26c431e9e3dd9e8fa4a00d7b57f^{commit}'
fatal: Not a valid object name 91373d55…^{commit}     (exit 128)
```

Same failure the r37 counter keys on (`measure.py:89`,
`git cat-file -e OLD_MUTANT^{commit}`).

## 4. Frozen counting command at the contract before-rev

```
$ python3 .ufo/evidence/round-37/calibration/measure.py --lane . --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d
C1_R37: unresolved_control_inputs=1 old_mutant_resolves=0 correction=0 manifest_ok=0 receipts_ok=0 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R37_PASS=false   (exit 1)
```

Matches the frozen `before.expected` of exactly one live mismatch at `d9c496b`.

## 5. Observed lane state (context for orchestrator; not my repair)

HEAD is `e6185d5` and already contains the r37 repair commits (`7500239` supersede
unreachable control input, `7397981` mode labels, `32826f3` provenance/mode
records, `e6185d5` records). `.ufo/evidence/round-37/control/` holds
`empty-panel/manifest.json`, `replay-at-final{,-fixed,-control}.{stdout,stderr,exit}`,
and `replay-empty-panel.py`. At HEAD the counter prints
`unresolved_control_inputs=0 … correction=1 manifest_ok=1 receipts_ok=1 … C1_R37_PASS=true`
(exit 0). The kill-rule pair (1 at `d9c496b`, 0 at tip) is therefore already
satisfied on the committed lane — flagging in case wave scheduling assumed the
mismatch was still live.

Confidence: high on all items — every fact above is a committed file line or a
re-run command output quoted verbatim. Remaining unknowns: none within scope.
