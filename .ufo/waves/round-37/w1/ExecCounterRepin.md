# ExecCounterRepin — r37 counter re-pin replay (C2 re-attestation)

**Verdict: C2_R37_REPIN_PASS=true, reproduced twice and byte-identical to the committed
receipt when replayed at that receipt's own revision.** All frozen v2 counts match; exit 0;
stderr empty; nothing in the live lane was touched except this report file.

## Isolation

The replay ran in an independent clone, never in the live lane checkout:

- clone: `/tmp/r37-repin-exec/lane-clone`, `git clone --no-hardlinks --no-checkout`
- detached checkout: `e6185d5f0b63a6963205110cb098f2f1eca27622` (run 1, live-lane HEAD / final
  evidence rev; tree `f83905416699c8fc74df4fa7c99828289e5f127b`) and
  `ae9b771ab795fb5b4a6302165d8abdc0a2c6b229` (run 2, the rev named by the committed receipt)
- clone object store is self-contained: `no_alternates` (no `.git/objects/info/alternates`)
- live lane after both runs: `HEAD=e6185d5f0b63a6963205110cb098f2f1eca27622`, tree unchanged;
  `git status --porcelain` shows only sibling seats' untracked
  `.ufo/waves/round-37/w1/*.md` files. No index, ref, `.git`, jj or evidence-byte change.
- wrapper temp work (`.ufo/evidence/round-37/c2-repin.py:52`) left nothing behind:
  `ls -d /tmp/tameshi-r37-repin-*` → none.

## Exact commands

```
# run 1 — final evidence rev
cd /tmp/r37-repin-exec/lane-clone
python3 .ufo/evidence/round-37/c2-repin.py \
  --lane "$PWD" --rev e6185d5f0b63a6963205110cb098f2f1eca27622 \
  > /tmp/r37-repin-exec/repin.stdout 2> /tmp/r37-repin-exec/repin.stderr
echo $? > /tmp/r37-repin-exec/repin.exit

# run 2 — the rev the committed receipt names
python3 .ufo/evidence/round-37/c2-repin.py \
  --lane "$PWD" --rev ae9b771ab795fb5b4a6302165d8abdc0a2c6b229 \
  > /tmp/r37-repin-exec/repin-ae9b771.stdout \
  2> /tmp/r37-repin-exec/repin-ae9b771.stderr
```

## Pin identity at the tested rev (observed, not inferred)

