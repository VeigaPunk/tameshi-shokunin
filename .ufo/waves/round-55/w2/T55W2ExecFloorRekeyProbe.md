# T55W2ExecFloorRekeyProbe — re-key probe before the L1 binds

Seat: `T55W2ExecFloorRekeyProbe` (wave 2, executive/floor). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit under attack: **C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`**; floor/base `0a2010acd1e9…`; counter
freeze `e2979f277138…` (+ amendments, `freeze.json`). Nothing in the lane was written; every bind ran on a
`git clone --shared` at C0 in `/fast/scratch/hyaku/tameshi-r55/T55W2ExecFloorRekeyProbe`.

Receipts: `.ufo/waves/round-55/w2/T55W2ExecFloorRekeyProbe-receipts/01-…10-…txt` (command + output + verdict
for every claim below).

---

## 0. Verdict in one paragraph

All three wave-2 reader deliverables for `## Standing rules` are **valid against the round-21 credit code**
(heading, `cand` = C0, `section_sha256` = the frozen round-18 `sectionize` value, `findings` a list of
`{quote, why}` whose quotes really occur in the section). They are **not bindable as delivered**: every one of
them carries findings (2 / 3 / 7), and the adapted binder admits a reader only up to a per-heading adjudication
count. The lane's `integrate/resolutions.json` is a decision log with no `{heading, n}` rows, so the binder
**crashes before doing anything** (`KeyError: 'n'`, receipt 04). With no resolutions it **skips** the section
(`reader-has-findings:2>0`, receipt 05). With an adjudication of `n >= 2` the section **binds and credits**
(receipt 06) — but only `T55W2Read01` is recorded (`minor_gaps=2`); Read02 and Read03 never reach the ledger, even
at `n=12`. The precheck does **not** return to 64/64 from these readers alone: at the bind snapshot it read
`cand_credited=55 lost=9 RED` (receipt 07), because 18 headings lost credit at C0 and only 9 had a C0-pinned reader
then. A mechanism probe that gives all 18 headings a C0-pinned reader returns **`floor_credited=64 cand_credited=64
lost=0 ok`** (receipt 08), so the arithmetic is fine — the gap is wave-3 deliverables, not mechanics.

---

## 1. The three reader deliverables vs the round-21 credit code

Required predicates, evaluated directly (receipt 01):

| reader | `heading == "## Standing rules"` | `cand == C0` | `section_sha256` == sectionize@C0 | `findings` list | n | item shape `{quote, why}` |
|---|---|---|---|---|---|---|
| `T55W2Read01.json` | yes | yes | yes | yes | 2 | yes |
| `T55W2Read02.json` | yes | yes | yes | yes | 3 | yes |
| `T55W2Read03.json` | yes | yes | yes | yes | 7 | yes |

Independent recomputation of the sha with the frozen sectionizer (receipt 02):

```
$ python3 - <<'EOF'  # importlib round-18 measure.py, sectionize(git show C0:SKILL.md)
sections=64
{'heading': '## Standing rules', 'start': 17, 'end': 44,
 'sha256': 'acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767'}
skill_sha256 e0ce89f7866062062f4987358e353c8626c18f56d2eb1589225af99f44d695a6
EOF
```

Additional check (receipt 01): every one of the 12 `quote` strings occurs in the section text at C0 when compared
with whitespace collapsed — the readers quoted the real bytes, not a paraphrase. Snapshot of the bytes validated
(the wave is live): `Read01` `ec7009d8…`, `Read02` `7b566b14…`, `Read03` `d7a48ddd…`.

**Verdict: three of three validate.** They are dense, anchored, and adversarial; nothing here says they are wrong.
What follows is only about whether the *binder* can consume them.

---

## 2. Credit at floor and at C0 (receipt 03)

```
base 0a2010acd1e9…  sections=64 credited=64  score=8   box3_full_page=True
C0   9cf0146b94dd…  sections=64 credited=46  score=6   box3_full_page=False
```

The 18 uncredited sections at C0 split cleanly:

- **1 byte-level loss** — `## Standing rules` (17-44), reason `no-ledger-entry`: its sha changed at C0, so no
  ledger entry matches. This is the section the three readers cover.
- **17 input-drift losses** — the sections whose entries pin the files C0 edited (`tools/repeat-control.py`,
  `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/bash-witness-study.py`,
  `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/knowledge/scratch-root-contract.md`, …). Their bytes did not
  change; their pinned inputs did.

