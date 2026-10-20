# EvidenceImmutable — historical evidence immutability (round 16, wave 2)

Seat `TameshiR16.EvidenceImmutable`. Lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Snapshot `2026-10-20T10:55:56-03:00`.
Base `28aeef498cc070c3183271b709bc79d344ff547a` ("round-15 verifier spot-check") → tip
`c699c8c36d6e4eca4b796b81a8247904aa145ec8` ("round-16: land js-round-gate case 7, …"; tip is
`origin/master` and `origin/HEAD`, i.e. pushed).

## Verdict

**holds** — the assigned diff is exactly **38 additions** (37 under `.ufo/evidence/round-16/`,
1 `corpus/lessons/round-16.md`), **0 modifications, 0 deletions, 0 renames**. Independent
blob-by-blob comparison shows all **749** paths that existed at base in the three dirs are
byte-identical at tip, including mode and type; and the prior verifier spot-check artifacts and
the concrete anchors they name re-verify at the revisions they name.

## Attacked

1. The assigned `git diff --stat` claim itself.
2. An independent path → (blob SHA, mode) tree comparison, not a second diff invocation.
3. The three intermediate commits between the endpoints, for transient modify/revert.
4. Working-tree bytes for every base-era file (all 749), index flags, filters, replace refs/grafts.
5. Prior verifier spot-check files + re-execution of the concrete anchors named in
   `corpus/lessons/round-15-verifier-spotcheck.md:89` and `:93`.

## 1. Assigned check

Command, exit 0:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat \
  28aeef4 c699c8c36d6e4eca4b796b81a8247904aa145ec8 -- .ufo/evidence/ corpus/lessons/ reports/
