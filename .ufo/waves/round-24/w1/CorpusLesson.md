# CorpusLesson — round-24 W1 critic: `corpus/lessons/round-24.md`

Verdict: **defects found, all fixable text corrections; nothing here requires rejecting the admit candidates.**
The Claims and S084/S085 anchors check out against retained evidence. The Mistakes row's
"shown able to fail" cell is only half delivered, though. It shows the base failing (1/11) and then
promises an after measurement "recorded below once executed", but nothing follows it. At the delivered
revision c8c5b88 the lesson records no after result, no replay run, and no source re-anchor
outcome. By the lesson's own first Reject rule and QUALITY48, it cannot yet serve as the evidence
that the fix holds after the change. Separately, the Gate flip condition is boilerplate. For two of
the four rejects, no "execution or authority record" could flip the inference.

Lesson revision inspected: last changed in d2eaecd (`git log -- corpus/lessons/round-24.md`), and the
same bytes are at HEAD c8c5b88. Read-only inspection only. No ruler, selftest or battery was run
(this item does not say "Run").

## Defects (each with a counterexample)

### D1 — the after half of "Fix / shown able to fail" is missing (medium, calibration)
- `corpus/lessons/round-24.md:53` ends: "The after measurement is recorded below once executed."
  The file has 53 lines (`wc -l`), so nothing comes below it.
- Commits after the lesson, absent from it: bd38c02 "retain refusing replay run and binding
  verdict" (`replay-command.json` exit 0 over 43 rows; `replay/live-dependent.json`
  live_dependent `["pin-disposition-read","verify-round15"]`, revision_pinned 41;
  `replay-gate.json` exit 0, `finding_ids []`, bundle_sha256 `4f42402…a9c6`) and c8c5b88
  (fifteen source re-anchors).
- The only after measurement is a seat report, `.ufo/waves/round-24/w1/RunRulerAfter.md`
  (11/11, exit 0 at c8c5b88). It sits in an untracked directory (`git status`: `?? .ufo/waves/round-24/`)
  and is not a retained lane receipt.
