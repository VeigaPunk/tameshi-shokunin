# T54W1Read15 — cold read: `## Effective expectation reconciliation — round 14`

Seat T54W1Read15 (reader, leaf). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Section bytes read from the git object only (no working-tree read of SKILL.md).

- cand: `59c38109bf119d0e9d4f878644a82babc937bc1e`
- reader-section span at C0: `start=1589 end=1622` (body = SKILL.md lines 1589–1621; trailing blank stripped)
- section_sha256: `9640e5dc426f1f9ed7050e2443ac96c478e008ed9c2948ad59790da8aa977e3d`
- command: `cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf119d0e9d4f878644a82babc937bc1e '## Effective expectation reconciliation — round 14'` (scratch `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read15`)
  → `{"heading": "## Effective expectation reconciliation — round 14", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1589, "end": 1622, "section_sha256": "9640e5dc426f1f9ed7050e2443ac96c478e008ed9c2948ad59790da8aa977e3d"}` (receipt `T54W1Read15-receipts/reader-section.json`)
- extracted section bytes re-hashed independently from `git show <cand>:SKILL.md`: `9640e5dc…` — matches, so the span and the sha are the same bytes.

## Findings (2)

### F1 — the row/input counts have no anchor, and the 13 inputs are not in the manifests the recipe names

quote: `distinguish twelve expected rows from thirteen pinned inputs.`

why: The rule names no file, and the thirteen inputs it counts are not the inputs of either manifest the recipe's commands name: both `.ufo/evidence/round-14/dispositions.json` and `dispositions-before.json` carry twelve rows but only three `inputs` entries (all still matching at C0), so the count resolves only in the referenced `.ufo/evidence/round-13/expected.json` (`expected_checks` 12, `inputs` 13), which the sentence never names.

What I opened: `.ufo/evidence/round-14/dispositions.json` and `dispositions-before.json` (`rows` = 12, `inputs` = 3 each, `expected_file` = `.ufo/evidence/round-13/expected.json`); `.ufo/evidence/round-13/expected.json` (`expected_checks` = 12, `inputs` = 13). Receipt: `T54W1Read15-receipts/manifest-inputs.txt`.

### F2 — the moved pins are attributed to the manifests, whose own pins did not move

quote: `their pinned inputs moved after round 14`

why: The two round-14 manifests' own pinned inputs did not move: all three digests in each manifest's `inputs` map still match at C0, and the three stale pins sit in the referenced `.ufo/evidence/round-13/expected.json`, so the sentence attributes the moved pins to the manifests that merely point at them.

What I opened: same three files as F1; recomputed sha256 of all three manifest-pinned paths at C0 (all OK in both manifests) and of all thirteen `expected.json` pins (three stale). The tool's own error path agrees: `expected_input_digest_mismatch` names `tools/bash-witness-study.py`, a pin of the referenced expected file, not of either manifest. Receipts: `T54W1Read15-receipts/manifest-inputs.txt`, `T54W1Read15-receipts/live-both-exit2.txt`.

## What I opened and what I checked

