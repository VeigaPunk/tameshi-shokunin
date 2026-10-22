# Read28: cold read of "## Effective expectation reconciliation — round 14"

**Verdict: gap-minor** (class: instruction). This is a recommendation for the L1 to integrate, not an admission.

Scope: SKILL.md lines 1563–1596 at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95. The next heading, `### Round-14 historical registry`, sits at line 1597. Work clone: /tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin, detached at the read revision. Every command ran under `tools/trace-inputs.py`; receipts are `.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-1.json` through `-23.json`.

## Evidence

Recipe, live tree (SKILL.md:1581–1582; claim holds):
- `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`, run in the clone: exit 2, `expected_input_digest_mismatch` (Read28-2). The same holds for `dispositions-before.json` (Read28-3).

Recipe step 2, replay in an extracted `git archive 28aeef4` tree (SKILL.md:1583–1584; claim holds):
- `dispositions-before.json`: exit 1, status failed, finding `expected_contains_missing` on `producer_before` (Read28-5). That is the named failing assertion, not a bare exit 1.

Recipe step 3 (SKILL.md:1585–1586; claim holds):
- `dispositions.json` in the same tree: exit 0, status clean, effective 11, superseded 1, no findings (Read28-6).
- Structural diff of the two manifests: top-level keys and `inputs` are equal. Only the `producer_before` row differs, from effective to superseded, with reason, raw_receipt, raw_check and superseded_by added. The other 11 rows are identical (Read28-18). This supports "the only repair is that row's explicit supersession".
- The raw observation is retained (`raw_retained` true), and both replacements pass: `producer_before_oracle` exit 1 against expected 1, `producer_after_oracle` exit 0 against expected 0 (Read28-6).

Step 1 counts (SKILL.md:1580):
- Each manifest has 12 rows (Read28-5, Read28-6, Read28-18).
- The 13 pinned inputs are the `inputs` of `.ufo/evidence/round-13/expected.json` (`expected_inputs_verified`, Read28-5). See G3.

Step 4 (SKILL.md:1587–1589; claim holds):
- `verification-final.json`: `disposition_selftest` PASS 34/34, `unresolved_before` exit 1, `resolved_after` exit 0 (Read28-11).
- `verification.json`: `disposition_selftest` prints `SELFTEST: FAIL (18/34 failed: …)` (Read28-11). This matches "initial18-of34 fixture failures".

Step 5 (SKILL.md:1592–1595; claim holds):
- `.ufo/evidence/round-14/capture-context.py` sets OUTPUT_REL to `.ufo/evidence/round-14/context-receipt.json` at line 58, and `write_receipt` replaces that file with `os.replace` at lines 583–602. I did not run the script, as the section directs.
- The maintained gate named at 1595 is `tools/context-capture.py`, listed in the round-15 registry (heading at line 1676, row at line 1680). `python3 tools/context-capture.py --check` prints `CONTEXT: OK (id=context_consistent … exit=0)` (Read28-17). The tool is present (Read28-15).

Pointers:
- "Live-tree form: the round-17 re-pin section" (1586) resolves to `## Live-tree re-pin and entry-command monitor — round 17` at line 1814. Its round-18 recipe works: `dispositions-before.json` gives exit 1 and `dispositions.json` gives exit 0 clean (Read28-21, Read28-22).

Table rows and sources:
- Row 1 (FileNotFoundError is a setup failure) matches the reason text in the superseded `producer_before` row (manifest text in Read28-1 and Read28-6).
- Row 3 (digest mismatch is could-not-evaluate) holds: exit 2 at head (Read28-2, Read28-3).
- S049 appears at `corpus/SOURCES.md:58` and `:256` ("round-14 Python child-environment contract"). S003 §Limitations appears at `:14`. Both check out (Read28-8).
- `corpus/knowledge/incremental-pin-disposition.md:314` is section 8, "Empirical correction and backlink — round 14" (Read28-8).
- `corpus/lessons/round-13-verifier-spotcheck.md:179–181` holds routed defects 1–3 (Read28-8; read by hand at 174–182).

