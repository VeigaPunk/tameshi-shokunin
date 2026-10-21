# Audit1846: round-18 `audit-1846` receipt-pair audit (tameshi round 19, w1)

- Seat: `TameshiR19-2.Audit1846` (reviewer, read-only). Date: 2026-10-21. These findings are advisory. They do not close or admit anything.
- Serves: C1's no-harm and verification boundary. The question is whether this historical receipt stays intact under the five routed round-18 corrections. This report does not expand the claim.
- Lane `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Read revision `REV=a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`.
  Frozen baseline `BASE=7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`. Delivered lane revision
  `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` (= `refs/heads/master` = `refs/remotes/origin/master`).

## Scope and envelope

Assigned evidence, all read-only:
- `.ufo/evidence/round-18/final/audit-1846.stdout`
- `.ufo/evidence/round-18/final/audit-1846.stderr`
- `.ufo/evidence/round-18/coldread/traces/L1/audit-1846.json` (the trace)
- The ledger entry `(skill_sha256=1334c512…, start=1846)` at `.ufo/evidence/round-18/coldread/ledger.json:12478-12522`, plus its cited report section `.ufo/waves/round-18/w3/L1Residual.md:624-677`.

To check the trace's revision and input facts, I also read:
- the pinned Git blobs of the 17 traced inputs;
- the trace's scratch clone `/tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin`, which still exists. I read only its HEAD, reflog and file digests.

Envelope:
- I did not execute the receipt argv.
- I did not run any lane tool, selftest, build, lint or formatter.
- I made no Git or JJ writes. Every git call was read-only (`cat-file`, `rev-parse`, `merge-base`, `diff-tree`, `diff`/`log`/`grep` on commits), with `GIT_*` stripped and `GIT_OPTIONAL_LOCKS=0`.
- I installed nothing.
- LSP does not apply: no code diff was assigned. Checks are Git- and byte-level.

## Verdict

**No actionable finding blocks C1.** The receipt pair, trace and ledger entry are intact and bound to `REV`. The delivered round-19 revision does not invalidate them: all 16 bound non-page inputs are still byte-identical, and the 1846 section hash is unchanged.

Two **low** receipt-hygiene observations predate round 19 and are outside the five routed defects (L1, L2 below). Record them as residual risk, not as a C1 expansion.

## Facts established (observed)

| # | Check | Command / source | Observed | Result |
|---|---|---|---|---|
| 1 | stdout/stderr identity | `sha256sum`; `git rev-parse a134a09:<p>`; `git hash-object --no-filters <p>` | stdout `97e7357a1cefddf552aea61d097de4b7b0eb862ac430cea0f8a03cf1a0349ecf`, 3264 B, 26 lines. stderr `e3b0c442…7852b855`, 0 B. Blobs `fdd5ace0…`/`e69de29b…`/`312e7a32…` (stdout/stderr/trace) were added in `a134a09` and equal the worktree. They are identical at `BASE` and `21e7932`. | PASS (bound by Git only) |
| 2 | stdout digest recorded in band | trace keys; ledger entry; grep for `97e7357a` over the lane worktree (incl. `.ufo/waves/round-19`) and the fleet `.ufo/reports`; `git grep` at `a134a09`, `a85f710`, `4b7c682`, `BASE`, `21e7932` | The trace has no stdout or stderr digest field, only `"exit": 0`. No file records the digest at any of those revisions. | NOT RECORDED → L1 |
| 3 | argv ↔ stdout binding | Static re-derivation of what `python3 -c PROGRAM SPEC` prints over `REV` blobs. The asserts were **not** re-evaluated. | Expected bytes equal stdout bytes exactly: `SECTION 1846 1853`, 8 page lines, 16 `OPEN` rows in spec order, the `VERIFIED` literal. `--chdir` = `cwd` = `root`. Nothing follows the spec in argv. Program sha256 `aeda7ed1…ff643`. | PASS |
| 4 | Trace revision | trace `rev`; ledger `read_rev`; scratch clone `git rev-parse HEAD`, `.git/logs/HEAD` | Both name `REV`. The clone's HEAD is still `REV`. Reflog: clone@`921ef80` 18:29:34 → `5923d89` 18:41:04 → `a9c94c5` 18:46:59 (-03:00). That is 1.3 s before the outputs' mtime of 18:47:00.70. `registry-branch-aligned.stdout` first exists at `REV` (`REV^`=`5923d89` lacks it). The outputs were added in `REV`'s child `a134a09` at 18:47:13. | PASS |
| 5 | Input digests | sha256 of `git cat-file blob REV:<p>` for all 17 trace inputs; sha256 of the clone's files | 17/17 equal `REV`, and also the clone, `a134a09`, `4b7c682` and `BASE`. The 16 `OPEN` rows equal the trace digests. At `21e7932` and in the worktree 16/17 equal; `SKILL.md` differs (see C1 section). | PASS |
| 6 | Ledger entry ↔ trace | ledger 12478-12522; sectionizer rule at `assemble.py:159-213` re-implemented in /tmp | `skill_sha256` = sha256(`SKILL.md@REV`). `start` 1846, `end` 1854, heading and `sha256 ad2320cb…` match the sectionization at `REV`. `inputs` = trace inputs minus `SKILL.md` (`DROPPED_INPUT_KEYS`, `assemble.py:130-134`); `inputs_dropped` is `["SKILL.md"]`; `external_inputs` is `{}`. There is exactly one entry for (1334c512, 1846). The entry is identical at `a134a09`, `a85f710`, `BASE`, `21e7932` and in the worktree. L1Residual's declared inputs match. | PASS |
| 7 | Section range | `SKILL.md@REV` lines 1846-1855 | The receipt printed 1846-1853. Ledger `end` 1854 is a blank line, which the assembler strips before hashing. Line 1855 is the next heading. | PASS (difference is benign) |
| 8 | What the 8 asserts matched (read only) | matching lines in the `REV` blobs | probes `DEFECT_PROBES: open=0 closed=11 total=11`; regression `REGRESSION: PASS (cases=8 passed=8; …)`; historical `(cases=4 passed=4; …)`; case7 and case8 `killed=5 survived=5 inconclusive=0 kill-rate=50%`; repeat `REPEAT_CONTROL: controls_match`; registry-branch-aligned held=31 total=31 superseded=4 exit=0 rev=`5923d89`; disposition `clean`; before `failed` | Consistent with exit 0 and the `VERIFIED` line |

## Findings by severity

### High / Medium

None.

### Low

**L1: stdout and stderr have no digest binding in the trace or the ledger.**
- Observation: the trace's keys are `argv cwd dropped_home_count env_overrides exit external inputs live_lane_reads rev rev_reason root schema tracked_filter untracked`. None of them is a stdout or stderr digest, and the ledger entry has none either.
- `assemble.py` `load_trace_receipt` (lines 439-497) checks only schema, `rev == read_rev`, `live_lane_reads` and the digest maps. A search for exit handling (`["exit"]`, `.get("exit")`, `'exit'`) finds nothing. So credit never looks at the trace's `exit` or at the stdout.
- Failing criterion: "the stdout hash can be checked against an in-band record." No such record exists. The only bindings are Git object identity (blob `fdd5ace0…` in `a134a09`) and the re-derivation in row 3.
- Contrast: the `final/checks.json` rows and round 19's `round18-final-measure.json` both carry `stdout_sha256`, `exit` and `revision`.
- Impact: none on C1 or on this entry's verdict. A replaced or deleted stdout would not change ledger credit. This matches the documented design at `SKILL.md:1934`, present at `REV` (2026-10-20) and at `21e7932` (2026-10-21): "input-keyed credit only: it binds credit to recorded inputs, not to the commands a bucket requires".

**L2: the `VERIFIED` line is a printed constant, and its second clause is never computed.**
- `audit-1846.stdout:26` (2026-10-20 18:47 -03:00) reads: "VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision".
- The program has 8 asserts. They are substring or field checks over 8 receipt files. It makes no revision or blob comparison: there is no git call and no revision token.
- `context.stdout` and `checks.json` are only hashed, never asserted. `checks.json@REV` records `registry` exit 1 at `921ef80` (the `REV` commit subject discloses "stale scratch-branch failure retained", 2026-10-20T18:46:21-03:00). It also records `bash-witness-selftest` exit 64, which is routed defect 4. The `VERIFIED` line covers both without inspecting them.
- Independent check (the receipt does not establish this):
  - Ten instrument blobs are identical at `921ef80`, `5923d89` and `REV`: `tools/{evidence-disposition.py, registry-check.py, mutate-and-run.sh, pin-disposition.py, registry.json, bash-witness-study.py, trace-inputs.py}` and `.ufo/evidence/round-18/{defect-probes.py, measure.py, coldread/assemble.py}`.
  - `diff-tree 921ef80 REV` touches 53 paths. The only non-`.ufo` paths are `SKILL.md` and `corpus/lessons/round-18.md`, and no `.ufo` code file changes.
  - `5923d89..REV` adds 6 receipt files.
  - The clone's reflog shows HEAD only ever at those three commits.
- What that means:
  - Observed: the clause is true for those revisions.
  - [INFERENCE] every retained receipt was produced in that clone.
  - Unknown: run revisions for regression, case7, case8, historical, context and repeat. None of them carries an in-band revision.
- This is already disclosed:
  - `L1Residual.md:632` (2026-10-20, `a134a09`) says "L1 residual verification is not a blind non-author cold read." and "Historical per-run timestamps and deleted scratch logs remain record-only."
  - The ledger records `commands_executed_count: 1` and verdict `gap-minor`.
  
  The ledger does not overclaim. Only the stdout literal does.

### Info

- **I1: section 1846's command completeness is neither established nor claimed.**
  - The section lists `--selftest` for all four tools, `mutate-and-run.sh --regression`, a `pin-disposition.py` run, and "the round-17 manifest now exits 2".
  - The receipt asserts nothing about `mutate-and-run --selftest`, any pin-disposition run or selftest, or the round-17 exit 2.
  - The evidence-disposition and registry-check selftests appear only in `checks.json`, which the program does not parse.
  - The ledger's count of 1 is this audit alone. I did not extrapolate further.
- **I2: `env_overrides` describes the wrapper, not the measured process.** The wrapper removed `GIT_CONFIG_*` and set `PYTHONPYCACHEPREFIX`. Inside, `env -i` sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` again and drops `PYTHONPYCACHEPREFIX`. This is harmless because the argv describes the inner environment itself, but the field is not the effective environment.
- **I3 (positive):** the revision binding is unusually strong because the scratch clone was kept. HEAD, the reflog timing and the file digests all agree with the trace.

