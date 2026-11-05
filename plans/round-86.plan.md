# Round 86 — the discriminating certification, and the repertoire bound to bytes

Base: `d10a9c66d6181cddcad52cdbffd672beb886ff6c`. L1: TameshiR86. Attempt 1.

## Declaration

TWO claims, causally separable, each frozen before its data.

**R86-C1 (operability — capability acquisition).** Certify the design-receipt
audit capability with a NEW frozen counter that the QUALITY criterion-111
cheat family cannot pass. This does not amend round-85's counter or verdict
(`.ufo/evidence/round-85/measure.py`, R85-C1 honest-stop): the r85 counter and
its witness stay exactly as committed. Round-85's closure routed defect 1 is
the motivation, and this round pays it: the cheat family is executed and
committed BEFORE this freeze.

Frozen predicate: `C1_R86 rev=<rev> passed=8/8 C1_R86_PASS=true`, exit 0, from
`python3 -I .ufo/evidence/round-86/measure.py --repo LANE --rev REV --work EMPTY_DIR`.
Controls, each committed in `controls/` before this declaration and each
required to print `C1_R86_PASS=false`:

| control | class | measured at base |
|---|---|---|
| `ctl-fingerprint.py` | content-recognition cheat | passed=0/8 |
| `ctl-sequence.py` | invocation-sequence cheat | passed=4/8 |
| `ctl-pinned-hash.py` | pinned-hash cheat | passed=0/8 |
| `ctl-always-accept.py` | always-accept arm | passed=0/8 |
| `ctl-r85-forgery.py` | round-85's own witness, byte-exact (`0acb90ac…`) | passed=6/8 |

Counter contract: per-run nonce fixture paths, bytes and commit messages;
shuffled case order per run; expected rows DERIVED from the candidate tree and
candidate blobs the counter itself reads (never a hand-written token list);
comparison is the complete anchored stdout (`DESIGN_BLOB_ROW <path> state=…`
per receipt in sorted path order plus the exact `DESIGN_BLOB: receipts=N
carried=C orphan=O` summary) and the exact exit, with empty stdout on every
exit-2 case. Eight cases: carried, mixed (carried/different/absent/nonregular),
malformed sha, incomplete marker, mixed headers, zero population, absolute
root, unresolvable candidate.

Kill rule: any control printing `passed=8/8`, or the real instrument printing
`passed<8/8` at the measured revision, kills the claim; a miss is honest-stop.

**R86-C2 (calibration).** Bind every row of the lane's own capability
repertoire (`SCORECARD.md` `## Capabilities`) to repo state: a row is bound
only by a live `selfstate-freshness` row naming it, or by a receipt the row
itself cites that resolves at the named revision. A relabelled row (pin not
cited by its own text) is refused, not bound.

Frozen predicate: `CAP_CENSUS: rows=30 bound=30 unbound=0 mismatches=0`, exit 0,
from `python3 -I -X utf8 tools/capability-census.py --repo . --rev REV`.

| state | command | measured |
|---|---|---|
| before | same counter, manifest restricted to the 18 rows the standing freshness sweep already binds (`c2-before.txt`) | `rows=30 bound=18 unbound=12 mismatches=0`, exit 1 |
| after | full `tools/capability-census.json` (`c2-after.txt`) | `rows=30 bound=30 unbound=0 mismatches=0`, exit 0 |
| relabel control | every row declared historical, pinned to a receipt the row never cites (`c2-relabel-control.txt`) | `rows=30 bound=0 unbound=30`, exit 1 |

Kill rule: any unbound row, any manifest defect (duplicate entry, extra entry,
live row naming a missing selfstate id, historical pin not cited by its row or
unresolvable at its revision), or a relabel control that binds a row, kills
the claim.

**Sourced claim.** R86-C1's expected-row derivation reads the per-entry
`objectmode`/`objecttype` fields of a tree listing. Source **S305** (Git
git-ls-tree documentation) re-opened by L1 on 2026-11-04; located quotes at
snapshot lines 1808 (“The mode of the object.”) and 1812 (“The type of the object
(commit, blob or tree).”), snapshot
`.ufo/evidence/round-86/sources/s305-ls-tree.html`. The source supports
listing semantics only, not the audit verdict policy; no new row is appended
(the URL is held as S305; a second row would be a within-scope duplicate).

## coldread_forecast

Planned monitored edit: `corpus/SOURCES.md` only (S305 `used-by` old→new; the
round note). No `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md` or
knowledge-entry edit is planned this round.

Measured with `python3 -I tools/rekey-cost.py --edit corpus/SOURCES.md` at the
base revision: `REKEY_COST sections=71 planned=1 at_risk=13 predicted_lost=13`.
The rekey is owed and is run after the edit lands; the lane's actual floor
must read `lost=0` at the landing tip before admission is reported.

## No harm and limits

No existing tool is modified: the round adds `tools/capability-census.py`,
`tools/capability-census.json`, the round's evidence counter and controls.
Round-85's counter, witness and rejected verdict are unchanged. Standing
sweeps (selfstate, pins, registry, defect bind, receipt bind, pointer,
attribution, anchors, additivity, arms, counts, wave) must read clean at the
records commit. Existing debts stay open: malformed kind/source-id, caller
revision authority, conversion attributes, receipt race/parent aliases, the
two-edit text pin, and the r85 `GIT_*` inheritance limit on that frozen
counter. The r85 supplemental-labelling defect is routed, not claimed here.

## Wave

One validated v1 wave, 10 seats (executor 3 · scribe 1 · scout 1 · reviewer 1
· critic 1 · mutation-tester 1 · connector 1 · sentinel 1); L1 holds the
planner seat. Attack roles 4/10 = 40 %. Sole integration owner: L1. Seats use
private scratch under `/fast/scratch/hyaku/tameshi-r86/<seat>/` and deliver
findings and proposal files; they never commit, push or run a mutating
git/jj command. No report before WAVE-DONE.

Assimilation: none — checked against `merge/tameshi/MERGE-REPORT.md` and the
newest `considerthese/2026-10-28.md`; neither serves these two frozen claims.
