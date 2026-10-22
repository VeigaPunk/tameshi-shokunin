# RerunC1 — C1 (calibration) counter re-measurement and falsification

**Verdict.** The counter is sound and the claim's target is *reachable*, but the wave as currently
dispatched cannot reach it. Two independent gaps, both measured, both fixable:

1. **The residual wave covers 8 of the 12 sections the L1's own SKILL.md edit invalidated.**
   Sections 1814, 1905, 1964, 2086 have no re-read seat. Best reachable with the residual wave as
   dispatched: **covered=60/64**, exit 1.
2. **The wave-1 seat reports use absolute live-lane trace paths.** The assembler copies them
   verbatim into the ledger; the strict monitor rejects absolute paths as `trace-missing`. The
   landed ledger was rewritten lane-relative by the L1 (b1cc95e), so this is already repaired — but
   it was a live hazard for the whole wave and must not recur.

I did not write the content I attack. Every number below was measured in my own `/tmp` clones.

---

## 1. The counter re-measurement (exact commands, observed output)

Private clones, exactly as the item directs:

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/rerunc1-r27
git -C /tmp/rerunc1-r27 checkout -q --detach 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/rerunc1-base
git -C /tmp/rerunc1-base checkout -q --detach 91edf9cd82ccc72e10f62f81d37181f549d593b8
```

### At the content revision 2227d83

```
$ cd /tmp/rerunc1-r27 && python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/rerunc1-r27 --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1 depth_score=9 rev=2227d8338c02aa9a5fd7d95c1a41b76865ad7647
  uncovered: # tameshi-shokunin
  uncovered: ## Standing rules
  ... (39 uncovered headings)
EXIT=1
```

### At base 91edf9cd

```
$ cd /tmp/rerunc1-base && python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/rerunc1-base --rev 91edf9cd82ccc72e10f62f81d37181f549d593b8
C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1 depth_score=9 rev=91edf9cd82ccc72e10f62f81d37181f549d593b8
  ... (39 uncovered headings)
