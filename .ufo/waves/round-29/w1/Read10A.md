# Read10A — cold read, SKILL.md §1925 "### Round-18 gate/probe registry — routed-defect closure"

Verdict: `gap-minor`. Class: `record` (a registry table of facts with pointers; it
prescribes a lane convention in one row but nothing is asked of the reader). Eight
rows checked against the cited code, fixtures and ledgers at
9f3084bc60ad56aac01e4556ef4c7653df2f65e5; every checkable claim held.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read10A", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1925, "heading": "### Round-18 gate/probe registry \u2014 routed-defect closure", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": ["defect-probes --rev REV was not executed end-to-end (fresh clone plus eleven bwrap probes exceeds the 6-minute cap), so the row's 'nested ptrace is refused -> 2' prediction for wrapping it in tools/trace-inputs.py is verified in code only (P05-P07 GUARD_SPECS mutate the collector at defect-probes.py:82-102 and run its selftest; the collector requires strace and exits 2 when the trace cannot be set up, tools/trace-inputs.py:44-54); the tool's own --selftest does not run the probes and passes under the collector (receipt Read10A-6.json)"],
  "commands_executed": [
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/registry-check.py tools/evidence-disposition.py tools/bash-witness-study.py tools/trace-inputs.py .ufo/evidence/round-18/defect-probes.py .ufo/evidence/round-18/measure.py .ufo/evidence/round-18/coldread/assemble.py .ufo/evidence/round-18/dispositions.json",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-2.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-19/measure.py .ufo/evidence/round-19/coldread/measure.py .ufo/evidence/round-19/contract.json .ufo/evidence/round-18/coldread/ledger.json .ufo/waves/round-18/w2/SentinelKillCode.md .ufo/evidence/round-19/digest-units.json",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-3.json -- python3 .ufo/evidence/round-19/coldread/measure.py --selftest",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-4.json -- python3 tools/evidence-disposition.py --selftest",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-5.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/registry.json .ufo/evidence/round-19/coldread/ledger.json",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-6.json -- python3 .ufo/evidence/round-18/defect-probes.py --selftest",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-7.json -- python3 tools/registry-check.py --selftest",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-8.json -- python3 .ufo/evidence/round-19/measure.py --selftest",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-9.json -- python3 .ufo/evidence/round-18/measure.py --selftest",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-10.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/QUALITY.md corpus/lessons/round-19.md corpus/SOURCES.md",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-11.json -- sh -c 'python3 .ufo/evidence/round-19/measure.py --bogus-flag; echo \"EXIT_A=$?\"; python3 .ufo/evidence/round-19/measure.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --snapshot /tmp/x.json; echo \"EXIT_B=$?\"; python3 .ufo/evidence/round-19/measure.py --selftest --check; echo \"EXIT_C=$?\"'",
    "python3 tools/trace-inputs.py --root $R --out $T/Read10A-12.json -- python3 -c <two-argument subprocess probe printing exit codes>"
  ],
  "opened": ["tools/registry-check.py", "tools/evidence-disposition.py", "tools/bash-witness-study.py", "tools/trace-inputs.py", "tools/registry.json", ".ufo/evidence/round-18/defect-probes.py", ".ufo/evidence/round-18/measure.py", ".ufo/evidence/round-18/coldread/assemble.py", ".ufo/evidence/round-18/dispositions.json", ".ufo/evidence/round-18/coldread/ledger.json", ".ufo/evidence/round-17/coldread/trace-inputs.py", ".ufo/evidence/round-19/measure.py", ".ufo/evidence/round-19/coldread/measure.py", ".ufo/evidence/round-19/contract.json", ".ufo/evidence/round-19/digest-units.json", ".ufo/evidence/round-19/coldread/ledger.json", ".ufo/evidence/round-19/checks-baseline.json", ".ufo/evidence/round-19/probes-baseline.txt", ".ufo/evidence/round-19/source-baseline.txt", ".ufo/evidence/round-19/source-round18-final.txt", ".ufo/waves/round-18/w2/SentinelKillCode.md", "corpus/QUALITY.md", "corpus/lessons/round-19.md", "corpus/SOURCES.md"],
  "inputs": {
    "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
    "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
    ".ufo/evidence/round-18/defect-probes.py": "99297d9645151dee948291638386f3e9189c7bab590bebda23de6e51dadebeaa",
    ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
    ".ufo/evidence/round-18/coldread/assemble.py": "bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a",
    ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
    ".ufo/evidence/round-18/coldread/ledger.json": "d654f3d2755c6c7b35a000acfc4e37ff14d0d576c98321c75771c87b65185939",
    ".ufo/evidence/round-17/coldread/trace-inputs.py": "521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070",
    ".ufo/evidence/round-19/measure.py": "7af3e951bf67f7671954dee33aaa4dc183a642fce85cbc2d9d782085f856cf72",
    ".ufo/evidence/round-19/coldread/measure.py": "4c9c74ca3bb0d85121d6bd3e4deeafe4474374d0a67becf9a9c9fe4c0d42f2f7",
    ".ufo/evidence/round-19/contract.json": "4a7de023f0dd45031d8b9020c66a247f6ee4855eb11e4d04319f630d61867ccc",
    ".ufo/evidence/round-19/digest-units.json": "0a18ef642bddc97dc9c16415c131cf92f67f99dc5b12e98ba9a8ab9c2389a835",
    ".ufo/evidence/round-19/coldread/ledger.json": "1ba190e5f34dcaf8a38540b48cb2d80835f2f7a656b175f08996077a2b105c02",
    ".ufo/evidence/round-19/checks-baseline.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
    ".ufo/evidence/round-19/probes-baseline.txt": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
    ".ufo/evidence/round-19/source-baseline.txt": "ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5",
    ".ufo/evidence/round-19/source-round18-final.txt": "018ee9a86500efc6d07ea141d20c7de6b2ec76e5e808ffbf12508ada46a84e0e",
    ".ufo/waves/round-18/w2/SentinelKillCode.md": "5b521c18271805bcaf7d69edadcbd4d78c3f42e6c656fa812239048f80e7ebb0",
    "corpus/QUALITY.md": "069ef729b7738927585f487afa3c26b4912b9d568cb9f0c69b00c3f172538e07",
    "corpus/lessons/round-19.md": "3517626e2e3c35b06ded28c9858642143ef925a016ea95d0472d4f0dac22a595",
    "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca"
  },
  "external_inputs": {
    "tameshi@4acc607dfd79f19d508bd50cdd06b77269fccd1d:tools/bash-witness-study.py": "49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80"
  },
  "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-6.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-7.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-8.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-9.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-10.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-11.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read10A-12.json"
  ]}]}
