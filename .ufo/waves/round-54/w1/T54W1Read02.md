# T54W1Read02 — cold read of `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`

Seat: T54W1Read02 (scribe). Lane read-only; no lane file edited. Round-54 wave 1,
milestone C1 cold-read re-read at C0.

- heading: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`
- cand: `59c38109bf119d0e9d4f878644a82babc937bc1e`
- section span at C0: `start=142 end=256`; the sha is over `SKILL.md` lines 142-255
  (verified: joining lines[141:255] of the C0 `git show` output hashes to the value below)
- section_sha256: `c413b4268eb842637f17df2396d06ab53cbffe5ba4fb063b6ee37165a800e65e`

Span/sha receipt:

```
$ export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read02
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf119d0e9d4f878644a82babc937bc1e "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence"
{"heading": "## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 142, "end": 256, "section_sha256": "c413b4268eb842637f17df2396d06ab53cbffe5ba4fb063b6ee37165a800e65e"}
```

The section bytes are **identical at base and at C0** (same sha `c413b426`; the span only
moved 134→142 because C0 inserted 8 lines above it), so every `SKILL.md:<line>` anchor used
below is a C0 line number, and the section text I cold-read is the text it had at base.

Verdict: two minor gaps, no blocking gap, no wrong expectation. Both are reported as
findings because each is a rule the section states that its own cited evidence refutes; both
are re-read artefacts of the section as it stands at C0 (neither was introduced by C0).

---

## Finding 1 — step 4's one-per-class rule is refuted by the exemplar it names

quote (byte-exact in the section and in this file):

`defects, one per class`

Section line 172-176 reads:

```
4. **Write the defect list from the templates.** 8–12 defects, one per class
   (catalog + entry template in the next section), each ONE exact-string
   replacement or single block deletion, each with a pre-registered
   `expect: killed|survived` and the reason — the JS 10-defect manifest is the
   shape (corpus/knowledge/mutation-case-kimi-census.md:41-53, :155-166).
```

Why it does not hold: the manifest named as "the shape" has two defects in one class, by its
own accounting, and the bash exemplar repeats the pattern.

```
$ git -C . show 59c38109...:corpus/knowledge/mutation-case-kimi-census.md | sed -n '44,45p;47,48p;55p'
| D1 | off-by-one count | K2 counted dir `counted: 18` → `17` (kimi-census.mjs:105) | ... | **killed** | ...
| D2 | off-by-one count (findings cap) | `findings.slice(0, 6)` → `slice(0, 5)` (kimi-census.mjs:378) | ... | **survived** | 0 |
| D4 | dropped arm | root-stray reporting loop deleted (kimi-census.mjs:351-353) | ... | **killed** | 3 |
| D5 | dropped arm (presence gate) | chain presence `gens.length > 0` → `true` (kimi-census.mjs:255) | ... | **killed** | 1 |
By class: off-by-one 1/2 · inverted condition 1/1 · dropped arm 2/2 · wrong mode pin 1/1 ·

$ git -C . show 59c38109...:corpus/knowledge/mutation-case-kagi-census.md | sed -n '70,71p'
| B4 | dropped branch | symlink arm deleted (`:200-204`) | 1 | `1/16` / FAIL | **killed** | 1 (symlink-swap) |
| B5 | dropped branch | exec x-bit arm deleted (`:214-217`) | 0 | `16 cases` / PASS | **survived** | 0 |
```

The kimi note's by-class tally at :55 is the decisive line: it counts `off-by-one 1/2` and
`dropped arm 2/2`, i.e. two defects per class — so the parenthetical labels ("(findings cap)",
"(presence gate)") are not a second-class escape, and the section's "one per class" rule
contradicts the manifest the same sentence calls "the shape". A reader who follows the rule
cannot reproduce the cited example; a reader who follows the example violates the rule.
Smallest fix: state the rule as "8-12 defects, at most one per class family unless the class
has a distinct sub-mechanism, and say which" — or drop the claim that the 10-defect manifest
is the shape of a one-per-class list.

This same gap was recorded by round-27 seat Read03 (`.ufo/waves/round-27/w1/Read03.md`,
minor_gaps[2], "Step 4 says 'one defect per class' ... but the manifests it names as the
shape do not follow that rule") and is still present byte-for-byte at C0. Of that seat's
seven minor gaps, the step-9 repo-revision omission, the `SELFTEST: FAIL (1/16 cases)`
citation, the `n/m pass` wording and the run-together tokens are repaired at C0; the
maintained-instrument gap is partially repaired (the driver is now named at `:434` and
`:579-583`, but the section still does not say which kill-rate rule governs); the unversioned-
scratch-driver caveat is not carried; this one-per-class gap is unchanged.

## Finding 2 — step 9 compares a size that step 2 never records

quote (byte-exact in the section and in this file):

`size and mtime unchanged`

Step 2 (C0 `SKILL.md:160-163`) records exactly this set:

```
2. **Pin the artifact — committed bytes only.** Record: path, full sha256,
   mtime, repo revision, and `git status --porcelain --
   <path>` empty (corpus/knowledge/mutation-case-kimi-census.md:13-16;
```

Step 9 (C0 `SKILL.md:234-236`) then says:

```
9. **Restore + prove endpoint identity.** Re-run step 2's checks (repo revision included; neither model note records an after-revision)
   sha256 after == before, size and mtime unchanged, `git status --porcelain --
```

Why it does not hold: "Re-run step 2's checks" yields path, sha256, mtime, repo revision and
`git status`, but no **size**, so the "size ... unchanged" comparison has no before value.
The omission is not hypothetical: both pin records the sentence cites do carry a byte size,
so the recipe's own instruction set is the incomplete part.

```
$ git -C . show 59c38109...:corpus/knowledge/mutation-case-kimi-census.md | sed -n '13,14p'
Artifact under test (O: `sha256sum`, `stat`, `git rev-parse`): sha256
`83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, 896 lines, 43273 B,
$ git -C . show 59c38109...:corpus/knowledge/mutation-case-kagi-census.md | sed -n '13,14p'
Artifact under test (O: `sha256sum`, `stat`, `git`): sha256
`275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, 44212 B, 886 newlines (the
```

Smallest fix: add `size` to step 2's record list (the two notes already print it), so step 9's
"size and mtime unchanged" has a recorded before value to re-read.

---

## What I opened (all at C0 unless stated) and what I checked

Reader setup: frozen sectionize loaded from `.ufo/evidence/round-18/measure.py` via
`.ufo/waves/round-54/reader-section.py`; every read is `git show 59c38109…:<path>`, never a
working-tree read.

1. `SKILL.md:142-255` — the section itself, read line by line with `repr` to catch broken
   spans (three code spans wrap a line: `git status --porcelain -- / <path>` twice and
   `SURFACE OK … (exec / 644)`; all render correctly, none is a defect).
2. `SKILL.md:17-40` (`## Standing rules`) — to test the section's scratch sentence
   (`$HYAKU_SCRATCH` default `/fast/scratch/hyaku`, `<lane>-r<round>/<sub>/`, deleted on
   exit). Standing rules states all three; consistent.
3. `SKILL.md:257-323` (`## Defect-taxonomy templates and exact-string guidance`) — the
   "next section" step 4 points at; it exists and carries the 12-class catalog + entry
   template. Resolves.
4. `SKILL.md:386-415` (`## Restore discipline`) — step 9's pointer; item 1 says
   "endpoint identity, not that no transient write occurred", item 7 allows recording a
   dirty pin. Step 9's "endpoint identity, not the absence of a transient write" matches
   item 1. Note: item 7's "record the dirty state exactly, or better, stop and re-pin" is
   looser than step 2's flat "If the path is dirty: stop." — considered and **not** reported
   (step 2 is the recipe's hard rule and Restore item 7 is a general checklist entry, not a
   competing recipe rule).
5. `SKILL.md:1733-1780` (`## Errata — round 16 full-page cold-read`) — the opening sentence's
   "round 16's full-page cold-read executed it end to end (two seats)"; the errata table's
   row 134-135 says exactly that, crediting CR04a and CR04b. Resolves.
6. `corpus/knowledge/mutation-case-kimi-census.md` (C0) lines 1-58, 60-110, 150-210 —
   every kimi citation in the section: `:4-7`, `:13-16`, `:20-21`, `:22-25`, `:26-28`,
   `:29-31`, `:30-33`, `:34-35`, `:41-53`, `:59-76`, `:82-99`, `:155-166`, `:183-191`,
   `:204-205`. All present and semantically as cited; `:55-57` is the by-class tally used
   in Finding 1.
7. `corpus/knowledge/mutation-case-kagi-census.md` (C0) lines 1-60, 62-130, 178-215,
   240-262 — every kagi citation: `:13-17` (incl. "the 887th line carries no trailing
   newline"), `:24-38`, `:27-35`, `:42-43`, `:44-45`, `:44-47`, `:48-49`, `:50-53`,
   `:54-56`, `:67`, `:82-103`, `:88-91`, `:111-114`, `:118-122`, `:184-191`, `:203-204`,
   `:252-254`. All present and semantically as cited; `:70-71` is the second exemplar used
   in Finding 1.
8. `corpus/knowledge/gates-survey-kumitate.md:1-40` — the `n/m cases passed` claim
   (`:19-31` table: cite-check `62/62 cases passed (hermetic)`, surface-probe `42/42 cases
   passed`, both `VERDICT: PASS`). Resolves.
9. `corpus/knowledge/gates-survey-kagi.md:495-575` — the "errata block" step 2 cites; the
   G-R2-1 entry at `:554-566` records the intermediate-dirty-state pin and its re-pin.
   Resolves.
10. `corpus/README.md:11` — the `G-R2-1` row step 2 cites. Resolves.
11. `tools/mutate-and-run.sh:420-445, 500-560, 560-595` — the two driver anchors:
    `:434` is the `APPLY FAIL … old-string-count=%d expected=1` print (step 5), and
    `:579-583` is the `pct` division plus the `MUTATE: DEGRADED` exit-1 branch (step 7);
    `total` at `:516` is every defect in the spec, so "divides by every defect" is accurate.
    Both anchors resolve at C0.
12. `.ufo/waves/round-27/w1/Read03.md` — the "corrected in round 27, seat Read03" claim in
    step 9. The report exists in the C0 tree and its wrong_expectations[0] is exactly the
    step-9 endpoint-identity correction the section now carries. Resolves.
13. `.ufo/evidence/round-54/c1/measure.py` + `c1/lost-headings-at-base.json` /
    `lost-headings-at-c0.json` — the heading is in both lost sets; the section text is not
    the cause (identical bytes at base and C0), so the credit loss is the input-keyed drift
    the round describes, not a text defect a reader can fix.

## Considered and not reported (reasons)

- **No per-defect `expect:` in the cited shape.** Step 4 asks for a pre-registered
  `expect:` and names the JS manifest as the shape, but that manifest lists class/edit/verdict
  columns and only §5 E1 records that expectations existed (and D7's was wrong). Not reported
  as a finding: the manifest is cited for the defect-list shape and E1 does evidence
  pre-registration; the next section's entry template carries the `expect:` line. A reviewer
  could still call it a gap, but it is a reading of what "shape" covers, not a contradiction.
- **Which kill-rate rule governs.** Step 7 defines `killed / (killed + survived)` and states
  the maintained driver "divides by every defect and marks the run DEGRADED"
  (`:579-583`, verified). The section discloses the divergence rather than resolving it.
  Not reported: the parenthetical is an explicit disclosure with the driver's line cited, so
  a reader knows the driver's number is degraded; the recipe's own definition is stated first.
- **Step 5's required literal `all unique` vs the in-tree driver.** `grep -n 'all unique'
  tools/mutate-and-run.sh` at C0 returns nothing; the driver prints `APPLY OK …
  old-count=1` on success (`:442`). The section credits `all unique` to "both lanes'
  drivers" (the two historical scratch drivers) and cites the maintained driver only for
  "the failing count" (`:434`), so the sentence is not self-contradictory. Not reported.

## Conformance and hygiene

- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → `tameshi ok
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, exit 0.
- No lane file edited; SKILL.md and every corpus/tool file were read through `git show` at C0
  only. No git mutation was run anywhere: only read-only subcommands (`show`, `log`,
  `ls-tree`, plus the frozen `reader-section.py`'s internal `rev-parse` and
  `sources-census.sh validate`).
- Tool installs this seat: none.
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1Read02` used for the `TMPDIR` of
  `reader-section.py` and for two `git show` dumps; removed at seat end (`rm -rf`), no tree
  left behind. Nothing written outside
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/`.
