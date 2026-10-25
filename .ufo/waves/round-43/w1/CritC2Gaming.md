# CritC2Gaming — are m12 and m13 reachable by a do-nothing edit?

Scope: the two new calibration classes of round-43 C2, attacked as games. No lane file, fleet
file, frozen contract or frozen counter was written. Probes call the counter's own predicates
and drive its unmodified `main()` with record bytes swapped in memory; `--rev`/`--freeze` were
the freeze revision only. These are control-mode falsification probes, **not** measurements at
a revision.

Instrument under attack is the **frozen** blob,
`17f6ef0c:.ufo/evidence/round-43/calibration/measure.py`,
sha256 `092c76cd6e10f9280af21237ec90dc14e63f0bdb9ae74fffb9da841730a8f286` = the contract pin.
The lane's working-tree copy of that file was mutated by another seat during this wave; §4
treats that separately.

## Verdict

**Yes — both targets together fall to 21 bytes of inserted text, with no repair, and the frozen
counter prints `C2_R43_PASS=true`, `self_pin=1`, `classes=7`, `total=0` on those bytes.** In
that state no claim is planned, no round-43 SCORECARD block exists, the newest standing
sources-registry row still carries the column-zero counting command, and that row was not
re-derived this round. A green C2_R43 is therefore not evidence of the record repair the claim
names.

The in-progress working-tree patch (§4) raises the cheapest floor and closes the two token
games, but leaves three independent passes standing: an empty planned field, a fenced *quoted*
standing row (which also re-anchors m6), and a column-zero command that merely mentions `0,3`
in a shell comment.

---

## 1. The counterexample

### A — plausible-looking: 31 bytes, 2 lines touched

```diff
@@ newest standing row, SCORECARD.md:2020 (@ freeze) @@
-… ; `corpus/SOURCES.md` | fleet round 1 (kaika) |
+… ; `corpus/SOURCES.md` | fleet round 1  (0,3)(kaika) |
@@ end of file, inside the round-42 block @@
 recorded in the lesson and the knowledge entry, outside the frozen claim.
+
+**Planned (round 43):**
```

### B — absolute floor: 21 bytes, 1 line touched

```diff
-… | fleet round 1 (kaika) |
+… | fleet round 1 0,3(kaika) |
@@ end of file
+Planned (round 43)      ← no newline, no bold, no colon, no claim, no round-43 block
```

### Receipts (`main()` of the frozen blob, `--rev`/`--freeze 17f6ef0c…`)

```
A_eyebrow_plus_suffix exit=0
  C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=3
          sources_rows=113 standing=113 receipts=17 revisions=3
          m13_probe=standing=6_column0=112_valid=113 … C2_R43_PASS=true
B_bare_substring_floor exit=0
  C2_R43: self_pin=1 classes=7 … m12=0 m13=0 total=0 … C2_R43_PASS=true
bytes appended: A=31 B=21
```

Baseline, same revision, unmodified bytes:

```
C2_R43: … m12=1 m13=1 total=2 … C2_R43_PASS=false first=m12:Planned_(round_43)   (exit 1)
```

### What is not repaired

| Item the C2 statement names | State after the 21-byte edit |
|---|---|
| "declares the next round's planned claims" (1–3 claims, each with an axis/capability, `AXES.md:81` fleet) | one bare substring; **0 claims**, no axis, no capability |
| "the newest SCORECARD round block" | still `## Round 42`; **no round-43 block exists** |
| "newest standing … counting command is census-valid" | command byte-identical: `grep -cE '^\| S[0-9]{3} \|'` |
| the row's count still matching the registry | `113 rows at round 42`: equals the census (113) only because nothing was re-derived; the round label is stale and unchecked |
| "load-bearing on an indented mirror" | executed: registry **113** = census 113; mirror **112** ≠ census 113 |

The edit is 18 characters of `Planned (round 43)` plus 3 characters `0,3`. No claim, no
measurement, no round record, no command fix.

---

## 2. Why the frozen counter cannot see it

### m12 — a substring from the last `## Round` heading to EOF

```python
# frozen measure.py:110-117
def newest_round_block(scorcard_text):
    matches = list(re.finditer(r'^## Round (\d+)\b.*$', scorcard_text, re.M))
    ...
    return int(last.group(1)), scorcard_text[last.start():]

# frozen measure.py:118-123
def m12_planned(block_text, round_no):
    wanted = 'Planned (round %d)' % (round_no + 1)
    hits = [] if wanted in block_text else [wanted]
```

Observed on the frozen blob:

| probe | m12 |
|---|---|
| `**Planned (round 43):**` with nothing after it (A) | 0 |
| `<!-- Planned (round 43) -->` | 0 |
| fenced quote ```` ```\n**Planned (round 43):** nothing\n``` ```` | 0 |
| the line in the **round-42** block (no round-43 block at all) | 0 |
| bare `Planned (round 43)`, no bold/colon/newline (B) | 0 |
| `## Round 44 — skip` + `**Planned (round 45):** tbd` | 0 — newest round 42→**44**; round 43 never recorded |

The docstring (`frozen:9-13`) and the contract text say "declares the next round's planned
claims"; the predicate tests a substring of a file suffix. Because `round_no` is read off the
heading the lane itself writes, a lane can also launder its round index.

Record-selection side effect: `main()` slices LOG at the newest round number
(`frozen:365-369`, `cut = log_text.find('round %d' % round_no)`; absent marker ⇒ `''`).
Appending `## Round 43` printed `revisions=0` with `records=3`: the m11 evidence set shrank
because the lane chose a heading with no LOG marker. A record can be **erased** rather than
repaired, and `records=N` is not a count of records that exist.

### m13 — substring anywhere in the row, plus a row-independent probe

```python
# frozen measure.py:158-172
def m13_standing_command(scorcard_text, registry_text):
    standing = standing_registry_rows(scorcard_text)   # line.startswith('| sources-registry |')
    newest = standing[-1]
    if '0,3' not in newest and '0-3space' not in newest:
        hits.append('standing command is column-zero only')
    mirror = indent_mirror(registry_text)
    column0, valid = count_patterns(mirror)            # frozen:140-146, two fixed regexes
    if not (valid == column0 + 1):
        hits.append('indent probe not load-bearing …')
```

* Clause (a) is a 3-character substring test over the whole table row. A and B pass with the
  command untouched; the token lands in a `fleet round 1 0,3(kaika)` cell that is visibly not
  a command and is not syntax-checked.
* Clause (b) never touches the row. `count_patterns` is two hardcoded regexes, so `valid ==
  column0 + 1` is equivalent to "the registry contains no 1–3-space-indented row" — a property
  of the fixture, satisfied for **any** row text on today's all-column-zero registry.
* It inverts when the hazard it claims to test materialises. With one census-admitted row
  already indented two spaces (census 113 on both texts), the **correct** census-valid row:

  ```
  all-column-zero registry : ([],  'standing=1 column0=112 valid=113')
  mixed registry           : (['indent probe not load-bearing (column0=111 valid=113)'], '…')
  ```

  A true statement scores `m13=1` exactly when indentation enters the registry.

### m6 — the count is compared but never re-derived, and its round discarded

```python
# frozen:133-137
def row_count_claim(cell):
    match = re.search(r'(\d+)\s+rows at round\s+(\d+)', cell)
# frozen:375-378
stated, stated_round = row_count_claim(standing[-1]) if standing else (None, None)
m6 = [] if stated == valid_count else ['standing=%s actual=%d' % (stated, valid_count)]
```

`stated_round` is bound and never used; `stated` is compared against a literal-regex count and
the row's command is never executed. Observed: `113 rows at round 3` → `m6=0`;
`112 rows at round 43` → `m6=1`. B keeps the old `113 rows at round 42` and is green while the
derivation the row promises was never run.

### Fences are not distinguished from records

`standing_registry_rows` (`frozen:125-130`) is a `startswith` scan with no fence awareness, so
an appended **quoted** row inside a code fence becomes the newest standing row for m13 *and*
m6:

```
freeze                                        m13=1  m6=0  standing=6  stated=113@r42
+ ```\n| sources-registry | quoted | `grep -cE '^ {0,3}\| S[0-9]{3} \|' …` → 113 rows at round 43 |\n```
                                              m13=0  m6=0  standing=7  stated=113@r43
the real row SCORECARD.md:2020 is byte-unchanged and still column-zero
```

A quotation re-anchors the standing claim without editing it — the exact hazard m10's class
text names ("a receipt named in another receipt's supersedes is history"), not honoured here.

### `classes=7` cannot fail

`frozen:409` `declared = 7` is a constant printed as `classes=%d`; the pass term is
`declared == 7` (`frozen:427`). It does not count classes that ran. (Independently,
`RevC2DoNothing.md` ran the decisive variant: a counter with hardcoded `m12=[] m13=[]` still
prints `classes=7 … C2_R43_PASS=true`.)

---

## 3. Secondary counterexamples, all measured on the frozen instrument

