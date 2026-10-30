# T58W1ExecAssim — assimilation mirror

Constructed an isolated clone at base `2a32aa8228d5f86a85c81a923a3148bf792a9538`, copied the draft knowledge entry and inserted all three draft rows immediately before `## Paths` (within the SOURCES registry). Fixture commit: `458ad97437d46163238752998dc30a2e9f551a47`.

## Census evidence

- `sources-census.sh validate --root <clone> --file <clone>/corpus/SOURCES.md`: exit 0. Warnings only: W04 duplicate URL across scopes (S047, S048, S075–S078, S081, S092, S104, S160, S265–S268, S274, S288), W01 tier-C mined (S101); file registry row reports `ok`.
- Manual commands per CORPUS.md § SOURCES.md: rows `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md` → 148; malformed-NF awk → 0; tier histogram → A=130 B=14 C=4; status histogram → mined=117 queued=22 rejected=9; duplicate-id awk/sort/uniq → empty; enum/tier-inflation awk → empty; mined used-by existence awk/while → empty.

## Collision evidence

- Registry IDs gathered with the registry-row awk and sorted unique: `S001`–`S037`, `S040`–`S037` is not contiguous; full exact output is recorded in JSON. In particular registry IDs include S153–S160 and S286–S288.
- Staged IDs from `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md | grep -oE 'S[0-9]{3,}' | sort -u`: S153–S255; full list in JSON.
- `comm -12` intersection: S153 S154 S155 S156 S157 S158 S159 S160. Staged source contract's anticipated S156/S165 are not an exact description of observed overlap: S156 collides, S165 is staged but not in registry, and observed collisions extend through S160.
- Guard fixture: initialized an isolated scratch git repo after verifying its top-level; row `   | S156 | fixture |` matched the 0–3-leading-space regex. `comm -12` against staged IDs returned S156.
- Draft row IDs extracted from sources-append.md: S286 S287 S288; none intersects staged IDs.

The first validate attempt using lane name `tameshi` failed because the detached clone has no `shokunin.conf` (`config not found`, unknown lane). The retry with explicit `--file` succeeded. No tool installs. Scratch clone/fixture removed before handoff.

Exact command outputs, including both complete ID lists, are in `T58W1ExecAssim.json`.