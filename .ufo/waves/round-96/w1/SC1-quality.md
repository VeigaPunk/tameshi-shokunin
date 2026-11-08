# SC1 — `corpus/QUALITY.md` draft, criteria 173-174 (round 96)

**Seat:** R96SC1 (scribe). **Lane:** `tameshi`. **Mode:** read-only — nothing under `corpus/`
was written; this file is a draft for the L1 to integrate.

**Read first.** Criteria 173 and 174 were landed by the L1 at `9b89c68d` (`corpus/QUALITY.md`
lines 2750-2777). This draft restates them in the established style, **with the two receipt
citations repaired** where the landed text cites a receipt that does not carry the string it
quotes. The repairs are marked inline; the criterion *wording* is not changed, because the
wording matches the spec this seat was given and each property it names is backed by a
committed receipt (verified below).

## Established style, restated

The style is the one criteria 169-172 use: a numbered paragraph whose first sentence is the
rule in the imperative, a "why" clause naming the concrete mechanism it closes, and an
**Able to fail:** clause that names a receipt path and the token it prints.

---

### 173

173. A revision named by an instrument is a **commit identity**, never a ref or a
    shorthand: it is checked as 40 hex, resolved with `rev-parse --verify --quiet
    <rev>^{commit}`, printed into the verdict line, and an empty or branch-shaped value is
    refused before any read. A bare `git rev-parse <40-hex>` echoes a nonexistent object id
    with rc 0 and a bare `rev-parse` resolves a branch that moves under the audit, so the
    "frozen revision" would not be pinned at all. Able to fail: the round-96 checker at
    `933df676` prints `DISPOSITION_SETUP rev-not-a-commit-id` exit 2 for `--rev ''` and
    `--rev master`, `DISPOSITION_SETUP rev-unresolvable` exit 2 for `--rev deadbeef…`
    (`.ufo/evidence/round-96/landing/c1-rev-{empty,branch,unresolvable}.out`), and the
    positive prints `DISPOSITION_INSTRUMENT rev=8ed9c526… sha256=…` — while the
    pre-amendment bytes (`10d8fa5d`) printed `rev-unresolvable` never and only `sha256=`
    (`w1/R96C1.md` C1.3, C1.5). (`lessons/round-96.md`; `plans/round-96.plan.md` §A2-A3.)

### 174

174. A tool that writes into a repository path **refuses an empty or relative lane, refuses
    a symlink at the destination, and writes atomically** (temp file with
    `O_CREAT|O_EXCL|O_NOFOLLOW`, `fsync`, `os.replace`) — and a battery that grades its own
    receipts reads **the path it wrote**, not a name-index search over the directory. An
    empty `--lane` resolves to the process CWD (`os.path.realpath("")`), a plain `open()`
    follows a symlink out of the tree, and a lowest-index search grades a planted file at
    index 0. Able to fail: `make-pins96.py --lane ''` prints `PINS_SETUP lane-empty` exit 2
    writing nothing; a symlink at `pins.json` prints `PINS_SETUP pins-symlink-refused` exit
    2 with the outside target's sha256 unchanged (`9660b330…` before and after;
    `.ufo/evidence/round-96/landing/c2-pins-{empty-lane,symlink}.out`); the driver grades
    `pos-real.rerun-1.out` — its own write — while a planted `pos-real.out` with
    `counter_sha=000…0` sits beside it (`c2-rerun-plant.out`), and refuses a symlinked
    `--outdir` (`outdir-symlink-refused`, `c2-outdir-symlink.out`). The pre-amendment
    round-95 tool wrote through the symlink and into the CWD (`w1/R96R2.md`; `w1/R96SN1.md`
    F4/F9). (`lessons/round-96.md`; `plans/round-96.plan.md` §A7, A9.)

---

## The two citation repairs (this seat's contribution)

