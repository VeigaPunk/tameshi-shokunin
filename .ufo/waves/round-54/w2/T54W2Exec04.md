# T54W2Exec04 — precheck + census at C1, and what the RED does and does not mean

- Round 54 (hyaku run 11), wave 2; L1 `TameshiR54a2`.
- Item: run and record the frozen round-48 precheck and the fleet census at C1; paste both last
  lines; explain why the precheck is expected RED before the re-key.
- Axes: calibration, operability. Milestone: **verify C1**.
- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (all paths absolute).
- Revisions: C1 `99c3bc88d704566197783f66b211ee0a830e0330`; precheck FLOOR
  `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`; worktree HEAD at read time
  `097985c18b9a186c310bd35890b95b733cbb7f5b` (C1 + 4 commits; `SKILL.md` byte-identical
  between C1 and HEAD — `git diff --stat C1 HEAD -- SKILL.md` is empty).
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Exec04`.
- Read-only on the lane: every lane file was opened with `read` / `git show` / `git ls-tree`; the
  only writes are this file and `T54W2Exec04-receipts/` under `.ufo/waves/round-54/w2/`.
- Tooling: nothing installed or upgraded (no `uv`/`npx`/binary fetch was needed; pacman is paused
  host-wide and was not used).

## 1. Frozen precheck at C1 — **RED, exit 1**

Command (exactly as assigned):

```sh
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/quality/coldread-precheck.sh \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 \
  99c3bc88d704566197783f66b211ee0a830e0330
```

`exit=1`; stdout is 24 lines (23 `LOST` + verdict), stderr empty. Full stdout
(retained at `T54W2Exec04-receipts/precheck-c1.stdout`):

```
LOST ## Context gate classification and explicit exit classes — round 15 | drifted=corpus/SOURCES.md,tools/bash-witness-study.py,tools/context-capture.py,tools/evidence-disposition.py,tools/mutate-and-run.sh,tools/pin-disposition.py,tools/registry.json,tools/trace-inputs.py
LOST ## Effective expectation reconciliation — round 14 | drifted=
LOST ## Live-tree re-pin and entry-command monitor — round 17 | drifted=
LOST ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence | drifted=
LOST ## Pin disposition and provenance correction — round 13 | drifted=
LOST ## Repeated controls and gate registry — round 12 | drifted=
LOST ## Standing rules | drifted=
LOST ## The leg ledger — replay, receipt, and how it is read (round 7, measured) | drifted=corpus/SOURCES.md
LOST ## The operator's runbook and the six-leg regression (round 10, measured) | drifted=tools/registry.json
LOST ### Gate/probe registry | drifted=tools/bash-witness-study.py
LOST ### Round-13 gate/probe registry | drifted=corpus/SOURCES.md,tools/bash-witness-study.py,tools/pin-disposition.py
LOST ### Round-14 historical registry — superseded by round 15 | drifted=tools/bash-witness-study.py,tools/evidence-disposition.py,tools/trace-inputs.py
LOST ### Round-15 gate/probe registry | drifted=
LOST ### Round-17 gate/probe registry — re-pin and monitor | drifted=
LOST ### Round-18 gate/probe registry — routed-defect closure | drifted=
LOST ### Round-21 gate/probe registry — finite environment differential | drifted=.ufo/evidence/round-15/verify.py,corpus/QUALITY.md,corpus/SOURCES.md,tools/env-diff.py,tools/registry-check.py,tools/registry.json
LOST ### Round-26 gate/probe registry — report interop | drifted=
LOST ### The boundaries — what a service run is not | drifted=
LOST ### The operator's runbook — `corpus/knowledge/operator-runbook.md` | drifted=
LOST ### The service's limits — what tameshi refuses to mutation-test | drifted=
LOST ### The tick and the pin read | drifted=tools/pin-disposition.py
LOST ### Triggers T1–T3 and the re-pin rule | drifted=corpus/QUALITY.md,corpus/SOURCES.md,corpus/knowledge/service-limits.md,tools/bash-witness-study.py,tools/evidence-disposition.py,tools/pin-disposition.py,tools/registry-check.py,tools/registry.json
LOST ### Using the ledger | drifted=
```

Last line:

```
COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=99c3bc88d704 cand_credited=41 lost=23 RED
```

Reproduced at HEAD too, same counts: `... cand=097985c18b9a cand_credited=41 lost=23 RED`
(exit 1) — nothing between C1 and HEAD changed this state.

## 2. Fleet census — **ok, exit 0**

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin tameshi
```

