# T55W1ScribeSkill — C2 rule sentence (`SKILL.md` `## Standing rules`)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (base `0a2010ac`, lane HEAD
`631cd6455e58dce969310b4c0466c3383d9f5108`). Judged on: operability. Milestone:
C2 SKILL.md rule sentence.

Item: read `## Standing rules`, draft the exact old→new replacement for the
round-54 sentence `Measured on each tool's --selftest/selftest path (round-54 C2
counter); other modes are outside that measurement`, keep line length and the
section's citation style, touch nothing else, and quote the section's sha256 at
base so the L1 can prove the drift is one section.

No lane production file was edited by this seat. Every measurement below ran in a
scratch clone (`/fast/scratch/hyaku/tameshi-r55/T55W1ScribeSkill/clone`, own git
toplevel, asserted before its only commit). Nothing was committed in the lane.

---

## 1. The exact replacement (base blob `SKILL.md`, `## Standing rules`)

Old (base lines 37–39, the tail of the third-arm bullet; verbatim):

```
  1. Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter);
  other modes are outside that measurement (corpus/knowledge/scratch-root-contract.md;
  the seven registry `scratch_root` cells).
```

New (7 lines replacing those 3; the rest of the bullet and the section are byte-identical):

```
  1. Measured on every allocating mode the seven registry cells name — the
  seven self-tests plus `env-diff --contract` — as one stderr line, exit 2:
  `<tool>: could-not-evaluate: cannot create clone scratch under the scratch root:
  TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`; the five
  non-allocating modes stay lazy (round-55 C2 counter;
  corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root`
  cells).
```

The bullet as it reads after the edit (`skill-after.md` lines 32–43) — paste this
whole bullet if replacing the working-tree draft:

```
- **The scratch root has three arms.** A tool that allocates scratch through
  `strict_scratch_root()` honours `TMPDIR`: unset → the platform default; empty
  (`TMPDIR=""`) → unset (the resolver skips an empty candidate, S278:163-165; the
  documented list follows, S279); set but unusable → exit 2, could-not-evaluate,
  naming the value — never a silent `/tmp` fallback, never a traceback, never exit
  1. Measured on every allocating mode the seven registry cells name — the
  seven self-tests plus `env-diff --contract` — as one stderr line, exit 2:
  `<tool>: could-not-evaluate: cannot create clone scratch under the scratch root:
  TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`; the five
  non-allocating modes stay lazy (round-55 C2 counter;
  corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root`
  cells).
```

Patch against the base blob (`git diff` of the demonstration commit,
`-receipts/skill-section.patch`):

```diff
@@ -34,9 +34,13 @@ Appendix A/B mutants (`.ufo/evidence/kaika-round-1/coldread/`); round 16 adds a
   (`TMPDIR=""`) → unset (the resolver skips an empty candidate, S278:163-165; the
   documented list follows, S279); set but unusable → exit 2, could-not-evaluate,
   naming the value — never a silent `/tmp` fallback, never a traceback, never exit
-  1. Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter);
-  other modes are outside that measurement (corpus/knowledge/scratch-root-contract.md;
-  the seven registry `scratch_root` cells).
+  1. Measured on every allocating mode the seven registry cells name — the
+  seven self-tests plus `env-diff --contract` — as one stderr line, exit 2:
+  `<tool>: could-not-evaluate: cannot create clone scratch under the scratch root:
+  TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`; the five
+  non-allocating modes stay lazy (round-55 C2 counter;
+  corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root`
+  cells).
```

Line widths: 74, 75, 82, 77, 54, 78, 9 — the section's pre-existing prose max is
82 (old line 36) and its one intentional long line (line 28) is untouched.
Wrapping matches the section's style (two-space continuation, `—` dashes, the
`(round-55 C2 counter; path; the seven registry \`scratch_root\` cells)` citation
tail). Wording choices against the working-tree draft (see §5):

- `exit 2` stated, because the frozen grammar is a line **and** an exit class.
- "the seven registry cells name" instead of "every documented allocating mode":
  the cells name exactly eight modes and the counter measures exactly eight; a
  broader phrase is false (§4 F1).
- The 70-char marker is kept contiguous on one physical line (line 3), so the
  **un-amended** frozen predicate (`MARKER in skill_txt`, raw) also scores
  `skill=1`; the draft in the lane's working tree relies on amendment 2's
  whitespace normalization.

## 2. Drift accounting — one section, provable

Command (round-18 `sectionize`, the function the cold-read ledger uses):

```
python3 - <<'PY'   # importlib-load .ufo/evidence/round-18/measure.py, call sectionize()
raw = git show 0a2010ac…:SKILL.md ; new = read(clone/SKILL.md)
compare {heading: sha256}
PY
```

Measured (`-receipts/section-drift.txt`):

