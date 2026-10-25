# CriticDepth — round 42 wave 2 (FALSIFY): C2 as depth / capability

Seat: `L1Tameshi42.CriticDepth` (critic, read-only). Accessed 2026-10-25. Lane read at integration tip
`a21845f523b75adbd3e3f7a62af91294db224ad9` (labelled **pre-run**); v4 sha256 `784de4c0…22fe5`.
The only counter run was a `--tool-file --text-mode` control (prints `C2_R42_CONTROL`), never the measurement.
Scratch dirs `/tmp/tameshi-r42w2-CriticDepth-{ctl,probes,shift}` were deleted before return. No tools installed.

Axes: **depth** (does v4 add a resolution edge, or re-score a held rule?), **load-bearing** (does a gate consume
it?), **admission evidence** (what proves it outside the gameable predicate?).

## F1 — Attr and method are new edge classes. Outflag is a new edge plus a re-score of the held F4 rule

- **Attr and method: depth, survives.** v4 adds two resolution edges: the class-wide `self.<attr>` binding
  (`tools/write-path-census-v4.py:111-132`, used at `:207-209`) and the same-class return fold (`:134-146`, used at
  `:195-199`). They feed v3's unchanged scratch rule (`SCRATCH_MARKERS`, `:373-375`). The rule is the same; the
  graph it reads is deeper.
- **Outflag: mixed.** The edges are new: argparse dest derivation (`Module`, `:74-99`) and the call-site parameter
  trace (`_param_args` `:227-257`, `_parse_args_ns` `:260-275`, `_out_flag` `:278-311`). The verdict changes, though. v3 computed
  `'unflagged': expected and not scratch and not flagged` (`write-path-census-v3.py:177`). v4 adds
  `and not explicit_out` (`v4:385`), a new exemption from the rule the lane holds. That rule says "The rule this entry
  admits is the flag itself: a write of an expected file is a flagged path"
  (`corpus/knowledge/r8-golden-update-flag.md:14`).
- Round 41 already filed `registry-replay.py:123` as "a real non-scratch write … That is a classification gap,
  not a hidden update" (`corpus/knowledge/r41-variable-destination-writes.md:57-61`). Round 42 counts it as one of
  "the three live v3 false positives" (`contract.json` C2 statement). Two of the three are resolution fixes. The
  third becomes a false positive only because the rule was re-scored. Kaidoku r29 (fleet
  `scripts/hyaku/lane-addendum.md:238-240`): "Re-scoring a rule the lane already holds on new inputs … is quality
  work, never coverage or depth". So the `explicit_out` exemption is quality work. Only the resolution edges under
  it count as depth.
- **The re-score alone does not pass the predicate.** Control: v3 with `--out\b|mkdtemp` added to `FLAG_RE`, a pure
  file-global re-score (sha256 `8b89ecce…a326`).
  ```
  python3 .ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f \
    --tool-file /tmp/tameshi-r42w2-CriticDepth-ctl/rescore_flag.py --text-mode
  FAIL F01_attr_scratch scratch=0 want 1 · FAIL F03_attr_ambiguous unflagged=0 want 1 · FAIL F04_outflag explicit_out=0 want 1
  FAIL F06_outflag_mixed_callers unflagged=0 want 1 · FAIL live 1682/1685 scratch=0 · FAIL live 123 explicit_out=0
  C2_R42_CONTROL: … selftest_exit=1 fixtures_pass=6/10 … live_unflagged_v4=0 … C2_R42_CONTROL_PASS=false
  ```
  F03 and F06 kill the file-global re-score, so the predicate does require the edges. The re-score still reaches
  **`live_unflagged_v4=0`**. So the "lane-wide unflagged 0" record (`SCORECARD.md:2006`,
  `corpus/README.md:536-537`, entry `:83-84`) is not depth evidence: a one-regex re-score yields the same number.

## F2 — Not load-bearing: no lane gate or skill section consumes any census version

- `git grep -n -E "write-path-census(-v[234])?\.py" a21845f -- ':!.ufo/waves' ':!LOG.md' ':!SCORECARD.md' ':!tools/write-path-census*'`
  finds only that round's own counter (`.ufo/evidence/round-{39..42}/census/measure.py`), contracts, the two
  knowledge entries (`r40-…:10`, `r41-…:31-33`, `r42-…:32`), the README coverage rows (`corpus/README.md:520,536`)
  and lessons.
- `git grep -n -i "golden\|update-flag\|r8-golden\|r41-variable\|r42-attribute\|census-v" a21845f -- SKILL.md` →
  empty. SKILL.md (2136 lines) was last edited in round 31 (`git log -- SKILL.md` → `2da841b`). The skill the lane
  ships does not mention the F4 write-path rule or any census tool.
- Fleet `MANIFEST.json:21126` lists v3 under `capabilities_added`. Nothing consumes v4's `explicit_out` field. Its
  only downstream number, lane-wide unflagged 0, can be reached without v4 (F1).
- Impact: this is a tradeoff for the judge, not a defect to fix this round. "Capability acquisition" here means an
  instrument the lane can run. No decision surface uses it.

## F3 — v4 hides real expected-value writes that v3 flags; three probes contradict properties the entry states

Each probe is a small file with one expected-value write into `tests/fixtures`, run as
`python3 -I tools/write-path-census-v4.py --file P --json`. v3 reports `unflagged=1` on every probe.

