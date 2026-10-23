# Read12C — cold read of SKILL.md section at line 1964 (rev 9f3084bc)

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read12C", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1964, "heading": "### Round-21 gate/probe registry — finite environment differential", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
    "Variant invocations not executed this read: round21-measure --claim c2 (the section itself documents it reads live fleet object stores via hard-coded FLEET, so its fresh exit is environment-dependent), coldread measure.py --repo --rev --explain (reads the L1-mutable coldread ledger; selftest covers the override refusals), wave-route-mix on the refusing spec1/wrong spec and registry-replay --project/--run/--plan entries. Each row's named self-invocation plus the two env-diff entry forms and the c1 facade entry were executed.",
    "The persisted receipt `.ufo/evidence/round-21/f5/receipt.json` is byte-identical to `f5/receipt-final-production.json` (same sha256); the section's singular pointer is accurate but two other receipt files (receipt-initial.json, receipt-supersession.json) sit alongside it.",
    "A second cold-run of the c1 facade under the trace collector yielded killed=16 survived=0 inconclusive=2 (pristine-control-not-green on the two trace-inputs mutants) vs an earlier identical clone run at killed=18/18: fresh re-measurement is host-timing-sensitive, consistent with the section's own 'bounded measurements' warning and its exit map (receipt exit 1 = failed population)."
  ],
  "commands_executed": [
    "python3 tools/env-diff.py --selftest",
    "python3 tools/wave-route-mix.py --selftest",
    "python3 tools/wave-accounting.py --selftest",
    "python3 tools/command-binding.py --selftest",
    "python3 tools/registry-replay.py --selftest",
    "python3 tools/round21-measure.py --selftest",
    "python3 .ufo/evidence/round-21/coldread/measure.py --selftest",
    "python3 -c \"import sys; [print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-21.md corpus/knowledge/hermetic-env-differential.md corpus/knowledge/callback-authoritative-accounting.md corpus/knowledge/required-command-binding.md corpus/knowledge/replay-projection-hardening.md corpus/QUALITY.md corpus/lessons/round-24.md",
    "python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/wrong-count-bundle.json --expected .ufo/evidence/round-22/wrong-count-expected.json --json",
    "python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/Read12C-keFe/scratch/tameshi-f5-b.json",
    "python3 tools/command-binding.py --bundle .ufo/evidence/round-22/wrong-count-bundle.json --expected .ufo/evidence/round-22/wrong-count-expected.json --json",
    "python3 tools/round21-measure.py --claim c1 --repo /tmp/Read12C-keFe/fleet/tameshi-shokunin --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --json"
  ],
  "opened": [
    "corpus/SOURCES.md", "corpus/QUALITY.md",
    "corpus/lessons/round-21.md", "corpus/lessons/round-24.md",
    "corpus/knowledge/hermetic-env-differential.md", "corpus/knowledge/callback-authoritative-accounting.md",
    "corpus/knowledge/required-command-binding.md", "corpus/knowledge/replay-projection-hardening.md",
    "tools/env-diff.py", "tools/wave-route-mix.py", "tools/round21-measure.py", "tools/wave-accounting.py",
    "tools/command-binding.py", "tools/registry-replay.py",
    ".ufo/evidence/round-18/measure.py",
    ".ufo/evidence/round-21/c1-survivors.py", ".ufo/evidence/round-21/c2-count.py", ".ufo/evidence/round-21/c2-contract.json",
    ".ufo/evidence/round-21/c1-mutants.json", ".ufo/evidence/round-21/coldread/measure.py",
    ".ufo/evidence/round-21/f5/receipt.json", ".ufo/evidence/round-21/f5/receipt-initial.json",
    ".ufo/evidence/round-21/f5/receipt-final-production.json", ".ufo/evidence/round-21/f5/receipt-supersession.json",
    ".ufo/evidence/round-21/final/registry.json", ".ufo/evidence/round-21/final/registry.stdout",
    ".ufo/evidence/round-21/final/registry.stderr", ".ufo/evidence/round-21/final/invariants.json",
    ".ufo/evidence/round-21/final/invariants-D.json", ".ufo/evidence/round-21/final/monitor-current.json",
    ".ufo/evidence/round-22/measure.py", ".ufo/evidence/round-22/accounting-extra-cases.json",
    ".ufo/evidence/round-22/wrong-count-bundle.json", ".ufo/evidence/round-22/wrong-count-expected.json",
    ".ufo/evidence/round-23/extra-cases.json",
    ".ufo/evidence/round-23/replay/bundle.json", ".ufo/evidence/round-23/replay/observations.json", ".ufo/evidence/round-23/replay/expected.json",
    ".ufo/evidence/round-24/measure.py", ".ufo/evidence/round-24/extra-cases.json",
    ".ufo/evidence/round-24/replay/bundle.json", ".ufo/evidence/round-24/replay/observations.json",
    ".ufo/evidence/round-24/replay/expected.json", ".ufo/evidence/round-24/replay/live-dependent.json",
    ".ufo/evidence/round-24/source-prefix-preservation.json", ".ufo/evidence/round-24/source-prefix-preservation-B.json",
    ".ufo/evidence/round-24/source-prefix-preservation-C.json",
    ".ufo/evidence/round-25/source-refresh-receipts.json",
    ".ufo/evidence/round-26/after/registry-40a12bf.json", ".ufo/evidence/round-27/after/registry-2227d83.json",
    ".ufo/waves/round-21/routemix-spec1.json"
  ],
  "inputs": {
    "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
    "corpus/QUALITY.md": "069ef729b7738927585f487afa3c26b4912b9d568cb9f0c69b00c3f172538e07",
    "corpus/lessons/round-21.md": "35444ddc32116089f87733c8f0a635dc7b452407d2bd0f47de483e8aacfb1a7d",
    "corpus/lessons/round-24.md": "29fd3e00a79242536bc259f6d56d6473e5e0d1e5bf451413c061fb6094b7d7a6",
    "corpus/knowledge/hermetic-env-differential.md": "90756351093e2273257ce6a738bb90b6923865bc22d9276ba2cf8aeafb262e7e",
    "corpus/knowledge/callback-authoritative-accounting.md": "ddf13b0835a5e6c21c308ab87ec24c9d8eee8bb8af3b3b254d73b554e9cf6035",
    "corpus/knowledge/required-command-binding.md": "2e72f8a04017b6d16e67ebd8e9e8bdb5d45b70701030a3f5466b187369ab4fd6",
    "corpus/knowledge/replay-projection-hardening.md": "7602943988d8c7a2ce566b810b28d98c01938c565244be2503bee295d76520f4",
    "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
    "tools/wave-route-mix.py": "1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782",
    "tools/round21-measure.py": "eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d",
    "tools/wave-accounting.py": "96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e",
    "tools/command-binding.py": "9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d",
    "tools/registry-replay.py": "9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714",
    ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
    ".ufo/evidence/round-21/c1-survivors.py": "a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396",
    ".ufo/evidence/round-21/c1-mutants.json": "670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c",
    ".ufo/evidence/round-21/c2-count.py": "9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2",
    ".ufo/evidence/round-21/c2-contract.json": "5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd",
    ".ufo/evidence/round-21/coldread/measure.py": "657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb",
    ".ufo/evidence/round-21/f5/receipt.json": "9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264",
    ".ufo/evidence/round-21/f5/receipt-initial.json": "909811037578ac32359ca72daad10ed48c5c18852c9ecb7efafd499ec2cdde19",
    ".ufo/evidence/round-21/f5/receipt-final-production.json": "9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264",
    ".ufo/evidence/round-21/f5/receipt-supersession.json": "2cee3c82165a265673c9396899f8d507a83a3f4e98969c8c2f606824beeb4c2a",
    ".ufo/evidence/round-21/final/registry.json": "3641db57dc5894f2ff7c55c952411ca69278d21fb9cbe3a712573cb1f8deb26a",
    ".ufo/evidence/round-21/final/registry.stdout": "cda2e7645cbecfdf356bd35cfa47507c56618a7a9785298bc3f7e2a161454bdf",
    ".ufo/evidence/round-21/final/registry.stderr": "3f1ec3fa5413685738c394345811f0d26ecca04cf2404c7a2989b097e76e04fd",
    ".ufo/evidence/round-21/final/invariants.json": "ffc92b663d2ec18e0244f0a43537bbd43a1ebc964410839566311fdb38bc36f7",
    ".ufo/evidence/round-21/final/invariants-D.json": "7a089d9348708e086af7cf6fd33fe52bac53f0fd0871d6b05c1ba9d8f19054d6",
    ".ufo/evidence/round-21/final/monitor-current.json": "fd39b344af60cfae11dceb3c4fdd8d98dfae28eadce5112a2ce8f11bf108b469",
    ".ufo/evidence/round-22/measure.py": "f833d067afd3ca17b8534fc942d6e8ed529edd3d55476802c18ea631c0678056",
    ".ufo/evidence/round-22/accounting-extra-cases.json": "e60807f2154164638b13709af930760d0f16c2c8c4a2dee7297a490c5338a41f",
    ".ufo/evidence/round-22/wrong-count-bundle.json": "d984c49c57d2b12b3a4e2583cc33842af6927f0612b3b0d663acb2ca09a7a17e",
    ".ufo/evidence/round-22/wrong-count-expected.json": "caf7d29e0fea8e8492152d3798201069452019928d6dd58ba052d98e6d0ad0ec",
    ".ufo/evidence/round-23/extra-cases.json": "87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00",
    ".ufo/evidence/round-23/replay/bundle.json": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9",
    ".ufo/evidence/round-23/replay/observations.json": "a83d8a0b53b6b51a6e2d445da5b99fd843586051b743908e43eff6ba947cfa16",
    ".ufo/evidence/round-23/replay/expected.json": "0831c9c820488dc9d9096c90aade44217b6b615501fae7810e6fce414cb2a0a1",
    ".ufo/evidence/round-24/measure.py": "0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64",
    ".ufo/evidence/round-24/extra-cases.json": "6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35",
    ".ufo/evidence/round-24/replay/bundle.json": "4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6",
    ".ufo/evidence/round-24/replay/observations.json": "2d9b1b77349bf148095a80bfd7ef9c98f8584b7a0c7c261a0d406896a69a7a88",
    ".ufo/evidence/round-24/replay/expected.json": "8fc9342ed1f07beb0e930f7a46fb0081a825e35494f43608ea5c2396f13b0868",
    ".ufo/evidence/round-24/replay/live-dependent.json": "c3a5f9133f6f90a2da337873b26b4bae9b09a397b7a1abdaeee6ce003b9a4ef3",
    ".ufo/evidence/round-24/source-prefix-preservation.json": "5dacb75adb5c13b3bb0d876c7878a2d61e572ba7ef9b4a1c7fac59185a0b4a2e",
    ".ufo/evidence/round-24/source-prefix-preservation-B.json": "b816953ba28b143f653b86f6134e9cdd094d6d67b24d18734c7fe91063efae88",
    ".ufo/evidence/round-24/source-prefix-preservation-C.json": "7dfb2dc10fcc4a4727fc0950be412d0f9ef3d1c9c7a6d439d93aadf043dcbfa4",
    ".ufo/evidence/round-25/source-refresh-receipts.json": "ab34b04e9f10dd8749ccb8e8b73e1bf4d902ca45ed226946a476ab21f5224435",
    ".ufo/evidence/round-26/after/registry-40a12bf.json": "9e8bf4b10b837c8a765710ab80a5c56ca4c13bc99ae518323b83605f218f26af",
    ".ufo/evidence/round-27/after/registry-2227d83.json": "db8371976aa519686c7429d88560580d5089dae8be93f55b4c35750970d5130c",
    ".ufo/waves/round-21/routemix-spec1.json": "92c1edb3fdf53ac45bb6d324c16d94b388c26960aceee53f74f6883af1b97d56"
  },
  "external_inputs": {
    "tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:.ufo/evidence/round-21/coldread/ledger.json": "c5b3a3496d6799d163e5902931a24fd857dbb04454e6f9b7b483e71dd6cf385f",
    "tameshi-shokunin@33d03b716d3edcf1d8656d46d6df61801d232c52:corpus/SOURCES.md": "9715f44dca8dfc2beac94b17e19f0f0206b1efa4d973eb1183650a0f9179794f",
    "/tmp/Read12C-keFe/scratch/tameshi-f5.json": "f0a7b35e48f6b3181f80bad839d696d2dcbd25104325f3acd59e208c70236e64",
    "/tmp/Read12C-keFe/scratch/tameshi-f5-b.json": "1d7aab014b1e37afd5dafdfb8251123e11f585f79de27d65281fd55d9b5b86bf"
  },
  "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-6.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-7.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-8.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-9.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-10.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-11.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12C-12.json"
  ]}]}
