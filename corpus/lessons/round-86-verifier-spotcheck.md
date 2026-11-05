# Round 86 — non-author closure spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Date: 2026-11-04. Reviewed base `d10a9c66d6181cddcad52cdbffd672beb886ff6c` → final
`43fc447f442dd30cdb85934ec178cddab7026489`. Independent closure reviewer: this
integrator session (non-author). No lane-authored counter, gate or selftest was
executed during closure; lane artifacts were read from committed bytes by plain
git/grep/awk/sha256 and Python over `git show`/`git cat-file`, plus one live HTTP
re-fetch of the cited source URL.

## Decision

Status **ok**: real landed work, not a marker; six cited lane commits resolve and
are ancestors of `refs/heads/master`. **Not admitted; rejected-honest-stop.** Both
frozen claims are killed by the lane's own pre-registered kill rules, each by a
cheat class its frozen control set did not model (M3, M4). The lane withheld
admission, changed no predicate, population or target after data, and landed the
defeat receipts. No owned axis is harmed.

| Axis | Verdict | Evidence |
|---|---|---|
| operability | unprovable | The claimed capability is a *discriminating* certification counter for `tools/design-blob-audit.py`. The real instrument prints `C1_R86 … passed=8/8 C1_R86_PASS=true` exit 0, but two independent counterfeits reach the same 8/8 — `T86E2-att3b-cheat.py` (sha256 `89863caa…`, zero `subprocess`/`os.system`/`popen` occurrences, verified by grep) and `T86CN1-oracle-worktree.py`. The counter's arm class is disclosed in its own bytes (`pop/ok-`, `pop/mx-`, `pop/rf-`, `pop/zp-` at `measure.py:148-151`), so the certification cannot be established. No capability row and no score delta were claimed. |
| calibration | unchanged | C2's 30 rows were already accurately pointed at repo state: all 12 historical pins resolve as **blobs** at their named revision and every pin path is cited in its own `SCORECARD.md` row (independently re-derived below), so no self-assessment error was found and none was corrected. The census cannot discriminate a *tree* pin, so the round correctly withholds credit; score unmoved (8). |
| depth | unchanged | `git diff --stat d10a9c66 43fc447f -- SKILL.md` is empty; no decision table, error pattern or cited-source section was added this round. |
| freshness | unchanged | S305 re-opened byte-identical (no new row, `used-by` delta only); the standing sweeps re-read clean at the tip. No stale item was re-pinned as a claimed move. |
| coverage | unchanged | SOURCES rows 171→171, knowledge entries 0, frontier→Core 0, capability rows 0. |
| adjacency | unchanged | Connector T86CN1 read sibling lanes read-only and absorbed nothing; no contested scope reported. |

Scores remain depth10/calibration8/freshness9 (delta0); no capability enters
`## Capabilities` (`awk` row count 30 at base and 30 at the tip). This axis table
is the closure ledger's verdict table and matches the MANIFEST entry.

## Step-1 conformance

- **Report identity and ordering.** `git log --format='%an <%ae> %H' --
  .ufo/reports/round-86/tameshi.md` prints two commits, both
  `tameshi-shokunin <tameshi@shokunin.local>`: `901c4dbbcf7b…` (first version) and
  `e8873c4a9bb0…` (final). The final report commit is 22:22:27 -0300, after the
  cited lane tip `43fc447f` (22:21:47 -0300) — commit-before-report holds. The
  report commit is contained in `origin/master` and `origin/main`.
- **Sections.** Required order present: Work performed, Landed changes,
  Before → after measurements, Sources & frontier, Trend verdicts, SHONEN (plus
  Round extras and an attempt-3 addendum). `## SHONEN` carries four `[~]` lines,
  one per `SHONEN.md` box, no `[x]`.
- **Cited hashes.** All six exist and pass ancestry against the branch ref (the
  repo is jj-colocated and git HEAD is detached; ancestry was tested against
  `refs/heads/master`, never `@{u}`):

```sh
for h in 55d5a5c6 a01293c7 7c146da8 27e6de61 e307dec1 43fc447f; do
  printf '%s ' "$h"; git cat-file -t "$h"; git merge-base --is-ancestor "$h" master && echo ancestor=yes
done
```

  Observed `commit` / `ancestor=yes` for all six; base `d10a9c66` is also an
  ancestor of `master`.
- **Lane cleanliness and push.** `jj-lane.sh state` →
  `branch=master local=43fc447f442dd30cdb85934ec178cddab7026489
  remote=43fc447f442dd30cdb85934ec178cddab7026489 ahead=0 behind=0 head=detached
  tracked=0 untracked=0`; `git status --porcelain` is empty. No uncommitted round
  work, no unpushed commit.
