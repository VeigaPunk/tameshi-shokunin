# RevGuardScope — is a staged-registry id guard in tameshi's province? (round 43, w2)

Lane: tameshi-shokunin. Mission: province fit (adjacency) of C3's
`tools/staged-id-guard.py`. Read-only on the lane; the only write is this file.
No counter was run (bounds: never at `c5335c70`; and no counter answers this question).

## Verdict

**In province — as a lane-local gate on tameshi's own `corpus/SOURCES.md`, not as a
fleet registry tool.** Neither chousa nor kumitate is the home: **no lane in the roster
owns "registry curation"**, and kumitate's "tooling" is scoped to the ufo-fsd
script/runtime surface. The registry *contract* is fleet doctrine (PROTOCOL.md:435), the
registry *instance* is per-lane (PROTOCOL.md:398), and tameshi's PROVINCE names its own
as Core (:37-38). The margin is the four boundary conditions in §5 — crossing any of
them flips the verdict, and §6 D6 is then mandatory.

## 1. The PROVINCE lines that decide it

All quotes are `tameshi-shokunin/PROVINCE.md`, numbered by `cat -n PROVINCE.md`.

| line | quote | why it decides |
|---|---|---|
| `:3-5` | "**Domain:** verification-fixture craft — the reusable method of honest checks: hermetic suites, mutation testing, **fail-closed arms**, verdict-line discipline, no-permissiveness audits, **before/after proof**." | The guard is a fail-closed refusal instrument: every malformed input class exits 2 as a setup refusal, the map verdict is `admissible`/`inadmissible`, and it ships a selftest plus a do-nothing counter control (`.ufo/evidence/round-43/guard/measure.py` docstring; contract C3 `do_nothing_control`). The domain sentence governs the *craft*, not the subject matter. |
| `:12` | "Also: **this lane's own corpus and gates**." | A gate on this lane's own corpus is explicitly owned. |
| `:37-38` | "…this lane's runner, **corpus and source registry (`corpus/SOURCES.md`)**." | **Decisive.** The surface the guard protects is named Core. It decides tameshi's adoption map *into tameshi's registry*; it governs nothing of another lane's. |
| `:14-17` | "**Refuses:** product domains — every lane's gate remains its own; tameshi owns only the reusable craft (**a pattern is admitted from evidence in TWO independent lanes before it is claimed general**). Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)." | The limit: no general/fleet claim, no sibling gate edit. |
| `:20` | "**Out of province → report, never absorb.**" | The disclosure rule (§6). |
| `:40-42` | "**Frontier** — F1–F10 … ground moves to Core only through an admitted, source-headed `knowledge/` entry whose `source:` cites a `mined` `SOURCES.md` row." | C3 is declared a **capability** (`SCORECARD.md:2074`, AXES.md §Capabilities), and no frontier item names registry adoption (`corpus/README.md:68-104`, F1–F10). So no knowledge entry and no Core move are owed — and none may be implied. |
| `:44-45` | "**Adjacent** — report, never absorb: every sibling gate's code and product clauses (owner lane)…" | Names the class of thing kengaku's gate is; forbids absorbing it. |

## 2. Why not chousa

