# RX1 — cold-read re-read, SKILL.md lines 1–16

Seat: TameshiR16.RX1 (fresh reader). Range: lines 1–16 (preamble 1–5 + heading `# tameshi-shokunin` at 6). Next heading is at 17 (`## Standing rules`), so the section under review is H1 + the single intro paragraph.

**Verdict: record section, structurally true — two minor prose defects in the line-10 wave-2 splice (M1, M2), no blocking gap.**

## Identity / scope evidence

| check | command | result |
|---|---|---|
| lane commit present | `git -C … rev-parse --verify 05a2247…^{commit}` | `05a224754db3c6fce18f5ec1816a6873bffe3d0e`, exit 0 |
| page sha256 | `git show 05a2247…:SKILL.md \| sha256sum` | `e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3` — matches assigned sha |
| page size | `git cat-file -s …:SKILL.md` | `127245` bytes, 1807 lines |
| drift | `git rev-parse HEAD`; `git --no-optional-locks status --porcelain -- SKILL.md`; `git log 05a2247..HEAD -- SKILL.md`; `git diff --stat 05a2247 -- SKILL.md` | HEAD == 05a2247; all three outputs empty — worktree and history identical to the revision I read |
| trailing byte | `git cat-file blob …:SKILL.md \| tail -c 20 \| xxd` | last bytes are `… space, pipe` (`ac 6c 65 20 c2 b7 20 31 20 69 74 20 66 61 69 6c 73 20 7c`) with **no** final newline (file-level observation, outside this range; not counted as a section gap) |

Range bytes were captured once to `/tmp/tameshi-r16w2-RX1-rM4Rt6/page.md` (exact committed bytes, sha re-verified there = e289…). All line-level facts below are from lines 1–16 only.

## Frontmatter strict YAML parse (target instruction)

Frontmatter extracted as lines 2–3 (delimiters `---` at 1 and 4, blank line 5).

- PyYAML 6.0.3 on CPython 3.14.8: `yaml.parse` OK (10 events); `yaml.compose` → `MappingNode tag:yaml.org,2002:map` with exactly two `ScalarNode` keys, both `tag:yaml.org,2002:str`; `description` scalar style `"` (double-quoted), `name` plain, no duplicate keys, no anchors/aliases, no non-core tags.
- `yaml.safe_load` → `dict` keys `['name','description']`:
  - `name` = `str`, len 16, `'tameshi-shokunin'`;
  - `description` = `str`, len 73, `'Domain specialist — verification-fixture craft. Rank: shonen (probation).'`, em dash preserved as U+2014.
- Cross-check Psych 5.2.2: `YAML.safe_load(fm, permitted_classes: [], aliases: false)` → `Hash` with the same two `String` values. Both strict loaders agree.
- In-range consistency: frontmatter `name` equals the H1 text `# tameshi-shokunin`; description phrase “verification-fixture craft” matches line 8 “verification-fixture craft playbook”.

**Result: frontmatter is valid strict YAML; no defect.**

## Classification

