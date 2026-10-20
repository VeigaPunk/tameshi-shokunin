# RGPriorCase — C1 recording mechanics: reconstructing how the sixth ledger case was recorded

Read-only reconstruction. No lane file was modified; no mutant was run; no suite was executed.
One sibling blob was materialized under `/tmp/tameshi-r16-RGPriorCase-WfE0lC/` (contract-sanctioned
`git show` read). Evidence marks: **[O]** = observed command/file output; **[I]** = inference.

Artifacts read (both inside the lane root):

| path | lines | sha256 |
|---|---|---|
| `tools/mutate-and-run.sh` | 1642 | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` |
| `corpus/knowledge/mutation-case-kumitate-claims.md` | 410 (409 newlines; no trailing newline) | `3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9` |

Both hashes measured this session. The tool's header self-identifies as `r10-2 (tameshi-shokunin,
2026-10-14)`; the note's Method paragraph pins the tool at `cf41efaa…` (1,341 L), i.e. the r7-1
revision — that difference is the documented pre-embedding state, not drift (see §1.3).

---

## 1. The sixth case, end to end

### 1.1 What the sixth case is

`js-claims-check` = `kumitate-shokunin/scripts/claims-check.mjs`, T8-2, tameshi round 8, recorded
2026-10-14 19:12:43Z. Note: `corpus/knowledge/mutation-case-kumitate-claims.md`. **[O]**

- Pin: `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b`, 48,265 B, 926 L
  (final line carries no trailing newline), git blob `fae4bbcd…` at kumitate HEAD `175de6b`
  (note `:11-21`). **[O]**
- Suite: `node "$MUTANT" --selftest`; result 7/10 killed, survivors D7/D8/D9, 0 inconclusive,
  restore `before=after` (note `:22-31`, `:63-65`, `:81-95`). **[O]**
- Spec: the ten exact edits in note `§8` (`:347-409`), held in the sweep scratch as
  `/tmp/w8-t8-2-claims/spec/claims-check.defects.spec` and later embedded **verbatim** in the tool
  (tool `:841-844`: `# r10-2 leg 6: … the recorded T8-2 spec file verbatim (> /tmp/w8-t8-2-claims/spec/
  claims-check.defects.spec), every @old re-verified count==1 against the pinned blob.`). **[O]**

### 1.2 The three-stage recording path (the thing to mirror)

1. **Sweep stage** — the case is run through `tools/mutate-and-run.sh` in `--target/--defects/
   --suite` mode against a materialized pinned copy; the note is the only fleet write. The note's
   `§6` explicitly says the table is *not* embedded at that time and files the embedding as
   follow-up `E3` (`:313-325`). **[O]**
2. **Embedding stage** — a later lane that owns the tool (r10-2, TAMESHI-T10-2) cut the recorded
   spec file into `regression_specs()` as heredoc `js-claims-check.spec`, added the pin/rev/table
   triplet, the leg invocation, the expectation printf, and the selftest ledger entry. The header
   records the resolution (`:11-14`, `:80`, `:93-97`, `:144-151`, `:195-197`) and the leg comment
   records the spec's provenance and re-verification (`:841-844`). **[O]**
3. **Ledger stage** — the leg becomes one row of the `--regression` sweep; its recorded §1 table is
   its exact expectation. `grep -n 'round-gate' tools/mutate-and-run.sh` → **no match, rc=1** [O]:
   the seventh leg is entirely additive.

### 1.3 Consequence for the seventh case

The note under reconstruction records the tool at `cf41efaa…` and says "cases=4" (`:313-325`). The
current tool is the r10-2 state and prints `cases=6`. A seventh case must be recorded against the
**current** tool state (pin the tool sha at sweep time in the new note's Method paragraph) and its
§6 must be able to quote a `REGRESSION: PASS (cases=7 …)` line over itself — the capability the
sixth note could not have. **[I]**

---

## 2. Every place `mutate-and-run.sh` enumerates the six legs or the number six

`grep -nE 'six|sixth|TABLE_|PIN_|REV_|leg|nlegs|cases='` plus an exhaustive standalone-`6` grep
(`grep -nE '(^|[^0-9A-Za-z_.])6([^0-9A-Za-z_.]|$)'`, rc=0). Complete leg-count surface:

| # | lines | kind | verbatim / content |
|---|---|---|---|
| 1 | 11–14 | header channels | `…cases 5/6 (kagi \`corpus/checklist-run.sh\`, kumitate \`scripts/claims-check.mjs\`) embedded as the fifth and sixth legs, completing the six measured gates in this ledger.` |
| 2 | 80 | header heading | `# --regression (r4-2; r7-1 leg ledger; r10-2 six legs) — the fleet's recorded` |
| 3 | 84–89 | header leg table | six rows: `js-kimi-census … 8/10 (80 %)`, `bash-surface-census … 8/10 (80 %)`, `bash-tsukuroi-census … 6/10 (60 %)`, `bash-mado-verify … 4/10 (40 %)`, `bash-checklist-run … 7/15 (47 %)`, `js-claims-check … 7/10 (70 %)` |
| 4 | 90–96 | header source list | six note refs, then `All six defect specs are embedded below (legs 1–4 cut from those notes' §7/§8/§9 reproduce manifests, all 40 @old strings re-verified count==1…; legs 5–6 are the recorded T8-1/T8-2 spec files, their 25 @old strings re-verified…)` |
| 5 | 144–151 | header selftest contract | `r10-2 adds the embedded-ledger sweep: the six leg specs are written and parsed, and each recorded table's ids, total and killed count are checked against its own spec…` |
| 6 | 195–197 | `usage()` prose | `--regression replays every recorded mutation case as a leg (js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, bash-checklist-run, js-claims-check) at its pinned original revision,` |
| 7 | 522–524 | section comment | `# Recorded expectations for --regression (r7-1 leg ledger; r10-2 leg cut # resolved — cases 5/6 embedded). Anchors:` |
| 8 | 535–541 | per-note anchors | six `mutation-case-…md §N` refs; the sixth is `mutation-case-kumitate-claims.md §1 (js — control green, killed D1-D6,D10, survived D7,D8,D9, 7/10 = 70 % at :63-65). The specs below: legs 1–4 are …; legs 5–6 are the recorded T8-1/T8-2 spec files …` |
| 9 | 542–553 | pin/rev block | six `PIN_*` + six `REV_*` pairs (interleaved per leg) |
| 10 | 554–559 | table block | six `TABLE_*` assignments, one line each |
| 11 | 587–891 | `regression_specs()` | six heredocs (`cat >"$d/<leg>.spec" <<'EOT'`) at **589, 630, 675, 720, 770, 845**, bodies ending at **629, 670, 715, 765, 840, 888**; six-way non-empty guard at **889–891**. Stale docstring at **587**: `# <dir> — write the two embedded case specs` (already false at six) |
| 12 | 1103–1109 | `REGRESSION_EXPECT` | one printf naming all six `<leg>=%s/%s` pairs and passing twelve `table_count`/`table_total` args |
| 13 | 1111 | locals | `local st_js st_kagi st_tsu st_mado st_checklist st_claims` |
| 14 | 1112–1141 | leg invocations | six `regression_case_git` calls (start lines 1112, 1117, 1122, 1127, 1132, 1137), each `name`, fleet-relative target, `$PIN_*`, `$REV_*`, spec path, suite, `$TABLE_*`, case workdir |
| 15 | 1143 | count literal | `local nlegs=6 npass=0 nfail=0 nsetup=0 st` |
| 16 | 1144 | status loop | `for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims"; do` |
| 17 | 1566–1571 | selftest comment | `# r10-2 (TAMESHI-T10-2) leg-cut resolution: the six embedded legs' specs and # recorded tables must agree with each other …` |
| 18 | 1576 | selftest label | `st 'embedded leg specs: six files written' $?` |
| 19 | 1577–1584 | selftest ledger tuple | `lent=(` six entries `'<leg>:<spec>:<TABLE_VAR>:<total>:<killed>'` |
| 20 | 1585–1601 | selftest loop | generic per-leg agreement loop (the only loop over `lent`); asserts sorted id-set equality, spec count == total, `table_total`, `table_count KILLED`, `table_count SURVIVED == total-killed` |

No other leg count exists. The remaining standalone `6` tokens are unrelated: step numbering `(6)`
(:65), plan anchor `plans/round-3.plan.md:6-7` (:16), py_helper argv arity (:383), target-code caps
`slice(0, 6)` in spec text (:595, :874), recorded kill-rates in comments (:86, :672, :717), the leg
number `leg 6` (:841), positional-arg slots `$6` (:911, :1068), and the tsukuroi table's killed
count `10:6` (:1580). **[O]**

---

## 3. Variable conventions and table string format

### 3.1 Placement and naming

Block order is fixed (`:522-560`): one anchor comment, then all `PIN_*`/`REV_*` (interleaved per
leg), then all `TABLE_*`, then `FLEET_ROOT=''` (`:560`). Helper functions `table_lookup` (:562),
`table_count` (:573), `table_total` (:581) follow.

- **`PIN_<TOKEN>`** — full 64-hex lowercase sha256 of the materialized blob bytes
  (`git -C <repo> show <rev>:<path> | sha256sum`). Never abbreviated. Equality is exact:
  `regression_case` compares the materialized copy's sha against it and returns 2 (SETUP) on
  mismatch (`:969-974`).
- **`REV_<TOKEN>`** — full 40-hex commit sha, gated by `git rev-parse --verify --quiet "${rev}^{commit}"`
  and `git cat-file -e "${rev}:${path}"` (`:924-930`). Revisions may repeat across legs (BASH and
  CHECKLIST both `fecee874…`; JS and CLAIMS both `175de6b…`); pins never do.
- **`TABLE_<TOKEN>`** — the recorded verdict table, single-quoted, comma-joined entries
  `ID:VERDICT`, no spaces. Example (`:559`):
  `TABLE_CLAIMS='D1:KILLED,D2:KILLED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:SURVIVED,D8:SURVIVED,D9:SURVIVED,D10:KILLED'`.
- **TOKEN** is a short uppercase handle chosen by the author, not mechanically derived
  (`JS`, `BASH`, `TSUKUROI`, `MADO`, `CHECKLIST`, `CLAIMS`). It appears verbatim in exactly four
  places: declaration, `REGRESSION_EXPECT` arg pair, `regression_case_git` arg, and the `lent`
  tuple's table-variable name (indirect expansion `${!ltbl}` at :1588). A seventh leg needs one
  consistent token (e.g. `ROUNDGATE`).

### 3.2 Table semantics (both directions enforced)

`table_lookup` (`:562-571`) splits on `,` and `:` via `${table//,/ }`, `${pair%%:*}`, `${pair#*:}`,
returning `-` when the id is absent. `regression_case` (`:1001` ff.: `while IFS=$'\t' read -r id v rest`; `table_lookup` at `:1011`):

- measured row whose id is absent from the table → `REGRESSION_DEFECT … recorded=ABSENT`, a flip;
- measured verdict ≠ recorded → flip;
- table entry absent from `results.tsv` → `measured=ABSENT recorded=<v>`, a flip.

So the table must be **exactly** the measured id set: no extras, no omissions, no
`INCONCLUSIVE` (a leg requires `inconclusive=0` at `:1043`). Ids are the spec's `@defect` ids,
charset `[A-Za-z0-9._-]` (parse at `:286`; id-charset refusal `:314`).

### 3.3 Acceptance formula

Ledger legs pass through `regression_case_git` (`:1063-1072`), which resolves `repo` from the first
fleet-relative path segment, `path` from the rest, and passes tolerance `0 0`. `regression_case`
builds `reasons` from (`:1039`–`:1052`): `|killed-exp_killed| > ktol`, `flips > ftol`,
`inconclusive > 0`, `total != exp_total`, control-not-green, restore-not-ok. PASS iff `reasons` is
empty; the leg's sweep is a full CLI sub-invocation of the tool (`:977-981`) with its own
`sweep.log`. Fixture-mode defaults are `BAND_KILLED=1`, `BAND_FLIPS=1` (`:168-169`); the ledger
legs never use them.

### 3.4 Spec format facts that bite when embedding a JS gate

- `@old` must occur exactly once per defect in the pinned blob; asserted for every defect **before
  any suite run**, else exit 2 (`:441-463`).
- Escapes are only `\n \t \r \\`; any other backslash sequence refuses the spec (`:259` `ESCAPES`; `:267-284` `unescape`). A
  literal two-character `\n` in JS source must be written `\\n` in the spec.
- CR is refused (`:293`); LF only; a `@defect` id must be unique; `@new == @old` is refused;
  `@old` empty is refused (`:340-342`).
- Embedded heredocs are quoted (`<<'EOT'`), so `$`, backticks and quotes pass literally; the body
  must simply not contain a line equal to `EOT`.
- `py_helper list` prints `<id>\t<line>\t<desc>` per defect; the selftest uses `cut -f1` for ids
  (`:346-348`, `:1593`).

---

## 4. The knowledge-note shape (sixth case, as the template)

410 lines total (409 newlines; last byte `.`, no trailing newline); heading map measured with `grep -n '^#\{1,4\} '`:

| span | section | required content |
|---|---|---|
| 1 | H1 | `# Mutation case — <repo> \`<path>\` <descriptor> (T<lane>)` |
| 3–9 | position paragraph | run date + UTC sweep time, lane, round, **which numbered case in the wave**, substrate read-only statement, "this note is the only fleet file written", no-network/no-secret line |
| 11–21 | **Pin** (provenance #1) | bold `**Pin (…).**`: path @ full sha256, byte size, line count + trailing-newline detail, git blob id @ repo HEAD, the `git show | sha256sum` cross-check, working-tree `cmp`/`porcelain` state, cross-ref to any standing pins |
| 22–31 | **Method** (provenance #2) | bold `**Method.**`: tool path @ full sha256 (+ line count), suite command, target path, defect count, `count(@old)==1` assertion, control-first, scratch dir + host/toolchain versions (node/bash/python/kernel) |
| 32–33 | **Anchors** (provenance #3) | `Anchors: **O** = observation …; **I** = inference; **U** = unknown. \`path:NNN\` = the pinned bytes above.` |
| 35 | §0 | gate choice + hermeticity (O) + method restated + bullets: control line, kill rate/survivors/inconclusive, cost, restore, composition split, pre-registration score |
| 81 (table at 83) | §1 | one table, header exactly `| # | Defect class | Injected defect (site on the pinned rev) | Exit | Suite line | Verdict | Failing cases |`; control row first (`| — | control | unmutated pristine copy | …`); one row per defect with `:NNN` site; verdict `**killed**`/`**survived**`; then a `By class:` roll-up line and `Kill mechanisms (O, verbatim from work/evidence/D*.out …)` bullets |
| 137 | §2 | survivor analysis + non-equivalence probes (probe id, pristine vs mutant output) |
| 175 | §3 | what the suite protects / read by nothing / threshold inventory / suite mechanics |
| 221 | §4 | cross-case matrix rows A–G + the fleet-axes table (one column per case) |
| 273 | §5 | calibration and errata, numbered **E1…E5**, append-only; E1 is the pre-registration score with misses recorded |
| 313 | §6 | `REGRESSION status (the harness's own gate)`: the tool's `REGRESSION: …` line, leg pins, and an explicit statement whether this case's table is embedded |
| 327 | §7 | unknowns **U1…U7** |
| 347 | §8 | reproduce manifest: scratch file listing (fenced), ordered commands (fenced, O), the ten edits with `site-line` + mutant sha256 prefix, sensitivity checks, and a spot-checks paragraph re-reading cited refs on the pinned bytes |

The note's §8 manifest commands are the recording contract: `git show <rev>:<path> > scratch/…`,
`sha256sum` of copy + working file, the uniqueness pre-check script, the `--target/--defects/
--suite/--workdir/--label/--tail` sweep, the probe script, `--regression`, and a final re-hash of
the fleet file (`:355-390`). **[O]**

---

## 5. Verified facts for the seventh case (`round-gate`)

Materialized at `/tmp/tameshi-r16-RGPriorCase-WfE0lC/round-gate.pinned.mjs`; all read-only:

```
git -C kumitate-shokunin rev-parse --verify --quiet '364f1d5954158ef8844bca4a5fef57b05d2f2ca5^{commit}'
  → 364f1d5954158ef8844bca4a5fef57b05d2f2ca5        rc=0
git -C kumitate-shokunin cat-file -e '364f1d5…:scripts/round-gate.mjs'  → path-present
git -C kumitate-shokunin ls-tree 364f1d5… -- scripts/round-gate.mjs
  → 100755 blob 1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3   scripts/round-gate.mjs
git -C kumitate-shokunin show '364f1d5…:scripts/round-gate.mjs' | sha256sum
  → f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9   (matches the C1 pin)
| wc -lc  → 1511  80415        (1511 newlines, 80,415 bytes)
tail -c 1 | xxd -p  → 0a      (file ends with LF)
merge-base --is-ancestor 364f1d5… HEAD  → rc=0   (kumitate HEAD short 1770305)
```

Static surface of the pinned blob **[O]**: self-spawns its own CLI in `--selftest`
(`runGate = spawnSync(process.execPath, [SELF, ...])`, :725-726; `SELF = fileURLToPath(import.meta.url)`,
:702), so a mutant is exercised end-to-end like `claims-check`; prints
`ROUND_GATE_SELFTEST: ${passed}/${results.length} pass` (:1505) and a hermeticity case that runs a
nested `--selftest` under a polluted env (:1389-1400). Mode is **100755**, so the leg's
`REGRESSION_PIN` line will read `mode=100755` and `regression_case` will `chmod +x` the materialized
copy (`:952`, the `blob_mode == 100755` branch) — harmless for `node "$MUTANT" --selftest`, but it must not be described as a
100644 leg.

Not verified here (other seats' lanes): control-green `60/60` and the ten mutants' verdicts. RGControl/
RGRecon own those; this report only fixes the recording mechanics.

---

## 6. Bounded recommendations for embedding `js-round-gate` as the seventh leg

All anchors verified against tool sha `75ed934d…`. Nineteen additive edits, in file order:

| # | anchor | edit |
|---|---|---|
| E1 | :11–14 | add an `r16` sentence to the channels paragraph; drop the "completing the six" claim for a seven-leg wording |
| E2 | :80 | retitle `(r4-2; r7-1 leg ledger; r10-2 six legs)` → include `r16 seven legs` |
| E3 | after :89 | add the aligned row `#   js-round-gate         kumitate-shokunin/scripts/round-gate.mjs    <k>/10 (<p> %)` (name column is 22 chars wide in the existing table) |
| E4 | :90–96 | add `mutation-case-kumitate-round-gate.md §1` to the source list; change `All six defect specs` and the `@old` totals sentence (legs 1–4 = 40, legs 5–6 = 25, seventh = 10 → 75) |
| E5 | :144–151 | `the six leg specs` → seven |
| E6 | :195–197 | add `js-round-gate` to the usage enumeration |
| E7 | :522–541 | add the new note's `§1` anchor with its kill-rate line span; extend the "legs 5–6 …" sentence to `legs 5–7` |
| E8 | after :553 / after :559 | `PIN_ROUNDGATE=f890e277…` (64 hex, from `git show … | sha256sum`, not the git blob id `1f7d623e…`), `REV_ROUNDGATE=364f1d59…` (40 hex), `TABLE_ROUNDGATE='<ids from the measured results.tsv>'` |
| E9 | :587 | fix the stale docstring `write the two embedded case specs` (already false at six) |
| E10 | between :888 and :889 | append the `cat >"$d/js-round-gate.spec" <<'EOT' … EOT` heredoc, preceded by a provenance comment in the exact `:841-844` shape: pin short sha, recorded `<k>/10 killed`, the recorded spec file **verbatim** from the pre-registration scratch path, every `@old` re-verified `count==1` against the pinned blob |
| E11 | :889–891 | extend the non-empty guard with `&& -s "$d/js-round-gate.spec"` |
| E12 | :1103–1109 | append ` js-round-gate=%s/%s` to the format string and the matching `"$(table_count "$TABLE_ROUNDGATE" KILLED)" "$(table_total "$TABLE_ROUNDGATE")"` args |
| E13 | :1111 | add `st_roundgate` to the locals |
| E14 | after :1141 | seventh `regression_case_git js-round-gate 'kumitate-shokunin/scripts/round-gate.mjs' "$PIN_ROUNDGATE" "$REV_ROUNDGATE" "$specs/js-round-gate.spec" 'node "$MUTANT" --selftest' "$TABLE_ROUNDGATE" "$root/js-round-gate"` + `st_roundgate=$?` |
| E15 | :1143 | `nlegs=6` → `nlegs=7` |
| E16 | :1144 | add `"$st_roundgate"` to the `for st in` list |
| E17 | :1566 | `the six embedded legs'` → seven |
| E18 | :1576 | `six files written` → `seven files written` |
| E19 | :1577–1584 | seventh `lent` tuple `'js-round-gate:js-round-gate.spec:TABLE_ROUNDGATE:<total>:<killed>'` |

Constraints the edits must respect:

- **Table = measurement, not prediction.** `TABLE_ROUNDGATE` must be transcribed from the sweep's
  `results.tsv` (one `KILLED|SURVIVED` per pre-registered id), because the leg's expectation is
  exact (`ktol=ftol=0`). A predicted table would make the leg fail on any calibration miss.
- **Ids must equal the spec's `@defect` ids** and the total must equal the directive count; the
  selftest (`:1595-1599`) and the per-leg sweep prep both enforce it. With ten mutants the tuple is
  `…:10:<killed>` and `TABLE_ROUNDGATE` carries ten entries.
- **Escapes/heredoc**: the round-gate source is JS and may contain literal `\n`; those must be
  `\\n` in the spec (parser unescapes `\n` to a newline). Quoted heredoc keeps `$`/backticks safe.
- **Mode**: 100755 → `REGRESSION_PIN … mode=100755`; do not hand-copy a 100644 claim into the note.
- **Suite**: `node "$MUTANT" --selftest` matches the pinned blob's own `--selftest` entry (it wins
  over other modes, blob :23, :294) and its self-spawn design exercises the mutant CLI.
- **Tool selftest count**: 34 static `st` call sites with exactly one loop (six `lent` entries), so
  the hermetic selftest reports `39/39` today and would report `40/40` with a seventh leg
  **[I — static count; not executed]**. Do not hardcode a count anywhere; the script prints
  `cases-failed/cases`.
- **Note for the case**: create `corpus/knowledge/mutation-case-kumitate-round-gate.md` in the
  §4 skeleton, with the provenance trio (Pin / Method / Anchors) and §1 exactly in the measured
  table shape; §5 must record the pre-registration score against
  `corpus/knowledge/arm-class-matrix.md §13` (verdicts and failing-case counts, misses left in);
  §6 can now quote `REGRESSION: PASS (cases=7 …)`; §8 must list the scratch spec path that E10
  embeds verbatim.

Out-of-scope but adjacent (named, not acted on): the corpus README row, `LOG.md`, and
`fleet-kill-rate-ledger.md` are owned by other lanes; the sixth note's E4 records that the ledger's
own cadence appends cases, not the sweep lane.

---

## 7. Evidence log (commands, exits, key lines)

| command (cwd = lane root unless noted) | exit | key output |
|---|---|---|
| `wc -l tools/mutate-and-run.sh corpus/knowledge/mutation-case-kumitate-claims.md` | 0 | `1642`; `409` (409 newlines, 410 lines — no trailing LF) |
| `sha256sum tools/mutate-and-run.sh` | 0 | `75ed934d…adc5` |
| `sha256sum corpus/knowledge/mutation-case-kumitate-claims.md` | 0 | `3da1312e…45d9` |
| `grep -nE 'six|sixth|TABLE_|PIN_|REV_|leg |legs|nlegs|cases=' tools/mutate-and-run.sh` | 0 | the map in §2 |
| `grep -nE '(^|[^0-9A-Za-z_.])6([^0-9A-Za-z_.]|$)' tools/mutate-and-run.sh` | 0 | standalone `6` tokens listed in §2 (none hidden) |
| `grep -n 'round-gate\|roundgate' tools/mutate-and-run.sh` | 1 | no output (absence confirmed) |
| `grep -nE '^(TABLE_|PIN_|REV_|BAND_|FLEET_ROOT|declare|local )' tools/mutate-and-run.sh` | 0 | declarations at 542–559 |
| `awk` numbered slices of 505–580, 585–592, 885–893, 899–1063, 1063–1076, 1100–1145, 1564–1604 | 0 | quoted lines in §2–§4 |
| `git -C kumitate-shokunin rev-parse --verify --quiet '364f1d5…^{commit}'` | 0 | full rev |
| `git -C kumitate-shokunin cat-file -e '364f1d5…:scripts/round-gate.mjs'` | 0 | path present |
| `git -C kumitate-shokunin ls-tree 364f1d5… -- scripts/round-gate.mjs` | 0 | `100755 blob 1f7d623e…` |
| `git … show …:scripts/round-gate.mjs \| sha256sum` | 0 | `f890e277…d3e9` |
| `git … show … \| wc -lc` | 0 | `1511 80415` |
| `tail -c 1 /tmp/…/round-gate.pinned.mjs \| xxd -p` | 0 | `0a` |
| `git -C kumitate-shokunin merge-base --is-ancestor 364f1d5… HEAD` | 0 | rev is an ancestor of HEAD `1770305` |
| `grep -nE 'MUTATE\|SELFTEST\|--selftest\|process.execPath\|spawnSync\|fileURLToPath' /tmp/…/round-gate.pinned.mjs` | 0 | self-spawn + `ROUND_GATE_SELFTEST:` + hermeticity case |

Scratch: `/tmp/tameshi-r16-RGPriorCase-WfE0lC/` (materialized blob only). No tool installed or
upgraded this session; no pacman transaction issued. No lane file written except this report.