```

I classed the section as `instruction`: its tables name Entry and Self-invocation commands for every instrument, and the appended round-28 correction explicitly tells a cold reader to substitute its own clone for `--repo`. Every named command I ran behaved per the section's verdict map, and the prose claims I opened all checked out at 9f3084bc:

- `env-diff.py --selftest` → ENVDIFF_SELFTEST: 9/9 (matches the persisted "9/9" and the "sensitivity, repeat variation and pin refusal" fixture wording: cases invariant/tz/locale/home/columns/repeat/missing-bwrap/timeout/pin-mismatch-public-cli).
- `env-diff.py --contract c2-contract.json --out ...` → `ENVDIFF: classified=9/9`, exit 0; fresh receipt reproduces 8 invariant + 1 nondeterministic (js-round-gate), matching the frozen `f5/receipt.json` and the "nine classified does not mean nine deterministic" caveat.
- `wave-route-mix.py --selftest` → 8/8; `wave-accounting.py --selftest` → 8/8 + 16/16 extra (matches "eight literal public-CLI rejection fixtures" + "16 further guards"); `command-binding.py --selftest` → 44/44 (matches "command-binding-selftest-r24 (44/44)"); `registry-replay.py --selftest` → 10/10 (matches "expects 10/10"); `round21-measure.py --selftest` → 13/13; coldread `measure.py --selftest` → 12/12 incl. eight SELECTOR_OVERRIDE refusals (matches "selftest 0 clean").
- `wave-accounting` on the wrong-count pair → receipt exit 1 with finding TOTAL_MISMATCH (claimed 40/35 vs observed 38/37), matching "persisted expected verdict is 1/TOTAL_MISMATCH". `command-binding` on the same pair → exit 2 INVALID_EXPECTED, matching "2 invalid/unavailable/tampered".
- `round21-measure.py --claim c1 --repo <clone> --rev 9f3084b --json` → 18 KILLED, exit 0 first run (the two inconclusive on the collector-wrapped second run are recorded as a minor gap, not a section defect).
- "unchanged from 33d03b7" verified: c1-survivors.py, c2-count.py, c2-contract.json, wave-route-mix.py are byte-identical blobs at 33d03b7 and HEAD; the other four tools were created after the freeze (added later — the diff is additive for those, which the section's wording allows).
- Round-28 correction line-pins verified byte-for-byte: c2-count.py line 19 `FLEET = Path("/home/vgpnk/Projects/shokunin")`, line 52 `show(FLEET / frozen["repo"], ...)`; wave-route-mix reads `~/.omp/agent/config.yml`; routemix-spec1.json has `ok: true`.
- 43-receipt replay population verified in both round-23 and round-24 replay dirs; `live-dependent.json` lists exactly `pin-disposition-read` and `verify-round15`, `revision_pinned=41`. "49 active rows from round 26 on" verified: 56 rows − 7 `superseded_by` at the round-26 and round-27 registries.
- "199-entry prefix" verified: coldread ledger (read via `git show` per the exception) records `round21_provenance.prefix_retained=199`, `source_read_entries=34`; lessons/round-21.md's "retains its 199-entry prefix" statement matches.
- QUALITY43–48 exist with the cited subjects (route-mix falsifier on the round20 spec; re-anchor rule; callback binding; command-binding; narrowings; frozen predicate rule).
- The S024-driven SOURCES.md drift flagged by the monitor does not touch this section's claims: its sources are S079/S028/S081/S082/S083/S084/S085, all still consistent at this revision.

No tooling installs or updates were needed. Scratch lived only in /tmp/Read12C-keFe; the clone stayed detached at the pinned rev.

COLDREAD Read12C: executed-ok
