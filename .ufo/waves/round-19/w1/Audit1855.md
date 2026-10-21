# Audit1855 — round 19 w1 reviewer (advisory)

Seat `TameshiR19-2.Audit1855`, reviewer. Opened 2026-10-21. These findings are advisory only. They do not close or admit anything.

**Scope.**
- `.ufo/evidence/round-18/final/audit-1855.{stdout,stderr}`
- `.ufo/evidence/round-18/coldread/traces/L1/audit-1855.json`
- The ledger entry that names this trace: `.ufo/evidence/round-18/coldread/ledger.json` `entries[155]`. Its seat block is `.ufo/waves/round-18/w3/L1Residual.md:678-729`.

To answer the C1 question I also read:
- pinned git objects for this entry's 16 recorded inputs;
- the `measure.py` docstring and credit code (`measure.py` is one of this entry's inputs);
- the C1 artifacts that re-key or re-measure this one bucket (1855).

**Revisions.**
- `read_rev`: `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`.
- Introducing commit: `a134a09d15c23b2c2f0373482bb36c292c175ea5`, whose only parent is a9c94c5.
- Also checked: `a85f710`, `4b7c682`, round-19 baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`, `78b99dd`, `21e7932`, `7af123b`, `c5730cc` and `88c8073`.
- HEAD (= `refs/heads/master`) was `21e7932` when the audit started and `cecaefe73482504a814064dd7b2242c8c0b8ad50` when it ended. Every statement below names the revision it was observed at.

**Method.**
- Read-only git object commands only: `ls-tree`, `cat-file blob`, `show REV:path`, `log`, `diff --name-status|-U0`, `merge-base --is-ancestor`. GIT_* variables were removed; none were set.
- sha256 computed with Python stdlib.
- The receipt argv was **not executed**. No measure, assemble, trace or selftest run. No jj command, no git write, no install.
- Code text is in §7.

## 1. Verdict (advisory)

The receipt pair and trace are internally consistent and bound to their revision:
- The stdout can be rebuilt byte-for-byte from the a9c94c5 blobs.
- The 15 credited input digests agree across trace, ledger, stdout and seat block.
- None of the three files changed at any checked revision through `cecaefe`.

Two things are **not** established:
- The receipt's printed `VERIFIED` summary does not follow from its argv (F1).
- No record binds the stdout or stderr by digest (F2).

Effect of C1 on this evidence:
- C1 did not falsify it, and none of its inputs drifted.
- C1 commit `88c8073` edited text inside this bucket, so audit-1855 no longer matches the current section (F3). Current credit rests on the successor entry 171 (`source-1855`).
- C1's defect-5 repair receipt at `4b7c682` *depends on* audit-1855 for this bucket. It does not invalidate it.

## 2. Findings by severity

### F1 — Low (historical, no numeric effect): the VERIFIED line is a literal, not a derived result

**What the receipt prints.** `audit-1855.stdout:72` (committed a134a09, 2026-10-20) reads: "VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision".

In trace `argv[29]` (the `python3 -c` program), that line is an unconditional `print`. It runs after nine predicates:
- registry `held==total==31`
- probes `open=0 closed=11 total=11`
- regression `cases=8 passed=8`
- historical `cases=4 passed=4`
- case7 and case8 `killed=5 survived=5 inconclusive=0 kill-rate=50%`
- disposition `status=='clean'`
- before `status=='failed'`
- repeat contains `controls_match`

**What the argv never does.**
- It compares no instrument blob across revisions.
- It never parses `checks.json` or `context.stdout`; it only hashes them.
- It checks no receipt's argv, exit code or revision.

**Failing criterion (observed).** At a9c94c5, `final/checks.json` key `bash-witness-selftest` records argv `python3 tools/bash-witness-study.py --selftest`, `exit: 64`, and `stdout_sha256` equal to the empty digest. This is routed defect #4: "`final/checks.json` records `bash-witness-selftest` argv exit 64 with an empty stdout" (`corpus/lessons/round-18-verifier-spotcheck.md:196-197`). audit-1855 hashed this exact file (`fed3c8e6…671d`) and still printed VERIFIED. So it could not catch failures in the bundle it names.

**Second clause, checked independently (outside the argv).**
- `git diff --name-status 921ef80..a9c94c5` lists only receipt and trace additions, plus `M SKILL.md` and `M corpus/lessons/round-18.md`.
- `git diff --name-status 5923d89..a9c94c5` lists only receipt additions.
- No `tools/` or `.ufo/evidence/round-18/*.py` path appears in either.
- So the clause agrees with tree history for the two revisions the seat names (L1Residual.md:686). The other ancestor run revisions are **UNKNOWN**; I did not open them.

**Impact.** No count changes. `measure.py` reads ledger fields and trace receipts, never the stdout. The seat disclosed this: "L1 residual verification is not a blind non-author cold read." (L1Residual.md:686, 2026-10-20).

**Route.** An optional, dated, named, append-only erratum. This is not one of the five routed defects, so it stays an explicitly open residual and does not widen C1.

### F2 — Low: stdout and stderr have no digest binding

- No lane file cites the stdout sha256 `bc7e9336baa27ce54cdcdd9e803bfe20b68e42ec1f738eb2706f44a393211a30` (7000 B) or the trace sha256 `41ac0ba8…`. I ran this one grep over the worktree at HEAD, with gitignore off.
- Schema `tameshi-trace-inputs-v1` has no stdout or stderr field.
- The ledger entry and the seat block name only the trace path.
- The binding today is a shared basename, the same introducing commit a134a09, and git blob identity: stdout `6479677d9ec3`, stderr `e69de29bb2d1` (the empty blob), trace `22a2340e180e`.
- Newer receipts already have this binding. `.ufo/evidence/round-19/coldread/refresh-recipe-receipt.json` binds stdout, stderr and trace digests, and all three matched their files at cecaefe. Advisory only.

### F3 — Info / C1 boundary: commit 88c8073 edited inside this bucket

**The edit.** `git diff -U0 c5730cc 88c8073 -- SKILL.md` gives `@@ -1890 +1890 @@`.
- Old line, which audit-1855 printed at stdout:37: "then `python3 .ufo/evidence/round-18/measure.py --rev REV`".
- New line: "then `python3 .ufo/evidence/round-19/coldread/measure.py --rev REV` → …".

**Effect on the section key.** Using the `measure.py:18-22` sectionizer rule, the section sha is `c6edc5f0…a493` from a9c94c5 through c5730cc. It becomes `43a041e7…6d77` at 88c8073 and cecaefe.

**Ledger state at cecaefe** (`.ufo/evidence/round-19/coldread/ledger.json`):
- Entry 155 is carried over unchanged (JSON-equal) but no longer matches any section.
- Entry 171 is the only entry that matches the new sha. Its seat is "L1 TameshiR19-2 author source re-anchor", its `read_rev` is 88c8073, and its trace is `.ufo/evidence/round-19/coldread/traces/L1/source-1855.json`.
- No entry pairs the new sha with audit-1855, so old credit was not reattached to new text.

**Scope.** This recipe migration is not one of the five routed defects. It is round-19 instrument plumbing (SKILL.md:1936 row, added at 7af123b).

**Gap.** No committed monitor exists at 88c8073 or cecaefe. No receipt I read measures this bucket's credit at HEAD, and I ran nothing.

## 3. Facts established (observations unless marked)

| Question | Source / command | Observed |
|---|---|---|
| stdout hash | sha256 of the worktree file; `git show REV:path` at a134a09, a85f710, 4b7c682, 7243e7f, 78b99dd, 21e7932, c5730cc, cecaefe; `git diff --stat HEAD` | `bc7e9336…1a30`, 7000 B, identical at every listed revision, no worktree diff. a134a09 is the only master commit that touches it. |
| stdout content | rebuilt by applying the argv's print logic to the a9c94c5 blobs; the argv itself was not run | Byte-identical (same sha, 7000 B). All nine predicates hold on the a9c94c5 blobs, so exit 0, the empty stderr and the final line are consistent with each other. |
| stderr | sha256 | 0 B, `e3b0c442…b855` (git empty blob `e69de29b`), unchanged through cecaefe. |
| trace ↔ ledger | entries whose `traces` name `traces/L1/audit-1855.json` | Exactly one, `entries[155]`: lines 1855–1896, class instruction, verdict gap-minor, blocking 0, wrong 0, minor 1, `commands_executed_count` 1. Its `read_rev` equals the trace `rev`, a9c94c5. |
| input agreement | trace `inputs` (16), ledger (15), stdout OPEN lines (15), seat-block `inputs` and `opened` | Trace minus `SKILL.md` equals the ledger set, with 0 digest mismatches. `SKILL.md` is in `inputs_dropped` and in `IGNORED_INPUTS` (`measure.py:135`). The OPEN paths, the argv spec paths and the seat `opened` list are the same list in the same order. Seat `inputs` equals the ledger. The trace's `SKILL.md` digest `1334c512…` equals both the ledger `skill_sha256` and `_meta.expect_skill_sha`. |
| inputs at the read rev | `git ls-tree` + `cat-file blob` at a9c94c5 | All 16 are regular blobs (100644/100755). Their sha256 values and byte counts equal the trace and the stdout OPEN lines. |
| revision bracket | `a9c94c5^` = `5923d89`; `a134a09^` = a9c94c5 | `final/registry-branch-aligned.stdout` is absent at 5923d89 and was first added on master by a9c94c5. So the recorded input set first exists at a9c94c5, and the trace was committed in a9c94c5's only child. **Limit:** a134a09…78b99dd hold identical inputs, so the inputs alone cannot tell those revisions apart. The `rev` field is the tool's own report: consistent and bracketed, but not proven unique. |
| commit-together rule (recipe step 4) | `git log refs/heads/master -- <paths>` | The trace, stdout, stderr and the first ledger version all land in a134a09. No recorded input changed between a9c94c5 and a134a09. Entry 155 is JSON-identical in the round-18 ledger at every revision from a134a09 to cecaefe. |
| section range | SKILL.md at a9c94c5, lines 1855–1897 | The argv printed 1855–1895; the ledger says 1896. Line 1896 is blank and line 1897 is `### Round-17 gate/probe registry — input-keyed credit`. The ledger sha `c6edc5f0…` equals `'\n'.join` of lines 1855–1895, which follows the `measure.py:18-22` rule. Every hashed byte was printed. Not a defect. |
| sandbox facts | trace fields | `root` = `cwd` = clone `/tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin`. `untracked`, `external` and `live_lane_reads` are all `{}`; `dropped_home_count` is 0. The command ran with `--unshare-net` and `env -i`. |
| sole credit basis | ledger entries with this heading: 56 (CR57), 66 (RR7), 113 (CR48, wrong-expectation), 155 | At a85f710, 4b7c682 and c5730cc, only entry 155 carries the section sha `c6edc5f0`. Entries 56, 66 and 113 hash older section bytes, so they neither credit nor veto. Sections are matched by sha (`measure.py:602-612`), and "a section is covered iff at least one entry credits AND no veto-eligible entry exists whose inputs still all verify at REV" (`measure.py:72-74`). |
| command completeness | argv compared with the section's four-step recipe | The argv ran none of the recipe commands (clone, trace-inputs, assemble, measure). It is a receipt-audit read. It shows what this one command read, not that the declared commands ran. This matches the limit stated in the section itself (stdout:47-56). |

**Not established by this receipt:**
- when it ran;
- which interpreter and version ran it (`python3` was resolved through a PATH that includes user shims; not recorded);
- whether `checks.json` and `context.stdout` were valid (F1);
- whether instruments were identical across revisions (F1);
- any digest record for the stdout (F2).

## 4. Could C1 repairs invalidate this historical evidence?

**Falsify: no.** The facts concern immutable a9c94c5 blobs, and the receipt blobs are unchanged at every checked revision through cecaefe.

**Drift: no, as of cecaefe.** `git log 7243e7f..cecaefe` touches none of the 15 credited inputs and none of the three receipt files. `SKILL.md` is an ignored input. By routed defect:

- **#1** `guard-kill-closure.md`: not an input.
- **#2** `mutation-case-kumitate-sources-check.md`: not an input of entry 155. It is an input of the 1905 entry, which I saw in the same read window.
- **#3** `corpus/lessons/round-18.md`: not an input.
- **#4** `final/checks.json`: **is** an input. C1 kept it byte-frozen and put the repair in new `.ufo/evidence/round-19/bash-witness-selftest{,-complete}.*` receipts. That approach does not invalidate this entry.
- **#5**: C1 added `.ufo/evidence/round-19/round18-final-measure.{json,stdout}` (argv `measure.py --rev 4b7c682 --explain`, exit 0, stdout digest verified). It reports this bucket `credited`, `vetoed: false`. Entry 155 is the only entry matching the section at 4b7c682. **So C1's defect-5 closure (60/60, calibration 8 at 4b7c682) relies on audit-1855 rather than invalidating it.**

**De-key: yes, by `88c8073` (F3).** audit-1855 now credits only revisions where the section sha is `c6edc5f0` (a9c94c5 through c5730cc). The monitors at 21e7932 and c5730cc show this bucket credited. From 88c8073 on, the current support is entry 171.

**What would still invalidate it:**
- An in-place rewrite of any of the 15 inputs, especially `final/checks.json`. That drifts entry 155, and also entry 171, which has the identical input set. The bucket would then be uncovered at HEAD.
- Deleting or renaming `traces/L1/audit-1855.json` (`trace-missing`). That would also undermine the defect-5 receipt's claim if 4b7c682 were re-measured.
- Editing `final/audit-1855.*` in place. No gate would detect this (F2).

## 5. Incidental pointer (outside this item; pinned; may be superseded by later landed updates; not assessed)

Two monitors committed at cecaefe report a lower calibration than C1's stated 8:

| Monitor file (`.ufo/evidence/round-19/`) | Revision | `calibration_restraint_score` | `box3_full_page` | Sections covered |
|---|---|---|---|---|
| `current-ledger-monitor-21e7932.json` | 21e7932 | 6 | false | 49/60 |
| `current-ledger-monitor-c5730cc.json` | c5730cc | 6 | false | 59/60 |

Bucket 1855 is credited in both, so it is not the cause. L1 should confirm which strict receipt backs "calibration 8" at the delivered revision.

## 6. Residual risk and verification gaps

- **UNKNOWN:** this bucket's credit at 88c8073 and cecaefe. I ran nothing, and no monitor exists at either revision.
- Entry 171 / `source-1855` was checked only for binding:
  - its trace `rev` equals its `read_rev`, 88c8073;
  - its inputs equal the trace inputs minus SKILL.md, the same 15-path set as entry 155;
  - its manifest digests match the files;
  - its stdout ends "SOURCE_READ complete; no recipe argv executed; external observations not reverified".

  Whether it is semantically sound is for another seat.
- F1's instrument-identity check is at name-status level only, and only for 921ef80 and 5923d89.
- The F2 digest grep covered the lane worktree only. It did not cover fleet siblings or deleted history.
- The temporary clone and bwrap run cannot be observed again. The trace's `rev` remains the tool's own report: bracketed, but not proven unique.

## 7. Investigation code (read-only; condensed from what I ran)

```python
import os, subprocess, hashlib, json
L = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
git = lambda *a: subprocess.run(['git', '-C', L, *a], env=ENV, capture_output=True).stdout
def blobinfo(rev, p):                      # mode, type, sha256, bytes of REV:p
    t = git('ls-tree', rev, '--', p).decode()
    if not t: return None
    mode, typ, oid = t.split('\t')[0].split(); b = git('cat-file', 'blob', oid)
    return mode, typ, hashlib.sha256(b).hexdigest(), len(b)
trace = json.load(open(L + '/.ufo/evidence/round-18/coldread/traces/L1/audit-1855.json'))
# 1) drift: each recorded input is a 100644/100755 blob with the recorded sha at each REV
#    drift = {rev: [p for p, s in trace['inputs'].items() if (blobinfo(rev, p) or (0, 0, None))[2] != s]}
# 2) stdout rebuilt from a9c94c5 blobs with the argv's print logic (argv never executed)
R = 'a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4'
spec = json.loads(trace['argv'][-1]); sl = git('show', R + ':SKILL.md').decode().splitlines()
out = ['SECTION %d %d' % (spec['start'], spec['end']), '\n'.join(sl[spec['start']-1:spec['end']])]
for p in spec['paths']:
    raw = git('show', R + ':' + p)
    out.append('OPEN %s sha256=%s bytes=%d' % (p, hashlib.sha256(raw).hexdigest(), len(raw)))
    if p.startswith('corpus/knowledge/'): out += [raw.decode().splitlines()[0], 'TAIL ' + raw.decode()[-700:]]
out.append('VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision')
assert '\n'.join(out) + '\n' == open(L + '/.ufo/evidence/round-18/final/audit-1855.stdout').read()
# the nine predicates were evaluated the same way on the R blobs (all True)
# 3) section sha per measure.py:18-22 (trailing blank lines stripped, '\n'-joined, no trailing newline)
assert hashlib.sha256('\n'.join(sl[1854:1895]).encode()).hexdigest().startswith('c6edc5f0')
```

Installs: none. Writes: this file only.