`exit=0`; 17 stdout lines = 16 advisory rows + 1 `ok` row (retained at
`T54W2Exec04-receipts/census.stdout`).

Last line:

```
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Source table: 139 rows, `S001`..`S279` (regex `^\|\s*S[0-9]{3,}\s*\|`), identical count on the
`corpus/SOURCES.md` blob at C1 (139), so the census audits the same table the round ships. The 16
advisory rows are 15 × `W04 duplicate url … across scopes` and 1 × `W01 S101 tierC mined
used-by=corpus/knowledge/witness-equivalence-rule.md`; per the script these are advisory and do
not affect exit status.

## 3. Why the precheck is expected RED before the re-key

The precheck's own contract is a *pre-freeze* gate: it is run on a candidate **before** that
candidate is frozen as the deciding revision, and it names every section that lost cold-read
credit plus the input paths that drifted. At C1 that is exactly what it reports, for two
mechanical reasons, and neither is evidence against C1:

1. **The ledger is keyed by the section's own bytes.** `round-18/measure.py` indexes entries by
   `entry['sha256']` and matches a section with `by_sha.get(sec['sha256'])`
   (`round-18/measure.py:610-612`); an entry's `sha256` is the hash of that section at its
   `read_rev`. The C1 fix pass rewrote SKILL.md (diff stat: 60 changed lines), so **14** sections
   now carry a `sha256` that no ledger entry holds → `no-ledger-entry`. Byte-level example:
   `## Standing rules` at C1 has `section_sha256
   61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc`
   (`reader-section.py` output) while the only ledger entries for that heading carry
   `976cffc976563a9a39721520596faf3b431dca333f93a602ce9dcc3286092969` (older read_revs) and
   `d3880242962e1b192647eff32ff056cc5efb454a98a3b36219291b4c795e7417` (`read_rev
   651773ab9e32…`, the round-53 re-key) — no C1 sha, so no match is possible.
2. **Nine sections kept their bytes but their pinned inputs moved.** Where the section sha still
   matches an entry, the entry pins lane files that the C1 pass edited — `tools/bash-witness-study.py`,
   `tools/context-capture.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`,
   `tools/pin-disposition.py`, `tools/trace-inputs.py`, `tools/registry.json`,
   `tools/registry-check.py`, `tools/env-diff.py`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
   `corpus/knowledge/service-limits.md`, `.ufo/evidence/round-15/verify.py` — so the entry fails the
   round-18 input gate (`git cat-file` sha256 must equal the recorded value) and is reported
   `input-drift:<p>`.

`c1/measure.py`'s own `--explain` run at C1 reproduces the split exactly and shows that the
restoration mechanism does not exist yet:

```sh
python3 .../round-54/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 99c3bc88d704566197783f66b211ee0a830e0330 --work <empty> --explain
```
```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=99c3bc88d704 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=99c3bc88d704 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```
(retained at `T54W2Exec04-receipts/c1-measure-at-c1.stdout`.)

So: **14 `no-ledger-entry` + 9 `input-drift` = 23 lost; 64 − 23 = 41 credited** — the numbers the
precheck prints. `git ls-tree -r --name-only C1 .ufo/evidence/round-21/coldread/` contains only
`rekey-r53-651773ab9e32`, `rekey-r53-a41195dfc13a`, `rekey-r53-a9773948087e`; a `rekey-r54-*`
directory exists at neither C1 nor HEAD (count 0). The re-key commit is the artifact that supplies
fresh entries bound at `<c0>`, with `read_rev` `<c0>` and inputs re-hashed at C1; until it is
committed, the round-21 selector has nothing to credit, so a RED precheck is the **expected
pre-re-key state**, and the claim's deciding revision is the later commit that carries the re-key
and the reader reports — not C1.

## 4. Cross-check: the 23 lost sections *are* the 23 wave-2 reader headings

Computed set equality over `spec-w2.json`'s 23 `T54W2Read*` items and the 23 uncredited headings
at C1:

```
readers 23 lost 23
readers-lost []
lost-readers []
EQUAL True
```

That is the calibration statement available at C1: the RED count is not a loose number — it is
exactly the section set the round budgeted to re-read, so a RED of any other size would mean the
reader scope was wrong.

## 5. Findings for L1 adjudication (frozen instrument, C1 counter)

### F1 — arm 4 reads the superseded wave, and the round's deliverable wave is excluded

`c1/measure.py` (frozen; `freeze.json` `files["c1/measure.py"] =
63f5f88147b898ee795dc925a04668d473c1fc845e370947307e3ea141a0b77b`, equal to the current bytes):

```
25:               `.ufo/waves/round-54/w1/*Read*.json` names the heading, pins
53:WAVE = '.ufo/waves/round-54/w1'
223:        if not re.search(r'/T54W\d+.*Read.*\.json$', path):
```

Arm 4 requires `d.get('cand') == c0` where `c0` comes from the re-key directory (arm 3), i.e. C1
in this round. Measured:

- All **23** committed `.ufo/waves/round-54/w1/T54W1Read*.json` pin
  `"cand": "59c38109bf119d0e9d4f878644a82babc937bc1e"` (C0) — histogram `{C0: 23}`. Example
  `w1/T54W1Read01.json` for `## Standing rules`: `section_sha256
  164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7` (C0 bytes) vs the C1 sha
  `61736dce…` above. Simulating arm 4's predicate over the w1 set gives **0 / 7** frozen
  headings satisfied.
- The wave-2 deliverables, which the wave context routes to
  `.ufo/waves/round-54/w2/<seat>.json`, are already C1-shaped: of the 17 `T54W2Read*.json`
  present at read time, 15 pin `cand = 99c3bc88…` with the exact C1 section sha; the 16th was
  still being written; the 17th is a peer mid-flight. Simulating the same predicate over the w2
  set gives **3 / 7** and rising (waves still in flight). `WAVE` excludes that directory.
- At C1 there is no `w1/` tree at all, so arm 4 is trivially 0/7 there; at HEAD the tree exists
  with 23 files but the `cand` is C0, so it is still 0/7 once `c0` = C1.

Consequence: with `WAVE` and the reports pointing at different waves, arm 4 cannot reach 7/7 from
this round's deliverables, and `C1_R54_PASS` stays false on arm 4 alone. The decision belongs to
the L1, before the single deciding invocation: either (a) an amendment to `WAVE` (the regex at
line 223 already matches `T54W2Read*.json`), which requires re-hashing `c1/measure.py` in
`freeze.json` and re-freezing, or (b) committing the wave-2 JSONs under
`.ufo/waves/round-54/w1/` as well. No production file was touched by this seat.

### F2 — arm 3's frozen list is 7, arm 1 needs all 23

`c1/lost-headings-at-base.json` freezes **7** headings and arm 3 requires exactly those 7 re-keyed
under `rekey-r54-<c0>`. Arm 1, and the contract's target sentence, require `cand_credited=64
lost=0`. At C1 there are **23** uncredited sections, so a re-key scoped to the frozen 7 (or to the
6 of them that are `no-ledger-entry`; `### Round-14 historical registry` is the seventh and is
currently `input-drift`) satisfies arm 3 while leaving 16 uncredited → arm 1 RED, arm 2
`covered<64`. A re-key that covers all 23 (each with inputs re-hashed at C1 and `read_rev` set to
`<c0>`) satisfies both, because round-18 aggregation lets a fresh crediting entry outrank the
stale/drifted ones (`covered = credited > 0 and not vetoes`; drifted entries are stale and do not
veto). Binding note for the deciding run, not a counter defect.

