# T54W2Exec02 — C2 counter (operability) at C1

**Item.** Run and record the C2 counter at `C1 = 99c3bc88d704566197783f66b211ee0a830e0330`
in lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; the claim must print
`C2_R54_PASS=true`, otherwise name the failing arm and paste its `EXPLAIN` line.

**Verdict: PASS. `C2_R54_PASS=true`, exit 0, `total=0`.** The counter was run twice with
identical `EXPLAIN` lines and an identical verdict line; the receipt holds the second run,
which was unpiped so its `RC=0` is the counter's own exit status (the first run's status was
masked by a `tail` pipe and is not relied on). All five arms were then re-measured without the
counter's aggregation (`receipts/arms-census.txt`).

## 1. Instrument identity (frozen bytes actually executed)

```
$ sha256sum .ufo/evidence/round-54/c2/measure.py
49280fe55bd9361c284ddb1b9e757fd3ec3267f60eed4ca587e1bfe446b718c8
$ python3 -c 'import json;print(json.load(open(".ufo/evidence/round-54/freeze.json"))["files"]["c2/measure.py"])'
49280fe55bd9361c284ddb1b9e757fd3ec3267f60eed4ca587e1bfe446b718c8   # MATCH
```

The `c2/measure.py` body is unchanged across the mid-wave re-freezes:
`git diff --quiet 097985c..HEAD -- .ufo/evidence/round-54/c2/measure.py` →
`UNCHANGED` (HEAD moved to `4e2de73`, amendment 3, which touched `c1/measure.py`,
`contract.json`, `freeze.json`, `QUALITY.md`, the note and the lesson only).
The amendment-2 body is therefore what ran; the pre-amendment copy committed inside
C1 is `b4684a3f555e8cbfda6fc9c7208827a3816a60cf53186269fdec41d5025e9e49`, which is the
disclosed amendment-2 delta and not a hidden edit.

The counter reads the note and the lesson **from the revision**
(`show(lane, rev, NOTE)` / `show(lane, rev, LESSON)`), so the 12:00:39 worktree edits to
`corpus/knowledge/scratch-root-contract.md` and `corpus/lessons/round-54.md` cannot have
influenced the arms measured below.

## 2. Command and output

`--work EMPTY` in the seat item is the placeholder for an *empty* directory: the counter
does `work.mkdir(parents=True)` and then refuses if `any(work.iterdir())`, cloning the lane
inside it. Passing the literal token `EMPTY` from the fleet-root cwd would create a
fleet-root directory, so the placeholder was resolved to an absolute empty dir in scratch
(host guard).

```console
$ export HYAKU_SCRATCH=/fast/scratch/hyaku
$ export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Exec02
$ S=/fast/scratch/hyaku/tameshi-r54/T54W2Exec02; mkdir -p "$S/work-c2b"
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 .ufo/evidence/round-54/c2/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 99c3bc88d704566197783f66b211ee0a830e0330 \
    --work "$S/work-c2b" --explain
```

Full stdout (`receipts/c2-run-at-C1.txt`, sha256 `91f06f6f51a9896afa8fd83e24651d7a6a30799939a122b9dc0c440bfeded677`):

```
EXPLAIN unusable registry-check rc=2 line='registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory'
EXPLAIN unusable env-diff rc=2 line='ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory:'
EXPLAIN unusable bash-witness-study rc=2 line='WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory:'
EXPLAIN unusable evidence-disposition rc=2 line='evidence-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable '
EXPLAIN unusable pin-disposition rc=2 line='pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable direc'
EXPLAIN unusable context-capture rc=2 line='SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable di'
EXPLAIN unusable repeat-control rc=2 line='repeat-control: setup: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable director'
C2_R54: rev=99c3bc88d704 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
RC=0
```

No arm failed, so there is no failing `EXPLAIN` line to name: every `EXPLAIN` line above is
the per-tool evidence *for* a passing unusable arm (`rc=2`), and the counter emits an
`EXPLAIN empty …` / `EXPLAIN usable …` line only when that arm loses a tool — none appeared.
Session note on the `EXPLAIN` text: the last-line echo is truncated at 120 chars and so
cuts before the quoted value; the value **is** in the message proper, which is what the
`naming` arm reads — see §3.

## 3. Arm-by-arm, counter vs. independent re-measurement

Independent census (`receipts/run-arms-census.sh`, output `receipts/arms-census.txt`):
own `git clone --shared` of the lane at C1 under scratch, toplevel asserted
(`fixture-toplevel-ok: /fast/scratch/hyaku/tameshi-r54/T54W2Exec02/census-clone`), the
unusable path asserted absent (`unusable path exists: no-good`), then each tool driven
directly.

