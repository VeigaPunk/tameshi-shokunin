# Review — `tools/registry-check.py` at eb7838b16490ca7ba17ea3242ade76a61f744af2

Target: `tools/registry-check.py` sha256 `0bf9d1d2971c9fe478823754c7b889315585b73361ee3146631f409c4c5a3765` (1314 lines);
`tools/registry.json` sha256 `98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630`.
Clone: `/tmp/tameshi-r17w2-ReviewRegistryCheckCode-OINo4d/fleet/tameshi-shokunin` (detached at the landing rev, fleet-mirror siblings symlinked). Python 3.14.8, git from PATH. No installs were needed and none were made. All execution in the clone; the only lane write is this report.

Axes attacked: exit mapping, superseded semantics, timeout enforcement, clone lifecycle/cleanup, env scrub, JSON report contract, and the selftest's adequacy as a verification fixture.

## 1. Selftest (baseline)

```
$ python3 tools/registry-check.py --selftest
SELFTEST_CASE ... (34 cases, all PASS)
SELFTEST: PASS (34 cases)
exit 0, wall 3.58 s
```

All 34 cases pass. Three independent mutations of a scratch copy (`/tmp/.../adv/*.py`, one-line edits, never the lane file) were run against it:

| mutation | selftest result | side effect |
|---|---|---|
| after `clone_lane_at_rev`, add `root = root_requested` (grade the source tree, not the clone) | **PASS 34/34, exit 0** | none observable — the suite cannot tell |
| replace `shutil.rmtree(work, ignore_errors=True)` in `main`'s `finally` with `pass` | **PASS 34/34, exit 0** | **6 leaked** `/tmp/tameshi-registry-check-*` clones |
| `_kill_group` direct-child kill instead of `killpg` | (not run) | — |

## 2. Findings, highest first

### F1 (medium) — `--only` on a superseded row can never fail; a hard timeout returns 0
`evaluate()` derives the verdict from active rows only (`tools/registry-check.py:541-551`), while `--only NAME` is documented to run "exactly the named row (any status)" (`:64`) and exits are documented as "0 all held · 1 any differs" (`:46`). With `--only` on a superseded row, `active=[]`, so `held == len(active)` is `0 == 0`.

Observed (adversarial registries):
- `--only old-fail` (superseded, actual exit 5, expect 0): **exit 0**, `REGISTRY_CHECK: held=0/0 superseded=1`; JSON `held=0,total=0,rows[0].held=false,got=5,exit=0`.
- `--only old` where the row hits its `timeout_s=1`: `ROW old superseded expect=0 got=timeout` — **exit 0**.
The same vacuous truth applies to `--tag` selections that contain only superseded rows, and to a wholly empty registry (F5). A one-row monitor cannot report its one row diverging.

### F2 (medium) — timeout is not a wall bound: an escaped session holding the pipe extends it without limit
`_kill_group` (`:306-324`) kills the row's process group; `communicate()` at `:387` then waits for pipe EOF with **no timeout**. A row that spawns `setsid` escapes the group while inheriting stdout/stderr.

| row | timeout_s | wall | reported |
|---|---|---|---|
| `subprocess.Popen(['setsid','sleep','6']); time.sleep(30)` | 1 | **6.07 s** | `got=timeout`, `elapsed_s=4.02` (second probe, sleep 4), wall 4.07 s |
| same with `sleep 86400` | 1 | ~1 day (by construction) | `timeout` only after the escapee exits [INFERENCE from the mechanism] |

The kill grace itself (`proc.wait(timeout=5)` then SIGKILL, `:315-324`) also means a `timeout_s=1` row can legitimately occupy ~6 s. `elapsed_s` is honest (measured after the wait), but the documented `timeout_s` contract is not enforced against pipe-holding descendants. The selftest's `timeout-kills-group` case (`:760-795`) covers only same-group grandchildren, not an escaped session.

### F3 (medium) — non-finite `timeout_s` passes validation, then crashes with exit 1 and no report
Validation is `isinstance(ts,(int,float)) and not ts <= 0` (`:221-227`). `NaN` and `Infinity` satisfy `not (ts <= 0)` and are accepted; `json.loads` accepts both literals. Execution then raises an uncaught exception:

```
NaN      -> ValueError: cannot convert float NaN to integer        exit 1, stdout empty
Infinity -> OverflowError: cannot convert float infinity to integer exit 1, stdout empty
```

Exit 1 is the documented "any differs" code, so a malformed registry is indistinguishable from a genuine divergence, and no `REGISTRY_CHECK` trailer or JSON report is produced. Fix: `math.isfinite(ts)` in `registry_errors`.

### F4 (medium) — superseded rows' recorded `expect` is decorative, and the shipped baseline superseded row already diverges at the landing rev
Superseded rows are excluded from `held/total` and their `expect` is never compared (`:541-551`); the human line omits `held|differs` (`:561-567`). Confirmed with `expect=9`, actual `0`: `ROW old superseded expect=9 got=0`, `held=0/0`, **exit 0**.

