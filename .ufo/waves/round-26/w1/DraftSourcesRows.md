# DraftSourcesRows — C1 frontier step, SOURCES rows S088 / S089

Seat: `TameshiR26.DraftSourcesRows` (leaf, no subagent dispatch).
Date: 2026-10-22. Lane: `tameshi-shokunin`.
Scope: open the two named sources, draft the two registry rows in the exact
11-column shape of `corpus/SOURCES.md`, record a located quote for each, and run
the census read-only.

**Verdict: both rows exist in the landed registry and both are census-clean, but the
landed S089 is not the row my brief named.** The brief asked for S089 =
`.../supported-mutators/`; the lane landed S089 = `.../equivalent-mutants/`, because
the brief's URL is already row **S052** in the same registry. The brief's URL is
admissible only as a *correction* row (`supersedes S052`) or as a *different-scope*
row that earns a W04 warning; as a plain same-scope row it is census error E04 and
fails validation. The landed choice is the one that satisfies the census and the
contract's append-only rule. Details, exact commands and observed output below.

I wrote nothing except this report file. No production file, registry row, lesson or
knowledge entry was edited; no git write command and no `jj` command was run in any
repo; no gate, selftest or sweep was executed inside the lane (the one selftest run
below happened in a `/tmp` scratch dir against a `/tmp` byte copy).

---

## 1. What the two sources are, and what I opened

### 1.1 S088 subject — kumitate `scripts/cite-check.mjs` (read-only, pinned)

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > /tmp/cite-check-pinned.mjs
$ sha256sum /tmp/cite-check-pinned.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/cite-check-pinned.mjs
$ wc -l -c /tmp/cite-check-pinned.mjs
 2537 126735 /tmp/cite-check-pinned.mjs
$ git -C …/kumitate-shokunin ls-tree 1205c66… scripts/cite-check.mjs
100755 blob 9770de8c5a834b2f2adb817f8b0a7ba9e166b87f	scripts/cite-check.mjs
$ git -C …/kumitate-shokunin ls-tree origin/master scripts/cite-check.mjs
100755 blob 9770de8c5a834b2f2adb817f8b0a7ba9e166b87f	scripts/cite-check.mjs
$ git -C …/kumitate-shokunin show origin/master:scripts/cite-check.mjs | sha256sum
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  -
```

The sha256 equals the frozen contract's `claims.C1.leg.blob_sha256` exactly. The
master tip carries the *same git blob id*, so "unchanged at kumitate master" is
grounded in the object graph, not inferred.

Anchor lines I located in those pinned bytes and re-read:

| anchor | content (observed) |
|---|---|
| `:69-71` | exit map: `exit 0 CLEAN · 1 DRIFT (error, or warn under --strict) · 2 fail-closed` / `(missing/non-dir --src or --self, empty scan set, zero resolutions)` / `64 usage error.` |
| `:73-76` | suite groups: `hermetic  fixture-only checks over a synthetic tree in the system temp dir.` … `This is the whole of --selftest.` |
| `:81-82` | `--selftest runs hermetic only · --integrations alone runs the integration group ·` |
| `:217-225` | `const SEVERITY = { … UNRESOLVED: 'error', LINE_OOR: 'error', … }` |
| `:1589-1590` | `const drift = totals.error > 0 \|\| (opts.strict && totals.warn > 0);` / `const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';` |

Counts the row's `teaches` cell asserts, each with the command that produced it:

```
$ grep -c "checkI(" /tmp/cite-check-pinned.mjs
9
$ env -i PATH="$PATH" HOME=$h/home TMPDIR=$h/tmp LC_ALL=C GIT_CONFIG_NOSYSTEM=1 \
    GIT_CEILING_DIRECTORIES=$h node /tmp/cite-check-pinned.mjs --selftest     # in /tmp/r26selftest
…
62/62 cases passed (hermetic)
VERDICT: PASS
exit=0
```

The 62 and the 9 are therefore observed, not inherited from a sibling's prose: 62 is
the runtime count the pinned gate prints, 9 is the number of `checkI(` integration
call sites in the pinned bytes.

**Located quote for S088** (17 words), pinned `:75-76`:
> "Never reads --src or --self; MUST PASS in any repo state. This is the whole of --selftest."

### 1.2 S089 subject — a Stryker Mutator docs page

**The brief's URL** (opened this session, ordinary fetch, no challenge, no headless
browser):
`https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/`

