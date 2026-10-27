# Gates survey — kagi-shokunin (TAMESHI-2, probation wave 1)

**Lane:** tameshi-shokunin · **Assignment:** TAMESHI-2
**Substrate:** `/home/vgpnk/Projects/shokunin/kagi-shokunin` — read-only for this survey.
**Substrate revision at survey:** `git rev-parse HEAD` = `4e48b771a3d8bd3a76f5ade605721d2252487ba9`, working tree dirty (see §8.1).
**Date:** 2026-10-14.
**Access proof:** `git status --porcelain` and `git rev-parse HEAD` were byte-identical
before and after every command in this survey. Secret-bearing files were never
content-read (§11).

Every claim below is one of three kinds and is labelled:

- **[OBS]** observation — a command output or a line in a file, quoted or counted.
- **[INF]** inference — a reading of observations, with the discriminator that would settle it.
- **[UNK]** unknown — not measured; the measurement that would close it.

---

## 1. What the six gates are, in one table

Line counts, byte sizes and sha256 (first 16 hex) are `wc -l`, `stat -c %s`,
`sha256sum` on the files as read, 2026-10-14.

| Gate | Lines | Bytes | sha256 (16) | Data file (rows¹) | Selftest cases² | Modes³ |
|---|---|---|---|---|---|---|
| `corpus/surface-census.sh` | 886 | 44212 | `275d8294a94e9eb7` | `surface-census.tsv` (35), `state-shape.tsv` (22) | **16** | verify (default) · `--verbs` · `--selftest` |
| `corpus/drift-pins.sh` | 451 | 19088 | `c138d34c7f0dfe95` | `drift-baseline.tsv` (15), `drift-symbols.tsv` (20) | **13** | verify (default) · `--pin` · `--selftest` · `--baseline/--symbols` |
| `corpus/op-ref-probe.sh` | 660 | 28660 | `509f084ad33229db` | contract arrays in-file⁴ | **29** | verify (default) · `--evaluate F` · `--fixture DIR` · `--selftest` |
| `corpus/checklist-run.sh` | 506 | 24697 | `7e5ec98b9e1d0afa` | `checklist.tsv` (16) | **34** | verify (default) · `--list` · `--ratio` · `--only ID` · `--selftest` |
| `corpus/scope-gate.sh` | 1129 | 55002 | `078a260184e25282` | `adjacency.tsv` (4) | **61** | gate (default) · `--map` · `--breadth` · `--selftest` · `--falsify` |
| `corpus/claim-ledger.sh` | 1319 | 79294 | `357fb24554cd0447` | `claim-ledger.tsv` (35), `stamps.tsv` (56) | **97** | `verify`/`citations`/`cells`/`docs` · `stamp` · `--selftest` |

¹ non-comment, non-blank lines: `grep -vcE '^\s*($|#)' <file>`.
² measured, not read — see §2.
³ mode argument dispatch: `surface-census.sh:89-92`, `drift-pins.sh:83-84`,
`op-ref-probe.sh:641-642`, `checklist-run.sh:81-83`, `scope-gate.sh:107-110`,
`claim-ledger.sh:190-192`.
⁴ `op-ref-probe.sh:71` — `OPRUN_CONTRACT=(…)` is a shell array, not a TSV; fixtures
are generated from it so a fixture cannot drift from its expectation (header claim,
`op-ref-probe.sh:53-56`).

---

## 2. Case counts — provable

**[OBS]** All six `--selftest` suites were run under `timeout 280` from
`kagi-shokunin/`, 2026-10-14. Each exited 0. Verdict lines, verbatim:

```
CHECKLIST_SELFTEST: PASS (34 cases)
SELFTEST: PASS (97 cases)              # claim-ledger
DRIFT_SELFTEST: PASS (13 cases)
OP_REF_SELFTEST: PASS (29 cases)
SCOPE_SELFTEST: PASS (61 cases)
SELFTEST: PASS (16 cases)              # surface-census
```

Total: **250 cases, 0 failures, 6/6 suites green.** These are the suite's own
`cases` counter printed by each gate's selftest epilogue —
`surface-census.sh:846`, `drift-pins.sh:444`, `op-ref-probe.sh:634`,
`checklist-run.sh:497`, `scope-gate.sh:1121`, `claim-ledger.sh:1317` — not a
static count of `cases=$((cases + 1))` sites. Counting sites statically gives
6/1/0/1/6/2 respectively and is **wrong**: the mutation and breadth loops register
cases dynamically. The measured counter is the only honest count.

**[OBS]** `bash -n` on all six exits 0 — all six parse.

**[OBS]** Case counts are not uniform per gate: `claim-ledger.sh` (97) carries
~39% of the fleet-wide selftest mass; `drift-pins.sh` (13) is the lightest.

---

## 3. POLICY and other fail-closed classes

