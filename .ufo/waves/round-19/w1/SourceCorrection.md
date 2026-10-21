# SourceCorrection — connector: SOURCES mutable-cell exception × five-row arithmetic × correction language

Seat `TameshiR19-2.SourceCorrection` (connector, round 19 attempt 1, w1, 2026-10-21).
This seat was read-only. This file is its only write. It made no production edit, ran no lane tool, selftest, build or test, and installed no tool.
Lane state as observed: `HEAD` = `master` = `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`. The L1 working tree was changing during the read:
`measure.py`, `corpus/SOURCES.md` (+3/−3), `round-19.md`, `LOG.md`, `SCORECARD.md` and two knowledge notes were modified. The in-flight
ruler's sha256 changed during this read (`1d275750…` → `e9b44cad…`). The committed ruler is `c538c33d…`.
Labels: **O** = observed, **I** = inference, **U** = unknown.

## Axes

- A1, calibration (C1): R18-3 counts as durably corrected only when the corrected statement is true and the same mistake does not recur in round 19.
- A2, verification: the R18-3 check should be able to fail against the historical SOURCES bytes, not only against the lane's own transcript.
- A3, source contract: three rules apply to SOURCES.
  - CORPUS SOURCES rule 2 (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`): "Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new".
  - QUALITY 35 (`corpus/QUALITY.md:262-279`): a footer is a literal append.
  - QUALITY 38 (`:344-351`): name the unit, and check immutable cells separately.
- A4, honest correction language.
- No-harm boundary: score 8 unchanged, no promotion, population stays five, historical bytes retained, no fleet or sibling edit, 18 survivors stay open.

## Evidence (read-only commands → observed)

| # | Command / source | Observed (O) |
|---|---|---|
| E1 | `git log --numstat 183f87b..21e7932 -- corpus/SOURCES.md` | `58e5d53` 15/2, `9ee1c80` 11/4, `21e7932` 9/1. No other commit in the range touches SOURCES. |
| E2 | `git diff --numstat 183f87b… 4b7c682… -- corpus/SOURCES.md` | `25 5`. Byte-equal to the last line of `.ufo/evidence/round-19/sources-diff.txt`. |
| E3 | Row-keyed cell audit (code below) over `git show REV:corpus/SOURCES.md` | See the window × unit table. |
| E4 | `git show REV:corpus/SOURCES.md \| grep -n 'Next unused id'` at 183f87b, 58e5d53, 9ee1c80, 4b7c682, 21e7932 | `:195 S065.` → `:208 S075.` (S065 line gone) → `:212 S065.` restored, `:213 S075.`, `:215 S079.` → unchanged → unchanged. |
| E5 | `git blame -s -L 45,52 -L 77,79 -L 113,116 4b7c682 -- corpus/lessons/round-18.md` | Lines 45–52 and 79 come from `4acdeac` (18:11:43), which is after both `58e5d53` and `9ee1c80`. Lines 113–116 come from `5923d89`. |
| E6 | `grep -c 'only in-place'` / `'four allowed'` per revision | Both strings first appear at `4acdeac`. At `21e7932`, `four allowed` appears twice: line 79 and the R18-3 quote at :123. `only in-place` appears once (line 48), and nothing supersedes it. |
| E7 | `measure.py` `arithmetic()`, committed at :105-111 and in flight at :120-128 | It checks the phrase `five deleted table lines`, that all five IDs are present, regex `^25\s+5\s+corpus/SOURCES\.md$` on `sources-diff.txt`, and (in flight) `DIFF_COMMAND` plus the retained line-79 text. It never reads historical SOURCES bytes. |
| E8 | `scripts/sources-census.sh:12` modes; grep `git\|--rev\|--base\|previous\|old→new` | Modes are `census\|validate\|overdue\|shared\|selftest`. The grep found no matches. No fleet tool compares two revisions, so nothing anywhere executes rule 2. |
| E9 | `git status --porcelain -- corpus/SOURCES.md`; `git diff --numstat` | ` M`, `3 3`. The pending working tree (sha256 `b684833d…2ebe`) changes S063, S077 and S078 `used-by` only. |
| E10 | Old→new check of `round-19.md` against the blobs (S049, S063, S077, S078) | The lesson's old lists and new lists match the bytes. `status` and `recheck` are unchanged. Rule-2 logging is accurate. |
| E11 | `env \| grep ^GIT_` | Only `GIT_EDITOR`, `GIT_PAGER` and `GIT_TERMINAL_PROMPT` are set. None changes which repository is read. Audit reads also used scrubbed env and `GIT_CONFIG_GLOBAL=/dev/null`. |

## Window × unit table (O, E1/E3/E4/E9)

| Window | Deleted table lines (IDs) | Changed cells | Immutable-cell changes | Deleted non-row lines | Rows |
|---|---|---|---|---|---|
| 183f87b..58e5d53 | 1 (S008) | 2 (S008 status + used-by) | 0 | **1** (`- Next unused id: S065.`) | 62→72 |
| 58e5d53..9ee1c80 | **4** (S001/S052/S056/S057) | **4** (used-by) | 0 | 0 (footer re-inserted) | 72→76 |
| 9ee1c80..4b7c682 | 0 | 0 | 0 | 0 | 76 |
| **net 183f87b..4b7c682** | **5** (S001/S008/S052/S056/S057) | **6** (used-by ×5, status ×1) | 0 | 0 | 62→76, no ID removed |
| 7243e7f..21e7932 | 1 (S049) | 1 (used-by) | 0 | 0 | 76 |
| 21e7932..worktree (pending) | 3 (S063/S077/S078) | 3 (used-by) | 0 | 0 | 76 |
| **net 7243e7f..worktree** | **4** (S049/S063/S077/S078) | **4** (used-by) | 0 | 0 | 76→76; +12/−4 |

Composition of the net range 183f87b..4b7c682: +25 = 5 replacement row lines + 14 new rows (S065–S078) + 6 non-row lines.
The per-commit deleted lines sum to 6. The net count is 5 because the footer was deleted and then restored, and the two cancel.

## Findings

- **F1 — The "four" is a window error, not only a unit error.**
  - O: line 79's "four allowed used-by cells" exactly matches the single-commit window `58e5d53..9ee1c80`: 4 lines and 4 cells.
  - O: line 48's "(the only in-place row change)" exactly matches `183f87b..58e5d53`.
  - O: both lines were authored at `4acdeac`, after both commits. The falsifier's own command spans `183f87b..<final>`, where the counts are 5 lines and 6 cells. "Four" is wrong in both units over that range.
  - I: the author took each count from one commit and stated it over the range.
  - Contradiction, kept open:
    - The round-19 Mistakes row 2 says "confuses rows and cells" (`round-19.md:51`), and QUALITY 38 says a count "names its unit". Neither names the window.
    - The round-19 Gate row title "five deleted source lines, not four cells" (`round-19.md:19`) suggests four is the right cell count. The cell count is six.
- **F2 — A second same-class stale count is unsuperseded.**
  - O: the R18-3 erratum says it "supersedes line 79's" text (`round-18.md:123`). Line 48 still states a one-row in-place count for the round's Gate.
  - The QUALITY 37 standard (`QUALITY.md:338-340`, 2026-10-21) is "never leave a second current-result implication". It is stated for metadata corrections.
  - L1 is already applying that sweep to R18-1 and R18-2 (working-tree sweep addenda). R18-3 is the only one of the three metadata items without its residual named.
- **F3 — The net falsifier cannot see a delete-then-restore.**
  - O: `58e5d53` deleted a non-row line (the footer). `9ee1c80` restored it byte-identically.
  - "zero deleted non-row lines" (`round-18.md:131-132`) is therefore a statement about the net window only. The round's own append-only breach, which line 79's row records, is invisible to it.
- **F4 — The erratum's three-part falsifier is asserted, not executed.**
  - O, E7: the R18-3 predicate trusts a two-line, lane-authored transcript. The transcript has no exit code and no digest.
  - The predicate never derives which IDs changed, which cells changed, or whether non-row lines were deleted.
  - QUALITY 38's "checks immutable cells separately" is implemented only for S008's `opened` cell, under R18-2 in flight.
  - O, from my re-implementation of the in-flight predicate; I did not run the lane ruler. On the real bytes, the in-flight predicate and the derived one both pass. The in-flight predicate also passes all four mutants below; the derived one fails every one:
    - M1: the erratum adds an extra ID, S049.
    - M2: the history is the 4-row window while the transcript still says `25 5`.
    - M3: S052's `teaches` cell is edited.
    - M4: the footer is deleted.
- **F5 — Round 19 is repeating the round-18 pattern right now.**
  - O, E9/E10: `21e7932` changed one row (S049). The pending sweep changes three more (S063, S077, S078). The net round-19 range will therefore have **4 deleted table lines = 4 used-by cells**, the same number as line 79, now true for a different window.
  - The working-tree lesson says "No immutable cells, added rows or tiers." That sentence is true per E3, but nothing executes it.
  - w1 statements such as "SOURCES 9/1, one deletion = S049" (`GateDraft.md`, `MetadataDraft.md` #19) are correct for `21e7932` only.
- **F6 — Wording problems.**
  - R18-3 says "those five removed row IDs" (`round-18.md:131`). In fact no row ID was removed (62→76). The five lines were replaced lines.
  - QUALITY 38's falsifier cites "the recorded historical diff", which is the transcript, not a derived diff.

## Proposed move (one): derive, don't trust — one rule-2 audit function, used for R18-3 and for round 19's own range

Fold the change into the ruler strengthening L1 already has in flight. The working-tree LOG says "final measurements apply one strengthened ruler to both endpoints", so this adds no extra re-measure.

1. **The audit function.** It takes two pinned SOURCES blobs, read with `git show <fixed commit>:corpus/SOURCES.md` whatever `--rev` is, and records their digests in `inputs`. It returns:
   - the changed row IDs;
   - the changed column names per row;
   - any immutable-cell changes (columns other than `status`, `recheck`, `used-by`);
   - any removed IDs;
   - whether the base's non-row lines are an ordered subsequence of the final's. This is QUALITY 35's "literal append" check for footer, search-log and paths lines.
2. **R18-3 predicate.** Keep the current text checks, and add:
   - changed IDs == `['S001','S008','S052','S056','S057']`;
   - no immutable-cell changes;
   - no removed IDs;
   - non-row lines append-only;
   - the last line of `sources-diff.txt` equals the computed `git diff --numstat` output. This verifies the transcript instead of trusting it, and the transcript stays byte-identical.

   At baseline `7243e7f` the item stays open, because the erratum is absent. At `21e7932`, all derived checks pass on the real bytes.
3. **Failure demonstrations.**
   - Selftest, keeping fixtures synthetic as now: an S008-only window that also deletes the footer; a four-row window; an immutable `teaches` edit; a removed ID.
   - A separate committed receipt runs the audit on the real windows. Expected:
     - `183f87b..58e5d53` fails on IDs and on the non-row deletion;
     - `58e5d53..9ee1c80` fails on IDs (exactly line 79's four);
     - the net range passes.

     This is CORPUS.md:179-184 ("A fix is shown able to fail before it counts"), demonstrated on real history.
4. **Round-19 no-harm line.** Report it, but do not count it among the five. Run the same function on `7243e7f..<delivered>`, both per commit and net. Expected result: {S049}, then {S063, S077, S078}, net four rows, `used-by` only, no immutable-cell changes, non-row lines append-only. Round 19's SOURCES statements are then derived, not recalled.
5. **Language, append-only.** The draft below goes in one dated addendum at the end of `round-18.md`. Its heading does not start with `## Erratum R18-3`, so the ruler's first-occurrence split and the `\n## ` bound stay unchanged. Add one sentence to the round-19 no-harm text.

Draft addendum for `corpus/lessons/round-18.md`:

> ## Addendum to R18-3 — counting window (2026-10-21, round 19)
> R18-3's counts are net over `183f87b899e6cae46be98d251cbc87fb5118f6ca` → `4b7c6823a462f5ea2eafcb262275300a545f3ed7`:
> - 5 replaced table lines; no row ID was removed (62→76 rows);
> - 6 changed mutable cells (`used-by` ×5, S008 `status` ×1);
> - 0 immutable-cell changes;
> - 0 net deleted non-row lines.
>
> Per commit:
> - `58e5d53d6a638fb72042d1f6607b24018aa299a8` replaced S008 and deleted the footer line `- Next unused id: S065.`;
> - `9ee1c8046295baf6c133c8d43b8315d562498aea` restored that footer line and replaced S001, S052, S056 and S057 (`used-by` only).
>
> Line 48's "the only in-place row change" holds for the first window only. Line 79's "four" equals the second window, not the range its command names. Both lines are retained as window-scoped history. A net count cannot detect the restored footer deletion; line 79's own row records it.

Draft round-19 no-harm sentence, filled in from the audit at the delivered revision:

> SOURCES `7243e7f…` → `<delivered>`: 4 replaced table lines (S049 at `21e7932`; S063/S077/S078 at `<rev>`), 4 changed `used-by` cells, 0 immutable-cell changes, 0 deleted non-row lines, 76→76 rows. Each change is logged old→new above, and the same audit function is used for R18-3.

Optional, appended to QUALITY: "a diff count names its unit **and its window**; a net count cannot detect a delete-then-restore".

## Affected axes, risks, verification

- **Gains.**
  - A1: R18-3 is checked against what actually happened, and the same failure mode is guarded in round 19's own sweep.
  - A2: the predicate catches M1–M4.
  - A3: rule 2 and the QUALITY 35/38 checks become executable for the first time. Before this, nothing executed them (E8).
  - A4: the language states only what the audit computes.
- **No harm:** the population and score are unchanged; `sources-diff.txt`, line 48 and line 79 stay byte-identical; nothing in the fleet changes.
- **Risks.**
  - The ruler sha changes, so the before and after receipts must be re-taken. Fold this into the existing strengthening pass rather than producing a third ruler.
  - Snapshot fixtures need keys for the two pinned blobs.
  - Use the row-keyed audit for the semantics. Use `git diff --numstat` only to verify the transcript in `--rev` mode, because the line-diff algorithm could otherwise matter. Python `difflib` counts matched git's on every range here.
  - Prefer a constant ID list checked against the history over set-equality on prose IDs, which is brittle.
  - U: the round-19 numbers assume the sweep lands as in working-tree `b684833d…`.
  - U: the in-flight ruler may change after this read.
- **Verify (L1 or a non-author):**
  - `git diff --numstat` per window, as in E1/E2.
  - Run the code below and expect the table above.
  - At the delivered revision, the strengthened ruler should report R18-3 `corrected`.
  - Mutants M1–M4 should reopen R18-3 only.
  - The real-window receipt should fail on exactly the reasons listed in move step 3.

## Code (bounded investigation, read-only; run in the eval kernel; no files written)

```python
import subprocess, os, re
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
ENV={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}; ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
ROW=re.compile(r'^\|\s*(S\d{3,})\s*\|')
COLS=['id','source','kind','tier','scope','anchor','teaches','status','opened','recheck','used-by']; MUT={'status','recheck','used-by'}
def show(rev, path='corpus/SOURCES.md'):
    r=subprocess.run(['git','-C',L,'show',f'{rev}:{path}'],env=ENV,capture_output=True); assert r.returncode==0; return r.stdout.decode()
def rows(t): return {m.group(1):(l,[c.strip() for c in l.split('|')[1:-1]]) for l in t.splitlines() for m in [ROW.match(l)] if m}
def is_subseq(small,big):
    it=iter(big); return all(any(x==y for y in it) for x in small)
def cell_audit(base, final):
    rb,rf=rows(base),rows(final); changed={}; immut=[]
    for i in rb:
        if i not in rf: immut.append((i,'row-removed')); continue
        cb,cf=rb[i][1],rf[i][1]
        if len(cb)!=11 or len(cf)!=11: immut.append((i,'malformed')); continue
        d=[COLS[k] for k in range(11) if cb[k]!=cf[k]]
        if d: changed[i]=d
        immut+=[(i,c) for c in d if c not in MUT]
    nb=[l for l in base.splitlines() if not ROW.match(l)]; nf=[l for l in final.splitlines() if not ROW.match(l)]
    return dict(changed_rows=sorted(changed), cells=changed, immutable=immut, nonrow_append_only=is_subseq(nb,nf))
# windows audited: 183f87b..58e5d53, 58e5d53..9ee1c80, 9ee1c80..4b7c682, 183f87b..4b7c682,
# 7243e7f..21e7932, 21e7932..worktree, 7243e7f..worktree (worktree = open(L+'/corpus/SOURCES.md').read())
```
