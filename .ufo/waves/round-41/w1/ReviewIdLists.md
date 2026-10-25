# ReviewIdLists — item-10 id lists in the round-41 report and LOG

Seat: `L1Tameshi41.ReviewIdLists` (reviewer, read-only). The lane checkout, `LOG.md` text, the Git
index and the jj state were not touched. The only file this seat wrote is this report. One
unintended artefact (`__pycache__` from a single counter import) was removed; see *Verification
gaps*.

## Verdict — the lists are MISSING everywhere; the report does not exist

Checked 2026-10-25T03:45–03:48-03:00; the m7 figures were re-verified at 03:47 against counter sha
`9aaa99ac…` (HEAD `b37ce97` plus working-tree amendment A5).

| artefact | path | both id lists pasted? | collision count? | renumber map? |
|---|---|---|---|---|
| round-41 **report** (fleet repo) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/tameshi.md` | **file absent** | — | — |
| **LOG** (live, appended during the wave) | `LOG.md:2093`, sentence at `LOG.md:2135-2137` | no — counts only | yes: 2 | yes: "empty" |
| **LOG draft** (seat report) | `.ufo/waves/round-41/w1/ScribeLog.md:19-31` | no — silent on item 10 | no | no |
| **lesson** (scanned record, not the report) | `corpus/lessons/round-41.md:40-46` | no — counts only | yes: 2 | yes: "no renumber map is applied" |
| item-10 scratch evidence | `.ufo/waves/round-41/assimilation/{reg-ids,staged-ids,collisions}` | present (109 / 103 / 2 lines) but **untracked** | — | — |

Requirement: `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-41.md:427-428` — "Paste both
id lists, the collision count and the renumber map into the report." This is round-40 routed defect 3
(`corpus/lessons/round-40-verifier-spotcheck.md:308-312`): round 40 committed `reg-ids` (105 ids) and
`staged-ids` (2 ids) as wave evidence and cited the collision count and empty map, but never pasted
the 105-id list into the report text. Round 41 repeats that exactly: the LOG (`LOG.md:2135-2137`) and
the lesson (`corpus/lessons/round-41.md:40-46`) both cite "registry ids 109, staged ids 103 beginning
at `S153`", "`collisions` holds `S153` and `S154`" and "the renumber map is empty" — and neither
pastes either list. The fleet report, the one artefact item 10 names, is absent.

Evidence that the files behind those counts are real and match:
`wc -l .ufo/waves/round-41/assimilation/{reg-ids,staged-ids,collisions}` → `109 / 103 / 2`;
`od -c .../collisions` → `S153\nS154\n`; `tail -1 .../reg-ids` → `S154`;
`head -1 .../staged-ids` → `S153`, `tail -1` → `S255`.

## Constraint the report text must respect: the lists cannot go into the LOG or the lesson

The C1 counter reads exactly three records: `measure.py:142-147` (`round41_records`) =
`corpus/lessons/round-41.md`, the `## Round 41` section of `SCORECARD.md`, and the
`## 2026-10-25 — round 41` section of `LOG.md`. It does **not** read the fleet report.

- m7 (`measure.py:227-235`) fails on every `S\d{3,}` cited in those records whose registry status is
  not `mined`. The landed registry has 28 non-mined ids — `S007 S009 S010 S013 S014 S015 S016 S017
  S018 S019 S020 S021 S022 S023 S025 S027 S029 S030 S040 S042 S043 S044 S045 S046 S067 S071 S080
  S092` (22 queued + 6 rejected).
- Run through the counter's own `S_CITE_RE`: appending the full 109-id registry list to the lesson
  yields **28 m7 mismatches** (`C1_R41_PASS=false`). The 103-id staged list adds 101 ids absent from
  the registry, which m7 classes as "cited but absent". So pasting either list into `LOG.md` or the
  lesson breaks C1 — on the frozen counter (m7 read `cells[9]`, the `opened` date) it breaks C1 on
  *any* cited S-id.
- Therefore the paste belongs in the report only. The report is outside both counters; the current
  LOG cites only `S153` and `S154` (both `mined`), which is m7-clean and should stay that way.

