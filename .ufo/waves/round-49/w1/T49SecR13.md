# T49SecR13 — C1 section critic: `## Pin disposition and provenance correction`

Base: `8ca67421111fa354b47b803358391d0b07fc6db9`. Deliverable: `T49SecR13.findings.json`
(15 findings: 2 false, 1 unverifiable, 12 true). Receipts: `T49SecR13.pin-probe.txt`,
`T49SecR13.witness-check.txt`, `T49SecR13.selftests.txt`, `T49SecR13.recorded-cases.txt`,
`T49SecR13.section-at-base.txt` (same directory).

## Scope

The section is SKILL.md lines 1517-1547 at base — confirmed against the counter's own
sectionizer, not assumed:

```
python3 -c "... round-18/measure.py sectionize ..." (scratch clone at base)
1517 1547 '## Pin disposition and provenance correction — round 13'
1548 1562 '### Round-13 gate/probe registry'
```

So the `###` registry block and the closing paragraphs (1548-1562) are a *different*
section. I audited 1517-1547 line by line, and reported one high-value stale count from
1555 with an explicit out-of-range note (F2) because no section-critic seat covers 1548-1562
in `spec-w1.json`.

All work was read-only on the lane: `git show`, `grep`, `sha256sum`, `git ls-tree`, and
tool runs confined to a scratch clone at base (`git clone --shared`, verified toplevel) and
an empty scratch `--root`. No lane tool was run against the fleet root; nothing in
`~/.local/state` was read; no panel or control stdout was opened. Tool installs/upgrades:
none.

## False statements

### F1 — SKILL.md:1530 (table row 5) — false: the explicit kind is not in the summary

> `| Frozen summary kind is null but its top-level declaration is explicit | Retain original bytes and add checked normalized companion | ... |`

The clause reads as a property of "the frozen summary", and of that object it is false.

```
python3 -c "import json;print(json.load(open('.ufo/evidence/round-12/BashWitness/summary.json'))['declaration']['kind'])"
None
python3 -c "import json;print(json.load(open('.ufo/evidence/round-12/BashWitness/declaration.json'))['kind'])"
declared-witness mapping (not a blind preregistration)
```

The companion itself records the split — `.ufo/evidence/round-13/witness-metadata.json`
`declaration.kind_source` = `declaration.json#/kind (explicit frozen top-level field)`,
and `original_nested` = `{source: "summary.json#/declaration/kind", value: null,
state: "historical-null-preserved"}`. A cold reader who follows the cell to
`summary.json#/declaration` finds `kind: null`; the explicit field lives in the separate
frozen `declaration.json`. Smallest fix: `its top-level declaration is explicit` →
`the frozen declaration's top-level kind is explicit`. No path/`file:N`/`S###` token is
added, so the pointer set stays at 9.

### F2 — SKILL.md:1555 (adjacent `###` block, out of this seat's range) — false at base: "six recorded cases"

> `No registry row changes rank, SHONEN authority, or the six recorded cases.`

Nine recorded cases at base, not six:

```
git show 8ca6742...:tools/mutate-and-run.sh | grep -cE '^#   (js|bash)-'      -> 9
git show 8ca6742...:tools/mutate-and-run.sh | sed -n '83p'
# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine) — the fleet's
#   legs listed: js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify,
#                bash-checklist-run, js-claims-check, js-round-gate, js-sources-check, js-cite-check
python3 .ufo/evidence/round-13/measure.py --rev 546b371a...   -> recorded_cases 6   (round-13 baseline)
.ufo/evidence/round-13/before-final.json                     -> {"recorded_cases": 6, "unique_recorded_gates": 6}
contract.json axes_at_base.depth                             -> "9 (command D recorded_cases=9)"
```

