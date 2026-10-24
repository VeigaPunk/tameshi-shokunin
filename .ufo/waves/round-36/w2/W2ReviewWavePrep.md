# W2ReviewWavePrep — wave-preparation receipts, falsified (round-36 w2, calibration)

**Verdict: PARTIALLY SUSTAINED, premise FALSE.** The two specs exist, are
validator-clean, and sum to **78** seats (39 + 39) — not 80; every seat prompt
carries the godspeed lead byte-verbatim and both identical contexts carry the
absolute-path bounds; no seat report existed at receipt time (nothing was
secretly dispatched). But the "80" premise is unsupported anywhere in the
record except this seat's own committed prompt, and the receipt layer carries
three citation defects (validate filenames, unbacked exit 0, "report itemizes"
attribution).

## What I attacked

1. The dispatch premise itself: "the report itemizes **80** prepared-but-undispatched seats".
2. Existence of `spec-w{1,2}.json` and the item sum.
3. The godspeed lead and the absolute-path bounds, byte level.
4. Whether any seat report existed when the receipt was made ("nothing was secretly dispatched").
5. Every corroborating count in `LOG.md`, `corpus/lessons/round-36.md` and the round report.

Round-36 lane revisions in play: `796e08b` (r35 tip), `e423c41` (content), `b455001` (refresh),
`d9c496b` (receipts), `fbb01cf` (HEAD, verifier spot-check, 2026-10-24 03:34:28 -0300).
Fleet round report: `f4ef953` (2026-10-24 03:23:40 -0300).

## Findings, by severity

### HIGH — the "80" premise is false, and it is baked into this wave's own validated dispatch

Canonical count is **78**: `spec-w1.json` 39 items + `spec-w2.json` 39 items. This is
stable at every revision and in every carrier:

| Carrier | w1 | w2 | total |
|---|---|---|---|
| `spec-*.json` `items[]` | 39 | 39 | 78 |
| `dispatch-*.json` `tasks[]` / `counts.total` / `registry.members` | 39 | 39 | 78 |
| validator re-run (`plan`, scratch copies) | 39 | 39 | 78 |
| fleet report `f4ef953` (`:56`, `:133`) | 39 | 39 | 78 |
| `LOG.md:1941-1942` ("Round total 78 prepared seats") | — | — | 78 |
| `corpus/lessons/round-36.md:83-85` | 39 | 39 | 78 |

Repo-wide grep for `80 prepared|prepared-but-undispatched: 80|80 seats` returns exactly
**3** hits, all the same bytes: `.ufo/waves/round-36/spec-w2.json:284`,
`.ufo/waves/round-36/validate-w2.stdout:568`, `.ufo/waves/round-36/dispatch-w2.json:568` —
i.e. this seat's prompt only, copied through validation into the dispatch untouched.
No receipt, log line, lesson, or report states 80. Any 80 would have to count seats that
exist in no spec (the L1 planner seat and/or the orchestrator), and nobody itemizes that.

Impact: this is a false premise injected into a calibration-judged falsification seat, in
committed bytes that the validator rendered. A seat that repeats it corrupts the round
record; the correct repair is to strike the count from `spec-w2.json:284` (and its
rendered `dispatch-w2.json` / `validate-w2.stdout`) or set it to 78 before the round folds.

### MEDIUM — `LOG.md:1940` names validation artifacts that never existed

`LOG.md:1939-1940` says the specs are "validator-checked specs (`validate-w1.json`,
`validate-w2.json`)". Neither path exists: `ls` → ENOENT, and
`git log --all -- .ufo/waves/round-36/validate-w1.json .ufo/waves/round-36/validate-w2.json`
returns 0 commits. The committed artifacts are `validate-w{1,2}.stdout` (byte-identical to
`dispatch-w{1,2}.json`: sha256 `03c7fe1c…` / `96d32f1e…`) and 0-byte `validate-w{1,2}.stderr`.
Same defect class as the round's own repaired dead pointer (QUALITY criterion 72): a cited
name that does not re-resolve.

### MEDIUM — "exit 0" for validation has no exit receipt

Round report `:53` claims "`validate-w1/w2.stdout` exit 0". There is no `.exit` artifact in
`.ufo/waves/round-36/` (directory holds exactly 2 specs, 2 dispatches, 2 stdouts, 2 empty
stderrs before the live wave dirs), and `validate-*.stdout` is the *rendered dispatch
payload*, not a verdict — it contains no pass/fail or exit field. Empty stderr is necessary
but not sufficient. The fact is independently true: I re-ran the validator
(`node /home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs plan --spec <copy>`,
exit 0 on both, empty stderr), and the re-rendered `tasks[]`/`context` are **byte-identical**
to the committed dispatch (only the `policy` block differs — see INFO below). So the claim is
true but undemonstrable from committed bytes; an exit-code receipt is missing.

