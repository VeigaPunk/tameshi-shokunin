# T55W1CritFreeze — freeze soundness and deciding-run gate logic

Round 55, wave 1, seat `T55W1CritFreeze` (critic). Lane `tameshi-shokunin`.
Freeze commit `631cd6455e58dce969310b4c0466c3383d9f5108`; base `0a2010acd1e92e4e332774050825e21bcfc7e079`.
All work in `/fast/scratch/hyaku/tameshi-r55/T55W1CritFreeze`; receipts copied to
`.ufo/waves/round-55/w1/T55W1CritFreeze-receipts/`. No lane production file, no frozen file was edited.
No tool was installed (nothing needed; `strace`, `git`, `python3` were already present).

## Verdict

The freeze **of record at 631cd645 is internally sound, and its coverage and set-equality claims hold**. The
freeze **as a decision instrument is not sound**: the FROZEN gate forbids the very amendments the contract
records, and the frozen C2 counter cannot certify C2 on this host even with a perfect tree. Seven gate holes are
also demonstrated; two of the gate's own defences were confirmed working.

- F1 (blocker, C2 decidability): committing the contract's amendments fails `FROZEN_UNCHANGED`; not committing
  them leaves the frozen counter's `usable` arm broken under `strace`. The round has no state in which C2 can pass.
- F2 (blocker, C2 decidability): the frozen counter itself, run from its own bytes at rev against base, prints
  `usable=12/13 … total=19 C2_R55_PASS=false`, not the frozen receipt's `usable=13/13 … total=18`. The receipt the
  manifest certifies is not reproducible, and **no tree can pass C2 while this counter is the frozen one**.
- F3 (high, provenance): the working-tree `freeze.json` re-derives from no revision — its `contract.json` entry is
  the contract truncated to exactly 3 amendments; at snapshot time the contract carried 5 amendments.

## Checks (command → result)

| # | Check | Command | Result |
|---|---|---|---|
| C1 | Every `freeze.json` sha256 re-derived from bytes at 631cd645 | `git -C LANE show 631cd645:.ufo/evidence/round-55/freeze.json` + `sha256(git show 631cd645:<path>)` for each entry (r1) | **6/6 OK**, `MISMATCH=0` |
| C2 | Coverage of `contract.frozen_paths` | set difference of `contract.frozen_paths`, `freeze.files`, `deciding-run.sh` `FROZEN=` (r2) | 7 paths, 6 hashed; the only uncovered path is `freeze.json` (the manifest itself); 0 extra entries |
| C3 | Manifest does not hash itself | `'.ufo/evidence/round-55/freeze.json' in freeze.files` (r2) | **False** (correct); `freeze.note` says exactly this |
| C4 | Deciding run's FROZEN list == contract list | normalise `/round-55/` prefixes, set-compare (r2) | **True**, 7 == 7, no difference either way |
| C5 | Gate harness is the frozen bytes | `cmp` of `gate.sh` lines 9–47 vs `631cd645:deciding-run.sh` lines 20–58 (r5) | **IDENTICAL**, 39 lines |
| C6 | Freeze integrity on the real lane | `bash gate.sh <lane-clone> 631cd645 631cd645 out` (r10) | `FREEZE_INTEGRITY: OK files=6 amendments=0`, then `control-receipt-missing` (correct at freeze time: `control/` does not exist at 631cd645) |
| C7 | Empty control receipt | fix3: `controls-a.exit` a 0-byte blob at REV (r6) | **REFUSED** `control-receipt-empty` (defence works) |
| C8 | Stale (pre-freeze) control receipt | fix4: receipts last touched before the freeze commit (r6) | **REFUSED** `control-receipt-not-after-freeze` (defence works) |
| C9 | Manifest that hashes nothing | fix2: `files={}`, `contract.frozen_paths` untouched (r6) | **OPENED** — `FREEZE_INTEGRITY: OK files=0` |
| C10 | Vacuous verdict line | fix5: `CONTROLS_A: 0/0 as pre-registered` (r6) | **OPENED**; regex also accepts `/`, `9/0`, `0/99` (r7-regex) |
| C11 | Stale content read from the working tree | fix6: REV blob is the 1 byte `x`; worktree carries the verdict; index flag `assume-unchanged` (r6) | `git status --porcelain` empty → **OPENED** |
| C12 | Exit receipts ignored | fix8: `controls-a.exit`/`controls-b.exit` committed as `1` (r6) | **OPENED**; the gate never reads `.exit` content |
| C13 | Second invocation | fix1: run with OUT1, `touch OUT1/c{1,2}.start`, re-run with OUT1 then OUT2 (r7) | OUT1 **REFUSED**; OUT2 **OPENED** — guard is OUT-scoped, not round-scoped |
| C14 | OUT contract ("existing, EMPTY dir inside LANE") | fix1: OUT outside LANE, then non-empty OUT (r7) | both **OPENED**; only `[ -d "$OUT" ]` is checked |
| C15 | Clean-tree check | fix5: untracked `junkfile`, OUT named `.*` (r7) | **OPENED**; `${OUT#$LANE/}` is an unescaped regex, `.*` hides every `??` line |
| C16 | FROZEN gate vs `REV` carrying the amendments | fix9: root = 631cd645 bytes, HEAD = worktree `contract.json` + `c2/measure.py` (r8) | `FROZEN_UNCHANGED=0`, `FROZEN_RC=1` |
| C16b | Frozen C2 counter at base, from its own bytes | `git show 631cd645:.ufo/evidence/round-55/c2/measure.py > frozen-c2.py; python3 frozen-c2.py --lane LANE --rev 0a2010ac --work <empty> --explain` (r12) | `grammar=6/8 lazy=5/5 empty=13/13 usable=12/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=19 C2_R55_PASS=false` |
| C17 | Frozen C2 `usable` arm on this host | `strace -f -e trace=mkdir,mkdirat python3 tools/registry-check.py --selftest`, good TMPDIR, rev clone (r11) | plain rc=0 (51/51 PASS); **strace rc=1** (timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe), reproduced 3/3 (two standalone + one inside the aggregate run) |
| C18 | Census conformance | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (r9) | **exit 0** (W04 duplicate-url warnings only) |
| C19 | `FREEZE` is caller-supplied | fix1: `bash gate.sh fix1 <REV> <REV> out` and `frozen-gate.sh fix1 <REV> <REV> out` (r13) | `FREEZE_INTEGRITY: OK`, `FROZEN_UNCHANGED=1`, **OPENED** — passing `FREEZE=REV` self-certifies |

