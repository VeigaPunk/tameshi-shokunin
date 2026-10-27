# T53W2Read15 — re-read at C**: `### Six-case confidence statement (round 8, measured)`

Seat T53W2Read15 (re-reader, wave 2). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Candidate `C**` = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`; section bytes read via git objects
only (`git -C …/tameshi-shokunin show C**:SKILL.md`, `git -C … show C**:<path>`). The working tree was
never read for section content. Scratch `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read15` (created with
`mkdir -p`, deleted at seat end); no git/jj mutation anywhere; no subagent dispatched.

## 1. Section identity and split verification

Splitter = the frozen monitor's `sectionize()` (`.ufo/evidence/round-18/measure.py:212-252`, used by
`.ufo/evidence/round-21/coldread/measure.py`): lines = blob text `.split('\n')` with one trailing `''`
popped; a heading is a line matching `^#{1,3}(\s|$)` outside ``` fences (fence state toggles on any line
whose `strip()` starts with ```); section = heading line through the line before the next heading,
trailing whitespace-only lines stripped, joined with `\n`, no trailing newline; sha256 over
`body.encode('utf-8','surrogateescape')`.

- Heading at **line 1098** of `SKILL.md`@C** (2,189 lines, 197,139 B, file sha256 `4b4a05251208beb6…`).
- Previous heading: `### Triggers T1–T3 and the re-pin rule` at 1075. Next heading outside fences:
  `## The cadence's first scheduled tick, and the service's limits (round 9, measured)` at 1162.
