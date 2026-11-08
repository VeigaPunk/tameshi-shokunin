# Round 98 — every recorded control code is a measurement (C1) and every guard refusal class runs (C2)

Lane `tameshi`, round 98 (2026-11-08). Base `034240a591575167f0747ad7372a1f4b9cd33a58`.
Claims frozen in `plans/round-98.plan.md` and `.ufo/waves/round-98/claims.json`:
C1 calibration (a control driver's graded code is measurement-derived, checked by a committed
static audit) and C2 operability (all six `GUARD_SETUP` refusal classes of the frozen
`guard-inertia.py` exercised end to end, with a red arm).

## Gate

Sources opened this round (fetched live by the L1 on 2026-11-08; snapshots under
`.ufo/evidence/round-98/sources/`). Located quotes use the lane renderer
(`.ufo/waves/round-93/w1/R93S1-tagstrip.py:strip_tags`: script/style removed, each tag replaced
by one space, entities unescaped, lines right-trimmed). Word counts are `len(quote.split())`.

- S012 (re-opened, tier B) "Oracles That Cannot Fail" (Canedo), `https://arxiv.org/abs/2608.17214`,
  fetched 2026-11-08 (HTTP date `Sun, 08 Nov 2026 15:46:31 GMT`; 42588 B; snapshot
  `s012.html` sha256 `fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80`),
  line 112 under the same renderer: "A test oracle that obtains its expected value from the
  system it is judging cannot fail." (16 words) — grounds C1's class: a comparison whose
  recorded side is a constant has no measurement to move, so it cannot fail; S012 names the
  dual (the expectation itself flowing from the system under test). `used-by` gains
  `corpus/knowledge/control-assertion-anchoring.md`.
- S009 (re-opened, tier A) `https://discovery.ucl.ac.uk/id/eprint/1499169/`: two fetches on
  2026-11-08. The default curl UA got HTTP 403, 5517 B, sha256
  `d04c1de85d861c7c846e1dd39d576f352035acb8866b4ecdf56d6c5733d3e75e` (a Cloudflare challenge
  page); a declared UA (`tameshi-r98-scout/1.0`) and a browser UA each got HTTP 200, 42254 B,
  sha256 `be3f85dbdb766ab8d1935145099d77b3888915e0220183511253b5c1fa29ed7c`, byte-identical
  (`R98SC1-fetch.out`). Abstract at renderer line 413: "Identifying equivalent mutants remains
  the largest impediment to the widespread uptake of mutation testing." (14 words) — the row's
  flip condition (a fetchable copy with a located quote) is met with a declared UA. The row is
  re-opened and stays `queued` (no admitted entry cites it); the 403 snapshot stays as the
  first-attempt record, and the UA dependence is M5. Caveat from the same re-open: the abstract
  grounds the rates ("more than 7% and 21%", "approximately 30%") but not the row's opening
  `teaches` clause "identical compiled output …"; `teaches` is immutable in place, so a
  correction would be a superseding row, not this round's append.

Refused / not opened this round: **none beyond S009's probe.** No new row is written.

Registry changes (old → new), all in place-allowed cells:

- S012 `used-by`: `corpus/knowledge/oracle-anchored-survivors.md` →
  `corpus/knowledge/oracle-anchored-survivors.md, corpus/knowledge/control-assertion-anchoring.md`.
  `status` stays `mined`; `recheck` stays `90d`; no other cell changes.

Round-97 in-place `anchor` edits, logged here old → new (spot-check D-1; remedy B — the cells
are not rewritten a second time):

- S006 `anchor` old: `README §The three verdicts and §How a row is run @ page currentOid
  7eefc73010ad6342b80e3ed43915503e02c90618, fetched 2026-10-19`; new (round 97):
  `… fetched 2026-10-19; re-opened 2026-11-08: snapshot .ufo/evidence/round-97/sources/s006.html
  281627 B sha256 55bb7196, lines 490-492 under the same renderer`. The added text belongs in a
  Gate record, not the anchor cell; it stays as landed and the class is now measured by
  `tools/registry-cell-immutability.py` (red pair finds it, green pair over the round-98 range
  finds zero).
