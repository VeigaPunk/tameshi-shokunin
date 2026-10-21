# Audit1164 — round-19 w1 — retained round-18 receipt `audit-1164`

Seat `TameshiR19-2.Audit1164` (reviewer, read-only, advisory — not closure). Read 2026-10-21.
`L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Claim served: C1 no-harm/source/verification boundary.

**Verdict.** The receipt is internally consistent. The stdout is byte-for-byte the output that its traced argv would print from the recorded inputs. All 14 recorded input hashes match the blobs at the self-reported revision `a9c94c5`. All nine asserted predicates hold over those blobs. The C1 repairs, as delivered at `21e7932`, do **not** invalidate this evidence. Two Low findings limit what the receipt can be cited for. Neither one is a C1-routed defect.

## Scope, sources, commands (no receipt argv executed)

- Read: `final/audit-1164.stdout`, `final/audit-1164.stderr`, and `coldread/traces/L1/audit-1164.json` (all under `$L/.ufo/evidence/round-18/`).
- Read the ledger entry at `coldread/ledger.json:12129-12170` (`start` 1164, `skill_sha256` `1334c512…`).
- Followed the entry's `reports` pointer: read `.ufo/waves/round-18/w3/L1Residual.md:214-261` and line 3 of the same file.
- Read one key of the input `final/checks.json` at blob `fed3c8e6…`: `bash-witness-selftest`, plus the per-key exit codes.
- Git commands were object reads only, run as `git --no-optional-locks -C $L` with all `GIT_*` variables unset. They were `rev-parse`, `cat-file blob`, `merge-base --is-ancestor`, `log`, and `diff --stat/--name-only/-U0`.
- No `jj` commands were run, because jj snapshots the working copy. Nothing was written except this report. No tools were installed.
- No `lsp` device exists in this session. That does not matter here: no code symbols are in scope, only text/JSON evidence.
- Lane-wide grep with gitignore off: `cd96fb063584` (stdout sha) → 0 hits. `d0af0495cb43` (trace sha) → 0 hits. `6982b649…` → 1 hit, the ledger entry. `audit-1164` → only `ledger.json:12159`, the trace itself, and `.jj/working_copy/tree_state`.

## Observed facts (O)

| # | Fact | Observed |
|---|---|---|
| O1 | `audit-1164.stdout` | sha256 `cd96fb063584045b033764b94df8fc106a6e204a0db842f80c5863b1b770d19f`, 5764 B, git blob `abe52b9c…` |
| O2 | `audit-1164.stderr` | 0 B, sha256 `e3b0c442…b855` (empty), blob `e69de29b…`; consistent with trace `"exit": 0` |
| O3 | trace JSON | sha256 `d0af0495…2884`, 5545 B, blob `6391f835…`; schema `tameshi-trace-inputs-v1`; `rev` `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`; `tracked_filter` true; `untracked`/`external`/`live_lane_reads` empty; `dropped_home_count` 0 |
| O4 | History of the trio | All three files were added in `a134a09` and appear in no later commit. Blobs are identical at `a134a09`, `a85f710`, `4b7c682`, `7243e7f`, and `21e7932`, and in the working copy (WC). None of the three exists at `a9c94c5`. |
| O5 | Lineage | `a9c94c5` → `a134a09` → `a85f710` → `4b7c682` → `7243e7f` (frozen baseline) → `78b99dd` → `21e7932` (git HEAD, "round-19: correct routed metadata and retain effective historical receipts"). `--is-ancestor` reports yes for every edge. |
| O6 | Argv → stdout | My own code reproduced the argv's print logic over `git cat-file` blobs at `a9c94c5` (code below). Result: **byte-identical**, sha `cd96fb06…`, 5764 B. Same section text, 13 `OPEN` lines in spec order, ledger first line + `TAIL`, and the `VERIFIED` line. |
| O7 | Asserted predicates at `a9c94c5` | registry `held==total==31` → (31,31). The probes, regression `8/8`, historical `4/4`, case7, case8 and `controls_match` substrings are all present. disposition `status` = `clean`; before `status` = `failed`. All nine hold. |
| O8 | Input binding | All 14 trace `inputs` hashes equal the blobs at `a9c94c5`. They also equal the blobs at `a85f710`, `4b7c682` and `7243e7f`. At `21e7932` and in the WC, 13/14 still match; only `SKILL.md` changed (O10). |
| O9 | Ledger ↔ trace | The ledger `inputs` equal the trace inputs minus `SKILL.md` (listed in `inputs_dropped`). `skill_sha256` equals the trace's `SKILL.md` hash and `_meta.expect_skill_sha`. `read_rev` equals the trace `rev`. `commands_executed_count` = 1, and exactly one entry cites this trace. The entry is identical at `a134a09`, `a85f710` and HEAD. |
| O10 | Section range | Argv spec covers lines 1164–1210; the ledger has `end` 1211. Line 1211 is `''`. The ledger `sha256` `6982b649…` = sha256 of `'\n'.join(lines 1164..1210)` = exactly the printed `SECTION` text. **No defect.** At HEAD those lines are identical and keep the same numbering; the only SKILL.md change since `7243e7f` is one added line at 1935, a `measure.py` registry row. |

## Findings (by severity)

**L1 — Low (receipt wording overclaims; historical, disclosed).** The last stdout line reads, verbatim: "VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision" (`audit-1164.stdout`, last line; `a134a09`, 2026-10-20).

- This is a string literal (trace JSON line 33, argv[29]). It is printed only after the nine substring/field assertions pass, and nothing else conditions it.
- The script contains no `rev`, `git`, `trace`, `exit` or ancestor logic. It reads no other revision, no trace or argv of the asserted receipts, and no instrument blob except `tools/mutate-and-run.sh` at the read tree.
- **Established by the receipt:** section bytes, 13 hashes/sizes, and nine content predicates.
- **Not established by the receipt:** "actual execution" provenance, and instrument identity across ancestors.
- **Independent git check (outside the receipt):** no `tools/` path changed in `921ef807..a9c94c5` or `5923d89..a9c94c5`, and the `mutate-and-run.sh` blob `d22c4025…` is unchanged. The clause is therefore not false for `tools/`. It is simply not established by this receipt.
- **Mitigation already present:** the ledger verdict is `gap-minor`. The report's minor gap discloses ancestor pinning: "Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments." (`L1Residual.md:222`, 2026-10-20). Its header says: "This is input-keyed evidence, not complete required-command coverage." (`L1Residual.md:3`, `a85f710`, 2026-10-20).
- **Failing criterion:** a receipt line asserts facts its command did not compute. Do not cite `audit-1164` for execution provenance. If it is ever cited that way, append a dated erratum; do not edit the receipt.

**L2 — Low (intersects C1 defect 4; the receipt only hashed this file).**
- `checks.json` at `fed3c8e6` is an input of this receipt and was opened for hashing only. Its `bash-witness-selftest` row records argv `python3 tools/bash-witness-study.py --selftest`, revision `921ef807…`, `exit` 64, and an empty `stdout_sha256`. Its `registry` row records `exit` 1.
- `audit-1164` printed `VERIFIED` over this bundle without reading any of it. Spot-check §5.4: "Do not leave a failed invocation as the selftest row of the final receipt bundle." (`corpus/lessons/round-18-verifier-spotcheck.md:199-200`, `7243e7f`, 2026-10-21).
- **Consequence:** `audit-1164` cannot detect defect 4 and must not be used as evidence for it, either way. The C1 defect-4 repair must rest on its own receipts. Observed: new files under `.ufo/evidence/round-19/bash-witness-selftest*`, and `checks.json` byte-identical at HEAD.

**I1 — Info (no recorded stdout binding; closed here by determinism).**
- The stdout and stderr hashes are recorded nowhere: not in the trace (it has no stdout/stderr fields), the ledger entry (`traces` only), the report, `checks.json`, or `traced-commands.json` (zero `audit` hits).
- Binding rests on filename convention, on co-addition in `a134a09`, and on O6's byte-identical derivation. For this receipt the derivation closes the gap. A ledger that recorded receipt hashes would not need re-derivation.

**I2 — Info (the revision pin is a self-report).**
- The inputs are byte-identical at `a9c94c5`, `a85f710`, `4b7c682` and `7243e7f`, so they are consistent with `a9c94c5` but do not uniquely imply it.
- The established facts do not depend on which of those revisions was read. No run timestamp is recorded.
- The scratch root `/tmp/tameshi-r18-L1-final-a2vitd82` still exists (`ls -d`). It was not inspected (out of scope).

**I3 — Info (trace environment record vs. effective environment).**
- `env_overrides` lists tracer-level changes: `PYTHONPYCACHEPREFIX` set, and `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_NOSYSTEM` removed. The argv's `env -i` clears these and re-sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`.
- The measured `python3`'s effective environment is therefore the argv's explicit list.
- Interpreter identity is unrecorded. Today the argv PATH resolves only `/usr/bin/python3` (→ `python3.14`); the run-time interpreter is unknown.
- Both points are immaterial given O6.

