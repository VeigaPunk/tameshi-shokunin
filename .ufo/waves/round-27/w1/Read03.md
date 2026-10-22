# Read03: cold read of the mutation-sweep recipe (SKILL.md:131-245)

Verdict: wrong-expectation. The recipe runs as written and reproduces the cited sweep results on two pinned artifacts. One expectation is false. Step 9 says the before/after check proves the absence of writes. The page's own Restore discipline says the check proves endpoint identity only (SKILL.md:228 against SKILL.md:377-378).

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read03",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 131,
      "heading": "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence",
      "class": "instruction",
      "verdict": "wrong-expectation",
      "blocking_gaps": [],
      "wrong_expectations": [
        "Step 9 (SKILL.md:224-229) says the before/after check 'proves the *absence* of writes' and is 'the record's headline, not an appendix'. The Restore discipline section it points to says 'Before/after fingerprints establish endpoint identity, not that no transient write occurred' (SKILL.md:377-378). Receipts 12, 36 and 37 show sha256, size, mtime and git status identical before and after the sweep, which supports endpoint identity and nothing stronger. Smallest correction: replace the sentence with 'The sweep's edits all lived in scratch, so the check shows endpoint identity only, not the absence of transient writes (Restore discipline below).' and reword 'Restore + prove the substrate never moved' to 'Restore + prove endpoint identity'."
      ],
      "minor_gaps": [
        "Step 9 says 'Re-run step 2's checks' but lists only sha256, size, mtime and git status. Step 2 also records the repo revision, and Restore discipline says the after-revision is not established (SKILL.md:150-152, 225-226, 386-391).",
        "The recipe never names the maintained instrument tools/mutate-and-run.sh. The lane table names it at SKILL.md:1391 and Restore item 6 names it as the replay route at SKILL.md:397-400. That instrument marks KILLED on any non-zero exit (tools/mutate-and-run.sh:35, :548), while step 7 requires count and token adjudication (SKILL.md:191-204). Its kill rate divides by all defects, inconclusive included (:505, :568), while step 7 excludes inconclusive runs (SKILL.md:210-211). The section does not say which rule governs.",
        "Step 4 says 'one defect per class' (SKILL.md:162-163), but the manifests it names as the shape do not follow that rule. Kimi D1 and D2 are both off-by-one count (mutation-case-kimi-census.md:44-45). Kimi D4 and D5 are both dropped arm (:47-48). Kagi B4 and B5 are both dropped branch (mutation-case-kagi-census.md:70-71).",
        "Step 5 presents 'both lanes' drivers' (SKILL.md:173-175) as the model, but those drivers are unversioned scratch scripts. The kagi erratum R21 says the case-note commands do not rebuild the driver after scratch loss (mutation-case-kagi-census.md:271-275), and Restore discipline item 6 says the same (SKILL.md:396-398). The recipe does not carry that caveat.",
        "Step 7 cites mutation-case-kagi-census.md:82-103 for the summary 'SELFTEST: FAIL (1/16 cases)', but that string is not in that range. The note's table has only '1/16' / FAIL at :67. Receipt 15 shows the suite prints the string verbatim, so the text is right and the citation is not.",
        "Step 1 says kumitate suites print 'n/m pass' (gates-survey-kumitate.md:19-31). Cite-check and surface-probe print 'n/m cases passed' (:21-22).",
        "Run-together tokens make numbers hard to read or copy: 'bash16' (SKILL.md:147), 'denominators43 and16' (:193), 'nodev24.21.0' and 'Round2:7.0s for11 runs' (:241), 'a280s bound' and 'round3:11.0s for11 runs' (:242), 'U5 at204-205' (:244)."
      ],
      "commands_executed": [
        "python3 /tmp/Read03-ntqN/scratch/reader.py corpus/knowledge/mutation-case-kimi-census.md",
        "python3 /tmp/Read03-ntqN/scratch/reader.py corpus/knowledge/mutation-case-kagi-census.md",
        "python3 /tmp/Read03-ntqN/scratch/reader.py corpus/knowledge/gates-survey-kumitate.md:1-40 corpus/knowledge/gates-survey-kagi.md corpus/README.md:re/G-R2-1 tools/mutate-and-run.sh:1-120",
        "python3 /tmp/Read03-ntqN/scratch/reader.py /tmp/Read03-ntqN/rehearse/pristine.sh:85,191,200-204,212-218,229,241,371,403-417,435,862",
        "python3 /tmp/Read03-ntqN/scratch/reader.py tools/mutate-and-run.sh:re/kill-rate",
        "python3 /tmp/Read03-ntqN/scratch/reader.py tools/mutate-and-run.sh:re/kill-rate|KILLED|SURVIVED|INCONCLUSIVE",
        "bash /tmp/Read03-ntqN/rehearse/pristine.sh --selftest",
        "python3 /tmp/Read03-ntqN/rehearse/make_mutants.py",
        "python3 /tmp/Read03-ntqN/rehearse/make_kimi.py",
        "python3 /tmp/Read03-ntqN/scratch/reader.py tools/mutate-and-run.sh:540-568",
        "sha256sum tools/trace-inputs.py tools/mutate-and-run.sh",
        "bash -c sha256sum /tmp/Read03-ntqN/fleet/kagi-shokunin/corpus/surface-census.sh && stat -c \"%s bytes mtime=%y %n\" /tmp/Read03-ntqN/fleet/kagi-shokunin/corpus/surface-census.sh && sha256sum /tmp/Read03-ntqN/fleet/kumitate-shokunin/scripts/kimi-census.mjs && stat -c \"%s bytes mtime=%y %n\" /tmp/Read03-ntqN/fleet/kumitate-shokunin/scripts/kimi-census.mjs",
        "python3 /tmp/Read03-ntqN/scratch/reader.py tools/mutate-and-run.sh:505-539",
        "node /tmp/Read03-ntqN/rehearse/pristine.mjs --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B1.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B2.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B3.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B4.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B5.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B6.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B7.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B8.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B9.sh --selftest",
        "timeout 280 bash /tmp/Read03-ntqN/rehearse/mutant-B10.sh --selftest",
        "timeout 280 node /tmp/Read03-ntqN/rehearse/mutant-D2.mjs --selftest",
        "timeout 280 node /tmp/Read03-ntqN/rehearse/mutant-D10.mjs --selftest",
        "timeout 280 node /tmp/Read03-ntqN/rehearse/pristine.mjs --root /tmp/Read03-ntqN/rehearse/empty-root",
        "timeout 280 node /tmp/Read03-ntqN/rehearse/mutant-D2.mjs --root /tmp/Read03-ntqN/rehearse/empty-root",
        "timeout 280 node /tmp/Read03-ntqN/rehearse/mutant-D10.mjs --root /tmp/Read03-ntqN/rehearse/empty-root",
        "python3 /tmp/Read03-ntqN/scratch/reader.py /tmp/Read03-ntqN/rehearse/pristine.sh:1-60",
        "python3 /tmp/Read03-ntqN/scratch/reader.py /tmp/Read03-ntqN/rehearse/pristine.sh:re/ROOT=|baseline=|BASELINE|\\$HOME\\}|expand|--census|--shapes|--baseline|verify\\)",
        "bash /tmp/Read03-ntqN/rehearse/pristine.sh verify --root /tmp/Read03-ntqN/rehearse/probe/host --census /tmp/Read03-ntqN/rehearse/probe/census5.tsv --shapes /tmp/Read03-ntqN/rehearse/probe/shapes.tsv --baseline /tmp/Read03-ntqN/rehearse/probe/baseline.tsv",
        "bash /tmp/Read03-ntqN/rehearse/mutant-B5.sh verify --root /tmp/Read03-ntqN/rehearse/probe/host --census /tmp/Read03-ntqN/rehearse/probe/census5.tsv --shapes /tmp/Read03-ntqN/rehearse/probe/shapes.tsv --baseline /tmp/Read03-ntqN/rehearse/probe/baseline.tsv",
        "bash /tmp/Read03-ntqN/rehearse/pristine.sh verify --root /tmp/Read03-ntqN/rehearse/probe/host --census /tmp/Read03-ntqN/rehearse/probe/census10.tsv --shapes /tmp/Read03-ntqN/rehearse/probe/shapes.tsv --baseline /tmp/Read03-ntqN/rehearse/probe/baseline.tsv",
        "bash /tmp/Read03-ntqN/rehearse/mutant-B10.sh verify --root /tmp/Read03-ntqN/rehearse/probe/host --census /tmp/Read03-ntqN/rehearse/probe/census10.tsv --shapes /tmp/Read03-ntqN/rehearse/probe/shapes.tsv --baseline /tmp/Read03-ntqN/rehearse/probe/baseline.tsv",
        "bash -c sha256sum /tmp/Read03-ntqN/fleet/kagi-shokunin/corpus/surface-census.sh && stat -c \"%s bytes mtime=%y %n\" /tmp/Read03-ntqN/fleet/kagi-shokunin/corpus/surface-census.sh && sha256sum /tmp/Read03-ntqN/fleet/kumitate-shokunin/scripts/kimi-census.mjs && stat -c \"%s bytes mtime=%y %n\" /tmp/Read03-ntqN/fleet/kumitate-shokunin/scripts/kimi-census.mjs",
        "bash -c GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read03-ntqN/fleet/kagi-shokunin status --porcelain -- corpus/surface-census.sh; echo \"porcelain-exit=$?\"; GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read03-ntqN/fleet/kagi-shokunin rev-parse HEAD",
        "strace -V",
        "python3 --version",
        "git rev-parse HEAD"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/knowledge/gates-survey-kumitate.md",
        "corpus/knowledge/gates-survey-kagi.md",
        "corpus/README.md",
        "tools/mutate-and-run.sh",
        "tools/trace-inputs.py"
      ],
      "inputs": {
        "corpus/README.md": "33915658d9ef1ed3b93ed0cf58ba5b341bc58facc5d1ff73574e6ddd297dcb79",
        "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
        "corpus/knowledge/gates-survey-kumitate.md": "3dca7a1a5c621bf0ec75948d0836839dec98651673bb2987861d9aa122579b0e",
        "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
      },
      "external_inputs": {
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "7818970b80d4951b8edf15dcc8c5a16efe57f457f956a5ce019f049068538156",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/.gitignore": "3767312444cc6425c133ea7e335892948272aa886559e4cc3d3e41a5394ce74e"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-13.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-16.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-17.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-18.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-19.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-20.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-21.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-22.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-23.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-24.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-25.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-26.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-27.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-28.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-29.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-30.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-31.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-32.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-33.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-34.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-35.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-36.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-37.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-38.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-39.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read03-40.json"
      ]
    }
  ]
}
```

## Note: what I checked

- Class: `instruction`. The section tells a reader to run a sweep, so I ran it. Heading at SKILL.md:131; the next heading is at :246; no fences inside 131-245.
- Pins: I took committed bytes with `git show` (outside the collector; listed under external_inputs). Kagi `corpus/surface-census.sh` at fecee874 hashes to 275d8294, 44212 bytes, 886 newlines, last byte `c`, which matches mutation-case-kagi-census.md:13-17. Kimi `scripts/kimi-census.mjs` at 175de6ba hashes to 83016d45, 43273 bytes, 896 lines, which matches mutation-case-kimi-census.md:13-16.
- Controls: kagi (receipt 7) prints `SELFTEST: PASS (16 cases)`, exit 0, with ok-cases 01-14 and skip-cases 15-16 (`substrate-absent`). Kimi (receipt 14) prints `KIMI_CENSUS_SELFTEST: 43/43 pass` and `VERDICT: PASS`, exit 0, on node v26.12.0. The note cites v24.21.0 (kimi:21), and the control still passes.
- Uniqueness gate (receipts 8 and 9): all 12 @old strings occur exactly once in the pinned bytes, every new string differs from its old string, and every mutant hash differs from pristine. Kagi lines: B1 241, B2 435, B3 229, B4 200-204, B5 214-217, B6 371, B7 405-406, B8 85, B9 191, B10 862. Kimi lines: D2 378, D10 145.
- Kagi sweep (receipts 15-24, `timeout 280`): exit 1 for B1, B2, B3, B4, B6, B7, B8 and B9, so eight kills; exit 0 for B5 and B10, the two survivors (kagi:67-76, :50). Failing labels match the note (kagi:84-103). B1 gives `bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got exit=0` and the summary `SELFTEST: FAIL (1/16 cases)`. B4 gives `bad-case 07 symlink-swap want exit=1 token=SURFACE LINK got exit=1`, a token-only kill (kagi:88-91). B2 fails cases 01 and 04; B3 fails 01, 04 and 06; B6 fails 01 and 04; B7 fails 10; B8 fails 13 and 14; B9 fails 03 and 04.
- Kimi survivors (receipts 25-29): D2 and D10 each pass 43/43 with exit 0 (kimi:44-53). On the empty root, the pristine verdict ends `+22 more`, D2 prints five ids then `+23 more`, and D10 prints `FAMILY K2 ... frozen=24` (kimi:82-99). All match the note.
- Kagi survivor probes (receipts 32-35): the note's own probe fixtures are not in the lane, so I wrote one-row fixtures from the gate header. B5: pristine prints `SURFACE DIVERGED $HOME/bin/tool (declared exec, no execute bit)` with exit 1; the mutant prints `SURFACE OK $HOME/bin/tool (exec 644)` with exit 0 (kagi:111-114, :252-254). B10: pristine prints `ok=1` with exit 0; the mutant prints `ok=0` with exit 0 (kagi:118-122).
- Substrate (receipts 12, 36, 37): the live kagi and kumitate files have the same sha256, size and mtime before and after the sweep, and `git status --porcelain` for the kagi path is empty. Live kagi HEAD is now 899c50b, not the pinned fecee874, and the live kumitate file has moved. That is why the pins come from `git show`.
- Citations: I opened every cited note range through the collector (receipts 1-4, 6, 10, 13, 30, 31). Everything I checked resolves to the claimed text, except the items in minor_gaps. The Standing rules at SKILL.md:25-28 do support the scratch namespace.
- Verdict reasoning: no step is blocked, and every executed command behaved as the section says. The one false statement is the step 9 claim about absence of writes, so the verdict is wrong-expectation. [INFERENCE] With that one sentence corrected, the remaining items are minor, and a re-read would likely give gap-minor. I did not re-run the section after any change.
- Not done: I did not re-run the full kimi 10-mutant sweep (only D2, D10, the control and the probes). I did not check the note's sensitivity commands at kagi:248-249, which need the unreproduced probe fixtures. That is an observation about the kagi note, outside this section.
- Drift for the L1: `tools/mutate-and-run.sh` at 2227d83 hashes to fb91ef76, while the evidence records 75ed934d (for example `.ufo/evidence/kaika-round-1/coldread/A-tool.txt`). Kimi's D2 and D10 verdicts held on node v26.12.0, which narrows U5 for two mutants without closing it.
- Unreceipted actions: `mktemp`, the lane `git clone --no-hardlinks` and detached checkout (setup, before the collector root existed); a first kagi control run with the same output as receipt 7; `command -v strace`; a listing of the live lane's traces and w1 directories (names only); pre-sweep read-only sibling git calls (`status`, `rev-parse`, `cat-file`, run with GIT_OPTIONAL_LOCKS=0); Python writes of scratch files; and discovery glob and grep across the clone, whose matches came from .ufo/evidence and corpus files that I did not use as evidence. Receipt 5 is a failed attempt, since an unquoted `|` split the command; it is listed in commands_executed.
- No installs or upgrades. strace 7.2, node v26.12.0 and Python 3.14.8 were already present, so I did not read RULES.md.

COLDREAD Read03: wrong-expectation
