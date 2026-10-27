# T53W1Read15 — cold read of `### Round-15 gate/probe registry`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Content commit read: `a41195dfc13a73958e4c5228ec196b28d03ded03` (C*), read through `git show C*:SKILL.md` only (never the working tree).
- Section range at C*: lines **1683–1712** (splitter end-exclusive 1713), heading line `:1683`.
- `section_sha256` = `b814e0afbad4c270b5d2d973639df287e982be1dbfac9deae8d9444fb57c1620`.
- Boundary check: the frozen-monitor `sectionize` (`^#{1,3}(\s|$)` outside ``` fences; heading line through the line before the next heading; trailing whitespace-only lines stripped; `\n` join, no trailing newline) reports `start=1683 end=1713` for this heading at C*, and `git show C*:SKILL.md | sed -n '1683,1712p'` hashed after stripping the final newline gives the same sha256 (`b814e0af…`), so the range and the digest agree.
- Same splitter at base `6db1d220b337c35ff1e25bf9cfd74abc9db1498d` gives lines 1676–1705 with the **identical** sha256 `b814e0af…`: this section was not edited by the round's fix pass (`218bc6b`), so both findings below are inherited, not introduced this round.
- Findings: **2**. Both are present-tense statements that are true only at the round-15 write and are contradicted by SKILL.md itself at C*.

## Checks executed (command → observed outcome)

| # | Command | Outcome |
|---|---|---|
| 1 | `git -C … show C*:SKILL.md \| sed -n '1683,1712p' \| sha256sum` (newline-stripped) | `b814e0afbad4c270b5d2d973639df287e982be1dbfac9deae8d9444fb57c1620` — matches the JSON |
| 2 | `git show C*:.ufo/evidence/round-14/context-receipt.json \| sha256sum` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` — equals the sha256 quoted in the registry row |
| 3 | `git show C*:.ufo/evidence/round-14/context-missing-env.json \| sha256sum` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` — equals the "negative fixture" sha256 in the row |
| 4 | `git show C*:tools/context-capture.py \| grep -n …` | literal `05cb55b8…` at `:153`; `EXPECTED_SCHEMA = "tameshi-context-expected-v1"`; finding ids `context_consistent` 0, `missing_injected_environment` 1, `snapshot_tampered` 2, `usage_error` 64; `FROZEN_EXPECTED_ID`/`FROZEN_EXPECTED_EXIT` pins |
| 5 | `python3 tools/context-capture.py --check` | exit **0**, `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b8… exit=0 findings=0)` |
| 6 | `python3 tools/context-capture.py --selftest` | exit **0**, `SELFTEST: PASS (49/49)` |
| 7 | `python3 tools/context-capture.py --check --bogus` | exit **64** (invalid invocation) |
| 8 | `python3 tools/context-capture.py --help` | exit **0** |
| 9 | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` | exit **0**, `effective 11 / superseded 1 / failed 0 / findings 0` — the row's "Live entry … → 0" holds |
| 10 | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | exit **2**, `id=expected_input_digest_mismatch`, detail `tools/bash-witness-study.py: observed cca77724… expects 49e9e5e2…` — the row's "superseded … returns 2 `expected_input_digest_mismatch` at `--root .`" holds |
| 11 | `git archive 28aeef4 \| tar -x -C <scratch>` then, in that cwd, `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | exit **0** (`effective 11 / superseded 1 / failed 0`) — the row's "frozen replay: cwd = extracted `git archive 28aeef4` → 0" holds; `28aeef4` resolves to commit `28aeef498cc070c3183271b709bc79d344ff547a` ("round-15 verifier spot-check …") |
| 12 | `python3 tools/evidence-disposition.py --selftest` | exit **0**, `SELFTEST: PASS (66/66)` (row's self-test command) |
| 13 | `python3 tools/evidence-disposition.py` (no args) / `--help` | exit **64** / exit **0** — matches "64 usage" and "Help exits0 only as a non-verdict informational mode" |
| 14 | pin comparison `.ufo/evidence/round-14/dispositions.json` inputs vs blobs at C* | 3/3 MATCH (`round-13/expected.json`, `producer-oracle-repair.json`, `verification.json`) |
| 15 | pin comparison `.ufo/evidence/round-13/expected.json` inputs vs blobs at C* | 13 inputs, 10 MATCH, 3 DRIFT (`tools/bash-witness-study.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`) — the runner input did move; the "because the runner input moved" clause is true though incomplete (see below) |
| 16 | `git show C*:SKILL.md \| grep -n 'Recorded case\|recorded case —'` | `:1761  ## Seventh recorded case and full-page cold-read — round 16`, `:1912  ## Eighth recorded case — round 18`, `:2111  ## Ninth recorded case — round 26` |
| 17 | `git show C*:SKILL.md \| sed -n '1398p'` | runner row: "`--selftest`, `--regression` (six-leg registry at round 11, seven since round 16, eight since round 18, nine since round 26, ten since round 51 …)" |
| 18 | `git show C*:tools/mutate-and-run.sh \| grep -n kumitate…` | legs `js-round-gate` / `js-sources-check` / `js-cite-check` are kumitate `scripts/*.mjs` (context for the consideration below) |

