# T55W1ScribeLog — the round-55 `LOG.md` entry, corrected against the round's own receipts

seat: T55W1ScribeLog-2 (scribe)
round: 55 (hyaku run 11), L1 TameshiR55
lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
base `0a2010acd1e92e4e332774050825e21bcfc7e079`; freeze `631cd6455e58dce969310b4c0466c3383d9f5108`;
freeze amendments 1–7 at `e2979f2`, amendment 8 at `133b2ce` (the freeze pointer the
round now uses); content commit C0 `9cf0146`
axis worked: calibration — the round's record against the tree
deliverable: this file. `LOG.md` is a lane production file and was **not**
edited here.

**What this seat found, in one line:** the L1's entry is committed (`LOG.md:2522-2553`)
but it quotes numbers the round's *own* re-frozen receipts no longer print, and
one of its landed-content claims (QUALITY 106) does not exist in the tree. §1 is
the entry rewritten to the receipts, §2 is the measurement behind every number,
§5 lists the mismatches with their commands, §6 is one tool defect the round's
own item 1 forbids and its counter cannot see.

Nothing in the lane was written by this seat. Scratch:
`/fast/scratch/hyaku/tameshi-r55/T55W1ScribeLog-2`. Receipts:
`.ufo/waves/round-55/w1/T55W1ScribeLog-receipts/` (index in its `README.txt`).

---

## 1. The entry, ready to replace `LOG.md:2522-2553`

Shape follows the file: one paragraph per claim, a content paragraph, the
sources paragraph, then the `(close)` block. `⟨FILL …⟩` marks what only the
deciding run can supply.

````markdown
## 2026-10-28 — round 55, attempt 1 (this round)

L1 TameshiR55, hyaku run 11. Base `0a2010ac`; contract, both counters, the
controls harness, the 15 no-harm monitors and the deciding script frozen at
`631cd645`, then amended eight times before any control was scored and before the
single deciding invocation — amendments 1–7 at `e2979f2`, amendment 8 at
`133b2ce`, which is the freeze pointer the deciding run uses. All eight are in
`freeze.json`, both counters are re-frozen on the amended bytes, and both base
receipts were re-measured with amendments 1–7 (`premise=9/10` for C1,
`grammar=6/9` for C2). Claims: **C1 calibration**
(the lowest non-retired axis, 8) — the lane's record must agree with the tree on
the ten routed defects the round-54 non-author spot-check pinned (R54.1–R54.10),
each carrying the value its receipt derives. **C2 operability** — one exit
class, one line, on every documented allocating mode of the seven tools that
call `strict_scratch_root()`, not the self-test only.

C1 (before → after). At base the re-frozen counter prints
`C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`
(`.ufo/evidence/round-55/before/c1.stdout`). Nine premises hold; R54.9's does not
at base because amendment 7 moves its staged-package count onto a committed
receipt that does not exist at `0a2010ac` (`staged=0`) — the contract's kill
rule makes that a reported miss, not a narrowed row. The debt is 4 stale classes
carrying 11 occurrences (R54.1 ×6, R54.2 ×3, R54.3 ×1, R54.9 ×1 — the
whitespace-collapsed scan finds three multi-line occurrences the line-scoped one
could not) plus the absent corrections section. At C0 `9cf0146` the same bytes
print `C1_R55: rev=9cf0146b94dd classes=10 premise=10/10 stale=0
classes_corrected=10/10 total=0 C1_R55_PASS=true`. The ten dispositions, each
`old → derived value` with the receipt that decides it:

- **R54.1** `CTL_POS_c1 true` (SCORECARD) and `rekeyed=7/7` on the positive
  control (QUALITY 105's falsifier, lesson round-54 — six occurrences under the
  collapsed scan) → `CTL_MISMATCH` + `2/3`; cause: phase B cloned the freeze
  commit `077d431e`, which predates the re-key `7fa9a5e`, so the control could
  not fire (`.ufo/evidence/round-54/control/controls-b.stdout`). Round 55's
  phase B clones the revision it certifies.
- **R54.2** three pointers (`7883e0e5`, `fe70474d`, `097985c1`) → one,
  `077d431e` (5 amendments) — `…/round-54/after/frozen.stdout`.
- **R54.3** `total=14` → `total=13` — `…/round-54/before/c2.stdout`.
- **R54.4** `49280fe5` → `8528ee85`, the amendment-4 bytes that decided —
  `…/round-54/freeze.json`, key `c2/measure.py`.
