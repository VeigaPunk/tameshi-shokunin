# T55W3RevBinderInputs — binder input choice (wave 3, round 55)

Item: for three of the 18 lost sections (one `corpus/SOURCES.md`, one tool, one
`corpus/QUALITY.md`), read `.ufo/evidence/round-54/integrate/binder.py`, say exactly which inputs
a re-key entry pins, whether they are the right inputs for that section's claims, and whether the
DROP list should carry anything else for this round. Report the three input sets as written.

Verdicts, in one line each:

- **The three sets are the binder's historical union, not the sections' inputs.** 30 / 124 / 75
  pins for sections whose text names 2 / 9 / 9 of them; 28 / 115 / 67 pins are files the section
  never names (`§2`). The union includes the *previous* re-key entry, so the pinned surface
  ratchets: `## Mutation-sweep recipe` would pin **7,702** files, `## Standing rules` **2,497**;
  11,188 pins over the 18 headings (`§2.2`).
- **The one argument that decides this round is `PIN = C0`.** With `PIN = C0` the round's own
  adjudicated C1 fixes re-drift **13 of the 18** re-keyed sections (11,188 → 13 exposed, `§4`).
  With `PIN = C1` the entries would instead pin bytes no reader read. Both are wrong without a
  second read pass; the binder cannot express either.
- **DROP must not grow.** Adding the drifted files to DROP frees **3 of 17** input-drift sections
  for `corpus/SOURCES.md` alone and **17 of 17** for the whole changed set — credit with no read
  (`§5`). What is broken is not DROP but three of the binder's *inputs*: the resolutions file
  (wrong schema → `KeyError`), the heading list (live working-tree read, absent at C0, unfrozen),
  and `PIN`.
- **The re-key entry's trace is false provenance** — argv for a `section` subcommand `main()`
  never implements, `exit: 0` where the run exits 1, "no live working-tree reads" where the
  binder reads two files from the working tree, and `inputs` = the union (`§3`). 23 such entries
  came from round 54 and **5 of the 46 credited sections credit only through one of them**.

Attacked: the binder's three parameter classes — `HEADINGS`, `RES`, `PIN` — plus the entry it
writes. Every number below is reproduced by
`.ufo/waves/round-55/w3/T55W3RevBinderInputs-receipts/repro.sh` (output kept at `repro.log`;
`derive.py` is the independent lost-set derivation; `04-three-input-sets.json` holds the three
entry `inputs` dicts verbatim).

---

## 1. The three sections, and why these three

Chosen from the 18 in `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` so that each isolates
one input class:

| pick | heading (SKILL.md @ C0) | line range | round-55 inputs that moved it |
|---|---|---|---|
| `corpus/SOURCES.md` | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | 936–949 (14 lines) | `corpus/SOURCES.md` **only** |
| tool | `### Gate/probe registry` | 1528–1545 (18 lines) | `tools/repeat-control.py` **only** |
| `corpus/QUALITY.md` | `### Round-21 gate/probe registry — finite environment differential` | 1994–2133 (140 lines) | `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/registry-check.py`, `tools/registry.json` |

The obligation itself is sound, and I verified it rather than assuming it: an independent replay of
the round-18/round-21 credit predicate at C0 (`derive.py`, entry selection by section sha, class
gate, `commands_executed_count > 0`, every input minus `IGNORED_INPUTS` hashed from one
`git cat-file --batch`) prints `CREDITED=46 LOST=18` and `DECLARED=18 SET_EQUAL=True`
(`repro.log §1`). The per-section cause lists match the nine files the C0 commit moved and nothing
else.

## 2. The three input sets as they would be written

Run at `PIN = 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (the content commit) with synthetic readers
whose `cand`/`section_sha256` are the C0 section (scratch clone only; `repro.sh §3`):

```
REKEY ## The leg ledger — replay, receipt, and how it is read (rou start=936  inputs=30   dropped=0
REKEY ### Gate/probe registry                                start=1528 inputs=124  dropped=0
REKEY ### Round-21 gate/probe registry — finite environment  start=1994 inputs=75   dropped=0
REFRESH rekeyed=3 skipped=15 headings=18
```

### 2.1 `## The leg ledger …` — 30 pins (complete)

