# DraftLesson25Correction — append-only "## Correction (round 26)" block for `corpus/lessons/round-25.md`

Seat: TameshiR26.DraftLesson25Correction (scribe, leaf — no subagent dispatch).
Scope: draft one append-only correction block for the end of
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-25.md`,
recording what **amendment 3** added and that it (in `77302fa`) also preceded
the after-measurement. Nothing else.

Verdict: **the defect is real and the block below is the minimal append.**
`round-25.md` `## Claims` (lines 26–28) names only amendment 1 (`c9ff09f`) and
amendment 2 (`09dc114`), while amendment 3 exists as
`.ufo/evidence/round-25/contract-amendment-3.json` and landed in `77302fa`
— the very commit the lesson's `## After measurement` section (line 89) names
as the measured revision `77302fa8f79144d06c1d2e2d2898c44b459bda`. The block
below appends the missing fact and quotes the JSON verbatim. Earlier text is
not rewritten.

## 1. Observed facts (exact commands, observed output)

### 1.1 The lesson names amendments 1–2 only

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-25.md:26-28`
(read this session), verbatim:

```
Both were frozen in `.ufo/evidence/round-25/contract.json` (`2a97ec1`) before
the wave. Amendment 1 (`c9ff09f`) only made the C2 counter runnable from a
clone. Amendment 2 (`09dc114`, before any after measurement) only added
checks the wave showed were missing; see `contract-amendment-2.json`.
```

No mention of amendment 3 or `77302fa` in the `## Claims` section
(`grep -n "Amendment 3\|amendment 3" corpus/lessons/round-25.md` → no hit;
the only hits in `corpus/` are in `round-25-verifier-spotcheck.md`).

### 1.2 Amendment 3 exists and landed in 77302fa

```
$ GIT_OPTIONAL_LOCKS=0 git -C …/tameshi-shokunin log --oneline --all --source \
    -- .ufo/evidence/round-25/contract-amendment-3.json
489a98d	refs/jj/keep/489a98df53a23f30e0ef2ac5109f4e5592766293
77302fa	refs/jj/keep/77302fa8f79144d06c1d2e2d2898c44b459bda round-25: wave reports, dead-falsifier disposition, knowledge entry, S086/S087, QUALITY50, lesson, SCORECARD rows, amendment 3
```

`489a98d` is the pre-commit `jj` keep-snapshot of the same content; the
committed revision is `77302fa` (whose commit subject literally ends
"amendment 3").

The working-tree file is byte-identical to the blob at `77302fa`:

```
$ sha256sum .ufo/evidence/round-25/contract-amendment-3.json
2ad542d3c90c8795e28b6a657c141e71e8ccfd1ec87e15db12cb65e0c542c5f0  .ufo/evidence/round-25/contract-amendment-3.json
$ GIT_OPTIONAL_LOCKS=0 git show 77302fa:.ufo/evidence/round-25/contract-amendment-3.json | sha256sum
2ad542d3c90c8795e28b6a657c141e71e8ccfd1ec87e15db12cb65e0c542c5f0  -
$ GIT_OPTIONAL_LOCKS=0 git diff --stat 77302fa -- .ufo/evidence/round-25/contract-amendment-3.json
(no output)
```

### 1.3 The tools amendment 3 pins are exactly the bytes at 77302fa

`contract-amendment-3.json` `tool_sha256` claims
`c1-pins.py` = `7bc1929f…52f440` and `tools/mte-interop.py` =
`8269b82f…6eb02c`. Verified:

```
$ GIT_OPTIONAL_LOCKS=0 git show 77302fa:.ufo/evidence/round-25/c1-pins.py | sha256sum
7bc1929fd4c291bbc7b37ae6a40dc3f80a5491a1b5bc08f5dceb72c29752f440  -
$ GIT_OPTIONAL_LOCKS=0 git show 77302fa:tools/mte-interop.py | sha256sum
8269b82f213e094ffd30adc20b20e28b1f67764d2eccb089983eb9dc546eb02c  -
```

Both equal the JSON's pinned values, so the amendment and the measured
revision describe the same tool bytes (independent corroboration of the
verifier's `tools/mte-interop.py` row at
`corpus/lessons/round-25-verifier-spotcheck.md:72`).

### 1.4 Ordering: amendment 3 precedes the recorded after-measurement

From `corpus/lessons/round-25-verifier-spotcheck.md:82-88` (read this
session), verbatim:

```
- Amendment 2 is `09dc114` (05:35 −03). Amendment 3 lands in `77302fa`
  (06:26), the measured commit itself. The recorded after receipts arrive in
  `154bf4d` (06:35). They were produced by the amendment-3 bytes: the
  `MTE_WORKDIR` line, the 17th selftest case `narrow-score-delta`, and c1-pins
  P5's exact row shape are all amendment-3 additions. **Both amendments precede
  the recorded after-measurement.**
```

The JSON's own flag is `"before_any_after_measurement": true`
(`contract-amendment-3.json`, 1288 bytes).

### 1.5 The limit of that flag (routed item 2)

`corpus/lessons/round-25-verifier-spotcheck.md:88-91`:

```
- Wave seats had already run the C2 counter at PASS 8/8 at `c9ff09f` and
  `09dc114` (`w1/C2LiveCheck.md`, `w1/DraftKnowledge.md:168`). That was before
  amendments 2 and 3, under the weaker ruler.
```

So `before_any_after_measurement: true` is accurate for the lane's recorded
after-measurement but does not cover the earlier seat probes. The block below
states that limit instead of repeating the flag unqualified.