`chousa-shokunin/PROVINCE.md:3` — "**Domain:** deep-research method (調査) — the reusable
craft of source research." `:5-8` — "**Owns:** question framing; source hierarchy (primary /
secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source
verification; search-strategy taxonomy; the external-target approval table for a research
window; **this lane's own corpus and gates**." `:10-15` — Refuses five domains; no registry,
id-allocation or curation clause appears anywhere.

The roster record agrees: `MANIFEST.json` mints chousa with the rationale "the general
source-research method is unowned" (`grep -n chousa MANIFEST.json` → `:2312-2314`).
**"Chousa (registry curation)" is not a role that exists** — chousa's corpus ownership
(`:8`) is the same per-lane shape as tameshi's (`:12`), not a fleet curation service. A
registry guard is not a research-method artefact.

## 3. Why not kumitate

`kumitate-shokunin/PROVINCE.md:3` — "**Domain:** orchestration & tooling — scopes OMP
task/hub, ufo-fsd scripts & runtime"; `:6` — "**Refuses:** anything outside this domain";
`:12-15` — Core governs the origin script layer, the origin runtime layer, the Kimi Code
substrate, and "**The lane's own** instruments `scripts/*.mjs` … and **its** learning
registry `corpus/SOURCES.md`". "Tooling" there is scoped to the ufo-fsd script/runtime
surface; a `tameshi-shokunin/tools/*.py` file is not in it, and tameshi already carries
in-tree instruments as Core (`PROVINCE.md:37` "this lane's runner"; `SCORECARD.md:241`
`tools/mutate-and-run.sh`; round-21 append `tools/env-diff.py`; round-25 append
`tools/mte-interop.py`). A new `tools/` instrument is the lane's established shape.

## 4. Who actually owns the registry contract (the thing C3 must not absorb)

- `PROTOCOL.md:398` — "a child lane's *registry home* is its own `SKILL.md`."
- `PROTOCOL.md:435` — "`corpus/SOURCES.md` | … contract v1, defined once in `CORPUS.md` …
  append-only per the contract; … the frozen contract `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`
  **is the authority**".
- `CORPUS.md:89` — "`id` — `S` + 3 or more digits, the next unused; **never reused**."
- `CORPUS.md:152` — "The maintained `scripts/sources-census.sh` CLI accepts **0–3 leading
  ASCII spaces** before Markdown table rows…" (the anchor the guard's extractor mirrors).

⇒ rule = fleet doctrine; instance = per-lane; census = the authority. The guard is in
province exactly as *an enforcer of published doctrine on tameshi's own registry*, and out
of province the moment it is described as the registry's authority or as a fleet tool.

**Precedent that settles the shape** — `kengaku-shokunin/PROVINCE.md:224-228` — "**Operability
addition:** `plans/sources_adopt.py` — a pre-append gate for registry adoption (id collisions
under the census's own 0–3-space anchor, staged-row schema, prose-`recheck` normalization,
`used-by` projection) with a ten-case selftest — and `plans/adoption_check.py` … **Both are
lane-local and compose with the fleet census, which remains the registry's authority;
neither replaces it.**"

**The staging repo's own invariant** — `shokuknow/README.md:6-7`: "**Nothing here is
authoritative fleet state.** The lane repos own their corpora; this campaign produces
adoption-ready packages that **a lane's own gate** passes before anything lands." `:251-257`:
"This campaign never writes into a lane repo… The campaign stages material; the lane's own
gate adopts it." Reading the package is a read-only probe, permitted by `PROVINCE.md:16-17`.

## 5. Boundary conditions — in province **iff** all four hold

1. **Surface.** The guard's only governing surface is `corpus/SOURCES.md`; it never writes
   to shokuknow or to another lane. Evidence:
   `grep -n "shokuknow\|/home/vgpnk" tools/staged-id-guard.py` → no match (exit 1); the
   tool's only file open is a read (`:423` `open(path, encoding='utf-8')`); the package path
   appears only in the counter (`guard/measure.py:6,56,145`) and is read with `read_bytes`.
2. **Claim.** Lane-local capability, not a general pattern. `SCORECARD.md:2074`: "which ids
   of a staged registry package collide with **the lane registry**". No knowledge entry:
   `grep -rln "staged-id-guard" corpus/knowledge/` → no output (exit 1); `corpus/README.md:544-549`
   Round 43 lists only `r43-survivor-resolution-rule.md`.
3. **Authority.** The guard composes with the census and never replaces it
   (`PROTOCOL.md:435`; kengaku's `:227-228` form). **Current record state: no round-43
   text says this** — see §7 finding 2.
4. **No sibling edit.** Stdlib-only (`grep -n "^import\|^from" tools/staged-id-guard.py` →
   argparse, hashlib, json, os, re, sys); the round's tool set is lane-local
   (contract `frozen_tools`: `tools/write-path-census-v4.py`, `tools/staged-id-guard.py`).

## 6. Required disclosures for the round-43 report

The item asks this "if out of province". Under the in-province verdict the report still
owes D1–D5 (no record states the boundary today); under a flipped verdict it owes D1–D6.

- **D1 — scope + authority.** "`tools/staged-id-guard.py` is lane-local: it decides the
  adoption map for this lane's `corpus/SOURCES.md`. The registry contract remains the fleet
  census's authority (`scripts/sources-census.sh`; `PROTOCOL.md:435`; `CORPUS.md:89,152`);
  the guard composes with it and never replaces it." Cite `kengaku-shokunin/PROVINCE.md:224-228`
  as precedent wording.
- **D2 — adjacency, named.** `kengaku-shokunin/plans/sources_adopt.py` is an independent
  same-class pre-append registry adoption gate (kengaku `PROVINCE.md:224-228`; the tool's
  docstring `sources_adopt.py:1-25` states the same gap: the fleet census "validates a
  registry that already exists; nothing in the lane checked a row set *before* it was
  appended"). tameshi did not read or edit it, and claims neither novelty nor generality.
  `PROVINCE.md:14-16`'s two-lane evidence bar is met **in form** (two lanes, two
  implementations) — but the two arose the same day under the same campaign pressure, so
  "independent" is the L1's judgment call, and a general claim would still need an
  admitted, source-headed `knowledge/` entry citing a mined row (`PROVINCE.md:40-42`).
  Absent that, the row stays a lane capability.
- **D3 — recommendation that travels, not absorbed.** kengaku's gate *refuses* a non-empty
  collision set (`sources_adopt.py:11-14`, capability 4), while tameshi's *resolves* it by
  document (held rows dedupe to their registry id; fresh documents take ids at/above the
  safe floor) and refuses only its own arithmetic map's cascade. The by-document resolution
  is the delta worth carrying to that gate's owner in the report; tameshi does not patch it.
- **D4 — staging invariant.** The package is the campaign's, not authoritative fleet state
  (`shokuknow/README.md:6-7,251-257`). The guard reads it read-only; the campaign-side
  recommendation is that a next package allocate ids above each lane's registry maximum
  (round-43 live set: 7 collisions `S153`–`S159`, 3 held → `S105`/`S106`/`S155`,
  `corpus/lessons/round-43.md:74-86`). Do **not** describe the guard as ruling on the
  package's ids; that is the campaign's allocation, not the lane's.
- **D5 — what must not appear.** No sentence calling the guard a fleet/registry authority,
  a "registry curation" tool, or a capability of another lane. And **no `PROVINCE.md`
  append for C3**: `grep -n "^## " PROVINCE.md` ends at the round-26 append; a capability
  belongs in the SCORECARD capability table (AXES.md §Capabilities), not in PROVINCE.
- **D6 — only if §5 (1), (2) or (3) breaks.** Then the verdict is **out of province** and
  the report must carry an explicit "recommendation only" block naming the owner (the
  census/contract side for authority; kengaku for its own gate; the campaign for its
  package ids) and stating that no tameshi measurement counts toward that owner's gate.

## 7. Findings (severity ordered)

- **LOW — generic operative wording.** `tools/staged-id-guard.py:2`: "Pre-adoption id guard
  for a staged SOURCES registry package." No lane qualifier, so a cold reader can take it as
  a fleet tool; `:4-9` does cite fleet doctrine correctly. **Recommendation for round 44**
  (the pin is frozen — contract `frozen_tools["tools/staged-id-guard.py"]`; editing now
  moves `tool_sha_ok`): add "for this lane's registry (`corpus/SOURCES.md`)" and one
  sentence that the census remains the authority. Reproduce: `sed -n '1,12p'
  tools/staged-id-guard.py`.
- **LOW — disclosure gap.** No round-43 record states the authority/composition boundary:
  the closest is `SCORECARD.md:2081` (`sources-registry` row, "census-gated", pointing at
  the external `sources-census.sh` run); `grep -niE "authority|compos|replace.*census"
  corpus/lessons/round-43.md` returns nothing for the guard (the `lessons` text stops at
  the collision report, `:74-86`). The only place the boundary would be stated is this
  seat report. Add D1 at the C3 section.
- **INFO — premise correction (the alternatives are not both real homes).** (a) No lane
  owns registry curation: chousa `:3-8` has no such clause and its mint record names source
  research; kumitate `:3-15` scopes tooling to ufo-fsd scripts/runtime and refuses anything
  outside. (b) The registry contract authority is already fixed fleet-side
  (`PROTOCOL.md:435`), so the real question is "lane gate vs contract authority", not
  "tameshi vs chousa vs kumitate". Reproduce: `sed -n '3,8p' ../chousa-shokunin/PROVINCE.md;
  sed -n '3,15p' ../kumitate-shokunin/PROVINCE.md; sed -n '398p;435p' ../PROTOCOL.md`.
- **INFO — affirmative: the records do not overclaim.** `SCORECARD.md:2074` says "the lane
  registry"; the contract C3 statement names no authority; `corpus/lessons/round-43.md:74-86`
  reports the collisions and the by-document map as an adoption decision, not as a rule for
  the package. Nothing in the records needs withdrawal.

## 8. Reproducible commands used

```
cat -n PROVINCE.md | sed -n '1,50p'                     # §1 quotes and line numbers
sed -n '3,8p;10,15p' ../chousa-shokunin/PROVINCE.md     # §2
sed -n '3,15p' ../kumitate-shokunin/PROVINCE.md         # §3
sed -n '398p;435p' ../PROTOCOL.md                       # §4 registry home + authority
sed -n '84,92p;148,155p' ../CORPUS.md                   # §4 id never reused; 0-3-space anchor
sed -n '224,228p' ../kengaku-shokunin/PROVINCE.md       # §4 precedent wording
sed -n '6,7p;251,257p' ../shokuknow/README.md           # §4 staging invariant
grep -n shokuknow tools/staged-id-guard.py              # §5.1 no match (exit 1)
grep -n "open(\|write" tools/staged-id-guard.py         # §5.1 one read open (:423)
grep -rln staged-id-guard corpus/knowledge/             # §5.2 no match (exit 1)
sed -n '544,549p' corpus/README.md                      # §5.2 round-43 notes table
sed -n '2074p' SCORECARD.md                             # §5.2 lane scope
sed -n '68,104p' corpus/README.md                       # §1 F1-F10, no registry item
grep -n "^## " PROVINCE.md                              # D5 no round-43 append
sed -n '74,86p' corpus/lessons/round-43.md              # D4 live collision set
sed -n '1,25p' ../kengaku-shokunin/plans/sources_adopt.py  # D2/D3 same-class gate
```

## 9. Residual risk / not verified

- **No counter was run** (bounds; none answers province fit). The counters' own claims are
  other seats' targets.
- I read kengaku's gate only at `PROVINCE.md:224-228` and `plans/sources_adopt.py:1-25`;
  "independent same-class" rests on those two records, not on an audit of its behaviour.
  That is enough for adjacency, not enough for D3's delta to be a defect claim.
- "Independent lanes" in `PROVINCE.md:14-16` is a judgment, not a check I can execute; both
  gates appeared on 2026-10-25 under the same campaign pressure, so a conservative reader
  may hold the general pattern open even though the sentence's form is satisfied.
- I did not verify that tameshi's `SKILL.md` carries the registry section `PROTOCOL.md:398`
  calls the registry home; it does not affect the province verdict, but it is the per-lane
  ownership cite if a later round argues the registry is fleet-owned.
- Campaign-side id allocation (D4) is out of tameshi's province to rule; I did not verify
  how shokuknow allocates ids.
