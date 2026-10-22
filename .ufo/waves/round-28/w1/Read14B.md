# Read14B: cold read of the round-21 gate/probe registry (SKILL.md:1964-2102)

Verdict: gap-minor. The section is a record: every falsifiable claim I checked held, including
the Round-28 correction's headline (c2-count.py reads the live lane through a hardcoded FLEET, so
--claim c2 is not hermetic from a clone). A handful of soft claims were not independently executed
(full 47/49-row battery, the coldread measure.py selftest, and ledger-content claims that sit in
an L1-appended file).

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read14B",
  "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6",
  "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [
    {
      "start": 1964,
      "heading": "### Round-21 gate/probe registry — finite environment differential",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Verified but not re-executed: 'The superseded 38/38 row still runs, fails against 44/44' — I confirmed the superseded row expects 'COMMAND_BINDING_SELFTEST: 38/38 pass' while the tool prints 44/44 (receipt 6), and registry.json shows it status=superseded, but I did not run tools/registry-check.py over the full registry, so 'still runs' is inferred, not observed.",
        "'(49 active rows from round 26 on; seat Read37)' — the round-26 snapshot registry-40a12bf.json does show 49 active / 7 superseded, and tools/registry.json at b05d2ee likewise; the parenthetical seat attribution was not checked.",
        "'Current source re-anchors retain the199-entry prefix' — corpus/lessons/round-21.md states it twice, but the ledger file that would carry the count (.ufo/evidence/round-21/coldread/ledger.json) is an L1-appended path I am forbidden to use, so the number rests on the lesson's word.",
        "'.ufo/evidence/round-21/coldread/measure.py ... selftest0 clean/1 failed' — the --selftest flag exists and its override-refusal cases are visible in source; the selftest was not executed.",
        "Qualitative hedge rows ('C1's guard kills include child-environment/command-pin contracts and synthetic process identities') — c1-mutants.json carries only mutant ids (MB03..R02); the characterization was not independently re-derived.",
        "'the replay verdict tests only exit and stdout' — consistent with the retained bundle (receipt keys argv/cwd/exit/revision/stdout/stderr and the gate's exit-0 result), but the stderr field's exact role was not probed."
      ],
      "commands_executed": [
        "python3 /tmp/Read14B-uA48/check.py",
        "python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/wrong-count-bundle.json --expected .ufo/evidence/round-22/wrong-count-expected.json --json",
        "python3 tools/command-binding.py --bundle .ufo/evidence/round-23/source-read-bundle.json --expected .ufo/evidence/round-23/source-read-expected.json --json",
        "python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json",
        "python3 tools/wave-accounting.py --selftest",
        "python3 tools/command-binding.py --selftest",
        "python3 tools/registry-replay.py --selftest",
        "python3 tools/wave-route-mix.py --spec .ufo/waves/round-21/spec1.json --json",
        "python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/Read14B-uA48/envdiff-out.json --jobs 3",
        "python3 /tmp/Read14B-uA48/check2.py",
        "python3 tools/env-diff.py --selftest",
        "python3 -c \"import sys\nfor p in sys.argv[1:]:\n    d=open(p).read()\n    print(p, len(d))\" .ufo/evidence/round-27/coldread/traces/ReRead03-1.json .ufo/evidence/round-26/after/registry-40a12bf.json corpus/lessons/round-23.md corpus/lessons/round-22.md corpus/knowledge/hermetic-env-differential.md corpus/knowledge/callback-authoritative-accounting.md corpus/knowledge/required-command-binding.md corpus/knowledge/replay-projection-hardening.md .ufo/evidence/round-21/routemix-r20-spec1.json .ufo/evidence/round-21/c1-mutants.json .ufo/evidence/round-23/requirements.json .ufo/evidence/round-23/registry-baseline.json .ufo/evidence/round-24/replay/bundle.json .ufo/evidence/round-24/replay/observations.json .ufo/evidence/round-22/bundle.json .ufo/evidence/round-23/source-refresh-plan.json .ufo/evidence/round-22/source-refresh-entries.json .ufo/evidence/round-23/source-prefix-preservation.json .ufo/evidence/round-24/source-prefix-preservation.json .ufo/evidence/round-24/noharm-c8c5b88.json .ufo/evidence/round-21/coldread/ledger.json",
        "python3 -c \"import sys\nfor p in sys.argv[1:]:\n    d=open(p).read()\n    print(p, len(d))\" .ufo/evidence/round-27/coldread/traces/ReRead03-1.json .ufo/evidence/round-26/after/registry-40a12bf.json corpus/lessons/round-23.md corpus/lessons/round-22.md corpus/knowledge/hermetic-env-differential.md corpus/knowledge/callback-authoritative-accounting.md corpus/knowledge/required-command-binding.md corpus/knowledge/replay-projection-hardening.md .ufo/evidence/round-21/routemix-r20-spec1.json .ufo/evidence/round-21/c1-mutants.json .ufo/evidence/round-23/requirements.json .ufo/evidence/round-23/registry-baseline.json .ufo/evidence/round-24/replay/bundle.json .ufo/evidence/round-24/replay/observations.json .ufo/evidence/round-22/bundle.json .ufo/evidence/round-23/source-refresh-plan.json .ufo/evidence/round-22/source-refresh-entries.json .ufo/evidence/round-23/source-prefix-preservation.json .ufo/evidence/round-24/source-prefix-preservation.json .ufo/evidence/round-24/noharm-c8c5b88.json"
      ],
      "opened": [
        ".ufo/evidence/round-15/verify.py",
        ".ufo/evidence/round-21/c1-mutants.json",
        ".ufo/evidence/round-21/c1-survivors.py",
        ".ufo/evidence/round-21/c2-contract.json",
        ".ufo/evidence/round-21/c2-count.py",
        ".ufo/evidence/round-21/coldread/measure.py",
        ".ufo/evidence/round-21/f5/receipt.json",
        ".ufo/evidence/round-21/routemix-r20-spec1.json",
        ".ufo/evidence/round-22/accounting-extra-cases.json",
        ".ufo/evidence/round-22/bundle.json",
        ".ufo/evidence/round-22/expected.json",
        ".ufo/evidence/round-22/measure.py",
        ".ufo/evidence/round-22/source-refresh-entries.json",
        ".ufo/evidence/round-22/wrong-count-bundle.json",
        ".ufo/evidence/round-22/wrong-count-expected.json",
        ".ufo/evidence/round-23/extra-cases.json",
        ".ufo/evidence/round-23/measure.py",
        ".ufo/evidence/round-23/registry-baseline.json",
        ".ufo/evidence/round-23/replay.py",
        ".ufo/evidence/round-23/replay/bundle.json",
        ".ufo/evidence/round-23/replay/expected.json",
        ".ufo/evidence/round-23/replay/observations.json",
        ".ufo/evidence/round-23/requirements.json",
        ".ufo/evidence/round-23/source-prefix-preservation.json",
        ".ufo/evidence/round-23/source-read-bundle.json",
        ".ufo/evidence/round-23/source-read-expected.json",
        ".ufo/evidence/round-23/source-refresh-plan.json",
        ".ufo/evidence/round-24/extra-cases.json",
        ".ufo/evidence/round-24/measure.py",
        ".ufo/evidence/round-24/noharm-c8c5b88.json",
        ".ufo/evidence/round-24/replay/bundle.json",
        ".ufo/evidence/round-24/replay/live-dependent.json",
        ".ufo/evidence/round-24/replay/observations.json",
        ".ufo/evidence/round-24/source-prefix-preservation.json",
        ".ufo/evidence/round-26/after/registry-40a12bf.json",
        ".ufo/evidence/round-27/coldread/traces/ReRead03-1.json",
        ".ufo/waves/round-21/routemix-spec1.json",
        ".ufo/waves/round-21/spec1.json",
        ".ufo/waves/round-24/w1/RunRegistry.md",
        ".ufo/waves/round-27/w1/Read03.md",
        "corpus/SOURCES.md",
        "corpus/knowledge/callback-authoritative-accounting.md",
        "corpus/knowledge/hermetic-env-differential.md",
        "corpus/knowledge/replay-projection-hardening.md",
        "corpus/knowledge/required-command-binding.md",
        "corpus/lessons/round-21.md",
        "corpus/lessons/round-22.md",
        "corpus/lessons/round-23.md",
        "corpus/lessons/round-24.md",
        "corpus/lessons/round-27-verifier-spotcheck.md",
        "tools/command-binding.py",
        "tools/env-diff.py",
        "tools/mutate-and-run.sh",
        "tools/registry-replay.py",
        "tools/registry.json",
        "tools/round21-measure.py",
        "tools/trace-inputs.py",
        "tools/wave-accounting.py",
        "tools/wave-route-mix.py"
      ],
      "inputs": {
        ".ufo/evidence/round-15/verify.py": "7e4519d9a0ea68ebbd02890629f06a6fac8e6eab034d9fa3b19d386b088a2522",
        ".ufo/evidence/round-21/c1-mutants.json": "670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c",
        ".ufo/evidence/round-21/c1-survivors.py": "a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396",
        ".ufo/evidence/round-21/c2-contract.json": "5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd",
        ".ufo/evidence/round-21/c2-count.py": "9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2",
        ".ufo/evidence/round-21/coldread/measure.py": "657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb",
        ".ufo/evidence/round-21/f5/receipt.json": "9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264",
        ".ufo/evidence/round-21/routemix-r20-spec1.json": "b43bd8943448c1ae918b5ce51c976f33829450b2650fd3242d6033be7c6eca7b",
        ".ufo/evidence/round-22/accounting-extra-cases.json": "e60807f2154164638b13709af930760d0f16c2c8c4a2dee7297a490c5338a41f",
        ".ufo/evidence/round-22/bundle.json": "dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e",
        ".ufo/evidence/round-22/expected.json": "e35a5934afa0ace85aeba5e687c8e12b7c7c2258af9cd00d76c13f8c0975457d",
        ".ufo/evidence/round-22/measure.py": "f833d067afd3ca17b8534fc942d6e8ed529edd3d55476802c18ea631c0678056",
        ".ufo/evidence/round-22/source-refresh-entries.json": "e66a01a05fa41d87b36f4ccb9537e68db9125d8fdc6e776b3ec41372b61fc175",
        ".ufo/evidence/round-22/wrong-count-bundle.json": "d984c49c57d2b12b3a4e2583cc33842af6927f0612b3b0d663acb2ca09a7a17e",
        ".ufo/evidence/round-22/wrong-count-expected.json": "caf7d29e0fea8e8492152d3798201069452019928d6dd58ba052d98e6d0ad0ec",
        ".ufo/evidence/round-23/extra-cases.json": "87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00",
        ".ufo/evidence/round-23/measure.py": "812749631090393b5fd08e102cae01708819487994806bff45670aad0f5e3939",
        ".ufo/evidence/round-23/registry-baseline.json": "ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a",
        ".ufo/evidence/round-23/replay.py": "adb4171652f954d460c5e0c86d8baa4fcfa2f7fdd0b87791995afb601ae22c11",
        ".ufo/evidence/round-23/replay/bundle.json": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9",
        ".ufo/evidence/round-23/replay/expected.json": "0831c9c820488dc9d9096c90aade44217b6b615501fae7810e6fce414cb2a0a1",
        ".ufo/evidence/round-23/replay/observations.json": "a83d8a0b53b6b51a6e2d445da5b99fd843586051b743908e43eff6ba947cfa16",
        ".ufo/evidence/round-23/requirements.json": "cd5205be9e5843e956191f673e620875f6f9c65a4c8ed9f224e656601a25a1e3",
        ".ufo/evidence/round-23/source-prefix-preservation.json": "56f0d004e4cb296704ed51802ccc7a3d03ca87b3abe22e6b871da3d1814ede8a",
        ".ufo/evidence/round-23/source-read-bundle.json": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf",
        ".ufo/evidence/round-23/source-read-expected.json": "70f357e354c4badb22f974070ccf37dfda512103c3cf3ab93297a3ea27cb5dc8",
        ".ufo/evidence/round-23/source-refresh-plan.json": "7085ae2038c18e21f8db78dd51e6a520bc7cde3e7cf264bc86451f59d2b6854e",
        ".ufo/evidence/round-24/extra-cases.json": "6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35",
        ".ufo/evidence/round-24/measure.py": "0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64",
        ".ufo/evidence/round-24/noharm-c8c5b88.json": "83e95c2210c8f22bc92fe8884fcd7a497727085348e3ff882ecea7a5bdebb21a",
        ".ufo/evidence/round-24/replay/bundle.json": "4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6",
        ".ufo/evidence/round-24/replay/live-dependent.json": "c3a5f9133f6f90a2da337873b26b4bae9b09a397b7a1abdaeee6ce003b9a4ef3",
        ".ufo/evidence/round-24/replay/observations.json": "2d9b1b77349bf148095a80bfd7ef9c98f8584b7a0c7c261a0d406896a69a7a88",
        ".ufo/evidence/round-24/source-prefix-preservation.json": "5dacb75adb5c13b3bb0d876c7878a2d61e572ba7ef9b4a1c7fac59185a0b4a2e",
        ".ufo/evidence/round-26/after/registry-40a12bf.json": "9e8bf4b10b837c8a765710ab80a5c56ca4c13bc99ae518323b83605f218f26af",
        ".ufo/evidence/round-27/coldread/traces/ReRead03-1.json": "41693a9bc1a29e3c34daebaf7dd5b42731531fcde07030e3e53b1cd3da650171",
        ".ufo/waves/round-21/routemix-spec1.json": "92c1edb3fdf53ac45bb6d324c16d94b388c26960aceee53f74f6883af1b97d56",
        ".ufo/waves/round-21/spec1.json": "f78fe7472ed8243d46e23ca29f1bff34e646ff47832093fee815f858c22317af",
        ".ufo/waves/round-24/w1/RunRegistry.md": "b31e3633b4bac10f18c307a8bc568bfd21979b8622c980545c559322b4c10edc",
        ".ufo/waves/round-27/w1/Read03.md": "cd90435cf142a2912b10efb3c683908f2747e482abf84d211f6e4242b30d96bc",
        "corpus/SOURCES.md": "a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45",
        "corpus/knowledge/callback-authoritative-accounting.md": "ddf13b0835a5e6c21c308ab87ec24c9d8eee8bb8af3b3b254d73b554e9cf6035",
        "corpus/knowledge/hermetic-env-differential.md": "90756351093e2273257ce6a738bb90b6923865bc22d9276ba2cf8aeafb262e7e",
        "corpus/knowledge/replay-projection-hardening.md": "7602943988d8c7a2ce566b810b28d98c01938c565244be2503bee295d76520f4",
        "corpus/knowledge/required-command-binding.md": "2e72f8a04017b6d16e67ebd8e9e8bdb5d45b70701030a3f5466b187369ab4fd6",
        "corpus/lessons/round-21.md": "35444ddc32116089f87733c8f0a635dc7b452407d2bd0f47de483e8aacfb1a7d",
        "corpus/lessons/round-22.md": "47fe282169e3bb142a348ba6cc79bc4ee029d59ed5168928c9929d5a8a35b553",
        "corpus/lessons/round-23.md": "07fdc1a037ad84e4ecfcd053d86547cfb35879b3883299e18c58e35e30fbb932",
        "corpus/lessons/round-24.md": "29fd3e00a79242536bc259f6d56d6473e5e0d1e5bf451413c061fb6094b7d7a6",
        "corpus/lessons/round-27-verifier-spotcheck.md": "12ea67c0c37661296fa5c41c91d1d5e7363728536fa7bf07976d6fe1906d6957",
        "tools/command-binding.py": "9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d",
        "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/registry-replay.py": "9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714",
        "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
        "tools/round21-measure.py": "eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/wave-accounting.py": "96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e",
        "tools/wave-route-mix.py": "1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read14B-13.json"
      ]
    }
  ]
}
```

## What I checked

Clone `/tmp/Read14B-uA48/fleet/tameshi-shokunin` at detached `b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a`
(SKILL.md sha256 matches the given `c46ec02e...`). The section runs 1964–2102 (next heading
`## Ninth recorded case` at 2104). Class: record — it documents gates/probes and their histories,
it does not tell a reader to run anything.

