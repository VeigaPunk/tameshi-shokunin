# Read30 cold read: SKILL.md line 1754 (round-16 seventh case), pinned rev 2227d83

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read30",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 1754,
      "heading": "## Seventh recorded case and full-page cold-read \u2014 round 16",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Survivor-probe step (SKILL.md:1794-1796) gives no invocation. probes.mjs takes one probe id as argv[2] (probes.mjs:12) and reads GATE and FXROOT from the environment (probes.mjs:10-11); both defaults point at /tmp/tameshi-r16-survivorprep, which a fresh host lacks. The header says it runs only the pristine blob and never a mutant (probes.mjs:2-3), so the mutant half of the claim needs a GATE override that the section does not name. With that override the exit codes match the section (receipt 5).",
        "Counting command (SKILL.md:1802-1803) defaults --repo to the live lane path (.ufo/evidence/round-16/measure.py:53 and :634-635). Run from a clone without --repo, it reads the live lane instead. The section does not say so; I passed --repo to the pinned clone (receipt 6).",
        "Box-3 pointer is stale (SKILL.md:1803-1804). The section says the full-page read earns the box-3 lane assertion. At 2227d83, SHONEN.md:9 still marks box 3 [~], but SHONEN.md:10 links .ufo/evidence/round-21/coldread/ledger.json, not the round-16 ledger the counting command checks. measure.py therefore reports shonen.box3_ledger_link false, box3_points false and calibration_restraint_score 6 (receipt 6). The L1 should repoint the box-3 line or mark this sentence as history.",
        "Pristine-run count (SKILL.md:1786-1789) says three pristine runs differ byte-for-byte. The case note records eight pristine runs, all exit 0 and each with different stdout (corpus/knowledge/mutation-case-kumitate-round-gate.md:28-29). The byte-difference claim holds; the count does not match the note.",
        "Recipe working directory and tools (SKILL.md:1764-1773) are unstated. The recipe uses relative paths (E=.ufo/..., bash tools/...), so it must run from the lane root with node and git on PATH; the section says neither."
      ],
      "commands_executed": [
        "sh -c 'command -v strace; command -v node; node --version; git --version; python3 --version'",
        "bash -c 'W=$(mktemp -d /tmp/tameshi-r16-rg.XXXXXX); git -C ~/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > \"$W/round-gate.mjs\" && sha256sum \"$W/round-gate.mjs\" && E=.ufo/evidence/round-16/round-gate && bash tools/mutate-and-run.sh --target \"$W/round-gate.mjs\" --defects \"$E/round-gate.defects.spec\" --suite \"$(cat \"$E/suite.txt\")\" --label js-round-gate --workdir \"$W/work\"; echo \"RECIPE_RC=$? W=$W\"'",
        "sh -c 'git status --porcelain; echo \"status_rc=$?\"; git diff --stat e69b488f65b17bcfd41949abf7d538a77678dc26 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 -- .ufo/evidence/round-16/round-gate corpus/knowledge/mutation-case-kumitate-round-gate.md; echo \"diff_rc=$?\"; git show -s --format=\"%H %cI %s\" e69b488f65b17bcfd41949abf7d538a77678dc26; echo \"show_rc=$?\"'",
        "sha256sum corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/arm-class-matrix.md .ufo/evidence/round-16/round-gate/predictions.json .ufo/evidence/round-16/round-gate/round-gate.defects.spec .ufo/evidence/round-16/round-gate/suite.txt .ufo/evidence/round-16/round-gate/runner-regression.txt .ufo/evidence/round-16/round-gate/runner-selftest.txt .ufo/evidence/round-16/round-gate/runner-sha256.txt .ufo/evidence/round-16/round-gate/legcount-redbefore-mutant.txt .ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs .ufo/evidence/round-16/round-gate/survivor-probes/c1059-probe.sh .ufo/evidence/round-16/round-gate/sweep/results.tsv .ufo/evidence/round-16/measure.py SHONEN.md tools/mutate-and-run.sh tools/repeat-control.py",
        "bash -c 'P=.ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs; W=/tmp/tameshi-r16-rg.zd6e97/work; for pair in \"P1 A2\" \"P6 B2\" \"P9 E1\"; do set -- $pair; GATE=$W/pristine.round-gate.mjs FXROOT=/tmp/Read30-probes/pristine-$1 node $P $1 > /tmp/Read30-probes-$1-pristine.log 2>&1; echo \"$1 pristine rc=$?\"; GATE=$W/mutant-$2.round-gate.mjs FXROOT=/tmp/Read30-probes/mutant-$1 node $P $1 > /tmp/Read30-probes-$1-mutant.log 2>&1; echo \"$1 mutant-$2 rc=$?\"; done'",
        "python3 .ufo/evidence/round-16/measure.py --repo /tmp/Read30-jNht/fleet/tameshi-shokunin --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
        "bash -c 'S=$(mktemp -d /tmp/Read30-gd-XXXX); git init -q \"$S/gd\"; export GIT_DIR=\"$S/gd/.git\"; node /tmp/tameshi-r16-rg.zd6e97/work/pristine.round-gate.mjs --selftest > \"$S/out.txt\" 2>&1; echo \"selftest_rc=$?\"; echo \"commits_in_exported_GIT_DIR=$(git --git-dir=\"$S/gd/.git\" rev-list --all --count)\"; echo \"selftest_output_lines=$(wc -l < \"$S/out.txt\")\"; cat \"$S/out.txt\"'",
        "bash -c 'S=$(mktemp -d /tmp/Read30-tmpx-XXXX); D=$PWD/.Read30-tmp-probe; mkdir -p \"$D\"; TMPDIR=\"$D\" node /tmp/tameshi-r16-rg.zd6e97/work/pristine.round-gate.mjs --selftest > \"$S/out.txt\" 2>&1; echo \"selftest_rc_TMPDIR_inside_worktree=$?\"; cat \"$S/out.txt\"; rm -rf \"$D\"; echo \"cleanup_rc=$?\"'",
        "bash -c 'git cat-file -t e69b488f65b17bcfd41949abf7d538a77678dc26; git merge-base --is-ancestor e69b488f65b17bcfd41949abf7d538a77678dc26 2227d8338c02aa9a5fd7d95c1a41b76865ad7647; echo \"ancestor_rc=$?\"; git show e69b488f65b17bcfd41949abf7d538a77678dc26:.ufo/evidence/round-16/round-gate/predictions.json | sha256sum; git show e69b488f65b17bcfd41949abf7d538a77678dc26:.ufo/evidence/round-16/round-gate/round-gate.defects.spec | sha256sum; sha256sum tools/trace-inputs.py corpus/knowledge/executor-test-sufficiency.md corpus/knowledge/guard-kill-closure.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/repeated-control-precondition.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/verification-patterns-fleet.md .ufo/evidence/round-16/coldread/SKILL.snapshot.md .ufo/evidence/round-16/coldread/skill-versions/SKILL.05a2247.md .ufo/evidence/round-16/coldread/skill-versions/SKILL.c699c8c.md tools/registry.json tools/witness-metadata.py'",
        "bash -c 'git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:SHONEN.md | sha256sum; git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:tools/mutate-and-run.sh | sha256sum; git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:corpus/SOURCES.md | sha256sum; git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:.ufo/evidence/round-16/coldread/ledger.json | sha256sum; sha256sum .ufo/evidence/round-26/cite-check/regression-worktree.stdout .ufo/evidence/round-18/coldread/traces/CR18/2.out.txt'",
        "sha256sum .ufo/evidence/round-18/coldread/traces/CR18-r3/2.out.txt .ufo/evidence/round-18/coldread/traces/CR18/6.out.txt .ufo/evidence/round-18/coldread/traces/CR18/7.out.txt .ufo/evidence/round-18/coldread/traces/CR25/11.json .ufo/evidence/round-18/coldread/traces/CR28/13.json .ufo/evidence/round-18/coldread/traces/CR31-r3/15.json .ufo/evidence/round-18/coldread/traces/L1/audit-1021.json .ufo/evidence/round-18/coldread/traces/L1/audit-1069.json .ufo/evidence/round-18/coldread/traces/L1/audit-1164.json .ufo/evidence/round-18/coldread/traces/L1/audit-1212.json .ufo/evidence/round-18/coldread/traces/L1/audit-131.json .ufo/evidence/round-18/coldread/traces/L1/audit-1436.json .ufo/evidence/round-18/coldread/traces/L1/audit-1479.json .ufo/evidence/round-18/coldread/traces/L1/audit-1676.json .ufo/evidence/round-18/coldread/traces/L1/audit-1707.json .ufo/evidence/round-18/coldread/traces/L1/audit-1754.json .ufo/evidence/round-18/coldread/traces/L1/audit-1814.json .ufo/evidence/round-18/coldread/traces/L1/audit-1846.json .ufo/evidence/round-18/coldread/traces/L1/audit-1855.json .ufo/evidence/round-26/contract.json .ufo/evidence/round-26/after/registry-40a12bf.json"
      ],
      "opened": [
        ".gitignore",
        ".ufo/evidence/round-16/coldread/SKILL.snapshot.md",
        ".ufo/evidence/round-16/coldread/skill-versions/SKILL.05a2247.md",
        ".ufo/evidence/round-16/coldread/skill-versions/SKILL.c699c8c.md",
        ".ufo/evidence/round-16/measure.py",
        ".ufo/evidence/round-16/round-gate/legcount-redbefore-mutant.txt",
        ".ufo/evidence/round-16/round-gate/predictions.json",
        ".ufo/evidence/round-16/round-gate/round-gate.defects.spec",
        ".ufo/evidence/round-16/round-gate/runner-regression.txt",
        ".ufo/evidence/round-16/round-gate/runner-selftest.txt",
        ".ufo/evidence/round-16/round-gate/runner-sha256.txt",
        ".ufo/evidence/round-16/round-gate/suite.txt",
        ".ufo/evidence/round-16/round-gate/survivor-probes/c1059-probe.sh",
        ".ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs",
        ".ufo/evidence/round-16/round-gate/sweep/results.tsv",
        ".ufo/evidence/round-18/coldread/traces/CR18/2.out.txt",
        ".ufo/evidence/round-26/cite-check/regression-worktree.stdout",
        "SHONEN.md",
        "corpus/knowledge/arm-class-matrix.md",
        "corpus/knowledge/executor-test-sufficiency.md",
        "corpus/knowledge/guard-kill-closure.md",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md",
        "corpus/knowledge/mutation-case-kumitate-sources-check.md",
        "corpus/knowledge/repeated-control-precondition.md",
        "corpus/knowledge/service-optin-protocol.md",
        "corpus/knowledge/verification-patterns-fleet.md",
        "tools/mutate-and-run.sh",
        "tools/registry.json",
        "tools/repeat-control.py",
        "tools/trace-inputs.py",
        "tools/witness-metadata.py",
        ".ufo/evidence/round-18/coldread/traces/CR18-r3/2.out.txt",
        ".ufo/evidence/round-18/coldread/traces/CR18/6.out.txt",
        ".ufo/evidence/round-18/coldread/traces/CR18/7.out.txt",
        ".ufo/evidence/round-18/coldread/traces/CR25/11.json",
        ".ufo/evidence/round-18/coldread/traces/CR28/13.json",
        ".ufo/evidence/round-18/coldread/traces/CR31-r3/15.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1021.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1069.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1164.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1212.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-131.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1436.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1479.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1676.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1707.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1754.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1814.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1846.json",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1855.json",
        ".ufo/evidence/round-26/contract.json",
        ".ufo/evidence/round-26/after/registry-40a12bf.json"
      ],
      "inputs": {
        ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116",
        ".ufo/evidence/round-16/coldread/SKILL.snapshot.md": "97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580",
        ".ufo/evidence/round-16/coldread/skill-versions/SKILL.05a2247.md": "e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3",
        ".ufo/evidence/round-16/coldread/skill-versions/SKILL.c699c8c.md": "3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4",
        ".ufo/evidence/round-16/measure.py": "03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",
        ".ufo/evidence/round-16/round-gate/legcount-redbefore-mutant.txt": "7381604aa50310d5d55b88fe8265ba4f7556e87935b5fdd939a0b1271fea5d50",
        ".ufo/evidence/round-16/round-gate/predictions.json": "bb344eee3b034d774a829042717dc5c78517edcf8ef5f369831bc2fae0f70bc1",
        ".ufo/evidence/round-16/round-gate/round-gate.defects.spec": "e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4",
        ".ufo/evidence/round-16/round-gate/runner-regression.txt": "630c3806e106af550d4afc6cd79bf2b0846472530a33772038df443db6e591e4",
        ".ufo/evidence/round-16/round-gate/runner-selftest.txt": "1df28c867553a3ec48107b69c44714298537e5744bb44a973d620a68fbbf5505",
        ".ufo/evidence/round-16/round-gate/runner-sha256.txt": "9758a1d89fd301dd93095a611eb1738a9a9afeebba2c6dbe28cfdbb04a764d99",
        ".ufo/evidence/round-16/round-gate/suite.txt": "6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b",
        ".ufo/evidence/round-16/round-gate/survivor-probes/c1059-probe.sh": "ee03b939a4659574256226008d3a8d3b423fc950dc2981332f13f18ec0741b25",
        ".ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs": "131c2835b1b5ce5fab60960fbca864c444d2cd75c19f08da410616e49bd332fb",
        ".ufo/evidence/round-16/round-gate/sweep/results.tsv": "97a9377635817a28349ff74aa44352dc8081fb2ef6ba5401c255b350f6e8d0bb",
        ".ufo/evidence/round-18/coldread/traces/CR18/2.out.txt": "e64348f0ba532948e478615cd0812cbc0e80ed6f550b244646fc014693327b52",
        ".ufo/evidence/round-26/cite-check/regression-worktree.stdout": "cf6e07b6d4251c466f1f68d5e406e0300b8daa8614e17edc69b6a0b6906ee6e5",
        "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
        "corpus/knowledge/arm-class-matrix.md": "bd4f4a02eb66f4e25e67a1518108d1f11c45b4edf2355d1901ec54ce55359088",
        "corpus/knowledge/executor-test-sufficiency.md": "b26021292d69b3686851e13363d8451009f12a32dc85925b5a7cd2295e34cf07",
        "corpus/knowledge/guard-kill-closure.md": "30ed4a23aa1151d26f3177b783e0b09d32a140f8c16d65191d4ad924862d6116",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
        "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38",
        "corpus/knowledge/repeated-control-precondition.md": "1339460070d6c2c2d9609915a675b6866f0c42089a39bdb1ecb39b52f1c5fe5b",
        "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
        "corpus/knowledge/verification-patterns-fleet.md": "814f471a93b32fb3297c43f24b1041170a632c0ae93d73b7317f3b5150d2aecb",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
        "tools/repeat-control.py": "296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
        ".ufo/evidence/round-18/coldread/traces/CR18-r3/2.out.txt": "c3990006017b244610bf2eefc5c6dbfcc2c25a8833db3a01f065d706e5038a5f",
        ".ufo/evidence/round-18/coldread/traces/CR18/6.out.txt": "236333dcb3675e6c0e0a2e6cad50b06efca36dbd8fc7914fe9115b98edd2152d",
        ".ufo/evidence/round-18/coldread/traces/CR18/7.out.txt": "055adf0079964773ae3e0a6168b152de9e9254ad5b20c9594de40133b501302a",
        ".ufo/evidence/round-18/coldread/traces/CR25/11.json": "3dd2781727540cb57d1ae67399d6074465338a9c125d314e52b35ecb8e066026",
        ".ufo/evidence/round-18/coldread/traces/CR28/13.json": "181d50b60e5dc94d1b48204ba5510ade0d9cb675b549d18b7b384dcc2d7f55fa",
        ".ufo/evidence/round-18/coldread/traces/CR31-r3/15.json": "7e6b3fd341be15d9b9643027542b1bb42e5c06a8d8a7dcea88fd1d6a77b44aa2",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1021.json": "5b619053e6e7fd11da8f6e6b5abc616f5ce5690e15ee0190715230edc2bda281",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1069.json": "e3b464cc4872908bd19f1776021bddd3e1b1ba4730af4f36f73e5988e42a7159",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1164.json": "d0af0495cb43c85ef6f290e763e3362622c1f7340d80f0bdd8f96eb7c6612884",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1212.json": "4c380253561ac866a4584b4694a5e406f5e0cdaf75cf07b637a6224f79525326",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-131.json": "ebc2c799e8a174a68bcf1991efff50203842e76cfda5401cfd0a644d068deae8",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1436.json": "2d2b3eba7c9e53a0371bb0cee047db358578c99144d48a5c8d6aae358e172d45",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1479.json": "bd5afc88c8b2497934baba9337dc86cd48b6a6620ca3c72b0400dfd3c6201760",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1676.json": "8378b05af142674ba3454d3728fcd521cdb840bb91b536dc0fde8608f5759a66",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1707.json": "40ccc9b02b582959c23ef09baa76caacdfa93e31405a70cd55e97115e1fa5188",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1754.json": "a7105fdf81e57dd05a7f6ae7825c35244e2f3268aa7dc9367c0163223f966ad4",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1814.json": "76a1caca8838cc8da11dcd1a82fa60ad3f129706f34a308789a38eeeacdf572d",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1846.json": "df56cb2b182706b47c27f815a207b7da44351f26c76bc0d5815e29e89bee79c7",
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1855.json": "41ac0ba89c53e466b5e2713659e0ddc3521a8c96b0e1523b1f237773808bcf86",
        ".ufo/evidence/round-26/contract.json": "db68b00099b13dee6a1f1852966ebb822fe295e85e2b7e8ed4cad4a929c55df9",
        ".ufo/evidence/round-26/after/registry-40a12bf.json": "9e8bf4b10b837c8a765710ab80a5c56ca4c13bc99ae518323b83605f218f26af"
      },
      "external_inputs": {
        "kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs": "f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9",
        "tameshi-shokunin@e69b488f65b17bcfd41949abf7d538a77678dc26:.ufo/evidence/round-16/round-gate/predictions.json": "bb344eee3b034d774a829042717dc5c78517edcf8ef5f369831bc2fae0f70bc1",
        "tameshi-shokunin@e69b488f65b17bcfd41949abf7d538a77678dc26:.ufo/evidence/round-16/round-gate/round-gate.defects.spec": "e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4",
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a",
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:.ufo/evidence/round-16/coldread/ledger.json": "b84151a35f0cefa0716f3dd200a183dee5badc7be09ba1bac11d61283f70623c"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read30-11.json"
      ]
    }
  ]
}
```

## Note

- Class and verdict. The section tells a reader to run three things: the Reproduce-it recipe, the survivor-probe harness, and the counting command. I therefore classed it as instruction, and gap-minor is credited for that class. I did not choose executed-ok because the five minor gaps above are real. None of them blocks reproduction.
- Recipe. I ran the recipe as one shell line with the same commands in the same order (receipt 2; exit 0; 84 s wall). Everything the section expects matched: the kumitate blob sha256 is f890e277...d3e9; CONTROL is GREEN with 60/60 checks; the sweep reports killed=5 survived=5 inconclusive=0 kill-rate=50%; MUTATE_RESTORE is OK; and each of the ten verdicts equals its pre-registered prediction.
- Records checked. Commit e69b488 exists, is an ancestor of 2227d83, and is dated 2026-10-20T10:39:59-03:00. predictions.json and round-gate.defects.spec are byte-identical at e69b488 and 2227d83 (receipts 3 and 9). Regression counts: cases=7 in the round-16 receipt (runner-regression.txt:41), cases=8 in the round-18 receipt (CR18/2.out.txt:45), and cases=9 in the round-26 receipt (cite-check/regression-worktree.stdout:50); measure.py also counts nine legs (receipt 6).
- Interval edge. C1059 survived. C1060 was killed at check [8], whose findings include REPORT_THIN (sweep log line 9 of C1060.out). REPORT_MIN_BYTES is 1024 at line 167 of the pinned blob. The [26, 1059] projection is at arm-class-matrix.md:404-417 and is labelled projected, not measured.
- Hazards. A TMPDIR inside the worktree gives 57/60, with checks 37, 51 and 56 failing and exit 1 (receipt 8), so the control goes red. An exported GIT_DIR sends 43 fixture commits into that repository, and the run then exits 1 (receipt 7). The env -i suite string in suite.txt is identical to the regression-leg string at tools/mutate-and-run.sh:1416.
- Survivor probes. P1, P6 and P9 exit 0 on the pristine copy and exit 1 on their mutants once GATE is set (receipt 5). The round-16 SKILL snapshot hashes to 97cf436b...3580, the value the errata cites (receipt 9).
- Not run or not checked. The full nine-leg regression was not run or timed. The round-gate leg alone took 84 s under the collector, so I did not start a replay that could exceed the six-minute bound. c1059-probe.sh was not run. CKIND has no probe; the case note argues equivalence instead. GuardAudit (hostile mutants) and the bwrap advice are recorded only, not re-measured. The wave files under .ufo/waves/round-16/w2 and w3 were listed but not opened, so the fresh-seat claims are unaudited. The original sweep time (13:40:15Z) comes from the case note; my run is dated 2026-10-22.
- Observation, not a gap. The runner in this tree hashes to fb91ef76...; the case note records 75ed934d... and the round-16 regression receipt records 0673d2e5.... The section names no runner hash, and the expected tokens matched.
- Provenance. Step 1 (the clone, the detached checkout and the sibling symlinks) ran before any trace root existed, so it is not in commands_executed. Three early git lookups in the clone ran untraced; receipts 3 and 9 repeat them. Directory-wide greps scanned more evidence files than they displayed; I hashed every displayed hit and relied only on the ones I cite. No receipt reads the live lane (live_lane_reads is empty in all eleven). No tools were installed or upgraded: strace, node v24.21.0, git 2.56.0 and Python 3.14.8 were already present.

COLDREAD Read30: gap-minor
