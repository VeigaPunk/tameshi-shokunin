# Read02 — cold read of `## Standing rules` (SKILL.md:17-29) at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read02", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [{"start": 17, "heading": "## Standing rules", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [], "commands_executed": ["python3 tools/trace-inputs.py --root /tmp/Read02-7YND/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read02-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" PROVINCE.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md"],
    "opened": ["PROVINCE.md", "corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md"],
    "inputs": {"PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be", "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548", "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0"},
    "external_inputs": {}, "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read02-1.json"]}]}
```

## What I checked

Classified the section as **record**: it states standing rules with pointers; it names no command to run. Read it fresh in a detached clone at 2227d833 (SKILL.md sha256 matched the given page hash; `git status --porcelain` clean). Opened all three cited artifacts under the trace collector (receipt rev = read_rev, exit 0):

- **"Read-only substrates unless PROVINCE.md declares a write surface"** — PROVINCE.md at this rev declares sibling gates as read-only primary surfaces, "never edits a sibling's gate code (read-only probes)", "Out of province → report, never absorb"; it declares no substrate write surface. Consistent.
- **Scratch namespace `/tmp/<lane>-r<round>-<n>-*/` with both cited anchors** — `mutation-case-kimi-census.md:4-7` reads "every mutant is a copy under `/tmp/tameshi-r2-1-work/` … no fleet file was written" and `mutation-case-kagi-census.md:4-6` reads "every mutant is a copy under `/tmp/tameshi-r3-1-work/` … the kagi tree was not written". Both scratch dirs match the stated namespace shape (`tameshi-r2-1-work`, `tameshi-r3-1-work`), and both notes' Reproduce sections keep `mutant-*` plus `evidence/` under the same root, supporting "kept every mutant + evidence there". Cited line numbers are exact at this rev.
- **"Secrets shape-only, never content-read"** — corroborated in the cited notes themselves: kimi-census:5-6 "No live `~/.kimi-code` path was read"; kagi-census:6-7 "no secret file was content-read (kagi's 0600 `stamps.tsv` appears in directory listings by name only)".
- **"Every claim: measured anchor … O/I/U stay separate"** — both notes carry explicit O/I/U anchor labels and separate Unknowns sections.
- **"Errata append-only; rejections kept"** — both notes carry "Calibration and errata (append-only)" sections that record the authors' own wrong expectations (E1 in each) plus appended errata blocks (kimi round-5 E2, kagi R21) explicitly scoped as append-only, nothing above edited.

The exception files (SCORECARD.md, LOG.md, `.ufo/evidence/round-21/coldread/ledger.json`) are not cited by this section and were never opened, under the collector or by path. No sibling-repo file was opened via `git show`, so `external_inputs` is empty. Auxiliary (non-collector) commands: the fleet-mirror clone/checkout setup, rev-pinned `git show | sha256sum` hash confirmation (all three hashes equal the receipt's `inputs`), heading-line listing, and ranged line verification; none touched the live lane, and no git write or `jj` command was run anywhere. No tools were installed or upgraded for this task.

COLDREAD Read02: verified-record
