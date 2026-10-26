# T48W2RevC1Separability — C1/C2 separability and append-only (round 48, attempt 2, wave a2w1)

Seat: reviewer, leaf (no subagents). Item: at CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`
(2026-10-26 10:27:19 -03, verified `git log -1`), check (1) SCORECARD.md append-only base→CONTENT,
(2) the C1 counter reads nothing C2 writes except via the `sources-registry` row, (3) the
`sources-registry` restated row's value equals `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh`
at CONTENT, (4) whether C1 would still verify at a tree without C2's rows if the row restated that
tree's count (the contract's separability note), (5) the C2 counter reads no SCORECARD.md.

Pins verified first: both counters at CONTENT match freeze-2.json sha256s byte-for-byte
(C1 `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3`, C2
`faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f`; `git show <rev>:<path> | sha256sum`);
`statements.json` at CONTENT = `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56` (= the
freeze pin); `contract.json` sha256 = `4fff75dbaac728992fa04ffd3ccfea6ace8ca80b944cc393b63c287fadc6d59e`
(= freeze-2 `contract_sha256`). Contract read in full including all ten amendments; never edited.

**Verdict: all five checks PASS. No defect found in the C1/C2 separability surface.** Evidence per check
below; every command shown is as run. Probes are labelled `C1_R48_PARTIAL` by the counter itself and are
never verdicts; the deciding run is the L1's.

## 1. SCORECARD.md at BASE is a byte prefix of SCORECARD.md at CONTENT — PASS

```
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
B=473336d9d789f6081195e7376d17836a24666bc3; C=c7586b9a10effc63b4bd327f976edc094c1bdc17
git -C "$L" cat-file -s "$B:SCORECARD.md"        # -> 248883
git -C "$L" cat-file -s "$C:SCORECARD.md"        # -> 263506
cmp <(git -C "$L" show "$B:SCORECARD.md") <(git -C "$L" show "$C:SCORECARD.md")
# -> cmp: EOF on /dev/fd/63 after byte 248883   (exit 1 = differ only by the extra tail)
git -C "$L" diff "$B" "$C" -- SCORECARD.md | grep -E '^(@@|diff )'
# -> @@ -2316,3 +2316,52 @@   (single hunk, end of file; +49 insertions, 0 deletions)
git -C "$L" show "$B:SCORECARD.md" | wc -l       # -> 2318
git -C "$L" show "$C:SCORECARD.md" | wc -l       # -> 2367
```

The first 248883 bytes are identical and the base file ends there: a proper byte prefix. The appended
49 lines are exactly the round-48 block: `### Standing self-assessment — re-stated at round 48`
(SCORECARD.md:2324 at CONTENT) plus its two tables; `grep -cE ', runs 3 (stable|nondeterministic)'`
over the whole CONTENT SCORECARD = **22**, and the round-46/47 restatement rows carry no `runs 3`
clause, so all 22 are the round-48 rows. The frozen counter implements the same property:
`.ufo/evidence/round-48/calibration/measure.py:429` — `append_only = int(rev_sc.startswith(base_sc))`.

## 2. The C1 counter reads nothing C2 writes except via the `sources-registry` row — PASS (code level)

Grep of `.ufo/evidence/round-48/calibration/measure.py` (frozen bytes) over
`SCORECARD|SOURCES|registry|lessons|freshness|C2-QUOTE|snapshot|receipt` and
`corpus|knowledge|S26[5-8]|e0(26|48|93|108)|round-48\.md|SOURCES\.md|observations`, plus an
`open(|read_text|read_bytes|.read(|os.listdir|walk(` enumeration. The counter's complete read surface:

- `open(os.path.abspath(__file__))` (its own bytes, measure.py:410) and `git show REV:SELF_PATH` (:411) — self-pin;
- `git show REV:STATEMENTS_PATH` (:413) — the round-47 statements (sha-pinned, pre-C2 file);
- `git show BASE:SCORECARD.md` / `git show REV:SCORECARD.md` (:424-425) — its own surface;
- `open(CENSUS_SCRIPT)` = the **fleet** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, digest only (:373);
- `git status --porcelain` + `git diff --quiet REV` over `corpus`, `tools`, `SCORECARD.md` (:376-379) — emptiness metadata, not content;
- sibling `*-shokunin` HEADs (:383-388) and `/usr/bin` + fleet listdirs for shims/mirrors (:273, :307).

