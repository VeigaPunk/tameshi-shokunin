# S20 — operator teachings and round-17 carry-forward (round 18, wave 1)

Scope: (1) `corpus/lessons/operator-*.md` teachings, lane and fleet; (2) fleet-level
operator lessons in `/home/vgpnk/Projects/shokunin/.ufo/` and `MANIFEST.json` that apply
to tameshi but are absent from `corpus/QUALITY.md` / `SKILL.md`; (3) the round-17 open
debts and which the round-18 plan does not address.

Base: lane `183f87b899e6cae46be98d251cbc87fb5118f6ca` (round-17 closure), an ancestor of
current `master`/`origin/master` `93d22aa21a144a0e2833b1be74718d15060f002b`
(`git merge-base --is-ancestor 183f87b… master` → rc 0). Fleet helper read at `ae12f33`
(per S06/S15). This seat wrote only this report; no installs, no lane or sibling writes.

## 1. Operator teaching files — empty discovery

| Check | Command | Exit | Result |
|---|---|---|---|
| Lane lesson inventory | `ls /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons` | 0 | 15 files, all `round-*`; **no `operator-*.md`** |
| Lane pattern, any depth | `find /home/vgpnk/Projects/shokunin/tameshi-shokunin -name 'operator-*.md'` | 0 | empty |
| Lane git history, all refs | `git -C …/tameshi-shokunin log --all --oneline --name-only -- 'corpus/lessons/operator-*'` | 0 | empty |
| Fleet pattern | `find /home/vgpnk/Projects/shokunin -ipath '*corpus/lessons/operator-*' -not -path '*/worktrees/*'` | 0 | empty |
| Fleet history | `git -C /home/vgpnk/Projects/shokunin log --all --oneline --name-only -- '*corpus/lessons/operator-*'` | 0 | empty |
| Reflected in corpus? | `grep -c -i 'operator teaching' corpus/QUALITY.md SKILL.md` | 1 | `0` in each file |

The convention is `LEARNING.md:50-54`: an operator teaching lands verbatim as
`corpus/lessons/operator-<YYYY-MM-DD>-<slug>.md` and by the lane's next round must be
reflected in `QUALITY.md` or `SKILL.md` with the lesson cited. No such file exists here or
in any sibling, so no teaching is silently unreflected — the obligation is vacuous this
round. This reproduces the sibling precedents (`kama-shokunin/.ufo/waves/round-14/advice/
TeachingSweep.md` §2.2; `tsukuroi-shokunin/.ufo/waves/round-16/build/OperatorTeaching.md`).

The only fleet files matching `operator-*` are scope demands, not teachings:
`.ufo/scopes/shokunin-12h-20261014/operator-demand.md` and
`.ufo/scopes/souji-mint-20261018/operator-demand.md`.

## 2. Fleet-level operator records that apply to tameshi — reflection status

