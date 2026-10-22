# R23-REATTACK RegistryRegistration (round 25, wave 1)

**Verdict: AGREE.** At lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df` the round-23 binding holds. The SKILL home row and the clean, selftest and red registry entries cite a real commit that contains the cited text. Their argv uses the public CLI with unchanged flags. The three active successor rows hold under the official runner. The round-23 selftest row (38/38) no longer holds, by design, because it was superseded by a 44/44 row. The residual notes below are provenance and display matters. None is a counterexample to the binding.

Attacked binding (round-23 item, verbatim): "new SKILL registry home row and tools/registry.json clean/selftest/red entries use actual source commit and fixed public CLI."

Checks: B1 home-row source commit; B2 registry `source` strings; B3 public CLI tokens and CLI stability; B4 entry outcomes at c9ff09f; B5 pinned digests; B6 outcomes at the cited source commit; B7 callers. Confidence is high for B1–B5. B7 rests on literal grep only (no `lsp` device), so its confidence is medium. B6 depends on how `source` is read (see RF1).

## Lane identity

- `git rev-parse HEAD` = `5b69fb23a9c4a27ea13fabf966d131be169846a6`. `c9ff09f` is an ancestor. `git diff --name-only c9ff09f HEAD` lists only `.ufo/evidence/round-25/contract-amendment-1.json` and `.ufo/waves/round-25/{dispatch.json,dispatch.stderr,make-spec.py,spec.json}`.
- `tools/registry.json` at c9ff09f is blob `60a6ff5c…`, the same as d2eaecd. `tools/command-binding.py` at c9ff09f is blob `1b4bbb77…`, the same as d2eaecd. Round 24 (d2eaecd) was the last commit to touch either file.
- `git diff --unified=0 496d212 HEAD -- tools/command-binding.py` shows two hunks, `@@ -164 +164 @@` and `@@ -166,3 +166,4 @@`. Both sit inside `selftest()`, in the fixture-loading lines. `evaluate()` (command-binding.py:65-113), `check()` (:115-130) and `main()` (:196-217) are unchanged since 496d212.
- Round-23 "source commit" 496d212 is the commit that introduced the SKILL row and the tool. Both replay bundles declare `revision: 496d212bc46789cdf8cafab72978bdb7f4182963`.

## B1: the home row's source commit is real and contains the row. HOLDS

- `git show 496d212:SKILL.md | sed -n 2019p` and `git show c9ff09f:SKILL.md | sed -n 2019p` return the same row: `| \`tools/command-binding.py\` | gate | \`python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json\` | 0 clean declaration binding; 1 mismatch; 2 invalid/unavailable/tampered, could-not-evaluate; 64 usage, could-not-evaluate | \`python3 tools/command-binding.py --selftest\` | … | tameshi |`
- `git log -S'| `tools/command-binding.py` | gate |' -- SKILL.md` returns only `496d212`. It is an ancestor of c9ff09f.
- The section header at SKILL.md:2010-2011 ("Round23 addition …") is unchanged at c9ff09f.

## B2: every registry `source` resolves to a real commit that contains the cited text. HOLDS

Parsed `tools/registry.json` at c9ff09f: 54 rows (47 active, 7 superseded), no duplicate names. Six rows run `tools/command-binding.py`. All six `source` strings pass `SOURCE_RE` (registry-check.py:108).

| row (registry.json lines) | status | source | rev | cited content |
|---|---|---|---|---|
| command-binding-selftest (928-937) | superseded by -r24 | SKILL.md@496d212…:2019 | commit, ancestor of c9ff09f | SKILL row at 2019 |
| command-binding-frozen-clean (939-948) | superseded by -pinned | SKILL.md@496d212…:2019 | same | SKILL row at 2019 |
| command-binding-source-read-red (950-959) | superseded by -pinned | SKILL.md@496d212…:2019 | same | SKILL row at 2019 |
| command-binding-selftest-r24 (961-969) | active | fresh-adjudication.json@6a1821a…:53-59 | commit, ancestor | routed ArgvExact and MutationDesign items |
| command-binding-frozen-clean-pinned (971-979) | active | fresh-adjudication.json@6a1821a…:66 | commit, ancestor | "do not pin bundle_sha256 literals" |
| command-binding-source-read-red-pinned (981-989) | active | fresh-adjudication.json@6a1821a…:66 | commit, ancestor | same |

