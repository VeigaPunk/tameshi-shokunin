# RerunC2After: C2 after-count re-run at the read rev

Seat: `TameshiR18.RerunC2After` (reviewer, leaf). Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`, which is lane `HEAD` = `master` = `origin/master` (`git --no-optional-locks log`, exit 0).
Scratch: `/tmp/tameshi-r18w2-RerunC2After-EpOq8v` (clone, extracts, driver). Installs or updates: none.

## Result

The C2 after-count reproduces at the read rev: `DEFECT_PROBES: open=0 closed=11 total=11` with exit 0. I got this in two independent runs, one in text mode and one in `--json` mode. Each guard probe P01–P07 reports `pristine_exit=0 mutant_exit=1` in both runs.

### Ruler identity
- The working-copy ruler `.ufo/evidence/round-18/defect-probes.py` has sha256 `99297d9645151dee948291638386f3e9189c7bab590bebda23de6e51dadebeaa`. `git show 01d586dd:.ufo/evidence/round-18/defect-probes.py | sha256sum` gives the same value, so I ran the ruler exactly as committed at the read rev.
- `git diff --stat e08271a 01d586dd -- tools/ .ufo/evidence/round-17/` is empty. The L1's tip receipt `c2-probes-v2-e08271a.txt` and this run therefore measured byte-identical tools. The L1's committed receipts are named for `e08271a`; this run resolved `--rev` to `01d586dd` itself.
- `defect-probes.py --selftest`, run in the same envelope, exits 0 with `SELFTEST: PASS (6 cases)`.

### Envelope (GIT_* unset, cwd outside the lane)
My shell inherited `GIT_EDITOR`, `GIT_PAGER` and `GIT_TERMINAL_PROMPT`. I dropped all of them with `env -i`; inside the envelope `env | grep -c ^GIT_` printed 0.

I ran the ruler unchanged inside an outer read-only bwrap. The bwrap maps `/tmp` to my scratch, so the ruler's own `mkdtemp(dir="/tmp")` workspace stays under my prefix. The ruler's per-child inner envelope (`defect-probes.py:4-14`, `:183-206`) is untouched. Inside the outer envelope `[ -w <lane> ]` reported `outer-lane-not-writable`. Afterwards `find /tmp -newermt 17:29` showed no host leftovers. The ruler's scratch was removed: `tA` and `tB` contain only `home`.

```
S=/tmp/tameshi-r18w2-RerunC2After-EpOq8v
bwrap --ro-bind / / --dev /dev --proc /proc --bind $S/tA /tmp --unshare-net --die-with-parent --chdir /tmp \
  env -i PATH=/home/vgpnk/.local/bin:/usr/bin:/bin HOME=/tmp/home LC_ALL=C \
  python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/defect-probes.py \
  --rev 01d586ddbc5fcd78659557c4e93a6ee8517b87d1
