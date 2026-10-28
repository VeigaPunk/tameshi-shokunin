# T55W1Connector1 — sibling-overlap scan: is the `could-not-evaluate` line grammar a lane invention or a fleet pattern?

Seat: connector (leaf). Judged axis: **operability**. Milestone: cross-lane exit-class grammar.
Lane HEAD at scan: `631cd6455e58dce969310b4c0466c3383d9f5108` (tree dirty with round-55 integration; base `0a2010acd1` is an ancestor). Read-only on all siblings.
Sibling revisions read: kumitate `14057f3e38`, kagi `69b61db46b`, tsukuroi `d7cfc27308`, mado `3b55b6e91e`, souji `da920356f9`, kama `7ee8cbdf16`, game-dev-3d `89dd182b70`, kaidoku `b5c4ea603d`. **Siblings were committing while I scanned** — by write time souji is `a512efb574` and kaidoku `c0112995817` (kaidoku moved twice). I therefore re-verified every cited file **by content at the current HEAD** (`git show <HEAD>:<path> | sed -n '<line>p'`): all 28 cited files are CLEAN at their lane HEAD and all 15 sampled line-number citations still land on the quoted text (receipt `09`). None of my citations is stale, and none of the dirty paths in any lane tree (kaidoku 68, tsukuroi 33, tameshi 21, souji 5) is one I cite.

---

## 1. Verdict — the grammar is two layers, not one

The question resolves only if the grammar is split. It is **not** a lane invention and **not** a fleet pattern; it is a **fleet-admitted core plus a lane-local tightening**.

| Layer | Status | Who holds it |
|---|---|---|
| (a) exit code → class (`2` = could-not-evaluate) | **fleet-general**, protocol-pinned | `PROTOCOL.md:380-383`; kagi, tsukuroi, mado, kumitate, souji, tameshi |
| (b) one line carrying the class, exit paired | **fleet-general**, ≥2 independent lanes | kama, souji, mado, kagi, kumitate, tsukuroi (six shapes) |
| (c) `<tool>: could-not-evaluate: <detail>` prefix on a failure line | **held by 2 lanes besides tameshi** — meets tameshi's PROVINCE two-lane bar | kama (live tool), souji (round instruments) |
| (d) the **second** class token — `'<value>' (could-not-evaluate)` suffix | **zero sibling holders → tameshi-local** | tameshi only |

So: cite (a)–(c) as admitted fleet craft; (d) is this lane's own stricter shape, and the fleet **explicitly declines to pin it**.

## 2. The rule that decides "general" — tameshi PROVINCE.md:15-16

`tameshi-shokunin/PROVINCE.md:14-17` (unchanged since fleet round 1, cited by line):

> `**Refuses:** product domains — every lane's gate remains its own; tameshi`
> `owns only the reusable craft (a pattern is admitted from evidence in TWO`
> `independent lanes before it is claimed general). Never edits a sibling's`
> `gate code (read-only probes; recommendations travel in round reports).`

The bar is **two independent lanes**, not "it looks standard". Layer (c) clears it (kama + souji); layer (d) does not.

## 3. The fleet rule that bounds the claim — PROTOCOL.md:380-383

`PROTOCOL.md:380-383` (fleet gate standard), verbatim:

> `- **Verdict.** `0` = `clean` and `1` = `failed` fleet-wide; every other code a gate exits (`2`, `3`,`
> `  `64`, …) is declared in its registry entry and mapped onto `clean | failed | could-not-evaluate`,`
> `  and an undeclared nonzero code reads as `could-not-evaluate`. Nothing else is pinned: a gate's own`
> `  vocabulary — WARN vs HIT, a missing baseline, finding kinds — stays lane-owned, and this section`
> `  governs the outer interface only.`

**"Nothing else is pinned … stays lane-owned" is the disposal of the whole question.** The fleet pins the *mapping*; it deliberately does not pin the *line*. tameshi's frozen grammar is therefore a legitimate lane declaration — a lane may declare its own vocabulary in its registry entry, which `tools/registry.json` now does — but it can never be evidence of fleet conformance, and no sibling is obliged to match it.

## 4. Evidence — the holders, `path:line`

### 4.1 Layer (c): the exact `<tool>: could-not-evaluate: <detail>` prefix

