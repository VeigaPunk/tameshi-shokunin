# ProvinceBox4 — SHONEN box 4: "No cross-domain bleed (PROVINCE.md still accurate)"

Seat: ProvinceBox4 · round 16 (hyaku phase 2), wave 1 · 2026-10-20
Target: read `PROVINCE.md` (47 lines) and verify each Core/Adjacent statement
against the repo; name the exact append-only Core line needed after the seventh
leg `js-round-gate` lands. Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
No lane file was written except this report. No tool installed. No test/mutant
run (leaf seat, wave 1).

## Snapshot state (the worktree moved during the audit)

- Lane HEAD at first read: `28aeef4` ("round-15 verifier spot-check").
- First `git status --porcelain | head -50` showed 3 entries and **no** `M tools/mutate-and-run.sh`.
- Re-check at 10:28 (`git status --porcelain=v1`): `A .ufo/evidence/round-16/coldread/SKILL.snapshot.md`,
  `M tools/mutate-and-run.sh`, `?? .ufo/evidence/round-16/census-start.txt`,
  `?? .ufo/waves/round-16/`. The tool mtime was `2026-10-20 10:26`; `git diff --stat`
  said `tools/mutate-and-run.sh | 72 +-`. **The seventh-leg edit was in flight and
  uncommitted.**
- Final check at `2026-10-20T13:31:40Z`: `git status` no longer lists the tool,
  `git diff --stat -- tools/mutate-and-run.sh` is empty (exit 0, no output), and
  `nl -ba` shows the six legs back at **84-89** with `# Sources:` at 90. The
  in-flight edit was **reverted** at tool mtime `10:27:31 -0300`, so the landing
  shape below is evidence of what leg 7 does to the numbering, not the landed
  file. Every anchor is given for all three observed states; the append must use
  the range measured after the real landing.

## Method — commands run, exit, key output

