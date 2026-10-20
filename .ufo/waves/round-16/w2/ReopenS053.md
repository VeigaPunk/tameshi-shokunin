# Reopen S053 — kumitate `scripts/round-gate.mjs` (round 16, wave 2)

**Question.** Re-open S053 at its pinned artifact and adjudicate its
`corpus/SOURCES.md` row (`corpus/SOURCES.md:62`) and its round-16 Gate quote
(`corpus/lessons/round-16.md:34`) read at lane commit
`c699c8c36d6e4eca4b796b81a8247904aa145ec8`: quote exact and ≤25 words at the
stated location; anchor resolvable; tier/kind/scope/teaches justified; used-by
paths exist and actually cite S053.

**Verdict: holds — every named field verifies; no field falls.** Three
non-blocking notes are recorded under §Observations (O1 source-side
hermeticity caveat, O2 anchor boundary, O3 quoting-form convention), none of
which changes the row.

Lane HEAD is the target commit (`git -C .../tameshi-shokunin rev-parse HEAD` →
`c699c8c36d6e4eca4b796b81a8247904aa145ec8`); the three files read here are
byte-identical at HEAD and at `c699c8c` (sha256 comparisons below).

## 1. Pinned artifact opens and is the bytes claimed

```
$ git -C kumitate-shokunin cat-file -e 364f1d5^{commit}; echo $?
0
$ git -C kumitate-shokunin log -1 --format='%H %ci %s' 364f1d5
364f1d5954158ef8844bca4a5fef57b05d2f2ca5 2026-10-13 22:49:20 -0300 round-24: triage — ... round-gate (60/60) ...
$ git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs | sha256sum
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  -
$ git -C kumitate-shokunin rev-parse 364f1d5:scripts/round-gate.mjs
1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3
$ git -C kumitate-shokunin rev-parse HEAD:scripts/round-gate.mjs
1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3     # HEAD 1770305f…, same blob
$ git -C kumitate-shokunin log -1 --format=%H -- scripts/round-gate.mjs
364f1d5954158ef8844bca4a5fef57b05d2f2ca5     # last-touching commit
$ git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs | wc -c -l
   1511   80415
```

The row's abbreviated hash `f890e277…d3e9` is the prefix/suffix of the measured
full sha256. The case doc's pin prose (80,415 B, 1,511 lines, last-touch
`364f1d5`, HEAD same blob) re-checks exactly
(`corpus/knowledge/mutation-case-kumitate-round-gate.md:17-20`). The pinned
bytes were copied to the scratch dir and hashed again:
`f890e277…d3e9`.

## 2. Per-field adjudication

Row text (`corpus/SOURCES.md:62`):

```text
| S053 | kumitate `scripts/round-gate.mjs` (fleet gate, read-only) — kumitate-shokunin/scripts/round-gate.mjs | code | A | the gate's own selftest/verdict behaviour at the measured revision | :2-21, :45-48, :635, :677-681 @ 364f1d5 (blob sha256 f890e277…d3e9) | a green verdict from this lane-local pre-check asserts nothing fleet-wide; its 60-case hermetic selftest is the suite a mutation case measures | mined | 2026-10-20 | 180d | corpus/knowledge/mutation-case-kumitate-round-gate.md |
```

Gate quote (`corpus/lessons/round-16.md:34`):

```text
| S053 | kumitate-shokunin `git show 364f1d5:scripts/round-gate.mjs` | 2026-10-20 | "a green verdict asserts nothing fleet-wide, and running the gate does not change mission completion" (header comment, :19-20) |
```

