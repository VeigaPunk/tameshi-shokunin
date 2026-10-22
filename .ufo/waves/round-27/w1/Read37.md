# Read37: cold read of SKILL.md:1964, "Round-21 gate/probe registry — finite environment differential"

**Verdict: wrong-expectation.** Class: `record`. The clone is detached at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, and its SKILL.md sha256 (386de44b…51e95) matches the pinned value. One stated expectation is false at that revision: line 2077 calls 47 the "current registry battery", but `tools/registry.json` has 49 active rows. Everything else I could check holds. The minor gaps below are wording, citation and prerequisite issues.

## Evidence

### 1. Wrong expectation (one)

- SKILL.md:2077 says "The 47-row current registry battery". Read37-9 reports, for `tools/registry.json` at 2227 (sha256 c1b75366…): 56 rows, 49 `active`, 7 `superseded`. The two active rows after the round-24 set are `mte-interop-selftest` and `mte-interop-check` (tag `new-r26`).
- 47 is the round-24 total. `corpus/lessons/round-24.md:76` reads "registry 47/47 held, 7 superseded, exit 0", and `:206` repeats 47/47; `corpus/lessons/round-24-verifier-spotcheck.md:35` and `:39` say the same (Read37-34). 49 minus the two new-r26 rows is 47, which matches.
- A reader could take 47 as 49 minus the two declared-live rows (`pin-disposition-read`, `verify-round15`), which is also 47. That reading does not fit the record: `tools/registry-check.py` counts every active row, live rows included (its docstring, Read37-25), and the round-24 47/47 is the full held count.
- The monitor flag `input-drift:tools/registry.json` is consistent with this same change.

### 2. Checked and holding (receipts in parentheses)

- Source ids: `corpus/SOURCES.md` lines 88 (S079), 91 (S082), 92 (S083), 93 (S084) and 94 (S085) are `mined`; line 89 (S080) is `rejected` and the section does not cite it. S028 (line 39) and S049 (line 58) exist (Read37-5, Read37-27).
- `corpus/lessons/round-21.md:79-80` carries QUALITY43 and QUALITY44 (Read37-6).
- Selftests run in the clone: env-diff 9/9 (Read37-20), wave-route-mix 8/8 (Read37-19), wave-accounting 8/8 and 16/16 (Read37-18), command-binding 44/44 (Read37-17), registry-replay 10/10 (Read37-16).
- Round-22 entries: the round-22 bundle exits 0 with completed 66, dead 80, seats 146 (Read37-12, exit in Read37-32); the wrong-count pair exits 1 with TOTAL_MISMATCH (Read37-13, Read37-32). The frozen round-22 counter has 8 CASES (Read37-26); the 16 supplemental cases pass (Read37-18).
- Round-23 entries: the frozen bundle exits 0 with bundle_sha256 3d6c99… (Read37-14). The source-read pair exits 1 with ARGV_MISMATCH and db6206… (Read37-15). The round-23 frozen counter has ten CASES (Read37-24). The replay bundle holds 43 requirements and 43 receipts, including `pin-disposition-read` and `verify-round15` (Read37-23).
- New round-24 rows: `registry-check --tag new-r24` holds 4/4 (Read37-35): command-binding-selftest-r24 at 44/44, both pinned bundle digests, and registry-replay-selftest at 10/10.
- Superseded row: `registry-check --only command-binding-selftest` runs the row. Its stdout lacks `COMMAND_BINDING_SELFTEST: 38/38 pass`, so it does not hold, and it sits outside the active tally (`held=0/0 superseded=1`, Read37-36). The section's "still runs, fails against 44/44, excluded from the active tally" holds.
- Round-21 instruments: `git diff --stat 33d03b7 2227d83…` over c1-survivors.py, c2-count.py, c1-mutants.json and c2-contract.json is empty. Only `tools/round21-measure.py` differs (+162 lines) (Read37-37). That supports "unchanged from 33d03b7" and "without rewriting those instruments".
- Round-21 counters: c2-contract.json has 9 surfaces and 7 required profiles, and f5/receipt.json has 9 surfaces (Read37-10). c1-mutants.json has 18 mutants (Read37-28, Read37-38). The C1 mutants include environment and git-config pins (MB03–MB10 on bash-witness-study.py) and process-identity guards in registry-check.py (R05, R07), which supports the caveat at SKILL.md:1980–1982 (Read37-38). c2-count.py checks pins, tuple arithmetic and a source header, and reads git objects at REV (Read37-11).
- Round-21 probes: the round21 facade reads sibling repos through `git show` at line 74 (Read37-33). The coldread selector imports the round-18 algorithm and refuses the three override flags (Read37-2).
- Round-23 replay: replay.py:60 calls `run_row(..., retain_streams=True)`. `tools/registry-check.py` defines `run_row` at line 648 with that parameter at line 724 (Read37-33).
- Round-24: the ruler has eleven K predicates (Read37-25). Errata E through P are all present in `corpus/lessons/round-24.md` (Read37-31). `tools/registry-replay.py` `project()` refuses on RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED and STREAM_LIMIT, and `publish()` writes nothing on refusal, so an older bundle stays in place (Read37-3, code reading; selftest Read37-16).
- C1 caveat: the mutant list supports "child-environment/command-pin contracts and synthetic process identities" (Read37-38). I did not test "not demonstrated malicious hooks or PID reuse".

