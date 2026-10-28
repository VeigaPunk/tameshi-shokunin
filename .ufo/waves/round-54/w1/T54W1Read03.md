# T54W1Read03 — cold read: `### The boundaries — what a service run is not`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Content commit (cand): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- Section at C0: lines 869-893 of `SKILL.md`, `section_sha256` `9aa3c41cfd365e32cc8e1feb1155e0be96df016dd5ea5c6d3ffa80aa8df3ba63`
- Every read below is of git objects at C0 (`git show 59c3810:SKILL.md`, etc.); no working-tree read of `SKILL.md` was used for the section bytes.
- Mode: cold read, executor with no oral context. No lane file was edited; no mutating git command was run anywhere.

Reader command (scratch `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read03`):

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && \
  python3 .ufo/waves/round-54/reader-section.py \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    59c38109bf119d0e9d4f878644a82babc937bc1e \
    "### The boundaries — what a service run is not"
```

Output:

```
{"heading": "### The boundaries \u2014 what a service run is not", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 869, "end": 893, "section_sha256": "9aa3c41cfd365e32cc8e1feb1155e0be96df016dd5ea5c6d3ffa80aa8df3ba63"}
```

The sha was recomputed independently with the frozen round-18 `sectionize()` loaded from `.ufo/evidence/round-18/measure.py` at C0 over the C0 `SKILL.md` blob: same section (`start` 869, `end` 893) and same sha `9aa3c41c…`. The heading is in both `.ufo/evidence/round-54/c1/lost-headings-at-base.json` and `lost-headings-at-c0.json`, so this is a frozen re-read set item.

## Findings (2)

### F1 — the porcelain-clean pointer no longer resolves

Quote (byte-exact in the section):

```
porcelain-clean is an opt-in precondition at open (SKILL.md:808-809)
```

Why: at C0 `SKILL.md:808-809` is the service intro — `method outward as the service the fleet census offered` / `(`fleet-suite-census.md:249-291`): an opting-in lane brings its own gate,` — with no "porcelain", "tree-clean" or opt-in-contract text in it. The clause the pointer was written for (a pinned revision requires "a porcelain-clean sibling tree at open") is in the opt-in contract item 1, at C0 `SKILL.md:819-820`. Cause is provable: the text was at 808-809 in the round-27 read revision `2227d8338c02aa9a5fd7d95c1a41b76865ad7647` (opened in `.ufo/waves/round-27/w1/Read09.md`, which proposed this very pointer), and C0's `## Standing rules` growth shifted the page by exactly 11 lines; 808 + 11 = 819 and 809 + 11 = 820.

