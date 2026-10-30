# T58W1Panel03 — blind panel

Axes: calibration accuracy, evidence/commit attribution, blind isolation, complete five-item coverage. No lane content edited; no runtime admission recommended.

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.

## Method and command evidence

All filesystem tool paths were absolute. Review clone was `/fast/scratch/hyaku/tameshi-r58/T58W1Panel03/clone`. In commands below, `$C` denotes exactly that absolute path; path operands beginning `$C/` expand to absolute paths. Creation command:

```sh
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r58/T58W1Panel03
mkdir -p "$S" && git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone" && test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone" && git -C "$S/clone" checkout --detach 2a32aa8228d5f86a85c81a923a3148bf792a9538
```

Output: `HEAD is now at 2a32aa82 round-57 verifier spot-check (integrator, hyaku): non-author admit/reject`; exit 0. Subsequent `git -C "$C" rev-parse HEAD` printed the full base hash, exit 0.

Exact command arguments, stdout, stderr and exits for the resolution patches and ancestry checks are preserved in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1Panel03-receipts/git-evidence.json`. No forbidden wave-57/panel or other wave-58 seat files were opened. A corpus-only discovery sweep incidentally returned round-57 lesson prose; it was not used as a status judgment or evidence. Statuses below derive from the earlier primary artifacts.

LSP availability: `read xd://lsp` returned `No such tool: xd://lsp`. Consequently textual source examination was used; no textual result is represented as semantic LSP proof. No installation/update performed.

## Open findings

### R51.8 — open

Source command: `read` absolute clone path `corpus/lessons/round-51.md:88:raw`.

Output includes: `Routed, not fixed: the round-52 deciding gate should bind each control receipt to a freeze-stamped header line (FREEZE=<sha> inside the receipt) rather than to git last-touch. Not yet shown able to fail.` This is a requested repair, not a reasoned decline.

Sweep command: `grep` tool with pattern `git log -1|FREEZE=|freeze.stamp|control-receipt-not-after-freeze`, absolute path `$C/.ufo/evidence/round-5[2-6]/deciding-run.sh`, gitignore false. Actual output:

```text
round-52/deciding-run.sh:25 c=$(git log -1 --format=%H "$REV" -- "$f")
round-52/deciding-run.sh:26 git merge-base --is-ancestor "$FREEZE" "$c" || { echo "DECIDING_REFUSED control-receipt-not-after-freeze $f"; exit 3; }
round-53/deciding-run.sh:25 c=$(git log -1 --format=%H "$REV" -- "$f")
round-54/deciding-run.sh:54 c=$(git log -1 --format=%H "$REV" -- "$f")
round-55/deciding-run.sh:51 c=$(git log -1 --format=%H "$REV" -- "$f")
round-56/deciding-run.sh:99 c=$(git log -1 --format=%H "$REV" -- "$f")
round-56/deciding-run.sh:100 git merge-base --is-ancestor "$FREEZE" "$c" || { echo "DECIDING_REFUSED control-receipt-not-after-freeze $f"; exit 3; }
```

The canonical carried gate still uses the mechanism the item identifies. No live falsifier was executed; there is no claim it passed or was killed.

### R52.3 — open

Command: `read` `$C/corpus/lessons/round-52.md:18-33`.

Output at lines 26–30:

```text
- 11 records are exact (03, 04, 05, 07, 08, 14-20).
- 8 over-count (01, 02, 06, 09-13). Example: Corr12, where the reviewer found 0 of 14 findings to be statements the reader marked as not holding.
- No reviewer found a missed failure.
So m4's counts are an upper bound on what the round-51 readers recorded; the frozen counter cannot see this (contract `cannot_see`).
```

Command: `git -C "$C" blame -L 25,30 -- "$C/corpus/lessons/round-52.md"`; output attributes all six lines to `7ff81a5b`, before routing.

Independent primary-source sweep: `grep` pattern `\*\*drift\*\*|stale|incomplete|false` on `$C/.ufo/evidence/round-51/coldread/reads/T51W2Read12.md`.

Relevant output:

```text
49:Legend: **holds** = true at CAND; **holds@sha** = true at the governing sha, moved/stale at CAND;
50:**holds-hist** = historical record, corroborated; **drift** = false/stale at CAND.
55:| P2 | "--regression replays **six** embedded legs" | **drift** | True at the pinned sha; at CAND ten legs ... |
63:| P10 | "default scratch mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX" | **drift** | At the sha :1089 literal /tmp. At CAND :1432 "${TMPDIR:-/tmp}/…" ... |
```

Command: `grep` pattern `0 of 14|holds-hist|over.count|0/14` on `$C/.ufo/waves/round-52/w2/T52W2RevCorr0912.md` returned line 61: `Corr12: over-counted 14; missed 0; verdict **over** (0/14 qualifies).`

