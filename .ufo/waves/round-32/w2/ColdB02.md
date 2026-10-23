# ColdB02 — round 32 wave 2 cold read (sections 4 and 5, rev a4f718138bdad20de741faeca57891645e5a64d9)

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdB02", "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a", "read_rev": "a4f718138bdad20de741faeca57891645e5a64d9",
 "sections": [
  {
   "start": 1938,
   "heading": "### Round-20 gate/probe registry — frozen receipt instruments",
   "class": "record",
   "verdict": "verified-record",
   "blocking_gaps": [],
   "wrong_expectations": [],
   "minor_gaps": [
    "Six registered selftests were executed green under the collector (receipt-window 20/20, receipt-measure 10/10, env-diff 9/9, wave-accounting 8/8+16/16, command-binding 44/44, registry-replay 10/10); the two coldread selector probes (.ufo/evidence/round-20/coldread/measure.py, .ufo/evidence/round-21/coldread/measure.py) were verified by source read only, not executed.",
    "tools/round21-measure.py --selftest was deliberately not run: the section's own Round 28 correction says it reads live fleet Git objects via c2-count.py, and the source confirms it (c2-count.py line 19 FLEET = Path(\"/home/vgpnk/Projects/shokunin\"), line 52 blob = show(FLEET / frozen[\"repo\"], ...) — both line numbers exact).",
    "Some persisted-value cells were checked by existence only, not content: .ufo/evidence/round-20/final/receipts.json, public-cli-cases.json, .ufo/evidence/round-22 wrong-count pair, .ufo/evidence/round-23/replay/bundle.json, .ufo/evidence/round-24/measure.py, .ufo/waves/round-21/spec1.json.",
    "The '47-row registry battery of round 24' count was not independently recounted; the '49 active rows' count was (grep of tools/registry.json = 49) and the 43-row replay population was confirmed from .ufo/evidence/round-24/replay/live-dependent.json (rows 43, revision_pinned 41, live rows pin-disposition-read and verify-round15).",
    "tools/wave-route-mix.py --selftest was not run (its gate mode reads the operator's live route table; the retained receipt .ufo/waves/round-21/routemix-spec1.json with ok:true was opened instead and matches)."
   ],
   "commands_executed": [
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-20.md corpus/QUALITY.md corpus/SOURCES.md",
    "python3 tools/receipt-window.py --selftest",
    "python3 tools/receipt-measure.py --selftest",
    "python3 tools/env-diff.py --selftest",
    "python3 tools/wave-accounting.py --selftest",
    "python3 tools/command-binding.py --selftest",
    "python3 tools/registry-replay.py --selftest",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-21/c2-count.py tools/round21-measure.py tools/wave-route-mix.py tools/receipt-measure.py tools/receipt-window.py .ufo/evidence/round-20/coldread/measure.py .ufo/evidence/round-23/replay.py tools/registry-replay.py",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-20/contract.json .ufo/evidence/round-21/c2-contract.json .ufo/waves/round-21/routemix-spec1.json .ufo/evidence/round-22/bundle.json .ufo/evidence/round-22/expected.json",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-24/replay/live-dependent.json .ufo/evidence/round-21/f5/receipt.json"
   ],
   "opened": [
    ".ufo/evidence/round-20/coldread/measure.py", ".ufo/evidence/round-20/contract.json", ".ufo/evidence/round-20/stage/measure.py", ".ufo/evidence/round-20/stage/receipt-window.py",
    ".ufo/evidence/round-21/c2-contract.json", ".ufo/evidence/round-21/c2-count.py", ".ufo/evidence/round-21/coldread/measure.py", ".ufo/evidence/round-21/f5/receipt.json",
    ".ufo/evidence/round-22/accounting-extra-cases.json", ".ufo/evidence/round-22/bundle.json", ".ufo/evidence/round-22/expected.json", ".ufo/evidence/round-22/measure.py",
    ".ufo/evidence/round-23/extra-cases.json", ".ufo/evidence/round-23/replay.py", ".ufo/evidence/round-24/extra-cases.json", ".ufo/evidence/round-24/replay/live-dependent.json",
    ".ufo/waves/round-21/routemix-spec1.json", "corpus/QUALITY.md", "corpus/README.md", "corpus/SOURCES.md", "corpus/knowledge/required-command-binding.md",
    "corpus/lessons/round-20.md", "corpus/lessons/round-21.md", "corpus/lessons/round-22.md", "corpus/lessons/round-23.md", "corpus/lessons/round-25.md",
    "tools/command-binding.py", "tools/env-diff.py", "tools/mutate-and-run.sh", "tools/receipt-measure.py", "tools/receipt-window.py", "tools/registry-replay.py",
    "tools/registry.json", "tools/round21-measure.py", "tools/wave-accounting.py", "tools/wave-route-mix.py"
   ],
   "inputs": {
    ".ufo/evidence/round-20/coldread/measure.py": "48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13",
    ".ufo/evidence/round-20/contract.json": "9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715",
    ".ufo/evidence/round-20/stage/measure.py": "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d",
    ".ufo/evidence/round-20/stage/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
    ".ufo/evidence/round-21/c2-contract.json": "5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd",
    ".ufo/evidence/round-21/c2-count.py": "9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2",
    ".ufo/evidence/round-21/coldread/measure.py": "657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb",
    ".ufo/evidence/round-21/f5/receipt.json": "9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264",
    ".ufo/evidence/round-22/accounting-extra-cases.json": "e60807f2154164638b13709af930760d0f16c2c8c4a2dee7297a490c5338a41f",
    ".ufo/evidence/round-22/bundle.json": "dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e",
    ".ufo/evidence/round-22/expected.json": "e35a5934afa0ace85aeba5e687c8e12b7c7c2258af9cd00d76c13f8c0975457d",
    ".ufo/evidence/round-22/measure.py": "f833d067afd3ca17b8534fc942d6e8ed529edd3d55476802c18ea631c0678056",
    ".ufo/evidence/round-23/extra-cases.json": "87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00",
    ".ufo/evidence/round-23/replay.py": "adb4171652f954d460c5e0c86d8baa4fcfa2f7fdd0b87791995afb601ae22c11",
    ".ufo/evidence/round-24/extra-cases.json": "6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35",
    ".ufo/evidence/round-24/replay/live-dependent.json": "c3a5f9133f6f90a2da337873b26b4bae9b09a397b7a1abdaeee6ce003b9a4ef3",
    ".ufo/waves/round-21/routemix-spec1.json": "92c1edb3fdf53ac45bb6d324c16d94b388c26960aceee53f74f6883af1b97d56",
    "corpus/QUALITY.md": "6cbf9cf7a9117a747be356f7ac5ed8288c8609195205bcca427809b4d96804ac",
    "corpus/README.md": "c244f8ca2f877411e2d90195503f446a186bd10600664d75edfd0d6d59f14437",
    "corpus/SOURCES.md": "56838b80b69f38743c3ad2b252463afb2bb3ff6d1c6097f885c210629772c3d8",
    "corpus/knowledge/required-command-binding.md": "2e72f8a04017b6d16e67ebd8e9e8bdb5d45b70701030a3f5466b187369ab4fd6",
    "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6",
    "corpus/lessons/round-21.md": "35444ddc32116089f87733c8f0a635dc7b452407d2bd0f47de483e8aacfb1a7d",
    "corpus/lessons/round-22.md": "47fe282169e3bb142a348ba6cc79bc4ee029d59ed5168928c9929d5a8a35b553",
    "corpus/lessons/round-23.md": "07fdc1a037ad84e4ecfcd053d86547cfb35879b3883299e18c58e35e30fbb932",
    "corpus/lessons/round-25.md": "54b8e1814b43b7fc1e042831e9644b727abc1aa9e77ae426e363648972c10a6b",
    "tools/command-binding.py": "9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d",
    "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
    "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa",
    "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
    "tools/registry-replay.py": "9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714",
    "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
    "tools/round21-measure.py": "eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d",
    "tools/wave-accounting.py": "96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e",
    "tools/wave-route-mix.py": "1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782"
   },
   "external_inputs": {},
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-6.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-7.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-8.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-9.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-4-10.json"
   ]
  },
  {
   "start": 2104,
   "heading": "## Ninth recorded case — round 26",
   "class": "record",
   "verdict": "verified-record",
   "blocking_gaps": [],
   "wrong_expectations": [],
   "minor_gaps": [
    "The embedded replay instruction `bash tools/mutate-and-run.sh --regression` was attempted live with --workdir /fast/scratch/hyaku/tameshi-r32-seats/ColdB02/rg-5 under the trace collector with timeout 350s: it reproduced the first leg exactly (REGRESSION_PIN/REGRESSION_SWEEP/REGRESSION_TABLE/REGRESSION_CASE js-kimi-census: PASS, match=10/10 killed=8, REGRESSION_TOOL sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9) and was then killed by the timeout — the full 9-leg regression needs more than the 6-minute box, so that attempt has no trace receipt (trace-inputs was killed before writing one). The claim's expected output (REGRESSION_CASE js-cite-check: PASS; cases=9 passed=9) is confirmed from the retained receipt .ufo/evidence/round-26/cite-check/regression-worktree.stdout of a complete run at the landed runner a08e85c5d7f899e8a5992e20517edb1a380d79eb, whose leg pins and table match TABLE_CITECHECK in tools/mutate-and-run.sh (line 631).",
    "The first traced read (trace ColdB02-5-1) used a wrong path for one argv element (.ufo/evidence/round-26/cite-check/evidence/control.out; actual location is sweep/evidence/control.out), so that traced command's child exited 1 after printing the other five files; a corrected trace (ColdB02-5-3) opened control.out cleanly (exit 0).",
    "'committed (622d31d) before any mutant ran' is corroborated by commit time 2026-10-22 07:01:47 -0300 (= 10:01:47Z) vs MUTATE_DATE 2026-10-22T10:02:07Z in sweep.txt plus the entry's ReviewPreregTiming pointer; the ordering itself was not independently re-derived. Byte-identity of the pre-registered files was verified: cite-check.defects.spec sha256 969f50d6... and predictions.json sha256 f1d26201... are identical at 622d31d and at a4f71813.",
    "The '--integrations kills none of the five and is red at the pristine pin on live trees' claim was checked against .ufo/waves/round-26/w1/ProbeIntegrations.md (verdict lines match verbatim), not re-executed against live trees.",
    "Blob identity of kumitate scripts/cite-check.mjs at 1205c66 was verified by git cat-file in a read-only sibling checkout (sha256 40573448..., 2537 lines, mode 100755 — all three exact); no byte-diff against a second source was done beyond the recorded pin."
   ],
   "commands_executed": [
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-26/cite-check/sweep/sweep.txt .ufo/evidence/round-26/cite-check/sweep/results.tsv .ufo/evidence/round-26/cite-check/predictions.json .ufo/evidence/round-26/cite-check/regression-worktree.stdout corpus/knowledge/mutation-case-kumitate-cite-check.md .ufo/evidence/round-26/cite-check/evidence/control.out",
    "python3 -c \"import sys;[print(open(p).read()[:60000]) for p in sys.argv[1:]]\" .ufo/evidence/round-26/cite-check/sweep/evidence/control.out .ufo/evidence/round-26/cite-check/sweep/evidence/S_EMPTY_GUARD.out .ufo/evidence/round-26/cite-check/cite-check.defects.spec",
    "bash tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r32-seats/ColdB02/rg-5"
   ],
   "opened": [
    ".ufo/evidence/round-26/cite-check/cite-check.defects.spec", ".ufo/evidence/round-26/cite-check/predictions.json", ".ufo/evidence/round-26/cite-check/regression-worktree.stdout",
    ".ufo/evidence/round-26/cite-check/sweep/evidence/S_EMPTY_GUARD.out", ".ufo/evidence/round-26/cite-check/sweep/evidence/control.out",
    ".ufo/evidence/round-26/cite-check/sweep/results.tsv", ".ufo/evidence/round-26/cite-check/sweep/sweep.txt",
    "corpus/SOURCES.md", "corpus/knowledge/mutation-case-kumitate-cite-check.md", "tools/mutate-and-run.sh", ".ufo/waves/round-26/w1/ProbeIntegrations.md (existence and head read, untraced side check)"
   ],
   "inputs": {
    ".ufo/evidence/round-26/cite-check/cite-check.defects.spec": "969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208",
    ".ufo/evidence/round-26/cite-check/predictions.json": "f1d26201ffac81fdd7415ac325165807c0f721f841ec5608636ba415879c938e",
    ".ufo/evidence/round-26/cite-check/regression-worktree.stdout": "cf6e07b6d4251c466f1f68d5e406e0300b8daa8614e17edc69b6a0b6906ee6e5",
    ".ufo/evidence/round-26/cite-check/sweep/evidence/S_EMPTY_GUARD.out": "280dfc28d5c84f2506d9795bb1d16731d2a135f209fe9005bee99cbaaf24bc4f",
    ".ufo/evidence/round-26/cite-check/sweep/evidence/control.out": "30772e087254d8119f9458cc48fe5922dc038016b42f552e96716a1b4de0b145",
    ".ufo/evidence/round-26/cite-check/sweep/results.tsv": "daa25ff90a7982db74f9dd8d1fbde79265b17f4e829ded05b0b621f00a81112d",
    ".ufo/evidence/round-26/cite-check/sweep/sweep.txt": "957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893",
    "corpus/SOURCES.md": "56838b80b69f38743c3ad2b252463afb2bb3ff6d1c6097f885c210629772c3d8",
    "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"
   },
   "external_inputs": {
    "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f",
    "tameshi-shokunin@622d31d90b1fbc55c56e91a2b012bc18d6f1421a:.ufo/evidence/round-26/cite-check/cite-check.defects.spec": "969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208",
    "tameshi-shokunin@622d31d90b1fbc55c56e91a2b012bc18d6f1421a:.ufo/evidence/round-26/cite-check/predictions.json": "f1d26201ffac81fdd7415ac325165807c0f721f841ec5608636ba415879c938e"
   },
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-5-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdB02-5-3.json"
   ]
  }
 ]
}
```

## What I checked (plain English)

**Setup.** Fleet-mirror clone at `/fast/scratch/hyaku/tameshi-r32-seats/ColdB02/fleet/tameshi-shokunin`, detached at `a4f718138bdad20de741faeca57891645e5a64d9`; whole-page SKILL.md sha256 matches the given `23818731...7d35a`. All reads and runs happened inside the clone or my scratch dir; every traced command ran under `tools/trace-inputs.py` with literal receipt names; the four L1-appended files (SCORECARD.md, LOG.md, round-21 coldread ledger, round-32 lesson) were never opened.

**Section 4 (lines 1938–2103, record).** Verified against the pinned bytes: (1) the Round-28 correction's exact anchors — `.ufo/evidence/round-21/c2-count.py` line 19 hardcodes `FLEET = Path("/home/vgpnk/Projects/shokunin")` and line 52 reads `show(FLEET / frozen["repo"], ...)` — so `round21-measure --claim c2`/`--selftest` genuinely read live fleet objects from a clone; (2) `wave-route-mix.py` line 19 `DEFAULT_CONFIG = Path.home() / ".omp/agent/config.yml"`; (3) six registered selftests executed green under the collector and match their registry rows verbatim (receipt-window 20/20, receipt-measure 10/10 printing `RECEIPT_MEASURE_RUNNER_SHA256: a67bffa9...` plus the separate frozen instrument sha `f34dc233...`, env-diff 9/9, wave-accounting 8/8 + 16 extra, command-binding 44/44, registry-replay 10/10); (4) `--check` omission confirmed (wrapper docstring + selftest case "frozen --check spelling remains unsupported") and `runner_sha256` recorded separately; (5) contract.json staged==installed digests equal the live tool bytes (`f03ae7e9...`); (6) cited persisted files exist, and the ones opened check out: c2-contract has 9 surfaces / 7 required profiles, round-22 `expected.json` bundle pin `dfb1027f...` equals the actual sha256 of `bundle.json`, routemix receipt `.ufo/waves/round-21/routemix-spec1.json` has `"ok": true` with 28/71 max share; (7) replay receipt `live-dependent.json` shows exactly rows 43, revision_pinned 41, live rows `pin-disposition-read` and `verify-round15`; (8) registry.json has 49 active rows, the three round-23 rows superseded append-only by the r24 rows, and `registry-replay-selftest` expecting 10/10; (9) source pointers resolve: `corpus/lessons/round-20.md` (round-20 receipt-window recipe, S049 used-by transition), QUALITY41 (`corpus/README.md:314`), QUALITY43–44 (round-21 lesson), QUALITY45 (round-22), QUALITY46 (round-23), QUALITY48 (`corpus/QUALITY.md:506`), S049/S089 rows in SOURCES.md.

**Section 5 (lines 2104–2131, record).** Verified: kumitate `scripts/cite-check.mjs` at `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` has blob sha256 `40573448...c10c9f`, 2537 lines, mode 100755 (all three exact, via read-only git cat-file in the fleet-mirror sibling); commit `622d31d` exists, is titled "pre-register claims ... spec and predictions before any mutant run" (2026-10-22 10:01:47Z, before MUTATE_DATE 10:02:07Z), and its spec+predictions bytes are byte-identical to the copies at the read rev (same sha256s); `sweep.txt`/`results.tsv` show control GREEN `62/62 cases passed (hermetic)` and exactly 10 defects, 5 killed / 5 survived (50%), matching `TABLE_CITECHECK` at `tools/mutate-and-run.sh:631` and the ten pre-registered predictions (10/10 verdict predictions held); `control.out` and `S_EMPTY_GUARD.out` confirm the 62-case hermetic group and the survivor behavior; the entry `corpus/knowledge/mutation-case-kumitate-cite-check.md` documents the four suite holes with hermetic witnesses, the S_EMPTY_GUARD equivalence argument (co-extensive guard; CriticEquivalence.md exists), S089's "cannot find or mark equivalents automatically", and the leg staying hermetic-only; `.ufo/waves/round-26/w1/ProbeIntegrations.md` states verbatim that the `--integrations` group kills none of the five and is red at the pristine pin on live trees. The live `--regression` replay reproduced the first of nine legs exactly (at the pinned runner sha `a7d3f2dd...2eb9`) before hitting my 6-minute box; the full-run expected output (`REGRESSION_CASE js-cite-check: PASS`, `cases=9 passed=9`) is attested by the retained `regression-worktree.stdout` receipt of a complete run at the landed runner `a08e85c`. Both traced reads for this section are receipted; the timed-out regression attempt is disclosed above with no receipt.

**Residual risk.** The two coldread selector probes and the wave-route-mix gate were source-verified, not executed; the 9-leg regression was not re-run to completion inside the time box; existence-only checks cover a handful of persisted-value cells. No wrong or unverifiable statement was found in either section. No tool installs were made. No processes I started remain running (checked `ps` for my scratch tree).

COLDREAD ColdB02: verified-record, verified-record
