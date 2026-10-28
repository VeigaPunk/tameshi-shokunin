# T55W1RevRekeyByteProof — reader-report contract for the one re-keyed section

Seat: reviewer. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base `0a2010acd1e92e4e332774050825e21bcfc7e079`; frozen counter set `631cd6455e58dce969310b4c0466c3383d9f5108`.
Milestone: attack the reader deliverable the re-key needs. Axis: calibration.

**Bottom line.** The reader-report contract is `{heading, cand, section_sha256, findings}` plus a
sibling `.md`, where `cand` is the **full 40-hex commit the reader actually read** and
`section_sha256` is the sha of that section's **bytes at that commit** under the frozen round-18
`sectionize`. I built a validator for exactly that predicate
(`T55W1RevRekeyByteProof-receipts/validate-reader.py`, sha256 `1ff88053…`), and it **accepts 23/23
round-54 w1 readers and 46/46 across both waves** (every finding quote verbatim in its own section
bytes) and **rejects the forged report in all four modes**. I then measured the three ways the
round-55 re-key can silently go red after a correct reader lands (§6, F1–F3); one of them is new and
worth the L1's attention: a single post-bind edit to a pinned input drops credited sections
**64 → 53**.

---

## 1. What the credit code actually accepts (the predicate I mirrored)

Three implementations credit a reader report. They are not identical, and the differences matter.

| # | code | predicate | section read at |
|---|---|---|---|
| 1 | `.ufo/evidence/round-54/integrate/binder.py:117` | `d['cand'] == c0` **and** `d['section_sha256'] == sec['sha256']` | **c0** (`binder.py:90-92`) |
| 1b | `binder.py:119-121` | `len(d.get('findings') or []) <= allowed` (allowed = adjudicated count, default 0) | – |
| 1c | `binder.py:125` | sibling `<stem>.md` exists | – |
| 2 | `.ufo/evidence/round-54/c1/measure.py:241` | `d['cand'] == c0` **and** `d['section_sha256'] == sec['sha256']` | **REV** (`measure.py:169`) |
| 3 | `.ufo/evidence/round-18/measure.py:610,612` | the *bound ledger entry*'s `sha256` must equal `sec['sha256']`; credit then runs `entry_reason(…, strict=True)` | **REV** |

The round-21 credit code proper (`round-18/measure.py` + `round-21/coldread/measure.py`) never reads a
reader JSON at all: it credits a **ledger entry**, and it finds that entry by hashing the section at
REV and looking the digest up in `by_sha` (`round-18/measure.py:610-613`). So the reader's
`section_sha256` is not decorative — it becomes the entry's `sha256`, and it is the only key by which
the section is ever credited.

`sectionize` (`round-18/measure.py:209-252`) is the definition of "the section": heading line through
the line before the next `^#{1,3}(\s|$)` outside a fence, trailing whitespace-only lines stripped,
joined with `\n`, **no trailing newline**, decoded/encoded `surrogateescape`. A reader that hashes a
hand-copied block, or that includes the trailing blank line, is off-contract.

## 2. The validator

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/T55W1RevRekeyByteProof-receipts/validate-reader.py`
(262 lines, stdlib only; the receipts copy above is the authoritative one - the scratch tree was removed
per the seat's cleanup discipline, and `how-to-reproduce.txt` rebuilds it and every number below).

```
validate-reader.py --lane LANE --rev REV [--c0 C0] [--mode M] [--quote-check] [--json-out F] FILE...
```

* `--mode canonical` — heading exists at `cand`; `cand` is the **full 40-hex** sha of a commit in the
  lane; `section_sha256` is the sha of that section at `cand`; `findings` is a list of `{quote, why}`.
  This is the contract §5 specifies.
* `--mode binder` — canonical + `cand == C0` + sibling `.md` (binder.py's own filter).
* `--mode counter` — canonical + `cand == C0` + sha equals the section at **REV** (arm 4 verbatim).
* `--mode all` — accept only if all three accept (fail-closed).
* `--quote-check` — the honesty arm the credit code does **not** have: every `findings[].quote` must
  be a verbatim substring of the section body at `cand`. Reported separately, never folded into the
  credit verdict.

Exit 0 iff every named file is accepted. Every read is a git-object read (`git -C LANE show REV:path`,
`ls-tree`); the live working tree is never consulted, and the section hasher is the **frozen
round-18 module extracted at the rev**, never a reimplementation — the same technique as
`.ufo/waves/round-54/reader-section.py`.

## 3. Verdict 1 — the genuine reports are accepted, 23/23 (and 46/46)

```
$ python3 validate-reader.py --lane $CL --rev 631cd64… --c0 59c38109… --mode canonical --quote-check \
    .ufo/waves/round-54/w1/T54W1Read*.json