## Holds (each pointer checked against C* bytes)

- **Row `retained invocation-context gate`.** Entry command, verdict map, self-test command, receipt pin and its built-in id/exit pin all resolve at C* (checks 1–7). Write-scope claim "check … writes nothing, never opens recorded root paths or executes stored argv" matches the tool: `--check` produced only the verdict line and the tool's docstring states "Check mode writes nothing; the only writes are --selftest fixtures under mkdtemp"; `grep -n 'O_NOFOLLOW|symlink|lstat'` finds none, so the paragraph's "Paths can follow filesystem symlinks: digest binding verifies the bytes read, not filesystem-origin authenticity or a race-free confinement boundary" also holds.
- **Row `effective expectation disposition`.** Entry command → exit 2 `expected_input_digest_mismatch` (check 10); live entry with `.ufo/evidence/round-18/dispositions.json` → exit 0 (check 9); frozen replay at `git archive 28aeef4` → exit 0 (check 11); self-test → 66/66 PASS (check 12); "0 clean; 1 failed semantic expectations; 2 and 64 could-not-evaluate" matches the tool's `USAGE` exit map (`:173-178`) and `main()` (`:3194-3221`); "selftest isolated temporary fixtures" matches `mkdtemp` usage.
- **"see the round-17 re-pin section".** Exists at C*: `## Live-tree re-pin and entry-command monitor — round 17` (`:1821`) and `### Round-17 gate/probe registry — re-pin and monitor` (`:1853`).
- **"the Gate standard's \"Two evidences\"".** Resolvable in-lane: `:1744 | 1614 | PROTOCOL.md §Gate standard | ../PROTOCOL.md (fleet root; the lane holds none) | CR27 |`, and the fleet-root `PROTOCOL.md:390` reads `- **Two evidences.** …` (read-only read outside the lane).
- **"Could-not-evaluate takes precedence …; a clean result with a wrong id/exit pin becomes failed/exit1."** Matches the tool's stated precedence ("Pinned-verdict precedence … converts a clean 0 into 1; on an exit-1 or exit-2 result it is a secondary finding"; "Tamper, malformed and other could-not-evaluate results never become exit 1").
- **"Selftest reads its own source for the reported tool digest, not live domain artifacts."** Matches the tool header ("Each subprocess reads its own tool source only to report tool_sha256; no live domain inputs or live lane path are read").
- **"the archived round-12–14 bytes" / "archived round-14 bytes retained".** `.ufo/evidence/round-14/capture-context.py` is present at C*, and the round-12/13/14 evidence trees resolve.
- **"historical expected pins13 original inputs".** `.ufo/evidence/round-13/expected.json` carries exactly 13 `inputs` keys (check 15). The substance holds; the missing space is cosmetic (see observations).
- **"the disposition selftest: 0 pass, 1 case failure or an uncaught setup traceback; round 17".** `main()` returns `selftest()` outside its try/except, so an uncaught setup traceback exits 1; per-case setup errors are recorded as failures and return 1; round 17 commit `eb7838b` is the selftest-fixture hardening commit, consistent with the attribution.

## Findings

### F1 — quote: `the six recorded cases`

