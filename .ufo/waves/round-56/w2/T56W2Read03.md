# T56W2Read03 — cold read at C0

- Heading: `## Live-tree re-pin and entry-command monitor — round 17`
- Candidate: `c0137451f5b7f22d65f748fc69f1b181f55e1378`
- Section: lines 1857–1888; frozen round-18 sectionizer SHA-256: `6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac`
- Verdict: **verified-record** (no false statement or command failure in this section)

## Commands run

1. Loaded `.ufo/evidence/round-18/measure.py` with `importlib`, ran `sectionize()` over `git show C0:SKILL.md`, and selected the exact heading. Result: start 1857, end 1888, 64 total sections, SHA-256 above.
2. Independently extracted `git show C0:SKILL.md | sed -n '1857,1888p'`, stripped trailing blank lines, and hashed the joined section bytes. Result: 31 lines, matching SHA-256.
3. Ran the round-18 disposition recipe commands in the C0 clone:
   - `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json` → exit 1, status `failed`, one failure; its finding has `expectation: "producer_before"` and id `expected_contains_missing`.
   - The two round-17 disposition files each exit 2, as stated.
   - `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` → exit 0, status `clean`, `effective: 11`, `superseded: 1`.
   - The text-mode command prints three `HISTORICAL <path> rev=<rev> sha256=<sha>` lines, one for each waived instrument.
4. Ran `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)`, including the named replace-ref, GIT_DIR, detached-anchor, tree-id, dangling, and shallow-repository cases.
5. Ran `python3 tools/registry-check.py --rev c0137451f5b7f22d65f748fc69f1b181f55e1378` from a fleet-mirror clone with sibling lanes symlinked. Result: `REGISTRY_CHECK: held=48/50 superseded=7`, exit 1; `sources-census` and `verify-round15` reported `differs`. Both also differed at base, so this does not contradict a claim in this section. `mte-interop-check` held with sibling lanes present.
6. Ran the required fleet census validator: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0.

Full command receipts are under `T56W2Read03-receipts/`.

## Notes for the L1

- The compound GIT-environment sentence says the helper sets two overrides and scrubs inherited `GIT_*`, citing `tools/evidence-disposition.py:385-395`. That range contains the G4 comment and `GIT_ENV_OVERRIDES` dict (including `GIT_NO_REPLACE_OBJECTS` and `GIT_GRAFT_FILE`); the executable inherited-variable filter is at `:406-409` (`startswith("GIT_")` at `:407`). The behavior itself is true, and both named selftests expect exit 0 and pass, so I treated this as a pointer-precision note rather than a false statement. T54W2Read19 previously recorded the same under-reach as a minor gap routed to round 55; T55W3R03 later called `:385-395` exact for the override block. The text remains unchanged at C0, so this is an unresolved adjudication disagreement.
- In the GIT-scrub table row, “round 18 adds `bash-witness-study.py`” is contextually about adding its scrub (round 18 did that); the file itself was created in round 12. Consider clarifying the wording.
- The C0 fleet-mirror registry replay exits 1 on two rows (`sources-census`, `verify-round15`); both differ at base 981c5e8 as well. This is a live registry observation, not a claim that this section says should pass.
- The census validator passes, but C0 has 142 source rows (140 at base, plus S281 and S282), not the task brief’s stated 141 after one new row.
