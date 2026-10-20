source: S065 — https://docs.python.org/3/library/json.html §Standard Compliance and Interoperability › Infinite and NaN Number Values; json.load() `parse_constant`; S066 — RFC 8259 §6 Numbers, https://www.rfc-editor.org/rfc/rfc8259; S068 — PR_SET_CHILD_SUBREAPER(2const) §DESCRIPTION, https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html (mined, opened 2026-10-20); S069 — setsid(2) §DESCRIPTION ¶2 and §ERRORS EPERM, https://man7.org/linux/man-pages/man2/setsid.2.html; S070 — Pro Git §10.8 Repository Locations, https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables (tier B); S072 — open(2) §DESCRIPTION, O_TRUNC, https://man7.org/linux/man-pages/man2/open.2.html; S073 — CPython 3.15 command line §1.2 PYTHONPYCACHEPREFIX and PYTHONDONTWRITEBYTECODE, https://docs.python.org/3/using/cmdline.html; S074 — git-symbolic-ref §OPTIONS -q, §NOTES, https://git-scm.com/docs/git-symbolic-ref; S063 — git(1) ENVIRONMENT VARIABLES, GIT_CONFIG_GLOBAL and GIT_CONFIG_NOSYSTEM entries, https://git-scm.com/docs/git (reopened 2026-10-20; the S063 row's anchor cell names only "The Git Repository" and must be widened to these entries); S061 — jj Git compatibility, colocated HEAD (landed row); own work — round-18 wave-1 reports and lane files at 183f87b, cited inline.
verified-at: 2026-10-20 at lane base 183f87b899e6cae46be98d251cbc87fb5118f6ca. Landed-tip results: PENDING (filled by L1 after landing).
recheck: `python3 .ufo/evidence/round-18/defect-probes.py --rev <branch tip>` (contract A; base receipt `.ufo/evidence/round-18/c2-probes-183f87b.txt`, `DEFECT_PROBES: open=11 closed=0 total=11`). Re-open S065–S074 and S063 and confirm each quoted sentence is still present at its URL; a missing quote is drift.
ground: none — method note for the round-18 C2 ruler; no frontier row moves.

# Guard-kill closure — how a guard earns "covered"

Scope: the method behind round-18 C2 (routed items R17-GUARD-COVERAGE, R17-JJ-GUARDS, R17-TIMEOUT, R17-GIT-ENV, R17-CMD-BIND for the trace collector). It states what a probe may claim, the fixture recipe for each defect class, and what remains unmeasured.

Citation form. `[w1/X]` is `.ufo/waves/round-18/w1/X.md`. `[lane:P:L]` is `P` at line `L` of `tools/…` or `corpus/…` at 183f87b (read with `git show 183f87b…:P`). `[src: Sxxx]` is the source row above. `[receipt:P##]` is the probe line in `.ufo/evidence/round-18/c2-probes-183f87b.txt`. Lines marked PENDING are not yet at the landed tip.

Id note. Ids follow the L1 map. Rejected rows are not cited: S067 (prctl(2)) and S071 (jj working copy). S061 is the landed jj row.

## 1. A guard is covered only when two legs hold

Rule. A guard G is covered by its owning `--selftest` only when both hold at the same rev:

- (a) pristine green: the unmodified selftest exits 0. A nonzero pristine exit is could-not-evaluate (exit 2), never "closed".
- (b) kill: the selftest exits nonzero when G's single-occurrence guard text is removed (the mutant applied to a copy).

Why (a). Without it, a broken selftest makes every mutant read as killed. K04 found that contract A never required a green pristine run, so an always-failing collector would read all three probes as closed [w1/K04TracePromotion.md:65-71]. X03 implements the fix: each guard-removal probe runs its owning pristine selftest first, and nonzero is an evaluation error [w1/X03DefectProbes.md:29].

Why not existence. A mutant that survives is not behavioural coverage. K01 states that a guard-removal probe measures mutant sensitivity, not that the guard works [w1/K01ProbeRulerGaming.md:14-20]. The round-17 lesson says the same: code existence is not behavioural coverage [lesson §7 item 3, `corpus/lessons/round-17-verifier-spotcheck.md:428-432`].