## Could C1 repairs invalidate this historical evidence?

What I observed at the delivered revision `21e7932`; the worktree equals it on every bound path:
- **Bound inputs:** all 16 bound non-page inputs are byte-identical to `REV`. The receipt triple, the ledger entry and the L1Residual report are unchanged.
- **Defect 4** (mis-invoked bash-witness selftest row in `final/checks.json`): the repair appended `.ufo/evidence/round-19/bash-witness-selftest{,-complete}.{json,stdout,stderr}`. `final/checks.json` is still `fed3c8e6…`, so this receipt's `OPEN` row and the ledger input remain true. The spot-check's instruction (`corpus/lessons/round-18-verifier-spotcheck.md:199-200`, `7243e7f`, 2026-10-21) was "Do not leave a failed invocation as the selftest row of the final receipt bundle." The repair met it by appending, not by rewriting.
- **Defect 5** (the unbacked claim at `4b7c682`): the repair appended `.ufo/evidence/round-19/round18-final-measure.{json,stdout,stderr}` at revision `4b7c682`.
  - Its cold-read list credits this bucket with no drift: `start: 1846`, `reasons: ["credited"]` (`round18-final-measure.stdout:1864-1874`).
  - All 17 trace inputs are equal at `4b7c682`.
  - So C1's defect-5 receipt **depends on** this evidence and agrees with it.
