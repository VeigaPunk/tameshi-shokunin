# T54W2Read03 — fresh cold read at C1

Section: `### The boundaries — what a service run is not`
Candidate: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
Span at C1: **869–893** (trailing blank line stripped by the frozen round-18 `sectionize`)
`section_sha256`: `ff4f61972eec106008e19366e9b643322c95f83bad28b916e08082a233116f1d`
Verdict: **1 finding** (one off-by-one citation range). The section's other twelve anchors resolve.

JSON deliverable: `.ufo/waves/round-54/w2/T54W2Read03.json`
Receipts: `.ufo/waves/round-54/w2/T54W2Read03-receipts/`

## Finding

### F1 — the "Sensitivity, not truth" cite starts one line late and swallows the next unknown

Quote (byte-exact, `SKILL.md:892` at C1):

```
  (`mutation-case-mado-verify.md:229-230`).
```

Why: the clause it supports is "a sweep measures what the suite can detect, never whether the gate's verdicts are right", which is item **U2** of the mado note occupying **`:228-229`**:

```
 228| - **U2** — suite sensitivity ≠ gate truth: nothing here measures whether the gate's verdicts
 229|   against the *real* config planes are right; only what its suite can detect.
 230| - **U3** — tool drift (I1): reproduction under the current harness revision `b56c6e57…` is
```

`:230` is the first line of the unrelated **U3** (tool drift / re-pin). The cited range therefore opens on U2's second line and closes on U3's first, so a reader following the pointer reads a superset that contains a different unknown, and the item's own first line — the one carrying the phrase the bullet paraphrases — is outside the range.

Provenance of the drift: the mado note has exactly one commit (`4494715 probation round 6 (training r5): see LOG`) and its line numbering is identical at C0 (`59c38109bf11:228-230` prints U2/U2/U3 verbatim, same numbers), so this is an authoring-time off-by-one inherited from round 18, **not** introduced by the C1 fix pass. The same offset was already reported by round-18 seat CR14 (`G1`) and by round-27 residual ReRead05 (`M1`, whose smallest-safe-correction list names `:228-229`), and it survived both corrections. Recording it again is correct: at C1 the anchor still does not resolve on the clause it is attached to.

Repair, if the L1 wants one: `229-230` → `228-229` on `SKILL.md:892`. (Recommendation only; I edited nothing.)

## Anchors that DO resolve at C1 (checked, not assumed)

Every anchor named inside 869–893, resolved against the artifact at C1:

| Anchor in the section | Resolves to | Verdict |
|---|---|---|
| `matrix row F` | `SKILL.md:739` `| F coordinated edits | unprobed | …` | resolves |
| `census §5 scope, fleet-suite-census.md:288-291` | §5 begins `:249`; `:288-291` is the "Scope of the offer" paragraph, naming single-edit/hermetic/per-revision-per-host | resolves |
| `SKILL.md:819-820` (porcelain-clean opt-in precondition) | `:820` "…and a porcelain-clean sibling tree at open" | resolves |
| `tools/mutate-and-run.sh:36-38` + quote "The target is never written" | the sentence spans `:37` ("…The target is") and `:38` ("never written: …"), i.e. inside the cited range | resolves (quote is a reflow of `:37-38`, still within `:36-38`) |
| `the ## Restore discipline section` | `SKILL.md:386` `## Restore discipline — before/after identity, not continuous non-write proof` | resolves |
| `mutation-case-mado-verify.md:57-59` (sha pair) | control line, `MUTATE_RESTORE: OK (target-sha256 before=… after=…)`, re-hash | resolves |
| `SKILL.md:346-347` (low kill rate is a report) | `:346` "**Bands are a report convention, not a pass/fail gate.** An 8/10 admits, and so" / `:347` "does a <50 % — with the gap recorded…" | resolves |
| `mutation-case-mado-verify.md:175-176` (first below the band) | "The fourth point is the first below the 50–80 band" | resolves |
| `mutation-case-mado-verify.md:66-72` (composition) | in-/out-of-surface split, "4/4 killed and 0/6 killed", "composition, not a regression" | resolves |
| `mutation-case-mado-verify.md:237-238` (unabsorbed) | U6 "records the findings unabsorbed." | resolves |
| `mutation-case-mado-verify.md:240-260` (recommendations) | §8 "Recommendations only, no patch", seven items | resolves |
| `mutation-case-mado-verify.md:17-23` (harness moved mid-round) | Incident I1, re-pin `b56c6e57…` | resolves |

Also verified and **not** reported:

- `B56c6e57…` is presented as a re-pin, and the note's `:22-23` ties every number to `597e1419…`, so the bullet's "every number stays tied to the executed revision" matches `:22`; no contradiction.
- "per-revision and per-host (census §5 scope…)" vs the census text "per-revision and per-host (no cross-host stability claim, matrix U5)" — consistent.
- "50-80" (ASCII hyphen) in this section vs "50–80" (en dash) in the cited mado note: orthographic variance only, and the page's own bands table (`:341`) writes `50-80 %`, so the section is internally consistent. Not a defect.