ACCEPT T54W1Read01.json reasons=none findings=1
…
ACCEPT T54W1Read23.json reasons=none findings=1
VALIDATOR mode=canonical rev=631cd6455e58 c0=59c38109bf11 files=23 accepted=23 rejected=0
EXIT=0
```
receipt: `T55W1RevRekeyByteProof-receipts/canonical-23.out` (+ `.json`).

Extended to both round-54 waves (w1 at `cand=59c38109`, w2 at `cand=99c3bc88`):

```
VALIDATOR mode=canonical rev=631cd6455e58 c0=99c3bc88d704 files=46 accepted=46 rejected=0
```
receipt: `canonical-46.json`. **All 53 findings across 46 reports quote text that is present
verbatim in the section at their own cand** — including the multi-line quote in `T54W1Read01.json`
(`"set but unusable →\n  exit 2, …"`), which only matches under the exact `\n`/stripping rule above.

Independent cross-check of a C1 class: the same run reproduces R54.5's derived counts exactly —
`accepted=46 w1_files=23 w2_files=23 / w1=28 w2=25 sections=12`
(`receipts/r54-5-crosscheck.txt`), matching the frozen counter's `finding_counts`
(`round-55/c1/measure.py:131-151`). Two independent implementations of the same count agree.

## 4. Verdict 2 — the forged report is rejected

`…/round-54/w2/T54W2Sent01-receipts/forged-reader.json` (sha256 `749abcdb…`), judged at every mode:

```
=== mode=canonical
REJECT forged-reader.json reasons=section_sha256-mismatch-at-cand findings=0
=== mode=binder
REJECT forged-reader.json reasons=section_sha256-mismatch-at-cand,binder-cand-not-c0,binder-sibling-md-missing
=== mode=counter
REJECT forged-reader.json reasons=section_sha256-mismatch-at-cand,counter-cand-not-c0,counter-section_sha256-mismatch-at-rev
=== mode=all
REJECT forged-reader.json reasons=section_sha256-mismatch-at-cand,binder-cand-not-c0,binder-sibling-md-missing,counter-cand-not-c0,counter-section_sha256-mismatch-at-rev
VALIDATOR mode=all … files=1 accepted=0 rejected=1   EXIT=1
```
receipt: `forged-all-modes.out`.

The primary rejection is the one R54.7 asserts: its `section_sha256` `b90c1f79…` is
`sha256(b"forged-r54-sent01: never read the section bytes")` and is **not** the section at its own
`cand` `99c3bc88` (`61736dce…`) nor at `c0` `59c38109` (`16439027…`). R54.7's parenthetical is
confirmed independently, and the forgery is rejected even without knowing `c0` — the
section-at-own-cand check alone kills it. That is the property the round-55 reader must inherit.

## 5. The exact shape the round-55 reader must take

Path: `.ufo/waves/round-55/w1/T55W1Read<NN>.json` (+ `.md`), or wherever the round-55 binder globs.

```json
{
 "heading": "## Standing rules",
 "cand": "<40-hex commit that carries the new `## Standing rules` bytes>",
 "section_sha256": "<sha256 of that section's bytes at cand>",
 "findings": []
}
```

| # | rule | why it is not optional |
|---|---|---|
| R1 | `cand` is the **full 40-hex** sha of a commit in the lane, and the reader must have read *those* bytes | the binder compares by string equality against a resolved c0 and arm 4 against a resolved c0; a 12-hex abbreviation never matches (`m1` rejected) |
| R2 | `section_sha256` = `reader-section.py LANE CAND "## Standing rules"` → `.section_sha256`; never hash a copied block | the digest is the ledger entry's `sha256` and the only key the credit algorithm looks up (`round-18/measure.py:610-613`) |
| R3 | **no commit after `cand` may change `SKILL.md`** before the deciding run | credit matches the section at **REV**, not at `cand`; a later edit drops the section to `no-ledger-entry` (measured: 64/64 → 63/64 at C56) |
| R4 | `findings` is `[]`, or a list of `{quote, why}` whose `quote` is a verbatim substring of the section body at `cand` | the credit code only calls `len()`; an invented quote is still credited (`m7` accepted by binder mode). The quote arm is the lane's only guard, and 53/53 round-54 findings pass it |
| R5 | the sibling `<stem>.md` exists | `binder.py:125` skips the report otherwise |
| R6 | filename must **not** match `/T54W\d+[A-Za-z]*Read\d+\.json$/` | `round-55/c1/measure.py:138` counts that regex for R54.5; a `findings`-bearing file under that name would shift the `w1=28` literal the corrections section carries |
| R7 | the binder must run with **PIN = the final content revision**, and no pinned input may change afterwards | measured: one post-bind edit to `tools/registry.json` took coverage 64/64 → **53/64** (`input-drift:tools/registry.json`) |

Provisional numbers for R2 (recompute at the real content commit; the lane working tree is being
edited by other seats right now): working-tree `SKILL.md` sha256 `e0ce89f7…` → `## Standing rules`
`start=17 end=44 section_sha256=acfb671a…`. **Do not paste this value** — it is derived from
uncommitted bytes (`git status` shows ` M SKILL.md` at the time of writing).