| input | path | sha256 | pin |
|---|---|---|---|
| frozen counter | `.ufo/evidence/round-36/c1/c1-measure-v2.py` | `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` | `counter_sha256`, `.ufo/evidence/round-37/counter-pin.json:6` — match |
| tally-audit | `tools/tally-audit-v3.py` | `da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede` | `tool_sha256`, `counter-pin.json:8` — match |
| runner (oracle pin) | `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `PIN_RUNNER`, counter `:63` — match |
| wrapper | `.ufo/evidence/round-37/c2-repin.py` | `f25eafa5d38bcddffd66289fda22e8a9f1eca78edd426e791c2136f74ab8bd3b` | identical at `ae9b771` and `e6185d5` |

The wrapper enforces both digests itself at `.ufo/evidence/round-37/c2-repin.py:49` before it
runs anything. Bytes on the pinned surface (`tools/mutate-and-run.sh`, `tools/tally-audit-v3.py`,
`.ufo/evidence/round-35/c1`, the frozen counter, the wrapper, `counter-pin.json`) are identical
between `ae9b771` and `e6185d5` (`git diff --stat` empty), so the two runs are a replay of one
frozen input set, not two different inputs.

## Receipts

| run | exit file | stdout | stderr |
|---|---|---|---|
| 1 @ `e6185d5` | `0\n` (sha `9a271f2a…86aa`), elapsed 228 s | 2361 B, sha `f5d527d3f7dcdb375046ec92ce560ef5e0abd96b65f862c081960f8739091798` | 0 B, sha `e3b0c442…b855` |
| 2 @ `ae9b771` | `0\n` (sha `9a271f2a…86aa`), elapsed 253 s | 2361 B, sha `cc273a771b6916fb26a862e8fe4b5f2f200aa597dd440e1dc6e4b26ff09e70b1` | 0 B, sha `e3b0c442…b855` |

Run 2's stdout is **byte-identical** (`cmp`) to the committed
`.ufo/evidence/round-37/c2-repin-after.stdout` (sha `cc273a77…70b1`), and its exit/stderr files
are byte-identical to the committed `c2-repin-after.exit` (`0\n`) and `c2-repin-after.stderr`
(empty). Run 1's stdout differs from the committed receipt only in the `rev=` token
(verified: equal after normalising `rev=<REV>`), i.e. every per-copy row and every count is
reproduced at the final evidence revision.

## Full stdout — run 1 (`e6185d5`, 18 lines, 2361 bytes)

```
COPY kill  cfg00-accept-swap                  cfg00-accept-swap.json div=(0,0) rc=1 checks=runtime pass=True
COPY kill  cfg11-pass-mask                    cfg11-pass-mask.json div=(1,1) rc=1 checks=runtime pass=True
COPY accept comment-brace                      comment-brace.json div=- rc=0 checks=- pass=True
COPY accept comment-esac                       comment-esac.json div=- rc=0 checks=- pass=True
COPY accept comment-names-leg                  comment-names-leg.json div=- rc=0 checks=- pass=True
COPY kill  root-keyed-auto-mask               root-keyed-auto-mask.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  root-keyed-auto-zero               root-keyed-auto-zero.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  root-keyed-shape6                  root-keyed-shape6.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  workdir-branch-swap                workdir-branch-swap.json div=(1,0),(0,0) rc=1 checks=runtime pass=True
COPY accept accept-trailing-comments           accept-trailing-comments.json div=- rc=0 checks=- pass=True
COPY kill  cfg00-setup-as-pass                cfg00-setup-as-pass.json div=(0,0) rc=1 checks=runtime pass=True
COPY kill  cfg11-workdir-wording              cfg11-workdir-wording.json div=(1,1) rc=1 checks=runtime pass=True
COPY accept comment-head-comment-quoted-legnames comment-head-comment-quoted-legnames.json div=- rc=0 checks=- pass=True
COPY accept inert-heredoc-apostrophe-comment   inert-heredoc-apostrophe-comment.json div=- rc=0 checks=- pass=True
COPY kill  workdir-branch-keep-swap           workdir-branch-keep-swap.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  workdir-keep-cleanup-nested-config workdir-keep-cleanup-nested-config.json div=(1,1) rc=1 checks=runtime pass=True
C1_R36V2_CONTROL: mode=control tool_present=1 tool_sha=da8c1ef4b30ce4e4 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C1_R36V2_CONTROL_PASS=true
C2_R37_REPIN: counter_sha256=9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53 tool_sha256=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede frozen_predicate_replayed=1 rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C2_R37_REPIN_PASS=true
```

Run 2 is the same 18 lines with `rev=ae9b771ab795fb5b4a6302165d8abdc0a2c6b229`
(and, at its own rev, is the already-committed receipt itself:
`.ufo/evidence/round-37/c2-repin-after.stdout:17-18`).

## Frozen v2 predicate counts — every one matches

Parsed from the run-1 output line (`C1_R36V2_CONTROL:`), against the frozen constants
`.ufo/evidence/round-36/c1/c1-measure-v2.py:63,68-70` and the counter predicate `:538-544`:

| counter | observed | frozen target | match |
|---|---|---|---|
| `pub_kill` | `6/6` | `PUB_KILL_SLOTS_TARGET=6` | yes |
| `pub_accept` | `3/3` | `PUB_ACCEPT_SLOTS_TARGET=3` | yes |
| `pub_slots` | `9` | 6+3 | yes |
| `pub_distinct` | `9` | `PUB_DISTINCT_TARGET=9` | yes |
| `ho_kill` | `4/4` | ≥4 and equals manifest slot count | yes |
| `ho_accept` | `3/3` | ≥2 and equals manifest slot count | yes |
| `ho_invalid` | `0` | `==0` | yes |
| `ho_distinct` | `7` | sealed cardinality (4+3) | yes |
| `sealed_after_freeze` | `1` | `sealed_ok` | yes |
| `runner_sha_ok` | `1` | `PIN_RUNNER` | yes |
| `tool_present` | `1` | required | yes |
| predicate line | `C1_R36V2_CONTROL_PASS=true`, `C2_R37_REPIN_PASS=true` | both true | yes |

Wrapper required-token coverage (`.ufo/evidence/round-37/c2-repin.py:69-72`) checks
`C1_R36V2_CONTROL_PASS=true`, `pub_kill=6/6`, `pub_accept=3/3`, `pub_slots=9`,
`pub_distinct=9`, `ho_kill=4/4`, `ho_accept=3/3`, `ho_invalid=0`, `rev=<resolved>` **and**
counter exit 0 (which is the counter's full `:538-544` predicate). No frozen count is
outside that conjunction.

## Independent re-derivation (not through the counter)

Computed directly from committed bytes at `e6185d5`, with a throwaway script that does not
import the counter:

- public panel `.ufo/evidence/round-35/c1/panel` at rev: 9 JSON specimens,
  6 `set=kill` + 3 `set=accept`, 9 distinct post-edit bodies, 0 edit-count failures;
- sealed set `.ufo/evidence/round-35/c1/sealed` at rev: 7 specimens, 4 kill + 3 accept,
  7 distinct post-edit bodies, 0 edit-count failures;
- sealed `manifest.json` `freeze_rev=d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` equals the
  first-add commit of `.ufo/evidence/round-35/contract.json` at the rev — the provenance gate
  the counter re-checks at `c1-measure-v2.py:490-497` is satisfied by history, not self-declaration;
- `tools/mutate-and-run.sh` at rev hashes to `PIN_RUNNER` `a7d3f2dd…912eb9`.

These independently confirm the slot, cardinality and distinctness counts the counter printed.

## Nuances, risks, holds

- **Control-mode `tool_sha_ok=1` is tautological.** The counter sets
  `tool_sha_ok = a.tool is not None or tool_sha == TOOL_SHA256`
  (`c1-measure-v2.py:462`), and the historical constant is the pre-r37 v3 digest
  `6188db16…d354` (line `:65`), deliberately bypassed per
  `counter-pin.json:10`. The printed `tool_sha_ok=1` is therefore **not** digest evidence; the
  wrapper's own sha256 comparison (`c2-repin.py:49`) is, and it matched `da8c1ef4…93ede`.
- The replay exercises the frozen r36 counter only. C2's primary two-fixture predicate
  (escaped-quote trailing comment blanked; literal hash preserved) is scored by
  `.ufo/evidence/round-37/code-view/measure.py`, outside this seat; the repin cannot
  substitute for it.
- Unsupported-form holds carried by the tool (nested `$(…)`, unquoted backslash-newline,
  parameter-branch quoting) are untouched by this replay and remain holds, not passes.
- Ambient environment carried only `GIT_EDITOR`, `GIT_PAGER`, `GIT_TERMINAL_PROMPT`; the
  wrapper strips all `GIT_*` and pins `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`
  (`c2-repin.py:18-21`), so the result cannot be an ambient-config artifact.
- Ephemeral evidence: `/tmp/r37-repin-exec/{repin.stdout,repin.stderr,repin.exit,repin-ae9b771.*,committed-receipt.stdout}`
  and the clone are under `/tmp` and not durable; the full stdout is preserved verbatim above
  and every hash needed to re-check it is recorded. No tool was installed and no `pacman`
  transaction was run.
