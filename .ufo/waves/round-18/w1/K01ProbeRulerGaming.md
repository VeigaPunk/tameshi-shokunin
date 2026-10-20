# K01ProbeRulerGaming — attack on the C2 ruler (contract A)

Seat: TameshiR18.K01ProbeRulerGaming. Scope: `.ufo/evidence/round-18/defect-probes.py`
(does not exist yet — the executor TameshiR18.X03DefectProbes is writing it now).
Everything below attacks the *measurement instrument* contract A before it is
implemented, plus conditions under which `open→closed` is meaningful.

Base evidence: lane tip `183f87b899e6cae46be98d251cbc87fb5118f6ca`; all source
references are `git show <rev>:<path>` against that revision. All 11 defects
were verified open-at-base by direct code reading (details in §2).

## 1. When open→closed is meaningful, and when it is self-fulfilling

**What a guard-removal probe (P01–P07) actually measures:** "the owning tool's
`--selftest` exits nonzero when *this exact text mutation* is applied." That is
**mutant sensitivity**, not behavioral coverage of the guard. R17-GUARD-COVERAGE
(routed item 3, `corpus/lessons/round-17-verifier-spotcheck.md:428-432`) says
exactly this: "code existence is not behavioral coverage." The ruler makes the
confusion *structural*: it equates "selftest catches the named removal" with
"the guard works."

The self-fulfilling risk is real and specific. Wave-1 fix seats (X04/X05/X06)
can read the probe file the moment X03 commits it — the exact mutant strings,
the counting rule, the classification oracle. A fix author who wants
`open→closed` on the cheap does not need to make the guard *work*; they need
*any* selftest case that trips on that diff. This is conspiring-author
measurement unless the acceptance conditions below are enforced. It is not
automatic disqualification — the probes are anchored on mutations that
*demonstrably survived* in round 17 (`.ufo/waves/round-17/w2/Mutate*V2.md`
kill tables), so closing them does remove a proven coverage hole — but
"closed" certifies **"the named r17 mutant now kills the selftest"**, nothing
broader. The C2 claim wording must stay at that bound.

**Asymmetry worth naming (both directions are mismeasurement):**
- False-closed: fix adds a mutant-sensitive-but-behaviorally-irrelevant case
  (see gaming §3.1). Defect still present, probe reports closed.
- False-open: fix repairs the defect *without deleting the old line* (e.g.
  adds a compensating check elsewhere, or fixes the bug upstream of the
  guarded call). The mutant still applies and the selftest may still pass on
  the mutated copy — probe stays `open` even though the defect is dead in
  production paths. This direction blocks honest credit; the L1 should be
  aware the ruler punishes non-destroying fixes.

## 2. Verification that all 11 defects are open at base (183f87b)

- P01 (G3 tag object): `evidence-disposition.py:447-455` —
  `rev-parse --verify rev^{commit}` resolves tag objects to the commit; the
  `resolved != rev` comparison at :445-448 (mutant G3Commit, survived 56/56
  in `MutateDispositionV2.md`) is the only barrier and it does not reject
  annotated tags — a tag peeled to a matching commit still passes.
- P02 (G5 symlink): `evidence-disposition.py:552` — `mode not in TREE_MODES`
  (`"100644","100755"` :518); mutant dropped the mode half, survived.
- P03 (detached checkout): `registry-check.py:466` — `"checkout","-q","--detach",sha`;
  mutant `reset --hard sha` survived 34/34 (`MutateRegistryCheck.md` M06).
- P04 (short-rev regex): `registry-check.py:96` —
  `SOURCE_RE = r"^[^@]+@[0-9a-f]{7,40}:..."`; mutant `{1,40}` survived (M07).
- P05 (O_RDWR): `.ufo/evidence/round-17/coldread/trace-inputs.py:82` —
  `WRITE_FLAGS_RE`; deleting `RDWR|` survived 27/27 (`MutateTraceInputs.md` M01).
- P06 (pycache): same file :516 — `env["PYTHONPYCACHEPREFIX"] = cache`;
  mutant `"."` survived (M03).
- P07 (execve): same file :644 — `first_pid not in tracer.exec_ok` removal
  survived (M04).
- P08 (HEAD vs branch tip): `evidence-disposition.py:450` `merge-base
  --is-ancestor rev HEAD` and `:518` `tree_entry(lane,"HEAD",path)` — both
  follow HEAD, not `refs/heads/<branch>`. Open.
- P09 (NaN timeout): `registry-check.py:281` `json.loads` with no
  `parse_constant` → literal `NaN`/`Infinity` parse to float; row validation
  `:220-227` (`isinstance(ts,bool) or not isinstance(ts,(int,float)) or
  ts<=0`) passes `NaN` (`NaN<=0` is False); verified empirically:
  `communicate(timeout=nan)` → `ValueError`, `timeout=inf` → `OverflowError`
  → traceback, exit ≠2. Open.