- Counterexample: a reader who applies the lesson's Reject 1 ("fails at base and holds after")
  to the lesson itself finds only the base half. QUALITY48's falsifier is also unexecuted
  (`corpus/QUALITY.md:504-505`: "is expected to give 11/11"), and so is SCORECARD round 24 ("Measured
  results are recorded below only after execution", with nothing below).
- Axis: calibration.
- Smallest safe correction: retain an after receipt such as `.ufo/evidence/round-24/after.json`, in
  the same shape as `before.json` (argv, cwd, revision, exit, stdout, instrument_sha256 `0a7f6daa…a64`).
  Then replace the dangling sentence with the result and its pointer, and add one line for the replay
  run (43 rows, 41 revision-pinned, 2 live-dependent, gate 0/[]).

### D2 — the flip condition cannot fire for half of the rejects (low–medium, calibration)
- `round-24.md:28-29`: "Flip condition: an independently retained, applicable execution or
  authority record." This is copied from round23 (`round-23.md:23-25`), where it covered
  receipt/authority inferences.
- Counterexample: for "four mutant kills as general mutation adequacy" (`:24`), no execution
  record of these four mutants flips anything. Only a broader mutation sweep would. For "realpath
  identity as write isolation" (`:25`), the replay clone's fleet mirror symlinks the live siblings
  (`knowledge/replay-projection-hardening.md:34-36`; `tools/registry-replay.py:19`). Only an
  isolation mechanism would flip that, not a record. A flip condition that cannot discriminate is
  not shown able to fail.
- Smallest safe correction: give each reject its own flip. Mutation adequacy flips on a retained
  sweep over the named guard class. Isolation flips on a retained, non-symlinked or read-only
  mount. Digest authentication flips on a producer signature. Keep the execution/authority record
  only for the "fixed" reject.

### D3 — the "Closure rounds[421]" pointer does not name its file or repository (low)
- `round-24.md:53` says "Closure rounds[421]". It resolves only to the fleet repository's
  `/home/vgpnk/Projects/shokunin/MANIFEST.json` (424 rounds; index 421 is `lane tameshi`,
  `lane_round 23`, `type closure`, committed in fleet 5e0ab5f). The lesson does not say this. Only
  `contract.json` "sources" says "MANIFEST rounds[421]".
- The cited probe (`verification.rechecks`) says the any-vs-all mutant "survives the ten-case ruler
  (single-token fixtures) but is killed by selftest all-of-tokens". The gap half is the ruler blind
  spot. The kill half is K4's control, which is fine, but the row should say which half it cites.
- Correction: "fleet `MANIFEST.json` rounds[421].verification.rechecks (fleet 5e0ab5f): survives
  the ten-case round23 ruler".

### D4 — K2 has no routed source (low, calibration provenance)
- `fresh-adjudication.json:48-106` `routed_not_executed` lists eight items. Only ArgvExact is the
  name-insensitive argv case (line 53). No case-fold item exists. `rg -i casefold|case-fold` over
  `.ufo/waves/round-23`, the closure MANIFEST and LOG finds nothing, apart from the round24 knowledge
  file and SCORECARD.
- `contract.json` claims the eleven are "routed by round23 critics and closure", and the lesson's
  title and QUALITY48 speak of routed gaps. K2 (argv-casefold) was added by the author.
- The admitted "round24 selftest fixtures" include `argv-padded-token` and `argv-repeated-flag`
  (`extra-cases.json`, 6 cases). No ruler mutant targets either one. [INFERENCE] The base exact list
  compare already rejects both, so they are controls rather than kills. Even so, the knowledge table's
  "stripped or de-duplicated … Fails when a weakened comparison lets the public selftest pass" is
  unmeasured.
- Correction: in Claims, label K2 as author-added hardening rather than routed, and name the two
  extra fixtures as controls.

### D5 — round24's own process mistakes are missing from the Mistakes table (low, completeness)
- `.ufo/waves/round-24/validation1-refused.stderr`: `unknown_role … items[54].role "labrat" is not a swarm role`.
- `dispatch1-attempt1.json` and `dispatch1-attempt2.json`: 64/64 seats each hit "Background job
  limit reached (100)".
- `dispatch1-attempt3.json`: dispatched by TameshiR24-2 rather than CloseTameshi22.
- Round23 recorded the same class as a "tooling invocation" row (`round-23.md:44`). These events
  came after the lesson commit, and their evidence is untracked.
- Correction: once this evidence is retained, append a tooling-invocation row pointing to these files.

### D6 — small anchor imprecisions (nit)
- S084: the lesson says non-strict mode "may still contain links or loops" "for missing
  components" (`:34-35`). The live doc's default-mode paragraph covers components that are missing,
  are symlink loops, or raise OSError. The paragraph quoted for S084 is the first one; the
  "may still contain" wording is in the third. The scoping argument stands.
- S085 says "lines 53–104". The `routed_not_executed` array spans 48–106, and 53–104 runs from the
  first defect line to the last. That is acceptable but not the whole array.
- Captured-by cites QUALITY15/29. QUALITY15 (`QUALITY.md:61`) concerns stale expectations and
  setup errors, which is a weak fit. The nearest existing criterion is QUALITY47 (`:472`). It already
  required live/external rows to be reported separately and named "cannot fail on argv by
  construction", but as a reporting rule rather than a failing predicate. The row's claim, "no
  criterion required routed gaps to become failing predicates", still holds.

## Verified (no defect found)
| Claim | Check | Result |
|---|---|---|
| 1/11 at 6a1821a; K1–K3 survive the 38-case selftest; K5–K6 still hold; K7–K11 tool-absent; K4 killed | parsed `before.json` stdout rows | exact: K1–K3 exit 0, `failing_cases []`, `38/38 pass`; K4 `CASE all-of-tokens FAIL`; K5/K6 control and substituted both True; K7–K11 `tool-absent` |
| ruler frozen at e338f1b | `sha256sum measure.py` vs `git show e338f1b:…` vs `before.json` instrument_sha256 | all `0a7f6daa…a64`; `git diff --stat e338f1b HEAD` empty for measure/contract/before |
| landed before any seat | e338f1b 15:47:40Z; first dispatch file 16:06Z; attempt3 at 16:27:53Z | holds |
| 34/64 dead, all 20 reviewers | `original-outcomes2.json`: seats 64, completed 30, dead 34; `('reviewer','failed'): 20` and no completed reviewer | holds |
| S085 line 66 quote | `fresh-adjudication.json:66`, unchanged between 6a1821a and HEAD | exact |
| S084 quote and version | `curl https://docs.python.org/3/library/os.path.html`: title "Python 3.15.1 documentation"; first paragraph starts with the quoted text; "may still contain links or loops" present | holds |
| SOURCES: two new mined rows; on-release/on-change; used-by; no existing row changed | `git diff 6a1821a HEAD -- corpus/SOURCES.md` | additions only (S084, S085, lookup note, `Next unused id: S086`) |
| bounded lookup 2/2/2/0 | SOURCES footer | matches |
| numeric calibration stays 8 | SCORECARD:1129 "depth 8, calibration 8"; contract bounds | consistent |
| Gate admit candidates exist; successors append-only and pinned | `git diff … tools/registry.json` | 3 rows superseded with `superseded_by`; pinned rows carry `bundle_sha256` literals; the selftest successor says 44/44 (= 38 + 6 cases) |
| replay runner hashed from the clone copy | `registry-replay.py:162-163`; `observations.json` `runner_sha256_clone_copy` | holds. The instrument digest in `replay-command.json` is from the live tree but is labelled "equals rev blob" |

Impacted axes: calibration (D1, D2, D4), with completeness and evidence resolvability (D3, D5).
None of these is a tradeoff the judge must reject. All are fixable text and receipt additions. The
judge should still not accept this lesson as the after evidence until D1 is fixed.

Tool installs and updates: none (used the existing curl and python3).
Not claimed: producer authentication, promotion, R17-CMD-BIND closure, numeric uplift.
