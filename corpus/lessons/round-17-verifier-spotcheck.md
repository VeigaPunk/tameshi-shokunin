author: hyaku closure (non-author integrator, @m_opus)

# Round 17 — non-author verifier spot-check (tameshi)

**Outcome: status `ok`, admitted `true`.** Both declared claims verify at
`30b0ca84b85e33948ba2960584dea1b36c1e8779`; no owned axis is harmed.
This admits the bounded calibration and operability moves, not a claim that
all new tooling is complete, all knowledge sentences are correct, or promotion
is earned. I grade **expansion unchanged, quality unchanged, discernment
improved**, rather than accepting all three author-assessed trend improvements.
The false knowledge-entry exit sentence and the G5 overclaim remain routed.

This is an independent closure, not lane authorship. Baseline:
`98bea7da5801f4bc58e4187690ee1687c8a5061f`. Report:
`.ufo/reports/round-17/tameshi.md`, fleet commit
`41a3a0a26512f69f637e2720b250f53382b4ff6f`.
I executed **no lane-owned gate, selftest, monitor, or measurement tool**.
Counts below were independently reconstructed from revision-pinned Git blobs;
gate verdicts and selftest tallies were evidence-verified, not re-executed.
Five read-only closure-dispatched reviewer seats assisted; their findings were
judged here, not treated as a substitute for integrator judgment.

Driver digest copied from the mutable watchdog log:
- `2026-10-20T12:07:33-03:00 launch tameshi round=17 pgid=4069358 driver=hyaku-inline attempt=1`
- `2026-10-20T16:03:32-03:00 complete tameshi round=17; hyaku-inline attempt=1`

## 1. Step-1 conformance

All lane commands below use
`L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`;
`F=/home/vgpnk/Projects/shokunin` denotes the fleet root.

| Check | Command / source | Observed |
|---|---|---|
| Report landed by lane, after lane work | `git -C "$F" log --format='%an <%ae> %H %cI' -- .ufo/reports/round-17/tameshi.md` | `tameshi-shokunin <tameshi@shokunin.local> 41a3a0a… 2026-10-20T16:03:04-03:00`; final lane commit was 16:01:32. Pass. |
| Substantive report / SHONEN | Report §§Work performed, Landed changes, SHONEN | Two checkable claims, six lane commits, LOG entry, four `[~]` box lines. Real report, not a marker. |
| Commit existence and ancestry | `git -C "$L" cat-file -e HASH^{commit}`; `git -C "$L" merge-base --is-ancestor HASH refs/heads/master` | Pass for 98bea7d, 2a22ade, eb7838b, fad9e95, 0ff2734, e3827ee, 30b0ca8, 4acc607, e69b488, 09ee1d0. Ancestry was tested against the branch ref, never detached HEAD or an upstream shorthand. |
| Lane identities | `git -C "$L" log --format='%h %an <%ae> %cI' 98bea7d..refs/heads/master` | Six commits, all `tameshi-shokunin <tameshi@shokunin.local>`. |
| Pushed / no round leftovers | `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state "$L"`; `git -C "$L" status --porcelain` | Before closure: local=remote=30b0ca84…, ahead=0, behind=0, head=detached, tracked=0, untracked=0; porcelain empty. |
| Actual remote | `git -C "$L" ls-remote origin refs/heads/master` | `30b0ca84b85e33948ba2960584dea1b36c1e8779`. |
| Prompt durability / fidelity | Fleet prompt history; compare canonical and fleet templates; Python literal membership test for every non-placeholder template line | Prompt committed as 36bcdad by tameshi at 12:07:32; templates byte-identical; **105/105** static lines present, plus hyaku §6. |
| Wave accounting | Parse `w1/swarm-registry.json` and `w2/swarm-registry.json` with Python JSON / Counter | 67 and 99 seats; role counts match report. W3 residual has eight seats as reported. |
| Dead seats | Compare W2 registry member names with committed `<name>.md` reports | Exactly seven absent: RegistryProvenance, SentinelLanded, SentinelTraceEscape, CriticC1, CriticC2, CriticNoHarm, CriticSeparability. Registry has one recorded identity each; consistent with the disclosed non-respawns. No claim is admitted on a missing seat's opinion. |

