seat: ExecC2Recheck

# ExecC2Recheck — C2 quote + recheck audit (round 45, wave 2)

Scope: the two C2 entries at integration commit `ad5942c6e9858af19d00000b58439b321ddfa62b`
(lane HEAD at audit time `1f9266ac6d4a107a16ca80a2b81c985df5ecad14`). Read-only on the lane; all
scratch under `/tmp/tameshi-r45-ExecC2Recheck/`. No tools installed or upgraded.

## 0. Entry bytes audited

```
$ L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
$ git -C "$L" show ad5942c6…:corpus/knowledge/r8-gtest-order-and-seed.md > /tmp/…/order.md
$ git -C "$L" show ad5942c6…:corpus/knowledge/r8-gtest-primer-independence.md > /tmp/…/primer.md
8c691f7945e56540869c755c252050e3097a8f30f3f586037b89af1090b11ba4  order.md   (30 lines)
08cba4bb58a91eb3fdeb48dc564ab787cef20d3c8774a15010f21525751be4fa  primer.md  (28 lines)
$ git -C "$L" diff --stat ad5942c6…..HEAD -- corpus/knowledge/r8-gtest-order-and-seed.md corpus/knowledge/r8-gtest-primer-independence.md
(empty, exit 0)   # no later commit touches corpus/knowledge/ in ad5942c6..HEAD
```
So every finding below holds identically at `ad5942c6` and at HEAD `1f9266ac`.

Snapshots audited (both present, sizes as committed):
`.ufo/evidence/round-45/coverage/sources/googletest-advanced.md` (2457 lines, 89689 B),
`googletest-primer.md` (482 lines, 19101 B).

```
$ sha256sum googletest-advanced.md googletest-primer.md
05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2  googletest-advanced.md
03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e  googletest-primer.md
$ curl -fsSL 'https://raw.githubusercontent.com/google/googletest/cd8e73f…/docs/advanced.md' | sha256sum
05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2  -
$ curl -fsSL 'https://raw.githubusercontent.com/google/googletest/cd8e73f…/docs/primer.md' | sha256sum
03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e  -
```
The prefixes cited in `order.md:1` (`05546ed6…`) and `primer.md:1` (`03d756ab…`) match, and live
bytes are byte-identical to both snapshots on 2026-10-25.

## 1. Every straight-double-quoted string: `grep -cF` count and cited line

28 quote instances (order.md 13, primer.md 15; 22 distinct strings). `grep -cF` is per-line, so a
quote that spans a markdown hard-wrap in the snapshot reports 0 even though it is present; the
last column is the independent check that the quoted span occurs in the cited line range after
whitespace folding (`re.sub(r"\s+"," ")`). "cited-on-line" = every `:N` / `:N-M` / `[snapshot:N-M]`
/ `` `:N` `` citation appearing on the same entry line as the quote.

### corpus/knowledge/r8-gtest-order-and-seed.md → googletest-advanced.md