## Mechanical sweeps (QUALITY 104 class: run-together tokens, spacing, duplicate parentheticals)

Run over the exact section bytes (`receipts/section-869-893.txt`, sha256 equal to the reader's `section_sha256`):

| Pattern | Hits |
|---|---|
| trailing space / tab at EOL | 0 |
| empty parens `()` or `( )` | 0 |
| adjacent parenthetical groups `)(` or `) (` | 0 |
| missing space after sentence period before a capital | 0 |
| duplicated adjacent word | 0 |
| lines with an odd number of backticks | 0 |
| paren balance | 15 open / 15 close |
| non-ASCII inventory | 6 × `—`, 1 × `…`, 1 × `§` (all intended) |

The 15 double-space hits are the two-space list-continuation indents and are correct, not run-together tokens.

Self-contradiction check inside the section: the three bullets that could collide are "Read-only" (no tree-clean check emitted; porcelain-clean is an open-time precondition) vs "Findings kept, never smoothed" (a report, not a failure) vs "Sensitivity, not truth" (not gate truth). They occupy disjoint claims; no sentence in the section contradicts another.

## Artifacts opened

- `git show 99c3bc88…:SKILL.md` lines 869–893 (the section; also 204–210, 244–252, 333–343, 386–415, 416–475, 719–745, 770–800, 817–823, 838–868, 894–931)
- `git show 99c3bc88…:corpus/knowledge/mutation-case-mado-verify.md` (whole, 323 lines; cites at 3-11, 8-9, 17-23, 44-49, 51-55, 57-59, 66-72, 73, 103-115, 175-176, 187-189, 228-230, 237-238, 240-260, 262-293)
- `git show 99c3bc88…:corpus/knowledge/fleet-suite-census.md` (185–196, 249–262, 280–292)
- `git show 99c3bc88…:tools/mutate-and-run.sh` (25–45, 470–560 workdir/target path, grep of `git`/`porcelain`/`MUTATE_RESTORE`)
- `git show 59c38109bf11:SKILL.md` lines 856–884 (C0 bytes of the same section, for the round's own diff)
- `git diff 59c38109bf11 99c3bc88… -- SKILL.md` (the `@@ -872,11 +872,11 @@` hunk: only the `SKILL.md:808-809 → 819-820` and `SKILL.md:335 → 346-347` pointers moved; the `229-230` pointer is untouched by C1)
- `git show 99c3bc88…:.ufo/evidence/round-18/measure.py` (`sectionize`, to reproduce the sha and span)
- `.ufo/waves/round-54/reader-section.py`
- `.ufo/waves/round-54/spec-w2.json` item[2]
- Historical (context only, not evidence about the final bytes): `.ufo/waves/round-18/w2/CR14.md`, `.ufo/waves/round-27/w1/Read09.md`, `.ufo/waves/round-27/residual/ReRead05.md`

## Commands run

Reader discipline (from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read03`):

```
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 "### The boundaries — what a service run is not"
# -> {"start": 869, "end": 893, "section_sha256": "ff4f6197…16f1d"}
```

Sha reproduction (independent of the reader, via the same frozen `sectionize`): recomputed over the joined 869–893 body → `ff4f61972eec106008e19366e9b643322c95f83bad28b916e08082a233116f1d` (match).

Anchor census (runnable receipt, read-only `git show` only):

```
bash .ufo/waves/round-54/w2/T54W2Read03-receipts/anchor-census.sh
# exit 0; output: .ufo/waves/round-54/w2/T54W2Read03-receipts/anchor-census.out
```

The census prints, for each anchor, the resolved lines at C1; A11/A11b show the `229-230` vs `228-229` boundary, A3b shows the tool quote is wrapped across `:37-38` but still inside the cited `:36-38`.

Byte probes reaching the finding:

```
git show 99c3bc88…:corpus/knowledge/mutation-case-mado-verify.md | awk 'NR>=228&&NR<=230'
git show 99c3bc88…:SKILL.md | awk 'NR>=890&&NR<=893'
git grep -c '229-230' 99c3bc88… -- SKILL.md    # 1 — the only occurrence in the page
```

## Write scope

Files created (all inside the wave-2 directory; nothing else touched):

- `.ufo/waves/round-54/w2/T54W2Read03.json`
- `.ufo/waves/round-54/w2/T54W2Read03.md`
- `.ufo/waves/round-54/w2/T54W2Read03-receipts/anchor-census.sh`
- `.ufo/waves/round-54/w2/T54W2Read03-receipts/anchor-census.out`
- `.ufo/waves/round-54/w2/T54W2Read03-receipts/section-869-893.txt`

`git status --porcelain -- .ufo/waves/round-54/w2/ SKILL.md corpus tools` → `?? .ufo/waves/round-54/w2/` only. No lane file, no production file, no git mutation. Scratch tree `/fast/scratch/hyaku/tameshi-r54/T54W2Read03/` holds the working copies. No tool install or upgrade was needed or performed.