`lost-headings-at-c0.json` lists exactly these 18, so a re-key must cover 18 headings even though only one needs a
fresh read of new bytes.

**Why this is load-bearing beyond the precheck:** `no-harm.sh:16-17` gates on
`calibration_restraint_score >= 8 AND coldread sections_covered >= 64`, and `measure.py:655` defines
`box3_full_page = sections_covered == sections_total`. At C0 the score is already 6, so a *partial* bind fails
twice — precheck RED and the `coldread-floor` no-harm monitor RED. Only 64/64 clears both.

---

## 3. Bind dry-run (scratch clone at C0)

Clone: `git clone --shared <lane> $S/clone; git -C $S/clone checkout 9cf0146b…`
(`toplevel == $S/clone` asserted before any commit). Staged into the clone because they are untracked in the lane
and absent at C0: the wave-2/wave-3 readers, `c1/lost-headings-at-c0.json`, `integrate/{binder.py,resolutions.json}`.
Binder under test: `.ufo/evidence/round-55/integrate/binder.py` sha256 `cbe49ffa…` (the L1's adaptation of the
round-54 binder; `E` → round-55, `WAVE_DIRS` → w2+w3, `HEADINGS` → the 18).

### 3.1 As found — binder + lane resolutions (receipt 04)

```
$ TMPDIR=$S/tmp python3 .ufo/evidence/round-55/integrate/binder.py $S/clone <C0> <C0> <rekey dir>
rc=1, stdout empty
Traceback (most recent call last):
  File ".../binder.py", line 54, in <module>
    RES[item['heading']] = int(item['n'])
KeyError: 'n'
```

The binder parses `LANE/.ufo/evidence/round-55/integrate/resolutions.json` as a list of `{heading, n}`
(binder.py:52-54). The round-55 file is a decision log (`id/from/finding/decision/evidence`). **The bind cannot
run at all** until the file is in the round-54 shape or the parse is changed.

### 3.2 No adjudication (receipt 05)

With the file absent: `RES={}` → `allowed=0` for every heading.

```
SKIP ## Standing rules reader-has-findings:2>0
REFRESH rekeyed=3 skipped=15 headings=18
```

The three sections bound in that run were the w3 readers that happened to report zero findings
(`T55W3R01`, `T55W3R02`, `T55W3R05`). **`## Standing rules` can never bind under a zero-findings gate**, because
all three wave-2 readers carry findings.

### 3.3 Adjudicated (receipt 06)

With a scratch adjudication `[{"heading": "## Standing rules", "n": 2}, …]`:

```
REKEY ## Standing rules start=17 inputs=2497 dropped=0 reader=T55W2Read01
```

Entry written (read back from the committed bind `b8678cb809ed`):

```
{'start': 17, 'end': 44, 'sha256': 'acfb671a…f767', 'class': 'instruction', 'verdict': 'gap-minor',
 'minor_gaps': 2, 'wrong_expectations': 0, 'commands_executed_count': 2498,
 'read_rev': '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb',
 'seats': ['T55W2Read01', 'L1 TameshiR55a2 re-key (round 54)'],
 'traces': ['…/rekey-r55-9cf0146b94dd/traces/section-07.json'], 'inputs': 2497}
```

**Raising `n` to 12 changes nothing.** The binder takes the *first* matching reader in sorted path order
(w2 before w3, `T55W2Read01` first): the same run with `n=12` still writes `reader=T55W2Read01`, `minor_gaps=2`
(receipt 06, VARIANT). Read02's 3 findings and Read03's 7 findings — including the two that attack the section's
cited C2 counter — are **silently dropped from the record** by the bind. If the L1 wants them in the ledger, an
adjudication count cannot express that; the entry shape has one `minor_gaps` integer and one reader seat.

### 3.4 Precheck after that bind (receipt 07)

```
$ bash .ufo/evidence/round-48/quality/coldread-precheck.sh $S/clone 0a2010acd1e9… b8678cb809ed…
COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=b8678cb809ed cand_credited=55 lost=9 RED
```

The section itself is fine at the bind commit — `measure.py --explain` reports
`{'## Standing rules': start 17, end 44, credited True, vetoed False, reason 'credited'}` — and total credit moves
46 → 55 (1 for `Standing rules` + 8 w3 headings bound in that snapshot). It is **not 64/64**, because 9 of the 18
headings had no C0-pinned reader at bind time.