Fleet-wide count of that regex (excluding `.git/.ufo/.scratch/__pycache__/node_modules`): **56 lines = souji 37, tameshi 18, kama 1** (receipt `01-prefix-form-by-lane.txt`). Outside tameshi, the substantive sites:

| lane | site | stream | exit |
|---|---|---|---|
| kama | `kama-shokunin/tools/seat-report-immutability.py:409-411` — `except EvalError as e: print("%s: could-not-evaluate: %s" % (NAME, e)); return 2` | stdout | **2** |
| souji | `souji-shokunin/census/round-19/verify-agreement-pin.py:197-198` — `print("verify-agreement-pin: could-not-evaluate: %s" % exc, file=sys.stderr); return 2` | **stderr** | **2** |
| souji | `souji-shokunin/census/round-22/mutation-adequacy.py:264-265` — `print('r22-mutation-adequacy: could-not-evaluate: ' + str(exc), file=sys.stderr); return 2` | **stderr** | **2** |
| souji | `census/round-13/run-verification.py:440`; `tests/fixtures/r22-result-oracle.py:113`; `tests/fixtures/r24-size-census.py:379` (duplicates under `census/round-32/waves/w1/deliver-*`) | mixed | 2 |

Honest qualification: **kama holds it in a live `tools/` gate; souji holds it in round instruments and fixtures — its live `tools/` directory has zero occurrences** of the prefix form (`grep -rn ... souji-shokunin/tools/` → 0 files). The two-lane bar is met on the letter; a stricter "live gates in two lanes" reading is *not* met by the prefix form alone.

### 4.2 Layer (b): one line carrying the class, exit paired — six independent shapes

| lane | declared line | pin | stream/exit |
|---|---|---|---|
| mado | `MADO_TRIPWIRE: clean \| permitted_only \| findings \| could_not_evaluate` (`tools/mado-tripwire.py:138`; emitted `:2920`, internal-error `:3459`) | **exact-string pin in the gate's own selftest**: `out[0] == "MADO_TRIPWIRE: " + case["want_label"]` (`:3365`) | stdout / 2 |
| kagi | `ADJACENCY_SCOPE: SETUP (…)` and `<tool>: <msg>` (`corpus/scope-gate.sh:83`, `:102`, `:184`) | line-shape/exit table (`corpus/knowledge/adjacency-scope.md:154`) | stderr + stdout / 2 |
| kumitate | `RECEIPT: WROTE` / `RECEIPT: VALID\|REPLAY\|TAMPERED` (`SKILL.md:624`) | "exactly two lines + trailing newline" | stdout / 0·1·2·64 |
| tsukuroi | `TSUKUROI_CENSUS_SELFTEST: PASS (n cases, m passed, 0 failed)` | **regex-pinned** `PASS_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: PASS \((\d+) cases, (\d+) passed, 0 failed\)$')` (`tools/score-selftest-mounts-r41.py:68`); `STORAGE ... state=(HEALTHY\|DEGRADED\|BLOCKED)` (`tools/score-storage-hidden-r39.py:58`) | stdout |
| kama | `could-not-evaluate: <detail>` (`tools/report-landing-audit.py:1620-1625`) | selftest arm `"could-not-evaluate-exits-2"` (`tools/seat-report-immutability.py:610-618`) | **stderr** / 2 |
| souji | `probe.status=could-not-evaluate probe.error=…` (`tools/souji-repo-structure.sh:211,231,279,287,293` — five sites) | declared exit 4 = could-not-evaluate (`SKILL.md:207`) | **stderr** / 4 |

Note the two different *devices* both live here and both matter for tameshi: a **closed enum at a fixed position** (mado, kumitate, tsukuroi) and a **class-prefixed free-text line** (kagi, kama, souji). tameshi's grammar is of the second kind.

Also relevant, the *discipline* rather than the shape — three lanes state tameshi's rule independently:

- mado: `except BaseException as exc:  # never let an internal error read as "findings"` then `MADO_TRIPWIRE: could_not_evaluate`, exit 2 (`mado-tripwire.py:3455-3459`).
- kama: `except Exception as exc:  # an unanticipated error is never a verdict` (`report-landing-audit.py:1629`).
- kagi: "Bootstrap failures must not be readable as 'drift found' … prints SETUP and exits 2 … **never a bare death**" and "the same class is present in `corpus/surface-census.sh:75` and is **reported, not silently shared**" (`corpus/scope-gate.sh:78-84`). That last clause is kagi's own version of tameshi's "the line is the contract; the Python type is not" — including the *duplicated, not shared* disposition tameshi's seven stand-alone tools take.

