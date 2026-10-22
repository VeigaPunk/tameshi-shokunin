# Draft — SKILL.md decision table: exporting a tameshi sweep as a mutation-testing-elements report

**Verdict: draft is ready; nothing was written to `SKILL.md`.** The table below is a
paste-ready SKILL.md section (title + decision table + three error patterns). It is derived
from measured behaviour of `tools/mte-interop.py` and the two vendored official packages,
not from prose.

Lane: `tameshi-shokunin`. Lane revision at drafting: `09dc114da9002525d31985c14093d32c6712bff4`
(`git rev-parse HEAD`, read-only). Pinned tool revision:
`tools/mte-interop.py` sha256 `24de859f18b9106c9e35d70cd35bcee92f7a3bef41eb22b732be23064f8f074f`.
Pinned runner: `tools/mutate-and-run.sh` sha256 `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`.

## Bounds honoured

- **Draft only.** `SKILL.md` is untouched; the drafted text lives in this report.
- Nothing written outside this file. No git/jj write command ran in the lane; no
  production file was edited.
- The selftest and the metrics probe ran **in `/tmp` copies only**
  (`/tmp/r25-draftskill/`, `/tmp/r25-metrics-probe/`), never in the lane checkout.

---

## 1. The measured facts the table rests on

### 1.1 The verdict vocabulary and its MTE mapping

`tools/mte-interop.py:69`

```
STATUS = {'KILLED': 'Killed', 'SURVIVED': 'Survived', 'INCONCLUSIVE': 'RuntimeError'}
```

The three tameshi verdicts are produced by the runner's exit map
(`tools/mutate-and-run.sh:537-542`): exit `0` → `SURVIVED`; exit `124` (timeout),
`126` (suite not executable), `127` (suite not found) → `INCONCLUSIVE`; any other exit →
`KILLED`. The emitter copies the verdict verbatim into the report's `statusReason`
(`tools/mte-interop.py:156-157`), so the MTE status is derived from the runner's own row,
never re-decided.

### 1.2 What the official library counts as valid / detected

Measured by running the vendored `mutation-testing-metrics` 3.9.0 (extracted from
`tools/vendor/mutation-testing-metrics-3.9.0.tgz`, member `package/dist/src/calculateMetrics.js`)
over one-mutant reports:

```
$ node /tmp/r25-metrics-probe/probe.mjs
Killed         valid=1 detected=1 invalid=0 mutants=1 score=100
Survived       valid=1 detected=0 invalid=0 mutants=1 score=0
RuntimeError   valid=0 detected=0 invalid=1 mutants=1 score=NaN
Timeout        valid=1 detected=1 invalid=0 mutants=1 score=100
NoCoverage     valid=1 detected=0 invalid=0 mutants=1 score=0
CompileError   valid=0 detected=0 invalid=1 mutants=1 score=NaN
```

The arithmetic behind those numbers is the library's own `toMetrics`
(`package/dist/src/calculateMetrics.js:169-191`):
`totalDetected = timeout + killed`; `totalUndetected = survived + noCoverage`;
`totalValid = totalUndetected + totalDetected`; `totalInvalid = runtimeErrors + compileErrors`;
`totalMutants = totalValid + totalInvalid + ignored + pending`;
`mutationScore = totalDetected / totalValid * 100`.

Three consequences the table depends on:

1. `Killed` and `Timeout` are both **detected**; `Survived` and `NoCoverage` are both
   **valid but undetected**; `RuntimeError` and `CompileError` are **invalid** — they leave
   the score denominator entirely.
2. `RuntimeError` mutants still appear in `totalMutants` (so `totalMutants == defects`
   holds even with inconclusive rows) and land in `totalInvalid` (so
   `totalInvalid == inconclusive` holds).
3. Because the mapping is `INCONCLUSIVE → RuntimeError`, the official denominator is
   exactly `killed + survived` — the same denominator tameshi's own kill rate uses
   (`tools/mte-interop.py:243-248` computes `killed / (killed + survived)`), and the
   official score equals tameshi's score to within 1e-9. The tool labels this check
   *"sanity only: with a 1:1 Killed/Survived mapping this equality holds by construction"*
   (`tools/mte-interop.py:246`).

### 1.3 The four independent checks a conforming leg must pass

