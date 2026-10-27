# T53W1Read29 — cold read of `### Using the ledger` at C*

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Content commit `C*`: `a41195dfc13a73958e4c5228ec196b28d03ded03`
- Section: heading `### Using the ledger`, lines **935–966** of `SKILL.md` at C* (bytes read with `git show C*:SKILL.md`, never the working tree; 194878 bytes)
- `section_sha256`: `1a6d9681bd90321ff6e66fa9887ed7e31026e40942aa02d2bbed11a74d2390fe`
- Hash method: the **frozen round-18 sectionize** (`.ufo/evidence/round-18/measure.py` extracted from C*, `importlib`-loaded) over the C* blob → 64 sections, this one `start=935 end=966`. An independent reimplementation of the documented rule (headings `^#{1,3}(\s|$)` outside ``` fences, trailing whitespace-only lines stripped, `\n` join, no trailing newline, UTF-8 surrogateescape) produced the identical range and digest.
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read29/` (created, used, deleted before yield). No pacman; no tool installs; no git/jj mutation anywhere; no write outside my deliverables and that scratch.

## Checks run

All reads at C* via `git show C*:<path>` (tool blob dumped to scratch as `mutate.sh`, 2159 lines, `sha256=977de470…` per its own `REGRESSION_TOOL` line).

### 1. Line anchors in the section, each verified against the C* blob

| Section pointer | C* content |
|---|---|
| `tools/mutate-and-run.sh:139-143` | the `--regression` exit map: `0 all cases PASS · 1 >= 1 case FAIL · 2 a case could not be verified` |
| `:1519-1548` | FAIL→`exit 1` (1519-1524), SETUP→`exit 2` (1525-1530), r30 tally-mismatch SETUP→`exit 2` (1531-1539), PASS print + `rm -rf "$root"` when `auto=1 && KEEP=0` (1540-1547), `exit 0` (1548) |
| `:78-79` | `# MUTATE: DONE|DEGRADED (target=… defects=… killed=… survived=… inconclusive=… kill-rate=…%)` and `# MUTATE: SETUP (<reason>)` |
| `:614-643` | `PIN_JS` (614) … `TABLE_DRIFTPINS` (643) — exactly the pins/revisions/tables block |
| `:671-849` | `regression_specs()` (671) through the fourth spec's `EOT` (849); legs 1–4 only |
| `:83-108` | `--regression` inventory header (83), ten leg rows + source lines (84-104), leg-8/leg-9 provenance start (105-108) |
| `:1459-1508` | the ten `regression_case_git …` dispatches and their `st_*=$?` captures (first 1459, last 1504-1508) |
| `:1275-1317` | `git show <rev>:<path> >"$dst"` (1276), blob-mode mirror (1285-1300), `REGRESSION_PIN` printf (1302-1306), target/pin mismatch refusal (1307-1317) |
| `:1302-1306` | `printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s mode=%s sha256=%s\n'` + the `source=file` arm |

### 2. Provenance of the legs (holds)

`git show <rev>:<path>` sha256 for each of the ten legs equals the recorded `PIN_*` (all ten `pin_ok`), and the pinned modes are `100644` for `js-kimi-census` and `100755` for the other nine — i.e. materialized bytes and mode match what `REGRESSION_PIN … mode=… sha256=…` will print.

- tsukuroi/mado "historical pins" hold: `tsukuroi-shokunin/tools/tsukuroi-census.sh` at HEAD hashes `adb1b4ce…` ≠ pin `084951be…`; `mado-shokunin/tools/mado-verify.sh` at HEAD hashes `050efc72…` ≠ pin `d7edaab4…`. The pins are old revisions, not a claim about current trees.

### 3. Scratch lifecycle and TMPDIR (holds) — executed

Run from the scratch copy at C* with `TMPDIR` bound to my scratch and no sibling repos present:

```
REGRESSION_TOOL: …/mutate.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
REGRESSION_CASE js-kimi-census: SETUP (repo_identity_mismatch: … kumitate-shokunin is not its own repository; toplevel=unresolved)
… ten SETUP lines, one per leg …
REGRESSION: SETUP (cases=10 passed=0 cannot-verify=10)
REGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r53/w1/T53W1Read29/t/tameshi-r4-2-regression.OAqO1K (kept)
EXIT=2
```

This evidences, at C*: `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` allocated under the bound `TMPDIR`; a refusal happens before that leg's suite; **later legs still run** and their statuses aggregate; a SETUP run retains the root; exit 2. The PASS arm (`removed on PASS unless --keep`) is the code at :1542-1547 and was not executed (see Limits).

### 4. Receipt counts (holds)

`local nlegs=…` per round, read from the blob at each revision: `9f1d3c3` (r7) → **4**; `c699c8c` (r16) → **7**; `58e5d53` (r18) → **8**; `a08e85c` (r26) → **9**; `6d8c11e` (r51) and C* → **10**. So "N=4 at r7-1, 7 since round 16, 8 since round 18, 9 since round 26, 10 since round 51" holds. The receipt literally printed at :1540 is `REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)` — the cited shape.

### 5. Contribution-contract items (holds)

The ten embedded specs carry 10/10/10/10/15/10/10/10/10/10 defects (105 total); every defect has exactly one `@old` and one `@new`, none has `@new == @old`; every suite string names `$MUTANT` and runs `--selftest`. The round-52 bracket "no current leg records a skipped count — enumerated and executed only" is accurate: the verdict vocabulary is `KILLED | SURVIVED | INCONCLUSIVE` (usage, :242) and the report line (:78) has `defects/killed/survived/inconclusive` with no skip field.

## Finding

### F1 — the anchor parenthetical attributes the current range to round 26

Verbatim quote (present byte-exact in the section, line 962):

> (round 52 re-anchor; round 26 recorded :614-643)

Why it fails at C*:

1. Round 26's tool did not have the pins/revisions/tables block at `:614-643`. `git show a08e85c:tools/mutate-and-run.sh` → `603:PIN_JS=…`, `621:TABLE_JS='…'`, `629:TABLE_CITECHECK='…'`, `630:FLEET_ROOT=''` — the block is **:603-629** (nine legs; `TABLE_DRIFTPINS` does not exist yet, so the range's own end line cannot be a round-26 line).
2. Round 26 recorded a different anchor for the same block: `git show a08e85c:SKILL.md | grep -n 'pins/revisions/tables'` → line 960 `Current anchors: pins/revisions/tables tools/mutate-and-run.sh:597-620,` (with `eight dispatches :1314-1356`). The round-51 page likewise recorded `(round 26): … :603-629` — never `:614-643`.
3. `:614-643` is the **round-51** block: `git show 6d8c11e:tools/mutate-and-run.sh` → `614:PIN_JS=…`, `643:TABLE_DRIFTPINS='…'`. That range comes into existence with the tenth leg at round 51.
4. `git log --oneline -S ':614-643' -- SKILL.md` returns only `7ff81a5` (round-52 wave-2). Its diff shows the mislabel being introduced: the old line `Current anchors (round 26): … :603-629` was replaced by `Current anchors (round 52 re-anchor; round 26 recorded :614-643): … :614-643` — the "round 26" label survived while the number was replaced with the round-51/52 value.

