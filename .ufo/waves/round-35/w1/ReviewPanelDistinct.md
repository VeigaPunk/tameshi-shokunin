# ReviewPanelDistinct — round-35 w1 seat report

Scope: re-derive the public C1 panel's slots, distinct bodies, and per-specimen
kill/accept labels WITHOUT running the tool (`tally-audit-v3.py`), by applying
each edit, hashing the resulting text, and running the blocks under the four
(auto,KEEP) configs over the counter's vector set. Verdicts are behavioral.

## Verdict

No CRITICAL, BOUND, or HYGIENE finding: the public panel is exactly as claimed.
- slots: 3 kill + 3 accept (6 specimens, one per JSON)
- `pub_distinct` = 6 (six pairwise-distinct full runner texts, sha256 below)
- every kill label is justified by real behavioral divergence under at least one
  config; every accept label is justified by behavioral identity on all four
  configs over the full vector set
- the divergences are precisely in the three classes the v3 fixes claim to
  close (whole-stdout line 2; (0,0)/(1,1) sweep; comment-blindness)

## Method and exact provenance

Lane clone (read-only, detached at the dispatch tip):

    env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
      /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      /fast/scratch/hyaku/tameshi-r35-seats/ReviewPanelDistinct/lane
    env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
      d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc
    # exit 0 for both; HEAD = d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc

Pin check (exit 0; all match contract.json):

    sha256sum tools/tally-audit-v3.py tools/tally-audit-v2.py tools/mutate-and-run.sh \
      .ufo/evidence/round-35/c1/c1-measure.py .ufo/evidence/round-35/c2/c2-measure.py
    da23d3a2…cfa9a16f  tally-audit-v3.py
    7b11ba25…b3598d10  tally-audit-v2.py
    a7d3f2dd…dd912eb9  mutate-and-run.sh
    78bb43eb…b7a947ef9  c1-measure.py
    67bb7118…b381018f9cc  c2-measure.py

Re-derivation: `/fast/scratch/hyaku/tameshi-r35-seats/ReviewPanelDistinct/panel_rederive.py`
(independent implementation — own code_view / function-span / block cut / vector set /
bash driver; no import of the counter or tool). Run: `python3 panel_rederive.py`,
exit 0. It loads the 6 panel JSONs, asserts each old-string occurs exactly once in
the pinned runner (c1-measure `apply_edits` semantics), hashes the edited full text,
cuts `(head, block)` per copy, and runs pristine + every copy under all four CONFIGS
over the 267-vector set (all 256 statuses at position 0 + fixed mixes) — 28 bash
runs, 7,476 individual tally executions, every run parsed fully (driver asserts
len(got)==len(vectors), exit 0).

Cross-check against the frozen counter's own oracle (`c1-measure.behavior`/
`diverge`, imported as a module — still not the tool): identical divergence sets
for all six copies (exit 0).

## Per-specimen results

| specimen | label | sha256 of edited full runner text | diverging configs (counter oracle) | witness tuple (pristine → mutated) |
|---|---|---|---|---|
| cfg00-accept-swap | kill | `3b5061b130abc7e07b9a8fbb74e06e98fdf7fcc624316eea16f70a61cd3e189a` | (0,0) | vector `1,0×8`, cfg (0,0): `rc=1 FAIL(cases=9 passed=8 failed=1 setup=0)` → `rc=2 SETUP(case-tally mismatch: cases=9 counted=8)` |
| cfg11-pass-mask | kill | `b3aaefcdd7a5a7b119982b261500523e7e617e7a7d6a090ce361d6a4d3a495d9` | (1,1) | vector `0×9`, cfg (1,1): `rc=0 PASS(passed=9)` → `rc=2 SETUP(case-tally mismatch: cases=9 counted=0)` |
| workdir-branch-swap | kill | `2df05fc3a26ef08ac9dd5914d37020336a53b886c909334b097a7aff5edcdf5e` | (1,0), (0,0) | vector `0×9`, cfg (1,0): `rc=0 PASS … WORKDIR: /tmp/tally-audit-work (removed on PASS; --keep retains)` → `rc=0 PASS … WORKDIR: … (kept)` — **only stdout line 2 differs** |
| comment-brace | accept | `b9eb589a3ee01e2f4285f721e2833ed0c5ccbf269e10e8c788da934e93068e2e` | — | identical (rc+full stdout) on all 4 configs × 267 vectors |
| comment-esac | accept | `5be9b417fcaef014fe53cf57722d2f5dd26afb0637415a4b51704fa59f1b160e` | — | identical on all 4 configs × 267 vectors |
| comment-names-leg | accept | `8c654bc71aa5f4877ddec3a52ee458a2af6668aaaacca5f6cc0e812901813b57` | — | identical on all 4 configs × 267 vectors |