- P10 (setsid escape): `registry-check.py:306-321` `_kill_group` signals
  `os.getpgid(proc.pid)` only; a `setsid()` grandchild is in a new group.
  Rows spawn with `start_new_session=True` (:375) so `killpg` covers only the
  row's own session. Open.
- P11 (GIT_* leak): `tools/bash-witness-study.py:337` `subprocess.run` for
  `git -C kagi show` passes **no env** → inherits `GIT_DIR`; sweep at :604-605
  uses `sweep_env()` (:572-576) whose `SCRUB_ENV` (:116-117) contains five
  non-GIT names only. Open.

## 3. Ways a fix flips a probe without fixing the defect

**3.1 Meta-cheat that closes all seven guard probes at once:** a selftest
case that *hashes or greps its own source* — e.g. "assert sha256(__file__)
== pin" or "assert 'RDWR' in Path(__file__).read_text()". Every P01–P07
mutant trips it; zero behavioral coverage was added. Contract A's literal
text ("selftest cases that FAIL when the guard is removed") permits this.
*Detection: the probe must print the failing case names (see §4-C6); any
case that reads the tool's own source bytes is an incidental kill.*

**3.2 Incidental kill:** the mutant changes observable behavior beyond the
guard, and an unrelated new case trips on the side effect, not the guard.
Example for P03: a new fixture asserts the clone's branch `master` still
points at clone origin — `reset --hard` moves it and fails the case even if
the fixer never wrote a detached-HEAD assertion. Selftest now "covers" the
mutant while still not verifying `symbolic-ref -q HEAD` fails.

**3.3 P08 half-fix:** the probe spec says "G2/G3 under a jj-colocated
fixture". G2 (`:518`) and G3 (`:450`) are *independent* HEAD sites. If the
fixture only exercises the G3 path (e.g. a waiver where the live path is
absent at HEAD and at tip alike), a fix that converts only `merge-base` to
the branch tip flips the probe while `tree_entry(lane,"HEAD",…)` still
follows HEAD. One probe over two guards needs the fixture to drive *both*
through diverging outcomes, or two probes.

**3.4 P09 three sub-defects, one probe:** the fix must (a) reject literal
`NaN`/`Infinity` at JSON parse (`parse_constant`), (b) reject non-finite
*numeric* values that parse fine (`1e999` → `inf` parses under default and
under `parse_constant`; only a `math.isfinite` check catches it), (c) name
`timeout_s` in the exit-2 error. A fix doing only (a) leaves `1e999` and
`-Infinity`-as-number holes; a fix doing (a)+(b) but printing "invalid
timeout" without the literal string `timeout_s` fails the closed criterion
anyway (probe stays open — false-open); a fix that crashes differently
(e.g. wraps `communicate` in `except Exception → got=unavailable`) turns
the traceback into a *clean row result* — still `open` per spec, but the
traceback-hiding is arguably a real improvement the ruler cannot credit.

**3.5 P10 narrow-kill and over-kill:** (a) fixture uses `setsid`+`sleep`;
a fix that kills `/proc` children matching the name `sleep` or only first-
generation descendants (a `setsid; fork; setsid` double escape) passes the
probe and fails the contract's "every descendant". (b) The reverse: a fix
that implements `PR_SET_CHILD_SUBREAPER` and then SIGKILLs *every* PID that
reparents to it — including the probe harness's own unrelated children —
kills the escaped process *and* the harness; if the harness dies mid-scan
the probe can report `closed` vacuously or error. The probe's liveness
check must verify the escaped PID *and* a sibling-process sentinel survive
appropriately.

**3.6 P11 partial scrub:** contract names only GIT_DIR+GIT_WORK_TREE for
the canary. A fix that `pop`s exactly those two keys passes P11 while
`GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_CONFIG`… still flow into both
subprocess sites (:337 inherits env entirely). Contract E demands *all*
inherited `GIT_*`; the probe under-measures its own contract.

**3.7 Mutant-string fragility cuts both ways:** `count==1` else exit-2 is
fail-closed for refactors (good), but a fix that *renames* the guarded
expression while keeping a vulnerable structure elsewhere cannot be probed
at all — the run goes exit-2 and blocks C2 entirely. Also: if the mutant
string coincidentally appears once more after the fix (e.g. the fix adds a
comment quoting the regex), count==2 → error → whole claim blocked by a
comment. The mutant anchor should match on a non-comment, non-string code
position or tolerate `count>=1` with first-match anchoring.

**3.8 Self-fulfilling scheduling:** if X03 writes probes *after* seeing the
fix diffs, mutants can be chosen to fail under the fix (e.g. anchoring on
text the fix deletes). The committed-before-fix ordering is the only
defense — and it must be enforced at the *blob* level (§4-C2), since a
later fix commit could also edit `defect-probes.py` itself to weaken a
stubbornly-open probe.

## 4. Proposed acceptance conditions (concrete)