What I opened: `SKILL.md` at C0 lines 800-816 (the cited span, which is the census-offer sentence), 817-832 (the opt-in contract, where item 1 carries the porcelain-clean clause), 894-908 (the report shape, which says `the tool emits no separate tree-clean check — round-18 correction` and is consistent with the section's "the tool emits no tree-clean check"); `SKILL.md` at `2227d83` lines 805-812 (the same item 1 then at 808-809).

### F2 — the kill-rate-report pointer no longer resolves

Quote (byte-exact in the section):

```
a low kill rate is a report, not a service failure (SKILL.md:335)
```

Why: at C0 `SKILL.md:335` reads `Both points sit on the 50-80/>80 boundary, so that boundary reading is the worked one; the bands below carry the admission decision.` — the boundary statement, not the report convention. The rule the pointer was written for, `**Bands are a report convention, not a pass/fail gate.**`, is at C0 `SKILL.md:346-347`. Same shift: at `2227d83` line 335 was that rule (opened: `SKILL.md` at `2227d83` lines 333-337), and 335 + 11 = 346.

What I opened: `SKILL.md` at C0 lines 330-340 (which shows line 335 as the boundary sentence and the bands context), 338-362 (the kill-rate bands table and its four rules, including the report-convention rule at 346-347), and `SKILL.md` at `2227d83` lines 333-337.

No other internal `SKILL.md:NNN` pointer exists in the section (enumerated: only `335` and `808-809`).

## Checked and resolving (no finding)

- **Single-edit mutants only** — `matrix row F` resolves: `## 7. Row F — Coordinated edits` at `corpus/knowledge/arm-class-matrix.md:206` (opened; the file is named by the page itself at `SKILL.md:683`, so the shorthand is page-resolvable). The claim itself is stated at `arm-class-matrix.md:458` and in the census.
- **Hermetic suites only** — `corpus/knowledge/fleet-suite-census.md:288-291` is exactly the "Scope of the offer" paragraph ("single-edit mutants only … hermetic suites only (no substrate-drift claim, matrix U5); results are per-revision and per-host"), and those lines sit inside §5 (heading at `:249`, next heading `## 6` at `:293`), matching "census §5 scope". Census blob at C0 sha256 `ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f` — unchanged from the hash the ledger entry records.
- **Read-only, `MUTATE_RESTORE`** — the token exists at `tools/mutate-and-run.sh:570`/`:574` at C0 (blob sha256 `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`); `"'The target is never written'"` is at `:37-38`, inside the cited `:36-38`.
- **Read-only, no tree-clean check** — `tools/mutate-and-run.sh` at C0 calls `git status --porcelain` only in the self-test canaries (`:1974`, `:1986`), never in the sweep path; the tool emits `MUTATE_TOOL`/`MUTATE_TARGET`/`MUTATE_RESTORE` lines only. The statement is true as written; only its `SKILL.md:808-809` pointer is stale (F1).
- **Restore discipline** — the heading `## Restore discipline — before/after identity, not continuous non-write proof` exists at C0 `SKILL.md:386`, i.e. the section's "endpoint identity, not that no transient write occurred (the `## Restore discipline` section)" resolves.
- **Findings kept** — mado's `40 %` and "first point below the 50–80 band" are at `mutation-case-mado-verify.md:175-176` (headline sequence `80 % (JS r2) · 80 % (kagi bash r3) · 60 % (tsukuroi bash r5) · 40 % (mado bash r6)`, "The fourth point is the first below the 50–80 band"); the composition reading `4 in-surface + 6 out-of-surface, measured 4/4 and 0/6` is at `:66-69`; the `4/10 (40 %)` kill line is at `:60`. File blob at C0 sha256 `f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3`, identical to the ledger's recorded input hash, so no drift in this cited artifact.
- **Recommendations-only** — `:237-238` (U6: "whether mado accepts any §8 recommendation is a decision of mado's lane; this note records the findings unabsorbed") and `:240-260` (§8 header "recommendations only, no patch" plus recommendations 1-7). Resolves.
- **Harness pinned per run** — `:17-23` is incident I1: the tool moved mid-round, re-pin `b56c6e57…2bcb` at 17:46:15Z, "Every number in this note is tied to `597e1419…`". Resolves, including the `b56c6e57…` fragment.
- **Sensitivity, not truth** — cited `:229-230`: line 229 carries the substance ("against the *real* config planes are right; only what its suite can detect"), line 230 opens U3, and the U2 label is on `:228`. Substantively resolves (the round-27 read had called the one-line start a minor gap); not reported as a finding.
- **sha pair** — `:57-59` holds `MUTATE_RESTORE: OK (target-sha256 before=d7edaab4…d0e13 after=d7edaab4…d0e13 pristine-sha256=…)`. Resolves.
- No tables in this section, so no stale table cell applies. I found no sentence that contradicts another within the section: the hermetic-only bullet disclaims substrate drift while the harness bullet records harness drift (different objects), and "the tool emits no tree-clean check" agrees with the report shape at `:904-905`, not with a run receipt.

## Sweep and method

- Read every cited anchor at C0, never from the working tree: `git show 59c3810:<path>` for `SKILL.md`, `corpus/knowledge/mutation-case-mado-verify.md`, `corpus/knowledge/fleet-suite-census.md`, `corpus/knowledge/arm-class-matrix.md`, `tools/mutate-and-run.sh`, `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/waves/round-27/w1/Read09.md`.
- `sha256sum` of the four cited non-SKILL files at C0 (values above) to detect input drift against the ledger's recorded hashes.
- `grep -n "SKILL.md:"` over the section bytes: only `335` and `808-809`.
- Cross-revision proof of the 11-line shift: `git show 2227d83:SKILL.md` lines 333-337 and 805-812 versus `git show 59c3810:SKILL.md` lines 335/346 and 808-809/819-820.
- No synthetic receipt directory was needed: this is a read item, not an attack item, and no fixture was written.
- No tool was installed or upgraded. No lane file, counter, contract, freeze, ledger or wave spec was modified. Scratch `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read03` (created, empty) and the one `mktemp -d` used only to load the frozen `measure.py` were both removed at exit.
- Residual risk: `mutation-case-mado-verify.md` content is verified at C0 (hash unchanged from the ledger), but the mado run's own receipt is a record; I did not run its gate. The section contains no instruction to run, so nothing was executed beyond reading and hashing.

COLDREAD T54W1Read03: gap-blocking (2 findings)
