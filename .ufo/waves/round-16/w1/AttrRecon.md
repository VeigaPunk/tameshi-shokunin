# AttrRecon — routed defect 2 recon: usage-finding attribution

Seat: TameshiR16.AttrRecon (leaf, read-only recon). Round 16 w1.
Question: in `.ufo/evidence/round-15/verify.py`, why do the `gate-usage` and
`usage-proof-new` rows of `verification-3.json` record
`observed_id=context_consistent`, and where does the terminal verdict
`CONTEXT: USAGE_ERROR (id=usage_error exit=64)` actually sit?

**Short answer:** both commands exit 64 with empty stdout; the retained stderr
contains the tool's full help block first, whose `exit 0` line documents
`(id=context_consistent)`. `run_command` extracts `observed_id` with a
leftmost `re.search(r"id=([a-z_]+)")` over stdout then stderr
(`verify.py:207-210`), so it latches the help-text occurrence at byte offset
936 and never sees the real terminal verdict, which is the final stderr line
at offset 1506 (`usage-proof-new`) / 1493 (`gate-usage`). Pass/fail is
unaffected: these rows declare `expected_id=None` and assert only exit 64 plus
the substring `id=usage_error`, both true. Only the `observed_id` and `detail`
fields are misattributed (and the `detail` string is what surfaced the defect).

## 1. The two rows, verbatim

Source: `.ufo/evidence/round-15/verification-3.json` (`checks` array;
`usage-proof-new` is 0-based index 23 / 1-based 24, `gate-usage` is 0-based
index 31 / 1-based 32).

### `usage-proof-new`

- `argv`: `["/usr/bin/python3", "-I", "/tmp/tameshi-r15-verify-bcmjaf6y/lane/tools/candidate.py", "--check", "--expected", "/tmp/tameshi-r15-verify-bcmjaf6y/usage-proof/expected.json", "--receipt", "--json"]`
- `cwd`: `/tmp/tameshi-r15-verify-bcmjaf6y` (scratch; since removed — see §5)
- `expected_exit` = 64 (declared map `verify.py:552`: `{"exit": 64, "stderr_token": "id=usage_error"}`; same in `attempt-3/expected.json`)
- `expected_id` = `None`; `expected_verdict_match` = `None`
- `observed_exit` = 64; `observed_id` = `"context_consistent"`; `observed_verdict_match` = `None`
- `passed` = true; `detail` = `"expected exit=64 id=None observed exit=64 id=context_consistent"`
- `stdout` (retained, 0 bytes): `''`
- `stderr` (retained, 1530 bytes):

```
usage: context-capture.py --check [--receipt FILE --expected FILE] [--json]
       context-capture.py --selftest

Retained-receipt gate for the round-14 context observation. `--check` alone
replays the frozen clean receipt against its built-in digest/id/exit pin.
`--check --receipt FILE --expected FILE` pins the receipt sha256 and the exact
expected finding id/exit from an expected file.

The gate re-derives comparison, environment, run, positive-control, source and
runner-mapping facts from raw retained fields; stored status/exit/reasons and
summary booleans are never trusted. It does not capture, execute the probe,
read live lane inputs, or write during check; frozen mode reads only the
archived receipt named by the built-in pin. Explicit mode reads only the
caller-selected receipt and expected JSON with the caller's permissions; select
non-secret files. No credential probe is executed.

exit 0   clean retained receipt (id=context_consistent)
exit 1   re-derived or pinned-verdict mismatch (a matched exit-1 pin still
         reports the retained mismatch as exit 1)
exit 2   could-not-evaluate receipt/expected/snapshot/internal failure
exit 64  usage / could-not-evaluate invocation

expected schema (exactly four keys):
  {"schema": "tameshi-context-expected-v1",
   "receipt_sha256": "<64 lowercase hex>",
   "id": "<stable finding id or context_consistent>",
   "exit": 0 | 1 | 2}
context-capture.py: --receipt cannot take a recognized flag as its value: --json
CONTEXT: USAGE_ERROR (id=usage_error exit=64)
```

### `gate-usage`

- `argv`: `["/usr/bin/python3", "-I", "/tmp/tameshi-r15-verify-bcmjaf6y/lane/tools/candidate.py", "--check", "--receipt", "receipt.json"]`
- `cwd`: `/tmp/tameshi-r15-verify-bcmjaf6y`
- `expected_exit` = 64 (declared map `verify.py:558`: `{"exit": 64, "stderr_token": "id=usage_error"}`; same in `attempt-3/expected.json`)
- `expected_id` = `None`; `expected_verdict_match` = `None`
- `observed_exit` = 64; `observed_id` = `"context_consistent"`; `observed_verdict_match` = `None`
- `passed` = true; `detail` = `"expected exit=64 id=None observed exit=64 id=context_consistent"`
- `stdout` (retained, 0 bytes): `''`
- `stderr` (retained, 1517 bytes): the same help block as above, then:

