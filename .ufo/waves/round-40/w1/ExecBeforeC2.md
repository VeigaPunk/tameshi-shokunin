# ExecBeforeC2 — C2 (freshness) re-run before settlement

Seat: executor, leaf. Axis: freshness. Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Frozen contract: `.ufo/evidence/round-40/contract.json` at `5641ed84c8dc148c34c8dd83f062279ddf06b4af`
(blob `0f012e56225ae79e66d0cd6d0b7f6136f946be23`; worktree copy byte-identical to that blob). Not edited.

## Assigned run — base rev 304e335

```
$ python3 .ufo/evidence/round-40/s108/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 304e3355705640af2879c772fc9a5c2902c61763
C2_R40: snapshot_absent=1 quote_in_snapshot=0 sha_ok=0 stripped_quote_fails=0 rev=304e3355705640af2879c772fc9a5c2902c61763 C2_R40_PASS=false
exit=1
```

Base stays `C2_R40_PASS=false` by the do-nothing path: `.ufo/evidence/round-40/s108/golden_tests.zh-cn.html`
is absent at that rev (`git show 304e335:.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` → exit 128;
`.../contract.json` → exit 128). The counter reads the **rev**, not the worktree: the snapshot file does
exist on disk, yet `snapshot_absent=1` at this rev.

## Pre-settlement re-run at freeze commit 5641ed8 (scratch copy, live script untouched)

`/tmp/tameshi-r40-ExecBeforeC2/measure_scratch.py` = verbatim copy of the s108 counter.

```
$ python3 /tmp/tameshi-r40-ExecBeforeC2/measure_scratch.py --lane .../tameshi-shokunin --rev 5641ed84c8dc148c34c8dd83f062279ddf06b4af
C2_R40: snapshot_absent=0 quote_in_snapshot=1 sha_ok=1 stripped_quote_fails=1 rev=5641ed84c8dc148c34c8dd83f062279ddf06b4af C2_R40_PASS=true

$ python3 /tmp/tameshi-r40-ExecBeforeC2/measure_scratch.py --lane .../tameshi-shokunin --rev 304e3355705640af2879c772fc9a5c2902c61763
C2_R40: snapshot_absent=1 quote_in_snapshot=0 sha_ok=0 stripped_quote_fails=0 rev=304e3355705640af2879c772fc9a5c2902c61763 C2_R40_PASS=false
```

The pass at 5641ed8 is the state settlement must preserve; the deciding run is still the L1's.

## Independent byte checks (no counter involved)

On the blob at `5641ed8:.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` (111405 bytes):

- `sha256 = f27cf274b5dd7c28122dcb5a137971b401dad7910f7702eb4cbd3c28cd782bf0` — equals
  `claims.C2.snapshot_sha256`. Worktree file has the same sha; same sha again at the two side commits
  that also carry this path (`2e7024e`, `58429fa`, both outside the current branch) — no alternate snapshot bytes exist.
- `quote_in_RAW_bytes = 0`, `quote_in_STRIPPED = 1`: the page wraps the flags in `<code>` and `.expected`
  in `<code>`, so the contiguous quote only exists after tag-stripping. The counter's `stripped_text`
  (measure.py:36-41) is the correct check; a raw-byte search would be a false negative.
- `prefix_occurrences = 1`; after replacing the contiguous prefix `可以通过使用参数` with `QUOTE_REMOVED`,
  `quote_in_stripped = 0` → `stripped_quote_fails=1`, i.e. the negative control named in the predicate
  actually bites (measure.py:79-81).
- Snapshot integrity: canonical link and `og:url` both `https://www.tensorflow.org/federated/golden_tests?hl=zh-cn`
  (the contract URL), `<title>` = `黄金测试 | TensorFlow Federated`, document ends `</html>` (not truncated).

## Falsification attempts and results

1. Missing file at rev → fail. Confirmed at base (exit 1, `snapshot_absent=1`).
2. Prefix removed → cannot pass. Confirmed by the scratch computation above (stripped quote disappears).
3. Wrong bytes with right status → not reachable: pass requires sha equality to the pin, not a status field.
4. Freshness of the source (live check, corroborative only): `https://www.tensorflow.org/federated/golden_tests?hl=zh-cn`
   fetched 2026-10-24 still renders `可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。`
   Page footer: `最后更新时间 (UTC)：2022-06-07` — stable source, snapshot not fabricated.

## Risks / notes

- `measure.py:52-66` reads pin and quote from the **contract blob at the rev under test**. A later commit
  that rewrites `contract.json` silently re-points the check. Settlement must run against a rev whose
  contract blob is still `0f012e56225ae79e66d0cd6d0b7f6136f946be23`; a changed contract is the one way this
  counter can be moved without touching the snapshot.
- Untracked wave inputs (`.ufo/waves/round-40/...`) and a pre-existing `corpus/QUALITY.md` modification are
  in the worktree; not mine, untouched.
- No live-lane file edited, no counter run in default mode against a candidate settlement rev, no tool installs.
