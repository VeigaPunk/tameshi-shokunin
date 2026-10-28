# T56W2Read11 — cold read of `### Round-13 gate/probe registry`

- **Heading:** `### Round-13 gate/probe registry`
- **cand:** `c0137451f5b7f22d65f748fc69f1b181f55e1378` (C0)
- **section_sha256:** `896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d`
- **Section span at C0:** lines **1590–1605** (recomputed at C0; at base it sat at 1577–1592)
- **Verdict:** `verified-record` (no findings)
- **Machine-readable:** `.ufo/waves/round-56/w2/T56W2Read11.json`
- **Receipts:** `.ufo/waves/round-56/w2/T56W2Read11-receipts/` (7 files)

## How the section hash was computed

The FROZEN round-18 sectionize was used unmodified — never reimplemented. `.ufo/evidence/round-18/measure.py`
was loaded with `importlib`, the blob was taken with
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md`,
and `m.sectionize(raw)` was applied:

```
total sections at C0: 64
heading: ### Round-13 gate/probe registry
start: 1590 end: 1605
section_sha256: 896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d
```

All 64 headings at C0 are distinct and this heading maps to exactly one section, so the binder's
`HEADING_AMBIGUOUS` refusal cannot fire on this report.

## Commands run

Every command the section tells a reader to run was executed in a scratch clone at C0
(`git clone --shared` of the lane, `git -C <clone> checkout --detach c0137451f5b7f22d65f748fc69f1b181f55e1378`),
and each was additionally re-run against the real lane root where the claim was read-only.

```
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin
python3 tools/pin-disposition.py --selftest
python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json
python3 tools/witness-metadata.py --selftest
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /nonexistent-root
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/nope.json --root /home/vgpnk/Projects/shokunin
TMPDIR=/nonexistent-tmpdir-xyz python3 tools/pin-disposition.py --selftest
python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/nope.json
python3 tools/witness-metadata.py
python3 tools/registry-check.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --only pin-disposition-read
python3 tools/registry-check.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --only witness-metadata-check
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Full transcripts: `T56W2Read11-receipts/01`…`07`.

## The section as read at C0

A two-row registry table (Name / Kind / Entry command / Verdict map / Self-test command / Pinned values /
Write scope / Owner), followed by four prose paragraphs: the "no registry row changes rank, SHONEN
authority, or the six recorded cases" sentence with its seventh-case pointer, the producer-SHA sentence,
the "no old evidence hash is regenerated" sentence, and the PIT source clarification.

## What was verified

**Row 1 — six-leg content disposition (probe).**
The entry command runs and exits 0 over the live fleet root (`status ok`, counts `legs=6 unchanged=1
changed=5 unavailable=0`). Its verdict map `0 observations, including changed/unavailable; 2 invalid
input/could-not-evaluate; selftest 1 failed` was exercised arm by arm:

| arm | command | result |
|---|---|---|
| 0, changed legs | entry command over the real fleet root | exit 0, `changed: 5` |
| 0, unavailable legs | entry command over a fake root whose sibling dirs are empty | exit 0, `unavailable: 6`, reason `repo_not_git` |
| 2 invalid usage | `python3 tools/pin-disposition.py` | exit 2, `invalid_usage` |
| 2 invalid manifest | `--manifest .ufo/evidence/round-13/nope.json` | exit 2, `invalid_manifest` |
| 2 invalid root | `--root /nonexistent-root` | exit 2, `invalid_root` |
| selftest 1 failed | one selftest expectation mutated 6→5 in a **throwaway clone**, never in the lane | `SELFTEST: FAIL (13/19 failed…)`, exit 1 |

The self-test command runs clean: `SELFTEST: PASS (19/19)`, exit 0.

Pinned values hold: `.ufo/evidence/round-13/pin-manifest.json` exists at C0; the tool's `CANONICAL_LEGS`
matches the manifest's six legs exactly in order and in `(repo, path)`; the selftest case labels are literal
strings in the tool source. The tool's self-reported `tool_sha256` (`c917bc41c3f4…`) equals the live file's
sha256 and is byte-identical at base `981c5e8` — the probe was not rewritten by this round.

Write scope holds: normal mode opens files only with `O_RDONLY` and runs only read-only git
(`rev-parse`, `cat-file`, `symbolic-ref`, `show-ref`, `for-each-ref`). Running it against the live fleet
root left every sibling repo's file mtimes untouched and the lane's `git status` clean. The self-test builds
isolated temp repos under `TMPDIR` and removes them on PASS (0 temp dirs left).

**Row 2 — exposed witness provenance companion (gate).**
The entry command runs and exits 0: `WITNESS_METADATA: metadata_consistent reason=ok exit=0
inputs=summary,declaration,declared,rerun_summary`. Its verdict map `0 metadata_consistent/clean;
1 metadata_inconsistent/failed; 2 input_unavailable or snapshot_tampered/could-not-evaluate, including usage`
was exercised arm by arm:

| arm | command | result |
|---|---|---|
| 0 | entry command | exit 0, `metadata_consistent` |
| 1 | companion `declaration.kind` tampered in a **throwaway clone** | exit 1, `metadata_inconsistent / normalized_kind_mismatch` |
| 2 input_unavailable | `--companion .ufo/evidence/round-13/nope.json` | exit 2, `companion_missing` |
| 2 usage | `python3 tools/witness-metadata.py` (no mode) | exit 2, argparse usage error |

`snapshot_tampered → exit 2` is covered by the tool's own selftest cases (`tamper-rerun-red`,
`tamper-declaration-red` observed `exit=2`). The self-test command runs clean: `SELFTEST: PASS 39/39`, exit 0.

Pinned values hold. The four frozen round-12 inputs exist at C0 with exactly the digests the tool pins as
literals:

```
.ufo/evidence/round-12/BashWitness/summary.json                       acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9
.ufo/evidence/round-12/BashWitness/declaration.json                   e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901
.ufo/evidence/round-12/BashWitness/declared.tsv                       0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3
.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json 6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0
```

`EXPECTED_KIND`, `EXPECTED_DISCLOSURE` and `EXPECTED_DISCLOSURE_SHA256` are literals in the tool; the
companion's expected verdict (`metadata_consistent` / exit 0) is checked by the tool.

The negative claim — "not `.ufo/evidence/round-13/expected.json`, which this gate never reads" — was confirmed
**two ways**: `expected.json` and `round-13/expected` occur **zero** times in `tools/witness-metadata.py`, and
the gate's verdict and exit code are **unchanged** when that file is deleted from a clone copy (exit 0
`metadata_consistent` either way). The file does exist at C0 (2943 bytes), so the negative claim is
meaningful rather than vacuous.

Write scope holds: `--check` performs no write and reads only the pinned lane files; the only `subprocess`
call in the tool is inside the self-test. The self-test creates exactly one temp tree under `TMPDIR`
(`tempfile.mkdtemp` honours `TMPDIR`) and removes it in a `finally` block — 0 temp dirs left after a PASS.

**Prose.**
- "the six recorded cases at this write" — the six ledger rows in
  `corpus/knowledge/fleet-kill-rate-ledger.md` are byte-identical between base `981c5e8` and C0;
  `SHONEN.md` is byte-identical between base and C0; the four `tools/registry.json` rows for these two
  tools are byte-identical between base and C0. No registry row changed the ledger, SHONEN or the case set.
- "The historical summary's producer SHA names the producer that actually ran, not the repaired current
  producer." — the companion's `producer.sha256` is `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`,
  identical to `summary.json`'s `tool.sha256`, and that digest matches `tools/bash-witness-study.py` at commit
  `9df9212` (the historical producer). The live file at C0 hashes to
  `f2bb50c77a6b6ffc53fd4e31d06c729f9cface7c1684f232c060f6a4978bf261` — the repaired current producer, a
  different digest. Holds.
- "No old evidence hash is regenerated" — corroborated: the four frozen round-12 evidence files still hash to
  the digests pinned in the tool at C0, which is why the gate exits 0 rather than reporting a digest mismatch.
