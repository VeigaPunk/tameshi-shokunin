# ScoutQ137 — Quarantine S137 (axis: depth)

## Verdict

Revision `31687496` (= `31687496b5f34b153626e123d12ae2febdbd86a0`) contains **only a
round-35 tally receipt**. No write-path census payload is present in the commit diff or
anywhere in its tree. Staged S137's citation is falsified.

## The claim being checked

`shokuknow/lanes/tameshi/round4/SOURCES-PROPOSED.md:22` (row S137): "tameshi's audited
write-path census of the fleet gate selftests … the four pinned gate blobs
`kumitate-shokunin/scripts/{kimi-census,claims-check,round-gate,cite-check}.mjs` at their
registry pins, read with `git show`, @ revision 31687496", with quoted census line
"kimi-census.mjs writeFile=0 appendFile=0 createWriteStream=0 fs.write=0 unlink=0
rename=0 stdout.write=0" (`:60` quote under "Gate — S137").

## Observed facts (lane repo, read-only)

1. `git show --stat 31687496` — subject: "round-35: final before + v2 control receipts
   on the 9-copy panel (before exit 1; control 0/6 kill 0/3 accept exit 1) + tool
   selftest 33/33 under the final pins". Exactly two files touched:
   - `.ufo/evidence/round-35/control/c1-v2-control.stdout` — adds one
     `COPY kill root-keyed-shape6` row and updates the final
     `C1_R35_CONTROL … pub_kill=0/6 … pub_slots=9 … C1_R35_CONTROL_PASS=false` line.
   - `.ufo/evidence/round-35/lessons/selftest-33.out` — new file, 33 `CASE` lines plus
     `TALLY_AUDIT_V3_SELFTEST: 33/33 pass`.
2. `git ls-tree 31687496 --name-only scripts/` → **empty**; the tree has no `scripts/`
   directory and no `*.mjs` gate blobs at all
   (`git ls-tree -r 31687496 | grep 'kumitate\|kimi-census\|claims-check\|round-gate\|cite-check'`
   matches only `.ufo/evidence/*` receipts and `corpus/knowledge/*` notes — zero scripts).
3. `git ls-tree -r 31687496 --name-only | grep -i 'write-path\|writepath'` → 0 hits;
   `tools/` at that rev lists no census tool (tally tools only:
   `tools/tally-audit*.py`, `mutate-and-run.sh`, etc.).
4. `git grep -l 'kimi-census.mjs writeFile' 31687496` → no match; the quoted census
   line is not stored anywhere in that tree. The only "write-path"-adjacent hit
   (`git grep -c 'WRITE_PATH\|write-path\|writeFile=0 appendFile=0' 31687496`) is
   `.ufo/waves/round-16/w1/Misroot.md` — unrelated prose about a misrooted `write`
   path, not a census.

## Assessment

S137 claims the revision hosts (a) the four pinned gate `.mjs` blobs and (b) the
measured write-path census output. Both are absent: the commit is a round-35
control/selftest receipt pair, and the cited blobs live in the sibling
`kumitate-shokunin` repository, not in this lane's tree at any path. The row's
"read with `git show` @ revision 31687496" is not reproducible — the objects it names
do not exist in that revision.

Confidence: high (tree-level listing + content grep over the exact revision).
Remaining unknowns: none for the asked question.
