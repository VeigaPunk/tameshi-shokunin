# Wave 1 — C2 fixture discrimination (MutC2Fixtures)

Seat: L1Tameshi42.MutC2Fixtures. Date: 2026-10-25.
Role: for each of the 10 C2 fixtures, name a plausible wrong v4 behaviour that ONLY that
fixture catches (or note redundancy), grounded in the v3 and junk control receipts, plus
empirical mutant probes. No lane files edited.

## Evidence base (all runs on scratch clone /tmp/tameshi-r42-MutC2Fixtures-1792920506,
git clone --shared of the lane; deleted after the run)

- Counter: `.ufo/evidence/round-42/census/measure.py` (sha pin 3c3727ec…, self_pin=1 at
  rev c77c2b7e… / freeze 322b5cd3…).
- Control receipts reproduced byte-identical:
  - junk: `python3 <clone>/.ufo/evidence/round-42/census/measure.py --lane <clone>
    --rev c77c2b7e64d2e356381441ecf94abac03e984606
    --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f
    --tool-file <lane>/.ufo/evidence/round-42/control/junk-tool.py`
    → identical to `control/c2-junk.stdout` (tool sha 99424c38…, fixtures_pass=1/10).
  - v3: same with `--tool-file <lane>/tools/write-path-census-v3.py --text-mode`
    → identical to `control/c2-v3-in-slot.stdout` (tool sha 095924a7…, fixtures_pass=8/10).
- 8 mutant probes: mock v4s built on v3's `classify_source` (same loader as junk-tool.py),
  each injecting one plausible wrong-v4 behaviour; run via `--tool-file` in control mode.
  Files: `<clone>/mocks/M{1..8}_*.py` (mf; not part of the lane).

### Fixture fingerprints from the two receipts
- v3 in v4 slot fails exactly **F01 (scratch=0 want 1), F04 (explicit_out=0 want 1)** +
  live 1682/1685 (scratch), 123 (explicit_out). So F01/F04 are the only fixtures that
  positively assert the two NEW capabilities (attr+scratch; outflag). All other 8 pass.
- junk (forces everything not-unflagged, keeps v3 expected/scratch) fails **F01 (scratch),
  F04 (explicit_out), F02 F03 F05 F06 F07 F08 F09 (unflagged=0 want 1)**; only **F10**
  passes. So F02/F03/F05/F06/F07/F08/F09 are pure unflagged-restraint guards, and F10 is
  the sole fixture that demands a *certain* classification for a plain (non-attr,
  non-flag) write path.

## Per-fixture unique wrong-v4 behaviour (each verified empirically: the probe kills
exactly that fixture beyond the v3-baseline failures F01-scratch/F04-explicit_out)

| Fixture | Wants (bits, needle) | Only-this-fixture catches | Probe → exact FAIL line |
|---|---|---|---|
| F01_attr_scratch | expected=1 scratch=1 explicit_out=0 unflagged=0, needle `mkdtemp` | attr-bound dest resolved but **mkdtemp provenance dropped** (scratch stays 0; resolved no longer names mkdtemp). The only fixture needing scratch=1 and the mkdtemp needle. | M1_attr_resolve_no_scratch → `FAIL F01_attr_scratch scratch=0 want 1` (F02/F03 stay green) |
| F02_attr_golden | expected=1 scratch=0 explicit_out=0 unflagged=1 | **over-resolution of a single-binding literal-rooted attr** (reports certainty / unflagged=0 for `self.root='golden'`). F03 is not hit by the single-binding form (it has a rebind). | M2_attr_resolve_all → `FAIL F02_attr_golden unflagged=0 want 1` |
| F03_attr_ambiguous | expected=1 scratch=0 explicit_out=0 unflagged=1 | **init-binding snapshot leaks scratch across `rebase()`** (scratch=1 want 0) — the only fixture whose attr is rebound; F02 cannot see this (no scratch-capable init). | M2_attr_resolve_all → `FAIL F03_attr_ambiguous scratch=1 want 0` |
| F04_outflag | expected=1 scratch=0 explicit_out=1 unflagged=0, needle `--out` | outflag resolution present but **explicit_out bit not set**, or **resolved text lacks `--out`** (the only fixture with an explicit_out needle). | M4 variant → `FAIL F04_outflag resolved lacks '--out'` |
| F05_inflag | expected=1 scratch=0 explicit_out=0 unflagged=1 | **non-output option (`--input`) misclassified as an output flag** (explicit_out=1). F06 uses a real `--out` and is unaffected. | M3_inflag_as_out → `FAIL F05_inflag explicit_out=1 want 0` |
| F06_outflag_mixed_callers | expected=1 scratch=0 explicit_out=0 unflagged=1, exactly 1 expected site | **outflag resolution applied despite mixed callers** (one `--out`, one literal) — the "traced through every in-module call site" gate. Also catches double-expected-site splitting. | M4_mixed_caller_out → `FAIL F06_outflag_mixed_callers explicit_out=1 want 0` |
| F07_module_constant | expected=1 scratch=0 explicit_out=0 unflagged=1 | **bare module-level constant NAME no longer followed to its value** (expected drops to 0). Near-redundant with F08; split only by join-vs-bare form. | M7_constant_name_lost → `FAIL F07_module_constant expected-value sites=0, want 1` |
| F08_variable_join | expected=1 scratch=0 explicit_out=0 unflagged=1 | **module-level `os.path.join` fold no longer evaluated** (expected drops to 0). Near-redundant with F07. | M8_module_join_lost → `FAIL F08_variable_join expected-value sites=0, want 1` |
| F09_symlink | expected=1 scratch=0 explicit_out=0 unflagged=1 | **symlink-creation write sites dropped from the census** (0 expected sites) — the only non-open/write_bytes write channel among fixtures. | M5_drop_symlink → `FAIL F09_symlink expected-value sites=0, want 1` |
| F10_update_flag | expected=1 scratch=0 explicit_out=0 unflagged=0 | **plain guarded golden writes drift into the unflagged set** (conservative over-flagging) — the only fixture asserting certainty on a non-attr/non-flag write; the only fixture that even the degenerate junk tool passes. | M6_conservative_unflag → `FAIL F10_update_flag unflagged=1 want 0` |

