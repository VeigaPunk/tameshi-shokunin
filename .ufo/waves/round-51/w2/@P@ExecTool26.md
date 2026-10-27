# T51W2ExecTool26 — C3 registry row falsification: `tools/witness-metadata.py`

Seat: executor, round-51 wave 2 (falsify). Item: independently audit the round-51 C3 registry row for
`tools/witness-metadata.py` at content candidate `6d8c11e378aa90b12650808e1b79270742935f15`; run the row's
exact backticked self-test and the `--r51-no-such-flag` usage probe from a `git clone --shared` at CAND with a
scratch TMPDIR and stdin `/dev/null`; check every row field against source; report mismatches. No source was
written, no row was repaired.

**Verdict: the row survives falsification on every field the C3 predicate tests, with two precision notes and
one disclosure (below). No mismatch that makes the row false was found. This tool is *not* the round's known C3
blocker.**

Read-only on the lane. All experiments ran under
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool26/` (a `git clone --shared` of the lane, `checkout --detach
6d8c11e3`, `git rev-parse --show-toplevel` printed the clone dir before anything ran), deleted before yield. No
tools installed, no pacman, no `~/.local/bin` change, no fleet-root file touched. Raw receipts:
`.ufo/waves/round-51/w2/@P@ExecTool26/` (`summary.txt` is the index). This report is also written byte-identically
to `.ufo/waves/round-51/w2/@P@ExecTool26.md` (the seat item's `@P@` path).

## 0. Reader statement (for the L1's re-key)

I read `#### Gate/probe registry — round 51` (SKILL.md:2138-2171 at CAND) and verified its claims about the
row rather than restating them. The row under audit is SKILL.md:2167 (sha256 of the line, newline stripped:
`61d923089c2c84b55f698f0eaff184d12f728e3ff6f172d26cbf2a073534be2e`); the tool is `tools/witness-metadata.py` at
CAND (blob `b38bec3cda5552597839cfaff5cad2bf1cdb7135`, sha256
`df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4`, 48 914 B, 1290 lines, mode 100755). Every
field was checked against that tool's bytes and against executed output. Seat T51W2ExecTool26 is available as the
named reader for this row. The older `### Gate/probe registry` (SKILL.md:1499-1516) holds only the round-12 rows
(repeat-control, bash-witness-study) and no witness-metadata row; the round-13..round-26 headings
(`### Round-13 gate/probe registry`, …) are *not* scanned by the C3 counter's heading regex
`^#{2,4} Gate/probe registry` (the leading "Round-NN " breaks the match — measured, see §7), so the round-13
witness-metadata row at SKILL.md:1553 is outside the counter's set. This report covers SKILL.md:2167 only.

The row under audit, verbatim:

```
| witness metadata companion | gate | `python3 tools/witness-metadata.py --check --lane-root DIR --companion FILE` | 0 clean; 1 failed; 2 could-not-evaluate (input unavailable, snapshot tampered, usage) | `python3 tools/witness-metadata.py --selftest` → SELFTEST: PASS 39/39 | `.ufo/evidence/round-13/witness-metadata.json`, `.ufo/evidence/round-12/BashWitness/summary.json`, `.ufo/evidence/round-12/BashWitness/declaration.json`, `.ufo/evidence/round-12/BashWitness/declared.tsv`, `.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json` | `--check` writes nothing and reads only the pinned lane files; selftest writes one isolated fixture tree under TMPDIR and removes it in a finally block | tameshi |
```

## 1. The row's exact backticked self-test, run as the counter runs it

`python3 tools/witness-metadata.py --selftest`, from the `--shared` clone at CAND, `TMPDIR` = scratch,
stdin `/dev/null`:

