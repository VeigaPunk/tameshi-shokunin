# K05 MigrationIntegrity — contract E attack (round-18 wave 1)

Scope: the round-18 manifest that waives `tools/bash-witness-study.py` at
`4acc607` (contract E), under tools/evidence-disposition.py at lane tip
`183f87b` (sha256 `f8f05c7a…`). All runs in a `/tmp` fleet-mirror clone at
`183f87b899e6cae46be98d251cbc87fb5118f6ca`, `env -u GIT_DIR -u GIT_WORK_TREE
-u GIT_INDEX_FILE -u GIT_COMMON_DIR`, cwd inside the clone. Clone:
`/tmp/tameshi-r18w1-K05-vl1ZAU/fleet/tameshi-shokunin`.

## Finding 1 (primary counterexample, fixable defect): `supersedes` as written can never pass

G7 (`tools/evidence-disposition.py:1412-1430`) requires the superseded
document to carry `schema == "evidence-dispositions-v1"` (:1416-1417) and
requires *every input of the superseded doc pinned identically* (:1422-1428).
Contract E names `supersedes = .ufo/evidence/round-17/dispositions.json`,
which is schema v2. Reproduced: manifest built exactly per contract E
(round-17 manifest bytes + `supersedes` retargeted + round-17 manifest pinned
in `inputs` + `tools/bash-witness-study.py` waiver at `4acc607`):

```
$ python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-18/dispositions.json --json
exit 2 — {"kind":"supersedes_mismatch",
  "message":"superseded document schema is not 'evidence-dispositions-v1'"}
```

Contract D (the only tool edit planned for this instrument) does not touch
`check_supersedes_lineage`. So contract E's manifest exits 2 at the expected
`--root . --json` gate forever — the `evidence-disposition-round18` row can
never hold. Precedent confirms the intended lineage: round-17's v2 manifest
supersedes round-14's **v1** manifest (star, not chain).

Smallest safe correction: amend contract E — `supersedes =
.ufo/evidence/round-14/dispositions.json` (the v1 root), while pinning the
round-17 manifest in `inputs` for provenance. Verified end-to-end in the
clone: after committing a marker edit to the tool, exit 0, `"status":
"clean"`, counts `{effective: 11, superseded: 1, passed: 11}`, and
`HISTORICAL tools/bash-witness-study.py rev=4acc607… sha256=49e9e5e2…`
matching the round-13 pin. Alternative (larger): extend G7 to accept v2
superseded docs — new code path, needs selftest coverage contract D does not
list. Not recommended this round.

## Finding 2 (missed blast radius): `evidence-disposition-round17-before` row also breaks

The moment the contract-E tool edit commits, BOTH round-17 registry rows
using unwaived manifests fail:

```
$ python3 tools/evidence-disposition.py --dispositions .ufo/evidence/round-17/dispositions.json
exit 2 — expected_input_digest_mismatch: tools/bash-witness-study.py
         observed 0ade8c6f… expects 49e9e5e2…
$ python3 tools/evidence-disposition.py --dispositions .ufo/evidence/round-17/dispositions-before.json
exit 2 — same
```

Contract E covers the `evidence-disposition-round17` row (superseded,
proposed to L1) but never names `evidence-disposition-round17-before`
(registry.json expects `exit: 1` + `"status": "failed"`; it will get exit 2).
The failure row cannot be repaired by editing `dispositions-before.json` —
that is committed round-17 evidence ("never edit pinned bytes"). Correction:
the registry proposal must also supersede `evidence-disposition-round17-before`,
or add a round-18 `dispositions-before.json` (with the waiver) plus a
replacement row to keep live negative-expectation coverage. Without one of
these, `tools/registry-check.py` reports the baseline row red — C2's
no-harm ruler fails.

## Q1 — does the waiver weaken what round-13 receipts prove?

