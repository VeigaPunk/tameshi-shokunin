# Audit1676 — round-18 L1 receipt `audit-1676` (tameshi round 19, w1, advisory)

Seat `TameshiR19-2.Audit1676` (reviewer, read-only), 2026-10-21. These findings are advisory and do not close anything on their own.
Scope: `.ufo/evidence/round-18/final/audit-1676.{stdout,stderr}`, `.ufo/evidence/round-18/coldread/traces/L1/audit-1676.json`,
and their ledger entry `.ufo/evidence/round-18/coldread/ledger.json` `entries[150]` (lines 12302–12345). Its referenced report entry is
`.ufo/waves/round-18/w3/L1Residual.md:416-467`. I did not re-execute anything, did not re-run any assertion, and made no git or jj writes.

**Verdict.** The receipt is internally consistent, and its inputs are byte-pinned to `a9c94c5`. Nothing records the stdout digest as an expected value.
The final `VERIFIED` line claims more than the recorded program measures. The C1 repairs at the delivered revision `21e7932` do **not**
invalidate this historical evidence.

Axes: stdout-digest binding · argv binding · revision/input facts · claim-vs-code · C1 no-harm.

## Objects (observed)

| Object | sha256 / bytes | git blob (prefix) | History |
|---|---|---|---|
| `final/audit-1676.stdout` | `1f9f18715f69db3d19d130b8511bca414b71fa1ab98178b03b0d390d2a6ae7a8` / 6099 B, 47 LF lines | `24bcafb858` | Only `a134a09` (2026-10-20T18:47:13-03:00). Identical at `a85f710`, `4b7c682`, `7243e7f`, `21e7932` and in the working tree |
| `final/audit-1676.stderr` | `e3b0c442…b855` (empty) / 0 B | `e69de29bb2` | Same history |
| `coldread/traces/L1/audit-1676.json` | `8378b05af142674ba3454d3728fcd521cdb840bb91b536dc0fde8608f5759a66` / 5851 B | `b0640d1d34` | Same history |
| `coldread/ledger.json` | — | `131510f720` | `a134a09`, then `a85f710`. The `entries[150]` JSON is identical at `a134a09`, `a85f710` and `21e7932` |

## Findings by severity

### M1 — Medium (advisory; not one of C1's five): the `VERIFIED` line asserts facts the program never measures

- Source: `audit-1676.stdout:47` (retained `a134a09`, 2026-10-20) reads “VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision”.
- Program (`audit-1676.json:33`): after the OPEN loop it runs 9 assertion checks over 9 receipt files, then prints that literal unconditionally:
  - registry `held==total==31`
  - probes `open=0 closed=11 total=11`
  - regression `cases=8 passed=8`
  - historical `cases=4 passed=4`
  - case7 and case8 `killed=5 survived=5 inconclusive=0 kill-rate=50%`
  - disposition `status=='clean'`
  - before `status=='failed'`
  - repeat `controls_match`
- The program has no git call, no ancestor revision, no instrument-blob comparison, and no check of the argv, exit code or revision behind any receipt.
- Four files are only hashed, never parsed: `checks.json`, `context.stdout`, `round-18/dispositions.json` and `round-14/context-receipt.json`.
- "Actual execution" is therefore not established. Substring and field checks cannot tell an execution transcript from authored text.
- Concrete consequence: the unparsed `checks.json` (`fed3c8e6…`, blob unchanged from `a9c94c5` to `4b7c682`) is the file in which the verifier found
  “`final/checks.json` records `bash-witness-selftest` argv exit 64 with an empty stdout”
  (`corpus/lessons/round-18-verifier-spotcheck.md:196-197`, committed `7243e7f` 2026-10-21). So `VERIFIED` was printed over a bundle that contains a failed invocation row.
  I relied on the spot-check for the row content and did not re-read the file.