```

Key output line: ` 38 files changed, 6523 insertions(+)`.
`git diff --numstat` over the same range sums to `add=6523 del=0`.
`git diff --name-status` over the same range: 38 lines, **all `A`** (`A=38 M=0 D=0 R=0`).
`git diff --quiet --diff-filter=DM 28aeef4 c699c8c -- .ufo/evidence/ corpus/lessons/ reports/`
→ exit 0 (no modified, no deleted path).

Added paths (all under the two allowed locations; 37 + 1 = 38):

```
A .ufo/evidence/round-16/attribution/correction-attrfix-draft.json
A .ufo/evidence/round-16/attribution/correction.json
A .ufo/evidence/round-16/attribution/reattribute.py
A .ufo/evidence/round-16/census-start.txt
A .ufo/evidence/round-16/coldread/SKILL.snapshot.md
A .ufo/evidence/round-16/coldread/assemble.py
A .ufo/evidence/round-16/measure.py
A .ufo/evidence/round-16/round-gate/predictions.json
A .ufo/evidence/round-16/round-gate/round-gate.defects.spec
A .ufo/evidence/round-16/round-gate/runner-regression.txt
A .ufo/evidence/round-16/round-gate/runner-selftest.txt
A .ufo/evidence/round-16/round-gate/runner-sha256.txt
A .ufo/evidence/round-16/round-gate/suite.txt
A .ufo/evidence/round-16/round-gate/survivor-probes/A2-P1-mutant-A2.log
A .ufo/evidence/round-16/round-gate/survivor-probes/A2-P1-pristine.log
A .ufo/evidence/round-16/round-gate/survivor-probes/A2-P1b-mutant-A2.log
A .ufo/evidence/round-16/round-gate/survivor-probes/A2-P1b-pristine.log
A .ufo/evidence/round-16/round-gate/survivor-probes/B2-P6-mutant-B2.log
A .ufo/evidence/round-16/round-gate/survivor-probes/B2-P6-pristine.log
A .ufo/evidence/round-16/round-gate/survivor-probes/E1-P9-mutant-E1.log
A .ufo/evidence/round-16/round-gate/survivor-probes/E1-P9-pristine.log
A .ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs
A .ufo/evidence/round-16/round-gate/sweep/defects.tsv
A .ufo/evidence/round-16/round-gate/sweep/evidence/A1.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/A2.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/A3.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/B1.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/B2.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/C1059.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/C1060.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/CKIND.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/E1.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/E3.out
A .ufo/evidence/round-16/round-gate/sweep/evidence/control.out
A .ufo/evidence/round-16/round-gate/sweep/results.tsv
A .ufo/evidence/round-16/round-gate/sweep/spec.copy
A .ufo/evidence/round-16/round-gate/sweep/sweep.log
A corpus/lessons/round-16.md
```

## 2. Independent blob-map comparison

Method: `git ls-tree -r -z <rev> -- .ufo/evidence corpus/lessons reports`, parsed as
`path → (blob SHA, mode, type)`, base map vs tip map (not `git diff`).

- base entries **749**, tip entries **787**; added **38**, deleted **0**, modified **0**
  (no mode/type changes, so no `100644↔100755` or file↔symlink/gitlink churn on old paths).
- added outside `.ufo/evidence/round-16/` or `corpus/lessons/round-16.md`: **0**.
- `reports/` tree object identical at both revisions:
  `09ee9091356d50c6e2c2f26ae42109f8edef1592` (9 files: r7–r11 audit/verifier notes, round-1
  calibration/cold-read).
- `corpus/lessons/` tree hash changes only because `round-16.md` is added; the 11 base-era
  lesson files, including all five `*-verifier-spotcheck.md`, keep identical blob SHAs.
- `.ufo/evidence/` changes only by the 37 `round-16/` additions; all pre-existing round-1…15
  evidence blobs keep identical SHAs.
- Added file modes: 34 × `100644`, 4 × `100755` (scripts: `measure.py`, `reattribute.py`,
  `assemble.py`, `probes.mjs`). Executable bits are additions, not edits to prior files.
- Path hygiene: 0 case-fold collisions, 0 NFC collisions, 0 control characters, no `..`
  segments, no trailing-whitespace names among the additions.

## 3. Intermediate history

`git merge-base --is-ancestor 28aeef4 c699c8c` → exit 0; `rev-list --count 28aeef4..c699c8c` = **3**:

| commit | subject | all changes | changes in the three scoped dirs |
|---|---|---|---|
| `0baf52e` | considerthese: 2026-10-20 daily reflection | 1 A | none |
| `e69b488` | round-16: pre-register js-round-gate mutation predictions; retain wave-1 seat reports | 84 A | 5 A, 0 M/D (`census-start.txt`, `coldread/SKILL.snapshot.md`, `round-gate/{predictions.json,round-gate.defects.spec,suite.txt}`) |
| `c699c8c` | round-16: land js-round-gate case 7, cold-read repairs, sources S052–S057, attribution repair | 35 A, 11 M | 33 A, **0 M/D** |

The 11 `M` paths in `c699c8c` are all outside the assigned pathspec: `.ufo/waves/round-16/w1/
CRMeasure.md`, `PROVINCE.md`, `SHONEN.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`,
`corpus/SOURCES.md`, `corpus/knowledge/{arm-class-matrix,fleet-kill-rate-ledger,
repeated-control-precondition}.md`, `tools/mutate-and-run.sh` (plus 2 non-scope additions:
`corpus/knowledge/mutation-case-kumitate-round-gate.md`, `.ufo/waves/round-16/w1/CRLedger.md`).
So there is no modify-then-revert of prior evidence hidden between the endpoints.

History-rewrite checks: `git replace -l` → empty; `.git/info/grafts` absent;
`rev-parse --is-shallow-repository` → `false`.

## 4. Prior verifier spot-checks byte-identical

The base commit itself is the round-15 verifier spot-check and adds exactly one file:
`corpus/lessons/round-15-verifier-spotcheck.md` (172 lines). Its SHA-256 is **identical at base,
tip, and in the worktree**: `cbc9a81176afbb0e723458e3629c5080f19eb2ecb8c4172753b8b55e55d96fde`.

Other prior verifier artifacts, SHA-256 base = tip = worktree (all byte-identical):

| path | sha256 |
|---|---|
| `corpus/lessons/round-1-verifier-spotcheck.md` | `f99ef0ae2b3a3e4939c86b9ce5ab1e701733801c1cc1c7063767edf692e0edad` |
| `corpus/lessons/round-12-verifier-spotcheck.md` | `6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30` |
| `corpus/lessons/round-13-verifier-spotcheck.md` | `6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420` |
| `corpus/lessons/round-14-verifier-spotcheck.md` | `d267576a0d165d81b734b6c40b5b80bf61ccd9c24c8765992093afbd097cf654` |
| `corpus/lessons/round-15-verifier-spotcheck.md` | `cbc9a81176afbb0e723458e3629c5080f19eb2ecb8c4172753b8b55e55d96fde` |
| `reports/r8-ver-t8.md` | `f2c8d91d6d441569827f60f6b922d5f96f445d56ee13c8ff3cb55d0978a5378c` |
| `reports/r9-ver-t9.md` | `803ec00849347b5458a3298605236d987f20885130bea17a886115def737b180` |

All 25 `.ufo/evidence/round-15/` blobs are identical base vs tip.

Re-executed anchors from the round-15 spot-check record (not a rerun of the gate):

- `corpus/lessons/round-15-verifier-spotcheck.md:89` claims a rounds-12–14 blob-map comparison of
  599→599 paths, 0 changed/missing, 0 added. Recomputed independently at base vs tip: base=599,
  tip=599, missing=0, added=0, changed=0. **Agrees.**
- Same line names runner SHA-256 `75ed934d…` and summary `acc01268…`. Located and re-hashed:
  `75ed934d…` = `tools/mutate-and-run.sh` at `7650fe4`, `9f2c86f`, and base `28aeef4`;
  `acc01268…` = `.ufo/evidence/round-12/BashWitness/summary.json` (identical at base and tip).
  **Agrees at the named revisions.**
- `:93` claims `verification-3.json` requested `7650fe4`, passed=true, failed_checks=[],
  44 checks all passed. Parsed `.ufo/evidence/round-15/verification-3.json`: `requested_rev`
  `7650fe4db89f…`, `passed: true`, `failed_checks: []`, 44/44 checks with `passed: true`.
  `attempt-3/expected.json` resolves `7650fe4…` (requested and resolved identical).
  Its **5 source bindings + 6 frozen expected/receipt files = 11/11 SHA-256 matches at
  `7650fe4` and 11/11 at `9f2c86f`**; the prefix binding resolves at `bca5deb`; maintained
  source `tools/context-capture.py` = `c4a1d165…` at `7650fe4`, `9f2c86f`, base and tip;
  all six frozen files exist at `b255055`. **Agrees.**
- `:5` names the fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-15/tameshi.md`
  at commit `800cf862…`. SHA-256 `7c1d06a2a9b728ed515fca8c2965b4404de879fe051f81389ef9592787bd75af`
  at `800cf862`, at fleet HEAD `5a228cd9…`, and in the worktree — identical. **Agrees.**

