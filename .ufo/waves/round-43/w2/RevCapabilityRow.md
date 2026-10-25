# RevCapabilityRow — does the round-43 capability row resolve?

wave 2 (falsify) · reviewer seat · lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
Target: `SCORECARD.md:2074` (the `staged-id adoption guard` capability row added by round 43),
with its two adjacent cells `SCORECARD.md:2061` (C3 claim row) and `SCORECARD.md:2053` (the
round-43 section header that names the freeze).
Revisions used: base `487b8f0da89fa0e2b8bea6930068accbf36e70a9`, freeze of record
`3aee2c078f8976499b587086af3577fc94dc8cf1`, records `c5335c70bff750218b3a6db0a92daae76509a0de`.
No counter was run at the records commit. `SCORECARD.md` is byte-unchanged from `c5335c7`
through HEAD (`git diff --stat c5335c70bbf..HEAD -- SCORECARD.md` → empty), so the row read
here is the committed record. While this review ran, HEAD moved `e20cf89` → `bb36f80` (A12)
→ `f551ca6` (A13) → `e25cd2f`; the guard tool pin stayed `2e8f2e89…` and the C3 counter pin
moved again at A12 to `47a6afce…` (a new `held_refused` probe). Everything below is measured
against `3aee2c0`, where the pins verified are the ones in force; the row's staleness is
therefore one pin deep on the tool and one-to-three on the counter — not an artifact of a
moving checkout.

## Row text under test (`SCORECARD.md:2074`)

> | staged-id adoption guard | … | deciding receipt `C3_R43: … C3_R43_PASS=true` at the
> round-43 measured commit, counter `.ufo/evidence/round-43/guard/measure.py`, tool
> `tools/staged-id-guard.py` @ `8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762` | round 43 |

and its counting command (`SCORECARD.md:2061`):

> `python3 .ufo/evidence/round-43/guard/measure.py --lane LANE --rev REV --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef`

## Three-way verdict

| Part | Verdict |
|---|---|
| `tool` sha256 matches the committed guard at the freeze | **DOES NOT RESOLVE** at the freeze of record (`2e8f2e89…`); the row's `8140945a…` is the committed blob only at the superseded freeze `17f6ef0c`, i.e. the pre-A4 blob its own amendment records as failing the predicate |
| named counter path exists | **RESOLVES** — `.ufo/evidence/round-43/guard/measure.py` is committed at the freeze with the pinned bytes `ae66342d…` (= `claims.C3.counter_sha256`); but the row's printed `--freeze` does not (F4) |
| named receipt line appears in a committed stdout | **DOES NOT RESOLVE** — no committed stdout anywhere at HEAD carries a passing C3 line for the round-43 measured state; the row's own `after/` pointer is an empty directory at every commit and the "after subsection" it cites does not exist for round 43 |

---

## F1 (high) — the row pins the pre-A4 blob, not the guard at the freeze of record

The row asserts `tools/staged-id-guard.py` @ `8140945a…`. Hash of the committed guard per rev
(run from the lane root):

```
$ for r in 697d2f1 f0f2636 17f6ef0 5cd2154 114ffacd 273c047 3aee2c07 c5335c70; do
    printf "%s " $r; git show $r:tools/staged-id-guard.py | sha256sum | cut -c1-16; done
697d2f17 8140945a81687356
f0f26367 8140945a81687356
17f6ef0c 8140945a81687356
5cd2154f efa5f129cba312c2
114ffacd 365bf95842ce9bb0
273c0471 e219007ff487a54b
3aee2c07 2e8f2e891ea20417      <- freeze of record
c5335c70 e219007ff487a54b      <- records commit (row committed here)
```

- Freeze of record `3aee2c0`: the committed guard is `2e8f2e89…`; `contract.json`
  `frozen_tools["tools/staged-id-guard.py"]` at that rev is `2e8f2e89…` — the row's value is
  not it.
- Records commit `c5335c7` (the commit that carries the row): the committed guard is
  `e219007f…`, the A9 pin. On the day the row was written its sha matched no committed guard
  at the then-current freeze (`273c047`, `e219007f…`) either.
- `8140945a…` is a real committed blob, but only at the three pre-A4 freezes. A4
  (`contract.json` amendment A4) records that this exact blob's map check
  `re.fullmatch(r'S\d{3,}', ''.join(targets))` refuses every multi-entry map, which is why its
  `safe_map_admitted=0` and `C3_R43_PASS=false`:

```
$ git show 17f6ef0c:tools/staged-id-guard.py | sed -n '172p'
    if not re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0'):
```

and wave 1 measured it at the row's own freeze against the live staged set
(`.ufo/waves/round-43/w1/ExecC3Live.md:107`, 13-case selftest, `live_collisions=6`):

> `C3_R43: … safe_map_admitted=0 … C3_R43_PASS=false`

