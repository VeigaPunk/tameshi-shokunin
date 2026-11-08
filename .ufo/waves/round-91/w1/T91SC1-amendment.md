# Round-91 amendment block — `corpus/knowledge/mutation-case-fleet-sources-census.md` (draft, seat T91SC1)

Integration draft for the L1 (TameshiR91). Nothing in this file is landed; the case note,
`corpus/SOURCES.md` and `corpus/lessons/` are untouched by this seat. The three parts below are
the amendment the sealed counter `C1_R91_PASS=true` requires at the landing revision, plus the
one companion landing the same counter requires outside the note.

Provenance of the evidence in this draft: the frozen plan
`plans/round-91.plan.md`; the sealed counter `.ufo/evidence/round-91/c1/measure-v91.py`; the
frozen spec `.ufo/evidence/round-91/c1/census-mutants.json` (sha256 `ce8983d5…e290`, bytes
identical to round 90's); the L1's own S318 snapshot `.ufo/evidence/round-91/sources/git-env.txt`
(+ `.html`, `.headers`) as committed in `ace200b5`. This seat did **not** fetch S318; it quotes
the L1's snapshot. Verification of this draft: `T91SC1-amendment-probe.py` /
`T91SC1-amendment-probe.out` (same directory), which builds a scratch fixture clone, applies
exactly Parts A+B and the companion row, and runs both frozen counters — at the fixture rev
`5425a392…` it prints `C1_R91_PASS=true` (exit 0, every conjunct true, `source=true`) and
`C2_R91_PASS=true` (exit 0), against `C1_R91_PASS=false` (`source=false`) on the unamended lane.

---

## 0. The note-side contract this amendment must satisfy (read before editing)

Five behaviours of the frozen counter decide the shape of every block below. All five were
re-derived by running the counter's own code, not by reading its prose.

| what the counter does | code | consequence for this amendment |
|---|---|---|
| reads the verdict column **by header name**: the first line whose pipe-split cells contain a cell equal to `verdict` (after strip+lower) fixes the column index | `measure-v91.py:135-137` (`parse_note`) | the header cell must stay the literal word `verdict`; the data rows must keep the verdict at that same index |
| refuses an **ambiguous** id-keyed row (duplicate, missing, or a value outside `{KILLED, SURVIVED}`) — it does not skip | `measure-v91.py:149-151`, `:264` (`ids_ok = (len(ambiguous) == 0) and …`) | exactly ONE copy of the twelve `C01…C12` rows may exist in the note |
| skips fenced code blocks (```), so a fenced sample can never pose as a row | `measure-v91.py:123-130` (`in_fence`) | a fenced copy of the table is inert to the row parser |
| requires exactly ONE line starting with `source:` — otherwise `cited = set()` | `measure-v91.py:268-269` | the S318 citation must be folded INTO the existing line, never added as a second line. **This scan is fence-blind**: a `source:` line inside a fence also counts |
| requires exactly ONE `measured: K/N killed` line equal to the derived counts | `measure-v91.py:266-267` | never restate the measured line anywhere in the note. **This scan is fence-blind too** |

Two hard consequences, both reproduced below in §4:
1. Appending a second copy of the verdict table (unfenced) makes all twelve ids ambiguous →
   `ids=false` → the counter refuses. This is the VOV1-dup-row control.
2. Adding a second `source:` line (fenced or not) zeroes `source`; adding a second `measured:`
   line makes `figure=false`. Both were measured on the current note bytes (§4).

Coverage needs no edit: `corpus/README.md` already carries the row naming this note
(`corpus/README.md:721`, the round-90 coverage-map table), and the counter's `coverage`
conjunct is already `true` at lane HEAD (receipt: `T91SC1-amendment-probe.out`, BEFORE run).

---

## Part A — the `source:` line (REPLACE note line 1; do NOT append)

The counter reads only `src[0]`, and only when the note has exactly one line starting with
`source:`. The note's line 1 currently cites S001, S316, S317 — **not S318**; the `source`
conjunct is `false` at lane HEAD because of that alone (BEFORE run, `C1_CONJUNCTS … source=false`).
So Part A is a one-line **substitution**, byte-exact.

- old line (no trailing newline): 695 bytes, sha256 `8d95fedac83fae3ce2d238f64a798be6b6c69b8c9071763a07da6dfe39bf460e`
- new line (no trailing newline): 1052 bytes, sha256 `399545af878ce016dda34a3eb568e686f4d87bce0d0e8d75837a743b3741e475`

The whole replacement line, byte-exact (fence markers are presentation only — copy the single
line between them):

```text
source: S316 gawk(1), `sub()` replacement `&` (docs, tier A, mined, opened 2026-11-06) — https://man.archlinux.org/man/gawk.1.en, `.ufo/evidence/round-90/sources/s-gawk1.txt:1026-1028`: "An & in the replacement text is replaced with the text that was actually matched" (grounds C09); S317 bash(1), `-e`/`-f` (docs, tier A, mined, opened 2026-11-06) — https://man.archlinux.org/man/bash.1.en, `.ufo/evidence/round-90/sources/s-bash1.txt:3197-3200`: "True if file exists and is a regular file" (grounds C08); S318 git(1), `GIT_NO_REPLACE_OBJECTS` (docs, tier A, mined, opened 2026-11-08) — https://git-scm.com/docs/git, `.ufo/evidence/round-91/sources/git-env.txt:1413-1415`: "Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects." (grounds the sealed counter's `GIT_NO_REPLACE_OBJECTS=1` read path); S001 Stryker mutant states and metrics — relied on only for the `detected / valid` arithmetic behind 5/12; fleet `scripts/sources-census.sh` @ `f47ad6ba` (the pinned gate, read-only)
```

What the new clause is, and where each piece comes from:

| piece | value | source |
|---|---|---|
| id + document | `S318 git(1), `GIT_NO_REPLACE_OBJECTS`` | the L1 opened S318 this round |
| tier/kind/status/opened | `(docs, tier A, mined, opened 2026-11-08)` | matches the note's own S316/S317 clause style; the S318 registry row in the companion block |
| URL | `https://git-scm.com/docs/git` | the L1's snapshot: `git-env.html` is the git(1) manual page (`NAME` → "git - the stupid content tracker", `Environment Variables` section), fetched per `.ufo/evidence/round-91/sources/git-env.headers` (`date: Sun, 08 Nov 2026 02:04:29 GMT`) |
| locator | `.ufo/evidence/round-91/sources/git-env.txt:1413-1415` | the L1's snapshot, lines verified: `1413` `GIT_NO_REPLACE_OBJECTS`, `1414-1415` the sentence |
| quote | "Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects." | **18 words** (≤ 25), verbatim from `git-env.txt:1414-1415` with the hard line break joined by one space |
| grounds | the sealed counter's `GIT_NO_REPLACE_OBJECTS=1` read path | the counter's `sealed_env()` (`measure-v91.py:38-44`) sets `GIT_NO_REPLACE_OBJECTS=1` plus `GIT_CONFIG_NOSYSTEM=1` / `GIT_CONFIG_GLOBAL=/dev/null` on every `git` call |

Why the quote is that sentence and not the `--no-replace-objects` option text: the sealing the
round's claim rests on is the *environment variable* (`GIT_NO_REPLACE_OBJECTS=1` on every read),
and `git-env.txt:1413-1415` is that variable's own entry. The option text at
`git-env.txt:484-487` ("This is equivalent to exporting the GIT_NO_REPLACE_OBJECTS environment
variable with any value.") is the same fact stated from the flag side; it is corroboration, not
a second row.

**S-ids cited by the resulting line**: `S001, S316, S317, S318`. The counter examines only
S318 (`if int(sid) != SOURCE_SID: continue`), so keeping S001/S316/S317 is harmless and correct —
they are the note's grounds for C09 and C08.

**Do not add `S318` anywhere else on a line starting with `source:`.** See §4 for the measurement.

---

## Part B — the admission-status appendix (APPEND at end of note, byte-for-byte)

This is the C2 repair's own block: the **not-admitted marker** (round-90 routed item 1) and the
**coverage back-citation** (routed item 2) are carried by this one section. The bytes must match
`.ufo/evidence/round-91/c2/fixes-v91.py`'s `NOTE_APPEND` **byte-for-byte**:

- 620 bytes (UTF-8), 614 characters, sha256 `0afa5192e809bfa0774a7a623e47fdddb60e95cf117db680291299554768957b`
- starts with one `\n` (so it opens with a blank line after the note's existing last line)
- ends with `…not on the measured table.\n`

Exact bytes (the fence markers are presentation only; the block starts with a blank line and is
NOT fenced in the note):

```markdown

## Admission status (appended round 91)

Appended; the entry above is unchanged. Its coverage-map row is
`corpus/README.md` § "Round 90 — coverage map: the fleet's own registry gate"
(R90-C1). This row carries **not admitted**: R90-C1 was killed by its own frozen
rule (a) — the round-90 counter honoured `refs/replace` (T90R1 K2) and skipped an
ambiguous id-keyed row (T90R1 K1) (`lessons/round-90-verifier-spotcheck.md` §2.3).
The verdicts above were independently reproduced (T90E1, T90L1) and are stated as
measurements in this note; the kill is on the counter that certified them,
not on the measured table.
```

The safest way to land these bytes is to let the frozen generator write them, so identity is by
construction rather than by transcription:

```sh
python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-91/c2/fixes-v91.py \
  --target <lane checkout>            # default --variant pos; appends NOTE_APPEND to this note
                                      # and LESSON_APPEND to corpus/lessons/round-90.md
```

Tokens this block supplies (the two `doc-contains` rows of `tools/defect-bind-r91.json`, both in
section `## Admission status (appended round 91)`):

| manifest row | tokens | present in the block |
|---|---|---|
| `R90-1-not-admitted-marker` | `This row carries **not admitted**`, `killed by its own frozen` | yes (byte-checked) |
| `R90-2-entry-cites-coverage-row` | `corpus/README.md`, `Round 90 — coverage map: the fleet's own registry gate` (U+2014 em dash), `killed by its own frozen` | yes (byte-checked) |

Parser safety of this block, measured: it contains no `|` at all, no line starting with
`source:`, no line matching `^measured: \d+/\d+ killed$`, no `^\|\s*C\d\d\s*\|` row, no cell
equal to `verdict`, and no ``` fence marker. It is inert to every note-side conjunct.

---

## Part C — the verdict table the note carries (UNCHANGED — verification copy, not an append)

The note's §1 table stays exactly where it is and is not edited. Its header row is spelled out
here because the frozen parser binds the verdict column **by that name**, not by position:

```text
| id | arm targeted | edit | verdict | witness |
|---|---|---|---|---|
| C01 | E10 community-at-A | `:668` `kind=="community"` → `kind=="communityX"` | KILLED | validate; one community row at tier A (S001) |
| C02 | W02 thin-reject length boundary | `:671` `length(teaches)<8` → `<7` | SURVIVED | validate; one rejected row, teaches `1234567` (7 chars) |
| C03 | E04 supersedes exemption id width | `:648` `/supersedes S[0-9]{3}/` → `{4}` | SURVIVED | validate; S002 teaches `supersedes S001 with newer text` |
| C04 | overdue due-day boundary | `:684` `due<=today_s` → `due<today_s` | KILLED | overdue; opened 2026-10-07 + 30d = `--today` 2026-11-06 |
| C05 | E08 opened-today boundary | `:661` `opened_epoch>today_s` → `>=` | KILLED | validate; one row opened 2026-11-06 = `--today` |
| C06 | separator row with alignment colons | `:596` `^:?-+:?$` → `^-+$` | SURVIVED | census; separator `:---` / `:---:` / `---:` over one row |
| C07 | awk row-indent width 0-3 | `:615` bound `{0,3}` → `{0,2}` | KILLED | census; header, separator and row indented three spaces |
| C08 | E11 used-by existence test (`-e`) | `:566` `! -e "$dir/$path"` → `! -f` | SURVIVED | validate; used-by `corpus/knowledge` (a directory) |
| C09 | URL fragment normalization | `:602` `sub(/#[^ ]*$/,"",u)` → `"&"` | SURVIVED | validate; two rows `…/p#a` and `…/p#b`, same scope |
| C10 | symbolic cadence with spaces | `:582` class `[A-Za-z0-9 _-]` → `[A-Za-z0-9_-]` | SURVIVED | validate; recheck `on next release` |
| C11 | missing-registry exit 2 | `:804` `[ "$missing_error" = 1 ] && exit 2` → `exit 1` | KILLED | validate; no `corpus/SOURCES.md` at all |
| C12 | used-by comma-list trimming | `:564` `path=$(trim_cell "$path")` → `path=$path` | SURVIVED | validate; used-by `corpus/a.md, corpus/b.md`, both present |
```

How the header-named parser binds it (measured with `parse_note` over the amended note):

- header pipe-split: `['', 'id', 'arm targeted', 'edit', 'verdict', 'witness', '']` → `vcol = 4`
- each data row's `cells[4]` is the verdict cell (`KILLED`/`SURVIVED`); both agree at index 4, so
  no column shift
- result on the amended fixture: `rows=12`, `ambiguous=[]`, and
  `C01=KILLED, C02=SURVIVED, C03=SURVIVED, C04=KILLED, C05=KILLED, C06=SURVIVED, C07=KILLED,
  C08=SURVIVED, C09=SURVIVED, C10=SURVIVED, C11=KILLED, C12=SURVIVED`

Three rules for the landing, each backed by a measurement in §4:

1. **The header cell must remain the literal word `verdict`.** The parser sets `vcol` from the
   first cell whose stripped lowercase form equals `verdict`. Rename it (`outcome`, `result`,
   `verdict (K/S)`) and `vcol` stays `None`, every `C\d\d` row becomes ambiguous, and the note is
   refused — the VOV3-draft-column class.
2. **Exactly one copy of the twelve rows, unfenced.** A second unfenced copy makes all twelve ids
   ambiguous (`if cid in rows: ambiguous.append(cid)`) and `ids=false`.
3. **The block above is a verification copy only — do not append it to the note.** The note's
   existing §1 table is the live one. If a copy is ever needed inside the note, it must be inside
   a ``` fence (the parser skips fenced lines) **and** must not carry a `measured:` line or a
   `source:` line (those two scans are fence-blind, §4).

---

## Companion landing the same counter requires (NOT part of the note)

`C1_R91_PASS=true` needs one more thing that does not live in the note: the `source` conjunct only
counts S318 if `corpus/SOURCES.md` carries a row with `c[1] == "S318"`, `c[8] == "mined"` and the
note path `corpus/knowledge/mutation-case-fleet-sources-census.md` inside `c[11]` (used-by)
(`measure-v91.py:270-279`). With Part A alone and no registry row, `source` stays `false` —
measured, §4.

**Companion row for `corpus/SOURCES.md`** (insert after the last `| S###` registry row — currently
line 193, S317; the `## Registry` section ends at `## Paths` on line 195. Inserting there leaves
every committed `corpus/SOURCES.md:L` pointer intact: `tools/pointer-recheck.json` holds live
pointers at `:140`, `:141`, `:142` and `:178`, all above the insertion point, and
`tools/defect-bind.json` binds S289's used-by cell and the `## Search log` section, neither of
which the new row touches. 11 columns / 13 pipe-split cells, as the counter and the census gate
both require):

```text
| S318 | git(1) — Git Documentation (git-scm.com; Git 2.56.0) — https://git-scm.com/docs/git | docs | A | git's own statement that GIT_NO_REPLACE_OBJECTS makes git ignore replacement refs and not replace Git objects | ENVIRONMENT VARIABLES, the GIT_NO_REPLACE_OBJECTS entry (tag-stripped snapshot line 1413-1415) @ page fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 02:04:29 GMT) | "Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects." (18 words) — the sealing ground for the round-91 counter: with GIT_NO_REPLACE_OBJECTS=1 every git read ignores replacement refs, so a `git replace` ref cannot swap the bytes a counter reads | mined | 2026-11-08 | 365d | corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-91.md |
```

**Companion row for `corpus/lessons/round-91.md` § Gate** — the plan's kill rule (d) requires a
Gate row carrying the URL, the access date and a located quote of ≤ 25 words for the cited new
S-id. Suggested row (this seat does not write the lesson):

```text
| S318 git(1), GIT_NO_REPLACE_OBJECTS | admit (A, `mined`) | https://git-scm.com/docs/git, fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 02:04:29 GMT` (`.ufo/evidence/round-91/sources/git-env.html`, text `git-env.txt`) | "Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects." (18 words, `git-env.txt:1413-1415`): the sealing ground for the round-91 counter's `GIT_NO_REPLACE_OBJECTS=1` read path. Cited by the case note. |
```

Three landing hazards, all measured or read from the frozen artifacts:

1. **E11 / the round-90 M6 recurrence.** The census gate's `usedby_findings` requires every
   used-by path of a **mined** row to exist on disk (`[ ! -e "$dir/$path" ]` → `E11`). So
   `corpus/lessons/round-91.md` must be committed in the **same commit** as the S318 row, or the
   lane's own census prints `E11 S318 missing used-by corpus/lessons/round-91.md` and exits 1 —
   exactly the round-90 M6 mistake ("land the lesson in the same commit as rows that cite it").
   If the lesson cannot land with it, drop `corpus/lessons/round-91.md` from used-by for that
   commit; the counter only needs the note path in used-by.
2. **W04, not E04.** S318's URL `git-scm.com/docs/git` is already held by S063 with a different
   scope, so the gate prints `W04 S318 duplicate url git-scm.com/docs/git across scopes`. That is
   a warning: `W-codes … never change status`, and the lane's validate still exits 0 (the lane
   already carries 19 such W04 rows). It is **not** `E04`, which fires only when URL *and* scope
   both match an existing non-rejected row.
3. **`opened: 2026-11-08` is `E08`-clean** (`E08` fires only when `epoch(opened) > today`), and
   `recheck: 365d` is `E09`-clean.

---

## Landing recipe (ordered)

1. Apply **Part B** with the frozen generator (`fixes-v91.py --target <lane>`); it writes the
   note appendix and the `corpus/lessons/round-90.md` receipt addendum in one pass. Two cautions,
   both the round-90 M7 defect class (evidence pointer `T90SN1.md` F1/F2/F3): it **appends
   unconditionally** (no existence guard), so run it exactly once — a second run lands a duplicate
   admission-status section; and `--target ""` resolves through `os.path.realpath("")` to the
   caller's **cwd**, so pass an explicit absolute lane path.
2. Apply **Part A**: replace note line 1 with the byte-exact line above. Check
   `sha256 == 399545af878ce016dda34a3eb568e686f4d87bce0d0e8d75837a743b3741e475`.
3. Land the **S318 registry row** in `corpus/SOURCES.md` and, in the same commit,
   `corpus/lessons/round-91.md` with its S318 Gate row (hazard 1 above).
4. Leave **Part C** untouched (the note's §1 table), the single `measured: 5/12 killed` line, and
   the `corpus/README.md:721` coverage row as they are.
5. Verify at the landing revision:
   `python3 -I .ufo/evidence/round-91/c1/measure-v91.py --repo <lane> --rev <REV> --work <empty dir>`
   → every conjunct `true`, `C1_R91_PASS=true`, exit 0; and
   `bash .ufo/evidence/round-91/c2/measure-c2-v91.sh <lane> <REV> <empty dir>`
   → `C2_R91_PASS=true`, exit 0.

Optional, not read by any counter — the note's `verified-at:`/`recheck:` lines (note lines 2–3)
still name the **round-90** instrument (`…/round-90/c1/measure.py`, `C1_R90_PASS=true`) and the
round-90 spec path. That is historically true but stale as a re-check pointer, since round 91's
live counter is `measure-v91.py` against `.ufo/evidence/round-91/c1/census-mutants.json` (same
bytes, same sha256 `ce8983d5…e290`). If the L1 wants the note to re-check itself against the
sealed successor, replace those two lines' counter reference accordingly; no conjunct changes
either way.

---

## 4. Measurements behind the rules above (re-runnable)

Reverse-engineered with the frozen parser itself (`measure-v91.py:parse_note`) plus the counter's
own two scans, applied to the current note bytes. `T91SC1-amendment-probe.py` reproduces the
first four rows and runs both frozen counters end to end.

| variant applied to the note | `rows` | `ambiguous` | `source:` lines | `measured:` heads | verdict |
|---|---|---|---|---|---|
| lane HEAD, no amendment | 12 | `[]` | 1 (cites S001/S316/S317) | 1 | `source=false` → C1 refused |
| + Part A (source line cites S318) + Part B, + companion row | 12 | `[]` | 1 (cites …/S318) | 1 | all conjuncts true — `C1_R91_PASS=true` and `C2_R91_PASS=true` in `T91SC1-amendment-probe.out` |
| + a second `source: …` line (fenced **or** unfenced) | 12 | `[]` | **2** → `cited = set()` | 1 | `source=false` |
| + a second `measured: 5/12 killed` line | 12 | `[]` | 1 | **2** | `figure=false` |
| + a second copy of the twelve rows, **unfenced** | 12 | **all twelve ids** | 1 | 1 | `ids=false` (refused, never skipped) |
| + a second copy of the twelve rows, **fenced** | 12 | `[]` | 1 | 1 | ids survive (parser skips fences) |

The last two rows are why Part C is a verification copy and not an append: the note's live table
must remain the only unfenced one.

---

## 5. Landed shape, in one line each

- line 1: one `source:` line citing S001/S316/S317/**S318** (Part A, substitution).
- §1: the twelve `C01…C12` rows, header `| id | arm targeted | edit | verdict | witness |`, the
  single `measured: 5/12 killed` line — unchanged (Part C).
- tail: the `## Admission status (appended round 91)` section, 620 bytes, sha256
  `0afa5192…957b` (Part B).
- outside the note: `corpus/SOURCES.md` S318 row + `corpus/lessons/round-91.md` Gate row.
- `corpus/README.md`: untouched (the coverage row already exists at line 721).

TOOLS: none
VERDICT: drafted
