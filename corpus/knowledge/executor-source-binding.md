source: S289 — Git, git-cat-file documentation (2.56.0) — https://git-scm.com/docs/git-cat-file — §DESCRIPTION, first sentence; §OPTIONS, -t, --textconv and --filters; opened 2026-10-30. Own-work contract: .ufo/evidence/round-59/contract.json and counter .ufo/evidence/round-59/measure.py at frozen commit e9cc34bec3f0c670550552bcc962563e7ae3ca58.
verified-at: 2026-10-30 — official documentation opened this round; the gate at tools/executor-source-pin.py was measured by the frozen counter at 93acc996cbb7bfed27112e797c9d2392ff4aa6b3 (24/24, C1_R59_PASS=true); control receipts in .ufo/evidence/round-59/controls/.
recheck: on-release — reopen Git §DESCRIPTION and §OPTIONS; compare this decision table with the frozen round contract before changing the CLI or failure mapping.

# Executor source binding: compare declared committed blobs, not claimed execution

## Source anchor and scope

Located quotation (S289, official Git documentation, §DESCRIPTION,
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

The measurement was run by the lane L1 at the tool commit (see the round-59 report). The work directory must be empty; the counter cleans its generated fixtures.
Without `--tool`, it extracts the implementation from the measured commit.
`--tool` is a control override, explicitly not a certification path.

The counter expects exits 0 for `equal`/`unrelated`, 1 for
`changed`/`missing`/`symlink`, and 2 for `unresolvable`, each with its matching
signature. It reports `C1_R59 rev=... passed=N/24 C1_R59_PASS=true|false`.
If the measured commit lacks the tool, its explicit failure signature is
`passed=0/24 C1_R59_PASS=false reason=tool-absent`.
The claim also requires skipped-work and always-accept controls to fail;
a positive counter line alone does not supply those control receipts. This
entry records the positive counter result and the control receipts only; execution of the gate's consumers is not claimed.

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
  by this entry; S289 is admitted in corpus/SOURCES.md at round 59.

## Amendment — round 60 (2026-10-30): installed discriminating counter, v2 plumbing arm, tested boundary

Lines above are unchanged and keep their meaning. This amendment is dated and
additive; it does not rewrite the round-59 record.

`verified-at:` 2026-10-30 (round 60) — re-measured at lane commit
`da2ae6b361de2d6294c6324a02ae141ff6cb482f`: the installed counter
`tools/executor-source-pin-measure.py` scored `passed=8/8 C1_R60_PASS=true`
(`.ufo/evidence/round-60/after/cert.out`) over the amended
`tools/executor-source-pin.py` v2 (worktree sha256
`d49ba88e002e8f77cb281d73770f9c729f96012d49885effb4f3507b51a02ade`, identical
at the measured commit), with every control arm failing
(`.ufo/evidence/round-60/controls/`).

### The decision table above gains one row, effective round 60

| Condition | Exit | Signature | Operator decision |
|---|---:|---|---|
| A declared blob read fails at plumbing level (trusted or candidate side) | 2 | `EXECUTOR_SOURCE_UNAVAILABLE` | No comparison verdict; the difference is unobservable, not absent. Repair object availability and rerun under verifier control. |

Round-59 spot-check defect 7 recorded that the v1 tool mapped this arm to
DRIFT (exit 1), contradicting the "unresolvable input" class above. The v2
tool (`tools/executor-source-pin.py`, lines 249-266 at the round-60 commit)
maps it to exit 2. The red-before witness is
`.ufo/evidence/round-60/controls/v1-tool-red.out`: the unfixed tool scores
`passed=7/8 C1_R60_PASS=false` with only the `corrupt` cell failing
(expected 2, observed 1) — the fix is shown able to fail.

### Exec-bit boundary: decided and now a tested cell

The boundary is decided, not enlarged (round-59 spot-check defect 4): blob
equality over declared regular sources is the contract; the mode is not bound
beyond regular-ness. Git's own index-entry layout is the ground (S291,
https://git-scm.com/docs/index-format, opened 2026-10-30): "9-bit unix
permission. Only 0755 and 0644 are valid for regular files. Symbolic links
and gitlinks have value 0 in this field." The counter's `execbit` cell flips
modes between 100644 and 100755 at constant bytes and expects exit 0
(`EXECUTOR_SOURCE_BOUND`); a symlink stays nonregular and drifts.

### The standing instrument is the round-60 counter

`.ufo/evidence/round-59/measure.py` (24 cells, one `--path` per call,
constant fixtures) remains the frozen round-59 instrument but is superseded
as the standing counter by `tools/executor-source-pin-measure.py`: 8 shuffled
class cells (`equal`, `unrelated`, `execbit`, `changed`, `missing`, `symlink`,
`corrupt`, `unresolvable`) over 5 declared paths (including the empty blob
`tools/empty-fixture.txt`) in ONE invocation per cell, per-run nonce fixture
bytes (S290), shuffled order, corrupt cell expecting exit 2. It reports
`C1_R60 rev=... passed=N/8 C1_R60_PASS=true|false`. Red receipts frozen
before data: `.ufo/evidence/round-60/controls/` (do-nothing tool-absent 0/8,
v1 tool 7/8, always-accept 3/8, fingerprint 3/8, sequence 3-5/8, hash-only
3/8, first-path-only 6/8, empty-blob-unsound 4/8). Sources added this round:
S290 (secrets), S291 (index-format); S103 (git-hash-object, the
content-addressed oid-equality ground) now also backs this entry.