**[OBS]** Every one of the six declares a three-valued exit lattice, and the
three values mean the same thing everywhere:

| Gate | Exit-0 | Exit-1 | Exit-2 | Header anchor |
|---|---|---|---|---|
| surface-census | clean | drift / failed probe | usage·setup | `surface-census.sh:37` |
| drift-pins | clean | any drift | usage·setup, *nothing written* | `drift-pins.sh:19` |
| op-ref-probe | CLEAN | DRIFT (measured behaviour changed) | SETUP/POLICY, *cannot measure or refused before exec* | `op-ref-probe.sh:45-46` |
| checklist-run | clean | item or declaration defect | usage·setup·shape, *nothing executed* | `checklist-run.sh:39` |
| scope-gate | clean | any defect | usage·setup | `scope-gate.sh:49` |
| claim-ledger | clean | drift/claim/id/cell/entry failure | policy/setup | `claim-ledger.sh:82` |

**[OBS]** Measured by `grep -nE '^# Exit' <gate> | head -2` on each file. All six
carry the lattice as a machine-findable header line rather than only in prose.

**[OBS]** The exit-2 class is *not* one class. Four distinct shapes appear, and
the distinction matters when reading a red run:

1. **Usage / setup — the gate cannot measure.** `surface-census.sh:85`
   (`die() { printf …; exit 2; }`), `scope-gate.sh:102`, `claim-ledger.sh:112`,
   `op-ref-probe.sh:141`. `scope-gate.sh:184` prints
   `ADJACENCY_SCOPE: SETUP (data file not found: …)` before exiting 2, so a
   missing input is never a bare death (header contract, `scope-gate.sh:48`).
   `op-ref-probe.sh:459-465` emits three SETUP variants (fixture dir not a dir,
   `op` not found, handler not executable).
2. **Malformed committed data — a setup error, deliberately not a verdict.**
   `surface-census.sh:31-32`: a malformed row `die`s at exit 2 because "it is not
   a verdict". `scope-gate.sh:198-228` instead accumulates `SCOPE BAD-ROW` and
   reports `DEFECT` at exit 1 — the two gates make *opposite* calls on the same
   situation. **[INF]** the scope-gate call is the safer one for a data-driven
   gate because one bad row still lets the other rules run and report; the
   census call keeps a malformed census from being mistaken for a clean host.
3. **POLICY — refused before the dangerous thing happens.** This is the class
   with the most measured teeth:
   - `op-ref-probe.sh:216-224` — `guard_op_file()` refuses, before any exec, an
     op-side path that is a symlink/FIFO/socket/device (`:218`) and any file
     carrying an `op://` reference token (`:222`). Plus `:204` (`adir` not a real
     directory) and `:207` (`absent.env` must stay absent — it is the premise of
     the missing-file probe). The header calls this "structural, not procedural"
     (`op-ref-probe.sh:29`) and states the consequence: no vault contact, no
     approval prompt, no sign-in dependency (`:43-44`).
   - `claim-ledger.sh:158` `ALLOWED_RE='^(bash|grep|sha256sum|wc|test)$'` — a
     committed claim row is an execution surface, so it must be a *single simple
     command*, first token in a five-entry allowlist.
   - `claim-ledger.sh:164` `DENY_WORD_RE` — 22 denied verbs
     (`op|the-janitor|git|rm|mv|cp|chmod|chown|curl|wget|sudo|ssh|scp|systemctl|tmux|kill|pkill|dd|truncate|shred|ln|rsync|tar`),
     matched on a **quote-stripped copy** so `g''it` / `g\it` / `o"p"` cannot
     walk past a name-based guard — the strip is `claim-ledger.sh:183`
     (`local dn=${c//\'/}; dn=${dn//\"/}`), the match `:184`. `claim-ledger.sh:160`
     `META_RE='[;&|<>$`]'` with `:171` refuse shell metacharacters; three further
     refusals guard the same surface — `inline-shell` (`bash -c`, `:174`),
     `backslash` (`:178`), `empty-quotes` (`:179`). Reason strings are printed by
     `policy_check()` (`:167`) and the selftest holds a case for each
     (`claim-ledger.sh:1210-1212`, `:1241`).
   - `claim-ledger.sh:218` — refuses a nested self-audit (`CLAIM_LEDGER_DEPTH`).
   - `claim-ledger.sh:255` — `stamp` refuses to shrink the pinned row set unless
     `--prune` is passed; the motivating loss was real (18 rows dropped by an
     in-flight 10-path stamp, `claim-ledger.sh:22`).
   - `checklist-run.sh:75` `DENY_CHECK` — a checklist row may not name
     `op.env`, `op run|read|inject`, `the-janitor start|stop|run`, or
     `claim-ledger.sh`; enforced at `:149-150`.
   - `drift-pins.sh:146` — `POLICY` when a baseline asks for a hash of a
     no-hash path, with the reason inline: *"secret-bearing path is never
     hashed"*.
