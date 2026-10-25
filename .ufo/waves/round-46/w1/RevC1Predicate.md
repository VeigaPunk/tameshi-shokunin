seat: RevC1Predicate
item: Three-way audit of the C1 calibration claim — contract `statement`/`target` vs the frozen predicate in `.ufo/evidence/round-46/calibration/measure.py` vs the printed receipt label `C1_R46_PASS` — with statements-list enumeration, first-cell confirmation over SCORECARD.md, AXES.md/prompt-§9 rule check, and receipt reproduction at the freeze rev.

## 1. Side-by-side quotes

- **Contract `claims.C1.statement`** (contract.json): "At REV the standing SCORECARD rows of all 22 frozen statements state exactly the value, exit code and tool sha256 prefix that the statement's frozen command prints at REV: mismatches + unparsed + unobservable = 0, the base SCORECARD.md stays a byte prefix, and the counter, its statements list (sha256 pinned) and its selftest are committed at REV."
- **Contract `claims.C1.target`**: "C1_R46_PASS=true: self_pin=1 stmts_pin=1 statements=22 append_only=1 total=0"
- **Frozen predicate** (measure.py docstring, lines 4-16): "C1_R46_PASS=true iff self_pin=1, stmts_pin=1, statements=22, append_only=1 and mismatches=0, where mismatches = statements whose standing row is absent or unparseable (`unparsed`), whose frozen command printed no matching line (`unobservable`), or whose standing row states a value different from what the command prints at REV (`mismatch`)." Plus the cap/axis split: "For a `cap` row the claim is the evidence cell's `CMD` → `PRINTED LINE`, exit N[, tool sha256 `12 hex`] ... compared whole ...; for an `axis` row the claim is the integer in the score cell".
- **Printed receipt label** (measure.py:230-232): `C1_R46: self_pin=%d stmts_pin=%d statements=%d mismatches=%d unparsed=%d unobservable=%d append_only=%d total=%d rev=%s C1_R46_PASS=%s`, with `passed = (self_pin == 1 and stmts_pin == 1 and len(statements) == n_expected and append_only == 1 and total == 0)` (measure.py:226) and `N_STATEMENTS = 22` (line 30).

**Verdict: same claim.** The target's five fields {self_pin, stmts_pin, statements, append_only, total} are exactly the `passed` conjunction and are a subset of the receipt's fields; `total` is printed as `mism + unparsed + unobs` = the contract's "mismatches + unparsed + unobservable"; the docstring's "mismatches=0" is defined as that same union. All three renditions are extensionally identical. Same statement — no drift found.

## 2. Universal-word audit (prompt section 9, "Claim sizing")

Prompt §9 is campaign-addendum item 9 at `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-46.md:417`: "Use no universal clauses ('all', 'complete', 'every', 'no harm anywhere') unless the counting command enumerates the full set."

- The only universal in the statement/target is **"all 22 frozen statements"** — and the set is enumerated: `statements.json` holds exactly 22 entries (`python3 -c json.load(...)` → `count 22`), sha256 `a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9`, which equals both the contract's `statements_sha256` and `measure.py`'s `STATEMENTS_SHA256`; the counter iterates every entry and enforces `len(statements) == 22` (T16 kills a 21-entry list: `C1_R46_PASS=false`). Compliant.
- Kinds confirmed: 19 `cap` + 3 `axis` (`depth`, `calibration`, `freshness`) — matches the contract surface "19 capability rows, depth, calibration, freshness axis rows". No duplicate ids (`dup ids: 0`); ids unique per `(kind,id)`.
- "exactly the value, exit code and tool sha256 prefix" — comparison is exact tuple equality (`tuple(claimed) == tuple(observed)`); selftests T2/T3/T4/T5 each kill one altered component.

## 3. First-cell enumeration over SCORECARD.md

Ran `measure.py`'s `last_rows` over the worktree `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md` (byte-identical to freeze `745a5831`'s and base `683eedde`'s SCORECARD.md — all three 207,916 bytes, `cmp` clean; worktree is a byte prefix of freeze: `startswith=True`):

- Parsed standing rows: **21 of 22** — every statement id has a first-cell row in a kind-matching table except `(axis, freshness)`.
- Raw-text check: all 22 ids occur as first cells of *some* table (`ids with zero first-cell occurrences in raw SCORECARD: []`). `freshness` is the first cell of 8 tables whose headers are `| Axis | <round> lane verdict | ...` (SCORECARD.md lines 111, 187, 325, 388, 445, 540, 591, 629) — those headers fail the frozen kind rule (header cell 2 must begin `Score`; the only qualifying axis tables are lines 64 and 1534), so the parser ignores them by design and freshness's standing row is genuinely absent at freeze.
- This absence is the before-state, not a counter defect: `before/c1-at-freeze.stdout` marks `axis/freshness: claimed=- ... UNPARSED`, and the append-only clause forces the fix to be an appended row in an axis-kind table at REV. Consistent.

## 4. Axis-rule compliance (AXES.md + prompt §9)

