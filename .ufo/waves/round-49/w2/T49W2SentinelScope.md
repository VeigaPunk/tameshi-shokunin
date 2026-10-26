# T49W2SentinelScope — scope and safety review of `f181a961` vs `8ca67421`

Seat: sentinel (wave 2, falsify). Read-only on the lane; nothing here is a verdict, and no claim counter was invoked.
All commands run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Receipts for every command cited below are
committed beside this report in `.ufo/waves/round-49/w2/T49W2SentinelScope.receipts/` (`changed-paths.txt`,
`pins-and-sizes.txt`, `secret-scan.txt`, `binary-scan.txt`, `tmp-scan.txt`, `containment-and-integrity.txt`,
`runner-path-safety.txt`, `wave-attribution.txt`). Scratch (`/fast/scratch/hyaku/tameshi-r49/`) used for the tree
extraction only; deleted before yielding. No tool installed or upgraded (none needed): no pacman transaction, no
`uv`/`npx`/binary install.

Candidate under review: `f181a961ae44061af486f600e5ea257d2baf78f8`; base `8ca67421111fa354b47b803358391d0b07fc6db9`;
counter freeze `14d03ea4270c6904064022b62b6faf467e5c0968`.

## Check results

| # | Item | Result |
|---|---|---|
| 1 | every changed path inside the lane write scope | **PASS** — 461 paths (454 A, 7 M), all lane-relative, no symlink/gitlink, no odd names |
| 2 | `tools/` only adds `tools/pbt-staged-id.py` | **PASS** |
| 3 | no pinned tool changed (sha256 vs `freeze.json`) | **PASS** — 13/13 pins byte-equal at freeze and candidate |
| 4 | no file > 1 MiB added outside evidence | **FAIL (literal)** — one file, 1.21 MiB, under `.ufo/waves/` (F1) |
| 5 | no secret-looking content in snapshots/receipts | **PASS** — 0 hits over 454 added files, all `+` diff lines, and added binaries |
| 6 | no `/tmp` path cited as evidence | **PASS** — no new `/tmp` citation this round (F5 is the neighbouring scratch-path item) |
| 7 | (adjacent) hidden panel not leaked / deciding run not consumed early | **PASS** — F6 |

Evidence for each, with the command and its observed output:

1. `git diff --name-status 8ca67421… f181a961…` → `461` lines (`A` 454, `M` 7). `git diff --raw …` → new-file modes
   `100644`×440, `100755`×21, zero `120000`/`160000`. Every path begins `.ufo/`, `corpus/`, `tools/`, or is
   `SKILL.md`/`LOG.md`/`SCORECARD.md`; the only non-`.ufo`/`corpus`/`tools` paths are those three root files
   (`containment-and-integrity.txt` §1). All 401 changed paths under `.ufo/waves/round-49/` resolve to one of the 55
   declared seat prefixes in `.ufo/waves/round-49/spec-w1.json` (`items[].name`) or to the wave harness
   (`w1/excerpt-check.txt`, `w1/swarm-registry.json`, `spec-w1.json`, `w1-dispatch.*`, `build-spec*.py`):
   `attributable=399 + harness=2` (`wave-attribution.txt`).
2. `git diff --name-status 8ca67421… f181a961… -- tools` → `A	tools/pbt-staged-id.py` (no other line). This is the same
   predicate the frozen monitor applies (`.ufo/evidence/round-49/no-harm.sh:26-27`: `case "$T" in ""|"A:tools/pbt-staged-id.py ")`),
   so the candidate is inside the round's declared tools scope by construction and by independent check.
3. `python3` loop over `freeze.json.sha256` hashing `git show <rev>:<path>` at both revisions → 26 `PIN_OK` lines, 0
   `PIN_DIFF` (`pins-and-sizes.txt`), including the named gate `tools/staged-id-guard.py` =
   `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` and the frozen contract, both counters, both
   control harnesses, `no-harm.sh`, `deciding-run.sh`, `.ufo/evidence/round-21/coldread/measure.py`,
   `.ufo/evidence/round-18/measure.py`, `.ufo/evidence/round-48/quality/coldread-precheck.sh`. `tools/staged-id-guard.py`
   is also unchanged base→candidate (three-way hash equal).
