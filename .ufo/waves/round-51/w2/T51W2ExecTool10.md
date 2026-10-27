# T51W2ExecTool10 — C3 registry row falsification: `tools/pin-disposition.py`

**Seat:** T51W2ExecTool10 (executor, axis operability, milestone C3 row falsification)
**Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**Base:** `9962033fd7a75aa2f2847e979dd687a5d28505a1` · **Candidate audited:** `6d8c11e378aa90b12650808e1b79270742935f15`
**Row audited:** `SKILL.md:2151`, section `#### Gate/probe registry — round 51`, data row **10 of 30**.
**Method:** read-only on lane/fleet/sibling repos; one `git clone --shared` at CAND in scratch; scratch root `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool10/`; explicit `TMPDIR`; `stdin=/dev/null`. No source or row was modified. No tool installed (none needed).

---

## 0. Verdict in one line

The row **passes the frozen C3 counter's mechanical checks** (counter verdict `None`, selftest exit 0, last line `SELFTEST: PASS (19/19)`), but the row's **prose is wrong in three checkable ways**: its exit-1 meaning is falsified by a reachable run-mode crash, its "0 clean" mapping contradicts both the tool's own `USAGE` and the lane's own prior row for the same tool, and its pinned-values cell both omits a load-bearing in-tool pin and describes a manifest whose own runner pin and line citations are stale at CAND.

**Row 16's known clone-context failure is NOT this row.** Data row 16 is `round21 measure facade` (`SKILL.md:2157`, the `round21-measure.py` blocker named in the assignment). This row's tool is `pin-disposition.py` and its selftest **passes cleanly from a fresh clone at CAND** (`exit=0`, `19/19`, ~0.9 s).

---

## 1. The row under audit (verbatim, `SKILL.md:2151`)

```
| pin disposition | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root FLEET` | 0 clean; 1 failed (selftest FAIL only); 2 could-not-evaluate (usage, invalid or mismatched manifest, fleet root not a directory) | `python3 tools/pin-disposition.py --selftest` → SELFTEST: PASS n/n finding id SELFTEST: | `.ufo/evidence/round-13/pin-manifest.json` | read-only over the named fleet root; selftest writes isolated /tmp/tameshi-r13-pin-disposition-selftest.* fixtures, removed on PASS | tameshi |
```

Also present in the same file for the same tool: the round-13 row `SKILL.md:1552` and a summary row `SKILL.md:1853`. Both are cited below as the lane's own prior statements.

---

## 2. Required measurements (all from `git clone --shared` at CAND, scratch TMPDIR, stdin `/dev/null`)

| # | Invocation | Exit | Wall | Last stdout line |
|---|---|---|---|---|
| M1 | `python3 tools/pin-disposition.py --selftest` (row's exact backticked cmd) | **0** | **0.94 s** (0.92–1.32 s over repeats) | `SELFTEST: PASS (19/19)` |
| M2 | `python3 tools/pin-disposition.py --r51-no-such-flag` (usage probe) | **2** | **0.024 s** | `}` (last line of the JSON error document; stdout is a JSON object, not a marker line) |
| M3 | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` (entry cmd, real fleet root) | **0** | **0.079 s** | `}` (JSON document) |
| M4 | same entry cmd with `--root` = the lane clone (no sibling repos) | **0** | — | `}` — `counts: {"legs": 6, "unchanged": 0, "changed": 0, "unavailable": 6}` |
| M5 | `python3 tools/pin-disposition.py --selftest` with `git` absent from `PATH` | **2** | 0.024 s | `SELFTEST: COULD_NOT_EVALUATE ([Errno 2] No such file or directory: 'git'; fixtures kept at /tmp/tameshi-r13-pin-disposition-selftest.njy9r7vi)` |

M3 payload: `counts: {"legs": 6, "unchanged": 1, "changed": 5, "unavailable": 0}` — **five of six legs drifted and the tool still exited 0.** (Receipt: `T51W2ExecTool10/entry.stdout`, `verify-results.txt`.)

**Counter's own evaluation of this row** (frozen `.ufo/evidence/round-51/c3/measure.py` imported and driven against CAND, `row_reason` + `run_row`): `row_reason` → `None`; `run_row` → `None`, `last_line='SELFTEST: PASS (19/19)'`, wall 1.80 s. Receipts: `counter-row-check.txt`, `counter-run-row.txt`.

**Fixture integrity:** `git rev-parse --show-toplevel` in the clone printed `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool10/clone` (asserted before use). No commit was made in the clone; `git status --porcelain` in the clone stayed empty after all probes.

