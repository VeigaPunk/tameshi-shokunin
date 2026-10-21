# RowAudit04 — round24 replay: five-row requirement/receipt audit

**Verdict: no false acceptance found in any of the five assigned rows.** For every row the
requirement carried in `observations.json` is byte-identical to the round-23 freeze, the receipt
reports `got == expect` and `held: true` with no cleanup error and no missing token, every required
stdout token is present in the full retained stdout, and the published `bundle.json` receipt is
byte-identical to the observation. An independent re-application of `command-binding.evaluate`
over those five bundle receipts yields zero findings, and the recorded gate receipt is exit 0,
`finding_ids: []`, over the digest-pinned bundle. Residual notes below are latent brittleness this
run did not exercise; none changes today's acceptance.

Scope: rows `bash-witness-count`, `evidence-disposition-selftest`, `measure-round16-selftest`,
`trace-inputs-selftest`, `round20-coldread-selector-selftest`. Replay revision
`d2eaecd443bf5f4e387e7e5331282e3d11dea047`; delivered revision
`c8c5b88c8e961a929cdc351b95a7074c76958909`.

## Axes

1. Requirement fidelity — `observations.row.requirement` vs `.ufo/evidence/round-23/requirements.json`.
2. Receipt fidelity — `runner_result` exit / full stdout / held, and `bundle.json` receipt congruence.
3. Binding semantics — does `held: true` actually mean "exit matched and all tokens matched"?
4. Provenance — was the run made with the frozen inputs, on the pinned tool blobs, at the claimed revision?
5. Selftest-inventory congruence — can the retained stdout be produced by the source version it claims?

## Method and provenance chain

- Frozen requirement file: `.ufo/evidence/round-23/requirements.json` sha256
  `cd5205be9e5843e956191f673e620875f6f9c65a4c8ed9f224e656601a25a1e3`; registry baseline
  `.ufo/evidence/round-23/registry-baseline.json` sha256
  `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a` — equals
  `requirements.json.registry_sha256` and `observations.registry_sha256`.
- The baseline is not a doctored subset: all 47 baseline row dicts (`argv`, `expect`, `kind`,
  `status`, `source`, `timeout_s`) compare equal to `tools/registry.json` at the frozen
  `source_revision` `28cae179e4dc2c1fa7f032a79cdddf0b5d862d76` (47 rows, 43 active, zero field
  differences). The 43 frozen requirements equal the 43 `status=="active"` baseline rows in
  order, compared as whole objects. Both files are unchanged since round-23 final `6a1821a`
  (`git diff --stat 6a1821a c8c5b88 --` over the two paths is empty).
- `run_replay` refuses on a baseline-digest mismatch (`tools/registry-replay.py:140`), on
  `requirements != active baseline rows` (`:145`), and on a clone HEAD that differs from the
  requested revision (`:158`).
- `d2eaecd` is an ancestor of the delivered `c8c5b88`. `git diff --name-only d2eaecd c8c5b88`
  lists 26 files, all `.ufo/evidence/**` (+6019/−0). No tool, registry, `SKILL.md` or corpus file
  changed, so the replay at `d2eaecd` exercises the delivered code.
- All five audited tools are byte-identical across the whole window: `git diff --stat
  6a1821a d2eaecd` and `git diff --stat 28cae179 d2eaecd` over
  `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/trace-inputs.py`,
  `.ufo/evidence/round-16/measure.py`, `.ufo/evidence/round-20/coldread/measure.py` are empty.
- Runner identity: `observations.runner_sha256_clone_copy` =
  `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad` for
  `tools/registry-check.py` in the clone. Replay instrument `9fcd2dbb…` equals both
  `replay-command.json.instrument_sha256` and the on-disk `tools/registry-replay.py` sha256.
- Run window `2026-10-21T15:56:41.156263Z – 16:01:01.739310Z`. Each of the five row intervals
  lies inside it, row intervals do not overlap, and each interval length equals its reported
  `elapsed_s` to within 0.4 ms (0.388/4.422/1.454/2.464/0.997 s).
- Evidence files on disk are the committed blobs: sha256 of `observations.json`
  (`2d9b1b77…`), `bundle.json` (`4f424023…`), `expected.json` (`8fc9342e…`), `replay-gate.json`
  (`73ca96f0…`) and `replay-command.json` (`6dfc45ae…`) equal `git show c8c5b88:<path>`.
  `git status --porcelain` shows only untracked `.ufo/waves/round-24/`.

## Per-row result

