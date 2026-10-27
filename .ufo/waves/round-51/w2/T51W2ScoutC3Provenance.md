# T51W2ScoutC3Provenance — why `round21-measure.py --selftest` is red in the C3 counter's clone

Seat scout, wave 2, round 51. Read-only on the lane (bytes via `git show 6d8c11e3:<path>`); all runs in
scratch `--shared` clones of the lane at CAND `6d8c11e378aa90b12650808e1b79270742935f15`
(toplevel asserted before checkout). `tools/round21-measure.py` blob is `24a36fec…` at both BASE
`9962033` and CAND (unchanged by the round). Scratch deleted before yield.

## Verdict (one paragraph)

`--selftest` computes the lane root as `Path(__file__).resolve().parents[1]` and then reads
the pinned blobs of the frozen C2 contract from **`ROOT.parent / surface["repo"]`**, i.e. from
sibling directories next to the lane. The contract pins surfaces in five repos
(`tameshi-shokunin`, `kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`).
In the lane, `ROOT.parent` is the fleet root, so all five resolve. In the C3 counter's clone,
`ROOT` is `WORK/tameshi-shokunin` (measure.py:195) so `ROOT.parent` is `WORK`, and only the
`tameshi-shokunin` pin resolves (to the clone itself); the second surface (`kumitate-shokunin`)
raises `CalledProcessError` (git rc 128) at line 74 and Python exits 1 with a traceback. Nothing in the
row can change this: the dependency is in the tool, not in the row text.

## Exact repo-root calculation and hardcoded dependencies (CAND bytes)

| Where | Code | Effect |
|---|---|---|
| `tools/round21-measure.py:21` | `ROOT = Path(__file__).resolve().parents[1]` | repo root = grandparent of the script's real path (symlinks resolved) |
| `:22` | `EVIDENCE = ROOT / ".ufo/evidence/round-21"` | delegates and contract read from the *clone's* own bytes (fine, frozen files are in-tree) |
| `:73-76` | `subprocess.run(["git","-C",str(ROOT.parent / surface["repo"]),"show", surface["rev"]+":"+surface["path"]], env=env, capture_output=True, check=True)` | **hardcoded fleet-sibling layout**: expects `<parent-of-lane>/<repo>` for every frozen surface repo; `check=True` + `capture_output=True` so git's "cannot change to … No such file" is swallowed and the only symptom is a traceback naming the path |
| `:72` | `frozen = json.loads((EVIDENCE/"c2-contract.json").read_text())` | surfaces list: tameshi-runner (tameshi-shokunin @08175c62 `tools/mutate-and-run.sh`), js-kimi-census/js-claims-check (kumitate), js-round-gate, js-sources-check (kumitate), bash-surface-census/bash-checklist-run (kagi), bash-tsukuroi-census (tsukuroi), bash-mado-verify (mado) — 9 surfaces, 5 repos |
| `.ufo/evidence/round-21/c2-count.py:19` | `FLEET = Path("/home/vgpnk/Projects/shokunin")` (absolute, frozen delegate) | second, independent dependency: the delegate `c2-count` reads pins via `FLEET / frozen["repo"]` (line 52), regardless of cwd/clone location |
| `c2-count.py:17` | `HERE = Path(__file__).resolve().parent` | delegate's own contract path, in-tree (fine) |
| `c1-survivors.py` | no sibling/fleet reference (`__file__` only for its own hash) | C1 half of selftest has no fleet dependency |

So there are **two layers**: (1) the facade's relative `ROOT.parent` (breaks in any non-fleet clone,
crashes before any case runs); (2) the frozen delegate's absolute `FLEET` (breaks on any host lacking
`/home/vgpnk/Projects/shokunin` with those revs, and is what makes a clone run read the *live* lane).

## Reproductions (scratch, `TMPDIR` explicit, stdin /dev/null)

1. **Counter-shaped layout** — `S/a/tameshi-shokunin` (shared clone, detached at CAND), parent `S/a`
   containing nothing else: `python3 tools/round21-measure.py --selftest` →
   no `MEASURE_CASE` line is printed (crash precedes `c1-killed`), traceback ends
   `CalledProcessError: Command '['git','-C','…/a/kumitate-shokunin','show','175de6ba…:scripts/kimi-census.mjs']' returned non-zero exit status 128`, **RC=1**.
   Surface 1 (`tameshi-runner`) did *not* fail: `ROOT.parent/tameshi-shokunin` is the clone itself and
   `08175c62` is reachable through the shared alternates.
2. **Sibling-resolvable layout** — same clone, parent `S/b` additionally holding symlinks
   `kumitate/kagi/tsukuroi/mado-shokunin → /home/vgpnk/Projects/shokunin/<repo>` (scratch only; fleet repos
   untouched, symlinks used solely to isolate the cause, not proposed as a row/shim): all 13
   `MEASURE_CASE … PASS`, `ROUND21_MEASURE_SELFTEST: 13/13 pass`, **RC=0**, 1.9 s.
