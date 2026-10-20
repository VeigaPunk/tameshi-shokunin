# ReviewQuality18 — QUALITY criteria 29–36 (round 18, wave 2, falsify)

Seat: `TameshiR18.ReviewQuality18` (reviewer, leaf). Read rev:
`01d586ddbc5fcd78659557c4e93a6ee8517b87d1`, used through a /tmp clone. Base for red-before:
`183f87b899e6cae46be98d251cbc87fb5118f6ca`.
Target: `corpus/QUALITY.md` `## Criteria appended — round 18` (`:169-295`) against
`corpus/lessons/round-17-verifier-spotcheck.md` §7 (`:415-454`).
Scratch: `/tmp/tameshi-r18w2-ReviewQuality18-0p9bd7` (clone at `fleet/tameshi-shokunin`, experiments
under `exp/`). Lane writes: this report only. Live-lane git: none. Every git write in the experiments
ran inside a `bwrap --ro-bind / / --tmpfs /tmp --bind $W $W --unshare-net` envelope with `env -i`.
Messages sent: none. Tool installs or updates: none (bwrap 0.13.1, git 2.56.0, Python 3.14.8, jj
0.45 were already installed).

Questions asked of each criterion: (a) is it falsifiable, (b) does it map to a routed §7 item, and
(c) has a committed red-before shown it can fail (a defect-probes base receipt or an erratum)? I
also checked whether each criterion holds at the read rev.

## Per-criterion verdict

| # | (a) Falsifiable | (b) §7 item | (c) Committed red-before | State at 01d586d | Verdict |
|---|---|---|---|---|---|
| 29 | yes. Mutant plus owning-selftest exit | item 3 | P01–P07 `open`, mutant_exit=0 (`.ufo/evidence/round-18/c2-probes-183f87b.txt:1-7`, committed in aee4f36 before the fix in 58e5d53) | v2 tip: all 7 `closed` | holds (F8 residual) |
| 30 | yes. jj fixture, branch tip vs HEAD | item 5 | P08 `open`, findings=[] at base (v1 and v2 base receipts, line 8) | tip `closed`, but the rule's "never bare HEAD" contradicts the tip's documented fallback (F5) | holds, minor gap |
| 31 | yes | item 6 (the carry-forward clause is not represented) | P09 NaN/Infinity exit 1 with traceback; P10 survivors=[5] for setsid and setpgid | tip correct. The −Infinity and boolean clauses were never red; the check misses overflow (F6) | holds, minor gap |
| 32 | yes | item 4 and criterion 28 | P11 tainted_exit=2, declared=False; X07 scrub-removed mutant 41/43, exit 1 | **The rule is false at the read rev** for an active registered tool. The check's variant cannot see it (F1) | **falls as a universal rule** |
| 33 | **partly** | item 2 | Narrowing half only: erratum `corpus/lessons/round-17.md:98-104` | Argv-binding check: no tool, no fixture, no red (F4) | **partial; binding clause prose-only** |
| 34 | yes, for definition anchors | item 7 | ER-jj2 erratum ×5 (appended); fleet `5d8a3b5` shows the miss | Paragraph-anchor clause unchecked. Round-18 corrections omit the rev the rule requires (F7) | holds, minor gap |
| 35 | yes. `--numstat` deletions | items 1 and 7 | 2a22ade: SOURCES `9 1`, operator-runbook `11 9`; c699c8c: SOURCES `16 1` | **Fails at its own landing commit 58e5d53**: SOURCES `15 2`, SHONEN `2 3`, no landed erratum (F2) | **falls at read rev** |
| 36 | **partly** | item 8 | Write-verb half only: `corpus/lessons/round-17.md:57` names `read-tree` and `update-ref` | The reflog-prefix clause is mis-specified. The capture clause has no instrument and no committed capture (F3) | **partial; reflog clause wrong** |

Prose-only clauses: no criterion is prose-only end to end. These clauses are:
- 33: "binds each declared command to an argv"; "Deleting one command from a fixture receipt must flip
  the verdict"; "names the commands it did not trace".
- 36: "The lane first captures the reflog, `fsck --full`, ref and index state, and a canary result".
  Its reflog check is also wrong (F3).
- 34: "A paragraph anchor names a quoted sentence or a heading". No check exists.

These clauses have never been red:
- 31: −Infinity and booleans (already rejected at base).
- 32: canary byte-unchanged for P11 (a read-only path cannot change the canary).

## Findings by severity