- Independent truth test (my own git tree reads; the receipt does not establish this). L1Residual.md:424 names the ancestors “ancestor-pinned (921ef807/5923d89)”.
  - `tools/context-capture.py` (`992d0a3e8b`) and `tools/evidence-disposition.py` (`6838762217`) are identical at `921ef807`, `5923d89` and `a9c94c5`.
  - `diff --raw 921ef807 a9c94c5`: 53 paths. The only path outside `.ufo/` and `corpus/` is `SKILL.md`. No path is executable-mode or has a script extension.
  - `5923d89..a9c94c5`: 6 paths, all inside `.ufo/` or `corpus/`, none of them scripts.
  - So the sentence is true at that scope but unproven by the receipt. The evidence never says which receipt came from which ancestor.
- Family-wide (literal grep): the same string is in all 17 L1 `audit-*.json` traces and their `.stdout` files. It appears in no C1-changed file.
- Failing criterion: a `VERIFIED` line must be conditioned on a check that measures it.
- Route: append a dated, named erratum that scopes the L1 line to "the 9 listed substring/status assertions passed over committed receipt text at `a9c94c5`".
  Never rewrite the receipts. This does not block C1. Do not cite this line as proof of ancestor identity or of execution.

### L1 — Low: no output-digest binding exists, so the stdout hash can only be recomputed

- The trace schema `tameshi-trace-inputs-v1` keys are `schema, argv, cwd, root, rev, rev_reason, exit, tracked_filter, env_overrides, inputs, untracked, external, live_lane_reads, dropped_home_count`.
  There is no stdout or stderr digest.
- Ledger `entries[150]` and `L1Residual.md:416-467` record only the trace path, with no stdout digest and no trace digest.
- A literal grep of the lane (gitignore off) for the stdout sha256, the trace sha256 and the stdout blob prefix found no match.
- What binds stdout to argv: the filename stem, co-retention in `a134a09`, and the content consistency shown below. Only git history makes tampering detectable.

### L2 — Low: this receipt covers the section's instructions only partly; ledger counts are not command completeness

- Section 1676–1705 contains two registry rows (`stdout:6-7`). They name:
  - entry commands: `context-capture.py --check`; the superseded round-14 disposition command; the live round-18 entry; a frozen replay from `git archive 28aeef4`
  - two `--selftest` commands
- The receipt runs none of them. Its assertions touch only `disposition.stdout` (clean) and `before.stdout` (failed). `context.stdout` is only hashed.
  No selftest receipt is asserted, and the frozen-replay claim is untested. Which command produced `disposition.stdout` is not established.
- Ledger `entries[150]` records `commands_executed_count: 1`, `wrong_expectations: 0`, `verdict: gap-minor`. L1Residual.md:424 discloses “L1 residual verification is not a blind non-author cold read.”
  So "0 wrong expectations" means none were detectable by this receipt for most of the row content.
- C1 already disclaims the inference: “No current-page full-read/command-completeness inference follows from these historical receipts.” (`SCORECARD.md:717-718` @`21e7932`, 2026-10-21).

### I1 — Info: ledger range ends at 1706, the executed range at 1705; no content gap

- argv spec `{"start": 1676, "end": 1705}` and `stdout:1` `SECTION 1676 1705`, while ledger `entries[150]` says `"end": 1706`.
- `SKILL.md@a9c94c5` line 1706 is empty; line 1707 is `## Errata — round 16 full-page cold-read`.
- The ledger `sha256` `b814e0afbad4c270…` equals sha256 of the lines 1676–1705 joined with `\n` and no trailing newline. The 1676–1706 variants give `772b853b…` and `220e17fa…`.
- So the ledger's section identity is exactly the printed content; only the coordinate is off.

### I2 — Info: `env_overrides` is not the child's effective environment

- The trace's `set` contains `PYTHONPYCACHEPREFIX`, and `git_vars_removed` lists `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM`.
- The argv's `env -i` clears the former and re-sets the latter (`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`).
- No effect here: the program makes no git call and `PYTHONDONTWRITEBYTECODE=1` is re-set. But the field records what the tracer changed, not what the child saw.

### I3 — Info: execution identity is not recorded; input digests do not single out `a9c94c5`