| row | frozen requirement (`requirements.json` line) | got / held | required tokens | decisive receipt evidence |
|---|---|---|---|---|
| `bash-witness-count` (`:54`) | `python3 tools/bash-witness-study.py count`, exit 0 | 0 / true | `unresolved\tnone` 1/1 | 1763-byte stdout, stderr empty; final line `unresolved\tnone`; declared digest line `0def0d3b370288f5…` equals sha256 of `.ufo/evidence/round-12/BashWitness/declared.tsv`; all 10 row lines plus `counts killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10 witness_classified=10` and `declared_none B5,B10` match `summary.json` field-for-field; stored `status=complete`, `counts.unresolved=[]`; zero `FAIL` |
| `evidence-disposition-selftest` (`:182`) | `python3 tools/evidence-disposition.py --selftest`, exit 0 | 0 / true | `SELFTEST: PASS` 1/1 | 4129-byte stdout, stderr empty; 66 `SELFTEST_CASE … PASS` lines, 66 unique names, every name present as a literal in the tool's selftest body; final line `SELFTEST: PASS (66/66)`; `tools/evidence-disposition.py:3119` returns 1 on any failed case and prints `SELFTEST: FAIL`, `:3123-3124` prints PASS and returns 0 only when `failed` is empty |
| `measure-round16-selftest` (`:305`) | `python3 .ufo/evidence/round-16/measure.py --selftest`, exit 0 | 0 / true | `MEASURE_SELFTEST:` 1/1 | 1065-byte stdout, stderr empty; 38 `PASS` lines, 0 `FAIL`; the 38 literal `check('…')` names in `.ufo/evidence/round-16/measure.py` equal the 38 observed names, zero difference; final `MEASURE_SELFTEST: 38/38 pass (scratch /tmp/tameshi-r16-CRMeasure-f5c0w6q7)`; return coupled at `:625-626` (`0 if passed == len(checks) else 1`) |
| `trace-inputs-selftest` (`:417`) | `python3 tools/trace-inputs.py --selftest`, exit 0 | 0 / true | `SELFTEST: ` 1/1 | 783-byte stdout, stderr empty; 30 `PASS` lines, 0 `FAIL`; the 30 literal `check('…')` names in `tools/trace-inputs.py` equal the 30 observed names; final `SELFTEST: 30/30`; return coupled at `:965-967` |
| `round20-coldread-selector-selftest` (`:529`) | `python3 .ufo/evidence/round-20/coldread/measure.py --selftest`, exit 0 | 0 / true | `SELECTOR_SELFTEST: 12/12 pass` 1/1 | 543-byte stdout, stderr empty; 12 `CASE … PASS` lines = 3 positive scenarios + 9 `override-refused:*` cases generated by the source loop; final `SELECTOR_SELFTEST: 12/12 pass`; return coupled at `:98-99` |

Requirement equality was checked on the whole object (`name`, `argv`, `expect`), not just the name:
all five `observations.row.requirement` objects compare equal to their `requirements.json` entries;
`observations.row.argv == requirement.argv` for all five (no re-quoting); `external` is `false`
and there is no `non_hermetic_argv` for any of the five.

## Binding semantics (why `held: true` is not self-vouching)

- `tools/registry-check.py:720`: `held = got == expected_exit and not missing and cleanup_ok`.
  `missing` is every required token absent from the **full** decoded stdout (not the 4096-byte
  tail), and `cleanup_ok` covers descendant cleanup. For all five rows `stdout_missing`,
  `cleanup_error`, `error` and `non_hermetic_argv` are absent; `stderr` is empty and `got == 0`.
- `tools/registry-replay.py:87-90`: a cleanup error becomes `RUNNER_CLEANUP_FAILED` and any
  `held is not True` becomes `RUNNER_NOT_HELD`; either refuses to publish a bundle. All 43 rows
  report `held True` on the console receipt (`replay-command.json`, 44 lines, final JSON
  `finding_ids: []`), and every one of the five appears there as `name 0 True`.
- Independent re-binding: applying `tools/command-binding.py:103-112` to the five bundle receipts
  gives no `ARGV_MISMATCH`, `CWD_MISMATCH`, `REVISION_MISMATCH`, `EXIT_MISMATCH` or
  `STDOUT_MISMATCH`; the recorded gate run is exit 0, `finding_ids: []`,
  `bundle_sha256 4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`, equal to
  `replay/expected.json`. Bundle receipts match the observations byte-for-byte on `stdout` and
  `stderr` and on `exit == got` for the five rows.
- Caveat: the bundle is a projection of the same observations. The gate re-checks the retained
  declaration against the requirement, not a re-execution; `command-binding.py` states this and
  claims no producer authenticity.

## Falsification attempts

