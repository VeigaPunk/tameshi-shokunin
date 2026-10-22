# Read18: cold read of SKILL.md:1212, "### The receipt at this boundary"

Verdict: gap-minor. Class: record. Section lines 1212-1229 (line 1230 starts the next ### heading; no code fences inside).

Every count and quoted line I could replay came out exact, from the named tool bytes and the pinned sibling blobs. The gaps are in provenance and labelling, not in the facts.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read18",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 1212,
      "heading": "### The receipt at this boundary",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Log and workdir pointers do not resolve: /tmp/w9-tameshi-t93/selftest.txt, /tmp/w9-tameshi-t93/regression.txt and /tmp/w9-tameshi-t93/regression are absent on this host (checked 2026-10-22). The ledger's own record of the same two harness runs (fleet-kill-rate-ledger.md:318-320, ER-4) names /tmp/w9-tameshi-t91/ (tick.log); that directory is also absent.",
        "The clock times 19:58:49Z and 19:58:59Z cannot be checked from any surviving record. The replay's REGRESSION_DATE (2026-10-22T12:49:04Z) is a different run and is not evidence for them.",
        "The anchor tools/mutate-and-run.sh:733-791 is correct only for the tool the section names (cf41efaa, commit 9f1d3c33): there line 733 opens regression_case() and lines 770 and 786-790 hold the git show materialization and the pin check. At 2227d83 regression_case() starts at line 1148 (git show at line 1202), and lines 733-791 hold spec heredoc text. The anchor carries no revision label.",
        "The counts 67/67 (selftest) and four legs belong to tool cf41efaa and carry no revision label. The tool at 2227d83 reports MUTATE_SELFTEST 97/97 and nine embedded legs (receipt Read18-10).",
        "The sentence 'Cases 5-6 are still not embedded' is true only as of the tick. Round 10 embedded them (SKILL.md:1274-1279 at 2227d83), and the section carries no supersession pointer."
      ],
      "commands_executed": [
        "python3 -c <inline reader: windows tools/mutate-and-run.sh 725-800 and corpus/knowledge/fleet-kill-rate-ledger.md 270-300>",
        "grep -n -e REGRESSION -e MUTATE_SELFTEST -e VERDICT -e killed-delta -e 'ledger legs' -e REGRESSION_DATE -e REGRESSION_TOOL -e flips -e 'match=' -e 'git show' -e 'cat-file' -e 'git archive' -e VERSION= tools/mutate-and-run.sh",
        "python3 -c <inline reader: windows tools/mutate-and-run.sh 108-140, 1146-1160, 1196-1232, 1436-1458, 1960-2017 and corpus/knowledge/fleet-kill-rate-ledger.md 296-330>",
        "grep -n -e git_clean -e GIT_OPTIONAL_LOCKS -e no-optional-locks -e selftest -e SELFTEST -e --regression -e --keep -e FLEET -e SIBLING tools/mutate-and-run.sh",
        "sha256sum tools/trace-inputs.py tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md",
        "sh -c <loop: git log --format=%H -- tools/mutate-and-run.sh, then the first 16 hex of git show | sha256sum for each commit>",
        "python3 -c <inline reader: /tmp/Read18-tFCU/tick/tameshi-shokunin/tools/mutate-and-run.sh lines 733-791 and its git show lines>",
        "bash /tmp/Read18-tFCU/tick/tameshi-shokunin/tools/mutate-and-run.sh --selftest",
        "bash /tmp/Read18-tFCU/tick/tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir /tmp/Read18-tFCU/regress-tick",
        "bash tools/mutate-and-run.sh --selftest",
        "sh -c <git -C /tmp/Read18-tFCU/tick/kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs | sha256sum; same for kagi-shokunin fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh and tsukuroi-shokunin 165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh>",
        "sh -c <git -C /tmp/Read18-tFCU/tick/mado-shokunin show eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh | sha256sum; git rev-parse --verify 9f1d3c339a7094968041c7708a65dbf7eab9fae6^{commit}>"
      ],
      "opened": [
        "tools/mutate-and-run.sh",
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "tools/trace-inputs.py"
      ],
      "inputs": {
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
      },
      "external_inputs": {
        "tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75",
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
        "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
        "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read18-12.json"
      ]
    }
  ]
}
```

## What I checked

All twelve receipts show rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 and exit 0. Each traced command ran as `python3 tools/trace-inputs.py --root /tmp/Read18-tFCU/fleet/tameshi-shokunin --out <receipt> -- <command>`.

- Class. The section states facts about a tick run and points at a tool, a ledger row and tool lines. It tells no reader to run anything, so it is a record.
- Tool identity. The tool the section names, cf41efaa, is commit 9f1d3c33 in this repo. Its bytes hash to cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75, with 1341 lines and 61632 bytes. Ledger line 281 gives the same size. The tool at 2227d83 hashes to fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de (Read18-1, Read18-5).
- Selftest replay (Read18-8). Running the tick-era tool bytes printed `MUTATE_SELFTEST: 67/67 pass` and `VERDICT: PASS`, exit 0. The 2227d83 tool printed `MUTATE_SELFTEST: 97/97 pass` (Read18-10).
- Regression replay (Read18-9, wall time 114.65 s). The tick-era tool printed `REGRESSION_TOOL: ... sha256=cf41efaa8be5f52d...`. It then printed four `REGRESSION_TABLE` lines, each with `match=10/10`, measured-killed 8, 8, 6 and 4, and `flips=0`. It closed with `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, exit 0, workdir kept. The four pinned blobs hash to their recorded pins (Read18-11, Read18-12).
- Anchor (Read18-7). In the tick-era tool, line 733 opens regression_case(). Line 770 runs `git -C "$repo" show "${rev}:${path}"`, and lines 786-790 compare the materialized sha with the pin. At 2227d83 regression_case() starts at line 1148, with the git show at line 1202. The header at lines 115-119 states the same design. So the materialization claim holds; only the line numbers are tick-era.
- Closing line at 2227d83. Line 1451 prints the same closing string as the section.
- Ledger. Line 282 says cases 5 and 6 are not embedded in --regression and carry no REGRESSION line (Read18-1). Rows 3 and 4 read stale at the tick, on lines 328-329 (Read18-3).
- Dead pointers. `ls -d` on /tmp/w9-tameshi-t91 and /tmp/w9-tameshi-t93 both reported no such file. These were path probes, not traced.
- Tooling. No tool was installed or upgraded. Already present: strace 7.2, python3 3.14.8, git 2.56.0, node v24.21.0 (fnm path), bash 5.3.20.

