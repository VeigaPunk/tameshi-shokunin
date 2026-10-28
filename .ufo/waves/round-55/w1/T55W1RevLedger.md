# T55W1RevLedger — the ledger machinery the round-55 re-key will use

Seat **T55W1RevLedger** (leaf, reported to L1 `TameshiR55`). Judged on
**calibration**. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; frozen
base `631cd6455e58dce969310b4c0466c3383d9f5108`; contract base
`0a2010acd1e92e4e332774050825e21bcfc7e079`.

Item: read the round-18 credit rules (`round-21/coldread/measure.py` →
`round-18/measure.py`) and the round-54 re-key binder (`round-54/integrate/binder.py`);
report **what exactly makes a section credit**, **which inputs the binder drops and
why**, and **whether a reader report with an empty findings list is accepted or
silently ignored**; then state **the minimal reader JSON for `## Standing rules`
and the exact binder arguments**, verified against the code.

I edited **no** lane file. Every experiment ran in a scratch clone under
`/fast/scratch/hyaku/tameshi-r55/T55W1RevLedger/`, `git -C <clone> rev-parse
--show-toplevel` was asserted equal to the clone before every commit there, and no
mutating git command ran against the lane. Receipts:
`.ufo/waves/round-55/w1/T55W1RevLedger-receipts/`. **No tool was installed** (git,
python3 stdlib only); no pacman/uv/npx/cargo call ran. Sources census conformance at
audit time: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → exit 0, `ok` on the lane file (140 rows in
`corpus/SOURCES.md`, S001 upward).

## 1. Answer

### 1.1 What makes a section credit — the reader report is not one of the inputs

Three artefacts are commonly assumed to gate credit. Only one does.

| artefact | gates credit? | evidence |
|---|---|---|
| the section bytes at the measured revision | **yes** — it is the key | `round-18/measure.py:209` (sectionize), `:602-612` (entries indexed by `entry['sha256']`), `:655` |
| the ledger **entry** (`verdict`/`class`/`counts`/`inputs`/`traces`) | **yes** — six gates | `:459-527`, `:330-353`, `:373-457` |
| `read_rev` | **no** — never read | `grep -n read_rev round-18/measure.py` → only the overlay field list (`:139`), help text (`:1532`) and self-test fixtures (`:831,1347,1350`). Probe: `entry_reason(..., read_rev='nonsense')` → `None` |
| the reader report (`*.json` under `.ufo/waves/…`) | **no** — the credit rule never opens it | no `reports`/`seats` logic anywhere in `round-18/measure.py` (`grep -n reports` → docstrings only). The entry's `reports`/`seats` fields are written by the binder and validated by nothing |

Measured on a real crediting entry of the lane at `631cd64` (`field-insensitivity.txt`,
one mutation per line, `entry_reason(..., strict=True)`):

```
baseline          None                 # credits
bogus start/end   None                 # start=999, end=999 -> still credits
bogus heading     None                 # heading='### nonsense' -> still credits
bogus read_rev    None                 # read_rev='nonsense' -> still credits
bogus skill_sha   None                 # skill_sha256='f'*64 -> still credits
bogus reports     None                 # reports=['nope/none.md'], seats=['nobody'] -> still credits
no traces         traces-unrecorded    # the trace gate is the one field that bites
```

`start`, `end`, `heading` and `skill_sha256` are therefore **informative only**;
the enforced rev-binding is the section sha256 plus the input digests plus one
committed trace.

The credit rule, in order, for every section the frozen sectionizer finds in
`SKILL.md` at REV:

