source: S283 — GNU Grep Manual, §2.3 Exit Status — https://www.gnu.org/software/grep/manual/grep.html#Exit-Status (row in `corpus/SOURCES.md`; opened 2026-10-28 by scout T57W1ScoutSourceA, quote re-opened by the L1 the same day; receipt `.ufo/waves/round-57/w1/T57W1ScoutSourceA-receipts/gnu-grep-manual.html` sha256 `517177d0…675f37`, quote at receipt line 1208); own work — `tools/receipt-revision-gate.py` at `5e3569969b53` (sha256 `c60772ce…0569ac9`; exits returned at :92, :183, :187, :194, :220)
verified-at: 2026-10-28 — the sweep and the staged-row recheck ran at base `5e3569969b532310d2b8a3d130901757a3df356b`; outputs in `.ufo/waves/round-57/w1/T57W1ScribeKnowledge-receipts/` (`gate-sweep.stdout`, `registry-recheck.stdout`, `lane-demo.stdout`)
recheck: 180d — `python3 tools/receipt-revision-gate.py --selftest` must print `GATE_SELFTEST: 19/19 pass`, and `python3 tools/registry-check.py --rev REV --tag new-r57` must print `REGISTRY_CHECK: held=3/3 superseded=0` (REV = the commit that installs the three rows; at base the tag selects no row and the command exits 2, `registry-recheck.stdout`)

# The gate's exit map and the registry rows that pin it (round 57)

## Why a gate needs executed rows beyond its selftest

`receipt-revision-gate.py --selftest` builds its own repository under `TMPDIR` and proves
that each code fires on that fixture. It does not prove that the command the lane writes
down runs (relative `--lane .`, a relative receipt path, cwd at the lane root), that the
receipt bytes the lane committed still give the recorded verdict, or that the entry resolves
at a revision. A registry row is the executed form of those three: `registry-check.py --rev REV`
clones the revision, runs the row's `argv` from the clone root, and holds the row only when
the exit equals `expect.exit` and every `stdout_contains` needle appears. Measured at base,
where the lane has no `tools/fixtures/receipt-gate/` tree (`lane-demo.stdout`), the staged
accept row's command gives `RECEIPT_MISSING` (rc 3) from the lane while the selftest reads
`GATE_SELFTEST: 19/19 pass` (rc 0). A row goes red on that; the selftest does not.

## The exit map

| exit | class | where | measured by (`gate-sweep.stdout`) |
|---|---|---|---|
| 0 | PASS: every receipt admitted; `verdict=PASS` | :220 | `accept-matched`, `identical-on-paths`, `control-ancestors`: rc 0 |
| 2 | could-not-evaluate: `--certified` does not resolve; the gate did not run (`GATE: error=unresolvable-certified`) | :194 | `certified-unresolvable`: rc 2, `RECEIPT_REV_UNRESOLVABLE` |
| 3 | REFUSED: at least one receipt carries a named code | :220 | 13 refusal cases (12 fixture cases and the `--json` form): rc 3, one code each |
| 1 | not in the header's map: usage (`SystemExit`, :92, :183, :187) and an uncaught `--paths` read (:197) | — | `usage-no-receipt`: rc 1, no verdict line; `paths-file-missing`: rc 1, `FileNotFoundError` traceback |

The module header documents exit 0, exit 3 and the eleven codes; exit 2 appears only in the
code and exit 1 nowhere. The scout's quotation of GNU grep (S283: "0 if a line is selected,
1 if no lines were selected, and 2 if an error occurred") gives 1 the meaning "negative
answer". A caller who reads exit 1 by that convention would misread a usage error
[INFERENCE: no caller in this lane does so today].

## Truth table: code by condition

Each row is one CLI invocation on a fixture repository (`c0`: `surface.txt`, `moved.txt`;
`c1` changes `moved.txt`; a side commit off `c0`) at base bytes `c60772ce`; `gate-sweep.sh`
prints the case names used here.

| condition | role | argv shape | rc | code |
|---|---|---|---|---|
| rev equals certified | positive | `--certified C1`, receipt names C1 | 0 | none |
| older rev, content identical on the declared surface | positive | `--paths surface.txt`, receipt names C0 | 0 | none |
| older rev, a listed path drifted | positive | `--paths surface.txt moved.txt` | 3 | `RECEIPT_REV_CONTENT_DRIFT` |
| older rev, no `--paths` | positive | receipt names C0 | 3 | `RECEIPT_REV_MISMATCH` |
| older rev, drift on the surface | verdict | as the drifted row | 3 | `RECEIPT_REV_CONTENT_DRIFT` |
| no `rev=` / JSON `rev` token | positive | `VERDICT: no revision named` | 3 | `RECEIPT_REV_ABSENT` |
| two distinct revs in one positive | positive | `A rev=C0`, `B rev=C1` | 3 | `RECEIPT_REV_AMBIGUOUS` |
| revision not in the repository | positive | `rev=deadbeefdead` | 3 | `RECEIPT_REV_UNRESOLVABLE` |
| control, every rev an ancestor | control | `CTL A rev=C0`, `CTL B rev=C1` | 0 | none |
| control names a non-ancestor | control | `CTL A rev=SIDE` | 3 | `RECEIPT_CONTROL_NOT_ANCESTOR` |
| sidecar digest wrong | verdict | `PATH.sha256` of 64 zeros | 3 | `RECEIPT_DIGEST_MISMATCH` |
| required regex absent | verdict | `:C1_X_PASS=` | 3 | `RECEIPT_REQUIRED_LINE_MISSING` |
| receipt path absent | positive | `nope.txt` | 3 | `RECEIPT_MISSING` |
| receipt empty | positive | one newline | 3 | `RECEIPT_EMPTY` |
| receipt path is a directory | positive | `r-dir/` | 3 | `RECEIPT_NOT_BLOB` |
| `--certified` does not resolve | positive | `--certified deadbeef…` | 2 | `RECEIPT_REV_UNRESOLVABLE` |
| no `--receipt` | — | `--lane --certified` only | 1 | none (usage) |
| `--paths` file absent | positive | `--paths no-such.txt` | 1 | none (traceback) |

