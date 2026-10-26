# Self-mutants of `tools/staged-id-guard.py` against the F10 generator

Round 49, seat `T49ExecGenerator`. Panel authored by this seat (the round's hidden C2 panel is
separate and was not read). Every mutant is the pinned guard
(`sha256 03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`) with **one
exact-string replacement**; the pair is listed so the mutant can be rebuilt byte-exactly.
Each mutant was run through the deliverable generator
`T49ExecGenerator.pbt-staged-id.py` with `--seed 4949 --cases 400` and, for a counterexample, the
same case file was replayed through the pristine guard and the mutant (differential confirmation:
different `(exit, JSON minus registry_sha256/staged_sha256)`).

Command per mutant (scratch tree, `$S=/fast/scratch/hyaku/tameshi-r49/T49ExecGenerator`):

```
python3 -I $S/gen.py --guard $S/mut/<M>.py --seed 4949 --cases 400 --dump $S/w/dump-<M>.jsonl
python3 -I $S/mut/<M>.py --selftest            # the guard's own 24-case fixture selftest
```

## Kills

| # | mutation (exact string → replacement) | generator | counterexample | differential | guard `--selftest` |
|---|---|---|---|---|---|
| M1 | `ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')` → `{0,2}` — census extractor narrowed, an indented collision is missed | exit 1, 4 of 400 cases run | 3 | confirmed | **PASS** (blind) |
| M2 | `COLUMN0_RE = re.compile(r'^\|\s*(S\d{3,})\s*\|')` → `r'^ *\|…'` — column-zero probe accepts any indent, `column0_miss` can never fire | exit 1, 1 case | 0 | confirmed | FAIL |
| M3 | `    text = re.sub(r'^www\.', '', text)` → `    text = text` — a www-form held document is not deduped | exit 1, 13 cases | 12 | confirmed | **PASS** (blind) |
| M4 | `        naive[sid] = 'S%03d' % (top + index)` → `(top + index + 1)` — naive renumber shifted | exit 1, 1 case | 0 | confirmed | FAIL |
| M5 | `        if id_number(target) < id_number(floor):` → `<=` — a fresh id exactly at the floor is refused | exit 1, 39 cases | 38 | confirmed | **PASS** (blind) |
| M6 | `        if len(cells) < 5:` → `< 4` — a four-cell row is accepted as a row | exit 1, 12 cases | 11 | confirmed | **PASS** (blind) |
| M7 | `        if sid in rows:` → `if False and sid in rows:` — duplicate ids accepted in one table | exit 1, 51 cases | 50 | confirmed | **PASS** (blind) |
| M8 | `        'safe_floor': 'S%03d' % (max(top, staged_top) + 1),` → `(top + 1)` — the staged maximum is ignored | exit 1, 6 cases | 5 | confirmed | **PASS** (blind) |
| M9 | `    refused = bool(unmapped) or bool(cascade)` → `bool(cascade)` — an unmapped collision no longer refuses the analysis | exit 1, 1 case | 0 | confirmed | FAIL |
| M11 | `    text = re.sub(r'^https?://', '', text)` → `    text = text` — document identity keeps the scheme | exit 1, 11 cases | 10 | confirmed | FAIL |
| M12 | `    return head if len(head) > 8 and openable else ''` → `len(head) > 0` — a 6-character openable head counts as a document | exit 1, 14 cases | 13 | confirmed | **PASS** (blind) |
| M13 | `    openable = '/' in head or (' ' not in head and` → `    openable = (' ' not in head and` — a path head is openable only by a dotted suffix | exit 1, 9 cases | 8 | confirmed | FAIL |
| M14 | `re.search(r'\.[A-Za-z0-9]{2,6}$', head))` → `{2,}` — the document suffix length is unbounded | exit 1, 40 cases | 39 | confirmed | **PASS** (blind) |

Violation lines, verbatim:

```
M1  VIOLATION index=3 field collision_count: guard 0, oracle 1
M2  VIOLATION index=0 field column0_collisions: guard ['S022'], oracle []
M3  VIOLATION index=12 exit 1, oracle expects 0
M4  VIOLATION index=0 field naive_map: guard {'S022': 'S024'}, oracle {'S022': 'S023'}
M5  VIOLATION index=38 exit 1, oracle expects 0
M6  VIOLATION index=11 exit 0, oracle expects 2
M7  VIOLATION index=50 exit 0, oracle expects 2
M8  VIOLATION index=5 field safe_floor: guard 'S024', oracle 'S025'
M9  VIOLATION index=0 exit 0, oracle expects 1
M11 VIOLATION index=10 field held: guard {}, oracle {'S023': 'S023'}
M12 VIOLATION index=13 exit 0, oracle expects 1
M13 VIOLATION index=8 exit 1, oracle expects 0
M14 VIOLATION index=39 exit 0, oracle expects 1
```

## Non-kill (control)

| # | mutation | generator | why it survives |
|---|---|---|---|
| M10 | `    text = raw.strip().lower()` → `    text = raw.lower().strip()` | exit 0, 400 cases, `violations=0` | semantically equivalent: no input distinguishes `strip` then `lower` from `lower` then `strip`. It is in the panel so that "0 violations" is shown to be a real answer and not a vacuous generator. |

## Reading

* 13 of 14 mutants killed; the one survivor is the deliberate equivalent.
* 8 of the 13 kills (`M1 M3 M5 M6 M7 M8 M12 M14`) **pass the guard's own 24-case `--selftest`**:
  the fixture selftest is blind to them and the property generator is not. That is the F10 claim in
  one line — the generator's surface is not the fixture's surface.
* Each kill is confirmed by differential replay of the counterexample case, so a kill is a real
  behavioural difference, not an oracle opinion.
* Recorded sha256 of the mutant files (scratch, deleted on yield; the string pairs above plus the
  pinned guard rebuild them byte-exactly): `M1 eac4e8a7…`, `M2 e9385081…`, `M3 2665d0ff…`,
  `M4 f5762acc…`, `M5 bfb27e92…`, `M6 48174be5…`, `M7 e1aa259d…`, `M8 2466dfa2…`, `M9 49070d93…`,
  `M10 2af1c90e…`, `M11 c6a9f91c…`, `M12 fc474f63…`, `M13 a8ea1c57…`, `M14 1e61b785…`; each file is
  the pristine 497-line guard with exactly one asserted-unique replacement.

## Generator-side observation recorded while building this panel

`document_key` (`tools/staged-id-guard.py:106`) takes the text **before** the first spaced dash as
the source head:

```
    head = re.split(r'\s+[—–]\s+', source)[0].strip()
```

so a path-like document only counts when it *begins* the source cell (`notes/paper-3.md — note`),
not when it follows a dash (`Src S003 — notes/paper-3.md` → head `Src S003`, 8 characters, fails
`len(head) > 8` at `:113`). The generator's path recipe was wrong on this first and the oracle said
so on the next case; the guard was right. This is why `rec_path_document` puts the document first
and why M12/M14 above are killable at all.
