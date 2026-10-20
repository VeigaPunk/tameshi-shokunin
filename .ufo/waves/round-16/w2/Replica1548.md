# Replica1548 — cold-read replica, SKILL.md lines 1548-1562

**Target attacked:** `### Round-13 gate/probe registry` (SKILL.md:1548-1562) — post-freeze replica; executed every command the registry rows name.
**Verdict: holds.** Every registered command reproduces its mapped verdict at commit `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.

## Page integrity

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c699c8c36d6e4eca4b796b81a8247904aa145ec8:SKILL.md | sha256sum`
  → `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` — matches the required page SHA.

## Scratch setup (commands, exits)

Scratch: `/tmp/tameshi-r16w2-Replica1548-gc4f2A`. Exported committed bytes for the files the section explicitly names plus the pinned fixtures the tools' selftests require (the tools name these paths internally; digests verified against literals and `expected.json`):

- `tools/pin-disposition.py` (53116 B, sha256 `29725397…ff14f11` — matches `expected.json` pin)
- `tools/witness-metadata.py` (48914 B, sha256 `df339068…cc0bed4` — matches pin)
- `.ufo/evidence/round-13/{pin-manifest.json,witness-metadata.json,expected.json}` (sha256 `64eaa43e…`, `46328227…` — match pins)
- `.ufo/evidence/round-12/BashWitness/{summary.json,declaration.json,declared.tsv}` and `rerun-20261020T035435Z/summary.json` — all four sha256 prefixes match the `PINNED_INPUTS`/`RERUN_SUMMARY_SHA256` literals in `tools/witness-metadata.py:72-130`.

## Row 1 — six-leg content disposition (probe)

- `python3 tools/pin-disposition.py --selftest` → exit 0, `SELFTEST: PASS (18/18)` (unchanged, changed-head, dirty-worktree, missing-* , symlink, malformed/duplicate/missing-leg, invalid-root cases all PASS). Matches verdict map "selftest 1 failed" → observed exit 0 = pass. Matches `expected.json.expected_checks.pin_selftest` (`exit:0`, `SELFTEST: PASS (18/18)`).
- `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0, `status: ok`, `counts: legs 6, unchanged 3, changed 3, unavailable 0`, `result_reuse: not_established` on all six legs. Exit 0 = verdict map's "0 observations" tier, consistent with the map (0 = observations incl. changed/unavailable — the tool reports observations successfully at exit 0). The six registry-recorded legs are present in the manifest (`len(legs)=6`).

## Row 2 — exposed witness provenance companion (gate)

- First `--selftest` attempt → exit 2 `SETUP_FAIL summary unreadable` — the tool requires the four pinned round-12 frozen files under its own `LANE_ROOT = Path(__file__).parent.parent` (`tools/witness-metadata.py:70`); after copying them from the commit:
- `python3 tools/witness-metadata.py --selftest` → exit 0, `SELFTEST: PASS 39/39` (all cases: corrected-companion-green, tamper-*, symlink/path-rejection, malformed JSON, schema/kind/disclosure mismatches, lane-root-missing — all OK). Matches `expected_checks.metadata_selftest` (`exit:0`, `SELFTEST: PASS 39/39`).
- `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` → exit 0, `WITNESS_METADATA: metadata_consistent reason=ok` — matches verdict map tier "0 metadata_consistent/clean" and `expected_checks.metadata_corrected` (`exit:0`, `id: metadata_consistent`).

## Record lines (1556-1561) — anchors re-checked

- "No registry row changes rank, SHONEN authority, or the six recorded cases" — manifest carries exactly six legs; no counter-observation.
- "Historical summary's producer SHA names the producer that actually ran, not the repaired current producer" — anchor holds: tool literal `PRODUCER_TOOL_SHA256` (`249d9dcd…`, `witness-metadata.py:117-119`) differs from `expected.json`'s pin for `tools/bash-witness-study.py` (`49e9e5e2…`), i.e. recorded-producer digest ≠ current-tool digest.
- PIT S048-over-S047 clarification — narrative record; no executable instruction, no gap observed.

## Gaps / notes

- Minor (setup, not the artifact): `--selftest` cannot run from a bare tools-only copy; it hard-requires the four pinned round-12 frozen inputs under the tool's own parent directory (documented in code as deliberate: "fail setup loudly if the lane does not hold the pinned bytes"). Reproduced exactly once fixtures were staged. Not counted as a registry gap — the registry names the tools, and the tools name their fixtures.
- No installs performed; system python3 was sufficient.

```json
{"seat":"Replica1548","skill_sha256":"3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4","sections":[{"start":1548,"heading":"### Round-13 gate/probe registry","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["witness-metadata --selftest exits 2 SETUP_FAIL unless the four pinned .ufo/evidence/round-12/BashWitness inputs exist under the tool's parent dir; requires staging committed fixture bytes in the temp copy"],"commands_executed":["git show c699c8c36d6e4eca4b796b81a8247904aa145ec8:SKILL.md | sha256sum","git show <commit>:<path> exports for tools/pin-disposition.py, tools/witness-metadata.py, .ufo/evidence/round-13/{pin-manifest.json,witness-metadata.json,expected.json}, .ufo/evidence/round-12/BashWitness/{summary.json,declaration.json,declared.tsv,rerun-20261020T035435Z/summary.json}","python3 tools/pin-disposition.py --selftest (exit 0, PASS 18/18)","python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin (exit 0, legs=6 unchanged=3 changed=3)","python3 tools/witness-metadata.py --selftest (exit 0, PASS 39/39 after fixture staging)","python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json (exit 0, metadata_consistent)"],"opened":["tools/pin-disposition.py","tools/witness-metadata.py",".ufo/evidence/round-13/pin-manifest.json",".ufo/evidence/round-13/witness-metadata.json",".ufo/evidence/round-13/expected.json",".ufo/evidence/round-12/BashWitness/summary.json",".ufo/evidence/round-12/BashWitness/declaration.json",".ufo/evidence/round-12/BashWitness/declared.tsv",".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json"],"scratch":"/tmp/tameshi-r16w2-Replica1548-gc4f2A"}]}
```
