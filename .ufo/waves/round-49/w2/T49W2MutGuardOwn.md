# T49W2MutGuardOwn — independent single-edit mutants vs the candidate generator (wave 2, round 49)

Attacked: the candidate's property-based generator `tools/pbt-staged-id.py` at content revision
`f181a961ae44061af486f600e5ea257d2baf78f8` — specifically its **kill power against an independent
mutant panel I built myself** (the C2 method's falsification surface). I did not author what I
attack; I never decide a claim; nothing here is a verdict (the deciding run is the L1's).

Independence: the 12 mutants were designed from the guard's source and docstring only. I never read
`/home/vgpnk/.local/state/`, never opened `c2-WITNESS.stdout`, `c2-CTL_FIX.stdout` or
`c2-CTL_ABSENT.stdout`, and never read the frozen `c2/measure.py` or the hidden panel. The lane file
`tools/staged-id-guard.py` was never edited (sha256 below, before == after); all mutants are scratch
copies. No subagents; no tool installs (stdlib python3 only; pacman untouched per the host-wide pause).

## Method

Scratch root `/fast/scratch/hyaku/tameshi-r49/T49W2MutGuardOwn` (deleted before this report was
finalised; every cited receipt is copied into `T49W2MutGuardOwn.receipts/` next to this file).

    S=/fast/scratch/hyaku/tameshi-r49/T49W2MutGuardOwn
    git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive f181a961ae44061af486f600e5ea257d2baf78f8 | tar -x -C "$S/cand"

- Pristine guard copy sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` ==
  the pinned lane file's sha256 (contract `claims.C2.named_gate`): the mutants mutate exactly the
  pinned bytes. Re-checked at the end: unchanged.
- Selftests at the candidate bytes: `python3 -I tools/pbt-staged-id.py --selftest` →
  `PBT_STAGED_ID_SELFTEST: cases=31 failed=0` (exit 0); `python3 -I tools/staged-id-guard.py
  --selftest` → `VERDICT: PASS` (exit 0).
- Panel run (per mutant, and once against the pristine guard as baseline):

      python3 -I tools/pbt-staged-id.py --guard <GUARD> --seed 4949 --cases 400 --dump <dump>

  TMPDIR pointed into scratch; the generator's own per-case workdir is `tempfile.mkdtemp`
  (`pbt-staged-id.py:789`, inside `run()` :783), removed by the generator itself.
- Kill confirmation: for every generator violation I re-ran the **exact dumped case bytes**
  (the dump line at the counterexample index, `pbt-staged-id.py:803-805` writes
  `{index, registry, staged, map}`) through both guards via the frozen CLI
  `python3 -I <guard> --registry R --staged G [--map M] --json` and required the outputs to differ.
  Full transcript: `T49W2MutGuardOwn.receipts/T49W2MutGuardOwn.replay.txt`.
- Determinism: the whole panel was run twice; every `PBT_STAGED_ID:` summary line and every dump
  hash reproduced (m02/m08 dumps byte-identical — both stop at case 0 on the same first case).

## The independent panel (12 single-edit mutants)

Sites are `tools/staged-id-guard.py` line numbers at `f181a961` (== pinned bytes). Diffs:
`T49W2MutGuardOwn.receipts/T49W2MutGuardOwn.m<NN>.diff`.

| id | site | single edit | defect story |
|----|------|-------------|--------------|
| m01 | :65 | `ROW_RE` `^ {0,3}` → `^ {0,4}` | 4-space rows become rows: the 0-3-space census rule (docstring bullet 1) is widened, the exact false-green shape the guard exists to catch, inverted |
| m02 | :65 | `ROW_RE` `S\d{3,}` → `S\d{4,}` | 3-digit ids stop being rows: every normal table goes invisible |
| m03 | :66 | `COLUMN0_RE` `^\|\s*` → `^\|` | column-zero pattern demands a flush id: blind to the normal `\| S002 \|` form, so `column0_miss` inverts |
| m04 | :67 | `URL_RE` `https?://` → `https://` | `http://` documents stop being extracted (form-insensitivity bullet) |
| m05 | :120 | drop `re.sub(r'^www\.', '', text)` | `www.` no longer stripped from document identity |
| m06 | :118 | `raw.strip().lower()` → `raw.strip()` | document identity no longer case-folded |
| m07 | :121 | `return text.rstrip('/')` → `return text` | trailing slash no longer normalised away |
| m08 | :102 | `URL_RE.search(blob)` → `URL_RE.match(blob)` | URL recognised only at the start of the cell blob |
| m09 | :112 | openable dot test `{2,6}` → `{2,3}` | `.test`-style host documents (4-char suffix) stop being documents |
| m10 | :127 | `len(sid) > 12` → `len(sid) > 5` | S-ids of 6+ chars raise setup refusal |
| m11 | :86 | `len(cells) < 5` → `len(cells) <= 5` | 5-cell rows refused as malformed |
| m12 | :443 | `json.loads(raw, object_pairs_hook=_no_duplicate_keys)` → `json.loads(raw)` | duplicate JSON keys in the map file no longer refused (`_no_duplicate_keys`, :406) |

## Result table (seed 4949, 400 cases)

Baseline pristine guard: `PBT_STAGED_ID: cases=400 violations=0 counterexample=none` (exit 0), all
twelve frozen classes ≥ 20 (`indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,
no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,
map_inadmissible=31`) — receipt `T49W2MutGuardOwn.pristine.out`.

| mutant | generator result | verdict | differential replay (same case bytes) |
|--------|------------------|---------|----------------------------------------|
| m01 | cases=21 violations=1 counterexample=20 — `field staged_max: guard 'S007', oracle 'S000'` | KILLED | both exit 0; pristine `staged_rows: 0, staged_max: "S000"` vs mutant `staged_rows: 1, staged_max: "S007"` |
| m02 | cases=1 violations=1 counterexample=0 — `exit 0, oracle expects 1` | KILLED | pristine exit 1 (`collisions ["S022"]`, `unmapped ["S022"]`, refused) vs mutant exit 0 (`registry_rows 0`, answered) |
| m03 | cases=3 violations=1 counterexample=2 — `field column0_collisions: guard [], oracle ['S020']` | KILLED | both exit 1; pristine `column0_collisions ["S020"], column0_miss []` vs mutant `[] / ["S020"]` |
| m04 | cases=11 violations=1 counterexample=10 — `field held: guard {}, oracle {'S023': 'S023'}` | KILLED | both exit 1; pristine `held {"S023":"S023"}, registry_docs 2` vs mutant `held {}, registry_docs 1` |
| m05 | cases=13 violations=1 counterexample=12 — `exit 1, oracle expects 0` | KILLED | pristine exit 0 admitted (`map_dedupe {"S015":"S005"}`) vs mutant exit 1 inadmissible (`map_clash ["S005"]`) |
| m06 | cases=22 violations=1 counterexample=21 — `field held: guard {}, oracle {'S018': 'S005'}` | KILLED | both exit 0; pristine `held {"S018":"S005"}` vs mutant `held {}` |
| m07 | cases=9 violations=1 counterexample=8 — `field held: guard {}, oracle {'S026': 'S015'}` | KILLED | both exit 0; pristine `held {"S026":"S015"}` vs mutant `held {}` |
| m08 | cases=1 violations=1 counterexample=0 — `field registry_docs: guard 0, oracle 1` | KILLED | both exit 1; pristine `registry_docs 1` vs mutant `0` |
| m09 | cases=35 violations=1 counterexample=34 — `exit 1, oracle expects 0` | KILLED | pristine exit 0 (`held {"S030":"S003"}`, answered) vs mutant exit 1 (`unmapped ["S030"]`, refused) |
| m10 | cases=17 violations=1 counterexample=16 — `exit 2, oracle expects 0` | KILLED | pristine exit 0 answered vs mutant exit 2 `{"reason": "S-id too long: 'S32121'", "verdict": "setup_refusal"}` |
| m11 | cases=400 violations=0 counterexample=none (exit 0) | SURVIVED | hand-made input below: pristine exit 1 vs mutant exit 2 |
| m12 | cases=400 violations=0 counterexample=none (exit 0) | SURVIVED | hand-made input below: pristine exit 2 vs mutant exit 1 |

**10/12 killed, both kills and survivors confirmed non-equivalent by output.** Kill latency varied
from 1 case (m02, m08) to 35 cases (m09 — host-kind path documents are one Cycle kind of one recipe,
`rec_path_document`/`DOCUMENT_KINDS`, `pbt-staged-id.py:686-735`): the generator's kill power on
rare-shape mutants is distribution-sensitive, which is worth remembering when reading the hidden
panel's 11/12 target.

## Confirmed kills — how each was confirmed

Command shape (per kill; full driver and verbatim outputs in
`T49W2MutGuardOwn.receipts/T49W2MutGuardOwn.replay.txt`):

    # case bytes = the dump line at the counterexample index (pbt-staged-id.py:779-782)
    python3 -I <pristine-or-mutant> --registry R --staged G [--map M] --json

Example (m01, counterexample index 20, a `rec_indent_4_plus` case whose staged row sits at 4 spaces):

    pristine: {"staged_max": "S000", "staged_rows": 0, ... "verdict": "answered"}   exit 0
    mutant:   {"staged_max": "S007", "staged_rows": 1, ... "verdict": "answered"}   exit 0

The generator's oracle (`pbt-staged-id.py:246` `oracle_case`, compared field-by-field in `check`
:296, field-set equality :312) treats the 4-space row as not-a-row; the widened extractor sees it —
outputs differ, mutant killed. The same replay discipline confirmed every kill above; no kill rests
on the generator's word alone.

## Survivors — hand-made distinguishing inputs (coverage findings, not contract changes)

### m11 (:86, `< 5` → `<= 5`)

The generator never emits a 5-cell row: its refusal recipes produce only 2- and 4-cell rows
(`rec_refusal`, `pbt-staged-id.py:483-516`) and normal rows have 11 cells. Scan of the pristine
400-case dump: **0 five-cell rows in 400 cases**. So the boundary at `parse_rows`' malformed-row
test is invisible to the generator's distribution. Hand-made input (registry = header + S001, S002
rows with URLs; staged = header + `| S002 | a | b | c | d |`):

    pristine exit=1  {"collisions": ["S002"], "unmapped": ["S002"], "verdict": "refused", ...}
    mutant   exit=2  {"reason": "staged:3 malformed row S002 (5 cells)", "verdict": "setup_refusal"}