EXIT=1
```

The base run is **byte-identical** to the frozen pre-registration receipt
`.ufo/evidence/round-27/c1-before.stdout` (`diff` → identical; `c1-before.exit` = `1`). The
contract's `before` string is reproduced exactly. **The content revision moved C1 by zero** — the
round-27 content commit (`2227d83`) added SOURCES rows, a knowledge file, QUALITY rows and README
lines, and none of that touched SKILL.md's section bytes or the ledger, so both revisions read
25/64.

### The counter's own numbers match the monitor's, unchanged

```
$ cd /tmp/rerunc1-r27 && python3 .ufo/evidence/round-21/coldread/measure.py --repo /tmp/rerunc1-r27 --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
```

Monitor fields at 2227d83 (from the JSON it emits): `sections_covered=25`, `sections_total=64`,
`box3_full_page=false`, `calibration_restraint_score=6`, `depth_score=9`, `trace_gate=strict`,
`overrides_used=false`, `ledger_source=rev`, `ledger_committed=true`,
`shonen.marks=["~","~","~","~"]`, `shonen.box3_marked=true`, `shonen.box3_ledger_link=true`,
`shonen.box3_points=false`, `sources.rows=89`.

The counter prints `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9`. Every field is the
monitor's own value, re-derived, not re-invented: `covered`/`total` from `coldread`,
`restraint` from `calibration_restraint_score`, `depth_score` from `depth_score`. The base run gives
the same values with `sources.rows=87` (the two extra rows are S090/S091, added this round).

**The counter reports the monitor's numbers unchanged.** No drift, no recomputation, no
second opinion. `depth_score=9` is `min(10, len(legs))` = 9 recorded regression legs.

---

## 2. Does `box3_mismatch` really compare SHONEN box 3 with the monitor? Can it read 0 while a
section stays uncovered?

**Yes to both — and this is the sharpest thing I found.**

Source, `.ufo/evidence/round-27/c1-measure.py:46-54`:

```python
shonen = m.get('shonen', {})
marked = shonen.get('box3_marked') and shonen.get('box3_ledger_link')
mismatch = int(bool(marked) and not c.get('box3_full_page'))
covered, total, restraint = c['sections_covered'], c['sections_total'], m['calibration_restraint_score']
...
return 0 if covered == total and restraint == 8 and mismatch == 0 else 1
```

The monitor side, `.ufo/evidence/round-18/measure.py:679-683`:

```python
box3_marked = len(marks) >= 3 and marks[2] == '~'
box3_link = len(boxes) >= 3 and BOX3_LINK in boxes[2][1]
box3_points = box3_marked and box3_link and cr['box3_full_page']
restraint = 2 * sum(len(marks) >= b and marks[b - 1] == '~' for b in (1, 2, 4)) + 2 * box3_points
```

SHONEN box 3 is `- [~] Instructions executable by an agent without oral context`, and its
continuation line cites `.ufo/evidence/round-21/coldread/ledger.json` — the ledger the strict
monitor actually reads (round-21 selector pins `DEFAULT_LEDGER_PATH` to that path,
`.ufo/evidence/round-21/coldread/measure.py:22,109-112`). So the three pieces do line up:
box 3's `[~]` mark, box 3's ledger link, and the monitor's full-page verdict.

**But `box3_mismatch` is one-directional, and it can read 0 while 39 sections stay uncovered.**

`mismatch` is 1 only when box 3 is *asserted* (`marked` true) **and** the monitor says the page is
not fully credited. If box 3 is not asserted, `marked` is falsy and `mismatch` is 0 **no matter how
uncovered the page is**. I confirmed this by mutation (probe A, `/tmp/rerunc1-probeA`): changing
SHONEN box 3 from `- [~]` to `- [x]` at the content revision gives

```
C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=0 depth_score=9 rev=c78669b0...
EXIT=1
```

`box3_mismatch` reads **0** with 25/64 covered and 39 sections uncovered. The exit code stays 1
because `covered == total` and `restraint == 8` also fail — so the *counter* is not fooled — but the
**number `box3_mismatch=0` on its own is not evidence of agreement**. Anyone quoting that field
alone as "the box-3 disagreement is repaired" would be wrong. Read it as: *box 3 asserts a claim the
monitor contradicts*, never as *box 3 agrees*.

Related, and worse for the target string: **`box3_mismatch=0` is reachable together with
`covered=T/T` and `restraint=8` only if box 3 stays asserted.** `restraint=8` needs
`2 * box3_points`, and `box3_points` needs `box3_full_page`, so `restraint=8` already implies
full-page credit. The target tuple `covered=T/T restraint=8 box3_mismatch=0` is therefore
self-consistent and jointly strong — but each element alone is weak, and the printed line carries
`depth_score` too, which is not part of the target and is easy to mistake for one.

**Second-order finding: the counter is only as good as the monitor's ledger path.** The counter
invokes the round-21 selector (`.ufo/evidence/round-27/c1-measure.py:35`), which pins the ledger to
`.ufo/evidence/round-21/coldread/ledger.json`. Wave-1's own output therefore had to land in the
**round-21** ledger, not a round-27 one — which is what the L1 did. A counter pointed at a
round-27 ledger would have measured a different instrument.

---

## 3. Falsification probes against the counter and the monitor

All probes are independent clones in `/tmp`; the lane repo was never written to.

| Probe | Mutation | Result | Reading |
|---|---|---|---|
| A | SHONEN box 3 `[~]`→`[x]` | `covered=25/64 box3_mismatch=0`, exit 1 | mismatch is one-directional |
| B | delete the 39 uncovered SKILL.md sections | `covered=25/25 restraint=8 box3_mismatch=0`, **exit 0** | target met by shrinking the page — the target is self-fulfilling if the page shrinks |
| C | forge ledger entries, no trace receipts | `covered=25/64`, exit 1 | strict trace gate holds; no receipt, no credit |
| D | commit an edit to `.ufo/evidence/round-18/measure.py` forcing `box3_full_page=True` | `covered=64/64 restraint=8 box3_mismatch=0`, **exit 0** | the counter measures *whatever monitor code is in the tree* |
| E | forge entries **plus** matching receipts | `covered=33/64`, exit 1 | receipts alone don't credit; inputs must also verify |
| F | same edit as D but **uncommitted** in the worktree | `covered=64/64`, **exit 0** | see below — this is the important one |
| G | ledger trace paths absolute | `trace-missing:/home/...`, no credit | absolute paths are not canonical lane paths |
| H | receipt with wrong `rev` | still credited (33/64) | the monitor does not bind receipt→entry `rev` |
| I | append one line to SKILL.md | `covered=25/64` | one byte anywhere in SKILL.md re-keys every section |
| J | forge entries + receipts for all 39 uncovered | `covered=64/64`, **exit 0** | the ceiling is reachable; the monitor is only as strong as the ledger's contents |
| K | insert a line inside a credited section | `covered=24/64`, that section → `no-ledger-entry` | section credit is keyed by section sha256 |
| L | re-read at a *later* rev than the read | credit collapses to 25/64 | input drift is real and unforgiving |

**Probe F is the finding that matters most for the L1's own measurement discipline.** The counter
runs the monitor with `cwd=a.repo`, i.e. it executes
`.ufo/evidence/round-21/coldread/measure.py` **as it exists in the working tree**, and that
selector imports `.ufo/evidence/round-18/measure.py` from the tree as well. An *uncommitted*
one-line edit to the round-18 monitor in the clone's worktree produced:

```
$ cd /tmp/rerunc1-probeF && git status --porcelain
 M .ufo/evidence/round-18/measure.py