| probe | shape | v4 | contradicts |
|---|---|---|---|
| P1 | `def pick(self, live): if live: return "tests/fixtures"` then top-level `return self.base` (mkdtemp) | `scr=1 unfl=0` | entry `:39` / v4 `:22` "exactly one top-level return" is the gate, but a nested return escapes it (`v4:138` scans `method.body` only). Selftest `method_two_returns` (`v4:510-524`) passes only because of statement order. Same witness as MutantAuthor W3. |
| P2 | `__init__`: `self.base = tempfile.mkdtemp()`; `reset`: `self.base, self.count = "tests/fixtures", 0` | `scr=1 unfl=0` | entry `:37` / v4 `:20` "two or more distinct expressions … never read as scratch". Tuple targets are skipped (`v4:128` accepts only a bare `ast.Attribute` target). |
| P7 | second binding `with open("cfg") as self.base:` | `scr=1 unfl=0` | same claim as P2: `with`-targets are not collected. |
| P5 | `emit("{}", ns.out)`; `sink = emit`; `sink("{}", "tests/fixtures")` | `out=1 unfl=0` | entry `:45-46` "A single call with any other argument (a constant …) keeps the site unflagged". An aliased call is invisible, yet the site is resolved rather than left unresolved. |
| P3 | `add_argument("--out", default="tests/fixtures")` | `out=1 unfl=0` | entry `:18` "whatever the operator passed". With the default, the operator names nothing (also CriticSourced). |
| P4 / P6 | `ns.out = "tests/fixtures"` after `parse_args`; external `r.base = …` | hidden | in the declared non-claims (entry `:70-73`, "attribute reassignment outside `self`"). |
| P8 | `--source` with `dest="out"` on a second parser | `out=1 unfl=0` | contrived: dests are keyed module-wide (`v4:99`), not per parser. |
| P9 (control) | renamed true scratch: `spool` / `slot` / `put` | `scr=1 unfl=0` | correct. |

Probe sha256s: P1 `ccfff1cb…1b96`, P2 `35743656…3845`, P3 `79decba9…0a27`, P4 `800f9f18…c6`,
P5 `1a95b9a5…b1d7b5`, P6 `059173ff…ee1d85`, P7 `fd45632d…e0fe`, P8 `c7b97276…54729`, P9 `427c3721…a87e`.
None of these shapes is live in the lane. Lane flips v3→v4 over every tracked `tools/*.py` at `a21845f` are
exactly `context-capture.py:1682`, `:1685` and `registry-replay.py:123`, with no new unflagged site (my script;
this matches ExecV3V4Parity). `registry-replay.py:259` declares a bare `--out` with no default, and `p.error` at `:275`/`:286`
stops the run without it, so the live `explicit_out` is correct.

## F4 — Admission needs evidence outside the predicate. Wave 2 supplies the anti-cheat half, but the depth record fails it

To admit a gameable battery (`w1/CriticFixtureOverfit.md` Finding 1: a literal-table `v3flip` and a byte-memo
`contentcheat` both pass 10/10 + live 3/3), the judge needs four kinds of evidence. Status of each:

1. **Structure, not names.** `python3 /tmp/tameshi-r42-CriticFixtureOverfit-r1/renamed_falsify.py tools/write-path-census-v4.py`
   gives `SUMMARY 6/6`, against v3flip 4/6 and contentcheat 0/6. `w2/LabRenamedBattery.md` reports 10/10
   renamed, with v3flip at 8/10. **Provided.**
2. **No line-number lock.** With 7 blank lines prepended, the sites move to 1689/1692/130 with the same classification
   (my run; `w2/ExecLiveShift.md` SURVIVES). The `rg` scan of the v4 source finds `case_dir`, `publish` and `root`
   only in the docstring and selftest sources. **Provided.**
3. **Mutants killed by an independent author.** `w2/MutantAuthor.md:38-44`: 4 of 6 killed, with
   `outflag_no_parse_args_check` and `method_fold_several_returns` surviving, so a scratch-clone run gives
   `mutants_killed=4` and the predicate fails (`measure.py:455` requires killed == declared). CriticSourced: 4/4 S157
   ablations survive the oracle. **Fails as built.**
4. **No new false negatives, or the false negatives disclosed.** F3 above (P1, P2, P5, P7 contradict properties the
   entry states) and MutantAuthor W3. **Fails.** The entry states guards that the code does not enforce.

The v4 selftest is written by the tool's author (the L1, contract P4), so it is not independent evidence.

## Smallest safe correction

- Label the outflag `explicit_out` exemption as a rule re-score in the round-42 record, and cite it against
  `r8-golden-update-flag.md:14` and `r41-…:57-61`. Count only the attr/method edges and the call-site trace as depth.
  Drop "lane-wide unflagged 0" as depth evidence.
- For the next round, not after this freeze: count `Return`s over `ast.walk(method)` while skipping nested defs.
  Treat any Store-context `self.<attr>` outside a simple `Assign`/`AnnAssign` as an extra distinct value. Leave a
  parameter unresolved when its function name appears in a non-call Load context. Refuse `explicit_out` when the
  option has a non-`None` default or `set_defaults`. Each fix gets a probe from F3 as its fixture.
- Until then, record P1, P2, P5 and P7 in the lesson's C2 limits list as contradictions of entry lines `:37`, `:39`
  and `:45-46`, not as scope.

## Verdict

BROKEN: C2 holds as depth only for the attr and method edges and the call-site trace; it is not load-bearing.
The `explicit_out` exemption at v4:385 re-scores the held F4 rule, and "lane-wide unflagged 0" is reachable by a
one-regex re-score. Evidence outside the predicate clears the cheat question (renamed battery and line shift) but
not admission: 2 of 6 independent mutants survive, and v4 hides P1, P2, P5 and P7, which contradict the knowledge
entry's stated guards.
