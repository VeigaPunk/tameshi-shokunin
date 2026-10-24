# CriticC2Scope — round-36 w1 — C2 claim framing attack

Attacked: the C2 claim framing — (a) whether `depth` is the right axis name for a
counter-predicate repair; (b) whether the frozen target 6/3/9 is re-derivable by a
stranger from one command over committed bytes; (c) whether the v2 deciding run at the
refresh commit measures the same tool bytes the capability row pins.

Scope: C2 framing only (C1 covered by CriticC1Scope). Read-only seat; no edits, no
counter runs consumed — the kill rule's one deciding run stands.

## Verdict: AGREE — the framing survives the strongest available counterexamples; no defect the canonical judge must reject. Two minor notations, neither fatal.

---

## Q1 — axis name: `depth (surface: the tally-audit counter's predicate completeness)` — DEFENSIBLE

The naming rule ("name the axis by the surface the round changes, not by the number it
produces") is applied correctly on its face: the changed surface is the counter's
predicate completeness (`c1-measure-v2.py:68-70, 538-544` — three frozen targets plus
three new conjunctions), and the claim produces no number on the depth rubric — the
SCORECARD itself discloses `depth 9 → 9` (`SCORECARD.md:1754-1756`, "C2's gain is
predicate completeness, not a ledger count"). No numeric depth move is claimed, so the
charge "named by the number it produces" fails.

Two attempted counterexamples, both rejected:

- **'calibration' would be a better name because self-assessment instrumentation
  improved.** Structurally impossible, not merely less apt: `AXES.md:32-33` requires
  distinct axes per round ("two claims on one axis in one round count as one claim"),
  and C1 already owns calibration. C2 could not name calibration without collapsing
  the round to one claim.
- **'operability' — the script now produces the stated outcome (refuses the vacuous
  pass).** Rejected on the surface rule: operability is the runnable-artifact axis
  ("a checklist item can be run and produces the stated outcome" — `AXES.md:13`), and
  the v1 counter already ran; what changed is *what it checks* — the decision content
  of the oracle — which is the depth axis's domain ("decision tables with real
  thresholds", `AXES.md:11`; the frozen constants `PUB_KILL_SLOTS_TARGET=6` etc. are
  literally thresholds). Lane precedent agrees: round-35's C1 named the same
  audit-surface family "depth (declared surface)" with operability as the secondary
  tag (`SCORECARD.md:1686`; contract r35 `claims[0].axis=depth`); the r35-r36 claims
  table in the mission prompt treats "audit-surface detail" as depth work. The
  residual defect that routed this work was filed as a *predicate-completeness* defect
  (`SCORECARD.md:1716-1720`, "counter defect for round 36", MAJOR).

Minor notation (not a defect): the axis tag rides a capability-successor claim on an
evidence instrument rather than on SKILL.md content. The lane's claim model permits
capability/fron-tier moves to carry per-axis verdicts (`AXES.md:40-41`), and the
SCORECARD records no capability-row addition and no score change, so the tag is a
label-by-surface, not a scored-axis assertion. A stranger reading AXES.md alone could
still contest the vocabulary; the lane's own cited convention is consistent.

## Q2 — frozen target 6/3/9 re-derivable — YES, empirically re-derived

One command class over committed bytes, no working-tree dependency:

- The counting command (`contract.json:35`:
  `python3 .ufo/evidence/round-36/c1/c1-measure-v2.py --lane LANE --rev REV --work
  EMPTY_DIR --sealed .ufo/evidence/round-35/c1/sealed`) reads the panel via
  `load_copies_rev` (`c1-measure-v2.py:296-311`), which uses `git ls-tree` + `git
  show` at REV — committed bytes only. Sealed set likewise at REV (`:487`). `--work`
  is scratch space and asserted empty at entry (`:434`).
- Independent re-derivation performed this seat at `b455001e`
  (the refresh/measured commit):
  `git ls-tree -r --name-only b455001e -- .ufo/evidence/round-35/c1/panel/` → 9 JSON
  copies; per-copy `copies[].set` field → **6 `kill` + 3 `accept`** (kill:
  cfg00-accept-swap, cfg11-pass-mask, root-keyed-auto-mask, root-keyed-auto-zero,
  root-keyed-shape6, workdir-branch-swap; accept: comment-brace, comment-esac,
  comment-names-leg). Matches `PUB_KILL_SLOTS_TARGET=6`, `PUB_ACCEPT_SLOTS_TARGET=3`
  exactly.
- `PUB_DISTINCT_TARGET=9` is body-level distinctness after `apply_edits`
  (`distinct_bodies`, `:409-414`) over committed panel + runner bytes; re-derived
  transitively by the frozen counter itself and corroborated by the independent r35
  deciding receipt at `34fa5b0` (`pub_distinct=9`) — same panel bytes, different
  measuring instrument.
- C2 predicate sentence in the contract (`contract.json:31`) matches the code
  conjunction (`:538-544`) — `pub_kill==6 && pub_accept==3 && pub_kill_slots==6 &&
  pub_accept_slots==3 && pub_distinct==9` conjoined with the inherited behavioral
  verdicts. Target == printed receipt fields == contract constants.

## Q3 — same tool bytes as the capability row pins — YES, byte-proven

- Capability row (`SCORECARD.md:1698`, tally-audit-v3 runner audit, round 35) pins
  `tools/tally-audit-v3.py @ 6188db16…` under counter `c1-measure.py @ d360a159…`.
- This seat's `git show` hashes: `tools/tally-audit-v3.py` at `b455001e` =
  `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354`; identical at
  tip `d9c496b`. `tools/mutate-and-run.sh` at `b455001e` =
  `a7d3f2dd…12eb9` (row's runner pin). Counter v2 at both `b455001e` and `d9c496b` =
  `9eb8944c…` = `contract.json:24 counter_sha256`.
- The deciding receipt (`after/c1v2-at-b455001e.stdout`) prints
  `tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1` — and `tool_sha_ok` is
  enforced inside the predicate (`:462, 538`), so the PASS is itself a byte-identity
  assertion, not an assumption.
- The v2 run therefore measures the identical tool bytes the row pins, under a
  strictly stronger predicate (the r35 PIN run's 16-copy verdicts plus slot
  cardinality and distinctness). The capability row's evidence pointer (frozen v1
  counter) is untouched — v2 is additive verification, not a moved pointer; the
  SCORECARD's "no new row" statement is accurate.

Minor notations (not defects):
- `mode=deciding` is printed whenever `--tool` is absent (`:450-455`), so the
  empty-panel control receipt (`control/v2-at-emptypanel.stdout`, at mutant rev
  `91373d55`) is labeled `deciding` despite being a control. The kill rule counts
  runs at the measurement commit — one, `rev=b455001e` — so the rule is honored;
  the label is cosmetically ambiguous to a naive receipt reader.
- The emptied-panel mutant commits (`91373d55`) carry `pub_slots=0` while passing v1 —
  the defect demonstration is genuine: v1 PASS=true on an empty panel, v2 PASS=false
  on identical bytes.

## Exact commands run (read-only; REV `b455001e` = refresh/measured commit, tip `d9c496b`)

```
git show b455001e:.ufo/evidence/round-36/c1/c1-measure-v2.py | sha256sum
  → 9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53 (== contract pin)
git show b455001e:tools/tally-audit-v3.py | sha256sum
  → 6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354 (== capability-row pin)
git show b455001e:tools/mutate-and-run.sh | sha256sum
  → a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 (== runner pin)
git show d9c496b:{c1-measure-v2.py, tools/tally-audit-v3.py} | sha256sum → same pins at tip
git ls-tree -r --name-only b455001e -- .ufo/evidence/round-35/c1/panel/
  + git show per file | json copies[].set tally → 6 kill / 3 accept / 9 files
```

Files read: `.ufo/evidence/round-36/contract.json`; `.ufo/evidence/round-36/c1/c1-measure-v2.py`
(full); `.ufo/evidence/round-36/after/c1v2-at-b455001e.stdout`;
`.ufo/evidence/round-36/control/{v1,v2}-at-emptypanel.stdout`;
`.ufo/evidence/round-35/after/c1-at-34fa5b0….stdout`; `.ufo/evidence/round-35/contract.json`;
`.ufo/evidence/round-35/closure/pins.stdout`; `.ufo/evidence/round-35/c1/sealed/manifest.json`;
`SCORECARD.md:1672-1776` (r35 Holds + r36 block); `/home/vgpnk/Projects/shokunin/AXES.md`.

Tooling: none installed.

**Verdict line: AGREE — C2's axis name is convention-consistent and structurally forced; the 6/3/9 target re-derives from committed bytes by `git ls-tree`+`git show` (verified by this seat); the deciding run at `b455001e` measures byte-identical tool/runner/counter pins; two cosmetic notations (deciding-label ambiguity on controls, un-scored axis tag) are not judge-rejectable defects.**
