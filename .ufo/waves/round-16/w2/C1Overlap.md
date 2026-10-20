# C1Overlap — sibling-overlap after landing (round 16, wave 2)

**Verdict (one line): holds — neither landed artifact claims a kumitate gate fix, certification, or re-pin authority; kumitate is byte-identical and porcelain-clean; the six owner items are phrased as reports; kaidoku and kama wrote only inside their own trees. Four non-blocking record/wording nits in tameshi's own text are named in §6.**

- Lane revision read: `c699c8c36d6e4eca4b796b81a8247904aa145ec8` (tameshi-shokunin).
- Artifacts attacked: `corpus/knowledge/mutation-case-kumitate-round-gate.md` (case 7) and the `PROVINCE.md` round-16 append (`PROVINCE.md:48-66`), plus the sibling-lane trees.
- Scratch: `/tmp/tameshi-r16w2-C1Overlap-Tpc5po`. No tools installed or upgraded (node v24.21.0 already present).

## 1. Boundary inventory — every kumitate-facing assertion in the two artifacts

| claim | artifact:line | form | verdict |
|---|---|---|---|
| target is a byte copy, tree read-only | note:7-9 | record | **verified** — pin and tree state re-derived (§2) |
| "No owner opt-in exists or was needed" | note:10-13; PROVINCE:55-56 | tameshi's own province | **holds, not a kumitate claim** — `PROVINCE.md:7-11` makes `kumitate/scripts/*` tameshi's read-only primary surfaces; the protocol's opt-in governs lane-requested *services* (`service-optin-protocol.md:16-30`) |
| rate limited to this suite/pin | note:126-127 | record | **verified anti-certification** — "not of kumitate's gates in general" |
| CKIND survivor is not a gate defect | note:87-92 | record | **verified anti-certification** — "recorded as that, not as a detection gap in the gate" |
| six owner recommendations | note:131-135 | report, not absorbed | **verified report form** (§3) |
| seventh ledger leg, read-only probe | PROVINCE:51-57 | record | **verified** — `js-round-gate` is the seventh leg, `mutate-and-run.sh:85-91` |
| kumitate carries seven gates | PROVINCE:61-62 | correction | **verified** — 7 `scripts/*.mjs`, all with `--selftest`; `sources-check.mjs` added in `1a8eed5` (2026-10-19) |
| tsukuroi r5 self-service, mado r6 service | PROVINCE:63-64 | correction | **verified** — protocol table at `service-optin-protocol.md:36-37` |
| kimi template path resolves | PROVINCE:65-66 | correction | **verified** — `/home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md:6-19` exists and shows the Core/Frontier/Adjacent shape |

No line in either artifact asserts the right to patch, repair, certify, absorb, sign off, or re-pin a kumitate gate; the only re-pin language in the corpus's protocol is `service-optin-protocol.md:75-77` — "The service never edits, repairs or re-pins the gate; a needed change is a recommendation to the owner, not a patch" — and the case note obeys it.

## 2. Kumitate tree unchanged — commands, exits, key lines

All commands run at open and again at close of this seat.

```
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kumitate-shokunin status --porcelain
  → (empty), rc 0  [both at open and at close]

git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin rev-parse HEAD
  → 1770305fae20826b39905a8251ddeca6b4957ac4   (unchanged)

sha256sum kumitate-shokunin/scripts/round-gate.mjs
  → f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9

git -C kumitate rev-parse HEAD:scripts/round-gate.mjs
  364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs
  175de6ba:scripts/round-gate.mjs
  → all three = 1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3   (the note's :7 "same blob")

git -C kumitate log -1 --format='%H %ad' -- scripts/round-gate.mjs
  → 364f1d5… 2026-10-13 22:49:20 -0300   (the note's "last-touching commit")

size 80415 · 1511 lines · mode 100755   (all three match note:16-18)
file mtime 2026-10-13 22:01:24 -0300     (predates this round; no write during it)
```

`git ls-tree -r --name-only c699c8c | grep round-gate` returns only `.ufo/evidence/round-16/round-gate/*` artifacts, the survivor probes, and the case note itself — **no source copy and no patched gate anywhere in the tameshi tree**. The landing commit touched no file under `kumitate-shokunin` (separate repo; clean status suffices).

Ancillary fact used by the note: `git -C kumitate grep -nIc -i tameshi HEAD` → **rc 1, no matches** — kumitate has recorded no opt-in request, so "no owner opt-in exists" is textually true; the precedent (`claims-check`, case 6) was swept the same way.

