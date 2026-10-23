# ColdA09 — wave C cold reads (sections 25, 26, 27)

Lane rev `bb681566b18211adf8ae9c28df91e17678e3f545`, SKILL.md sha256
`c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6` (verified in
clone). Clone: `/tmp/ColdA09-qdk6/fleet/tameshi-shokunin`, detached at the read
rev, fleet-mirror layout with sibling `*-shokunin` symlinks.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdA09", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
 "sections": [
 {"start": 1846, "heading": "### Round-17 gate/probe registry — re-pin and monitor", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [],
  "commands_executed": [
   "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json (exit 0; status clean)",
   "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json (exit 2; could_not_evaluate)",
   "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json (exit 2; could_not_evaluate)",
   "timeout 260 bash tools/mutate-and-run.sh --selftest (exit 0; MUTATE_SELFTEST: 106/106 pass, VERDICT: PASS)"],
  "opened": ["SKILL.md", "tools/evidence-disposition.py", "tools/registry-check.py", "tools/mutate-and-run.sh", "tools/pin-disposition.py", "tools/bash-witness-study.py", "tools/witness-metadata.py", ".ufo/evidence/round-18/dispositions.json", ".ufo/evidence/round-17/dispositions.json", ".ufo/evidence/round-17/dispositions-before.json", ".ufo/evidence/round-14/dispositions.json", ".ufo/evidence/round-14/dispositions-before.json", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/producer-before.py", ".ufo/evidence/round-13/producer-oracle.py", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-13/verification.json", ".ufo/evidence/round-13/witness-metadata.json", ".ufo/evidence/round-13/witness-metadata-old-null.json", ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/summary.json", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json"],
  "inputs": {
   ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
   ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
   ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
   ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
   ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
   ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
   ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
   ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
   ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
   ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
   ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
   ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
   ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
   ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
   ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
   ".ufo/evidence/round-17/dispositions-before.json": "79f0b397b727152b260df90e3ba9aa886d20eb7b5e5a43f6c3d03c7d3ee32354",
   ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
   "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
   "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
   "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
   "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
   "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
   "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"},
  "external_inputs": {},
  "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA09-25-1.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA09-25-2.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA09-25-3.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA09-25-4.json"]},
 {"start": 1905, "heading": "## Eighth recorded case — round 18", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [],
  "commands_executed": [
   "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-18/sources-check/suite.txt .ufo/evidence/round-18/sources-check/predictions.json .ufo/evidence/round-18/sources-check/sources-check.defects.spec .ufo/evidence/round-18/sources-check/control.txt .ufo/evidence/round-18/sources-check/control/hazard-summary.md .ufo/evidence/round-18/sources-check/control/strace-summary.md corpus/knowledge/mutation-case-kumitate-sources-check.md tools/mutate-and-run.sh (exit 0)"],
  "opened": ["SKILL.md", ".ufo/evidence/round-18/sources-check/suite.txt", ".ufo/evidence/round-18/sources-check/predictions.json", ".ufo/evidence/round-18/sources-check/sources-check.defects.spec", ".ufo/evidence/round-18/sources-check/control.txt", ".ufo/evidence/round-18/sources-check/control/hazard-summary.md", ".ufo/evidence/round-18/sources-check/control/strace-summary.md", ".ufo/evidence/round-18/sources-check/control/repeat-hashes.json", "corpus/knowledge/mutation-case-kumitate-sources-check.md", "tools/mutate-and-run.sh"],
  "inputs": {
   ".ufo/evidence/round-18/sources-check/control.txt": "74061bdf3d1f6bfe5a066c5c454678ae8647d2c5d123f6d4bea182093158d1a0",
   ".ufo/evidence/round-18/sources-check/control/hazard-summary.md": "8b93c3eb94463ce33160fb2f91d5453cc6d60546c9b2f540f86a2c6c535a7185",
   ".ufo/evidence/round-18/sources-check/control/repeat-hashes.json": "79d94d2756a9639cd2999c741af200f16237969a11e8869d4106b79e7bf6bb37",
   ".ufo/evidence/round-18/sources-check/control/strace-summary.md": "6ecfbdbfd1395bcc99b3d81f91afd75ab841d7e8b4506a0c6c8bc201aaac6950",
   ".ufo/evidence/round-18/sources-check/predictions.json": "5749a27a92c862278a2c77307496f2b80b3c6619c6125def0ea0066b7252d35f",
   ".ufo/evidence/round-18/sources-check/sources-check.defects.spec": "c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91",
   ".ufo/evidence/round-18/sources-check/suite.txt": "6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b",
   "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38",
   "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"},
  "external_inputs": {
   "kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs": "6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f",
   "tameshi-shokunin@93d22aa21a144a0e2833b1be74718d15060f002b:.ufo/evidence/round-18/sources-check/sources-check.defects.spec": "c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91",
   "tameshi-shokunin@93d22aa21a144a0e2833b1be74718d15060f002b:.ufo/evidence/round-18/sources-check/predictions.json": "5749a27a92c862278a2c77307496f2b80b3c6619c6125def0ea0066b7252d35f"},
  "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA09-26-1.json"]},
 {"start": 1925, "heading": "### Round-18 gate/probe registry — routed-defect closure", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [],
  "commands_executed": [
   "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-18/defect-probes.py .ufo/evidence/round-18/measure.py .ufo/evidence/round-18/coldread/assemble.py .ufo/evidence/round-18/dispositions.json .ufo/evidence/round-19/measure.py .ufo/evidence/round-19/coldread/measure.py .ufo/evidence/round-17/coldread/trace-inputs.py .ufo/waves/round-18/w2/SentinelKillCode.md tools/trace-inputs.py tools/registry-check.py tools/evidence-disposition.py tools/bash-witness-study.py tools/mutate-and-run.sh tools/registry.json (exit 0)"],
  "opened": ["SKILL.md", ".ufo/evidence/round-18/defect-probes.py", ".ufo/evidence/round-18/measure.py", ".ufo/evidence/round-18/coldread/assemble.py", ".ufo/evidence/round-18/dispositions.json", ".ufo/evidence/round-19/measure.py", ".ufo/evidence/round-19/coldread/measure.py", ".ufo/evidence/round-17/coldread/trace-inputs.py", ".ufo/waves/round-18/w2/SentinelKillCode.md", "tools/trace-inputs.py", "tools/registry-check.py", "tools/evidence-disposition.py", "tools/bash-witness-study.py", "tools/mutate-and-run.sh", "tools/registry.json"],
  "inputs": {
   ".ufo/evidence/round-17/coldread/trace-inputs.py": "521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070",
   ".ufo/evidence/round-18/coldread/assemble.py": "bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a",
   ".ufo/evidence/round-18/defect-probes.py": "99297d9645151dee948291638386f3e9189c7bab590bebda23de6e51dadebeaa",
   ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
   ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
   ".ufo/evidence/round-19/coldread/measure.py": "4c9c74ca3bb0d85121d6bd3e4deeafe4474374d0a67becf9a9c9fe4c0d42f2f7",
   ".ufo/evidence/round-19/measure.py": "7af3e951bf67f7671954dee33aaa4dc183a642fce85cbc2d9d782085f856cf72",
   ".ufo/waves/round-18/w2/SentinelKillCode.md": "5b521c18271805bcaf7d69edadcbd4d78c3f42e6c656fa812239048f80e7ebb0",
   "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
   "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
   "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
   "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
   "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
   "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"},
  "external_inputs": {},
  "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA09-27-1.json"]}]}
