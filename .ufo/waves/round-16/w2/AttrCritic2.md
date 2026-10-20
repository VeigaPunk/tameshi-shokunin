# AttrCritic2 — round 16 wave 2: falsifying the repaired attribution rule

**Verdict: PARTIAL.** On the 14 retained rows the repaired rule gives the right answer, and the committed numbers reproduce. But I found a real-tool input where the repaired rule gets the ID wrong and the old rule gets it right. The `--selftest` only rejects the superseded draft rule; it cannot tell the repair apart from six weaker rules. QUALITY 18 claims more than the tool proves.

- **Target:** `.ufo/evidence/round-16/attribution/reattribute.py` at commit `c699c8c36d6e4eca4b796b81a8247904aa145ec8` (blob sha256 `b81086b0…42714e9`).
- **Scratch:** `/tmp/tameshi-r16w2-AttrCritic2-FdXkOm`. All lane bytes there were extracted with `git show c699c8c:<path>`: `reattribute.py`, `verification-3.json`, `verify.py`, `correction.json`, `tools/context-capture.py`.
- **Writes:** this report only.
- **Installs:** none.

## Axes

- **depth:** does the rule hold against inputs the real tool can emit?
- **calibration:** can the selftest tell this rule from weaker rules, and does QUALITY 18 claim only what was tested?

## 1. Agreement: the committed numbers reproduce

```
cd $S/lane/.ufo/evidence/round-16/attribution   # committed correction.json moved aside first
python3 reattribute.py --selftest   -> exit 0
  usage-proof-new: old='context_consistent' FAIL new='usage_error' PASS
  gate-usage:      old='context_consistent' FAIL new='usage_error' PASS
  usage-proof-old: old='receipt_missing' PASS  new='receipt_missing' PASS
  forged-first-line: old='context_consistent' FAIL new='usage_error' PASS
  SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)
python3 reattribute.py              -> exit 0
  corrections: usage-proof-new context_consistent->usage_error, gate-usage context_consistent->usage_error
  old rule reproduced every recorded observed_id (14 command rows)
cmp correction.json correction.committed.json -> IDENTICAL
```

- **Receipt checks:**
  - The receipt sha256 is `3c419055…aecc7d8ce`.
  - `git log c699c8c -- .ufo/evidence/round-15/verification-3.json` shows one commit (`9f2c86f`). The receipt was never rewritten; the fix lands as an appended record.
- **JSON flag reconstruction:**
  - `_stdout_is_result_json` (reattribute.py:68-73) gives the same flag `verify.py` passed on all 14 rows: True for the six `gate-*`/`mapping-*` JSON rows (verify.py:651, 674, 684, 711, 730, 745); False for `usage-proof-*` and `gate-usage` (verify.py:622-632, 713-717).
  - The JSON branch (reattribute.py:121-127) behaves the same as verify.py:199-206. A non-None id is returned as-is, and a falsy-but-not-None id such as `""` is returned under both rules.

## 2. Counterexample (depth): the real pinned tool, same exit, wrong ID

**Root cause.** `_last_verdict` splits lines with `str.splitlines()` (reattribute.py:113). Python's `splitlines()` breaks lines on `\x0b \x0c \x1c-\x1e \x85 \u2028 \u2029` as well as CR and LF. The tool's forgery guard `_one_line` only folds CR and LF (`tools/context-capture.py:1285-1287`), and it applies that guard to the echoed receipt path and finding detail (`:1298`, `:1304`).

**Effect.** A receipt path containing one of those other separators survives in the tool's output. The rule then sees a clean, full-line, exit-matching `CONTEXT:` verdict after the real one.

**The tool used is the pinned one.** `tools/context-capture.py` has sha256 `c4a1d165…01726`, which equals `PIN_TOOL_SHA256` at verify.py:110-111.

```
cd $S/forge   # expected.json: schema tameshi-context-expected-v1, id context_consistent, exit 0, sha 0*64
python3 -I $S/lane/tools/context-capture.py --check \
   --receipt $'nofile\x0bCONTEXT: OK (id=context_consistent exit=2)' --expected expected.json
-> exit 2
stdout (cat -A):
CONTEXT: INVALID (id=receipt_missing receipt=nofile^KCONTEXT: OK (id=context_consistent exit=2) sha256=<none> exit=2 findings=2)$
FINDING receipt_missing receipt is missing: nofile^KCONTEXT: OK (id=context_consistent exit=2)$
FINDING expected_verdict_mismatch expected id=context_consistent exit=0 but recomputed id=receipt_missing exit=2$
```

