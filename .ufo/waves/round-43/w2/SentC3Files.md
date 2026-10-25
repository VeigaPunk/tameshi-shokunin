# SentC3Files — round 43, wave 2: file-handling attack on tools/staged-id-guard.py (C3, operability)

Seat: `L1Tameshi43.SentC3Files` (subagent, leaf — no subagent dispatch). 2026-10-25.
Item: attack `tools/staged-id-guard.py`'s input handling in `/tmp/tameshi-r43-w2-SentC3Files-`:
a FIFO as `--map`, a 2 MiB map, invalid UTF-8, duplicate JSON keys, a directory as `--registry`,
a map whose targets are ints/lists/null, a 5000-digit S-id. For each: exit code, whether stdout
is JSON, whether the process hangs (`timeout 5`). Hold the tool to its docstring: exit 2 and no
traceback for setup refusals.

Method: byte-identical copy of the frozen tool (`sha256 2e8f…6ff2`) at
`/tmp/tameshi-r43-w2-SentC3Files-/bin/guard.py`; every run `python3 -I -B`, under `timeout 5`
(`timeout` in the harness; a run that would exceed 5 s is reported as a hang). Lane checkout
read-only; no tool installed (nothing needed); no counter run at `c5335c7…`; the only lane write
is this file. All evidence is reproduced in `/tmp/tameshi-r43-w2-SentC3Files-/out/` under
`drv.txt`/`drv2.txt`/`results.json`/`strace.txt`.

---

## Result table (the seven assigned inputs)

| input | exit | stdout is JSON | hangs (>5 s) | docstring met? |
|---|---|---|---|---|
| FIFO as `--map` | 2 | yes `{"verdict":"setup_refusal",…}` | no | yes |
| 2 MiB map (> `MAX_MAP` 1 MiB) | 2 | yes | no | yes |
| invalid UTF-8 in map | 2 | yes | no | yes |
| duplicate JSON keys (top-level and nested) | 2 | yes | no | yes |
| directory as `--registry` | 2 | yes | no | yes |
| map targets int / list / null / bool / float / object | 2 | yes | no | yes |
| 5000-digit S-id (key, target, or registry/staged row) | 2 | yes | no | yes |
| **5000-digit *integer* map target** | **1** | **no (stdout empty)** | no | **no — traceback** |
| **deeply nested map JSON (≥ ~52k deep)** | **1** | **no (stdout empty)** | no | **no — traceback** |

All assigned inputs are *refused* correctly: exit 2, a single-line JSON verdict on stdout, a
one-line `staged-id-guard: REFUSED: …` on stderr, no traceback, no hang. The FIFO is refused
because `read_text` stats first (`tools/staged-id-guard.py:432` `os.stat`, `:421`
`S_ISREG`) and refuses non-regular files before any read — even with a writer holding the FIFO
open. The 2 MiB map is refused by `:423` `st_size > limit` (`MAX_MAP` 1 MiB; a map of exactly
1 MiB is admitted). Invalid UTF-8 is refused by the `UnicodeDecodeError` handler in `read_text`
(`:437-439`). Duplicate keys are refused by `_no_duplicate_keys` (`:406-414`, `object_pairs_hook`
at `:443`) at the top level and in nested objects. int/list/null/bool/float/object targets are
refused by `validate_map` (`:203-207`: key/target must be str matching `SID_RE`). The 5000-digit
S-id is refused by `id_number` `:117-124` (`len(sid) > 12` → "S-id too long") in the map key,
the map target, and a row; a 12-char id (`S00000000002`) is *admissible*-bound (names a staged
row the package does not carry → inadmissible, exit 1), which is consistent: the docstring's
`S\d{3,}` is capped at 11 digits by `id_number`.

`timeout 5` never fired (no hang) on any of the seven assigned inputs or any variant below except
where noted.

---
## Findings

### F1 HIGH — first-line BOM silently drops a data row → false-green `verdict: answered` (exit 0)
`read_text` reads with plain `utf-8` (`:434`), so a UTF-8 BOM (`\ufeff`) is left in the text;
`parse_rows`' `ROW_RE` is `^ {0,3}\|\s*(S\d{3,})…` (`:60`, `:78`), so a line that begins with
`\ufeff` never matches and is *silently skipped* — no refusal, no warning, no line number.

