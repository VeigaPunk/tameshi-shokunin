# W2ReviewC2Predicate — per-clause falsifiability of the C2 v2 predicate

Seat: leaf reviewer, read-only (no production edits). Lane:
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Lane tip at review:
`fbb01cf46f8437fd1264c1a3acc053c882fa2164`; measurement commit
`b455001e2589b3f4f471d94a3de7e5e549b9f54c`; counter landed once at `e423c41`.

Frozen bytes re-verified before any conclusion (absolute paths):
`c1-measure-v2.py` = `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`
(also at `b455001e` via `git show … | sha256sum`), `tools/tally-audit-v3.py` =
`6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354`,
`tools/mutate-and-run.sh` =
`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`,
v1 `c1-measure.py` = `d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3`.
`git log -- .ufo/evidence/round-36/c1/c1-measure-v2.py` shows one commit
(`e423c41`); the counter is byte-identical at the tip, so the deciding receipt's
inputs are unchanged at tip.

## What I attacked

C2's depth surface = the tally-audit counter's predicate completeness. I extracted
`C1_R36V2_PASS` from the committed v2 bytes and asked, per conjunct: which committed
receipt records it **false**, and would any committed receipt's verdict change if that
clause alone were deleted (the wave's "a clause no receipt can fail is decorative"
test). The v2 delta over v1 is exactly three source lines:

- constants `.ufo/evidence/round-36/c1/c1-measure-v2.py:68-70` —
  `PUB_KILL_SLOTS_TARGET=6`, `PUB_ACCEPT_SLOTS_TARGET=3`, `PUB_DISTINCT_TARGET=9`;
- predicate `:538-544`, new terms `:539-541`:
  `pub_kill_slots==6 and pub_accept_slots==3 and pub_kill==6 and pub_accept==3 and pub_distinct==9`;
- v1 baseline `.ufo/evidence/round-35/c1/c1-measure.py:516-521` required only
  `pub_kill == pub_kill_slots and pub_accept == pub_accept_slots` (vacuously 0==0).

Committed v2 receipts at the tip (`git grep -n "C1_R36V2_PASS" fbb01cf`) are exactly
two execution receipts plus docs:

| receipt | rev | verdict |
|---|---|---|
| `.ufo/evidence/round-36/after/c1v2-at-b455001e.stdout` (`.exit` EXIT=0) | `b455001e…` | `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 … C1_R36V2_PASS=true` |
| `.ufo/evidence/round-36/control/v2-at-emptypanel.stdout` (`.exit` V2_EXIT=1) | `91373d55…` | `pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 … C1_R36V2_PASS=false` |

Auxiliary committed value observation (v1-labelled, but the printed operands evaluate
under v2 too): `.ufo/evidence/round-35/control/c1-v2-control.stdout` —
`pub_kill=0/6 pub_accept=0/3 pub_slots=9 pub_distinct=9 ho_kill=0/0 ho_accept=0/0 …
PASS=false`.

## Per-clause coverage (v2 delta, lines 539-541)

Legend — "isolating" = a committed receipt where this clause is false while the other
delta clauses are true. "Deletion" = does deleting this clause alone change the verdict
of some committed v2 receipt?

| clause | false in committed receipt | other delta clauses true there | isolating | deletion changes a verdict |
|---|---|---|---|---|
| `pub_kill_slots == 6` (:539) | only `control/v2-at-emptypanel` (slots 0) | no — all five delta terms false | **no** | **no** (after stays true; empty panel stays false via `pub_kill==6`) |
| `pub_accept_slots == 3` (:539) | only `control/v2-at-emptypanel` (slots 0) | no — all five false | **no** | **no** |
| `pub_kill == 6` (:540) | empty panel (0/6); aux r35 control (0/6) | aux: D (slots 6), E (slots 3), H (distinct 9) true; G also false | **partly** — isolates the kill-count pair (F,G) from D/E/H, but never false with G true | **no** (empty panel still false via G; aux still false via G) |
| `pub_accept == 3` (:540) | empty panel (0/3); aux r35 control (0/3) | aux: D, E, H true; F also false | **partly** — same shape, never false with F true | **no** |
| `pub_distinct == 9` (:541) | empty panel (distinct 0); r35 lesson receipts record `pub_distinct=6` on a 6-doc panel (F false there too) | empty panel: all five false; lessons: D/E/G true, F false | **no** — never false with F and G both true | **no** (empty panel still false via D/F) |

