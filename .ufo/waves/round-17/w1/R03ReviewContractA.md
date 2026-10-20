# R03 — Contract A review: v2 dispositions, `historical_inputs`, integrity ordering

Reviewer: TameshiR17.R03ReviewContractA (leaf, read-only outside this report).
Target: contract A (wave context) vs `tools/evidence-disposition.py` at
`98bea7da5801f4bc58e4187690ee1687c8a5061f` (`run_mode` :1125-1213, `safe_file`
:230-262, `read_regular` :264-315, `validate_inputs` :317-330,
`validate_expected` :452-482), plus the round-17 artifacts X02 has landed
(`.ufo/evidence/round-17/dispositions{,-before}.json`).

Because the staged v2 tool was still a byte-for-byte copy of the committed v1
file when this review ran (sha256 `1609a9df…42d2d95` for both, 1956 lines, 12:31),
I validated contract A against the committed code and against a **reference
probe**: a `/tmp` copy of the committed tool patched to the contract's letter
(helpers `git_run`/`validate_historical`/`read_historical`, v2 branch in
`run_mode`, payload field). The probe and two deliberately wrong mutants
(fallback-on-mismatch, `text=True` blob read) are what make the selftest list
below discriminating rather than aspirational. Probe artifacts are under
`/tmp/tameshi-r17w1-R03ReviewContractA-4BofiO/`; nothing outside this report
was written in the lane.

## Answers to the three questions

**1. Integrity-first ordering — v1 holds; v2 is only teeth-safe if the
classification happens before the live expected-inputs loop.** In v1 the
dispositions pins are hashed at :1164-1177 before the expected file is parsed,
and every `expected.inputs` digest is verified at :1182-1192 before
`load_receipts`/`evaluate_dispositions` (:1194-1202). The only structural
validation before the hash loops (`validate_rows` :1153) reads no receipt
bytes; the docstring claim at :42-46 is accurate. A v2 implementation must
decide *which* `expected.inputs` keys are historical before it enters the
:1182 loop and skip only those, then read the blob and compare it to
**expected.json's** pin. A live-first "try live, fall back to git on mismatch"
order preserves the edited-file case but keeps failing when the live
instrument is deleted, symlinked, or replaced by a directory. Measured with the
fallback mutant on a tip clone + the round-17 manifest:

| live `tools/mutate-and-run.sh` state | contract-correct probe | fallback mutant |
|---|---|---|
| edited (appended byte) | 0 clean | 0 clean (fallback fires) |
| deleted | 0 clean | 2 `expected_input_missing` |
| symlink to a copy | 0 clean | 2 `path_rejected` |
| directory | 0 clean | 2 `path_rejected` |

Contract A says "reads bytes with `git cat-file blob …` instead of the live
file"; it never says this must be classification-before-read. That is the
largest unspecified degree of freedom in A and the one that leaves the
R16-OP1 repair half-applied (instruments "move by design" includes removal).

**2. v1 byte-identical — behaviourally reproducible, but the comparison
surface is undefined.** With a careful probe, v1 output is identical in
text mode (exit + stdout + stderr) on 8 cases and identical in JSON after
dropping `tool`/`tool_sha256` on 5 cases: clean (`0`, 11 effective + 1
superseded), `dispositions-before` (`1` `expected_contains_missing`),
row-missing (`1`), row-duplicate (`1`), tampered receipt (`2`
`input_digest_mismatch`), bad schema (`2` `schema_mismatch`), a v1 doc
carrying a stray `historical_inputs` key (`0` — still ignored), empty `inputs`
(`2`). Two traps: (a) `tool` and `tool_sha256` necessarily change, so
"byte-identical" cannot cover the raw JSON payload; (b) the `schema_mismatch`
detail string for a non-v1/v2 schema is easy to "improve" into a v1-visible
change. Define the surface as *text-mode stdout byte-equal + JSON equal after
removing `tool`/`tool_sha256`*, and keep the v1 invalid-schema detail text.

