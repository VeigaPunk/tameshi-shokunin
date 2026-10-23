# CtlAlwaysPass — C1 pre-data control

## Verdict

**Rejected as expected.** The always-pass control produced `C1_R32_PASS=false`, exit **1**, with `kill=0/18 accept=8/8 other=18`. No counter bypass was observed.

**Mutation verdict: inconclusive, not killed.** The pristine revision has no audit tool and also fails the counter. Its failure cannot establish a killed mutant. The narrower assigned negative-control result is that unconditional success does not satisfy C1.

Axes: **operability**; preserved surfaces: runner bytes and frozen counter/contract bytes. No other expertise-axis move is claimed.

## Evidence and mutant

- Frozen predicate: `.ufo/evidence/round-32/contract.json:13-20`.
- Outcome decoding: `.ufo/evidence/round-32/c1-measure.py:189-194`; acceptance of the whole claim: lines 267-277.
- Mutant: add only `tools/tally-audit.py:1` in the isolated clone, unconditionally print success, ignore all arguments and runner bytes, and exit 0 by normal Python termination.
- One sandbox commit: `480669998580460d45e65ab1cce61d78636dd12e`, created directly on `c31814978969a41a8e9b0f7d99fa308c5993c1b7`. No production Git writes were performed.

Full control source (27 bytes, including the final newline):

```python
print("TALLY_AUDIT: PASS")
```

Control SHA-256: `947673c980687ba9166eff9b3689b9cc8488b64f70018dc322209fc3f3093da5`.

Expected detector: reject the control because every must-kill copy requires exit 1 and a `TALLY_AUDIT: FAIL` line, while this tool always emits `TALLY_AUDIT: PASS` with exit 0.

Observed: it got exactly the eight must-accept copies right: `B0-pristine`, `B1-T07`, `B2-reversed`, `B3-decoys`, `B4-cosmetic`, `B5-renamed`, `gB6-permuted`, `gB7-nonce`. It incorrectly accepted all 18 must-kill copies. Here `other=18` counts outcomes that do not meet their set expectation, even though those individual COPY outcomes are `ACCEPT`.

## Exact setup and sandbox commit commands

Working directory for every command: `/fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass`.

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed setup output: empty. The clone and frozen checkout completed.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlAlwaysPass
```

Observed commit output: empty. The mutation counter below reports the committed revision.

## Mutation counter: full stdout

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/w-CtlAlwaysPass
```

Fresh absent work directory; no `--seed` or counter modification.

```text
COPY set=kill id=T08 outcome=ACCEPT exit=0 sha256=12ad1d9076a55050 last='TALLY_AUDIT: PASS'
COPY set=kill id=N05 outcome=ACCEPT exit=0 sha256=e1ef181c1e621962 last='TALLY_AUDIT: PASS'
COPY set=kill id=H03 outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: PASS'
COPY set=kill id=H04 outcome=ACCEPT exit=0 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: PASS'
COPY set=kill id=H05 outcome=ACCEPT exit=0 sha256=adf6763d6524f342 last='TALLY_AUDIT: PASS'
COPY set=kill id=N01 outcome=ACCEPT exit=0 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: PASS'
COPY set=kill id=N02 outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS'
COPY set=kill id=N03 outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=D01 outcome=ACCEPT exit=0 sha256=71a66c5a611d408f last='TALLY_AUDIT: PASS'
COPY set=kill id=gT08(arm=75) outcome=ACCEPT exit=0 sha256=884e03fd46441fa6 last='TALLY_AUDIT: PASS'
COPY set=kill id=gN05(< nlegs + 0) outcome=ACCEPT exit=0 sha256=461cdc5f098398c4 last='TALLY_AUDIT: PASS'
COPY set=kill id=gH03(form=1) outcome=ACCEPT exit=0 sha256=c307192c9c04517f last='TALLY_AUDIT: PASS'
COPY set=kill id=gH04(rc=$?) outcome=ACCEPT exit=0 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: PASS'
COPY set=kill id=gH05(drop=4,dup=7) outcome=ACCEPT exit=0 sha256=7d0d53be731545b9 last='TALLY_AUDIT: PASS'
COPY set=kill id=gN01(vector=1) outcome=ACCEPT exit=0 sha256=ebf4a902638d568e last='TALLY_AUDIT: PASS'
COPY set=kill id=gN02(or) outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS'
COPY set=kill id=gN03(or) outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=gD01(drop=st_checklist,dup=st_roundgate) outcome=ACCEPT exit=0 sha256=c5c8435d058e774a last='TALLY_AUDIT: PASS'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=fb09edeed480feac last='TALLY_AUDIT: PASS'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=778f36b6d4d3ee13 last='TALLY_AUDIT: PASS'
C1_R32: kill=0/18 accept=8/8 other=18 runner_sha_ok=1 tool_present=1 seed=829c6336e5e8d197 rev=480669998580460d45e65ab1cce61d78636dd12e C1_R32_PASS=false
```

