## Gate

Criterion for the round-59 Gate section: one row per candidate considered — corpus entries, claim
certifications, and considerthese proposals — each with a disposition (admit / reject / defer), an
evidence-based reason, an evidence pointer, and a concrete flip condition. Do not report admits
alone, and do not silently drop a candidate the round's Planned named. This criterion is drafted
from the round-58 forged-executor failure and the failed round-58 positive control; it binds the
round-59 lesson's Gate records.

Standing historical rejected targets carried into round 59 unchanged unless their own flip
condition fires (preserve; never rewrite, never reconstruct):

- **S285 keeps its `rejected` status.** S288 supersedes only the unreachable locator
  (`CORPUS.md` rule 2); it does not cure the rejected evidence class — vendor self-description,
  no measured outcomes. Flip: an independently located source with relevant measured outcomes.
- **Round-58 C2 certification stays rejected.** The frozen C2 counter accepted a claimant-authored
  executor: `.ufo/waves/round-58/w1/T58W1RevengerC2-receipts/attack-b-out.txt` — the bent lane
  prints `held=3/3 mutants=3/3 total=0 C2_R58_PASS=true` while the same forged lane under the real
  runner prints `ROW c2-fx-ok expect=0 got=3 differs` (two rows held of three, the corrected
  count). Round-59 C1 is a binding prerequisite, not a re-certification: per
  `.ufo/evidence/round-59/contract.json` (`trust_boundary`) the gate compares declared Git blobs at
  a candidate against a verifier-supplied trusted revision only — it does not attest execution,
  dependencies, interpreter identity, completeness of the source closure, or author-independent
  trust, and it is not round-58 C2 certification. Flip: none by rerunning round-58 instruments; a
  later round needs its own declared target and controls.
- **R51.6 stays open** in `corpus/routed-defects.json` (status `open`; assessment: the prospective
  practice improvement is not credited as the historical fix). Round-59 Gate records rejected
  candidates with reasons going forward; it does not reconstruct round 51's missing historical
  rejected-candidate record (round-58 withdrawal of R51.6 from the fixed set stands). No flip —
  this is a preservation rule, not a fixable defect.

Considered and rejected this round — the round's single consideration:

- **Claiming the executor-source-pin gate implements the considerthese/2026-10-28 proposal-2
  arm-liveness census — REJECTED.** Proposal 2 requires, for each frozen counter, a list of its
  arms and one committed input per arm that moves that arm's tally away from zero
  (`considerthese/2026-10-28.md`, self-improvement idea 2). The round-59 gate binds one declared
  executor's source blobs for one tool invocation (contract `interface`: `--repo --trusted
  --candidate --path…`, exit map 0/1/2); it enumerates no arms and requires no per-arm live
  inputs. Round-58 mined the census only as a successor-gate requirement, "not claimed
  implemented" (`corpus/lessons/round-58.md`, "considerthese mined"). Flip: a committed
  counter-level census instrument enumerating every frozen counter's arms with one committed
  input per arm that moves that arm's tally.

Control dispositions are Gate rows backed by receipts, not prose assertions: the counter's
`reason=tool-absent` zero path (`.ufo/evidence/round-59/measure.py:36-39`; the tool is absent at
base `b83f1bfc7b302f22e89d9631ac7e6ac87ea78c2a` and at freeze `e9cc34bec3f0c670550552bcc962563e7ae3ca58`
— `git cat-file -e` fails at both revisions), so missing tool counts zero; the skipped-work
control and the always-accept control must fail for C1 to score, and each records its committed
receipt whichever way it lands.

## Mistakes

Criterion for the round-59 Mistakes section: one row per captured failure with class, evidence
pointer, captured-by criterion (or `none` — the absence is the lesson), and a fix shown able to
fail on a named red case. Worked rows seeded by the round-58 events this round's claim answers:

| Class | Evidence | Captured-by | Fix and failability |
|---|---|---|---|
| forged-executor — the party producing the verdict is the party producing the evidence | `.ufo/waves/round-58/w1/T58W1RevengerC2-receipts/attack-b-out.txt` (quoted above); class analysis `.ufo/waves/round-58/w1/T58W1RevengerC2.md` §4 | none — no criterion bound an executed tally to the identity of the executor's source; the counter's executed arms ran the artifact-under-test's own executor | Round-59 C1 pins declared executor source blobs against the trusted revision before any executed result is credited. Shown able to fail (T59W1S56 probe, git 2.56.0, scratch fixtures): trusted bytes hash to blob `2e01eef0c14a…` at all four path spellings, forged bytes to `fbd2ab209ba4…`, so `changed` separates by blob id; `missing` separates by `git cat-file -e REV:PATH` exit 128 ("exists on disk, but not in <rev>"); `symlink` separates by `git ls-tree` mode `120000`. Those fixtures are the red cases; a gate that accepts any of them is wrong by construction. |
| positive-control-locator-drift | `.ufo/evidence/round-58/control/ctl-CTL_POS_c1.full`: `EXPLAIN evidence-bad R51.3 excerpt-not-in-lines .ufo/evidence/round-21/coldread/ledger.json`; final line `C1_R58: … total=1 C1_R58_PASS=false` | the round-58 controls pre-registration (one generation, recomputed, never read) correctly barred rerolling — but no criterion required a positive control's anchor to be durable across a cold-read re-bind | Failed positive receipts are retained and never substituted (`corpus/lessons/round-58.md`, "Terminal admission stop"): C1 lacked round-58 certification even with a later direct zero read; the row locator was repaired for durable truth to serve later rounds, not to re-certify round 58. Shown able to fail: any second control generation, or a PASS declared while the only positive-control receipt carries `evidence-bad`, violates the criterion; the retained receipt's `C1_R58_PASS=false` line is the red witness. |
| resolvability-by-syntax (pre-registered by this seat before the gate lands; not yet a landed failure) | T59W1S56 probe, git 2.56.0: `git rev-parse --verify <40-hex>` exits 0 and echoes the hex for a well-formed but absent object — the null OID `0`×40 and `deadbeef`×5 alike — while `git cat-file -e` exits 1 and `rev-parse <rev>^{object}` exits 128 for both | none — pre-registered by the round-59 criterion seat | The gate's `EXECUTOR_SOURCE_UNAVAILABLE` class (exit 2) must classify unresolvable candidates by object existence (`cat-file -e` or `<rev>^{object}`), never by bare `rev-parse --verify` acceptance, which is a syntax check. Red case: candidate `0`×40 must yield exit 2 `EXECUTOR_SOURCE_UNAVAILABLE`, not a mis-classified drift (exit 1). |

Number discipline carried from round 58: quote the receipt, not a summary — the real-runner
control over the bent lane held two rows of three (`held=0/1`, `held=1/1`, `held=1/1`), not the
earlier summary's one.
