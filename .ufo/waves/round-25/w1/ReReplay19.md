# ReReplay19 — re-attack of round-23 Replay19 (row `measure-round16-rev`)

## Verdict

FINDING. The row's argv and expect are statically bound exactly, but `command-binding.py`
accepts the row's revision field without any evidence that the command measured that revision.
The receipt `revision` is copied from the same Python variable as the bundle `revision`
(`replay.py`), and the command's own stdout reports the symbolic `"revision": "HEAD"`. A receipt
whose stdout is the measurement of a different commit, even one whose stdout names that other
commit, is still accepted as CLEAN. The finding still applies at lane revision `c9ff09f`: the
registry row is byte-identical, `measure.py` is unchanged, and the round-25 binding gives the same
results. Round 24's replay carries the same gap forward.

For this specific frozen receipt, the evidence is genuinely present. I reproduced it
independently. That came from my own re-measurement, not from anything the binding checks.

## What was checked (static binding — holds)

- `round-23/requirements.json` row `measure-round16-rev` is equal to `replay/bundle.json`
  `requirements[18]`, and to the row in `registry-baseline.json` at
  `source_revision 28cae17`. That registry's sha256 is `ebd2e69a…` and matches `registry_sha256`.
  - argv: `python3 .ufo/evidence/round-16/measure.py --rev HEAD --repo .`
  - expect: `exit 0` with `stdout_contains ["\"calibration_restraint_score\":", "\"coldread\":"]`
- Baseline source `SKILL.md@98bea7d:1811` is the round-16 registry line
  `` `python3 .ufo/evidence/round-16/measure.py --rev REV` · `--selftest` | 0 measured · 2 rev/blob missing · 64 usage ``.
  The frozen argv instantiates `REV` as the symbolic `HEAD`, and `exit 0` matches "measured".
  The stdout tokens are not in that source. Line 1803 names the counting field
  `coldread.box3_full_page`, and the expect does not bind it.
- Bundle sha256 `3d6c99b7…` equals `replay/expected.json`. Receipt 18 is the only receipt with
  this name. Its argv, cwd (`/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`), revision
  `496d212…` and exit 0 match the bundle.
- The full output is retained. Receipt stdout (8110 chars, stderr empty) is byte-equal to
  `observations.json rows[18].runner_result.stdout`, and the 4096-char `stdout_tail` is its suffix.
  The judgement here used full stdout, not tails.
- Invocation metadata for this row is newly retained by the round-23 replay
  (`measurement_interval 14:44:34.673→14:44:34.780`, inside the run interval). It is not a retrofill
  of historical observations: `replay.py` builds every receipt field from the rows it ran itself
  (`replay.py:57-71`). This does not authenticate the producer, and I make no such claim.

## Field-level false acceptance: `revision`

- `replay.py:32` resolves `revision` once from the source repo. `replay.py:63` stores that value in
  each observation, and `replay.py:66,69` copy it into both `bundle.revision` and
  `receipt.revision`. Nothing re-reads the clone's HEAD after `checkout --detach` (`:50`), or
  around each row.
- `command-binding.py:107` only compares `receipt['revision'] != bundle['revision']`. For a
  replay-produced bundle, that comparison can never fail.
- `measure.py:647-660` runs `rev-parse --verify` but discards the resolved SHA, and then measures and
  prints `args.rev` verbatim. The retained stdout therefore says `"revision": "HEAD"`, so the output
  does not identify which commit was measured.
- The binding never compares stdout to the revision. `stdout_contains` only checks two key names,
  so any values pass (`command-binding.py:111`).

### Adversarial delta (executed, /tmp scratch only)

I cloned the lane with `git clone --no-hardlinks` into `/tmp/rereplay19-ZYif`, detached it at
`496d212`, and ran the read-only probe with explicit SHAs (not the registry argv):

- `measure.py --rev 496d212… --repo .`: exit 0. Its stdout is byte-identical to the retained receipt
  stdout once `"revision": "<sha>"` is replaced by `"HEAD"`.
