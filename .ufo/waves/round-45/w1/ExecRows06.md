seat: ExecRows06

# Round-45 w1 — C1 row re-verification (S049, S052, S054)

Author seat for these three ledger entries. All rows fetched live on 2026-10-25 from their exact row URLs; verdict `holds` for all three; all three fragments pass `--check --rev 3310e7be803516ca5934b4e949d91bcec824b179` with `verified ok`. Raw snapshots retained at `/tmp/tameshi-r45-ExecRows06/S{049,052,054}.raw` for L1 integration (L1 compresses to the referenced `.gz` snapshot paths).

No tool installs/updates needed (system curl, python3, git show — no pacman/uv/npx/cargo actions).

## S049 — https://docs.python.org/3/library/subprocess.html

- curl: exit 0 (single attempt, Mozilla/5.0 UA), 208624 bytes, sha256 `587938d256dede9dc64c5f543ab3f19c74e42abd5de648056697701f199adf71`
- CHECK: `CHECK S049 verified ok`
- note: The Popen env note says the env parameter modifies the child's environment rather than doing it in preexec_fn, grounding the teaches claim that explicit env mappings define child environment rather than merely documenting an intended injection.
- First attempt, quote from the run() env paragraph ("If env is not None , it must be a mapping that defines the environment variables for the new process"), returned `CHECK S049 invalid overlap 1` — the counter computes overlap only against scope+anchor+teaches (not source), where that sentence shares only `environment`. Replaced with the Popen-note quote below (shares environment/child/rather), verified verbatim in `--extract` output and passing.

```json
{"id":"S049","url":"https://docs.python.org/3/library/subprocess.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"587938d256dede9dc64c5f543ab3f19c74e42abd5de648056697701f199adf71","quote":"If you need to modify the environment for the child use the env parameter rather than doing it in a preexec_fn","snapshot":".ufo/evidence/round-45/freshness/sources/S049.raw.gz","author":"ExecRows06","note":"The Popen env note states the env parameter modifies the child's environment rather than doing it in preexec_fn, grounding the teaches claim that explicit env mappings define child environment rather than merely documenting an intended injection."}
```

## S052 — https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/

- curl: exit 0 (single attempt, Mozilla/5.0 UA), 47923 bytes, sha256 `b19e6ca97778551a09fcc772e50c33f711c374817e34248fef1fdf42cb754c8c`
- CHECK: `CHECK S052 verified ok`
- note: The Support table names the mutator families and shows StrykerJS supports Array Declaration while not supporting Assignment Expression (❌), grounding the teaches claim about the JS single-edit operator families and the unsupported assignment expression.

```json
{"id":"S052","url":"https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/","opened":"2026-10-25","verdict":"holds","raw_sha256":"b19e6ca97778551a09fcc772e50c33f711c374817e34248fef1fdf42cb754c8c","quote":"Mutator StrykerJS Stryker.NET Stryker4s Arithmetic Operator ✅ ✅ ❌ Array Declaration ✅ ✅ ❌ Assignment Expression ❌ ✅ n/a","snapshot":".ufo/evidence/round-45/freshness/sources/S052.raw.gz","author":"ExecRows06","note":"The Support table row names the mutator families and shows StrykerJS supports Array Declaration while not supporting Assignment Expression (❌), grounding the teaches claim about JS single-edit operator families and the unsupported assignment expression."}
```

## S054 — https://diataxis.fr/compass/

- curl: exit 0 (single attempt, Mozilla/5.0 UA), 20288 bytes, sha256 `8597a5b13f235ddff56b24b234745fd46ba9a115af2b165b1f4e59b82514e1a0`
- CHECK: `CHECK S054 verified ok`
- note: The compass section says only two questions need asking (action or cognition, acquisition or application) to yield the classification, grounding the teaches claim that a section is classified by asking whether it informs action or cognition.

```json
{"id":"S054","url":"https://diataxis.fr/compass/","opened":"2026-10-25","verdict":"holds","raw_sha256":"8597a5b13f235ddff56b24b234745fd46ba9a115af2b165b1f4e59b82514e1a0","quote":"just two questions need to be asked: action or cognition? acquisition or application? And it yields the answer.","snapshot":".ufo/evidence/round-45/freshness/sources/S054.raw.gz","author":"ExecRows06","note":"The compass section says only two questions need asking (action or cognition, acquisition or application) to yield the classification, grounding the teaches claim that a section is classified by asking whether it informs action or cognition."}
```

## Summary

- 3/3 rows fetched live (curl exit 0), verdict `holds`, all fragments pass `--check --rev 3310e7be803516ca5934b4e949d91bcec824b179 --snapdir /tmp/tameshi-r45-ExecRows06` printing `verified ok`.
- Commands used (one per row):
  - `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows06/S###.raw '<url>'`
  - `python3 .ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecRows06/S###.raw` (wrote `/tmp/tameshi-r45-ExecRows06/S###.txt`)
  - `python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecRows06/S###.json --snapdir /tmp/tameshi-r45-ExecRows06`
- Fragments also written at `/tmp/tameshi-r45-ExecRows06/S{049,052,054}.json`.
- Blocker: none. S052/S054 passed on first quote; S049 needed one quote correction after `invalid overlap 1` (documented above; never faked).