`tools/mte-interop.py:237-262` — `judge()` returns the sorted list of failed check names:

| check | what it compares | independence |
|---|---|---|
| `schema` | the report against the vendored official JSON Schema (draft-07) | the schema, not tameshi's code |
| `score` | official `mutationScore` vs tameshi's `killed/(killed+survived)` | sanity only — holds by construction under the 1:1 mapping |
| `ledger` | official `killed`/`survived`/`totalInvalid`/`totalMutants` vs the runner's own `REGRESSION_TABLE` row for that leg, plus `flips == 0` | the runner's measured ledger line, not the emitter |
| `per_mutant` | every mutant's `status` vs the **committed** per-defect recorded verdict table (`TABLE_*` in the runner, leg→table map at `tools/mte-interop.py:74-78`) | committed bytes, not this run |

The `ledger` check's source row is `REGRESSION_TABLE <leg>: match=…/… recorded-killed=…
measured-killed=… survived=… inconclusive=… flips=…` (`tools/mutate-and-run.sh:1249-1250`,
parsed by `tools/mte-interop.py:71-72`).

---

## 2. Draft SKILL.md section (paste-ready)

```markdown
## Exporting a tameshi sweep as a mutation-testing-elements report (round 25, measured)

`tools/mte-interop.py` turns a tameshi sweep into one mutation-testing-elements
report per leg — schema `mutation-testing-report-schema` 3.9.0, scored by the
official `mutation-testing-metrics` 3.9.0 library, both vendored and
sha512-pinned in `tools/vendor/` (`tools/mte-interop.py:61-68`, re-verified
before every use at `:182-190`). The report is a *rendering of the runner's own
verdicts*, never a second opinion: the verdict cell of each
`<workdir>/<leg>/results.tsv` row (`tools/mutate-and-run.sh:531,546`) is copied
into `statusReason` and mapped once, by table, to the MTE status
(`tools/mte-interop.py:69,156-157`).

### The verdict → status decision table

| tameshi verdict | MTE status | counts in valid? | counts as detected? | source row |
|---|---|---|---|---|
| `KILLED` | `Killed` | yes — `totalValid` +1 | yes — `totalDetected` +1 (numerator) | measured row `results.tsv` for that defect id (`tools/mutate-and-run.sh:546`); expectation = the committed per-defect recorded row `TABLE_<LEG>` (`tools/mutate-and-run.sh:613-620`), leg→table map `tools/mte-interop.py:74-78` |
| `SURVIVED` | `Survived` | yes — `totalValid` +1 | no — counts as `totalUndetected` | same two rows as above; the aggregate is the `survived=` field of the leg's `REGRESSION_TABLE` row (`tools/mutate-and-run.sh:1249`) |
| `INCONCLUSIVE` (exit 124 / 126 / 127) | `RuntimeError` | **no** — counts as `totalInvalid` +1, leaves the score denominator; still counted in `totalMutants` | no | measured row `results.tsv`; aggregate is the `inconclusive=` field of the leg's `REGRESSION_TABLE` row (`tools/mutate-and-run.sh:1249`, parsed at `tools/mte-interop.py:71-72`) |

Reading the columns: *"counts in valid?"* is membership of the official
`totalValid` denominator; *"counts as detected?"* is membership of the
`totalDetected` numerator. Both are the vendored library's own arithmetic
(`mutation-testing-metrics` 3.9.0, `package/dist/src/calculateMetrics.js:169-191`),
not tameshi's.

Two invariants follow from the table and are what the checks enforce:

- **The denominator is `killed + survived`.** `INCONCLUSIVE → RuntimeError` keeps an
  inconclusive mutant out of `totalValid`, so the official denominator is the same
  population tameshi's kill rate divides by — the official `mutationScore` and
  tameshi's `killed/(killed+survived)` agree to within 1e-9
  (`tools/mte-interop.py:243-248`; the tool calls this check *sanity only*).
