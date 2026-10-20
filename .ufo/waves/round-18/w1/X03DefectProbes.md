# Round 18 wave 1 — X03 defect probes

**Axes:** depth and calibration (verification-fixture craft); operability is monitored.  
**Scope:** contract A, probes P01–P11, at pinned landing `183f87b899e6cae46be98d251cbc87fb5118f6ca`.

## Execution and retained result

The lane was cloned at the pinned revision into `/tmp/tameshi-r18w1-X03DefectProbes-_hc2eq4c/fleet/tameshi-shokunin`; clone and detached checkout both exited 0. The probe runner was copied into that clone (it is new and absent from the pinned commit). Git environment was explicitly scrubbed for the setup and probe invocation. The runner’s subprocesses used the bwrap envelope documented in `defect-probes.py:4-14`, including a read-only fleet-source bind, private `/tmp` backed by W/tmp, `env -i`, and isolated PID/network namespaces. P10 observes and kills marker processes inside the same PID namespace.

Commands exercised:

- `python3 .ufo/evidence/round-18/defect-probes.py --selftest` under the same bwrap envelope — **exit 0**, `SELFTEST: PASS (6 cases)`.
- `python3 .ufo/evidence/round-18/defect-probes.py --rev 183f87b899e6cae46be98d251cbc87fb5118f6ca`, cwd at the temporary lane clone — **exit 0**, `DEFECT_PROBES: open=11 closed=0 total=11`.

Selftest output:

```text
SELFTEST_CASE replace-one-anchor PASS (one exact replacement)
SELFTEST_CASE reject-nonunique-anchor PASS (missing and duplicate anchors refused)
SELFTEST_CASE scrub-inherited-git PASS (env -i omits inherited repo selectors; explicit canary is retained)
SELFTEST_CASE preserve-nonfinite-json-literal PASS (NaN remains an unquoted JSON token)
SELFTEST_CASE unique-process-marker PASS (one unique marker for P10 process observation)
SELFTEST_CASE probe-id-domain PASS (eleven stable probe ids)
SELFTEST: PASS (6 cases)
```

## Probe outcomes at the base

Each guard-removal probe first ran its owning pristine `--selftest`; a nonzero pristine result is treated as an evaluation error. The table records the exact one-occurrence mutant and the paired pristine/mutant exits. Trace collector probes also count-check the guard in both candidate collector paths when present; at this landing only the historical round-17 path was present.

| Probe / target line | Exact guard removal | Pristine → mutant | Base result |
|---|---|---:|---|
| P01 `tools/evidence-disposition.py:445` | `if proc.returncode != 0 or resolved != rev:` → `if False:` | 0 → 0; `SELFTEST: PASS (56/56)` | open |
| P02 `tools/evidence-disposition.py:552` | `if kind != "blob" or mode not in TREE_MODES:` → `if kind != "blob":` | 0 → 0; `SELFTEST: PASS (56/56)` | open |
| P03 `tools/registry-check.py:466` | `checkout -q --detach sha` → `reset -q --hard sha` | 0 → 0; `SELFTEST: PASS (34 cases)` | open |
| P04 `tools/registry-check.py:96` | source regex `{7,40}` → `{1,40}` | 0 → 0; `SELFTEST: PASS (34 cases)` | open |
| P05 `.ufo/evidence/round-17/coldread/trace-inputs.py:82` | delete `RDWR|` from `WRITE_FLAGS_RE` | 0 → 0; `SELFTEST: 27/27` | open |
| P06 `.ufo/evidence/round-17/coldread/trace-inputs.py:516` | `env["PYTHONPYCACHEPREFIX"] = cache` → `env["PYTHONPYCACHEPREFIX"] = "."` | 0 → 0; `SELFTEST: 27/27` | open |
| P07 `.ufo/evidence/round-17/coldread/trace-inputs.py:644` | remove `or tracer.first_pid not in tracer.exec_ok` | 0 → 0; `SELFTEST: 27/27` | open |

Behavioural probes (each fixture was under the temporary W and ran against the detached base clone):

| Probe / target line | Exact fixture | Base observation |
|---|---|---|
| P08 `tools/evidence-disposition.py` G2 `518-539`; G3 `450-455` | `jj git init --colocate`; commit A with pinned tool bytes, B with changed live bytes, and side commit D with the B tool bytes. Keep `@-`/Git `HEAD` at B, then move `refs/heads/master` first to A and then D. A=`a5f138f268d6e250a895169ed38c92298ba094d2`, B=`e35f7db17f67d37f84192209a6a7a17497ef8a37`, D=`921285c7b5f254dd55b9dba03500fb789d7c8d4a`. | G2: `HEAD=B`, `master=A`, `@-=B`, clean verdict. G3: `HEAD=B`, `master=D`, `@-=B`, clean verdict. Both follow `HEAD`: open. |
| P09 `tools/registry-check.py:221-227` | Two synthetic registry rows containing raw JSON `NaN` and `Infinity` as `timeout_s`; each names row `timeout-nonfinite`. | Both were accepted into execution and crashed: NaN `ValueError: cannot convert float NaN to integer`; Infinity `OverflowError: cannot convert float infinity to integer`. Exit 1, open. |
| P10 `tools/registry-check.py:306-322, 385-387` | `timeout_s=1`; separately run `setsid sh -c 'exec sleep 40 </dev/null >/dev/null 2>&1' ... & sleep 40` and a Python `os.setpgid(0,0); time.sleep(40)` escape. Each escaped process carries a unique environment marker. | Both checkers returned `got=timeout` and left a marker process alive at the immediate post-return check (`survivors=[5]` in each isolated PID namespace). The supervisor then killed both. Open. |
| P11 `tools/bash-witness-study.py:337-344` | Clone the pinned kagi source into W; compare a clean `declare` baseline against `declare` with `GIT_DIR` and `GIT_WORK_TREE` explicitly set to a separate scratch canary repo. Snapshot the canary before/after. Pinned source revision: `fecee8743e52eb8fb5fbb40782934cb619a1a96e`. | Clean baseline exit 0 and declared successfully. Tainted run exit 2 with `CANNOT-EVALUATE` from `git show`; canary contents/index/objects were unchanged. The output difference demonstrates a Git subprocess honoring the exported selectors. Open. |

Final machine-readable trailer from the base run: `DEFECT_PROBES: open=11 closed=0 total=11`. No probe error occurred. The P10 escape processes were cleaned up inside their sandbox; no canary changes were observed in P11.

## Safety, risks, and blockers

- Mutants were applied only to the temporary clone, restored in `finally`, and each was anchored to one exact source string. No live lane instrument or sibling repository was edited.
- P08 requires `jj`; P11 requires the sibling `kagi-shokunin` repository and its pinned object. If either prerequisite is unavailable, the probe fails closed as could-not-evaluate (exit 2).
- No tools were installed or updated. No blocker remains.

**Verdict: built — contract A is implemented; all eleven expected survivors were open at the pinned base, and the synthetic selftest passed 6/6.**
