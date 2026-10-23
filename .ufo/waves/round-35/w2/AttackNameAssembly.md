# AttackNameAssembly — twice-only head rule: runtime-assembled leg names and a comment-blanking desync

Round 35 / wave 2 / seat `AttackNameAssembly` (leaf, no subagents). Lane tip at dispatch
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. All work under
`/fast/scratch/hyaku/tameshi-r35-seats/AttackNameAssembly/`; the lane checkout was never written.

**Verdict in one line.** The twice-only head rule is a substring count, not a dataflow rule. Two
independent bypasses survive `tools/tally-audit-v3.py` at the pin: a **runtime-assembled leg
name** (shared with v2 — a fail-open BOUND) and a **`$'…\'` quote desync in `code_view` that hides
real head code as a "comment"** — that one v2 KILLS and v3 ACCEPTS, i.e. a **CRITICAL regression
introduced by round-35 fix 3**. Both change the runner's verdict from FAIL/SETUP to PASS while the
audit prints `TALLY_AUDIT: PASS`.

## Artifacts (sha256, read-only, matched the freeze)

| file | sha256 |
|---|---|
| `tools/mutate-and-run.sh` (runner) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` |
| `tools/tally-audit-v2.py` (control) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` |
| pristine copy of the runner = runner bytes | `a7d3f2dd…` (same) |

Lane cleanliness after the run: `git -C lane status --porcelain` → empty. Tool installs: **none needed**.

## The surface being attacked (why the head is the blind spot)

- `check_head` blanks comments with `code_view` then, for each leg name, requires
  `head_code.count(nm) == 2` (`tools/tally-audit-v3.py:453-461`). The docstring asserts this
  "catches them all", explicitly naming `printf -v`, `eval`, `declare` (:455-457).
- `check_runtime` never executes the head: it extracts only the tally block and synthesises the
  leg statuses as function arguments (`run_vectors`, :376-410). A head edit is therefore invisible
  to the runtime oracle, by construction.
- The runner's own `--selftest` tally harness also extracts only the block
  (`mutate-and-run.sh:1994-1995`), so it cannot see a head edit either.
- The C1 public panel has **no head *kill* specimen**. Seven of the eight JSONs edit only
  tally-block text (`cfg00-accept-swap`, `cfg11-pass-mask`, `comment-brace`, `comment-esac`,
  `root-keyed-auto-mask`, `root-keyed-auto-zero`, `workdir-branch-swap`); the eighth
  (`comment-names-leg`, accept) inserts the inert comment `# st_js is captured immediately above`
  after the capture — the round-35 false-kill case, not a mask. The only head **kill** coverage in
  the apparatus is v3's own selftest, whose two head seeds are **literal** spellings
  (`st_kagi=$(($? & 127))` :762, `st_claims=0` :768).

So the head rule is guarded by one text scan, and that scan is the only barrier. Both findings
below walk through it.

## Method (bounded behavioural detector)

`work/headprobe.sh` (sha256 `06bc6e7fce700397bc6fa198a81c918265af54de4faa8602fa3b982ffbff12a0`) extracts `run_regression` verbatim from a
runner copy (first `^run_regression() {$` to the next `^}$`, i.e. lines 1345-1471), stubs **only**
the nine `regression_case_git` leg invocations (each returns a configured status), pins
`SELF=/stub/runner` and normalises the auto root and the date, then runs the real head + the real
tally block. Every runner copy is audited by **both** tools and swept over the four (auto,KEEP)
triples and the vectors `all-zero`, `one-1`, `one-2`, `one-3`, `one-255`, `mixed-a`, `mixed-b`.

The detector was validated in both directions: an inert decoy edit (`st_jjs`, see HYGIENE-1) shows
SAME on every vector, while real masks diverge exactly where their masked leg is non-zero.

## CRITICAL-1 — round-35 fix 3 regression: v2 KILLS, v3 ACCEPTS, behavior diverges