- `superseded_by` targets exist and are active for all three superseded rows. The registry validator accepted the file on every `--only` run.
- Fresh-adjudication lines 53-59, 66 and 74-93 hash to the same `sha256` (`124199ad…`) at 6a1821a and at HEAD. The cited content supports what the rows claim: a swapped-name supplemental case, and pinned `bundle_sha256` literals.

## B3: the public CLI is the same in the SKILL row and the entries. HOLDS

- Tokens match across SKILL.md:2019 and the registry argv (registry.json:930, 941, 952, 963, 973, 983). The gate is `--bundle … --expected … --json`. The selftest is `--selftest`. The red pair is `source-read-bundle.json` and `source-read-expected.json`.
- `main()` (command-binding.py:198-201) defines exactly `--bundle`, `--expected`, `--json` and `--selftest`, with `allow_abbrev=False`.
- Usage probes at c9ff09f, run from a `/tmp` export:
  - no arguments: exit 64, `--bundle and --expected are required`
  - `--selftest --json`: exit 64, `--selftest takes no other arguments`
  - `--bundle …` alone: exit 64
  - replay bundle with source-read expected: exit 2, `SNAPSHOT_TAMPERED`
  These match the SKILL verdict map (64 usage, 2 tampered).

## B4: the entries hold at c9ff09f. HOLDS for the active rows. The superseded selftest differs by design.

