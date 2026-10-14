# Operator runbook — the tameshi mutation service, end to end (round 10, T10-1)

Written 2026-10-14 by lane T10-1 (tameshi round 10). Role: the mutation
service's single operator-facing document — **the tool, the six-case ledger,
the opt-in protocol, the limits, the cadence (the tick), and the regression
mode** — so the service can be run and commissioned without oral context.
Landed at `corpus/knowledge/operator-runbook.md` per the round-10 dispatch
(T10-1). This runbook adds no gate measurement of its own: every line restates a
measured source and carries its anchor. It is never a second home — where this
runbook and an anchored source diverge, the anchored source governs (the
rendering/divergence rule, `SKILL.md:1249-1254`).

Anchors: **O** observation · **I** inference · **U** unknown. Line cites are
at the revision stamp below; on any later revision, re-resolve rather than
trust (`SKILL.md:1269-1270`).

**Revision stamp (write-time pins, re-measured 2026-10-14T20:53Z by this lane;
commands `sha256sum <file>` · `wc -l <file>` · `stat -c%s <file>`):**

| file | sha256 (first-16) | lines (`wc -l`) | bytes |
|---|---|---|---|
| `tools/mutate-and-run.sh` | `cf41efaa8be5f52d` | 1341 | 61 632 |
| `SKILL.md` | `ee09c3bd6d6cc705` | 1269 | 85 320 |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | `2f25c51e3e0a7851` | 363 | 36 169 |
| `corpus/knowledge/service-optin-protocol.md` | `84d0c1547eed257d` | 286 | 17 644 |
| `corpus/knowledge/service-limits.md` | `a57a1e69be02896a` | 276 | 21 720 |
| `corpus/QUALITY.md` | `1923c94f49788ade` | 8 | 329 |

`wc -l` counts newlines; `SKILL.md` and the ledger each carry one unterminated
final line, so their last displayed line is `wc -l`+1. Tameshi HEAD at this
write: `b8eb96e` ("probation round 9 (training r8)") [O]; the tree was clean at
the opening read (20:47Z) — concurrent round-10 lanes wrote during this
runbook's own window, recorded in ER-R1 below.

## 0. Quick start — the operator loop in one block

Run from the tameshi repo root. `<gate-file>` / `<owner-repo>` / `<path>` /
`REV` are the case's recorded row (§3); capture every log in one lane-scoped
scratch (`/tmp/w<N>-<lane>-*`, `SKILL.md:25-28`).

```bash
# (1) the instrument — is the tool the revision the records were measured under?
sha256sum tools/mutate-and-run.sh

# (2) the instrument's own gates (hermetic; /tmp scratch only)
bash tools/mutate-and-run.sh --selftest
bash tools/mutate-and-run.sh --regression --workdir /tmp/<scratch>/regression

# (3) the six-case pin read — per case, ER-3's exact command set
sha256sum <gate-file>                                    # live vs the recorded pin
git -C <owner-repo> show HEAD:<path> | sha256sum         # is the recorded revision the HEAD blob?
git -C <owner-repo> status --porcelain -- <path>         # worktree vs HEAD
git -C <owner-repo> merge-base --is-ancestor <REV> HEAD  # moved past the recorded revision?

# (4) read it: per case current|stale|drift, tool held|moved (§6), then the
#     trigger table T1–T3; append-only on the ledger — never edit §1–§4.
```

Sources: command set `fleet-kill-rate-ledger.md:287-293` (ER-3) and `:320`
(ER-4); readings `SKILL.md:1031-1036`; triggers `SKILL.md:1069-1090`; scratch
convention `SKILL.md:25-28`. The healthy-tick shape ER-4 recorded — and this
runbook re-ran, §9: `LEDGER: 6 cases in; target current=4 stale=2 drift=0;
tool held (cf41efaa…)` (`fleet-kill-rate-ledger.md:333`).

## 1. The service in one page

- **What it does.** Single-edit mutation sweeps of fleet gates: for each
  defect, "if this one exact edit were present in the target, would the gate's
  hermetic suite go red?" — KILLED / SURVIVED / INCONCLUSIVE per defect, one
  kill-rate headline (`tools/mutate-and-run.sh:22-27`).
