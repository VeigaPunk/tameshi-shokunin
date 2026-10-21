# Section1938 — Round-20 gate/probe registry (SKILL.md:1938–1963)

**Verdict:** done / **no-blocking-gaps** (re-anchor feasible at pin; two verdict-map wording defects)

**Read revision:** `790abd2129f153c13b471e381d454186edbde65e`  
**Scope:** SKILL.md lines 1938–1963 only. No mutation recipes re-run; no cold-read replay. Sources via `git show 790abd2129f153c13b471e381d454186edbde65e:<path>`.

**Commands used:** `git show` / `git grep` on pinned paths only (no installs, no selftest execution).

---

## Axes (godspeed)

| Axis | Result |
|---|---|
| CLI / exit-map fidelity vs pinned tools | Mostly holds; two table cells mislabel exit 64 |
| Citation anchoring (lesson, contract, stage bytes) | Holds; QUALITY41 is composite source, not text inside `round-20.md` |
| Historical vs current claims | `--check` in `contract.json` marked historical; table + wrapper are current |
| Deletable duplicate prose | Recipe block (1953–1962) largely repeats `corpus/lessons/round-20.md` |

---

## What was checked

### Source preamble (1940–1945)

- **`corpus/lessons/round-20.md`:** Gate § (S049 child-env boundary, admit/reject rules), Mistakes row on `--check` drift, and C01SchemaComplete on `install_window` / `expectations` align with the recipe paragraph.
- **QUALITY41:** Present as criterion 41 in `corpus/QUALITY.md:388–396` (freeze-before-dispatch, interval rules). **Not** named in `round-20.md` (Mistakes cite QUALITY20/21). Treating QUALITY41 as a co-source alongside the lesson is **discoverable** via LOG/README/residual notes; not a false claim, but not a line citation inside the lesson file.
- **`--check` omission / `runner_sha256`:** `contract.json` `measurement` still records staged `--check` (`git show …:contract.json`). Active counting CLI in the table uses `tools/receipt-measure.py … --json`. Wrapper docstring and selftest explicitly reject `--check` and print `RECEIPT_MEASURE_RUNNER_SHA256` (`tools/receipt-measure.py` at pin). **Current assertion accurate**; contract string is **dated historical** (also narrated in lesson Mistakes).

### Row: `tools/receipt-window.py` (1949)

| Claim | Evidence |
|---|---|
| Gate CLI | Matches `argparse` in `tools/receipt-window.py` (`--contract`, `--receipts`, `--json`). |
| Exits 0/1/2/64 | Docstring L12; `EXIT_CLEAN, EXIT_FAIL, EXIT_CE, EXIT_USAGE = 0, 1, 2, 64` L23. |
| Selftest | `python3 tools/receipt-window.py --selftest`; registry row `receipt-window-selftest` sources `SKILL.md@c51eb32f:1949`. |
| Runtime inputs | Gate reads contract + receipts only (`load_contract`, `load_receipts`). |
| `public-cli-cases.json` | File exists at `.ufo/evidence/round-20/public-cli-cases.json`; consumed as fixture manifest in `.ufo/evidence/round-20/final/public-cli-results.json` (20 held cases invoking `tools/receipt-window.py`). **Not** loaded by `receipt-window.py` source at pin (`git grep` on tool tree: no match). Persisted-values column is **evidence-scope** (lesson L153 references `final/public-cli-results.json`), not runtime gate inputs. |

**Wrong expectation (1):** Verdict cell ends with `64 usage/could-not-evaluate`. In the tool, **64 is usage only** and **2 is could-not-evaluate** (separate codes). Round-21 registry rows use the clearer pattern `2 could-not-evaluate; 64 usage`. Slash grouping here blurs two exits.

### Row: `tools/receipt-measure.py` (1950)

| Claim | Evidence |
|---|---|
| Delegates to frozen stage ruler | `MEASURE = …/stage/measure.py`; `subprocess.run([…, MEASURE, *arguments])`. |
| Six predicates | `ITEM_IDS` six entries; `stage/measure.py` `TOTAL = 6`, docstring “six receipt-window population items”. |
| Exits 0 / 1 / 2 | Stage ruler L11–12: `0 corrected==total, 1 otherwise, 2 could-not-evaluate`. Wrapper adds usage **2** for bad `--selftest` / missing `--repo` (selftest L308–309). No exit 64 in this chain. |
| `2 usage/could-not-evaluate` | **Accurate:** both usage faults and CE paths use exit **2** in wrapper + staged ruler. |
| No live-tree writes in selftest | `tempfile.TemporaryDirectory(prefix="receipt-measure-selftest.")`. |