The bound ledger entry the binder must produce: `read_rev = cand`, `sha256 = section at cand`,
`start/end` from `sectionize`, `class`/`verdict` carried from the newest prior entry with
`gap-minor` + `minor_gaps = len(findings)` when findings exist, `blocking_gaps = 0`,
`wrong_expectations = 0`, `inputs` = the union of the prior entries' inputs minus
`DROP = (LOG.md, SCORECARD.md, SKILL.md, .ufo/evidence/round-21/coldread/ledger.json)`
(`binder.py:49`) each pinned at PIN, one trace under `rekey-r55-<cand12>/traces/section-NN.json`,
`seats`/`reports` naming the seat and both files.

### 5.1 Order of operations that keeps R3 and R7 true

```
# 1. land every content edit (the SKILL.md sentence LAST among them), then take C0 = that commit
C0=$(git -C $LANE rev-parse HEAD)                     # carries the new ## Standing rules bytes
# 2. read the section and write the report from reader-section.py's output, not from a copy
python3 .ufo/waves/round-54/reader-section.py $LANE $C0 "## Standing rules"
#    -> {"heading": ..., "cand": C0, "start": ..., "end": ..., "section_sha256": ...}
#    write .ufo/waves/round-55/w1/T55W1Read<NN>.json + .md from it; confirm findings quotes are verbatim
python3 validate-reader.py --lane $LANE --rev $C0 --c0 $C0 --mode all --quote-check \
    .ufo/waves/round-55/w1/T55W1Read<NN>.json           # must print ACCEPT
# 3. commit the report + md, then bind with PIN = the final content revision (>= every pinned-input edit)
python3 .ufo/evidence/<r55-binder>.py $CLONE $C0 $PIN .ufo/evidence/round-21/coldread/rekey-r55-${C0:0:12}
# 4. only record-only commits may follow (SCORECARD.md, LOG.md, corpus/lessons/round-55.md, wave files).
#    corpus/QUALITY.md and corpus/SOURCES.md are NOT record-only: they are pinned inputs (F2).
# 5. verify before freezing: round-21 monitor sections_covered == 64 and the frozen precheck exit 0
```

