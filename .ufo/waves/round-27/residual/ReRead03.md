# ReRead03 — cold read, round-27 residual

Lane revision b1cc95e1fb62532646d74e2863770c4fed0851cc. SKILL.md sha256 fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f, checked in the pinned clone /tmp/ReRead03-Ut1W/fleet/tameshi-shokunin (detached at the pinned revision). Every path I passed to a traced command was under /tmp. The facade's own reads of the live lane are excluded and disclosed under Deviations.

## Verdicts

1. SKILL.md:668, "## Third case — cross-author confirmation (round 5, measured)": gap-minor (class record).
2. SKILL.md:1964, "### Round-21 gate/probe registry — finite environment differential": gap-blocking (class instruction). The C1 and C2 counter results rest only on receipts that must be excluded, because the facade read live-lane .git objects, and --claim c1 was not run.

Part 1 is not blocked. Part 2 is blocked by the counter's tameshi-runner pin read from the live fleet. Each has a correction below.

## Part 1 — SKILL.md:668–793 (record)

Evidence (receipts ReRead03-1, -2, -3, -20 and -35; sibling git reads are listed in external_inputs)
- Pinned census bytes. `git show 165307fe…:tools/tsukuroi-census.sh | sha256sum` gives 084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5, 44947 bytes, 977 lines. The same blob is at 9bcd1627, the last census change before the pin. This matches SKILL.md:676 and corpus/knowledge/mutation-case-tsukuroi-census.md:10–13.
- Hardened bytes. `git show da952909…` gives aae45531fc393579…07df6, 48410 bytes, 1033 lines. `git diff --numstat 165307fe da952909 -- tools/tsukuroi-census.sh` gives `56 0`. This matches SKILL.md:689 (+56 lines, 0 deletions, 26 → 35).
- Mutant sites. Lines 160, 210, 281, 434–452, 473, 487–493, 578, 615, 935 and 967 of the pinned bytes hold the text quoted in the table at SKILL.md:700–711 and in the note's manifest at :351–370 (checked by ReRead03-20).
- Replication (ReRead03-20: `python3 /tmp/ReRead03-Ut1W/scratch/mutants.py`). The ten mutants were rebuilt from the note's manifest, because the original driver is not in the lane. Control: `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`, rc 0. B1 rc 1 with 2 failing cases; B2 rc 1 with 3; B3 rc 1 with 1 (empty ring); B4 rc 1 with 1 (boot errors); B5 rc 1 with 1 (timer drift); B6 rc 1 with 21; B7, B8, B9 and B10 rc 0 with 26/26 passing (survived). KILL_RATE 6/10, with the same kill set, counts and labels as SKILL.md:700–711 and note :68–99. The hardened control prints `PASS (35 cases, 35 passed, 0 failed)`, as in note :308–310.
- In-page matrix check. Appendix B (SKILL.md:652–653): B8 2/16, B5 and B10 survive, B2 2/16, B7 1/16, B1 1/16, B3 3/16, B6 2/16, B9 2/16. This agrees with matrix rows A–G in the bash r3 column. Appendix A (SKILL.md:585–588): D2 and D10 survive, D8 has 3 failing cases, D1, D3, D6, D7 and D9 are killed, D4 and D5 are reached. This agrees with the JS column.
- Cited sources. corpus/knowledge/arm-class-matrix.md:498–525 holds the round-5 errata (E3 chmod enumeration and the companion JS 'unreached' wording). PROVINCE.md:15–16 holds the two-lane admission bar. plans/round-5.plan.md:9–10 holds the pre-registered anti-claim. The mutation-note ranges cited in the section contain the statements they support.

Smallest corrections
1. SKILL.md:693, :755 and :790: replace "revision `aae45531`" with "sha256 `aae45531…`, commit da952909". In the sibling, `git cat-file -t aae45531` fails.
2. SKILL.md:676: add "commit 165307fe" after "at measurement".
3. SKILL.md:689: write "14:06:23 -03".
4. SKILL.md:337–339: add a dated pointer to :733–738, which records the round-5 50–80 % row.
5. SKILL.md:670 and :773: point to the file that holds the "corrected round 27, seat Read07" correction, or mark it unverified.

## Part 2 — SKILL.md:1964–2085 (instruction)