1. **Weak prefix tokens could mask a partial selftest** (`MEASURE_SELFTEST:`, `SELFTEST: `).
   Refuted by exit coupling: `measure.py:626` and `trace-inputs.py:967` return 1 whenever
   `passed != len(checks)`, and the requirement also demands exit 0. Observed tallies are
   `38/38` and `30/30`; a failing run would print the prefix but exit 1, so `held` would be false.
2. **Crash-as-success on `bash-witness-count`.** Refuted: `cmd_count` re-parses `declared.tsv`,
   verifies its digest, recomputes every row and count from the raw sweep, and raises `Fail` on
   any summary/raw or count mismatch (`tools/bash-witness-study.py:1051-1123`); only then does it
   print `unresolved\t<ids|none>` and return `EXIT_FAIL if tally["unresolved"] else EXIT_OK`
   (`:1124-1125`). Exit 0 therefore implies `status complete` and an empty unresolved list, which
   the stored `summary.json` confirms. The in-stdout declared digest equals the actual file hash.
3. **Token smuggled from stderr or a tail.** Refuted: tokens are stdout-only; stderr is empty for
   all five; each token is found in the retained full stdout (positions 1747/1763, 4106/4129,
   990/1065, 767/783, 513/543), and for `evidence-disposition-selftest` the 4129-byte stdout is
   larger than the 4096-byte tail, yet the check ran over the full stream (the tail also contains
   the token).
4. **Stale or forged receipt.** Refuted on the available static evidence: the per-run clone path
   `/tmp/tameshi-registry-replay-dzo3ypiq/...` appears both in the observation `cwd` and in the
   `bash-witness-count` stdout; per-row interval length equals `elapsed_s` to <0.5 ms; intervals
   are disjoint and inside the recorded run window; runner/instrument digests pin the executing
   files; on-disk evidence blobs equal the committed blobs. This is consistency, not producer
   authentication.
5. **Revision substitution.** Refuted for these rows: the replay ran at `d2eaecd`, but all five
   tool blobs are byte-identical from the round-23 freeze through the delivered `c8c5b88`, and
   the only commits after the replay add evidence files. Receipts therefore describe the
   delivered code.
6. **Weakened requirement set.** Refuted: baseline digest, baseline-vs-`registry.json@28cae179`
   full-row equality, frozen-vs-active-row equality, and the replay tool's own three refusal
   gates. Note: the 43-row freeze excludes three round-23 rows that were added after
   `28cae179` (`command-binding-frozen-clean`, `command-binding-selftest`,
   `command-binding-source-read-red`); they are `superseded` in the live registry by pinned
   successors and are not among my five. The replay covers 43 frozen rows, not the 47 live active
   rows — scope, not a row-level false acceptance.
7. **Selftest inventory substitution.** Refuted for plausibility: the four selftest outputs
   reconcile exactly with the source inventories (38/38, 30/30, 66/66 unique names all literal in
   the source, 12 = 3+9 cases), so a different inventory would show unknown names or a different
   tally. This is congruence, not proof the run executed those exact bytes.
8. **Token-valid but degraded bash study.** Real but unexercised: `unresolved\tnone` is
   insensitive to the survivor count (today `survived=2`, `inconclusive=0`); an all-survived
   frozen sweep would still exit 0 and print the token. This is an adequacy limit of the round-23
   freeze (the row is a regression check over a frozen evidence directory), not a false
   acceptance in this receipt; tightening it needs a new requirements revision.

## Row-scope caveats (do not over-read this audit)

- These five rows are unchanged round-23 requirements; their receipts are regression evidence
  (no drift), not round-24 hardening and not calibration uplift.
- `bundle.json.cwd` is the temp clone path, now deleted; `command-binding.canonical_cwd` is
  lexical, so cwd binding is self-consistency, not existence. Reproducibility rests on the
  revision pin `d2eaecd`, which is present in history.
- `replay/live-dependent.json` lists only `pin-disposition-read` and `verify-round15`; none of
  the five rows names an absolute live-fleet path or is flagged `non_hermetic_argv`.
- `held` is runner-reported. The gate and this audit can validate the declaration's internal
  consistency and the pinned source/tool identities, not that a producer ran the commands.

## Smallest safe correction

None required for this wave's acceptance. If a later wave wants stronger row tokens, tighten them
in a new frozen requirements revision (for example `MEASURE_SELFTEST: 38/38 pass`,
`SELFTEST: 30/30`, `SELFTEST: PASS (66/66)`, and `unresolved\tnone` paired with the counts line) —
do not edit the round-23 freeze in place.

## Tooling / bounds

No installs or upgrades. Read-only inspection only: `read`, `grep`, read-only `git
cat-file`/`show`/`diff`/`status` with `GIT_OPTIONAL_LOCKS=0`, and in-memory Python over the
evidence JSON. No registry battery, gate, or selftest was executed in the repo; no writes outside
this report.