### F1 — HIGH — criterion 32 is false at 01d586d for an active registered selftest, and its check misses it

Criterion 32 (`corpus/QUALITY.md:217-221`) says: "Every lane subprocess that may run git, including
read-only `git show`, selftest fixtures and fixture scripts, removes every inherited `GIT_*` variable".
- `.ufo/evidence/round-16/measure.py:78-79`: `git()` calls `subprocess.run(['git', '-C', repo] + …)`
  with no env.
- `.ufo/evidence/round-16/measure.py:412`: the selftest builds `env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1',
  GIT_AUTHOR_*…, HOME=tmp)`, so it inherits `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`.
- The tool is live:
  - `tools/registry.json:483` row `measure-round16-rev` (`--rev HEAD --repo .`) and `:508` row
    `measure-round16-selftest` are both `active`.
  - `SKILL.md:1802` and `:1811` tell readers to run it, including `--selftest`.

Sandbox runs at the read rev (scripts `exp/e1*.sh`):
- **E1c** reproduces the round-17 incident shape: only `GIT_DIR` is exported, pointing at a committed
  canary repo. `python3 .ufo/evidence/round-16/measure.py --selftest` produced:
  - **exit 0**, `MEASURE_SELFTEST: 38/38 pass`;
  - canary HEAD moved `f9daf606…` → `c70e0493…`, commits went 1 → 16, and the index was rewritten;
  - canary reflog `HEAD@{0}: commit: drop SHONEN.md`, …
  
  This is the round-17 signature: the selftest passes while it commits fixtures into another repository.
  Control: `.ufo/evidence/round-18/measure.py --selftest` under the same export exits 0
  (98/98) and the canary HEAD does not move.
- **E1/E1b** use the `GIT_DIR`+`GIT_WORK_TREE` pair that the criterion's check names:
  - The same selftest exits 1 with an `AssertionError` (`measure.py:434`). HEAD is unchanged, but the
    canary is not byte-unchanged: `.git/COMMIT_EDITMSG` was rewritten.
  - `measure.py --rev HEAD --repo .` exits 0 in a clean environment. Under the export it exits 2 with
    `{"error": "blob-missing", … "rev": "HEAD"}`, because it read the canary instead of `--repo`.
  - The round-18 `measure.py` control gives identical clean and tainted outputs.

The lane already held committed red signals and did not route them:
- `.ufo/waves/round-18/w1/S11GitEnvSweep.md:89,161` found this tool unscrubbed (`:79`/`:419`).
- `S11GitEnvSweep.md:166,174` predicted that the canary triad would mask it.
- `.ufo/waves/round-18/w1/X09GitEnvCanary.md:28,41` recorded exit 1 for `measure-round16-selftest` under
  the canary, with "clean" and no cause assigned.
- `git grep` over `corpus/`, `SKILL.md` and `.ufo/evidence/round-18/` finds no line that names it as debt.
- Criterion 32 carries only criterion 28's debt (`:174`, `:235`).

Why the check cannot see it:
- The check exports "`GIT_DIR` (and `GIT_WORK_TREE`)" (`:220`). With `GIT_WORK_TREE` set, the fixture
  `add -A` sees the canary's clean tree, so `commit` fails instead of moving HEAD (compare E1 with E1c).
- X09's harness also exports the triad, `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`
  (`.ufo/evidence/round-18/git-env-canary.py:222-229`).
- X09 fingerprints only HEAD, refs, index and objects (`:157`). The "byte-unchanged" wording is stricter
  than the instrument.
- Mitigation that exists: registry rows run under `row_env()`, which drops `GIT_*`
  (`tools/registry-check.py:150`). Only direct invocation is exposed.

Advisory: name the tool as open criterion-32 debt, or supersede both rows by appended rows. Make the
check require the GIT_DIR-only variant.

### F2 — HIGH — criterion 35 is violated by the commit that landed it (58e5d53)

The rule (`:262-266`) says corrections are appended, "The original bytes are never rewritten in place,
and a SOURCES footer update is a literal append: it deletes no line." Running the criterion's own
command, `git diff --numstat 183f87b 58e5d53 -- corpus/SOURCES.md SHONEN.md`, gives:

- **`corpus/SOURCES.md` `15 2`.**
  - `- Next unused id: S065.` was deleted and replaced (`:207-208` at the read rev). Rounds 16 and 17
    did the same: `c699c8c` `16 1`, `2a22ade` `9 1`, where `- Next unused id: S058.` was deleted. §7 item 7
    routed exactly this defect.
  - Row S008 was also rewritten in place (`queued` → `mined`, used-by filled). This has a precedent: the
    S011 row was changed at `9df9212` in round 12. Whether a status transition counts as a "correction"
    is unstated [INFERENCE].
