# ControlSnapshot — tameshi round 12, wave w2 (read-only review)

Advisory, lane-internal. Not an independent non-author review and not an admission.
Scope: the `--snapshot DIR` path of `tools/repeat-control.py` (sha256 `29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a`, 790 lines, untracked at HEAD `18ad5d0`) and the pinned expected files it reads.
Method: code reading and file inventory only (`read`, `grep`, `find`, `od`, `sha256sum`). The gate was not executed; no selftest, no snapshot run, no build, no test. Every behavioral statement below is `[INFERENCE]` from code unless marked observed.

## Observed inventory (O)

- `find . -name 'expected*.json'` → no match in the repo.
- `.ufo/evidence/round-12/ControlGate/` holds only `run-{1,2,3}.{stdout,stderr,exit}` and `mismatch/` holds only `run-{1,2,3}.{stdout,stderr,exit}`. Byte content is as the child would print: `stable-out\n` / `stable-err\n` / `0\n`; mismatch run-3 stdout is `mismatch-out-changed\n`.
- `git ls-files .ufo/evidence/round-12` → 0 tracked files. All round-12 evidence is untracked.
- `grep object_pairs_hook tools/repeat-control.py` → no match.

## Findings (by severity)

**F1 (high). The pinned expected files the gate and selftest rely on do not exist.**
- `tools/repeat-control.py:337-341` — `load_snapshot` reads `expected.json`; any `OSError` becomes `TamperError`.
- Docstring claims committed snapshots live at `ControlGate/` and `ControlGate/mismatch/` (`tools/repeat-control.py:60-62`, `:73-75`). Neither directory has an `expected.json`.
- `[INFERENCE]` `--snapshot .ufo/evidence/round-12/ControlGate` → `snapshot_tampered`, exit 2. Selftest cases `snapshot-committed-stable` (`:737`, expects 0) and `snapshot-committed-mismatch` (`:738-743`, expects 1) therefore fail, and `--selftest` returns 1 (`:747-749`). The docstring's "committed snapshots" claim is unmet.
- The external anchor the docstring names — "the repository's committed history" (`:84-85`) — is also unmet: round-12 evidence is 0 tracked files (O above).

**F2 (high). Duplicate keys in the pin are accepted (last-wins). Required fix R2 is not implemented.**
- `tools/repeat-control.py:343` — `json.loads(raw.decode("utf-8"))` with no `object_pairs_hook`; `grep` confirms none exists.
- Consequence: a second `"inputs"` key silently replaces the first. A pin whose first `"inputs"` holds the good digest and whose last `"inputs"` holds the edited digest is verified against the edit. This is the same ambiguity as probe F (`.ufo/evidence/round-12/SnapshotReview/probe.py:116-133`; `probe-output.txt` row F: "first-pin=good -> BAD").
- Requirement source: `.ufo/waves/round-12/w1/SnapshotReview.md:24-26` (R2) and `:34` (F-A, "Required fix: reject duplicates"). Not implemented.

**F3 (medium). "Absence of unlisted input" does not cover subdirectories or directory-symlinks.**
- `tools/repeat-control.py:364-367` — `listed` is built only from entries where `os.path.isdir(...)` is false. Subdirectories are never listed, so `extra` (`:368-370`) never sees them.
- Consequence: `ControlGate/mismatch/` is silently ignored when `ControlGate/` is validated, so its contents are outside the pinned inputs for the stable snapshot. Any arbitrary subdirectory added to a snapshot DIR is accepted. A symlink to a directory is also `isdir`-true and is skipped.
- Contradicts the stated contract "every unlisted file … exits 2" (`:58-59`) for any non-regular entry. Only regular-file extras are caught.

**F4 (medium). Coverage of "every input": the command under control is not pinned, and run-mode output cannot be frozen.**
- `expected.json` schema (`:346-360`) has `runs`, `expected_id`, `expected_exit`, `inputs` only. No argv, cwd, or tool identity is pinned. The w1 proposal carried `argv` (`.ufo/waves/round-12/w1/SnapshotReview.md:81`); it was dropped without a recorded decision.
- Run mode writes `command.txt` (`:306`) and `finding.txt` (`:323-326`) into the same DIR. Snapshot mode rejects any extra regular file (`:368-370`). `[INFERENCE]` a DIR produced by `--out` is therefore rejected as `snapshot_tampered` unless those two files are hand-deleted first. The committed `ControlGate/` contains neither file, so its provenance (verbatim run output or hand-assembled) is not recorded.

