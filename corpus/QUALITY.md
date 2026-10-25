# Admission bar (probation draft)

1. Every claim falsifiable or marked opinion.
2. Every claim carries a source: a measured anchor (path:line, command,
   evidence id) — never oral knowledge.
3. Observation, inference, and unknown stay separate.
4. Errata are append-only blocks.
5. A rejection is kept, not silently dropped.

## Criteria appended — fleet round 1 (kaika continuation, 2026-10-19)

Each criterion cites the mistake it learns from
(`lessons/round-1.md` `## Mistakes`). Criteria 1–5 are unchanged.

6. A pre-registered prediction carries its executed outcome in the same
   entry; a miss is an errata row naming the discriminator, never a
   silent drop. (MK-2, MK-3)
7. A knowledge file lands with its coverage-map row in the same round,
   or the missing row is named as debt in `LOG.md` with an owner.
   (MK-4)
8. A verification that ran lands its report in-repo in the round it
   ran; an executed-but-unreported verification is named debt, never
   cited as a pass. (MK-5)
9. Scratch stays in `/tmp`; evidence a claim rests on is copied into
   the repo (`.ufo/evidence/…`) before the commit that cites it.
   (MK-6)
10. A new `knowledge/` entry opens with `source:`, `verified-at:` and
    `recheck:`; an external source enters through a `SOURCES.md` row
    opened in the round that writes it (tiers: `SOURCES.md`, contract
    v1); a tier-C row is never sole support. (MK-7)

## Criteria appended — round 12

11. A repeated-control clean verdict names its finite sample and compares
    raw exit/stdout/stderr tuples; it never proves determinism. Its
    counterexample must defeat a one-control observation and trigger the
    same committed mismatch oracle after the repair.
    (`lessons/round-12.md`, vacuous mistake)
12. A frozen witness declaration records prior exposure and checks integrity
    before replay. Report all declared defects, unresolved denominators and
    accidental kills; reanalyzing an existing artifact is not a new gate.
    (`lessons/round-12.md`, attribution mistake)
13. Promotion restraint remains separate from partial procedure exercises:
    an Appendix A/B cold-read cannot earn full-page box-3 score credit.
    (`lessons/round-1-verifier-spotcheck.md`, Adjudication;
    `lessons/round-12.md`, attribution mistake)

## Criteria appended — round 13

14. A normalized provenance field must agree with its digest-anchored
    declaration source and preserve its prior-exposure disclosure.
    Missing or null companion metadata is not a clean normalization;
    retain the frozen faulty observation and add a separately checked
    correction. The same checker must reject the old-null companion and
    accept the kind-only repair.
    (`lessons/round-13.md`, reference-drift mistake; outside routed
    `lessons/round-12-verifier-spotcheck.md`, Routed defects item 3)

## Criteria appended — round 14

15. Every retained expectation is explicitly effective or superseded by named,
    checked replacement evidence. A setup error with the expected exit code
    is not proof of the intended assertion; the same reconciliation command
    must reject the unresolved original row and accept the disposition-only
    repair without rewriting its raw observation.
    (`lessons/round-14.md`, stale-expectation mistake; outside
    `lessons/round-13-verifier-spotcheck.md`, Routed defects item1)
16. An environment-injection claim retains its bounded non-secret overrides
    beside argv, cwd and outcome; comparison names every excluded volatile
    field. An undocumented historical setup stays unproven even when a new
    documented experiment succeeds.
    (`lessons/round-14.md`, missing-setup mistake; outside
    `lessons/round-13-verifier-spotcheck.md`, Routed defects item2; S049)

## Criteria appended — round 15

17. Classify an instrument by its behavior, not its label: comparing persisted
    expectations and returning a mismatch verdict makes it a gate. Its public
    isolated self-invocation asserts literal exits and stable finding IDs;
    helper-only controls are not a standalone selftest. Explicitly classify
    every nonzero exit, including usage, and retain the unsupported old
    invocation alongside the same-command repaired result.
    (`lessons/round-15.md`, gate-misclassification and exit-class-ambiguity;
    outside `lessons/round-14-verifier-spotcheck.md`, Routed defects5)

## Criteria appended — round 16

18. An attributed finding ID comes from the stream's terminal structured
    verdict, cross-checked against the process exit, never from the first
    token match in mixed help and verdict text. The repair keeps any prior
    structured branch (JSON) unchanged. The same command must reject the old
    attribution and accept the repair on the same retained bytes, including a
    forged-line fixture. The faulty receipt is corrected by an appended
    record, never rewritten.
    (`lessons/round-16.md`, attribution mistakes; outside
    `lessons/round-15-verifier-spotcheck.md`, Routed defects 2)
19. A seat note lands under the lane root or reaches the L1 as a message.
    Every per-seat prompt names the L1 as `agent://<id>`; a bare id is a file
    path. The round's misroot sweep checks fleet-root entries with no
    pathspec, and it must flag the archived round-15 bytes.
    (`lessons/round-16.md`, landing mistake)
20. An instrument that seats execute in a wave is not edited in place during
    that wave. Changes are staged at a separate path and installed after the
    readers finish, and every receipt names the instrument sha it ran.
    (`lessons/round-16.md`, scope mistake)

21. Supersedes criterion 20's last clause ("every receipt names the instrument
    sha it ran"). A retained receipt carries the instrument's sha256 beside it
    in the same file, because the runner's `--selftest` prints none
    (`.ufo/evidence/round-16/round-gate/runner-selftest.txt` ends with the
    sha line). Criterion 20's no-in-place-edit rule stands; it recurred once
    in wave 2 (`measure.py` repaired after dispatch), and that wave's
    attackers read the committed bytes, so no verdict mixed the two.
    (`lessons/round-16.md`, scope and vacuous rows; w2 QualityReview,
    MistakeAudit)
22. Supersedes criterion 18's proof clause. An attribution repair's selftest
    must defeat each weaker rule it claims to exclude, one fixture per rule:
    first match, no exit cross-check, a line split wider than the emitter's,
    both-stream ambiguity, and a missing structured branch. A mutant that
    survives is named as equivalent with its reason. One forged-first-line
    fixture does not discriminate.
    (`lessons/round-16.md`, attribution rows; w2 AttrCritic2, MutateReattribute;
    `.ufo/evidence/round-16/attribution/selftest-mutants.json`)

## Criteria appended — round 17

23. Cold-read credit is keyed to what the read ran against, not only to the
    bucket's bytes. Every credited ledger entry carries non-empty `inputs`
    (lane path → sha256); each input must still be a regular blob with that
    sha at the measured rev, and an entry that executed commands must name
    committed trace receipts whose inputs it covers. A failing entry whose
    inputs still verify vetoes the bucket. Shown able to fail: the round-14
    bucket is credited at `e69b488` and uncredited (`input-drift:tools/mutate-and-run.sh`)
    at `09ee1d0` under `.ufo/evidence/round-17/measure.py`.
    (`lessons/round-16-verifier-spotcheck.md` §2, routed R16-C2b; S058, S059)
24. Editing an instrument that a registered gate pins means running that
    gate's registered entry command before landing. An outcome that changes
    is re-pinned or superseded by an appended manifest in the same round —
    "by design" may describe the mechanism, never excuse the outcome — and
    every mention of the old outcome is swept in that round.
    (`lessons/round-16-verifier-spotcheck.md` §3, routed R16-OP1 and R16-C2a;
    `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt`)
25. The no-harm monitor runs every active registered entry command
    (`python3 tools/registry-check.py --rev REV`), not only selftests, and
    grades each row against the outcome its capability was admitted with.
    A row leaves `active` only as `superseded` with a `superseded_by` row,
    and still runs. The monitor runs in a clone, never writing the lane.
    (`lessons/round-16-verifier-spotcheck.md` §3, routed R16-MON1;
    `.ufo/waves/round-17/w1/V02ToolsNoHarmScope.md`, K04RegistrySelfFulfilling.md)