4. See F1.
5. `grep -I` over the 454 added files plus `git diff … | grep '^+'` with the key/token/credential pattern set →
   `added_scan_hits=0`, `diff_plus_line_hits=0`, `secret_named_files_added=0` (`secret-scan.txt`); `grep -a` over the
   added PDFs/PNGs → `binary_hits_total=0` (`binary-scan.txt`).
6. `git diff … | grep '^+' | grep -c '/tmp/tameshi-r49'` → `0`; `/tmp` strings inside the 253 appended ledger lines →
   `0` (`tmp-scan.txt`). Every `/tmp` string in the diff is quoted historical case-note text (`/tmp/tameshi-r2-1-work`,
   `-r3-1-work`, `-r12-*`, `-r14-*`, `-r17*`, `-r18*`, `-r29-*`, `/tmp/ReRead06-*`, `/tmp/ColdB07-*`) or the unchanged
   Standing-rules template on the context line `SKILL.md:141`. Inside round-49 evidence, `/tmp` appears only in
   `.ufo/evidence/round-49/c1/reads.json` (2 lines, quoting the historical note text) and
   `.ufo/evidence/round-49/control/monitor-at-base-8ca67421.json` (30 lines, which re-emit the ledger's pre-existing
   `external` maps — same strings at base).
7. F6.

## Findings

### F1 — a 1.21 MiB PDF was added outside `.ufo/evidence/` (bound exceeded; no monitor covers it) — LOW

Attack surface: the wave bound "no file > 1 MiB added outside evidence", and repo weight.

Evidence — command `git cat-file -s f181a961…:<path>` for every added path, classified by prefix (`pins-and-sizes.txt`):

```
OUTSIDE-EVIDENCE 1269821 .ufo/waves/round-49/w1/T49ScribeRows.src/smallbone.pdf
```

That is 1.211 MiB, in `.ufo/waves/`, not `.ufo/evidence/`. It is the first such file: at base, `git ls-tree -r -l
8ca67421…` filtered to `.ufo/waves/` and size > 1048576 returns `count= 0`, while every >1 MiB blob at base lives under
`.ufo/evidence/`. (Under the looser reading "`.ufo/` is evidence" the file passes; under the literal bound it does not —
I report the literal reading.) No round-49 monitor would catch it: `no-harm.sh` has no size monitor, and its only
`tools/`-scoped line is `no-harm.sh:26-27`.

Impact: 1.21 MiB of duplicated third-party bytes in the lane's history (the same paper's text is already committed as
page extracts under `.ufo/waves/round-49/w1/T49ExecSrcSmallbone/pages/`, and its sha256 + page map are recorded in
`corpus/SOURCES.md` S270 and `T49ScribeRows.md:12`). A bound that is stated and then exceeded with no monitor is a
calibration defect: the next round cannot tell whether the bound was meant.

Smallest remediation: drop the blob (`git rm --cached`-equivalent in the L1's own commit flow, i.e. remove the path from
the tree that becomes REV) and keep S270's citations pointing at the fetched-bytes digest plus the committed page
extracts; alternatively amend the bound in the wave spec to "1 MiB outside `.ufo/`; 1.5 MiB under `.ufo/waves/`" so the
next seat has a real ceiling. Do not add a size monitor mid-round unless the spec says so.

### F2 — the deciding script's `OUTDIR` containment and emptiness are prose only — LOW

Attack surface: the one command that creates the round's decisive receipts (`.ufo/evidence/round-49/deciding-run.sh`).

Evidence — `grep -n 'OUT|outdir|EMPTY' .ufo/evidence/round-49/deciding-run.sh` (`runner-path-safety.txt`):