| # | Record and anchor | What it binds here | Reflected in QUALITY/SKILL? | Disposition |
|---|---|---|---|---|
| O1 | Operator amendments 2026-10-16: multi-claim cap 3, capabilities table, exploratory claims — `PROTOCOL-APPENDIX.md:48-50` | Claim shape and SCORECARD rows | Not QUALITY/SKILL; reflected in `SCORECARD.md:236,251,262,279` (Capabilities/Saturation/Planned/Retired) and the prompt | Correct home is AXES/SCORECARD; no action |
| O2 | Planner ruling 2026-10-19 — `.ufo/l0-questions.md:53` (L0 ANSWER, hyaku orchestrator) | L1 holds the planner seat; validator excludes planner | Dispatch only (prompt §3) | Not corpus material |
| O3 | Tooling authorization 2026-10-19 — `.ufo/prompts/tameshi-round-18.md:336-339`; wave context in `.ufo/waves/round-18/spec1.json` | Install/upgrade allowed; read RULES.md; record tool/version/channel/reason | **No**: `grep -c -E 'tooling directive\|RULES\.md\|install or upgrade\|uv tool\|~/.local/bin' corpus/QUALITY.md SKILL.md` → 0, rc 1 | Operational only. Installs were reported (`MANIFEST.json` r17 note: `ruff 0.17.1`, `vulture 2.16`); no durable rule in the lane |
| O4 | Pacman guard 2026-10-20 — `.ufo/prompts/tameshi-round-18.md:339-346`; recorded in `.ufo/l0-questions.md:54-55,57` | All pacman transactions paused; install only via `uv tool`/`npx`/official binary; no `-Sy/-Syu/-U/-R`, downgrade, service restart; dry-run rule when lifted | **No**: `grep -c -i pacman corpus/QUALITY.md SKILL.md` → 0, rc 1 | Honored operationally (`LOG.md:968`: “all pacman transactions became operator-paused”; `MANIFEST.json` r17 note: “No closure-seat installs”). If the pause outlives the campaign, it needs a durable home |
| O5 | jj as git manager 2026-10-20 — `.ufo/prompts/tameshi-round-18.md:293-294` | Lane commits only through `jj-lane.sh`; branch tip never bare HEAD | **Yes, partly**: `SKILL.md:1027-1035` (branch-tip reading rule), `SKILL.md:1818` (jj leaves Git HEAD detached); QUALITY draft 30 (B16) makes it a criterion | Reflected. The `SKILL.md:1029` line anchor and resolver are stale — see §4 item 5 |
| O6 | Live-lane git safety / sandbox clone 2026-10-20 — `.ufo/prompts/tameshi-round-18.md:320` | “A lane gate or selftest that runs git writes must run on a sandbox clone, never in the lane.” | **Partial**: QUALITY 27/28 require the `GIT_*` scrub and canary; `SKILL.md:1830` records the incident; `SKILL.md:1881-1883` clones for registry replay. Phrase `sandbox clone` → 0 hits in both files. QUALITY draft 36 (B16) states it prospectively | Addressed in-plan (criterion 36 + X09 canary + staged `bash-witness-study.py`) |
| O7 | Fleet safety boundary — `.ufo/scopes/shokunin-12h-20261014/operator-demand.md:7` (“do not change global configs”), `.ufo/scopes/souji-mint-20261018/operator-demand.md:27` (never operator config, credentials, host services, dirty/unpushed lane) | Seat write scope | **Partial**: `AGENTS.md:5` covers “Secrets are shape-only, never content-read”; QUALITY/SKILL never mention host services/global config | No round-18 criterion; low risk (lane tools touch neither) but no durable rule |
| O8 | Sibling lesson: host-install guard — `mado-shokunin/corpus/QUALITY.md:72-90` (criteria 20–21), `mado-shokunin/SKILL.md:458-497` (“Tool installs are not exempt from host safety”) | Same tooling authorization as O3; tameshi seats may install | **No**: no install/pacman text in tameshi QUALITY/SKILL (grep above) | Applicable fleet lesson from the libinput incident; not in the round-18 plan |
| O9 | Campaign mechanics 2026-10-20: 64–100 seats/wave, route table, no hardcoded model aliases, REA MCP disabled — `.ufo/prompts/tameshi-round-18.md:141-160,182`; wave context | Dispatch shape and host routing | Not corpus material; prompt §3 forbids hardcoded aliases. Lane hits for `m_*` are historical lessons/reports only (`corpus/lessons/round-1.md:226`, `round-15.md:91-93`, `round-17.md:63`) | Honored; nothing to reflect in QUALITY/SKILL |

`considerthese/2026-10-19.md` and `considerthese/2026-10-20.md` are GitHub reflections
(“proposals only, not acted on”), not operator teachings — same distinction the mado
round-17 report draws at `.ufo/reports/round-17/mado.md:46`. They create no
QUALITY/SKILL obligation.

## 3. Round-17 debt inventory vs the round-18 plan

Plan sources: `.ufo/waves/round-18/spec1.json` item prompts and
`.ufo/waves/round-18/assignments1.json` (73 seats), plus the staged files under
`.ufo/waves/round-18/staged/`. Landing state below is a snapshot at ~16:39 -03 while
wave 1 was still running; “planned” is not “landed”.

### 3.1 `round-17-verifier-spotcheck.md` §7 routed items