26. A receipt found stale gets a dated correction appended in the round that
    finds it, naming both digests and their revisions; the original line is
    never rewritten. (`lessons/round-16-verifier-spotcheck.md` §6 item 5, routed R16-EV1)
27. Every lane tool that runs git — selftest fixtures included — scrubs the
    inherited `GIT_*` environment first, and its selftest proves it with a
    canary repository named by an exported `GIT_DIR` that must stay
    unchanged. An unscrubbed fixture commit moved the live lane's HEAD and
    index in round 17 wave 1. (`lessons/round-17.md`, environment-leak
    mistake; S063)
28. Correction to criterion 27 (round 17 wave 2, QualityCriteriaReview): as
    landed it was false for two git callers — `tools/bash-witness-study.py:337-341`
    (read-only `git show`, no env scrub; an exported `GIT_DIR` redirects the read)
    and `.ufo/evidence/round-17/jj/head-vs-branch.sh` (fixture commits leaked into
    a canary). The fixture script now scrubs `GIT_*` and proves it on a canary;
    `bash-witness-study.py` is pinned by round-13 `expected.json`, so its scrub
    lands with an appended disposition waiver in a later round and stays open
    debt until then. Criterion 27 applies to every other lane git caller.
    (`.ufo/waves/round-17/w2/QualityCriteriaReview.md`; `lessons/round-17.md`)

## Criteria appended — round 18

Each criterion turns one routed item of
`lessons/round-17-verifier-spotcheck.md` §7 into a falsifiable rule. Each
states its rule, what captured the failure, and the check that can fail.
Criteria 1–28 are unchanged; criterion 28's open debt is not closed here.

29. A lane guard is a check whose removal changes a verdict on some input.
    It counts as behaviorally covered only when removing its code makes the
    owning `--selftest` exit nonzero. Code existence is not coverage. A
    one-defect removal that leaves the selftest at exit 0 is a surviving
    mutant; the owner either adds a killing selftest case in its next round
    or names the mutant equivalent, with its reason, in the mutation report.
    Captured by: round-17 wave 2 reports `.ufo/waves/round-17/w2/MutateDispositionV2.md`
    (G3 tag-object and G5 symlink-mode survived), `MutateRegistryCheck.md`
    (detached-checkout and short-rev regex survived) and `MutateTraceInputs.md`
    (trace O_RDWR, pycache-prefix and execve survived).
    Check that can fail: apply each named removal to the owner's tool at the
    cited rev; the owning `--selftest` must exit nonzero for every one. Exit 0
    keeps that guard open debt.
    (`lessons/round-17-verifier-spotcheck.md` §7 item 3, R17-GUARD-COVERAGE)
30. A lane-state comparison reads the resolved branch tip
    `refs/heads/<branch>`, never bare `HEAD`. In a jj-colocated repository
    HEAD can differ from the branch tip, so a HEAD comparison can pass or fail
    for the wrong reason. A closure that observes HEAD = master proves that
    state only, not jj states in general.
    Captured by: `tools/evidence-disposition.py` at 183f87b states G2 and G3
    against HEAD (`:45-48`, `:179-180`) and implements G3 as
    `merge-base --is-ancestor rev HEAD` in `resolve_historical_rev` (`:441-451`).
    Check that can fail: a fixture from `jj git init --colocate` in /tmp whose
    HEAD differs from the branch tip; the verdict must follow the branch tip,
    and the same fixture must fail a HEAD-based copy of the tool.
    (`lessons/round-17-verifier-spotcheck.md` §7 item 5, R17-JJ-GUARDS)
31. A numeric config value read from a registry or manifest is finite and
    positive before use. NaN, Infinity, -Infinity and booleans are rejected
    with exit 2 naming the row and field. At timeout, every descendant of the
    row is killed, including one that called `setsid` and left the row's
    process group. A process still alive after the tool returns is a failure.
    Captured by: `tools/registry-check.py` at 183f87b; the positive check
    (`:221-227`, `ts <= 0`) admits NaN and infinity; `load_registry` (`:273`)
    parses at `:281` with plain `json.loads`, which accepts `NaN` and `Infinity`; the
    timeout path signals only the process group (`_kill_group`, `:306-322`,
    called at `:386`).
    Check that can fail: registry rows with `timeout_s` set to the JSON literal
    `NaN` and to `Infinity` must each exit 2 naming `timeout_s`; a row that
    starts `setsid` on a long-lived child must leave no live descendant after
    `registry-check` returns.
    (`lessons/round-17-verifier-spotcheck.md` §7 item 6, R17-TIMEOUT)
32. Every lane subprocess that may run git, including read-only `git show`,
    selftest fixtures and fixture scripts, removes every inherited `GIT_*`
    variable before it spawns. The scrub is proven by a selftest whose canary
    repository is named by an exported `GIT_DIR` (and `GIT_WORK_TREE`) and must
    stay byte-unchanged. A pinned tool's scrub fix lands only through an
    appended disposition waiver or manifest. The pinned bytes are not edited,
    and the old pin is marked superseded, not deleted.
    Captured by: `tools/bash-witness-study.py` at 183f87b has no `GIT_*`
    environment scrub (its only `GIT_` substrings are the identifier
    `TARGET_GIT_PATH`, lines 97, 339, 342, 359, 887); its `git show`
    subprocess runs at `:337-342` with inherited environment. Its round-13 pin is in
    `.ufo/evidence/round-13/expected.json:11`
    (`49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`).
    Check that can fail: export `GIT_DIR` at a canary and run the tool's
    selftest and its read-only path; the canary must be unchanged and the tool
    must read its intended repository. Removing the scrub from a staged copy
    must fail that case. Until the migration lands, the pinned sha must still
    match the file at the pinned rev.
    (`lessons/round-17-verifier-spotcheck.md` §7 item 4, R17-GIT-ENV; criterion 28)
33. Input-keyed credit (criterion 23) is evidence about the inputs a read ran
    against, not about the commands it ran. A claim that holes or commands are
    "covered", "closed" or "all run" binds each declared command to an argv in a
    committed trace receipt whose inputs cover the entry. Without that binding
    the entry says only "input-keyed evidence" and names the commands it did
    not trace.
    Captured by: the round-17 K02 claim that holes 1–4 were all closed; the
    closure routed it as an overclaim and named two remedies: bind trace argv
    to the required commands, or narrow the claim to input-keyed evidence
    (`lessons/round-17-verifier-spotcheck.md` §7 item 2).
    Check that can fail: compare the declared command set of each entry with
    the union of its receipts' argv. A declared command absent from every argv,
    or a "closed" sentence over an input-keyed-only entry, fails. Deleting one
    command from a fixture receipt must flip the verdict.
    (`lessons/round-17-verifier-spotcheck.md` §7 item 2, R17-CMD-BIND; criterion 23)
34. A citation into a file that moves, or that the lane does not own, is
    anchored by function or symbol name and the cited rev. A line range is a
    secondary aid. A bare line anchor into such a file expires with the next
    edit to that file. A paragraph anchor names a quoted sentence or a heading.
    Captured by: `detect_branch` moved to line 115 in fleet `5d8a3b5`, while
    SKILL:1029 and five ER-jj/R3 knowledge notes still cite lines 53–65. S060's
    stat-only inference and S061's paragraph anchor were imprecise.
    Check that can fail: at the cited rev, `git show REV:<path> | grep -n <name>`
    must find the cited definition inside the cited range. A line-only anchor
    into a moving file fails.
    (`lessons/round-17-verifier-spotcheck.md` §7 item 7, R17-CITATIONS)
