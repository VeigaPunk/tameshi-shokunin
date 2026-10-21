# ResAccounting-5 — round-24 wave-1 seat accounting attack (residual, item 5)

**Scope.** Attack the seat accounting of wave 1 of round 24: `accounting1.json`,
`accounting1-expected.json`, `accounting1-result.json`, `outcomes1.json` against
`task-call1.json` (64 tasks), `dispatch1-attempt1/2/3.json` and the 64 reports in
`w1/`. Two questions from the item: (a) is *report presence never completion*
respected, (b) is the RowAudit01 misroot handling (lesson `## Mistakes` addendum)
consistent.

**Verdict.** The accounting *totals and seat set are sound* — the gate runs clean
(exit 0, 64/64/0) and reproduces the retained result byte-for-byte, and the 64 seat
names, ids, roles and report paths agree across every retained artifact.
*Report presence never completion* is respected in the tool, in the frozen oracle,
and in the integrator's own prose. Two real defects were found, both in the
**citation/receipt layer, not in the numbers**: (D1) the lesson's `seat misroot`
row points at the *destination* path instead of the *defect site*, which makes the
row's factual claim false as written; (D2) round 24 retained **no** misroot-sweep
receipt, unlike rounds 20/21/22, so the row's "shown able to fail" evidence and
the byte-exactness claim are unverifiable from retained bytes. Two lower-severity
gaps: (D3) `accounting1-result.json` dropped the round-23 receipt convention
(argv/exit/cwd/tool_sha256/timestamp/basis); (D4) wave-name drift
(`round24-w1` vs `tameshi-r24-w1`).

No tool, fixture, ruler or registry byte was changed. No production file was
edited. The only file written is this report.

---

## 0. Environment, provenance, tooling

* Lane clone (private): `/fast/scratch/hyaku/tameshi-r24/ResAccounting-5/repo`,
  `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin …`,
  `git checkout --detach 4903959687d16623adeeeae059bc010dcfc9d23f`
  (`HEAD is now at 4903959 round-24: retain wave-1 spec, dispatch receipts, 64 seat
  reports, accounting and errata O-P`). The initial `/tmp` clone was moved to the
  `/fast/scratch` path per the L1 host directive (the `/tmp` volume was full).
* Tooling: **no install, no upgrade** — the task needed only `python3` (3.x,
  stdlib) and `git`. Nothing was installed, so no tool/version/channel record is
  owed under the operator tooling directive.
* Live lane state at inspection time: `git rev-parse HEAD` =
  `4903959687d16623adeeeae059bc010dcfc9d23f`; `git status --porcelain` shows only
  `?? .ufo/evidence/round-24/final-verification.json` (post-tip closure receipt),
  `?? .ufo/waves/round-24/residual-dispatch.json` (this residual wave) and
  `?? .ufo/waves/round-24/residual/` (peer residual reports + this file).
  No tracked byte differs from the tip.

## 1. Required command — exit code and totals (as asked)

```
$ cd /fast/scratch/hyaku/tameshi-r24/ResAccounting-5/repo
$ python3 tools/wave-accounting.py --bundle .ufo/waves/round-24/accounting1.json \
      --expected .ufo/waves/round-24/accounting1-expected.json --json
{
  "authority": "declared retained callbacks; report presence never completion; not provider authentication",
  "bundle_sha256": "5216539e9743b8435b345f9dcfe2f74966f75a761b7c6c8b14caf0554b8cf70a",
  "finding_ids": [], "findings": [],
  "schema": "wave-accounting-result-v1",
  "total": { "completed": 64, "dead": 0, "seats": 64 },
  "waves": [ { "completed": 64, "dead": 0, "failed_with_report": [],
               "name": "round24-w1", "report_artifacts": 64, "seats": 64 } ]
}
EXIT=0
```

* **exit 0**, `finding_ids: []`, totals **seats 64 / completed 64 / dead 0**,
  `report_artifacts 64`, `failed_with_report []`.
* The retained `.ufo/waves/round-24/accounting1-result.json` is **identical** to
  this output (parsed-object equality `mine == retained` → `True`).