Three lane-level cases in `lane-demo.stdout` and `gate-sweep.stdout` agree with the recorded
entries: the round-56 copy of the round-54 control (`.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout`)
gives `RECEIPT_REV_CONTENT_DRIFT` (rc 3); `.ufo/evidence/round-54/control/controls-b.stdout` gives
`RECEIPT_REV_UNRESOLVABLE` (rc 3); round 55's `c2.stdout` gives `RECEIPT_REV_ABSENT` (rc 3).

## What the three staged rows cover, and what they do not

The rows are staged in `T57W1ExecRegistryRows`; run at a scratch commit they give
`REGISTRY_CHECK: held=3/3 superseded=0` (`registry-recheck.stdout`): `receipt-gate-accept`
(exit 0), `receipt-gate-content-drift` (exit 3), `receipt-gate-unresolvable-certified` (exit 2).

- They emit **2 of the 11 codes**, `RECEIPT_REV_CONTENT_DRIFT` and `RECEIPT_REV_UNRESOLVABLE`.
  **Nine codes are emitted by no registry row**: `RECEIPT_MISSING`, `RECEIPT_EMPTY`,
  `RECEIPT_NOT_BLOB`, `RECEIPT_REV_ABSENT`, `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_REV_MISMATCH`,
  `RECEIPT_CONTROL_NOT_ANCESTOR`, `RECEIPT_DIGEST_MISMATCH`, `RECEIPT_REQUIRED_LINE_MISSING`
  (`lane-demo.stdout`, final block). The round contract's count of six is wrong for this row set.
- The sweep emits all eleven codes from the CLI (`lane-demo.stdout`: "emitted by the sweep: 11").
  That is executed coverage, not a registry row, and the lane does not re-run it.
- The accept row names the certified revision, so it exercises the strict match. The `--paths`
  content-identity exception is covered only by selftest case `content-identical-positive-accepted`
  and the sweep's `identical-on-paths`.
- Exit 1 (usage and the `--paths` traceback) is reached by no row.

## Limits

- A row proves one command at one revision with one fixture. The limits in
  `knowledge/receipt-revision-binding.md` §What the gate cannot see still hold: a copied
  `rev=` passes, a sidecar copied with its receipt passes, the claim text is not read.
- The truth table covers only the conditions the sweep builds.
- Routed, not fixed here (the gate is a lane production file):
  1. `paths-file-missing` exits 1 with a traceback. Exit 2 (could-not-evaluate) is in the code
     (:194) and in the SKILL row, not in the header; the gate returns 1 from an unguarded
     `Path(paths).read_text` (:197). Route to the lane's next round.
  2. Fixed at C0 `ca75c26` (`SKILL.md:53`): `## Standing rules` row one now names
     `RECEIPT_REV_CONTENT_DRIFT` for a verdict receipt on a declared surface, as the sweep's
     `verdict-role-drift` emits (R56.2). This entry keeps its base reading.

## Re-derive

```sh
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
git -C "$L" show 5e3569969b532310d2b8a3d130901757a3df356b:tools/receipt-revision-gate.py | sha256sum   # c60772ce…0569ac9
python3 "$L/tools/receipt-revision-gate.py" --selftest                  # GATE_SELFTEST: 19/19 pass
bash "$L/.ufo/waves/round-57/w1/T57W1ScribeKnowledge-receipts/gate-sweep.sh"        # truth table
bash "$L/.ufo/waves/round-57/w1/T57W1ScribeKnowledge-receipts/registry-recheck.sh"  # staged rows, scratch commit
bash "$L/.ufo/waves/round-57/w1/T57W1ScribeKnowledge-receipts/lane-demo.sh"         # lane block, coverage count
```

## Falsifier

This entry is wrong if any of these happens; each is a command, not an opinion.

1. `--selftest` at the cited sha prints anything but `GATE_SELFTEST: 19/19 pass`.
2. A `gate-sweep.sh` case returns a different exit or code from the truth table.
3. At the content-final commit, `registry-check.py --rev REV --tag new-r57` does not print `REGISTRY_CHECK: held=3/3 superseded=0`.
4. The gate's `CODES` tuple stops having eleven entries, or the sweep stops emitting one of them.