Second constraint for the lesson/LOG, not the report: `measure.py:51-56` (`PATH_PREFIXES`) resolves
backticked paths under `.ufo/waves/round-41/` and `.ufo/evidence/round-41/` at the measured revision
(m8). Any citation of `.ufo/waves/round-41/assimilation/reg-ids` therefore requires the three files
to be committed with the round-41 commit — they are currently untracked (`git status --porcelain
.ufo/waves/round-41/` → `?? .ufo/waves/round-41/`). Neither the LOG nor the lesson backticks those
paths today, so m8 is not yet exposed.

## Measured values (read-only; item 10's own extractor)

```
A=/tmp/tameshi-r41-reviewidl-freeze
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

- Landed registry (working tree, i.e. the state the evidence files record): **109 ids**, `S001`–`S154`;
  gaps at `S038`, `S039`, `S098`, `S109`–`S131` and `S133`–`S151` are the retired/unallocated range.
  Status tally 81 `mined` / 22 `queued` / 6 `rejected`.
- Freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`: **107 ids** (the same list without `S153`,
  `S154`; tally 79 / 22 / 6 — the contract's before-state).
- Staged set: **103 ids**, `S153`–`S255`, consecutive, from
  `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`.
- Collision count: **2** (`S153`, `S154`) against the landed registry; **0** against the freeze
  registry. The applied renumber map is **empty** — no staged row was adopted this round.
- Next-round map (if any staged row is adopted): document-anchored, never arithmetic. The two
  colliding staged rows take the next free ids above `S154` (`S155`, `S156`); a whole-set adoption
  lands on the block `S155`–`S257` because each adopted row takes the next free id in document order.

## Exact text to add

### 1. Round-41 report — `/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/tameshi.md`, in `## Sources & frontier`, immediately after the census bullet (before the Assimilation/quarantine bullets)

Paste this block verbatim; the two lists are the files' own contents and are not scanned by either
counter here:

```markdown
**Item 10 id-collision check** (discharges round-40 routed defect 3: both lists pasted, not only the
counts). Extractor and `comm -12` as item 10 prescribes; `reg-ids`, `staged-ids` and `collisions` are
committed as wave evidence at `.ufo/waves/round-41/assimilation/`.

- Registry ids — **109**, `reg-ids` (`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort`): S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S099 S100 S101 S102 S103 S104 S105 S106 S107 S108 S132 S152 S153 S154
- Staged ids — **103**, `staged-ids` (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`): S153 S154 S155 S156 S157 S158 S159 S160 S161 S162 S163 S164 S165 S166 S167 S168 S169 S170 S171 S172 S173 S174 S175 S176 S177 S178 S179 S180 S181 S182 S183 S184 S185 S186 S187 S188 S189 S190 S191 S192 S193 S194 S195 S196 S197 S198 S199 S200 S201 S202 S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218 S219 S220 S221 S222 S223 S224 S225 S226 S227 S228 S229 S230 S231 S232 S233 S234 S235 S236 S237 S238 S239 S240 S241 S242 S243 S244 S245 S246 S247 S248 S249 S250 S251 S252 S253 S254 S255
- Collision count: **2** — `comm -12 reg-ids staged-ids` → `S153`, `S154`, the staged package's first
  two ids, which now name this round's own `ast` and `pathlib` rows. The same extractor over the
  freeze registry `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937` (107 ids) returns 0 collisions.
- Renumber map: **empty** — no staged row was adopted, so no id moved and none is renumbered in this
  round's registry. Any next adoption renumbers in scratch by document, not arithmetic: the two
  colliding staged rows take the next free ids above `S154` (`S155`, `S156`); a whole-set adoption
  lands on `S155`–`S257`.
