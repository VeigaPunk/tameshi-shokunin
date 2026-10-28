# T54W1ExecCitations — do the 23 lost sections' citations still resolve at C0?

Seat: T54W1ExecCitations (executor, L1 TameshiR54a2). Item: for each of the 23
headings the round-54 C1 counter loses at C0, extract every lane-relative path
and every `file:line` reference and check it against the **C0 commit only**
(`59c38109bf119d0e9d4f878644a82babc937bc1e`). No lane file was edited; every
write is under `.ufo/waves/round-54/w1/`.

## 0. Verdict

| Layer | Result |
|---|---|
| Path citations (lane blob/tree existence at C0) | **189 checked, 0 missing** |
| `file:line` citations (cited line ≤ the blob's line count at C0) | **99 checked, 0 out of range** |
| Mechanically unresolved | **0 of 288** |
| Content-level unresolved (line exists, does not carry the claim) | **8 anchors across 6 sections** |
| Sections that need a fix | 6 of 23: `## The boundaries…`, `### Using the ledger`, `### The service's limits…`, `### The operator's runbook…`, `## Repeated controls…`, `## Live-tree re-pin…` |

So: **every citation still opens; none of the 23 sections is citation-dead.**
The residual defect is narrower and specific — six sections cite a line number
that the round-54 edit itself (or earlier growth) moved, so the number opens on
the wrong bytes. Section 3 names all six and gives the falsifying command for
each.

## 1. Method (one instrument, no judgement baked in)

`T54W1ExecCitations-receipts/citations.py` (in this directory) does exactly two
things per section, using git objects only:

1. collect every token with a lane prefix (`corpus/ tools/ plans/ .ufo/`) or a
   lane root file (`SKILL.md PROVINCE.md SHONEN.md`), dedupe, and require
   `git cat-file -e REV:<path>` to succeed (blob **or** tree, so a cited
   evidence directory counts);
2. collect every `name:line[-line]` cluster (including the bare `:N` clusters
   that inherit the file their sentence names) and require
   `max(line) <= wc -l REV:<path>`.

Sections come from the same sectionizer the round-54 counter uses
(`.ufo/evidence/round-18/measure.py` at C0), so the 23 spans are the counter's
own, not my paragraphing. Basenames that exist twice (`corpus/knowledge/x.md`
and its round-53 `.ufo/evidence/round-53/assimilation/validate/…` snapshot) are
resolved to the lane's `corpus/`/`tools/` copy by an explicit preference order —
the snapshot copies are never the citation's target.

```
$ export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1ExecCitations
$ python3 .ufo/waves/round-54/w1/T54W1ExecCitations-receipts/citations.py \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    59c38109bf119d0e9d4f878644a82babc937bc1e
…
TOTAL citations checked=288 unresolved=0 across 23 sections
$ echo $?
0
```

Full output: `T54W1ExecCitations-receipts/citations.out`.

Four citations deliberately resolve **outside** the lane and are checked in the
fleet repo instead (the section places them there): `../scripts/hyaku/jj-lane.sh`,
`scripts/shokunin-watchdog.sh@17c1fad`, `shokunin.conf`, `../PROTOCOL.md`. All
four exist. One path is a sibling lane's file, not this lane's
(`tools/mado-verify.sh`, named inside a quoted mado edit) and is excluded.
`tools/__pycache__` is a write-scope name in the shrink-case row, not a
committed citation.

## 2. Per-section tally (the item's requested count)

`paths` = distinct lane paths checked; `file:line` = distinct line citations
checked (bare clusters count once per cluster); `unres` = mechanically
unresolved. Content findings are in section 3 and are not double-counted here.

| section | lines | paths | file:line | unres |
|---|---|---|---|---|
| ## Standing rules | 17–40 | 1 | 2 | 0 |
| ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence | 142–256 | 6 | 34 | 0 |
| ### The boundaries — what a service run is not | 869–893 | 1 | 11 | 0 |
| ## The leg ledger — replay, receipt, and how it is read (round 7, measured) | 932–945 | 2 | 2 | 0 |
| ### Using the ledger | 946–977 | 1 | 11 | 0 |
| ### The tick and the pin read | 1034–1082 | 1 | 3 | 0 |
| ### Triggers T1–T3 and the re-pin rule | 1083–1105 | 1 | 9 | 0 |
| ### The service's limits — what tameshi refuses to mutation-test | 1265–1294 | 1 | 18 | 0 |
| ## The operator's runbook and the six-leg regression (round 10, measured) | 1295–1303 | 0 | 0 | 0 |
| ### The operator's runbook — `corpus/knowledge/operator-runbook.md` | 1304–1324 | 1 | 1 | 0 |
| ## Repeated controls and gate registry — round 12 | 1504–1523 | 4 | 1 | 0 |
| ### Gate/probe registry | 1524–1541 | 6 | 0 | 0 |
| ## Pin disposition and provenance correction — round 13 | 1542–1572 | 7 | 0 | 0 |
| ### Round-13 gate/probe registry | 1573–1588 | 5 | 0 | 0 |
| ## Effective expectation reconciliation — round 14 | 1589–1622 | 9 | 0 | 0 |
| ### Round-14 historical registry — superseded by round 15 | 1623–1634 | 4 | 0 | 0 |
| ## Context gate classification and explicit exit classes — round 15 | 1635–1701 | 6 | 3 | 0 |
| ### Round-15 gate/probe registry | 1702–1732 | 5 | 0 | 0 |
| ## Live-tree re-pin and entry-command monitor — round 17 | 1840–1871 | 8 | 4 | 0 |
| ### Round-17 gate/probe registry — re-pin and monitor | 1872–1880 | 6 | 0 | 0 |
| ### Round-18 gate/probe registry — routed-defect closure | 1951–1963 | 11 | 0 | 0 |
| ### Round-21 gate/probe registry — finite environment differential | 1990–2129 | 25 | 0 | 0 |
| ### Round-26 gate/probe registry — report interop | 2158–2197 | 78 | 0 | 0 |
| **total** | | **189** | **99** | **0** |

Nine sections carry no `file:line` citation, and that is a property of their
shape, not a gap in the check: `## The operator's runbook and the six-leg
regression` is a transitional paragraph with no citation at all, and the eight
table-only registries (`### Gate/probe registry`, `### Round-13`, `### Round-14`,
`### Round-15`, `### Round-17`, `### Round-18`, `### Round-21`, `### Round-26`)
cite pinned **values** and evidence paths rather than lines. Their path counts
are in the table above and every one of them resolves at C0.

## 3. Findings — 8 citations that open on the wrong bytes

Every command below runs with

```
lane=/home/vgpnk/Projects/shokunin/tameshi-shokunin
rev=59c38109bf119d0e9d4f878644a82babc937bc1e
```

The round-54 edit moved line numbers inside two files it edited:

* `SKILL.md` +8 lines (one hunk, all inside `## Standing rules`):
  `git -C $lane diff -U0 d33053f7 59c38109 -- SKILL.md` → `@@ -29,6 +29,8 @@`, 2197−2189 lines.
* `corpus/SOURCES.md` +3 lines at 152–154 (rows S277–S279) plus 2 at the tail:
  `git -C $lane diff -U0 d33053f7 59c38109 -- corpus/SOURCES.md` →
  `@@ -151,0 +152,3 @@` and `@@ -509,0 +513,2 @@`.

Every page-relative anchor below line 31 of `SKILL.md`, and every `SOURCES.md`
anchor below line 151, therefore shifted; the prose that carries the anchors
did not. Each finding is byte-exact in both the section and `SKILL.md` at C0
(verified by substring test, section 6).

### F1 — `## The boundaries — what a service run is not` (1)

> `porcelain-clean is an opt-in precondition at open (SKILL.md:808-809)`

**Why:** at C0 lines 808–809 are the mutation-service introduction, so the
self-reference no longer lands on the opt-in precondition.

```
$ git -C $lane show $rev:SKILL.md | sed -n '808,809p;817p;820p' | cut -c1-120
method outward as the service the fleet census offered
(`fleet-suite-census.md:249-291`): an opting-in lane brings its own gate, the
### The opt-in contract — what the lane brings
   count, mtime, and a porcelain-clean sibling tree at open. Mado's pin:
```

Written against base, where 809 was exactly `### The opt-in contract — what the
lane brings` and 812 carried "porcelain-clean sibling tree at open"; the +8
insertion moved them to 817/820. Correct C0 anchor: **819–820** (or 817 for the
block heading).

### F2 — `## The boundaries — what a service run is not` (2)

> `a low kill rate is a report, not a service failure (SKILL.md:335)`

**Why:** at C0 line 335 carries the 50-80/>80 boundary note, and neither the
`<50 %` band row nor the "Bands are a report convention, not a pass/fail gate"
rule the claim paraphrases is inside 335.

```
$ git -C $lane show $rev:SKILL.md | sed -n '335p;342p;346,347p' | cut -c1-120
Both points sit on the 50-80/>80 boundary, so that boundary reading is the
| **<50 %** | nominal: green is a count, not a catch | never cite it as protection; the round admits anyway — the surv
- **Bands are a report convention, not a pass/fail gate.** An 8/10 admits, and so
  does a <50 % — with the gap recorded in the table, not softened
```

At base the `<50 %` row was 334 and 335 its blank terminator; C0 puts the row at
342 and the rule at 346–347 (+8).

### F3 — `### Using the ledger` (1)

> `tool lines re-verified at C**`

**Why:** `C**` is not a revision (nor a sha prefix, nor an evidence id) — there
is nothing for a reader to open, so the parenthetical's claim that the tool
lines were re-verified is unanchored, against the page's own rule that every
claim carries "path:line, command output, evidence id".

```
$ git rev-parse --verify 'C**^{commit}'
fatal: Needed a single revision
```

The neighbouring claim in the same sentence is anchored properly
(`:1247-1317,1459-1517`, both inside the 2160-line tool), which is what makes
the placeholder stand out. Either name the revision or drop the clause.

### F4 — `### The service's limits — what tameshi refuses to mutation-test` (1)

> `` spec/control failures are `MUTATE: SETUP`, exit 2, no headline | `:813-817`; `:840-844` ``

**Why:** row (b)'s service-side anchor `:840-844` opens on the protocol preamble
and the command block, not on the `MUTATE: SETUP` / exit-2 rule the cell states.

```
$ git -C $lane show $rev:SKILL.md | sed -n '840,844p;853p' | cut -c1-120
All writes in scratch, through the pinned harness `tools/mutate-and-run.sh`
(the mado run used revision `597e1419…ff6331b`, 1001 lines, commit `b58b26fb`; this path now holds a later revision, s
`git show b58b26fb:tools/mutate-and-run.sh`; every run log carries its own `MUTATE_TOOL` pin; corrected in round 27, sea

```bash
   `MUTATE: SETUP (<reason>)`, exit 2 — no headline.
```

The rule the cell states is at **853**, the last of the protocol's ordered
steps, not at 840–844. The first anchor of the same cell, `:813-817`, also
points at the round-6 measure clause at C0; only by reading on to the opt-in
contract at 819–825 does a reader reach "one-command hermetic suite".

### F5 — `### The service's limits — what tameshi refuses to mutation-test` (2)

> `never measured — sensitivity ≠ truth | `:879-881``

**Why:** at C0 lines 879–881 are the "Findings kept, never smoothed" bullet; the
`Sensitivity, not truth` bullet the cell cites is at 890–892.

```
$ git -C $lane show $rev:SKILL.md | sed -n '879,881p;890,892p' | cut -c1-120
  a low kill rate is a report, not a service failure (SKILL.md:335). Mado's 40 % is the
  first point below the 50-80 band (`mutation-case-mado-verify.md:175-176`), and it reads as composition (4 in-surface
  + 6 out-of-surface, measured 4/4 and 0/6), not as a suite regression
- **Sensitivity, not truth** — a sweep measures what the suite can detect,
  never whether the gate's verdicts are right
  (`mutation-case-mado-verify.md:229-230`).
```

The section closes with "Anchors re-resolved 2026-10-14 on the live bytes; a
reader on a differing revision re-resolves rather than trusts" — but every
anchor in that table is base-anchored shifted, so the disclaimer does not
restore them at C0. Correct anchors: rows (b) → 819–825, (c) → 819–825 / 838–839,
(f) → 890–892.

### F6 — `### The operator's runbook — corpus/knowledge/operator-runbook.md` (1)

> `` rule this page applies to `service-limits.md` (`:1250-1254`) ``

**Why:** at C0 lines 1250–1254 are the round-9 T1 re-pin bullets, not the
rendering/divergence rule the sentence says this page applies.

```
$ git -C $lane show $rev:SKILL.md | sed -n '1250,1254p;1276,1277p'
  never an edit of the recorded table.
- **The intake precondition round 8 named is present, not errata.** The opt-in
  protocol carries the re-pin rule — "A moved substrate needs a re-pin, never a
  re-interpretation of the old table"
  (`corpus/knowledge/service-optin-protocol.md:59-62`) — cited here.
and the intake-precondition check; this page is the compact rendering, and a
divergence between the two is the finding, never smoothed.
```

Correct C0 anchor: **1276–1277**. This one was already ~18 lines stale at base
(base 1268–1269) and is 26 lines stale at C0: the +8 insertion plus earlier
rounds' growth. It is the only finding here whose drift predates this round by
more than one screen.

### F7 — `## Repeated controls and gate registry — round 12` (1)

> `` (S026 superseded by S265, `corpus/SOURCES.md:500`) ``

**Why:** at C0 line 500 is the round-46 "Next unused id: S265" bullet — the
opposite statement, that S265 is not yet used — while the supersession the
parenthetical claims is at line 503.

```
$ git -C $lane show $rev:corpus/SOURCES.md | sed -n '500p;503p'
- Next unused id: S265 (S261–S264 are map-only reserved; staged ids S161–S255 stay reserved by document for the package).
- Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; snapshots and receipts under `.ufo/evidence/round-48/freshness/sources/`).
```

This is the cleanest instance of the round's own drift: at base line 500 was
exactly the Round-48 supersession bullet, and the three S277–S279 rows inserted
at 152–154 moved it to 503. Correct C0 anchor: **503**.

### F8 — `## Live-tree re-pin and entry-command monitor — round 17` (1)

> `` selftest `v2-registry-clone-detached-anchor` :2891-2896 expects exit 0, fixture docstring :2256 "anchors at HEAD" ``

**Why:** at C0 `:2891-2896` is the unrelated `v2-historical-tag-object` case and
`:2256` is a bare closing paren; the named case starts at 2911 and the named
docstring at 2275.

```
$ git -C $lane show $rev:tools/evidence-disposition.py | grep -n 'v2-registry-clone-detached-anchor\|anchors at HEAD'
2911:        "v2-registry-clone-detached-anchor",
2275:    """A detached harness clone anchors at HEAD, not its later remote tip."""
$ git -C $lane show $rev:tools/evidence-disposition.py | sed -n '2891,2896p'
    historical_case(
        "v2-historical-tag-object",
        2,
        ["historical_input_unavailable"],
        _setup_hist_tag,
    )
```

The tool grew +9 net lines this round (`12 insertions, 3 deletions`), all above
these anchors: at base the case was 2906 and the docstring 2270, i.e. **+5** at
C0 on top of an already ~15-line staleness. Correct C0 anchors: **2911–2916**
and **2275**.

## 4. Opened and resolved — positive evidence, not assumed

Each of these was opened at C0 and the cited line carries the claim. They are
the reason 17 of the 23 sections are clean and the reason the six above are
narrow rather than wholesale.

| citation | C0 fact |
|---|---|
| `corpus/knowledge/operator-runbook.md` `e1e349b6… / 511 L / 31 416 B` (sec 09) | blob `329398d6…` is 31 416 B, 511 lines, sha256 `e1e349b6…` — the cited triple is exact, and the "the sha governs" caveat explains the 516-line C0 file |
| `tools/mutate-and-run.sh@9f1d3c3:72-109`, `:511-522` (sec 03) | revision resolves (1341 lines); 72–78 is the four-leg table with rates, 511–522 the `PIN_*`/`REV_*`/`TABLE_*` block |
| `tools/mutate-and-run.sh@4b7c682:597-620` (sec 03) | revision resolves (1940 lines); 597–620 is the eight-leg pin + verdict-table block the sentence points at |
| `tools/mutate-and-run.sh:434`, `:579-583`, `:614-643`, `:671-849`, `:83-108`, `:1275-1317`, `:1302-1306`, `:1459-1508`, `:78-79`, `:36-38`, `:139-143` (sec 01/02/04) | all inside 2160 lines and on the claimed constructs (`APPLY FAIL … old-string-count`, the DEGRADED division, `PIN_*`/`TABLE_*`, `regression_specs`, the leg inventory, the git materialization, `REGRESSION_PIN` format, the ten dispatches) |
| `corpus/knowledge/fleet-kill-rate-ledger.md:156-158`, `:170-173`, `:220`, `:281`, `:310`, `:318`, `:420` (sec 06/07) | 156–158 "suite sensitivity ≠ gate truth"; 170–173 "appended row, not an edit of §1–§4"; 220 U2; 281 the ER-1 supersession with `cf41efaa…`; 310 ER-3 re-pin; 318 ER-4; 420 ER-jj branch-tip rule |
| `corpus/SOURCES.md` rows S003, S004, S026, S041, S047, S048, S049, S051, S061, S062, S063, S079, S082–S085, S265, S277, S278, S279 | all present at C0; S277–S279 are the rows this round added (152–154) |
| `scripts/shokunin-watchdog.sh:3-5`, `:14` at fleet `17c1fad` | resolves in the fleet repo: 3–5 "Tick 450s.", 14 the `LANES=` map, which does not name tameshi |
| `.ufo/evidence/round-14/capture-context.py` `:2-31`, `:553-580`, `:605-643` (sec 16) | 647-line blob; 2–31 the module docstring, 553–580 `decide()`, 605–643 `main()` |
| `tools/evidence-disposition.py:368-390`, `:460-525` (sec 18) | inside 3246 lines and on the `GIT_*` scrub / shallow + `for-each-ref` anchor logic |
| `mismatch/expected.json`, `coldread/assemble.py`, `coldread/ledger.json`, `round-23/replay.py`, `rerun-20261020T035435Z/summary.json` | every shorthand path expands to an existing C0 blob (`.ufo/evidence/round-12/ControlGate/mismatch/expected.json`, `.ufo/evidence/round-18/coldread/*`, `.ufo/evidence/round-23/replay.py`, `.ufo/evidence/round-12/BashWitness/rerun-…/summary.json`) |

## 5. Recorded, not charged

* **`### The service's limits…`, `:813-817` and `:823-825`.** Both shifted by the
  same +8 and now open on adjacent text that still contains the claim's subject
  ("one-command hermetic suite" at 813–815; "moved substrate needs a re-pin" at
  823). A reader lands close enough; only `:840-844` and `:879-881` (F4, F5)
  open on unrelated prose, so only those are charged. A re-anchor of the whole
  table should still move all four.
* **`tools/evidence-disposition.py:368-390`.** The range ends on the first line
  of `GIT_ENV_OVERRIDES = {` (390) rather than inside it; the `GIT_NO_REPLACE_OBJECTS` /
  `GIT_GRAFT_FILE` values are the next few lines. Off by a few, in the right
  neighbourhood — not charged.
* **Content claims I did not try to falsify** and therefore claim nothing
  about: selftest tallies quoted as prose (e.g. `66/66`, `51/51`, `9/9`), the
  per-round narrative counts, and external-source line ranges inside
  `SOURCES.md` rows (e.g. S278's `:163-165` of CPython `Lib/tempfile.py`). Those
  need the named upstream bytes, not the lane's objects.
* **The nine sections with no `file:line` citation** (see section 2) are not gaps
  in this check, just sections that cite pinned values and paths instead of
  lines.

## 6. Reproduce

```
lane=/home/vgpnk/Projects/shokunin/tameshi-shokunin
rev=59c38109bf119d0e9d4f878644a82babc937bc1e
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1ExecCitations   # scratch; deleted after the run

# the section spans the counter uses
python3 $lane/.ufo/waves/round-54/reader-section.py $lane $rev "<heading>"

# the mechanical sweep (0 unresolved)
python3 $lane/.ufo/waves/round-54/w1/T54W1ExecCitations-receipts/citations.py $lane $rev

# the drift that causes F1/F2/F6
git -C $lane diff -U0 d33053f7552d $rev -- SKILL.md
# the drift that causes F7
git -C $lane diff -U0 d33053f7552d $rev -- corpus/SOURCES.md
# the drift that causes F8
git -C $lane diff --numstat d33053f7552d $rev -- tools/evidence-disposition.py

# each finding's falsifier, e.g. F1
git -C $lane show $rev:SKILL.md | sed -n '808,809p;817p;820p'
# each finding's quote is byte-exact in its section and in SKILL.md at C0:
#   python3 -c 'import sys;q=sys.argv[1];print(q in open(sys.argv[2]).read())' "<quote>" <file>
```

## 7. Bounds kept, and residual risk

* **No lane file was edited.** The only writes are
  `.ufo/waves/round-54/w1/T54W1ExecCitations.md`, this directory's
  `citations.py` and `citations.out`. No fixture was needed, so
  `T54W1ExecCitations-receipts/` holds the instrument and its output only.
* **No mutating git:** every git call is `show` / `cat-file` / `ls-tree` /
  `rev-list` / `diff` / `rev-parse`, read-only, `-C` on the lane or the fleet
  root.
* **Scratch** `/fast/scratch/hyaku/tameshi-r54/T54W1ExecCitations/` is removed
  at the end of this run (`rm -rf`; the tree holds only the C0 dumps and the
  generated `spans.json`).
* **Tooling:** nothing installed — the check needed only `python3` and `git`.
* **Residual risk / what a re-read must not assume:** the line numbers here are
  C0-bound. Writing the section numbers into prose without moving the anchors
  makes them stale again the next time anything is inserted above line 31 of
  `SKILL.md` or line 151 of `corpus/SOURCES.md` — which is exactly how F1, F2
  and F7 arose. The safest repair is an anchor that survives insertion (a
  heading name, a bullet's first words, or an evidence path), or a line figure
  introduced together with the bytes it names.