| measurement | value |
|---|---|
| exit | **0** |
| last non-empty stdout line | `SELFTEST: PASS 39/39` |
| first token (the counter's "finding id") | `SELFTEST:` — present in the row's Self-test cell |
| stderr | empty (0 bytes) |
| wall time | 1 583 ms under counter-identical env; 2 013–2 157 ms over 5 further runs |
| stdout shape | 39 `SELFTEST_CASE …` lines + the tally line (40 lines) |

Receipts: `selftest.out`, `selftest.err`, `timings.txt`. The counter's own machinery reproduces this exactly:
importing `.ufo/evidence/round-51/c3/measure.py` and calling its `registry_rows` + `row_reason` + `run_row` on
this row returns `row_reason -> None` and `run_row -> (None, 'SELFTEST: PASS 39/39')` — i.e. the row is
structurally accepted *and* behaviourally green in the counter's own clone, cwd, TMPDIR and 900 s limit
(`counter-run-row.py`, `row-cells-at-cand.py`).

The "39" in the row's cell is truthful, not decorative: `SELFTEST_CASES` holds exactly 39 entries
(`"case"` count = 39) and the tool prints `total = len(SELFTEST_CASES)` (wm.py:1207).

## 2. The usage probe

`python3 tools/witness-metadata.py --r51-no-such-flag` (same clone, same limits):

| measurement | value |
|---|---|
| exit | **2** |
| stdout | empty (0 bytes) |
| stderr | argparse usage text; last line `witness-metadata.py: error: one of the arguments --check --selftest --emit is required` |
| wall time | 35 ms |

2 is declared in the row's Verdict map cell, so the counter's usage-code check passes
(`re.search(r'(?<![0-9])2(?![0-9])', vmap)` hits "2 could-not-evaluate"). Note *why* it is 2 and not 64:
argparse's default error exit is 2 and the tool uses no custom `exit` code (grep for `exit(` finds only
`sys.exit(main())`, wm.py:1290). The row is honest that usage shares code 2 with the tool's genuine
could-not-evaluate class; sibling rows in the same table use 64 for usage, this one cannot.
Receipt: `usage.out`, `usage.err`.

## 3. Row field-by-field against source

**Kind `gate` — correct.** PROTOCOL §Gate standard: "A tool that cannot fail is a probe." The tool can and does
fail. Measured on scratch copies of the clone:

| injected fault | result |
|---|---|
| companion re-serialized with `declaration.kind = "blind preregistration"` | exit **1**, `metadata_inconsistent`, reason `normalized_kind_mismatch` |
| one byte appended to the committed `summary.json` | exit **2**, `snapshot_tampered`, reason `summary_digest_mismatch` |
| committed companion deleted | exit **2**, `input_unavailable`, reason `companion_missing` |
| committed companion re-serialized with identical *content* but different *bytes* | exit **0**, `metadata_consistent` |

The last row is the interesting one and is treated in §5.

**Verdict map `0 clean; 1 failed; 2 could-not-evaluate (input unavailable, snapshot tampered, usage)` — complete.**
Exhaustive exit sweep of the tool at CAND (`exit-sweep.txt`):

```
no args                          exit=2 (argparse: one of --check --selftest --emit is required)
--help                           exit=0
--emit                           exit=0
--check (green)                  exit=0  metadata_consistent
--check --lane-root missing      exit=2  input_unavailable / lane_root_unavailable
--check --companion missing      exit=2  input_unavailable / companion_missing
--selftest                       exit=0  SELFTEST: PASS 39/39
--check --selftest (both)        exit=2  (argparse mutually-exclusive group)
--r51-no-such-flag               exit=2
--check --r51-no-such-flag       exit=2
--emit --json                    exit=0
```

The tool's reachable code set is exactly {0, 1, 2}; the source has no other exit (`_fail` is called only with 1 or
2 — wm.py:259-268, 14 call sites with `1`, 25 with `2`), and argparse's own error path is also 2. Every code the
tool can return is named in the row's map, so PROTOCOL's "every other code a gate exits … is declared" is
satisfied. The tool's docstring exit map (wm.py:31-34) is *narrower* than the row's: it names 2 as "input_unavailable
or snapshot_tampered" and omits usage; the row adds usage under 2, which matches the observed behaviour. The row
is the more complete of the two.

**Entry command `python3 tools/witness-metadata.py --check --lane-root DIR --companion FILE` — runnable and
meaningful.** Run verbatim at CAND: exit 0, `metadata_consistent`. Cross-rev run (lane root = the base commit
9962033's tree, companion = CAND's) also exits 0, because the four frozen inputs are byte-identical base→CAND and
the companion file is byte-identical base→CAND (measured: `SAME_AS_BASE` for all five pinned paths). The gate is
therefore rev-stable over the round's own span.

**Self-test command and its finding id — truthful.** See §1. The marker is the tool's own computed tally, not
author-chosen text: mutating the tool flips the last line to `SELFTEST: FAIL 27/39`, `FAIL 38/39`, `FAIL 34/39`
etc. (§6). One genericity note, not a defect: `SELFTEST:` is a marker shared with several other lane tools
(pin-disposition, repeat-control, registry-check, trace-inputs all print a `SELFTEST:`-prefixed last line), so
the counter's "finding id in the row cell" test is satisfied by a generic token for this row. The counter also
matches the row by the entry cell naming the tool, which is specific.

