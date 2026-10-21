# E07 — Git provenance rule (`git show` / `git rev-parse`) vs the four historical instrument shas

Seat: `TameshiR20-3.E07GitProvenance` (scout, read-only) · Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` · 2026-10-21
Godspeed axes: (1) quote fidelity from upstream git docs, (2) sha→bytes binding for all four historical shas, (3) reproducibility of every command, (4) scope discipline (one report file, zero production writes).
Tooling directive: **no installs performed** (git 2.56.0 already present); pacman untouched.

## Finding 1 — the provenance rule, quoted

- `git-show` docs (https://git-scm.com/docs/git-show, DESCRIPTION): *"For plain blobs, it shows the plain contents."* (8 words) — `git show <rev>:<path>` streams the **committed blob bytes**, i.e. the measured bytes.
- Object-name spelling (`<rev>:<path>`) lives in `gitrevisions(7)` (linked from both the `git-show` and `git-rev-parse` doc pages, "SPECIFYING REVISIONS"): *"names the blob or tree at the given path in the tree-ish object named by the part before the colon"* (21 words).
- `git-rev-parse` resolves the same spelling to the blob id — observed: `git rev-parse 6fd220bc:.ufo/evidence/round-20/stage/receipt-window.py` → `ebb70e49d7b0c255ff8df1c9aeb2d0845052656c`; `…/stage/measure.py` → `7f9fb1c5891e86efa3f1f2775491cc27e3f33ea6` (repo object format `sha1`; the contract's `frozen_sha256` values are sha256 **content digests** of the same bytes — two names, one byte stream).
- Rule half (b): a working-tree file is a separate byte source — untracked, mutable, addressed by no revision — and is **not** the measured bytes. Demonstration below (the ruler case).

## Finding 2 — frozen staged instruments verified at the frozen commit (HEAD = 6fd220bc)

```
$ git show 6fd220bce3705498d1d1054e99e3cae73c203751:.ufo/evidence/round-20/stage/receipt-window.py | sha256sum
f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc  -        == contract.receipt-window.frozen_sha256 ✓
$ git show 6fd220bce3705498d1d1054e99e3cae73c203751:.ufo/evidence/round-20/stage/measure.py | sha256sum
f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d  -        == contract.round20-measure.frozen_sha256 ✓
```
Worktree copies hash identically today, but per Finding 1 the committed blob — not the worktree copy — is the evidence basis.

## Finding 3 — each historical instrument sha named and bound to bytes (rider satisfied)

| sha256 | name | provenance (all read-only) |
|---|---|---|
| `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` | round18-measure | **blob-provable**: `git show 6435388dee766325af10ad44d8b3dee8371fc9ff:.ufo/evidence/round-18/measure.py \| sha256sum` → exact match ✓ |
| `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12` | witness-tool | **blob-provable**: `git show 2f794eb84d8916a200ebefbdef8675238d9b7441:tools/bash-witness-study.py \| sha256sum` → exact match ✓ (blob `bac63301…`; also carried at `.ufo/waves/round-18/staged/tools/bash-witness-study.py`) |
| `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` | witness-runner | **blob-provable**: `git show 2f794eb84d8916a200ebefbdef8675238d9b7441:tools/mutate-and-run.sh \| sha256sum` → exact match ✓ (blob `fd1a63a3…`; also at `.ufo/waves/round-18/staged/tools/mutate-and-run.sh`) |
| `96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef` | round19-ruler-wave1 | **not a blob anywhere** — see Finding 4 |

Blob-at-rev outputs observed (verbatim):
```
$ git show 2f794eb84d8916a200ebefbdef8675238d9b7441:tools/bash-witness-study.py | sha256sum
8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12  -
$ git show 2f794eb84d8916a200ebefbdef8675238d9b7441:tools/mutate-and-run.sh | sha256sum
d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b  -
$ git show 6435388dee766325af10ad44d8b3dee8371fc9ff:.ufo/evidence/round-18/measure.py | sha256sum
7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37  -
```

## Finding 4 — round19-ruler-wave1 (`96a68b60…`): the working-tree/scratch case, proven exhaustively

1. **No reachable commit carries it at any path.** `git rev-list --all -- .ufo/evidence/round-19/measure.py` → 19 commits; hashing the blob at every one yields seven distinct digests (`7af3e951…`, `8b6eb1fe…`, `3f19a16b…`, `bb651eef…`, `fac15f7b…`, `e9b44cad…`, `c538c33d…`) — never `96a68b60…`.
2. **It never entered the object database at all.** Full scan `git cat-file --batch-all-objects --batch` (5,892 objects, including unreachable ones), sha256 of every blob: zero blobs hash to `96a68b60…`. The other three historical shas each appear as exactly one blob.
3. **The bytes are nonetheless recoverable from committed bytes** as a deterministic slice: the second ```` ```python ```` fence of `.ufo/waves/round-19/w1/ReceiptDesign.md` (blob `bcf455eac80f531d1636491ba80697bab780e1f8`, identical at baseline `c144dcd8` and frozen `6fd220bc`), lines 53–376:
```
$ git show c144dcd807166dfc275c1ac2936fd2fa4b678bda:.ufo/waves/round-19/w1/ReceiptDesign.md | sed -n '53,376p' | sha256sum
96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef  -
$ git show 6fd220bce3705498d1d1054e99e3cae73c203751:.ufo/waves/round-19/w1/ReceiptDesign.md | sed -n '53,376p' | sha256sum
96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef  -
$ git show c144dcd807166dfc275c1ac2936fd2fa4b678bda:.ufo/waves/round-19/w1/ReceiptDesign.md | sha256sum   # negative control: whole report blob ≠ ruler
38a6259b04aceda11249f923a00ff3888c71cedc3d9c1839b2ffd1f3b5be1c93  -
```
4. The originally recorded scratch original `/tmp/tameshi-r19-ReceiptDesign-k1jzTs/audit.py` still exists and hashes to `96a68b60…`, but `/tmp` is outside the repo and unversioned — exactly the "working-tree file" class Finding 1 excludes as a measured-bytes basis. It is corroboration, not evidence-grade provenance.