**Mutant** (one line, 25 bytes, inserted at runner line 1431, between `st_citecheck=$?` (:1430) and
`local nlegs=` (:1432)):

```sh
  : $'x\' # y' ; st_js=0
```

Copy sha256 `0fa2152dc898220f488798ed8b56b7fa5b4bad5c0ad5903939f519a707dc53de`.
`bash -n` rc 0.

**Why bash executes it.** `$'x\'` is ANSI-C quoting whose `\'` is a literal apostrophe; the string
runs on through ` # y` and closes at the next `'`. The `#` is **inside the string**, so
`st_js=0` after the `;` is real code. The runner's `st_js` is overwritten to 0.

**Why v3 does not see it.** `code_view` (:150-196) has no `$'…'` case: it opens a quote at `'`
(:181), closes it early at the escaped apostrophe, then hits `#` at word start and blanks the rest
of the line. Trace on the inserted line:

```
RAW "  : $'x\\' # y' ; st_js=0"
CV  "  : $'x\\'               "     # `; st_js=0` is blanked as if it were a comment
```

Counts for the masked leg: raw head `st_js` = 3, code view = 2 → the twice-only rule passes.

**Tool verdicts on identical bytes:**

```
$ python3 /fast/.../lane/tools/tally-audit-v3.py --runner .../copies/mut_ansic_clean.sh
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
exit 0

$ python3 /fast/.../lane/tools/tally-audit-v2.py --runner .../copies/mut_ansic_clean.sh
CHECK head FAIL legs=9; leg st_js appears 3 times in the head (want exactly 2: ...)
...
TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)
exit 1
```

v2's kill is a true positive on exactly the masked leg: in this copy the third `st_js` occurrence
is the real `st_js=0` (the string contains no leg name; raw `st_kagi` = 2). **A class v2 caught and
v3 now accepts — the regression the tasking asked for.**

**Behavioural divergence** (`headprobe.sh`, same bytes, same inputs):

```
leg js-kimi-census=1, auto, KEEP=0
pristine  exit 1  REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)   workdir present
mutant    exit 0  REGRESSION: PASS (cases=9 passed=9; ledger legs exact: ...) workdir absent
```

Divergence matrix for this copy (7 vectors × 4 configs, 2 repetitions, identical each time):
`one-1` and `mixed-a` DIVERGE in all four triples; `all-zero`, `one-2`, `one-3`, `one-255`,
`mixed-b` SAME (only `st_js` is masked, so only vectors with `st_js≠0` move). The all-pass control
is byte-identical: pristine and mutant stdout sha256 `96ca41b5d45a10f11e29608d264220a9f01661644db0f4ccba1d9698e88d526e`.

**Rank: CRITICAL** — a claim in the frozen tool is false. Fix 3 says the structural scans now run
on a "quote-aware code view" so that comment text is never code (:150-196, docstring :23-28); in
fact `code_view` misclassifies **real code** as comment, and the twice-only rule that round 35
kept as its head barrier is defeated by a 25-byte line. This is a false negative on the kill side
introduced by the round-35 fix.

## CRITICAL-2 — runtime-assembled leg names: both tools accept, behaviour diverges

The same insertion point (:1431) with a name assembled at run time. The head text never contains a
full `st_<leg>` token, so **both** v2 and v3 pass `CHECK head`:

| insertion | bytes | v3 | v2 | effect |
|---|---|---|---|---|
| `for n in js kagi tsu mado checklist claims roundgate sourcescheck citecheck; do printf -v "st_$n" 0; done` | 108 | PASS | PASS | all 9 legs zeroed |
| `… do eval "st_$n=0"; done` | 103 | PASS | PASS | all 9 legs zeroed |
| `… do declare -n ref="st_$n"; ref=0; done` | 118 | PASS | PASS | all 9 legs zeroed |
| `p=st_ n=js; (( ${p}${n} = 0 ))` | 33 | PASS | PASS | `st_js` zeroed (arithmetic indirect) |
| `n=js; printf -v "st_$n" 0` | 28 | PASS | PASS | `st_js` zeroed |
| `n=s;printf -v st_j$n 0` | 25 | PASS | PASS | `st_js` zeroed |
| `n=js;eval "st_$n=0"` (cheapest found) | 22 | PASS | PASS | `st_js` zeroed |