4. **Zero-work is refused.** `claim-ledger.sh:757` refuses to report coverage
   over a scorecard with no round tables; `:762` refuses a cell audit where no
   cell cites a claim row ("the audit would be vacuous"). **[INF]** this is the
   strongest evidence-discipline pattern in the set: a gate that measures nothing
   must not exit 0.

**[OBS]** Counts of the literal string `POLICY` on lines whose first non-blank
character is not `#`, per gate, measured by
`grep -nE 'POLICY' <f> | grep -vE '^[0-9]+:\s*#' | wc -l`: op-ref-probe 10,
checklist-run 24, claim-ledger 11, drift-pins 1, scope-gate 0, surface-census 0.
(The totals including comment lines are 17/26/13/2/0/0.) **[INF]** the two
zero-POLICY gates are zero because they have no pre-exec refusal surface to
guard — both are data-file gates whose arms read committed TSVs and `stat` the
host; neither execs a binary. **[UNK]** whether that absence is deliberate or
simply unneeded is not recorded anywhere I read.

---

## 4. Evidence discipline — five shared habits

**[OBS]** Measured across all six; each is a repeatable pattern, not a one-off.

1. **A verdict line is a summary, and a summary must be last.**
   `claim-ledger.sh:26-28` states the rule: a claim passes only when the exit
   code equals the expected one **and** the expected ERE matches the *last
   non-empty output line*. `claim-ledger.sh:423` emits
   `FAIL <id> reason=verdict-not-final exit=<rc>` for the case that prints a
   verdict-shaped string and then fails. **[INF]** this is the single most
   portable idea in the set — a check that greps anywhere in stdout can be
   satisfied by a warning line.
2. **Verdicts carry their counts, not just their name.**
   `SURFACE_CENSUS: DRIFT (diverged=… gone=… …)` (`surface-census.sh:865`),
   `DRIFT_PINS: DRIFT (files_ok=… files_bad=… symbols_ok=… symbols_bad=…)`
   (`drift-pins.sh:253`), `OP_REF_PROBE: DRIFT (checks=… failed=… …)`
   (`op-ref-probe.sh:442`), `ADJACENCY_SCOPE: DEFECT (…)` with 25 named counters
   (`scope-gate.sh:659`, `CLEAN` at `:657`; observed run in §6), and
   `CLAIM_LEDGER: FAIL (claims=… failed=… deferred=…)` (`claim-ledger.sh:950-951`,
   `CLAIM_LEDGER: POLICY` at `:946`). A reader can tell *how much*
   drifted without re-running.
3. **Count-only pins where a name would be the leak.**
   `drift-pins.sh:14-16` — a `COUNT` verdict form (`<path>:#<pin>->#<actual>`)
   exists precisely because naming the matched text would leak; `:19-24` — the
   `op.env` row is pinned by mode + lines only, sha field `-`, since a content
   hash of a secret-bearing file is an offline guessing oracle.
   `scope-gate.sh:19-20` — breadth pins are count-only, so no private child-name
   manifest is committed (`# breadth <dir>  children=<N>  declared=<M>` is the
   whole schema, `scope-gate.sh:25`). **[INF]** this is the clean answer to "pin
   the host without publishing the host".
4. **Abstention is declared, counted, and exit-neutral.**
   `scope-gate.sh:52-55` — `unresolved` / `contested` are *declared* classes
   printed in the summary; a legitimately absent runtime row abstains from R9
   (`ADJACENCY_ABSTAIN: rows=N`); but a path that exists and cannot be resolved
   is `UNVERIFIED` and **fails closed** (`scope-gate.sh:1077` selftest asserts
   this). `surface-census.sh:37-38` — exit 0 is returned even when the only
   non-OK lines are `ABSENT`/`SKIP`.
   `claim-ledger.sh:397-398` — a `[substrate]`-tagged row prints
   `DEFER <id> reason=substrate-absent` and does not fail.
   **[INF]** the guard that keeps this from becoming a blanket excuse is
   `claim-ledger.sh:136-137`: a row that defers while the substrate is *present*
   is a genuine run, and the selftest proves both paths (`:1313-1315`).
5. **Secret hygiene is stated in the header as a prohibition, not a hope.**
   `surface-census.sh:40`, `drift-pins.sh:21`, `checklist-run.sh:41`,
   `scope-gate.sh:58`, `claim-ledger.sh:84`. Notably `claim-ledger.sh:85-86`:
   the gate *never echoes a claim's output* — only the verdict line is matched,
   never printed, because a claim could read a private file.

---

## 5. Cross-checks — kagi's prose against measurement

### 5.1 Case-count claims in `corpus/README.md` — 6/6 confirmed

**[OBS]** The README's gate table asserts a case count for each gate. I measured
each. All six agree:

| README anchor | Claim | Measured | Agree |
|---|---|---|---|
| `corpus/README.md:33` | checklist-run "34 cases" | 34 | yes |
| `corpus/README.md:36` | drift-pins "13 cases" | 13 | yes |
| `corpus/README.md:40` | surface-census "16 cases" | 16 | yes |
| `corpus/README.md:43` | scope-gate "61 cases" | 61 | yes |
| `corpus/README.md:63` | claim-ledger "97 cases" | 97 | yes |
| `corpus/README.md:69` | op-ref-probe "29 cases" | 29 | yes |

**[INF]** six-for-six on independently reproducible numbers is weak evidence about
a *doc* but strong evidence about a *habit*: kagi's prose numbers are derived from
runs, not typed from memory. It is not a general licence — the same table's
`--falsify` claim fails (§6).

### 5.2 The 16-item checklist bijection — verified two ways

**[OBS]** `checklist-run.sh:11-21` claims a bijection between 16 `SKILL.md`
items and 16 `checklist.tsv` rows. Independently: `grep -c '^- \[ \] ' SKILL.md`
= **16**; non-comment rows in `checklist.tsv` = **16**.

**[OBS]** README:33 asserts the split `runnable=9 by_hand=7 delegated=3 direct=6`.
Independent tally of `checklist.tsv` column 2: **9 runnable, 7 by-hand**.
`awk -F'\t' '$2=="runnable"{print $4}' | grep -c '^bash corpus/'` = **3** delegated,
and 9 − 3 = 6 direct. **[OBS]** by-hand classes are a closed set of four:
`authoring-duty` (4), `cross-lane` (1), `manual-change` (1), `runtime-behavior` (1),
enforced on shape and ≥24 chars at `checklist-run.sh:155-162`.

**[INF]** the `delegated`/`direct` split (`checklist-run.sh:29-31`) is the
honest part of this design: 3 of the 9 "runnable" rows are `bash corpus/<gate>.sh`
and therefore re-assert nothing the gate did not already assert. A ratio line
that did not split them would overstate the checklist's own coverage by 50%.

### 5.3 The revision stamp set — 56/56 resolving

**[OBS]** `corpus/stamps.tsv` holds 56 rows (path, sha256, lines, bytes). A full
recompute of every stamped sha against the live files returned
`ok=56 stale=0 missing=0 nohash=0` at 09:55:50 on 2026-10-14.

**[OBS]** The same procedure run ~40 seconds earlier returned a *different*
answer: `corpus/claim-ledger.sh` was stamped `60b5eb39…` (1319 lines, 79336
bytes) while the file on disk was `357fb245…` (1319 lines, 79294 bytes) — same
line count, 42 bytes apart, i.e. a same-length-region content edit. See §8.1.

---

## 6. Finding F-1 — `--falsify` measures 16/18 on this host, README says 18/18

**[OBS]** Command: `bash corpus/scope-gate.sh --falsify` from
`kagi-shokunin/`, 2026-10-14. Real exit code **1**. Final line, verbatim:

```
SCOPE_FALSIFY: FAIL (caught=16/18 failed=2)
```

**[OBS]** The two uncaught mutations print as:

```
FALSIFY FAIL breadth-exceeds (exit 1 want 1, token SCOPE BREADTH-EXCEEDS)
FALSIFY FAIL breadth-new-declared-child (exit 1 want 1, token SCOPE BREADTH-EXCEEDS)
```

Exit code **matched** in both (want 1, got 1); the *token* did not. The mutations
are `scope-gate.sh:779` and `scope-gate.sh:802`; the expected token is emitted at
`scope-gate.sh:594`.

**[OBS]** The live breadth state the run reported:

```
BREADTH_AUDIT: DEFECT (required=4 pins=4 checked=3 ok=0 children=38 declared=1
  undeclared=37 missing=0 invalid=0 drift=6 exceeds=0 unverified=1)
SCOPE BREADTH-CHILDREN-DRIFT $HOME/.config/opencode pinned=20 live=3
SCOPE BREADTH-CHILDREN-DRIFT $HOME/.local/bin pinned=105 live=34
SCOPE BREADTH-CHILDREN-DRIFT $HOME/.agents pinned=4 live=1
SCOPE BREADTH-HOST-MISSING $HOME/.local/share/the-musketeer/chrome-profile
```

`exceeds=0` — the `BREADTH-EXCEEDS` class (declared > live children,
`scope-gate.sh:594`) never fires because live child counts are *far below* their
pins: the drift is in the opposite direction.

**[OBS]** The prose and the ledger both claim otherwise:
`corpus/README.md:43` — "`--falsify` (18/18 mutations)";
`corpus/claim-ledger.tsv:40` row `R16-03` expects
`^SCOPE_FALSIFY: PASS \(caught=18/18 failed=0\)$`, exit 0, timeout 300.