- `python3` is resolved through the recorded PATH, which lists user directories (`~/.grok/bin`, `~/.kimi-code/bin`, mise shims, fnm…) before `/usr/bin`.
- Not recorded: interpreter path, version or digest; tracer tool digest; timestamp.
- Today that PATH resolves to `/usr/bin/python3`. This is current state, not historical evidence.
- [INFERENCE] Run window, assuming truthful committer clocks: `a9c94c5` was committed at 18:46:21-03:00, and its only child `a134a09`, which retains the receipts, at 18:47:13-03:00 (2026-10-20). The run fell in that ≤52 s window.
- The same 16-input set exists at `4b7c682`, `7243e7f` and `78b99dd` (`SKILL.md` blob `4bb239c9` is unchanged until `21e7932`). `rev` is the tracer's assertion; the commit ordering is consistent with it.

## Facts this evidence does establish (observed)

1. The stdout has 47 lines: 1 `SECTION`, 30 section lines, 15 `OPEN` lines and 1 `VERIFIED`. That is exactly the recorded print sequence; no path is under `corpus/knowledge/`, so there are no `TAIL` lines.
2. `stdout:2-31` equals `SKILL.md@a9c94c5` lines 1676–1705, compared line by line.
3. The 15 `OPEN` paths equal the argv spec paths in the same order. Their digests equal the trace `inputs`, and their byte counts equal the blob sizes at `a9c94c5`.
4. All 16 trace input digests equal the sha256 of the blobs at `a9c94c5`. This includes `SKILL.md` `1334c512…`, which matches ledger `skill_sha256` and the ledger `_meta.pages` entry (rev `a9c94c5`, 60 buckets).
5. Ledger vs trace:
   - Ledger `inputs` equal trace `inputs` minus `SKILL.md`, which the ledger lists under `inputs_dropped`.
   - `read_rev` equals trace `rev`.
   - `traces` is `[audit-1676.json]`.
   - `L1Residual.md:429-461` `opened` and `inputs` match.
6. The argv `--chdir` path equals the trace `cwd` and `root`. The tracer reports `untracked {}`, `external {}`, `live_lane_reads {}` and `dropped_home_count 0`; the tracer's own identity is not recorded.
7. `exit 0` and a 0-byte stderr are consistent with all 9 assertion checks passing [INFERENCE — the assertions were not re-run, per contract].

## C1 impact: is this historical evidence invalidated?

**No.** Revisions observed:
- `7243e7f` (2026-10-21T00:51:38-03:00, spot-check)
- `78b99dd` (02:28:10, freeze)
- `21e7932` (02:48:27, “round-19: correct routed metadata and retain effective historical receipts”), which is `master` and `origin/master`

What C1 left unchanged:
- The receipt pair, the trace, `ledger.json` and `L1Residual.md` are byte-identical at `7243e7f`, at `21e7932` and in the working tree.
- 15 of the 16 inputs are byte-identical from `a9c94c5` through `21e7932` and in the working tree. That includes the defect-4 surface `final/checks.json` (`fed3c8e6`).
  - C1 *added* `.ufo/evidence/round-19/bash-witness-selftest*.{json,stdout,stderr}` (status A).
  - C1 explicitly rejected overwriting `checks.json`: “Reclassify historical failed invocations as passing or overwrite checks.json | reject | would erase the observation that failed” (`corpus/lessons/round-19.md` @`21e7932`, 2026-10-21).
- `SKILL.md` changed only by a one-line append at end of file: `@@ -1934,0 +1935 @@` with 0 deletions, registering `.ufo/evidence/round-19/measure.py`.
  - Section 1676–1705 is identical at the same coordinates, the section sha `b814e0af…` is unchanged, and line 1706 is still empty.
  - The uncommitted working copy (mtime 2026-10-21T02:54:34) appends one more line at end of file (1936). The section is still identical.
- The files for defects 1–3 and the defect-5 surfaces are not inputs of this receipt. The C1-modified text files have 0 deleted lines:
  - `LOG.md`, `SCORECARD.md`, `SKILL.md`
  - `corpus/QUALITY.md`, `corpus/README.md`
  - `corpus/lessons/round-18.md`, `corpus/lessons/round-19.md`
  - `corpus/knowledge/guard-kill-closure.md`, `corpus/knowledge/mutation-case-kumitate-sources-check.md`

