seat: ExecMirror
item: C3 integration dry run in a throwaway Git mirror — three registry rows S258/S259/S260, three re-grounded entries, README index, then five declared breaks (plus two extra) with the counter line for each.

## What was built

Scratch repo `D=/tmp/tameshi-r46-ExecMirror/d.tG0c7c`, created exactly as the item prescribes:

```
D=$(mktemp -d /tmp/tameshi-r46-ExecMirror/d.XXXXXX)   # -> /tmp/tameshi-r46-ExecMirror/d.tG0c7c
git -C "$D" init -q -b m
git -C "$D" rev-parse --show-toplevel                 # -> /tmp/tameshi-r46-ExecMirror/d.tG0c7c  (equals $D)
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive 745a583181648cfc7f9c1b476cd1be7dc68f7433 | tar -x -C "$D"
```

The extraction produced 146 MB. Blob counts measured as `git -C <repo> ls-tree -r <rev> | awk '{print $3" "$4}' | sort -k2 | wc -l`: 9632 for the lane at the freeze rev, 9635 for the mirror at its final HEAD (the three new entries). Nothing in the lane was written: my only lane write is this report.

Integration commit `f762d3138912eec24db06995488165bd31ca1ce5` ("r46 C3 scratch mirror: S258/S259/S260 + three entries + index").

Blast radius against the freeze tree (`git -C lane ls-tree -r 745a583…` vs `git -C "$D" ls-tree -r HEAD`, compared as `sha path` pairs, `diff` exit 1) — exactly five paths differ and nothing else:

```
> 47d232a0 corpus/knowledge/r5-undetected-flaky-failures.md      (new, 3327 B)
> 21b69446 corpus/knowledge/r6-flaky-failures-cluster.md         (new, 2987 B)
> 040a944f corpus/knowledge/r9-false-red-rate.md                 (new, 3359 B)
< 60a5f770 -> f12d67b0 corpus/README.md                          (section appended)
< b61cd91f -> a85a2203 corpus/SOURCES.md                         (three rows appended)
```

Rows: appended directly after the last registry row (S257) and before `## Paths`, so all three sit inside `## Registry` (`corpus/SOURCES.md` headings: `## Registry` at :8, `## Paths` at :137 after insertion). Each row has 13 `|`-split cells (`awk -F'|' '{print NF}'` → 13), status `mined`, tier A, kind `paper`/`paper`/`docs`, opened `2026-10-25`, recheck `365d`; the anchor cell carries the snapshot path and an 8-hex prefix:

| id | source URL | snapshot | bytes | sha256[:8] | used-by |
|---|---|---|---|---|---|
| S258 | `https://arxiv.org/abs/2504.16777` | `.ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html` | 43376 | `28d2954d` | `corpus/knowledge/r6-flaky-failures-cluster.md` |
| S259 | `https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/` | `.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html` | 51850 | `5eb59adf` | `corpus/knowledge/r5-undetected-flaky-failures.md` |
| S260 | `https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json` | `.ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json` | 8353 | `434d8658` | `corpus/knowledge/r9-false-red-rate.md` |

Entry basenames deliberately match the package copies (`r6-flaky-failures-cluster.md`, `r5-undetected-flaky-failures.md`, `r9-false-red-rate.md`) — the counter resolves the package copy by basename, so matching names is what puts the freshness test in force. Each entry opens with the three-line provenance header (`source:` citing its row / `verified-at: 2026-10-25` / `recheck: 365d — <re-run command>`), carries its quotes on single lines, and each is indexed in `corpus/README.md` as a backticked `knowledge/<file>` under a new `## Round 46` table.

Quote accounting, computed with the counter's own `fold`/`norm_text`/`QUOTE_RE` over the committed entries (script `/tmp/tameshi-r46-ExecMirror/` — inline python importing `measure.py` by path):

```
r6 located=5 fresh=3
r5 located=5 fresh=5
r9 located=4 fresh=3
```

(the r9 fifth quote, "we see a continual rate of about 1.5% of all test runs reporting a flaky result", is a true sentence that the counter cannot locate: the feed snapshot carries it as `reporting a \"flaky\" result`, so the escaped quotes break the substring — see failure mode F9 below).

## Receipts

**Before (read-only, lane repo, no writes):**

```
python3 .ufo/evidence/round-46/coverage/measure.py --lane <lane> --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433
C3_R46: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=745a583… C3_R46_PASS=false     exit 1
python3 … --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
C3_R46: self_pin=0 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=683eedd… C3_R46_PASS=false     exit 1
```

