# ScoutRegistry — registry ids, status tally, item-10 collision run

Axes: **(a) registry truth** (ids + statuses at a pinned revision), **(b) id-collision
count** (item-10 receipt), **(c) revision pinning** (freeze/base vs live worktree). No
counter was run (prohibited before the L1's deciding run); no campaign tool was run.

## 1. Extractor (item 10)

The item-10 id extractor is the 0–3-leading-space table-row pattern already frozen in the
lane: `corpus/lessons/round-40-verifier-spotcheck.md:191` carries
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` and the frozen counter uses the same rule
(`.ufo/evidence/round-41/calibration/measure.py:43`,
`S_ROW_RE = re.compile(r'^ {0,3}\|[ \t]*S(\d{3,})')`). Exact commands run (scratch
`/tmp/tameshi-r41-scoutregistry/`):

```bash
REV=a3d6c690bcbf8914551d4f4e8e1612784c1c2046
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git show $REV:corpus/SOURCES.md \
  | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]{3,}' | sort -u \
  > /tmp/tameshi-r41-scoutregistry/reg-ids-frozen          # 107 lines
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' \
  /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md \
  | grep -oE 'S[0-9]{3,}' | sort -u > /tmp/tameshi-r41-scoutregistry/staged-ids   # 103 lines
comm -12 /tmp/tameshi-r41-scoutregistry/reg-ids-frozen \
         /tmp/tameshi-r41-scoutregistry/staged-ids \
  > /tmp/tameshi-r41-scoutregistry/collisions-frozen       # 0 lines = 0 collisions
```

The same pair run against the **live working-tree** `corpus/SOURCES.md` (see §3) yields a
collision file of **2 lines**.

## 2. Registry id list — frozen/base `a3d6c690` (also `d4ee4e63`, identical blob)

`corpus/SOURCES.md` at both revisions is sha256
`62b05736d565d681109f9ef95d1ac4deed4d7136fc5b2ee3291160f0644605a7`; **107 rows, 107 unique
ids, no duplicate**.

```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018
S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036
S037 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056
S057 S058 S059 S060 S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074
S075 S076 S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092
S093 S094 S095 S096 S097 S099 S100 S101 S102 S103 S104 S105 S106 S107 S108 S132 S152
```

- **Highest id: `S152`.** Gaps (never allocated): `S038 S039 S098`, `S109`–`S131`,
  `S133`–`S151`.
- **Status tally: `mined=79`, `queued=22`, `rejected=6`** (79+22+6 = 107). No other status
  value occurs. Tally is computed on the status cell (field 8) after splitting on unescaped
  `|` (`re.split(r'(?<!\\)\|', line)`), so escaped pipes in `recheck` do not shift columns.
- **S153 and S154 are unused at these revisions** — confirmed by the id list (ends `S152`)
  and by `grep -c '^S15[34]$'` on `reg-ids-frozen` → `0`/`0`.

## 3. Live-worktree drift (matters for the measured revision)

Two rows were appended by this wave's executors after the freeze commit:

- `corpus/SOURCES.md:123` → `| S153 | ast — Abstract syntax trees (Python 3.15.1 documentation) …`
  (`status=mined`)
- `corpus/SOURCES.md:124` → `| S154 | pathlib — Object-oriented filesystem paths (Python 3.15.1 documentation) …`
  (`status=mined`)

Both rows are now **committed** in `b37ce97` (2026-10-25 03:39, "sources S153/S154, lesson,
amendments A1-A4"), which is the current tip; the frozen/base revisions still carry 107 rows.
`corpus/SOURCES.md` at `b37ce97` has 109 rows, highest `S154`, same 81/22/6 tally, and
`- Next unused id: S155.` at `:440`.

Registry at `b37ce97`: sha256
`186a817098e99bc615e7bf033a5bea7a7dc4756734becc1e29a44ca640ba646c`, **109 rows, 109 unique
ids, highest `S154`**, tally **`mined=81`, `queued=22`, `rejected=6`** (81+22+6 = 109). The
worktree is still moving (a later edit added byte counts and sha256 prefixes to the same two
`recheck` cells only; observed sha256 `ad3b3ab5c626342360beed31d5e77b705d1f62cf9d4df9085db3c41a7450fff5`,
same 109 rows / ids / tally), so pin counts to the commit, not to a worktree hash.
`SCORECARD.md:1851` already restates the standing `sources-registry` cell to **109 rows at
round 41**, which agrees with this file at the worktree (m6 material at the measured
revision is consistent); at the base revision the same cell said 103 against 107 rows, which
is the contract's recorded `m6=1`.

## 4. Staged id list — `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`
(read-only; no campaign tool run)

File sha256 `020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807`; 103 table
rows between the two `<!-- … -->` comments, first row at `:7`.

```
S153 S154 S155 S156 S157 S158 S159 S160 S161 S162 S163 S164 S165 S166 S167 S168 S169 S170
S171 S172 S173 S174 S175 S176 S177 S178 S179 S180 S181 S182 S183 S184 S185 S186 S187 S188
S189 S190 S191 S192 S193 S194 S195 S196 S197 S198 S199 S200 S201 S202 S203 S204 S205 S206
S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218 S219 S220 S221 S222 S223 S224
S225 S226 S227 S228 S229 S230 S231 S232 S233 S234 S235 S236 S237 S238 S239 S240 S241 S242
S243 S244 S245 S246 S247 S248 S249 S250 S251 S252 S253 S254 S255
```

- 103 ids, **contiguous `S153`–`S255`**, no intra-file duplicates (103 rows → 103 unique).

## 5. Collision line count

| registry basis | reg ids | staged ids | `comm -12` lines |
|---|---|---|---|
| frozen/base `a3d6c690` / `d4ee4e63` (before this round's append) | 107 | 103 | **0** |
| landed `b37ce97` and live worktree (append at `corpus/SOURCES.md:123-124`) | 109 | 103 | **2** (`S153`, `S154`) |

So: **the item-10 collision count for round 41 as landed is 2** — the staged package's first
two ids (`S153`, `S154`) now name the lane's own two rows; it was 0 against the frozen
registry. No staged row was adopted, so no renumber map applies; if a later round adopts any
staged row, renumbering must start at `S155` (first free id; `corpus/SOURCES.md:440` carries
`- Next unused id: S155.`), per the campaign's own rule in
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/merge-plan.py:288`
(a collision is a numbering mistake — re-point, keep the work).