Runner identity and history:
- `75ed934d…` is the sha256 of `tools/mutate-and-run.sh` at 28aeef4 (Read28-13). It appears once in `.ufo/evidence/round-13/expected.json` (Read28-11).
- `mutate-and-run.sh` was pinned at commit 606716f (round 10). Round-16 commits c699c8c3 and 05a22475 changed it. Later changes came in 2a22adeb (round 17), 58e5d53d (round 18) and a08e85c5 (round 26, HEAD fb91ef76) (Read28-16, Read28-23).
- `bash-witness-study.py` was pinned at 4acc607 (round 13, 49e9e5e2). It changed in 58e5d53d (round 18) and 370f2dff (round 21, now 60575e62) (Read28-16, Read28-23).

## Minor gaps (ordered by how likely they are to mislead)

- G2: The recipe header at SKILL.md:1578 says "Recipe, from this lane root:". Steps 2–3 need the cwd to be an extracted 28aeef4 tree. Run from the lane root, the same command exits 2 (Read28-2, Read28-3), not 1 or 0.
- G5: The parenthetical "(the runner moved in round 16)" at SKILL.md:1582 is accurate for `tools/mutate-and-run.sh`. But the gate prints the first mismatch in sorted order, which is `tools/bash-witness-study.py` (observed 60575e62…, pinned 49e9e5e2…). That file moved in rounds 18 and 21. The gate stops at that first mismatch (`tools/evidence-disposition.py:1633–1644`), so the runner is never named. It is also stale at head (fb91ef76…, pinned 75ed934d…; Read28-12).
- G1: Step 2 gives no extraction command (SKILL.md:1582–1583). I used `git archive 28aeef4 | tar -x -C DIR` (Read28-4), and the replays then matched.
- G4: "runner `75ed934d…`" (SKILL.md:1581) is a hash prefix with no path. It is `tools/mutate-and-run.sh`.
- G6: The anchor is not explained. Commit 28aeef4 is titled "round-15 verifier spot-check" (Read28-19). The last round-14 commit that touches the manifests or the disposition tool before it is 4d409d7 (Read28-20). The replays work at 28aeef4, but the section gives no reason for that commit.
- G3: "thirteen pinned inputs" (SKILL.md:1580) is undefined. The 13 are the inputs of `expected.json`. Each disposition manifest pins only three inputs (Read28-5, Read28-6).
- G7: "correction8" (SKILL.md:1567) is shorthand for section 8 of `corpus/knowledge/incremental-pin-disposition.md`.
- G8: "The revision measured is recorded separately" (SKILL.md:1590) gives no location. The commits sit in each file's `measured_commit` field: verification.json `0c6e36d0bd2fd98077de4cff4c90c6f467c2e1fb`, verification-final.json `64314783836bb0d05ad06a774d7310fd3a23b5bd` (Read28-7).

No blocking gaps. No wrong expectations.

## Smallest safe correction

1. Header at line 1578 and step 2 (1581–1584): say that steps 2–3 run with cwd set to an extracted `git archive 28aeef4` tree (`git archive 28aeef4 | tar -x -C DIR`, then `cd DIR`). Drop "from this lane root" for those steps.
2. Step 2 (1581–1582): name the runner as `tools/mutate-and-run.sh` with its full sha256. Add that the gate stops at the first mismatch in sorted order. At head that is `tools/bash-witness-study.py`, while the runner is also stale.
3. Step 2 anchor: add one clause giving the reason for 28aeef4, and cite 4d409d7 as the last round-14 change before it. The lane text I read does not supply the reason, so the author must.
4. Step 1 (line 1580): write "thirteen pinned inputs (the `inputs` of `.ufo/evidence/round-13/expected.json`)".
5. Line 1567: change "correction8" to "§8 of `corpus/knowledge/incremental-pin-disposition.md`".
6. Line 1590: name the `measured_commit` field of each verification file.

## Residual risk and verification gaps

