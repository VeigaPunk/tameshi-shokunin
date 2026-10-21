# Route02 — R18-2 exact append-only correction + failure-capable predicate (S008 queued vs mined)

Seat: `TameshiR19-2.Route02` (advisory leaf, round 19 attempt 1 BUILD wave, 2026-10-21).
No production edits; no subagents; no tool installs; only this report written. All
commands below were plain read-only `git show`/`diff`/`awk`/`grep` reads in the lane
(`git -C` with `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE/GIT_COMMON_DIR` unset); no lane
tool rerun. Axes touched: metadata-correctness (defect closed), no-harm (append-only),
verifiability (predicate fails closed).

## 1. Defect (verifier §5 item 2; `.ufo/evidence/round-19/contract.json` R18-2)

`corpus/lessons/round-18-verifier-spotcheck.md` §5(2) reads: "still calls S008 `queued
… not yet a mined row`, while `corpus/SOURCES.md` S008 is `mined`" and prescribes
"Sweep the metadata mention or append a correction naming it." (both: §5 item 2,
note dated by its round-18 closure, 2026-10-20/21). Target per contract.json:
`corpus/knowledge/mutation-case-kumitate-sources-check.md:1`.

### 1.1 Observed before-state (frozen baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190` and delivered lane tip `4b7c6823a462f5ea2eafcb262275300a545f3ed7`)

| Command | Observed |
|---|---|
| `git show 4b7c6823…:corpus/knowledge/mutation-case-kumitate-sources-check.md \| sed -n 1p` | Line 1 `source:` header names S008 "(paper, tier A, **queued** — Q1 quote recorded in `.ufo/waves/round-18/sources/S066-B02SrcGoogleMutation.md`, not yet a mined row)". |
| same blob at `7243e7f…`, `\| sha256sum` | `dd405bd364016819a7609a0fae7c5a987ad0e06872ff97328e4f5b1b171b96c6` — byte-identical to `4b7c6823…`; matches the wave-2 audit binding `.ufo/evidence/round-18/final/audit-1905.stdout:21` (`OPEN … sha256=dd405bd… bytes=18779`). |
| same blobs, `grep -c 'R18-2'` | `0` at both revisions (rc=1): no superseding erratum existed. |
| `git show 4b7c6823…:corpus/SOURCES.md \| awk -F'\|' S008 NF==13 {print $9,$10,$12}` | `mined`, `2026-10-19`, `corpus/knowledge/mutation-case-kumitate-sources-check.md` — registry already contradicts line 1 at the defect revision. |
| same read at `183f87b…` and at transition commit `58e5d53` | `183f87b`: `queued`, `—`; `58e5d53`: `mined` + used-by = this entry. Confirms ER8-1's "S008 is `mined` since `58e5d53`" (entry errata block). |

So the contradiction is exactly: registry `mined` + used-by since `58e5d53`, while the
entry's own line-1 provenance says queued/not-yet-mined, with no superseding erratum.

## 2. Exact append-only correction

