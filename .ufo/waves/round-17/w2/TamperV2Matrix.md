# TamperV2Matrix — v2 disposition gate, 17/17 tamper rows at `eb7838b`

Seat: `TameshiR17.TamperV2Matrix-2` (leaf; no dispatch). Read revision:
`eb7838b16490ca7ba17ea3242ade76a61f744af2` (SKILL.md sha256
`b1bd20aee58a0bd241e257f69e3610f3b8c2b805b2ebbb18f48b8e3184bf9d09`).
Gate under test: `tools/evidence-disposition.py`, reported `tool_sha256`
`f8f05c7aa601cf0b6f0907cc1ead2fc01acaad6a3c19e81888c084a969583e27`
in the baseline and final payloads (the tool file was never edited during the
matrix). All execution in a fleet-mirror clone; the live lane was never
written except this file.

## 1. Setup and baseline

```
W=$(mktemp -d /tmp/tameshi-r17w2-TamperV2Matrix-XXXXXX); mkdir $W/fleet
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" $W/fleet/
done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2
cd $W/fleet/tameshi-shokunin
```

- HEAD == `eb7838b16490ca7ba17ea3242ade76a61f744af2`; `git status --porcelain` empty.
- 13 expected inputs are the `inputs{}` block at
  `.ufo/evidence/round-13/expected.json:4-17` (9 evidence files + 4 `tools/*`
  files).
- 4 dispositions pins are `inputs{}` at
  `.ufo/evidence/round-17/dispositions.json:5-10`.
- 2 waivers (`tools/mutate-and-run.sh`, `tools/pin-disposition.py`) at
  `.ufo/evidence/round-17/dispositions.json:11-19`, both `rev =
  4acc607dfd79f19d508bd50cdd06b77269fccd1d`; the rev blobs hash to the pins
  (`75ed934d…` / `29725397…`, verified with `git cat-file -p`).

Baseline:

```
python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-17/dispositions.json --json
```

exit 0; `"status": "clean"`, `"counts": {"effective": 11, "expected_checks":
12, "failed": 0, "findings": 0, "passed": 11, "superseded": 1}`,
`expected_inputs_verified` has 13 entries, `inputs_verified` has 4.

## 2. Required matrix — one byte flipped per target

Driver: `python3 /tmp/tameshi-r17w2-TamperV2Matrix-8T3d7a/matrix.py`
(scratch; flips `byte[len//2] ^= 0x01`, runs the gate, parses the finding id,
restores with `git checkout -- <path>`, asserts the sha256 is restored, and
re-runs the gate asserting exit 0). Terminal line:

```
ROWS=34 MISMATCHES=0 FINAL_EXIT=0 GIT_DIRTY='' ; SCRIPT_EXIT=0   (4.52 s)
```

| target (kind) | offset | byte | exit | finding id | JSON parses | restore gate exit |
|---|---|---|---|---|---|---|
| pin `.ufo/evidence/round-13/expected.json` | 1471 | `0x62`→`0x63` | 2 | `input_digest_mismatch` | valid | 0 |
| pin `.ufo/evidence/round-13/producer-oracle-repair.json` | 3069 | `0x63`→`0x62` | 2 | `input_digest_mismatch` | valid | 0 |
| pin `.ufo/evidence/round-13/verification.json` | 21325 | `0x20`→`0x21` | 2 | `input_digest_mismatch` | valid | 0 |
| pin `.ufo/evidence/round-14/dispositions.json` | 1651 | `0x69`→`0x68` | 2 | `input_digest_mismatch` | valid | 0 |
| expected `.ufo/evidence/round-12/BashWitness/declaration.json` | 1514 | `0x61`→`0x60` | 2 | `expected_input_digest_mismatch` | valid | 0 |
| expected `.ufo/evidence/round-12/BashWitness/declared.tsv` | 2152 | `0x3a`→`0x3b` | 2 | `expected_input_digest_mismatch` | — | 0 |
| expected `.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json` | 9460 | `0x34`→`0x35` | 2 | `expected_input_digest_mismatch` | valid | 0 |
| expected `.ufo/evidence/round-12/BashWitness/summary.json` | 9349 | `0x5f`→`0x5e` | 2 | `expected_input_digest_mismatch` | valid | 0 |
| expected `.ufo/evidence/round-13/pin-manifest.json` | 1333 | `0x72`→`0x73` | 2 | `expected_input_digest_mismatch` | valid | 0 |
| expected `.ufo/evidence/round-13/producer-before.py` | 37817 | `0x5f`→`0x5e` | 2 | `expected_input_digest_mismatch` | — | 0 |
| expected `.ufo/evidence/round-13/producer-oracle.py` | 357 | `0x65`→`0x64` | 2 | `expected_input_digest_mismatch` | — | 0 |
| expected `.ufo/evidence/round-13/witness-metadata-old-null.json` | 1724 | `0x22`→`0x23` | 2 | `expected_input_digest_mismatch` | **invalid** | 0 |
| expected `.ufo/evidence/round-13/witness-metadata.json` | 1750 | `0x20`→`0x21` | 2 | `expected_input_digest_mismatch` | **invalid** | 0 |
| expected `tools/bash-witness-study.py` | 37807 | `0x20`→`0x21` | 2 | `expected_input_digest_mismatch` | — | 0 |
| expected `tools/mutate-and-run.sh` (waived) | 46105 | `0x73`→`0x72` | 2 | `historical_input_uncommitted` | — | 0 |
| expected `tools/pin-disposition.py` (waived) | 29647 | `0x75`→`0x74` | 2 | `historical_input_uncommitted` | — | 0 |
| expected `tools/witness-metadata.py` | 24457 | `0x69`→`0x68` | 2 | `expected_input_digest_mismatch` | — | 0 |

