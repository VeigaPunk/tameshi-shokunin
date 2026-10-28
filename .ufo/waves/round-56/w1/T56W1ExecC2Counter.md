# T56W1ExecC2Counter — dry run of the frozen C2 counter (round 56, wave 1)

Seat: `T56W1ExecC2Counter`. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf`.
Counter (read, never edited): `.ufo/evidence/round-56/c2/measure.py`; gate (read, never edited): `tools/receipt-revision-gate.py`.
Receipts: `.ufo/waves/round-56/w1/T56W1ExecC2Counter-receipts/`. Machine-readable findings: `T56W1ExecC2Counter.json`.

Scratch: `HYAKU_SCRATCH=/fast/scratch/hyaku`, `S=/fast/scratch/hyaku/tameshi-r56/T56W1ExecC2Counter`.
No mutating git command ran against the lane; every fixture was a `git clone --shared` of the lane with `git -C "$D" rev-parse --show-toplevel` asserted equal to `$D` before any commit there. No tool was installed (python3 stdlib + git were sufficient).

## Verdict

| item | result |
|---|---|
| (a) base `981c5e8b` | **PASS as specified** — `error=gate-missing`, exit 1: the claim's subject does not exist at base |
| (b) freeze `c3e2ca9f` | **PASS** — the before line reproduces **byte-identically** (sha256 `5ec46f99…f486c5e2`), also from a fresh clone |
| (c) arms 2/3/4 | **LIVE** — each is red on the real receipt and flips green when that receipt is altered; each mutant moves exactly its own arm |
| (d) arm 5 `own` | **CANNOT PASS under the L1's planned order** — the frozen `controls.sh` makes 5 of 7 phase-A lines name control commits that exist only in throwaway clones (D2) |
| arm 6 `docs` | **CANNOT REACH 4/4 at any revision** — the `mined` cell is read from the wrong column (D1) |

**The contract's C2 target (`C2_R56_PASS=true`, `total=0`) is unreachable at every revision of this lane with the frozen counter.** D1 alone forces `docs ≤ 3` hence `total ≥ 1`; D2 independently forces `own=REFUSED` under the planned order. Both files are frozen, so this is a report-only finding: the L1 must either amend the contract (its `amendments` array is `[]`) or close C2 as `C2_R56_PASS=false` with D1/D2 named. It must not be papered over — a `total=0` line cannot be produced honestly.

---

## (a) Base: the subject does not exist

```
$ python3 .../.ufo/evidence/round-56/c2/measure.py --lane <lane> \
    --rev 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 --work <empty> --explain