Result: **5/5 delta clauses are exercised only as a conjunction.** The single committed
negative receipt falsifies every delta clause at once, so it cannot attribute failure to
any one of them; deleting any single delta clause leaves every committed verdict
unchanged. In the direction that motivated the r35 repair (a *panel-shape* defect with
behavioural counts otherwise correct), no committed receipt moves: D and E appear false
only in the empty panel, and H appears false only where F is also false (the empty panel,
and the two r35 lesson receipts whose 6-document panels print `pub_distinct=6`). No
committed receipt has D, E or H false with F and G both true. The three **constants**
are separately load-bearing in the *constant-error*
direction — the deciding receipt's recorded PASS is arithmetically impossible under any
other constant value — and that direction has executed witnesses, but they are in the
untracked phase-1 reports (see Residual risk), not in committed receipts.

### Target constants, individually

| constant | committed receipt that would be false if the constant were wrong | executed witness | committed at tip? |
|---|---|---|---|
| `PUB_KILL_SLOTS_TARGET = 6` (:68) | `after/c1v2-at-b455001e`: both :539 (`pub_kill_slots=6`) and :540 (`pub_kill=6`) compare to it, so any other value turns the recorded PASS into false | w1/MTV2Predicate1 (6→7): predicate line flips, all 16 `COPY` rows byte-identical | no — `.ufo/waves/round-36/w1/` is untracked |
| `PUB_ACCEPT_SLOTS_TARGET = 3` (:69) | same receipt (`pub_accept_slots=3`, `pub_accept=3`) | w1/MTV2Predicate3 (3→2): flips, rows unchanged | no |
| `PUB_DISTINCT_TARGET = 9` (:70) | same receipt (`pub_distinct=9` is the sole :541 operand) | w1/MTV2Predicate2 (9→1): flips, stdout differs by one predicate line | no |

So all three constants are individually able to fail and each has an executed witness;
the witnesses are phase-1 scratch runs, not committed receipts, which is the whole of
the coverage gap below.

## Per-clause coverage (nine inherited conjuncts, lines 538, 542-544)

| clause | false in a committed receipt | note |
|---|---|---|
| `runner_ok` (:538) | none | no committed `runner_sha_ok=0` receipt in `.ufo/evidence/round-3*` |
| `tool_present` (:538) | `.ufo/evidence/round-35/before/c1-at-base.stdout` (`tool_present=0`, PASS=false) | v1-lineage receipt; no committed v2 before receipt |
| `tool_sha_ok` (:538) | none in the r35/r36 evidence tree | the r35 re-pin catch is in git history/LOG; round 33's before receipt records `tool_sha_ok=0` for that round's own counter |
| `ho_kill_total >= 4` (:542) | r35 controls (`ho_kill=0/0`) | joint with J (and with F/G in the r35 control) |
| `ho_accept_total >= 2` (:542) | same | joint with I |
| `ho_kill == ho_kill_total` (:543) | none | 0==0 in every control; 4==4 in every deciding run |
| `ho_accept == ho_accept_total` (:543) | none | 0==0 / 3==3 everywhere |
| `ho_invalid == 0` (:544) | none | `ho_invalid=0` in every committed v2/v1 receipt |
| `sealed_ok` (:544) | none in evidence receipts | `SEALED-*` diagnostics print only in control mode (counter :499, :514); the r35 wave report (`w2/SimplifyCounter.md:84`) quotes a `SEALED-SET-EMPTY` transcript, not an evidence receipt |

These are v1-lineage terms, outside the C2 delta, but they are part of "the round-35
behavioral verdicts all hold" that C2's predicate sentence names; six of the nine have
no committed negative receipt of their own.

## Findings

**MAJOR (coverage, does not falsify the frozen claim) — the v2 delta has no isolating
per-clause receipt.** With `after/c1v2-at-b455001e` (all true) and
`control/v2-at-emptypanel` (all five false) as the only committed v2 executions, the
delta's discriminating power is demonstrated only as a block. D (`pub_kill_slots==6`),
E (`pub_accept_slots==3`) and H (`pub_distinct==9`) have no committed observation in
which they are false and the other delta clauses hold, i.e. no committed receipt would
change if any one of them were removed. F and G are distinguished from D/E/H by the r35
control's operands (0/6, 0/3 with slots 6/3 and distinct 9), but F is never false with G
true, nor G with F true. The frozen `after_target` and `kill_rule` are still met; this is
a craft/coverage finding against the wave's own "every clause must be able to fail"
standard, not a contradiction of C2.

