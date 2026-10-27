# T53W1Read01 — cold read: `## Context gate classification and explicit exit classes — round 15`

Seat: reader (wave 1). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit (`cand`): `a41195dfc13a73958e4c5228ec196b28d03ded03`.
Source read method: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C*:SKILL.md` into scratch; working tree never used for section bytes.

## Section bytes (frozen-monitor definition)

Heading line: `## Context gate classification and explicit exit classes — round 15`.
Split rule applied: SKILL.md at C* split into lines (2178 lines); a heading is a line matching `^#{1,3}(\s|$)` outside ``` fences; the section is the heading line through the line before the next heading; trailing whitespace-only lines stripped; joined with `\n`, no trailing newline; sha256 over UTF-8 bytes with `surrogateescape`.

- Heading matched exactly once, at line **1616** (outside fences; the section contains no fences).
- Next heading: `### Round-15 gate/probe registry` at line **1683** → section lines **1616–1681** (line 1682 is whitespace-only and is stripped).
- Section size: **5104 characters / 5112 bytes** (`wc -c` cross-check on the slice gives 5112).
- `section_sha256` = `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6`

Reproduction cross-check (independent of the extraction script):

```
printf '%s' "$(git show C*:SKILL.md | sed -n '1616,1681p')" | sha256sum
132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6  -
```

## Checks run