| field | claim | observed | verdict |
|---|---|---|---|
| quote exact | text quoted from `:19-20` | 15 words; after stripping the ` * ` comment gutter the quote is a contiguous exact substring of lines 19-20 (no ellipsis, no stitched words); line 19 begins `a green verdict asserts…`, line 20 supplies `change mission completion` | **holds** |
| quote ≤25 words | rule 1 limit | 15 words | **holds** |
| stated location | `header comment, :19-20` | lines 19-20 are inside the `/** … */` header (:2-21) at rev `364f1d5`; verbatim print below | **holds** |
| anchor | `:2-21, :45-48, :635, :677-681 @ 364f1d5` | commit resolves; all ranges in 1..1511; contents are exactly the boundary paragraph (:2-21), the hermetic-selftest clause (:45-48), the selftest dispatch `if (opts.selftest) return selfTest();` (:635), and the text verdict + `return exitCode` (:677-681); blob sha256 matches | **holds** |
| tier A | primary/authoritative for `scope` | contract: "A: primary or authoritative for that scope (spec, official docs, **source code**, original paper, maintainer statement, the lane's own re-runnable gate output)" — the artifact is the source code whose own behaviour is the scope | **holds** |
| kind `code` | allowed enum | `code` is in the contract enum; target is a Node ESM script | **holds** |
| scope | "the gate's own selftest/verdict behaviour at the measured revision" | bounded to the artifact's own behaviour, not fleet authority; revision pinned in anchor; behaviour re-observed at those bytes (§3) | **holds** |
| teaches | lane-local boundary + 60-case hermetic suite used as a mutation-case oracle | header says "lane-local pre-check of the fleet round-close contract" (:3) and "a green verdict asserts nothing fleet-wide" (:19), "NOT a fleet report-conformance authority" (:13); selftest prints `60/60 pass`; case doc line 21 names the same suite (`node round-gate.mjs --selftest`, 60 checks) and line 1 cites S053 | **holds** |
| used-by exists | `corpus/knowledge/mutation-case-kumitate-round-gate.md` | exists at `c699c8c` (`git cat-file -e` rc 0) and in the worktree; the contract's mined-row census prints no `missing:` line | **holds** |
| used-by cites S053 | path actually cites row | knowledge doc line 1: `source: S053 kumitate scripts/round-gate.mjs @ 364f1d5… (blob sha256 f890e277…d3e9), read-only; …` | **holds** |
| status `mined` | ≥1 citing used-by path | the used-by path exists and cites S053 | **holds** |
| opened / recheck | `2026-10-20` / `180d` | matches the Gate access date; `180d` is an allowed cadence (ISO date or 90d/180d/on-release); row is byte-pinned so it cannot drift silently | **holds** |

Verbatim source lines quoted by the Gate (`git show 364f1d5:scripts/round-gate.mjs | sed -n '19,20p'`):

```
 *   a green verdict asserts nothing fleet-wide, and running the gate does not
 *   change mission completion (mission state is projected read-only from
```

Programmatic quote check (lesson line extracted from the committed blob, source
from the pinned blob; comment gutter stripped, whitespace normalised):

```
cells 4
cells[3] = '"a green verdict asserts nothing fleet-wide, and running the gate does not change mission completion" (header comment, :19-20)'
quote = 'a green verdict asserts nothing fleet-wide, and running the gate does not change mission completion'
words = 15
loc   = 'header comment, :19-20'
quote_exact_in_19_20 = True
quote_in_full_doc    = True
has_ellipsis         = False
```

## 3. Execution evidence for `teaches` (60-case hermetic selftest)

Scratch: `/tmp/tameshi-r16w2-ReopenS053-LvYNOw`. The selftest and strace runs
were made against `/tmp/r16w2-s053.mjs`; that file was moved into the scratch
dir afterwards as `$W/r16w2-s053.mjs` (byte-identical, sha256
`f890e277…d3e9`). All runs used the committed bytes.

```
$ node $W/r16w2-s053.mjs --selftest
kumitate round-gate --selftest (hermetic, node v24.21.0)
...
PASS  [60/60]  every declared finding kind fires in at least one fixture — 14 kinds observed
ROUND_GATE_SELFTEST: 60/60 pass
VERDICT: PASS
exit=0
```

- Case count in source: `grep -c "  check("` → **60**; first case at
  `:878`, matching the emitted `[ 1/60]`.
- Zero network: `unshare -n -r node $W/r16w2-s053.mjs --selftest` → `60/60
  pass`, `VERDICT: PASS`, exit 0. Independent of the case doc's RGRecon claim.