```

### 2. LOG and lesson — no lists; one optional pointer sentence

`LOG.md:2135-2137` and `corpus/lessons/round-41.md:40-46` already carry the collision count and the
empty map. Do **not** add either list there (28 m7 mismatches). If the LOG should point at the paste,
this sentence is m7/m8-safe (it cites no S-id and no `.ufo/...` path):

```
Id lists for the item-10 check are pasted in the round report's Sources & frontier section.
```

### 3. Precondition before the deciding run

Commit `.ufo/waves/round-41/assimilation/reg-ids`, `staged-ids`, `collisions` (and
`.ufo/evidence/round-41/sources/`) with the round-41 commit; they are untracked now and any later
backticked citation of them in the lesson/LOG is an m8 failure until they are. The report block above
names them, and the report itself is not m8-scanned, so this is a lesson/LOG precondition only.

### 4. Acceptance check once the report lands

The fix is mechanical to verify — the pasted tokens must equal the evidence files exactly:

```
python3 - <<'PY'
import re
t = open('/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/tameshi.md').read()
ev = '.ufo/waves/round-41/assimilation/'
for name in ('reg-ids', 'staged-ids'):
    want = open(ev + name).read().split()
    line = [l for l in t.splitlines() if '`%s`' % name in l]
    got = re.findall(r'\bS\d{3}\b', ' '.join(line))
    print(name, len(got), got == want)
print('collisions', open(ev + 'collisions').read().split())
PY
```

Expected: `reg-ids 109 True`, `staged-ids 103 True`, `collisions ['S153', 'S154']`.

## Coupled risk (not this seat's class; flagged once with evidence)

The freeze artefacts moved after the freeze, and the counter is still moving:

- Freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`: `calibration/measure.py` sha256
  `f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2`, which is exactly what the
  frozen `contract.json` pinned. That version read `status = cells[9]` in `registry()` — the `opened`
  date — so *any* cited S-id failed m7.
- Commit `b37ce97` (landed during this seat's run) carries amendments A1–A4 with C1 pin
  `8bc9b4221c59c7b380892b7f97885e9b8ada1f5d82b0703effa166f0519ce11c`: `cells[8]` for m7, `exists` in
  `resolves`, `rstrip('/')`, m9 gate change.
- Working tree at 03:47: a further amendment **A5** (uncommitted) changes m9's correction gate to
  derive the expected words from the round-40 table counts; C1 pin now
  `9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd`, which equals the live file.
  `contract.json` remains `M` in `git status`, so the freeze is being amended while the wave runs and
  after seats had read it.
- This matters for the id-list text only through m7: on the frozen counter every cited S-id fails; on
  the current counter only the 28 non-mined ids fail. Both give the same prescription (paste in the
  report, never in the scanned records), and the m7 figures above were re-verified under
  `9aaa99ac…`: the three records cite only `S001`/`S153`/`S154` (all `mined`), and the full registry
  list still yields 28 mismatches. `ScribeLog.md:49-56` cites the frozen sha and the `cells[9]`
  behaviour, so it was written against the pre-amendment file. Freeze integrity
  is `ReviewC1Counter`'s finding, not this seat's; it is recorded here because the text I prescribe
  depends on which counter runs.

## Verification gaps

- No default-mode counter run at the tip or at any measurement revision (forbidden by the seat
  brief). Every value here comes from the item-10 extractor and from `wc`/`od` over the freeze rev and
  the working tree.
- I imported the live C1 counter once at 03:43; that import created
  `.ufo/evidence/round-41/calibration/__pycache__/measure.cpython-314.pyc`, which I removed at
  03:44:59. Later imports used `PYTHONDONTWRITEBYTECODE=1`. A `__pycache__` reappeared at 03:45:56;
  its mtime is not this seat's run (another seat imported the counter), and I left it alone. No other
  lane file was written by this seat.
- The LOG section was appended by the L1 during this seat's run (`LOG.md:2093` appeared between 03:40
  and 03:45); this report checks the current text at 03:46. If the L1 rewrites that section, re-check
  m7 (`python3 -c` with the counter's own `S_CITE_RE` over the section is the cheap test).
- Tooling: no install or upgrade; `python3`, `git`, `comm`, `wc`, `od`, `sha256sum` were sufficient.
  No pacman transaction attempted (host-wide pause respected).

Report: .ufo/waves/round-41/w1/ReviewIdLists.md