Copy hashes: `mut_runtime_name` `f6b2a443…`, `mut_eval` `d1ba7f6f…`, `mut_declare_n` `12c247de…`,
`mut_arith` `a25df35e…`, `mut_single_leg` `2009ec1d…`, `mut_cheap2` `18d2b5bf…` (full hashes in the
command log). All `bash -n` rc 0.

**Tool verdict** on `mut_runtime_name` and `mut_cheap2` (v3 shown; v2 is identical except `vectors=15158`):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS   (v3 exit 0; v2 exit 0)
```

**Behavioural divergence** (full mask `mut_runtime_name`: all four configs, every non-zero vector
DIVERGE; `all-zero` SAME; e.g. `one-1` pristine `FAIL passed=8 failed=1` exit 1 → mutant `PASS
passed=9` exit 0, and the auto workdir flips from kept to removed). Single-leg variant `mut_cheap2`
(25 bytes) diverges on `one-1` and `mixed-a` in all four triples, SAME elsewhere; the same
`leg js-kimi-census=1` record as CRITICAL-1:

```
pristine exit 1  REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
mutant   exit 0  REGRESSION: PASS (cases=9 passed=9; ledger legs exact: ...)
```

**Rank: CRITICAL (false claim), pre-existing (not a v2→v3 regression).** The tool's own docstring
at `tools/tally-audit-v3.py:455-457` states that `printf -v`, `eval` and `declare` occurrences of a
leg "rewrite the captured status and fails closed here … substring counting catches them all."
That is false for every dynamically assembled name above: the count stays at 2 because the full
token never appears in the head. v2 accepts the same copies, so this is a shared fail-open BOUND on
the head rule rather than a regression — but it directly contradicts the frozen tool's stated
guarantee, which is why it is ranked CRITICAL and not BOUND. The cheapest demonstrated bypass is
22 bytes (`n=js;eval "st_$n=0"` at :1431; v3 `TALLY_AUDIT: PASS` exit 0, v2 `PASS` exit 0, and
`js-kimi-census=1` flips pristine `FAIL (passed=8 failed=1)` exit 1 to mutant `PASS (passed=9)` exit 0).

## BOUND-1 — reverse desync: v3 false-kills a behaviourally pristine copy

The same `$'…\'` desync runs the other way too. With

```sh
  x=$'\''
  # st_kagi is captured above
```

`code_view` leaves a quote open at the end of the first line (trace: both lines are passed through
unchanged), so the **inert comment** on the next line is counted as code:

```
CHECK head FAIL legs=9; leg st_kagi appears 3 times in the head (want exactly 2: ...)
TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)   # v3 exit 1
```

v2 also fails it (`head` FAIL, exit 1), so this is **not** a v2→v3 regression; but the copy is
behaviourally identical to pristine on **28/28** combos (4 configs × 7 vectors: 0 divergent combos,
verified), i.e. it is a valid *accept* specimen that both tools reject. It falsifies the docstring's
accept-side promise that "comment text cannot … refuse a behaviourally pristine copy"
(`tools/tally-audit-v3.py:150-167`, `code_view` docstring). Rank **BOUND** (fail-closed), with the note that if such a copy
were authored into the sealed accept set it would fail C1's accept count.

## BOUND-2 — the C1 counter cannot see head divergence at all

`c1-measure.py`'s behaviour oracle is `tally_block()` (:132) + `leg_names(head)` (:159), i.e. it
executes **only the tally block**; `behavior()` (:204) never runs the head. Empirically, on
pristine vs the CRITICAL-1 copy:

```
head edit diverged configs per c1.behavior(): []      # block behavior identical: True
tally_block identical pristine vs mutant: True
```

Consequently `score_copies` (:285-316) computes `row['valid'] = bool(div)` = False for any head
kill specimen and prints `INVALID: kill copy without behavioural divergence`. The sealed-authoring
rule ("a kill specimen must diverge under at least one triple") therefore cannot express this class:
it is scored invalid, never "survived". The measurement apparatus, not just the tool, is head-blind.
(The counter also carries its own copy of `code_view` at `c1-measure.py:95` with the identical
`$'…\'` desync, so it would inherit CRITICAL-1 if it ever ran on head bytes.)

This is why the finding above must be scored with a head-aware detector such as
`work/headprobe.sh`; the panel/sealed route cannot produce it.

## HYGIENE

- **HYGIENE-1 — inert decoy (control, correctly accepted).** `n=s;printf -v st_j$n 0` with
  `n=js` forms `st_jjs`; the copy (`mut_cheap.sh`, `c7f7ba06…`) is behaviourally identical (SAME on
  28/28 combos) and v3 PASS is the right verdict. It is kept as the discriminator that proves the
  divergence results are behavioural, not textual.
- **HYGIENE-2 — duplicated parser.** `c1-measure.py:95` re-implements `code_view` with the same
  `$'…\'` handling; any fix to `tally-audit-v3.py:150-196` must be mirrored there or the counter
  and the tool will disagree on the same bytes.