Evidence (receipts ReRead03-4 to -11, -14 to -34, -36 and -37; each run at b1cc95e under the collector)
- env-diff. `--selftest` gives ENVDIFF_SELFTEST: 9/9 pass, exit 0 (-4). The entry with the frozen contract gives ENVDIFF: classified=9/9, exit 0 (-9; output to scratch). Its fresh classes are eight invariant and one nondeterministic (the js-round-gate surface, blob f890e277…). That is the pattern in the table of corpus/knowledge/hermetic-env-differential.md (read in -18).
- Round-22 wave-accounting. The entry exits 0 with finding_ids []. The selftests print 8/8 and 16/16 (-7, -11). The wrong-count pair exits 1 with TOTAL_MISMATCH, as persisted (-15). `--help` exits 0 (-28).
- Round-23 command-binding. The entry exits 0 with bundle_sha256 3d6c99b7…b9 (-6). Its selftest prints 44/44 (-8). The source-read pinned pair exits 1 with ARGV_MISMATCH and bundle db620668… (-34). These match the active rows in tools/registry.json (-31).
- Round-24 registry-replay. Its selftest prints REGISTRY_REPLAY_SELFTEST: 10/10 pass (-14). `--plan --repo <clone> --json` prints the clone, the fleet root and realpaths of the live siblings (-27). tools/registry.json has 56 rows, 49 active (-19). Its two external rows are pin-disposition-read and verify-round15 (-31). The tool's docstring and code agree on refusal, live-dependent listing and realpath planning (-23). The frozen ruler .ufo/evidence/round-24/measure.py defines predicates K1–K11 (-32).
- Frozen files. c1-survivors.py, c2-count.py, c1-mutants.json and c2-contract.json have the same git blob at 33d03b7 and at b1cc95e, and `git diff --quiet` over them exits 0 (-24, -25, -26). c2-contract.json has nine surfaces and seven required profiles (-18). The counter's source (-22) and the facade's source (-36) show the delegation and the reads described below.
- Ledger, read only through git show: 342 entries. Its provenance text reads "original184 entries retained … plus15 … re-anchors", which sums to 199.
- Route-mix. The selftest prints 8/8 (-5). The entry on spec1 exits 1 today (-10). The persisted round-21 receipt .ufo/waves/round-21/routemix-spec1.json has ok true and the same role counts (-37). Route receipts across rounds 21 to 24 are listed in -33.

Not verified in this report
- The facade selftest (13 cases) and the facade's --claim c2 run (classified 9/9, tool_selftest pass, f5_entry true). Their receipts, EXCLUDED-ReRead03-12.json and EXCLUDED-ReRead03-13.json, are excluded (see Deviations).
- --claim c1 (not run) and coldread/measure.py (not run).

Blocking gap and smallest correction
1. c2-count.py takes the tameshi-runner pin from FLEET = /home/vgpnk/Projects/shokunin, not from --repo. Make it read that pin from --repo or a fleet-root argument, so that a clone run reads no live-lane objects. Then rerun the facade selftest, --claim c1 and --claim c2 from a pinned clone and cite those receipts.

Smallest corrections (minor)
1. SKILL.md:1976: cite .ufo/waves/round-21/routemix-spec1.json as the acceptance record, and label the Entry as dependent on live routing.
2. SKILL.md:1977: give a clone path and a pinned REV in the Entry, and say that the sibling pins come from the live fleet.
3. SKILL.md:1968–1971, or the c2-count.py docstring: say that c2-count.py reads its contract and hashes itself from its own checkout (HERE), not from --rev.
4. Insert the missing spaces at :1968, :1976, :1986, :1990, :2001, :2004, :2007, :2011, :2019 and :2044.
5. SKILL.md:1986: name the ledger path.

## Deviations and limits

