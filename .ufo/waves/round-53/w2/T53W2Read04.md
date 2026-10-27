# T53W2Read04 — wave-2 re-read: `## Standing rules` at C**

Seat T53W2Read04 (tameshi round 53, hyaku run 10, wave 2). Re-read of one section at the wave-2
content commit C** = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`. Every section byte below was read
from that git object; the working tree was never used for section content. No product file,
contract, corpus, tool, MANIFEST or `.ufo/evidence/` file was written; the only writes are this
report and its JSON sibling under `.ufo/waves/round-53/w2/`, plus the seat scratch removed before
yield.

Scope reminder: the wave-1 reader of this heading filed three findings (F1 the
`<lane>-r<round>-<n>-*/` pattern, F2 the dead `/tmp` receipt, F3 "Errata append-only"), and the L1
applied a fix pass. This seat verifies the three named fixes in the C** bytes **first**, then reads
the section for anything else that does not hold at C**.

## Section identity and hash (reproduced, not copied)

- Source: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md`
  → 2,189 lines, 197,139 bytes, blob sha256 `4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d`
  (`git rev-parse <rev>:SKILL.md` → `3afe0fa87a81bb082457dee04c0d42c3c7461811`).
- Split by the frozen monitor rule (line matching `^#{1,3}(\s|$)` outside ``` fences): the
  `## Standing rules` heading is **line 17**; the next heading `## Source notes` is **line 33**.
  Section = lines 17–31 (the whitespace-only separator at line 32 stripped), 15 lines, **1,145
  bytes**, no trailing newline.
- `sha256` of the UTF-8 (`surrogateescape`) section bytes:
  `828e0431106ed44ebab2e939ad2c1e58be2bf8c3a3cf8ef17a3bb9515049b3ba`.
- Split verified before hashing, twice and independently:
  1. the seat's own builder asserts heading index 16 (0-based), next heading index 32, stripped body
     `SKILL.md:17-31`, and prints `line32 == ''`, `line33 == '## Source notes'` — passed;
  2. the frozen round-18 `sectionize` (`.ufo/evidence/round-18/measure.py`, loaded with
     `spec.loader.exec_module` and run on the raw C** bytes) returns
     `{'start': 17, 'end': 32, 'heading': '## Standing rules', 'sha256':
     '828e0431106ed44ebab2e939ad2c1e58be2bf8c3a3cf8ef17a3bb9515049b3ba'}` and reports 64 sections
     in the file — the same count the contract's C1 predicate uses.
  Both agree; `section_sha256` in the JSON is that value.

The three fixes were located by diffing the section at C* (`a41195dfc13a73958e4c5228ec196b28d03ded03`,
section sha256 `374964f40ab5ff71fd4713282867b360506d23c1918eb1c627645cdb03639053`) against C**.

## Fix verification (run first)

### V1 — scratch shape `<lane>-r<round>/<sub>`: PRESENT

Quote (byte-exact, `SKILL.md:28`):

```
`$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)/`<lane>-r<round>/<sub>/`
```

The C* dash-form string (the old `$HYAKU_SCRATCH/<lane>-r<round>-<n>-*/` pattern) is gone from the
bullet (it survives later in the same line only as the explicitly historical form). The C** shape
matches current practice: the round-53
evidence scripts bind `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r53/deciding`
(`.ufo/evidence/round-53/deciding-run.sh:16`) and `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r53/no-harm`
(`.ufo/evidence/round-53/no-harm.sh:11`), and this wave's seats sit at
`/fast/scratch/hyaku/tameshi-r53/w2/<seat>/`. The fix itself landed; its supporting justification
does not (finding F1 below).

### V2 — historical `/tmp` parenthetical: PRESENT and now true of its citations

Quote (byte-exact, `SKILL.md:29-30`):

```
(in the original `/tmp` namespace: both mutation lanes kept every mutant + evidence there —
  mutation-case-kimi-census.md:4-7; mutation-case-kagi-census.md:4-6)