```

## What I checked

All three sections are `record` class — they state registry rows and case facts
with pointers; the commands are cited rows, not imperatives to a reader.

**Section 25 (lines 1846–1854).** All four rows' tools exist at the read rev.
Ran `tools/evidence-disposition.py` as written: the round-18
`dispositions.json` manifest exits 0 with `status: clean` (receipt
ColdA09-25-1, tool sha `39ee5c5e…`); both round-17 manifests
(`dispositions.json`, `dispositions-before.json`) exit 2 with
`status: could_not_evaluate`, exactly as the row claims ("the round-17 manifest
now exits 2"). Ran `bash tools/mutate-and-run.sh --selftest`: exit 0,
`MUTATE_SELFTEST: 106/106 pass`, `VERDICT: PASS` (receipt 25-4). The
`.ufo/evidence/round-13/pin-manifest.json` cited by the `pin-disposition.py`
row exists (opened by the disposition run itself, sha `64eaa43e…`), and
`pin-disposition.py` exists at sha `331529ea…`. `registry-check.py` accepts the
documented `--rev`/`--registry`/`--tag`/`--json`/`--selftest` CLI (usage block
at :118). Not exercised: `registry-check.py --rev` (clones the lane and
replays every registry row — exceeds my box under fleet load) and
`pin-disposition.py` against `--root /home/vgpnk/Projects/shokunin` (the cited
form would open the live lane inside the trace; the probe is a record row, so
I verified its inputs rather than run it pointed at the live fleet).

**Section 26 (lines 1905–1924).** Sibling pin verified by git-object reads:
`kumitate-shokunin@0acb7752…:scripts/sources-check.mjs` is mode 100755, 897
lines, blob sha256 `6a293a72…` — all three numbers exact (recorded as
external_input). `tools/mutate-and-run.sh` carries the `js-sources-check` leg
(:1421) pinned to that rev/sha with the documented 5/10 kill expectation and
the hermetic `env -i` suite — the suite string matches `suite.txt` byte for
byte (`sha256=6e550d5a…`, and `predictions.json.suite_sha256` agrees). The
pre-registration commit `93d22aa21a144a…` ("C1 pre-registration —
js-sources-check 10-defect spec +
predictions (before any mutant run)") adds spec + predictions + suite +
control.txt; the spec bytes at that rev hash to `c8d24cb4…` ==
`predictions.json.spec_sha256` == the current lane blob — committed before
the mutant runs at `183f87b`. Predictions: 10 defects, five K_ predicted
KILLED / five S_ predicted SURVIVED — matching "5/10 killed, 10/10
predictions held" (knowledge entry §2 headline identical). "Eight pristine
controls byte-identical" is `control/repeat-hashes.json`: runs=8,
`all_exits_zero`, `distinct_stdout_sha256=1`. The SKILL.md survivor table
has four rows covering all five S_ survivors (S_KIND; S_VERDICT; S_DUP_LINE
and S_ENTRY_COUNT share one row; S_FILE_READ), "fix belongs to kumitate" on
each — consistent with the entry's ER8-2 probe table ("four are
non-equivalent, S_KIND differs only in --help output"). `--regression`
replay: attempted twice under the collector (ColdA09-26-2); both were killed
by my own timeout at 300s and 560s — under wave-C fleet saturation the
nine-leg replay could not finish inside my box, so no receipt exists and the
run is not listed in commands_executed. Before each kill every completed leg
printed `REGRESSION_CASE <leg>: PASS` with `flips=0` and `killed` matching
the recorded table, including the `REGRESSION_EXPECT` line
`js-sources-check=5/10`; this is a timeout of my own choosing, not a runner
failure.

**Section 27 (lines 1925–1937).** Every cited path exists at the read rev.
`defect-probes.py` defines exactly P01–P11 (total=11), prints
`DEFECT_PROBES: open= closed= total=`, launches children under bwrap with a
read-only fleet envelope, and P05–P07 do touch `tools/trace-inputs.py` plus
the historical round-17 copy (:336–364) — the "never wrap it" warning is
consistent. `registry-check.py` enforces finite `timeout_s` in (0, 86400]
(`MAX_TIMEOUT_S = 86400`, `math.isfinite` check, NaN/Infinity/negative
fixture cases) and emits `cleanup_error` for escaped children — matching the
row's claimed bounds. `evidence-disposition.py` docstring confirms the
`lane.branch`/attached-branch anchor, the jj-colocated + detached-HEAD → 2
rule, and that its selftest needs `jj` on PATH. `bash-witness-study.py`
scrubs inherited `GIT_*` and sets `GIT_CONFIG_GLOBAL=/dev/null` +
`GIT_CONFIG_NOSYSTEM=1` (:336–338). Promoted `tools/trace-inputs.py` differs
from the historical round-17 copy (`cmp` exits 1) — "not byte-identical" as
claimed. `round-18/coldread/assemble.py` implements `--carry` with
`carried_from`. `round-19/measure.py` carries `SOURCE_PINS` and invokes the
frozen `.ufo/evidence/round-18/measure.py`; `round-19/coldread/measure.py`
delegates to it selecting the round-19 ledger. `.ufo/waves/round-18/w2/
SentinelKillCode.md` exists. Not exercised: `defect-probes.py --selftest`
(bwrap + ptrace selftests, heavy under load).

Residual risk: none beyond the unexercised long-running commands noted above.
No blocking gaps, no wrong expectations found in any section. Tooling: none
installed (python3/node/strace/bash already present).
COLDREAD ColdA09: verified-record, verified-record, verified-record