```
4:#   FREEZE  … OUTDIR  an existing, EMPTY directory inside LANE for receipts
13:LANE=$1; REV=$2; FREEZE=$3; OUT=$4
22:[ -d "$OUT" ] || { echo "DECIDING_REFUSED outdir-missing"; exit 3; }
```

`OUT` comes straight from `argv[4]`; the script checks only that it is a directory (`:22`) and that it holds no
`c1.start`/`c2.start` (`:29`). Nothing asserts `OUT` is under `$LANE/.ufo/evidence/round-49/`, and nothing asserts it is
empty — yet it writes `frozen.stdout`, `no-harm.*`, `coldread-precheck.*`, `census.*`, `c2.*`, `c1.*`,
`deciding-run.stdout` into it (`:33-52`). Contrast with the lane/rev handling that is checked (`:15`, `:19-20`).

Exploit path (operator error, not an attacker): `deciding-run.sh $LANE $REV $FREEZE /home/vgpnk/Projects/shokunin/…` or
`… $LANE/..` writes the round's decisive receipts outside the lane's evidence tree, where the kill rule's "receipts-only
commit" and the census cannot see them; and a non-empty `OUT` (e.g. a seat's leftover `c1.stdout` probe) is silently
overwritten, so the receipt that the report quotes may be the deciding run's while the timestamp ordering is not provable
from the file.

Impact: scope escape is silent; the "empty directory" precondition the docstring promises is unenforced. The
one-invocation guard is intact (it keys on the start receipts, not on emptiness).

Smallest remediation: after `:22`, add
`case "$(realpath -m "$OUT")" in "$LANE"/.ufo/evidence/round-49/*) ;; *) echo DECIDING_REFUSED outdir-outside-lane; exit 3;; esac`
and refuse a non-empty `OUT` (`[ -z "$(ls -A "$OUT")" ] || exit 3`) — but note the script is frozen and pinned
(`freeze.json`), so a change here means a new freeze, which the contract's `amendments` rules would have to carry; the
minimal within-freeze fix is for the L1 to pass only `$LANE/.ufo/evidence/round-49/after` and to have the round report
state the `OUT` path in the receipt.

### F3 — the re-key script rewrites the 3.5 MB prior-round monitor ledger in place, with no atomic replace and no post-write assertion — MEDIUM (pattern; not realized this round)

Attack surface: `.ufo/evidence/round-49/c1/refresh.py` is the only writer of `.ufo/evidence/round-21/coldread/ledger.json`,
the file the unchanged round-21 monitor reads; it belongs to round 21 and holds 497 entries of prior rounds' evidence.

Evidence — `grep -n` in `runner-path-safety.txt`:

```
73:    ledger_path = os.path.join(LANE, LEDGER)
74:    ledger = json.load(open(ledger_path, encoding='utf-8'))
117:    with open(ledger_path, 'w', encoding='utf-8') as fh:
118:        fh.write(json.dumps(ledger, indent=1, ensure_ascii=True))
119:    with open(os.path.join(LANE, E, 'coldread/refresh-receipts.json'), 'w', …)
```

The whole file is re-serialized through a truncating `open(…, 'w')`. A crash, ENOSPC or a kill between `:117` and the end
of `:118` leaves a truncated ledger; there is no `os.replace` from a temp file, no pre-image copy, and no assertion that
the appended count is exactly `len(before)+7` or that the first `len(before)` entries are unchanged. `:119` then writes
the receipts after the ledger, so a failure there leaves new ledger entries with no receipt.

Realized state is clean — I verified it independently rather than taking the commit message's word
(`containment-and-integrity.txt` §2): `git diff --numstat` on the ledger is `253	0`, parsed entries go `497 → 504`, the
first 497 candidate entries compare equal to base after JSON parse, the four scalar fields (`carried_from`,
`provenance`, `round21_provenance`, `schema`) are equal, and the seven new entries carry no record-file input, no
`external` and no `live_lane_reads` (they are trace-bound through `.ufo/evidence/round-49/coldread/traces/section-<n>.json`).
So the ledger's append-only invariant held this time by luck of a successful write, not by construction.