1. **Keying.** `by_sha[entry['sha256']]` (`:602-612`). Matching is by **section
   sha256 alone** — not by heading, not by `start`/`end`, not by
   `skill_sha256`. Probe: an entry whose `skill_sha256` was set to `f`*64 still
   returns `entry_reason → None`; the same for a bogus `start`/`end`.
   The section body is: heading line through the line before the next
   `^#{1,3}(\s|$)` heading outside ``` fences, trailing whitespace-only lines
   stripped, `\n`-joined, no trailing newline, sha256 over the `surrogateescape`
   bytes (`:209-255`).
2. **Findings/shape** (`entry_failure`, `:459`): `verdict` ∈ the six strings;
   not in `{gap-blocking, wrong-expectation, not-executed}`; `blocking_gaps == 0`
   and `wrong_expectations == 0` as JSON ints (bools/strings → `malformed-entry`).
3. **Class gate** (`entry_credit_reason`, `:477`): `class == instruction` → verdict
   ∈ `{executed-ok, gap-minor}` **and** `commands_executed_count >= 1`;
   `class == record` → verdict ∈ `{verified-record, gap-minor}`.
4. **Commands gate** (`:513-527`): `commands_executed_count > 0` for every class
   (`commands-unrecorded` otherwise).
5. **Input gate** (`input_reason`, `:330-353`): `inputs` **minus** `IGNORED_INPUTS`
   must be non-empty; every remaining key canonical lane-relative (no leading `/`,
   no `./`, no empty/`.`/`..`/`.git` component, no NUL); `git ls-tree REV -- p`
   must name exactly one entry with mode `100644`/`100755`; and
   `sha256(git cat-file blob REV:p)` must equal the recorded value.
   At runtime `IGNORED_INPUTS` is `{SKILL.md, .ufo/evidence/round-17/coldread/ledger.json,
   .ufo/evidence/round-18/coldread/ledger.json, .ufo/evidence/round-21/coldread/ledger.json}`
   — the last is added by the round-21 wrapper (`round-21/coldread/measure.py`, the
   `IGNORED_INPUTS |= {LEDGER}` statement).
6. **Trace gate** (`trace_reason`, `:373-457`, strict mode = no override flags):
   at least one committed trace; each trace is a blob at REV whose schema is
   `tameshi-trace-inputs-v1`, whose `inputs` are a **subset** of the entry's inputs
   with equal digests, whose `external` names no unbound path under the live lane
   root, and whose `live_lane_reads` are bound to REV.
7. **Aggregation** (`:612-655`): a section is covered iff **≥1 entry credits AND
   no veto-eligible entry exists whose inputs still verify at REV** (a failing
   entry whose inputs have drifted is stale and does not veto; one with
   absent/empty inputs does veto).

So for `## Standing rules` the binding question is: *does a ledger entry exist
whose `sha256` equals the current section body's sha, whose six gates pass at the
deciding revision, whose `inputs` all still hash to their recorded values there,
and whose one trace is committed there?* Nothing else.

`read_rev` is documentary. The binder writes `read_rev = C0`, and the honest
reason to keep it accurate is auditability, not credit.

### 1.2 Which inputs the binder drops, and why

`binder.py:49`:

```python
DROP = ('LOG.md', 'SCORECARD.md', 'SKILL.md', '.ufo/evidence/round-21/coldread/ledger.json')
```

applied at `:140-147` while unioning the heading's prior entries' inputs:

| dropped path | why (code + measured consequence) |
|---|---|
| `LOG.md`, `SCORECARD.md` | They are rewritten every round **after** the bind. The input gate verifies every recorded digest **at REV**, so keeping them makes the fresh entry stale at the next record commit — the round-53 failure mode named in the binder docstring. Proven by counterfactual: with a `DROP` lacking `SCORECARD.md`, a post-pin `SCORECARD.md` edit yields `entry_reason = 'input-drift:SCORECARD.md'` and the section is uncovered (48/64 vs 49/64 in the fixture). With the shipped `DROP`, the same edit leaves 64/64 (`rekey-all18.stdout`, last line). |
| `SKILL.md` | The page the section is cut from; its per-section sha **is** the ledger key, and the credit rule already lists `SKILL.md` in `IGNORED_INPUTS`. Dropping it here keeps the stored `inputs` honest about what the gate actually verifies. (The docstring says "SKILL.md's ignored status left to the credit algorithm" while the code also drops it — harmless, but the comment and the constant disagree.) |
| `.ufo/evidence/round-21/coldread/ledger.json` | The binder's own output; also in `IGNORED_INPUTS`. Recording it would be self-reference. |

