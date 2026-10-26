# T50Disp41 — C1 disposer, spot-check round 41 (items R41.1–R41.7)

Seat: T50Disp41 (scribe/disposer). Judged on calibration. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Tree judged at the frozen base `e3729de862f73ae080d98fcf522a7081ce16e40a`; the counter's REV in my scratch
self-check is that base plus the round-50 control commit (the frozen defect set `.ufo/evidence/round-50/c1/defects.json`
is absent at `e3729de` — the counter refuses REV without it, so the lowest workable REV is `4afb060` + my rows).

Rows delivered: `T50Disp41.rows.json` ({"round": 41, "rows": [...]}), 7 rows — 6 `fixed`, 1 `declined`.
Commands used for every "found at" claim are shown inline; all line numbers are at `e3729de`.

---

## R41.1 — m8 extractor pairing defect (BACKTICK_RE spans newlines) → **fixed**

Ask: the m8 path extractor's backtick pattern `` `([^`]+)` `` matched across newlines, so a cited path inside a
mispaired span was skipped (`corpus/SOURCES.md` was skipped in round 41); fix with `[^\n]+` or line-scoped
extraction. Found: the round-42 successor C1 counter carries the line-scoped pattern —
`git -C <lane> show e3729de:.ufo/evidence/round-42/calibration/measure.py | nl -ba | sed -n '77,81p'` →
`.ufo/evidence/round-42/calibration/measure.py:79` `BACKTICK_RE = re.compile(r'`([^`\n]+)`')`, and its docstring
declares the rule at `:14-16` ("a backtick span never crosses a newline"). The difference is shown able to fail, not
asserted: `.ufo/evidence/round-42/before/c1-selftest.stdout:1-2` `SELFTEST T1_old_extractor_misses OK` /
`SELFTEST T1_new_extractor_sees OK`. Commit: `322b5cd32b4319a05340d249ae752d12a9e6b19f` ("round-42: freeze contract
and counters (C1 calibration, C2 depth) before any seat"), located with
`git log --diff-filter=A -- .ufo/evidence/round-42/calibration/measure.py`. The round-41 counter keeps the old
pattern (`.ufo/evidence/round-41/calibration/measure.py:45`) by design — it is a closed-round, frozen instrument.
Status `fixed`.

## R41.2 — stale `residual/receipt.json` (`ResidualReceipts → present:false`) → **fixed**

Ask: the round-41 residual receipt asserts `present:false` for a report that exists; regenerate or supersede
receipts after the last write they describe. Found: the lane took the supersede route, which is the append-only
repair it later codified. The superseding receipt exists at
`.ufo/waves/round-42/supersede/round-41-residual-receipt.json` (commit `5f739acf21e878e22bd3f66249ae8bec2aaf1fc1`,
`git log --diff-filter=A -- .ufo/waves/round-42/supersede/round-41-residual-receipt.json`): it names
`"supersedes": ".ufo/waves/round-41/residual/receipt.json"` and re-asserts all eight round-41 seats `present:true`.
I checked the re-assertions against the tree: `git cat-file -e e3729de:.ufo/waves/round-41/residual/<seat>.md` exits 0
for all eight (ResidualReplayC1, ResidualReplayC2, ResidualReceipts, ResidualScope, ResidualIds, ResidualCounts,
ResidualAppendOnly, ResidualClaims). The rule itself is `corpus/QUALITY.md:1001-1011` (criterion 81, added in
`5f739acf`), whose live instance is named at `:1010-1011`. Ledger evidence cites `corpus/QUALITY.md` because the
counter's soft-path rule (`.ufo/waves/` allowed only when the path ends with one of the item's keys) refuses the
supersede file itself — recorded here so the omission is not read as absence. Status `fixed`.

## R41.3 — C1 counter lacks self-pin / records gate / out-of-process / `resolved` / exit-plus-FAIL → **fixed**

Ask: a successor pair routed to round 42 must add a self-pin clause, a `records >= 1` gate, out-of-process tool
execution, `resolved` inspection, and an exit-plus-FAIL kill oracle. Found, all five, in the two frozen round-42
counters (both added by `322b5cd32b4319a05340d249ae752d12a9e6b19f`):

| ask | where | code check |
|---|---|---|
| self-pin | `.ufo/evidence/round-42/calibration/measure.py:7-11` | sha256 of the running file vs the pin read at FREEZE, `:375-384` |
| `records >= 1` | same file `:12-13` | `EXPECTED_RECORDS = 6` at `:75`, gate at `:387-389` |
| out-of-process | `.ufo/evidence/round-42/census/measure.py:7-9` | `[sys.executable, '-I', tool, ...]` at `:231`, `:415` |
| `resolved` inspection | same file `:14-15` | needle in `site['resolved']` at `:257`, `:278-279` |
| exit-plus-FAIL oracle | same file `:16-21` | `FAIL` lines at `:421`; exit checked at `:239` |

The two other complaints in the item text are also gone from the successor: m8 scope widened from four prefixes to
six (`measure.py:81` `PATH_PREFIXES`) and the whole-lesson m9 class does not exist in the round-42 counter at all
(`grep -c 'm9' .ufo/evidence/round-42/calibration/measure.py` → 0). Compound item, every ask met. Status `fixed`.

## R41.4 — v3 `unflagged` false positives on three live sites → **fixed**

Ask: `tools/context-capture.py:1682`/`:1685` and `tools/registry-replay.py:123` were v3 `unflagged` false
positives. Found: v4 resolves all three, and this is observed, not taken from prose. I copied the base bytes of the
three files and `tools/write-path-census-v4.py` into scratch and ran
`TMPDIR=$S python3 -I v4.py --file context-capture.py --json` at base bytes:
`{'lineno': 1682, 'kind': 'open', 'expected': True, 'scratch': True, 'explicit_out': False, 'flagged': False,
'unflagged': False}` and the same for `1685`; `registry-replay.py` gives
`{'lineno': 123, 'kind': 'write_bytes', 'expected': True, 'scratch': False, 'explicit_out': True, 'flagged': False,
'unflagged': False}` with `resolved: 'expected.json argparse --out'`. The counter that has to see them names the
three sites at `.ufo/evidence/round-42/census/measure.py:29-33`; the lane's disposition is
`corpus/lessons/round-42.md:252-253` ("resolved by v4, not by editing v3: v3's bytes stay pinned"). v4 landed in
`5f739acf21e878e22bd3f66249ae8bec2aaf1fc1`. Status `fixed`.

## R41.5 — v3 docstring's blanket "NOT resolved" overstates scope → **fixed**

Ask: correct the blanket claim in the sha-pinned v3 docstring; the item itself says the correction waits for the
successor round because v3 is pinned. Found: the successor v4 docstring restates the bound instead of overstating it —
`tools/write-path-census-v4.py:37-40`: "Aliases, closures over reassigned names and attribute reassignment are not
reliably resolved: a name can bind by definition order or keep a stale binding, so a reader must not treat an
unresolved destination as proven safe", followed by an explicit out-of-scope list (`:40-43`). The lane records the
correction at `corpus/lessons/round-42.md:246-248` ("which corrects v3's blanket \"NOT resolved\" (round-41 routed
defect 5)") and the knowledge entry now lists shapes that provably mis-resolve. v3's bytes stay at the pinned
`095924a7…`. Commit `5f739acf21e878e22bd3f66249ae8bec2aaf1fc1`. Status `fixed`.

## R41.6 — staged ids S153/S154 collide with lane rows → **fixed**

Ask: the next assimilation round must renumber by document in scratch before appending. Found: round 42 did exactly
that — `corpus/SOURCES.md:469-471` (`git show e3729de:corpus/SOURCES.md | nl -ba | sed -n '468,472p'`): the collision
check runs in `.ufo/waves/round-42/assimilation/`, `comm -12` yields "2 collisions, `S153` and `S154`", the 0–3-space
guard is proven on an indented fixture, and the "Renumber map, by document" maps `staged:S159` → S155 and
`staged:S160` → S156 with "No other staged row is appended". Commit
`5f739acf21e878e22bd3f66249ae8bec2aaf1fc1`, located with `git log -S'Renumber map, by document' c77c2b7..e3729de --
corpus/SOURCES.md`. Status `fixed`.

## R41.7 — cosmetic bullet-list split in the round-41 SOURCES note block → **declined**

Ask (self-described cosmetic, no parse impact): reflow the round-41 note block at `corpus/SOURCES.md:436-437` so a
blank line stops splitting its bullet list. Found: not done, and the lane decided not to do it —
`corpus/lessons/round-42.md:254-255`: "Round-41 routed defect 7 (cosmetic list split in `corpus/SOURCES.md`) is left
as is: re-flowing a closed note is an in-place edit for no parse gain." The tree agrees: at `e3729de` the block is
byte-identical to the routed revision apart from later appended blocks (`git show c77c2b7:corpus/SOURCES.md | nl -ba |
sed -n '434,440p'` vs `git show e3729de:...`). The decline is the lane's own recorded decision and is consistent with
the append-only rule for landed registry notes; reflowing rewrites closed-round bytes for a rendering-only gain.
Status `declined`, reason in the row (≥40 chars).

**Counter interaction (finding, not a verdict).** R41.7 is the one row where the frozen key set is unsatisfiable by
honest evidence: its keys are `SOURCES.md:436`, `436-437`, `bullet list`, and outside the spot-check file (excluded by
the counter) those strings occur only in soft-excluded `.ufo/waves/` paths that are unrelated to this item —
`.ufo/waves/round-16/w1/CR01.md` (`436-437`) and `.ufo/waves/round-16/w1/CRSource2.md`, `round-45/w2-results.json`,
`round-48/a2w1/T48A2ScribeReportWork.md`, `round-49/w1/T49ScribeConsider.md` (`bullet list`) —
`git grep -in '436-437' e3729de --` and `git grep -in 'bullet list' e3729de --`. My scratch run therefore reports
`EXPLAIN key-miss R41.7` and a total of 62 with every other term for my rows clean
(`T50Disp41.explain.stdout`: `fixed=6 open=0 declined=1 evidence_bad=0 key_miss=1 fixed_bad=0 declined_bad=0`).
`fix_plan` for the key: when the L1 writes `corpus/lessons/round-50.md`, add one decision line and cite it as the
row's evidence —
`R41.7 (`corpus/SOURCES.md:436-437`, a bullet list split across a blank line) declined: re-flowing a closed note is an in-place edit for no parse gain.`
I verified this in scratch (`T50Disp41.explain-probe.stdout`): with that line present and cited at
`corpus/lessons/round-50.md:3-3`, `key_miss` drops from 1 to 0 and no other term for my rows changes
(`total=61`, remaining terms are the 42 rows other seats own plus the floors). Because the file does not exist at
base, the delivered row keeps the `corpus/lessons/round-42.md:254-255` evidence so it resolves today; swap the
evidence item for the round-50 line once the lesson exists.

---

## Gates

- `python3 .ufo/evidence/round-50/c1/measure.py --lane <clone> --rev HEAD --explain` in a scratch clone
  (`git clone -q --shared <lane> $S/lane`, `git checkout -q -B rows 4afb060c…`, rows committed with a scratch
  identity): exit 1, my ids clean except the structural R41.7 key-miss; all other EXPLAIN lines are `missing` for
  the 42 items other seats own (`T50Disp41.explain.stdout`). Not a verdict — a probe.
- Ancestry: `git merge-base --is-ancestor c77c2b7 322b5cd` (yes), `… 322b5cd e3729de` (yes), `… 5f739acf e3729de`
  (yes), `… c77c2b7 5f739acf` (yes) — no cited commit predates routing or postdates base.
- v4 probe on base bytes (three live sites, above) — the only execution evidence in this report; everything else is
  read from committed bytes.

## Touched surfaces

Read-only on the lane except: `.ufo/waves/round-50/w1/T50Disp41.rows.json`, `T50Disp41.md`,
`T50Disp41.explain.stdout`, `T50Disp41.explain-probe.stdout`. No lane commit, no index change, no jj command, no
fleet-root file, nothing under `~/.local/state`, no mutant names or control stdout read. No tool installed
(pacman paused; python3/git already present).

## Out of scope

Other rounds' rows (42 seats own R40/R42–R49); the C1 verdict; any C2/shrinker work; the lane's SCORECARD Planned
paragraph (the L1 writes it — relevant only to `open` rows, of which I have none).

## Findings

1. Six of seven round-41 routed items are closed in the tree, all by round-42 commits
   (`322b5cd` instruments, `5f739acf` content); none was closed by prose alone.
2. R41.7 is a recorded decline by the lane, not an omission (`corpus/lessons/round-42.md:254-255`), and the frozen key
   set for it has no resolvable carrier in the tree — a key defect in `defects.json`/`keys.json` that costs a
   `key_miss` on any honest ledger.
3. Citing `.ufo/waves/round-42/supersede/round-41-residual-receipt.json` (R41.2) is impossible under the counter's
   soft-path rule even though it is the fix; the row cites `corpus/QUALITY.md:1001-1011` (criterion 81) instead.
4. The round-41 instrument file itself still carries the old regex and the retired m9 class; that is correct for a
   closed round but a reader comparing instruments must compare against round-42, not round-41.

## Artifacts

- `.ufo/waves/round-50/w1/T50Disp41.rows.json` — 7 rows, ledger schema.
- `.ufo/waves/round-50/w1/T50Disp41.explain.stdout` — scratch counter run over my rows.
- `.ufo/waves/round-50/w1/T50Disp41.explain-probe.stdout` — scratch run proving the R41.7 keyed-decision fix.
- `.ufo/waves/round-50/w1/T50Disp41.md` — this report.

## Summary

- R41.1 fixed: line-scoped `BACKTICK_RE` at `.ufo/evidence/round-42/calibration/measure.py:79`, proven by T1 selftests.
- R41.2 fixed: superseding receipt `5f739acf` + QUALITY 81 (`corpus/QUALITY.md:1001-1011`); all eight seats present.
- R41.3 fixed: self-pin, records gate, out-of-process, `resolved`, exit-plus-FAIL all present and code-checked.
- R41.4 fixed: v4 probed at base bytes — the three v3 false positives are `unflagged:false`.
- R41.5 fixed: v4 docstring corrects the blanket claim; v3 stays pinned.
- R41.6 fixed: round-42 renumber map by document (`corpus/SOURCES.md:469-471`).
- R41.7 declined (lane's recorded decision); the frozen key set makes it a structural `key-miss`, fix verified in scratch.
- Scratch counter over my rows: fixed=6, declined=1, all terms clean except that key-miss; probe with a round-50 decision line clears it.