```

The parenthetical now marks the `/tmp` base as the *original* namespace instead of attaching it to
`$HYAKU_SCRATCH`. The two cited ranges support it at C**:

```
axis: depth). Substrate: kumitate-shokunin **read-only** — every mutant is a copy under
`/tmp/tameshi-r2-1-work/`, and no fleet file was written. No live `~/.kimi-code` path was
read: every run is `--selftest` (fixtures under the suite's own `mkdtemp` root) or `--root`
pointed at an empty dir under `/tmp`.
```
(`corpus/knowledge/mutation-case-kimi-census.md:4-7`)

```
axes: depth + operability). Substrate: kagi-shokunin **read-only** — every mutant is a copy under
`/tmp/tameshi-r3-1-work/`, and the kagi tree was not written (restore proof §0); this note is the
only fleet file written by this run. No external site was contacted; no secret file was
```
(`corpus/knowledge/mutation-case-kagi-census.md:4-6`)

"kept every mutant + evidence there" is corroborated in the same two documents at
`mutation-case-kimi-census.md:150` ("Scratch (all under `/tmp/tameshi-r2-1-work/`)") and `:171`
(`mkdir -p /tmp/tameshi-r2-1-work/evidence`), and `mutation-case-kagi-census.md:210`, `:242`. Wave-1's
F2 (pointers record the opposite base) is repaired: the base the pointers record is now the base the
sentence names.

### V3 — errata-bullet nuance: PRESENT and consistent with the block it cites

Quote (byte-exact, `SKILL.md:24-27`):

```
- Errata append-only: new errata entries are appended and prior entries never
  rewritten; a documented correction may supersede an entry's content and the
  block says so (the round-16 errata block, `## Errata — round 16 full-page
  cold-read`, discloses its own in-place repairs). Rejections kept.
```

- The named heading exists at C** with the quoted text exactly: `SKILL.md:1725` is
  `## Errata — round 16 full-page cold-read` (no `(append-only)` suffix, and the bullet does not
  claim one).
