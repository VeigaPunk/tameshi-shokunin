# T49W2Reread04 — C1 semantic re-read, `## Mutation-sweep recipe`, ordinals 27–40

Seat: T49W2Reread04 (wave 2, falsify). Base `8ca67421111fa354b47b803358391d0b07fc6db9`, candidate `f181a961ae44061af486f600e5ea257d2baf78f8`. I did not author what I attack. All paths below are relative to the lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; `B=` that dir, `R=f181a961ae44061af486f600e5ea257d2baf78f8`.

Method: read `.ufo/evidence/round-49/contract.json` (never edited); extracted reads.json, SKILL.md (base+candidate) and the diff at the two revisions with `git show`/`git diff` (read-only; no counter run, no clone — nothing here is a verdict). Every target was opened at the candidate; `git diff --stat 8ca67421…f181a96 -- corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/gates-survey-kagi.md corpus/knowledge/gates-survey-kumitate.md` prints nothing, so the four note targets are byte-identical at both revisions; `corpus/README.md` (+8 lines) was read at the candidate.

Scope fact: recipe ordinals at the candidate run 0–35 (36 rows; base 0–33, 34 rows — `jq` group_by on reads.json vs `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`). Ordinals 36–40 do not exist in this section; I judged rows 27–35 (9 rows). The +2 rows are the new line pointers `tools/mutate-and-run.sh:425` (ordinal 11) and `tools/mutate-and-run.sh:569-574` (ordinal 22) from the L1's step-5/step-7 corrections; every later ordinal shifts +1/+2 vs base (base 27–33 = candidate 29–35). All 11 SKILL.md hunks are line-count-preserving, so base and candidate line numbers coincide (`git diff … -- SKILL.md | grep -c '^@@'` → 11; hunks at 140, 169, 190, 207, 218, 238 are in my section).

## Row verdicts (9/9 support their clauses)

| ord | raw | supports | one-line why |
|---|---|---|---|
| 27 | `mutation-case-kimi-census.md:34-35` | true | step-9 triple (sha after==before, size+mtime, porcelain empty) all at :34-35; excerpt quotes the size/mtime/clean half, sha equality is :34's first half, inside the range |
| 28 | `mutation-case-kagi-census.md:54-56` | true | same triple at :54-56 plus cmp-identical copy — strictly more than the clause asks |
| 29 | `SKILL.md:377-378` | true | target's 2nd sentence is the endpoint-identity limit verbatim; round-27 tag accurate (`.ufo/waves/round-27/w1/Read03.md:3,:19`) |
| 30 | `mutation-case-kimi-census.md:20-21,29-31` | true | node v24.21.0 at :21; 11 runs + 7.0 s wall at :29-31; 300 s phrased against the sweep wall (per-run attribution is step 6's, SKILL.md:183-184 — already in the row's note) |
| 31 | `mutation-case-kagi-census.md:50-53` | true | 8/10 (80 %), 11 runs, 11.0 s wall, 280 s bound, suite count held `(<n>/16 cases)` — serves both the cost-profile and step-7 denominator clauses |
| 32 | `corpus/README.md` | true | README:11 G-R2-1 row carries the dirty-intermediate + re-pin story verbatim; excerpt located |
| 33 | `gates-survey-kagi.md` | true | errata §10 :503, round-2 errata :545, G-R2-1 :554-566; excerpt = :554-558 verbatim |
| 34 | `mutation-case-kimi-census.md` | true | §1:39, §3:109, §4:148, §5:183, §6:193 all exist; excerpt (§1 header + control row) = :39-43 |
| 35 | `mutation-case-kagi-census.md` | true | §1:62 … §7:208 all exist; excerpt = :62-66; Erratum R21 (:261) appended after §7 |

No row fails to support its clause. Two compressions recorded, neither misleading: rows 27/28's excerpts omit the sha-equality half (carried by the cited range's first line); row 32/33's clause "had to be re-pinned" merges "claim-ledger pin corrected (79294→79301)" + "`stamps.tsv:4` re-pinned after the substrate moved" — both targets state the precise incident.

## Correction verdicts (6 hunks, 10 entries — all ok, one residual)

All verified against the candidate bytes; details with commands are in `T49W2Reread04.json` (corrections[]). Highlights:

- :143 step-1 parenthetical "(cite-check and surface-probe print `n/m cases passed`)" — supported by gates-survey-kumitate.md:21-22 (`62/62 cases passed (hermetic)`, `42/42 cases passed`); the other four suites print `n/m pass` (:23-26), so the scoping is right.
- :174 step-5 — dropping "the count" is right (kimi:22-25 records "first-line match on all 10", no count print) and the new pointer `tools/mutate-and-run.sh:425` is right (:425 prints `old-string-count=%d` on the uniqueness-failure path). **Residual below (F1).**
- :177 step-5 guard sentence — sharpened to the named `new != old` guard; accurate (neither note records such an assert).
- :198 step-7 — the base text quoted a summary `SELFTEST: FAIL (1/16 cases)` that appears nowhere in the kagi note (`grep -n 'SELFTEST: FAIL'` on the note → none), so the base pointer could not support it; the new text "the failing suite line `1/16` / FAIL as the note records it (:67,82-103)" matches the bytes (:67 B1 row `1/16` / FAIL; :82-103 failing-case labels). Real staleness fixed.
- :211 step-7 kill-rate — "sit outside the denominator" = same rule; new parenthetical verified: kimi:29-31 / kagi:50-53 both say "No inconclusive run"; `tools/mutate-and-run.sh:506-507` total = every spec defect, :570 divides by total, :571-574 prints `MUTATE: DEGRADED` + exit 1 when inconcl>0.
- :221 step-8 pointer `:251-253`→`:252-254` — right: :251 is blank; :252-254 is exactly the B5/B10 sensitivity expectations; the old range cut "both exit 0" at :254.
- :224 step-9 parenthetical — accurate (step 2 at :150-152 records line count + repo revision; kimi:34-35 / kagi:54-56 record no after-revision; matches Restore :388/:391).
- :146, :193, :241-244 — pure cold-read damage repairs (missing spaces: "exit0", "bash16", "denominators43 and16", "Round2:7.0s…nodev24.21.0", "a280s bound", "U5 at204-205…at203-204"); meaning unchanged, facts carried by the already-cited ranges.

## Findings

**F1 (minor, residual overclaim — SKILL.md:172-174 at f181a96).** The corrected step 5 still says "both lanes' drivers did exactly this" where "this" includes "print the first matching line". The kimi cite supports it (`mutation-case-kimi-census.md:24` "first-line match on all 10"), but the kagi cite does not: `mutation-case-kagi-census.md:44-47` and the reproduce block :245 record only the assert + `all unique`, and `git -C "$B" show $R:corpus/knowledge/mutation-case-kagi-census.md | grep -in first` prints only :57 ("the first is round 2's" — unrelated). The overclaim predates this round (base claimed count AND first line); the correction narrowed it but left "both lanes" unsupported for kagi's print clause. Minimal fix if the L1 wants it: scope the print to the kimi note, or write "the kimi driver's note records the first-line print; the kagi note records the assert and `all unique`". Not a C1 predicate element (the counter checks presence, not this scope), so it does not block the deciding run.

**F2 (observation, no violation — pointer count 34→36).** Recipe pointers went 34 (base) → 36 (candidate) via the two new `tools/mutate-and-run.sh` line pointers. The contract predicate says "each section keeping its base pointer count"; the frozen counter's own rule is "at least" (`.ufo/evidence/round-49/c1/measure.py:25`: "Each section keeps at least its base pointer count (FLOORS)", FLOORS recipe=34), so 36 ≥ 34 satisfies it. Both new rows exist in reads.json (ordinals 11, 22, verdict holds) and both targets verify (see corrections :174/:211). Recorded so the closure reads "keeping" as the counter's ≥, not ==.

**F3 (observation, not a correction defect).** Step 9's heading "Restore + prove the substrate never moved" (SKILL.md:224) was kept, though round-27's Read03 (:19) also suggested rewording it to "Restore + prove endpoint identity". The body immediately limits the claim (:225-228), the heading is base text the L1 did not change, and the applied correction matches Read03's "smallest correction" for the sentence. No action needed; noted for the closure's spot-check.

## Bounds, tooling, scratch

- Read-only on the lane except the two deliverable files named by my item (`T49W2Reread04.json`, this report). No git/jj mutations; no counter invocations; no clone (git show/diff only). Did not read `~/.local/state/`, the c2 witness/stdout files, or anything under `/home/vgpnk/Projects/shokuknow`.
- Tooling authorization: no tools installed or upgraded (none needed).
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49W2Reread04/` deleted before yield; no receipts cited from scratch — every cited output is reproducible from the commands inline above and in the JSON.

## Summary

- Re-read recipe rows 27–35 (the section's ordinals end at 35; 36–40 do not exist) at `f181a96`: 9/9 excerpts support their clauses; two benign compressions noted (sha-half omitted in 27/28; "re-pinned" merge in 32/33).
- Judged all 6 SKILL.md correction hunks in the section (10 entries): all ok — two new pointers (`tools/mutate-and-run.sh:425`, `:569-574`) verified at the named lines; the `:67,82-103` and `:252-254` re-points fix real base mismatches; spacing hunks are cold-read damage repairs.
- F1 (minor): step 5's "both lanes' drivers did exactly this" still overclaims the first-line print for kagi (its note records only assert + `all unique`); pre-existing, does not block C1.
- F2: recipe pointers 34→36; frozen counter requires "at least" (measure.py:25) — no violation.
- F3: step-9 heading kept as base; body limits it; no action.
- No counter run, no clone, no installs; deliverables at `.ufo/waves/round-49/w2/T49W2Reread04.json` and `T49W2Reread04.md`.
