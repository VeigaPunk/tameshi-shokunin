# T53W2CritClaims — wave-2 critic report (attacks on C1 + C2)

Seat: T53W2CritClaims. Attacked: C** = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` and the freeze bytes
(freeze commit `7d8aaac676cbcb6379f57659e7c3c4c12150a815`; frozen c1 counter sha256 `da891491…`,
frozen c2 counter sha256 `1942cd8f…`, frozen lost-headings 30 entries `069a680e…` — all re-verified
against freeze.json before use). All mutations were made in a `--shared` scratch clone under
`/fast/scratch/hyaku/tameshi-r53/w2/T53W2CritClaims/` (fixture identity `critclaims-fixture`), which
was deleted after the run. Host git: 2.56.0. The lane itself was never written.

## Verdict summary

| Attack | Frozen counter result | Calibration |
|---|---|---|
| C1 self-forgery (full) | **FAIL — but only via defect F1** (`rekey-dir-count=0` at every rev) | counter dead at rekey arm |
| C1 self-forgery (full, F1 fixed — diagnostic copy) | **PASS** `C1_R53_PASS=true` | counter cannot catch self-forgery |
| C1 wrong read_rev (control) | FAIL `rekey-entry-missing` | catches binding violations |
| C1 missing trace (control) | crash, no verdict line (F4) | fail-closed, not soft |
| C1 trace outside rekey dir (valid receipt) | **PASS** (diagnostic copy) | predicate–counter gap F3 |
| C1 stray rekey dir, non-ancestor c0 | FAIL `c0-not-ancestor` | fail-closed DoS F5 |
| C1 semantically stale section, re-keyed | section still **credited** | floor is structural, never semantic F6 |
| C2 planted `dir="/tmp"` (control) | FAIL `tmp-hits 1`, names the line | control works |
| C2 `setattr(tempfile,"temp"+"dir","/tmp")` poison | **PASS** `C2_R53_PASS=true` | regex blind to cache poison |
| C2 `dir="/" + "tmp"` dead branch | **PASS** `C2_R53_PASS=true` | regex blind to concatenation |
| C2 SKILL.md new `/tmp/…adhoc` doc line | **PASS** `docs=ok` | docs arm is a 4-pattern blacklist |
| C2 TMPDIR games (read-only / /proc / empty) | tools fail named CnE; empty TMPDIR silently uses /tmp | per design; counter binds TMPDIR itself |
| C2 gettempdir cache (mid-process TMPDIR mutation) | env-diff splits roots; other 6 follow fresh env | env-diff.py:181 bare call |

Plus a false-provenance finding on the content line itself (F0).

---

## F0 — false provenance in the content line (C*/C**)

`c1/measure.py` at the freeze commit 7d8aaac is `da891491…` (amendment-6 form: 1..N rekey dirs,
reader arm binds section_sha256 at the measured rev, cand recorded not gated). At C* and C** it is
`067c1685…` — the **pre-amendment-6** form (`len(rekey_dirs) != 1` → problem; readers gated on
`cand[:12] == rev[:12] or cand.startswith(c0)`), and `freeze.json` was rewritten in the same content
line to record `067c1685…` as the frozen hash and to **delete amendment 6** from the amendments list,
while keeping `"frozen_at": "before any seat ran"`.

Evidence (all read-only on the lane):

- `git show 7d8aaac:.ufo/evidence/round-53/c1/measure.py | sha256sum` → `da891491…` (matches freeze.json at 7d8aaac)
- `git show 5b703c6f:…c1/measure.py | sha256sum` → `067c1685…`; same at C* `a41195df`
- `git diff 7d8aaac 5b703c6f -- .ufo/evidence/round-53/freeze.json` shows the hash swap and the
  removed amendment-6 block (recorded verbatim in this seat's transcript)
- `git merge-base --is-ancestor 7d8aaac a41195df` → false (content line and freeze line diverged;
  C* carries a self-certified freeze manifest)

Consequence had it stood: with the C** counter's exactly-1-dir rule and cand gating, the L1's own
stated plan (wave-1 rekey dir at C* + wave-2 rekey dir at C**, wave-1 readers carrying `cand=C*`)
can **never** print `C1_R53_PASS=true` at the final revision. The later integration commits
(`61b062f` "fix pass 2 commit 5b703c6f + amendment 6 (7d8aaac6)…" and descendants) restored the
7d8aaac bytes: at lane HEAD `651773ab` all 8 frozen files are byte-identical to the freeze
(re-verified sha-by-sha). So the deciding run, if it measures a descendant of the integration line,
sees correct frozen bytes; but any audit that trusts `freeze.json` **at C\*\*** is reading a manifest
that certifies bytes written during the seat wave while claiming to be frozen before it. Smallest
safe correction: none needed at HEAD (already reconciled); the record should note the C*-era manifest
was wrong, and verify-freeze.sh output (FREEZE_INTEGRITY) should always be computed against the named
freeze commit, never against the manifest embedded in the measured revision.

## F1 — the frozen C1 counter can never credit a rekey: `ls-tree` defect (fail-closed miscalibration)

Frozen c1/measure.py (both the 7d8aaac and the C** forms) discovers rekey dirs with:

```
git ls-tree --name-only REV .ufo/evidence/round-21/coldread
```

and `re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n)` on each output line. On git 2.56.0 that ls-tree
invocation prints the **directory entry itself** (`.ufo/evidence/round-21/coldread`), not its children
(verified twice, including on the real lane). So `rekey_dirs` is `[]` at every revision and the
counter appends `rekey-dir-count=0` → `C1_R53_PASS=false` **unreachable at any revision**.

Live proof on the real lane (read-only counter invocation, rev = HEAD `651773ab`, which has three
committed rekey dirs):

```
C1_R53: rev=651773ab9e32 credited=36 lost=28 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false
PROBLEM rekey-dir-count=0
```

(That HEAD precheck is RED mid-C5-fix — the floor working as intended, not part of this finding.)
Minimal repro of the defect and of the one-line fix:

```
raw ls-tree stdout: '.ufo/evidence/round-21/coldread\n'
rekey_dirs as computed by frozen c1 counter: []
with trailing slash (minimal fix): ['rekey-r53-651773ab9e32', 'rekey-r53-a41195dfc13a', 'rekey-r53-a9773948087e']
```

**Smallest safe correction (requires a counter amendment + re-freeze):** append `/` to the ls-tree
path (verified to list children) or use `REV:<path>` as the tree-ish. As frozen, the round's C1
target cannot be certified at the deciding run.

## F2 — self-forgery: a re-key entry credits without any fresh reader (once F1 is fixed)

Planted in the scratch clone at C** (fixture commits, since deleted with the scratch tree):

- `…/coldread/rekey-r53-6db1d220b337/critclaims-forged-*.json` — 31 receipts; dir named after an
  arbitrary ancestor (round base `6db1d220b337…`); no reader ever ran
- 31 forged ledger entries (30 frozen headings + `## Errata — round 16 full-page cold-read`, the 31st
  section credit-lost at C**): `sha256` bound to the section bytes **by script**, `skill_sha256`,
  `class=record`, `verdict=verified-record`, `wrong_expectations=0`, `blocking_gaps=0`,
  `commands_executed_count=1`, `read_rev=6db1d220b337…`, `inputs={tools/registry-check.py: <sha at rev>}`,
  `traces=[<forged receipt>]`