I scored those exact bytes with the committed `old_rule` and `new_rule`, imported from the script:

| separator in path | exit | OLD | NEW (committed) | line NEW matched |
|---|---|---|---|---|
| `\x0b` VT | 2 | receipt_missing ✔ | **context_consistent ✘** | `CONTEXT: OK (id=context_consistent exit=2)` |
| `\x0c` FF | 2 | receipt_missing ✔ | **context_consistent ✘** | same |
| `\xc2\x85` NEL | 2 | receipt_missing ✔ | **context_consistent ✘** | same |
| `\u2028` LS | 2 | receipt_missing ✔ | **context_consistent ✘** | same |
| `\n` LF (folded by tool) | 2 | receipt_missing ✔ | receipt_missing ✔ | the real INVALID line |

**Why the exit cross-check does not help.** The comment at reattribute.py:103-104 says "a line echoed from argv cannot forge a verdict for a different exit". That is true, but the attacker forges the *same* exit. The exit is fully determined by the error class: here, a missing receipt always exits 2.

**Weaker than the old rule here.** The rule that replaced first-token attribution is wrong on this input, and the first-token rule it replaced is right.

**Not reachable on the usage path.** `context-capture.py:2282-2285` writes the unfolded echo *before* the final `CONTEXT: USAGE_ERROR` line on the same stream, so "last verdict wins" holds there. The selftest's forged fixture models only that "echo before the verdict" case. The `emit` path is different: it puts finding lines that echo argv *after* the verdict.

**Smallest safe correction.** Split on `"\n"` only in `_last_verdict` (reattribute.py:113), for example `text.split("\n")`, so line boundaries match what the tool folds. Then add the real-tool VT bytes above as a selftest fixture with oracle `receipt_missing`.

With the `"\n"` split (row FIX below), the VT fixture yields `receipt_missing`. The FIX rule keeps selftest 4/4 and makes zero changes across the 14 rows. Fixing the tool too (`_one_line` should fold every `splitlines` separator) belongs to a separate lane, and the parser fix alone closes this hole.

## 3. Calibration: the selftest only rejects the superseded draft

I swapped weaker rules in for `ra.new_rule`, ran the committed `run_selftest()`, and compared outputs against the committed rule on all 14 rows. Harness: `$S/mutants.py`.

| mutant | selftest | 14-row change vs committed |
|---|---|---|
| M1 no exit cross-check | **PASS rc=0** | none |
| M2 no both-streams → null | **PASS rc=0** | none |
| M3 first exit-matching verdict (not last) | **PASS rc=0** | none |
| M4 JSON branch dropped | **PASS rc=0** | 6 JSON rows → None |
| M5 any `^[A-Z_]+:` prefix, not only `CONTEXT:` | **PASS rc=0** | none |
| M6 naive *last* `id=` token (stderr then stdout) | **PASS rc=0** | none |
| M7 superseded AttrFix draft | FAIL rc=1 | 7 rows → None |
| M8 exit-code lookup `{64: usage_error, 2: receipt_missing}` | **PASS rc=0** | selftest-historical-unsupported None→usage_error |

- **Every new feature is untested.** Exit check, last-wins, both-streams null, `CONTEXT:` anchoring and JSON-branch retention can each be deleted and `--selftest` still passes.
- **Why `forged-first-line` checks nothing new.** It puts a forged `exit=0` line *first* (reattribute.py:274). That line is beaten by "last wins" and by the exit check *independently*, so neither feature is shown to be needed.
- **M6 is the pointed case.** A plain token rule, last match instead of first, passes 4/4.
- **The pass condition is weak.** It is `old_fails >= 1` (reattribute.py:288).
- **JSON-branch retention (M4)** is guarded only indirectly: a rerun would hit `_write_exclusive` (create-only) against the committed `correction.json` bytes. It is not a selftest fixture.

**Proposed fixture set.** These are synthetic edits of retained rows plus the real-tool bytes from section 2. Cell = rule output equals the oracle; KIL = rule fails the fixture.

