# C01SchemaComplete — contract schema vs checker loader audit (round 20 attempt 2, wave 1)

Seat: reviewer (leaf, no sub-swarm). Date: 2026-10-21.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Read-only seat; only this file written.
No tool installs performed (system `python3` only). No Git/JJ mutation (read-only `git show`/`git log` only).

## Scope and method

- Schema authority audited: `load_contract()` in `.ufo/evidence/round-20/stage/receipt-window.py` (lines 61–120), the gate's contract loader, plus its consumers `check()`/`run()` (lines 132–232).
- Second contract consumer audited: `.ufo/evidence/round-20/stage/measure.py` (ruler; contract reads at lines 135, 158–160, 178, 223).
- Dynamic confirmation: 18 contract-variant probes run in a private `/tmp` sandbox (`/tmp/c01-probe.py`) against a copy of the staged gate bytes. Only the staged checker was executed; no lane file mutated.
- Byte identity: staged instruments and contract compared by sha256, worktree vs frozen commit.

Axes walked (godspeed): completeness of the loader-required-field enumeration; ignored-field detection; ambiguity detection; evidence rigor; zero lane mutation. All five improved together; none harmed.

## Loader-required fields (validated by the gate, `load_contract`)

| Field | Requirement enforced |
|---|---|
| (document) | must be a JSON object |
| `instruments` | required; must be a nonempty object; each key a nonempty string; each entry an object |
| `instruments.<name>.frozen_sha256` | required; lowercase 64-hex (`^[0-9a-f]{64}$`) |
| `instruments.<name>.installed_sha256` | required; lowercase 64-hex |
| `instruments.<name>.edit_interval` | required iff `frozen_sha256 != installed_sha256`: object with `start`/`end` aware ISO-8601, `start < end` (strict); optional but still validated (aware, ordered) when present on an identity instrument |
| (cross-entry) | one sha claimed by two instrument names → refused; historical key colliding with a current instrument sha → refused |
| `historical` | optional (default `{}`); if present: object, keys lowercase 64-hex, values nonempty (non-blank) string labels |
| `round` | read via `doc.get("round")` and echoed into the loader result, but **never consumed** by `check()`/`run()` (probe: `round: "twenty"` → CLEAN) |

The delivered contract satisfies every requirement; no required field is missing (both instruments are identity `frozen == installed`, so `edit_interval` is not required).

## Fields present in contract.json that the gate loader ignores

Top level: `attempt`, `baseline`, `frozen_at`, `claim`, `population`, `expectations`, `measurement`, `dispatch_artifact`, `sources`, `invariants` — all ignored by the gate (`only-loader-fields` probe: exit 0 CLEAN; `unknown-extra-keys` probe: exit 0 CLEAN).
Per-instrument: `staged_path`, `install_path`, `install_window`, `note` — ignored by the gate.

## Fields the ruler (`measure.py`) additionally reads

`frozen_at` (aware-ISO ordering vs contract commit time and `dispatch.wave1_dispatched_at`); `instruments["receipt-window"].frozen_sha256` and `instruments["round20-measure"].frozen_sha256` (vs staged bytes); `instruments["receipt-window"].installed_sha256` (vs installed bytes); `historical` keys+labels (vs hardcoded `EXPECT_HIST`). The ruler ignores `attempt`, `baseline`, `claim`, `population`, `expectations`, `measurement`, `dispatch_artifact` (it hardcodes the same path as its own `DISPATCH` constant), `sources`, `invariants`, and the per-instrument path/note fields.

## Findings, by severity

### MEDIUM — `install_window` vs `edit_interval`: the contract's declared window field is dead schema
Contract declares `instruments.receipt-window.install_window` (start/end); the loader's live field is `edit_interval`. Today frozen == installed, so no loader requirement triggers and `install_window` is silently unvalidated by anything (reversed or naive timestamps inside it would pass). Latent trap: a future revision with `installed_sha256 != frozen_sha256` declaring only `install_window` is refused by the gate — `instrument receipt-window differs frozen/installed and needs edit_interval` (probe 8). Conversely, had the field been named `edit_interval`, it would be validated even on identity instruments (probes 16–17: reversed/naive `edit_interval` → CONTRACT_INVALID). Two names for one concept, only one schema-live.

### LOW — `expectations` is not machine-read by either checker
`expectations {corrected:6, open:0, total:6, exit:0}` is advisory: the ruler hardcodes `TOTAL = 6` and `EXPECT_HIST` literals; the gate never reads it. An edited `expectations` block changes no verdict. Single-source-of-truth drift risk (contract text vs ruler literals).

### LOW — instrument names and paths are duplicated, not bound
The gate treats instrument names as free-form strings; the ruler hardcodes `"receipt-window"`/`"round20-measure"` and its own path constants (`CONTRACT`, `DISPATCH`, `STAGE_GATE`, `STAGE_MEASURE`, `INSTALLED`). The contract's `staged_path`/`install_path`/`measurement`/`dispatch_artifact` strings are never cross-checked against the ruler constants; a divergent edit would go undetected. (Values currently agree: contract `dispatch_artifact` `.ufo/waves/round-20/dispatch.json` == ruler `DISPATCH`; dispatch.json exists with `wave1_dispatched_at 2026-10-21T09:29:09.517Z`.)

