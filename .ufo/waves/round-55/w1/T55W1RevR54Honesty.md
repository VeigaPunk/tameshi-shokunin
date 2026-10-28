# T55W1RevR54Honesty — the round-54 spotcheck as a claim set, and whether round 55's corrections are faithful

seat: `T55W1RevR54Honesty` (reviewer, round 55, wave 1)
item: treat `corpus/lessons/round-54-verifier-spotcheck.md` as a claim set — for each R54.N, does the quoted receipt text exist **verbatim** and is its **count** right; where does the spotcheck itself overreach; are the round-55 corrections faithful to what the receipts say.
lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
base (spotcheck claims): `0a2010acd1e92e4e332774050825e21bcfc7e079`
frozen round-55 counter set: `631cd6455e58dce969310b4c0466c3383d9f5108`
scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1RevR54Honesty` (clone `--shared` of the lane, detached at `631cd64`; fixture commits only inside the clone, `git rev-parse --show-toplevel` asserted equal to the clone before each)
tooling: none installed; nothing added to any PATH directory.
receipts: `.ufo/waves/round-55/w1/T55W1RevR54Honesty-receipts/`

No lane production file was edited. Findings marked **FROZEN** concern files I may not
touch (the round-55 counter set); they are reported, not fixed.

---

## 0. Snapshot discipline (the tree moved under me)

All spotcheck claims are checked against the **committed** bytes at `0a2010ac` (immutable).
The round-55 corrections are uncommitted and siblings were editing them during this pass,
so every statement about the working tree names the sha256 I read:

| file | sha256 at 14:03:13 −03 (final snapshot) |
|---|---|
| `SCORECARD.md` | `22b9fffd0109b5490a432c91970279c8438204b6618fafd3ef22dda8959c75ce` |
| `corpus/QUALITY.md` | `b4e6eabbe9346c9bc418540e336f460c6710c7bc073ce995675ee9eec0de576a` |
| `corpus/lessons/round-54.md` | `e0eeb6a392dac1a27cdf27772f3c2041bfcab426a60453404034754e551b5970` |
| `LOG.md` | `4482f48a5a778acb2a36065602d3a9d239af30d0d8cd33618b90783a35bd66d1` |
| `.ufo/evidence/round-55/c1/measure.py` | `711507e7b5bdd060a67b42162d043aabaef339408b3291a3c6ca39599d566dcd` |

An earlier snapshot (13:55) differed in two places that matter below; both are quoted with
their bytes, because what a sibling fixed at 14:00 is itself evidence of what the record
said at 13:55.

---

## 1. Per-class verification: quote verbatim, count right

Verified against `0a2010ac`. "verbatim" = the quoted fragment appears in the named file's
committed bytes with no word changed; ellipses are the spotcheck's own.

| # | the spotcheck's quote | verbatim | count/claim right | receipt |
|---|---|---|---|---|
| R54.1 | `CTL CTL_POS_c1 … c0=99c3bc88d704 credited=60 lost=4 rekeyed=3/7 readers=6/7 … C1_R54_PASS=false`; `CTL_MISMATCH CTL_POS_c1 expected=true actual=false`; `CONTROLS_B: 2/3 as pre-registered`; exit 1 | **yes** | **yes** — `controls-b.exit` is `1`; four files carry the opposite claim (report `:162`, `SCORECARD.md:2583`, `QUALITY.md:1590`, lesson `:74,101`), all located | `r54.1-controls-b.txt` |
| R54.2 | `7883e0e5` "the freeze pointer the deciding run uses"; `fe70474d` (amendments 1-5); `097985c1`; receipt `freeze=077d431e`, 5 amendments | **yes** | **yes**, with one attribution caveat (F6 below): `7883e0e5` has 7 files/1 amendment, `fe70474d` 10/4, `097985c1` 10/2, `077d431e` 10/5 | `r54.2-freeze.txt` |
| R54.3 | `SCORECARD.md:2584` `total=14`; the receipt prints `total=13` | **yes** | **yes** — `before/c2.stdout` and the contract's `C2.before` both print `total=13`; no receipt anywhere prints `14` | `r54.3-total13.txt` |
| R54.4 | report cites `d7749f84` (c1) and `49280fe5` (c2); `freeze.json` pins `8528ee85` | **yes** | **yes in substance**; `49280fe5` is the sha256 at `19c7558`/`7e533b1` (regex `mkdir(?:at)\(`), `8528ee85` at `077d431e` (regex `mkdir(?:at)?\(`) — but it is a **sha256 digest, not a "blob"** (F-O3) | `r54.4-digest.txt` |
| R54.5 | report `:62` "25 findings"; `:79,100` "22 findings in 9 … nine sections"; committed readers 28 / 25-in-12; `resolutions.json` 12/25; ledger 25 over 12 | **yes** | **yes** — w1 28 findings over 23 reports (28 distinct quotes), w2 25 over 12 of 23, `resolutions.json` 12 entries/25 findings, ledger `minor_gaps` 0×11,1×8,2×3,11×1 = 25 over 12 entries. The 28 is **not** inflated by receipt JSON: the 9 `-receipts/*.json` under `w1/` carry no `findings` key | `r54.5-counts.txt` |
| R54.6 | 3 untracked seat deliverables; `after/clean-tree-after.txt` shows `??` | **yes** | **yes** — `ff2a821` adds exactly those three (`A`, byte-identical); all 47 `w2-registry.json` items have a committed top-level `.md` (47/47) | `r54.6-sweep.txt` |
| R54.7 | `7fa9a5e` renames (`R100`) the forged reader into the receipts dir; path fails arm 4; `b90c1f79` matches no section | **yes** | **yes for the w2 file** — `R100` confirmed. Mechanism is narrower than stated: see **F-O2** | `r54.7-forged.txt` |
| R54.8 | seat `:324` scope note asserts "on the operator's direct instruction in-session, which is the higher authority"; `config.yml:418` now `scout: "@m_grok"`; lesson has no `config.yml` | **yes** (the quoted words start on `:325`, the scope note opens on `:324`) | **yes** — the host line reads `scout: "@m_grok"`; `git grep config.yml` on `corpus/lessons/round-54.md@0a2010ac` returns nothing | `r54.8-config.txt` |
| R54.9 | `role_mix` reviewer 5, sum 76; `attack_seats` 21 → 27.6 %; report itemizes 75 seats with 4 reviewers and 26.3 %; 81 staged `.md` | **yes** | **yes** — `role_mix` sums to 76; the report's itemization sums to 75 (it is one reviewer short); `find merge/tameshi/knowledge -name '*.md'` = 81 | `r54.9-wave.txt` |
| R54.10 | report quotes `CTL_R53 (… 58/64, rekeyed=0/30)` to `controls-a.stdout`; that file prints `rekeyed=0/7`; `0/30` belongs to `r53-counter-at-88afa941.stdout` | **yes** | **yes** — report `:51-52`; `controls-a` `CTL_R53 … rekeyed=0/7`; the r53 receipt `C1_R53: … rekeyed=0/30 … total=37` | `r54.10-ctl-r53.txt` |

Step-1 rows I also re-derived: the ten commits are 10/10 ancestors of `0a2010ac`; readers are
23 w1 at `cand=59c38109…` and 23 w2 at `cand=99c3bc88…`; the `delta-debugging-minimization-contract.md`
entry is present at base (added `79f44b5`) (`spotcheck-adjacent.txt`, `counter-stale-arms.txt`).

**Verdict on the claim set: ten of ten quoted receipts and counts hold.** The defects the
spotcheck routed are real, pinned to committed bytes, and its own arithmetic is accurate —
including in exactly the place the trap would be easiest (the w1 finding count excludes the
receipt JSONs and the forged reader).

---

## 2. Where the spotcheck itself overreaches

### F-O1 (medium) — an "all revisions" claim that is false twice
R54.1, line 107: `.ufo/evidence/round-54/control/controls-b.stdout` is described as
"**(committed, unchanged across all 5 revisions that touch it)**".

Measured (`r54.1-revisions.txt`):

```
git log -- .ufo/evidence/round-54/control/controls-b.stdout  →  2 commits (7fa9a5e, 5564954)
7fa9a5e → blob 8333e8ce6fb07f627cb4f42cf0dafc24b3e7b83f
5564954 → blob d910366b5f89760c1d47bed7d7570c11a6992a58
```

`5564954` **appends** two lines ("receipt re-stated at the round-54 freeze `077d431e` (bytes
unchanged; the verdict line above stands)"). So "5 revisions" is wrong (2) and "unchanged" is
wrong (the blob differs). The spotcheck reproduced the receipt's own self-assertion instead of
measuring it. The substance is unaffected — the four verdict lines are byte-identical across
both blobs — but the parenthetical is an unmeasured all-revisions claim of exactly the kind
the spotcheck is routing elsewhere (R54.1's subject).

### F-O2 (medium) — "it never credited and cannot" is proved for the w2 file, but the mechanism it names does not protect the lane's other forged artifact
R54.7, line 120: "It never credited and cannot: **the path fails arm 4's
`/T54W\d+.*Read.*\.json$/`** and its `section_sha256` (`b90c1f79…`) is not the genuine
reader's (`61736dce…`) nor any section at `c0`."

Both halves are true of `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json`. But
the lane carries a **second** forged artifact that the spotcheck never opens:
`.ufo/waves/round-54/w1/T54W1Sent01-receipts/lane-forged-report-T54W1ReadForged.json`
(`r54.7-forged.txt`):

```
arm-4 regex /T54W\d+.*Read.*\.json$/:
  True   w2/.../forged-reader.json                      (before the rename: also True)
  True   w1/.../lane-forged-report-T54W1ReadForged.json
w1 forged file: cand = 59c38109bf11… (= c0, exactly what arm 4 requires),
                section_sha256 = 9942353c… (c0 "## Standing rules" = 16439027…, c1 = 61736dce…)
```

So for that file the path test **passes** and the `cand` test **passes**; it is excluded only
by the hash. The spotcheck's "cannot" is correct for the file it names, but it presents the
path test as the guard, and the lane's similarly-forged w1 file is not mentioned in a report
whose header claims "the forged-file incident … named". A reader who trusts the stated
mechanism would conclude the class is closed by naming, when it is closed by hash. (It is
genuinely closed — `9942353c` matches no section at `c0`, and round 55's R54.5 regex
`[A-Za-z]*Read\d+` does not even admit the name — but the reasoning given is not the reason.)

### F-O3 (low) — terminology: `49280fe5` is a digest, not a blob
R54.4 calls it "the **pre-amendment-4 blob**". `freeze.json` pins **sha256** digests;
`49280fe55b93…` is the sha256 of `c2/measure.py` at `19c7558`/`7e533b1`, whose **git blob** is
`16302ef26b0d…`. The diagnosis, the two commits it names, and the regex it quotes are all
right (`r54.4-digest.txt`).

### F-O4 (low) — a count that omits a receipt class (checked, and it is not a defect)
Step-1 row, line 26: "`git status --porcelain` → **3** untracked". The deciding run's own
`after/clean-tree-after.txt` prints **four** `??` lines — the fourth is
`?? .ufo/evidence/round-54/after/` itself, i.e. the receipt directory that later became
`4fe57df`. Two different moments, both correctly stated; recorded here so no later reader
"corrects" the 3. **No finding.**

### F-O5 (informational) — the four places R54.1 names are four *files* but five *locations*
The lesson's false claim is at `:74-75` (wording "proves the arm on the positive control …
requires `rekeyed=7/7`") **and** `:101` ("proven live by the positive control (`CTL_POS_c1`,
which prints `rekeyed=7/7`)"). The spotcheck quotes only the `:101` wording in its parenthetical,
so a corrector following the quote fixes one of the two. This is the seam that F3 below
actually opened.

---

## 3. Are the round-55 corrections faithful to what the receipts say?

Re-derived at `0a2010ac` and against the frozen round-55 counter. **Values: ten of ten
faithful.** Every "Corrected" value in `SCORECARD.md` `## Round 55 - round-54 record
corrections` matches an independent derivation from the tree:

| ER | corrected value in the section | independent derivation | agrees |
|---|---|---|---|
| ER-R54-1 | `CTL_MISMATCH`; `expected=true actual=false`; `CONTROLS_B: 2/3`; cause = phase B cloned the freeze, which predates the re-key | `controls-b.stdout` verbatim; `077d431e` is an ancestor of `7fa9a5e` (the re-key commit) | yes |
| ER-R54-2 | one pointer `077d431e` (5 amendments), "what the deciding receipt prints", receipt `after/frozen.stdout` | `frozen.stdout` prints `freeze=077d431e…`; **the amendment count is in `freeze.json`, not in that receipt** (F6) | yes, pointer wrong (F6) |
| ER-R54-3 | `total=13`; receipt `before/c2.stdout`; "and the contract's own `before` text" | both print `total=13` | yes |
| ER-R54-4 | `8528ee85` — "the amendment-4 bytes that decided"; receipt `freeze.json` key `c2/measure.py` | key present, value `8528ee8555da…`; tree at `c2108100` hashes to it | yes |
| ER-R54-5 | `w1=28 w2=25 sections=12`, "`-receipts/` JSON excluded" | 28 / 25 / 12, receipts carry no findings key | yes |
| ER-R54-6 | committed; sweep `ff2a821` | `ff2a821` adds exactly the three | yes |
| ER-R54-7 | renamed at `7fa9a5e` (`R100`); "can never credit" | `R100` confirmed; hash matches no section | yes (mechanism note F7) |
| ER-R54-8 | recorded in `corpus/lessons/round-55.md`; seat file marked superseded; `config.yml` reads `@m_grok` again | lesson-55 `:62` names it; the seat diff appends a `SUPERSEDED (round 55, ER-R54-8)` block and leaves the original text visible; host line is `scout: "@m_grok"` | yes |
| ER-R54-9 | `reviewers=5 attack=21/76 seats=76`; `staged=81` | registry sums to 76, reviewer 5, attack 21; `find … knowledge -name '*.md'` = 81 | yes |
| ER-R54-10 | `controls-a.stdout` prints `rekeyed=0/7`; `0/30` belongs to `r53-counter-at-88afa941.stdout` | both confirmed | yes |

The corrections are therefore **faithful in value and correctly receipted**, with two
pointer-level exceptions (F6, F7). What follows is about *application* and about the
instrument that scores it — and one of these is a live blocker.

### F1 (high, **FROZEN**) — the frozen/amended C1 counter fails R54.1 on the *truthful* correction
Running the round-55 C1 counter over a clone carrying the working-tree record files
(`r55-live-c1.txt`, candidate `e7587ce4`, counter sha `711507e7`) gives:

```
EXPLAIN R54.1 FAIL premise=ok corrected=ok stale=3 derived=CTL_MISMATCH + 2/3
EXPLAIN R54.1 stale: corpus/lessons/round-54.md:75: (`rekeyed=7/7`); the pre-registered positive control was cloned at the freeze
EXPLAIN R54.1 stale: corpus/lessons/round-54.md@4293: …(`rekeyed=7/7`); the pre-registered positive control was cloned at the f
EXPLAIN R54.1 stale: corpus/lessons/round-54.md@5821: …and the arm prints `rekeyed=7/7` at the deciding revision; the pre-registered positive control was cloned at the f
C1_R55: rev=e7587ce4fe01 classes=10 premise=10/10 stale=1 classes_corrected=10/10 total=1 C1_R55_PASS=false
```

All three hits are on **true statements**:

- `corpus/lessons/round-54.md:73-78` now reads "the arm's own count is read at the deciding
  revision (`rekeyed=7/7`); the pre-registered positive control was cloned at the freeze
  commit, printed `CTL_MISMATCH` (`rekeyed=3/7`) and therefore never fired" — exactly what
  `controls-b.stdout` says;
- `:106-107` (the R53.1 disposition) says the same thing in one line.

The stale predicate is token proximity:
`(positive control[^\n]{0,160}rekeyed=7/7)|(rekeyed=7/7[^\n]{0,160}positive control)`, and the
amendment added the whitespace-normalized twin `scan_span`. Any sentence that honestly puts
the deciding revision's `rekeyed=7/7` before "positive control" — the only natural order —
trips it.

The same predicate in the **frozen** bytes (`631cd64`, sha `77abe1e9`) was line-local, so it
missed the false claim while it was split across `:74-75`. Reproducible proof
(`r55-frozen-blind.txt`): the base lesson `0a2010ac` carries the R54.1 falsehood **twice** —
`:74-75` ("proves the arm on the positive control CTL_POS_c1, which / requires `rekeyed=7/7`")
and `:101` ("proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`)"),
both on the record at 13:55 after the wave had fixed `:101` only. Run the frozen counter over
that record with the current corrections present:

```
EXPLAIN R54.1 stale: corpus/lessons/round-54.md:101: proven live by the positive control … `rekeyed=7/7`.
EXPLAIN R54.1 FAIL … stale=1        (no hit at :74-75 — the split-line falsehood is invisible)
```

That is the first candidate run at 13:55 in one line: with `:101` corrected, `R54.1` printed
`stale=0` while `:74-75` still lied (rev `cfa1b48f`, in-session; the reproducible fixture is
what the receipt holds). The amended bytes then flag the *corrected* text three times.

So the arm is wrong in both directions with one cause: it tests that two tokens sit near each
other, not that the assertion is the wrong one. A pass can be earned by a falsehood split
across a line break; a failure can be incurred by the truth. **This is not mine to fix** (the
counter is in `frozen_paths`). The L1 has two live choices, both of which the record should
name: re-word the correction so the two tokens never share a 160-character window (satisfies
the counter without changing a fact — but then the arm still cannot tell truth from
falsehood), or amend the counter's R54.1 stale arm to a claim-shaped pattern (e.g. the old
"proven live by"/"proves the arm" phrasing with the value, which is what R54.1 actually
alleged) and re-freeze. As it stands `C1_R55_PASS=false` at the working-tree record.

### F2 (high, **FROZEN**) — the freeze manifest does not match the tree it would certify
At 14:02:57 (`r55-frozen-state.txt`) three of the six hashed paths disagree with
`freeze.json`, and the amendment list records three entries `[1,2,3]` where the earlier
snapshot recorded four:

```
MISMATCH contract.json   pin ed6871e17697  tree 5de4f37b14db
MISMATCH c1/measure.py   pin 77abe1e9daf4  tree 711507e7b5bd
MISMATCH c2/measure.py   pin ab3ae7514691  tree d6ca1d851bb0
MATCH    no-harm.sh / deciding-run.sh / controls.sh
```

The deciding script's `FROZEN_UNCHANGED` gate compares exactly these; at this snapshot it
cannot pass. Re-checked at 14:05:49 with identical hashes and still `[1,2,3]`, so this is not
a momentary write-in-progress: it is a standing mismatch that must be closed before the
deciding invocation. The c1 amendment is also **undisclosed**: adding `scan_span` to R54.1
and `LOG.md` to `RECORD` changes a predicate's reach, which is not "discovery plumbing only",
and the amendment text should say so.

### F3 (medium) — the corrections section's own claims were unearned at the snapshot they were written
Working tree at 13:55, `SCORECARD.md` `2626-2629`:

> "The same corrections were applied in place above so that the lane's record reads true where
> a reader meets it; this section is the only place where the old values are quoted"

At 13:55 that was false in three places I measured, and none of them is scanned by any stale
arm of the frozen counter:

```
corpus/lessons/round-54.md:74  "…proves the arm on the positive control CTL_POS_c1, which / requires `rekeyed=7/7`"
LOG.md:2500-2501               "amendment 1 at `7883e0e5` … — the freeze pointer the deciding run uses"
LOG.md:2508-2509               "C1 `99c3bc88` (25 / wave-1 reader findings adjudicated and fixed"
```

A sibling fixed all three between 13:55 and 14:03 (`LOG.md` now: "the round's one freeze
pointer is `077d431e`", "C1 `99c3bc88` (28 wave-1 reader findings"; lesson now reads the true
pairing). At the final snapshot my sweep over `SCORECARD.md` (corrections excluded),
`corpus/QUALITY.md`, `corpus/lessons/round-54.md`, `LOG.md`, `SKILL.md` for all eight
wrong-assertion shapes returns **none**. So the claim is true *now* and was not true when
written — which is the honest statement, and the round should not describe the in-place pass
as complete without naming that it was finished by a second editor.

### F4 (medium) — six of ten C1 classes have no stale arm at all; `LOG.md` was outside `RECORD`
From the frozen bytes (`counter-stale-arms.txt`):

```
R54.1  stale = scan(RECORD, CTL_POS_c1 true) + scan(QUALITY,lesson54, proximity)
R54.2  stale = scan(SCORECARD.md, 7883e0e5|fe70474d)          ← SCORECARD only
R54.3  stale = scan(SCORECARD.md, total=14)
R54.4  stale = []   R54.5 stale = []   R54.6 stale = []   R54.7 stale = []
R54.8  stale = []   R54.9 stale = scan(lesson-54, 84 staged)  R54.10 stale = []
RECORD = (SCORECARD.md, corpus/QUALITY.md, corpus/lessons/round-54.md)   ← no LOG.md, no SKILL.md
```

The contract's C1 target is "zero stale hits outside the corrections section" for **every**
class. The counter measures that for four classes, two of them on one file. `49280fe5`
(R54.4), the `25`/`22` counts (R54.5), `deletion lands in 7fa9a5e0` (R54.7), and the
`0/30`-under-`controls-a` pairing (R54.10) could each stand anywhere in `LOG.md`,
`SKILL.md`, the wave reports or the fleet report and the class would still print `stale=0`.
My sweep found no live survivors (the wave fixed them), but that is a fact about the tree,
not something the instrument established. The live counter now adds `LOG.md` to `RECORD` and
`scan_span` to R54.1 only — R54.2's pointer scan is still `SCORECARD.md`-only, so the
`7883e0e5` line F3 found in `LOG.md` would still have escaped.

### F5 (low) — ER-R54-1's "Old:" enumeration is three of the four places
The section lists the claim row, the QUALITY falsifier and the lesson's `:101` wording. It
omits the fleet report `:162` ("proven live by the phase-B positive control") and the
lesson's `:74` wording. The fleet report is outside the lane, so this is a scope statement
that should be made explicitly ("the fleet report still carries it; no lane edit can reach
it"), not silence.

### F6 (low) — ER-R54-2's receipt pointer does not carry the amendment count
"Corrected: one pointer, `077d431e` (5 amendments), which is what the deciding receipt prints.
Receipt: `after/frozen.stdout`". That receipt prints `FROZEN_UNCHANGED=1 freeze=… rev=…` and
nothing about amendments (`r54.2-freeze.txt`: `grep -c amendments` → 0). Cite `freeze.json`
for the `5`, the receipt for the pointer, or say "the deciding receipt and the manifest".
The same over-attribution is in the spotcheck's R54.2 ("The receipt says … with 5 amendments").

### F7 (low) — ER-R54-7 repeats the path-only mechanism, and the exclusion mechanism has since changed
"It can never credit: **its path fails the reader pattern** and its `section_sha256` matches no
section" — same narrowness as F-O2, now inherited into the lane's own record. Separately,
round 55's R54.5 counter uses `/T54W\d+[A-Za-z]*Read\d+\.json$/`, which is *not* round 54's
arm-4 regex `/T54W\d+.*Read.*\.json$/`; that difference is what actually excludes
`ReadForged.json` from the count and it is nowhere stated.

### F8 (low) — the frozen C2 `before` receipt was replaced, not preserved
`.ufo/evidence/round-55/before/c2.stdout` at `631cd64` is 43 lines of per-mode `EXPLAIN`
output; the working tree holds one line (`C2_R55: rev=0a2010acd1e9 … total=18 …`). The
`LOG.md` round-55 entry still cites that file for "`repeat-control` and `context-capture`
printed the raw exception type (and `context-capture` printed on stdout)" — evidence the
trimmed receipt no longer contains. Either append the re-run and keep the original, or make
the LOG sentence cite `631cd64:before/c2.stdout` explicitly. (Out of my item's subject; noted
because it is the same class of receipt-fidelity defect the round is routing.)

---

## 4. Findings by severity

| id | sev | finding | frozen? |
|---|---|---|---|
| F1 | high | C1's R54.1 stale arm fails on the truthful correction (3 hits, `total=1 PASS=false`); caused by token-proximity matching, not claim matching | **yes — report only** |
| F2 | high | `freeze.json` pins mismatched for `contract.json`, `c1/measure.py`, `c2/measure.py`; the c1 `scan_span` change is an undisclosed predicate change | **yes — report only** |
| F-O2 | medium | spotcheck's "cannot credit" names the path test; the lane's other forged artifact (`T54W1ReadForged.json`) passes the path test and `cand`, and is excluded only by its hash — unmentioned | no (record text) |
| F3 | medium | corrections section's "applied in place / only place old values are quoted" was false at 13:55 (3 live stale assertions incl. `LOG.md`); repaired by a later editor by 14:03 | no (record text) |
| F4 | medium | 6/10 classes have no stale arm; `LOG.md`/`SKILL.md` outside `RECORD`; contract's "zero stale hits" target not measured for them | **yes — report only** |
| F-O1 | medium | R54.1's "unchanged across all 5 revisions that touch it": 2 revisions, different blobs | no (spotcheck text) |
| F6 | low | ER-R54-2 attributes "5 amendments" to `after/frozen.stdout`, which prints no amendment count | no |
| F7 | low | ER-R54-7 path-only mechanism; R54.5's regex differs from arm 4's and the difference is unstated | no |
| F5 | low | ER-R54-1 omits the fleet report `:162` and the lesson `:74` wording from its "Old:" list | no |
| F-O3 | low | R54.4 calls a sha256 a "blob" | no (spotcheck text) |
| F8 | low | the C2 `before` receipt was replaced (43 → 1 line) while `LOG.md` still cites its per-mode content | no |

None of these overturns the spotcheck's ten routed defects: every one of them is real, and
round 55 has corrected every value from the tree. The two high findings are about the
instrument that certifies the correction, not about whether the correction is true.

---

## 5. Residual risk and verification gaps

- **Concurrency.** The lane's working tree changed under this pass (a sibling added
  `scan_span` and `LOG.md` to the counter and repaired `LOG.md` and the lesson between 13:55
  and 14:03). Every working-tree statement above is pinned to a sha256 in §0; a later edit
  can invalidate F3's and F8's live form without invalidating the observation.
- **Not re-executed:** the round-54 C1/C2 counters at `d33053f7`/`c2108100`. I re-derived
  their claims from committed receipts and from the committed reader/registry/ledger files;
  the spotcheck's own runs and the closure's receipts are treated as evidence. My item did
  not require re-running them.
- **Not in scope:** the C2 claim, the wave's 75-vs-76 seat count in the round-55 LOG entry,
  and whether `--contract`'s grammar is correct. Flagged only where they touch a class here.
- **Census:** not re-run by me; it is the L1's gate (139 rows expected).
- **Fleet report** read at `fcb8d8db` (the only commit touching it). Line citations there
  (`:51-52`, `:62`, `:79`, `:100`, `:157`, `:162`) are to that file, which is outside the
  lane — no lane edit can correct it.
- The spotcheck's own "reads: 46 reader files … 0 mismatches" is consistent with what I
  measured for `cand` (23+23) but I did not re-verify all 46 `section_sha256` values against
  46 sectionizations; I verified the two forged files and the `## Standing rules` values
  (`c0` `16439027…`, `c1` `61736dce…`) that the R54.7 argument rests on.