- **`SHONEN.md` `2 3`.**
  - `SHONEN.md:10-11` at 183f87b was deleted in place: the round-16 full-page line plus the landed
    "Correction (round 17, routed R16-C2c)…" paragraph. That paragraph is a landed SHONEN correction,
    which criterion 35 names explicitly.
  - `:13`, the box-4 label, was trimmed.
  - No appended dated erratum exists. `LOG.md` was last changed at `30b0ca8`, and `git grep` over
    `corpus/` finds no round-18 SHONEN erratum.
  - B17 drafted the preservation lines (`.ufo/waves/round-18/w1/B17ShonenCanonical.md:36-45`), but they
    are not landed at the read rev.

Gaps in the check:
- It applies only "for an erratum-only change" (`:276-278`). 58e5d53 mixes rows, footer and erratum, so
  the check does not fire even though the rule is broken.
- "Append-only file" is never enumerated. The same commit corrected a citation in place at
  `SKILL.md:1028-1029` (`SKILL.md` `39 10`); a literal reading of "a citation" covers it.
- A `Next unused id:` counter line cannot be advanced by literal append unless the criterion says how.

### F3 — MEDIUM — criterion 36's reflog check points the wrong way; its capture clause has no instrument

- The check (`:292-294`) says "the saved reflog is a prefix of the current `git reflog` output". But
  `git reflog` prints newest first, with shifting `HEAD@{n}` selectors.
- **E3** saved the reflog of a 2-commit repo, then made one ordinary commit:
  - default format: prefix **no**, suffix **no**;
  - `--date=iso`: prefix **no**, suffix **yes**;
  - raw `.git/logs/HEAD`: byte-prefix **yes**.
  
  The clause therefore fails after any legitimate later commit; a jj lane adds an "export from jj" entry
  on every landing. It passes only when nothing happened since the capture.
- No committed capture exists: `git ls-tree -r --name-only 01d586d | grep -ciE 'reflog|fsck|incident'`
  returns 0. Round 17 saved none, so this half has never been shown to fail on a committed artifact.
- The write-verb half does have a red-before: `corpus/lessons/round-17.md:57` names
  `git read-tree 98bea7d` and `update-ref --no-deref HEAD 98bea7d`; spot-check `:72-74`.
- Advisory replacement: "the saved `.git/logs/HEAD` is a byte prefix of the current file". An
  alternative is "the saved `git reflog --date=iso` lines are a suffix of the current output".

### F4 — MEDIUM — criterion 33's binding check is prose-only

- No lane tool compares declared commands with receipt argv:
  - `.ufo/evidence/round-18/measure.py` has `argv` only in a selftest fixture (`:789`).
  - `coldread/assemble.py` checks only "commands ⇒ traces non-empty" (`:596-600`).
  - Neither reads `coldread/bucket-commands.json` (grep: no hits).
- No fixture exists for "Deleting one command from a fixture receipt must flip the verdict", and no
  committed red-before exists for the binding.
- The v2 report schema has no slot to "name the commands it did not trace" (`assemble.py:13-19`).
- The narrowing half does have committed reds:
  - `corpus/lessons/round-17.md:98-104`: the G5 "closed" overclaim, the G7 pointer and the 89-vs-94 tally;
  - `corpus/knowledge/input-keyed-coldread-credit.md:128-131`;
  - the round-18 SKILL registry row ("never cite it as command coverage").
- Not implementing the binding was deliberate (`.ufo/waves/round-18/w1/S20OperatorTeachings.md:66`).
  The criterion should say the binding clause is unimplemented and give its owner.

### F5 — LOW — criterion 30's "never bare HEAD" contradicts the landed fix

- In the tip `tools/evidence-disposition.py`, `resolve_historical_anchor` (`:460-525`) returns
  `("HEAD", commit)` (`:498`, `:525`). It does this for an unbound detached non-jj harness when any local
  or remote-tracking ref contains HEAD.
- The tool documents this (`:51-53`), and so does the round-18 SKILL registry row.
- Criterion 30 (`:190-191`) states no exception, so a literal application flags the tip.
- The red-before is sound: P08 is `open` with findings=[] at base and `closed` at the tip.
- Captured-by anchors were verified at 183f87b:
  - `:45-48` and `:179-180`: G2/G3 stated against HEAD;
  - `:441`: `def resolve_historical_rev`;
  - `:450`: `merge-base --is-ancestor … rev, "HEAD"`.

