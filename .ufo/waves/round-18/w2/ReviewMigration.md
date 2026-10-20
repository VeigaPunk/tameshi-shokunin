# ReviewMigration — round-18 disposition migration (wave 2, reviewer)

Seat: TameshiR18.ReviewMigration (reviewer). Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
Clone: `/tmp/tameshi-r18w2-ReviewMigration-mA6N4b/fleet/tameshi-shokunin`, a fleet-mirror clone with siblings symlinked and HEAD detached at the read rev. The local `master` (= `origin/master`) is `01d586d`.
Every gate run used bwrap with the fleet bound read-only, the network off, `env -i`, `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`. Each tamper control ran in its own `/tmp` clone-of-clone. This report is my only write to the lane. Nothing was installed.

Axes: calibration (do the manifest and registry claims mean what they say) and operability (the registered commands and their documented outcomes). Depth is not touched.

## Answer to the target questions

| Question | Answer | Evidence |
|---|---|---|
| Does `4acc607` hold the `49e9e5e2…` bytes pinned for `tools/bash-witness-study.py`? | **Yes** | `git show 4acc607:tools/bash-witness-study.py \| sha256sum` → `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`. This equals `.ufo/evidence/round-13/expected.json:11`. `git ls-tree 4acc607` gives `100755 blob 48a89b32…`. The same blob is at `183f87b` (diff header `index 48a89b3..bac6330`), so the bytes were unchanged from `4acc607` to `183f87b`. They moved only at `58e5d53`, to `8dfaa25a…`. `git merge-base --is-ancestor 4acc607 01d586d` → exit 0. The waiver reason says the round-13 receipts ran on these bytes; `.ufo/evidence/round-13/verification.json:11` (`measured_input_sha256`) records `49e9e5e2…`, which confirms it. |
| How does round 18 differ from round 17's manifests? | **Only the new waiver** | `diff round-17/dispositions.json round-18/dispositions.json` → exit 1. The only hunk is `+tools/bash-witness-study.py {rev 4acc607…, reason …}` (`round-18/dispositions.json:20-23`). The `-before` pair gives the same single hunk. `rows`, `inputs`, `expected_file` and `supersedes` are byte-identical. |
| Do the round-18 manifests give exit 0 (11 effective + 1 superseded) and exit 1 (`producer_before`)? | **Yes** | Gate runs 1 and 2 below. |
| Do the round-17 manifests now exit 2? | **Yes** | Gate runs 3 and 4 below. The id is `expected_input_digest_mismatch` on `tools/bash-witness-study.py`, observed `8dfaa25a…`, expected `49e9e5e2…`. |
| Registry state | **As stated** | `round18` and `round18-before` are active. Both round-17 rows are superseded, and the round-14 row's `superseded_by` now points at round 18. The superseded rows still run, and `got=2` stays visible. |
| Is anything a silent pin edit? | **No** | Pinned evidence bytes are unchanged. No digest was rewritten. No registry `expect` was relabelled. The waiver can only be added after the move (control C1) and is the minimum needed (C6, C7c). Details are under "Verified" below. |

## Findings, by severity

### F1 — medium: QUALITY 24 mention sweep not done at the read rev (a doc debt, not a pin edit)

The round-18 tool move changed the outcome of the registered round-17 commands from 0 and 1 to 2 (gate runs 3 and 4). QUALITY 24 (`corpus/QUALITY.md:136-140`) requires that "every mention of the old outcome is swept in that round". The page's own rule says the same (`SKILL.md:1828`, "Re-pin or supersede in the same round; sweep every mention").

At `01d586d` the operative page still sends readers to the round-17 manifests and states their old outcomes:

- `SKILL.md:1601`: "live entry since round 17: `.ufo/evidence/round-17/dispositions.json`". That command now exits 2.
- `SKILL.md:1681`: "Live entry: `--dispositions .ufo/evidence/round-17/dispositions.json` → 0". It is observed as 2.
- `SKILL.md:1835-1838` (round-17 recipe, "from this lane root"): step 1, `round-17/dispositions-before.json` → 1; step 2, `round-17/dispositions.json` → 0 clean. Both are observed as 2.
- `SKILL.md:1850`: the round-17 registry table still lists the round-17 manifest as the gate command.
- `SKILL.md:1586`: "Live-tree form: the round-17 re-pin section", which points at the stale recipe above.
- The only swept mention is `SKILL.md:1930`: "(the round-17 manifests are superseded)". It names `.ufo/evidence/round-18/dispositions.json` but gives no command and no outcome. `dispositions-before.json` for round 18 appears nowhere in SKILL.md (a grep for `round-18/dispositions` matches only `:1930`).