All commands ran from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` or from the seat scratch dir; none mutates git, the lane tree, or any path outside scratch.

| # | Claim under test | Command (abbreviated) | Observed | Result |
|---|---|---|---|---|
| 1 | Section boundaries/digest | heading scan + slice of `git show C*:SKILL.md` | 1616–1681, sha256 `132cfb9e…edf6` | HOLDS |
| 2 | Archived script digest | `git show C*:.ufo/evidence/round-14/capture-context.py \| sha256sum` | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` | HOLDS |
| 3 | Negative fixture digest | same on `.ufo/evidence/round-14/context-missing-env.json` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` | HOLDS |
| 4 | Clean receipt digest | same on `.ufo/evidence/round-14/context-receipt.json` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` | HOLDS |
| 5 | Line pointers `:2-31`, `:553-580`, `:605-643` | `nl -ba` over the archived script (647 lines) | docstring spans 2–31 (closes at 32); `def decide` 553–580 with `return "ok", 0, []` at 580; `def main` 605–643 with `return 64` at 613 | HOLDS |
| 6 | `decide()` returns `ok`/exit0 or `mismatch`/exit1 | same listing | lines 579–580: `return "mismatch", 1, reasons` / `return "ok", 0, []` | HOLDS |
| 7 | Archived script compares two probe documents, only top-level `observed_at` excluded | `nl` 340–395 (`comparison_block`) | pops only top-level `observed_at` from copies, canonical JSON compare, `exclusions: ["observed_at"]` | HOLDS |
| 8 | Environment delta + positive git control + six leg mappings | `nl` 213–340, 395–413, 465–551 | `parse_runner_mapping` enforces 6 header rows / 6 calls / 6 PIN_ / 6 REV_; `positive_control_block` is a `git rev-parse --git-dir` control; `env_delta_matches_declared` recomputed | HOLDS |
| 9 | Probe/runner source digests persisted against round-13 `expected.json` / `pin-manifest.json` | `nl` 476–509 | `sources.probe.matches_declared` vs `expected_r13.inputs[tools/pin-disposition.py]`; `sources.runner.matches_manifest_declaration` vs `manifest.derived_from` | HOLDS |
| 10 | Manifest really has six legs | `git show C*:.ufo/evidence/round-13/pin-manifest.json` → `legs` length | `legs: 6` ("the six ledger legs") | HOLDS |
| 11 | Maintained gate exists, CLI shape, exit map, frozen default | `grep`/`nl` over `C*:tools/context-capture.py` | `--check [--receipt FILE --expected FILE] [--json]`, `--selftest`; finding-id table with `exit 0`, `exit 1`, `exit 2`, `usage_error exit 64`; `FROZEN_RECEIPT_REL=.ufo/evidence/round-14/context-receipt.json`, `FROZEN_RECEIPT_SHA256=05cb55b8…c1a`, `FROZEN_EXPECTED_ID=context_consistent`, `FROZEN_EXPECTED_EXIT=0` | HOLDS |
| 12 | `tameshi-context-expected-v1` is exactly four keys; exit ∈ {0,1,2} | `nl` 265, 1223–1246 | `EXPECTED_KEYS = {schema, receipt_sha256, id, exit}`; `require_int(..., {0, 1, 2})`; extra/missing keys → `expected_invalid` exit2 | HOLDS |
| 13 | Check mode never executes retained argv / never opens a recorded root path; writes nothing | `grep 'open(\|os.replace\|subprocess'` + `nl` 490–520 | only reads; `subprocess` appears inside the selftest harness; writes at 1667/1682/1685 are selftest fixtures; `lane_root`/`fleet_root` are validated as absolute strings and their parent relation checked, never opened | HOLDS |
| 14 | Negative fixture must fail at exit1 with `missing_injected_environment` under its committed pin | ran `C*:tools/context-capture.py --check --receipt context-missing-env.json --expected frozen/context-missing-env/expected.json` in scratch | `CONTEXT: MISMATCH (id=missing_injected_environment … exit=1 findings=2)`, shell exit **1**; pin file is `{"schema":"tameshi-context-expected-v1","receipt_sha256":"1ee9d09b…","id":"missing_injected_environment","exit":1}` | HOLDS |
| 15 | Clean retained receipt is the exit0 counterpart | same tool, clean receipt + `frozen/context-clean/expected.json` | `CONTEXT: OK (id=context_consistent … exit=0 findings=0)`, shell exit **0** | HOLDS |
| 16 | Duplicate-key / non-UTF-8 / malformed input are could-not-evaluate | `nl` 328–347, 1361–1379 and selftest case list | `_no_duplicate_keys` → `receipt_json_invalid`/`expected_invalid` exit2; `UnicodeDecodeError` → exit2; `snapshot_tampered` exit2 | HOLDS |
| 17 | "two earlier failed harness receipts" | `git show C*` of `.ufo/evidence/round-15/verification{,2,3}.json` | `verification.json passed=False failed=['selftest-new','selftest-new-full-count']`; `verification-2.json passed=False failed=['runner-internal-error']`; `verification-3.json passed=True` (attempt 3) | HOLDS |
| 18 | Cited lesson sections/items exist | `git show C*:corpus/lessons/round-15.md` headings; `…/round-14-verifier-spotcheck.md` item 5 | `## Gate`, `## Mistakes`; `## Routed defects and residuals` item `5. **Tameshi, next round registry/selftest correction:** …` | HOLDS |
| 19 | Source ids S051 / S049 | `git show C*:corpus/SOURCES.md` rows 58, 60 | `S049` = Python subprocess env mapping (explicit child invocation, opened 2026-10-20); `S051` = "Retained context-receipt gate — tools/context-capture.py", own-work, opened 2026-10-20 | HOLDS |
| 20 | `../PROTOCOL.md` §Gate standard supports the classification and exit classes | `sed -n '375,430p' /home/vgpnk/Projects/shokunin/PROTOCOL.md` (read-only, outside lane) | gate = committed re-runnable verdict script comparing surfaces to persisted expected values; `0`=clean, `1`=failed fleet-wide, other codes declared and mapped, undeclared nonzero = could-not-evaluate | HOLDS |
| 21 | "Former" states of the corrected rows | `git show 0c6e36d:SKILL.md` (round-14 revision) rows, compared with C* | round-14 registry classified the script as a probe with a verdict map ending at `2 could-not-evaluate setup` (no 64), and its recipe step 5 ran the script with no arguments; at C* the row is archived and step 5 is marked as an archived experiment directing use of the maintained gate (verbatim row fragments in the holds list below) | HOLDS |
| 22 | Registry rows at C* now carry the corrected classes | `git show C*:SKILL.md` lines 1683–1712 | context row: `0 clean (context_consistent); 1 failed stable finding ID; 2 and 64 could-not-evaluate (…)`; disposition row: `0 clean; 1 failed semantic expectations; 2 and 64 could-not-evaluate (… 64 usage)`; exactly two rows, matching "both active gates" | HOLDS |
| 23 | Maintained gate never invokes the archive | `grep -n 'capture-context' C*:tools/context-capture.py` | only the docstring line naming it as the archived predecessor | HOLDS |
| 24 | Selftest inputs are synthetic, distinct from retained files | `nl` 1624–1690, 1789–1800 | fixtures built in-process (`build_fixture_receipt`), written under `mkdtemp`, removed in `finally`; `hermetic-no-lane-path` asserts the default lane root never appears in subprocess output | HOLDS |

## Holds — section statements verified against C* bytes

Quotes below are byte-exact single-line fragments of the section (lines given).

