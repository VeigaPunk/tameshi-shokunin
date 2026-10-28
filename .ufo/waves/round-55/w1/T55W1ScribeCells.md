# T55W1ScribeCells — C2 registry cells (round 55, wave 1)

Seat: `T55W1ScribeCells` (leaf, no dispatch). Axis: **operability**. Milestone: **C2 registry cells**.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base `0a2010ac`; counter set `631cd64` and the
L1's re-freeze `e2979f2`; integration commit `9cf0146` ("C0"). No lane production file was edited by
this seat.

Deliverables:

- `T55W1ScribeCells.json` — `rows` is the requested `row name -> new cell` map, plus template,
  scope table, the lazy-mode answer, `landed_review` (see §3) and findings with receipts.
- `T55W1ScribeCells.md` — this report.
- `T55W1ScribeCells-receipts/` — counter runs, per-mode grammar captures at two revisions, the
  lazy-mode strace files, `make_cells.py` (generator), `validate_cells.py` (checker),
  `cells-vs-c0.diff` (the 7-line patch against C0).

**Filename note.** The item text says to write `T55W1Er10.json`/`T55W1Er10.md`, but `T55W1Er10` is a
different live seat in this wave (C1, R54.10 correction) and those two filenames are its report and
machine list (`w1/swarm-registry.json` lists both seats). Verified while I worked: those two paths
are already contested — at the time of writing `T55W1Er10.md` carries seat `T55W1ScribeNote`'s
`## One line, every mode` draft and `T55W1Er10.json` carries a cold-read/ledger payload
(keys `pristine_ledger_entry`, `rekey_demo`). Writing there would have clobbered another seat, so the
same content lives under this seat's name; `jq .rows T55W1ScribeCells.json` is the requested map.

## 1. Answer

One ASCII template sentence per row, with three slots (`{prefix}`, `{modes}`, `{outside}`): the frozen
grammar line with the prefix the tool **actually prints**, the value named, exit 2, no
`RuntimeError`/`Traceback` token on either stream, both `TMPDIR` arms, the `/tmp` claim, and a scope
clause that names the tool's allocating modes and says which modes are outside.

- The seven cells are drafted, shape-checked and measured: `docs=7/7` on the frozen counter, with the
  cells' quoted prefixes equal to the measured first stderr tokens (`validate_cells.py`, `ok: true`).
- **The L1 landed a first version at C0 (`9cf0146`) and four of its seven cells quote a line no tool
  prints** (§3). `docs` still reads 7/7 because the arm only looks for the marker. The 7-line patch
  that fixes them, verified against the measured lines, is `cells-vs-c0.diff`
  (demo commit `ae76985`).
- Answer to the lazy-mode question: **all five lazy modes are outside the cell** (§4); no eighth cell
  may exist.

## 2. The template and the seven cells

ASCII only (the registry is byte-ASCII; the patch keeps 0 bytes > 127):

    Allocating-mode scratch-root class (round 55): on a set-but-unusable `TMPDIR`, exactly one
    stderr line and exit 2, `{prefix}: could-not-evaluate: cannot create clone scratch under the
    scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`, the value
    named with no `RuntimeError`/`Traceback` token on either stream; `TMPDIR` unset or empty (`''`)
    is the unset arm (the resolver skips an empty candidate, so the platform default applies); a
    usable `TMPDIR` holds every `mkdtemp` and the run creates nothing under `/tmp` (strace);
    scope: {modes}; {outside} (corpus/knowledge/scratch-root-contract.md).

| row | `{prefix}` (measured at C0) | `{modes}` | `{outside}` / caveat |
|---|---|---|---|
| repeat-control-selftest | `repeat-control` | `--selftest` | `--snapshot`, `--runs/--out` run mode |
| bash-witness-selftest | `WITNESS_STUDY` | `selftest` | `declare`, `run`, `rerun`, `count`, `check` |
| pin-disposition-selftest | `pin-disposition.py` | `--selftest` | `--manifest/--root` read mode |
| evidence-disposition-selftest | `evidence-disposition.py` | `--selftest` | `--json` disposition mode |
| context-capture-selftest | `context-capture.py` | `--selftest` | `--check` |
| registry-check-selftest | `registry-check` | `--selftest`, `--rev` | `--rev` sits on the unusable arm only (its usable path is the traced `--selftest`); live `--root` opens no scratch root |
| env-diff-selftest | `ENVDIFF_SETUP` | `--selftest`, `--contract` | none |