## 6. Artifacts opened

- `.ufo/evidence/round-48/quality/coldread-precheck.sh` (whole file: usage, FLOOR/CAND comparison,
  RED condition `len(cand_credited) < len(floor_credited)`).
- `.ufo/evidence/round-54/c1/measure.py` lines 1-143 and 144-259 (all five arms, verdict line,
  `WAVE`, `REKEY_RE`, arm-3 directory discovery, arm-4 reader predicate).
- `.ufo/evidence/round-18/measure.py` lines 30-110 (credit rule v2: shape, class gate, commands
  gate, input gate, trace gate, fail-closed aggregation) and 590-650 (section→entry matching by
  `sha256`, `no-ledger-entry`, veto logic).
- `.ufo/evidence/round-21/coldread/measure.py` (selector wrapper; default ledger path, override
  refusal).
- `.ufo/evidence/round-54/contract.json` (C1/C2 claims, targets, counters, kill rules, frozen
  paths, amendments).
- `.ufo/evidence/round-54/c1/lost-headings-at-base.json` (7 frozen headings).
- `.ufo/evidence/round-54/deciding-run.sh` (freeze-integrity gate, the BASE-vs-REV precheck call,
  the per-counter start/exit receipts, clean-tree and second-invocation gates).
- `.ufo/evidence/round-54/freeze.json` (`files["c1/measure.py"]` digest).
- `.ufo/waves/round-54/spec-w2.json` (23 reader items, their headings, the w2 deliverable path).
- `.ufo/evidence/round-21/coldread/ledger.json` (568 entries; `## Standing rules` entry shas and
  `read_rev`s; `### The tick and the pin read` entry inputs).