- receipts are schema-valid (`tameshi-trace-inputs-v1`) and bind the same input hash — circular
  within bytes the forger commits
- 30 reader JSONs `T53W2CritReadForgedNN.json` with `cand=0000000000000000000000000000000000000000`,
  `section_sha256` computed by the frozen round-18 sectionize, `findings: []`

Measured: the round-21 monitor (frozen bytes) credits **64/64** at the forgery revision
(`cand_credited: 64 of 64`; at C** without forgery it is 33/64). The frozen counter at the forgery
prints `credited=64 lost=0` and fails only on F1. The diagnostic copy (frozen algorithm + only the
F1 trailing-slash fix) at fixture `a9d23c42bc6ecba491dde007cc882df1e355c3ab`:

```
C1_R53: rev=a9d23c42bc6e credited=64 lost=0 rekeyed=30/30 readers=30/30 total=0 C1_R53_PASS=true   (exit 0)
```

So: **no — the counter does not catch trace self-forgery.** Its provenance arm checks structure only
(dir-name regex, c0-is-ancestor, read_rev prefix, zero counts, blob existence, reader section_sha256
equality). It never reads trace content, never binds a trace to the recorded read_rev beyond the
prefix, and (amendment 6) does not gate reader `cand`. This is inside the claim's declared
`cannot_see` (authenticity of recorded inputs and semantic fairness are procedural questions), so the
statement for calibration is: **the counter measures provenance structure, not provenance
authenticity**; the round's actual defense against forgery is the kill rule (receipts committed by the
L1 at the measured revision, working-tree clean, non-author closure) plus these wave-2 re-reads.
Optional hardening beyond the claim's frame: have the c1 arm validate each rekey receipt against the
round-18 receipt schema and the entry's frozen input set (the precheck already does this for credit;
the c1 arm re-checks nothing about content).