**Pinned values — the four frozen inputs are genuinely pinned and live; the companion is load-bearing but is
pinned by canonical-object equality, not by digest.** Per-pin liveness (`pin-liveness.txt`), each of the four
`PINNED_INPUTS`/`RERUN_SUMMARY` digests (wm.py:72-90, 127-132) was individually tampered by appending one byte:

```
summary.json            -> exit 2 snapshot_tampered reason=summary_digest_mismatch
declaration.json        -> exit 2 snapshot_tampered reason=declaration_digest_mismatch
declared.tsv            -> exit 2 snapshot_tampered reason=declared_digest_mismatch
rerun-.../summary.json  -> exit 2 snapshot_tampered reason=rerun_summary_digest_mismatch
```

Integrity is checked *before* any exit-1 comparison (wm.py:388-404 hash all four, then the semantic comparisons
begin at :407), which is the PROTOCOL ordering ("verifies those digests before comparing verdicts"). The tool's
own literal digests are load-bearing too: mutating the `summary.json` digest literal to `"0"*64` in the tool
makes the selftest exit 2 with `SELFTEST: SETUP_FAIL summary digest … != 0000…` (wm.py:1099-1108), i.e. the
selftest re-verifies the lane's frozen bytes before running any case.

The fifth pinned path, `.ufo/evidence/round-13/witness-metadata.json` (the companion), is a real input — delete it
→ exit 2, doctor it → exit 1 — but the tool does **not** digest-pin its bytes. It compares the *parsed object*
against `build_companion()` (wm.py:615-616, `if companion != build_companion(): _fail("companion_noncanonical", 1)`).
Measured consequence: a companion re-serialized from the same JSON content but with different bytes
(sha `72647dcb…` vs the committed `46328227…`) still exits 0 `metadata_consistent`. The byte-level anchor for the
companion lives in `.ufo/evidence/round-13/expected.json` (`…/witness-metadata.json: 46328227…`, plus the tool's
own sha `df339068…`) — a file the tool never reads and which the round-51 row's Pinned values cell does not
cite. Both expected.json pins still match the live bytes at CAND (measured).

This is the row's one substantive imprecision, and it is a **precision note, not a falsification**:

* **Precision note P1.** The round-51 Pinned values cell lists the companion file alongside the four digest-pinned
  inputs, which reads as "five digest-pinned inputs". Four are digest-pinned inside the tool; the companion is
  pinned by canonical-object equality inside the tool, and by digest only in `round-13/expected.json`, which the row
  does not cite. The two pinned mechanisms are not interchangeable: a byte-only drift of the companion (whitespace,
  key order) is accepted, and the committed companion is never byte-compared by the gate.
  For contrast, the superseded round-13 row (SKILL.md:1553, receipt `row-1553-round13.txt`) cited
  `.ufo/evidence/round-13/expected.json` as a pinned value — but the tool never reads that file (grep: no
  reference to `expected.json` anywhere in `tools/witness-metadata.py`), so *that* row's pinned claim was the
  inaccurate one. The round-51 row is the more accurate of the two; it simply trades a false file reference for a
  digest-vs-canonicality distinction it does not spell out.
* **Disclosure D1.** The C3 counter only requires that the pinned paths *exist* at REV (it does not check that the
  tool pins them by digest), and the predicate's own `cannot_see` clause already concedes that "the verdict map
  names every code the tool can exit with beyond 0, 1 and the usage code" is out of scope. P1 lives inside that
  conceded gap: the row's pinned-value description is true of the *paths*, and true of the tool's dependence on
  them, but it does not distinguish digest-pinned from canonically-compared.

**Write scope — accurate, with one conditional.** Measured with `strace -f -e trace=openat,creat,unlink,mkdir,rename`:

* `--check` performs **zero** write-mode opens anywhere in the lane; the only lane reads are the four pinned files,
  the companion, and the tool itself (`strace-check.txt`). It writes nothing. ✓
* `--selftest` writes only inside one `tempfile.mkdtemp(prefix="witness-metadata-selftest-")` tree under TMPDIR
  (wm.py:1122): the tree root plus per-case copies of the four pinned files and the companion
  (wm.py:936-946, 948-957). The tree is removed in the `finally` block (wm.py:1185-1186): TMPDIR is empty
  afterwards and `/tmp` has zero `witness-metadata-selftest-*` residue (`write-scope.txt`,
  `strace-selftest-writes.txt`). The lane tree is untouched: `git status --porcelain --untracked-files=all` in the
  clone is empty after the selftest, and no `__pycache__` is created.