### 3.5 Mechanism probe — 64/64 is reachable (receipt 08)

To separate "can this binder reach 64/64" from "are the deliverables here", I gave the 9 then-missing headings
synthetic readers in the scratch clone (heading, `cand`=C0, correct `section_sha256`, `findings: []`) and re-ran
the bind over all 18:

```
REFRESH rekeyed=18 skipped=0 headings=18
measure:  credited 64 of 64, score=8
COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=97d8f759e575 cand_credited=64 lost=0 ok
```

**The stubs are a fixture, not deliverables** — they exist only to prove the arithmetic and the layout. The
conclusion for the L1: *64/64 holds exactly when every one of the 18 headings has a reader JSON pinned at C0 whose
`section_sha256` equals the frozen sectionize value for that section.*

---

## 4. Which deliverables cannot be bound (state at probe time)

Reader inventory at `2026-10-28T17:51Z` (receipt 10; the wave is still writing — this must be re-derived at bind
time):

- **`## Standing rules` — three readers, none bindable at `n=0`; only `T55W2Read01` is ever bound** (see §3.3).
  A fourth is now present (`T55W3R07`, 2 findings).
- **3 of 18 headings still have no C0-pinned reader:** `## The operator's runbook and the six-leg regression
  (round 10, measured)`, `### Round-21 gate/probe registry — finite environment differential`,
  `### Round-26 gate/probe registry — report interop`. Until each gets a JSON whose `cand`/`section_sha256` match
  C0, the precheck cannot reach 64/64 — those sections' bytes are unchanged, so the reader's only mechanical job
  is to pin them (but the binder will not accept a heading without one).
- **Duplicate deliverable:** `T55W3R07.{json,md}` was written into **both** `.ufo/waves/round-55/w2/` and
  `w3/` (identical bytes, sha `e30ec45b…`). The binder's glob sees both; sorted order picks the `w2/` copy. If the
  two copies ever diverge, the ledger's `reports` path names whichever sorts first, with no digest to tell them
  apart. Move one copy out before the bind commit.
- At the earlier bind snapshot (≈17:44) only 9/18 headings had readers; that is the state the `55/64` number was
  measured in. Both snapshots are receipts, not predictions.

---

## 5. Exact commands the L1 should run

Assumes `LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin`, `C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`,
`S=$HYAKU_SCRATCH/tameshi-r55/<seat>`.

**(a) Adjudication file in the shape the binder parses** — the binder reads
`LANE/.ufo/evidence/round-55/integrate/resolutions.json`; it must be a JSON list of `{"heading": <exact heading>,
"n": <allowed findings>}`. Keep the current decision log under a different name (e.g. `decisions.json`) or merge
both keys into one list; an entry without `n` still crashes the parse.

**(b) Dry-run on a clone first** (exactly what this seat did):

```
git clone --shared "$LANE" "$S/clone" && git -C "$S/clone" checkout "$C0"
git -C "$S/clone" rev-parse --show-toplevel     # must print $S/clone
# copy the committed-at-REV deliverables the binder reads (readers, lost-headings, binder, resolutions)
mkdir -p "$S/clone/.ufo/evidence/round-21/coldread/rekey-r55-9cf0146b94dd"
TMPDIR=$S/tmp python3 "$S/clone/.ufo/evidence/round-55/integrate/binder.py" \
    "$S/clone" "$C0" "$PIN" "$S/clone/.ufo/evidence/round-21/coldread/rekey-r55-9cf0146b94dd"
# expect: REFRESH rekeyed=18 skipped=0 headings=18   (exit 0)
git -C "$S/clone" add -A && git -C "$S/clone" commit -m "probe"
python3 "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$S/clone" \
    0a2010acd1e92e4e332774050825e21bcfc7e079 "$(git -C "$S/clone" rev-parse HEAD)"
# expect: COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=… cand_credited=64 lost=0 ok
```

**(c) In-lane bind, then the deciding run's own gate:**

