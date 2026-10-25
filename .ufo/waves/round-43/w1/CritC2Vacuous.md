# CritC2Vacuous — vacuity and masking attack on the C2 classes (round 43, w1)

Scope: my item only — attack the *new* classes (m12, m13) and the three assigned extraction
fixtures (m7 staged/next-free, m8 dropped cites, m10 prefix resolution) for vacuity and for
masking. I did not judge the claims, edit the lane, or run a mutating git command in it. All
lane reads; all writes in `/tmp/tameshi-r43-CritC2Vacuous-lane`.

## Verdict

**`C2_R43_PASS=true` is reachable while every one of the three assigned attacks is live in the
tree, and the two new classes are pure substring tests that a decoy sentence satisfies.**
Measured, not argued: rev `2655ded` and `607e0cd` in the scratch repo print

```
C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 ... C2_R43_PASS=true
```

with these objects present at the same rev: a fabricated `staged:S901`/`staged:S902`, a
`Next unused id: S001` that collides with a real mined row, five unresolvable in-lane path
cites, a self-witnessing presence receipt, one false `present=true` receipt laundered by a
`supersedes` key, and a superseding receipt whose own false claim is exempt. Plus (separately)
a round block that says *nothing is planned* and a standing command that is still column-zero.

The counter is **right in direction and wrong as a check**. Of the seven forms my item names:

| form | disposition | right? |
|---|---|---|
| `staged:S###` token | masked, unconditionally (`:65`, `:67`, `:384-386`) | direction only (F1) |
| `Next unused id: S###` | masked, unconditionally (`:68`) | direction only, hides a collision (F2) |
| absolute in-lane cite | dropped (`:178`) | no (F3) |
| `…/` elided cite | dropped (`:178`), tail unchecked | partly: tail is checkable (F3) |
| brace cite `{a,b}` | **not** dropped — mangled to `tools/.py` (`:182`) | no, false positive (F3) |
| directory cite | dropped before the resolver runs (`:185` vs `:203`) | no (F4) |
| prefix-resolved receipt | accepted, but the subject is unfalsifiable (`:248`) | boolean yes, guard no (F5) |

Beyond the item, two more: `m10`'s `supersedes` exemption is a *measured regression against its
own predecessor* (F6), and the new classes m12/m13 are substring tests that a decoy sentence
satisfies (F7). A declaration is not a declaration merely because the string appears, and a
command is not census-valid merely because the token appears.

## Method

Scratch repo = `cp -a` of the lane at the freeze minus `.jj`
(`/tmp/tameshi-r43-CritC2Vacuous-lane`, `.git` intact, no write reaches the lane). Every run:

```
python3 .ufo/evidence/round-43/calibration/measure.py \
  --lane /tmp/tameshi-r43-CritC2Vacuous-lane --rev <scratch rev> \
  --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
```

`self_pin=1` on every scratch run, i.e. the scratch repo's counter bytes and the freeze blob
are the pinned ones; only the *lane content read via `git show`* differs.

Lane-context runs, for reference (allowed revisions only):

| run | command output | exit |
|---|---|---|
| base `487b8f0` | `m12=1 m13=1 total=2 records=3 receipts=17 ... C2_R43_PASS=false first=m12:Planned_(round_43)` | 1 |
| freeze `17f6ef0` | identical (`records=3 receipts=17`) | 1 |
| `--selftest` | `C2_R43_SELFTEST: cases=10 failed=0` / `VERDICT: PASS` | 0 |

Scratch commits (each a single attributable step; full log in the scratch repo):

| rev | step | counter |
|---|---|---|
| `f39194d` S1 | reach the predicate (planned line + census command) | PASS=true |
| `22dae19` S2 | **(a)** only `staged:S90x` / `Next unused id:` ids | PASS=true |
| `26c31ce` S2b | **(a) control**: plain `S904` (unknown) + `S007` (queued) | m7=2 |
| `802ddcf` S3 | **(b)** five dropped cites + two positive controls | m8=2 |
| `0135f7a` S3b | **(b)** brace form `tools/{alpha,beta}.py` | m8=3 (`tools/.py`) |
| `bdff49e` S4 | **(c)** receipts: dir targets, file targets | m10=2 |
| `50cfe66` S5 | **(c)** self-witnessing dir receipt + one false file receipt | m10=1 |
| `f1043f9` S6 | **(c)** one `supersedes` key | m10=0 |
| `03daedf` S7 | only dropped cites remain (control hit left in) | m8=2 |
| `2655ded` S8 | **all attacks live, nothing flagged** | **PASS=true** |
| `607e0cd` S9 | m12/m13 decoys (expected strings in negating prose) | **PASS=true** |
| `f1ce1b8` S10 | `supersedes` target need not exist | **PASS=true** |