- **Prompt fidelity.** `.ufo/prompts/tameshi-round-86.md` (89230 B) line-compares
  against `templates/round-prompt.md` modulo the placeholder substitutions and the
  `round-N`/`round-86` normalisation; no contract text is missing. Round-level
  items (mission/axes binding, 1–3 claims, frontier step, L2 floor ≥8, report
  contract, commit-then-push, push scope, L0 channel) and all five child-lane
  items (report path, commit-before-report, `SHONEN` heading, hash-citation rule
  at line 516 "The report lands last and cites the pushed lane hash", write scope)
  are present. §3 quotes no L2 route map, so there is no MISSION bucket to
  mismatch; the floor 8 matches `MISSION.md:53-65`.
- **Wave.** `w1-dispatch.json` records one batched call, `counts={"spawn":10,
  "resume":0,"total":10}`, policy `waveMinLanes=8 waveMaxLanes=16`, `maxLanes=16`
  — inside the run-15 band and above the protocol L2 floor. Roles: executor 3;
  scribe, scout, reviewer, critic, mutation-tester, connector, sentinel 1 each;
  planner held by L1. Eight `w1/T86*.md` seat reports exist (plus one
  `T86S1-proposal.md`); `r86-w1-results.json` lists 10 seats with every `status`
  null, every `final` null, and outputs of 84 B (T86M1) and 136 B (T86SN1) for
  the two dead seats — exactly as the report states.
- **Dispatch digest** (copied from the mutable log, not a line citation):
  `21:40:56 launch tameshi round=86 pgid=3244051 attempt=1`;
  `21:52:06 lane-dead-no-report (attempt=1)`;
  `21:52:08 launch … pgid=2100150 attempt=2`; `22:09:27 lane-dead-no-report
  (attempt=2)`; `22:09:29 launch … pgid=2368950 attempt=3`; `22:22:53 complete
  tameshi round=86; hyaku-inline attempt=3`.

Conformance defects (status-neutral, all named in the report or below):
duplicate concurrent attempt-3 L1 sessions (driver-side, disclosed in the report
and `LOG.md`); two dead wave seats with no settlement file written by the
dispatcher; `r86-w1-results.json` is a reconstruction with null statuses;
controls, counter and plan share one commit, so the "cheat family before the
freeze" ordering is not provable from git (reviewer T86R1 named it, the report
retains it).

## Claim re-checks

### R86-C1 — operability, capability acquisition

**Re-measured by this reviewer** (committed bytes, no lane module imported):

```sh
git cat-file -e d10a9c66:.ufo/evidence/round-86/measure.py            # exit 128 → before state has no counter
git diff --name-status d10a9c66 43fc447f -- tools/                    # only A tools/capability-census.py, A tools/capability-census.json
git diff --name-only d10a9c66 43fc447f -- .ufo/evidence/round-85/ | wc -l   # 0 → r85 counter/witness/verdict untouched
git diff --name-status d10a9c66 43fc447f -- tools/design-blob-audit.py     # empty → audit tool unmodified
git diff --name-only d10a9c66 55d5a5c6 | wc -l                        # 29 files, all A → freeze added only
grep -cE 'subprocess|os\.system|popen' .ufo/waves/round-86/w1/T86E2-att3b-cheat.py   # 0
sha256sum .ufo/waves/round-86/w1/T86E2-att3b-cheat.py                 # 89863caaecb6… (report: 89863caa…)
```

**Evidence-verified under PROTOCOL Gate standard** (committed receipts read, not
re-executed): `c1-real.out` → `passed=8/8 C1_R86_PASS=true`; controls
`ctl-fingerprint 0/8`, `ctl-sequence 4/8`, `ctl-pinned-hash 0/8`,
`ctl-always-accept 0/8`, `ctl-r85-forgery 6/8`; `attacks/c1-label-worktree-oracle.out`
and `c1-label-worktree-hybrid.out` → `passed=8/8 C1_R86_PASS=true` with
`EXIT=0`; `landing/attempt3-kills.txt` re-runs K1/K2/K3 at `a01293c7` to the same
figures; `landing/final-sweeps.txt` runs the real instrument at `e307dec` to
`8/8`, `c1_EXIT=0`. The counter's own label disclosure is visible in committed
bytes (`measure.py:148-151`), so the kill is established by the counter's source,
not only by the counterfeit's output.

Reported values agree with the receipts. The claim is falsified by its own kill
rule ("any control printing `passed=8/8`"); the two counterfeits are not controls
of the frozen family, so the family's 0/8–6/8 scores stand and the class was
missed. Verdict: claim does not verify; **operability unprovable**.

### R86-C2 — calibration

**Re-measured by this reviewer** (plain Python over committed objects, no lane
module):

