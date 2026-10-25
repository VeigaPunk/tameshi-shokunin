# CriticC2One — C2 depth, milestone "Constant one"

## Finding

A census tool whose classifier always reports `unflagged=1` fails the
`planted_scratch` selftest conjunct because the planted scratch body must
classify to `unflagged=0`, and it is excluded twice over — once by the scratch
regex and once by the expected-path regex.

## Planted scratch body (cited)

`tools/write-path-census.py` at contract pin
`bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62`:

- `write-path-census.py:60` — `'scratch': 'open("/tmp/census-scratch.txt", "w")\n',`
  inside `PLANTED` (`:57-61`).
- `write-path-census.py:54` — `SCRATCH_RE = re.compile(r'/tmp/|tempfile|TemporaryDirectory|NamedTemporaryFile|\bscratch\b')`
  matches `/tmp/` in that path.
- `write-path-census.py:51-53` — `EXPECTED_RE` requires `.expected` /
  `expected.txt` / `golden` / `snapshot`; `census-scratch.txt` matches none.
- `write-path-census.py:72` — a write line counts as unflagged only if
  `EXPECTED_RE.search(line) and SCRATCH_RE.search(line) is None and not flagged`;
  the scratch line fails on both regex grounds, so the correct count is 0.
- `write-path-census.py:89` — `expect = {'unflagged': 1, 'flagged': 0, 'scratch': 0}`
  hard-codes `scratch: 0`; `selftest()` emits
  `FAIL planted scratch: want unflagged=0 got 1` and returns rc=1.
- Counter side: `.ufo/evidence/round-39/census/measure.py:128` requires
  `fields.get('planted_scratch') == '0'`; line 130 requires `rc == 0`. Both fail.

## Evidence (commands run, all in /tmp, live lane untouched)

1. `python3 write-path-census.py --selftest` (pinned tool at HEAD):
   `planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1`,
   exit 0.
2. `python3 const1.py --selftest` (same tool, `return write_sites, unflagged`
   at line 74 replaced by `return write_sites, 1`):
   `planted_unflagged=1 planted_flagged=1 planted_scratch=1 fixture_wrote=1`
   plus `FAIL planted scratch: want unflagged=0 got 1`, exit 1.
3. End-to-end counter run against a /tmp scratch lane
   (`/tmp/tameshi-r39-CriticC2One/fake-lane`, rev `611ab832…`, 21 real gates +
   constant-1 tool committed):
   `python3 .ufo/evidence/round-39/census/measure.py --lane /tmp/tameshi-r39-CriticC2One/fake-lane --rev 611ab832a2c38ffc81263be8dfbd98a004e459f2`
   → `planted_scratch=1 … C2_R39_PASS=false`, exit 1.

## Impacted axis

Depth (C2). `planted_scratch` is a non-negotiable PASS conjunct
(measure.py:128,133); a constant-1 classifier cannot reach
`C2_R39_PASS=true` regardless of sha pin or gate coverage. It also trips
`planted_flagged` (same constant, `want unflagged=0`), so the constant-1
classifier fails on two independent planted controls — it cannot distinguish
a guarded/scratch write from a live unflagged expected-file write, which is
precisely the depth the claim measures. This matches the contract's own
do-nothing control note: "A classifier that always reports 1 fails
planted_flagged and planted_scratch" (contract.json:28).

## Smallest safe correction

None available to the tool itself — a constant output is rejected by
construction. The real fix is exactly what the pinned tool does: run
`WRITE_RE` line-by-line and count a site only when `EXPECTED_RE` matches,
`SCRATCH_RE` does not, and no `FLAG_RE` appears in the body
(write-path-census.py:64-74). No predicate or contract edit needed; the
planted bodies already encode the required discrimination.
