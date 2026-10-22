# Read02B — cold read, round 28 wave 1

Section: `### The report shape — what the opting-in lane receives` (SKILL.md:883–898 at b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read02B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [{"start": 883, "heading": "### The report shape — what the opting-in lane receives", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [], "commands_executed": ["python3 tools/trace-inputs.py --root /tmp/Read02B-7kzg/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read02B-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-mado-verify.md"], "opened": ["corpus/knowledge/mutation-case-mado-verify.md"],
  "inputs": {"corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3"}, "external_inputs": {}, "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read02B-1.json"]}]}
```

Checked (all line numbers at b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a):

- Class: record — the section states facts about the mado-run report shape with pointers; nothing tells the reader to run a command.
- The only cited file, `corpus/knowledge/mutation-case-mado-verify.md`, exists in the lane and was opened whole under the trace collector (exit 0, receipt rev = read_rev).
- Pins claim: the note records tool sha256 `597e1419…6331b` printed as `MUTATE_TOOL`/`REGRESSION_TOOL` (lines 18–21), target sha256 `d7edaab4…d0e13`, and the suite line `bash "$MUTANT" --selftest` (lines 52, 287) — consistent with "supplied by the lane in the note (the tool does not print them)" for line count / suite command / clause map.
- Kill-rate table claim: note §1 (lines 75–89) is control + one row per defect D1–D9,R1 with id, clause, exit, verdict, and failing-assertion labels; line 92 says the kill mechanisms are "verbatim from `evidence/D*.out`" — matches.
- Survivor probes claim: probe preamble (lines 103–106) says each probe "constructs an input the suite's fixtures do not"; P3 (line 110) and P8 (line 113) use the clean fixture, and lines 274–275 state `probe/fixture-A` is "the suite's own clean fixture" rebuilt byte-identically — matches `(:103-115, :110, :113, :274-275)`.
- Restore proof claim: line 58 quotes `MUTATE_RESTORE: OK (target-sha256 before=d7edaab4…d0e13 after=d7edaab4…d0e13 pristine-sha256=d7edaab4…d0e13)` — sha before = after, matches.
- "Only fleet file the run writes": lines 8–9 state exactly that — matches `(:8-9)`.
- Reproduce block `(:262-293)`: §9 starts at line 262, the commands block runs 281–293 and records the commands only; the spec lives under `/tmp/w6-tameshi-mado-verify/` (scratch), the edit table lists all 10 mutants but the kill table's survivor detail relies on per-defect evidence under /tmp — consistent with "does not rebuild the sweep from the lane". The round-27 Read10 cold read exists in the round-27 ledger records (a Read10 report at `.ufo/waves/round-27/w1/Read10.md` was ledgered).

Every claim I could open resolves as written; no blocking or minor gaps found. No tools installed (none needed); pacman untouched.
COLDREAD Read02B: verified-record
