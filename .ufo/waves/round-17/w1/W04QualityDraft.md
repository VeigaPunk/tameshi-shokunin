# W04 — QUALITY.md criteria 23–26 (draft)

Seat: `TameshiR17.W04QualityDraft` (scribe, wave 1, round 17). Lane tip read: `98bea7da5801f4bc58e4187690ee1687c8a5061f`.
Scope: draft text only. `corpus/QUALITY.md` is not edited; the L1 installs the text.

## Evidence used

| Fact | Command | Observed |
|---|---|---|
| Last criterion at tip is 22 | `git show 98bea7da:corpus/QUALITY.md \| grep -n '^[0-9]\+\.'` | criteria 1–22; 22 at line 116, file 123 lines |
| Heading style for appended rounds | same file | `## Criteria appended — round N`, then numbered paragraphs with `(\`lessons/…\`, mistake)` pointers |
| Source lesson exists | `git show 98bea7da:corpus/lessons/round-16-verifier-spotcheck.md` | exists; §2 (C2 fails, sha-only credit), §3 (operability harmed), §6 R16-OP1, R16-C2a/b/c, R16-EV1, R16-MON1 |
| Round-16 mistake file exists | `git show 98bea7da:corpus/lessons/round-16.md` | exists |
| EV1 receipt is stale at tip | `git show 98bea7da:.ufo/evidence/round-16/round-gate/runner-sha256.txt` | `89722ddb…  tools/mutate-and-run.sh` (the c699c8c runner); spotcheck §6 says the landed runner is `0673d2e5…` |
| Disposition gate has the digest-mismatch path | `git show 98bea7da:tools/evidence-disposition.py \| grep -n expected_input_digest_mismatch` | lines 1190, 1755 |
| Registry and ledger v2 do not exist at tip | `git show 98bea7da:tools/registry.json`, `…:.ufo/evidence/round-17/coldread/ledger.json` | both `fatal: path … does not exist`. The criteria below name them as wave-1 deliverables in flight; they are not cited as present. |

No command was executed against the gate or the selftests; this is a text draft.

## Draft text

Append after criterion 22 in `corpus/QUALITY.md`:

```
## Criteria appended — round 17

23. A cold-read's credit is keyed to the inputs its executed commands ran
    against. An entry that executed commands credits its bucket only when
    every lane input in its `inputs` record still has the recorded sha256 at
    the measured revision. A drifted or unrecorded input uncredits the bucket
    and names the path. A section sha256 alone is not credit for an
    instruction that runs other lane files. The measuring command must
    uncredit an otherwise credited bucket when one input drifts (red before)
    and credit it again once a fresh read records the new digest (green
    after). (`lessons/round-16-verifier-spotcheck.md`, §2 and §6 R16-C2b; the
    round-14 recipe bucket SKILL.md:1563-1596 kept its round-16 credit at sha
    `97cf436b` while `tools/mutate-and-run.sh` moved under its commands.)
24. Editing an instrument pinned by a registered gate runs that gate's
    registered entry command (its `tools/registry.json` row, argv run from the
    lane root) before the edit lands, and the executed exit is recorded beside
    the edit. An outcome change must be declared by design before landing. A
    by-design change is re-pinned or superseded by a named disposition in the
    same round. An undeclared change blocks landing. A passing selftest does
    not satisfy this rule. Criterion 20 still forbids in-place edits during a
    wave. (`lessons/round-16-verifier-spotcheck.md`, §3 Operability and §6
    R16-OP1: the round-14 disposition gate went from 0 at HEAD to exit 2
    `expected_input_digest_mismatch` after `tools/mutate-and-run.sh` was edited,
    and no re-pin or superseding disposition was recorded.)
25. The no-harm monitor for tool changes runs the registered entry commands,
    not only selftests. Each row of the entry registry is executed from the
    lane root at the measured revision and compared with its `expect` exit
    (and `stdout_contains`, where declared). A selftest proves the instrument's
    own controls; it does not witness a live-tree verdict. A round whose
    monitor ran selftests only cannot record its no-harm verdict as held. The
    registered-command check must be shown able to fail before it counts: an
    old revision graded against the new registry reports `differs` for the
    changed row. (`lessons/round-16-verifier-spotcheck.md`, §3 and §6 R16-MON1:
    ToolsNoHarm ran selftests only and did not see the round-14 gate's exit
    change.)
26. A corrected receipt gets a dated, appended correction in the round its
    error is found. The correction names the receipt path, the wrong value,
    the correct value with its sha256 and the commit that establishes it. The
    faulty receipt is not rewritten. A receipt error that is found and left
    for a later round is named as debt, with an owner, in the same round's
    report. (`lessons/round-16-verifier-spotcheck.md`, §2 and §6 R16-EV1 and
    R16-C2c: `.ufo/evidence/round-16/round-gate/runner-sha256.txt` reads
    `89722ddb…` while the landed runner is `0673d2e5…`, and the correction was
    routed to the next round; criteria 4, 14 and 18 already require appended
    corrections.)
```

## Checks on the draft

- Each rule has a discriminator, as criteria 11–22 do: 23 names red-before/green-after on drift; 24 names the exit record and the by-design/undeclared split; 25 names the `differs` result on an old rev; 26 names the dated append and the debt line.
- Numbering starts at 23. Criterion 24 does not supersede 20; 25 does not supersede 17 or 19; 26 does not supersede 4, 14 or 18.
- Every pointer resolves at tip (see table). Quoted hashes are the ones in the cited files.
- Criterion 23 and 25 depend on artifacts that wave 1 is building (ledger v2, `tools/registry.json`). The text does not cite them as present.

## Coordination note

Other wave-1 seats may draft criteria in the same range. The L1 must reconcile numbering before install. This draft assumes 23 is the first free slot.

## Out of scope

- No edit to `corpus/QUALITY.md`, to the lesson files, or to any lane tool.
- No gate or selftest was run (not assigned).
- No messages sent (no blocker).

## Verdict

built (draft text for criteria 23–26; not installed).
