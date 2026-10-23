# ColdA03 — wave 2 cold read (sections 7, 8, 9)

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdA03", "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a", "read_rev": "2da841bd9913a2037d2bf612793382e572c9d205",
  "sections": [
    {"start": 1855, "heading": "## Input-keyed cold-read credit — round 17", "class": "instruction", "verdict": "gap-minor",
     "blocking_gaps": [], "wrong_expectations": [],
     "minor_gaps": ["recipe steps 3-4 (assemble.py, ledger commit) were not executed: assembling and committing are outside this leaf seat's bounds (no git writes); the recipe's named step-4 command python3 .ufo/evidence/round-19/coldread/measure.py --rev 2da841bd9913a2037d2bf612793382e572c9d205 ran under the trace collector from the clone and exited 0 with a full measurement at the read rev (inputs: round-18/measure.py, round-19/coldread/measure.py; no live-lane reads; overrides_used false, trace_gate strict)"],
     "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-16-verifier-spotcheck.md corpus/knowledge/input-keyed-coldread-credit.md corpus/SOURCES.md", "python3 .ufo/evidence/round-19/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r31-seats/ColdA03/fleet/tameshi-shokunin --rev 2da841bd9913a2037d2bf612793382e572c9d205"],
     "opened": ["corpus/lessons/round-16-verifier-spotcheck.md", "corpus/knowledge/input-keyed-coldread-credit.md", "corpus/SOURCES.md", ".ufo/evidence/round-18/measure.py", ".ufo/evidence/round-19/coldread/measure.py"],
     "inputs": {"corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37", "corpus/knowledge/input-keyed-coldread-credit.md": "0c45dccb4dfa78cdfd2dfddc59132d1e636ed0d548abcb9528d1b1aa21fd0636", "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741", ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37", ".ufo/evidence/round-19/coldread/measure.py": "4c9c74ca3bb0d85121d6bd3e4deeafe4474374d0a67becf9a9c9fe4c0d42f2f7"},
     "external_inputs": {},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA03-7-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA03-7-2.json"]},
    {"start": 1938, "heading": "### Round-20 gate/probe registry — frozen receipt instruments", "class": "record", "verdict": "verified-record",
     "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
     "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-20.md corpus/QUALITY.md corpus/SOURCES.md", "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/receipt-window.py tools/receipt-measure.py .ufo/evidence/round-20/contract.json .ufo/evidence/round-20/final/receipts.json .ufo/evidence/round-20/stage/measure.py .ufo/evidence/round-20/coldread/measure.py .ufo/evidence/round-20/public-cli-cases.json"],
     "opened": ["corpus/lessons/round-20.md", "corpus/QUALITY.md", "corpus/SOURCES.md", "tools/receipt-window.py", "tools/receipt-measure.py", ".ufo/evidence/round-20/contract.json", ".ufo/evidence/round-20/final/receipts.json", ".ufo/evidence/round-20/stage/measure.py", ".ufo/evidence/round-20/coldread/measure.py", ".ufo/evidence/round-20/public-cli-cases.json"],
     "inputs": {"corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6", "corpus/QUALITY.md": "6cbf9cf7a9117a747be356f7ac5ed8288c8609195205bcca427809b4d96804ac", "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741", "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc", "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa", ".ufo/evidence/round-20/contract.json": "9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715", ".ufo/evidence/round-20/final/receipts.json": "4186b44e6f5ef95aeb39768e5b9d8a0e6953283961bcc009733dbbcde48cb5d6", ".ufo/evidence/round-20/stage/measure.py": "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d", ".ufo/evidence/round-20/coldread/measure.py": "48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13", ".ufo/evidence/round-20/public-cli-cases.json": "590df60420a60bec1f6dddad6b5eaf34a5d700cdd86c5cf231b1ef8f5a3b27b2"},
     "external_inputs": {},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA03-8-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA03-8-2.json"]},
    {"start": 2104, "heading": "## Ninth recorded case — round 26", "class": "record", "verdict": "verified-record",
     "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
     "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-26/cite-check/sweep/sweep.txt corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/QUALITY.md corpus/SOURCES.md tools/mutate-and-run.sh", "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" scripts/cite-check.mjs"],
     "opened": [".ufo/evidence/round-26/cite-check/sweep/sweep.txt", "corpus/knowledge/mutation-case-kumitate-cite-check.md", "corpus/QUALITY.md", "corpus/SOURCES.md", "tools/mutate-and-run.sh"],
     "inputs": {".ufo/evidence/round-26/cite-check/sweep/sweep.txt": "957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893", "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e", "corpus/QUALITY.md": "6cbf9cf7a9117a747be356f7ac5ed8288c8609195205bcca427809b4d96804ac", "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741", "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"},
     "external_inputs": {"kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"},
     "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA03-9-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA03-9-2.json"]}
  ]}
```

## What I checked

Fleet-mirror clone at read_rev `2da841bd9913a2037d2bf612793382e572c9d205` (SKILL.md sha256
matches the pinned `2381873162…7d35a`). All six trace receipts have `rev == read_rev`, argv
matching the command after `--`, and empty `live_lane_reads`; the second section-9 trace
(ColdA03-9-2) had to fail because `scripts/cite-check.mjs` is not a tameshi-shokunin lane
file — the pinned script lives in the kumitate sibling repo, so I verified it as an external
git-object read (`kumitate-shokunin@1205c66…:scripts/cite-check.mjs`, sha256
`40573448…c10c9f`, mode 100755, 2537 lines), which matches the section's pin exactly.

Section 7 (instruction, gap-minor): sources opened — round-16 verifier spot-check §2/§6
route R16-C2b/C2c, `input-keyed-coldread-credit.md` exists, S058/S059/S060/S064 rows carry
the quoted teaches. I executed the recipe's named step-4 command, round-19 `measure.py` at
the read rev from the clone, under the trace collector: exit 0, overrides_used false, no
live-lane reads. The recipe's assemble/commit steps were not executed because they are
outside a leaf cold-read seat's bounds (no git writes); that is the only gap.

Section 8 (record, verified-record): opened the round-20 lesson, QUALITY41, S049, and all
instruments/evidence. Identity checks are byte-exact: `tools/receipt-window.py` == frozen
`f03ae7e9…` and `stage/measure.py` == frozen `f34dc233…` (both equal their contract
frozen/installed shas), the four historical instrument shas match the contract and the
runner's HISTORICAL table, the six-item population/`meas_sha256` wrapper behavior matches
the source (ITEM_IDS, no `--check`, FROZEN_MEASURE_SHA), the 20-case selftest tally in
code matches the lesson, and `public-cli-cases.json` is an independent synthetic fixture set.

Section 9 (record, verified-record): sweep.txt shows 10 defects, 5 killed / 5 survived,
kill-rate 50%, pristine control matching the pinned sha; pre-registration commit 622d31d
(10:01:47Z) predates the sweep (10:02:07Z) and adds spec + predictions; committed
`regression-worktree.stdout` contains `REGRESSION_CASE js-cite-check: PASS` and
`REGRESSION: PASS (cases=9 passed=9 …)`; wave-1 probes exist for all five survivors —
four DISTINGUISHED hermetic off-suite witnesses (S_OOR_EDGE, S_STRICT, S_USAGE,
S_PIN_INCLUDES), S_EMPTY_GUARD EQUIVALENT with a structural proof (CriticEquivalence), and
the integrations probe shows none of the five killed and the group red at the pristine pin
on live trees, consistent with "leg stays hermetic-only". The failed trace was the wrong-repo
attempt; it is listed for honesty but adds no inputs.

COLDREAD ColdA03: gap-minor, verified-record, verified-record