`{"corpus/SOURCES.md": "57ece0e5716deb46ec9d1d6c0c076beab31a9ba82ad323a68e85450b429be112", …}`

1. `.ufo/evidence/round-18/final/{before,case7,case8,context,disposition,historical,probes,registry-branch-aligned,regression,repeat}.stdout`
2. `.ufo/evidence/round-18/final/checks.json`
3. `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`
4. `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`
5. `corpus/README.md`, `corpus/SOURCES.md`
6. `corpus/knowledge/{closeout-r11,fleet-kill-rate-ledger,incremental-pin-disposition,mutation-case-kagi-checklist,mutation-case-kumitate-cite-check,mutation-case-kumitate-claims,operator-runbook,service-limits,service-standing-state}.md`
7. `corpus/lessons/{round-18-verifier-spotcheck,round-18,round-20}.md`
8. `plans/round-7.plan.md`, `tools/mutate-and-run.sh`, `tools/trace-inputs.py`

Written verbatim (this is `entry.inputs`, sorted; the same dict is `inputs` in the trace the binder generates):

```json
{
 ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
 ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
 ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
 ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
 ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
 ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
 ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
 ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
 ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
 ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
 ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
 ".ufo/evidence/round-18/sources-check/sources-check.defects.spec": "c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91",
 ".ufo/evidence/round-26/cite-check/cite-check.defects.spec": "969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208",
 "corpus/README.md": "0acfcf3ad5d878d25854d8d0817c254535b44268dfc5ae4fa4b53e088ecf456a",
 "corpus/SOURCES.md": "57ece0e5716deb46ec9d1d6c0c076beab31a9ba82ad323a68e85450b429be112",
 "corpus/knowledge/closeout-r11.md": "f0894bf65aee32d81fde3f9233b8f35968e200bc7906d0035a786d3df94d1fd7",
 "corpus/knowledge/fleet-kill-rate-ledger.md": "d345ae3e53e48a8b5ccb46e7d6f048a105081865e0edee89609f8e653fcf17c6",
 "corpus/knowledge/incremental-pin-disposition.md": "966a8065ea8e175cb7debc56bc58c4d1beaeddd159856c2e13fe74ea7fcab06b",
 "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7",
 "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
 "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
 "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
 "corpus/knowledge/service-limits.md": "8e9a1fe1261dd2c02d4c3daf5fe0126de96b7af40c59e667eb3ddf025b2ef0c1",
 "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952",
 "corpus/lessons/round-18-verifier-spotcheck.md": "3cfda4e1f64131a290c04278fb60c4402ffd58dd477ca2178eac4e2a00364fef",
 "corpus/lessons/round-18.md": "88b17f6df3290cf61d886bab322add21e863177003e1725df4f928c44b7d3159",
 "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6",
 "plans/round-7.plan.md": "49cd55fd0efaf892c281ec90538310cd5691af2af4ab1270c9945146fdc0fcec",
 "tools/mutate-and-run.sh": "977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda",
 "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
}
```

The 124- and 75-pin dicts are too large to inline and are committed verbatim in
`T55W3RevBinderInputs-receipts/04-three-input-sets.json`.

### 2.2 `### Gate/probe registry` — 124 pins; `### Round-21 …` — 75 pins

Complete dicts in `04-three-input-sets.json`. Shape:

- `### Gate/probe registry`: 117 `.ufo/evidence/round-12/…` files (the crashed
  `BashWitness` sweep, `ControlGate` fixtures), `.gitignore`, `SHONEN.md`, `corpus/…` (1),
  `tools/{repeat-control,bash-witness-study}.py`, `tools/registry.json`. Drift cause among them:
  `tools/repeat-control.py`.
