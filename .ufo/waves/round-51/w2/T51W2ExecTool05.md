# T51W2ExecTool05 — independent audit of the C3 registry row for `tools/evidence-disposition.py`

Seat: T51W2ExecTool05 (round 51, wave 2, falsify lane). Milestone: C3 row falsification.
Candidate `6d8c11e378aa90b12650808e1b79270742935f15`; base `9962033fd7a75aa2f2847e979dd687a5d28505a1`.
Verdict map, predicate, counter and spec are untouched; I wrote no source and repaired no row.

**Verdict: the row's mechanical C3 fields hold — the counter covers it and its self-test really does
pass from a fresh clone at CAND. Four textual/structural claims in the row are false or materially
incomplete, and one of them hides a live C2↔C3 coupling. The row's `Pinned values` and
`Write scope` cells are not true of the tool.**

Row under audit: `SKILL.md:2146` — "| evidence disposition accounting | gate | …" — table row **5**
of 30 in `#### Gate/probe registry — round 51` (rows start at `SKILL.md:2142`).

---

## 1. What I ran, and what it returned

All execution in a fixture clone, never in the lane:

```
git clone -q --shared --no-checkout <lane> $S/clone
git -C $S/clone checkout -q --detach 6d8c11e378aa90b12650808e1b79270742935f15
git -C $S/clone rev-parse --show-toplevel   # => $S/clone, asserted before any operation
```

Scratch root `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool05/`, `TMPDIR=$S/work/tmp`, `stdin`
`/dev/null`, cwd the clone — the counter's exact conditions.

| Probe | Command | Exit | Last stdout line | Wall |
|---|---|---|---|---|
| row's exact backticked self-test | `python3 tools/evidence-disposition.py --selftest` | **0** | `SELFTEST: PASS (66/66)` | 3.69–5.36 s (18 timed runs, median ≈4.7 s) |
| usage probe | `python3 tools/evidence-disposition.py --r51-no-such-flag` | **64** | (stdout empty; stderr `evidence-disposition.py: unknown argument: --r51-no-such-flag`) | 0.04–0.05 s |
| the counter's own `row_reason()` on line 2146 | — | — | `None` (no static failure) | — |
| the counter's own `run_row()` on line 2146 | — | — | `(None, 'SELFTEST: PASS (66/66)')` | 4.56 s |

Receipts: `@P@ExecTool05/measurements.txt`, `selftest-CAND-clone.stdout`,
`usage-r51-no-such-flag.{stdout,stderr}`. Cross-check against a peer's full counter run is
consistent: `@P@ExecTool02/c3-counter-full-run.txt:5` reads
`C3_TOOL tools/evidence-disposition.py: covered line 2146 selftest exit=0 last=SELFTEST: PASS (66/66)`.

The 66 is genuine, not an author-chosen constant: the tool computes `total = passed + len(failed)`
(`tools/evidence-disposition.py:3112-3123`), prints 66 distinct `SELFTEST_CASE` lines with 66 unique
names and no duplicates, and the string `66` occurs nowhere in the source as a literal. The
`SELFTEST:` marker is a real computed tally, not help text.

**Root cause of the silently-low failure register, checked and excluded for this row:** the selftest
writes its fixtures to `/tmp` *hardcoded* (`tempfile.mkdtemp(prefix="tameshi-r14-evidence-disposition-selftest.", dir="/tmp")`,
`:2351`) and ignores `TMPDIR`. So the counter's `TMPDIR=WORK/tmp` isolation does not contain it; on a
failing run the fixtures stay behind. I measured 15 pre-existing
`/tmp/tameshi-r14-evidence-disposition-selftest.*` trees (100 MB) from earlier runs before I started,
plus the one my own deliberate `jj`-less run created (6.7 MB, removed). This is a real write-scope
defect, recorded in §4.

---

## 2. The known C3 blocker is **not** this row

The task says "including row16's known clone-context failure if your tool is it". It is not. Row 16 of
the round-51 table is `SKILL.md:2157` = **round21 measure facade** (`tools/round21-measure.py`), the
tool whose truthful `--selftest` exits 1 from the counter's fresh clone because its fixture expects
sibling fleet repos. My row is table row 5 (`SKILL.md:2146`).

