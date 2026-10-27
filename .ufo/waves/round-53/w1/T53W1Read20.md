# T53W1Read20 — cold read: `### Six-case confidence statement (round 8, measured)`

Seat: T53W1Read20 (reader, wave 1). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit (C*): `a41195dfc13a73958e4c5228ec196b28d03ded03` — read via git objects only
(`git -C …/tameshi-shokunin show <C*>:<path>`); the working tree was never read for section content.

## 1. Section identity

- Heading: `### Six-case confidence statement (round 8, measured)`, at line **1094** of `SKILL.md`@C*.
- Monitor split reproduced independently: lines 1..2178 split on `\n`; headings = lines matching
  `^#{1,3}(\s|$)` **outside** ``` fences; fence state toggled on any line whose strip starts with ```.
  The heading before it is `### Triggers T1–T3 and the re-pin rule` (line 1071); the next heading
  outside fences is `## The cadence's first scheduled tick, and the service's limits (round 9, measured)`
  (line 1157). Section = lines **1094–1156**, with lines 1156 (empty) and any trailing
  whitespace-only lines stripped → bytes over lines **1094–1155**, joined with `\n`, no trailing newline.
- Verified: line 1155 is the section's last non-blank line
  (`  survivor taxonomy and the composition rule, not the headline percentage.`); line 1156 is `$`-empty.
- `section_sha256 = 71c46c773e7f80782caee328f9f1e8bdb35e6f87ce5f498c703a0e2da849a206`
  (UTF-8, `surrogateescape`; 4477 chars).

## 2. Checks run (scratch `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read20`, deleted at seat end)

Scratch was created with `mkdir -p` before use; `SKILL.md`@C* and the six cited gate blobs were
materialized there from git objects. No git/jj mutating command was run anywhere.

