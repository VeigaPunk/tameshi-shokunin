# ReviewFlagWholeFile — whole-text FLAG_RE dependence of the planted flagged cases

Milestone: ReviewFlagWholeFile
Axis: depth (C1, `write-path-census-v2`, contract `.ufo/evidence/round-40/contract.json`, frozen `5641ed84…`)
Scratch: `/tmp/tameshi-r40-ReviewFlagWholeFile/` (no lane file touched; lane checkout sha-verified, unmodified)

## Mechanism (definition check)

`tools/write-path-census-v2.py:32-44` — `classify_text` computes
`flagged = FLAG_RE.search(text) is not None` on the **whole fixture text** (`:33`) and gates
unflagged on `… SCRATCH_RE.search(line) is None and not flagged` (`:40`). One flag token
anywhere zeroes unflagged for every line. `FLAG_RE` = `--update_goldens|--update-goldens|--update\b|update_goldens`
(`write-path-census-v2.py:25`). The counter scores the planted counts through exactly this
function: `measure.py:159` (`got = {name: mod.classify_text(planted[name]) …}`). The embedded
v1 replay has the same document-global scope (`measure.py:62`, `:69`).

Checkout identity: `sha256sum tools/write-path-census-v2.py` →
`4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b` = contract pin; v1 →
`bc8c660c…` = contract `v1_sha256`. Fixtures are absent at base `304e3355` (`git show 304e3355:.ufo/evidence/round-40/census/fixtures.json` → "exists on disk, but not in") and tracked+clean at HEAD.

## Finding (severity: load-bearing for C1's flagged-case clause)

**Both planted flagged cases depend on whole-text flag scope; a same-line-only flag flips
their planted counts 0→1 and would flip C1_R40_PASS true→false.**

In `.ufo/evidence/round-40/census/fixtures.json`, both flagged fixtures put the flag token on
line 1 and the write on line 2:

```
bytes_flagged    L1 [F E] "if '--update_goldens' in argv:"
                 L2 [W E] "    (out / 'expected.json').write_bytes(b'x')"
replace_flagged  L1 [F E] "if '--update_goldens' in argv:"
                 L2 [W E] "    os.replace(tmp, 'case.expected')"
```

(F=FLAG_RE, W=WRITE_RE, E=EXPECTED_RE, S=SCRATCH_RE; L2 has no scratch hit.) The only thing
that keeps L2 from scoring unflagged=1 is the document-global flag from L1 — v2's
write/expected discrimination itself carries no flag awareness. Line-level note: L1's
`--update_goldens` also hits v2 EXPECTED_RE via its `golden` alternative, so L1 is [F E], but
it has no write, so this changes nothing.

Counterfactual — one-line patch of the pinned v2 (`not flagged` → `FLAG_RE.search(line) is
None`, i.e. same-line-only flag; scratch copy
`/tmp/tameshi-r40-ReviewFlagWholeFile/v2-sameline.py`), replayed via
`mod.classify_text` over the planted fixtures:

```
                   whole-text   same-line-only
bytes_unflagged      (1, 1)        (1, 1)      unchanged
bytes_flagged        (1, 0)  →     (1, 1)      FLIPS
replace_unflagged    (1, 1)        (1, 1)      unchanged
replace_flagged      (1, 0)  →     (1, 1)      FLIPS
scratch_replace      (1, 0)        (1, 0)      unchanged (SCRATCH_RE hits the line; no expected match)
```

The same variant's `--selftest --fixtures` fails on exactly those two cases:

```
rc=1  WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=1 replace_flagged=1 scratch_replace=0
FAIL planted bytes_flagged: want unflagged=0 got 1
FAIL planted replace_flagged: want unflagged=0 got 1
```

(pinned v2 selftest: rc=0, `…bytes_flagged=0 replace_flagged=0…`). Through the counter:
`measure.py:210-219` (`planted_ok`) requires `got['bytes_flagged'][1] == 0` (`:213`) and
`got['replace_flagged'][1] == 0` (`:214`) plus `rc.returncode == 0` (`:218`) — all three break.
Every other C1 clause is flag-scope-invariant: `bytes_unflagged=1`/`replace_unflagged=1`
(no flag token in those fixtures); the embedded-v1 misses `v1_bytes = v1_classify(planted['bytes_unflagged'])[1]`
/ `v1_replace_writes = v1_classify(planted['replace_unflagged'])[0]` (`measure.py:187-188`) miss
because V1_EXPECTED_RE cannot see `'expected.json'` and V1_WRITE_RE has no `os.replace`, not
because of any flag; `live_ok` (registry-replay / bash-witness lines) and the mutant-kill
checks never touch FLAG_RE.

`--control` baseline (allowed): `python3 .ufo/evidence/round-40/census/measure.py --control --lane .`
→ `C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false`
— the expected do-nothing state; control's two fixtures carry no flag token, so it is
flag-scope-invariant as well.

Consequence for the claim: C1's "both flagged cases … are 0" is supplied entirely by the
document-global flag scope of the pinned tool, not by anything in the v2 write/expected
capability being claimed. A same-line-only flag (arguably the more faithful reading of "this
write is flag-gated") zeroes the same planted counts only if the guard and the write share a
line — the planted fixtures never do. The predicate text is mechanism-agnostic, so a v2
variant that detects the guard on the write's own line could still pass C1 — but the pinned
sha `40228532…` does not do that, and changing it breaks the pin.

Side note, not load-bearing for C1: v1's own planted `flagged` fixture in
`tools/write-path-census.py:58-60` has the identical cross-line structure
(`if "--update_goldens" in argv:` / `open("case.expected", "w")`) and the same
document-global classifier (`:65`, `:72`); C1 gates v1 only by sha, so this dependence is
inert for the round-40 predicate.

## Residual risk / verification gaps

- Default-mode C1 was not run (reserved for the L1's deciding run). All numbers come from
  `--control`, the pinned source, and a scratch replay of the exact function the counter
  calls (`measure.py:159`). `measure.py` loads the tool blob from `git show REV:tools/write-path-census-v2.py`;
  the analysis is exact for any REV whose blob sha-equals the pin, which C1 requires anyway.
- The deciding REV is not known to me; if the L1 ships a tool whose sha differs from the pin,
  C1 fails on `tool_sha_ok` regardless of this finding.
- No lsp server was consulted: the claims are pure-Python regex semantics verified by direct
  execution of the pinned classifier, which is stronger than reference/definition lookup here.
