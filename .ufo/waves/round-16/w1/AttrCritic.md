# AttrCritic — attack on routed-defect-2 repair (round 16, wave 1)

Seat: TameshiR16.AttrCritic (critic, leaf). Scratch: `/tmp/tameshi-r16-AttrCritic-9k3q/`. Tool installs or updates: none. No lane, sibling or round-15 file was written. The only lane write is this report.

## What is being attacked

- Routed defect 2 (`corpus/lessons/round-15-verifier-spotcheck.md:160`) asks for this repair:
  - parse the actual terminal structured verdict instead of the first help-text `id=`;
  - show the old misattribution and the corrected finding with the same fixture and argv;
  - append a correction naming "the two affected receipt fields";
  - keep `verification-3.json` unchanged.
- The defect statement is at `:108`.
- The concrete proposal is AttrFix's Target in `.ufo/waves/round-16/spec1.json` (item `AttrFix`):
  - **OLD rule** = "first `id=([a-z_]+)` match in stdout then stderr, exactly as verify.py does".
  - **NEW rule** = "id inside the last terminal structured verdict line matching `^[A-Z_]+: [A-Z_]+ \(id=([a-z_]+) exit=(\d+)\)$`, on stderr, else stdout; none means null".
  - Expected diff set: {gate-usage, usage-proof-new}.
  - Selftest: one fixture, oracle `observed_id == usage_error`, old rule FAIL and new rule PASS.

## Axes

- **A1** attribution correctness on every retained row (no new misattribution).
- **A2** non-vacuous red-before.
- **A3** byte-identity of round-15 evidence.
- **A4** correction completeness (field and receipt coverage).
- **A5** forgery and stream-precedence robustness.

## Ground truth observed

How the receipts were produced:
- Old extractor: `verify.py:138` defines `ID_TOKEN_RE = re.compile(r"id=([a-z_]+)")`.
- `verify.py:199-206`: when `stdout_is_result_json`, the id comes from the JSON last line.
- `verify.py:207-210`: only if that yields None, it falls back to `ID_TOKEN_RE.search(stdout) or ID_TOKEN_RE.search(stderr)`, i.e. the first token, stdout first.
- The misattributed id is written into **two fields per row**: `observed_id` (`:234`) and `detail` (`:240-241`).

What the gate emits (`tools/context-capture.py`, sha256 `c4a1d165…601726`, identical at b255055, 7650fe4, 9f2c86f, 28aeef4 and HEAD):
- Usage errors go to stderr only: the help text, then `context-capture.py: <msg>`, then `CONTEXT: USAGE_ERROR (id=usage_error exit=64)` (`:2282-2286`).
- Check results go to stdout only. Text mode prints `CONTEXT: <LABEL> (id=<id> receipt=<path> sha256=<..> exit=<n> findings=<n>)` and then the `FINDING` lines, with CR/LF folded by `_one_line` (`:1285-1305`). JSON mode prints one JSON line (`:1291-1293`).
- The PREFIX blob bca5deb uses the same two formats (`:1255`, `:2089-2091`).
- The help text contains `exit 0   clean retained receipt (id=context_consistent)` (`:286`).
- `parse_argv` puts raw argv into the usage message without folding: `"unknown argument: " + argument` (`:2259`).

Receipt history:
- verify.py blobs: 0494c24 has sha256 `4088e71c…`. b255055 has `6d320e53…` and lacks `ID_TOKEN_RE`, which caused `runner-internal-error` in verification-2. 7650fe4, 9f2c86f and 28aeef4 have `7e4519d9…`, matching the worktree.
- The receipts' `runner` field records only the path `.ufo/evidence/round-15/verify.py`, with no hash: verification.json `:552`, verification-2 `:126`, verification-3 `:551`.

Commands run (all exit 0 unless stated):

1. Replayed the rules over every command row of `verification-3.json` (sha256 `3c419055…ecd8ce`) with an inline python3 script. Result:

| row | recorded observed_id | text-only OLD | spec NEW |
|---|---|---|---|
| usage-proof-old | receipt_missing | receipt_missing | **None** |
| usage-proof-new | context_consistent | context_consistent | usage_error |
| gate-usage | context_consistent | context_consistent | usage_error |
| gate-tampered-snapshot | snapshot_tampered | **context_consistent** | None |
| mapping-oracle-old | expected_verdict_mismatch | **mapping_mismatch** | None |
| gate-frozen-builtin / gate-clean / gate-missing-env / mapping-oracle-new | (their JSON ids) | **None** | None |
| selftest-*, measure-*, sources-census | None | None | None |