Kill/accept label check on behavior: kill 3/3 diverge, accept 3/3 identical.
`pub_distinct` = 6 unique full-text hashes (contract after_target expects 6).

## What I could NOT break (proof)

1. **Whole-stdout comparison is load-bearing.** `workdir-branch-swap` diverges
   from pristine only in the second `REGRESSION_WORKDIR` line (removed ↔ kept),
   with identical exit code 0 and identical first line, under (1,0) and (0,0).
   A first-line-only comparison would pass it; only the full-stdout tuple sees
   it. Proof: witness table above.
2. **The (0,0)/(1,1) config sweep is load-bearing.** `cfg00-accept-swap` and
   `cfg11-pass-mask` are inert under (0,1) and (1,0) and diverge only under
   (0,0) resp. (1,1) — the two triples the v2 control never swept
   (round-34 hold: Mutkillvectorarmswap F3). Proof: divergence sets above.
3. **All three accept specimens are behaviorally pristine on every input, not
   just the sampled vectors.** Each edit inserts bytes inside a shell comment
   (POSIX §2.3: a `#` at token start discards to end-of-line before
   tokenization), and none alters quotes/heredocs/line structure; the token
   stream is identical, so behavior is identical for all vectors and configs.
   Structurally, `code_view` blanks exactly the inserted spans, so the v3
   scans see the same code view as pristine (same length, same offsets) — the
   round-34 false-kill class (comment naming a leg, comment `}`, comment
   `esac`) cannot re-trigger on these copies.
4. **Runner identity.** Edits apply exactly once each (count==1 asserted per
   spec; also `grep -cF` on the pinned runner: 1/1/1/1 for the four old
   strings); pristine runner sha256 = `a7d3f2dd…dd912eb9` (PIN_RUNNER); all
   copy hashes are the frozen panel's computed bodies.

## Verification gaps (explicitly out of instruction scope)

- Tool-side verdict alignment (kill ⇒ rc 1 with failing check `runtime` alone;
  accept ⇒ rc 0) is the counter's measurement, which this seat was instructed
  NOT to run ("WITHOUT running the tool"). All three kills are behaviorally
  divergent on the counter's oracle — the ground truth the labels encode — and
  the divergence lies in exactly the fixed classes, so no label is unjustified
  at the behavior level; the tool's rc/failed-checks agreement is covered by
  the sibling tool-review seats (ReviewToolDelta, ReviewSealedGate, …).
- The counter's 267-vector set is smaller than the tool's runtime sweep; for
  the accept copies this cannot matter (comment-only edits, argument 3 above).

## Notes

- No tool installs/updates were performed (nothing needed); no pacman use.
- Scratch: `/fast/scratch/hyaku/tameshi-r35-seats/ReviewPanelDistinct/`
  (lane read-only, untouched; no git mutations anywhere).
- The ad-hoc witness probe failed once on a local script tuple-unpacking bug
  (not a specimen artifact); fixed and re-run, exit 0, evidence above.
