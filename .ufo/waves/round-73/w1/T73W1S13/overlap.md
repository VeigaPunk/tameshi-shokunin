# R73-C1 — sibling-overlap scan + assimilation reachability (seat T73W1S13)

Read-only seat. Nothing outside this directory and `/fast/scratch/hyaku/tameshi-r73/T73W1S13/`
was written (scratch removed before yield). Every claim below names the command that produced it.

**The class under test** (as the frozen plan R73-C1 states it): *a checker that compares a round
record's execution claims — seat count, committed seat-report count, role multiset, attack share —
against the committed wave artifacts, at pinned revisions, with `expect: meet|drift` standing arms.*

Two questions per candidate: (a) does it read a **record** (report / plan / lesson / SCORECARD) and
extract a printed claim? (b) does it re-derive the population from **committed wave artifacts**
(`*-results.json`, dispatch counts, seat-report files, registry member lists)?

---

## 0. Scope actually scanned

```
$ ls -d */tools 2>/dev/null
chousa-shokunin/tools  kaidoku-shokunin/tools  kama-shokunin/tools  kotodama-shokunin/tools
mado-shokunin/tools    mori-shokunin/tools     souji-shokunin/tools  tameshi-shokunin/tools
tsukuroi-shokunin/tools
$ ls -d */corpus/knowledge 2>/dev/null | wc -l
21
```

Nine lanes hold a top-level `tools/` surface; `kaidoku-shokunin/tools/` holds only `round-N/`
subdirectories (round-25 … round-67) and was walked at that depth. The other twelve lanes have no
top-level tool surface (`game-dev-2d`, `game-dev-3d`, `audio`, `kagi`, `kake`, `kasegi`, `kengaku`,
`kotoba`, `kumitate`, `lore`, `revenger`, `tabi`), so a lane-held instrument of the class cannot exist
there under the named scan surfaces.

Search patterns run over the nine tool dirs:

```
$ grep -E 'results\.json|-results\.json|\.ufo/waves' <nine tool dirs>          # 260 matches
$ grep -E 'attack[- _]?share|labrat|revenger|attack roles|frozen swarm roles|swarm roles'
$ grep -E 'attack share|attack_share|role multiset|role_counts|role mix|seats=|seats ==|seat count'
$ grep -lE 'seat|results\.json|reconcil' */tools/*.sh                          # 14 files, all noise
$ grep -l -- '-results\.json' */tools/*.sh                                     # 1 file
```

The only shell tool that touches a wave results file is
`souji-shokunin/tools/souji-wave-evidence-capture.sh` — an evidence *custody* tool (copies a round's
`.ufo/waves` evidence into a census receipt and can re-verify it against `git ls-tree`/`cat-file` at
`--rev`); it reconciles bytes with bytes, never a record claim. It is not of the class.

Knowledge sweep (`*/corpus/knowledge/*.md`, 21 dirs) for the class:

```
$ grep -E 'wave-reconcile|record-vs-artifact|record vs artifact|wave artifact.*count|seat count.*committed|reports.*committed.*artifact'
No matches found
$ grep -E 'seat report|seat-report|declared members|report_artifacts|reports=|report count'   # 38 files
```

All 38 hits are *citations* to seat reports inside knowledge entries, except the two mori entries
listed in the table below (`wave-settlement-r20.md`, `wave-settlement-artifacts-r59.md`), which
document the artifact shape rather than a record-vs-artifact checker.

---

## 1. Candidate table — does another lane hold this ground?