Lines 6–16 contain no imperative addressed to a reader — H1 plus a descriptive paragraph about provenance, page structure, and what round 16 added. **Class: record.** (The only instruction in play is the target's “parse the frontmatter”, which was executed.)

## Anchor checks for the record

Method note: the cold-read interface forbids opening SKILL.md lines outside 1–16, so I did **not** read section bodies. Anchors were taken from (a) heading lines only (`grep -nE '^#{1,6} '`), (b) a fence-aware pass to discard `#` code comments, and (c) numeric aggregates (counts, wrap widths). No out-of-range content was disclosed or relied on for wording.

| claim cluster (range) | anchor at 05a2247 | result |
|---|---|---|
| “Rounds 1–3 built the corpus from measured surfaces” (8–9) | `## Kill-rate bands — admission readings (rounds 2–3, measured)` (314); `## Cross-language divergence — bash vs JS (round 3, measured)` (405) | supported |
| “this page carries the method as an executable recipe: numbered steps from pin to restore proof” (10–11) | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (131); `## Restore discipline — proof the substrate never moved` (375) | supported |
| “defect templates with exact-string guidance” (12) | `## Defect-taxonomy templates and exact-string guidance` (246) | exact match |
| “kill-rate bands” (12) | heading 314 | supported |
| “the measured bash-vs-JS divergences” (13) | heading 405 | supported |
| “complete reproduce specs for both cases (Appendix A / Appendix B)” (13–14) | `## Appendix A — worked example: JS case (reproduce from this page alone)` (527); `## Appendix B — worked example: bash case (reproduce from this page alone)` (594) | referents exist; “complete” is body-level, unverified |
| “seven recorded since round 16” (10) | count corroborated: `## Third case — cross-author confirmation (round 5, measured)` (668), `## Six-case confidence statement (round 8, measured)` (1092), `## Seventh recorded case and full-page cold-read — round 16` (1749) | count = 7 ✓; wording conflicts — see M2 |
| “Historical cold-read proof covers one JS mutant only; round 16 adds a full-page cold-read (Errata — round 16)” (14–15) | `## Errata — round 16 full-page cold-read (append-only)` (1707) | errata referent exists; “one JS mutant only” is body-level, unverified |
| fence integrity of the H1 | fence count in 1–16 = 0; fence-aware scan shows line 6 is the only genuine H1 (`# write driver`, `# survivor probes`, `# expect:` at 549/552/618/621/1768 are code comments) | supported |

## Findings

### M1 (minor) — line 10 is a wrap/splice break

`NR=10` is **117 chars / 121 bytes**; the other seven prose lines of the same paragraph are 69–78 chars (8=78, 9=77, 11=77, 12=69, 13=77, 14=75, 15=76). Page-wide, fence-aware, non-table prose (1302 lines): median 74, p99 87, only 11 lines >90 chars, and 117 is the **3rd-longest** prose line in the whole page (behind 126 @1535 and 121 @1581). Exact line text:

`— round 2 JS, round 3 bash, both 8/10 killed — are worked here (seven recorded since round 16), and this page carries`

Impact: readability/wrap only; no semantic loss. Cause [INFERENCE] consistent with the wave-2 “SKILL residuals” edit joining what were two wrapped lines and inserting a parenthetical mid-clause (the wave-2 commit message names “SKILL residuals”).

### M2 (minor) — “seven recorded since round 16” is temporally imprecise

Literal reading = seven cases recorded from round 16 onward. The page's own chronology contradicts that: the 3rd case is bound to round 5 (668), the six-case statement to round 8 (1092), and only the 7th to round 16 (1749). Intended meaning must be “seven recorded **as of** round 16”. Secondary problem: the parenthetical sits inside the clause about the *first two* cases, so “seven” initially reads as a count of the two worked cases.

Suggested exact string: `(seven recorded as of round 16)` — or move the count out of the clause: `… are worked here, and this page carries the method … (seven cases recorded as of round 16)`.

No blocking gaps; no wrong expectations observed (nothing in the range sets an expectation the artifact fails).

## Residual risk / verification gaps

- Body-level claims left unverified by design: “both 8/10 killed”, “every rule below earns a cited source” (aggregate only: 25 case-insensitive `source` lines, 2 `source:` across 1807 lines — presence, not per-rule coverage), “Historical cold-read proof covers one JS mutant only”, and the “complete” qualifier on the appendices. These require lines outside 1–16, which the cold-read interface forbids opening; they are **not** counted as defects.
- Heading enumeration includes `#` code-comment lines; I confirmed via fence tracking that no such line was used as an anchor, so no false-positive anchor entered this report.
- No commands in this range required execution; nothing was run in /tmp beyond parsing and aggregation.
- No tools installed or upgraded.
- Scratch: `/tmp/tameshi-r16w2-RX1-rM4Rt6` (`page.md` = exact committed bytes). Report write is the only lane write.

**One-line verdict:** record section verified (referents and count hold); two minor prose defects at line 10 (wrap splice M1, imprecise “since round 16” M2) — non-blocking.

```json
{"seat":"RX1","skill_sha256":"e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3","sections":[{"start":1,"heading":"","class":"record","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[],"commands_executed":["git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --verify 05a224754db3c6fce18f5ec1816a6873bffe3d0e^{commit}","git show 05a224754db3c6fce18f5ec1816a6873bffe3d0e:SKILL.md | sha256sum","git cat-file -s 05a224754db3c6fce18f5ec1816a6873bffe3d0e:SKILL.md","python3 PyYAML 6.0.3 yaml.parse/yaml.compose/yaml.safe_load on lines 2-3","ruby -ryaml Psych 5.2.2 YAML.safe_load(permitted_classes: [], aliases: false) on lines 2-3"],"opened":["SKILL.md:1-16"],"scratch":"/tmp/tameshi-r16w2-RX1-rM4Rt6"},{"start":6,"heading":"# tameshi-shokunin","class":"record","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["M1 line 10 is 117 chars vs 69-78 for every other line of the same paragraph; 3rd-longest of 1302 page-wide prose lines (median 74, p99 87) - wrap/splice break","M2 '(seven recorded since round 16)' reads as seven cases since round 16, but cases 3-6 predate it (rounds 5 and 8 per headings 668/1092) and only the 7th is round 16 (heading 1749); should read 'as of round 16', and the parenthetical interrupts the clause about the first two cases"],"commands_executed":["grep -nE '^#{1,6} ' on committed page (heading lines only)","awk/python line-length and fence-aware prose-width histogram (numeric aggregates only)","grep -c -i for source/corpus/round/measured counts (counts only)","git --no-optional-locks status --porcelain -- SKILL.md; git log 05a2247..HEAD -- SKILL.md; git diff --stat 05a2247 -- SKILL.md"],"opened":["SKILL.md:1-16","SKILL.md heading lines only (no section bodies outside 1-16)"],"scratch":"/tmp/tameshi-r16w2-RX1-rM4Rt6"}]}
```

Correction (L1 review): the preamble is a record whose in-range checks all passed, so its verdict is `verified-record` — `executed-ok` is reserved for instruction sections. This block supersedes the one above; the last block is the authoritative one.

```json
{"seat":"RX1","skill_sha256":"e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3","sections":[{"start":1,"heading":"","class":"record","verdict":"verified-record","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[],"commands_executed":["git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --verify 05a224754db3c6fce18f5ec1816a6873bffe3d0e^{commit}","git show 05a224754db3c6fce18f5ec1816a6873bffe3d0e:SKILL.md | sha256sum","git cat-file -s 05a224754db3c6fce18f5ec1816a6873bffe3d0e:SKILL.md","python3 PyYAML 6.0.3 yaml.parse/yaml.compose/yaml.safe_load on lines 2-3","ruby -ryaml Psych 5.2.2 YAML.safe_load(permitted_classes: [], aliases: false) on lines 2-3"],"opened":["SKILL.md:1-16"],"scratch":"/tmp/tameshi-r16w2-RX1-rM4Rt6"},{"start":6,"heading":"# tameshi-shokunin","class":"record","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["M1 line 10 is 117 chars vs 69-78 for every other line of the same paragraph; 3rd-longest of 1302 page-wide prose lines (median 74, p99 87) - wrap/splice break","M2 '(seven recorded since round 16)' reads as seven cases since round 16, but cases 3-6 predate it (rounds 5 and 8 per headings 668/1092) and only the 7th is round 16 (heading 1749); should read 'as of round 16', and the parenthetical interrupts the clause about the first two cases"],"commands_executed":["grep -nE '^#{1,6} ' on committed page (heading lines only)","awk/python line-length and fence-aware prose-width histogram (numeric aggregates only)","grep -c -i for source/corpus/round/measured counts (counts only)","git --no-optional-locks status --porcelain -- SKILL.md; git log 05a2247..HEAD -- SKILL.md; git diff --stat 05a2247 -- SKILL.md"],"opened":["SKILL.md:1-16","SKILL.md heading lines only (no section bodies outside 1-16)"],"scratch":"/tmp/tameshi-r16w2-RX1-rM4Rt6"}]}
```
