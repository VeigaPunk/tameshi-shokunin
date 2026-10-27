# T53W1Read07 — cold read of `## Standing rules` at C*

Seat: T53W1Read07 (tameshi round 53, wave 1, hyaku run 10). Read-only cold read of one
SKILL.md section at the frozen content commit. No product file, contract, corpus, tool,
MANIFEST or evidence file was written; the only writes are this report and its JSON
sibling under `.ufo/waves/round-53/w1/`, plus a scratch dir removed before yield.

## Section identity

- Source: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md`
  (git object only; the working tree was never read for section bytes).
- Heading line: `## Standing rules` at `SKILL.md:17`; next heading `## Source notes` at
  `SKILL.md:30` (both 1-based, computed by the frozen-monitor rule: a line matching
  `^#{1,3}(\s|$)` outside ``` fences).
- Section = `SKILL.md:17-28`: heading line through the line before the next heading, with
  the trailing whitespace-only line (`SKILL.md:29`, the blank separator) stripped,
  joined with `\n`, no trailing newline.
- Bytes: **739**; `sha256` = `374964f40ab5ff71fd4713282867b360506d23c1918eb1c627645cdb03639053`.
- Split verification before hashing: the heading index is `16` (0-based), the next heading
  index is `29`, the stripped body is 12 lines, so the 1-based range is 17-28 and the
  stripped line is 29 — reproduced in the builder with `assert hi+1==17 and end+1==30 and
  len(body)==12`, which passed.

## Checks run

All commands read git objects at `a41195dfc13a73958e4c5228ec196b28d03ded03`; none writes outside the seat scratch dir.

1. `git show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md` → 2178 lines, sha256 of the whole blob
   `c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee`.
2. Section split + hash (below).
3. `git grep -hoE 'fast/scratch/hyaku/tameshi-r<NN>/<sub>' a41195dfc13a73958e4c5228ec196b28d03ded03` and the dash variant,
   per round 48-52 (table under F1) — the lane's actual scratch namespace.
4. `git show a41195dfc13a73958e4c5228ec196b28d03ded03:corpus/knowledge/mutation-case-kimi-census.md | sed -n '4,7p'` and
   `...kagi-census.md | sed -n '4,6p'` — the two pointers the section cites.
5. `git show a41195dfc13a73958e4c5228ec196b28d03ded03:PROVINCE.md` (118 lines) + `grep -niE 'write|read-only|edits'` — the
   document the first bullet names.
6. `git show a41195dfc13a73958e4c5228ec196b28d03ded03:corpus/SOURCES.md | grep -c '| rejected |'` → 6.
7. Errata block extracted at `c699c8c` (the commit that introduced the heading) and at
   `a41195dfc13a73958e4c5228ec196b28d03ded03`, then `difflib.unified_diff` over the two section texts.
8. `git log --oneline -S'the wave deliverables are the record' c699c8c..a41195dfc13a73958e4c5228ec196b28d03ded03 -- SKILL.md`
   → `05a2247` (the in-place rewrite of the CR23 row).

## Holds (verified, not findings)

- **Read-only substrates unless PROVINCE.md declares a write surface.** `PROVINCE.md`
  exists at `a41195dfc13a73958e4c5228ec196b28d03ded03` (118 lines) and its own text is read-only in force:
  `PROVINCE.md:16-17` "Never edits a sibling's gate code (read-only probes;
  recommendations travel in round reports)", `:30`, `:55`, `:79`, `:104` "library are
  read-only external surfaces", `:113`. `grep -niE 'write surface'` over `PROVINCE.md`
  returns **0** hits, so the escape hatch is never invoked at C* — the bullet is absolute
  and the recorded practice matches it (every recorded leg works in copies). Unmet
  antecedent, not a falsified statement; no finding.
- **Secrets shape-only, never content-read.** The lane's own note states the practice
  that the rule asks for: `corpus/knowledge/mutation-case-kagi-census.md:6-7` —
  "No external site was contacted; no secret file was / content-read (kagi's 0600
  `stamps.tsv` appears in directory listings by name only)." No counter-example found.
- **Every claim: measured anchor (path:line, command output, evidence id); observation /
  inference / unknown stay separate.** The section is a rule statement; its own bullets
  are anchored by the sibling `.md` files it names, and the two census notes carry an
  explicit `O`/`I`/`U` anchor legend (`mutation-case-kimi-census.md:9-11`). No
  counter-example found.
- **Errata exists and rejections are kept** (the second half of the errata bullet).
  `## Errata — round 16 full-page cold-read` is present at `SKILL.md:1714-1759`, and
  `corpus/SOURCES.md` keeps **6** `| rejected |` rows (S029, S030, S046, S067, S071,
  S080), each with a flip condition.
- **The dated directive clause.** "(host scratch directive of 2026-10-25: `/tmp` is for
  files under 50 MB only; a seat deletes its tree on exit)" is explicitly dated and
  matches the operator directive in force this wave — a dated milestone, so a HOLD.
