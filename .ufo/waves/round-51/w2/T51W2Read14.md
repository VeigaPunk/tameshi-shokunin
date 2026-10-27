# T51W2Read14 — cold-read rekey row: SKILL.md `### Gate/probe registry`

- Rev read: `6d8c11e378aa90b12650808e1b79270742935f15` (base `9962033fd7a75aa2f2847e979dd687a5d28505a1`), lane `tameshi-shokunin`. All reads via `git show <rev>:<path>`; no lane/fleet/sibling mutation. Empirical runs only inside `git clone --shared` fixture at scratch `/fast/scratch/hyaku/tameshi-r51/T51W2Read14/` (toplevel asserted before use; deleted before yield).
- Heading re-resolved at CAND: `### Gate/probe registry` at line 1499; section = lines 1499-1547; next heading `### Round-13 gate/probe registry` at 1548; parent `## Repeated controls and gate registry — round 12` at 1496.
- Section bytes are IDENTICAL base→CAND (`diff` of extracted ranges: empty). The +35 SKILL.md lines of this candidate are elsewhere; this section neither moved nor changed.
- Old READERS_JSON and the w1 fixture list were not trusted; every pointer below was re-derived from the section text at CAND and checked against CAND bytes.

## Row for reads.json

```json
{
  "seat": "T51W2Read14",
  "rev": "6d8c11e378aa90b12650808e1b79270742935f15",
  "base": "9962033fd7a75aa2f2847e979dd687a5d28505a1",
  "file": "SKILL.md",
  "heading": "### Gate/probe registry",
  "heading_line_cand": 1499,
  "section_lines_cand": "1499-1547",
  "next_heading": "### Round-13 gate/probe registry @1548",
  "section_bytes_equal_base": true,
  "verdict": "holds",
  "pointers": [
    {"raw": "python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` or `--snapshot DIR", "file": "tools/repeat-control.py", "ranges": "14,50,143,714,878-881", "verdict": "holds", "excerpt": "--snapshot DIR: read-only validation of a committed frozen control snapshot."},
    {"raw": "0 clean; 1 failed; 2 and 64 could-not-evaluate", "file": "tools/repeat-control.py", "ranges": "42-45,127", "verdict": "holds", "excerpt": "controls_match 0 · controls_mismatch 1 · baseline_nonzero 2 · command_unavailable 2 · snapshot_tampered 2 · setup_error 2 · invalid_usage 64 … and invalid_usage are could-not-evaluate"},
    {"raw": "python3 tools/repeat-control.py --selftest", "file": "tools/repeat-control.py", "ranges": "592-865", "verdict": "holds", "excerpt": "ran in fixture at CAND: exit 0, 'SELFTEST: PASS (29 cases)'"},
    {"raw": ".ufo/evidence/round-12/ControlGate/expected.json, mismatch/expected.json", "file": ".ufo/evidence/round-12/ControlGate/expected.json; .ufo/evidence/round-12/ControlGate/mismatch/expected.json", "ranges": "-", "verdict": "holds", "excerpt": "both in tree at CAND; --snapshot on each returned 0 (controls_match) and 1 (controls_mismatch) respectively in fixture"},
    {"raw": "literal expected IDs/exits in tool selftest", "file": "tools/repeat-control.py", "ranges": "784-848", "verdict": "holds", "excerpt": "snapshot_case(\"snapshot-pass\", snap_stable, \"controls_match\", 0) … (\"snapshot-tamper-byte\", tamper_byte, \"snapshot_tampered\", 2)"},
    {"raw": "fresh caller-selected DIR; isolated /tmp/tameshi-r12-* selftest; snapshot read-only", "file": "tools/repeat-control.py", "ranges": "50,597", "verdict": "holds", "excerpt": "tempfile.mkdtemp(prefix=\"tameshi-r12-repeat-control-selftest.\", dir=\"/tmp\")"},
    {"raw": "python3 tools/bash-witness-study.py count", "file": "tools/bash-witness-study.py", "ranges": "1051-1125,1744", "verdict": "holds", "excerpt": "exit 0 at CAND; output byte-identical with the fixture runner tampered (count never reads the runner)"},
    {"raw": "0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage only (argparse)", "file": "tools/bash-witness-study.py", "ranges": "39-41,63,119,1719-1724", "verdict": "holds", "excerpt": "EXIT_OK, EXIT_FAIL, EXIT_CANNOT, EXIT_USAGE = 0, 1, 2, 64; UsageParser.error -> self.exit(EXIT_USAGE, …); measured --r51-no-such-flag -> 64"},
    {"raw": "python3 tools/bash-witness-study.py selftest", "file": "tools/bash-witness-study.py", "ranges": "1228-1716", "verdict": "holds", "excerpt": "ran in fixture at CAND: exit 0, 'WITNESS_SELFTEST: 51/51 pass', 'VERDICT: PASS'"},
    {"raw": ".ufo/evidence/round-12/BashWitness/declaration.json, declared.tsv, manifest.json", "file": ".ufo/evidence/round-12/BashWitness/{declaration.json,declared.tsv,manifest.json}", "ranges": "-", "verdict": "holds", "excerpt": "all three present at CAND (ls-tree)"},
    {"raw": "own evidence directory plus isolated /tmp/bash-witness-selftest-private.* (selftest only); sibling object store read-only", "file": "tools/bash-witness-study.py", "ranges": "341-354,1241", "verdict": "holds", "excerpt": "prefix=\"bash-witness-selftest-private.\", dir=\"/tmp\"; materialize_target uses only `git -C kagi show`"},
    {"raw": "Registry scope is these round-12 instruments; no new conformance assertion is made about the historical runner.", "file": "SKILL.md", "ranges": "1505-1506", "verdict": "holds", "excerpt": "table at CAND still has exactly the two round-12 rows; the C2 tenth leg is a runner ledger case, not a registry row"},
    {"raw": "integrity-frozen (declaration, mapping, target, spec, summary; manifest.json itself is not pinned, seat ReRead08)", "file": ".ufo/evidence/round-12/BashWitness/declaration.json", "ranges": "top-level keys", "verdict": "holds", "excerpt": "pins declared/sha256, target/pin, spec/sha256, runner/sha256; no manifest self-pin (keys: created_at, declared, disclosure, environment_at_declare, inputs, kind, round, seat, spec_precheck, study)"},
    {"raw": "not blind: before declaring, their author had seen the source, the spec, the recorded aggregate outcomes and the per-defect KILLED/SURVIVED entries (…; seat ReRead08)", "file": ".ufo/evidence/round-12/BashWitness/declaration.json; .ufo/waves/round-27/residual/ReRead08.md", "ranges": "-", "verdict": "holds", "excerpt": "declaration disclosure field: 'declared-witness mapping, not a blind preregistration: before declaring, the author had seen … the recorded TABLE_BASH per-defect KILLED/SURVIVED entries surfaced by a pin grep'; ReRead08.md exists at CAND"},
    {"raw": "The declaration's runner pin 75ed934d… is stale at round 27 (check exits 1 DRIFT; run/rerun refuse, exit 2; count never reads the runner; seat Read25, .ufo/waves/round-27/w1/Read25.md)", "file": ".ufo/evidence/round-12/BashWitness/declaration.json; tools/bash-witness-study.py; tools/mutate-and-run.sh", "ranges": "566-570,949,1128-1222,119", "verdict": "holds", "excerpt": "pin 75ed934dc863… vs CAND runner sha 977de47034cb…; fixture runs at CAND: check -> exit 1, exactly 1 problem 'WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de470… committed=75ed934d… (96 files covered)'; run -> exit 2 'CANNOT-EVALUATE (runner-drift …)'; rerun -> exit 2 same; count -> exit 0, byte-identical with runner tampered; Read25.md exists at CAND"},
    {"raw": "The bash study deepens one recorded case, never a seventh independently measured gate.", "file": ".ufo/evidence/round-12/BashWitness/declaration.json", "ranges": "inputs.target", "verdict": "holds", "excerpt": "single pinned target kagi corpus/surface-census.sh @ fecee874…; no study leg added at CAND"},
    {"raw": "SHONEN.md box 3 carried a scope-bounded [~] at round 12, not [ ]", "file": "SHONEN.md", "ranges": "9-10", "verdict": "holds", "excerpt": "- [~] Instructions executable by an agent without oral context — [lane assertion, input-keyed monitor only; no independent promotion verifier](.ufo/evidence/round-21/coldread/ledger.json)"},
    {"raw": "corpus/lessons/round-1-verifier-spotcheck.md excludes it from the score.", "file": "corpus/lessons/round-1-verifier-spotcheck.md", "ranges": "17", "verdict": "holds", "excerpt": "the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed)"},
    {"raw": "Appending this registry does not extend the earlier Appendix A/B cold-read to new material or establish full-page instruction sufficiency.", "file": "SKILL.md; corpus/lessons/round-1-verifier-spotcheck.md:17", "ranges": "1540-1547", "verdict": "holds", "excerpt": "scope disclaimer consistent with the spotcheck lesson's non-credit of box 3; no pointer to falsify"}
  ],
  "falsifiers_checked": [
    "registry table silently grown at CAND (would falsify the scope sentence) — section byte-identical base..CAND, 2 rows only",
    "pin 75ed934d… coincidentally matching the changed runner (would falsify 'stale') — CAND runner sha 977de470… != pin; DRIFT reproduced empirically",
    "tenth-leg/runner-TMPDIR edit changing the read25-restated exit contracts — re-measured at CAND: check=1(DRIFT), run=2, rerun=2, count=0 and runner-independent; contracts intact a fortiori",
    "four panel-tool updates (tools/tally-audit.py, tally-audit-v2.py, tally-audit-v3.py, mte-interop.py) making a section statement false — section cites none of them; no interaction",
    "pinned evidence paths absent at CAND — all present (ControlGate expected.json + mismatch/expected.json; BashWitness declaration.json, declared.tsv, manifest.json)",
    "usage exit regressed to argparse default 2 — measured 64 for both tools",
    "selftest cells describing failing commands — both selftests exit 0 at CAND (29/29 and 51/51)"
  ],
  "empirical": {
    "fixture": "git clone --shared of lane, detached at 6d8c11e3, rev-parse --show-toplevel asserted; runner tamper (one appended comment line) applied only in fixture; no fixture commit; scratch deleted after",
    "repeat-control.py --selftest": "exit 0, SELFTEST: PASS (29 cases)",
    "bash-witness-study.py selftest": "exit 0, 51/51 pass, VERDICT: PASS",
    "check": "exit 1, 1 problem, DRIFT 977de470… vs committed 75ed934d…, 96 files covered",
    "run/rerun": "exit 2 each, CANNOT-EVALUATE (runner-drift …), no sweep executed",
    "count": "exit 0; stdout byte-identical before/after runner tamper",
    "usage": "--r51-no-such-flag -> 64 (both tools)",
    "snapshots": "--snapshot .ufo/evidence/round-12/ControlGate -> 0; --snapshot …/mismatch -> 1"
  }
}
```

