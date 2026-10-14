# Service standing state — the boundary: what tameshi hands the fleet, what stays lane-owned (T10-3, round 10)

Written 2026-10-14 by lane T10-3 (tameshi round 10). Role: the boundary table of
the standing service — one row per artifact class, in both directions: what is
**fleet-visible** (committed, citable, re-derivable by a lane that did not run
the case) and what stays **lane-owned** (scratch, in-flight state, the
substrates themselves) — plus the **handoff conditions** that put something
across the line. It states the boundary; it adds no gate measurement, re-cuts no
rate, edits no record, and writes no sibling tree.

Anchors: **O** observation (command output / file:line, re-quoted measured cell)
· **I** inference · **U** unknown. Substrates read-only during this write; scratch
`/tmp/w10-t10-3/`; this note is the lane's only write. Line cites are this
write's revision of each file (§6 pins, measured 2026-10-14T20:52Z); a reader on
a differing revision re-resolves rather than trusts (`SKILL.md:1269-1270`).

## 0. What "fleet-visible" means here

Two directions, two different lines:

- **Per run (service mode).** An owner lane brings a gate; tameshi sweeps it
  read-only and hands back **one corpus note** plus recommendations. The line
  inside a run: all writes in lane scratch, and "the note is the only fleet file
  the run writes" (`SKILL.md:895-896`; `service-optin-protocol.md:92`,
  `:133-135`; `fleet-kill-rate-ledger.md:312`). Absorption stays owner-side
  (`PROVINCE.md:16-18`).
- **Standing.** The committed records are the fleet's receipts: the ledger is
  "one standing receipt instead of re-quoting"
  (`fleet-kill-rate-ledger.md:4-8`); the method page is the reproduction surface
  (the executor test re-ran the method from `SKILL.md` alone,
  `executor-test-sufficiency.md:3-9`); the protocol is the request/response
  contract.

**Visible by citation, not by index — measured [O].** No fleet-level document
indexes these artifacts: at this read the fleet root's `CORPUS.md`, `AXES.md`,
`LEARNING.md`, `LOG.md`, `PROTOCOL.md`, `README.md` name tameshi `0` times each;
the fleet `MANIFEST.json` carries tameshi's lane + per-round rows instead
(`tameshi` on 13 lines, `:1714-2129`). Cross-repo, measured mentions are
asymmetric: `tsukuroi-shokunin` 12 files · `mado-shokunin` 19 files vs
`kumitate-shokunin` 0 · `kagi-shokunin` 0 (`grep -rl tameshi <repo>
--exclude-dir=.git`, §4 SC3). [I] the citation appears where the owning lane
wrote it back, not merely where a sweep happened: kagi's r8 checklist run was
service-form and still left no mention in kagi's tree, while the two trees that
do mention tameshi are the two whose lanes recorded an acceptance/hardening
record. Fleet visibility is by direct citation of a committed
file, and the citation is one-way unless the owner writes it back — nothing in
this service pushes an artifact into a sibling lane.

## 1. Fleet-visible artifacts (the handed side)

| # | Artifact | Class | Written by | What makes it citable | What it is not |
|---|---|---|---|---|---|
| 1 | `SKILL.md` | method page | tameshi rounds | section + pinned sha; "a reader on a differing revision re-resolves" (`:1269-1270`) | not a receipt for a rate — it re-quotes the ledger's rows |
| 2 | `corpus/knowledge/mutation-case-*.md` (6 notes) | run report | the run's lane, one note per run | pins · pre-registered table · verbatim `evidence/<id>.out` rows · non-equivalence probes · restore proof · reproduce block (`SKILL.md:883-897`, `:954-963`) | recommendations only; owner-side acceptance/hardening is a separate owner file (`service-optin-protocol.md:93-95`) |
| 3 | `corpus/knowledge/fleet-kill-rate-ledger.md` | standing receipt | round lanes, append-only | one row per gate with composition + pin; cite the row, not the prose (`:4-8`, `:21-39`) | no measurement of its own ("adds no new gate measurement", `:5-8`); "it proves the instrument, not the gates" (`SKILL.md:993-997`) |
| 4 | `corpus/knowledge/service-optin-protocol.md` | contract | r7 lane | request shape (§1), guarantees (§2), owner-hardens (§3), report shape (§4) | not a schedule — the queue is "an offer, not a schedule" (`:26-30`) |
| 5 | `corpus/knowledge/service-limits.md` | refusal detail of record | r9 lane | one verbatim anchor per refusal row; intake precondition checked (`:172-194`) | the method page's table is the compact copy; a divergence is the finding, never smoothed (`SKILL.md:1246-1254`) |
| 6 | `corpus/knowledge/fleet-suite-census.md` + `gates-survey-*.md` | survey | rounds 1–5 lanes | pins + executed counters on the read bytes | a survey is not a sweep; its instrument pin can lag (census §5 re-pin debt, `fleet-kill-rate-ledger.md:282`) |
| 7 | `tools/mutate-and-run.sh` | instrument | tool owner (tameshi) | every run log carries its own `MUTATE_TOOL` sha; selftest + `--regression` receipts | never writes a target; the 4-vs-6 leg cut "stands with the tool owner" (`fleet-kill-rate-ledger.md:282`, `:350`) |
| 8 | `PROVINCE.md` / `AGENTS.md` | boundary rules | repo | the read-only-substrate rule, secrets shape-only, out-of-province → report | inherits nothing from sibling provinces (`PROVINCE.md:14-20`) |
| 9 | `corpus/README.md` coverage map | index | house review | a row naming the note and its sources | currently 9 rows covering **6 of 16** knowledge notes — 10 uncarried, this one included [O] (§4 SC3) |
| 10 | `LOG.md` / `SCORECARD.md` | house record | folded at lane review | one row per round with its axis + evidence | not the receipt — the receipts are 2/3 above |
| 11 | `plans/*.md`, `reports/*.md` | round documents, lane-scoped | the round's lanes / scribe / verifier | in-repo and citable cross-repo (the protocol cites owners' plans, `service-optin-protocol.md:36-38`; ER-4 cites sibling drafts, `fleet-kill-rate-ledger.md:356`) | not service material: a plan is the lane's own dispatch/anti-claim; a report is a verifier/auditor output; both may be in flight during the round |