The prefix slot is the load-bearing part. Five of the seven tools do not print their file name:
`repeat-control` and `registry-check` print the stem, `bash-witness-study.py` prints `WITNESS_STUDY`,
`env-diff.py` prints `ENVDIFF_SETUP`. Only `pin-disposition`, `evidence-disposition` and
`context-capture` print `<name>.py`. Every prefix above was read from the tool (`receipts/c0-grammar/
*.err`) and asserted by `validate_cells.py`, never inferred from the module name.

## 3. The landed cells at C0 quote four lines that do not exist

Measured at `9cf0146` in a shared clone, `TMPDIR=<nonexistent>`, one stderr line each, rc 2
(`receipts/c0-grammar/`, comparison in `receipts/c0-cell-vs-measured.txt`):

| row | landed cell quotes | tool prints | |
|---|---|---|---|
| repeat-control-selftest | `repeat-control.py` | `repeat-control` | **false line** |
| bash-witness-selftest | `bash-witness-study.py` | `WITNESS_STUDY` | **false line** |
| registry-check-selftest | `registry-check.py` | `registry-check` | **false line** |
| env-diff-selftest | `env-diff.py` | `ENVDIFF_SETUP` | **false line** |
| pin-disposition-selftest | `pin-disposition.py` | `pin-disposition.py` | ok |
| evidence-disposition-selftest | `evidence-disposition.py` | `evidence-disposition.py` | ok |
| context-capture-selftest | `context-capture.py` | `context-capture.py` | ok |

Consequences, in the lane's own vocabulary: the cell is a *record* of what the tool prints, and four
of them assert a line the tree never emits — the same class of defect C1 is measuring, one revision
further out. The counter cannot see it: its docs arm is `MARKER in cell` and `len(cells) == 7`, and
the replayed selector on the landed file prints 7/7. The landed text also differs from the item in
two further ways: it names its allocating modes but not the non-allocating ones (so the lazy
boundary is invisible), and its registry-check cell names `--rev` without saying that `--rev` is
measured on the unusable arm only, which overstates what the `/tmp` census covers (the note seat
raised the same point for the note).

The fix is `receipts/cells-vs-c0.diff`: `1 file changed, 7 insertions(+), 7 deletions(-)`, generated
by `make_cells.py`, indentation-preserving against C0's 3-space serialization. Applied in a demo
clone it commits as `ae76985`, and `validate_cells.py` returns `ok: true` for all seven against the
`9cf0146` captures.

## 4. The five lazy modes: which one is *not* covered by that cell

**All five are not covered, and the cell says so.** The cell's promise is stated for allocating modes
only. Verified per mode, both `TMPDIR` states, `strace -f` (`receipts/lazy-*-*.strace`):

| lazy mode | registry rows | exit under unusable `TMPDIR` | references to the scratch-root path | `/tmp` references with a usable root |
|---|---|---|---|---|
| `repeat-control --snapshot` | `-snapshot-clean`, `-mismatch` | 0 | 0 | 0 |
| `bash-witness-study count` | `bash-witness-count` | 0 | 0 | 0 |
| `pin-disposition --read` | `pin-disposition-read` | 0 | 0 | 0 |
| `evidence-disposition --json` | `-round17`, `-round17-before`, `-round18`, `-round18-before`, `-round14-superseded` | 0 (branch checkout) | 0 | 0 |
| `context-capture --check` | `-frozen`, `-missing-env`, `-mapping-suffix` | 0 | 0 | 0 |

Consequences: (1) **no eighth cell** — the docs arm asserts `len(cells) == 7`, so a `scratch_root`
cell on any lazy row turns 7/7 into a failure; (2) the exclusion worth naming in review is
**`context-capture --check`**, because its tool is the one whose base `--selftest` printed the setup
class on stdout, so a reader could think `--check` prints the class too (it does not: it never touches
the scratch root); (3) `evidence-disposition --json` exits 2 with `historical_input_unavailable` on a
detached HEAD — the fact behind the counter's amendment 1 — so its lazy measurement needs a branch.

## 5. Evidence