## Findings

### F1 (blocker) — the FROZEN gate makes the contract's amendments unregistrable

`deciding-run.sh` requires `contract.json` **and** `c2/measure.py` to be byte-identical between FREEZE and REV
(line 65–66). The contract in the working tree records five amendments that edit exactly those two files. Either
state fails:

- commit the amendments at REV → `FROZEN_UNCHANGED=0` → `rc=1` (C16, r8). Demonstrated with the real bytes:
  `contract.json 2388cb50 → 5de4f37b`, `c2/measure.py 9d076812 → d6ca1d85`.
- do not commit them → the counters executed are `git show "$REV:$E/c2/measure.py"`, i.e. the pre-amendment
  bytes, and all five amendments are dead letters that no gate ever reads (`FREEZE_INTEGRITY` reads
  `$FREEZE:freeze.json`; the working-tree `freeze.json` is not consulted at all).

The contract's amendment prose ("before any deciding invocation", "predicate unchanged") is therefore
unfalsifiable — and the freeze manifest's own `amendments` array at 631cd645 is empty (0), so the manifest of
record does not carry them either.

Smallest safe correction (L1 decision, not mine to apply): re-anchor at a **new freeze commit** that contains the
amended bytes and a `freeze.json` regenerated from them, and run `deciding-run.sh <LANE> <REV> <NEW_FREEZE> <OUT>`;
leave 631cd645 in the record as the superseded freeze. The alternative — reverting the working tree to the rev
bytes — leaves F2 in force and C2 undecidable.

### F2 (blocker) — the frozen C2 counter cannot pass C2, and its own receipt is not reproducible

`c2/measure.py` (rev) takes the `usable` exit code from `trace()`: `strace -f -e trace=mkdir,mkdirat …`. On a rev
clone with a good TMPDIR:

```
plain : python3 tools/registry-check.py --selftest            rc=0  SELFTEST: PASS (51 cases)
traced: strace -f -e trace=mkdir,mkdirat python3 … --selftest rc=1  FAIL (timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)
```

reproduced on three independent runs (r11; 226.7 s, 338.9 s). Therefore `usable=12/13` on any tree.
The decisive receipt is the counter run from its own frozen bytes against the base revision (r12):

```
C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=12/13 tmp_mkdirs=0 docs=0/7 note=0/8
        skill=0/1 total=19 C2_R55_PASS=false
```