## 3. Owner recommendations are reports — exact text and vocabulary

`corpus/knowledge/mutation-case-kumitate-round-gate.md:131-135`:

> Recommendations for the owner, reported and not absorbed: a `--tracked` missing-reports-dir fixture (B2), a full-line pin on rt8 (A3), a detail-tail assert on one fail-closed fixture (A2), a set-value `UFO_SRC` fixture (E1), a point pin of the floor constant (C1059), and an `observed ⊆ enum` check (CKIND).

- Vocabulary scan of the whole note for `certif|admit|approv|authoriz|authority|patch|repair|re-pin|owner|absorb|sign-off` yields exactly two substantive hits — line 10 (the boundary sentence) and line 131 (the recommendation line); the third grep hit, line 59, is the substring "prefix" in "rt8's prefix regex".
- The `PROVINCE.md` append (`:48-66`) has **zero** hits for `must|should|needs?|required?|fix|patch|apply|adopt` (grep rc 1).
- `PROVINCE.md:14-18` states the governing rule the note follows: "Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)."

## 4. Re-execution — one named instruction set reproduced end to end

I ran the case-7 reproduce block from the landed page against git-materialized bytes (tool, spec, suite, target), all in `/tmp`:

```
runner sha256 89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594  (= runner-sha256.txt)
target sha256 f890e277…d3e9   spec sha256 e99b87eb…11c4 (= sweep/spec.copy)
node v24.21.0

CONTROL: GREEN (exit=0)
A1 KILLED  A3 KILLED  B1 KILLED  E3 KILLED  C1060 KILLED
C1059 SURVIVED  A2 SURVIVED  B2 SURVIVED  CKIND SURVIVED  E1 SURVIVED
MUTATE_RESTORE: OK (before = after = pristine f890e277…)
```

5/10 killed, 0 inconclusive, 10/10 predictions held — identical to the recorded table (`sweep/results.tsv`). Wall 40.45 s vs the note's 32 s (the note's figure is the sum of per-run `duration-ms`; verdicts are the invariant, host load is not).

Other record anchors that reproduce:

- **Pre-registration ordering.** `predictions.json` and `round-gate.defects.spec` were both added in `e69b488` (committer date `2026-10-20T10:39:59-03:00`); `registered_at_utc=2026-10-20T13:39:42Z`; sweep `13:40:15Z`. Predictions precede the sweep by 33 s.
- **Nested tally claim (note:69-71).** The committed `[51/60]` detail tails are `A1 50/60, A3 58/60, B1 58/60, C1060 59/60, E3 59/60` — **exactly the note's numbers**. The outer summaries are `49/57/57/58/58`; the note's parenthetical is the *nested* tally that the outer `[51]` line reports. A direct rerun of mutant A1 reproduced both: outer `ROUND_GATE_SELFTEST: 49/60`, `[51]` tail `50/60`; with `KUMITATE_ROUND_GATE_NESTED=1` the gate prints `SKIP [51/60]` and `50/60`.
- **Determinism claim (note:27-30).** `tools/repeat-control.py --runs 8` on the pristine suite: 8 × exit 0, stderr 0 bytes, stdout 10167 bytes each, **9 changed lines per run**, identical after normalizing the per-run `mkdtemp` tokens → `REPEAT_CONTROL: controls_mismatch`, rc 1. The note's "one mkdtemp suffix, 9 lines per run" is exact.
- **Ledger receipts.** `runner-regression.txt` → `REGRESSION_CASE js-round-gate: PASS … cases=7 passed=7`, rc 0; `runner-selftest.txt` → `MUTATE_SELFTEST: 81/81 pass`; committed tool sha equals the §5 receipt (`89722ddb…`).
- **PROVINCE append counts.** 7 `scripts/*.mjs` in kumitate at HEAD, all 7 contain `--selftest`; six-leg list at `e69b488:tools/mutate-and-run.sh:84-89`, seven-leg list at `c699c8c:…:85-91`; S052–S057 are all `mined` in `corpus/SOURCES.md:61-66`, satisfying the Core-admission rule at `PROVINCE.md:40-42`.

## 5. Sibling lanes — nothing tameshi owns was touched

