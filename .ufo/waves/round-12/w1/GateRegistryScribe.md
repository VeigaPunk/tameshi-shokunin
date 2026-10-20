# GateRegistryScribe — round 12 w1 report (advisory, lane-internal)

Scope: draft SKILL registry row for `tools/repeat-control.py` from the contract interface
(exit map 0/1/2/64, selftest, pinned fixture path, read/write scopes, owners). Draft only.
Not an independent non-author promotion or admission. No tests, builds, or lints were run.

## Behavior

- Drafted one registry row (Coverage-map shape), a gate-interface card, an exit-precedence
  reading rule, and gaps G-1..G-8.
- Interface source: `.ufo/waves/round-12/spec.json` `context` ("New gate interface"),
  sha256 `e13d92af643cf4fb0a20c82f64cfaf6a1873e0dcda717d2a2c7b276926891cc2`.
- Source status re-read from `corpus/SOURCES.md`: S004 `mined` (:15); S011 `queued` (:22);
  S026 `queued` (:37); S040 `queued` (:49). The draft does not claim any of S011/S026/S040 as support.

## Exit map (contract text; NOT observed — tool absent)

| exit | finding ID(s) | meaning |
|---|---|---|
| 0 | `controls_match` | N pristine runs identical in exit, stdout, stderr |
| 1 | `controls_mismatch` | any output or exit disagreement |
| 2 | `baseline_nonzero`, `command_unavailable`, `snapshot_tampered` | could-not-evaluate (ID is the only discriminator) |
| 64 | invalid usage | could-not-evaluate |

Consistency check (read-only): `tools/mutate-and-run.sh` uses 64 for usage (`:221`), 2 for
setup (`:226`), 1 for FAIL/selftest FAIL (`:513`, `:1615`), 0 for PASS (`:517`, `:1612`).
The contract's 0/1/2/64 mapping does not contradict this convention. Exit 2 is overloaded
here more than in the mutation runner.

## Gate status observed

- `tools/repeat-control.py`: ABSENT (2026-10-20T02:14Z). ControlGate owns it.
- `.ufo/evidence/round-12/ControlGate/expected.json` (pinned fixture): ABSENT.
- `tools/mutate-and-run.sh` sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`
  (matches the pinned tool revision recorded at `SKILL.md:1304`). Not edited.
- HEAD `18ad5d050ef4bcd830fe513825baed878f025024`.

## Findings and risks

1. Exit 2 is overloaded (three IDs). A consumer keyed on exit alone conflates setup, baseline, tamper.
2. `controls_match` is a control-stability observation only. The row must not be read as a
   determinism proof or as a kill-rate input (contract forbids both).
3. `--out DIR` existing-directory behavior is unspecified: stale run files could satisfy a later
   comparison (G-1, ControlGate; GateSecurity to review).
4. `--snapshot DIR` layout (manifest path, expected ID/exit record) is unspecified (G-2, SnapshotReview to propose).
5. Run-count boundary for N < 3, zero, non-integer is unspecified (G-3). Proposal: exit 64 — [INFERENCE].
6. `--selftest` pass/fail exit and summary line are unspecified (G-4). Proposal mirrors
   mutate-and-run: 0 pass / 1 fail — [INFERENCE].
7. No per-run timeout or signal-exit representation in the contract (G-5).
8. Source gap: only S004 is `mined`. S011/S026/S040 are `queued`; the knowledge entry cannot cite them as support until opened and promoted in the round that writes it (QUALITY.md 10).

## Out of scope (not done)

- No edits to `SKILL.md`, `LOG.md`, `corpus/*`, `tools/*`, or any sibling seat directory.
- No registry promotion, no admission, no LOG round entry (L1 owns the LOG entry).
- No executed verification of the gate; the contract forbids mid-flight runs.

## Artifact paths (exact)

- `.ufo/evidence/round-12/GateRegistryScribe/registry-row-draft.md` — draft row, interface card, gaps G-1..G-8, owned-path list
- `.ufo/evidence/round-12/GateRegistryScribe/observed-probes.txt` — read-only probes (HEAD, sha256s, absence checks, exit anchors)
- `.ufo/waves/round-12/w1/GateRegistryScribe.md` — this report

## Tooling

- Installed or updated: none. No tool was needed; read-only shell probes only (`git`, `grep`, `sed`, `sha256sum`, `python3` JSON read).

## Next steps for L1 (main agent)

- Decide G-1..G-4 and G-3 with ControlGate and SnapshotReview before the row is applied.
- Apply the row to `SKILL.md` or the corpus coverage map only with a LOG.md round entry.
- Run the gate's `--selftest` and `--snapshot` once after ControlGate lands; check the observed exit/IDs against §Exit map above.
