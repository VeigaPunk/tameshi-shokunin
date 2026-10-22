# Read04A: cold read of SKILL.md "### Triggers T1–T3 and the re-pin rule" (line 1069)

Read rev b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a, detached in the clone
/tmp/Read04A-cNAK/fleet/tameshi-shokunin (fleet siblings symlinked into a mirror).
SKILL.md sha256 c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6.
The section runs 1069–1091; the next heading is 1092.

Class: instruction — the three triggers tell a reader to re-measure, re-run the
reproduction and record an appended row. Verdict: executed-ok — the T1 pin-read and
the T2 regression re-run both executed and reproduced the recorded state; every
claim I could check in the record portions verified. The T3 action is a write and
was not executed (bounds); its precedent pointer (`fleet-kill-rate-ledger.md:170-173`)
resolves verbatim.

```json
{"schema":"tameshi-coldread-report-v2","seat":"Read04A","skill_sha256":"c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6","read_rev":"b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a","sections":[{"start":1069,"heading":"### Triggers T1–T3 and the re-pin rule","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["The bare filename `RerunSweep.md` resolves to .ufo/waves/round-16/w2/RerunSweep.md; a second RerunSweep.md exists at .ufo/waves/round-16/w1/ (I did not disambiguate by directory in-file, but :19-23 lands on the w2 file and the tool sha there matches `89722ddb…`)","The five-sha harness sequence `597e1419… → b56c6e57… → 4dc69ef9… → e3f838d4… → cf41efaa…` includes `4dc69ef9`/`e3f838d4`, which appear in no committed blob of tools/mutate-and-run.sh (verified by commit chain and corroborated by .ufo/waves/round-16/w1/CR18.md:82-84 and w2/Replica1021.md:33 — they were working-tree states); 'moved four times in one day' is consistent as mtime states, not committed pins","The 'rc 0' part of the round-8 replay receipt is recorded at corpus/knowledge/mutation-case-kumitate-claims.md:316-317 (19:14:16Z, rc 0), not at the cited fleet-kill-rate-ledger.md:281 which gives the same REGRESSION PASS string and timestamp but not the exit code","The T3 action 'an appended row' is a ledger write and cannot be executed by a cold read; its precedent citation (fleet-kill-rate-ledger.md:170-173) does contain the appended-row rule verbatim"],"commands_executed":["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/waves/round-16/w2/RerunSweep.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/mutation-case-kumitate-claims.md .ufo/waves/round-27/w1/Read15.md .ufo/waves/round-27/residual/ReRead07.md .ufo/waves/round-16/w1/CR18.md .ufo/waves/round-16/w2/Replica1021.md","bash -c \"sha256sum $W/fleet/tsukuroi-shokunin/tools/tsukuroi-census.sh $W/fleet/mado-shokunin/tools/mado-verify.sh; GIT_OPTIONAL_LOCKS=0 git -C $W/fleet/tsukuroi-shokunin show HEAD:tools/tsukuroi-census.sh | sha256sum; GIT_OPTIONAL_LOCKS=0 git -C $W/fleet/mado-shokunin show HEAD:tools/mado-verify.sh | sha256sum; GIT_OPTIONAL_LOCKS=0 git -C $W/fleet/tsukuroi-shokunin status --porcelain -- tools/tsukuroi-census.sh; GIT_OPTIONAL_LOCKS=0 git -C $W/fleet/mado-shokunin status --porcelain -- tools/mado-verify.sh; echo done\"","bash tools/mutate-and-run.sh --regression --workdir /tmp/Read04A-cNAK/regression"],"opened":[".ufo/waves/round-16/w1/CR18.md",".ufo/waves/round-16/w2/Replica1021.md",".ufo/waves/round-16/w2/RerunSweep.md",".ufo/waves/round-18/staged/corpus/knowledge/fleet-kill-rate-ledger.md",".ufo/waves/round-27/residual/ReRead07.md",".ufo/waves/round-27/w1/Read15.md","corpus/knowledge/fleet-kill-rate-ledger.md","corpus/knowledge/mutation-case-kumitate-claims.md","corpus/knowledge/mutation-case-mado-verify.md","corpus/knowledge/service-optin-protocol.md","tools/mutate-and-run.sh","tools/trace-inputs.py"],"inputs":{".ufo/waves/round-16/w1/CR18.md":"cc6bfdb3da63152d393b134c9312e38444f82877b0d044ba7b2dd368ca424de5",".ufo/waves/round-16/w2/Replica1021.md":"9c7432a4017ae7c236e88962e9f5a301605b94eaa7e2c7908ec325b08e557579",".ufo/waves/round-16/w2/RerunSweep.md":"8b03036e4942ee5b5b1680c25219f0e4c006a2aa58ef4b8a01bc450df53cdbc1",".ufo/waves/round-18/staged/corpus/knowledge/fleet-kill-rate-ledger.md":"1c06c6ba1eee45dd2aed540c9d70e2e361d05d9f82acc43afe64c8964ef38611",".ufo/waves/round-27/residual/ReRead07.md":"683334bbcb3cde4e5a487105e121727c4cef68a7bf92033fbae6b706d1b9c363",".ufo/waves/round-27/w1/Read15.md":"776fb28ef4fa9fffc21a9e00b4c055b38f97919e0b07250fdf538e2c7e67a05f","corpus/knowledge/fleet-kill-rate-ledger.md":"13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e","corpus/knowledge/mutation-case-kumitate-claims.md":"3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9","corpus/knowledge/mutation-case-mado-verify.md":"f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3","corpus/knowledge/service-optin-protocol.md":"84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e","tools/mutate-and-run.sh":"fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de","tools/trace-inputs.py":"f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"},"external_inputs":{"/home/vgpnk/Projects/shokunin/mado-shokunin/.gitignore":"d949e4ef14286bcc34282c15538a4a023a6c74d436cba3dae0f5155239d8f817","/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh":"050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.gitignore":"65e9a6838b253022bd43ee70918dcf5f6d920cb9c2e80b91ccfb15e8e54ee027","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh":"d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e"},"traces":["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read04A-1.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read04A-2.json","/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read04A-3.json"]}]}
```