- **HYGIENE-3 — thin head coverage.** The public panel's single head specimen is an inert comment
  (`comment-names-leg.json`, accept); there is no head kill specimen, and v3's selftest seeds the
  head only with literal spellings (:762, :768). The head rule is therefore exercised far less than
  the block rule; a sealed head kill specimen is the natural way to keep it honest (with the
  BOUND-2 caveat about the counter's oracle).

## What I could NOT break (bounded negatives, with proof)

1. **Literal leg-name occurrences of every spelling are still killed.** Inserting each of
   `printf -v st_js 0`, `eval "st_js=0"`, `declare -n r=st_js; r=0`, `(( st_js = 0 ))` at :1431 gives
   v3 `CHECK head FAIL legs=9; leg st_js appears 3 times in the head …`, `TALLY_AUDIT: FAIL`, exit 1
   (four separate runs, `out/v3-lit_*.out`). The twice-only rule works exactly as documented for
   static text; only runtime construction escapes it.
2. **A behaviourally inert head edit is still accepted (correctly).** `n=s;printf -v st_j$n 0` as
   first written by me formed `st_jjs` (an unused variable), not `st_js`; v3 PASS, and the detector
   showed SAME on all 28 combos. Recorded as a control: the sweep distinguishes a real mask from a
   typo, and v3's acceptance there is correct.
3. **The block-level checks were not moved.** `static`, `runtime` and `harness` all pass on every
   head mutant because the head is outside their inputs (that is the gap, not a break). No attempt
   was made to reopen A4/A5 through the block; that is other seats' surface.
4. **No runner bytes were changed.** The runner copy used for measurement is byte-identical to the
   pin (`a7d3f2dd…`) and `runner_sha_ok` is unaffected.

## Restoration evidence (mutate → detect → restore)

Single scratch file `work/probe-target.sh`, same detector and tool on pristine, mutated and
restored bytes:

| step | sha256 | all-zero (auto,KEEP=0) | js=1 (auto,KEEP=0) | v3 |
|---|---|---|---|---|
| pristine | `a7d3f2dd…` (frozen) | exit 0 PASS, root absent, stdout `96ca41b5…` | exit 1 FAIL, root present, stdout `2ddecade…` | PASS |
| mutated (+25 B) | `0fa2152d…` | exit 0 PASS, root absent, stdout `96ca41b5…` | **exit 0 PASS**, root absent, stdout `e6a49be5…` | **PASS** |
| restored | `a7d3f2dd…` | exit 0 PASS, root absent, stdout `96ca41b5…` | exit 1 FAIL, root present, stdout `2ddecade…` | PASS |

`pristine == restored` byte-for-byte (`a7d3f2dd…`), all detector outputs identical, and the restored
bytes `cmp`-equal the lane runner. No lane path was written; `git status --porcelain` empty.

## Security/scope

No writes inside `.git`, the lane, the fleet repo, sibling lanes or `.ufo/state/`. Scratch copies
only under `/fast/scratch/hyaku/tameshi-r35-seats/AttackNameAssembly/{lane(read-only),copies,work,out}`.
No mutating git/jj commands, no network, no installs.

## Suggested follow-ups for L1 (not performed here)

- If a sealed **kill** specimen of the CRITICAL-1 class is wanted, the copy bytes are reproduced by
  inserting the single line above at :1431; but note BOUND-2: the C1 counter will mark it INVALID
  unless the counter's behavior oracle is extended to the head.
- The head check needs either a real shell parser or a dataflow check; a text scan cannot close
  runtime name construction. The docstring sentence at :455-457 should not be relied on as-is.
- `code_view` needs `$'…'` handling (and command-substitution/backtick quote stacks); until then
  both `tally-audit-v3.py` and `c1-measure.py` share the desync.

## Appendix A — artifact hashes (all under `/fast/scratch/hyaku/tameshi-r35-seats/AttackNameAssembly/`)

| artifact | sha256 |
|---|---|
| `copies/pristine.sh` (= lane runner) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `copies/mut_ansic_clean.sh` | `0fa2152dc898220f488798ed8b56b7fa5b4bad5c0ad5903939f519a707dc53de` |
| `copies/mut_runtime_name.sh` | `f6b2a44347c64117a372f4a1a76deb381261c24e43817e7f4f524f7de6eeabd0` |
| `copies/mut_eval.sh` | `d1ba7f6fa37607b994519fbbb3782ae50ae9d931731ba5328a38dc8baaf4c102` |
| `copies/mut_declare_n.sh` | `12c247de582d659ec4182fbd35ceac29c544a6392073060a55800b18fc26f77c` |
| `copies/mut_single_leg.sh` | `2009ec1d5d7bd3ba841769876fd5fdf850376c7a0fb4403b2a1963f7032fc146` |
| `copies/mut_cheap2.sh` | `18d2b5bfae1ab1577d222e859e1d486cfd0a212b13f24a7b7c13d128d1643eed` |
| `copies/mut_cheap_eval.sh` | `22ff4dee7176bab9ce95d401a68942aa9bee029f6ec97af978d3ca43afec0232` |
| `copies/mut_cheap_arith.sh` | `61467bf3cfec220cebd7e909bf4b4637766ac3774b7f3357b90396eaf9a17d5d` |
| `copies/mut_arith.sh` | `a25df35edad4375e3518e3624ebd8f52c59a0b97026b981629dbac1b7daa708f` |
| `copies/pristine_desync_falsekill.sh` | `9686ee6c586042650a5b5d1d09f75c2fff032c121c1d82cb88e21741fb143359` |
| `copies/mut_cheap.sh` (inert decoy `st_jjs`) | `c7f7ba06b20b618d819cc3160db2b8c7d0663ca87d518a7650d957c8918812a3` |
| `copies/lit_printfv.sh` | `c1ca0a4a0469d8327ffd01b717f86948e7283495a3c8f2b33b0dab6df4889884` |
| `copies/lit_eval.sh` | `057ebc10f8df72b0c716e33cb84a900d0cec9914cf94b68b75451f5b8d9bc182` |
| `copies/lit_declare.sh` | `5ff4acde99c118fe0112d404e79574f44b1a9f73e7fafb425e1bb53e1ac403ac` |
| `copies/lit_arith.sh` | `656ad76abedcf4aeffbeaccafe6bd644f2cfa00e8d6bb1d7bd1ab6538b33c4a1` |
| `work/headprobe.sh` (detector) | `06bc6e7fce700397bc6fa198a81c918265af54de4faa8602fa3b982ffbff12a0` |
| `work/probe-target.sh` before/after restore | `a7d3f2dd…` / `a7d3f2dd…` (mutant `0fa2152d…`) |

## Appendix B — exact commands and exit codes

Run from `/fast/scratch/hyaku/tameshi-r35-seats/AttackNameAssembly/`:

```
python3 lane/tools/tally-audit-v3.py --runner copies/pristine.sh                 exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/pristine.sh                 exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v3.py --runner copies/mut_ansic_clean.sh          exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/mut_ansic_clean.sh          exit 1  CHECK head FAIL (st_js 3)
python3 lane/tools/tally-audit-v3.py --runner copies/mut_runtime_name.sh         exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/mut_runtime_name.sh         exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v3.py --runner copies/mut_eval.sh                 exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/mut_eval.sh                 exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v3.py --runner copies/mut_declare_n.sh            exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/mut_declare_n.sh            exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v3.py --runner copies/mut_single_leg.sh           exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/mut_single_leg.sh           exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v3.py --runner copies/mut_cheap2.sh               exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/mut_cheap2.sh               exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v3.py --runner copies/mut_cheap_eval.sh          exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/mut_cheap_eval.sh          exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v3.py --runner copies/mut_arith.sh                exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v2.py --runner copies/mut_arith.sh                exit 0  TALLY_AUDIT: PASS
python3 lane/tools/tally-audit-v3.py --runner copies/pristine_desync_falsekill.sh exit 1 CHECK head FAIL (st_kagi 3)
python3 lane/tools/tally-audit-v2.py --runner copies/pristine_desync_falsekill.sh exit 1 CHECK head FAIL (st_kagi 3)
python3 lane/tools/tally-audit-v3.py --runner copies/lit_printfv.sh              exit 1  CHECK head FAIL (st_js 3)
python3 lane/tools/tally-audit-v3.py --runner copies/lit_eval.sh                 exit 1  CHECK head FAIL (st_js 3)
python3 lane/tools/tally-audit-v3.py --runner copies/lit_declare.sh              exit 1  CHECK head FAIL (st_js 3)
python3 lane/tools/tally-audit-v3.py --runner copies/lit_arith.sh                exit 1  CHECK head FAIL (st_js 3)
```

Detector invocation:

```
bash work/headprobe.sh copies/<copy>.sh '<CASE=STATUS[,CASE=STATUS...]>' <KEEP> <auto|explicit> [workdir]
```

`CASE` is the runner's regression case name (`js-kimi-census`, `bash-surface-census`,
`bash-tsukuroi-census`, `bash-mado-verify`, `bash-checklist-run`, `js-claims-check`,
`js-round-gate`, `js-sources-check`, `js-cite-check`); omitted cases default to 0.
`SELF` is pinned to `/stub/runner` inside the detector so the tool line is comparable.

## Appendix C — normalization and detector-validation note

- `stdout sha256` values in the restoration table are over **normalized** stdout: auto root
  `/tmp/tameshi-r4-2-regression.XXXXXX` → `<ROOT>`, `REGRESSION_DATE` → `D`, `SELF` → `/stub/runner`.
  Raw stdout differs between runs only in those fields.
- One early sweep cell reported `all-zero` as DIVERGE for `mut_cheap2` in auto mode. Rerun five
  times plus a direct byte diff: identical 5/5. It was a detector-normalization artifact of that
  single sweep, not runner behaviour; the reproducible matrix (two full repetitions × four
  configs × seven vectors) is the one in CRITICAL-1/2.
- The inert decoy (`mut_cheap.sh`, masks the never-read `st_jjs`) is accepted by v3 on all checks
  and shows SAME on every vector — correct behaviour, and the control that proves the sweep
  separates a real mask from a spelling slip.
