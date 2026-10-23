# TameshiR29.Read01B — cold read, SKILL.md:131-245

Seat: Read01B. Claim served: C1 (calibration repair). Clone detached at
9f3084bc60ad56aac01e4556ef4c7653df2f65e5; SKILL.md sha256 c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read01B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 131, "heading": "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence", "class": "instruction", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
    "The literal `SELFTEST: FAIL (1/16 cases)` is not inside the cited range mutation-case-kagi-census.md:82-103 — the note prints the bad-case line but never the epilogue. Verified live on the pinned bytes instead: the B1 mutant run emitted exactly `SELFTEST: FAIL (1/16 cases)`, matching the gate's printf at surface-census.sh:848.",
    "Run-together typography inside the section: `exit0` (SKILL.md:146), `denominators43 and16` (:193), `Round2:7.0s for11 runs, nodev24.21.0` (:241), `a280s bound` (:242), `at204-205`/`at203-204` (:244).",
    "Step 9 says 'Re-run step 2's checks' but enumerates only sha256/size/mtime/`git status`; step 2's record list also includes path, line count and repo revision (the notes record no after-repo revision, as the section itself states). Wording imprecision, not a wrong fact.",
    "Step 5 presents 'both lanes' drivers' as the --check model without carrying the caveat that they were unversioned scratch scripts that do not rebuild after scratch loss (the caveat exists only in kagi erratum R21 and Restore item 6 elsewhere on the page).",
    "The section never names the maintained instrument tools/mutate-and-run.sh; its conventions differ from this recipe — the tool divides kill rate by all spec defects including inconclusive (:568) and marks KILLED on non-zero exit alone (:548), while steps 6-7 exclude inconclusive runs and require count+token adjudication (standing note of round-27 seat Read03)."
  ],
  "commands_executed": [
    "python3 -c \"import sys\\nfor p in sys.argv[1:]: sys.stdout.write(open(p).read()[:200000])\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/gates-survey-kumitate.md corpus/knowledge/gates-survey-kagi.md corpus/README.md",
    "bash /tmp/tameshi-r29-b1-work/run-sweep.sh",
    "bash -c \"git -C /tmp/Read01B-5ySQ/fleet/kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh > /tmp/tameshi-r29-b1-work/pin-via-git-show.check\""
  ],
  "opened": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/knowledge/gates-survey-kumitate.md", "corpus/knowledge/gates-survey-kagi.md", "corpus/README.md", ".ufo/waves/round-27/w1/Read03.md", "tools/mutate-and-run.sh", "tools/trace-inputs.py"],
  "inputs": {
    "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
    "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
    "corpus/knowledge/gates-survey-kumitate.md": "3dca7a1a5c621bf0ec75948d0836839dec98651673bb2987861d9aa122579b0e",
    "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
    "corpus/README.md": "91c782f6803a30f26734793f73733e58bb6afc117965e06cbe4c625b88fd3c67",
    ".ufo/waves/round-27/w1/Read03.md": "cd90435cf142a2912b10efb3c683908f2747e482abf84d211f6e4242b30d96bc",
    "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
    "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
  },
  "external_inputs": {
    "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
    "/tmp/tameshi-r29-b1-work/run-sweep.sh": "d150d2529041d4607dabdd094023fda000bce59fc475848de80061db77ffb941",
    "/tmp/tameshi-r29-b1-work/pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    "/tmp/tameshi-r29-b1-work/evidence/control.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    "/tmp/tameshi-r29-b1-work/mutant-B1.sh": "1d0e511055a74b11307d827913d264d87f43b93e21fdb679556439d96a4ca3cc"
  },
  "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read01B-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read01B-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read01B-3.json"
  ]}]}
```

## What I checked

Class: `instruction` (ten numbered steps with literal commands). Verdict `gap-minor`.

Executed the recipe end to end on the pinned bash leg inside
`/tmp/tameshi-r29-b1-work/` (standing scratch namespace): materialized the
committed blob `kagi-shokunin@fecee8743…:corpus/surface-census.sh` (sha256
`275d8294…53009f`, 44212 B, 886 newlines, last byte `c` — the note's pin and the
"887th line carries no trailing newline" claim both confirmed), pinned the
artifact with sha256/size/lines/mtime/rev/`git status --porcelain` (empty),
`cp -p` to scratch plus `sha256sum`/`cmp` re-verify, ran the step-5 uniqueness
check (`count=1`, first-line match `[[ ${#SCAN_DIR[@]} -eq 0 ]] && return 0`,
literal `all unique`), ran the control (`SELFTEST: PASS (16 cases)`, exit 0,
`skip-case 15/16` substrate-absent — the enumerated-skip claim reproduced live),
applied defect B1 as one exact `str.replace` (mutant sha `1d0e5110…` ≠
pristine), and ran the mutant: `bad-case 05 undeclared-file want exit=1
token=SURFACE UNLISTED got exit=0` + `SELFTEST: FAIL (1/16 cases)` exit 1 —
exactly the section's bash grammar and B1's recorded row. Restore proof held:
sha256/size/mtime identical, `cmp`-identical, porcelain clean. Wall ~7.2 s,
bound 280 s.

Cross-checked every cited line range in `mutation-case-kimi-census.md` and
`mutation-case-kagi-census.md` (controls 43/43 and 16-cases; pin records at
:13-16/:13-17; driver `--check` at :22-25/:44-47; evidence fields at
:26-28/:48-49; kill rates 8/10=80% with 7.0 s/11.0 s and 300 s/280 s bounds;
enumerated denominators held; D2/D10 and B5/B10 survivor probes at :82-99,
:111-114, :118-122, :251-253; failing-case labels at :59-76/:82-103; E1
calibration blocks at :183-191/:184-191; U5 lines at kimi 204-205 and kagi
203-204 — all exact). `kumitate n/m pass + VERDICT:` at
gates-survey-kumitate.md:19-31 confirmed (six rows incl. `KIMI_CENSUS_SELFTEST:
43/43 pass`). The dirty-pin re-pin story (corpus/README.md G-R2-1 row;
gates-survey-kagi.md §10/Errata-round-2 blocks at :503/:545/:557) confirmed.
SKILL.md:377-378 self-anchor resolves to the endpoint-identity sentence; the
"corrected in round 27, seat Read03" claim is real (Read03.md records the
wrong-expectation verdict and the exact rewording now present). "Two seats"
executed the recipe in round 16 = CR04a/CR04b (Errata table row for snapshot
lines 134-135). The current kagi working tree carries different bytes
(`1e697b01…`), so the committed-bytes pin remains load-bearing.

Minor gaps are listed in the JSON: one unanchored literal (the FAIL epilogue is
real — verified live — but not inside the cited range), run-together
typography, step 9's shorter re-run checklist vs step 2's record list, the
unflagged unversioned driver caveat, and the recipe's silence on the maintained
instrument whose verdict/kill-rate conventions differ (round-27 standing note).

COLDREAD Read01B: gap-minor
