# T73W1S03 — binding audit of the six standing `wave-reconcile` rows

- **Seat:** T73W1S03 — round 73, wave w1, lane `tameshi-shokunin`.
- **Base revision:** `a3dd35742eee608d1205843dacebc461b4242b9e` (= `origin/master`).
- **Scope:** R73-C1 **binding**, not arithmetic: the six rows of
  `tameshi-shokunin/tools/wave-reconcile.json`; three deliberate span mutations;
  the round-72 report's `12 seats, 11 reports` population test.
- **Read-only:** no tracked file was written; no git/jj mutation was run. The
  only repository created was a `mktemp -d` fixture whose `--show-toplevel`
  was asserted equal to `$D` before its first commit, and it was removed at the
  end. Scratch `/fast/scratch/hyaku/tameshi-r73/T73W1S03/` deleted before yield.
- **No subagents, no tools installed or upgraded.** No LSP was used or exposed
  to this seat: the work is git-object and byte-level, not symbol navigation;
  every finding below is a `git` read or an in-process Python byte search.
- Every command below is shown with its exit code and its pasted output.

---

## 0. Verdict (seat opinion for the L1, not a verdict)

1. **All six rows bind.** Every record revision resolves as a commit, every
   record blob exists at that revision, every named span is a verbatim byte
   substring with a unique offset, and every artifact revision resolves with
   the named artifact present (`wave.dir` → tree, `wave.results` → blob;
   `declaration.path` → blob for the two `roles` rows).
2. **The three mandated span mutations are setup exit 2, each with a naming
   line; none is a silent pass.** One byte changed → `span-not-in-record`;
   one digit added to the printed token → `span-not-in-record`; a span lifted
   from another document → `span-not-in-record`.
3. **The report's `11 reports` matches no defensible population.** Every
   population defined over the committed wave artifacts at the row's artifact
   revision yields 0, 9, 10, 12, 13, 17, 20 or 26 — never 11. Top-level `*.md`
   and `results[]` both yield **12**. The only arithmetic path to 11 is to drop
   exactly one committed seat report (the `S01..S11` name truncation), which is
   the counting error the red arm measures, not a population.
4. **Scoped caveats that do not move the frozen counter** (L1 to judge):
   the `record` block is **inert** for `roles` and `attack_share` rows — a
   forged `record.span` there is a **silent pass** (`rows=6 met=6`, exit 0) —
   and row `r72-spec-roles` carries `printed=12` in a span (`"T72W1S01"`) that
   does not contain `12` at all. Separately, omitting `--extra-root fleet=…`
   makes a record-level `root: fleet` raise an uncaught `KeyError` (exit 1,
   traceback) instead of setup exit 2.

---

## 1. Frozen counters, for orientation (literal commands)

