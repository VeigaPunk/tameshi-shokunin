# Round 36 w1 — ReviewLogCorrection (LOG dead-pointer correction)

Seat: leaf reviewer, `ReviewLogCorrection`. Read-only on the lane; no production edits.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
Tip at review: `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (`git rev-parse HEAD`).
Correction commit: `e423c41ba253357ab8c8513f0376dad9d38ab248` ("round-36: content — LOG dead-pointer
correction + round-36 entry, …"). r35 record commit: `5df962b`; r35 tip: `796e08b`.
Tool installs: none (no `uv`, `npx`, release binary, or package-manager action was needed).
Methods: git plumbing over committed bytes and text search. No LSP device is mounted in this seat
(`read xd://lsp` → `No such tool: xd://lsp. Mounted devices: ast_edit, debug`), so no server-backed
`references`/`definition`/`diagnostics` pass was possible; every citation below is git evidence or a
literal text search, and is labelled as such. Markdown prose and git object graphs have no LSP
server in this lane regardless.

## What I attacked

The round-36 correction block at `LOG.md:1900-1908`, the round-35 sentence it corrects
(`LOG.md:1892-1893`), the residual-report set it enumerates, and `corpus/QUALITY.md` criterion 72
(`corpus/QUALITY.md:846-856`, appended by `e423c41`, `12 0` numstat = 12 insertions / 0 deletions).

## Check verdicts

### (a) The round-35 `ResidualSentinelClosure.md` sentence exists as quoted — PASS