### 3. Live routing check (route-mix row)

- Read37-21 and Read37-32: `wave-route-mix.py --spec .ufo/waves/round-21/spec1.json --json` exits 1 on this host (REFUSE; opencode-go 38/71 above the 0.40 bound).
- Read37-28: the retained round-20 `.exit` file is 1 and its stderr shows REFUSE (openai-codex 35/72). This matches `corpus/lessons/round-21.md:79` for round 20.
- `corpus/lessons/round-21.md:79` records the round-21 spec at 28/71 and exit 0 (Read37-40). The gate reads live operator routing, so the round-21 acceptance is not reproducible at this host.

## Smallest safe correction

- SKILL.md:2077: replace "The 47-row current registry battery" with "The 49 active rows of `tools/registry.json` at this revision (47 at round 24, before the two new-r26 mte-interop rows)". If 47 should stay, anchor it to round 24.

## Minor gaps (true but imprecise; fix in the same edit)

1. Run-together tokens: SKILL.md:1968 "from33d03b7" (commit exists; Read37-37 confirms the instruments are unchanged from it); :1976 "max-share0.40" (flag `--max-share`, default 0.40); :1978 "selftest0 clean/1 failed"; :1986 "retain the199-entry prefix"; :1990 "minedS082"; :2001 "cover16"; :2004 "is1/TOTAL_MISMATCH" (exit 1, Read37-13); :2008 "exits0" (help exit 0, code reading); :2011 "minedS083"; :2012 "including62/62"; :2019 "expected1/ARGV_MISMATCH" (exit 1, Read37-15); :2044 "minedS084/S085". Each value checks out. The joins hide the number boundaries and break exact search.
2. Env-diff row (SKILL.md:1975) does not name bubblewrap as a prerequisite. `tools/env-diff.py:57-60` returns BWRAP_UNAVAILABLE without it; by code reading (not run), every surface then becomes unavailable and the run exits 1. The entry also runs each pinned sibling selftest under bwrap (`tools/env-diff.py:68-70`; sibling blobs come from `git show` in `read_surface`), which the write-scope cell ("sibling blobs read-only, no network") does not say. bwrap works here: the sensitivity cases pass (Read37-20).
3. Route-mix row (SKILL.md:1976): "round21 accepted spec retained" is true as a file statement. The verdict reads live routing (`~/.omp/agent/config.yml`), and on this host the same command now exits 1 (see section 3). Say that the verdict depends on routing, and give 28/71 as the round-21 record.
4. Citation placement: SKILL.md:2012 "62/62" is in `corpus/lessons/round-23.md:58,98,100` and `corpus/lessons/round-22.md:150`, not in `corpus/knowledge/required-command-binding.md` (Read37-7, Read37-34). SKILL.md:1990 "QUALITY45" is in `corpus/lessons/round-22.md:46`, not in `callback-authoritative-accounting.md` (Read37-7). SKILL.md:2044 "QUALITY48" is in `corpus/lessons/round-24.md:53` and `corpus/QUALITY.md:506`, not in `replay-projection-hardening.md` (Read37-7, Read37-34).
5. Unverified prefix: SKILL.md:1986 repeats `corpus/lessons/round-21.md:158` ("retains its199-entry prefix"). The round-21 ledger at 2227 has 304 entries (read with `git show`; see external inputs). That fits a 199-entry prefix, but I did not compare its first 199 entries with an earlier ledger.
6. Registry-replay table row (SKILL.md:2052) still says the write scope is "writes only under --out". The correction at SKILL.md:2062–2072 says that cell is not a reliable safety promise. Strike or mark the cell so the table and the correction agree.
7. Probe entries (SKILL.md:1977–1978) name the live lane path as `--repo`. The probes read git objects at REV, so results stay rev-pinned, but a clone-based cold read must substitute its own path. The section does not say so.

