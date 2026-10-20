# MistakeScribe — round 16 `## Mistakes` draft and QUALITY 18–19 draft

Seat: TameshiR16.MistakeScribe (leaf scribe). Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Scratch: `/tmp/tameshi-r16-MistakeScribe-EYIz/` (read-only probes only). No lane file, fleet file, or `corpus/lessons/round-16.md` was created or edited. No message sent. No tools installed or updated.

## 1. Verdict

Both target defects are confirmed from committed evidence. Two rows are drafted (a, b), and QUALITY 18 and 19 are drafted. Every claim below carries its command or path:line pointer. Inference is marked `[INFERENCE]`.

## 2. Commands run and observed results

| # | Command (abbreviated) | Exit | Key observed output |
|---|---|---|---|
| 1 | `read` of `/home/vgpnk/Projects/shokunin/CORPUS.md` | ok | Rules block `CORPUS.md:157-184`; `## Mistakes` rule `:171-178`; class vocabulary `:174-176` = `vacuous, survivor, stale-premise, reference-drift, number-drift, scope, attribution, landing, provider` |
| 2 | `read` of `tameshi-shokunin/corpus/QUALITY.md` | ok | Criteria 1–17 only (`QUALITY.md` lines 3–84). No `18.` or `19.` heading |
| 3 | `read` of `corpus/lessons/round-15-verifier-spotcheck.md` | ok | Status-neutral defect `:108`; Routed defects item 2 `:160`; item 1 `:159`; item 3 `:161` |
| 4 | query `verification-3.json` checks named `gate-usage` / `usage-proof-new` | ok | Both rows: `expected_id: null`, `observed_id: "context_consistent"`, `observed_exit: 64`, `passed: true`. Row starts `verification-3.json:213` (usage-proof-new name), `:359` (gate-usage name) |
| 5 | `read` of `tameshi-shokunin/.ufo/evidence/round-15/verify.py:179-262` | ok | `run_command` body (see §3a) |
| 6 | `_grep` of `verify.py` for id/expected_id/stderr_token | ok | `:138` `ID_TOKEN_RE`; `:207-210` first-match fallback; `:212-213` id check gated on `expected_id is not None`; `:222-223` `stderr_token in stderr`; `:552`, `:558` usage rows expect `stderr_token` only; `:631-632`, `:716-717` call sites |
| 7 | `git -C shokunin ls-files .ufo/waves/hyaku/misroots` | 0 | 3 tracked files: `MoriR16.Lesson`, `SoujiR15`, `TameshiR15` |
| 8 | `git -C shokunin log --oneline -- .ufo/waves/hyaku/misroots/TameshiR15` | 0 | Only commit: `ac0a7fc 2026-10-20 06:30:51 -0300 ops(hyaku): wrap-up …` (file mtime is 05:06:36, earlier) |
| 9 | `git -C shokunin status --porcelain -- .ufo/waves/hyaku/misroots` | 0 | empty (tracked, unmodified) |
| 10 | `cmp .ufo/waves/hyaku/misroots/TameshiR15 tameshi-shokunin/.ufo/waves/round-15/w1/Frontier.md` | 1 | `differ: char 1, line 1` — misroot is not a copy of the lane report |
| 11 | `sha256sum` misroot | 0 | `b413df980b7781b8c4b904770e968391c2664c908e327d4231c4727f7f236469` (605 bytes) |
| 12 | `python3 /tmp/…/extract_check.py` (read-only, stdlib, retained JSON only) | 0 | See §3a; negative control returns `[]` |
| 13 | `python3 /tmp/…/sweep.py` (read-only, retained JSON only) | 0 | 14 command checks; 3 flagged by heuristic, 2 real (see §3a) |
| 14 | `grep` QUALITY.md `^1[89]\. ` | 1 | no match: 18 and 19 are free |
| 15 | `ls corpus/lessons/round-16.md` | 2 | absent (correctly not created) |
| 16 | `grep -niE 'bare|prefix|agent://<'` on `.ufo/prompts/tameshi-round-16.md` | no output | the round-16 prompt file contains no bare-name / prefix rule (only `agent://all` at `:239`) |
| 17 | `grep -rni misroot` on `corpus/lessons/round-15.md`, `…round-15-verifier-spotcheck.md`, `.ufo/reports/round-15/tameshi.md` | no output | the round-15 misroot is recorded nowhere in the lane's round-15 lesson or report |

## 3. Findings

### 3a. Defect (a) — usage-finding misattribution in `verify.py` (confirmed)

Mechanism, from source:

- `verify.py:138` `ID_TOKEN_RE = re.compile(r"id=([a-z_]+)")`.
- `verify.py:207-210`: when no JSON result is parsed, `observed_id` is the **first** `id=` match in stdout, else in stderr (`ID_TOKEN_RE.search(stdout) or ID_TOKEN_RE.search(stderr)`).
- `verify.py:212-213`: the id is only compared when `expected_id is not None`. The usage rows set `expected_id=None` (`:552`, `:558` use `stderr_token` only), so the wrong `observed_id` is never asserted.
- `verify.py:222-223`: `stderr_token` is a substring test. `"id=usage_error" in stderr` is true because the terminal line is present, so the row passes.

Retained evidence (`verification-3.json`, read-only probe output):

- The help text printed to stderr contains `(id=context_consistent)` at stderr line **17** (`exit 0   clean retained receipt (id=context_consistent)`). This is the first `id=` token.
- The terminal verdict, the last stderr line, is `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`.
- Recomputed first-match id = `context_consistent` for both rows. Recorded `observed_id` = `context_consistent` for both rows. Terminal verdict token = `usage_error`, exit `64`.
- Negative control: with the terminal line removed from the same retained stderr, the corrected terminal-line pattern returns `[]`, so a fixed check must fail there.

Scope check (sweep, read-only, 14 command checks):

- Real hits: `usage-proof-new` and `gate-usage`. Both have `expected_id: null` and the misattributed `observed_id`.
- Heuristic false positive: `mapping-oracle-old` (`expected_verdict_mismatch`) also has several distinct `id=` tokens, but its `observed_id` comes from the JSON `id` field (`verify.py:199-206`, `stdout_is_result_json=True`), not the regex. It is correctly attributed and is **not** affected. Recorded here so the sweep is not over-cited.

Nature of the defect: the rows' pass/fail verdict (exit 64 plus the stderr token) is still supported by raw exit and terminal output, as the spot-check says. The defect is status-neutral attribution: the `observed_id` field is wrong, and the rows cannot detect it because they do not assert the id. This matches `round-15-verifier-spotcheck.md:108` and routed item 2 (`:160`).

### 3b. Defect (b) — round-15 fleet-root misroot (confirmed as a misroot; mechanism `[INFERENCE]`)

- Path: `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/TameshiR15` (605 bytes, mtime `2026-10-20 05:06:36`), tracked at fleet root (finding 7–9).
- Body is a seat-to-L1 message, not a lane report: `Frontier report written: .ufo/waves/round-15/w1/Frontier.md. Implementation-critical for L1: (1) …(4)…`. Its own text says it is a message to L1.
- The lane's real artifact `tameshi-shokunin/.ufo/waves/round-15/w1/Frontier.md` exists (16871 bytes, mtime `05:06`) and differs byte-for-byte (`cmp` exit 1). The misroot is therefore not a copy of it, so it cannot be copied "to the same relative path" without overwriting the lane's real `Frontier.md`. That is a decision for the fleet owner, not a lane-side copy.
- Mechanism `[INFERENCE]`: the body reads as a peer message written with a bare id (`TameshiR15`) instead of `agent://TameshiR15`, which creates a file at the fleet root. I did not observe the write call. This mechanism is the one named in the round-16 task text ("a bare name ... creates a stray file at the fleet root").
- Recurrence: the same directory holds `SoujiR15` (431 bytes) and `MoriR16.Lesson` (847 bytes). All three are tracked at fleet root, so the class has recurred, not just happened once.
- Not recorded: the round-15 lesson, spot-check, and report contain no misroot row (command 17). The round-16 prompt's instruction to record misroots under `## Mistakes` (`.ufo/prompts/tameshi-round-16.md:251`) is post-hoc cleanup guidance, not prevention.
- Prevention gap: the round-16 prompt file has no mandatory-prefix sentence (command 16). The `agent://` rule exists in this seat's task text, not in the prompt file it cites.

## 4. Draft `## Mistakes` prose for `corpus/lessons/round-16.md` (not created)

Columns follow `round-15.md` `## Mistakes` plus the fifth column the round-16 target asks for.