The safe map the counter builds covers every collision (7 at the freeze of record), so a tool
carrying the join bug cannot return `safe_map_admitted=1`. In other words: the only sha the
row could have copied from a passing state is *not* `8140945a…`, and the sha it did copy is
the one its own amendment says fails.

## F2 (high) — the named receipt line is in no committed stdout, and the "after" evidence is empty

```
$ git grep -l 'C3_R43_PASS=true' HEAD -- '*.stdout' '*.txt' '*.log'
HEAD:.ufo/evidence/round-43/prerun/c3-at-freeze.stdout

$ git ls-tree -r --name-only 3aee2c07 .ufo/evidence/round-43/after/ | wc -l   -> 0
$ git ls-tree -r --name-only c5335c70 .ufo/evidence/round-43/after/ | wc -l   -> 0
$ git ls-tree -r --name-only HEAD      .ufo/evidence/round-43/after/ | wc -l   -> 0
$ ls -la .ufo/evidence/round-43/after/                                        -> empty dir
```

The single committed passing line is the *prerun*, and it is not the claim's receipt:

```
$ cat .ufo/evidence/round-43/prerun/c3-at-freeze.stdout
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=23 … staged_rows=103
        live_collisions=6 live_collisions_agree=1 live_held=2 … safe_map_admitted=1 … safe_floor=S256
        rev=114ffacd813d67286e369fc8f7b89f2c0418aaf4 freeze=114ffacd813d67286e369fc8f7b89f2c0418aaf4 C3_R43_PASS=true
```

Three independent reasons it cannot be "the deciding receipt at the round-43 measured commit":

1. It ran at `rev=freeze=114ffacd`, a superseded A6/A7 freeze — not a measured (records) commit.
2. It was produced by a counter that is not the frozen one (`git show 114ffacd:…/guard/measure.py
   | sha256sum` → `8c8147e7…`, not the frozen `ae66342d…`), and it measured a guard blob that is
   neither the row's citation nor the freeze-of-record pin (`365bf958…`, 23 cases).
3. Its state predates the row's own records: it reads a 113-row registry (`live_collisions=6`,
   `live_held=2`), while the freeze of record's registry carries S159 (114 rows) and the frozen
   counter reads `live_collisions=7`, `live_held=3` (my run below). The receipt therefore
   describes records that this capability row is not about.

The row's own cells also point at a subsection that does not exist:

```
$ awk 'NR>=2048 && NR<=2085 && /^#/ {print NR": "$0}' SCORECARD.md
2048: ## Round 43 — survivor resolution (depth) + record agreement extended (calibration) + staged-id guard (operability) (2026-10-25)
```

Rounds 41 and 42 have their after-receipts as `### Round 41 — after the deciding run`
(`SCORECARD.md:1969`) and `### Round 42 — after the deciding run` (`:2022`), each backed by
committed `.ufo/evidence/round-42/after/c{1,2}-at-242c1b4a.{stdout,exit}`. Round 43 has neither
the heading nor an `after/` file, so the row's "Measured commit": "see the after subsection"
resolves to nothing and "the round-43 measured commit" is unnamed. The LOG round-43 entry
(`LOG.md:2221-2259`) likewise states C3 as answered and cites no deciding-run receipt, while
the round-42 entry just above it does cite one (`LOG.md:2219-2220`).

## F3 (medium) — the counter path does resolve, at the freeze and at the records commit

```
$ git show 3aee2c07:.ufo/evidence/round-43/guard/measure.py | sha256sum
ae66342df05a4ea9ff2a03799552cc14dac99f823cf0491ba4fd757a8f54161e
$ git show c5335c70:.ufo/evidence/round-43/guard/measure.py | sha256sum
ae66342df05a4ea9ff2a03799552cc14dac99f823cf0491ba4fd757a8f54161e
$ python3 -c 'import json;print(json.load(open(".ufo/evidence/round-43/contract.json"))["claims"]["C3"]["counter_sha256"])'
ae66342df05a4ea9ff2a03799552cc14dac99f823cf0491ba4fd757a8f54161e
```

It is the pinned counter, and `self_pin` resolves when the freeze is the freeze of record. It
does *not* resolve at `114ffacd` (`8c8147e7…`), so the path only exists from A9 (`273c047`)
onward — the row names no rev, which is why F1/F4 cannot be excused by "the counter at the
freeze named it". I ran the pinned counter at the freeze of record (allowed revision):

```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-43/guard/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 3aee2c078f8976499b587086af3577fc94dc8cf1 --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=24 selftest_failed=0
        staged_rows=103 live_collisions=7 live_collisions_agree=1 live_held=3 live_held_agree=1
        live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=1
        map_dedupe_live=1 safe_floor=S256 staged_sha256=020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807
        naive_agree=1 substitute=0 rev=3aee2c07… freeze=3aee2c07… C3_R43_PASS=true
EXIT=0
```

