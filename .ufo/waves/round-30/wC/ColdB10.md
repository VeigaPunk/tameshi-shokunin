# ColdB10 — cold reads of SKILL.md sections 29–31 at bb681566b18211adf8ae9c28df91e17678e3f545

Clone: `/tmp/ColdB10-DqXo/fleet/tameshi-shokunin`, detached at `bb681566b18211adf8ae9c28df91e17678e3f545`;
`SKILL.md` sha256 `c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6` (verified).
Siblings symlinked read-only into `/tmp/ColdB10-DqXo/fleet/`. All commands ran under
`tools/trace-inputs.py`; every receipt shows `rev` = the pinned lane revision and zero live-lane reads.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdB10", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
 "sections": [
  {"start": 1964, "heading": "### Round-21 gate/probe registry — finite environment differential", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
   "minor_gaps": [],
   "commands_executed": [
    "python3 -c \"import sys,hashlib\nfor p in sys.argv[1:]:\n    b=open(p,'rb').read()\n    print(p,len(b),hashlib.sha256(b).hexdigest()[:16])\" tools/env-diff.py tools/wave-route-mix.py tools/round21-measure.py .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-21/c2-contract.json .ufo/evidence/round-21/f5/receipt.json .ufo/evidence/round-21/c2-count.py .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/coldread/ledger.json .ufo/evidence/round-21/coldread/affected-sections.json .ufo/waves/round-21/spec1.json .ufo/waves/round-21/routemix-spec1.json tools/wave-accounting.py .ufo/evidence/round-22/bundle.json .ufo/evidence/round-22/expected.json .ufo/evidence/round-22/wrong-count-bundle.json .ufo/evidence/round-22/wrong-count-expected.json .ufo/evidence/round-22/measure.py tools/command-binding.py .ufo/evidence/round-23/replay/bundle.json .ufo/evidence/round-23/replay/expected.json .ufo/evidence/round-23/replay/observations.json .ufo/evidence/round-23/extra-cases.json .ufo/evidence/round-23/measure.py .ufo/evidence/round-23/replay.py .ufo/evidence/round-23/source-read-bundle.json .ufo/evidence/round-23/source-read-expected.json tools/registry-replay.py .ufo/evidence/round-24/measure.py .ufo/evidence/round-24/extra-cases.json .ufo/evidence/round-24/replay/live-dependent.json tools/registry.json corpus/knowledge/hermetic-env-differential.md corpus/knowledge/callback-authoritative-accounting.md corpus/knowledge/required-command-binding.md corpus/knowledge/replay-projection-hardening.md corpus/lessons/round-21.md corpus/lessons/round-24.md",
    "python3 tools/wave-route-mix.py --selftest",
    "python3 tools/env-diff.py --selftest"],
   "opened": ["tools/env-diff.py","tools/wave-route-mix.py","tools/round21-measure.py","tools/wave-accounting.py","tools/command-binding.py","tools/registry-replay.py","tools/registry.json",".ufo/evidence/round-21/coldread/measure.py",".ufo/evidence/round-21/c2-contract.json",".ufo/evidence/round-21/f5/receipt.json",".ufo/evidence/round-21/c2-count.py",".ufo/evidence/round-21/c1-survivors.py",".ufo/evidence/round-21/coldread/ledger.json",".ufo/evidence/round-21/coldread/affected-sections.json",".ufo/waves/round-21/spec1.json",".ufo/waves/round-21/routemix-spec1.json",".ufo/evidence/round-22/bundle.json",".ufo/evidence/round-22/expected.json",".ufo/evidence/round-22/wrong-count-bundle.json",".ufo/evidence/round-22/wrong-count-expected.json",".ufo/evidence/round-22/measure.py",".ufo/evidence/round-23/replay/bundle.json",".ufo/evidence/round-23/replay/expected.json",".ufo/evidence/round-23/replay/observations.json",".ufo/evidence/round-23/extra-cases.json",".ufo/evidence/round-23/measure.py",".ufo/evidence/round-23/replay.py",".ufo/evidence/round-23/source-read-bundle.json",".ufo/evidence/round-23/source-read-expected.json",".ufo/evidence/round-24/measure.py",".ufo/evidence/round-24/extra-cases.json",".ufo/evidence/round-24/replay/live-dependent.json","corpus/knowledge/hermetic-env-differential.md","corpus/knowledge/callback-authoritative-accounting.md","corpus/knowledge/required-command-binding.md","corpus/knowledge/replay-projection-hardening.md","corpus/lessons/round-21.md","corpus/lessons/round-24.md"],
   "inputs": {
    "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
    "tools/wave-route-mix.py": "1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782",
    "tools/round21-measure.py": "eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d",
    "tools/wave-accounting.py": "96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e",
    "tools/command-binding.py": "9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d",
    "tools/registry-replay.py": "9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714",
    "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
    ".ufo/evidence/round-21/coldread/measure.py": "657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb",
    ".ufo/evidence/round-21/c2-contract.json": "5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd",
    ".ufo/evidence/round-21/f5/receipt.json": "9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264",
    ".ufo/evidence/round-21/c2-count.py": "9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2",
    ".ufo/evidence/round-21/c1-survivors.py": "a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396",
    ".ufo/evidence/round-21/coldread/ledger.json": "90c56e2e07e59aa7fe592d64e4044f5f121849c5f57ca4ab6b30c320c3d9ee53",
    ".ufo/evidence/round-21/coldread/affected-sections.json": "cffc98790d5ebdc75094dff9ca8fbd816412a87c5c9c1a6c58e36f1b7e1b8090",
    ".ufo/waves/round-21/spec1.json": "f78fe7472ed8243d46e23ca29f1bff34e646ff47832093fee815f858c22317af",
    ".ufo/waves/round-21/routemix-spec1.json": "92c1edb3fdf53ac45bb6d324c16d94b388c26960aceee53f74f6883af1b97d56",
    ".ufo/evidence/round-22/bundle.json": "dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e",
    ".ufo/evidence/round-22/expected.json": "e35a5934afa0ace85aeba5e687c8e12b7c7c2258af9cd00d76c13f8c0975457d",
    ".ufo/evidence/round-22/wrong-count-bundle.json": "d984c49c57d2b12b3a4e2583cc33842af6927f0612b3b0d663acb2ca09a7a17e",
    ".ufo/evidence/round-22/wrong-count-expected.json": "caf7d29e0fea8e8492152d3798201069452019928d6dd58ba052d98e6d0ad0ec",
    ".ufo/evidence/round-22/measure.py": "f833d067afd3ca17b8534fc942d6e8ed529edd3d55476802c18ea631c0678056",
    ".ufo/evidence/round-23/replay/bundle.json": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9",
    ".ufo/evidence/round-23/replay/expected.json": "0831c9c820488dc9d9096c90aade44217b6b615501fae7810e6fce414cb2a0a1",
    ".ufo/evidence/round-23/replay/observations.json": "a83d8a0b53b6b51a6e2d445da5b99fd843586051b743908e43eff6ba947cfa16",
    ".ufo/evidence/round-23/extra-cases.json": "87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00",
    ".ufo/evidence/round-23/measure.py": "812749631090393b5fd08e102cae01708819487994806bff45670aad0f5e3939",
    ".ufo/evidence/round-23/replay.py": "adb4171652f954d460c5e0c86d8baa4fcfa2f7fdd0b87791995afb601ae22c11",
    ".ufo/evidence/round-23/source-read-bundle.json": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf",
    ".ufo/evidence/round-23/source-read-expected.json": "70f357e354c4badb22f974070ccf37dfda512103c3cf3ab93297a3ea27cb5dc8",
    ".ufo/evidence/round-24/measure.py": "0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64",
    ".ufo/evidence/round-24/extra-cases.json": "6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35",
    ".ufo/evidence/round-24/replay/live-dependent.json": "c3a5f9133f6f90a2da337873b26b4bae9b09a397b7a1abdaeee6ce003b9a4ef3",
    "corpus/knowledge/hermetic-env-differential.md": "90756351093e2273257ce6a738bb90b6923865bc22d9276ba2cf8aeafb262e7e",
    "corpus/knowledge/callback-authoritative-accounting.md": "ddf13b0835a5e6c21c308ab87ec24c9d8eee8bb8af3b3b254d73b554e9cf6035",
    "corpus/knowledge/required-command-binding.md": "2e72f8a04017b6d16e67ebd8e9e8bdb5d45b70701030a3f5466b187369ab4fd6",
    "corpus/knowledge/replay-projection-hardening.md": "7602943988d8c7a2ce566b810b28d98c01938c565244be2503bee295d76520f4",
    "corpus/lessons/round-21.md": "35444ddc32116089f87733c8f0a635dc7b452407d2bd0f47de483e8aacfb1a7d",
    "corpus/lessons/round-24.md": "29fd3e00a79242536bc259f6d56d6473e5e0d1e5bf451413c061fb6094b7d7a6"},
   "external_inputs": {},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-29-1.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-29-2.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-29-3.json"]},
  {"start": 2104, "heading": "## Ninth recorded case — round 26", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
   "minor_gaps": [],
   "commands_executed": [
    "timeout 840 bash tools/mutate-and-run.sh --regression",
    "python3 -c \"import sys,hashlib\nfor p in sys.argv[1:]:\n    b=open(p,'rb').read()\n    print(p,len(b),hashlib.sha256(b).hexdigest()[:16])\" tools/mutate-and-run.sh corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md .ufo/evidence/round-26/cite-check/cite-check.defects.spec .ufo/evidence/round-26/cite-check/predictions.json .ufo/evidence/round-26/cite-check/sweep/sweep.txt .ufo/evidence/round-26/cite-check/sweep/results.tsv .ufo/evidence/round-26/cite-check/sweep/defects.tsv .ufo/evidence/round-26/cite-check/sweep/evidence/control.out .ufo/evidence/round-26/cite-check/regression-worktree.stdout tools/registry.json .ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md .ufo/waves/round-26/w1/CriticEquivalence.md corpus/SOURCES.md corpus/QUALITY.md",
    "python3 -c \"import sys,hashlib\nfor p in sys.argv[1:]:\n    b=open(p,'rb').read()\n    print(p,len(b),hashlib.sha256(b).hexdigest()[:16])\" corpus/lessons/round-29-verifier-spotcheck.md corpus/README.md",
    "git -C /tmp/ColdB10-DqXo/fleet/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum"],
   "opened": ["tools/mutate-and-run.sh","tools/registry.json","corpus/knowledge/mutation-case-kumitate-cite-check.md","corpus/knowledge/mutation-case-kumitate-round-gate.md","corpus/knowledge/mutation-case-kumitate-sources-check.md",".ufo/evidence/round-26/cite-check/cite-check.defects.spec",".ufo/evidence/round-26/cite-check/predictions.json",".ufo/evidence/round-26/cite-check/sweep/sweep.txt",".ufo/evidence/round-26/cite-check/sweep/results.tsv",".ufo/evidence/round-26/cite-check/sweep/defects.tsv",".ufo/evidence/round-26/cite-check/sweep/evidence/control.out",".ufo/evidence/round-26/cite-check/regression-worktree.stdout",".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md",".ufo/waves/round-26/w1/CriticEquivalence.md","corpus/SOURCES.md","corpus/QUALITY.md","corpus/README.md","corpus/lessons/round-29-verifier-spotcheck.md"],
   "inputs": {
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
    "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
    "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
    "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
    "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38",
    ".ufo/evidence/round-26/cite-check/cite-check.defects.spec": "969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208",
    ".ufo/evidence/round-26/cite-check/predictions.json": "f1d26201ffac81fdd7415ac325165807c0f721f841ec5608636ba415879c938e",
    ".ufo/evidence/round-26/cite-check/sweep/sweep.txt": "957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893",
    ".ufo/evidence/round-26/cite-check/sweep/results.tsv": "daa25ff90a7982db74f9dd8d1fbde79265b17f4e829ded05b0b621f00a81112d",
    ".ufo/evidence/round-26/cite-check/sweep/defects.tsv": "ddbfa4f932527afc98ec4f4c86e5789247f3fc0d5fa52a84089b51761fbb812c",
    ".ufo/evidence/round-26/cite-check/sweep/evidence/control.out": "30772e087254d8119f9458cc48fe5922dc038016b42f552e96716a1b4de0b145",
    ".ufo/evidence/round-26/cite-check/regression-worktree.stdout": "cf6e07b6d4251c466f1f68d5e406e0300b8daa8614e17edc69b6a0b6906ee6e5",
    ".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md": "7be4dc4cf29ee7d62c6a494627cafb33d2035072c174189b00bd52753b96ccd9",
    ".ufo/waves/round-26/w1/CriticEquivalence.md": "575ef324cba9b25c56ad8dd4ea4d251fb2c4941505a11b76b25a777f10d22285",
    "corpus/SOURCES.md": "b830d6fa03699f15bcfaeb7579899d247284b7a85a17e7ddb61a979a451007c7",
    "corpus/QUALITY.md": "f7e0dc952e6dc8c06dee59767b065a635920ce1a281cf8d4fa3d9e9420356a7a",
    "corpus/README.md": "636b716e7891f09cc3eb4a2c47bcf3a5120460c356dcfc07f5d8ba9b63259909",
    "corpus/lessons/round-29-verifier-spotcheck.md": "f130b4b9fa5a3ddc22c76d0e3536e2f37522c7a17bb598e994e99904d391ef39"},
   "external_inputs": {"kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-30-1.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-30-2.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-30-3.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-30-4.json"]},
  {"start": 2132, "heading": "### Round-26 gate/probe registry — report interop", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
   "minor_gaps": [],
   "commands_executed": [
    "python3 -c \"import sys,hashlib\nfor p in sys.argv[1:]:\n    b=open(p,'rb').read()\n    print(p,len(b),hashlib.sha256(b).hexdigest()[:16])\" tools/mte-interop.py tools/mutate-and-run.sh tools/registry.json tools/vendor/mutation-testing-metrics-3.9.0.tgz tools/vendor/mutation-testing-report-schema-3.9.0.tgz",
    "uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest",
    "timeout 840 uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /tmp/ColdB10-DqXo/fleet"],
   "opened": ["tools/mte-interop.py","tools/mutate-and-run.sh","tools/registry.json","tools/vendor/mutation-testing-metrics-3.9.0.tgz","tools/vendor/mutation-testing-report-schema-3.9.0.tgz"],
   "inputs": {
    "tools/mte-interop.py": "193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4",
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
    "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
    "tools/vendor/mutation-testing-metrics-3.9.0.tgz": "ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548",
    "tools/vendor/mutation-testing-report-schema-3.9.0.tgz": "adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280"},
   "external_inputs": {},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-31-1.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-31-2.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB10-31-3.json"]}]}
```

## What I checked

All three sections are records: they describe pinned tools, frozen counters and
retained receipts; each entry's selftest is named but the section does not direct
the reader to run the lane. I read every cited lane file under the trace
collector (receipts above), ran the named selftests where safe, and re-ran the
two long live checks in my own clone/fleet mirror.

- **Section 29** (round-21 registry, plus round-22/23/24 additions and the
  round-28 correction). Verified: `env-diff.py` and `wave-route-mix.py` exist
  with `--selftest` entry points and run clean (9/9 and 8/8, traced);
  `wave-route-mix.py` defaults `max_share=0.40` and reads
  `~/.omp/agent/config.yml` (line 19); `routemix-spec1.json` receipt exists and
  says `ok: true`; `round21-measure.py` maps claims to
  `c1-survivors.py`/`c2-count.py`; `c2-contract.json` holds nine surfaces and
  seven required profiles; `c2-count.py` hardcodes
  `FLEET = Path("/home/vgpnk/Projects/shokunin")` at line 19 and reads
  `FLEET / frozen["repo"]` at line 52 (the non-hermetic claim is exact);
  round-22/23/24 frozen counters declare eight, ten and eleven predicates;
  `replay/bundle.json` holds 43 receipts; `live-dependent.json` records
  `revision_pinned: 41`, `live_dependent: [pin-disposition-read,
  verify-round15]`; `tools/registry.json` has 49 active rows including
  `command-binding-selftest-r24` (44/44), the two `bundle_sha256`-pinned rows
  whose digests match the bundle files on disk, `registry-replay-selftest`
  (10/10), and the superseded 38/38 row still present; `ledger.json` has
  `prefix_retained: 199`; QUALITY items 43–48 exist; S079/S028/S082/S083/
  S084/S085 exist in SOURCES.md with the cited pointers.
- **Section 30** (ninth case, js-cite-check). Verified byte-exact: the
  kumitate blob at `1205c662…` is sha256 `40573448…c10c9f`, 2537 lines, mode
  100755 (traced `git show`; recorded as external input). `results.tsv` shows
  exactly the five K_/S_ verdicts claimed (5/10 killed) matching
  `predictions.json` and the embedded `TABLE_CITECHECK`; spec and predictions
  were committed at `622d31d` 10:01:47Z before the sweep at 10:02:07Z;
  `control.out` shows `62/62 cases passed (hermetic)`. I re-ran
  `bash tools/mutate-and-run.sh --regression` in the clone under the collector:
  `REGRESSION_CASE js-cite-check: PASS` and `REGRESSION: PASS (cases=9
  passed=9; ledger legs exact: killed-delta<=0 flips<=0)` — the replay claim
  re-verifies at the pinned revision, not just as a stored receipt. The
  S_EMPTY_GUARD equivalence is argued correctly in `ProbeSEMPTYGUARD.md` /
  `CriticEquivalence.md` (filesScanned increments before resolved, so
  resolved>0 implies filesScanned>0; the dropped guard is redundant), and the
  survivor table's four holes match the spec comments.
- **Section 31** (mte-interop). Verified: `mte-interop.py` entry lines match
  (gate with `--check`, `--selftest`, `--emit DIR`, `--fleet-root` default the
  checkout's parent); registry rows `mte-interop-selftest` (expects
  `MTE_SELFTEST: 17/17 pass`) and `mte-interop-check` (expects `MTE_INTEROP:
  PASS legs_conforming=9/9`) exist and are active. I ran both in the clone:
  selftest printed `MTE_SELFTEST: 17/17 pass` (exit 0, vendored tarballs
  extracted to scratch only); `--check --fleet-root <my mirror>` replayed the
  nine-leg ledger and printed nine `CONFORMS` legs plus `MTE_INTEROP: PASS
  legs_conforming=9/9`, matching the row's exit map (0 = every leg conforms).
  Its non-hermetic claim is accurate: the check stages a temp fleet that
  symlinks the sibling repos and replays their pinned objects.

No wrong expectations found. Notes: `--regression` takes ~11 minutes under
strace (above the 6-minute skip line but within the time box, so I ran it);
`mte-interop --check` took ~5.7 minutes under strace including a second
regression replay. `uv` resolved `jsonschema==4.25.1` into an ephemeral env
(no package installed). Two 300-second tool-cap kills occurred on the first
attempts; both runs were repeated to completion and only completed receipts
are cited. No tooling was installed (uv was already present at
`~/.local/bin/uv` 0.13.0; used only for the ephemeral jsonschema env the tool
entry itself prescribes).

COLDREAD ColdB10: verified-record, verified-record, verified-record