- AXES.md:15: calibration = "SHONEN.md/SCORECARD entries match observed repo state". Prompt §9: "A calibration claim must count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state. It cannot be an assertion."
- C1 is a mismatch count, not an assertion: it measures `total = mismatches + unparsed + unobservable` over 22 enumerated standing rows, before 21 → target 0, with kill rule "total > 0 or stmts_pin=0 or append_only=0 = honest miss". The do-nothing control (unchanged freeze tree) scores `C1_R46_PASS=false`, receipt committed. Compliant on both rules.

## 5. Before-state is a count — confirmed and reproduced

- `before/c1-at-freeze.stdout` final line: `C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=2 unparsed=19 unobservable=0 append_only=1 total=21 rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C1_R46_PASS=false` — a count, matching the contract's "total>0 and C1_R46_PASS=false".
- My reproduction (bounds-compliant seat run, scratch work dir `/tmp/tameshi-r46-RevC1Predicate/wk-freeze`): `python3 measure.py --lane <lane> --rev 745a5831... --base 683eedde... --work ...` — output **byte-identical to the committed receipt** (`diff` shows only my appended `freeze exit=1` marker; run exit 1 = PASS false, never a verdict). Per-statement breakdown agrees: 2 MISMATCH (`cap/six-leg regression ledger` — row quotes a `…`-truncated line vs printed `REGRESSION: PASS (cases=9 passed=9`; `axis/calibration` — claimed 8 vs observed 6), 19 UNPARSED (18 cap rows absent/unparseable + `axis/freshness` absent), 1 MATCH (`axis/depth` 9=9), 0 UNOBSERVABLE.
- Selftest: `--selftest` → `C1_R46_SELFTEST: cases=18 failed=0` / `VERDICT: PASS`, exit 0. Matches the committed `selftest/c1-selftest.stdout` case-for-case (per-case fixture revs differ between runs — throwaway temp-repo commits, expected nondeterminism; case names, wants and verdicts all match).
- Base-rev run (`--rev 683eedde...`): exits 2, stderr `C1_R46: statements.json absent at rev`, no verdict line — the counter cleanly refuses to measure the base rev (statements list first exists at freeze). So of the two bounds-permitted revs, only the freeze rev is measurable for C1; the base option is a clean hard stop, not a silent pass.

## 6. Findings by severity

**Blocking defects: none.**

Informational (wording, no adjudication risk):

1. **Literal over-cover in the contract sentence** — "state exactly the value, exit code and tool sha256 prefix" reads as if every row states all three components; in fact the 3 axis statements claim an integer only, and 2 of the 19 cap statements (`sources-registry`, `six-leg regression ledger`) have `sha_file=null`, so no sha component exists for them (confirmed in the receipt: their `observed` fields have no third part). The docstring states the split precisely ("for a `cap` row ... for an `axis` row the claim is the integer"), and the code (`CLAIM_SHA` vs `CLAIM_BASE`, `claim_of`) implements exactly that. The coded predicate is narrower than a hyper-literal reading of the sentence; target/label unaffected.
2. **"The same sentence" is the same predicate, not the same wording** — docstring line 3-4 calls the docstring text "the same sentence in the contract, here and in the receipt label"; the three renditions differ in wording (contract: three count nouns; docstring: iff-form redefining `mismatches` as the union; label: four separate counts + `total` + `rev`). Extensionally identical, so §9's intent (one freeze-proof predicate) is met; noting the literalism only.
3. **Parser minutiae, untriggered** — `tables()` unconditionally treats the line after a header as the separator (`block[2:]`), so a separator-less table would lose its first data row; fenced/HTML-comment blanking is non-greedy. Neither shape occurs in the frozen SCORECARD; T10/T11 cover the present forms.
4. **`unobservable` also swallows timeouts** (docstring says "printed no matching line"); semantically consistent, worth knowing when reading receipts.

## 7. Hygiene

- I created no scratch inside the lane; all scratch under `/tmp/tameshi-r46-RevC1Predicate/`. One slip, self-corrected: loading `measure.py` via importlib wrote an untracked `.ufo/evidence/round-46/calibration/__pycache__/measure.cpython-314.pyc` (18:18:30 today); I removed the directory (`rm -rf`), restoring the committed tree; `git status --porcelain` on the calibration dir is now clean. No tool installs (none needed; pacman untouched).
- Bounds respected: counter run only as `--selftest` or at the two permitted revs into empty scratch work dirs; never as a verdict; no lane mutations, no git/jj state changes.

## 8. Residual risk and verification gaps

- The deciding run (the L1's, at its REV with appended rows) is unobservable to me; my checks validate the counter at the freeze only. Whether the L1's appended rows state each command's exact printed line (incl. the `…`-truncation fix and the freshness axis row) is judged by that run, not by this seat.
- `append_only` is checked base→REV by `startswith`; a rewrite of SCORECARD.md history between base and freeze would not be caught by this seat (freeze SCORECARD == base SCORECARD byte-for-byte today, so the precondition holds now).
- The 22 frozen commands' own determinism (e.g. census `rows=117`, selftest counts) is inherited from the round-45/earlier fixtures and was not re-audited here beyond the freeze receipt reproduction.