### F6 — LOW — criterion 31: two clauses were never red, and the check is narrower than the rule

**E2b** ran the base and tip `registry-check.py` bytes on `timeout_s` literals. At 183f87b:

| Literal | Exit | Outcome |
|---|---|---|
| NaN | 1 | ValueError traceback |
| Infinity | 1 | OverflowError traceback |
| −Infinity | 2 | rejected (`ts <= 0`) |
| true | 2 | rejected (`isinstance(ts, bool)`, `:223`) |
| 1e999 | **1** | OverflowError traceback |
| 0 | 2 | rejected |

At 01d586d all six exit 2 and name both the row and the field. The tip selftest carries all five cases
(`tools/registry-check.py:1490-1513`).

- **No red-before for −Infinity or booleans:** both were already rejected at base.
- **Overflow:** `1e999` was a real base defect. The criterion's check names only the NaN and Infinity
  literals (`:212-213`), so a parse-time literal filter would pass the check while violating "finite".
- Captured-by anchors verified at 183f87b: `:221-227`, `:273`, `:281`, `:306`, `:386`.
- P10 red-before: survivors=[5] for both setsid and setpgid.
- §7 item 6's carry-forward of the r16 debts has no criterion text.

### F7 — LOW — criterion 34: an undefined scope term, an unchecked clause, and self-application

- Captured-by verified:
  - At fleet `5d8a3b5`, `scripts/hyaku/jj-lane.sh` has `detect_branch()` at `:115` and `usage()` at
    `:50`; `:53-65` is usage text. Fleet HEAD `a7c4efb` still has it at `:115`.
  - At 183f87b, `:53-65` is cited at `SKILL.md:1029` and in five ER-jj/R3 notes:
    `fleet-kill-rate-ledger.md:420`, `incremental-pin-disposition.md:386`, `operator-runbook.md:514`,
    `service-limits.md:279` and `verification-patterns-fleet.md:309`.
  - Committed red: ER-jj2 is appended to all five notes (`2 0` each).
- The rule requires "function or symbol name **and the cited rev**" (`:251-252`). ER-jj2 ×5 and the
  `SKILL.md:1028-1029` replacement give the name but no fleet rev.
- Criteria 31 and 32 themselves use rev-pinned bare ranges with no symbol, for example 32's `:337-342`;
  the enclosing function `materialize_target` is defined at `:332`.
- "A file that moves" is undefined, and the paragraph-anchor sentence (`:254`) has no check.

### F8 — LOW — residuals in criteria 29 and 32

- **29:** `trace-inputs-round17-selftest` (`tools/registry.json:656`) is still active, and its bytes are
  unchanged. The three trace removals therefore still survive that copy's selftest (base receipt
  P05–P07); the closure covers only `tools/trace-inputs.py`. The criterion's "at the cited rev"
  (`:186-187`) cites no rev.
- **32:** for P11 the canary half never discriminated: canary_changed=False at both base and tip. Only
  the "reads its intended repository" half did (declared False → True).

### F9 — INFO — mapping and wording

- All eight §7 items map to criteria: 1→35, 2→33, 3→29, 4→32, 5→30, 6→31, 7→34 and 35, 8→36.
- §7 item 2's G7 and G5-tally corrections exist only as errata (`round-17.md:103-104`). No criterion
  cites item 2 for correction mechanics.
- `QUALITY.md:174` says "criterion 28's open debt is not closed here". After the bash-witness migration
  landed (P11 closed; `dispositions.json`), this reads stale.
- The SHONEN box-3 link `.ufo/evidence/round-18/coldread/ledger.json` does not exist at 01d586d (the
  directory holds only `assemble.py`). B17 says it is written by this wave (`B17ShonenCanonical.md:3`).

## Verified, no finding

- Criteria 1–28 are byte-identical. `diff <(git show 183f87b:corpus/QUALITY.md) <(head -n 167 corpus/QUALITY.md)`
  exits 0, and `QUALITY.md` numstat is `128 0`. The staged and landed files are identical
  (sha256 `ffed5023df9d4d9b…`).
- Criterion 29's Captured-by reports name exactly the seven survivors: `MutateDispositionV2.md:54,58`,
  `MutateRegistryCheck.md:52-53`, `MutateTraceInputs.md:52,54,55`.