The frozen C1 counters, run exactly as frozen from the lane root. These are
context for the binding audit; the L1 owns the counter.

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-report-seatreports kind=seat_reports expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | declared={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1} measured={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1}
WAVE_ROW r72-plan-roles kind=roles expect=drift measured=drift ok | declared={"connector": 1, "critic": 1, "executor": 3, "labrat": 1, "mutation-tester": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1} measured={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1}
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | attack=3/12=25.0% floor=25.0%
WAVE_RECONCILE: rows=6 met=6 unexpected=0
exit=0
```

```
$ python3 -I -X utf8 tools/wave-reconcile.py --selftest      # TMPDIR on the seat scratch
SELFTEST arm1-seats-meet                      ok (got=meet want=meet)
SELFTEST arm2-seats-mismatch-caught           ok (got=1 want=1)
SELFTEST arm3-seatreports-drift-measured      ok (got=drift want=drift)
SELFTEST arm4-roles-spec-meet                 ok (got=meet want=meet)
SELFTEST arm5-roles-text-drift-measured       ok (got=drift want=drift)
SELFTEST arm6-attack-below-floor-caught       ok (got=1 want=1)
SELFTEST arm7-attack-at-floor-meet            ok (got=meet want=meet)
SELFTEST arm8-bom-refused                     ok (got=setup want=setup)
SELFTEST arm9-invalid-utf8-refused            ok (got=setup want=setup)
SELFTEST arm10-zero-rows-refused              ok (got=setup want=setup)
SELFTEST arm11-unresolvable-rev-refused       ok (got=setup want=setup)
SELFTEST arm12-declaration-absent-refused     ok (got=setup want=setup)
WAVE_RECONCILE_SELFTEST: 12/12 pass
exit=0
```

---

## 2. Six rows: revision resolution and byte binding

### 2.1 Summary table

| # | row id | kind | record root:path @ rev | rev type | record blob | span bytes | span offset (0-based) | span occ | printed | delimited in span | printed occ in span | engine reads `record`? | artifacts at row rev |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `r72-report-seats` | `seats` | fleet:`.ufo/reports/round-72/tameshi.md` @ `3664a6d3…` | commit | `7f8c8017…` | 20 | **3618** | 1 | 12 | **true** | 1 | yes | `wave.dir` tree, `wave.results` blob |
| 2 | `r72-report-seatreports` | `seat_reports` | fleet: same record | commit | `7f8c8017…` | 20 | **3618** | 1 | 11 | **true** | 1 | yes | same |
| 3 | `r72-plan-seats` | `seats` | lane:`plans/round-72.plan.md` @ `a3dd3574…` | commit | `4a9b4081…` | 25 | **179** | 1 | 12 | **true** | 1 | yes | `wave.dir` tree, `wave.results` blob |
| 4 | `r72-spec-roles` | `roles` | lane:`.ufo/waves/round-72/w1-spec.json` @ `a3dd3574…` | commit | `f5429c18…` | 10 | **4138** | 1 | 12 | **false** | **0** | **no** | `wave.*` + `declaration` blob |
| 5 | `r72-plan-roles` | `roles` | lane:`plans/round-72.plan.md` @ `a3dd3574…` | commit | `4a9b4081…` | 134 | **7042** | 1 | 12 | **true** | 1 | **no** | `wave.*` + `declaration` blob |
| 6 | `r72-attack-share` | `attack_share` | fleet:`.ufo/reports/round-72/tameshi.md` @ `3664a6d3…` | commit | `7f8c8017…` | 20 | **3618** | 1 | 12 | **true** | 1 | **no** | `wave.dir` tree, `wave.results` blob |

- Record blobs: report `7f8c8017af897291245d06f6045af59fdbe695a1` (18,439 B);
  plan `4a9b408164f6da483a05b4da2707be9c30a189b6` (7,372 B); spec
  `f5429c1811464a666a28ae16aac20391b694207f` (18,239 B).
- Every `wave.rev` is `a3dd35742eee608d1205843dacebc461b4242b9e`, which
  resolves as a commit in the lane repo; `.ufo/waves/round-72/w1` is a tree and
  `.ufo/waves/round-72/w1-results.json` is a blob at that revision.
- Row 4's declaration (form `spec-items`) is the same blob as its record:
  12 items, roles `{connector:1, critic:1, executor:3, mutation-tester:1,
  revenger:1, reviewer:1, scout:1, scribe:2, sentinel:1}`.
- Row 5's declaration (form `text-tokens`) span is at the **same offset 7042**
  in the same plan blob (1 occurrence) and all nine `N role` pairs are present
  in it (`3 executor`, `2 scribe`, `1 scout`, `1 connector`, `1 reviewer`,
  `1 critic`, `1 mutation-tester`, `1 sentinel`, `1 labrat`).

### 2.2 Audit output (one read-only script; byte search, exactly `bytes.find`)

The script reads the manifest read-only and, per row, runs
`git -C <root> cat-file -t <rev>`, `git -C <root> rev-parse <rev>:<path>`,
`git -C <root> cat-file blob <rev>:<path>`, the tool's own
`re.search(r'(?<![0-9])%d(?![0-9])' % printed, span)` and
`raw.find(span.encode())`.

```
manifest=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/wave-reconcile.json schema=tameshi-wave-reconcile-v1 rows=6

ROW 1 r72-report-seats kind=seats expect=meet
  record root=fleet repo=/home/vgpnk/Projects/shokunin
  record path=.ufo/reports/round-72/tameshi.md
  record rev=3664a6d30051410c3d2bb8c32926d13e284a5118 type=commit
  record blob=7f8c8017af897291245d06f6045af59fdbe695a1
  record bytes=18439 span-bytes=20 span-offsets=[3618] occurrences=1
  span head bytes=31322073656174732c20313120726570
  span tail bytes=207265706f727473
  printed=12 delimited-in-span=True occurrences-in-span=1
  counterexample-left  '912 seats, 11 reports' delimited=False
  counterexample-right '129 seats, 11 reports' delimited=False
  regex='(?<![0-9])12(?![0-9])'
  engine-reads-record-for-kind=True
  wave rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  wave dir    =.ufo/waves/round-72/w1 exists=True type=tree
  wave results=.ufo/waves/round-72/w1-results.json exists=True type=blob

ROW 2 r72-report-seatreports kind=seat_reports expect=drift
  record root=fleet repo=/home/vgpnk/Projects/shokunin
  record path=.ufo/reports/round-72/tameshi.md
  record rev=3664a6d30051410c3d2bb8c32926d13e284a5118 type=commit
  record blob=7f8c8017af897291245d06f6045af59fdbe695a1
  record bytes=18439 span-bytes=20 span-offsets=[3618] occurrences=1
  span head bytes=31322073656174732c20313120726570
  span tail bytes=207265706f727473
  printed=11 delimited-in-span=True occurrences-in-span=1
  counterexample-left  '12 seats, 911 reports' delimited=False
  counterexample-right '12 seats, 119 reports' delimited=False
  regex='(?<![0-9])11(?![0-9])'
  engine-reads-record-for-kind=True
  wave rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  wave dir    =.ufo/waves/round-72/w1 exists=True type=tree
  wave results=.ufo/waves/round-72/w1-results.json exists=True type=blob