```
BASE_start=17 BASE_end=40 BASE_sha256=61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc
NEW_start=17  NEW_end=44  NEW_sha256=aca6189098fb902c3c51887872f522ea821f5300e356dd110b9d8ee032831165
changed_headings=['## Standing rules']
headings_added=[] headings_removed=[]
base_sections=64 new_sections=64
base_bytes=199128 new_bytes=199376 delta=248
```

So the re-key the round owes is `## Standing rules`: `61736dce…` → `aca61890…`,
at the content commit. Exactly one of 64 sections drifts; the patch hunk
(`@@ -34,9 +34,13 @@`) removes the three old lines and touches nothing else in the
section or the file.

For comparison, the lane working tree as it stands carries a **different, earlier
draft**: `SKILL.md` sha256 `a157f37d8915d460c0694b5eb660db48f37d9c3ce99e9d13917e74f01ec55545`,
`## Standing rules` section sha `4f959fd727cdb630d2507de403b2cb20ae5c14ccc170c527a0d708f997e08b9b`
(lines 17–43). The patch above is against the base blob, so it will not apply to
that tree; paste the 7-line block over lines 37–42 of the working tree instead.

## 3. Why each clause is true (measured, not asserted)

Demonstration clone: lane HEAD + the working-tree `tools/repeat-control.py`,
`tools/context-capture.py`, `tools/registry.json`,
`corpus/knowledge/scratch-root-contract.md` (sha256s in
`-receipts/inputs.sha256`), plus this `SKILL.md` block → local commit
`2e0dbbc6440e6ef992c3b889d2ec6b6e988f4716` in the seat clone.

