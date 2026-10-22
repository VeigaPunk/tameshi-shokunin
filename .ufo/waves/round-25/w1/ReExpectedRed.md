# ReExpectedRed — re-attack of round-23 wave-2 ExpectedRed (reviewer, calibration)

Seat history: `TameshiR23.ExpectedRed` was spawned but died with the round-23 author before any
execution or report (`.ufo/waves/round-23/original-outcomes2.json:1239-1247`, status failed,
transcript retained, no callback). This is the first run of this falsifier. Original item text is
quoted verbatim in the round-25 dispatch; the attacked binding parses into two conjuncts:

1. **All baseline expected-red child exits remain valid** — every registry row tagged `baseline`
   whose required child exit is nonzero must, when actually executed, exit nonzero with
   `got == expect` and `held = true`.
2. **Gate exit0 means contract match** — `tools/command-binding.py` exits 0 only when the
   digest-pinned bundle genuinely satisfies the declared binding (no false green), and exits
   nonzero on every contract violation shape.

## Verdict

The binding holds on the frozen round-23 artifacts and still applies at lane revision
`c9ff09fb41fb8aac5fc335faf10858ff606bd5df`. No counterexample found. Supersession check: the
round-23 command-binding rows were superseded (by pinned round-24 successors), but none of the
four `baseline` expected-red rows is superseded, and all still hold when re-executed at c9ff09f.

## What I checked, with evidence

### 1. Round-23 frozen artifacts (static reads, no execution in the live lane)

- **Frozen full-fleet receipt** `.ufo/evidence/round-23/registry-C.json`: `registry-check.py
  --rev 336565fc… --json` recorded `exit 0`, `held 46`, 50 rows, 46 active. Every baseline
  expected-red row held with `got == expect`:
  `repeat-control-snapshot-mismatch expect=1 got=1 held`, `evidence-disposition-round18-before
  expect=1 got=1 held`, `context-capture-missing-env expect=1 got=1 held`,
  `context-capture-mapping-suffix expect=1 got=1 held` (rows parsed from the recorded stdout).
  The only not-held red row, `evidence-disposition-round17-before` (expect=1 got=2 held=False),
  is `status superseded`, tags `["new-r17"]` — not a baseline row and excluded from the gate
  verdict by status; its successor `evidence-disposition-round18-before` held. Honest recording,
  not a false red. Not a counterexample.
- **Gate receipts, both directions, on frozen bytes**: `correct-command-gate-A.json` exit 0,
  `finding_ids []`, `bundle_sha256 90dc14bf…`; recomputed sha256 of
  `.ufo/evidence/round-23/correct-command-bundle.json` = `90dc14bf5ca6e2d6…aed277` — match.
  `source-read-gate-A.json` exit 1, `["ARGV_MISMATCH"]`, `bundle_sha256 db620668…`; recomputed
  sha256 of `source-read-bundle.json` = `db620668efe12c00…3cf` — match. So at round 23: exit 0
  occurred exactly on the matching pinned bundle, exit 1 on the violating one.
- **Round-23 gate selftest** `.ufo/evidence/round-23/selftest-A.json`: `COMMAND_BINDING_SELFTEST:
  38/38 pass`, exit 0 — includes `CASE clean-with-expected-red PASS` (expected nonzero child exit
  accepted) and 16+19 negative shapes all mapped to nonzero exits.
- **Receipt/gate identity**: the frozen receipts ran the gate with content digest `d533dc1e…`,
  identical at 496d212 and 336565fc (my `git show <rev>:tools/command-binding.py | sha256sum`),
  consistent with `.ufo/waves/round-23/fresh-adjudication.json` "accepted_now_as_corrections".

### 2. Supersession and drift at c9ff09f

- Working tree `tools/command-binding.py` and `tools/registry.json` are byte-identical to
  c9ff09f (sha256 compared against `git show c9ff09f:<path>`; both EQUAL), so reading the live
  files reads the frozen revision.