Step 3's binder must be a round-55 copy whose `WAVE_DIRS` point at the round-55 wave directory (or
the file placed where the unchanged round-54 binder globs — see R6). Step 5 is what F1 says the two
frozen gates already measure.

## 6. Findings

### F1 — BLOCKING: the re-key is load-bearing for `no-harm` and the deciding run, not a formality
`round-55/no-harm.sh:16-17` requires the round-21 monitor's `sections_covered >= 64`; the frozen
precheck invoked at `deciding-run.sh:70-71` prints RED whenever CAND credits fewer sections than
FLOOR (`round-48/quality/coldread-precheck.sh:22-30`). Replacing the `## Standing rules` sentence
changes its digest, so no existing entry matches and the section goes uncovered:

```
COVERAGE rev=631cd6455e58 covered=64/64 standing=[(True, 'credited')]      # baseline
COVERAGE rev=45680d9838f6 covered=63/64 standing=[(False, 'no-ledger-entry')]  # content commit, ledger unchanged
COVERAGE rev=76b30b94b6f9 covered=64/64 standing=[(True, 'credited')]      # after the frozen binder bound the fresh reader
```
receipts: `coverage-chain.txt`, `fixture-drift-rekey.out`. The mechanism is `by_sha`
(`round-18/measure.py:610-613`): entries are matched by the section at REV. So both gates go red on a
merely-edited SKILL.md, and green again only after the bind.