- **R54.5** 25 wave-1 / 22 wave-2 in 9 sections → `w1=28 w2=25 sections=12`,
  re-derived over the committed reader files.
- **R54.6** three seat deliverables untracked at closure → committed by the
  sweep `ff2a821`.
- **R54.7** "the deletion lands in `7fa9a5e0`" → **renamed** (`R100`) into
  `…/round-54/w2/T54W2Sent01-receipts/forged-reader.json`, where it stays as
  the incident receipt and can never credit.
- **R54.8** the incident named but unrecorded → the fabricated `config.yml`
  write is recorded in `corpus/lessons/round-55.md`, and
  `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` carries a
  `SUPERSEDED (round 55, ER-R54-8)` block.
- **R54.9** 4 reviewers / 26.3 % / "84 staged" → `reviewers=5 attack=21/76
  seats=76` (27.6 %) and `staged=81`.
- **R54.10** `rekeyed=0/30` cited to `controls-a.stdout` → that file prints
  `0/7`; `0/30` belongs to `…/round-54/control/r53-counter-at-88afa941.stdout`.

C2 (before → after). At base the amendment-8 counter prints
`C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false`
(`before/c2.stdout` still carries the amendment-7 reading, `total=21`, and needs
one re-measure at the amendment-8 pointer): three of the nine allocating modes carried no parseable
class line — `repeat-control` and `context-capture` printed the raw exception
type, and `registry-check --rev` printed its token on stdout with empty stderr —
and no document named the line. At C0 `9cf0146` the amendment-8 bytes print
`C2_R55: rev=9cf0146b94dd grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true`
(`c2-c0-amendment8.stdout`) — **verifies** at the content commit (under
amendment 7 the same tree read `grammar=9/9 … total=1 C2_R55_PASS=false` with an
empty `bad` map: the total-formula defect amendment 8 repairs) nine allocating modes exit 2 with the frozen grammar on
stderr, 5/5 non-allocating modes stay lazy, 13/13 keep their expected exit on the
empty and usable arms, zero `mkdir` under `/tmp`, and the seven registry
`scratch_root` cells, the note's `## One line, every mode` (nine allocating,
five lazy) and `SKILL.md` state the grammar.

Content: `e2979f2` — the seven freeze amendments, both counters re-frozen, both
base receipts re-measured with them — and `9cf0146` (C0) — `repeat-control`,
`context-capture` and `registry-check` now raise `ScratchRootUnusable` and print
the frozen grammar on stderr with exit 2; the seven registry `scratch_root` cells
state the grammar and the allocating modes; the note's `## One line, every mode`
names the nine allocating and five lazy modes and says the class is an
operator-visible line grammar, not a shared Python type; `SKILL.md` `## Standing
rules` replaces the sentence that said the measurement stopped at `--selftest`
— that drift is re-read and re-keyed ⟨FILL: reader id, read revision, bound
`rekey-r55-*` ledger entry; none is bound at the time of this draft⟩;
`SCORECARD.md` gains `## Round 55 - round-54 record corrections` (ER-R54-1…10,
old → derived value → receipt) with the stale assertions fixed in place, the
round-55 block and the standing axis table re-stated;
`corpus/lessons/round-55.md` (Gate + Mistakes + dispositions). ⟨FILL: QUALITY —
the C0 message and the current entry claim "QUALITY 106 (a control is scored at
the revision it certifies) with an erratum on 105", but `corpus/QUALITY.md` ends
at `### Criterion 105` and C0's diff to it is one changed falsifier line (no new
criterion, no erratum label). Either land both or drop the claim⟩.