```

### Run A (text mode): exit 0, 45 s (20:31:01Z–20:31:46Z), all PROBE lines verbatim
```
PROBE P01 closed target=tools/evidence-disposition.py:445 G3 exact commit-object identity guard pristine_exit=0 mutant_exit=1; anchors=tools/evidence-disposition.py; mutant='if proc.returncode != 0 or resolved != rev:' -> 'if False:'; SELFTEST: FAIL (1/63 failed: v2-historical-tag-object; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.qh8q1tya)
PROBE P02 closed target=tools/evidence-disposition.py:552 G5 regular-blob mode guard pristine_exit=0 mutant_exit=1; anchors=tools/evidence-disposition.py; mutant='if kind != "blob" or mode not in TREE_MODES:' -> 'if kind != "blob":'; SELFTEST: FAIL (1/63 failed: v2-historical-symlink-mode; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.ehi5i86v)
PROBE P03 closed target=tools/registry-check.py:466 detached-checkout operation pristine_exit=0 mutant_exit=1; anchors=tools/registry-check.py; mutant='["git", "-C", clone_root, "checkout", "-q", "--detach", sha]' -> '["git", "-C", clone_root, "reset", "-q", "--hard", sha]'; SELFTEST: FAIL (1 of 46 cases: rev-clone-detached)
PROBE P04 closed target=tools/registry-check.py:96 source-revision minimum-length regex pristine_exit=0 mutant_exit=1; anchors=tools/registry-check.py; mutant='^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$' -> '^[^@]+@[0-9a-f]{1,40}:[0-9]+(-[0-9]+)?$'; SELFTEST: FAIL (1 of 46 cases: short-source-revision)
PROBE P05 closed target=tools/trace-inputs.py:82 O_RDWR write-mode exclusion pristine_exit=0 mutant_exit=1; anchors=tools/trace-inputs.py,.ufo/evidence/round-17/coldread/trace-inputs.py; mutant='WRITE_FLAGS_RE = re.compile(r"\\bO_(?:WRONLY|RDWR|CREAT|TRUNC|APPEND|TMPFILE)\\b")' -> 'WRITE_FLAGS_RE = re.compile(r"\\bO_(?:WRONLY|CREAT|TRUNC|APPEND|TMPFILE)\\b")'; SELFTEST: 29/30
PROBE P06 closed target=tools/trace-inputs.py:516 private PYTHONPYCACHEPREFIX setting pristine_exit=0 mutant_exit=1; anchors=tools/trace-inputs.py,.ufo/evidence/round-17/coldread/trace-inputs.py; mutant='env["PYTHONPYCACHEPREFIX"] = cache' -> 'env["PYTHONPYCACHEPREFIX"] = "."'; SELFTEST: 29/30
PROBE P07 closed target=tools/trace-inputs.py:644 successful root execve requirement pristine_exit=0 mutant_exit=1; anchors=tools/trace-inputs.py,.ufo/evidence/round-17/coldread/trace-inputs.py; mutant='if tracer.first_pid is None or tracer.first_pid not in tracer.exec_ok:' -> 'if tracer.first_pid is None:'; SELFTEST: 29/30
PROBE P08 closed target=tools/evidence-disposition.py: G2 518-539; G3 450-455 jj git init --colocate A=b175d572be77cb1073021aa0fb5447e3c6d9d3bd B=2466040b2cc106a1f1f39559e75601a829f5e8df D=4744ae445c54f699918618f885daf4b8e53c8be2 historical_rev=A; G2-live-bytes closed HEAD=2466040b2cc106a1f1f39559e75601a829f5e8df master=b175d572be77cb1073021aa0fb5447e3c6d9d3bd @-=2466040b2cc106a1f1f39559e75601a829f5e8df findings=['historical_input_uncommitted']; G3-ancestor closed HEAD=2466040b2cc106a1f1f39559e75601a829f5e8df master=4744ae445c54f699918618f885daf4b8e53c8be2 @-=2466040b2cc106a1f1f39559e75601a829f5e8df findings=['historical_input_unavailable']
PROBE P09 closed target=tools/registry-check.py:221-227 (timeout_s validation) literal JSON values NaN:closed exit=2 timeout_s_named registry-check: warning: live --root mode runs rows in the lane; rows may write into the root (use --rev to grade a throwaway clone); Infinity:closed exit=2 timeout_s_named registry-check: warning: live --root mode runs rows in the lane; rows may write into the root (use --rev to grade a throwaway clone)
PROBE P10 closed target=tools/registry-check.py:306-322, 385-387 (kill/communicate after timeout) timeout_s=1; setsid checker_exit=1 outer_timeout=False row_timeout=True survivors=[]; setpgid checker_exit=1 outer_timeout=False row_timeout=True survivors=[]
PROBE P11 closed target=tools/bash-witness-study.py:337-344 (materialize_target git show) rev=fecee8743e52eb8fb5fbb40782934cb619a1a96e clean_exit=0 clean_declared=True; canary GIT_DIR/GIT_WORK_TREE tainted_exit=0 timeout=False canary_changed=False declared=True WITNESS_DECLARE: declaration.json sha256=bcfb72bd190ee9039d90936cead7c62ef29e3d8c68d85c8f535a551113c28af1
DEFECT_PROBES: open=0 closed=11 total=11
exit=0
```
The "fixtures kept at /tmp/…" paths are inside the ruler's inner `/tmp` (= its W/tmp), which the ruler removes on exit.

### Run B (`--json`, same envelope, own `/tmp`, concurrent): exit 0, 43.9 s
The parsed payload is `schema=tameshi-defect-probes-v1`, `rev_resolved=01d586ddbc5fcd78659557c4e93a6ee8517b87d1`, `open=0 closed=11 total=11`.

The structured fields are P01–P07 `pristine_exit=0`, `mutant_exit=1`. P08–P11 have no pristine/mutant fields; they are behaviour probes. Status for every probe matches Run A. The only differences are run-unique values:
- P08 jj ids: A=676af19b…, B=ce8a970a…, D=e51a43fd…; findings are the same.
- P11 declaration sha: d3d3780f….
- Kept-fixture temp names.

### Guard probes: what kills each mutant
Every kill comes from a completed selftest with exactly one named failing case that matches the guard. None is a crash.

| Probe | Pristine / mutant exit | Killing case (failing count) |
|---|---|---|
| P01 | 0 / 1 | `v2-historical-tag-object` (1/63) |
| P02 | 0 / 1 | `v2-historical-symlink-mode` (1/63) |
| P03 | 0 / 1 | `rev-clone-detached` (1 of 46) |
| P04 | 0 / 1 | `short-source-revision` (1 of 46) |
| P05 | 0 / 1 | `rdwr-open-excluded` (`tools/trace-inputs.py:818-820`) |
| P06 | 0 / 1 | `pycache-prefix-private` (`:926-930`) |
| P07 | 0 / 1 | `root-exec-required` (`:872`) |

For P01–P04 the case names come from the ruler's excerpt. The ruler prints only `SELFTEST: 29/30` for P05–P07, so I identified those three cases with my own driver (F1 below). Pristine selftests are 63, 46 and 30 cases, against 56, 34 and 27 at base (`c2-probes-v2-183f87b.txt:1-7`).

P09 seen directly: `tools/registry-check.py --registry <row timeout_s=NaN|Infinity|-Infinity>` exits 2 each time with `rows[0].timeout_s (row 'timeout-nonfinite'): non-finite JSON number NaN` (likewise for `Infinity` and `-Infinity`). The rejection is specific to `timeout_s`; `-Infinity` goes beyond what the probe tests.

P11 scrub at the read rev: `tools/bash-witness-study.py:333-339` (`git_clean_env`) drops every `GIT_*` prefix and pins the global and system config. The git child at `:347-350` passes `env=git_clean_env()`.

## Findings (by severity)

### F1 (low–medium): P05–P07 count as closed because the measurement moved to the promoted file; the frozen round-17 collector still lets all three mutants survive at the read rev
- **Different files measured.** The base receipt measured `.ufo/evidence/round-17/coldread/trace-inputs.py` (`c2-probes-v2-183f87b.txt:5-7`). The tip measures `tools/trace-inputs.py`, because `trace_tool()` prefers the promoted copy (`defect-probes.py:335-342`).
  - This preference was already in the v1 ruler pre-registered before any fix (`aee4f36:.ufo/evidence/round-18/defect-probes.py:333-340`), so it is not a post-hoc re-route.
  - SKILL.md says it openly: `SKILL.md:1931` (round-17 copy "stays byte-identical as evidence") and `SKILL.md:1885` (round-18 tracing uses `tools/trace-inputs.py`).
- **The frozen copy still has the defects.** It is byte-identical at base and read rev (sha256 `521be95581a5…`). I ran each mutant against both copies at the read rev with a scratch driver (`$S/drive_trace.py`, run under bwrap in my clone, exit 0, both files restored and sha-verified):
  ```
  COPY promoted sha256=fb1d81f6… pristine exit=0 SELFTEST: 30/30
  MUTANT promoted P05 exit=1 SELFTEST: 29/30 fails=['rdwr-open-excluded'] verdict=killed
  MUTANT promoted P06 exit=1 SELFTEST: 29/30 fails=['pycache-prefix-private'] verdict=killed
  MUTANT promoted P07 exit=1 SELFTEST: 29/30 fails=['root-exec-required'] verdict=killed
  COPY r17 sha256=521be955… pristine exit=0 SELFTEST: 27/27
  MUTANT r17 P05 exit=0 SELFTEST: 27/27 fails=[] verdict=SURVIVED
  MUTANT r17 P06 exit=0 SELFTEST: 27/27 fails=[] verdict=SURVIVED
  MUTANT r17 P07 exit=0 SELFTEST: 27/27 fails=[] verdict=SURVIVED
  ```
- **It is still live in three places:**
  - It is an **active** registry row: `tools/registry.json:655-675` (`trace-inputs-round17-selftest`, `"status": "active"`). It held in the full run (`registry-full-e08271a.json:441-442`).
  - It is still a documented probe: `SKILL.md:1902`.
  - It is still a recheck: `corpus/knowledge/input-keyed-coldread-credit.md:3` names its `--selftest` (exit 0) as the drift check, and that check passes with all three guards removed.
- **Misleading output.** The PROBE detail `anchors=tools/trace-inputs.py,.ufo/evidence/round-17/coldread/trace-inputs.py` lists both paths, but only the promoted one is mutated.
- **Effect on C2:** the 0/11 holds for the canonical runtime. The P05–P07 part of "11/11 → 0/11" is closure by promotion, not an in-place fix. The frozen copy keeps the survivors by design, because its sha keys past receipts (`corpus/knowledge/guard-kill-closure.md:124`).

### F2 (low): every `target=` line label except P05–P07 is the base-rev line, so it points at the wrong code at the read rev
I re-located each anchor in `git show` extracts. Every guard anchor appears exactly once. The labels match `183f87b` exactly, which I also checked.

| Probe | Label (correct at 183f87b) | Actual location at 01d586dd |
|---|---|---|
| P01 | `evidence-disposition.py:445` | `:532`. Line `:445` is now the end of the shallow-repository refusal (`:442-445`). |
| P02 | `evidence-disposition.py:552` | `:645` |
| P03 | `registry-check.py:466` | `:786` |
| P04 | `registry-check.py:96` | `:104` |
| P05–P07 | `trace-inputs.py:82/516/644` | match |
| P08 | "G2 518-539; G3 450-455" | G2 raises at `evidence-disposition.py:612-633`; G3 identity and ancestor checks at `:532-545` |
| P09 | `registry-check.py:221-227` | `:234-249` |
| P10 | `306-322, 385-387` | `_kill_group` is gone. Now `run_row` at `:641-689` (Popen `start_new_session` `:676`, communicate `:686`) and `_cleanup_row` at `:570` |
| P11 | `bash-witness-study.py:337-344` | `:347-351` |

The counts are unaffected because mutation is byte-anchored with a uniqueness check (`defect-probes.py:257-261`). Path:line citations copied from the tip receipts (the L1's and mine) are wrong at the read rev.

### F3 (low; owned by the entry review, noted because C2 names this entry): the knowledge entry still says PENDING and "untracked" at the read rev
- `corpus/knowledge/guard-kill-closure.md:118` says "PENDING: `tools/trace-inputs.py` is untracked at 183f87b".
- `:132` says "Tools not at the landed tip: `tools/trace-inputs.py` (untracked)… Every landed-tip number is PENDING".
- `:136` says "After-measurement (PENDING, filled by L1)… open/closed count: PENDING".

`git cat-file -e 01d586dd:tools/trace-inputs.py` exits 0 (and `183f87b` exits 128). So "not at the landed tip" is false at the read rev, and the entry does not yet record the measured 0/11. It is labelled "filled by L1", so this may be pending by plan.

### F4 (info): ruler v2 was changed after the v1 tip errored; the change was applied to base too and is defensible
- **Why v1 errored at the tip** (`c2-probes-e08271a.txt:9-13`):
  - The P01/P02 pristine selftests failed 3/63 (`v2-jj-*` cases) because the v1 child `PATH=/usr/bin:/bin` lacks jj.
  - The P08 G2 case got `historical_input_unavailable` because the fixed tool refuses an unbound jj workspace (`evidence-disposition.py:493-496`).
- **What v2 changed** (`git diff aee4f36 01d586dd -- defect-probes.py`): it adds the jj directory to the child `PATH` (`:156`) and `lane.branch` to the P08 fixture (`:482-485`).
- **It was applied to base too:** v2 at base is still open=11/11 (`c2-probes-v2-183f87b.txt:12`).
- **Side effect:** that directory is `/home/vgpnk/.local/bin` (49 entries), placed first, so it shadows `bat`, `fd`, `gh`, `jq` and `rg`.
  - `git`, `python3`, `sh`, `bash`, `strace` and `setsid` still resolve to `/usr/bin`.
  - A grep of the five probed tool files finds no call to any shadowed name.

### F5 (info, ruler calibration): any mutant exit 1 counts as closed (`defect-probes.py:350-353`, `:392`)
A Python crash also exits 1, so a crash-kill would be counted as closed. That did not happen here: every mutant run printed a completed summary with exactly one named failing case (table above).

## Process incident (self-reported)
- **What happened:** at 17:29:07 -0300, a quoting/sequencing error in my nested-bwrap test command ran `touch /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ro-test` on the **host**, outside the sandbox. This created an empty, untracked file at the lane root.
- **Fix:** I removed it with `rm` at 17:29:27; `ls` now reports "No such file".
- **No jj snapshot captured it.** Read-only `jj --ignore-working-copy op log` shows the last operation is `68ffcf1df0de` at 17:24:26.511, a push of `master`. Nothing ran between creation and removal, and `jj --ignore-working-copy diff -r @ --summary` does not contain `.ro-test`.
- No git command touched the index. Net change to lane content: none. The lane-root directory's mtime was bumped [INFERENCE].
- Every later command used `[ -w … ]` for read-only checks; nothing else wrote to the lane.

## Residual risk and verification gaps
- **Not run by me:** the base side (`--rev 183f87b`). The "before" 11/11 rests on the L1's `c2-probes-v2-183f87b.txt`, which is outside this target.
- **Envelope:** I ran the ruler only inside the outer read-only envelope, not directly on the host. The ruler's inner per-child envelope is unchanged by this, and I saw no difference from the L1's receipt.
- **Not checked:** whether the owning tools' selftests carry failure-backed cases for P08–P11. Those are behaviour probes, measured here only by the ruler. The C2 wording "closed with failure-backed selftests" is backed by this run only for P01–P07.
- **P10 scope:** P10 observes survivors only inside the ruler's PID namespace, as documented in `defect-probes.py:12-14`.

Verdict: holds. At `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` the ruler gives open=0 closed=11 total=11 (exit 0, twice), with P01–P07 all pristine_exit=0 mutant_exit=1. Two residuals: P05–P07 are closed only in the promoted `tools/trace-inputs.py`, and the frozen, still-registered round-17 collector still lets all three survive (F1); most `target=` line labels are stale (F2).