| Item (anchor) | Round-18 plan | Status |
|---|---|---|
| 1. R17-KNOW-EXIT / correction sweep — `:419-422` | B13 staged `corpus/knowledge/input-keyed-coldread-credit.md` (75 → 147 lines, +72: §5 exit sentence, `measure-*.json` narrowing, R17-CMD-BIND narrower claim); S07 report; B16 criterion 35 | Addressed; staged diff non-empty, earlier bytes prefix-identical |
| 2. R17-CMD-BIND / G5 — `:423-427` (assertion, argv binding or narrower claim, G7 pointer, 89-vs-94 tally) | S12 (K02 status), S13 (tally), B15 staged `corpus/lessons/round-17.md` (+10 lines: G5 overclaim, G7 hole 5→7, 89 is the W2 receipt vs final 94); B16 criterion 33; B13 §3 states the narrower claim | Addressed by the permitted **narrowing**; trace-argv-to-declared-command binding is deliberately **not implemented** |
| 3. R17-GUARD-COVERAGE — `:428-432` (seven surviving guard removals) | X03 `defect-probes.py` P01–P07; X04 `tools/trace-inputs.py`; X05 `registry-check.py`; X06 `evidence-disposition.py`; contracts B/C/D | Planned and in flight: `tools/trace-inputs.py` exists (37 123 B); `defect-probes.py` absent; `staged/tools/registry-check.py` absent; `staged/tools/evidence-disposition.py` still byte-identical to base (`f8f05c7…`, empty diff) |
| 4. R17-GIT-ENV — `:433-436` (bash-witness scrub; migration, not pinned-byte edit) | X07 staged `tools/bash-witness-study.py` (base `49e9e5e2…` matches the round-13 pin; staged `c0d14ed4…`, 157 diff-output lines); `.ufo/evidence/round-18/dispositions.json` exists (4 108 B); X09 canary; B16 criterion 32 | Addressed in plan; scrub staged |
| 5. R17-JJ-GUARDS — `:437-439` (G2/G3 vs HEAD) | X06 staged copy (contract D), P08 jj fixture; B16 criterion 30 | Planned; not yet landed (staged copy identical to base) |
| 6. R17-TIMEOUT — `:440-443` (NaN/Infinity, setsid escape; older confinement/scrub/successor debts) | X05 staged copy (contract C), P09/P10; S09 non-finite sweep, S10 timeout-escape sweep; B16 criterion 31 | Planned for `registry-check.py`; other tools’ findings are routed, not fixed. Confinement and successor sweep are **not** in the plan |
| 7. R17-CITATIONS / CORRECTION-MECHANICS — `:444-451` | B14 staged five corpus appends (four ER-jj + `operator-runbook.md` ER-R3/ER-jj2; all staged diffs are pure EOF appends, prefix `cmp` verified by S06 §4.1); S06 report; S16 report; S17 map; B16 criteria 34–35; B17 staged canonical `SHONEN.md` | **Partial**: see §4 items 5–8 for the sub-items with no staged owner |
| 8. R17-INCIDENT — `:452-456` | S15 report drafts the L0 question; X09 canary; B16 criterion 36; QUALITY 27/28 retained | Routing planned; the L0 append is the L1’s, the helper is fleet/operator-owned |

### 3.2 `round-17.md` “Open, named, not closed by prose” (`:87-96`)

| Debt | Plan | Status |
|---|---|---|
| Seven selftest survivors (G3 tag-object, G5 symlink-mode; registry detached-checkout, short-rev regex; trace O_RDWR, pycache prefix, execve) | §3.1 item 3 (P01–P07 + contracts B/C/D) | Addressed in plan |
| `registry-check` NaN/Infinity and setsid escape | §3.1 item 6 | Addressed in plan |
| `evidence-disposition` G2/G3 vs HEAD | §3.1 item 5 | Addressed in plan |
| Knowledge entry §5 missing-ledger exit 2 | §3.1 item 1 | Addressed; staged erratum |
| Duplicated sectionizer/path predicates across `measure`/`assemble` (`SimplifyNewTools`) | X08 creates round-18 copies by “changing only” ledger path, box-3 string, ignored inputs, `--carry`, trace receipts, `--explain` | **Not addressed** — duplication is copied forward |
| `bash-witness-study.py:337-341` GIT_* scrub | §3.1 item 4 | Addressed; staged |

### 3.3 Carried older debts, trend debts and cross-domain routing

| Debt (anchor) | Plan | Status |
|---|---|---|
| Older-leg environment scrub / confinement / successor-sweep (`spotcheck:440-443`; `MANIFEST.json` r17 note) | X07 fixes the named tool; S11/X09 sweep and evidence only | Environment scrub: partial. Confinement and successor sweep: **not addressed** |
| Freshness unchanged; external line anchors remain citation debt (`spotcheck:381`) | Citation corrections only (§3.1 item 7) | Partial (§4) |
| Coverage unchanged; F7 open (`spotcheck:380`; `corpus/README.md:84`) | No coverage claim or seat | **Not addressed** |
| mado old-runner prose; kaidoku `ConnFleetJjPractice.md:86-89`; fleet/operator recovery helper; seven dead W2 seats (`spotcheck:456-461`) | C03/C04 read-only sibling context; S15 drafts the L0 | Correctly not tameshi work; owners unchanged |

## 4. Carry-forward list — not addressed by the round-18 plan

1. **Sectionizer/path-predicate duplication** between round-18 `measure.py` and
   `coldread/assemble.py`. `round-17.md:95` names it; X08 copies both files with minimal
   changes and adds no simplifier. Debt survives.
2. **Confinement.** Untrusted mutants can still write outside their directory or reach
   the network (`SKILL.md:1785` says use `bwrap` when mutants are untrusted); no round-18
   item adds confinement or a confinement test.