```
git --no-optional-locks -C kaidoku-shokunin status --porcelain
  → M/?? only under .ufo/waves/round-17/…   (its own tree)
git -C kaidoku-shokunin log -8 --name-only --format='%h %s' | grep -i tameshi
  → 0 lines
git --no-optional-locks -C kama-shokunin status --porcelain
  → ?? .ufo/waves/round-16/{build,falsify}/…, __pycache__/   (its own tree)
git -C kama-shokunin log -8 --name-only | grep -i tameshi
  → .ufo/waves/round-16/build/advice/ConnectTameshi.md  — inside kama's repo; header reads "Seat: read-only connector", advice only
```

Fleet-root writes are attributable elsewhere: `.ufo/state/*.report-baseline` (including `tameshi.report-baseline`) are written by `scripts/shokunin-watchdog.sh` (grep hit), mtime 10:14, before the 10:49 landing; `.ufo/watchdog.log` 10:51; untracked `scripts/hyaku/jj-lane*.sh` are the jj harness (this session's `JjLaneHelper-3`), not the sibling lanes. No file under `tameshi-shokunin` was written by kaidoku or kama. The post-landing tameshi writes are wave-2 in-lane outputs only: `w2/*` (10:53-10:59), `w1/Overlap1.md` (10:49:59), `corpus/lessons/round-16.md` and `.ufo/evidence/round-16/measure.py` (10:52), and the wave-2 coldread/C1059 evidence files (10:54-10:58).

## 6. Findings — non-blocking, for the L1

1. **Skip wording (note:71-73).** "No check was skipped in any run" is true of the outer runs (control + all 10 mutants: 0 `SKIP` lines) but **false for the nested runs**: `round-gate.mjs:1381-1382` replaces the recursive hermeticity check with `{ok:true, skipped:true}` printed as `SKIP`, and `:1498` (`results.filter(r => r.ok)`) counts it as passed. That auto-pass is precisely why the note's nested tallies are one above `60 − failures`. Suggested repair keeps the line count: "no skip in any outer run; each nested run carries the recursion guard's SKIP, counted as a pass."
2. **Census staleness (pre-existing, not introduced).** `corpus/knowledge/fleet-suite-census.md:607-615` still reads "Still unmeasured, kumitate's five" and lists `round-gate` (and `claims-check`) unmeasured. The note is dated 2026-10-14 (round-5 receipt), so it is a historical snapshot, but §R.4's present tense now contradicts case 7 and `PROVINCE.md:51-57`. One dating clause ("at the round-5 write") removes the contradiction; the census is another seat's surface — route through the L1, do not edit here.
3. **"round-1 six-leg anchor" (PROVINCE:56-57).** The line numbers verify against `e69b488:…:84-89`, but the six-leg list landed at r10-2 (`tools/mutate-and-run.sh:81`; `git log -S js-claims-check` → `606716f`, round 10). The phrase means "the anchor in the fleet-round-1 section"; "r10-2 six-leg anchor" would be unambiguous.
4. **"0 entries before and after" (note:9).** The "after" state is verified; the "before" capture is not retained. Immaterial here (kumitate HEAD unchanged since 2026-10-19, target mtime 2026-10-13), but it is a claim with no receipt.

No finding blocks the landing, and none is a kumitate-ownership breach.

## 7. Axes, bounded proposal, risks, verification

- **Axes.** Depth: case 7 is an independent seventh ledger leg — distinct gate, distinct bytes, pre-registered predictions, and a reproduce block that reruns clean; it does not re-analyse an existing case. Calibration: every measured number in the note and the append reproduces; the two nits above are wording, not measurement. Neither axis is harmed.
- **Proposed move (one, bounded).** In the L1's landing repair, edit only the two tameshi-owned text items — the note's skip sentence (finding 1) and the census's R.4 date stamp (finding 2) — keeping line counts unchanged so self-anchors resolve; leave `PROVINCE.md`'s line numbers and kumitate untouched, and re-open no sweep.
- **Risks.** (a) The census is shared corpus surface: change it only through the L1's integration, and only with a dating clause, never a rewrite of measured rows. (b) The note's self-anchor rule is line-count preservation — any repair must stay within the existing paragraph. (c) Do not "fix" the gate: the SKIP is kumitate's deliberate recursion guard; the defect, if any, is only in tameshi's prose.
- **Verification.** `git -C kumitate … status --porcelain` empty; `sha256sum kumitate/scripts/round-gate.mjs` = `f890e277…`; rerun the reproduce block (expect `CONTROL: GREEN`, killed set `A1 A3 B1 E3 C1060`, `MUTATE_RESTORE: OK`); `python3 tools/repeat-control.py --runs 8 …` → `controls_mismatch` rc 1. All four were executed above.
