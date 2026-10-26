## Sources & frontier

Registry rows **124 → 128** between base `473336d9d789f6081195e7376d17836a24666bc3` and content revision
`c7586b9a10effc63b4bd327f976edc094c1bdc17`. Counting command (the round-47 form, run on each revision's own blob):

```sh
git show 473336d9d789f6081195e7376d17836a24666bc3:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'   # 124
git show c7586b9a10effc63b4bd327f976edc094c1bdc17:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'   # 128
scripts/sources-census.sh census --file tameshi-shokunin/corpus/SOURCES.md   # file rows 128; tier.A 114 tier.B 11 tier.C 3;
                                                                             # status.mined 100 queued 22 rejected 6; exit 0
```

Semantic gate, as the contract's frontier step requires: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`.

| receipt | lines | codes | exit |
|---|---|---|---|
| start `.ufo/evidence/round-48/census-start.stdout` | 12 | 1×W01 (S101), 10×W04 | 0 (`.exit` = `0`, stderr empty) |
| end `.ufo/evidence/round-48/census-end.stdout` | — | — | not yet written at this reading: `deciding-run.sh:34` copies `after/census.stdout` here, and `.ufo/evidence/round-48/after/` does not exist |

The item's "if present" clause therefore does not fire yet, so the end state is shown two other ways and neither is a
verdict: the two committed wave receipts for the same tree, `.ufo/waves/round-48/a2w1/T48W2ExecC2Run-census.out.txt`
(10:30:41 −0300) and `.ufo/waves/round-48/a2w1/T48W2CritC2Rows.census.out.txt` (10:34:56 −0300), and this seat's own
read-only run (`sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`, output to scratch): **16
lines, 1×W01, 14×W04, 0 E codes, exit 0**, last line `tameshi	ok	…/corpus/SOURCES.md`. When the deciding run lands, its
`census-end.*` is the receipt the report cites; it runs the same command against the same tree, and nothing in `corpus/`
has moved since the content revision (`git diff --name-only c7586b9a HEAD -- corpus/ | wc -l` → 0; `git status
--porcelain -- corpus tools SCORECARD.md | wc -l` → 0), so the same 16 lines are what it measures unless another seat
writes the registry first. The delta from start is exactly four W04 lines —
`S265 … testing.googleblog.com/2016/05/…`, `S266 … pitest.org/quickstart/incremental_analysis`, `S267 …
github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml`, `S268 … www.tensorflow.org/federated/golden_tests?hl=zh-cn`
— the expected shape of a superseding row that carries its predecessor's URL under a new scope; W04 is non-fatal and
changes no lane status (no E04, no E03).

**Rows added by tier:** A=3 (S265, S266, S267), B=1 (S268), C=0; all kind `docs`, status `mined`, opened 2026-10-26.
Derivation: `git show <rev>:corpus/SOURCES.md | awk -F'|' '/^\| *S26[5-8]/{…}'` prints
`S265|A|mined|2026-10-26|730d`, `S266|A|…|90d`, `S267|A|…|on-release`, `S268|B|…|180d`; whole-registry tiers
`awk -F'|' '/^ *\| *S[0-9]/{gsub(/ /,"",$5); print $5}'` → base `111 A / 10 B / 3 C` = 124, rev `114 A / 11 B / 3 C`
= 128.

**Rows touched old→new:** no existing registry row's cells changed — `git diff --shortstat 473336d9 c7586b9a --
corpus/SOURCES.md` → `1 file changed, 4 insertions(+)`, 0 deletions, and the four added lines are S265–S268 at
`corpus/SOURCES.md:140-143`. The pointer refresh sits in the four knowledge entries the new `used-by` cells name
(`git diff -U0 473336d9 c7586b9a -- corpus/knowledge`):

| entry (line 1–2 of the file) | old → new |
|---|---|
| `corpus/knowledge/repeated-control-precondition.md` | `S026 — https://testing.googleblog.com/…; fetched 2026-10-20T02:13:47Z, sha256 ca1145fb…` → `S265 (supersedes S026) — …; re-fetched 2026-10-26T08:40:51Z, sha256 a4c5c46b…`; `verified-at: 2026-10-20` → `2026-10-26` |
| `corpus/knowledge/incremental-pin-disposition.md` | `…S047 — the same URL…` → `…S047 — …; S266 — https://pitest.org/quickstart/incremental_analysis/ — §Incremental analysis`; `verified-at: 2026-10-20` → `2026-10-26` (S048's base `used-by` is this entry, which quotes the page as S041/S047) |
| `corpus/knowledge/regression-tally-completeness.md` | `…S093 — bwrap(1)…; S094 —` → `…S093 — …; S267 — the same bwrap.xml at tag v0.13.1, re-anchored 2026-10-26…; S094 —`; `verified-at: 2026-10-23` → `2026-10-26 — S267 re-opened live: … sha256 2cb77df2f4be…` |
| `corpus/knowledge/r8-golden-update-flag.md` | `…S108 — https://www.tensorflow.org/federated/golden_tests?hl=zh-cn — 如何更新 .expected 文件？` → `…; S268 — the same zh-cn URL, re-anchored 2026-10-26…`; `verified-at: 2026-10-24` → `2026-10-26 — the zh-cn page re-opened live…` |

S093 and S108 keep their citations and gain the successor beside them; S026 is the exception — its citation is replaced
by `S265 (supersedes S026)`, so the base id survives only inside the successor's parenthetical. Base→rev occurrence
count of each id on the entry's `source:` line (`sed -n '1p' | grep -o '<id>\b' | wc -l`) is S026 1→1, S093 1→2,
S108 1→2, S048 0→0 (that entry never named S048; it names the same page as S041/S047).

**Frontier rows advanced:** S265–S268 are the round's frontier step (`.ufo/evidence/round-48/contract.json`
`frontier_step`): each opens 2026-10-26, is `mined`, and is pinned to a committed 2026-10-26 snapshot whose 12-hex digest
is in its anchor cell —

| row | snapshot | bytes | sha256 (first 12) | receipt `fetched_at` / `http_status` |
|---|---|---|---|---|
| S265 | `.ufo/evidence/round-48/freshness/sources/S026.html` | 236387 | `a4c5c46b4af9` | 2026-10-26T08:40:51Z / 200 |
| S266 | `.ufo/evidence/round-48/freshness/sources/S048.html` | 8892 | `e9cbc3e1ab7c` | 2026-10-26T08:40:42Z / 200 |
| S267 | `.ufo/evidence/round-48/freshness/sources/S093.xml` | 33289 | `2cb77df2f4be` | 2026-10-26T08:41:10Z / 200 |
| S268 | `.ufo/evidence/round-48/freshness/sources/S108.html` | 111409 | `04e4c091715a` | 2026-10-26T08:41:18Z / 200 |

(`sha256sum` named on each path — S108 starts `S1`, so an `S0*` glob shows three of the four.) No frontier **F-row**
changes status: `grep -c 'S265\|S266\|S267\|S268' corpus/README.md` → `0`, and the candidate-source cells still name
the base ids only — F3 `S004, S011, S025, S026, S027, S040` (`corpus/README.md:80`), F4 `S013…S045` (`:81`), F5
`S015, S016, S028` (`:82`), F7 `S003, S004, S005, S008, S041` (`:84`). F3/F4/F5/F7 stay `open`; a re-anchor is a
freshness repair of ground already counted, not a new ground. Sourced claim: C2, counted by the frozen
`.ufo/evidence/round-48/freshness/measure.py` against the snapshots, receipts and Gate lines in the table above
(`corpus/lessons/round-48.md` carries 4 lines matching `^- C2-QUOTE S[0-9]{3,} S[0-9]{3,}: \``) — this section cites the
state it reads, not its verdict.

**Assimilation: none.** Reason, from `.ufo/waves/round-48/w1/T48ScoutPackage.md`: neither claim needs a package row or
entry (C2 re-anchors the four held rows from their own live URLs); every staged row touching S026, S048, S093 or S108
is already held or already adopted — S216 already adopted as S260, S209 = held S107, S212/S210 are the same documents
under different carriers and supply no live-page snapshot; the staged ids S153–S255 still collide with held rows
(S153–S160) and no adoption map is needed for `none`. The one theme the scout ranks least-bad
(`r3-snapshot-fixture-update-paths`, staged S196/S152) is off both axes and was not taken.

**considerthese:** `corpus/lessons/round-48.md:9` reads `considerthese: idea 5 mined (section below)`; the section at
`corpus/lessons/round-48.md:364` records the proposal-uptake ledger (of eight absorbed proposals, criteria 79 and 86
were cited in later rounds, 76/78/80 not after their own round; proposals about a recurring thing fired, one-off
incidents did not) and lands as that lesson section only — no QUALITY criterion and no SOURCES row, because the table
has no falsifier a counter could pin.

**Mined mistakes:** nine rows in `corpus/lessons/round-48.md` `## Mistakes` (7 in the main table plus the two appended
mined-mistake blocks) — `landing` 4, `attribution` 1, `provider` 1, `reference-drift` 1, `scope` 1, `stale-premise` 1
(`awk '/^## Mistakes/,/^## considerthese/' … | grep -oE '^\| \`[a-z-]+\`' | sort | uniq -c`). Seven red-state commands
`d1`–`d7` carry the red-before receipts; row 1 is the round-47 C1 miss (a one-shot flaky observation restated as a
standing value, `.ufo/evidence/round-47/after/c1.stdout:5` against `SCORECARD.md:2318`), the premise CTL_B refuses.
