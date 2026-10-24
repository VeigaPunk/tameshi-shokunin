# W2ReviewFrontierSourced — is the S103 citation load-bearing, or decorative? (round 36, w2)

Seat: reviewer (read-only), lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, tip `fbb01cf`.
Attack target: the sourced-claim requirement — "at least one round claim must rest on the S103
row OPENED this round". I tested the *claim* side (counterfactual: does any claim's pass/fail
change when S103's citation is removed?) as well as the *citation* side (presence, accuracy,
enforceability), not just string presence.

## Verdict line

**VERDICT: citation PRESENT and ACCURATE; NOT load-bearing in the adjudication chain — under the
counterfactual test the citation is decorative. C1's measured 6 → 8 rests on byte pins and trace
bindings, which I verified *are* load-bearing; S103 contributes no adjudicating byte. The
requirement is met under its literal reading ("…or lesson actually names S103") and failed under
its stated intent ("claim must rest on the row"). Severity: MEDIUM scoring/frontier-inflation risk,
not a broken gate.**

## What I attacked (axes)

1. **Citation presence/resolution** — receipts, lesson Gate, SCORECARD, LOG, SOURCES `used-by`.
2. **Citation accuracy** — snapshot digest/size/quote/date vs the row and the Gate.
3. **Counterfactual load-bearing (the falsifier)** — erase the citation, keep the claim, re-measure.
4. **Discrimination control** — is the claim bound to *S103 specifically* or to the whole
   `SOURCES.md` byte pin? (unrelated-row deletion control).
5. **Enforceability** — does any instrument read the citation? Does the census check used-by content?

## Findings, by severity

### 1. MEDIUM — the citation is not load-bearing: erasing it leaves C1 at 8/64/64

`refresh-receipts.json` names S103 four times in a prose field (`:32,:60,:88,:116 "cited_source"`)
plus `:125 "cited_source_row": "S103"`. I erased **all five** to `(none)` in a scratch clone and
re-ran the pinned counter:

- rev `a8458e2` (citation stripped, receipts otherwise byte-identical): `calibration_restraint_score
  8, sections_covered 64/64, reasons {'credited': 64}` — **identical to baseline**.

No instrument consumes the field: `grep -c cited_source` is **0** in both
`.ufo/evidence/round-18/measure.py` (the credit implementation) and
`.ufo/evidence/round-21/coldread/measure.py` (the selector); the word "reports" appears in
round-18 measure.py only in docstrings (`:81,:92,:1003`), never as a ledger key the gate validates.
The ledger entry key space that gates credit is `inputs` / `traces` / `commands_executed_count` /
`read_rev` / section digests — S103 is in none of them (`grep -ci s103 ledger.json` = 0).