- The block does disclose its own in-place repairs: its intro reads "The page edits are in-place
  repairs, and so are this table's own cells: a later row's corrections of an earlier row stay
  visible in git (`git log -p -- SKILL.md`), not as appended rows." (`SKILL.md:1733-1735`), and the
  same paragraph keeps the re-anchoring debt ("except `### Round-15 gate/probe registry`, +1 blank
  separator"). So the "may supersede … and the block says so" carve-out is satisfied by the block
  it points at; the C* contradiction wave-1 reported is gone.
- "Rejections kept" holds: `corpus/SOURCES.md` carries 6 `| rejected |` rows
  (`git show C**:corpus/SOURCES.md | grep -c '| rejected |'` → 6).

## Finding (1)

### F1 — the justification clause misdates the scratch-shape transition (`stale-as-current`; also self-contradicts the page's live recipe)

Quote (byte-exact, `SKILL.md:28`):

```
the shape every landed round since 37 uses — the older `<lane>-r<round>-<n>-*` dash form died at round 36
```

Why it does not hold at C**: the lane's landed rounds 37–47 do **not** use the slash shape; their
committed artifacts name the dash form under `/tmp` thousands of times, and the slash shape becomes
uniform only at round 48. Measured over the whole C** tree (committed path strings only):

```
round  /fast/scratch/hyaku/tameshi-r<N>/   /fast/scratch/hyaku/tameshi-r<N>-   /tmp/tameshi-r<N>-
   35                                    0                                1716                   66
   36                                    0                                 155                   48
   37                                    0                                   0                   18
   38                                    0                                   0                   10
   39                                    0                                   0                  155
   40                                    0                                   0                  164
   41                                    0                                   0                  213
   42                                    0 (1 × /tmp/tameshi-r42/)          0                  154
   43                                    0                                   0                  247
   44                                    0                                   0                  115
   45                                    0                                   0                 1712
   46                                    0                                   0                  595
   47                                    0                                   0                  400
   48                                  301                                   0                    0
   49                                  638                                   0                    0  (+4 × `$HYAKU_SCRATCH/tameshi-r49/…`)
   50                                 4822                                   0                    0
   51                                 2258                                   0                    0  (+10 × `$HYAKU_SCRATCH/tameshi-r51/…`)
   52                                  160                                   0                    0  (+6 × `$HYAKU_SCRATCH/tameshi-r52/…`)
   53                                    6 (round-53 evidence scripts + per-seat wave specs)  0   11 (round-17 trace fixtures *named* CR53, not round-53 scratch)
```

Command (both passes at C**, no working tree):

```
git -C <lane> grep -h -o -E '(/fast/scratch/hyaku|/tmp)/tameshi-r([0-9]+)([-/])' 5b703c6f
git -C <lane> grep -h -o -E '\$HYAKU_SCRATCH/tameshi-r([0-9]+)([-/])'            5b703c6f
```

Sample paths, round 47 (last dash round) and round 48 (first slash round):

```
/tmp/tameshi-r47-deciding
/tmp/tameshi-r47-T47ConnCross
/tmp/tameshi-r47-T47CritC1Claim
/fast/scratch/hyaku/tameshi-r48/deciding
/fast/scratch/hyaku/tameshi-r48/L1
/fast/scratch/hyaku/tameshi-r48/T48A2ConnLessons
```

Rounds 37–47 are landed rounds, not drafts: `SCORECARD.md` carries `## Round 37` … `## Round 47`
(e.g. `## Round 45 — held-row live re-verification (freshness) + GoogleTest F3 adoption (2026-10-25)`,
`## Round 47 — dependence-declaring standing rows; mutant-pool hardening; F3 measurement ground`),
`LOG.md` carries round entries for 39–47 (41, 42, 45, 46 and 47 dated `2026-10-25`, the directive's
own date), and `.ufo/evidence/round-37..47/` hold committed counters and receipts. Their committed scratch
references are 3,783 dash-form paths under `/tmp` and one slash path — i.e. of the 16 landed rounds
since 37, eleven (37–47) use the form the sentence calls dead.

Both readings of the clause fail, so the whole span is unrepairable as written:

1. Read as "the dash form ended at round 36" — false: it continues through round 47 (round 45 alone
   has 1,712 committed `/tmp/tameshi-r45-*` references, e.g. `.ufo/evidence/round-45/freshness/integrate.py:22`
   defaults `--glob` to `/tmp/tameshi-r45-ExecRows*/S[0-9][0-9][0-9].json`; round 46's deciding run
   defaults `WORK=${4:-/tmp/tameshi-r46-deciding}`, `.ufo/evidence/round-46/deciding-run.sh:20`).
   The literal numeric form spelled in the sentence (`<lane>-r<round>-<n>-*`) occurs only at rounds
   2, 3 and 4 (171 / 174 / 1,407 matches of
   `(/fast/scratch/hyaku|/tmp)/tameshi-r([0-9]+)-([0-9]+)`), not at round 36 either.
2. Read as "the dash form died at round 36 *under `$HYAKU_SCRATCH`*" — then "the shape every landed
   round since 37 uses" is false for the same eleven rounds, which used `/tmp`, not the namespace.

The clause also contradicts the page's own live instruction. The mutation-sweep recipe at C** still
tells the reader to create the dash form and cites this section for it:

```
Scratch for a sweep: `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)/`<lane>-r<round>-<n>-work/` (Standing rules; deleted on exit).
```
(`SKILL.md:139`)

```
3. **Copy pristine to scratch.** `mkdir -p "$HYAKU_SCRATCH/<lane>-r<round>-<n>-work/evidence"`
```
(`SKILL.md:161`)

So a seat obeying `SKILL.md:139`/`:161` creates `$HYAKU_SCRATCH/<lane>-r<round>-<n>-work/`, the
form `SKILL.md:28` now declares dead since round 36 — while the page's own practice since round 48
is `$HYAKU_SCRATCH/<lane>-r<round>/<sub>/`. (These two lines are in another section; they are cited
here only as the contradiction witness for this section's clause, not as findings about that
section.)

What would hold: the slash shape is what every landed round **since 48** uses, and the dash form
ends after round 47 — the same two boundaries, shifted eleven rounds from the ones written.

## Holds (verified, not findings)

| Section statement | Verified at C** |
|---|---|
| `SKILL.md:19-20` "Read-only substrates unless PROVINCE.md declares a write surface; detection-and-report for operator-owned remediation" | `PROVINCE.md` exists at C** and is itself read-only in force (`PROVINCE.md:16-17` "Never edits a sibling's gate code (read-only probes…)"). The escape hatch's phrase "write surface" occurs 0 times in `PROVINCE.md` (`grep -niE 'write surface'` → rc 1), so the conditional is never triggered; an unmet antecedent, not a falsified statement |
| `SKILL.md:21` "Secrets shape-only, never content-read" | `corpus/knowledge/mutation-case-kagi-census.md:6-7`: line 6 ends "No external site was contacted; no secret file was" and line 7 reads "content-read (kagi's 0600 `stamps.tsv` appears in directory listings by name only)." No counter-example found |
| `SKILL.md:22-23` "Every claim: measured anchor (path:line, command output, evidence id). Observation / inference / unknown stay separate" | Rule statement; the notes it governs carry the legend (e.g. `mutation-case-kimi-census.md:9-11`). No counter-example found inside the section |
| `SKILL.md:24-27` errata nuance, heading quote, in-place disclosure, "Rejections kept" | V3 above: `SKILL.md:1725` heading byte-identical; `SKILL.md:1733-1735` discloses the table's own in-place repairs; 6 `\| rejected \|` rows in `corpus/SOURCES.md` |
| `SKILL.md:28` "(host scratch directive of 2026-10-25: `/tmp` is for files under 50 MB only; a seat deletes its tree on exit…)" | Dated directive; matches the directive in force for this wave and the shape of the round-53 evidence (`${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r53/deciding`, `.ufo/evidence/round-53/deciding-run.sh:16`). A dated milestone is a hold |
| `SKILL.md:29-31` historical `/tmp` parenthetical + "The substrate tree is never a mutation target" | V2 above: both cited notes place every mutant under `/tmp/tameshi-r{2-1,3-1}-work/` with the substrate marked read-only; evidence dirs at kimi`:171`, kagi`:242` |

## Considered but not reported

- The V2 parenthetical's citation range shows the mutants under `/tmp` but not the *evidence*
  directory; "evidence there" is corroborated one block later in the same document (kimi`:150`,
  `:171`; kagi`:210`, `:242`). The claim is true and the pointers are to the right documents, so the
  range's under-coverage of one word is not raised as a finding.
- The first bullet's escape hatch ("unless PROVINCE.md declares a write surface") is undefined in
  `PROVINCE.md`'s vocabulary (0 hits). Nothing is falsified, only an unused condition; named for the
  L1, not reported.
- The line-28 bullet is a single 317-character line carrying three code spans and a nested
  parenthetical; long for a cold read, but no statement is wrong because of it.
- Rounds 37–47 used `/tmp` while the 2026-10-25 directive was in force; that is a fact about those
  rounds' records, not about this section's rule text, and `/tmp` is permitted for small files, so
  nothing is charged here beyond F1's misdating.

## Limits

One section, one content commit, one pass. Reads were git-object only (`git show`/`git grep`/
`git rev-parse` plus local `sha256sum`/`grep` on a dumped copy in scratch); no recipe step, counter,
gate or sweep was re-executed in this seat, and nothing here re-measures the round-2/3 mutation
runs. The scratch-shape table counts only paths that were actually named in committed files at C**;
a scratch directory that no committed artifact mentions is invisible to this method, so the table
is a lower bound per round, and a round shown with 0 slash references could still have used the
slash shape once without recording it. The claim F1 attacks is an absolute ("every landed round
since 37"), so the observed counter-examples are sufficient to falsify it; no claim is made that
rounds 37–47 *never* used any other shape. Every fenced quote in this file was re-matched against
the C** bytes programmatically: blocks 1, 2, 5 and 6 match the section bytes; blocks 3 and 4 match
the cited note ranges `kimi:4-7` / `kagi:4-6` exactly; blocks 10 and 11 match `SKILL.md:139` and
`:161`; the remaining blocks are derived summaries (table, commands, sample paths), not quotations.

## Seat hygiene

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read04/` (created with `mkdir -p`, removed with
  `rm -rf --` before yield). No inherited TMPDIR was relied on.
- No git or jj mutation anywhere (no commit, checkout, fetch, prune; only read-only `git show`,
  `git grep`, `git rev-parse`, `git ls-tree`); no pacman; no tool install; no network use; no
  subagent dispatch.
- Deliverables: `.ufo/waves/round-53/w2/T53W2Read04.json` and this file.
