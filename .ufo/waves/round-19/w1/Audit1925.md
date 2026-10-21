# Audit 1925 — retained receipt review (2026-10-21)

## Scope and sources
Read only the assigned retained receipt pair, its linked trace, and the matching round-18 ledger entry:
- `.ufo/evidence/round-18/final/audit-1925.stdout` (especially lines 1–31)
- `.ufo/evidence/round-18/final/audit-1925.stderr`
- `.ufo/evidence/round-18/coldread/traces/L1/audit-1925.json` (argv, revision and input fields)
- `.ufo/evidence/round-18/coldread/ledger.json`, entry `start=1925, end=1934`, linked trace `audit-1925.json`

No target command was re-executed.

## Observations
- `sha256sum .ufo/evidence/round-18/final/audit-1925.stdout` observed `c1ee0c85c7b33720b307334a61e36f2925b77b64f12563109459fdcc060eda2b`; `wc -c` observed 5,348 bytes. `wc -c` on the stderr receipt observed 0 bytes.
- This is an observed digest of the retained stdout, not a comparison against an expected stdout digest: the assigned trace has no stdout-artifact digest, and the matching ledger entry's `sha256` is `884b3df3741b6172a65c5ebd74b082e9044e62fbb6aec3aa4187e52318616d62`, with no indication it is the stdout digest. The stdout digest therefore is not independently cross-bound by this receipt pair/entry.
- The trace records `exit: 0`, `rev: a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`, and matching `cwd`/`root` at `/tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin`. Its argv binds a `bwrap` invocation to that temporary root and then `env -i ... python3 -c <program> <spec>`; the recorded spec selects `SKILL.md` lines 1925–1934 and 19 named paths. The recorded Python program emits the selected section, hashes/prints those paths, checks the listed receipt markers, and exits through those assertions. I inspected the recorded argv only; I did not run it.
- The trace's 20 tracked input digests include `SKILL.md` (`1334c5128c7e53a6834c388e71a1b90a1778e72cbbed0ceccf8c1ba0423ac1e0`) plus the 19 `OPEN` paths; their printed hashes in stdout lines 12–30 agree with the trace input map. The trace reports `tracked_filter: true`, empty `untracked`, `external`, and `live_lane_reads` maps, and `dropped_home_count: 0`. These are the trace's recorded facts, not a claim that every possible environmental influence was inventoried.
- The ledger entry links this exact trace and has `read_rev` equal to the trace `rev`; it records the section range 1925–1934, `verdict: gap-minor`, one minor gap, and `inputs_dropped: ["SKILL.md"]`. The trace preserves a digest for `SKILL.md` despite that ledger omission. The entry says one command was executed; I infer no broader command coverage from that count.

## Findings (low severity)
1. **Output-hash cross-binding is absent.** The stdout can be hashed locally (digest above), but neither assigned record supplies an expected hash for the stdout artifact. Do not represent the computed digest as a verified match to a stored manifest.
2. **Ancestor-instrument equivalence is not established by this run.** Stdout line 31 says “ancestor runs have the same instrument blobs as the read revision.” In the recorded Python source (trace line 33), that sentence is printed unconditionally after assertions on the specifically listed receipts; there is no comparison of ancestor runs or their instrument blobs in the recorded program/input list. The observed successful run supports the listed checks and captured input hashes, not that ancestry claim.

## C1 impact, residual risk, and verification gap
Later C1 repairs do not by themselves mutate or invalidate these retained historical bytes. They may supply new evidence about corrected behavior, but cannot retroactively create the missing stdout-digest cross-binding or substantiate the ancestor-equivalence sentence. Retain this receipt as evidence of the recorded revision and listed checks, with those limits; do not use it as proof of corrected-lane behavior or ancestor instrument identity. Verification was limited to the assigned pair, linked trace, and ledger entry; no re-execution or broader ancestry audit was performed.