### 4.3 Layer (d): the duplicated class token — negative sweep

Fleet-wide, every line outside tameshi containing `could-not-evaluate` **twice**:

```
$ grep -rIn "could-not-evaluate" . | grep -v "^./tameshi-shokunin/" \
    | awk '{n=gsub(/could-not-evaluate/,"&"); if (n>=2) print}'
3x  kaidoku-shokunin/SKILL.md:761,1381,1499        (registry prose)
2x  kaidoku-shokunin/SKILL.md:1048,1422,1501,1617  (registry prose)
2x  game-dev-3d-shokunin/reports/round-103/gate/exit-codes.md:21,236,277  (analysis prose)
3x  souji-shokunin/SKILL.md:204,207                (gate-map prose)
2x  SCORECARD.md:195                               (fleet prose)
1x  kotodama-shokunin/reports/round-9/.../author.md:79  (a *test case* whose gate prints `FINDING G-DATA: [could-not-evaluate] …` — one bracket token, not a template)
```

Zero emitted code templates repeat the class. The parenthesised `(could-not-evaluate)` does appear across kaidoku (`SKILL.md:1457,1460`), tabi (`SKILL.md:2907`), lore (`corpus/tools/README.md:274`), tsukuroi (`SKILL.md:2202`) and mori (`tools/mori-round13-regressions.py:3282`) — **as exit-map prose or a single mid-line annotation, never as a suffix duplicating a prefix**. tameshi's `… '<value>' (could-not-evaluate)` is its own invention.

### 4.4 Negative control — a lane that does *not* hold the pattern

`game-dev-3d-shokunin/reports/round-103/gate/exit-codes.md:21`:

> "the lane's only classifier has **no could-not-evaluate vocabulary at all** … **exit 2 already means 'this arm PASSED'** in this lane"

This is why the claim must be written as *admitted from two lanes*, not *the fleet does this*. The pattern is general by the PROVINCE bar, and it is **not universal**.

## 5. What this changes for the round (`corpus/knowledge/scratch-root-contract.md`, item 3)

The section as it stands (tree, `## One line, every mode (round 55)`) already carries the honest type note —

> "The line is the contract; the Python type is not: the tools keep their own exception classes … because seven standalone tools should not depend on one module for a one-line rule."

— and it makes **no** general claim, so there is nothing to retract. What is missing is the *provenance*, and that absence is a calibration exposure both ways: a future reader can either overclaim ("the fleet does this") or underclaim ("we invented a grammar"), and this scan refutes both. **Proposed diff** (production file untouched by me — the L1 integrates):

```diff
--- a/corpus/knowledge/scratch-root-contract.md
+++ b/corpus/knowledge/scratch-root-contract.md
@@ ... @@ The line is the contract; the Python type is not: the tools keep their own
 exception classes (`ScratchRootUnusable` in the two round-55 edits, a local
 class in `env-diff`), because seven standalone tools should not depend on one
 module for a one-line rule.
+
+Where the shape comes from: the class is fleet, the grammar is not.
+`PROTOCOL.md:380-383` pins only the mapping (`2` -> could-not-evaluate) and
+says "Nothing else is pinned: a gate's own vocabulary … stays lane-owned", so
+no sibling owes this wording. The `<tool>: could-not-evaluate: <detail>`
+prefix on a paired exit 2 is held independently by two other lanes —
+`kama-shokunin/tools/seat-report-immutability.py:409-411` (exit 2, stdout) and
+`souji-shokunin/census/round-19/verify-agreement-pin.py:197` plus
+`:…/round-22/mutation-adequacy.py:264` (stderr, exit 2); kama also emits the
+class alone on stderr (`tools/report-landing-audit.py:1620`) and souji on
+stderr in key=value form (`tools/souji-repo-structure.sh:287`, its declared
+exit 4). That clears PROVINCE.md:15-16's two-lane bar for the prefix and the
+exit. What no sibling has is the *second* token: this line repeats the class
+in parentheses after the quoted value, and a fleet-wide sweep of every line
+holding the token twice finds only prose (round-55 wave-1 receipt
+`T55W1Connector1-receipts/07-negative-double-token-sweep.txt`). So read the
+prefix and the exit as the admitted part, the suffix and the fixed wording as
+this lane's tightening — and never cite this grammar as a fleet conformance
+property.
```

