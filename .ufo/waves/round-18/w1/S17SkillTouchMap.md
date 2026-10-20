# S17 — SKILL.md touch map for round 18 (lane tip `183f87b`)

Measured revision: `183f87b899e6cae46be98d251cbc87fb5118f6ca` (branch `master`,
lane `tameshi-shokunin`). Every lane byte below was read through
`git show <rev>:<path>`; no lane file was opened from the worktree, no lane git
state was written. Scratch: `/tmp/tameshi-r18w1-S17SkillTouchMap-3T00pb`
(`mktemp -d /tmp/tameshi-r18w1-S17SkillTouchMap-XXXXXX`).

## Evidence base

```
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
W=/tmp/tameshi-r18w1-S17SkillTouchMap-3T00pb
$ git -C "$L" show 183f87b899e6cae46be98d251cbc87fb5118f6ca:SKILL.md > "$W/SKILL.md"
exit 0; wc -l -> 1903
$ grep -n '^#' "$W/SKILL.md"                   # 62 lines starting '#', incl. fence-internal
                                               # shell comments; last heading :1897
$ grep -c 'timeout_s' $W/SKILL.md              -> 0
$ grep -n 'G[0-9]' $W/SKILL.md                 -> exit 1 (no match)
$ git -C L cat-file -e REV:tools/trace-inputs.py
  fatal: path 'tools/trace-inputs.py' exists on disk, but not in '<rev>'; exit 128
$ git -C L cat-file -e REV:.ufo/evidence/round-17/coldread/trace-inputs.py; exit 0
```

LSP: no language server answers Markdown in this workspace and `lsp` is not
among the mounted devices, so the evidence here is byte-exact text at a pinned
rev, not semantic resolution. Presence/absence claims are exact; "must appear"
judgements are editor judgement and are marked **[INFERENCE]** where they go
beyond a byte match.

Append-only line-count property used throughout: every edit below is a
same-line replacement inside an existing section, and the new round-18 section
is appended **after line 1903**. No pre-existing `SKILL.md:<line>` self-anchor
moves (`:925`, `:950`, `:1029`, `:1390`, `:1391`, `:1826`, `:1851`, `:1901-1903`
still resolve). Section *hashes* do change — see "Cold-read consequence".

---

## (a) Recorded mutation cases / ledger legs — where "seven" must become "eight"

The live case count is carried in five SKILL.md places plus the new case
record. At `183f87b` the only count-bearing sentences are:

| # | Heading (line range) | Current text (excerpt) | Minimal edit |
|---|---|---|---|
| A1 | Preamble, no heading (`:8-15`) | `:10` — `... are worked here (seven recorded since round 16), and this page carries` | `(seven recorded since round 16)` → `(eight recorded since round 18)` |
| A2 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` (`:921-1008`), intro | `:925` — `Four legs at that revision (r7-1; seven since round 16) — \`js-kimi-census\`` | `(r7-1; seven since round 16)` → `(r7-1; eight since round 18)` (keep "Four legs" — already dated text, per the round-16 errata row at `:1733`) |
| A3 | same section, `### Using the ledger` (`:933-963`) | `:949-950` — ``Cite `REGRESSION: PASS (cases=N passed=N; …)` (N=4 at r7-1, 7 since round 16)`` | `(N=4 at r7-1, 7 since round 16)` → `(N=4 at r7-1, 8 since round 18)` |
| A4 | `## Final pointers — the standing map at the arc's close (round 11, measured)` (`:1365-1462`), `### The map` (`:1380-1394`) | `:1390` — `` `corpus/knowledge/mutation-case-*.md` (six at round 11; seven since round 16) `` | `(six at round 11; seven since round 16)` → `(six at round 11; eight since round 18)` |
| A5 | same table, next row | `:1391` — `` `--regression` (six-leg registry at round 11, seven since round 16; git-materialized replay) `` | `(six-leg registry at round 11, seven since round 16; …)` → `(six-leg registry at round 11, eight since round 18; …)` |
| A6 | **new section appended at `:1904`** | none (EOF after the round-17 input-keyed registry table) | Add `## Eighth recorded case — round 18` (pattern: `## Seventh recorded case and full-page cold-read — round 16`, `:1754-1805`) plus `### Round-18 gate/probe registry`. Content per C1: leg `js-sources-check`, target kumitate `scripts/sources-check.mjs` at `0acb7752d19058b953ebbeba253b1e35f6548de5`, blob sha256 `6a293a72…37e258f`, 46-check `--selftest`, 10-defect spec + predictions committed before the sweep, `--regression` receipt `cases=8` PASS, and the case note (proposed `corpus/knowledge/mutation-case-kumitate-sources-check.md`, **[INFERENCE]** from the existing `mutation-case-kumitate-round-gate.md` naming pattern). |