C2_R56: error=gate-missing total=1 C2_R56_PASS=false
exit=1
```
`receipts/a-base.stdout`, `a-base.exit`.

The counter short-circuits at `show(lane, rev, GATE) is None` (measure.py:118-121) before any arm runs — so at base the C2 claim has no measurable surface at all, which is what the item asks to confirm:

```
$ git -C <lane> cat-file -t 981c5e8b20a2:tools/receipt-revision-gate.py
fatal: path 'tools/receipt-revision-gate.py' exists on disk, but not in '981c5e8b20a2…'
$ git -C <lane> cat-file -t c3e2ca9f0207:tools/receipt-revision-gate.py
blob
```
The gate first appears in the freeze commit (`git show --stat c3e2ca9` lists `tools/receipt-revision-gate.py | 331 ++++`). Correct behaviour, not a defect: the round-56 freeze *creates* the subject.

## (b) Freeze: the before line reproduces exactly

```
$ python3 <counter> --lane <lane> --rev c3e2ca9f020776b3d66c7af854fb82c834674fcf --work <empty> --explain
EXPLAIN arm1-selftest exit=0 14/14
EXPLAIN arm2-red54 exit=3 codes=RECEIPT_REV_CONTENT_DRIFT old-gate-accepted=True
EXPLAIN arm3-red54b exit=3 codes=RECEIPT_REV_UNRESOLVABLE
EXPLAIN arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT
EXPLAIN arm6-docs 0/4
C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false
exit=1
```
`receipts/b-freeze.stdout`. `cmp` against `.ufo/evidence/round-56/before/c2.stdout` → **identical bytes**, sha256 `5ec46f996321e85d46cab5af1cc266bc1f9d047a74981f98003d7823f486c5e2` on both.

Repeated from a fresh `--shared` clone at the freeze (`receipts/c-M0.stdout`, also byte-identical): the counter's reads are git-object reads at `--rev` and are clone-invariant, so a scratch clone is a faithful place to mutate inputs.

Arm 1 independently: `python3 gate.py --selftest` → `CASE codes-closed PASS` … `GATE_SELFTEST: 14/14 pass`, exit 0 (`receipts/gate-selftest.stdout`). The suite runs in a `tempfile.TemporaryDirectory` under the `TMPDIR` the counter sets to `--work`; nothing lands in `/tmp`.

## (c) Arms 2, 3 and 4 depend on the REAL receipt each names

Method: clone at the freeze, change one token in the named input, commit in the clone (toplevel asserted), run the frozen counter against the mutant commit with a fresh empty `--work`. Each row is a separate clone, so no mutant can inherit another's change.

| mutant | one-token change | arm before | arm after | whole line |
|---|---|---|---|---|
| M0 (none) | — | `red54=RECEIPT_REV_CONTENT_DRIFT red54b=…UNRESOLVABLE red55=…ABSENT` | identical to before line | `total=2` |
| **M2** | red-before slice `rev=077d431e6996` → `rev=c21081008adb` (the certified revision) | `arm2 exit=3 codes=RECEIPT_REV_CONTENT_DRIFT` | `arm2 exit=0 codes=none` | `red54=none … total=3` |
| M2b | delete `.ufo/evidence/round-21/coldread/ledger.json` from the declared surface | `…CONTENT_DRIFT` | still `…CONTENT_DRIFT` (other paths drift) | `total=2` |
| **M3a** | round-54 control set `rev=7df0e0426c98` → `rev=981c5e8b20a2` (a resolvable rev) | `arm3 exit=3 codes=RECEIPT_REV_UNRESOLVABLE` | `arm3 exit=3 codes=RECEIPT_REV_AMBIGUOUS` | `red54b=RECEIPT_REV_AMBIGUOUS … total=3` |
| **M3b** | every `rev=` in the control set → `c21081008adb` | `…UNRESOLVABLE` | `arm3 exit=0 codes=none` | `red54b=none … total=3` |
| **M4** | append one line naming `rev=4c04c1d33377` to the truncated round-55 C2 receipt | `arm4 exit=3 codes=RECEIPT_REV_ABSENT` | `arm4 exit=0 codes=none` | `red55=none … total=3` |

Receipts: `c-M0.stdout`, `c-M2.stdout`, `c-M2b.stdout`, `c-M3a.stdout`, `c-M3b.stdout`, `c-M4.stdout`.

Every mutant moved **exactly one** arm (M2/M2b/M3a/M3b/M4 each left the other two red at their original codes and left `own`/`docs` unchanged), so the three arms are separable and none is a restatement of another. The arm is green only when the receipt stops carrying the defect the arm names:

```
# arm 2 real, gate detail (receipts/gate-arm234-detail.txt)
GATE REFUSED … role=positive revs=077d431e6996 code=RECEIPT_REV_CONTENT_DRIFT
     drift=.ufo/evidence/round-21/coldread/ledger.json,.ufo/waves/round-54/w1/T54W1Crit02-receipts/coldread-at-base.json,…
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED  exit=3
# arm 3 real
GATE REFUSED … role=positive revs=077d431e6996,7df0e0426c98 code=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98
# arm 4 real
GATE REFUSED … role=verdict revs=none code=RECEIPT_REV_ABSENT
```

Two facts the L1 should carry:

- **Arm 2's drift is not hostage to the ledger.** Its docstring says "naming the cold-read ledger"; the gate actually names six drifted paths, and removing the ledger from `--paths` (M2b) still refuses. The arm only tests `'RECEIPT_REV_CONTENT_DRIFT' in codes`, so this is robustness, not a mismatch — but the docstring understates the drift set, and the round-54 receipt is red for far more than one file.
- **Arm 2's second conjunct is real.** `R54_EXIT` reads `DECIDING_RUN_EXIT=0` (`receipts/r54-deciding.exit`): the round-54 gate did accept the set the round-56 gate now refuses, which is the R55.5 defect stated as evidence rather than assertion.

## (d) Arm 5: what must exist at the deciding revision, and why the planned order does not produce it

### What arm 5 requires (measure.py:200-220, gate `check()` 90-165)

Three files, **in the tree of REV** (the counter reads git objects at `--rev`, never the working tree):

1. `.ufo/evidence/round-56/control/controls-a.stdout`, role `control` — every distinct `rev=` token must **resolve in the lane** and be **an ancestor of, or equal to, REV**. One unresolvable token refuses the whole file.
2. `.ufo/evidence/round-56/control/controls-b.stdout`, role `positive` — **exactly one** distinct `rev=` token (two → `RECEIPT_REV_AMBIGUOUS`), which must equal REV or be byte-identical to REV on every path listed in
3. `.ufo/evidence/round-56/control/frozen-surface.paths` — already committed at the freeze and itself byte-frozen (contract `frozen_paths`, and `deciding-run.sh`'s `FROZEN` list), so it must not change. Its ten paths are `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge`, `tools/registry.json`, `tools/receipt-revision-gate.py`, `.ufo/evidence/round-21/coldread/ledger.json`, `c1/measure.py`, `c2/measure.py`.

So arm 5's real constraint on the L1's sequence is: **REV may differ from PIN only outside those ten paths** (adding `control/*` is outside them — good), and **every rev token in `controls-a` must be reachable and ancestral**.

### The L1's planned order, as the frozen scripts state it

`controls.sh LANE BASE PIN FREEZE OUT` (usage line; phase B comment: "the positive controls are scored AT the revision they certify (PIN, the content-final revision) in a fresh clone") → commit `control/controls-a.stdout`, `controls-b.stdout`, `.exit` → `REV` → `deciding-run.sh LANE REV FREEZE OUT`. `deciding-run.sh` enforces the shape: `HEAD == REV`, clean tree, control receipts committed at REV in a commit descending from FREEZE, and gate 0b runs **the same gate call as arm 5** against REV.

### It does not produce a passing arm 5 — measured

`controls.sh` phase A runs five mutation controls in `clone_at` clones, each of which makes a commit inside that throwaway clone and then runs the counter with `--rev "$(git -C "$repo" rev-parse HEAD)"`. `emit` echoes the counter's verdict line verbatim, so those five lines carry rev tokens of commits that exist only in the clone. Built faithfully in a scratch clone (`receipts/demo3-gate.txt`, counter output `d-demo3-NOANCESTOR.stdout`):

```
GATE REFUSED …/controls-a.stdout role=control
  revs=09a400e7…,1b6425dc…,38caf81b…,65ea555d…,76dc7ab3…,981c5e8b20a2…,c3e2ca9f0207…
  code=RECEIPT_REV_UNRESOLVABLE rev=76dc7ab3f9085605783e03415a8dbabda336a1ac
GATE OK      …/controls-b.stdout role=positive revs=c3e2ca9f0207…
GATE: receipts=2 ok=1 refused=1 codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED   exit=3

09a400e7… in-lane=NO   1b6425dc… in-lane=NO   38caf81b… in-lane=NO
65ea555d… in-lane=NO   76dc7ab3… in-lane=NO
981c5e8b20a2… in-lane=yes   c3e2ca9f0207… in-lane=yes
C2_R56: … own=REFUSED docs=0/4 total=2 C2_R56_PASS=false
```

The same refusal fires inside `deciding-run.sh` gate 0b, which is the identical gate call, so the deciding run would stop at `DECIDING_REFUSED receipt-binding` and `DECIDING_RUN_EXIT≠0` even if every other gate passed. (At the freeze the phase-A needles are absent and the mutations produce no byte change — that is why `CTL_0_c2` alone looks harmless — but at a real PIN the rekey entries, the reader hashes, the standing row, the gate arm and the red-before slice all exist, so all five commits happen. The freeze-time behaviour is an accident that does not carry to a real PIN.)

### The one order that does pass, demonstrated

Fetch the five control commits into the lane and record them as **ancestors** of REV (`git merge -s ours`), so the tokens resolve and the ancestry test holds while REV's tree stays PIN's tree plus receipts. Built end to end in a scratch clone with the docs content, five control commits, and a REV whose tree adds only `control/*` (`receipts/d-demo-PASS.stdout`):

```
EXPLAIN arm1-selftest exit=0 14/14
EXPLAIN arm2-red54 exit=3 codes=RECEIPT_REV_CONTENT_DRIFT old-gate-accepted=True
EXPLAIN arm3-red54b exit=3 codes=RECEIPT_REV_UNRESOLVABLE
EXPLAIN arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT
EXPLAIN arm5-own exit=0 verdict=PASS
EXPLAIN arm6-docs 3/4
C2_R56: … own=PASS docs=3/4 total=1 C2_R56_PASS=false
```

`own=PASS` is reachable — but only by injecting control commits into the lane's ancestry, which the L1 must weigh explicitly (five commits whose own trees contain the mutated content: removed rekey entries, a fabricated reader hash, a standing row asserting 9, a gate without the binding arm, a fabricated red-before slice). They would be ancestors of the closing commit while absent from its tree; a reviewer reading `git log` sees the round's falsification fixtures in its history. That is a disclosure obligation, not a free win — and it still leaves D1 blocking `total=0`.

The same run also pins the other half of the constraint: editing a frozen-surface path after PIN breaks arm 5 (`receipts/d-demo2-alldocs.stdout`, `own=REFUSED`), because `controls-b` then names PIN while the certified REV drifts from it on `corpus/knowledge/receipt-revision-binding.md`. Any late docs fix after `controls.sh` re-runs costs arm 5.

## Defects (reported, not edited — the counter and gate are frozen)

### D1 — blocking, claim-killing: arm 6 reads `mined` from the wrong SOURCES column

measure.py:246 tests `cells[8] == 'mined'`. The registry header is
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`, so **`status` is `cells[7]`; `cells[8]` is `opened`.**

```
$ (over corpus/SOURCES.md at the freeze)
rows: 140   cell-count histogram: {11: 140}
cells[8]=='mined' (what the counter tests): 0
cells[7]=='mined' (the header's status column): 113
S001 cells: [0]S001 [1]source [2]docs [3]A [4]scope [5]anchor [6]teaches [7]mined [8]2026-10-19 [9]180d [10]used-by
```

The `mined` set is therefore always empty and `cited & mined` is always empty, so the knowledge sub-check can never add its point: `docs ≤ 3/4`, `total ≥ 1`, `C2_R56_PASS=false` at every revision. Proven, not argued: a note citing **every one of the 140 S-rows** still reads `docs=3/4` (`receipts/d-demo2-alldocs.stdout`), and the instrumented replication shows the other three sub-checks green and this one structurally dead (`receipts/arm6-predicates.txt`):

```
sub-check 1 QUALITY : gate named = True | refusal code present = ['RECEIPT_REV_CONTENT_DRIFT']
sub-check 2 NOTE    : trio = True | cites S-row = True
                    cited = ['001'] | mined set size = 0 | distinct cells[8] values = ['2026-10-19', '2026-10-20', …]
                    cited & mined = set() -> sub-check can never add a point
sub-check 3 SKILL   : receipt-revision-gate anywhere in SKILL.md = True
sub-check 4 REGISTRY: gate named = True | refusal codes present = 3
```

There is no conformant workaround. A row shaped so `cells[8]=='mined'` puts `mined` in the `opened` column, and the census rejects it (`receipts/census-mined-cell.txt`):

```
$ scripts/sources-census.sh validate --root <fixture> tameshi      # conformant rows
tameshi  ok  …/corpus/SOURCES.md                            exit=0
$ …plus '| S002 | … | mined | mined | 90d | — |'
tameshi  E08  S002 opened=mined
tameshi  W03  S002 mined but unused                         exit=1
```
`E08` → `census.exit≠0` → `deciding-run.sh` sets `rc=1`. Shifting the column the other way (`status`=date, `recheck`=mined) leaves `cells[8]` a date and still does not match. Placing such a row outside `## Registry` trips `E12`.

Proposed patch (diff text only; the counter is frozen):
```diff
-                if len(cells) == 11 and re.fullmatch(r'S\d{3,}', cells[0]) and cells[8] == 'mined':
+                if len(cells) == 11 and re.fullmatch(r'S\d{3,}', cells[0]) and cells[7] == 'mined':
```
With that token changed the demo tree would read `docs=4/4` and the claim would be reachable. This needs a contract amendment, not a seat edit.

### D2 — blocking, order-killing: arm 5's `control` role cannot accept `controls.sh`'s own output

Detailed in (d). `controls.sh` (frozen) emits five phase-A lines whose `rev=` names a commit made inside a throwaway clone; the gate's `control` role requires every token to resolve in the lane **and** be ancestral to REV. The planned order therefore ends in `own=REFUSED` / `DECIDING_REFUSED receipt-binding`.

Patch options, none available this round: (i) `controls.sh` should not run the mutation controls with `--rev "$(git rev-parse HEAD)"` of the mutated clone but should emit the verdict **without** a rev token (or with PIN plus a `clone=` field the gate does not parse); (ii) the gate's `control` role should ignore unresolvable revs on lines it cannot attribute to the lane. Either is a re-freeze. The only in-round route is the ancestry injection demonstrated above.

### D3 — minor: `RECEIPT_DIGEST_MISMATCH` is unreachable inside the counter

The freeze commits `c2/red-before/round-54-ctl-pos-c1.stdout.sha256`, and the gate checks a `<receipt>.sha256` sidecar, but the counter copies only the receipt into `--work` and never the sidecar, so no arm can ever trip the code (`receipts/sidecar-reachability.txt`):

```
$ ls -1 <work>            r54-controls-b.stdout r54-ctl-pos-c1.stdout r54-surface.paths r55-c2.stdout receipt-revision-gate.py
$ sha256sum rec/slice.stdout              3310ff60…db455698
$ frozen sidecar bytes                    3310ff60…db455698      (they match; the counter just never looks)
$ gate with a sidecar beside the receipt  codes=RECEIPT_DIGEST_MISMATCH verdict=REFUSED   (the path exists)
```
Consequence: the contract's `cannot_see` says "the digest sidecar narrows but does not close that gap" — in the counter as frozen it narrows nothing. The digest narrowing the report claims does not exist; say so or copy the sidecar beside the receipt.

### D4 — minor: arm 6's three text sub-checks are weaker than their stated obligation

The docstring says "the SKILL.md `## Standing rules` section names `receipt-revision-gate`"; the code tests `'receipt-revision-gate' in skill` over the whole file. Likewise QUALITY accepts the gate path and one refusal code anywhere in the file, and the registry accepts the path plus any three codes anywhere. A passing mention in an unrelated section satisfies all three. The C2 content seat's rule must therefore be placed where a reader meets it by discipline, not by the counter — the counter will not catch a rule parked in the wrong section.

### D5 — note, not a defect: arm 2's docstring understates its own drift set

The docstring says the refusal names the cold-read ledger; the gate names six paths, and the ledger is not load-bearing (M2b). Worth correcting in the round's records so the lesson does not claim a single-path defect where the receipt drifts from the certified revision on six.

## Cross-check worth carrying to the L1

`deciding-run.sh` gate 0 accepts a control set by grepping for the **presence** of `CONTROLS_A: n/m as pre-registered`, not for `n == m`:

```
grep -q '^CONTROLS_A: [0-9]*/[0-9]* as pre-registered' "$LANE/$E/control/controls-a.stdout"
```
A `CONTROLS_A: 0/7` set passes that gate. That is the R55.4 class (a control sentence that asserts nothing) one level up, and it is the reason the `own` arm's refusal — not the deciding gate — is the only thing that would catch a vacuous phase A. It is also an argument against the "let the mutations no-op" escape for D2: it would satisfy the deciding gate while controlling nothing.

## Files changed by this seat

Only deliverables, no lane production file and no frozen instrument:

- `.ufo/waves/round-56/w1/T56W1ExecC2Counter.md` (this report)
- `.ufo/waves/round-56/w1/T56W1ExecC2Counter.json`
- `.ufo/waves/round-56/w1/T56W1ExecC2Counter-receipts/` (28 files, listed in the JSON)

## What the L1 should do next

1. Treat C2's target as **unreachable as frozen**: D1 caps `docs` at 3 and D2 refuses `own` under the planned order. Decide explicitly between a contract amendment (fix `cells[8]`→`cells[7]` and either the `controls.sh` emit shape or the gate's `control` role, then re-freeze) and closing C2 `false` with both defects named.
2. If the round proceeds without an amendment, the only order that reaches `own=PASS` is the ancestry injection in (d); it must be disclosed in the LOG as five control commits in the lane's ancestry, and it does not change `total≥1`.
3. Freeze the surface discipline in the wave-2/3 plan: after `controls.sh` runs at PIN, no edit to any of the ten `frozen-surface.paths` entries may land before REV, or `own` drops to `RECEIPT_REV_CONTENT_DRIFT` (`d-demo2-alldocs.stdout`).
4. Do not cite the digest sidecar as narrowing anything (D3) and do not rely on arm 6 to police *where* the rule is written (D4).