- Live-tree reads: `strace -f -e trace=%file -o $W/trace node $W/… --selftest`
  → exit 0, 60/60. Under `/home/vgpnk/Projects`: **0** `openat`/content reads;
  only the existence probes `newfstatat("/home/vgpnk/Projects/shokunin")` and
  `access("/home/vgpnk/Projects/ufo-fsd-alpha")` (fixture shell `$PWD` handling
  and the derived default-origin candidates). `socket(`/`connect(` count: **0**.
  This matches the case doc's precise wording "under strace, zero reads under
  `~/Projects`, no network" (`…-gate.md:21-22`).
- Pollution claim boundary: `env -i HOME=$W/home TMPDIR=$W/tmpd
  PATH=… GIT_DIR=/nonexistent … $NODE $W/… --selftest` → exit 1,
  `Error: fixture lane init failed: exit 1 /nonexistent: Permission denied`
  (`:722`, via `fxLaneRepo`). An exported `GIT_DIR` does reach the fixture git
  calls because `GIT_ENV = {...process.env, …}` does not clear it (`:704-712`).
  This is exactly the RGSentinel hazard the case doc records
  (`…-gate.md:22-25`) and the reason the sweep runs the suite under `env -i`
  with a private `HOME`/`TMPDIR`. It does not falsify the row's "hermetic"
  word — temp-dirs-only, zero network, zero content reads all hold — but it
  qualifies the source header's stronger "a polluted env cannot affect it"
  (`:46-48`). See Observation O1.

## 4. Registry integrity around the row

- `corpus/SOURCES.md` diff `e69b488..c699c8c`: **+17 / −1**; the only removed
  line is `- Next unused id: S052.` (replaced by `S058`). Rows S052–S057 are
  pure additions; no existing row's `status`, `recheck` or `used-by` changed,
  matching `corpus/lessons/round-16.md:40-43`.
- Contract census on the committed blob: 55 rows; malformed rows `0`;
  duplicate ids none; enum/tier-inflation violations none; S053 `NF=13`.
- Mined-row used-by existence sweep: no missing path (worktree and `c699c8c`).
- Convention check: S032–S037 are the existing sibling-lane gates and use the
  identical `(fleet gate, read-only)` label, a local repo path in `source`, and
  the scope stem "the gate's own behavior at the measured revision"
  (`corpus/SOURCES.md:43-48`); round-1 Gate quotes for S032/S037 use
  `<repo>/<path> @ <rev> (<blob>)` + quote + blob-line location
  (`corpus/lessons/round-1.md:433,438`). S053's label, locator form and scope
  are the established pattern, not a deviation.

## Observations (non-blocking, none changes a field)

- **O1 — hermeticity is condition-bounded.** The header's `:46-48` "a polluted
  env cannot affect it" is false for an exported `GIT_DIR` (observed: fixture
  `git init` fails; with a writable value the fixture commits would land in
  that repo, as the case doc records). The row's one-word "hermetic" is true in
  the measured senses (temp dirs only, zero network, zero content reads) and
  the caveat is carried by the used-by doc; a future re-user should not read it
  as blanket env-immunity. No row edit is implied: the row's `teaches` does not
  claim env-immunity.
- **O2 — anchor boundary.** `scope` says "selftest/verdict behaviour"; the
  anchor sample `:677-681` covers the audit-mode verdict print/exit, while the
  tracked-mode verdict shape appears at `:42-44`, inside the cited `:2-21`
  header range. The anchor is therefore sufficient for the scope as written.
- **O3 — Gate quoting form.** The lesson's locator is a `git show` command
  rather than a URL; this matches the lane's sibling-gate precedent (S032/S037
  Gate rows) and the artifact is also carried by
  `https://github.com/VeigaPunk/kumitate-shokunin` (origin; `364f1d5` is
  contained in `origin/master`). No action.

No tools were installed or upgraded during this seat. No lane files other than
this report were written; the kumitate tree was read only
(`git --no-optional-locks status --porcelain` → 0 entries before and after).

**One-line verdict: holds — S053's row and Gate quote survive re-open at `364f1d5`/`c699c8c` on quote, location, anchor, tier, kind, scope, teaches, used-by, status and cadence; the only caveats are the source's own over-broad env claim (already recorded in the used-by doc) and the tracked-verdict line not being in the anchor sample.**