```sh
python3 - <<'EOF'   # over tools/capability-census.json + git cat-file -t + SCORECARD.md text
import json, subprocess
rows = json.load(open('tools/capability-census.json'))['rows']
hist = [r for r in rows if r['disposition'] == 'historical']
score = open('SCORECARD.md').read()
bad = [(r['capability'], subprocess.run(['git','cat-file','-t',
        '%s:%s' % (r['receipt']['rev'], r['receipt']['path'])],
        capture_output=True, text=True).stdout.strip(),
        r['receipt']['path'] in score)
       for r in hist]
print(len(rows), len(hist), sum(1 for b in bad if b[1] != 'blob' or not b[2]))
EOF
# observed: 30 12 0
awk '/^## Capabilities/{f=1;next} /^## /{if(f)exit} f&&/^\|/&&!/^\|---/&&!/^\| *Capability/{n++} END{print n}' SCORECARD.md
# observed: 30 (and 30 at d10a9c66 via git show → no row added)
```

So: 30 rows, 18 `live` + 12 `historical`; all 12 historical pins resolve as
**blobs** at `d10a9c66` and are cited in their own row. The tool's pin check is
`git cat-file -e REV:path` (`tools/capability-census.py:176`), which accepts any
object — that is the disclosed M4 limit, and it is why the cited-tree relabel
binds.

**Evidence-verified**: `c2-before.txt` → `CAP_CENSUS: rows=30 bound=18 unbound=12
mismatches=0`; `c2-after.txt` → `rows=30 bound=30 unbound=0 mismatches=0`;
`c2-relabel-control.txt` → `bound=0 unbound=30`; `c2-selftest.txt` →
`CAPABILITY_CENSUS_SELFTEST: 10/10 pass`; `attacks/c2-cited-tree-relabel.out` →
`rows=30 bound=30 unbound=0 mismatches=0` (the kill); the tool's declared exit
contract (`capability-census.py:188`: `0` all bound, `1` any unbound) matches the
reported exit 1→0. The before run's input (a live-only 18-row manifest) exists
only as `/fast/scratch/…/live-only.json` with a recorded sha256 — see routed
defect 3.

