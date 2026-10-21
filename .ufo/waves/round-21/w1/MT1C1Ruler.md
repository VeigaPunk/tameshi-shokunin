done — five single-point ruler mutants probed; 2 KILLED, 3 SURVIVED, 0 INCONCLUSIVE. All five scratch copies restored byte-for-byte; the lane ruler and spec were never edited.

# MT1C1Ruler — frozen C1 ruler mutation probe

## Axes and scope

- **Calibration:** distinguish observed detector sensitivity from unexercised rejection/error paths. A surviving ruler mutant is a coverage finding, not a change to the frozen contract.
- **Operability:** run the same bounded, real ruler invocation on pristine, mutated and restored bytes, recording receipts, process status and hashes.
- Target: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py` at `33d03b716d3edcf1d8656d46d6df61801d232c52`.
- Selected frozen population: `MB03,D11,R02`, spanning bash-witness, disposition and registry selftests. The assignment permits a 2–3-ID diagnostic subset; trace-inputs was not included.
- The supplied full-population baseline is killed=0/survived=18. This probe observed only the selected subset: killed=0/survived=3/inconclusive=0 before and after every mutation. It does **not** independently remeasure all 18.
- Five independent scratch copies lived under `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/{anchor,control,timeout,mapping,exit}`. Each had its own unmodified copy of `c1-mutants.json` and its own `TMPDIR`. No subagents, background jobs, lane commits, index operations, integrations or other agent runtimes were invoked.

## Detector and expected observation

For each copy, the detector executed this exact argv, with `NAME` substituted by the directory names above:

```text
python3 /tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/NAME/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 33d03b716d3edcf1d8656d46d6df61801d232c52 --only MB03,D11,R02 --jobs 1 --json
```

Its cwd was `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/NAME`. The process environment was the invoking environment minus every `GIT_*`, then these fixed overrides:

```text
TMPDIR=/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/NAME/tmp
GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_NOSYSTEM=1
```

All ruler-created clones consequently remained under this seat's scratch. The ruler's existing bwrap selftest envelope was retained, including its separate environment scrub, read-only host root, private writable scratch, isolated network and per-selftest 900-second timeout. An additional **600-second wall-clock bound per ruler invocation** was applied externally; none expired. Five copies ran concurrently within each of the three synchronous phases; `--jobs 1` kept each individual ruler's tool work sequential.

Expected semantic observation:

```json
{"returncode":1,"counts":{"killed":0,"survived":3,"inconclusive":0,"total":3},"rows":[["MB03","SURVIVED",null],["D11","SURVIVED",null],["R02","SURVIVED",null]]}
```

A ruler mutant is KILLED here only when pristine and restored observations match that expectation, restored bytes match pristine bytes, and the mutated semantic observation differs. Otherwise an unchanged observation means SURVIVED; a failed pristine/restored prerequisite would mean INCONCLUSIVE. No baseline failure occurred. The normal ruler exit 1 is expected for this all-surviving population, not a failed pristine control.

The comparison deliberately excludes elapsed seconds, temporary-path-dependent output digests and the ruler's own changed hash: those are not behavioral kill evidence. Complete raw stdout and stderr were retained, not normalized or discarded.

## Mutant table — observed output

Counts below are `killed/survived/inconclusive`; every receipt had total=3. `P`, `M`, `R` mean pristine, mutated, restored. Ruler-mutant verdicts in the final column are distinct from the verdicts the ruler assigns to the three frozen tool mutants.

| Ruler mutant | Single behavior-bearing change, frozen line | Expected distinguishing detector condition | P: counts; exit | M: counts; exit; rows | R: counts; exit | Ruler-mutant verdict |
|---|---|---|---|---|---|---|
| anchor | L110: `if r["anchor_count"] != 1:` → `if r["anchor_count"] > 1:`; mistakenly permits a missing anchor | Need an anchor count of 0 to distinguish this weakening; the assigned subset could detect a difference only if it supplied one | `0/3/0; 1` | `0/3/0; 1`; all three SURVIVED | `0/3/0; 1` | **SURVIVED** |
| control | L114: `if c["exit"] != 0:` → `if False:`; deletes pristine-control rejection | Need a failed or timed-out pristine control; otherwise both variants continue normally | `0/3/0; 1` | `0/3/0; 1`; all three SURVIVED | `0/3/0; 1` | **SURVIVED** |
| timeout | L126: timeout verdict `INCONCLUSIVE` → `KILLED`, retaining reason `timeout` | Need a mutant selftest timeout to distinguish an inconclusive run from a false kill | `0/3/0; 1` | `0/3/0; 1`; all three SURVIVED | `0/3/0; 1` | **SURVIVED** |
| mapping | L127: `elif res["exit"] == 0:` → `elif res["exit"] != 0:`; reverses non-timeout mapping | All three real mutant selftests exit 0; detector must reject any KILLED label for them | `0/3/0; 1` | `3/0/0; 0`; all three **KILLED despite selftest exit 0** | `0/3/0; 1` | **KILLED** |
| exit | L151: `return 0 if counts["KILLED"] == len(rows) else 1` → same expression with `else 0` | Counts remain all-surviving, so the process must still exit 1 | `0/3/0; 1` | `0/3/0; 0`; all three SURVIVED | `0/3/0; 1` | **KILLED** |

In every invocation, each selected anchor count was exactly **1**. Every pristine control and every actual frozen-mutant selftest returned exit **0**, timeout **false**, with these final stdout summaries:

| Owning tool | Selected ID | Control and tool-mutant summary |
|---|---|---|
| `tools/bash-witness-study.py` | MB03 | `VERDICT: PASS` |
| `tools/evidence-disposition.py` | D11 | `SELFTEST: PASS (63/63)` |
| `tools/registry-check.py` | R02 | `SELFTEST: PASS (48 cases)` |

Thus the mapping mutant's three reported kills are fabricated by that deliberate ruler mutation; they are **not** C1 capability improvements or actual killed tool mutants.

### Actual stderr

All pristine and restored runs, and the mutated `anchor`, `control`, `timeout` and `exit` runs, emitted exactly:

```text
C1 MB03 tools/bash-witness-study.py SURVIVED
C1 D11 tools/evidence-disposition.py SURVIVED
C1 R02 tools/registry-check.py SURVIVED
C1: killed=0 survived=3 inconclusive=0 total=3 rev=33d03b716d3edcf1d8656d46d6df61801d232c52
```

SHA-256 of that stderr: `f3d728db2b700ffccab3e877df6a5f98cd0b848899c6a7ca07a36e90b8b2d372`.

Only the mutated `mapping` run emitted:

```text
C1 MB03 tools/bash-witness-study.py KILLED
C1 D11 tools/evidence-disposition.py KILLED
C1 R02 tools/registry-check.py KILLED
C1: killed=3 survived=0 inconclusive=0 total=3 rev=33d03b716d3edcf1d8656d46d6df61801d232c52
```

SHA-256 of that stderr: `d576f8d7c6f9c96df9d1564019e05bb8373e938b950427a83f6e000705c6bee1`.

## Surviving guards and unexercised observations

1. **Anchor-count rejection, L110–112:** the mutation allowing a zero-match anchor survived. Every observed count was 1; neither missing-anchor nor multiple-anchor rejection was exercised. This does not establish that the original guard is defective.
2. **Pristine-control gate, L114–116:** deleting it survived. All controls were green, so no observation exercised rejection of a nonzero control or a timed-out control (`exit=None`).
3. **Timeout → INCONCLUSIVE, L125–126:** converting timeout into KILLED survived because no mutant timed out. The `selftest()` TimeoutExpired return at L49–50 was likewise not exercised.
4. **Nonzero mutant exit → KILLED, L129–130:** the zero-exit half of the mapping was exercised and killed an inversion, but no actual tool-mutant selftest exited nonzero. Correct recognition of a real failed selftest therefore remains unobserved.
5. **Other exit branches:** the normal non-kill exit 1 was exercised and protected by the detector. Genuine all-killed success exit 0, mixed/inconclusive populations, setup exit 2 and usage exit 64 were not exercised. The corrupted mapping reaching exit 0 is not an independent test of a genuine all-killed population.

These are bounded coverage findings for this diagnostic subset, not evidence that all 18 frozen cases or arbitrary failure environments exercise those guards. No failed-control fixture, synthetic timeout, altered population or second contract was added just to obtain more kills.

## Exact executed commands and statuses

The three phase commands below were run synchronously through Python `subprocess.run(..., capture_output=True, timeout=650)`; each detector internally waited for all five concurrent ruler processes, each bounded at 600 seconds:

```text
python3 /tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/detect.py pristine
python3 /tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/detect.py mutated
python3 /tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/detect.py restored
```

All three driver commands exited **0**, with empty driver stderr. Driver exit 0 means all JSON observations were collected, **not** that mutated receipts were correct. Child ruler exits are the explicit P/M/R table above.

| Copy | Pristine seconds | Mutated seconds | Restored seconds |
|---|---:|---:|---:|
| anchor | 22.174 | 22.929 | 23.488 |
| control | 22.182 | 22.923 | 23.518 |
| timeout | 22.163 | 22.810 | 23.468 |
| mapping | 22.151 | 22.944 | 23.552 |
| exit | 22.158 | 22.913 | 23.463 |

Pin provenance was read with these exact argv under the Git-scrubbed environment plus the two fixed Git-config overrides; both exited **0**, stderr empty:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 33d03b716d3edcf1d8656d46d6df61801d232c52:.ufo/evidence/round-21/c1-survivors.py
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 33d03b716d3edcf1d8656d46d6df61801d232c52:.ufo/evidence/round-21/c1-mutants.json
```

