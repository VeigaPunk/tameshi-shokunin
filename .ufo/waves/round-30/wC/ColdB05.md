# ColdB05 — cold reads, SKILL.md sections 14/15/16 at bb681566

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdB05", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
  "sections": [
    {"start": 1302, "heading": "### The six-leg regression — usage and this round's receipt", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [
       "Anchor truncation: the leg list sits at blob lines 84-89 of tools/mutate-and-run.sh@75ed934d; the cite :85-89 names only five of six legs",
       "Anchor truncation: pins/tables span lines 542-559; the cite :550-559 names only the last two PIN/REV pairs plus all six TABLE_ lines",
       "Anchor truncation: the registry's six regression_case_git calls span 1112-1140; the cite :1132-1141 covers only the checklist-run and js-claims-check calls",
       "Spec anchors :766/:841 land on the r10-2 comment headers 3-4 lines above the spec heredocs (`cat >` at 770 and 845); they name the right specs but point high",
       "Mode-mirror anchor :104-106 lands in the r10-2 doc comment (100-106); the mechanism code is :932-960, which the pair does cite",
       "Misquote: section calls the round-7 line \"Four legs at this revision\"; SKILL.md:925 reads \"Four legs at that revision\" (errata table SKILL.md:1733 records the same wording, so the quote is reproduced loosely)",
       "Not re-verifiable here: the receipt's own timestamps and /tmp/w10-t10-4-ev workdir, and the owner's 21:00:24Z run closing identically (no receipt file cited)"
     ],
     "commands_executed": [
       "bash -c 'git show 606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh > /tmp/ColdB05-dxMx/mar-r10-2.sh && sha256sum /tmp/ColdB05-dxMx/mar-r10-2.sh && wc -l /tmp/ColdB05-dxMx/mar-r10-2.sh'",
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/operator-runbook.md",
       "timeout 300 bash tools/mar-r10-2.sh --selftest",
       "timeout 420 bash tools/mar-r10-2.sh --regression --workdir /tmp/ColdB05-dxMx/r10regression --keep"
     ],
     "opened": ["tools/mutate-and-run.sh", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/operator-runbook.md"],
     "inputs": {"tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e", "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859"},
     "external_inputs": {"tameshi-shokunin@606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5", "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426", "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f", "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5", "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13", "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf", "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b"},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-14-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-14-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-14-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-14-4.json"]},

    {"start": 1380, "heading": "### The map — where a reader enters, artifact by artifact", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [],
     "commands_executed": [
       "python3 -c \"import sys;[print(open(p).read()[:120000]) for p in sys.argv[1:]]\" corpus/knowledge/service-limits.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/fleet-suite-census.md corpus/knowledge/service-standing-state.md corpus/knowledge/closeout-r11.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/operator-runbook.md corpus/README.md tools/mutate-and-run.sh plans/completion-evidence.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-tsukuroi-census.md",
       "bash -c 'ls plans/round-*.plan.md; echo ===; ls plans/round-*-record-draft.md; echo ===; ls corpus/knowledge/mutation-case-*.md | wc -l; echo ===; ls plans/*record* plans/*11* 2>/dev/null'"
     ],
     "opened": ["corpus/knowledge/operator-runbook.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/service-limits.md", "corpus/knowledge/service-optin-protocol.md", "corpus/knowledge/fleet-suite-census.md", "corpus/knowledge/service-standing-state.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/knowledge/mutation-case-kagi-checklist.md", "corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kumitate-cite-check.md", "corpus/knowledge/mutation-case-kumitate-claims.md", "corpus/knowledge/mutation-case-kumitate-round-gate.md", "corpus/knowledge/mutation-case-kumitate-sources-check.md", "corpus/knowledge/mutation-case-mado-verify.md", "corpus/knowledge/mutation-case-tsukuroi-census.md", "tools/mutate-and-run.sh", "corpus/README.md", "plans/completion-evidence.md", "corpus/knowledge/closeout-r11.md"],
     "inputs": {"corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e", "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0", "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e", "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f", "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952", "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0", "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7", "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548", "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e", "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9", "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec", "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38", "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3", "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604", "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9", "corpus/README.md": "636b716e7891f09cc3eb4a2c47bcf3a5120460c356dcfc07f5d8ba9b63259909", "plans/completion-evidence.md": "8e0485655a4801b9070bfa7dd688e774fed1a2e8b1692b046109ad83ebe2a3ef", "corpus/knowledge/closeout-r11.md": "cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265"},
     "external_inputs": {"tameshi-shokunin@bb681566b18211adf8ae9c28df91e17678e3f545:LOG.md": "d603864623685c9b0a7bee7a2ea00aeb93e266cc4f6641617bd6b0070fb79db7", "tameshi-shokunin@bb681566b18211adf8ae9c28df91e17678e3f545:SCORECARD.md": "9ba015ca568db27e71dd35322884952c18f7be0e306667f35391da7174fd920a"},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-15-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-15-2.json"]},

    {"start": 1479, "heading": "## Repeated controls and gate registry — round 12", "class": "instruction", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": [
       "Repeat-row verdict-map cell \"2 and 64 could-not-evaluate\" conflates findings: in tools/repeat-control.py exit 64 is invalid_usage only, while every could-not-evaluate finding (baseline_nonzero, command_unavailable, snapshot_tampered, setup_error) exits 2",
       "Same row labels exits 0/1 \"clean\"/\"failed\"; the tool's findings are controls_match/controls_mismatch (EXIT_BY_ID). Codes right, glosses loose",
       "The \"at round 12\" SHONEN claim was verified only at commit c7986cd (post-round-12 SHONEN carries [~] at box 3); the exact round-12 write-time blob was not located by this reader"
     ],
     "commands_executed": [
       "python3 tools/repeat-control.py --runs 3 --out /tmp/ColdB05-r12-controls -- /bin/true",
       "timeout 150 python3 tools/repeat-control.py --selftest",
       "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/repeat-control.py tools/bash-witness-study.py .ufo/evidence/round-12/verification-final.json .ufo/evidence/round-12/ControlGate/expected.json .ufo/evidence/round-12/ControlGate/mismatch/expected.json .ufo/evidence/round-12/BashWitness/declaration.json .ufo/evidence/round-12/BashWitness/declared.tsv .ufo/evidence/round-12/BashWitness/manifest.json corpus/knowledge/repeated-control-precondition.md corpus/lessons/round-1-verifier-spotcheck.md .ufo/waves/round-27/w1/Read25.md SHONEN.md"
     ],
     "opened": ["tools/repeat-control.py", "tools/bash-witness-study.py", ".ufo/evidence/round-12/verification-final.json", ".ufo/evidence/round-12/ControlGate/expected.json", ".ufo/evidence/round-12/ControlGate/mismatch/expected.json", ".ufo/evidence/round-12/ControlGate/run-1.exit", ".ufo/evidence/round-12/ControlGate/run-1.stderr", ".ufo/evidence/round-12/ControlGate/run-1.stdout", ".ufo/evidence/round-12/ControlGate/run-2.exit", ".ufo/evidence/round-12/ControlGate/run-2.stderr", ".ufo/evidence/round-12/ControlGate/run-2.stdout", ".ufo/evidence/round-12/ControlGate/run-3.exit", ".ufo/evidence/round-12/ControlGate/run-3.stderr", ".ufo/evidence/round-12/ControlGate/run-3.stdout", ".ufo/evidence/round-12/ControlGate/mismatch/run-1.exit", ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stderr", ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stdout", ".ufo/evidence/round-12/ControlGate/mismatch/run-2.exit", ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stderr", ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stdout", ".ufo/evidence/round-12/ControlGate/mismatch/run-3.exit", ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stderr", ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stdout", ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/manifest.json", "corpus/knowledge/repeated-control-precondition.md", "corpus/lessons/round-1-verifier-spotcheck.md", ".ufo/waves/round-27/w1/Read25.md", "SHONEN.md"],
     "inputs": {"tools/repeat-control.py": "296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25", "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9", ".ufo/evidence/round-12/verification-final.json": "9f3d117af3b613d0a00b7d0a623d31136e36f53cb6fcb5626e42cf0c6e022201", ".ufo/evidence/round-12/ControlGate/expected.json": "1b645be04d756c304a1ef5ecc221cf92f82c5f4afbdcfde4b77fe27117684aa1", ".ufo/evidence/round-12/ControlGate/mismatch/expected.json": "57f010e99e69a6632869c125229f8bcf0cfdaf866b6dcab9f16ed07ebc8f6771", ".ufo/evidence/round-12/ControlGate/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa", ".ufo/evidence/round-12/ControlGate/run-1.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1", ".ufo/evidence/round-12/ControlGate/run-1.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a", ".ufo/evidence/round-12/ControlGate/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa", ".ufo/evidence/round-12/ControlGate/run-2.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1", ".ufo/evidence/round-12/ControlGate/run-2.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a", ".ufo/evidence/round-12/ControlGate/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa", ".ufo/evidence/round-12/ControlGate/run-3.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1", ".ufo/evidence/round-12/ControlGate/run-3.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a", ".ufo/evidence/round-12/ControlGate/mismatch/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa", ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096", ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stdout": "5223d0557d70eaaa8555c648e04c01d463e4572853f782100b7afb15b3f2b6c8", ".ufo/evidence/round-12/ControlGate/mismatch/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa", ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096", ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stdout": "5223d0557d70eaaa8555c648e04c01d463e4572853f782100b7afb15b3f2b6c8", ".ufo/evidence/round-12/ControlGate/mismatch/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa", ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096", ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stdout": "b52929a30ae03d121fdd499fa74bd6ec58f06ebbc802c53c3b1918e67916b539", ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901", ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3", ".ufo/evidence/round-12/BashWitness/manifest.json": "273ffc39308a6c55bdb1c8f7a86bac9f95886ec470773c99b4d1e2db5b25e1cf", "corpus/knowledge/repeated-control-precondition.md": "1339460070d6c2c2d9609915a675b6866f0c42089a39bdb1ecb39b52f1c5fe5b", "corpus/lessons/round-1-verifier-spotcheck.md": "f99ef0ae2b3a3e4939c86b9ce5ab1e701733801c1cc1c7063767edf692e0edad", ".ufo/waves/round-27/w1/Read25.md": "6e6b3cca20d1fa6db9230f2a38a3398a8038b477b98a5edc86783e44f9e3e173", "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09"},
     "external_inputs": {"tameshi-shokunin@c7986cdf051cbe9d047f02f76f2e1da0b36a84e3:SHONEN.md": "f9bcbe1a24e3ffbcd5de8d7ffb36740d9f8a098e006f2d38bddc4e9a167e3e7b"},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-16-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-16-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB05-16-3.json"]}
  ]}
```

## What I checked

**Section 14 (record — the six-leg regression receipt).** The section anchors
everything at tool sha256 `75ed934d…`. I located that blob in history (commit
`606716f`), materialized it to `/tmp/ColdB05-dxMx/mar-r10-2.sh` (sha256 and the
"1 642 L" line count both match), and read its embedded registry: all six legs,
their recorded revisions (`175de6ba`, `fecee874`, `165307fe`, `eead56b2`) and
recorded verdict tables give exactly the claimed rates (8/8/6/4 kills of 10,
7/15 for checklist). Because the tool resolves `FLEET_ROOT` from `$SELF`, I ran
it inside my fleet-mirror clone where every pinned sibling revision exists. The
receipt **reproduced end to end**: `--selftest` → `MUTATE_SELFTEST: 80/80 pass`
/ `VERDICT: PASS` (including the new arms for the exec-bit mirror and the
embedded-spec/recorded-table agreement check), and `--regression` → all six
legs `match=N/N flips=0 inconclusive=0`, killed 8/8/6/4/7-of-15/7, closing
`REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0
flips<=0)` with `mode=` carried on every `REGRESSION_PIN`. The ledger claims
check out too: `fleet-kill-rate-ledger.md:85-88` still says "cases 1 and 2
only", the `:281` bullet (inside ER-2) supersedes it with four materialized
legs, and SKILL.md's own `:925-929`/`:1218-1222`/`:1226-1228` cites land where
claimed. Held back from `verified-record` by anchor precision only: four cited
windows are truncated (`:85-89` omits leg 1 at line 84; `:550-559` omits the
first four pin pairs starting at 542; `:1132-1141` covers only the last two of
six registry calls; `:766`/`:841` point at comment headers above the heredocs),
plus one reproduced misquote ("this revision" vs the line's "that revision",
already noted in the page's own errata table at `:1733`). Smallest safe
correction: retarget those four windows to 84-89, 542-559, 1112-1140, 770/845,
and quote line 925 verbatim.

**Section 15 (record — the artifact map).** All eleven rows verified: every
cited file exists and its "holds" description matches the file's real
structure — the runbook's § list matches its `##` headers exactly
(§0/§2/§3/§4/§5/§6/§7/§10); the ledger states §1–§4 byte-frozen; limits is the
refusal table; optin-protocol carries request shape/re-pin/read-only/report;
census §5 is the offer+queue; standing-state carries the boundary note with
SC1–SC3 at lines 159/174/181; nine `mutation-case-*.md` notes exist with
spec/verdict-table/survivor/reproduce structure; the current tool header
itself documents six legs at round 11 growing to nine by round 26; README is
the one-row-per-note coverage map; plans show the round-4–10 plan+record-draft
convention with no round-11 record file (LOG.md:316-317 confirms "the lane
deliverables ARE the wave record", read via `git show`); `closeout-r11.md` and
`plans/completion-evidence.md` (committed now, "uncommitted at this write")
exist; LOG.md/SCORECARD.md carry the round rows and counting commands
(`git show`, hashes in external_inputs). The two self-anchors resolve:
`:1294-1297` is the "anchored source governs" line and `:1246-1270` is the
service-limits rendering. No gaps found.

**Section 16 (instruction — the repeat-control recipe + registry).** The
recipe ran as written: `python3 tools/repeat-control.py --runs 3 --out
/tmp/ColdB05-r12-controls -- /bin/true` printed `REPEAT_RUN 1-3 exit=0`,
`REPEAT_COMPARE identical=yes`, `REPEAT_CONTROL: controls_match` — the
decision table's first row. `--selftest` passed `SELFTEST: PASS (29 cases)`,
exercising the pinned ControlGate `expected.json` snapshots (the receipt shows
the tool opened them, matching the "pinned values" cell). The registry rows
check out against code: repeat-control exits 0/1/2/64 per its EXIT_BY_ID table
("snapshot read-only" — snapshot mode executes nothing); bash-witness-study
has `count`/`selftest`/`check`/`run`/`rerun` commands with the stated exit
conventions and argparse-driven 64; `declaration.json` carries the not-blind
disclosure verbatim and the runner pin `75ed934d…`; the cited Read25 report is
real and its three findings (B1 stale runner pin, W2 the 64 conflation, W3
frozen-list over-claim) are all now resolved in the section text — the current
text discloses the runner-pin staleness and narrows "integrity-frozen" to a
named list. Minor gaps: the repeat row's "2 and 64 could-not-evaluate" lumps
`invalid_usage` (64) into could-not-evaluate, and its "clean"/"failed" labels
are loose glosses; the "at round 12" SHONEN `[~]` was verified at `c7986cd`,
not at the exact round-12 write commit. Smallest safe correction: split the
verdict-map cell into "2 could-not-evaluate · 64 usage".

No tools installed or upgraded; stock bash/python3/git/strace sufficed.
COLDREAD ColdB05: gap-minor, verified-record, gap-minor