Outputs differ → not equivalent; the generator cannot see this defect class.

### m12 (:443, duplicate-key hook dropped)

The generator's map files are always `json.dumps(case['map'])` of a Python dict
(`pbt-staged-id.py:768`) — duplicate JSON keys are impossible by construction, so the guard's
duplicate-key refusal (`_no_duplicate_keys`, `staged-id-guard.py:406`, wired at :443; the guard's
own T10 selftest covers it) is never exercised. Hand-made map file bytes
`{"map": {"S002": "S010"}, "map": {"S002": "S001"}}` (registry S001 `https://a.test/x`, staged S002
`https://b.test/y`):

    pristine exit=2  {"reason": "map file repeats the key 'map' (as 'map')", "verdict": "setup_refusal"}
    mutant   exit=1  {... "map_clash": ["S001"], "map_ok": false, "verdict": "inadmissible" ...}

Outputs differ → not equivalent; the generator cannot see this defect class.

## Integrity

- Lane `tools/staged-id-guard.py` sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`
  before and after the session — the pinned file was never edited; mutants lived only in scratch.
- No git/jj mutation anywhere; candidate tree obtained read-only via `git archive`; no clone kept.
- Scratch dir deleted before this report was finalised; all cited receipts copied to
  `T49W2MutGuardOwn.receipts/` (26 files: 13 `.out`, 12 `.diff`, 1 `replay.txt`).
- Tooling record: nothing installed or upgraded (stdlib python3 only; host-wide pacman pause
  respected).

## Summary

- Built 12 NEW single-edit mutants of the pinned `tools/staged-id-guard.py` (scratch copies; lane sha256 unchanged before/after) and ran the candidate generator `tools/pbt-staged-id.py` (seed 4949, 400 cases) on each plus a pristine baseline.
- Baseline: 400 cases, 0 violations, all 12 classes ≥ 20 — the candidate generator is sound on the pristine guard.
- 10/12 mutants KILLED (m01-m10: extractor width, id-digit floor, column-zero pattern, http/`www.`/case/trailing-slash document identity, URL-at-start extraction, host-dot openable test, id-length refusal), every kill confirmed by differential replay of the exact dumped case bytes through pristine and mutant guards.
- 2/12 SURVIVED, both proven non-equivalent by hand-made inputs: m11 (5-cell row boundary, exit 1 vs 2) and m12 (duplicate JSON map keys, exit 2 vs 1).
- Coverage findings for C2's method: the generator never emits 5-cell rows (0 in the 400-case dump) and cannot emit duplicate JSON keys by construction (`json.dumps(dict)`, pbt-staged-id.py:768) — two guard behaviours its distribution cannot reach.
- Kill latency is distribution-sensitive (1 to 35 cases across mutants; m09's host-document shape is the rarest) — relevant when reading the hidden panel's 11/12 kill target.
- Nothing here is a verdict; the deciding run is the L1's. Receipts: `T49W2MutGuardOwn.receipts/` (26 files).