## Findings

### F1 — (a) `staged:S###` is masked unconditionally: right direction, no enforcement

`ID_RE` carries `(?<!staged:)` (`measure.py:65`) and `MASK_IDS` substitutes
`staged:S\d{3,}` with a space (`:67`, applied at `:384-386`). Nothing compares the masked id to
any staged manifest.

Fixture (S2, `22dae19`), the record's only ids:

```
The assimilation package header names staged:S901 and staged:S902 as the ids it would append.
Next unused id: S903
Next unused id: S001
```

Result: `m7=0`, `PASS=true`. **All four ids are fabricated**: the lane registry tops out at
`S158`, and the staging package (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`)
tops out at `S255` — `S901`–`S903` appear in neither (`grep -c` = 0 for each).

Control S2b (`26c31ce`) adds one plain `S904` and one plain `S007` (queued, unmined) →
`m7=2 ... first=m7:corpus/lessons/round-43.md_unmined_S007`. So the detector works; the mask is
the entire reason a fabricated id passes.

**Is the counter right?** In direction, yes: a package token is not a citation of a registry
row, and the staged ids live outside the lane, so they cannot be resolved against
`corpus/SOURCES.md`. As a *check*, no: one seven-character prefix (`staged:`) launders any id,
and the counter never checks the mask's own precondition. The lane already holds the manifest
that makes the conditional cheap: `.ufo/waves/round-42/assimilation/staged-ids` (103 ids) is a
tracked, rev-scoped receipt of the staged set.

*Smallest safe correction:* mask `staged:S###` only when the id is a member of the round's
`staged-ids` receipt at REV; otherwise emit `staged-token not in staged manifest <sid>`. Also
delete the now-redundant lookbehind (`:65`) — the substitution already removes the token, so
the two mechanisms together only widen the blind spot (`unstaged:S123` is masked by both).

### F2 — (a) `Next unused id:` hides an id collision that no class can see

Same fixture line `Next unused id: S001`; `S001` is row 12 of `corpus/SOURCES.md`, `mined`.
`MASK_IDS` erases it (`:68`), `m7=0`, and `m6` compares row *counts* (113 = 113), so a duplicate
next-free declaration is invisible to all seven classes. That collision is exactly what the
registry census and the staged-id guard exist to prevent.

**Is the counter right?** Right to exclude the declaration from "citations of a row" (a next-free
id is not a row yet); wrong to exclude it from *every* check.

*Smallest safe correction:* after masking, if a declared next-free id is in `registry_rows`,
emit `next-free collides <sid>`. Three lines next to `:385`; no new extraction needed.

### F3 — (b) m8's drop surface, and one form that is not dropped but *fabricated*

`path_cites` (`:174-192`) silently discards, before any resolution test:

| form in fixture | where dropped | observed |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/definitely-missing.py` | `:178` `startswith('/')` | not counted |
| `…/tools/definitely-missing.py` | `:178` `startswith('…')` | not counted |
| `corpus/definitely-no-such-dir` | `:185` `endswith(SKIP_SUFFIXES)` | not counted |
| `./tools/definitely-missing.py` | `:189-192` (no prefix matches `./tools/`) | not counted |
| `tools/definitely-missing.yaml` | `:185` (closed 15-suffix allowlist, `:63-64`) | not counted |

Controls in the same record were counted: `tools/definitely-missing.py:12` **and**
`corpus/definitely-no-such-dir.md` → `m8=2` (S3, `802ddcf`); `path_cites` returned
`['corpus/SOURCES.md', 'corpus/definitely-no-such-dir.md', 'tools/definitely-missing.py']` and
the five forms above are absent. So the class is decided by spelling, not by resolvability.

The **brace form** is the opposite failure. `` `tools/{alpha,beta}.py` `` is *not* dropped:
`:182` `re.sub(r'\{[^}]*\}', '', token)` deletes the expansion and leaves `tools/.py`, which
then passes the prefix test and is reported as a missing path. S3b (`0135f7a`): `m8=3`, with
`... :tools/.py` in the hit list. **The counter fabricates a path that no author wrote**, so an
honest brace cite cannot pass a PASS-required predicate.

**Is the counter right?**
- absolute: no. An in-lane absolute cite is exactly as resolvable as the relative form; dropping
  it is a free evade. Fix: if the token starts with the lane root, strip to the relative cite
  and run the normal path (one `os.path.relpath`, no new rule).
- `…/` elision: the head is unknowable at REV, but the tail is not. Fix: require some tree path
  to *end with* the elided tail; report when none does. This keeps elision legal and stops a
  wrong tail passing.
- directory (no suffix): no — see F4, this is an ordering bug, not a policy.
- `./`: no. Normalize `./` before the prefix test.
- closed suffix allowlist: no, it is vacuous by construction. `m8`'s declared scope is "(after
  `:NN` and brace normalization)" — a closed 15-entry allowlist silently exempts `.yaml`,
  `.yml`, `.toml`, `.lock`, `.cfg`, `.ini`, `.csv`, `.patch`, `.png`, `.gif`, `.svg`, `.rs`,
  `.go`, `.lua`, `.js`, `.ts`.
- brace: no — deleting the braces in place is wrong in both directions. Fix: expand `{a,b}` into
  its members and resolve each; never emit the stripped remainder as a candidate.

### F4 — (b) the directory branch is unreachable for exactly the tokens it was written for

`m8_paths:202-203` resolves a directory as a prefix (`any(p.startswith(token.rstrip('/') + '/'))`),
but `path_cites:185` has already discarded every token lacking a listed file suffix. So the
directory rule can only fire on tokens that *look like files* — and a directory named `x.md`
is the only way in. Demonstrated in one run, same prefix, only the suffix differs:

```
corpus/definitely-no-such-dir     -> not a hit          (dropped at :185)
corpus/definitely-no-such-dir.md  -> hit 'r:corpus/definitely-no-such-dir.md'
```

**Is the counter right?** No. The two rules contradict: the extractor's suffix gate makes the
resolver's directory branch dead code for real directory cites. *Smallest safe correction:*
test directory-ness before the suffix gate (`token.endswith('/')` or the prefix branch), i.e.
move `:183-185` below the directory test, or drop the suffix gate for tokens under a declared
prefix.

### F5 — (c) prefix resolution is right for the boolean and unfalsifiable for the subject

`m10_receipts:248` computes `exists = rel in tree or any(p.startswith(rel.rstrip('/') + '/') for p in tree)`.
Since `<rev>` is listed with `git ls-tree -r` (files only), the second disjunct is "the
directory exists". S4 (`bdff49e`, `m10=2`, 22 claims) shows the pair behaving as intended:

```
.ufo/waves/round-43/w1/DirPresent.json   present=true  corpus/lessons              -> 0 hits  (directory resolves)
.ufo/waves/round-43/w1/RootPresent.json  present=true  .ufo                        -> 0 hits
.ufo/waves/round-43/w1/FilePresent.json  present=true  .../DirPresent.json         -> 0 hits
.ufo/waves/round-43/w1/DirAbsentClaim.json present=false corpus/lessons            -> hit (correct: exists != false)
.ufo/waves/round-43/w1/MissingFile.json  present=true  corpus/lessons/does-not-exist.md -> hit
```

So `present=false` on a directory is caught, correctly.

The vacuity is the other direction. S5 (`50cfe66`) adds

```
.ufo/waves/round-43/w1/SelfWitness.json  {"present": true, "report": ".ufo/waves/round-43/w1"}
```

`m10=1` — the only hit is the *file* claim, not this one, although at that rev the claimed
directory exists **solely because the receipt itself was written into it** (`git ls-tree`
round-43/w1 at `03daedf` lists only the six fixture receipts). A receipt that means "the w1 wave
carries its seat reports" is encoded as `present=true` + a directory path, and the check is then
true by construction, independent of the seats.

**Is the counter right?** For the boolean, yes: "some path under it exists" *is* directory
presence, and flagging `present=false` on an existing directory is correct. As a guard, no: for a
directory target the claim has no falsifiable subject, so the class measures a name, not a claim.

*Smallest safe correction:* resolve directory claims against `tree - {receipt}`; if the target's
only members are the receipts that sit in it, emit `self-witnessed directory <rel>`. One set
difference, no new extraction; it kills the circular case and leaves honest directory receipts
(which always have other members) green.

### F6 — (c) masking *regression*: the `supersedes` exemption now exempts the superseder itself

`m10_receipts:241-244`:

```
superseded = set()
for key, value in supersedes.items():
    superseded.add(key[2:] if key.startswith('./') else key)
    superseded.add(value)          # <- the superseding receipt's own path
```

`:252` then skips **any** claim whose receipt path is in that set. Two consequences, both measured:

1. **self-waiver.** A receipt carrying any non-empty `supersedes` is exempt from its *own*
   presence claims. S6 (`f1043f9`) launders both false claims with one key; S10 (`f1ce1b8`) points
   `supersedes` at `.ufo/waves/round-43/w1/predecessor-that-never-existed.json` — a target that
   does not exist — and the false claim `tools/definitely-missing-3.py present=true` is still
   suppressed: `m10=0`, `PASS=true`, `receipts=24`.
2. **no re-assertion.** The docstring at `:250-251` says "the superseding receipt re-asserts its
   claims against the tree", but nothing checks that. The target's claims are dropped even when
   the superseder asserts the same subject as `present=false`.

**This is a regression against the round-42 counter on the identical tree.** Round 42
(`.ufo/evidence/round-42/calibration/measure.py:187-217`) exempts only the *superseded* receipt
(`covered.add(sup)`, `:213`), only when the target exists in `receipts` (`:208`), and only when
`theirs <= mine` (`:212`) — the superseder must actually carry the claims. Differential, same
scratch repo, same rev:

```
f1043f9  predecessor receipt_audit -> 2 hits (Laundered.json, Launderer.json)
f1043f9  successor   m10            -> 0 hits
f1ce1b8  predecessor receipt_audit -> 3 hits (Laundered, Launderer, Launderer2)
f1ce1b8  successor   m10            -> 0 hits
```

The A1 commit `f0f2636` ("m7/m8/m10 corrected pre-data") replaced
`if any(key in receipt for key in supersedes) or receipt in supersedes:` with the set above;
the predecessor exempted keys only. So the *tightening* introduced the looser branch, and the
successor now reports 0 where its predecessor reported 2–3.

**Is the counter right?** No, in both parts. History is a property of the superseded receipt, not
of the superseder. *Smallest safe correction:* delete `:244` (never exempt the value), and
require re-assertion before exempting the key — reuse the predecessor's `theirs <= mine` and its
`sup in receipts` existence test. That is strictly a return to measured behaviour, not a new rule.

### F7 — m12 and m13 are substring tests; a decoy sentence satisfies both

- `m12_planned:118-121` is `hits = [] if wanted in block_text else [wanted]`.
- `m13_standing_command:165` is `if '0,3' not in newest and '0-3space' not in newest`.

S9 (`607e0cd`) replaces the round-42 block's plan with

```
This block declares no plan for its successor. The string Planned (round 43) is quoted here
only as a decoy; nothing in this block is planned.
```

and reverts the standing row to the column-zero pattern while appending prose
`(an earlier standing row used the 0,3 form)`. Result: `m12=0 m13=0 total=0 PASS=true`.

`m13`'s second half is not a command check at all: `count_patterns` runs on `indent_mirror(registry)`
*built by the counter* (`:148-155`), never on the cell's command. So the class proves "the cell
contains the terminal string `0,3`" plus "a mirror built here is countable" — nothing about the
standing command, whose own pattern, file, or existence is never tested.

**Is the counter right?** No. `m12` should bound the match to the declaration construct (e.g.
`^\*\*Planned \(round N\+1\):\*\*` at line start, with non-empty content after it), and `m13`
should either execute the cell's command against a census-valid mirror and compare its output to
`valid`, or match the census pattern shape `^ {0,3}\| S[0-9]{3} \|` as a single token. Both are
one regex each.

### F8 — supporting: the three "corrected" extraction rules have no selftest, and the record set can silently shrink

`--selftest` reports `cases=10 failed=0`, but the case list (`:280-313`) is T1×2 (m12 happy/stale),
T2×3 (m13 probe/column-zero/clean), T3×2 (m8 one resolvable + one undeclared-prefix miss), T4×2
(registry parse, `ID_RE` on plain ids), T5×1 (count claim). There is:

- **no m7 mask case** — although m7's mask is what A1 changed (`MASK_IDS` is new), and the
  round-42 counter *did* carry one (`round-42/measure.py:328-331`,
  `T4_staged_skipped_bare_counted`, `'staged:S159 maps to S001; S777'` → exactly 1). The
  successor's `T4_id_regex` tests only the unmasked direction.
- **no m10 case at all**, and m10 is the class A1 rewrote most (F6).
- **no drop-form or decoy case** for the m8 drops (F3) or the m12/m13 decoys (F7).

Consequently the selftest's `VERDICT: PASS` is evidence for exactly the happy paths and one
negative per class, and says nothing about the rules the round changed pre-data.

Also `:367-369`: if `LOG.md` lacks the literal lowercase `round 43`, `record_texts['LOG.md#round-43']`
is set to `''` with no refusal. At the freeze, `LOG.md` has no such marker (2219 lines,
`grep -c 'round 43'` = 0), so `records=3` at base and freeze: m7/m8/m11 inspect the round-42
record, the SCORECARD block and an empty LOG tail. The round record is unchecked until the marker
appears, silently.

## Axis impact

**calibration** — C2's own instrument. The class set is declared as seven classes of agreement,
but three of the five carried classes and both new classes can be passed by construction:

- m7: two unconditional masks (F1, F2) — one target class, one supporting class, both unenforced.
- m8: five drops and one fabrication (F3), plus a contradiction that makes the directory resolver
  dead for its own inputs (F4).
- m10: an unfalsifiable subject class (F5) and a *regression* that removes detections its
  predecessor made (F6).
- m12, m13: substring presence, defeated by prose (F7).
- the selftest does not exercise any of the changed rules (F8).

That is not a claim that the round's `before_state` is wrong — m12=1/m13=1 at base are reproduced
exactly, and the two classes do detect the freeze's real defects. It is that `total=0` is not
evidence of agreement: the target line is reachable with fabricated provenance, dead path cites,
false presence claims and an undeclared successor. If C2 is admitted on a `total=0`, the recorded
gain is in the records, not in the instrument.

**depth** — not judged (other seats). One cross-reference only: F6 is a pre-data change to a
frozen counter whose declared justification ("extraction rules corrected") does not hold for the
branch it loosened; any claim resting on "the counter got stricter" should not inherit it.

## Corrections, ranked by cost (all for the *next* counter revision; the freeze's
`counter_sha256` binds this round's bytes, so none may be applied now)

1. **Delete `measure.py:244` and restore re-assertion** (F6). Return to the predecessor's measured
   behaviour; 4 lines, removes a regression. Highest value, lowest risk.
2. **`next-free collides`** (F2). 3 lines at `:385`.
3. **Bound m12's and m13's matches** (F7). One regex each.
4. **Fix the m8 gate order and normalize `./`** (F4, F3-dir/dot-slash). Move the suffix gate below
   the directory test; strip a leading `./`.
5. **Brace expansion instead of brace deletion** (F3-brace). Removes a false positive that can
   block an honest PASS.
6. **Conditional `staged:` mask against the round's `staged-ids` receipt** (F1). One set lookup;
   the receipt exists at the freeze (`.ufo/waves/round-42/assimilation/staged-ids`, 103 lines).
7. **In-lane absolute and `…/` suffix resolution** (F3). One relpath; one `endswith`.
8. **Self-witnessed-directory test** (F5). `tree - {receipt}` set difference.
9. **Selftest cases** for 1–8 (F8), including the two decoy cases and the fabricated-supersedes
   case, so the class set cannot regress silently again.

If this round measures `total=0` unchanged, the honest disclosure is the instrument limit, in the
style of round 42's own "m10 is content-blind …": m7's masks are unconditional, m8 drops five cite
forms and fabricates brace forms, m10 exempts any receipt that carries `supersedes`, and m12/m13
are substring tests.

## Replay

Scratch repo stands at `/tmp/tameshi-r43-CritC2Vacuous-lane` (kept: my item names that directory
as the construction site). `EVIDENCE.txt` there holds the 13 counter runs. Re-run any row of the
table above with the command in **Method**; `git log --oneline 17f6ef0..HEAD` in the scratch repo
lists S1–S10 with their commit messages.

## Tooling

No install or upgrade: `python3` (system, 3.x) plus the lane's own `git`/`grep`/`wc`. No pacman,
no network. Scratch writes confined to `/tmp/tameshi-r43-CritC2Vacuous-*`; the only lane write is
this report.