Counter identity: `sha256(c2/measure.py) = 36ca47d3…` (`counter-sha*.txt`); the counter was amended
during the round (contract amendments 1-7; a ninth allocating mode `registry-check --rev`; note
denominator `len(allocating)`; cheap/expensive split), so every run is quoted with its own
denominators.

| rev (scratch clone) | contents | counter | verdict line |
|---|---|---|---|
| `de89493` | first cells, UTF-8 | 8-mode | `grammar=6/8 … docs=7/7 note=0/8 skill=0/1 total=11` |
| `6e350be` | + tool grammar, note, SKILL | 8-mode | `grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=0` **PASS** |
| `b8bd0e2` | ASCII cells | 8-mode | same **PASS**, `docs=7/7` (`c2-explain-ascii.stdout`) |
| `7de93ea` | ASCII cells, `--rev` marked outside the counter | 9-mode | `grammar=8/9 docs=7/7 note=8/9 skill=1/1 total=3` |
| `ee45944` | cells with `--rev` in scope, pre-fix `registry-check.py` replaced, note naming nine | 9-mode | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1` — every arm at its maximum, `bad: {}`; total=1 is the amendment-window arithmetic (F7) |
| `51c315c` | first cells patch onto C0 (`9cf0146`), prefixes corrected | 9-mode | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false` — every arm at its maximum, `bad: {}` (F7) |
| `ae76985` | same cells, indentation preserved (`cells-vs-c0.diff`) | 9-mode | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0` **PASS** (`c2-explain-ae76985.stdout`) |

Counter bytes could not be pinned across the wave: the file under
`.ufo/evidence/round-55/c2/` is being amended live (recorded at launch in `counter-sha*.txt` as
`36ca47d3…`; `0458f632…` when last read). The two C0 runs above report the same arms and the same
`bad: {}` yet print different totals, which is the amendment window, not an arm difference — so each
verdict is quoted with its own receipt and its own launch-time sha, and the per-run `c2-receipts*.json`
is the authority for the arm counts.

Commands:

    S=/fast/scratch/hyaku/tameshi-r55/T55W1ScribeCells
    git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/c0
    git -C $S/c0 checkout --detach 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
    TMPDIR=$S/no-such-tmpdir python3 tools/<tool>.py <allocating-mode>   # per-mode captures
    python3 $S/make_cells.py tools/registry.json $S/registry-c0b.json      # 7/7 lines replaced
    python3 T55W1ScribeCells-receipts/validate_cells.py tools/registry.json \
        T55W1ScribeCells-receipts/c0-grammar
    python3 .ufo/evidence/round-55/c2/measure.py --lane $S/c0 --rev <rev> --work <empty> --explain

Other checks: registry gate still loads the edited file (`--only registry-check-selftest` →
`held=1/1`, rc 0, `registry-gate-row-json.out`); census `validate --root
/home/vgpnk/Projects/shokunin tameshi` → rc 0 (`census-validate.out`); the patch keeps the file ASCII
and `json.load` valid; the in-flight lane `tools/registry.json` before C0 was a whole-file
re-serialization with identical parsed rows (`lane-registry-semantic.txt`).

## 6. Findings (none repaired here)

**F1 — `registry-check --rev` had no class line; fixed at C0 and now measured.** `--rev` allocates the
fleet-mirror clone (`tools/registry-check.py:780`). Before the fix: rc 2, the class on **stdout** in
the parenthesis form `REGISTRY_CHECK: could-not-evaluate (cannot …)`, empty stderr, and `--rev --json`
printed JSON only with no class line (`gap-registry-check-rev*.out/.err`). At C0 both invocations
print exactly one grammar-matching stderr line with rc 2 and empty stdout
(`c0-grammar/registry-check-rev.err`, `revfix-*.err`). The counter was amended to nine modes and the
note moved to nine names; the cell names `--rev` in scope with the unusable-arm caveat.

**F2 — `repeat-control` writes a setup token to stdout.** `tools/repeat-control.py:232-234`
(`could_not_evaluate`) prints `REPEAT_CONTROL: setup_error` on stdout beside the stderr class line.
The round's requirement for this edit was "stdout carries no setup error"; the counter checks stdout
only for `RuntimeError`/`Traceback`, so C2 passes. The note seat flagged the same token independently.
Routing: the tool's owner. The fix is one line — drop the `emit(...)`; the exit code carries the class.

**F3 — the pre-C0 `tools/registry.json` change was a whole-file re-serialization** (1275 insertions /
1026 deletions) for a change whose parsed rows are identical to the base outside the cells. Applying a
7-line patch keeps the review honest; C0's own file is now 3-space serialized, hence the
indentation-preserving generator.

**F4 — `/fast/scratch/hyaku/tameshi-r55/` was deleted mid-run** between two calls (a 205 s counter
invocation), taking that run's receipts; rebuilt, and receipts are now written straight into the wave
directory. The note seat lost its scratch directory the same way — an external cleanup is active under
`/fast/scratch/hyaku` and the L1 should warn the wave.

**F5 — the counter moved under the wave.** My cell text deliberately carries no mode counts (no
"eight", no "nine") so it survives the amendment window; the note cannot, and its "Eight allocating
modes" had to become "Nine".

**F6 — four of the seven landed C0 cells quote a line the tool never prints** (§3). The docs arm is
blind to it by construction. Patch: `cells-vs-c0.diff`.

**F7 — totals inside the amendment window run one above the deficits their own receipts show.**
`7de93ea` printed `total=3` with two arms short by one each (`grammar=8/9`, `note=8/9`);
`ee45944` and `51c315c` printed `total=1` with every arm at its maximum and `bad: {}`; `ae76985`
printed `total=0`. Same receipts, different verdicts: the extra point tracks the counter's own
edits, not a measured arm. Every run here is therefore quoted with a launch-time sha and its
receipt. Report-only — but if a deciding run lands in that window, its verdict line and its receipt
will disagree, and the receipt is the better record.

**F8 — conflict with the note seat's F1, reported verbatim.** `T55W1ScribeNote` stated
"registry-check declares none [no `ScratchRootUnusable`]". At `9cf0146`,
`tools/registry-check.py:757` declares `class ScratchRootUnusable(RuntimeError)` and both handlers
(`--selftest` at :1851, `--rev` at :1935); at the base `631cd64` the class does not exist (0 grep
hits). So the note's claim holds for the base tree, not for C0. No action needed on the cells, which
make no claim about Python types; the canonical adjudication is the L1's.

## 7. Limits — what this seat cannot see

- The docs arm tests only the marker substring in seven rows. `validate_cells.py` closes that for the
  claims it encodes (template shape, prefix equality with the measured token, the four required
  clauses); nothing automated proves a *future* mode keeps the class.
- The `/tmp` census clause is measured for the modes the counter traces; `registry-check --rev` is not
  traced by amendment, and the cell says so.
- The unset/empty arm is the resolver fact the note records (S278/S279); I did not re-derive CPython's
  candidate list here.
- Whether a caller parses the class by prefix or by the whole regex is outside both the counter and
  the cells; the cells quote the full line so both readings anchor on the same text.

## 8. Out of scope / not touched

No lane production file was edited; writes are only under `.ufo/waves/round-55/` (this seat's files).
The note, `SKILL.md`, the tool fixes, the counter amendments and the C0 commit belong to the L1 and
the other seats. All mutating git ran in a scratch clone after asserting
`git -C <clone> rev-parse --show-toplevel` equalled that clone. No tool install was needed
(`git`, `python3`, `strace`, `bwrap` present), so there is no install record.

## 9. Reproduction

    export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r55/T55W1ScribeCells
    L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
    mkdir -p "$S" && git clone -q --shared "$L" "$S/c0"
    git -C "$S/c0" checkout -q --detach 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
    python3 "$L/.ufo/waves/round-55/w1/T55W1ScribeCells-receipts/make_cells.py" \
        "$S/c0/tools/registry.json" "$S/c0/tools/registry.json.new"
    cp "$S/c0/tools/registry.json.new" "$S/c0/tools/registry.json"
    python3 "$L/.ufo/waves/round-55/w1/T55W1ScribeCells-receipts/validate_cells.py" \
        "$S/c0/tools/registry.json" \
        "$L/.ufo/waves/round-55/w1/T55W1ScribeCells-receipts/c0-grammar"
    mkdir -p "$S/work" && python3 "$L/.ufo/evidence/round-55/c2/measure.py" \
        --lane "$S/c0" --rev <commit-with-the-cells> --work "$S/work" --explain
