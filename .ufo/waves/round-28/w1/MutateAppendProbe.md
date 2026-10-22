# MutateAppendProbe — round-28 wave 1

**Role:** mutation-tester (leaf member, no subagents dispatched).
**Item:** reproduce lesson round-28 Mistake 1 (one blank-line append to a widely read
lane file de-credits cold-read sections) independently in /tmp clones at
`b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a`, and confirm for the L1 whether
SCORECARD.md, LOG.md and the lesson file can be appended after the cold reads
without any drop.

---

## Verdict

1. **The committed receipt `.ufo/evidence/round-28/append-probe.txt` is honest and
   reproducible — at the base it names (`06b59b93`).** My independent clones
   reproduced every number in it exactly (SOURCES 60→50, README 60→55,
   QUALITY 60→57, SHONEN 60→59, LOG 60→60, SCORECARD 60→60).
2. **Its per-file numbers do not transfer to the landed head `b05d2ee`.** At
   `b05d2ee` the baseline is already `covered=50/64` (14 sections uncovered,
   10 of them from the round's own `corpus/SOURCES.md` edit), and the per-file
   append effects are different: SOURCES 50→50, README 50→48, QUALITY 50→50,
   SHONEN 50→49, LOG 50→50, SCORECARD 50→50, lesson file 50→50, ledger 50→50.
   A reader who quotes the base-06b59b93 table as a property of the landed head
   will be wrong about SOURCES (0 drop, not 10) and QUALITY (0 drop, not 3).
3. **Critical for the L1:** at `b05d2ee`, against the ledger that exists today,
   SCORECARD.md, LOG.md, `corpus/lessons/round-28.md` and the round-21 ledger
   **can** all be appended with **no drop** (50/64 → 50/64, restored 50/64).
   But that is a property of the *current* round-21 entries, not a guarantee.
   A synthetic fresh round-28 entry that records one of those files in its
   `inputs` loses its section the moment the file is appended (51→50 in four
   independent synthetic cases). The wave exception ("never open them under the
   trace collector or by path") is exactly what makes the append safe — it is
   the load-bearing condition, not a formality.
4. **The ledger append can be made neutral and is safe, but only as a
   whitespace-level change.** A single trailing newline keeps the JSON valid
   and keeps `covered=50/64`. A single extra byte that breaks JSON parsing
   collapses the monitor to `covered=0/64` (total loss, exit 1).
5. **Files that must not be appended after the fresh reads:** `corpus/SOURCES.md`,
   `corpus/README.md`, `corpus/QUALITY.md`, `SHONEN.md`, and any file a fresh
   read records as an input. README and SHONEN already cost coverage at
   `b05d2ee` (README −2, SHONEN −1) with today's ledger alone; SOURCES and
   QUALITY will cost coverage once the fresh round-28 entries record them.

**Baseline failure disclosure:** the frozen counter exits **1** in every
pristine, mutated and restored run at `b05d2ee` (`covered=50/64 restraint=6
box3_mismatch=1`, target is `64/64 restraint=8 box3_mismatch=0`). Exit code is
therefore an **inconclusive** detector here — a baseline failure is not a killed
mutant. My detector is the **covered count** (and the uncovered-section set),
which moves and is restored exactly. The claim under test ("a blank-line append
de-credits cold-read sections") is **not falsified**: it holds at the base it
names and still holds at the landed head for README and SHONEN.

---

## Reproduction procedure

Every probe ran in its own throwaway clone under `/tmp/mutappend/`. The lane
repo was never written to; no `jj` command was run anywhere; the only git
commands inside the lane were read-only (`show`, `log`, `status`, `diff`).

```
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/mutappend/work-<tag>
git -C /tmp/mutappend/work-<tag> checkout -q b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a
# pristine
python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/mutappend/work-<tag> --rev HEAD
# mutate: one blank line
printf '\n' >> <target>
git -C ... add <target> && git -C ... commit -m "probe: append blank line to <target>"
# mutated
python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/mutappend/work-<tag> --rev HEAD
# restore exact bytes
git -C ... checkout -q b05d2ee... -- <target> && git -C ... commit -m restore
python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/mutappend/work-<tag> --rev HEAD
```

Restoration evidence: sha256 of every target file after restore equals the
sha256 before the mutation, for all eight targets (table in §2), and the
restored counter output equals the pristine output in every case.

---

## 1. The table the L1 asked for — file → covered count at `b05d2ee`

Pristine baseline at `b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a`:

```
C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a
```

(The 14 uncovered headings at the base are the round-27 four
`no-ledger-entry` sections 883 / 1069 / 1499 / 1964 plus ten
`input-drift:corpus/SOURCES.md` sections 131, 921, 1479, 1517, 1548, 1563,
1609, 1814, 1925, 1938 — the round's own SOURCES edit.)

| appended file | covered pristine | covered mutated | covered restored | drop |
|---|---:|---:|---:|---:|
| `corpus/SOURCES.md` | 50/64 | 50/64 | 50/64 | 0 |
| `corpus/README.md` | 50/64 | **48/64** | 50/64 | **−2** |
| `corpus/QUALITY.md` | 50/64 | 50/64 | 50/64 | 0 |
| `SHONEN.md` | 50/64 | **49/64** | 50/64 | **−1** |
| `LOG.md` | 50/64 | 50/64 | 50/64 | 0 |
| `SCORECARD.md` | 50/64 | 50/64 | 50/64 | 0 |
| `corpus/lessons/round-28.md` | 50/64 | 50/64 | 50/64 | 0 |
| `.ufo/evidence/round-21/coldread/ledger.json` (one trailing newline) | 50/64 | 50/64 | 50/64 | 0 |

Raw counter lines (mutated runs):

```
sources   C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=13f72c92fcab0b29dd46e98d9808d530b82621ed
readme    C1_MONITOR: covered=48/64 restraint=6 box3_mismatch=1 depth_score=9 rev=49c0d3c4584e238cab7dcc055daa27f9550727c2
quality   C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=402eef715db362787b07a57f255e0e60bb099720
shonen    C1_MONITOR: covered=49/64 restraint=6 box3_mismatch=1 depth_score=9 rev=613e74fb8842e61c8764662b2e05bff27caee341
log       C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=c2c99a6ce1bb952841f59f30733decc72aa8a370
scorecard C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=d232417c232c2a5607e0acb0f0b5a26b4ebc8142
lesson    C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=c43f2b2b0ef340d00a96a4af20f050389940ea7f
ledger    C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=b3d65f78a42be3975477a309595866fd6bc98476
```

Every mutated run and every restored run exited 1 (baseline already fails; see
disclosure in the verdict).

Which sections move (from `--explain` runs):

* `corpus/README.md` append → sections **375** and **1380** fall out of credit
  (new uncovered set: 131, 375, 883, 921, 1069, 1380, 1479, 1499, 1517, 1548,
  1563, 1609, 1814, 1925, 1938, 1964).
* `SHONEN.md` append → section **1754** falls out of credit (new uncovered set:
  131, 883, 921, 1069, 1479, 1499, 1517, 1548, 1563, 1609, 1754, 1814, 1925,
  1938, 1964).
* SOURCES, QUALITY, LOG, SCORECARD, lesson file, ledger → uncovered set
  unchanged from pristine.

### 2. Before / after / restored sha256 (all eight targets)

```
sources  | sha256_before=a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45 | sha256_after=2bccb7057da68ed62f244685e13c4b88911ea379ebe340377a22a24fe0bc2723 | sha256_restored=a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45
readme   | sha256_before=33915658d9ef1ed3b93ed0cf58ba5b341bc58facc5d1ff73574e6ddd297dcb79 | sha256_after=cbd5a16eb388e7ae9f182b36ca079cdf638200251ea9929a2ecea1091abf30d9 | sha256_restored=33915658d9ef1ed3b93ed0cf58ba5b341bc58facc5d1ff73574e6ddd297dcb79
quality  | sha256_before=b4ce6c9091f99b854151035a4949af4a03850a08e937a8ccdd0de1c0c4c047a8 | sha256_after=fc0e82f48f6224619ca43b01c4882925c27e57920c21eda59ae94fbe1fe4e77a | sha256_restored=b4ce6c9091f99b854151035a4949af4a03850a08e937a8ccdd0de1c0c4c047a8
shonen   | sha256_before=55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09 | sha256_after=86c459047c76a7a6633f9f19a2b1c0a864855e499c8dda89387de128f5c3c07a | sha256_restored=55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09
log      | sha256_before=e0807383d745111a44fdd94d549d3e8211a41e3d0a1b936f15ac3221e81a32a6 | sha256_after=6146973df67153c8b2524933f46271bddfc162a95df9f7e352e03739b52fa467 | sha256_restored=e0807383d745111a44fdd94d549d3e8211a41e3d0a1b936f15ac3221e81a32a6
scorecard| sha256_before=cc93835f401189b48bd0f6d588361be3331321151a658bc5340cf2fbcabd5eac | sha256_after=b3fb5629f2eccbf2245fad674c87574121bf2cb4014c460ef32e14a487a310d9 | sha256_restored=cc93835f401189b48bd0f6d588361be3331321151a658bc5340cf2fbcabd5eac
lesson   | sha256_before=272341d9039916230a6500cec4096cb6f80d6baacb2f18b4cfc678634ba9be3d | sha256_after=4d7f6e55410d15a6e0a88cc39d52ee05a2ea90729284223f3a667e79ad1a2446 | sha256_restored=272341d9039916230a6500cec4096cb6f80d6baacb2f18b4cfc678634ba9be3d
ledger   | sha256_before=d799a7bbb2e3356ca2c4f2bb83a3e34e8f1a6a93755a2570b73cffd14643244c | sha256_after=7b95b255fda17485b7d2e41ce2937875f833409374372f745fcd0c0cd68c26cb | sha256_restored=d799a7bbb2e3356ca2c4f2bb83a3e34e8f1a6a93755a2570b73cffd14643244c
```

---

## 3. Comparison with the committed receipt `.ufo/evidence/round-28/append-probe.txt`

Committed receipt (at `b05d2ee`, `git show b05d2ee:.ufo/evidence/round-28/append-probe.txt`):

```
# round-28 append probe at base 06b59b93: one blank line appended to the named file(s), committed in a scratch clone, frozen C1 counter run
corpus_SOURCES.md: C1_MONITOR: covered=50/64 ... rev=074d30b1a67883ca3d16424b97fff20085354833
corpus_README.md:  C1_MONITOR: covered=55/64 ... rev=35bc273fd87821b91c1197fe444fecac2a8ccff0
corpus_QUALITY.md: C1_MONITOR: covered=57/64 ... rev=03785be36333e4ec53fb3f26ca57383f35909405
LOG.md:            C1_MONITOR: covered=60/64 ... rev=4f313b577fd94e157680c55ff818be53fac3a73c
SCORECARD.md:      C1_MONITOR: covered=60/64 ... rev=4d912e3c46e80671f0269e98d1be132559f79808
SHONEN.md:         C1_MONITOR: covered=59/64 ... rev=23b9b9cfa14200fd4f002b4672baf5f7d106e560
all six:           C1_MONITOR: covered=47/64 ... rev=2da8c3cdf15949f73bbd930cf86ec8953c1a13dd
base:              C1_MONITOR: covered=60/64 ... rev=06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c
```

My independent replication at the same base `06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c`
(separate clones, same method) reproduces it number for number:

```
sources   base 60/64 -> mutated 50/64
readme    base 60/64 -> mutated 55/64
quality   base 60/64 -> mutated 57/64
shonen    base 60/64 -> mutated 59/64
log       base 60/64 -> mutated 60/64
scorecard base 60/64 -> mutated 60/64
```

So the receipt is **not** falsified. But it is a **base-06b59b93** measurement, and
the lesson (`corpus/lessons/round-28.md:29-45`) presents it as a statement about
the round's own bookkeeping without pinning that its per-file numbers do not
hold at the landed head. At `b05d2ee` the same probe gives a different table
(§1). The lesson's `fix` sentence ("order the round so every edit to a widely
read lane file … lands BEFORE the content revision the cold reads are run
against") is directionally right, but incomplete: it names SOURCES, README,
QUALITY, SHONEN as the risky set and is silent on the fact that the fresh
round-28 entries themselves will re-bind those files' digests, and silent on
the four exception files.

---

## 4. Mechanism — why a drop happens, and when it does not

The counter's input gate is digest-keyed:
`.ufo/evidence/round-18/measure.py:330-350` (`input_failures`, reason string
`input-drift:<path>` at line 349), applied per ledger entry at
`:513-526` (`entry_reason`). A section is credited when at least one ledger
entry for its section sha passes and no veto fires (`:623-641`, `covered =
credited > 0 and not vetoes` at `:638`).

Consequences that the base table hides:

* A section de-credits only when **every** entry for that section sha fails.
  At the base, `corpus/SOURCES.md` was recorded by 99 entries and 10 sections
  had no other passing entry — hence 60→50.
* At `b05d2ee` the round's own SOURCES edit already broke every entry that
  recorded SOURCES.md's digest, so a further append changes nothing (50→50).
  Same for QUALITY.md, whose digest was already stale for the sections that
  recorded it.
* LOG.md and SCORECARD.md are recorded by only two entries each (sections 17
  and 1155), and each of those sections has 5–6 sibling entries; a stale
  sibling is not veto-eligible (`entry_is_stale` at `:528-537`), so the
  sections stay credited. That is why the base table shows LOG/SCORECARD 60→60
  and the landed head shows 50→50.
* `corpus/lessons/round-28.md` is recorded by **0** entries; nothing keys on
  its digest today.
* The round-21 ledger path is in the selector's ignore set
  (`.ufo/evidence/round-21/coldread/measure.py:112`,
  `module.IGNORED_INPUTS = module.IGNORED_INPUTS | frozenset((LEDGER,))`), so
  no entry's input gate looks at the ledger's own digest.

Entry-count census of the round-21 ledger at `b05d2ee`
(`entries[].inputs` keys): `corpus/SOURCES.md` 99, `corpus/README.md` 54,
`corpus/QUALITY.md` 31, `SHONEN.md` 10, `LOG.md` 2, `SCORECARD.md` 2,
`corpus/lessons/round-28.md` 0, `.ufo/evidence/round-21/coldread/ledger.json` 0.

### 4.1 Synthetic fresh-read probe — the load-bearing condition

To test what happens **after** this wave's cold reads, I added one synthetic
entry to the round-21 ledger in a clone: a well-formed `instruction` /
`executed-ok` entry for the currently-uncovered section 883, with
`commands_executed_count: 1`, a committed trace receipt, and the target file
recorded in `inputs` (the way a reader that opened the file under the trace
collector records it). Then I appended one blank line to that target.

```
### scorecard  target=SCORECARD.md
  before:   covered=51/64 ... exit 1
  after:    covered=50/64 ... exit 1
  restored: covered=51/64 ... exit 1
### log  target=LOG.md
  before:   covered=51/64 ... exit 1
  after:    covered=50/64 ... exit 1
  restored: covered=51/64 ... exit 1
### lesson  target=corpus/lessons/round-28.md
  before:   covered=51/64 ... exit 1
  after:    covered=50/64 ... exit 1
  restored: covered=51/64 ... exit 1
### sources  target=corpus/SOURCES.md
  before:   covered=51/64 ... exit 1
  after:    covered=50/64 ... exit 1
  restored: covered=51/64 ... exit 1
```

So **a fresh read that records a file as an input loses its section the moment
that file is appended** — for the three exception files just as much as for
SOURCES. The safety of "SCORECARD.md, LOG.md and the lesson file can be
appended after the cold reads" is therefore entirely dependent on the wave
exception being honoured: those files must never be opened under the trace
collector or by path, and must be read with `git show` outside the collector
and recorded only as `external_inputs` (`tameshi-shokunin@b05d2ee:<path>`),
which the input gate does not check
(`inputs_view` at `.ufo/evidence/round-18/measure.py:321-327` uses only the
entry's `inputs` map).

A second synthetic variant that recorded the target only under `external_inputs`
produced `covered=50/64` before and after the append — but its entry never
credited (its `inputs` map held only `SKILL.md`, which is in the ignore set, so
it failed the non-empty input gate with `inputs-unrecorded`). That variant is
**inconclusive** and I do not claim it as evidence either way; the load-bearing
claim above rests on the `inputs`-recording variant, which was positive in all
four cases.

### 4.2 Ledger append: neutral vs. non-neutral

```
trailing newline (JSON stays valid):
  C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=d54496299ad3c2cd1838d86d36318b5b720fd024
  exit=1     (ledger still parses; 354 entries)
one extra byte 'x' (JSON invalid):
  C1_MONITOR: covered=0/64 restraint=6 box3_mismatch=1 depth_score=9 rev=6f6b78bb010c3ae8b94c95f1aae7304c31c57035
  exit=1     (all 64 sections uncovered)
```

The neutral form is safe; any byte that breaks JSON parsing collapses the
monitor to 0/64. This is the one hazard with no cheap guard — a JSON syntax
error in the ledger is indistinguishable from "no credit at all" in the
counter's output.

---

## 5. Answers for the L1

* **Can SCORECARD.md, LOG.md and `corpus/lessons/round-28.md` be appended after
  the cold reads without any drop?** Yes — with today's round-21 ledger, each
  of the three appends measures `covered=50/64` before and after, and restores
  to `covered=50/64`. **Condition:** no fresh round-28 entry records them in
  `inputs` (the wave exception). If a reader opens one of them under the
  collector, the append costs that section (§4.1).
* **Can the round-21 ledger be appended?** Yes, as a whitespace-level change
  only (§4.2). It must remain parseable JSON.
* **What must not be appended after the fresh reads?** `corpus/SOURCES.md`,
  `corpus/README.md`, `corpus/QUALITY.md`, `SHONEN.md`, and any file the
  fresh reads record as an input. README already costs 2 sections and SHONEN 1
  section at `b05d2ee` with today's ledger alone; SOURCES and QUALITY will
  start costing as soon as the fresh entries record their digests.
* **Do the committed receipt's numbers apply to the landed head?** No. They are
  a base-`06b59b93` measurement; §1 is the `b05d2ee` measurement.

---

## 6. Smallest safe correction

1. **Do not append anything that a fresh round-28 entry records in `inputs`.**
   The four exception files (SCORECARD.md, LOG.md, the round-21 ledger, the
   lesson file) are safe only while the wave exception holds; keep the
   exception and state it in the report as a condition, not as a formality.
2. **Append the round-21 ledger as a whitespace-level change only** (a
   trailing newline is proven neutral here), and re-run
   `python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev HEAD`
   after it. If the counter reports `covered=0/64`, the ledger JSON is broken
   — check that first, before suspecting the reads.
3. **Fix the lesson's evidence pointer, not its conclusion.** In
   `corpus/lessons/round-28.md` Mistake 1 (lines 29-45), label the quoted
   per-file numbers as the base-`06b59b93` measurement they are and add the
   `b05d2ee` table (§1). The conclusion ("a blank-line append to a widely read
   lane file de-credits cold-read sections") stands; the numbers quoted do not
   describe the landed head.
4. **Land the `corpus/SOURCES.md` edit before the reads, and make no further
   edit to it, README.md, QUALITY.md or SHONEN.md after them.** The lesson's
   fix already says this; keep it, and add the mechanism in one clause: a
   section de-credits only when *every* entry for it fails, so the count of
   files that "cost credit" is smaller than the count of entries that name
   them.

---

## 7. Tooling

No tool was installed or upgraded for this item. Everything used was already
present: `git`, `python3` (standard library only), `sha256sum`, and the lane's
own frozen scripts. No `jj` command was run anywhere, in the lane or in a
clone. No file in `/home/vgpnk/Projects/shokunin/tameshi-shokunin` was written
except this report; all code ran inside `/tmp/mutappend/`.

Report: .ufo/waves/round-28/w1/MutateAppendProbe.md