- **Gate changed since round 23, semantics did not**: `git diff 496d212 c9ff09f --
  tools/command-binding.py` = 5 insertions / 4 deletions, entirely inside `selftest()` — the
  fixture load becomes a loop over `round-23/extra-cases.json` plus `round-24/extra-cases.json`
  (6 more cases → 44/44). `evaluate()`/`check()` are untouched (strict key-set checks were
  already in the round-23 committed gate d533dc1e; only the pre-review snapshot
  `.ufo/evidence/round-23/pre-review-command-binding.py` lacked them).
- **Row supersession** (`tools/registry.json`, 54 rows, 47 active / 7 superseded):
  `command-binding-selftest` (38/38), `command-binding-frozen-clean`,
  `command-binding-source-read-red` are `superseded` by `-r24` / `-pinned` successors that pin
  `bundle_sha256` literals (closing the routed RevisionDeclared F1/CorpusClaim F3 defect). The
  four `baseline` expected-red rows: **all still `active`** at c9ff09f.

### 3. Live falsifier at c9ff09f (executed only inside my /tmp clone)

Clone: `git clone <lane> /tmp/r25-expred && git checkout --detach c9ff09f` (clone HEAD verified
`c9ff09fb41fb8aac5fc335faf10858ff606bd5df`). Ran `python3 tools/registry-check.py --only <row>
--json` per row; observed:

| row | expect | got | held | rc |
|---|---|---|---|---|
| repeat-control-snapshot-mismatch (baseline red) | 1 | 1 | true | 0 |
| context-capture-missing-env (baseline red) | 1 | 1 | true | 0 |
| context-capture-mapping-suffix (baseline red) | 1 | 1 | true | 0 |
| evidence-disposition-round18-before (baseline red) | 1 | 1 | true | 0 |
| wave-accounting-wrong-count-entry (r22 red) | 1 | 1 | true | 0 |
| command-binding-source-read-red-pinned (r24 red) | 1 | 1 | true | 0 |
| command-binding-frozen-clean-pinned (exit0 side) | 0 | 0 | true | 0 |

`python3 tools/command-binding.py --selftest` → rc 0, `COMMAND_BINDING_SELFTEST: 44/44 pass`:
18 violation shapes (argv/cwd/revision/exit/stdout/membership/duplicate + malformed shapes →
exit 1 or 2) never yield exit 0; `clean-with-expected-red` and the tampered/duplicate-json-key
controls behave (tamper → 2 `SNAPSHOT_TAMPERED`, never 0).

### 4. False-green hunt on the c9ff09f gate (read-level)

`evaluate()` (tools/command-binding.py:66-114) checks: exact schema and key sets, canonical cwd,
40-hex revision, `type(exit) is int` (bools rejected), nonempty argv strings, duplicate
requirements/receipts rejected, receipt set == requirement set, exact argv/cwd/revision equality,
exit equality, and `stdout_contains` tokens via substring over `stdout` only (stderr can never
supply a token). `check()` (:116-131) pins all bundle bytes by sha256 against the caller-owned
expected file; any digest, shape, or read failure returns 2, never 0. Only theoretical laxity
found: an empty `stdout_contains` token (`""`) trivially matches — but that is a degenerate
caller-owned commitment pinned byte-exactly by the expected digest, not a gate bypass, and it is
within the gate's declared scope ("validates retained declarations, not their producer
authenticity" — docstring line 8). No input shape found where a contract-violating bundle exits 0.

## Residual risk and verification gaps

- No `lsp` device is available in this seat's tool inventory; caller/definition checks used
  direct reads and git, not a language server.
- I re-ran the seven claim-relevant rows, not the full 46-row active registry (the fleet-live row
  `pin-disposition-read` touches sibling repos and is outside this item's scope).
- Guard-weakening mutants of the gate are round-25 C1 R2 material (`guard-mutants.spec`); I did
  not re-derive that sweep, so "no mutant yields a false green" is established here only by the
  44-case selftest plus read-level analysis, not by an independent mutant sweep.
- The superseded `evidence-disposition-round17-before` row's current exit 2 was not
  re-diagnosed; it is outside the baseline scope and honestly recorded as not held.

R23-REATTACK ExpectedRed: AGREE