- Section span lines **1098–1161**; line 1161 is `$`-empty (`cat -A`), so the body is **lines
  1098–1160**, 63 lines. No ```-fenced line inside the span, so no fence-state risk.
- `section_sha256 = a0907bd725da1ffb92db43f530c9cee1d73f17b4d76ab6fb27a2962e15b308d0`
  (4,716 chars).
- **Splitter validated before hashing**: the same code run over `SKILL.md`@C* (`a41195df…`) returns
  heading 1094 / next 1157 / sha256 `71c46c773e7f80782caee328f9f1e8bdb35e6f87ce5f498c703a0e2da849a206`,
  byte-for-byte the value the wave-1 reader recorded for this heading at C* — an independent
  reproduction of the wave-1 split. The same run yields **64 sections** over the C** page (the C1 claim's
  64-section page).

## 2. Checks run (fix verification first)

| # | check | command (absolute paths; `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`) | outcome |
|---|---|---|---|
| 1 | **fix present — history marker** | `section.count("named here as history only")` | 1 — marker present |
| 2 | **fix present — evidence of record named** | `section.count("the evidence of record is the case notes")` | 1 — both note paths follow it |
| 3 | **fix delta is exactly this** | `diff -u` of the section body C* vs C** | one hunk, 1 line removed / 2 added, the `/tmp` sentence only; no other byte of the section moved |
| 4 | cited paths still dead | `ls -ld /tmp/w8-tameshi-t81 /tmp/w8-t8-2-claims` | both `No such file or directory`; `/fast/scratch/hyaku` exists |
| 5 | evidence-of-record files exist at C** | `git -C $L rev-parse C**:corpus/knowledge/mutation-case-kagi-checklist.md` / `…kumitate-claims.md` | blobs `a267cbe0…` / `3b5c3109…`, identical to their C* blobs (untouched by the fix pass) |
| 6 | evidence of record carries the controls | `grep -n` over both notes at C** | `CHECKLIST_SELFTEST: PASS (34 cases)` at kagi `:49`, `:261`; `CLAIMS_SELFTEST: 39/39 pass` at kumi `:53`, `:62`; `MUTATE_RESTORE: OK` at kagi `:199`, `:262`, kumi `:69` |
| 7 | host /tmp ageing mechanism | `grep -v '^#' /usr/lib/tmpfiles.d/tmp.conf` | `q /tmp 1777 root root 10d` |
| 8 | rule text / date the fix invokes | `sed -n '29,32p' SKILL.md`@C** | “host scratch directive of 2026-10-25: `/tmp` is for files under 50 MB only; a seat deletes its tree on exit […]”; no reaping clause |
| 9 | any record of the w8 scratch being reaped | `grep -rIn 'w8-tameshi-t81\|w8-t8-2-claims'` over the lane | only live-at-write mentions (notes, `plans/round-8-record-draft.md`, `reports/r8-aud-t8.md`); no reaping record |
| 10 | six table pins resolve to single blobs | sha256 over every `git rev-list --all --objects -- <path>` blob per owner repo | all six found exactly once (below) |
| 11 | shebangs at the pinned bytes | `head -1` of each materialized pin | node ×2, bash ×4 |
| 12 | grammar families at the pinned bytes | `grep -n` on each pin | five families as stated (below) |
| 13 | checklist suite size | `grep -cE '(^\|[^[:alnum:]_])run[[:space:]]+"'` on the pinned `checklist-run.sh` | 34 `run` invocations = the 34 cases |
| 14 | pointers inside the section | `grep -n` on `fleet-kill-rate-ledger.md`@C**, `tools/mutate-and-run.sh`@C**, both notes@C** | all resolve (below) |
| 15 | round-8 harness and its legs | sha256 scan of all 13 `tools/mutate-and-run.sh` blobs in tameshi history | `cf41efaa8be5f52d…c75` = blob `935adec3…`, 61,632 B / 1,341 newlines; four embedded spec heredocs |
| 16 | round-5 section pointer and its classes | `grep -n` over `SKILL.md`@C** | heading at 671, row E at 730, §4 item 4 at 752 |

Pin resolution (check 10), all in `/home/vgpnk/Projects/shokunin/<lane>-shokunin`:

| row | pin | blob found | bytes |
|---|---|---|---|
| 1 kumitate `scripts/kimi-census.mjs` | `83016d45` | `a2bf15c0…` | 43,273 |
| 2 kagi `corpus/surface-census.sh` | `275d8294` | `dcf878b9…` | 44,212 |
| 3 tsukuroi `tools/tsukuroi-census.sh` | `084951be` | `dfcf6f59…` | 44,947 |
| 4 mado `tools/mado-verify.sh` | `d7edaab4` | `7ccc601f…` | 45,334 |
| 5 kagi `corpus/checklist-run.sh` | `7e5ec98b` | `78f2c45e…` | 24,697 |
| 6 kumitate `scripts/claims-check.mjs` | `e9a21b44` | `fae4bbcd…` | 48,265 |

## 3. Holds

Every statement of the section except the one in §4 was checked and holds at C**:

- **The two wave-1 fixes are in the bytes.** The `/tmp` sentence now carries
  `named here as history only` and names the notes as `the evidence of record is the case notes`; the
  evidence the section cites survives on the fleet at C** (check 5) and carries the exact controls it
  quotes (check 6, e.g. `CHECKLIST_SELFTEST: PASS (34 cases)`, `CLAIMS_SELFTEST: 39/39 pass`,
  `MUTATE_RESTORE: OK`). The wave-1 finding's operative defect — an ephemeral path presented as a live
  receipt — is therefore cured; only the causal gloss in the same clause does not hold (§4).
- **Table rows.** Rates, compositions and revision tags match `fleet-kill-rate-ledger.md`@C** §1 rows 1–4
  (`:45-48`) and ER-2 rows 5–6 (`:276-277`) cell for cell: 43 · 8/10 = 80 % · 10 kill-aimed; 16 · 8/10 ·
  10; 26 · 6/10 · 6 kill + 4 hole; 28 · 4/10 · 4 in + 6 out; 34 · 7/15 = 47 % · 7 kill + 8 hole;
  39 · 7/10 · 6 kill + 4 hole. Compositions sum to their denominators (10/10/6+4/4+6/7+8/6+4) and the band
  `40 / 47 / 60 / 70 / 80 / 80` is ascending and equals the six rows.
- **Pins.** All six `revision` cells resolve to exactly one blob in their owner repo with the stated
  sha256 prefix (check 10); row 5's pin is a 506-line / 24,697 B bash file and row 6's a 925-newline /
  48,265 B node file, as ER-2 records.
- **`two language classes` / shebangs.** Read from the pinned bytes: `#!/usr/bin/env node` ×2
  (kimi-census, claims-check), `#!/usr/bin/env bash` ×4 (surface-census, tsukuroi-census, mado-verify,
  checklist-run) — node ESM ×2 + bash ×4, as claimed.
- **`five measured families over the six gates`.** At the pinned bytes: kimi prints `KIMI_CENSUS_SELFTEST:`
  with a `${passed}/${results.length}` numerator and ` pass` (`:852`) plus `FAIL ${r.label}` (`:850`);
  claims
  `CLAIMS_SELFTEST: …pass` (`:861`) with the identical `FAIL ${r.label}` (`:859`) → one family over the
  two kumitate node gates. kagi's two bash gates differ: surface-census `ok-case`/`bad-case … got exit=`
  (`:755`, `:758`) and `SELFTEST: PASS/FAIL (n cases)` (`:846-847`) versus checklist-run
  `checklist-selftest: …` (`:418`, `:421`) and `CHECKLIST_SELFTEST: PASS/FAIL (n cases)` (`:494`, `:497`).
  tsukuroi prints `PASS %s` from `ok()` (`:693`) invoked as `ok "$label (exit $rc, $wverdict)"` (`:782`);
  mado prints `MADO_SELFTEST: $n_pass/$n_pass assertions passed` (`:423`). 1+2+1+1 = 5, each in the shape
  the section names.
