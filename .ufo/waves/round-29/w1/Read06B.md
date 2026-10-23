# Read06B — cold read of `### Round-13 gate/probe registry` (SKILL.md:1548-1562) at 9f3084bc60ad56aac01e4556ef4c7653df2f65e5

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read06B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1548, "heading": "### Round-13 gate/probe registry", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [],
    "commands_executed": [
      "python3 tools/pin-disposition.py --selftest",
      "python3 tools/witness-metadata.py --selftest",
      "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
      "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/pin-disposition.py tools/witness-metadata.py .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/expected.json .ufo/evidence/round-13/witness-metadata.json",
      "python3 -c \"import re\nsrc = open('corpus/SOURCES.md').read()\nfor sid in ('S047','S048'):\n    m = re.search(r'^#+\\s*'+sid+r'\\b.*?(?=^#+\\s*\\S|\\Z)', src, re.S|re.M)\n    print('==== '+sid+' ====')\n    print(m.group(0)[:3000] if m else 'NOT FOUND')\npit = open('corpus/knowledge/incremental-pin-disposition.md').read()\nprint('==== PIT item-4 context ====')\nfor m in re.finditer(r'prioritisation|reuse skip|item 4', pit):\n    print(pit[max(0,m.start()-300):m.start()+300].replace(chr(10),' | '))\nprint('==== pin-disposition failed-arm ====')\ntool = open('tools/pin-disposition.py').read()\nfor m in re.finditer(r'exit\\(1\\)|return 1|\\\"failed\\\"|\\x27failed\\x27|1 failed', tool):\n    print(tool[max(0,m.start()-200):m.start()+200].replace(chr(10),' | '))\"",
      "python3 -c \"src = open('corpus/SOURCES.md').read()\nfor i, line in enumerate(src.splitlines(), 1):\n    if 'S047' in line or 'S048' in line or 'pitest.org' in line:\n        print(i, line[:400])\"",
      "python3 tools/witness-metadata.py",
      "python3 -c \"import hashlib\nfor p in ['tools/pin-disposition.py','tools/witness-metadata.py','.ufo/evidence/round-13/pin-manifest.json','.ufo/evidence/round-13/expected.json','.ufo/evidence/round-13/witness-metadata.json','corpus/SOURCES.md','corpus/knowledge/incremental-pin-disposition.md','SHONEN.md']:\n    print(p, hashlib.sha256(open(p,'rb').read()).hexdigest())\""
    ],
    "opened": ["tools/pin-disposition.py", "tools/witness-metadata.py", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/witness-metadata.json", "corpus/SOURCES.md", "corpus/knowledge/incremental-pin-disposition.md", "SHONEN.md"],
    "inputs": {
      "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
      "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
      ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
      ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
      ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
      "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
      "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
      "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09"
    },
    "external_inputs": {},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-5.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-6.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-7.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-8.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read06B-9.json"]}]}
```

## What I checked

Section bounds: heading at SKILL.md:1548, next heading (`## Effective expectation reconciliation — round 14`) at 1563; the section is lines 1548-1562 and contains no fenced code, so the fence rule never engages. Clone detached at the read rev; whole-page SKILL.md sha256 matched `c46ec02e…e36d6`.

Class: instruction. Both registry rows name entry commands and self-test commands; I ran all four as written, plus a bare-invocation usage probe, every run under tools/trace-inputs.py with receipts whose `rev` is the read rev.

- Row 1 ("six-leg content disposition", probe): `--selftest` printed `SELFTEST: PASS (19/19)`, exit 0; its six exit-2 cases (malformed-digest, duplicate-leg, missing-leg, malformed-json, missing-manifest, invalid-root) exercised the "2 invalid input/could-not-evaluate" arm. The entry command with `--root /home/vgpnk/Projects/shokunin` exited 0 with `status: ok`, `legs: 6, unchanged: 1, changed: 5, unavailable: 0` — the "0 observations, including changed/unavailable" arm, exactly as the verdict map folds changed/unavailable into exit 0. The tool docstring states it never writes to a target repo or worktree (read-only as the Write scope cell claims); I ran it with GIT_OPTIONAL_LOCKS=0.
- Row 2 ("exposed witness provenance companion", gate): `--selftest` printed `SELFTEST: PASS 39/39`, exit 0, with exit-1 `metadata_inconsistent` cases and exit-2 `input_unavailable`/`snapshot_tampered` cases matching the verdict map. The entry command `--check --companion .ufo/evidence/round-13/witness-metadata.json` printed `WITNESS_METADATA: metadata_consistent reason=ok exit=0` — the "0 metadata_consistent/clean" arm. Bare invocation printed the argparse usage error and the receipt records child exit 2 — the "including usage" exit-2 clause.
- Verdict-map cell "selftest 1 failed" (row 1): the only exit-1 path in tools/pin-disposition.py is the selftest-failure branch (`if failed: … return 1`); probe mode has no exit-1 arm. Read as "exit 1 = selftest failed", the cell is accurate; it is compressed phrasing, not an error.
- Closing paragraph: "six recorded cases" matches the manifest's six legs and the tool's canonical leg list ("Leg definitions are the six recorded legs only (no seventh case)"); SHONEN.md exists and no registry row touches it. "Producer SHA names the producer that actually ran, not the repaired current producer / no old evidence hash is regenerated" matches the tool's pinned literals (PRODUCER_TOOL_SHA256 for tools/bash-witness-study.py, HISTORICAL_RUNNER_SHA256 for tools/mutate-and-run.sh, `checked_live: false`, "This gate does not rewrite those bytes", `frozen_bytes_rewritten` must be false). "S048 supersedes S047's object-specific paraphrase; retain only 'item 4 is prioritisation, not a reuse skip'" is supported verbatim by corpus/SOURCES.md:57 ("supersedes S047 — item 4 is prioritisation rather than a reuse skip; no…" — S047/S048 registered at lines 56-57) and by corpus/knowledge/incremental-pin-disposition.md ("S048 supersedes S047's object-specific paraphrase… The supported operational distinction is item4 prioritisation, not a reuse skip; no pronoun referent is resolved here.").
- `.ufo/evidence/round-13/expected.json` exists at the cited path and pins the historical round-13 expectations (e.g., `pin_selftest` "SELFTEST: PASS (18/18)", `pin_live` rows 6 unchanged 3/changed 3); those are frozen historical values, and the registry only cites the file as a pinned value — today's 19/19 and 1/5 observations supersede it without contradicting the section.

No installation or tooling changes were made. Scratch clone `/tmp/Read06B-rVvx` used for all execution; live lane read only through the permitted receipt/report writes.

COLDREAD Read06B: executed-ok
