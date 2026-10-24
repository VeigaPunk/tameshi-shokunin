# MTContract — mutation probe: contract-to-counter digest compliance

Seat: MTContract (mutation-tester, leaf). Lane tip under probe:
`d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (`round-36: receipts — monitor before(796e08b)=6 / …`).
Scratch clone (disposable): `/fast/scratch/hyaku/tameshi-r36-seats/MTContract/lane`
(`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks <lane> lane`).
The real lane was never written: its `contract.json` re-hashed after the probe still
`3aaabcddf27d49d59f1930643fb52b46a55f0eaa16eeabd0e0767211419db4f9`, and the dispatch-specified
frozen artifacts were read only.

## What was attacked

The kill-rule compliance invariant the round-36 record claims for C2: the contract's
`claims.C2.counter_sha256` equals the actual bytes of
`.ufo/evidence/round-36/c1/c1-measure-v2.py`. The claim appears as:

- `.ufo/evidence/round-36/contract.json:24` — `"counter_sha256": "9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53"`;
- `SCORECARD.md` round-36 C2 row — "(C2 counter sha256 `9eb8944c…` recorded there)";
- dispatch instructions to peers `ReviewC2Claim` ("counter sha256 must equal 9eb8944c... frozen
  in contract.json — recompute") and `RevengerContractFreeze` ("the v2 sha256 in the contract
  equals the sha256 of the v2 file at the refresh commit").

## Mutant

Scratch-only, minimal, behavior-bearing: first hex nibble of `claims.C2.counter_sha256`
changed `9` → `8` (all other bytes identical; the file still parses as JSON, so this is a
semantic not a syntax mutant).

Detector — the same contract-vs-file comparison the report claims
(`/fast/scratch/hyaku/tameshi-r36-seats/MTContract/check-contract-hash.sh`):

```bash
#!/usr/bin/env bash
set -u
LANE="${1:?lane root}"
CONTRACT="$LANE/.ufo/evidence/round-36/contract.json"
CTR="$LANE/.ufo/evidence/round-36/c1/c1-measure-v2.py"
want=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["claims"]["C2"]["counter_sha256"])' "$CONTRACT") || exit 2
got=$(sha256sum "$CTR" | cut -d' ' -f1)
if [ "$want" = "$got" ]; then echo "PASS contract=$want actual=$got"; exit 0
else echo "FAIL contract=$want actual=$got"; exit 1; fi
```

## Outputs (verbatim)

| State | contract.json sha256 | Detector output | exit | Verdict |
|---|---|---|---|---|
| pristine scratch at `d9c496b` | `3aaabcdd…db4f9` | `PASS contract=9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53 actual=9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` | 0 | baseline green |
| mutant 1 (`9`→`8`) | `a12c89a3…bf61a4` | `FAIL contract=8eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53 actual=9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` | 1 | **killed** |
| restored | `3aaabcdd…db4f9` | `PASS contract=9eb8944c…fa53 actual=9eb8944c…fa53` | 0 | green again |

The counter file was never touched: `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`
throughout. `python3 -c 'json.load(...)'` on the mutant printed `valid json` — the failure is
the digest mismatch, not a parse error. Baseline failure did not occur; the killed verdict is
therefore sound.

**Restoration evidence.** Final scratch digests diffed byte-for-byte against the recorded
baseline (`baseline.sha256`): `IDENTICAL-TO-BASELINE`; `git -C lane status --porcelain` is empty;
detector back to `PASS` exit 0. The scratch clone is restored to its pristine lane-tip state.

## Supplementary calibration probe (same invariant, different nibble)

Mutating only the **last** nibble (`…fa53` → `…fa54`):

- full-digest detector: `FAIL … actual=…fa53`, exit 1 (killed);
- truncated-prefix comparison — the form the record actually evidences (`9eb8944c…`, first 8
  hex): `PASS prefix contract=9eb8944c… actual=9eb8944c…`, exit 0 (**survives**).

So a prefix-level reading of the pin cannot detect drift in the remaining 56 nibbles, while the
full-digest comparison can. This is a coverage observation, not a contract change.

## What the lane's own verification would have caught

1. **Nothing automated for this pin.** No committed script compares round-36's
   `claims.C2.counter_sha256` to the counter bytes. `grep -rln counter_sha256 tools/ scripts/ bin/`
   returns nothing; lane-wide, the token in executable code appears only in historical counters
   that *emit their own* digest (`.ufo/evidence/round-21/c2-count.py`, `.ufo/evidence/round-33/c1/c1-measure.py`)
   and in prose records/wave specs — none reads `.ufo/evidence/round-36/contract.json`. The
   committed receipts under `.ufo/evidence/round-36/` record the counter's *outputs*, not a
   digest re-derivation of contract against file.
2. **Caught only if a seat remembers to recompute.** The comparison is specified as narration —
   SCORECARD prose plus the dispatch prompts to `ReviewC2Claim` and `RevengerContractFreeze`.
   Those two in-flight seats would catch mutant 1 *if* they run the recompute; the committed
   evidence chain alone would not. Had the one-nibble mutant landed in the content commit and no
   seat recomputed, "Kill rule honored" would remain unfalsified in the record.
3. **Asymmetric risk.** Mutant 1 changes the 8-nibble prefix the SCORECARD quotes, so even a
   careful prose-level reader could spot it. The last-nibble variant is invisible to both the
   record's truncated evidence and any 8-hex comparison, and only a full-digest receipt kills it.
4. **Fix direction (not applied; no contract change).** The pin the record claims should be
   enforced by a committed receipt that emits the two digests and an exit code — the detector
   above is that shape — so the kill rule is gate-checked at write time rather than recalled in
   prose.

## Verdict

KILLED. A one-hex-digit edit to `contract.json`'s `claims.C2.counter_sha256` is caught by the
contract-vs-file digest comparison the report claims (FAIL, exit 1), and the pristine bytes
restore to `3aaabc…db4f9` with the detector green. The lane's own committed verification is not
an executable gate and would not have caught this mutation on its own; detection rests on the
two in-wave recompute seats, and a last-nibble variant would additionally survive a
prefix-only reading of the record's quoted `9eb8944c…`.