The narrow counting rule requested by the item already contradicts zero: P2 and P10 are explicit drift, not holds-hist. I do not infer a final corrected count for all eight records. The lesson still asserts the disputed total/example, so this is not resolved by the closure merely identifying the error. A sweep over later round-53–56 lessons, knowledge, QUALITY and tools for `freeze.stamp|receipt-recency-by-last-touch|Corr12|holds-hist|0 of 14|over.count` found only unrelated self-hardening-r6 over-count text, not a correction.

## Fixed items

### R51.7 — fixed

Resolving commit: `bcba8924894216268afc4171f06eb8c28e912b46`.

Commands: `read` `$C/corpus/knowledge/fleet-kill-rate-ledger.md:439-445`; `git -C "$C" blame -L 439,441 -- "$C/corpus/knowledge/fleet-kill-rate-ledger.md"`; `git -C "$C" show --format=fuller bcba8924894216268afc4171f06eb8c28e912b46 -- "$C/corpus/knowledge/fleet-kill-rate-ledger.md"`.

Output: the blame names `bcba8924` for the appended heading and resolution. The commit patch adds:

> The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; round 51 measured ... as recorded case 10 ... That case 10 measurement supersedes the cell; §3's table stays as written.

Thus the old historical cell remaining at line 119 is intentional and satisfies the explicit append-only request.

### R52.1 — fixed

Resolving receipt commit: `4fe57df5e7f72dd9b6629708e0f6dad807196315`, not a pipeline-introduction commit.

Commands: `read` `$C/.ufo/evidence/round-54/after/c1.stdout:1-45` and `$C/.ufo/evidence/round-54/after/deciding-run.exit:1-2`; `git -C "$C" show --format=fuller 4fe57df5e7f72dd9b6629708e0f6dad807196315 -- "$C/.ufo/evidence/round-54/after/c1.stdout" "$C/.ufo/evidence/round-54/after/deciding-run.exit"`.

Actual output, introduced by that commit:

```text
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=c21081008adb cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor exit=0 covered=64 score=8
EXPLAIN arm3-rekey dirs=['rekey-r54-99c3bc88d704'] c0=99c3bc88d704566197783f66b211ee0a830e0330
EXPLAIN arm4-readers 7/7
C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
DECIDING_RUN_EXIT=0
```

This is committed evidence of the eventual re-key/deciding repair against the inherited round-52 floor, not an assertion that round 52 itself succeeded. The round-53 LOG close explicitly records its intermediate honest stop at 58/64; the later 64/64 receipts resolve that remaining debt. These receipts were inspected, not independently rerun.

### R52.2 — fixed

Resolving commit: `a41195dfc13a73958e4c5228ec196b28d03ded03`.

Commands: `read` `$C/LOG.md:2440-2497`; `git -C "$C" blame -L 2444,2463 -- "$C/LOG.md"`; `git -C "$C" show --format=fuller a41195dfc13a73958e4c5228ec196b28d03ded03 -- "$C/LOG.md"`.

Output attributes the appended round-52 entry to `a41195df`; patch includes:

```text
## 2026-10-27 — round 52 (honest stop, run wrap-up)
... Landed, in bcba8924 → f1a32461 (tip) ...
... rejected-harmed: the frozen cold-read floor read RED (64 → 45 credited,
19 sections lost by the round's own edits; the re-key never landed) ...
No claim is admitted by the round-52 report itself ...
```

The entry names both endpoints and the disposition, as requested. Its later prose about timing of repair is not used as proof of R52.1.

## Ancestry, risk and cleanup

For each fixed hash above, ran `git -C "$C" merge-base --is-ancestor <full-hash> 2a32aa8228d5f86a85c81a923a3148bf792a9538`. All three returned exit 0, empty stdout/stderr (exact calls in receipt JSON).

Verification gaps: static document/code and committed-receipt review only; no new counter execution, no live recency mutant, no complete eight-record re-count. Verdicts are panel recommendations, not admission. No status inferred solely from another seat's verdict.

Cleanup command executed: `rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W1Panel03 && printf 'SCRATCH_REMOVED /fast/scratch/hyaku/tameshi-r58/T58W1Panel03\n'`; exit 0, output `SCRATCH_REMOVED /fast/scratch/hyaku/tameshi-r58/T58W1Panel03`. Scratch deleted. No tool installs or updates.

Self-evaluation: accuracy 4 (receipts inspected rather than re-executed); completeness 5 (five IDs, three full ancestor hashes, two grounded open defects); clarity 4 (command evidence split between prose and JSON); actionability 5 (exact verdict schema and remaining defects); conciseness 4 (evidence repeats some excerpts for independent reproducibility). Overall 4.4/5. Highest-impact improvement would be an authorized live recency falsifier; no unrun result is claimed here.
