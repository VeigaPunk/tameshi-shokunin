# RR4-2 — cold re-read: `## Pin disposition and provenance correction — round 13`

Seat RR4-2, wave 3 residual re-read. Target: SKILL.md lines 1517-1547 at
`0ff273448ac4e62893c9b28a4cea7c580712df19` (heading `## Pin disposition and provenance
correction — round 13`, sectionizer sha256
`eb9c487be851b8886298fa2340a61af0c970d6ce75cbabd0e7eea741875e3e83` — recomputed per the
assemble sectionizer rule over lines 1517-1547 with trailing blank stripped; matches the
assignment). Page blob sha256 at the read rev:
`de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc` (verified on
`git show 0ff27344…:SKILL.md`; 1903 lines).

## Setup

Fleet-mirror clone at `/tmp/tameshi-r17w3-RR4-KDxO61` (siblings symlinked, lane cloned and
detached at the read rev). All commands below ran through
`.ufo/evidence/round-17/coldread/trace-inputs.py --root $C … --cwd $C` with receipts under
`.ufo/evidence/round-17/coldread/traces/RR4/`. Every receipt carries
`rev=0ff273448ac4e62893c9b28a4cea7c580712df19`, `live_lane_reads={}`.

## Commands executed (all traced; exits are the traced command's, from the receipts)

| # | Receipt | Command (cwd = clone lane root) | Exit | Key output |
|---|---------|--------------------------------|------|------------|
| 1 | traces/RR4/1.json | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /tmp/tameshi-r17w3-RR4-KDxO61/fleet` | 0 | 6 legs, all `unavailable` reason `repo_symlink`; every row `result_reuse=not_established`; `not_compared` 8 items; `live_lane_reads` empty |
| 2 | traces/RR4/2.json | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 | `WITNESS_METADATA: metadata_consistent reason=ok` — matches companion `expected {id: metadata_consistent, exit: 0}` |
| 3 | traces/RR4/3.json | `python3 .ufo/evidence/round-13/producer-oracle.py --source .ufo/evidence/round-13/producer-before.py --runner tools/mutate-and-run.sh` | 1 | `WITNESS_SELFTEST: 40/41 pass`, `VERDICT: FAIL`; failing check = `summary preserves top-level exposed declaration kind` — matches committed `producer-oracle-repair.json` (`expected_exit: 1`) |
| 4 | traces/RR4/4.json | `python3 .ufo/evidence/round-13/producer-oracle.py --source tools/bash-witness-study.py --runner tools/mutate-and-run.sh` | 0 | `WITNESS_SELFTEST: 41/41 pass`, `VERDICT: PASS` — matches committed `expected_exit: 0` |
| 5 | traces/RR4/5.json | record check: sha256 of the four frozen round-12 files; `declaration.kind` of summary + rerun; companion scope/original_nested/frozen_bytes_rewritten; SOURCES row counts | 0 | digests `acc01268…`, `e8d2024a…`, `0def0d3b…`, `6726421f…` all equal the companion's pins; `summary declaration.kind = None`, `rerun declaration.kind = None`; covered=[summary.json], uncovered=[rerun… `named-residual-uncorrected`]; `original_nested None historical-null-preserved`; `frozen_bytes_rewritten: False`; S003/S041/S047 rows present (1 each) |
| 6 | traces/RR4/6.json | custody check: `git rev-parse HEAD`; committed round-13 receipts at the read rev; measured-revision fields of `pin-dispositions.json` + `verification-verdict.json` | 0 | all 16 receipts committed; `observed_at=2026-10-20T04:59:26Z root=/home/vgpnk/Projects/shokunin tool_sha256=29725397…` counts 6/3/3/0 with per-leg measured head commits (`1770305f`, `c2cab35b`, `9574a189`, `59cfbdc3`, `c2cab35b`, `1770305f`); verdict receipt all checks matched |
| 7 | traces/RR4/7.json | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` (literal page command) | 0 | fresh dated reading `observed_at=2026-10-20T18:30:13Z`: counts `{'legs': 6, 'unchanged': 3, 'changed': 3, 'unavailable': 0}`, all six `pinned.status=verified`, every row `result_reuse=not_established`; heads moved since the historical read on two legs (tsukuroi `9574a189→661020f0`, mado `59cfbdc3→c7693eb2`) with identical content statuses |