All five A1–A5 strings are unique when taken with their surrounding words
(`seven since round 16` alone also appears at `:1733`, `:1738`, `:1740`, which
are **not** edited — see below). Each replacement keeps the line count.

### Dated statements that must NOT be edited (append-only convention)

- `:718` "three cases, seven rows" — matrix rows, not mutation cases.
- `:1092-1105` round-8 six-case table; `:1131` "seventh *artifact*" (boundary
  item, different sense); `:1152` "at six cases"; `:1272-1364` round-10
  six-leg receipt (`cases=6`); `:1421-1430` round-11 six-leg receipt;
  `:1456` "the six-leg registry".
- `:1509` "never a seventh independently measured gate" (round-12 scope);
  `:1555` "the six recorded cases" (round 13); `:1618`, `:1691` "seventh
  recorded case" (round 15 claims); `:1555`, `:1689` count six at their write.
- `:1733`, `:1738`, `:1740` — round-16 errata table cells ("Now" column); they
  are a snapshot of the round-16 repair and stay as written.
- `:1762` `cases=7` — the round-16 receipt; errata `:1734` already fixes the
  convention "`cases=N`, N per revision", so the round-18 section cites
  `cases=8` without rewriting `:1762`.
- `:1810-1813` round-16 registry rows; `:1852` "as the round-16 row".

### Out-of-SKILL counting surface (required for C1's depth number)

Command D (`SCORECARD.md:73`) counts lines matching
`^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` in `tools/mutate-and-run.sh`:
at `183f87b` it finds exactly seven, `:85-91`:

```
85|#   js-kimi-census        kumitate-shokunin/scripts/kimi-census.mjs   8/10 (80 %)
...
91|#   js-round-gate         kumitate-shokunin/scripts/round-gate.mjs    5/10 (50 %)
```

To move `recorded_cases` 7→8 the runner needs (all at the integration rev,
listed because the SKILL count row A5 describes this surface):
`:81` header `--regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven)`
→ `…; r18 eight`; a new `#   js-sources-check ...` line after `:91`; a
`PIN_SOURCES`/`REV_SOURCES` pair and `TABLE_SOURCES` beside `:592-612`; the
spec writer beside `:640`/`:947`/`:1009`; `REGRESSION_EXPECT` `:1236`; the
`regression_case_git` block beside `:1276-1279`; and the selftest arm at
`:1776-1805`. Additional mentions needing sweep: `:14-15`, `:98`, `:150`,
`:204`, `:588`. `SCORECARD.md:73` itself needs no edit (it derives the count);
the round row (`SCORECARD.md:184`, `:310`, `:369`, `:625` are prior dated rows)
and `corpus/knowledge/fleet-kill-rate-ledger.md` (append-only owner row) are
outside SKILL.md and not written here.

---

## (b) registry / registry-check documentation — timeout semantics

There is **no timeout documentation in SKILL.md**: `grep -c 'timeout_s'` → 0.
The only registry-check surfaces are:

| # | Heading (line range) | Current text (excerpt) | Gap |
|---|---|---|---|
| B1 | `## Live-tree re-pin and entry-command monitor — round 17` (`:1814-1854`), evidence table | `:1829` — ``A registry row stops holding its admitted outcome \| `registry-check.py` reports `differs`, exit 1`` | says nothing about a row that hangs or a malformed `timeout_s` |
| B2 | same section, recipe | `:1839-1842` — run `registry-check.py --rev <40-hex>`; "replays every row … ends with `REGISTRY_CHECK: held=N/M superseded=K`"; "Run it with `--rev`, never on the live tree" | no timeout/kill statement |
| B3 | `### Round-17 gate/probe registry — re-pin and monitor` (`:1846-1853`) | `:1851` — ``0 every active row held · 1 a row differs · 2 registry invalid, rev unresolvable or clone failed · 64 usage`` | this row describes the round-17 tool bytes; a timeout is a per-row `got=timeout` (held=false → exit 1), which is not named, and invalid `timeout_s` is not in the exit-2 cell |