Evidence that mine is clone-context-clean: the selftest passes 66/66 from the fresh `--shared` clone
with no sibling repos present, and it passes from an unrelated cwd with no `.git` at all. Peer receipt
confirms only round21-measure is missing (`C3_TOOL tools/round21-measure.py: MISSING (line 2157
selftest-exit=1 last=)`). See `@P@ExecTool05/row16-and-jj-dependency.txt`.

The one real environmental dependency of my row is **`jj` on PATH**. With `PATH=/usr/bin:/bin` the
selftest exits **1**: `SELFTEST: FAIL (3/66 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip,
v2-jj-without-lane-branch; fixtures kept at …)`. The row discloses this ("needs jj on PATH"), jj
0.45.1 is at `/home/vgpnk/.local/bin/jj` here, and the counter's `env()` does not strip PATH — so the
disclosure is true and the row is covered in this environment. But it is load-bearing: in an
environment without jj, this covered row becomes a missing one, and the row's `Self-test` cell is the
only thing that warns a reader.

---

## 3. `Pinned values` is materially incomplete — and hides the C2 coupling

The cell names four paths:

```
`.ufo/evidence/round-13/expected.json`, `.ufo/evidence/round-13/verification.json`,
`.ufo/evidence/round-13/producer-oracle-repair.json`, `.ufo/evidence/round-18/dispositions.json`;
expected ids and exits are literals in the tool selftest
```

