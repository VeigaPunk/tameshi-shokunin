# SnapshotReview — tameshi round 12, wave w1 (narrowed per Main)

Advisory, lane-internal. Not an independent non-author review and not an admission.
Scope: the snapshot clause of the round-12 gate interface (`--snapshot DIR`). No production
writes. `tools/repeat-control.py` does not exist at HEAD `18ad5d0`; nothing below is observed
gate behavior. Claims are design review plus a sketch probe.

Authority model (per Main): the digest manifest is authoritative relative to its committed
revision. It is not self-authenticating. A self-consistent change to manifest plus inputs at a
different revision is out of scope; the two-evidence protocol compares the same committed revision.

## Contract under review

Source: `.ufo/waves/round-12/spec.json:3`: `--snapshot DIR validates committed input digests and
expected ID/exit, tamper exit2 snapshot_tampered.`

Precedent: `kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:407-410` and
`PROTOCOL-APPENDIX.md:45` (round-12 `expected.json` pinned only part of the inputs; an edit still
read `baseline: match`, exit 0).

## Required behavior (in scope)

R1. Every persisted input digest is verified before the first run, and again after the last run.
    Any mismatch, missing file, or unreadable file gives `snapshot_tampered`, exit 2.
R2. The manifest is parsed unambiguously. Duplicate keys are rejected, because otherwise the
    digest check in R1 is itself undefined (probe F: last-wins accepts an edit that first-wins rejects).
R3. Tamper is decided before any child runs. A tampered snapshot yields zero child executions and
    exit 2, never `controls_match` or `controls_mismatch`.
R4. Expected comparison: the observed finding ID and exit are compared to the `expected` values in the
    manifest. The expected values are hand-authored, not recorded from a run.

## Findings on the required behavior

**F-A (R2/R1). Duplicate keys.** Probe F reproduces the ambiguity. Required fix: reject duplicates. [in scope]

**F-B (R1). Post-run recheck.** Probe H: the child appends to an input during the run; the pre-run check
passes and the post-run check fails. Required: the post-run recheck (R1). [in scope]

**F-C (R4). Expected finding independence.** A record or regenerate mode would make `expected` circular and
reproduces the appendix regenerate-the-pin bypass. Required: no write mode in the tool. [in scope; reviewed
at code level only, not yet implemented]

**F-D (interface). `--snapshot` run semantics.** The contract says "validates committed input digests and
expected ID/exit" without naming the command or saying whether it runs. R4 requires running and comparing,
so the reading is: run the pinned argv N=3 times and compare to `expected`. **Decision for L1:** confirm the
argv source and the observed-≠-expected outcome. The contract names no ID for that outcome; do not map it
silently to `controls_match` or `controls_mismatch`.

**F-E (precedence). Ordering.** Usage (64), then R1/R2 verification (2), then runs, then verdict. Tamper versus
`baseline_nonzero` (both exit 2, different IDs) is unstated. **Decision for L1:** tamper wins, since it is
checked first.

**F-F (output format). Tamper stdout line.** The contract does not give a format. **Decision for L1:** pin one
line for the test.

## Unimplemented limits (reported, not required)

These are stronger threat-model proposals. They are not part of the round-12 requirement and must not be
implemented or tested as such.

- **L1. Self-consistent rewrite at the same revision.** Rewriting an input and its pin together passes R1–R4
  (probe E). Detection would need an external anchor on `expected.json` (committed blob or sha in the round
  LOG). Not required; the two-evidence protocol is the mechanism for same-revision comparison.
- **L2. Command and dependency graph.** Pinning the argv executable and its transitive dependencies is not
  required. Editing the command script without changing a pinned input is not detected.
- **L3. Unlisted files in the snapshot directory.** Probe C: an extra file passes R1 (digest-only). Set equality
  would catch it, but "every input" is only defined by the manifest, so this is a limit, not a requirement.
- **L4. Symlinks, absolute paths, `..`, and subdirectories in the manifest or DIR.** Not probed. [INFERENCE]
- **L5. Signatures or any authenticity of the manifest.** Out of scope per Main.
- **L6. Empty `inputs`.** Probe G passes vacuously. Not required under the narrowed scope; reported as a limit.
- **L7. Precondition: nothing committed yet.** `git ls-files` for `.ufo/evidence/round-12` and
  `.ufo/waves/round-12` returns 0 tracked files, and `ControlGate/expected.json` is absent. The "committed"
  premise is unmet today. This blocks acceptance, not the design.

## Minimal fixture (proposed; field names are a proposal)

```
DIR/
  child.sh        # cat data.txt; exit 0
  data.txt        # "ok\n"
  expected.json   # {"argv":["bash","child.sh"],
                  #  "inputs":{"child.sh":"<sha256>","data.txt":"<sha256>"},
                  #  "expected":{"finding":"controls_match","exit":0}}
```

## Exact expected behavior (required rows only)

| Case (committed DIR) | Finding ID | Exit | Child runs |
|---|---|---|---|
| pristine | `controls_match` | 0 | 3 |
| one-byte edit to `data.txt` | `snapshot_tampered` | 2 | 0 |
| delete `data.txt` | `snapshot_tampered` | 2 | 0 |
| duplicate `"inputs"` key | `snapshot_tampered` | 2 | 0 |
| child appends to `data.txt` during runs | `snapshot_tampered` | 2 | ≥1 (post-run recheck) |
| observed ≠ expected, pins clean | **undecided — L1 names the ID** (F-D) | — | 3 |

Limit rows, expected to pass (documented, not tested as required): add `extra.txt` (L3); rewrite
`data.txt` plus its pin together (L1); `"inputs": {}` (L6).

For the pristine row, the observable is exit 0, `controls_match`, and three byte-identical numbered
stdout/stderr/exit sets. For tamper rows, the observable is exit 2, the line from F-F, and no numbered run
output (`run-1` absent).

## Probe evidence

- `.ufo/evidence/round-12/SnapshotReview/probe.py`, sha256 `a71b40e2e1af1e6b6607ba670d1f7cbdb28307d7153d4f24457ded0c9a304890`
- `.ufo/evidence/round-12/SnapshotReview/probe-output.txt` (rows A–H plus post-run)
- Python 3.14.7, stdlib only. Scratch dirs under `/tmp/snapreview-*`.
- Results relevant to required behavior: strict sketch catches F (duplicate key), H-post (drift), and
  one-byte and deletion tamper. Digest-only misses F and H-post. Limit cases C, E, G pass as documented.

## Tools and installs

- None installed or updated. Used the existing `python3`, `git` (read-only), `sha256sum`. No commits,
  builds, or tests.

## Owned paths

- Written: `.ufo/waves/round-12/w1/SnapshotReview.md`
- Written: `.ufo/evidence/round-12/SnapshotReview/probe.py`, `.ufo/evidence/round-12/SnapshotReview/probe-output.txt`
- Not written: any production file, `LOG.md`, sibling seat directories.

## Residual risk and verification gaps

- The probe is a sketch, not the gate. Re-check R1–R4 against `tools/repeat-control.py --snapshot`
  once ControlGate lands. No pass is claimed.
- Decisions needed from L1: F-D (run semantics and observed-≠-expected ID), F-E (precedence), F-F
  (tamper stdout line).
- Round LOG entry: this lane changed no production file, so none is written here.