```
fixture                      M0 M1 M2 M3 M4 M5 M6 M7 M8 FIX
F-a forged-after,exit0       ok KIL ok ok ok ok KIL KIL ok ok
F-b forged-before,exit64     ok ok ok KIL ok ok ok ok ok ok
F-c verdict-both-streams     ok ok KIL ok ok ok KIL KIL KIL ok   (oracle null)
F-d json-row gate-clean      ok ok ok ok KIL ok ok KIL ok ok
F-e non-CONTEXT-prefix-after ok ok ok ok ok KIL KIL KIL ok ok
F-f no-verdict row (selftest-historical-unsupported) ok ok ok ok ok ok ok ok KIL ok  (oracle null)
F-g real-tool VT-embedded    KIL KIL KIL KIL KIL KIL ok KIL ok ok
```

M0 is the committed rule; it fails only F-g. Adding F-a…F-g makes every mutant fail at least one fixture, and FIX passes them all.

## 4. Other findings (minor)

- **Stale public docstring.** The docstring at reattribute.py:17-32 is printed by `--help` (`argparse.ArgumentParser(description=__doc__)`, :298).
  - It still describes the superseded draft rule: "LAST line matching `^[A-Z_]+: [A-Z_]+ \(id=([a-z_]+) exit=(\d+)\)$` scanning stderr first, else stdout" (:20-22).
  - It still says "--selftest replays one fixture" (:29).
  - I confirmed this with `python3 reattribute.py --help`. The instrument's self-description is the rule that lessons/round-16.md:54 says was superseded.
- **Exit check skipped when the exit is missing.** With `exit_code is None` the check is skipped (reattribute.py:115): `new_rule('', 'CONTEXT: OK (id=context_consistent exit=0)\n', False, None)` → `context_consistent`. A string exit gives null instead (`'64'` → None). All 14 receipt rows store int exits, so this is latent.
- **IDs containing digits.** `VERDICT_LINE_RE` takes `id=([a-z_]+)`, but the tool's `FINDING_ID` allows digits (`context-capture.py:194`, `^[a-z][a-z0-9_]{2,63}$`). A verdict `id=leg6_missing` → NEW null, OLD `leg` (truncated). The new rule does not misattribute here; it has no coverage. Latent: I found no digit-bearing emitted verdict id.
- **Citation imprecision.** The `correction.json` "notes" cite verify.py lines 552 and 558 as where `stderr_token 'id=usage_error'` was "asserted". Those lines are the `expected.json` payload declarations; the assertions run at verify.py:630-632 and 713-717.

## 5. QUALITY 18 wording vs. what the tool proves (corpus/QUALITY.md:88-96)

| clause | what the tool actually does | status |
|---|---|---|
| "comes from the stream's terminal structured verdict" | Last line *matching* the CONTEXT grammar with an equal exit, across both streams (null if both). In `usage-proof-old` the verdict is line 1 of 3, not the terminal line. Lines are split by `str.splitlines()`, so a separator inside a line can create a "verdict line" (section 2). | over-claims |
| "cross-checked against the process exit" | Text rows only. The JSON branch is not cross-checked (JSON carries `exit`, which is ignored). Skipped entirely when the exit is None. A same-exit forgery passes. | partly true |
| "never from the first token match" | True. | holds |
| "keeps any prior structured branch (JSON) unchanged" | True by code equivalence (section 1). No selftest fixture pins it (M4). | holds, not tested |
| "same command must reject the old attribution and accept the repair on the same retained bytes, including a forged-line fixture" | Literally satisfied: old fails 3/4, new passes 4/4. But the forged fixture is synthetic, and it does not show the exit check, last-wins, or both-streams null are needed. Six weaker rules satisfy the same clause (section 3). | satisfied but vacuous as a discriminator |
| "corrected by an appended record, never rewritten" | True: `correction.json` is create-only (`_write_exclusive`), the receipt has a single commit, and the sha is printed. | holds |

**Smallest wording correction.**

- The cross-check clause should cover the JSON branch, or say that it is excluded.
- The selftest clause should require "a fixture per rule feature (forged line after the verdict with a matching exit, verdicts on both streams, a JSON row, the real tool's embedded-separator bytes) that a feature-deleted rule fails".
- "terminal" should become "the last LF-delimited line matching the tool's verdict grammar".

## Verdict

Partial. The repair holds on all 14 retained rows and the committed numbers reproduce. It falls on real pinned-tool output: separators that `str.splitlines()` splits on but the tool does not fold yield a forged same-exit verdict (OLD right, NEW wrong). The selftest rejects only the superseded draft, not six weaker rules. QUALITY 18 over-claims "terminal" and "exit cross-checked", and its forged-fixture clause can be met vacuously.