So the capability claim is **true and runnable at the freeze of record** with the guard
`2e8f2e89…`; what is missing is the receipt, not the capability. The before-state also
reproduces with `self_pin=1` under the freeze of record:

```
$ python3 …/guard/measure.py --lane … --rev 487b8f0 --freeze 3aee2c0…
C3_R43: self_pin=1 tool_absent=1 tool_sha_ok=0 selftest_exit=1 guard_error=no_json C3_R43_PASS=false
EXIT=1
```

## F4 (medium) — the row's printed counting command cannot produce its own target line

With `--freeze 17f6ef0c…` (the freeze printed in `SCORECARD.md:2061`) the `self_pin` conjunct
compares the *running* counter (`ae66342d…`) against that freeze's counter pin (`6278edcd…`),
so it is 0 by construction:

```
$ git show 17f6ef0c:.ufo/evidence/round-43/guard/measure.py | sha256sum
6278edcd691e230b32383a8b2ac25f38910e17f3041e4082271a5863a8d78601
$ python3 …/guard/measure.py --lane … --rev 487b8f0 --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
C3_R43: self_pin=0 tool_absent=1 … C3_R43_PASS=false
EXIT=1
```

Any deciding run that follows the row's command verbatim therefore fails `self_pin` before a
tool is even measured; a reader who "restores" the old counter at that freeze instead gets the
`8140945a…` join-bug blob and `safe_map_admitted=0` (F1). The same stale freeze appears in the
section header (`SCORECARD.md:2053`) and in C1/C2's commands (`:2059-2060`), so the row cannot
be repaired alone — the whole round-43 block still names `17f6ef0c` as the freeze while the
contract chain ends at `3aee2c0` (A8–A10 are amendments of that same file).

Arithmetic that follows without running a counter (records commit is off-limits for me): at
`rev=c5335c7` the guard blob is `e219007f…` (above), the freeze-of-record pin is `2e8f2e89…`,
so `tool_sha_ok=0` and the predicate is false there; and the row's own asserted pin
`8140945a…` differs from both, so no reading of the row's tool cell yields `tool_sha_ok=1` at
the measured commit.

## F5 (high) — the row is in the table without a passing demonstration (admission rule)

The capability table's own rule (`/home/vgpnk/Projects/shokunin/AXES.md:57-63`):

> Rows enter only through a round that demonstrates the capability running; a capability
> without a passing demonstration in the round report is pre-claiming and does not enter the
> table.

There is no round-43 report (`ls .ufo/reports/round-43 reports/round-43` → both absent) and no
committed stdout with the passing line (F2); the only passing evidence in the tree is a
wave-1 markdown transcript using a **substitute** tool, which the counter now marks
`substitute=1` and refuses (`.ufo/waves/round-43/w1/ExecC3Live.md:114`, `RevC3Tool.md:76`
"pinned_fixed" via the allowed `--tool-file` control). The frozen counter would score such a
run `C3_R43_PASS=false`. The row is therefore pre-claiming as written, independent of the sha
error.

## What resolves, and the minimal evidence repair

- Counter path: resolves (F3).
- Claim itself: verified true at the freeze of record by me (F3 run) with
  `staged_sha256=020fbeaa…`, 24 cases, 7 collisions, 3 held documents, `safe_floor=S256`.
- Repair implied by the findings (not performed — this seat is read-only): point the row's
  tool at `2e8f2e89…`, set the freeze to `3aee2c0…` in `SCORECARD.md:2053/2059-2061`, and
  commit the deciding-run `stdout`/`exit` under `.ufo/evidence/round-43/after/` with a
  `### Round 43 — after the deciding run` subsection naming the measured commit. Only then
  does the row's "deciding receipt" name something a reader can open.

## Residual risk / verification gaps

- The live half depends on a path outside the repository
  (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`). The frozen counter prints
  `staged_sha256=020fbeaa…` (A9), so a mutable-input receipt is *self*-pinning; but the
  committed prerun receipt (the only PASS in the tree) predates that field, so the row's cited
  receipt is not re-verifiable from lane bytes alone.
- I did not run any counter at `c5335c7` (forbidden). The `tool_sha_ok=0` at the measured
  commit is stated from the committed blob's sha256 versus the committed pin, not from a run.
- `8140945a…`'s failure is established from (a) the blob's own line 172, (b) amendment A4's
  record, and (c) the committed wave-1 measurement at that same pin — three independent
  sources, none of them a re-run of the counter at a disallowed rev.

## Method / tooling

`git show`/`sha256sum`/`git ls-tree`/`git grep` on the lane checkout; one scratch dir per run
under `/tmp/tameshi-r43-w2-RevCapabilityRow-*` (the counter writes only its own `mkdtemp`
workdir and removes it). No installs, no upgrades (`python3` system only), no lane writes, no
`git add/commit/stash/checkout/switch/reset/pull/push`, no `jj` command, no assimilation-repo
write.