- **Four author lanes — kumitate ×2, kagi ×2, tsukuroi, mado** (the section wraps this sentence after
  “four author lanes”, so it is not one continuous string). The six rows' `(author · file)` cells match
  ledger §1/ER-2 owners.
- **“The case set at this write: the four embedded legs plus the two queue gates entering in round 8”**
  (sentence wrapped in the source; verified by content). The round-8 harness
  `cf41efaa…` (1,341 lines) writes exactly four embedded case specs — `js-kimi-census.spec` (`:552`),
  `bash-surface-census.spec` (`:593`), `bash-tsukuroi-census.spec` (`:638`), `bash-mado-verify.spec`
  (`:683`); the two queue rows are ledger §3 `claims-check` (`:111`) and `checklist-run` (`:121`), as
  ER-2 states.
- **The round-52 bracket.** `fleet-kill-rate-ledger.md:276-277` is exactly rows 5 and 6, and
  `tools/mutate-and-run.sh:850` / `:925` are exactly the `# r10-2 leg 5` / `# r10-2 leg 6` headers.
- **The follow-up / authority sentence.** The notes do name both follow-ups: claims note E3
  (`:292-296`) records the `--regression` embedding as a follow-up, E4 (`:297-305`) records the ledger
  append (“The ledger's §1 still carries four rows; its own cadence (round 7/8) appends the fifth and
  sixth”).
- **`the checklist note classifies C1 … and F2 … as family (a) and six more as unreached inputs`.**
  `mutation-case-kagi-checklist.md:183-190` gives C1 (a), F2 (a) and six (b) rows; `:192-193`
  “six of the eight are unreached inputs … two are values the gate prints but no case asserts”. All
  inside the cited `:180-194`.
- **`D7` / `D8` / `D9` pointers.** `mutation-case-kumitate-claims.md:142` is D7 (“cap unreached:
  `shown.slice(0, 6)` → `5`”, “the kimi-D2 shape … reproduced on a sibling gate”), `:150` starts D8
  (= E2 at `:285`, “the assert-blind threshold”, inside `:285-291`), `:249-250` is Row E with
  “**First JS instance measured** (D9)”, inside the cited `:249-254`.
- **`the round-5 three-case statement (this page's "Third case…" section)`.** That section is
  `## Third case — cross-author confirmation (round 5, measured)` at 671; its row E at 730 carries
  “2 bash instances + inventory, zero JS instances” and its item 4 at 752 is “**Width is not a language
  property.** […] Read width off placement, never off language” — i.e. the round-3/5 finding does place
  the differences in kill width and composition, not language. The three-gate frame is the section's own
  (“Three-case confidence statement”, `:758`).
- **Counting tameshi’s own harness meta-sweep (ledger §2)** — the section wraps this phrase across two
  source lines. §2 is `:90-97`; the meta-sweep row is
  `:95` (pre-hardening 0/6, post 6/6, owner “the instrument's own gate, hardened by its owner (tameshi)”), so
  artifact 7 / author 5, as the section says.
- **Unknown in all six** (the source wraps this bullet; the items are) — coordinated rewrites; cross-host
  stability; the 50 % crossover; the two round-8 notes' own unknowns. Ledger §8 U2 (coordinated multi-edit
  rewrites unmeasured) and U1 (no
  cross-host/toolchain stability reading); the 50 % crossover is still unmeasured in the round-5 section
  (`:741`, `:774`); both notes carry their own U lists (kagi U1–U4+, kumi U1–U4+).

## 4. Finding (1)

**Class: unsupported premise (causal attribution).**

Verbatim from the section at C**:

```
scratch paths long since reaped under the host scratch rule, named here as history only
```

The clause reads, with the two paths immediately preceding it elided here: “…
`scratch paths long since reaped under the host scratch rule, named here as history only`; the evidence
of record is the case notes …”.

What holds: the paths are absent
(`ls -ld /tmp/w8-tameshi-t81 /tmp/w8-t8-2-claims` → `No such file or directory` for both), and the
history marking plus the evidence-of-record naming are exactly the wave-1 repair.

