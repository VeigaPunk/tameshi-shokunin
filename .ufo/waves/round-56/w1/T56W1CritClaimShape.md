# T56W1CritClaimShape — claim-shape audit of C1/C2 against round-prompt §9 + AXES.md

Seat `T56W1CritClaimShape` (critic, wave 1, leaf — no subagent dispatch).
Item: audit the two claims against the fleet's claim-sizing rules:
(a) each after-state one concrete value one command re-derives over committed
bytes; (b) no universal clauses without an enumerating command; (c) at least
one claim on the lowest non-retired axis (re-derive depth + freshness at base);
(d) C1 and C2 causally separable; (e) a do-nothing control cannot reach either
target; (f) at least one claim sourced (S-row opened this round).

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf`
- Receipts: `.ufo/waves/round-56/w1/T56W1CritClaimShape-receipts/`
- Scratch: `$HYAKU_SCRATCH/tameshi-r56/T56W1CritClaimShape` (clone + clone2 live
  there; nothing else retained)
- Tooling: nothing installed or upgraded (curl, python3, git, bash suffice).
- No lane production file edited; no frozen instrument edited; no mutating git
  on the lane (two `git clone --shared` + `checkout --detach` inside my own
  scratch dir only; `rev-parse --show-toplevel` asserted on both).

## Verdict rows (one per audited item)

| # | Rule | Verdict | Command that shows it |
|---|---|---|---|
| a-C1 | C1's after-state is one concrete value, one command, over committed bytes | **PASS** | `python3 .ufo/evidence/round-56/c1/measure.py --lane LANE --rev 981c5e8b --work <empty> --explain` re-derived `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false`, byte-identical to `before/c1.stdout` (`receipts/c1-at-base.stdout`). One caveat: arm 1's measure is not fully a function of REV bytes — see F2. |
| a-C2 | C2's after-state same | **FAIL** — the stated value `C2_R56_PASS=true` is unreachable at any REV | `python3 .ufo/evidence/round-56/c2/measure.py --lane LANE --rev c3e2ca9f --work <empty> --explain` → `docs=0/4 total=2`, and arm 6's note cell can never increment (F1). The contract's own `before` quote also contradicts its cited receipt (F3). |
| b | No universal clause without an enumerating command | **FAIL** — C2's claim statement is universal but no command enumerates the set | contract `claims.C2.surface`: "Every receipt the lane certifies is bound…" — the counter checks exactly 5 receipts (3 red-before + 2 own); the deciding run emits ~9 more receipts it never gates; `receipt-inventory.json` exists but no arm reads it (F4). All of C1's universals are enumerated (arm3/arm4 denominators = 18 frozen headings; arm5 sweeps every bound entry; arm6 = last matching row). `base_note`'s "every claim path" is true but unlisted (F7). |
| c | At least one claim works the lowest non-retired axis | **PASS** — calibration 6 is lowest | command D at base → `recorded_cases=10 depth_score=10`; round-45 freshness measure at base → `fresh=71 score=9`; round-21 monitor at base → `score=6 credited=46`. `Retired: none` at `SCORECARD.md:281-283`. C1 works calibration. (`receipts/commandD-at-base.txt`, `r45-freshness-at-base.txt`) |
| d | C1 and C2 causally separable | **PASS by design, half unobservable while F1 stands** — two sequencing couplings named (F6) | Disjoint input sets: C1 reads `{precheck,r18,r21,ledger.json,SKILL.md,SCORECARD.md,waves w2/w3}`; C2 reads `{gate,receipts,QUALITY,SOURCES,registry.json,SKILL.md,control/*}`. Tree A (C1-only content) exists; tree B is design-buildable but unmeasurable until F1 is fixed. |
| e | A do-nothing control cannot reach either target | **PASS** | cheapest do-nothing for C1 = run the counter at untouched base: `total=5 C1_R56_PASS=false`; for C2 = run at the freeze: `total=2 C2_R56_PASS=false` (at base the gate is absent: `error=gate-missing total=1`). `controls.sh:39-40` registers exactly these as `CTL_0_c1`/`CTL_0_c2` expected-false. |
| f | At least one claim sourced, citing an S-row opened this round | **PASS** — C2 is the sourced claim | draft `corpus/knowledge/receipt-revision-binding.md` (`T56W1ScribeKnowledge-receipts/receipt-revision-binding.md.draft`) opens with `source:`/`verified-at:`/`recheck:` and cites **S281** (in-toto statement.md v1.2.0, fetched 2026-10-28, sha256 `cbe684a1…ebea` re-verified by my own fetch; the quoted line "Subject artifacts are matched purely by digest…" sits at lines 54-55 — `receipts/s281-fetch.txt`) plus already-mined S103; the scout row drafts S281 as `mined` with a located quote (`T56W1ScribeSources.md:13`). **Caveat F5:** no arm verifies the S281 row landed or that the cited `mined` row was opened *this* round. |

## Findings

**F1 — C2_R56_PASS is unreachable: `c2/measure.py:245` reads the wrong column
(`cells[8]=='mined'`; `status` is `cells[7]`).** SOURCES.md at the freeze has
142 eleven-cell rows; `cells[8]` is the `opened` date, so the counter's `mined`
set is empty for every possible tree — the docs arm caps at 3/4, `total >= 1`
always. Demonstrated: the counter's own parse over the real registry gives
`cells[8]==mined` → 0 rows, `cells[7]==mined` → 113 rows
(`receipts/c2-arm6-cells-defect.txt`); even on a tree where S281 *is* landed as
`mined`, the counter's mined set stays empty. Independently corroborated:
`T56W1ScribeSources-receipts/c2-arm6-defect.txt` runs the frozen counter on a
fixture with all four docs conditions → `docs=3/4`; the same file patched
`cells[8]→cells[7]` → `docs=4/4`. Prior counters agree on the column:
`round-49/c2/measure.py:285` and `round-50/c2/measure.py:352` both use
`cells[7]=='mined'` with `cells[8]` as `opened`. Prior round-45 used
`len(cells)!=13` (a 13-cell schema that no longer exists). **Impact:** item (a)
fails for C2, item (d)'s C2-holds tree is unbuildable today, and item (f) is
instrumentally invisible. Fix = `cells[8]` → `cells[7]`; the instrument is
frozen, so this needs a contract amendment (pre-data) or an L1 ruling —
reported, not patched.

**F2 — C1 arm 1 does not run on committed bytes: the frozen precheck invokes
the *worktree* copy of the round-21 measure.** `c1/measure.py` extracts the
REV bytes of `.ufo/evidence/round-48/quality/coldread-precheck.sh`, but that
script `cd "$LANE"` and runs `python3 .ufo/evidence/round-21/coldread/measure.py`
— the file on disk, not `git show REV:` bytes. Demonstrated
(`receipts/precheck-worktree-demo.txt`): in a scratch clone with the worktree
copy replaced by `sys.exit(42)`, the precheck prints
`COLDREAD_PRECHECK error=floor-measure` (the poisoned copy ran); on a clean
clone it prints `…lost=18 RED`. So the C1 docstring's "the live working tree is
never read" is false for arm 1 (arm 2's mirrored monitor does use REV bytes),
and `cand_credited`/`lost=` can be moved by uncommitted dirt. Same pattern
recurs in `no-harm.sh`'s `coldread-floor` monitor (also invokes the worktree
measure) and in the deciding run's own extracted precheck (it extracts the
REV bytes of the precheck but the script still cd's to the lane). The defect is
inherited (round-48 bytes), but this round's instruments *claim* committed-byte
reads for it. Reported, not patched (frozen bytes at REV must stay unchanged;
fixing the lane-side `measure.py` invocation is the precheck author's, not this
round's — but the claim text should stop asserting the universal).

**F3 — the frozen contract's C2 `before` quotes `total=6`; its own cited
receipt prints `total=2`** (`receipts/c2-before-misquote.txt`). Contract:
"verdict `C2_R56: … total=6 C2_R56_PASS=false`
(.ufo/evidence/round-56/before/c2.stdout)". Receipt + my re-run at the freeze:
`… own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false`. This is the
exact R55.2 class (a quoted total its own receipt contradicts) *inside the
frozen instrument whose round exists to repair it*; the round's own R55.2
disposition ("every value in this round's records names the receipt that
carries it") is breached at line one of the claim text. The cited receipt is
correct — the quote is wrong. (Same class, lower severity: the C1 `before`
quote silently drops the `rev=`/`c0=` fields; the values themselves all match.)

**F4 — C2's "Every receipt the lane certifies" is a universal clause without an
enumerating command.** The counter's coverage is exactly five receipt files:
the three frozen red-before slices plus the round's own `controls-a/b.stdout`
(arm 5). The deciding run produces ~9 further receipts (`receipt-gate.*`,
`frozen.stdout`, `no-harm.stdout`, `coldread-precheck.stdout`, `census.*`,
`clean-tree-*`, `*.start/*.end`) that no arm gates — several of them name no
revision at all, so under a literal reading of the claim they would violate the
rule the round lands. `w1/receipt-inventory.json` enumerates the lane's
receipt-bearing files, but no counter arm consumes it. Smallest correction:
scope the claim text to what arm 5 enumerates ("every receipt the round's
deciding path consumes as claim evidence") or add an inventory-driven arm.

**F5 — even with F1 fixed, arm 6 does not check what the claim asserts.** (i)
`cited & mined` is satisfied by *any* mined row — S103 is mined today, so a
note citing only S103 passes the note cell with zero new-source work; no arm
verifies the new S281 row exists in SOURCES.md at REV or that the cited mined
row was opened *this* round (the claim's "one SOURCES.md row for the source
opened this round" has no checking arm at all). (ii) The SKILL cell greps
`receipt-revision-gate` anywhere in `SKILL.md`; the claim says the rule belongs
in `## Standing rules` — a note dropped in, say, the appendix passes arm 6 with
the claim's section untouched (also relevant to C1: `## Standing rules` is a
frozen re-read heading). Both are "weaker instrument than claim" issues for the
L1/contract amendment, not fixable in wave 1.

**F6 — separability holds by design, but two sequencing couplings bind the
landing order.** (i) `SKILL.md`'s `## Standing rules` section sits on both
surfaces: C2's docs arm needs `receipt-revision-gate` in it, and C1 re-reads it
as one of the 18 frozen headings — so the SKILL edit must land **in or before
C0** or the heading's `section_sha256` at REV mismatches every reader report
(`T56W1ScribeSkill-receipts/08-section-record.json` shows base sha
`acfb671a…` → post-edit `449d7f42…`). (ii) `ledger.json` sits on C2's
positive-control surface (`control/frozen-surface.paths`): C1's wave-3 bind
writes it, so the controls run's receipts must be produced at a revision that
already contains the bind or the round's own positive control trips
`RECEIPT_REV_CONTENT_DRIFT` in arm 5. Both are *orderings*, not verification
dependencies — each claim verifies on a tree where the other was never touched.
Today the C2-holds side cannot be demonstrated because F1 caps `docs` at 3/4.

**F7 — `base_note`'s "byte-identical to fa48c06c for every claim path" is true
but "every claim path" is never listed.** Verified: `git diff --name-only
fa48c06c 981c5e8b` changes only `.ufo/` paths; the five named surfaces +
`ledger.json` are all identical (`receipts/base-note-check.txt`). Minor: name
the claim-path list in the contract or accept "all paths outside `.ufo/`".

**F8 — `.ufo/evidence/round-56/before/` is untracked at this write.**
`git status --porcelain` → `?? .ufo/evidence/round-56/before/`; the contract
and every drafted record cite `before/c1.stdout`, `before/c2.stdout`,
`before/c2-at-base.stdout`. If C0 omits them, every before-pointer fails
criterion 97 at the deciding revision (ScribeQuality F107-5 independently).
Also required: the S281 snapshot (`in-toto-statement-v1.md`) must be committed
at REV for the note's `verified-at` to be checkable.

**F9 — steering noise noted for the L1:** peer `C2Floor` sent the single word
"DISALLOWED" to me mid-seat (and to `T56W1ScribeRegistry`, per its report).
No code, command or scope; nothing in the contract or item identifies a
referent, so I treated it as noise and changed nothing on that basis.

## What wave-1 seats have already landed (context for the L1)

The drafted records consistent with this audit: ScribeScorecard's C2 before
quote correctly prints `total=2` (the records do not repeat the contract's
misquote); ScribeSources demonstrated F1 end-to-end; ScribeReport's skeleton at
line 30 already carries `cells[8]==mined=0 cells[7]==mined=113`.
Census at round start: `sources-census.sh validate --root … tameshi` →
`tameshi ok …/SOURCES.md`, exit 0 (`receipts/census.txt`).

## Report note on tooling

No installs; `pacman` untouched (host-wide pause). Every command above names
the revision it read.