| # | probe (no repair of the claim) | verdict |
|---|---|---|
| F | fenced **quoted** standing row with a census-valid command (+ A's eyebrow) | `m12=0 m13=0 m6=0`, `stated=113@r43`; real row untouched |
| C | fenced quoted row whose grep is **column-zero** but carries a `# 0,3` shell comment | `m12=0 m13=0 m6=0` |
| D | `## Round 44` + `**Planned (round 45):** tbd` | `m12=0`; round 43 skipped entirely |
| E | `113 rows at round 3`, census-valid pattern | `m6=0` (round label unchecked) |
| G | mixed registry, **correct** census-valid row | `m13=1` `indent probe not load-bearing (column0=111 valid=113)` |

---

## 4. The pinned counter was mutated mid-wave (operational finding)

```
$ sha256sum .ufo/evidence/round-43/calibration/measure.py
52961c3709a39ef76f5a1c7de94080a384244703ea1b8ab9fcd6217c23666fdf   (working tree, mtime 2026-10-25 07:56:54 -0300)
$ git show 17f6ef0c…:.ufo/evidence/round-43/calibration/measure.py | sha256sum
092c76cd6e10f9280af21237ec90dc14e63f0bdb9ae74fffb9da841730a8f286   (= contract pin)
$ git status --porcelain -- .ufo/evidence/round-43/calibration/measure.py
 M .ufo/evidence/round-43/calibration/measure.py        (53 insertions, 22 deletions)
```

`self_pin` (`frozen:346-353`) requires the *running* file and the freeze blob to both equal the
pinned sha. Any commit of the working-tree edit makes `self_pin=0` → `C2_R43_PASS=false`
against the declared freeze; making it pass again would require re-freezing the contract with a
new counter sha *after* wave-1 data was seen, which `amendments_note` ("claims.*, the
predicates, counters … byte-unchanged") and the freeze-before-any-seat rule forbid. **The edit
therefore belongs to the round-44 counter, not to round 43.**

What the edit changes, and what it leaves standing (predicates run against the same probe
texts):

| probe | frozen (pin) | in-progress patch |
|---|---|---|
| A: bold eyebrow + `(0,3)` in the trailing cell | `m12=0 m13=0` **PASS** | `m12=0` **`m13=1`** — token game closed |
| B: bare substring + `0,3` in the trailing cell | `m12=0 m13=0` **PASS** | `m12=1 m13=1` — closed |
| F: fenced quoted row, census-valid command | `m12=0 m13=0 m6=0` **PASS** | `m12=0 m13=0 m6=0` **still PASS** |
| C: fenced quoted row, column-zero command + `# 0,3` comment | `m12=0 m13=0` **PASS** | `m12=0 m13=0` **still PASS** |
| D: round laundering to 44 | `m12=0` **PASS** | `m12=0` **still PASS** |

Residual defects in the patch, by its own line numbers:

* **m12 remains a substring.** `wanted = '**Planned (round %d):**'` tested with `in
  block_text` (patch:131): an empty field passes, and it passes inside a fence or an HTML
  comment, in the previous block, and after a laundered `## Round 44` heading.
* **m13 remains a substring inside the command cell.** `elif not any('0,3' in span …)`
  (patch:182): `grep -cE '^\| S[0-9]{3} \|' … # 0,3` satisfies it with a column-zero pattern
  (probe C). No extraction, no execution, no quantifier check.
* **Fence blindness unchanged** (`standing_registry_rows` untouched): probe F is still a pass
  and still re-anchors m6.
* **The mirror probe is unchanged**: still `count_patterns` over fixed regexes, so the
  mixed-registry false red (probe G) stands.
* **m6 is unchanged**: count still not re-derived, `stated_round` still discarded.
* **m11 is widened.** `git cat-file -e token` without `^{commit}` (patch:290) admits any
  object. Verified at freeze: blob `cd827448d43f9125b705dfb5aeb5808c112b7cb5`
  (`git rev-parse 17f6ef0c:SCORECARD.md`) resolves plain and does **not** peel as a commit, so
  a cited blob id would now count as a reachable "revision".

---

## 5. What the counter should require (smallest safe correction)

Two predicates plus one adjacent field; no new file, no new dependency.

**m12** — (1) search only outside fenced blocks and `<!-- -->`; (2) require the newest block
number to equal `contract['round']`, which kills round laundering *and* requires the current
round to have a block; (3) require exactly one **line-start** `**Planned (round N+1):**`;
(4) require the remainder to name a claim — a `C<n>` token, an axis word from the contract, or
a backticked token that resolves at REV — and at least four words.

**m13** — (1) same fence/comment stripping before collecting standing rows; (2) extract the
`-cE '<pattern>'` from the row's backticked grep (no pattern ⇒ hit); (3) require that pattern to
carry `^ ?{0,3}`; (4) **execute** the compiled pattern against the registry *and* against
`indent_mirror(registry)` and require both counts to equal the census count. This replaces the
fixed-regex probe with the row's own command, so it is load-bearing for the declared command
and stays green on a mixed registry.

**m6** — require `stated == census(registry)` **and** `stated_round == newest round number`.
Composed with m13 (declared command == census on both texts) the stated count is then anchored
to the row's own command.

Validation (`proposed.py`, strict m6+m12+m13 over four texts):

| text | m6 | m12 | m13 | total | outcome |
|---|---|---|---|---|---|
| freeze bytes | 0 | 2 | 2 | 4 | **FAIL** |
| gamed A, 31 bytes | 0 | 2 | 2 | 4 | **FAIL** (`planned line names no claim ('')`) |
| gamed B, 21-byte floor | 0 | 2 | 2 | 4 | **FAIL** (field absent) |
| genuine repair (round-43 block naming an axis + a capability; row pattern `^ {0,3}\| S[0-9]{3} \|` → 113 rows at round 43) | 0 | 0 | 0 | 0 | **PASS** |
| genuine repair, mixed registry (one row pre-indented 2 spaces, census 113) | 0 | 0 | 0 | 0 | **PASS**, no false red |

Every secondary probe is caught by the same predicate: fenced standing row (2), `0,3` in a
description cell (2), `0,3` suffix (2), fenced planned quote (2), comment planned line (2),
round laundering to 44 (2), stale count 112 (1), stale round label `round 3` (1).

Minimality: the honest repair and the cheapest game differ only in that the honest one puts a
real claim after the field and changes the row's pattern to `^ {0,3}` — the correction demands
exactly those two things and nothing else.

---

## 6. Impacted axes and freeze consequence

* **calibration** (the axis C2 carries) — the two classes are the whole evidence for the
  round-43 calibration move, and both are token tests. **depth** and **operability** are not
  affected.
* The correction **cannot** be applied to round 43's counter: it is sha-pinned in
  `claims.C2.counter_sha256`, `self_pin` compares both copies, and `amendments_note` fixes the
  predicates byte-unchanged. §4 shows the concrete failure mode already present in the working
  tree.
* Smallest safe action for this round: (a) disclose in the round-43 lesson and in the SCORECARD
  instrument-limits paragraph that m12 is a substring test and m13's probe is row-independent —
  the form the round-42 block already uses for m10's content-blindness; (b) freeze the
  four-part predicate above in the **round-44** counter before that round's first run; (c) do
  not describe `m12=0 m13=0` in round 43 as "the block declares planned claims" or "the
  command is census-valid" — the predicates establish neither.
* For the canonical judge: this is a **fixable defect in the instrument**, not a tradeoff. The
  target is reachable honestly (validated above), so the C2 *move* is admissible; the C2
  *measurement* at the current counter sha is insufficient evidence by itself.

---

## 7. Evidence and reproduction

Counter at the freeze revision (permitted):

```
python3 .ufo/evidence/round-43/calibration/measure.py --lane … --rev 17f6ef0c… --freeze 17f6ef0c…
→ C2_R43: self_pin=1 classes=7 … m12=1 m13=1 total=2 … C2_R43_PASS=false first=m12:Planned_(round_43)
```

Artifacts (item-mandated scratch dir; retained because the item asks for the cheapest edit to
be written there):

```
/tmp/tameshi-r43-CritC2Gaming-W42B/
  cheapest-edit.md              the 31-byte and 21-byte edits
  cheapest-SCORECARD.md         doctored A bytes (PASS=true under the frozen main())
  cheapest-floor-SCORECARD.md   doctored B bytes (21 bytes, PASS=true)
  cheapest.diff  cheapest-floor.diff        A/B against the freeze blob
  receipts-frozen.txt           self_pin=1 receipts for A and B
  against-frozen.txt  against-inprogress.txt  §4 comparison
  frozen-measure.py             freeze blob (sha 092c76cd…)
  game.py  game2.py  run_against.py  proposed.py  cheapest.py
  SCORECARD.md  SOURCES.md       freeze blobs (git show)
```

Frozen counter line numbers: `newest_round_block` 110-117, `m12_planned` 118-123,
`standing_registry_rows` 125-130, `row_count_claim` 133-137, `count_patterns` 140-146,
`indent_mirror` 148-156, `m13_standing_command` 158-172, LOG slice 365-369, m6 375-378,
m12/m13 wiring 403-406, `declared = 7` 409, pass term 427.
In-progress working-tree patch line numbers: `m12_planned` 124-131, m13 clauses 169-183,
m11 `cat-file` 290.

Not written anywhere: the frozen contract, either counter, the registry, the SCORECARD, the
LOG, any git/jj state, the fleet repo, or `shokuknow`.

Tooling: nothing installed or upgraded (no pacman, uv, cargo or npm invocation).