**Effect.** An operator following `SKILL.md:1835-1838` gets exit 2 where the page promises 1 and 0. Any cold-read bucket containing `:1601`, `:1681` or `:1814-1853` will correctly record `wrong-expectation` at `01d586d`. This repeats the round-16/17 "partial sweep" class (`corpus/lessons/round-17.md:56`).

**Smallest fix (append-only, like round 17's treatment of `:1681`):**
- Annotate `:1601`, `:1681`, `:1835-1838` and `:1850` with: "superseded in round 18: returns 2 `expected_input_digest_mismatch` (`tools/bash-witness-study.py` moved)".
- Point those lines at `--dispositions .ufo/evidence/round-18/dispositions.json` → 0 clean (11/1, three `HISTORICAL` lines) and `round-18/dispositions-before.json` → 1 (`producer_before`).
- Give both round-18 commands and their outcomes a line in the round-18 table (`SKILL.md:1923-1932`). This also repairs F4.

### F2 — low: build commit `58e5d53` is registry-red

`58e5d53` contains both the tool move and the round-18 manifests, so the manifests themselves are atomic. The registry supersession landed separately in `e08271a`, 14 s later.

At `58e5d53` the round-17 rows are still active:
- `registry-check.py --rev 58e5d53 --only evidence-disposition-round17` → exit 1, `ROW … expect=0 got=2 differs`.
- `--only evidence-disposition-round17-before` → exit 1, `expect=1 got=2 differs`.

This happened inside the round, so the "same round" clause of QUALITY 24 holds, and the graded receipts are at `e08271a`. However, `58e5d53` must not be cited as a registry-green rev.

### F3 — minor: the `mutate-and-run.sh` waiver reason was not updated for its round-18 move

`round-18/dispositions.json:14` (and `-before:14`) copies the round-17 reason ("round 16 … and round 17 …"). The runner moved again in round 18: `fb6d86d5…` at `183f87b` → `d22c4025…` at `58e5d53`, a 102+/28− diff adding leg 8. The reason is informational and not machine-checked; G1 and G2 enforce the substance and pass. The text is still incomplete.

### F4 — minor: the lineage from round 17 to round 18 is not recorded in the manifest, and one registry `source` is weak

- G7 forces `supersedes` to point at a v1 document (`tools/evidence-disposition.py:1509-1510`), so round 18 supersedes round 14 directly (`round-18/dispositions.json:4`).
- The round-17 manifests are not pinned in round 18's `inputs` (`:5-10`). Wave 1 suggested pinning them (`w1/K05MigrationIntegrity.md:33-35`); that was not adopted.
- I verified that the delta is purely additive (diff above), but no tool enforces it. Only the registry `superseded_by` (`tools/registry.json:222,249`) records the lineage.
- Row `evidence-disposition-round18-before` cites `source: SKILL.md@58e5d53:1923-1932` (`tools/registry.json:299`). That range never names its manifest or its admitted outcome.

### F5 — disclosed tradeoff, not a defect: committed edits to the newly waived tool now pass the disposition gate

Control C3 (scratch branch, a committed one-line edit, tool sha `28c82622…`) → exit 0 clean. This was disclosed in round 17 (`corpus/lessons/round-17-verifier-spotcheck.md:284-285`: "Committed edits to a waived tool are deliberately accepted"). Round 18 extends it to a third tool.

The live bytes are still exercised elsewhere:
- Registry rows `bash-witness-selftest` and `bash-witness-count` held at `e08271a` (`.ufo/evidence/round-18/registry-full-e08271a.stderr:4-5`).
- My run of `python3 tools/bash-witness-study.py selftest` in a scratch clone at `01d586d` → exit 0, `WITNESS_SELFTEST: 43/43 pass`, including both new `GIT_DIR/GIT_WORK_TREE` canary checks. The count was 41/41 at `4acc607`, which is a historical record (`expected.json:49-51`, `SCORECARD.md:245`). `SKILL.md:1504` states no count, so nothing is stale there.
- Probe P11 is closed at `e08271a` (`.ufo/evidence/round-18/c2-probes-v2-e08271a.txt:11`) and open at `183f87b` (`c2-probes-v2-183f87b.txt:11`).

The new digest `8dfaa25a…` appears in the round-18 receipts only incidentally, in the superseded rows' stdout tails (`registry-full-e08271a.json:156,175,219`).

## Verified (no finding)

1. **Pinned evidence is unchanged.**
   - `git diff --stat 183f87b 01d586d -- .ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14 .ufo/evidence/round-17` → empty.
   - `expected.json`, `verification.json` and `producer-oracle-repair.json` were last touched in `4acc607`. The only later round-13 commit, `7dd16d9`, added `after-committed.json` only.
   - The round-14 manifests were last touched in `0c6e36d`; the round-17 manifests only in `2a22ade`.
   - Hashes at `01d586d`: `expected.json` `a0160794…`, `verification.json` `a02718e9…`, `producer-oracle-repair.json` `df83a729…`, round-14 `77faac58…`/`a7a965bb…`, round-17 `55cf1b5d…`/`79f0b397…`, round-18 `9caa2f76…`/`dc948a5e…`. These match every pin that names them.
2. **The waiver set is minimal and drift-derived.** The live tools at `01d586d` are:
   - `bash-witness-study.py` `8dfaa25a…` (pin `49e9e5e2…`)
   - `mutate-and-run.sh` `d22c4025…` (pin `75ed934d…`)
   - `pin-disposition.py` `331529ea…` (pin `29725397…`)
   - `witness-metadata.py` `df339068…`, which equals its pin and is correctly not waived.

   Controls C1, C6 and C7c below show the waiver is required and could not be added early.
3. **Tool change scope.** `git diff 183f87b 58e5d53 -- tools/evidence-disposition.py` changes only the G2/G3 anchor (HEAD → `lane.branch` or attached branch tip, or a detached HEAD contained by some ref) and adds selftest cases. Integrity-first hashing (`:1586-1599`) and the expected-input mismatch path (`:1633-1644`) are untouched.

   `git diff 183f87b 58e5d53 -- tools/bash-witness-study.py` contains:
   - `git_clean_env()` applied to `materialize_target` and `sweep_env`
   - `env_facts` now lists `"GIT_*"`
   - two canary selftest checks
   - a private tmp root

   This matches the "C2 P11" reason.
4. **The registry edit is explicit.**
   - `git show e08271a -- tools/registry.json` only changes `status` and `superseded_by` and adds rows. The round-17 rows keep `expect` exit 0 and 1 (`tools/registry.json:209,237`); they were not relabelled to 2.
   - The round-14 row's target was retargeted to round 18 (`:323`), with `expect {exit:0}` unchanged.
   - Superseded targets must be active (`tools/registry-check.py:270-291`), and superseded rows still run (`:30-35`).
   - Receipt `registry-full-e08271a.stderr:10-14,36` shows the superseded rows at `got=2`, the round-18 rows held, and `REGISTRY_CHECK: held=32/32 superseded=3`.
   - `tools/` is identical from `e08271a` to `01d586d` (`git diff --stat` is empty).
5. **The frozen replay is unaffected** (`SKILL.md:1581-1585`, `:1681`). In a `git archive 28aeef4` tree with the archived tool: round-14 `-before` → 1 (`producer_before`); round-14 → 0 clean (11/1).

## Commands and exits

Gate runs at `01d586d`. Each command is `python3 tools/evidence-disposition.py --root . --dispositions <m> --json`, run from the clone under bwrap.

| # | Manifest | Exit | Key output |
|---|---|---|---|
| 1 | `.ufo/evidence/round-18/dispositions.json` | **0** | `clean`; effective 11, superseded 1, passed 11; `HISTORICAL tools/bash-witness-study.py rev=4acc607… sha256=49e9e5e2…`, plus `mutate-and-run.sh` → `75ed934d…` and `pin-disposition.py` → `29725397…` |
| 2 | `.ufo/evidence/round-18/dispositions-before.json` | **1** | `failed`; finding `expected_contains_missing` / `producer_before`; effective 12, failed 1 |
| 3 | `.ufo/evidence/round-17/dispositions.json` | **2** | `expected_input_digest_mismatch`: `tools/bash-witness-study.py` observed `8dfaa25a…` expects `49e9e5e2…` |
| 4 | `.ufo/evidence/round-17/dispositions-before.json` | **2** | same as run 3 |
| 5 | `.ufo/evidence/round-14/dispositions.json` | 2 | same id; `bash-witness-study.py` is the first sorted pin |
| 6 | `.ufo/evidence/round-14/dispositions-before.json` | 2 | same |
| 7 | round-18 manifest, text mode | 0 | 12 `ROW` lines plus the three `HISTORICAL` lines |

Controls with the real manifests (a scratch clone at the read rev unless noted):

| Control | Setup | Exit | Id / output |
|---|---|---|---|
| C1 | round-18 manifests against a `183f87b` tree (before the move) | 2, 2 | `historical_input_unneeded` for `tools/bash-witness-study.py`, so the waiver cannot predate the move |
| C2 | uncommitted one-line edit to `tools/bash-witness-study.py` | 2 | `historical_input_uncommitted` ("live bytes differ from HEAD:…") |
| C3 | the same edit committed on a scratch branch | 0 | clean (F5, disclosed) |
| C4 | one byte appended to `.ufo/evidence/round-13/verification.json` | 2 | `input_digest_mismatch` (observed `d2917c63…`, expects `a02718e9…`) |
| C5 | manifest copy waiving `.ufo/evidence/round-13/verification.json` | 2 | `historical_input_forbidden` |
| C6 | manifest copy also waiving the unchanged `tools/witness-metadata.py` | 2 | `historical_input_unneeded` |
| C7a | waiver rev set to `9df9212d…`, the round-12 blob `249d9dcd…` | 2 | `expected_input_digest_mismatch`; the content stays pinned by sha256 |
| C7b | waiver rev set to `183f87b…`, which holds the same blob | 0 | clean. The rev is provenance only; the sha256 guards the content |
| C7c | the bash-witness waiver removed | 2 | `expected_input_digest_mismatch`, so the waiver is necessary |
| C8 | scratch clone with `git config lane.branch master` | 0 / 1 | bound-anchor path: round-18 clean, `-before` gives `producer_before` |
| C9 | `git archive 28aeef4`, archived tool, round-14 v1 `-before` / main | 1 / 0 | frozen replay intact |

Registry checks:
- C11: `python3 tools/registry-check.py --rev 01d586d… --only <row>`. Each run exits 0:
  - `round18`: `expect=0 got=0 held`
  - `round18-before`: `expect=1 got=1 held`
  - `round17`: `superseded expect=0 got=2`
  - `round17-before`: `superseded expect=1 got=2`
  - `round14-superseded`: `superseded expect=0 got=2`
- C12: `--rev 58e5d53 --only evidence-disposition-round17` and `--only …-round17-before` → exit 1, `differs` (F2).

Other commands:
- `git -C $C log --format='%h %s' -- <round-13 pins | round-14/17/18 manifests | tools/bash-witness-study.py>`
- `git show <rev>:<tool> | sha256sum` for revs 9df9212, 4acc607, 2a22ade, 183f87b, 58e5d53, e08271a and 01d586d, over all four pinned tools

Cited file hashes at `01d586d`:

| File | sha256 |
|---|---|
| `tools/registry.json` | `d2d1972e…` |
| `tools/evidence-disposition.py` | `66655a3a…` |
| `tools/registry-check.py` | `e072fd39…` |
| `SKILL.md` | `2e20e549…` |
| `corpus/QUALITY.md` | `ffed5023…` |
| `corpus/lessons/round-17-verifier-spotcheck.md` | `62869c87…` |
| `.ufo/evidence/round-18/registry-full-e08271a.stderr` | `f21d6eb4…` |
| `.ufo/evidence/round-18/c2-probes-v2-e08271a.txt` | `e61e777b…` |

## Residual risk and verification gaps

- No `lsp` device exists in this session's `xd://` inventory. Caller and definition checks came from direct reads and literal grep; they are not semantic proof.
- I did not rerun the full registry at `01d586d`, only the five disposition rows. The 32/32 figure rests on the `e08271a` receipt plus `tools/` being identical from `e08271a` to `01d586d`.
- I did not exercise the live lane (jj-colocated, with its own `lane.branch` binding), as the contract requires. C8 simulates a bound `lane.branch` in a scratch clone only.
- I am not a CR seat, so these commands were not wrapped in `trace-inputs.py`. The scratch outputs are under `/tmp/tameshi-r18w2-ReviewMigration-mA6N4b/out/` and are not lane evidence.

Verdict: **partial.** There is no silent pin edit. The bytes at `4acc607` match the pin, the only manifest change is the waiver, the four gate outcomes reproduce (0, 1, 2, 2), and the registry supersession is explicit and still runs. But at `01d586d` the migration has not yet swept QUALITY 24's mentions: `SKILL.md:1601/1681/1835-1838/1850` still give round-17 outcomes that are now exit 2 (F1).
