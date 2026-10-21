# Audit921: round-19 w1 advisory audit of the round-18 `audit-921` receipt pair

Seat `TameshiR19-2.Audit921` (reviewer, read-only). Observed 2026-10-21. This audit is advisory only. It does not close or admit anything.

## Scope and method

- **Assigned files:** `.ufo/evidence/round-18/final/audit-921.stdout`, `.ufo/evidence/round-18/final/audit-921.stderr`, and `.ufo/evidence/round-18/coldread/traces/L1/audit-921.json`.
- **Ledger entry:** the only ledger entry that cites this trace is `.ufo/evidence/round-18/coldread/ledger.json:12001-12042`. I also read its `_meta` at `:12706-12878` and its seat source at `.ufo/waves/round-18/w3/L1Residual.md:66-113`.
- **Context:** `corpus/lessons/round-18-verifier-spotcheck.md:180-208` (§5).
- **Not done:**
  - I did not run the receipt argv or re-evaluate its asserts.
  - I did not read the contents of the other receipts, and I did not read `assemble.py`, the tracer, or round-19 `measure.py`.
  - I ran no tests, builds or lints, used no jj commands, and installed or updated no tools.
- **Git use (read-only):** `log`, `merge-base --is-ancestor`, `diff --name-status`, `diff -U0 -- SKILL.md`, `cat-file blob` and `for-each-ref`, all with `GIT_*` removed from the environment.
- **LSP:** not applicable, because no code symbols are under review. I searched for digests and paths with `grep`. That is a text search only, not semantic proof.

Labels: **O** = observation, **I** = inference, **U** = unknown.

## Established facts

### Stdout hash

| file | sha256 | bytes |
|---|---|---|
| `audit-921.stdout` | `60c300f1f88a8ca7ba4a12516197fb5c4a1ecd79c472dec1517c97435b7e0663` | 3491 |
| `audit-921.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 0 |
| `audit-921.json` | `ce080d0c7f719bb09a40e8c6b5885560ce00b2ff3709203fb7d8e7513a07c4b6` | 5543 |

- **O:** All three files were added only in `a134a09` (the only commit in `git log` for each). They are byte-identical at `4b7c682`, `7243e7f`, `78b99dd`, `21e7932`, `5774d8f` and in the worktree.
- **O:** No lane file records either digest. A grep for `60c300f1f88a8ca7|ce080d0c7f719bb0` across the lane (gitignore off) found nothing. The trace schema `tameshi-trace-inputs-v1` has no field for the stdout or stderr digest, and the ledger entry lists only the trace path.
- **Result:** no recorded expected stdout hash exists to check against. The digest above is established here for the first time. It is stable from the landing commit through the delivered revision.

### Trace argv ↔ stdout binding

- **O: the stdout matches the argv byte-for-byte.** The stdout is exactly these parts, in this order:
  - `SECTION 921 931`
  - `SKILL.md@a9c94c5` lines 921–931
  - 13 `OPEN` lines, in the same order as the spec's `paths`, with the head line and `TAIL` block after the one `corpus/knowledge/` path
  - the literal `VERIFIED …` line

  I checked this with my own comparison code against `git cat-file` blobs at `a9c94c5` (2610 bytes after the section block match exactly).
- **O: OPEN lines.** All 13 `OPEN` sha256 and byte values match `trace.inputs` and the `a9c94c5` blobs. All 14 `trace.inputs` entries (including `SKILL.md`) match the `a9c94c5` blobs.
- **O: exit status.** Trace `exit: 0`, the empty stderr and the final `VERIFIED` line are consistent with every assert having passed. I did not re-evaluate the asserts.
- **O: how trace and stdout are linked.** Only by the shared file-name stem `audit-921` and by matching content. No digest or timestamp links them.

### Ledger entry ↔ trace

- **O: fields agree.**
  - `read_rev` equals the trace `rev` (`a9c94c5…`).
  - `skill_sha256` `1334c512…` equals the trace's `SKILL.md` digest and `_meta.expect_skill_sha` (`ledger.json:12875`).
  - `inputs` equals `trace.inputs` minus `inputs_dropped: ["SKILL.md"]` (13 of 13).
  - The seat block's `inputs` (`L1Residual.md:94-108`) are equal.
  - The seat block's `opened` list equals the spec paths.
  - `commands_executed_count: 1` matches the one trace.
- **O: `end: 932` vs `end: 931` is not a coverage gap.** The ledger says `end: 932`; the spec says `end: 931`.
  - The ledger's section `sha256` `21a2ebc8ab8b…75ef0e` equals the sha256 of `"\n".join(lines 921–931)` of `SKILL.md@a9c94c5`.
  - Line 932 is blank. Line 933 (`### Using the ledger`) is its own bucket, 933–964 (for example `ledger.json:1125-1128`).
  - So the printed section bytes are the same bytes the ledger hashed.

