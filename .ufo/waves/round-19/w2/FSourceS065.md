# FSourceS065 — scoped falsifier (2026-10-21)

- **Strongest assertion attacked:** w1 SourceS065 says S065 “bears on none” of R18-1…R18-5 “and not on the 0/5→5/5 count.”
- **Verdict: partially disagree.** Agree S065 is not evidence that any correction happened, the five-item arithmetic, or historical execution. Disagree with the categorical “not on the count”: S065 documents a JSON-input validation behavior that the count ruler itself uses when accepting receipts.

## Evidence

- Re-opened the official page, `https://docs.python.org/3/library/json.html`: `json.load()` `parse_constant` parameter says “If set, a function that is called with one of the following strings: '-Infinity', 'Infinity', or 'NaN'.” (17 words; page lines 306–308). §Infinite and NaN Number Values says the deserializer’s `parse_constant` can alter default acceptance (lines 601–618).
- Exact delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c9` has `.ufo/evidence/round-19/measure.py` SHA-256 `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`. Its `strict_json` is `json.loads(..., object_pairs_hook=unique, parse_constant=constant)`; `receipt()` uses it on R18-4 / R18-5 JSON. The post-55e worktree diff changes other ruler checks, not this parser/receipt path.
- **Concrete falsifier to the categorical boundary [INFERENCE from code]:** add an otherwise valid witness receipt’s unused field as `"extra": NaN`. `strict_json` invokes `constant` and raises before the receipt predicate; ordinary `json.loads` accepts that value. Thus S065 directly supports one receipt-input acceptance condition in the measurement instrument. It still does not show any real receipt was malformed or change the five outcomes by itself.
- The narrow sourcing claim remains accurate: contract.json:14 names S049 only; round-19 lesson:27–40 says other openings are advisory. The `SOURCES.md` blob at 55e matches the worktree exactly; S065 at line 74 still lists only `corpus/knowledge/guard-kill-closure.md` in used-by. No missed S065 row correction or C1 citation found.
- Plain JSON recount: `before.json` records baseline `7243e7f…`, five rows all `open`, corrected=0/open=5/total=5. `after-21e7932.json` records `21e79329…`, those same five IDs all `corrected`, corrected=5/open=0/total=5. Both receipts name ruler SHA-256 `c538c33d…`; this arithmetic is true for baseline→21e7932.
- **Revision / argv attribution:** the available `after` receipt is for 21e7932, not 55e. The 55e ruler blob hash differs from `c538…`; no after-55e measurement receipt was present in the round-19 evidence directory. Therefore the cited receipts do not establish a final 5/5 measurement at 55e (the lesson says L1 will run the final same-ruler measurement). R18-4 JSON records argv `python3 tools/bash-witness-study.py selftest`, revision `4b7c6823…`, exit 0; R18-5 records argv `python3 .ufo/evidence/round-18/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 4b7c6823… --explain`, revision `4b7c6823…`, exit 0. No argv/revision mismatch observed.

## Remaining unknowns

- Whether a final same-ruler receipt at 55e was created after this evidence snapshot; none was found here. No selftest or ruler was run.
- No observed evidence that any real round-19 receipt contained NaN/Infinity. The falsifier is limited to the ruler’s documented parsing dependency, not a defect in the counted corrections.

No files outside this report were changed; no tools installed.