ROW 3 r72-plan-seats kind=seats expect=meet
  record root=lane repo=/home/vgpnk/Projects/shokunin/tameshi-shokunin
  record path=plans/round-72.plan.md
  record rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  record blob=4a9b408164f6da483a05b4da2707be9c30a189b6
  record bytes=7372 span-bytes=25 span-offsets=[179] occurrences=1
  span head bytes=2a2a6f6e6520763120776176652c2031
  span tail bytes=2073656174732a2a
  printed=12 delimited-in-span=True occurrences-in-span=1
  counterexample-left  '**one v1 wave, 912 seats**' delimited=False
  counterexample-right '**one v1 wave, 129 seats**' delimited=False
  regex='(?<![0-9])12(?![0-9])'
  engine-reads-record-for-kind=True
  wave rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  wave dir    =.ufo/waves/round-72/w1 exists=True type=tree
  wave results=.ufo/waves/round-72/w1-results.json exists=True type=blob

ROW 4 r72-spec-roles kind=roles expect=meet
  record root=lane repo=/home/vgpnk/Projects/shokunin/tameshi-shokunin
  record path=.ufo/waves/round-72/w1-spec.json
  record rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  record blob=f5429c1811464a666a28ae16aac20391b694207f
  record bytes=18239 span-bytes=10 span-offsets=[4138] occurrences=1
  span head bytes=225437325731533031222c0a20202022
  span tail bytes=3732573153303122
  printed=12 delimited-in-span=False occurrences-in-span=0
  engine-reads-record-for-kind=False
  wave rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  wave dir    =.ufo/waves/round-72/w1 exists=True type=tree
  wave results=.ufo/waves/round-72/w1-results.json exists=True type=blob
  declaration form=spec-items path=.ufo/waves/round-72/w1-spec.json rev=a3dd35742eee608d1205843dacebc461b4242b9e exists=True type=blob
  declaration items=12 roles={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1}

ROW 5 r72-plan-roles kind=roles expect=drift
  record root=lane repo=/home/vgpnk/Projects/shokunin/tameshi-shokunin
  record path=plans/round-72.plan.md
  record rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  record blob=4a9b408164f6da483a05b4da2707be9c30a189b6
  record bytes=7372 span-bytes=134 span-offsets=[7042] occurrences=1
  span head bytes=2d205761766520607731603a20313220
  span tail bytes=206c61627261742e
  printed=12 delimited-in-span=True occurrences-in-span=1
  counterexample-left  '- Wave `w1`: 912 seats — 3 executor, 2 scribe, 1 scout, 1 connector,\n  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.' delimited=False
  counterexample-right '- Wave `w1`: 129 seats — 3 executor, 2 scribe, 1 scout, 1 connector,\n  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.' delimited=False
  regex='(?<![0-9])12(?![0-9])'
  engine-reads-record-for-kind=False
  wave rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  wave dir    =.ufo/waves/round-72/w1 exists=True type=tree
  wave results=.ufo/waves/round-72/w1-results.json exists=True type=blob
  declaration form=text-tokens path=plans/round-72.plan.md rev=a3dd35742eee608d1205843dacebc461b4242b9e exists=True type=blob
  declaration span-offsets=[7042] occurrences=1
    declared  1 connector       present=True
    declared  1 critic          present=True
    declared  3 executor        present=True
    declared  1 labrat          present=True
    declared  1 mutation-tester present=True
    declared  1 reviewer        present=True
    declared  1 scout           present=True
    declared  2 scribe          present=True
    declared  1 sentinel        present=True

ROW 6 r72-attack-share kind=attack_share expect=meet
  record root=fleet repo=/home/vgpnk/Projects/shokunin
  record path=.ufo/reports/round-72/tameshi.md
  record rev=3664a6d30051410c3d2bb8c32926d13e284a5118 type=commit
  record blob=7f8c8017af897291245d06f6045af59fdbe695a1
  record bytes=18439 span-bytes=20 span-offsets=[3618] occurrences=1
  span head bytes=31322073656174732c20313120726570
  span tail bytes=207265706f727473
  printed=12 delimited-in-span=True occurrences-in-span=1
  counterexample-left  '912 seats, 11 reports' delimited=False
  counterexample-right '129 seats, 11 reports' delimited=False
  regex='(?<![0-9])12(?![0-9])'
  engine-reads-record-for-kind=False
  wave rev=a3dd35742eee608d1205843dacebc461b4242b9e type=commit
  wave dir    =.ufo/waves/round-72/w1 exists=True type=tree
  wave results=.ufo/waves/round-72/w1-results.json exists=True type=blob
  named=['reviewer', 'critic', 'mutation-tester', 'labrat'] floor_pct=25