- **Defects 1-3** edit `corpus/knowledge/guard-kill-closure.md`, `corpus/knowledge/mutation-case-kumitate-sources-check.md` and `corpus/lessons/round-18.md`. This receipt binds none of them.
- **`SKILL.md`:** round 19 inserted one line after 1934 (the round-19 `measure.py` registry row). Section 1846 is still at 1846-1854 with the same section sha `ad2320cb…`. The page sha changed from `1334c512…` to `4d0190fd…`.

**Conclusion: the repairs do not invalidate this evidence.**
- The historical facts are pinned to `REV` blobs, so later edits cannot change them.
- The current tree also still matches every bound input.

Four kinds of repair would break that match; none occurred:
- (a) Rewriting `final/checks.json` in place, or any other bound `final/*.stdout`: the `OPEN` rows and ledger input digests would stop matching the live tree. Input-keyed credit would then drift at any revision containing the rewrite.
- (b) Editing `SKILL.md` lines 1846-1854: the section sha would change.
- (c) Rewriting or deleting the receipt triple, the ledger or `L1Residual.md`.
- (d) Fixing the `VERIFIED` literal in place instead of appending a dated, named erratum.

## Residual risk and verification gaps

- **Ledger key vs delivered page.** The ledger key (`skill_sha256 1334c512…`, start 1846) does not name the delivered page (`4d0190fd…`). Calibration measured at `21e7932` must therefore use the section-sha carry basis, which still matches, or fresh reads. C1 claims no new coverage, so no claim depends on this.
- **Asserts not re-evaluated.** I infer that they passed from four things: `exit 0`, empty stderr, the `VERIFIED` line being present, and the byte-exact re-derivation.
- **Capture completeness not audited.** I did not check how completely `tools/trace-inputs.py` captures reads. By inspection, the 17 recorded inputs equal the program's reads (page plus 16 paths).
- **Provenance of the 8 opened receipts.** Only `checks.json` and `registry-branch-aligned` record argv, exit or revision. For the rest, provenance is unknown here and outside my scope.
- **L1 and L2** are pre-existing hygiene issues. They are not among the five routed defects and are left open; this report claims no fix.