Two further exclusion paths, not named by `DROP`:

* **Absent at PIN** (`:143-146`): `blob_at(pin, p) is None` → the path is appended
  to `dropped` and left out. This is how renamed/deleted historical inputs fall
  away silently; `dropped=0` in every round-54/55 run so far.
* **First-writer-wins** (`:141`): `if p in inputs … continue` — the union keeps the
  digest of the **first** prior entry that lists a path, but since every retained
  path is re-hashed from the PIN blob (`:146`) the recorded value is always PIN's,
  never a stale prior entry's.

Everything else survives. For `## Standing rules` that is **2,497 paths** (prior
union 2,500 minus the three dropped record files; the ledger never appears in the
union). They include `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/*.py`,
`tools/registry.json`, and ~2,000 historical `.ufo/waves/**` / `.ufo/evidence/**`
files. **All 2,497 must still hash to their PIN values at the deciding revision.**
This is the whole risk surface, and §2 shows it is not hypothetical.

### 1.3 Is a reader report with an empty findings list accepted? Yes — and so is one with no `findings` key at all

`binder.py:114-131`:

```python
for f, d in readers.get(h, []):
    if d.get('cand') != c0 or d.get('section_sha256') != sec['sha256']:
        continue
    findings = d.get('findings') or []
    md = Path(f[:-5] + '.md')
    if len(findings) > allowed:            # allowed = RES.get(h, 0)
        skipped.append((h, 'reader-has-findings:%d>%d' % (len(findings), allowed)))
        good = None
        break
    if not md.exists():
        skipped.append((h, 'reader-md-missing'))
        good = None
        break
    good = (f, d)
    break
```

An empty list is `0 > 0 == False` → the reader is accepted, the heading is bound,
`minor_gaps = 0`, and the verdict is carried from the newest prior entry with
failing verdicts rewritten (`:150-159`). **It is not silently ignored — it is the
happy path.** Measured (`demo.stdout`, ARM A):

```
BIND[armA] rc=0 REKEY ## Standing rules start=17 inputs=2497 dropped=0 reader=… | REFRESH rekeyed=1 skipped=0 headings=1
```

Two acceptance gaps on the same three lines, both measured (ARM C):

* **C6 — no `findings` key at all** → `d.get('findings') or []` → `[]` → **bound**
  (`rc=0 REKEY … reader=probe`). The binder cannot tell "read the section, found
  nothing" from "forgot the field".
* **C7 — reader `skill_sha256` = `f`*64** → **bound**. The binder never compares the
  reader's whole-file claim with the `skill_sha256` it derives from C0; the claim is
  discarded.
* **C8 — sibling `.md` present but zero bytes** → **bound**. Only existence is
  checked, never content.

And one refusal that is order-dependent (see F3 below): **C9** a finding-bearing
reader whose filename sorts *before* the clean one → `reader-has-findings:1>0`,
`SKIP`; **C10** the same pair with the clean one sorting first → `REKEY`.

### 1.4 The minimal reader JSON for `## Standing rules`, and the exact binder arguments

**Minimal reader JSON.** The binder reads exactly four keys and one sibling file.
Everything else (`skill_sha256`, `section`, `seat`, `method`, `checks`,
`milestone`, `axes`) is ignored by the code.

```json
{
 "heading": "## Standing rules",
 "cand": "<C0: the full 40-hex content commit>",
 "section_sha256": "<sectionize(SKILL.md at C0)['## Standing rules']['sha256']>",
 "findings": []
}
```

plus a sibling `<same stem>.md` that must exist (content unchecked).