Zero occurrences of any C2-written path: no `corpus/SOURCES.md`, no `corpus/lessons/round-48.md`,
no `corpus/knowledge/*`, no `.ufo/evidence/round-48/freshness/`, no S265–S268, no C2-QUOTE, no
snapshot/receipt paths. `OBSERVATIONS_DIR` (:79) is defined but never read — amendment 4 removed
`load_attestations`/`attest_token` (grep: zero hits), so committed observation files are never input.

Nuance recorded (invocation level, not counter code): the counter *executes* the 22 statements' argvs
inside its own clone of REV, and two of those argvs parse the registry file that contains C2's rows:
(a) the `sources-registry` census — the designed coupling, the contract's separability note names it;
(b) the `freshness` axis statement runs the **round-45** counter
(`.ufo/evidence/round-45/freshness/measure.py`), which parses all 13-field rows at REV but its
population is capped at `id <= S160` (`MAX_ID = 160`); C2's rows are S265–S268, so they are parsed and
then excluded — value invariant (observed `9` at CONTENT and `9` at T′ below). The `retained
invocation-context gate` runs the fleet census over the live fleet root
(`.ufo/evidence/round-15/verify.py:835-837`), reading the live lane registry, but only its binary
CLEAN-ness enters the value (both the 124-row and 128-row registries are census-CLEAN — both observed
in this seat). No other statement argv names any C2-written path (statements.json grep: only the
`sources-registry` census and the round-45 freshness path; `tools/` grep for
`round-48|corpus/lessons|corpus/knowledge|corpus/SOURCES|freshness`: comments, historical data cites
and fixture strings only; `env-diff.py`: zero hits; `staged-id-guard.py`: docstring prose only; the
`--regression` replay materialises pinned blobs from the object store, immune to the worktree).

So: the counter's code reads nothing C2 writes at all, and among the statements it runs, the only
value that can move with C2's rows arrives via the `sources-registry` row — the item's claim holds.

## 3. The `sources-registry` restated row's value equals the census at CONTENT — PASS

Standing row at CONTENT (SCORECARD.md:2332, the last `runs 3` row for the id):

```
| sources-registry | curate where the lane learns: … | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → `rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0, tool sha256 `b9b754713c9c`, deps `none`, runs 3 stable | fleet round 1 (kaika) |
```

Census run in the scratch clone at CONTENT (`git clone -q --shared` + `checkout -q CONTENT`;
`rev-parse --show-toplevel` = the clone; `git status --porcelain | wc -l` = 0 before and after):

```
== A rows
128
== A malformed (must be 0)
0
== A tiers
A=114 B=11 C=3
== A status
mined=100 queued=22 rejected=6
…
== VERDICT
SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)
CENSUS_EXIT=0
```

The counter's census parser (measure.py:256-260) builds exactly `rows=128 SOURCES_CENSUS: CLEAN
(contract v1 + H4 id-or-path)` from that output — byte-equal to the row's backticked member — and the
exit is 0. Tool pin: the v2 script at CONTENT hashes
`b9b754713c9c359823e85106e0177e6678bd95b567d1c897fd7f3464945a2bc3` → prefix `b9b754713c9c` = the row's
`tool sha256`. 128 = 124 + C2's four rows: the registry diff BASE→CONTENT is exactly the four added
rows S265–S268 (`git diff --name-status` + full diff shown; nothing else in the file changed), so the
row value tracks C2's row additions, as the contract's separability note says.

## 4. Counterfactual: C1 at a tree without C2's rows, row restating that tree's count — YES (demonstrated)

Contract note (pre-registered, claims.C1.separability): *"C1 is verifiable without C2: its rows
restate whatever the tree prints. The `sources-registry` statement prints the registry row count, so
its row value tracks C2's row additions; C1 is measured at the content revision and its truth does not
depend on C2 verifying."*

Built T′ in the scratch clone (all writes in scratch; one commit, throwaway identity
`t48w2sep <t48w2sep@scratch.invalid>`), **T′ = `512a08963240cceaf5b353014be5d47267bd5350`**:

- `git checkout -q BASE -- corpus/SOURCES.md corpus/knowledge/incremental-pin-disposition.md corpus/knowledge/r8-golden-update-flag.md corpus/knowledge/regression-tally-completeness.md corpus/knowledge/repeated-control-precondition.md` (the CONTENT registry diff is exactly the four rows, so this removes precisely C2's rows; the four entries lose their re-points);
- `rm -rf .ufo/evidence/round-48/freshness/sources` (the 8 C2 artifact files: S026.html, S026.receipt.json, S048.html, S048.receipt.json, S093.receipt.json, S093.xml, S108.html, S108.receipt.json);
- SCORECARD.md:2332 `rows=128` → `rows=124` (the only C1-surface edit; BASE stays a byte prefix);
- `corpus/lessons/round-48.md` left intact — its C2-QUOTE gate lines are unread by C1 (check 2), so they cannot matter here.

Census at T′: `== A rows / 124`, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0, tree
clean. Probe (sanctioned form: scratch tree, scratch work dir, `--only`, reported as observed):

```
TMPDIR="$S/w" python3 "$L/.ufo/evidence/round-48/calibration/measure.py" \
  --lane "$S/clone" --rev HEAD --base 473336d9d789f6081195e7376d17836a24666bc3 \
  --work "$S/w/c1work" --only sources-registry,freshness,calibration --rounds 1