### Revision and input facts

- **O: the revision comes from the tracer, not the program.** The trace's `rev: a9c94c5` (with `rev_reason: null`) is the tracer's own record. The program prints no revision and runs no git.
- **O: content does not pin `a9c94c5` uniquely.** All 14 input digests also match at `a134a09`, `a85f710`, `4b7c682`, `7243e7f` and `78b99dd`.
- **O: ancestry.** `a9c94c5` is an ancestor of `4b7c682` and of the frozen baseline `7243e7f`. The commit chain is: `a9c94c5` → `a134a09` (lands the trace, stdout/stderr and ledger) → `a85f710` → `4b7c682` → `7243e7f` → `78b99dd` → `21e7932` (`master`, `origin/master`).
- **O: `5774d8f`.** Jj keep ref `5774d8f` is a child of `21e7932` with an empty description. It changes only `LOG.md`, `SCORECARD.md` and `corpus/lessons/round-19.md`.
- **I: run window.** Between 18:46:21 and 18:47:13 −03:00 on 2026-10-20, going by the committer dates of `a9c94c5` and `a134a09`. Those dates are self-asserted.
- **U: interpreter.** Which `python3` ran is not recorded (`external: {}`). The host PATH starts with `~/.grok/bin`, `~/.kimi-code/bin` and mise shims.
- **U: clean clone.** Whether the clone was clean beyond the traced files is not established. The trace shows only `tracked_filter: true` and `untracked: {}`.

## Findings by severity

**Blocking or medium:** none. No finding blocks C1, and none shows a C1 repair invalidating audit-921.

### Minor