## Not run, and why

- `.ufo/evidence/round-21/coldread/measure.py --selftest` and `--explain`: the selector reads the excepted round-21 ledger, and the rules bar opening it under the collector. I read that ledger only with `git show`.
- `tools/env-diff.py --contract …` (the entry): runs nine pinned sibling selftests under bwrap. That is outside the bound that keeps sibling lanes untouched.
- `tools/round21-measure.py --claim c1|c2`, its `--selftest`, `c1-survivors.py` and `c2-count.py`: they run sibling mutants or read sibling object stores (`tools/round21-measure.py:74`).
- `tools/mutate-and-run.sh --regression`: heavy, and it reads sibling object stores (`tools/mutate-and-run.sh:630`, `:1338–1339`).
- `.ufo/evidence/round-23/replay.py` and `.ufo/evidence/round-24/measure.py`: they clone and run 43 rows (two live-dependent) and eleven predicates.
- `tools/registry-replay.py --run` and `--plan`: the selftest covers projection and plan fixtures (Read37-16), not `--run`.
- The full registry battery: heavy, and it includes sibling-reading rows.
- Not checked: the provenance of "round20 strict override refusal" (SKILL.md:1978); "revision_pinned=41" (formula only; no run produced it); "Normal --help exits 0" (code reading only).

## Scope, receipts and bounds

- Class `record`: the section states registry facts with pointers, and its entry commands describe tools rather than a sequence to follow. The evidence is the reads, the selftests and the frozen-bundle gates listed above.
- Traces list Read37-1 to Read37-29 and Read37-31 to Read37-41. Every listed receipt has `rev` 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, `rev_reason` null, and empty `external`, `live_lane_reads` and `untracked` objects. A positive control and a negative search over the receipts confirmed this.
- Excluded: Read37-30 is a broad `grep -rn` over `corpus/` and the round-22 to round-24 evidence folders. Its input set is a tree-wide sweep that I cannot list by hand. No verdict depends on it: its hits were checked with the targeted searches Read37-34 and Read37-40. Its receipt file remains in the traces folder, and I disclose it here rather than list its inputs.
- The round-21 ledger was read only with `git show` (sha256 1bd763a5…), as the rules require for the three excepted files. I did not open SCORECARD.md or LOG.md.
- After the traces, I read the first lines of my own receipts to copy argv and exit values. Those reads are not cold-read inputs. Read37-41 checks the JSON block in this report.
- The route-mix gate read `~/.omp/agent/config.yml`. The collector does not hash /home paths, so its digest (887fbbb3…) came from a receipt-only `sha256sum` (Read37-39) and is listed under external inputs.
- Tooling: nothing was installed or updated. Present on the host: strace (`/usr/bin/strace`), python3 3.14.8, git 2.56.0, uv (`~/.local/bin/uv`). bubblewrap works, since the env-diff sensitivity cases pass.