**3. Tamper detection of every round-12/13/14 evidence input — v1 covers all
13 expected inputs and all 3 disposition pins; v2 at tip must keep the 9
evidence inputs live and may only move the 4 `tools/` pins to git.** Measured
at the round-13 tree (`4acc607d`, the rev whose blobs equal the pins): every
one of the 13 `expected.inputs` mutated one at a time → exit 2
`expected_input_digest_mismatch` (13/13); `verification.json`,
`expected.json`, `producer-oracle-repair.json` → exit 2
`input_digest_mismatch`; symlink/directory substitution → `path_rejected`.
Ordering beats semantics: dropped row + tampered receipt → exit 2
`input_digest_mismatch`, not exit 1. Under the v2 manifest at the tip, the
9 evidence inputs → 2 `expected_input_digest_mismatch` (9/9) and the 4 pins
(`round-14/dispositions.json` included) → 2 `input_digest_mismatch` (4/4);
live edits of a declared historical tool are correctly invisible.
Round-17 manifest facts: rows equal round-14's (11 effective + 1 superseded /
12 effective), all 4 `inputs` pins match live bytes, `4acc607d` is an ancestor
of tip, and all 4 `tools/` blobs at `4acc607d` match `expected.json`'s pins.
Probe results on the live lane: `dispositions.json` → exit 0 clean,
11 effective + 1 superseded; `dispositions-before.json` → exit 1
`expected_contains_missing` ("producer_before unresolved"). Without
`historical_inputs`, the repair is unreachable at tip: removing the block from
`dispositions.json` yields 2 `expected_input_digest_mismatch` (measured), and
the v1 before-manifest at tip yields the same 2, so a v2 before-manifest that
omitted the block could not produce the required exit 1.

## Findings (severity, evidence, selftest that catches it)

### F1 — HIGH — contract does not require historical classification before the live read
`run_mode` :1182-1192 reads every `expected.inputs` key through
`safe_file`+`read_regular` unconditionally; a v2 patch that consults git only
after a digest mismatch (or after a caught `CouldNotEvaluate`) passes the
live-lane demonstration and still exits 2 for deleted/symlinked/directory live
instruments (table above). **Selftest:** `v2-live-tool-deleted`,
`v2-live-tool-symlink`, `v2-live-tool-directory` (each expected 0 clean) plus
`v2-live-tool-edited` (0) and the no-historical control for each (2:
`expected_input_missing` / `path_rejected` / `path_rejected` /
`expected_input_digest_mismatch`).

### F2 — HIGH — `rev` is specified as a 40-hex *commit* but nothing in the contract forces commit-ness
`git cat-file blob <tree-id>:<path>` succeeds: I resolved the round-13 tree
`b40a9b8b4c90329fa9dd19fb70be94d5c9c4e61a` and got the pinned
`tools/pin-disposition.py` bytes (sha256 `2972539…`), while
`git rev-parse --verify <tree>^{commit}` correctly fails with "expected commit
type". An implementation that validates `^[0-9a-f]{40}$` and calls
`cat-file blob <rev>:<path>` therefore accepts a tree object, and an
implementation that passes arbitrary strings accepts `HEAD`, branches, or
`4acc607dfd79`. **Selftest:** `v2-rev-head`, `v2-rev-branch`, `v2-rev-abbrev`,
`v2-rev-uppercase`, `v2-rev-tree`, `v2-rev-blob`, `v2-rev-bool` (JSON `true`),
`v2-rev-missing-object` → all 2 `historical_input_unavailable`; `v2-rev-valid`
→ 0. The probe's `rev-parse --verify --quiet --end-of-options <rev>^{commit}`
+ 40-hex recheck satisfies this.

### F3 — MEDIUM — blob bytes must never pass through text mode
`subprocess.run(..., text=True)` applies universal-newline translation: a
committed `a\r\nb\r\n` blob came back as 4 bytes (sha256 `911169dd…`) instead
of the 6 stored bytes (`58055bdc…`). A CRLF fixture lane with the raw-blob pin
is clean under the probe and exits 2 `expected_input_digest_mismatch` under
the `text=True` mutant. The current tools are LF, so this is latent, but a
future `tools/` pin on any generated/binary file would silently false-fail.
**Selftest:** `v2-blob-bytes-crlf` (committed CRLF blob, pin = sha256 of raw
blob → 0 clean; the `text=True` implementation must fail this case).

