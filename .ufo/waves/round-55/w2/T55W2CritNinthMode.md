# T55W2CritNinthMode — the ninth allocating mode (`registry-check --rev`), round 55 wave 2

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; base `0a2010acd1e92e4e332774050825e21bcfc7e079`,
content commit C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`. Axis: **operability**.
Scratch `$S=/fast/scratch/hyaku/tameshi-r55/T55W2CritNinthMode` (clones `base`, `c0`, `head`,
`fleet/mut-shokunin`; every clone made with `git clone --shared --no-checkout`, every git call
addressed `-C`, `git -C … rev-parse --show-toplevel` checked before the one fixture commit).
Receipts: `.ufo/waves/round-55/w2/T55W2CritNinthMode-receipts/`.
No lane production file, no frozen file (`.ufo/evidence/round-55/*`), no wave spec was edited; no
subagent was dispatched; no tool was installed (`git`, `python3`, `strace`, `timeout` sufficed).

**Counter bytes used.** The lane moved while I worked (HEAD went `9cf0146` → `4c04c1d`, freeze
amendments 8 and 9 landed). All counter runs below used the working-tree
`.ufo/evidence/round-55/c2/measure.py`, sha256
`0458f632087f665fbafc07efc6920d32febf7551d9fc5964d0c87fa0e139476b` — the digest the freeze manifest
at `4c04c1d` names for that path (amendment 8: the total's terms now use the denominators they
measure). The digest frozen at `e2979f2` (`36ca47d3…`) has `+ (8 - note)` while the note denominator
is 9; on the all-green arms that is `-1`, so it can never print `total=0`. The committed base receipt
(`total=20`) is only reproducible under the amended formula (`3 grammar + 7 docs + 9 note + 1 skill
= 20`), which is why the pointer moved. This is the sibling seat T55W2CritFreeze2's F2 territory;
recorded here only as provenance.

---

## Answer up front

1. **Base arm — TRUE.** At `0a2010ac`, `TMPDIR=/nonexistent/ninth python3 tools/registry-check.py
   --rev HEAD` prints exactly `REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under
   the scratch root: TMPDIR is not a usable directory: '/nonexistent/ninth' (could-not-evaluate))` on
   **stdout**, **0 bytes on stderr**, exit 2.
2. **C0 grammar arm — TRUE.** At `9cf0146`, the same command prints **0 bytes on stdout** and one
   stderr line, `registry-check: could-not-evaluate: cannot create clone scratch under the scratch
   root: TMPDIR is not a usable directory: '/nonexistent/ninth' (could-not-evaluate)`, exit 2. The
   line matches the frozen `GRAMMAR` regex in `c2/measure.py` (checked with that regex, not by eye).
   So the ninth mode's arm is real and discriminating: base FAIL, C0 ok in the committed
   `before/c2.stdout` and in my C0 counter run.
3. **Usable arm — the premise is FALSE.** `--rev 9cf0146…` under a good `TMPDIR` does **not** succeed:
   from the real lane it exits **1** after **1050 s** (cap 1800 s, not hit), `REGISTRY_CHECK:
   held=47/49 superseded=7`, with `sources-census` and `verify-round15` differing. Both rows are
   **introduced by C0** (both held at base) and **both persist at lane HEAD `4c04c1d`**. The frozen
   C2 counter still reads `total=0 C2_R55_PASS=true` at the same rev — so the mode's whole usable
   path is invisible to the claim that certifies it.
4. **Design — the grammar-only choice is disclosed, the compensating claim is not true for the whole
   path.** The note (C0 lines 82-84) and the counter's `modes()` docstring both say `--rev` is
   measured on the unusable arm only and that "its usable path is covered by the tool's own
   self-test, which exercises the same helper." A mutant that drops the fleet-mirror sibling symlinks
   in `clone_lane_at_rev` passes the tool's own selftest **51/51** and passes the frozen C2 counter
   **`total=0`, grammar 9/9**, while a sibling-resolving row graded through `--rev` returns
   `differs`/rc 1. So a regression in the usable path passes unseen by both gates — the selftest
   exercises the clone leg, not the mirror leg.
5. **C0 `--json` asymmetry (found, already closed upstream).** At C0, `--rev --json` under an
   unusable `TMPDIR` emits **0 bytes on stdout** while the tool's usage text promises a machine
   report there (base emitted the JSON report). Fixed at `51d1f0e`; my receipt at HEAD `4c04c1d`
   shows JSON on stdout plus the grammar line on stderr.

Severity: **(3) high — a red registered gate at the certified revision, unseen by C2**;
**(4) medium — the arm cannot see the path it certifies, and the note overstates coverage**;
**(5) low at C0, closed**. Findings 3 also hand the integrator two concrete lane defects (S280
citation, context-capture re-pin).

---

## 1. Base arm — `REGISTRY_CHECK: could-not-evaluate` on stdout, empty stderr

```
$ export HYAKU_SCRATCH=/fast/scratch/hyaku
$ S=$HYAKU_SCRATCH/tameshi-r55/T55W2CritNinthMode
$ git clone --shared -q --no-checkout <lane> $S/base
$ git -C $S/base checkout -q -B rb 0a2010acd1e92e4e332774050825e21bcfc7e079
$ cd $S/base && TMPDIR=/nonexistent/ninth python3 tools/registry-check.py --rev HEAD
rc=2
--- stdout (165 bytes)
REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/ninth' (could-not-evaluate))
--- stderr (0 bytes)
```

Receipts `base-rev-unusable.stdout`, `base-rev-unusable.stderr`. The committed base receipt agrees
independently: `.ufo/evidence/round-55/before/c2.stdout` has `EXPLAIN grammar registry-check --rev
rc=2 FAIL`.

## 2. C0 arm — one grammar line on stderr, exit 2, stdout empty

```
$ cd $S/c0 && TMPDIR=/nonexistent/ninth python3 tools/registry-check.py --rev HEAD
rc=2
--- stdout (0 bytes)
--- stderr (164 bytes)
registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/ninth' (could-not-evaluate)
```

Receipts `c0-rev-unusable.stdout/.stderr`. Two more probes of the same handler:

| probe (cwd `$S/c0`) | rc | stdout | stderr |
|---|---|---|---|
| `TMPDIR=/etc/passwd … --rev HEAD` (a file, not a dir) | 2 | 0 B | same grammar line naming `'/etc/passwd'` |
| `TMPDIR=/nope … --rev HEAD --json` | 2 | **0 B** (see §5) | same grammar line naming `'/nope'` |

Regex check with the frozen pattern (the counter's `GRAMMAR`, copied verbatim into a probe):

```
line: registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/ninth' (could-not-evaluate)
matches frozen GRAMMAR: True
base line grammar match (must be False): False
```

The new branch is what runs (not the generic `RuntimeError` handler): the generic handler in
`main()` still writes its report to stdout (`REGISTRY_CHECK: could-not-evaluate (...)`), and stdout is
empty here. That is why the arm discriminates at base vs C0.

## 3. Usable arm — the tool does not "succeed" at C0 (primary falsification)

Two runs, each with a fresh writable `TMPDIR`, each capped:

| cwd | command | cap | elapsed | rc | trailer |
|---|---|---|---|---|---|
| the real lane | `TMPDIR=$S/usable-tmp2 python3 tools/registry-check.py --rev 9cf0146…` | 1800 s | **1050 s** | **1** | `REGISTRY_CHECK: held=47/49 superseded=7` |
| `$S/c0` (scratch clone, no `*-shokunin` siblings) | same | 1800 s | 170 s | 1 | `REGISTRY_CHECK: held=45/49 superseded=7` |

Lane run differences (`lane-rev-usable.stdout`):

```
ROW sources-census expect=0 got=1 differs
ROW verify-round15 expect=0 got=1 differs
```

Clone run adds `mutate-and-run-regression got=2` and `mte-interop-check got=2` — the two rows that
resolve sibling lanes, which the clone's fleet mirror has none of. That is the same failure mode as
the mutation in §4 and is the real-world symptom of a broken/absent mirror.

### 3a. `sources-census` — C0's new S280 row is not cited by its own used-by file

```
$ cd $S/base && bash .ufo/evidence/kaika-round-1/sources-census-v2.sh … → SOURCES_CENSUS: CLEAN, rc=0
$ cd $S/c0   && bash .ufo/evidence/kaika-round-1/sources-census-v2.sh … → rc=1
no-id-or-path-cite: S280 corpus/knowledge/scratch-root-contract.md (Errors.html)
== VERDICT
SOURCES_CENSUS: VIOLATIONS
```

C0 added `| S280 | … https://www.gnu.org/prep/standards/html_node/Errors.html | … | corpus/knowledge/scratch-root-contract.md |`.
Rule B2 of that gate requires the used-by file to contain the row id or the source token
(`Errors.html`); the note contains neither (`grep -c S280` = 0, `grep -c Errors.html` = 0 at C0 and at
HEAD). Receipts `lane-rev-usable.stdout`, `head-census.out`.

### 3b. `verify-round15` — C0 moved `context-capture.py` without the round-53 re-pin

```
$ cd $S/base && python3 .ufo/evidence/round-15/verify.py --rev 7650fe4d…  → rc=0
$ cd $S/c0   && python3 .ufo/evidence/round-15/verify.py --rev 7650fe4d…  → rc=1
registered-tool-source-pin: FAIL worktree tools/context-capture.py sha256=f1043425085a08… pinned=c4a1d1658b93…
```

`tools/context-capture.py` sha256 at base `be539b4c…`, at C0 `f1043425…`; `verify.py`'s
`PIN_MAINTAINED_TOOL_SHA256` is still `be539b4c…` at C0 and at HEAD. The round-53 rule
(`8f47441`, "the moved digest is appended per the re-pin rule") was not applied to this edit.
Receipts `c0-verify-round15.out`, `head-verify.out`.

### 3c. Both persist at lane HEAD `4c04c1d`

```
$ git -C $S/head checkout -q -B rh 4c04c1d33377e5b6a3636199c5fdda197fc670d5
$ (census)  → rc=1, no-id-or-path-cite: S280 corpus/knowledge/scratch-root-contract.md (Errors.html)
$ (verify)  → rc=1, registered-tool-source-pin: FAIL worktree sha256=831b7810… pinned=c4a1d165…
```

So the ninth mode's usable arm is **red at the revision the wave certifies and at HEAD**, while the
C2 counter reads `C2_R55: rev=9cf0146b94dd grammar=9/9 … total=0 C2_R55_PASS=true` (receipt
`c2counter-c0.out`, rc 0, 304 s). No wave-1 artifact reports these two rows: every wave-1 `--rev`
receipt is the unusable arm (`T55W1ScribeLog-receipts/registry-check-rev-mode.txt` at candidate
`63d08ed1`, `T55W1ExecModeDiscovery-receipts/r07-…`, `T55W1ExecC2Full-receipts/…-unusable-arm*.txt`),
and the only wave-1 run that reaches the usable path is
`T55W1ExecModeDiscovery-receipts/r08-registry-check-rev-usable.txt` — `--only repeat-control-selftest`
at **base**, `held=1/1`, rc 0. (`T55W1Connector2.md:159` quotes a round-51 lesson that leaves the
`mte-interop-check` row unmarked; that row holds in the real-fleet lane run, so it is not this red
pair.) The lane's own rule (`SKILL.md:1859`) says a registered row that stops holding is a gate
failure; at C0 two do.

## 4. Design attack — grammar-only; the compensating coverage claim is false for the mirror leg

Disclosure exists and is accurate about *what is not run*:

* `corpus/knowledge/scratch-root-contract.md` (C0, lines 82-84): "`registry-check --rev` is measured
  on the unusable arm only: it builds a full fleet clone (minutes), so its usable path is covered by
  the tool's own self-test, which exercises the same helper."
* `c2/measure.py`, `modes()` docstring + `cheap=False` for that mode: not run on the empty/usable arms.

The compensation is the weak link. The selftest's `--rev` fixtures live under the scratch dir, and
the only entry there ending in `-shokunin` is the fixture lane itself — which `clone_lane_at_rev`
excludes from the mirror. No selftest case therefore exercises the sibling-symlink leg, and the
fd/docstring argument ("the same helper") covers the clone call, not the mirror.

**Mutant (fixture, clone at C0, commit `cd64d471` in `$S/fleet/mut-shokunin`; diff
`mutant.diff`)** — one line, the mirror's `os.symlink` becomes dead code:

```
-            os.symlink(src, os.path.join(fleet, name))
+            if False:  # mutation W2: the fleet mirror is dropped (regression under test)
+                os.symlink(src, os.path.join(fleet, name))
```

Fixture: `$S/fleet/sib-shokunin/marker.txt` next to the graded lane, one registry row
`cat ../sib-shokunin/marker.txt` (expect 0, needle `SIBOK`), graded with `--registry`:

| build | command | rc | result |
|---|---|---|---|
| C0 tool, unmutated | `--root $S/fleet/mut-shokunin --rev HEAD --registry reg.json` | 0 | `ROW sibling-marker expect=0 got=0 held` / `held=1/1` |
| mutant | same, mutant's own tool | **1** | `ROW sibling-marker expect=0 got=1 differs` / `held=0/1` |
| mutant | `python3 tools/registry-check.py --selftest` | **0** | `SELFTEST: PASS (51 cases)` |
| mutant | frozen C2 counter, `--lane $S/fleet/mut-shokunin --rev cd64d471…` | **0** | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true` |

Receipts: `fleetmirror-pristine.out`, `fleetmirror-mutant.out`, `mutant-selftest.out`,
`c2counter-mutant.out` (237 s), `mutant.diff`, `mutant-sha.txt`.

Conclusion: a regression confined to the `--rev` usable path passes **both** gates that are said to
cover it (the tool's selftest) or to certify it (C2). The counter's grammar arm cannot see it by
construction; the selftest cannot see the mirror leg; and at C0 the counter demonstrably passes while
the real usable arm is red (§3). The note's sentence should be qualified, not left as coverage.

```
# C0, freeze-of-record counter bytes (0458f632…), rc 0, 304 s
W=$(mktemp -d "$S/c2work-c0.XXXX")
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/c2/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb --work "$W" --explain
# → C2_R55: rev=9cf0146b94dd grammar=9/9 … total=0 C2_R55_PASS=true          (c2counter-c0.out)

# mutant, same bytes, rc 0, 237 s
W=$(mktemp -d "$S/c2work-mut.XXXX")
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/c2/measure.py \
  --lane "$S/fleet/mut-shokunin" \
  --rev cd64d4719d9698555ace323f8c441d08ac66f5b1 --work "$W" --explain
# → C2_R55: rev=cd64d4719d96 grammar=9/9 … total=0 C2_R55_PASS=true          (c2counter-mutant.out)
```

Residual, same class: the mode has no `scratch_root` registry cell of its own — the seven cells are
the seven `--selftest` rows. The claim's surface is "every documented mode", so this is consistent,
but it means the *docs* arm says nothing about `--rev`; only the note does.

## 5. `--json` asymmetry at C0 (small finding, already closed at `51d1f0e`)

The tool's usage text promises `--json` a machine report on stdout; every other exit-2 branch
(`root_unavailable`, bad rev, clone failure) still emits it. At C0 the new `ScratchRootUnusable`
handler prints only the stderr line:

```
$ cd $S/c0 && TMPDIR=/nope python3 tools/registry-check.py --rev HEAD --json
rc=2 ; stdout 0 bytes ; stderr = grammar line naming '/nope'
$ cd $S/base && TMPDIR=/nope python3 tools/registry-check.py --rev HEAD --json
rc=2 ; stdout = {"error": "cannot create clone scratch …", "rev": "HEAD", "rev_resolved": "0a2010ac…", …} ; stderr 0 B
```

Receipts `c0-rev-json-unusable.*`, `base-rev-json-unusable.*`. At HEAD `4c04c1d` (`51d1f0e`, "keeps
its machine report") the JSON report is back on stdout beside the grammar line
(`head-rev-json-unusable.*`). No further action; recorded so the C0 reading is not mistaken for the
current one. A JSON body on stdout does not disturb the grammar arm (it greps `RuntimeError`/
`Traceback` only), so the fix is counter-compatible.

---

## Axes impacted

| axis | impact |
|---|---|
| **operability** | positive on the class (base→C0 is a real fix, proven); negative on the claim's completeness: the mode's usable arm is red at C0/HEAD and unmeasured, and its entire path is outside the counter |
| calibration | C0 introduced two record/tree disagreements (`S280` citation, `context-capture` pin); the census and `verify-round15` rows are the receipts |
| provenance | the committed base C2 receipt (`total=20`) is only reproducible with post-amendment-8 bytes; already routed as amendment 8 / `c31cdd9` |

## Smallest safe corrections

1. **C2 counter, one bounded usable arm for the ninth mode**: run
   `registry-check --rev REV --only <one cheap row>` with a fresh `TMPDIR` and require rc 0 (the
   wave-1 receipt shows this costs ~4-8 s; my fixture run was 4.4 s). It measures clone → grade →
   report and would have caught a broken usable path; it will not catch the mirror leg.
2. **`tools/registry-check.py` selftest, one mirror case**: create a sibling `*-shokunin` dir beside
   the fixture lane and assert a row reading `../<sibling>/…` holds under `--rev`. That is the only
   cheap place the mirror leg can be covered; without it, the note's coverage claim must be narrowed
   to "the clone leg".
3. **Close the two C0 defects** (they keep the lane's own gate red at HEAD):
   cite `S280` in `corpus/knowledge/scratch-root-contract.md` (B2 id-or-path), and append the moved
   `tools/context-capture.py` digest to `verify.py`'s `PIN_MAINTAINED_TOOL_SHA256` per the round-53
   re-pin rule (C0 `f1043425…`, HEAD `831b7810…`).
4. Note wording (C0 lines 82-84): qualify "its usable path is covered by the tool's own self-test" to
   the clone leg, or delete it once (1)+(2) exist.

## Artifacts opened

`contract.json`, `freeze.json` (both the `e2979f2` bytes and the manifest at `4c04c1d`),
`.ufo/evidence/round-55/c2/measure.py` (`0458f632…`) and its `e2979f2` blob (`36ca47d3…`),
`.ufo/evidence/round-55/before/c2.stdout`, `tools/registry-check.py` at base/C0/HEAD,
`tools/registry.json` (56 rows), `corpus/knowledge/scratch-root-contract.md` at C0 and HEAD,
`SKILL.md` (scratch rule, registry-row rule, registry-check row), `.ufo/evidence/round-15/verify.py`
(pin blocks at base and C0), `.ufo/evidence/kaika-round-1/sources-census-v2.sh`, `corpus/SOURCES.md`
(S280 row + round-55 block), `LOG.md` at C0, wave-1 receipts
`T55W1ExecModeDiscovery-receipts/r08-registry-check-rev-usable.txt`,
`T55W1ScribeCells-receipts/registry-gate-row.out`, `.ufo/waves/round-55/spec-w2.json` (this item),
and the commits `9cf0146`, `e2979f2`, `133b2ce`, `c31cdd9`, `4f7a704`, `51d1f0e`, `4c04c1d`.