| Arm | Counter | Independent | Evidence |
|---|---|---|---|
| unusable → exit 2 | `unusable_exit2=7` | 7/7 `rc=2` | each self-test prints `could-not-evaluate`, the quoted path, and `(could-not-evaluate)` on one line |
| names the TMPDIR value | `naming=7` | 7/7 (`names_value=1`) | e.g. `... TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W2Exec02/work-c2/unusable-tmpdir-r54' (could-not-evaluate)` |
| no traceback | (folded into `unusable_exit2`) | 7/7 `tracebacks=0` | `grep -c 'Traceback (most recent call last)'` = 0 for all seven |
| `TMPDIR=""` → exit 0 | `empty_ok=7` | 7/7 `empty_rc=0` | empty string resolves as unset (note arm cites S278/S279) |
| usable root → exit 0 | `usable_ok=7` | 7/7 `usable_rc=0` | plain run, per amendment 2 |
| no `mkdir` under `/tmp` | `tmp_mkdirs=0` | 0 under both regexes | `frozen=0 repaired=0` on all seven traces |
| `scratch_root` cells | `docs=7` | 7/7 rows | every row's cell is the identical sentence naming `TMPDIR`, `empty` and `could-not-evaluate`: ``TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 54, corpus/knowledge/scratch-root-contract.md)`` |
| note exists/cites a mined S row | `note=1 sources=3` | confirmed | note cites S277, S278, S279; `/tmp`-free |
| lesson Gate names a cited S id + URL + date | `sources=3` | confirmed | `corpus/SOURCES.md` rows S277/S278/S279 each carry cell 8 `mined` and cell 11 `corpus/knowledge/scratch-root-contract.md`; the lesson `## Gate` names S277 with `https://pubs.opengroup.org/…V1_chap08.html` and `opened 2026-10-28` |

Delta against the claim's `before` (`.ufo/evidence/round-54/before/c2.stdout`, read directly):

```
C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false
```

so the C1 delta is `unusable_exit2 3→7`, `docs 0→7`, `note 0→1`, `sources 0→3`, `total 13→0` —
exactly the four arms the round was supposed to move, with `naming`/`empty_ok`/`usable_ok`/
`tmp_mkdirs` held.

## 4. F1 — instrument defect found (does not flip the verdict at C1): the `/tmp` census regex cannot match a plain `mkdir`

Attack target: the frozen `c2/measure.py` arm 3 census, line 142:

```
142:        hits = len(re.findall(r'mkdir(?:at)\([^)]*"/tmp', log.read_text(errors='replace')))
```

`(?:at)` is a **required** non-capturing group, not an optional one, so the pattern matches
`mkdirat(` only — never `mkdir(`. On Linux `os.mkdir`/`os.makedirs`/`tempfile.mkdtemp` issue the
plain `mkdir(2)` syscall, so the exact regression this arm exists to catch (round 53's
`dir="/tmp"` fallback) would allocate `/tmp` with `mkdir(` and score **0 hits**.

Runnable receipt: `receipts/run-ctl-pos.sh` (fixture `receipts/probe-mkdir-tmp.py`) runs a
probe that creates one directory under `/tmp` through `os.makedirs`, under the counter's own
strace vector, then lifts the regex literal **out of the frozen file**:

```console
$ bash .ufo/waves/round-54/w2/T54W2Exec02-receipts/run-ctl-pos.sh
strace_rc=0 target=/tmp/T54W2Exec02-probe-207737
--- strace log ---
207767 mkdir("/tmp/T54W2Exec02-probe-207737", 0777) = 0
207767 +++ exited with 0 +++
--- census ---
FROZEN LINE: hits = len(re.findall(r'mkdir(?:at)\([^)]*"/tmp', log.read_text(errors='replace')))
EXTRACTED REGEX: r'mkdir(?:at)\([^)]*"/tmp'
FROZEN HITS  : 0
REPAIRED     : mkdir(?:at)?\([^)]*"/tmp -> 1
```

(`receipts/ctl-pos.out.txt`.) The syscall census over the real run's seven traces shows why
this is not academic: `2750 mkdir(` vs `344 mkdirat(` — the vast majority of calls are in the
form the regex cannot see.

