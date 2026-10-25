# ScribeQuality — round 41, wave 1: draft the pin blast-radius criterion

Read-only seat. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Contract read first and not edited: `.ufo/evidence/round-41/contract.json` (freeze `d4ee4e6`,
base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`).
Extraction window 2026-10-25T06:3xZ–06:47Z. **No counter was executed** — not the C1
calibration counter, not the C2 census counter, in any mode (`--rev`, `--rev work`,
`--control`, `--selftest`). Every command below is `git show` / `git grep` / `git cat-file` /
`sha256sum` / `sed` / `grep` / `stat` plus one read-only `python3` JSON walk.

**Outcome in one line:** the criterion this seat was asked to draft landed while I worked —
as `### Criterion 80` in `b37ce97`, already carrying my falsifier and blast-radius table. What
remains uncovered, and is therefore drafted below as **criterion 81**, is the obligation that a
declared pin be repaired and that a contract left frozen receive its `pin-reconciliation.json`
row. That gap is live at HEAD: `tools/tally-audit-v3.py` has been `da8c1ef4…` since `ae9b771`
while `.ufo/evidence/round-35/contract.json:11` still names `6188db16…` and the ledger has no
entry (`grep -c "tally-audit-v3" .ufo/evidence/round-35/pin-reconciliation.json` → 0).

## 1. How the target moved during the seat (timestamped)

| time (−0300) | bytes | state |
|---|---|---|
| 03:39:54 | `corpus/QUALITY.md` 62978 B, 985 lines | worktree only: ` M`, 20 inserted lines, no criterion 80 at `d4ee4e6` (965 lines, `grep -c` → 0) |
| 03:42:28 | `corpus/lessons/round-41.md` | untracked; `git cat-file -e d4ee4e6:corpus/lessons/round-41.md` → fatal |
| 03:43:14 / 03:43:45 | `LOG.md` / `SCORECARD.md` | ` M`, same landing |
| 03:43:41 | `.ufo/waves/round-41/w1/ScribeQuality.md` | this seat's only write |
| 06:45Z | HEAD `b37ce97` | criterion 80, the lesson and `SCORECARD.md` committed; worktree clean except `.ufo/waves/round-41/w1/` |

The worktree block I first read (`corpus/QUALITY.md:966-985`, quoted in the earlier revision of
this report) was **rewritten before commit**. The committed `### Criterion 80` at `b37ce97`:

- keeps the `git show 691bb51…` / `TOOL_SHA256` falsifier with the observed exits `d16f9b5`
  0, `691bb51` 1, `5829676` 0 — the same falsifier this seat derived independently;
- keeps the measured blast radius for `tools/tally-audit-v3.py` at `a3d6c690` (counter
  constant, contract + amendments, `c1-measure-v2.py`, `replay-empty-panel.py`, two truncated
  `SCORECARD.md` rows), which is §5 of this report;
- drops the three defects I had flagged in the pre-commit text: the `V1_SHA` name (no such
  constant exists; round 41's is `V2_SHA` at `.ufo/evidence/round-41/census/measure.py:30`),
  the falsifier that only observed `.ufo/evidence/round-41/calibration/measure.py` being absent
  at the base revision (`git cat-file -e a3d6c69:…` → absent; present at `d4ee4e6`), and the
  unqualified `grep -c 'tool_sha256'` with no path or revision.

So the review half of this seat's work is discharged by the commit, not by a new criterion.
No criterion 81 exists (`git show b37ce97:corpus/QUALITY.md | grep -c "Criterion 81"` → 0).

## 2. What the committed 80 still does not cover

`git show b37ce97:corpus/QUALITY.md | sed -n '/### Criterion 80/,$p' | grep -c "reconcil\|pin-reconciliation"`
→ `0`. It requires the declaration ("record, before the edit lands, which pins that change
breaks … the old and the new digest per pin") but says nothing about:

1. **repairing the declared pin in the same round** — a declaration that ends in a stale pin is
   the round-35 A6/A8 class again (`.ufo/evidence/round-35/contract.json:162`);
2. **the frozen-contract reconciliation row** — `pin-reconciliation.json`'s own written rule
   says a contract bytes stay frozen and "the re-pin is recorded here"; `ae9b771` re-pinned
   `tools/tally-audit-v3.py` to `da8c1ef4…` and added no row, so
   `.ufo/evidence/round-35/contract.json:11` is unreconciled *by the ledger's own rule*;
3. **no counter fires on that**: m4 (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c2/c2-measure.py:106-131`)
   reads only `.ufo/evidence/round-33/contract.json`, and `grep -rln frozen_artifacts
   --include=*.py .ufo/evidence` returns that one file.

That is the residue worth a criterion, because it is mechanically checkable at a named
revision and it is violated at HEAD.

## 3. Axes I named, and what each move bought

1. **Falsifier falsifiability** — the check must exit non-zero at a named revision *for the
   criterion's own reason*. This moved twice: the pre-commit 80 failed for a missing file;
   the landed 80 and the 81 draft both fail for a torn pin chain.
2. **Pin-class coverage** — contracts, counter/wrapper constants, capability rows (including
   truncated prefixes a full-digest grep cannot see), and the reconciliation ledger. The
   ledger row is the one class the landed criterion leaves out.
3. **Provenance** — every digest recomputed here at a named revision; worktree bytes are
   labelled ` M`/untracked and never cited as history.
4. **Conflict honesty** — §1 records that the target landed mid-seat instead of re-arguing a
   criterion that is now history, and withdraws the superseded text rather than stacking a
   duplicate 81 on the same subject.

## 4. Draft — criterion 81 (the residue), ready to paste

```markdown
### Criterion 81 — a declared pin is repaired, and a frozen contract gets its reconciliation row

Criterion 80 requires a tool edit to declare the pins it breaks before the edit lands. This
criterion requires the declaration to be discharged in the same round. Every pin named in the
blast-radius table ends the round in exactly one of two states: **re-pinned**, with a receipt
that re-derives the old and the new digest in one run (the round-37 shape:
`.ufo/evidence/round-37/counter-pin.json` with `c2-repin.py` printing
`C2_R37_REPIN_PASS=true`), or **retired** with its reason and the rounds it governed. Where
the pinned artifact's own bytes stay frozen — every `.ufo/evidence/<round>/contract.json` —
the re-pin is recorded instead as an entry in `.ufo/evidence/round-35/pin-reconciliation.json`
naming the contract, the path, the old digest, the new digest and the re-pinning round, which
is that file's own written rule. A pin that is declared and then left stale is a discovered
blast radius with a receipt attached, not a repaired one.

Lesson: `.ufo/evidence/round-35/pin-reconciliation.json` rule text; `corpus/lessons/round-36.md:67-73`
(the fix held for three pins, then re-pinned in round 37); `.ufo/evidence/round-35/contract.json:162`
(A8: "A7 re-pinned the tool to `6188db16…` but left the counter constant at `ef98fc53…` — the
same class A6 fixed one commit earlier"). Source of the reflection:
`considerthese/2026-10-24.md` proposal 1, dated 2026-10-24, mined 2026-10-25, not edited —
a declared cost is only useful if the round settles it. Criterion 80 covers the declaration;
this covers the settlement, which is why the two are separate.

Falsifier that must fail: at a revision where a contract's frozen pin and the pinned tool's
bytes disagree, the reconciliation ledger must contain the matching entry. At `ae9b771` —
the commit that re-pinned `tools/tally-audit-v3.py` to
`da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede` — the check exits 1:
`.ufo/evidence/round-35/contract.json:11` still carries
`6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354`, and
`git -C LANE show ae9b771:.ufo/evidence/round-35/pin-reconciliation.json | grep -c tally-audit-v3`
is 0. The same check exits 0 at `d9c496b` (pre-re-pin: pin and bytes agree, nothing to
reconcile) and must exit 0 once a row with `contract: ".ufo/evidence/round-35/contract.json"`,
`path: "tools/tally-audit-v3.py"`, `old_sha256: 6188db16…`, `new_sha256: da8c1ef4…` lands.
It still exits 1 at HEAD `b37ce97`, which is the live defect this criterion names.

```sh
R=ae9b771; C=.ufo/evidence/round-35/contract.json
P=$(git -C LANE show $R:$C | sed -n 's/.*"tool_sha256": "\([0-9a-f]\{64\}\)".*/\1/p' | head -1)
T=$(git -C LANE show $R:tools/tally-audit-v3.py | sha256sum | cut -d' ' -f1)
[ "$P" = "$T" ] && exit 0
git -C LANE show $R:.ufo/evidence/round-35/pin-reconciliation.json \
  | grep -q '"\''"$P"''\".*"\''"$T"''"' ] && exit 0
exit 1
```

Declared limit: the falsifier tests the ledger half, which is byte-checkable. The
"re-pinned or retired" half is checked by reading the round's receipts; it has no
single-command oracle and this criterion does not claim one.
```

Observed for the ledger half (all run here): `d9c496b` pin/bytes agree, ledger entry 0 →
clean; `ae9b771`, `e6185d5`, `a3d6c69`, `b37ce97` pin `6188db16…` vs bytes `da8c1ef4…`,
ledger entry 0 → torn.

## 5. Criterion 80's falsifier receipts (executed here, read-only)

Compare `git show REV:tools/tally-audit-v3.py | sha256sum` against the `TOOL_SHA256` in
`git show REV:.ufo/evidence/round-35/c1/c1-measure.py`.

| rev | tool sha256 (12) | counter pin (12) | exit |
|---|---|---|---|
| `d16f9b5` (round-35 tool freeze) | `da23d3a25271` | `da23d3a25271` | 0 |
| `23bd903` (A5 fix commit) | `ef98fc5367cd` | `da23d3a25271` | **1** |
| `691bb51` (A4–A7 apparatus) | `6188db16de04` | `ef98fc5367cd` | **1** |
| `5829676` (A8 re-pin) | `6188db16de04` | `6188db16de04` | 0 |

Constant line numbers: `c1-measure.py:44` at `d16f9b5`, `:46` at `23bd903`, `:53` at
`691bb51` and `5829676`.

## 6. Pin blast radius, measured (the standing table proposal 1 asks for)

**`tools/tally-audit-v3.py` at base `a3d6c69`** — live pins carrying `6188db16…`:

| pin class | path:line | form |
|---|---|---|
| counter constant | `.ufo/evidence/round-35/c1/c1-measure.py:53` | full digest |
| contract field | `.ufo/evidence/round-35/contract.json:11` | `frozen_artifacts.tool_sha256` |
| contract amendments | `.ufo/evidence/round-35/contract.json:110,152,164,168` | `amendments[3/6/7].pins_old|pins_new.tool_sha256` |
| counter constant | `.ufo/evidence/round-36/c1/c1-measure-v2.py:65` | full digest |
| replay constant | `.ufo/evidence/round-37/control/replay-empty-panel.py:24` | `FROZEN_TOOL_SHA256` |
| capability row | `SCORECARD.md:1698` | `tool tools/tally-audit-v3.py @ 6188db16…` (truncated) |
| capability row | `SCORECARD.md:1686` | `tool_sha=6188db16de045f29` (truncated) |
| reconciliation ledger | `.ufo/evidence/round-35/pin-reconciliation.json` | **no entry** — the §4 gap |

`git grep -l 6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354 a3d6c69`
returns 24 files: the four pin-bearing files above, four inherited wave spec/dispatch copies,
and 16 dated receipts the criterion does not treat as pins. The two `SCORECARD.md` rows are
invisible to that command (16-hex prefixes) and are found by
`git grep -n 6188db16 a3d6c69 -- SCORECARD.md`.

**`tools/write-path-census-v2.py`** — 3 pins: `V2_SHA`
`.ufo/evidence/round-41/census/measure.py:30`; `claims.C2.v2_sha256`
`.ufo/evidence/round-41/contract.json:44` (`d4ee4e6` numbering); capability row
`SCORECARD.md:1889` (full digest).

**`tools/write-path-census-v3.py`** — exactly 1 pin: `.ufo/evidence/round-41/contract.json:40`
(`claims.C2.tool_sha256` = `095924a7…`). The census counter does not embed the v3 digest; it
reads the pin from the contract at `.ufo/evidence/round-41/census/measure.py:146` and compares
at `:148`. [INFERENCE, code read not executed: a post-freeze edit to the v3 tool prints
`tool_sha_ok=0` unless a contract amendment re-pins `claims.C2.tool_sha256`.] That one-row
radius is the cost visibility proposal 1 exists to provide — and the round's own amendments
A1–A4 (`.ufo/evidence/round-41/contract.json:58-…` at HEAD) already use the declared form
(`frozen_field`, `old_sha256`, `new_sha256`, `before_data: true`), which is the positive shape
both criteria point at.

## 7. Findings

1. **The requested criterion landed mid-seat, as committed 80** (`b37ce97`), with the
   falsifier and blast radius of this seat's draft. The pre-commit version's three defects
   (`V1_SHA`, counter-absence falsifier, pathless grep) were fixed before commit; nothing of
   that draft survives into the report except the comparison in §1.
2. **Criterion 80 stops at declaration.** It is met by a round that writes the table and does
   nothing else; the residue is §4, and it is violated at HEAD.
3. **The reconciliation ledger is unenforced by every counter.** Its rule is written, its
   entry is missing since `ae9b771`, and m4 reads only the round-33 contract
   (`c2-measure.py:106-131`; `grep -rln frozen_artifacts --include=*.py .ufo/evidence` → 1
   file). The `b37ce97` tree is therefore self-inconsistent by the ledger's own sentence.
4. **Truncated capability-row digests remain a miss class**: 4 full-digest pin files versus
   6 pins including the two 16-hex `SCORECARD.md` rows.
5. **Ordering is what the lane got wrong, twice**: `23bd903` (A5) carried the pre-A4 pin and
   `691bb51` (A4–A7) carried the pre-A7 pin; each was repaired by a dedicated later commit
   (`f9df589`, `5829676`) titled "counter TOOL_SHA256 re-pinned".

## 8. Gates and scope

- Counters executed: **0** — no default-mode run, no `--rev work`, no `--control`, no
  `--selftest` on either round-41 counter. The R41 measurement remains entirely the L1's.
- Writes: this report only. No edit to `corpus/QUALITY.md`, the contract, either counter,
  fixtures, `SCORECARD.md`, the lesson, the lane checkout, the Git index or jj state.
- Tool installs/upgrades: **none** (nothing was needed; pacman guard untouched).
- Not done, deliberately: judging criterion 80's admission (the canonical judge's call);
  writing a general pin-auditor tool, which is outside this seat's write scope and would
  itself add pinned bytes.

Report: .ufo/waves/round-41/w1/ScribeQuality.md