**Recommendation on item 4: do not touch `SKILL.md` again for this.** The replacement sentence already in the tree ("as one stderr line, `<tool>: could-not-evaluate: …` … round-55 C2 counter; `corpus/knowledge/scratch-root-contract.md`") is factual and already delegates to the knowledge entry. Item 4 costs one cold-read re-key; adding a provenance clause there would double that drift and buy no C2 arm, because the counter reads the registry cells and the knowledge note, not SKILL's prose. Put the provenance in the knowledge entry only — this is the "improve one axis, harm none" form of the move.

**Registry cells (item 2): no change needed.** They read `One stderr line, exit 2, could-not-evaluate: "…"` and cite `(round 55, corpus/knowledge/scratch-root-contract.md)` — a lane-local provenance, no general claim. I verified all seven cells and they are internally consistent with the contract's "eight allocating modes" (7 tools, `env-diff` carrying two: `--selftest` and `--contract`).

## 6. Contradictions stated, not smoothed

1. **PROTOCOL:382 ("nothing else is pinned") vs a frozen line grammar with a 7-tool counter.** Not a violation: PROTOCOL pins the outer interface and lets a lane declare vocabulary in its registry entry, which tameshi does. The contradiction only becomes real if the round *describes* the grammar as a fleet property. Hence §5's wording.
2. **PROVINCE's two-lane bar is met on the letter, thinly.** kama is a live holder; souji's holders are round instruments and fixtures. If the L1 wants "two live gates", layer (c) alone does not supply it — layer (b) does (kama + souji stderr `probe.status=`, mado + kagi class lines). State which bar is being claimed.
3. **kagi's class word is `SETUP`, not `could-not-evaluate`.** The *device* is shared; the *vocabulary* is not. Do not cite kagi as holding tameshi's class name.
4. **souji's class line sits at exit 4, not 2** (`SKILL.md:204,207`). Legitimate under PROTOCOL:381-383 (every non-0/1 code is declared and mapped), but it means "exit 2" is not itself the fleet invariant — the *mapping* is.
5. **game-dev-3d reads exit 2 as a pass** (`round-103/gate/exit-codes.md:21`). Any sentence of the form "the fleet treats exit 2 as could-not-evaluate" is false as written.

## 7. Risks of the proposed move

- **Length vs. the entry's register.** The added paragraph is ~150 words in a lane whose knowledge entries are dense tables; it fits, but if the L1 prefers, cut the souji/kama site list to the three primary citations and keep the receipt pointer.
- **Stale-pointer risk.** The paragraph cites sibling paths, which drift. It cites them as *provenance at a scan*, with no revision pin inside the entry; the receipt file carries the revisions (`souji da920356f9`, `kama 7ee8cbdf16`). If that is judged too loose, add the two short hashes inline.
- **No C1/C2 movement.** This move cannot change `C1_R55_PASS` or `C2_R55_PASS` — it is calibration hygiene, not a counter arm. It must not be presented as evidence toward either claim.
- **Nothing in the frozen set is touched**: `c1/measure.py`, `c2/measure.py`, `contract.json`, `freeze.json`, no-harm and deciding-run scripts are unread-for-edit and unmodified.

## 8. Sweep I ran (reproducible; receipts in `T55W1Connector1-receipts/`)