35. A correction to a landed entry (an exit sentence, a count, a citation, a
    footer or a SHONEN correction) is an appended, dated erratum. It names the
    false text, its replacement and both revisions. The original bytes are never
    rewritten in place, and a SOURCES footer update is a literal append: it
    deletes no line. Where the stale text sits in a file the lane does not own,
    the lane appends its own erratum and routes the owner's substitution as a
    finding; it does not edit that file. This extends criterion 26 from receipts
    to corpus prose; criterion 4 (admission bar) already requires append-only
    errata.
    Captured by: the false exit sentence in the round-17 knowledge entry that §7 item 1 names;
    over-broad `measure-*.json` citation; operator-runbook substitutions named by
    an appended ER-R3 but made in place; a SOURCES footer edit that was not a
    pure append; and SHONEN correction prose beyond the single-evidence-line
    format.
    Check that can fail: `git diff --numstat REV_OLD REV_NEW -- <append-only file>`
    must report zero deleted lines for an erratum-only change. The named erratum
    must exist in the file under its own dated heading.
    (`lessons/round-17-verifier-spotcheck.md` §7 items 1 and 7, R17-KNOW-EXIT and R17-CITATIONS / CORRECTION-MECHANICS)
36. A stray write that moves a live lane repository (HEAD, a ref, the index or
    an object) by a process other than the lane's intended writer is preserved,
    not repaired by ad hoc plumbing. The lane first captures the reflog,
    `fsck --full`, ref and index state, and a canary result into the round's
    evidence directory. Restoration is performed only by a fleet- or
    operator-owned helper with a named procedure. A seat or lane tool issues no
    git write (`update-ref`, `read-tree`, `reset`, `symbolic-ref`, `checkout`,
    `commit`) to repair it outside a /tmp sandbox. The incident is routed to the
    owner as a finding.
    Captured by: round 17 wave 1, when a seat's fixture commits moved the live
    HEAD through a `GIT_DIR` leak. The L1's `read-tree` and `update-ref` repair
    bypassed the helper-only writer rule (`lessons/round-17-verifier-spotcheck.md` §2).
    Check that can fail: the incident record's repair transcript contains no
    live write verb from the list above, and the saved reflog is a prefix of
    the current `git reflog` output.
    (`lessons/round-17-verifier-spotcheck.md` §7 item 8, R17-INCIDENT)

## Corrections appended — round 18 wave 2 (2026-10-20)

Criteria 29–36 above stay as written; these corrections narrow them after
the non-author wave-2 review (`.ufo/waves/round-18/w2/ReviewQuality18.md`,
`ReviewAppendOnly.md`, `ReviewGuardKillEntry.md`).

- **32 (GIT_* scrub) is not yet true for every registered tool.**
  `.ufo/evidence/round-16/measure.py` (historical evidence bytes, two active
  registry rows) still passes inherited `GIT_*` to git; with only `GIT_DIR`
  exported its selftest commits into the exported repo. `registry-check`
  scrubs before every row, so the registered path is safe; a direct run is
  not. Open, routed to round 19 (migrate the rows to a scrubbed wrapper; never
  edit the round-16 bytes).
- **35 (append-only) — round 18 broke it twice and repaired one.** The
  `corpus/SOURCES.md` footer line `Next unused id: S065.` was replaced in
  `58e5d53`; it is restored and the new pointer appended after wave 2. The
  `SHONEN.md` regeneration replaced lines in place: PROTOCOL.md:446 requires
  the canonical seed verbatim, so SHONEN is the one file this criterion
  exempts; its removed prose is preserved verbatim in the round-18 LOG entry.
  The criterion's numstat check applies to append-only corpus files and
  `LOG.md`, not to `SKILL.md` or `SHONEN.md`.
- **36 (incident preservation) — the reflog check pointed the wrong way.**
  `git reflog` prints newest first, so a saved copy is a suffix of later
  output; the falsifiable check is that a saved copy of `.git/logs/HEAD` is a
  byte prefix of the current file.
- **33 (command binding) — the binding clause is a future rule.** Nothing in
  the round-18 kit compares declared commands with receipt argv; until a
  failure-backed implementation lands, 33 only forbids calling input-keyed
  credit command coverage.
- **29–31 (what the round-18 probes certify).** The probes are bounded:
  P08 binds `master`, P11 exports `GIT_DIR`/`GIT_WORK_TREE` only, P09 tries the
  two literals. Wave-2 mutation testing left 18 survivors in the new code
  (3 registry-check, 3 evidence-disposition, 2 trace-inputs, 10 bash-witness
  scrub/config); each is a named round-19 coverage gap under criterion 29.

## Criteria appended — round 19 (2026-10-21)

37. A metadata correction names the exact stale provenance field and line,
    not merely a body statement on the same subject. A preserved draft's
    `source:` or `verified-at:` line can remain byte-identical only when a
    dated, explicitly superseding erratum gives its effective value,
    measured revision and evidence pointer. Audit every staged/PENDING
    mention in the corrected entry; say which are historical, never leave
    a second current-result implication. Captured by round-18 verifier §5
    items 1–2; lesson `lessons/round-19.md`, Mistakes row 1. Falsifier:
    removing R18-1 or R18-2's explicit metadata erratum independently
    reopens that named population item in the round-19 correction ruler.
38. A diff count names its unit: changed cells, deleted table lines and
    deleted non-row lines are different quantities. A SOURCES mutable-cell
    exception lists each affected row ID and checks immutable cells
    separately; counting deletion lines does not prove cell compliance.
    Captured by round-18 verifier §5 item 3 and round-19 Mistakes row 2.
    Falsifier: the recorded historical diff is 25 added / 5 deleted lines,
    IDs S001/S008/S052/S056/S057; a four-line or four-cell assertion cannot
    satisfy the R18-3 correction, even though S008 changed two cells.
39. A final-success claim names one effective receipt with matching argv,
    measured revision, integer exit, retained stdout/stderr and both
    digests. A failed usage/setup attempt stays failed and byte-preserved;
    its successful successor explicitly names what it supersedes.
    Timeliness is not repaired retroactively: a later replay is dated as
    later, not presented as a receipt that already existed. Captured by
    round-18 verifier §5 items 4–5 and round-19 Mistakes rows 3–5.
    Falsifier: the same round-19 ruler rejects wrong argv/revision,
    bool-as-exit, exit 64, stream tampering or missing supersession, and
    rejects a missing exact-final-revision measure receipt. It does not
    authenticate the historical producer or certify required-command
    coverage; those remain distinct duties (criterion 33).
40. A historical calibration receipt is not a current no-harm monitor.
    After corpus/instruction changes, run the input-keyed ruler at the
    delivered revision; a lower current score is named before asserting
    unchanged calibration. Preserve the old ledger and refresh affected
    inputs through actual recorded source reads, with author/independent
    provenance labeled. Do not call source re-anchoring a blind cold-read
    or required-command coverage. Captured by round19's actual
    `current-ledger-monitor-21e7932.json` (49/60, restraint6) and w1 AxisBound;
    lesson `lessons/round-19.md`, No-harm repair. Falsifier: the strict
    default-ledger command at the cited delivered revision must reproduce
    the claimed current count with `overrides_used=false`, not a historical
    number copied from4b7c682.

Criterion38 range qualification (round19 w1 SourceCorrection): counts
bind both their **unit and full commit range**. Over183f87b→4b7c682 there
are five replaced table lines and six changed cells, not “four cells”;
the four-used-by-only observation holds for58e5d53→9ee1c80 alone.
Enforce allowed mutable cells by comparing the two pinned source tables,
not a handwritten numstat transcript. The round19 ruler pins both snapshot
digests, derives exact changed IDs/cells, and checks no removed IDs,
immutable changes or net lost non-row lines. Snapshot tampering, wrong
history or an extra claimed source ID must reopen R18-3. Lesson:
`lessons/round-19.md`, Build-wave findings / source range addendum.

## Criterion appended — round 20 (2026-10-21)

