# W2CriticReport — attack on the round-36 report

**Attacked:** `/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/tameshi.md` (fleet commit
`f4ef953`), cross-checked against lane tip `fbb01cf` (report's named tip `d9c496b1`), contract
`.ufo/evidence/round-36/contract.json`, all committed receipts, LOG/SCORECARD/QUALITY/lesson
records, and both wave specs/dispatches.

## Commands run (read-only; all git at `/home/vgpnk/Projects/shokunin/tameshi-shokunin`)

- `git log --format='%h %H %s' -14` ; `git status -sb`
- `git diff --name-status 796e08b… e423c41b…` / `e423c41b… b455001e…` / `b455001e… d9c496b1…`
- `sha256sum` of `c1-measure-v2.py`, `s103-git-hash-object.html`, `tally-audit-v3.py`, `mutate-and-run.sh` — all four match their pins.
- Parsed every committed receipt (`after/*.stdout`, `control/*.stdout`, `.exit`, `.stderr`) with `python3 json`.
- Ledger counts: `git show e423c41b:…ledger.json` → 493 entries; `git show b455001e:…ledger.json` → 497, last four headings exactly the four drifted sections.
- Independent re-run: `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (this seat's scratch, read-only) → **score 8, 64/64, rows 100, shonen 4/0/4/0, exit 0** — the report's uncommitted tip claim reproduces.
- Role census: `python3` `collections.Counter` over `dispatch-w1/w2.json` `registry.members` and `spec-w1.json` `items`.
- `git cat-file -t 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` → `fatal: could not get object info`; scanned every `.git` under `/fast/scratch/hyaku` (depth ≤5) — object absent everywhere.
- `git log --all -- '*ResidualSentinelClosure*'` → empty (dead-pointer claim TRUE); residual dir holds exactly the five named reports.
- `git -C /home/vgpnk/Projects/shokunin log --oneline -- .ufo/reports/round-36/tameshi.md` → `f4ef953`.
- Greps: LOG.md round-36 block (lines 1893–1942), SCORECARD.md:1731+, QUALITY.md:846 (criterion 72), lesson Holds/Gate, spec-w2 task text, `reports/round-1-calibration.md` anchors `## box-1/2/4`.

## What holds (verified, no defect)

Every receipt pointer in the report resolves to a committed file whose content matches the
claimed numbers exactly: monitor 6/60-64 @`796e08b` (exit 0), control 6/60-64 @`e423c41b`,
after 8/64-64 @`b455001e`, v2 deciding `C1_R36V2_PASS=true` 6/3/9 @`b455001e` (exit 0), v1
`C1_R35_PASS=true` and v2 `C1_R36V2_PASS=false` on the empty panel, census exit 0, depthD
9/9 + runner pin, SOURCES 100 rows. Kill rule clean: `e423c41b..b455001e` touches only
coldread evidence; `b455001e..d9c496b1` touches only receipts. Contract order honored
(contract in `e423c41b`, before all receipt commits). All 78 task prompts lead with
`/skill:godspeed` + bounds/pacman guards; both specs 39 seats within band 32–64. LOG
correction names the five real residual reports; criterion 72 + lesson Gate/Mistakes/Holds
exist; SHONEN box anchors resolve; S103 row `mined` with snapshot sha + used-by cites.

## Defects found

**D1 (moderate) — w1 role mix misstated.** Report line ~49: "spec-w1.json (39 seats:
1 connector, **3 executors**, 1 scribe, 2+ scouts, reviewers, critics, mutation-testers,
revengers, **simplifier** …)". Committed `dispatch-w1.json` registry and `spec-w1.json`
items both count: connector 1, scout 6, **executor 6**, scribe 1, reviewer 4, critic 4,
mutation-tester 10, revenger 5, **simplifier 2**. The reported "3 executors" is w2's
executor count transplanted onto w1. Evidence pointer exists and resolves — the number
next to it is wrong. *Correction:* re-read the parenthetical against the registry; the
correct w1 mix is 1/6/6/1/4/4/10/5/2 = 39.