That four-key file is not a hypothesis: a reader holding exactly those keys and a
one-line `.md` bound in the fixture —
`BIND rc=0 REKEY ## Standing rules start=17 inputs=2497 dropped=0 reader=only.reader | REFRESH rekeyed=1 skipped=0 headings=1`
(`probe2.stdout`, part 1).

Rules the code enforces on those fields:

* `heading` must equal the sectionizer's heading string **byte for byte**
  (including `## ` and any em dashes) — it is the `readers` key (`:104`) and the
  `HEADINGS` lookup (`:108-110`).
* `cand` must equal the **resolved** `C0` — `resolve()` runs
  `git rev-parse --verify <arg>^{commit}`, so `C0` may be short, but the reader's
  `cand` is compared to the resolved 40-hex string (`:118`). A 12-hex prefix in
  the reader never matches (probe C2).
* `section_sha256` must equal the section body's sha computed by the **frozen
  round-18 sectionizer extracted at C0** (`:86-93`, `:108`). A stale value is
  `no-clean-reader` (probe C3). It is *not* the sha of `SKILL.md`.
* `findings` ≤ 0 unless a `--resolutions` file grants a count for that heading
  (`RES.get(h, 0)`); with no resolutions file, **any** finding refuses the bind.
  `findings: []` (or omitted) is required for a clean read.

Derivation command (writes nothing; reads git objects at C0 only) — run it at the
commit the L1 actually lands and paste the two values:

```sh
C0=$(git -C "$LANE" rev-parse --verify '<content-commit>^{commit}')
git -C "$LANE" show "$C0:.ufo/evidence/round-18/measure.py" > "$S/r18.py"
git -C "$LANE" show "$C0:SKILL.md" > "$S/SKILL.md"
python3 - "$S/r18.py" "$S/SKILL.md" "$C0" <<'PY'
import hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location('r18', sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw = open(sys.argv[2], 'rb').read()
sec = [s for s in m.sectionize(raw) if s['heading'] == '## Standing rules'][0]
print(json.dumps({'heading': sec['heading'], 'cand': sys.argv[3],
                  'section_sha256': sec['sha256'], 'findings': []},
                 ensure_ascii=False, indent=1))
PY
```

**Exact binder arguments.** The frozen round-54 driver takes **four positional
arguments and no flags** (`binder.py:44`):

```
python3 .ufo/evidence/round-54/integrate/binder.py LANE C0 PIN OUTDIR
```

but it hard-codes the round-54 heading sources (`E = '.ufo/evidence/round-54'`,
`c1/lost-headings-at-c0.json` ∪ `lost-headings-at-base.json` at `:50-52`), the
round-54 wave dirs (`:48`) and the round-54 resolutions file (`:53`). **It cannot
be invoked unmodified for round 55**: it would re-key the round-54 heading set from
round-54 wave dirs. The L1 needs a round-55 driver; the dry-bind receipts already
carry a working one (`T55W1ExecReKeyDryBind-receipts/binder-r55.patch`,
`binder-r55.py`) adding `--headings FILE`, `--waves DIR`, `--resolutions FILE`,
`--label TEXT` after the four positionals. I re-derived the same four edits and ran
them; the invocation that works, byte-for-byte against the code, is:

```sh
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=<content commit: the SKILL.md edit and every production edit>
PIN=<the last commit touching any pinned input; see F4 — safest PIN = C0>
OUT="$LANE/.ufo/evidence/round-21/coldread/rekey-r55-${C0:0:12}"
mkdir -p "$OUT"
python3 "$ROUND55_BINDER" "$LANE" "$C0" "$PIN" "$OUT" \
  --headings "$H"                  # JSON list, exact heading strings, e.g. ["## Standing rules"]
  --waves .ufo/waves/round-55/w1   # relative to LANE; the reader *.json live here
  --label 'L1 TameshiR55 re-key (round 55)'
# then commit the ledger + "$OUT/traces/**" + the reader json/md as REV and measure at REV
```