| # | check | command (absolute paths) | outcome |
|---|---|---|---|
| 1 | C* is a commit | `git -C …/tameshi-shokunin cat-file -t a41195df…` | `commit` |
| 2 | section split | python split over `SKILL.md`@C* (rules above) | heading 1094, next 1157, section 1094–1155 |
| 3 | quote uniqueness | `section.count("runs under\n`/tmp/w8-tameshi-t81/sweep/` and `/tmp/w8-t8-2-claims/work/`")` | 1 |
| 4 | ledger rows at ER-2 | `sed -n '276,277p'` of `corpus/knowledge/fleet-kill-rate-ledger.md`@C* | row 5 = kagi `corpus/checklist-run.sh` 34 cases 7/15 (47 %); row 6 = kumitate `scripts/claims-check.mjs` 39 checks 7/10 (70 %) |
| 5 | regression legs | `sed -n '850p;925p' tools/mutate-and-run.sh`@C* | line 850 `# r10-2 leg 5: kagi corpus/checklist-run.sh @ fecee874 (pin 7e5ec98b…)`; line 925 `# r10-2 leg 6: kumitate scripts/claims-check.mjs @ 175de6b (pin e9a21b44…)` |
| 6 | checklist note pointers | `sed -n '178,196p' corpus/knowledge/mutation-case-kagi-checklist.md`@C* | 180–181 class legend (a)/(b); 186 C1 = (a); 189 F2 = (a); 192–194 "six of the eight are unreached inputs … two are values the gate prints but no case asserts" |
| 7 | claims note pointers | `sed -n '140,150p;247,256p;283,293p' corpus/knowledge/mutation-case-kumitate-claims.md`@C* | D7 at 142–148 (`shown.slice(0, 6)` → `5`); Row E "**First JS instance measured** (D9)" at 249–254; E2/D8 "assert-blind threshold … cannot see the floor" at 285–289 |
| 8 | six pins as reachable blobs | sha256 over every blob of each gate path in each owner repo (`git rev-list --all --objects -- <path>`, `git cat-file blob`) | all six found (see §3) |
| 9 | suite grammar at pinned bytes | grep over the materialized pinned blobs | see §3 |
| 10 | checklist suite size | `grep -cE '(^|[^[:alnum:]_])run[[:space:]]+"'` over pinned `checklist-run.sh` | 34 `run` invocations = the 34 cases the control line reports |
| 11 | round-8 harness pin | sha256 scan of `tools/mutate-and-run.sh` blobs in tameshi history | `cf41efaa8be5f52d…` present, 1,341 lines (matches ledger ER-2); legs 3 and 4 carried `# r7-1 leg` markers |
| 12 | `/tmp` receipts | `ls -ld /tmp/w8-tameshi-t81 /tmp/w8-t8-2-claims`; `ls -ld /fast/scratch/hyaku` | both `/tmp` dirs: **No such file or directory**; `/fast/scratch/hyaku` exists |
| 13 | note scratch subpaths | grep `/tmp/w8` in both notes@C* | kagi note `:285` `--workdir /tmp/w8-tameshi-t81/sweep`; claims note `:373` `--workdir /tmp/w8-t8-2-claims/work` (the section's subpaths are faithful) |
| 14 | round-5 pointer | grep over `SKILL.md`@C* | `## Third case — cross-author confirmation (round 5, measured)` exists at line 668 |

## 3. Holds (verified against C* bytes)

Table cells, one by one, against the pinned blobs (sha256 prefix = the row's `revision` cell):

| # | case row | pin | pinned blob evidence |
|---|---|---|---|
| 1 | kumitate `scripts/kimi-census.mjs`, 43, `8/10`, 10 kill-aimed | `83016d45…` | blob `a2bf15c0…`, 43,273 B, 896 newlines, `#!/usr/bin/env node` |
| 2 | kagi `corpus/surface-census.sh`, 16, `8/10`, 10 kill-aimed | `275d8294…` | blob `dcf878b9…`, 44,212 B, 886 newlines, `#!/usr/bin/env bash` |
| 3 | tsukuroi `tools/tsukuroi-census.sh`, 26, `6/10`, 6 kill + 4 hole | `084951be…` | blob `dfcf6f59…`, 44,947 B, 976 newlines, bash |
| 4 | mado `tools/mado-verify.sh`, 28, `4/10`, 4 in + 6 out | `d7edaab4…` | blob `7ccc601f…`, 45,334 B, 1,098 newlines, bash |
| 5 | kagi `corpus/checklist-run.sh`, 34, `7/15`, 7 kill + 8 hole | `7e5ec98b…` | blob `78f2c45e…`, 24,697 B, 506 lines, bash (also still the live file: `sha256sum` = `7e5ec98b9e1d0afa…`) |
| 6 | kumitate `scripts/claims-check.mjs`, 39, `7/10`, 6 kill + 4 hole | `e9a21b44…` | blob `fae4bbcd…`, 48,265 B, 925 newlines (926 lines), `#!/usr/bin/env node` |

- **Rates / composition arithmetic** — 8/10, 8/10, 6/10, 4/10, 7/15 (=46.67 → 47 %), 7/10; compositions
  10; 10; 6+4; 4+6; 7+8; 6+4 all sum to the denominator. Band `40 / 47 / 60 / 70 / 80 / 80` is ascending
  and equals the six rows. Matches `fleet-kill-rate-ledger.md` §1 (rows 1–4) and ER-2 (rows 5–6) verbatim.
- **Shebang claim** — "read from the pinned bytes: `#!/usr/bin/env node` ×2, `#!/usr/bin/env bash` ×4":
  true at the blobs listed above (read from the blobs, not the working trees). Two language classes,
  and the author split (kumitate ×2, kagi ×2, tsukuroi, mado) is the roster's own.
- **Grammar families (five over six gates)** — at pinned bytes:
  kimi `KIMI_CENSUS_SELFTEST: n/m pass` + `FAIL ${r.label}` (line 850/852);
  claims `CLAIMS_SELFTEST: n/m pass` + the **same** `FAIL ${r.label}` shape (line 859/861) → the two node
  gates do share the family; surface-census `ok-case`/`bad-case … got exit=` + `SELFTEST surfaces+shapes`
  (755/758/766); checklist-run `checklist-selftest:` + `CHECKLIST_SELFTEST:` (418/421, 494/497);
  tsukuroi `printf 'PASS %s'` invoked as `(exit $rc, $wverdict)` (693/782); mado
  `MADO_SELFTEST: $n_pass/$n_pass assertions passed` (423) = "n/n assertions". 1+2+1+1 = 5.
- **Controls cited for cases 5–6** — `CHECKLIST_SELFTEST: PASS (34 cases)` at
  `mutation-case-kagi-checklist.md:49` and `:261`; `CLAIMS_SELFTEST: 39/39 pass` at
  `mutation-case-kumitate-claims.md:53/62`; `MUTATE_RESTORE: OK` at `:199` and `:69`; tool
  `cf41efaa8be5f52d…` at `kagi.md:32`/`kumi.md:23` and present as a reachable harness blob (1,341 lines).
- **Round-52 bracket** — ledger rows at ER-2 `:276-277` = exactly rows 5 and 6; `--regression` legs at
  `tools/mutate-and-run.sh:850,925` = exactly the r10-2 leg-5/leg-6 headers. Both pointers exact at C*.
- **`mutation-case-kagi-checklist.md:180-194`** — C1 and F2 both class (a), six (A1, B1, B3, D1, E2, G1)
  class (b), and the "two are values the gate prints but no case asserts" reading is at 193–194.
- **`mutation-case-kumitate-claims.md:142-148,285-291`** — D7 = `shown.slice(0, 6)` → `5` (the kimi D2
  seam); 285–289 = E2 "assert-blind threshold (D8) … cannot see the floor". Pointer pair supports both halves.
- **`mutation-case-kumitate-claims.md:249-254`** — Row E, "**First JS instance measured** (D9)", and the
  amendment of the tsukuroi reading: exactly the range 249–254.
- **"Third case…" pointer** — `## Third case — cross-author confirmation (round 5, measured)` at line 668.
  Its row E (`zero JS instances`) and §4 ("Width is not a language property") are what the section claims
  the round-5 statement said about language.
- **"Unknown in all six"** — coordinated rewrites unknown at round 5 (row F, "unknown in all three"),
  cross-host stability disclaimed in ledger §4, "the 50 % crossover is still unmeasured" in round-5 item 1.
- **"Counting tameshi's own harness meta-sweep (ledger §2)"** — ledger §2 row 2 (`:95`) is the harness
  meta-sweep (0/6 → 6/6), owned by tameshi: seventh artifact, fifth author. Holds.
- **`cf41efaa…` has four legs at round 8** — the r7-1 harness blob (1,341 L) carries legs 3 and 4 under
  `# r7-1 leg` markers over the older r6 legs; matches ledger ER-2's "four materialized legs".

## 4. Finding (1)

**Class: scratch-directive violation (dead receipt).**

Verbatim quote from the section (byte-exact, newline included):

```
runs under
`/tmp/w8-tameshi-t81/sweep/` and `/tmp/w8-t8-2-claims/work/`
```

The statement that fails: the section names the run's evidence location as two `/tmp` directories.
The host scratch directive (`$HYAKU_SCRATCH`, default `/fast/scratch/hyaku`; `/tmp` only for files
under 50 MB — i.e. never as the durable home of a sweep's evidence) makes that an unsanctioned
receipt location, and at C* both paths are gone:

```
$ ls -ld /tmp/w8-tameshi-t81 /tmp/w8-t8-2-claims
ls: cannot access '/tmp/w8-tameshi-t81': No such file or directory
ls: cannot access '/tmp/w8-t8-2-claims': No such file or directory
$ ls -ld /fast/scratch/hyaku
drwxr-xr-x 18 vgpnk vgpnk 4096 Oct 27 10:30 /fast/scratch/hyaku
```

Why it fails rather than holds: the paths are presented as where the runs *are* (the only receipt the
section gives for cases 5–6 beyond the notes), and the cited evidence is unrecoverable — the claims note
itself states it at C*: "Scratch `/tmp/w8-t8-2-claims/` (all evidence lives here; the fleet holds only
this note)" (`mutation-case-kumitate-claims.md:349`). The subpaths themselves are faithful to the notes
(`:285`, `:373`), so this is not a typo: the defect is the choice of `/tmp` as the evidence store.
The rest of the sentence's content (controls, `MUTATE_RESTORE`, tool pin) does hold — see §3.

## 5. Candidates examined and dismissed (not findings)

- **`tool cf41efaa…`** — not dead: the blob is present in tameshi's harness history (1,341 lines), so the
  instrument pin is checkable.
- **"the four embedded legs plus the two queue gates"** — pinned to "at this write" (round 8); the
  round-8 harness (`cf41efaa…`) carries four legs, and legs 5/6 arrive later at r10-2. The C* harness
  (10 legs) does not falsify a "at this write" statement.
- **"five measured families"** — the notes' own axes table distinguishes the two node gates in wording
  ("FAIL labels" vs "FAIL-only printing"), but at the pinned bytes both print the identical
  `FAIL ${r.label}` line and the identical `*_SELFTEST: n/m pass` summary, so the collapse to one family
  (and the count of five) is supported by the code, not contradicted by it.
- **"both notes landed while this section was being written"** vs the round-52 bracket "both landed after
  this write" — the first-and-final-content distinction: `git log --diff-filter=A` shows both notes and
  this section text first appear in the same commit (`c611d5d`, 2026-10-14 16:55:09 -0300), and the notes'
  own headers record in-flight state at that write. The bracket refines, it does not contradict.
- **Quoted round-5 phrase ("two bash instances, still zero JS")** — a condensation of the round-5 row E
  cell ("2 bash instances + inventory, zero JS instances") and §4 item 3 ("both instances are bash and no
  JS instance exists"). Substance is verbatim-faithful; quoted form is not a byte quote, and I do not
  count paraphrase-of-content as a failing statement.
- **`fleet-kill-rate-ledger.md:276-277` / `mutate-and-run.sh:850,925`** — both exact at C* (check 4, 5);
  no drift from this round's C2 tool edits in this section.

## 6. Limits

- The six suite sizes and rates are note-sourced receipts; I re-derived only what bytes allow (pinned blob
  sizes/shebangs, the 34 `run` invocations in `checklist-run.sh`). I did not re-execute any gate's
  `--selftest`, so `43/16/26/28/34/39` and the control lines stand as recorded controls, not as my runs.
- `claims-check.mjs` check count (39) is dynamic (`results.length`), not statically countable; likewise
  kimi's 43. No contradiction was observed between the notes and the section on either.
- Live-file drift in the owner repos (e.g. `surface-census.sh` live `1e697b01…` vs pin `275d8294…`) is a
  post-round-8 owner change and is not a claim of this section, which records measurements, not liveness.
- Findings list is what the bytes show; nothing else in the section failed a check I could run.