```
context-capture.py: --receipt and --expected must be given together
CONTEXT: USAGE_ERROR (id=usage_error exit=64)
```

So yes — the raw text the extractor saw is retained in full: `run_command`
stores `stdout`/`stderr` untruncated in each check entry
(`verify.py:236-237`); unlike the selftest helper (`tools/context-capture.py:
1746-1757`), `run_command` does not slice to 400 bytes.

## 2. Extractor mechanism (`verify.py`)

- `verify.py:138` — `ID_TOKEN_RE = re.compile(r"id=([a-z_]+)")`.
- `verify.py:197-210` — `observed_id` starts `None`; `stdout_is_result_json`
  is False for these two calls, so the JSON branch is skipped; then
  `token = ID_TOKEN_RE.search(stdout) or ID_TOKEN_RE.search(stderr)`.
  `str` search over empty stdout returns `None`, and `re.search` returns the
  **leftmost** match in stderr.
- Both calls: `verify.py:629-632` (`usage-proof-new`) and `verify.py:713-717`
  (`gate-usage`) pass no `expected_id` and no `stdout_is_result_json`, only
  `stderr_token="id=usage_error"`.
- `verify.py:211-228` — `ok` = exit equality (64 == 64) and
  `stderr_token in stderr` (true) and no `"Traceback"` (true);
  `expected_id` block is skipped entirely.
- `verify.py:230-241` — the wrong `observed_id` is written to the entry and
  interpolated into `detail`; `passed` stays true.

Simulating the exact expression on the retained stderr bytes (pure text, no
tool execution):

| row | `search()` | all `id=` occurrences `(offset, token)` |
|---|---|---|
| `usage-proof-new` | `context_consistent` @ 936 | `(936, context_consistent)`, `(1506, usage_error)` |
| `gate-usage` | `context_consistent` @ 936 | `(936, context_consistent)`, `(1493, usage_error)` |

The second occurrence in each row is the real finding id; the first is help
text.

## 3. Why the first match is help text, and where the verdict sits

Maintained tool source `tools/context-capture.py` (sha256
`c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726`, identical
to `git show 7650fe4db89f...:tools/context-capture.py`):

- `tools/context-capture.py:270-300` — `USAGE` literal. Line 286 is
  `exit 0   clean retained receipt (id=context_consistent)`, the first `id=`
  token in the emitted text. It is legitimate documentation, not a finding.
  (Line 295's `<stable finding id or context_consistent>` has no literal
  `id=`; `ID_TOKEN_RE` does not match it.)
- `tools/context-capture.py:2276-2286` — `main`: on `UsageError` it writes
  `USAGE` to stderr (2282), then writes the per-invocation reason and the
  terminal line in one call (2283-2286):
  `"context-capture.py: {}\nCONTEXT: USAGE_ERROR (id=usage_error exit=64)\n"`.
  Exit 64.
- Path into `UsageError`:
  - `usage-proof-new`: `--receipt` is followed by `--json`, a member of
    `KNOWN_ARGUMENTS` (`tools/context-capture.py:267-268`), so
    `tools/context-capture.py:2244-2248` raises
    `"--receipt cannot take a recognized flag as its value: --json"`.
  - `gate-usage`: `--receipt receipt.json` without `--expected`, so
    `tools/context-capture.py:2266-2267` raises
    `"--receipt and --expected must be given together"`.
- Therefore the ordered stderr layout is: `USAGE` (0..~940) → the reason line
  → `CONTEXT: USAGE_ERROR (id=usage_error exit=64)` as the **final line**
  (`usage-proof-new` offset 1506 of 1530; `gate-usage` offset 1493 of 1517).
  The real verdict is nowhere in stdout; stdout is empty.
- Contrast: the prefix tool (`usage-proof-old`, `0ed784e0...`) accepted the
  dangling `--json` as a receipt filename and emitted its structured
  `CONTEXT: INVALID (id=receipt_missing ...)` on stdout with exit 2; that row's
  `observed_id=receipt_missing` is correct because no help text is printed on
  that path. The mismatch is specific to paths that print `USAGE` to stderr.

The maintained tool's own selftest treats usage as a substring fact
(`"id=usage_error" in proc.stderr`, `tools/context-capture.py:1746-1757`), so
the tool's contract is "terminal verdict text present", not "first id= token".

## 4. Impact assessment

- `passed=true` on both rows is legitimate: exit 64 and the terminal
  `id=usage_error` substring are both observed; `expected_id=None` means
  neither row ever asserted equality to the misattributed token.
- Misattribution is confined to `checks[*].observed_id` and
  `checks[*].detail` for the two rows; it is an evidence-quality defect, not a
  false pass. C1's bounded usage proof is not invalidated; the spotcheck lesson
  records the same conclusion (`corpus/lessons/round-15-verifier-spotcheck.md:
  108`) and routes the extractor correction (line 160).

## 5. Identity / provenance checks

