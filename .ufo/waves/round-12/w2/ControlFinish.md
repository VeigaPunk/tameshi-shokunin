# ControlFinish — round-12 w2 — repeat-control.py scoped defect fixes (advisory)

Seat: ControlFinish (executor, leaf). Advisory, lane-internal. Not an independent
non-author admission, promotion, or pass. No commit, no fleet write, no LOG edit.

## Owned scope

- `tools/repeat-control.py` (rewritten in place; no reimplementation).
- `.ufo/evidence/round-12/ControlGate/expected.json` and
  `.ufo/evidence/round-12/ControlGate/mismatch/expected.json` (assigned by Main/L1 after
  the inherited directory shipped without them).
- This report.

## Inputs read

- `tools/repeat-control.py` in full (790 lines at pre-edit sha
  `29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a`).
- Inherited reviews: `.ufo/waves/round-12/w1/ExitReview.md`, `BytesReview.md`,
  `GateSecurity.md`, `SnapshotReview.md`; `.ufo/waves/round-12/w2/ControlSecurity.md`.
- Evidence: `.ufo/evidence/round-12/SnapshotReview/probe-output.txt:10` (duplicate-key
  row), `.ufo/evidence/round-12/GateSecurity/probes.out` (P3 FIFO/symlink, P5 exec,
  P7 pipe, P8 leftover writer).
- L1 IRC rulings received in-session: duplicate-key refusal + CLI arm; snapshot is
  read-only observation reclassification (no argv execution); a run-mode DIR is not a
  frozen snapshot; F2 doc-vs-code choice; existing-out / nonzero-precedence /
  strict `expected_exit` / `/tmp` scratch; CC1 `/dev/full` class integrity; CC2
  background-pipe correction; S2 `expected.json` regular-file check; keep scoped.
- `/home/vgpnk/.omp/agent/RULES.md` (no install needed).
- I did not read any secret or session material.

## Axes walked

1. Finding-class conformance (exit map, disagreement-before-baseline, usage arms).
2. Snapshot trust boundary (manifest parse ambiguity, regular-file records, tamper arms,
   committed pins).
3. Documentation truth (selftest exit semantics, PIPE/background behavior, run-mode vs
   frozen snapshot).
4. Class integrity of the tool's own output path (a refused terminal must not fabricate
   or reclassify a verdict).

## Changes (all in `tools/repeat-control.py`)

1. **Duplicate manifest keys were silently last-wins.** Evidence:
   `SnapshotReview.md:25` (R2), `:34` (F-A "Required fix: reject duplicates"), and
   `SnapshotReview/probe-output.txt:10` ("strict must refuse duplicates"); reconfirmed by
   ControlSnapshot to L1 against `load_snapshot`. A duplicate `"inputs"` key makes the
   digest pin itself ambiguous. Fix: `reject_duplicate_keys` (`:352-358`) is passed as
   `object_pairs_hook` to `json.loads` (`:374`); a duplicate anywhere in the record raises
   `TamperError` → `snapshot_tampered`/2. New selftest arm copies the stable fixture and
   inserts a second, empty `"inputs"` key before the real one, so a last-wins parser would
   still verify and pass (`:806-815`). The docstring now counts six tamper arms (`:76-79`).