Ground truth at the measured rev (`tools/registry-check.py`, read via
`git show`), confirming the two R17-TIMEOUT debts:

- `:281` `data = json.loads(raw.decode("utf-8"))` and the validator at
  `:221-227` (`isinstance(ts, bool) or not isinstance(ts,(int,float)) or ts <= 0`)
  accept `NaN`/`Infinity`: `python3 -c 'import json; v=json.loads("NaN");
  print(type(v).__name__, v<=0, isinstance(v,(int,float)))'` → `float False True`
  (so the "positive number" test passes NaN and ±Infinity).
- `:375` `start_new_session=True` plus `_kill_group` (`:306-323`, `killpg` only)
  kills the row's process group; a child that calls `setsid` leaves the group
  and survives.

Minimal edit: do **not** rewrite `:1851` (it is the dated round-17 registry
row). Append to the new round-18 registry:

```
| `tools/registry-check.py` (timeout + descendant kill) | gate |
`python3 tools/registry-check.py --rev REV [--registry PATH] [--tag TAG] [--json]` · `--selftest` |
0 every active row held · 1 a row differs (a row that hits `timeout_s` is `got=timeout`, held=false)
· 2 registry invalid — including a non-finite or boolean `timeout_s` (NaN, ±Infinity rejected at
JSON parse, exit 2 naming the row) — rev unresolvable, or clone failed · 64 usage; at `timeout_s`
every descendant is killed even if it called `setsid` (subreaper + /proc descendant walk) |
```

Plus one sentence in the round-18 prose: the round-17 registry entry at
`:1851` predates these two rules and stands as its dated record.

---

## (c) evidence-disposition G2/G3 description

**No SKILL.md text names G2/G3 or G5** (`grep -n 'G[0-9]'` → exit 1). The
nearest description is the round-17 evidence table, and it still binds HEAD:

- `:1825` — waiver-needed rule (G1) + `historical_input_forbidden`;
- `:1826` — `| A waived path's live bytes differ from \`HEAD:<path>\` | Could
  not evaluate, exit 2 \`historical_input_uncommitted\` | A worktree edit is
  tampering, not a by-design move |` (this is G2, HEAD-bound);
- `:1827` — `| The waiver rev is a tree id, dangling, not an ancestor, shallow,
  or reached through replace refs, grafts or an inherited \`GIT_DIR\` | …` (this
  is G3+G4+G7, with no ref for "ancestor");
- `:1850` registry row: `tools/evidence-disposition.py (v2 manifests)` — exits
  only, no guard names.