Corpus state at this read: `corpus/knowledge/` = 16 notes; `corpus/lessons/`
empty [O] (§4 SC3).

## 2. Lane-owned (the withheld side)

| # | What | Where | The rule | Anchor |
|---|---|---|---|---|
| a | Round scratch + run evidence | `/tmp/w<N>-<lane>-*/` (incl. the run's `MUTATE_EVIDENCE` dir) | lane-scoped; "foreign scratch never removed"; the mado run kept exactly its own 8 of ≥37 foreign dirs | `service-optin-protocol.md:86-91`, `:105` |
| b | Default run/regression scratch | `mktemp -d /tmp/tameshi-r4-2-run\|regression.XXXXXX` | "removed on PASS unless `--keep`, kept on FAIL/SETUP, never removed when `--workdir` was given" | `tools/mutate-and-run.sh:105-107`, `:972-973` |
| c | In-flight / moving state | working-tree diffs on the owners' gates | `drift` is "a reading for ledger hygiene" — "a writer is on the gate; wait for the commit, then re-pin"; a tick reading "never carried as a standing claim" | `fleet-kill-rate-ledger.md:293`, `:362`; `SKILL.md:1188-1189` |
| d | The substrates | sibling gates + trees | read-only; "the service never edits, repairs or re-pins the gate; a needed change is a recommendation to the owner" | `SKILL.md:823-825`; `PROVINCE.md:16-18` |
| e | The live plane | sessions, services, host state | "never read: PATH-level stubs only, never the session" | `service-optin-protocol.md:129-132` |
| f | Secrets / session material | vault refs, tokens, `op.env` | shape-only, never content-read; out of province → report, never absorb | `SKILL.md:21`; `PROVINCE.md:20` |
| g | Drafts | round record drafts, dispatch notes | the scribe's/lane's working document; landed bytes are the authority once committed | `fleet-kill-rate-ledger.md:356`; write-scope precedent `:17-19` |

## 3. The handoff conditions

A handoff is not a file move: it is the set of conditions under which a claim
becomes citable. Grouped by which line it crosses; every item carries its anchor.

### A. A gate crosses in (service intake)

1. **A pinned revision** — committed bytes with sha256 · size · lines · mtime
   and a porcelain-clean sibling tree at open; "a moved substrate needs a re-pin,
   never a re-interpretation of the old table" (`SKILL.md:808-812`;
   `service-optin-protocol.md:59-62`).
2. **A one-command hermetic suite** invocable against a copy — it must exercise
   the copy, print its own executed count and verdict, and read no live path
   (`SKILL.md:813-817`).
3. **A clause-mapped single-edit spec** with pre-registered expectations; every
   `@old` unique "asserted **before any suite run**", `@new == @old` refused; a
   red control exits 2 — no headline (`SKILL.md:818-825`, `:838-844`).
4. **Nothing else** — and the write boundary that comes with it: all writes in
   lane scratch, the note is the only fleet file
   (`SKILL.md:823-825`, `:895-896`; `service-optin-protocol.md:92`).

### B. A result crosses out (the run's product)

5. **The report shape** — pins, the kill-rate table verbatim from
   `evidence/<id>.out`, survivor non-equivalence probes, `MUTATE_RESTORE: OK`
   plus the tree-clean check, recommendation + named unknowns
   (`SKILL.md:883-897`; `service-optin-protocol.md:182-197`).
