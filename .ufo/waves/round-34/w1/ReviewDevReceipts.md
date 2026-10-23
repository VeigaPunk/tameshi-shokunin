# [seat ReviewDevReceipts] Amendment-6 dev receipts — internal-consistency audit

Round-34 C1 wave, dev-receipt consistency check of `.ufo/evidence/round-34/dev/` against
amendment-6 semantics in `.ufo/evidence/round-33/c1/c1-measure.py` (sha256
`f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`, matches pin) and the
byte-pinned artifacts. Lane tip audited: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (scratch
clone detached at it). The counter was exercised **by module import only** (never as a
default-mode run), per the consumed kill rule.

## Pin verification (all exit 0)

| artifact | command | result |
|---|---|---|
| tool | `git -C …/lane show 0b99d48:tools/tally-audit-v2.py > tool.py; sha256sum` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` — **matches pin** |
| runner | `git -C …/lane show 0b99d48:tools/mutate-and-run.sh > pristine.sh; sha256sum` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — **matches pin** |
| counter | `sha256sum .ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c…a07f28c` — **matches pin** |
| rev order | `git merge-base --is-ancestor 6aaad5b c17e593b && … c17e593b 0b99d48` | both exit 0 (6aaad5b → 9dd3174 → c17e593b → 0b99d48) |
| byte drift | `git diff --stat c17e593b 0b99d48 -- tools/ .ufo/evidence/round-34/dev/` | empty: tool/runner/dev receipts identical at measurement rev and tip |

## Check 1 — witness-probes.json: 8 verdicts, exact set-aware semantics — PASS

`ho_witness_ok` (counter lines 184–221, amendment 6) branches: kill+head requires a
leg-assignment diff (bare-`st_x=$?` multiset `A` or all-`st_*=` multiset `X` must change) with
byte-identical block; accept+head requires identical block; accept+vector requires `a == b`
with bytes changed; kill+vector requires `a != b` and block changed. Each stored verdict lands
on exactly the branch its probe name describes:

| stored verdict (witness-probes.json) | branch exercised |
|---|---|
| `Q1-comment-accept -> (True, 'vector-equivalence')` | accept+vector, `a==b` and `mutated != pristine` |
| `Q3-inert-head-kill -> (False, 'head-edit-cannot-kill')` | kill+head, A/X multisets unchanged |
| `Q3b-ridealong-accept -> (False, 'head-with-block-edit')` | accept+head, block also edited (lethal ride-along refused) |
| `K-extra-leg-assign-kill -> (True, 'head-leg-assignment')` | kill+head, X multiset changed (extra `st_js=` line) |
| `K-nonbare-leg-kill -> (True, 'head-leg-assignment')` | kill+head, A multiset changed (bare `st_js=$?` lost) |
| `A-inert-head-accept -> (True, 'head')` | accept+head, identical block |
| `A-head-with-block -> (False, 'head-with-block-edit')` | accept+head, block also edited |
| `KV-block-identical -> (False, 'block-identical')` | kill+vector, `pb == mb` |

Re-run proof (reconstructed probe inputs — the L1's generator script is not committed; every
verdict is input-insensitive within its class): my scratch script `/fast/scratch/hyaku/
tameshi-r34-seats/ReviewDevReceipts/audit.py` rebuilt all 8 probes against the pinned runner
bytes and called `ho_witness_ok` via module import. Byte-compare of my 8 lines against the
stored JSON strings: `match: True n=8` (`python3` compare, exit 0). Both preamble lines of
`witness-probes.stdout` reproduce byte-identically on the pinned runner: `VERSION in head:
True` (VERSION at runner line 177, inside `head_of`) and `st_js line count: 1`
(`grep -c '^  st_js=\$?'` = 1, line 1390); `diff` of stored-vs-rerun preamble exits 0.

## Check 2 — panel.stdout 18/18 + 8/8 line — PASS

File: `panel copies: 26 kill: 18 accept: 8` / `PANEL: kill=18/18 accept=8/8 elapsed=109.0s`.
Structural counts from v1 (`round-32/c1-measure.py` 82–175): `frozen_kill`=9 + `generated_kill`=9
= **18**; `frozen_accept`=6 + `generated_accept`=2 = **8**; total **26**, seed-independent.
Independent re-score via `c1m.public_panel(bytes, '685f63bd25263908')` + `c1m.score_tool`
against the pinned tool (scratch `tool.py`): `panel copies: 26 kill: 18 accept: 8`, then
`PANEL: kill=18/18 accept=8/8 elapsed=251.2s` — hit counts byte-match; elapsed differs
(109.0s vs 251.2s) as expected for a load-dependent wall clock; not a defect.

## Check 3 — tool-selftest.stdout 22/22 line — PASS, with provenance caveat (Finding 2)

Trailer `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` present. Re-run of the pinned tool
(`python3 tool.py --selftest`, scratch dir with `mutate-and-run.sh` sibling) exited **0** with
**23 stdout lines**: 22 `CASE … (exit N)` lines + trailer, all `PASS` — the code prints one
CASE line per case unconditionally (`tool.py:670`). The committed receipt is only the last two
CASE lines + trailer (3 lines): a `tail -n 3`-style partial capture, internally consistent but
not a byte-complete stdout. No wrongness implied; the claim itself re-verified.

## Check 4 — authoring-receipts.json: 14 entries, all expected — PASS

14 entries (8 `ho-kill-*`, 6 `ho-accept-*`), `id` set equal to the 14 sealed filenames in
`.ufo/evidence/round-33/heldout/`; every `as_expected=true`; `set` matches the id prefix; every
tool verdict matches its label (kill → `["KILL",1,"TALLY_AUDIT: FAIL (…)"]`; accept →
`["ACCEPT",0,"TALLY_AUDIT: PASS (…)"]`). Independent re-validation of all 14 sealed copies
through the module (`validate_ho` → `apply_edits` → `ho_witness_ok`, pristine pinned bytes):
`heldout entries revalidated=14 mismatches=0` — every `edits_ok`, witness `(ok, reason)` tuple,
`as_expected`, and label check re-derived and equal. Extra byte-compare beyond the required
scope: re-scored `ho-kill-vector-setup-threshold` through `run_tool_sandboxed` →
`('KILL', 1, 'TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)')`,
**byte-identical** to the receipt's `tool` cell (`tool_rescore_byte_match=True`).

## Findings

**[LOW] Receipts landed at 6aaad5b, not c17e593b as LOG/lesson imply — commit-message overreach.**
`git log --format='%h %s' -- .ufo/evidence/round-34/dev/authoring-receipts.json` → only
`6aaad5b` (same for all six dev files); `git show --stat c17e593b` → exactly the 14 heldout
JSONs, no dev receipts; `git diff --stat 6aaad5b 0b99d48 -- .ufo/evidence/round-34/dev/` →
empty. Yet LOG.md:1835 attaches `— c17e593b` to the clause naming
`round-34/dev/authoring-receipts.json`, and the c17e593b commit message ("…per-copy authoring
receipts") describes files it does not contain. Consequence, not fabrication: the committed
order cannot demonstrate "amendment adopted BEFORE any sealed authoring" — the evidence of
that authoring lands in the same commit as the gate it exercises. The gate's precedence is
demonstrable only via scratch ordering; the receipts' content does prove the *amended* gate
was in force at authoring time (`Q1 … (True,'vector-equivalence')` is unreachable under the
set-blind rule, which demanded `a != b` for all sets).

**[LOW] tool-selftest.stdout is a 3-line tail, not full stdout.** Reproduce: committed file =
3 lines (`wc -l`); true pinned-tool run = 23 lines (re-run above, exit 0). The receipt is
truthful but partial; a reader can verify the trailer line and the two shown CASE lines only.

**[INFO] authoring.stdout vs authoring-receipts.json are two generations of one harness.**
`authoring.stdout` shows `ho-kill-vector-setup-threshold` as `[false,"vector"]`,
`as_expected=false`, trailer `SEALED: kill=8 accept=6 all_as_expected=False`; the JSON shows
the same copy `[true,"vector"]`, `as_expected=true`. Lesson
`corpus/lessons/round-34.md` (Mistakes 1) documents this as the first-generation catch
(witness `[2,2,0,…]` ties under `nsetup -gt 1`; fix `[2,0,…]`), and the sealed copy on disk
carries exactly the fixed vector `[2,0,0,0,0,0,0,0,0]`. Generation-2 is corroborated by the
deciding run (`ho_invalid=0` requires every sealed witness true) and by my re-derivation
(`(True,'vector')` + `KILL` byte-match). Within the dev dir alone the pair reads as
contradictory; the stdout is unlabeled first-generation output.

**[INFO] Gate branch coverage.** The 8 probes do not exercise two `ho_witness_ok` branches:
head-kind with *unchanged* head → `(False,'head')`, and head/other kind missing `vector` →
`(False,'no-witness')`. Not an inconsistency ("exactly the set-aware semantics" is satisfied);
noted for completeness.

## Corroboration of the deciding run (no override)

`c1-deciding-run.exit` = 0; `c1-deciding-run.stdout` = the claimed `C1_R33 … C1_R33_PASS=true`
line verbatim (grep -F hits in `SCORECARD.md:1643`; LOG quotes it wrapped across lines — a
formatting wrap, not a mismatch); stderr empty. `controls-receipt.json`: 4 controls
(CtlDoNothing 0/18+8/8, CtlAlwaysPass 0/18+8/8, CtlAlwaysFail 18/18+0/8, CtlShaOnly 18/18+1/8),
all `predicate_pass=false`, `all_false=true`, `counter_sha256` = the pinned counter bytes.
Nothing here contradicts the measurement.

## Residual risk / verification gaps

- Probe and authoring generator scripts were never committed; only the verdict strings are
  reproducible (my probe inputs are faithful reconstructions, disclosed above).
- 13 of 14 `tool` verdict cells in authoring-receipts.json were not independently re-scored by
  this seat (the deciding run already scored all 14 through the same code path; one cell was
  re-scored byte-identically).
- `elapsed=109.0s` is unreproducible by construction (wall clock).

## Tooling

No installs or upgrades needed (bwrap 0.13.1 already present). All writes confined to
`/fast/scratch/hyaku/tameshi-r34-seats/ReviewDevReceipts/` + this report; lane untouched.