- **The substrate tree is never a mutation target.** Every recorded leg injects into a
  copy; the two cited notes say so at `mutation-case-kimi-census.md:4-5` and
  `mutation-case-kagi-census.md:4-5`. No counter-example found.

## Findings (3)

### F1 — stale namespace pattern (`stale-namespace-pattern`)

Quote (byte-exact, `SKILL.md:25`):

```
**Scratch namespace is `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)/`<lane>-r<round>-<n>-*/`**
```

Why it fails at C*: the pattern `$HYAKU_SCRATCH/<lane>-r<round>-<n>-*/` is not the shape
the lane's scratch dirs have. Counting the committed paths under the default base, the
dash form (`tameshi-r<NN>-<token>`) appears **0** times for rounds 48-52, while the slash
form (`tameshi-r<NN>/<sub>`) appears thousands of times:

| round | `/fast/scratch/hyaku/tameshi-r<NN>/<sub>` | `/fast/scratch/hyaku/tameshi-r<NN>-<token>` |
|---|---|---|
| 48 | 282 | 0 |
| 49 | 576 | 0 |
| 50 | 4810 | 0 |
| 51 | 2251 | 0 |
| 52 | 148 | 0 |

Round 53, the round this seat runs in, uses the var form of the same slash shape:
`${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r53/deciding`
(`.ufo/evidence/round-53/deciding-run.sh:16`) and
`${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r53/no-harm`
(`.ufo/evidence/round-53/no-harm.sh:11`). This seat's own wave spec assigns
`/fast/scratch/hyaku/tameshi-r53/w1/<seat>/` — again no `-<n>-` component.

The dash form is not invented: it is what rounds **25, 27, 29, 31-36** used (5932
occurrences, 9 distinct round prefixes). The section therefore still prescribes the
round-36-and-earlier naming in a page whose last five landed rounds all use
`<lane>-r<round>/<sub>`. A seat obeying the bullet literally creates
`tameshi-r53-<n>-*`, a name shape no round since 36 uses and one the round-53 evidence
does not contain. Its own recipe agrees with the bullet, not with practice
(`SKILL.md:136` "Scratch for a sweep: `$HYAKU_SCRATCH` (default
`/fast/scratch/hyaku`)/`<lane>-r<round>-<n>-work/`", `SKILL.md:158` the matching
`mkdir -p`), so the drift is between the page and the lane's own scratch dirs.

### F2 — dead receipt (`dead-receipt`)

Quote (byte-exact, `SKILL.md:26-27`):

```
(both mutation lanes kept every mutant + evidence there —
  mutation-case-kimi-census.md:4-7; mutation-case-kagi-census.md:4-6)
```

Why it fails at C*: the parenthetical is the receipt for the base just named
(`$HYAKU_SCRATCH`, default `/fast/scratch/hyaku`). Both cited pointers record the opposite
base — `/tmp`. Verbatim, at C*:

`corpus/knowledge/mutation-case-kimi-census.md:4-7`

```
axis: depth). Substrate: kumitate-shokunin **read-only** — every mutant is a copy under
`/tmp/tameshi-r2-1-work/`, and no fleet file was written. No live `~/.kimi-code` path was
read: every run is `--selftest` (fixtures under the suite's own `mkdtemp` root) or `--root`
pointed at an empty dir under `/tmp`.
```

`corpus/knowledge/mutation-case-kagi-census.md:4-6`

```
axes: depth + operability). Substrate: kagi-shokunin **read-only** — every mutant is a copy under
`/tmp/tameshi-r3-1-work/`, and the kagi tree was not written (restore proof §0); this note is the
only fleet file written by this run. No external site was contacted; no secret file was
```

"there" is the `$HYAKU_SCRATCH` namespace; the two notes it cites put every mutant under
`/tmp/tameshi-r2-1-work/` and `/tmp/tameshi-r3-1-work/`. Both runs are dated 2026-10-14
(`mutation-case-kimi-census.md:3`, `mutation-case-kagi-census.md:3`), eleven days before
the 2026-10-25 directive the same sentence carries, so neither can evidence post-directive
practice under the new base. What the pointers do support is the dir-name shape
(`<lane>-r<round>-<n>-work/`), which is exactly the shape F1 shows the lane no longer
uses — the receipt is load-bearing for neither half of the claim it is attached to.

### F3 — "Errata append-only" is contradicted by the errata block itself (`self-contradiction`)

Quote (byte-exact, `SKILL.md:24`):

```
- Errata append-only; rejections kept.
```

Why it fails at C*: the errata block is edited in place, and says so. The heading lost its
own marker — at `c699c8c` it read `## Errata — round 16 full-page cold-read (append-only)`;
at C* it reads `## Errata — round 16 full-page cold-read` (`SKILL.md:1714`). The phrase
`(append-only)` now survives exactly once in the page — `SKILL.md:1242`, describing
`fleet-kill-rate-ledger.md` — and no longer marks the errata block at all. Existing table
cells were rewritten, not appended:

```
--- c699c8c:SKILL.md
+++ a41195df:SKILL.md
@@ -1,2 +1,2 @@
-## Errata — round 16 full-page cold-read (append-only)
+## Errata — round 16 full-page cold-read
 
@@ -4,7 +4,13 @@
 `97cf436b…3580`, 51 buckets = preamble + 50 headings outside code fences)
-with 30 lane seats; reports `.ufo/waves/round-16/w1/CR*.md`, ledger
-`.ufo/evidence/round-16/coldread/ledger.json`. Wrong expectations were repaired
-in place with the line count of every edited section unchanged, so every
+with 30 cold-read seats (CR01–CR27, three of them with a/b replicas); reports
+`.ufo/waves/round-16/w1/CR*.md`, re-reads `w2/RR*.md` and `w3/RX*.md`, ledger
+`.ufo/evidence/round-16/coldread/ledger.json` (assembled from those reports by
+`coldread/assemble.py`; it holds the merged verdict and gap counts per bucket).
+The page edits are in-place repairs, and so are this table's own cells: a
+later row's corrections of an earlier row stay visible in git
+(`git log -p -- SKILL.md`), not as appended rows. Wrong expectations were repaired
+in place with the line count of every edited section unchanged (except `### Round-15 gate/probe registry`, +1 blank separator; see the round-17 section), so every
 `SKILL.md:<line>` self-anchor still resolves; the old wording stays in git
-(`git show 97cf436b…` is the snapshot blob at commit `e69b488`). Repairs:
+(`git show e69b488:SKILL.md`, sha256 `97cf436b…`; also
+`.ufo/evidence/round-16/coldread/SKILL.snapshot.md`). Repairs:
 
@@ -14,5 +20,5 @@
 | 134-135 | observed cold-read proof covers one historical JS mutant | round 16 executed the recipe end to end (CR04a, CR04b) | CRCritic1 |
-| 61 | live gate "exit lattice 0/1/2 (usage 64)" | kagi folds usage/setup into 2; 64 is kumitate's hermetic usage code (`claim-ledger.sh --bogus-flag` → 2, `claims-check.mjs --bogus-flag` → 64) | CR02 |
-| 269-270 | a two-space substring "produces a *different mutant*" | it yields the byte-identical mutant; the full line keeps `count == 1` robust | CR05 |
-| 277-279 | `${n}` said to appear in the two notes' manifests | `${n}` is in Appendix A's D4 on this page; the notes carry the other three tokens | CR05 |
+| 63 | live gate "exit lattice 0/1/2 (usage 64)" | kagi folds usage/setup into 2; 64 is kumitate's hermetic usage code (`claim-ledger.sh --bogus-flag` → 2, `claims-check.mjs --bogus-flag` → 64) | CR02 |
+| 271-272 | a two-space substring "produces a *different mutant*" | it yields the byte-identical mutant; the full line keeps `count == 1` robust | CR05 |
+| 278-280 | `${n}` said to appear in the two notes' manifests | `${n}` is in Appendix A's D4 on this page; the notes carry the other three tokens | CR05 |
 | 360-361 | D1/D3 "die on the same 16 cases" | 16 cases each, 14 shared | CR06 |
@@ -22,7 +28,12 @@
 | 949-950 | receipt literal `cases=4` | `cases=N`, N per revision | CR16 |
-| 1388, 1392 | mutation-case notes "(six)"; round-11 record "lands" in `plans/` | dated count; the record is `corpus/knowledge/closeout-r11.md` | CR23 |
+| 1390, 1393 | mutation-case notes "(six)"; round-11 record "lands" in `plans/` | dated count; no separate round-11 record file exists (the wave deliverables are the record) | CR23, RR08 (w2) |
 | 1472 | "Box 3 remains `[ ]`" | dated: `[ ]` at that write, `[~]` since | CRCritic1, CRCritic2 |
 | 1614 | `PROTOCOL.md` §Gate standard | `../PROTOCOL.md` (fleet root; the lane holds none) | CR27 |
+| 3, 9-10 | unquoted frontmatter `description:` (strict YAML rejects the second `: `); "Two mutation cases are now measured" | quoted; the first two cases are worked here, seven recorded since round 16 | RR01 (w2) |
+| 1346 | quotes "Four legs at this revision" at `:925-929` | notes that line 925 is dated since round 16 | WholePage (w2) |
+| 1391 | "six-leg registry" | six at round 11, seven since round 16 | RR08, RR11 (w2) |
+| round-15 registry, disposition row | `--root .` said to exit 0 | since round 16 the runner input moved: `--root .` → 2 `expected_input_digest_mismatch` by design; run with `--root` at an extracted `git archive 28aeef4`, from the lane root → 0 | RR10 (w2) |
+| round-16 registry, assemble row | "64 usage" | argparse usage exits 2 | RR13 (w2) |
 
-Minor gaps (non-blocking, kept as named debt in the ledger): dead `/tmp`
+Minor gaps (non-blocking; named in the seat reports, counted in the ledger): dead `/tmp`
 evidence paths in records of rounds 6–9; anchors written as tool sha256 values
@@ -31,2 +42,5 @@
 header schema); `git status --porcelain` on a sibling may take its index lock —
