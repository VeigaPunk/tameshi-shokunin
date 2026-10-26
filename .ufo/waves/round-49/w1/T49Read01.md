# T49Read01 — C1 reader: `## Mutation-sweep recipe` pointer ordinals 0–4

Base `8ca67421111fa354b47b803358391d0b07fc6db9`. Section `## Mutation-sweep recipe — numbered
steps; bounded cold-read evidence`, section_start 131, frozen `section_sha256`
`e37cf21e3155bdd39a68ef24a5135f2ad62861bbb5794ec954abf42bb0bd631d` — recomputed from the base blob
with the monitor's own `sectionize` and found equal (command in Artifacts, receipt line 2).

Pointers are the five rows of `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`
with this heading and `ordinal` 0–4 (all `kind: line`, `skill_line` 141, 141, 143, 147, 148).

No counter was invoked for this read; no probe; no verdict. Excerpt assertions use only the
frozen counter's pure helpers `norm()` and `pointed_text()` (`.ufo/evidence/round-49/c1/measure.py:202-208`)
against the base blob bytes, i.e. the same test the counter applies to a read row.

## Verdicts

| ord | raw | base_verdict | one-line reasoning |
|---|---|---|---|
| 0 | `mutation-case-kimi-census.md:4-7` | **holds** | `corpus/knowledge/mutation-case-kimi-census.md:4-7` is still the substrate paragraph: mutants are copies under `/tmp/tameshi-r2-1-work/`, no fleet file written, "No live `~/.kimi-code` path was read", runs are `--selftest` (suite's own `mkdtemp` root) or `--root` at an empty dir — it carries step 1's "no live-path or host effects" + "private `--root` fixtures" half. |
| 1 | `mutation-case-kagi-census.md:24-38` | **holds** | `corpus/knowledge/mutation-case-kagi-census.md:24-30` shows the verify/shape path reads no live path and the two trailing verb cases are substrate-gated (`skip-case … substrate-absent`, "does not execute the verbs block"), `:33-35` shows skips counted as cases — this is the "exclude or control host-gated branches" half the parenthetical assigns to it. |
| 2 | `gates-survey-kumitate.md:19-31` | **holds** | `corpus/knowledge/gates-survey-kumitate.md:19-26` is the per-gate table: exit code plus the verbatim summary line, `round-gate … `ROUND_GATE_SELFTEST: 60/60 pass` / `VERDICT: PASS`` and five `n/n cases passed` / `VERDICT: PASS` rows — the `n/m pass` + `VERDICT:` form line 143 requires; `:28-31` is the `mkdtemp` hermeticity observation. |
| 3 | `mutation-case-kimi-census.md:20-21` | **holds** | `corpus/knowledge/mutation-case-kimi-census.md:20-21` reads `control run, unmutated copy — … `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 (node v24.21.0)`, identical to the string quoted at SKILL.md:145-146, and the copy is of the artifact pinned at `:13-16` ("pinned bytes" holds). |
| 4 | `mutation-case-kagi-census.md:27-35,42-43` | **holds** | `corpus/knowledge/mutation-case-kagi-census.md:33-35` gives `ok-case 01..14` + `skip-case 15`/`16`, epilogue `SELFTEST: PASS (16 cases)` and states "the hermetic case set here is 14, plus 2" = "14 executed +2 skipped"; `:42-43` is the green control (`SELFTEST: PASS (16 cases)`, exit 0). Both ranges sit on the intended content; no line drift. |

Result: 0 stale, 0 unresolved, 0 absent among ordinals 0–4. No `proposed_fix` rows are produced,
and no pointer is proposed for deletion (the section's frozen floor is 34 pointers; the counter
keeps a per-section pointer count, so the section text at 138–148 should be left intact for these
five).

## Commands that show each verdict

```
git -C LANE show 8ca67421…:SKILL.md | sed -n '138,149p'                     # the clauses
git -C LANE show 8ca67421…:corpus/knowledge/mutation-case-kimi-census.md | sed -n '4,7p;13,16p;20,21p'
git -C LANE show 8ca67421…:corpus/knowledge/mutation-case-kagi-census.md | sed -n '24,38p;42,43p'
git -C LANE show 8ca67421…:corpus/knowledge/gates-survey-kumitate.md | sed -n '19,31p;345,356p'
```

LANE = `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. The excerpt/claim containment run and its
per-pointer output are in `.ufo/waves/round-49/w1/T49Read01.excerpt-check.txt` (all five
`occurs True`, lengths 161/193/135/145/237, all inside the counter's 24–400 bound).

## Findings

1. **No staleness in ordinals 0–4.** Each pointed range still contains exactly the evidence its
   clause needs; the two `kumi`-census pointers (0, 3) and the `kagi` pointers (1, 4) are on their
   intended paragraphs, not merely on text that "reads plausibly". Evidence: table above and the
   receipt.
2. **The two evidence chains agree at base (cross-check, not part of any verdict).**
   `corpus/knowledge/mutation-case-kimi-census.md:20-21` (`43/43`) and
   `corpus/knowledge/gates-survey-kumitate.md:26` (same `43/43` row) match; the kagi skip arithmetic
   (`:33-35`, 16 = 14 + 2) matches SKILL.md:147-148. No contradiction to report to the Rust judge.
3. **Observation, outside my pointed ranges and not a staleness finding:**
   `corpus/knowledge/mutation-case-kimi-census.md:207` has an append-only errata heading fused onto
   the end of the previous paragraph — `reads the live tree by construction.## Errata (round 5) — …`.
   Shown by `git -C LANE show 8ca67421…:corpus/knowledge/mutation-case-kimi-census.md | sed -n '206,208p' | cat -A`.
   Any pointer inside that file that expects a heading at `:207` will not find one; my ranges
   (`:4-7`, `:20-21`) are untouched by it. I did not edit the file (read-only seat, and the file is
   not one of my deliverables).
4. **Scope note for integration:** step 1's sentence (SKILL.md:138-141) is jointly carried by two
   pointers — kimi `:4-7` for "no live-path or host effects"/"private `--root` fixtures" and kagi
   `:24-38` for "exclude or control host-gated branches". If the section is reworded, both pointers
   must stay paired or the clause loses one half; neither pointer alone covers all of it.

## Out of scope / not done

- No counter invocation at any revision (`--selftest`, `--list` or otherwise) — not needed for a
  read row, and deciding runs belong to the L1.
- No edits to SKILL.md, the three target files, the contract, the pointer control file, reads.json,
  or any other lane path. Deliverables written: the two files under
  `.ufo/waves/round-49/w1/` listed below.
- Ordinals 5–33 of this section and the other six lapsed sections are other seats' items.
- No tools installed; no package manager touched.

## Artifacts

- `.ufo/waves/round-49/w1/T49Read01.rows.json` — 5 rows, sha256 `3b9b86a1a7c8e3e57a44a60ad4c58a9484c20aa29b25398a8ebac1cbca4bca39`.
- `.ufo/waves/round-49/w1/T49Read01.excerpt-check.txt` — receipt: pointers-file sha256
  `92a2e532fb323bee556e44b0877107339f7faa9e1c8f9636a8a6b1a8de6d4d3c`, per-row excerpt length /
  containment / claim-verbatim flags, section-sha equality note.
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read01/` (base blobs used for reading) removed before
  yield; nothing cited from it.

## Summary

Five recipe pointers (ordinals 0–4) read at base against their targets: all five **hold** — 0 stale,
0 unresolved, 0 absent.
Ordinal 0 (kimi `:4-7`) carries the no-live-path/private-`--root` half of step 1; ordinal 1 (kagi
`:24-38`) carries host-gated-branch control; the pair is required, neither alone suffices.
Ordinal 2 (kumitate `:19-31`) is the `n/m pass` + `VERDICT:` table, counts re-verified in the file's
own K-R2-1 erratum at `:345-356`.
Ordinal 3 (kimi `:20-21`) is the verbatim `43/43` / `PASS` control on the pinned copy; ordinal 4
(kagi `:27-35,42-43`) is 16 cases = 14 executed + 2 skipped plus the green control.
All five excerpts pass the counter's own `norm()`/`pointed_text()` containment test at 24–400 chars
(receipt: `T49Read01.excerpt-check.txt`).
No proposed fixes; section pointer floor (34) untouched. Non-finding noted: kimi-census:207 has a
fused errata heading, outside my ranges.
No counter run, no probe, no verdict; no tooling installed.
Artifacts: `T49Read01.rows.json`, `T49Read01.excerpt-check.txt`.
