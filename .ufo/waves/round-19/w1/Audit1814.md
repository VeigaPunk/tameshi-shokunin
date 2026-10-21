# Audit1814 — round 19, w1 (seat `TameshiR19-2.Audit1814`)

Date: 2026-10-21. Read-only reviewer. These findings are advisory and do not close anything.

**Scope.** I read these files:
- `.ufo/evidence/round-18/final/audit-1814.stdout` and `.stderr`
- `.ufo/evidence/round-18/coldread/traces/L1/audit-1814.json` (the trace)
- the ledger entry at `.ufo/evidence/round-18/coldread/ledger.json:12432-12477` and its report block at `.ufo/waves/round-18/w3/L1Residual.md:568-623`
- `corpus/lessons/round-18-verifier-spotcheck.md` §5, to map the C1 defects

All paths are relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

**What I did not do.** I did not re-run the receipt argv. I ran no builds, tests, linters or formatters, installed nothing, and wrote nothing except this file. I ran no `jj` commands, because jj snapshots the working copy and imports refs.

**How I used Git.** Only read-only plumbing, as `git --no-optional-locks`, with the environment reduced to `PATH=/usr/bin:/bin HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C`.

**Axes:** byte integrity · binding from argv to stdout · whether revision and inputs are established · whether claims are honest · whether C1 does no harm.

## Verdict

- **Bytes, binding and input pins hold.** The record supports read revision `a9c94c5c` well, but it cannot be proven on its own (fact 7).
- **Finding F1 (Medium): the receipt's `VERIFIED` line cannot fail on what it claims.**
- **C1 does not invalidate this evidence.** This holds as committed at `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` and for the live working tree on 2026-10-21. Only one change could break it at the byte level: rewriting `round-18/final/checks.json` (defect 4) or another pinned input in place. Nobody has done that.

## Established facts

These are observations unless marked otherwise.

1. **Retained bytes.** Commands: `sha256sum`, `stat`, `git cat-file blob <rev>:<path>`, `git ls-files -s`.

   | File | Size | sha256 | Git blob |
   |---|---|---|---|
   | stdout | 5740 B | `e5f76ad4dc91f6bb1d10053f6abbc9f0573e61cdb31f612618ef6b3e33930937` | `125988b0` |
   | stderr | 0 B | `e3b0c442…b855` (empty) | `e69de29b` |
   | trace | 6107 B | `76a1caca8838cc8da11dcd1a82fa60ad3f129706f34a308789a38eeeacdf572d` | `09c579b2` |

   - All three files first enter history at `a134a09` (2026-10-20T18:47:13-03:00). Its only parent is `a9c94c5c`.
   - All three are byte-identical at `a134a09`, `4b7c682`, baseline `7243e7f1`, HEAD `21e79329`, and the live tree.
   - The ledger (`d654f3d2755c6c7b…`) and `L1Residual.md` (`51ce65e4143fff79…`) have not changed since `a85f710`.

2. **No recorded stdout or trace digest exists.** I grepped the whole lane (gitignore off, `.ufo` and `.jj` included) for `e5f76ad4dc91f6bb` and `76a1caca8838cc8d` and found 0 hits. The trace has no stdout field, and the ledger entry and the L1Residual block name only the trace. See F2.

3. **Stdout content matches the trace argv.** Compared against trace lines 33–34 (script and spec):
   - Stdout line 1 is `SECTION 1814 1844`, which equals the spec.
   - Stdout lines 2–32 are byte-exact copies of `SKILL.md@a9c94c5c` lines 1814–1844.
   - There are 17 `OPEN` lines, in spec order. Their sha256 values equal `trace.inputs`, and each `bytes=` value equals the blob length at `a9c94c5c`.
   - There are no `TAIL` lines, which is correct because no spec path is under `corpus/knowledge/`.
   - The last line is the script's literal final `print`.
   - Stderr is empty and the trace records `exit 0`.

4. **The asserts hold.** I evaluated each predicate myself over the `a9c94c5c` blobs, without running the argv. All 9 hold:
   - registry `held == total == 31`
   - probes `open=0 closed=11 total=11`
   - regression `cases=8 passed=8`
   - historical `cases=4 passed=4`
   - case7 and case8 `killed=5 survived=5 inconclusive=0 kill-rate=50%`
   - disposition `clean`
   - before `failed`
   - repeat `controls_match`

   This is consistent with exit 0.