**[OBS]** `R16-03`'s note is tagged `[substrate]`, and the tag has teeth:
`claim-ledger.sh:138-145` `substrate_present()` returns true only when
`[[ -x "$HOME/.local/bin/the-janitor" ]]`; on this host that path does **not**
exist (`ls` → No such file or directory). `claim-ledger.sh:397-398` therefore
prints `DEFER R16-03 reason=substrate-absent` and does **not** fail.
**[INF]** the ledger's own discipline absorbs this discrepancy by design; the
*README's* unqualified "18/18" at `README.md:43` does not carry the same
qualifier, so a reader of the README alone is told a stronger thing than the
ledger is willing to assert.

**[INF]** the two failures read as host-state dependence, not gate logic. The
discriminator: the same rule has a scratch case, `scope-gate.sh:934`
(`run_case breadth-exceeds 1 'SCOPE BREADTH-EXCEEDS'`), and that case **passed**
inside the 61/61 selftest, where the scratch tree's counts are consistent by
construction. So the `exceeds` rule fires when counts line up and cannot fire
when live children have collapsed.

**[INF]** Status: **not** ruled a defect, and **not** ruled clean. Settling it
needs a falsify run against a tree whose breadth pins match live child counts —
either a host where the four pinned directories still hold their declared
children, or `--falsify` extended to accept `--root` pointing at a consistent
scratch host. Until then, `README.md:43` is an unqualified claim contradicted by
a reproducible measurement on a real host, and `R16-03` will not surface it
because its substrate tag makes it defer.

---

## 6b. Finding F-2 — three of six refusal paths in `policy_check()` have no selftest case

**[OBS]** `policy_check()` (`claim-ledger.sh:167`) declares six refusal reasons,
each printed as a distinct token:

| Reason token | Line | Asserted by a `tcase`? |
|---|---|---|
| `first-token:<w>` | `claim-ledger.sh:170` | yes — `:1211` |
| `metachar` | `claim-ledger.sh:171` | yes — `:1210` |
| `inline-shell` | `claim-ledger.sh:174` | **no** |
| `backslash` | `claim-ledger.sh:178` | **no** |
| `empty-quotes` | `claim-ledger.sh:179` | **no** |
| `denied-verb:<w>` | `claim-ledger.sh:184` | yes — `:1212` |

Measured by `grep 'tcase' claim-ledger.sh | grep -c '<token>'`, which returns
1/1/0/0/0/1 in the order above. There are exactly four `tcase policy…` cases
(`:1210-1212`, `:1241`); `policy-split-verb` (`:1241`) expects only the generic
`POLICY c1 reason=` prefix.

**[OBS]** The header states the opposite: `claim-ledger.sh:94-95` —
"`--selftest` proves each refusal path on scratch data". That is true for three
of the six and unproven for `inline-shell`, `backslash` and `empty-quotes`.

**[INF]** severity is moderate, not cosmetic: these three are the *bypass* class.
`claim-ledger.sh:92-94` records that `backslash` and `empty-quotes` exist because
round-11's executor A03/A04 actually executed a stand-in through `g''it` and
`g\it`, and `:172-173` records that `inline-shell` exists because a round-11
sentinel found policy-clean rows mutating state via `bash -c` (`:177` records
that the empty-quote case came from the same executor). So the three
unproven paths are precisely the three that a real adversary found. A future
edit that deletes or reorders any of them would be caught by nothing.

**[INF]** the fix is two lines per path and needs no new machinery: the harness
already exists (`tcase <name> <exit> <token-regex> <cmd…>`), and the reasons are
already distinct tokens chosen to be matched. Settling this needs the three cases
added — or the header claim at `:94-95` weakened to name the three unproven
paths. I did not test whether the refusals *fire*; I only measured whether the
suite asserts them.

---

## 7. Spot-checks (three anchors, re-verified on the current revision)

All three were read a second time *after* the substrate moved under the survey
(§8.1); each line below is the line at the sha in §1.

**S-1 — `claim-ledger.sh:158`.** Quoted verbatim:

```
ALLOWED_RE='^(bash|grep|sha256sum|wc|test)$'
```

Confirmed by `sed -n '158p'`. This is the five-entry allowlist that makes a
committed claim row safe to execute. Its sibling at `:160`
(`META_RE='[;&|<>$`]'`) and `:164` (`DENY_WORD_RE`, 22 verbs) complete the
refusal set; `:171` prints the `metachar` reason. The refusal is *before* the
run. **Corrected:** the selftest holds a live case for three of the six reason
strings (`claim-ledger.sh:1210-1212`), not for each — see F-2 (§6b).

**S-2 — `op-ref-probe.sh:218`.** Quoted verbatim:

```
printf 'OP_REF_PROBE: POLICY (op-side path is not a plain regular file, refused before exec: %s)\n' "$f" >&2
```

