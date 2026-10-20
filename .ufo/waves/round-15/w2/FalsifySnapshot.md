# FalsifySnapshot — round 15 wave 2 critic

Seat: TameshiR15.FalsifySnapshot (critic, leaf). This was a static review only. I did not run the gate, the selftest, or any build, test, or formatter. I did not install anything.

## Source read (exact)

`tools/context-capture.py`. When I read it, its sha256 was `0ed784e0076b3de5ec5000c3862a771a3e3e2eb83241da347a6cf3f2f2c61edc`, as reported by `sha256sum`. The read tag was `#472A`. I read these ranges:
- 1–106: docstring, finding IDs, exit map
- 296–350: hash, strict JSON, `read_regular`
- 1108–1216: verdict, invalid blocks, `check_receipt`, expected-pin validation
- 1248–1346: `emit`, `apply_expected`, `result_from_exception`, `run_check`
- 1579–1770: selftest harness and early cases
- 1880–2018: snapshot, JSON, expected and usage cases
- 2020–2116: CLI

I also grepped the whole file for every `open(`, `os.stat`, `subprocess` and `read_regular(` site, and for every `receipt_bytes=` and `expected_override=` call.

These are static byte observations, not gate runs:
- `sha256sum .ufo/evidence/round-14/context-receipt.json` gives `05cb55b8…99c1a`. This equals `FROZEN_RECEIPT_SHA256`.
- `sha256sum .ufo/evidence/round-14/capture-context.py` gives `7313e9a2…7d89`. This equals `FROZEN_TOOL_SHA256`. The receipt's own `tool_sha256` at line 4 has the same value.
- At lines 421–423 the frozen receipt records `status` `ok`, `exit` 0 and empty `reasons`.

## Bounded agreement: the source enforces the property

- **Digest check comes before parsing.** In `run_check`, `read_regular` reads the receipt into a single `raw` buffer (1318). The tool hashes that buffer (1323) and compares it with `expected["receipt_sha256"]` (1324). On a mismatch it returns `snapshot_tampered` with exit 2 (1325–1333) before `parse_json_strict` (1335) or `check_receipt` (1336) runs. Parsing uses the same `raw` bytes that were hashed, so the file cannot change between the hash and the parse.
- **A tampered receipt can never pass.** `apply_expected` only rewrites the result when its exit is 0 (1277–1282). A tampered receipt has exit 2, so `expected_verdict_mismatch` is only appended as a secondary finding. The primary result stays `snapshot_tampered` with exit 2, and no expected pin can turn a digest mismatch into exit 0.
- **Every check-mode input is covered.** The only file reads on the check path are the receipt and the expected pin (`read_regular`, 1213 and 1318) and the tool itself. The tool reads its own bytes in `tool_sha256()` (302), but the result only reports that value and never uses it to decide.
  - In frozen mode the pin is built into the tool (1303–1308). Its digest matches the archived bytes above.
  - In explicit mode the expected file is the caller's trust root, which the docstring says (99–100). Requiring a digest of the pin itself would be inflating the requirement.
  - The `sources.*` digests are compared only as strings inside the receipt, and lines 11 and 100–102 disclose this. Requiring a disk re-hash would go beyond bounded retained-replay C1.

## Falsifiable hole: the selftest does not pin "before semantic comparison"

**Counterexample (mutant M2):** keep the source as it is, but move the digest comparison (1323–1333) after `check_receipt`. Then return the semantic findings when there are any, and emit `snapshot_tampered` only when the receipt is semantically clean. This is the plausible "verify content, then integrity" ordering.

Under M2, every current selftest case still gets its pinned id and exit:
- The only case with a mismatched digest is `snapshot-tampered` (1906–1913). It pairs the semantically clean fixture `clean` with the pin `"0"*64`. M2 parses it, finds nothing, then reports `snapshot_tampered` with exit 2, so the case still passes.
- Every case that supplies `receipt_bytes=` (1887–1904) gets a pin the harness computed from those same bytes (1627). Their digests match, so M2 handles them unchanged.
- The `expected-*` cases fail inside `load_expected` before any receipt is read, so M2 does not touch them.

The broken behaviour M2 adds, which the selftest cannot detect:
- Write the `comparison_raw_mismatch` fixture bytes, but pin them with the sha256 of the clean fixture bytes, using `id=comparison_mismatch` and `exit=1`.
- The real source returns `snapshot_tampered` with exit 2.
- M2 returns `comparison_mismatch` with exit 1 and `verdict_matches_expected: true`. A byte-mutated receipt then counts as reproducing its pin. This is the false-provenance failure the digest pin exists to prevent.

A weaker variant, M1, parses before hashing and lets `CouldNotEvaluate` return first. Fed `b"{"` under the clean pin, it gives `receipt_json_invalid` instead of `snapshot_tampered`. The exit is still 2 and only the id changes. The current selftest also passes M1.

**Impacted axes:**
- Calibration (C1): the selftest does not pin the literal exit/finding pair for the ordering property.
- Provenance: the selftest gives no proof that integrity is checked before semantics.

The delivered source is correct. This is a defect in the test's power, not a wrong verdict today.

**Smallest safe correction:** add one subprocess case through the existing harness. It needs no new API:

```python
mutated = mutate(comparison_raw_mismatch)
clean_bytes = (json.dumps(clean, indent=2, sort_keys=True) + "\n").encode()
harness.check_case(
    "snapshot-tampered-before-semantic", mutated, "snapshot_tampered", 2,
    expected_override={"schema": EXPECTED_SCHEMA,
                       "receipt_sha256": sha256_bytes(clean_bytes),
                       "id": "comparison_mismatch", "exit": 1})
```

What it catches:
- It kills M2: the primary id would be `comparison_mismatch` and the exit 1.
- With `receipt_bytes=b"{"` and the same clean-pin override, it also kills M1: the primary id would be `receipt_json_invalid`.
- The harness's existing primary-id and exit assertions (1653–1659) are enough to tell the cases apart. No harness change is needed.

This is a fixable defect, not a tradeoff that the canonical judge has to reject.