Status-neutral conformance defects are recorded below: the disclosed unsafe
selftest/live-Git incident and out-of-helper repair; corpus correction mechanics;
and minor citation/receipt wording. They do not make this a failed marker.
No closure seat installed or updated a tool. The report discloses the lane seat's
`ruff 0.17.1` and `vulture 2.16` installs via `uv tool install` for dead-code review.

## 2. Incident: HEAD/index restoration and preservation

I independently inspected both reflogs, object integrity, refs, index and worktree.

| Check | Command | Observed |
|---|---|---|
| HEAD incident / restoration | `git -C "$L" reflog -n 40 --date=iso HEAD` | At 12:29:33 HEAD moved through f8832ef → 0559c60 → e16adb7. At **12:36:43** it returned to 98bea7d with message `round-17 L1 repair: restore HEAD after R04 seat fixture commits (GIT_DIR leak)`. Subsequent six round commits are helper `export from jj` entries. |
| Branch never moved into fixtures | `git -C "$L" reflog --date=iso refs/heads/master -n 10` | Master remained 98bea7d throughout the incident; next move is 2a22ade at 12:54:21. |
| Fixture objects not landed | `git cat-file -t`, `git log -1 --format=…`, `git branch -a --contains`, and `git merge-base --is-ancestor` for each fixture hash | All three objects exist, author `tameshi <tameshi@selftest>`, one linear fixture chain rooted at 98bea7d. None is an ancestor of master; no branch contains them. Final remote master is the legitimate round chain. |
| Current index and worktree | `git -C "$L" diff --cached --quiet HEAD`; `git -C "$L" diff --quiet` | Both exit 0: index=HEAD, worktree=index. HEAD and master both resolve to 30b0ca8 before closure. |
| Object database | `git -C "$L" fsck --full --no-dangling` | Exit 0, no output. No missing/corrupt object finding. |
| No intervening jj snapshot | `find "$L/.jj/repo/op_store" -type f -newermt '2026-10-20 12:25' ! -newermt '2026-10-20 12:40' …` | No operation-store files in that window. Nearest groups are 12:06:01–03 and 12:54:20–22. Consistent with jj never importing the fixture HEAD before restoration. |
| Tracked-file preservation | `git -C "$L" diff --diff-filter=D --name-only 98bea7d 30b0ca8`; reopen W1 R04ReviewContractB §§0,6 and N01TraceGitSafety §F1 | No tracked files deleted in the landed round. R04 records comparison against `git archive master`: all **1296** baseline tracked files byte-identical except named intended wave edits; post-repair index again had 1296 entries and only intended changes. |

**Judgment:** current branch, remote, index and working tree integrity hold.
The retained contemporary archive comparison supports preservation of worktree
bytes; it is evidence-verified, not a historical comparison I can retroactively
re-execute. My current Git/object checks corroborate it. No lost bytes were found.
The fixture commits replaced the index/tree of detached HEAD, not the lane's
on-disk worktree or master history. Their unreachable objects are not landed work.

The unsafe seat invocation violated the sandbox/no-live-writes contract. The
L1's disclosed `read-tree` / `update-ref` repair also bypassed the helper-only
writer rule. Record both as conformance defects, not normal sanctioned workflow.
The runner's scrub/identity fixes and canary-mutant receipts address the cause;
they do not erase the incident or prove every older tool scrubbed.

## 3. C1 — calibration 6 → 8: verified, re-measured

I read the committed rule but did not execute `measure.py`. My own Python cells
used `subprocess` calls to `git show REV:PATH`, SHA-256, JSON parsing and
`git ls-tree -r REV`. Section hashing strips trailing blank lines and joins with
LF, no final LF. The implementation uses preamble plus `#`–`###` headings outside
backtick fences. An independent 1–6/backtick/tilde-fence sectionizer agrees:
there are no deeper headings or tilde fences in either page being measured.

The independent Python-cell operations are reproduced below as a standalone
read-only count over these committed ledger bytes (no lane module import):

