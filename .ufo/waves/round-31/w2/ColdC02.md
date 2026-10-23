# ColdC02 — independent cold read, Tameshi round 31 wave 2

Seat: ColdC02. Read revision: 2da841bd9913a2037d2bf612793382e572c9d205 (clone detached there;
SKILL.md sha256 2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a matches).
I read three SKILL.md sections (6, 7, 8 as assigned), each with fresh cold traces written via
`python3 tools/trace-inputs.py` from inside the scratch clone. All 24 trace receipts list
rev=2da841bd9913a2037d2bf612793382e572c9d205 and argv identical to the commands below.

## Section 6 (line 1814, "## Live-tree re-pin and entry-command monitor — round 17") — gap-minor (instruction)
Executed the recipe commands and every one matched the section's stated outcomes:
- `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json` → exit 1, status failed, 1 failed finding, expectation "producer_before" unresolved (id expected_contains_missing). Matches step 1.
- Same with `.ufo/evidence/round-18/dispositions.json` → exit 0, status clean, effective=11, superseded=1 (12 rows). Matches step 2.
- Text mode of the same command printed exactly one `HISTORICAL <path> rev=<rev> sha256=<sha>` line per waived instrument (3 lines for tools/bash-witness-study.py, tools/mutate-and-run.sh, tools/pin-disposition.py). Matches the "text mode prints one HISTORICAL line per waived instrument" claim.
- Round-17 manifests: both `.ufo/evidence/round-17/dispositions-before.json` and `dispositions.json` exit 2 with `expected_input_digest_mismatch` (observed 60575e62… vs expects 49e9e5e2… for tools/bash-witness-study.py). Confirms the parenthetical "round 17's two now exit 2".
- Sources check out: corpus/lessons/round-16-verifier-spotcheck.md §3 and §6 route R16-OP1 and R16-MON1; SOURCES.md rows S061 (jj leaves Git HEAD detached at the working-copy commit's parent, i.e. @-), S062 (git rev-parse --show-toplevel), S063 (repository discovery and GIT_* environment) match the section's parentheticals.
- Minor gaps: recipe step 3 (`python3 tools/registry-check.py --rev <40-hex>`) was NOT executed — replaying all 56 rows of tools/registry.json (including `mutate-and-run --regression` timeout_s=900 and `mte-interop-check` timeout_s=900) exceeds the 6-minute bound for this cold-read item; I verified the trailer format `REGISTRY_CHECK: held=N/M superseded=K` and the exit map from tools/registry-check.py:46-54 instead. Recipe step 4 (reading branch-tip bytes via tools/pin-disposition.py head rows) is documentation and was not executed.

## Section 7 (line 1855, "## Input-keyed cold-read credit — round 17") — verified-record (record)
- Sources verified: corpus/lessons/round-16-verifier-spotcheck.md §2 and §6 route R16-C2b and R16-C2c; SOURCES.md rows S058 (verifying traces: rebuild when a recorded dependency hash differs), S059 and S064 (a cache hit is sound only for inputs in its key), S060 (strace sees files opened by name) match the section's descriptors; corpus/knowledge/input-keyed-coldread-credit.md exists and states the same input-keyed rules (blob check, veto, limits, re-measure).
- Tools verified live: `.ufo/evidence/round-18/coldread/assemble.py --selftest` → SELFTEST 80/80 pass; `.ufo/evidence/round-19/coldread/measure.py --selftest` → SELECTOR_SELFTEST 3/3 pass. Both tools open the files the recipe names.
- QUALITY 67 (criterion in corpus/QUALITY.md) matches the recipe's `--workdir`/kill-scope sentence.
- The correction-of-round-16 paragraph was checked against git history: the `### Round-15 gate/probe registry` section has 30 lines including its heading at 28aeef4 and e69b488 and 31 lines (including heading) at c699c8c, 05a2247, 09ee1d0 and 017a2b0, so "grew from 30 to 31 lines" holds under the natural counting that includes the heading line. The round-14 bucket story (sha-only credit kept while tools/mutate-and-run.sh moved; recipe exited 2) is consistent with the spot-check lesson §2.
- No failing or wrong expectation found.

## Section 8 (line 1938, "### Round-20 gate/probe registry — frozen receipt instruments") — verified-record (record)
- `python3 tools/receipt-window.py --contract .ufo/evidence/round-20/contract.json --receipts .ufo/evidence/round-20/final/receipts.json --json` → verdict CLEAN, exit 0 (2 receipts, both INSTALL_IDENTITY).
- `python3 tools/receipt-window.py --selftest` → RECEIPT_WINDOW_SELFTEST 20/20 pass.
- `python3 tools/receipt-measure.py --selftest` → RECEIPT_MEASURE_SELFTEST 10/10 pass; prints runner sha256 a67bffa9… (matches the receipt runner_sha256) and instrument sha256 f34dc233… (matches contract frozen round20-measure).
- `python3 .ufo/evidence/round-20/coldread/measure.py --selftest` → SELECTOR_SELFTEST 12/12 pass, including the nine override-refused cases (--ledger-file, --ledger-rev, --inputs-overlay plus abbreviations and equals forms, all exit 64 with SELECTOR_OVERRIDE_FORBIDDEN).
- `python3 tools/receipt-measure.py --repo <scratch clone> --rev 2da841bd9913a2037d2bf612793382e572c9d205 --json` → 6/6 PASS, exit 0 (contract order, staged shas, installed gate, selftest receipt 20/20, final receipts clean, 4/4 historical identities classified).
- Source check: corpus/lessons/round-20.md documents the S049 child-environment reopening and the frozen/installed/edit-interval rules; QUALITY criterion 41 (corpus/QUALITY.md:390) states the no-in-place-edit/freeze-before-dispatch rule; SOURCES.md S049 says explicit env mappings define child environment; `.ufo/evidence/round-20/public-cli-cases.json` exists as independent synthetic expectations.
- No failing or wrong expectation found.

## Residual risk and verification gaps
- Section 6: the registry-check --rev replay is the only named command not run (6-minute bound); trailer format verified by code reading, not execution.
- Section 7: the round-14 ledger-level claim (CR26 at snapshot sha, runner 75ed934d) was not re-derived from the old ledger; I verified the corroborating spot-check lesson and the line-count claim from git history.
- Sections 7 and 8 are classed `record`; their recipe-style parts are procedure documentation, and the named tools were exercised via selftests and CLI runs as recorded above.
- No tool installs were performed (no pacman/uv/npx installs this session).

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ColdC02",
  "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a",
  "read_rev": "2da841bd9913a2037d2bf612793382e572c9d205",
  "sections": [
    {
      "start": 1814,
      "heading": "## Live-tree re-pin and entry-command monitor \u2014 round 17",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Recipe step 3 (`python3 tools/registry-check.py --rev <40-hex lane commit>`) not executed: replaying all 56 registry rows (including `mutate-and-run --regression` with timeout_s=900 and `mte-interop-check` with timeout_s=900) exceeds the cold-read item's 6-minute bound; the trailer format `REGISTRY_CHECK: held=N/M superseded=K` and exit map were verified from tools/registry-check.py:46-54 instead.",
        "Recipe step 4 (read siblings/lane committed bytes at refs/heads/<branch> via tools/pin-disposition.py head rows) is documentation, not executed."
      ],
      "commands_executed": [
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] corpus/lessons/round-16-verifier-spotcheck.md corpus/SOURCES.md",
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] tools/evidence-disposition.py tools/registry-check.py tools/registry.json tools/pin-disposition.py",
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] .ufo/evidence/round-18/dispositions-before.json .ufo/evidence/round-18/dispositions.json",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json"
      ],
      "opened": [
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/producer-before.py",
        ".ufo/evidence/round-13/producer-oracle-repair.json",
        ".ufo/evidence/round-13/producer-oracle.py",
        ".ufo/evidence/round-13/verification.json",
        ".ufo/evidence/round-13/witness-metadata-old-null.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-14/dispositions-before.json",
        ".ufo/evidence/round-14/dispositions.json",
        ".ufo/evidence/round-17/dispositions-before.json",
        ".ufo/evidence/round-17/dispositions.json",
        ".ufo/evidence/round-18/dispositions-before.json",
        ".ufo/evidence/round-18/dispositions.json",
        "corpus/SOURCES.md",
        "corpus/lessons/round-16-verifier-spotcheck.md",
        "tools/bash-witness-study.py",
        "tools/evidence-disposition.py",
        "tools/mutate-and-run.sh",
        "tools/pin-disposition.py",
        "tools/registry-check.py",
        "tools/registry.json",
        "tools/witness-metadata.py"
      ],
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
        ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
        ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
        ".ufo/evidence/round-17/dispositions-before.json": "79f0b397b727152b260df90e3ba9aa886d20eb7b5e5a43f6c3d03c7d3ee32354",
        ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
        ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
        ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
        "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741",
        "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
        "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
        "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
        "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
        "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-6-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-6-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-6-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-6-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-6-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-6-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-6-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-6-8.json"
      ]
    },
    {
      "start": 1855,
      "heading": "## Input-keyed cold-read credit \u2014 round 17",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] corpus/lessons/round-16-verifier-spotcheck.md corpus/SOURCES.md corpus/knowledge/input-keyed-coldread-credit.md",
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] tools/trace-inputs.py .ufo/evidence/round-18/coldread/assemble.py .ufo/evidence/round-19/coldread/measure.py",
        "python3 .ufo/evidence/round-18/coldread/assemble.py --selftest",
        "python3 .ufo/evidence/round-19/coldread/measure.py --selftest",
        "git -C /fast/scratch/hyaku/tameshi-r31-seats/ColdC02/fleet/tameshi-shokunin show 09ee1d0:SKILL.md",
        "git -C /fast/scratch/hyaku/tameshi-r31-seats/ColdC02/fleet/tameshi-shokunin show 28aeef4:SKILL.md",
        "python3 -c \nimport subprocess\nrep='/fast/scratch/hyaku/tameshi-r31-seats/ColdC02/fleet/tameshi-shokunin'\nrevs=['28aeef498cc070c3183271b709bc79d344ff547a','e69b488','c699c8c','05a2247','09ee1d0','017a2b0c0d1a8fe513e41710416c87b9d6ef9ae9']\nhdr='### Round-15 gate/probe registry'\nfor rev in revs:\n    out=subprocess.run(['git','-C',rep,'show',rev+':SKILL.md'],capture_output=True,text=True).stdout.splitlines()\n    hits=[i for i,l in enumerate(out) if l.strip()==hdr]\n    if not hits:\n        print(rev[:8],'NO_EXACT_HEADING', [l[:60] for l in out if 'Round-15' in l][:3]); continue\n    s=hits[0]; e=None\n    for i in range(s+1,len(out)):\n        if out[i].startswith('#') and out[i].strip()!=hdr:\n            e=i; break\n    if e is None: e=len(out)\n    print(rev[:8],'hit_lines',hits,'count_excl_heading',e-s-1,'count_incl_heading',e-s)\n"
      ],
      "opened": [
        ".ufo/evidence/round-18/coldread/assemble.py",
        ".ufo/evidence/round-18/measure.py",
        ".ufo/evidence/round-19/coldread/measure.py",
        "corpus/SOURCES.md",
        "corpus/knowledge/input-keyed-coldread-credit.md",
        "corpus/lessons/round-16-verifier-spotcheck.md",
        "tools/trace-inputs.py"
      ],
      "inputs": {
        ".ufo/evidence/round-18/coldread/assemble.py": "bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a",
        ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
        ".ufo/evidence/round-19/coldread/measure.py": "4c9c74ca3bb0d85121d6bd3e4deeafe4474374d0a67becf9a9c9fe4c0d42f2f7",
        "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741",
        "corpus/knowledge/input-keyed-coldread-credit.md": "0c45dccb4dfa78cdfd2dfddc59132d1e636ed0d548abcb9528d1b1aa21fd0636",
        "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
      },
      "external_inputs": {
        "tameshi-shokunin@09ee1d0:SKILL.md": "906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:SKILL.md": "97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580",
        "tameshi-shokunin@e69b488:SKILL.md": "97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580",
        "tameshi-shokunin@c699c8c:SKILL.md": "3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4",
        "tameshi-shokunin@05a2247:SKILL.md": "e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3",
        "tameshi-shokunin@017a2b0c0d1a8fe513e41710416c87b9d6ef9ae9:SKILL.md": "906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-7-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-7-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-7-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-7-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-7-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-7-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-7-7.json"
      ]
    },
    {
      "start": 1938,
      "heading": "### Round-20 gate/probe registry \u2014 frozen receipt instruments",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] corpus/lessons/round-20.md corpus/QUALITY.md corpus/SOURCES.md",
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] tools/receipt-window.py .ufo/evidence/round-20/contract.json .ufo/evidence/round-20/final/receipts.json",
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] tools/receipt-measure.py .ufo/evidence/round-20/stage/measure.py .ufo/evidence/round-20/coldread/measure.py",
        "python3 tools/receipt-window.py --contract .ufo/evidence/round-20/contract.json --receipts .ufo/evidence/round-20/final/receipts.json --json",
        "python3 tools/receipt-window.py --selftest",
        "python3 tools/receipt-measure.py --selftest",
        "python3 .ufo/evidence/round-20/coldread/measure.py --selftest",
        "python3 tools/receipt-measure.py --repo /fast/scratch/hyaku/tameshi-r31-seats/ColdC02/fleet/tameshi-shokunin --rev 2da841bd9913a2037d2bf612793382e572c9d205 --json",
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] .ufo/evidence/round-20/public-cli-cases.json"
      ],
      "opened": [
        ".ufo/evidence/round-18/measure.py",
        ".ufo/evidence/round-20/coldread/measure.py",
        ".ufo/evidence/round-20/contract.json",
        ".ufo/evidence/round-20/final/receipts.json",
        ".ufo/evidence/round-20/public-cli-cases.json",
        ".ufo/evidence/round-20/stage/measure.py",
        ".ufo/evidence/round-20/stage/receipt-window.py",
        "corpus/QUALITY.md",
        "corpus/SOURCES.md",
        "corpus/lessons/round-20.md",
        "tools/receipt-measure.py",
        "tools/receipt-window.py"
      ],
      "inputs": {
        ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
        ".ufo/evidence/round-20/coldread/measure.py": "48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13",
        ".ufo/evidence/round-20/contract.json": "9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715",
        ".ufo/evidence/round-20/final/receipts.json": "4186b44e6f5ef95aeb39768e5b9d8a0e6953283961bcc009733dbbcde48cb5d6",
        ".ufo/evidence/round-20/public-cli-cases.json": "590df60420a60bec1f6dddad6b5eaf34a5d700cdd86c5cf231b1ef8f5a3b27b2",
        ".ufo/evidence/round-20/stage/measure.py": "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d",
        ".ufo/evidence/round-20/stage/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
        "corpus/QUALITY.md": "6cbf9cf7a9117a747be356f7ac5ed8288c8609195205bcca427809b4d96804ac",
        "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741",
        "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6",
        "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa",
        "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdC02-8-9.json"
      ]
    }
  ]
}
```
COLDREAD ColdC02: gap-minor, verified-record, verified-record