- PIT source clarification — holds against `corpus/knowledge/incremental-pin-disposition.md:346-350`
  ("S048 supersedes S047's object-specific paraphrase … The supported operational distinction is item4
  **prioritisation, not a reuse skip**; no pronoun referent is resolved here") and
  `corpus/lessons/round-13-verifier-spotcheck.md:149` ("No pronoun resolution or new URL is claimed").
- The pointer `## Seventh recorded case and full-page cold-read — round 16` resolves at C0 line 1797.

**Registry replay.** `registry-check` holds all four rows for these two tools:
`pin-disposition-read`, `pin-disposition-selftest`, `witness-metadata-check`, `witness-metadata-selftest`
— each `expect=0 got=0 held`, `held=1/1`, exit 0.

**No contradiction with other sections.** `SKILL.md:1896` (round-17 registry) says the pin-disposition row is
"as the round-13 row, plus exit 2 could-not-evaluate when TMPDIR is set and unusable (round 54)", and
`SKILL.md:2194/2210` (round-26 registry) restate both rows with the same exit classes — those rows explicitly
extend this section's rows rather than contradict them. The round-54 arm was confirmed empirically:
`TMPDIR=/nonexistent-tmpdir-xyz python3 tools/pin-disposition.py --selftest` prints
`could-not-evaluate: … TMPDIR is not a usable directory` and exits 2.

## Findings

**None.** Every command the section names runs, every pointer resolves, every claim is true of the tree at
C0, and no other section contradicts this one. Verdict `verified-record`.

## Notes (improvements, stale-but-true, style — no text edit made here)

1. **STALE — the seventh-case parenthetical undercounts.** "a seventh case is recorded since round 16" is
   literally true (the heading exists at C0 line 1797) but understates the tree at C0: `SKILL.md:961` and
   `:1425` record **nine** cases since round 26 and **ten** since round 51. A reader acting on this section
   alone would undercount the recorded cases. Deferred to round 57 by the L1.
2. **DANGLING TERM — "rank" resolves nowhere (already routed, not re-raised as a finding).**
   "No registry row changes rank, SHONEN authority, or the six recorded cases" uses the word *rank*, which
   resolves nowhere in the live lane: `tools/registry.json` has no `rank` key in **any** commit, and
   `SHONEN.md` and `corpus/` never use it. The claim is vacuous rather than false, so it is filed as a note
   and left to the existing route — this is exactly routed defect **R49.3** in `corpus/routed-defects.json`
   (status `open`, seat `T50Disp49`), which quotes this sentence and records that the three sentences were
   byte-unchanged at base and routed rather than edited.
3. **CROSS-SECTION OBSERVATION (outside this section; for L1 awareness only).** `SKILL.md:2210` says the
   witness-metadata self-test "writes one isolated fixture tree under TMPDIR".
   `tools/witness-metadata.py` uses `tempfile.mkdtemp` without the strict scratch-root helper, so with a
   set-but-unusable `TMPDIR`, Python's `tempfile.gettempdir()` falls back to `/tmp` silently and the
   self-test still exits 0 (measured: `gettempdir() → /tmp` with `TMPDIR=/nonexistent-tmpdir-xyz`;
   `SELFTEST: PASS 39/39`, exit 0). The round-55 scratch-root contract (CR47) treats a silent `/tmp` fallback
   as a deviation. This is the round-26 registry row's claim, not this section's — this section says only
   "selftest isolated temp trees only", which holds.
4. **CENSUS (lane-level).** `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin tameshi` exits **0** (16 W-codes, 0 E-codes). The row count at C0 is **142**,
   not the 141 the assignment states: base `981c5e8` carries 140 rows and C0 adds **two** (`S281` and `S282`),
   so 140 + 2 = 142. The exit-0 requirement is met; the "141 / one new row" figure in the dispatch text is
   stale relative to the C0 commit (whose own message reads "SOURCES S281-S282").

## Validator proof (this seat passes)

The frozen round-56 reader validator (`.ufo/waves/round-56/validate-readers.py`) reads reports from the
**committed** tree (`git ls-tree` at `--rev`), so this report was committed in a **throwaway scratch clone**
(C0 plus one commit adding only `T56W2Read11.json` and `T56W2Read11.md` — the lane was never committed to by
this seat) and the validator was run there:

```
WARN READER_FINDINGS_EMPTY path=.ufo/waves/round-56/w2/T56W2Read11.json
EXPLAIN PASS '### Round-13 gate/probe registry' sha=896722c49418
READERS_R56: rev=515bf4fe3e37 c0=c0137451f5b7 r18=7ca87a7c9819 headings=18 passed=1/18 failed=17 refusals=17 warn=1 xrev=0
```

The seat **passes**: `cand` matches C0, `section_sha256` matches the C0 sectionize digest, `findings` is a
list, `commands` is a non-empty list of strings, and the sibling `.md` names the heading and runs a listed
command verbatim. The only line naming this seat is `WARN READER_FINDINGS_EMPTY`, which the validator raises
(line 322) for **any** clean read with an empty findings list — a warning, not a refusal, and the expected
state for `verdict=verified-record`. The other 17 headings `FAIL` with `READER_MISSING` because no other
wave-2 seat has committed yet; this seat contributes 1/18.

> **L1 action required.** This report and its `.md` are on disk but **uncommitted** (the lane working tree shows
> only `?? .ufo/waves/round-56/`). The round-55 binder refuses a reader report that is not committed, and
> `validate-readers.py` only sees committed reports — so the L1 must commit
> `.ufo/waves/round-56/w2/T56W2Read11.json` and `.ufo/waves/round-56/w2/T56W2Read11.md` for this seat to count.

## Tooling

No tool was installed, upgraded or removed by this seat (no `pacman`, `uv`, `npm` or `cargo` transaction was
run, consistent with the host-wide pacman pause). Versions used, all preinstalled: Python 3.14.8,
git 2.56.0, bash 5.3.20(1)-release, gawk 5.4.1 (see `T56W2Read11-receipts/06-tool-versions.txt`).

## Scope discipline

`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**` and everything under `.ufo/evidence/round-56/`
were **not** modified. The only files written are this report, its `.json`, and the
`T56W2Read11-receipts/` directory. All mutation experiments (the pin-disposition selftest expectation
6→5 and the companion `declaration.kind` tamper) were performed in a throwaway clone under
`$HYAKU_SCRATCH/tameshi-r56/T56W2Read11/clone2`, never in the lane; no mutating git or jj command was run
anywhere, and the only git commands in the clone were read-only.
