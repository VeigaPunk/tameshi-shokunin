# T54W2Read16 — cold read at C1

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Candidate: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- Heading: `### Round-14 historical registry — superseded by round 15`
- Span: `start 1623`, `end 1634`
- `section_sha256`: `06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af` (printed by `reader-section.py`, independently reproduced below byte-for-byte)
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Read16` (`TMPDIR`/`HYAKU_SCRATCH` set there)
- Lane files edited: none (read-only seat; deliverables only in `.ufo/waves/round-54/w2/`)
- Tools installed: none needed (no channel change to record)

## Findings (2)

### F1 — run-together token `pins13` (missing space)

- Quote (byte-exact): `historical expected pins13 original inputs`
- Why: `pins13` is a run-together token for `pins 13 original inputs` (the cited round-13 expected file pins exactly 13 inputs), so a cold reader parses a nonexistent identifier instead of a verb plus count (QUALITY 104 missing space).
- Evidence:

```
$ git -C <clone> show C1:SKILL.md | grep -o 'pins13'
pins13

$ python3 -c "... expected.json['inputs'] ..."
expected.json bash keys: ['tools/bash-witness-study.py']     # 13 total keys in inputs
inputs -> dict 13
```

  The cell's claim is otherwise true: `.ufo/evidence/round-13/expected.json` has exactly 13 entries under `inputs`. Only the space is missing.

### F2 — run-together token `round13` (missing space)

- Quote (byte-exact): `unchanged round13 pin manifest and context receipt`
- Why: `round13` is a run-together token for the spaced form this section uses in its own qualifier and rule (`round 17's`, `round 18`) and for the artifact it names, `.ufo/evidence/round-13/pin-manifest.json` (QUALITY 104 missing space).
- Evidence:

```
$ git -C <clone> show C1:SKILL.md | grep -o 'round1[0-9]' | wc -l    -> 6
$ git -C <clone> show C1:SKILL.md | grep -o 'round [0-9]'  | wc -l    -> 168
# within the section itself (line 1627): "live entry since round 18", "round 17's now exits 2"
$ git cat-file -e C1:.ufo/evidence/round-13/pin-manifest.json          -> EXISTS
```

  Same sentence's other anchor resolves: `.ufo/evidence/round-14/context-receipt.json` EXISTS at C1.

## Verified clean (no finding claimed)

- **Entry command runs as written** (`python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`): exists, accepted flags; exits **2** with `expected_input_digest_mismatch` for `tools/bash-witness-study.py`, i.e. the row's own exit class `2 could-not-evaluate invalid/missing/tampered inputs`. Table cell is not stale.
- **Parenthetical claims tested and true**: live entry `.ufo/evidence/round-18/dispositions.json` → exit **0**; `round 17's now exits 2` → round-17 dispositions → exit **2** (`expected_input_digest_mismatch`).
- **Self-test cell**: `python3 tools/evidence-disposition.py --selftest` → exit **0**, `SELFTEST: PASS (66/66)`; the tool carries literal isolated expectations (`SELFTEST_CASE ...`), matching `literal isolated selftest expectations in tool`.
- **Verdict map** matches the tool docstring (`0 clean / 1 semantic / 2 could-not-evaluate / 64 usage`); `usage` → 64 also exercised by the selftest cases.
- **Row 2 anchors**: `.ufo/evidence/round-14/capture-context.py` EXISTS; it has `USAGE = "usage: capture-context.py"` and rejects unexpected args, with no `--selftest`, so `historical helper-only controls do not satisfy the standalone gate selftest` is consistent. It reads `.ufo/evidence/round-13/expected.json` and writes `.ufo/evidence/round-14/context-receipt.json`, matching `unchanged round13 pin manifest and context receipt`.
- **`before counterpart` resolves**: `.ufo/evidence/round-14/dispositions-before.json` (same `expected_file` and 3 inputs) and `.ufo/evidence/round-14/before.json` exist.
- **Structure/typography**: 8 header cells = 9 pipes on every table line; backticks even on every line (8 and 2); no tabs, CR, double spaces or trailing whitespace; only non-ASCII char is the heading em dash `—`.
- **No self-contradiction**: heading "superseded by round 15" vs row-1 live entry "since round 18" is a later move, not a conflict; row 1's command is explicitly labelled historical; row 2 is "historical gate, not active".

## Observations not claimed (kept out of `findings`)