Guard non-vacuity (extractor shown able to fail), scratch
`/tmp/tameshi-r41-scoutregistry/guard/`: appending the indented row
`  | S153 | Indented collision proof — https://example.invalid/s153 | …` to a copy of the
frozen registry gives `reg-ids=108 collisions=1 → S153`; the column-zero-only control on the
same file gives `reg-ids=107 collisions=0`. This reproduces the round-38/round-40 guard
result (`corpus/lessons/round-38.md:60-62`, `corpus/lessons/round-40-verifier-spotcheck.md:207-210`).

## 6. Scope and non-actions

- `corpus/SOURCES.md` was read via `git show` at the two pinned revisions **and** the
  worktree was read to detect drift; nothing was edited, staged, or committed.
- `/home/vgpnk/Projects/shokuknow` was read (that one file) only; no campaign tool
  (`merge-plan.py`, `audit-wave.py`, …) was executed.
- Neither C1 nor C2 counter was run at any revision (`--rev`, `--control`, `--selftest` all
  untouched). No tool was installed or upgraded.
- Scratch is outside the checkout: `/tmp/tameshi-r41-scoutregistry/{reg-ids-frozen,
  staged-ids,collisions-frozen,guard/}`.

## 7. Remaining unknowns

- The campaign may rewrite `SOURCES.append.md` after this snapshot; the sha256 above pins
  the copy this finding is about, so a re-run on a changed file invalidates §4–§5.
- Whether the L1 wants the staged S153/S154 rows re-pointed rather than merely recorded:
  current draft records the collision without a renumber map (consistent with "nothing
  adopted"), which is correct only while no staged row is assimilated this round.