Direct runs in the `/tmp` export of c9ff09f:
- `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0.
- clean gate → exit 0, `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}`.
- red gate → exit 1, `{"bundle_sha256": "db620668…", "exit": 1, "finding_ids": ["ARGV_MISMATCH"], …}`.

Official runner, `python3 tools/registry-check.py --root /tmp/r25-rr23-reattack/lane --rev c9ff09f… --only NAME`. The lane was a `/tmp` clone with no `*-shokunin` siblings beside it; the JSON reports `live: false`.
- `ROW command-binding-selftest-r24 expect=0 got=0 held`, `REGISTRY_CHECK: held=1/1 superseded=0`
- `ROW command-binding-frozen-clean-pinned expect=0 got=0 held`, `held=1/1`
- `ROW command-binding-source-read-red-pinned expect=1 got=1 held`, `held=1/1`
- `command-binding-frozen-clean` (superseded): `got=0`. Its needle `"finding_ids": []` is present in the direct output.
- `command-binding-source-read-red` (superseded): `got=1`. Its needle `"finding_ids": ["ARGV_MISMATCH"]` is present.
- `command-binding-selftest` (superseded): `got=0`, but the `--json` fragment shows `held: false` and `stdout_missing: ["COMMAND_BINDING_SELFTEST: 38/38 pass"]`. It is excluded from N/M by design (registry-check.py:30-35; SKILL.md:2082: "fails against 44/44, and is excluded from the active tally").

## B5: the pinned digests. HOLDS

- `sha256sum` of `.ufo/evidence/round-23/replay/bundle.json` = `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9`. This matches the literal at registry.json:974.
- `sha256sum` of `.ufo/evidence/round-23/source-read-bundle.json` = `db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf`. This matches the literal at registry.json:984.

## B6: the outcome at the cited source commit. HOLDS for the selftest. Clean and red are not reproducible at 496d212 (RF1).

- At 496d212 the selftest run gives `38/38 pass`, exit 0. The superseded selftest expectation holds at its own source.
- At 496d212 the clean and red gates exit 2 with `INVALID_INPUT`, because their bundles are absent from that tree.
- `registry-check --rev 496d212 --registry <c9ff registry> --only command-binding-frozen-clean` → `expect=0 got=2`. For `command-binding-source-read-red` → `expect=1 got=2`.
- The same rows at `--rev 8f66b5d` → `got=0` and `got=1`.
- `git log --diff-filter=A` puts the first commit for each evidence file at 8f66b5d: `replay/bundle.json`, `replay/expected.json`, `source-read-bundle.json` and `source-read-expected.json`. `tools/command-binding.py` and `.ufo/evidence/round-23/extra-cases.json` were added at 496d212.

## B7: callers. HOLDS, with a literal-grep caveat

- No `lsp` device is available in this session. Callers were found with literal text search, which is a fallback and not semantic proof.
- Callers of `command-binding` in `tools/`, round-24 evidence and round-23 scripts: the six registry rows, the SKILL rows, `.ufo/evidence/round-23/measure.py`, `tools/registry-replay.py` (which builds bundles in the same schema at lines 111-126 and matches no gate invocation), and round-24 measurement artifacts (outside this item).
- `python3 .ufo/evidence/round-23/measure.py --repo <c9ff export>` → `discriminated 10 / 10`, exit 0. This matches the SKILL row's "frozen ten-case counter". The ruler uses only `--bundle`, `--expected` and `--json`.

## Residual findings (none is a counterexample)

- **RF1 (low, provenance).** The clean and red superseded rows cite 496d212. The SKILL row is there, so the text is right. But the evidence they execute was first committed at 8f66b5d, and at 496d212 they return `got=2` (B6). The bundles do declare 496d212 as their code revision, so that commit is the tested code. [INFERENCE] The registry's `source` field is a text-provenance pointer. Its format is validated, and its SKILL usage (`Source:` labels) is provenance text. Under that reading the binding holds. If the lane instead requires each `source` commit to reproduce its row's outcome, the clean and red superseded rows fail that stricter check at 496d212. I do not adopt the stricter reading.
- **RF2 (low, display).** For a superseded row, the human trailer prints only `expect` and `got`. `ROW command-binding-selftest superseded expect=0 got=0` looks green while the needle fails. The `--json` report is truthful (`held: false`), and SKILL.md:2082 documents the failure.
- **RF3 (low, provenance).** The SKILL row at 496d212 (line 2019) describes "source-read bundle/expected pair is expected1/ARGV_MISMATCH". That pair is absent at 496d212 and first committed at 8f66b5d. It is correct at c9ff09f (sha `db620668…`, exit 1, `ARGV_MISMATCH`). This is the same root cause as RF1.
- **RF4 (info).** `.ufo/evidence/round-23/pre-review-command-binding.py` is an older draft, not the committed tool. `diff` against `git show 496d212:tools/command-binding.py` produces only deletions, 22 lines in all. The committed tool has extra key-set checks in `evaluate()` and a fixture-loading loop in `selftest()`. No registry row and no SKILL row references the draft. Do not cite it as the CLI.
- **RF5 (info).** The red bundle's receipts declare the live lane root (`/home/vgpnk/Projects/shokunin/tameshi-shokunin`) as cwd. The replay bundle declares a `/tmp` fleet-mirror path. The gate only checks that bundle and receipts agree on cwd (command-binding.py:105-106). Its docstring (lines 11-13) says it does not establish producer authenticity. For these rows the red reason is the intended one: a source-read `cat tools/registry.json` is checked against a `tools/receipt-measure.py --selftest` requirement, giving `ARGV_MISMATCH`.

## Smallest safe correction

None is required for the attacked binding. Two optional notes, not applied (this report is the only file I wrote):
1. In the SKILL.md round-24 paragraph (around lines 2054-2056 or 2082), add one sentence: the round-23 clean and red evidence is first committed at 8f66b5d, and `registry-check --rev 496d212` grades those superseded rows `got=2`.
2. In registry-check's human trailer, print `needle-missing` for superseded rows, as `--json` already does with `held: false`.

## Verification gaps

- Not run: the full 54-row `registry-check` at c9ff09f. I ran only the six command-binding rows, with `--only`. The main agent may run the full battery once.
- Not run: `.ufo/evidence/round-24/measure.py` (the K-mutants) and `replay.py`. Both are outside this item.
- `registry-replay.py` was checked by literal grep only, not by execution.

## Lane hygiene and tooling

- Writes: only this report, at `.ufo/waves/round-25/w1/ReRegistryRegistration.md`. Every run was in `/tmp/r25-rr23-reattack`: `git archive` exports of c9ff09f, 496d212 and 8f66b5d; one `git clone --no-hardlinks` of the lane; `registry-check` runs in that clone; `measure.py` and selftests in the exports.
- Read-only git everywhere except one early `git status --porcelain`, which I ran without `GIT_OPTIONAL_LOCKS=0`. It may have refreshed the index stat cache. No content changed.
- No tools were installed or upgraded. I used the existing `python3` (3.14.8) and `git`.

R23-REATTACK RegistryRegistration: AGREE