6. **Restore + tree-clean, the provable negative** — "the service's writes never
   touched the gate"; not the positive claim that the bytes were stable
   (`SKILL.md:864-866`; `service-optin-protocol.md:114-124`). A mid-run move by
   the owner is an incident recorded with both pins, not smoothed
   (`mutation-case-tsukuroi-census.md:9-35`).
7. **Recommendations-only** — absorption stays with the owner; "no acceptance
   means the recommendation is recorded unabsorbed" (`SKILL.md:872-874`;
   `service-optin-protocol.md:142-180`).

### C. A result enters the standing record (becoming quotable)

8. **Appended, never edited in place.** The outcome "lands **as an appended row
   or errata block in this ledger** — never as an edit of §1–§4"; both revisions
   stay in the record on a move (`fleet-kill-rate-ledger.md:312`, `:34-36`).
9. **The contribution contract, to become a leg** — pinned file set + revision +
   sha; defect spec; hermetic suite; recorded verdict table, "exact for ledger
   legs" (`SKILL.md:954-963`). The ledger proves the instrument, not the gates
   (`SKILL.md:993-997`).
10. **Receipt discipline** — "read the block, not the last line"; cite
    `REGRESSION_TOOL` + per-leg `REGRESSION_PIN`; FAIL names its rows; SETUP is
    not a verdict (`SKILL.md:965-992`).
11. **A rate never travels** — per-revision, per-host; composition binds it;
    re-sweep outcomes append (`fleet-kill-rate-ledger.md:22-39`; `:296-314`).
12. **A tick reading is a timestamped observation**, "re-run at the next
    boundary — never carried as a standing claim"; `moved=0 stale=0` is a
    complete outcome (`SKILL.md:1188-1189`, `:1085-1086`;
    `fleet-kill-rate-ledger.md:352`).
13. **Append-only errata everywhere** — "Errata are append-only blocks"
    (`corpus/QUALITY.md:7`); the service protocol and limits note end in such
    blocks (`service-optin-protocol.md:276`; `service-limits.md:264`); a sibling's
    note is never edited — an attestation returns a receipt or names the missing
    piece (`SKILL.md:998-1001`).

### D. What never crosses (stop conditions)

14. **The refusals apply at intake** — ten rows: no pin/no opt-in · no hermetic
    suite · moved substrate · live substrates/sessions · secrets-adjacent ·
    product semantics · coordinated rewrites · the exit-flatten family ·
    directed-repair-as-rate · foreign scratch
    (`SKILL.md:1246-1267`; detail of record `service-limits.md:42-55`). Three
    claim-bounds ride every sweep and never cross: single-edit mutants only ·
    hermetic only · per-revision and per-host (`fleet-suite-census.md:288-291`).
15. **The schedule is not handed.** "No daemon, no timer"; "who runs the update
    is the dispatcher's call" — the service hands a policy + an executed command,
    not a promise that it fires (`fleet-kill-rate-ledger.md:235-237`, `:314`;
    `SKILL.md:1017-1019`).
16. **The dispatch hand-off itself** — how an opt-in reaches the service between
    waves with no tameshi lane live — is unmeasured; the standing record is the
    no-opt-in line (`service-optin-protocol.md:264-266`).

## 4. Spot-checks (three, executed at this write; scratch `/tmp/w10-t10-3/`)