```
$ curl -sS -I -A "Mozilla/5.0" …/supported-mutators/ | grep -i last-modified
last-modified: Wed, 21 Oct 2026 16:23:16 GMT
$ curl -sS -A "Mozilla/5.0" …/supported-mutators/ -o /tmp/supported-mutators.html
$ sha256sum /tmp/supported-mutators.html
fbbac72439fc5d5194bc76bca6b1826a25b86ed6fe1b1cedb843c7046c0fe98b  /tmp/supported-mutators.html
```

**Located quote for the brief's URL** (24 words), the lead paragraph under the
`## Support` heading:
> "All Stryker versions support a variety of different mutators. We've aligned on a standard naming scheme so it is easy to switch and compare implementations."

**The URL the lane actually landed as S089** (also opened this session):
`https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/`

```
$ curl -sS -A "Mozilla/5.0" …/equivalent-mutants/ -o /tmp/equivalent-mutants.html
$ sha256sum /tmp/equivalent-mutants.html
bc57267629e20668a6542c5c225d1da9e6fef8de466cbab1337df3ff7c42e04d  /tmp/equivalent-mutants.html
```

That html sha256 equals the sha256 the landed S089 anchor records
(`bc572676…e04d`) — the landed row's anchor is reproducible. Both served pages are
byte-stable across repeated fetches, so the anchor hashes are reproducible and not
one-off responses:

```
$ for i in 1 2 3; do curl -sS -A "Mozilla/5.0" …/supported-mutators/ -o /tmp/sm-$i.html; sha256sum /tmp/sm-$i.html; done
fbbac72439fc5d5194bc76bca6b1826a25b86ed6fe1b1cedb843c7046c0fe98b  /tmp/sm-1.html
fbbac72439fc5d5194bc76bca6b1826a25b86ed6fe1b1cedb843c7046c0fe98b  /tmp/sm-2.html
fbbac72439fc5d5194bc76bca6b1826a25b86ed6fe1b1cedb843c7046c0fe98b  /tmp/sm-3.html
$ for i in 1 2; do curl -sS -A "Mozilla/5.0" …/equivalent-mutants/ -o /tmp/em-$i.html; sha256sum /tmp/em-$i.html; done
bc57267629e20668a6542c5c225d1da9e6fef8de466cbab1337df3ff7c42e04d  /tmp/em-1.html
bc57267629e20668a6542c5c225d1da9e6fef8de466cbab1337df3ff7c42e04d  /tmp/em-2.html
```

**Located quote for the landed S089 URL** (25 words), the paragraph immediately after
the `10 ** 0` example:
> "There is no definitive way for Stryker to find and ignore them. There is currently also no way yet to mark them to be ignored."

Located by byte offset in the fetched html, so the position is not a guess:

```
$ python3 - <<'PY'   # over /tmp/equivalent-mutants.html
i = s.find('10 ** 0 = 1'); j = s.find('no definitive way for Stryker')
# i = 30613, j = 30826
text between: "10 ** 0 = 1, so even if we change >= to <= and even < or > we will get
the same output each time! It is called equivalent mutant . There is"
PY
```

### 1.3 The duplication that decided the row

`corpus/SOURCES.md:61` already holds the brief's URL:

```
| S052 | Supported mutators (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ | docs | A | StrykerJS's named single-edit operator classes for JS mutant selection | §Supported mutators opening paragraph and §Support table @ page fetched 2026-10-20 (Docusaurus build, last-modified 2026-10-19; no commit pin exposed) | names the JS single-edit operator families a mutant set is drawn from (equality, conditional, string literal, boolean, array declaration) and which StrykerJS does not support (assignment expression) | mined | 2026-10-20 | 180d | corpus/knowledge/mutation-case-kumitate-round-gate.md, corpus/knowledge/mutation-case-kumitate-sources-check.md |
```

Neither URL appears in any other lane's registry (`grep -l supported-mutators */corpus/SOURCES.md`
→ `tameshi-shokunin/corpus/SOURCES.md` only; same for `equivalent-mutants`), so the
cross-lane `shared` census mode reports neither.

---

## 2. The two rows, in the exact column shape of the table

Column shape (`corpus/SOURCES.md:10`): `id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by` — 11 columns, NF = 13 when split on
`|`, no `|` inside any cell.

### 2.1 S088 — as landed, `corpus/SOURCES.md:97` (verbatim)

