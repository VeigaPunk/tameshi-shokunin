# ResidualReviewC2 — independent C2 re-derivation at round-35 tip

Read-only seat; this file is my only repo write. No tools installed (nothing to record under the operator 2026-10-19 tooling directive). Scratch: none used.

## Tip observed
```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse master && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
34fa5b0cfe909f3cde644676ead723256281dd05
34fa5b0cfe909f3cde644676ead723256281dd05
```
The tip I measured equals 34fa5b0cfe909f3cde644676ead723256281dd05: **YES**.

## Counter semantics (from .ufo/evidence/round-35/c2/c2-measure.py, one line each)
- **m1**: per missing line-start key (`source:`, `verified-at:`, `recheck:`) in the header block (bytes before first `^## `) of each `corpus/knowledge/*.md` at REV whose first-add commit has BASELINE `284ab0f0…` as ancestor (`merge-base --is-ancestor`, so an entry added *at* the baseline counts).
- **m2**: per after-baseline entry whose `knowledge/<basename>` substring is absent from `corpus/README.md` at REV.
- **m3**: per untracked (`??`) regular file under fleet `.ufo/waves/` excluding `.ufo/waves/hyaku/` whose lowercased body contains `tameshi`.
- **m4**: round-33 contract `frozen_artifacts.tool_sha256` vs sha256 of `tools/tally-audit-v2.py` bytes at REV, unless `.ufo/evidence/round-35/pin-reconciliation.json` has an entry matching contract, path, old_sha256 and new_sha256.
- **m5**: round-34 `dev/authoring.stdout` has `^SEALED: .*all_as_expected=False` while `dev/authoring-receipts.json` is a nonempty list with all `as_expected is True`, and no `^# ROUND-35 ADJUDICATION` line.
- **m6**: the LAST `| sources-registry |` SCORECARD row's first `(\d+) rows` match vs count of `^\| S\d{3} \|` lines in `corpus/SOURCES.md` at REV.

## Hand derivation
### m1/m2 candidate set (after-baseline)
```
$ git ls-tree -r --name-only master corpus/knowledge | grep '\.md$' | while read -r e; do added=$(git log --diff-filter=A -1 --format=%H -- "$e"); if [ -n "$added" ] && git merge-base --is-ancestor 284ab0f0b8b989ee73d9c00c0c0df0a59757af8d "$added" 2>/dev/null; then echo "AFTER $e added=$added"; else echo "SKIP $e added=${added:-none}"; fi; done
AFTER corpus/knowledge/callback-authoritative-accounting.md added=66a25abf9a07f99df6f8584044a83a21349706a1   (…22 AFTER lines total…)
SKIP corpus/knowledge/arm-class-matrix.md added=b58b26fbeba8fd972e1d31ac8a9175a81e333b32                     (…18 SKIP lines total…)
$ git ls-tree -r --name-only master corpus/knowledge | grep -c '\.md$'
40
```
22 AFTER + 18 SKIP = 40. Edge: `closeout-r11.md` has `added=284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` — added *at* the baseline itself; `is-ancestor` includes it, identical to the frozen counter; it carries the full trio (below), so the edge changes no count.

### m1 — header trio over the 22 AFTER entries
```
$ for e in <the 22 AFTER basenames>; do h=$(git show master:"corpus/knowledge/$e.md" | awk 'BEGIN{h=1} /^## /{h=0} h{print}'); miss=''; for k in 'source:' 'verified-at:' 'recheck:'; do echo "$h" | grep -q -- "^$k" || miss="$miss $k"; done; echo "$e missing:(${miss:- NONE})"; done | grep -c 'missing:( NONE)'
22
```
All 22 lines were `… missing:( NONE)` before the count (loop re-runnable verbatim). Hand **m1 = 0**.

### m2 — README index over the 22 AFTER entries
```
$ for e in <the 22 AFTER basenames>; do c=$(git show master:corpus/README.md | grep -cF "knowledge/$e.md" || true); echo "$e readme_rows=$c"; done
callback-authoritative-accounting readme_rows=1        (…22 lines; every readme_rows >= 1: 1,1,1,2,1,2,2,1,1,1,1,2,2,1,1,1,1,1,1,1,1,4…)
$ …same loop… | grep -c 'readme_rows=0'
0
```
Hand **m2 = 0**.

