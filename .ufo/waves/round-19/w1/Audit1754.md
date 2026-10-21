# Audit1754 — round 19 w1 reviewer findings (advisory, not closure)

Seat `TameshiR19-2.Audit1754`, 2026-10-21 (checked at 02:55:36 -03:00). This serves C1's
verification and no-harm boundary only: is a retained round-18 receipt bound and honest, and
can the C1 repairs invalidate it? This report does not claim expansion or promotion.

## Read set and method

- Receipt pair: `.ufo/evidence/round-18/final/audit-1754.stdout` (6382 B, 81 LF) and
  `.stderr` (0 B). Trace: `.ufo/evidence/round-18/coldread/traces/L1/audit-1754.json`
  (5945 B).
- Ledger entry: `.ufo/evidence/round-18/coldread/ledger.json:12388-12431` (schema
  `tameshi-coldread-ledger-v2`, start 1754). Its referenced seat row:
  `.ufo/waves/round-18/w3/L1Residual.md:516-567`. The routed list in
  `corpus/lessons/round-18-verifier-spotcheck.md` §5 (:180-208).
- Git was used read-only (`cat-file`, `rev-parse`, `merge-base`, `log`,
  `diff --name-status`, and `diff -U0 -- SKILL.md`) with `GIT_*` removed and
  `GIT_OPTIONAL_LOCKS=0`. No index, ref, or JJ writes were made.
- The receipt argv was **not** executed. I did not read the contents of other receipts; they
  were compared by blob digest only. I did not read or run any measure script. I ran no
  tests, builds, or formatters and installed no tools.

Axes: A1 stdout binding · A2 argv binding · A3 revision/input facts · A4 claim honesty ·
A5 C1 no-harm.

## Established (observation)

1. **Stdout hash (A1).** The retained stdout has sha256 `e4764d511a33a3ad7d76c94e1bc405d8e9c52b11dc8fd243936430f529889846`
   (6382 B, 81 LF). The stderr is empty (`e3b0c442…b855`). I rebuilt the script's print path
   from the `a9c94c5` git blobs with my own code (below), without running the receipt argv.
   The result is byte-identical: same sha256, 6382 B.

   The trace records `"exit": 0`. Together with the empty stderr and the final VERIFIED
   line, this is consistent with all nine assert executions having passed.
2. **Argv binding (A2).** The argv spec at trace line 34 is
   `{"start":1754,"end":1804, 15 paths}`. It matches stdout line 1, `SECTION 1754 1804`.
   - The `OPEN` lines appear in exactly `spec.paths` order (15/15).
   - Every `OPEN` sha256 and `bytes=` value equals both the trace `inputs` and the
     `a9c94c5` blob.
   - Trace `inputs` = spec paths + `SKILL.md` (`1334c512…`), which the script reads to print
     the section.
3. **Revision and input facts (A3).**
   - Trace `rev` = ledger `read_rev` = `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`
     (commit time 2026-10-20 18:46:21 -0300).
   - All 16 recorded input digests equal the git blobs at `a9c94c5`, `a134a09`, `a85f710`,
     `4b7c682`, and the frozen baseline `7243e7f`.
   - Ledger `inputs` = trace inputs minus `SKILL.md`, by exact dict equality, with
     `inputs_dropped: ["SKILL.md"]`. Ledger `skill_sha256` = the trace's `SKILL.md` digest.
   - Seat row `L1Residual.md:546-561` (inputs) and `:529-545` (opened) contain the same sets.
   - Ledger section `sha256` `b43ed7be…` = sha256 of `'\n'.join(SKILL.md lines 1754–1804)`
     at `a9c94c5`. The ledger's `end: 1805` points at a blank line, and line 1806 is
     `### Round-16 gate/probe registry`. So 1804 vs 1805 is an extent convention, not a
     content gap.
   - This ledger entry is identical at `a134a09`, `a85f710`, `7243e7f`, HEAD, and the
     worktree.
4. **Retention.**
   - The trio was added once, in `a134a09` (2026-10-20 18:47:13, child of `a9c94c5`), and
     never modified since.
   - Blobs: stdout `2c27151a…`, stderr `e69de29b…`, trace `238ff14f…`. These are identical
     at `a134a09`, `a85f710`, `4b7c682`, `7243e7f`, HEAD `21e7932`, and the worktree.
   - File mtimes (18:47:00) fall between the two commits. This is weak corroboration, since
     mtimes can be changed.

## Findings (by severity)

### M1 — The VERIFIED line prints an ancestry claim the script never computes (A4)

- The final stdout line (:81, retained in `a134a09`, 2026-10-20): "VERIFIED actual execution
  receipts; ancestor runs have the same instrument blobs as the read revision".