## Machine-readable record

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read37",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 1964,
      "heading": "### Round-21 gate/probe registry \u2014 finite environment differential",
      "class": "record",
      "verdict": "wrong-expectation",
      "blocking_gaps": [],
      "wrong_expectations": [
        "SKILL.md:2077 says 'The 47-row current registry battery'. At 2227d83 tools/registry.json has 49 active rows (56 rows, 7 superseded); the two extra active rows are mte-interop-selftest and mte-interop-check (tag new-r26). 47 is the round-24 total (corpus/lessons/round-24.md:76, registry 47/47 held). Fix: state 49 at this revision, or anchor 47 to round 24."
      ],
      "minor_gaps": [
        "Run-together tokens: SKILL.md:1968 'from33d03b7', :1976 'max-share0.40', :1978 'selftest0 clean/1 failed', :1986 'retain the199-entry prefix', :1990 'minedS082', :2001 'cover16', :2004 'is1/TOTAL_MISMATCH', :2008 'exits0', :2011 'minedS083', :2012 'including62/62', :2019 'expected1/ARGV_MISMATCH', :2044 'minedS084/S085'. Each value checks out; the joins hide the number boundaries.",
        "Env-diff row (SKILL.md:1975) does not name bubblewrap as a prerequisite (tools/env-diff.py:57-60 returns BWRAP_UNAVAILABLE without it; by code reading the run then exits 1 with every surface unavailable) and does not say the entry runs each pinned sibling selftest under bwrap (tools/env-diff.py:68-70). bwrap works here (Read37-20 sensitivity cases pass).",
        "Route-mix row (SKILL.md:1976): 'round21 accepted spec retained' is true as a file statement, but the verdict reads live operator routing (~/.omp/agent/config.yml). On this host the same command exits 1 (REFUSE, opencode-go 38/71 above 0.40; Read37-21, Read37-32). corpus/lessons/round-21.md:79 records 28/71 and exit 0. Say the verdict is routing-dependent.",
        "Citation placement: SKILL.md:2012 '62/62' is in corpus/lessons/round-23.md:58,98,100 and round-22.md:150, not in required-command-binding.md; SKILL.md:1990 'QUALITY45' is in corpus/lessons/round-22.md:46, not in callback-authoritative-accounting.md; SKILL.md:2044 'QUALITY48' is in corpus/lessons/round-24.md:53 and corpus/QUALITY.md:506, not in replay-projection-hardening.md.",
        "Unverified prefix: SKILL.md:1986 repeats corpus/lessons/round-21.md:158 ('retains its199-entry prefix'). The round-21 ledger at 2227 has 304 entries (git show; external_inputs), which fits a 199-entry prefix, but its first 199 entries were not compared with an earlier ledger.",
        "Registry-replay table row (SKILL.md:2052) still says write scope is 'writes only under --out'; the correction at SKILL.md:2062-2072 says that cell is not a reliable safety promise. Strike or mark the cell.",
        "Probe entries (SKILL.md:1977-1978) name the live lane path as --repo. The probes read git objects at REV, so results are rev-pinned, but a clone-based cold read must substitute its own path, which the section does not say."
      ],
      "commands_executed": [
        "cat tools/env-diff.py tools/wave-route-mix.py",
        "cat tools/round21-measure.py .ufo/evidence/round-21/coldread/measure.py",
        "cat tools/wave-accounting.py tools/command-binding.py tools/registry-replay.py",
        "python3 -c import json,sys; d=json.load(open('tools/registry.json')); print(type(d).__name__, len(d) if hasattr(d,'__len__') else ''); print(json.dumps(d, indent=1)[:60000])",
        "python3 -c import re; t=open('corpus/SOURCES.md', encoding='utf-8').read().splitlines(); print('lines', len(t)); print('\\n'.join(t[:3])); ids=set(re.findall(r'\\bS(\\d{3})\\b', '\\n'.join(t))); print('distinct S-ids', len(ids), 'min', min(ids), 'max', max(ids)); [print(i+1, l[:300]) for i,l in enumerate(t) if re.search(r'\\bS(079|028|049|080|082|083|084|085)\\b', l)]",
        "python3 -c import re; files=['corpus/lessons/round-21.md','corpus/knowledge/hermetic-env-differential.md']; [print(f, 'lines', len(open(f,encoding='utf-8').read().splitlines()))) for f in files]; [print(f+':'+str(i)+': '+l[:500]) for f in files for i,l in enumerate(open(f,encoding='utf-8').read().splitlines(),1) if re.search(r'QUALITY4[34]|S079|S028|S049|^#', l)]",
        "python3 -c import re; files=['corpus/knowledge/callback-authoritative-accounting.md','corpus/knowledge/required-command-binding.md','corpus/knowledge/replay-projection-hardening.md']; [print(f+' lines '+str(len(open(f,encoding='utf-8').read().splitlines()))) for f in files]; [print(f+':'+str(i)+': '+l[:500]) for f in files for i,l in enumerate(open(f,encoding='utf-8').read().splitlines(),1) if re.search(r'QUALITY4[5-8]|S08[2-5]|^#|62/62', l)]",
        "python3 -c import re; f='corpus/lessons/round-24.md'; t=open(f,encoding='utf-8').read().splitlines(); print('lines', len(t)); [print(str(i)+': '+l[:300]) for i,l in enumerate(t,1) if re.search(r'^#|Errata|QUALITY4[6-8]|S08[4-5]|eleven|predicate|ruler', l)]",
        "python3 -c import json,collections; d=json.load(open('tools/registry.json', encoding='utf-8')); rows=d['rows']; print('rows', len(rows)); print('status', dict(collections.Counter(r.get('status') for r in rows))); print('kind', dict(collections.Counter(r.get('kind') for r in rows))); print('active', len([r for r in rows if r.get('status')=='active'])); print('external', [r['name'] for r in rows if r.get('external') is True]); print('new-r24', [r['name'] for r in rows if 'new-r24' in r.get('tags',[])]); print('new-r21', [r['name'] for r in rows if 'new-r21' in r.get('tags',[])]); print('active-new-r26', [r['name'] for r in rows if 'new-r26' in r.get('tags',[]) and r.get('status')=='active']); print('superseded', [(r['name'], r.get('superseded_by')) for r in rows if r.get('status')=='superseded'])",
        "python3 -c import json; c=json.load(open('.ufo/evidence/round-21/c2-contract.json', encoding='utf-8')); print('keys', sorted(c)); print('surfaces', len(c.get('surfaces',[]))); print('required_profiles', c.get('required_profiles')); print('receipt_schema', c.get('receipt_schema'), 'receipt_path', c.get('receipt_path')); print([s.get('name') for s in c.get('surfaces',[])]); r=json.load(open('.ufo/evidence/round-21/f5/receipt.json', encoding='utf-8')); print('f5 keys', sorted(r)); print('f5 surfaces', len(r.get('surfaces',[])))",
        "cat .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/c2-count.py",
        "python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/bundle.json --expected .ufo/evidence/round-22/expected.json --json",
        "python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/wrong-count-bundle.json --expected .ufo/evidence/round-22/wrong-count-expected.json --json",
        "python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json",
        "python3 tools/command-binding.py --bundle .ufo/evidence/round-23/source-read-bundle.json --expected .ufo/evidence/round-23/source-read-expected.json --json",
        "python3 tools/registry-replay.py --selftest",
        "python3 tools/command-binding.py --selftest",
        "python3 tools/wave-accounting.py --selftest",
        "python3 tools/wave-route-mix.py --selftest",
        "python3 tools/env-diff.py --selftest",
        "python3 tools/wave-route-mix.py --spec .ufo/waves/round-21/spec1.json --json",
        "sha256sum tools/trace-inputs.py tools/registry-check.py tools/env-diff.py tools/round21-measure.py tools/wave-accounting.py tools/command-binding.py tools/registry-replay.py tools/wave-route-mix.py",
        "python3 -c import json; b=json.load(open('.ufo/evidence/round-23/replay/bundle.json', encoding='utf-8')); print('keys', sorted(b)); print('requirements', len(b['requirements']), 'receipts', len(b['receipts'])); print('revision', b['revision'], 'cwd', b['cwd']); print('names', [r['name'] for r in b['receipts']]); print('expected', open('.ufo/evidence/round-23/replay/expected.json', encoding='utf-8').read().strip()); x=json.load(open('.ufo/evidence/round-23/extra-cases.json', encoding='utf-8')); print('round23 extra cases', len(x['cases']) if isinstance(x, dict) and 'cases' in x else type(x).__name__); y=json.load(open('.ufo/evidence/round-24/extra-cases.json', encoding='utf-8')); print('round24 extra cases', len(y['cases']) if isinstance(y, dict) and 'cases' in y else type(y).__name__)",
        "cat .ufo/evidence/round-23/measure.py .ufo/evidence/round-23/replay.py",
        "cat .ufo/evidence/round-24/measure.py tools/registry-check.py",
        "cat .ufo/evidence/round-22/measure.py .ufo/evidence/round-18/measure.py",
        "python3 -c import re; rows=[l for l in open('corpus/SOURCES.md', encoding='utf-8').read().splitlines() if re.match(r'^\\|\\s*S\\d{3}\\s*\\|', l)]; print('table rows', len(rows)); [print(' || '.join(c.strip()[:110] for c in l.split('|')[1:-1])) for l in rows if re.match(r'^\\|\\s*S0(79|8[0-5])\\s*\\|', l)]; print('199 mentions', sum(1 for l in open('corpus/SOURCES.md', encoding='utf-8') if '199' in l)); print([l[:160] for l in open('corpus/SOURCES.md', encoding='utf-8').read().splitlines() if '199' in l][:5])",
        "python3 -c print(repr(open('.ufo/evidence/round-21/routemix-r20-spec1.exit', encoding='utf-8').read())); print(open('.ufo/evidence/round-21/routemix-r20-spec1.stderr', encoding='utf-8').read()[:1500]); import json; m=json.load(open('.ufo/evidence/round-21/c1-mutants.json', encoding='utf-8')); print('c1 mutants', len(m['mutants']), [x['id'] for x in m['mutants']])",
        "python3 -c import re; t=open('tools/mutate-and-run.sh', encoding='utf-8').read().splitlines(); print('lines', len(t)); [print(str(i)+': '+l[:200]) for i,l in enumerate(t,1) if re.search(r'FLEET|fleet|sibling|\\.\\./|/home/vgpnk|regression|--shared|alternates|objects', l)][:0] if False else None; hits=[(i,l) for i,l in enumerate(t,1) if re.search(r'FLEET|fleet|sibling|/home/vgpnk|alternates|objects|shared', l)]; print('hits', len(hits)); [print(str(i)+': '+l[:200]) for i,l in hits[:60]]",
        "python3 -c import re; t=open('corpus/lessons/round-24.md', encoding='utf-8').read().splitlines(); print('errata letters', sorted(set(m.group(1) for l in t for m in re.finditer(r'Errat(?:um|a) ([A-Z])\\b', l)))); print([(i+1, l[:140]) for i,l in enumerate(t) if re.search(r'Erratum [A-Z]\\b', l)][:30])",
        "python3 -c import subprocess; cmds=[['python3','tools/wave-route-mix.py','--spec','.ufo/waves/round-21/spec1.json','--json'],['python3','tools/wave-accounting.py','--bundle','.ufo/evidence/round-22/bundle.json','--expected','.ufo/evidence/round-22/expected.json','--json'],['python3','tools/wave-accounting.py','--bundle','.ufo/evidence/round-22/wrong-count-bundle.json','--expected','.ufo/evidence/round-22/wrong-count-expected.json','--json']]; [print(' '.join(c[1:]), '-> exit', subprocess.run(c, capture_output=True, text=True).returncode) for c in cmds]",
        "grep -n -E bwrap|def run_row|retain_streams|Superseded rows still execute|ROOT\\.parent|BWRAP_UNAVAILABLE tools/env-diff.py tools/registry-check.py tools/round21-measure.py .ufo/evidence/round-23/replay.py",
        "grep -n -E 62/62|QUALITY45|QUALITY48|47/47 corpus/lessons/round-21.md corpus/lessons/round-22.md corpus/lessons/round-23.md corpus/lessons/round-24.md corpus/lessons/round-24-verifier-spotcheck.md corpus/QUALITY.md",
        "python3 tools/registry-check.py --root /tmp/Read37-gA12/fleet/tameshi-shokunin --tag new-r24 --json",
        "python3 tools/registry-check.py --root /tmp/Read37-gA12/fleet/tameshi-shokunin --only command-binding-selftest --json",
        "git --no-pager -C /tmp/Read37-gA12/fleet/tameshi-shokunin diff --stat 33d03b7 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 -- .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/c2-count.py .ufo/evidence/round-21/c1-mutants.json .ufo/evidence/round-21/c2-contract.json tools/round21-measure.py",
        "python3 -c import json; m=json.load(open('.ufo/evidence/round-21/c1-mutants.json', encoding='utf-8')); print('mutants', len(m['mutants'])); [print(x['id'], x['path'], repr(x['old'][:90]), '->', repr(x['new'][:90])) for x in m['mutants']]",
        "sha256sum .ufo/evidence/round-21/coldread/measure.py tools/registry.json corpus/SOURCES.md corpus/lessons/round-21.md corpus/knowledge/hermetic-env-differential.md corpus/knowledge/callback-authoritative-accounting.md corpus/knowledge/required-command-binding.md corpus/knowledge/replay-projection-hardening.md corpus/lessons/round-24.md .ufo/evidence/round-21/c2-contract.json .ufo/evidence/round-21/f5/receipt.json .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/c2-count.py .ufo/evidence/round-22/bundle.json .ufo/evidence/round-22/expected.json .ufo/evidence/round-22/wrong-count-bundle.json .ufo/evidence/round-22/wrong-count-expected.json .ufo/evidence/round-23/replay/bundle.json .ufo/evidence/round-23/replay/expected.json .ufo/evidence/round-23/source-read-bundle.json .ufo/evidence/round-23/source-read-expected.json .ufo/evidence/round-23/extra-cases.json .ufo/evidence/round-24/extra-cases.json .ufo/evidence/round-22/measure.py .ufo/evidence/round-22/accounting-extra-cases.json .ufo/waves/round-21/spec1.json .ufo/evidence/round-23/measure.py .ufo/evidence/round-23/replay.py .ufo/evidence/round-24/measure.py .ufo/evidence/round-18/measure.py .ufo/evidence/round-21/routemix-r20-spec1.exit .ufo/evidence/round-21/routemix-r20-spec1.stderr .ufo/evidence/round-21/c1-mutants.json tools/mutate-and-run.sh corpus/lessons/round-22.md corpus/lessons/round-23.md corpus/lessons/round-24-verifier-spotcheck.md corpus/QUALITY.md /home/vgpnk/.omp/agent/config.yml",
        "python3 -c import re; t=open('corpus/lessons/round-21.md', encoding='utf-8').read().splitlines(); print([(i+1, l[:220]) for i,l in enumerate(t) if '199-entry' in l or 'accepts the round21' in l or '28/71' in l])",
        "python3 -c import json; t=open('/tmp/Read37-gA12/Read37-report.md', encoding='utf-8').read(); f=chr(96)*3; print('json fences', t.count(f+'json'), 'fence total', t.count(f)); d=json.loads(t.split(f+'json')[1].split(f)[0]); s=d['sections'][0]; print(d['schema'], s['verdict'], len(s['traces']), len(s['commands_executed']), len(s['inputs']), len(s['opened'])); print(repr(t.rstrip().splitlines()[-1]))"
      ],
      "opened": [
        "tools/trace-inputs.py",
        "tools/registry-check.py",
        "tools/env-diff.py",
        "tools/round21-measure.py",
        "tools/wave-accounting.py",
        "tools/command-binding.py",
        "tools/registry-replay.py",
        "tools/wave-route-mix.py",
        "tools/registry.json",
        "tools/mutate-and-run.sh",
        "corpus/SOURCES.md",
        "corpus/lessons/round-21.md",
        "corpus/lessons/round-22.md",
        "corpus/lessons/round-23.md",
        "corpus/lessons/round-24.md",
        "corpus/lessons/round-24-verifier-spotcheck.md",
        "corpus/QUALITY.md",
        "corpus/knowledge/hermetic-env-differential.md",
        "corpus/knowledge/callback-authoritative-accounting.md",
        "corpus/knowledge/required-command-binding.md",
        "corpus/knowledge/replay-projection-hardening.md",
        ".ufo/evidence/round-21/coldread/measure.py",
        ".ufo/evidence/round-21/c1-survivors.py",
        ".ufo/evidence/round-21/c2-count.py",
        ".ufo/evidence/round-21/c1-mutants.json",
        ".ufo/evidence/round-21/c2-contract.json",
        ".ufo/evidence/round-21/f5/receipt.json",
        ".ufo/evidence/round-21/routemix-r20-spec1.exit",
        ".ufo/evidence/round-21/routemix-r20-spec1.stderr",
        ".ufo/waves/round-21/spec1.json",
        ".ufo/evidence/round-22/bundle.json",
        ".ufo/evidence/round-22/expected.json",
        ".ufo/evidence/round-22/wrong-count-bundle.json",
        ".ufo/evidence/round-22/wrong-count-expected.json",
        ".ufo/evidence/round-22/measure.py",
        ".ufo/evidence/round-22/accounting-extra-cases.json",
        ".ufo/evidence/round-23/replay/bundle.json",
        ".ufo/evidence/round-23/replay/expected.json",
        ".ufo/evidence/round-23/source-read-bundle.json",
        ".ufo/evidence/round-23/source-read-expected.json",
        ".ufo/evidence/round-23/extra-cases.json",
        ".ufo/evidence/round-23/measure.py",
        ".ufo/evidence/round-23/replay.py",
        ".ufo/evidence/round-24/extra-cases.json",
        ".ufo/evidence/round-24/measure.py",
        ".ufo/evidence/round-18/measure.py"
      ],
      "inputs": {
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
        "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
        "tools/round21-measure.py": "eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d",
        "tools/wave-accounting.py": "96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e",
        "tools/command-binding.py": "9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d",
        "tools/registry-replay.py": "9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714",
        "tools/wave-route-mix.py": "1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782",
        "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a",
        "corpus/lessons/round-21.md": "35444ddc32116089f87733c8f0a635dc7b452407d2bd0f47de483e8aacfb1a7d",
        "corpus/lessons/round-22.md": "47fe282169e3bb142a348ba6cc79bc4ee029d59ed5168928c9929d5a8a35b553",
        "corpus/lessons/round-23.md": "07fdc1a037ad84e4ecfcd053d86547cfb35879b3883299e18c58e35e30fbb932",
        "corpus/lessons/round-24.md": "29fd3e00a79242536bc259f6d56d6473e5e0d1e5bf451413c061fb6094b7d7a6",
        "corpus/lessons/round-24-verifier-spotcheck.md": "640db921c53a8639071fc74dde9bc42def13167e0f28b6bef39688bddd1a0ee5",
        "corpus/QUALITY.md": "b4ce6c9091f99b854151035a4949af4a03850a08e937a8ccdd0de1c0c4c047a8",
        "corpus/knowledge/hermetic-env-differential.md": "90756351093e2273257ce6a738bb90b6923865bc22d9276ba2cf8aeafb262e7e",
        "corpus/knowledge/callback-authoritative-accounting.md": "ddf13b0835a5e6c21c308ab87ec24c9d8eee8bb8af3b3b254d73b554e9cf6035",
        "corpus/knowledge/required-command-binding.md": "2e72f8a04017b6d16e67ebd8e9e8bdb5d45b70701030a3f5466b187369ab4fd6",
        "corpus/knowledge/replay-projection-hardening.md": "7602943988d8c7a2ce566b810b28d98c01938c565244be2503bee295d76520f4",
        ".ufo/evidence/round-21/coldread/measure.py": "657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb",
        ".ufo/evidence/round-21/c1-survivors.py": "a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396",
        ".ufo/evidence/round-21/c2-count.py": "9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2",
        ".ufo/evidence/round-21/c1-mutants.json": "670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c",
        ".ufo/evidence/round-21/c2-contract.json": "5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd",
        ".ufo/evidence/round-21/f5/receipt.json": "9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264",
        ".ufo/evidence/round-21/routemix-r20-spec1.exit": "cf205dbb8cea84897b488abcc281bf96698d5e94b1096b16657b4caba9082a22",
        ".ufo/evidence/round-21/routemix-r20-spec1.stderr": "88e99fc2d6ad8560d28248ea0717076ca0620e07184d52261b2483ccae6494c5",
        ".ufo/waves/round-21/spec1.json": "f78fe7472ed8243d46e23ca29f1bff34e646ff47832093fee815f858c22317af",
        ".ufo/evidence/round-22/bundle.json": "dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e",
        ".ufo/evidence/round-22/expected.json": "e35a5934afa0ace85aeba5e687c8e12b7c7c2258af9cd00d76c13f8c0975457d",
        ".ufo/evidence/round-22/wrong-count-bundle.json": "d984c49c57d2b12b3a4e2583cc33842af6927f0612b3b0d663acb2ca09a7a17e",
        ".ufo/evidence/round-22/wrong-count-expected.json": "caf7d29e0fea8e8492152d3798201069452019928d6dd58ba052d98e6d0ad0ec",
        ".ufo/evidence/round-22/measure.py": "f833d067afd3ca17b8534fc942d6e8ed529edd3d55476802c18ea631c0678056",
        ".ufo/evidence/round-22/accounting-extra-cases.json": "e60807f2154164638b13709af930760d0f16c2c8c4a2dee7297a490c5338a41f",
        ".ufo/evidence/round-23/replay/bundle.json": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9",
        ".ufo/evidence/round-23/replay/expected.json": "0831c9c820488dc9d9096c90aade44217b6b615501fae7810e6fce414cb2a0a1",
        ".ufo/evidence/round-23/source-read-bundle.json": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf",
        ".ufo/evidence/round-23/source-read-expected.json": "70f357e354c4badb22f974070ccf37dfda512103c3cf3ab93297a3ea27cb5dc8",
        ".ufo/evidence/round-23/extra-cases.json": "87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00",
        ".ufo/evidence/round-23/measure.py": "812749631090393b5fd08e102cae01708819487994806bff45670aad0f5e3939",
        ".ufo/evidence/round-23/replay.py": "adb4171652f954d460c5e0c86d8baa4fcfa2f7fdd0b87791995afb601ae22c11",
        ".ufo/evidence/round-24/extra-cases.json": "6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35",
        ".ufo/evidence/round-24/measure.py": "0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64",
        ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37"
      },
      "external_inputs": {
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:.ufo/evidence/round-21/coldread/ledger.json": "1bd763a5899b28fa4515aaeb0e46ef206335620b97cc955cecce41ddfc697b21",
        "/home/vgpnk/.omp/agent/config.yml": "887fbbb305e815cd02c2be3e39cc73cd56971eb9199055fb452e7eda1ff1484e"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-13.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-16.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-17.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-18.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-19.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-20.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-21.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-22.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-23.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-24.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-25.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-26.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-27.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-28.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-29.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-31.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-32.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-33.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-34.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-35.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-36.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-37.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-38.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-39.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-40.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read37-41.json"
      ]
    }
  ]
}
```

Plain-English note: I read the section and classed it as a record. I traced the cited tools, fixtures, lessons and knowledge notes at 2227d83, and ran the selftests and frozen-bundle gates that are safe in a clone. I also ran the new-r24 rows and the superseded row, and checked the route-mix entry, the round-21 instrument history and the C1 mutant list. One expectation fails: the 47-row count. The other gaps are wording, citation and prerequisite issues.

COLDREAD Read37: wrong-expectation