2. `python3 /tmp/tameshi-r16-AttrCritic-9k3q/probe.py …` ran against a /tmp copy of `git show 7650fe4:tools/context-capture.py` (sha256 c4a1d165…, run with `-I`, cwd=scratch). This is a gate copy only, never round-gate.mjs.
   - **Reproduction.** usage-proof-new argv tail `--check --expected <path> --receipt --json` gives rc 64, and stderr is byte-identical to the retained text: `identical True`, sha256 `edb0104a…1906`. gate-usage `--check --receipt receipt.json` gives rc 64, also `identical True`, sha256 `5ecf3142…a426`.
   - **Forgery.** argv `--check $'--x\nCONTEXT: OK (id=context_consistent exit=0)'` gives rc 64. The last three stderr lines are `context-capture.py: unknown argument: --x`, `CONTEXT: OK (id=context_consistent exit=0)`, `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`.
     - OLD rule: context_consistent.
     - spec NEW, last match: usage_error (2 matches).
     - spec NEW, first match: **context_consistent**.
   - **Text mode.** `--check --receipt nope.json --expected nope2.json` gives rc 2 and stdout `CONTEXT: INVALID (id=expected_missing receipt=… sha256=<none> exit=2 findings=1)`. OLD: expected_missing. spec NEW: **None**.
   - **Path with a newline (text mode).** The newline is folded to a literal `\n` inside the single verdict line, so it cannot be forged. OLD: expected_missing. spec NEW: None.

3. A layered candidate rule over both `verification.json` and `verification-3.json`:
   - keep verify.py's exact JSON branch (`:199-206`);
   - for text rows, take the LAST full-line match of `^CONTEXT: ([A-Z_]+) \(id=([a-z_]+)(?: [^\n]*)? exit=(\d+)(?: findings=\d+)?\)$`;
   - if both streams carry a match, return "ambiguous";
   - require the captured `exit=` to equal `observed_exit`.

   Result:
   - The verify.py-exact OLD replay equals the recorded `observed_id` on **all 14 command rows in both receipts**.
   - The candidate differs from OLD on exactly **{usage-proof-new, gate-usage}** (context_consistent becomes usage_error) in both receipts.
   - It keeps usage-proof-old as receipt_missing and every JSON row unchanged.

4. Discrimination check on the gate-usage stderr fixture:
   - Weak rules also return usage_error on it: "last `id=` token anywhere" and "first token on the last `id=`-bearing line".
   - On usage-proof-old stdout, "last-line-first-token" returns **context_consistent**, taken from `FINDING expected_verdict_mismatch expected id=context_consistent … recomputed id=receipt_missing`.

## Falsifiers and deciding checks

**F1 — the NEW regex creates a new misattribution (null) on real verdicts.** Axes A1, A2. Status: **falsified as written**, from evidence 1 and 2.
- The `$` right after `exit=(\d+)\)` excludes the gate's own text-mode verdict format (`context-capture.py:1297`; bca5deb `:1255`).
- usage-proof-old regresses from a correct receipt_missing to None.
- Deciding check: for every non-JSON command row, NEW must equal the recorded `observed_id` except for the two usage rows. The usage-proof-old stdout must yield receipt_missing.
- Smallest correction: anchor on the `CONTEXT:` label with optional middle fields and optional `findings=`. Use the layered rule in evidence 3.