Meta-cheat. A selftest case that hashes or greps its own source kills every P01–P07 mutant with no behavioural coverage [w1/K01ProbeRulerGaming.md:83-89]. A kill that comes from an unrelated case tripped by a side effect of the mutant is incidental [w1/K01ProbeRulerGaming.md:91-96]. Detection: the probe prints the failing case names, and a case that reads the tool's own bytes does not count.

Base result at 183f87b. The ruler reports `DEFECT_PROBES: open=11 closed=0 total=11` [receipt; w1/X03DefectProbes.md:13]. For P01–P07 the pristine and mutant selftests both exit 0 (for example P01 0→0, P05 27/27 both) [w1/X03DefectProbes.md:33-39].

Bound. "Closed" certifies only that the named round-17 mutant now kills the selftest. It does not certify the guard in production [w1/K01ProbeRulerGaming.md:30-32]. P10 and P11 are behavioural probes, not guard removals, so their closed condition differs [w1/X03DefectProbes.md:47-48].

## 2. jj colocation: HEAD is `@-` and can differ from the branch tip

Fact. In a colocated repository, Git HEAD is the working-copy parent `@-`. It is not the branch tip when a commit is made without moving the bookmark [src: S061 row, `corpus/SOURCES.md:70`; w1/C02MoriJjPatterns.md:35-43]. Measured on jj 0.45.1 and git 2.56.0 in /tmp [w1/C02MoriJjPatterns.md:31].

- `jj git init --colocate` alone leaves HEAD attached at the branch tip, so it does not create the divergence [w1/C03FleetJjPractice.md:40, :47].
- `jj new` moves HEAD to the previous working-copy commit. Commit ids diverge but trees do not, so a byte check cannot see it [w1/C03FleetJjPractice.md:41, :48].
- `jj commit` of a content change, before `bookmark set`, moves HEAD to the new `@-`. The live bytes match `HEAD:` and differ from `refs/heads/<branch>:` [w1/C03FleetJjPractice.md:49].
- After `bookmark set`, HEAD equals the branch tip and stays detached [w1/C03FleetJjPractice.md:43, :50].

Fixture recipe (P08). Build it in /tmp only, with the git environment unset for the setup and probe [w1/C02MoriJjPatterns.md:18; w1/R05ReproJj.md:9].

1. `git init -b master`, one commit, then `jj git init --colocate`.
2. Change a tracked file and `jj commit -- <path>`. Do not run `bookmark set`.
3. Before the tool runs, assert: `git symbolic-ref HEAD` returns rc 1 (detached); `refs/heads/master` is the unique branch; git HEAD equals `jj log -r @-`; git HEAD differs from `@`; and the blobs differ between HEAD and the branch [w1/C02MoriJjPatterns.md:73; w1/C03FleetJjPractice.md:102].
4. Commit-id inequality is not enough. G2 and G3 split only at tree level, so the fixture must make the byte relations diverge [w1/C02MoriJjPatterns.md:57-62, :77]. A fixture that stops at colocate, or bookmarks before the assert, has HEAD equal to the tip and HEAD-based code passes [w1/C03FleetJjPractice.md:106].

S074 bears on step 3. `git symbolic-ref HEAD` names the branch only when HEAD is attached. With `-q`, a detached HEAD exits 1 silently and any other error exits 128. A resolver must branch on exit 1 as "detached", not as a read failure [src: S074, quotes A–C].

