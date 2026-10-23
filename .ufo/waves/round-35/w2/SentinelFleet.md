# Round 35 w2 — SentinelFleet

Axes: fleet-root boundary integrity; artifact provenance; command-execution exposure.

## Verdict

**CRITICAL: none. BOUND: none demonstrated. HYGIENE: one conditional command-execution surface and one scratch-path collision.** No Tameshi lane report or other lane-authored artifact was found at the fleet root. The only Tameshi-named root status entry is driver state: `.ufo/state/tameshi.report-baseline`.

## Fleet-root status and classification

Command `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` exited **0**. The captured status bytes are `/fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/fleet-root-status.txt`, SHA-256 `7b78be92d9ddafdc1aa80c3c55ea220511e5d76e491d3df454b0d9e90d90a037`; `wc -l` on that capture exited **0** and reported **31** entries.

Classification evidence: fleet-root `AGENTS.md` SHA-256 `382f28ab4e2846a94e176f67b5ea93d6c6a347997778a10ddc4c78772886eb86`; its lines 76–81 identify `.ufo/state/` and `.ufo/watchdog.log` as driver runtime and `scripts/` as operator-side. The 16 remaining untracked ambient files below are classified **driver/ambient [INFERENCE]** by location/content; porcelain alone does not prove their human or process author. No entry is evidenced as lane-authored or other-lane-authored.

- **Driver state (directly classified by the root policy; 15 entries):**
  - ` M .ufo/state/chousa.report-baseline`
  - ` M .ufo/state/kagi.report-baseline`
  - ` M .ufo/state/kaidoku.report-baseline`
  - ` M .ufo/state/kake.report-baseline`
  - ` M .ufo/state/kama.report-baseline`
  - ` M .ufo/state/kengaku.report-baseline`
  - ` M .ufo/state/kumitate.report-baseline`
  - ` M .ufo/state/mado.report-baseline`
  - ` M .ufo/state/mori.report-baseline`
  - ` M .ufo/state/tameshi.report-baseline`
  - ` M .ufo/state/tsukuroi.report-baseline`
  - ` M .ufo/watchdog.log`
  - `?? .ufo/state/kotoba.report-baseline`
  - `?? .ufo/state/kotodama.report-baseline`
  - `?? .ufo/state/revenger.report-baseline`

  The Tameshi baseline bytes hash to `ed9951ef052a6e0fa4703bc182b8aabc9f96877046c1e9bd9f09f80771115b88`; it is a modified driver baseline, not a lane report.

- **Driver/ambient [INFERENCE] (16 entries; no lane authorship evidence):**
  - `?? .omp/mcp.json`
  - `?? 0`
  - `?? AGENTS.md`
  - `?? bm.json`
  - `?? live.html`
  - `?? live_s228.html`
  - `?? nama.html`
  - `?? s395.txt`
  - `?? scripts/hyaku/__pycache__/append-closure.cpython-314.pyc`
  - `?? scripts/hyaku/__pycache__/wave-live.cpython-314.pyc`
  - `?? scripts/hyaku/append-closure.py.bak-20261023T040735Z`
  - `?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z`
  - `?? tf_bavelas.html`
  - `?? wb2.html`
  - `?? write`
  - `?? xc.xml`

## Finding

**HYGIENE — untracked MCP configuration is a conditional execution surface.** `.omp/mcp.json` is status `??`, SHA-256 `3439a008a7e682813f88ac8ff5e0390813fec8c9a4cf9106f11ee382ee396a74`, mode `0644` (`stat -c '%a %U:%G %n' ...` exited 0). Static `read` query `paths(scalars) as $p | {path:$p, value:(getpath($p) as $v | if ($v|tostring|test("(?i)(token|secret|password|api[_-]?key|credential)")) then "<REDACTED>" else $v end)}` returned `mcpServers.rea` as `stdio`, command `npx`, args `-y rea-agents@6.7.0 mcp`; no inspected scalar matched those credential patterns (a static read has no process exit code). **Exploit path:** a client that loads this fleet-root config would launch the specified package as its user. This inspection does not establish that any client loaded it, and I did not invoke it or another runtime. **Impact:** conditional local code execution through the configured MCP process. **Smallest remediation:** require an explicit trust/approval decision for this untracked config (or use an approved, locally pinned executable). No remediation was in scope or applied.

## Misroot check and setup evidence

The exact requested setup attempt (exit **128**) was:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane checkout -q --detach 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
```

Git reported that the destination already existed and was not empty. The pre-existing checkout was left untouched. Its read-only identity/status command exited **0**:

```sh
git -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane rev-parse HEAD && git -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane status --porcelain --untracked-files=all && sha256sum /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane/tools/tally-audit-v3.py /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane/.ufo/evidence/round-35/c1/c1-measure.py /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane/.ufo/evidence/round-35/c2/c2-measure.py
```

It reported HEAD `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` and empty porcelain status; that is not the requested pin. I cloned to the separate scratch path `lane-target`. The exact clone/checkout command exited **0**:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane-target && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane-target checkout -q --detach 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
```

The exact verification command exited **0**, reporting HEAD `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` and empty status:

```sh
git -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane-target rev-parse HEAD && git -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane-target status --porcelain --untracked-files=all && sha256sum /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane-target/tools/tally-audit-v3.py /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane-target/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane-target/.ufo/evidence/round-35/c1/c1-measure.py /fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/lane-target/.ufo/evidence/round-35/c2/c2-measure.py
```

The pin-check hashes are:


- `tools/tally-audit-v3.py`: `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`
- `tools/mutate-and-run.sh`: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
- `.ufo/evidence/round-35/c1/c1-measure.py`: `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`
- `.ufo/evidence/round-35/c2/c2-measure.py`: `67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc`

`test ! -e /home/vgpnk/Projects/shokunin/.ufo/waves/round-35 && printf 'ABSENT: /home/vgpnk/Projects/shokunin/.ufo/waves/round-35\n'` exited **0**: the fleet-root round-35 wave path is absent. The fleet-root round-34 `w1/` directory was read and was empty. Thus there is no fleet-root `w2/SentinelFleet.md` or other current Tameshi wave report at the root. The `Report:` destination is inside the Tameshi lane, not the fleet root.

This seat created no files at the fleet root; all scratch evidence and the usable checkout are under `/fast/scratch/hyaku/tameshi-r35-seats/SentinelFleet/`. No package/tool was installed, no runtime was invoked, and no lane artifact was modified except this assigned report.

Report: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SentinelFleet.md`