### F4 — MEDIUM — the contract names three finding ids and leaves the rest undefined
A and v1 define `historical_input_forbidden`, `historical_input_unknown`,
`historical_input_unavailable`, and reuse `expected_input_digest_mismatch`.
Unspecified: unpinned/non-canonical `supersedes`, non-object
`historical_inputs`, `rev` type errors (int/bool/null), empty/non-string
`reason`, unknown keys inside an entry. The probe chose
`input_unpinned` (supersedes not pinned), `path_rejected` (non-canonical key or
supersedes), `dispositions_field_invalid` (shape/type errors) — all exit 2 —
and those ids should be written into the tool docstring before integration,
because the selftest can only assert what is specified. Measured probe exits:
all of the above 2; the three contract ids 2 as required.
**Selftest:** `v2-supersedes-unpinned`, `v2-supersedes-absolute`,
`v2-historical-not-object`, `v2-historical-rev-int`, `v2-historical-rev-bool`,
`v2-historical-reason-int`, `v2-historical-extra-key`, each asserting the
documented id and exit 2.

### F5 — MEDIUM — overlap between `inputs` and `historical_inputs` is unspecified
The two pins are different authorities: `inputs` is live-verified (:1167-1177)
and `expected.inputs` is live-or-git-verified (:1182-1192). A path in both can
be satisfied only if the live pin and the rev pin are both honored. The probe
enforces both (measured: `inputs` pin = live digest + expected pin = rev digest
→ 0 clean; `inputs` pin = rev digest + live drift → 2 `input_digest_mismatch`).
An implementation that skips the live pin for a historical key silently
weakens the dispositions `inputs` guarantee. **Selftest:**
`v2-overlap-both-pins` (0) and `v2-overlap-live-pin-violated` (2
`input_digest_mismatch`); optionally reject overlap with a documented id.

### F6 — MEDIUM — identity-guard failure modes beyond "root in a super-repo"
The contract requires `realpath(rev-parse --show-toplevel) == realpath(root)`.
Measured on the probe: root inside a super-repo → 2
`historical_input_unavailable` ("not its own git toplevel" — verified
`git -C sub rev-parse --show-toplevel` returns the parent); a non-git copy of
the lane → 2 `historical_input_unavailable`; `PATH` without `git` → 2
`historical_input_unavailable` (not `internal_error`); text mode stays one line
(`EVIDENCE_DISPOSITION: could_not_evaluate exit=2 id=historical_input_unavailable
detail=…`). v1 stays git-free: the 8-case differential ran in `.git`-less
copies and exited 0/1/2 as divided above. **Selftest:** the three cases above
plus `v1-nongit-clean` (0) and `v2-git-unreadable` (`.git` mode 000 → 2), which
shares the same mapping. Note git's `safe.directory` refusal (documented
"dubious ownership") lands in the same bucket; no extra code needed, one case
if a grader uid differs.

### F7 — MEDIUM — "byte-identical" needs an explicit comparison surface
See answer 2. **Selftest:** a differential harness in `--selftest` is not
possible (the old tool is replaced in place), so this belongs in the wave
receipt: text-mode stdout+exit over the 8 cases above must be byte-equal, and
JSON must be equal after removing `tool`/`tool_sha256`. Also assert the v2
payload adds `expected_inputs_historical` **only** for v2 (v1 keys unchanged,
measured: `keys_equal True`), and that a v1 doc with a stray `historical_inputs`
key is still ignored (`v1-with-v2-key` → 0).

### F8 — LOW/MEDIUM — key validation order and prefix traps
Contract lists forbidden before unknown. Measured probe: an evidence key that
is in `expected.inputs` → `historical_input_forbidden`; a `tools/` key not in
`expected.inputs` → `historical_input_unknown`; `tools/../.ufo/…` and a NUL key
→ `path_rejected`; `tools-evil/x`, bare `tools`, `Tools/x` → forbidden.
**Selftest:** one case per line; keep the forbidden-before-unknown order so a
combined-invalid key has one deterministic id.

### F9 — LOW — git environment inheritance
`git -C <root>` does not override `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_OBJECT_DIRECTORY`, or `GIT_CONFIG_*`. The sha256 pin still prevents byte
substitution (a forged object must hash to the pin), so this cannot smuggle
content; it can only confuse provenance/identity. Recommended: scrub `GIT_*`
in the subprocess env (or rely on the guard, which then fails closed).
**Selftest:** `GIT_DIR=<other-repo>` → 2 `historical_input_unavailable`, never
a clean read from the foreign repo.