**Tie-in to C1:** three of four historical instruments satisfy the strict rule (committed blob at `<rev>:<path>` reproduces the recorded sha256). The fourth is attested only by a deterministic extraction from a committed *report* blob — committed bytes, but not a blob at the instrument's own path. The contract's `historical_classified` row requires only that the installed gate **classify** the four shas (`stage/measure.py` `EXPECT_HIST` names all four, contract `.ufo/evidence/round-20/contract.json:38-42`), which is well-defined for all four since classification is by digest. Any future need to *re-execute* the ruler must re-derive bytes from the `ReceiptDesign.md` fence slice (Finding 4.3).

## Commands used (all read-only; no lane file touched except this report)

`git rev-parse`, `git show <rev>:<path> | sha256sum`, `git ls-tree -r`, `git show --stat`, `git status --porcelain`, `git log/rev-list --all -- <path>`, `git cat-file --batch-all-objects --batch` (scan driven by a throwaway in-memory Python loop; nothing written), `sha256sum`, `sed -n`. No staged checker was executed (not my item); no builds/suites/linters; no installs.

## Agree / disagree

- **Agree** with `contract.json` instrument table: both `staged_path` values are correct and blob-verified at the frozen commit.
- **Agree** with the rider: per-sha naming is required — six distinct instrument shas are in play (2 staged + 4 historical); a singular "frozen SHA" would be false.
- **Disagree (wording only)** with the wave-context frozen-facts line "adds … `stage/receipt-window.py` … `stage/measure.py`": the committed paths are `.ufo/evidence/round-20/stage/*.py`; `git show 6fd220bc:stage/measure.py` fails with `fatal: path 'stage/measure.py' does not exist in '6fd220bc…'`. `contract.json`'s own `staged_path` is correct, so this is a context-summary erratum, not a contract defect. (D07 owns wording.)

## Defects

1. **[wording, non-blocking]** Frozen-facts shorthand `stage/…` vs committed `.ufo/evidence/round-20/stage/…` — see Disagree above. Reproduction: `git show 6fd220bce3705498d1d1054e99e3cae73c203751:stage/measure.py` → fatal.
2. **[provenance asymmetry, non-blocking]** `round19-ruler-wave1` (`96a68b60…`) is not blob-addressable at its own path anywhere in history; its durable attestation is the `ReceiptDesign.md` fence-slice reconstruction. Seats A01 (ruler reviewer) and B10 (ruler receipt row) should state the ruler's provenance this way rather than claiming a committed `measure.py` blob.
3. **[observation]** Commits `2f794eb8…`, `6435388d…`, `040d1826…` (instrument carriers) have empty subject lines under `git log -1 --format='%s'`. Noted without judgment.

## Remaining unknowns

- None for my question. (Whether the empty-subject commits stem from the jj bridge is out of scope.)