- **SC1 — the live/recorded boundary is real today, and the instrument held.**
  The six-case pin read (ER-3's command set, `fleet-kill-rate-ledger.md:287-291`
  + `merge-base --is-ancestor`), 2026-10-14T20:52:11Z, host `plazir27`, log
  `/tmp/w10-t10-3/pin-read.txt`: **4 current · 2 stale · 0 drift**, all six case
  paths porcelain-clean; tsukuroi-census pin `084951be…` → live `c396662e…`
  (recorded rev `165307fe` ancestor of HEAD `fac745b`), mado-verify pin
  `d7edaab4…` → live `93e43f8f…` (recorded rev `eead56b2` ancestor of HEAD
  `de22dfd`). Both moved cells are **past** ER-4's readings
  (`bba6cdf6…` / `7da4ec50…`): the owners' round-9 commits (`fac745b` /
  `de22dfd`, 17:47:30 −03:00) landed after the tick — the live side moves, the
  recorded rows stand at their revisions. Tool `cf41efaa8be5f52d…`, 1 341 L ·
  **held** (= ER-4's pin, `:320`); `bash tools/mutate-and-run.sh --selftest` →
  `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 (4.9 s, log
  `/tmp/w10-t10-3/selftest-tail.txt`). `--regression` was **not** re-run by this
  lane; the round's tick receipt is the tick lane's.
- **SC2 — the write-boundary text on the live bytes.**
  `grep -n "fleet file" SKILL.md corpus/knowledge/service-optin-protocol.md
  corpus/knowledge/fleet-kill-rate-ledger.md` → `SKILL.md:896` ·
  protocol `:92`, `:104`, `:197` · ledger `:272`, `:312`; `sed -n '7p'
  corpus/QUALITY.md` → `4. Errata are append-only blocks.`;
  `grep -n "^## Errata" corpus/knowledge/fleet-kill-rate-ledger.md` → `:239`
  (+ `:276` protocol, `:264` limits). [O]
- **SC3 — visibility is by citation, not by index.** `for r in
  kumitate-shokunin kagi-shokunin tsukuroi-shokunin mado-shokunin; do grep -rl
  tameshi "$r" --exclude-dir=.git | wc -l; done` → 0 · 0 · 12 · 19; fleet root
  `grep -ci tameshi` → `CORPUS/AXES/LEARNING/LOG/PROTOCOL/README` 0 each,
  `MANIFEST.json` 13; `ls corpus/knowledge/*.md | wc -l` → 16;
  `grep -c '^| \`knowledge/' corpus/README.md` → 9 rows covering 6 distinct note
  paths (`grep -o '^| \`knowledge/[^\`]*\`' corpus/README.md | sort -u`) —
  10 notes uncarried, this one included. [O]

## 5. Unknowns

- **U1 — driver invocation.** Whether any fleet driver applies the tick or the
  boundary rows with no lane acting is the cadence's open [U]
  (`SKILL.md:1017-1019`; `service-limits.md:220-223`).
- **U2 — the dispatch hand-off** between waves with no tameshi lane live is
  unmeasured (`service-optin-protocol.md:264-266`).
- **U3 — citation visibility is measured for four siblings only** (the SC3
  command shape); whether other lanes read these artifacts is unmeasured here.
- **U4 — the coverage-map gap** (10 of 16 notes uncarried, §4 SC3) is a measured
  state, not a verdict: whether/when rows land is the review/scribe call.
- **U5 — single host** (`plazir27`, 2026-10-14): no cross-host reading for any
  cell here (`fleet-kill-rate-ledger.md:218-219`).
- Carried as written: the ledger's U1–U9, the protocol's U1–U6, the limits
  note's U1–U5; this note adds no measurement to them.

## 6. Sources (pinned at this write; sha256 first-16 · `wc -l`)

| File | sha256 (16) | lines |
|---|---|---|
| `SKILL.md` | `ee09c3bddb6c` | 1269 |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | `2f25c51e3e0a` | 363 |
| `corpus/knowledge/service-optin-protocol.md` | `84d0c1547eed` | 286 |
| `corpus/knowledge/service-limits.md` | `a57a1e69be02` | 276 |
| `corpus/knowledge/fleet-suite-census.md` | `ec1c2d8d2877` | 674 |
| `corpus/README.md` | `1fe3050002f5` | 20 |
| `corpus/QUALITY.md` | `1923c94f4978` | 8 |
| `PROVINCE.md` | `f5e28bf144b0601c` | 20 |
| `tools/mutate-and-run.sh` | `cf41efaa8be5f52d` | 1341 |

[O] tameshi HEAD `b8eb96e`, worktree clean; siblings at this read: kumitate
`175de6b` · kagi `fecee87` · tsukuroi `fac745b` · mado `de22dfd` (case paths
clean). A concurrent round-10 lane may move files after this write; every line
cite above is tied to the pins in this table, and a reader on a differing
revision re-resolves.

## 7. Errata (append-only)

(none yet — new entries go below this line, never edits above, per
`corpus/QUALITY.md:7`, item 4)

**ER-1 — post-write concurrent drift, recorded not smoothed (O; appended
2026-10-14 ~20:56Z by T10-3, minutes after §4/§6).** Between this note's
readings (20:52Z) and this append, the instrument moved under a concurrent
round-10 lane: `tools/mutate-and-run.sh` `cf41efaa8be5f52d…` (1 341 L — the
revision §4 SC1 read **held**) → worktree `ac779b912860…`, 1 373 L
(`git diff --numstat` +75/−43; mtime 20:54:48Z; ` M` on porcelain). The worktree
is no longer clean: also present, untracked, is `corpus/knowledge/
operator-runbook.md` — another lane's in-flight file, never touched by this
lane (which wrote only this note; this note itself is untracked at this append).
No §1–§5 claim is re-cut: SC1's `held` is true at its timestamp; a moved tool is
a new revision and any receipt must cite the pin that ran (`SKILL.md:1036`; the
leg-cut work is a named hand-off, `fleet-kill-rate-ledger.md:282`). Re-read the
tool before quoting it.