```

Context around each offset (same script, `raw[o-30 : o+len(span)+30]`, newlines
shown as `\n`):

```
r72-report-seats         off=3618  printed=12  delimited=True  | ...he wave** (see "Wave" below): 12 seats, 11 reports; three seats found real\n  def...
r72-report-seatreports   off=3618  printed=11  delimited=True  | ...he wave** (see "Wave" below): 12 seats, 11 reports; three seats found real\n  def...
r72-plan-seats           off=179   printed=12  delimited=True  | ...r`, clean tree). Round shape: **one v1 wave, 12 seats**\n(policy `scripts/hyaku/ufo-wa...
r72-spec-roles           off=4138  printed=12  delimited=False | ...",\n "items": [\n  {\n   "name": "T72W1S01",\n   "role": "executor",\n   "a...
r72-plan-roles           off=7042  printed=12  delimited=True  | ... controls committed pre-data\n\n- Wave `w1`: 12 seats — 3 executor, 2 scribe, 1 scout, 1 connector,\n  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.\n- Planner seat: held by the L...
r72-attack-share         off=3618  printed=12  delimited=True  | ...he wave** (see "Wave" below): 12 seats, 11 reports; three seats found real\n  def...
```

### 2.3 Independent byte-offset cross-check (`grep -aboF`)

`grep -abo` reports the byte offset; it agrees with the Python byte search.
Row 5's full span is multi-line, so its first line is matched here; the span
starts 13 bytes earlier (the `- Wave …:` prefix is 13 bytes), at 7042 = 7055 − 13, which the
Python search confirmed.

```
$ F=/home/vgpnk/Projects/shokunin; L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
$ git -C $F cat-file blob 3664a6d30051410c3d2bb8c32926d13e284a5118:.ufo/reports/round-72/tameshi.md | grep -aboF '12 seats, 11 reports'
3618:12 seats, 11 reports
$ git -C $L cat-file blob a3dd35742eee608d1205843dacebc461b4242b9e:plans/round-72.plan.md | grep -aboF '**one v1 wave, 12 seats**'
179:**one v1 wave, 12 seats**
$ git -C $L cat-file blob a3dd35742eee608d1205843dacebc461b4242b9e:.ufo/waves/round-72/w1-spec.json | grep -aboF '"T72W1S01"'
4138:"T72W1S01"
$ git -C $L cat-file blob a3dd35742eee608d1205843dacebc461b4242b9e:plans/round-72.plan.md | grep -aboF '12 seats — 3 executor, 2 scribe, 1 scout, 1 connector,'
7055:12 seats — 3 executor, 2 scribe, 1 scout, 1 connector,
```

---

## 3. The printed integer as a delimited token

### 3.1 Static counter-examples

The tool's rule is `re.search(r'(?<![0-9])%d(?![0-9])' % printed, span)`.
For each row the audit builds the two one-neighbour twins (a digit prepended /
appended to the printed token) and re-runs the rule:

| row | span token | left twin | right twin | delimited left/right |
|---|---|---|---|---|
| `r72-report-seats` | `12` | `912 seats, 11 reports` | `129 seats, 11 reports` | false / false |
| `r72-report-seatreports` | `11` | `12 seats, 911 reports` | `12 seats, 119 reports` | false / false |
| `r72-plan-seats` | `12` | `**one v1 wave, 912 seats**` | `**one v1 wave, 129 seats**` | false / false |
| `r72-spec-roles` | `12` | — (token absent: 0 occurrences) | — | **false** (no token at all) |
| `r72-plan-roles` | `12` | `912 seats — 3 executor, …` | `129 seats — 3 executor, …` | false / false |
| `r72-attack-share` | `12` | `912 seats, 11 reports` | `129 seats, 11 reports` | false / false |

Note the row-4 result: `printed=12` does **not** occur in its declared span
`"T72W1S01"`. The engine never applies the delimited rule for `kind: roles`
(see §5.1), so the standing sweep is green anyway. If the plan's binding rule
were applied uniformly to every row, `r72-spec-roles` would be setup exit 2
`printed-not-in-span`.

### 3.2 Live fixture: the span binds, but the digit twin must not

A hermetic fixture (`mktemp -d`; `git init -q`; toplevel asserted) whose record
contains **both** numbers:

```
- the wave ran 112 seats; the plan said 12 seats, 11 reports
```

with a `results.json` of `seats=12` and 12 records. Three manifests point at
the same record/rev:

| manifest | span | printed | result |
|---|---|---|---|
| control | `12 seats, 11 reports` | 12 | `WAVE_ROW … measured=meet` — exit 0 |
| digit twin | `112 seats` | 12 | setup exit 2, `printed-not-in-span:twin-row` |
| twin's own integer | `112 seats` | 112 | binds, `measured=drift` — exit 0 (`expect: drift`) |

```
fixture=/fast/scratch/hyaku/tameshi-r73/T73W1S03/tmp.7p4BKRWbhr
toplevel-ok=/fast/scratch/hyaku/tameshi-r73/T73W1S03/tmp.7p4BKRWbhr
fixture-rev=10356dd23aac1e0b9f6fc931a5161e777428554c
record-bytes=61
record-content=- the wave ran 112 seats; the plan said 12 seats, 11 reports
===== fixture-control =====
exit=0
--- stdout ---
WAVE_ROW control-row kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_RECONCILE: rows=1 met=1 unexpected=0
--- stderr ---