```
python3  # exact substring test over LOG.md:1820-1895 vs the first quoted span at LOG.md:1900-1908
quoted spans: 5
span0 verbatim in r35: True
span0 normalized in r35(norm): True
1893 '  (`ResidualSentinelClosure.md`).'
```
The correction quotes `was respawned by the closure\n  (`ResidualSentinelClosure.md`)`
(`LOG.md:1901-1902`) as an exact substring, including the two-space continuation indent; no
whitespace normalization was required. The source sentence (`LOG.md:1892-1893`) reads: "the residual
sentinel seat left no report and was respawned by the closure (`ResidualSentinelClosure.md`)."
The quote is a partial quotation of the predicate and is framed as such ("its waves paragraph
says … "); only the sentence-final period is omitted, which is normal punctuation practice, not a
misquote. The sentence is inside the `- Waves:` bullet, as the correction states.

### (b) `git log --all -- '*ResidualSentinelClosure*'` is empty — PASS

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git log --all -- '*ResidualSentinelClosure*'      # no output, exit 0
git log --all -- '*ResidualSentinel*'             # no output, exit 0 (broader glob, the lesson's form)
git rev-list --objects --all | grep -i 'sentinelclosure'   # no output
find . -iname '*residualsentinel*' -not -path './.git/*'   # no output (includes ignored/untracked)
find .git -name '*ResidualSentinel*'                       # no output
git fsck --unreachable --no-reflogs                        # 8 unreachable commits; each ls-tree scanned → no match
```
Absence holds for the working tree, every reachable tree in every ref, every object path ever
committed, and the 8 dangling commits. The correction's "No such file exists anywhere in the lane"
(`LOG.md:1902`) is accurate.

### (c) The correction names exactly the five residual reports on disk — PASS

```
python3  # set compare: backticked Residual*.md names at LOG.md:1900-1908 vs .ufo/waves/round-35/residual
named: [ResidualCriticPredicate.md, ResidualReviewC2.md, ResidualReviewReceipt.md,
        ResidualReviewSealed.md, ResidualScoutRecords.md, ResidualSentinelClosure.md]
disk : [5 names]   git@e423c41: [5 names, identical]
missing from correction: []      extra in correction: ['ResidualSentinelClosure.md']
```
The affirmative enumeration (`LOG.md:1904-1905`) is set-equal to the directory at the correction's
write commit (`git ls-tree -r --name-only e423c41 -- .ufo/waves/round-35/residual/`), at the r35 tip
`796e08b`, and at the review tip — five files, all committed, no untracked residue (`git status
--porcelain -- .ufo/waves/round-35/residual/` empty). The sixth backticked token is the dead name
itself, occurring twice and correctly: inside the quotation (`LOG.md:1902`) and inside the
`git log` glob (`LOG.md:1903`). "the five committed reports" is exact.

Corroboration of "the sentinel seat left no report": the r35 waves text describes a 6-seat residual
wave (2 reviewers, 1 critic, 1 sentinel, 1 scout, 1 reviewer on C2) at `LOG.md:1888-1889`; the
residual dir holds the five non-sentinel seats (`grep -h 'SEAT:' residual/*.md` → CriticPredicate,
ReviewC2, ReviewReceipt, ReviewSealed, ScoutRecords). The sentinel is the missing sixth.

### (d) `QUALITY.md` criterion 72 cites this lesson — PASS on substance, with two citation-precision defects

The criterion exists at the tip (`corpus/QUALITY.md:846-856`; 72 criteria total, appended last,
`12 0` numstat). Its rule ("must name a file that exists at write time: the citation is re-resolved
(path or `git log --all -- <path>`) before the entry commits") and its falsifier (the r35 dead
pointer, the empty `git log` result, the round-36 correction naming five reports) are both
reproducible and true — I reproduced each. It cites the lesson that captured the defect
(`lessons/round-35-verifier-spotcheck.md`, routed defect 1), which states exactly:
"LOG.md round-35 entry cites `ResidualSentinelClosure.md` … no such file exists anywhere in the lane
… Commit the file or append a correction naming the real artifact" (`:75`). So the assignment's
check holds if "this lesson" means the routing lesson.

It does **not** cite `corpus/lessons/round-36.md`, where this round files the mistake class
(`## Mistakes`, "class: reference-drift", `:53-64`). Two precision defects follow (MINOR, MINOR
below); neither breaks the rule.

## Findings

### MINOR-1 — The redirect clause attributes sentinel findings to a file that does not carry them

`LOG.md:1906-1907`: "the predicate findings the sentence points at are carried by
`ResidualCriticPredicate.md`".

- `grep -in 'sentinel' .ufo/waves/round-35/residual/*.md` → **no matches in any of the five**,
  including `ResidualCriticPredicate.md`.
- The corrected sentence names no predicate findings. `grep -in 'predicate'` over the r35 entry
  region hits only `LOG.md:1832` (`predicate_pass=false) — 9dd3174c`), which is about the C1
  receipt, not the sentinel clause at `:1892-1893`. The correction's "the sentence points at" has
  no referent in the quoted text.
- `ResidualCriticPredicate.md` is a different, independent advisory seat
  (`SEAT: ResidualCriticPredicate model=openai-codex/gpt-6.1-sol`); its contents are the counter
  PASS predicate (`c1-measure.py:517`, MAJOR 1), stale control prose (MINOR 2), retained-receipt
  cardinality (NOTE 3), `code_view` ANSI-C lexing (MAJOR 4), and a no-credit note (NOTE 5). It
  contains nothing about the sentinel seat, a respawn, or a closure.

Effect: the dead pointer is gone and the five real artifacts are named, but the replacement adds a
provenance link that the target file does not support; a reader can infer the sentinel's findings
survive in `ResidualCriticPredicate.md` when the truthful statement is that the sentinel left no
report and its findings are unrecoverable. Smallest correction (future append, never an in-place
edit): say that the sentinel seat's own findings are unrecoverable, and keep the five-report
enumeration separate from any claim about what the missing file would have carried.

### MINOR-2 — Criterion 72 misnames the capture site as a "step-1 pointer sweep"

`corpus/QUALITY.md:850-852`: "Captured by: the r35 closure's step-1 pointer sweep
(`lessons/round-35-verifier-spotcheck.md`, routed defect 1)".

The cited lesson contradicts the label:
- `corpus/lessons/round-35-verifier-spotcheck.md:8-19` is `## Step-1 conformance`, and records
  "Defects named (status-neutral): **none at step 1**." Its step-1 rows are report identity, SHONEN
  heading/pointers, cited commit ancestry, clean tree, prompt contract, marker test — the LOG
  evidence pointer is not among them.
- The defect is filed at `:73-75` under `## Routed defects for round 36` item 1, marked
  "**(closure-found)**" — a later closure pass, not the step-1 sweep.
- The round-36 lesson describes the same capture without the label: "captured-by: none at write
  time — the r35 closure's non-author sweep caught it" (`corpus/lessons/round-36.md:60-61`).

Effect: a normative criterion states a capture provenance its own cited source denies. The finding
it cites is real and the citation target resolves; only the step label is wrong. Smallest
correction: "the r35 closure's routed defect 1 (closure-found)".

## Notes (not defects)

- **NOTE-1 — round-36 lesson not cited.** Criterion 72 cites the routing lesson only, not
  `lessons/round-36.md` where this round's `## Mistakes` files the class. The lane's convention for
  round-appended criteria is to cite the round's own lesson plus, where routed, the spotcheck lesson
  (e.g. criteria 6, 11-17, 71). Check (d) therefore passes or fails on which lesson "this" means; I
  report both readings rather than pick one.
- **NOTE-2 — "no in-lane criterion caught it" is literal-true but narrower than implied.**
  Admission-bar criterion 2 already requires every claim to carry "a measured anchor (path:line,
  command, evidence id)" (`corpus/QUALITY.md:3`); criterion 34's failing check — at the cited rev,
  `git show REV:<path> | grep -n <name>` must find the cited content — cannot pass for a
  never-existent path, though its scope is "a file that moves, or that the lane does not own"
  (`:251-260`); criterion 35 already mandates an appended, dated erratum for a false citation
  (`:262-266`); and fleet `PROTOCOL.md:345-359` already defines evidence as "a resolvable pointer"
  and requires resolution at closure time. What criterion 72 adds is the narrow, useful step:
  re-resolution **before the entry commits**, with the exact command. Worth keeping; worth not
  reading as the first resolvability rule.

## Residual risk

- The quoted r35 sentence's other clause, "was respawned by the closure", remains unverified. The
  correction removes the dead pointer but does not establish whether any respawn occurred; it
  correctly does not assert one. If a later round wants the waves narrative complete, that clause
  needs its own evidence or an erratum.
- **Mechanical-check hazard:** a naive regex over the enumeration counts **six** backticked
  `Residual*.md` names because the dead name appears inside the quotation and the `git log` glob.
  Any automated re-check of "names exactly five" must exclude quoted/command text (as the set
  compare above does); a raw `grep -c` will produce a false positive.
- Four `w2/Sentinel*.md` reports exist (`SentinelFleet`, `SentinelSandbox`, `SentinelLeak`,
  `SentinelScope`) and are **wave-2** seats, not a residual respawn (`for f in w2/Sentinel*.md` →
  headers say "Round 35 w2"). The correction's "The sentinel seat" is scoped by the preceding
  sentence to the residual wave, so this is a clarity risk for a scanning reader, not an error.
- Dangling objects: the absence scan covered reachable objects and the 8 `git fsck --unreachable`
  commits, but not a dangling tree/blob unreferenced by any commit. Excluding that class would
  require object-name reconstruction I did not perform; the risk is negligible for a claim about
  lane content, and no lane path or ref carries the name.

## Verification gaps

- No LSP device in this seat (recorded above); no server-backed caller/definition/diagnostic pass.
  This work is prose and git-object claims, which no LSP server in this lane models.
- I did not execute the C1/C2 counters or the cold-read monitor: out of this seat's assigned scope
  (other seats own those), and nothing in this report bears on their numeric claims.
- The `e423c41` write-time property was checked by `git ls-tree` at that commit and by the
  byte-identical-prefix test below, not by re-running the command in a checkout of `e423c41`.

## Append-only invariant (supporting evidence for the correction's own claim)

`git diff --numstat` per commit touching `LOG.md`: `5df962b 50 0`, `e423c41 46 0`, and no entries
for `796e08b`, `b455001`, `d9c496b` (they do not touch LOG.md). Byte test: `git show
5df962b:LOG.md` and the first `$(git show 5df962b:LOG.md | wc -c)` bytes of `git show
{e423c41,d9c496b}:LOG.md` all hash to
`290680756f8ba80574ed9d24659c9d694416a7a661bc55bc3fcacb0886c5a5f8`. The round-35 entry is
unmodified byte-for-byte, exactly as the correction states ("append-only; the entry stays as
written").

## Verdict

**PASS** on all four assigned checks: (a) quoted sentence exists verbatim; (b) the `git log` glob is
empty across reachable objects, the working tree, and 8 dangling commits; (c) the enumeration is
set-equal at write time and now to the five real residual reports; (d) criterion 72 exists with a
reproducible rule and falsifier. Two MINOR citation-precision defects (unsupported redirect
attribution; "step-1 pointer sweep" label contradicted by its own cited lesson) and two notes; no
MAJOR. The dead pointer is genuinely repaired under append-only mechanics, and every claim that
matters for the repair resolves.