The frozen `before/c2.stdout` records `usable=13/13 … total=18`. Same lane, same rev, same invocation: the
receipt the manifest certifies is not reproducible from the counter the manifest certifies. Even with every
integration arm perfect (grammar 8/8, docs/note/skill fixed), `usable` alone holds `total ≥ 1`, so
**C2_R55_PASS=true is unreachable while 631cd645's counter is the frozen one**. Amendment 4 in the working-tree
contract describes exactly this defect and fixes it — and cannot be registered (F1).

Smallest safe correction: under a new freeze (F1) apply amendment 4 (plain rc for `usable`, trace only for the
`/tmp` census), then re-derive the `before` receipt from that counter. Absent a re-freeze, C2 must be reported as
a **counter defect** (a miss), not as a failed claim: the `kill_rule` makes a short arm false, but this arm reads
false from a correct tree.

### F3 (high) — the working-tree `freeze.json` is a hybrid that re-derives from no revision

At the 14:05 snapshot (r3, r4):

| entry | manifest | rev 631cd645 | worktree |
|---|---|---|---|
| `contract.json` | `ed6871e1…` | `2388cb50…` | `5de4f37b…` (5 amendments) |
| `c2/measure.py` | `ab3ae751…` | `9d076812…` | `d6ca1d85…` |
| `c1/measure.py` | `77abe1e9…` (= rev) | `77abe1e9…` | `711507e7…` |
| `controls.sh`, `deciding-run.sh`, `no-harm.sh` | = rev = worktree | = | = |