Constraints that follow from the code, each measured:

* **OUTDIR must live inside LANE.** The trace path recorded is
  `os.path.relpath(OUT, LANE) + '/traces/section-NN.json'` (`:167-168`); a `..`
  component fails `canonical_lane_path` and the section reads
  `trace-missing:<path>`. Measured (probe 2, part 2):
  `recorded trace path: ['../outside-out/traces/section-01.json']` →
  `entry_reason = 'trace-missing:../outside-out/traces/section-01.json'`, with
  `trace blob committed inside the lane? False` — and the bind itself printed
  `REKEY …` and exited 0, so the failure is silent until the counter runs.
* **The binder writes the lane working tree**, not a commit:
  `Path(LANE, LEDGER).write_text(...)` at `:197`. The L1 must commit the ledger and
  `OUT/traces/**`; the trace blob must be readable at REV or the trace gate fails.
* **Reader discovery reads the working tree** (`glob(Path(LANE, wd, '*.json'))`,
  `:100-104`), not git objects — reader files need not be committed *before* the
  bind, but they must not be left dirty afterwards.
* **`--waves` takes exactly one directory** in the patched driver; readers split
  across w1/w2 need two passes (the second pass replaces the first entry only when
  heading + `read_rev` + trace prefix match, `:190-193`).
* **A second pass over a later PIN replaces, not grows** — same replacement key.
* **The ledger grows by the number of headings re-keyed.** Measured in the
  all-18 fixture: 591 entries at the content revision → **609** at REV (the
  `ledger-not-shrunk` monitor in `no-harm.sh` compares base to REV and is satisfied).

## 2. The re-key obligation is 18 headings, not one — this gates the deciding run

The round's integration item says the `SKILL.md` edit "DRIFTS that one cold-read
section". The `SKILL.md` edit does drift exactly one section. But the round's
**other** required edits drift seventeen more, because `corpus/QUALITY.md`,
`corpus/SOURCES.md` and `tools/*` are pinned inputs of those sections and are *not*
in `DROP`.

Measured on a clone of the lane at the frozen base carrying the lane worktree's
current round-55 production edits (`floor-at-content-rev.txt`,
`rekey-all18.stdout`):

| state | `sections_covered` | `restraint` | `box3_full_page` |
|---|---|---|---|
| frozen base `631cd64` | **64/64** | 8 | true |
| content revision W (round-55 production edits, nothing re-keyed) | **46/64** | 6 | false |
| W + re-key of `## Standing rules` **only** | **47/64** | 6 | false |
| W + re-key of **all 18** drifted headings | **64/64** | 8 | true |
| 64/64 state, then `SCORECARD.md`/`LOG.md` edited after REV | **64/64** | 8 | true |
| 64/64 state, then the six pinned inputs edited after PIN | **46/64** | 6 | false |

Rows 1 and 6 are my own runs (`floor-at-frozen-base.txt`, `probe3.stdout`); the rest
are `floor-at-content-rev.txt`, `rekey-all18.stdout` and `probe2.stdout`.
Note that the bind itself reports success in every case — the loss is only visible
to the counter, which is exactly why the precheck (`coldread-precheck.sh`) exists.

`no-harm.sh`'s calibration-critical monitor is
`NOHARM coldread-floor … ok` iff `score>=8 and credited>=64`, and
`deciding-run.sh` exits non-zero when any `NOHARM` line is `RED`. So a re-key of
only `## Standing rules` leaves `credited=47` and **fails the deciding run**.

The 18 headings (derived, not asserted — the derivation is
`measure --repo <clone> --rev W` and reading `coldread.sections[].credited`):