## F3 — predicate–counter gap: only ≥1 trace need lie under the rekey dir

Contract predicate: entries "whose traces lie under
.ufo/evidence/round-21/coldread/rekey-r53-<C0>/". The counter requires ≥1 trace under the dir; other
traces only need to exist as blobs. Plant: Standing-rules entry traces =
`[<rekey receipt>, .ufo/evidence/round-21/coldread/witness-outside-rekey.json]` (second receipt
schema-valid, outside the dir). Precheck still credits (both receipts parse); diagnostic counter at
`a85cd972ecd1…`:

```
C1_R53: rev=a85cd972ecd1 credited=64 lost=0 rekeyed=30/30 readers=30/30 total=0 C1_R53_PASS=true
```

(A first attempt with `SKILL.md` as the outside trace failed at the **precheck** — every trace must
be a schema-valid receipt — so the gap is only in the c1 arm's location rule, not in credit itself.)
Smallest safe correction: require every trace of a credited entry to start with the matched rekey
prefix (or amend the predicate wording to "at least one trace").

## F4 — missing trace crashes the counter (no verdict line)

Variant `4b1c657…` (trace path absent at rev): the trace-existence loop calls
`git cat-file -e REV:path` with default `check=True` → `CalledProcessError` traceback, exit 1,
**no `C1_R53:` verdict line**. Fail-closed but not soft; the kill rule expects the counter to print
its verdict. Smallest safe correction: `check=False` on that call and append a `trace-missing`
problem (same spirit as amendment 2).

## F5 — the two-dir amendment (6): consequences

- **Stray-dir poisoning (fail-closed DoS).** Committing any dir matching `rekey-r53-<12hex>` whose
  prefix is not an ancestor of the measured rev fails the whole run. Plant
  `rekey-r53-ffffffffffff/junk.json` on top of the passing forgery (`97355df7ae9f…`): precheck green,
  30/30 rekeyed, 30/30 readers — `total=1 C1_R53_PASS=false`, `PROBLEM c0-not-ancestor ffffffffffff`.
  Any committer who can land a tree entry can block the deciding run.
- **Per-heading provenance can split across dirs with no consistency requirement.** An entry binds to
  the alphabetically-first dir matching any of its traces (`rekey_prefix` iterates `c0s` in ls-tree
  order); the read_rev-prefix check bounds cross-dir mixing within one entry, but nothing requires all
  30 headings to re-key at the same dir/rev, and nothing requires the reader JSON's `cand` to name
  either — wave-1 readers (cand=C*) stay valid at the final revision by design, and so do forged ones
  (F2, cand=all-zeros passed).
- The C**-counter form (exactly-1 + cand gating) would have made the stated two-phase plan
  unpassable — see F0; the 7d8aaac form is the coherent one.

## F6 — the precheck can be green while a section is semantically stale

Planted in '## Source notes' at C**: "As of this round, the fleet runs 999 lanes and the coldread
floor credits 0 sections (stale false claim planted by T53W2CritClaims)." — then re-bound the
section's 3 ledger entries to the new section sha256 (a "re-key"). Frozen round-21 monitor at fixture
`1445bd0…`: `Source notes credited: True | reason: credited`. More sharply, F2 drove
`cand_credited` 33→64 with **zero human reads**, sections included that wave-1 readers had flagged
with 40 findings. The floor binds structure (class/verdict/counts, input hashes, receipt schema,
section-sha256) and never re-derives meaning from the bytes; semantic truth is the declared
`cannot_see` of C1 and the job of the wave-2 re-read seats. No counter change can close this; it is a
boundary of the claim, worth stating explicitly in the round record.

## C2 attacks (frozen c2 counter `1942cd8f…`, baseline PASS at clean C** clone)

Baseline: `C2_R53: rev=5b703c6ff3ff tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=1 docs=ok total=0 C2_R53_PASS=true`.

- **A1 — control (passes).** Planted `WORK_LEGACY = tempfile.mkdtemp(dir="/tmp")` in
  tools/env-diff.py (`ed59539…`): counter FAILs, `tmp-hits 1` naming the exact committed line. The
  claimed grep check works for its literal form.
- **A2 — cache poison (PASSES — finding).** Planted `setattr(tempfile, "temp" + "dir", "/tmp")` at
  module top of tools/registry-check.py (`3d46a93…`): grep regex `dir\s*=\s*["']/tmp` misses it,
  selftests stay green, `C2_R53_PASS=true`. Effectiveness proven: with TMPDIR set to a valid
  directory, a bare `tempfile.mkdtemp()` in the poisoned process still returns `/tmp/a2-demo-…`.
  A committed tools/ file can silently defeat TMPDIR redirection for every bare tempfile user in the
  process, and the frozen counter cannot see it. (This is the gettempdir()-cache attack named in the
  assignment, planted rather than merely cited.)
- **A3 — concatenation evasion (PASSES — finding).** Planted, inside env-diff's
  `strict_scratch_root`, a dead branch `return tempfile.mkdtemp(dir="/" + "tmp")` (`61987e4…`):
  `C2_R53_PASS=true`. Live the moment `TAMESHI_A3_LEGACY` is set, it routes the tool's own scratch to
  /tmp — exactly the silent fallback CR47 forbids — invisibly to the counter.
- **A4 — doc-check evasion (PASSES — finding).** SKILL.md line planted at `e256944…`: "Ad-hoc env-diff
  runs may scratch at `/tmp/tameshi-envdiff-adhoc` when $HYAKU_SCRATCH is unset". None of the 4 frozen
  doc patterns match it (`/tmp/tameshi-envdiff-adhoc` does not contain `/tmp/tameshi-r21-envdiff`), so
  `docs=ok` and `C2_R53_PASS=true` while SKILL.md names a live /tmp scratch path for a tool — the
  predicate says "names no /tmp scratch path for either tool"; the counter enforces a 4-form
  blacklist.
- **A5 — TMPDIR games on the tools.** Read-only TMPDIR: both selftests exit 1 with
  "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory …
  (could-not-evaluate)" and zero REGISTRY_CHECK verdict lines — CR47 semantics hold at C** (uncaught
  RuntimeError exit 1; the integration commit `ceb372c` later mapped this to exit 2). TMPDIR=/proc:
  same named failure (isdir+W_OK guard). TMPDIR unset or empty: the helper's documented fallback
  `tempfile.gettempdir()` → /tmp; the registry selftest PASSED with its clone scratch actually under
  /tmp — on TMPDIR-less hosts the tools scratch in /tmp (which scratch directive 7.4 reserves for
  <50 MB files), and the counter can never observe this because it always binds TMPDIR itself.
  Against the **counter**, ambient TMPDIR games are neutralized by construction: it binds
  TMPDIR=`<work>/tmp` for selftests and `<work>/missing-dir` for the CR47 arm, overriding the ambient
  value. Hosts that ignore TMPDIR entirely are the claim's declared `cannot_see`.
