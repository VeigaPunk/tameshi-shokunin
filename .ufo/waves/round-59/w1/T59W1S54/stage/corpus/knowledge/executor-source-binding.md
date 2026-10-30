source: S289 (proposed only; L1 must resolve registry-id collisions before admission) — Git, git-cat-file documentation — https://git-scm.com/docs/git-cat-file — §DESCRIPTION, first sentence; §OPTIONS, -t, --textconv and --filters; opened 2026-10-30, page reports last updated in 2.56.0. Own-work contract: .ufo/evidence/round-59/contract.json and independent counter .ufo/evidence/round-59/measure.py at frozen commit e9cc34bec3f0c670550552bcc962563e7ae3ca58.
verified-at: 2026-10-30 — official documentation opened and frozen contract/counter read; this draft records specified behavior, not an executed gate result or a deciding measurement.
recheck: on-release — reopen Git §DESCRIPTION and §OPTIONS; compare this decision table with the frozen round contract before changing the CLI or failure mapping. L1 owns the independent counter run and final source-id collision check.

# Executor source binding: compare declared committed blobs, not claimed execution

## Source anchor and scope

Located quotation (S289 proposed, official Git documentation, §DESCRIPTION,
first sentence; accessed 2026-10-30):

> Output the contents or other properties such as size, type or delta information of one or more objects.

Git documents object inspection, not execution attestation. Its `-t` option
reports object type; `--textconv` and `--filters` explicitly transform content.
Those distinctions explain why an object-binding gate must compare committed
source objects rather than a rendered or filtered working-tree file. They do
not independently establish the implementation's correctness.

Round 59's bounded capability compares each verifier-declared executor source
path in a candidate Git commit against the same path in a verifier-supplied
trusted commit. A successful comparison is a binding prerequisite only.
An unrelated commit change may pass because this is not whole-tree equality.

## Operator invocation

Use the exact contract interface:

```text
python3 TOOL --repo REPO --trusted COMMIT --candidate COMMIT --path PATH [--path PATH ...]
```

`TOOL` is the verifier-selected copy of `tools/executor-source-pin.py`.
`REPO` is the repository containing both commits. The verifier supplies the
trusted revision and the declared path closure; candidate-authored suggestions
are not an authority for either. Resolve and record immutable commit ids before
invoking the gate. Record the tool identity, full argv, exit status, stdout and
stderr with any receipt so the comparison can be reproduced.

For an invocation with several declared sources, repeat `--path`; shell-quote
each path as a single argument, for example `--path 'tools/space name.py'`.
The frozen spellings also include `tools/runner.py`, `tools/日本語.py` and
`tools/-runner.py`. Do not silently drop paths that are awkward to quote.
“Executable-source” describes the source's role, not a requirement established
here that its executable permission bit be set.

## Operational decision table

These are contract expectations, not observations from this draft's author.
The table assumes a valid trusted commit and regular trusted source except
where the row explicitly says otherwise.

| Condition | Exit | Signature | Operator decision |
|---|---:|---|---|
| All declared regular candidate source blobs equal trusted blobs | 0 | `EXECUTOR_SOURCE_BOUND` | Record declared-source binding only; retain separate execution and closure checks. |
| Candidate differs only outside declared source paths | 0 | `EXECUTOR_SOURCE_BOUND` | Accept only this binding prerequisite, not the unrelated changes. |
| A declared candidate source blob has changed | 1 | `EXECUTOR_SOURCE_DRIFT` | Stop admission on this prerequisite; inspect the named source change against the trusted baseline. |
| A declared candidate source is missing or nonregular, including a symlink | 1 | `EXECUTOR_SOURCE_DRIFT` | Stop; restoring bytes elsewhere or following the link does not bind this declared regular source. |
| Candidate commit cannot be resolved | 2 | `EXECUTOR_SOURCE_UNAVAILABLE` | No comparison verdict; repair the revision/object availability and rerun under verifier control. |
| Arguments, trusted commit or trusted source are invalid | 2 | `EXECUTOR_SOURCE_UNAVAILABLE` | No usable trusted comparison; correct verifier inputs, never substitute candidate-selected trust. |

Treat exit 1 and exit 2 as distinct failures, neither as acceptance. Retain both
output streams: the frozen counter accepts the required signature in stdout
or stderr, paired with the expected exit status. Missing/conflicting signatures,
or an unexpected exit, do not establish the specified result; preserve the raw
receipt rather than inventing an extra diagnostic contract.

## Independent measurement and failure signatures

The frozen counter enumerates six classes (`equal`, `changed`, `missing`,
`unrelated`, `unresolvable`, `symlink`) across the four spellings above. Its
24-case target is specified in the frozen contract; the measurement command is:

```text
python3 /ABS/LANE/.ufo/evidence/round-59/measure.py --lane /ABS/LANE --rev CANDIDATE_COMMIT --work /ABS/EMPTY_SCRATCH
```

This command is supplied for L1, not executed as part of this knowledge draft.
The work directory must be empty; the counter cleans its generated fixtures.
Without `--tool`, it extracts the implementation from the measured commit.
`--tool` is a control override, explicitly not a certification path.

The counter expects exits 0 for `equal`/`unrelated`, 1 for
`changed`/`missing`/`symlink`, and 2 for `unresolvable`, each with its matching
signature. It reports `C1_R59 rev=... passed=N/24 C1_R59_PASS=true|false`.
If the measured commit lacks the tool, its explicit failure signature is
`passed=0/24 C1_R59_PASS=false reason=tool-absent`.
The claim also requires skipped-work and always-accept controls to fail;
a positive counter line alone does not supply those control receipts. This
entry claims neither the positive result nor execution of either control.

## Trust boundary and known limits

- The verifier, not this gate, establishes the trusted revision's authority and
  the completeness of the declared source closure. Omitted sources can drift
  without this comparison noticing; a pass cannot certify closure completeness.
- Matching committed blobs does not prove that those blobs were executed, that
  work occurred, or that an output was produced by them. Binding and execution
  attestation are separate claims.
- Dependencies, interpreter identity, runtime environment and working-tree
  modifications are outside this declared-object comparison. Any relationship
  between committed objects and runtime inputs needs separate evidence.
- Source identity is not source quality or safety. Identically bad trusted and
  candidate source can satisfy this prerequisite.
- The frozen fixture matrix is finite evidence for the declared capability,
  not proof over all Git object layouts, path spellings or host configurations.
- This is not round-58 C2 certification and does not create author-independent
  trust. No source registry row, coverage admission or deciding score is implied
  by this staged document; proposed S289 remains subject to L1's collision check.