- **What an opted-in lane brings:** a pinned revision, a one-command hermetic
  suite, a clause-mapped defect spec — nothing else (`SKILL.md:806-825`;
  `service-optin-protocol.md:54-77`).
- **What comes back:** a kill-rate table with per-defect verdicts, survivor
  non-equivalence probes, a restore proof, and recommendations as a corpus
  note — the only fleet file the run writes
  (`SKILL.md:883-897`; `service-optin-protocol.md:182-197`).
- **Absorption stays with the owner lane** — the service never edits, repairs
  or re-pins a gate (`SKILL.md:823-825`; `service-optin-protocol.md:142-180`).
- **Three engagement forms** (first two measured; attestation planned [U]):
  self-service (opting lane runs the harness on /tmp copies; tsukuroi r5),
  service (tameshi runs it for the lane; mado r6), attestation (tameshi
  replays an owner's recorded pins read-only; not yet executed)
  (`service-optin-protocol.md:32-38`; U1 `:259-261`).
- **Bounds riding every sweep:** single-edit mutants only · hermetic suites
  only · results per-revision and per-host (`fleet-suite-census.md:288-291`;
  `SKILL.md:860-863`).

Sources: this section restates `SKILL.md:794-897` and
`service-optin-protocol.md:16-38`; the standing offer and its queue
`fleet-suite-census.md:249-291`.

## 2. The tool — `tools/mutate-and-run.sh`

Contract revision `cf41efaa8be5f52d…` (r7-1, 1341 L / 61 632 B; version string
`mutate-and-run.sh r7-1 (tameshi-shokunin, 2026-10-14)`). The file header
`:1-131` is the full contract; what an operator needs:

- **Four invocations** (`:150-192`):
  `--target FILE --defects SPEC --suite CMD [--workdir DIR] [--label NAME]
  [--timeout N] [--tail N]` · `--regression [--workdir DIR] [--keep]` ·
  `--selftest` · `--help`.
- **The suite command** runs as `bash -c CMD` with `$MUTANT` = the artifact
  under test (the pristine copy for the control run); exit 0 = green, non-zero
  = red, 124 (timeout) / 126 / 127 (not runnable) = INCONCLUSIVE (`:43-51`).
- **Defect spec v1** — `@defect <id> | <desc>`, `@old <text>`, `@new <text>`;
  escapes `\n \t \r \\` only; every `@old` must occur exactly once and
  `@new == @old` is refused — all asserted **before any suite run** (`:29-41`).
- **Run order (fail-closed):** pin + pristine copy → parse spec → build every
  mutant, assert count==1 (any failure exits 2 before a suite run) → control
  run (a red control exits 2 — kills could not be attributed) → mutant runs →
  sha re-check → kill-rate report (`:53-59`).
- **Verdict lines** the operator quotes: `MUTATE_TOOL` · `CONTROL: GREEN|RED` ·
  `DEFECT <id>: KILLED|SURVIVED|INCONCLUSIVE` · `MUTATE_RESTORE: OK|DRIFT` ·
  `MUTATE: DONE|DEGRADED (… killed=… survived=… inconclusive=… kill-rate=…%)` ·
  `MUTATE: SETUP (<reason>)` (`:61-67`). Exit map: 0 done · 1
  done-with-inconclusive · 2 setup/refusal · 64 usage (`:69-70`).
- **Evidence layout** (`MUTATE_EVIDENCE: <dir>`): pristine copy, every mutant,
  `evidence/<id>.out`, `evidence/control.out`, `defects.tsv`, `results.tsv`,
  `spec.copy` — default `mktemp -d /tmp/tameshi-r4-2-run.XXXXXX` (`:110-113`).
- **Dependencies:** bash · python3 (byte-exact edit + spec parse) · git
  (`--regression` + the selftest's ledger-engine cases) · coreutils
  (`:129-131`).
- **The tool is pinned per run:** every log carries its own `MUTATE_TOOL`
  sha256; a mid-round tool move is an incident recorded, not smoothed
  (`service-optin-protocol.md:125-128`).

Sources: `tools/mutate-and-run.sh:1-131`, `:150-192`;
`service-optin-protocol.md:40-52` (self-service fit check).

## 3. The six-case ledger — the standing view

`corpus/knowledge/fleet-kill-rate-ledger.md` is one row per measured gate —
suite size, kill-rate, survivor classes, hardened-or-not, last sweep date +
pin — so every kill-rate claim cites one standing receipt instead of
re-quoting. It adds no measurement of its own; errata are append-only
(`fleet-kill-rate-ledger.md:1-19`, item 4 `corpus/QUALITY.md:7`).

**Reading a row** (§0, `:21-39`): suite counts are the suite's own executed
counters; a kill-rate is **composition-bound** (always read it with its
composition); survivors are measured, each with a non-equivalence probe;
"hardened" is what the owner did after the sweep — and a post-hardening re-run
of the same spec is a **directed repair, not an independent rate** (`:35-36`).

**The six measured cases:**

| # | case (owner · file) | suite | rate · composition | revised | pin · source |
|---|---|---|---|---|---|
| 1 | kumitate `scripts/kimi-census.mjs` | 43 | 8/10 = 80 % · 10 kill-aimed | r2 · `83016d45…` | ledger `:45` |
| 2 | kagi `corpus/surface-census.sh` | 16 | 8/10 = 80 % · 10 kill-aimed | r3 · `275d8294…` | ledger `:46` |
| 3 | tsukuroi `tools/tsukuroi-census.sh` | 26 | 6/10 = 60 % · 6 kill + 4 hole | r5 · `084951be…` | ledger `:47` |
| 4 | mado `tools/mado-verify.sh` | 28 | 4/10 = 40 % · 4 in + 6 out | r6 · `d7edaab4…` | ledger `:48` |
| 5 | kagi `corpus/checklist-run.sh` | 34 | 7/15 = 47 % · 7 kill + 8 hole | r8 · `7e5ec98b…` | ER-2 `:276` |
| 6 | kumitate `scripts/claims-check.mjs` | 39 | 7/10 = 70 % · 6 kill + 4 hole | r8 · `e9a21b44…` | ER-2 `:277` |

Rate sequence: 80 · 80 · 60 · 40 · 47 · 70, with directed-repair follow-ups
100 % (mado hardened, same spec) and the harness meta 0/6 → 6/6
(`fleet-kill-rate-ledger.md:134-137`; ER-2 `:279`). Survivor-class vocabulary
(measured instances, `:143-150`): **(a)** reported-but-unasserted surface —
kimi D2/D10, kagi B10, tsukuroi B9, mado D3/D8, checklist C1/F2; **(b)**
unreached fixture/arm — kagi B5, tsukuroi B7/B10, mado D7/R1, claims D9 (the
class's first JS instance); **(c)** one-directional assert — mado D9; **(d)**
out-of-band exit map — tsukuroi B8, mado D5. Round-8 mechanisms to know:
CLI fail-open (checklist G1), output-capture loss (E2), deny-list re-openable
(B3), assert-blind threshold (claims D8) (`:276-277`).

**Not claimed** (`:154-158`): cross-host/toolchain stability [U], coordinated
multi-edit rewrites [U], gate truth, live-substrate drift. The ledger's own
unknowns U1–U9 stand at `:216-237`.

**Where a new row goes:** appended, as a row or an errata block — **never an
edit of §1–§4** (`ER-3 :312`; `corpus/QUALITY.md:7`). **Embedding status:**
the harness's `--regression` carries four legs; cases 5/6 are **not embedded**
— their rows carry no `REGRESSION` line (named debt, tool owner's call; ER-2
`:282`; `SKILL.md:1226-1228`).

Sources: `fleet-kill-rate-ledger.md:21-48`, `:85-88`, `:132-158`, `:216-237`,
`:272-283`, `:312`; six-case roster restated at `SKILL.md:1092-1104`.

## 4. The opt-in protocol — running/commissioning a sweep

Sources: `corpus/knowledge/service-optin-protocol.md` (round 7, the two
measured engagements distilled) and the method-side rendering
`SKILL.md:794-897`.

**The offer.** Any lane may ask for a sweep of one of its gates. The queue is
an offer, not a schedule; a round with no opt-in records the no-opt-in line
as its complete outcome (`service-optin-protocol.md:26-30`;
`fleet-suite-census.md:269-291`). [U] how an opt-in reaches the service with
no tameshi lane live — the dispatch hand-off is unmeasured
(`service-optin-protocol.md:264-266`).

**Request shape — what the opting-in lane brings** (`:54-77`,
`SKILL.md:806-825`):

1. a **pinned revision** — sha256, size, line count, mtime, porcelain-clean
   tree at open; a moved substrate needs a **re-pin, never a
   re-interpretation of the old table** (`:59-62`);
2. a **one-command hermetic suite** invocable on a copy — must exercise the
   copy it is handed, print its own executed count + verdict, read no live path;
3. a **clause-mapped defect spec** — one single-edit defect per declared
   clause, expectation pre-registered `killed|survived`;
4. nothing else.

Fill-in template (`:97-107`):

```
mode:       service | self-service | attestation
target:     <path> @ sha256 <…>, <B> B, <n> lines, mtime <…>; tree porcelain-clean at open
suite:      <one command with "$MUTANT">; prints own count + verdict; hermetic (no live path)
spec:       <n> single-edit defects, one per clause <A…>; @old uniqueness asserted; expect: pre-registered
evidence:   <corpus note path>   (the only fleet file the run writes)
scratch:    /tmp/w<N>-<lane>-*   (lane-scoped; foreign scratch never removed)
absorption: owner lane hardens + accepts; the service side is recommendations-only
```

**Read-only guarantees** (`:109-135`): the target is never a write target
(pristine copy; `MUTATE_RESTORE: OK` sha256 before = after); the sibling tree
stays clean before/after — the provable negative is "this lane's writes never
touched the gate"; the harness is pinned per run; no live substrate read
(PATH-level stubs only, never a session); all writes confined to scratch + the
one corpus note.

**Owner-hardens discipline** (`:142-180`, rules 1–6): recommendations only ·
the owner hardens with a ledger (survivor → case label → line → executed
count) · closure is proven by re-running the same spec (a directed repair,
quoted before → after) · a replay names what remains open · no acceptance
means recorded unabsorbed — a complete outcome · harden the boundary classes,
not just the survivors.

**Report shape** (`:182-218`): pins · kill-rate table (control + one row per
defect, verbatim from `evidence/<id>.out`) · survivor non-equivalence probes ·
restore proof + tree-clean check · recommendation + named unknowns. Fleet-wide
adjudication: killed = suite red **and** the full case count still enumerated
(exit-only insufficient); survived = green at the same count; inconclusive is
excluded from the rate and named beside it; `kill-rate =
killed/(killed+survived)`; bands are a report convention, not a gate
(`:199-204`; tsukuroi-shokunin `SKILL.md:611-617`).

**Two conventions that make a table quotable:** pre-register the expected
table before the run; record composition beside the rate (`:206-218`).

## 5. The limits — what the service refuses

Detail of record: `corpus/knowledge/service-limits.md` (rows a–j with the
trigger column and verbatim anchor quotes, `:44-55`, `:57-170`); compact
rendering `SKILL.md:1246-1267`. **This runbook restates with pointers — it is
not a second home; on drift the anchored source governs** (a divergence
between the renderings is the finding, never smoothed, `SKILL.md:1249-1254`;
`service-limits.md:9-12`). The cadence applies this table at intake.

| # | refused — no sweep against… | operator consequence (anchor) |
|---|---|---|
| a | no opt-in / no pinned revision | no sweep; queue is an offer, not a schedule; record the no-opt-in line (`service-optin-protocol.md:26-30`) |
| b | no one-command hermetic suite | refused before any suite runs: `MUTATE: SETUP`, exit 2, no headline; red control also exits 2 (`SKILL.md:840-844`) |
| c | a moved substrate held to the old table | re-pin, never re-interpret; old table stays; service never edits/pins the gate (`SKILL.md:1083-1086`, `:811-812`) |
| d | live substrates / sessions (incl. handler-gated cases) | never read; PATH-level stubs only; hermetic subset measured, live rows declared out of scope (`service-optin-protocol.md:129-132`) |
| e | credential material / endpoint health | out of province → report, never absorb (→ kagi / → kama); secrets shape-only; secret *guards* are sweepable, the material is not (`PROVINCE.md:14-20`) |
| f | product semantics (is a gate's verdict right?) | never measured — sensitivity ≠ truth (`SKILL.md:879-881`) |
| g | coordinated multi-edit rewrites | outside the defect vocabulary — no rate claimed (`fleet-kill-rate-ledger.md:220`) |
| h | the exit-flatten family | harness boundary — named, not fixed; exit-only adjudication cannot kill it (`service-optin-protocol.md:267-269`) |
| i | a directed-repair re-run presented as a rate | recorded as directed repair, not an independent rate (`fleet-kill-rate-ledger.md:35-36`) |
| j | foreign scratch | never removed; only the service's own scratch paths (`service-optin-protocol.md:86-91`) |

Sources: `service-limits.md` §1–§3 (incl. the intake-precondition check: the
re-pin rule is present in the protocol, `:172-194`); unknowns U1–U5 at
`service-limits.md:218-239`.

## 6. The cadence — the tick, the reading map, the triggers

The cadence is **a pin read executed at the tick** — three readings per case,
three triggers, one re-pin rule. No daemon, no timer: "standing" is the ledger
+ the policy + an executed command at the round boundary
(`SKILL.md:1010-1019`; executed first at round 9, `:1155-1163`). [U] whether
any fleet driver would invoke it with no lane acting (`SKILL.md:1017-1019`).

**The reading map** (`SKILL.md:1031-1036`):

| reading | rule | meaning |
|---|---|---|
| `current` | `git show HEAD:<path>` sha == recorded pin | swept bytes are the gate's live blob |
| `stale` | recorded revision is an ancestor of HEAD, live blob differs | gate moved past the recorded revision; the table is historical, not wrong |
| `drift` | worktree differs from HEAD (porcelain non-empty, or live sha ≠ HEAD blob sha) | uncommitted bytes; a hygiene reading — git-materialized replays are already immune |
| tool `held` / `moved` | harness sha == / ≠ the sha on the last `REGRESSION_TOOL`/`MUTATE_TOOL` line | the instrument moved since the table was measured |

**Triggers — what to do** (`SKILL.md:1069-1090`):

- **T1 — a case reads `stale`** → re-measure at the live revision, or record
  the STALE cell with its reason; never edit the recorded table.
- **T2 — the harness sha ≠ the revision a case was measured under** → re-run
  the reproduction under the new revision and record both pins (precedent:
  mado's spec re-cut under `b56c6e57…`, identical verdicts and mutant shas).
- **T3 — an owner records a re-run at a new revision** → an appended row;
  §1–§4 never edited.
- **The re-pin rule:** a moved pin is never re-interpreted against the new
  bytes; both revisions stay in the record; `moved=0 stale=0` is a complete
  outcome, recorded as such (drift is never manufactured by re-cutting
  cases). A `drift` reading waits for the commit, then re-pins
  (`SKILL.md:1083-1086`; `fleet-kill-rate-ledger.md:293`, `:310`;
  `service-optin-protocol.md:59-62`).

**The tick is a timestamped observation, re-run at the next boundary — never
carried as a standing claim** (`SKILL.md:1188-1189`).

**Append discipline** (the ledger's own rule): new rows/errata go below the
last; §1–§4 are never edited (`fleet-kill-rate-ledger.md:312`;
`corpus/QUALITY.md:7`). Demonstrated by this lane on a scratch copy:
pre-append **36 169 bytes byte-identical** (`head -c 36169 copy | cmp -`
→ rc 0), then the drill row appended below; the real ledger's sha unchanged
(`2f25c51e3e0a7851…` before = after; scratch `/tmp/w10-t10-1/ledger-copy.md`,
drill block `DR-1`). No rate claimed — a drill. [O]

**Executed tick at this writing** (lane T10-1, 2026-10-14;
scratch `/tmp/w10-t10-1/pin-read.txt`, `:20:52:19Z`; shas `:20:52:28Z`):

| # | case | recorded pin @ rev | live (HEAD blob) | HEAD | worktree | reading |
|---|---|---|---|---|---|---|
| 1 | js-kimi-census | `83016d45…` @ `175de6ba` | `83016d45…` | `175de6ba` | clean | current |
| 2 | bash-surface-census | `275d8294…` @ `fecee874` | `275d8294…` | `fecee874` | clean | current |
| 3 | bash-tsukuroi-census | `084951be…` @ `165307fe` | `c396662e…` | `fac745b2` | clean | **stale** |
| 4 | bash-mado-verify | `d7edaab4…` @ `eead56b2` | `93e43f8f…` | `de22dfde` | clean | **stale** |
| 5 | kagi-checklist-run | `7e5ec98b…` @ `fecee874` | `7e5ec98b…` | `fecee874` | clean | current |
| 6 | kumitate-claims-check | `e9a21b44…` @ `175de6ba` | `e9a21b44…` | `175de6ba` | clean | current |

Headline as measured: `target current=4 stale=2 drift=0`; tool `held` at
`cf41efaa…`; recorded revisions ancestor-of-HEAD for both stale rows; all six
trees porcelain-clean at the read. Context for the two stale cells: rows 3/4
were already `stale` at ER-4's tick (`bba6cdf6…` @ `72b038d`;
`7da4ec50…` @ `12c8f08`, `fleet-kill-rate-ledger.md:328-329`) and the owners'
own round-9/10 lanes have since moved both repos' HEADs again (`fac745b2`,
`de22dfde` — observed, lineage unverified [U]); ER-4's addendum then caught
both worktrees dirty minutes after its clean read (`:356-362`). Their
re-sweeps are open work: an appended row per case, at the revision measured
(T1). Reader-side falsifier (drift arm), run in scratch: a `/tmp` copy of
kagi's `surface-census.sh` with one line appended hashes `508b7b02…` vs the
HEAD blob `275d8294…` → would read **drift**, while the substrate shows 0
porcelain lines after — the reading follows the row's pin, not the
substrate's history (round-8/9 falsifiers, `SKILL.md:1062-1067`,
`:1191-1195`). [O]

Sources: `fleet-kill-rate-ledger.md:285-316` (ER-3, the policy),
`:318-362` (ER-4 + addendum, the executed precedent); `SKILL.md:1010-1090`,
`:1155-1244`; executed instance above by this lane.

## 7. The regression mode — replaying the recorded legs

**One command replays every embedded leg**:
`bash tools/mutate-and-run.sh --regression [--workdir DIR] [--keep]`
(`SKILL.md:933-963`). Default scratch is a fresh
`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, removed on PASS unless
`--keep`, kept on FAIL/SETUP, **never removed when `--workdir` was given**.
Exit map: 0 all legs PASS · 1 ≥1 leg FAIL · 2 cannot verify
(`tools/mutate-and-run.sh:98-108`).

- **Each leg's bytes come from the repo's git object store**, not the working
  tree: `git show <rev>:<path>`, sha256 must equal the recorded pin
  (`REGRESSION_PIN` names repo + rev + path + pin). A drifted tree cannot
  move a replay; a missing repo/rev/blob or pin mismatch is a **SETUP refusal
  before any suite runs** (`SKILL.md:941-948`; `tools/mutate-and-run.sh:84-91`).
- **Expectation:** per leg, exact — every verdict row `match=10/10 flips=0`,
  closing `REGRESSION: PASS (cases=4 passed=4; ledger legs exact:
  killed-delta<=0 flips<=0)` (`SKILL.md:973-979`).
- **Reading a receipt — the discipline** (`SKILL.md:965-1008`): read the
  block, not the last line (`REGRESSION_TOOL` · `DATE` · `BAND` · `EXPECT` ·
  one `REGRESSION_PIN` per leg · per leg `SWEEP`/`TABLE`/`CASE` · `DEFECT`
  rows for differences · closing line); PASS is exact for ledger legs; **FAIL
  names its rows** — quote the rows, never hand-re-sweep to "confirm"; **SETUP
  is not a verdict** (cannot verify — fix the environment, never re-interpret
  the table); **the ledger proves the instrument, not the gates** (a leg PASS
  says the tool reproduces the recorded table on the pinned bytes; rates live
  in the ledger, per revision). The engine's own arms are selftested —
  `--selftest` → `MUTATE_SELFTEST: 67/67 pass`, including a doctored-pin
  refusal (`SKILL.md:1002-1008`).
- **Embedding status:** four legs at this revision (cases 1–4); cases 5/6
  are **not embedded** — named debt, tool owner's call
  (`fleet-kill-rate-ledger.md:282`; `SKILL.md:1226-1228`).

**Executed receipt at this writing** (lane T10-1, tool `cf41efaa…`, rc 0;
log `/tmp/w10-t10-1/regression.log`; workdir kept, `--workdir` given):

```
REGRESSION_DATE: 2026-10-14T20:51:32Z
REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact); fixture-mode default killed-delta<=1 flips<=1
REGRESSION_SWEEP js-kimi-census: MUTATE: DONE (target=js-kimi-census defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80%)
REGRESSION_TABLE js-kimi-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_CASE js-kimi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_SWEEP bash-surface-census: MUTATE: DONE (target=bash-surface-census defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80%)
REGRESSION_TABLE bash-surface-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_CASE bash-surface-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_SWEEP bash-tsukuroi-census: MUTATE: DONE (target=bash-tsukuroi-census defects=10 killed=6 survived=4 inconclusive=0 kill-rate=60%)
REGRESSION_TABLE bash-tsukuroi-census: match=10/10 recorded-killed=6 measured-killed=6 survived=4 inconclusive=0 flips=0
REGRESSION_CASE bash-tsukuroi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_SWEEP bash-mado-verify: MUTATE: DONE (target=bash-mado-verify defects=10 killed=4 survived=6 inconclusive=0 kill-rate=40%)
REGRESSION_TABLE bash-mado-verify: match=10/10 recorded-killed=4 measured-killed=4 survived=6 inconclusive=0 flips=0
REGRESSION_CASE bash-mado-verify: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)
```

Each leg materialized at its recorded revision (legs 1–4: `175de6ba`,
`fecee874`, `165307fe`, `eead56b2`) over the pins `83016d45…`, `275d8294…`,
`084951be…`, `d7edaab4…`; **the two `stale` substrates above cannot move these
legs** (git-materialized) — a PASS here is a statement about the recorded
revisions, not the live files (`fleet-kill-rate-ledger.md:350`). [O]

Sources: `SKILL.md:921-1008`; `tools/mutate-and-run.sh:72-109`, `:150-182`;
`fleet-kill-rate-ledger.md:341-352`.

## 8. The operator's full loop — commissioning to append

1. **Tick** (§0, §6) at the round boundary: tool pin → `--selftest` →
   `--regression` → six-case pin read → classify readings → T1–T3.
2. **On `stale`:** no action on the recorded table; either re-measure the live
   revision (a new sweep at the new pin) or append a STALE cell with its
   reason; both revisions stay in the record (T1, §6).
3. **On `drift`:** wait for the commit, then re-pin; nothing is re-interpreted
   against a moving file (§6, `service-limits.md` row c).
4. **On tool `moved`:** re-run the reproduction under the new revision and
   record both pins (T2).
5. **On FAIL:** quote the `REGRESSION_DEFECT`/`TABLE` rows; never hand-re-sweep
   to confirm; the divergence is the finding (§7).
6. **On SETUP:** fix the environment (repo/rev/pin), never re-interpret the
   recorded table (§7).
7. **New opt-in:** take the request shape (§4) → run per §2 → the corpus note
   is the only fleet file the run writes → owner absorbs with its own ledger →
   the outcome lands as an **appended row or errata block** in
   `fleet-kill-rate-ledger.md` (§3; ER-3 `:312`).
8. **A submission to become a leg** needs the contribution contract: pinned
   file set (path + revision + sha256), a defect spec (`@old` unique,
   `@new != @old`), a one-command hermetic suite with `$MUTANT`, and the
   recorded verdict table as its expectation (`SKILL.md:954-963`). [U] no
   fleet-contributed leg exists yet.
9. **Nothing else is promised:** no daemon, no timer, no schedule — "who runs
   it" is the operator's standing choice; the service's refusals stand (§5).

Sources: the trigger table `SKILL.md:1069-1090`; ER-3 `:306-314`; ER-4
`:318-333`; `service-optin-protocol.md:54-107`, `:142-218`.

## 9. Receipts from this writing — what was actually executed

Executed by the author lane (T10-1) at the revision stamp above, all writes in
`/tmp/w10-t10-1/`; sibling trees read-only — all six clean at the §6 read
(their own lanes write to them independently of this runbook):

- `--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0
  (`/tmp/w10-t10-1/selftest.log`, sha256 first-16 `775d8f68e019da07`). [O]
- `--regression` (above, §7) → rc 0, `cases=4 passed=4`, exact band. [O]
- six-case pin read (§6) → `current=4 stale=2 drift=0`; tool `held` at
  `cf41efaa…` — held vs ER-2's tool pin (`fleet-kill-rate-ledger.md:281`). [O]
- append drill on a scratch ledger copy (§6) → pre-append bytes identical,
  original sha unchanged. [O]
- reader-side drift falsifier (§6) → scratch copy reads `drift`, substrate
  0 porcelain lines after. [O]

Not executed here, named rather than assumed: a fresh-executor sufficiency
test of this runbook (a round-10 seat that did not write it; the
round-3 precedent vocabulary is `executor-test-sufficiency.md`); a real
re-sweep (no opt-in this round; the two `stale` cases' re-sweeps are open
appended-row work); cases 5/6 embedding (tool owner's call); any change to the
commitments this runbook restates. The runbook adds **no gate measurement** —
the ledger's own rule (`fleet-kill-rate-ledger.md:7`).

## 10. Unknowns carried — the service's open questions

- **Ledger U1–U9** (`fleet-kill-rate-ledger.md:216-237`): cross-host stability
  · coordinated multi-edit rewrites · cases-5/6 regression coverage (U3, since
  narrowed by ER-2 `:281`) · the ten unmeasured gates' profiles · live-substrate
  sensitivity · suite sensitivity ≠ gate truth · hardened revisions measured
  only against their own specs · sightings' gate-ness · the cadence's human
  invocation (U9).
- **Protocol U1–U6** (`service-optin-protocol.md:259-274`): attestation form
  unexecuted · no third-lane adoption · the dispatch hand-off · exit-flatten
  vs a stdout-reading harness · cross-shell PATH-stub behaviour · hardened
  rates across future spec extensions.
- **Limits U1–U5** (`service-limits.md:218-239`): driver invocation ·
  handler-present hosts · request-side secrets refusal untested · the
  exit-flatten boundary · host-dependence of PATH readings.
- **The cadence's [U]** (`SKILL.md:1017-1019`): whether any fleet driver would
  invoke the tick with no lane acting. Adoption is not measured by anything
  here — a round lands the runbook, not its use.

## Errata (append-only)

(none yet — new entries go below this line, never edits above per
`corpus/QUALITY.md:7`, item 4)

**ER-R1 — post-write tool drift, observed and recorded (O; appended
2026-10-14 ~20:58Z by T10-1, minutes after §9's receipts).** Every receipt in
this runbook (§2, §6, §7, §9) was executed at tool
`cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` (r7-1) —
the revision the stamp table pins. At this append the tameshi worktree holds
`4b3dfed5dbd07e8bd6f94edadd068906bb2bd7195fc528bbb7a47a046f703efe` —
VERSION `mutate-and-run.sh r10-2`, 1 509 L / 71 059 B, `git diff --numstat`
+217/−49 vs HEAD `b8eb96e`, uncommitted, mtime 2026-10-14T20:55:39Z. [I] a
concurrent round-10 lane's in-flight edit; its behaviour is **[U] here** —
nothing in this runbook measured it. Recorded, not smoothed: the §7/§9
receipts stay tied to the executed revision, no number is re-interpreted, and
**T2 is the fix** — when the edit lands, re-run `--selftest` and
`--regression` under the new revision and record both pins
(`SKILL.md:1075-1080`; ER-1 tool-drift precedent,
`fleet-kill-rate-ledger.md:250-259`, `:360`).

New errata entries go below this one.

**ER-R2 — the tool still in motion at close (O; appended 2026-10-14 ~21:00Z by
T10-1).** A re-read minutes after ER-R1: `tools/mutate-and-run.sh` now holds
`5807fd3877c6a3b8…` (1 547 L / 73 056 B, VERSION line still r10-2, ` M` on
`git status`), superseding ER-R1's live cell — the concurrent lane is still
writing. Both entries are timestamped readings; ER-R1's value stands at its
own timestamp, and no number above is re-interpreted. The remedy is unchanged:
the T2 step, once the edit lands (per ER-1's own rule, "re-read before
quoting", `fleet-kill-rate-ledger.md:259`). The receipts' executed revision
(`cf41efaa…`) is unaffected.