So a reader who treats the parenthetical as provenance and checks round 26 finds `REV_CLAIMS … table_count` at `:614-643`, and finds the real pins/tables block at `:603-629`. The four current numbers themselves (`:614-643`, `:671-849`, `:83-108`, `:1459-1508`) are correct at C* — only the round attribution is false.

## Rejected candidate (recorded, not filed)

- The bullet "Exits0/1/2: PASS/FAIL/SETUP" is not exhaustive for the command: `--regression --target X` and `--regression --bogus` both exited **64** (`EXIT_noargs=64`, `EXIT_bogus=64`) via `usage_exit` (:247-251, :1419, :2150). Not filed as a finding: the statement maps exit→case status and its own cited anchor (`:139-143`) carries the identical 0/1/2-only map, with `64 usage error` documented at `:81-82`. Under the "a statement that does not hold" test the mapping holds; the omission is a tool-documentation choice reproduced faithfully.

## Limits

- The full ten-leg PASS ledger was not executed from this seat (legs 1–6 run their gates **without** the `env -i` wrapper that legs 7–10 use, so a full run touches the host `HOME`); the PASS/removal arm is verified from the C* blob (:1540-1547) and the induced SETUP arm above was executed end to end. `--keep` on PASS was likewise not executed (same code path).
- The r7–r51 `nlegs` values were read from the blob at each landing revision, not from receipts of live runs.
- No claim here rests on the working tree; the C* blob and `git show` object reads are the only sources.
