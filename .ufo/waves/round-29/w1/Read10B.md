# Read10B — cold read of "### Round-18 gate/probe registry — routed-defect closure" (SKILL.md lines 1925–1937 @ 9f3084bc)

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read10B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1925, "heading": "### Round-18 gate/probe registry — routed-defect closure", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [], "commands_executed": [
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-18/defect-probes.py tools/registry-check.py tools/evidence-disposition.py tools/bash-witness-study.py tools/trace-inputs.py .ufo/evidence/round-18/measure.py .ufo/evidence/round-18/coldread/assemble.py .ufo/evidence/round-18/coldread/measure.py .ufo/evidence/round-19/measure.py .ufo/evidence/round-19/coldread/measure.py .ufo/evidence/round-18/dispositions.json .ufo/waves/round-18/w2/SentinelKillCode.md corpus/lessons/round-18.md corpus/QUALITY.md corpus/SOURCES.md .ufo/evidence/round-18/coldread/ledger.json .ufo/evidence/round-19/contract.json .ufo/evidence/round-18/c2-probes-183f87b.txt",
    "python3 -c \"import sys;[print(p, len(open(p).read()[:200000])) for p in sys.argv[1:]]\" .ufo/evidence/round-18/coldread/assemble.py .ufo/evidence/round-18/coldread/ledger.json .ufo/evidence/round-19/measure.py .ufo/evidence/round-19/coldread/measure.py .ufo/evidence/round-19/contract.json .ufo/evidence/round-19/before.json .ufo/evidence/round-19/after-21e7932.json .ufo/evidence/round-17/coldread/trace-inputs.py corpus/QUALITY.md corpus/SOURCES.md corpus/lessons/round-19.md corpus/lessons/round-18.md .ufo/evidence/round-18/dispositions.json .ufo/waves/round-18/w2/SentinelKillCode.md"],
  "opened": [
    ".ufo/evidence/round-13/verification.json",
    ".ufo/evidence/round-14/dispositions.json",
    ".ufo/evidence/round-17/coldread/trace-inputs.py",
    ".ufo/evidence/round-17/coldread/traces/CR41/23-appendix-manifests.json",
    ".ufo/evidence/round-17/dispositions.json",
    ".ufo/evidence/round-17/dispositions-before.json",
    ".ufo/evidence/round-18/coldread/assemble.py",
    ".ufo/evidence/round-18/coldread/ledger.json",
    ".ufo/evidence/round-18/defect-probes.py",
    ".ufo/evidence/round-18/dispositions-before.json",
    ".ufo/evidence/round-18/dispositions.json",
    ".ufo/evidence/round-18/final/audit-1814.stdout",
    ".ufo/evidence/round-18/final/audit-1925.stdout",
    ".ufo/evidence/round-18/final/bash-witness-selftest.stderr",
    ".ufo/evidence/round-18/final/before.stdout",
    ".ufo/evidence/round-18/measure.py",
    ".ufo/evidence/round-19/after-21e7932.json",
    ".ufo/evidence/round-19/before.json",
    ".ufo/evidence/round-19/coldread/measure.py",
    ".ufo/evidence/round-19/contract.json",
    ".ufo/evidence/round-19/measure.py",
    ".ufo/evidence/round-21/coldread/measure.py",
    ".ufo/evidence/round-21/f5/receipt.json",
    ".ufo/waves/round-18/w2/SentinelKillCode.md",
    "corpus/QUALITY.md",
    "corpus/SOURCES.md",
    "corpus/lessons/round-18.md",
    "corpus/lessons/round-19-verifier-spotcheck.md",
    "corpus/lessons/round-19.md",
    "tools/bash-witness-study.py",
    "tools/env-diff.py",
    "tools/evidence-disposition.py",
    "tools/registry-check.py",
    "tools/trace-inputs.py"],
  "inputs": {
    ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
    ".ufo/evidence/round-17/coldread/trace-inputs.py": "521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070",
    ".ufo/evidence/round-17/coldread/traces/CR41/23-appendix-manifests.json": "06b425c42175f3f1492ea1bd4a20643514e52bf603b17ad854f74e249650b782",
    ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
    ".ufo/evidence/round-17/dispositions-before.json": "79f0b397b727152b260df90e3ba9aa886d20eb7b5e5a43f6c3d03c7d3ee32354",
    ".ufo/evidence/round-18/coldread/assemble.py": "bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a",
    ".ufo/evidence/round-18/coldread/ledger.json": "d654f3d2755c6c7b35a000acfc4e37ff14d0d576c98321c75771c87b65185939",
    ".ufo/evidence/round-18/defect-probes.py": "99297d9645151dee948291638386f3e9189c7bab590bebda23de6e51dadebeaa",
    ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
    ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
    ".ufo/evidence/round-18/final/audit-1814.stdout": "e5f76ad4dc91f6bb1d10053f6abbc9f0573e61cdb31f612618ef6b3e33930937",
    ".ufo/evidence/round-18/final/audit-1925.stdout": "c1ee0c85c7b33720b307334a61e36f2925b77b64f12563109459fdcc060eda2b",
    ".ufo/evidence/round-18/final/bash-witness-selftest.stderr": "6a192f7b98c44ed542761b9c38d889ab41202f835385e493c596f546dc287d66",
    ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
    ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
    ".ufo/evidence/round-19/after-21e7932.json": "ef7a957c6cd3fb04c8e23b5779d083c934ffd550ddd819cf3efe801495df127a",
    ".ufo/evidence/round-19/before.json": "55c8fa309ac0d74ffafb59c8f8cfb331cc116e1f5cc274b536d7dc393b62c95f",
    ".ufo/evidence/round-19/coldread/measure.py": "4c9c74ca3bb0d85121d6bd3e4deeafe4474374d0a67becf9a9c9fe4c0d42f2f7",
    ".ufo/evidence/round-19/contract.json": "4a7de023f0dd45031d8b9020c66a247f6ee4855eb11e4d04319f630d61867ccc",
    ".ufo/evidence/round-19/measure.py": "7af3e951bf67f7671954dee33aaa4dc183a642fce85cbc2d9d782085f856cf72",
    ".ufo/evidence/round-21/coldread/measure.py": "657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb",
    ".ufo/evidence/round-21/f5/receipt.json": "9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264",
    ".ufo/waves/round-18/w2/SentinelKillCode.md": "5b521c18271805bcaf7d69edadcbd4d78c3f42e6c656fa812239048f80e7ebb0",
    "corpus/QUALITY.md": "069ef729b7738927585f487afa3c26b4912b9d568cb9f0c69b00c3f172538e07",
    "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
    "corpus/lessons/round-18.md": "88b17f6df3290cf61d886bab322add21e863177003e1725df4f928c44b7d3159",
    "corpus/lessons/round-19-verifier-spotcheck.md": "cb3d96a6f24f10524e3f3303a2b5e4fed2f3fbd8d6ae0b4e677262e51c720a43",
    "corpus/lessons/round-19.md": "3517626e2e3c35b06ded28c9858642143ef925a016ea95d0472d4f0dac22a595",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
    "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
    "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"},
  "external_inputs": {
    "tameshi-shokunin@4acc607dfd79f19d508bd50cdd06b77269fccd1d:tools/bash-witness-study.py": "49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80",
    "https://docs.python.org/3/library/os.html": "2ac87dd3ac1f30a3210cb1631c5bd41f3708f100cbeeb2b5874ea4b29e17d993",
    "https://docs.python.org/3.10/library/os.html": "ee0cc58a9dadb846f0563e8d22a23e9246cb3e31bc54d62da9986cf19145383c"},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10B-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10B-2.json"]}]}