- **C1 — red-before-fix committed receipt:** the probe file is committed in
  a lane commit that precedes every commit touching the 4 target files, and
  the wave records an `exit 0, DEFECT_PROBES: open=11 closed=0 total=11`
  receipt at `183f87b…` (or the declared base). Any probe that is
  could-not-evaluate at base makes the run exit 2 → receipt invalid.
- **C2 — probe blob pinned:** the base receipt records sha256 of
  `defect-probes.py`; the final claim requires the same blob, or a re-run
  base receipt committed alongside any probe edit. Otherwise "open→closed"
  can be manufactured by editing the ruler post-review.
- **C3 — pristine control inside the harness:** for every guard-removal
  probe, run the owning `--selftest` on the *unmutated* clone first and
  require exit 0; classify `closed` only on `unmutated-pass ∧ mutated-fail`.
  This kills the "selftest fails for environmental/all-input reasons →
  vacuous closed" flip, and turns previously-nonzero selftests into an
  explicit error rather than silent mismeasurement. Contract A does not
  state this; add it.
- **C4 — mutants anchored on guard code:** mutant old-strings copied
  verbatim from the surviving-mutant reports (MutateDispositionV2 G3Commit
  `proc.returncode != 0 or resolved != rev`, G5Mode `mode not in
  TREE_MODES`; MutateRegistryCheck M06 argv tail, M07 `{7,40}`;
  MutateTraceInputs M01 `RDWR|`, M03 `= cache`, M04 `or tracer.first_pid
  not in tracer.exec_ok`), not on test/fixture text. Anchoring on test code
  would let a fix flip a probe by deleting a test.
- **C5 — behavioural probes observe externally visible effects only:**
  P08 reads the tool's verdict/exit against a ground-truth fixture; P09
  reads process exit + stderr text; P10 checks `kill(pid,0)` on the escaped
  PID after a bounded poll (avoid the reap race — poll ≥2 intervals, not a
  single sleep+check); P11 checks canary-repo object visibility/mutation.
  No behavioural probe may assert on implementation internals (function
  names, call counts).
- **C6 — transparency fields:** each `PROBE` line for P01–P07 appends the
  failing selftest case names; the summary line gains `errors=K`; exit 2
  iff K>0. Reviewers then reject closures whose failing cases are
  meta-checks (§3.1) or unrelated cases (§3.2).
- **C7 — fixture design minimums (against §3.3–3.6):**
  - P08: two sub-fixtures (one per guard site) or one waiver that forces
    both G2 and G3 to diverge between HEAD and tip; branch name ≠ `master`
    and ≠ the lane's real branch (kills hardcoded-ref fixes). jj 0.45.1 is
    on PATH; `jj git init --colocate` then `git checkout --detach <A>` gives
    HEAD≠tip in a colocated repo.
  - P09: fixture set = {literal `NaN`, literal `Infinity`, `1e999`, `true`,
    `-5`}: closed requires *each* rejected with exit 2 naming `timeout_s`,
    else report partial explicitly.
  - P10: escaped process = `setsid` grandchild running a generic binary
    (`python3 -c 'import time;time.sleep(60)'`), plus a non-targeted
    sentinel process the fix must not kill.
  - P11: canary exports `GIT_DIR`+`GIT_WORK_TREE` *and* a second canary
    with `GIT_INDEX_FILE`; both subprocess sites (:337 git show, :604
    sweep) must be covered — e.g. canary contains the same `rev:path` with
    different bytes so honoring `GIT_DIR` changes observable output, not
    just exit.
- **C8 — claim wording bound:** C2's "0/11" certifies "the seven named r17
  surviving mutants now kill their selftests and four behavioural defects
  produce the corrected external effect" — the report must not generalize
  to "guards are covered" (the r17 lesson's exact complaint).

## 5. Residual holes the ruler cannot see (for wave-2 falsifiers)

- Guard-removal probes measure the *named* mutant only; sibling mutants
  (e.g. `rev-parse` without `^{commit}`, `TREE_MODES` widened to include
  `120000`) remain unmeasured unless someone writes second-generation
  mutants.
- `--only ID` + exit-0 lets a partial run print a `total=1` summary that a
  careless reader could miscount; recommend the summary line always prints
  the denominator of the *full* suite plus a `selected=K` field.
- Probe `--selftest` (contract A) must be synthetic-only; nothing in the
  spec prevents the probe file from being counted as an instrument input
  and self-invalidating if later edited — keep it out of credit ledgers.

**Verdict: partial — contract A is measurable and fail-closed on errors, but open→closed is only meaningful if pristine-control (C3), probe-blob pinning (C2), failing-case transparency (C6) and the §4-C7 fixture minimums are added; as specified, all seven guard probes can be flipped by one source-grep selftest case, and P08/P09/P10/P11 each admit a narrow or over-broad fix that flips the probe without fixing the routed defect.**