- S159 `anchor` old: `§Mutation testing overview, p ids mw-Q and mw-w, and §Overview p mw-Q @ page
  fetched 2026-10-25, snapshot .ufo/evidence/round-43/sources/wikipedia-mutation-testing.html
  170793 B sha256 6e4a06c0 revid 1373580212`; new (round 97): `… revid 1373580212; re-opened
  2026-11-08: snapshot .ufo/evidence/round-97/sources/s159.html 171636 B sha256 4b5a8374, line 762
  under the lane renderer …`. Same disposition.

Census before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → exit 0, rows 183 (A 165 · B 14 · C 4), mined 149 ·
queued 23 · rejected 11 (`.ufo/waves/round-98/census-before.txt`). Census after: see
§Measurements.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **an assertion that cannot fail, in the round's own new tool**: `guard-refusals.py` ended with `main()` instead of `sys.exit(main())`, so the first red run printed `GUARD_REFUSALS classes=6 refused=5 wrong=1 … red=state-unbuildable` and still exited 0. | `.ufo/evidence/round-98/pre-freeze/c2-refusals-red.out` first version ended `rc=0` after the `wrong=1` line; the pre-freeze receipt's own `rc=$?` line exposed it. | the receipt writer's `rc=` line — an exit code that is part of the receipt, not an assumption. | `sys.exit(main())`; re-run prints the same line with `rc=1` (committed receipt). The class is the round's own claim: a control whose exit is not the verdict cannot fail. |
| M2 | **wrong base for a no-work control**: `controls98.py` was first run with `--base 034240a5` (the round-98 lane tip), where the round-97 evidence already contains `GUARD_INERTIA`/`BATTERY states=`; both inherited no-work states printed MISMATCH (`states=18 matched=16 mismatched=2`). | `.ufo/evidence/round-98/pre-freeze/controls98-at-round-base.out` (`c1-nowork-bind-absent MISMATCH rc=0 want=1`, `c2-nowork-absent MISMATCH rc=0 want=1`); the correct base `07e50d6d` prints `states=18 matched=18` (`controls98-run.out`). | the driver's own MISMATCH lines — an inherited control carries the base it was written for. | run at `07e50d6d` (the round-97 pre-instrument base) and disclose the at-round-base behaviour as a declared limit; no control is deleted. |
| M3 | **append-only violation in the registry** (mined from round 97): the `anchor` cells of S006 and S159 gained round-97 re-open text in place. `CORPUS.md` rule 2 allows only `status`/`recheck`/`used-by` to change. | `git diff --numstat 0b19af5f..29734beb -- corpus/SOURCES.md` → `2 2 corpus/SOURCES.md`; the census passes (it checks shape, not cell mutability). | the non-author spot-check (D-1) — no lane instrument compared cells between revisions. | `tools/registry-cell-immutability.py`: the live red pair prints the two `anchor` findings (`changed=2`, exit 1), the green pair over `29734beb..d32043ec` prints `changed=0 removed=0 added=0` (exit 0), and the selftest is 10/10 including an indented-row arm. |
| M4 | **an eyeballed count**: the C1 draft counted 16 `add` sites by eye; the tool measures 15 static call sites (a loop site counts once, two sites register more than one state at runtime). | the audit's `sites=15` against `grep -cE '^[[:space:]]+add\('` over either driver (E1 re-derives it); the runtime state count is 18. | the tool's own output against an independent static count — the claim states `sites=`, not states. | the claim wording names sites and the acceptance requires the static count to equal the audit's; no number is typed from memory. |

| M5 | **a fetch conclusion that depended on the client**: my first S009 fetch used the default curl UA, got the 403 challenge and the Gate first recorded "not re-opened"; the scout's UA control fetched the same page with a declared UA (200, 42254 B, byte-identical across two non-default UAs) and located the abstract at renderer line 413. | `.ufo/waves/round-98/w1/R98SC1-fetch.out` (the UA control); the freeze snapshot `.ufo/evidence/round-98/sources/s009.html` (403, 5517 B) | the scout's UA control — the 403 was a client-keyed challenge, not an absent page. | re-open S009 with the 200 snapshot and the located quote in the Gate; both snapshots stay; status stays `queued` (no entry cites it). |

| M6 | **the round's own audit certified a narrower property than its sentence**: the wave's f02/f13 (`if`/dead-branch literal last), f17 (name from another function's scope), f08 (shadowed `add`), f12 (`p.returncode = 0` after the runner) and f18 (`rc += 7`) all printed `measured` while recording a constant — five mechanisms, one class: the resolver read source order, not the call's scope chain, all assignments, the recorder identity or attribute mutation. | `R98R1.md` fixtures `f02`, `f08`, `f12`, `f13`, `f17`, `f18`; `R98C1-c1-kill-a-shadow.txt` (nested-scope constant) | the wave reviewer and critic, running fixtures the freeze controls did not include; the pre-freeze 12-arm selftest had `measured-tuple-run` enshrining a stub as a runner and no shadow arm. | instrument repaired to v3 (A5): scope-chain resolution, every pre-call assignment must be measured, `returncode` reassignment and augmented assignment classified, duplicate `add` definitions make every site unresolved; selftest 12 → 18 arms; both real drivers keep 15/15/0 and 15/14/1. |
| M7 | **the round's own battery certified a pin the caller supplied**: a stub that refuses every class and runs nothing scored `classes=6 refused=6` when its own digest was passed, and the red summary could not distinguish a missed class from a refused one; no successful class was printed. | `R98R2.md` F1-F3 and attacks (b)/(c); `R98SN1.md` F1; `R98E2.md` F1/F3 (`R98E2-red-constant.out`) | the reviewer, sentinel and executor, each building the substituted tool or reading the loop arithmetic; the pre-freeze battery had no frozen-digest constant and no per-class line. | battery repaired (A7/A8/A9): the frozen tool's sha256 is a constant and `--tool-sha` must equal it; one `GUARD_REFUSAL` line per class, the positive's `GUARD_ROW` lines, and a red `observed=missed|refused` line with a computed exit; a base manifest carrying `GUARD_SETUP` is refused. |

Sweep for an inherited mistake: the round-97 spot-check's D-1…D-7 are this round's work items
(D-1/M3, D-2/C1, D-3, D-4, D-5, D-6/C2, D-7); the r97 lesson's M1–M4 were already mined.

## Errata (round-97 report, appended here per D-5)

- The round-97 report's Work-performed bullet says S159's quote is "14 words" and locates the
  snapshot at `00082805…`-class bytes under `s159.html`. Measured: the renderer span is **15**
  words (the lesson's own count), and `00082805…` is `equiv.html`'s digest; `s159.html` is
  `4b5a8374…`. The lesson's `## Gate` carries the corrected counts.
- The same bullet gives S006 as "lines 490-491" where the lesson says 490-492. Measured: the
  quoted sentence is the renderer span 490-491; the paragraph is 490-492. Both readings are
  stated in the lesson.
- The round-97 controls summary line `CONTROLS97 states=18 matched=18 mismatched=0` was quoted
  from stdout and not committed; it is now restated in
  `.ufo/evidence/round-97/pre-freeze/CONTROLS97-summary.txt` (a labelled restatement, not a
  re-execution; the 18 per-state receipts are authoritative).
- Round-97 spot-check D-3: the three stale pre-A15 fragments are marked superseded by appended
  notes beside them (`.ufo/evidence/round-97/pre-freeze/NOTE-superseded-r98.txt`,
  `.ufo/waves/round-97/w1/NOTE-superseded-r98.txt`), with both digests; nothing is rewritten.

## Registry changes

See §Gate: one `used-by` change (S012), logged old → new; no row added, removed, retired or
status-changed. The two round-97 `anchor` edits are logged, not re-edited.

## Measurements

Every number below is a line a committed receipt printed at the records revision (named in
`.ufo/waves/round-98/records-rev.txt`).

- **C1 audit at R.** `CONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0`, rc 0
  (`records/c1-audit-controls98.out`); the round-97 driver `sites=15 measured=14 literal=1
  unmeasured=1`, rc 1, line 156 named (`records/c1-audit-r97-driver.out`); selftest
  `CONTROL_ASSERT_SELFTEST: 18/18 pass` (`records/c1-audit-selftest.out`).
- **C1 driver at R.** `CONTROLS98 states=18 matched=18 mismatched=0`, rc 0, at base
  `07e50d6d`, with `c2-nowork-absent` outer `rc=1` (`records/controls98-run.out`,
  `records/controls/c2-nowork-absent.out`).
- **C2 battery at R.** Six `GUARD_REFUSAL <class> rc=2 token=ok` lines, the ten
  `GUARD_ROW` lines, `GUARD_REFUSAL_POSITIVE rows=10 rc=0`, and
  `GUARD_REFUSALS classes=6 refused=6 wrong=0 positive=ok`, rc 0
  (`records/c2-refusals-positive.out`); the red arm prints
  `GUARD_REFUSALS_RED state-unbuildable observed=missed rc=0` and
  `classes=6 refused=5 wrong=1 positive=ok red=state-unbuildable`, rc 1
  (`records/c2-refusals-red.out`); selftest 9/9.
- **Registry at R.** Green pair from `29734beb` to the records revision: `changed=0 removed=0
  added=0`, rc 0
  (`records/registry-green-r97-records.out`); selftest 10/10; the historical red pair
  (`0b19af5f..29734beb`) prints two `anchor` findings, `changed=2`, rc 1
  (`pre-freeze/registry-red-r96-r97.out`).
- **Census after.** Exit 0, rows 183 (A 165 · B 14 · C 4), mined 149 · queued 23 ·
  rejected 11 (`.ufo/waves/round-98/census-after.txt`).

## Wave

`w1`, 13 seats (executor 4, scribe 1, scout 1, reviewer 2, critic 1, mutation-tester 1,
sentinel 1, connector 1, revenger 1; attack 6/13 = 46%). Twelve seats filed a report;
executor R98E4 settled with no report and no receipts (output truncated at its first line),
recorded as the round's one dead seat. Findings are the amendments A5-A10 and mistakes
M6/M7: R98R1 falsified five C1 classification mechanisms (branch order, function scope,
shadowed `add`, attribute reassignment, augmented assignment) plus the stub-runner
spelling; R98C1 found the nested-scope constant and the `want=code` tautology; R98R2,
R98SN1 and R98E2 falsified C2's caller-supplied tool pin, red-summary indistinguishability,
missing per-class transcript and poisoned-base-manifest path. The instruments were
repaired after the readers finished (audit v3 `82c2e54b…`, battery v2 `de94cbcc…`) and the
records run re-ran every counter at the records revision.

## considerthese and assimilation

- `considerthese/2026-11-08.md` idea 1 (frozen-tally reconciler) is **not mined** this round:
  every tally this round lands (12/12, 9/9, 10/10, `sites=15`, `states=18`) is bound to a receipt
  path in the same record (the manual form); the mechanical reconciler stays a proposal.
  Idea 3 (hardening lint for drivers) is exercised only by the sentinel's probes on the three new
  tools, not made a standing scan.
- Idea 7's sweep: one candidate was probed twice (S009 at
  `https://discovery.ucl.ac.uk/id/eprint/1499169/`: default UA 403 challenge, declared UA 200 with
  the abstract) and re-opened; no new candidate was screened, and no row was appended or
  rejected this round.
- Assimilation: none — no `merge/tameshi/` package was adopted this round.