```python
import functools, hashlib, json, os, re, subprocess
L = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
LP = '.ufo/evidence/round-17/coldread/ledger.json'
ignored = {'SKILL.md', LP}
regular = {'100644', '100755'}
sha = lambda raw: hashlib.sha256(raw).hexdigest()

@functools.lru_cache(None)
def blob(rev, path):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None

def sections(raw):
    lines = raw.decode().splitlines()
    starts, fence = [], False
    for n, line in enumerate(lines):
        if line.strip().startswith('```'):
            fence = not fence
            continue
        if not fence and re.match(r'^#{1,3}(?:\s|$)', line):
            starts.append(n)
    if not starts or starts[0] != 0:
        starts.insert(0, 0)
    hashes = []
    for a, b in zip(starts, starts[1:] + [len(lines)]):
        body = lines[a:b]
        while body and not body[-1].strip():
            body.pop()
        hashes.append(sha('\n'.join(body).encode()))
    return hashes

for rev in ['98bea7d', 'e3827ee', '30b0ca8']:
    modes = {}
    for line in subprocess.check_output(
            ['git', '-C', L, 'ls-tree', '-r', rev]).decode().splitlines():
        meta, path = line.split('\t', 1)
        modes[path] = meta.split()[0]
    raw = blob(rev, LP)
    entries = json.loads(raw)['entries'] if raw else []
    passing, vetoes = set(), set()
    for entry in entries:
        inp = {p: h for p, h in entry.get('inputs', {}).items()
               if p not in ignored}
        stale = any(modes.get(p) not in regular or
                    sha(blob(rev, p) or b'') != h for p, h in inp.items())
        bad = (entry['verdict'] not in
               {'executed-ok', 'verified-record', 'gap-minor'} or
               entry['blocking_gaps'] != 0 or entry['wrong_expectations'] != 0)
        if bad and not stale:
            vetoes.add(entry['sha256'])
        accepted = {'instruction': {'executed-ok', 'gap-minor'},
                    'record': {'verified-record', 'gap-minor'}}
        valid = (not bad and bool(inp) and not stale and
                 entry['verdict'] in accepted.get(entry['class'], set()) and
                 entry['commands_executed_count'] > 0 and
                 bool(re.fullmatch('[0-9a-f]{40}', entry['read_rev'])) and
                 bool(entry.get('traces')))
        for path in entry.get('traces', []):
            if modes.get(path) not in regular:
                valid = False
                continue
            receipt = json.loads(blob(rev, path))
            valid &= receipt['schema'] == 'tameshi-trace-inputs-v1'
            valid &= all(p in ignored or inp.get(p) == h
                         for p, h in receipt['inputs'].items())
            reads = {**receipt.get('external', {}),
                     **receipt.get('live_lane_reads', {})}
            for p, h in reads.items():
                if p.startswith(L + '/'):
                    rel = os.path.relpath(os.path.realpath(p), L)
                    if rel != '.git' and not rel.startswith('.git/'):
                        valid &= (modes.get(rel) in regular and
                                  sha(blob(rev, rel) or b'') == h)
        if valid:
            passing.add(entry['sha256'])
    hashes = sections(blob(rev, 'SKILL.md'))
    covered = sum(h in passing and h not in vetoes for h in hashes)
    print(rev, covered, '/', len(hashes), 'ledger_present', raw is not None)