Their stdout hashes matched the initial lane bytes and all pristine copies. SHA-256 was computed from captured stdout without rewriting the lane.

Initial hash command, exit **0**:

```text
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-mutants.json
```

Restoration hash command, exit **0** (brace expressions expanded by Bash):

```text
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-mutants.json /tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/{anchor,control,timeout,mapping,exit}/c1-survivors.py /tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/{anchor,control,timeout,mapping,exit}/c1-mutants.json
```

## Hashes and exact restoration evidence

Common ruler SHA-256 **before every edit and after every restoration**:

```text
a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396
```

| Copy | Mutated ruler SHA-256 | Restored SHA-256 |
|---|---|---|
| anchor | `df062ef8f611377d588a4248035ae7332cd0337593c11147a826c0595bc8ca9d` | common pristine hash above |
| control | `0358c9c5c395f0ea9ac6aa7fd8e386f6f433c0baed2e117e871bdb83900ce950` | common pristine hash above |
| timeout | `21d9b2136e95e64402491109195e616a3132806b57a34272b62c3286751e3ccc` | common pristine hash above |
| mapping | `8222b4baec3b2b700955c267a34c32639a1d5a999358ad9bef09b931a630fcca` | common pristine hash above |
| exit | `a3a16da49f918ad094920399b4232c52f2a5225c34cdf5b47dc0a82ca8236327` | common pristine hash above |

