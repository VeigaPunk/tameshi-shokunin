source: S083 — tools/registry.json at 28cae179e4dc2c1fa7f032a79cdddf0b5d862d76; tools/registry-check.py:15-38; .ufo/evidence/round-23/contract.json
verified-at: 2026-10-21 — registry declaration opened; executed capability observations are appended below only after execution
recheck: python3 tools/command-binding.py --selftest; python3 .ufo/evidence/round-23/measure.py --repo REPO_AT_REV

# Required commands are not source reads

A positive `commands_executed_count` establishes neither which command was
required nor whether its retained receipt matches that command. The existing
input-keyed source monitor deliberately measures source-read support, not
required-command coverage. Its historic/current source counts remain that
same unit; this entry does not relabel them.

`tools/command-binding.py` checks a finite declared requirement set against
retained receipts. A trusted expected file pins the entire bundle by SHA-256.
The bundle declares `revision`, a canonical absolute `cwd`, nonempty
`requirements` and `receipts`. Requirements carry a unique name, exact argv,
and expected integer exit plus optional literal stdout tokens. Receipts carry
the same name, exact argv, cwd, full revision, integer exit and stdout/stderr.
All fields come from one retained observation, never merged from different runs.

| Decision | Gate result |
|---|---|
| Exact names, argv, cwd, revision and expected outcomes match | 0, clean |
| Missing/unknown or duplicate command; argv/cwd/revision mismatch; wrong exit or missing stdout token | 1, failed, stable finding ID |
| Malformed shape, boolean/string exit, invalid JSON or duplicate JSON key | 2, could-not-evaluate |
| Bundle bytes disagree with trusted expected digest | 2, SNAPSHOT_TAMPERED |
| Usage or mixed selftest options | 64, could-not-evaluate |

An expected child exit1 is valid when its own requirement says1. The gate's
exit0 means all declarations match, not that every child exit was0. Stdout
tokens must occur in stdout, not stderr; arbitrary `held=true`, report text or
source paths do not supply outcomes. Exact argv comparison deliberately
rejects normalization, reordered flags and superficially equivalent aliases.
A relocated replay requires its own exact cwd contract, not silent rewriting.

## Finite workflow

1. Freeze the required registry rows before executing them; retain their
   source revision and registry bytes. Do not derive expected argv or tokens
   from the receipts being graded.
2. Execute the declared commands in an isolated revision checkout and retain
   actual argv, cwd, revision, exit and streams for each named observation.
3. Commit the bundle and an expected file containing
   `schema: command-binding-expected-v1` and its `bundle_sha256`.
4. Run `python3 tools/command-binding.py --bundle BUNDLE --expected EXPECTED --json`.
5. Keep an otherwise identical source-read substitution with the wrong argv;
   the same command must return1/ARGV_MISMATCH while the original is clean.

## Bounds

The trusted expected file is an authority boundary, not a signature. Changing
both requirements and expected digest chooses a new contract; it is not an
undetected corruption of the old pinned contract. Self-consistent forged
receipts can pass: no producer/provider authentication or actual execution
attestation is claimed. A revision string is declared metadata, not evidence
of continuous checkout identity. The actual replay observation is separately
retained; validating its declarations is a different operation.

The ten frozen rejection predicates are synthetic capability tests, separate
from the baseline registry population. Neither denominator is full-page recipe
completeness, independent/blind cold-read, promotion credit or expertise-score
inflation. Existing registry outcome semantics and supersession stay unchanged.

## Executed finite demonstration (2026-10-21)

At496d212bc46789cdf8cafab72978bdb7f4182963, the baseline registry
population is43 active rows: `python3 .ufo/evidence/round-23/replay.py
--repo REPO --rev 496d212bc46789cdf8cafab72978bdb7f4182963 --out OUT`
actually holds43/43 and retains complete decoded stdout/stderr. The same
bundle's gate verdict is0/[] (`replay-gate-A.json`). The ten-case counter is
10/10, public selftest38/38 and bounded guard sweep kills10/10 with green
pristine/restored controls (`c1-after-A.json`, `selftest-A.json`,
`mutations-A.json`, all under `.ufo/evidence/round-23/`).

An actual source read of the registry returns an expected token and exit0,
yet exact argv binding rejects1/ARGV_MISMATCH. A newly executed correct
command is clean0; respective receipts are `source-read-gate-A.json` and
`correct-command-gate-A.json`. This supplies the failure-backed discriminator
for QUALITY46; it does not make unsigned process declarations authentic.

## Erratum — round23 fresh falsification (2026-10-21)

Workflow step 2 asks for an isolated checkout and actual argv/cwd/revision.
The round23 replay met that step only partly:
- The instrument supplied receipt argv, cwd and revision from the values it
  executed. On that population the gate therefore checked only exit and
  stdout.
- Two rows, `pin-disposition-read` and `verify-round15`, read live fleet
  state, and live sibling repos were symlinked into the clone. The replay is
  41 revision-pinned rows plus 2 live-dependent rows, not a hermetic clone.

The gate sees only the requirements declared inside the bundle. Freezing the
requirement set is a separate obligation, carried out by `replay.py`
comparing evidence-local `requirements.json` with `registry-baseline.json`
before running. See QUALITY47 and `lessons/round-23.md`, "Fresh falsification
wave"; earlier text above stays unchanged.