## Commands run (read-only)

```sh
sha256sum audit-1846.stdout audit-1846.stderr ../coldread/traces/L1/audit-1846.json ../coldread/ledger.json   # cwd .ufo/evidence/round-18/final
GIT_OPTIONAL_LOCKS=0 git -C "$L" log --format='%H %an <%ae> %cI %s' -- <receipt triple + ledger>
GIT_OPTIONAL_LOCKS=0 git -C "$L" cat-file blob a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4:.ufo/evidence/round-18/final/checks.json
GIT_OPTIONAL_LOCKS=0 git -C "$L" rev-parse a134a09^ a85f710^
GIT_OPTIONAL_LOCKS=0 git -C "$L" log --format='%h %cI %an %s' 7243e7f..refs/heads/master
GIT_OPTIONAL_LOCKS=0 git -C "$L" for-each-ref --format='%(refname) %(objectname:short)'
GIT_OPTIONAL_LOCKS=0 git -C "$L" grep -l -e 97e7357a -e audit-1846.stdout <rev> -- .   # rev in a134a09 a85f710 4b7c682 7243e7f refs/heads/master
GIT_OPTIONAL_LOCKS=0 git -C "$L" rev-parse a134a09:<p>; git hash-object --no-filters "$L/<p>"   # receipt triple
GIT_OPTIONAL_LOCKS=0 git -C "$L" diff-tree -r --name-status --no-renames 5923d89 a9c94c5; ... a9c94c5^ a9c94c5
GIT_OPTIONAL_LOCKS=0 git -C "$L" show -s --format='%H %cI %s' a9c94c5^ 4acc607df
GIT_OPTIONAL_LOCKS=0 git -C "$L" diff --unified=1 7243e7f refs/heads/master -- SKILL.md
GIT_OPTIONAL_LOCKS=0 git -C /tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin rev-parse HEAD; git ... log -1; cat .git/logs/HEAD
date -d @1792531774 -Iseconds; date -d @1792532464 -Iseconds; date -d @1792532819 -Iseconds
python3 /tmp/audit1846/verify.py      # sha256 f2d8654285e79cdd0a636f808631a0d394c75f7d296c81d45ac92b6465e2daf8
python3 /tmp/audit1846/c1impact.py    # sha256 e01362a541a42284af35bf48fe7d159576cc7cf31616b2ec3234781e07356906
```

Results: every observation above, including all `PASS` rows. `verify.py` printed `stdout == static re-derivation over REV blobs: True`. `c1impact.py` printed `sec-sha-match=[True]` for `REV`, `BASE`, `78b99dd`, `21e7932` and the worktree.

Inline check (clone and `4b7c682` digests). Output: `clone files == trace inputs: True []`, `4b7c682 blobs == trace inputs: True []`.

```python
import hashlib, json, subprocess, os
C="/tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin"; L="/home/vgpnk/Projects/shokunin/tameshi-shokunin"
tr=json.load(open(L+"/.ufo/evidence/round-18/coldread/traces/L1/audit-1846.json"))
env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}; env["GIT_OPTIONAL_LOCKS"]="0"
ok_clone=[]; ok_4b=[]
for p,d in sorted(tr["inputs"].items()):
    f=os.path.join(C,p); ok_clone.append((p, os.path.isfile(f) and hashlib.sha256(open(f,"rb").read()).hexdigest()==d))
    b=subprocess.run(["git","-C",L,"cat-file","blob","4b7c6823a462f5ea2eafcb262275300a545f3ed7:"+p],capture_output=True,env=env).stdout
    ok_4b.append((p, hashlib.sha256(b).hexdigest()==d))
print("clone files == trace inputs:", all(v for _,v in ok_clone), [p for p,v in ok_clone if not v])
print("4b7c682 blobs == trace inputs:", all(v for _,v in ok_4b), [p for p,v in ok_4b if not v])
```