What does not hold: the attribution. The page's own host scratch rule is the directive of **2026-10-25**
(`SKILL.md`@C**:29), eleven days after the runs it is applied to (both notes are dated 2026-10-14 —
`mutation-case-kagi-checklist.md:3`, `mutation-case-kumitate-claims.md:3`), and its text contains **no
/tmp reaping mandate**: it fixes the scratch root, says “`/tmp` is for files under 50 MB only”, and binds
each seat to delete *its own* tree (`SKILL.md`@C**:29-32). The mechanism that actually ages `/tmp` on
this host is `systemd-tmpfiles`:

```
$ grep -v '^#' /usr/lib/tmpfiles.d/tmp.conf
q /tmp 1777 root root 10d
```

On that policy the 2026-10-14 trees were due for removal around 2026-10-24 — before the directive
existed — so the reaping was not “under the host scratch rule”. The other horn is no better: if a seat
removed the trees after 2026-10-25, the removal is one or two days old, not “long since”. And nothing
records the removal at all: `grep -rIn 'w8-tameshi-t81\|w8-t8-2-claims'` over the lane returns only
live-at-write mentions (both notes, `plans/round-8-record-draft.md:87-90,166,302,388`,
`reports/r8-aud-t8.md:31,164`) — no reaping receipt, no cleanup log.

Fair scope: this is the only residue of the fix. The sentence's operative job — “do not read these as
live receipts” — is set by `named here as history only`, which holds; the causal gloss should read as
plain absence (“gone”), the form the page already uses for a volatile path elsewhere
(`SKILL.md`@C**:991, “[round 52: that volatile path is gone; …]”).

## 5. Candidates examined and dismissed (not findings)

- **“the evidence of record is the case notes …” (is the notes’ own text against it?)** — no. The notes
  are the fleet’s surviving records for these sweeps: ER-2 states “each note is its run's only fleet
  file”, and the claims note says the scratch holds the raw evidence while “the fleet holds only this
  note” (`:349`). Naming the notes the evidence of record is the accurate fleet-level statement, and both
  notes carry the recorded tables, controls, spec and restore receipts (checks 5–6).
- **“both notes landed while this section was being written” vs the round-52 bracket “both landed after
  this write”** — not a contradiction. Both notes and this section text first appear in the same commit
  (`git log --diff-filter=A` → `c611d5d`, 2026-10-14 16:55:09 -0300; `git log -S` for the heading returns
  the same commit), so the notes landed inside the section’s write window and the bracketed note records
  their landing relative to the authored text. The round-52 line is explicitly a later reading.
- **Quoted round-5 phrase (“two bash instances, still zero JS”)** — a condensation of row E’s cell (“2
  bash instances + inventory, zero JS instances”, `SKILL.md`@C**:730) and of the claims note’s own
  quotation (`:250`). Substance faithful; not counted as a failing statement.
- **“The ledger rows and any `--regression` leg for either are follow-ups the notes themselves name
  (claims note E3)”** — the claim holds; E3 (`:292-296`) names the harness embedding and E4 (`:297-305`)
  names the ledger append. The parenthetical label cites the note by its leg half only; the statement is
  true, so this is a citation-scope nit, not a finding.
- **`Six cases` / `four author lanes` / `five measured families` as stale counts** — dated: the heading is
  `(round 8, measured)` and the body is framed “at this write”. The page records the later case count
  elsewhere (ten since round 51, `:1400`), which does not falsify a round-8 statement.
- **Suite sizes 43 / 39** — dynamic (`results.length`) in the pinned node gates; recorded receipts in the
  notes/ledger, not contradictable from bytes. Only 34 (checklist) is statically countable, and it matches
  (check 13).
- **“runs under `/tmp/w8-tameshi-t81/sweep/` and `/tmp/w8-t8-2-claims/work/`” as subpath drift** — both
  subpaths are faithful to the notes (kagi note `:285` gives `--workdir /tmp/w8-tameshi-t81/sweep`; claims
  note `:373` gives `--workdir /tmp/w8-t8-2-claims/work`).

## 6. Limits

- I executed no gate `--selftest` and re-ran no sweep: the six rates and the sizes 43/16/26/28/39 stand as
  the notes’ and ledger’s recorded receipts. What I re-derived from pinned bytes is the pins themselves,
  the shebangs, the five grammar shapes, the 34 `run` invocations, the harness’s 1,341 lines and four
  embedded legs.
- The date the w8 `/tmp` trees were removed is not directly observable (the trees are gone). The finding’s
  reason is therefore the rule’s text and date plus the host’s tmpfiles policy plus the absence of any
  reaping record — not a timestamp of deletion.
- The section’s own “opens”/`[I]` markers do not appear in this section; nothing in it required inferring
  authorship.