Per-row identity of `observed`/`expects` in the detail messages was checked
against the recorded sha256 before/after for the 25 digest-bearing byte-flip
rows: 25 checked, 0 mismatches. The 2 waived-tool mid-flip rows report
`live bytes differ from HEAD` instead of a digest pair; their restore identity
was checked by sha256 + gate exit 0 the same way. Sample rows (abridged from the
driver's per-row stdout):

```
{"exit": 2, "ids": ["input_digest_mismatch"], "kind": "pin",
 "path": ".ufo/evidence/round-13/expected.json", "restore_exit": 0}
{"exit": 2, "ids": ["expected_input_digest_mismatch"], "kind": "expected_input",
 "path": "tools/bash-witness-study.py", "restore_exit": 0}
{"exit": 2, "ids": ["historical_input_uncommitted"], "kind": "expected_input",
 "path": "tools/mutate-and-run.sh", "restore_exit": 0}
```

Text mode is identical (one probe, `verification.json` flip):

```
EVIDENCE_DISPOSITION: could_not_evaluate exit=2 id=input_digest_mismatch
 detail=.ufo/evidence/round-13/verification.json: observed 3be0054f… expects a02718e9…
```

Mechanism, in evaluation order: pins are hashed first
(`tools/evidence-disposition.py:1493-1504`, `input_digest_mismatch`), then
waivers are classified before any live read of the waived paths
(`:1518-1532`; `check_historical_waiver` at `:510-541`, G2
`historical_input_uncommitted` for the observed worktree edit at `:538-540`),
then the 13 expected inputs are
hashed, waived ones from the rev blob (`:1533-1544`; `historical_blob` at
`:543`). Two mid-flips (`witness-metadata*.json`) destroyed JSON syntax and
were still reported as `expected_input_digest_mismatch` — detection is
integrity-first, not parse-dependent. All 17 restores re-ran clean at exit 0
with the original sha256 (script asserts, every row).

## 3. Additional tamper modes (17 more runs, all restored to 0)

| probe | rows | observed |
|---|---|---|
| one alnum→alnum byte that leaves the JSON valid (all 10 JSON pins/inputs) | 10 | exit 2, same id as its mid-flip row (`input_digest_mismatch` ×4, `expected_input_digest_mismatch` ×6) |
| waived tool, same flip **committed** (live == HEAD) | 2 | exit 0, `status clean` — the pin is the rev blob, so a committed third content is not a mismatch |
| waived tool reverted to the **old pin bytes** and committed | 2 | exit 2, `historical_input_unneeded` ("live bytes still equal the expected pin; the waiver is unnecessary") |
| pin + waived tool flipped together | 1 | exit 2, `input_digest_mismatch` (integrity-first wins) |
| waived tool + expected input flipped together | 1 | exit 2, `historical_input_uncommitted` (waiver check precedes expected loop) |
| two expected inputs flipped together | 1 | exit 2, `expected_input_digest_mismatch` (first sorted, deterministic) |

The committed-flip exit 0 is exactly the claimed contract ("for waived tools
only uncommitted edits give 2"); `check_historical_waiver` compares live bytes
to `HEAD:<path>` (`:510-541`), and the expected digest is read from the rev blob
(`:1533-1539`). The JSON output keeps this honest: the waived paths appear in
`expected_inputs_verified`, while `historical_text` prints
`HISTORICAL tools/mutate-and-run.sh rev=4acc607… sha256=75ed934d…` (same for
`pin-disposition.py`), so the bytes verified are identifiable as rev bytes, not
HEAD bytes.

## 4. Boundary probes (non-byte, outside the claimed matrix)

| probe | command result |
|---|---|
| pinned evidence replaced by a symlink (`pin-manifest.json` → other file) | exit 2, `path_rejected` (`safe_file` lstat symlink check, `:276-305`) |
| pinned evidence deleted (`producer-before.py`) | exit 2, `expected_input_missing` (`safe_file` FileNotFoundError raise, `:285`) |
| self-consistent rewrite of **one evidence document's pin chain** (`declaration.json` + its pin in `expected.json` + `expected.json` pin in the v2 manifest) | exit 2, `supersedes_mismatch` — the v1 manifest at `.ufo/evidence/round-14/dispositions.json:4-8` still pins the old `expected.json`, and G7 requires identical pins (`:1412-1431`) |
| coordinated rewrite of the whole chain (tampered `declaration.json` + updated `expected.json`, `round-14/dispositions.json`, `round-17/dispositions.json`) | **exit 0, `status clean`** (observed; see residual risk R2) |

Gate selftest at this rev: `python3 tools/evidence-disposition.py --selftest`
→ exit 0, `SELFTEST: PASS (56/56)` (includes `argv-never-executed PASS`).

## 5. Findings

**A. Agreement (no defect).** All 17 required rows behave exactly as claimed:
every one of the 13 expected inputs and all 4 dispositions pins exits 2, with
`input_digest_mismatch` for pins, `expected_input_digest_mismatch` for the 11
non-waived expected inputs (9 evidence files + `bash-witness-study.py` +
`witness-metadata.py`), and `historical_input_uncommitted` for the 2 waived
tools when the worktree edit is uncommitted. Restore then returns exit 0 every
time. The 10 semantically-plausible (JSON-valid) flips are detected identically,
so the gate is not relying on structural parse errors.

**B. Minor, outside the claim — SIGPIPE turns into a traceback and exit 1**
(`tools/evidence-disposition.py:2870-2875` catch-all re-enters
`emit_could_not_evaluate` at `:1351-1367`, which writes again to the closed
pipe). Repro:

```
python3 tools/evidence-disposition.py --root . --dispositions \
  .ufo/evidence/round-17/dispositions.json | head -1 >/dev/null
PIPESTATUS=1/0
```

`BrokenPipeError` traceback on stderr, process exit 1 — colliding with the
documented `exit 1 failed semantic expectation` (`:170`) and never reaching the
`could_not_evaluate` code 2. Non-blocking for the matrix (all tamper runs used
captured output and exited 2), but an operator piping to `head`/`grep -m1` sees a
false "failed" code and a stack trace.

**C. Residual risk R1 — waived tools are pinned at rev, not at HEAD.** By design
and as claimed, a committed third-content edit to `tools/mutate-and-run.sh` or
`tools/pin-disposition.py` does not fail the gate (observed exit 0). The guard
is "live == HEAD", not "live == old pin"; this is the documented v2 semantics
(`:41-46`, `:179-180`), so it is agreement, not a hole — but it means the
matrix's `historical_input_uncommitted` result for those two paths proves an
*uncommitted* edit only.

**D. Residual risk R2 — the v2 manifest is the unpinned trust root.** The
sha256 of `.ufo/evidence/round-17/dispositions.json` is
`55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f`; `git grep`
over the whole landing tree for that digest (and its 12-hex prefix) returns no
site. A one-document rewrite is caught by the supersedes lineage check, but a
rewrite coordinated across the four documents (evidence file, `expected.json`,
the v1 manifest, the v2 manifest) passes with exit 0 (observed). This is the
normal boundary of an in-tree manifest checker and is outside C1/C2; stated so
the L1 does not read "input-keyed" as "anchored outside the manifest".

## 6. Verification gaps

- No race/TOCTOU test was run; the single-read `O_NOFOLLOW` + lstat/fstat
  identity guard (`:310-341`) is source-read only here.
- Restore identity was confirmed by sha256 equality plus gate exit 0 after each
  of 34 runs; file modes were untouched (contents rewritten in place, restored
  from git).
- Committed-flip and chain-rewrite probes used `git add/commit/reset --hard`
  **inside the /tmp clone only**; the lane repo received no git writes.
- The chain-rewrite boundary was observed once per configuration, not replicated.
- No tools installed or upgraded (none needed).

## Verdict

**Holds** — every one of the 17 required byte flips at `eb7838b` exits 2 with
exactly the claimed finding id (`input_digest_mismatch` ×4 pins,
`expected_input_digest_mismatch` ×11, `historical_input_uncommitted` ×2 waived
worktree edits), every restore re-runs clean at exit 0, and the only defect
found is a non-blocking SIGPIPE traceback outside the claimed behavior.