The census validator does not check citation *content* either — only path existence
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` E11, `if [ ! -e "$dir/$path" ]` ~:563-567):

- S103 `used-by` → `corpus/QUALITY.md` (exists, never mentions S103): `validate` → **`CENSUS_EXIT=0`**,
  final line `tameshi-shokunin ok …/corpus/SOURCES.md`.
- S103 `used-by` → `corpus/knowledge/does-not-exist-s103.md` (control): `E11 S103 missing used-by …`,
  `CENSUS_EXIT=1`.

So "mined" is falsifiable only as "the named path exists". The w1 gate audit discharged the same
requirement by counting strings (`ScribeGateAudit.md:37` item 10, `:98` caveat C6 "cited, not
exercised, at that consumer"); this measurement shows the stronger fact — **the reference can be
deleted entirely without moving the number**.

### 2. MEDIUM (same finding, control) — the claim is bound to `SOURCES.md` bytes, not to S103

Deleting the S103 row at the measured rev *does* drop credit — but so does deleting an unrelated row:

| probe (scratch clone, own commit) | rev | monitor |
|---|---|---|
| baseline, lane tip | `fbb01cf` | 8, 64/64, `{'credited': 64}` |
| A: S103 row deleted | `eca5321` | 6, 63/64, `input-drift:…corpus/SOURCES.md…` |
| A2: **unrelated S092 row** deleted, S103 intact | `d891b5e` | 6, 63/64, same `input-drift` reason |
| B: S103 citation erased from receipts | `a8458e2` | 8, 64/64 (no change) |

A and A2 are the same failure mode (`SOURCES.md` is a pinned input of section 131 at `read_rev`;
any byte change drifts it). This proves the pin works and simultaneously proves it carries **no
S103-specific** information — the observable is file identity, not the source row.

### 3. LOW — Gate word count is wrong (19 vs 18)

`corpus/lessons/round-36.md:38` says `"…with the contents of the named file" (19 words)`. The quoted
sentence is **18 words**: `Computes(1) the(2) object(3) ID(4) value(5) for(6) an(7) object(8) with(9)
specified(10) type(11) with(12) the(13) contents(14) of(15) the(16) named(17) file(18)`. The round-36
verifier spot-check already records 18 (`corpus/lessons/round-36-verifier-spotcheck.md:77`), so the
lesson and its own spot-check disagree. The quote itself is exact (see positives).

### 4. LOW — receipt `--out` is a lane-absolute path; re-running the receipt argv writes the lane

`refresh-receipts.json` receipts embed `--out /home/vgpnk/…/.ufo/evidence/round-36/coldread/traces/L1/
source-N.json`. Running the recorded argv verbatim (the natural reproduction move) **overwrites four
committed evidence files** — I did exactly that while checking reproducibility. Restored
byte-exactly from the commit (`git cat-file blob HEAD:<path>`), worktree hashes now equal the blob
hashes (`908dfa76…`, `1e23a1ad…`, `c039d691…`, `065c4a14…`) and `git status --porcelain .ufo/evidence`
is clean. No content damage; the footgun is in the receipt's argv design (a `--out` under the
measured tree with no "scratch-only" guard), not in the traces.

### 5. LOW — zero-length measurement interval and a dead `/tmp` instrument root

Both receipts record `measurement_interval.start == end` (no duration), and `argv[0]`/`--root` point
at `/tmp/tameshi-r36-refresh-08zapax9/lane`, which no longer exists. Reproducible only by
substitution; substitution reproduces the digests exactly (below), so this is a provenance-quality
note, not an evidence defect.

## Positives verified (what survived attack)

- **Citation resolves everywhere it is claimed.** `SOURCES.md:112` row (tier A, `mined`, opened
  2026-10-24, recheck 365d, `used-by` = receipts + lesson, both exist); lesson Gate
  `corpus/lessons/round-36.md:31-42`; `SCORECARD.md:1769` ("Frontier: S103 opened and mined");
  `LOG.md:1932`; receipts `:32,:60,:88,:116,:125`; `contract.json` `new_source_row`.
- **Row facts are exact.** Snapshot sha256 `dd826dae…` = contract = row = lesson; size 29,933 bytes
  = row; the quoted sentence is verbatim at char 2980 of the tag-stripped, whitespace-collapsed
  snapshot text ("…DESCRIPTION Computes the
  object ID value for an object with specified type with the contents of the named file (which can be
  outside of the work tree)…"), so the row's teaches-cell ("a blob's ID is computed from the contents
  … a recorded digest binds audit evidence to exact bytes") is the page's own claim.
- **The byte-identity discipline the citation names IS load-bearing — and it is enforced.** Two
  independent breakers drop the claim:

  | probe | rev | monitor |
  |---|---|---|
  | C: trace for section 375 → `source-4.json` | `979b7ec` | 6, 63/64, `…trace-input-unrecorded:corpus/knowledge/closeout-r11.md` |
  | D: recorded `LOG.md` digest → zeros (round-36 entry 131) | `849817f` | 6, 63/64, `input-drift:LOG.md;…` |

  Erasing the *citation* (B) changes nothing; breaking the *digest* (C/D) breaks the claim. That is
  the correct direction of dependence, and it is the exact round-35 regression mechanism.
- **Receipt digests are real, not fabricated.** All four `stdout_sha256` reproduce byte-exactly from
  the `e423c41` blobs (inner command only, no wrapper): `b17c30ea…`, `913f4064…`, `b56fa112…`,
  `05c7ce3f…` — 4/4 MATCH (8,931 / 2,271 / 2,940 / 1,009 stdout bytes).
- **Ledger section/input digests verify.** All four round-36 entries' `skill_sha256`/section `sha256`
  reproduce under the round-18 canonical normalization (trailing whitespace-only lines stripped,
  `\n`-joined), and every `inputs` digest matches the `e423c41` blob (SKILL `238187…`, LOG `a2223d…`,
  SCORECARD `1b0124…`, QUALITY `f7382e…`, README `7c0fe5…`, SOURCES `16fae0…`, closeout `f0894b…`,
  survivor-fixture `116b56…`, runner `a7d3f2dd…`).
- **"Only delta" holds semantically.** `e423c41` → `b455001` ledger: 493 → 497 entries, existing 493
  semantically identical, added starts `[131, 375, 1380, 1436]`, added `read_rev` all `e423c41…`;
  `schema`/`carried_from`/`provenance`/`round21_provenance` unchanged. (The 80k-line textual diff is
  JSON re-indentation only.)
- **Honest saturation.** The receipts' scope line ("L1-author input-keyed source reads only; not
  independent/blind cold-read, recipe re-execution or required-command coverage") is carried in the
  lesson `## Holds` and SCORECARD; no claim upgrades it to a blind cold-read.