- `sha256sum tools/context-capture.py` →
  `c4a1d165...1726` = `PIN_TOOL_SHA256` (`verify.py:112-113`).
- `git show 7650fe4db89f3a706aed63d048ac47e02289cc72:tools/context-capture.py | sha256sum`
  → `c4a1d165...1726` (the revision `verification-3.json` names,
  `requested_rev=7650fe4...`).
- `git show bca5deb:tools/context-capture.py | sha256sum` → `0ed784e0...edc`
  = `PIN_PREFIX_TOOL_SHA256`.
- `verify.py`, `verification-3.json`, `expected.json` are tracked and clean
  (`git status --porcelain -- .ufo/evidence/round-15/` empty). No edits were
  made; `verification-3.json` was only read.
- Scratch dir `/tmp/tameshi-r15-verify-bcmjaf6y` no longer exists (`ls -d`
  found nothing), so `candidate.py` cannot be re-read there; the git blob
  digests above are the identity evidence. Do not rerun the old argv without
  materializing the pinned blob.
- Layout note for the correction author: top-level
  `.ufo/evidence/round-15/expected.json` names `requested_rev=0494c244...`
  (attempt 1), while `verification-3.json` and
  `attempt-3/expected.json` name `7650fe4...`. For any correction referencing
  `verification-3.json` expectations, cite `attempt-3/expected.json`.

## 6. Bounded recommendations (for AttrFix / L1; not applied by this seat)

1. **Fix the extractor, not the help text.** Replace the first-match fallback
   at `verify.py:207-210` with a parse of the terminal structured verdict:
   scan `stdout` then `stderr` for lines matching
   `^CONTEXT: [A-Z_]+ \(id=([a-z_]+)` (re.MULTILINE), take the last match;
   keep the current leftmost `id=` as a fallback only when no verdict line
   exists. On the retained bytes this yields `usage_error` for both rows and
   leaves `receipt_missing` (`usage-proof-old`) unchanged.
2. **Make the regression failure-backed.** Once (1) is in, add
   `expected_id="usage_error"` to the two calls (`verify.py:629-632`,
   `713-717`) and to the declared map (`verify.py:552`, `558`) plus a fixture
   that replays the same argv on pinned tool bytes. On the pre-fix extractor
   that fixture must fail (observed `context_consistent`); on the fixed
   extractor it must pass. This is the "old misattribution + corrected
   finding, same fixture/argv" demonstration.
3. **Append-only attribution correction.** Leave `verification-3.json`
   byte-identical. Append a correction artefact naming exactly
   `checks[23].observed_id` + `checks[23].detail` (`usage-proof-new`, 1-based
   24) and `checks[31].observed_id` + `checks[31].detail` (`gate-usage`,
   1-based 32), with the corrected value `usage_error` and the retained
   stderr offsets above as support. Path/format is L1's call.
4. **Do not delete `(id=context_consistent)` from `USAGE`.** It is correct
   operator documentation; the reproducible defect is the extractor's
   leftmost-match rule. Deleting it would also silently mask the bug without
   the failure-backed fixture that the spotcheck asks for.

## 7. Commands executed / files opened

All read-only; no tool install, no network, no candidate execution.

- `read skill://godspeed` (exit 0)
- `ls -la .ufo/evidence/round-15/`; `wc -l verify.py verification-3.json`
  (exit 0)
- `python3` extraction of `verification-3.json` rows, check indices, full
  stdout/stderr, `id=` offsets, `finditer` simulation (exit 0 each)
- `grep -n` on `verify.py`, `tools/context-capture.py`,
  `corpus/lessons/round-15-verifier-spotcheck.md` (exit 0)
- `sed -n` ranges of `tools/context-capture.py` 260-305, 1730-1765,
  2212-2270, 2260-2295 (exit 0)
- `git ls-files` / `git status --porcelain` / `git log --oneline` on the
  evidence dir (exit 0)
- `git show <rev>:tools/context-capture.py | sha256sum` for rev `7650fe4...`
  and prefix `bca5deb` (exit 0; digests in §5)
- `cmp -s expected.json attempt-3/expected.json` (exit 1: they differ, as
  expected; different `requested_rev`)
- Files opened: `.ufo/evidence/round-15/verify.py` (ranges 99-273, 519-743),
  `.ufo/evidence/round-15/verification-3.json`,
  `.ufo/evidence/round-15/expected.json`,
  `.ufo/evidence/round-15/attempt-3/expected.json`,
  `tools/context-capture.py` (ranges cited above),
  `corpus/lessons/round-15-verifier-spotcheck.md` (grep hits at lines 108 and
  160).

## 8. Remaining unknowns

- No material unknowns for the attribution question. The only unobservable
  item is the scratch `candidate.py` bytes (scratch removed); identity is
  corroborated by the pinned git blobs and working-tree digest.
- Inference (not directly executed): the fixed "last verdict line" extractor
  would return `usage_error` on the retained bytes — this follows from
  `finditer` ordering shown in §2, not from running modified code.