Expected, disclosed side-effect:
- The trace's `SKILL.md` digest `1334c512…` no longer matches the live file (`4d0190fd…` at `21e7932`, `b653979a…` in the working copy). So this receipt is not a current-page read at any round-19 revision.
- C1 disclaims that (`SCORECARD.md:717-718` above), and `corpus/lessons/round-18.md:154-155` @`21e7932` says “nor that 60/60 holds at any round-19 revision”.

What would invalidate it (none observed):
- an in-place rewrite of any of the 15 retained inputs, especially `checks.json`
- an insertion above `SKILL.md:1676`, which would shift the coordinates
- a rewrite or deletion of the receipt pair, the trace or the ledger entry
- C1 citing the M1 line as proof

Grep: `audit-1676` appears only in `ledger.json`, `L1Residual.md` and the round-19 wave assignment files.

Bearing on C1: the defect-4 surface is one of this receipt's inputs. Because C1's repair is append-only, the receipt's input digests can still be checked at the delivered revision, so the no-harm boundary holds for this receipt. This audit does not measure the 5/5 claim itself.

## Residual risk and verification gaps

- The exit-64 content of `checks.json` comes from the spot-check; I did not re-read it (outside scope). Identity rests on the unchanged blob.
- The assertions were not re-run, so their outcomes are inferred from `exit 0` and the empty stderr.
- What the tracer's `external` / `tracked_filter` exclude is unknown without the tracer source (outside scope).
- The M1 pattern spans 17 L1 receipts; only `audit-1676` was audited here.
- The jj working copy holds an uncommitted `SKILL.md` change. I assessed only the section identity.
- No `lsp` device is available in this session. Literal grep was used only to check whether digests and strings are present; it is not semantic proof.

## Method (read-only) and code text

Git commands used: plumbing only, inherited `GIT_*` removed, `GIT_OPTIONAL_LOCKS=0` set defensively, no writes.
- `rev-parse --verify`, `cat-file blob REV:PATH`, `hash-object` (no `-w`)
- `log --format=%h %cI %an %s -- PATH`, `rev-list --parents -n1`
- `merge-base --is-ancestor`: `a9c94c5` → `a85f710` → `4b7c682` → `7243e7f` → `21e7932`, all true
- `for-each-ref`
- tree-to-tree `diff --name-status|--raw|-U0` (`7243e7f..21e7932`, `921ef807..a9c94c5`, `5923d89..a9c94c5`)

```python
import os, subprocess, json, re, hashlib
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; ENV={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}|{'GIT_OPTIONAL_LOCKS':'0','LC_ALL':'C'}
def g(*a, binary=False):
    r=subprocess.run(['git','-C',L,*a],env=ENV,capture_output=True,check=True)
    return r.stdout if binary else r.stdout.decode()
t=json.load(open(L+'/.ufo/evidence/round-18/coldread/traces/L1/audit-1676.json')); spec=json.loads(t['argv'][-1]); A='a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4'
out=open(L+'/.ufo/evidence/round-18/final/audit-1676.stdout').read().splitlines()
op=[re.fullmatch(r'OPEN (\S+) sha256=([0-9a-f]{64}) bytes=(\d+)',l).groups() for l in out if l.startswith('OPEN ')]
assert [p for p,_,_ in op]==spec['paths'] and all(t['inputs'][p]==h for p,h,_ in op)
assert all(hashlib.sha256(g('cat-file','blob',f'{A}:{p}',binary=True)).hexdigest()==h for p,h in t['inputs'].items())
sl=g('cat-file','blob',f'{A}:SKILL.md').splitlines(); assert out[1:31]==sl[1675:1705]
assert hashlib.sha256('\n'.join(sl[1675:1705]).encode()).hexdigest().startswith('b814e0af')   # ledger entries[150].sha256
# per input: blob id at a9c94c5 / 4b7c682 / 7243e7f / 78b99dd / master, via rev-parse REV:PATH -> only SKILL.md differs (at 21e7932)
```

Tooling: nothing installed or updated. Production, refs, index and jj state are untouched; this report is the only file written.