Resolution order (the fleet's v2 `state`, read-only). The order is: `lane.branch`; then `detect_branch()`, which takes an attached `refs/heads/*` or else `refs/remotes/origin/HEAD`; then the unique one of `master` and `main`; then a 40-hex `refs/heads/<branch>`. Otherwise it is an error. Never HEAD [w1/C03FleetJjPractice.md:17-27, :70, :102]. The v1 ladder (`--short` then `origin/HEAD` then master, main, first branch) and the HEAD fallback in `tools/pin-disposition.py` are not to be copied into G2/G3 [w1/C03FleetJjPractice.md:76, :94; w1/C02MoriJjPatterns.md:55].

Base state. P08 is open. At 183f87b G2 reads HEAD (`tree_entry(lane, "HEAD", path)`) at `[lane:tools/evidence-disposition.py:518]`, and G3 runs `merge-base --is-ancestor … HEAD` at `[lane:tools/evidence-disposition.py:450]`, inside `resolve_historical_rev` at `:441`. The probe receipt shows both following HEAD [receipt:P08; w1/X03DefectProbes.md:45]. R05 reproduced this at the dispatch rev: G3 accepts a rev that is not an ancestor of `refs/heads/master`, and G2 accepts bytes present only on the HEAD history [w1/R05ReproJj.md:44].

PENDING. Retargeting G2/G3 to `refs/heads/<branch>` (contract D) is not at 183f87b. The landed-tip result is PENDING.

## 3. Non-finite JSON numbers

Fact. `json.loads` accepts `NaN`, `Infinity` and `-Infinity` by default, as if they were valid JSON numbers [src: S065, quote "by default, this module accepts and outputs `Infinity`, `-Infinity`, and `NaN`…"]. The `parse_constant` hook receives each such literal and can raise [src: S065, json.load() `parse_constant`]. RFC 8259 §6 states that numeric values not representable in the grammar, such as Infinity and NaN, are not permitted [src: S066, quote]. That sentence has no RFC 2119 keyword. Rejecting a non-finite `timeout_s` with exit 2 is a design choice, not a quoted requirement [src: S066, Gate note].

Base code. The registry parses with plain `json.loads` at `[lane:tools/registry-check.py:281]`, with no `parse_constant` [w1/S09NonFiniteSweep.md:33]. The positive check at `[lane:tools/registry-check.py:221-227]` is `ts <= 0`, so NaN passes (NaN compares false) and +Infinity passes [w1/S09NonFiniteSweep.md:35-37; w1/K01ProbeRulerGaming.md:66-70].

Observed at base (clone). `NaN` exit 1 with an uncaught `ValueError`. `Infinity` exit 1 with `OverflowError`. `1e400` exit 1 with `OverflowError`, with no literal needed. `-Infinity` exit 2 "must be a positive number" [w1/S09NonFiniteSweep.md:42-48]. P09 open: NaN and Infinity each reach execution [receipt:P09; w1/X03DefectProbes.md:46].

Two sub-defects. `parse_constant` alone rejects only the literals. `1e999` parses to `inf` under both settings, so an `isfinite` check is also needed [w1/K01ProbeRulerGaming.md:106-110]. The exit-2 error must name `timeout_s`, or P09 stays open [w1/K01ProbeRulerGaming.md:112-113].

PENDING. The staged `tools/registry-check.py` uses `parse_constant=_reject_json_constant` and `math.isfinite`, and removing either fails a named case [w1/X05RegistryCheck.md:5, :33-34]. That staged result is not at the landed tip.

Routed, not C2. `tools/mutate-and-run.sh` aborts with exit 1 on a non-integer `--timeout` or `--tail` ("unbound variable"), which collides with the DEGRADED exit [w1/S09NonFiniteSweep.md:65-79].

## 4. Process escape: setsid and setpgid leave the group

Fact. `setsid()` makes the caller the only process in a new process group and a new session [src: S069, quote "The calling process will be the only process in the new process group and in the new session."]. A group-directed signal to the old group therefore does not reach it. That consequence is inference from the new group ID; `killpg` is not named on the man page [src: S069, Gate note]. `setsid` fails with EPERM for a process group leader, so an escaping process must fork first [src: S069, §ERRORS].

Subreaper rule. An orphaned process is reparented to the nearest living ancestor subreaper. Quote: "When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper." [src: S068, PR_SET_CHILD_SUBREAPER(2const) §DESCRIPTION]. This is the rule the cleanup walk relies on: an escapee that double-forks stays a descendant of the checker while the checker is the nearest subreaper.

Base code. `_kill_group` signals only `os.getpgid(proc.pid)` with `os.killpg` at `[lane:tools/registry-check.py:306-322]`. The row starts with `start_new_session=True` at `[lane:tools/registry-check.py:375]`. After timeout the code calls `proc.communicate()` with no timeout at `[lane:tools/registry-check.py:387]` [w1/S10TimeoutEscapeSweep.md:42-43].

Observed. `setsid` escapes a group kill (`survivors=[5]`), and so does a plain `os.setpgid(0,0)` [receipt:P10; w1/X03DefectProbes.md:47]. Both checkers returned `got=timeout`. A `setsid` escapee holding the row's pipe held the monitor for 6037 ms with `timeout_s: 1` [w1/S10TimeoutEscapeSweep.md:18-20]. A row that exits before its timeout can leave a daemonised child alive while the row reports held [w1/S10TimeoutEscapeSweep.md:14-16].

PID reuse. `proc.pid` is a bare number after the leader exits. If it is reused before `os.getpgid` runs, `killpg` can signal an unrelated group [w1/N02KillScopeSafety.md:21].

Required design, from the reviews.

- Set `PR_SET_CHILD_SUBREAPER` before each row. Failure is "unavailable", not a fallback to group-only cleanup [w1/N02KillScopeSafety.md:27; w1/X05RegistryCheck.md:7, :43]. The reparenting rule is S068 above.
- Walk `/proc` ancestry by process leaders. Parse `stat` after the last `)`. Keep identities `(pid, starttime)`, not UID, session or group [w1/N02KillScopeSafety.md:28].
- Revalidate starttime after `pidfd_open`, then signal through the pidfd. Never a later numeric `kill` [w1/N02KillScopeSafety.md:29; w1/X05RegistryCheck.md:7].
- Drain bounded: bound `communicate` and the final wait. Completion is "no visible row descendant", not "pipe closed" [w1/X05RegistryCheck.md:7; w1/V02TimeoutIntent.md:33].
- A cgroup with `cgroup.kill` is the stronger guarantee against PID reuse and parentage escape. If it is unavailable, state the weaker guarantee [w1/N02KillScopeSafety.md:32].

Residual limits. A descendant that changes UID is not signalable by an unprivileged monitor (EPERM) [w1/V02TimeoutIntent.md:31]. A same-tick PID reuse can race before the pidfd opens, because starttime has tick granularity [w1/X05RegistryCheck.md:43]. A double-forked descendant cannot leave an active subreaper's tree [w1/X05RegistryCheck.md:43].

PENDING. The base is process-group-only cleanup. The subreaper and walk exist only in the staged X05 source, and its falsifier table is staged evidence, not landed evidence.

## 5. Git environment: prefix-filter, then pin the config

Prefix filter. Remove every inherited name that starts with `GIT_`, not a fixed list [w1/C04GitEnvPriorArt.md:44-48]. The base holes: `tools/bash-witness-study.py` runs `git show` at `[lane:tools/bash-witness-study.py:337-340]` with no `env`, and `sweep_env()` pops only five non-git names at `[lane:tools/bash-witness-study.py:116-117]` [w1/S11GitEnvSweep.md:45-46; w1/C04GitEnvPriorArt.md:60-63]. Repository location variables are defined in [src: S070, quote "GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree"] and in the git(1) ENVIRONMENT VARIABLES list [src: S063]. S070 is Pro Git, tier B; the normative source is S063.

Config pins. The staged X07 build sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` after the filter, and disables hooks in fixture repositories [w1/X07BashWitnessScrub.md:12, :22]. These are PENDING at the landed tip.

Source for the two config variables. git(1) documents `GIT_CONFIG_GLOBAL`: "Take the configuration from the given files instead from global or system-level configuration files … Likewise, if GIT_CONFIG_GLOBAL is set, neither $HOME/.gitconfig nor $XDG_CONFIG_HOME/git/config will be read. Can be set to /dev/null to skip reading configuration files of the respective level." `GIT_CONFIG_NOSYSTEM`: "Whether to skip reading settings from the system-wide $(prefix)/etc/gitconfig file." [src: S063, reopened 2026-10-20 at https://git-scm.com/docs/git]. The S063 row's anchor cell names only "The Git Repository", so the L1 widens it to these ENVIRONMENT VARIABLES entries. Hooks-off is not in git(1); it stays UNSOURCED. The fixture's hook-disable is a choice of the fixture, not a documented guarantee.

The trio is not enough. Unsetting `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` leaves `GIT_OBJECT_DIRECTORY` in place. `rev-parse HEAD` then looks clean while `cat-file` still reads the decoy object store [w1/C04GitEnvPriorArt.md:79-82, :87]. A canary that watches only the decoy HEAD is a false green. A prefix filter closes this arm [w1/C04GitEnvPriorArt.md:83]. The canary passes only when the intended blob is returned [w1/C04GitEnvPriorArt.md:89].

Do not adopt. `{**clean_env(), **identity}` can put `GIT_*` back [w1/C04GitEnvPriorArt.md:65]. `LC_ALL=C` changes git's stderr [w1/C04GitEnvPriorArt.md:65]. An `env -i` harness hides a missing inner scrub [w1/C04GitEnvPriorArt.md:96].

Migration of pinned tools. `tools/bash-witness-study.py` is pinned at `49e9e5e2…350ad80` in `.ufo/evidence/round-13/expected.json:11`. The historical bytes at `4acc607` match that pin [w1/X07BashWitnessScrub.md:21]. The bytes are not edited. The change is an appended v2 manifest with a historical waiver [w1/K05MigrationIntegrity.md:67-75].

Manifest rules found by attack:

- `supersedes` must name the v1 document (round-14). Naming the round-17 v2 manifest exits 2 with `supersedes_mismatch`, because G7 requires schema v1 [w1/K05MigrationIntegrity.md:10-25, :33-35]. The L1 ruling keeps round-14 [w1/X07BashWitnessScrub.md:14].
- A waiver breaks the round-17 rows that do not waive the tool. The `round17-before` row expects an input digest and exits 2 after the edit commits [w1/K05MigrationIntegrity.md:43-65]. The row must be superseded or replaced.
- The tool edit and the manifest must land in one commit, or the manifest last. A gate run between them exits 2 [w1/K05MigrationIntegrity.md:91-95].
- A waiver accepts later committed edits. The manifest should pin the new digest as a live input to keep drift detection [w1/K05MigrationIntegrity.md:77-87].

Staged result. X07 reports the round-18 manifest exits 0 (`clean`, 11 effective, 1 superseded) and the round-17 `dispositions-before.json` exits 2. The round-18 `dispositions-before.json` exits 1 with `expected_contains_missing` [w1/X07BashWitnessScrub.md:27-30]. The last item is an open defect in the staged work. PENDING at the landed tip.

## 6. Trace-collector guards

O_RDWR is write-capable. A write-mode open with O_TRUNC truncates at open time whenever the access mode allows writing, and O_RDWR and O_WRONLY both do [src: S072, quote "the access mode allows writing (i.e., is O_RDWR or O_WRONLY) it will be truncated to length 0."]. An O_RDWR open is therefore not a pure read input. The collector's write-flag regex includes `RDWR`. Deleting `RDWR|` from it survives the base selftest at the frozen path `.ufo/evidence/round-17/coldread/trace-inputs.py:82` [receipt:P05; w1/X03DefectProbes.md:37]. The promoted `tools/trace-inputs.py` has the exclusion at `:818-820` in the staged X04 build [w1/X04TraceInputs.md:13, :20]. PENDING: `tools/trace-inputs.py` is untracked at 183f87b.

Private pycache prefix. `PYTHONPYCACHEPREFIX` writes `.pyc` files in a mirror tree at that path instead of `__pycache__`. A non-empty `PYTHONDONTWRITEBYTECODE` stops `.pyc` writes on import [src: S073, quotes]. The round-17 collector sets the prefix at `.ufo/evidence/round-17/coldread/trace-inputs.py:516`. Replacing it with `"."` survives the base selftest [receipt:P06; w1/X03DefectProbes.md:38]. The round-17 mutant report records the receipt advertising the private path while the real prefix was `.` [`.ufo/waves/round-17/w2/MutateTraceInputs.md`, M03]. The staged X04 selftest checks the child's prefix against the receipt and the private path at `:925-930` [w1/X04TraceInputs.md:13]. PENDING.

Root execve. The receipt requires a successful root execve. Removing `first_pid not in exec_ok` survives at the frozen path `:644` [receipt:P07; w1/X03DefectProbes.md:39]. The staged X04 selftest kills it with a synthetic trace that has a successful `openat` and no successful exec [w1/X04TraceInputs.md:13, :22]. PENDING.

Scope of the collector's own reads. A traced collector's own open is not recorded when it is the traced root, so editing the collector invalidates existing entries only if seats traced opens of the file [w1/K04TracePromotion.md:41-44]. The frozen copy's sha must not change in place. Its identity is a separate integrity check that the probes do not run [w1/K04TracePromotion.md:73-83].

## 7. Limits — what this does NOT prove

- The ruler proves a mutant kills a selftest. It does not prove production behaviour [§1; w1/K01ProbeRulerGaming.md:30-32].
- The probes run in the bwrap envelope in `defect-probes.py:4-14`, with `env -i`, a private /tmp, and isolated PID and network namespaces. P10 is observed inside that PID namespace [w1/X03DefectProbes.md:8]. The envelope is a sandbox for the probes, not a proof of containment for the tools under test.
- P11's open verdict rests on the tainted run exiting 2 with CANNOT-EVALUATE under an exported `GIT_DIR`. That shows the subprocess honours the variable [receipt:P11; w1/X03DefectProbes.md:48]. It does not measure a scrubbed fix.
- Canary breadth. X09 ran 14 registered selftests at base. The result is partial: the bash-witness selftest did not touch the canary, and `measure-round16-selftest` exited 1 with a clean canary [w1/X09GitEnvCanary.md:28, :40-43]. A clean canary on a selftest is not proof of a scrub at every subprocess site. S11 lists sites with no `env` argument, such as `tools/repeat-control.py:281`, which has no git call and so no canary [w1/S11GitEnvSweep.md:63-65].
- Tools not at the landed tip: `tools/trace-inputs.py` (untracked), staged `tools/registry-check.py` (X05), staged `tools/bash-witness-study.py` and manifests (X07). Every landed-tip number is PENDING.
- Unsourced: hooks-off has no row and no git(1) entry; it stays UNSOURCED. `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM` are sourced to git(1) S063 once its anchor is widened (§5). The subreaper page is row S068 once B13 installs it.
- Not run: no after-landing probe run, no `registry-check --json` held count at the landed tip, no canary run after the scrub lands.

After-measurement (PENDING, filled by L1). `defect-probes.py --rev <branch tip>` open/closed count: PENDING. `tools/registry-check.py --rev <branch tip> --json` held count: PENDING. Staged-to-landed diff for each §4–§6 item: PENDING.

## Errata — round 18 wave 2 (2026-10-20, append-only)

Appended after the non-author wave-2 reads at `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`
(`.ufo/waves/round-18/w2/ReviewGuardKillEntry.md`); the lines above stay as written.

- **EG-1 measured, no longer PENDING.** Ruler v2 (`.ufo/evidence/round-18/defect-probes.py`):
  base `183f87b` open=11/11 (`c2-probes-v2-183f87b.txt`), tip `e08271a` and
  `01d586d` open=0/11 (`c2-probes-v2-e08271a.txt`; w2 RerunC2After, RerunC2Before).
  Registry at `e08271a` and `01d586d`: 32/32 held, 3 superseded (w2 RegistryNoHarm).
  The v1 tip run errored on two ruler defects and is retained (`c2-probes-e08271a.txt`).
- **EG-2 §2 anchor rule as landed.** "Never HEAD" holds for a bound lane
  (`lane.branch` set, or HEAD attached). An unbound jj workspace with detached
  HEAD is refused (exit 2); an unbound detached non-jj clone (what
  `registry-check --rev` makes) anchors on its checked-out commit only when a
  local branch or remote-tracking ref contains it. A P08-style fixture must bind
  `lane.branch` as the jj-lane helper's `init` does; ruler v2 does.
- **EG-3 what "closed" certifies (bounded).** P08 binds `master`, so a fix that
  hardcodes `master` instead of reading `lane.branch` also closes it (63/63
  selftest); P11 exports only `GIT_DIR`/`GIT_WORK_TREE`, so a three-name unset
  instead of the prefix filter also closes it (43/43). P09 exercises the two
  literals; a finite `timeout_s` ≥ 2147484 crashed the round-18 build with exit
  1 and is capped at 86400 after wave 2. These are named survivor classes for
  round 19, together with the wave-2 mutation survivors
  (`.ufo/waves/round-18/w2/Mutate{RegistryCheck,Disposition,TraceInputs,BashWitness}18.md`:
  3 + 3 + 2 + 10).
- **EG-4 sources.** S072's teaches overstated O_TRUNC; S078 supersedes it.
  S068's anchor is §DESCRIPTION ¶2; S077 supersedes it. Both new rows are
  round-18 corrections (`corpus/SOURCES.md`); this entry's claims rest on the
  O_RDWR access-mode sentence and the unchanged reparenting quote. The probe
  prints failing case names for P01–P04 only; for P05–P07 it prints the tally.
  The round-18 `dispositions-before.json` exit 1 is the registered negative
  control (`producer_before`), not a defect.
