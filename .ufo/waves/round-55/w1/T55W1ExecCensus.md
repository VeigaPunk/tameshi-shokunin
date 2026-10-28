# T55W1ExecCensus — census at base (round 55, w1)

**Item.** Run `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`, report exit code, row count
(`grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md`) and every warning; then prove the duplicate guard is
load-bearing on a scratch copy of the lane corpus with one indented `  | S999 |` duplicate row appended.

**Verdict.** Item done. At base the conformance check exits **0** with **139 rows** and **16 warnings, zero E codes**;
all 16 are enumerated below. The duplicate guard is load-bearing: a two-space-indented `  | S999 |` duplicate row
appended inside `## Registry` of a scratch copy is reported as **E04** (exit 1), a verbatim duplicate as **E03 + E04**.
Two append hazards and one frozen-artifact integrity drift are reported (not fixed).

Base rev `0a2010acd1e92e4e332774050825e21bcfc7e079`; frozen counter set `631cd645…`. Lane:
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. No lane production file was edited by this seat.

## 1. Base measurement (exact)

```
$ cd /home/vgpnk/Projects/shokunin
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
… 16 W lines + "tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md"
EXIT=0
```

| metric | value | evidence |
|---|---|---|
| exit | **0** | `T55W1ExecCensus-receipts/base-validate.tsv` (log: `census-fixtures.log`) |
| rows (`grep -cE '^ {0,3}\| S[0-9]{3,} \|'`) | **139** | same |
| E codes | **0** | same |
| W codes | **16** (15 × W04, 1 × W01) | same |
| stdout lines | 17 (16 findings + 1 `ok`) | same |
| stderr | 0 bytes | `base-validate.err` |
| `corpus/SOURCES.md` sha256 | `4a466c10d6bb4935d20b8fb74a2d4ec08b315ceb67a2896a83f84e5d1258f992` | `census-base-rev.log` |

Base-rev cross-check (immutability of the "at base" claim): `git clone --shared` of the lane into scratch,
`rev-parse --show-toplevel` asserted equal to the clone path, `checkout --detach 0a2010ac`; same 139 rows, same
sha256, **identical finding set** after stripping the lane label and path
(`T55W1ExecCensus-receipts/base-rev-validate.tsv`, `census-base-rev.log` →
`identical (worktree == base rev findings)`).

## 2. Every warning (all 16, verbatim; order as printed)

```
W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
W04	S092 duplicate url bazel.build/remote/caching across scopes
W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
W04	S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
W04	S265 duplicate url testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html across scopes
W04	S266 duplicate url pitest.org/quickstart/incremental_analysis across scopes
W04	S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes
W04	S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes
W04	S274 duplicate url bazel.build/basics/hermeticity across scopes
```