## Verification results per section item

- **Item 1 (read scope + not_compared before the result).** Read
  `corpus/knowledge/incremental-pin-disposition.md` (scope: content disposition of the six
  recorded legs only; §6 names the reader invariants incl. `not_compared` disclosure),
  the manifest note ("Environment, dependencies, fixtures and suite-command identity are
  unproven"), and the receipt's `not_compared` (mode/exec-bit, runner version and embedded
  defect specs, suite command and test harness, interpreter/toolchain, environment,
  dependencies, fixture/companion files, timeouts). Sources verified present:
  `corpus/SOURCES.md` rows S003, S041, S047.
- **Item 2 (pin-disposition run).** Executed both as the mandated clone-mirror run (receipt
  1) and as the literal command (receipt 7). Literal run reproduces the committed round-13
  receipt's counts exactly (3 unchanged / 3 changed / 0 unavailable) with all six pins
  `verified` and fresh branch-tip commits recorded — the page's "dated reading" caveat is
  demonstrated, not violated: two sibling heads advanced between 04:59Z and 18:30Z with
  content dispositions stable. `It executes no sibling gate` corroborated by receipt
  buckets: no sibling gate file in `inputs`/`external` of any pin-disposition receipt, and
  `live_lane_reads` empty. Receipt 1 (mirror run) also exercises table row 3: symlinked
  repos are reported `unavailable` with reason `repo_symlink` — never silently borrowed,
  exit still 0.
- **Item 3 (witness-metadata --check).** Exit 0, `metadata_consistent`; the companion's
  digest pins equal the bytes at the read rev (receipt 5).
- **Item 4 (record claims).** All true at the read rev: original summary and rerun summary
  each carry `declaration.kind = null`; the companion normalizes only the canonical summary
  (covered list = summary.json) and names the rerun null as outside scope
  (`uncovered_null_observations` → `named-residual-uncorrected`); original nested null kept
  as `historical-null-preserved`; `frozen_bytes_rewritten: false`. The producer's
  wrong-nesting bug is fixed in the current producer (`tools/bash-witness-study.py:787`
  reads top-level `declaration.get("kind")`) and its regression selftest asserts the exact
  top-level exposed kind (`:1542-1545`, literal
  `"declared-witness mapping (not a blind preregistration)"`) — exercised red-before via
  the oracle pair (receipts 3/4: FAIL→PASS on exactly that check), matching the committed
  `producer-oracle-repair.json`.
- **Item 5 (no sibling-gate rerun; closure from committed receipts).** No sibling gate was
  executed at any point. All 16 `.ufo/evidence/round-13/` receipts are committed at the
  read rev and carry their measured revision identity (`observed_at`, per-leg head commits,
  `tool_sha256`); `verification-verdict.json` records 15/15 checks matched and honestly
  excludes the initial `producer_before` path-layout failure as superseded by
  `producer-oracle-repair.json`.

## Observations (non-blocking)