Confirmed by `sed -n '218p'`; it is the first branch of `guard_op_file()`
(opened at `:214`), inside a `[[ -L $f || ! -f $f ]]` test. The reason the test
is a *path* test and not a name list is recorded at `op-ref-probe.sh:41-42`: the
round-12 sentinel found two bypasses (`absent.env`, `adir`) that a fixed name
list would have missed. **[OBS]** the sibling refusal at `:222` greps the file
for `op://` and refuses — so the gate can never resolve a reference, and the
header's claim of "no vault contact by construction" (`README.md:69`) rests on
this one function.

**S-3 — `scope-gate.sh:934`.** Quoted verbatim:

```
run_case breadth-exceeds 1 'SCOPE BREADTH-EXCEEDS'
```

Confirmed by `sed -n '934p'`. This is the scratch-tree case that distinguished
F-1 (§6): it asserts exit 1 **and** the token on a generated tree, and it passed
in the 61/61 run. Its live counterpart, the falsify mutation at `:779`, failed.
Reading the two together is what tells you the rule is intact and the host is
not.

**Supporting anchor — `drift-pins.sh:146`.** `POLICY  %s baseline sha must be
\`-\` (secret-bearing path is never hashed)` — the single POLICY site in that
gate, and the mechanism behind §4.3.

---

## 8. Caveats on this survey itself

### 8.1 The substrate moved during the survey

**[OBS]** `corpus/claim-ledger.sh` mtime = 2026-10-14 09:54:11 and
`corpus/stamps.tsv` mtime = 2026-10-14 09:55:50, both **after** this survey's
opening directory listing (which showed `claim-ledger.sh` at 09:49 and
`stamps.tsv` at 09:52). Something in kagi-shokunin was actively writing while I
was reading.

**[OBS]** Consequence: an early read of `stamps.tsv` showed `claim-ledger.sh`
stamped `60b5eb39…` while the live file was `357fb245…` — a stale state I
observed, then observed re-pinned. The full tally a minute later was
`ok=56 stale=0`.

**[OBS]** Every `path:line` citation in this document was re-read against the
current revision after the move (`sed -n '<n>p'` on each) and each resolves to
the text quoted here; this pass is what produced the corrections in §3.3, §4.1,
§4.2, §6b and S-1. Line numbers are pinned to the sha256 in §1; a reader on a
differing revision should re-resolve rather than trust the numbers.

**[UNK]** which process wrote, and whether it is kagi's own round-19 work or
another lane in this wave. Observable only as mtimes; no author was seen.

### 8.2 What this survey did not measure

- **[UNK] Live verdicts for five of six gates.** I ran `--selftest` for all six
  and `scope-gate.sh --falsify` live. I did **not** run `surface-census.sh`,
  `drift-pins.sh`, `op-ref-probe.sh`, `checklist-run.sh` or `claim-ledger.sh` in
  live verify mode. So I have no measurement of whether the host currently
  passes those gates, and no measurement of their drift counts. F-1 (§6) is the
  one live verdict I hold.
- **[UNK] `op` behaviour.** I never invoked `op` (`which op` → `/usr/bin/op`; no
  version read). The masking contract is pinned to `op` 2.35.0 at
  `op-ref-probe.sh:20-24` and `:71`, `:91`; whether this host's binary still
  behaves that way is unmeasured by me.
- **[UNK] Row counts are not assertions.** The counts in §1 column 5 are counts
  of committed data rows. They say nothing about whether each row holds on this
  host. `surface-census.tsv` (35 rows) + `state-shape.tsv` (22) in particular
  encode host claims I did not execute.
- **[UNK] `scope-gate.sh --falsify`'s other 16 mutations.** I know 16 caught and
  2 not; I did not inspect each of the 16 individually to confirm each exercised
  a distinct rule. The gate names them (`FALSIFY OK <name>`), which is checkable
  but was not checked here.
- **[OBS] Scope of the "250 cases" number.** It is cases *run and reported*, not
  unique assertions: several cases in `claim-ledger.sh` re-invoke the gate's own
  `--selftest` (`claim-ledger.sh:1073`), so the total double-counts some inner
  cases. **[INF]** treat 250 as a suite-size measure, not an assertion-count.

---

## 9. Reusable pattern (candidate — for the tameshi method, not a claim on kagi)

**[INF]** The six gates share an eleven-item shape that looks portable. Stated as
a checklist, with the kagi anchor that evidences each item, and explicitly *not*
claimed as a fleet generalisation — per `tameshi-shokunin/PROVINCE.md`, a pattern
is admitted from evidence in **two** independent lanes:

1. Three-valued exit lattice, same meaning everywhere (§3 table).
2. POLICY class separate from SETUP, both exit 2, both *before* the effect.
3. Malformed committed data is not a verdict (§3.2) — note the five gates that
   still disagree on which exit code this earns.
4. Last-non-empty-line rule for any verdict-shaped expectation
   (`claim-ledger.sh:53-56`).