`sha256(json.dumps(contract, indent=1)+"\n")` with the amendment list truncated proves the generation:
`amendments=5 → 5de4f37b`, `=4 → 0b99dd8c`, **`=3 → ed6871e1` (the manifest's entry)**, `=0 → 2388cb50` (rev).
The manifest was written after amendment 3 and never regenerated; the contract has since gained amendments 4–5.
A scan of every blob in the object database found no object whose sha256 is `ed6871e1…` or `ab3ae751…` (r3 note),
so the manifest's two entries name bytes that exist in no commit.

This does not open or close the gate (the gate reads the rev manifest), but it means the manifest a reader sees in
the lane cannot be verified, and the freeze's own amendments are invisible. Any regeneration must hash the bytes
of the commit it will be committed in, together with it.

Smallest safe correction: generate `freeze.json` with the amended files in the same commit, then re-derive all
entries from that commit before committing (a one-line loop is enough; see F7).

### F4 (medium) — the verdict check reads the working tree, and `assume-unchanged` hides that

Lines 54–55 grep `$LANE/$E/control/controls-a.stdout` (working tree) while lines 47–53 validate blobs at `$REV`.
The clean-tree check runs afterwards and `git status` honours the `assume-unchanged`/`skip-worktree` index flags.
Demonstration (C11): REV commits a 1-byte `controls-a.stdout` (`x`), the worktree file is overwritten with the
verdict, `git update-index --assume-unchanged` is set, `git status --porcelain` prints nothing, and the gate opens.

Smallest safe correction: copy the receipt out of REV (`git show "$REV:$f" > "$OUT/…"`) and grep that file; add a
refusal when `git ls-files -v` reports any lowercase/`S` flag.

### F5 (medium) — the verdict regex accepts a vacuous denominator

`^CONTROLS_A: [0-9]*/[0-9]* as pre-registered` accepts `0/0`, `9/0`, `0/99`, and even `/` (empty `[0-9]*`), and
nothing compares the numerator/denominator to the pre-registered control count. C10, r7-regex.

Smallest safe correction: `[1-9][0-9]*/[1-9][0-9]*` and require the exact expected `N/N` recorded in the contract.

### F6 (medium) — the `.exit` receipts are never read

The gate requires each `controls-*.exit` to be a non-empty blob and then ignores its content. Committed `1`
receipts open the gate (C12). Smallest safe correction: require `[ "$(git show "$REV:$f")" = 0 ]`.

### F7 (medium) — the integrity check never cross-checks the manifest against `contract.frozen_paths`

The integrity block iterates `freeze.files` only. A manifest with `files={}` prints `FREEZE_INTEGRITY: OK files=0`
and the gate opens (C9), even though the contract lists seven frozen paths. The current manifest is complete, but
nothing enforces that it stays complete. Smallest safe correction: inside the integrity block, load
`contract.frozen_paths` (from FREEZE) and refuse when the normalised sets differ (allowing only `freeze.json`).

### F8 (medium) — the second-invocation guard is scoped to the caller-chosen OUT

`for k in c1 c2; do [ -e "$OUT/$k.start" ] …` only inspects the OUT passed on this invocation. A second invocation
with a fresh, even non-empty, even out-of-lane OUT opens (C13, C14). `deciding_invocations: 1` is therefore not
enforced. Smallest safe correction: keep a round-global sentinel (a fixed path under `$SCR`, plus refusal when any
`deciding-run.exit` receipt already exists under the lane's evidence dir), and require `${OUT#LANE/} != "$OUT"`.

### F9 (low) — the clean-tree check is an unescaped regex

`grep -vc "^?? ${OUT#$LANE/}"` treats the OUT path as a pattern. An OUT directory literally named `.*` makes the
filter match every untracked line, so `?? junkfile` is invisible and the gate opens on a dirty tree (C15).
Smallest safe correction: `grep -vF -- "?? ${OUT#$LANE/}"` (fixed string) or compare against `git status
--porcelain -z` parsed in Python.

### F10 (high) — `FREEZE` is caller-supplied and unconstrained, so `FREEZE=REV` self-certifies

The fourth argument to `deciding-run.sh` is a bare rev. Nothing pins it to the contract's freeze, requires
`FREEZE != REV`, or requires `FREEZE` to be an ancestor of `BASE` (0a2010ac). Passing `FREEZE=REV` makes the
integrity block hash the manifest it finds at REV against the bytes at REV and makes `git diff FREEZE REV` empty:
`FREEZE_INTEGRITY: OK files=6 amendments=0`, `FROZEN_UNCHANGED=1`, gate opens (C19, r13). The receipt records
`freeze=<sha> rev=<sha>`, so an auditor can see it — but the gate itself does not refuse it, and the contract's
`frozen_paths`/`lowest_axis` prose is the only anchor. Smallest safe correction: take the freeze from the contract
(or a fixed constant) instead of argv, and refuse unless `FREEZE` is an ancestor of `BASE` and `FREEZE != REV`.

### F3 re-check (14:12)

The working-tree manifest mismatched three entries again at 14:12 — `c1/measure.py` worktree `5e8f50d1` vs
manifest `77abe1e9`, `c2/measure.py` worktree `36ca47d3` vs manifest `ab3ae751`, `contract.json` worktree
`5de4f37b` vs manifest `ed6871e1` — with `contract.amendments=5`, `freeze.amendments=3`. The counters are being
edited live; the manifest has not been regenerated.

## Non-findings (what the sweep confirmed)

- All six manifest entries re-derive at 631cd645; no self-hash; the only uncovered `frozen_paths` entry is the
  manifest itself, as stated.
- The deciding run's FROZEN list is exactly the contract's `frozen_paths` (normalised), 7 == 7.
- An empty control blob at REV is refused; a receipt last touched before FREEZE is refused; `HEAD` must equal `REV`;
  counters, no-harm and precheck are read from REV, not the working tree.
- The gate harness used for the attacks is the frozen script verbatim (C5), so the findings are about the real code.

## Observed lane mutations (reported, not fixed)

While this seat ran, the lane's intermediate evidence changed under it: `c1/measure.py` (`5e8f50d1` at 14:12),
`c2/measure.py` (`36ca47d3` at 14:12), `contract.json` (5 amendments) and `freeze.json` (still the 3-amendment
generation) are modified but uncommitted; `.ufo/evidence/round-55/before/c2.stdout` was truncated to 0 bytes in
the working tree (the blob at 631cd645 still has 43 lines). These are expected mid-wave edits by other seats and are why F3 exists; they were
not touched here, and nothing in the frozen set was modified.

## Receipts

`.ufo/waves/round-55/w1/T55W1CritFreeze-receipts/`:
`r1-freeze-at-rev.txt`, `r2-coverage-sets.txt`, `r3-worktree-manifest.txt`,
`r4-amendment-hash-reconstruction.txt`, `r5-harness-provenance.txt`, `r6-gate-attacks.txt`,
`r7-out-and-clean-tree-attacks.txt`, `r7-regex.txt`, `r8-frozen-gate-amendment.txt`, `r9-census.txt`,
`r10-real-lane-gate.txt`, `r11-regcheck-{plain,strace,strace2}.{out,err}`,
`r12-c2-frozen-at-base.out`, `r13-self-referential-freeze.txt`, `snapshot/` (bytes cited for the live lane at 14:05).
