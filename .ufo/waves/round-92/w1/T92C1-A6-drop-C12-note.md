source: S316 gawk(1), `sub()` replacement `&` (docs, tier A, mined, opened 2026-11-06) — https://man.archlinux.org/man/gawk.1.en, `.ufo/evidence/round-90/sources/s-gawk1.txt:1026-1028`: "An & in the replacement text is replaced with the text that was actually matched" (grounds C09); S317 bash(1), `-e`/`-f` (docs, tier A, mined, opened 2026-11-06) — https://man.archlinux.org/man/bash.1.en, `.ufo/evidence/round-90/sources/s-bash1.txt:3197-3200`: "True if file exists and is a regular file" (grounds C08); S001 Stryker mutant states and metrics — relied on only for the `detected / valid` arithmetic behind 5/12; fleet `scripts/sources-census.sh` @ `f47ad6ba` (the pinned gate, read-only)
verified-at: 2026-11-06; spec sha256 `ce8983d5…e290` committed alone in `33dd6e47` (18:15:50 -03:00, before any verdict receipt) together with the predictions in `pre-freeze/expected.tsv`; controls committed in `3cf905bc` (18:26:24 -03:00) and `a4797ebe` (18:28:47 -03:00); the twelve verdicts below are copied from `pre-freeze/controls/CTL1b-nowork-A.out` (rev `33dd6e47`, rows `:2-13`) and the positive control prints the same twelve (`pre-freeze/controls/CTL14-pos.out:2-13`, `C1_R90_PASS=true` at `:16`); pin and fixture facts re-read from the fleet object store at `f47ad6ba` for this draft
recheck: `git -C /home/vgpnk/Projects/shokunin show f47ad6ba8d306f8125597401cb2ce45c1297a593:scripts/sources-census.sh | sha256sum` → `3fb72615…4e30`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file blob <REV>:.ufo/evidence/round-90/c1/census-mutants.json | sha256sum` → `ce8983d5…e290`; `python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-90/c1/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev <REV> --work <empty dir>` → `C1_R90_PASS=true` once the note is landed (honest-fixture state: `pre-freeze/controls/CTL14-pos.out:16`)

# Mutation case 12 — fleet scripts/sources-census.sh

The twelfth recorded case and the first whose target is the fleet's own gate: the
eleven earlier legs measure gates inside sibling lane repos, this one measures
`scripts/sources-census.sh` in `/home/vgpnk/Projects/shokunin` at `f47ad6ba`
(`plans/round-90.plan.md`, R90-C1; `measure.py:1-30`). The gate is read-only here:
every mutant is a scratch copy materialized from the fleet's object store
(`measure.py:71-84`), sha256-equal to the pin (`C1_CONJUNCTS pin=true`,
`CTL1b-nowork-A.out:15`), so no fleet byte is written.

Why it matters: the gate is the fleet's source-registry CLI (`AGENTS.md:16`,
`README.md:44-47`). The roster is built from `shokunin.conf` plus each lane's
`corpus/SOURCES.md` (`sources-census.sh:452` `build_roster`); the two main-repo
lanes hold no corpus (`PROTOCOL.md:435`), so every lane that keeps a registry is
censused through it, and round-end censuses are recorded with it (tameshi:
`corpus/SOURCES.md:573,589`; this round's `pre-freeze/census-start.txt:1-22`,
`tameshi ok … exit=0` at `:21-22`). A hole in the gate's own selftest is a hole
in the certificate every lane's census rests on.

A bare `sources-census.sh:NN` is the pinned blob at `f47ad6ba`; a bare
`census-mutants.json:NN` is under `.ufo/evidence/round-90/c1/`, a bare
`pre-freeze/…:NN` under `.ufo/evidence/round-90/`, and a bare
`T90SC1-fixture-absence.out:NN` under `.ufo/waves/round-90/w1/`.

## 0. Pin and suite

- Target: fleet repo `/home/vgpnk/Projects/shokunin`, rev
  `f47ad6ba8d306f8125597401cb2ce45c1297a593` (protocol-shokunin
  <protocol@shokunin.local>, 2026-10-25T09:29:03-03:00), path
  `scripts/sources-census.sh`, mode 100755, git blob
  `3f314620b2395eeb70d8405410132027dfe608e4`, sha256 `3fb72615…4e30`, 35 466 B,
  806 lines (`census-mutants.json:3-8` for repo/commit/path/sha256; size and line
  count read from the pinned blob with `git cat-file -s` and
  `git show <pin>:<path> | wc -l`; the sha256 matches `C1_CONJUNCTS pin=true`).
- Fixtures: `scripts/fixtures/sources-census` (`census-mutants.json:8`) — five
  registries, 22 rows, plus 17 row-shaped lines written by the selftest's own
  fixtures (`T90SC1-fixture-absence.out:2`).
- Modes: census (default), validate, overdue, shared, selftest
  (`sources-census.sh:12`); exit 2 for usage/env/missing registry, 3 for selftest
  failure (`:17`).
- Suite: the gate's own `selftest` (`:98-447`), invoked as `bash <copy> selftest`
  in the fixture tree; the suite is green iff every arm prints `killed` and the
  exit is 0 with the literal `selftest ok` (`:447`).
- Oracle (suite `selftest`, 180 s, two runs per verdict: `census-mutants.json:10-14`;
  all mechanics from the counter): rc 0 = SURVIVED, rc ≠ 0 = KILLED, 180 s timeout
  = INCONCLUSIVE, two runs differing = UNSTABLE (`measure.py:172-176`);
  pristine green twice (`:143-144`); canary = pristine with `exit 97` after
  line 1 must exit 97 (`:147-150`); each mutant must occur exactly once in the
  pin, differ from it, and pass `bash -n` (`:152-166`); a "trivial" mutant — one
  whose `validate` on the fixtures' clean lane c exits 2 or prints
  `gawk failed`/`syntax error` — is rejected rather than measured
  (`:167-170`); each mutant's witness registry from the spec is rebuilt and run
  under pristine and mutant in its declared mode, `differs` iff (rc, stdout)
  differ (`:177-192`).

## 1. The measured table — 5/12 killed

`C1_SUMMARY … n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0
trivial=0 witnessed=7/7 note=absent mismatched=0` (`CTL1b-nowork-A.out:14`);
every row's two runs agree, and every survivor's witness differs
(`witness=differs`, `:2-13`). The verdict cells below are copied verbatim from
that receipt.

| id | arm targeted | edit | verdict | witness |
|---|---|---|---|---|
| C01 | E10 community-at-A | `:668` `kind=="community"` → `kind=="communityX"` | KILLED | validate; one community row at tier A (S001) |
| C02 | W02 thin-reject length boundary | `:671` `length(teaches)<8` → `<7` | SURVIVED | validate; one rejected row, teaches `1234567` (7 chars) |
| C03 | E04 supersedes exemption id width | `:648` `/supersedes S[0-9]{3}/` → `{4}` | SURVIVED | validate; S002 teaches `supersedes S001 with newer text` |
| C04 | overdue due-day boundary | `:684` `due<=today_s` → `due<today_s` | KILLED | overdue; opened 2026-10-07 + 30d = `--today` 2026-11-06 |
| C05 | E08 opened-today boundary | `:661` `opened_epoch>today_s` → `>=` | KILLED | validate; one row opened 2026-11-06 = `--today` |
| C06 | separator row with alignment colons | `:596` `^:?-+:?$` → `^-+$` | SURVIVED | census; separator `:---` / `:---:` / `---:` over one row |
| C07 | awk row-indent width 0-3 | `:615` bound `{0,3}` → `{0,2}` | KILLED | census; header, separator and row indented three spaces |
| C08 | E11 used-by existence test (`-e`) | `:566` `! -e "$dir/$path"` → `! -f` | SURVIVED | validate; used-by `corpus/knowledge` (a directory) |
| C09 | URL fragment normalization | `:602` `sub(/#[^ ]*$/,"",u)` → `"&"` | SURVIVED | validate; two rows `…/p#a` and `…/p#b`, same scope |
| C10 | symbolic cadence with spaces | `:582` class `[A-Za-z0-9 _-]` → `[A-Za-z0-9_-]` | SURVIVED | validate; recheck `on next release` |
| C11 | missing-registry exit 2 | `:804` `[ "$missing_error" = 1 ] && exit 2` → `exit 1` | KILLED | validate; no `corpus/SOURCES.md` at all |

measured: 5/12 killed

The five kills are named selftest arms, not incidental exit codes:

- **C01** — `E10-community-at-A` (`sources-census.sh:135`) validates fixture lane
  a, whose S010 is a community row at tier A
  (`scripts/fixtures/sources-census/root/a-shokunin/corpus/SOURCES.md:17`); with
  `kind=="communityX"` no E10 line is printed and the check goes red.
- **C04** — `cadence-due-on-opened-plus-N` (`:147`) expects `S002 0d` at
  `--today 2026-08-30`; a's S002 opened 2026-06-01 with `90d` is due exactly that
  day (`…/root/a-shokunin/corpus/SOURCES.md:8`), so `due<today_s` drops the row.
- **C05** — z's only row opened `2026-10-19`
  (`…/root/z-shokunin/corpus/SOURCES.md:7`) equals `--today 2026-10-19` in
  `unlisted-warning-not-failure` (`:157`) and `UTC-date-in-Sao-Paulo`
  (`:160-161`), which require z to stay `ok` / exit 0; under `>=` E08 fires and
  both report `SURVIVED`.
- **C07** — the indent loop (`:287`) runs widths 0-3; at width 3 the census
  checkline expects `rows 1` (`:308`) and the overdue check expects the row
  (`:313`), and `{0,2}` stops parsing the width-3 registry.
- **C11** — `validate-missing-exit-2` (`:144`) runs the missing fixture lane d
  and requires exit 2.

## 2. Survivors — seven holes, seven witnesses

Each survivor changes a branch the suite never exercises. The counts below are
from the wave probe reading the pin's committed bytes
(`T90SC1-fixture-absence.out`, source `T90SC1-fixture-absence.py`); the witness
column is the spec's registry (`census-mutants.json`), and every one of them
prints differently under pristine and mutant (`witness=differs` at
`CTL1b-nowork-A.out:3-5,7-13`). The killing arms are report-only: they are not in the fleet gate. Each was
proven in scratch copies by wave seat T90E3 (`.ufo/waves/round-90/w1/T90E3.md`,
patch `T90E3-arms.patch`, driver `T90E3-prove.sh`, transcript `T90E3-prove.out`):
pristine + arms stays green (`selftest ok`), each survivor mutant + arms exits 3
with its arm red, and the five killed mutants stay killed — `VERDICT: arms-kill-7/7`.

| survivor | what the selftest misses (at the pin) | witness registry (one line) | consequence | killing arm (report-only, proven in scratch by T90E3) |
|---|---|---|---|---|
| C02 · W02 thin-reject length | the only rejected rows with a short reason teach `no` (2 chars; a S015 and z S001); the generated rejected rows teach 17, 25 and 24 chars, so no cell sits at 7 and `<8` and `<7` agree on every observation (`:6-7`); `W02-thin-reject` (`:138`) is green either way | one rejected row, teaches `1234567` | a 7-character rejection reason — the thinnest text W02 exists to refuse — becomes admissible silently (false negative) | a lane fixture with that row; `check "W02-thin-7" "W02" … validate …` — pristine prints W02, the mutant prints nothing |
| C03 · E04 supersedes exemption | no fixture or generated row carries `supersedes` (`:5`: 0 in fixtures; the gate's two hits are the comment at `:25` and the regex at `:648`); the E04 duplicate-url fixture (a S003/S004, same URL `c.example/x`, same scope, `…/root/a-shokunin/corpus/SOURCES.md:9,11`) is caught identically under both regexes because neither teaches cell contains the word | two rows, the second teaches `supersedes S001 with newer text` | a legitimate re-registration that names the superseded three-digit id is reported E04 (false positive, exit 1): the exemption silently stops covering S001-S999 | two-row fixture, second teaches `supersedes S001`; `checkx … 0` — pristine exempts, the mutant prints E04 and exits 1 |
| C06 · alignment separator | all 12 separator rows across the fixtures and the gate-generated fixtures are plain dash runs with no colon (`:3`), so `separator_row`'s `^:?-+:?$` is only ever exercised with the plain form (e.g. `…/root/a-shokunin/corpus/SOURCES.md:6`) | registry whose separator is `:---` / `:---:` / `---:` over one valid row | a GitHub-style alignment separator is parsed as a data row: the dash cells fire E02 plus the enum/date checks (E05-E09) and are counted as a row with `tier.invalid`/`status.invalid`, so validate exits 1 on a well-formed registry and census inflates | registry with an alignment separator and one row; `checkline` census `rows 1` plus `checkx` validate 0 |
| C08 · E11 existence test | every used-by cell at the pin names a regular file (`corpus/knowledge/real.md`) or an absent path (`corpus/knowledge/ghost.md`, `corpus/knowledge/missing-N.md`); 0 cells name a directory (`:10-11`), the only input on which `-e` and `-f` differ; the E11 arms observe only file and absent (`:136`, `:328`) | one mined row, used-by `corpus/knowledge`, the directory created | a used-by cell naming a directory is reported "missing used-by" and validate exits 1 although the path exists (false positive) | a fixture lane with `corpus/knowledge/` present and a mined row citing it; `checkx … 0` — pristine clean, the mutant prints E11 and exits 1 |
| C09 · URL fragment strip | no URL cell at the pin carries a `#` — every `#` byte is a heading (`:4`); the only normalization the suite sees is trailing slash plus host case (`shared-across-lanes`, `:152`, a S016 `https://SHARED.example/canon/` vs b S001 `https://shared.example/canon`), so the fragment substitution never runs with a fragment | two rows, same scope, `https://w9.example/p#a` and `…/p#b` | a fragment regression suppresses the duplicate-URL finding: two citations of one page at different anchors stay distinct, so a genuine duplicate escapes E04 within scope (and W04 across scopes) | two rows in one scope, `#a` and `#b`; `check "E04-fragment-duplicate" "E04" …` — pristine prints E04, the mutant prints nothing |
| C10 · symbolic cadence space | the distinct symbolic cadences at the pin are `annual` and `on-release` (`:8`) — no internal space; `symbolic-on-release-reported` (`:148`) and `symbolic-annual-reported` (`:149`) are the only symbolic observations and the generated rows use `30d`/`90d`/dates | one row, recheck `on next release` | a spaced symbolic cadence is refused at admission (E09, exit 1), and in overdue mode it is neither numeric nor symbolic, so `due=epoch(…)` is INVALID and the row is never reported due — freshness is lost silently | one row with `on next release`; `checkx … 0` — pristine clean, the mutant prints E09 and exits 1 |
| C12 · used-by comma-list trim | used-by cells are single-path or `—` everywhere at the pin and 0 cells contain a comma (`:9`); `IFS=',' read -a` splits before `trim_cell` runs (`:561-564`), so the second path keeps its leading space when the trim is dropped, and no fixture has two paths | one mined row, used-by `corpus/a.md, corpus/b.md`, both files present | a multi-path used-by — the ordinary shape of an entry cited by several knowledge files — yields E11 for the space-prefixed second path and exit 1 on a path that exists (false positive) | both files present, one mined row listing them; `checkx … 0` — pristine clean, the mutant prints E11 for ` corpus/b.md` |

Two readings to keep apart: the survivors are holes in the *suite*, not proof that
the gate misbehaves on live registries. Each is non-equivalent on its witness
(`witness=differs`), but whether the absent fixture feature occurs in a lane's
real registry is a different measurement (routed to the round's impact seat,
report-only).

## 2b. Fleet impact of the seven holes (report-only)

Wave seat T90CN1 scanned every real fleet registry (`*-shokunin/corpus/SOURCES.md`, 21
lanes) under the pinned gate's own parsing rules and ran pristine vs mutant over the
lanes that hit each class (`.ufo/waves/round-90/w1/T90CN1.md`, script `T90CN1-scan.py`):

| survivor | lanes hit | effect on live registries |
|---|---|---|
| C12 used-by trim | 20 | 1695 false E11 findings over 1146 mined rows, validate exit 0 -> 1 on 20 lanes; every trimmed path exists |
| C03 supersedes width | 20 shape / 15 effective | 97 rows gain E04, validate exit 0 -> 1 on 15 lanes |
| C09 fragment strip | 9 | W04 set changes (+15 / -111); exit unchanged |
| C10 spaced cadence | 2 | 11 rows gain E09 and lose their cadence line; exit 0 -> 1 on 2 lanes |
| C02, C06, C08 | 0 | no live registry carries the shape today |

So the selftest's most consequential hole is C12: the fleet's ordinary multi-path
`used-by` convention (`path, path`) is exactly the input no fixture carries, and a
regression that drops the per-path trim would turn every lane's round-end census red
while the gate's own selftest stays `selftest ok`. The T90E3 arm for C12 kills it.

## 3. Predictions vs measured — 12/12

The spec was committed alone in `33dd6e47` with twelve ids, edits and predictions
before any verdict receipt, and the counter pins the spec bytes
(`measure.py:40`; `C1_CONJUNCTS spec=true`). The measured table is 5 KILLED + 7
SURVIVED (`CTL1b-nowork-A.out:2-13`) and every prediction in
`pre-freeze/expected.tsv:4-15` holds: **12/12, no flips**. The predictions'
stated reasons name the same arms the table's prose does — e.g. C04 "expects
`S002 0d` on the due day" (`expected.tsv:7`), C05 "z lane opened 2026-10-19 =
`--today` 2026-10-19 → E08 under `>=`" (`:8`), C07 "indented-*-3 arms use a
3-space indent" (`:10`).

Prediction accuracy and kill rate are separate readings: 12/12 says the prior
table was right about this suite, 5/12 says the suite observes five of these
twelve faults. Amendment 1 to the expectations touched only counter controls and
says so; the C1 predictions are unchanged (`expected.tsv:35`).

## 4. Limits

- One pin (`f47ad6ba`), one host, one suite. 5/12 is a property of this spec
  under this selftest, not of the gate's strength against faults.
- The gate's production modes are observed only through the checks the selftest
  makes, over the shipped fixture tree and fixtures the suite writes itself; the
  selftest never runs the gate over a live lane registry. `--out` has exactly one
  guard arm (`:383-393`), and the CLI's behaviour under `--out` beyond that guard
  is unobserved.
- A SURVIVED witness proves non-equivalence on one registry, not that the
  behaviour matters on real registries; the impact of the seven holes is measured
  separately (report-only).
- The canary shows the scratch copy runs, not which selftest arm executed a
  mutated line (`plans/round-90.plan.md`, R90-C1 declared limits).
- The counter's environment is minimal — `PATH` fixed, `HOME`/`TMPDIR` inside the
  work dir, `LC_ALL=C.UTF-8` (`measure.py:64-69`). Outside it, wave seat T90E1 re-ran
  every mutant's selftest twice in an ordinary shell with its own driver and agreed
  12/12 (`.ufo/waves/round-90/w1/T90E1.md`, `VERDICT: reproduced-12/12`), and T90L1
  found the verdicts invariant across six TZ/locale/PATH/TMPDIR environments
  (`T90L1.md`, `VERDICT: invariant`).
- The counter reads only this note's twelve verdict cells, the `measured:` line and the
  `source:` line (`measure.py:209-245`); the prose, the survivor table and the arms are
  not counted. A note that copies the committed predictions instead of the measured
  receipt carries the same cells and passes (wave critic T90C1, `T90C1.md` probe A):
  the counter certifies that the cells are true, not how they were obtained. This note's
  cells are copied from the measured receipt `CTL1b-nowork-A.out:2-13`.

## 5. Reproduce

The frozen counter (sha256 `d7365bbb…b528`,
`pre-freeze/instrument-sha256-v2.txt:1`):

```sh
S=/fast/scratch/hyaku/tameshi-r90/<seat>/replay
mkdir -p "$S"
python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-90/c1/measure.py \
  --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 33dd6e474ec3660f72c3c1e1c30105269807fe12 --work "$S"
```

Expected: the twelve `C1_ROW` lines of `CTL1b-nowork-A.out:2-13` (twice-identical
runs, `witness=differs`), then

```
C1_SUMMARY rev=33dd6e474ec3660f72c3c1e1c30105269807fe12 n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0 trivial=0 witnessed=7/7 note=absent mismatched=0
C1_R90_PASS=false
```

At `33dd6e47` the failing conjuncts are exactly the note-dependent ones —
`note`, `ids`, `mismatched0`, `figure`, `source`, `coverage` (`:15`); at the landing revision with the note and its registry rows the same
twelve verdicts print and `C1_R90_PASS=true` (`CTL14-pos.out:16`).

The survivor-side absence facts, re-runnable from committed bytes:

```sh
python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-90/w1/T90SC1-fixture-absence.py \
  /home/vgpnk/Projects/shokunin f47ad6ba8d306f8125597401cb2ce45c1297a593
```

Expected: the eleven lines of `T90SC1-fixture-absence.out`, including
`gate_blob_sha256 3fb72615…4e30`, `SEP total 12 with_colon 0`,
`URL_FRAGMENT rows_with_fragment 0`, `SUPERSEDES fixture_occurrences 0`,
`REJECTED exactly_7_chars 0`, `SYMBOLIC_CADENCE … with_space []`,
`USED_BY … with_comma []` and
`USED_BY_DIRECTORY fixture_cells_naming_a_directory 0`.

## Admission status (appended round 91)

Appended; the entry above is unchanged. Its coverage-map row is
`corpus/README.md` § "Round 90 — coverage map: the fleet's own registry gate".
This row carries **not admitted**: R90-C1 was killed by its own frozen rule (a) —
the round-90 counter honoured `refs/replace` (T90R1 K2) and skipped an ambiguous
id-keyed row (T90R1 K1) (`corpus/lessons/round-90-verifier-spotcheck.md` §2.3).
The verdicts above were independently reproduced (T90E1, T90L1, and again in
round 91 by `.ufo/waves/round-91/w1/T91E1.md`, `VERDICT: reproducible`) and are
stated as measurements; the kill is on the counters that certified them, not on
the measured table. Round 91's sealed successor that was to re-certify this note
was itself killed (`.ufo/waves/round-91/w1/T91C1.md` §1,
`corpus/lessons/round-91.md`), so this note stays a measurement without a
standing certificate.