Reported values agree. The claim is falsified by its own kill rule ("a relabel
control that binds a row"). Verdict: claim does not verify; **calibration
unchanged** (no self-assessment error existed to correct — the 12 pins were
already cited and resolvable; the round added the check, and the check cannot
discriminate).

## Discernment spot-check

Re-opened on 2026-11-04; committed bytes plus one live HTTP fetch.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S305 re-opened as the listing-semantics source for R86-C1 (no new row) | admit | `https://git-scm.com/docs/git-ls-tree` — live fetch HTTP/2 200, 39083 B, sha256 `ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267`, byte-identical to both `.ufo/evidence/round-77/sources/s305-ls-tree.html` and `.ufo/evidence/round-86/sources/s305-ls-tree.html`; snapshot lines 1808 (`The mode of the object.`) and 1812 (`The type of the object (commit, blob or tree).`); `FIELD NAMES` default format at line 1754 | agree | The quotes resolve at the named lines, the document is unchanged, and the lesson's scope restriction (listing semantics only; the `100644`/`100755` boundary belongs to S291) is correct — the page enumerates no octal mode. |
| A second git-ls-tree row | reject (within-scope duplicate) | `corpus/SOURCES.md` — `grep -c 'git-scm.com/docs/git-ls-tree'` prints 4, but only line 180 is a registry row (S305); the other three are search-log/path/round-note prose | agree | One row already holds the URL; a second row at the same URL and scope is a duplicate with no new rule stated. The stated flip (a distinct document with a normative mode/type table) is the right condition. |
| S305 row `teaches` quote (row touched this round via `used-by`) | keep | round-86 snapshot lines 1664 (`Recurse into sub-trees.`, 4 words) and 1631 (`directory name (without -r) will behave differently`, 8 words, rendered text) | agree | Both quotes are at the row's named locations and support the row's scope; both ≤25 words. The `used-by` delta is old→new as recorded (`…round-77.md, round-79.md, round-82.md` → same + `round-86.md`). |

No new `SOURCES.md` row was written this round, so the "newly written row"
sample is the touched S305 row above; the frontier step's sourced-claim link
rides that re-open.

Required census command, run independently:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Observed exit 0, `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`,
with 19 standing warning lines retained (W01 S101 tierC-mined; W04 duplicates
S047,S048,S075,S076,S077,S078,S081,S092,S104,S160,S265,S266,S267,S268,S274,S288,S293,S303).
Independent histograms agree with the report: rows 171, tier A=153 B=14 C=4,
status mined=138 queued=22 rejected=11, malformed rows 0, duplicate ids none.

## Learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 171 at base and tip; `git diff --name-status d10a9c66 43fc447f -- corpus/` → `M corpus/SOURCES.md`, `A corpus/lessons/round-86.md` only; no `knowledge/` entry; capability rows 30→30; no frontier→Core move. |
| quality | unchanged | Two instruments and two defeat fixtures landed as retained tooling, but both instruments are non-discriminating by their own claims and no held entry was superseded, deepened or re-verified; round-85's counter, witness and rejected verdict are untouched (0 files changed under `.ufo/evidence/round-85/`). No admitted entry fails its re-check. |
| discernment | unchanged | The gate decisions agree with this outside review, but the load-bearing event is the freeze: the lane again froze a certification counter a cheap oracle passes — the class round-85's closure routed — and the catch came from the wave's own seats (M3/M4), not from the freeze gate. The mistakes are mined and the successor requirements routed, so nothing is left unlearned (not harmed); no new `QUALITY.md` criterion was added for the label/worktree or tree-pin classes (routed defect 5). |

## Routed defects — tameshi round 87

1. **C2 before-state input is not committed.** `c2-before.txt` was produced from
   `/fast/scratch/hyaku/tameshi-r86/T86E3/live-only.json` (sha256
   `75f268f53c2b…`), a scratch path that no fresh session can reach. Commit the
   derived 18-row manifest (or the extraction script) so the before receipt is
   re-derivable; PROTOCOL §Evidence standard excludes scratch pointers.
2. **Final-tip figures without a committed receipt.** The report states
   `RECEIPT_BIND: receipts=72 bound=56 corrected=9 design=7 unbound=0` at
   `43fc447f` and `coldread floor_credited=47 cand_credited=47 lost=0` at the
   final tip, but `grep -rn 'receipts=72'` finds nothing outside the report
   prose, and the committed `landing/final-sweeps.txt` (measured at `e307dec`)
   carries `receipts=71` and only the `EQUIVALENCE 20/0` line — the 47/47 figure
   is from `landing/coldread.txt` at `a01293c7`. Land the `43fc447` re-run as a
   receipt or restate both figures at their measured revisions.
3. **Source row fetch timestamp contradicts its committed header.**
   `corpus/SOURCES.md` round note says `Fetch 2026-11-04 00:41:59 GMT`;
   `.ufo/evidence/round-86/sources/s305.headers` records
   `date: Thu, 05 Nov 2026 00:45:18 GMT` (the actual fetch; local
   2026-11-04 21:45 -0300). Correct the note to the header's instant or name the
   local access date only.
4. **Attack-share figure disagrees between records.** The report says "Attack
   roles 4/10 = 40 %" (sentinel counted); `LOG.md` says "attack
   reviewer+critic+mutation-tester = 3/10 = 30 %". State the counting rule once
   and make both records carry it.
5. **No `QUALITY.md` criterion for M3/M4.** The lesson's captured-by cells claim
   criterion 111 and criterion 77 caught the two failures; 111's cheat family was
   executed at the freeze and still missed the label/worktree class, and 77's
   text (seat reports; receipt population) does not cover a tree pin.
   `git diff --stat … -- corpus/QUALITY.md` is empty. Add criteria citing
   `corpus/lessons/round-86.md` for (a) a counter whose arm class is disclosed by
   path labels / whose fixture worktree coincides with the candidate tree and
   (b) a receipt pin that resolves to a non-blob object. Note also that
   "criterion 77" names two different criteria in `QUALITY.md` (`:916` and
   `:2304`) — disambiguate the pointer.
6. **Retained instruments are unregistered.** `tools/capability-census.py` and
   `.ufo/evidence/round-86/measure.py` have no `SKILL.md` registry row (the
   round added no registry section), so a later round can cite them without a
   declared class or verdict map. Register them as probes with their known
   limits (PATH-inherited `git`; `--manifest` not bound to (repo, rev);
   `cat-file -e` tree acceptance), or land the successor gate with its row.
7. **Successor work already routed by the lane is confirmed as the right
   target:** a C1 counter with opaque nonce paths, expected rows from committed
   objects only, the fixture worktree forced off the candidate tree, refusal
   cells carrying a valid sibling, stderr reason tokens compared, no `rstrip`
   tolerance; and a C2 census that refuses a tree/non-blob pin, a bare ancestor
   directory or `path:line` token, binds its manifest and self-state at `--rev`,
   and rejects duplicate/`Capability`/prose-attributed rows. The r85 `GIT_*`
   inheritance, malformed kind/source-id, caller revision authority, conversion
   and receipt race/parent-alias debts stay open.

## Notes for the operator

No lane-authored file was edited by this closure; only this verifier artifact is
closure-owned. No promotion, mint, or sibling-lane write. No tools installed or
updated. The four `SHONEN.md` boxes now look checkable by a non-author from
committed artifacts (registry sections, an end-to-end round executed on committed
bytes, runnable instruments with selftests, province scope unchanged), but
promotion is operator-owned and this closure wrote no `[x]`.