Why the **C2 verdict at C1 still stands**: the arm's substance is "no `mkdir` under `/tmp`",
and that holds under the repaired regex too — `frozen=0 repaired=0` on every one of the seven
traces, re-measured independently (`receipts/arms-census.txt`, last block). So `tmp_mkdirs=0`
is a true reading, not an artefact of the bug. The defect is a latent **false-negative** in a
*frozen* instrument: it leaves the arm unable to fire on the class it names, so the round-53
fallback could return unnoticed and this counter would still print `tmp_mkdirs=0`. The note's
own falsifier (present in C1's bytes: "A tool that regains a `dir="/tmp"` literal fails the
round-53 monitor and the C2 `tmp_mkdirs` arm together") is therefore not reachable through the
C2 half today. Reported,
not fixed: the file is frozen and outside this seat's write scope; adjudication is L1's.

## 5. Observations adjacent to the claim (residues and conditioning, none claim-defeating)

- **`EXPLAIN` line truncation.** `text.strip().splitlines()[-1][:120]` cuts the last line
  before the quoted value for five of the seven tools. The `naming` predicate reads the whole
  `stdout+stderr`, and the value is present in every tool's message (§3), so no arm is
  weakened; only the human-facing echo is shortened.
- **`TMP`/`TEMP` are inherited, not stripped.** `run_tool` overrides `TMPDIR` only. On this
  host both are unset (`TMP=[<unset>] TEMP=[<unset>]`, so `tempfile.gettempdir()` is the
  arm's own value), which is what makes the `""` arm mean "platform default". On a host with
  `TEMP` set the empty arm would still exit 0 but would no longer demonstrate the documented
  resolver order. Conditioning, not a finding at C1.
- **`context-capture` prefixes the could-not-evaluate line with a verdict token.**
  At C1 it prints `SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch
  under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate))`
  — rc 2, class present, value present, no traceback, so the claim's named arms hold, but the
  literal token `FAIL` is a *verdict* in front of a line that declares no verdict may be
  printed. This is not a new discovery: the note at HEAD names exactly this residue and routes
  it to round 55 (`git diff 99c3bc88d704…HEAD -- corpus/knowledge/scratch-root-contract.md`,
  added by `8da3539`), and the C1 bytes predate that sentence. Recorded so the C1 reading is
  attributed correctly: the residue exists at C1, is adjudicated after C1, and `repeat-control`
  shows the same shape (`repeat-control: setup: RuntimeError: …`).

## 6. Artifacts opened

- `.ufo/evidence/round-54/c2/measure.py` (frozen instrument; read in full, lines 40–200 and 1–39).
- `.ufo/evidence/round-54/contract.json` (C2 row: target, kill rule, `before`, `cannot_see`).
- `.ufo/evidence/round-54/freeze.json` (digest of `c2/measure.py` and the amendment log).
- `.ufo/evidence/round-54/before/c2.stdout` (the claim's `before` reading).
- `tools/registry.json` at C1 (seven `scratch_root` cells).
- `corpus/knowledge/scratch-root-contract.md` at C1 (three arms, falsifier, blind spot).
- `corpus/lessons/round-54.md` at C1 (`## Gate`, S277/S278/S279 with URLs and 2026-10-28).
- `corpus/SOURCES.md` at C1 (rows S275–S279 state).
- The seven tools' self-test output at C1 (via the C1 clone).

## 7. Exact retained evidence

| File | What it is |
|---|---|
| `receipts/c2-run-at-C1.txt` | full counter stdout+rc at C1 (the run quoted in §2) |
| `receipts/arms-census.txt` | independent per-tool census of all five arms + the dual-regex `/tmp` count |
| `receipts/c2-run-at-C1.txt` sha256 | `91f06f6f51a9896afa8fd83e24651d7a6a30799939a122b9dc0c440bfeded677` |
| `receipts/run-arms-census.sh` | the driver that reproduced the census |
| `receipts/run-ctl-pos.sh`, `receipts/probe-mkdir-tmp.py`, `receipts/ctl-pos.out.txt`, `receipts/ctl-pos-strace.log` | F1 positive control, runnable |
| `receipts/strace-*.log` (7) | the counter's own strace logs of the usable arm, from the passing run |

Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Exec02/` (counter work dirs `work-c2`, `work-c2b`,
`census-clone`; `TMPDIR` pointed there for every run). No lane file edited; no mutating git
command run in the lane; the only clones are `git clone --shared` under that scratch, with
`git -C "$D" rev-parse --show-toplevel` asserted before use.

**Tooling.** Nothing installed or upgraded; no `pacman`, `uv`, `npx` or PATH write (pacman is
paused host-wide per the operator note). Tools used: `strace 6.x` (`/usr/bin/strace`),
`python3 3.14.8`, `git`.

## 8. Risks / blockers

- **None blocking.** The claim measures PASS at C1 and every arm reproduces independently.
- **F1 (above)** is an adjudication input for L1: a one-character repair
  (`(?:at)` → `(?:at)?`) would restore the arm's ability to fire, but changing it now is a
  fourth amendment to a frozen instrument and is outside this seat's scope.
- The lane's HEAD advanced to `4e2de73` (amendment 3) *during* this verification; `c2/measure.py`
  is unchanged by it, and the note/lesson arms read C1's bytes, so nothing here is stale.