-prefer `git --no-optional-locks -C <repo> status --porcelain`.
+prefer `git --no-optional-locks -C <repo> status --porcelain`; round-7 section
+`tools/mutate-and-run.sh:<line>` anchors predate later growth of the tool
+(CR16, RR07); nested check [51] of round-gate's selftest records itself as a
+skip-as-pass (`round-gate.mjs:1381-1382`).
```

The `| 61 |`, `| 269-270 |` and `| 277-279 |` rows were re-anchored to `63`,
`271-272`, `278-280`; the CR23 row's substance changed (a named record file
`corpus/knowledge/closeout-r11.md` became "no separate round-11 record file exists"); the
intro paragraph gained the sentence at `SKILL.md:1722-1724`: "The page edits are in-place
repairs, and so are this table's own cells: a later row's corrections of an earlier row
stay visible in git (`git log -p -- SKILL.md`), not as appended rows." `git log` confirms
the rewrite commit: `-S'the wave deliverables are the record'` → `05a2247` (round-16 wave
2). So at C* the rule says append-only while the object it governs is revised in place by
design; both cannot hold.

"rejections kept" — the second half of the same bullet — does hold (6 rows, see Holds); the
finding is scoped to "append-only".

## Adjacent observations (checked, not findings)

- The dated `/tmp` placements survive where they are historical: the rounds 2-3 kill-band
  bullet ("Every mutant is a copy under `/tmp/<lane>-r<round>-<n>-work/`",
  `SKILL.md:342-346`) sits in "## Kill-rate bands — admission readings (rounds 2–3,
  measured)", and Appendix A/B are replica recipes (`SKILL.md:543`, `:611`,
  "Replicates TAMESHI-R3-1"). Dated historical milestones explicitly marked as dated are
  HOLDS, so they are not counted as findings here.
- `.ufo/evidence/round-53/c2/measure.py:19` states as a premise: "sweep recipe's scratch
  lines name $HYAKU_SCRATCH, not /tmp." At C* that is true of the live recipe
  steps (`SKILL.md:136`, `:158`) and false of the dated readings (`SKILL.md:342-346`) and
  of Appendix A/B (`:543`, `:611`), which still spell `W=/tmp/<lane>-r<round>-<n>-work`.
  The tool's four `FLEET_DOC_PATTERNS` do not match those dated strings, so the check
  passes; only the prose premise overstates. Reported here, not as a finding about this
  section.
- The escape-hatch vocabulary: `PROVINCE.md` never uses the phrase "write surface"
  (0 hits). The first bullet's conditional is therefore never triggered at C*; the lane
  writes its own tree under PROVINCE's "Owns" list, not under a declared write surface.
  Named for the L1, not raised as a finding — the statement is not falsified, only its
  escape hatch is undefined.

## Seat hygiene

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read07` (created with `mkdir -p`,
  removed with `rm -rf --` before yield; the report and JSON live in the wave dir only).
- No git/jj mutation, no commit, push, fetch or prune; no pacman; no tool install; no
  network use. Reads were `git show`/`git grep`/`git log` and local `grep`/`sed` over a
  dumped object copy in scratch.
- Deliverables: `.ufo/waves/round-53/w1/T53W1Read07.json`, `.ufo/waves/round-53/w1/T53W1Read07.md`.
