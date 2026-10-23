# ResidueGuard2Divisibility — round-34 w1 seat report

Seat: `tameshi-r34-w1-ResidueGuard2Divisibility` (mutation tester, leaf). Scope: the routed
measurement-only probe of the r32 **Guard-2 divisibility** class against the frozen detector
`tools/tally-audit-v2.py` (C1, MEASURED TRUE at `c17e593b51802dd4ed568da3265f21c6d00c4273`,
lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`). No tool/runner edits were made or proposed
as landed work; every write landed in
`/fast/scratch/hyaku/tameshi-r34-seats/ResidueGuard2Divisibility/` except this report.

## Verdict (measured, not predicted)

- **15-member `%`-guard family: 10 killed, 5 survived, 0 inconclusive.**
- Baseline (pristine bytes) audit PASS exit 0; restored bytes re-audited after the family,
  PASS exit 0, byte-identical (`cmp` exit 0).
- **The five survivors are exactly the predicates that agree with `!= nlegs` on the only counts
  the detector exercises ({8, 9, 10}).** Every divergence count for every survivor lies outside
  that domain (executed map below: `18,27` for the literal r32 predicate; odd≠9 for the parity
  members; multiples of 3≠9 for `% 3`).
- The **literal r32 Guard-2 predicate alone survives** (`% nlegs != 0` → tool exit 0). The
  **r32 copy as sealed** (predicate + its 18-operand witness loop) **is killed** (static +
  runtime, exit 1) — so C1's landed receipt is not falsified; the gap is the predicate in
  isolation, and it is invisible on **both** detector axes (runtime sweep counts and the runner's
  own harness: harness probe ACCEPTS the divisibility block, REJECTS the guard-removed control).
- No defect was found in the landed measurement chain. This is a coverage finding, not a
  contract change.

## Setup and pins (every command's exit captured with `; echo $? > file`)

```
S=/fast/scratch/hyaku/tameshi-r34-seats/ResidueGuard2Divisibility
mkdir -p $S
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/lane          # clone.exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $S/lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                          # checkout.exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $S/lane rev-parse HEAD
                                                                   # 0b99d48e…68b7, revparse.exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $S/lane show 0b99d48e…:tools/tally-audit-v2.py > $S/tool.py        # show-tool.exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $S/lane show 0b99d48e…:tools/mutate-and-run.sh  > $S/pristine.sh   # show-runner.exit=0
sha256sum $S/tool.py $S/pristine.sh
```

| artifact | sha256 | expected pin | match |
|---|---|---|---|
| `tool.py` (from tip) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | `7b11ba25…8d10` | YES |
| `pristine.sh` (from tip) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `a7d3f2dd…2eb9` | YES |
| live lane `tools/tally-audit-v2.py` | `7b11ba25…8d10` | same | YES |
| live lane `tools/mutate-and-run.sh` | `a7d3f2dd…2eb9` | same | YES |
| counter `.ufo/evidence/round-33/c1/c1-measure.py` (hash only, never executed) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | `f6b8868c…a07f28c` | YES |

Deciding-run receipt read at tip (not re-executed): `.ufo/evidence/round-34/measure/c1-deciding-run.exit`
= `0`; stdout verbatim `C1_R33: … ho_kill=8/8 … C1_R33_PASS=true` (matches the dispatch text).
Lane left clean: `git -C $S/lane status --porcelain` → 0 lines, exit 0.

## Detector and baseline

Detector = the frozen tool, unmodified, run as a subprocess against a **copy** of the runner:

```
python3 tool.py --runner <copy>    # 0 = survived (audit PASS), 1 = killed (audit FAIL), 2 = cannot audit
cp pristine.sh copies/base.sh
python3 tool.py --runner copies/base.sh > out/base.stdout; echo $? > out/base.exit
```

`out/base.exit` = `0`; stdout:

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

The detector's count domain is derivable from its own output: 15,158 = 2×(256 + 8×256 + 55 + 18
+ 5,184) + 2×(9 positions × 2 stress kinds) = 2×7,561 + 36. The 7,561 one-config vectors all
carry nine statuses (`tally_block` loop, `run_vectors`), and the 36 stress runs are one-operand
dup/drop, i.e. counts **10 and 8** (`with_operands`, `check_runtime`). No other count is ever fed
to the completeness guard.

## Family (single anchored edit per copy, anchor count asserted == 1)

Anchors on `pristine.sh` (each occurs exactly once): sum guard line 1456
`  if (( npass + nfail + nsetup != nlegs )); then`; FAIL guard line 1441
`  if [[ $nfail -gt 0 ]]; then`; SETUP guard line 1447 `  if [[ $nsetup -gt 0 ]]; then`.
Driver: `python3 family.py > out/family.summary; echo $?` → `0` (full JSON: `out/family.json`).

| # | member | substituted predicate | exit | verdict | runtime mismatch (first observed) |
|---|---|---|---|---|---|
| 1 | `guard-mod-nlegs` | `(npass+nfail+nsetup) % nlegs != 0` — **literal r32 Guard-2** | 0 | **survived** | 0 |
| 2 | `guard-mod2-odd` | `… % 2 != 0` | 1 | killed | 56; all-pass → SETUP `counted=9`, want PASS |
| 3 | `guard-mod2-even` | `… % 2 == 0` | 0 | **survived** | 0 |
| 4 | `guard-mod3-nonzero` | `… % 3 != 0` | 0 | **survived** | 0 |
| 5 | `guard-mod-nlegs-eq0` | `… % nlegs == 0` | 1 | killed | 56; all-pass → SETUP `counted=9`, want PASS |
| 6 | `guard-parity-eq` | `… % 2 == nlegs % 2` | 1 | killed | 56; all-pass → SETUP `counted=9`, want PASS |
| 7 | `guard-parity-ne` | `… % 2 != nlegs % 2` | 0 | **survived** | 0 |
| 8 | `guard-even-and-ne` | `… % 2 == 0 && … != nlegs` | 0 | **survived** | 0 |
| 9 | `guard-odd-and-ne` | `… % 2 != 0 && … != nlegs` | 1 | killed | 36; stress dup operand 0 → PASS `passed=10`, want SETUP `counted=10` |
| 10 | `fail-odd-only` | `$nfail -gt 0 && $((nfail % 2)) -eq 1` | 1 | killed | 124; two fails → PASS `passed=7`, want FAIL `failed=2` |
| 11 | `fail-even-only` | `$nfail -gt 0 && $((nfail % 2)) -eq 0` | 1 | killed | 1,676; one fail → PASS, want FAIL `failed=1` |
| 12 | `fail-mod3-only` | `$nfail -gt 0 && $((nfail % 3)) -eq 0` | 1 | killed | 1,770; one fail → PASS, want FAIL `failed=1` |
| 13 | `setup-odd-only` | `$nsetup -gt 0 && $((nsetup % 2)) -eq 1` | 1 | killed | 8,720; two setups → PASS, want SETUP `cannot-verify=2` |
| 14 | `setup-even-only` | `$nsetup -gt 0 && $((nsetup % 2)) -eq 0` | 1 | killed | 4,582; one setup → PASS, want SETUP `cannot-verify=1` |
| 15 | `setup-mod3-only` | `$nsetup -gt 0 && $((nsetup % 3)) -eq 0` | 1 | killed | 13,296; one setup → PASS, want SETUP `cannot-verify=1` |

On every member only `CHECK runtime` failed; `head`, `static` and `harness` passed (34/34 faults
rejected) — the kill/escape decision is entirely the runtime oracle's. Exit files:
`out/<member>.exit`; reports: `out/<member>.stdout`.

Copy sha256 (the exact bytes each audit consumed):

```
base.sh                     a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
restored.sh                 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
guard-mod-nlegs             32d139f976f8c6eba6f66ea41bec8144fe2a251d142259210a32664f703b4358
guard-mod2-odd              dcb7f5326721c20dc34bb08d53deeb4cd812c99a56ef491375c0401de6e2d163
guard-mod2-even             477a382b1141c82bda7af3c13e4232cd83f9354e6000387e1b8f8370ed0c18af
guard-mod3-nonzero          45b1d885e2bc3c5f5cad07315bae8f13036a563b6ab72b638fe8c58c5633691a
guard-mod-nlegs-eq0         af727efcd50d7d8cae079911b940201be5a7b26a5fb2e2a227af63523daa83b7
guard-parity-eq             343cfe5cd0f990c7267e67d61da917349278c0a99085490977821313eb3a2970
guard-parity-ne             ebc1df36fbaaeec7b656d41babac01c15b60cb111d48435d4572ea7782e2ad30
guard-even-and-ne           899516ad02292ba606994acd14c70c57cda38050d56e57dc514457e395ab4da5
guard-odd-and-ne            e491cc2a59fea077cca812d0b6e4ad73d88af6974c3dbaf4b0a70b8f2e570049
fail-odd-only               cb8dd6a38bbd3ef24659688514b38ed6ca6412bf75e98485d2a2a9cb0916641d
fail-even-only              aaf713781b94bf7013db158ee14b2a4be7da6cc0dd2ee40d733f87392d4d7031
fail-mod3-only              fed903d8302c6fa4df170c27c88d2495d959e08c7defe152bf726e61e0a91b44
setup-odd-only              ee3a46e5d07db56dd5c43ec891a98b1a17e631775d5b16c077417cdb658857cf
setup-even-only             747d313ffde0479c6b31c33b50a258bf3486e087b22fb86c0a79b37f5876a7b1
setup-mod3-only             af4dea900ddb77d92de696e8dc20871a38d6069105a9c43fd7f80e0ab2d71caa
guard2-r32-witness          8c8112608d239627d0a611441b38321945fc52f35fa2935a57df739e069201f0
```

## Why the five survive: executed blind-count map

`python3 blind_map.py; echo $?` → `0` (`out/blind_map.stdout`). For each count 1…27 the pristine
block, each survivor and the tool's own oracle are executed at that count
(`with_operands` + `run_vectors` + `oracle`).

```
pristine disagreements with oracle on counts 1..27: none
guard-mod-nlegs      blind-counts=[18, 27]                                  exercised-among-them=none
guard-mod2-even      blind-counts=[1,3,5,7,11,13,15,17,19,21,23,25,27]      exercised-among-them=none
guard-mod3-nonzero   blind-counts=[3,6,12,15,18,21,24,27]                   exercised-among-them=none
guard-parity-ne      blind-counts=[1,3,5,7,11,13,15,17,19,21,23,25,27]      exercised-among-them=none
guard-even-and-ne    blind-counts=[1,3,5,7,11,13,15,17,19,21,23,25,27]      exercised-among-them=none
```

The blind counts are exactly the counts the runtime sweep never feeds the guard (domain
{9} ∪ {8,10} above). `python3 count_probe.py; echo $?` → `0` (`out/count_probe.stdout`)
executes the literal r32 predicate block at those counts:

```
count 8    pristine rc=2 SETUP counted=8   mutant rc=2 SETUP counted=8    oracle rc=2 SETUP counted=8    agree
count 9    pristine rc=0 PASS passed=9     mutant rc=0 PASS passed=9      oracle rc=0 PASS passed=9      agree
count 10   pristine rc=2 SETUP counted=10  mutant rc=2 SETUP counted=10   oracle rc=2 SETUP counted=10   agree
count 18   pristine rc=2 SETUP counted=18  mutant rc=0 PASS passed=18     oracle rc=2 SETUP counted=18   DISAGREE
count 27   pristine rc=2 SETUP counted=27  mutant rc=0 PASS passed=27     oracle rc=2 SETUP counted=27   DISAGREE
```

So the r32 predicate is genuinely non-equivalent (it reports PASS on an 18-count tally, the r32
rationale verbatim), and the survival is a *count-coverage* fact, not an equivalent mutant in the
abstract. For a runner whose tally loop counts exactly the nine declared legs the predicate is
inert (sum is always 9); it becomes live only when a second defect inflates the counted total,
which is exactly the defense-in-depth the guard exists to provide.

## The r32 sealed copy vs its predicate alone

- Reconstructing the committed r32 JSON edit on tip bytes
  (`HeldOutGuard-2.json` → `edits[0]`) yields bytes **identical** to `copies/guard-mod-nlegs.sh`
  (sha `32d139f9…b4358`, equality checked in the transcript). The literal class member is in the
  family as member 1.
- The r32 copy **as witnessed** (same predicate + the JSON's 18-name `witness.loop` substituted
  into the loop) — `copies/guard2-r32-witness.sh`, sha `8c811260…01f0` — is **killed**:

```
python3 tool.py --runner copies/guard2-r32-witness.sh; echo $?    # 1
CHECK static  FAIL legs=9 operands=18 nlegs=9; loop operands != legs …
CHECK runtime FAIL vectors=15194 mismatched=20; first: all-pass → PASS passed=18, want SETUP counted=18
TALLY_AUDIT: FAIL (head=pass static=fail runtime=fail harness=pass)
```

`vectors=15194 = 15122 + 2×(18 positions × 2 kinds)`, consistent with the operand list being the
thing the stress walks. So the tool kills the r32 *artifact* through the operand-multiset static
check and the count-18 runtime vector, while the predicate alone passes — the precise boundary of
the gap.

## Harness axis: also blind

`python3 harness_probe.py; echo $?` → `0` (`out/harness_probe.stdout`), injecting blocks into the
runner's own selftest harness through the tool's `harness_section`/`run_harness`:

```
REF_BLOCK                        (cases, failed)=(9, 0)  ACCEPTED
guard-removed                    (cases, failed)=(9, 8)  REJECTED
guard-overcount-only (> nlegs)   (cases, failed)=(9, 1)  REJECTED
guard-mod-nlegs (% nlegs != 0)   (cases, failed)=(9, 0)  ACCEPTED
```

The harness's nine cases are all nine-status vectors; the divisibility predicate is indistinguishable
there too. The tool's own fault panel likewise carries `guard-removed`, `guard-overcount-only` and
`guard-overcount-only-alt` (`tool.py:469,470,487`) and no `%`-weakening — same hole on the panel axis.

## Findings

### F1 — MEDIUM (coverage; routed Hold confirmed, no landed artifact wrong)

The r32 Guard-2 divisibility class is **not killed** as a guard-predicate copy: 5/15 family members
survive, including the exact committed predicate `(npass + nfail + nsetup) % nlegs != 0`.
Both the runtime sweep (counts {8,9,10}) and the embedded harness (nine-status cases) are blind to
every predicate that agrees with `!= nlegs` on {8,9,10}, and every survivor's divergence counts lie
outside that domain (executed map above). Impact on C1: none — the sealed r33 kill set contains no
divisibility member, and the r32 artifact itself is killed; `ho_kill=8/8` is untouched. Impact on
the v3 Hold: the Hold is real and now has an executable witness and a named blind domain (counts
18/27 and odd/multiples-of-3 counts away from 9). Fixing it would be a tool edit (forbidden this
wave; tool frozen at `7b11ba25…8d10`).

Reproduce:
```
python3 tool.py --runner copies/guard-mod-nlegs.sh; echo $?          # 0 (survived)
python3 tool.py --runner copies/guard2-r32-witness.sh; echo $?      # 1 (killed)
python3 blind_map.py; echo $?                                        # 0
python3 count_probe.py; echo $?                                      # 0
python3 harness_probe.py; echo $?                                    # 0
```

### F2 — none. No landed artifact was proven wrong.

Pins match at tip and in the live lane; the deciding receipt is present and its text matches the
dispatch; the family's baseline and restored runs both PASS with the pinned bytes. The probe
produced a coverage observation only.

## Restoration / hygiene

- `tool.py` before/after: `7b11ba25…8d10` = `7b11ba25…8d10`; `pristine.sh` before/after:
  `a7d3f2dd…2eb9` = `a7d3f2dd…2eb9` (family.py printed both lines; `out/family.summary`).
- `copies/restored.sh` sha `a7d3f2dd…2eb9`, `cmp -s pristine.sh copies/restored.sh` → exit 0;
  `python3 tool.py --runner copies/restored.sh` → exit 0, `TALLY_AUDIT: PASS` (out/restored.*).
- Baseline `copies/base.sh` sha identical to the pin; audit exit 0 (out/base.*).
- Lane read-only: `git -C lane status --porcelain` → 0 lines, exit 0. No git/jj write commands;
  no MANIFEST/templates/state/watchdog/sibling-repo writes; only scratch copies and this report.
- Kill rule respected: `c1-measure.py` was hashed for the pin table only, never executed in any
  mode; no counter import, no counter CLI. The tool was used unmodified as a subprocess; its
  functions were imported only in the auxiliary probes (`count_probe.py`, `blind_map.py`,
  `harness_probe.py`) operating on scratch bytes.

## Tooling

No installs or upgrades. Host `python3` (`Python 3.14.8`), `git`, `sha256sum`, `cmp` sufficed. Pacman
untouched per the 2026-10-20 pause ruling.