| # | sweep | result | receipt |
|---|---|---|---|
| 1 | `[A-Za-z0-9_.-]+: could-not-evaluate:` fleet-wide, grouped by lane | 56 lines: souji 37, tameshi 18, kama 1 | `01-prefix-form-by-lane.txt` |
| 2 | same, outside tameshi, code sites only | kama 1 live tool; souji 6 sites (2 stderr) | `02-prefix-form-code-sites-outside-tameshi.txt` |
| 3 | `PROTOCOL.md:376-384` + `PROVINCE.md:14-17` | quoted in §2–§3 | `03-fleet-protocol-and-province.txt` |
| 4 | kagi `scope-gate.sh` emitters + line/exit table + claim-ledger one-line rule | `:48-52`, `:78-84`, `:102`, `:184`, `adjacency-scope.md:154`, `claim-ledger.md:212-218` | `04-kagi-emitters.txt` |
| 5 | mado exact-string pin + kama prefix emitter | `:138`, `:2920`, `:3365`, `:3455-3459`; kama `:409-411`, `:84-86` | `05-mado-and-kama-emitters.txt` |
| 6 | kumitate receipt line, tsukuroi regex pins, tsukuroi QUALITY 84 | `SKILL.md:624`; `score-selftest-mounts-r41.py:68`; `score-storage-hidden-r39.py:58`; `QUALITY.md:165` | `06-kumitate-and-tsukuroi-emitters.txt` |
| 7 | **negative**: any line with the class token twice, fleet-wide | only prose/docs; **0 emitted templates** | `07-negative-double-token-sweep.txt` |
| 8 | kama/souji live stderr holders + class-exit selftest arms | `report-landing-audit.py:1620-1625`, `souji-repo-structure.sh:287`, kama `:610-618` | `08-kama-souji-live-holders.txt` |
| 9 | line-number re-verification of every cited sibling site | souji 5 sites; tsukuroi `PASS_RE:68`, `LINE_RE:58`, JSON emit `:520-527` | `09-line-number-verification.txt` |

Additional reads (no receipt, quoted inline): `kagi corpus/claim-ledger.sh:146` (`die() { printf 'claim-ledger: %s\n' "$1" >&2; exit 2; }` — 104 call sites across four kagi gates), `kumitate scripts/wave-census.mjs:626` ("Any read error … is could-not-evaluate (2)"), `tsukuroi tools/_revision.py:12` (the `RevisionError` docstring: "one finding id, exit class 2 = could-not-evaluate"), rendered by `tools/check-boot-writers.py:520-527` as JSON `"status":"CANNOT_EVALUATE"` on stdout — **not** a line, the deliberate opposite shape, `mado tools/mado-assessment.py:165-167` (`{'code': 2, 'result': 'could-not-evaluate'}`), `souji tools/souji-cert-evidence.py:178` (`EXIT_COULD_NOT_EVALUATE: "could-not-evaluate"`).

**Typo worth reporting, not fixing:** the kagi adjacency table writes `ADJACENCY_SCOPE: SETUP (…)` but `scope-gate.sh:83` actually prints `scope-gate: SETUP (…)`; the two forms are both listed on the same table row, so the table is right and the `ADJACENCY_SCOPE` prefix is the *stdout* form at `:184`. No action needed — noted so a reader does not reconcile them wrongly.

## 9. Reproduction

```sh
cd /home/vgpnk/Projects/shokunin
# the whole negative claim in one line
grep -rIn --exclude-dir=.git --exclude-dir=.ufo --exclude-dir=.scratch \
  --exclude-dir=__pycache__ --exclude-dir=node_modules "could-not-evaluate" . \
  | grep -v "^./tameshi-shokunin/" \
  | awk '{n=gsub(/could-not-evaluate/,"&"); if (n>=2) print}' \
  | grep -E "print\(|printf|>&2|file=sys.stderr"        # -> 0
# the positive claim
grep -rn "could-not-evaluate" kama-shokunin/tools/seat-report-immutability.py kama-shokunin/tools/report-landing-audit.py
grep -n "probe.status=could-not-evaluate" souji-shokunin/tools/souji-repo-structure.sh
sed -n '380,383p' PROTOCOL.md; sed -n '14,17p' tameshi-shokunin/PROVINCE.md
```

## 10. Conformance / tooling

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → **exit 0** (last line `tameshi	ok	…/corpus/SOURCES.md`; W04 duplicate-URL warnings are advisory and pre-existing).
- **No tools installed or upgraded**; no pacman, no `uv`, no binary drops. No mutating git/jj anywhere: all git calls were `rev-parse`, `status`, `diff --quiet`, `merge-base --is-ancestor`. Scratch: `$HYAKU_SCRATCH/tameshi-r55/T55W1Connector1` (created, unused for write work beyond the receipts below).
- Deliverables written: this report; `.ufo/waves/round-55/w1/T55W1Connector1-receipts/01..09`. No `.json` requested for this item (no machine-readable list in the item text), so none written.
- No lane production file was edited; the only patch is the diff in §5.