3. **Counterfactual one-line change** (scratch copy of the tool, reverted with `git checkout`): replacing
   `str(ROOT.parent / surface["repo"])` by `"/home/vgpnk/Projects/shokunin/" + surface["repo"]` in layout 1
   → 13/13 pass, RC=0. This shows layer (1) is the only thing failing in the counter's clone, and that
   layer (2) is already satisfied there because the delegate uses the absolute `FLEET`.

Consistency with w1: `T51CritC3Counter.md` records the counter's own result for this row as
`selftest-exit=1` (fixture B) and that an `--help --selftest` alias is the only way to turn it green; my
layout 1 reproduces that exit code without the counter, and layout 2 shows the genuine tool is green when
siblings resolve. The tool's selftest is therefore truthful in both layouts (it measures C1/C2 against fleet
pins); what is wrong is its environment contract.

## Calibration notes / what the lane already says

- The lane already discloses layer (2): SKILL.md:2088-2100 (Round 28 correction) says `c2-count.py` hardcodes
  `FLEET` (line 19, used line 52) so facade runs "read the live lane's Git objects even when run from a
  clone". That text is accurate for `--claim c2` and for `--selftest` **when siblings resolve**; it does
  **not** mention layer (1), and it understates the clone outcome: from a clone with no sibling repos the
  selftest does not read live objects, it **crashes with exit 1** (not the documented `2 could-not-evaluate`,
  SKILL.md:1977 / round-21 docstring lines 7-8). SKILL.md:2076-2078 also says only that
  `round21-measure-selftest` "additionally read[s] live sibling object stores".
- The exit 1 is an incidental uncaught-exception code, not the tool's documented "1 failed". A row that
  says `0 clean; 1 failed` for this tool is accurate by letter but cannot be made to mean "the selftest ran and
  a case failed" — no case ran.
- The existing registry row (SKILL.md:2157) pins the c2-contract/c2-count/c1-survivors paths (they exist) but
  its write-scope cell ("TMPDIR only … target repo read-only") omits the sibling-repo *read* dependency.
  The only honest row today is one that states "needs sibling fleet repos at `../<repo>`; exit 1 otherwise"
  and the C3 predicate then fails honestly at this row (selftest-exit=1) in a bare clone. No row text can make
  the clone run exit 0; I do not suggest one (in particular not `--help --selftest`, which only prints argparse
  help and exits 0 without running a case).

## Province: can a later round fix it?

- **Facade (`tools/round21-measure.py`)**: yes, in province for a later round. It is a "maintained public
  CLI/selftest facade" (docstring line 2); it is not a frozen counter. It is unchanged this round and
  **cannot** be changed in round 51: `no-harm.sh:8,35` tools-scope allows only
  `M:tools/mutate-and-run.sh`, `tally-audit{,-v2,-v3}.py`, `mte-interop.py` (amendment 2); editing
  `round21-measure.py` is a RED tools-scope, and C3 was frozen with this tool in the 30 without a repair path.
- **Delegates (`c1-survivors.py`, `c2-count.py`, `c2-contract.json`)**: frozen round-21 files; the facade
  "delegates unchanged" (SKILL.md:1977, docstring). Their bytes are the round-21 receipt rulers
  (`counter_sha256` recorded in the receipts). Fixing layer (2) would need either an environment-supplied
  fleet root (changing a frozen counter, which invalidates its receipt hash) or leaving it documented.
- **Minimal later-round fix (facade only)**: derive the sibling root without `ROOT.parent`, e.g. take the same
  fleet constant as the delegate (reproduction 3, validated in scratch), or read it from an explicit flag/env and
  exit 2 (could-not-evaluate, matching the docstring) with a one-line message when a pinned repo is missing,
  instead of a traceback. This fixes the clone crash and the exit-code miscalibration; it does not make the
  selftest hermetic (still needs the five repos at their pinned revs on the host) — hermetic would require
  embedding or fixturizing the 9 pinned blobs, which changes what the selftest verifies.
- Fleet-dependency risk is the same class as the already-known `registry-replay` live-read rows (SKILL.md:2074-2079),
  so a later round could handle it as a class (declare "fleet-bound" in the registry vocabulary or give the C3
  counter an optional `--fleet-root` for such rows); that is a counter/spec amendment, out of this round.

## Confidence

High (reproduced both outcomes; exact lines read at CAND). Not tested: effect of `bwrap` absence on c2-count
inside the selftest (layer-2 fixture passed with bwrap present); whether the counter's clone parent could
contain stray siblings on another host (it is a fresh `mkdtemp` work dir under the counter's `--work`).
