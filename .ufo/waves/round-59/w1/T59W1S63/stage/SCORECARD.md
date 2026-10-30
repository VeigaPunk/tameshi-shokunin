
## Round 59 — declared source-pinning capability (pending measurement)

| Capability | Bounded behavior | Evidence / admission gate | First-working round |
|---|---|---|---|
| executor-source-pin (proposed; unmeasured) | Compare only declared executor-source Git blobs at a candidate commit with a verifier-supplied trusted commit. CLI: `python3 tools/executor-source-pin.py --repo REPO --trusted COMMIT --candidate COMMIT --path PATH [--path PATH ...]`. Exit 0: all declared regular source blobs equal; exit 1: candidate source drift, missing or nonregular; exit 2: bad arguments, invalid trusted commit/source or unresolvable candidate. | Frozen `.ufo/evidence/round-59/contract.json` and `measure.py`; target 24/24 committed-object fixtures (six classes × four path spellings), with skipped-work and always-accept controls failing. No execution or control result is supplied by this draft; acquisition remains pending L1 measurement. | Not established |

Trusted revision and complete source closure are verifier inputs. This is a binding prerequisite, not execution attestation, dependency/interpreter identity, closure-completeness proof, author-independent trust or round-58 C2 certification. No numeric score increase or historical claim admission follows.

**Still open:** R45.1, R45.4, R46.2, R47.5, R48.4, R49.3, R49.5; R51.6 (missing historical Gate reject list). This append closes none of these items and does not supersede other routed debts or historical records.
