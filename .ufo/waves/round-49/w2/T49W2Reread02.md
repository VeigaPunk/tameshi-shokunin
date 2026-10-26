# T49W2Reread02 — C1 semantic re-read: `## Mutation-sweep recipe`, ordinals 9–17 (candidate `f181a961`)

## Scope and method

- Item: for each `reads.json` row with heading `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` and ordinal 9–17, judge at candidate `f181a961ae44061af486f600e5ea257d2baf78f8` whether the row's excerpt really supports the SKILL.md clause it anchors (the frozen counter only checks the excerpt is located), and judge every L1 correction in the section. Read-only seat; no counter was run and no verdict is expressed.
- `reads.json` at the lane worktree is byte-identical to the candidate's (compared directly against `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961…:.ufo/evidence/round-49/c1/reads.json`): 94 rows, schema `tameshi-r49-reads-v1`.
- All target bytes were read at the candidate via `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961…:<path>`; base/candidate SKILL.md and `git -C … diff 8ca674211111fa354b47b803358391d0b07fc6db9 f181a961… -- SKILL.md` were extracted to scratch (deleted before yield; the diff is copied beside this report as `T49W2Reread02-SKILL-base-to-candidate.diff`).
- Line-number note: every base→candidate hunk in SKILL.md is net-zero (−n/+n), so candidate line == base line throughout the section; confirmed by anchors — `mutation-case-kimi-census.md:26-28` at :186 in both, `mutation-case-kimi-census.md:30-33` at :194 in both, `mutation-case-kimi-census.md:59-76` at :196 in both (frozen control `skill_line` values agree).

## Finding 1 — row 13 does not support its clause (the only non-support)

- Row: `reads.json` ordinal 13, raw `mutation-case-kagi-census.md:44-47`, verdict `holds` (reader T49Read03), pointer line SKILL.md:175.
- Clause (SKILL.md:172–175 at `f181a961`): "assert `count(old) == 1` in the pristine copy, print the first matching line, and require the literal line `all unique` — both lanes' drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`) (mutation-case-kimi-census.md:22-25; mutation-case-kagi-census.md:44-47)."
- Observed target (`git -C … show f181a961…:corpus/knowledge/mutation-case-kagi-census.md`, :44–47): "each defect = ONE exact-string replacement applied to a fresh copy of `pristine.sh` (a `cp -p` byte copy, `cmp`-verified); the driver asserts the old string occurs exactly once before writing (`mutate_driver.py --check` → `all unique`, all 10). No defect compounds with another; the kagi original was never written…" — count==1 assert ✓, literal `all unique` ✓, no-compounding ✓; **no first-matching-line record**.
- Command that shows the absence: case-insensitive search for `first` over the whole of `mutation-case-kagi-census.md` at `f181a961` returns exactly one hit, :57 "…the first is round 2's…" — an unrelated context line. No line of the kagi record records printing a first matching line.
- Why it fails: the clause's "both lanes' drivers did exactly this" has three parts; the kagi half establishes two. The first-line half is over-claimed for the kagi lane. The counter cannot see this (contract.json C1 `cannot_see`: it "cannot check that the quoted text supports the section's sentence").
- Suggested fix: scope "print the first matching line" to the kimi record (kimi:24 "first-line match on all 10" supports it — row 12) or drop it from the shared claim. The L1's correction at SKILL.md:172 already removed the equally unsupported "print the count" half; this is the same defect shape left in place.

## Minor observations (no label risk)

1. **Row 16 range over-open.** `kimi:30-33` — the supporting lines are :32–33 ("suite count held: every mutant run still enumerated the full suite (`<n>/43`)…"); :30–31 are the kill-rate/no-inconclusive bullet, already cited separately at SKILL.md:212 (`kimi:29-31`). Over-open, not unsupporting.
2. **Row 17 two-range split.** The held-16 claim is at `kagi:50-53` ("the suite count held (`(<n>/16 cases)` on every run; green runs printed exactly `SELFTEST: PASS (16 cases)`)"); :27–35 corroborates the 16-case enumeration composition (`ok-case 01..14` + `skip-case 15/16`, epilogue `SELFTEST: PASS (16 cases)` at :33–35). Union supports.
3. **Predicate prose vs frozen counter.** contract.json C1 predicate says "each section keeping its base pointer count"; the frozen counter implements a floor — `.ufo/evidence/round-49/c1/measure.py:382` `floor_short = sum(1 for h in TARGETS if h not in missing and counts[h] < FLOORS[h])` (docstring :25 "keeps at least its base pointer count"). The L1's corrections added pointers (recipe 34→36, restore 10→11, map 17→18; total 90→94) — all ≥ floors, so no `floor_short`; but the contract prose is stricter than the scored implementation. Observation only: the counter is the scoring authority.
4. **Ordinal drift between the frozen control and reads.json.** The frozen control's recipe ordinals 9–17 (`c1-pointers-at-base-8ca67421.json`) differ from `reads.json` ordinals 9–17 because the L1's inline pointer at SKILL.md:174 shifts later ordinals by +1 (frozen ordinal 17 = `kimi:59-76` is `reads.json` ordinal 18). This report follows the item's definition (reads.json rows 9–17). `kimi:59-76` has a `holds` row (ordinal 18) and its pointer line SKILL.md:196 is unchanged from base — covered, but the L1 should confirm a sibling seat's range includes it under the candidate numbering.