| # | entry | quote | `grep -cF` | tokens | cited-on-line | cited range holds it (folded) |
|---|---|---|---|---|---|---|
| 1 | order.md:12 | Remember that the test order is undefined, so your code can't depend on a test | 1 | 15 | 896, 897, 899 | **896** |
| 2 | order.md:12 | preceding or following another. Also, the tests must either not modify the state | 1 | 13 | 896, 897, 899 | **897** |
| 3 | order.md:12 | state to its original value before passing control to the next test. | 1 | 12 | 896, 897, 899 | **899** |
| 4 | order.md:14 | This helps to reveal bad dependencies between tests. | 1 | 8 | 1975, 1977, 1979, 1981, 1982 | **1977** |
| 5 | order.md:14 | By default, GoogleTest uses a random seed calculated from the current time. | 1 | 12 | 1975…1982 | **1979** |
| 6 | order.md:14 | the random seed value, such that you can reproduce an order-related test failure | 1 | 13 | 1975…1982 | **1981** |
| 7 | order.md:14 | To specify the random seed explicitly, use the \`--gtest_random_seed=SEED\` | 1 | 9 | 1975…1982 | **1982** |
| 8 | order.md:16 | GoogleTest creates a new test fixture object for each test in order to make | 1 | 14 | 872, 873, 874-875, 881-888 | **872** |
| 9 | order.md:16 | tests independent and easier to debug. | 1 | 6 | 872…888 | **873** |
| 10 | order.md:21 | This helps to reveal bad dependencies between tests. | 1 | 8 | 1977, 897, 899 | **1977** |
| 11 | order.md:21 | preceding or following another. Also, the tests must either not modify the state | 1 | 13 | 1977, 897, 899 | **897** |
| 12 | order.md:21 | state to its original value before passing control to the next test. | 1 | 12 | 1977, 897, 899 | **899** |
| 13 | order.md:29 | This helps to reveal bad dependencies between tests. | 1 | 8 | — (no citation on line) | n/a — Limits bullet restating :1977; count 1 |

All 13: `grep -cF` = 1, i.e. each sits wholly on one snapshot line, and that line is the one cited.

Cited lines verbatim (`sed -n 'Np'`, first 160 cols):
```
872|GoogleTest creates a new test fixture object for each test in order to make
873|tests independent and easier to debug. However, sometimes tests use resources
874|that are expensive to set up, making the one-copy-per-test model prohibitively
875|expensive.
881|1.  In your test fixture class (say `FooTest` ), declare as `static` some member
888|    TearDownTestSuite()` function to tear them down.
896|Remember that the test order is undefined, so your code can't depend on a test
897|preceding or following another. Also, the tests must either not modify the state
899|state to its original value before passing control to the next test.
1975|You can specify the `--gtest_shuffle` flag (or set the `GTEST_SHUFFLE`
1977|This helps to reveal bad dependencies between tests.
1979|By default, GoogleTest uses a random seed calculated from the current time.
1981|the random seed value, such that you can reproduce an order-related test failure
1982|later. To specify the random seed explicitly, use the `--gtest_random_seed=SEED`
```
(`:1975` is cited only as the flag location, not as a quoted span; the quoted sentence is on
`:1977` — consistent. `:874-875` and `:881-888` are cited for the paraphrase, not a quote; both
ranges do support the sentence they are attached to.)

### corpus/knowledge/r8-gtest-primer-independence.md → googletest-primer.md

| # | entry | quote | `grep -cF` | tokens | cited-on-line | cited range holds it (folded) |
|---|---|---|---|---|---|---|
| 1 | primer.md:12 | Tests should be \*independent\* and \*repeatable\*. It's a pain to debug a test that succeeds or fails as a result of other tests. | **0** | 23 | 14-15, 15-16 | **14-15** |
| 2 | primer.md:12 | GoogleTest isolates the tests by running each of them on a different object. | **0** | 13 | 14-15, 15-16 | **15-16** |
| 3 | primer.md:14 | GoogleTest always deletes a test fixture before it creates the next one. | 1 | 12 | 251, 252-253, 329-330, 356-364 | **251** |
| 4 | primer.md:14 | GoogleTest does \*\*not\*\* reuse the same test fixture for multiple tests. Any changes one test makes to the fixture do not affect other tests. | **0** | 24 | 251…356-364 | **252-253** |
| 5 | primer.md:14 | GoogleTest constructs a \`QueueTest\` object (let's call it \`t1\`). | 1 | 9 | 251…356-364 | **329-330** (on 329) |
| 6 | primer.md:14 | The first test (\`IsEmptyInitially\`) runs on \`t1\`. | 1 | 7 | 251…356-364 | **329-330** (on 330) |
| 7 | primer.md:14 | Runs the test on the fixture object. | 1 | 7 | 251…356-364 | **356-364** (on 356) |
| 8 | primer.md:14 | Cleans up the fixture via \`TearDown()\`. | 1 | 6 | 251…356-364 | **356-364** (on 358) |
| 9 | primer.md:14 | Restores the state of all GoogleTest flags. | 1 | 7 | 251…356-364 | **356-364** (on 362) |
| 10 | primer.md:14 | Repeats the above steps for the next test, until all tests have run. | 1 | 13 | 251…356-364 | **356-364** (on 364) |
| 11 | primer.md:16 | The assertions come in pairs that test the same thing but have different effects on the current function. | **0** | 18 | 107-109, 109-110, 110-111, 83-84 | **107-109** |
| 12 | primer.md:16 | \`ASSERT_\*\` versions generate fatal failures when they fail, and \*\*abort the current function\*\*. | **0** | 13 | 107-109, 109-110, 110-111, 83-84 | **107-109** (on 108-109) |
| 13 | primer.md:16 | \`EXPECT_\*\` versions generate nonfatal failures, which don't abort the current function. | **0** | 11 | 107-109, 109-110, 110-111, 83-84 | **109-110** |
| 14 | primer.md:16 | Usually \`EXPECT_\*\` are preferred, as they allow more than one failure to be reported in a test. | **0** | 17 | 107-109, 109-110, 110-111, 83-84 | **110-111** |
| 15 | primer.md:16 | If a fatal failure occurs, it aborts the current function; otherwise the program continues normally. | **0** | 15 | 107-109, 109-110, 110-111, 83-84 | **83-84** |

Cited lines verbatim (`sed -n 'Np'`, first 160 cols):
```
 14|1.  Tests should be *independent* and *repeatable*. It's a pain to debug a test
 15|    that succeeds or fails as a result of other tests. GoogleTest isolates the
 16|    tests by running each of them on a different object. When a test fails,
 83|*nonfatal failure*, or *fatal failure*. If a fatal failure occurs, it aborts the
 84|current function; otherwise the program continues normally.