- **A leg conforms only on four independent checks.** `schema` (official schema),
  `score` (official metrics vs tameshi's rate), `ledger` (official counts vs the
  runner's own measured `REGRESSION_TABLE` row, `flips == 0`), `per_mutant` (every
  mutant's status vs the *committed* per-defect recorded verdict table). The first
  and last are independent of this run; `ledger` is independent of the emitter
  (`tools/mte-interop.py:237-262`).

### Three export error patterns, each pinned by a selftest case

The selftest of `tools/mte-interop.py` is a battery of doctored reports; each case
below is a real report that must be rejected, and the case name is the anchor.

| # | error pattern | what it looks like | why it is wrong | selftest case (tools/mte-interop.py) |
|---|---|---|---|---|
| E1 | **tameshi vocabulary leaks into the MTE status** | a mutant emitted with `status: "KILLED"` (or `"SURVIVED"`) instead of the schema's `"Killed"`/`"Survived"` | the official schema's status enum is `Killed, Survived, NoCoverage, CompileError, RuntimeError, Timeout, Ignored, Pending` (vendored `package/src/mutation-testing-report-schema.json:92`); tameshi's own tokens are not in it, so the report is invalid before any counting happens | `tameshi-vocabulary-status` (`:406`) |
| E2 | **line 0 location** | a mutant's `location.start`/`location.end` emitted with `line: 0` (0-based or off-by-one line/column) | the schema's `position` is 1-based on both axes (`minimum: 1`, vendored `package/src/mutation-testing-report-schema.json:310-320`); the emitter derives 1-based, end-exclusive positions from the unique `@old` string (`tools/mte-interop.py:126-130,150-155`), pinned by the positive case `emitter-locations` (`:436`: `D1 (1,1,1,6)`, `D2 (2,1,3,9)`, `D3 (3,5,3,9)`) | `line-zero-location` (`:407`) |
| E3 | **a timeout reported as a kill** | a mutant whose tameshi verdict was not a kill emitted with `status: "Timeout"` (or `"Killed"`), e.g. an `INCONCLUSIVE`/timeout row | the official library counts `timeout` inside `totalDetected` (`calculateMetrics.js:170`), so the official score reads higher than tameshi's kill rate and the two stop meaning the same thing; the export of an inconclusive row is `RuntimeError`, which is invalid and leaves both the numerator and the denominator | `timeout-is-not-a-tameshi-kill` (`:414`) |

Rule of thumb, in one line: **the MTE status is a rendering of the runner's verdict
cell, and the verdict cell is the only thing that may decide it.**
```

---

## 3. Evidence for the three error patterns (observed, not asserted)

Command (in `/tmp/r25-draftskill`, a copy of the pinned tool plus the vendored
packages; the lane checkout was never executed):

```
$ cd /tmp/r25-draftskill && uv run --no-project --with jsonschema==4.25.1 \
    python3 tools/mte-interop.py --selftest
```

Observed lines (verbatim, from the run at tool sha `24de859f…`):

```
CASE tameshi-vocabulary-status PASS (schema=invalid:'KILLED' is not one of ['Killed', 'Survived', 'NoCoverage', 'CompileError', 'RuntimeError', 'Timeout', 'Ignored', 'Pendi official_score=50 official_killed=1 official_survived=1 official_invalid=0 recorded=2/3 per_mutant=mismatch failed=ledger,per_mutant,schema,score)
CASE line-zero-location PASS (schema=invalid:0 is less than the minimum of 1|0 is less than the minimum of 1 official_score=66.66666666666666 official_killed=2 official_survived=1 official_invalid=0 recorded=2/3 per_mutant=ok failed=schema)
CASE timeout-is-not-a-tameshi-kill PASS (schema=ok official_score=66.66666666666666 official_killed=1 official_survived=1 official_invalid=0 recorded=1/3 per_mutant=mismatch failed=ledger,per_mutant,score)
MTE_SELFTEST: 16/16 pass
```

Each case is declared with the check that must reject it — `schema`, `schema`, `score`
respectively (`tools/mte-interop.py:406,407,414`) — and each case's declared reason is
present in its `failed=` list. `MTE_SELFTEST: 16/16 pass`, exit 0.

Neighbouring cases in the same battery, cited for coverage:

| case | line | what it pins |
|---|---|---|
| `survived-as-nocoverage` | `:412` | `NoCoverage` is valid-but-undetected, so a survivor mis-typed as `NoCoverage` breaks the `ledger` check (official `survived` 0 vs recorded 1) — it does not hide |
| `inconclusive-is-not-recorded-survived` | `:413` | an `INCONCLUSIVE` row exported as `Survived` breaks `per_mutant` |
| `status-flipped-vs-verdict` | `:410` | a flipped status breaks `per_mutant` even when the aggregate counts still balance |
| `balanced-flip-same-counts` | `:411` | equal aggregate counts are not evidence — only `per_mutant` catches a swap |
| `runner-flips-nonzero` | `:416` | a non-zero `flips` in the runner's row breaks `ledger` |
| `no-recorded-table` | `:418` | a leg with no committed recorded table cannot pass `per_mutant` |
| `emitter-inconclusive-to-runtimeerror` | `:419` | positive control: the real emitter maps `INCONCLUSIVE → RuntimeError` and the leg still conforms |
| `emitter-locations` | `:436` | positive control: 1-based, end-exclusive locations from the unique `@old` |

---

## 4. Findings (for the canonical judge)

1. **The tool file moved under the drafter.** `tools/mte-interop.py` changed revision
   three times during this drafting session (sha256 `e0c5f2f3…` → `8c24255c…` →
   `24de859f…`; 454 → 455 lines; `git status --porcelain` shows ` M tools/mte-interop.py`
   against lane revision `09dc114`). Every line number in this report is against
   `24de859f…`; a reader on a different revision must re-resolve, not trust. The
   *semantics* (status map, four checks, three error patterns) were stable across all
   three revisions.
2. **The `ledger` check's contract changed between the two revisions** and the draft
   follows the newer one. The earlier revision compared official `totalValid` against
   the recorded defect count; the current revision compares `totalMutants == defects`
   **and** `totalInvalid == inconclusive` (`tools/mte-interop.py:250-255`). The newer
   form is the one that survives inconclusive rows, because `RuntimeError` mutants are
   invalid rather than valid. A draft that quoted the older contract would be wrong.
3. **The `score` check is not independent evidence.** With the 1:1
   `KILLED→Killed` / `SURVIVED→Survived` mapping the equality holds by construction;
   the tool says so in its own comment (`tools/mte-interop.py:246`). The draft
   therefore states it as an invariant plus a sanity check, and leans on `ledger` and
   `per_mutant` for the load-bearing claims.
4. **`Timeout` is a detected status in the official library**, not an invalid one —
   the single most dangerous export mistake, because it inflates the official score
   instead of breaking it loudly. This is E3 and is why `INCONCLUSIVE` must map to
   `RuntimeError` (`:69`) and never to `Timeout`.
5. **Coverage of the mandated columns.** "counts in valid?" and "counts as detected?"
   are answered from measured library behaviour per status (probe output in §1.2), not
   inferred. "source row" is resolved to the two rows that actually carry a verdict —
   the measured `results.tsv` row and the committed `TABLE_<LEG>` row — plus the
   aggregate `REGRESSION_TABLE` row where the count is checked.

## 5. Out of scope (not touched)

- `SKILL.md` itself — not edited; the draft is text only.
- The C2 counter run (`--check --fleet-root`) — not run by this seat; it is a
  different seat's item and needs the fleet, not a `/tmp` copy.
- `tools/mte-interop.py` and `tools/mutate-and-run.sh` — not edited.
- The fleet root `/home/vgpnk/Projects/shokunin` and sibling lanes — read only, and
  not read at all for this item.

## 6. Tooling

No new tool was installed. The selftest used the same pinned dependency the C2
counter names — `uv run --no-project --with jsonschema==4.25.1` (Python `jsonschema`
4.25.1, ephemeral uv environment; nothing added to the host) — with the host's
`node v24.21.0` and `uv` already present. The metrics probe ran the vendored
library from `tools/vendor/mutation-testing-metrics-3.9.0.tgz` as extracted into
`/tmp/r25-metrics-probe/node_modules/`, so the probe measured the pinned bytes and
not a registry copy.

## 7. Artifact paths

- This report: `tameshi-shokunin/.ufo/waves/round-25/w1/DraftSkillTable.md`
- Drafted section text: §2 above (paste-ready markdown block)
- Scratch (throwaway, outside the lane): `/tmp/r25-draftskill/` (tool copy + vendored
  packages), `/tmp/r25-metrics-probe/` (metrics probe), `/tmp/mte-schema-x/`,
  `/tmp/mte-metrics-x/` (extracted tarballs)