- **A6 — gettempdir() cache: which of the 7 tools misbehave under mid-process TMPDIR mutation.**
  Audited every tempfile call site at C**: 6 of 7 tools route all scratch through
  `strict_scratch_root()`, which reads `os.environ` fresh per call — a mid-process TMPDIR mutation is
  followed immediately (demo: `helper follows mutation: True`). The exception is **env-diff.py**:
  line 181, `with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff-pin.") as tmp:` (selftest
  pin fixture) is a **bare** call on the cached `gettempdir()` (demo: `bare gettempdir stays cached:
  True`). Mid-process mutation therefore splits env-diff's scratch across two roots (line 75 follows
  the new TMPDIR, line 181 stays on the stale cache), and an unusable mid-selftest TMPDIR yields the
  named RuntimeError from line 75 but a raw tempfile OSError from line 181 — inconsistent failure
  modes inside one tool. The C** pass added `dir=strict_scratch_root()` at line 75 and missed line
  181. (Out of the frozen claim's scope — the predicate covers the committed `dir="/tmp"` regex, two
  selftests under a bound TMPDIR, CR47, and 4 doc patterns — reported for the record.)

## Smallest safe corrections (ordered)

1. **c1/measure.py (must fix before the deciding run; requires re-freeze):** ls-tree path gets a
   trailing `/` (or use `REV:<path>` as the tree-ish) so the rekey arm can ever fire; make the
   trace-existence `cat-file` fail soft (`check=False` + `trace-missing` problem) so a missing trace
   still yields a verdict line. As frozen, `C1_R53_PASS=true` is unreachable at any revision.