**M1. The `VERIFIED` line claims something the program never checks.**
- The stdout's last line ends with "ancestor runs have the same instrument blobs as the read revision" (`audit-921.stdout` final line, landed 2026-10-20 in `a134a09`).
- The program prints that literal unconditionally once the asserts pass. It runs under `env -i`, never calls git, and reads only files in the clone root. It reads no ancestor revision.
- The seat's minor-gap sentence "Real command execution receipts are ancestor-pinned (921ef807/5923d89)" (`L1Residual.md:74`, 2026-10-20) is also not established by the single recorded command.
- **My own check (not the receipt's):** `git diff --name-status` from `921ef807` to `a9c94c5` and from `5923d89` to `a9c94c5` shows:
  - no `tools/` path changes;
  - only added receipts and traces, plus edits to `SKILL.md` and `corpus/lessons/round-18.md`.

  So the claim holds for lane-tracked `tools/`. The revision each receipt actually ran at remains record-only.
- **Failing criterion:** receipt text states a fact its argv cannot observe.

**M2. One predicate checks presence, not value.**
- `assert 'controls_match' in …repeat.stdout` passes whatever the value is. A receipt containing `"controls_match": false` would also pass.
- I did not check the actual value, because `repeat.stdout` is outside my read scope.

**M3. Some inputs are hashed but never asserted, and the section's record claims are untested.**
- Four of the 13 opened inputs appear in no assert:
  - `final/checks.json`
  - `final/context.stdout`
  - `tools/mutate-and-run.sh`
  - `corpus/knowledge/fleet-kill-rate-ledger.md` (only its head line and last 700 characters are printed)
- `checks.json` is the file behind routed defect 4 (spot-check §5 item 4). Audit-921 printed `VERIFIED` with it as an input but never read its rows. So audit-921 neither caught nor contradicts defect 4, and it must not be cited as having checked it.
- The section's specific record claims are not tested by any predicate:
  - "eight since round 18" and "eight rows since its round-18 block"
  - `:597-620`
  - `@9f1d3c3:72-109`
  - `:511-522`
- The ledger's `wrong_expectations: 0` and `gap-minor` verdict for this `record` section therefore rest on the seat's reading, not on this trace (`commands_executed_count: 1`).
- This is outside C1's five items. It is a residual calibration risk, and this report makes no claim to widen C1 to cover it.

### Info

- **I1.** The receipt files are not content-addressed by any record (see the stdout hash section). Their integrity rests on git history, and they are stable.
- **I2.** `env_overrides` describes the tracer's own environment. Because the argv runs `env -i`, `PYTHONPYCACHEPREFIX` never reaches `python3`. The argv sets `PYTHONDONTWRITEBYTECODE=1` itself. This is not a defect.

## Could C1 repairs invalidate this historical evidence?

**No, not as a historical record.** One indirect pin drifts at the delivered tip; details below.

**O: nothing was rewritten.** The stdout, stderr, trace and `ledger.json` are byte-identical at `7243e7f`, `78b99dd`, `21e7932`, `5774d8f` and in the worktree. The 13 inputs other than `SKILL.md` are byte-identical at all of those and in the worktree.

**O: the five routed-defect surfaces, against audit-921's inputs** (from `git diff --name-status 7243e7f 21e7932`):

1. `corpus/knowledge/guard-kill-closure.md` was modified. It is not an input.
2. `corpus/knowledge/mutation-case-kumitate-sources-check.md` was modified. It is not an input; it is only named inside the printed ledger tail.
3. `corpus/lessons/round-18.md` was modified. It is not an input.
4. `final/checks.json` **is** an input, and it was not changed: still `fed3c8e6…` at `21e7932`, `5774d8f` and in the worktree. The repair added `.ufo/evidence/round-19/bash-witness-selftest{,-complete}.{json,stdout,stderr}` instead, so the binding holds. Rewriting `checks.json` in place would have broken this input binding at the tip. That did not happen.
5. `.ufo/evidence/round-19/round18-final-measure.{json,stdout,stderr}` was added. At `4b7c682`, all 14 inputs, including `SKILL.md`, match `a9c94c5`, and `SKILL.md`'s hash is the ledger's `expect_skill_sha`. So audit-921's entry can be bound at the cited revision. **Gap:** I did not read whether that measure actually counted this entry.

**O: what changed in `SKILL.md` at `21e7932`.**
- It is a pure append. The old 143694-byte file is a byte-for-byte prefix of the new 144592-byte file.
- The diff is one hunk, `@@ -1934,0 +1935 @@`: a table row that registers `.ufo/evidence/round-19/measure.py`.
- Lines 921–931 still hash to `21a2ebc8…` at `21e7932` and `5774d8f`, and their line numbers are unchanged.
- The whole-file hash changes from `1334c512…` to `4d0190fd672c…`. So `_meta.expect_skill_sha` in the round-18 ledger no longer matches `SKILL.md` at the delivered tip.

**I: what this means.**
- The ledger declares `"carry_coverage_basis": "section_sha256"` (`ledger.json:12874`). Under that basis this entry would carry forward. I did not read the assembler logic.
- The evidence stays fully bound at `a9c94c5`, `4b7c682` and `7243e7f`.
- At `21e7932`, any "60/60" figure taken from this ledger needs the ledger re-assembled against the new `SKILL.md` hash. C1 claims no new cold-read coverage, so C1 is not harmed as long as nobody cites round-18 coverage at `21e7932`.

**Conditions that would invalidate it in future:**
- any edit at or before `SKILL.md:931`;
- any in-place edit of the 13 inputs, especially `checks.json`;
- any in-place edit of the receipt files themselves.

The contract requires corrections to be appended as dated, named errata.

## Residual risk and verification gaps

- **Not read:**
  - the value of `controls_match` in `repeat.stdout`;
  - the rows of `checks.json`;
  - `assemble.py`, the tracer and round-19 `measure.py` source;
  - the `round18-final-measure` receipt.
- **Point-in-time worktree check:** the worktree hashes are a snapshot from 2026-10-21. L1 may still be writing.
- **Resume continuity:** `resume_continuity_v1` does not apply, because this receipt has no resume path.

## Investigation code

Read-only `python3`, run in the session kernel. These are condensed restatements of the cells I ran. The original cells printed booleans, and each check shown here printed True or an empty mismatch list. Some section-hash canonicalizations I tried and rejected (for example the `keepends` variants and 921–932 joins) printed False; only `"\n".join(lines 921–931)` reproduced the ledger hash.

```python
import hashlib, json, os, subprocess, re
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
GENV={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
def git(*a, binary=False, ok=False):
    r=subprocess.run(['git','-C',L,*a],capture_output=True,env=GENV)
    if r.returncode:
        if ok: return None
        raise RuntimeError(r.stderr.decode())
    return r.stdout if binary else r.stdout.decode()
def blob(rev,path): return git('cat-file','blob',f'{rev}:{path}',binary=True,ok=True)
sha=lambda b: hashlib.sha256(b).hexdigest()
REV='a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4'
P_TR='.ufo/evidence/round-18/coldread/traces/L1/audit-921.json'
so=open(f'{L}/.ufo/evidence/round-18/final/audit-921.stdout','rb').read(); txt=so.decode()
tr=json.loads(open(f'{L}/{P_TR}','rb').read()); spec=json.loads(tr['argv'][-1])
opens=[(m.group(1),m.group(2),int(m.group(3))) for m in re.finditer(r'^OPEN (\S+) sha256=([0-9a-f]{64}) bytes=(\d+)$',txt,re.M)]
print([o[0] for o in opens]==spec['paths'])                                   # True
print([p for p,h,n in opens if not (h==tr['inputs'].get(p)==sha(blob(REV,p)) and n==len(blob(REV,p)))])  # []
print([p for p,h in tr['inputs'].items() if sha(blob(REV,p))!=h])             # []
skl=blob(REV,'SKILL.md').decode().splitlines()
sec='SECTION 921 931\n'+'\n'.join(skl[920:931])+'\n'
print(txt.startswith(sec), sha('\n'.join(skl[920:931]).encode()))             # True 21a2ebc8…
led=blob(REV,'corpus/knowledge/fleet-kill-rate-ledger.md').decode()
blk=led.splitlines()[0]+'\nTAIL '+led[-700:]+'\n'
exp=''.join(f'OPEN {p} sha256={h} bytes={n}\n'+(blk if p.startswith('corpus/knowledge/') else '') for p,h,n in opens)
exp+='VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision\n'
print(txt[len(sec):]==exp)                                                    # True
# Drift: every input and the receipt triple at a134a09,a85f710,4b7c682,7243e7f,78b99dd,21e7932,5774d8f and the worktree,
# compared with tr['inputs'] and the a134a09 blobs. Only SKILL.md differs, at 21e7932, 5774d8f and the worktree (4d0190fd…).
# Section re-anchor: heading index, cut at the next '#' line, trailing blanks stripped -> (921, 931, 21a2ebc8…) at every revision.
ledg=json.load(open(f'{L}/.ufo/evidence/round-18/coldread/ledger.json'))
e=[x for x in ledg['entries'] if P_TR in x.get('traces',[])][0]
print(e['inputs']=={k:v for k,v in tr['inputs'].items() if k not in e['inputs_dropped']},
      e['read_rev']==tr['rev'], ledg['_meta']['expect_skill_sha']==e['skill_sha256']==tr['inputs']['SKILL.md'])  # True True True
d=git('diff','-U0','7243e7f163f08978c8fd9b6c1ef67a2fefe7d190','21e79329f8bdcf01a62be63b3e46db4a7de6b6f9','--','SKILL.md')
print([l for l in d.splitlines() if l.startswith('@@')])                      # ['@@ -1934,0 +1935 @@ …']
new=blob('21e79329f8bdcf01a62be63b3e46db4a7de6b6f9','SKILL.md'); print(new.startswith(blob(REV,'SKILL.md')))  # True
```