```

| Revision | Page SHA-256 | Buckets credited / total | Full page | Restraint |
|---|---|---:|---|---:|
| 98bea7d | 906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397 | **0/54** | false | **6** |
| e3827ee | de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc | **58/58** | true | **8** |
| 30b0ca8 | same as e3827ee | **58/58** | true | **8** |

Important baseline qualification: at 98bea7d the **round-17 default ledger is
absent**. Its 0/54 is `no-ledger:54`, not 54 failed reads and not a rerun of the
old round-16 ledger. This matches `c1-measure-98bea7d.json`: overrides false,
ledger_committed false. The final receipt is strict/no-override with a committed
ledger. The causal proof of the new rule is the separate real-byte red-before,
not simply the missing-ledger baseline.

At each final revision my reconstruction found **68 entries, 58 passing and 10
nonpassing** (five findings, five input-drift cases). The five nonstale failure
veto hashes match no current bucket. Passing entries involve **287 unique
recorded input paths and 626 unique committed trace receipts**; **92** live-lane
receipt records were checked against the published binding rule. No credited
input occurs among the eight paths changed from e3827ee to 30b0ca8. The changed
LOG/SCORECARD inputs occur only in noncredited older entries.

All four SHONEN marks are `[~]`. The rubric gives two points each for restrained
boxes 1/2/4, plus two for box 3 only with its round-17 ledger link and full-page
credit: 6 → 8. This is not four independent promotion checks.

### Real-byte input-drift red-before

Commands I ran: `git -C "$L" show REV:tools/mutate-and-run.sh` hashed with Python
`hashlib.sha256`; parse the three committed `redbefore/measure-REV.json` files
and `redbefore/legacy-r14-inputs.json`.

| Revision | Runner SHA | Round-14 bucket receipt |
|---|---|---|
| e69b488 | 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5 | credited |
| 09ee1d0 | 0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa | `input-drift:tools/mutate-and-run.sh` |
| 98bea7d | same as 09ee1d0 | same input-drift finding |

The overlay records the e69b488 digest, and the retained 19-input replay binds
that demonstration to the earlier bytes. All three demonstration receipts say
overrides_used=true; they are not substituted for the strict final score.

### Fidelity sample

Closure reviewer C1Rederive compared CR01, CR13, CR48 and W3 RR7 reports, ledger
entries and receipts; I also opened their actual receipt argv values.
CR01: 6 commands/6 receipts align, verified-record, zero wrong expectations.
CR13: 9/9 align, one wrong expectation, old noncurrent section hash; empty trace
input maps do not credit this failed entry. CR48: 10 report commands and four
ledger traces; all four traces correspond to the report's explicitly traced
invocations, including live v2 disposition exit 0, with no unrelated trace.
Its executed-ok/four-minor-gap report is documentedly normalized to gap-minor.
RR7: 23 report commands/23 receipt argv align, six recorded input pins agree;
its no-ledger observation was at the earlier read rev 0ff2734, not the later
committed-ledger measurement. No sample exposed a false credited read.

**Bound:** the general absence of argv-to-required-command enforcement is real
(§5 G5). The new knowledge entry itself disclaims skipped commands and completeness.
Thus 58/58 verifies the stated input-keyed evidence rule and sampled fidelity,
not a mechanical proof that every command an agent ought to run was executed.

## 4. C2 — operability restored plus entry-command monitor: verified

I independently parsed each committed registry JSON and recounted active rows:
`sum(row['held'] for row in rows if row['status']=='active')` and the denominator,
then compared `got`, `expect`, revision and registry digest. These are **counts
over committed gate evidence**, not fresh executions of the gates.

| Receipt at 30b0ca8 | Measured rev | Independently counted active held / total | Exit | Superseded |
|---|---|---:|---:|---:|
| c2-before-98bea7da5801f4bc58e4187690ee1687c8a5061f.json | 98bea7d | **22/23** | 1 | 1 |
| c2-after-eb7838b.json | eb7838b | **23/23** | 0 | 1 |
| c2-after-e3827ee.json | e3827ee | **23/23** | 0 | 1 |
| registry-full-e3827ee.json | e3827ee | **28/28** | 0 | 1 |

Registry SHA-256 in all four receipts equals my hash of committed
`tools/registry.json`:
`98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630`.
There are 29 rows, 28 active and one superseded. Baseline selection includes
23 active plus the superseded row. Only `evidence-disposition-round17` differs
at baseline (expected 0, got 2: its new manifest is absent there). The older
round-14 command **still runs and still returns 2**, expected 0; it is explicitly
superseded, not repaired in place or silently removed from the report.
The first build's selftest failure at 2a22ade (22/23, full 27/28) is retained;
eb7838b fixes its missing hermetic fixture identity before the claimed green.

C2Evidence checked five source rows against `98bea7d:SKILL.md:1503-1504`
(three repeat-control rows and two bash-witness rows): commands and admitted
exit expectations match. The current v2 entry/exit map is in SKILL.md:1850-1853.

### OP1 historical-input integrity

My `git show 4acc607:PATH` SHA-256 results:
- runner: `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`;
- pin-disposition: `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`.

Both equal the round-13 expected-input pins. Both final v2 manifests waive
exactly these two moved instruments at ancestor
`4acc607dfd79f19d508bd50cdd06b77269fccd1d`. Other expected input digests remain
live-checked (`tools/evidence-disposition.py:1493-1544`).
`git diff --stat 98bea7d 30b0ca8 -- .ufo/evidence/round-13 .ufo/evidence/round-14`
is empty: historical receipts/manifests were not rewritten.

Committed evidence:
- `op1-redbefore-98bea7d.txt`: exit **2**, expected_input_digest_mismatch;
- `op1-green-dispositions-before-2a22ade.txt`: semantic exit **1**, producer_before;
- `op1-green-dispositions-2a22ade.txt`: **clean exit 0**, 12 expected,
  11 effective + one superseded, 11 passed, zero findings;
- W2 TamperV2Matrix: 17 required flips exit 2 with named findings; restored
  runs clean; `ROWS=34 MISMATCHES=0 FINAL_EXIT=0` at eb7838b.

The two historical reads preserve the meaning of retained expectation
reconciliation, not validation of the current runner's behavior. Historical
waivers are disclosed. Committed edits to a waived tool are deliberately
accepted; coordinated rewrites of unanchored local manifest chains are not a
cryptographic adversary guarantee. G2/G3 still use HEAD rather than the branch
tip; this is latent jj correctness debt. At this closure HEAD=master=30b0ca8,
so it does not defeat the measured result.

`git diff --stat eb7838b 30b0ca8 -- tools/ '.ufo/evidence/round-17/dispositions*.json'`
is empty. e3827ee→30b0ca8 changes only receipts, LOG and SCORECARD, not relevant
registry/tool/manifest inputs. The evidence therefore transfers to the named
final tip without pretending a new gate execution occurred there.

### Gate standard: two evidences and revision

Final `registry-full-e3827ee.json` records exit 0 and the following tallies;
C2Evidence independently hashed the measured files at e3827ee:

| Instrument | Committed selftest tally | Measured file SHA prefix |
|---|---|---|
| evidence-disposition | 56/56 | f8f05c7a |
| registry-check | 34 cases | 0bf9d1d2 |
| mutate-and-run | 95/95 | fb6d86d5 |
| pin-disposition | 19/19 | 331529ea |
| round-17 measure | 94/94 | d25d3d04 |
| trace-inputs | 27/27 | 521be955 |

These are paired with the frozen before/after and tip registry receipts above.
W2 NoHarmSelftests at eb7838b records 16/16 entry points green and no baseline
case deletions: runner 83→95, disposition 34→56, pin 18→19; regression seven
cases unchanged. Its earlier measure tally is 89, not the final 94; those are
versioned receipts, not interchangeable counts. Final full registry receipts
cover the later instrument bytes. No sibling gate was executed by closure.

## 5. Discernment spot-check

Sample from `corpus/lessons/round-17.md` §Gate; source paths below are committed
under this lane, not ephemeral scratch locations.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| G2 guarded two-input historical waiver | admit | v2 manifests; expected.json pins; W1 X01DispositionV2, K03HistoricalInputsTamper:58-85; W2 RerunOP1 / TamperV2Matrix; final guard code | agree, bounded | Pins and ancestry hold; waiver is necessary/scoped, other inputs remain live-checked; retained clean/fail/tamper evidence supports restored capability. HEAD-vs-branch debt is not hidden. |
| G5 input-keyed credit, claiming K02 holes 1–4 closed | admit | W1 K02InputCreditHoles:43-47; W1 R05; W2 LessonReview; final measure:368-424,508-521; assemble:439-496,589-610 | **disagree with the breadth of the gate reason** | The zero-command class dodge is fixed, and current input-keyed counts verify. But the consumer does not bind receipt argv to report commands or extracted required page commands. K02's command-binding requirement is not fully closed. This is a source-based residual hole, not an observed unrelated trace in the sampled ledger. |
| G1 blanket four-input waiver | reject | W1 K03HistoricalInputsTamper:23-40; X01DispositionV2:160-164; final waiver guard:510-540 | agree | Blanket waiver hid a live edit in the contract model; actual landed code rejects an unneeded waiver. |
| G4 sha-only credit | reject | W1 M01ShaOnlyHole:14-30,68-102; real-byte drift receipts | agree | A behavior-changing return-2→0 mutant left the old detector at 54/54. Input-sensitive invalidation is warranted. |
| G7 key every seat-opened file, including page/ledger | reject | W1 K02InputCreditHoles, hole 7; final IGNORED_INPUTS | agree on substance | Avoids whole-page self-invalidation; section SHA already keys the page. Lesson's pointer to K02 hole 5 is wrong: that hole is about live-lane reads; the cited reasoning is hole 7. |

Two admits and three rejects sampled: four substantive agreements, one bounded
disagreement routed. The G5 disagreement does **not** falsify the independently
reconstructed C1 predicate or establish that a particular credited read is false.
It forbids calling the verifier a complete command-coverage proof.

### Newly written sources reopened

All seven URLs were independently reopened by closure reviewer SourcesReopen;
I also reopened S064 directly. Quotes from the lesson are verbatim modulo
wrapping, at their stated quoted locations, and within 25 words.

| Row | Source | Quote words | Result |
|---|---|---:|---|
| S058 | https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf — §4.2.2 p.79:14 | 21 | agree |
| S059 | https://bazel.build/remote/caching — Known issues | 24 | agree |
| S060 | https://man7.org/linux/man-pages/man1/strace.1.html — Filtering, `%file` | 12 | quote agrees; teaches/anchor needs qualification |
| S061 | https://docs.jj-vcs.dev/latest/git-compatibility/ — conversion recipe comment | 12 | quote agrees; separate paragraph-number citation debt remains |
| S062 | https://git-scm.com/docs/git-rev-parse — Options for Files, --show-toplevel | 23 | agree |
| S063 | https://git-scm.com/docs/git — GIT_CEILING_DIRECTORIES | 17 | agree |
| S064 | https://bazel.build/basics/hermeticity — Benefits | 19 | agree |

S064's checked quote: “The output of an action can be cached, and the action
need not be run again unless inputs change.” S060's quote is accurate, but
`%file` includes stat calls. The collector actually uses an explicit
open/exec/chdir/dup syscall list, not `%file`; its stat-only exclusion must be
anchored to that implementation rather than presented as a `%file` limit.
All new used-by paths exist at 30b0ca8; tiers/kinds fit their primary scope.

I ran the required census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`.
Exit **0**: only inherited W04 duplicate-URL warnings for S047/S048, then
`tameshi ok …/corpus/SOURCES.md`.