All four exist at CAND (the counter's `PATHISH` existence check passes), and each named path really
does affect the verdict — I tampered each and the tool went exit 2 `input_digest_mismatch`
(`tamper-named-pin-verification-json.stdout`; same shape for the others).

But the tool digest-verifies **17** distinct paths, not 4: the v2 manifest's `inputs` (4) plus
`expected.json`'s own `inputs` map (13). **13 of the 17 are undeclared.** Each of these undeclared
paths flips the verdict, measured:

| Undeclared pinned path | Tamper result |
|---|---|
| `.ufo/evidence/round-14/dispositions.json` | exit 2 `input_digest_mismatch` |
| `.ufo/evidence/round-13/pin-manifest.json` | exit 2 `expected_input_digest_mismatch` |
| `.ufo/evidence/round-12/BashWitness/declared.tsv` | exit 2 `expected_input_digest_mismatch` |
| `tools/bash-witness-study.py` (live bytes) | exit 2 `historical_input_uncommitted` |
| `tools/mutate-and-run.sh` (live bytes) | exit 2 `historical_input_uncommitted` |

Receipts `tamper-unnamed-*.stdout`, `pinned-set-analysis.txt`.

**This is the C2↔C3 coupling the row makes invisible.** `tools/mutate-and-run.sh` is one of the v2
manifest's three `historical_inputs` waivers, pinned at rev `4acc607d` to
`75ed934d…` — which equals `expected.json`'s own pin for the runner. C2's tenth leg changes the
runner's live bytes at CAND (`977de470…`; base was already `a7d3f2dd…`). The waiver stays legitimate
precisely because the live bytes moved away from the pin (G1 `historical_input_unneeded` refuses a
waiver whose live bytes still equal the pin). Measured in the CAND clone:

* live edit of `tools/mutate-and-run.sh` → exit 2 `historical_input_uncommitted`
* runner reverted to the round-13 (waived-rev) bytes → exit 2 `historical_input_unneeded`
* CAND bytes → exit 0 clean

So the gate is green at BASE too (`entry-mode-base.stdout`), and C2 neither breaks nor is required by
it — but **any future edit that restores the runner's round-13 bytes turns this C3 gate red**, and the
row's `Pinned values` cell never names the runner, so no reader of the registry can see that. Receipt:
`@P@ExecTool05/C2-interaction.txt`.

Also false as written: "**expected ids and exits are literals in the tool selftest**". Eight of the
twelve lane-level expected check names (`pin_selftest`, `metadata_selftest`, `metadata_old_null`,
`metadata_corrected`, `producer_after`, `witness_check`, `witness_count`, `source_census`) appear
nowhere in the tool source; they live in the pinned `.ufo/evidence/round-13/expected.json`. Only
`producer_before`, `producer_before_oracle`, `producer_after_oracle` and `pin_live` appear, and those
are selftest-fixture names, not the lane's entry-mode expectations. The expected ids/exits for the
**entry command** are data in `expected.json`, digest-pinned — the opposite of "literals in the tool".

---

## 4. `Write scope` claims a scope the tool does not honour

The cell reads: "none in the lane — read-only over --root; selftest fixtures under
/tmp/tameshi-r14-evidence-disposition-selftest.* removed on pass, kept on failure".

True parts, verified: entry mode is read-only over `--root` (the lane working tree was unchanged after
I ran it in place); the prefix is exactly `/tmp/tameshi-r14-evidence-disposition-selftest.`; on **PASS**
the tree is removed (`shutil.rmtree(scratch)`, `:3120-3123`); on **FAIL** it is kept (the FAIL branch
prints `fixtures kept at …`, `:3113-3119`).

Untrue or incomplete, measured:

1. **`TMPDIR` is ignored.** The scratch root is `dir="/tmp"` hardcoded at `:2351`. The C3 counter runs
   every self-test with `TMPDIR=WORK/tmp/<hash>` (`c3/measure.py:160-168`); for this tool that
   isolation silently does not apply, and a failing selftest deposits a 6.7 MB tree in the host `/tmp`
   instead of the counter's work dir. 15 such trees (100 MB) from earlier rounds were already there.
   The row says "/tmp", so a careful reader sees the location — but the cell does not say the tool
   ignores `TMPDIR`, which is the fact that matters to the counter operator.
2. **`jj` config leakage is out of scope but real.** `_jj()` sets `HOME=lane.parent` and
   `XDG_CONFIG_HOME=lane.parent/"jj-config"` (`:2037-2038`), so jj does *not* write to the operator's
   `$HOME/.config/jj`. Measured: the real `~/.config/jj/repos` count was identical (1699 → 1699) before
   and after a full selftest, and the two files there with recent mtimes belong to other lanes' users
   (`kengaku-shokunin`, `tsukuroi-shokunin`), not to my runs. The tool is clean here; the *write scope
   cell* simply has no room to say so, and its "/tmp only" framing is therefore the accurate part of
   the claim.

---

## 5. `Verdict map` — declared codes are right; one code is mis-classified

The four codes the tool can return are declared (0 clean / 1 failed semantic expectation /
2 could-not-evaluate / 64 usage-could-not-evaluate) and match the tool's own docstring exit map
(`:107-113`). Reachability measured:

| code | how reached | class the row assigns | correct? |
|---|---|---|---|
| 0 | lane run, clean | clean | ✓ |
| 1 | a self-consistent dispositions set that breaks one expectation (`expected_exit_mismatch`) | failed semantic expectation | ✓ |
| 2 | digest tamper / invalid schema / missing file / non-dir root / `historical_input_committed`+`unneeded` | could-not-evaluate | ✓ |
| 64 | `--r51-no-such-flag`, missing value, `--selftest --json`, no args | could-not-evaluate (usage) | ✓ |

Two gaps in the mapping, both narrow:

* **An internal failure on the `--selftest` path surfaces as exit 1, not 2.** `main()` calls
  `selftest()` *outside* the guarded `try` (`:3209-3210`, the `try/except Exception → internal_error`
  is at `:3211-3219`). With `/tmp` unwritable the CLI exits **1** with a `PermissionError` traceback,
  which the row's map reads as "failed semantic expectation" instead of could-not-evaluate. Receipt:
  `selftest-internal-failure-exit.txt`, probe `selftest-crash-path-probe.py` / `cli_crash_probe.py`.
  Entry mode is correctly fail-closed (any exception → 2).
* **`--help`/`-h` exits 0** (`:3200-3202`), i.e. a usage request is classified "clean". Harmless in
  practice (the counter's usage probe is `--r51-no-such-flag`, which is 64), but it means exit 0 is not
  exclusively a verdict in this tool.

Neither gap makes the C3 predicate fail: the counter only requires the usage probe's code to appear in
the verdict map, and it does.

---

## 6. `Kind = gate` is correct (`tool truly fails or is only a probe`)

The tool can fail on its own merits: I produced exit **1** with `FINDING expected_exit_mismatch` from a
*self-consistent* dispositions/manifest set (re-pinned `expected.json` with `witness_count` expecting
exit 7 → the receipt's exit 0 mismatches), i.e. a genuine semantic verdict, not an input fault that any
fail-closed reader would grade 2. Lane entry command at CAND and in the live lane:
`EVIDENCE_DISPOSITION: clean exit=0 expected=12 effective=11 superseded=1 passed=11 failed=0
findings=0` plus three `HISTORICAL` lines for the waived tools. `kind = gate` stands, and it is not a
probe.

`Self-test command` cell is accurate apart from the timing figure: it claims "66/66 cases in about 3 s
at rev 84aa673a". The count and the rev are right — the tool blob at `84aa673a` and at CAND are the
same bytes (`123b8f1c…`), and I re-ran the selftest in a clone at `84aa673a`: exit 0, 66/66
(`selftest-at-84aa673a.stdout`). The "about 3 s" is optimistic: 10 timed runs spread 3.69–5.36 s
(median ≈4.9 s) at load average 13–24 on this host. A timing claim in the fast direction is the kind
of number a deciding run will not reproduce.

---

## 7. Mismatches, ranked

1. **`Pinned values` under-declares 13 of 17 digest-verified inputs**, and the omission includes
   `tools/mutate-and-run.sh`, the one path C2 edits. A restored runner silently reddens this gate; no
   other registry row or note discloses it. *(factual; citable at `@P@ExecTool05/C2-interaction.txt`,
   `pinned-set-analysis.txt`)*
2. **"expected ids and exits are literals in the tool selftest" is false** for the entry command: 8 of
   12 lane expectations exist only in pinned `expected.json`. *(factual)*
3. **`Write scope` omits that the tool hardcodes `/tmp` and ignores `TMPDIR`**, so the C3 counter's
   per-row scratch isolation does not apply to it; a failing selftest leaves 6.7 MB outside the counter
   work dir (15 such trees already on this host). *(factual; mechanism at `:2351`)*
4. **Verdict map mis-classes an internal failure on the `--selftest` path as exit 1 (failed) rather than
   exit 2 (could-not-evaluate)**; `--help` exits 0. *(narrow; `selftest-internal-failure-exit.txt`)*
5. **"in about 3 s"** is 3.69–5.36 s measured at load average 13–24. *(soft)*

None of these breaks C3's frozen predicate, which checks only: 8 cells present, kind ∈ {gate, probe},
entry names the tool, verdict map carries `0` and `1`, one backticked metacharacter-free self-test
argv of the form `python3 [-I] tools/T … selftest …`, every backticked path-like pinned token exists at
REV, non-empty write scope, owner `tameshi`, self-test exits 0 from a fresh clone at REV with its
last-line finding id present in the row, and the usage probe's exit code token in the verdict map. All
nine hold at CAND — I verified each independently and then via the counter's own `row_reason`/`run_row`.

I did **not** repair the row, and I did not touch the counter, the contract or any source file.

---

## 8. Files and integrity

Deliverable receipts: `.ufo/waves/round-51/w2/@P@ExecTool05/` —
`measurements.txt`, `pinned-set-analysis.txt`, `C2-interaction.txt`,
`row16-and-jj-dependency.txt`, `selftest-internal-failure-exit.txt`,
`selftest-CAND-clone.stdout` (+ empty `.stderr`), `selftest-at-84aa673a.stdout`,
`selftest-without-jj-on-PATH.stdout`, `usage-r51-no-such-flag.{stdout,stderr}`,
`entry-mode-lane-run.stdout`, `entry-mode-real-lane.stdout`, `entry-mode-base.stdout`,
`entry-mode-exit1-semantic-failure.stdout`, `tamper-named-pin-verification-json.stdout`,
`tamper-unnamed-pin-round14-dispositions.stdout`, `tamper-unnamed-pin-round13-pin-manifest.stdout`,
`tamper-unnamed-pin-round12-declared-tsv.stdout`,
`tamper-unnamed-historical-tools-bash-witness-study.stdout`, `tamper-manifest-rowdrop.stdout`,
`row-SKILL2146-evidence-disposition.txt`, `round51-table-rows-SKILL2142-2171.txt`,
`evidence-disposition.CAND.py`, `selftest-crash-path-probe.py`.

No git or jj mutation in the lane, fleet or any sibling repo: every write went to
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool05/`, to the shared clones inside it (asserted via
`rev-parse --show-toplevel`), or to my own deliverable paths. All clones were `git clone --shared`.
Scratch root deleted before yield; the one `/tmp` fixture tree my own deliberate `jj`-less failure left
behind was removed (the other 15 predate this seat). No tools installed or updated; pacman untouched.
