# Round-35 w2 — AttackStderrScope

Seat: `tameshi-r35-w2-AttackStderrScope` (leaf mutation-tester, godspeed). Dispatch lane tip
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (clone-verified; the fleet repo itself advanced to
`f9df589` mid-wave — see §8). All work under
`/fast/scratch/hyaku/tameshi-r35-seats/AttackStderrScope/`; the lane checkout is read-only and was
never written (proof in §6). No installs, no `pacman`, no subagents.

Axis: **the comparison scope of the runtime oracle** — the tuple is `(exit, FULL stdout)`; stderr is
captured separately and never compared. Two constructions were assigned (extra stderr line; move a
diagnostic from stderr to stdout). Both were built and measured, plus four adjacent probes on the
same scope boundary (stdout line structure, trailing bytes, the filesystem postcondition the stdout
line announces, and the harness's own stderr capture).

Frozen bytes used (verified in the lane at the dispatch tip; `sha256sum`):

| artifact | sha256 | pin |
|---|---|---|
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` | matches contract |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | matches contract |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` | matches contract |
| `d16f9b5` tool (predecessor) | `da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f` | historical |

## 1. The compared tuple, as implemented

- Tool `run_vectors` (`tally-audit-v3.py:376-399`): `out=$(tally … 2>"$TMPDIR/stderr.%i")` — stderr
  goes to a side file that is never read; stdout has its newlines replaced by `\x1f`, is split on
  `\t`, and has `\x1f` decoded back to `\n`. Comparison is `(rc, decoded stdout)` against `oracle()`
  (`:401-421`).
- Frozen counter `run_block` (`c1-measure.py:163-190`): `out=$(tally … 2>/dev/null)` — the same
  encoding, stderr **discarded**; `behavior`/`diverge` (`:204-217`) use only that tuple to decide
  kill vs accept.
- Both are deliberate and documented: tool docstring `:63` and `:379` ("stdout-only: stderr goes to a
  side file, never into the compared string (round-32 tool review M1)").
- The audited object is the **tally block** only: runner `:1994` extracts it from `$SELF`; counter
  docstring `:8-13` defines both specimen classes on "the copy's tally block".
- In the pristine block there is **no stderr surface at all**: 267 vectors × 4 configs = 1068 raw
  runs, `stderr` empty in every one (§3). The only stderr writes in the whole runner are
  `usage_exit`/`die_setup` (`:239-246`) and the python helper (`:324,425,437`) — all outside the
  block.

So the question is not "does v3 discard stderr" (it does, by design) but **whether stderr is
behavior-bearing anywhere in the runner's own contract**. It is: the runner's own `--selftest`
merges it into the string it compares.

## 2. Constructions (exact edits, byte-identical source + one edit each)

All copies are `cp` of the pinned runner (`pristine.sh` sha256 `a7d3f2dd…912eb9`), then one edit each:

| copy | edit (unified-diff hunk) | sha256 |
|---|---|---|
| M1-stderr-extra | after the tally loop: `+ printf 'REGRESSION_NOTE: counted=%s\n' "$((npass + nfail + nsetup))" >&2` | `9751084bb33fce7089e1411bc3e7800bd32a77304f279f0887df73dbdd263458` |
| M2-diesetup-stdout | `- printf 'MUTATE: SETUP (%s)\n' "$1" >&2` / `+ printf 'MUTATE: SETUP (%s)\n' "$1"` | `cd7719dcf7d3968a4683a865446ac4ef1133b094c9011c76d0fd66fad8c17f2c` |
| M3-us-sep-fail | FAIL verdict terminator `\n` → `\x1f` | `08e331159e4440fe8b875fa41e8188361e40eb130080b4c3c31b41dfea43015e` |
| M4-fail-line-to-stderr | FAIL branch `printf 'REGRESSION_WORKDIR…' "$root"` → `… "$root" >&2` | `f584630a00c1e044d8d87ef88d019eec99c627f68ece7273a02b6a4bc86f5572` |
| M5-no-remove | PASS branch: delete `rm -rf "$root"` (keep the `(removed on PASS; --keep retains)` print) | `1d3d121d43533e989f657998aad3751bbfd50ee397f6eeb8b629ae9fb2b80020` |
| M6-harness-no-stderr | `tally_line`: `out=$(bash "$root/tally.sh" 2>&1)` → `out=$(bash "$root/tally.sh")` | `896e6d0b29d823972d5a6d5461d4cb72749f5f9347ec4627b571c0d4acb756b3` |
| M6M1-harness-blind | M6 edit applied on top of M1 | `7ce78238abccbcd456c21927514c25dc9c8d22b218cf46b3a307e31b3aa83ad4` |
| M7-extra-stdout-line | before `exit 0`: `+ printf 'REGRESSION_TRACE: done\n'` (stdout) | `c818725f0415b4835af5b14fae154d142d30eb401cb29efe92f0e0e50f0b2a12` |
| M8-trailing-newline | before `exit 0`: `+ printf '\n'` (stdout) | `1c68825148ec44b75e68f859a919816908be37f66ab6f3df2b5447e12a4615ac` |

Detector: `work/detect.py` (independent of the tool under test; imports only the frozen counter's
block/leg extraction, `CONFIGS`, `vectors_for`, `behavior`/`diverge`). It runs each
(copy, config, vector) in its own bash process with its **own** real root
`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` for the two auto triples (one root per run, as
`mutate-and-run.sh:1357-1365` does), and compares **raw bytes**: exit, full stdout, full stderr, and
the workdir-existence postcondition (root string normalised to `<ROOT>` before comparison).
Vectors: 267 (all-zero, every status 0..255 at leg 0, one-1/one-2/one-3/one-255, two-mixed) × 4
configs.

## 3. Results matrix

| copy | frozen-counter class | raw byte diffs (267 vec × 4 cfg) | v3 verdict |
|---|---|---|---|
| pristine | — | 1068/1068 runs: stderr empty; PASS vector removes root | `TALLY_AUDIT: PASS` rc 0 |
| M1-stderr-extra | **identical** (accept) | stderr **1068/1068**; stdout 0; exit 0; rootstate 0 | **PASS, rc 0** |
| M2-diesetup-stdout | **identical** (accept) | 0/0/0/0 (block unchanged) | **PASS, rc 0** |
| M3-us-sep-fail | **identical** | stdout **24** (6 failing vectors × 4 cfg), same length, `\n`→`\x1f` | **PASS, rc 0** |
| M4-fail-line-to-stderr | **DIVERGED** (all 4 cfgs) | stdout 24, stderr 24 | **FAIL** rc 1, `runtime` only, mismatched=3600 |
| M5-no-remove | **identical** (accept) | rootstate **2** (the two all-zero vectors, cfg (1,0)); stdout/exit 0 | **PASS, rc 0** |
| M6-harness-no-stderr | identical | 0/0/0/0 | **PASS, rc 0** |
| M6M1-harness-blind | identical | stderr differs (M1 note); runner selftest green (§4.5) | **PASS, rc 0** |
| M7-extra-stdout-line | **DIVERGED** (all 4 cfgs) | stdout 8 | **FAIL** rc 1, `runtime` only, mismatched=40 |
| M8-trailing-newline | identical | stdout 8 (len 142→143) | **PASS, rc 0** |

Assignment-minimum vectors for the two assigned constructions (cfg `(auto,KEEP)`; `E` = stderr
differs, `X` = rootstate differs, `O` = stdout differs, `-` = identical):

```
M1  all-zero :E E E E   one-1:E E E E   one-2:E E E E   one-3:E E E E   one-255:E E E E   two-mixed:E E E E
M2  all-zero :- - - -   one-1:- - - -   one-2:- - - -   one-3:- - - -   one-255:- - - -   two-mixed:- - - -
M4  all-zero :- - - -   one-1:O+E all   one-2:- - - -   one-3:- - - -   one-255:- - - -   two-mixed:O+E all
M5  all-zero :X at (1,0), - at (1,1),(0,1),(0,0);  the other five vectors identical everywhere
```

## 4. Findings

### BOUND-1 (assigned construction 1) — a block-local stderr write is invisible to v3 *and* to the frozen counter, although the runner's own `--selftest` compares it

M1 adds a diagnostic line to fd 2 after the tally loop. v3 accepts:

```
$ python3 /fast/scratch/hyaku/tameshi-r35-seats/AttackStderrScope/lane/tools/tally-audit-v3.py \
    --runner /fast/…/AttackStderrScope/work/M1-stderr-extra.sh ; echo EXIT=$?
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
EXIT=0
```

The frozen counter also classifies it as behaviorally identical (`div=-`, §3) and would admit it as a
**valid accept specimen** (`c1-measure.py:12-13`, `:204-217`, `:2>/dev/null` at `:171`).

**Contract clause that makes this a real divergence:** the runner's own selftest extracts the tally
block from `$SELF` (`mutate-and-run.sh:1994`) and merges streams into the string it compares:

```
2003      '  local root=selftest-tally auto=0 KEEP=1' "$tblock" '}' 'tally' >"$root/tally.sh"
2004      out=$(bash "$root/tally.sh" 2>&1)
2006      [[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]]
```

Live, same bytes, same host:

```
$ bash work/pristine.sh --selftest     -> MUTATE_SELFTEST: 106/106 pass   VERDICT: PASS        EXIT=0
$ bash work/M1-stderr-extra.sh --selftest -> MUTATE_SELFTEST:  98/106 pass VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.e8bhx5)  EXIT=1
```

All eight tally-harness cases turn red (the merged first line is `REGRESSION_NOTE: …`):
`diff st.pristine.out st.M1-stderr-extra.out` — lines 96-103, e.g.
`PASS tally harness: all nine legs pass -> …` → `FAIL …`. `--selftest` is part of the runner's
documented contract (`mutate-and-run.sh:151`, `VERDICT: PASS`/exit 0). So the copy is a runner that
**fails its own gate**, and the audit blesses it.

Why BOUND, not CRITICAL: the frozen counting rule defines kill/accept on the block's
`(exit, FULL stdout)` tuple (`contract.json` C1 `count` rule; `c1-measure.py:8-13`), and under that
rule M1 *is* an accept specimen, so C1's predicate is not literally falsified. But the predicate's
sentence ("accepts every accept specimen (behaviorally identical on every config and vector)") is
false for M1 at the runner level, and the counter cannot see it; if a sealed seat authors this class
as KILL the counter marks it `INVALID` (fail-closed), and if authored as ACCEPT it is admitted and
blessed (fail-open). The sealed set therefore **cannot encode the wider contract** while the tuple
stays `(exit, stdout)`.

Cheap, targeted fix (two lines, no contract redefinition): `run_harness` already receives the copy's
harness section; add one `run_harness(runner_path, sec, extracts, <copy's own block>, tmp)` call and
require `failed == 0`. The copy's harness merges stderr, so M1 fails there. Alternatively add a fifth
check `bash <copy> --selftest` (`TIMEOUT`-bounded, expects exit 0 + `VERDICT: PASS`), which also
covers M5's class of latent breakage. If instead the tuple itself is widened, `tally-audit-v3.py:392`
and `c1-measure.py:171` must change in lock-step or tool and counter disagree.

### BOUND-2 (assigned construction 2) — a moved stderr diagnostic is accepted, but the runner's documented contract does **not** pin that stream; the move is outside the audited object

M2 removes `>&2` from `die_setup()` (`mutate-and-run.sh:244-245`). v3 PASS (rc 0, all four checks).
Live refusal path (PATH holding only `readlink`, so the first guard `command -v python3` fires):

```
$ env -i PATH=/tmp/ss-bin HOME=/tmp TMPDIR=/tmp /bin/bash work/pristine.sh --regression
EXIT=2  stdout: <empty>   stderr: MUTATE: SETUP (python3 missing)
$ env -i PATH=/tmp/ss-bin HOME=/tmp TMPDIR=/tmp /bin/bash work/M2-diesetup-stdout.sh --regression
EXIT=2  stdout: MUTATE: SETUP (python3 missing)   stderr: <empty>
```

So the SETUP reason moves between streams, observably. But the honest label: **not established as a
contract violation.** The header lists `MUTATE: SETUP (<reason>)` among the verdict lines
(`:78`) without naming a stream, and the runner's own refusal assertion captures `2>&1`
(`:1591-1593`), so the selftest does not distinguish either (M2 `--selftest` = 106/106 PASS, EXIT=0).
It is a capability limit of the *object*: `die_setup`/`usage_exit` are defined before
`run_regression`, outside `regression_body`, and the audit executes only the extracted block — a
whole-file copy can rewrite every diagnostic outside the block and pass. Ranked HYGIENE-1 below for
that reason, not BOUND.

### BOUND-3 — the compared tuple omits the filesystem postcondition that the compared stdout line announces

M5 deletes `rm -rf "$root"` but keeps `printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\n'`.
v3 PASS (rc 0). Counter class: identical. Raw detector, cfg (1,0), all-zero vector:

```
pristine: rc=0 exists=absent   out='REGRESSION: PASS (…)\nREGRESSION_WORKDIR: <ROOT> (removed on PASS; --keep retains)\n'
copy    : rc=0 exists=present  out=<byte-identical>
```

**Contract clause:** `mutate-and-run.sh:141-143` — "Scratch root: `mktemp -d
/tmp/tameshi-r4-2-regression.XXXXXX` by default; **removed on PASS unless --keep**, kept on
FAIL/SETUP, never removed when `--workdir` was given." The stdout line the oracle *does* compare is
the claim; the side effect it describes is not in the tuple. This is a plausible refactor defect
(dead-looking `rm` dropped while the message stays) and it is inside the audited block.

Fix note with a trap: the tool memoises one root per audit (`AUTO_ROOT`/`auto_root()`,
`tally-audit-v3.py:351-367`; `run_vectors` reuses it for every vector), so after the first PASS the
root is gone and every later PASS vector `rm`s a nonexistent path — a naive post-check would only
catch the first PASS vector and would pass M5 on the rest. The witness must create **one fresh real
root per vector** (as the real runner does per invocation) and compare `isdir(root)` against the
triple's expected kept/removed decision. The counter's `run_block` needs the same change, or
M5-class copies remain misclassified as accept.

### HYGIENE-1 — "FULL stdout" is a lossy encoding, not the stdout bytes

Three independent losses, all exercised:

- `\n`↔`\x1f` collision (M3): the tool encodes newlines to `\x1f` and decodes them back, so a copy
  that emits a literal `0x1F` where the pristine emits `\n` compares equal. Raw proof, cfg (1,0),
  vector `1 0 0 …`: pristine `sha=cc13e9bc00c55267 len=87 tail='…setup=0)\nREGRESSION_WORKDIR: <ROOT> (kept)\n'`;
  M3 `sha=f52f50dd94349f03 len=87 tail='…setup=0)\x1fREGRESSION_WORKDIR: <ROOT> (kept)\n'`.
  v3 PASS; counter identical. The two records are now one physical line, so a line consumer
  (`grep '^REGRESSION_WORKDIR:'`, the header's `Lines:` vocabulary at `:140-143`) loses the workdir
  line. Defect plausibility is low (no natural edit produces `0x1F`), hence HYGIENE.
- Trailing newline (M8): `$()` strips all trailing newlines, so an extra final `\n` is invisible.
  Raw: pristine `len=142 sha=8e8956ab45f248d3 tail='…(removed on PASS; --keep retains)\n'`;
  M8 `len=143 sha=3eb8f0e2acc68642 tail='…(removed on PASS; --keep retains)\n\n'`. v3 PASS (rc 0).
- NUL: bash 5.3.20 command substitution silently drops NUL bytes
  (`y=$(printf 'A\0B')` → warning `ignored null byte in input`, value `AB`), so a NUL inside stdout
  is also outside the compared string. Probe: `printf 'A\x1fB\n' | od -c` → `A 037 B \n`.

Fix: compare a lossless encoding (base64 of raw stdout, or its hash) in both `run_vectors` and
`run_block`. This does not change any current panel verdict; it makes the clause "FULL stdout"
literally true.

### HYGIENE-2 — the harness check cannot certify the harness's stderr capture

v3's `harness` check runs the **copy's** harness section against a panel of 34 faults built from the
tool's `REF_BLOCK` (`tally-audit-v3.py:638-679`); it never feeds the copy's own block to the harness,
and no panel fault writes to stderr.

- M6 (`tally_line` drops `2>&1`, runner `:2004`): v3 `CHECK harness PASS … faults rejected=34/34`,
  `TALLY_AUDIT: PASS` rc 0; runner `--selftest` 106/106 PASS (latent — nothing observes it today).
- M6M1 (M6 + M1's note): v3 PASS rc 0; runner `--selftest` **106/106 PASS**, and
  `diff st.pristine.out st.M6M1-harness-blind.out` is empty — the weakened harness masks exactly the
  class that is 98/106 RED under the pristine harness.

The docstring bounds the certified classes: "A weakened harness (exit only, swallowed status, a
skipped position or vector, a skipped guard stress) accepts at least one fault"
(`tally-audit-v3.py:80-81`) — "swallowed stderr" is not among them, and v3's own `--selftest` has no
stderr case (grep: the only stderr mentions are the docstring and the `run_vectors` side-file line).
Fix: add a `faults()` entry whose only edit is a stderr write in `REF_BLOCK`, and one stderr seed in
v3's own selftest.

## 5. What I could NOT break (with proof)

1. **A block-local stdout divergence is killed, with failing check exactly `runtime`.**
   M4 (FAIL branch's `REGRESSION_WORKDIR` line moved to stderr): `EXIT=1`,
   `CHECK runtime FAIL vectors=30316 mismatched=3600; first: cfg(1,0) statuses 1 0 …: got 1
   'REGRESSION: FAIL (…)', want 1 'REGRESSION: FAIL (…) | REGRESSION_WORKDIR:
   /tmp/tameshi-r4-2-regression.9wwer0go (kept)'`; all other checks PASS; counter `DIVERGED` on all
   four configs. M7 (a plain extra ASCII stdout line): `EXIT=1`, `runtime FAIL … mismatched=40`;
   counter `DIVERGED` all four. So the reversal of the assigned mutant ("move a diagnostic from
   stdout to stderr") is exactly what the full-line comparison is built to catch.
2. **Every stderr-only change leaves `(exit, stdout)` untouched.** M1: exit and stdout identical on
   1068/1068 runs; the divergence is exclusively in the runner's own merged-stream selftest. If the
   contract is read as `(exit, stdout)` only, v3's acceptance of M1 is correct and documented
   (`:63`, `:379`) — the finding is that the runner's contract is wider than that tuple.
3. **The pristine block has no stderr surface**: 1068/1068 runs with `stderr == b''`; therefore the
   stderr class exists only for copies that add one, and no current panel/sealed specimen can
   accidentally trip it.
4. **A gate that mutates or branches on `$root`** is outside this seat's axis (A4 landed); my
   detector used real per-run roots and every mutant here is root-independent, so no root-keyed
   behaviour was re-litigated.
5. **The lane and frozen bytes are intact**: `git -C lane status --porcelain` = 0 lines;
   `rev-parse HEAD` = `7da6e07…7e5b`; tool/runner/counter hashes = pins (table above), before and
   after every probe.

## 6. Immutability / restoration

- The lane checkout was **never written** (read-only per tasking): `git status --porcelain | wc -l`
  = `0` after all probes; the three frozen artifact hashes match their pins.
- No file under `/home/vgpnk/Projects/shokunin/` was written except this report. No git/jj mutation
  was run (only `clone`, `checkout --detach`, `rev-parse`, `status`, `ls-tree`, `log`, `show` in the
  scratch clone / read-only queries against the lane).
- Mutants live only under `/fast/scratch/…/AttackStderrScope/work/` (disposable scratch; hashes in
  §2). The `--selftest` scratch dir that M1 kept (`/tmp/tameshi-r4-2-selftest.e8bhx5`) was removed
  after capture; all other selftests removed their own roots on PASS.
- Tool transcripts are retained at `work/tool.<copy>.out` (and `.err`), selftests at
  `work/st.<copy>.out`.

## 7. Round-36 tightening (ordered by cost)

1. **Add the copy's block to the harness check** (one `run_harness(…, block, …)` call, require
   `failed == 0`) — closes BOUND-1 and HYGIENE-2's mask at near-zero cost.
2. **Filesystem postcondition**: fresh per-vector root + `isdir(root)` in `run_vectors`
   *and* `run_block` — closes BOUND-3. Note the shared-root trap (`AUTO_ROOT` memoisation).
3. **Lossless stdout**: base64/hash raw stdout instead of `\n`→`\x1f` in both tool and counter —
   closes HYGIENE-1 (byte-level "FULL stdout").
4. **Harness stream fault**: add a stderr-writing `REF_BLOCK` fault to `faults()` and a stderr case
   to v3's `--selftest`.
5. If the contract's meaning of "behavior" is meant to include stderr, amend the counting rule
   (A7) *before* the deciding run and change tool+counter in the same commit; otherwise state in the
   contract that the tuple is `(exit, stdout)` deliberately, so this class is a known, accepted
   limit rather than an unstated one.

## 8. Notes

- The fleet repo advanced during this wave (`f9df589`, A6: counter `TOOL_SHA256` re-pinned to the A4
  bytes). My clone stays at the dispatch tip `7da6e07` as tasking requires; no verdict here depends
  on the counter's `TOOL_SHA256` (the detector imports only the block/vector/ground-truth helpers).
- The A6 class (stale counter tool pin, caught by wave-2 seat CriticPredicate) and the A4/A5 classes
  (root witness, sealed provenance) are **not** re-litigated by this seat.
- External commands used: `bash 5.3.20`, `python3`, `git`, `od`, `diff`, `sha256sum`, `mktemp`.
  Nothing installed.
