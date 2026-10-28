# T56W2Read05 — cold-read re-read 5/18 (round 56, wave 2)

Heading: `## Pin disposition and provenance correction — round 13`
Candidate (content commit C0): `c0137451f5b7f22d65f748fc69f1b181f55e1378`
Section sha256 (frozen round-18 sectionize, computed at C0): `1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31`
Section extent at C0: lines 1559–1589 of `SKILL.md`.
Verdict: **verified-record** (no false statements; no failing commands).

Every command below was run in a scratch clone of the lane at C0
(`git clone --shared` then `git -C <clone> checkout --detach c0137451…`;
`git rev-parse --show-toplevel` printed the scratch clone path). Receipts are in
`.ufo/waves/round-56/w2/T56W2Read05-receipts/`. No lane file was edited; the
clone's `git status --porcelain` returned zero lines after every run.

## How the sha256 was computed (frozen sectionize, never reimplemented)

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md
```

loaded into `.ufo/evidence/round-18/measure.py` via `importlib`
(`m.sectionize(raw)`); that module's blob sha256 is
`7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`, identical at
base and at the round-56 freeze, and identical whether loaded from the worktree or
from the REV blob. Result: `1559 1589 1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31`.

## Commands run, and their outputs

### 1. The section's own probe (recipe step 2)

```
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin
```

exit 0, stderr empty. Receipt `01-pin-disposition-C0.json`.
`status=ok`, `counts={legs:6, unchanged:1, changed:5, unavailable:0}`,
`result_reuse=not_established`, `not_compared` present with 8 entries
(`mode/exec-bit`, `runner version and embedded defect specs`, `suite command and
test harness`, `interpreter and toolchain versions`, `environment variables`,
`dependency versions`, `fixture and companion files`, `timeouts`).

Per leg, all six `pinned.status=verified` and `result_reuse=not_established`,
each with `head.branch=master`, a branch-tip commit, and
`head_differs_from_branch=false`:

| leg | content_status | pinned | head branch | head commit | worktree path |
|---|---|---|---|---|---|
| js-kimi-census | changed | verified | master | 14057f3e3899 | kumitate-shokunin/scripts/kimi-census.mjs |
| bash-surface-census | changed | verified | master | 69b61db46be4 | kagi-shokunin/corpus/surface-census.sh |
| bash-tsukuroi-census | changed | verified | master | 39e694934cf6 | tsukuroi-shokunin/tools/tsukuroi-census.sh |
| bash-mado-verify | changed | verified | master | 3b55b6e91e40 | mado-shokunin/tools/mado-verify.sh |
| bash-checklist-run | unchanged | verified | master | 69b61db46be4 | kagi-shokunin/corpus/checklist-run.sh |
| js-claims-check | changed | verified | master | 14057f3e3899 | kumitate-shokunin/scripts/claims-check.mjs |

The stdout carries the sibling branch-tip commits and the `root` /
`manifest` fields the recipe asks a reader to retain, so the reading is dated
and attributable.

### 2. The section's companion gate (recipe step 3)

```
python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json
```

exit 0, stderr empty. Receipt `02-witness-metadata-check.out`:

```
WITNESS_METADATA: metadata_consistent reason=ok exit=0 companion=…/.ufo/evidence/round-13/witness-metadata.json inputs=summary,declaration,declared,rerun_summary
```

### 3. The section's two self-test commands (registry row, run for corroboration)

```
python3 tools/pin-disposition.py --selftest
```

exit 0, `SELFTEST: PASS (19/19)` (receipt `03-pin-disposition-selftest.out`).

```
python3 tools/witness-metadata.py --selftest
```

exit 0, `SELFTEST: PASS 39/39` (receipt `04-witness-metadata-selftest.out`).

```
python3 tools/bash-witness-study.py selftest
```

exit 0, `WITNESS_SELFTEST: 51/51 pass`, `VERDICT: PASS`, including
`check summary preserves top-level exposed declaration kind ok`
(receipt `05-producer-selftest.out`).

### 4. Negative check for the "unavailable" row of the section's table

The probe was re-run against an empty scratch root so the "Repo, commit, path
or pin cannot be evaluated → report `unavailable`, with reason" row could be
exercised rather than assumed:

```
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root <empty scratch dir>
```

exit 0, `counts={legs:6, unchanged:0, changed:0, unavailable:6}`, every leg
`content_status=unavailable`, `worktree.reason=repo_missing`,
`pinned.reason=repo_missing`. No leg was labelled unchanged and the enclosing
repo was not borrowed. Receipt `06-pin-disposition-empty-root.json`.

### 5. Negative check that the companion gate is tamper-evident

A copy of the companion with `frozen_declaration.summary.sha256` set to 64
zeros was checked with the section's own step-3 command: exit 2,

```
WITNESS_METADATA: snapshot_tampered reason=companion_digest_unpinned exit=2
WITNESS_METADATA_DETAIL: summary: companion digest is not the pinned value
```

### 6. Read-only / no-sibling-gate sweep (the recipe's own assertions)

`strace -f -e trace=execve` over the probe: the only binaries executed are
`git` and `python3`; a census of git subcommands over 720 git execve calls
gives `cat-file` 564, `rev-parse` 377, `symbolic-ref` 210 — no `status`,
`diff`, `hash-object`, `add`, `commit` or `write-tree`. Receipts
`07-pin-disposition-execve.strace`, `08-pin-disposition-openat.strace`.
An `openat` sweep of the same run shows the only writable opens are
`/dev/null` (git's stdin redirect); the probe writes nothing. The
`witness-metadata --check` run likewise opens no writable file outside
`/dev/null`.

### 7. Every pointer the section names, resolved at C0

| pointer | resolves at C0 | what it actually is |
|---|---|---|
| `corpus/knowledge/incremental-pin-disposition.md` | yes | the knowledge entry; header carries `source-correction: S048` |
| `corpus/lessons/round-12-verifier-spotcheck.md`, Routed defects item 3 | yes | "Tameshi next round: … Disclose/repair the already named nested `declaration.kind=null` metadata defect only through new evidence without rewriting the frozen declaration." — the defect the section's fifth table row addresses |
| `.ufo/evidence/round-13/` runtime receipts | yes | 16 files incl. `pin-manifest.json`, `pin-dispositions.json`, `witness-metadata.json` |
| `tools/pin-disposition.py:67-71` | yes | docstring restatement of the content-status rule |
| `tools/pin-disposition.py:563-567` | yes | the `pinned["status"] != "verified"` → `unavailable` guard (`worktree.reason = "pin_not_verified"`) |
| `tools/witness-metadata.py` | yes | the gate; `expected.json` appears nowhere in it (the section's registry row's "this gate never reads" claim holds) |

### 8. The section's own claims checked against the tree

- "Recorded target bytes equal the current worktree AND the pin verifies
  against the manifest digest" — the manifest's `expected_sha256` equals the
  blob at the recorded commit for all six legs (`pinned.status=verified`), and
  `content_status` is `unchanged` only when the worktree bytes also equal it.
  True.
- "Report `unchanged` content … Mode, dependencies, environment, runner/spec
  and invocation identity remain unmeasured" — matches the eight
  `not_compared` entries exactly. True.
- "Readable verified pin differs from current bytes → `changed`" — five legs
  report `changed`. True.
- "Repo, commit, path or pin cannot be evaluated → `unavailable`, with
  reason" — exercised in run 4. True.
- "All three content identities agree → keep `result_reuse=not_established`"
  — every row carries `not_established`. True.
- "Frozen summary kind is null but the frozen declaration's top-level kind is
  explicit → retain original bytes and add checked normalized companion" —
  `round-12/BashWitness/summary.json` has `declaration.kind = null` and
  `declaration.json` has top-level
  `kind = "declared-witness mapping (not a blind preregistration)"`; the
  companion carries the identical `kind` and the identical `disclosure`
  (byte-for-byte equal to the declaration's), `blind=false`,
  `prior_exposure=true`, `expected={id: metadata_consistent, exit: 0}`. The
  companion's `scope.covered_null_observations` names the canonical summary
  and `scope.uncovered_null_observations` names the rerun summary as a
  sha256-anchored named residual — i.e. the rerun null is outside the
  companion's normalized scope, as the section says. True.
- "The original round-12 summary and rerun summary retain their historical
  null fields" — both sha256s still match the companion's pins
  (`acc01268…`, `6726421f…`), and both still carry `declaration.kind = null`.
  True.
- "The producer's wrong-nesting bug is fixed separately for future summary
  generation; its regression selftest asserts the exact top-level exposed
  kind" — `tools/bash-witness-study.py:813-818` reads the declaration's
  top-level `kind`, and the producer selftest asserts the summary's
  `declaration.kind` equals the exact non-blind string. True (producer
  selftest run above).
- "It executes no sibling gate" — the execve sweep shows only `git` and
  `python3`. True.
- "Do not rerun a sibling's gate to obtain closure evidence" — complied with:
  no sibling gate was run; the frozen round-12 bytes were read, not re-executed.
- Source IDs S003 / S047 / S041 all exist in `corpus/SOURCES.md` (rows 14,
  56, 50). True.

## Findings

None. No statement in the section is false of the tree at C0, and no command
the section gives a reader fails.

## Notes (improvements, not findings)

1. **Source citation is stale-but-true.** The section names "PIT precision
   correction S047 (historical S041 retained)". Both rows exist and the
   statement is true, but `corpus/SOURCES.md:57` records **S048** as
   superseding S047's object-specific paraphrase, and the knowledge entry
   carries `source-correction: S048`. The S048 clarification does appear in
   `SKILL.md` at line 1601 — inside the neighbouring `### Round-13 gate/probe
   registry` heading, not this one — so a reader of this heading alone
   understates the current PIT source. Naming S048 alongside S047 here would
   close the gap.
2. **The first table row's line pointers stop one hop short.**
   `tools/pin-disposition.py:67-71` is the docstring restatement of the rule
   and `:563-567` is the "pin not verified → unavailable" guard; the actual
   manifest-digest comparison is at `:331-337` and the unchanged/changed
   decision at `:568-573`. The stated rule is true; the pointer does not name
   the comparison itself.
3. **No exit-code expectation is stated for step 2.** The tool's own exit map
   is 0 for observations and 2 for could-not-evaluate (tool docstring
   `:77-80`; registry rows `SKILL.md:1594` and `:2194`). A reader following
   only this heading has nothing to check the stdout against.
4. **Row 4 under-describes the tool.** `result_reuse=not_established` is on
   *every* row, not only on agreeing rows. The row is true as written; the
   operative constraint is its limit cell.
5. **Step 3's gate is tamper-evident but the section gives only the happy
   path.** Tampering one pinned digest turns exit 0 into exit 2 with
   `snapshot_tampered reason=companion_digest_unpinned`. Recording both exit
   codes would make the step checkable by a reader.
6. **The section does not say that the companion's producer sha256 is the
   historical producer**, while the live `tools/bash-witness-study.py` at C0
   hashes `f2bb50c7…` and the companion's own `checked_live` is `false`.
   Stated in the neighbouring registry heading, so this is a placement
   improvement only.

## Deliverables

- `.ufo/waves/round-56/w2/T56W2Read05.json` (this report's machine form)
- `.ufo/waves/round-56/w2/T56W2Read05.md` (this file)
- `.ufo/waves/round-56/w2/T56W2Read05-receipts/` — 10 receipt files

Tool installs/updates: none (no `uv tool` / `npm` / binary install was needed;
Python 3.14.8 and git 2.56.0 from the host were sufficient). `pacman`
transactions were not attempted, per the host-wide pause.