Impact: one unhandled failure destroys 497 entries of prior-round evidence that no git object in this lane can rebuild
in place, and the frozen monitor would then credit 0 sections — a failure mode that looks like a claim failure, not like
an interrupted write.

Smallest remediation: `tmp = ledger_path + '.tmp'` with `json.dump(..., open(tmp,'w'))`, `os.replace(tmp, ledger_path)`,
after `assert len(ledger['entries']) == before + len(c1.TARGETS)` and `assert ledger['entries'][:before] == pre_entries`;
write `refresh-receipts.json` first, since it is the thing that proves the write happened.

### F4 — the two lane-mutating scripts trust their `argv[1]` as the lane; neither asserts it is the tameshi lane — LOW

Attack surface: `refresh.py` writes `$LANE/.ufo/evidence/round-21/coldread/ledger.json` plus two evidence files;
`apply-corrections.py` writes `$LANE/SKILL.md`.

Evidence (`runner-path-safety.txt`): `refresh.py:73-74,117-119` build every path from `LANE`; `apply-corrections.py:14`
`LANE = os.path.realpath(sys.argv[1])` with no identity check, and `:42` `open(path, 'w')` on `$LANE/SKILL.md`. The host
guard for this round says the process cwd is the fleet root, so a relative or wrong first argument is a live mistake
shape, not a hypothetical.

`apply-corrections.py` is otherwise fail-closed and I checked the order (`:21` read, validations at `:26`, `:28`, `:31`,
`:36`, single write at `:42`, then only a line-count re-check at `:41`): every correction is validated against a unique
occurrence inside a declared target section and a line-count-neutral old/new pair *before* the first byte is written, and
the file is written once. That is the right shape; what is missing is (a) the lane identity and (b) a post-write check
that only the seven target sections changed (e.g. compare `sectionize()` sha256 per heading against the pre-image).

Impact: a wrong-argument invocation either dies harmlessly (both scripts load
`$LANE/.ufo/evidence/round-49/c1/measure.py`, absent outside the lane) or, in a lane that happens to carry that tree,
edits another repo's record. `refresh.py` has the same shape and additionally writes.

Smallest remediation: one line in each, `assert os.path.basename(LANE) == 'tameshi-shokunin'`, and in
`apply-corrections.py` a post-write re-sectionize comparing the 57 non-target headings' sha256 to the pre-image.

### F5 — scratch paths are baked into committed traces and receipts as `cwd`/`root`/`PYTHONPYCACHEPREFIX`; credit does not resolve them — INFORMATIONAL

Evidence — `.ufo/evidence/round-49/coldread/traces/section-1.json:15,16,28`:

```
"cwd": "/fast/scratch/hyaku/tameshi-r49/refresh/lane"
"root": "/fast/scratch/hyaku/tameshi-r49/refresh/lane"
"PYTHONPYCACHEPREFIX": "/fast/scratch/hyaku/tameshi-r49/refresh/trace-inputs-run-fcrt4wv1/pycache"
```

and the same keys in `refresh-receipts.json:38,75,127,163,199,241,287`. This is not a violation of "a scratch path is
never citable evidence": the monitor's trace gate reads only the committed receipt's `schema`, `inputs`,
`live_lane_reads` and `external` (`.ufo/evidence/round-18/measure.py:406,408,418,423`; `root`/`cwd` are never opened),
so deleting the scratch clone — which the operator directive requires — cannot lapse the entry. What it does mean is
that the receipt is not re-executable from its recorded paths: after cleanup, `root` names a directory that never
existed again. Worth one sentence in the pilot/lesson so a future reader does not try to replay from `root`; not worth a
change to frozen code.