107|The assertions come in pairs that test the same thing but have different effects
108|on the current function. `ASSERT_*` versions generate fatal failures when they
109|fail, and **abort the current function**. `EXPECT_*` versions generate nonfatal
110|failures, which don't abort the current function. Usually `EXPECT_*` are
111|preferred, as they allow more than one failure to be reported in a test.
251|GoogleTest always deletes a test fixture before it creates the next one.
252|GoogleTest does **not** reuse the same test fixture for multiple tests. Any
253|changes one test makes to the fixture do not affect other tests.
329|1.  GoogleTest constructs a `QueueTest` object (let's call it `t1`).
330|2.  The first test (`IsEmptyInitially`) runs on `t1`.
356|*   Runs the test on the fixture object.
358|*   Cleans up the fixture via `TearDown()`.
362|*   Restores the state of all GoogleTest flags.
364|*   Repeats the above steps for the next test, until all tests have run.
```

**Verdict on (1):** no fabricated or misplaced quote. All 28 instances are located in the cited
snapshot exactly once after whitespace folding (document-wide count = 1 for each of the 22 distinct
strings) and each begins inside the range cited on its own entry line. The eight `grep -cF` = 0
results are a per-line artifact of `grep` against markdown hard-wraps (quotes 1, 2, 4, 11, 12, 13,
14, 15 in the primer table) — e.g. primer.md:14's `**not**` quote is split across snapshot lines
252/253, and the `:251` single-line quote in the same sentence does return 1. All token counts are
inside the contract's 6-25 window (min 6: `tests independent and easier to debug.` /
`Cleans up the fixture via TearDown().`; max 24: the `**not**` quote).

## 2. `recheck:` commands (entry line 3), run verbatim

order.md:3
```
$ curl -fsSL 'https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/advanced.md' | grep -cF 'the random seed value, such that you can reproduce an order-related test failure'
1
exit=0
```
Entry records "ran 2026-10-25 → 1" — reproduced: 1.

primer.md:3
```
$ curl -fsSL 'https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md' | grep -c 'GoogleTest always deletes a test fixture before it creates the next one.'
1
exit=0
$ curl -fsSL '…/primer.md' | grep -cF 'GoogleTest always deletes a test fixture before it creates the next one.'
1
exit=0
```
Entry records "expect 1; ran 2026-10-25 → 1" — reproduced: 1. (The recorded form is `grep -c`
BRE, so `.` is a wildcard; the fixed-string form also returns 1, so the match does not depend on
the wildcard.)

## 3. C2 counter preview at the integration commit (read-only; L1 makes the deciding run)

```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/coverage/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev ad5942c6e9858af19d00000b58439b321ddfa62b
ENTRY corpus/knowledge/r8-gtest-order-and-seed.md
ENTRY corpus/knowledge/r8-gtest-primer-independence.md
C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=ad5942c6e9858af19d00000b58439b321ddfa62b C2_R45_PASS=true
exit=0
```
`C2_R45_PASS=true` at `ad5942c6`; no `REFUSED` lines. This is a preview only — the deciding run is
the L1's.

## 4. Notes on the counter's strictness (why this audit is stricter)

`.ufo/evidence/round-45/coverage/measure.py:108-112` accepts an entry as soon as **any one** quote
that folds to 6-25 tokens is a substring of a cited row's normalized snapshot text; it does not
require every quote in the entry to be located, nor that the quote sits in the line range cited
beside it. The per-quote table in §1 therefore covers more than the counter does, and it passes.

## 5. Risks / blockers

- None for C2 as audited: entries unchanged `ad5942c6..HEAD`, snapshots byte-identical to live, both
  rechecks reproduce, counter preview green.
- Environment note (no artifact lost): `/tmp` (own 128 G filesystem) hit 100% mid-audit and one
  scratch write failed with `ENOSPC`; the retry succeeded. Cause is other seats' clones, not mine
  (my dir is 24 K). Nothing in the lane or the evidence tree was affected.
- Not run: `measure.py --selftest` (out of the assigned item; disk was tight).