- The committed `pin-dispositions.json` pins `tool_sha256=29725397…` ("pin-disposition.py
  r13"); the tool at the read rev is `331529ea…` ("r17"). The receipt retains the
  historical producer identity it ran under; the page does not claim otherwise.
- Companion `producer.path` sha `249d9dcd…` (historical round-12 producer) differs from the
  current `tools/bash-witness-study.py` (`49e9e5e2…`) — declared `checked_live: false`,
  consistent with item 4's "fixed separately for future summary generation".
- Manifest `derived_from` runner sha `75ed934d…` differs from the runner at the read rev
  (`fb6d86d6…`); the manifest is the configured round-13 baseline, not a live assertion,
  and no receipt treats it as reuse authority.
- No pacman installs were performed; no tools were installed or upgraded for this seat.

## Verdict

Section holds: every instruction executed at the read rev with the stated outcomes (two
pin-disposition readings, metadata_consistent, oracle red-before/green-after), every
checkable record claim verified true against committed bytes; minor gaps are
environment/tool-generation observations only.

```json
{"schema":"tameshi-coldread-report-v2","seat":"RR4-2","skill_sha256":"de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc","read_rev":"0ff273448ac4e62893c9b28a4cea7c580712df19","sections":[{"start":1517,"heading":"## Pin disposition and provenance correction — round 13","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["mirror-isolated run of item 2 (receipt 1) reports all six legs unavailable/repo_symlink because the clone fleet mirror presents siblings as symlinks; the literal --root run (receipt 7) reproduces the committed 3 unchanged / 3 changed counts — both outcomes are the page's own table semantics (dated reading; unavailable with reason)","committed pin-dispositions.json records the r13 tool (29725397…) while the read rev carries the r17 tool (331529ea…); companion producer sha 249d9dcd… and manifest runner sha 75ed934d… are declared historical identities differing from the read-rev bytes (49e9e5e2…, fb6d86d6…) — all consistent with the page's historical-identity declarations"],"commands_executed":["python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /tmp/tameshi-r17w3-RR4-KDxO61/fleet","python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json","python3 .ufo/evidence/round-13/producer-oracle.py --source .ufo/evidence/round-13/producer-before.py --runner tools/mutate-and-run.sh","python3 .ufo/evidence/round-13/producer-oracle.py --source tools/bash-witness-study.py --runner tools/mutate-and-run.sh","bash /tmp/tameshi-r17w3-RR4-KDxO61/check5.sh (sha256 + kind fields of frozen round-12 files, companion scope, SOURCES row counts)","bash /tmp/tameshi-r17w3-RR4-KDxO61/check6.sh (committed round-13 receipts and measured-revision fields at the read rev)","python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin"],"opened":[".ufo/evidence/round-13/pin-manifest.json",".ufo/evidence/round-13/witness-metadata.json",".ufo/evidence/round-13/pin-dispositions.json",".ufo/evidence/round-13/verification-verdict.json",".ufo/evidence/round-13/producer-oracle-repair.json",".ufo/evidence/round-13/producer-oracle.py",".ufo/evidence/round-13/producer-before.py",".ufo/evidence/round-12/BashWitness/summary.json",".ufo/evidence/round-12/BashWitness/declaration.json",".ufo/evidence/round-12/BashWitness/declared.tsv",".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json","corpus/knowledge/incremental-pin-disposition.md","corpus/SOURCES.md","tools/pin-disposition.py","tools/witness-metadata.py","tools/bash-witness-study.py","tools/mutate-and-run.sh"],"inputs":{".ufo/evidence/round-13/pin-manifest.json":"64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",".ufo/evidence/round-13/witness-metadata.json":"463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",".ufo/evidence/round-13/pin-dispositions.json":"210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",".ufo/evidence/round-13/verification-verdict.json":"1d128a44e0417eb29ca75195bc7f97b8d0ceae246f520710faf67c397ef35a4c",".ufo/evidence/round-13/producer-oracle-repair.json":"df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",".ufo/evidence/round-13/producer-oracle.py":"d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",".ufo/evidence/round-13/producer-before.py":"592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",".ufo/evidence/round-12/BashWitness/summary.json":"acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",".ufo/evidence/round-12/BashWitness/declaration.json":"e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",".ufo/evidence/round-12/BashWitness/declared.tsv":"0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json":"6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0","corpus/knowledge/incremental-pin-disposition.md":"8ac942f5a7e8369f90c6e1df2683bbcab7821b8be0ae2968aa933ad1e30ecf03","corpus/SOURCES.md":"ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5","tools/pin-disposition.py":"331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c","tools/witness-metadata.py":"df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4","tools/bash-witness-study.py":"49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80","tools/mutate-and-run.sh":"fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a"},"external_inputs":{"/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs":"5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0","/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh":"275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh":"d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e","/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh":"071d39d99aa94d9e3d0c0a8c9d9e9e98b4bc79b51af0703e4dba774f85f7c75d","/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh":"7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf","/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs":"e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b"},"traces":[".ufo/evidence/round-17/coldread/traces/RR4/1.json",".ufo/evidence/round-17/coldread/traces/RR4/2.json",".ufo/evidence/round-17/coldread/traces/RR4/3.json",".ufo/evidence/round-17/coldread/traces/RR4/4.json",".ufo/evidence/round-17/coldread/traces/RR4/5.json",".ufo/evidence/round-17/coldread/traces/RR4/6.json",".ufo/evidence/round-17/coldread/traces/RR4/7.json"]}]}
```