### LOW–MEDIUM — "the round report itemizes the 78 prepared-but-undispatched seats" is a category error

`corpus/lessons/round-36.md:85` and `LOG.md:1940-1941` attribute the per-seat itemization to
the round report. The report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/tameshi.md`,
`f4ef953`) contains **zero** seat names — grep for four sampled names
(`ConnectorSiblingOverlap`, `W2ReviewC1Causality`, `W2ReviewWavePrep`, `ScribeGateAudit`) →
0 hits. It gives aggregate counts and a §3-floor sentence and delegates enumeration to the
spec files. The itemization does exist — 78 pairwise-distinct named items in
`spec-w{1,2}.json` — just not where the lesson/LOG say it is.

**Correction to two w1 peers (calibration value):** `ReviewC1Claim.md` (MEDIUM, "dangling
round-36 report") and `SimplifierReceiptDupes.md` (C1) are **false positives as written**.
The round report is not missing; it is in the FLEET repo at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/tameshi.md` (`f4ef953`), and both peers
searched only the lane's `.ufo/reports/` (which holds `round-1/tameshi.md` alone). The real
defect is narrower: the report exists but does not itemize names (this finding). A
lane-relative reading of `.ufo/reports/` is still a dead pointer, so the LOG wording should
carry the fleet path.

### LOW — the w1 role enumeration understates the mix

Report `:49-50`: "`spec-w1.json` (39 seats: 1 connector, 3 executors, 1 scribe, 2+ scouts,
reviewers, critics, mutation-testers, revengers, simplifier …)". Read as a mix this is wrong;
as a §3-floor restatement it is right. Actual w1 mix (computed from `spec-w1.json`):
connector 1, executor **6**, scribe 1, scout **6**, reviewer 4, critic 4, mutation-tester 10,
revenger 5, simplifier 2 = 39. The floor claim itself holds (connector ≥1, executor ≥3,
scribe ≥1, scout ≥1, reviewer/critic present). w2 (39): reviewer 7, critic 6,
mutation-tester 9, revenger 5, scout 7, simplifier 2, executor 3 — no connector/scribe, which
policy v1 permits (floor is a w1 obligation).

### INFO — re-render is not byte-reproducible because the live policy moved

The committed dispatch `policy` block records `minLanes 16, waveMin 32, waveMax 64`
(v1 band). Today's live `ufo-fsd-alpha/config/ufo.json → sighting.dispatch.swarm` is
`{minLanes 32, maxLanes 256, rampBatchSize 5, rampIntervalMs 700}`, so the same specs
re-render with `waveMin 32 / waveMax 256`. Tasks and context are byte-identical; only
`policy` differs, so the specs still validate (39 is inside 32–256) but `dispatch-*.json`
cannot be reproduced byte-for-byte from today's config. Not a defect in the receipt, a
reproducibility caveat for anyone re-running it.

### INFO — registry rows are unwritten

`dispatch-*.json` names `registry.path = .ufo/waves/round-36/w{1,2}/swarm-registry.json`;
neither exists, and neither wave dir was tracked at HEAD. Member rows are all
`agentId: null, item: null` — correct pre-dispatch, but it means "which agent ran which
seat" rests on report filenames until `record` runs.

## What checked out

- **Both specs exist and are committed**: blobs `d6df5eb8…` (w1) / `e9b95864…` (w2),
  identical at `ef37d72`, `e423c41`, `b455001`, `d9c496b`, `fbb01cf`. File sha256
  `1d7fba5a…` / `5dddc961…`; dispatch `03c7fe1c…` / `96d32f1e…`; each `validate-*.stdout`
  is byte-identical to its dispatch; both stderrs 0 bytes.
- **Godspeed lead is byte-verbatim and universal**: every one of the 78 item prompts begins
  with `/skill:godspeed\n\n` + the 427-byte `~/.agents/skills/godspeed/directive.md`
  (sha256 `db88963c…`) + `\n\n` = a single distinct 446-byte prefix per wave, same sha256
  `08689bcd…` in both waves. The 78 dispatch tasks start with that prefix and append
  `Lane bounds: leaf member — no subagent dispatch.` / `Judged on: <axes>` / the Report
  trailer; `Judged on` agrees with the spec `axes` on **78/78** (calibration 59, depth 19),
  and every trailer resolves to `<reportDir>/<name>.md` (78/78).