### F10 — LOW — round-17 manifest reason text overstates drift (X02-owned file)
`dispositions.json` says of `tools/pin-disposition.py` that "jj branch-tip
resolution repair landed later". Measured: live digest = run-13 pin = blob at
`4acc607d` = `2972539…`; `git diff 4acc607d 98bea7da -- tools/pin-disposition.py`
is empty. The same holds for `witness-metadata.py` and
`bash-witness-study.py`. Only `tools/mutate-and-run.sh` moved
(`0673d2e5…` live vs `75ed934d…` pin). `historical-rev.txt` §3 states this
correctly, so the manifest reason should be corrected (or generalized to
"declared historical per contract A's rule for every pinned tools/ path")
before integration; otherwise the audit trail misnames the moved instrument.
Not a gate failure. No selftest is possible for prose; the receipt table is
the check.

### F11 — LOW/INFO — provenance limits of `historical_inputs`
The rev is not required to be an ancestor of HEAD or even a commit’s tip of
this branch; the pin is content-addressed, so acceptance only proves "some
object in this repo has these bytes". Contract A's `4acc607d` is an ancestor
(verified), but the tool does not (and by contract need not) check ancestry.
Accepting a tree id (F2) makes the provenance claim weaker than the contract
text. Also, a shallow clone lacks old objects → 2 `historical_input_unavailable`;
the live lane’s full history is required (clone `.git` was 9.1 MB).

### F12 — INFO (cross-contract) — the registry/recipe still names the round-14 manifest
`SKILL.md:1601` and `:1681` register
`--dispositions .ufo/evidence/round-14/dispositions.json`. That v1 command is
red at tip by design (measured 2 `expected_input_digest_mismatch`), and A's
repair manifest is not the registered path. Unless X04 repoints the registry
row to `.ufo/evidence/round-17/dispositions.json`, C2's "registered command
returns its registered outcome" is graded against the unrepaired manifest.

## Selftest checklist the staged tool must contain (ids and required assertions)

Contract-mandated (X01 already has these; keep the ids explicit):
`v2-clean-historical` 0/clean/11+1 · `v2-historical-digest-mismatch` 2
`expected_input_digest_mismatch` · `v2-historical-unknown` 2
`historical_input_unknown` · `v2-historical-forbidden` 2
`historical_input_forbidden` · `v2-historical-missing-rev` 2
`historical_input_unavailable` · `v2-superrepo-root` 2
`historical_input_unavailable` · `v1-clean-unchanged` 0 · `v2-live-nonhistorical-mismatch`
2 `expected_input_digest_mismatch`.

Added by this review (each discriminates a measured mutant or an unstated
contract degree of freedom): `v2-live-tool-deleted|symlink|directory` 0 ·
`v2-rev-head|branch|abbrev|uppercase|tree|blob|bool` 2 · `v2-blob-bytes-crlf`
0 · `v2-overlap-both-pins` 0 and `v2-overlap-live-pin-violated` 2
`input_digest_mismatch` · `v2-supersedes-unpinned` 2 `input_unpinned` ·
`v2-historical-entry-shape` (rev int/bool, reason int/empty, extra key) 2
`dispositions_field_invalid` · `v2-key-tools-evil|tools|Tools` 2 forbidden ·
`v2-key-nul|traversal` 2 `path_rejected` · `v2-git-unavailable-binary` 2
`historical_input_unavailable` · `v1-nongit-clean` 0 · `v1-with-v2-key` 0 ·
`v2-integrity-before-predicates` (bad rev + dropped row → 2, not 1) ·
`v2-payload-historical-v2-only`.

## Residual risk
- `historical_inputs` intentionally blinds the gate to future live edits of
  declared tools. Round 17 declares all four `tools/` pins historical even
  though three are unchanged, so any later live change to those three is
  invisible by construction; that is the contract's instrument-move policy, not
  a defect, but it should be stated in the tool docstring (it changes what
  "tamper detection" means for four paths).
- Text-mode single-line output is preserved for git failures in the probe, but
  only if the implementation folds git stderr to its first line; raw stderr
  would break line-oriented consumers.
- The reference probe is not a delivered artifact; its only purpose is to show
  the listed cases are green for a contract-faithful implementation and red for
  the two named mutants. It was not installed and nothing outside this report
  was written in the lane.

Verdict: **partial** — contract A is implementable and the two stated outcomes
reproduce (0 clean 11+1; 1 failed producer_before), v1 is behaviourally
reproducible and its 13-input tamper coverage is intact, but F1/F2 must be
made normative (classification before the live read; rev resolved as a commit)
and F3–F8 pinned to exact ids/shapes before the staged tool can be judged to
hold the interface.