5. **The ledger's section hash matches.** Source: `ledger.json:12433-12437`.
   - `skill_sha256` `1334c512…` equals the trace's `SKILL.md` input and the blob at `a9c94c5c`.
   - The section sha256 `dae48ab619051e3844dc322a85128e49bcc9286edf6031748a00c29feeeedd83` equals `sha256("\n".join(lines 1814..1844))`. That is also the hash of stdout lines 2–32.
   - The ledger says `end: 1845` and the argv says `end: 1844`. This is not a gap: line 1845 is blank, so the stdout printed the whole hashed section.

6. **Input pins are consistent everywhere.** For all 17 inputs other than `SKILL.md`, the hash is the same in `trace.inputs`, the stdout `OPEN` lines, the ledger, and `L1Residual.md:600-618`. It is also the same in the blobs at `a9c94c5c`, `a85f710`, `4b7c682`, `7243e7f1` and `21e79329`, and on the live tree.
   - The ledger's inputs equal the trace's inputs minus `SKILL.md`, matching its `inputs_dropped` field.
   - The L1Residual `opened` list equals the spec paths.

7. **Revision.**
   - `a9c94c5c` exists as a commit (2026-10-20T18:46:21-03:00). It is an ancestor of `4b7c682`, `7243e7f1` and HEAD.
   - The input fingerprint rules out the parent `5923d89` and `921ef807`, because `final/registry-branch-aligned.stdout` is absent at both.
   - The fingerprint does **not** tell `a9c94c5c` apart from `a134a09`, `a85f710`, `4b7c682` or `7243e7f1`, which all have identical inputs.
   - The revision therefore rests on two things: the producer-recorded `trace.rev`, and the commit order (the receipts first appear at `a134a09`, which is a child of `a9c94c5c`). [INFERENCE: no record of the scratch clone's HEAD was retained.]

8. **The "ancestor instruments" clause is true, but the receipt did not establish it.** I compared the six instrument inputs (`tools/evidence-disposition.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/pin-disposition.py`, `round-18/dispositions.json`, `round-18/dispositions-before.json`). Their blobs are identical at `921ef807`, `5923d89` and `a9c94c5c`.
   - `git diff --name-status 921ef807 a9c94c5c` has 53 entries: 51 receipt or trace additions under `round-18/final/` and `round-18/coldread/traces/`, plus modifications to `SKILL.md` and `corpus/lessons/round-18.md`.
   - The `SKILL.md` change is one hunk, `@@ -974,3 +974,3 @@`, outside lines 1814–1844. Lines 1814–1844 are identical at `921ef807`.
   - Nothing under `tools/` changed.

## Findings, by severity

### F1 — Medium (claim honesty; does not block C1): the `VERIFIED` line is unfalsifiable

- **Source.** `audit-1814.stdout:50` (2026-10-20): "VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision".
- **Why it cannot fail.** In the trace's script (`audit-1814.json:33`), this line is an unconditional literal `print`. The script contains no `git` call, no `subprocess`, no blob or revision comparison, and no ancestor IDs. It reaches `checks.json` only through the generic loop that hashes each path; it never parses it.
- **Criterion it fails.** A verification command must be able to fail on the claim it prints. No assert covers either clause.
- **Concrete consequence.** Among the inputs it hashed is `final/checks.json` (`fed3c8e6…`). Its `bash-witness-selftest` row has argv `["python3", "tools/bash-witness-study.py", "--selftest"]`, `"revision": "921ef807…"`, `"exit": 64`, and an empty-stdout `stdout_sha256` of `e3b0c442…`. That is routed defect 4. The command printed `VERIFIED` regardless.
  - `L1Residual.md:579` uses the same label: "committed actual-execution receipt audit".
- **Mitigation already in the record.** The ledger verdict is `gap-minor`. Its minor gap (`L1Residual.md:576`, 2026-10-20) discloses: "Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction". The ancestor clause is in fact true (fact 8).
- **Advisory.** This is outside C1's five items, and history stays immutable. If the lane corrects it, use an appended, dated erratum naming `audit-1814.stdout:50`, not an edit. No one should cite this line as evidence that the round-18 final bundle held only successful executions.

### F2 — Low (receipt hygiene): stdout and stderr digests are not recorded

- The trace schema `tameshi-trace-inputs-v1` has no stdout or stderr field (`audit-1814.json:1-76`).
- The ledger entry (`ledger.json:12432-12477`) and the L1Residual block point only to the trace.
- The lane's own `checks.json` records a `stdout_sha256` for each row, but that convention was not applied here.
- **Effect.** The stdout can only be checked against Git (blob `125988b0` at `a134a09`) and by content consistency (fact 3). The `audit-1814.*` files are paired with the trace only by naming convention.

### F3 — Low: the trace's `env_overrides` do not describe the measured process

- `audit-1814.json:42-51` records `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM` as removed, and `PYTHONPYCACHEPREFIX` as set.
- But the argv runs `env -i` (`:21-22`), which clears `PYTHONPYCACHEPREFIX` and sets both Git variables again (`:26-27`). Separately, `--tmpfs /tmp` (`:12-13`) hides `/tmp/trace-inputs-run-*` inside the sandbox.
- The effective environment is spelled out in the argv; the field describes the wrapper. This changes none of this receipt's facts.

### F4 — Low: the interpreter and tracer are not identified, and `external: {}` is a filtered category

- `python3` is resolved through a 16-entry `PATH` that includes user shim directories (`:23`). The trace records no resolved path, version or hash for it, and no name or version for the tracer.
- Importing `json`, `hashlib` and `pathlib` requires reading the standard library, so `external: {}` cannot mean "nothing outside the root was read". [INFERENCE] The filter rule is UNKNOWN; I did not open the producer (out of scope).
- Today, the only `python3` on that `PATH` is `/usr/bin/python3`, which resolves to `python3.14`. That is current, not historical.

## Could the C1 repairs invalidate this evidence?

**What changed under round 18.**
- `git log 7243e7f1..21e79329 -- .ufo/evidence/round-18 .ufo/waves/round-18` is empty.
- `git diff --name-status 7243e7f1 21e79329` touches no path under round 18.
- The working-tree diff against HEAD covers only `round-19/measure.py`, `LOG.md`, `SCORECARD.md` and `corpus/lessons/round-19.md`. The untracked files are all round-19 files.

**Each routed defect from §5** (spotcheck committed 2026-10-21 at `7243e7f1`):
1. `corpus/knowledge/guard-kill-closure.md:2` is not an input. No effect.
2. `corpus/knowledge/mutation-case-kumitate-sources-check.md:1` is not an input. No effect.
3. `corpus/lessons/round-18.md:79` is not an input. No effect.
4. `final/checks.json` **is** an input; it is hashed but never parsed. The repair is append-only: `round-19/bash-witness-selftest{,-complete}.{json,stdout,stderr}` were added, and the live `checks.json` is still `fed3c8e6…`.
   - Rewriting it in place would break the live pin of 17 L1 ledger entries that all pin `fed3c8e6…`. They start at sections 131, 921, 965, 1021, 1069, 1164, 1212, 1436, 1479, 1676, 1707, 1754, 1814, 1846, 1855, 1905 and 1925.
   - It would also contradict this spotcheck rule (2026-10-21): "Do not leave a failed invocation as the selftest row of the final receipt bundle." The right way to satisfy that is an appended correction, which is what was done.
5. **The unbacked `4b7c682` claim.** `ledger.json` and all 18 audit-1814 inputs are identical at `a85f710` and `4b7c682`. Landing a receipt at `4b7c682` would carry this entry over unchanged, and dropping the sentence does not touch it.

**`SKILL.md`.** C1 appends one registry row at HEAD line 1935 (`round-19/measure.py`). The whole-file sha256 changes from `1334c512…` to `4d0190fd…`. Lines 1814–1844 keep their content, their line numbers and section hash `dae48ab6…`.
- This is not an invalidation. A consumer keyed on the whole-file `skill_sha256` would see the entry as stale.
- The ledger already holds 142 of 159 entries with a different `skill_sha256`, and 68 entries with `carried_from`, so it evidently matches by section. [INFERENCE]

**Meaning, as opposed to bytes.** The defect-4 fix confirms that the bundle audit-1814 certified contained a failed invocation. That sharpens F1 but changes no byte or pin. No committed round-19 artifact cites audit-1814: the only matches are this seat's assignment text in `plan1.json`, `run1.json` and `spec1.json`. So C1 does not depend on it.

**Conclusion.** C1, as committed at `21e79329` and on the current working tree, does not invalidate this historical evidence.

## Residual risk and verification gaps

- **The delivered revision may land after this audit.** A failure-capable check that `.ufo/evidence/round-18/**` is byte-equal between `7243e7f1` and the delivered revision would close this. (Advisory.)
- **Section 1925 changes under C1** (outside this seat's section; flagged for the no-harm owner and Audit1925). At `a9c94c5c` the last section of `SKILL.md`, `### Round-18 gate/probe registry — routed-defect closure`, runs from line 1925 to 1934, the end of the file. C1's row extends it to line 1935.
  - The text from 1925 to the end of the file no longer hashes to its ledger value `884b3df3…`, although lines 1925–1934 still do.
  - If calibration 8 is measured as strict cold-read section coverage at the delivered revision, this section needs the lane monitor to account for it. [INFERENCE; the measuring rule is UNKNOWN here.]
- **Producer assertions I could not check.** `trace.rev`, `tracked_filter`, `untracked`, `live_lane_reads` and `dropped_home_count` are asserted by the producer, and no syscall log was retained, so they are UNKNOWN beyond consistency. The scratch directory `/tmp/tameshi-r18-L1-final-a2vitd82` still exists, but I did not inspect it: it is out of scope, and its current state is not the historical one.
- **Not established by these artifacts:** which revisions produced the receipts that the asserts cover, and how complete the set of commands was. `commands_executed_count: 1` counts traces, not processes.
- **`SKILL.md:974`.** I did not inspect the content of this hunk (`921ef807`→`a9c94c5c`), so its "D/N prose correction" label is UNKNOWN.
- **LSP** is not applicable: no source diff was under review.

## Investigation code (read-only; run in the Python eval kernel, condensed)

```python
import subprocess, hashlib, json, os, re, difflib
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
ENV={'PATH':'/usr/bin:/bin','HOME':'/tmp','GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_NOSYSTEM':'1','LC_ALL':'C'}
def gitrc(*a):
    r=subprocess.run(['git','--no-optional-locks','-C',L,*a],env=ENV,capture_output=True); return r.returncode,r.stdout.decode().strip()
def blob(rev,p):
    r=subprocess.run(['git','--no-optional-locks','-C',L,'cat-file','blob',f'{rev}:{p}'],env=ENV,capture_output=True); return r.stdout if r.returncode==0 else None
sha=lambda b: hashlib.sha256(b).hexdigest() if b is not None else None
T=json.load(open(f'{L}/.ufo/evidence/round-18/coldread/traces/L1/audit-1814.json')); spec=json.loads(T['argv'][-1])
OUT=open(f'{L}/.ufo/evidence/round-18/final/audit-1814.stdout','rb').read().decode().split('\n')
opens={m[1]:(m[2],int(m[3])) for m in (re.match(r'^OPEN (\S+) sha256=([0-9a-f]{64}) bytes=(\d+)$',x) for x in OUT) if m}
E=[e for e in json.load(open(f'{L}/.ufo/evidence/round-18/coldread/ledger.json'))['entries'] if '.ufo/evidence/round-18/coldread/traces/L1/audit-1814.json' in e.get('traces',[])][0]
for p,h in T['inputs'].items():   # pins vs OPEN, ledger, blobs at read/base/HEAD, live
    print(p, opens.get(p,(h,))[0]==h, E['inputs'].get(p,h)==h, [sha(blob(r,p))==h for r in ('a9c94c5c','7243e7f1','HEAD')], sha(open(f'{L}/{p}','rb').read())==h)
sl=blob('a9c94c5c','SKILL.md').decode().splitlines()
print(OUT[1:32]==sl[1813:1844], hashlib.sha256('\n'.join(sl[1813:1844]).encode()).hexdigest()==E['sha256'])
for a,b in [('a9c94c5c','7243e7f1'),('921ef807','a9c94c5c'),('5923d89','a9c94c5c')]: print(a,b,gitrc('merge-base','--is-ancestor',a,b)[0]==0)
print(gitrc('diff','--name-status','7243e7f1','HEAD')[1]); print(gitrc('log','--format=%h %s','7243e7f1..HEAD','--','.ufo/evidence/round-18','.ufo/waves/round-18')[1] or '<none>')
print(json.loads(blob('a9c94c5c','.ufo/evidence/round-18/final/checks.json'))['bash-witness-selftest'])
```

**Installs and updates:** none.
