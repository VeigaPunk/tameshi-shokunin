# Trace selftest receipt audit

Audit date: 2026-10-21. Scope: only `trace-selftest` in `.ufo/evidence/round-18/final/checks.json`, its retained `.stdout`/`.stderr`, and the named CLI source. The command was not executed.

## Findings

- **Digest: 1/1 recorded digest matches.** The row's `stdout_sha256` is `fadbe2c9cb385eb4da8304cc8d1d7b6368bfdde82ee8a920696d23294feffda1`; `sha256sum` of `.ufo/evidence/round-18/final/trace-selftest.stdout` returned that exact digest. The retained stdout is 783 bytes and ends `SELFTEST: 30/30` (line 31). Retained stderr is 0 bytes (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). The row records no stderr digest, so stderr is corroborating retained evidence, not a second digest match.
- **Argv spelling: agrees with the CLI source.** The row records `python3 tools/trace-inputs.py --selftest`. `tools/trace-inputs.py:978-983` defines `--selftest` and dispatches it to `selftest()`; its docstring at lines 53-54 says the option runs synthetic fixtures and is location-independent. Thus the relative script path and option spelling are valid for the recorded working-directory context, though the row does not record `cwd`.
- **Revision attribution: recorded and source-correlated, but not execution-bound.** The row names revision `921ef8077440f90d092aab4b9fdc750a45de1224`. Read-only `jj log -r 921ef8077440f90d092aab4b9fdc750a45de1224 --no-graph` resolves it to the 2026-10-20 round-18 commit. The SHA-256 of `tools/trace-inputs.py` retrieved from that revision equals the inspected working-tree file SHA-256 (`fb1d81f67551fb04e9e447cbc706ef5cc9cfd5208169004184b24ab15f3f2636`). This corroborates the argv/source spelling against the attributed revision. The receipt has no source digest or `cwd`, so it does not independently bind the process execution to that revision.
- **Outcome: successful retained evidence, not a failed raw attempt.** The row says `exit: 0`; the exact retained stdout reports 30/30, with empty stderr. Nothing in this scoped row or its paired streams establishes a failed attempt. Any separately preserved raw failure must remain labeled as that distinct attempt, not substituted for or silently collapsed into this successful receipt.

## Preserved-history treatment

Keep the original row and both retained stream files unchanged. Append this dated audit as a separate adjudication; do not rewrite the receipt to remove a historical failed attempt or call this successful row a failure. If another preserved record documents a raw failure, retain it unchanged as a separate failed attempt and keep its relation to this successful current evidence explicit. The scoped materials do not identify such a failure, so its existence remains unverified here.

## Evidence locations / command

- `.ufo/evidence/round-18/final/checks.json:55-64` — argv, revision, exit, and stdout digest.
- `.ufo/evidence/round-18/final/trace-selftest.stdout:1-31` and `trace-selftest.stderr` — retained output bytes.
- `tools/trace-inputs.py:53-54,978-983` — selftest contract and dispatch.
- Read-only commands: `sha256sum`/`wc -c` on the two retained streams; `jj log -r 921ef8077440f90d092aab4b9fdc750a45de1224 --no-graph`; and `jj file show -r 921ef8077440f90d092aab4b9fdc750a45de1224 tools/trace-inputs.py | sha256sum` compared with `sha256sum tools/trace-inputs.py`. The CLI itself was not run.

Quoted source excerpts (2026-10-21 audit): “SELFTEST: 30/30” (`trace-selftest.stdout:31`); “--selftest runs synthetic fixtures only, location-independent” (`tools/trace-inputs.py:53-54`).