Exit code: **1**. Stderr: empty.

## Pristine counter: full stdout

Run before adding the control, at the frozen base with `tools/tally-audit.py` absent.

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/w-pristine
```

```text
COPY set=kill id=T08 outcome=OTHER exit=no-tool sha256=12ad1d9076a55050 last=''
COPY set=kill id=N05 outcome=OTHER exit=no-tool sha256=e1ef181c1e621962 last=''
COPY set=kill id=H03 outcome=OTHER exit=no-tool sha256=2ac4ce5344e6100a last=''
COPY set=kill id=H04 outcome=OTHER exit=no-tool sha256=0dc1e6b07452f610 last=''
COPY set=kill id=H05 outcome=OTHER exit=no-tool sha256=adf6763d6524f342 last=''
COPY set=kill id=N01 outcome=OTHER exit=no-tool sha256=c0a32ec4e69d3cb0 last=''
COPY set=kill id=N02 outcome=OTHER exit=no-tool sha256=31128639afc3e57a last=''
COPY set=kill id=N03 outcome=OTHER exit=no-tool sha256=741907e82ca7e907 last=''
COPY set=kill id=D01 outcome=OTHER exit=no-tool sha256=71a66c5a611d408f last=''
COPY set=kill id=gT08(arm=68) outcome=OTHER exit=no-tool sha256=c63c5fd222033890 last=''
COPY set=kill id=gN05(< nlegs) outcome=OTHER exit=no-tool sha256=e1ef181c1e621962 last=''
COPY set=kill id=gH03(form=1) outcome=OTHER exit=no-tool sha256=c307192c9c04517f last=''
COPY set=kill id=gH04(rc=$?) outcome=OTHER exit=no-tool sha256=0dc1e6b07452f610 last=''
COPY set=kill id=gH05(drop=1,dup=5) outcome=OTHER exit=no-tool sha256=ba5473fb0198e642 last=''
COPY set=kill id=gN01(vector=0) outcome=OTHER exit=no-tool sha256=71d7c5f20bfccac6 last=''
COPY set=kill id=gN02(true) outcome=OTHER exit=no-tool sha256=29d0e2b6649efed2 last=''
COPY set=kill id=gN03(split) outcome=OTHER exit=no-tool sha256=16566843890d60ab last=''
COPY set=kill id=gD01(drop=st_kagi,dup=st_roundgate) outcome=OTHER exit=no-tool sha256=00d77bd273fb03b6 last=''
COPY set=accept id=B0-pristine outcome=OTHER exit=no-tool sha256=a7d3f2dd7d47511a last=''
COPY set=accept id=B1-T07 outcome=OTHER exit=no-tool sha256=91066af826f69ecb last=''
COPY set=accept id=B2-reversed outcome=OTHER exit=no-tool sha256=7d3d5a5f34fe3595 last=''
COPY set=accept id=B3-decoys outcome=OTHER exit=no-tool sha256=7c76617e87c11c49 last=''
COPY set=accept id=B4-cosmetic outcome=OTHER exit=no-tool sha256=137a7ba8a58c5277 last=''
COPY set=accept id=B5-renamed outcome=OTHER exit=no-tool sha256=f66fe32a4ea7ce76 last=''
COPY set=accept id=gB6-permuted outcome=OTHER exit=no-tool sha256=c61b6dc8d693eb1d last=''
COPY set=accept id=gB7-nonce outcome=OTHER exit=no-tool sha256=fdc3d49964309d17 last=''
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=c8c352a765b2c4d2 rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

Exit code: **1**. Stderr: empty.

## Restoration evidence

Restoration ran in a `finally` block after the mutation detector returned. It restored the sandbox checkout to the exact original revision; the candidate commit remains available by its recorded hash.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed exit: **0**. Stdout and stderr: empty.

| Surface | Before | Mutated | Restored |
|---|---|---|---|
| `tools/tally-audit.py` | absent (no hash) | `947673c980687ba9166eff9b3689b9cc8488b64f70018dc322209fc3f3093da5` | absent (no hash) |
| `tools/mutate-and-run.sh` SHA-256 | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |

The only added working-tree path was removed by the frozen checkout. The restored detector below again reports the original revision and `tool_present=0`.

Frozen production inputs were hashed before and after the probe, without editing them:

| Input | Before SHA-256 | After SHA-256 |
|---|---|---|
| `.ufo/evidence/round-32/c1-measure.py` | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` |
| `.ufo/evidence/round-32/contract.json` | `7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583` | `7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583` |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |

## Restored counter: full stdout

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/w-restored
```

```text
COPY set=kill id=T08 outcome=OTHER exit=no-tool sha256=12ad1d9076a55050 last=''
COPY set=kill id=N05 outcome=OTHER exit=no-tool sha256=e1ef181c1e621962 last=''
COPY set=kill id=H03 outcome=OTHER exit=no-tool sha256=2ac4ce5344e6100a last=''
COPY set=kill id=H04 outcome=OTHER exit=no-tool sha256=0dc1e6b07452f610 last=''
COPY set=kill id=H05 outcome=OTHER exit=no-tool sha256=adf6763d6524f342 last=''
COPY set=kill id=N01 outcome=OTHER exit=no-tool sha256=c0a32ec4e69d3cb0 last=''
COPY set=kill id=N02 outcome=OTHER exit=no-tool sha256=31128639afc3e57a last=''
COPY set=kill id=N03 outcome=OTHER exit=no-tool sha256=741907e82ca7e907 last=''
COPY set=kill id=D01 outcome=OTHER exit=no-tool sha256=71a66c5a611d408f last=''
COPY set=kill id=gT08(arm=254) outcome=OTHER exit=no-tool sha256=2ae296ae448e7a88 last=''
COPY set=kill id=gN05(< nlegs + 0) outcome=OTHER exit=no-tool sha256=461cdc5f098398c4 last=''
COPY set=kill id=gH03(form=0) outcome=OTHER exit=no-tool sha256=2ac4ce5344e6100a last=''
COPY set=kill id=gH04(true) outcome=OTHER exit=no-tool sha256=eceff075da31e6d4 last=''
COPY set=kill id=gH05(drop=6,dup=1) outcome=OTHER exit=no-tool sha256=060bb8d9dab86478 last=''
COPY set=kill id=gN01(vector=2) outcome=OTHER exit=no-tool sha256=c0a32ec4e69d3cb0 last=''
COPY set=kill id=gN02(true) outcome=OTHER exit=no-tool sha256=29d0e2b6649efed2 last=''
COPY set=kill id=gN03(or) outcome=OTHER exit=no-tool sha256=741907e82ca7e907 last=''
COPY set=kill id=gD01(drop=st_sourcescheck,dup=st_mado) outcome=OTHER exit=no-tool sha256=800678d9ce0f091e last=''
COPY set=accept id=B0-pristine outcome=OTHER exit=no-tool sha256=a7d3f2dd7d47511a last=''
COPY set=accept id=B1-T07 outcome=OTHER exit=no-tool sha256=91066af826f69ecb last=''
COPY set=accept id=B2-reversed outcome=OTHER exit=no-tool sha256=7d3d5a5f34fe3595 last=''
COPY set=accept id=B3-decoys outcome=OTHER exit=no-tool sha256=7c76617e87c11c49 last=''
COPY set=accept id=B4-cosmetic outcome=OTHER exit=no-tool sha256=137a7ba8a58c5277 last=''
COPY set=accept id=B5-renamed outcome=OTHER exit=no-tool sha256=f66fe32a4ea7ce76 last=''
COPY set=accept id=gB6-permuted outcome=OTHER exit=no-tool sha256=dc7ec93f6233c96d last=''
COPY set=accept id=gB7-nonce outcome=OTHER exit=no-tool sha256=d8fc291156f9c471 last=''
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=dc4257f22afbe108 rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

Exit code: **1**. Stderr: empty.

All three runs used the same frozen bounded detector with fresh work directories and no seed override. Each run drew its own printed seed; the generated panels are therefore not byte-identical across phases. All observed runs are included above.

## Smallest safe correction

None to the frozen counter or contract: leave them unchanged. Keep this intentionally defective control out of production; the isolated working copy is restored. The actual audit tool must discriminate must-kill from must-accept behavior rather than return a constant result.

## Probe scope and artifacts

- Complete structured receipt: `/fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/probe.json`.
- Raw output and exit receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysPass/{pristine,mutated,restored}.{stdout,stderr,exit}`.
- A pre-run orchestration CWD assertion stopped before any counter was invoked; the harness then explicitly entered its allowed scratch directory. No counter run is omitted.
- `df -h /fast` before cloning reported 108G available (87% used). No builds or regression runs were invoked.
- No tools were installed or updated. No subagents or other agent runtime were invoked. Every started command completed; no process tree remains to kill.