```
## Standing rules
## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
## The leg ledger — replay, receipt, and how it is read (round 7, measured)
### Triggers T1–T3 and the re-pin rule
### The service's limits — what tameshi refuses to mutation-test
## The operator's runbook and the six-leg regression (round 10, measured)
## Repeated controls and gate registry — round 12
### Gate/probe registry
## Pin disposition and provenance correction — round 13
### Round-13 gate/probe registry
## Effective expectation reconciliation — round 14
## Context gate classification and explicit exit classes — round 15
### Round-15 gate/probe registry
## Live-tree re-pin and entry-command monitor — round 17
### Round-17 gate/probe registry — re-pin and monitor
### Round-18 gate/probe registry — routed-defect closure
### Round-21 gate/probe registry — finite environment differential
### Round-26 gate/probe registry — report interop
```

Cause, per §1.2: the pinned input union of those sections contains the six files
the round edits — `corpus/QUALITY.md` (9 sections), `corpus/SOURCES.md` (17),
`tools/registry.json` (15), `tools/context-capture.py` (11),
`tools/registry-check.py` (10), `tools/repeat-control.py` (11); the union over
those six is exactly the 18 headings above. Every one of them needs its own clean
reader at C0 and its own bound entry.

The round-54 dry-bind seat had already measured the same 18
(`T55W1ExecReKeyDryBind-receipts/round55-edits-lost-sections.txt` lists the same
headings, and its `registry-drift-lost-sections.txt` shows 11 lost from a
`registry.json` edit alone). That receipt is evidence the finding is real in the
lane, not an artefact of my fixture.

## 3. Findings, by severity

### Critical

**F1 — a one-heading re-key fails the deciding run.** 47/64 against a `>=64`
monitor (§2). The L1 must derive the full drifted set at its content commit
(the set can grow if it edits more inputs) and plant one clean reader per heading.
Fix is mechanical: `--headings` with the derived list. Round 54 is the precedent —
its receipt (`.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/refresh-receipts.json`)
records **23** headings re-keyed in one binder run, `skipped=0`, 0 dropped inputs.

**F2 — the existing dry-bind reader cannot be reused.** Its `cand`
`314cfe29036a2347b138761b9eb7d6e06dad41f8` **does not exist in the lane**
(`git -C <lane> cat-file -t 314cfe…` → `fatal: could not get object info`), and its
`PIN` `03d434ab…` does not either. The binder resolves both with
`git -C LANE rev-parse` (`:78`) and compares `cand` to that string, so a
clone-only commit can never be the bind's C0. Worse, its `section_sha256`
`4f959fd7…` was derived from a `SKILL.md` whose sha was `a157f37d…`; the lane
worktree's `SKILL.md` is now `e0ce89f7866062062f4987358e353c8626c18f56d2eb1589225af99f44d695a6`
and its `## Standing rules` body hashes to `acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767`
(`start 17`, `end 44` — the section grew by a line when `registry-check --rev`
joined the ninth allocating mode). A stale reader is `no-clean-reader`, so the bind
silently skips the heading. **Re-derive `cand` + `section_sha256` at the landed
commit; do not copy the dry-bind values.**

### High

**F3 — reader selection stops at the first candidate, so a dirty reader blocks a clean one.** `binder.py:114-131` `break`s out of the reader loop when the first
`cand`+`sha`-matching reader has more findings than `allowed`. Probes C9/C10: same
two files, only the filename order differs — `a-dirty`+`z-clean` → `SKIP
reader-has-findings:1>0`; `a-clean`+`z-dirty` → `REKEY`. Consequence: leave exactly
one `cand`+`sha`-matching reader per heading in the wave dir, or make the clean one
sort first.

**F4 — ordering: the pinned inputs must not move after PIN.** `DROP` covers only
`LOG.md`, `SCORECARD.md`, `SKILL.md` and the ledger. Measured on the all-18-rekeyed
state: a post-PIN edit of the six pinned inputs (`corpus/QUALITY.md`,
`corpus/SOURCES.md`, `tools/{context-capture,registry-check,repeat-control}.py`,
`tools/registry.json`) takes **64/64 → 46/64** (`probe3.stdout`); a post-pin
`QUALITY.md` edit alone costs credit in the one-heading state (`probe2.stdout`,
47/64 → 46/64). So:

* the round's QUALITY criterion and its SOURCES rows must be landed **at or before
  `PIN`** — the natural choice is `PIN = C0`, the content commit, and then a
  follow-up commit that touches only the ledger, the traces and the reader reports;
* `corpus/lessons/round-55.md`, `corpus/lessons/round-54.md` and
  `corpus/knowledge/scratch-root-contract.md` are in no input union (0 sections) and
  can land whenever;
* `SCORECARD.md` and `LOG.md` are safe after `PIN` — `DROP` absorbs them, measured.

### Medium

**F5 — an omitted `findings` key is indistinguishable from a clean read** (§1.3,
probe C6). A reader that crashed before writing findings binds as clean.

**F6 — the binder never checks the reader's `skill_sha256`** (probe C7); it
substitutes its own value from C0. Fine for credit, but the reader's whole-file
claim is unverified decoration.

**F7 — "newest prior entry" is lexicographic, not chronological.** `:150`
`max(old, key=lambda e: str(e.get('read_rev','')))`. For `## Standing rules` the
prior `read_rev`s are `eb7838b1, 01d586dd, 4acdeac9, 8eaae28e, 154bf4d7, 2227d833,
651773ab, 99c3bc88`; the max is **`eb7838b1…` (round 17)**, not the round-54
`99c3bc88…`. The carried `class`/`verdict` therefore come from an arbitrary era.
Both happen to be `instruction`/`gap-minor` here, so credit is unaffected — but see
F8.

**F8 — the binder launders a failing prior verdict.** `:154`: any prior verdict in
`{gap-blocking, wrong-expectation, not-executed}` is rewritten to
`verified-record`/`executed-ok`, and a zero-finding reader never sets
`gap-minor`. Combined with `blocking_gaps: 0` / `wrong_expectations: 0` being
hard-coded (`:180`), **the binder can never produce a failing entry**: a heading
whose previous read found a wrong expectation is re-keyed as `executed-ok`. That is
the design (a fresh clean read supersedes), but it means "the re-key credits" is
not evidence that the section is defect-free — only that this round's reader found
nothing.

**F9 — `commands_executed_count` is synthesized.** `:182` writes
`1 + len(inputs)` = **2,498** for a bind that executed one command. The credit gate
only needs `> 0`, so no gating consequence; but the ledger now records a number
that is not a command count, and `--explain`/audits will read it as one.

**F10 — `read_rev`, `reports`, `seats`, `external_inputs`, `start`, `end` and
`skill_sha256` are never validated by any counter I could find**
(round-18/21 credit, round-48 precheck, rounds 45-47 coverage/freshness). Their
only consumer is a human reading the ledger. That is worth knowing before anyone
cites "the ledger says the section was read at C0" as a measured fact: the
rev-binding the machinery actually enforces is the section sha plus the input
digests, nothing else.

### Low

**F11 — the bound entry carries `verdict: gap-minor` with `minor_gaps: 0`**
(verdict inherited, findings empty). Internally inconsistent; credits either way.

**F12 — binder docstring vs code.** `:27-28` says "SKILL.md's ignored status left
to the credit algorithm", but `DROP` at `:49` drops `SKILL.md` outright. Harmless
(the credit rule ignores it too), but the sentence is not what the code does.

**F13 — `blob_at()` uses `git show`, not `git cat-file blob`** (`:75-79`). For a
directory path `git cat-file -e` succeeds and `git show REV:dir` prints a tree
listing, so the binder would record a digest over that listing and the credit rule
would then reject the same key with `input-not-blob` — a silent self-inflicted
failure. Not live for this heading: all 2,497 carried inputs are `blob` objects at
the frozen base (`git cat-file --batch-check` over the union: `{'blob': 2497}`),
but it is a latent trap for any heading that ever recorded a directory input.

