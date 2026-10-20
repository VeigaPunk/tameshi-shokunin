# X02 — Disposition v2 appended manifests (contract A)

Wave: tameshi round 17, wave 1. Seat: TameshiR17.X02DispositionV2Files.

## Files written (all owned)

- `.ufo/evidence/round-17/dispositions.json` — schema `evidence-dispositions-v2`, supersedes `.ufo/evidence/round-14/dispositions.json`.
- `.ufo/evidence/round-17/dispositions-before.json` — schema `evidence-dispositions-v2`, supersedes `.ufo/evidence/round-14/dispositions-before.json`.
- `.ufo/evidence/round-17/historical-rev.txt` — digest proofs.

## Construction

- `rows` copied verbatim from the parsed round-14 manifests (byte-compared parsed: `json.dumps(rows, sort_keys=True)` equality asserted post-write; `dispositions.json` = 11 effective + 1 superseded, `dispositions-before.json` = 12 effective).
- `expected_file` unchanged: `.ufo/evidence/round-13/expected.json`.
- `inputs` = round-14's three pins verbatim + the superseded round-14 file's sha256 (`dispositions.json` → `77faac58…9005`, `dispositions-before.json` → `a7a965bb…9725`, per `sha256sum` on live files; round-14 files are immutable so live = committed).
- `historical_inputs` = all 4 `tools/` paths pinned in round-13 `expected.json`, each at rev `4acc607dfd79f19d508bd50cdd06b77269fccd1d` with a reason string.

## Chosen rev proof

`4acc607dfd79f19d508bd50cdd06b77269fccd1d` (dispatch candidate) is an ancestor of master tip `98bea7da5801f4bc58e4187690ee1687c8a5061f`:

    $ git -C <lane> merge-base --is-ancestor 4acc607… 98bea7d…   → exit 0

Every `tools/` blob at that rev carries its pinned digest (`git cat-file blob <rev>:<path> | sha256sum`, all MATCH — full transcript in `historical-rev.txt`):

| path | pinned digest (round-13 expected.json) | @4acc607 | live @tip |
|---|---|---|---|
| tools/pin-disposition.py | 297253971d…f14f11 | MATCH | MATCH |
| tools/witness-metadata.py | df3390682a…0bed4 | MATCH | MATCH |
| tools/bash-witness-study.py | 49e9e5e20b…0ad80 | MATCH | MATCH |
| tools/mutate-and-run.sh | 75ed934dc8…9adc5 | MATCH | DRIFTED → `0673d2e537…8118aa` (post-round-16 jj repo-identity guard fix) |

`mutate-and-run.sh` drift is the operative motivation for `historical_inputs`; the other three are pinned for uniformity (contract: "for EVERY `tools/` path pinned in round-13 expected.json").

## Validation performed

- Python shape check (own, since the v2 tool is being staged in parallel by X01): both files parse as JSON; `schema == evidence-dispositions-v2`; `supersedes` is lane-relative and its sha256 is pinned in `inputs`; every `historical_inputs` key starts with `tools/` (else `historical_input_forbidden`), is present in `expected.json` `inputs` (else `historical_input_unknown`), and has a 40-hex rev + non-empty reason; every historical blob at the chosen rev equals the pinned digest (else `expected_input_digest_mismatch`); `rows` and v1 `inputs` byte-equal the round-14 source. All assertions passed.
- Not run: `tools/evidence-disposition.py` v2 path (tool staged by X01; not yet installed). L1 should run `tools/evidence-disposition.py --root . --json .ufo/evidence/round-17/dispositions.json` → expect 0 clean / 11 effective + 1 superseded, and on `dispositions-before.json` → 1 failed, `producer_before` unresolved, per contract A.

## Constraints honored

No jj, no git writes, no edits outside owned paths; read-only `git` plumbing only; no installs.

## Risks / blockers

- None. If the v2 tool reads `inputs` with integrity-first live verification, the added `supersedes` pin requires the round-14 file to remain byte-immutable — guaranteed by the appended-manifest convention.
- One nit for X01's implementation: my `historical_inputs` reasons mention the jj-fix drift factually; if the tool requires any reason-schema beyond `{rev, reason: text}`, contract A's spec was followed literally.

## Verdict

**built** — both v2 manifests written, rows byte-equal to round-14's, all four `tools/` digests proven at ancestor rev 4acc607dfd79f19d508bd50cdd06b77269fccd1d.