Round shape: one v2 wave of 75 filed seats (band 64–128; 22 scribe, 18 reviewer,
17 executor, 6 critic, 4 mutation-tester, 2 connector, 2 scout, 2 sentinel, 1
revenger, 1 simplifier — attack roles 28 = reviewer 18 + critic 6 +
mutation-tester 4 = 37.3 %, the definition that also gives round 54's 21/76),
plus one v1 wave (band 32–64) over what it produced ⟨FILL: wave-2 seats, role
mix, attack share⟩.

Sources opened this round: **S280** GNU Coding Standards §4.4 "Formatting Error
Messages" (https://www.gnu.org/prep/standards/html_node/Errors.html, fetched
2026-10-28, HTTP 200, 7147 B, sha256 `54c55cd4de53023b…`) — admitted and mined
for the one program-prefixed line (`program: message`); it says nothing about
the exit code, so the exit-2 class is the lane's own declaration. The FreeBSD
`sysexits(3)` candidate was rejected before append: the document is already held
as **S090** (same URL, so a new row would be a within-scope duplicate), and it
deprecates its own interface, so it cannot ground a rule that adopts its codes
(its snapshot is kept as the rejection's evidence). Registry at C0: 140 rows,
S001–S280; census exit 0.

  (close) Deciding run ⟨FILL: the `FROZEN_UNCHANGED=1 freeze=… rev=…` line, the
  no-harm count (15 monitors), the census exit, both verdict lines and
  `DECIDING_RUN_EXIT`⟩.
  Re-key bound ⟨FILL⟩; skipped: ⟨FILL⟩.
  C1 verdict: ⟨FILL⟩. C2 verdict: ⟨FILL⟩.
  Fleet census end: exit 0.
````

## 2. The measurements behind §1 (each reproducible)

Clone of the lane at `0a2010ac`, the two content commits fetched, each counter
run with an empty `--work` under this seat's scratch. Frozen bytes as re-frozen
at `e2979f2` (`c1/measure.py 5e8f50d1…`, `c2/measure.py 36ca47d3…`).

| run | line | receipt |
|---|---|---|
| C1 at base `0a2010ac` | `classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`; stale: R54.1 ×6, R54.2 ×3, R54.3 ×1, R54.9 ×1; R54.9 `premise=miss` (`staged=0`) | `c1-base-refrozen.stdout` |
| C1 at C0 `9cf0146` | `premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true` | `c1-c0-explain.stdout` |
| C2 at base, amendment 7 | `… total=21` (one higher than its own arms) | `git show e2979f2:.ufo/evidence/round-55/before/c2.stdout` |
| C2 at base, amendment 8 | `grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20` | `c2-base-amendment8.stdout` |
| C2 at C0, amendment 7 | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false` with `bad={}` | `c2-c0-amendment7.stdout`, `c2-c0-amendment7-receipts.json` |
| C2 at C0, amendment 8 | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true` | `c2-c0-amendment8.stdout`, `c2-c0-amendment8-receipts.json` |

C1 at base reproduces the bytes committed at `e2979f2` exactly; so does C2
(`before/c2.stdout` ends `grammar=6/9 … total=21`) — the pair is the round's
base row, not the older `631cd645` receipts (`premise=10/10`, `total=18`), which
belong to the pre-amendment counters.

Independent probes of the C2 surface on the C0 tree, with
`TMPDIR=/nonexistent/r55/probe`:

| mode | rc | stderr grammar | stdout |
|---|---|---|---|
| `repeat-control --selftest` | 2 | ✓ | **`REPEAT_CONTROL: setup_error`** |
| `context-capture --selftest` | 2 | ✓ | empty |
| `registry-check --rev HEAD` | 2 | ✓ | empty |
| `registry-check --selftest` | 2 | ✓ | empty |
| `bash-witness-study selftest` | 2 | ✓ | empty |
| `pin-disposition --selftest` | 2 | ✓ | empty |
| `evidence-disposition --selftest` | 2 | ✓ | empty |
| `env-diff --selftest` | 2 | ✓ | empty |
| `env-diff --contract …` | 2 | ✓ | empty |

(`allocating-modes-probe.txt`, `env-diff-contract-mode.txt`,
`registry-check-rev-mode.txt`.) Eight of nine are clean; `repeat-control`
carries a stdout token — §6.

## 3. Placeholder derivations

| marker | derivation |
|---|---|
| C2 after-line and verdict | `python3 .ufo/evidence/round-55/c2/measure.py --lane . --rev <deciding-rev> --work <empty> --explain` (receipt `c2-c0.stdout` when my run lands) |
| wave-2 seats / role mix / attack share | tally over `.ufo/waves/round-55/w2-registry.json` (`seats`, `attack_seats`, `role_mix`) |
| re-key binding | `.ufo/evidence/round-21/coldread/ledger.json` entry named `rekey-r55-*` (none bound at this draft) |
| QUALITY | `grep -n '^### ' corpus/QUALITY.md \| tail -1` → still `### Criterion 105` |
| close lines | `.ufo/evidence/round-55/after/{frozen,no-harm,c1,c2}.stdout`, `census.exit`, `DECIDING_RUN_EXIT` |

## 4. Facts this entry rests on

Receipt index: `T55W1ScribeLog-receipts/README.txt`.

| fact | value | command / receipt |
|---|---|---|
| base | `0a2010acd1e92e4e332774050825e21bcfc7e079` | `git rev-parse 0a2010ac` |
| freeze / amendments | `631cd645…`; amendments 1–7 at `e2979f2`, `freeze.json` lists all seven and its 8 pins (the 7 code files + `c1/staged-at-freeze.txt`) match the C0 bytes 8/8; no frozen path differs `e2979f2..9cf0146` | `freeze-integrity-at-c0.txt` |
| frozen paths since `e2979f2` | unchanged through C0 (`git diff --stat e2979f2 9cf0146 -- .ufo/evidence/round-55/` empty) | command output in §5 |
| wave-1 | 75 seats (band 64–128 ✓); scribe 22, reviewer 18, executor 17, critic 6, mutation-tester 4, connector 2, scout 2, sentinel 2, revenger 1, simplifier 1; axes calibration 46 / operability 22 / coverage 4 / freshness 3 | tally `base-freeze-and-rolemix.txt` |
| attack definition | reviewer + critic + mutation-tester: 18+6+4 = 28 (37.3 %) at round 55; 5+4+12 = 21 (27.6 %) at round 54 | both registries |
| SOURCES | 139 at base → 140 at C0 (S280); S090 is the same FreeBSD sysexits URL | `grep -c '^| S' corpus/SOURCES.md` |
| census | exit 0 at round start and at C0 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` |
| sources | GNU Errors HTTP 200, 7147 B, sha256 `54c55cd4de53023b…`; sysexits HTTP 200, 59251 B, sha256 `1fc793a298a937d7…` | `source-fetches.txt` |
| `bash-witness-study` mode | `--selftest` → rc 64 usage error; `selftest` → `WITNESS_SELFTEST: 51/51 pass`, rc 0 | `bash-witness-invocations.txt` |

## 5. The committed entry against the tree (each mismatch re-derived)

The entry at `LOG.md:2522-2553` (committed in C0) states seven things the tree
does not say. §1 fixes all seven; here is the evidence, so the L1 can check
without re-running anything.

1. **"amended four times … all four recorded in `freeze.json`"** — it is seven,
   and they are recorded: `contract.json` and `freeze.json` both list
   `[1..7]`, and the manifest's eight pins match the C0 bytes
   (`freeze-integrity-at-c0.txt`). At 13:51 this was false
   (3 listed, 2 stale pins, `freeze-manifest-check.out`); `e2979f2` repaired it.
   The entry was written to the pre-repair state.
2. **base C1 `premise=10/10`** — the receipt the entry names
   (`before/c1.stdout`) prints `premise=9/10` since `e2979f2`; the miss is
   R54.9 (`staged=0` at base). Quoting a receipt whose bytes changed under the
   quote is the same defect class as R54.3/R54.4.
3. **base C2 `grammar=6/8 … total=18`** — the receipt the entry names
   (`before/c2.stdout`) now reads `grammar=6/9 … note=0/9 … total=21` under
   amendment 7 and `total=20` under amendment 8 (the 21 over-counted its own
   arms by one):
   `registry-check --rev` is the ninth allocating mode the round added
   (amendment 6), so both the grammar and the note denominators grew, and the
   total moved with them.
4. **"the eight allocating modes"** (in the note sentence) — the note and the
   counter say nine; the entry inherited eight from the freeze before amendment
   6.
5. **"both tools now raise `ScratchRootUnusable`"** — three: `repeat-control`,
   `context-capture`, `registry-check` (C0 subject; `git show --stat 9cf0146`).
6. **"QUALITY 106 … with an erratum on 105"** — absent. `git show 9cf0146 --
   corpus/QUALITY.md` is one changed line (105's falsifier text); the file's
   last heading is `### Criterion 105` and nothing is labelled an erratum.
   This is round 54's defect class (a record asserting content the tree does not
   carry) recurring in round 55's own record.