```

What I checked, row by row:

- **defect-probes.py**: `PROBE_IDS` is `P%02d` over `range(1, 12)` — eleven probes, so `total=11` in the trailer matches `defect-probes.py:44` and the printer at `:956`. A guard is `closed` only when the pristine selftest exits 0 and the mutant exits nonzero (`:383-392`); anchor uniqueness is enforced (`:259-260`, `:370-372`); `UsageParser.error` exits 64 (`:110-113`). Children run under the bwrap envelope (`:191-195`), bwrap 0.13.1 confirmed on the host. `SELFTEST: PASS (6 cases)`, exit 0, receipt Read10A-6.json. The `--rev` probe run itself was not executed (over the 6-minute cap); the never-wrap-in-trace-inputs rationale is code-verified (P05-P07 specs mutate the collector's O_RDWR/pycache/execve guards at `:82-102`).
- **registry-check.py**: `MAX_TIMEOUT_S = 86400` with the `communicate()` overflow rationale (`:104-107`); `NaN`/`Infinity` literals rejected at JSON parse via `parse_constant` with the row named by `_nonfinite_location`; finite check `math.isfinite(ts) and 0 < ts <= MAX_TIMEOUT_S`; descendant cleanup via child subreaper + pidfd start-time/ownership revalidation, called on the timeout path and after row exit (`:692-732`), `cleanup_error` on survivors; bounded pipe drain (`PIPE_DRAIN_TIMEOUT_S`). Selftest `SELFTEST: PASS (51 cases)` including `timeout-nan`, `timeout-infinity`, `timeout-kills-setsid-pipe`, `timeout-kills-setpgid-pipe`, `bounded-pipe-drain` — receipt Read10A-7.json. The stated limits (UID change, same-tick PID reuse, adopted orphans) match `.ufo/waves/round-18/w2/SentinelKillCode.md` findings 1-2 and the tool's own docstring.
- **evidence-disposition.py**: anchor resolution reads `lane.branch`, else attached `refs/heads/<branch>` (`:461-490`); an unbound jj workspace is refused (`:494-496`); a detached non-jj clone anchors on HEAD only when a `refs/heads/` or `refs/remotes/` ref contains it (`:503-525`); jj fixtures move HEAD while the bookmark stays (`@-`, `:2185`). `--selftest` does need `jj` on PATH — it is at `~/.local/bin/jj` and the 66-case selftest passed under the collector including `v2-jj-prebookmark-branch-tip`, `v2-jj-without-lane-branch`, `v2-registry-clone-detached-anchor`, `v2-detached-no-published-ref` (receipt Read10A-4.json).
- **bash-witness-study.py**: every git child drops inherited `GIT_*` and pins `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` (`:336-338`, selftest `:1284-1297`). `dispositions.json` `historical_inputs` pins `tools/bash-witness-study.py` to `4acc607dfd79f19d508bd50cdd06b77269fccd1d`; `git show 4acc607:tools/bash-witness-study.py | sha256sum` gives `49e9e5e2…` — exactly the round-13 pinned bytes. The round-17 dispositions are indeed superseded in `tools/registry.json` (`evidence-disposition-round17*` → `superseded_by: evidence-disposition-round18*`).
- **trace-inputs.py**: the promoted collector (`f59c9312…`) differs byte-wise from the frozen round-17 evidence copy (`521be955…`, sha taken by hand and cross-checked against round-17 ledger records). `tools/registry.json` supersedes `trace-inputs-round17-selftest` with `trace-inputs-selftest`. The promoted selftest checks `rdwr-open-excluded`, `pycache-prefix-private` and root-`execve` — the three guards P05-P07 mutate.
- **round-18 measure.py + assemble.py**: `--explain` emits per-section `end` and sorted `reasons` (`section_record`, `:540-546`, exercised in `explain-section-shape`); the default ledger sits next to each script (round-18 `coldread/ledger.json` read; `DROPPED_INPUT_KEYS` confirms the canonical path); `--carry` copies entries verbatim plus `carried_from` (`:979-981`, carry selftest). `MEASURE_SELFTEST: 98/98 pass` (receipt Read10A-9.json). The input-keyed-only bound is literal in the reasons the ruler emits (`inputs-unrecorded`, `commands-unrecorded`, `verdict-class:*` cases all observed in the run).
- **round-19 measure.py**: docstring exit map 0/1/2/64 verified live — `--bogus-flag` and `--rev`+`--snapshot` both exit 64 through `Parser.error → self.exit(64)` (`:395-397`, receipt Read10A-12.json; an untracked bad `--rev` exits 2). `SELFTEST: 43/43` (receipt Read10A-8.json). `SOURCE_PINS` binds `source-baseline.txt`/`source-round18-final.txt`, and the receipt captured exactly four package fixtures (`probes-baseline.txt`, `checks-baseline.json`, `source-baseline.txt`, `source-round18-final.txt`) with hashes matching the pins. `contract.json` describes the five-item population verbatim (R18-1…R18-5); the selftest builds synthetic snapshots and never reads the contract or the before/after receipts. QUALITY 37–39 exist (`corpus/QUALITY.md:334-352`), `corpus/lessons/round-19.md` exists, S049 is a live row.
- **round-19 coldread/measure.py**: delegates to frozen `.ufo/evidence/round-18/measure.py` via `importlib` (`:18-21`), selects `.ufo/evidence/round-19/coldread/ledger.json` (`:22`); `SELECTOR_SELFTEST: 3/3 pass` (receipt Read10A-3.json). The ledger mixes `carried_from` round-17 entries with round-19 L1-author source reads — matching the "L1-author source reads, not new cold-read/command-coverage evidence" bound.

Single minor gap: the `defect-probes --rev REV` measurement run (and hence the nested-ptrace → 2 prediction) was not executed; the mechanism is verified in code but not end-to-end within the 6-minute cap.

COLDREAD Read10A: gap-minor