41. QUALITY20's no-in-place-edit rule is unchanged; QUALITY21 still requires
    the instrument identity beside the retained observation. Freeze staged
    paths and their SHA-256 values before dispatch. Install only after every
    reader returns. A receipt-window check compares the receipt's instrument
    SHA with the persisted frozen/installed identities and rejects unknown
    bytes. If the identities differ, a frozen measurement must end no later
    than edit start, and an installed measurement must begin no earlier than
    edit end. Record aware, ordered measurement intervals; classify older
    instrument identities explicitly instead of calling them all “the frozen
    SHA”. Equal identities are a byte-identity case, not evidence that the
    host was continuously monitored. Captured by the repeated enforcement
    failure in `lessons/round-19-verifier-spotcheck.md` routed item 1 and
    `lessons/round-20.md` Mistakes. Falsifier: public receipt-window fixtures
    for UNKNOWN_INSTRUMENT, FROZEN_AFTER_EDIT and INSTALLED_BEFORE_INSTALL
    fail with exit 1 while unchanged before/after-boundary controls pass.
    This validates declared receipt metadata, not producer authenticity,
    continuous edit detection, or required-command coverage.

42. A published “no overrides” measurement entry refuses alternative-ledger
    and input-overlay options at its maintained CLI boundary, including
    argparse abbreviations and equals forms, rather than relying on a
    reviewer to notice `overrides_used=true` after credit was calculated.
    Keep the underlying historical algorithm frozen; guard its current
    selector. Captured by round20 ResidualCurrentMonitor and the actual
    exit0/legacy/override red-before receipt in `lessons/round-20.md`.
    Falsifier: the same override argv changes from accepted exit0 to
    exit64/SELECTOR_OVERRIDE_FORBIDDEN, while ordinary strict/default
    measurements remain available. Public tests cover all three switches
    and their alternative spellings. This is invocation enforcement,
    not independent cold-read or producer authentication.

## Criteria appended — round 21 (2026-10-21)

43. Before a large wave, inspect live capacity and resolve the seat-role
    mix through the current primary routes. This lane's concentration guard
    refuses a primary provider share above0.40. The threshold is a policy
    choice motivated by round20's35/72 Codex deaths, not a measured capacity
    guarantee; fallback overlap and availability remain separate.
    Captured by `lessons/round-21.md` provider mistake.
    Falsifier: `tools/wave-route-mix.py --spec .ufo/waves/round-20/spec1.json`
    refuses exit1, while the round21 spec passes exit0; never replace a
    provider-dead seat or count its dispatch as completed work.
44. A frozen mutation population rechecks each exact anchor at its freeze
    revision before dispatch. A stale anchor is explicitly re-anchored to
    the same semantic edit with its historical rewrite named, never dropped
    from the denominator. Captured by R02's timeout-cap rewrite in
    `lessons/round-21.md`. Falsifier: the old round18 anchor is absent at
    08175c6, while the documented current positive-zero-boundary anchor
    occurs exactly once; deleting any anchor produces INCONCLUSIVE, not
    a kill. Round21's real baseline retains18/18 unique anchors.

## Criterion appended — round 22 (2026-10-21)

45. A seat-completion census binds each retained terminal callback to its
    original exact registered name, agent ID and role. A report is an
    orthogonal artifact, possibly partial; its presence or “done” prose
    never changes a failed callback to completed. Totals derive from the
    status vector, not directory file count. The retained callback snapshot
    and expected digest establish declared-input integrity, not provider
    authenticity. Captured by `lessons/round-22.md` partial-report mistake,
    preserved round21 outcome-accounting erratum. Falsifier: the digest-
    matching wrong-count bundle exits1/TOTAL_MISMATCH, while the identical
    statuses with corrected claimed totals exit0. The two failed-with-report
    identities remain failed in both runs; no dead identity is replaced.

## Criterion appended — round 23 (2026-10-21)

46. A finite required-command receipt claim freezes its requirement set
    before execution and matches each unique name to exact ordered argv,
    declared cwd/revision and typed expected outcomes in one retained
    observation. Output tokens or positive source-read counts cannot fill
    a missing command. Full-stream evidence is not reconstructed from a
    truncated tail. The caller-owned trusted commitment pins declarations,
    not producer authenticity. Captured by the historical R17-CMD-BIND
    overclaim (criterion33), and `lessons/round-23.md` Mistakes. Falsifier:
    an otherwise matching receipt with source-read argv fails1/ARGV_MISMATCH;
    deleting a required receipt fails1/MEMBERSHIP_MISMATCH; restoring only
    that field restores clean0. The new finite registry demonstration does
    not close historical full-page/coldread command coverage.

## Criterion appended — round 23 correction (2026-10-21)

47. Narrows criterion46; 46 stays unchanged. A command-binding gate binds the
    requirements declared inside its pinned bundle. The requirement set is
    frozen before execution only by the replay instrument's evidence-local
    digest/compile check, so cite that check separately. Receipt argv, cwd
    or revision copied by the instrument from what it executes are
    invocation parameters, not observations. A population verdict over such
    receipts tests only exit and stdout, so argv discrimination must cite a
    real substituted-command pair. Report rows that read live or external
    state separately from revision-pinned rows; never call such a replay an
    isolated clone. Captured by: `lessons/round-23.md` "Fresh falsification
    wave", Errata A–C (CorpusClaim, CwdDeclared, RevisionDeclared,
    MistakeRule). Falsifier: the retained source-read pair must still return
    1/ARGV_MISMATCH while the correct command returns 0; the 43-row replay
    cannot fail on argv by construction.

## Criterion appended — round 24 (2026-10-21)

48. A routed hardening gap does not count as repaired until a frozen predicate
    for it fails at the base revision and holds after the change.
    - The predicate must use the public detector: a selftest kill of a named
      mutant, a pinned registry row failing on a self-consistent substituted
      bundle, or a refusing CLI projection.
    - A gap already caught at the base, such as round23's any-token stdout
      mutant, stays in the denominator as a control. It does not count as a
      repair.
    - Superseding a registry row is append-only: `superseded` plus
      `superseded_by`, with a new active row.

    Captured by: `lessons/round-24.md` Mistakes (round23 routed defects, loss
    of all 20 wave-2 reviewers). Falsifier: the round24 ruler gives 1/11 at
    6a1821a and is expected to give 11/11 after the change.

## Criterion appended — round 24 fresh wave (2026-10-21)

QUALITY48 execution note: the round24 ruler was executed at c8c5b88: 11/11,
exit 0 (`.ufo/evidence/round-24/after.json`). K4 is the control, so ten
predicates moved. K7–K11 failed at base only because the tool was absent,
so they show a new capability, not a repair. The runner-digest fix has no
predicate, so under 48 it does not count as a repair (lesson Erratum I).

49. Narrows 48. A guard with several triggers is covered only when each
    trigger has its own single-trigger fixture. Several triggers means a
    disjunction, a per-row loop, a byte-versus-character choice, or an
    alias-resolution step. In a per-row fixture, the offending row comes
    after a clean row. A predicate whose one fixture sets every trigger at
    once counts once, for the conjunction only. Record each predicate's
    expected failing case or finding, not just "some failure".
    Captured by: `lessons/round-24.md` "Fresh wave 1", Erratum F (PredK7–K11,
    MutProject, MutPlan, MutFixtures). Falsifier: the remove-external
    mutant of `registry-replay.py` leaves frozen K10 discriminated while the
    tool selftest's single-trigger `external` case fails, so K10 alone is
    not coverage of either disjunct.

Round24 residual correction to 48/49 (ResQuality49): the execution note
explicitly narrows 48: absence of a tool is new capability, not repair.
Criterion 49 supplements QUALITY29's mutation requirement and QUALITY15's
right-reason requirement; it does not replace either. A loop-coverage claim
requires the offending element in both first and later positions among
clean elements (rows or tokens); a clean-then-offending case alone misses
last-wins mutants. Its trigger list is illustrative, not a complete taxonomy.
Sign, truthiness and case-fold weakenings remain open under QUALITY29.
Single-row external/non-hermetic tests discriminate M05/M06 in MutProject,
but do not satisfy this stronger loop-position condition. The frozen K10
still counts one conjunction fixture, not coverage of either disjunct.
No round24 fixture implements this corrected rule; the lesson's QUALITY49
fix is not claimed failure-backed. The already executed M05/M06 probes
motivate the rule, not a claim that the new rule has been operationalized.