### LOW — cross-entry collision diagnostic is masked by field-order validation
The loader validates each entry's `edit_interval` requirement before the sha-collision index check inside the same loop, so a duplicate-sha instrument that also lacks `edit_interval` reports the wrong root cause (probe 12: `instrument twin differs frozen/installed and needs edit_interval` — the collision error `sha … is claimed by both …` is unreachable in that ordering). Diagnostic-accuracy defect only; refusal still occurs (fail-closed).

### INFO — `round` is parsed but unused; untyped
Echoed in the loader result, consumed by no verdict path; wrong type accepted (probe 14). Either validate it (`round == 20`) or drop it from the loader echo.

### INFO — `historical` is optional, permitting a contract that can never classify history
A contract omitting `historical` loads CLEAN (probe 9: exit 1 only because the probe receipt cited a historical sha), yet any historical-sha receipt then fails `UNKNOWN_INSTRUMENT`. The schema permits a state that can never satisfy population item `historical_classified`; only the ruler's item 6 catches it.

### INFO — receipts schema is implicit; `instrument` name field optional
A receipt carries only `id`, `instrument_sha256`, `measurement_interval{start,end}`; `instrument` may be omitted and classification falls back to sha matching alone (probe 18: CLEAN). Contract.json documents none of this receipts schema; it lives only in gate code/selftest.

### INFO — `measurement` embeds a host-absolute path
`"python3 … --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin …"` is an advisory, unread, host-specific string; harmless for verdicts (ignored), but it is dead weight if the lane moves.

## Byte identity and ordering verification (commands + observed outputs)

```
sha256sum .ufo/evidence/round-20/stage/receipt-window.py .ufo/evidence/round-20/stage/measure.py .ufo/evidence/round-20/contract.json
→ f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc  stage/receipt-window.py
→ f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d  stage/measure.py
→ 9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715  contract.json

git show 6fd220bce3705498d1d1054e99e3cae73c203751:.ufo/evidence/round-20/contract.json | sha256sum
→ 9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715   (identical: staged bytes frozen)
git log -1 --format=%cI 6fd220b… -- .ufo/evidence/round-20/contract.json
→ 2026-10-21T04:41:02-03:00  (= 07:41:02Z)
```
Ordering: `frozen_at 07:40:18Z ≤ commit 07:41:02Z ≤ wave1_dispatched_at 09:29:09.517Z` — population item 1's declared chain holds on the observed values.

Probe summary (staged gate, /tmp sandbox, 18 variants): baseline CLEAN; loader-minimal contract CLEAN; missing/empty `instruments`, missing `frozen_sha256`/`installed_sha256`, uppercase sha, bad historical key, historical/current sha collision, reversed/naive `edit_interval`, and frozen≠installed without `edit_interval` all → exit 2 `CONTRACT_INVALID` with specific messages; wrong-type `round` and unknown extra keys → accepted.

## Agreement with frozen facts

- Staged instrument shas match the frozen facts exactly (`f03ae7e9…`, `f34dc233…`); historical shas in contract.json match all four frozen-fact instruments verbatim.
- `tools/receipt-window.py` is absent at the current worktree — consistent with the contract note ("install copies the same bytes after every wave reader returns"); not a defect. Ruler items 3/5 would currently report absence, which matches the pre-integration state and the 0/6 baseline receipts (`c1-before.json`: `contract.json absent at revision` at baseline `c144dcd8…`).
- Baseline `c144dcd807166dfc275c1ac2936fd2fa4b678bda` appears in contract and c1-before receipt; consistent.

## Defects recommended for L1 (all schema-documentation level; no behavioral failure observed in the delivered contract)

1. Rename or alias `install_window` → `edit_interval` in a future contract revision (or document that `install_window` is advisory prose, validated by nothing).
2. Either consume/validate `round` or remove it from the loader echo.
3. Ruler should derive `TOTAL`/`EXPECT_HIST` (or at least cross-check them) from `expectations`/`historical` instead of independent literals.
4. Reorder `load_contract` to check cross-entry sha collisions before per-entry `edit_interval` requirements for accurate diagnostics.
5. Document the receipts schema (`instrument` optional) in the contract or gate docstring.

## Residual risk and verification gaps

- I did not execute `measure.py` end-to-end (other seats own the 0/6 → 6/6 claim); my loader conclusions come from the gate code plus variant probes, which exercised `load_contract`/`check` directly.
- `edit_interval` positive-window behavior was confirmed via probes on copies; the delivered contract never exercises it (identity instruments).
- I did not verify the install step's future bytes (`tools/receipt-window.py` absent); the frozen==installed identity claim is verified for staged bytes only.
