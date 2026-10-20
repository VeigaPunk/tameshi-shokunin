# W02KnowledgeDraft — round 17 wave 1 (tameshi)

Scope: draft `corpus/knowledge/input-keyed-coldread-credit.md` as text in this report. Nothing under `corpus/` was written. Lane tip read: `98bea7da5801f4bc58e4187690ee1687c8a5061f`.

Verdict: **built** (draft below, §D). The draft describes contract C as specified in the wave brief. Its trace and sectionizer claims are observed on this host at 98bea7d/strace 7.2. The v2 helpers (`trace-inputs.py`, `measure.py --rev`, `assemble.py`) are not committed at the tip, so every claim about their behaviour is contract text, not an observed run. The draft says so.

## A. Commands and key output

| # | Command (abridged) | Exit | Key output |
|---|---|---|---|
| 1 | `git show 98bea7d:corpus/knowledge/incremental-pin-disposition.md` | 0 | provenance trio `source:` / `verified-at:` / `recheck:`, then `ground:`, `source-correction:`; `# <claim as title>`; sections `## N. … (O)/(I)/(U)` tags |
| 2 | `ls-tree 98bea7d -- corpus/knowledge/` | 0 | 24 knowledge entries; no `input-keyed*` file |
| 3 | `git show 98bea7d:.ufo/evidence/round-16/measure.py` (grep) | 0 | `HEADING_RE` `:64` = `^#{1,3}(?:\s|$)`; `sectionize` fence toggle is `startswith('```')` only; `entry_credit_reason` `:178-217`; `coldread` `:218-266`; `by_sha` credit `:243-248` |
| 4 | `git show 98bea7d:SKILL.md \| grep -c '^~~~'` | 0 | 0 lines starting `~~~` (no current effect of the ``` / ~~~ fence difference, see F4) |
| 5 | `git show 98bea7d:corpus/lessons/round-16-verifier-spotcheck.md` | 0 | §2 "Why C2 still fails": CR26 bucket `SKILL.md:1563-1596`, runner `75ed934d` → `c699c8c`/`05a2247`; `[INFERENCE]` exit 2 `expected_input_digest_mismatch`; §6 R16-C2b |
| 6 | `git show 98bea7d:.ufo/evidence/round-16/coldread/ledger.json` (shape) | 0 | keys `schema, entries, _meta, skill_pins`; entry keys `skill_sha256, start, end, heading, sha256, class, verdict, blocking_gaps, wrong_expectations, minor_gaps, commands_executed_count, seats, reports, positions`; no `inputs`, `external_inputs`, `read_rev` (v1) |
| 7 | `git show 98bea7d:corpus/knowledge/incremental-pin-disposition.md` (tail/§5a/§8) | 0 | exemplar shape, §5a mode-bit note (`100755`, round-10 SETUP), `CT=1` timing input |
| 8 | `strace -V` | 0 | `strace -- version 7.2` (`/usr/bin/strace`, already installed; nothing installed) |
| 9 | `strace -f -qq -e trace=openat,open,openat2,execve -o $D/trace.txt sh -c 'cat …/in.txt; cat …/absent.txt; true'` in `/tmp/tameshi-r17w1-W02KnowledgeDraft-3cEpbM` | 0 | `73678 openat(… "/tmp/…/root/in.txt", O_RDONLY) = 3`; `73679 openat(… "/tmp/…/root/absent.txt", O_RDONLY) = -1 ENOENT`; `/etc/passwd`, `/usr/lib/locale/locale-archive`, `/usr/bin/cat` execve all present in raw trace |
| 10 | symlink / write-mode probe in `/tmp/tameshi-r17w1-W02KnowledgeDraft-xthuaU` | 0 | `openat(… "…/root/link.txt", O_RDONLY) = 3` (the link name, not its target); `openat(… "…/root/out.txt", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3`; `… "…/root/sub/none", O_RDONLY) = -1 ENOENT` |
| 11 | `sha256sum` of the probe input | 0 | `b6a98d9c…` (scratch file, illustrative only) |

Not run: `trace-inputs.py --selftest`, `measure.py --selftest`, `assemble.py --selftest`, and any gate. The helpers are not committed at 98bea7d and not present in the live tree's `round-17/` (only `census-start.txt`, `op1-redbefore-98bea7d.txt`, `redbefore/`). Nothing was executed against a lane-owned gate.

## B. Findings

**F1 — the draft's central claim is observed, the mechanism is contract.** The sha-only hole (R16-C2b) is observed in the round-16 closure (committed lesson §2, executed reads, not a re-run of the gate). The input-keyed rule itself exists only in the wave brief (contract C). The draft marks which is which.

**F2 — the tracer contract, as written, drops absence and writes.** Observed in probe 9–10: `strace -qq` on `openat` reports every open, not only successful reads. Contract C says "successful opens of regular files under root". So:
- ENOENT probes are dropped. An input that is absent at run time and created later is undetected (absence is an input, observed as `-1 ENOENT`).
- Write-mode opens under root (`O_WRONLY|O_CREAT|O_TRUNC`) are recorded as inputs unless the helper filters them. A command that writes an evidence file under root would record its own output, and the next measure would report `input-drift` on it. Recommendation for L1/X08: filter write-mode opens out of `inputs` and report them separately, or state the exclusion in the helper's receipt. The draft states this as an open item, not a decided rule.

**F3 — symlinks and hash timing are unspecified.** `openat` records the path string the program passed (probe 10), not the resolved target. A link inside root to a file outside root would be keyed by the in-root name. Contract C does not say when `sha256` is computed (at open, at exit, or at measure time). A file changed mid-run would record its later bytes. Recommendation: `realpath` before keying, and hash at exit with a before/after size+mtime check, or record the hash at open. Both are open items in the draft.

**F4 — sectionizer fence mismatch (latent).** `measure.py` toggles fences only on lines starting with ```` ``` ```` (`sectionize`). The round-16 closure's independent sectionizer also excluded `~~~` fences. SKILL.md at 98bea7d has zero `~~~` lines (probe 4), so no current bucket differs. The draft states the ``` rule, matching `measure.py`, and flags the difference.

**F5 — the external map and the trace disagree in scope.** Contract C's `external` covers regular files under `/home` outside root. Probe 9 shows reads of `/etc/passwd`, `/usr/lib/locale/…` and an exec of `/usr/bin/cat`, none of which the contract records. The interpreter binary a selftest runs (`node`, `python3`, `bash`) is therefore invisible to the input set. This matches the `process.execPath` note in `incremental-pin-disposition.md` §5a. The draft lists it as an undeclared input.

**F6 — `read_rev` is recorded, not a credit condition.** Contract C requires `read_rev` on each ledger entry, but the credit rule (contract C, measure v2) keys only on `inputs`. An entry whose `read_rev` is older than an unchanged input is still credited when the input's sha matches at REV. This is consistent with the rule as written. The draft states it so the reader does not assume `read_rev` gates credit.

**F7 — seat-opened lane files are self-reported.** Contract C adds "every lane file the seat opened to check the section" to `inputs`. The tracer cannot see those reads, so the seat's report is the only source. The draft lists this as an unverified part of the input set.

## C. Out of scope / not touched

- No file under `corpus/`, `tools/`, `.ufo/evidence/round-17/`, `MANIFEST.json`, `.ufo/state/` or `.ufo/watchdog.log` was written.
- No `jj` or git write. Git reads only: `git show <rev>:<path>`, `ls-tree <rev>`, `status --porcelain` not needed.
- No tool installed or upgraded. `strace` 7.2 was already at `/usr/bin/strace`. Pacman is paused host-wide, so no install was attempted.
- Scratch under `/tmp/tameshi-r17w1-W02KnowledgeDraft-*` only (removed at the end of the wave).
- No subagent, no background job, no message to `agent://TameshiR17` (no blocker).

## D. Draft entry — `corpus/knowledge/input-keyed-coldread-credit.md`

Placeholders for L1: `S0xx` markers in the `source:` line and in §1, §3. `ground:` frontier id is L1's call.

````markdown
source: S0xx — lane lesson `corpus/lessons/round-16-verifier-spotcheck.md` §2 and §6 (R16-C2b) @ 98bea7da5801f4bc58e4187690ee1687c8a5061f; S0xx — lane instrument `.ufo/evidence/round-16/measure.py` @ 98bea7d (`HEADING_RE` :64, `sectionize`, `entry_credit_reason` :178-217, `coldread` :218-266); S0xx — `strace` 7.2 on this host (`/usr/bin/strace`), output observed 2026-10-20 in `/tmp` scratch (probes described in §3)
verified-at: 2026-10-20
recheck: 90d — `git show 98bea7d:.ufo/evidence/round-16/measure.py | grep -c 'def entry_credit_reason'` → 1; once round-17 helpers are committed, `python3 .ufo/evidence/round-17/measure.py --selftest` → exit 0 and `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest` → exit 0 (both NOT RUN at draft time; a missing helper is drift, not a pass)
ground: F<L1> — cold-read credit hole (R16-C2b); L1 assigns the frontier id

# Sha-only cold-read credit goes stale; credit must also be keyed to the inputs a bucket ran against

Scope: one method step for the tameshi SKILL.md cold-read ledger — how a
credited bucket is invalidated when a surface its executed commands read has
changed. It does not make the tracer a sandbox, does not re-read any bucket,
and does not claim the ledger proves SKILL.md correct.

## 1. The observed hole (O)

Round 16 credited every SKILL.md bucket by the sha256 of its section text
(`measure.py` `coldread`, `by_sha` credit :243-248). A bucket whose bytes did
not change kept its credit while the surface its instructions run against
changed. The round-16 closure (`corpus/lessons/round-16-verifier-spotcheck.md`
§2, S0xx) reproduced one case: the bucket `## Effective expectation
reconciliation — round 14` (SKILL.md:1563-1596) had one credit, recorded
against runner `75ed934d`; later commits changed `tools/mutate-and-run.sh`,
which the expected-input pin still names at `75ed934d`. The closure's reading
of the gate is `[INFERENCE]` from code (`tools/evidence-disposition.py:1182-1192`),
not an executed result. The bucket's bytes never changed, so the sha-only
rule could not notice.

Invariant this entry adds: a bucket's credit at REV requires the section sha
**and** that every input its executed commands opened still has its recorded
sha256 at REV.

## 2. The input-keyed rule (O, contract C; design binding for round 17)

Seat cold-read reports carry one fenced `json` block, schema
`tameshi-coldread-report-v2`, with `read_rev` (the 40-hex lane commit the
seat's clone was at), per section `inputs` (lane-relative path → sha256:
every lane-tracked file the section's executed commands opened, plus every
lane file the seat opened to check the section) and `external_inputs`
(absolute path or `repo@rev:path` → sha256).

Ledger v2 (`tameshi-coldread-ledger-v2`) keeps every v1 field and adds
`read_rev`, `inputs`, `external_inputs`. `measure.py --rev REV` credits an
entry as follows:

- Verdict, `blocking_gaps`, `wrong_expectations` and class conditions are the
  v1 rule, unchanged (`entry_credit_reason`).
- If `commands_executed_count > 0`: the entry credits only when `inputs` is
  non-empty and each input path's blob at REV has the recorded sha256.
  Otherwise the reasons are `inputs-unrecorded`, `input-missing:<path>`,
  `input-drift:<path>`.
- If `commands_executed_count == 0`: the v1 rule applies, with no input check.
  (v1 already refuses an `instruction` entry with zero executed commands:
  `commands-executed-count:0`.)
- `external_inputs` are reported, never credited.

`read_rev` is recorded for provenance; the credit check does not read it [I
— from contract text].

## 3. How inputs are traced (O for the probe; contract for the helper)

`trace-inputs.py --root DIR [--cwd DIR] --out FILE -- ARGV...` runs `ARGV`
under `strace -f -qq` and writes `tameshi-trace-inputs-v1` JSON: `argv`,
`cwd`, `root`, `rev` (`git rev-parse HEAD` of root, or null), `exit`,
`inputs` (`{rel: sha256}` for successful opens of regular files under root,
excluding `.git/`) and `external` (`{abs: sha256}` for regular files under
`/home` outside root). The command's stdout and stderr pass through.

What the raw trace shows (strace 7.2, `-f -qq -e trace=openat,open,openat2,execve`,
this host, 2026-10-20):

- One line per syscall, PID-prefixed, with the path **as passed**:
  `openat(AT_FDCWD, "<path>", O_RDONLY) = 3`. Child processes appear under
  their own PIDs.
- Failed opens are present: `… = -1 ENOENT (No such file or directory)`.
- Write-mode opens are present: `O_WRONLY|O_CREAT|O_TRUNC`.
- A symlink is recorded by the link name, not its target.
- Reads outside root (`/etc/passwd`, `/usr/lib/locale/…`) and `execve` of
  binaries (`/usr/bin/cat`) are present.

Consequences the helper must handle (the first three are open items, not
decided rules):

1. **Absence.** The contract records only successful opens, so a file that
   a command probed, found missing, and that later exists is undetected.
   Options: record `-1 ENOENT` probes as absence entries, or state the gap in
   the receipt.
2. **Writes.** A write-mode open under root would record a command's own
   output as an input. The next measure would then report `input-drift` on
   that file. Options: exclude `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC` opens from
   `inputs` and list them separately.
3. **Symlinks and hash timing.** Key by `realpath`, or a link into an
   outside file hides the outside bytes behind an in-root key. The contract
   does not say when `sha256` is taken; a file changed during the run would
   record its later bytes. Options: hash at exit with a size+mtime check
   before and after, or hash at open.
4. **Scope of `external`.** Only regular files under `/home` are recorded.
   Interpreters, `/etc` files and locale data are read in the trace but not
   recorded (§4).

## 4. Limits: what the input set does not contain (O / I)

| undeclared input | why it is not in `inputs` | status |
|---|---|---|
| interpreter and toolchain binaries (`node`, `python3`, `bash`) | exec'd outside root and outside `/home`; `external` does not cover them | not recorded; `process.execPath` is the case in `incremental-pin-disposition.md` §5a |
| environment variables (`PATH`, `TMPDIR`, `LC_*`, `GIT_DIR`) | not an open | not recorded |
| files read through an inherited fd or stdin | no `openat` | not recorded |
| network reads | no file open | not recorded |
| file mode bits (exec bit) | `sha256` is over bytes only | not recorded; the round-10 checklist-run SETUP (`100755` lost, exit 126) is the case in `incremental-pin-disposition.md` §5a |
| time and resource budgets (`CT=1` timing input) | not an open | not recorded |
| files absent at run time and later created | ENOENT not recorded (§3.1) | open unless absence entries are added |
| files changed during the run | depends on hash timing (§3.3) | open |
| section-to-section dependency (a bucket relies on another bucket's text) | the bucket's sha covers only its own bytes | not keyed |
| files a seat opened to check a section | self-reported, not traced | unverified; the seat's report is the only source |

A credited bucket with a clean input set is "every recorded input unchanged
at REV". It is not "the bucket's instructions are correct for every
environment".

## 5. How to re-measure (O for commands; outputs NOT RUN here)

1. Pin the revision: `REV=$(git -C <lane> rev-parse HEAD)`.
2. Count:
   `python3 .ufo/evidence/round-17/measure.py --rev "$REV" --ledger-rev "$REV:.ufo/evidence/round-17/coldread/ledger.json"`
   Exit 0 measured; 2 a rev or blob is missing; 64 usage. Use `--ledger-file PATH` to measure a working-copy ledger.
3. Check one bucket by hand: for each path in its `inputs`,
   `git -C <lane> show "$REV:<path>" | sha256sum` must equal the recorded value.
4. Red-before: `measure.py --selftest` includes a case where input drift
   uncredits an otherwise credited bucket. A selftest that cannot fail on
   that case is not evidence.
5. Trace a new command:
   `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --root <lane> --out "$D/t.json" -- <argv>`.

Record REV, the ledger's sha256, and each exit. A bucket with drifted inputs
at REV is uncredited. It is re-read by a new seat report with a new
`read_rev`; it is not re-judged in place.

## 6. Boundaries and unknowns (U)

- Only the round-16 CR26 bucket is observed in the closure. The other round-16
  buckets' input sets are unmeasured until round-17 wave 2 produces them.
- The sectionizer toggles fences on ```` ``` ```` only (`measure.py` :111
  region). The round-16 closure's independent sectionizer also excluded `~~~`.
  SKILL.md at 98bea7d has no `~~~` line, so no current bucket differs. The
  rule here is the ```` ``` ```` rule.
- `strace` availability is checked by the helper (exit 2 when absent); the
  version it was validated with is 7.2 on this host. Other versions are not
  established.
- Whether the tracer's open-mode, symlink and hash-timing decisions (§3) are
  settled is L1's integration call. This entry names them as open.
- No generality claim. This is one lane's cold-read ledger; no second lane
  is cited.
````

## E. Handoff notes for L1

- Replace `S0xx` markers. The lesson, the `measure.py` line references and the strace probe are the three citable sources; the strace probe needs a `[INFERENCE]` or `[O]` tag per L1's convention.
- Before this entry is final, decide F2 (absence and writes) and F3 (realpath and hash timing) in X08's helper. The draft lists them as open. If X08 lands them, §3 items 1–3 become rules, and §4's rows change.
- The `recheck:` line depends on the round-17 helpers being committed. Until then it reads NOT RUN, as written.
- `ground:` frontier id is yours.