- `round 17's now exits 2, bash-witness moved` — the exit-2 fact is verified. The causal gloss "moved" is imprecise: the path `tools/bash-witness-study.py` is unchanged (present in the round-17 tree and at C1; no rename anywhere in lane history, and `tools/bash-witness.py` never existed), and the observed failure is a content `expected_input_digest_mismatch` (pin `49e9e5e2…` vs C1 sha256 `f2bb50c7…`). Not reported because the actionable claim (exit 2) is correct and "moved" is used doc-wide as shorthand for pinned-byte drift (cf. the later registry row); a cold executor is not misled about the exit class.

## Artifacts opened

- `tameshi-shokunin/SKILL.md` @ `99c3bc8…`, lines 1623–1634 (section bytes) and bordered context 1615–1645; also line 1707 (later registry row, comparison only) and line 1621 (`round15` occurrence, outside section)
- `tameshi-shokunin/.ufo/waves/round-54/reader-section.py`
- `tameshi-shokunin/.ufo/evidence/round-18/measure.py` (`sectionize`, used to reproduce the sha)
- `tameshi-shokunin/tools/evidence-disposition.py` (usage/exit-class docstring, `expected_input_digest_mismatch` emitter, selftest cases)
- `tameshi-shokunin/.ufo/evidence/round-14/{dispositions.json, dispositions-before.json, before.json, capture-context.py, context-receipt.json}`
- `tameshi-shokunin/.ufo/evidence/round-13/{expected.json, pin-manifest.json}`
- `tameshi-shokunin/.ufo/evidence/round-17/dispositions.json`, `tameshi-shokunin/.ufo/evidence/round-18/dispositions.json`

## Commands run

Scratch setup (per wave discipline):

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r54/T54W2Read16; mkdir -p "$S"; export TMPDIR="$S"
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 .ufo/waves/round-54/reader-section.py "$PWD" 99c3bc88d704566197783f66b211ee0a830e0330 \
  "### Round-14 historical registry — superseded by round 15"
# -> {"start": 1623, "end": 1634, "section_sha256": "06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af"}
```

Byte extraction and reproduction of the frozen sha (no lane writes):

```
git -C <lane> show 99c3bc8:SKILL.md | sed -n '1623,1634p' | cat -A
python3 - <<'PY'   # split on '\n', strip trailing blank lines, join '\n'
... hashlib.sha256(body.encode('utf-8','surrogateescape')).hexdigest()
PY
# -> start 1623 end 1634 sha 06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af len 1641
# -> quote pins13: True ; quote round13: True
```

Fixture clone and read-only checks (all git calls with `-C "$D"`; no lane mutation):

```
D=$(mktemp -d "$S/clone.XXXXXX")
git clone --shared --quiet <lane> "$D/lane"
git -C "$D/lane" checkout --quiet --detach 99c3bc88d704566197783f66b211ee0a830e0330   # rev-parse HEAD = C1
cd "$D/lane"
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json   # exit 2, digest mismatch
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json   # exit 2
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json   # exit 0
python3 tools/evidence-disposition.py --selftest                                                                # exit 0, PASS (66/66)
git -C "$D/lane" ls-tree --name-only 99c3bc8:.ufo/evidence/round-14/
git -C "$D/lane" ls-tree --name-only 99c3bc8:.ufo/evidence/round-13/
git -C "$D/lane" log --oneline -- tools/bash-witness-study.py
git -C "$D/lane" log --all --oneline -- tools/bash-witness.py          # empty: path never existed
git -C "$D/lane" cat-file -e 99c3bc8:tools/bash-witness.py             # MISSING
git -C "$D/lane" cat-file -e 99c3bc8:.ufo/evidence/round-13/pin-manifest.json       # EXISTS
git -C "$D/lane" cat-file -e 99c3bc8:.ufo/evidence/round-14/context-receipt.json    # EXISTS
sha256sum of tools/bash-witness-study.py at 9df9212/4acc607/58e5d53/370f2df/218bc6b/5b703c6
# -> 49e9e5e2… occurs exactly at 4acc607 (round 13); C1 content = f2bb50c7…
```

Structural sweep over the exact section bytes: pipe counts (9 per table line), backtick parity (even), run-together-token regex (`python3`, `pins13`, `round13` only), non-ASCII set (`—` only), tabs/CR/double-space/trailing-whitespace scan (none).

## Scope and limits

- Read-only outside `.ufo/waves/round-54/w2/`; no lane production file, counter, contract, freeze, ledger or wave spec touched; no mutating git/jj command run anywhere.
- Wave-1 reader JSONs were not opened; verdict-independent read of the C1 bytes only.
- Section is byte-identical to C0 (diff of the extracted block between `59c3810` and `99c3bc8` is empty), i.e. the C1 fix pass did not touch this block; both findings ship at C1.
- Not in scope for this seat and not run: census validator, both frozen counters, contract/freeze checks.