**Frozen C2 counter** (lane's counter, sha256 `d6ca1d851bb0037368c304f4d80254f7dc5bf76b1c3119cdf0f2a64bca95631a`,
i.e. with the L1's amendments 1–4):

```
python3 .ufo/evidence/round-55/c2/measure.py --lane <seat clone> --rev 2e0dbbc6440e… --work <empty> --explain
C2_R55: rev=2e0dbbc6440e grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0
        docs=7/7 note=8/8 skill=1/1 total=0 C2_R55_PASS=true   (exit 0)
```

(`-receipts/c2-demo.out`, `-receipts/c2-demo-receipts.json`; `bad={}`.)

**The sentence's own claims**, independent sweep of the same 13 modes plus one
extra, all with `TMPDIR=<nonexistent>` (`-receipts/mode-sweep.json`):

| mode | rc | stderr lines | frozen GRAMMAR match | `RuntimeError`/`Traceback` |
|---|---|---|---|---|
| env-diff --selftest | 2 | 1 | 1 | no |
| env-diff --contract | 2 | 1 | 1 | no |
| repeat-control --selftest | 2 | 1 | 1 | no |
| registry-check --selftest | 2 | 1 | 1 | no |
| bash-witness-study selftest | 2 | 1 | 1 | no |
| pin-disposition --selftest | 2 | 1 | 1 | no |
| evidence-disposition --selftest | 2 | 1 | 1 | no |
| context-capture --selftest | 2 | 1 | 1 | no |
| repeat-control --snapshot | 0 | 0 | – | no |
| bash-witness-study count | 0 | 0 | – | no |
| pin-disposition --read | 0 | 0 | – | no |
| evidence-disposition --json | 0 | 0 | – | no |
| context-capture --check | 0 | 0 | – | no |

"One stderr line" is literal: exactly one non-blank stderr line for each of the
eight, and it is the one the frozen regex matches. The eight per-tool prefixes are
`ENVDIFF_SETUP`, `repeat-control`, `registry-check`, `WITNESS_STUDY`,
`pin-disposition.py`, `evidence-disposition.py`, `context-capture.py` — all inside
the grammar's `[A-Za-z][A-Za-z0-9_.-]*(\.py)?`.

"Non-allocating modes" is code-level, not only behavioural: the only
`strict_scratch_root()` call sites in the seven tools are `selftest()` /
`cmd_selftest()` / `SelftestHarness` / `env-diff.execute()` /
`registry-check.clone_lane_at_rev()` (`grep -n strict_scratch_root tools/*.py`), and
none of the five lazy modes reaches them — hence rc 0 with no stderr line.

**Marker under both matchers** (`-receipts/skill-arm-both-matchers.txt`):

```
HEAD-frozen predicate  skill = 1 if MARKER in skill_txt else 0        -> 1
amended predicate      skill = 1 if MARKER in norm(skill_txt) else 0  -> 1
```

## 4. Findings — reported, not fixed

**F1 (operability, needs an L1 decision). `registry-check --rev` is a documented
allocating mode that the frozen 13-mode table does not measure, and it prints the
class on stdout, not stderr.** Evidence, in the demonstration clone:

```
$ TMPDIR=<nonexistent> python3 tools/registry-check.py --rev HEAD --root .
rc=2
stdout: REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the
        scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate))
stderr: (empty)
```

(`-receipts/mode-sweep.json`, last row; earlier direct probe identical.) Code:
`tools/registry-check.py:770 def clone_lane_at_rev` → `:780 tempfile.mkdtemp(...,
dir=strict_scratch_root())`, reached from `:1927` when `--rev` is given; `--rev` is
documented in the tool's USAGE (`registry-check.py:11`). Consequences:

- The phrase "every **documented** allocating mode" is false as written — the
  working-tree draft's wording. My block says "every allocating mode the seven
  registry cells name", which is exactly the eight the cells list and the counter
  measures, so it stays true under either reading.
- The `registry-check` registry cell says `Allocating modes: selftest.` — that is
  incomplete for `--rev` (the cell is a per-tool claim, unlike the sentence's
  cross-tool scoping).
- The class here is exit 2 with the naming line but **stdout placement**, so it
  would fail the frozen grammar's "one stderr line" if it were in the table. The
  note already discloses the general shape of this blind spot
  (`corpus/knowledge/scratch-root-contract.md`, "its blind spot is narrower but
  real… the grammar is matched on stderr, so a caller that parses stdout sees
  nothing"); this is the concrete instance. Route or disclose — not mine to fix
  (frozen counter, lane production files).

**F2 (minor, adjacent).** `repeat-control --selftest` on the refusal path writes a
status token to stdout as well as the grammar line to stderr:
`stdout: REPEAT_CONTROL: setup_error` (`-receipts/mode-sweep.json`). The frozen
grammar arm reads exit code, stderr shape and the `RuntimeError`/`Traceback`
tokens only, so the counter passes; the round's prose ("stdout carries no setup
error") can be read stricter. The sentence I drafted makes no stdout claim.

**F3 (process, unexplained).** The seat scratch tree
`/fast/scratch/hyaku/tameshi-r55/T55W1ScribeSkill` was deleted by something other
than this seat between 13:53 and 13:54 while the first counter run was in its
`usable` arm (it had already reported grammar 8/8 and lazy 5/5). The run was lost
and rebuilt from scratch: the clone, patch, sweep and verdict in this report are
the second, complete run. Sibling seat trees in the same parent were intact. Not
diagnosed further.

**F4 (no action).** Sources census: `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` exits 0
(`-receipts/census-validate.txt`). The lane's `corpus/SOURCES.md` now carries 140
`| S### |` rows, S001–S280; S280 is this round's own added row (SOURCES.md:155 and
the round-55 footer note), so the brief's "139 rows (S001–S279)" is the round-start
state, not a drift.

## 5. Integration note for the L1

- Take §1's 7-line block verbatim; it supersedes the 6-line draft now in
  `SKILL.md` lines 37–42 (`a157f37d…`).
- Re-key the cold-read ledger entry for `## Standing rules`:
  `61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc` →
  `aca6189098fb902c3c51887872f522ea821f5300e356dd110b9d8ee032831165` (§2; one
  section of 64, no headings added or removed).
- With this block in place, the frozen C2 counter reaches
  `grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8
  skill=1/1 total=0` on a tree that also carries the working-tree tool, registry
  and note edits (§3).
- My block does not need amendment 2: it satisfies the raw predicate too.

## 6. Out of scope / not verified by this seat

`SCORECARD.md` corrections, `LOG.md`, `QUALITY.md`, `corpus/lessons/round-55.md`,
the cold-read re-key itself, the deciding run, the no-harm monitors, and the
`registry.json` reformat (taken as-is from the working tree and only hashed).
No tool was installed or upgraded; system `python3`, `git`, `strace` sufficed
(pacman is paused host-wide and was not touched).

## 7. Receipts

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/`

| file | what |
|---|---|
| `skill-section.patch` | the full diff of the demonstration commit for `SKILL.md` (sha256 `60f689902a480797e78e819da75fada2a0752d7da0740da644a1fbe40ce937e6`; base index `8482934`) |
| `skill-after.md` | post-edit `SKILL.md` (199376 bytes, sha256 `995bd5f6217387f3624cfef6bd60f82080bbc0092b28a095298e363c76372526`) |
| `section-drift.txt` | base/new section sha256 + one-section-changed proof + widths |
| `mode-sweep.json` | 13 counter modes + `registry-check --rev`, unusable `TMPDIR`: rc, stderr line count, grammar match, tokens (sha256 `f3d2a543…`) |
| `skill-arm-both-matchers.txt` | raw and normalized marker predicates both 1 |
| `c2-demo.out`, `c2-demo.err`, `c2-demo.rc`, `c2-demo-receipts.json` | counter verdict line and per-arm receipt (`total=0`, exit 0); `c2-demo.out` sha256 `9ba02ceb1969fadd55b5eb2c76a520a0b3dbdd23a4f89542a68779b702a45556` |
| `RECEIPTS.sha256` | sha256 of every receipt file named in this table |
| `c2-measure.sha256` | the exact counter bytes that produced the verdict |
| `inputs.sha256` | sha256 of the four working-tree files copied into the demonstration clone |
| `demo-commit.txt` | demonstration commit id + stat |
| `census-validate.txt` | census `validate` exit 0 and row accounting |