- L3–4 `Sources: S051 (maintained retained-context gate, opened this round),` and `S049 (explicit child invocation)` — both rows exist in `corpus/SOURCES.md` at C* (checks 19).
- L10–11 `Effective runtime evidence is` / ``.ufo/evidence/round-15/verification-3.json`` — file exists, `passed: true`, `attempt: 3`; the two earlier attempts are `passed: false` (check 17).
- L18–21 archive paragraph, digest `7313e9a2…7d89` — reproduced byte-exactly (check 2).
- L20–21 `is a **gate** under §Gate standard, not a probe.` — PROTOCOL §Gate standard defines a gate as a script comparing surfaces against persisted expected values (check 20).
- L30 `` gate is `tools/context-capture.py`; the active use is retained-receipt replay, `` — the maintained tool is retained-receipt replay only (checks 11, 13).
- L34–37 expected-pin semantics (`built in for the frozen clean receipt`, `--receipt`/`--expected` otherwise) — matches `FROZEN_*` constants and explicit-mode key validation (checks 11, 12).
- L38 `receipt is data: check mode never executes retained argv, never opens a` — no runtime `subprocess` in check mode; recorded roots are string-validated only (check 13).
- L40–42 stored `status`/`exit`/`reasons` are not trusted — `verify_recorded_verdict` recomputes and emits `receipt_verdict_mismatch`; observed in check 14 (the negative fixture records `status 'ok' exit 0` yet the tool returns exit 1).
- L43–46 negative fixture plus schema `tameshi-context-expected-v1` naming `missing_injected_environment` and exit1 — executed: exit 1 (check 14); schema is exactly four keys (check 12).
- L47–48 `Selftest inputs are` / `synthetic fixtures, distinct from these retained files.` — selftest builds its own receipts and never reads `.ufo/evidence` (check 24).
- L50–58 decision table — each row matches the implemented finding-id/exit map and the two executed paths (clean → 0, missing-env → 1, invalid/tampered → 2, usage → 64) (checks 11, 14, 15, 16).
- L59–62 `Both active gates share three classes over four exit codes` — at C* the round-15 registry has exactly two rows and both declare `2 and 64 could-not-evaluate` (check 22); the disposition tool's usage path returns 64 with no JSON contract (`main()` lines 3197–3208).
- L62–64 `This corrects the disposition row's former` / `` `64 usage` `` wording and the context row's former probe label and absence of 64 — confirmed against the round-14 revision (`0c6e36d`), whose context row reads `probe` with a verdict map ending at `2 could-not-evaluate setup`, and whose disposition row lists `64 usage` as a bare class (check 21).

Row fragments behind the previous bullet, quoted byte-exactly from the registry tables (provenance: `0c6e36d:SKILL.md` and `C*:SKILL.md`, not this section):

- `invocation context capture | probe` (round-14 row, first two columns)
- `0 bounded experiment/mappings agree; 1 observed mismatch or failed control; 2 could-not-evaluate setup` (round-14 verdict map; 64 absent from the map)
- `archived invocation context capture | historical gate, not active | do not run` (C* row, first three columns)

## Findings

**None.** `findings: []` — no statement in this section fails against C* bytes.

Considered and rejected as findings (recorded so the L1 can see the reasoning, not as claims):

- `registry history is retained above with an inline archive marker, not a callable entry.` (line 22; the sentence begins on line 21 with "The round-14"). The round-14 registry table at C* does still contain a *callable* disposition row, so a whole-table reading would fail. The sentence sits immediately after the capture-context classification correction and its own next sentence (`That historical script is **archived, not active**:`) fixes the referent as the archived context-capture row, which at C* reads `archived invocation context capture | historical gate, not active | do not run`. Referent-scoped reading holds; I could not evidence a reading under which the sentence is false without discarding the adjacent sentence.
- Table row 3 lists "Missing, unreadable, wrongly typed, duplicate-key or non-UTF-8 input" as exit2 while an *absent receipt field* (`environment.injected_env`) yields exit1 `missing_injected_environment`. The two are consistent: row 3 covers input files; row 2 covers absent/wrongly-typed derived fields, and its own parenthetical names the missing-environment case as exit1. Executed both paths (checks 14, 16).
- Selftest fixtures land under `tempfile.gettempdir()` (`mkdtemp(dir=...)`). That honours `TMPDIR` and the fixtures are kilobytes, so the host scratch directive (`/tmp` only for files under 50 MB) is not violated; the section itself makes no scratch-path claim.

## Limits / out-of-scope

- Read-only throughout: no git/jj mutation, no writes outside `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-53/w1/` and the seat scratch dir. I did not run the maintained gate's `--selftest` or its frozen default mode (frozen mode resolves its lane root from the script location, which a scratch copy would falsify); those remain the L1's re-execution surface. Claims about them are evidenced statically plus by the two explicit-mode runs in checks 14–15.
- I did not re-execute the archived round-14 script (by design: it would replace the frozen receipt), and I did not execute any sibling lane gate.
- Only this section was graded; the registry rows above/below were read solely as pointers for its claims.
- No tools installed or upgraded (nothing was needed): tooling record = none.

## Artifacts

- `.ufo/waves/round-53/w1/T53W1Read01.json` (machine deliverable)
- `.ufo/waves/round-53/w1/T53W1Read01.md` (this report)

Scratch `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read01/` was removed before yield.