Six is true of round 13 only; the sentence carries no date qualifier, so at base it asserts
a lane count the lane no longer holds. Fix: `or the six recorded cases.` → `or the six cases
recorded at round 13.` (the longer phrase is unique in SKILL.md; the plain phrase recurs at
SKILL.md:1689 in the round-14 section, which is T49SecR14's range — flag for that seat).

## Unverifiable statement

### U1 — SKILL.md:1534 (recipe step 1) — "the source-backed scope" has no referent

> `1. Read the source-backed scope and `

The probe emits no `scope` element. Scratch run at base:

```
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root "$S"
EXIT=0
keys: schema tool tool_sha256 status observed_at manifest root result_reuse
      result_reuse_reason not_compared counts legs
counts: {'legs': 6, 'unchanged': 0, 'changed': 0, 'unavailable': 6}
grep -n 'scope' tools/pin-disposition.py   -> no match (usage text :1-92 never uses the word)
pin-manifest.json keys -> schema derived_from source note legs
```

The ordering half is true — `not_compared` precedes `counts`/`legs` in the document — but
"the source-backed scope" names nothing a reader can open; the nearest existing element is
the manifest's `derived_from`/`source`/`note`. Fix: `Read the source-backed scope and
\`not_compared\` list before the result.` → `Read the manifest's recorded source and the
output's \`not_compared\` list before the rows.` (pointer-neutral).

## True statements (each verified, with the proving command)

| Line | Statement (short) | Verdict | Proof |
|---|---|---|---|
| 1519 | Sources S003 + PIT precision correction S047, historical S041 | true | `git show base:corpus/SOURCES.md` — :14 S003 mined; :50 S041 mined; :56 S047 mined, "supersedes S041"; :57 S048 mined, "supersedes S047" |
| 1520 | `corpus/knowledge/incremental-pin-disposition.md` | true | `git cat-file -e base:corpus/knowledge/incremental-pin-disposition.md` → present (27870 B); its `## 4. Six-leg content disposition vs a fresh re-sweep` licenses the table |
| 1521 | outside routed `round-12-verifier-spotcheck.md`, Routed defects item 3 | true | `git show base:corpus/lessons/round-12-verifier-spotcheck.md` → `## Routed defects and residuals` item 3 orders exactly the nested `declaration.kind=null` disclosure this section performs |
| 1522 | runtime receipts in `.ufo/evidence/round-13/` | true | `git ls-tree -r base -- .ufo/evidence/round-13/` → 16 committed receipts; `pin-dispositions.json` carries `observed_at`, counts `{unchanged:3, changed:3, unavailable:0}` |
| 1526 | bytes equal worktree → `unchanged`; limits unmeasured | true | `tools/pin-disposition.py:67-73` status semantics; selftest `unchanged`/`changed-head` PASS; `NOT_COMPARED` in the receipt has exactly the listed limits |
| 1527 | verified pin differs → `changed` | true | tool doc :70-71; selftest `changed-head PASS`, `pinned-blob-mismatch PASS`; round-13 live receipt shows 3 changed rows |
| 1528 | unevaluable repo/commit/path/pin → `unavailable` + reason; never borrow fleet repo | true | tool :67-73 and `repo_identity` :245-250 (toplevel equality); selftest `missing-repo`, `missing-pinned-blob`, `missing-pinned-commit`, `worktree-outside-repo`, `worktree-symlink`, `repo-symlink` PASS; scratch probe with empty root returned six `unavailable`/`repo_missing`, exit 0 |
| 1529 | all three identities agree → keep `result_reuse=not_established` | true | `tools/pin-disposition.py:118` `RESULT_REUSE = "not_established"`, :55; every row carries pinned/head/worktree; probe still printed `not_established` with all legs unavailable |
| 1535 | step-2 command; only hashes/git metadata; keep branch tips; executes no sibling gate | true | same command exit 0 in scratch (`T49SecR13.pin-probe.txt`); only subprocess sites are `git_run` (:224-242, read-only plumbing per :82-92) and selftest fixtures (:770, :931); `head.branch`/`head.commit` in each row; selftest `detached-head-uses-branch-tip PASS (14 literal checks)` |
| 1538 | step-3 command; digest-anchored check | true | `witness-metadata --check` → `metadata_consistent reason=ok exit=0 ... inputs=summary,declaration,declared,rerun_summary`; old-null → `metadata_inconsistent reason=normalized_kind_null exit=1`; literal pins at `tools/witness-metadata.py:76,81,86,116`; tool sha equals the round-13 pin |
| 1540 | null fields retained; companion scopes canonical only; producer bug fixed separately with a selftest asserting the top-level kind | true | both frozen summaries' nulls = `['/declaration/kind','/environment/the_janitor_on_path']`; `git log` on `summary.json` → only `9df9212`; companion `covered_null_observations` vs `uncovered_null_observations` (`named-residual-uncorrected`); `git show 4acc607:tools/bash-witness-study.py \| sha256sum` = `49e9e5e2…` (round-13 pin) vs `9df9212:` = `249d9dcd…` (sha in the frozen summary) vs live `60575e62…`; `bash-witness-study.py selftest` at base → `check summary preserves top-level exposed declaration kind ok`, `WITNESS_SELFTEST: 51/51 pass` |
| 1545 | do not rerun a sibling gate; closure verifies committed receipts and their revision | true | `round-13/measure.py:2` "Count committed round-13 observations, never execute a target or gate"; `verification.json` hashes pinned inputs, `verification-verdict.json` `input_digests_match: true`; `before.json`/`after-committed.json` both carry `revision: 546b371a…` |

Advisories attached to true rows (no fix proposed):

- 1519: naming S048 would add a 10th distinct S-id pointer to a C1 target section (base 9)
  and therefore a 10th read row; the supersession is already disclosed at SKILL.md:1558.
- 1520: file name carries no section anchor (calibration only); optional fix supplied.
- 1526: the Observation column states byte equality only; the digest-verification
  precondition is supplied by row 3, so the table is consistent when read whole.
- 1535: "hashes and git metadata" understates the lstat checks (regular file, no symlink,
  containment) but claims nothing about reuse.
- 1545: `verification.json` has no `revision` field of its own; "their measured revision"
  holds because the hashed receipts name it.
- 1522: the cited directory's counter no longer runs at base —
  `python3 .ufo/evidence/round-13/measure.py --rev 8ca6742…` → EXIT=1, `IndexError` at
  `measure.py:43`, because `corpus/SOURCES.md:468` splits into a cell with an S-id and
  fewer than 5 cells. Historical receipt, not a claim of this section, but a reader
  re-running the cited receipt should know.

## Adjacent section (`### Round-13 gate/probe registry`, 1548-1562) — observations only

Not this seat's deliverable; recorded so the L1 can route them:

- 1552 row map `0 observations…; 2 invalid input/could-not-evaluate; selftest 1 failed`
  is true but incomplete: `--selftest` also returns 0 on pass (observed
  `SELFTEST: PASS (19/19)`, exit 0) and 2 on `SELFTEST: COULD_NOT_EVALUATE`
  (`tools/pin-disposition.py:1320-1330`).
- 1552 pinned selftest label: round-13 `expected.json` pins `SELFTEST: PASS (18/18)`, live
  at base prints `(19/19)` — the tool changed after round 13 (pin
  `297253971dab…`, live `331529eadafe…`), so the recipe's step-2 tool is not the
  round-13 byte-identical one. Not a false statement (the row says "literal selftest
  labels in tool"), but worth a dated-reading note.
- 1553 is accurate: `metadata_consistent/clean` 0, `metadata_inconsistent` 1,
  `input_unavailable`/`snapshot_tampered`/usage 2 — all exercised by the 39-case selftest
  and by my two `--check` runs.
- 1558-1561 S048-supersession paragraph is true (S048's support cell: "supersedes S047 —
  item 4 is prioritisation rather than a reuse skip; no claim here resolves its pronoun to
  test versus mutation").

## Constraints for the integrator

- The C1 extractor (`c1/measure.py`) counts, per target section: every `file:N` occurrence,
  every distinct `FILE_RE` path token, and every distinct `S\d{3,}` id. `FLOORS` is applied
  as `counts[h] < FLOORS[h]` (a floor, not equality), but **every extracted pointer needs a
  unique read row or it lands in `unresolved`/`unverified`**. All four proposed fixes were
  checked to add zero pointer tokens (script in this report's run; knowledge path token
  already exists).
- Section `sha256` changes with any edit; the L1 re-keys, so that is expected.
- Do not rename the heading and do not delete any `file:N` pointer (none of my fixes does).

## Summary

Two false statements in range-adjacent prose, one unverifiable and twelve true:
F1 SKILL.md:1530 attributes the explicit top-level `kind` to the frozen summary; it is
null there and explicit only in `declaration.json`. F2 SKILL.md:1555 (adjacent `###`
block) says "six recorded cases"; the lane holds nine at base (`r26 nine`).
U1 SKILL.md:1534's "source-backed scope" names nothing the probe emits.
The rest of the section is accurate: both recipe commands reproduce their claimed results
at base, the null-field and companion-scope claims are exact, the producer repair and its
regression assertion are real, and `result_reuse=not_established` is unconditional.
Four pointer-neutral fixes supplied; none adds a `file:N` or `S###` token, so the 9-pointer
C1 set and its read rows are untouched. Tool installs: none.