```

Observed at T′ (probe, `C1_R48_PARTIAL`, exit 1):

```
STATEMENT cap/sources-registry: claimed=rows=124 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 sha=b9b754713c9c ROUNDS r1=rows=124 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT axis/calibration: claimed=6 sha=657f009bdf1c ROUNDS r1=6 … MATCH DEPS-MISMATCH
STATEMENT axis/freshness: claimed=9 sha=ba64041f49ff ROUNDS r1=9 … MATCH DEPS-MISMATCH
PROFILES sources-registry: P0…P5 all = rows=124 …|0
PROFILES calibration: P0=6 P1=6 P2=6 P3=6 P4=6 P5=-
PROFILES freshness: P0=9 P1=9 P2=9 P3=9 P4=9 P5=0
C1_R48_PARTIAL: self_pin=1 stmts_pin=1 statements=3 rounds=1 append_only=1 unpinned=0 total=2 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=2 unattested=0 oversize=0 … fleet_drift=0 sibling_moves=0 rev=512a08963240cceaf5b353014be5d47267bd5350 C1_R48_PASS=false
```

The value-level counterfactual holds: with the row restated to the tree's own count, the
`sources-registry` statement — the only one whose value tracks C2's rows — verifies **MATCH DEPS-OK**
at the C2-less tree, and both axis values equal their CONTENT-declared values (6, 9).

**The two `DEPS-MISMATCH` lines are my probe's artifact, not a tree property — three independent
proofs:**

1. *Control at CONTENT:* the identical probe (`--rev CONTENT`, fresh work dir) shows the same picture —
   sources-registry MATCH DEPS-OK at 128, the same two axis DEPS-MISMATCH, `total=2` — so the anomaly is
   identical at both revs and cannot be caused by C2's rows or their removal.
2. *Root cause (P5 observation files the counter leaves in the work dir):*
   `w/c1work/round1/P5/obs-calibration.stdout` = `{"error": "blob-missing", "missing":
   ["tools/mutate-and-run.sh", "SHONEN.md", "SKILL.md", "corpus/SOURCES.md"], "rev": "512a0896…"}`;
   `obs-freshness.stdout` = `C1_R45: self_pin=0 population=0 … fresh=0 score=0`. My `--lane` was a
   `git clone --shared` of the lane: its own object store holds only locally-created blobs, everything
   else resolves through alternates into the lane's store — and P5 binds the fleet root (which contains
   the lane) to a decoy (measure.py:326-328), making the alternates target unreachable. The counter's
   `setup_profile` sub-clones (`git clone -q --no-hardlinks`, measure.py:313-315) do not inherit
   alternates, so blobs never materialised locally are missing exactly under P5. (`git fetch origin`
   does not repair a `--shared` clone — objects are already "present" through alternates — confirmed by
   an identical re-run.)
3. *Committed emit receipt (real lane as `--lane`, 3 rounds):*
   `git show CONTENT:.ufo/evidence/round-48/calibration/emit-15b1521.stdout` shows, in **all three
   rounds**, `PROFILES calibration: … P5=6` and `PROFILES freshness: … P5=9`, with
   `DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node` for both axes and for
   sources-registry — grounding the rows' `deps none` in real-lane P5 behaviour. The emit rev
   15b1521ea2e95d0d708059458c090e9f334adf32 is an ancestor of CONTENT whose registry already holds the
   four C2 rows (`merge-base --is-ancestor` = yes; `grep -cE '^\| S26[5-8] '` = 4) and whose SCORECARD
   has zero `runs 3` rows (the honest unparsed before-state), so the emit's `rows=128` observation is
   consistent at both revs.

**Answer: YES.** C1's verdict machinery contains no C2-dependence: `append_only` is graded on
SCORECARD.md, which C2 never writes (check 5); the only row value that tracks C2's rows is
`sources-registry`'s, and it is graded against the tree's own census output (measure.py:256-260), so
restating that tree's count makes it verify — observed MATCH DEPS-OK at T′; the other 21 statements'
inputs are byte-identical between CONTENT and T′ (their argvs read no C2-written file — check 2's
enumeration), and the freshness axis demonstrably excludes C2's rows from its population (id ≤ S160).
This is exactly the contract's separability note, and it is sound.

## 5. The C2 counter reads no SCORECARD.md — PASS

- `grep -i scorecard .ufo/evidence/round-48/freshness/measure.py` → **no matches**.
- Full read enumeration of the frozen C2 counter: `show_text`/`show_bytes` on `corpus/SOURCES.md`
  (BASE and REV), `corpus/lessons/round-48.md`, `.ufo/evidence/round-48/freshness/sources/T.*`
  (snapshots) and `T.receipt.json`, the BASE used-by entry paths, and its own `SELF_PATH`;
  the single `tree_paths` call uses the `SNAP_DIR` prefix only (measure.py:233); the census check
  materialises SOURCES.md and its used-by blobs into a temp dir and runs the **fleet**
  `sources-census.sh validate --file` there (:383-391) — that script contains zero `SCORECARD`
  references (grep of `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`).
- Indirect corner closed: no used-by cell in the registry names `SCORECARD.md` at BASE or CONTENT
  (`git show <rev>:corpus/SOURCES.md | grep -c SCORECARD` = 0 at both), so even `_materialise`'s
  used-by blob writes can never touch SCORECARD.md.
- Matches the contract's C2 separability note verbatim: *"C2 is verifiable without C1: it reads
  SOURCES.md, the lesson Gate lines, the entries and the snapshots, never SCORECARD.md."*

## Residual risk and verification gaps

- The counterfactual is demonstrated at probe strength: `--rounds 1`, 3 of 22 statements, scratch
  tree, label `C1_R48_PARTIAL` (the counter itself refuses a PASS verdict on probes). The remaining 19
  statements' invariance rests on the argv/grep enumeration (their inputs are byte-identical between
  CONTENT and T′), not on re-observation at T′.
- My probe's `dep_mismatch=2` (P5 alternates artifact) is documented above so no reader mistakes it
  for a C1 defect; it is absent with the real lane as `--lane` (emit receipt) and identical at CONTENT
  and T′ (control).
- Nothing here is a verdict on C1/C2; the single deciding invocation is the L1's
  (`.ufo/evidence/round-48/deciding-run.sh`, receipts under `after/`).

## Bounds and tooling

- Lane checkout untouched: only read-only git (`cat-file`, `log`, `show`, `diff`, `status`,
  `merge-base --is-ancestor`, `ls-tree` via the counters) and file reads; no `git add/commit/stash/
  checkout/switch/reset/pull/push` and no jj command in the lane; nothing written under the lane
  except this report file.
- Scratch: `/fast/scratch/hyaku/tameshi-r48/T48W2RevC1Separability` (clone at CONTENT, T′ commit,
  probe work dirs, TMPDIR) — deleted at the end of this seat; disk-guard status checked before the
  heavy pass (616.7G free on `/fast/scratch/hyaku`).
- Tooling authorization: no tool installed or upgraded (none needed); no pacman transaction.