## Could C1 repairs invalidate this historical evidence?

**As delivered (`21e7932` and the WC at read time): no.**
- Zero paths under `.ufo/evidence/round-18/` changed between `7243e7f` and `21e7932`.
- The receipt trio and `ledger.json` (`d654f3d2…`) are unchanged, and the 1164 entry is unchanged.
- 13 of 14 inputs are byte-identical.
- `SKILL.md`'s whole-file hash moved from `1334c512…` to `4d0190fd…`, so whole-file pins (`skill_sha256`, `_meta.expect_skill_sha`) no longer equal HEAD. Lines 1164–1210 are unchanged in bytes and numbering, and the section sha recomputed at HEAD still equals `6982b649…`.
- `_meta.carry_coverage_basis` = `section_sha256`. [INFERENCE: field name only; the carry/measure code was not read] A section-sha carry would still credit this entry.

**Where C1 meets this receipt.**
- Of the five §5 targets, only defect 4 (`checks.json`) touches its inputs.
- The receipt never asserts anything about `checks.json` content (L2), so repairing defect 4 cannot falsify any of its nine predicates.
- Defects 1, 2, 3 and 5 touch files that are not inputs: `guard-kill-closure.md`, `mutation-case-kumitate-sources-check.md`, `lessons/round-18.md`, and new `round-19/round18-final-measure.*` receipts. They were delivered as appends or new files.

