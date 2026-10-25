# ScribeReject — w1, milestone "Reject text"

Seat: scribe (leaf, no delegation). Axes: depth. Date: 2026-10-24.
Deliverable: drafted reason + flip condition for refusing gate `r4-gate-write-path-audit`
(staged source S137) on the ground that revision `31687496` has no write-path census payload.
Lane writes: this report only. No pacman installs (none needed; pacman paused per bounds).

## Draft reject text (paste-ready; matches the lane's existing two-field convention)

Reason: quarantined `payload-absent`. The cited revision `31687496`
(full `31687496b5f34b153626e123d12ae2febdbd86a0`, 2026-10-23 18:57:14 -0300, subject
"round-35: final before + v2 control receipts on the 9-copy panel (before exit 1; control
0/6 kill 0/3 accept exit 1) + tool selftest 33/33 under the final pins") is a round-35
tally-receipt commit, not a census commit. Its only changed paths are
`.ufo/evidence/round-35/control/c1-v2-control.stdout` (M) and
`.ufo/evidence/round-35/lessons/selftest-33.out` (A) — mutation kill/accept tally tables
and a `C1_R35_CONTROL: … C1_R35_CONTROL_PASS=false` receipt. Its tree carries no write-path
census payload: `tools/write-path-census.py` is absent, no `*write-path*` path exists
anywhere in the tree, `.ufo/evidence/` stops at `round-35` (no round-39), and the four
pinned fleet gate blobs the row claims to have measured
(`kumitate-shokunin/scripts/{kimi-census,claims-check,round-gate,cite-check}.mjs`) are not
lane bytes — no `scripts/*.mjs` blob exists in that tree, only lane-side receipts about
those gates (round-16/17/21/25/26 evidence). The row's zero-write-site census is therefore
unverifiable from the cited revision: nothing in that tree can reproduce it.

Flip: a hand-check that locates a write-path census artifact in `31687496`'s tree whose
counts reproduce. Concrete, contract-anchored test:
`python3 .ufo/evidence/round-39/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 31687496b5f34b153626e123d12ae2febdbd86a0`
reporting `tool_sha_ok=1` and `gates=21/21` — i.e. the pinned census tool and all 21 frozen
gate blobs it classifies actually exist at the cited revision (contract.json:24,30:
classification must come "from REV bytes" and the tool pin is the sha256). Minimally: any
census blob at that revision re-run from that revision's bytes with matching counts.

## Evidence (all commands read-only, run 2026-10-24)

1. Revision resolves: `git -C <lane> rev-parse '31687496^{commit}'` →
   `31687496b5f34b153626e123d12ae2febdbd86a0`; `git show -s --format='%H%n%ci%n%s'` →
   2026-10-23 18:57:14 -0300, round-35 receipts subject (quoted above).
2. Commit touches only tally receipts: `git show --no-color --name-status 31687496` →
   `M .ufo/evidence/round-35/control/c1-v2-control.stdout`,
   `A .ufo/evidence/round-35/lessons/selftest-33.out`.
3. Tool absent at cited rev: `git cat-file -e 31687496:tools/write-path-census.py` →
   exit 128, "fatal: path 'tools/write-path-census.py' exists on disk, but not in
   '31687496'". (Present in the current working tree at `tools/write-path-census.py`,
   5444 B — so the reject is about the cited revision, not the lane.)
4. No write-path path anywhere in that tree:
   `git ls-tree -r --name-only 31687496 | grep -i 'write-path'` → no output, exit 1.
5. No round-39 evidence at that rev:
   `git ls-tree --name-only 31687496:.ufo/evidence | tail` → ends at `round-35`.
6. Tally-receipt content confirmed: `git show 31687496:.ufo/evidence/round-35/control/c1-v2-control.stdout`
   → COPY kill/accept rows + `C1_R35_CONTROL: … PASS=false rev=691bb512…`;
   `git show 31687496:.ufo/evidence/round-35/lessons/selftest-33.out` → `CASE … PASS` selftest lines.
7. Fleet gate blobs are not lane bytes:
   `git ls-tree -r --name-only 31687496 | grep -E 'kimi-census|claims-check|round-gate|cite-check|kumitate'`
   → only `.ufo/…` receipts and `corpus/knowledge/…` notes; no `scripts/*.mjs` source blob.

## Corroboration (read-only fleet checkout, not modified)

- Staged row: `/home/vgpnk/Projects/shokuknow/lanes/tameshi/round4/KNOWLEDGE-PROPOSED.md:160-163`
  — staged entry `corpus/knowledge/r4-gate-write-path-audit.md`, source S141, citing "the
  four pinned gate blobs `kumitate-shokunin/scripts/{kimi-census,claims-check,round-gate,cite-check}.mjs`
  at their registry pins … @ revision 31687496 — measured 2026-10-23".
- `/home/vgpnk/Projects/shokuknow/lanes/tameshi/round4/SOURCES-PROPOSED.md:22` — the row's
  claim: "the surveyed gates contain **no** file-write call sites at all … run 2026-10-23
  at revision 31687496" — but the tree at that revision holds no census payload (items 3-7).
- The source owner's own later correction already disputes the count on the merits:
  `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r5-gate-write-site-census-corrected.md:11-15`
  — "That count was wrong. The same command on the same blobs returns 15 for `kimi-census`".

## Precedent / conventions reused

- `corpus/lessons/round-39.md:21-24` (L1-authored, untracked working-tree file;
  `git log -1 -- corpus/lessons/round-39.md` prints nothing) already records this same
  reject with class `payload-absent`. This draft keeps that class label and Reason/Flip
  shape; the lesson file was NOT edited by this seat.
- Contract anchor: `.ufo/evidence/round-39/contract.json:24` (C2 predicate, "classified
  from REV bytes"), `:26` (before-state `tool_absent=1 gates=0/21` at base rev),
  `:30` (tool sha256 pin). The frozen contract was read, not edited. Base rev
  `50aadd1bbd94e43cd3fcfb81459414394db2dc35` was not touched; no C1/C2 counter was run
  at the cited revision (the flip is a draft condition for a future hand-check; the
  contract's kill_rule reserves deciding runs for after the wave settles).

## Gates observed

- Read-only git plumbing only (`rev-parse`, `cat-file -e`, `ls-tree`, `show`, `log`);
  no jj commands, no index/index-lock writes, no `.ufo/state` or domain-tree writes.
- Only lane write: this report at `.ufo/waves/round-39/w1/ScribeReject.md` (sanctioned Report path).
- Scratch: `/tmp/tameshi-r39-ScribeReject/`.

## Out of scope / limits

- Sibling seat ScoutQ141 handles S141 (`r5-gate-write-site-census-corrected.md`), which
  cites the same revision for a 6-gate `writeFileSync` census; same `payload-absent`
  class, not re-judged here.
- The staged S137 document body was not re-read beyond the fleet staged package above;
  the reject is grounded in the cited revision's bytes, which is this seat's target.
- The flip condition was not executed (it would fail today by items 3-5; running it is
  the deciding-run's business, not a scribe seat's).
