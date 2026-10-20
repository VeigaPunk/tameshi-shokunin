# RX2 — cold-read re-read: `SKILL.md:246-313` (defect-taxonomy templates + exact-string guidance)

Seat RX2 (TameshiR16.RX2). Fresh reader; no prior-range material used.

## Pin verification (before reading)

```
$ git -C <lane> rev-parse HEAD
05a224754db3c6fce18f5ec1816a6873bffe3d0e
$ git -C <lane> show 05a224754…:SKILL.md | sha256sum
e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3  -      # matches the interface sha
$ … | wc -l
1807
```

Range read: **246-313**, exactly one heading (`246:## Defect-taxonomy templates and exact-string guidance`,
next heading at 314). Class: **instruction** (template to write, rules to follow, catalog to read).

Cited artifacts, re-derived from the revisions the section names, never from live working files:

```
$ git -C kumitate-shokunin show 175de6ba…:scripts/kimi-census.mjs > /tmp/…/kimi-census.mjs
83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426   896 lines, 43273 B   # census:13-16 ✓
$ git -C kagi-shokunin show fecee874…:corpus/surface-census.sh > /tmp/…/surface-census.sh
275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f   886 newlines, 44212 B  # census:13-15 ✓
$ tail -c1 surface-census.sh | xxd -p
63                                                                   # 'c': 887th line has no trailing newline (census:14-15 ✓)
```

Tooling: no installs needed (`node v24.21.0`, `sqlite3 3.54.0`, `bash`, `python3` present; `/usr/bin/time`
is absent on this host, so wall time came from Python `time.monotonic`).

## What I executed

1. Re-read every line anchor the section cites in both censuses (`:44-53`, `:82-107`, `:156-166`, `:22-25`,
   `:29-37`; kagi `:14-15`, `:67-76`, `:84-126`, `:204-205`, `:218-236`) — all present, all as cited.
2. Built a 20-defect driver (`/tmp/…/driver.py`) that takes every `old` as a **byte slice of the pinned
   artifact at the cited span** (never retyped from the note), then applies `str.replace(old, new, 1)`.
3. Ran the uniqueness gate, both controls, all 20 mutants, the D2 max-findings probe, and the
   survivor non-equivalence probes.
4. Ran the mechanical rule checks (2, 4, 5) as measurements, not by inspection.

## Entry template — executed

Every defect was formed in the 7-field template. Two worked examples as run (byte slices, not quotes):

```
id:      D8
class:   wrong exit-code mapping
site:    kumitate-shokunin/scripts/kimi-census.mjs:396 at pinned rev 175de6b (sha256 83016d45…4f426)
old:       "  return 2;\n"          # count == 1; the newline is inside old
new:       "  return 1;\n"
why:     a real regression maps the fail-closed path onto the ordinary drift exit
expect:  killed — the three fail-closed cases assert exit 2 (--root /nonexistent, unreadable root, --json)
```

```
id:      B7
class:   off-by-one count / table desync
site:    kagi-shokunin/corpus/surface-census.sh:405-406 at pinned rev fecee87 (sha256 275d8294…53009f)
old:     the printf 'SHAPE UNVERIFIED …' line + "N_UNVERIFIED=$((N_UNVERIFIED + 1)); FAILED=1"
new:     same two lines with N_UNVERIFIED + 2   (the :416 rows_min twin left untouched)
why:     a counting edit that inflates the reported unverified total
expect:  killed — case 10 demands the exact substring "unverified=3"; +2 per event yields "unverified=6"
```

`old` for D4 (lines 351-353) and B4 (lines 200-204) was `new: EMPTY` (block deleted), as the template allows.

## Exact-string rules — measured

**Rule 1 — copy `old` from the pinned artifact; `count(old) == 1`, literal `all unique`.**
`python3 driver.py --check` → `all unique`, exit 0 (20/20: literal count 1, span matches the cited
lines, `old != new`). Also, rule 1's "re-derive on any substrate movement" is live, not hypothetical:
the pinned JS artifact has moved in the substrate —

```
$ sha256sum kumitate-shokunin/scripts/kimi-census.mjs
5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0     # live HEAD, 922 lines
$ git -C kumitate-shokunin show HEAD:scripts/kimi-census.mjs | grep -n 'FROZEN ='
149:const FROZEN = { K1: 3, K2: 26, K3: 9, K4: 9, K5: 3 };            # pinned rev has K2: 25 at :145
```