Repro (`/tmp/tameshi-r43-w2-SentC3Files-/in/staged_bom.md` — headerless staged package whose first
row collides):
```
printf '\xef\xbb\xbf| S002 | Gamma docs — https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |\n| S004 | Delta docs — https://example.test/delta | … |\n' > staged_bom.md
python3 -I -B tools/staged-id-guard.py --registry reg.md --staged staged_bom.md --json
→ exit 0, "staged_rows": 1 (not 2), "collisions": [], "verdict": "answered", "next_free": "S004"
```
The colliding `S002` row is invisible to the census: the tool answers the append question
green (`answered`, exit 0) exactly when the staged package does collide. The only disclosure is
`staged_rows: 1` compared to the file's real row count — nothing refuses or warns. With a normal
header first, the BOM lands on the header (already skipped) and is harmless; the attack needs the
first *data* line to carry the BOM (headerless package, or a BOM introduced mid-edit), but that
is precisely the redirect the tool exists to catch. The C3 counter's own extractor has the same
blind spot (`.ufo/evidence/round-43/guard/measure.py:114-121`: `read()` with `utf-8`,
`splitlines()`, same `ROW_RE`), so `live_collisions_agree` would confirm the wrong answer —
self-consistent false green. Smallest remediation: strip a leading BOM in `read_text` (or read
`utf-8-sig`) *and* in `measure.py`'s `read`; add a selftest case.

### F2 MEDIUM — two map-JSON shapes escape `load_map`'s handler → bare traceback, exit 1, empty stdout
`load_map` (`:440-445`) catches only `json.JSONDecodeError`. Two valid-JSON inputs raise other
exceptions that propagate out of `main`'s `except Refusal`:
- an integer literal longer than 4300 digits — Python's `sys.set_int_max_str_digits` limit:
  `ValueError: Exceeds the limit (4300 digits) for integer string conversion` — regardless of
  where it sits (`{"map": {"S002": 9999…}}` and a bystander field `{"map": …, "note": 9999…}`
  both crash; the latter is a 5 KB file, well inside `MAX_MAP`);
- an array nested ≥ about 52k deep (binary-searched threshold: first traceback at 52 239,
  max non-crash ≈ 52 046): `RecursionError: Stack overflow … while decoding a JSON array` —
  a ~104 KB file, well inside `MAX_MAP`.

Both: exit 1, `stdout` empty (not JSON), `stderr` ends in the full Python traceback. The
docstring promises exit 1 = "the map is not admissible" and "never a bare traceback"; a crash
conflates with a legitimate verdict and a `--json` consumer gets an empty stdout. The C3 counter
parses stdout defensively (`measure.py:132-137`, `doc=None` on empty → the predicate scores red,
not green), so the counter is not fooled; a human/wrapper reading `exit 1` as "map rejected" is.
Smallest remediation: `except (json.JSONDecodeError, ValueError, RecursionError) as exc:` in
`load_map` (and a guard of nesting depth before `json.loads`).

### F3 MEDIUM — `staged:`-prefixed keys bypass the duplicate-key guard (order-dependent verdict)
`_no_duplicate_keys` compares literal JSON keys, but `validate_map` normalises `staged:S002` →
`S002` (`:203`) *after*; the map has no seen-set on the *bare* id. A hand-authored
`{"map": {"S002": "S010", "staged:S002": "S002"}}` passes the duplicate hook, then the last seen
entry silently overwrites (`mapping[bare] = target`, `:208`) — verdict is *order-dependent*:
`S002 → S010, staged:S002 → S002` ⇒ `inadmissible` (self-map); `staged:S002 → S002, S002 → S010`
⇒ `admitted` (the overwrite hides the self-map). Repro files `in/sd_a.json`, `in/sd_b.json`.
Two spellings of one row should be a refusal under the tool's own promise ("keys accepted as
S153 or staged:S153" — one row, not two). Smallest remediation: track a `bare` seen-set and
refuse a repeated id in `validate_map`.