Isolation is cheap and none of the five clauses is structurally redundant. Computed from
committed panel/runner bytes (probe below, no tool execution):

| clause isolated | panel mutation | computed operands | expected predicate |
|---|---|---|---|
| H only | duplicate one kill copy's edits over another kill copy (9 docs) | slots 6/3, all rows still pass, `pub_distinct=8` | `PASS=false` (only :541 false) |
| D only | 10 docs: extra `set:"kill"` doc whose edits equal an accept copy's edits → invalid kill row | `pub_kill_slots=7`, `pub_kill=6`, accept 3/3, `pub_distinct=9` | `PASS=false` (only D false) |
| E only | mirror: 10 docs, extra `set:"accept"` doc equal to a kill copy → invalid accept row | kill 6/6, `pub_accept_slots=4`, `pub_accept=3`, `pub_distinct=9` | `PASS=false` (only E false) |
| F only | 6 kill docs where one diverges but the tool exits 0 (unique body) | slots 6, `pub_kill=5`, accept 3/3, `pub_distinct=9` | `PASS=false` (only F false) |

I did not execute these mutants: at review time seven peer counter processes were live
(`pgrep -af c1-measure`) and all counters fan out through the fixed
`/tmp/tally-audit-explicit` specimen root (`CONFIGS` :75-76), so a concurrent run risks
cross-contaminating other seats' deciding runs — the race the w1 RevengerEmptyPanel
report already serialized around. The four rows above are static implications of :539-541
plus the recomputed operands; I label them computed, not observed.

**MINOR — the empty-panel control's cited revision is unreachable from the lane.**
`git cat-file -t 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` → `fatal: bad object` at the
tip, and a sweep of every `.git` under `/fast/scratch/hyaku/tameshi-r36-seats/*/` found no
clone containing that object. An independent reproduction of the same mutant (peer, clone
commit `09c047f7`, parent `d9c496b1`) yields byte-equal predicate fields, so the receipt
is faithful; the gap is provenance only. Already disclosed in the committed lesson
(`corpus/lessons/round-36-verifier-spotcheck.md:90`, "minor, status-neutral") — recorded
here as confirmation, not a new routing.

**MINOR — the v2 delta does not freeze total panel cardinality or the `set` vocabulary.**
`load_copies_rev` loads every committed `*.json` except `manifest.json` (:296-315), but
`counted()` only filters `set=='kill'`/`'accept'` (:524-527). Probe result: a 10-document
panel — the 9 canonical copies plus one doc with `set:"noise"` whose edits duplicate a
kill body — yields `pub_kill_slots=6`, `pub_accept_slots=3`, `pub_distinct=9`, so all
five delta clauses hold while the panel carries an extra specimen. Latent only (the panel
is immutable at the measured rev), but "frozen public-slot cardinality" is today the
cardinality of two labels, not of the panel. A `len(pub)==9` or unknown-set rejection
clause would close it.

**MINOR — the mutant-demo receipt self-labels as a deciding run.**
`control/v2-at-emptypanel.stdout:8` prints `mode=deciding … C1_R36V2_PASS=false`; the
counter only substitutes the `CONTROL` label when `--tool` is passed (`:453-455`), and
control mode then bypasses the tool-sha check (`:462`). The kill rule's "exactly one
default-mode v2 run at the measurement commit" is therefore verifiable only from `rev=`.
No violation at `b455001e` (one deciding receipt, one mutant-demo receipt at a different
rev), but a reader counting `mode=deciding` lines sees two.

## What holds (verified, no finding)

- Pins exact at both `b455001e` and the tip; counter landed once and never edited after
  the freeze; tip `fbb01cf` only adds the lesson file, so the deciding receipt's inputs
  are untouched at tip (one canonical runtime, no reroute).
- The deciding receipt's 14 conjuncts are all true with exit 0; I independently
  recomputed `pub_distinct` from the committed panel + runner at `b455001e` (frozen
  module imported read-only): 9 copies, 6 kill / 3 accept, `distinct=9` — matches the
  receipt.
- The defect-2 closure is real: v1 prints `C1_R35_PASS=true` (exit 0) and v2
  `C1_R36V2_PASS=false` (exit 1) on the same zero-slot mutant rev, with the sealed/`ho_*`
  terms green in both, so the flip is attributable to the pub-surface terms alone.