===== fixture-digit-twin =====
exit=2
--- stdout ---
--- stderr ---
WAVE_RECONCILE error=setup:printed-not-in-span:twin-row

===== fixture-digit-twin-own =====
exit=0
--- stdout ---
WAVE_ROW twin-own-row kind=seats expect=drift measured=drift ok | printed=112 seats=12 records=12
WAVE_RECONCILE: rows=1 met=1 unexpected=0
--- stderr ---

fixture-removed=/fast/scratch/hyaku/tameshi-r73/T73W1S03/tmp.7p4BKRWbhr
```

The construction, self-contained (every git call names `-C "$D"`; the first
commit is guarded by the toplevel assertion):

```sh
D=$(mktemp -d); git -C "$D" init -q
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || exit 9
printf '%s\n' '- the wave ran 112 seats; the plan said 12 seats, 11 reports' > "$D/report.md"
python3 - "$D/results.json" <<'PY'
import json, sys
json.dump({'seats': 12,
           'results': [{'name': 'S%02d' % i, 'agent': 'executor'}
                       for i in range(1, 13)]}, open(sys.argv[1], 'w'))
PY
git -C "$D" add report.md results.json
git -C "$D" -c user.name=seat -c user.email=seat@example.invalid commit -q -m fixture
REV=$(git -C "$D" rev-parse HEAD)
```

Each row manifest is `{"rows":[{"id":…,"kind":"seats","expect":…,
"record":{"path":"report.md","rev":"$REV","root":"lane","span":…,
"printed":…},"wave":{"results":"results.json","rev":"$REV"}}]}`; the tool is
run `--repo "$D" --manifest <mutant>`.

---

## 4. Three mandated span mutations

### 4.1 Construction

The original manifest is edited **at the byte level** (not re-serialised), so
the mutant differs from the standing manifest only in the named span. The
builder below is condensed (the splice assertion, the JSON re-parse and the
three mutations are exactly as run):

```python
ORIG = '/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/wave-reconcile.json'
orig = open(ORIG, 'rb').read()
REPORT_SPAN = b'"12 seats, 11 reports"'         # 3 occurrences: rows 1, 2, 6
PLAN_SPAN   = b'"**one v1 wave, 12 seats**"'    # 1 occurrence: row 3

def nth(hay, needle, n):                        # start offset of occurrence n (1-based)
    start = 0; found = -1
    for _ in range(n):
        found = hay.find(needle, start)
        start = found + 1
    return found

def build(name, pos, old, new):
    assert orig[pos:pos + len(old)] == old
    open(name, 'wb').write(orig[:pos] + new + orig[pos + len(old):])
    json.loads(open(name, 'rb').read().decode('utf-8'))     # still parses

build('mutant-1-byte-span.json',        nth(orig, REPORT_SPAN, 1), REPORT_SPAN, b'"12 seats, 11 reportz"')
build('mutant-2-digit-twin-span.json',  orig.find(PLAN_SPAN),      PLAN_SPAN,   b'"**one v1 wave, 112 seats**"')
build('mutant-3-foreign-span.json',     nth(orig, REPORT_SPAN, 2), REPORT_SPAN, PLAN_SPAN)
```

Verified construction facts:

```
mutant-1-byte-span.json        offset=1295 old=b'"12 seats, 11 reports"' new=b'"12 seats, 11 reportz"' lenediff=+0 differing-bytes=1
mutant-2-digit-twin-span.json  offset=2178 old=b'"**one v1 wave, 12 seats**"' new=b'"**one v1 wave, 112 seats**"' lenediff=+1 spliced-ok=True
mutant-3-foreign-span.json     offset=1750 old=b'"12 seats, 11 reports"' new=b'"**one v1 wave, 12 seats**"' lenediff=+5 spliced-ok=True
```

```
$ cmp -l tools/wave-reconcile.json mutant-1-byte-span.json
1316 163 172
```

`cmp` position 1316 (1-based) = 0-based 1315 = span start 1295 + 20; the two
octal bytes are `s` → `z`. **Exactly one byte differs.** The unified diffs:

```
--- mutant-1-byte-span ---
-    "span": "12 seats, 11 reports",
+    "span": "12 seats, 11 reportz",
--- mutant-2-digit-twin-span ---
-    "span": "**one v1 wave, 12 seats**",
+    "span": "**one v1 wave, 112 seats**",
--- mutant-3-foreign-span ---
-    "span": "12 seats, 11 reports",
+    "span": "**one v1 wave, 12 seats**",
```

(Mutant 2 changes row 3's span; mutant 3 replaces row 2's span with row 3's
span — i.e. a span taken from another document.)

### 4.2 Results — all three are setup exit 2 with a naming line

```
$ python3 -I -X utf8 tools/wave-reconcile.py --repo <lane> \
      --extra-root fleet=/home/vgpnk/Projects/shokunin \
      --manifest <scratch>/mutant-N.json