### F2 — BLOCKING (new): bind **last**; a post-bind edit to a pinned input costs 11 sections
The currently-crediting `## Standing rules` entry pins 2497 inputs, and among them are files round 55
itself edits: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/repeat-control.py`,
`tools/context-capture.py`, `tools/registry.json`, `tools/registry-check.py`, `SHONEN.md`,
`PROVINCE.md` (`SKILL.md`, `SCORECARD.md`, `LOG.md` are dropped by the binder, so those are safe).
Editing one of them after the bind:

```
COVERAGE rev=cd736a5a9429 covered=64/64 standing=[(True, 'credited')]                       # C57
COVERAGE rev=231220211d5b covered=53/64 standing=[(False, 'input-drift:tools/registry.json')] # C58: one pinned input edited
```
receipt: `coverage-chain.txt` (same run). **One late `tools/registry.json` write knocked out 11
credited sections.** The L1 must therefore run the binder *after* the last edit to any of those
eight paths, with `PIN` = that revision; `C0` may stay at the content commit (`binder.py` takes
`C0` and `PIN` separately for exactly this reason). Record-only commits after the bind are safe;
`corpus/QUALITY.md` and `corpus/SOURCES.md` are **not** record-only for this purpose.

### F3 — BLOCKING: a reader at `cand` is not enough if SKILL.md moves afterwards
The same reader accepted as a true read of C55 is rejected by arm 4 once SKILL.md moves to C56, even
though it is still an honest report of C55:

```
=== mode=canonical (reader cand=C55, judged at C56)
ACCEPT T55W1ReadBYTEPROOF.json reasons=none            EXIT=0
=== mode=counter
REJECT … reasons=counter-section_sha256-mismatch-at-rev EXIT=1
=== mode=all
REJECT … reasons=counter-section_sha256-mismatch-at-rev EXIT=1
```
receipt: `reader-at-c55-judged-at-c56.txt`; coverage at C56 with that reader in place:
63/64 `no-ledger-entry`. Consequence: `cand` must be the **last** commit that touches `SKILL.md`, and
the L1 must not "tidy" the section afterwards. (This is R3; it is the same invariant as F1's, seen
from the reader side.)

### F4 — MEDIUM: the credit code never verifies a finding's quote
`binder.py:119-121,155,181` uses `len(findings)` only. A report with a **fabricated** quote is
credited by the binder filter itself:

```
=== mode=binder (m7 = genuine heading/cand/sha + an invented quote)
ACCEPT m7-findings-invented-quote.json reasons=none findings=1
=== mode=canonical --quote-check
REJECT m7-findings-invented-quote.json reasons=finding-0-quote-not-in-section-at-cand
```
receipts: `mutants-binder.out`, `mutants-canonical.out`. This is the remaining forgery surface after
R54.7: a real section digest with invented content. Nothing in the lane measured it before this seat;
the round-54 corpus happens to be clean (53/53 quotes verbatim — §3), but that is a fact about those
readers, not an enforced rule. Recommend the round-55 lesson state the quote rule and the L1 run the
`--quote-check` arm over the new reader before binding.

### F5 — MEDIUM (divergence, safe direction): non-list `findings` is accepted by the credit code
`d.get('findings') or []` then `len(...)` means a **dict** or a **string** is silently counted:

```
len(findings) = 1 type = dict | binder compares > allowed (1 for this heading) -> False
n_find = len(d.get("findings") or []) = 1
```
receipt: `credit-len-dict.txt`. My validator rejects `findings-not-list` (`m5`, `m6`). This is
*stricter* than the frozen code, so it cannot credit anything the credit code would not — but it is
not "exactly equal", and the honest statement of the contract is: **a report whose `findings` is not a
list is accepted-and-counted by the frozen binder and rejected by the contract.** I did not "fix" the
frozen code (report, don't fix, per the seat bounds); the round-55 spec should state the list shape so
no one relies on the lenient path.

### F6 — LOW: `findings` may be absent entirely
`m8` (key removed) is ACCEPTed by both binder mode and canonical mode, with `findings=0` — matching
`d.get('findings') or []`. The contract should still require the key (a reader that omits it is
indistinguishable from one that found nothing).

### F7 — LOW: where to put the file, and what must not be named what
The frozen binder globs **`.ufo/waves/round-54/w1|w2/*.json` with no name filter** (`binder.py:48,99`)
and indexes by `heading`, while R54.5 counts only `/T54W\d+[A-Za-z]*Read\d+\.json$`
(`round-55/c1/measure.py:138`). So:
* name the file `T55W1Read<NN>.json` — never `T54W…Read….json`;
* if the round-55 binder is a copy with its own `WAVE_DIRS`, put the report in
  `.ufo/waves/round-55/w1/`; if the round-54 binder is reused unchanged, the file must sit under
  `.ufo/waves/round-54/w1/` (a `T55W…` name there is invisible to R54.5 — verified by reading both
  regexes, and by the R54.5 cross-check in §3);
* a findings-bearing report under a `T54W…` name would change the `w1=28` literal the corrections
  section carries and flip C1.

### Mutant sweep (the attack, so "nothing found" is not asserted)
Nine mutants of `T54W1Read01.json` (built under `$S/mutants/`, rebuilt by
`how-to-reproduce.txt`), judged at base:

| mutant | canonical +quote-check | binder |
|---|---|---|
| m1 `cand` abbreviated to 12 hex | REJECT `cand-not-full-sha` | REJECT `cand-not-full-sha,binder-cand-not-c0` |
| m2 honest read of the **later** commit (sha `61736dce`) | REJECT `finding-0-quote-not-in-section-at-cand` (the section changed, so the old quote no longer exists there); **ACCEPT** with `--quote-check` off | REJECT `binder-cand-not-c0` |
| m3 sha of a different section | REJECT `section_sha256-mismatch-at-cand` | REJECT same |
| m4 heading typo (`Rule` for `Rules`) | REJECT `heading-absent-at-cand` | REJECT same |
| m5 `findings` = dict | REJECT `findings-not-list` | REJECT same (frozen code would count it — F5) |
| m6 `findings` = string | REJECT `findings-not-list` | REJECT same |
| m7 invented quote, everything else genuine | REJECT `finding-0-quote-not-in-section-at-cand` | **ACCEPT** (F4) |
| m8 `findings` key absent | ACCEPT (`findings=0`) | ACCEPT (F6) |
| m9 `cand` = 40 zeros | REJECT `cand-unresolvable` | REJECT `cand-unresolvable,binder-cand-not-c0` |

receipts: `mutants-canonical.out`, `mutants-binder.out`, `mutants-*.json`.

## 7. Residual risk and verification gaps

* **Provisional digest.** The `acfb671a…` value in §5 comes from uncommitted working-tree `SKILL.md`.
  The L1 must re-derive it with `reader-section.py` at the content commit; if the section changes
  again (it is currently 4 lines longer than at base, `end` 40 → 44), every number in §5 shifts.
* **I did not run the round-55 counters.** My scope is the reader contract; the counters are frozen and
  another seat owns them. The coverage figures are the frozen round-18 `coldread()` run directly, not
  `c1/measure.py`.
* **Fixture, not the real round.** The drift/re-key chain was measured in a `git clone --shared` of the
  lane (`$S/clone`, `rev-parse --show-toplevel` asserted before every commit); the lane was only read.
  The fixture's `SKILL.md` edit is a marker, not the round's wording — the mechanism is what was
  measured (1 section → 11 sections), not the wording.
* **`m2` without `--quote-check` is ACCEPTed by canonical mode.** That is correct and intended: it is a
  true read of *a* commit. It is not creditable (binder rejects `cand != c0`), which is why R1 and R3
  are separate rules.
* **The 2497-input entry** is why the coldread runs took ~45 s each; a `PIN` at the wrong rev is not a
  theoretical risk but an 11-section loss (F2).
* **The contract proves bytes, not attention.** A seat that runs
  `reader-section.py`, pastes the three fields and writes `findings: []` without opening the section is
  indistinguishable from an honest clean read — the validator, the binder, arm 4 and the credit
  algorithm all accept it. This is inherent to a digest-keyed contract, and it is the one forgery
  class no artifact this lane owns can exclude; the round-54 set happens to be genuine (53/53 quotes
  land verbatim, which a non-reader would have had to fabricate consistently). State the limit rather
  than claim the re-key is unforgeable.
* **Frozen-file observations reported, not fixed:** `binder.py:119-121` accepts any sized object as
  `findings` (F5); `round-54/c1/measure.py` arm 4 compares against the section at REV while its
  docstring says "at REV" and its sibling `binder` compares at c0 — the two agree only while SKILL.md
  is byte-identical at c0 and REV, which round 55 breaks by design (F3). Both are in the lane's
  evidence tree, not in the round-55 freeze manifest; I changed nothing.

## 8. Hygiene

* Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit **0** (W01/W04 warnings only). Ran at 14:2xZ, same day.
* Lane: read-only. No `add`/`commit`/`checkout`/`push`/`jj` anywhere on the lane; every git mutation
  named `-C "$CL"` inside my scratch clone, with `git rev-parse --show-toplevel` asserted first.
* Scratch: `HYAKU_SCRATCH=/fast/scratch/hyaku`, `$S=/fast/scratch/hyaku/tameshi-r55/T55W1RevRekeyByteProof`,
  `TMPDIR=$S/tmp`; nothing written under `/tmp`. `$S` was removed after the receipts were copied into
  this wave directory (`how-to-reproduce.txt` rebuilds it).
* Tooling: **no installs needed** (python3 stdlib + git only); nothing changed on `PATH`.
* No lane production file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`) was edited.

## 9. Receipts index

`T55W1RevRekeyByteProof-receipts/`: `validate-reader.py` (`1ff88053…`), `fixture-drift-rekey.sh`
(`9be47a02…`), `canonical-23.out`/`.json`, `canonical-46.json`, `r54-5-crosscheck.txt`,
`forged-all-modes.out`, `forged-{canonical,binder,counter,all}.json`, `mutants-canonical.out`,
`mutants-binder.out`, `mutants-*.json`, `credit-len-dict.txt`, `fixture-drift-rekey.out`,
`coverage-chain.txt`, `pin-drift-coverage.out`, `reader-section-at-c55.json`,
`reader-at-c55-judged-at-c56.txt`, `sha256s.txt`.