My own Python census parsed pipe-table rows from `git show REV:corpus/SOURCES.md`:

| Rev | Rows | Tier histogram | Status histogram |
|---|---:|---|---|
| 98bea7d | 55 | A47 B6 C2 | mined28 queued24 rejected3 |
| 30b0ca8 | 62 | A54 B6 C2 | mined35 queued24 rejected3 |

No prior registry row changed. Literal diff is **9 additions / 1 deletion**,
not a strictly pure append: the next-unused-ID footer changed S058→S065.
Keep that distinction in future report wording and appendix discipline.

## 6. Per-axis and trend verdicts

| Axis | Verdict | Evidence / bound |
|---|---|---|
| calibration | **improved** | C1 independently re-derived 6→8, with real-byte drift red-before and corrected SHONEN assertion. |
| operability | **improved** | C2 restored retained reconciliation at the tip; active baseline22/23→23/23 and new entry-command monitor. No old capability lost. |
| depth | unchanged | Independent header-case count `re.findall(r'^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+', runner, re.M)` gives seven at both revisions; regression evidence also seven. |
| coverage | unchanged | No frontier ground moved; F7 remains open. |
| freshness | unchanged | No successor sweep claimed; external line anchors remain citation debt. |
| adjacency | unchanged | Read-only sibling author/time-window scan found no tameshi-authored sibling commits; no inherited sibling pin was broken by the moved tools. |