## Exactly what I ran (all read-only against the lane; scratch under `/fast`)

Scratch root: `/fast/scratch/hyaku/tameshi-r36-seats/W2ReviewFrontierSourced/`.

```
# pristine extract of e423c41 for digest work
git archive e423c41 | tar -x -C $S/lane
# receipt stdout reproduction (inner argv only)
python3 -c '<inner command from receipt argv, root substituted to $S/lane>'
sha256sum .ufo/evidence/round-36/coldread/traces/L1/*.json
python3 - <<'EOF'  # ledger section + input digests vs git show e423c41:<path>
EOF
# baseline + mutants, each its own `git clone --shared` of the lane
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev fbb01cf   # 8, 64/64
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev eca5321   # A  : 6, 63/64
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev d891b5e   # A2 : 6, 63/64
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev a8458e2   # B  : 8, 64/64
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev 979b7ec   # C  : 6, 63/64
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev 849817f   # D  : 6, 63/64
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev eca5321 --explain
# census: scratch fleet copy of HEAD, used-by mutants
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate $S/fleet/tameshi-shokunin
# ledger semantic diff
python3 - code comparing git show e423c41:<ledger> vs b455001:<ledger>
```

Notes: no `pacman`; no tool installs/upgrades (nothing needed); no subagent dispatch; no mutating
git/jj on any real checkout — clone-local commits only in `/fast` scratch. The single exception to
"read-only everywhere" is disclosed in finding 4: my reproduction of the receipt argv wrote four
trace files inside the lane, and I restored them byte-exactly (hashes above, porcelain clean).

## Verification gaps / residual risk

- **`lsp` device unavailable in this runtime** (no `lsp` tool exposed; `xd://` lists only
  `ast_edit`, `debug`). Caller/consumer questions were therefore settled by executing the
  instruments and by static reading of `.ufo/evidence/round-18/measure.py` + the round-21 selector,
  not by semantic IDE references. The "no consumer" conclusion is grounded in `grep -c = 0` plus a
  behavioural null (mutant B), which is stronger than grep alone.
- **The deleted `/tmp` instrument root** means I could not re-run the *wrapper* itself; I reproduced
  the inner command's stdout digests (4/4) but not the wrapper's own JSON emission path.
- **Mutant B erases the citation but leaves the S103 row**; I did not test "row deleted *and*
  receipts citation intact at a rev whose SOURCES.md still matches the pin" — impossible, since the
  pin is on the file's bytes (that impossibility is finding 2).
- **"Rest on" may be intended in the weak/citation sense.** If the round's rule is literally "the
  receipts/lesson name the row", the requirement passes and finding 1 is a design critique of the
  frontier metric (an unfalsifiable `mined` status). I flag it as MEDIUM rather than blocking on
  that ambiguity, and state both readings explicitly.
- Not in scope / N-A here: canonical-runtime routing, same-identity rerouting,
  `resume_continuity_v1` preflight rejection (no resume path in this claim), C2's counter predicate
  (other seats).