- No delta clause is redundant by construction (isolation table above): the gap is
  receipt coverage, not predicate design.

## Residual risk / verification gaps

- The three constant-mutation witnesses (6→7, 3→2, 9→1) live in
  `.ufo/waves/round-36/w1/MTV2Predicate{1,2,3}.md`, which are **untracked** at the tip
  (`git status --porcelain` → `?? .ufo/waves/round-36/w1/`, `?? …/w2/`); MTV2Predicate2
  reports 16/16 `pass=True` rows unchanged and a one-line predicate flip 9→1. Until
  committed they are not receipts. The in-flight phase-2 seats W2MTV2EmptyKill,
  W2MTV2EmptyAccept and W2MTV2DupBody are producing exactly the D/E/H isolations.
- Six inherited conjuncts (`runner_ok`, `tool_sha_ok`, `ho_kill==total`,
  `ho_accept==total`, `ho_invalid==0`, `sealed_ok`) have no committed negative receipt in
  the r35/r36 evidence trees; only the sealed-gate `SEALED-*` path is documented, and
  only in a wave report/trace, not an evidence receipt.
- I consumed no counter run and did not execute the isolation mutants (shared
  `/tmp/tally-audit-explicit` race with live peers). The H-isolation operand (`distinct=8`
  with slots 6/3) is computed from committed bytes, not run.
- No `lsp` device is mounted in this seat (`xd://lsp` → "No such tool: xd://lsp";
  mounted: `ast_edit`, `debug`), so caller/definition checks were done against committed
  git objects and the frozen source; no grep result is presented as semantic proof.

## Verdict

VERDICT: **C2 HOLDS AS FROZEN** — the deciding receipt at the measurement commit prints
`C1_R36V2_PASS=true` (all 14 conjuncts true, exit 0) and the empty-panel control prints
`C1_R36V2_PASS=false` (exit 1) where v1 prints `true`, so the routed defect-2 vacuous
accept is closed by the committed v2 bytes under the frozen pins. **Per-clause coverage:
5/5 v2-delta clauses are exercised only jointly** — D/E/H have no committed isolating
negative receipt and no committed receipt changes when any single delta clause is
deleted; F/G are separated from D/E/H only by the r35 control's operands. No clause is
decorative by construction (each is isolatable with a small panel mutant), so the gap is
receipt coverage, and it closes when the in-flight D/E/H isolation receipts land.

## Commands run

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
sha256sum .ufo/evidence/round-36/c1/c1-measure-v2.py tools/tally-audit-v3.py tools/mutate-and-run.sh .ufo/evidence/round-35/c1/c1-measure.py
git show b455001e2589b3f4f471d94a3de7e5e549b9f54c:.ufo/evidence/round-36/c1/c1-measure-v2.py | sha256sum
git show fbb01cf:.ufo/evidence/round-36/c1/c1-measure-v2.py | sha256sum
git log --oneline -- .ufo/evidence/round-36/c1/c1-measure-v2.py
git log --oneline -2 -- .ufo/evidence/round-36/control/v2-at-emptypanel.stdout .ufo/evidence/round-36/after/c1v2-at-b455001e.stdout
git grep -n "C1_R36V2_PASS" fbb01cf -- .
git cat-file -t 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f        # fatal: bad object
git show --stat --oneline fbb01cf
git status --porcelain
cat .ufo/evidence/round-36/{after/c1v2-at-b455001e,control/v2-at-emptypanel,control/v1-at-emptypanel}.{stdout,exit}
cat .ufo/evidence/round-35/control/c1-v2-control.stdout .ufo/evidence/round-35/after/c1-at-34fa5b0c….stdout
python3 /fast/scratch/hyaku/tameshi-r36-seats/W2ReviewC2Predicate/probe_distinct.py
pgrep -af c1-measure
```

Probe output (imports the frozen v2 module read-only; reads panel and runner with
`git show` at `b455001e`; no tool execution, no counter run):

```text
copies 9 kill_slots 6 accept_slots 3
distinct 9
dup-kill-body: slots 6/3 = 6 3 distinct 8
extra-unknown-set: kill_slots 6 accept_slots 3 distinct 9
```

No tools installed or upgraded; no `pacman`; lane, fleet repo, sibling lanes,
`.ufo/state/` and all frozen artifacts untouched; the only lane write is this report.