Chosen arm: **append a correction naming it** (verifier's second option), not an
in-place sweep. This is load-bearing, not stylistic: the frozen round-19 audit
harness `.ufo/evidence/round-19/measure.py` (`source()`, lines ~101-107) requires the
pre-erratum text to still contain `**queued**` (`text(CASE).split('## Erratum R18-2',
1)[0]`), so an in-place rewrite of line 1 would score R18-2 open/fail. Append-only is
also the corpus discipline this file already follows ("the lines above stay as
written", its ER8 header).

Landed state (already committed before this seat ran — observed, not authored here):
commit `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` (2026-10-21T02:48:27-03:00,
"round-19: correct routed metadata and retain effective historical receipts") appends
exactly 12 lines to the entry (`git diff --numstat 7243e7f 21e7932 -- <entry>` →
`12 0`; commit numstat identical; zero deleted lines). The block is:

- `:266` heading: `## Erratum R18-2 — source metadata (2026-10-21, round 19)` — the
  exact split anchor the frozen harness requires, and the only occurrence in the blob
  (count 1 at HEAD).
- `:267-268`: names the superseded text — quote (14 words): "explicitly supersedes
  line 1's S008 `queued` / `not yet a` [sic, line-wrapped] `mined row` description."
- `:269-271`: grounds it — quote (12 words): "At delivered round-18 revision
  `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, S008 is `mined`, with
  `corpus/knowledge/mutation-case-kumitate-sources-check.md` in `used-by`."
- Provenance: "ER8-1 had already recorded the transition" (block tail), consistent
  with ER8-1 (landed `9ee1c80`, 2026-10-20T18:09:06-03:00) and the observed `58e5d53`
  row transition.
- Verification instruction: "Verify with that revision's `corpus/SOURCES.md` S008
  row, not with an assumed status inferred from this entry alone." (`:273`).

Every factual claim of the block re-verified by this seat: §1.1 rows above; worktree
registry row identical (`mined` / `2026-10-19` / entry used-by). Line 1 bytes are
unchanged (`**queued**` retained), satisfying the frozen harness's append-only
conjunct. No new coverage, score, or cold-read claim is made by the block; the
round-19 calibration stays 8.

In-flight note (observation only, untouched): `git status --porcelain` shows
` M <entry>` — an uncommitted ~5-line worktree delta on top of `21e7932`, presumably a
sibling seat's edit; not evaluated, not part of the landed correction.

## 3. Failure-capable predicate P-R18-2

Scoped, read-only, revision-parameterized; exit 0 = corrected, 1 = defect present,
2 = could-not-evaluate. Complements (does not contradict) the frozen harness
`measure.py::source()`, adding three failure-capabilities it lacks: append-only
enforcement (C2), grounding-revision re-check (C4), and id-cite integrity (C3).
Demonstrated below by running each conjunct as the same plain reads; the script text
is attached for executor use from `/tmp` (contract: bounded new investigation code in
`/tmp` only).

```sh
#!/bin/sh
# P-R18-2 — defect 2: entry line-1 S008 provenance vs registry. usage:
#   sh P-R18-2.sh LANE_ROOT [REV=HEAD] [BASE=7243e7f163f08978c8fd9b6c1ef67a2fefe7d190]
L=${1:?lane root}; REV=${2:-HEAD}; BASE=${3:-7243e7f163f08978c8fd9b6c1ef67a2fefe7d190}
ENTRY=corpus/knowledge/mutation-case-kumitate-sources-check.md
G() { env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git -C "$L" "$@"; }
fail() { echo "P-R18-2: FAIL($REV) $*"; exit 1; }

# C1 registry ground truth at REV: exactly one S008 row, 13 cells, status mined,
#    opened 2026-10-19 unchanged, used-by names the entry (census v1 shape).
row=$(G show "$REV:corpus/SOURCES.md" 2>/dev/null | awk -F'|' '
  /^\|[[:space:]]*S008[[:space:]]*\|/ && NF==13 {
    s=$9; o=$10; u=$12; gsub(/[[:space:]]/,"",s); gsub(/[[:space:]]/,"",o); print s"|"o"|"u }')
[ -n "$row" ] || { echo "P-R18-2: COULD-NOT-EVALUATE no S008 row at $REV"; exit 2; }
[ "$(printf '%s\n' "$row" | grep -c .)" -eq 1 ] || fail "S008 row not unique"
st=$(printf '%s' "$row" | cut -d'|' -f1); op=$(printf '%s' "$row" | cut -d'|' -f2)
ub=$(printf '%s' "$row" | cut -d'|' -f3)
[ "$st" = mined ] || fail "S008 status=$st not mined"
[ "$op" = 2026-10-19 ] || fail "S008 opened=$op drifted"
case $ub in *"$ENTRY"*) ;; *) fail "S008 used-by lacks entry";; esac

# C2 append-only: zero deleted lines in ENTRY from BASE to REV.
d=$(G diff --numstat "$BASE" "$REV" -- "$ENTRY" | awk '{print $2}')
[ -n "$d" ] || { echo "P-R18-2: COULD-NOT-EVALUATE empty numstat"; exit 2; }
[ "$d" = 0 ] || fail "entry deleted $d line(s) vs BASE"

# C3 id-cite intact: line 1 still names S008 (mined-row used-by integrity).
ent=$(G show "$REV:$ENTRY") || { echo "P-R18-2: COULD-NOT-EVALUATE entry unreadable"; exit 2; }
printf '%s\n' "$ent" | sed -n '1p' | grep -q 'S008' || fail "line 1 lost S008 id-cite"

# C4 stale provenance must be superseded by an appended erratum naming line 1,
#    mined, and a 40-hex revision at which the registry is already mined.
if printf '%s\n' "$ent" | sed -n '1p' | grep -Eq '\*\*queued\*\*|not yet a mined row'; then
  note=$(printf '%s\n' "$ent" | awk 'f{print} /^## Erratum R18-2/{f=1}')
  [ -n "$note" ] || fail "stale line 1 with no Erratum R18-2 section"
  printf '%s\n' "$note" | grep -q 'line 1'    || fail "erratum does not name line 1"
  printf '%s\n' "$note" | grep -q 'mined'     || fail "erratum does not state mined"
  R=$(printf '%s\n' "$note" | grep -m1 -oE '[0-9a-f]{40}')
  [ -n "$R" ] || fail "erratum names no 40-hex revision"
  G show "$R:corpus/SOURCES.md" | awk -F'|' '
    /^\|[[:space:]]*S008[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); print s}' \
    | grep -qx mined || fail "registry not mined at erratum revision $R"