### Row: `.ufo/evidence/round-20/coldread/measure.py` (1951)

| Claim | Evidence |
|---|---|
| Default round-20 ledger | `LEDGER = '.ufo/evidence/round-20/coldread/ledger.json'`; delegates to `.ufo/evidence/round-18/measure.py`. |
| `--explain` on entry CLI | Round-18 `main()` supports `--explain` (L1535–1536); coldread passes argv through after override check. |
| Override refusal / 64 | `FORBIDDEN_OVERRIDES`; `sys.exit(64)` with `SELECTOR_OVERRIDE_FORBIDDEN` (coldread `__main__` at pin). Selftest covers `=` and abbreviated forms. |
| Non-selftest exits | Delegated `measure.main()` returns **0** (observed JSON) or **2** (CE); coldread adds **64** before delegate. No exit **1** on probe path (selftest alone uses 0/1). |
| Selftest 0/1 | `return 0 if passed == len(outcomes) else 1`. |

**Wrong expectation (2):** Verdict cell `64 usage/forbidden override (could-not-evaluate)` parenthesizes **could-not-evaluate** on the **64** arm. **64** is forbidden-override usage; **2** is could-not-evaluate from the delegated ruler.

### Recipe paragraph (1953–1962)

- **`edit_interval` vs `install_window`:** `receipt-window.py` `load_contract` uses `edit_interval` on instruments; no `install_window` reference in tool source. Contract instruments still carry `install_window` (planning). Matches lesson C01SchemaComplete (L75–81).
- **Six hardcoded predicates / not generic schema validator:** Matches `stage/measure.py` hardcoded paths and population checks.
- **`expectations` not enforced by ruler:** Top-level `contract.json` `expectations` object present; stage ruler does not read it (lesson L81).

---

## Agreements with pinned implementation

- Frozen receipt-window gate behavior and exit map (tool source).
- Wrapper as published counting entry without `--check`; `runner_sha256` vs `instrument_sha256` split.
- Six-item C1 ruler and historical-instrument classification semantics.
- Round-20 coldread selector ledger default and strict override refusal.
- Registry selftest rows for all three instruments (`tools/registry.json` at pin).

---

## Wrong expectations (count: 2)

1. **SKILL.md:1949** — `64 usage/could-not-evaluate` conflates exit **64** (usage) with exit **2** (could-not-evaluate). Source: `tools/receipt-window.py:12,23`.
2. **SKILL.md:1951** — `(could-not-evaluate)` attached to the **64** / forbidden-override clause. Source: coldread `__main__` (64 + stderr) vs `.ufo/evidence/round-18/measure.py` (returns 2 for CE, 0 for success).

No other blocking gaps for L1 re-anchor: line range, tool paths, and lesson linkage are stable at `790abd21`.

---

## Obsolete / duplicated prose (deletion candidates — not edited)

Safe to trim later **without behavior change** if replaced by pointers:

1. **1953–1962** — Nearly full duplicate of `corpus/lessons/round-20.md` Gate workflow, C01SchemaComplete, and QUALITY41 bounds already stated in lesson + QUALITY.md.
2. **1940–1945 (partial)** — `--check` / `runner_sha256` narrative repeats lesson Mistakes row and `receipt-measure.py` header; table row already states effective CLI.
3. **Verdict-map shorthand** — Could normalize to round-21 style (`2 …; 64 …` on separate clauses) instead of slash/parenthetical forms; cosmetic + calibration, not tool change.

**Preserve:** Table rows (registry contract for `tools/registry.json` sources), distinct instrument names/paths, and explicit “not generic schema validator / not blind cold-read” bounds (coldread row L1951 narrative).

---

## Historical vs current (explicit)

| Assertion | Kind |
|---|---|
| `contract.json` `measurement` includes `--check` on staged `measure.py` | Historical committed drift; documented in lesson + SKILL preamble |
| Stage paths under `.ufo/evidence/round-20/stage/` byte-frozen | Historical evidence; installed tools delegate or copy |
| `public-cli-results.json` observations | Historical measurements; manifest `public-cli-cases.json` |
| Table CLI `receipt-measure.py … --json` | **Current** counting entry |
| QUALITY41 criterion text | **Current** corpus; linked from SKILL, not duplicated in lesson body |

---

## Evidence artifact

Machine mark: `.ufo/waves/round-21/w2/sections/1938.json`

**Installs:** none
