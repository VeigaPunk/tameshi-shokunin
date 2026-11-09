# Round 100 — registry rows for the round-98/99 audits (C1, operability) and Gate line-pointer recheck (C2, calibration)

Lane `tameshi`, attempt 2 (L1 `TameshiR100a2`; attempt 1 `TameshiR100` froze both claims, built
and dispatched wave w1, and died when the orchestrator session was SIGTERM-killed). Base
`34d8d7cef87ec78ed84bf5247e2609814cce74c8`; instruments `f8f912dfd569a33fade039af605f55cec15b921a`;
freeze `56f247da25a0252fcdb8e04a61675e0d73aae9ab`; wave spec `6ab72d6f`; records revision R in
`.ufo/waves/round-100/records-rev.txt`. Plan `plans/round-100.plan.md` (amendments in
§Amendments); claims `.ufo/waves/round-100/claims.json`.

## Gate

Sources opened this round. Attempt 1 fetched both on 2026-11-08 (HTTP dates
`Sun, 08 Nov 2026 23:50:27 GMT` / `23:50:36 GMT`; snapshots `.ufo/evidence/round-100/sources/`).
The scribe seat R100S1 re-read both committed snapshots at the freeze and located both quotes
(`.ufo/waves/round-100/w1/R100S1-sources-s327-s328-digest-and-quote.out`, rc 0). Attempt 2
re-fetched both live on 2026-11-09 UTC (HTTP dates `Mon, 09 Nov 2026 00:12:39 GMT` /
`00:12:42 GMT`): S327 4722 B (same length; sha256 `e14b7e4d…` differs from the snapshot's
`bbd5b0fb…`, the REST envelope carries volatile fields) and the S327 quote is present in the
live `abstractText`. Word counts are `len(quote.split())`.

- **S327 (new, tier A, admit)** — Jergas & Baethge 2015, "Quotation accuracy in medical journal
  articles — a systematic review and meta-analysis", PeerJ e1364, Europe PMC REST record
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.7717/peerj.1364&resultType=core&format=json`,
  accessed 2026-11-08 (4722 B; `s327.json` sha256
  `bbd5b0fbb8bafe42b6dbc8a43fcf64b49ba6060f5fbd8f834020a66e2c310c5f`), field `abstractText`:
  "Studies indicate, however, that quotations not serving their purpose-quotation errors-may be
  prevalent." (12 words). Grounds C2 and `corpus/knowledge/gate-line-pointer-recheck.md`: a
  citation can carry the right words and still point at the wrong place, so the pointer needs
  its own check.
- **S328 (new, tier A, REJECT)** — Mogull 2017, "Accuracy of cited "facts" in medical research
  articles: a review of study methodology and recalculation of quotation error rate", PLoS One,
  Europe PMC REST record
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1371/journal.pone.0184727&resultType=core&format=json`,
  accessed 2026-11-08 (5482 B; `s328.json` sha256
  `2d6d1f7a29b07923cdaa59cad9c1967600cdec1025dfb9c03ed352fd82bc9700`), field `abstractText`:
  "Previous reviews estimated that approximately 20 to 25% of assertions cited from original
  research articles, or "facts," are inaccurately quoted in the medical literature." (24 words).
  Rejected: it re-weights S327's error rate per quotation instead of per reference; the lane
  reports no rate. Flip: a lane claim that reports a pointer-error rate across records.

Registry changes (old → new): two rows appended (S327 `mined`, S328 `rejected`); no existing
row touched. `used-by` S327: `corpus/knowledge/gate-line-pointer-recheck.md,
corpus/lessons/round-100.md`; S328: `corpus/lessons/round-100.md`. Recheck S327 `365d`, S328
`180d`.

Assimilation: none (no `merge/tameshi/` package adopted). considerthese:
`considerthese/2026-11-08.md` idea 2 ("Gate line-pointer checker", proposals only) is mined as
C2; the pointer was grounded by re-reading the round-95 closure D1
(`corpus/lessons/round-95-verifier-spotcheck.md:172-183`).