No for the historical claim: the gate still re-verifies the waived blob at
`4acc607` against the round-13 pin (`:1534-1546`), so the receipts' measured
subject is unchanged — `49e9e5e2…` at `4acc607` (verified:
`git show 4acc607:tools/bash-witness-study.py | sha256sum` = pin; rev is a
round-13 commit and ancestor of master; zero edits to the tool since
`4acc607`). `.ufo/evidence/round-13/expected.json` itself stays pinned in the
manifest `inputs` map and is hashed before any predicate (`:1496-1506`).

Yes for live drift detection (tradeoff, previously admitted for two tools —
spotcheck §4 "committed edits to a waived tool are deliberately accepted"):
before the waiver, ANY edit to the tool fails the gate; after, only
*uncommitted* divergence does. The manifest never records the new tool bytes'
digest, so the gate cannot distinguish "the intended GIT_* scrub" from any
later committed edit. Mitigation exists and is cheap: `inputs` accepts any
lane-relative path, so the manifest MAY pin `tools/bash-witness-study.py`'s
new digest as a live `inputs` entry — restores drift detection at the cost
of a manifest update on every tool edit. Recommend recording the new live
sha256 in the receipt at minimum (git log gives it, but the receipt should
state it).

## Q2 — G1/G2 after the move

G1 (`:510-517`): live bytes must differ from the pin — holds once the scrub
edit commits; REJECTS the waiver before the edit lands (observed:
`historical_input_unneeded` on the committed-but-unedited clone). Hard
ordering requirement: tool edit and manifest land in the same commit, or the
manifest last; any gate run in between exits 2.

G2 (`:518-540`): live bytes must equal the comparator commit — observed
`historical_input_uncommitted` on an uncommitted worktree edit. G3 ancestry
(`:441-455`): `4acc607` is an ancestor of HEAD/master — holds.

Interaction risk with contract D (flagged, not proven): D retargets G2/G3
from `HEAD` to `refs/heads/<branch>`. Two consequences worth a spec line:
(a) detached-HEAD `--rev REV` measurement runs (registry-check clone
workflow) will see the waived tool's REV bytes differ from the branch tip →
false `historical_input_uncommitted` on historical runs; the comparator
should be the *evaluated* rev when one is given. (b) In a jj-colocated lane,
a live run mid-flight (worktree ahead of the branch ref) newly fails G2 —
stricter, probably intended, but it means the gate only passes at exported,
clean-tip states.

## Q3 — what the receipt must show (anti silent-pin-edit)

1. `historical_text` line: `HISTORICAL tools/bash-witness-study.py
   rev=4acc607… sha256=49e9e5e2…` — binds the round-13 pin to identical
   historical bytes (emitted by the tool; verified in clone).
2. Red-before: the gate against the NEW tool bytes under the UNAMENDED
   round-17 manifest exits 2 `expected_input_digest_mismatch` (observed
   above) — proves the waiver was needed, not a pin rewrite.
3. Immutability: manifest `inputs` pin for `.ufo/evidence/round-13/
   expected.json` = `a0160794…` (unchanged from round-14/17 manifests — G7
   enforces this when superseding the v1 doc); `git diff --stat <prev> <tip>
   -- .ufo/evidence/round-13` empty.
4. New tool digest recorded: sha256 of post-scrub
   `tools/bash-witness-study.py` printed in the receipt (the manifest does
   not pin it).
5. Registry receipt: round-18 row active and clean, round-17 row AND
   `evidence-disposition-round17-before` both superseded with pointers;
   `registry-check --json` held.
6. Atomicity: manifest and tool edit in one commit (or manifest second), so
   no evaluated rev ever sees waiver-without-edit (G1) or edit-without-waiver
   (digest mismatch).

No tool installs performed; no lane files modified outside this report.

Verdict: falls — contract E's `supersedes` targets a v2 document the unchanged
G7 rejects (demonstrated exit 2), and the `evidence-disposition-round17-before`
row breaks unnamed; both fixable (supersede the round-14 v1 + keep round-17 in
`inputs`; supersede or replace the `-before` row), with the drift-detection
weakening a disclosed tradeoff, not a defect.