## Scratch code (verbatim)

`/tmp/audit1846/verify.py` (sha256 `f2d86542…e2daf8`):

```python
#!/usr/bin/env python3
"""Audit1846 (tameshi round-19 w1) read-only verifier.

Never executes the receipt argv. Reads the receipt pair, its trace, the
ledger entry, and pinned Git blobs (cat-file / rev-parse / merge-base /
diff-tree only; GIT_* removed, GIT_OPTIONAL_LOCKS=0).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4"
BASE = "7243e7f163f08978c8fd9b6c1ef67a2fefe7d190"
P_OUT = ".ufo/evidence/round-18/final/audit-1846.stdout"
P_ERR = ".ufo/evidence/round-18/final/audit-1846.stderr"
P_TR = ".ufo/evidence/round-18/coldread/traces/L1/audit-1846.json"
P_LED = ".ufo/evidence/round-18/coldread/ledger.json"
P_REP = ".ufo/waves/round-18/w3/L1Residual.md"

ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV["GIT_OPTIONAL_LOCKS"] = "0"


def git(*a, check=True):
    r = subprocess.run(["git", "-C", L, *a], capture_output=True, env=ENV)
    if check and r.returncode:
        sys.exit("git %s -> %d: %s" % (a, r.returncode, r.stderr.decode()))
    return r


def blob(rev, path):
    r = git("cat-file", "blob", "%s:%s" % (rev, path), check=False)
    return r.stdout if r.returncode == 0 else None


def sha(b):
    return None if b is None else hashlib.sha256(b).hexdigest()


def full(rev):
    return git("rev-parse", "--verify", rev + "^{commit}").stdout.decode().strip()


def anc(a, b):
    return git("merge-base", "--is-ancestor", a, b, check=False).returncode == 0


def wt(path):
    p = os.path.join(L, path)
    return open(p, "rb").read() if os.path.isfile(p) else None


def hdr(t):
    print("\n## " + t)


out, err = wt(P_OUT), wt(P_ERR)
tr = json.loads(wt(P_TR))
led = json.loads(wt(P_LED))

hdr("1 receipt identity")
print("stdout sha256=%s bytes=%d lines=%d" % (sha(out), len(out), out.count(b"\n")))
print("stderr sha256=%s bytes=%d" % (sha(err), len(err)))
print("trace keys:", sorted(tr))
print("trace has stdout/stderr digest field:",
      [k for k in tr if "stdout" in k or "stderr" in k or "output" in k])
print("trace schema=%s rev=%s rev_reason=%s exit=%s tracked_filter=%s"
      % (tr["schema"], tr["rev"], tr["rev_reason"], tr["exit"], tr["tracked_filter"]))
print("trace untracked=%s external=%s live_lane_reads=%s dropped_home=%s"
      % (tr["untracked"], tr["external"], tr["live_lane_reads"], tr["dropped_home_count"]))
print("trace env_overrides:", json.dumps(tr["env_overrides"], sort_keys=True))

hdr("2 argv binding (static re-derivation; asserts NOT re-evaluated)")
argv = tr["argv"]
i = argv.index("python3")
assert argv[i + 1] == "-c", argv[i + 1]
prog, spec_s = argv[i + 2], argv[i + 3]
print("argv len=%d python3 at %d; trailing argv after spec: %r" % (len(argv), i, argv[i + 4:]))
print("argv --chdir == trace cwd == trace root:",
      argv[argv.index("--chdir") + 1] == tr["cwd"] == tr["root"])
envi = argv.index("env")
print("env -i inner vars:", argv[envi + 1:i])
print("program sha256:", sha(prog.encode()))
spec = json.loads(spec_s)
start, end, paths = spec["start"], spec["end"], spec["paths"]
print("spec start=%d end=%d paths=%d" % (start, end, len(paths)))
skill = blob(REV, "SKILL.md")
print("SKILL.md@REV sha256=%s (trace input %s)" % (sha(skill), tr["inputs"].get("SKILL.md")))
lines = skill.decode().splitlines()
VER = ("VERIFIED actual execution receipts; ancestor runs have the same "
       "instrument blobs as the read revision")
assert ("print('%s')" % VER) in prog
exp = ["SECTION %d %d" % (start, end)] + lines[start - 1:end]
for p in paths:
    b = blob(REV, p)
    exp.append("OPEN %s sha256=%s bytes=%d" % (p, sha(b), len(b)))
    assert not p.startswith("corpus/knowledge/")
exp.append(VER)
exp_b = ("\n".join(exp) + "\n").encode()
print("stdout == static re-derivation over REV blobs:", exp_b == out)
if exp_b != out:
    for n, (a, b) in enumerate(zip(exp_b.decode().split("\n"), out.decode().split("\n")), 1):
        if a != b:
            print(" first diff line %d\n  exp %r\n  got %r" % (n, a, b))
            break
print("asserts present in program (count):", prog.count("assert "))
print("does program compare instrument blobs across revisions? (git/rev tokens):",
      [t for t in ("git", "rev", "921ef80", "5923d89", "ancestor") if t in prog.replace(VER, "")])

hdr("3 trace inputs vs REV blobs / baseline / working tree")
tips = {"REV": REV, "a134a09": full("a134a09"), "BASE": BASE, "master": full("refs/heads/master")}
print("tips:", json.dumps(tips))
for p, d in sorted(tr["inputs"].items()):
    row = {k: (sha(blob(v, p)) == d) for k, v in tips.items()}
    row["worktree"] = sha(wt(p)) == d
    print("%-62s %s" % (p, " ".join("%s=%s" % (k, "ok" if v else "DIFF") for k, v in row.items())))
opened = re.findall(r"^OPEN (\S+) sha256=([0-9a-f]{64}) bytes=(\d+)$", out.decode(), re.M)
print("stdout OPEN rows=%d all equal trace inputs: %s"
      % (len(opened), all(tr["inputs"].get(p) == h for p, h, _ in opened)))
print("trace inputs not OPENed in stdout:", sorted(set(tr["inputs"]) - {p for p, _, _ in opened}))

hdr("4 ledger entry binding")
ents = [e for e in led["entries"] if P_TR in (e.get("traces") or [])]
print("ledger entries citing trace:", len(ents))
e = ents[0]
nxt = [x for x in led["entries"] if x["skill_sha256"] == e["skill_sha256"] and x["start"] > e["start"]]
print("entry:", json.dumps({k: e[k] for k in ("skill_sha256", "start", "end", "heading", "sha256",
      "class", "verdict", "blocking_gaps", "wrong_expectations", "minor_gaps",
      "commands_executed_count", "read_rev", "seats", "inputs_dropped")}, ensure_ascii=True))
print("skill_sha256 == sha(SKILL.md@REV):", e["skill_sha256"] == sha(skill))
print("read_rev == trace rev == REV:", e["read_rev"] == tr["rev"] == REV)
body = lines[e["start"] - 1:e["end"]]
print("line %d=%r line %d(end)=%r line %d=%r" % (e["start"], lines[e["start"] - 1], e["end"],
      lines[e["end"] - 1], e["end"] + 1, lines[e["end"]]))
print("headings inside start+1..end:", [n for n in range(e["start"] + 1, e["end"] + 1) if lines[n - 1].startswith("#")])
while body and not body[-1].strip():
    body.pop()
print("section sha (assemble rule) == ledger sha:", sha("\n".join(body).encode()) == e["sha256"])
print("non-blank section lines %d..%d; receipt printed %d..%d -> covers all non-blank: %s"
      % (e["start"], e["start"] + len(body) - 1, start, end, e["start"] + len(body) - 1 <= end))
want = {k: v for k, v in tr["inputs"].items() if k != "SKILL.md"}
print("ledger inputs == trace inputs minus SKILL.md:", e["inputs"] == want)
print("ledger external_inputs empty:", e["external_inputs"] == {})
print("next entry start:", min(x["start"] for x in nxt) if nxt else None)
others = [x for x in led["entries"] if x["skill_sha256"] == e["skill_sha256"] and x["start"] == e["start"] and x is not e]
print("other entries same (skill,start):", len(others))
for rev_name in ("a134a09", "a85f710", "BASE", "master"):
    r = tips.get(rev_name) or full(rev_name)
    b = blob(r, P_LED)
    le = [x for x in json.loads(b)["entries"] if P_TR in (x.get("traces") or [])] if b else None
    print("ledger entry at %s identical to worktree: %s" % (rev_name, le == [e]))
rep = wt(P_REP).decode()
print("L1Residual report sha256:", sha(rep.encode()))

hdr("5 commit placement and history")
add = git("log", "--format=%H %cI", "--diff-filter=A", "--", P_OUT).stdout.decode().split()
print("added in:", add)
print("REV ancestor of add commit:", anc(REV, add[0]), "; add ancestor of BASE:", anc(add[0], BASE),
      "; BASE ancestor of master:", anc(BASE, tips["master"]))
for p in (P_OUT, P_ERR, P_TR):
    print("%-60s" % p, " ".join("%s=%s" % (k, sha(blob(v, p)) == sha(wt(p))) for k, v in tips.items() if k != "REV"),
          "REV-has=%s" % (blob(REV, p) is not None))
print("REV commit time:", git("show", "-s", "--format=%cI %s", REV).stdout.decode().strip())

hdr("6 instrument identity across run revisions (independent; NOT established by receipt)")
inst = ["tools/evidence-disposition.py", "tools/registry-check.py", "tools/mutate-and-run.sh",
        "tools/pin-disposition.py", "tools/registry.json", ".ufo/evidence/round-18/defect-probes.py",
        "tools/bash-witness-study.py", "tools/trace-inputs.py", ".ufo/evidence/round-18/measure.py",
        ".ufo/evidence/round-18/coldread/assemble.py"]
runrevs = {"921ef80": full("921ef80"), "5923d89": full("5923d89"), "REV": REV}
for p in inst:
    ids = {k: sha(blob(v, p)) for k, v in runrevs.items()}
    print("%-46s same@921ef80/5923d89/REV=%s  REV=%s" % (p, len(set(ids.values())) == 1, (ids["REV"] or "absent")[:12]))
for a in ("921ef80", "5923d89"):
    ns = git("diff-tree", "-r", "--name-status", "--no-renames", runrevs[a], REV).stdout.decode().splitlines()
    print("diff %s..REV: %d paths; non-.ufo paths: %s" % (a, len(ns), [x for x in ns if ".ufo/" not in x]))
    print("   .ufo code-like paths:", [x for x in ns if ".ufo/" in x and re.search(r"\.(py|sh|mjs|js)$", x)])

hdr("7 run revisions named inside the opened receipts (REV blobs)")
for p in paths:
    if not p.startswith(".ufo/"):
        continue
    t = blob(REV, p).decode(errors="replace")
    revs = sorted(set(re.findall(r"\b[0-9a-f]{40}\b", t)))
    named = [r[:9] for r in revs if git("cat-file", "-e", r + "^{commit}", check=False).returncode == 0]
    print("%-58s 40-hex commits=%s" % (p.split("/")[-1], named))

hdr("8 assert predicates: matching context in REV blobs (read only)")
def ctx(p, needle):
    t = blob(REV, p).decode(errors="replace")
    return [ln.strip()[:160] for ln in t.splitlines() if needle in ln][:3]
F = ".ufo/evidence/round-18/final/"
for p, n in ((F + "probes.stdout", "open=0 closed=11 total=11"),
             (F + "regression.stdout", "cases=8 passed=8"),
             (F + "historical.stdout", "cases=4 passed=4"),
             (F + "case7.stdout", "killed=5 survived=5 inconclusive=0 kill-rate=50%"),
             (F + "case8.stdout", "killed=5 survived=5 inconclusive=0 kill-rate=50%"),
             (F + "repeat.stdout", "controls_match")):
    print("%-18s %r -> %s" % (p.split("/")[-1], n, ctx(p, n)))
rr = json.loads(blob(REV, F + "registry-branch-aligned.stdout"))
print("registry-branch-aligned: held=%s total=%s superseded=%s exit=%s rev=%s"
      % (rr.get("held"), rr.get("total"), rr.get("superseded"), rr.get("exit"), str(rr.get("rev"))[:12]))
for p in ("disposition.stdout", "before.stdout"):
    print(p, "status=", json.loads(blob(REV, F + p)).get("status"))
print("repeat.stdout full:", blob(REV, F + "repeat.stdout").decode())
print("context.stdout full:", blob(REV, F + "context.stdout").decode())
ck = json.loads(blob(REV, F + "checks.json"))
print("checks.json rows (exit):", {k: v["exit"] for k, v in ck.items()})

hdr("9 round-19 changes since BASE touching bound paths")
bound = set(tr["inputs"]) | {P_OUT, P_ERR, P_TR, P_LED, P_REP}
ns = git("diff-tree", "-r", "--name-status", "--no-renames", BASE, tips["master"]).stdout.decode().splitlines()
print("BASE..master changed paths:", len(ns))
print("intersect bound:", [x for x in ns if x.split("\t", 1)[-1] in bound])
dirty = [p for p in sorted(bound) if sha(wt(p)) != sha(blob(BASE, p))]
print("worktree vs BASE differs for bound paths:", dirty)
```