- Live-lane reads (assembler rule external-input-lane). Receipts -12 (facade --selftest) and -13 (facade --claim c2) each recorded eight reads of the live lane's .git metadata. c2-count.py takes the tameshi-runner pin from FLEET = /home/vgpnk/Projects/shokunin (ReRead03-22), not from --repo, so the facade read the live lane although I passed a clone path. Both receipts are renamed EXCLUDED-ReRead03-12.json and EXCLUDED-ReRead03-13.json, and neither is listed in traces or commands_executed. I read the facade source only after those runs (-36, -22). I then stopped and did not run --claim c1. The live-lane keys are removed from external_inputs of both sections. inputs of Part 2 were recomputed from the remaining receipts, so files opened only by the excluded receipts are gone.
- Failed receipts, both kept in commands_executed: -16 (a syntax error in my reader; corrected as -18) and -29 (ls-tree does not support git's glob pathspec magic; corrected as -33).
- Receipt name: ReRead03-21b.json was renamed to ReRead03-36.json to keep integer names.
- Dropped opens (paths under /home outside the fleet; counted, not hashed, by design): -4 (4), -9 (4457), -10 (1, the operator's ~/.omp/agent/config.yml), -17 (3), -24 (3), -25 (3), -26 (2), -33 (3). The excluded -12 (448) and -13 (63) are not counted here.
- Receipt summaries and this JSON were produced by Python reads of my own receipts, outside the collector. Those reads are not evidence.
- The grep tool searched the clone while I located items, so it read lane files, possibly including the committed copies of the three excepted files. None of those hits is cited as evidence, and none is in inputs.
- Not executed: .ufo/evidence/round-21/coldread/measure.py (it reads an excepted ledger), --claim c1, registry-replay --run, --project with OBS, and round-23 replay.py.
- Installs: none. No tool was installed or updated.
- Timing: the census control took 2.9 s here, against 1.77 s in the note. This is host-local (note U5) and is not a defect.

## Report JSON

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ReRead03",
  "skill_sha256": "fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f",
  "read_rev": "b1cc95e1fb62532646d74e2863770c4fed0851cc",
  "sections": [
    {
      "start": 668,
      "heading": "## Third case — cross-author confirmation (round 5, measured)",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Identifier type: SKILL.md:693, :755 and :790 call aae45531 a revision. It is the sha256 prefix (aae45531fc393579…07df6; 48410 bytes; 1033 lines) of tools/tsukuroi-census.sh as committed at da952909 (2026-10-14T14:33:30-03:00). In the sibling, git cat-file -t aae45531 returns fatal: Not a valid object name. Smallest fix: write sha256 aae45531…, commit da952909 at those three places.",
        "Pin not tied to a commit: SKILL.md:676 gives 084951be…c78c5 at measurement with no commit. The same bytes (sha256 084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5; 44947 bytes; 977 lines) are the blob at 165307fe (HEAD at the pin, note :11-13) and at 9bcd1627 (last census change before the pin). Smallest fix: name 165307fe at :676.",
        "Time zone: SKILL.md:689 gives 14:06:23 with no zone. The note gives mtime 14:06:23.048 -03 (note :14-16). Smallest fix: add -03.",
        "Stale bands rule: SKILL.md:337-339 still says the band interiors are still unprobed. The round-5 50-80 % measurement is recorded only at :733-738, not at the bands table (:327-331). Smallest fix: add a dated pointer at :337.",
        "Unverified attribution: corrected round 27, seat Read07 (SKILL.md:670, :773) cannot be checked from the cited files. The correction sits in lane files I did not open (LOG.md is one of the three excepted files and was not read). Marked unverified, not contradicted."
      ],
      "commands_executed": [
        "python3 -c 'import sys;[print(p+'\"'\"':'\"'\"'+str(i)+'\"'\"': '\"'\"'+l,end='\"'\"''\"'\"') for p in sys.argv[1:] for i,l in enumerate(open(p,encoding='\"'\"'utf-8'\"'\"'),1)]' corpus/knowledge/mutation-case-tsukuroi-census.md",
        "python3 -c 'import sys;[print(p+'\"'\"':'\"'\"'+str(i)+'\"'\"': '\"'\"'+l,end='\"'\"''\"'\"') for a in sys.argv[1:] for p,_,r in [a.partition('\"'\"':'\"'\"')] for i,l in enumerate(open(p,encoding='\"'\"'utf-8'\"'\"'),1) if (not r or int(r.split('\"'\"'-'\"'\"')[0])<=i<=int(r.split('\"'\"'-'\"'\"')[1]))]' corpus/knowledge/arm-class-matrix.md:498-525 PROVINCE.md plans/round-5.plan.md",
        "python3 -c 'import sys,hashlib;p=sys.argv[1];b=open(p,'\"'\"'rb'\"'\"').read();print(p,hashlib.sha256(b).hexdigest(),len(b),b.count(b'\"'\"'\\n'\"'\"'))' /tmp/ReRead03-Ut1W/fleet/tsukuroi-shokunin/tools/tsukuroi-census.sh",
        "python3 /tmp/ReRead03-Ut1W/scratch/mutants.py",
        "python3 -c 'import hashlib,sys;[print(p,hashlib.sha256(open(p,'\"'\"'rb'\"'\"').read()).hexdigest()) for p in sys.argv[1:]]' tools/trace-inputs.py"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-tsukuroi-census.md",
        "corpus/knowledge/arm-class-matrix.md",
        "PROVINCE.md",
        "plans/round-5.plan.md",
        "tools/trace-inputs.py"
      ],
      "inputs": {
        "PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be",
        "corpus/knowledge/arm-class-matrix.md": "bd4f4a02eb66f4e25e67a1518108d1f11c45b4edf2355d1901ec54ce55359088",
        "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604",
        "plans/round-5.plan.md": "5ade0413bc9a8d891df774156e597f893617ff80a49b4fe274adc204b8a63582",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
      },
      "external_inputs": {
        "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
        "tsukuroi-shokunin@9bcd1627072f7d8def172eed3b7a702ff218e71e:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
        "tsukuroi-shokunin@da952909584bcad9c643e842c41d6025d732fb56:tools/tsukuroi-census.sh": "aae45531fc393579b9e575683eaca0e7f337004c19713eb9a6a213e961207df6",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-20.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-35.json"
      ]
    },
    {
      "start": 1964,
      "heading": "### Round-21 gate/probe registry — finite environment differential",
      "class": "instruction",
      "verdict": "gap-blocking",
      "blocking_gaps": [
        "The C1 and C2 counter results are not verified by any receipt in this report. The facade selftest and its --claim c2 run (receipts EXCLUDED-ReRead03-12.json and EXCLUDED-ReRead03-13.json) each recorded eight reads of the live lane's .git metadata, because c2-count.py takes the tameshi-runner pin from FLEET = /home/vgpnk/Projects/shokunin rather than from --repo (ReRead03-22). --claim c1 was not run. So the counter target in c2-contract.json (classified 9/9, tool_selftest pass, f5_entry true) and the facade's 13 selftest fixtures are unverified here. Smallest fix: read the tameshi-runner pin from --repo or a fleet-root argument, so that a clone run reads no live-lane objects; then rerun the facade selftest, --claim c1 and --claim c2 from a pinned clone and cite those receipts."
      ],
      "wrong_expectations": [],
      "minor_gaps": [
        "Live routing decides the wave-route-mix Entry (SKILL.md:1976, spec .ufo/waves/round-21/spec1.json). At b1cc95e it exits 1: ROUTEMIX: REFUSE seats=71 max_share=0.4 opencode-go=38/71 zai=15/71 commandcode=12/71 cursor=4/71 openai-codex=2/71 over=['opencode-go'] (ReRead03-10). The persisted round-21 receipt .ufo/waves/round-21/routemix-spec1.json has ok true with openai-codex 28/71 and zai 27/71, for the same role counts (ReRead03-37). The gate reads ~/.omp/agent/config.yml (tools/wave-route-mix.py), which the trace records only as a dropped count (ReRead03-10: 1), not as an input. Smallest fix: cite the round-21 receipt at :1976 and label the Entry as live-routing dependent.",
        "Counter provenance wording: c2-count.py reads c2-contract.json and hashes itself from its own directory (HERE), not from --rev, although its docstring says it reads only git objects at --rev (ReRead03-22). The four frozen files are identical at 33d03b7 and b1cc95e (ReRead03-24 to -26), so the frozen claim at :1968 holds for this revision. Smallest fix: read both through git show at --rev, or document the working-tree read.",
        "The Entry at :1977 names the live lane path (/home/vgpnk/Projects/shokunin/tameshi-shokunin) and a REV placeholder, so a cold reader following it reads the live lane. The write-scope cell at :1977 ('isolated fixture/private clones only') covers writes, not reads. Smallest fix: give a clone-safe Entry and state that the write-scope cell covers writes only.",
        "Not executed by me and not counted as verified: :1978 coldread/measure.py (reads the round-21 ledger, one of the three L1-appended excepted files; the ledger was read only through git show); registry-replay --run at :2052 (the section's own correction at :2061-2072 says writes are not confined); --project with OBS (no observation file is named).",
        "Run-together tokens make exact values hard to read: :1968 'from33d03b7', :1976 'max-share0.40', :1986 'the199-entry', :1990 'minedS082', :2001 'cover16', :2004 'is1/TOTAL_MISMATCH', :2007 'exits0', :2011 'minedS083', :2019 'expected1/ARGV_MISMATCH', :2044 'minedS084/S085'. Smallest fix: insert spaces.",
        "Unnamed count: :1986 'retain the199-entry prefix' names no file. The excepted ledger's provenance text gives original 184 entries plus 15 re-anchors, which sums to 199 (342 entries in total). Entries at indices 197-198 carry skill_sha256 2859d3a3…, and index 199 carries 91e495d6…. Git show; ledger sha256 49214e8e40910a5da529da64af8f22f4df0498c36f0a9f341bb151d1bd3046f0. Smallest fix: name the ledger path.",
        "Placeholders: the Entry columns use REV, OBS, DIR and LANE, and the env-diff row writes /tmp/tameshi-f5.json. I substituted the clone path and a scratch output path (ReRead03-9)."
      ],
      "commands_executed": [
        "python3 tools/env-diff.py --selftest",
        "python3 tools/wave-route-mix.py --selftest",
        "python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json",
        "python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/bundle.json --expected .ufo/evidence/round-22/expected.json --json",
        "python3 tools/command-binding.py --selftest",
        "python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/ReRead03-Ut1W/scratch/f5-envdiff.json",
        "python3 tools/wave-route-mix.py --spec .ufo/waves/round-21/spec1.json --json",
        "python3 tools/wave-accounting.py --selftest",
        "python3 tools/registry-replay.py --selftest",
        "python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/wrong-count-bundle.json --expected .ufo/evidence/round-22/wrong-count-expected.json --json",
        "python3 -c 'import sys;[print('\"'\"'=== '\"'\"'+p+'\"'\"' ==='\"'\"');print(open(p,encoding='\"'\"'utf-8'\"'\"').read()[:200000]) for p in sys.argv[1:]]' .ufo/evidence/round-21/c2-contract.json .ufo/waves/round-21/spec1.json corpus/knowledge/hermetic-env-differential.md",
        "git -C /tmp/ReRead03-Ut1W/fleet/tameshi-shokunin diff --stat 33d03b7 b1cc95e1fb62532646d74e2863770c4fed0851cc -- .ufo/evidence/round-21 tools/round21-measure.py tools/env-diff.py tools/wave-route-mix.py tools/wave-accounting.py tools/command-binding.py tools/registry-replay.py",
        "python3 -c 'import sys;[print('\"'\"'=== '\"'\"'+p+'\"'\"' ===\\n'\"'\"'+open(p,encoding='\"'\"'utf-8'\"'\"').read()[:200000]) for p in sys.argv[1:]]' .ufo/evidence/round-21/c2-contract.json .ufo/waves/round-21/spec1.json corpus/knowledge/hermetic-env-differential.md",
        "python3 -c 'import json,collections;d=json.load(open('\"'\"'tools/registry.json'\"'\"',encoding='\"'\"'utf-8'\"'\"'));print('\"'\"'TOP'\"'\"',type(d).__name__,list(d)[:12] if isinstance(d,dict) else len(d));rows=[v for v in d.values() if isinstance(v,list)][0] if isinstance(d,dict) else d;print('\"'\"'ROWS'\"'\"',len(rows));print('\"'\"'STATUS'\"'\"',dict(collections.Counter(r.get('\"'\"'status'\"'\"') for r in rows)));names=('\"'\"'command-binding-selftest-r24'\"'\"','\"'\"'command-binding-frozen-clean-pinned'\"'\"','\"'\"'command-binding-source-read-red-pinned'\"'\"','\"'\"'registry-replay-selftest'\"'\"','\"'\"'command-binding-selftest'\"'\"','\"'\"'command-binding-frozen-clean'\"'\"','\"'\"'command-binding-source-read-red'\"'\"');[print(r.get('\"'\"'name'\"'\"'),r.get('\"'\"'status'\"'\"'),r.get('\"'\"'kind'\"'\"'),json.dumps(r.get('\"'\"'expect'\"'\"'))[:160]) for r in rows if r.get('\"'\"'name'\"'\"') in names]'",
        "python3 -c 'import sys;print(open('\"'\"'tools/wave-route-mix.py'\"'\"',encoding='\"'\"'utf-8'\"'\"').read()[:200000])'",
        "python3 -c 'print(open('\"'\"'.ufo/evidence/round-21/c2-count.py'\"'\"',encoding='\"'\"'utf-8'\"'\"').read()[:200000])'",
        "python3 -c 'print(open('\"'\"'tools/registry-replay.py'\"'\"',encoding='\"'\"'utf-8'\"'\"').read()[:200000])'",
        "git -C /tmp/ReRead03-Ut1W/fleet/tameshi-shokunin ls-tree 33d03b7 -- .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/c2-count.py .ufo/evidence/round-21/c1-mutants.json .ufo/evidence/round-21/c2-contract.json",
        "git -C /tmp/ReRead03-Ut1W/fleet/tameshi-shokunin ls-tree b1cc95e1fb62532646d74e2863770c4fed0851cc -- .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/c2-count.py .ufo/evidence/round-21/c1-mutants.json .ufo/evidence/round-21/c2-contract.json",
        "git -C /tmp/ReRead03-Ut1W/fleet/tameshi-shokunin diff --quiet 33d03b7 b1cc95e1fb62532646d74e2863770c4fed0851cc -- .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/c2-count.py .ufo/evidence/round-21/c1-mutants.json .ufo/evidence/round-21/c2-contract.json",
        "python3 tools/registry-replay.py --plan --repo /tmp/ReRead03-Ut1W/fleet/tameshi-shokunin --json",
        "python3 tools/wave-accounting.py --help",
        "git -C /tmp/ReRead03-Ut1W/fleet/tameshi-shokunin ls-tree -r --name-only b1cc95e1fb62532646d74e2863770c4fed0851cc -- ':(glob).ufo/**/routemix*'",
        "python3 -c 'import sys;[print('\"'\"'=== '\"'\"'+p+'\"'\"' ===\\n'\"'\"'+open(p,encoding='\"'\"'utf-8'\"'\"').read()[:20000]) for p in sys.argv[1:]]' .ufo/evidence/round-21/routemix-r20-spec1.exit .ufo/evidence/round-21/routemix-r20-spec1.stderr",
        "python3 -c 'import json,collections;d=json.load(open('\"'\"'tools/registry.json'\"'\"',encoding='\"'\"'utf-8'\"'\"'));rows=[v for v in d.values() if isinstance(v,list)][0];names=('\"'\"'command-binding-source-read-red-pinned'\"'\"','\"'\"'command-binding-frozen-clean-pinned'\"'\"','\"'\"'registry-replay-selftest'\"'\"','\"'\"'command-binding-selftest-r24'\"'\"');[print('\"'\"'ROW'\"'\"',r.get('\"'\"'name'\"'\"'),r.get('\"'\"'status'\"'\"'),'\"'\"'argv='\"'\"'+json.dumps(r.get('\"'\"'argv'\"'\"')),'\"'\"'cwd='\"'\"'+str(r.get('\"'\"'cwd'\"'\"')),'\"'\"'expect='\"'\"'+json.dumps(r.get('\"'\"'expect'\"'\"'))[:200]) for r in rows if r.get('\"'\"'name'\"'\"') in names];print('\"'\"'EXTERNAL_ROWS'\"'\"',[r.get('\"'\"'name'\"'\"') for r in rows if r.get('\"'\"'external'\"'\"') is True]);print('\"'\"'ROWKEYS'\"'\"',sorted(set(k for r in rows for k in r)))'",
        "python3 -c 'import sys;print(open('\"'\"'.ufo/evidence/round-24/measure.py'\"'\"',encoding='\"'\"'utf-8'\"'\"').read()[:200000])'",
        "python3 -c 'import subprocess;out=subprocess.run(['\"'\"'git'\"'\"','\"'\"'ls-tree'\"'\"','\"'\"'-r'\"'\"','\"'\"'--name-only'\"'\"','\"'\"'b1cc95e1fb62532646d74e2863770c4fed0851cc'\"'\"','\"'\"'--'\"'\"','\"'\"'.ufo'\"'\"'],capture_output=True,text=True,check=True).stdout;lines=out.splitlines();hits=[l for l in lines if ('\"'\"'routemix'\"'\"' in l.lower()) or ('\"'\"'route-mix'\"'\"' in l.lower()) or ('\"'\"'route_mix'\"'\"' in l.lower())];print('\"'\"'TOTAL_UFO_FILES'\"'\"',len(lines));[print('\"'\"'ROUTE'\"'\"',h) for h in hits];print('\"'\"'ROUTE_HITS'\"'\"',len(hits))'",
        "python3 tools/command-binding.py --bundle .ufo/evidence/round-23/source-read-bundle.json --expected .ufo/evidence/round-23/source-read-expected.json --json",
        "python3 -c 'print(open('\"'\"'tools/round21-measure.py'\"'\"',encoding='\"'\"'utf-8'\"'\"').read()[:200000])'",
        "python3 -c 'import sys;[print('\"'\"'=== '\"'\"'+p+'\"'\"' ===\\n'\"'\"'+open(p,encoding='\"'\"'utf-8'\"'\"').read()[:20000]) for p in sys.argv[1:]]' .ufo/waves/round-21/routemix-spec1.json .ufo/waves/round-21/routemix-spec2.json .ufo/waves/round-21/routemix-spec2.stderr .ufo/waves/round-22/route-mix.json .ufo/waves/round-24/route-mix1.stderr"
      ],
      "opened": [
        ".ufo/evidence/round-21/c2-contract.json",
        ".ufo/evidence/round-21/c2-count.py",
        ".ufo/evidence/round-21/routemix-r20-spec1.exit",
        ".ufo/evidence/round-21/routemix-r20-spec1.stderr",
        ".ufo/evidence/round-22/accounting-extra-cases.json",
        ".ufo/evidence/round-22/bundle.json",
        ".ufo/evidence/round-22/expected.json",
        ".ufo/evidence/round-22/measure.py",
        ".ufo/evidence/round-22/wrong-count-bundle.json",
        ".ufo/evidence/round-22/wrong-count-expected.json",
        ".ufo/evidence/round-23/extra-cases.json",
        ".ufo/evidence/round-23/replay/bundle.json",
        ".ufo/evidence/round-23/replay/expected.json",
        ".ufo/evidence/round-23/source-read-bundle.json",
        ".ufo/evidence/round-23/source-read-expected.json",
        ".ufo/evidence/round-24/extra-cases.json",
        ".ufo/evidence/round-24/measure.py",
        ".ufo/waves/round-21/routemix-spec1.json",
        ".ufo/waves/round-21/routemix-spec2.json",
        ".ufo/waves/round-21/routemix-spec2.stderr",
        ".ufo/waves/round-21/spec1.json",
        ".ufo/waves/round-22/route-mix.json",
        ".ufo/waves/round-24/route-mix1.stderr",
        "corpus/knowledge/hermetic-env-differential.md",
        "tools/command-binding.py",
        "tools/env-diff.py",
        "tools/registry-replay.py",
        "tools/registry.json",
        "tools/round21-measure.py",
        "tools/wave-accounting.py",
        "tools/wave-route-mix.py"
      ],
      "inputs": {
        ".ufo/evidence/round-21/c2-contract.json": "5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd",
        ".ufo/evidence/round-21/c2-count.py": "9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2",
        ".ufo/evidence/round-21/routemix-r20-spec1.exit": "cf205dbb8cea84897b488abcc281bf96698d5e94b1096b16657b4caba9082a22",
        ".ufo/evidence/round-21/routemix-r20-spec1.stderr": "88e99fc2d6ad8560d28248ea0717076ca0620e07184d52261b2483ccae6494c5",
        ".ufo/evidence/round-22/accounting-extra-cases.json": "e60807f2154164638b13709af930760d0f16c2c8c4a2dee7297a490c5338a41f",
        ".ufo/evidence/round-22/bundle.json": "dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e",
        ".ufo/evidence/round-22/expected.json": "e35a5934afa0ace85aeba5e687c8e12b7c7c2258af9cd00d76c13f8c0975457d",
        ".ufo/evidence/round-22/measure.py": "f833d067afd3ca17b8534fc942d6e8ed529edd3d55476802c18ea631c0678056",
        ".ufo/evidence/round-22/wrong-count-bundle.json": "d984c49c57d2b12b3a4e2583cc33842af6927f0612b3b0d663acb2ca09a7a17e",
        ".ufo/evidence/round-22/wrong-count-expected.json": "caf7d29e0fea8e8492152d3798201069452019928d6dd58ba052d98e6d0ad0ec",
        ".ufo/evidence/round-23/extra-cases.json": "87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00",
        ".ufo/evidence/round-23/replay/bundle.json": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9",
        ".ufo/evidence/round-23/replay/expected.json": "0831c9c820488dc9d9096c90aade44217b6b615501fae7810e6fce414cb2a0a1",
        ".ufo/evidence/round-23/source-read-bundle.json": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf",
        ".ufo/evidence/round-23/source-read-expected.json": "70f357e354c4badb22f974070ccf37dfda512103c3cf3ab93297a3ea27cb5dc8",
        ".ufo/evidence/round-24/extra-cases.json": "6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35",
        ".ufo/evidence/round-24/measure.py": "0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64",
        ".ufo/waves/round-21/routemix-spec1.json": "92c1edb3fdf53ac45bb6d324c16d94b388c26960aceee53f74f6883af1b97d56",
        ".ufo/waves/round-21/routemix-spec2.json": "9bf8554f1967df87cba8a5d97047089673d84ce9fffccfab5a80f464a2edbb51",
        ".ufo/waves/round-21/routemix-spec2.stderr": "23c9b86cf481ea5dbf9a7a51c59f6e63d50895eb040dcdd6f33d878a2f67c256",
        ".ufo/waves/round-21/spec1.json": "f78fe7472ed8243d46e23ca29f1bff34e646ff47832093fee815f858c22317af",
        ".ufo/waves/round-22/route-mix.json": "f5f98c3a4fba15d9da8c35997f0df194009f6ec272b79bbee07df1b2998fc4dc",
        ".ufo/waves/round-24/route-mix1.stderr": "631a54bb8c6194c67f3ffd825ec97a5b17f1802ef18501fd3168cb2d7877db64",
        "corpus/knowledge/hermetic-env-differential.md": "90756351093e2273257ce6a738bb90b6923865bc22d9276ba2cf8aeafb262e7e",
        "tools/command-binding.py": "9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d",
        "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
        "tools/registry-replay.py": "9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714",
        "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
        "tools/round21-measure.py": "eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d",
        "tools/wave-accounting.py": "96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e",
        "tools/wave-route-mix.py": "1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782"
      },
      "external_inputs": {
        "tameshi-shokunin@b1cc95e1fb62532646d74e2863770c4fed0851cc:.ufo/evidence/round-21/coldread/ledger.json": "49214e8e40910a5da529da64af8f22f4df0498c36f0a9f341bb151d1bd3046f0"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-16.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-17.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-18.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-19.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-21.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-22.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-23.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-24.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-25.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-26.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-27.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-28.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-29.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-30.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-31.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-32.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-33.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-34.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-36.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead03-37.json"
      ]
    }
  ]
}
```

## Note (plain English)

For the Third-case section I checked the cited facts against the mutation note, the sibling's git history and a rebuilt mutant sweep. The census bytes, the hardened blob and its 56-line insertion, the ten mutant sites, the 6/10 kill set and the failing counts all reproduce. The gaps are naming and pointers: "revision aae45531" is a file digest, and the pin lacks its commit.

For the Round-21 registry I ran every self-invocation the table names except the coldread measure.py (it reads an excepted ledger) and the facade selftest, whose receipt is excluded. The env-diff, route-mix, wave-accounting, command-binding and registry-replay entries pass with the exit codes the tables give. The route-mix entry does not reproduce from the revision: it depends on live operator routing and refuses today, while the round-21 receipt accepted the same role counts. The C1 and C2 counter results are not verified here, because the counter reads its tameshi-runner pin from the live fleet. So Part 2 is gap-blocking.

COLDREAD ReRead03: gap-minor, gap-blocking