Boundary on the "byte-identical" reading: the round-15 record's runner digest verifies at the
revisions it names (`7650fe4`, `9f2c86f`, base `28aeef4`), **not at tip**: round-16 changed
`tools/mutate-and-run.sh` (tip SHA-256 `89722ddb3082abd6…`), and `PROVINCE.md`, `SHONEN.md`,
`SKILL.md` also differ at tip. Those are round-16 artifacts/tools outside
`.ufo/evidence/ corpus/lessons/ reports/`, not evidence mutation; flagged so no one over-reads
"prior spot-check anchors byte-identical" as covering `tools/` or top-level round artifacts at tip.

## 5. Modified / deleted paths

**Committed history, scoped: none.** `--diff-filter=DM` empty (exit 0); tree maps show
0 deleted, 0 modified among the 749 base-era paths.

Working tree, post-commit (observed at the snapshot above; sibling wave-2 seats are actively
writing, so this list moves):

| path | state | committed bytes vs worktree | note |
|---|---|---|---|
| `.ufo/evidence/round-16/measure.py` | `M` | sha256 `dc3483609d14a8ef…` vs `a8f105c29f45a4e0…`, 36+/2− | round-16 L1 repair (`measure.py:142`); `measure-repair/` manifests record old `box3_ledger_link:false` → repaired `true`; round-16 file, not historical |
| `corpus/lessons/round-16.md` | `M` | sha256 `1e0dc9fa20defdf8…` vs `ab32a1e8590a4ad1…`, +1 line | added `:57` "vacuous" disclosure row; round-16 file, not historical |
| `.ufo/waves/round-16/w1/Overlap1.md` | `M` | +2 lines | wave-1 seat report, not evidence |

Untracked additions under `.ufo/evidence/round-16/` only (all additions, no historical path):
`Overlap1/{manifest-replay.txt,manifest.sha256}`,
`measure-repair/{old-tool-at-c699c8c.json,repaired-tool-at-c699c8c.json}`,
`round-gate/survivor-probes/c1059-{mutant.log,pristine.log,probe.sh}`.

No historical (base-era) path is modified or deleted in the worktree either: every one of the
749 base-scope files was hashed from the working tree and matches its base blob — 0 mismatches,
0 missing. `git ls-files -v` over the scope lists 787 entries with **0** assume-unchanged
(`h`) or skip-worktree (`S`) flags; there is no `.gitattributes`; `core.autocrlf` is unset, so
no clean/smudge divergence between blob and checkout for these paths.

## 6. Residual risk / verification gaps

- The working tree is mid-wave: the three `M` files and the untracked `round-16/` additions are
  round-16 work in progress. They do not affect commit-to-commit immutability, but any seat
  reading `measure.py` or `round-16.md` from disk gets bytes that differ from `c699c8c`; use
  `git show c699c8c:<path>` for committed evidence.
- The check is local-object based: replace refs empty, no grafts, repository not shallow, base is
  an ancestor of tip, tip is on `origin/master`. A remote-side rewrite is outside scope.
- Prior spot-check re-execution covers the anchors named in
  `corpus/lessons/round-15-verifier-spotcheck.md` (`:5`, `:89`, `:93`); I did not rerun the lane's
  gate/verifier/selftest (read-only evidence check), and the spot-check itself states its claims
  were evidence-verified, not rerun.
- `reports/round-15/tameshi.md` referenced by the spot-check resolves to the fleet path
  `.ufo/reports/round-15/tameshi.md`, not to the lane's `reports/`; verified byte-identical there.