```
| S088 | kumitate `scripts/cite-check.mjs` (fleet gate, read-only) — kumitate-shokunin/scripts/cite-check.mjs | code | A | the gate's own exit map and hermetic selftest group at the measured revision | :69-71 (exit map), :73-76 (suite groups), :217-225 (SEVERITY), :1589-1590 (drift and verdict) @ 1205c66 (blob sha256 40573448…c10c9f, 2537 lines, mode 100755; unchanged at kumitate master) | its 62-case hermetic `--selftest` is the suite the ninth mutation case measures; the 9 integration-group checks do not run under `--selftest` | mined | 2026-10-22 | 180d | corpus/knowledge/mutation-case-kumitate-cite-check.md |
```

Every anchor in that cell was re-read against the pinned bytes in §1.1 and matches.
Located quote: pinned `:75-76` (17 words), quoted in §1.1.

### 2.2 S089 — as landed, `corpus/SOURCES.md:98` (verbatim)

```
| S089 | Equivalent mutants (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | docs | A | Stryker's own statement that equivalent mutants cannot be found or marked automatically | page body after the `10 ** 0` example @ page fetched 2026-10-22 (version unstated; html sha256 bc572676…e04d) | an equivalent mutant stays a survivor in the score; calling a survivor a test-suite hole needs an off-suite witness or an explicit equivalence argument | mined | 2026-10-22 | 180d | corpus/knowledge/mutation-case-kumitate-cite-check.md |
```

Located quote: the paragraph after the `10 ** 0` example (25 words), quoted and
byte-offset-located in §1.2.

### 2.3 The brief's S089, drafted — and the census verdict on each of three shapes

The brief's URL is S052's URL. The census rule that bites is **E04** (duplicate URL
*within* a scope) and **W04** (same URL *across* scopes). I built all three shapes
on a `/tmp` copy of the lane corpus and ran the maintained census on each. Observed:

**Shape A — brief's URL, scope different from S052's** → warning only, validation
still exits 0:

```
tameshi-shokunin	W04	S089 duplicate url stryker-mutator.io/docs/mutation-testing-elements/supported-mutators across scopes
tameshi-shokunin	ok	/tmp/r26varA/tameshi-shokunin/corpus/SOURCES.md
exit=0
```

**Shape B — brief's URL, scope identical to S052's, no `supersedes`** → census
**error**, validation exits 1:

```
tameshi-shokunin	E04	S089 duplicate url stryker-mutator.io/docs/mutation-testing-elements/supported-mutators within scope StrykerJS's named single-edit operator classes for JS mutant selection
exit=1
```

**Shape C — brief's URL, scope identical to S052's, `teaches` opening
`supersedes S052 —`** → E04 waived, exit 0:

```
tameshi-shokunin	ok	/tmp/r26varC/tameshi-shokunin/corpus/SOURCES.md
exit=0
```