| lane | path | record read? | artifact population | what it checks | verdict vs C1 |
|---|---|---|---|---|---|
| **kaidoku** | `tools/round-47/record.py` | **yes** — `SCORECARD.md` `## Round N` sections at `--rev` | **yes** — `.ufo/waves/round-N/*-dispatch.json` → `counts.spawn`, in file order | atoms `seats` (`Waves: A + B = C seats`, `Wave 1: A seats; wave 2: B seats`), `window`, `path`, `rev`, `axes`; `- corrects <class> <key>:` append-only exemptions re-derived | **DUPLICATE of the `seats` row class**, cross-lane and already landed. Differs: record surface is SCORECARD's round section (not the round report/plan); artifact is dispatch `counts.spawn` (not `results[]`/`seats`); no drift arms (correction-exemption model); no `seat_reports`, `roles`, `attack_share` |
| **kaidoku** | `tools/round-30/settle-gate.py` | no | yes — `*/swarm-registry.json` members, `settle.tsv`, `<reportDir>/<name>.md` bytes | `MISSING_ROW`, `REPORT_ABSENT`, `REPORT_SHA_MISMATCH` (a seat that rewrote its report after settling) | **DUPLICATE of the seat/seat-report population idea**, but dispatch-side only; no printed claim is read |
| **kaidoku** | `tools/round-42/prefile-gate.py` | no | yes — `*.ready`, `*.ready.dispatched`, `*-results.json`, dispatch `counts.total` | advisory: `results` entries ≠ declared `seats`; entries < dispatch total (partial) | **ADJACENT** — artifact-internal consistency, not a record claim |
| **kama** | `tools/seat-yield.py` | no — expectation is a CLI flag (`--expect-reports N --expect-seats N`) | **yes** — `<wave>-results.json` + `out/<seat>.md` (and the round-44 nested `out/<seat>/<seat>.md`) | `wave=<name> seats=S status=… reports=R missing=M` | **DUPLICATE of the `seat_reports` counting mechanism**; the expectation is typed by the caller, not bound to a record span or a revision |
| **kama** | `tools/report-landing-audit.py` | **yes** — fleet `.ufo/reports/round-N/kama.md` | no (git commit objects) | unresolved full hashes, landed-commit omissions, missing `## Landed changes` | same *record* surface, different claim class (citations, not counts) |
| **kama** | `tools/pre-report-gate.py` | yes, indirectly | — | one gate over four reconciled instruments (selfdesc reconciler, newest-closure counter, receipt-pointer audit, worktree-landing) | **ADJACENT** — a meta-gate; none of its arms is a wave-population reconciler |
| **kama** | `tools/round42-selfdesc-reconcile.py` | yes — SCORECARD head/README/PROVINCE | no | self-description surfaces vs repo state at `--tip` | **ADJACENT** — record-vs-tree, not record-vs-wave-artifact |
| **kama** | `tools/manifest-crosscheck.py` | yes — trend-verdict ledger `outside` rows | no | ledger verdicts vs fleet `MANIFEST.json` closure entries | record-vs-record; not the class |
| **mori** | `tools/mori-settlement-scan.py` | no | **yes** — one or more `<wave>-results.json` | `seats == len(results)`, member key set, `agent` ∈ ten frozen roles, duplicate names, `role_counts` | **ADJACENT, and the nearest `roles` neighbour**: it computes the executed role multiset but compares it to the *role vocabulary*, never to a record's declaration. It also holds the `seats == len(results)` arithmetic |
| **mori** | `tools/mori-unlanded-check.py` | no (motivated by a report's seat count) | yes — `.ufo/waves/round-N/` paths in `git status --porcelain` | work on disk not committed | **ADJACENT** — tree-vs-index; same *motivation* ("the report's seat count was not what the repository held") |
| **mori** | `tools/mori-vote-bind.py` (documented by `corpus/knowledge/vote-binding-r56.md`) | **yes** — a knowledge ledger's vote rows | **yes** — committed `.ufo/waves/round-55/w1-results.json` | `TALLY rows=78 agree=78 … voters=16 bound_voters=15` | **record-vs-artifact, different claim class** (votes/quotas, not seats/roles/share) |
| **chousa** | `tools/claims-audit.py` | **yes** — frozen claims file | committed bytes via generic check classes | statements the repo contradicts, driven by a rule TSV | record-vs-committed-bytes; no wave population |
| **souji** | `tools/souji-citation-reconcile.py` | **yes** — self-assessment cells | committed receipts | quoted after-values vs receipt bytes | record-vs-receipt; no wave population |
| **souji** | `tools/souji-wave-evidence-capture.sh` | no | yes (custody) | captures/verifies wave evidence against `--rev` blobs | custody, not claims |
| **tsukuroi** | `tools/check-seat-scope.py` | no | yes — `swarm-registry.json` ∪ `spec.json`, `<Name>.md` | `Scope:` trailer vs `EXEC-AUTHORIZED`; seat names and roles are read from registry ∪ spec | **ADJACENT** — roles are consumed, never reconciled to a record claim |
| fleet (out of the named surfaces) | `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs` (§263) | no | no | dispatch-time topology: `planner`/`distiller`/`labrat`/`Main` are frozen-topology seats, the ten `proposalRoles` are the swarm | pre-dispatch validator; **no attack share, no floor** |

`corpus/knowledge` entries that document the population (not checkers):
`mori-shokunin/corpus/knowledge/wave-settlement-r20.md` ("for every
`ufo-swarm-wave-dispatch-v1` file … which declared members have a non-empty report at their
`Report:` trailer path") and `wave-settlement-artifacts-r59.md` (shape facts of committed
`<wave>-results.json`, recheck `python3 .ufo/waves/round-59/count-c2.py R`).

### Is the ground new?

**New as a class, not new in two of its four row kinds.** No lane holds a *manifest-driven standing
sweep* that binds a record span at a record revision to a wave artifact population at an artifact
revision. That composition is new. But:

- **`seats` is already held cross-lane** by `kaidoku-shokunin/tools/round-47/record.py`
  (SCORECARD claim → `dispatch.json` `counts.spawn`, at `--rev`). The plan's Before-sentence — "No
  instrument compares a round record's execution claims with the committed wave artifacts" — is
  **overstated for this row kind**. State it as inherited ground, not as novelty.
- **`seat_reports` is already held** as a counting mechanism by `kama/tools/seat-yield.py` and as a
  population by `kaidoku/tools/round-30/settle-gate.py`. What C1 adds there is the *binding* (the
  printed integer must be a delimited token of a byte-substring of the record at the record rev).
- **`roles` is new as a record-vs-executed-multiset comparison.** The only role multiset in the fleet
  (mori) compares against the role vocabulary, and tsukuroi reads roles from the spec that dispatched
  them — neither compares a record's declaration to the agents that actually ran.
- **`attack_share` is held nowhere.** `ufo-wave-policy.json` has no `attack` key at all
  (`grep -n -i attack scripts/hyaku/ufo-wave-policy{,-v2}.json` → no line); the plan's "policy's
  named set" is the plan's own reading. The row's `named`/`floor_pct` are self-declared, which the
  shipped manifest already discloses (`ATTACK_NOTE`).

---

## 2. Cousin table — this lane's nearest instruments

All six read from git objects only, never the worktree; all six ship a manifest or a document sweep;
the pattern is the lane's established idiom since round 65.

| tool | claim class it covers | source of truth | manifest / rows | red arms | verdict token |
|---|---|---|---|---|---|
| `tools/receipt-exists.py` | a record's cited `.ufo/` or `tools/` path **exists** at the pinned rev | `git cat-file -e REV:path` | none — per-document sweep | n/a | `RECEIPT_EXISTS doc= checked= skipped= missing=` |
| `tools/receipt-commit-bind.py` | a commit message's **receipt names** are carried by the bytes of that commit / range | git objects, three arms over `base..tip` | none — range sweep | 3 arms | `RECEIPT_COMMIT_BIND`, `BIND_OK` / `BIND_DEFECT` |
| `tools/quoted-line-exists.py` | a **quoted counter line** in a record is byte-equal to a cited receipt's committed bytes | `git cat-file blob REV:path` | none — `--quote` or `--doc` sweep | n/a | `QUOTED_LINE_EXISTS …` |
| `tools/count-recheck.py` | a record's **printed counting figure** equals the count its **named command** produces at the revision the record names | re-runs `git grep -c [-E] <pattern> <rev> -- <path>` | `count-recheck.json`, 7 rows | 2 (`expect=drift`: `scorecard-r68corr-unanchored-r67tip`, `lesson-r69-unanchored-r67tip`) | `COUNT_RECHECK …` |
| `tools/pointer-recheck.py` | a record's **cited line pointer** still points at the content the record claims, at the named revisions | `git cat-file blob rev:path \| sed -n START,ENDp` | `pointer-recheck.json`, 12 rows | 3 (`expect=miss`) | `POINTER_RECHECK …` |
| `tools/anchor-drift-sweep.py` | a held source row's **anchor heading** still matches its pinned snapshot's heading | snapshot blob at rev | `anchor-drift-sweep.json`, 16 rows | 1 (`expect=absent`, `s299-anchor-as-written`) | `ANCHOR_DRIFT …` |
| `tools/figure-attribution.py` | a record's **single figure** is attributed to receipt bytes | receipt bytes | `figure-attribution.json`, 3 rows | 1 (`expect=misattributed`) | `FIGURE_ATTRIBUTION …` |
| **`tools/wave-reconcile.py`** (in-flight, untracked) | a round record's **printed execution claims** — seats, committed seat-report count, role multiset, attack-share floor — vs the **committed wave artifacts** | two revs and two roots: record blob at `record.rev` (`lane` \| `fleet` via `--extra-root`), artifacts at `wave.rev` (`ls-tree` listing + `cat-file blob`) | `wave-reconcile.json`, 6 rows | 2 (`expect=drift`: `r72-report-seatreports`, `r72-plan-roles`) | `WAVE_RECONCILE: rows=6 met=6 unexpected=0` |

Manifest row census, measured:

```
$ python3 - … (schema / rows / id / kind / expect per manifest)
== count-recheck.json schema tameshi-count-recheck-v1 n= 7        (2 expect=drift)
== pointer-recheck.json schema tameshi-pointer-recheck-v1 n= 12   (3 expect=miss)
== anchor-drift-sweep.json schema tameshi-anchor-drift-v1 n= 16   (1 expect=absent)
== figure-attribution.json schema tameshi-figure-attribution-v1 n= 3 (1 expect=misattributed)
== arm-liveness.json schema tameshi-arm-liveness-v1 n= 9
== wave-reconcile.json schema tameshi-wave-reconcile-v1 n= 6
    r72-report-seats    kind= seats        expect= meet
    r72-report-seatreports kind= seat_reports expect= drift
    r72-plan-seats      kind= seats        expect= meet
    r72-spec-roles      kind= roles        expect= meet
    r72-plan-roles      kind= roles        expect= drift
    r72-attack-share    kind= attack_share expect= meet
```

### What the new instrument adds, precisely

1. **A population that is not a command's stdout.** Every cousin measures a *scalar against bytes*
   (a count from `git grep -c`, a line span, a heading, a figure). `wave-reconcile` measures against
   (i) an **array** (`results[]`, `results.seats`) and (ii) a **directory listing**
   (`*.md` at the top of the wave dir at the artifact rev). No existing row kind in the lane does
   either.
2. **A multiset equality claim** (`roles`) and a **threshold claim** (`attack_share`). The cousins
   model equality/position/attribution of one value. A multiset against a record's `N role` token
   list, and a share against a declared floor, have no ancestor in this lane's manifests.
3. **Two roots in one sweep.** The record lives in the fleet repo (`.ufo/reports/round-N/<lane>.md`)
   while the artifacts live in the lane. `--extra-root fleet=<path>` is the `receipt-exists.py`
   precedent generalised to a *row-level* `root` per side — record and artifact each resolve
   independently.
4. **What it does *not* add, and should not claim**: the seats arithmetic (kaidoku r47), the
   report-file census (kama seat-yield), and the claimed-totals-vs-derived-members check
   (`tools/wave-accounting.py`'s `TOTAL_MISMATCH`, on a digest-pinned declared bundle). Those are
   inherited ground.

---

## 3. In-lane instruments that already touch the "claimed vs observed" arithmetic

- `tools/wave-accounting.py` — `evaluate()` compares a declared `claimed` triple
  (`seats`/`completed`/`dead`) to the derived summary and raises `TOTAL_MISMATCH`; it also checks
  `IDENTITY_MISMATCH` between declared member role and observed outcome role, and inventories
  `report_artifacts=len(reports)` while refusing to let report presence supply completion
  (`corpus/knowledge/callback-authoritative-accounting.md`: "Report prose and file presence never
  supply the completed count"). **This is the in-lane ancestor of the `seats` row's arithmetic**, on a
  declared bundle rather than on a record span + git artifacts.
- `tools/wave-route-mix.py` — builds a **role census of a wave spec** and resolves each role through
  the live routing table to refuse provider concentration (`ROUTEMIX: OK seats=N max_share=…`). It
  reads roles *before* dispatch; it never compares them to the agents that ran.
- `tools/wave-parent-settle.py`, `tools/arm-liveness.py` — settlement/liveness, not claims.

---

## 4. Assimilation reachability

```
$ ls -la /home/vgpnk/Projects/shokuknow/merge/tameshi/
drwxr-xr-x … .        -rw-r--r-- … 39434 MERGE-REPORT.json   -rw-r--r-- … 21804 MERGE-REPORT.md
-rw-r--r-- … 154031 SOURCES.append.md
drwxr-xr-x … amendments/            drwxr-xr-x … knowledge/
$ head -3 MERGE-REPORT.md
# Merge package — tameshi

Staged by `corpus-expansion-1`. **Nothing was written into the lane repo.**
$ find amendments knowledge -type f | wc -l
85
$ stat -c '%y %n' MERGE-REPORT.md
2026-10-24 23:33:20 MERGE-REPORT.md
```

Census as the package states it (read, not re-derived):

- proposed rows **accepted 103**, **refused 0**
- proposed **knowledge entries 86** (`MERGE-REPORT.json` `entries` len 86)
- **`existing_rows` 107** at staging; `renumbered` list empty; first staged id **S153**
- rows by round (16 rounds): round1=14, round2=8, round3=7, round4=6, round5=5, round6=4, round7=5,
  round8=9, round9=5, round10=5, round11=5, round12=4, round13=8, round14=11, round15=4, round16=3
- one target-path conflict (`corpus/knowledge/japanese-flaky-verdict-and-environment.md`, rounds 13/2),
  four `used-by` pointers corrected at packaging time, 5 rows flagged as already-held pages
  (S153/S154/S196/S209/S211)

**The census is a 2026-10-24 staging snapshot and is stale for round 73.** The lane's registry now
holds **163** rows (`grep -cE '^\| S[0-9]{3}' corpus/SOURCES.md` → 163), not 107, and the package has
already been *partially* assimilated by document — `corpus/SOURCES.md` records staged S159/S160 →
S155/S156 (round 42, line 506), staged S182/S183 → S269/S270 (round 49, line 531) and staged S167 →
S271 (round 50, line 533). Reading 103/107 as "today's pending work" would overstate it.

`ASSIMILATION=readable directory lists, MERGE-REPORT.md head reads, census 103 accepted / 0 refused / 86 entries / existing_rows 107 at 2026-10-24 (stale: registry now 163 rows and three landed staged→row mappings)`