At eb7838b the one shipped superseded row (`tools/registry.json:250-268`, tags `["baseline"]`) does not match its recorded expectation:

```
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
REGISTRY_CHECK: held=22/22 superseded=1        # (baseline minus the 900 s regression row)
exit 0
```

Direct cause: `tools/evidence-disposition.py --dispositions .ufo/evidence/round-14/dispositions.json` reports `expected_input_digest_mismatch` for `tools/mutate-and-run.sh` (`observed fb6d86d5… expects 75ed934d…`). Because the row is superseded, this can never affect the verdict — the registry records an expectation that is unenforced and currently false. Consequence for C2's wording "at eb7838b every baseline row holds": true for the 22 **active** baseline rows I ran; the baseline-tagged superseded row visibly differs in the same output. The C2 sub-claim "the old round-14 command is reported superseded" holds literally.

### F5 (low) — empty / zero-active selection is a success
`{"rows": []}` → `REGISTRY_CHECK: held=0/0 superseded=0`, **exit 0** (JSON `exit=0`). A registry whose `rows` was accidentally emptied, or any future selection with no active rows, is indistinguishable from a fully passing one by exit code. The doc defines 2 for "`--only`/`--tag` miss" but not for "nothing evaluable". Suggest exit 2 when `total == 0`.

### F6 (low) — the hermeticity guard is lexical and bypassable with `..`
`_argv_outside_fleet` (`:326-340`) compares `token.startswith(fleet_root + "/")` after splitting once on `=`. Under `--rev` with fleet root `F`:

```
F/lane/tools/registry.json        -> got=non-hermetic (held=false)      # caught
F/./lane/tools/registry.json      -> got=non-hermetic                    # caught
<parent>/fleetX/../F-basename…/registry.json
                                  -> got=0 held=true, non_hermetic_argv absent
```

The third token is absolute and resolves inside the fleet root (an existing sibling directory is enough; a symlink needs nothing), yet the row executes. The doc says a held row "names no absolute path under the live fleet root". `os.path.realpath` on each absolute token (or at least `normpath`) would close the `..` case. Code-embedded paths (an absolute path inside a `python -c` string) and relative `../sibling-shokunin` paths are likewise unflagged — inherent to argv scanning [INFERENCE for the code-string variant].

### F7 (low) — SIGTERM abandons the in-flight row
`_sigterm` (`:1183-1184`) raises `SystemExit(2)` inside `communicate`; no child cleanup runs. Observed: monitor exits 2, **stdout and stderr empty** (no report), the row survived and appended its marker 4 s later. The `mkdtemp` clone *was* removed, so cleanup of the tree holds. In live `--root` mode this leaves a mutating row running in the lane after the operator stops the monitor.

### F8 (low) — early-error JSON lacks `exit` and most schema fields; JSON mode drops the human error line
Evaluated report keys: `exit, held, live, only, registry, registry_sha256, rev, rev_resolved, root, rows, schema, superseded, tags, total`.
Early-error reports (`:1240-1282`) have only `error, rev, root, schema` — no `exit`, so `report["exit"]` KeyErrors. In `--json` mode those paths emit the JSON only; the evaluated path additionally writes the human `REGISTRY_CHECK:` line to stderr, so JSON-mode error output is inconsistent. The doc's additive-field list (`:69-71`) does not mention `exit` though it is always present on evaluated reports.

### F9 (low) — `root` and `registry` point into the deleted clone
Under `--rev`, `root` is the mkdtemp clone (`report["root"]` at `:507`) and `registry` defaults inside it. Both are removed before the JSON is printed (`:1301-1305`). Observed: `isdir(root) == False`, registry parent gone. `rev_resolved` is the only durable identity; a consumer cannot inspect the graded tree.

### F10 (low) — dead branch and wrong diagnostic for `--only` + `--tag`
`if only is not None and not selected` (`:534-537`) is unreachable: with `--only` set, `selected` is non-empty or the earlier `return 2` (`:522-530`) fires; if a tag filter empties it, `:531-533` returns first. Observed: `--only ok-row --tag zzz` → `could-not-evaluate (--tag ['zzz'] selects no registry row)`, never the intended `--only … is excluded by --tag`. Selftest `only-tag-conflict` (`:1116`) asserts only the exit code, so the message is untested.

### F11 (low) — needle matching is over full stdout, not the "retained tail"
`:394-395` checks `stdout_text` (full). A row printing `NEEDLE` followed by 8000 `x` holds `stdout_contains: ["NEEDLE"]` while `stdout_tail` (4096 B) does not contain it. The doc (`:37`) says the check is "over the retained tail"; that sentence is false, and a JSON-only reader cannot reproduce the match.