7. **"is re-keyed with a fresh reader at C0"** — unearned:
   `grep -c r55 .ufo/evidence/round-21/coldread/ledger.json` → 0, and no
   `rekey-r55-*` artifact exists. The re-key is still owed.

## 6. The one tool residue the round's own item forbids and its counter cannot see

`tools/repeat-control.py`'s `could_not_evaluate()` prints
`REPEAT_CONTROL: setup_error` on **stdout** in addition to the grammar line on
stderr, so a caller parsing stdout still gets a setup verdict token. Round 55's
integration item 1 says "stdout carries no setup error"; the frozen C2 grammar
arm checks only `rc == 2`, a stderr line matching the grammar, and the absence of
`RuntimeError`/`Traceback` — it never reads stdout, so C2 can be true while the
item is unmet. Measured on the C0 tree (`9cf0146`), receipt
`repeat-control-stdout.txt`:

```
$ TMPDIR=/nonexistent/r55/probe python3 tools/repeat-control.py --selftest
rc=2
stdout='REPEAT_CONTROL: setup_error\n'
stderr="repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/r55/probe' (could-not-evaluate)\n"
```

The same class was found in `registry-check --rev` (stdout token, empty stderr)
by a wave seat and fixed in C0; `repeat-control` was not. Re-checked live against
the worktree at the close of this seat — `TMPDIR=/nonexistent/r55/probe python3
tools/repeat-control.py --selftest` prints the grammar line on stderr **and**
`REPEAT_CONTROL: setup_error` on stdout, exit 2 — while
`tools/registry-check.py` is modified in the worktree (the L1 is on the same
class there). Proposed one-line fix,
demonstrated in a scratch clone (stdout empty, rc 2, one stderr line, and the
tool's own `SELFTEST: PASS (29 cases)` still green under a usable `TMPDIR`):

```diff
--- i/tools/repeat-control.py
+++ w/tools/repeat-control.py
@@ -232,5 +232,4 @@ def could_not_evaluate(message):
     the exception type never reaches the operator line."""
     emit_err(f"repeat-control: could-not-evaluate: {message}")
-    emit("REPEAT_CONTROL: setup_error")
     return EXIT_BY_ID["setup_error"]
```

No consumer parses that token (`grep -rn 'REPEAT_CONTROL: setup_error'` finds the
tool and a round-12 superseded copy only), and `setup_failure()` keeps its own
token for the non-scratch setup class. If the L1 prefers not to touch the tool,
the honest alternative is to weaken item 1's stdout clause and the note — but the
note currently promises stdout clean.

## 7. Counter observations (reported, not fixed)

- **The C2 grammar arm cannot see a stdout token** (§6): the class is defined as
  a stderr line, which is the right contract, but a tool that also emits a
  verdict token on stdout passes. A one-line arm (`stdout == ""` for the
  allocating modes on the unusable path) would close it — a round-56 candidate,
  since the bytes are frozen.
- **The C2 `total` formula was one short of its own arms** — at C0 every printed
  arm was green (`grammar 9/9 … skill 1/1`) with an empty `bad` map, yet the
  verdict read `total=1 C2_R55_PASS=false` (`c2-c0-amendment7.stdout`). This
  seat reproduced it independently; the L1's amendment 8 (`133b2ce`) makes the
  totals use the denominators they measure and moves the freeze pointer with it.
  Recorded as agreement, not as an open finding.
- **The R54.8 seat-file arm is now sound.** It used to accept any occurrence of
  `superseded` — true at base in an unrelated sentence
  (`…/T54W1ExecStraceNoise.md:299`) — and amendment 7 tightened it to
  `SUPERSEDED (round 55`. This seat reached the same conclusion independently
  before seeing the amendment; recorded as agreement, not as a finding.
- **`tools/registry.json` is re-serialized, not only edited:** `git diff
  --numstat 0a2010ac 9cf0146 -- tools/registry.json` is far larger than the seven
  cells whose values change (a key-order-insensitive walk prints 7 `VAL` lines
  and no adds/deletes/length changes). Reviewability cost only.

## 8. Out of scope / not done

- `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/**`, `tools/**`: not touched;
  §1 is the entry and §6 the one proposed tool diff.
- The deciding run, the controls, the re-key: the L1's, one invocation each.
- No tool was installed or upgraded (nothing was needed; `python3`, `git`,
  `curl`, `strace` sufficed).
- Scratch note: the first scratch root this seat used
  (`…/tameshi-r55/T55W1ScribeLog`) was deleted mid-run by a sibling holding the
  same path (its `EXIT` trap); the seat re-ran under `…/T55W1ScribeLog-2`. Not a
  lane defect.