```

| mutation | changed row | exit | naming line |
|---|---|---|---|
| 1 — one byte (`reports`→`reportz`) | `r72-report-seats` | **2** | `WAVE_RECONCILE error=setup:span-not-in-record:r72-report-seats:.ufo/reports/round-72/tameshi.md` |
| 2 — digit-added twin (`12`→`112`) | `r72-plan-seats` | **2** | `WAVE_RECONCILE error=setup:span-not-in-record:r72-plan-seats:plans/round-72.plan.md` |
| 3 — span from another document | `r72-report-seatreports` | **2** | `WAVE_RECONCILE error=setup:span-not-in-record:r72-report-seatreports:.ufo/reports/round-72/tameshi.md` |

Raw runs:

```
===== mutant-1-byte-span =====
exit=2
--- stdout ---
--- stderr ---
WAVE_RECONCILE error=setup:span-not-in-record:r72-report-seats:.ufo/reports/round-72/tameshi.md

===== mutant-2-digit-twin-span =====
exit=2
--- stdout ---
--- stderr ---
WAVE_RECONCILE error=setup:span-not-in-record:r72-plan-seats:plans/round-72.plan.md

===== mutant-3-foreign-span =====
exit=2
--- stdout ---
--- stderr ---
WAVE_RECONCILE error=setup:span-not-in-record:r72-report-seatreports:.ufo/reports/round-72/tameshi.md
```

No mutation produced a `WAVE_ROW`/`WAVE_RECONCILE` sweep line; stdout is empty
in all three cases. The errors are raised before any row is reported.

---

## 5. Additional scoped probes (not one of the three)

### 5.1 The `record` block is inert on `roles` and `attack_share`

`measure()` calls `_record_span()` only for `kind` `seats` and `seat_reports`
(`roles` reads `declaration`, `attack_share` reads `results` + inline
`named`/`floor_pct`). Forging `record.span` on those rows is therefore a
**silent pass**:

```
=== probe 4: attack_share record span forged ===
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-report-seatreports kind=seat_reports expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | declared={…} measured={…}
WAVE_ROW r72-plan-roles kind=roles expect=drift measured=drift ok | declared={…} measured={…}
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | attack=3/12=25.0% floor=25.0%
WAVE_RECONCILE: rows=6 met=6 unexpected=0
exit=0
=== probe 5: roles(spec-items) record span forged ===
(same six WAVE_ROW lines, byte-identical to the probe-4 run)
WAVE_RECONCILE: rows=6 met=6 unexpected=0
exit=0
```

The two `roles` detail strings are elided with `…` above (they are identical
to the §1 run: `declared={…labrat…}` for row 5, matching multisets for row 4);
the `rows=6 met=6 unexpected=0` line and the exit code are verbatim.

- **Probe 4** set `rows[5].record.span = "span-forged-at-row-6"` (no such text
  anywhere); **probe 5** set `rows[3].record.span = "span-forged-at-row-4"`.
- Both mutants are valid JSON and the sweep is unchanged. So of the six record
  blocks, **three are inert** (rows 4 and 6 entirely; row 5's record block is
  inert too but duplicates its `declaration.span`, which *is* byte-checked).
  The three rows whose claim is a record *span* (1, 2, 3) are the only ones the
  span-binding rule actually protects.
- This does not move the frozen counter: each row's actual claim is still
  bound through its kind-appropriate path (results blob for 1/2/3/6;
  declaration blob for 4/5). It does mean a future manifest row of kind
  `roles`/`attack_share` could carry a forged `record` block silently.

### 5.2 Missing `--extra-root fleet` is an uncaught `KeyError`, not setup exit 2

`_artifact()` guards an unknown root (`unknown-root:` → setup exit 2), but
`_record_span()` does `readers[rec.get('root', 'lane')]` with no membership
check. Rows 1/2/6 name `root: fleet`, so dropping the flag crashes:

```
$ python3 -I -X utf8 tools/wave-reconcile.py --repo <lane> \
      --manifest <lane>/tools/wave-reconcile.json