$ python3 /tmp/rerunc1-r27/.ufo/evidence/round-27/c1-measure.py --repo /tmp/rerunc1-probeF --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=2227d8338c02aa9a5fd7d95c1a41b76865ad7647
EXIT=0
```

The `--rev` was the unmodified content revision, yet the counter reported 64/64 exit 0. The counter
verifies the *revision* it measured (`m['revision'] != rev` → exit 2,
`c1-measure.py:42`) and the trace gate, but it never verifies the **monitor code's digest**. The
round-26 lesson recorded in QUALITY 53/54 is precisely about a counter that trusts the bytes it
runs. The C1 counter binds the ledger by path but not the instrument by digest.

**Smallest safe correction for that:** before the after-measurement, measure from a *clean* clone
whose worktree is byte-identical to the measured rev, and record the sha256 of
`.ufo/evidence/round-21/coldread/measure.py` and `.ufo/evidence/round-18/measure.py` next to the
result. The C2 counter already does the digest-binding the amendment-1 mentions
(`c2-measure.py:86-88` binds `probe_sha256` and `anchors_sha256`); C1 does not. This is a
measurement-hygiene fix, not a counter rewrite.

**Probe B deserves the L1's attention as a design note.** The contract's target is
"covered=T/T where T is the section total at the landed head". If the landed head's SKILL.md
*shrinks*, T shrinks with it and the target becomes satisfiable by deleting the uncovered
material. Probe B deleted the 39 uncovered sections and the counter printed
`covered=25/25 restraint=8 box3_mismatch=0`, exit 0 — a green C1 with a gutted page. The landed
head kept all 64 sections (verified: 64 old, 64 new), so this is not a live harm; but the target
wording would not catch it. Pinning T to the base count (64) would close it.

---

## 4. The measured state of the landed head, and the gap in the residual wave

The L1 landed `b1cc95e` while I was working:

```
b1cc95e round-27: wave-1 cold reads appended to the round-21 ledger (38 entries), traces, wave
records; SKILL corrections of the 12 sections the cold reads failed; F8 entry and lesson
corrections from wave findings
```

Measured at that head:

```
$ cd /tmp/rerunc1-head && python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/rerunc1-head --rev b1cc95e
C1_MONITOR: covered=52/64 restraint=6 box3_mismatch=1 depth_score=9 rev=b1cc95e1fb62532646d74e2863770c4fed0851cc
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Cross-language divergence — bash vs JS (round 3, measured)
  uncovered: ## Third case — cross-author confirmation (round 5, measured)
  uncovered: ### The protocol — ordered, fail-closed
  uncovered: ### The boundaries — what a service run is not
  ... (12 uncovered in total)
EXIT=1
```

Up from 25/64 — the wave-1 seats did real work — but still 12 short, and **all 12 fail with
`no-ledger-entry`**, the same reason as probe K: the L1's SKILL.md corrections changed those
sections' bytes, so their sha256 changed, so the wave-1 entries (keyed by the old sha) no longer
match. The credit is *keyed by section sha256*, not by section identity.

### The gap: 8 residual seats for 12 changed sections

The L1 changed **12** section bodies in `b1cc95e` (sha256 diff of `SKILL.md` at `2227d83` vs
`b1cc95e`, computed with the monitor's own `sectionize`):

```
131, 405, 668, 827, 858, 883, 1069, 1499, 1814, 1905, 1964, 2086
```

The residual wave `.ufo/waves/round-27/spec-residual.json` dispatches **8** seats, reading at
`b1cc95e`:

```
ReRead01 → 131    ReRead02 → 405    ReRead03 → 668    ReRead04 → 827
ReRead05 → 858    ReRead06 → 883    ReRead07 → 1069   ReRead08 → 1499
```

**Four changed sections have no re-read seat: 1814, 1905, 1964, 2086.**

I measured the ceiling this produces (probe W, `/tmp/rerunc1-probeW`): the landed head, plus
honest re-read entries for exactly the 8 sections the residual wave covers, and nothing for the
other four:

```
C1_MONITOR: covered=60/64 restraint=6 box3_mismatch=1 depth_score=9 rev=f918e7c6...
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ## Eighth recorded case — round 18
  uncovered: ### Round-21 gate/probe registry — finite environment differential
  uncovered: ## Ninth recorded case — round 26
