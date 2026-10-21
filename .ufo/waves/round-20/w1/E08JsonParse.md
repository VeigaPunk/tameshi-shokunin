# E08 — Malformed JSON and the checker’s exit-2 path

## Findings

Axes: documentation-quote fidelity, checker exit-code mapping, and parse/schema separation.

The Python documentation states: “If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised.” (16 words; [`json` documentation](https://docs.python.org/3/library/json.html), JSON decoder documentation.) It also defines `json.JSONDecodeError` as a subclass of `ValueError`.

In the frozen staged gate, `.ufo/evidence/round-20/stage/receipt-window.py` declares exit 2 as `EXIT_CE` (“could-not-evaluate”). `load_contract()` and `load_receipts()` call `json.load()` inside broad `except Exception` handlers. A malformed JSON document therefore raises `JSONDecodeError`, is wrapped as `ContractError("cannot read contract: ...")` or `ReceiptsError("cannot read receipts: ...")`, and is handled by `run()` as `CONTRACT_INVALID` or `RECEIPTS_INVALID`. `emit_ce()` returns exit 2. Text output has the form `RECEIPT_WINDOW: COULD_NOT_EVALUATE (<kind>: <detail>)`; `--json` emits the `tameshi-receipt-window-v1` schema with verdict `COULD_NOT_EVALUATE`, `kind`, and `detail`. Exact detail text depends on the malformed bytes and was not executed here.

**Parse failure vs. schema failure:** parse failure means `json.load()` cannot decode the input and raises `JSONDecodeError`. Schema failure means decoding succeeds but the gate rejects the resulting value, e.g. a non-object contract, invalid/empty `contract.instruments`, or a receipts document lacking an object with a `receipts` array. These schema errors also take exit 2, but are raised directly as `ContractError`/`ReceiptsError`, not as `JSONDecodeError`. The shared exit code and kind identify the file category, not whether the cause was syntax or schema; the detail distinguishes the checker’s messages. Further, the broad parse/read handlers also map I/O and text-decoding exceptions into this could-not-evaluate path, so exit 2 is not exclusive to malformed JSON. Per-receipt validation findings after envelope loading instead return exit 1.

The staged `measure.py` has a separate `load_json_bytes()` helper which catches exceptions and returns `None`; its separate `return 2` for a missing revision is not the receipt-window gate’s malformed-JSON exit-2 path.

## Commands / inspection actions and observed outputs

- `read https://docs.python.org/3/library/json.html` and `read https://docs.python.org/3/library/json.html:390-478` — observed the quoted invalid-document rule and `JSONDecodeError` documentation. The page identified itself as Python 3.15.0 documentation.
- `read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py:35-180` — observed `load_contract()`’s JSON parse wrapper and contract schema checks (lines 61–120), plus the receipts-envelope checks (lines 123–131) and receipt findings logic.
- `read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py:179-278` and `:1-33,203-241,350-367` — observed `EXIT_CE == 2`, the `run()`/`emit_ce()` mapping and output fields, CLI handoff, and `sys.exit(main())`.
- `read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/measure.py:34-163` and `:74-80,125-149` — observed `load_json_bytes()` returning `None` after any exception and the distinct measurement logic.
- No shell code or checker fixture was run; consequently no concrete runtime stdout, stderr, or process return code was collected. The output forms and exit-code mapping above are from the inspected source.

## Agreement / disagreement

Agree: malformed JSON is covered by the gate’s exit-2 could-not-evaluate handling. Important qualification: exit 2 also covers parse/read and envelope-schema failures; valid JSON with per-receipt findings is exit 1. No disagreement with the documentation semantics.

## Defects / unresolved gaps

No defect established. The checker intentionally catches broadly, so its exit-2 category is not specific to JSON syntax. A concrete `JSONDecodeError` detail for a particular malformed input remains unobserved because no fixture was run.