`self_pin=0` at base is expected and worth knowing: the counter pins *its own bytes at REV*, so a deciding run must be at a revision that contains the frozen counter (REV ≥ freeze). At base the counter file does not exist.

**After (mirror, integration commit f762d31):**

```
python3 "$D/.ufo/evidence/round-46/coverage/measure.py" --lane "$D" --rev f762d3138912eec24db06995488165bd31ca1ce5
ENTRY corpus/knowledge/r5-undetected-flaky-failures.md
ENTRY corpus/knowledge/r6-flaky-failures-cluster.md
ENTRY corpus/knowledge/r9-false-red-rate.md
C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=f762d31… C3_R46_PASS=true   exit 0
```

23 pre-existing entries are listed as `REFUSED … no provenance trio` on every run; that is the lane's standing state, not something this integration changes (the same 23 lines appear at the freeze rev).

**Census:**

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$D/corpus/SOURCES.md"
file  W01  S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
file  W04  S047,S048 (pitest.org/quickstart/incremental_analysis), S075, S076, S077, S078, S081, S092, S104, S160
file  ok   $D/corpus/SOURCES.md
exit 0        (12 lines: 1 W01, 10 W04, 1 ok; no E codes)
```

All eleven warnings are pre-existing at the freeze rev; my three rows add none. In particular S260's *feed* URL does not collide with S026's *page* URL (`https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html`), so no W04.

**Counter selftest** (allowed mode; sanity that the frozen counter behaves in this tree):

```
python3 "$D/.ufo/evidence/round-46/coverage/measure.py" --selftest
C3_R46_SELFTEST: cases=24 failed=0
VERDICT: PASS        exit 0
```

## Recipe for a later round (followed end to end here)

1. `D=$(mktemp -d /tmp/tameshi-r46-<Seat>/d.XXXXXX) && git -C "$D" init -q -b m`; assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before anything else.
2. `git -C <lane> archive <freeze-rev> | tar -x -C "$D"` — the mirror carries the frozen counter and the committed snapshots, so `self_pin=1` is automatic and no snapshot has to be copied.
3. Confirm the three snapshots exist in the mirror and record size + `sha256sum <f> | cut -c1-16` for each: `28d2954d22ea45af` (43376 B), `5eb59adf099304a0` (51850 B), `434d86586ecf3ea0` (8353 B). The 8-hex prefix written into the row is the first 8 of those (`28d2954d`, `5eb59adf`, `434d8658`) and must be a prefix of the snapshot bytes at REV.
4. Take the ids from the guard map, not from a naive next-free counter: `S258/S259/S260` are the guard-admitted floor (`assimilation/guard-map.json` `map_floor: S258`), and `assimilation/reg-ids` shows none of them taken while staged ids `S161–S255` stay reserved.
5. Append one row per document **immediately after the last registry row** (inside `## Registry`, never after `## Paths`), with exactly 12 pipes / 13 cells, `status=mined`, and the snapshot path + 8-hex digest **in the anchor cell** (cells[6]) — the digest check reads cells[6] only (`measure.py:110,117`).
6. Write each entry at `corpus/knowledge/<basename>.md` where `<basename>` equals the package copy's basename, with line 1 `source:` citing the row id, line 2 `verified-at: 2026-10-25`, line 3 `recheck: …` (lines 1-3 are positional, `measure.py:126-134`).
7. Put every quote on **one physical line**, 6–25 whitespace tokens after folding, 10–400 characters, in straight or curly double quotes (`measure.py:52,142`); make sure at least one located quote does **not** occur in the package copy of the same basename (freshness, `measure.py:147-151`).
8. Index each entry in `corpus/README.md` as a backticked `` `knowledge/<file>` `` or `` `corpus/knowledge/<file>` `` (`measure.py:169-171`).
9. Commit (`git -C "$D" -c user.name=t -c user.email=t@t commit -qam …`) and run `python3 "$D/.ufo/evidence/round-46/coverage/measure.py" --lane "$D" --rev "$(git -C "$D" rev-parse HEAD)"`; expect `self_pin=1 rows=3 entries=3 indexed=3 covered=3 … C3_R46_PASS=true`, exit 0.
10. Validate the registry **in place**: `sources-census.sh validate --file "$D/corpus/SOURCES.md"` (exit 0, warnings only). Do not validate a copy elsewhere — the census resolves used-by against the file's grandparent directory (`sources-census.sh:497-503,564-568`), so a copy under `/tmp` produces one E11 per used-by row: measured, `validate --file /tmp/tameshi-r46-ExecMirror/SOURCES.copy.md` → `145 E11`, exit 1.