- The base receipt came before the fix: `git merge-base --is-ancestor aee4f36 58e5d53` exits 0. Counts:
  v1 and v2 base open=11/11, v2 tip open=0/11. The v1 tip receipt errored on P01, P02 and P08, which is a
  ruler defect and is retained.
- Criterion 32 pin integrity:
  - `.ufo/evidence/round-13/expected.json:11` = `49e9e5e2…350ad80`, which equals
    `git show 4acc607:tools/bash-witness-study.py | sha256sum`.
  - Nothing under `.ufo/evidence/round-13/` or `round-17/` changed from 183f87b to 01d586d.
  - The superseded registry rows are retained.
  - The landed tool sha `8dfaa25a…` equals X07's staged copy; X07's mutant gave 41/43, exit 1 (`X07:26`).
  - Captured-by verified: `GIT_` substrings only in `TARGET_GIT_PATH` (lines 97, 339, 342, 359 and 887),
    and `git show` at `:337-342` with no env.

## Commands (all from the /tmp clone unless marked; exit codes)

- Clone and detach at the read rev with `env -u GIT_*` → 0. `git rev-parse HEAD` → `01d586dd…`.
- `git diff --numstat 183f87b 01d586d -- corpus/QUALITY.md corpus/SOURCES.md SHONEN.md SKILL.md corpus/knowledge/ corpus/lessons/`
  → 0. Results: QUALITY `128 0`, SOURCES `15 2`, SHONEN `2 3`, SKILL `39 10`, knowledge ER appends `2 0`.
- `git show --numstat 58e5d53|2a22ade|c699c8c -- corpus/SOURCES.md` → 0, giving `15 2`, `9 1` and `16 1`.
  `git show --numstat 2a22ade -- corpus/knowledge/operator-runbook.md` → 0, giving `11 9`.
- `git show 183f87b:tools/{evidence-disposition,registry-check,bash-witness-study}.py | sed -n …/grep -n …`
  → 0 (anchors above).
- `git show 183f87b:.ufo/evidence/round-13/expected.json | sed -n 11p` → 0.
  `git show 4acc607:tools/bash-witness-study.py | sha256sum` → 0.
- Fleet (read-only): `git -C /home/vgpnk/Projects/shokunin show 5d8a3b5:scripts/hyaku/jj-lane.sh | grep -n …`
  and `sed -n 53,65p` → 0. `git … show HEAD:scripts/hyaku/jj-lane.sh | grep -n 'detect_branch()'` → 0 (`:115`).
- `git grep -n "jj-lane.sh:53-65" 183f87b -- .` → 0, 17 hits including the 6 cited.
- `git ls-tree -r --name-only 01d586d | grep -ciE 'reflog|fsck|incident'` → 0 matches.
- The experiments ran as `bwrap … env -i PATH HOME=$W/home TMPDIR=$W/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C bash $W/exp/<script>`.
  Every bwrap call exited 0, and the inner exits are as reported:
  - `e1-r16measure.sh`: E1, inner exits 0, 1, 0, 2, 0, 0;
  - `e1b-canary-files.sh`: E1b, inner exit 1, `COMMIT_EDITMSG` changed;
  - `e1c-gitdir-only.sh`: E1c, inner exits 0 and 0, HEAD moved / not moved;
  - `e2b-timeouts-base.sh`: E2b, table in F6;
  - `e3-reflog.sh`: E3.
- My first E2 run used uppercase row names (`row-NaN`), which the base name regex rejected, so its base
  rows were confounded. I discarded it and replaced it with E2b, which uses lowercase names.

## Residual risk and verification gaps

- I did not re-run `defect-probes.py`; I relied on its committed receipts. E2b independently reproduced
  P09 at base and at tip.
- I did not open the other w2 reports, `LOG.md` prose beyond the grep, or `SCORECARD.md`.
- F1's hazard needs a caller-exported `GIT_DIR`. The wave contract forbids that, and the registry monitor
  path scrubs it, so the exposure is to direct runs such as SKILL readers and fixtures [INFERENCE].
- [INFERENCE] I treat SHONEN.md and the SOURCES footer as inside criterion 35's scope because the
  criterion names them. I treat SKILL.md as ambiguous.

Verdict: **partial**. All eight criteria map to §7, and committed red-befores show 29–32, 34 and 35 can
fail. Three clauses are prose-only or mis-specified: 33's argv binding, 36's capture procedure and reflog
check, and 34's paragraph-anchor clause. Criteria 32 and 35 are false at `01d586dd` against the lane's
own active tool and its own landing commit.