50. Round 25. A claim that cites routed items (it says "routed by", or cites
    a closure, spot-check or `routed_not_executed` list) freezes a ledger of
    those items with its contract, before any seat. The ledger has one row
    per item of every cited routing source, quoted with its path:line or JSON
    pointer. Each row maps the item by identity to counted checks, or to a
    recorded decision: deferred with an owner, declined with a reason, or
    implemented without a check. Each counted check names its routed item, or
    is labelled author-added or control. Matching counts never stand in for
    matching items. An item that names an existing artifact ("re-run X", "in
    the ruler") maps to that artifact's exact population, or names each member
    it drops. With any item unmapped, the claim is worded covered/total of
    the source, never "the routed items". Narrows 12 and 48; replaces neither.
    Captured by: `lessons/round-24-verifier-spotcheck.md:34,37`;
    `lessons/round-24.md` Erratum I; round-25 seats QualityCriterion and
    C1Framing. Falsifier: round 24's eleven predicates against MANIFEST
    `rounds[421].notes` leave three closure items unmapped, so its
    "routed" qualifier fails; round 25's `c1-pins.py` refuses a disposition
    ledger with one of the 34 rows dropped (P3), shown in
    `lessons/round-25.md` `## After measurement`.

51. Round 26. A knowledge entry's `verified-at` line names the sha256 of the
    tool bytes it vouches for, the lane revision of the run, and a committed
    receipt of that run; when the tool changes after the line is written
    (a later amendment, a new leg), the line is refreshed in the same landing
    and the superseded run is named, not silently dropped. An earlier seat run
    never stands for the measured tool. Captured by:
    `lessons/round-25-verifier-spotcheck.md:197-199` (routed item 3: the line
    named the `09dc114` run, tool `8c24255c…`, selftest 16/16, while the
    measured tool was `8269b82f…` with 17/17). Falsifier:
    `.ufo/evidence/round-26/c2-measure.py` item R25-SPOT-3 reads MISMATCH at
    base `d4140796` (`.ufo/evidence/round-26/c2-before.stdout`) and RESOLVED
    only when the named sha prefixes the tool at the revision and a named
    `.stdout` receipt carries the selftest count. Bound (round-26 seat
    CriticC2): the receipt check does not tie a receipt to the tool bytes
    that produced it.

52. Round 26. Every wave context names `jj` next to git: no seat runs any
    `jj` command (not `jj log`, not `jj st`), at the fleet root, in the lane
    or in a clone, because by default every jj command snapshots a colocated
    working copy and imports git refs. A registry row's `source` uses the
    enforced `<file>@<rev>:<line>` form before it lands; a prose source makes
    `tools/registry-check.py` refuse the whole registry. Captured by:
    `lessons/round-25.md:83` and `round-25-verifier-spotcheck.md:204-205`
    (seats ReReplay14 and ReOutputComplete); round-26 seat RegistryCheck.
    Falsifier: the round-25 wave context (`.ufo/waves/round-25/spec.json`,
    key `context`) names only "mutating jj" in the lane, which this rule
    rejects, while the round-26 contexts (`spec-w1.json`, `spec-w2.json`)
    pass; `registry-check.py --rev a08e85c` exits 2,
    `could-not-evaluate (registry invalid: rows[54].source must be
    <file>@<7-40 hex rev>:<line> …)` (`.ufo/waves/round-26/w1/RegistryCheck.md`).

53. Round 27. A round that edits a file traced as an input of a credited
    cold-read section either has those sections cold-read again by
    independent seats at its content revision before it lands, or declares
    calibration harmed among its measured results. A calibration no-harm
    reading names the strict monitor at the landed head, never an earlier
    revision. Captured by: `lessons/round-26-verifier-spotcheck.md:112-135`
    (62/62, restraint 8 at base → 25/64, restraint 6 at head, while the
    measured table read "numeric 8 → 8"). Falsifier:
    `.ufo/evidence/round-27/c1-measure.py` exits 1 with `box3_mismatch=1` at
    `e08444d3` and at round-27 base `91edf9cd`
    (`.ufo/evidence/round-27/c1-before.stdout`).

54. Round 27. A counter that accepts a run receipt checks that the receipt
    names the sha256 of the tool bytes and of the input bytes at the measured
    revision; a receipt from other bytes counts as absent. Captured by:
    `lessons/round-26-verifier-spotcheck.md:225-228` (routed item 4: the
    round-26 C2 receipt check did not tie a receipt to the tool bytes; seat
    MutateC2Counter). Falsifier: `.ufo/evidence/round-27/c2-measure.py`
    prints `receipt not bound to probe and anchors bytes` and exits 1 when
    `anchor-probe.py` or `anchors.json` differs from the bytes the receipt
    names.

55. Round 29. Amendments to 53 and 54 (round-27 spot-check routed item 5,
    seat ReviewQuality, `.ufo/waves/round-27/w1/ReviewQuality.md`
    H1, M1, M2, L2). Criterion 53 uses the crediting-entry reading: a round
    re-reads a section when it edits an input of the entry that credits that
    section; entries that already fail are not measured. Independence of the
    re-reading seats is checked by reading each new entry's `seats` and
    `reports` against the committed wave roster, not by the monitor; from
    round 29 the claim counter checks that binding
    (`.ufo/evidence/round-29/c1-measure.py`). External inputs are recorded,
    not measured. For 54: naming a digest is not provenance; a claim that a
    run happened needs a re-run at the measured revision, by the counter or
    through a result digest the counter recomputes. Falsifier: the round-27
    C2 receipt check passes a receipt whose digest was rewritten to the
    current probe (ReviewQuality M1).

56. Round 29. Every edit a round makes to a widely read lane file
    (corpus/SOURCES.md, corpus/README.md, corpus/QUALITY.md, SHONEN.md)
    lands in or before the content revision its cold reads target; after
    that revision the round only adds new files or appends to SCORECARD.md,
    LOG.md, its own lesson and the cold-read ledger. Captured by:
    `lessons/round-28.md` Mistake 1 and `round-28-verifier-spotcheck.md`
    routed item 1. Falsifier: `.ufo/evidence/round-28/append-probe.txt`
    (one blank line appended to corpus/SOURCES.md drops 60 → 50 credited
    sections at round-28 base).

57. Round 29. A round closes against one lane head: the fleet report names
    the final lane head, and no lane commit lands and no fleet report is
    rewritten after the report is filed. Check: `git log --oneline
    <report-named head>..<lane branch>` prints nothing when the closure
    starts. Captured by: `round-28-verifier-spotcheck.md` routed item 3.
    Falsifier: round 28 filed against `1076914a`, then landed `41da22a3`
    and `1dde85f3` and rewrote the report `2012146` → `38ae0ff`, so the
    check prints two commits.

## Criteria appended — round 30 (2026-10-23)

Routed by `lessons/round-29-verifier-spotcheck.md` (routed items 1–7; 5(c)
and item 7's S059 and MutateLegSum carry-overs are work assignments, not
criteria), `lessons/round-29.md` Mistakes 1, 4 and 5, and round-30 controls.

58. Round 30. A required control whose seat is refused or dies blocks the
    data wave until another control of the same class is built and scored,
    by another seat or by the L1, which records which one built it. The
    refused seat's task is never resent. A claim whose contract names a
    shortcut control class with no scored receipt is declared exploratory
    before data, or it does not dispatch. Captured by: spot-check routed
    item 1. Falsifier: round 29 `contract.json` lists the class "shortcut
    keyed on ids or labels", and `.ufo/waves/round-29/ctl/` holds no scored
    receipt for it. CtlC1Shortcut and CtlC2Shortcut were refused, and wave 1
    dispatched anyway. The refusal holds are recorded in
    `.ufo/waves/round-29/res/ReviewControls.md`.

59. Round 30. Data dispatches only after every control report file is
    present at its path, or its seat is recorded dead with its error text
    after a final check of that path. A seat's status is not that check.
    The control receipts are committed in a lane commit that precedes the
    data-wave spec commit. Mtimes are not the ordering proof. Captured by:
    spot-check routed items 4 and 7 (Mistake 1).
    Falsifier: `.ufo/evidence/round-30/r29-mistake1-ordering.txt`, committed
    in the same lane commit as this criterion.
    `CriticC2v2.md` mtime 22:33:57-03 is after `task-adapter-w1.json`
    22:27:45-03, and both first landed together in `bc2058a4`, so no
    committed order existed.

60. Round 30. Every appended cold-read entry carries a binding to an
    artifact outside the report. The round's binding receipt names the
    registry member, its agent id and its host session transcript path
    with sha256, so a closure checks it without a session search. Any
    binding check is run on one real assembled entry before it is frozen.
    The wave context fixes `seat` to the registry name. Captured by:
    spot-check routed items 2 and 3 (Mistake 5). Falsifier:
    `.ufo/evidence/round-29/coldread/select-receipt-w1.json` lists 10
    entries excluded on assembler shape alone (assembler verdict
    normalization, report `executed-ok` vs entry `gap-minor`, and seat
    self-labels such as `TameshiR29.Read08A`), every report verdict a
    passing class.

61. Round 30. Every wave context carries both rules: absolute lane paths for
    every `Report:` trailer, and "never kill a process you did not start;
    check /proc/<pid>/cwd first". Before assembly, the report files present
    are compared with the registry members that returned, and any gap
    triggers the misroot sweep. Captured by: spot-check routed items 5(a)
    and 5(b) (Mistakes 3 and 4). Falsifier: round 29 `spec-w1.json`
    `context` lacks the never-kill sentence (BuildF6B killed BuildF6A's
    PID 2758108), and `lessons/round-29.md` Mistake 3 records Read10C's
    report written at the fleet root and moved byte-exact (sha256
    `fafd4c36…`).

62. Round 30. A report names a revision as measured only if a counter
    receipt for that revision is committed. A value that appears in no
    committed receipt is not reported. A value carried from an
    input-identical revision is labelled as inferred. Captured by:
    spot-check routed item 6. Falsifier: the round-29 report gives C2
    `quote_located=1` and names three head commits, while the only C2 head
    receipt, `.ufo/evidence/round-29/c2-at-E.stdout` (measured rev
    `7a45f7b9`, committed at `9bb699ad`), reads `quote_located=0`, and no C2
    receipt is committed for `6892c3ee`, `1a1e8b22` or `3c16b3a6`.

63. Round 30. Before a round edits a widely read lane file or tool, it
    measures that edit's cold-read drift on a sandbox commit and plans the
    re-reads in the same round. If the round cannot staff the re-reads, it
    does not make the edit. Captured by: QUALITY 56 as applied in round 29
    (the widely read edits landed at `9f3084bc` and dropped the monitor to
    52/64 before the re-reads were staffed). Falsifier:
    `.ufo/evidence/round-30/drift-sim-union4.txt`: one comment line
    appended to each of SOURCES, QUALITY, README and the runner drops
    64 → 33 credited sections (`rev=daa11583`), against 52 with the three
    file edits and no runner edit (`.ufo/evidence/round-29/c1-at-A.stdout`,
    rev `9f3084bc`).

64. Round 30. A counter that drives a program under test gives every judged
    run the same observable identity: no run learns its job label, class or
    role (pristine, drop, held-out, sealed, equivalent) from its working
    directory or name, argv, environment, stdin, a file it can read, or the
    /proc entry of its parent. Before data, a control keyed on job identity
    is scored against the frozen counter and must not pass. Captured by:
    control K9 against the round-30 v4 draft counter. Falsifier:
    `.ufo/evidence/round-30/v4/c1-measure-v4-draft.py` ran each `--selftest`
    in a directory named after its job (`st-<job>`), and
    `.ufo/evidence/round-30/v4/K9-on-draft.stdout` reads `PREDICATE:
    C1_R30_PASS=true`, while the same control on the frozen counter
    (`.ufo/evidence/round-30/v4/K9.stdout`) reads `PREDICATE:
    C1_R30_PASS=false`.

65. Round 30. A counter that scores only verdicts (kills and accepted
    rewrites) cannot tell a program that runs the judged code from one that
    models it correctly. A claim whose property is "runs the code" names a
    measure that a correct static model fails, or it is exploratory and the
    property is checked by reading the code. Captured by: control
    CtlS2SymEval. Falsifier: `.ufo/evidence/round-30/v4/ctl2/CtlS2SymEval-v4.stdout`
    reads `sealed_killed=6/6 sealed_equiv=6/6` and `PREDICATE:
    C1_R30_PASS=true` for a selftest that never runs bash on the block
    (`.ufo/evidence/round-30/wA/CtlS2SymEval-11.diff`), which forced
    `.ufo/evidence/round-30/contract-amendment-4.json`.

## Criteria appended — round 31 (2026-10-23)

Routed by `lessons/round-30-verifier-spotcheck.md` (Conformance defects and routed defects 1–5) and `lessons/round-30.md` Mistakes 2, 4 and 5. Criteria 1–65 remain unchanged.

66. Round 31. A seat dispatched by this lane remains part of the lane and is
    not described as a non-author or independent reviewer of that lane's work.
    A different seat name or report does not change dispatch provenance; its
    report may support the lane's ruling but cannot supply the non-author
    ruling. Captured by: `lessons/round-30-verifier-spotcheck.md:40-43`
    (LEARNING.md §Discernment and AXES.md quotes). Falsifier:
    `.ufo/waves/round-30/wC/JudgeC1.md:3` calls JudgeC1's review
    "Non-author"; `SCORECARD.md:1473` calls it a "named non-author seat"
    although the spot-check records that the L1 dispatched JudgeC1.

67. Round 31. Every seat invocation of `--regression` passes `--workdir`
    with a directory beneath that seat's own scratch directory. Before any
    process is killed, the seat checks `/proc/<pid>/cwd` and verifies that it
    resolves beneath that seat's own scratch; a process the seat did not start
    is never killed. Captured by: `lessons/round-30.md:169-182` (Mistake 5).
    Falsifier: `.ufo/waves/round-30/wC/ColdA01.md:45` records
    `timeout 240 bash tools/mutate-and-run.sh --regression --keep` without a
    `--workdir`; `ColdA01.md:100` discloses killing sibling processes with a
    broad `pgrep`/kill.

68. Round 31. Before any re-dispatch after a seat is dead or has no report,
    a committed check lists every dead seat for the round and compares each
    dead seat's task text with each proposed item. The check records the
    comparison and disposition; an item measuring the same object is not
    dispatched again. A name match triggers comparison but does not replace
    the task-text comparison. Captured by: `lessons/round-30.md:159-168`
    (Mistake 4). Falsifier: `.ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt:7-10`
    lists ConnectorOverlap among the dead seats, while
    `.ufo/waves/round-30/spec-wC.json:279-284` includes an item of that name;
    `lessons/round-30.md:164-168` records that no overlap check ran before
    dispatch.

69. Round 31. The binding conditions for a data wave are frozen as executable
    code before data dispatch, and the frozen code is scored against the
    required controls before data. A post-data audit may add findings but
    cannot supply, change or retroactively satisfy a binding condition.
    Captured by: `lessons/round-30.md:69-73,213` (Mistake 2 and routed
    binding v4). Falsifier: `.ufo/evidence/round-30/coldread/bind-select-v3.py:2-10`
    freezes a selector that lacks the stricter conditions implemented by the
    separate post-data audit `.ufo/evidence/round-30/coldread/audit-bound-wC.py:2-9`.

70. Round 31. A line-range citation to a paragraph names all and only the
    lines containing that paragraph; it excludes adjacent blank lines and a
    following heading. A one-line paragraph is cited as one line. Captured by:
    `lessons/round-30-verifier-spotcheck.md:44-45`. Falsifier:
    `lessons/round-30.md:59` cites the S094 paragraph as `:60-62`, although
    the paragraph is line 60, line 61 is blank, and line 62 is `## Limits`.

## Errata — round 30 QUALITY imprecisions (append-only; 2026-10-23)

These errata qualify the prior text; they do not rewrite it.

- **F1 — criterion 60 (`corpus/QUALITY.md:683-688`).** The Falsifier's
  normalization example is incomplete. Read “report `executed-ok` vs entry
  `gap-minor`” as “reports `executed-ok` and `verified-record` normalized to
  entry `gap-minor`.” The second observed pair is `verified-record` to
  `gap-minor` (`.ufo/waves/round-30/wC/ReviewQualityR30.md:22-29`); the
  claim that the excluded entry verdicts are passing classes is unchanged.
- **F2 — round-30 routing preamble (`corpus/QUALITY.md:649-651`).** Its
  mistake list is incomplete. Read “Mistakes 1, 4 and 5” as “Mistakes 1, 3,
  4 and 5”; criterion 61 itself routes Mistakes 3 and 4
  (`ReviewQualityR30.md:35-43`).
- **F3 — criterion 62 Falsifier (`corpus/QUALITY.md:705-709`).** “The only
  C2 head receipt” overstates the revision measured by
  `c2-at-E.stdout` (`7a45f7b9`, committed at `9bb699ad`). Read it as “the
  only committed C2 counter receipt”; the receipt is not a head receipt, and
  no receipt is committed for the three named head commits
  (`ReviewQualityR30.md:45-56`).
- **F4 — criterion 63 Falsifier (`corpus/QUALITY.md:716-721`).** The
  committed `drift-sim-union4.txt` reports `covered=33/64` at
  `rev=daa11583`; `contract.json:45` records the four-file comment-line
  sandbox recipe. The sandbox revision is not an object in the lane
  repository, so the receipt establishes its printed output, not an
  independently re-checkable construction. The 64/64 base and 52/64 earlier
  readings are separately recorded by `monitor-at-base.stdout` and
  `.ufo/evidence/round-29/c1-at-A.stdout`. Retain the recipe only as
  contract-reported context, not as verified construction evidence
  (`ReviewQualityR30.md:58-71`).

## Criterion appended — round 31 claim C1 (2026-10-23)

71. Round 31. A standing SCORECARD row that quotes a command's output
    (a capability row's selftest tally, a score row) is a claim about a
    named revision. When the quoted tool changes, the lane appends a new
    row that states the values the command prints at a named revision;
    a prose line that "supersedes" counts is itself a standing statement
    and goes stale the same way. Captured by: the round-31 C1 counter
    (`.ufo/evidence/round-31/c1-measure.py`). Falsifier:
    `.ufo/evidence/round-31/before/c1-at-base.stdout` reads
    `mismatches=7` at `36c1d393` (runner 80/80 stated, 106/106 printed;
    regression 6 legs stated, 9 printed), and the round-17 supersession
    line `SCORECARD.md:632-636` states runner 95/95, regression 7 and
    evidence-disposition 56/56, all three stale at the same revision.

72. Round 36. A LOG.md entry that names a file as evidence must name a
    file that exists at write time: the citation is re-resolved (path or
    `git log --all -- <path>`) before the entry commits, and a pointer to
    a never-committed artifact is corrected by an append-only entry naming
    the real artifact, never silently repaired. Captured by: the r35
    closure's step-1 pointer sweep (`lessons/round-35-verifier-spotcheck.md`,
    routed defect 1) — no in-lane criterion caught it at r35 write time.
    Falsifier: `LOG.md` round-35 entry named `ResidualSentinelClosure.md`,
    which `git log --all -- '*ResidualSentinelClosure*'` shows was never
    committed; the round-36 entry corrects it naming the five real
    residual reports.

## Criteria appended — round 37 (2026-10-24)

73. Round 37. A mutant control that redirects a frozen counter to a committed
    alternate input names and verifies the counter revision, input-tree identity,
    and explicit control mode when the counter supports one. A scratch-only mutant
    revision or a `mode=deciding` label is not a closure-resolvable control.
    Captured by: the r36 verifier spot-check's routed empty-panel defect and the
    r36 W2 C2 mode-label review; `corpus/lessons/round-37.md`, Mistakes 1 and 4.
    Falsifier: `.ufo/evidence/round-37/calibration/before-final-control.stdout`
    reads `unresolved_control_inputs=1`; the earlier replay receipt reports
    `mode=deciding`; the committed manifest + explicit-control replay +
    `after-control-final.stdout` must re-derive zero and `mode=control`.

74. Round 37. A Bash `code_view` claim names each supported quoting form. ANSI-C
    `$'...'` handling preserves escaped single quotes, blanks a following comment,
    and preserves `#` inside the quoted string; this finite support does not imply
    a full Bash lexer. Captured by: `corpus/lessons/round-37.md`, Mistake 2, and
    source S104. Falsifier:
    `.ufo/evidence/round-37/code-view/before.stdout` reads the escaped-quote case
    FAIL with the old scanner; the committed tool's same counter must read both
    fixtures PASS, and removing the ANSI-C state must make the escaped-quote
    case fail.

75. Round 37. A scorecard statement labeled `measured` is backed by an observed
    output at or before the revision it names; until that output exists, record
    the value as a target. A later receipt cannot retroactively make an earlier
    commit's sentence a measurement. Captured by: the round-36 `Numeric axes,
    measured` paragraph at content revision `e423c41b` (`SCORECARD.md` R36
    erratum) and `corpus/lessons/round-37.md`, Additional record corrections.
    Falsifier: `git show e423c41ba253357ab8c8513f0376dad9d38ab248:SCORECARD.md`
    contains the 8/64-64 statement, while its after receipt is at
    `b455001e2589b3f4f471d94a3de7e5e549b9f54c`.

Correction note (round 37, append-only; found by wave-1 seat ReviewQualityCriterion):
criterion 73's falsifier names `.ufo/evidence/round-37/calibration/before-final-control.stdout`
for the `unresolved_control_inputs=1` before-state — correct — but its `mode=control`
requirement is evidenced by `.ufo/evidence/round-37/control/replay-at-final-control.stdout`
(not by any calibration/ receipt, which carries no mode label). Read the falsifier as:
before-state = `calibration/before-final-control.stdout`; control-mode state =
`control/replay-at-final-control.stdout` (`mode=control`, v1 PASS / v2 FAIL); after-state =
`calibration/after-control-final.stdout` (`unresolved_control_inputs=0`). Also: criterion
74's anti-hardcoding clause ("removing the ANSI-C state must make the escaped-quote case
fail") gained a committed falsifier path at `.ufo/evidence/round-37/mutation/` (branch-removal
mutant receipt; the gap the same seat named is closed).

### Criterion 76 — a standing self-assessment row must state what the committed tree holds

A standing SCORECARD row that states a count of committed bytes (the sources-registry row
count) is a claim about the repo and must equal what the committed tree holds at every
deciding run; a stale count is a self-assessment mismatch, not a dated restatement.
Lesson: `corpus/lessons/round-38.md` `## Mistakes` row 1 (the standing row said 99 rows
while `corpus/SOURCES.md` held 101).
Falsifier that must fail: the frozen counter
`python3 .ufo/evidence/round-35/c2/c2-measure.py --lane LANE --rev REV --fleet /home/vgpnk/Projects/shokunin`
must print `m6=1 ... C2_R35_PASS=false` and exit 1 when the standing row's count is one off
the committed registry (receipt: `.ufo/evidence/round-38/calibration/before-at-base.stdout`,
which carries exactly that mismatch).

