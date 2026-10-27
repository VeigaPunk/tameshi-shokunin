# T52W2CritRekey

Axes: calibration (round-21 monitor credit and C2 m6 integrity); evidence/provenance integrity.

## Counterexample

A re-key entry with honest, nonempty findings cannot be credited by the round-21 monitor. The refresh assigns `wrong_expectations=len(findings)` (`.ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py:214-220`), while the unchanged round-18 entry gate rejects every positive `wrong_expectations` count (`.ufo/evidence/round-18/measure.py:459-474,477-494`). Round-21 selection runs that algorithm unchanged (`.ufo/evidence/round-21/coldread/measure.py:1-5,18-21`). Thus any honest finding list with length >0 makes the entry fail credit; an empty list is accepted by m6 unless otherwise malformed, but conveys no reported findings. This is not merely untested: W1's synthetic run produced a finding-bearing entry and observed 63/64 coverage (`.ufo/waves/round-52/w1/T52W1ExecRefresh.md:26-28,56-64`). Command: `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev REV --explain` (for a synthetic fixture, run after generated ledger is committed); the gate is visible via `python3 .ufo/evidence/round-18/measure.py --selftest` only for its suite, not this specific conflict.

**Fixable conflict, not a judge verdict:** C2 m6 requires the ledger's `wrong_expectations == len(findings)` and authentic quote strings, but does not require findings to be nonempty nor tie them to independently committed reader output (`.ufo/evidence/round-52/c2/measure.py:29-31,82-95,166-176`). W1 refresh deliberately makes monitor credit impossible when honest findings are nonempty. L1 must not resolve this by hiding or zeroing findings: that would undermine the m6 purpose. Smallest safe correction is change the frozen contract/monitor-credit acceptance design before applying re-key (e.g. distinguish reader findings from monitor wrong_expectations and have a counter enforce the former); if the frozen C2 rule is immutable, candidly report the incompatible acceptance constraints and do not claim credit-after-rekey. Do not change the C2 predicate after a seat runs.

## Selective omission / provenance

`refresh.py` accepts a caller-supplied `READERS_JSON`; it validates schema, that each quote appears somewhere in any listed markdown file, and a nonempty class (`.ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py:112-141,148-150,194-197`). It does not parse reader files as authoritative records, compare submitted findings with a reader's recorded JSON block, require a seat-to-file mapping, or verify reader files are committed before refresh. Therefore L1 can omit a real finding from submitted JSON, or list an unrelated markdown file containing a quote; C2 m6 only validates the final ledger against those same selected files and finds the same subset. A finding dropped from the ledger is invisible to m6. Seats are arbitrary nonempty strings and files arbitrary lane-relative markdown paths.

Smallest binding: each reader emits a canonical machine-readable record keyed to exactly one seat and target heading, including findings and read-section hash; reader records are committed at a fixed pre-refresh revision. Refresh should accept only that committed revision, enumerate the required seats/targets from the wave assignment, load each seat's designated record from that revision, and copy findings mechanically (no L1-authored replacement or filtering). C2 should independently check the required reader roster/record set and compare ledger findings/counts against those records, not merely quote substrings. Preserve exact reader bytes and commit IDs in receipts. This makes omissions detectable; quote occurrence alone does not.

## Read identity and refusal delta

The script does bind the *generated ledger entry* to the exact CAND section bytes: `sections_at` derives `sec['sha256']` and refresh writes it as both `skill_sha256` and `sha256`, with start/end/heading (`refresh.py:73-87,214-220`). Its trace command reads section lines from the detached candidate clone at `cand` (`refresh.py:28-33,198-206`), and receipts include hash/bounds (`refresh.py:222-224`). But it does **not bind the reader's actual read** to that hash/revision: reader JSON has no required read_rev or section hash, and validation checks only that submitted quote strings occur in listed files. So it can claim a re-key for a section version the named readers never read. The `read_rev` written to the entry is the candidate, not independently verified reader provenance.

Diff command: `diff -u .ufo/evidence/round-51/coldread/refresh.py .ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py` (run from lane root). The central refusal for target headings absent at CAND is retained (`round-51:185-186`; round-52:176-178). The explicit check that each target was credited at BASE is removed (`round-51:182-184`); targets are now constructed only from `base_rows` whose `base_credit[h]` is true (`round-52:170-175`), so this particular refusal is redundant rather than a weakening. No evidence of a weakened target-credit refusal from the inspected logic. One meaningful provenance restriction is also absent: round-51 only accepted a seat list, whereas round-52's `validate_readers` adds quote/file checks but not committed-reader provenance. This is an added validation surface, not a stronger binding. The scripts both retain detached-clone top-level check, strict-monitor requirement, target nonempty, clean trace checks, and ledger-at-CAND comparison (`round-51:154-181,188-223`; round-52:151-179,198-213).

Commands evidencing locations:
- `nl -ba .ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py | ...` (112-141, 170-224)
- `nl -ba .ufo/evidence/round-51/coldread/refresh.py | ...` (172-186)
- `nl -ba .ufo/evidence/round-18/measure.py | ...` (459-510, 623-653)
- `nl -ba .ufo/evidence/round-52/c2/measure.py | ...` (29-31, 82-95, 166-176)
- `diff -u .ufo/evidence/round-51/coldread/refresh.py .ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py`

## Summary
- Honest nonempty findings force positive `wrong_expectations`, which the monitor rejects; W1 observed 63/64.
- L1 controls the submitted findings; quote-in-file validation does not detect omission or bind seat to file.
- Ledger section SHA is computed from CAND, but reader section SHA/read revision is not verified.
- Restore provenance by consuming committed, seat-bound reader records mechanically and checking them independently; resolve the m6/monitor rule conflict without hiding findings.
- No install/update performed.