## Failure modes, measured

Each break is its own commit on `m`, measured, then restored by the next commit. All five required breaks plus two extra:

| # | rev | mutation | counter line | exit |
|---|---|---|---|---|
| B1 | `8582dac` | S258 used-by cell `corpus/knowledge/r6-flaky-failures-cluster.md` → `—` | `REFUSED corpus/knowledge/r6-flaky-failures-cluster.md not in used-by` / `C3_R46: self_pin=1 rows=3 entries=2 indexed=2 covered=2 row_ids=S258,S259,S260 … C3_R46_PASS=false` | 1 |
| B2 | `b81f58f` | S258 anchor digest `28d2954d` → `28d2954e` | `C3_R46: self_pin=1 rows=2 entries=2 indexed=2 covered=2 row_ids=S259,S260 … C3_R46_PASS=false` — **no REFUSED line for r6** | 1 |
| B3 | `11a2ac7` | r6 `verified-at: 2026-10-25` → `2026-10-24` | `REFUSED corpus/knowledge/r6-flaky-failures-cluster.md verified-at` / `… entries=2 indexed=2 covered=2 … C3_R46_PASS=false` | 1 |
| B4 | `c2bc72e` | removed the `` `knowledge/r9-false-red-rate.md` `` cell from the README row | `ENTRY corpus/knowledge/r9-false-red-rate.md (not indexed)` / `… rows=3 entries=3 indexed=2 covered=3 … C3_R46_PASS=false` | 1 |
| B5 | `8621a7f` | r6 body rewritten so every quote is package-copy text (relabel) | `REFUSED corpus/knowledge/r6-flaky-failures-cluster.md no quote fresh against the package copy` / `… entries=2 … C3_R46_PASS=false` | 1 |
| X1 | `f529eaf` | every r6 quote wrapped across two source lines (still 6–25 tokens) | `REFUSED corpus/knowledge/r6-flaky-failures-cluster.md no located quote` / `… entries=2 … C3_R46_PASS=false` | 1 |
| X3 | `1cf8318` | an extra `\|` inside S259's teaches cell (14 cells) | `C3_R46: self_pin=1 rows=2 entries=2 indexed=2 covered=2 row_ids=S258,S260 … C3_R46_PASS=false` — no REFUSED line for r5; census at the same tree: `file E01 S259 fields=12`, exit 1 | 1 |

Restored state `694c0e6` ("restore: final good C3 state"): `C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 … C3_R46_PASS=true`, exit 0; census exit 0; `git -C "$D" status --porcelain` empty.

Cross-checks worth carrying into the real round:

- **B1 is a warning in the census, a fail in C3.** `sources-census.sh validate --file "$D/corpus/SOURCES.md"` on the B1 tree prints `file W03 S258 mined but unused` and exits 0. The census cannot see the entry, so only the C3 counter turns a dropped used-by into a red.
- **B2 and X3 are silent in the counter.** A row that fails its own admission (digest, cell count, URL, status, indent, round-46 snapshot prefix) disappears from `rows`, and its entry then hits the `cites no flaky row` branch, which the counter deliberately does not print (`measure.py:172`). The verdict line still says `PASS=false`, but it does not name the row; the census names the cell-count case (`E01`) and nothing names a bad digest. Read `row_ids=` on the verdict line — a missing id there is the only in-counter signal.
- **B5 is the control the contract names** (`CTL_B` relabel) and it fires exactly as written; the relabel is rejected because `r6`'s two package sentences are present in `fold(package copy)` while all three fresh quotes are not.
- **X1 shows the single-line rule is load-bearing.** The counter's quote regex forbids newlines (`[^"\n]`), so a wrapped blockquote is invisible, not merely unmatched: the entry degrades from "fresh" to "no located quote" with no other change.

## Failure modes read from the counter but not exercised here

Marked as code-read; each cites the line that would decide it.

