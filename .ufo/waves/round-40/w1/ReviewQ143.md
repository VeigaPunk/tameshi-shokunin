# ReviewQ143 — Hand-check quarantined S143 (axis: depth)

## Verdict

**REFUSE.** The quoted payload cannot be presented. The cited source was fetched and is
live, but the quote occurs in none of it. The register row's class
`payload-absent` is **confirmed** by independent fetch — refusal class: cannot
adopt; the citation's claimed artifact path does not exist at the pinned revision.

## Row under check

`tameshi | round5 | S143 | payload-absent` — absent-defect-register.md:228
(shokuknow, read-only). Quote:
`mavis-trash: failed to trash '/tmp/tmp.jMukhJoKoe/host'`.
Cited source (SOURCES.append.md:41, merge/tameshi): expectation table at
`tools/mutate-and-run.sh:86-96` plus the failing leg's
`bash-surface-census/evidence/control.out` (three cases, then the cleanup line),
@ revision `31687496`, instrument sha256 `a7d3f2dd7d47511a…`, repository
`https://github.com/VeigaPunk/tameshi-shokunin`.

## What checks out (citation anchors are genuine)

- Cited GitHub repo is live; cloned to `/tmp/tameshi-r40-ReviewQ143/cited-source`
  (`git clone … && echo clone-exit: 0`). Its HEAD is `5641ed8` — the same
  round-40 freeze commit as the lane — and pinned rev `31687496` is present in
  the clone (`git cat-file -t 31687496` → `commit`).
- Instrument pin is real:
  `git show 31687496:tools/mutate-and-run.sh | sha256sum` →
  `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — matches
  the citation prefix `a7d3f2dd7d47511a…`.
- The expectation table at `tools/mutate-and-run.sh:86-96` @ `31687496` exists
  and reads as described (nine legs with pinned kill-rate expectations).

## What falsifies the payload (exact commands and results)

1. Cited source (GitHub clone, full object store):
   `git cat-file --batch-all-objects --unordered --batch | grep -c 'mavis-trash'` → **0**;
   `grep -rni 'mavis' .` → 0 hits; `grep -rn 'jMukhJoKoe'` → 0 hits;
   `grep -rni 'failed to trash'` → 0 hits.
2. Lane repo, full object store (all blobs, reachable or not):
   `git cat-file --batch-all-objects --unordered --batch | grep -c 'mavis-trash'` → **0**;
   same for `tmp.jMukhJoKoe` → **0**; `git log --all -S 'mavis-trash'` → no commits;
   worktree `grep -rn 'mavis-trash'` → 0 hits.
3. The citation's claimed artifact path does not exist at the pin:
   `git ls-tree -r 31687496 --name-only | grep -i 'bash-surface-census'` → only
   `.spec`/`.mte.json`/waves files, **no** `bash-surface-census/evidence/control.out`;
   `git ls-tree --name-only 31687496:.ufo/evidence/round-35/` → `after before c1 c2
   contract.json control lessons pin-reconciliation.json src`; `control/` holds only
   `c1-v2-control.stdout`, whose content (`git show 31687496:…/c1-v2-control.stdout`)
   is a COPY-kill verdict table + `C1_R35_CONTROL…PASS=false` line — no trash line,
   no "three cases, then cleanup line" shape. `grep -in 'trash\|mavis'` on it → 0 hits.

## Mechanism (why the quote is plausible yet unverifiable)

`mavis-trash` is a real host tool: `/home/vgpnk/.minimax/bin/mavis-trash`, whose
emission format `mavis-trash: failed to trash '$file'` is genuine (script lines 393
and 428). So the quoted line's *wording* is real tool output, most plausibly
transcribed from a kept workdir's control log (cf. S147's "kept workdir" citations,
which report `mavis-trash` tails: 5/1/1 `ok-case` lines) — but that log was never
committed: the string exists in zero git objects on either side of the citation, and
the path the citation names for it is absent at the pin. A runtime-random mktemp
path (`/tmp/tmp.jMukhJoKoe/host`) can only be evidenced by a captured artifact;
none exists.

## Bounds observed

No edits to the lane checkout, shokuknow, the register, or `.ufo/state`; no C1/C2
counter runs; scratch clone only under `/tmp/tameshi-r40-ReviewQ143/`. All git
invocations read-only (`log -S`, `grep <rev>`, `show`, `ls-tree`,
`cat-file --batch-all-objects`, `status`). Pre-existing worktree state
(`M corpus/QUALITY.md`, untracked round-40 wave files) untouched.

## Residual risk

- GitHub code search API was not used (auth-required); the clone + full
  object-store scan is the stronger check and subsumes it.
- A kept workdir outside any git object store could once have held the line; it is
  not reachable now, so the payload stays unpresentable regardless of origin.