- `.ufo/waves/round-54/w1/T54W1Read*.json` (23 files; `cand` histogram) and the in-flight
  `.ufo/waves/round-54/w2/T54W2Read*.json` (17 files at read time).
- `corpus/SOURCES.md` at C1 and in the worktree (row census).
- `git log`/`git ls-tree`/`git diff` at C1 and HEAD.

## 7. Commands run (all read-only)

| # | command | exit |
|---|---|---|
| 1 | `bash .../round-48/quality/coldread-precheck.sh LANE ef19d8e1e7ba 99c3bc88d704` | **1** (RED) |
| 2 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | **0** (ok) |
| 3 | same precheck with CAND=`097985c18b9a` (HEAD) | **1** (RED, same counts) |
| 4 | `python3 .../round-54/c1/measure.py --lane LANE --rev 99c3bc88d704 --work <empty> --explain` | **1** (C1_R54_PASS=false) |
| 5 | `python3 .../round-21/coldread/measure.py --repo . --rev 99c3bc88d704 --explain` | 0 (41/64, score 6) |
| 6 | `python3 .ufo/waves/round-54/reader-section.py LANE 99c3bc88d704 '## Standing rules'` | 0 (`section_sha256 61736dce…`) |
| 7 | `git ls-tree`/`git show`/`git log`/`git diff` at C1 and HEAD; ledger and reader-JSON histograms | 0 |

## 8. Retained evidence

`T54W2Exec04-receipts/` (raw bytes):
`precheck-c1.stdout` (24 lines), `precheck-c1.stderr` (empty), `census.stdout` (17 lines),
`census.stderr` (empty), `c1-measure-at-c1.stdout` (4 EXPLAIN lines + verdict).

## 9. Limits

- The census audits `corpus/SOURCES.md` only; it says nothing about the scratch-root exit class, so
  the operability axis is untouched by this item beyond confirming the census is green.
- The precheck measures credit, not fairness of any reader judgment (the contract's own
  `cannot_see`), and it runs the ledger at C1, where the re-key by design does not exist yet.
- F1/F2 are instrument/scope observations with commands and outputs above; adjudication and any
  re-freeze are the L1's, and nothing here changes the lane.
