# CtlAlwaysFail — pre-data control

## Verdict

**Rejected as expected.** The always-fail control produced `C1_R32_PASS=false`, exit 1: `kill=18/18 accept=0/8 other=8 runner_sha_ok=1 tool_present=1`. It did not escape the frozen counter.

**Differential mutation verdict: inconclusive, not killed.** The pristine and restored revisions have no audit tool and already fail the detector. Their failure cannot establish a causal mutant kill. The pre-data control result itself is conclusive: an input-ignoring failure response does not satisfy C1.

Axis: **operability** (C1). No other expertise axis was measured. Runner preservation was a binding constraint.

## Evidence and expected detector

- Frozen predicate: `.ufo/evidence/round-32/contract.json:13-20`; control expectation: line 33.
- Frozen detector: `.ufo/evidence/round-32/c1-measure.py:177-196` classifies individual responses; lines 264-277 require all 18 must-kill and all 8 must-accept results plus the pinned runner and committed tool.
- Control source: `/fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/w-CtlAlwaysFail/tool/tally-audit.py:1-2`, exported by the counter from sandbox commit `ed8263d9ee75face2414bbd78369138da4953bcc`. The identical source was written to `/fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/tally-audit.py` and committed once on top of `c31814978969a41a8e9b0f7d99fa308c5993c1b7`.
- Control receipt: `/fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/control.stdout:1-27`; exit receipt: `/fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/control.exit:1`; `control.stderr` is empty. Pristine and restored receipts use the same directory and the `pristine` and `restored` prefixes.

The control returns the expected response on every must-kill copy, including all nine generated families, solely because it always fails. It returns the wrong response on all eight must-accept copies: B0-pristine, B1-T07, B2-reversed, B3-decoys, B4-cosmetic, B5-renamed, gB6-permuted, and gB7-nonce. Per-copy `outcome=KILL` on these acceptable copies is the counter's response classification; those eight mismatches contribute to aggregate `other=8`, not `accept`.

### Complete control source

```python
print("TALLY_AUDIT: FAIL")
raise SystemExit(1)
```

This is a two-line, 47-byte tool. It neither reads arguments nor opens the runner.

### Setup and the single sandbox commit