The two claims are distinct and separable at their declared measurement
boundaries: C2's baseline monitor reads no round-17 ledger; C1 verifies
recorded input/section evidence rather than the registry's verdict count.
Calibration 6 was the lowest owned numeric axis after the r16 closure.

- **Expansion: unchanged.** A real new method entry and monitor were written,
  seven primary sources mined, and a coverage-map row added; no frontier ground
  moved. I withhold the report's unqualified new-knowledge admission credit while
  the new entry's exit-contract sentence remains false. This is a bounded new
  entry debt, not loss of previously held ground.
- **Quality: unchanged.** The old gate/recipe harm is genuinely repaired and
  seven sampled-page expectation classes were corrected. But the new knowledge
  entry fails its exit-contract recheck, so I do not award “improved” under
  LEARNING's no-admitted-entry-failing-recheck condition. The false sentence is
  explicitly, durably marked in lesson:93-95, SCORECARD end and report; it is
  therefore not an unacknowledged regression. There is no rule here requiring
  that all external named errata be ignored when interpreting “left unmarked.”
  The entry-local correction is still owed under the correction-sweep rule.
- **Discernment: improved.** Prior outside disagreements became evidence-backed
  QUALITY23–26 criteria and red-before/green-after repairs. QUALITY28 explicitly
  corrects the false breadth of27. The outside sample agrees on admits and
  rejects; G5's newly identified overclaim is preserved/routed rather than
  silently counted as resolved. No claim relies on a dead critic's approval.

