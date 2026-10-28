# T54W1Read19 — cold read: `## Live-tree re-pin and entry-command monitor — round 17`

- heading: `## Live-tree re-pin and entry-command monitor — round 17`
- cand: 59c38109bf119d0e9d4f878644a82babc937bc1e
- span at C0: lines 1840-1870 (reader-section.py printed start=1840 end=1871; 1871 is the blank line before `### Round-17 gate/probe registry — re-pin and monitor`, which the frozen round-18 sectionize strips, leaving 31 lines)
- section_sha256 (as printed by reader-section.py): 037c9df3076fc7ada495b906b9bf458e9d06099bfaf9d1270b88de0acb4151f3
- every byte below was read with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md`; no working-tree read.

## Findings

### F1 — the scrub anchor stops one line short of the code it names

quote:

`tools/evidence-disposition.py:368-390`

why: At C0 that range ends on the opening brace GIT_ENV_OVERRIDES = { at line 390, so the constants the cell names (GIT_NO_REPLACE_OBJECTS and GIT_GRAFT_FILE, lines 391-392, closing brace 395) fall outside it; C0's own +5-line ScratchRootUnusable insertion pushed the block from 385-390 out of the cited range.

### F2 — the detached-anchor range no longer covers the decision

quote:

`tools/evidence-disposition.py:460-525`

why: At C0 resolve_historical_anchor runs 479-544, so 460-525 begins inside the shallow-repository check and stops at the for-each-ref argument list, excluding the containing_refs filter (535-538) and return "HEAD", commit (544) that implement the raw-HEAD anchor the cell cites.

### F3 — the selftest range names a different case with the opposite exit

quote:

selftest `v2-registry-clone-detached-anchor` :2891-2896 expects exit 0

why: At C0 lines 2891-2896 hold the v2-historical-tag-object case, which expects exit 2, while v2-registry-clone-detached-anchor with exit 0 sits at 2910-2915, so the cited range names a different selftest with the opposite expected exit.

### F4 — the fixture-docstring line points at a stray parenthesis

quote:

fixture docstring :2256 "anchors at HEAD"

why: At C0 line 2256 is a bare closing parenthesis inside _setup_hist_jj_branch_tip; the docstring 'A detached harness clone anchors at HEAD, not its later remote tip.' is at 2275, inside _setup_hist_registry_clone.

## What I opened and what I checked

Recomputed the section sha from the blob with the frozen round-18 sectionize (`git show C0:.ufo/evidence/round-18/measure.py`, `sectionize` at :209-249) to confirm the printed sha is the sha of these 31 lines:

    $ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
    $ python3 .ufo/waves/round-54/reader-section.py "$PWD" \
        59c38109bf119d0e9d4f878644a82babc937bc1e \
        "## Live-tree re-pin and entry-command monitor — round 17"
    {"heading": "## Live-tree re-pin and entry-command monitor — round 17",
     "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e",
     "start": 1840, "end": 1871,
     "section_sha256": "037c9df3076fc7ada495b906b9bf458e9d06099bfaf9d1270b88de0acb4151f3"}

Line anchors, all read at C0 (`git show 59c38109bf11:tools/evidence-disposition.py`, 3246 lines):

    $ awk 'NR==390||NR==391||NR==392||NR==395||NR==460||NR==479||NR==525||NR==535||NR==538||NR==544||NR==2256||NR==2275||NR==2891||NR==2892||NR==2896||NR==2910||NR==2911||NR==2912{printf "%d: %s\n", NR, $0}' evidence-disposition.py
    390: GIT_ENV_OVERRIDES = {
    391:     "GIT_NO_REPLACE_OBJECTS": "1",
    392:     "GIT_GRAFT_FILE": "/dev/null",
    395: }
    460:     if proc.returncode != 0 or proc.stdout.decode("utf-8", "replace").strip() != "false":
    479: def resolve_historical_anchor(lane):
    525:             "for-each-ref",
    535:     containing_refs = [
    538:     ]
    544:     return "HEAD", commit
    2256:         )
    2275:     """A detached harness clone anchors at HEAD, not its later remote tip."""
    2891:     historical_case(
    2892:         "v2-historical-tag-object",
    2896:     )
    2910:     historical_case(
    2911:         "v2-registry-clone-detached-anchor",
    2912:         0,

Provenance of the drift: the four cited anchors resolved exactly at the round-52 commit 7ff81a5 that introduced the bracket (`git log -S"[round 52: when bound the anchor" -- SKILL.md` -> 7ff81a5), where `git show 7ff81a5:tools/evidence-disposition.py` puts GIT_ENV_OVERRIDES at 371, resolve_historical_anchor at 460, the "anchors at HEAD" docstring at 2256 and the `v2-registry-clone-detached-anchor` case at 2891-2896. At base d33053f7552d the file is already +14 lines (`git show d33053f7552d:tools/evidence-disposition.py`: GIT_ENV_OVERRIDES at 385, docstring at 2270, case at 2910, function at 474); C0's ScratchRootUnusable block (diff hunk `@@ -188,15 +188,20 @@`) adds 5 more, making it +19 and moving all four anchors out of the cited text.

Comparative anchors I resolved at C0 (no defect):

    $ grep -n "anchors at HEAD\|v2-registry-clone-detached-anchor" evidence-disposition.py   # C0
    2275:    """A detached harness clone anchors at HEAD, not its later remote tip."""
    2911:        "v2-registry-clone-detached-anchor",
    $ grep -n "v2-historical-replace-ref\|v2-gitdir-env" -A 2 evidence-disposition.py
    2929:        "v2-historical-replace-ref", 0, []   # expects exit 0
    2944:        "v2-gitdir-env",             0, []   # expects exit 0

Recipe outcomes, run from the lane root read-only (TMPDIR inside my own scratch):

    $ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json; echo exit=$?
    {"counts": {"effective": 12, "expected_checks": 12, "failed": 1, "findings": 1, "passed": 11, "superseded": 0}, ... "exit": 1 ...}
    exit=1                                   # and the finding carries "expectation": "producer_before"

    $ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json; echo exit=$?
    {"counts": {"effective": 11, "expected_checks": 12, "failed": 0, "findings": 0, "passed": 11, "superseded": 1}, ... "exit": 0 ...}
    exit=0

    $ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json | grep -c '^HISTORICAL '
    3                                        # = the three historical_inputs, one line per waived instrument
    $ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json >/dev/null 2>&1; echo exit=$?
    exit=2
    $ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json >/dev/null 2>&1; echo exit=$?
    exit=2                                   # "round 17's two now exit 2" holds

Counts read straight out of the committed manifests (`.ufo/evidence/round-18/dispositions.json`): 12 rows, 11 `effective`, 1 `superseded` (producer_before, superseded_by producer_before_oracle + producer_after_oracle), 3 `historical_inputs`, 4 `inputs`. This matches the cell `"effective": 11`, `"superseded": 1` exactly.

Other cited surfaces, each opened at C0 and found to hold:

- `corpus/SOURCES.md`: S061 row (:70, jj detached at the working-copy commit's parent = `@-`), S062 (:71, `--show-toplevel`), S063 (:72, discovery and `GIT_*`), plus S076 (:85, supersedes S061's paragraph anchor only, conclusion stands) - the Sources line resolves.
- `corpus/lessons/round-16-verifier-spotcheck.md` §3 (:123) and §6 (:214) exist and route R16-OP1 (§3) and R16-MON1 (§6), as the Sources line states.
- `tools/registry-check.py`: `print_human` (:901-918) writes `ROW ... differs` and ends with `REGISTRY_CHECK: held={held}/{total} superseded={superseded}`; exit 1 when held < active (:899); superseded rows are still run and only labelled (`run_row` over `selected`, then partitioned at :887-893); siblings symlinked beside the clone (:796). All three recipe-step-3 sentences hold.
- `tools/pin-disposition.py`: head rows carry `branch` (:403, :426) and `head_differs_from_branch` (:408, :445); recipe step 4 holds.
- `tools/mutate-and-run.sh`: `SETUP (repo_identity_mismatch: ...)` at :1263 with exit 2 in the regression leg; last table row holds.
- "Every lane tool scrubs `GIT_*` before git": swept all 31 files in `tools/` for the literal `git`/`git -C` and for a `GIT_`-dropping env. Ten tools call git and each builds an environment that drops inherited `GIT_*`: `bash-witness-study.py:355`, `env-diff.py:56`, `evidence-disposition.py:407`, `pin-disposition.py:228,770`, `receipt-measure.py:50`, `registry-check.py:154`, `registry-replay.py:58`, `round21-measure.py:32`, `trace-inputs.py:512,746`, `mutate-and-run.sh:270-284` (every git call through `git_clean`). `.ufo/evidence/round-18/measure.py:144` and `.ufo/evidence/round-21/coldread/measure.py:34` also scrub. `.ufo/evidence/round-16/measure.py:412-415` sets `GIT_CONFIG_*`/identity but drops no inherited `GIT_*`, exactly as the cell says, and `registry-check.py`'s own git env (:154) does scrub before it replays that script.
- `tools/vendor/` holds only tarballs; the lane has no `scripts/` git caller.

One sentence I considered and did **not** report: table row 2 says the anchor is "not `HEAD`", its round-52 bracket says an unbound non-jj detached root "anchors at raw `HEAD`", and recipe step 4 says "never at `HEAD`". The three are conditioned on different subjects (tool-internal anchor when bound vs the documented unbound case vs who a human reads), so I could not defend this as a same-section contradiction and left it out rather than invent one.

## Scratch and scope

- All reads were `git show`/`grep`/`python3 -c json.load` against the lane at C0 or against committed blobs; no lane file edited, no git/jj mutation, no `git add`/commit. Working tree untouched apart from the two deliverables written to `.ufo/waves/round-54/w1/`.
- Scratch tree `/fast/scratch/hyaku/tameshi-r54/T54W1Read19` (TMPDIR for reader-section.py and the two recipe runs) removed on exit; nothing left behind.
- No tool installs or upgrades were needed.