3. **Successor mutation sweep / freshness.** `spotcheck:381` keeps freshness
   `unchanged`; no successor sweep is claimed or scheduled. The r16 carry stands.
4. **F7 per-leg reuse-decision frontier** (`corpus/README.md:84`, open; `spotcheck:380`
   coverage `unchanged`). No coverage work this round.
5. **`SKILL.md:1029` resolver, not just its anchor.** B14’s draft correction says cite
   `detect_branch()` by name. S06 measured that v2 `detect_branch` is init-scoped
   (`:115-126`) and returns nothing in a detached lane with no `origin/HEAD`; the
   resolver the rule needs is `jj-lane.sh state <repo>`, field `branch=` (`lane.branch` →
   `detect_branch` → single `master`/`main`). S06 §4.2 proposes the better append; the
   L1 has not staged any SKILL edit.
6. **`tools/pin-disposition.py` stale anchors** at `:42-43` and `:325` (both cite
   `detect_branch (:53-65)`; the `:325` docstring also mirrors the v1 ladder, not v2).
   S06 §4.3 proposes docstring repairs; no seat owns the file and no staged copy exists.
7. **`corpus/SOURCES.md` append-only correction for S060/S061.** S16 verified S060 is an
   explicit 16-syscall `-e trace=` list, not `%file` (and `-f` is §Tracing, not §General),
   and S061’s paragraph is ¶3, not ¶2. S16 supplies verbatim correction text for the
   SOURCES notes list; no staged SOURCES file or owning seat exists.
8. **Knowledge entry source line.** `input-keyed-coldread-credit.md:1` repeats the S060
   off-anchors (`%file`, §General `-f`); B13’s erratum covers §5 and the `measure-*.json`
   citation only, and S16 explicitly leaves this as “separate edit, not made here.”
9. **SOURCES footer “pure append” wording.** B16 criterion 35 makes it prospective; the
   historical 9-add/1-delete footer (`spotcheck:449`) is a reporting-discipline item,
   not a repair. No work item.
10. **Conditional sweep findings.** S08 routes further bare-`HEAD` sites, S09 further
    non-finite numeric inputs, S10 further timeout escapes, S11/X09 further unscrubbed git
    callers. The plan fixes only the named tools (`evidence-disposition`, `registry-check`,
    `bash-witness-study`); any additional instance the sweeps name becomes new debt.
11. **Command-binding capability** (K02 holes 1/2: trace `argv` bound to declared/required
    commands). The plan chooses §7 item 2’s narrower-claim branch and B16 criterion 33
    forbids calling input-keyed credit “command coverage”. The capability itself remains
    unimplemented; do not let round-18 prose re-widen the claim.
12. **Fleet/operator recovery helper.** S15 confirms `jj-lane.sh` has only
    `init|commit|push|state` and no HEAD/index restore subcommand; fleet `scripts/` has no
    such helper. S15 drafts an L0 line; the L1 must append it, and the helper remains
    fleet/operator scope. Until then the incident is preserved, not repaired by lane
    plumbing.
13. **Operator-directive reflection decisions (O3, O4, O7, O8).** No `operator-*.md`
    teaching exists, so LEARNING’s next-round reflection duty is not triggered. If the
    L1 wants a durable home, the minimal move is a SKILL tooling-safety subsection
    mirroring mado QUALITY 20–21 / SKILL 458–497, plus the pacman pause while it holds;
    current evidence is prompt/LOG-only.
14. **Cross-domain and external items** (not tameshi’s to edit): mado’s old-runner prose,
    kaidoku’s `ConnFleetJjPractice.md:86-89` staged-pin statement, the fleet recovery
    helper, the seven dead W2 seats (disclosed, not respawned), and PR #1 on
    `VeigaPunk/tameshi-shokunin` (open draft per `considerthese/2026-10-20.md`).

## 5. Limits

- Wave 1 was in flight at the snapshot: `defect-probes.py` and staged `registry-check.py`
  were absent and staged `evidence-disposition.py` was still identical to base. No
  landing verdict is implied.
- `git log --all` covers local and fetched remote refs only; an unfetched remote branch
  could carry an `operator-*.md` not seen here. No fetch was made.
- Whether the L1 installs the SKILL/SOURCES corrections (items 5–8) is a decision, not an
  observable yet.

Verdict: **holds** — no `corpus/lessons/operator-*.md` teaching exists in tameshi or the
fleet, so none is unreflected; four fleet operator directives and the mado install lesson
have no QUALITY/SKILL home, and the carry-forward list above names the round-17 debts
(sectionizer duplication, confinement, successor sweep/F7, `SKILL.md:1029` resolver,
`pin-disposition`/SOURCES citations, command binding) that the round-18 plan does not
address.