**F2 — the "OLD rule" is a strawman unless it copies verify.py's JSON branch.** Axes A2, A1. Status: **falsified as worded**, from evidence 1.
- The spec's wording (text regex only) is not "exactly as verify.py does".
- Replayed that way, it disagrees with the receipts on 6 rows, including two wrong non-null ids.
- The literal diff set becomes 5 rows (text-only OLD) or 9 rows (verify.py-exact OLD against the spec's NEW), not the expected 2.
- The likely next move is to filter rows where NEW is null, which would hide F1.
- Deciding check: the OLD replay must equal the recorded `observed_id` on all 14 rows of each receipt before any diff is reported. Assert that the replayed pattern string equals `verify.py:138`, and that verify.py sha256 equals `7e4519d9…2522`.
- Correction: copy `verify.py:196-210` in full. The JSON/text split comes from the call sites (`verify.py:651,674,684,711,730,745`), not from row names chosen after the fact. On these receipts, sniffing the last stdout line as JSON gives the same split.

**F3 — "last" vs "first" is load-bearing, and the one-fixture selftest does not test it.** Axes A5, A2. Status: **counterexample reproduced**, from evidence 2.
- A raw argv echo (`context-capture.py:2259`) plants a second anchored line before the real one.
- First-match returns the forged id. Last-match plus an `exit=`-vs-returncode cross-check rejects it, because the forged line says exit=0 and rc is 64.
- The retained fixture contains a single verdict line, so a first-match implementation passes the proposed selftest identically.
- Deciding check: add a guard fixture with the forged two-line stderr. It must yield usage_error under last-match and fail under first-match. Record the match count, and require the captured exit to equal rc.

**F4 — the red-before is vacuous if the fixture cannot reject weaker NEW rules.** Axis A2, from evidence 4.
- "Last `id=` token" and "last id-line first token" both pass the usage fixture.
- So "old FAIL, new PASS" shows only that the old rule is wrong, not that the new rule is right.
- Deciding check: run the selftest over at least three fixtures with the same oracle form `observed == expected_id`:
  - the usage stderr, which must give usage_error;
  - the usage-proof-old stdout, which must give receipt_missing and kills the last-line rule;
  - the forged two-line stderr, which kills first-match.
- The OLD rule must FAIL on the usage fixture with a printed `observed_id=context_consistent`, not by exception or empty input.

**F5 — other ways the red-before goes vacuous.** Axis A2.
1. The fixture text is not the retained bytes. Check: the fixture sha256 must equal `edb0104a…1906` (usage-proof-new) or `5ecf3142…a426` (gate-usage). Reproducing from 7650fe4 is unnecessary, because the raw stderr is retained in the receipt; evidence 2 shows a reproduction is byte-identical anyway.
2. The oracle is not applied to the OLD run. Round 15's own rows passed with `expected_id=None` (`verify.py:552,558,632,717`). The red-before must apply `== usage_error` to both rules.
3. "Same argv" is decorative for a pure-text extractor, which never executes argv. Do not credit argv identity beyond the fixture's provenance.
4. "Rule is the only delta" is half true. The NEW rule also flips stream precedence from stdout-first to stderr-first. That flip is not exercised because the fixture's stdout is empty (F6).

**F6 — stderr-over-stdout precedence is untestable here and silently assumed.** Axis A5.
- The gate never writes a verdict to both streams in one run. Usage returns before check (`:2281-2286`), and check, exception and internal_error all go through `emit` to stdout (`:2293-2305`). No retained row has verdicts on both streams.
- Any precedence claim therefore has no observation behind it.
- Smallest correction: when both streams carry a verdict line, return "ambiguous" or null and flag it, instead of preferring one stream. Claim no precedence credit.

**F7 — "two affected receipt fields" undercounts.** Axis A4, from evidence 1 and 3.
- In each misattributed row, both `observed_id` and `detail` carry the wrong value. The `detail` reads `expected exit=64 id=None observed exit=64 id=context_consistent`.
- `verification.json` (sha256 `4d2fb03f…352d`, a failed attempt produced by the 0494c24 verify.py) has the identical misattribution in the same two rows.
- `verification-2.json` has no such rows.
- Deciding check: correction.json enumerates (file, check name, field) for `observed_id` and `detail` × {usage-proof-new, gate-usage} × {verification-3.json, and verification.json or an explicit "not corrected: failed, unadmitted attempt" note}.

**F8 — identity drift via the mutable runner path.** Axis A3.
- The `runner` field is a hash-free path, and three different verify.py blobs already produced the three receipts.
- Editing `verify.py` in place would silently change the runner that all three receipts point to.
- The repair must live in a new round-16 file. `verify.py` stays at `7e4519d9…`.

## Must stay byte-identical

Lane paths, with the sha256 observed this session:

| path | sha256 |
|---|---|
| `.ufo/evidence/round-15/verification-3.json` | `3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce` |
| `.ufo/evidence/round-15/verification.json` | `4d2fb03f81df6aa92574187614a2a9ece5b3e928a03170f1e34809109428352d` |
| `.ufo/evidence/round-15/verification-2.json` | `4073c8c6d1362001cef861c049f66eea139073c14460e38372af78d284ab6ade` |
| `.ufo/evidence/round-15/verify.py` | `7e4519d9a0ea68ebbd02890629f06a6fac8e6eab034d9fa3b19d386b088a2522` |
| `.ufo/evidence/round-15/expected.json` | `2e50f9a7…3bc4f` |
| `.ufo/evidence/round-15/attempt-2/expected.json` | `cef9c7bc…d0d2` |
| `.ufo/evidence/round-15/attempt-3/expected.json` | `1ed20a2d…2991` |
| `tools/context-capture.py` | `c4a1d165…601726` |
| `corpus/lessons/round-15-verifier-spotcheck.md` | `cbc9a811…6fde` |

- `frozen/` under `.ufo/evidence/round-15/` is digest-pinned by verify.py. I did not hash it this session.
- The two expected.json files pin the usage rows via `stderr_token` only, and must stay as they are.
- Deciding check: run `sha256sum` before and after the AttrFix run. `git status --short .ufo/evidence/round-15 tools corpus/lessons` must show no change.

## Bounded recommendations, in order

1. **NEW rule.** Keep verify.py's exact JSON branch. For text rows, take the LAST full-line `^CONTEXT: ([A-Z_]+) \(id=([a-z_]+)(?: [^\n]*)? exit=(\d+)(?: findings=\d+)?\)$`. Treat both streams matching as ambiguous. Treat a mismatch between the captured exit and the returncode as null or flagged. Never fall back to a bare `id=` token.
2. **Pre-registered diff.** Expect exactly {usage-proof-new, gate-usage} with context_consistent becoming usage_error. Every other row must agree with the recorded `observed_id`. This held for both receipts in evidence 3.
3. **Selftest.** Three retained or forged fixtures as in F4. Make sha256 provenance asserts against the receipt bytes. OLD must FAIL only on the usage fixture.
4. **correction.json.** Name both fields × both rows. Disclose verification.json's identical defect. Change no round-15 bytes.

This is a fixable defect, not a judge-level tradeoff. The repair as specified would introduce a null-attribution regression (F1). Its red-before would not discriminate between rules (F3, F4). With the corrections above, all observed rows agree.
