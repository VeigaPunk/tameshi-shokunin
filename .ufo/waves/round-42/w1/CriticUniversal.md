# CriticUniversal — round 42 wave 1

Author: L1Tameshi42.CriticUniversal — 2026-10-25
Scope: scan contract.json claim statements/targets for universal words (all / every / no / complete); for each, check whether the counter enumerates the full set.

## Findings

### 1. C1 m7 — universal "round-41 **and** round-42 records cite no unmined S-id" is only half-enumerated (UNBOUNDED)

- Contract statement (contract.json C1.statement): "…the round-41 and round-42 records cite no unmined S-id…".
- Counter enumerates only **round-42** records for m7: `.ufo/evidence/round-42/calibration/measure.py:236-243` — `for _name, text in rec42:` is the only use of `S_CITE_RE` (grep: line 237 is the sole call site). `rec41` is built (`measure.py:234`) and used for m8/m11, but never fed to the m7 loop.
- The counter's own docstring confirms the asymmetry: `measure.py:32-36` "round-42 records (lesson, `## Round 42` SCORECARD section, `## 2026-10-25 — round 42` LOG section) for m7/m8/m11" — m7 is intentionally round-42-only, while m8/m11 run over both rounds (`measure.py:244,249`).
- Observable consequence: a round-41 record citing an unmined S-id would still yield m7=0. Concrete round-41 citation that is never audited: `corpus/lessons/round-41.md:13-14` cites S153/S154 ("Admit — `corpus/knowledge/r41-variable-destination-writes.md` (S153, S154)"). Today those ids are mined (SOURCES.md:123-124 status `mined`, `git show 322b5cd:corpus/SOURCES.md | grep 'S153|S154'`), so no live violation — but the statement's universal is not verified for the round-41 half.
- Smallest safe correction: either extend the m7 loop to `rec41 + rec42` (matching m8/m11), or narrow the statement to "the round-42 records cite no unmined S-id".

### 2. C1 m8 — universal "no unresolvable repo path" is narrower in the counter than in the statement (minor gap)

- `measure.py:162-172` (`path_tokens`) extracts only **backticked** tokens (BACKTICK_RE, `measure.py:79`), keeps only tokens starting with the whitelisted prefixes `corpus/ tools/ .ufo/ considerthese/ plans/ reports/` or exact root files (`measure.py:81-85`), and skips tokens containing any of `<>*{}|()…, $`. A path cited in plain text (no backticks) or under an unlisted prefix is not resolved.
- The statement says "no unresolvable repo path (line-scoped extraction)" — the counter's scope is prefix- and backtick-scoped, so the universal is satisfied only modulo both filters. The contract class m8 (contract.json C1.classes.m8) lists the same prefixes, so this is a statement-vs-counter wording gap, not a live miss: no current record path outside the filters was found.

### 3. C1 m10 — universal "no committed wave receipt asserts a report presence the tree contradicts" is enumerated only over tracked JSON

- `measure.py:190-201` (`receipt_audit`) scans `repo.tracked('.ufo/waves')` and keeps only `*.json`; non-JSON files and malformed JSON are silently skipped (the `except Exception: continue` at `measure.py:195-196`).
- Check of the current tree at freeze `322b5cd`: `git grep -nE 'present[": ]+(true|false)' 322b5cd -- .ufo/waves/ | grep -vE '\.json:'` returns only tool-output prose (e.g. `coldread.ledger_present: false` in round-16 w2 .md files), no `md` wave receipt asserting report presence. So today the JSON-only scan covers all existing presence assertions; the universal is complete in practice but structurally JSON-only (an .md receipt asserting `present` would escape).

### 4. C2 — all enumerated universals are bounded (no finding)

- "live_unflagged_v4=0 over every tracked tools/*.py": `census/measure.py:325-326` stages **all** tracked `.py` under `tools/` at REV via `git ls-tree -r --name-only REV -- tools/` (25 files at freeze), and `lane_unflagged` (336-344) runs the tool over each; per-file tool failures land in `v4_errors` and `v4_errors==0` is required (`measure.py:464`). Full set enumerated.
- "every counter fixture keeps its declared classification": FIXTURES is a literal 10-case table (`measure.py:72-202`), battery runs exactly those 10 (`287-297`), `fixtures_pass=10/10` required.
- "every declared mutant … is killed": mutants.json at REV is enumerated (`431-455`); each mutant must apply exactly once (`find.count == 1`, line 441), non-applying mutants count `invalid` (not killed), and `killed == declared` plus class coverage `{attr,method,outflag}` are required (`455`).
- "the three live v3 false positives": LIVE tuple (204-211) pins the exact 3 sites; `len(live_ok) == len(LIVE)` required (464).

## Could not check

- The v4 tool bytes are absent at base/freeze (`before_expected` tool_absent=1), so the tool_interface universal "for every write site, lineno/kind/…/resolved" could not be exercised against the 25 live tools files; that belongs to the deciding run.
- No deciding measurement was run (forbidden); all rev-pinned reads above used `--rev 322b5cd32b4319a05340d249ae752d12a9e6b19f` / base `c77c2b7e64d2e356381441ecf94abac03e984606` via `git show`/`git grep`.