2. **`expected.json` was opened without the regular-file check the run files get.**
   Evidence: ControlSecurity S2 (`.ufo/waves/round-12/w2/ControlSecurity.md:47-57`), P3:
   a symlinked record is followed; a FIFO record blocks `open()`. Fix: `lstat` +
   `S_ISREG` on the manifest before reading (`:361-372`); a symlink, FIFO, directory or
   missing record raises `TamperError`. Selftest arm commits `expected.json` as a symlink
   to the intact fixture record (`:817-829`); the observation-symlink arm
   (`:831-843`) also exercises the pre-existing `read_checked` `S_ISREG` branch (`:418`).
   Residual: the `lstat`→`open` race (ControlSecurity's `O_NOFOLLOW` helper) is not
   closed; the committed-symlink presentation is rejected.

3. **`expected_exit` accepted non-integer JSON numbers.** `0.0 == 0` let a float pair
   pass the "stable pair" check. Fix: `expected_exit` must be a non-bool `int` before
   equality (`:383-390`); the recorded exit is still never used as the process exit.

4. **No selftest arm for the existing `--out` refusal (exit 64).** Evidence:
   ControlSecurity S4 (`ControlSecurity.md:72-75`); the refusal is implemented at
   `run_controls` (`os.makedirs(..., exist_ok=False)`). Fix: a pre-created empty out dir
   is passed to a child invocation, expecting `invalid_usage`/64 (`:748-756`), with
   `check_existing_out_untouched` (`:676-681`) asserting the refused directory stays
   empty (so `command.txt` is not written either).

5. **No arm pinned disagreement-before-baseline for differing nonzero exits.** Evidence:
   `ExitReview.md` Addendum (`[1,2,1]`/`[1,0,1]` must be `controls_mismatch`/1, not
   `baseline_nonzero`/2). Fix: `MISMATCH_NONZERO_EXITS_SH` exits 1,2,1 with identical
   stdout/stderr (`:520-527`), registered at `:553`, asserted
   `controls_mismatch`/1 at `:703-708`.

6. **Selftest doc claimed exit 2 for a "damaged" committed fixture, code records a FAIL
   and exits 1.** Evidence: ControlSelftest F2 via L1. Chosen behavior: exit 2 only when
   `EVIDENCE_ROOT` is not a usable directory; content damage is a failing case → exit 1.
   Doc corrected (`:79-81`); the could-not-evaluate message now matches
   (`:595`).

7. **Selftest scratch was not pinned to `/tmp`.** Lane scratch rule via L1. Fix:
   `tempfile.mkdtemp(..., dir="/tmp")` (`:597`), matching the docstring's stated
   `/tmp/tameshi-r12-repeat-control-selftest.*` location.

8. **A refused stdout/stderr could turn any class into exit 1 (or 120 at shutdown).**
   Evidence: ControlCritic CC1 via L1 (`/dev/full` secondary error). `emit`/`emit_err`
   now swallow `OSError`/`ValueError` from their own writes (`:152-166`), including
   `UnicodeEncodeError` (a `ValueError` subclass, closing the ControlSecurity S5(a)
   divergence shape); `main` flushes both streams and swaps any still-refusing stream for
   `/dev/null` before interpreter shutdown, preserving the computed status (`:890-909`);
   the `--help` text also goes through `emit` (`:885`). The finding class is now
   independent of terminal acceptance.

9. **Doc claimed a background writer can append to a finished run file.** False under
   PIPE capture (CC2 via L1; GateSecurity `probes.out` P7a measured a 4.0 s delay, P8
   showed the pipe held open). The limitation text now states that a held-open
   stdout/stderr delays or hangs the gate, and that shared background state (files,
   ports, locks) can still change later runs (`:84-89`). The docstring's
   `snapshot_tampered` sentence now also states that a run-mode DIR
   (command.txt/finding.txt, no expected.json) is not a frozen snapshot and is refused
   (`:56-57`), per the L1 read-only reclassification ruling.

No other behavior was changed; `classify`, run-mode argv splitting, `OSError` →
`command_unavailable`, byte comparison, `--out` creation/`xb`, and the snapshot
recompute path are untouched.

## New files (frozen pins)

Authored from the nine existing observation files in each directory; expected IDs
specified independently of observation, not recorded from a gate run:

- `.ufo/evidence/round-12/ControlGate/expected.json` — `runs=3`,
  `expected_id=controls_match`, `expected_exit=0`, 9 digests. Its own sha256:
  `1b645be04d756c304a1ef5ecc221cf92f82c5f4afbdcfde4b77fe27117684aa1`.
- `.ufo/evidence/round-12/ControlGate/mismatch/expected.json` — `runs=3`,
  `expected_id=controls_mismatch`, `expected_exit=1`, 9 digests. Its own sha256:
  `57f010e99e69a6632869c125229f8bcf0cfdaf866b6dcab9f16ed07ebc8f6771`.

Authoring-integrity comparison (not a gate run): a local script hashed all 18 frozen
observation files against the manifest values and reported `digest disagreements: 0`.
The stable directory holds three identical `stable-*` observations plus the allowed
`mismatch/` subdirectory (skipped by the listing loop by design, per L1); the mismatch
directory differs only in `run-3.stdout`.

## No-change decisions (with reasons)

- **Unbounded `runs` in a tampered manifest** (ControlSecurity S3): not routed by L1 and
  no schema bound exists; a cap would be invented. Residual: `runs=10^12` builds the
  required-name set before the inputs check, so a hostile snapshot can hang or OOM
  instead of returning `snapshot_tampered`. Smaller fix if wanted later: check
  `len(inputs) == 3 * runs` before building `required`.
- **`read_checked` EACCES on a run file** raises out of `recompute_snapshot` and is caught
  by `main` as `setup_error`/2, not `snapshot_tampered`/2. Same exit class; the ID
  differs. Not ordered; no probe exists for it.
- **ControlSecurity S5** (`REPEAT_OUT`/`cwd` line injection; `REPEAT_OUT` emitted after
  `finding.txt`): not ordered; the encoding-divergence half is closed by change 8, and
  last-line consumers (`last_finding_id`) are already safe. Atomic emit ordering is not
  changed.
- **S6** (`--out ""` and >4300-digit `--runs` → `setup_error` instead of `invalid_usage`),
  **S7** (unlisted directories / symlinks-to-directories ignored), **S8** (non-canonical
  `exit` spellings like `00\n` accepted): not ordered; S7 is partly required by design
  (root contains `mismatch/`). Named, not silently dropped.
- **Interrupt handling / process-group kill** (GateSecurity C4): no supervisor is the
  documented boundary; no `KeyboardInterrupt` handling was added.
- **TOCTOU after `lstat`** for the manifest and run files: residual; `O_NOFOLLOW`
  `fstat`-then-read helper is ControlSecurity's stronger proposal, not the ordered S2.
- **BytesReview 20-case table**: observed at tool sha `d45d8e39…`, which is not the
  pre-edit sha (`29d80254…`) and not the final sha. Those observations no longer apply
  and must not be cited for this file; L1 re-run owns them.

## Verification status

- No gate, `--selftest`, `--snapshot`, or experiment was run (not assigned; L1 owns
  integrated checks). No build, lint, formatter, or test suite was run.
- Only checksum facts were executed: `sha256sum` of the changed files and the
  authoring-integrity digest comparison above.
- Final `tools/repeat-control.py` sha256:
  `fb297a266b430093595c7639cf1ba22fa74fa77e7a306293e297e023666974e1`.
- Pre-edit sha for traceability:
  `29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a`; BytesReview's
  `d45d8e3948c24c2f6b2afcc336a5a44d2119e66b32eaea9fbe5c9eb08807d17d` and
  ControlSecurity's `29d80254` are both superseded.

## Risks / blockers

- The manifests are untracked until L1 commits them; the self-referential-digest limit
  (docstring `:90-92`) means the external anchor is the repository history, which does
  not exist for these paths yet.
- The six tamper arms and the new selftest expectations are authored but unexecuted at
  this sha. Their expected IDs follow the code paths read here, not an observed run.
- Both committed snapshots now depend on the listing tolerance for the `mismatch/`
  subdirectory; moving that directory or adding another entry under `ControlGate/` will
  produce `snapshot_tampered` (stable) as designed.
- `ControlGate/` also contains `mismatch/`, so `--snapshot` of the stable root is not a
  directory-empty check; this is the inherited layout, not a new fixture.

## Owned paths written

- `.ufo/waves/round-12/w2/ControlFinish.md` (this report)
- `tools/repeat-control.py`
- `.ufo/evidence/round-12/ControlGate/expected.json`
- `.ufo/evidence/round-12/ControlGate/mismatch/expected.json`

No LOG.md entry (L1 owns the round entry); no commit; no sibling/fleet file touched.
Tooling: nothing installed or updated.

## Peer re-review (advisory, not authority)

ControlSecurity re-read the changed code at sha `fb297a26…74e1` and re-hashed both
snapshot directories without running the gate or selftest: its appended re-review in
`.ufo/waves/round-12/w2/ControlSecurity.md` closes S1, S2 and S4 and independently
confirms all 18 recorded digests match with no unlisted file. It keeps S3, S5, S6, S7,
S8 and the `lstat`→read race as open residuals — the same list recorded above. This is
peer observation only; no gate run exists yet, and the pins remain untracked until L1
commits them.