5. Zero-work is a setup error, never a clean run (`claim-ledger.sh:757`, `:762`).
6. Abstentions named, counted, exit-neutral, and pinned by a both-paths selftest
   (`claim-ledger.sh:136-137`, `:1313-1315`).
7. Count-only pins wherever a name would leak (§4.3).
8. Scratch-tree selftest that *fires* every rule, run as the proof
   (§2; the case counts are the evidence). **Amended after F-2 (§6b):** "every
   rule" is an aspiration, not a property — measure the refusal paths against the
   asserted ones before repeating the claim.
9. A mutation mode that attacks the gate itself (`scope-gate.sh:669`, `--falsify`).
10. Secret hygiene stated as a prohibition in the header (§4.5).
11. Revision stamps so a reader can name the artefact they read (§5.3).

**[INF]** Items 4, 5, 6 and 7 are the ones with a *measured cost of absence*
recorded in kagi's own history: item 4's absence let a verdict-shaped-then-failed
command pass; item 5's absence would make an empty audit look green; item 7's
absence would either leak or forbid pinning at all. Items 1–3 are cheap and
structural. The candidate is a tameshi hypothesis until a second lane's gates
show the same shape.

---

## 10. Errata (append-only)

Entries below are never edited in place — per `tameshi-shokunin/corpus/QUALITY.md`
item 4. New entries go the bottom of this list.

**ER-1 — 2026-10-14, same session as issue.** Sixteen citations were wrong in the
first issue of this document and were corrected during the citation audit, before
hand-off. Recorded rather than silently fixed, because the failure mode is the
one this lane exists to catch:

| Where | Was | Is | How found |
|---|---|---|---|
| §3.3 | `claim-ledger.sh:100-105` for the quote-strip | `:183` strip, `:184` match | `sed -n '181,184p'` |
| §3.3 | `claim-ledger.sh:28-31` for the 18-row stamp loss | `:22` | `grep -n 'lost 18 rows'` |
| §3.3 | POLICY sites 13 / 6 | 24 / 11 (code-only lines) | `grep -nE POLICY \| grep -vE '^[0-9]+:\s*#'` |
| §4.1 | `claim-ledger.sh:53-56` for the final-line rule | `:26-28` | `sed -n '26,28p'` |
| §4.2 | `scope-gate.sh:594` for `ADJACENCY_SCOPE: DEFECT` | `:659` (`:594` is `BREADTH-EXCEEDS`) | `sed -n '656,660p'` |
| §4.2 | `claim-ledger.sh:951-953` for the FAIL summary | `:950-951` | `sed -n '945,953p'` |
| §3 table | `surface-census.sh:36` for the exit lattice | `:37` | `grep -nE '^# Exit'` |
| §3 table | `drift-pins.sh:18` | `:19` | same |
| §3 table | `op-ref-probe.sh:47-48` | `:45-46` | `sed -n '45,47p'` |
| §3 table | `checklist-run.sh:38` | `:39` | `grep -nE '^# Exit'` |
| §3 table | `scope-gate.sh:47-48` | `:49` | same |
| §3 table | `claim-ledger.sh:81` | `:82` | same |
| §4.4 | `surface-census.sh:33-34` for the ABSENT/SKIP exit-0 rule | `:37-38` | `sed -n '30,38p'` |
| §6b | `claim-ledger.sh:96-99` for the A03/A04 bypass history | `:92-94` | `sed -n '92,99p'` |
| §1 fn4 | `op-ref-probe.sh:57-59` for fixture generation | `:53-56` | `sed -n '51,57p'` |
| §4.3 | `scope-gate.sh:37-39` for count-only breadth pins | `:19-20` (schema at `:25`) | `grep -n 'Count-only breadth'` |

**Lesson (for the tameshi method, not a claim on kagi):** every one of the
sixteen was a *right-file, wrong-line* (or wrong-count) error — the kind that
reads as verified because the file genuinely contains the claim. **[INF]** two
generators dominate, by the table above: twelve of the sixteen rows were
transcribed from a **stripped** header view — a rendering that removes the
leading `# ` shifts every number by the lines it drops, which is why those rows
landed 1–3 lines early and never once landed late; the other four were cited from
memory of what a section said rather than from its number. The only thing that
caught them was re-reading each cited line **by number** after writing. The
countermeasure that makes the error visible on the page is quoting the line
verbatim in the survey, not merely citing it — a wrong number under a quoted line
is checkable by eye; a wrong number alone is not.

### Errata (round 2)

Applied 2026-10-14 by TAMESHI-R2-2 from the wave-1 review trail (the wave's
audits re-verified anchors+counts — commit `3da686c`; wave record LOG.md:42-48
and the carried round-2 items LOG.md:64-66; per plans/round-2.plan.md:10).
Append-only: nothing above is edited; new entries go to the bottom of this
list. Round-2 re-measurements were run by this lane 2026-10-14 (scratch
`/tmp/tameshi-r2-2-work/`).