`/tmp/audit1846/c1impact.py` (sha256 `e01362a5…356906`):

```python
#!/usr/bin/env python3
"""Audit1846: does round-19 (BASE..master) disturb what audit-1846 bound?

Read-only: cat-file / diff-tree / diff on commits only; GIT_* removed,
GIT_OPTIONAL_LOCKS=0. Sectionizer re-implements assemble.py's documented
rule (HEADING_RE ^#{1,3}(\\s|$), fence-aware, trailing blank lines stripped).
"""
import hashlib
import json
import os
import re
import subprocess

L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4"
BASE = "7243e7f163f08978c8fd9b6c1ef67a2fefe7d190"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV["GIT_OPTIONAL_LOCKS"] = "0"
HEADING_RE = re.compile(r"^#{1,3}(?:\s|$)")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
SEC_SHA = "ad2320cb7770e47aa5fa628f0a0aa96e751e42c821cff4fe9d0c9fe03af0dcd9"
HEAD = "### Round-17 gate/probe registry \u2014 re-pin and monitor"


def git(*a):
    r = subprocess.run(["git", "-C", L, *a], capture_output=True, env=ENV)
    assert r.returncode == 0, (a, r.stderr)
    return r.stdout


def sectionize(text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    in_f, mk, hs = False, "", []
    for i, ln in enumerate(lines, 1):
        m = FENCE_RE.match(ln)
        if m:
            if not in_f:
                in_f, mk = True, m.group(1)[0]
            elif m.group(1)[0] == mk:
                in_f = False
            continue
        if not in_f and HEADING_RE.match(ln):
            hs.append(i)
    b = [(1, hs[0] - 1, "")] if hs and hs[0] > 1 else []
    for k, h in enumerate(hs):
        b.append((h, hs[k + 1] - 1 if k + 1 < len(hs) else len(lines), lines[h - 1]))
    out = []
    for s, e, h in b:
        body = lines[s - 1:e]
        while body and not body[-1].strip():
            body.pop()
        out.append((s, e, h, hashlib.sha256("\n".join(body).encode()).hexdigest()))
    return out


master = git("rev-parse", "refs/heads/master").decode().strip()
pages = {"REV": git("cat-file", "blob", REV + ":SKILL.md"),
         "BASE": git("cat-file", "blob", BASE + ":SKILL.md"),
         "78b99dd": git("cat-file", "blob", "78b99dd:SKILL.md"),
         "master": git("cat-file", "blob", master + ":SKILL.md"),
         "worktree": open(os.path.join(L, "SKILL.md"), "rb").read()}
for k, v in pages.items():
    secs = sectionize(v.decode())
    hit = [s for s in secs if s[2] == HEAD]
    print("%-8s SKILL sha=%s sections=%d heading-at=%s sec-sha-match=%s sha-present-anywhere=%s"
          % (k, hashlib.sha256(v).hexdigest()[:12], len(secs),
             [(s[0], s[1]) for s in hit], [s[3] == SEC_SHA for s in hit],
             any(s[3] == SEC_SHA for s in secs)))
print("worktree SKILL == master SKILL:", pages["worktree"] == pages["master"])
print("\nBASE..master hunks in SKILL.md:")
d = git("diff", "--unified=0", BASE, master, "--", "SKILL.md").decode()
print("\n".join(ln for ln in d.splitlines() if ln.startswith("@@")))
print("\nBASE..master name-status:")
print(git("diff-tree", "-r", "--name-status", "--no-renames", BASE, master).decode())
for c in ("78b99dd", master):
    print("commit %s touches:" % c[:9])
    print(git("diff-tree", "-r", "--name-status", "--no-renames", "--no-commit-id", c).decode())
```

Tool installs or updates: none.