The authoritative description today is in the instrument, not the page:
`tools/evidence-disposition.py:40-53` ("v2 guards (round-17 hardening): G1 …
G2 … G3 …") and `:174-180` ("differ from HEAD … revs must be commits ancestral
to HEAD"); implementation `:442-455` (`merge-base --is-ancestor … HEAD`) and
`:511-540` (`tree_entry(lane, "HEAD", path)`).

Minimal edit: append to the round-18 section a row/paragraph for the
`tools/evidence-disposition.py` registry entry:

```
G2: a waived path's live bytes are compared with `refs/heads/<branch>:<path>`
(the resolved branch tip), never bare HEAD; G3: the waiver rev must be exactly a
40-hex commit id and an ancestor of `refs/heads/<branch>`. A jj-colocated
fixture (`jj git init --colocate`; HEAD != branch tip) is a selftest case and
fails the HEAD-based code. v1/v2 schemas and exits 0/1/2/64 unchanged.
```

and a one-sentence correction: `:1826-1827` describe the round-17 code (HEAD);
round 18 resolves both guards at the branch tip, matching the canonical rule at
`:1033-1035`. If the L1 instead treats the round-17 table as live contract
rather than dated record, the only minimal in-place option is a same-line
rewrite of `:1826` (`\`HEAD:<path>\`` → \`refs/heads/<branch>:<path>\`) and a
suffix on `:1827` naming the branch tip; that would misattribute round-17's
code and needs the correction note either way. **Recommendation: append, keep
`:1826` as the dated row.**

---

## (d) trace-inputs location

Two SKILL.md references, both inside the round-17 input-keyed section:

| # | Heading (line range) | Current text (excerpt) | Minimal edit |
|---|---|---|---|
| D1 | `## Input-keyed cold-read credit — round 17` (`:1855-1895`), recipe step 2 | `:1885` — ``python3 .ufo/evidence/round-17/coldread/trace-inputs.py --root $W/fleet/tameshi-shokunin --out <receipt.json> -- <argv…>`` | repoint to `python3 tools/trace-inputs.py …` (contract B promotion). Same line count. |
| D2 | `### Round-17 gate/probe registry — input-keyed credit` (`:1897-1903`) | `:1902` — row for `.ufo/evidence/round-17/coldread/trace-inputs.py`, exits `0 traced · 2 strace unavailable/never executed · 64 usage; --selftest 0 pass, 1 a case failed — never wrap it (nested ptrace)` | keep as the dated round-17 row; append a round-18 row `tools/trace-inputs.py` with the same CLI and receipt schema `tameshi-trace-inputs-v1`, exits unchanged, and add the three new selftest guard classes: it fails when the **O_RDWR exclusion**, the **`PYTHONCACHEPREFIX`/`PYTHONDONTWRITEBYTECODE` setting**, or **execve recording** is removed. |

Verified state: `tools/trace-inputs.py` is absent at the measured rev
(`cat-file -e` exit 128), while the round-17 copy is tracked
(`cat-file -e` exit 0), so D1's current text cannot run from a clean clone of
`183f87b` once contract B lands (the promoted path is the only forward path;
the old path must stay byte-identical per contract B).

Adjacent paths in the same recipe block that move with contract F (round-18
kit): `:1888` `.ufo/evidence/round-17/coldread/assemble.py` and `:1890`
`.ufo/evidence/round-17/measure.py`, plus their registry rows `:1901` and
`:1903`. Minimal coherent treatment: repoint the recipe block `:1885-1891` at
`tools/trace-inputs.py` + `.ufo/evidence/round-18/coldread/assemble.py` +
`.ufo/evidence/round-18/measure.py`, and keep all four round-17 rows
`:1901-1903` as dated. The round-18 section then carries its own recipe
(default ledger `.ufo/evidence/round-18/coldread/ledger.json`; box-3 link
string that same path; ignored inputs `SKILL.md` + both ledgers; `--carry` for
the round-17 ledger; `--explain`; report schema `tameshi-coldread-report-v2`
with receipts from `tools/trace-inputs.py`).

---

## (e) jj rule `:1027-1035` and the `:1029` detect_branch cite

Heading/section: `## The re-sweep cadence and the six-case confidence statement
(round 8, measured)` (`:1010-1154`), subheading `### The tick and the pin read`
(`:1021-1067`). The rule block is `:1027-1036`; the citation sits at `:1029`:

```
1027|- **Per case, two readings:** the target's relation to each repo's branch-tip bytes
1028|  (`current` / `stale` / `drift`; `<branch>` per `detect_branch`,
1029|  `../scripts/hyaku/jj-lane.sh:53-65`) and the tool's relation to the last run (`held` / `moved`):
```

The cited range is stale at every fleet revision after `67a3123` (v1):

```
$ git -C /home/vgpnk/Projects/shokunin show 67a3123:scripts/hyaku/jj-lane.sh | sed -n '53,65p'
  -> detect_branch() { ... }   # exactly 13 lines, v1
$ git -C /home/vgpnk/Projects/shokunin show 5d8a3b5:scripts/hyaku/jj-lane.sh | grep -n 'detect_branch()'  -> 115
$ git -C ... show 14df5b9:scripts/hyaku/jj-lane.sh | grep -n 'detect_branch()'                           -> 115
$ git -C ... show HEAD:scripts/hyaku/jj-lane.sh | grep -n 'detect_branch()'                             -> 115
  fleet HEAD = ae12f330697d09bcf7fa7df7552e1c48a6443950
$ git -C ... show HEAD:scripts/hyaku/jj-lane.sh | sed -n '53,65p'
  -> usage() body lines "jj-lane.sh init …" through "err() { ... }" (not detect_branch)
```

Minimal edit at `:1029` (line count unchanged):

```
-  `../scripts/hyaku/jj-lane.sh:53-65`) and the tool's relation to the last run (`held` / `moved`):
+  `../scripts/hyaku/jj-lane.sh:115` at fleet `14df5b9`) and the tool's relation to the last run (`held` / `moved`):
```

Pinning the fleet rev is the round-17 cold-read finding F4 (`CR27.md:49`: the
unversioned external cite drifted mid-read). `:115` is stable across v2
`14df5b9`, `5d8a3b5`, and current `ae12f33`; citing the current fleet HEAD
instead is also defensible but re-drifts. Semantic caveat: at v2 the helper's
own comment (`:112-114`) marks `detect_branch` "used ONLY by init", and `state`
prefers `lane_branch_jj`/`lane_branch_git` (`:387-391`). For SKILL's purpose
(resolve a repo's branch tip for an external reader) the attached-HEAD-else-
origin/HEAD resolver at `:115-125` is still the right anchor — **[INFERENCE]**;
if the round wants the helper's newest runtime resolver, cite
`lane_branch_git` too.

Companion cites outside SKILL.md (same stale `53-65`, routed by
`corpus/lessons/round-17-verifier-spotcheck.md` §7 item 7, not edited by this
map): `corpus/knowledge/fleet-kill-rate-ledger.md:420`,
`corpus/knowledge/incremental-pin-disposition.md:386`,
`corpus/knowledge/operator-runbook.md:514`,
`corpus/knowledge/service-limits.md:279`,
`corpus/knowledge/verification-patterns-fleet.md:309`. Each says
`(detect_branch, ../scripts/hyaku/jj-lane.sh:53-65)` and needs the same
`:115` correction or a rev-pinned cite.

---

## Cross-cutting consequences for the L1

1. **Anchor stability.** Every A/B/C/D/E edit above is a same-line replacement;
   the new round-18 section is appended after `:1903`. No existing
   `SKILL.md:<line>` self-anchor changes. New `cases=8` receipts are stated in
   the new section, never by rewriting `:1762`'s `cases=7`.
2. **Cold-read consequence [INFERENCE].** Editing lines `:10`, `:925`, `:950`,
   `:1390-1391`, `:1029` changes the section hashes for the preamble,
   `## The leg ledger …`, `### Using the ledger`, `### The map`, and
   `### The tick and the pin read`; repointing `:1885` changes
   `## Input-keyed cold-read credit — round 17`. Under the round-18 no-harm
   monitor those buckets lose their old credit and must be re-read/re-recorded
   in the round-18 ledger (input-keyed rule, contract F); the old round-17
   ledger still credits the old bytes at its own rev.
3. **Registry placement.** One new `### Round-18 gate/probe registry` can carry
   all new/updated rows: `tools/registry-check.py` (timeout/descendants),
   `tools/evidence-disposition.py` (branch-tip G2/G3), `tools/trace-inputs.py`
   (promoted), `.ufo/evidence/round-18/measure.py`,
   `.ufo/evidence/round-18/coldread/assemble.py`,
   `.ufo/evidence/round-18/defect-probes.py`, and the
   `.ufo/evidence/round-18/dispositions.json` manifest. Keep `:1850-1853` and
   `:1901-1903` as dated rows.

## Remaining unknowns

- Whether the L1 wants the round-17 evidence table `:1826-1827` rewritten in
  place (HEAD → branch tip) or corrected by an appended round-18 note; the
  lane's own precedent (round 17 "Correction of round 16", `:1863-1869`) favours
  append.
- The eighth case's knowledge-note filename is not fixed by C1; the proposed
  `mutation-case-kumitate-sources-check.md` is inferred from the existing
  naming pattern.
- Which fleet rev to pin in `:1029` (`14df5b9` recommended; `ae12f33` current;
  both place `detect_branch` at `:115`).
- The measured kill rate of the eighth case is not asserted here; the new
  section must quote the sweep receipt, not a predicted number.

Verdict: built — the five requested SKILL.md surfaces are mapped to exact
lines with same-line minimal edits, the new-section insertion point is `:1904`,
and the out-of-SKILL counting dependency for the eighth case is named.