EXIT=1
```

**60/64, exit 1.** The residual wave as dispatched cannot reach the target, and cannot reach
`box3_mismatch=0` either, because `restraint=8` requires full-page credit. Two of the four
missing sections are also still failing on their own merits: 1814 (Read32's `wrong-expectation`
on the waiver/`GIT_DIR` claim) and 1964 (Read37's `wrong-expectation` on the "47-row registry
battery" — `tools/registry.json` has 49 active rows at `2227d83`). Their wave-1 verdicts were
honest, and the L1 corrected the SKILL.md text for them; what is missing is a *fresh read of the
corrected text*.

For completeness: the target **is** reachable. Probe V (landed head + honest re-reads for all 12
changed sections) gives `covered=64/64 restraint=8 box3_mismatch=0`, **exit 0**.

### Smallest safe correction

**Dispatch four more residual seats for 1814, 1905, 1964 and 2086**, reading at `b1cc95e`, on the
same template as ReRead01–08. No counter change, no contract change, no content change is needed —
the mechanism already works (probe V). Four seats, four sections, and C1 closes at 64/64 exit 0.

Two smaller items, both cheap:

- **Read08's report is unparseable** and was rejected by the assembler:
  `json block does not parse: Expecting ',' delimiter: line 41 column 683 (char 8191)`. The cause is
  a single JSON string in `commands_executed` whose inner `"` characters are unescaped — the
  `commands_executed` entry on that line embeds a shell command containing `python3 -c "..."` and the
  inner quotes terminate the JSON string early (quote positions 8/680/715 on that line). ReRead04
  already covers section 827, so this is now moot for credit, but the wave-1 report itself stays
  broken in the evidence.
- **Four receipts are named `EXCLUDED-*.json`** (`EXCLUDED-Read05-2`, `EXCLUDED-Read17-13`,
  `EXCLUDED-Read24-10`, `EXCLUDED-Read29-13`) while the reports still cite the un-prefixed names,
  which exist separately. The named files exist and the reports' cited files exist; the `EXCLUDED-`
  copies are orphans. They carry no credit either way.

---

## 5. Wave-1 credit accounting (for the record)

The wave dispatched 39 seats for the 39 sections uncovered at the content revision — a clean 1:1
mapping, no gaps (verified by joining `spec-w1.json` seat→section against the monitor's uncovered
list). Assembling the wave's own reports with the frozen round-18 assembler against the round-21
ledger yields **341 entries, `coverage: 64/64 buckets covered`** — the assembler is satisfied.

The monitor, however, is the credit authority (the assembler says so itself), and it credits
**52 of 64** at the landed head. The difference is not assembly failure; it is:

- **11 sections carry a failing wave verdict** (10 `wrong-expectation`, 1 `gap-blocking`). These
  veto credit by design (`measure.py:635`, `covered = credited > 0 and not vetoes`). The findings
  are substantive: Read03 on the restore-discipline "absence of writes" claim, Read06 on the
  band-interior readings, Read07 on the "two gates of one lane" attribution, Read10 on the
  reproduce block, Read15 on the runner revision, Read25 on the bash row's write scope and exit
  map, Read32 on the waiver `GIT_DIR` claim, Read34 on `cases=8 passed=8`, Read37 on the 47-row
  registry, Read38 on the `S_EMPTY_GUARD` survivor. **These are correct findings**, and the L1's
  `b1cc95e` SKILL.md corrections address them.
- **The section sha256 keying** then invalidates the wave-1 credit for exactly those sections
  once the text is corrected — probe K, and the `no-ledger-entry` reason on all 12 at `b1cc95e`.

So the wave is doing its job and the harm is being repaired; the repair simply needs the re-read.

---

## 6. What I did not do

I did not write to the lane repo, did not run any `jj` command, did not touch the fleet root or
sibling lanes, did not run the C2 counter, and did not judge C2. No production file was edited. The
only artifact I wrote is this report. All probe clones live under `/tmp/rerunc1-*`.

### Files changed

- `.ufo/waves/round-27/w1/RerunC1.md` (this report) — the only file written.

### Tooling

No tools were installed or updated for this item; the host already had `git` and `python3`. Nothing
to record.

### Risks the L1 should weigh

1. **Residual wave covers 8 of 12 changed sections** → measured ceiling 60/64, exit 1. Four more
   seats needed.
2. **The counter does not digest-bind the monitor it runs** (probe F: an uncommitted worktree edit
   to the round-18 monitor yields 64/64 exit 0 at an unmodified rev). Measure the after-value from a
   clean clone at the head rev and record the two monitor-file sha256s beside the result. The C2
   counter already binds its probe and anchors by digest; C1 should be brought to parity.
3. **The contract's `covered=T/T` target is satisfiable by shrinking the page** (probe B: exit 0
   with 25/25). The landed head keeps all 64 sections, so no live harm — but pinning T to the base
   count would close the shape for future rounds.
4. **`box3_mismatch=0` does not mean "box 3 agrees"** (probe A: 0 with 25/64 covered). Quote the
   exit code and the covered fraction together, never the mismatch field alone.