**F5 (medium, decision not ratified). An expectation mismatch is reported as `controls_mismatch`.**
- `tools/repeat-control.py:425-434` — when observed ≠ expected, snapshot mode finishes with `controls_mismatch` (exit 1).
- w1 F-D (`SnapshotReview.md:43-47`) said: "do not map it silently to `controls_match` or `controls_mismatch`", and asked L1 to name the ID. The code does map it, and the docstring documents it (`:56-60`). The mapping is now a choice made in code, not a ratified decision. A snapshot whose pin is wrong and a run whose controls disagree both exit 1 with the same ID.

**F6 (informational). No post-run recheck exists, and the snapshot path never runs the child.**
- `snapshot_mode` (`:412-434`) calls no subprocess. Only `:266`, `:565`, `:599` spawn processes (run mode and selftest).
- Consequence: the w1 requirements "re-verify after the last run" (R1, `SnapshotReview.md:23-24`), and the zero-child-runs-on-tamper case (R3, `:27-28`), are vacuous for snapshot mode because it runs nothing. Run mode (`run_controls`, `:297-331`) does not bind to any snapshot, so probe H (edit during runs, `probe-output.txt` row H) is not covered by any path in the file.
- Design divergence: w1 F-D (`:43-45`) proposed running the pinned argv N=3 times and comparing to `expected`. The implementation instead recomputes from stored bytes. The round spec (`.ufo/waves/round-12/spec.json:3`) says only "validates committed input digests and expected ID/exit". This needs L1 to name which reading governs.

## Dynamic-expectation tautology: not found in the snapshot path

- `expected_id` and `expected_exit` come from the pin file (`:351-353`), not from observations. `expected_exit` is only checked against `EXIT_BY_ID[expected_id]` (`:352`), which is a fixed table.
- `observed` is recomputed from digest-verified bytes by the same `classify` used in run mode (`:408`, `:191-205`). The expectation is never derived by running the child or from the observed value.
- No write/regenerate mode is reachable. `dispatch` (`:762-779`) has no snapshot-writing branch; `write_snapshot` (`:523-542`) is called only from selftest (`:698-714`) with literal expected IDs (`"controls_match"`, `"controls_mismatch"`).
- Residual, documented but unanchored: `expected.json` is not itself digested (limit L1, `w1/SnapshotReview.md:61-63`; docstring `:83-85`). A coordinated rewrite of one observation plus its digest plus the pin passes. Detection requires an external anchor, and none is committed (F1).

## Coverage of inputs: positive checks

- Required set = `run-{1..runs}.{stdout,stderr,exit}` (`:354-357`); `inputs` must equal it exactly (`:358-360`). Every listed input is digest-checked (`:361-363`, `:374-385`) and consumed by `recompute_snapshot` (`:388-407`), so no listed input is verified-but-unused.
- Digests are required to be 64 lowercase hex (`:361-363`). `runs` must be an int ≥ 3, not a bool (`:348-350`).
- Tamper arms exercised in selftest: changed byte (`:718-725`), missing input (`:727-730`), unlisted regular file (`:732-735`). Not exercised: duplicate key, empty inputs, subdirectory, symlink, directory-named-as-input.

## Recommendations (for L1 decision; not applied — read-only seat)

1. Commit a pinned `expected.json` for `ControlGate/` and `ControlGate/mismatch/` (or remove the committed-snapshot claims and the two selftest cases) — F1.
2. Add `object_pairs_hook` that raises on duplicate keys — F2.
3. Treat any non-regular entry, including directories and directory-symlinks, as unlisted (`:364-370`) — F3.
4. Decide whether argv is part of the pin; if so, add it and exempt `command.txt`/`finding.txt` explicitly — F4.
5. Name the ID for expectation-not-reproduced (F5) and decide whether post-run recheck is in scope (F6).

## Verification gaps

- Nothing executed. F1 and F4 are `[INFERENCE]` from code reading; each is cheap to confirm by the main agent with `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate`, `--selftest`, and a duplicate-key pin probe. Those checks are for L1 to run once after integration; they are not run here.
- The committed ControlGate byte content was read, not regenerated; provenance of those files is unknown (F4).

## Tools and installs

- None installed or updated.

## Owned paths

- Written: `.ufo/waves/round-12/w2/ControlSnapshot.md`.
- Not written: `tools/repeat-control.py`, any `.ufo/evidence/…`, `LOG.md`, sibling seat directories, `expected.json` (none created).
