# CriticV1Control — v1-pattern control on planted fixtures

## Scope
Contract predicate under test (`.ufo/evidence/round-40/contract.json#EF33`, C1):
"embedded v1 patterns score bytes_unflagged=0 and replace writes=0 on those two
planted cases". Attempted falsification: could the embedded v1 regexes flag or
count a write on `bytes_unflagged` / `replace_unflagged`, which would make the
v1-miss clause and the `--control` do-nothing path vacuous?

## Finding — holds (not falsified)

Command run:

    $ python3 .ufo/evidence/round-40/census/measure.py \
        --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --control
    C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false
    exit=1

Direct `v1_classify` replay (scratch copy at /tmp/tameshi-r40-CriticV1Control/,
all five planted fixtures):

    bytes_unflagged    writes=1 unflagged=0
    bytes_flagged      writes=1 unflagged=0
    replace_unflagged  writes=0 unflagged=0
    replace_flagged    writes=0 unflagged=0
    scratch_replace    writes=0 unflagged=0

## Mechanism (path:line)

- `.ufo/evidence/round-40/census/measure.py:33-37` — `V1_WRITE_RE` covers only
  `open(...'w'/'a'/'wb'...)`, `.write_text(`, `.write_bytes(`. It has no
  `os.replace` alternative, so the `replace_unflagged` fixture
  `os.replace(tmp, 'case.expected')` scores `writes=0`.
- `.ufo/evidence/round-40/census/measure.py:38-40` — `V1_EXPECTED_RE` requires
  `\.expected\b` (leading dot), `expected\.txt`, `golden`, or `snapshot` inside
  quotes. `'expected.json'` matches none, so the `bytes_unflagged` write line
  `(out / 'expected.json').write_bytes(b'x')` scores `unflagged=0` despite
  `writes=1`.
- `.ufo/evidence/round-40/census/measure.py:187-188` — the counter itself
  computes `v1_bytes = v1_classify(planted['bytes_unflagged'])[1]` and
  `v1_replace_writes = v1_classify(planted['replace_unflagged'])[0]`; both are
  0, so `v1_misses` (line 220) is a real gate, not vacuous.
- `.ufo/evidence/round-40/census/measure.py:96-99` — `--control` encodes the
  same v2 target (`bytes_u == 1 and replace_w >= 1`); v1 emits 0s and the
  control exits 1. The do-nothing path is excluded as the contract intends.

## Consequence
Embedded v1 patterns score `bytes_unflagged=0` and `replace_writes=0` on the
planted fixtures and cannot meet the v2 target (both classes at 1). The
`v1_misses` clause (measure.py:220) is computed from the counter's own embedded
v1 regexes, not the submitted tool; it is what bars a v1-equivalent tool from
reaching `planted bytes_unflagged=1 and replace_unflagged=1`. Confirmed sound.

## Note (not a defect)
`--control`'s `meets` expression adds `v1_replace_unflagged == 1`
(measure.py:99), stricter than the stated v2 target of "both new classes at 1".
Since v1 scores 0 everywhere this only strengthens the control's rejection; the
target is still unreachable for v1.

No installs performed; pacman untouched. Live lane checkout unmodified; all
replays ran against scratch copies under /tmp/tameshi-r40-CriticV1Control/.