- Not checked against artifacts: table rows at lines 1575–1576 (policy wording for context experiments and GIT_DIR injection), and the closing rule at line 1591. I cross-read them only against the round-15 text.
- Not run, on purpose: `capture-context.py` (the section forbids it), the raw round-13 producers, and any sibling gate.
- At head, both manifests fail closed with exit 2 by design. The recipe passes at head only through the round-18 form. That is the section's own statement, not a defect.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "TameshiR27.Read28",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 1563,
      "heading": "## Effective expectation reconciliation — round 14",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "G2: the recipe header at SKILL.md:1578 says 'Recipe, from this lane root:', but steps 2-3 (SKILL.md:1581-1586) need cwd set to an extracted git archive 28aeef4 tree. The same command run from the lane root exits 2 (Read28-2, Read28-3), not 1 or 0.",
        "G5: the parenthetical '(the runner moved in round 16)' at SKILL.md:1582 is accurate for tools/mutate-and-run.sh (round-16 commits c699c8c3 and 05a22475 changed it after its pin; Read28-16, Read28-23). The gate prints the first mismatch in sorted order, tools/bash-witness-study.py (observed 60575e62..., pinned 49e9e5e2...; Read28-2), which moved in rounds 18 and 21. The gate raises on that first mismatch (tools/evidence-disposition.py:1633-1644), so the runner is never named. The runner is also stale at head (fb91ef76..., pinned 75ed934d...; Read28-12).",
        "G1: step 2 gives no extraction command for the 28aeef4 tree (SKILL.md:1582-1583). Read28-4 used git archive 28aeef4 | tar -x -C DIR, and the replays then matched (Read28-5, Read28-6).",
        "G4: 'runner 75ed934d...' (SKILL.md:1581) is a hash prefix with no path. It is the sha256 of tools/mutate-and-run.sh at 28aeef4 (Read28-13) and appears once in .ufo/evidence/round-13/expected.json (Read28-11).",
        "G6: the anchor 28aeef4 is not explained (SKILL.md:1582-1583). Its subject is 'round-15 verifier spot-check' (Read28-19). The last round-14 commit touching the round-14 manifests or the disposition tool before it is 4d409d7 (Read28-20; 6431478 and 0c6e36d are older). The replays work at 28aeef4 (Read28-5, Read28-6), but no reason for that commit is given.",
        "G3: 'thirteen pinned inputs' (SKILL.md:1580) is undefined. The 13 are the inputs of .ufo/evidence/round-13/expected.json (expected_inputs_verified, Read28-5). Each disposition manifest pins only three inputs (inputs_verified; Read28-5, Read28-6).",
        "G7: 'correction8' (SKILL.md:1567) is shorthand for section 8 of corpus/knowledge/incremental-pin-disposition.md (line 314, 'Empirical correction and backlink — round 14'; Read28-8).",
        "G8: 'The revision measured is recorded separately' (SKILL.md:1590) names no location. The commits sit in measured_commit fields: verification.json 0c6e36d0bd2fd98077de4cff4c90c6f467c2e1fb and verification-final.json 64314783836bb0d05ad06a774d7310fd3a23b5bd (Read28-7)."
      ],
      "commands_executed": [
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-14/dispositions.json",
        "[cwd=/tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin] python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json",
        "[cwd=/tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin] python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json",
        "sh -c mkdir -p /tmp/TameshiR27-Read28-L6CK/arch28 && git -C /tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin archive 28aeef4 | tar -x -C /tmp/TameshiR27-Read28-L6CK/arch28",
        "[cwd=/tmp/TameshiR27-Read28-L6CK/arch28] python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json",
        "[cwd=/tmp/TameshiR27-Read28-L6CK/arch28] python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json",
        "python3 -c import json,sys\nfor p in sys.argv[1:]:\n    raw=open(p,encoding='utf-8').read()\n    print('==', p, len(raw), 'bytes')\n    try:\n        d=json.loads(raw)\n    except Exception as e:\n        print('not json', e); print(raw[:1500]); continue\n    if isinstance(d,dict):\n        print('top keys:', list(d.keys()))\n        for k,v in d.items():\n            s=json.dumps(v)\n            print('  ', k, ':', s[:400])\n    else:\n        print(type(d).__name__)\n .ufo/evidence/round-13/expected.json .ufo/evidence/round-14/verification-final.json .ufo/evidence/round-14/verification.json",
        "python3 -c import re,sys\npats=[r'S049',r'S003',r'Limitations',r'[Cc]orrection ?8',r'[Rr]outed defects',r'[Pp]ython child',r'[Ee]mpirical']\nfor p in sys.argv[1:]:\n    lines=open(p,encoding='utf-8').read().splitlines()\n    print('==', p, len(lines), 'lines')\n    for n,l in enumerate(lines,1):\n        if any(re.search(x,l) for x in pats): print(p+':'+str(n)+': '+l[:400])\n corpus/SOURCES.md corpus/knowledge/incremental-pin-disposition.md corpus/lessons/round-13-verifier-spotcheck.md",
        "python3 -c import re,sys\np='.ufo/evidence/round-14/capture-context.py'\nlines=open(p,encoding='utf-8').read().splitlines()\nprint('==', p, len(lines), 'lines')\nfor n,l in enumerate(lines,1):\n    if re.search(r'receipt|OUT|out_path|--out|argv|default', l): print(str(n)+': '+l[:300])\n",
        "git -C /tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin rev-parse --verify --quiet 75ed934d",
        "python3 -c import json,re\nfiles=['.ufo/evidence/round-13/expected.json','.ufo/evidence/round-14/verification.json','.ufo/evidence/round-14/verification-final.json','.ufo/evidence/round-14/dispositions-before.json','.ufo/evidence/round-14/dispositions.json','.ufo/evidence/round-14/capture-context.py']\nfor p in files:\n    raw=open(p,encoding='utf-8').read()\n    print('75ed934d occurrences in', p, len(re.findall('75ed934d', raw)))\nfor p in files[1:3]:\n    d=json.loads(open(p,encoding='utf-8').read())\n    print('==', p, 'input_sha256:')\n    for k,v in d['input_sha256'].items():\n        print('   ', k, v)\n    print('==', p, 'checks:')\n    for c in d['checks']:\n        out=c.get('stdout','') or ''\n        print('   ', c.get('name'), 'exit', c.get('exit'), 'expected_exit', c.get('expected_exit'), 'PASS', out.count('PASS'), 'FAIL', out.count('FAIL'))\nd=json.loads(open(files[1],encoding='utf-8').read())\nfor c in d['checks']:\n    if c.get('name')=='disposition_selftest':\n        print('--- verification.json disposition_selftest stdout (last 1500) ---')\n        print((c.get('stdout') or '')[-1500:])\nd=json.loads(open(files[2],encoding='utf-8').read())\nfor c in d['checks']:\n    if c.get('name')=='disposition_selftest':\n        print('--- verification-final.json disposition_selftest stdout (last 800) ---')\n        print((c.get('stdout') or '')[-800:])\n",
        "sh -c sha256sum tools/mutate-and-run.sh tools/bash-witness-study.py tools/evidence-disposition.py tools/trace-inputs.py",
        "python3 -c import hashlib,subprocess,sys\nR=sys.argv[1]; W=sys.argv[2]; paths=sys.argv[3:]\nfull=subprocess.run(['git','-C',R,'rev-parse','--verify','28aeef4^{commit}'],capture_output=True,text=True).stdout.strip()\nprint('commit', full)\nfor p in paths:\n    data=subprocess.run(['git','-C',R,'show',full+':'+p],capture_output=True).stdout\n    arch=open(W+'/arch28/'+p,'rb').read()\n    g=hashlib.sha256(data).hexdigest(); a=hashlib.sha256(arch).hexdigest()\n    print(p, 'git_show_sha256', g, 'archive_sha256', a, 'equal' if g==a else 'DIFFERENT', len(data))\n /tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin /tmp/TameshiR27-Read28-L6CK tools/evidence-disposition.py .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-14/dispositions.json .ufo/evidence/round-13/expected.json .ufo/evidence/round-13/verification.json .ufo/evidence/round-13/producer-oracle-repair.json .ufo/evidence/round-12/BashWitness/declaration.json .ufo/evidence/round-12/BashWitness/declared.tsv .ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json .ufo/evidence/round-12/BashWitness/summary.json .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/producer-before.py .ufo/evidence/round-13/producer-oracle.py .ufo/evidence/round-13/witness-metadata-old-null.json .ufo/evidence/round-13/witness-metadata.json tools/bash-witness-study.py tools/mutate-and-run.sh tools/pin-disposition.py tools/witness-metadata.py",
        "git -C /tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin log --format=%h%x20%ad%x20%s --date=short -- tools/bash-witness-study.py tools/mutate-and-run.sh",
        "python3 -c import os;print(sorted(os.listdir('tools')));print('context-capture present:', os.path.exists('tools/context-capture.py'))",
        "python3 -c import hashlib,subprocess,sys\nR=sys.argv[1]\ndef git(*a):\n    return subprocess.run(['git','-C',R]+list(a),capture_output=True,text=True).stdout\ndef sha_at(c,p):\n    data=subprocess.run(['git','-C',R,'show',c+':'+p],capture_output=True).stdout\n    return hashlib.sha256(data).hexdigest()[:8]\nfor p in ['tools/mutate-and-run.sh','tools/bash-witness-study.py']:\n    print('== history of', p)\n    for c in git('log','--format=%H','--reverse','--',p).split():\n        print(c[:8], sha_at(c,p), git('log','-1','--format=%ad %s','--date=short',c).strip()[:150])\nprint('HEAD', p, sha_at('HEAD','tools/bash-witness-study.py'), sha_at('HEAD','tools/mutate-and-run.sh'))\nprint('28aeef4 is ancestor of HEAD:', subprocess.run(['git','-C',R,'merge-base','--is-ancestor','28aeef4','HEAD']).returncode==0)\n /tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin",
        "python3 tools/context-capture.py --check",
        "python3 -c import json\na=json.load(open('.ufo/evidence/round-14/dispositions-before.json',encoding='utf-8'))\nb=json.load(open('.ufo/evidence/round-14/dispositions.json',encoding='utf-8'))\nprint('top-level keys equal:', sorted(a)==sorted(b))\nfor k in sorted(set(a)|set(b)):\n    if k=='rows':\n        continue\n    print(k, 'equal' if a.get(k)==b.get(k) else 'DIFFERENT')\nprint('row name order equal:', [r['name'] for r in a['rows']]==[r['name'] for r in b['rows']], len(a['rows']), len(b['rows']))\nra={r['name']:r for r in a['rows']}; rb={r['name']:r for r in b['rows']}\nfor n in ra:\n    if ra[n]!=rb.get(n):\n        print('row differs:', n, 'before', ra[n].get('state'), 'after', rb[n].get('state'), 'after keys', sorted(rb[n].keys()))\nprint('rows identical other than differing ones:', sum(1 for n in ra if ra[n]==rb.get(n)))\n",
        "sh -c sha256sum SKILL.md && wc -l SKILL.md tools/trace-inputs.py tools/evidence-disposition.py corpus/SOURCES.md corpus/knowledge/incremental-pin-disposition.md corpus/lessons/round-13-verifier-spotcheck.md && git rev-parse HEAD && git cat-file -t 28aeef4 && git log --oneline -1 28aeef4 && ls -la .ufo/evidence/round-14",
        "git -C /tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin log --format=%h%x20%ad%x20%s --date=short -n 3 28aeef4 -- .ufo/evidence/round-14/dispositions.json .ufo/evidence/round-14/verification-final.json tools/evidence-disposition.py",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
        "python3 -c import hashlib,subprocess,sys\nR=sys.argv[1]\nfor p in ['tools/mutate-and-run.sh','tools/bash-witness-study.py']:\n    out=subprocess.run(['git','-C',R,'log','--format=%H','--reverse','--',p],capture_output=True,text=True).stdout.split()\n    for c in out:\n        data=subprocess.run(['git','-C',R,'show',c+':'+p],capture_output=True).stdout\n        print(p, c, hashlib.sha256(data).hexdigest())\n /tmp/TameshiR27-Read28-L6CK/fleet/tameshi-shokunin"
      ],
      "opened": [
        "SKILL.md",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/producer-before.py",
        ".ufo/evidence/round-13/producer-oracle-repair.json",
        ".ufo/evidence/round-13/producer-oracle.py",
        ".ufo/evidence/round-13/verification.json",
        ".ufo/evidence/round-13/witness-metadata-old-null.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-14/capture-context.py",
        ".ufo/evidence/round-14/context-receipt.json",
        ".ufo/evidence/round-14/dispositions-before.json",
        ".ufo/evidence/round-14/dispositions.json",
        ".ufo/evidence/round-14/verification-final.json",
        ".ufo/evidence/round-14/verification.json",
        ".ufo/evidence/round-18/dispositions-before.json",
        ".ufo/evidence/round-18/dispositions.json",
        "corpus/SOURCES.md",
        "corpus/knowledge/incremental-pin-disposition.md",
        "corpus/lessons/round-13-verifier-spotcheck.md",
        "tools/bash-witness-study.py",
        "tools/context-capture.py",
        "tools/evidence-disposition.py",
        "tools/mutate-and-run.sh",
        "tools/pin-disposition.py",
        "tools/trace-inputs.py",
        "tools/witness-metadata.py"
      ],
      "inputs": {
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
        ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
        ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
        ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
        ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89",
        ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
        ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
        ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
        ".ufo/evidence/round-14/verification-final.json": "e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2",
        ".ufo/evidence/round-14/verification.json": "1d480a0ddd0cd8a801d0ae38f7d774b6d772c8d0910bf6200c3e666696532939",
        ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
        ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
        "corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a",
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420",
        "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
        "tools/context-capture.py": "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726",
        "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
      },
      "external_inputs": {
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/evidence-disposition.py": "1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/bash-witness-study.py": "49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/pin-disposition.py": "297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
        "tameshi-shokunin@4acc607dfd79f19d508bd50cdd06b77269fccd1d:tools/bash-witness-study.py": "49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80",
        "tameshi-shokunin@4acc607dfd79f19d508bd50cdd06b77269fccd1d:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
        "tameshi-shokunin@4acc607dfd79f19d508bd50cdd06b77269fccd1d:tools/pin-disposition.py": "297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11",
        "tameshi-shokunin@53e74a890c70fdcb97487eadb67c2e36faf7bb7b:tools/mutate-and-run.sh": "d8abee522efbf27c3570acd68d7bc4b9dd30a3888f6e9c2359020e179a7eda68",
        "tameshi-shokunin@b58b26fbeba8fd972e1d31ac8a9175a81e333b32:tools/mutate-and-run.sh": "597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b",
        "tameshi-shokunin@44947154c23772f766f9f5439090fb5c7ad76e46:tools/mutate-and-run.sh": "b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb",
        "tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75",
        "tameshi-shokunin@606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
        "tameshi-shokunin@c699c8c36d6e4eca4b796b81a8247904aa145ec8:tools/mutate-and-run.sh": "89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594",
        "tameshi-shokunin@05a224754db3c6fce18f5ec1816a6873bffe3d0e:tools/mutate-and-run.sh": "0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa",
        "tameshi-shokunin@2a22adeb7d1de5e7189e62ce41ac679d71a97b44:tools/mutate-and-run.sh": "fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a",
        "tameshi-shokunin@58e5d53d6a638fb72042d1f6607b24018aa299a8:tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b",
        "tameshi-shokunin@a08e85c5d7f899e8a5992e20517edb1a380d79eb:tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tameshi-shokunin@9df9212d33dc2dbda133e88f28ad47bb08839a5b:tools/bash-witness-study.py": "249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a",
        "tameshi-shokunin@58e5d53d6a638fb72042d1f6607b24018aa299a8:tools/bash-witness-study.py": "8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12",
        "tameshi-shokunin@370f2dffe66f00c3c7412c962bf3e8fcbe75dfdb:tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-13.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-16.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-17.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-18.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-19.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-20.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-21.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-22.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/TameshiR27.Read28-23.json"
      ]
    }
  ]
}
```

Checked, as a cold reader would: I cloned the lane at the read revision, detached, into /tmp, and read the section (lines 1563–1596). I ran the recipe's gate commands under the collector, both at the clone root and in an extracted `git archive 28aeef4` tree. The exit codes, the failing `producer_before` finding, the single differing manifest row, the 12-row and 13-input counts, the two verification files, the maintained context gate, the round-18 live-tree pointer, and each cited source line all matched what the section says. The five monitor-listed inputs (SOURCES.md, bash-witness-study.py, evidence-disposition.py, mutate-and-run.sh, trace-inputs.py) have receipt-backed hashes at this revision. Archive-tree runs used `--cwd` with `--root` still at the clone, so their reads sit under `external_inputs` as git blobs at 28aeef4. Setup: the step 1 clone and checkout ran outside the collector, as prescribed, with `GIT_OPTIONAL_LOCKS=0`. That setup call also printed HEAD and the SKILL.md sha256 outside the collector; Read28-19 re-runs those checks under the collector, and I rely only on traced output. The early `wc`, `ls` and `git cat-file` probes also ran outside the collector; their facts are re-confirmed by Read28-19 and by the reads in Read28-7 and Read28-11. SKILL.md was read with the read and grep tools, not shell commands. No tool was installed or upgraded. Scratch work lived only under /tmp (the clone, the archive tree, and symlinks to sibling repos, which I did not run anything in). Nothing else was written except this report and the 23 receipts.

COLDREAD Read28: gap-minor