* Digest binding is live: re-running the *edited* bundle against the *un-edited*
  expected file returns **exit 2 / `SNAPSHOT_TAMPERED`**.
* The tool's own frozen selftest at this tip: `python3 tools/wave-accounting.py
  --selftest` → `ACCOUNTING_SELFTEST: 8/8 pass`, `ACCOUNTING_EXTRA_SELFTEST:
  16/16 pass`, `FINDING: SELFTEST_PASS`, **exit 0**.
* Live-lane vs committed-tip bytes for the accounting set and the lesson are
  identical (sha256): `accounting1.json 5216539e…`, `outcomes1.json d604075b…`,
  `accounting1-expected.json 4a85d0d5…`, `accounting1-result.json 2590cc8d…`,
  `corpus/lessons/round-24.md 72b9c490…`; all 64 `w1/*.md` identical to the clone.

## 2. Is *report presence never completion* respected? — YES, in all three places

**(a) The gate.** `tools/wave-accounting.py:100-113` derives completion *only* from
`outcomes[].status`; `reports` feeds nothing but the `report_artifacts` count and
the `failed_with_report` cross-check (a *failed* seat that also has a report).
`claimed` totals are compared against the status-derived summary
(`tools/wave-accounting.py:115-119`), so a report can never promote a seat.

**(b) The frozen oracle** already encodes the rule:
`.ufo/evidence/round-22/measure.py:13-14` — cases `false-completion-count` and
`failed-with-report-counted-completed` (both expect `TOTAL_MISMATCH`);
`.ufo/evidence/round-22/accounting-extra-cases.json:77-82` —
`no-reports-still-one-completed` (`"reports": []` with one `completed` seat,
`expected_exit 0`). Both pass at this tip via the selftest run above.

**(c) My own falsification probes** (private scratch, copies only — the lane's
bytes were never touched):

| probe | mutation | result |
|---|---|---|
| P0 | re-serialised bundle, fresh digest | exit 0, 64/64/0 |
| P1 | **drop `RowAudit01` from `reports`, keep status `completed`** | **exit 0**, `completed` stays **64**, `report_artifacts` 63 → completion is *not* derived from report presence |
| P2 | `RowAudit01` status → `failed`, report kept | exit 1, `TOTAL_MISMATCH`, `failed_with_report: ['RowAudit01']` → a report does not make a seat completed |
| P3 | remove the seat from members/outcomes/reports | exit 1, `TOTAL_MISMATCH` (63 seats) |
| P4 | add a report for a non-member (`GhostSeat`) | exit 1, `UNKNOWN_REPORT` |
| P5 | edit bundle, keep old expected digest | exit 2, `SNAPSHOT_TAMPERED` |

**(d) The integrator's prose is consistent with the rule.** `outcomes1.json:2`
("report files never establish completion … 63 reports were written in the lane;
RowAudit01 misrooted its report to the fleet root, moved byte-exact (`cmp 0`)"),
and every emitted result carries
`"authority": "declared retained callbacks; report presence never completion; not
provider authentication"`. Round 23's equivalent receipt says the same in other
words: `.ufo/evidence/round-23/accounting/receipt.json` → `basis: "… report files
are an artifact inventory only"`.

**Consequence for this wave's honesty.** The 64 reports on disk and the 64
declared completions agree *by coincidence of a healthy wave*, not by
construction: 63 reports were written in the lane and 1 was misrooted and moved
back, so a directory listing alone would also have shown 64. The retained
`outcomes1.json` correctly attributes completion to callbacks, not to files.

## 3. Cross-artifact consistency of the seat set (all 64)

Identical **64 names in identical order** across: `spec1.json` `items` (64) →
`task-call1.json` `tasks` (64) → `dispatch1-attempt3.json`
`result.details.progress[64].id` → `w1/swarm-registry.json` `members` (64) →
`accounting1.json` `members`/`outcomes`/`reports` (64/64/64) → `outcomes1.json`
`completed` (64) → the 64 `.md` files in `w1/` (the 65th file there is
`swarm-registry.json`, correctly *not* counted as a report).

* **Roles**: bundle role == dispatch receipt per-seat `agent` field == registry
  role == `route-mix1.stdout` histogram (reviewer 14, critic 13, scout 11,
  executor 10, connector 6, mutation-tester 4, revenger 3, sentinel 1, scribe 1,
  simplifier 1) — 0 mismatches.
* **Ids**: every bundle id is `TameshiR24-2.<Seat>`; the receipt's 64 ids are
  identical and in the same order; `job` == `id` for all 64.
* **Payload**: for all 64, `progress[i].assignment` == `task-call1.json` task text
  **+ one identical 980-byte operator tooling-directive block** appended by the
  harness. So "the same validated 64-seat payload unchanged" (lesson
  `## Mistakes` row 4) is true for attempt 3.
* **Reports**: bundle `reports` (64) == `w1/*.md` basenames (64), no extras, no
  missing; all 64 files are non-empty (2 364 B … 36 028 B), all 64 sha256 are
  distinct (no duplicate/copy-paste report), every file contains a `Verdict`
  line, and no report contains a TODO/placeholder/self-declared-incomplete
  marker that would contradict `status: completed`.
* **Dispatch attempts 1-2**: each receipt contains exactly **64** refusal
  segments, every one `Background job limit reached (100)` — 0 spawned, as
  claimed. Attempt 3: `Spawned 64 background agents`, 64 progress entries.
  The receipt's `result.details.results` is `[]` and all 64 progress entries are
  `status: "pending"` (a spawn-time snapshot), i.e. the receipt itself cannot
  evidence completion — consistent with the declared-callback authority.

## 4. Findings

### D1 — MEDIUM — lesson `## Mistakes` addendum cites the wrong path for the defect site

`corpus/lessons/round-24.md:219`:

> | seat misroot | RowAudit01 wrote its report to the fleet root, at
> `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-24/w1/RowAudit01.md`
> (sha256 `3bc5633c…`), despite the wave context's absolute-path rule | … |

The cited path is the **lane destination** — the path the wave context *requires*
— not the fleet root, and not where the seat actually wrote. The fleet root is
`/home/vgpnk/Projects/shokunin`; the lane is a child of it, so the sentence is
false under either reading of "fleet root", and the defect site is not recorded
anywhere.

The row's own "shown able to fail" indicator disproves the cited path:
`git -C /home/vgpnk/Projects/shokunin status --porcelain` listed
`?? .ufo/waves/round-24/`. That line can only come from the **fleet's** own
`.ufo/` tree, because the fleet repo ignores the whole lane:
`/home/vgpnk/Projects/shokunin/.gitignore:1` = `*-shokunin/`, and
`git check-ignore -v tameshi-shokunin` → `.gitignore:1:*-shokunin/ tameshi-shokunin`.
A write under `tameshi-shokunin/` can **never** appear in the fleet porcelain.
The governing prompt agrees: `/home/vgpnk/Projects/shokunin/.ufo/prompts/
tameshi-round-24.md:297-301` ("seat tools also start at the fleet root, so a
relative path such as `.ufo/waves/...` lands in the FLEET repo") and
`:312-316` (the §6.3 misroot sweep: copy byte-exact into the same relative path
under the lane, `cmp`, delete the fleet copy, record under `## Mistakes`). The
seat's trailer was the relative `Report: .ufo/waves/round-24/w1/RowAudit01.md`
(from its own dispatched prompt, retained in `dispatch1-attempt3.json`), so the
misroot site was `/home/vgpnk/Projects/shokunin/.ufo/waves/round-24/w1/RowAudit01.md`.

Everything else in the row checks out: the retained lane copy's digest is
`3bc5633cbdb22df4861df820849a69c6ba37eca53bc5953762cfb626ad0b908f` (matches the
cited `3bc5633c…`); the fleet copy is gone
(`/home/vgpnk/Projects/shokunin/.ufo/waves/round-24` → *No such file or
directory*); today's fleet porcelain (13 lines) no longer lists
`?? .ufo/waves/round-24/`; and the handling itself (copy byte-exact into the
lane, delete the one fleet copy, record under `## Mistakes`) matches prompt §6.3
and QUALITY criterion 19 (`corpus/QUALITY.md:97-100`, "The round's misroot sweep
checks fleet-root entries with no pathspec"). The "Captured-by: prompt §6.3
misroot sweep" pointer is accurate.

**Impact.** A reader cannot re-derive the defect from the row: it names the
corrected location as the defect. If the row is taken literally, the fleet-root
misroot becomes invisible and a future seat can repeat it believing the lane path
was the forbidden place.

**Smallest safe correction** (append-only, no tool/fixture/ruler/registry byte
touched): in `corpus/lessons/round-24.md:219`, replace the evidence pointer with
the defect site and name the destination separately, e.g. *"RowAudit01 wrote its
report to the fleet root at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-24/w1/RowAudit01.md`; it was
copied byte-exact to
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-24/w1/RowAudit01.md`
(sha256 `3bc5633c…`) and the fleet copy deleted."* The `sha256 3bc5633c…` value
and the `cmp 0` / porcelain indicator stay as they are.

### D2 — LOW/MEDIUM — no retained misroot-sweep receipt for round 24

Rounds 20, 21 and 22 each retained the sweep itself:
`.ufo/evidence/round-20/final/misroot-sweep.json` (argv, exit, stdout,
classification), `.ufo/evidence/round-21/final/misroot-sweep.json`,
`.ufo/evidence/round-22/misroot-sweep.txt` (command, exit, observation).
Round 24 retains **none** — `ls .ufo/evidence/round-24/` yields no
`misroot-sweep*`. The row's "shown able to fail" therefore rests on an
*unretained* command output, and because the fleet copy was deleted, the
"copied byte-exact (`cmp 0`)" claim has no retained witness either: the only
retained digest is that of the file that now sits in the lane, which cannot
distinguish "copied byte-exact" from "was always there".

**Impact.** The lesson's evidence pointer is the weakest of its kind: a prose
claim about a command nobody retained, on the one class of error (a seat writing
outside its lane) that the fleet's gitignore makes invisible by construction.

**Smallest safe correction.** Retain a sweep receipt for round 24 in
`.ufo/evidence/round-24/` in the round-20/21/22 shape: the `git -C
/home/vgpnk/Projects/shokunin status --porcelain` argv and exit, the stdout line
`?? .ufo/waves/round-24/` as observed before the move, the post-removal stdout,
and the moved file's sha256 at both ends (`3bc5633c…`). No tool/fixture/ruler
byte changes.

### D3 — LOW — `accounting1-result.json` regressed the round-23 receipt convention

`.ufo/evidence/round-23/accounting/receipt.json` retains the full invocation:
`argv`, `cwd`, `revision_of_tool 549ede24…`, `tool_sha256 96b3038a…`,
`measurement_interval`, `exit`, `stdout`, `stderr`, `basis`.
`.ufo/waves/round-24/accounting1-result.json` retains only the parsed result
(`authority`, `bundle_sha256`, `finding_ids`, `findings`, `schema`, `total`,
`waves`). Nothing binds that file to a tool version or an invocation: a
hand-written file of the same shape is indistinguishable from a captured one.

Mitigating facts: `tools/wave-accounting.py` is **byte-identical** at
`549ede24aa9b2a6746d3973cf55dc4ceb07a5413` and at the tip
(sha256 `96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e`,
`git log 549ede2..4903959 -- tools/wave-accounting.py` is empty), and I re-ran
the gate at the tip and reproduced the retained file exactly — so the *content*
is correct; only the provenance record is missing.

**Smallest safe correction.** Add a receipt wrapper beside it (argv, cwd,
tool_sha256, exit, stdout, basis) in the round-23 shape, or fold the same
fields into `accounting1-result.json` as an appended sibling file.

### D4 — LOW (nit) — wave-name drift

`accounting1.json` names the wave `round24-w1`; `spec1.json` and
`w1/swarm-registry.json` name it `tameshi-r24-w1`; round 22 used `wave1`/`wave2`
and round 23 `w1`/`w2`. Findings are keyed by wave name, so cross-round
aggregation needs a mapping. Cosmetic only (each bundle holds one wave).

### D5 — INFO (already recorded by a peer; no new defect) — attempt 2 was not the identical payload

`dispatch1-attempt2.json` refused the seats under **mutated** names
(`CloseTameshi22.PredK1-2` … `CloseTameshi22.RowAudit08-2`), while attempt 1 used
`CloseTameshi22.<Seat>`. Both refused 64/64 at the 100-job cap and spawned
nothing, so no seat existed under either name and no accounting consequence
follows; the lesson's "same validated 64-seat payload unchanged" claim is about
attempt 3 and is verified true (§3). `w1/OverlapKama.md:93` already records that
round 24 has 0 `ufo-swarm-wave-dispatch-v1` files, so the standard settlement
tool (`mori-wave-settlement.py`, which classifies
present/empty/stub/missing/misrooted/unsafe per seat) cannot settle this wave —
which is why the misroot was caught by a manual sweep rather than by tooling.
That is a pre-existing, already-recorded gap, not a new finding.

## 5. What I checked and found clean (no defect)

* Gate exit code, totals, and byte-exact reproduction of the retained result.
* Digest pinning of the bundle (`SNAPSHOT_TAMPERED` on edit) and the
  `expected` schema guard.
* Completion is never derived from report presence — code, frozen oracle, extra
  fixtures, and four independent mutation probes.
* 64/64 seat-name, id and role agreement across seven artifacts; no duplicate
  agent ids; no `replaced: true` (all 64 `replaced: false`, `outcomes1.json`
  `replaced: []`).
* Every seat's dispatched assignment equals its validated task text plus the one
  identical operator-directive block; every seat's `Report:` trailer equals
  `.ufo/waves/round-24/w1/<Seat>.md`, matching the accounting `reports` list.
* Attempts 1-2 refused 64/64 with the exact 100-job-cap message; attempt 3
  spawned 64 with the right ids/roles/payload.
* All 64 reports non-empty, mutually distinct, each with a verdict, none
  self-declared incomplete → no report contradicts a `completed` status.
* The wave context's §6.3 requirement and QUALITY criterion 19 (no-pathspec
  fleet sweep) are met in substance: the fleet copy is gone and the fleet
  porcelain no longer lists `.ufo/waves/round-24/`.
* Lane tree equals the committed tip for every accounting/lesson byte.

## 6. Residual risk / verification gaps

* Completion authority remains *declared* (`outcomes1.json`): the callback
  notices are not retained as bytes, and the dispatch receipt's own
  `results: []` shows the spawn receipt cannot evidence completion. The gate
  says so in every output (`not provider authentication`); nothing in this round
  upgrades it, and I do not claim producer authentication.
* Because the lane is gitignored by the fleet (`*-shokunin/`), any *future* lane
  misroot that lands under `tameshi-shokunin/` is invisible to the prescribed
  sweep — only misroots into the fleet's `.ufo/` tree are detectable by it. The
  round-24 case was of the detectable kind, but the blind spot is systematic.
* D1/D2 leave the round-24 misroot class documented but not fully
  re-verifiable from retained bytes; a retained sweep receipt (D2) plus the
  corrected pointer (D1) closes it.

## 7. Smallest safe correction set (append-only, no production bytes)

1. `corpus/lessons/round-24.md:219` — correct the `seat misroot` evidence
   pointer to the fleet-root defect site
   (`/home/vgpnk/Projects/shokunin/.ufo/waves/round-24/w1/RowAudit01.md`) and
   name the lane destination
   (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-24/w1/RowAudit01.md`,
   sha256 `3bc5633c…`). Keep `sha256`, `cmp 0` and the porcelain indicator.
2. Retain `.ufo/evidence/round-24/misroot-sweep.json` in the round-20/21/22
   shape (argv, exit, before/after stdout, sha256 at both ends).
3. Add `.ufo/waves/round-24/accounting1-receipt.json` with argv, cwd,
   tool_sha256 `96b3038a…`, exit, stdout, basis (round-23 shape).
4. Optional: state the wave-name mapping (`round24-w1` ≡ `tameshi-r24-w1`) in
   the accounting bundle or the receipt.

None of these touch a tool, fixture, ruler or registry byte, so the frozen
before/after pair and the no-harm receipts stay valid.