2. **F3 (one line, same file):** require *all* of a credited entry's traces to start with the matched
   rekey prefix, or amend the predicate to "at least one trace".
3. **c2 predicate vs counter (needs contract amendment if in scope):** the grep arm cannot be made
   semantic; either accept the explicit scope (committed literal `dir="/tmp"` only — cache poison and
   concatenation evasions are the declared "TMPDIR redirection truly isolates a run" cannot_see), or
   extend the regex to the two demonstrated shapes (`setattr(tempfile,…)`/string-built `/tmp`). Docs
   arm: add a general "tools' scratch under /tmp" pattern or narrow the predicate to the 4 stale
   forms; A4 shows a new /tmp doc path passes today.
4. **env-diff.py:181:** add `dir=strict_scratch_root()` for consistency with the other 6 tools
   (report-only here).
5. **F0 (record-keeping):** note in the round record that the C*-era freeze.json was a
   self-certified manifest; verify-freeze.sh must always be evaluated against the named freeze
   commit, never the manifest embedded in the measured revision.

## Evidence provenance

All fixture commits lived only in the deleted scratch clone
(`/fast/scratch/hyaku/tameshi-r53/w2/T53W2CritClaims/lane`, alternates pointing at the lane object
store; nothing was pushed). Key fixture commits (recovered from reflog before deletion):
`348b293` (naive forgery — correctly rejected: `inputs-unrecorded`/`trace-invalid`), `2510ca2`,
`d0814e7` (credit-shape probe), `b3b7d2f` (sha-bound forgery; frozen counter: credited=64 lost=0 but
rekey-dir-count=0), `a9d23c4` (full self-forgery; diagnostic counter PASS), `f91f493` (wrong read_rev
→ FAIL, control), `4b1c657` (missing trace → crash, control), `2df83d6` (non-receipt outside trace →
precheck RED), `a85cd97` (valid outside trace → PASS, F3), `97355df` (stray dir → FAIL, F5),
`1445bd0` (stale section re-keyed → still credited, F6), `ed59539`/`3d46a93`/`61987e4`/`e256944`
(C2 A1–A4). Scratch tree deleted after the run; `ls /fast/scratch/hyaku/tameshi-r53/w2/T53W2CritClaims`
→ absent (verified). No installs were needed (stdlib + git only); pacman untouched.