- **Absolute-path bounds are carried**: the two contexts are byte-identical and include
  "# Bounds (hard)" with "Your tools start at the FLEET ROOT. Every path you use MUST be
  absolute; a relative path such as `.ufo/waves/...` lands in the FLEET repo and is a scope
  violation", the tooling authorization, the `pacman` guard, and the lane-report resolution
  rule. The Report trailers are lane-relative *by design* and resolvable only through that
  context — observed working: 39/39 w1 reports landed at the lane path.
- **Nothing was secretly dispatched.** No `round-36/w1/` or `w2/` path exists in any git
  object (`git rev-list --all --objects | grep round-36/w[12]/` → empty; no deleting commit
  in `--diff-filter=D` history). Earliest existing seat report is
  `w1/ScoutSHONEN.md` at **03:25:54**; the fleet report was committed **03:23:40**; the
  watchdog records `complete tameshi round=36` at **03:24:28** (`watchdog.log:1154`).
  Dispatch therefore began ≥86 s *after* the L1's round closed — the receipt's
  "0 dispatched this seat" is true, and "undispatched" was true at commit time.
- **Live state (audit time, superseding the receipt as expected)**: 39 w1 + 20 w2 reports
  at first count, 27 w2 by write time — w2 was still landing, so the number is a snapshot.
  All untracked (`git status --porcelain` → `?? .ufo/waves/round-36/w1/`,
  `?? .ufo/waves/round-36/w2/`), every filename ⊆ its spec's name set, zero extras. w1 is
  39/39 complete. This is the orchestrator's post-round dispatch, not a leak of the L1's seat.
- **No dead seats**: 0 duplicate prompt bodies and 0 duplicate task bodies in either wave;
  78 distinct names; registry members == dispatch names (39/39 each); no `model` key anywhere
  (recursive scan); one dispatch call per wave, compaction not applied.

## Commands run (all read-only; lane revision `fbb01cf` unless stated)

1. `ls -la` / `stat` / `python3` JSON parses of `.ufo/waves/round-36/{spec,dispatch}-w{1,2}.json`
   — item/task/registry counts, role histograms, recursive `model` scan, prompt-prefix hashing,
   duplicate-prompt and duplicate-task detection, `Judged on` vs `axes` agreement, trailer paths.
2. `sha256sum` / `md5sum` on specs, dispatches, validate stdout/stderr; byte compare
   `validate-w*.stdout` vs `dispatch-w*.json`.
3. `git log --oneline`, `git rev-parse HEAD`, `git ls-tree -r --name-only HEAD -- .ufo/waves/round-36`,
   `git show <rev>:<path>` for `e423c41`, `b455001`, `d9c496b`, `fbb01cf`; `git log --all` for
   `validate-w{1,2}.json` (0 commits); `git rev-list --all --objects | grep round-36/w[12]/`
   (empty); `git log --all --diff-filter=D -- .ufo/waves/round-36` (empty);
   `git status --porcelain -- .ufo/waves/round-36`.
4. Byte compare of the 446-byte prompt prefix against `~/.agents/skills/godspeed/directive.md`
   and `skill://godspeed` / `SKILL.md`.
5. Independent validation, scratch copies only
   (`/fast/scratch/hyaku/tameshi-r36-seats/W2ReviewWavePrep/`):
   `node /home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs plan --spec <copy>`
   → exit 0 both waves, 0-byte stderr; JSON diff vs committed dispatch = `policy` key only.
6. Reads: fleet `.ufo/reports/round-36/tameshi.md` (`f4ef953`, 138 lines), `LOG.md:1935-1943`,
   `corpus/lessons/round-36.md:78-90`, `ufo-fsd-alpha/config/ufo.json`,
   `scripts/hyaku/ufo-wave-policy{,-v2}.json`, `.ufo/watchdog.log:1143,1154`.
7. Repo-wide grep for `prepared-but-undispatched` and for `80 prepared|80 seats` (3 hits, all
   this seat's prompt bytes).

Tool installs: **none**. No `pacman`, no mutating git/jj, no lane/fleet/state edits; the only
lane file written is this report.

## Residual risk / gaps

- "Public slots" style count drift is the risk here too: 80 vs 78 is exactly the class of
  error the round is trying to eliminate, and it now sits in committed dispatch bytes that a
  later wave may quote as authoritative.
- Byte-reproducibility is gone for `dispatch-*.json` (live policy moved); future audits must
  compare `tasks`/`context`, not whole-file hashes.
- The "no secret dispatch" conclusion rests on git objects (strong) plus report mtimes and the
  watchdog round-close line (strong but not cryptographic); a seat that ran and wrote nowhere
  would be invisible.
- I did not run the dispatcher's `record` path, so registry population is unverified by design.