## Why gap-minor and not gap-blocking

The gaps are: the log and workdir pointers do not resolve, the clock times cannot be checked, the anchor and the counts carry no tool revision label, and "still not embedded" holds only as of the tick. Each is a provenance or wording fault. I reproduced every number and quoted string that I tested. If the page owner decides that a receipt without its logs cannot count as a receipt, the verdict would move to gap-blocking. I found no stated fact that fails.

## Smallest safe correction (text only; I made no edit)

1. Revision-label the anchor: "tools/mutate-and-run.sh:733-791 at cf41efaa (commit 9f1d3c33)".
2. Replace the three /tmp/w9-tameshi-t93 pointers with "logs not retained; replay at 9f1d3c33 reproduces the counts", or cite ER-4's scratch root with its absent status.
3. Qualify the cases 5-6 sentence: "as of the tick; embedded at round 10 (SKILL.md:1274-1279)".
4. Label 67/67 and the four legs as cf41efaa's counts.

## Residual risk and gaps

- The clock times 19:58:49Z and 19:58:59Z are unverified.
- The replay ran on 2026-10-22, not at the tick. It used the tick tool's bytes and the pinned sibling blobs, not the tick's logs.
- I did not replay the 2227d83 regression (nine legs). The section makes no claim about it.
- The sibling repos were read through the mirror with read-only git (show, cat-file, rev-parse, ls-tree). Nothing was written to any sibling repo.
- Outside the collector: the clone and mirror links that step 1 prescribes, `git show` copies of the tick-era tool and the sibling blobs (recorded in external_inputs), `command -v` probes, and two first attempts that ran from the wrong directory. Those two wrote no receipt and are not listed. None of these opened lane file contents.
- My own receipts were read back after the traces. They are outputs, so they are not in inputs. SKILL.md was read as the subject and is not in inputs.

COLDREAD Read18: gap-minor