- Section line: `rank, SHONEN authority, the six recorded cases, or the archived round-12–14`
- Class: **stale-count**.
- Why it fails at C*: the sentence names the lane's measured-case set as six. At C* the same SKILL.md records a seventh case (`## Seventh recorded case and full-page cold-read — round 16`, `:1761`), an eighth (`## Eighth recorded case — round 18`, `:1912`) and a ninth (`## Ninth recorded case — round 26`, `:2111`), and its runner row at `:1398` states the registry is "ten since round 51". A cold reader therefore takes a set size that no longer exists as current.
- Lane precedent that this class is a real defect: `.ufo/waves/round-50/w1/T50Disp49.md` (R49.3) records the identical phrase at `SKILL.md:1555` as "true-but-stale" and asks for an erratum append rather than an in-place edit; nothing at C* corrects this second instance at `:1696` — `git show C*:SKILL.md | grep -n -i 'erratum'` returns only `:1483`, the unrelated round-37 source-audit erratum, so this occurrence is residual.

### F2 — quote: `successor sweep or seventh case is claimed.`

- Section line: `successor sweep or seventh case is claimed.`
- Class: **stale-negation** (present-tense negation overtaken by later rounds).
- Why it fails at C*: the clause asserts that no seventh case is claimed. SKILL.md at C* claims it outright — `:1763 **The seventh case.** kumitate `scripts/round-gate.mjs` at rev `364f1d5` … **5/10 killed (50 %)**` — and then claims an eighth and a ninth. Unlike the dated milestones elsewhere in the file (e.g. `:925` "Four legs at this revision", corrected as dated in the errata table `:1740`), this negation carries no date marker, so it reads as a statement about the lane at the revision being read.
- Note: F1 and F2 are the same stale case-set premise expressed twice (count and negation); they are reported separately because each is independently falsifiable and each would need its own wording fix.

## Considered and deliberately not asserted as findings

- **`no sibling gate is registered or executed by this lane`.** Literal reading fails at C*: `tools/mutate-and-run.sh` registers and executes kumitate's `scripts/round-gate.mjs`, `scripts/sources-check.mjs` and `scripts/cite-check.mjs` as the `js-round-gate`/`js-sources-check`/`js-cite-check` legs (checks 17–18), and those are sibling-lane gates. Counter-reading: the clause sits in a sentence whose first half is scoped by "No row here", and the round-15 intent is "no sibling gate is registered *in this registry*". I could not exclude the scoped reading from the bytes alone, so I do not raise it as a finding; it is recorded here for the L1.
- **`because the runner input moved`.** True but incomplete: three pinned inputs drift at C* (`tools/bash-witness-study.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`), and the tool fails fast on the first (a probe, not the runner), so an operator told only "the runner input moved" would be surprised by the reported finding id. The clause is not false, so it is not a finding.
- **`historical expected pins13 original inputs`** — missing space between "pins" and "13"; the count itself is verified. Cosmetic, not a statement that fails.

## Out-of-scope observations (not findings against this section)

- `tools/evidence-disposition.py:181` (`USAGE`) still reads "`--selftest` builds isolated /tmp fixtures." and `:2350` reads `"""Isolated /tmp fixtures; invokes this CLI via subprocess only."""`, although the selftest creates its fixtures via `tempfile.mkdtemp` under `TMPDIR`. This is `tools/` documentation, not this section's text, and it does not match C2's `dir\s*=\s*["']/tmp` surface; routed here only as an observation.
- `tools/context-capture.py:26-27` reads "against isolated synthetic fixtures under / the scratch root (tempfile.mkdtemp(dir=tempfile.gettempdir()))" — a damaged sentence left by the TMPDIR edit. Again `tools/`, not this section.

## Limits

- Row `disposition` exit 1 ("failed semantic expectation") was verified by reading `USAGE` plus `main()`/`emit_result`; I did not build a fixture that provokes exit 1 (a valid dispositions document needs a pinned receipt graph and a repo-identity-clean root).
- The frozen replay was exercised for `28aeef4` only; no other historical revision was replayed.
- The "six recorded cases" referent: I did not reconstruct the round-12 case ledger itself; the finding rests on SKILL.md's own later case sections and its runner row, which is enough to show the sentence is not current at C*.
- Scratch used and removed: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read15/` (archive replay tree, receipt outputs, `TMPDIR`). No tool installs were needed; nothing was added to `PATH`.