### Criterion 77 — a seat report belongs in the lane repo, and a lane that claims it must carry it

A seat's report is lane evidence: it is written under the lane's own wave directory, and a
lane's own count of its residual reports must match the files that are actually committed
there. A seat file found at the fleet root is misrooted output and is neither committed nor
counted until it is copied byte-exact into the lane repo (cmp-verified) and the fleet-root
copy is deleted.
Lesson: `corpus/lessons/round-38.md` `## Mistakes` row 2 (the round-37 residual report
`ResCorrections.md` was stranded at the fleet root, so the lane's claim of six residual
reports did not match its five committed files).
Falsifier that must fail: the same frozen counter must print `m3=1 ... C2_R35_PASS=false`
and exit 1 while a tameshi-attributable untracked file remains under the fleet root's
`.ufo/waves/` tree, and `m3=0` once the file is committed into the lane and the fleet copy
is gone (before receipt: `.ufo/evidence/round-38/calibration/before-at-base.stdout`).

### Criterion 78 — a wave parent that exits before seat terminals is unsettled

A dispatched wave is settled only when every seat has a terminal timestamp and the
dispatcher parent exit is at or after the latest of those timestamps. A parent that
exits while seats are still running is unsettled, even if the parent process itself
exits 0. Prepared specs are not dispatched seats. Dead seats are not replaced.
Lesson: `corpus/lessons/round-39.md` (the round-38 parent-exit, and
`considerthese/2026-10-24.md` proposal 4, mined 2026-10-24, not edited).
Falsifier that must fail: `python3 tools/wave-parent-settle.py --selftest` must fail
if the red fixture (parent_exit_unix=10, seat terminal_unix=20) is classified SETTLED.
The committed selftest classifies that receipt UNSETTLED and exits 0 only because the
tool's own check expects UNSETTLED.