Round-28 correction (the item under C1): `c2-count.py:19` is literally
`FLEET = Path("/home/vgpnk/Projects/shokunin")` and `:52` is `blob = show(FLEET / frozen["repo"], ...)`,
so `--repo` is bypassed for the tameshi-runner pin — verified statically. `tools/wave-route-mix.py:19`
defaults to `~/.omp/agent/config.yml`, and the retained receipt `.ufo/waves/round-21/routemix-spec1.json`
is `ok: true`. Routed item 1 in `corpus/lessons/round-27-verifier-spotcheck.md` names this section
("Round-21 gate/probe registry ... gap-blocking"). ReRead03 receipts carry `rev b1cc95e1fb62...`,
matching the cited `b1cc95e`.

Executed claims (all under `tools/trace-inputs.py`, all receipts `rev == read_rev`, zero
`live_lane_reads` in every receipt): `env-diff.py --contract` → `classified=9/9`, exit 0, and a
fresh classification differing from round-21's on `js-round-gate` (nondeterministic — exactly the
repeat-variation caveat the section makes); `env-diff --selftest` 9/9; `command-binding.py` on the
frozen replay pair → exit 0, `finding_ids: []`, `bundle_sha256 3d6c99b7…` (matching the pinned registry
row); on the source-read pair → exit 1, `ARGV_MISMATCH` (matching `command-binding-source-read-red-pinned`);
`command-binding --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass` (matches row
`command-binding-selftest-r24`, and the superseded row still expects 38/38); `wave-accounting` on
wrong-count pair → exit 1 `TOTAL_MISMATCH`; `--selftest` → `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`;
`registry-replay --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`; `wave-route-mix --spec
.ufo/waves/round-21/spec1.json` → exit 0 `ok: true` (today's live route table happens to still hold it).

Static/table checks: 56 registry rows, 49 active / 7 superseded; the four named r24 rows exist with the
exact expects quoted (44/44, both `bundle_sha256` pins, 10/10); `live-dependent.json` lists exactly
`pin-disposition-read` and `verify-round15` with `revision_pinned=41, rows=43`; `verify.py` itself
hardcodes `/home/vgpnk/Projects/shokunin`; `mutate-and-run.sh` resolves sibling repos via `$FLEET_ROOT`
pins; `round21-measure.py` delegates to unchanged `c1-survivors.py`/`c2-count.py` (all three frozen
files unchanged since `33d03b7`, verified by `git diff`); round-24 `measure.py` docstring says eleven
predicates and carries K1–K11; round-22/23 `measure.py` carry `total: 8`/`10`; round-22
`accounting-extra-cases.json` has 16 cases; all cited knowledge entries, lessons (QUALITY43–49,
Errata E–P present), SOURCES rows (S028/S079/S082/S083/S084/S085, S079 reopened-mined, S028 reopened
per round-21 lesson) exist; `replay.py` uses `retain_streams`; bundle receipts are 43 with instrument-
supplied argv/cwd/revision. Skipped (stated): `round21-measure.py --claim c2`/`--selftest` and the
`coldread/measure.py` runs — both would read the live lane or an L1-appended file, forbidden during
traces; the full 47/49-row registry battery (time + live reads).

One honest incident: in batch receipt `Read14B-12.json` I mistakenly included
`.ufo/evidence/round-21/coldread/ledger.json` in a file-list read; it is an L1-appended exception file.
I reran the identical batch without it (`Read14B-13.json`, clean), listed the original command and
receipt verbatim for completeness, and excluded the ledger from `inputs`. Nothing else I did depends
on its contents.

Tooling: nothing installed; python3/strace/bwrap already present.

COLDREAD Read14B: gap-minor