**Both are QUALITY 168-class defects** — *"a `## Mistakes` (or any lesson) evidence pointer
that quotes a receipt line is byte-backed by that receipt at the revision the lesson names"*
— applied to QUALITY itself. Each landed citation names a receipt that exists, but the
receipt does **not** carry the string the criterion quotes from it.

### Repair 1 — criterion 174, the planted-receipt sentence

The landed text says:

> the driver grades `pos-real.rerun-1.out` — its own write — while a planted `pos-real.out`
> with `counter_sha=000…0` sits beside it (`c2-rerun-plant.out`)

The receipt `.ufo/evidence/round-96/landing/c2-rerun-plant.out` is **four lines** and
contains none of the three quoted strings:

```
1  CONTROL_INSTRUMENT sha256=69ee68b6fa230e29ef5ddc4e02d619562d5fe5f3620fb2355903c7f9f09a18d9
2  pos-real MATCH exit=0
3  C1_CONTROLS states=1 matched=1 mismatches=0 missing=0
4  exit=0
```

`grep -c "rerun-1"`, `grep -c "pos-real.out"` and `grep -c "counter_sha=000"` on that file
all return **0** (receipt: `.ufo/waves/round-96/w1/R96SC1-regrade.txt` header and this
seat's grep of the committed blob). The strings are real, but they live in **different**
receipts, both committed:

- `.ufo/waves/round-96/w1/R96R2-out-rerun9-planted.out` — carries `counter_sha=000000…0`
  (the planted receipt's body), `exit=1`, `C1_CONJUNCTS pass=false verdict_tables=false`;
- `.ufo/waves/round-96/w1/R96R2-out-symlink-summary.txt` — carries `pos-real SYMLINK-REFUSED`.

So the fix is to cite the receipt that carries the string, and to keep
`c2-rerun-plant.out` for what it does carry (the driver graded `pos-real` as `MATCH`,
`states=1 matched=1 mismatches=0 missing=0`, exit 0). Corrected clause:

> …and a battery that grades its own receipts reads **the path it wrote**, not a
> name-index search over the directory. … Able to fail: … the driver grades its own write:
> `c2-rerun-plant.out` prints `pos-real MATCH exit=0` and
> `C1_CONTROLS states=1 matched=1 mismatches=0 missing=0`, exit 0, while the planted
> receipt it did **not** grade is carried by `w1/R96R2-out-rerun9-planted.out`
> (`counter_sha=000000…0`, `exit=1`, `pass=false verdict_tables=false`); a symlinked
> receipt is refused, `w1/R96R2-out-symlink-summary.txt` prints `pos-real SYMLINK-REFUSED`;
> and a symlinked `--outdir` is refused (`outdir-symlink-refused`,
> `.ufo/evidence/round-96/landing/c2-outdir-symlink.out`). The pre-amendment
> round-95 tool wrote through the symlink and into the CWD (`w1/R96R2.md`;
> `w1/R96SN1.md` F4/F9). (`lessons/round-96.md`; `plans/round-96.plan.md` §A7, A9.)

### Repair 2 — the same defect in criterion 174's sibling, the lesson's `## Measurements`

The landed lesson (`corpus/lessons/round-96.md`, `## Measurements`) repeats the same
unbacked citation: *"`c2-rerun-plant.out`: a planted `pos-real.out` carrying
`counter_sha=000…0` sits beside the driver's own `pos-real.rerun-1.out`, and the driver
prints `pos-real MATCH exit=0 states=1 matched=1` — it graded its own write."* The receipt
carries `pos-real MATCH exit=0` on line 2 and `C1_CONTROLS states=1 matched=1 mismatches=0
missing=0` on line 3 — two separate lines, not one `states=1 matched=1` string — and it
carries neither `pos-real.out` nor `counter_sha=000…0`. The corrected text is in
`SC1-lesson.md`'s Measurements section.

## Verification of every pointer in the two criteria

Each pointer below was opened and read by this seat; the token each quotes is present.

| pointer | token read | present |
|---|---|---|
| `.ufo/evidence/round-96/landing/c1-rev-empty.out` | `DISPOSITION_SETUP rev-not-a-commit-id` | yes |
| `.ufo/evidence/round-96/landing/c1-rev-branch.out` | `DISPOSITION_SETUP rev-not-a-commit-id` | yes |
| `.ufo/evidence/round-96/landing/c1-rev-unresolvable.out` | `DISPOSITION_SETUP rev-unresolvable` | yes |
| `.ufo/evidence/round-96/landing/c1-positive.out` | `DISPOSITION_INSTRUMENT rev=8ed9c5262bd2f36f3cc8a64550897f4d1adb3a3b sha256=69ee68b6… conjuncts=19` | yes |
| `.ufo/evidence/round-96/landing/c2-pins-empty-lane.out` | `PINS_SETUP lane-empty` / `exit=2` | yes |
| `.ufo/evidence/round-96/landing/c2-pins-symlink.out` | `PINS_SETUP pins-symlink-refused` / `exit=2` / `target_before == target_after == 9660b330…` | yes |
| `.ufo/evidence/round-96/landing/c2-pins-positive.out` | `PINS_WRITTEN …/pins.json`, `PINS_CHECK OK` | yes |
| `.ufo/evidence/round-96/landing/c2-outdir-symlink.out` | `outdir-symlink-refused` / `exit=1` | yes |
| `.ufo/evidence/round-96/landing/c2-rerun-plant.out` | `pos-real MATCH exit=0`, `C1_CONTROLS states=1 matched=1 mismatches=0 missing=0`, `exit=0` | yes |
| `.ufo/waves/round-96/w1/R96R2-out-rerun9-planted.out` | `counter_sha=000000…0`, `exit=1`, `pass=false verdict_tables=false` | yes |
| `.ufo/waves/round-96/w1/R96R2-out-symlink-summary.txt` | `pos-real SYMLINK-REFUSED` | yes |

## Two facts the criteria lean on that this seat measured independently

**173's `--rev` guard is real at the instrument, not only in the receipt.** Running the
amended checker blob at HEAD (`933df676`) directly:
`--rev ''` → `DISPOSITION_SETUP rev-not-a-commit-id` exit 2; `--rev master` → the same;
`--rev deadbeef…` → `DISPOSITION_SETUP rev-unresolvable` exit 2; and the amended **counter**
at HEAD refuses `--rev ''` and `--rev master` with `C1_SETUP rev-not-a-commit-id` exit 2.
Receipt: `.ufo/waves/round-96/w1/R96SC1-amended-counter.txt`. The guard's own source is
`.ufo/evidence/round-96/c1/measure-v96.py:420` (`die("rev-not-a-commit-id")`) and
`:421-426` (`rev-parse` then `die("rev-unresolvable")`).

**174's atomicity is in the tool's source, and the positive path is reachable.** The write
path is `make-pins96.py:87-101`: the temp file is opened `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`,
flushed, `fsync`'d, and only then `os.replace`'d over the destination — the destination path
is never opened for writing. The refusals are at `:61` (`lane-empty`), `:66`
(`lane-not-absolute`), `:88` (`pins-symlink-refused`) and `:92` (`tmp-symlink-refused`).
Receipt for the source read: `.ufo/waves/round-96/w1/R96SC1-pin-state.txt` and this seat's
direct read of the committed blob; the executed receipts are the `c2-pins-*.out` files
above. The round-95 before-witness — the same two attacks succeeding — is
`.ufo/waves/round-96/w1/R96E3-before-witness.out` (`PINS_WRITTEN …/cwd95/…` exit 0 for the
empty lane, and the outside target's sha256 changing from `343f3bba…` to `688fe42a…`).

## What this draft does not change

The criterion **wording** of 173 and 174 is unchanged from the landed text. Every property
both criteria name is backed by a committed receipt (the table above), and the spec this
seat was given names exactly these two rules. Only the receipt citations are repaired, and
the repairs make the criteria cite the receipt that carries the quoted string — the rule
QUALITY 168 already states, applied to QUALITY itself.