All commands ran from `/fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail` after creating that directory with `os.makedirs(path, exist_ok=True)` and selecting it with `os.chdir(path)`. Disk check before cloning: `df -h /fast` reported 114G available (86% used).

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed setup output: empty. The control file was created using the file-writing tool, followed by:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlAlwaysFail && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane rev-parse HEAD
```

Observed output:

```text
ed8263d9ee75face2414bbd78369138da4953bcc
```

### Detector runs — full stdout verbatim

The same bounded, unchanged detector ran against pristine, control, and restored committed bytes. Each invocation used a fresh work directory, default job count, and no `--seed`. The independent random seeds are recorded in the unedited outputs below. These are the only three counter runs in this probe.

#### Pristine

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/w-pristine
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
COPY set=kill id=gT08(arm=99) outcome=OTHER exit=no-tool sha256=c4e2f61b9af3c246 last=''
COPY set=kill id=gN05(< nlegs) outcome=OTHER exit=no-tool sha256=e1ef181c1e621962 last=''
COPY set=kill id=gH03(form=0) outcome=OTHER exit=no-tool sha256=2ac4ce5344e6100a last=''
COPY set=kill id=gH04(rc=$?) outcome=OTHER exit=no-tool sha256=0dc1e6b07452f610 last=''
COPY set=kill id=gH05(drop=6,dup=4) outcome=OTHER exit=no-tool sha256=0cb528a3bb3836fc last=''
COPY set=kill id=gN01(vector=2) outcome=OTHER exit=no-tool sha256=c0a32ec4e69d3cb0 last=''
COPY set=kill id=gN02(true) outcome=OTHER exit=no-tool sha256=29d0e2b6649efed2 last=''
COPY set=kill id=gN03(split) outcome=OTHER exit=no-tool sha256=16566843890d60ab last=''
COPY set=kill id=gD01(drop=st_checklist,dup=st_roundgate) outcome=OTHER exit=no-tool sha256=c5c8435d058e774a last=''
COPY set=accept id=B0-pristine outcome=OTHER exit=no-tool sha256=a7d3f2dd7d47511a last=''
COPY set=accept id=B1-T07 outcome=OTHER exit=no-tool sha256=91066af826f69ecb last=''
COPY set=accept id=B2-reversed outcome=OTHER exit=no-tool sha256=7d3d5a5f34fe3595 last=''
COPY set=accept id=B3-decoys outcome=OTHER exit=no-tool sha256=7c76617e87c11c49 last=''
COPY set=accept id=B4-cosmetic outcome=OTHER exit=no-tool sha256=137a7ba8a58c5277 last=''
COPY set=accept id=B5-renamed outcome=OTHER exit=no-tool sha256=f66fe32a4ea7ce76 last=''
COPY set=accept id=gB6-permuted outcome=OTHER exit=no-tool sha256=62cb5c3683f30e99 last=''
COPY set=accept id=gB7-nonce outcome=OTHER exit=no-tool sha256=896e674ae74fc0c7 last=''
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=83bc3df21bcbb011 rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty.

#### Always-fail control

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/w-CtlAlwaysFail
```

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gT08(arm=169) outcome=KILL exit=1 sha256=ed1747d453f003ac last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH03(form=0) outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH04(rc=$?) outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=3,dup=5) outcome=KILL exit=1 sha256=0e52b974929facb3 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN01(vector=0) outcome=KILL exit=1 sha256=71d7c5f20bfccac6 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(true) outcome=KILL exit=1 sha256=29d0e2b6649efed2 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(or) outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gD01(drop=st_sourcescheck,dup=st_claims) outcome=KILL exit=1 sha256=8d762e5454abaaa4 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B0-pristine outcome=KILL exit=1 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: FAIL'
COPY set=accept id=B1-T07 outcome=KILL exit=1 sha256=91066af826f69ecb last='TALLY_AUDIT: FAIL'
COPY set=accept id=B2-reversed outcome=KILL exit=1 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B3-decoys outcome=KILL exit=1 sha256=7c76617e87c11c49 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B4-cosmetic outcome=KILL exit=1 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B5-renamed outcome=KILL exit=1 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB6-permuted outcome=KILL exit=1 sha256=1560c594688d94ec last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB7-nonce outcome=KILL exit=1 sha256=1fc63c8ccc69c1cc last='TALLY_AUDIT: FAIL'
C1_R32: kill=18/18 accept=0/8 other=8 runner_sha_ok=1 tool_present=1 seed=93122c09d3406c84 rev=ed8263d9ee75face2414bbd78369138da4953bcc C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty.

#### Restored

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/w-restored
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
COPY set=kill id=gT08(arm=37) outcome=OTHER exit=no-tool sha256=f0a40ef9d2bc9cb2 last=''
COPY set=kill id=gN05(<= nlegs - 1) outcome=OTHER exit=no-tool sha256=7184b157539cad8c last=''
COPY set=kill id=gH03(form=2) outcome=OTHER exit=no-tool sha256=7f1787411f0ff16c last=''
COPY set=kill id=gH04(true) outcome=OTHER exit=no-tool sha256=eceff075da31e6d4 last=''
COPY set=kill id=gH05(drop=0,dup=2) outcome=OTHER exit=no-tool sha256=45d9362b5c0544a8 last=''
COPY set=kill id=gN01(vector=2) outcome=OTHER exit=no-tool sha256=c0a32ec4e69d3cb0 last=''
COPY set=kill id=gN02(true) outcome=OTHER exit=no-tool sha256=29d0e2b6649efed2 last=''
COPY set=kill id=gN03(or) outcome=OTHER exit=no-tool sha256=741907e82ca7e907 last=''
COPY set=kill id=gD01(drop=st_mado,dup=st_sourcescheck) outcome=OTHER exit=no-tool sha256=30613205a72b566a last=''
COPY set=accept id=B0-pristine outcome=OTHER exit=no-tool sha256=a7d3f2dd7d47511a last=''
COPY set=accept id=B1-T07 outcome=OTHER exit=no-tool sha256=91066af826f69ecb last=''
COPY set=accept id=B2-reversed outcome=OTHER exit=no-tool sha256=7d3d5a5f34fe3595 last=''
COPY set=accept id=B3-decoys outcome=OTHER exit=no-tool sha256=7c76617e87c11c49 last=''
COPY set=accept id=B4-cosmetic outcome=OTHER exit=no-tool sha256=137a7ba8a58c5277 last=''
COPY set=accept id=B5-renamed outcome=OTHER exit=no-tool sha256=f66fe32a4ea7ce76 last=''
COPY set=accept id=gB6-permuted outcome=OTHER exit=no-tool sha256=eb835d27d712b419 last=''
COPY set=accept id=gB7-nonce outcome=OTHER exit=no-tool sha256=8570eb550f2daba6 last=''
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=2aa6bda755cef96d rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty.