Census before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ exit 0, 186 registry rows (`.ufo/waves/round-100/census-before.txt`). Census after: exit 0,
188 rows (`.ufo/waves/round-100/census-after.txt`); rows counted with `grep -c '^| S[0-9]' corpus/SOURCES.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **a selftest that resolved its own fixture relative to the scratch copy it ran from** (this round, pre-freeze): `gate-line-recheck.py --selftest` executed from `git show 4b6ebcc4:<tool>` bytes looked for the renderer under the scratch dir and exited 2 (`renderer-unreadable /fast/scratch/…/R93S1-tagstrip.py`) | `.ufo/evidence/round-100/mistakes/selftest-from-blob-4b6ebcc4.out` (rc 2) | the pre-freeze control runner (tools execute from blobs, round-99 M5) | `f8f912df`: the selftest reads the renderer blob at `--rev`; shown able to fail — the same command at `4b6ebcc4` rc 2, at `f8f912df` `GATE_LINE_SELFTEST: 24/24 pass` rc 0 (`mistakes/selftest-from-blob-f8f912df.out`) |
| M2 | **line numbers written into a Gate with no receipt that printed them** (mined from round 95): the round-95 Gate's six pointers (84, 4399, 4393, 4493, 2615, 2355) were rewritten at `16cf0d58` together with a new renderer description; no round-95 receipt prints them and no tested line rendering reproduces them | `.ufo/waves/round-100/w1/R100RV1.md` F1 (`R100RV1-receipts/R100RV1-repro.txt`); round-95 spot-check D1 | none at the time (quote-presence checks stayed green; `pre-freeze/c2-control-quote-presence.out` `flagged_d1=0`) | C2 `tools/gate-line-recheck.py` + QUALITY 180; shown able to fail — round-95 alone `miss=6` exit 1 (`records/c2-red-r95-only.out`), a one-pointer forgery flips to `miss` (`records/c2-forgery-r96-pointer.out`) |
| M3 | **a docstring sentence wider than the loader** (this round; the Amendment-59 class): "only the four definitions … are compiled (via `ast`, nothing else in it runs)" while compiling a `def` evaluates its decorators and default arguments | `w1/R100R2-receipt-renderer-default-arg.out` (`DEFARG_MARKER exists after run: True`); `w1/R100SN1-F1-renderer-exec.out` | the Amendment-59 ledger (reviewer and sentinel seats) | A2 narrows the plan sentence before the records run; tool bytes unchanged |
| M4 | **verdict names wider than the matcher** (this round): `absent` read as "not in the snapshot" while it is "`locate()` finds no word sequence"; one block per markdown table binds every row to the first sid | `w1/R100E3.md` F4/F5 (`R100E3-receipt-locate-mechanism.out`) | the out-of-set probe seat | A1 narrows the declared semantics; the in-set population has `absent=0` and no table-shared block |
| M5 | **an L1 attempt died with its wave in flight** (this round): the orchestrator SIGTERM ended attempt 1 and all twelve w1 seats; five attack/build seats (R100C1, R100CN1, R100R1, R100E1, R100SC1) and two report files (R100R2, R100SN1, R100S1 left receipts only) never landed | `.ufo/waves/round-100/w1-results.json` (`output: null`, kernel-restart note); `.ufo/watchdog.log` `lane-dead-no-report tameshi round=100` | the driver's dead-lane check | attempt 2 re-ran the four evidence-less attack/build seats as residual `w1r` (`make-w1r-dispatch.py`, names suffixed `b`); seats with receipts were adopted, not re-run |

## Registry changes

S327 and S328 appended (see Gate); no in-place edit of any existing row.

## Measurements

At R `2e792c8fd30b504c98d0abaafed720ecdb0723b9` (tool bytes executed from `git show R:<tool>`;
runner `.ufo/evidence/round-100/records-run.sh`; receipts `.ufo/evidence/round-100/records/`, each
headed by measured revision, tool path, tool sha256 and command; `c1-at-instruments.out` is the
runner's fixed file name and measures R):

```
c1-before-tag-miss      (base 34d8d7ce) REGISTRY_CHECK: could-not-evaluate (--tag ['r100-c1'] selects no registry row)   rc=2
c1-rows-base-vs-instr   tools_with_rows=0/4 at base (86 rows) -> 4/4 at R (98 rows; 3 rows per tool)
c1-at-instruments       (R) REGISTRY_CHECK: held=12/12 superseded=0   rc=0   registry-check sha256 7984540c…
c1-forgery-stub-* x4    REGISTRY_CHECK: held=11/12 superseded=0   rc=1 each (the stubbed tool's red row differs)
c1-full-registry        REGISTRY_CHECK: held=87/91 superseded=7   rc=1; differing: sources-census, verify-round15, mte-interop-check, receipt-bytes-tree (base: held=75/79, same four)
c2-before-token         git grep -c GATE_LINE_RECHECK 34d8d7ce   rc=1
c2-population           GATE_LINE_RECHECK records=5 pointers=21 hit=12 miss=6 absent=0 unbound=3   rc=1   tool sha256 dae90e50…
                        miss: round-95.md:17..22 cited 84/4399/4393/4493/2615/2355 observed 88/4403/4395-4397/4496-4497/2618-2619/2358-2359
c2-red-r95-only         pointers=6 hit=0 miss=6 absent=0 unbound=0   rc=1
c2-green-r97-only       pointers=2 hit=2 miss=0 absent=0 unbound=0   rc=0
c2-green-r99-only       pointers=2 hit=2 miss=0 absent=0 unbound=0   rc=0
c2-selftest             GATE_LINE_SELFTEST: 24/24 pass   rc=0
c2-control-quote-presence  QUOTE_PRESENCE pointers=21 present=18 absent=0 unbound=3 flagged_d1=0   rc=0
c2-forgery-r96-pointer  hit=5 miss=1 (forged child of R)   vs   c2-forgery-r96-unforged  hit=6 miss=0
c2-r95-stated-renderer  R95_STATED pointers=6 hit_under_stated=0   rc=0
```

Every frozen predicate holds at R; the full-registry run took 11 m 50 s (900 s rows; the wave's
critic and executor seats each lost a run to a ~300 s session kill before running it detached,
`w1/R100C1b.md` F1, `w1/R100E1b.md` method note).

## Wave

One v1 wave `w1`, 12 seats (executor 3, reviewer 2, critic 1, mutation-tester 1, sentinel 1,
connector 1, revenger 1, scout 1, scribe 1; attack seats by the §8 set — reviewer×2, critic,
mutation-tester, sentinel, connector, revenger — 7/12), spawned 20:58:40 and finalized with
`output: null` after the orchestrator kill (21:09:40). Residual `w1r`, 4 seats (critic, connector,
reviewer, executor), spawned 21:11:08, settled 21:42. Round total 16 seats. E2 re-derived all 21
pointers with an independent renderer (no false green); E3 ran 85 out-of-set lessons (A1); M1 ran
16 mutants (survivors are selftest coverage gaps); RV1 traced the round-95 numbers to an
un-receipted rewrite at `16cf0d58` (M2); R2 and SN1 left receipts only (A1, A2); S1 left receipts
only; SC1 left nothing. C1b built the frozen-pin printer (A3) and confirmed separability, axis
naming and the complete C2 population (21 of 21 Gate pointers across rounds 93-99); R1b built the
argv-aware stub (A4); E1b ran 12 own stubs (none keeps 12/12) and the full registry; CN1b found no
in-lane or sibling instrument that already graded line pointers.