Spec SHA-256 for the committed pin, initial lane bytes, every phase of every scratch copy and final lane bytes:

```text
670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c
```

Each mutation was undone with a one-line anchored edit before the restored detector phase. The restored phase independently emitted the common ruler hash, original spec hash and original semantic observation in all five receipts. Final lane hashes were also unchanged. No lane source patch or clone commit is delivered: this is an investigation, not a permanent fix.

## Evidence paths

The observations and restoration evidence necessary for the scoped result are embedded above; the following scratch files preserve the complete, unabridged receipts as supplemental evidence:

- Driver and expected semantic projection: `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/detect.py`.
- Full phase metadata: `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/pristine.json`, `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/mutated.json`, `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/restored.json`.
- For each `NAME` in `anchor,control,timeout,mapping,exit` and `PHASE` in `pristine,mutated,restored`: `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/NAME/PHASE/stdout.json`, `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/NAME/PHASE/stderr.txt`, `/tmp/tameshi-r21-MT1C1Ruler-ZSgUfD/NAME/PHASE/metadata.json`. Metadata contains the complete executed argv, cwd, child exit, seconds, ruler/spec hashes, stdout/stderr hashes, control outcomes, anchor counts and semantic comparison.

Scratch paths are ephemeral; the report's tables, exact mutations, outputs, commands and full hashes are the durable result. No conclusions depend solely on unreported scratch content.

## Disagreements, defects and tooling

- **Disagreements:** none with the supplied all-surviving baseline for the three selected IDs. No conclusion about the remaining 15 IDs was drawn.
- **Coverage defects:** missing-anchor rejection, failed-pristine-control rejection and timeout classification were not protected by these successful-control observations. The two observable corruptions were the mapping inversion and wrong non-kill process status. A counter that checked counts but ignored process status would miss the exit mutant; a counter that trusted the mutated ruler's labels would mistake the mapping mutant's output for three genuine tool kills.
- **Tool behavior:** no observed tool-output/schema inconsistency required a tool issue report.
- **Available tools actually queried:** `python3 --version` → `Python 3.14.8`; `bwrap --version` → `bubblewrap 0.13.1`; `git --version` → `git version 2.56.0`; combined command exit **0**. No installations, updates or pacman transactions occurred.
- **Checks not run:** full 18-ID replay, synthetic failure/timeout fixtures, unrelated gates, builds, linters and formatters. No shipping or admission judgment is made.