fi
echo "P-R18-2: PASS($REV)"; exit 0
```

### 3.1 Demonstrated truth table (conjuncts run as inline reads, 2026-10-21)

| REV | C1 | C2 | C3 | C4 | Result |
|---|---|---|---|---|---|
| `4b7c6823…` (delivered round-18 tip) | mined/2026-10-19/used-by ✓ (§1.1) | n/a | ✓ | **fails**: `R18-2` count 0 in blob `dd405bd…` | **FAIL — defect present** (fail-closed) |
| `7243e7f…` (frozen baseline; entry byte-identical, sha256 match) | ✓ | n/a | ✓ | **fails**: count 0 | **FAIL — defect present** |
| `21e7932…` (HEAD, correction landed) | ✓ worktree+HEAD registry row | `12 0` deleted=0 ✓ | line 1 names S008 ✓ | erratum `:266` names line 1 + `mined` + 40-hex `4b7c6823…` (blob `:270`); registry mined at that rev ✓ | **PASS** |
| hypothetical in-place sweep of line 1 (argued, not run) | ✓ | **fails**: deletions > 0 | – | skipped (stale text gone) | **FAIL — rewrite detected** |

Frozen-harness consistency: the landed block satisfies every `measure.py::source()`
conjunct this seat could observe — split anchor `## Erratum R18-2` present exactly
once, `line 1` + REV18 + `mined` in the note, `**queued**` retained pre-split
(numstat 12/0), S008 row unique/13-cell/`mined`/`2026-10-19`/used-by — so the wave
audit should read R18-2 = corrected at `21e7932`, agreeing with P-R18-2.

## 4. Residual risk and verification gaps

- The worktree's uncommitted entry delta (§2 note) is unevaluated; if it lands,
  rerun `P-R18-2.sh <lane> <new-HEAD> 7243e7f…` — the predicate is
  revision-parameterized for exactly this.
- C4 accepts any 40-hex revision named in the erratum at which the registry is
  already mined; a *wrong-but-mined* revision would pass C4 alone. Mitigated by the
  frozen harness's exact `REV18` string match, which P-R18-2 complements rather than
  replaces. Advisory verdicts from either tool remain recommendations.
- Defect 2 is metadata hygiene only; the verifier's own scoping — "None of these
  changes a claim verdict" (§5, 7 words) — is consistent with everything observed
  here; no claim or score is affected, and the 18 guard survivors remain open debt.
- Observation vs inference: §1/§2/§3.1 rows are observed commands/outputs; the
  in-place-sweep row of §3.1 and the sibling attribution of the worktree delta are
  inference; nothing in scope is unknown-blocking.
