# T52W3ExecNoHarm — no-harm + C2 probe at CAND1 (round 52, wave 3)

Seat: `T52W3ExecNoHarm` (executor). Item: run the round-52 no-harm script, the frozen C2 counter and the
SOURCES census at content candidate CAND1 `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`, copy the outputs into
`.ufo/waves/round-52/w3/`, report every monitor and any RED with cause. Read-only on the lane; the only lane
writes in this seat were the pre-existing wave-3 bookkeeping (none by me). Scratch root
`/fast/scratch/hyaku/tameshi-r52/T52W3ExecNoHarm` (removed before yield); one `--shared` clone, checked with
`git -C … rev-parse --show-toplevel` before any fixture commit.

Tooling: nothing installed, nothing upgraded (no pacman/uv/npx/official-binary call). All runs used host
`python3`/`bash`/`curl` already present.

## Environment facts recorded before running

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
f1a3246105f75bb9f678f20e25878c44db3a2caf
$ git -C … merge-base --is-ancestor 7ff81a5b0ab0… HEAD && echo ANCESTOR
ANCESTOR
$ git -C … diff --name-status --no-renames 7ff81a5b0ab0… HEAD
A .ufo/evidence/round-52/coldread/refresh.py
A .ufo/evidence/round-52/integrate/precheck-cand1.stdout
A .ufo/waves/round-52/build-spec-w3.py
A .ufo/waves/round-52/spec-w3.json
A .ufo/waves/round-52/w3-dispatch.err
A .ufo/waves/round-52/w3-dispatch.json
$ git -C … rev-parse 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135
7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135
```

CAND1 is **not** the branch tip (the assignment text says tip; HEAD is `f1a3246`), but `cand1..HEAD` adds only
`.ufo` evidence/spec files — no content file (`SKILL.md`, `tools/*`, `corpus/*`) differs. C2 was therefore also
run at HEAD to show the probe carries to the tip (same result, below). No-harm was deliberately run at the named
rev `7ff81a5b…`. Content delta `BASE..CAND1` (excluding `.ufo`):

```
$ git -C … diff --stat --no-renames ef19d8e1e7ba… 7ff81a5b0ab0… -- . ':(exclude).ufo'
 SCORECARD.md | 11 +++ / SKILL.md | 122 +++--- / corpus/QUALITY.md | 12 +++ / corpus/SOURCES.md | 3 +
 corpus/knowledge/fleet-kill-rate-ledger.md | 4 +++ / corpus/lessons/round-52.md | 54 ++++
 tools/registry.json | 4 +- / tools/round21-measure.py | 11 +-
$ git -C … show 7ff81a5b0ab0…:SKILL.md | wc -l
2171
```

## 1. No-harm at CAND1 — 10 ok, 1 RED (coldread-floor), as pre-registered

```
$ S=/fast/scratch/hyaku/tameshi-r52/T52W3ExecNoHarm
$ HYAKU_SCRATCH=$S bash .ufo/evidence/round-52/no-harm.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=6 credited=45 RED
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-133 134 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [M:tools/registry.json M:tools/round21-measure.py ] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none
        classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,
        held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
```

Receipt: `.ufo/waves/round-52/w3/T52W3ExecNoHarm-noharm.out` (stderr empty, 21 s).

Same script at BASE for the delta (shows the 10 green monitors are discriminating, not stuck green):

```
$ HYAKU_SCRATCH=$S/base bash .ufo/evidence/round-52/no-harm.sh … ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-133 133 ok
NOHARM r46-coverage … ok   NOHARM r47-coverage … ok
NOHARM tools-scope [] ok
NOHARM r49-generator-capability [PBT_STAGED_ID …] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
```

Receipt: `T52W3ExecNoHarm-noharm-base.out`. Delta BASE→CAND1 is exactly the one pre-registered monitor:
`coldread-floor 64/8 → 45/6`; `registry-rows` 133 → 134 (S274); `tools-scope` `[]` → the two declared files.

## 2. The RED, with cause

`coldread-floor` (`.ufo/evidence/round-52/no-harm.sh:19`) demands `score>=8 and credited>=64`; CAND1 gives
`score=6 credited=45`, i.e. 19 of 64 base-credited sections lost. Explained per section:

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev 7ff81a5b0ab0… --explain
sections_total=64 sections_covered=45 score=6
reasons: no-ledger-entry=16
         input-drift:corpus/knowledge/fleet-kill-rate-ledger.md=1
         input-drift:corpus/knowledge/fleet-kill-rate-ledger.md;…;tools/mutate-and-run.sh;tools/trace-inputs.py=1
         input-drift:corpus/knowledge/closeout-r11.md;…;tools/registry.json;tools/trace-inputs.py;…=1
```

Receipt: `T52W3ExecNoHarm-coldread-cand1.out`; the same 19 headings are listed in
`.ufo/evidence/round-52/integrate/precheck-cand1.stdout` (`COLDREAD_PRECHECK … floor_credited=64
cand_credited=45 lost=19 RED`). So the loss is two mechanisms, both caused by this round's own content edits:

- **16 × `no-ledger-entry`** — `SKILL.md` section bytes changed (122-line diff; 59 in-line fixes), so no ledger
  entry pins the new section digest; the round-18 matcher keys sections by exact `sha256`
  (`.ufo/evidence/round-18/measure.py:607-618`).
- **3 × `input-drift`** — the section body still matches, but a cited input blob changed digest:
  `corpus/knowledge/fleet-kill-rate-ledger.md` (4-line append) in all three, plus `tools/mutate-and-run.sh`,
  `tools/registry.json`, `tools/trace-inputs.py`, `corpus/knowledge/{closeout-r11,operator-runbook,
  incremental-pin-disposition}.md`. The input gate rejects a trace whose recorded digest ≠ live blob.

This is the pre-registered expected RED ("expected RED until the re-key lands (19 sections)"); the wave-3
re-reads plus `.ufo/evidence/round-52/coldread/refresh.py` are the designed remedy. Nothing in the 10 green
monitors regressed.

## 3. C2 counter at CAND1 — `total=0 C2_R52_PASS=true`

```
$ TMPDIR=$S/w python3 .ufo/evidence/round-52/c2/measure.py --lane LANE --rev 7ff81a5b0ab0… --explain
C2_CHECK m1 ok legs=10 phrases=['ten'] bad=[] mte_check_mentions=[('10', '10')]
C2_CHECK m2 ok row=True tmp=True tmpdir=True
C2_CHECK m3a ok lines=1 pointer=tools/mutate-and-run.sh:434
C2_CHECK m3b ok lines=1 pointer=tools/mutate-and-run.sh:579-583
C2_CHECK m3c ok bullet=1 tmp=False tmpdir=True
C2_CHECK m4 ok r51_entries=20 corrections=20 bad=[]
C2_CHECK m5 ok row=1 note=True
C2_CHECK m6 ok t52_entries=0 bad=[]
C2_R52: rev=7ff81a5b0ab0… m1=0 m2=0 m3=0 m4=0 m5=0 m6=0 total=0 C2_R52_PASS=true
```

Receipt: `T52W3ExecNoHarm-c2.out`. Counter integrity and discrimination:

- `.ufo/evidence/round-52/c2/measure.py --selftest` → `C2_SELFTEST: cases=8 failed=0`
  (`T52W3ExecNoHarm-c2-selftest.out`).
- At BASE the same counter prints `m1=2 m2=1 m3=3 m4=20 m5=1 m6=0 total=27 C2_R52_PASS=false` — exactly the
  contract's `before` (`T52W3ExecNoHarm-c2-base.out`, rc=1).
- At lane HEAD `f1a3246` it prints `total=0 C2_R52_PASS=true` (`T52W3ExecNoHarm-c2-head.out`).

**Caveat the counter cannot express: m6 is vacuous at CAND1.** `m6 ok t52_entries=0` means "no round-52 re-key
entry exists yet", not "re-key entries are sound". `.ufo/evidence/round-52/c2/measure.py:167` selects entries
whose `seats` start with `T52`; with zero such entries the loop body never runs. The C2 pass at CAND1 therefore
rests on m1–m5 only; m6 begins to bind only after `refresh.py` appends entries, which is also when the frozen
m6 rules (`:171-175`: quote verbatim in `reader_files`, `wrong_expectations == len(findings)`) start to apply:
`.ufo/evidence/round-52/coldread/refresh.py:216` writes `wrong_expectations = len(reader['findings'])`, so an
honest finding keeps m6 green while leaving the section uncredited (§4).

## 4. What the monitor arithmetic forces on the re-key (derived, not a verdict)

Credit rule at CAND1: an entry credits a section only with `wrong_expectations == 0` and a passing input gate
(`.ufo/evidence/round-18/measure.py:472`, `:493`); a non-stale matching entry that fails vetoes the whole
section (`:635`); coverage needs `credited > 0 and not vetoes` (`:638`). Since the re-key entry's
`wrong_expectations` equals its finding count, after the re-key

```
credited = 45 + #{of the 19 re-keyed sections whose reader recorded zero findings}
```

so `credited >= 64` at the deciding run holds **iff all 19 readers record no stale statement**. A single honest
finding in any of the 19 caps the monitor at 63 and keeps `coldread-floor` RED. That is the round's declared
honest-stop shape, not a defect; recorded here so a wave-3 finding is not later read as a wave failure, and so
the L1 sees that "re-key done" and "monitor green" are the same event only if the re-reads are clean.

## 5. Re-key instrument preconditions (read-only probe)

`.ufo/evidence/round-52/coldread/refresh.py` is the instrument the L1 must run. Probed without mutating the
lane: imported the instrument and the round-49 helper module against the scratch clone at CAND1 and replayed its
`sectionize`/`cited_files`/`follow_internal` path for the 19 target headings
(`T52W3ExecNoHarm-rekey-probe.out`):

```
VOLATILE ['LOG.md','SCORECARD.md','corpus/QUALITY.md','corpus/README.md','corpus/SOURCES.md']
sections_at=64 targets=19
OK … (19 rows) …
WOULD_ABORT=0 of 19
```

- Targets = base-credited ∧ ¬cand-credited (`refresh.py:173-175`) = the same 19 the precheck lists.
- Every one of the 19 cites ≥1 non-record lane file, so the `section %s cites no non-record lane file` guard
  (`refresh.py:193`) will not fire.
- The 3 `input-drift` sections cite `corpus/knowledge/fleet-kill-rate-ledger.md` **directly**
  (`### The re-sweep cadence…`, `### The re-pin semantics, as executed`, `## The operator's runbook…` plus the
  `tools/*` inputs), so a fresh trace rebinds the new digests and clears the drift.
- Operability constraint worth knowing before the run: `refresh.py:165` aborts
  (`working-tree ledger differs from the ledger at CAND`) unless the lane working-tree
  `.ufo/evidence/round-21/coldread/ledger.json` is byte-equal to the blob at the CAND argument. It must be run
  with CAND = the rev whose ledger is still the working-tree file (it is today: `cand1..HEAD` touches no
  ledger), and not after a later ledger edit lands uncommitted.
- The instrument has no `--selftest` (grep of `refresh.py` finds none), unlike both round-52 counters; its own
  output is the only evidence of its behaviour.

## 6. Census — exit 0, warnings only

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file \
      /fast/scratch/hyaku/tameshi-r52/T52W3ExecNoHarm/clone/corpus/SOURCES.md --today 2026-10-27
file  W04  S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file  W04  S048 … (S075, S076, S077, S078, S081, S092, S104, S160, S265, S266, S267, S268, S274)
file  W01  S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
file  ok    /fast/scratch/…/clone/corpus/SOURCES.md
census-rc=0
```

Receipt: `T52W3ExecNoHarm-census.out` (15 × W04, 1 × W01, final `ok`, exit 0). The contract's frontier-step
form gives the same answer at the fleet root:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi  … same 16 warning lines …   tameshi  ok  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
rc=0
```

Receipt: `T52W3ExecNoHarm-census-root.out`. W-codes never change status (`sources-census.sh` header), so the
census gate is clean at CAND1: exit 0, `ok`.

## Findings

**F1 — RED, pre-registered: `coldread-floor score=6 credited=45` at CAND1.**
Cause: 16 sections lost as `no-ledger-entry` (SKILL.md section digests changed by the round's 59 in-line fixes;
matcher keys on section `sha256`, `.ufo/evidence/round-18/measure.py:607-618`) and 3 as `input-drift` on
`corpus/knowledge/fleet-kill-rate-ledger.md` / `tools/*` (`§2` above).
Shown by: `HYAKU_SCRATCH=$S bash .ufo/evidence/round-52/no-harm.sh LANE 7ff81a5b0ab0…` (§1) and
`python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev 7ff81a5b0ab0… --explain` (§2,
`T52W3ExecNoHarm-coldread-cand1.out`). This monitor is the only regression against BASE, and it is the one the
contract declares will stay RED until the re-key lands.

**F2 — the re-key can only restore credit through zero-finding entries (arithmetic, code-cited).**
`.ufo/evidence/round-18/measure.py:472,493,635,638` + `.ufo/evidence/round-52/coldread/refresh.py:216` imply
`credited = 45 + #{clean re-keys}`; the deciding run needs 64, so all 19 must be clean (§4). Honest findings are
still recorded — they just leave the section uncredited, which is the designed honest stop.

**F3 — C2's `m6 ok` is vacuous now, and m6 has a reader-file hole.**
`.ufo/evidence/round-52/c2/measure.py:167` (`t52 = [… seats startswith 'T52']`) returns 0 entries at CAND1, so
m6 contributes 0 to `total` without inspecting anything. Probing the entry shape on a scratch clone at CAND1
plus one synthetic commit (`T52W3ExecNoHarm-c2-m6probe.out`, probe rev `d8abe0ba97e36075b250d882934d1f2431740edc`
inside the scratch clone only):

```
m6 MISMATCH bad=['PROBE-B-zero-findings-no-reader-files:findings-or-reader-missing',
                 'PROBE-C-zero-findings-one-missing-reader:findings-or-reader-missing',
                 'PROBE-E-one-quote-count-zero:count!=findings',
                 "PROBE-G-forged-quote:quote-not-verbatim:'this sentence does not appear…'"]
```

`PROBE-A` (zero findings, one existing reader file) and `PROBE-D` (zero findings, **two** nonexistent reader
files) both pass. The leniency is `.ufo/evidence/round-52/c2/measure.py:170-171`: `'\n'.join(show(…) or '' for f
in files)` is `''` for one missing file (falsy → `texts or None` → mismatch) but `'\n'` for two (truthy → empty
`flat` → no findings to check → pass). Consequence: m6 will not catch a re-key entry that lists two
non-existent reader files with zero findings; it will reject the one-file case. Practical rule for the L1: list
at least one **existing** reader file per re-key entry, and treat m6's green as meaningful only after
`t52_entries=19`.

**F4 — `refresh.py` preconditions verified: run it against the rev whose ledger is the working-tree file.**
`.ufo/evidence/round-52/coldread/refresh.py:165` aborts on any ledger divergence from CAND; targets are exactly
the 19 lost sections (`:173-175`); no target hits the `cites no non-record lane file` abort (`:193`), and the
drift inputs are cited directly, so fresh traces clear the drift (`T52W3ExecNoHarm-rekey-probe.out`,
`WOULD_ABORT=0 of 19`).

**F5 — census W04: the round opened a second row on an already-registered URL.**
`corpus/SOURCES.md:149` (S274, opened 2026-10-27, `used-by corpus/lessons/round-52.md`) carries
`https://bazel.build/basics/hermeticity`, already registered at `corpus/SOURCES.md:73` (S064, opened 2026-10-20,
mined, `used-by corpus/knowledge/input-keyed-coldread-credit.md`). The census reports both as
`W04 duplicate url … across scopes` and stays exit 0 by contract (`W` codes never change status). The two rows
record different "markdown alternate" digests — S064 `76167a0d…`, S274 `2355150f…`. I re-fetched the live
rendition today:

```
$ curl -sS -m 25 -o $S/herm.md -w 'http=%{http_code} bytes=%{size_download}\n' https://bazel.build/basics/hermeticity.md
http=200 bytes=5878
$ sha256sum $S/herm.md
2355150f5e9b08c392de169a67b788f4b3f0c446919a8abea9180bf9daccbbc6
```

S274's recorded digest is live-accurate (5878 B, HTTP 200); S064's older digest no longer matches the current
rendition. No monitor covers this (the census only warns), and it does not touch m1–m6 or C1. Recorded as a
C2/census observation; the fix belongs to a later round that re-pins S064, not to this wave.

**F6 — the assignment's "lane branch tip" label is stale.** HEAD is `f1a3246`, CAND1 is its ancestor; the 6
added paths are `.ufo` evidence/spec only, no content file, and C2 at HEAD also prints `total=0`
(`T52W3ExecNoHarm-c2-head.out`), so this seat's results hold at both revs. No-harm was run at the named rev
`7ff81a5b…` as instructed.

## Deliverables (all under `.ufo/waves/round-52/w3/`)

| file | content |
|---|---|
| `T52W3ExecNoHarm-noharm.out` / `.err` | no-harm at CAND1 (10 ok, coldread-floor RED), empty stderr |
| `T52W3ExecNoHarm-noharm-base.out` / `.err` | no-harm at BASE (11 ok) |
| `T52W3ExecNoHarm-c2.out` | C2 `--explain` at CAND1, `total=0 PASS=true` |
| `T52W3ExecNoHarm-c2-selftest.out` | `C2_SELFTEST: cases=8 failed=0` |
| `T52W3ExecNoHarm-c2-base.out` | C2 at BASE, `total=27` (matches contract `before`) |
| `T52W3ExecNoHarm-c2-head.out` | C2 at lane HEAD `f1a3246`, `total=0` |
| `T52W3ExecNoHarm-c2-m6probe.out` + `…-m6probe-reader.md` | m6 entry-shape probe on the scratch clone |
| `T52W3ExecNoHarm-m6probe-apply.py` | the seven synthetic entries used by that probe (for re-running it) |
| `T52W3ExecNoHarm-rekey-probe.py` | the read-only `refresh.py` target/abort probe (§5) |
| `T52W3ExecNoHarm-coldread-cand1.out` / `.err` | coldread `--explain`, 19 lost with per-section reasons |
| `T52W3ExecNoHarm-rekey-probe.out` | `refresh.py` target/abort surface for the 19 sections |
| `T52W3ExecNoHarm-census.out` | census `validate --file` on the CAND1 copy, exit 0 |
| `T52W3ExecNoHarm-census-root.out` | census `validate --root FLEET tameshi`, exit 0 |

## Risks and blockers

- No blocker for this seat's item: all three runs are reproduced above and their receipts are in `w3/`.
- Blocking for the round, not for me: per F2 the deciding run's `coldread-floor` is green only if all 19
  re-keyed readers record zero findings; per F3 the C2 pass at CAND1 carries a vacuous m6 and will get its
  first real test from those same entries. A re-key entry naming two nonexistent reader files with zero
  findings would pass m6 silently (F3) — that is the shape most worth a checker's eye when the re-key lands.
- Lane state was left untouched except for the wave-3 dispatch files that already existed; the scratch clone
  (including the probe commit `d8abe0ba`) and the scratch root were deleted before yield.

## Summary

No-harm at CAND1 `7ff81a5b`: 10 of 11 monitors ok; `coldread-floor score=6 credited=45` RED, exactly the
pre-registered 19-section loss (16 `no-ledger-entry` from SKILL.md section digests, 3 `input-drift` on the
kill-rate ledger and `tools/*`). BASE re-run is 11/11, so nothing else regressed.
C2 at CAND1 (and at HEAD `f1a3246`): `m1..m6 = 0`, `total=0 C2_R52_PASS=true`; BASE gives `total=27`; counter
selftest 8/8. Caveat: m6 is vacuous (`t52_entries=0`) and has a reader-file hole (two missing files pass).
Census: exit 0 (15 W04 + W01); S274 duplicates S064's Bazel hermeticity URL, and my live fetch confirms S274's
digest while S064's no longer matches the current rendition.
Re-key math: `credited = 45 + clean re-keys`, so 64 needs all 19 readers clean; `refresh.py` will not abort on
any of the 19 (`WOULD_ABORT=0`) but must run while its CAND ledger equals the working-tree ledger.