## Restoration evidence and hashes

The original audit-tool state was **absent**, not an empty file. After the control run, the sandbox commit was retained on branch `CtlAlwaysFail`, and the scratch checkout was restored to the frozen base. No second commit was made.

Exact restoration command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane branch CtlAlwaysFail ed8263d9ee75face2414bbd78369138da4953bcc && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane rev-parse HEAD HEAD^{tree} refs/heads/CtlAlwaysFail^{tree}
```

Observed output:

```text
c31814978969a41a8e9b0f7d99fa308c5993c1b7
2dc56d3a5ab11b1c07f72caa22ac726ed5c7f6d4
6646f2d07d1c1cb5089117c7cd49647a53280fae
```

The pristine/restored committed tree is `2dc56d3a5ab11b1c07f72caa22ac726ed5c7f6d4`; the control tree is `6646f2d07d1c1cb5089117c7cd49647a53280fae` (Git tree object IDs). After restoration, the explicit path-presence observation was `RESTORATION tool_path_exists=false`. The restored counter again observed `tool_present=0` and the same base revision.

SHA-256 evidence:

| Surface | Pristine | Control | Restored |
|---|---|---|---|
| `tools/tally-audit.py` | absent; no file hash | `6241dd6a1654272146e00f1b6d5bd055b73a80e679cd9daa52bc0bfb9b37c156` | absent; no file hash |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same SHA-256 | same SHA-256 |
| Frozen counter | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` | same SHA-256 | same SHA-256 |
| Frozen contract | `7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583` | same SHA-256 | same SHA-256 |

Exact pre-control hash command and observed output:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/mutate-and-run.sh
```

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/mutate-and-run.sh
```

Exact control-state hash command and observed output:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/tally-audit.py /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/mutate-and-run.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

```text
6241dd6a1654272146e00f1b6d5bd055b73a80e679cd9daa52bc0bfb9b37c156  /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/tally-audit.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

Exact restored-state hash command and observed output:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/mutate-and-run.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/w-CtlAlwaysFail/tool/tally-audit.py
```

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/lane/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
6241dd6a1654272146e00f1b6d5bd055b73a80e679cd9daa52bc0bfb9b37c156  /fast/scratch/hyaku/tameshi-r32-seats/CtlAlwaysFail/w-CtlAlwaysFail/tool/tally-audit.py
```

The counter-exported control remains available at its evidence path, and its hash matches the committed control source. Every subprocess invocation completed; no long-lived service was started and no process kill was needed. No production source, frozen counter, contract, or sibling scratch copy was edited. Only this report was written outside the assigned scratch directory. No tool was installed or updated.

## Smallest safe correction

None to the frozen detector: it already rejects this control. Keep the counter and predicate unchanged. The real audit implementation must distinguish acceptable from faulty runner behavior; unconditional failure cannot supply that capability. The scratch checkout has already been restored to its original bytes, while the one control commit and exact receipts remain available for inspection.