## Adversarial findings

None actionable. No stale or moved pointer; no statement in the section is made false by the tenth leg, the runner TMPDIR change, or the four panel-tool updates. The one runner-coupled claim (stale pin, `check` 1/DRIFT, `run`/`rerun` 2, `count` runner-independent) was re-measured against the changed CAND runner and holds a fortiori (the drift only deepened: `75ed934d…` → `977de470…`, and a further-fresh tamper sha `b3358659…` is likewise refused).

Minor observations, not defects:
- Verdict-map row 1 wording "2 and 64 could-not-evaluate" is the tool's own classification verbatim (`invalid_usage` is listed among could-not-evaluate), so it is exact, not a compression.
- The section cites "seat ReRead08" without a path; the report is locatable at `.ufo/waves/round-27/residual/ReRead08.md` (exists at CAND).
- The section's historical round-12 claims are corroborated by current bytes and the existence of the cited records; re-deriving the round-12-era byte state itself is outside a cold-read row's reach and not asserted here.

## Verification gaps
- The `run`/`rerun` refusal was exercised at the pin precheck (fast path); a full sweep execution was not run (not needed to test any section claim, and it would mutate evidence dirs).
- `repeat-control.py` entry mode (`--runs 3 --out DIR -- COMMAND`) was exercised only via its selftest's child calls plus the two `--snapshot` runs, not by a fresh caller-side entry invocation; the selftest covers that path end to end.

Seat: T51W2Read14. No tools installed or updated.
