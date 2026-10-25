# ReviewScratchToken — Attack SCRATCH_RE

Milestone: ReviewScratchToken · axis: depth · round 40, w1
Target: `SCRATCH_RE = re.compile(r'/tmp/|tempfile|TemporaryDirectory|NamedTemporaryFile|\bscratch\b')`
— `tools/write-path-census.py:54`, `tools/write-path-census-v2.py:26`, `.ufo/evidence/round-40/census/measure.py:41` (all byte-identical; pinned rev `5641ed84` confirmed via `git show`).

## Answers

**Is `/tmp/scratch-out.json` excluded by `/tmp/` or by the word `scratch`? — Both, independently.**
`SCRATCH_RE.search("'/tmp/scratch-out.json'")` returns `/tmp/` at span 12–17 (leftmost match wins), but the `\bscratch\b` alternation also matches on its own at span 18–25: the `-` after `scratch` is a non-word char, so `scratch-out` *does* contain the "word" `scratch`. Removing either single alternation leaves the path excluded; only removing both exposes it. Probe (`python3 /tmp/tameshi-r40-ReviewScratchToken/probe2.py`), verbatim regexes:

| mutant SCRATCH_RE | `unflagged` on `os.replace('/tmp/a','/tmp/scratch-out.json')` |
|---|---|
| frozen | 0 |
| minus `\bscratch\b` | 0 (`/tmp/` still hits) |
| minus `/tmp/` | 0 (`\bscratch\b` still hits) |
| SCRATCH_RE deleted entirely | **0 — see defect below** |

**Would a `/var/tmp` path be counted? — Excluded, if it has any component after `tmp`.**
`/tmp/` is an unanchored substring match: `'/var/tmp/case.expected'` matches `/tmp/` at offset 10, so it is excluded (probe: `scratch='/tmp/'`, `unflagged=0`). Edge: a bare `'/var/tmp'` with no trailing slash does **not** match — the literal needs `/tmp/` incl. the slash — so `os.replace('a','/var/tmp')` evades SCRATCH_RE entirely (though such a path also fails EXPECTED_RE in practice).

## Concrete defect — the `scratch_replace` fixture does not test SCRATCH_RE at all

`fixtures.json` plants `scratch_replace = "os.replace('/tmp/a', '/tmp/scratch-out.json')\n"`, and the C1 predicate (`contract.json` claims.C1) requires `scratch_replace` = 0. But the line scores 0 on **EXPECTED_RE grounds alone**: `scratch-out.json` contains none of `.expected`/`expected.txt`/`expected.json`/`golden`/`snapshot` (`EXPECTED_RE.search` → `None`, verified above). `classify_text` (`write-path-census-v2.py:40`, `measure.py:69`) requires EXPECTED_RE *and* no-SCRATCH_RE; the first conjunct fails before scratch is ever consulted.

Consequence: the fixture cannot discriminate `/tmp/` vs `\bscratch\b` vs *no scratch regex at all* — a v2 build with SCRATCH_RE removed entirely still prints `scratch_replace=0` and passes that conjunct of C1. The "scratch" claim is unfalsified-by-fixture, not verified-by-fixture. To make it bite, the destination path would need an expected-token name, e.g. `os.replace('/scratch/a','/scratch/case.expected')` (probe: excluded via `\bscratch\b`, `unflagged=0`) or `os.replace('a','/var/tmp/case.expected')` (excluded via `/tmp/` substring).

## Word-boundary precision (what "word scratch" actually admits)

`\bscratch\b` is token-delimited, not substring: `scratch-out`/`x.scratch`/`scratch/…` match; `scratch_out`, `scratchout`, `myscratch/…`, `scratchy/…` do **not** (probe: `scratchy/case.expected` → `unflagged=1`, counted). So a path containing `scratch` as an affix, not a word, is counted — the narrow reading of "the word scratch" is correct, but the planted fixture exercises none of this boundary logic.

## Evidence
- Regex bytes: `tools/write-path-census-v2.py:26`, `tools/write-path-census.py:54`, `measure.py:41`; gate at `write-path-census-v2.py:40` / `measure.py:69`.
- Fixture: `.ufo/evidence/round-40/census/fixtures.json` → `"scratch_replace": "os.replace('/tmp/a', '/tmp/scratch-out.json')\n"`.
- All match/mutant outputs above are from `python3 /tmp/tameshi-r40-ReviewScratchToken/probe{,2}.py` using the verbatim frozen patterns; live lane untouched, no counters run in default mode.