## Corrections judged (10; all verified against target bytes at `f181a961`; all ok)

In-range (lines carrying ordinals 9–17):

1. **SKILL.md:172** — base "print the count and first matching line" → candidate "print the first matching line". Right: neither cited record (kimi 22-25, kagi 44-47) records printing the count; the removed half was unsupported. Residual: the first-line half stays over-claimed for kagi (Finding 1).
2. **SKILL.md:174** — inserted "(the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`)". Verified: `tools/mutate-and-run.sh:424-426` — guard `if count != 1:` at :424, :425 stderr-writes `APPLY FAIL id=… line=… old-string-count=%d expected=1`, exit 2 at :426. Pointer and claim correct; historical claim's scope untouched. Nit: "also" sits inside the both-lanes sentence; natural reading is fine.
3. **SKILL.md:177** — "not establish that particular round-2 guard" → "not establish that the round-2 driver carried the `new != old` no-op guard". Disambiguates the referent; the negative claim stays correctly hedged (neither cited record mentions `new != old`). No meaning inversion.
4. **SKILL.md:193** — "denominators43 and16" → "denominators 43 and 16". Whitespace repair of glued words; no pointer or meaning change.

Adjacent (same section, outside ordinals 9–17; judged for completeness):

5. **SKILL.md:143** — added "(cite-check and surface-probe print `n/m cases passed`)". Verified: `gates-survey-kumitate.md:21-22` at `f181a961` records cite-check `62/62 cases passed (hermetic)` and surface-probe `42/42 cases passed`. Accurate; pointer :19-31 unchanged.
6. **SKILL.md:146–147** — "exit0"→"exit 0", "bash16 enumerated cases,"→"bash: 16 enumerated cases,". Whitespace corruption repair; pointers unchanged, meaning restored.
7. **SKILL.md:198–199** — base "and summary `SELFTEST: FAIL (1/16 cases)` (kagi 82-103)" → candidate "and the failing suite line `1/16` / FAIL as the note records it (kagi 67,82-103)". Right: `SELFTEST: FAIL (1/16 cases)` appears nowhere in kagi-census.md (search: no hits); the note records `1/16` / FAIL in the kill-rate table at :67 and the bad-case grammar line at :84. New pointer 67 correct; sentence now matches the record.
8. **SKILL.md:210–211** — added "(neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`)". Verified: driver :569–574 computes pct over total defects (`(200*killed+total)/(2*total)`) and prints `MUTATE: DEGRADED` when inconclusive>0 (:571–574). Disclosure accurate; the recipe rule (inconclusive outside the denominator) unchanged.
9. **SKILL.md:221** — kagi ":251-253" → ":252-254". Right: the B10 sensitivity text ("B10's summary must read `ok=0` (pristine `ok=1`)") sits at kagi-census.md:252–254; :251 is blank and the old range clipped the sentence.
10. **SKILL.md:241–244** — "Round2:7.0s for11 runs, nodev24.21.0" → spaced, through "Kimi U5 at 204-205; Kagi U5 at 203-204". Whitespace corruption repair; pointers unchanged.

## Coverage

- 9/9 rows judged: 8 support, 1 does not (ordinal 13 — Finding 1).
- All 10 corrections in the section judged: 4 on lines carrying ordinals 9–17 (172, 174, 177, 193), 6 adjacent (143, 146, 199, 211, 221, 241). All verified against target bytes at the candidate.
- No counter invocation (bounds); no claim decided. Tooling: nothing installed or upgraded (none needed; pacman transactions paused host-wide per operator directive).

## Summary

- Row 13 (`kagi:44-47`, SKILL.md:172–175) does **not** support its clause: the kagi record establishes the count==1 assert and the literal `all unique` line but never records printing a first matching line (case-insensitive `first` over the whole file hits only :57, unrelated) — the clause's "both lanes' drivers did exactly this" over-claims that half for kagi. Fix: scope the half to kimi or drop it.
- Rows 9–12, 14–17 support their clauses at `f181a961` (verified against target bytes); row 16's range opens two lines early (:30–31 vs supporting :32–33), row 17's first range (:27–35) is corroborating composition — both noted, not defects.
- All 10 L1 corrections in the recipe section are right: the step-5 cluster (172/174/177) removes an unsupported count-print claim and adds a verified maintained-driver pointer (`mutate-and-run.sh:425` = the `old-string-count` stderr write under `if count != 1:`); the kagi re-ranges (67,82-103; 252-254) and the 569-574 DEGRADED disclosure all match the records; the rest are whitespace repairs of glued words.
- Structural: counter floor check is `counts[h] < FLOORS[h]` (measure.py:382) — added pointers (recipe 34→36, total 90→94) stay ≥ floors, so no `floor_short`; contract prose "keeping its base pointer count" is stricter than the scored implementation (observation).
- Ordinal drift: frozen-control recipe ordinals 9–17 ≠ reads.json ordinals 9–17 (inline pointer at SKILL.md:174 shifts +1; frozen ordinal 17 `kimi:59-76` is now reads.json ordinal 18, holds row present, pointer line unchanged) — L1 should confirm sibling coverage under the candidate numbering.
- Deliverables: `T49W2Reread02.json` (rows + corrections), this report, receipt `T49W2Reread02-SKILL-base-to-candidate.diff`.