### F6 — panel containment and the deciding-run precondition are intact (positive check, no defect)

`.ufo/evidence/round-49/c2/` at the candidate contains exactly `measure.py` → `['.ufo/evidence/round-49/c2/measure.py']`;
`after/` is absent; no `c1.start`/`c2.start` exists anywhere under `.ufo/evidence/round-49/`
(`containment-and-integrity.txt` §3). So the panel is not revealed early and the one-invocation rule of
`deciding-run.sh:29` has not been consumed. No added file outside the three panel-naming control stdouts contains
mutant definitions (`grep -rl '"old":'` over round-49 evidence and waves returns only
`.ufo/evidence/round-49/c1/corrections.json`, which holds SKILL.md text corrections), and no file references the hidden
panel store (`.local/state`) — that string occurs only in the pre-existing `kaika-round-1` evidence, untouched by this
diff.

### F7 — residual risk the contract already declares: gate 0 binds control *order*, not control *bytes* — INFORMATIONAL

`deciding-run.sh:25-28` proves each control receipt exists at REV and that the last commit touching it descends from
FREEZE; it does not hash the receipt against what the L1 scored at freeze. `corpus/QUALITY.md:1453` states this
explicitly ("The criterion binds the order, not the values"), so this is declared, not smuggled. Recorded so the closure
does not read gate 0 as a bytes guarantee.

### F8 — `reads.json` covers the 90 frozen pointers plus 4 new ones, but 37 of the 90 differ from the base `raw` (consumer hazard) — INFORMATIONAL

`containment-and-integrity.txt` §4: `94` rows, `94` distinct `(heading, ordinal)` keys, all `90` frozen
`(heading, ordinal)` pairs covered, `4` extra keys — recipe ordinals `34,35`, restore `10`, map `17` (new pointers
introduced by the corrections); verdicts `{holds: 91, absent: 3}`; 20 distinct readers; row keys exactly the contract's
schema `{heading, ordinal, raw, file, ranges, verdict, excerpt, reader, fleet_commit?, base_verdict?, note?}`. A join on
`(heading, ordinal)` is complete; a join on `raw` silently loses 37 pointers, because correction changed the pointer
text. Not a defect (the contract says rows are re-derived at the corrected text) — a hazard for any later consumer that
joins to `control/c1-pointers-at-base-8ca67421.json` on `raw`. Cite it in the lesson's pointer-join line.

## Summary

- Scope holds: 461 changed paths, all lane-relative (454 A / 7 M); no symlink or gitlink added; all 401 wave paths
  attribute to a declared seat or the wave harness; the only non-round-49 file touched is the re-keyed round-21 ledger.
- `tools/` adds exactly `tools/pbt-staged-id.py`; all 13 `freeze.json` pins are byte-equal at freeze and candidate,
  including `tools/staged-id-guard.py` (`03a796c5…c2dca8`).
- One bound is exceeded literally: `T49ScribeRows.src/smallbone.pdf`, 1,269,821 B in `.ufo/waves/` (base had no
  >1 MiB file under `.ufo/waves/`); no monitor covers size (F1).
- Secrets: zero hits over 454 added files, every `+` diff line, and the added PDFs/PNGs. No new `/tmp` citation
  (`/tmp/tameshi-r49` count 0; 0 in the appended ledger lines).
- Safety defects are in the *runners*, not the candidate content: `deciding-run.sh` never enforces its own
  "OUTDIR inside LANE, empty" contract (F2), and `refresh.py` truncating-rewrites the 3.5 MB prior-round ledger with no
  atomic replace or post-write assertion (F3, invariant verified clean this round: 253/0, 497→504, prefix-equal).
- Panel containment and the one-invocation precondition are intact: `c2/` holds only `measure.py`, no `after/`, no
  `c1.start`/`c2.start`; gate 0's order-not-bytes scope is declared (QUALITY 99) and correctly described (F6, F7).