**D2 (moderate) — w2 role mix not recorded at all.** The lane addendum requires "each
wave's seat count, role mix and dead seats" in the report. Report records w2 only as "39
falsify seats" — no role mix (actual: reviewer 7, critic 6, mutation-tester 9, revenger 5,
scout 7, executor 3, simplifier 2). Required section content absent.

**D3 (moderate) — the C2 before-demonstration's revision pointer does not resolve.**
Report cites mutant commit `91373d55…` (full hash in the receipts:
`91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`). `git cat-file -t` fails in the lane object
store and the object exists in no clone under `/fast/scratch/hyaku`. The vacuous-PASS
state is therefore un-inspectable at the named object; only the committed
stdout/stderr/exit receipts attest it. Receipts are self-consistent (rev field proves the
run happened), so this is a verifiability gap, not a fabrication. *Smallest correction:*
commit the emptied-panel file set or a `git bundle` of the scratch clone under
`.ufo/evidence/round-36/control/`, or record that the mutant is re-derivable by deleting
the public panel at `e423c41b` (which it is).

**D4 (minor) — three measurements lack committed receipts.** (a) "Re-measured at the
final tip `d9c496b1`: 8, 64/64" — no receipt file; I re-ran the counting command myself:
8, 64/64, exit 0 — claim TRUE but uncommitted. (b) "SHONEN census at tip: boxes=4
checked=0 asserted=4 untouched=0" — same, corroborated by my tip re-run. (c) "census run
at start (99 rows, exit 0)" — no start-census receipt; corroborated only indirectly
(monitor `sources.rows=99` at `796e08b`). Verdicts reproducible but carried without the
receipts the report's own discipline demands. *Correction:* commit the three stdout/exit
pairs under `after/` as the other receipts already are.

**D5 (minor, report-adjacent) — the LOG entry the report attests carries three dead
pointers of the class it was written to fix.** `LOG.md` round-36 entry cites
`validate-w1.json`/`validate-w2.json` (committed names: `validate-w1.stdout`,
`validate-w2.stdout`, plus `.stderr`) and `monitor-at-content-commit.*` (committed name:
`monitor-at-e423c41b.*`) — all unresolvable. These landed in `e423c41b`, the same commit
that added QUALITY criterion 72 ("a LOG.md entry that names a file as evidence must name
a file that exists at write time"). *Correction:* append-only LOG correction naming the
real filenames — the same mechanism this round used for `ResidualSentinelClosure.md`.

**D6 (minor, report-adjacent) — stale seat count in the committed w2 spec.** The
`W2ReviewWavePrep` task prompt inside `spec-w2.json` instructs: "the report itemizes 80
prepared-but-undispatched seats; verify the two specs … sum to 80 items". Both specs sum
to 78, and the report itself correctly says 78 — the wave artifact contains a stale
expectation that will produce a false-positive finding. *Correction:* none possible
post-commit; note it in LOG so the seat's "discrepancy" isn't misread as a report defect.

**D7 (cosmetic) — misrouted receipt naming.** The C1 *before* receipt lives under
`after/` (`after/monitor-at-796e08b.stdout`) while the *control* lives under `control/`.
Both pointers resolve, but the directory semantics contradict the filenames' role; the
LOG entry mirrors it. *Correction:* none required now; prefer a `before/` directory (as
round 35 used) going forward.

## Axis judgment

Calibration of the report's claims: **all quantitative verdicts reproduce** (score 6→8,
60/64→64/64, 6/3/9 predicate, 99→100 rows, depth 9, 78 seats, pins) — the numbers are
honest. The defects are record-keeping class: one wrong enumerated tally (D1), one
missing required enumeration (D2), one dead revision pointer (D3), three uncommitted
receipts (D4), plus dead pointers and a stale count in adjacent record artifacts
(D5–D6). Fixable, none load-bearing against C1 or C2.

**Verdict: ATTACK SUCCEEDED — 5 defects (2 moderate record-accuracy, 1 moderate
verifiability, 2 minor) + 2 cosmetic findings; all measured claims verified true against
committed receipts and one independent re-run.**

Installs/tools: none installed (system python3 + git only). Scratch:
`/fast/scratch/hyaku/tameshi-r36-seats/W2CriticReport/` (monitor tip re-run output).
