# W2MTV2EmptyAccept — accept-half-emptied public panel: v1 passes vacuously, v2 killed on PUB_ACCEPT_SLOTS_TARGET

## What was attacked

C2's depth surface (round-36 contract, `.ufo/evidence/round-36/contract.json`): the frozen v2 successor
counter `.ufo/evidence/round-36/c1/c1-measure-v2.py` (sha256 `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`)
adds frozen public-slot cardinality + distinctness asserts (6 kill slots / 3 accept slots / 9 distinct
bodies) over the round-35 v1 counter. This probe isolates the **accept half**: the public panel is emptied
of its three accept copies only — the six kill copies stay byte-identical — and both counters are run on
the mutant.

Mutant class (bounded, smallest behavior-bearing point): remove exactly the three public `set: "accept"`
specimens (`comment-brace.json`, `comment-esac.json`, `comment-names-leg.json`) from
`.ufo/evidence/round-35/c1/panel/` at a committed rev. Expected detector: v1's `pub_kill == pub_kill_slots`
∧ `pub_accept == pub_accept_slots` still holds (6==6, 0==0 → vacuous accept → PASS); v2's
`pub_accept_slots == PUB_ACCEPT_SLOTS_TARGET` (3) fails (0≠3) → `C1_R36V2_PASS=false`.

## Preconditions verified (read-only)

- Lane tip at clone time: `fbb01cf46f8437fd1264c1a3acc053c882fa2164` ("round-36 verifier spot-check …"), the parent of the mutant commit.
- Frozen pins matched at source and again at the mutant rev via `git show`:
  `tools/tally-audit-v3.py` = `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354`;
  `tools/mutate-and-run.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`;
  `.ufo/evidence/round-36/c1/c1-measure-v2.py` = `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`.
- Sealed set at the mutant rev: 4 kill + 3 accept, `manifest.json freeze_rev=d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`,
  which is the commit that first added `.ufo/evidence/round-35/contract.json` and is an ancestor of the mutant rev (verified in-clone).
- No tool installs (system `git`, system `python3`); no `pacman` use.

## Mutant commit

Scratch clone: `/fast/scratch/hyaku/tameshi-r36-seats/W2MTV2EmptyAccept/lane`
(`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin <clone>`).

```
git -C <clone> rm -q .ufo/evidence/round-35/c1/panel/comment-brace.json \
                   .ufo/evidence/round-35/c1/panel/comment-esac.json \
                   .ufo/evidence/round-35/c1/panel/comment-names-leg.json
git -C <clone> -c user.name='W2MTV2EmptyAccept' \
               -c user.email='w2mtv2-empty-accept@tameshi-shokunin.local' \
               commit -q -m 'empty-accept mutant: remove the three public accept copies (6 kill kept, zero accept slots) — W2MTV2EmptyAccept'
```

- Mutant rev: **`74154e9afa3d00f07898af2d8573aa42d84a5cdb`**, single commit on parent `fbb01cf46f8437fd1264c1a3acc053c882fa2164`.
- Rev-to-rev delta (`git diff --name-status fbb01cf 74154e9`): exactly three `D` lines for the accept panel
  files; `--shortstat` = `3 files changed, 45 deletions(-)`. No other path differs, so the ONLY delta between
  pristine and mutant bytes is the accept half of the public panel.
- Panel at mutant rev (`git ls-tree -r --name-only 74154e9 -- .ufo/evidence/round-35/c1/panel`): the six kill
  files `cfg00-accept-swap.json`, `cfg11-pass-mask.json`, `root-keyed-auto-mask.json`,
  `root-keyed-auto-zero.json`, `root-keyed-shape6.json`, `workdir-branch-swap.json`.

## Exact commands run (both counters are the frozen canonical files, never copied or edited)

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r36-seats/W2MTV2EmptyAccept/lane \
  --rev <REV> --work <fresh empty dir> --sealed .ufo/evidence/round-35/c1/sealed

python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/c1/c1-measure-v2.py \
  --lane /fast/scratch/hyaku/tameshi-r36-seats/W2MTV2EmptyAccept/lane \
  --rev <REV> --work <fresh empty dir> --sealed .ufo/evidence/round-35/c1/sealed
