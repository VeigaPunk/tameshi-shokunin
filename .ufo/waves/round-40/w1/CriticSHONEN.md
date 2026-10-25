# CriticSHONEN — round-40 w1 (calibration)

## Finding

CONFIRMED, no counterexample found. `SHONEN.md` holds four `[~]` and zero
`[x]` at both the frozen base and HEAD, the file is byte-identical across
`304e335..HEAD`, and nothing in the round-40 contract or counting tools
touches it.

## Evidence

- `SHONEN.md:5,7,9,11` — all four boxes read `- [~]`; every continuation
  line is annotated "no independent promotion verifier"
  (`SHONEN.md:6,8,10,12`).
- Mark census (same command form as round-1 command C):

  ```
  git show 304e3355705640af2879c772fc9a5c2902c61763:SHONEN.md | python3 -c \
    'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); \
     print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~")))'
  → boxes=4 checked=0 asserted=4 untouched=0
  ```

  Identical result at `HEAD` (`5641ed84c8dc148c34c8dd83f062279ddf06b4af`,
  the contract-frozen commit).

- `git diff --stat 304e335..HEAD -- SHONEN.md` → empty; file untouched this
  round. `git status --porcelain -- SHONEN.md` → clean.
- Neither counting tool references SHONEN: `grep -l SHONEN
  .ufo/evidence/round-40/census/measure.py
  .ufo/evidence/round-40/s108/measure.py` → no match. C1 (write-path
  census v2) and C2 (s108 source pin) cannot flip a mark.
- Frozen contract `.ufo/evidence/round-40/contract.json:19-42` scopes C1/C2
  to tool-sha and snapshot-sha predicates only; no SHONEN clause exists.
- Only other SHONEN.md in the lane is the archived copy
  `.ufo/waves/round-18/staged/SHONEN.md` — also four `[~]`, zero `[x]`;
  staging artifact, not live.

## Why [x] must not be written this round

`[x]` requires a named non-author verifier (PROTOCOL.md promotion rule,
restated at `.ufo/waves/round-12/w1/AdmissionBounds.md:79-80`); every box's
own annotation records that no independent promotion verifier exists, and
no round-40 claim supplies one. Any `[x]` write would repeat the round-1
baseline defect (`fleet-round-1/calibration-acceptance.json`: four
self-attributed `[x]`, calibration 0) and regress calibration.

## Impacted axes

calibration only. Depth/freshness unaffected.

## Smallest safe correction

None needed — state already conforms. Guard stands: keep all four `[~]`.