**G-R2-1 (measured — corrected pin, §1).** The table's `claim-ledger.sh` row
reads `79294` bytes / sha256 first16 `357fb24554cd0447`; the live file at the
committed revision is **`79301` / `93c5827202b9cdec`** (1319 lines held). The
surveyed bytes were an intermediate dirty-tree state that was never committed
(`git cat-file -t 357fb24554cd0447` → fatal: not a valid object name); the
substrate then moved again at 09:58:55 (mtime), and the lane committed at
10:05:10 — HEAD `fecee874` (round-18, tree now clean) — with
`corpus/stamps.tsv:4` re-pinned to the new sha/bytes. The other five §1 rows
held on re-measure (sha256 first16: surface-census `275d8294a94e9eb7`,
drift-pins `c138d34c7f0dfe95`, op-ref-probe `509f084ad33229db`,
checklist-run `7e5ec98b9e1d0afa`, scope-gate `078a260184e25282`; byte sizes
44212/19088/28660/24697/55002 held). Command: `sha256sum corpus/*.sh;
stat -c %s corpus/*.sh; git -C kagi-shokunin log -1 --format='%h %ci'`.

**G-R2-2 (measured — corrected citation, §9 item 4).** §9 item 4 cites
`claim-ledger.sh:53-56` for the last-non-empty-line rule; on the current
bytes :53-56 = the `entry`/`docs` usage paragraph, :26-28 = the rule — the
same correction ER-1 made to §4.1 but which §9 retained.
Command: `sed -n '26,28p' corpus/claim-ledger.sh` (rule present),
`sed -n '53,56p' …` (not the rule).

**G-R2-3 (measured — corrected count, §3.3).** "22 denied verbs" → **23**: the
regex carries 23 alternatives, and the note's own parenthetical lists all 23
(op, the-janitor, git, rm, mv, cp, chmod, chown, curl, wget, sudo, ssh, scp,
systemctl, tmux, kill, pkill, dd, truncate, shred, ln, rsync, tar). Command:
`grep '^DENY_WORD_RE=' corpus/claim-ledger.sh | grep -oE '\(op\|[^)]*\)' |
tr '|' '\n' | wc -l` → 23.

**G-R2-4 (measured — held, re-verified set).** Six `--selftest` runs exit 0:
16/13/29/34/61/97 (surface-census, drift-pins, op-ref-probe, checklist-run,
scope-gate, claim-ledger) = 250 held (§2). `--falsify` exit 1 →
`SCOPE_FALSIFY: FAIL (caught=16/18 failed=2)` with the same two
`FALSIFY FAIL … SCOPE BREADTH-EXCEEDS` lines and the same live breadth tens
(§6 F-1 held; `~/.local/bin/the-janitor` still absent, so R16-03 still defers;
`README.md:43` still says unqualified "18/18"). POLICY code-line counts held
10/24/11/1/0/0 (totals 17/26/13/2/0/0, §3.3); data rows held
35/22/15/20/16/4/35/56 (§1 fn1); stamps recompute `ok=56 stale=0 missing=0
nohash=0` (§5.3); README anchors :33/:36/:40/:43/:63/:69 still carry
34/13/16/61/97/29 (§5.1); F-2 `tcase` counts still 1/1/0/0/0/1
(first-token/metachar/inline-shell/backslash/empty-quotes/denied-verb, §6b).

**G-R2-5 (measured/inferred — §8.1 [UNK] discharged).** The mid-survey writer
is identified in round 2: the next commit touching `claim-ledger.sh`/
`stamps.tsv` is kagi's own round-18 `fecee87` (2026-10-14 10:05:10, "two lane
defects fixed (census selftest hermeticity, indistinguishable claim
failure)"); **[INF]** the 09:54-09:58 writes were that in-flight round-18
work, not another lane.

**G-R2-6 (judgment — wave-record position, §6b/§8.2).** Carried, not absorbed
(LOG.md:64-66): live verdicts remain unmeasured for five of six gates, and
F-2's two-lines-per-path fix stays a recommendation to the sibling lane
(PROVINCE.md:16-18 — tameshi never edits a sibling's gate). G-R2-4 confirms
the three refusal paths are still asserted by no case.

---

## 11. Secret handling — positive statement

**[OBS]** This survey never read the content of `~/.config/the-janitor/op.env`,
any `op://` reference path, any vault item, any OAuth token, or any
`server.token`. The only mode-600 file read in full was
`kagi-shokunin/corpus/stamps.tsv`, whose every field is a repo path, a sha256, a
line count and a byte count — and it was read as a row set for §5.3, not
transcribed. One **shape-only** check was made against the host:
`ls -l "$HOME/.local/bin/the-janitor"` returned *No such file or directory*,
which is a presence fact about a path, not file content, and is the fact F-1
turns on.