Per-code meaning (from the script's own contract header): W04 = same normalised URL across ≥2 scopes (warn-only,
does not change exit); W01 = tier-C row mined with a non-`—` used-by. W-codes never flip the exit code
(`W04-does-not-fail-validation`, `W-only-registry-exit-0` in the script's selftest), which is why the lane is
conformant despite 16 warnings.

Machine-readable copy: `T55W1ExecCensus.json` (`warnings[]`, code + detail) and
`T55W1ExecCensus-receipts/warnings.json`.

## 3. Guard load-bearing proof (scratch copies of the lane, `/fast/scratch/hyaku`)

Method: `rsync -a --exclude .git` of the lane into scratch, the duplicate row inserted as the last line of
`## Registry` (immediately before `## Paths`), then
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin <scratch>/tameshi-shokunin`.
The row used is an exact copy of S279 (Python `tempfile` docs, scope "the documented search order behind the
resolver", no `supersedes` token so the E04 exemption cannot mask it), id replaced by S999 for the primary case.

| fixture | inserted line | exit | observed findings | receipt |
|---|---|---|---|---|
| **fx-a (primary)** | `  | S999 | <S279 url+scope> …` — 2-space indent | **1** | `E04 S999 duplicate url docs.python.org/3/library/tempfile.html within scope the documented search order behind the resolver` | `fx-a.tsv` |
| fx-b | `  | S279 | …` — verbatim S279 row, 2-space indent | **1** | `E03 S279 duplicate id` + `E04 S279 duplicate url … within scope …` | `fx-b.tsv` |
| fx-c | `    | S999 | …` — 4-space indent | 0 | none; rows still 139 | `fx-c.tsv` |
| fx-e | S280 used-by repointed to a non-existent path | **1** | `E11 S280 missing used-by corpus/lessons/round-55-missing-fixture.md` | `fx-e.tsv` |

Guard is load-bearing end to end: the row count moves 139 → 140 for parsed rows (fx-a/fx-b), the duplicate is named
by id/url/scope, and the exit code flips to 1. Read the `delta_vs_base` block in `census-fixtures.log` carefully: every
line differs in the lane-label/path column (`tameshi` → `tameshi-shokunin`), because the fixture is addressed by
directory instead of by `shokunin.conf` name; normalising that column, the finding set differs from base by exactly
the single added `E04 S999` line — the 16 pre-existing warnings are unchanged.

**fx-c caveat (by design, but worth naming):** the parser contract is "0–3 leading spaces are rows, 4+ are indented
code". A row accidentally indented by four spaces is *silently invisible* — not counted, not validated, exit 0. The
guard therefore covers 0–3-space rows only, which is exactly the `  | S999 |` shape the round asked about.

## 4. Append hazards (measured, not asserted)

The base file **had no trailing newline** (last byte `.`; `census-base-rev.log`). Two EOF-append behaviours were
measured on scratch copies:

| fixture | how appended | result | receipt |
|---|---|---|---|
| fx-d1-newline-closed | newline closed first, then `  | S999 |` row, 2-space indent, at EOF | `E12 S999 row outside Registry section`, **exit 1** — the last section is `## Id allocation`, so an EOF row is outside `## Registry` | `fx-d1-newline-closed.tsv` |
| fx-d2-no-trailing-newline | plain `>>` onto the unterminated last line | row **fused into the last `## Id allocation` bullet**; grep for `^ {0,3}\| S999 \|` = 0 while `S999` occurs once; census **exit 0**, zero E codes — the append is invisible | `fx-d2-no-trailing-newline.tsv` |

Consequence for whoever appends rows: insert inside the Registry table (before `## Paths`) and make sure the file
ends with a newline first; an EOF `>>` either yields E12 or, on an unterminated file, silently loses the row. The
round-55 append itself did this correctly: S280 is the last Registry row (line 155), immediately before `## Paths`,
and the file now ends with a newline.

## 5. Wave-in-flight state (freshness)

The lane moved under this seat; three snapshots, all with the same command:

| captured (UTC) | rows | exit | E codes | notes |
|---|---|---|---|---|
| before any round-55 append (base) | **139** | **0** | 0 | sha `4a466c10…`; 16 warnings; `base-validate.tsv` |
| mid-wave (between the base capture and 16:52:35Z) | 140 | **1** | 1 | `E11 S280 missing used-by corpus/lessons/round-55.md` — S280 landed before its lesson file |
| 16:52:35Z / 16:52:56Z | **140** | **0** | 0 | `round-55.md` written; S280 parses as 13 fields; warning set identical to base (`warning_delta_vs_base` empty); `census-live-state.log`, `census-end-state.log` |

Also observed once mid-wave: `census` printed `tameshi rows 95` while the file was being rewritten (partial file).
Both transient states are concurrency artefacts of other seats' writes, not validator defects; the E11 mechanism is
separately reproduced deterministically in fx-e so it does not rest on an unrepeatable snapshot.

At report time the conformance check is **exit 0, 140 rows, 0 E, 16 W, stderr empty**
(`conformance-validate.tsv`, `census-frozen-artifacts.log`, captured 2026-10-28T16:54:13Z).

ID coverage: 139 rows at base = S001–S279 with documented gaps — S038–S039 (allocated, never written, retired),
S098 (source not opened), S109–S131/S133–S151 (round-40 refusals, `corpus/lessons/round-40.md`), S161–S255 (staged
ids reserved by document for the package). `validate` has no gap check by design; the gaps are documented, not lost
rows. Round 55 adds S280.

## 6. Frozen-artifact observations (report only — this seat edited nothing there)

Two independent integrity problems in the frozen counter set, both present in this seat's very first `git status`
(before any read or write by it) and unchanged by it:

1. **The freeze manifest does not self-verify.** 2 of 6 digests fail:
   ```
   $ jq -r '.files | to_entries[] | "\(.value)  \(.key)"' .ufo/evidence/round-55/freeze.json | sha256sum -c -
   .ufo/evidence/round-55/contract.json: FAILED
   .ufo/evidence/round-55/c1/measure.py: OK
   .ufo/evidence/round-55/c2/measure.py: FAILED
   .ufo/evidence/round-55/no-harm.sh: OK
   .ufo/evidence/round-55/deciding-run.sh: OK
   .ufo/evidence/round-55/controls.sh: OK
   ```
   Timing shows why: `freeze.json` mtime `13:49:59 -0300`, `contract.json` and `c2/measure.py` mtime
   `13:50:08 -0300` — the manifest was written 9 s before the last edits to the two files it pins, and the
   recorded digests (`ed6871e1…`, `ab3ae751…`) do not match the current bytes (`0b99dd8c…`, `d6ca1d85…`).
   `contract.json` carries 4 in-band `amendments[]` entries, `freeze.json` 3, so this reads as a sanctioned
   amendment whose digest map was not recomputed after the final edit. For C2 auditability the manifest should be
   re-frozen (digests recomputed, amendment appended) before the deciding run.
2. **A frozen before-receipt is empty in the worktree.** `.ufo/evidence/round-55/before/c2.stdout` is **0 bytes**;
   the frozen commit `631cd64` holds **2634 bytes** starting `EXPLAIN grammar repeat-control --selftest rc=2 FAIL`.
   `before/c1.stdout` is intact (2276 B). If this is not an in-progress rewrite, the C2 "before" evidence is lost
   from the worktree and must be restored from `631cd64` by the integrator (this seat must not write there).

Both may be a live-editing race with the amendment process; the check should be re-run once the wave settles.

## 7. Scope, freshness, tooling

- Wrote only: this report, `T55W1ExecCensus.json`, and `T55W1ExecCensus-receipts/` (34 files: 13 `.tsv`, 13 `.err`,
  7 `.log`, `warnings.json`). No edit to `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`, or
  `.ufo/evidence/**`; verified with `git status --porcelain` (`corpus/SOURCES.md` and the round-55 evidence edits
  are other seats' writes).
- Scratch: `HYAKU_SCRATCH=/fast/scratch/hyaku`, `S=/fast/scratch/hyaku/tameshi-r55/<fixture>`, each with
  `trap 'rm -rf -- "$S"' EXIT`; every git call named `-C "$D"` and the clone's `rev-parse --show-toplevel` was
  asserted equal to `$D` before `checkout --detach`. All fixture trees removed on exit; runner scripts deleted.
- No mutating git operation anywhere on the lane (no add/commit/push/checkout of the lane, no jj).
- Tooling: **no installs, no upgrades** — `bash`, `gawk`, `rsync`, `coreutils`, and the pre-existing
  `/home/vgpnk/.local/bin/jq` sufficed. pacman transactions are paused host-wide and were not needed.

## 8. Files

- Report: `.ufo/waves/round-55/w1/T55W1ExecCensus.md`
- Machine-readable: `.ufo/waves/round-55/w1/T55W1ExecCensus.json`
- Receipts: `.ufo/waves/round-55/w1/T55W1ExecCensus-receipts/`
  - `base-validate.tsv|.err` — the base run
  - `base-rev-validate.tsv|.err`, `census-base-rev.log` — base-rev clone reproduction
  - `fx-a.tsv`, `fx-b.tsv`, `fx-c.tsv`, `fx-d.tsv`, `fx-d1-newline-closed.tsv`, `fx-d2-no-trailing-newline.tsv`,
    `fx-e.tsv` (+ `.err`), `census-fixtures.log`, `census-eof-append.log`, `census-fixture-e11.log` — guard proofs
  - `current-validate.tsv`, `census-live-state.log` — mid-wave snapshot
  - `end-validate.tsv`, `conformance-validate.tsv`, `final-conformance.tsv|.err`, `census-end-state.log`,
    `census-frozen-artifacts.log` — end state
  - `warnings.json` — the 16 warnings as JSON