The false sentence is `input-keyed-coldread-credit.md:75`: “2 rev/blob/ledger
missing.” A **missing default ledger** actually produces measured `no-ledger`
and exit0 (`measure.py:535-553,1545-1598`); missing explicitly requested
`--ledger-file` / `--ledger-rev` can exit2. The entry itself contains no local
erratum. Disclosure is not a correction, but a disclosed new local error does
not by itself show a lost pre-existing axis capability or falsify C1/C2.

## 7. Routed defects and closure boundaries

Tameshi owns these next-round items; none was repaired by this closure:

1. **R17-KNOW-EXIT / correction sweep:** append an entry-local erratum naming
   the false §5 exit sentence, distinguishing absent default vs explicit ledger.
   Also narrow the `measure-*.json` citation: its `-strict` receipt is not an
   overlay run. Retain old evidence bytes.
2. **R17-CMD-BIND / G5:** correct the assertion that K02 holes1–4 are all closed;
   either bind trace argv to the declared/required commands with failure-backed
   coverage, or explicitly preserve the narrower input-keyed evidence claim.
   G7's hole5→hole7 pointer and G5's dated89 versus final94 tally also need a
   named correction, not historical evidence rewrites.
3. **R17-GUARD-COVERAGE:** surviving removals of G3 tag-object and G5 symlink-mode
   guards; registry detached-checkout and short-rev regex; trace O_RDWR,
   pycache-prefix and execve guards. These seven named guard removals across
   three mutation reports survived their selftests; code existence is not
   behavioral coverage. Add the missing tests in the owner's next round.
4. **R17-GIT-ENV:** `tools/bash-witness-study.py` still lacks a full GIT_* scrub;
   its round-13 pin is `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`.
   Its remedy must preserve historical receipts via an explicit migration, not
   silently edit pinned bytes. QUALITY28 correctly leaves this open.
5. **R17-JJ-GUARDS:** evidence-disposition G2/G3 still compare to HEAD, not the
   resolved branch tip. Repair with a failure-backed jj fixture. Current closure
   equality HEAD=master must not be generalized to all jj states.
6. **R17-TIMEOUT:** registry NaN/Infinity timeout parsing and setsid escape;
   retained as disclosed tool-operability edge debts, not proofs of baseline-row
   regression. Carry forward older-leg environment scrub, confinement and
   successor-sweep debts from r16.
7. **R17-CITATIONS / CORRECTION-MECHANICS:** S060's stat-only inference needs the
   collector syscall-list anchor; S061's paragraph anchor is imprecise.
   `detect_branch` moved to line115 in fleet5d8a3b5 while SKILL:1029 and five
   ER-jj/R3 knowledge notes cite53–65. Operator-runbook in-place substitutions,
   though named by appended ER-R3, do not follow the corpus's append-only
   correction mechanism. The SOURCES footer update is not a literal pure append.
   SHONEN's added correction prose also exceeds the canonical single-evidence-line
   format; resolve its format without treating this closure as promotion.
8. **R17-INCIDENT:** preserve the disclosed live Git write/helper-bypass incident
   and its canary evidence. A safe helper-owned recovery procedure is fleet/operator
   tooling scope; tameshi must route that need, never normalize ad hoc Git plumbing.

Cross-domain routing, without sibling edits: mado owns stale prose naming the
old runner as the live harness; kaidoku owns the staged-pin statement in
`ConnFleetJjPractice.md:86-89` that predates the final landing. Fleet/operator
owns the recovery helper and its moving line anchors. The seven dead W2 seats
remain disclosed as dead, not retroactively replaced by this closure's reviewers.

All four SHONEN boxes remain `[~]`. This round makes the bounded box-3 evidence
checkable; I have not independently re-adjudicated the historical end-to-end
and all-box promotion evidence. Consequently I do not assert all four boxes
fully checkable for promotion, and no mark, rank, promotion or mint was changed.