---

## 3. Findings

### F1 — MATERIAL — the verdict map's exit-1 meaning is falsified: exit 1 is reachable from the **run mode**, not only from a selftest FAIL

The row declares `1 failed (selftest FAIL only)`. That parenthetical is false. `read_manifest` parses the manifest with `json.loads` guarded only by `except json.JSONDecodeError` (`tools/pin-disposition.py:591`), and `main()` catches only `InvalidInput` (`tools/pin-disposition.py:1385-1386`). A `ValueError` or `RecursionError` raised by `json.loads` therefore escapes both handlers, and Python exits **1** with a traceback on stderr and **empty stdout** — from the **entry command**, with no selftest involved.

Two independent reproductions, both from the clone at CAND:

**(a) integer string-conversion limit** — a manifest carrying one extra 5000-digit integer literal:
```
$ python3 tools/pin-disposition.py --manifest <copy of pin-manifest.json with a 5000-digit field> --root /home/vgpnk/Projects/shokunin
EXIT = 1
ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; use sys.set_int_max_str_digits()
stdout bytes: 0
```
(`repro-exit1-crash.py`, receipt `exit1-bigint.stderr`. `json.JSONDecodeError` is a *subclass* of `ValueError`, so `except json.JSONDecodeError` does not catch a plain `ValueError`.)

**(b) recursion limit** — a manifest of 100 000 nested `[`:
```
exit=1  ERR:RecursionError: Stack overflow (used 8140 kB) while decoding a JSON array from a unicode string
stdout: empty
```

**Why this matters for C3.** The C3 predicate requires "a verdict map with 0 and 1", and the contract's own `cannot_see` clause for C3 reserves exactly this to wave-2 per-row probes: *"the verdict map names every code the tool can exit with beyond 0, 1 and the usage code (attacked per row by wave-2 probes)"*. The tool's exit set is `{0, 1, 2}` — no undeclared code such as 64 — but the **class attached to 1 is wrong**. Under `PROTOCOL.md` §Gate standard (fleet root, line 380-384), `1` means `failed` fleet-wide and *"an undeclared nonzero code reads as `could-not-evaluate`"*. An uncaught crash in the probe's entry command exits 1 and would be read by the registry as **`failed`** — a content verdict — when the honest reading is **could-not-evaluate**. The row's own words foreclose that reading by asserting exit 1 means `selftest FAIL only`.

Also note the crash is *silent to the caller*: stdout is empty, so a reader who checks only the exit code sees `1` = failed, and a reader who checks stdout sees no verdict document at all.

**Scope note.** The C3 counter does **not** catch this: `measure.py:173-184` only runs the row's self-test command and the usage probe, and `usage` here is `python3 tools/pin-disposition.py --r51-no-such-flag` → exit 2, which the map declares, so `run_row` returns `None`. This is a counter blind spot, not a counter failure — but it does mean the row's prose is the only place the defect is visible, and the prose is wrong.

### F2 — MATERIAL — "0 clean" is wrong for this tool: exit 0 means "observations emitted", and the lane's own prior row for the same tool said so

The row maps `0` to `clean`. For this tool that is false, and it is false **on the tool's own authority**:

* `tools/pin-disposition.py:156-157` (the tool's `USAGE` string): `exit 0  observations emitted (drift and unavailable legs included)`.
* `tools/pin-disposition.py:151-154` (module docstring): "Per leg the JSON carries `result_reuse=not_established`…".
* The lane's **own round-13 registry row for this very tool**, `SKILL.md:1552`, states: `0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate; selftest 1 failed`.

The round-51 row compresses that accurate statement to `0 clean`. Measured at CAND against the real fleet root (M3): `counts = {"legs": 6, "unchanged": 1, "changed": 5, "unavailable": 0}` — **exit 0 with five drifted legs**. A reader consulting the registry would read `0 clean` as "the pins verified clean". They did not; the probe's whole point is that it reports drift while exiting 0.

This is a **regression against the lane's own prior, more precise wording for the same tool at the same candidate**, and it is a protocol-facing mis-description: `PROTOCOL.md` §Gate standard line 380 binds `0 = clean` to *gates*, and this row is registered `kind=probe` — a probe's exit 0 is "the observation ran", not "the observation is clean". (The `kind=probe` classification itself is **correct** — see §4.)

### F3 — MATERIAL — the pinned-values cell is incomplete, and the manifest it names carries a stale runner pin with stale line citations that the tool never verifies

The row's `Pinned values` cell names one path: `.ufo/evidence/round-13/pin-manifest.json`. Findings:

**(a) A second load-bearing pin is not named.** The tool hard-codes the six-leg mapping `CANONICAL_LEGS` (`tools/pin-disposition.py:138-145`), and `read_manifest` **rejects any manifest whose leg `repo`/`path` disagree with it** (`:629-645`, `invalid_manifest`). Measured: a manifest naming a different `repo` → exit 2 (`invalid_manifest`, "does not match the recorded repo"). The manifest alone is therefore *not* the full pinned set; the in-tool leg table pins behaviour too. The lane's own round-13 row said so explicitly (`SKILL.md:1552`: "`.ufo/evidence/round-13/pin-manifest.json`; **canonical leg mapping and literal selftest labels in tool**"). The round-51 row drops that clause. The C3 counter's pinned-path check (`measure.py:148-152`) only verifies that a backticked relative path exists at REV, so it cannot see the omission.

**(b) The manifest's own `derived_from` runner pin is stale at CAND, and the tool never checks it.** `pin-manifest.json:3-6` declares `derived_from.sha256 = 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` for `tameshi-shokunin/tools/mutate-and-run.sh`. Measured sha256 of that path:
| revision | sha256 of `tools/mutate-and-run.sh` |
|---|---|
| `606716f` (= the round-13 manifest commit's runner) | `75ed934d…` ← the manifest's declared pin |
| BASE `9962033` | `a7d3f2dd…` |
| CAND `6d8c11e3` | `977de470…` |

The manifest's pin matches **neither BASE nor CAND**. `grep -n derived_from tools/pin-disposition.py` → **no reference in the tool source**: the tool never verifies `derived_from`, so the staleness is invisible at runtime and no code path can report it.

**(c) The manifest's own line citations are stale at CAND.** `pin-manifest.json:7` cites `tools/mutate-and-run.sh:84-89 (leg/path table), :542-553 (PIN_*/REV_* pairs), :1112-1140 (six ledger leg calls)`. At CAND those ranges hold different content: the leg table is at **:88-97**, the `PIN_*`/`REV_*` pairs at **:614-633**, and the six `regression_case_git` calls at **:1459-1484** (`:1112-1140` is now the embedded defect-spec table). The citations were accurate at `606716f` and drifted with the runner.

**(d) The six-leg ceiling is undisclosed and now excludes four recorded legs — including the tenth leg this round added.** The runner at CAND records **ten** legs (`SKILL.md`-adjacent runner comment table `:88-97`: `js-kimi-census`, `bash-surface-census`, `bash-tsukuroi-census`, `bash-mado-verify`, `bash-checklist-run`, `js-claims-check`, `js-round-gate`, `js-sources-check`, `js-cite-check`, `bash-drift-pins`), the tenth being `bash-drift-pins` → `kagi-shokunin/corpus/drift-pins.sh` with `PIN_DRIFTPINS=c138d34c…` / `REV_DRIFTPINS=e64e81b8…` at runner `:632-633` — the exact leg C2 added this round. The tool's `CANONICAL_LEGS` still names only six, and `read_manifest` refuses a seventh. Measured: a manifest naming `js-round-gate` (leg 7, present in the CAND runner) → **exit 2**, `invalid_manifest`, "leg entry 7 names unknown leg 'js-round-gate' (six recorded legs only)" (`:620-624`). The row's verdict map and write scope describe the probe as covering the fleet root without disclosing the six-of-ten ceiling; the tool's own comment at `:136` still points at the stale `(:84-89, :1112-1140)`.

**(What does hold.)** The pinned manifest's `expected_sha256` values *are* load-bearing on expected behaviour: mutating one leg's `expected_sha256` in a copy of the manifest flipped that leg to `pinned.status=mismatch`, `content_status=unavailable`, `reason=pinned_blob_mismatch` (receipt `verify-results.txt` line 7b). So "pinned values really affect expected behavior" — yes, for the digests; the defect is that the pinned set is *understated* and its provenance is *stale and unverified*.

### F4 — MINOR/MATERIAL for operability — the write-scope cell is literally true but omits the half that leaves state behind, and the tool ignores `TMPDIR`

The row says: "selftest writes isolated /tmp/tameshi-r13-pin-disposition-selftest.* fixtures, **removed on PASS**".

* **Accurate half.** Verified over 6 consecutive clean runs from a wiped `/tmp`: residue count **0** after every PASS run (`verify-results.txt` step 8b). The removal is `shutil.rmtree(scratch, ignore_errors=True)` at `:1328`, executed only on the PASS path.
* **Omitted half — state is retained on failure.** The FAIL path (`:1321-1327`) and the `COULD_NOT_EVALUATE` path (`:1316-1318`) both print **"fixtures kept at {scratch}"** and return **without** removing the tree. Measured: the git-absent run (M5) left `/tmp/tameshi-r13-pin-disposition-selftest.njy9r7vi` behind; a second run with `git` absent leaves another. The row states only the removal-on-PASS half, so a reader cannot tell that a failed selftest leaves a fixture tree in the global `/tmp`.
* **`TMPDIR` is ignored.** The scratch root is hard-coded: `tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir="/tmp")` (`:706`) — `dir="/tmp"`, not `TMPDIR`. The C3 counter deliberately isolates each row with `e['TMPDIR'] = tmp` under `WORK/tmp` (`measure.py:160-171`, and its own docstring at `:19` "TMPDIR=WORK/tmp"), and this tool writes outside that sandbox. Most sibling rows in the same table say "TMPDIR"; this one says "/tmp/…" and is thereby accurate about the location, but the counter's isolation guarantee does not hold for it. (Consequence for the counter is nil here: `mkdtemp` names are unique, and the lane clone stayed clean.)
* **Read-only claim holds.** `git status --porcelain` sha256 for `kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin` was byte-identical before and after M3 (receipt `verify-results.txt` step 9b). The tool's git calls are read-only and run with `GIT_OPTIONAL_LOCKS=0` (`:216`).

### F5 — MINOR — the recorded finding id is non-discriminating and the expected case count is left as the literal placeholder `n/n`

The row's self-test cell reads `→ SELFTEST: PASS n/n finding id SELFTEST:`.

* **`n/n` is a placeholder, not the pinned expectation.** The tool prints `SELFTEST: PASS (19/19)` at CAND — 19 cases, deterministic. Every comparable row in the same table pins a concrete count (`context receipt replay` → `49/49 cases`; `receipt-window validity` → `20/20 pass`; `tally audit v3` → `35/35 pass`; `write-path census v4` → `cases=15 failed=0`). This row alone leaves the expected count unspecified, so the registry does not pin what the selftest is supposed to assert.
* **The recorded finding id `SELFTEST:` cannot distinguish pass from fail.** The tool emits three terminal forms sharing that first token: `SELFTEST: PASS (19/19)` (`:1329`), `SELFTEST: FAIL (n/m failed: …; fixtures kept at …)` (`:1322-1326`), `SELFTEST: COULD_NOT_EVALUATE (…; fixtures kept at …)` (`:1317`). The row's named id is a prefix common to all three. It is a genuine tool-emitted diagnostic (not author-chosen help text, so the item's bar is met), but it does not discriminate the outcome a reader would need.
* **The counter accepts it anyway:** `measure.py:178-180` takes `marker = last.split()[0]` and checks `marker in st` — a substring test against the whole self-test cell, which contains "SELFTEST:" twice. So the counter's finding-id check cannot fail this row.

---

## 4. What I checked and found **holds** (so the L1 does not re-litigate it)

* **`kind=probe` is correct.** `PROTOCOL.md:378-379`: "A tool that cannot fail is a **probe**, and is registered as one." The tool never returns a content-based failure: `run_mode` returns 0 unconditionally after emitting the document (`:691`); content outcomes travel in the payload as `content_status` ∈ {`unchanged`, `changed`, `unavailable`}. The only non-zero exits are 2 (could-not-evaluate) and the crash-derived 1 of F1. Probe is the right kind.
* **Owner `tameshi` — correct**; the tool lives in the lane.
* **Exit-code set is `{0, 1, 2}`** — no undeclared code (no 64, no 3). Every code the tool exits with is named in the map; only the *meaning* of 1 is mis-stated (F1).
* **Usage probe behaves as the map says:** `--r51-no-such-flag` → exit 2 (`invalid_input`, `kind=invalid_usage`, "unknown argument: --r51-no-such-flag"), and 2 is declared `could-not-evaluate`.
* **Self-test is hermetic and clone-context-clean.** `--selftest` builds its own fixture tree under `/tmp`, sets `HOME` to it, and reads no fleet or sibling repo; it passed from a fresh `git clone --shared` at CAND with no sibling repos present (19/19, exit 0, ~0.94 s). The known `round21-measure.py` clone-context blocker belongs to data row 16, not to this row.
* **Write scope over the fleet root is read-only** (F4).
* **Pinned digests affect expected behaviour** (F3).
* **The row's eight cells are structurally what C3 requires**: kind ∈ {gate, probe}; entry names the tool; verdict map carries standalone `0` and `1`; exactly one backticked self-test command with no shell metacharacters; `python3 tools/pin-disposition.py --selftest` parses to the tool plus a `selftest`-bearing argument; pinned cell non-empty with a path that exists at REV; write scope non-empty; owner `tameshi`. The frozen counter returns `None` for `row_reason` and `None` for `run_row`.

---

## 5. Exact reproductions

```bash
# fixture (read-only on the lane; clone only)
S=/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool10
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
git -C "$S/clone" checkout -q --detach 6d8c11e378aa90b12650808e1b79270742935f15
git -C "$S/clone" rev-parse --show-toplevel   # -> $S/clone   (assert before any fixture op)
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR"; cd "$S/clone"

# M1 selftest / M2 usage probe / M3 entry command
python3 tools/pin-disposition.py --selftest            # exit 0, "SELFTEST: PASS (19/19)"
python3 tools/pin-disposition.py --r51-no-such-flag    # exit 2, JSON invalid_input
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json \
        --root /home/vgpnk/Projects/shokunin          # exit 0, counts changed=5 unchanged=1

# F1 exit 1 from the RUN mode (not a selftest FAIL)
python3 tools/pin-disposition.py --manifest "$S/bigint2.json" --root /home/vgpnk/Projects/shokunin
#   -> exit 1, ValueError (4300-digit limit), stdout empty
python3 tools/pin-disposition.py --manifest "$S/deep2.json" --root /tmp
#   -> exit 1, RecursionError, stdout empty

# F3(d) the six-leg ceiling
python3 tools/pin-disposition.py --manifest "$S/sevenlegs.json" --root /home/vgpnk/Projects/shokunin
#   -> exit 2, invalid_manifest "names unknown leg 'js-round-gate' (six recorded legs only)"

# F4 selftest leaves fixtures behind when it cannot evaluate
PATH="$S/emptybin" python3 tools/pin-disposition.py --selftest
#   -> exit 2, "fixtures kept at /tmp/tameshi-r13-pin-disposition-selftest.*"

# bundled driver (all of the above, incl. residue and sibling-read-only checks)
python3 "$S/verify.py"          # -> verify-results.txt
```

Receipts in `.ufo/waves/round-51/w2/T51W2ExecTool10/` (and mirrored at `@P@ExecTool10/`):
`verify-results.txt`, `counter-row-check.txt`, `counter-run-row.txt`, `selftest.stdout`,
`usage.stdout`, `entry.stdout`, `entry-nosiblings.stdout`, `selftest-git-absent.stdout`,
`exit1-hunt.txt`, `exit1-bigint.stderr`, `timings.txt`, `row-text-line2151.txt`,
`repro-verify.py`, `repro-exit1-crash.py`.

---

## 6. Bottom line for the L1

This row is **operable** — its self-test runs green from a clone at CAND in ~0.9 s and the counter accepts it — and it does **not** obstruct C3's deciding run. But the row's prose is not accurate about its own tool, and the C3 predicate explicitly assigns this to wave-2 per-row probes. Ranked:

1. **F1** — exit 1 is reachable from the run mode (uncaught `ValueError`/`RecursionError` in `read_manifest`), so `1 failed (selftest FAIL only)` is false, and a crash would be misread as a content `failed` verdict rather than `could-not-evaluate`. *No row or source edit is required to observe it; the row wording is what is wrong.*
2. **F2** — `0 clean` contradicts the tool's `USAGE` (`:156`), its docstring, and the lane's own prior row for this tool (`SKILL.md:1552`); measured exit 0 with 5 of 6 legs drifted.
3. **F3** — pinned-values cell understates the pin set (omits the in-tool `CANONICAL_LEGS` table that the manifest must match), and the named manifest carries a runner pin (`75ed934d…`) matching neither BASE nor CAND plus line citations that no longer resolve at CAND; the tool never verifies `derived_from`. The probe also structurally covers 6 of the runner's 10 recorded legs, including excluding C2's new tenth leg.
4. **F4** — write-scope cell omits fixture retention on FAIL/COULD_NOT_EVALUATE; the tool hard-codes `/tmp` and ignores `TMPDIR`, escaping the counter's per-row isolation.
5. **F5** — expected selftest count left as literal `n/n` (actual `19/19`), and the recorded finding id `SELFTEST:` is common to PASS, FAIL and COULD_NOT_EVALUATE.

None of these is the C3 blocker the round already knows about (that one is `round21-measure.py`, data row 16). **C3's frozen predicate is not falsified by this row**; what is falsified is this row's description of its tool.