| command | exit | key output |
|---|---|---|
| `nl -ba PROVINCE.md` | 0 | 47 lines; Core at 28-38, Frontier 40-42, Adjacent 44-47 |
| `git show HEAD:tools/mutate-and-run.sh \| nl -ba \| sed -n '80,91p'` | 0 | six leg lines at **84-89** (js-kimi-census … js-claims-check); header line 80 "r10-2 six legs" |
| `nl -ba tools/mutate-and-run.sh \| sed -n '78,100p'` (10:26-10:28 only; **since reverted**) | 0 | header line 81 "…r10-2 six legs; **r16 seven**"; leg lines at **85-90**; `js-round-gate` at **91**: `kumitate-shokunin/scripts/round-gate.mjs    @@RG_KILLED@@/10 (@@RG_PCT@@ %)` |
| command D (`SCORECARD.md:73` regex) on HEAD, the observed edit, and the reverted worktree | 0 | all `recorded_cases=6 depth_score=6` — the placeholder rate was not `\d+/\d+`, so the leg was never counted |
| `git -C kumitate-shokunin cat-file -e 364f1d59…` | 0 | revision exists |
| `git -C kumitate-shokunin show 364f1d59…:scripts/round-gate.mjs \| sha256sum` | 0 | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  -` (matches C1's pin) |
| `… \| wc -l` | 0 | `1511` |
| `git -C kumitate-shokunin show HEAD:scripts/round-gate.mjs \| sha256sum` | 0 | same `f890e277…d3e9` — the pin **is** the current kumitate HEAD blob; no drift to re-pin |
| `git -C kumitate-shokunin log -1 364f1d59…` | 0 | `round-24: … round-gate (60/60)` (2026-10-13 22:49:20) |
| `for f in kumitate-shokunin/scripts/*.mjs; do grep -c -- --selftest "$f"; done` | 0 | **7** files, each with `--selftest` (cite-check 12, claims-check 8, kimi-census 4, proxy-check 18, round-gate 12, **sources-check 4**, surface-probe 13) |
| `grep -c '^\| .* \| gate \|' kumitate-shokunin/SKILL.md` | 0 | **7** gate registry rows, `SKILL.md:599-605`, incl. `sources-check … independent gate … --selftest` (605) |
| `git -C kumitate-shokunin log -1 1a8eed5` | 0 | `2026-10-19 19:41:02 -0300 round-34: sources-registry gate …` |
| `git -C tameshi-shokunin log -1 c7986cd` | 0 | `2026-10-19 19:15:33 -0300 round-1: close fleet round 1 …` (the PROVINCE append) |
| `git -C kumitate-shokunin ls-tree --name-only 72d9ccd scripts/ \| wc -l` | 0 | `6` (last kumitate commit before the append) |
| `diff <(git show 40f8e1f:PROVINCE.md \| sed -n '1,20p') <(sed -n '1,20p' PROVINCE.md)` | 0 | silent → `LINES-1-20-IDENTICAL` |
| `grep -n "self-service\|service\*\*" corpus/knowledge/service-optin-protocol.md` | 0 | `:36` self-service → **tsukuroi r5**; `:37` service → **mado r6**; `:222` "tsukuroi r5 — self-service \| mado r6 — service" |
| `sed -n '38,50p' SCORECARD.md` | 0 | `:46` tameshi r4 = tsukuroi 6/10; `:47` tameshi r5 = first service engagement (mado 4/10) |
| `grep -n "^| F1 \|^| F10 " corpus/README.md` | 0 | `:78` F1 … `:87` F10 (all F1-F10 present) |
| `sed -n '68,76p' corpus/README.md` | 0 | `:72-75` "A ground moves to `held` only through an admitted `knowledge/` entry with a `source:` header citing a `mined` `SOURCES.md` row." |
| `grep -n "\| S030 \|" corpus/SOURCES.md` | 0 | `:41` S030 … `REJECTED: … an adjacent UI domain to report, not absorb` … status `rejected` |
| `grep -n "^\*\*Domain" kagi-shokunin/PROVINCE.md kama-shokunin/PROVINCE.md` | 0 | kagi `:3` "secrets & vault ops — … credential hygiene"; kama `:3` "local model serving & endpoint health" |
| `ls -d kimi-shokunin` (fleet root) | **2** | `ls: cannot access 'kimi-shokunin'`; actual template `/home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md` (`nl`: `## Core` at 6, `## Frontier` at 11, `## Adjacent` at 16) |
| `grep -n '"game-dev-2d"\|"verifier": "AGREE' .ufo/waves/shokunin-train-20261014-w7/closeout.json` | 0 | `:14` game-dev-2d, `:19` `"verifier": "AGREE 5/5"`; `:23`/`:28` game-dev-3d likewise |
| `grep -n "fleet trees are never written" tools/mutate-and-run.sh` | 0 | `:108` "…the fleet trees are never written." (read-only mechanism) |
| `for r in kumitate kagi tsukuroi mado kaidoku; do git -C $r-shokunin status --porcelain \| wc -l; done` | 0 | `kumitate 0, kagi 0, tsukuroi 0, mado 0, kaidoku 1` — observed at the check only; kaidoku's one entry is its owner's, not attributed here |

Not executed (and therefore not claimed): `node round-gate.mjs --selftest`
60/60 — leaf seat, no test runs. Corroboration only: the pinned commit message
records "round-gate (60/60)" and `corpus/knowledge/fleet-suite-census.md:49`
records 60 executed cases for round-gate on 2026-10-14.

## Findings, by severity

### F1 — REQUIRED when leg 7 lands: the Core count and the tool anchor

`PROVINCE.md:29-33` currently reads "the **six** recorded mutation legs' gates …
(`tools/mutate-and-run.sh:84-89`…)". At committed HEAD this is **true**: six leg
lines sit at 84-89. It becomes **false** the moment `js-round-gate` lands:

- The observed in-flight edit (10:26-10:28, since reverted) added `js-round-gate`
  at worktree line 91 and moved the leg block to **85-91** (one line was inserted
  at line 14-15, shifting the header). In that state `PROVINCE.md:33`'s `:84-89`
  spanned `# expectation:` + five of the six old legs (kimi…checklist), missing
  `js-claims-check` (90) and `js-round-gate` (91). The current worktree is back
  to six legs at 84-89, so the drift will recur when the leg is re-landed.
- The leg is not yet "landed" in the counted sense: in the observed edit the rate
  was `@@RG_KILLED@@/10 (@@RG_PCT@@ %)`, and command D (`SCORECARD.md:73`) read
  `recorded_cases=6 depth_score=6` on both HEAD and that edit; it will read 7
  only once the land carries a numeric rate.
- Gate facts are solid and already match C1: rev `364f1d59…` exists; blob sha256
  `f890e277…d3e9`; 1511 lines; **the same blob is kumitate HEAD**, so the pin is
  drift-immune today.

**The exact append-only Core line needed (verbatim, append after line 47; do not
edit 1-47):**

```markdown
## Core amendment — seventh recorded mutation leg (round 16, appended 2026-10-20)

**Core** — the recorded mutation legs are seven, not six. The seventh is
kumitate `scripts/round-gate.mjs` (git rev
`364f1d5954158ef8844bca4a5fef57b05d2f2ca5`, blob sha256
`f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`; hermetic
`node round-gate.mjs --selftest`), entered as ledger leg `js-round-gate` in
`tools/mutate-and-run.sh`'s `--regression` leg list. `:84-89` is the round-1
six-leg anchor and stays the historical record; the landed seven-leg list is
`tools/mutate-and-run.sh:85-91` (leg line 91 in the observed 2026-10-20 landing
shape — re-measure at paste). Lines 1-47 above are unchanged (they are cited by
line across the lane).
```

Before pasting, re-measure the two numbers against the final landed file:
`grep -n '^#   js-round-gate' tools/mutate-and-run.sh` — expect
`91:#   js-round-gate …` — and `nl -ba tools/mutate-and-run.sh | sed -n '85,91p'`
— expect the seven leg lines. If either differs, substitute the measured range
in both places; do not paste the observed range as if it were measured on the
landed file. (Observed 2026-10-20: the edit's first hunk added one header line,
so the six-leg block moved 84-89 → 85-90 and the seventh line landed at 91.)

### F2 — currently inaccurate (minor): `PROVINCE.md:8` says six gates; kumitate now has seven

`PROVINCE.md:7-9` — "`kumitate-shokunin/scripts/*` (**six** gates with selftest
suites + mutation controls)". The wildcard now matches **seven** `.mjs` files,
all `--selftest`-bearing, and kumitate's own gate registry lists seven rows
(`kumitate-shokunin/SKILL.md:599-605`, `sources-check` at 605). Timeline:
this lane's append `c7986cd` is 2026-10-19 **19:15:33 -0300**; kumitate round-34
commit `1a8eed5` (sources-check) is **19:41:02 -0300** — 25 minutes later; at
`72d9ccd` (11:59, last kumitate commit before the append) `scripts/` held
exactly 6 entries. The count was true when written and has been false since
19:41.

### F3 — currently inaccurate (minor): `PROVINCE.md:35` calls both entries "service runs"

"the tsukuroi and mado gates entered through the round-5/6 **service** runs".
`corpus/knowledge/service-optin-protocol.md:36` records tsukuroi r5 as
**self-service** ("the opting-in lane, on /tmp copies"); only `:37` mado r6 is
**service**; §5 `:222` repeats "tsukuroi r5 — self-service | mado r6 — service".
Separately, the round numbers are the sibling lanes' (`tsukuroi` plan r5, mado
plan r6): this lane's own move log enters them in tameshi r4 and r5
(`SCORECARD.md:46-47`). Only mado's engagement was a tameshi service run.

### F4 — currently unresolvable (minor): `PROVINCE.md:26` canonical-template path

`` `kimi-shokunin/templates/mint/PROVINCE.md:6-19` `` does not resolve from the
lane root or the fleet root (`ls -d kimi-shokunin` → exit 2; no such directory).
The file is `/home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md`, and
its lines 6-19 do hold `## Core` / `## Frontier` / `## Adjacent` — the shape
claim is right, the relative path is wrong. Other lanes cite it host-absolute or
`~/Projects/…` (e.g. `mori-shokunin/.ufo/waves/round-13/build/ReviewPromotion.md:14`).

### F5 — wording ambiguity (minor): `PROVINCE.md:8` "mutation controls"

Read distributively ("six gates each having mutation controls") the phrase is
false: `corpus/knowledge/fleet-suite-census.md:56` records **in-suite mutation
controls 1 of 6**, and `corpus/knowledge/gates-survey-kumitate.md:308-311`
explicitly says the arm-coverage meta-checks are "**not** mutation controls".
The phrase should be read as "six gates [that have selftest suites] plus the
mutation controls [tameshi applies]"; if the parenthetical is ever restated, say
that outright. No count change is needed beyond F2.

## Statement-by-statement audit

| PROVINCE.md | statement | verdict | evidence |
|---|---|---|---|
| 3-5 | domain = verification-fixture craft (hermetic suites, mutation, fail-closed arms, verdict lines, no-permissiveness, before/after proof) | verified-record | `README.md:5` "**Domain:** verification-fixture craft"; `SKILL.md:1-6` front matter + opening |
| 7-8 | Owns `kumitate-shokunin/scripts/*` (six gates…) | **inaccurate (F2/F5)** | 7 `.mjs`, all `--selftest`; `kumitate-shokunin/SKILL.md:599-605` |
| 9 | kagi `corpus/*check*.sh` + census gates | verified-record | `kagi-shokunin/corpus/checklist-run.sh` (matches `*check*.sh`), `surface-census.sh`, `sources-census.sh` all present |
| 10-11 | kaidoku audit-lane pattern (verify: lines, bit-exact evidence ids) | verified-record | 550 `verify:` lines in kaidoku `*.md`; `kaidoku-shokunin/SKILL.md:436` "evidence id X"; `kaidoku-shokunin/corpus/knowledge/2026-10-14-r14-02-final-sweep.md:176` "bit-exact" |
| 11 | game lanes' verifier-AGREE loops (fleet root `.ufo/waves/`) | verified-record | `game-dev-2d-shokunin/reports/round-61/r61-verifier.md:15,35,62,81`; fleet `.ufo/waves/shokunin-train-20261014-w7/closeout.json:14,19` (game-dev-2d, "AGREE 5/5"), `:23,28` (game-dev-3d) |
| 12 | also this lane's own corpus and gates | verified-record | `tools/`, `corpus/` present; `tools/mutate-and-run.sh` is the lane's runner |
| 14-17 | refuses product domains; two-lane generality bar; never edits a sibling gate | verified-record (rule + mechanism) | `PROVINCE.md:15-16` repeated at `SKILL.md:763`; runner materializes legs via `git show` and `tools/mutate-and-run.sh:108` "the fleet trees are never written" |
| 18 | credential material → kagi; endpoint health → kama | verified-record | `kagi-shokunin/PROVINCE.md:3`; `kama-shokunin/PROVINCE.md:3` ("local model serving & endpoint health"), kama Refuses "credential material & auth flows (kagi)" |
| 20 | out of province → report, never absorb | verified-record (rule) | `PROVINCE.md:20`; cited by `corpus/knowledge/verification-patterns-fleet.md:65` |
| 22 | fleet round 1, appended 2026-10-19 | verified-record | `git -C tameshi-shokunin log -1 c7986cd` → 2026-10-19 19:15:33 |
| 24-25 | lines 1-20 unchanged, cited by line | verified-record | `diff` vs `40f8e1f:PROVINCE.md` lines 1-20 → silent |
| 26 | canonical shape `kimi-shokunin/templates/mint/PROVINCE.md:6-19` | **inaccurate (F4)** | path absent at fleet/lane root; actual file is `/home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md`; shape match at 6/11/16 |
| 28-29 | Core = method + six recorded legs' gates | **stale on count (F1)** | HEAD true (6 legs, 84-89); the observed 10:26-10:28 edit had 7 legs at 85-91 (leg line 91 placeholder), now reverted |
| 30-33 | gate list + `tools/mutate-and-run.sh:84-89` | verified at HEAD; **anchor stale in the observed edit (F1)** | HEAD legs 84-89; in the observed edit `:84-89` = expectation + 5 legs |
| 33-35 | Owns list names only kumitate, kagi, kaidoku, game lanes | verified-record | `PROVINCE.md:7-12` |
| 35 | tsukuroi and mado entered through round-5/6 service runs | **inaccurate (F3)** | protocol `:36-37`, `:222`; `SCORECARD.md:46-47` |
| 36-38 | mutation service + opt-in protocol; runner, corpus, `corpus/SOURCES.md` | verified-record | `corpus/knowledge/service-optin-protocol.md` present; `tools/mutate-and-run.sh`; `corpus/SOURCES.md` present |
| 40-42 | Frontier = F1–F10 in `corpus/README.md ## Frontier`; admission rule | verified-record | `corpus/README.md:68` heading, `:78` F1 … `:87` F10; rule at `:72-75` ("moves to `held`" = this file's "Core"; same gate) |
| 44-45 | every sibling gate's code and product clauses = owner lane | verified-record (rule) | `PROVINCE.md:14-17`; `kumitate-shokunin/PROVINCE.md:5` Refuses outside domain |
| 45-46 | credential (kagi), endpoint health (kama) | verified-record | as line 18 |
| 46 | visual/UI snapshot diffing = rejected row S030, adjacent UI lanes | verified-record | `corpus/SOURCES.md:41` status `rejected`, teaches "an adjacent UI domain to report, not absorb"; `mado-shokunin/PROVINCE.md:3` desktop/compositor |
| 46-47 | engine-specific nondeterminism = game lanes | verified-record (rule) | `game-dev-2d-shokunin`, `game-dev-3d-shokunin` exist; their verifier records show engine-shaped divergence maps (`closeout.json:14-30`), reported not absorbed |

No cross-domain **bleed** observed in the committed artifacts: the Core surfaces
are read-only, the runner replays sibling bytes from the git object store
(`tools/mutate-and-run.sh:99-108`), and no PROVINCE claim asserts ownership of a
sibling gate, credential or endpoint. The three inaccuracies above are staleness
of counts/paths/round labels, not absorbed domains.

## Recommended companions to the same append (optional, close F2–F4)

Append after the Core block, same append-only discipline; each leaves all
existing line numbers intact:

```markdown
**Owns (amended round 16, appended 2026-10-20).** `kumitate-shokunin/scripts/*`
now holds seven gates, not six: the round-5 census's six (`:8`) plus
`scripts/sources-check.mjs` (kumitate round 34, commit `1a8eed5`;
`kumitate-shokunin/SKILL.md:599-605` registers it as a gate with `--selftest`).
Lines 1-20 above are unchanged.
```

```markdown
**Core footnote (amended round 16, appended 2026-10-20).** The tsukuroi gate
entered through its own round-5 **self-service** run; only the mado gate
entered through tameshi's service engagement
(`corpus/knowledge/service-optin-protocol.md:36-37`, `:222`). `:35`'s
"round-5/6 service runs" is corrected here.
```

```markdown
**Shape citation (amended round 16, appended 2026-10-20).** The canonical
template cited at `:26` resolves on this host as
`/home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md:6-19`; the
repo-relative form does not resolve from the lane or fleet root.
```

## Residual risk / verification gaps

- **I did not execute** `node round-gate.mjs --selftest` (60/60 is the claim; leaf
  seat, no test runs) or any mutant. The sweep outcome and the leg's recorded
  rate are L1's to measure; F1's text deliberately carries no rate.
- **Anchor numbers are concurrency-sensitive.** The tool changed mid-audit; the
  final line numbers must be re-measured immediately before the PROVINCE paste
  (commands in F1). The permanent fix is name-first citation; the round-13
  connector already flagged this same brittleness
  (`.ufo/waves/round-13/w1/EvidenceConnector.md:61`).
- **SCORECARD also cites `:84-89`** (`SCORECARD.md:66`) and command D's regex
  will read 7 only after `@@RG_*@@` placeholders are replaced. That file is not
  mine to edit; flag for its owner in the same landing.
- Box 4 remains a **lane assertion** (no independent promotion verifier,
  `SHONEN.md:11-12`); this audit re-checks PROVINCE, not a historical no-bleed
  audit of sibling worktrees (the round-1 audit's own stated limit,
  `reports/round-1-calibration.md:186-193`).
- Sibling trees may carry their owners' concurrent work; I asserted nothing about
  their global cleanliness, only that this lane's mechanism never writes them.
- No secrets/credential surfaces were read; no `.omp` agent DB; no tool installs.

## Bounded recommendations

1. Land leg 7 with a numeric rate first; confirm command D prints
   `recorded_cases=7 depth_score=7`.
2. Then append the F1 block verbatim after line 47; verify
   `diff <(git show 28aeef4:PROVINCE.md | sed -n '1,47p') <(sed -n '1,47p' PROVINCE.md)`
   is silent.
3. Append the F2–F4 companions (one appended section is enough) so box 4's
   "PROVINCE.md still accurate" is true after the round, not only for the Core
   count.
4. Keep box 4 at `[~]` until those appends land; even then do not promote it to
   `[x]` from a lane-dispatched read — the mark's blocker is the independent
   verifier, not this evidence.