| Class | Evidence pointer | Captured-by | Fix | How the fix is shown able to fail |
|---|---|---|---|---|
| `attribution` (primary); secondary `vacuous` — the id field is unasserted when `expected_id` is null | `tameshi-shokunin/.ufo/evidence/round-15/verify.py:138`, `:207-210`, `:212-213`, `:222-223`, `:552`, `:558`; `verification-3.json:213` (usage-proof-new), `:359` (gate-usage); help line `context_consistent` at stderr line 17; terminal `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`; `round-15-verifier-spotcheck.md:108`, `:160` | `none`. Nearest is QUALITY 17 (`QUALITY.md:77-84`), which covers the gate's own `--selftest` and not the runner's receipt parser; a null `expected_id` leaves the id unasserted, so 17 cannot fire. | Parse the terminal structured verdict (last line matching `^CONTEXT: USAGE_ERROR \(id=([a-z_]+) exit=(\d+)\)$`) for the usage rows; set `expected_id="usage_error"` and exit 64 on both. Forbid first-match extraction for non-JSON commands. Append a correction receipt that names `observed_id` for `usage-proof-new` and `gate-usage`; leave `verification-3.json` byte-unchanged. | Red-before: on the retained stderr, the old extraction yields `context_consistent`, so a check asserting `usage_error` fails (routed to the round-16 lane, not run here). Negative control: remove the terminal line from the same stderr. The fixed parser returns no finding and the check must fail; observed here: parser returns `[]`. Both red outputs must be committed before the fix counts. |
| `attribution` — write outside the lane root (C10 write-scope/attribution in `kaika-w1/mistakes.md:88`) | `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/TameshiR15` (605 B, sha256 `b413df98…7236469`, tracked via `ac0a7fc`); distinct from lane `round-15/w1/Frontier.md` (`cmp` exit 1); siblings `SoujiR15`, `MoriR16.Lesson` in the same dir; mechanism `[INFERENCE]`: bare-name write, not `agent://TameshiR15` | `none`. No QUALITY criterion checks landing paths or message addressing. Round-16 prompt `:251` is cleanup guidance, not prevention; the prompt file has no bare-name / prefix rule. | Record the fleet copy's sha256 and class here. The fleet owner decides removal after the lane confirms the copy is a message, not the lane report (its bytes differ from `Frontier.md`, so no byte-exact copy to the same relative path). Add a round-closure sweep that lists tracked misroots for the round. Prevention is the QUALITY 19 sweep and `agent://<id>` addressing. | Red-before observable now: `git -C /home/vgpnk/Projects/shokunin ls-files .ufo/waves/hyaku/misroots` exits 0 and lists `TameshiR15`, so a sweep that fails on any tracked round misroot is red on the current tree. The fix counts only when the same sweep exits 0 after the fleet owner removes the copy and the lesson records it. |

## 5. Draft QUALITY criteria 18 and 19 (for `corpus/QUALITY.md`, to append; not written)

18. A verifier that reads a finding ID or verdict from a tool's output takes it from the tool's terminal structured verdict, never from the first `id=` or marker in help or usage text. Every checked row that claims an attribution asserts its expected ID; a null `expected_id` on such a row is not a pass. A repaired extractor is shown able to fail on the retained output that exposed the defect: the old misattribution is recorded red, and a negative fixture with the terminal verdict removed must fail the check. Corrections are appended beside the frozen receipt, never rewritten. (`lessons/round-16.md`, `## Mistakes`, attribution row (a); outside `lessons/round-15-verifier-spotcheck.md`, Routed defects item 2.)

19. Every seat output that a round accepts must sit at its declared lane-root path. A file under the fleet root written by a lane seat is a misroot until its bytes are copied into the lane path, `cmp` exits 0, and its fleet owner removes the copy. A peer message carries the `agent://<id>` prefix; a bare-name write is itself a misroot. The round-closure sweep lists tracked fleet-root misroots for the round and exits non-zero on any. The round lesson records each misroot's sha256 and class under `## Mistakes`. (`lessons/round-16.md`, `## Mistakes`, misroot row (b); `.ufo/waves/hyaku/misroots/TameshiR15`.)

## 6. Bounded recommendations

1. Round-16 lane: add the `## Mistakes` rows of §4 to `corpus/lessons/round-16.md`, with `Captured-by` as written. Do not edit `corpus/QUALITY.md` before the round-16 gate.
2. Verifier correction (routed item 2): implement the terminal-verdict parse and the red-before / negative-control pair from §4 row (a). Append the correction receipt. Do not change `verification-3.json`.
3. Misroot (b): the fleet owner should decide whether to remove `TameshiR15` after the lane records its sha256 `b413df98…7236469` and class. The lane must not overwrite `Frontier.md` with it.
4. Prompt hygiene: the round prompt template should carry the `agent://<id>` rule, since the prompt file currently lacks it (command 16). `[INFERENCE]` that this is a template question, not a per-round one.
5. Sweep: add the tracked-misroot sweep to round closure, as in QUALITY 19.

## 7. Not done / limits

- No verifier, gate, or selftest was run. Only stdlib probes over retained JSON in `/tmp`, plus git reads. The red-before outputs in §4 are specified for the lane to run, not observed here.
- Class mapping for (b) is my judgment against the `mistakes.md` taxonomy (C10 write-scope/attribution). It is `[INFERENCE]`.
- The misroot's write mechanism is `[INFERENCE]`; the write call was not observed.
- Installed/updated tools: none. Messages sent: none.