### Criterion 79 — a located quote needs a committed snapshot

A mined row that presents a located quote as support is not citable until a
committed snapshot contains that quote. A live fetch that cannot be repeated,
or a page whose quote is split by markup, is not a substitute for the bytes.
Unreachable is not fabrication: the quote is unverifiable until the snapshot
lands. A status edit does not replace the snapshot.
Lesson: `corpus/lessons/round-40.md`, and `considerthese/2026-10-24.md`
proposal 3, mined 2026-10-24, not edited. The reflection pointed at repeatedly
unreachable sources and suggested pinned alternatives; the evidence is the
round-39 closure's redirect-loop on S108 and the snapshot pinned this round.
The pointer was opened, not paraphrased: `https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html`
— the class of address the proposal names — timed out again on 2026-10-24 (no
response in 40 s), while the lane's existing pinned alternative for that family
is the raw upstream source (`S097`, `S104`, cgit raw `doc/bashref.texi`).
This criterion generalises that practice to every mined quote.
Falsifier that must fail: `python3 .ufo/evidence/round-40/s108/measure.py
--lane LANE --rev 304e3355705640af2879c772fc9a5c2902c61763` prints
`snapshot_absent=1 C2_R40_PASS=false` and exits 1. The same command at
`5641ed84c8dc148c34c8dd83f062279ddf06b4af` prints `quote_in_snapshot=1
stripped_quote_fails=1 C2_R40_PASS=true`. Removing the prefix
`可以通过使用参数` from a copy of the snapshot must make the quote check fail.

