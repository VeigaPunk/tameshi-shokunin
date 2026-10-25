# CriticQuoteRaw — round-40 C2 raw-quote attack review

## Verdict
Attack falsified — no defect. A counter that searches the raw HTML for the
contiguous quote MUST fail; the frozen predicate and the counter both check
tag-stripped text.

## Evidence

1. **Frozen predicate is tag-stripped.**
   `.ufo/evidence/round-40/contract.json:33` —
   "the quote occurs in its tag-stripped text; a missing file, or the same
   file with the contiguous prefix 可以通过使用参数 removed, cannot pass".

2. **Counter implements stripped-text search.**
   `.ufo/evidence/round-40/s108/measure.py:36-41` (`stripped_text` removes
   script/style blocks, all tags, collapses whitespace) and `measure.py:76`
   (`present = int(quote_bytes in stripped_text(blob))`).

3. **Raw contiguous quote is absent from the snapshot.**
   Command:
   ```
   python3 -c "data=open('.ufo/evidence/round-40/s108/golden_tests.zh-cn.html',encoding='utf-8').read();
   q='可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。';
   print(q in data)"
   ```
   Output: `False`. Raw bytes at offset 88171:
   `可以通过使用参数 <code>--test_arg=--update_goldens --test_strategy=local</code> 运行受影响的测试目标来更新 <code>.expected</code> 文件。`
   — `<code>` tags split the quote, so a raw-byte contiguous search fails.
   After tag stripping the quote is present exactly once.

4. **Prefix removal fires `stripped_quote_fails`.**
   Replicating `measure.py:77-79` on the working-tree blob (scratch-level
   check; no counter run against a rev):
   - `可以通过使用参数` occurs 1× in the blob; quote occurs 1× in stripped text.
   - `blob.replace(prefix, b'QUOTE_REMOVED', 1)` → quote absent from
     stripped text → `stripped_quote_fails=1`.

5. **Sha pin blocks mutation bypass.**
   `sha256sum` of the snapshot = `f27cf274b5dd7c28122dcb5a137971b401dad7910f7702eb4cbd3c28cd782bf0`,
   matching `contract.json:36`; any edit (including pre-stripping the file or
   planting a second contiguous copy) breaks `sha_ok` (`measure.py:80`).

## Smallest safe correction
None required. The predicate's negative control (prefix removal) is exercised
by the counter's own `stripped_quote_fails` field and holds on the pinned
bytes.
