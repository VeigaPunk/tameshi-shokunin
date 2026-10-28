# T55W3CritRekeyLoop — is the re-key a measurement or a ritual?

Seat: T55W3CritRekeyLoop (leaf critic, round 55 wave 3).
Lane read-only; every mutation below happens in `git clone --shared` copies under
`/fast/scratch/hyaku/tameshi-r55/T55W3CritRekeyLoop` (the seat's own dir only; the shared parent untouched).
Receipts: `.ufo/waves/round-55/w3/T55W3CritRekeyLoop-receipts/` — `run.sh` reproduces every file in it
(clones are pinned to `4f7a7040`; the lane moved to `875bb75` while this seat ran, see §9).

## Verdict

**The gate is a measurement; the re-key entry is a ritual.** The cold-read credit gate
(`.ufo/evidence/round-18/measure.py`, selected by `.ufo/evidence/round-21/coldread/measure.py`) really
re-hashes every recorded input at the measured rev and really refuses drift — that is why the floor sits at
**46/64, score 6** at C0. But the entry that clears the drift is written by the integration driver, from a
section sha the driver itself recomputes, an input set inherited from earlier entries, and a trace receipt
the driver fabricates. **Nothing a reader does or fails to do is observable to the mechanism.** Eighteen
reader files that say in their own markdown that they read nothing take the floor to **64/64, score 8**.

And at the state this wave was dispatched against, the binder does not run at all:
`KeyError: 'n'` at `binder.py:54`, before a single heading is bound. **Zero `rekey-r55` entries exist in the
ledger at any lane rev** (`4f7a704` or `875bb75`), so the round has never actually closed the loop it
promises. The 64/64 obligation in `no-harm.sh` is currently met by no run of anything.

So the item's premise — "the floor returns to 64/64 by construction" — is true, and that is the indictment:
it is *by construction*, not by reading.

## 1. What the floor is before any re-key (the gate is real)

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo $S/lane --rev 0a2010acd1e92e4e332774050825e21bcfc7e079
score 8 covered 64 of 64 box3 True
$ ... --rev 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
score 6 covered 46 of 64 box3 False
$ ... --rev 4f7a7040a57e7aed17db941be9c27b300aafb783
score 6 covered 46 of 64 box3 False
```
receipt: `floor-before.out`.

The 18 uncovered sections fail with `input-drift:` reasons. Those reason strings carry the files C0 edited
(`corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/registry.json`, `tools/registry-check.py`,
`tools/context-capture.py`) together with paths that drifted in earlier rounds and are still pinned by older
entries of the same section (`.ufo/evidence/round-15/verify.py`, `tools/env-diff.py`,
`tools/bash-witness-study.py`, `corpus/knowledge/service-limits.md`). The drift detector works; nothing in
this report disputes it. The base measurement is the 64/64 that `no-harm.sh` monitors, so the whole 64 → 46
drop is attributable to C0's edits, and the whole 46 → 64 recovery in §3 is attributable to the re-key alone.

## 2. The binder as committed cannot run

```
$ python3 .ufo/evidence/round-55/integrate/binder.py $LANE $C0 $PIN $OUT
Traceback (most recent call last):
  File ".../binder.py", line 54, in <module>
    RES[item['heading']] = int(item['n'])
KeyError: 'n'
RC=1
```
receipt: `binder-as-committed.out`.

Cause: `binder.py:51-54` reads `.ufo/evidence/round-55/integrate/resolutions.json` as round 54's
`[{"heading":…, "n":…}]` map. Round 55's file is a prose adjudication log
(`{"id","from","finding","decision","evidence"}`, 11 entries at `4f7a704`, 21 in the working tree) — no
entry has `heading` or `n`. Round 54's `resolutions.json` *did* have that shape, and round 53's re-key took
`--resolutions FILE` as an argument. Round 55 kept the loader and changed the file.

The lane later added `.ufo/evidence/round-55/integrate/adjudicate.py`, which writes
`.ufo/evidence/round-55/integrate/allowed.json` — and **nothing reads `allowed.json`**: the binder still
greps out as `RES_PATH = …/resolutions.json` (§9 receipt `adjudicator.out`). The round built a producer and
left the consumer pointing at a file with a different schema.

Consequence: `python3 -c` over the ledger at both `4f7a704` and `875bb75` prints
`entries with rekey-r55 traces: 0`. The floor has not been restored once.

## 3. The ritual: 18 reader files that read nothing → 64/64

Fixture (`make-fixture.py`, in the receipts dir): for each of the 18 lost headings, it computes the section
sha at C0 with the frozen `sectionize`, then writes
`{"heading", "cand": C0, "section_sha256": <sha>, "findings": []}` plus a `.md` that says, in the file
itself, that the seat did not open `SKILL.md`, ran no command and read no artifact.

Patch applied to the clone only: the loader skips entries without `heading`/`n` (the one-line repair a
fixer would make, `binder-loader.patch`). Then:

```
REKEY ## Context gate classification …            start=1639 inputs=42   dropped=0 reader=FAKEREAD01
REKEY ## Mutation-sweep recipe …                  start=146  inputs=7702 dropped=0 reader=FAKEREAD04
REKEY ## Standing rules                           start=17   inputs=2497 dropped=0 reader=FAKEREAD07
...
REFRESH rekeyed=18 skipped=0 headings=18

$ measure.py --repo lane2 --rev <fixture commit>
score 8
covered 64 / 64
box3 True
reasons {'credited': 64}
```
receipts: `fixture.out`, `binder-patched.out`, `ritual-measure.out`.

The credit gate never sees the reader's markdown (`md.exists()` only, `binder.py:122`), never sees a command,
and never sees an input the reader opened. It sees one string: `section_sha256`, which the binder recomputes
from `git show C0:SKILL.md` and compares to itself. A reader that copies the value, or computes it with the
same frozen function (as the fixture does), is indistinguishable from a reader that read the page and found
it clean.

## 4. The trace receipt is authored by the driver, not observed

`binder.py:157-170` writes a `tameshi-trace-inputs-v1` receipt whose:

- `inputs` are the union of the section's **prior ledger entries'** inputs, re-hashed at PIN
  (`binder.py:134-143`) — not what a read touched. `grep -c strace binder.py` → **0**.
- `argv` is `[python, binder.py, LANE, C0, PIN, OUT, 'section', <heading>]` — 8 arguments, of which
  `binder.py:43` reads the first four and ignores the rest.
- `exit` is the literal `0` (`binder.py:165`).

Replaying the recorded argv of `section-07` (`## Standing rules`):

```
replay exit: 0 stdout lines: 19
first line: REKEY ## Context gate classification … 
last line: REFRESH rekeyed=18 skipped=0 headings=18
REKEY lines on replay: 18
ledger sha before: ff275c79a0182c50 after: ff275c79a0182c50 unchanged: True
```
receipt: `argv-replay.out`.

The recorded command does not reproduce the recorded trace; it re-runs the whole bind. The receipt is not a
record of a run — it is a template the binder fills in. Under the rule this lane adopted in round 17 (S058
"verifying trace": record the hashes of what a step *used*), the receipt records hashes of what *earlier
entries* used. That is false provenance, and it is the only artefact that satisfies the `traces-unrecorded`
arm of the gate.

The run's own input key is also not the section's: it is the union over all prior entries, so a heading read
in round 12 pins 7702 files for the `## Mutation-sweep recipe` and 2497 for `## Standing rules` — and
`commands_executed_count` is invented as `1 + len(inputs)` (`binder.py:179`), i.e. **7703 commands
"executed"** for a section no command ran against.

Because C0→PIN changed only evidence files (`git diff --name-only C0 PIN` = 10 paths, all under
`.ufo/evidence/round-55/`), none of the inherited inputs differ between C0 and PIN this round
(`provenance.out`: `changed_c0_to_pin = 0` for all 18 headings). So `read_rev: C0` with PIN-hashed inputs is
**latent, not active** this round — but it is latent by luck: the docstring explicitly anticipates a PIN that
"carries the round's record edits", and on any round where a pinned content file changes after C0 the entry
would claim a read at C0 against bytes that did not exist at C0. The gate never reads `read_rev`
(`grep read_rev round-18/measure.py` → only overlay/selftest uses), so the claim is unverifiable and unused.

## 5. The binder silently converts recorded failures into passes

`binder.py:147-152`:

```python
newest = max(old, key=lambda e: str(e.get('read_rev', ''))) if old else {}
verdict = newest.get('verdict', 'verified-record')
if verdict in ('gap-blocking', 'wrong-expectation', 'not-executed'):
    verdict = 'verified-record' if klass == 'record' else 'executed-ok'
```

Two independent defects in five lines:

- **Selection is hex order, not history.** `read_rev` is a commit hash; `max()` over strings has no relation
  to time. Measured over the ledger for the 18 headings: **18/18 picks are not the newest entry by commit
  date** (the newest by date is `99c3bc88` for every heading; the binder picks `f2a225ce`, `eb7838b1`,
  `c6e827a9`, `bb681566` — entries from rounds 17–26). The docstring's claim "class/verdict carried from the
  section's newest prior entry" is false.
- **A FAIL verdict is rewritten to a passing one with no new evidence.** In the fixture run this happened to
  two real headings:

```
HEADING ### Round-15 gate/probe registry
  prior pick     : verdict=wrong-expectation class=instruction read_rev=eb7838b16490
  new entry      : verdict=executed-ok … blocking_gaps=0 wrong_expectations=0 commands=39 inputs=38
  evidence added : ['.ufo/waves/round-55/w3/FAKEREAD12.json', '.ufo/waves/round-55/w3/FAKEREAD12.md']
HEADING ### Triggers T1–T3 and the re-pin rule
  prior pick     : verdict=wrong-expectation class=instruction read_rev=eb7838b16490
  new entry      : verdict=executed-ok …
```
receipts: `laundered-verdicts.out`; `recency.out` (`recency.py` re-derives the pick from the ledger at
`875bb75`: `RECENCY mismatches=18 of 18`).

The only "evidence" added is a file that claims the section was clean. A section with a recorded
wrong-expectation becomes credited, and the wrong-expectation is gone from the ledger's live view.

## 6. The mechanism selects for silence

The gate the binder applies to a reader is `len(findings) > allowed` with `allowed = RES.get(h, 0)`
(`binder.py:111,118`). With the shipped (prose) resolutions the map is empty, so `allowed = 0` always, and any
honest finding blocks the section. Worse: candidates are taken in sorted glob order and the **first** one
wins (`binder.py:113-126`). Probe with the live wave-3 reader for `## Standing rules` (`T55W3R07`, 2 findings)
and one extra file (`AAA07`, same heading, same sha, findings emptied):

```
=== RUN A: honest reader only (findings=2)
SKIP ## Standing rules reader-has-findings:2>0
REFRESH rekeyed=0 skipped=18 headings=18
=== RUN B: honest reader + a zero-findings file for the same heading
REKEY ## Standing rules start=17 inputs=2497 dropped=0 reader=AAA07
REFRESH rekeyed=1 skipped=17 headings=18
```
receipt: `selection.out`.

Any seat can neutralise a peer's finding by filing a quieter file for the same heading. The new
`adjudicate.py` builds the same property in: `min(cand, key=lambda x: len(x[1]["findings"]))` (line 43) takes
the *fewest-findings* candidate and allows exactly that many. And once a section binds with
`verdict: gap-minor`, `minor_gaps` is never gated (`grep -c minor_gaps round-18/measure.py` → **0**), so an
arbitrarily large accepted-findings count still credits.

At the live state (`875bb75`) the adjudicator reports `ADJUDICATE headings=18 with_findings=5 allowed_total=8`
and **12 of 18 headings have no reader at all** (`adjudicator.out`). The round cannot reach 64/64 honestly
today even with a working binder; what the binder would do at that point is reward whoever reported least.

## 7. The strongest counterexample, stated plainly

Take the exact claim: *a reader confirms the section's bytes and the binder records the current input hashes,
so the floor returns to 64/64 by construction.*

- The reader confirms nothing the binder does not already have: the binder recomputes the sha from the same
  blob with the same frozen function and compares. The reader's assertion is a copy of the expected value.
- The "current input hashes" are current by definition — the binder writes what it hashes. That is a
  consistency check on the ledger, not a check on a read.
- The 64/64 is therefore reached by the act of writing 18 small JSON files. Verified twice: once with the
  loader patched only, once again from scratch by `run.sh`, score 8, 64/64 (`ritual-measure.out` records
the fixture commit).

**What the mechanism can certify:** for every heading named, a file claiming that heading exists whose
`section_sha256` equals the sectionizer's hash of the C0 blob; every inherited input path is a canonical blob
at PIN with the recorded sha; a receipt exists in the tree whose inputs equal the entry's. Those are all
true of the round and all consistent with nobody reading anything.

**What it cannot certify:** that a byte of the section was read; that the recorded inputs are the ones the
read touched; that `findings` reflects a read; that the read happened at `read_rev` (the gate never reads it);
that the carried class/verdict is the authoritative one (it is chosen by hash order and then rewritten).

**What a reader would have to do for the credit to mean something** (all four, or the number is a ledger
invariant, not a calibration result):

1. Run the frozen tracer at C0 — `tools/trace-inputs.py` under `strace -f -y` over a command that actually
   reads the section and the artifacts its claims cite (`git show C0:SKILL.md`, `git show C0:<artifact>` per
   claim) — and commit the resulting `tameshi-trace-inputs-v1` receipt.
2. Have the binder take `inputs` **from that receipt**, hashed at C0, and refuse to bind a heading with no
   receipt. `read_rev` must equal the receipt's `rev` and the rev its inputs verify at.
3. Carry the prior verdict unchanged. A re-key refreshes hashes; it may never upgrade `gap-blocking` /
   `wrong-expectation` / `not-executed` to a passing class. Only a new read that resolves the finding may do
   that, and the resolution must be keyed by heading (round 53's `--resolutions FILE` shape), not inferred
   from the quietest file.
4. Aggregate findings across every reader file for a heading (union, or max count) so one quiet file cannot
   mask a peer's finding.

Even then the strongest honest claim is narrow and should be written down: *these bytes were opened, these
commands ran, at this rev.* A trace shows opening, not comprehension — the lane's own note says so
(`corpus/knowledge/input-keyed-coldread-credit.md` §4: "A seat can still skip a command; the rule makes a
recorded read checkable, not complete").

## 8. Smallest safe corrections, in order of size

1. **Make the binder runnable and wired.** Read the map the round actually produces
   (`allowed.json` from `adjudicate.py`) or take `--resolutions FILE` as round 53 did; tolerate prose entries.
   One path constant plus one guard. Without it nothing else in this report can be exercised at all.
2. **Delete the FAIL→pass rewrite** (`binder.py:150-152`). Carry the verdict.
3. **Select the prior entry by ancestry** (`git merge-base --is-ancestor`), not `max(str(read_rev))`.
4. **Bind inputs from a committed trace receipt at C0**, not from the prior union; `read_rev == rev` of the
   hashes. If that cannot land this round, the honest alternative is not to bind: report the floor at 46/64
   and name the re-key as owed.
5. **Aggregate findings per heading** (union/max) in both `binder.py:112` and `adjudicate.py:43`.

## 9. Live-state note

The lane advanced during this seat: `875bb75` ("the round filed before every seat settled … 18 re-key readers
still incomplete: the round reports that honestly"), with `51d1f0e` (C1 tool fixes) and `4c04c1d` (C2).
Re-checked at that rev: `binder.py` unchanged (same `KeyError` at line 54), `resolutions.json` still prose
(no `heading`/`n`), ledger has **0** `rekey-r55` traces, and the new `adjudicate.py` writes `allowed.json`
that the binder never opens. All findings above hold at `875bb75` as well as at the dispatch state
`4f7a704`; the measured floor at both is 46/64, score 6.

This seat did not attack the c1/c2 counters, the freeze, the tool edits or the records — other seats own
those. No lane production file, frozen file or wave spec was modified; no tool was installed.

## Artifacts opened

- `.ufo/evidence/round-55/integrate/binder.py` (at `4f7a704` and `875bb75`)
- `.ufo/evidence/round-55/integrate/resolutions.json` (committed at `4f7a704`/`875bb75` and the working tree)
- `.ufo/evidence/round-55/integrate/adjudicate.py` (at `875bb75`)
- `.ufo/evidence/round-21/coldread/measure.py`, `.ufo/evidence/round-21/coldread/ledger.json`
- `.ufo/evidence/round-18/measure.py` (`sectionize`, `entry_reason`, `entry_credit_reason`,
  `entry_is_stale`, `trace_reason`, `input_failures`)
- `.ufo/evidence/round-53/integrate/rekey.py`, `.ufo/evidence/round-53`/`round-54` `resolutions.json`,
  `.ufo/evidence/round-21/coldread/rekey-r53-*/refresh-receipts.json`, `rekey-r54-99c3bc88d704/refresh-receipts.json`
- `.ufo/evidence/round-17/coldread/traces/CR01/1.json`
- `.ufo/evidence/round-55/c1/lost-headings-at-c0.json`, `.ufo/evidence/round-55/no-harm.sh`,
  `.ufo/evidence/round-55/freeze.json`
- `.ufo/waves/round-55/w3/T55W3R06.json`, `T55W3R07.json`/`.md`, `T55W3R10.md`, `T55W3R11.json`,
  `T55W3R13.json`, `T55W3R18.json`
- `corpus/knowledge/input-keyed-coldread-credit.md`
- lane `git` objects at `9cf0146b`, `4f7a7040`, `875bb756`, `a2f559c`

## Reproduction

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w3/T55W3CritRekeyLoop-receipts
./run.sh            # exit 0; rewrites every receipt here from clean clones pinned at 4f7a704
```
Observed on a clean scratch dir: `binder-as-committed` → KeyError/RC=1; `ritual-measure` → score 8, 64/64,
box3 True; `selection` → RUN A skip / RUN B rekey; `argv-replay` → 18 REKEY lines, ledger unchanged; `recency` →
18 of 18 mismatches. Last verified: `run.sh` rc=0, every receipt here regenerated from clean clones pinned
at `4f7a704`; the fixture commit hash is the first line of `ritual-measure.out`.