### Criterion 80 — name the pins a tool edit breaks, before the edit

A round that changes a tool's or a counter's bytes must record, before the edit lands,
which pins that change breaks: every frozen contract field carrying the old digest
(`tool_sha256`, `fixtures_sha256`, a counter's `TOOL_SHA256` constant), every capability
row whose evidence pointer quotes a digest, and every registry anchor cell that carries
one. The record names the old and the new digest per pin — a table a reader can check, not
a sentence. An edit that lands first and inventories afterwards is a blast radius
discovered, not declared.
Lesson: `corpus/lessons/round-41.md`. The positive shape is the round-41 contract's
`amendments` array: one entry per change with `frozen_field`, `old_sha256`, `new_sha256`
and `before_data`. Source of the reflection: `considerthese/2026-10-24.md` proposal 1
(pin blast-radius report before a tool edit), mined 2026-10-25, not edited. It points at
the round-36 deferral, where one tool fix was held back because three pins depended on it.
Measured blast radius, as an example rather than a rule: `tools/tally-audit-v3.py` at
`a3d6c690` is pinned by `.ufo/evidence/round-35/c1/c1-measure.py` (its `TOOL_SHA256`),
the round-35 contract and its amendments, `c1-measure-v2.py`, `replay-empty-panel.py`,
and two capability rows in `SCORECARD.md` whose digest is truncated to 16 hex characters
— a full-digest grep misses those two, which is the point of writing the radius down.
Falsifier that must fail (run from the lane; a 0 means the pin still matches, a non-zero
means the pin chain is torn at that revision):

```
test "$(git -C LANE show 691bb51:tools/tally-audit-v3.py | sha256sum | cut -d' ' -f1)" \
   = "$(git -C LANE show 691bb51:.ufo/evidence/round-35/c1/c1-measure.py \
        | sed -n "s/^TOOL_SHA256 = '\([0-9a-f]\{64\}\)'.*/\1/p")"
```

Observed: `d16f9b5` exit 0, `691bb51` exit 1 (tool `6188db16…`, pin `ef98fc53…` — the A7
re-pin that left the counter constant behind), `5829676` exit 0 (A8 repaired it). The
criterion is met only by a round that names such a break before it makes one.

## Criteria appended — round 42 (2026-10-25)

### Criterion 81 — a presence receipt is written after the writes it describes, or superseded

A committed receipt that asserts a file's presence or absence (`present`, `report_exists`)
is a self-assessment record. It is written after the last write it describes. When the
tree later contradicts it, the fix is an appended superseding receipt. That receipt names
the old one in `supersedes`, re-asserts every path the old one asserted, and agrees with
the tree on each. It is not an in-place rewrite of closed-round evidence. A receipt that
the tree contradicts and that nothing supersedes is a calibration mismatch, whatever
the round report says about it.
Lesson: `corpus/lessons/round-42.md`. The live instance was the round-41 residual
receipt: `present: false` for `ResidualReceipts.md`, written before that report landed.
The round-42 C1 counter's m10 class audits `present` assertions under `.ufo/waves/`. Its
known limits are recorded in the lesson: it reads presence by path only, so an empty file
satisfies it, and it does not read other key names such as `report_exists`.
Falsifier that must fail (from the lane; prints `C1_R42_PASS=false` and exits 1 at the
base, where the stale receipt is not yet superseded):

```
python3 .ufo/evidence/round-42/calibration/measure.py --lane LANE \
  --rev c77c2b7e64d2e356381441ecf94abac03e984606 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f
```

### Criterion 82 — a kill is a completed run with a failed check; a crash is not a kill

When the lane mutates its own tools, a mutant counts as killed only when the run finishes
with parseable output and at least one declared check fails. A non-zero exit, a Traceback
or unparseable output is a run error and does not count as a kill. A run with no failing
check is a survivor. This is the lane's own verdict rule (`SKILL.md:208-209`: a crash
before the summary is Inconclusive, not a kill) and Stryker's (S001: Runtime error "is not
represented in your mutation score"). PIT differs: its code scores `RUN_ERROR` as detected
(S158, `corpus/knowledge/pit-outcome-vocabulary.md`). A kill oracle that cites a tool must
cite the tool whose rule it actually follows, and a kill count must say which oracle
produced it.
Lesson: `corpus/lessons/round-42.md`. The round-42 contract's first wording cited PIT
and Stryker together for this rule. A wave-1 critic opened PIT's source and found the PIT
half false. The citation is corrected in the contract's post-freeze amendments; the
pinned counter bytes are not edited.
Falsifier that must fail (from the lane; a tool that crashes on every input must print
`probe_outcome=runtime_error`, never `killed`; the probe file is the wave-1 executor's,
re-created by the command):

```
printf 'raise SystemExit("crash")\n' > /tmp/crash-probe.py
python3 .ufo/evidence/round-42/census/measure.py --lane LANE \
  --rev 322b5cd32b4319a05340d249ae752d12a9e6b19f --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f \
  --probe-mutant /tmp/crash-probe.py
```
