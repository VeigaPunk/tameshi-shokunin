# ColdA02 — cold reads of SKILL.md sections 4, 5, 6 at bb681566b18211adf8ae9c28df91e17678e3f545

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdA02", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
  "sections": [
    {"start": 858, "heading": "### The boundaries — what a service run is not", "class": "record", "verdict": "verified-record",
      "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
      "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/fleet-suite-census.md tools/mutate-and-run.sh"],
      "opened": ["corpus/knowledge/mutation-case-mado-verify.md", "corpus/knowledge/fleet-suite-census.md", "tools/mutate-and-run.sh"],
      "inputs": {"corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
                  "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
                  "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"},
      "external_inputs": {},
      "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA02-4-1.json"]},
    {"start": 921, "heading": "## The leg ledger — replay, receipt, and how it is read (round 7, measured)", "class": "record", "verdict": "verified-record",
      "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
      "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/fleet-kill-rate-ledger.md tools/mutate-and-run.sh"],
      "opened": ["corpus/knowledge/fleet-kill-rate-ledger.md", "tools/mutate-and-run.sh"],
      "inputs": {"corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
                  "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"},
      "external_inputs": {"tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75",
                          "tameshi-shokunin@58e5d53d6a638fb72042d1f6607b24018aa299a8:tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"},
      "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA02-5-1.json"]},
    {"start": 933, "heading": "### Using the ledger", "class": "instruction", "verdict": "executed-ok",
      "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
      "commands_executed": ["bash tools/mutate-and-run.sh --regression"],
      "opened": ["tools/mutate-and-run.sh"],
      "inputs": {"tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"},
      "external_inputs": {},
      "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA02-6-1.json"]}
  ]}
```

What I checked, in plain terms:

- Section 4 (line 858, record): every named citation resolves and says what the
  bullet claims. `fleet-suite-census.md:288-291` is the scope paragraph
  (single-edit mutants, hermetic suites, per-revision/per-host; "coordinated
  edits" is matrix column F at census :185-187/:341). `tools/mutate-and-run.sh:36-38`
  says the target is never written and the before/after sha256 is the restore
  proof. In `mutation-case-mado-verify.md`: :57-59 carries the target sha pair
  and `MUTATE_RESTORE: OK`; :175-176 and :187-189 are the 40 % / 10-of-10
  pre-registration lines; :229-230 is the sensitivity clause; :237-238 and
  :240-260 are the unabsorbed recommendations; :17-23 is incident I1 with the
  `b56c6e57` re-pin; :8-9 says the note is the only fleet file the run writes.
  The two "corrected in round 27 after the cold read of seat Read09/Read10"
  parentheticals are backed by `.ufo/waves/round-27/w1/Read09.md` and
  `Read10.md` existing in the lane.

- Section 5 (line 921, record): the nine-leg inventory at
  `tools/mutate-and-run.sh:83-96` lists exactly the four legs named with the
  same kill rates (8/10, 8/10, 6/10, 4/10) plus legs 5-9. The historical cite
  `tools/mutate-and-run.sh@9f1d3c3:72-109` holds: `9f1d3c3` resolves to
  `9f1d3c339a7094968041c7708a65dbf7eab9fae6` (the r7 commit) and lines 72-109
  there are the four-leg ledger listing; `:511-522` are the PIN/REV/TABLE
  anchors. At the round-18 commit `58e5d53d6a638fb72042d1f6607b24018aa299a8`
  the recorded tables do sit at `:597-620` (eight legs, matching "eight since
  round 18"). `corpus/knowledge/fleet-kill-rate-ledger.md` carries the per-gate
  rate rows (rows 1-4 at :45-48, rows 5-6 at :276-277, legs 7-9 at
  :410/:432 plus the round-26 cite-check block) — the nine rates match the
  inventory. The live `--regression` run (section 6's trace) printed
  `REGRESSION_EXPECT` with the same nine recorded kill-rates.

- Section 6 (line 933, instruction): ran `bash tools/mutate-and-run.sh
  --regression` from the clone under the trace collector. It allocated a fresh
  `/tmp/tameshi-r4-2-regression.XXXXXX` after the documented prerequisite
  checks, materialized all nine legs from their repos' git object stores
  (`REGRESSION_PIN … source=git … sha256=` matching the PIN_ constants),
  ran each as a sub-sweep, printed one `REGRESSION_SWEEP`/`REGRESSION_TABLE`/
  `REGRESSION_CASE` per leg, closed with `REGRESSION: PASS (cases=9 passed=9;
  ledger legs exact: killed-delta<=0 flips<=0)` with `match=N/N … flips=0` on
  every leg (D=10, D=15 for checklist-run), removed the auto-allocated root on
  PASS as documented, and exited 0 (receipt `exit: 0`, `rev:
  bb681566b18211adf8ae9c28df91e17678e3f545`). Wall time about 339 s, inside the
  6-minute budget. The anchors cited at :603-629 (pins/tables), :1384-1428
  (nine `regression_case_git` dispatches), :126-136 (exit map and the r30
  case-tally note) all check. The SETUP/refusal and `--keep` branches were not
  exercised — only the documented happy path is claimed as verified.

No installs were needed (strace 7.2, node v24.21.0, bun 1.4.3 already present).
The clone stayed detached at `bb681566b18211adf8ae9c28df91e17678e3f545`; no git
write commands were run anywhere.

COLDREAD ColdA02: verified-record, verified-record, executed-ok
