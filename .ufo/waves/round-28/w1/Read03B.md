# Read03B — cold read, SKILL.md ## The leg ledger — replay, receipt, and how it is read (round 7, measured)

Independent second read of SKILL.md lines 921–1009 at b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a (page sha256 c46ec02e…36d6). Class: record — it states the ledger's receipts, pins, exit map and reading discipline with pointers; no reader-facing run instruction beyond the record's own cites. I ran the record reader over every cited lane file plus the `--selftest` arm the section names, both under tools/trace-inputs.py in a detached /tmp clone (fleet siblings symlinked, never written).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read03B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [{"start": 921, "heading": "## The leg ledger — replay, receipt, and how it is read (round 7, measured)", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
    "Stale line anchors: ':1104-1175' cited for git-show materialization now sits inside regression_specs/comments; the materialize+validate code is :1184-1227. ':1159-1160' cited for REGRESSION_PIN is a comment line; the printfs are :1228-1231.",
    "':1273-1294,1364-1384' cited for workdir/exits spans the defect-diff loop and the dispatch head; mktemp allocation is :1357-1359, removal :1453-1458, exit codes 0/1/2 at :1459/:1443/:1449 (the semantic claims all hold).",
    "':1384-1450' cited for failure aggregation is mostly the nine leg dispatches (:1384-1428); the aggregation loop itself is :1430-1459.",
    "Negative-run scratch '/tmp/w7-tameshi-1/flip-run.out' is gone (ephemeral /tmp as named), so the doctored-table FAIL example is unverifiable on-host; the quoted REGRESSION_DEFECT/FAIL formats match the code at :1283-1297,:1326.",
    "r7-1 tool cite '9f1d3c3' (blob cf41efaa…) resolves; '597e1419…' inside the cited plan/ledger text is not a commit object at this rev (it is the older tool blob sha). Both are cited as tool revisions elsewhere, so no behavior claim is affected."
  ],
  "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md plans/round-7.plan.md tools/trace-inputs.py .ufo/evidence/round-26/cite-check/cite-check.defects.spec .ufo/evidence/round-18/sources-check/sources-check.defects.spec", "bash tools/mutate-and-run.sh --selftest"],
  "opened": ["tools/mutate-and-run.sh", "corpus/knowledge/fleet-kill-rate-ledger.md", "plans/round-7.plan.md", "tools/trace-inputs.py", ".ufo/evidence/round-26/cite-check/cite-check.defects.spec", ".ufo/evidence/round-18/sources-check/sources-check.defects.spec"],
  "inputs": {"tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e", "plans/round-7.plan.md": "49cd55fd0efaf892c281ec90538310cd5691af2af4ab1270c9945146fdc0fcec", "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4", ".ufo/evidence/round-26/cite-check/cite-check.defects.spec": "969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208", ".ufo/evidence/round-18/sources-check/sources-check.defects.spec": "c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91"},
  "external_inputs": {"tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75", "tameshi-shokunin@58e5d53d6a638fb72042d1f6607b24018aa299a8:tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read03B-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read03B-2.json"]}]}
```

What I checked, against the tree at b05d2ee and the pinned blobs:

- **Leg count and kill-rates**: the script header (:83-95) names nine legs "r26 nine" with the exact rates the section lists (js-kimi-census 8/10, bash-surface-census 8/10, bash-tsukuroi-census 6/10, bash-mado-verify 4/10) plus five more; pins/revs/tables live at :603-629 (claim ":603-629" — exact), nine dispatches :1384-1428 (claim exact), aggregation loop :1430-1459 emitting `REGRESSION: PASS|FAIL|SETUP` with exits 0/1/2.
- **Git-materialization claim**: `regression_case` materializes via `git show <rev>:<path>` into the case workdir, checks mode, emits `REGRESSION_PIN … source=git repo=… rev=… path=… mode=… sha256=…`, refuses SETUP on missing repo/rev/blob or pin mismatch (:1184-1240); later legs still run (statuses aggregated :1430-1450) — the section's claims hold, but its ":1104-1175" and ":1159-1160" anchors are stale (see minor gaps).
- **Workdir/exit discipline**: mktemp `/tmp/tameshi-r4-2-regression.XXXXXX` after prereq checks, `auto=1` removed on PASS unless `--keep`, kept on FAIL/SETUP, caller `--workdir` never removed — all confirmed at :1355-1363, :1442-1458; the cited anchor block is off (minor gap).
- **Ledger file**: `fleet-kill-rate-ledger.md` ends at the "Round 18 — eighth row appended" block (4 §1 rows + 2 ER-2 + r16 + r18 = 8 rows; no round-26 row) — "eight rows since its round-18 block" is accurate.
- **Revision cites**: `9f1d3c3` resolves (r7 commit, 2026-10-14); its tool blob hashes to `cf41efaa8be5f52d…` exactly as the section and ledger name; `:72-109` there = the four-leg `--regression` comment, `:511-522` = the four legs' PIN/REV/TABLE lines. Round-18 build commit `58e5d53` puts the recorded tables exactly at `:597-620` as claimed.
- **TABLE sizes**: TABLE_CHECKLIST has 15 entries (D=15 for checklist-run), all other current tables have 10 — matches "D is 15 for checklist-run, 10 for other current legs".
- **Selftest arm (named in item 7)**: `bash tools/mutate-and-run.sh --selftest` ran under the collector in the clone → `MUTATE_SELFTEST: 97/97 pass` / `VERDICT: PASS`, rc 0. The section's "67/67" is qualified to `cf41efaa…` (that blob has 67 reachable `st` cases) and the ledger's ER-4 records that count, so the qualified claim is true; the listed arms (git-materialized exact replay, drifted tree immovability, pin-mismatch/unresolvable-rev SETUP, loud flip failure) are all present as selftest cases. Fixture band `killed-delta<=1 flips<=1` = BAND_KILLED/BAND_FLIPS=1 (:186-187), exercised by selftest only — confirmed.
- **plans/round-7.plan.md:11-15** does describe the attestation leg ("ATTESTED read-only… the lane operates; tameshi attests"), supporting item 6.
- **Spec files cited in the header** (`.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`) exist and are tracked at this rev.

No blocking gaps, no wrong expectations: every checkable factual claim is correct at this revision or correctly pinned to the revision it names; the faults are stale line anchors plus one dead ephemeral path — listed above.

COLDREAD Read03B: gap-minor
