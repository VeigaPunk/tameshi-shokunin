# CR12b — cold-read report: SKILL.md lines 594–667

Seat: `TameshiR16.CR12b` · Range: snapshot lines 594–667 (one heading:
`## Appendix B — worked example: bash case (reproduce from this page al)` —
the snapshot heading is exactly `## Appendix B — worked example: bash case
(reproduce from this page alone)` at line 594).
Scratch: `/tmp/tameshi-r16-CR12b-hhAlGu` (snapshot copy) and work dir
`/tmp/tameshi-r16-cr12b-work` (mutants, evidence, probe fixtures).

## Snapshot pin

```
$ cp .ufo/evidence/round-16/coldread/SKILL.snapshot.md /tmp/tameshi-r16-CR12b-hhAlGu/
$ sha256sum SKILL.snapshot.md
97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580  (MATCHES declared pin)
```

## Section inventory

The range contains exactly one section heading, at line 594; the section body
runs 594–666 (line 667 blank). Everything in the body was executed or
re-checked from the page alone plus files the page names.

## Execution log — what a cold reader did

### 1. Artifact pin (lines 601–606)

```
$ sha256sum kagi-shokunin/corpus/surface-census.sh
275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f   MATCH
$ stat -c '%s %a' …   →  44212 bytes, mode 755   MATCH
$ wc -l               →  886 newlines           MATCH (line 887 has no trailing \n; last byte 0x63)
$ git -C kagi-shokunin status --porcelain -- corpus/surface-census.sh → empty  MATCH
```

**Deviation observed (minor):** `git rev-parse HEAD` in kagi-shokunin prints
`c2cab35bc92e57e39e5489bac3386db078345b3f`, not the pinned `fecee87`.
The pinned commit exists (`git cat-file -t` → `commit`) and
`git rev-parse fecee87…:corpus/surface-census.sh` ==
`HEAD:corpus/surface-census.sh` == `dcf878b95e172253a282adf2dc2cc9e8dd8c0d7c`
(blob identical at both revs), so the sha-pinned artifact is intact; the
reader's page-written appendix text ("re-derive… if sha differs") covers this:
the sha matched, so proceed. Recommendation: the pin text could note that
"rev fecee87" is a historical anchor, not a HEAD claim, to spare readers a
verification detour.

### 2. Control selftest (line 615)

```
$ bash "$W/pristine.sh" --selftest
ok-case  01 clean               exit=0 SURFACE OK
… (ok-case 01..14, exactly the tokens the page implies) …
ok-case  14 fused-shape-row     exit=2 fused-row refused
skip-case 15 verbs-sandboxed    substrate-absent (handler not on PATH)
skip-case 16 verbs-break-injection substrate-absent (handler not on PATH)
SELFTEST: PASS (16 cases)   rc=0   — MATCHES page ("control: SELFTEST: PASS (16 cases), rc=0")
```

### 3. Driver + manifest (lines 626–650)

Wrote `/tmp/tameshi-r16-cr12b-work/mutate_driver.py` from the Appendix A
contract (named by the page: "same as Appendix A except…") with SPECS copied
verbatim from lines 638–649, including multi-line `old`/`new` literals.
`--check` printed per-defect `occurrences=1` ×10 and `CHECK: all unique`, rc=0.

**Ambiguity (minor, resolved by inference):** the manifest comment says "`\n`
are real newlines, `\"` real quotes, `\\n` a literal backslash-n inside a
printf format" — I read the SPECS block as Python source and pasted it
directly; the uniqueness check confirmed every literal byte-exact, so the
reading is self-verifying.

### 4. Sweep (line 620)

```
$ python3 mutate_driver.py --run   →  killed 8/10, mismatches 0   rc=0, 13.4 s wall
```

Per-mutant verdicts and `bad-case` IDs (from `evidence/<id>.meta.json`):

| mutant | exit | verdict  | failing cases (observed) | page expects |
|--------|------|----------|--------------------------|--------------|
| B00-control | 0 | pass | — | PASS 16 |
| B1 | 1 | killed | 05 | 05 undeclared-file ✓ |
| B2 | 1 | killed | 01 04 | 01, 04 ✓ |
| B3 | 1 | killed | 01 04 06 | 01, 04, 06 ✓ |
| B4 | 1 | killed | 07 | 07 symlink-swap ✓ |
| B5 | 0 | **survived** | — | survivor ✓ |
| B6 | 1 | killed | 01 04 | 01, 04 ✓ |
| B7 | 1 | killed | 10 | 10 sqlite-unavailable ✓ |
| B8 | 1 | killed | 13 14 | 13, 14 ✓ |
| B9 | 1 | killed | 03 04 | 03, 04 ✓ |
| B10 | 0 | **survived** | — | survivor ✓ |

Aggregate: **8/10 killed (80 %)**, survivors B5/B10 — exact match to lines
652–660. Wall time 13.4 s vs the page's "11.0 s sweep" — host-dependent, not
a stated invariant; noted for completeness.

### 5. Survivor non-equivalence probes (lines 621–623)

The page gives the probe commands but no fixture contents; the note it names
(`mutation-case-kagi-census.md` §7, page :622 "note §7 commands") likewise
lists fixture paths without contents. A cold reader must construct `probe/`
and `probe2/` from the substrate's usage + selftest fixture builders. I built
minimal one-row fixtures (census row `$HOME/.local/bin/the-janitor asset exec
- CLI`, empty shapes.tsv/baseline.tsv; host file mode 644 for probe, 755 for
probe2 — mode `-` avoids tripping the mode-drift arm, which the page's "(exec
644)" output implies):