```

Revisions run:
- **pristine**: `REV=fbb01cf46f8437fd1264c1a3acc053c882fa2164` (v1 and v2)
- **mutated**: `REV=74154e9afa3d00f07898af2d8573aa42d84a5cdb` (v1 and v2)
- **restored**: clone `git reset --hard fbb01cf46f8437fd1264c1a3acc053c882fa2164`, then v1 and v2 again.

Each `--work` was a freshly created empty directory (`work-pristine-v1`, `work-pristine-v2`, `work-mutant-v1`,
`work-mutant-v2`, `work-restored-v1`, `work-restored-v2`) — the counters abort on non-empty work. Runs that
share `/tmp/tally-audit-explicit` are safe here because that literal is only a root *string* in the tally-block
triples (the block's `rm -rf "$root"` executes only under the auto/`KEEP=0` triple, whose root is a per-process
`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`). Wall times: pristine v1 185 s; pristine v2 + mutant v1
concurrent 167 s; mutant v2 135 s; restored v1+v2 concurrent 155 s.

## Captured predicate lines (verbatim)

Pristine `fbb01cf` — v1 (exit 0) **PASS**:

```
C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=fbb01cf46f8437fd1264c1a3acc053c882fa2164 C1_R35_PASS=true
```

Pristine `fbb01cf` — v2 (exit 0) **PASS**:

```
C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=fbb01cf46f8437fd1264c1a3acc053c882fa2164 C1_R36V2_PASS=true
```

Mutant `74154e9` — v1 (exit 0) **PASS (vacuous accept)**:

```
C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=0/0 pub_slots=6 pub_distinct=6 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=74154e9afa3d00f07898af2d8573aa42d84a5cdb C1_R35_PASS=true
```

Mutant `74154e9` — v2 (exit 1) **FAIL**:

```
C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=0/0 pub_slots=6 pub_distinct=6 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=74154e9afa3d00f07898af2d8573aa42d84a5cdb C1_R36V2_PASS=false
```

Restored `fbb01cf` — v1 (exit 0) and v2 (exit 0), byte-identical to the pristine predicate lines
(`diff` of the grepped lines: `v1_line_identical`, `v2_line_identical`):

```
C1_R35:   ... pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ... rev=fbb01cf46f8437fd1264c1a3acc053c882fa2164 C1_R35_PASS=true
C1_R36V2: ... pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ... rev=fbb01cf46f8437fd1264c1a3acc053c882fa2164 C1_R36V2_PASS=true
```

## Which frozen assert killed it

Constants parsed from the frozen v2 source, evaluated against the mutant's observed counts
(`pub_kill_slots=6, pub_accept_slots=0, pub_kill=6, pub_accept=0, pub_distinct=6`):

| v2 conjunct | verdict |
|---|---|
| `pub_kill_slots == PUB_KILL_SLOTS_TARGET` (6) | HOLDS (6==6) |
| `pub_accept_slots == PUB_ACCEPT_SLOTS_TARGET` (3) | **FALSE (0≠3)** |
| `pub_kill == PUB_KILL_SLOTS_TARGET` (6) | HOLDS (6==6) |
| `pub_accept == PUB_ACCEPT_SLOTS_TARGET` (3) | **FALSE (0≠3)** |
| `pub_distinct == PUB_DISTINCT_TARGET` (9) | **FALSE (6≠9)** |

v1's two public conjuncts on the same counts both hold (`6==6`, `0==0`), which is exactly the vacuous-accept
hole: emptying the accept half makes a component that scores nothing look complete. The targeted assertion —
the accept-slot cardinality `PUB_ACCEPT_SLOTS_TARGET=3` — is falsified (`pub_accept=0/0`), and the
distinctness assert falls as a byproduct (three distinct accept bodies removed: 9→6). All kill-side asserts
still hold at 6/6, so the kill half is not what v2 caught.

Per-copy detail at the mutant rev (v1 and v2 emitted the same 13 COPY lines — 6 public kill + 7 sealed):

```
COPY kill  cfg00-accept-swap                  cfg00-accept-swap.json div=(0,0) rc=1 checks=runtime pass=True
COPY kill  cfg11-pass-mask                    cfg11-pass-mask.json div=(1,1) rc=1 checks=runtime pass=True
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
```

Pristine and restored runs emitted the same 13 lines plus the three removed public accept copies
(`comment-brace`, `comment-esac`, `comment-names-leg`, each `div=- rc=0 pass=True`) — 16 COPY lines.

## Restoration evidence

- `git reset --hard fbb01cf46f8437fd1264c1a3acc053c882fa2164` in the scratch clone; `git status --porcelain` = 0 lines.
- Tree identity: clone `HEAD^{tree}` = `049acfb928866c808ed061a5b5c1fa1ee86349dd` = source lane
  `rev-parse fbb01cf^{tree}` = `049acfb928866c808ed061a5b5c1fa1ee86349dd` — exact bytes restored.
- Restored accept blobs match their pre-mutation sha256 (recorded before the mutant commit and again after restore):
  `comment-brace.json` `8fbf2436fce2172dda4485851b838ec036ee10e242b0dfe7df4c38d08b8e9f33`,
  `comment-esac.json` `2f10fb95d209f9c2a9492282424fe764b8c5e1b2e0c5e6d5a81deb6c2e25b276`,
  `comment-names-leg.json` `e39a524babea863f918cd531ad834b81ca700b997492933f847ad592ed183a5a`.
  At the mutant rev these three blobs are absent from the panel tree and nothing else changed.
- The mutant commit object `74154e9` remains reachable in the scratch clone (`git cat-file -t` = commit) for
  re-reading; the source lane was never modified: its HEAD is still
  `fbb01cf46f8437fd1264c1a3acc053c882fa2164` and its only status entries are the pre-existing untracked
  `.ufo/waves/round-36/w1/`, `.ufo/waves/round-36/w2/` report dirs.

## Verdict

VERDICT: **MUTANT KILLED** — at mutant commit `74154e9afa3d00f07898af2d8573aa42d84a5cdb` (parent = lane tip
`fbb01cf`, delta = deletion of the three public accept copies only), the frozen v1 counter prints
`C1_R35_PASS=true` (exit 0; `pub_kill=6/6 pub_accept=0/0 pub_distinct=6` — accept half scored vacuously),
while the frozen v2 counter prints `C1_R36V2_PASS=false` (exit 1; same counts), falsifying
`PUB_ACCEPT_SLOTS_TARGET` (3 vs `pub_accept_slots=0`) and, as byproducts, `pub_accept==3` and
`PUB_DISTINCT_TARGET` (9 vs 6). Sealed set and all kill-side asserts stayed green in every run
(`ho_kill=4/4 ho_accept=3/3 ho_invalid=0 sealed_after_freeze=1`, pins `tool_sha_ok=1 runner_sha_ok=1`), and the
restored-bytes runs reproduce the pristine predicate lines byte-for-byte. No defect found in either counter;
v2's accept-slot cardinality assert demonstrably closes the vacuous-accept path for the accept half.