**Ways a repair would have broken it (all avoided at `21e7932`):**
- rewriting `final/checks.json` in place, which breaks input hash `fed3c8e6`;
- editing `corpus/knowledge/fleet-kill-rate-ledger.md` or `tools/mutate-and-run.sh`;
- inserting or removing `SKILL.md` lines at or before 1210, which shifts or alters the section.

Even then the receipt would stay valid as a record at `a9c94c5`. It would no longer reproduce at the tip.

## Residual risk / verification gaps

- If L1 delivers a revision after `21e7932`, re-hash these 18 paths: the 14 inputs, the trio, and `ledger.json`. Also recheck the `SKILL.md` 1164–1210 section sha.
- Not done (out of scope): the carry/measure code (`assemble.py`, `round-19/measure.py`), the provenance traces of the nine asserted receipts, the scratch clone, and run-time interpreter identity.
- Execution provenance of the asserted receipts remains unverified by this receipt (L1).

## Independent derivation code (run in-session; reads git blobs only; receipt argv not executed)

```python
import subprocess, os, hashlib, json
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; R='a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4'
ENV={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
blob=lambda p: subprocess.run(['git','--no-optional-locks','-C',L,'cat-file','blob',f'{R}:{p}'],capture_output=True,env=ENV,check=True).stdout
t=json.load(open(L+'/.ufo/evidence/round-18/coldread/traces/L1/audit-1164.json')); spec=json.loads(t['argv'][-1])
lines=blob('SKILL.md').decode().splitlines()
out=[f"SECTION {spec['start']} {spec['end']}", '\n'.join(lines[spec['start']-1:spec['end']])]
for p in spec['paths']:
    raw=blob(p); out.append(f"OPEN {p} sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}")
    if p.startswith('corpus/knowledge/'): out+= [raw.decode().splitlines()[0], 'TAIL '+raw.decode()[-700:]]
out.append('VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision')
assert ('\n'.join(out)+'\n').encode()==open(L+'/.ufo/evidence/round-18/final/audit-1164.stdout','rb').read()
```