Re-running the rule-1 gate against live HEAD: 9/10 JS `old` strings still count 1, but **D10's `old`
counts 0** (`K2: 25` no longer exists). The bash artifact has not moved (live sha == pinned sha).
Verdict: the rule is correct and necessary; all my `old`s came from the pinned rev, as the section says.

**Rule 2 — full line when indentation disambiguates (D3, six spaces).**

```
count("      if (!e.children.includes(n)) {\n") == 1
count("  if (!e.children.includes(n)) {\n")     == 1        # two-space substring, also once
mutant via full line sha: 1ea6d77f787cd03a905ac97212cc36b05d5d175c1553ec4e3b09241b24b4f971
mutant via 2-space  sha: 1ea6d77f787cd03a905ac97212cc36b05d5d175c1553ec4e3b09241b24b4f971
byte-identical: True     # context: '      if (e.children.includes(n)) {' (six spaces preserved)
```

**Rule 3 — one behavior per edit.** All 21 mutant files were generated from `pristine` independently;
`diff -u pristine mutant | grep -c '^@@'` = **1 hunk for every one**; 0 duplicate shas among mutants;
no mutant sha equals pristine (driver assert). B7 keeps its `:416` twin untouched, which is what makes
its reading single-mechanism (verified in the byte slice).

**Rule 4 — literal replacement, never regex.** Python `re` against the pinned bytes vs literal count:

| string | regex matches | literal count |
|---|---|---|
| `[[ "$got" -ge "$floor" ]]` (bash) | **153** (`FutureWarning: nested set`) | 1 |
| `slice(0, 6)` (JS) | **0** (silent no-op) | 1 |
| `(mode & m.modeFloor)` (JS) | 1, but span is `mode & m.modeFloor` — parens consumed as grouping | 1 |
| `${n}` (JS) | **0**; only `\$\{n\}` matches | 4 |

The three in-cited-range strings are present exactly where the section says: `slice(0, 6)` at
mutation-case-kimi-census.md:157, `(mode & m.modeFloor)` at :162, `[[ "$got" -ge "$floor" ]]` at
mutation-case-kagi-census.md:221. `${n}` is attributed to **Appendix A's D4**, which is outside my
range; I did not open it (see residual risks). My 20 edits all used `str.replace`, so this remained a
demonstration, not a hazard.

**Rule 5 — byte-level exactness.** `count("  return 2;\n") == 1` (D8; the trailing newline is in `old`).
The bash gate's no-trailing-newline property survived every interior edit: `tail -c1 mutant-B4.sh` and
`mutant-B10.sh` → `63` (`c`). Mutant sha ≠ pristine sha asserted for all 20 (e.g. D8
`0628ed0a02ac…`, B4 `c5f3b2b9d479…`).

**Rule 6 — never compound / never patch after a run.** Each mutant is built from a fresh copy of
`pristine`; a new idea gets a new run id. I hit this rule for real: my first D9 `new` carried one extra
closing paren (`: kind === 'file'))`), so the mutant died at parse (`SyntaxError`, 0.014 s, no suite
line). I did **not** patch that file; I re-cut it from pristine as **D9r2** with the census's own
single-paren form (`? (… : kind === 'file')`), which reproduces the census exactly (below).

## Class catalog — re-executed (20/20 expectations matched)