* **Precision note P2.** "under TMPDIR" is conditional on TMPDIR being a usable directory. With
  `TMPDIR=/nonexistent-xyz` the stdlib `tempfile` falls back to `/tmp` and the tree lands at
  `/tmp/witness-metadata-selftest-200fick3` (measured, `strace-bad-tmpdir-fallback.txt`); the row's wording then
  overstates by one path. The C3 counter always sets a real TMPDIR, so this never fires under the counter. It is
  also the same stdlib-fallback pattern other lane rows rely on.
* **Precision note P3 (read scope, narrower than the tool).** "reads only the pinned lane files" holds for the
  default invocation, where the companion defaults to `lane_root/DEFAULT_COMPANION_REL` (wm.py:68, 1259-1264). But
  the row's *own entry command* exposes `--companion FILE`, and the tool explicitly permits a companion outside
  the lane (wm.py:373-375: "An explicit --companion may live outside the lane (direct old-null red probe)"): a
  companion in my scratch, outside the clone, yields exit 0 with `"companion_in_lane": false` in the `--json`
  output (wm.py:618-622). So the read scope is "the pinned lane files under `--lane-root`, plus the companion at
  `--companion`, which the caller may point outside the lane." The tool reports this honestly in its own output;
  the row does not.

**Owner `tameshi` — correct** (the lane's own registry home, owner column).

## 4. What the counter says about this row at CAND

I ran the frozen counter itself against CAND (read-only on the lane; its clone and work dir lived in my scratch):
`.ufo/evidence/round-51/c3/measure.py --lane <lane> --rev 6d8c11e3… --work <scratch> --explain`
(`c3-counter-explain.out`).

```
C3_TOOL tools/witness-metadata.py: covered line 2167 selftest exit=0 last=SELFTEST: PASS 39/39
C3_R51: rev=6d8c11e3… tools=30 rows=32 covered=29 missing=1 deleted=0 selftest_fail_rows=2 total=1 C3_R51_PASS=false
```

So the row is **covered** and contributes nothing to the round's C3 shortfall. The single missing tool is
`tools/round21-measure.py` (line 2157, `selftest-exit=1`) — the known clone-context blocker, whose selftest
shells out to `git -C <path> show <sha>:tools/mutate-and-run.sh` against a path absent from the counter's fresh
clone (I reproduced it: `subprocess.CalledProcessError … git … returned non-zero exit status 128`,
`/fast/scratch/…/tameshi-shokunin`). That is not my tool and not my row: `tools/witness-metadata.py`'s selftest has
**no** sibling-repo or sibling-path dependency (grep for fleet/sibling paths in the tool: none; the selftest
copies only the lane's own frozen files into a TMPDIR fixture), and it passes 39/39 from a fresh clone at CAND.
`tools/witness-metadata.py` is listed in the frozen 30 (`.ufo/evidence/round-51/c3/tools-base.json`) and is not
deleted at CAND.

Also measured, for the L1's benefit: the counter's heading regex `^#{2,4} Gate/probe registry` matches only
SKILL.md:1499 and SKILL.md:2138 in the whole file; the `### Round-13/14/15/16/17/18/20/21/26 gate/probe registry`
headings do not match because of the leading "Round-NN ". Hence 32 parsed 8-cell rows (2 from the round-12
table + 30 from the round-51 table), and the round-13 witness-metadata row at 1553 is invisible to the counter.
The tool's own entry command is still live and green (`--check --companion .ufo/evidence/round-13/witness-metadata.json`
→ exit 0), so the superseded row does not mislead a human reader into a false state.

## 5. Is the row's self-test a meaningful diagnostic, or author-chosen text?

I ran a 19-mutant battery against the tool (each mutant applied to a scratch copy of the clone) and asked whether
the row's two claims — "selftest exits 0 and prints `SELFTEST: PASS 39/39`" and "the tool is a gate that fails" —
would survive a weakened tool (`mutation-battery.txt`, `mutation-battery.py`):

| # | mutant | selftest | live `--check` |
|---|---|---|---|
| 1 | `build_companion` `purpose` text changed | PASS 39/39 (exit 0) | **exit 1** |
| 2 | `build_companion` `producer.source` changed | PASS 39/39 (exit 0) | **exit 1** |
| 3 | `build_companion` `historical_runner.source` changed | PASS 39/39 (exit 0) | **exit 1** |
| 4 | `scope.uncovered_null_observations[0].disposition` literal changed | PASS 39/39 (exit 0) | **exit 1** |
| 5 | `declaration.get("kind") != EXPECTED_KIND` check removed | PASS 39/39 (exit 0) | exit 0 |
| 6 | `build_companion` `measured_claim_unchanged` changed | FAIL 37/39 (exit 1) | exit 1 |
| 7 | `build_companion` `frozen_bytes_rewritten` changed | FAIL 37/39 (exit 1) | exit 1 |
| 8 | `EXPECTED_VERDICT_ID` literal changed | FAIL 38/39 (exit 1) | exit 1 |
| 9 | `kind_source` rule changed | FAIL 30/39 (exit 1) | exit 1 |
| 10 | `EXPECTED_KIND` trailing space | FAIL 27/39 (exit 1) | exit 1 |
| 11 | `EXPECTED_VERDICT_EXIT` 0→1 | FAIL 38/39 (exit 1) | exit 1 |
| 12 | `EXPECTED_DISCLOSURE` mutated | FAIL 27/39 (exit 1) | exit 1 |
| 13 | canonical `companion != build_companion()` check removed | FAIL 38/39 (exit 1) | exit 0 |
| 14 | companion digest-vs-literal check removed | FAIL 38/39 (exit 1) | exit 0 |
| 15 | input digest check removed | FAIL 34/39 (exit 1) | exit 0 |
| 16 | `comp_decl` normalized-kind check removed | FAIL 37/39 (exit 1) | exit 0 |
| 17 | `producer.checked_live` check removed | FAIL 38/39 (exit 1) | exit 0 |
| 18 | `PINNED_INPUTS` summary digest literal → `"0"*64` | SETUP_FAIL (exit 2) | exit 2 |
| 19 | `EXPECTED_DISCLOSURE` / `EXPECTED_VERDICT_EXIT` literals changed | FAIL (exit 1) | exit 1 |

Reading: the row's marker is computed, not decorative — **13 of the 19 mutants flip the selftest to
`FAIL n/39` (exit 1) and a 14th flips it to `SETUP_FAIL` (exit 2)**, so the last line is a live diagnostic and
the row's `SELFTEST: PASS 39/39` marker would not survive a weakened tool. The four "PASS 39/39 but exit 1"
mutants (#1–#4) are the *expected* shape for fields the selftest does not pin independently: the selftest builds
its expected companion with the same `build_companion()` it is testing, so a change to the builder stays
self-consistent and only the committed companion catches it. Mutant #5 is worth naming: removing the check
`declaration.get("kind") != EXPECTED_KIND` (wm.py:521-522) leaves both the selftest green and `--check` green —
that branch is unreachable-by-construction for the selftest, because the field lives inside the digest-pinned
`declaration.json`, so any change to it trips the digest check first (exit 2, `declaration_digest_mismatch`) and
the semantic branch can never be reached from a fixture. That is a redundant-by-construction defence, not a hole
in the row.

**Disclosure D2 (the one substantive finding of this seat).** The C3 counter's per-row test is *only* "the
self-test exits 0 and prints a finding id recorded in the row" plus "the usage exit is declared". A tool whose
selftest is self-referential can satisfy that test while the committed evidence it grades has drifted. For this
tool the drift is caught — but by the **entry command**, not by the self-test the row names: the four
`build_companion` prose/source-pointer fields above are unobservable to `--selftest` and observable only to
`--check` against the committed companion. Concretely: `build_companion`'s `purpose`,
`producer.source`, `historical_runner.source` and the `scope.uncovered_null_observations[0].disposition` literal
are compared against nothing in the selftest's 39 fixtures, and a re-serialization of the committed companion
(same content, different bytes) exits 0. So the row's self-test cell, read alone, is a weaker guarantee than the
row's other cells; the gate's strength lives in the `companion != build_companion()` canonical comparison and in
the four digest pins. This does not falsify any field of the row as written, and it does not move the counter's
verdict — but the C3 predicate's `cannot_see` clause ("that a row's kind, write scope and pinned-value description
are true of the tool") is exactly where D1/D2 live, and both should be visible to the L1 as disclosed data rather
than as a kill.

## 6. Findings summary

| # | kind | finding |
|---|---|---|
| — | **no falsification** | Every C3-tested field of SKILL.md:2167 is true at CAND: kind `gate` (the tool fails), verdict map complete over {0,1,2} with usage included under 2, self-test exits 0 printing `SELFTEST: PASS 39/39` with 39 real cases, usage probe exits 2 (declared), pinned paths all exist at REV and are load-bearing, write scope holds, owner `tameshi`. The counter covers this row: `covered line 2167`. |
| P1 | precision | Pinned values cell lists the companion among "pinned values"; the tool pins it by canonical-object equality (wm.py:615-616), not by digest — a byte-only drift of the companion exits 0. The byte anchor lives in `round-13/expected.json`, which the row does not cite (and which the tool never reads). |
| P2 | precision | "selftest writes one isolated fixture tree under TMPDIR" holds only when TMPDIR is a usable directory; with an unusable TMPDIR the stdlib falls back to `/tmp` (measured). The counter always sets a usable TMPDIR. |
| P3 | precision | "reads only the pinned lane files" does not describe the row's own entry command: `--companion FILE` may point outside the lane (the tool documents and reports this: `companion_in_lane: false`). |
| D1 | disclosure | The C3 counter checks pinned-path *existence*, not digest-pinning; the row's pinned description is true of the paths and of the tool's dependence on them but does not distinguish digest-pinned from canonically-compared. |
| D2 | disclosure | The selftest is partly self-referential (it builds its expected companion with the same `build_companion()` it tests): four `build_companion` prose/source-pointer fields are invisible to `--selftest` and caught only by `--check` against the committed companion. 11/15 mutants flip the selftest tally, so the marker is a live diagnostic, but the self-test cell alone understates the gate. |

Cross-references for the L1: the round's C3 shortfall at CAND is `tools/round21-measure.py` (row 2157), whose
selftest exits 1 in the counter's fresh clone because it invokes `git -C <absent path> show <sha>:
tools/mutate-and-run.sh` — a sibling-repo-shaped fixture, unlike `tools/witness-metadata.py`, which passes 39/39
from a fresh clone. Reproduced at
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w2/@P@ExecTool26/` (`c3-counter-explain.out`).

## 7. Receipt index (`.ufo/waves/round-51/w2/@P@ExecTool26/`)

| file | what it shows |
|---|---|
| `summary.txt` | this seat's receipt index and headline numbers |
| `row-2167.txt` | the audited row, verbatim, from SKILL.md at CAND |
| `row-2167.sha256` | sha256 of that line (newline stripped) |
| `section-round51-table.txt` | SKILL.md:2138-2172 at CAND (heading + full round-51 table) |
| `row-1553-round13.txt` | the superseded round-13 witness-metadata row, for the P1 contrast |
| `SKILL-at-cand.md` | SKILL.md at CAND (whole file) |
| `tool-at-cand.py` | `tools/witness-metadata.py` at CAND (48 914 B) |
| `row-cells-at-cand.py` | script printing the counter's parsed 8 cells for the row |
| `counter-run-row.py` | script running the counter's own `row_reason` + `run_row` on the row |
| `c3-counter-explain.out` | full `--explain` output of the frozen counter at CAND (cover line + final line) |
| `selftest.out` / `selftest.err` | the row's exact self-test, stdout / stderr (stderr empty) |
| `usage.out` / `usage.err` | the `--r51-no-such-flag` usage probe, stdout (empty) / stderr |
| `exit-sweep.txt` | exhaustive exit-code sweep of the tool |
| `timings.txt` | wall times for the self-test and the usage probe |
| `pin-liveness.txt` | per-pin tamper results and the companion's byte-vs-content behaviour |
| `write-scope.txt` | strace-derived write/read scope, TMPDIR fallback, lane cleanliness |
| `strace-check.txt` | full strace of `--check` (no write opens) |
| `strace-selftest-writes.txt` | every lane-relevant write-mode open of `--selftest` (all under the TMPDIR tree) |
| `strace-bad-tmpdir-fallback.txt` | the `/tmp` fallback when TMPDIR is unusable |
| `mutation-battery.py` / `mutation-battery.txt` | 15-mutant battery: selftest vs live `--check` per mutant |
| `round13-expected.json` | the round-13 frozen expected record (pins the companion digest and the tool's sha) |

Cleanup: the scratch root `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool26/` (clone, work trees, copies) is
deleted before this seat yields. The lane repo was never written to; the only lane-side writes are this seat's
report and its receipts under `.ufo/waves/round-51/w2/`.