- **F1 pipe anywhere in a cell** — 13-cell test `measure.py:105` (exercised as X3) and the census's `E01`.
- **F2 four-space indented row** — `ROW_RE = ^ {0,3}\|` (`:48`) and the census's 0–3-space parser both ignore it; the row would be invisible to both. [code-read]
- **F3 digest placed in the teaches cell** — `HEX_RE.findall(cells[6])` only (`:117`); the row drops silently, same shape as B2.
- **F4 a URL earlier in the source cell** — `URL_RE.search(cells[2])` takes the *first* URL (`:107`); a title containing a link before the source URL would make the row unmatchable.
- **F5 snapshot under another round's directory** — `SNAP_RE` hard-codes `.ufo/evidence/round-46/coverage/sources/` (`:50`); the counter's own T12 selftest asserts `rows=0` for a `round-45` prefix.
- **F6 snapshot path or digest in the wrong cell vs a missing blob** — `tree.read` returning `None` skips the row (`:112-114`); indistinguishable from a wrong URL in the verdict line.
- **F7 entry whose line 1 cites two rows, one not listing it in used-by** — `cited` is filtered to rows whose used-by contains this exact path (`:136`), so the extra citation is silently dropped and `covered` never grows.
- **F8 package copy dropped in verbatim** — the package files open with a blank line and cite staged ids (`source: S195 — …`), so a byte-exact copy fails first at `len(lines) < 3 or not lines[0].startswith('source:')` if the blank line is kept, and at `cites no flaky row` if it is stripped (`:126-129`). This is `CTL_A`; the counter's message differs between the two variants.
- **F9 escaped quotes inside a JSON snapshot** — the feed stores `\"flaky\"`, so any quote spanning that span can never be located (observed: r9 `located=4` of 5 written quotes). Pick JSON quotes that avoid `\"`; a curly-quote branch exists (`:52`) but does not help with backslashes.
- **F10 stale `verified-at` written as `2026-10-25T…`** — the regex is anchored to `\d{4}-\d{2}-\d{2}` right after `verified-at:` (`:131`); a timestamp still matches its date prefix, but a space before the date (`verified-at:  2026-10-25`) does match `\s*` while a different field order does not. [code-read]
- **F11 `covered != rows`** — every admitted row must be cited by an admitted entry (`:176-177`); a fourth row added without an entry turns PASS false even with three good entries.

## Bounds and non-runs

- Read-only on the lane: the only lane file written is this report. All scratch under `/tmp/tameshi-r46-ExecMirror/` (mirror repo `d.tG0c7c`, folded snapshot texts, receipts, blob lists).
- One lane side effect, recorded and removed: importing `coverage/measure.py` by path (to reuse its `fold`/`norm_text`/`QUOTE_RE` for the quote accounting) wrote `.ufo/evidence/round-46/coverage/__pycache__/measure.cpython-314.pyc` at 18:20:40 — `sys.dont_write_bytecode = True` runs too late to stop it. The directory is gitignored (`.gitignore:4:__pycache__/`, `git check-ignore` exit 0) and I deleted it (`rm -rf .ufo/evidence/round-46/coverage/__pycache__`); `git status --porcelain .ufo/evidence/round-46/coverage/` is now empty and `measure.py` is unchanged (18089 B, mtime 17:58). The `__pycache__` dirs under `control/` (18:04:28), `hardening/` (18:08:40) and `calibration/` (18:30:04) are not mine and were left alone. A later round should run the counter as a script (never import it) or `python3 -B`.
- No `git add/commit/stash/checkout/switch/reset/pull/push` in the lane, no jj command, no write under `/home/vgpnk/Projects/shokuknow`, no pacman. Every git call names `-C "$D"`; commits use `-c user.name=t -c user.email=t@t` inside `$D` only.
- No tool installed or upgraded (nothing was needed; python3/git/tar/gawk/coreutils were present).
- Not run, by bounds: the deciding C1 and C2 counters, `.ufo/evidence/round-46/no-harm.sh`, any build/lint/test/formatter. The C3 counter was run only as `--selftest` and against explicit `--rev` values (freeze, base, and my own mirror commits), never as a verdict.
- The mirror is not a deliverable: it is a recipe proof. The real round writes the same five paths into the lane and takes its deciding run at its own content revision.

## Risks

- **The r9 entry carries one unlocatable quote** (F9). The counter still admits the entry (`located=4`, `fresh=3`), so this is not a false pass, but a reviewer reading the entry against the snapshot will not find that sentence through the counter's fold; if the real round wants every quote machine-checkable, that sentence must be replaced or the snapshot must be re-committed unescaped.
- **`covered == rows` makes row count and entry count one number.** If a later round opens a fourth frozen document row without an entry, C3 goes false for a reason that reads like a coverage miss rather than an index miss; the verdict line distinguishes it only through `covered` vs `rows`.
- **Silent row admission failures** (B2/X3) mean a green-looking `rows=2` can be a typo, not a scope decision. The recipe's step 5 plus the `row_ids=` read is the cheap defence.
