source: S107 — https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md — §How do I update `.expected` files?; S108 — https://www.tensorflow.org/federated/golden_tests?hl=zh-cn — 如何更新 .expected 文件？
verified-at: 2026-10-24
recheck: 365d
ground: F4 (golden / snapshot fixture discipline — the explicit update flag)

# An expected-value write sits behind an explicit update flag

## What was opened

TensorFlow Federated's golden-file note, at commit `4d3a89c9b72f9c19352318d1457a5f7c01462824`, states the update path in one place: `.expected` files are updated by running the affected test with `--test_arg=--update_goldens --test_strategy=local`, and the resulting diff is checked for unanticipated changes. The same page's official zh-cn localization restates that flag and the diff check. This round opened both pages (2026-10-24). The upstream markdown is the tier-A statement; the localization is tier B for the wording on that page, not a second behavioural authority.

## What this lane uses it for

F4 asks whether an update path writes an expected value without an explicit flag. The rule this entry admits is the flag itself: a write of an expected file is a flagged path, and a comparison that rewrites the expected file with no flag is not the discipline. The lane's round-39 census (`tools/write-path-census.py`) is the measurement of that question over the lane's own gates. This entry does not claim that measurement; the counter receipt does.

## Boundary

- The note describes a documented flag. It is not a run of TensorFlow Federated's test runner, and it does not say the lane's gates are free of unflagged writes.
- POSIX `diff`'s three exit values stay in `golden-comparison-verdict.md`. This entry does not widen that lattice.
- A variable named `golden` is not an expected-value path. The census pattern counts a string literal, not an identifier.
