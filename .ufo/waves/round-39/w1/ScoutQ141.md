# ScoutQ141 — staged S141 @ rev 31687496 (read-only hand-check)

**Verdict: NO — rev `31687496` does not contain the six-gate writeFileSync census, and the S141 row it anchors is itself falsified by the pinned bytes.**

## The row

`/home/vgpnk/Projects/shokuknow/lanes/tameshi/round4/SOURCES-PROPOSED.md:22` (staging id S141; shokuknow ID-REMAP:82 maps round4 S137 → staged S141; the on-disk file is already renumbered). The row claims:

- scope: **four** pinned gate blobs `kumitate-shokunin/scripts/{kimi-census,claims-check,round-gate,cite-check}.mjs` read with `git show` @ tameshi rev `31687496`;
- claim: "the surveyed gates contain **no** file-write call sites at all";
- gate block (line ~57): `"kimi-census.mjs writeFile=0 appendFile=0 createWriteStream=0 fs.write=0 unlink=0 rename=0 stdout.write=0"`.

The task's "six-gate" wording belongs to the *corrected* round-5 row `| S145 |` (`round5/SOURCES-PROPOSED.md:21`, 86 sites) — S141 is the four-gate row it corrects.

## What rev 31687496 actually pins

`git show 31687496:tools/mutate-and-run.sh`:

- lines 87-95: **nine** legs, of which **five** kumitate JS gates (kimi-census, claims-check, round-gate, sources-check, cite-check) — not four, not six;
- lines 605-622: `PIN_*`/`REV_*` constants; `proxy-check` and `surface-probe` occur 0 times in the file and have no pins at this rev.

## Re-run against the pinned blobs (read-only)

`git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show <rev>:scripts/<g>.mjs | sha256sum` matches each recorded pin; `grep -c writeFileSync` on the same bytes:

| gate | rev | pin check | writeFileSync lines |
|---|---|---|---|
| kimi-census | 175de6ba | OK (83016d45…) | 15 |
| claims-check | 175de6ba | OK (e9a21b44…) | 5 |
| round-gate | 364f1d59 | OK (f890e277…) | 17 |
| sources-check | 0acb7752 | OK (6a293a72…) | 6 |
| cite-check | 1205c662 | OK (40573448…) | 36 |

The four gates S141 actually names total **73** `writeFileSync` lines; its quoted `writeFile=0` for kimi-census is false at the same pinned blob — `kimi-census.mjs:440` is `writeFileSync(abs, 'fixture\n');` and `:452` is `else writeFileSync(join(root, e.dir, \`${name}.md\`), 'x\n');` (the round-5 file quotes both as counter-evidence). All observed writes target selftest scratch trees, so the F4 conclusion (0 unflagged expected-value writes) survives, but the census data and gate count in the row do not.

## Bottom line

- Six-gate census at rev 31687496: **absent** — no six-gate pin set exists there (five kumitate JS legs; proxy-check/surface-probe unpinned).
- S141 row claim as written: **falsified** — four gates claimed zero write sites; the four pinned blobs contain 73 `writeFileSync` lines and the quoted census line is contradicted by the same blob it cites.

Read-only: no lane files, register, or sibling repo mutated. No tools installed.