```

Section is lines 1925–1937 (the next `###` heading sits at 1938; no fences inside). It is an eight-row registry of instrument names, kinds, entry CLIs and exit/rule texts — a `record` of pointers, not an instruction directed at this reader.

What I checked (all in the detached clone at 9f3084bc):

- Row 1929 (defect-probes.py): docstring gives `DEFECT_PROBES: open=N closed=M total=N`, `PROBE_IDS` is `P01..P11` (total=11 ✓), `status = "open" if mutant_proc.returncode == 0 else "closed"` and pristine≠0 → `ProbeError` → exit 2; non-unique anchor → `ProbeError` → 2 (selftest `reject-nonunique-anchor`); children run under `bwrap --ro-bind / / ...` with the fleet ro-bound; P05–P07 have `path=None` → `trace_tool(root)` selects the collector, so wrapping this probe in `trace-inputs.py` would nest ptrace → could-not-evaluate → 2. ✓
- Row 1930 (registry-check.py): `MAX_TIMEOUT_S = 86400`, `math.isfinite(ts) and 0 < ts <= MAX_TIMEOUT_S`, `json.loads(..., parse_constant=_reject_json_constant)` refuses `NaN`/`Infinity` at parse → "registry invalid … non-finite JSON number" → exit 2; selftest expects `proc.returncode == 2` with the row name and `timeout_s` in the error line. `_cleanup_row` kills descendants after `communicate` (timeout path and normal path), bounded `_bounded_communicate` drain, `held = got == expected_exit and not missing and cleanup_ok` (survivors → `cleanup_error`). The stated limits match SentinelKillCode.md (adopted-orphan signalling, same-tick PID reuse) and the file's own contract lines 39–44. The historical `communicate()` overflow crash is a "used to" claim — today overflow values are refused with exit 2 (consistent). ✓
- Row 1931 (evidence-disposition.py): `resolve_historical_anchor` — `refs/heads/` + `lane.branch`; unbound jj workspace → `CouldNotEvaluate` → 2; detached non-jj uses HEAD only when `for-each-ref --contains` on `refs/heads/ refs/remotes/` finds a branch/remote-tracking ref; `--selftest` fixtures invoke `jj` directly (`["jj"] + argv`, jj branch-tip cases) → jj required on PATH. ✓
- Row 1932 (bash-witness-study.py): `{k:v for k,v in os.environ.items() if not k.startswith("GIT_")}` plus `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` at :336–338 ✓. "Pinned round-13 bytes read from `4acc607` through `.ufo/evidence/round-18/dispositions.json`": the document pins `tools/bash-witness-study.py` at rev `4acc607dfd…` and `git show 4acc607:tools/bash-witness-study.py` hashes to `49e9e5e2…`, matching both the dispositions reason text and `round-13/verification.json`'s `measured_input_sha256`. "(round-17 manifests are superseded)": `evidence-disposition.py` calls these documents "manifests", the round-17 document lacks the witness pin and exists in both variants, and SKILL.md:1850 states "the round-17 manifest now exits 2". ✓
- Row 1933 (trace-inputs.py): promoted `tools/` copy (sha f59c9312…) vs historical `.ufo/evidence/round-17/coldread/` copy (sha 521be955…) — present and not byte-identical ✓; P05–P07 mutation targets are exactly the O_RDWR exclusion (`WRITE_FLAGS_RE`:82), private-cache anchoring (`PYTHONPYCACHEPREFIX`:516) and root-execve check (:644). ✓
- Row 1934 (measure.py, coldread/assemble.py): `DEFAULT_LEDGER_PATH = '.ufo/evidence/round-18/coldread/ledger.json'` ✓; `--carry`/`carried_from`/`--explain` implemented (assemble selftest exercises verbatim carry + `carried_from` key; measure.py `--explain` reports per-section end/reasons) ✓; credit is input-keyed (report inputs union/receipt inputs, never commands) — consistent with the "input-keyed credit only" wording. ✓
- Row 1935 (round-19 measure.py): `return int(args.check and corrected != 5)` — without `--check` exit 0 always (a count, not acceptance) ✓; five rows from `contract.json` population (5 items, verified) ✓; `SOURCE_PINS` binds `source-baseline.txt`/`source-round18-final.txt` ✓; selftest uses inline synthetic snapshots + four frozen package fixtures (:245 comment) ✓; `before.json`/`after-*.json` exist as measured outputs and are not selftest inputs ✓; QUALITY37–39 exist in `corpus/QUALITY.md:334/344/352`, `lessonround19` exists, `S049` exists in `corpus/SOURCES.md:58` (listed as used-by round-19). ✓
- Row 1936 (round-19 coldread measure.py): `IMPLEMENTATION = ROOT/'.ufo/evidence/round-18/measure.py'`, `LEDGER = '.ufo/evidence/round-19/coldread/ledger.json'`, no legacy-override handling in the selector ✓; input hashes keyed on `read_rev` (revision-pinned) ✓; selftest writes only under `/tmp` temp dirs ✓.

The Python docs fetches (external, https://docs.python.org/…) were used to sanity-check `os.open` flag semantics mentioned in passing while studying; they had no bearing on the verdict. No blocking gaps, no wrong expectations; "manifests" plural for the two round-17 disposition documents is loose but accurate in substance.

COLDREAD Read10B: verified-record