- `### Round-21 …`: 54 `.ufo/evidence/round-1x/…` files (round-15/18/20/21/22/26 measures,
  receipts, routemix specs), 12 `corpus/…`, 10 `tools/…`. Drift causes among them:
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/registry-check.py`, `tools/registry.json`.

Total written over the 18 headings: **11,188 pins** (`repro.log §7`).

The rule that produces these numbers is `binder.py:134-142`: for every ledger entry carrying the
heading (`old = [e for e in entries if e.get('heading') == h]`), take each `inputs` key, skip
`DROP`, re-hash at PIN. It is a union over *history*, and because the previous round's re-key entry
is itself an entry, the next round's union contains it.

## 3. Are these the right inputs for those sections' claims?

Measured against the section bytes at C0 (`repro.log §5`):

| heading | pins | names its own commands/anchors | pinned **and** named | unnamed pins |
|---|---|---|---|---|
| `## The leg ledger …` | 30 | `tools/mutate-and-run.sh`, `corpus/knowledge/fleet-kill-rate-ledger.md` | 2 | 28 |
| `### Gate/probe registry` | 124 | `repeat-control.py`, `bash-witness-study.py`, 5 round-12 evidence files, `SHONEN.md`, a lesson | 9 | 115 |
| `### Round-21 …` | 75 | 4 tools, `c2-contract.json`, `f5/receipt.json`, 3 knowledge pages, `QUALITY43-44/45`, `S028/S079/S082-S085` | 8 (+SOURCES by row id) | 67 |

1. **`## The leg ledger` — the pin set is defensible, the drift is not.** The 14-line section names
   `tools/mutate-and-run.sh` and `corpus/knowledge/fleet-kill-rate-ledger.md`; both are pinned, so
   the set is *sound*. `corpus/SOURCES.md` is pinned for a transitive reason: the named page cites
   rows `S003`, `S048`, `S061`. But the round's edit to `SOURCES.md` is the new `S280` row (GNU
   error-message formatting), which no row in this section's chain touches. So this section's
   re-read is **not evidence-driven**: it is the coarseness of whole-file pins, not a change in
   anything the section asserts. 28 of its 30 pins are neither named nor in its chain.
2. **`### Gate/probe registry` — one pin is exactly right; the other 115 are noise.** The drifted
   input, `tools/repeat-control.py`, is the tool the row documents and whose verdict map the row
   asserts ("0 clean; 1 failed; 2 and 64 could-not-evaluate"). The C0 edit gave the tool a
   `ScratchRootUnusable` class on stderr with exit 2 — a genuine change to a claim in this section,
   and the re-read is owed. It is owed for 9 files, not 124: the other 115 are round-12 sweep
   artefacts that no re-read of this row is about.
3. **`### Round-21 …` — two of the four drift causes are not this section's inputs.**
   `corpus/QUALITY.md` is cited by line (`QUALITY43-44`, `QUALITY45`) — pinning it is right and is
   the only thing that keeps a line-number citation honest. `corpus/SOURCES.md` is cited by row id
   (`S028/S079/S082-S085`) — right in kind, coarse in form (an append anywhere drifts it).
   `tools/registry-check.py` and `tools/registry.json` are **not named** by this section: the row
   set is `env-diff.py`, `wave-route-mix.py`, `round21-measure.py`, `wave-accounting.py`. Two of
   the section's four drift causes are therefore exposure it does not carry, and the pin set gives
   them the same standing as the two it does.

**Right input set, if the binder had to name one**, per section: the commands/anchors/pages the
section's text names, plus the source rows it cites — 2 pins, 9 pins, ~12 pins respectively. That
is what the credit rule's own §2 asks for ("what a step used"), and it is what the wave-1 spec
for the SKILL.md edit assumed ("inputs are the files its commands/anchors name").

## 4. `PIN`, and the trap this round sets

`binder.py` usage: `PIN` is "the revision whose bytes the entries' inputs are pinned at (>= C0: it
carries the round's record edits, which readers do not read)". For round 55 that premise is false:
the post-C0 edits this round has already adjudicated are edits to *pinned content*, not to records.
`integrate/resolutions.json` commits to fixing, at C1:

- `W2-TOOLDIFF-F1` → `tools/context-capture.py`, `tools/registry-check.py`
- `W2-TOOLDIFF-F2`, `-F6` → `tools/registry-check.py`
- `W2-TOOLDIFF-F3` → `tools/registry.json` ("each cell now quotes the token its tool actually
  prints")

All four are still unfixed at C0, verified on the C0 clone (`repro.log §6`):

```
tools/repeat-control.py --selftest   rc=2  repeat-control: could-not-evaluate: …
tools/bash-witness-study.py selftest rc=2  WITNESS_STUDY: could-not-evaluate: …
tools/registry-check.py --selftest   rc=2  registry-check: could-not-evaluate: …
tools/env-diff.py --selftest         rc=2  ENVDIFF_SETUP: could-not-evaluate: …
bash-witness-selftest   cell=bash-witness-study.py:  actual=WITNESS_STUDY:    FALSE
registry-check-selftest cell=registry-check.py:      actual=registry-check:   FALSE
repeat-control-selftest cell=repeat-control.py:      actual=repeat-control:   FALSE
env-diff-selftest       cell=env-diff.py:            actual=ENVDIFF_SETUP:    FALSE
context-capture --selftest 2>/dev/full rc=1        (F1 owed: must be 2)
registry-check --rev --json stdout bytes=0         (F2 owed: must emit the report)
```

Consequence, measured (`repro.log §7`): **13 of the 18** re-keyed sections pin one of those three
files, so with `PIN = C0` and the C1 fixes landed, the floor returns to at most 51/64 at the
deciding revision — the 18 re-reads would have bought nothing for 13 of them:

```
 42 pins  ## Context gate classification …        [registry.json, context-capture.py]
 42 pins  ## Effective expectation …              [context-capture.py]
 78 pins  ## Live-tree re-pin …                   [registry.json, context-capture.py, registry-check.py]
7702 pins  ## Mutation-sweep recipe …             [registry.json, context-capture.py, registry-check.py]
2497 pins  ## Standing rules                      [registry.json, context-capture.py, registry-check.py]
  11 pins  ## The operator's runbook …            [registry.json]
  38 pins  ### Round-15 gate/probe registry       [context-capture.py]
  51 pins  ### Round-17 gate/probe registry …     [registry.json, context-capture.py, registry-check.py]
  71 pins  ### Round-18 gate/probe registry …     [registry.json, registry-check.py]
  75 pins  ### Round-21 gate/probe registry …     [registry.json, registry-check.py]
  74 pins  ### Round-26 gate/probe registry …     [registry.json, context-capture.py, registry-check.py]
  39 pins  ### The service's limits …             [registry.json, context-capture.py, registry-check.py]
  89 pins  ### Triggers T1–T3 and the re-pin rule [registry.json, context-capture.py, registry-check.py]
EXPOSED=13/18
```

`PIN = C1` is not the fix: it would write shas for bytes read by nobody (the readers read C0), which
is the exact hole the input-keyed rule exists to close. The honest sequence is: bind at `PIN = C0`,
then re-read those 13 headings once the C1 edits are committed (a second reader pass at the C1
bytes), or land the C1 fixes *before* readers read and re-base `cand`. Anything else is credit for
bytes that were never the state any seat checked.

## 5. The DROP list for THIS round

Current: `LOG.md`, `SCORECARD.md`, `SKILL.md`, `.ufo/evidence/round-21/coldread/ledger.json`
(`binder.py:48`) — i.e. the files that change every round by construction and the two self-outputs
(the section sha keys `SKILL.md`; the ledger is the output). That list is right, and **nothing
should be added from the drifted set**. Counterfactual measured (`repro.log §7b`, over the 17
input-drift headings):

```
DROP+corpus/SOURCES.md                      frees  3 of 17: Pin disposition …, The leg ledger, Round-13 …
DROP+corpus/QUALITY.md                      frees  0 of 17
DROP+tools/registry.json                    frees  1 of 17: The operator's runbook …
DROP+{context-capture,registry-check}.py    frees  1 of 17: Round-15 …
DROP+tools/repeat-control.py                frees  1 of 17: Gate/probe registry
DROP+<all nine changed files>               frees 17 of 17
```

Adding `SOURCES.md` because it is append-only would hand three sections credit without a read, for
a row (`S280`) that has nothing to do with them; adding the changed set hands out 17 of 17. The
cost the round actually wants to remove (whole-file pins drifting on appends) needs a schema that
can pin a *row* (`corpus/SOURCES.md#S280`) or a per-section cited-input closure — a ledger/measure
change, not a DROP entry, and not this round's.

Two DROP-adjacent things do need changing, and neither is a list entry:

1. **`HEADINGS` is not bound to anything.** `binder.py:49` reads
   `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` from the *live working tree*.
   `git cat-file -e C0:<that path>` → **rc=128** (the file does not exist at C0); it was added at
   `4f7a704` (F5), i.e. after the freeze pointer `133b2ce`; `contract.frozen_paths` (8 entries)
   does not list it (`repro.log §8`). The obligation the whole wave serves is an unfrozen,
   post-freeze, hand-authored file. Its content is right (I derived the same 18 independently), so
   the fix is to bind it — freeze it, or derive it inside the binder from C0 — not to re-author it.
2. **`RES` is the wrong file.** `binder.py:50-54` expects round-54's shape
   (`{heading, n, kind, reader, routed, findings[]}`, 12 items) to learn how many adjudicated
   findings each heading may carry. Round-55's `integrate/resolutions.json` is 21 items with keys
   `{decision, evidence, finding, from, id}` — no `heading`, no `n` — and the committed binder
   **dies at import** on it (`KeyError: 'n'`, `binder.py:54`; `repro.log §2`). If it were
   "fixed" by emptying `RES`, `allowed = RES.get(h, 0)` = 0, so any reader with findings is
   skipped: the round's 21 accepted dispositions could never unblock a findings-bearing reader.
   The binder's adjudication input must be re-specified for this round, in this round's schema.

## 6. Findings by severity

**F1 (blocker) — the binder cannot run on this round's tree.** `integrate/resolutions.json` is a
dispositions list, not the per-heading findings budget; `binder.py:54` raises `KeyError: 'n'`.
Receipt: `repro.log §2` (schema dump of both files + the traceback). Effect: as committed, the
re-key produces nothing; and the schema does not even express what round 54's file expressed.

**F2 (blocker) — `PIN` cannot absorb this round's C1 edits, and `PIN = C1` would launder them.**
13/18 re-keyed sections pin `tools/registry.json`, `tools/context-capture.py` or
`tools/registry-check.py`, all three of which the round has already decided to edit at C1 and all
three of which are still unfixed at C0 (4/7 registry cells false; F1 `rc=1`; F2 0 bytes).
Receipt: `repro.log §6`, `§7`. Required: `PIN = C0`, plus a documented second read pass for those
13 headings after C1 (or C1 fixes moved before the reader `cand`).

**F3 (high) — the union policy is the wrong input set, and it ratchets.** 11,188 pins over 18
headings; 28/115/67 unnamed pins in the three attacked sections; 7,702 pins for one heading whose
round cause is 6 files. Because the union contains the previous re-key entry, each round's pin
surface is monotone non-decreasing, so every future edit to any of those 11,188 files re-forfeits a
section. Receipt: `repro.log §4`, `§5`, `§7`; `04-three-input-sets.json`.

**F4 (high) — the written trace is false provenance.** For each re-keyed section the binder writes
`traces/section-NN.json` with `argv = [python, binder.py, LANE, C0, PIN, OUT, 'section', H]` (no
such subcommand exists in `main()`), `exit: 0` (the run returned **1**),
`rev_reason: "… no live working-tree reads"` (the binder reads `HEADINGS` and `RES` from the
working tree), and `inputs` = the full union (30/124/75) rather than anything a read opened. The
round-21 trace gate only checks `trace.inputs ⊆ entry.inputs`, so all of it passes. Inherited and
already load-bearing: 23 such entries exist at `read_rev 99c3bc88d704…` from round 54, and **5 of
the 46 credited sections** credit only through one of them (`### The boundaries — what a service run
is not`, `### Using the ledger`, `### The tick and the pin read`, `### The operator's runbook —
… operator-runbook.md`, `### Round-14 historical registry — superseded by round 15`). Receipt:
`repro.log §3` + the entry/trace dump in the seat scratch (`out/traces/section-08.json`).

**F5 (medium) — the heading list is unfrozen and absent at C0** (see §5.1). Receipt: `repro.log §8`
(`rc=128`, add-commit `4f7a704`, `lost-headings frozen? False`).

**F6 (low) — three observable-contract slips in the binder.** (a) docstring line 15 says reader
reports come from `.ufo/waves/round-55/w1/*.json` while `WAVE_DIRS` is `w2`,`w3` — a reader landed
in `w1` is silently ignored; (b) the entry's `seats` field is stamped
`'L1 TameshiR55a2 re-key (round 54)'`; (c) `commands_executed_count = 1 + len(inputs)` (31/125/76
for a read that ran one command), which the ledger's command-count fields and any consumer of them
inherit. Receipt: `repro.log §3`, `§8`, `§4`.

**F7 (confirmation, not a new find) — the C1 drift F2 rests on is wave 2's, and it is real.**
`W2-TOOLDIFF-F3` is independently confirmed: 4 of the 7 `scratch_root` cells are false at C0
against the first token each tool prints. It matters here because it is the mechanism by which 11
of the 18 pins move at C1.

## 7. Residual risk and verification gaps

- My lost-set replay (`derive.py`) reproduces the counter's own verdict (`46/18`, set-equal) but
  does not run the round-21 measure end to end (it is slow: 591 entries × historical inputs); the
  trace gate is therefore *not* re-evaluated by my script. That gate cannot change the lost set
  here (a trace's inputs are a subset of its entry's). `repro.sh` is the runnable form.
- The binder run in `repro.sh` uses a one-line scratch-only adaptation (tolerate the round-55
  resolutions schema). No lane file was edited; the adaptation is visible in `repro.log §3`.
- Whether the C1 edits actually land is a plan, not a fact: F2 is a prediction conditioned on
  `integrate/resolutions.json` being honoured. If the L1 instead drops those dispositions, the
  round keeps 4/7 false registry cells and two open crash paths — the C2 claim's surface.
- I did not test the second-pass replacement rule with two different `OUT` dirs; from the code
  (`binder.py:187-191`) a second pass lands a *second* entry unless the trace prefix matches
  exactly, which would double-pin rather than re-pin.
- `PACMAN`/tooling: nothing needed installing; no install was performed.

## 8. Artifacts opened

`.ufo/evidence/round-54/integrate/binder.py` (all 212 lines), `binder.py` and
`resolutions.json` in `.ufo/evidence/round-55/integrate/`, `.ufo/evidence/round-55/contract.json`,
`c1/lost-headings-at-c0.json`, `.ufo/evidence/round-18/measure.py` (`sectionize`,
`input_failure(s)`, `input_reason`, `entry_reason`, `coldread`, `IGNORED_INPUTS` at :135),
`.ufo/evidence/round-21/coldread/measure.py`, `.ufo/evidence/round-21/coldread/ledger.json` at C0
(591 entries), `SKILL.md` at C0 (64 sections), `corpus/knowledge/input-keyed-coldread-credit.md`,
`corpus/QUALITY.md` and `corpus/SOURCES.md` diffs base→C0, `tools/registry.json` (7 cells),
`corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/waves/round-55/spec-w1.json`/`spec-w3.json`
(T55W3RevBinderInputs item), wave-1 reports `T55W1ExecReKeyDryBind.md`, `T55W1ExecRekeyPrep.md`.

Receipts: `.ufo/waves/round-55/w3/T55W3RevBinderInputs-receipts/{repro.sh,derive.py,repro.log,04-three-input-sets.json}`.
Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W3RevBinderInputs/` (clone is `--shared`; the lane was
read with `git show`/`cat-file` only).
