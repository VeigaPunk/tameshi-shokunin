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