**F14 — frozen `no-harm.sh` misstates the obligation its own monitor enforces
(reported, not fixed — the file is frozen).** `.ufo/evidence/round-55/no-harm.sh:5-7`
says the cold-read floor "is monitored at 64/64, which is the re-key obligation this
round carries for **the one SKILL.md section** its edit drifts." The monitor is
right (it requires 64/64); the parenthetical is wrong — §2 measures **18** sections
losing credit, 17 of them from the round's record/tool edits rather than from the
`SKILL.md` edit. Anyone reading that comment as the obligation will land one reader
and fail the run.

## 4. Residual risk and verification gaps

* **The 18-heading set is derived at the lane worktree as it stands now.** The L1
  keeps editing; if it touches another file that is a pinned input of a section
  (e.g. `tools/env-diff.py`, `tools/bash-witness-study.py`, `corpus/knowledge/service-limits.md`),
  the set grows. Re-derive after the final production commit — the command is in
  the receipt (`floor-at-content-rev.txt` regenerates from one measure).
* **I did not measure the round-55 counters (C1/C2).** My scope is the ledger
  machinery; whether the re-keyed ledger passes `c1/measure.py` is untouched by
  this audit (C1 reads `SCORECARD.md`/`corpus/QUALITY.md`/`corpus/lessons/round-54.md`/`LOG.md`
  and never reads the ledger).
* **Doc drift is a moving target.** `SKILL.md` changed twice while I worked
  (`a157f37d…` → `e0ce89f7…`, section `17-43` → `17-44`). Every hash in this
  report is labelled with the revision it came from; none should be copied forward.
* **What the machinery cannot see.** A reader that reports `findings: []` is taken
  on trust: the binder writes a trace that attests the *inputs*, not the reading,
  and the credit rule never opens the reader report at all. That is the same limit
  the round-18 credit rule has always had (`cannot_see` in the round-55 contract's
  C1 block says as much).
* **A pre-existing accounting oddity, not fixed here because it is outside this
  seat's item:** `## Standing rules`'s 2,497-input union is 2,407 `.ufo/**` paths
  (713 `.ufo/waves/**`, 1,690 `.ufo/evidence/**`) and only 90 real production
  files. Any future round that edits one of those historical paths re-drops this
  section. Excluding historical `.ufo/**` from the carried inputs would make
  re-keys durable; that is a round-54-binder design change, not something this
  round should make quietly.

## 5. Receipts

Under `.ufo/waves/round-55/w1/T55W1RevLedger-receipts/`:

| file | what it is |
|---|---|
| `demo.stdout` | the field-by-field binder probe (arms A/B/C/D/E): empty findings accepted, every refusal shape, three silent acceptances, reader-ordering, `DROP` counterfactual, `read_rev`/`skill_sha256` proved inert |
| `rekey-all18.stdout` | base 64/64 → content revision 46/64 (18 lost) → re-key all 18 → 64/64 → post-REV record edits → 64/64 |
| `floor-at-content-rev.txt` | the 18 lost headings and their `input-drift:` reasons at the content revision |
| `floor-at-frozen-base.txt` | `64/64`, restraint 8, `box3_full_page=true` at `631cd64` — my own run, not a quoted receipt |
| `probe2.stdout` | only-`## Standing rules` re-key → 47/64; post-PIN `QUALITY.md` → 46/64; OUTDIR outside the lane → trace path rejected |
| `probe3.stdout` | the all-18 state before and after a post-pin edit of the six pinned inputs |
| `field-insensitivity.txt` | which entry fields the credit rule actually reads (start/end/heading/read_rev/skill_sha/reports inert; traces gate) |
| `demo.py`, `rekey_demo.py`, `probe2.py`, `probe3.py` | the drivers, so every number above is re-runnable against a clone |

Machine-readable companion: `T55W1RevLedger.json` (the minimal reader JSON
template, the exact binder argv, and the 18-heading list).
