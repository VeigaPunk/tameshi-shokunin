# T54W1Read14 — cold read of `### Round-13 gate/probe registry`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- CAND: `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0)
- Section span: SKILL.md lines 1573-1588 (canonical section bytes = lines 1573-1587, 15 lines, 2033 bytes)
- `reader-section.py` printed `section_sha256 896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d`; independently recomputed over the stripped section bytes (split on `\n`, trailing blank lines dropped, no trailing newline, joined with `\n`): same `896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d`.

## Findings

None. `findings` is empty in `T54W1Read14.json`. No rule anchor, table cell, count or sentence in this section failed to resolve or contradicted another at C0. Everything below is the sweep that produced that result, so the empty list is evidenced rather than asserted.

## Artifacts opened and what was checked

All reads at C0 unless stated; the lane working tree was never read. Commands were run in a `git clone --shared` copy at `/fast/scratch/hyaku/tameshi-r54/T54W1Read14/lane` checked out at C0 (`git rev-parse --show-toplevel` asserted before every mutating-capable run).

1. Section bytes and shape.
   - `git -C <lane> show 59c38109bf11…:SKILL.md | sed -n '1573,1588p'`; the table header plus both rows parse as 8 cells each (`|` count 9 per row), matching the 8 column names.
2. Row `six-leg content disposition` — entry command.
   - `github-clone> python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0, `"status": "ok"`, `"counts": {"legs": 6, "unchanged": 1, "changed": 5, "unavailable": 0}`, every leg `pinned.status = verified`.
   - Matches the verdict map cell: exit 0 with drift included (`changed=5`).
3. Row `six-leg content disposition` — verdict map and self-test.
   - `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0.
   - Code paths at C0: failure of a case returns 1 (`tools/pin-disposition.py:1346`), `ScratchRootUnusable` maps to exit 2 (`:1337`), invalid input returns 2 (`:220`, `:1337`), normal runs return 0 (`:1349`). So "0 observations … 2 invalid input/could-not-evaluate; selftest 1 failed" is the actual map.
4. Row `six-leg content disposition` — pinned values.
   - `tools/pin-disposition.py` carries `CANONICAL_LEGS = (` at line 138 and `CANONICAL_BY_LEG` at line 146; literal selftest labels are the `SELFTEST_CASE {}` names in the same file.
   - `.ufo/evidence/round-13/pin-manifest.json` exists at C0 and lists exactly `['js-kimi-census','bash-surface-census','bash-tsukuroi-census','bash-mado-verify','bash-checklist-run','js-claims-check']`.
5. Row `six-leg content disposition` — write scope.
   - Selftest scratch is `tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir=strict_scratch_root())` (`:725`), removed at `:1347`; fixtures are written only under that temp tree.
   - After both selftest and entry-command runs, `git -C <clone> status --porcelain` printed nothing: nothing outside the temp tree was written.
6. Row `exposed witness provenance companion` — entry command.
   - `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` → `WITNESS_METADATA: metadata_consistent reason=ok exit=0 companion=…/witness-metadata.json inputs=summary,declaration,declared,rerun_summary`, exit 0.
   - Verdict map class 0 (`metadata_consistent`) matches; class mapping verified in `_fail` (`:255-268`): exit 1 → `metadata_inconsistent`, exit 2 → `snapshot_tampered` only for `_digest_mismatch`/`SNAPSHOT_TAMPER_REASONS`, else `input_unavailable`. Usage exits 2: `python3 tools/witness-metadata.py` with no mode argument printed argparse usage and exited 2 ("including usage" holds).
7. Row `exposed witness provenance companion` — self-test.
   - `python3 tools/witness-metadata.py --selftest` → 39 case lines all `OK`, `SELFTEST: PASS 39/39`, exit 0.
8. Row `exposed witness provenance companion` — pinned values, digest-by-digest.
   - `tools/witness-metadata.py` pins `PINNED_INPUTS` for `summary`, `declaration`, `declared` (`:74-90`) plus `RERUN_SUMMARY_SHA256` (`:128`), all under `.ufo/evidence/round-12/BashWitness/`.
   - Recomputed `git show C0:<path> | sha256sum` for the four files:
     - `summary.json` → `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9`
     - `declaration.json` → `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901`
     - `declared.tsv` → `0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3`
     - `rerun-20261020T035435Z/summary.json` → `6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0`
     all four equal to the tool's literals, and the four are exactly the `inputs=` names the run reports.
   - `.ufo/evidence/round-13/witness-metadata.json` contains `"expected": {"id": "metadata_consistent", "exit": 0}`, so "companion expected verdict" is accurate.
   - The cell's exclusion claim is false-proof-negative: `.ufo/evidence/round-13/expected.json` exists at C0, and `grep -n 'expected\.json' tools/witness-metadata.py` returns no line, so the gate never reads it.