### F12 (low) — schema/exit-mapping nits
- `expect.exit` is any int (`:211-213`); `256` is accepted and can never hold. No 0-255 range check.
- A missing `git` binary raises uncaught `FileNotFoundError` → exit 1, empty stdout instead of the documented 2 for "rev missing" (`:409-423`, `:426+`).
- `rows, data, error = load_registry(...)` (`:502`): `data` is never used.

### F13 (verification-fixture gaps) — the selftest does not check the two promises it appears to check
- **Rows run in the clone**: mutation `root = root_requested` after a successful clone → `SELFTEST: PASS (34 cases)`. The fixture lane has one commit, so its row output is identical in source and clone; no case reads a file whose content differs between HEAD and the graded rev, and no case asserts the row's cwd. The tool's internal `clone HEAD == sha` check (`:479-487`) survives the mutation.
- **Clone cleanup**: mutation dropping `rmtree(work)` → `SELFTEST: PASS (34 cases)` with 6 leaked clones. No case asserts absence of `tameshi-registry-check-*`.
- No case covers F1 (superseded verdict), F3 (non-finite timeout), F5 (empty registry), F6 (`..` bypass), F8 (early-error shape), or SIGTERM (F7).

## 3. Verified holds (agreement)

- Exit mapping for evaluated, well-formed registries: 0 all active held, 1 any active differs, 2 could-not-evaluate, 64 usage (selftest + A1/A4/B/K/Q).
- Registry validation rejects bad schema/kind/name/duplicate/argv/source/status/tags/type rows (selftest cases; `:163-270`).
- `superseded_by` must name an existing **active** row; targets resolve against the full registry (selftest).
- `--tag` is any-of, repeatable, and a miss is exit 2; superseded rows are filtered like any other row (selftest + M).
- `--json` puts the machine report on stdout and ROW/trailer lines on stderr; `registry_sha256` matches the file bytes (A3, selftest `json-report`).
- Environment scrub works: with `GIT_DIR` exported by the parent, the row sees `GIT_DIR` absent, `stdin` at EOF, `PYTHONDONTWRITEBYTECODE=1` (probe R, needle `False '' 1` held).
- `--rev` resolves, clones detached at the resolved sha, verifies `HEAD`, reports `rev_resolved`, and removes the mkdtemp on success, on an evaluate-time crash (NaN probe), and on SIGTERM (no leftover `/tmp/tameshi-registry-check-*` in every case).
- A rev that is resolvable in the source but unreachable from any ref (`HEAD` detached, committed, branch moved back) still grades correctly: the local clone copies the loose objects (J).
- `--root` pointing at a file is exit 2 with `root_unavailable`.
- Live mode prints the "rows may write into the root" warning on stderr.

## 4. Observations bearing on the wave claims (advisory; other seats own the reruns)

- C2 command shape at the landing (clone root, `--rev eb7838b…`, landing registry, `--tag baseline`): with the 900 s `mutate-and-run-regression` row excluded from my run, **22/22 active baseline rows held, exit 0, 21 s wall**; the baseline-tagged superseded row printed `got=2` against `expect=0` (F4). The verdict line `held=22/22 superseded=1` cannot express that divergence.
- With the landing registry's disposition rows at 98bea7d, `evidence-disposition-round17`, `evidence-disposition-round17-before` and `evidence-disposition-round14-superseded` all return 2, while `evidence-disposition-selftest` holds. `.ufo/evidence/round-17/` does not exist at that rev (`git ls-tree` empty), so at least the round-17 gate's difference is missing inputs, not (only) a code capability [INFERENCE: the phrase "capability differs" is supported by exit codes but the proximate cause is the absent evidence tree].
- Not run by me: `mutate-and-run-regression` (900 s timeout). My baseline numbers therefore exclude it.

## 5. Residual risk

- `--rev` is a hermeticity claim about argv only, not a sandbox. Rows inherit the full environment except `GIT_*`, can write `$HOME` and `/tmp`, can use the network, and can name live paths inside code strings or relative `../sibling-shokunin` paths (F6). The `external` flag legitimizes the one such row in the shipped registry (`pin-disposition-read`).
- `timeout_s` is a soft budget, not a maximum wall time (F2).
- Superseded rows are evidence-free by construction: their expectations are never enforced (F4), so the registry cannot serve as a record of what a superseded command actually returns.

## 6. Verdict

The tool's normal-path exit mapping, schema checks, env scrub, detached-clone identity and cleanup hold; but `--only` on a superseded row reports success even on timeout/wrong exit, an escaped `setsid` child makes the timeout unbounded, non-finite `timeout_s` crashes into exit 1 with no report, and the shipped baseline superseded row already diverges (expect 0 / got 2) while the monitor prints `held=22/22` — **partial**: attacker's findings F1-F4 are real, the selftest is green because it does not test them or the clone-tree/cleanup promises.