### 1.6 Routing source

`corpus/lessons/round-25-verifier-spotcheck.md:193-196` (routed defect 2):

```
2. The SCORECARD round-25 header and the lesson's `## Claims` name only
   amendments 1–2. Amendment 3 (in `77302fa`) appears only in its JSON and the
   report. Its `before_any_after_measurement` flag also omits that seats saw
   C2 PASS 8/8 at `c9ff09f`/`09dc114`. Append a correction; do not rewrite.
```

## 2. The block to append (fenced; L1 integrates it at the end of `corpus/lessons/round-25.md`)

Append-only: nothing above the appended text is edited, and the block
repeats no earlier sentence. Both required strings — "amendment 3" and
"77302fa" — appear in it.

```markdown
## Correction (round 26)

Appended 2026-10-22 (round 26). Nothing above this line is rewritten.

The `## Claims` section above names amendments 1-2 only. It omits
**amendment 3**, which landed in `77302fa`
(`77302fa8f79144d06c1d2e2d2898c44b459bda`) and also preceded the
after-measurement recorded above. Amendment 3 amends
`.ufo/evidence/round-25/contract.json` and adds only refusals and one
selftest case; it changes no target, no claim population and no byte of the
frozen counter.

What amendment 3 added, quoting `.ufo/evidence/round-25/contract-amendment-3.json`:

- `"number": 3`, `"schema": "tameshi-r25-contract-amendment-v1"`,
  `"amends": ".ufo/evidence/round-25/contract.json"`,
  `"before_any_after_measurement": true`,
  `"c1_input_sha256_unchanged": true`.
- `.ufo/evidence/round-25/c1-pins.py`: "P5 requires the exact row shape
  `| R23-ROUTED-n | dispositioned |`"
- `tools/mte-interop.py`: "leg set and table set must equal the eight ledger
  legs (else SETUP); tar members must be relative regular files or directories
  under package/; node timeout -> SETUP; node presence checked before the
  sweep; MTE_WORKDIR printed; selftest case narrow-score-delta (17 cases)"
- `tool_sha256`: `.ufo/evidence/round-25/c1-pins.py`
  `7bc1929fd4c291bbc7b37ae6a40dc3f80a5491a1b5bc08f5dceb72c29752f440`;
  `tools/mte-interop.py`
  `8269b82f213e094ffd30adc20b20e28b1f67764d2eccb089983eb9dc546eb02c`.
  Both hashes equal the tool bytes at `77302fa`.
- `"why"`: "Late wave seats found more missing checks after amendment 2
  landed: C2TarSafety (a --workdir run could PASS over fewer legs; absolute tar
  member names not contained; node timeout escaped as exit 1), C2Mutants
  (score tolerance mutants survive), DraftLesson and C1BeforeRerun
  (c1-pins P5 accepted a row reading "NOT dispositioned"). Each change only
  adds a refusal or a selftest case; targets, claims and the frozen counter
  are unchanged."

Limit on the flag: `before_any_after_measurement: true` is the author's
assertion in that JSON. It holds for the lane's recorded after-measurement —
the verifier records amendment 3 in `77302fa` (06:26 -03) and the recorded
after receipts in `154bf4d` (06:35), and both amendments precede the recorded
after-measurement — but it does not cover seat probes: wave seats had already
run the C2 counter at PASS 8/8 at `c9ff09f` and `09dc114`, before amendments 2
and 3, under the weaker ruler. No target was narrowed by any of the three
amendments; each only adds refusals, which makes a pass harder.
```

## 3. Calibration notes

- The block states the amendment's own flag as the author's assertion and
  then states the two facts that bound it: the verifier's ordering evidence
  (`77302fa` 06:26 vs. recorded receipts `154bf4d` 06:35) and the earlier
  seat probes at `c9ff09f`/`09dc114`. It does not upgrade the flag into an
  unqualified claim, and it does not claim the amendment moved a target — the
  JSON's own `why` field says targets, claims and the frozen counter are
  unchanged, and that text is quoted rather than paraphrased.
- The only hashes in the block are hashes the amendment pins and that I
  re-derived from `git show 77302fa:…` (section 1.3). No numeric score,
  promotion or producer-authentication claim is made.
- Round-25 bytes quoted in the block (the JSON's `changes` and `why` strings)
  come from the working-tree file whose sha256 equals the `77302fa` blob
  (section 1.2). The `why` string is quoted as its parsed value: the file
  encodes the inner double quotes around `NOT dispositioned` as `\"` in its
  JSON string encoding.

## 4. Out of scope (routed elsewhere, not touched)

- The SCORECARD round-25 header, which also names only amendments 1-2
  (routed defect 2, first half; another seat's surface).
- `corpus/knowledge/mte-report-interop.md` `verified-at` still records the
  `09dc114` run (routed defect 3).
- `tools/mte-interop.py` registry row (routed defect 1).

## 5. Surfaces touched, tools, bounds

- Wrote exactly one file: this report,
  `.ufo/waves/round-26/w1/DraftLesson25Correction.md`.
- `corpus/lessons/round-25.md` was **read only**; the block above is a draft
  for the L1 to append (leaf seat; only the L1 edits lane files).
- No git write command was run in the lane (read-only `git log`/`git show`/
  `git diff`/`git branch` with `GIT_OPTIONAL_LOCKS=0`); no `jj` command was
  run anywhere; the fleet repo and sibling lanes were not touched; no code
  was executed, so no clone or scratch dir was needed.
- No tool was installed or upgraded (nothing was missing for this task).