Controls: JS `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 (0.73-1.18 s);
bash `SELFTEST: PASS (16 cases)`, exit 0, 2 skips (handler absent, as the census records), 1.21-2.01 s.
Cost: JS 10 mutant runs **7.24 s** (census: 7.0 s / 11 runs); bash 10 mutant runs **12.94 s**
(census: 11.0 s / 11 runs) — same shape, ~18 % slower per bash run on this host.

| id | class | exit | suite | observed | fails | failing cases |
|---|---|---|---|---|---|---|
| D1 | off-by-one count / table desync | 1 | 27/43 | killed | 16 | incl. exact green baseline |
| D2 | boundary / truncation cap | 0 | 43/43 | **survived** | 0 | — |
| D3 | inverted condition | 1 | 27/43 | killed | 16 | incl. exact green baseline |
| D4 | dropped arm | 1 | 40/43 | killed | 3 | the three root-enum cases |
| D5 | weakened presence gate | 1 | 42/43 | killed | 1 | `MEMBER_MISSING: the drift chain vanished entirely` |
| D6 | wrong constant pin | 1 | 41/43 | killed | 2 | 0600 floor + FIFO collateral |
| D7 | weakened predicate semantics | 1 | 41/43 | killed | 2 | 0700 floor + 0600 floor |
| D8 | wrong exit-code mapping | 1 | 40/43 | killed | 3 | the three fail-closed cases |
| D10 | reported constant (display-only) | 0 | 43/43 | **survived** | 0 | — |
| D9r2 | weakened type/kind pin | 1 | 41/43 | killed | 2 | FIFO token + dangling symlink |
| B1 | guard inversion | 1 | FAIL 1/16 | killed | 1 | `bad-case 05 undeclared-file` |
| B2 | boundary / truncation cap | 1 | FAIL 2/16 | killed | 2 | `01 clean`, `04 runtime-absent` |
| B3 | inverted condition | 1 | FAIL 3/16 | killed | 3 | `01`, `04`, `06 crosscheck-disagree` |
| B4 | dropped arm | 1 | FAIL 1/16 | killed | 1 | `07 symlink-swap` (token-only) |
| B5 | dropped arm | 0 | PASS 16 | **survived** | 0 | — |
| B6 | boundary / truncation cap | 1 | FAIL 2/16 | killed | 2 | `01`, `04` |
| B7 | off-by-one count / table desync | 1 | FAIL 1/16 | killed | 1 | `10 sqlite-unavailable`, output `unverified=6` |
| B8 | wrong exit-code mapping | 1 | FAIL 2/16 | killed | 2 | `13 malformed-row`, `14 fused-shape-row` |
| B9 | inverted class select | 1 | FAIL 2/16 | killed | 2 | `03 asset-gone`, `04 runtime-absent` |
| B10 | reported constant (display-only) | 0 | PASS 16 | **survived** | 0 | — |

Kill rate **16/20 (8/10 per suite)** — the catalog's headline rows are all reproducible.

## Specific claims re-measured

- **D2 "max 2 vs cap 6"**: instrumented `renderVerdict` entry with `appendFileSync(findings.length)`;
  suite stdout byte-identical to control, still 43/43. Logged **28** text-mode verify runs,
  distribution `0×8, 1×19, 2×1`, **max 2** against the cap 6 at `:378`. ✓
- **D2/D10 non-equivalence** (empty root, 28 findings): pristine `+22 more`, D2 `+23 more`; pristine
  `FAMILY K2 … frozen=25`, D10 `frozen=24`; all exit 1. ✓ (both are real differences the suite cannot see)
- **B4 "token-only kill"**: on a symlink probe fixture, pristine `SURFACE LINK … (declared exec)` exit 1;
  B4 `SURFACE DIVERGED … (declared exec, live symlink)` **exit 1** — same exit code, `SURFACE LINK`
  token gone. ✓
- **B5 "fixture-absent arm"**: `grep -n -- '-x '` → exactly one hit, `:214`, inside the deleted arm; the
  fixture creates the exec row at `chmod 755` (`:707`) and no case strips it. Probe row `asset exec -`
  with a mode-644 file: pristine `SURFACE DIVERGED … (declared exec, no execute bit)` exit 1; B5
  `SURFACE OK … (exec 644)` exit 0. ✓ (real surviving defect, not a no-op)
- **B10 "ok= unasserted"**: `run_case` asserts exit + one substring token only (`:747-760`). Probe
  one-row green fixture: pristine `CLEAN (… ok=1 …)`; B10 `CLEAN (… ok=0 …)`; both exit 0. ✓
- **B7 arithmetic**: mutant output token `unverified=6` against case 10's required `unverified=3`. ✓

## Findings

1. **minor — catalog double-lists D5 under two classes whose edit shapes disagree.** Line 298
   ("dropped arm / delete the arm's reporting/effect lines") cites `D5 → 1`, and line 299 ("weakened
   presence gate / force a presence bool to `true`") cites the same `D5 → 1` (same source line, :48).
   D5 is `const present = gens.length > 0;` → `const present = true;` — no lines are deleted, so it does
   not match the "dropped arm" edit shape. The count (1) is right in both places; a reader designing a
   sweep from the table would produce two different edits for one row. (Related, non-blocking: the
   catalog also re-cuts the census's own labels — the census classes D2 as "off-by-one (findings cap)"
   and D5 as "dropped arm (presence gate)" at :45/:48.)
2. **minor — stale chmod enumeration in the cited B5 block.** The section cites
   `mutation-case-kagi-census.md:105-126` for the fixture-absent survivor; that block says "the only
   chmods are `:521-588`, `:704-717`, `:768`", but `chmod` also appears at **:608** and **:654**
   (`$S/op.env`, `$S/present.env`). Neither touches an exec row, so the B5 conclusion stands
   (independently re-verified above); the parenthetical is just no longer exhaustive.
3. **Not a gap, but load-bearing:** the pinned JS artifact has moved (live sha `5e8d5913…`, 922 lines,
   `K2: 26`); D10's `old` no longer exists there. Rule 1's re-derive clause is what keeps this honest.

**Residual risks / verification gaps.** I did not open `Appendix A` (`${n}` attribution) or
"recipe step 5" — both are outside 246-313 and the interface forbids opening other page ranges; the
rule's substance was verified against the pinned artifact instead (`${n}` literal count 4). The two
`mutate_driver.py` files are scratch-only (not committed in tameshi/kumitate/kagi), so "both drivers"
was verified by re-implementing the prescribed method, not by reading them. Bash fixture probes were
minimal hand-built fixtures in the suite's documented TSV format, not the suite's own builders.
Verbs-path cases 15/16 skipped on this host (handler absent), so verb logic is untouched by this
re-read — consistent with both censuses' U2.

**Verdict:** every numeric and label claim in 246-313 reproduced on the pinned artifacts (16/20 killed,
same four survivors, same case labels); one minor taxonomy inconsistency (D5 double-listed) and one
stale parenthetical in the cited evidence — no blocking gap.

```json
{"seat":"RX2","skill_sha256":"e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3","sections":[{"start":246,"heading":"## Defect-taxonomy templates and exact-string guidance","class":"instruction","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["catalog lines 298-299 double-list D5: the 'dropped arm' row's edit shape (delete the arm's reporting/effect lines) does not match D5's actual edit (const present = gens.length > 0 -> true); counts are correct in both rows","cited evidence block mutation-case-kagi-census.md:105-126 states 'the only chmods are :521-588, :704-717, :768' but chmod also occurs at :608 and :654 (neither touches an exec row; B5 conclusion re-verified independently)"],"commands_executed":["git show 05a224754db3c6fce18f5ec1816a6873bffe3d0e:SKILL.md | sha256sum (e289acec…f794b3)","git -C kumitate-shokunin show 175de6ba…:scripts/kimi-census.mjs | sha256sum (83016d45…4f426)","git -C kagi-shokunin show fecee874…:corpus/surface-census.sh | sha256sum (275d8294…53009f)","python3 driver.py --check -> all unique (20/20, exit 0)","python3 driver.py --run -> control JS 43/43 PASS exit 0; control bash PASS (16 cases) exit 0; kill 16/20; survivors D2,D10,B5,B10","node probe.mjs --selftest -> 28 renderVerdict calls, 0x8/1x19/2x1, max 2 vs cap 6; stdout byte-identical to control","node pristine.mjs|mutant-D2.mjs|mutant-D10.mjs --root empty-root -> +22 vs +23 more; frozen=25 vs 24; exits 1","bash pristine/mutant-B5 verify on exec-no-x fixture -> DIVERGED exit 1 vs OK (exec 644) exit 0","bash pristine/mutant-B10 verify on one-row green fixture -> ok=1 vs ok=0, both exit 0","bash pristine/mutant-B4 verify on symlink fixture -> both exit 1, SURFACE LINK token only on pristine","python3 re vs literal count on pinned bytes: [[ \"$got\" -ge \"$floor\" ]] 153 vs 1; slice(0, 6) 0 vs 1; (mode & m.modeFloor) span excludes parens; ${n} 0 vs 4","diff -u pristine mutant-* | grep -c ^@@ -> 1 hunk each; sha256sum mutants -> 0 duplicates","sha256sum live kumitate kimi-census.mjs -> 5e8d5913… (moved from pinned); grep FROZEN live -> K2: 26"],"opened":["SKILL.md:246-313 (pinned rev 05a22475)","corpus/knowledge/mutation-case-kimi-census.md (pinned rev; lines 1-237)","corpus/knowledge/mutation-case-kagi-census.md (pinned rev; lines 1-258)","kumitate-shokunin/scripts/kimi-census.mjs @ 175de6ba (896 lines, sha256 83016d45…f426)","kagi-shokunin/corpus/surface-census.sh @ fecee874 (886 newlines, sha256 275d8294…009f)","kumitate-shokunin HEAD scripts/kimi-census.mjs (only to test rule-1 substrate movement)"],"scratch":"/tmp/tameshi-r16w2-RX2-pticF0"}]}
```