- Over the first 39 first-parent ancestors, 0 give byte-identical normalized stdout. The parent
  `15ae602…` differs at `sources.rows 81→80`, `status.mined 52→51` and `tiers.A 72→71`. The
  retained stdout therefore does identify `496d212`, but only my re-measurement shows it.

I then rewrote `receipts[18]` and re-pinned `expected.json` to each new digest, as the trusted
caller would. I ran both binding versions on each case: the round-23 binding (`git show 496d212:tools/command-binding.py`,
sha256 `d533dc1e…`) and the lane binding at `c9ff09f` (sha256 `9230c68e…`, the same as the working tree).

| receipt[18] edit | r23 binding | c9ff09f binding |
|---|---|---|
| none (control) | exit 0 `[]` | exit 0 `[]` |
| stdout = parent `15ae602` measurement, labelled `HEAD` | exit 0 `[]` | exit 0 `[]` |
| stdout = parent measurement, literally `"revision": "15ae6029…"` | exit 0 `[]` | exit 0 `[]` |
| stdout = `{"calibration_restraint_score": 0, "coldread": null}` | exit 0 `[]` | exit 0 `[]` |
| stdout = `error: "calibration_restraint_score": "coldread": unavailable` | exit 0 `[]` | exit 0 `[]` |
| stdout lacks `"coldread":` (negative control) | exit 1 `STDOUT_MISMATCH` | exit 1 `STDOUT_MISMATCH` |

Row 3 is the strongest counterexample: the receipt declares `revision 496d212`, its full stdout
says it measured `15ae602`, and the binding reports CLEAN. Rows 4 and 5 show that the token
expectation accepts a zero score, a null cold-read, and non-JSON text.

I did not observe whether the clone's HEAD actually moved during the round-23 run. `mutate-and-run.sh` has no
checkout, reset or switch on its caller repo (a grep for `git … checkout|reset|switch|stash|commit|worktree`
found only comments at `:256` and `:1110`), and the byte-identity reproduction above is consistent
with HEAD having been `496d212` when row 18 ran. **[INFERENCE]** For this frozen receipt, the gap is
latent and did not cause a wrong acceptance.

## Status at lane revision c9ff09f

- `tools/registry.json` row `measure-round16-rev` is byte-identical at `28cae17`, `496d212`,
  `1f73157` and `c9ff09f`: argv, expect, `source SKILL.md@98bea7d:1811`, `status active`. It has not
  been superseded.
- `.ufo/evidence/round-16/measure.py` has sha256 `03b67f58…` at all four revisions.
- `tools/command-binding.py` changed between `496d212` and `c9ff09f` only in its selftest fixture loop,
  which now also loads `round-24/extra-cases.json`. `evaluate()` is unchanged, and the table above
  shows identical results.
- Round 24 carries the gap forward. In `round-24/replay/bundle.json`, the bundle and receipt
  revisions are both `d2eaecd…`, and the stdout says `"revision": "HEAD"`.

## Smallest safe correction

Correct it at the row, not in the shared binding. Freeze the argv to the full SHA that the replay
checks out, and require that SHA in stdout. In practice, the replay instrument should instantiate
`--rev <revision>`, and the expect should add `stdout_contains: ["\"revision\": \"<revision>\""]`,
because `measure.py` echoes `args.rev`. This makes the command's own output carry the measured
revision, and the binding's existing `STDOUT_MISMATCH` path would then reject row 3 above.

If the registry must keep `HEAD`, a smaller fix is in `replay.py`: record the clone's
`git rev-parse HEAD` immediately before and after each row as the receipt revision, instead of
copying the outer variable. This makes `REVISION_MISMATCH` reachable, but it is still metadata
asserted by the instrument and does not bind stdout.

Tightening the tokens (for example `"box3_full_page": `, the counting field named at
`SKILL.md@98bea7d:1803`) is a separate tradeoff that the judge should weigh. It is not required to
close the revision gap.

## Tooling

No tools were installed or updated. I wrote nothing outside this report and the `/tmp` scratch,
which I have since removed. No git or jj write commands were run in the lane, and no registry
command or suite was run.

R23-REATTACK Replay19: FINDING
