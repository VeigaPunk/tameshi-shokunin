source: S085 — .ufo/waves/round-23/fresh-adjudication.json@6a1821a8897eea6e7d9669292160ec9593669409:53-104 (routed defects); S084 — https://docs.python.org/3/library/os.path.html#os.path.realpath ("Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path"); .ufo/evidence/round-24/contract.json
verified-at: 2026-10-21 — frozen eleven-predicate ruler before 1/11 at 6a1821a; later executed results are recorded in the round24 lesson and SCORECARD only after execution
recheck: python3 .ufo/evidence/round-24/measure.py --repo CLONE_AT_REV; python3 tools/registry-replay.py --selftest; python3 tools/command-binding.py --selftest

# Hardening a command-binding demonstration

A self-consistent replay can stay green while its weakest links drift. In
round23, falsifiers named the links. This entry turns each into a predicate
that can fail.

| Weak link | Hardened rule | Fails when |
|---|---|---|
| argv compared name-insensitively, case-folded, stripped or de-duplicated | supplemental fixtures swap argv between two names, change only case, pad a token, repeat a flag | a weakened comparison lets the public selftest pass |
| negative (signal-style) exits ignored | a fixture expects 0 and receives -9; a declared -15 that matches stays clean | `>= 0` short-circuits the exit check |
| stdout tokens checked with any() instead of all() | existing `all-of-tokens` fixture (round23) | only one of two required tokens is present |
| frozen-bundle registry row checks only `finding_ids` | the row also requires the exact `"bundle_sha256": "…"` literal from the sorted-key report | a different valid bundle plus regenerated expected file replaces the frozen one |
| replay publishes a bundle although the runner rejected a row | `tools/registry-replay.py --project` refuses: RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED | `held` is not `true` or `cleanup_error` is set |
| unbounded retained streams | `--max-stream-bytes` (default 1 MiB) refuses with STREAM_LIMIT | a stdout/stderr exceeds the bound |
| live-dependent rows reported as revision-pinned | `external` source rows and runner `non_hermetic_argv` rows are listed in `live_dependent` | the list omits such a row |
| sibling identity by string | `--plan` realpath-normalises lane, fleet root and siblings | a symlinked or `..` path alias changes identity |
| runner digest from the live tree | the runner is hashed from the clone copy that executes | — (recorded per run, not a ruler predicate) |

Superseding a registry row is append-only. The old row gets
`status: superseded` and `superseded_by`, and a new active row carries the
stronger expectation. The runner still executes superseded rows; they do
not count toward `held`.

## Bounds

- Receipt argv, cwd and revision remain the invocation parameters the
  instrument passes to the runner. They are not observed process metadata.
- A bundle digest pin means a later commit that changes both the row and the
  bundle selects a new contract. Neither the pin nor the gate authenticates
  the producer.
- Row commands run in a clone whose fleet mirror symlinks the live sibling
  repos. Realpath identity is not write isolation. Non-strict `realpath` may
  still leave missing components unresolved (S084).
- Four specific mutants killed is not general mutation adequacy.
- The eleven predicates are synthetic capability checks. They are not
  historical defects or an expertise score.
