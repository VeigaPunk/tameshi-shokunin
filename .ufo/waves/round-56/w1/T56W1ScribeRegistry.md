# T56W1ScribeRegistry — the registry cell for `tools/receipt-revision-gate.py`

Opened 2026-10-28. No lane production file was written (`tools/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/` all clean at this seat's exit — `T56W1ScribeRegistry-receipts/lane-scope-and-needles.txt`). No frozen instrument under `.ufo/evidence/round-56/` was edited; the gate's bytes equal its `freeze.json` sha256 (`source-pointer-and-freeze.txt`). No tool was installed (nothing was needed; `/usr/bin/time` is absent on the host and Python's own timing was used instead).

The cell below is a **proposal**: this seat does not append it. The L1 appends it to `tools/registry.json` in C0.

## The cell — exact JSON object

Append as the last element of `rows` (index 56; the file is `json.dumps(..., indent=1)` and round-trips byte-identically under that format, so the diff is additive only).

```json
{
 "name": "receipt-revision-gate-selftest",
 "scratch_root": "Read-only on the lane: the receipt form `receipt-revision-gate.py --lane LANE --certified REV [--paths FILE] --receipt PATH:positive|verdict|control[:REGEX] ... [--json]` reads git objects only (rev-parse, merge-base, diff), clones nothing, writes nothing, stdlib only; `--selftest` is its only allocating mode - one fixture repo in a `tempfile.TemporaryDirectory(prefix='tameshi-r56-gate-')` under TMPDIR, removed on exit (0.4 s) - and with TMPDIR unusable it falls back to the platform default `/tmp` with no could-not-evaluate line and exit 0, so the round-55 scratch-root contract is NOT implemented by this frozen instrument (measured in round 56, reported not edited). Refusal codes, each a named refusal at exit 3: RECEIPT_MISSING, RECEIPT_EMPTY, RECEIPT_NOT_BLOB, RECEIPT_REV_ABSENT, RECEIPT_REV_AMBIGUOUS, RECEIPT_REV_UNRESOLVABLE, RECEIPT_REV_MISMATCH, RECEIPT_REV_CONTENT_DRIFT, RECEIPT_CONTROL_NOT_ANCESTOR, RECEIPT_DIGEST_MISMATCH, RECEIPT_REQUIRED_LINE_MISSING. Verdict line `GATE: receipts=N ok=N refused=N codes=<comma|none> verdict=PASS|REFUSED`; exit 0 iff PASS.",
 "kind": "selftest",
 "argv": [
  "python3",
  "tools/receipt-revision-gate.py",
  "--selftest"
 ],
 "expect": {
  "exit": 0,
  "stdout_contains": [
   "GATE_SELFTEST: 14/14 pass",
   "CASE content-drift-refused PASS",
   "CASE strict-mismatch-refused PASS",
   "CASE absent-refused PASS",
   "CASE ambiguous-refused PASS",
   "CASE unresolvable-refused PASS",
   "CASE control-not-ancestor-refused PASS",
   "CASE digest-mismatch-refused PASS",
   "CASE required-line-refused PASS",
   "CASE missing-refused PASS",
   "CASE empty-refused PASS",
   "CASE codes-closed PASS"
  ]
 },
 "timeout_s": 60,
 "source": "tools/receipt-revision-gate.py@c3e2ca9f020776b3d66c7af854fb82c834674fcf:10-29",
 "status": "active",
 "tags": [
  "new-r56"
 ]
}
```

`T56W1ScribeRegistry.json` in this directory is this same object, alone, for verbatim append.

## Why each key is what it is

**Key set — no new key name.** The registry schema (`tools/registry-check.py:181-299`, `registry_errors`) constrains `name`, `kind`, `argv`, `expect{exit,stdout_contains}`, `timeout_s`, `source`, `status`, `tags` and the optional booleans `external`/`discriminating`; it also admits the free-text `scratch_root` that two existing rows carry (`repeat-control-selftest`, `registry-check-selftest`). This row uses exactly that second set, in the same key order as those two rows. No tool in the lane reads a row's `scratch_root`: all 15 `scratch_root` occurrences in `tools/*.py` (7 files) are a tool's own `strict_scratch_root()` helper for its `mkdtemp`, never a registry-field read (`claims-sweep.txt`), so the field is prose and safe to carry the contract.

**The tool, its two modes, its eleven codes.** The selftest is the only hermetic mode, so the row is `kind: "selftest"` and `argv` runs it; the receipt form is named in the note. The refusal codes cannot go in `expect.stdout_contains`: a needle must appear literally in stdout (`registry-check.py:36-38`) and the selftest prints case names (`CASE content-drift-refused PASS`), never a code token. They cannot go in a new key. `scratch_root` is therefore the only field that can name them, and it names all eleven (the item asks six; the C2 docs arm reads `tools/registry.json` for `tools/receipt-revision-gate.py` and at least three code tokens — `.ufo/evidence/round-56/c2/measure.py:252-258` — so all eleven is also the robust count).

**Round-55's cell marker is not a round-56 requirement.** Round 55's counter counted the `scratch_root` cells that carried a GRAMMAR marker (`.ufo/evidence/round-55/c2/measure.py:26,246-250`); round 56's frozen counter reads neither a row `scratch_root` nor any marker (`grep` exit 1), and no lane document mandates the `Allocating modes` token (`grep -rn "Allocating modes" SKILL.md SCORECARD.md corpus/` exit 1). The cell still states "`--selftest` is its only allocating mode" in that same field, so a reader gets the fact without the retired marker.

**`source`.** `tools/receipt-revision-gate.py@c3e2ca9f020776b3d66c7af854fb82c834674fcf:10-29` resolves to the tool's own usage block: lines 10-13 name both modes, lines 15-23 the three roles, lines 25-29 the eleven codes (`source-pointer-and-freeze.txt`). The gate is in `freeze.json` (`1d80f8a6…fbd2`, matching the working tree), so this pointer cannot rot. No existing row sources a `tools/*.py` file (0 of 56); if the L1 prefers the doc form, `source` can be re-pointed to the `SKILL.md` `## Standing rules` line at C0 — that is a one-field change and the only field I would touch.

**`timeout_s: 60`.** Measured 0.38-0.55 s per run (`scratch-root-probe.json`); 60 s matches the two `scratch_root` rows.

**Twelve needles.** The required summary `GATE_SELFTEST: 14/14 pass` plus the ten `-refused` case lines and `codes-closed`: each refusal code in the note has a case in the suite that must print PASS, and `codes-closed` is the case asserting `len(CODES) == 11`. All twelve are literal substrings of the observed stdout, and the 473-byte stdout sits inside `registry-check`'s 4096-byte retained tail (`lane-scope-and-needles.txt`).

**The scratch/read-only note states a defect, because the tool has one.** `--selftest` allocates one `tempfile.TemporaryDirectory(prefix='tameshi-r56-gate-')`; with a usable `TMPDIR` the fixture is created there and removed on exit, and with `TMPDIR=/nonexistent/nope` the fixture is created under `/tmp` with exit 0 and an empty stderr — no could-not-evaluate line. That is not the round-55 scratch-root contract (`corpus/knowledge/scratch-root-contract.md`), and the instrument is frozen, so the note records the behaviour instead of asserting the contract (finding F1).

## Verification — commands and outcomes

| # | Command | Outcome |
|---|---|---|
| 1 | `python3 -c 'import json;json.load(open("<scratch>/registry-with-row.json"))'` | exit 0, `parsed rows=57` (`parse-exact-commands.txt`, `registry-parse.txt`) |
| 2 | every existing row re-parsed individually, and rows 0-55 compared canonically against the unedited file | `rows_parsed=57/57 bad=[] existing_rows_unchanged=True` (`rows-parse.txt`) |
| 3 | `registry_errors(json.load(<edited>))` via `importlib` on `tools/registry-check.py` | `errors=0`; baseline unedited registry also `0`; `name_ok=True kind_ok=True status_ok=True source_re=True` (`registry-schema-validate.txt`) |
| 4 | `python3 tools/registry-check.py --registry <edited> --root LANE --only receipt-revision-gate-selftest` | exit 0, `ROW receipt-revision-gate-selftest expect=0 got=0 held`, `REGISTRY_CHECK: held=1/1 superseded=0` (`registry-check-only.stdout`), 2.02 s |
| 5 | same with `--rev c3e2ca9f020776b3d66c7af854fb82c834674fcf` (hermetic clone, `non_hermetic_argv` check active) | exit 0, `held=1/1`, empty stderr (`registry-check-rev.stdout`), 2.38 s |
| 6 | gate `--selftest` under `TMPDIR=<scratch>` and under `TMPDIR=/nonexistent/nope`, polling for the fixture dir | exit 0 both, `GATE_SELFTEST: 14/14 pass` both; fixture seen in the scratch root in the first and in `/tmp` in the second; nothing left behind (`scratch-root-probe.json`, `gate-selftest.stdout`, `gate-selftest-bad-tmpdir.stdout`) |
| 7 | receipt form on the three real red-before receipts | `red54 → RECEIPT_REV_CONTENT_DRIFT` (drift on `.ufo/evidence/round-21/coldread/ledger.json` + 5 wave paths), `red54b → RECEIPT_REV_UNRESOLVABLE` (`rev=7df0e0426c98`), `red55 → RECEIPT_REV_ABSENT`; all exit 3 (`gate-receipt-form-red.txt`) |
| 8 | receipt form on two scratch receipts (positive naming `c3e2ca9f…`, control set `981c5e8b…` + `c3e2ca9f…`) | `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS`, exit 0 both (`gate-receipt-form-accept.txt`) |
| 9 | `diff -u tools/registry.json <edited>` | 34 added lines, 1 replaced line (`  }` → `  },`); patch at `registry-row.patch` |

Runs 7 and 8 are the modes the note names, exercised end to end: the form refuses what it should and accepts a receipt bound to the certified revision. Run 8 uses scratch receipts because the round's own `control/controls-a.stdout` and `control/controls-b.stdout` do not exist yet (only `control/frozen-surface.paths` is committed); the C2 counter's arm 5 will produce them in a later wave.

## Findings

**F1 — the frozen gate does not implement the round-55 scratch-root contract.** The contract (`corpus/knowledge/scratch-root-contract.md`, round 55, implemented round 53) is `strict_scratch_root()`: `TMPDIR` set and usable is used, `TMPDIR` set and unusable is `could-not-evaluate` — "never a silent fallback to /tmp" (`tools/registry-check.py:761-772`); seven tools in `tools/` carry it. The gate does not: `tools/receipt-revision-gate.py:226` calls `tempfile.TemporaryDirectory(prefix='tameshi-r56-gate-')` with no `dir=`, so with `TMPDIR=/nonexistent/nope` the fixture is built under `/tmp`, the suite prints `GATE_SELFTEST: 14/14 pass`, stderr is empty and the exit is 0; `tempfile.gettempdir()` returns `/tmp` for the same value. Evidence: `scratch-root-probe.json`. Not fixed — the instrument is frozen; the row's note states the behaviour so the registry does not assert a contract the tool breaks.

**F2 — the codes are prose-only in this schema.** The registry has no structured field for a tool's refusal codes, so the docs arm (`c2/measure.py:252-258`) can only count literal occurrences in the file text. Anyone who later trims `scratch_root` to "read-only, no scratch" silently drops the arm from 11 hits to 0 and fails `docs`. If the L1 shortens the note, the code list must survive somewhere in the registry text.

**F3 — `source` convention gap.** All 56 existing rows source a document (`SKILL.md`, `SCORECARD.md`, `corpus/lessons/*`, `.ufo/waves/*`); none sources a tool. My pointer is the tool's own usage/codes block at the freeze revision — resolvable and non-rotting — but it is a new provenance shape. The alternative (`SKILL.md@<c0>:<line>`) needs C0's line number, which this seat cannot know.

**No other defect found in the cell's surface.** The sweep: schema validator (run 3), full-row grading live and at the freeze rev (runs 4-5), needle literals against observed stdout (`lane-scope-and-needles.txt`), source pointer resolution and freeze sha256 (`source-pointer-and-freeze.txt`), both modes exercised (runs 6-8), and the lane tree clean of this seat's writes.

## Out of scope here (owned elsewhere)

- Appending the row to `tools/registry.json` — L1, in C0.
- The `corpus/QUALITY.md` criterion, `corpus/knowledge/receipt-revision-binding.md`, the `SOURCES.md` row and the `SKILL.md` `## Standing rules` rule — other seats; the C2 docs arm needs all four plus this cell.
- Any edit to the gate or to `.ufo/evidence/round-56/**` — frozen.
- Census (`scripts/sources-census.sh validate`) and the C1 heading drift map — not this seat's item.

## Artifacts

- `.ufo/waves/round-56/w1/T56W1ScribeRegistry.md` (this report)
- `.ufo/waves/round-56/w1/T56W1ScribeRegistry.json` (the cell alone)
- `.ufo/waves/round-56/w1/T56W1ScribeRegistry-receipts/` — `row.json`, `registry-row.patch`, `parse-exact-commands.txt`, `registry-parse.txt`, `rows-parse.txt`, `registry-schema-validate.txt`, `registry-check-only.stdout|.stderr`, `registry-check-rev.stdout|.stderr`, `gate-selftest.stdout|.stderr`, `gate-selftest-bad-tmpdir.stdout|.stderr`, `scratch-root-probe.json`, `gate-receipt-form-red.txt`, `gate-receipt-form-accept.txt`, `source-pointer-and-freeze.txt`, `lane-scope-and-needles.txt`

## Limits

- The row is validated against the current schema and grader, not against C0's tree: if another seat's C0 edits touch `tools/registry.json` first, the append point moves (the row itself is position-independent).
- Run 4 executed the row live in the lane root; the row writes nothing outside `TMPDIR` (run 6), and `git status` over `tools/ SKILL.md SCORECARD.md LOG.md corpus/` stayed empty.
- The scratch-root finding is measured for the selftest mode only; the receipt form writes nothing at all and so has no scratch root to test.
- Peer `C2Floor` sent the single word `DISALLOWED` mid-seat, with no code, command, scope or rationale. Nothing in the round-56 contract, the frozen counters or this item identifies what it refers to, so no change was made on that basis; the cell still meets every requirement the item and `c2/measure.py:252-258` state. Flagged for the L1 in case it is a real steering signal from another seat.