### F4 LOW-MEDIUM — splitlines() splits on Unicode line separators: same row bytes refused or silently truncated
`parse_rows` iterates `text.splitlines()` (`:80`), which splits not just on `\n`/`\r` but on
U+2028/U+2029, U+0085, `\x0b`, `\x0c`. Row text containing one of those breaks mid-row:
- break before the 6th cell (with <5 cells before it) → `Refusal` "malformed row" (exit 2) —
  fail-safe, but a *valid UTF-8 file* is refused;
- break after the 5th cell → the row is *accepted, truncated*: the cells after the break are
  lost silently (e.g. the URL after a U+2028 disappears → a held row becomes undocumented and
  the analysis flips between `held` and `unmapped`), with no refusal and no disclosure beyond the
  truncated cell count.

Inconsistent handling of one input class; the counter's `own_parse` (`measure.py:114-121`)
shares it, so again the checks agree. Smallest remediation: split on `\n` only (or refuse
non-`\n`/`\r\n` separators), in both the tool and the counter.

### F5 LOW — empty registry/staged is answered, not refused
`--registry empty.md` (or a BOM-only file), `--staged empty.md` → `verdict: answered`, exit 0,
`registry_rows/staged_rows: 0`, `collisions: []`. For a guard whose entire job is "answer before
anything is appended", zero parsed rows means the question was not answered — a wrong-file typo
or a failed export reads as a green light. The data is disclosed in the JSON (`registry_rows: 0`)
but nothing refuses or warns, and the non-JSON mode prints only the verdict line. Smallest
remediation: refuse (exit 2) when a required input parses to 0 rows.

### F6 LOW — structurale: MAX_TEXT/MAX_MAP is a stat-time, name-based pre-check, not bound to the opened descriptor
`strace` of a full run (out/strace.txt) shows `newfstatat(path)` then `openat(path,
O_RDONLY|O_CLOEXEC)` with no `fstat` on the returned fd, no `O_NOFOLLOW`, no `O_NONBLOCK`:
the regular-file and size refusals are two path lookups, so the bytes actually read are never
revalidated. A path swapped between stat and open (file ↔ FIFO) would block forever on `open`,
and a file growing after stat is read past its cap (`handle.read()` has no incremental limit). I
attempted to win both; in practice the window is tiny — 400/400 runs in a 60 s atomic-rename
swap race were refused (the stat won), and the growth case was always caught because the writer
outpaced the gap — so I report this as structural hardening, not a reproduced hang. Smallest
remediation: `os.open(path, O_RDONLY|O_CLOEXEC|O_NONBLOCK)` + `fstat` on the fd (O_NONBLOCK
turns a FIFO open into ENXIO instead of a block; `fstat` re-checks `S_ISREG` and size).

---

## What held up (no findings)
- All seven assigned inputs exit 2 with JSON and no traceback; no `timeout 5` hang anywhere
  (the only `timeout(  observed was an artifact of my own harness polling loop, not the tool —
  re-timed: 16-25 MiB registries parse in 0.45-0.7 s, ~1.9 s with `--map`, and the 32 MiB cap
  is refused at stat in ~30 ms).
- Non-UTF-8 *filenames* (surrogateescape in argv, e.g. `fifo_bad\xffname`) are handled safely:
  stderr uses backslashreplace, `json.dumps` uses `ensure_ascii`; no traceback.
- Map `st_size` exactly 1 MiB is admitted; 1 byte over is refused. `NaN`/`Infinity`/huge-float
  JSON values are refused; a whitespace-only map, an empty map, a list/string/`null` top level,
  `{"map": null}`, and a BOM-prefixed map are all refused with exit 2.
- Symlink to a regular file is accepted (stat follows); symlink to a FIFO refused; `/dev/zero`,
  a directory as `--map`, and `--staged` as a directory all refused with exit 2.
- Duplicate keys are refused at the top level *and* nested (a map's `"map"` object duplicates
  and bystander-object duplicates both refused).
- The 5000-digit S-id in every position is refused with a named reason ("S-id too long"),
  before any other analysis.
- Selftest is green on this Python (3.14.8): 24/24, exit 0; it does not cover F1-F4 (no BOM,
  no ≥4300-digit int, no deep nesting, no `staged:` duplicate).
- The C3 counter swallows a guard crash safely (empty stdout → `doc=None` → predicate red).