## What I checked

- T1's two dated examples (round 8): tsukuroi `084951be…` (6/10) → `bba6cdf6…` and
  mado `d7edaab4…` (4/10) → `90d50cdd…` match the ledger blob chains at
  fleet-kill-rate-ledger.md:301-302,337-338 — `bba6cdf6` was the recorded HEAD blob
  for tsukuroi and `90d50cdd` the committed round-7 link for mado. I re-ran the
  pin read itself (ER-3's own command set): today both gates read live
  `d17d32a3…`/`050efc72…`, still ≠ recorded pins, consistent with the section's
  dated statements and "moved again since".
- T2's precedent: `RerunSweep.md:19-23` records the tool at `89722ddb…` at commit
  c699c8c; `0673d2e5…` is the later runner (commit 05a2247, verified ancestor
  chain and sha256s of tools/mutate-and-run.sh at each commit). The mado
  SCR-T6 re-run under `b56c6e57…` (4/10, identical mutant shas) is recorded at
  service-optin-protocol.md:232, and the mado note does keep the reproduction U
  (mutation-case-mado-verify.md:17-23). The round-27 seat corrections are real:
  Read15.md (round-27 w1) flagged `0673d2e5` vs `89722ddb`, ReRead07.md (round-27
  residual) flagged "never re-cut" — both repairs are present at this revision.
- The re-pin self-anchor `(:811-812)` contains the "re-pin, never a
  re-interpretation" sentence verbatim; T3's pointer `fleet-kill-rate-ledger.md:170-173`
  contains the appended-row sentence verbatim (identical text in the corpus and
  round-18 staged copies; the corpus copy is canonical).
- The round-8 replay receipt (tool `cf41efaa…`, four legs, 19:14:16Z,
  `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`)
  matches fleet-kill-rate-ledger.md:281 and the claims note §6 (:316-317 adds rc 0).
- Executed the T2 action end to end: `bash tools/mutate-and-run.sh --regression`
  at b05d2ee (runner sha256 `fb91ef76…`) passed all nine embedded legs,
  `REGRESSION: PASS (cases=9 passed=9; ledger legs exact)`, 227.6 s — the recorded
  tables hold at their pinned blobs under today's live tool, exactly the re-pin
  rule's consequence.
- Executed the T1 action (re-measure at the live revision) per the ledger's pin
  read on the two stale cases; readings consistent with the recorded story.
- No blocking gaps, no wrong expectations; minor gaps listed in the JSON (bare
  filename ambiguity for RerunSweep.md, two non-committed pins in the harness
  chain, rc-0 pointer nuance, T3 write not executable in a cold read).
- Live lane was never read during traces (all receipts show `live_lane_reads: {}`);
  exception files were not touched. No tools installed (existing bash/git/python3/
  node sufficed).

COLDREAD Read04A: executed-ok