```
pristine on probe : SURFACE DIVERGED …(declared exec, no execute bit)  rc=1
mutant-B5         : SURFACE OK       …(exec 644)                       rc=0
pristine on probe2: CLEAN (… ok=1 absent=0 skipped=0)                  rc=0
mutant-B10        : CLEAN (… ok=0 absent=0 skipped=0)                  rc=0
```

All four observations match lines 661–663 exactly.

### 6. Restore pins (lines 664–666)

```
sha256sum "$W/pristine.sh" → 275d8294…53009f (unchanged)
cmp pristine.sh kagi original → identical
git status --porcelain for the path → empty (kagi repo clean)
44212 B / mode 755 preserved on the copy
```

### 7. Note anchors re-checked (record facets embedded in the section)

`mutation-case-kagi-census.md` anchors cited by the page, re-read:
`:62-80` kill-rate table — every row matches my observed run (verdicts +
failing-case names identical); `:50-53` 11.0 s / 80 % claim present;
`:111-122` B5/B10 non-equivalence outputs — matched verbatim by my probes;
`:34-35`/`54-56` restore-proof claims — consistent with my after-state.
Manifest line claims verified on the pinned blob: `:85` die, `:191` runtime
branch, `:229` != test, `:241` -eq guard, `:371` head -c, `:405-406`
N_UNVERIFIED, `:435` -ge floor, `:862` summary arg, `:200-204` symlink arm,
`:214-217` exec x-bit arm — all exact.

## Verdict

**executed-ok** (with one minor gap). The page is reproducible from itself
plus the named note and substrate: control, check, run, probes, and restore
pins all confirmed; kill rate, survivor set, and per-mutant failing-case IDs
matched bit-for-bit in naming. Two minor frictions, neither blocking:
(a) the `kagi rev fecee87` pin is stale as a HEAD claim (blob identical at
HEAD, sha anchor held — the page's own drift text covers it);
(b) probe fixture contents are not on the page or in §7 — derivable from the
substrate + the page's expected probe output, but a reader who cannot infer
`asset exec -` + chmod 644 would stall; a one-line fixture sketch would
remove the only inference step in the whole section.

## Bounded recommendations

1. Pin text: say "rev `fecee87` (blob at pin time)" or add "(blob unchanged
   at HEAD: dcf878b…)" so the rev reads as an anchor, not a HEAD assertion.
2. Add one line under the probe commands: `probe/: exec-declared file chmod
   644, census row 'asset exec -'; probe2/: same file chmod 755` — §7 already
   lists fixture paths; contents are the missing byte.

```json
{"seat":"CR12b","skill_sha256":"97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580","sections":[{"start":594,"heading":"## Appendix B — worked example: bash case (reproduce from this page alone)","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["pinned rev fecee87 is stale as a HEAD claim (kagi HEAD=c2cab35; file blob identical at both revs, sha256 anchor held — covered by the page's own drift paragraph, minor detour only)","probe fixture contents (probe/, probe2/ census+shapes+baseline+host tree) are not given on the page or in the named note §7; derivable from substrate usage + expected probe output — inferred 'asset exec -' row, chmod 644/755"],"commands_executed":["cp .ufo/evidence/round-16/coldread/SKILL.snapshot.md /tmp/tameshi-r16-CR12b-hhAlGu/ && sha256sum (matched 97cf436b…)","git -C kagi-shokunin rev-parse HEAD → c2cab35 (≠ pinned fecee87; blob identical: git rev-parse fecee87:corpus/surface-census.sh == HEAD:corpus/surface-census.sh == dcf878b95e…)","git -C kagi-shokunin status --porcelain -- corpus/surface-census.sh → empty","cp -p corpus/surface-census.sh $W/pristine.sh; sha256sum → 275d8294…53009f","bash pristine.sh --selftest → SELFTEST: PASS (16 cases) rc=0 (14 ok + 2 substrate-absent skips)","python3 mutate_driver.py --check → occurrences=1 ×10, 'CHECK: all unique', rc=0","python3 mutate_driver.py --run → killed 8/10, mismatches 0; survivors B5,B10; per-mutant bad-case IDs all match page (B1:05 B2:01,04 B3:01,04,06 B4:07 B6:01,04 B7:10 B8:13,14 B9:03,04)","built probe/, probe2/ fixtures; pristine verify → 'SURFACE DIVERGED … no execute bit' rc=1; mutant-B5 → 'SURFACE OK … (exec 644)' rc=0; pristine probe2 → 'ok=1' rc=0; mutant-B10 → 'ok=0' rc=0","sha256sum/cmp restore pins: pristine.sh still 275d8294…53009f, cmp-identical to kagi file, kagi porcelain clean"],"opened":["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/SKILL.snapshot.md (copy → /tmp/tameshi-r16-CR12b-hhAlGu/SKILL.snapshot.md; lines 497-672 read: assigned 594-667 plus Appendix A 520-593 which line 626 names as the driver contract)","/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh (via cp -p → /tmp/…/pristine.sh; read ranges 76-101,142-243,314-330,689-773,850-887 + usage text; also git rev-parse blob compare — repo read-only)","/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-kagi-census.md (named by page; read :208-260 §7 reproduce commands, :24-60 restore/method, :62-80 kill table, :104-123 survivor analysis)"],"scratch":"/tmp/tameshi-r16-CR12b-hhAlGu (snapshot copy), /tmp/tameshi-r16-cr12b-work (pristine.sh, mutate_driver.py, mutant-B{1..10}.sh, evidence/, probe/, probe2/)"}]}
```