### m3 — untracked tameshi wave files at the FLEET root
```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all
 M .ufo/state/chousa.report-baseline … ?? .ufo/state/kotoba.report-baseline                               (…32 lines total…)
?? .ufo/waves/hyaku/inline-run-20261023.md
?? .ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py
$ grep -ic tameshi /home/vgpnk/Projects/shokunin/.ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py
0
```
Only two `.ufo/waves/` entries: the hyaku one is excluded by class definition; the other contains no `tameshi` anywhere (a mori round-36 SOURCES.md probe). Hand **m3 = 0**.

### m4 — round-33 tool pin vs tool bytes at tip
```
$ git show master:.ufo/evidence/round-33/contract.json | python3 -c "import json,sys; a=json.load(sys.stdin)['frozen_artifacts']; print(a['tool'], a['tool_sha256'])"
tools/tally-audit-v2.py 9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4
$ git show master:tools/tally-audit-v2.py | sha256sum
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  -
```
Pin ≠ observed → reconciliation required. `.ufo/evidence/round-35/pin-reconciliation.json` at master has exactly one entry with `contract=".ufo/evidence/round-33/contract.json"`, `path="tools/tally-audit-v2.py"`, `old_sha256="9dbbce62…"`, `new_sha256="7b11ba25…"` — all four fields match the counter's requirement → reconciled. Hand **m4 = 0**.

### m5 — round-34 authoring receipt disagreement
```
$ git show master:.ufo/evidence/round-34/dev/authoring.stdout | grep -nE '^(SEALED:|# ROUND-35 ADJUDICATION)'
15:SEALED: kill=8 accept=6 all_as_expected=False
16:# ROUND-35 ADJUDICATION (round-34 seat PanelSeed4 F1; recorded 2026-10-23):
$ git show master:.ufo/evidence/round-34/dev/authoring-receipts.json | python3 -c "import json,sys; d=json.load(sys.stdin); rs=d if isinstance(d,list) else d.get('copies',[]); print(len(rs), all(r.get('as_expected') is True for r in rs))"
14 True
```
Stale `all_as_expected=False` exists, receipts all true — but the adjudication line is present in the same file → no mismatch. Hand **m5 = 0**.

### m6 — SCORECARD standing sources-registry row vs SOURCES.md
```
$ git show master:SCORECARD.md | grep -c '^| sources-registry |'
3
$ git show master:SCORECARD.md | grep '^| sources-registry |' | tail -1
| sources-registry | … row count from the re-derivable command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 99 rows at round 35 (the "96 rows" this cell carried was a round-32 observation; corrected 2026-10-23, round 35, per r34 AllFourScorecard F1); …
$ grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md
99
$ git show master:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'
99
$ git status --porcelain -- corpus/SOURCES.md corpus/README.md SCORECARD.md   → no output (working tree matches tip)
```
3 standing rows exist; counter and I take the LAST; its first `(\d+) rows` match is 99. 99 = 99. Hand **m6 = 0**.

## Frozen counter cross-check (one run)
```
$ python3 .ufo/evidence/round-35/c2/c2-measure.py --lane . --rev master --fleet /home/vgpnk/Projects/shokunin; echo EXIT=$?
C2_R35: m1=0 m2=0 m3=0 m4=0 m5=0 m6=0 total=0 entries=40 sources_rows=99 rev=34fa5b0cfe909f3cde644676ead723256281dd05 C2_R35_PASS=true
EXIT=0
```

## Six-row table
| class | hand count | counter count | verdict |
|---|---|---|---|
| m1 | 0 | 0 | agree |
| m2 | 0 | 0 | agree |
| m3 | 0 | 0 | agree |
| m4 | 0 | 0 | agree |
| m5 | 0 | 0 | agree |
| m6 | 0 | 0 | agree |

No class disagrees (total 0 = 0; secondary aggregates also match: entries 40 = 40, sources_rows 99 = 99). No DEFECT.

## VERDICT: CONFIRMED total=0

## Residual risk / verification gaps
- m3 reads the fleet working tree live; seats run concurrently, so untracked files can change between my `status` snapshot and the counter run. Both observations here saw only the hyaku file and a non-tameshi mori probe under `.ufo/waves/`.
- m1 baseline edge (entry added exactly AT `284ab0f0…` counts as after-baseline under `is-ancestor`) is interpretation, not a count defect: `closeout-r11.md` satisfies trio and README row either way.
- m6 has 3 standing rows; both derivations used the last-row rule; the "96 rows" string is a dated in-line mention, not the regex's first match.
- LSP device: not used — audited objects are committed bytes and shell-observable repo state, not source symbols; text-grep results above are presented as byte evidence only.

SEAT: TameshiR35.ResidualReviewC2 model=zai/glm-5.3-flash
