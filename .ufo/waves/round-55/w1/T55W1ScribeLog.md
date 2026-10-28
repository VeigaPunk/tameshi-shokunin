# T55W1ScribeLog — the round-55 `LOG.md` entry, completed and checked

seat: T55W1ScribeLog-2 (scribe)
round: 55 (hyaku run 11), L1 TameshiR55
lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
base `0a2010acd1e92e4e332774050825e21bcfc7e079`; freeze commit
`631cd6455e58dce969310b4c0466c3383d9f5108`
axis worked: calibration — the round's record against the tree
deliverable: this file. `LOG.md` is a lane production file and was **not**
edited here. The L1 landed its own entry at `LOG.md:2522-2553` (uncommitted in
the worktree while this seat ran); §1 is that entry **revised**: its facts kept,
its missing required elements added, its three unearned claims either fixed or
turned into explicit `⟨FILL …⟩` markers. §5 is the check behind those edits.

Nothing in the lane was written by this seat. Scratch:
`/fast/scratch/hyaku/tameshi-r55/T55W1ScribeLog-2` (clone, patched clone,
counters). Receipts: `.ufo/waves/round-55/w1/T55W1ScribeLog-receipts/`.

---

## 1. The entry, ready to replace `LOG.md:2522-2553`

Shape follows the file: one paragraph per claim, a content paragraph, then a
`(close)` block. `⟨FILL …⟩` marks a value only the L1's own run can supply; §3
gives each marker's derivation command.

````markdown
## 2026-10-28 — round 55, attempt 1 (this round)

L1 TameshiR55, hyaku run 11. Base `0a2010ac`; contract, both counters, the
controls harness, the 15 no-harm monitors and the deciding script frozen at
`631cd645`, amended four times before any control was scored or any deciding
invocation ran ⟨FILL: the freeze-amendment commit that re-hashes `freeze.json`
for all four amendments and lists them — at the time of this draft `freeze.json`
records three, and two of its pins (`contract.json`, `c2/measure.py`) no longer
match the worktree bytes, so the deciding gate would print `FROZEN_UNCHANGED=0`⟩.
Claims: **C1 calibration** (the lowest non-retired axis, 8) — the lane's record
must agree with the tree on the ten routed defects the round-54 non-author
spot-check pinned (R54.1–R54.10), each with the receipt the defect names.
**C2 operability** — one exit class, one line, every documented allocating mode
of the seven tools that call `strict_scratch_root()`, not the self-test only.

C1 (before → after). At base the frozen counter prints
`C1_R55: rev=0a2010acd1e9 classes=10 premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`
(`.ufo/evidence/round-55/before/c1.stdout`): every class's premise already held,
so the round is a record repair, and the debt is 8 stale occurrences in 4
classes (R54.1 ×3, R54.2 ×3, R54.3 ×1, R54.9 ×1) plus the absent corrections
section. At ⟨FILL: content rev⟩ the same frozen bytes print ⟨FILL: the C1 line,
`... total=0 C1_R55_PASS=true`⟩ — ⟨FILL: verdict⟩. Each class now carries the
value derived from a receipt, not a literal; the ten dispositions:

- **R54.1** `CTL_POS_c1 true` (SCORECARD) and `rekeyed=7/7` on the positive
  control (QUALITY 105's falsifier, lesson round-54) → `CTL_MISMATCH` + `2/3`;
  cause: phase B cloned the freeze commit `077d431e`, which predates the re-key
  `7fa9a5e`, so the control could not fire
  (`.ufo/evidence/round-54/control/controls-b.stdout`). Round 55's phase B
  clones the revision it certifies.
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
  `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` is marked superseded.
- **R54.9** 4 reviewers / 26.3 % / "84 staged" → `reviewers=5 attack=21/76
  seats=76` (27.6 %) and `staged=81`.
- **R54.10** `rekeyed=0/30` cited to `controls-a.stdout` → that file prints
  `0/7`; `0/30` belongs to `…/round-54/control/r53-counter-at-88afa941.stdout`.

C2 (before → after). At base the frozen counter prints
`C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false`
(`before/c2.stdout`): `repeat-control` and `context-capture` printed the raw
exception type (and `context-capture` printed on stdout), so 2 of the 8
allocating modes carried no parseable class line, and no document named the
line. ⟨FILL: decide the base row — the *amended* bytes re-run at base read
`usable=12/13 … total=19`, `registry-check --selftest rc=1` on the base
`registry.json`; round 54's precedent makes the amended re-run the base row, so
if that is the rule this line becomes the 19 one and the 18 stays named as the
pre-amendment receipt⟩. At ⟨FILL: content rev⟩ it prints ⟨FILL: the C2 line,
`... total=0 C2_R55_PASS=true`⟩ — ⟨FILL: verdict⟩: 8/8 allocating modes (the
seven self-tests plus `env-diff --contract`) exit 2 with one stderr line
matching the frozen grammar and no `RuntimeError`/`Traceback` token, 5/5
non-allocating modes stay lazy, 13/13 keep their expected exit on the empty and
usable arms, zero `mkdir` under `/tmp`, and the seven registry `scratch_root`
cells, the note's `## One line, every mode` and `SKILL.md` state the grammar.

Content: ⟨FILL: the C0 content commit and the fix commit(s), hash and subject⟩.
C0: both tools raise `ScratchRootUnusable` and print the frozen grammar on
stderr with exit 2; the seven registry `scratch_root` cells state the grammar
and the eight allocating modes; the note's `## One line, every mode` names the
eight allocating and five lazy modes and says the class is an
operator-visible line grammar, not a shared Python type; `SKILL.md`
`## Standing rules` replaces the sentence that said the measurement stopped at
`--selftest` — the section that edit drifts was re-read and re-keyed
⟨FILL: reader id, read revision, bound ledger entry — no `rekey-r55-*` entry is
bound at the time of this draft⟩; `SCORECARD.md` gained `## Round 55 - round-54
record corrections` (ER-R54-1…10, old → derived value → receipt) with the stale
assertions fixed in place, the round-55 block and the standing axis table
re-stated; QUALITY 106 (a control is scored at the revision it certifies) with
105's falsifier corrected in place ⟨FILL: confirm 106 landed — `grep -n '^### '
corpus/QUALITY.md | tail -1` still reads 105⟩; `corpus/lessons/round-55.md`
(Gate + Mistakes + dispositions).

Sources opened this round: **S280** GNU Coding Standards §4.4 "Formatting Error
Messages" (https://www.gnu.org/prep/standards/html_node/Errors.html, fetched
2026-10-28, HTTP 200, 7147 B, sha256 `54c55cd4de53023b…`) — admitted and mined
for the one program-prefixed line (`program: message`), cited by the note; it
says nothing about the exit code, so the exit-2 class is the lane's own
declaration. The FreeBSD `sysexits(3)` candidate was **rejected before append**:
the document is already held as **S090** (same URL), so a new row would be a
within-scope duplicate, and it deprecates its own interface, so it cannot
ground a rule that adopts its codes (the snapshot is kept as the rejection's
evidence). Census at round end: exit 0, ⟨FILL: row count — 140 (S001–S280) at
this draft⟩.

  (close) Deciding run ⟨FILL: the `FROZEN_UNCHANGED=1 freeze=… rev=…` line, the
  no-harm count (the contract pre-registers 15 monitors), the census exit, both
  verdict lines and `DECIDING_RUN_EXIT`⟩.
  Re-key bound ⟨FILL: n of n headings⟩; skipped: ⟨FILL⟩.
  C1 verdict: ⟨FILL⟩. C2 verdict: ⟨FILL⟩.
  Fleet census end: exit 0.
````

## 2. Provisional measurement of the candidate tree (not the deciding run)

The L1's worktree was cloned at `0a2010ac`, its diff applied and committed in
the clone — `63d08ed1a32f9d9718872f20efbfb08daac60268`, with
`git -C <clone> rev-parse --show-toplevel` = the clone. The frozen C1 bytes
read:

```
C1_R55: rev=63d08ed1a32f classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

(`T55W1ScribeLog-receipts/c1-candidate.stdout`; the earlier snapshot
`06be1401` read the same). `total=0` is therefore already reachable; this is
**not** the deciding run and must not be quoted as the after-line.

The frozen C2 bytes on the same clone read:

```
C2_R55: rev=63d08ed1a32f grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=0 C2_R55_PASS=true
```

(`T55W1ScribeLog-receipts/c2-candidate.stdout`.) Again provisional — the L1's
deciding run is the one that counts — but it says the whole C2 surface is
already reachable from the candidate bytes, including the three document arms
that read 0 at base. The run takes ~6 minutes; the cost is dominated by
`registry-check --selftest` (32.2 s plain, longer under `strace`).

Independently of the counter, the eight allocating modes were driven by hand
with a set-but-unusable `TMPDIR` on the candidate tree:

| mode | rc | stderr lines | grammar | stdout |
|---|---|---|---|---|
| `repeat-control --selftest` | 2 | 1 | ✓ | **`REPEAT_CONTROL: setup_error`** |
| `registry-check --selftest` | 2 | 1 | ✓ | empty |
| `bash-witness-study selftest` | 2 | 1 | ✓ | empty |
| `pin-disposition --selftest` | 2 | 1 | ✓ | empty |
| `evidence-disposition --selftest` | 2 | 1 | ✓ | empty |
| `context-capture --selftest` | 2 | 1 | ✓ | empty |
| `env-diff --selftest` | 2 | 1 | ✓ | empty |
| `env-diff --contract …` | 2 | 1 | ✓ | empty |

(`allocating-modes-probe.txt`, `env-diff-contract-mode.txt`.) Seven of eight
meet the round's integration item 1 in full; `repeat-control` meets the frozen
counter's arm but not the item's stdout clause — see §6.

## 3. Placeholder derivations

| marker | derivation |
|---|---|
| freeze-amendment commit | `python3 -c "import json;print([a['n'] for a in json.load(open('.ufo/evidence/round-55/freeze.json'))['amendments']])"` must list 1–4, and `sha256sum` of every `freeze.json` `files` key must equal its pin |
| wave-2 seats / role mix / attack share | same tally as wave 1 over `.ufo/waves/round-55/w2-registry.json`: `seats`, `attack_seats`, `role_mix` |
| C1 after-line + verdict | `python3 .ufo/evidence/round-55/c1/measure.py --lane . --rev <content-rev> --work <empty> --explain` |
| C2 after-line + verdict | `python3 .ufo/evidence/round-55/c2/measure.py --lane . --rev <content-rev> --work <empty> --explain` |
| content commits | `git log --oneline 0a2010ac..<content-rev>` |
| re-key binding | `.ufo/evidence/round-21/coldread/ledger.json` entry named `rekey-r55-*` (none bound at this draft) |
| QUALITY 106 | `grep -n '^### ' corpus/QUALITY.md \| tail -1` |
| SOURCES row count | `grep -c '^\| S' corpus/SOURCES.md` |
| close lines | `.ufo/evidence/round-55/after/{frozen,no-harm,c1,c2}.stdout`, `census.exit`, `DECIDING_RUN_EXIT` |

## 4. Facts this entry rests on (each with its command)

Receipt index: `T55W1ScribeLog-receipts/README.txt` — one line per file.

| fact | value | command / receipt |
|---|---|---|
| base | `0a2010acd1e92e4e332774050825e21bcfc7e079` | `git rev-parse 0a2010ac` |
| freeze commit | `631cd6455e58dce969310b4c0466c3383d9f5108` | `git rev-parse 631cd64` |
| C1 base | `premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`; stale hits SCORECARD.md:2583,2564,2567,2584,2608 + QUALITY.md:1590 + lessons/round-54.md:51,101 | `c1/measure.py --explain` at base (`c1-base-explain.stdout`) — reproduces `before/c1.stdout` byte for byte |
| C1 candidate | `stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true` at `63d08ed1` | (`c1-candidate.stdout`) |
| C2 base (frozen) | `grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18`; failing modes `repeat-control`, `context-capture` | `git show 631cd64:.ufo/evidence/round-55/before/c2.stdout` |
| wave-1 | 75 seats; scribe 22, reviewer 18, executor 17, critic 6, mutation-tester 4, connector 2, scout 2, sentinel 2, revenger 1, simplifier 1; axes 46/22/4/3 | tally over `w1/swarm-registry.json` (`base-freeze-and-rolemix.txt`) |
| attack definition | reviewer + critic + mutation-tester: 18+6+4 = 28 (37.3 %) for round 55, 5+4+12 = 21 (27.6 %) for round 54 | both registries |
| SOURCES | 139 rows at base (S001–S279) → 140 now (S280); S090 is the same FreeBSD sysexits URL | `grep -c '^| S' corpus/SOURCES.md`; `grep -n '^| S090' corpus/SOURCES.md` |
| census | start exit 0; current exit 0 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` |
| sources | GNU Errors HTTP 200, 7147 B, sha256 `54c55cd4de53023b…`; sysexits HTTP 200, 59251 B, sha256 `1fc793a298a937d7…` | `curl` + `sha256sum` (`source-fetches.txt`) |
| `bash-witness-study` mode | `--selftest` → rc 64 usage error; `selftest` → `WITNESS_SELFTEST: 51/51 pass`, rc 0 | probe (`bash-witness-invocations.txt`) |

## 5. What the L1's own draft got wrong or left unearned (checked, not assumed)

The L1's entry (`LOG.md` worktree, `git diff -- LOG.md`) is a good draft; these
are the places where the tree does not yet say what it says. Each is a
`⟨FILL⟩` in §1.

1. **"amended four times … all four recorded in `freeze.json`"** — false as of
   this check: `freeze.json` lists `[1, 2, 3]` while `contract.json` listed
   `[1, 2, 3, 4]` at the first check and `[1, 2, 3, 4, 5]` at the close of this
   seat, and two pins no longer match their files (`c2/measure.py` `d6ca1d85`
   vs pinned `ab3ae751`; `contract.json` `0b99dd8c` vs pinned `ed6871e1`). The
   deciding script's gate compares the freeze commit to the deciding rev over
   the frozen paths (`deciding-run.sh:65`), so committing the amended
   instrument without a freeze-amendment commit that re-hashes the manifest
   makes `FROZEN_UNCHANGED=0` and the run exits non-zero. Receipt:
   `freeze-manifest-check.out`, `freeze-integrity.txt`.
2. **"QUALITY 106 … with an erratum on 105"** — 106 has not landed:
   `grep -n '^### ' corpus/QUALITY.md | tail -1` → `### Criterion 105 …`. The
   105 falsifier was corrected in place (good), but it is not labelled an
   erratum and there is no 106.
3. **"the one SKILL.md section … is re-keyed with a fresh reader at C0"** —
   no binding exists: `grep -c r55 .ufo/evidence/round-21/coldread/ledger.json`
   → 0, and no `rekey-r55-*` artifact is present.
4. **"Census at round end: … 141 rows"** (the lesson, not the entry) —
   `grep -c '^| S' corpus/SOURCES.md` → **140** at this check (139 at base +
   S280; the rejected sysexits candidate correctly adds nothing).
5. **The entry's C2 before-line is the frozen receipt's** (`usable=13/13
   total=18`), while the amended instrument, run at base in a scratch clone,
   reads `usable=12/13 … total=19` with the failing mode
   `registry-check --selftest rc=1` (`c2-base-amended.stdout`). Both readings
   are real: the frozen receipt is the pre-amendment bytes (its usable rc came
   from the traced run), the amended bytes take the plain run's rc and the base
   `registry.json` fails `registry-check`'s own selftest. Round 54's precedent is
   that **the amended counter re-run at base is the base row** — so the entry
   should cite the amended denominator and disclose the frozen receipt's 18,
   rather than quote 18 as the round's before. Receipt:
   `before-receipt-drift.txt`, `c2-base-amended.stdout`.

Two further observations, not defects of the entry:

- **The C1 counter's R54.8 seat arm cannot fail on its own half.**
  `c1/measure.py:223` asks `"superseded" in seat.lower()`, and the round-54 seat
  file already contains the word at base in an unrelated sentence
  (`git show 0a2010ac:.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md:299`,
  "the round-50 directive superseded it"). The class still discriminated at
  base only because `corrected` also requires `config.yml` and `fabricated` in
  the corrections section. Reported, not fixed: the bytes are frozen, and a
  re-anchored arm (`^**SUPERSEDED \(round 55`) is a round-56 candidate.
- **`tools/registry.json` is re-serialized, not only edited.** `git diff
  --numstat` = 1275/1026 for a change whose semantic content is exactly the 7
  `scratch_root` cells (a key-order-insensitive walk over
  `git show 0a2010ac:tools/registry.json` vs the worktree prints 7 `VAL` lines
  and no adds/deletes/length changes); `git diff -w` still reports 319/70.
  Reviewability cost only.
- **The frozen C2 label for `bash-witness-study` was display-only.** The frozen
  `modes()` invoked the `selftest` subcommand while labelling the row
  `--selftest` (`git show 631cd64:…/c2/measure.py:84,90`), so the receipt's
  `rc=2`/`rc=0` are live readings of the subcommand — the flag form is an
  argparse usage error (rc 64). Recorded so no later reader "corrects" the
  receipt to 64.

## 6. One routed defect this round should carry (with its demonstration)

**Item 1's stdout clause is unmet and unmeasured.** `tools/repeat-control.py`'s
`could_not_evaluate()` prints `REPEAT_CONTROL: setup_error` on **stdout** as
well as the grammar line on stderr, so a caller parsing stdout still sees a
setup verdict token — exactly the vocabulary residue the note condemns for
`context-capture` and the round's integration item 1 forbids ("stdout carries
no setup error"). The tool's own docstring two lines above claims the opposite
("stdout keeps no setup error" is the note's wording for context-capture; the
handler's docstring says "the exception type never reaches the operator line").
The frozen C2 grammar arm does not look at stdout, so C2 can pass while the
item is unmet.

Measured on the candidate tree (`63d08ed1`), receipt
`T55W1ScribeLog-receipts/repeat-control-stdout.txt`:

```
$ TMPDIR=/nonexistent/r55/probe python3 tools/repeat-control.py --selftest
rc=2
stdout='REPEAT_CONTROL: setup_error\n'
stderr="repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/r55/probe' (could-not-evaluate)\n"
```

Proposed one-line fix (demonstrated in a scratch clone: stdout becomes empty,
rc 2, one stderr line, and the tool's own 29-case selftest still passes under a
usable `TMPDIR`):

```diff
--- i/tools/repeat-control.py
+++ w/tools/repeat-control.py
@@ -232,5 +232,4 @@ def could_not_evaluate(message):
     the exception type never reaches the operator line."""
     emit_err(f"repeat-control: could-not-evaluate: {message}")
-    emit("REPEAT_CONTROL: setup_error")
     return EXIT_BY_ID["setup_error"]
```

No consumer parses that token (`grep -rn 'REPEAT_CONTROL: setup_error'` finds
only the tool and a round-12 superseded copy), and `setup_failure()` keeps its
own token for the non-scratch setup class. If the L1 prefers not to touch the
tool, the honest alternative is to drop the stdout clause from the integration
list and the note — but the note currently makes the stronger promise.

## 7. Out of scope / not done

- `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/**`, `tools/**`: not touched;
  §1 is the patch and §6 the one proposed tool diff.
- The deciding run, the controls, the re-key: the L1's, one invocation each.
- No tool was installed or upgraded (nothing was needed; `python3`, `git`,
  `curl`, `strace` sufficed).
- Scratch note: the first scratch root this seat used
  (`…/tameshi-r55/T55W1ScribeLog`) was deleted mid-run by a sibling holding the
  same path (its `EXIT` trap), which cost one C2 run; the seat re-ran under
  `…/T55W1ScribeLog-2`. Not a lane defect.