Traceback (most recent call last):
  File ".../tools/wave-reconcile.py", line 485, in <module>
    sys.exit(main())
  ...
  File ".../tools/wave-reconcile.py", line 152, in _record_span
    reader = readers[rec.get('root', 'lane')]
KeyError: 'fleet'
exit=1
```

The frozen counter always passes the flag, so the counter is unaffected; the
asymmetry is that a setup fault on the record path exits 1 with a traceback
instead of exit 2 with `WAVE_RECONCILE error=setup:…`. The same unguarded
lookup exists for `declaration.root`, but both declarations name `lane`, so it
is not reachable in the standing manifest.

---

## 6. Population table for the round-72 report's `12 seats, 11 reports`

The span is at offset 3618 in `.ufo/reports/round-72/tameshi.md` at
`3664a6d3…`, line 56:

```
$ git -C /home/vgpnk/Projects/shokunin cat-file blob 3664a6d3…:.ufo/reports/round-72/tameshi.md | nl -ba | sed -n '56p'
    56  - **The wave** (see "Wave" below): 12 seats, 11 reports; three seats found real
```

### 6.1 Counts at the row's artifact revision (`a3dd3574…`, lane)

Variables used below:
`L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
`F=/home/vgpnk/Projects/shokunin`,
`R=a3dd35742eee608d1205843dacebc461b4242b9e`.

| # | population | counting command | count |
|---|---|---|---|
| P1 | all files, recursive | `git -C $L ls-tree -r --name-only $R -- .ufo/waves/round-72/w1 \| wc -l` | **26** |
| P2 | `*.md` at top level of `w1` | `git -C $L ls-tree --name-only $R -- .ufo/waves/round-72/w1/ \| grep -c '\.md$'` | **12** |
| P3 | `*.md` at any depth | `git -C $L ls-tree -r --name-only $R -- .ufo/waves/round-72/w1 \| grep -c '\.md$'` | **17** |
| P4 | directories strictly under `w1` | `git -C $L ls-tree -r -d --name-only $R -- .ufo/waves/round-72/w1 \| grep -c '^\.ufo/waves/round-72/w1/'` | **9** |
| P4b | top-level directories of `w1` | same but `awk '$2=="tree"'` | **7** |
| P5 | records in `w1-results.json` | `… \| python3 -c "import json,sys;print(len(json.load(sys.stdin)['results']))"` | **12** |
| P5b | `seats` field in `w1-results.json` | same, `print(d['seats'])` | **12** |
| P6 | spec items (`w1-spec.json`) | `…print(len(d['items']))` | **12** |
| P7 | distinct `agent` values | `…print(len({r['agent'] for r in d['results']}))` | **9** |
| P8 | top-level blobs of `w1` | `git -C $L ls-tree $R -- …/w1/ \| awk '$2=="blob"' \| wc -l` | **13** |
| P9 | top-level entries of `w1` | `git -C $L ls-tree --name-only $R -- …/w1/ \| wc -l` | **20** |
| P10 | `S01..S11` name truncation | `…/w1/ \| grep -Ec '/T72W1S(0[1-9]\|1[01])\.md$'` | **11** |
| P11 | fleet `.ufo/reports/round-72/*.md` | `git -C $F ls-tree --name-only 3664a6d3 -- .ufo/reports/round-72/ \| grep -c '\.md$'` | **10** |
| P12 | lane `.ufo/reports/round-72` | `git -C $L ls-tree -r --name-only 3664a6d3 -- .ufo/reports/round-72` | **0** |
| P13 | `swarm-registry.json` members | `… \| python3 -c "import json,sys;print(len(json.load(sys.stdin)['members']))"` | **12** |

Raw block:

```
=== worktree populations (read-only) ===
worktree top-level *.md (ls):      12
worktree top-level *.md (find):    12
worktree *.md any depth (find):    17
worktree top-level dirs:           7
worktree all files:                26
=== git populations at a3dd3574 ===
P1 all files (ls-tree -r):         26
P2 *.md top level (ls-tree dir):   12
P3 *.md any depth:                 17
P4 dirs strictly under w1:         9
P4b top-level dirs of w1:          7
P5 results records:                12
P5b results seats field:           12
P6 spec items:                     12
P7 distinct agents:                9
P8 top-level blobs:                13
P9 top-level entries:              20
P10 S01..S11 name selection:       11
P11 fleet round-72 report *.md:    10
```

### 6.2 History: no committed state ever had 11 seat reports

Lane command:

```sh
for r in dfb534ca 292ceec0 56866fa3 a3dd3574 17cd1939; do
  md=$(git -C $L ls-tree --name-only $r -- .ufo/waves/round-72/w1/ 2>/dev/null | grep -c '\.md$' || true)
  rec=$(git -C $L cat-file blob $r:.ufo/waves/round-72/w1-results.json 2>/dev/null \
        | python3 -I -X utf8 -c "import json,sys;print(len(json.load(sys.stdin)['results']))" \
        2>/dev/null || echo NA)
  echo "$r md=$md records=$rec"
done
```

Output (`dfb534ca` is the freeze commit: only `swarm-registry.json` exists;
`292ceec0` is the wave-evidence commit; `56866fa3` is wave settlement):

```
dfb534ca md=0 records=NA
292ceec0 md=12 records=NA
56866fa3 md=12 records=12
a3dd3574 md=12 records=12
17cd1939 md=12 records=12
```

Fleet command and output (newest first; the report directory also never
reaches 11 — `3664a6d3` takes it from 9 to 10):

```sh
for c in $(git -C $F log --format=%h -- .ufo/reports/round-72); do
  n=$(git -C $F ls-tree --name-only $c -- .ufo/reports/round-72/ 2>/dev/null | grep -c '\.md$' || true)
  echo "$c md=$n $(git -C $F log -1 --format=%s $c | cut -c1-60)"
done
```

```
3664a6d3 md=10 round-72: tameshi report
2613d99b md=9 round-72: kake report
f0bc1298 md=8 round-72: chousa report (hyaku zcode run 14)
f5f9cb4b md=7 round-72: kumitate report (hyaku zcode run 14)
a0eaa890 md=6 round-72: mori report (hyaku zcode run 14)
5fe6541a md=5 round-72: revenger report
4777eca6 md=4 round-72: kotoba report
80d8c9b5 md=3 round-72: kotodama report erratum 5 (SimplifierRows cuts lan
a62f700e md=3 round-72: kotodama report erratum 4 (register-map verificati
e7cdde73 md=3 round-72: kotodama report erratum 3 (CDX canonical sweep fin
6efd7f4e md=3 round-72: kotodama report erratum 2 hash correction
da70b66f md=3 round-72: kotodama report erratum 2 (controls/draft hygiene)
406c4e9e md=3 round-72: kotodama report erratum (post-landing routings)
a151ec38 md=3 round-72: kotodama report
f47ad6ba md=2 repair: restore fleet tree deleted by stray commit 35b91714 
35b91714 md=0 t
c1b7a4fb md=2 w14 closeout: r75/r74/r83 all ADMIT-corr; fleet reports file
ef633e2e md=1 fleet: wave shokunin-train-20261013-w3 adjudication — audi
```

Also, `swarm-registry.json` at the artifact revision has 12 members:

```
members type dict len 12
names ['T72W1S01', 'T72W1S02', 'T72W1S03', 'T72W1S04', 'T72W1S05', 'T72W1S06',
       'T72W1S07', 'T72W1S08', 'T72W1S09', 'T72W1S10', 'T72W1S11', 'T72W1S12']
```

### 6.3 Plain answer

**`11` matches no defensible population of the committed wave artifacts.**
Every natural population yields 0, 7, 9, 10, 12, 13, 17, 20 or 26. Both
seat-report populations (`*.md` at top level; `results[]`) yield **12**, and
the committed history contains **no revision** with 11 seat reports — the
12 reports were committed atomically at `292ceec0`. The only way to obtain 11
is to drop exactly one committed report, e.g. the `S01..S11` name truncation
that excludes `T72W1S12.md` (which exists at the rev, has a `results[]`
record, and is listed in the report's own 12-row wave table). That is a
counting error, not a population — exactly the drift the `seat_reports` red arm
measures (`printed=11 files=12`, `expect=drift measured=drift`).

---

## 7. Honest negatives

- I did **not** edit any tracked file, and ran no git/jj mutation. `git status`
  was read only.
- I did **not** spawn any subagent (the single permitted labrat was not
  needed).
- I did **not** install or upgrade any tool or package.
- The three mutations were run against a scratch copy of the manifest; the
  standing manifest's bytes were only read.
- The frozen sweep and selftest were run literally from the lane root
  (`--repo .`), and additionally with absolute paths for the per-row work; the
  outputs agree.
- The live digit-twin is a fixture, not the standing manifest: the standing
  Record documents contain no `112 seats` twin, so the twin had to be
  constructed. The static per-row counter-examples (§3.1) are pure-function
  applications of the tool's own regex to the real spans.

## 8. Files written and cleanup

- `.ufo/waves/round-73/w1/T73W1S03/binding-audit.md` (this file).
- `.ufo/waves/round-73/w1/T73W1S03.md` (seat report; same findings).
- Scratch `/fast/scratch/hyaku/tameshi-r73/T73W1S03/` (scripts, mutants,
  fixture) — deleted before yield; the fixture repo was removed inside its
  script, and its `$D` was never outside the scratch tree.
