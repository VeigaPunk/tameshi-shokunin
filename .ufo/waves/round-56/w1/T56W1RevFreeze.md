# T56W1RevFreeze — freeze-discipline audit (round 56, wave 1)

Seat: `T56W1RevFreeze` (leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Freeze revision audited: `c3e2ca9f020776b3d66c7af854fb82c834674fcf`. Base: `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`.
Scratch: `$HYAKU_SCRATCH/tameshi-r56/T56W1RevFreeze` (`/fast/scratch/hyaku/...`); lane clone is `git clone --shared` + `checkout --detach c3e2ca9f`, `rev-parse --show-toplevel` asserted equal to the clone before every commit there. No lane file was written except this report, its `.json` and the receipts directory. No mutating git command ran against the lane.

**Verdict.** The manifest is honest about the bytes it names — **10/10 digests re-derive at the freeze revision** — but the enforcement around it has **two high, two medium and two low holes**: the deciding run cannot execute the C1 counter at all (H1), the freeze commit is pinned nowhere so an instrument can be re-frozen with no amendment (H2), two files committed *as* frozen instruments are in no manifest and their mutation prints `FROZEN_UNCHANGED=1` (H3), and the round's `before/` receipts are uncommitted (M1). `FREEZE_DISCIPLINE=false` until H1–H3 are dispositioned; none of them is fixable inside this seat (instruments are frozen).

---

## (a) `freeze.json` keys vs `contract.json` `frozen_paths`; digest re-derivation

Command (receipt `a-rederive.txt`): a script that reads `freeze.json` and `contract.json` **at the freeze commit** through `git show` with `GIT_CONFIG_GLOBAL=/dev/null`, maps each `files` key with the deciding run's own rule (`rel if rel.startswith(('tools/','.ufo/evidence/round-21/','.ufo/evidence/round-48/')) else '<E>/'+rel`), and re-hashes the blob bytes with `hashlib.sha256`.

```
schema=tameshi-freeze-v1 round=56 lane=tameshi base=981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
files=10 amendments=[]
OK    c1/lost-headings-at-base.json                 dcfc9f800b8bc7b2 dcfc9f800b8bc7b2
OK    c1/measure.py                                 048122cf1c7c65d2 048122cf1c7c65d2
OK    c2/measure.py                                 d17d36bd263b3e9d d17d36bd263b3e9d
OK    c2/red-before/round-54-surface.paths          95ead282432b1bde 95ead282432b1bde
OK    contract.json                                 2530a54775aecde0 2530a54775aecde0
OK    control/frozen-surface.paths                  a0ebd3d4216d5103 a0ebd3d4216d5103
OK    controls.sh                                   df1ee355ce626172 df1ee355ce626172
OK    deciding-run.sh                               6a63f5058be15f5f 6a63f5058be15f5f
OK    no-harm.sh                                    a13ba1a8433752c8 a13ba1a8433752c8
OK    tools/receipt-revision-gate.py                1d80f8a665f83508 1d80f8a665f83508
REDERIVE_BAD=0
```

Independent cross-check with `sha256sum` over `git cat-file blob FREEZE:<path>` (receipt `a2-sha256sum.txt`) reproduces all ten digests byte-for-byte, e.g.
`2530a54775aecde0ead0d989b5bb7a782e5a6fcd7390b41bebb10eea454bb50f  .ufo/evidence/round-56/contract.json`,
`1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2  tools/receipt-revision-gate.py`.

Coverage: `contract.frozen_paths` has **11** entries, `freeze.json.files` has **10**; mapping both through the deciding run's rule gives **10 IN-FREEZE-JSON, 1 NOT-IN-FREEZE-JSON**:

```
.ufo/evidence/round-56/freeze.json   -> freeze.json   NOT-IN-FREEZE-JSON
```

No `freeze.json` key is absent from `frozen_paths` (no extras). So the only uncovered frozen path is the manifest itself — a self-digest is impossible, and the deciding run compensates with the `FREEZE..REV` diff instead (`FROZEN=` includes `$E/freeze.json`). That compensation is worth exactly as much as the `FREEZE` argument, which is **caller-supplied and pinned nowhere** — see H2.

## (b) `deciding-run.sh` `FROZEN=` vs `freeze.json`

Command (receipt `b-frozen-list.txt`): parse the `FROZEN=` line out of the script **at the freeze commit**, expand `$E/`, compare with the mapped `freeze.json` keys.

```
FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py $E/c1/lost-headings-at-base.json $E/c2/measure.py $E/control/frozen-surface.paths $E/c2/red-before/round-54-surface.paths $E/no-harm.sh $E/deciding-run.sh $E/controls.sh tools/receipt-revision-gate.py"
FROZEN_count=11 freeze_files_count=10
BOTH  .ufo/evidence/round-56/contract.json
FROZEN-ONLY .ufo/evidence/round-56/freeze.json
BOTH  .ufo/evidence/round-56/c1/measure.py
BOTH  .ufo/evidence/round-56/c1/lost-headings-at-base.json
BOTH  .ufo/evidence/round-56/c2/measure.py
BOTH  .ufo/evidence/round-56/control/frozen-surface.paths
BOTH  .ufo/evidence/round-56/c2/red-before/round-54-surface.paths
BOTH  .ufo/evidence/round-56/no-harm.sh
BOTH  .ufo/evidence/round-56/deciding-run.sh
BOTH  .ufo/evidence/round-56/controls.sh
BOTH  tools/receipt-revision-gate.py
```

The two sets agree up to `freeze.json` (expected: it cannot contain its own digest). **No path is in one list and not the other**, so item (b)'s literal test is clean. The hole is not in the set difference but in the *files both lists omit* — H3.

The script's own freeze enforcement is exactly three things, and I checked each:

1. the `FREEZE_INTEGRITY` heredoc (lines 26–48) — re-derives `files` at `FREEZE`, prints `FREEZE_INTEGRITY: OK|MISMATCH files=N amendments=M`;
2. the `FROZEN_UNCHANGED` two-tree diff (lines 79–80);
3. the control-receipt ancestry check (`merge-base --is-ancestor FREEZE <receipt commit>`, line 54).

Nothing else in the script or in either counter reads `freeze.json`: `grep -n freeze .ufo/evidence/round-56/c1/measure.py .ufo/evidence/round-56/c2/measure.py` → no match (receipt `o-counter-freeze-refs.txt`); `grep -n freeze tools/receipt-revision-gate.py` → no match (receipt `q-gate-freeze.txt`). There is **no** `merge-base --is-ancestor "$FREEZE" "$REV"` for the instruments; the only `is-ancestor` in the script is line 54, for control receipts (receipt `i2-verbatim-clean.txt`).

## (c) Amendment protocol: can an instrument change after the freeze without an amendment?

**Yes, three ways.** `amendments` appears in exactly three places lane-wide — `contract.json:47`, `freeze.json:18`, and the deciding run's print — and nothing validates it (receipt `n-sidecar-amendments.txt`):

```
.ufo/evidence/round-56/contract.json:47: "amendments": []
.ufo/evidence/round-56/deciding-run.sh:40:print('FREEZE_INTEGRITY: %s files=%d amendments=%d'
.ufo/evidence/round-56/deciding-run.sh:41:      % ('OK' if not bad else 'MISMATCH', len(fr['files']), len(fr.get('amendments') or [])))
.ufo/evidence/round-56/freeze.json:18: "amendments": []
```

The run prints the *count* and never looks at the entries; nothing requires an amendment when a digest changes, and nothing names which commit the freeze was.

Experiments (fixture clone `/fast/scratch/hyaku/tameshi-r56/T56W1RevFreeze/mut`, toplevel asserted, commits made with a fixture identity; receipt `g-mutation-experiments.txt`, re-evaluated with the script's **verbatim** lines 79–80 in receipt `i2-verbatim-clean.txt`):

**M1 — mutate a file both manifests omit** (`c2/red-before/round-54-ctl-pos-c1.stdout`, read by `c2/measure.py:146`):

```
FROZEN_UNCHANGED=1 freeze=c3e2ca9f0207 rev=245905239bf18d01fb2ece6b053ce2ebc800ad13
rc=0
FREEZE_INTEGRITY: OK files=10 amendments=0
```

The deciding run prints **nothing about the change**. That is H3.

**M2 — mutate a listed instrument** (`c1/measure.py`, +2 lines):

```
FROZEN_UNCHANGED=0 freeze=c3e2ca9f0207 rev=cda8dfd245208c201e7829012fe3acb0c8e2d340
 .ufo/evidence/round-56/c1/measure.py | 2 ++
 1 file changed, 2 insertions(+)
rc=1
```

Caught — but note the verifier still printed `FREEZE_INTEGRITY: OK files=10 amendments=0` in the same run, because it re-derives at `FREEZE`, not at `REV`. The single thing that catches a post-freeze instrument edit is the two-tree diff.

**M3 — mutate a listed instrument *and* rewrite its digest in `freeze.json`, then pass the new commit as `FREEZE`** (the deciding run's `FREEZE` is `$3`, `git rev-parse`-verified and otherwise unpinned; `BASE` is hardcoded, `FREEZE` is not):

```
freeze.json c1/measure.py digest rewritten to 5f1222b03ba0c670 amendments= []
FREEZE_INTEGRITY: OK files=10 amendments=0
verifier_exit=0
FROZEN_UNCHANGED=1 freeze=a23b5e2d9449d921266c0cc86c64153721bbcada rev=a23b5e2d9449d921266c0cc86c64153721bbcada
```

Both freeze checks pass, `amendments` is `[]`, and an instrument changed after the freeze. Supporting fact: **the freeze commit is pinned nowhere in the frozen material** — `git grep -n c3e2ca9f <freeze> -- .ufo/evidence/round-56` → `NO_OCCURRENCE` (receipt `j-contract-vs-instruments.txt`). This is H2.

**M4 — free-text amendment**:

```
amendments= [{'whatever': 'no evidence, no commit, no signature'}]
FREEZE_INTEGRITY: OK files=10 amendments=1
FROZEN_UNCHANGED=1 freeze=0e9f288c4b24 rev=0e9f288c4b24
```

Any string counts as an amendment. The protocol is a comment, not a mechanism.

## (d) The freeze commit contains every instrument and no content edit

Receipt `c-freeze-commit.txt`:

```
c3e2ca9f020776b3d66c7af854fb82c834674fcf
tameshi-shokunin <tameshi@shokunin.local>
Wed Oct 28 15:36:14 2026 -0300
981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
round-56: freeze the claim instruments (contract, c1/c2 counters, receipt-revision gate, controls, no-harm, deciding run)
```

`git diff --name-status 981c5e8b c3e2ca9f` (receipt `p-base-freeze-diff-census.txt`) is **13 × `A`, 0 × `M`, 0 × `D`**:

```
A	.ufo/evidence/round-56/c1/lost-headings-at-base.json
A	.ufo/evidence/round-56/c1/measure.py
A	.ufo/evidence/round-56/c2/measure.py
A	.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout
A	.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout.sha256
A	.ufo/evidence/round-56/c2/red-before/round-54-surface.paths
A	.ufo/evidence/round-56/contract.json
A	.ufo/evidence/round-56/control/frozen-surface.paths
A	.ufo/evidence/round-56/controls.sh
A	.ufo/evidence/round-56/deciding-run.sh
A	.ufo/evidence/round-56/freeze.json
A	.ufo/evidence/round-56/no-harm.sh
A	tools/receipt-revision-gate.py
```

So: every manifest file is present, `freeze.json` is present, **no content file was modified** — the only non-`.ufo` addition is `tools/receipt-revision-gate.py`, the C2 instrument, which `no-harm.sh:30` explicitly allowlists (`A:tools/receipt-revision-gate.py`). Two of the thirteen additions are in **no manifest** (H3). `before/` is in **neither the commit nor any manifest** (M1).

Contract-vs-instrument arithmetic also checks out (receipt `j-contract-vs-instruments.txt`): `no_harm_monitors=15` vs 15 `NOHARM` emitters in `no-harm.sh`; 9 control emitters (7 negative `A`, 2 positive `B`) matching the union of the two claims' `controls` lists; `deciding_invocations=1` vs a guard that is **not** a global one (M2).

---

## Holes, by severity

### H1 — HIGH: the deciding run cannot run the C1 counter from committed bytes
`deciding-run.sh:60-62` materializes only `c1/measure.py`, `c2/measure.py`, `no-harm.sh`; `c1/measure.py:179` loads its input from `Path(__file__).resolve().parent / 'lost-headings-at-base.json'`. Reproduced exactly (receipt `f1-c1-materialized.txt`):

```
python3 $SCR/code/c1/measure.py --lane <clone> --rev c3e2ca9f0207 --work $SCR/c1 --explain
Traceback (most recent call last):
  File ".../scr/code/c1/measure.py", line 179, in main
    frozen = json.loads((Path(__file__).resolve().parent / 'lost-headings-at-base.json').read_text('utf-8'))
FileNotFoundError: [Errno 2] No such file or directory: '.../scr/code/c1/lost-headings-at-base.json'
EXIT=1
```

Consequence inside the deciding run: no `C1_R56:` line is produced, `grep -q "C1_R56_PASS=true"` fails, and `DECIDING_RUN_EXIT=1` — **at every revision**, whatever the lane does. With the file copied beside it the same invocation works (receipt `f2-c1-with-sibling.txt`):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=c3e2ca9f0207 cand_credited=46 lost=18 RED
EXPLAIN arm2-monitor covered=46 score=6 box3=False
C1_R56: rev=c3e2ca9f0207 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false
```

(The counter also defines `HEADINGS = '.ufo/evidence/round-56/c1/lost-headings-at-base.json'` at line 62 and then ignores it — an internal inconsistency that only bites when the script is run from outside the repo, which is precisely what the deciding run does. `controls.sh:35` runs `"$repo/$C1"`, in-repo, so the controls never expose it.)

### H2 — HIGH: the freeze commit is unpinned; instruments can be re-frozen with no amendment
`FREEZE=$3`, `git rev-parse`-verified, never compared to a constant (`BASE` is). `git grep c3e2ca9f` in the frozen evidence → `NO_OCCURRENCE`. `freeze.json` cannot digest itself and nothing else pins it. M3 shows a post-freeze instrument edit passing both freeze checks with `amendments=[]`. Anyone who can commit can re-freeze; the round's freeze discipline then reduces to the reviewer reading the commit log.

### H3 — HIGH: two files committed *in* the freeze commit are in no manifest
`.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout` and `...stdout.sha256` are in the freeze commit, are read by `c2/measure.py:146-151` at `REV`, and appear in **neither** `freeze.json.files`, **neither** `contract.frozen_paths`, **nor** the `FROZEN=` list. M1: mutating the receipt yields `FROZEN_UNCHANGED=1` and `FREEZE_INTEGRITY: OK`. The receipt is `CTL CTL_POS_c1 C1_R54: rev=077d431e6996 ...` — the exact evidence C2's red-before arm rests on. Additionally the sidecar is never materialized into the counter's work dir (`c2/measure.py` writes only `slice_path`), so the gate's `if sidecar.exists()` digest check (`receipt-revision-gate.py:106-110`) is **skipped** for arm 2: even the digest binding that exists is inert on that path.

### M1 — MEDIUM: the round's `before/` receipts are uncommitted and undigested
`git ls-tree -r <freeze> -- .ufo/evidence/round-56/before` → empty; the working tree has `before/c1.stdout`, `before/c2.stdout`, `before/c2-at-base.stdout` untracked and **not gitignored** (`git check-ignore` exit 1) — receipt `k-before-tracking.txt`. Rounds 54 and 55 committed `before/c1.stdout` and `before/c2.stdout` at base; round 56 did not, while `contract.json` cites `before/c1.stdout` and `before/c2.stdout` as the claim's "before". The cited evidence is mutable and not reproducible from any commit.

### M2 — MEDIUM: `deciding_invocations: 1` is unenforced
The second-invocation guard is `[ -e "$OUT/$k.start" ]` (line 58) and `OUT` is caller-chosen; line 46 checks only `-d "$OUT"` (not emptiness, despite the usage text saying "existing, EMPTY"). A second invocation with a fresh `OUT` passes. The header's "A second invocation is refused" holds only within one `OUT` directory.

### L1 — LOW: no ancestry check for the instruments
The `FROZEN_UNCHANGED` test is a two-tree `git diff`, so a `REV` on an unrelated history whose instrument bytes happen to match passes. Only control receipts get `merge-base --is-ancestor` (line 54).

### L2 — LOW (wave-3 precondition, not a freeze defect): the lane tree is dirty for the deciding run
Applying the script's clean-tree gate to today's tree (receipt `m-cleantree-gate.txt`):

```
?? .ufo/evidence/round-56/assimilation/
?? .ufo/evidence/round-56/before/
?? .ufo/evidence/round-56/census-start.stderr
?? .ufo/evidence/round-56/census-start.stdout
?? .ufo/waves/round-56/
non-OUT status lines=5
DECIDING_REFUSED dirty-tree
```

`before/` and the wave reports must be committed (or removed) before the deciding run, or it refuses at gate 0a.

---

## Proposed patches (diff only — the L1 integrates; I edited nothing)

`deciding-run.sh` is frozen; changing it needs an amendment, and H2 says the amendment protocol enforces nothing, so the L1 must record the reason and bump the manifest itself.

```diff
--- a/.ufo/evidence/round-56/deciding-run.sh
+++ b/.ufo/evidence/round-56/deciding-run.sh
@@ -13,12 +13,14 @@
 BASE=981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
+FREEZEPIN=c3e2ca9f020776b3d66c7af854fb82c834674fcf
 FLEET=/home/vgpnk/Projects/shokunin
 ...
 FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
+[ "$FREEZE" = "$FREEZEPIN" ] || { echo "DECIDING_REFUSED freeze-not-pinned"; exit 3; }
@@ -60,6 +62,7 @@
 for f in c1/measure.py c2/measure.py no-harm.sh; do
   mkdir -p "$SCR/code/$(dirname $f)"; git show "$REV:$E/$f" > "$SCR/code/$f" || exit 2
 done
+git show "$REV:$E/c1/lost-headings-at-base.json" > "$SCR/code/c1/lost-headings-at-base.json" || exit 2
```

and, closing H3, both manifest lists must gain the two files (digests are the current committed bytes):

```diff
-FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py ..."
+FROZEN="$E/contract.json $E/freeze.json $E/c2/red-before/round-54-ctl-pos-c1.stdout $E/c2/red-before/round-54-ctl-pos-c1.stdout.sha256 $E/c1/measure.py ..."
```
```diff
--- a/.ufo/evidence/round-56/freeze.json
+++ b/.ufo/evidence/round-56/freeze.json
@@
   "c2/red-before/round-54-surface.paths": "95ead282432b1bded8eaa0d9ba60e68f8d4aa06d8947d5488172f13cf0e1d880",
+  "c2/red-before/round-54-ctl-pos-c1.stdout": "3310ff60802af88993006dd1fc59b50cbcbb33b094b02ee532ac5573db455698",
+  "c2/red-before/round-54-ctl-pos-c1.stdout.sha256": "2491775e3a6b2f754bf86226fb81b51493c413fa83c47e347843494457513068",
```
and `contract.json.frozen_paths` must gain the same two paths (otherwise (a) re-opens). For M1, commit `before/c1.stdout` (`6789d9b0…`), `before/c2.stdout` (`5ec46f99…`), `before/c2-at-base.stdout` (`6fca5f29…`) at C0 and add them to both lists — or delete them and stop citing them. For the inert sidecar, `c2/measure.py` must copy `R54_SLICE + '.sha256'` into the work dir beside the slice (instrument change → amendment).

Demonstration in the scratch clone (receipt `r-patch-demo.txt`): the patched script refuses a re-frozen `FREEZE` and accepts the true one —

```
--- patched script's pin check against the re-frozen commit M4 (must refuse):
DECIDING_REFUSED freeze-not-pinned
--- and against the true freeze commit (must pass):
pin-ok
```

and patch 1 is demonstrated end-to-end by receipt `f2-c1-with-sibling.txt` (the counter runs and emits its `C1_R56:` verdict from the materialized directory).

## What this audit cannot see

- Whether the *frozen* instruments were correct at the moment of freezing: I verify identity and coverage, not intent. The `before/` receipts are uncommitted, so "the state before the freeze" is attested only by untracked files (M1).
- Whether the L1 will commit the wave reports before the deciding run (L2) — that is a process fact, not a repo fact.
- Any claim about C1/C2 arm behaviour: other seats own liveness, fuzz and mutants; I only read the counters for their freeze-relevant I/O.

## Tooling

Nothing installed; no pacman/uv/npx transaction was run. `python3` 3.14, `git`, `sha256sum` as present on the host. Census (round-start conformance, read-only): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → `census_exit=0`, `tameshi ok .../corpus/SOURCES.md` (receipt `p-base-freeze-diff-census.txt`).

## Receipts

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w1/T56W1RevFreeze-receipts/` — `a-rederive.txt`, `a2-sha256sum.txt`, `b-frozen-list.txt`, `c-freeze-commit.txt`, `d-freeze-vs-base.txt`, `e-c1-selfpath.txt`, `f1-c1-materialized.txt`, `f2-c1-with-sibling.txt`, `g-mutation-experiments.txt`, `h-inputs-and-before.txt`, `i-verbatim-check.txt`, `i2-verbatim-clean.txt`, `j-contract-vs-instruments.txt`, `k-before-tracking.txt`, `l-unlisted-freeze-files.txt`, `m-cleantree-gate.txt`, `n-sidecar-amendments.txt`, `o-counter-freeze-refs.txt`, `p-base-freeze-diff-census.txt`, `q-gate-freeze.txt`, `r-patch-demo.txt`.