- The argv script (trace JSON line 33) contains no git, rev, ancestor, or subprocess logic.
  The string is printed unconditionally once the asserts pass. The receipt therefore
  establishes neither instrument-blob identity nor any run revision.
- The claim actually rests on the seat note at `L1Residual.md:524` (2026-10-20): "Real
  command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds
  only citation/receipt files and the D/N prose correction, not executable instruments."
- My own metadata corroboration (not the receipt's):
  - The `tools/mutate-and-run.sh` blob `fd1a63a3…` is identical at `921ef807`, `5923d89`,
    and `a9c94c5`.
  - No path outside `*.md/*.json/*.stdout/*.stderr/*.txt` changed in `921ef807..a9c94c5` or
    `5923d89..a9c94c5`. This is an extension-based heuristic; the set of "instruments" is
    never defined.
  - This pair does not record the revision each receipt was run at.
- Failing criterion: a line labelled VERIFIED must be computed. This is outside C1. Route it
  as a named limitation via an appended erratum. Do not rewrite the retained stdout.

### M2 — `final/checks.json` is opened and hashed but never asserted; it is the §5.4 defect file and couples 17 retained reads (A4/A5)

- `final/checks.json` (`fed3c8e6…`, 2411 B) appears in OPEN and in inputs, but the script
  asserts nothing about it.
- 6 of the 15 opened files are digest-only: checks.json, context.stdout, predictions.json,
  round-gate.defects.spec, tools/mutate-and-run.sh, and the knowledge note.
- The routed list (spotcheck :196-200, committed in `7243e7f`, 2026-10-21) places a failed
  exit-64 selftest row in that file. "VERIFIED actual execution receipts" therefore cannot
  be cited as vouching for the contents of checks.json.
- 17 of the 159 ledger entries (61 unique sections) list `final/checks.json` as an input:
  starts 131, 921, 965, 1021, 1069, 1164, 1212, 1436, 1479, 1676, 1707, 1754, 1814, 1846,
  1855, 1905, 1925.
- At `21e7932`, C1 repaired §5.4 by appending new
  `.ufo/evidence/round-19/bash-witness-selftest*.{json,stdout,stderr}` files.
  `checks.json` is unchanged, so nothing is invalidated.
- Taking §5.4 literally — "Do not leave a failed invocation as the selftest row of the final
  receipt bundle." — and rewriting checks.json in place would break digest agreement for all
  17 entries.

### L1 — SKILL.md whole-file digest drift at the delivered tip (A5; integrator check needed)

- `21e7932` changes SKILL.md from `1334c512…` to `4d0190fd…` by appending one row at line
  1935 (the `round-19/measure.py` row).
- Section 1754–1805 is byte-identical at the same line numbers. The ledger section sha256
  `b43ed7be…` reproduces at HEAD and in the worktree.
- The ledger still keeps the per-entry `skill_sha256: 1334c512…`, which is now stale, while
  dropping SKILL.md from `inputs`.
- **UNKNOWN within my read scope:** whether the strict cold-read counter keys on the
  whole-file `skill_sha256` or on the section hash.
  - If it keys on the whole file, every entry recorded at `1334c512` is stale at `21e7932`.
    That would threaten the "calibration 8 unchanged" boundary.
  - Round 18 gives no observation of this, because SKILL.md was constant from `a9c94c5`
    through `7243e7f`.
  - Input-digest edits do invalidate reads: see commit `a85f710` (2026-10-20), "refresh T2
    section after lesson citation edit invalidated one retained read".

### L2 — Neither the trace nor the ledger binds the stdout/stderr by digest (A1)

- The trace schema `tameshi-trace-inputs-v1` has the keys argv, cwd, dropped_home_count,
  env_overrides, exit, external, inputs, live_lane_reads, rev, rev_reason, root, schema,
  tracked_filter, and untracked. There is no stdout/stderr path or digest.
- The ledger entry names only the trace.
- I grepped `.ufo`, `corpus`, `SKILL.md`, `SCORECARD.md`, and `LOG.md` for
  `e4764d51|2c27151a0791|a7105fdf81e5|238ff14fa105` and found no matches.
- The binding is therefore only filename convention, content consistency (item 1), and git
  history.

### I1 — `env_overrides` describes the tracer, not the measured process (A2)

- `env -i` in argv (JSON lines 21–22) clears the recorded `set.PYTHONPYCACHEPREFIX`.
- argv then re-sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` (lines 26–27),
  which `env_overrides` lists as `git_vars_removed`.
- Neither affects the output: the script runs no git, and `-c` code writes no bytecode.

### I2 — The environment identity is not pinned (A2)

- `python3` is resolved through the recorded PATH, which puts user shim dirs before
  `/usr/bin`.
- The trace has no field for the interpreter path or digest, the bwrap version, or how the
  scratch tree was materialized and whether it was clean. `tracked_filter: true` with
  `untracked: {}` shows the files were tracked, not that they were unmodified.
- Items 1 and 3 mitigate this for this receipt.

### I3 — What "commands_executed" means for an instruction-class section (A4; no extrapolation)

- The ledger has `class: instruction` and `commands_executed_count: 1`. That single command
  is the receipt audit (`L1Residual.md:527`).
- It did **not** run:
  - the section's reproduce block (`git show 364f1d5…` and the `mutate-and-run.sh` sweep)
  - the survivor probes
- It did **not** check:
  - kumitate blob `f890e277…`
  - `CONTROL: GREEN` or `MUTATE_RESTORE: OK`
  - the prediction outcomes
  - the 1059/1060 edge
- Beyond digests, it establishes only these facts:
  - registry: held==total==31
  - probes: `open=0 closed=11 total=11`
  - regression: `cases=8 passed=8`
  - historical: `cases=4 passed=4`
  - case7 and case8: `killed=5 survived=5 inconclusive=0 kill-rate=50%`
  - disposition: status clean
  - before: status failed
  - repeat: contains `controls_match`. This is a substring test, not a field check, so it is
    weaker. I did not read repeat.stdout.

## Can the C1 repairs invalidate this historical evidence?

- **As landed (`78b99dd`, `21e7932`; the worktree was identical at check time): no** for the
  receipts, the section, and the 15 ledger inputs.
  - `7243e7f..HEAD` touches no `.ufo/evidence/round-18/**` path; every `.ufo` change is an
    addition under round 19.
  - C1 modified LOG.md, SCORECARD.md, SKILL.md, corpus/QUALITY.md, corpus/README.md,
    corpus/SOURCES.md, guard-kill-closure.md, mutation-case-kumitate-sources-check.md, and
    lessons/round-18.md. These overlap this entry only at SKILL.md, and its section is
    intact.
  - Still open: L1.
- **Moves that would invalidate it:**
  - editing `final/checks.json` in place (17 entries) or any of the other 14 recorded inputs
  - adding or removing lines above SKILL.md:1754, or editing lines 1754–1804, since both the
    line-keyed name and the section hash depend on them
  - rewriting the retained stdout or trace, for example to "fix" M1
  
  Per Contract, corrections must be appended errata.
- The historical fact itself, "read at `a9c94c5`", survives later edits because git
  preserves the blobs. What later edits can break is the claim that the read still holds at
  the delivered revision.

## Residual risk and verification gaps

- **Integrator:** run the round-18 strict cold-read counter (no override) at the delivered
  revision and confirm 60/60 with SKILL.md `4d0190fd…`, or confirm that the counter binds
  SKILL only through the section hash (L1). I did not run it; it is outside my scope.
- I did not read the contents of the nine asserted receipts or of checks.json. Nothing here
  verifies them beyond the asserted strings.
- The mtime and timing corroboration is weak. No resume path is in scope, so
  `resume_continuity_v1` does not apply.

## Commands and code (read-only)

`sha256sum`/`wc`/`ls --time-style=full-iso` on the trio, plus the git queries named above.
I used in-memory Python only, with no scratch files:

```python
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}; ENV['GIT_OPTIONAL_LOCKS'] = '0'
blob = lambda rev, p: subprocess.run(['git','-C',L,'cat-file','blob',f'{rev}:{p}'],capture_output=True,env=ENV).stdout
spec = json.loads(trace['argv'][-1]); R = 'a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4'
ln = blob(R, 'SKILL.md').decode().splitlines()
buf = [f"SECTION {spec['start']} {spec['end']}", '\n'.join(ln[spec['start']-1:spec['end']])]
for p in spec['paths']:
    raw = blob(R, p); buf.append(f"OPEN {p} sha256={sha256(raw).hexdigest()} bytes={len(raw)}")
    if p.startswith('corpus/knowledge/'):
        buf += [raw.decode().splitlines()[0], 'TAIL ' + raw.decode()[-700:]]
buf.append('VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision')
assert ('\n'.join(buf) + '\n').encode() == retained_stdout   # held: sha256 e4764d51…9846
# per rev in {a9c94c5,a134a09,a85f710,4b7c682,7243e7f,HEAD}+worktree: sha256(blob(rev,p)) == trace['inputs'][p]
# ledger: sha256('\n'.join(SKILL lines 1754..1804)) == entry['sha256']; entry['inputs'] == trace inputs - SKILL.md
```

Tool installs or updates: none.
