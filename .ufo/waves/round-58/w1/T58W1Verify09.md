# T58W1Verify09 — row verification

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Item routed-at revision: `650987a0d6fc285b37f0f9e63a3aae864af9cd5a`.

Commands used in the detached base clone:
- `git clone --shared ...` then `git -C "$S/clone" checkout --detach 2a32aa8228d5f86a85c81a923a3148bf792a9538`; `git -C ... rev-parse --show-toplevel` returned `/fast/scratch/hyaku/tameshi-r58/T58W1Verify09/clone`.
- `git show <base>:corpus/lessons/round-54-verifier-spotcheck.md | nl -ba` inspected the routed items and later re-check section.
- `git show <base>:.ufo/waves/round-54/w2/T54W2Sent01.md | nl -ba` checked report wording for R54.7.
- `git grep -n -E ... <base> -- corpus/lessons/round-54-verifier-spotcheck.md` located each item and the R54.6 resolution assertion.
- `git log --all --format='%H %s' -- <R54.6 paths>` returned `ff2a821a1e83acd92bb4d62bad15f380973a55ea round-54: commit the lane's wave-2 sentinel report T54W2Sent03 and its two cited receipts ...`.
- `git show --format= --name-status ff2a821a1e83acd92bb4d62bad15f380973a55ea` listed additions of `T54W2Sent03.md`, `c1committed-positive.stdout`, and `rejection-attribution.txt`.
- `git cat-file -e 650987a0...:<path>` confirmed the report and receipts already existed at routed_at; the forged-reader original path was absent there.

## Findings

- **R54.6 — fixed at base.** The deciding record's `after/clean-tree-after.txt` at base lists the three named files as untracked (`??`). Commit `ff2a821a1e83acd92bb4d62bad15f380973a55ea` subsequently added the report plus both cited receipts. The lesson's base line 155 explicitly reports `git status --porcelain` empty and identifies R54.6 as resolved by `ff2a821`. Proposed resolving commit: that full hash.
- **R54.7 — open.** Base lesson line 120 says the forged artifact was renamed into the receipts directory, but says the report claims deletion and must be corrected. Base `T54W2Sent01.md` lines 185–189 indeed says deletion and that it must be recorded in the next commit. Proposed round-58 correction: accurately describe the R100 rename.
- **R54.8 — open.** Base lesson line 122 identifies both outstanding corrections. The report's authority claim remains in `T54W1ExecStraceNoise.md:324`; `corpus/lessons/round-54.md` lacks the stated incident correction. Proposed round-58 correction: mark the claim superseded and add the incident to the lesson.
- **R54.9 — open.** Base lesson line 124 contrasts the report's values with its evidence: 4 vs 5 reviewers, 26.3% vs 27.6%, and 84 vs 81 staged Markdown files. Proposed round-58 correction: correct those report figures.

The JSON contains one row for each assigned id. No tools were installed. Scratch clone removed before handoff.