```
OUT="$LANE/.ufo/evidence/round-21/coldread/rekey-r55-9cf0146b94dd"; mkdir -p "$OUT"
TMPDIR=$S/tmp python3 "$LANE/.ufo/evidence/round-55/integrate/binder.py" "$LANE" "$C0" "$PIN" "$OUT"
# commit readers + binder + resolutions + $OUT + the rewritten ledger, then:
bash "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$LANE" 0a2010acd1e9… "$REV"
python3 "$LANE/.ufo/evidence/round-21/coldread/measure.py" --repo "$LANE" --rev "$REV" \
  | python3 -c 'import json,sys;d=json.load(sys.stdin);print("score",d["calibration_restraint_score"],"covered",d["coldread"]["sections_covered"])'
# both gates need 64/64: no-harm.sh:16-17 requires score>=8 AND covered>=64
```

**PIN choice:** inputs are pinned from `PIN` (`blob_at(pin, p)`), so use the revision that already carries the
final bytes of every input (the last content commit, `>= C0`). If any input file is edited after `PIN` and before
the deciding `REV`, that section drifts again and the precheck goes RED — that is exactly how the 17 input-drift
losses arose at C0.

---

## 6. Residuals / risks (no fix attempted; lane is out of my write scope)

1. **Provenance label:** `binder.py:184` writes `'L1 TameshiR55a2 re-key (round 54)'` — every round-55 entry
   carries a `round 54` seat label. Observed in the committed probe entries. One-line fix.
2. **Docstring vs behaviour:** `binder.py:15-19` says a reader *with findings* is not re-keyed and readers live in
   `w1/`; the code globs `w2/`+`w3/` (`:47`) and binds a reader with findings when `n>0`. The docstring describes a
   stricter contract than the code enforces.
3. **Reader selection is order-dependent, not quality-dependent:** with `n` large enough, the ledger still records
   the alphabetically first reader (`T55W2Read01`) and its finding count. Read02/Read03's findings never enter the
   record (receipt 06).
4. **Reports are not digested:** an entry stores reader paths under `reports` with no sha, and neither the round-18
   nor the round-21 measure gates on them (`grep -n "reports\|seats"` finds no gate). A reader report edited after
   the bind does not drift its entry; only the section sha and the `inputs`/`traces` are pinned (receipt 09).
5. **`HEADINGS` is read from the lane worktree** (`binder.py:49`), i.e. from an untracked file. It must be the same
   file at bind time and at the deciding revision, or the re-key set silently changes.
6. **Snapshot drift:** the wave was writing while this probe ran (9/18 → 15/18 headings covered between the bind run
   and the inventory; `T55W3R06.md` appeared mid-probe). Every number above is timestamped and re-derivable; none
   should be quoted as the deciding state.

---

## 7. Housekeeping

- **Tooling:** none installed or upgraded (no `pacman`, no `uv tool`, no binaries). The probe used only `git`,
  `python3` stdlib, and the lane's frozen scripts.
- **Census:** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  tameshi` → **exit 0**, `corpus/SOURCES.md` 140 `S###` rows (`tameshi ok …/corpus/SOURCES.md`).
- **Writes:** only `.ufo/waves/round-55/w2/T55W2ExecFloorRekeyProbe.md` and
  `.ufo/waves/round-55/w2/T55W2ExecFloorRekeyProbe-receipts/`. The lane's tracked files, the frozen
  `.ufo/evidence/round-55/*`, `contract.json`, `freeze.json` and the wave spec were read only. All binds ran in a
  scratch clone; the scratch parent `/fast/scratch/hyaku/tameshi-r55` was never removed.

## 8. Artifacts opened

Lane: `.ufo/evidence/round-55/{contract.json,freeze.json,deciding-run.sh,c1/lost-headings-at-c0.json}` ·
`.ufo/evidence/round-55/integrate/{binder.py,resolutions.json}` · `.ufo/evidence/round-21/coldread/{measure.py,ledger.json}`
· `.ufo/evidence/round-18/measure.py` · `.ufo/evidence/round-48/quality/coldread-precheck.sh` ·
`.ufo/evidence/round-54/integrate/binder.py` · `.ufo/waves/round-55/w2/T55W2Read0{1,2,3}.{json,md}` ·
`.ufo/waves/round-55/w3/*` (inventory) · `corpus/SOURCES.md` · `tools/{repeat-control,context-capture,registry-check}.py`
(via C0 objects only) · `SKILL.md` at C0 (git object). Scratch: the clone at C0 and the bind commits
`b8678cb809ed`, `97d8f759e575`.