1. `corpus/lessons/round-13-verifier-spotcheck.md` — exists at C0. Its `## Routed defects and residuals` list holds items 1–5, so the source line's `Routed defects 1–3` resolves; item 1 is the FileNotFoundError-before-the-kind-assertion case the section's first table row describes.
2. `corpus/knowledge/incremental-pin-disposition.md` §8 — heading `## 8. Empirical correction and backlink — round 14 (2026-10-20)`; it states eleven effective plus one explicitly superseded, selftest 34/34, and initial 18-of-34 failures retained in `verification.json`. Matches item 4.
3. `corpus/SOURCES.md` at C0 — S049 is the Python subprocess environment-mapping row (child-environment contract); S003 is the StrykerJS incremental row whose locator carries `§Limitations`. Both source pointers resolve.
4. `.ufo/evidence/round-14/dispositions.json` vs `dispositions-before.json` — 12 rows each; the only difference is the `producer_before` row (effective with `receipt`/`check` in the before manifest; `superseded` with `raw_receipt`, `raw_check`, `reason` and `superseded_by: [producer_before_oracle, producer_after_oracle]` after, and both replacements are effective). Item 3's claim that the only repair is that row's explicit supersession holds, and table row 2's requirement that both named oracle replacements be effective and pass holds in the exit-0 replay.
5. `.ufo/evidence/round-13/expected.json` at C0 — `inputs` 13, `expected_checks` 12, and exactly three stale pins (`tools/mutate-and-run.sh` pinned `75ed934d…`, `tools/bash-witness-study.py`, `tools/pin-disposition.py`). The section's `three of the thirteen are stale at the live bytes` and the three named inputs resolve exactly.
6. Live-tree commands at C0 (`git clone --shared` of the lane at `59c3810`, cwd = clone root): both manifests → exit 2, `kind: expected_input_digest_mismatch`. Item 2's first clause resolves.
7. Archived replay (`git archive 28aeef4` = round-15 spot-check commit 2026-10-20, extracted tree, cwd = that tree): `dispositions-before.json` → exit 1 with finding `expected_contains_missing`, `expectation: producer_before`, detail `producer_before: stdout lacks 'summary preserves top-level exposed declaration kind'`; `dispositions.json` → exit 0, `effective 11 / superseded 1 / passed 11`. Items 2 and 3 resolve in both directions.
8. `.ufo/evidence/round-14/verification.json` — `measured_commit 0c6e36d…` (round-14 commit), `disposition_selftest` exit 1 with stdout containing `SELFTEST: FAIL (18/34 failed: clean-superseded`; `verification-final.json` — `measured_commit 6431478…`, three checks: `disposition_selftest` exit 0, `unresolved_before` exit 1, `resolved_after` exit 0. Item 4's corrected selftest, frozen before/after and the 18-of-34 count all resolve.
9. `.ufo/evidence/round-14/capture-context.py` — `OUTPUT_REL = ".ufo/evidence/round-14/context-receipt.json"` (line 58), atomic write at `:584-602`; the receipt file exists. Item 5's "its historical output path replaces that frozen receipt" resolves.
10. Pointer `round15 registry below` — the section is followed by `### Round-14 historical registry — superseded by round 15` and then, inside the round-15 section, by `### Round-15 gate/probe registry`, whose retained invocation-context row is the maintained `tools/context-capture.py` gate. The pointer resolves (to the round-15 registry, not to the immediately following round-14 archive table).
11. Pointer `the round-17 re-pin section` — resolves to `## Live-tree re-pin and entry-command monitor — round 17` (SKILL.md:1840 at C0); its item 1/2 returns 1 then 0 on the round-18 manifests, which I re-ran at C0 (exit 1 / exit 0). Item 3's live-tree form resolves.
12. Table rows 1–5 — checked against artifacts, no stale cell found: row 1's FileNotFoundError claim is in `.ufo/evidence/round-13/verification.json` `producer_before.stderr` (`FileNotFoundError` in `sha256_file(RUNNER)`) and in `verification-verdict.json`'s `excluded_initial_failure`; row 3's could-not-evaluate behaviour is the actual exit 2 `expected_input_digest_mismatch`; row 4/5 match the retained-receipt semantics stated in the round-15 section (round-14 receipts are read-only inputs and are never regenerated).
13. Round attributions in item 2 — `git log --follow` confirms the runner first moved in round 16 (`c699c8c`, `05a2247`), the bash witness-study tool in rounds 18 and 21 (`58e5d53`, `370f2df`), and `tools/pin-disposition.py` in round 17 (`2a22ade`). Observation, not filed as a separate finding: the same three inputs also moved in later rounds — both tool files again in round 53 (`218bc6b`, `5b703c6`) and at this commit `59c3810`, and the runner again in rounds 17/18/26/30/51 — so the round list stops before the bytes that are live at C0 (`bash-witness-study.py` `60575e62…`@370f2df vs `f2bb50c7…`@59c3810; `pin-disposition.py` `331529ea…`@2a22ade vs `c917bc41…`@59c3810). The stale-count claim itself still holds at 3 of 13, so I did not file this as a finding; a fixing round rewriting the sentence for F2 can absorb it. Receipt `T54W1Read15-receipts/digests-at-named-rounds.txt`.
14. Census conformance: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, final line `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`.

## Receipts

- `T54W1Read15-receipts/reader-section.json` — span + sha at C0.
- `T54W1Read15-receipts/manifest-inputs.txt` — rows/inputs per manifest, all manifest pins OK at C0, 13/3 stale in the expected file.
- `T54W1Read15-receipts/live-both-exit2.txt` — both manifests at C0: exit 2, kind and message.
- `T54W1Read15-receipts/archived-replay-28aeef4.txt` — archived-tree replay: exit 1 (`producer_before`) and exit 0.
- `T54W1Read15-receipts/digests-at-named-rounds.txt` — blob sha256 at the named rounds and at C0.

## Scope

No lane file was edited; SKILL.md was read only from git objects. No tool installs, no mutating git command (the C0 worktree and the `28aeef4` tree are `git clone --shared` / `git archive` fixtures under `/fast/scratch/hyaku/tameshi-r54/T54W1Read15/`, removed after the receipts were copied here). Pacman untouched.
