# ScoutS108 — C2 S108 snapshot quote verification

## Question
Confirm the frozen C2 quote occurs in the tag-stripped text of
`.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` and does not occur as one
contiguous raw byte string. Record the sha256.

## Findings

- **sha256** of `golden_tests.zh-cn.html` (worktree, 111405 bytes):
  `f27cf274b5dd7c28122dcb5a137971b401dad7910f7702eb4cbd3c28cd782bf0`
  — equals frozen `claims.C2.snapshot_sha256` in `contract.json:36` (pin
  `5641ed84c8dc148c34c8dd83f062279ddf06b4af`). `git status --porcelain` is
  clean for the file; HEAD is `5641ed8` (the freeze commit).

- **Quote in tag-stripped text: YES.** Applying `measure.py`'s
  `stripped_text()` transform (remove `<script…>`, `<style…>`, all `<…>` tags,
  collapse whitespace), the quote
  `可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。`
  occurs at stripped byte offset **4819**.

- **Quote as contiguous raw bytes: NO.** The source line splits it with
  `<code>` tags:
  `golden_tests.zh-cn.html:3611`
  `<p>可以通过使用参数 <code>--test_arg=--update_goldens --test_strategy=local</code> 运行受影响的测试目标来更新 <code>.expected</code> 文件。应检查由此产生的差异是否存在意外的变化。</p>`

- **Prefix control holds.** `可以通过使用参数` occurs exactly once in raw
  bytes (`blob.count == 1`); removing it makes the stripped quote miss
  (measure.py `stripped_fails=1` condition satisfied).

## Commands run
- `sha256sum golden_tests.zh-cn.html` → `f27cf2…782bf0`
- Python repro of `measure.py`'s `stripped_text()` + `quote in stripped` /
  `quote in blob` (read-only; did not run the counter in default mode)
- `grep -n "可以通过使用参数" golden_tests.zh-cn.html` → line 3611

## Verdict
Snapshot is consistent with the C2 predicate: pin matches, stripped quote
present, contiguous raw quote absent, prefix-removal control holds.
Confidence: high.

No tools installed; no installs needed.