Shape C is the only same-URL admissible form, and it is the contract's correction
mechanism (SOURCES contract rule 2: "A correction is a new row whose `teaches` opens
`supersedes S0NN —`"). The landed S089 does not need it because it is a *different
page*, so it carries neither E04 nor W04.

Draft of Shape C, should the L1 prefer the brief's URL over a second Stryker page:

```
| S089 | Supported mutators (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ | docs | A | StrykerJS's named single-edit operator classes for JS mutant selection | §Support lead paragraph and §Support table @ page fetched 2026-10-22 (Docusaurus v3.10.2; served last-modified 2026-10-21 16:23 GMT; html sha256 fbbac724…fe98b) | supersedes S052 — the operator families the tenth defect's family names come from | mined | 2026-10-22 | 180d | corpus/knowledge/mutation-case-kumitate-cite-check.md |
```

Located quote for that draft: the `## Support` lead paragraph (24 words), quoted in
§1.2.

---

## 3. Census — run read-only, and the rules the rows must satisfy

### 3.1 The run

The script is read-only (it parses `corpus/SOURCES.md` textually, writes only stdout
or `--out`, never edits the registry) and it is the lane's own no-harm companion
(`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
is named in `.ufo/evidence/round-26/contract.json`,
`claims.C1.no_harm_companions[3]`). Run against the real fleet root:

```
$ cd /home/vgpnk/Projects/shokunin
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi-shokunin	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi-shokunin	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi-shokunin	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi-shokunin	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi-shokunin	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi-shokunin	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi-shokunin	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi-shokunin	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
exit=0
```

**exit 0 — clean.** The seven W04s are pre-existing (S047/S048 and the round-18
correction rows S075–S078, S081) and are warnings only; none belongs to S088/S089.

For completeness, the other two modes, same root:

```
$ ./scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi
tameshi	rows	87
tameshi	tier.A	78   tier.B	7   tier.C	2
tameshi	status.mined	58   status.queued	23   status.rejected	6
FLEET	rows	87 … FLEET	missing	0
$ ./scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin tameshi
tameshi	cadence	S086 recheck=180d opened=2026-10-22
tameshi	cadence	S087 recheck=180d opened=2026-10-22
tameshi	cadence	S088 recheck=180d opened=2026-10-22
tameshi	cadence	S089 recheck=180d opened=2026-10-22
exit=0
```

Both new rows are cadence-reported, not overdue (180d from 2026-10-22).

The frozen manual census from `CORPUS.md` on the same file, all clean:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md            → 87
$ awk -F'|' '/^…S[0-9][0-9][0-9]+…/ && NF!=13 {n++} END{print n+0}'                    → 0
$ awk -F'|' '… tier histogram …'                                       → A=78 B=7 C=2
$ awk -F'|' '… status histogram …'                                     → mined=58 queued=23 rejected=6
$ awk -F'|' '… duplicate ids …' | sort | uniq -d                      → (nothing)
$ awk -F'|' '… enum violations and tier inflation …'                   → (nothing)
```

### 3.2 The census rules these two rows must satisfy

- **NF = 13** (11 columns) — a row with a `|` inside any cell becomes NF ≠ 13 → **E01**
  (malformed). Both landed rows split to exactly 13 fields.
- **id shape `S[0-9]{3,}`** → **E02**; **ids unique** → **E03**. S088/S089 are new
  and unused; the registry's next-unused marker now reads `S090`
  (`corpus/SOURCES.md:336`).
- **E04 — duplicate URL *within* a scope.** A second row on the brief's
  `supported-mutators` URL with S052's scope, status not `rejected`, and no
  `supersedes S0NN` in `teaches` → **E04, exit 1** (proved in §2.3 Shape B). Waived
  only by `supersedes S0NN` in `teaches` (Shape C).
- **W04 — same URL *across* scopes.** Same URL, different scope → warning, exit
  unchanged (Shape A). Both landed rows are warning-free.
- **kind ∈ {spec, docs, paper, code, tool, dataset, talk, book, community,
  own-work}** → **E05**. S088 `code`, S089 `docs`.
- **tier ∈ {A, B, C}** → **E06**; **`community` is never tier A** → **E10**. Both A.
- **status ∈ {queued, mined, rejected}** → **E07**. Both `mined`.
- **`opened` must be a past/present ISO date** → **E08**. Both 2026-10-22 (today).
- **`recheck` must be an ISO date, `Nd`, or a symbolic cadence** → **E09**. Both
  `180d`.
- **W01 — tier C mined with a non-`—` used-by.** Not applicable (both A).
- **W02 — rejected row with a thin `teaches`.** Not applicable.
- **W03 — mined row with `used-by` = `—`.** Both name the entry, so neither fires.
- **E11 — a `mined` row's `used-by` paths must exist on disk**, resolved relative to
  the **lane root**, so the path is `corpus/knowledge/mutation-case-kumitate-cite-check.md`.
  The brief wrote it as `knowledge/mutation-case-kumitate-cite-check.md`; that form
  is E11 and exits 1. Measured both ways on a `/tmp` copy:

  ```
  used-by corpus/knowledge/mutation-case-kumitate-cite-check.md → tameshi-shokunin ok, exit=0
  used-by knowledge/mutation-case-kumitate-cite-check.md         → E11 S088, E11 S089, exit=1
  ```

  The landed rows use the `corpus/…` form and the file exists
  (`corpus/knowledge/mutation-case-kumitate-cite-check.md`, sha256
  `a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e`, 128 lines).
- **E12 — a row-shaped line outside the `## Registry` section.** Both rows are inside
  the Registry (the table spans `corpus/SOURCES.md:8`–`:99`; `## Paths` starts at
  `:102`).
- **Append-only (contract rule 2).** Only `status`, `recheck`, `used-by` change in
  place; a correction is a new row opening `supersedes S0NN —`. Neither landed row
  edits an existing row; S052 is untouched.
- **Row-is-a-claim (contract rule 1).** A row is written only after the source is
  opened in the round that writes it. Both landed rows were opened this session by
  me, with the fetch commands and byte offsets in §1.

---

## 4. Findings for the L1

1. **The brief's S089 URL is S052's URL.** A plain S089 row on
   `…/supported-mutators/` in S052's scope is census error **E04** and fails
   validation; in a different scope it earns **W04** (warning only). The lane landed
   `…/equivalent-mutants/` as S089 instead — a different page, no E04, no W04, exit
   0. That is the sound choice and it is already committed (`40a12bf`). If the
   brief's URL is wanted anyway, §2.3 Shape C is the admissible draft.
2. **The brief's `used-by` path is wrong for the census.** `knowledge/…` is E11;
   the census resolves used-by from the lane root, so it must be
   `corpus/knowledge/mutation-case-kumitate-cite-check.md`. The landed rows have the
   working form, and the landed lesson (`corpus/lessons/round-26.md:48-59`) names the
   landed URLs and both located quotes. The wave-1 lesson *draft*
   (`.ufo/waves/round-26/w1/DraftLesson26.md`) initially copied the brief's URL with
   a `<<QUOTE PENDING>>` marker; seat `DraftLesson26` re-saved it after I reported
   the two census findings, and it now carries the landed rows, both quotes, the
   `4/4/2/2` lookup counts and the S052-unchanged note, with the deviation recorded
   in its own findings for the judge. **Resolved — no stale artifact remains.**
3. **S052's anchor now carries a stale build stamp.** S052 records
   "last-modified 2026-10-19"; the page served on 2026-10-22 reports
   `last-modified: Wed, 21 Oct 2026 16:23:16 GMT` (html sha256
   `fbbac72439fc5d5194bc76bca6b1826a25b86ed6fe1b1cedb843c7046c0fe98b`). The served
   stamp is a **site-wide rebuild**, not an edit to that page: the
   `equivalent-mutants` page carries the identical `21 Oct 2026 16:23:16/17 GMT`
   stamp, and its content differs. The page's *content* still supports S052's
   `teaches` — I re-read the `## Support` table and the operator tables;
   Assignment Expression is still the only ❌ for StrykerJS, and the
   equality/conditional/string-literal/boolean/array-declaration families are all
   still listed. Seat `OpenStrykerMutators` independently re-opened the same page
   for this round (`.ufo/waves/round-26/w1/OpenStrykerMutators.md:39`, full page
   read, 387 lines) and reached the same reading of S052's subject. So this is
   anchor drift, not a wrong row. Fixing it under the append-only rule means a new
   correction row (the S075–S078 pattern), not an in-place edit. **Left to the L1:**
   open it or record it as a known drift.

   Mechanical re-check of S052's `teaches` against the served `## Support` table
   (each row extracted from `/tmp/supported-mutators.html`; the three columns are
   StrykerJS / Stryker.NET / Stryker4s):

   | mutator family in S052's teaches | served Support row |
   |---|---|
   | Equality Operator | `✅ ✅ ✅` |
   | Conditional Expression | `✅ ✅ ✅` |
   | String Literal | `✅ ✅ ✅` |
   | Boolean Literal | `✅ ✅ ️✅` |
   | Array Declaration | `✅ ✅ ❌` |
   | Assignment Expression (the "not supported" one) | `❌ ✅ n/a` |

   Every family S052 names is still listed with the same StrykerJS support value it
   named in round 16; the `Assignment Expression` ❌ for StrykerJS still holds.
4. **Both new rows' `teaches` are count-bearing and now carry their commands.**
   S088 asserts "62-case" and "9 integration-group checks"; both were re-derived
   here (§1.1) — 62 from the pinned gate's own `62/62 cases passed (hermetic)`
   output at exit 0, 9 from `grep -c "checkI("`. The row cell itself states the
   counts without the commands, which is the lane's existing house style for this
   table (S031, S032–S037 do the same) and the knowledge entry carries the
   commands; the lesson's `## Gate` records the row and the quotes. No correction
   proposed.

## 5. Paths

- This report: `.ufo/waves/round-26/w1/DraftSourcesRows.md`
- Landed rows: `corpus/SOURCES.md:97` (S088), `corpus/SOURCES.md:98` (S089)
- Registry next-unused marker: `corpus/SOURCES.md:336` (`S090`)
- Cited entry: `corpus/knowledge/mutation-case-kumitate-cite-check.md`
- Landed lesson Gate rows: `corpus/lessons/round-26.md:48-59`
- Pinned source (read-only, sibling lane): `kumitate-shokunin/scripts/cite-check.mjs`
  @ `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`
- `/tmp` scratch only: `/tmp/cite-check-pinned.mjs`, `/tmp/supported-mutators.html`,
  `/tmp/equivalent-mutants.html`, `/tmp/r26census`, `/tmp/r26varA`, `/tmp/r26varB`,
  `/tmp/r26varC`, `/tmp/r26e11`, `/tmp/r26selftest`