Redundancy notes: F02/F03 are a pair (jointly kill any resolve-all-attr mutant; M2 kills both
while F01 + live attr sites pass) — F02 pins the unflagged bit, F03 pins the scratch bit.
F07/F08 are near-duplicates differing only in join-vs-bare-constant form; a defect hitting
both forms is caught by either, only the single-form defects are unique.

## Fixture × defect matrix
Defect classes: D1 attr resolution absent; D2 attr scratch provenance dropped; D3 literal-rooted
attr over-resolved (single binding); D4 rebound attr scratch leak; D5 outflag resolution absent;
D6 outflag resolved w/o `--out` text; D7 inflag misclassified as outflag; D8 outflag over-applied
on mixed callers; D9 module constant name unfollowed; D10 module join fold lost; D11 symlink
writes dropped; D12 plain writes drift to unflagged.

| | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F01 | × | **×** | | | | | | | | | | |
| F02 | | | **×** | | | | | | | | | |
| F03 | | | | **×** | | | | | | | | |
| F04 | | | | | × | **×** | | | | | | |
| F05 | | | | | | | **×** | | | | | |
| F06 | | | | | | | | **×** | | | | |
| F07 | | | | | | | | | **×** | | | |
| F08 | | | | | | | | | | **×** | | |
| F09 | | | | | | | | | | | **×** | |
| F10 | | | | | | | | | | | | **×** |

(× = caught; **×** = unique to that fixture. D1 additionally caught by live 1682/1685,
D5 by live 123. No fixture pair beyond F02/F03 and F07/F08 shares a defect signature.)

## Defect classes NO fixture catches
1. **expected=False quadrant entirely absent**: all 10 fixtures demand expected=1; none asserts
   a non-expected write site (e.g. temp leaf not `expected.json`/golden). A tool that drops or
   misbits non-expected writes passes; extra false-positive non-expected sites pass (check_site
   only counts `expected=True` sites).
2. **`kind` never asserted**: a v4 emitting kind='bogus' on every site passes (only the four
   bits + needle are checked).
3. **`resolved` text fidelity beyond two needles**: only F01 (`mkdtemp`) and F04 (`--out`)
   carry needles; for F02/F03/F05/F06/F07/F08/F09/F10 the resolved string may be empty or
   garbage and still pass.
4. **attr × outflag interaction**: no fixture combines both new capabilities in one file
   (priority/conflict rules untested).
5. **argparse option-style variants**: fixtures only use `parser.add_argument('--out')` +
   `parse_args()`; `--out=x`, `default=`, aliases, subparsers, `parse_known_args` untested.
6. **Attribute-binding contexts**: only direct `__init__` instance binds are exercised; class
   body attrs, `@property`, inherited/superclass attrs, helper-method binding, `setattr`,
   conditional/looped reassignment are untested.
7. **Other scratch markers / write channels**: only `mkdtemp` (F01, live) among
   SCRATCH_MARKERS; only open/write_bytes/os.symlink among write kinds. `NamedTemporaryFile`,
   `TemporaryDirectory`, stdout writes, fd writes, `os.rename` (a v3 kind), `Path.touch`,
   `subprocess` redirection are untested.
8. **Flag scope semantics**: v3's `flagged` is file-global; no fixture tests a flag string in
   an unrelated function/comment leaking onto another site, or per-site vs global flagged.
9. **Line numbers**: fixture checks locate the site by `expected=True` (lineno=None); only the
   3 live sites assert exact linenos. A v4 with correct bits at wrong linenos passes all 10.
10. **Robustness**: all fixtures are valid Python; parse-error handling, non-zero exit, timeout,
    unparseable JSON are caught only globally (run_errors), never per-fixture.
11. **Multiple-site behaviors**: only F06 has two writes; site ordering, dedup, duplicate
    linenos, extra JSON keys are unasserted.

## Could not check
- Real v4 bytes do not exist at base/freeze (tools/ holds only write-path-census{,v2,v3}.py);
  intended v4 semantics inferred from contract C2 text and fixture declarations only.
- Knowledge entry `corpus/knowledge/r42-attribute-and-outflag-destinations.md` cited by the
  contract is absent from the tree at freeze — not needed for the discriminator analysis.
- Tooling: no installs/updates performed (system python3 + git used throughout).
