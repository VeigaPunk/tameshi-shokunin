# SentinelLeak — round 35 W2 hygiene review

**Axes:** calibration; artifact hygiene (host-path exposure, credential/token and SSH-reference scan).

## Scope and method

Inspected the round-35 commit snapshot at `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`, including the complete 44-path diff from base `51d3f08073be65d3475cf0286042fc0dbe4c4a7d`, and the W1 reports in that snapshot. Also scanned the W2 report files present in `.ufo/waves/round-35/w2/` at the time of the final inventory: 22 reports plus `swarm-registry.json`. The W2 files are live working-tree reports, not part of the dispatch-pin snapshot.

To avoid a Git clone/checkout mutation, I materialized the snapshot only in `/fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/` with read-only `git archive` commands. Exact commands/results:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --verify '7da6e076c2e25936a3b60dde2a4080d8f05b7e5b^{commit}'
# exit 0; 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --name-only 51d3f08073be65d3475cf0286042fc0dbe4c4a7d 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
# exit 0; 44 changed paths

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b .ufo/evidence/round-35 .ufo/waves/round-35 | tar -x -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned
# PIPESTATUS=0 0

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b .ufo/evidence/round-34/dev/authoring.stdout .ufo/waves/round-34/w1/PanelSeed4.md .ufo/waves/round-34/w1/ReviewDevReceipts.md SCORECARD.md corpus/README.md corpus/SOURCES.md corpus/knowledge/closeout-r11.md corpus/knowledge/survivor-fixture-minimization.md corpus/knowledge/witness-equivalence-rule.md corpus/lessons/round-34.md tools/tally-audit-v3.py | tar -x -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/additional
# PIPESTATUS=0 0
```

Path searches used the specialized `functions.grep` tool on those extracted commit inputs and the live W2 report directory. Credential searches returned `No matches found`; the search tool does not expose a numeric process exit status. Hash commands below were `sha256sum` over the listed full paths and exited 0. For the W2 reports, one `sha256sum` invocation over all 22 report paths exited 0; the registry hash was obtained separately, also exit 0.

## Exact SHA-256 commands

Each command exited 0; the output hashes are listed beside the corresponding file/line pointers above and below.

```sh
sha256sum /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/waves/round-35/dispatch-w1.json /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/waves/round-35/spec-w1.json /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/waves/round-35/w1/ExecPristine.md /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/waves/round-35/w1/RevengerRootShape.md /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/waves/round-35/w1/ReviewPanelDistinct.md /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/waves/round-35/w1/ReviewSealedGate.md /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/waves/round-35/w1/ScribeReport.md /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/waves/round-35/w1/SealAcceptCommentBlock.md
sha256sum /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/pinned/.ufo/evidence/round-35/after/census-at-round-end.stdout /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/additional/SCORECARD.md /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/additional/.ufo/waves/round-34/w1/PanelSeed4.md /fast/scratch/hyaku/tameshi-r35-seats/SentinelLeak/additional/.ufo/waves/round-34/w1/ReviewDevReceipts.md
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ExecReplayC2Before.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/CriticAxis.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/CriticPredicate.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ScoutCorpusRows.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealAcceptCommentHead.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealAcceptHeredoc.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ScribeS102.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealCfg11Mask.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealCfg00Guard.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SentinelFleet.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/CriticC2.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/CriticOverfit.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealAcceptTrailing.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/CriticRunner.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealStdoutWorkdir.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealKillStaticOp.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ExecReplayControl.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealStdoutDetail.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SealKillHeadRead.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ScribeTrio.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ExecSelftest.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/AttackPerIndexParse.md
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/swarm-registry.json
```
## Findings — HYGIENE

### H1. Committed dispatch/spec contain host-specific setup paths

**Evidence:** `dispatch-w1.json` SHA-256 `58c9bc4ea35d0cea0c22c0d9639f2addef1a0150394d53216616cf84c2bab2ca`, lines `613` and `618 + 5n` for `n=0..63` (task prompt lines through `933`); `spec-w1.json` SHA-256 `427a0bd31fee2fc95ef44269977cda0e9cec26835e46f90a7ac2a838ca472acd`, lines `4` and `12 + 8n` for `n=0..63` (prompt lines through `516`). The embedded task setup repeats `/home/vgpnk/Projects/shokunin/tameshi-shokunin` and `/fast/scratch/hyaku/tameshi-r35-seats/<seat>/...`.

**Impact/exploit path:** any reader of the committed dispatch artifacts can recover the host account name, project checkout root, scratch mount, and seat-directory naming. Those paths are also nonportable outside this workstation. No credential is exposed by these strings.

**Smallest remediation:** replace literal workstation roots in committed task payloads with `$REPO_ROOT`/`$SCRATCH_ROOT` variables or repository-relative placeholders; retain resolved absolute paths only in uncommitted execution logs.

### H2. Other committed round-35 diff bytes retain local home/scratch roots

**Evidence:** each entry gives the exact line(s) and SHA-256 of the inspected bytes.

| Committed file at pin | Exact path-bearing line(s) | SHA-256 |
|---|---:|---|
| `.ufo/evidence/round-35/after/census-at-round-end.stdout` | 10 | `681ef7768435ec2812cbab2014397bfe10d857a7a53385f71afe61d792462992` |
| `SCORECARD.md` | 702, 784, 869–870, 1221, 1243, 1643 | `cbea24c85074baac8904cab3b2937c6e93634431c9ee408b711fc58e66e7961f` |
| `.ufo/waves/round-34/w1/PanelSeed4.md` | 7, 37, 40–42, 525 | `985c64ea63dfc68f93fbda71230418c93cc9c5f63863e2236820d15753f78a9c` |
| `.ufo/waves/round-34/w1/ReviewDevReceipts.md` | 40–41, 136 | `ff532da39c28846c3d0ff832340312cdb97a457e68843ddc8e8642898267b3c2` |

The lines contain `/home/vgpnk/...` and/or `/fast/scratch/hyaku/...`; the SCORECARD and two W1 reports are in the base-to-pin changed-file set. The paths make archived evidence host-bound and disclose a local account/workspace layout.

**Smallest remediation:** use repo-relative evidence pointers and describe scratch artifacts by report-local names instead of machine roots. No such cleanup was made in this scan-only assignment.

### H3. Six committed W1 reports embed host paths

| W1 report | Exact path-bearing line(s) | SHA-256 |
|---|---:|---|
| `ExecPristine.md` | 8, 11, 15, 18, 32, 37, 41 | `4f9fbc7673c0dfd3203afecb0b0b96fed0ce6720eed7a00057abe95aa1065d41` |
| `RevengerRootShape.md` | 15–16, 141 | `60dd10a1631347bbceb3ecd0e92351c1a3c84ef73a37b9042ff07579331221ce` |
| `ReviewPanelDistinct.md` | 24–25, 40, 108 | `e0fa4ae55e168411f2d6f9f5023d35fb45583efba6835db6e21b8a753dead9ea` |
| `ReviewSealedGate.md` | 4, 87 | `c8e270e8bc856482547c17de1a69379eb10003f91470c29057e62996d96bd480` |
| `ScribeReport.md` | 6, 18–20, 24, 28, 58, 76, 82–86, 92, 107, 111 | `4131167552610afaa38bea46425ffcba4e3e3bf19162ac6343b4bfb3858f71ff` |
| `SealAcceptCommentBlock.md` | 13, 21, 23, 72–74 | `ac81767cc9c123e59aefe82798c5bb5fb57beaf9029ba9b1407f901b98d0cded` |

The cited lines expose `/home/vgpnk/...` and/or per-seat `/fast/scratch/...` paths. These are not secrets, but they are machine-local paths committed into long-lived reports and can make the documented commands unusable elsewhere.

**Smallest remediation:** replace local roots with relative paths or named variables, retaining commit IDs and content hashes as provenance.

### H4. Live W2 reports also contain workstation roots

These are the 22 W2 reports present at the final inventory; exact path-bearing lines and their current hashes follow. The registry was also scanned (SHA-256 `0929b1c1f72d86c70f6172348fdf72242c33599a384b74e3e3ff4c3298acbead`).

| W2 report | Exact path-bearing line(s) | SHA-256 |
|---|---:|---|
| `ExecReplayC2Before.md` | 5, 14, 17, 19, 21, 26, 29, 43–44 | `a91a979aeb75d025eb3832c73fc04c0efa86d30f916734fa5fd27b8035bc3d26` |
| `CriticAxis.md` | 11, 19–20, 22, 24, 34, 44, 51, 61, 80–89, 97, 103, 109–110, 118, 126 | `c4e01dc6d8ef59b74cd9cb373c7b004b87e97c7c3fd992fd1814b218d7bd3c0c` |
| `CriticPredicate.md` | 7, 18, 28–33, 36, 48, 55, 61–62 | `16386777d729d8efa160b1e1179b88c75e91f1c84585411adbd1b8f2c8cf6b6d` |
| `ScoutCorpusRows.md` | 5, 58 | `d89143ecbc1e7904c0659e215b3683306eaea5e5f8bdd235c8e59435ac82be6a` |
| `SealAcceptCommentHead.md` | 19, 25, 27, 90 | `a27f7245c583364b6a39d5092af0fbc1e224ebfc4bfde2e36e822aab96ed7005` |
| `SealAcceptHeredoc.md` | 29, 33, 35 | `d6e0eebf3841bfca1314267be87fcbf936d7e937df96a9f517b5adb3071f8de1` |
| `ScribeS102.md` | 22, 25, 28, 36, 47, 52, 61–62 | `291e45882f6f22285de1165b3638acf0543f5c20045582babe6ff8e2139a4337` |
| `SealCfg11Mask.md` | 3, 35, 37–38, 82 | `e6f14f28bf991ca846732487b1403aa739dae53edbfed79a596bdb34575d2898` |
| `SealCfg00Guard.md` | 3, 18, 32, 42–52, 66, 70–76 | `39008a7c46f1d37c05da57f5824f341b1921116ae719fa50be6899e0e17639b2` |
| `SentinelFleet.md` | 11, 61, 67, 73, 79, 90, 92, 94 | `10ecf6f53337cda1d93163895bf0c0190b8e225db9e16bf7c25c260d416dd44b` |
| `CriticC2.md` | 15, 20–21, 28–31, 35, 51, 59, 63, 74–75, 88, 97–99, 104, 127, 129 | `648e1eb5c99cf68f8c0bf459a81463a8e6e910f0159198aee760bfb6db6da703` |
| `CriticOverfit.md` | 11, 15, 33, 42, 45–46, 57, 61–62, 65, 86, 93, 98, 110–112, 117–118, 141–142 | `41d4d49c5bece06f28923e2a5cff0d4408b77c1aa508f0545a1892a816eac0ee` |
| `SealAcceptTrailing.md` | 36–37, 39–40 | `90f1ab56f1650d5903e0ebfe6c427a433af41cc4407ae9f857e86757465d3d63` |
| `CriticRunner.md` | 19, 28–29, 38, 43–45, 48, 57, 69, 75, 92–93, 99–100, 115–116, 137–138, 145 | `e12c8830710e4e03b109b591e1def54f35ad42554078e34ac6b7c57342dd25d0` |
| `SealStdoutWorkdir.md` | 19, 21, 29–35, 43–49, 58, 62, 69 | `973600e8bf55fe151e943873b6b1f84f3412fd7635e3b54ce826a6f2493cc14f` |
| `SealKillStaticOp.md` | 75, 78, 83, 86 | `e46a449932bf3c3cc15e8cddc53dc547ea429bf1a14abfe86e7ab97e8e3411a1` |
| `ExecReplayControl.md` | 7, 18, 21 | `0ac352b6c10992572209aae3e9ffde349041945779fe9d74bbdce4b496d5ef79` |
| `SealStdoutDetail.md` | 33, 37, 39, 88, 92 | `73e1d9ac7bda19bff25b5a4f4df8ca01ccbbb7d3f982a7c6481eca74cae7f649` |
| `SealKillHeadRead.md` | 34, 42–48, 56–62, 77, 83, 87, 93–94, 96 | `0b288a2a83af1b1a28a9cf2dc69935659d13736e5db69a59415699ec045127fe` |
| `ScribeTrio.md` | 73, 76, 79, 82, 85, 88, 91, 94, 97, 107 | `cf752a22a703477db60f83d5a62cf909b0972daed6b5e2701b67c0575692780f` |
| `ExecSelftest.md` | 16, 25, 31 | `8a249dd0fbbb5094f6ce335eeef688e6ca0ec8cf654c18aa123e15cd8f4c2359` |
| `AttackPerIndexParse.md` | 15, 22, 24, 35–36, 168, 236 | `bac62687ad6a5170c7f01bb9bf07216bb2f333e65d72ceee936a6373484cf800` |

**Impact/exploit path:** readers of these persisted reports can identify the host user and checkout/scratch layout, while command snippets are tied to those local roots. The smallest remediation is the same as H1: use repo-relative references or `$REPO_ROOT`/`$SCRATCH_ROOT` placeholders in reports, keeping hashes and commit IDs for provenance.

## What I could not break

- **No credential or token material matched the scanned signatures** in the 44-path base-to-pin diff or the W2 report/registry snapshot. The scan covered PEM private-key headers; AWS, GitHub, GitLab, Slack, Google, OpenAI, npm/PyPI-style, and JWT token forms; bearer strings; and password/API-key/secret/access-token assignments. These searches returned `No matches found`; this is bounded to those patterns, not proof against encoded or novel secret formats.
- **No `~/.ssh` or `.ssh/` references matched** the committed snapshot, W1 reports, or W2 reports/registry.
- No CRITICAL or BOUND finding in this assigned hygiene surface. The observed absolute `/tmp/tameshi-r4-2-regression.*` roots are the contract-required runner test roots; they were not treated as user/workspace path disclosure. No files other than this requested report were changed, and no tools were installed.

Report: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/SentinelLeak.md`