9. Row `exposed witness provenance companion` — write scope.
   - Selftest fixture tree: `tempfile.mkdtemp(prefix="witness-metadata-selftest-")` (`:1122`), `shutil.rmtree(temp_root, ignore_errors=True)` (`:1186`); fixture writes (`:941-1081`) are confined to that tree. The `--check` path only reads the pinned inputs and companion.
10. Prose paragraph on recorded cases.
    - `git show C0:tools/mutate-and-run.sh | grep -cE '^#   (js|bash)-…'` → 10 case lines, which is consistent with the ledger header line 84 (`r16 seven; r18 eight; r26 nine; r51 ten`).
    - `git blame -L 84,100 C0 -- tools/mutate-and-run.sh` shows the first six lines added by `606716f` (2026-10-14) and the seventh (`js-round-gate`) by `c699c8c` (2026-10-20). `the six recorded cases` (line-broken before `this write`) and `a seventh case is recorded since round 16` are therefore historically true, not stale at C0, and the sentence is explicitly scoped by `this write`.
    - The referenced heading exists byte-for-byte: SKILL.md line 1780 is `## Seventh recorded case and full-page cold-read — round 16`; its body states the round-16 case count as seven and names the later counts, so the pointer lands on material that already accounts for the eighth and ninth cases.
11. Prose paragraph on the producer SHA and old hashes.
    - Frozen `.ufo/evidence/round-12/BashWitness/summary.json` carries `tool.sha256 = 249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`; `tools/bash-witness-study.py` at C0 hashes to `f2bb50c77a6b6ffc53fd4e31d06c729f9cface7c1684f232c060f6a4978bf261`. The historical SHA names the producer that ran, not the current file — the sentence holds.
    - "No old evidence hash is regenerated": `git rev-parse` of the four round-12 blobs at their add commit `9df9212d33dc2dbda133e88f28ad47bb08839a5b` and at C0 are identical for all four (`ac4e227b…`, `7fb79463…`, `553b7e0f…`, `045370ef…`).
12. PIT clarification paragraph.
    - `corpus/SOURCES.md` at C0, line 56 (S047) and line 57 (S048): S048's row says it "supersedes S047 — item 4 is prioritisation rather than a reuse skip; no claim here resolves its pronoun to test versus mutation". The section's retained distinction and its "no test-versus-mutation pronoun claim" sentence match the row. The section's own anchor `S048 supersedes S047` is present verbatim.
13. Census conformance (round context, read-only): `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → last line `ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, exit 0 (only W01/W04 advisory rows printed).

## Considered and deliberately not reported

- The four round-12 files in the `Pinned values` cell are cited by bare basename (`summary.json`, `declaration.json`, `declared.tsv`, `rerun-20261020T035435Z/summary.json`). The row frames them as "the four frozen round-12 files", and all four resolve to `.ufo/evidence/round-12/BashWitness/<name>` (round-12 holds many evidence subdirectories, but these four basenames occur nowhere else under it), with the tool pinning them at those full paths. The last commit to rewrite this cell before C0 (5b703c6) deliberately replaced the old `expected.json` pinned value with the companion plus these four files and the explicit exclusion. Treating a resolvable basename as a broken anchor would be a false positive, so no finding is filed.
- "0 metadata_consistent/clean" uses `clean` where the tool prints `reason=ok`. The token is a class word for exit 0, the same wording the later registry row uses, and the companion's own `expected.id` is `metadata_consistent`; not a stale cell.
- The section's write-scope cells do not repeat the `$TMPDIR` detail the round-12 registry uses, but the C0 standing rule added at SKILL.md:32-39 covers the scratch-root arm and both cells stay true under it (verified by the runs above).

## Limits

- The two entry commands were exercised in a shared clone against the live fleet root (read-only) and the clone's own C0 evidence; they were not re-run against the live lane working tree.
- The `git blame`/`rev-parse` checks read history only; no lane file, contract, freeze, ledger, wave spec or counter was modified.
- Received one advisory note from `git log -L` output; no mutation was run.
- No tool was installed or upgraded for this seat.
