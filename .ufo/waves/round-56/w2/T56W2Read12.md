# T56W2Read12 — cold-read re-read at C0

Seat: `T56W2Read12` (wave 2, cold-read re-read 12/18)
Heading: `### Round-15 gate/probe registry`
Candidate (`cand`): `c0137451f5b7f22d65f748fc69f1b181f55e1378`
Section at C0: lines **1719–1749** (31 lines), `section_sha256` = `78edbb693cdddcab61902811985918087529c444d3fb01da7bcaf4a674daf4ea`
Verdict: **verified-record** (no findings)

Section hash computed with the FROZEN round-18 `sectionize` (never reimplemented),
loaded by `importlib` from
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py`,
whose blob at C0 hashes to `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`
(the round-56 validator's `R18_PIN`; reproduced independently through
`.ufo/waves/round-56/validate-readers.py::load_sectionize` + `group_sections` → same
`sha256`, unique heading, one section).

Receipts: `.ufo/waves/round-56/w2/T56W2Read12-receipts/` (11 transcripts).

## Commands run

Setup (scratch, `/fast/scratch/hyaku/tameshi-r56/T56W2Read12`):

```
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin clone && git -C clone checkout --detach c0137451f5b7f22d65f748fc69f1b181f55e1378
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md
git -C clone archive 28aeef4 | tar -x -C frozen28
```

All gate commands were run with cwd = the clone at C0 (`clone/`), and the frozen
replay with cwd = the extracted `frozen28/` tree.

```
python3 tools/context-capture.py --check
python3 tools/context-capture.py --selftest
python3 tools/context-capture.py --check --receipt .ufo/evidence/round-15/frozen/context-clean/receipt.json --expected .ufo/evidence/round-15/frozen/context-clean/expected.json
python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-missing-env.json --expected .ufo/evidence/round-15/frozen/context-missing-env/expected.json
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json
python3 tools/evidence-disposition.py --selftest
sha256sum .ufo/evidence/round-14/context-receipt.json .ufo/evidence/round-14/context-missing-env.json
strace -f -qq -e trace=openat,open,execve -o strace-check.txt python3 tools/context-capture.py --check
```

Exit-class probes (same cwd): `python3 tools/context-capture.py` (no args),
`python3 tools/context-capture.py --help`, `python3 tools/context-capture.py --selftest extra`,
`python3 tools/evidence-disposition.py` (no args), `python3 tools/evidence-disposition.py --help`,
`python3 tools/evidence-disposition.py --selftest extra`, a tampered receipt copy, a missing
receipt, a wrong id/exit expected pin, a symlinked receipt, `--root /nonexistent-root-xyz`,
and a malformed `--dispositions` file.

## What the section claims, and what the tree at C0 does

Row 1 — *retained invocation-context gate* (`python3 tools/context-capture.py --check`):

| Claim | Observed at C0 | Receipt |
|---|---|---|
| `--check` on the frozen round-14 clean receipt → 0 clean, `context_consistent` | `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b8… exit=0 findings=0)`, `EXIT=0` | `02` |
| `--check --receipt FILE --expected FILE` for a caller-pinned retained receipt | clean pinned pair → `EXIT=0`; negative pinned pair → `EXIT=1`, `id=missing_injected_environment` | `04` |
| 0 clean / 1 failed stable finding ID / 2 and 64 could-not-evaluate (`snapshot_tampered`; 64 `usage_error`) | tampered receipt → `id=snapshot_tampered` `EXIT=2`; missing receipt → `id=receipt_missing` `EXIT=2`; wrong pin → `id=expected_verdict_mismatch` `EXIT=1`; no args → `EXIT=64` | `10` |
| self-test `python3 tools/context-capture.py --selftest` | `SELFTEST: PASS (49/49)`, `EXIT=0`; `--selftest extra` → `EXIT=64` | `03`, `10` |
| pinned clean receipt sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` | `sha256sum` matches byte for byte | `09` |
| negative fixture `context-missing-env.json` sha256 `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` | matches `.ufo/evidence/round-14/context-missing-env.json` | `09` |
| expected-pin schema `tameshi-context-expected-v1` (`receipt_sha256`/`id`/`exit`) | present in `tools/context-capture.py` and in the frozen `expected.json` files (four keys: `schema`, `receipt_sha256`, `id`, `exit`) | — |
| write scope: check reads the receipt/expected bytes and its own source, writes nothing, never opens recorded root paths, never executes stored argv | `strace` shows only `tools/context-capture.py` and `.ufo/evidence/round-14/context-receipt.json` opened in the lane; the only `execve` is `/usr/bin/python3` (the receipt's recorded `invocation.argv` is not run); whole-tree diff before/after check+selftest+disposition = `NO TREE CHANGES` | `11` |

Row 2 — *effective expectation disposition*:

| Claim | Observed at C0 | Receipt |
|---|---|---|
| `--root . --dispositions .ufo/evidence/round-14/dispositions.json --json` → 2 `expected_input_digest_mismatch` | `status=could_not_evaluate`, `exit=2`, `id=expected_input_digest_mismatch` | `05` |
| live entry `--dispositions .ufo/evidence/round-18/dispositions.json` → 0 | `status=clean`, `exit=0`, counts `{effective 11, expected_checks 12, passed 11, failed 0, superseded 1}` | `06` |
| "round 17's now 2" | `--dispositions .ufo/evidence/round-17/dispositions.json` → `exit=2`, `id=expected_input_digest_mismatch` | `06` |
| frozen replay: cwd = extracted `git archive 28aeef4` → 0 | extracted tree, cwd=`frozen28`: `status=clean`, `exit=0` | `08` |
| self-test `python3 tools/evidence-disposition.py --selftest` | `SELFTEST: PASS (66/66)`, `EXIT=0`; `--selftest extra` → `EXIT=64` | `07`, `10` |
| historical expected pins 13 original inputs | `.ufo/evidence/round-13/expected.json` → `inputs 13` | `09` |
| write scope: normal mode read-only lane evidence, stdout only; selftest isolated temporary fixtures | whole-tree diff after the disposition commands = `NO TREE CHANGES`; `--json` emitted on stdout only | `11` |

Prose paragraphs:

- *"a clean check replays recorded predicates and pinned digest binding, never a re-execution of
  stored argv and never a fresh measurement"* — confirmed by the `strace` transcript: the only
  `execve` is the interpreter itself (`11`).
- *"the frozen retained replay is the committed-input evidence of the Gate standard's 'Two
  evidences'"* — the pointer resolves: `/home/vgpnk/Projects/shokunin/PROTOCOL.md` §Gate standard
  carries the "Two evidences" clause at lines 390–397, and the committed frozen replay lives at
  `.ufo/evidence/round-15/frozen/{context-clean,context-missing-env,mapping-suffix}/`.
- *"Could-not-evaluate takes precedence over a mismatched expected verdict"* — confirmed: the
  tampered-receipt and missing-receipt runs exit 2 with the expected-verdict disagreement reported
  only as a secondary finding (`10`).
- *"A clean result with a wrong id/exit pin becomes failed/exit1"* — confirmed: `EXIT=1`,
  `id=expected_verdict_mismatch` (`10`).
- *"Help exits0 only as a non-verdict informational mode"* — confirmed: `--help` → `EXIT=0` for
  both tools (`10`).
- *"Paths can follow filesystem symlinks"* — confirmed: a symlinked receipt is read and bound by
  digest (`10`).
- *the disposition selftest names an unusable scratch root / unreadable input, never a traceback
  (round 54)* — confirmed: `--root /nonexistent-root-xyz` → `exit=2`, `id=root_unavailable`,
  "lane root is not a directory"; a malformed `--dispositions` file → `exit=2`,
  `id=dispositions_json_invalid`, "malformed JSON: …"; no traceback in either output (`10`).

Cross-section consistency: the round-17 registry section
(`### Round-17 gate/probe registry — re-pin and monitor`) states the same live entry
(round-18 manifest) and the same "the round-17 manifest now exits 2"; the round-51 registry row
for "context receipt replay" states `SELFTEST: PASS (49/49)` and the round-51 row for "evidence
disposition accounting" states `66/66` — both match the observed selftests. No contradiction
found.

## Findings

None. No statement in the section is false of the tree at C0 and no command the section names
fails.

## Notes (improvements / stale-but-true / style — not findings)

1. **Cause wording is imprecise but the exit class is right.** The row-2 parenthetical "since
   round 16 this command returns 2 `expected_input_digest_mismatch` at `--root .` because the
   runner input moved" is true as to the outcome (exit 2, `expected_input_digest_mismatch`) but
   the tool's *first named* mismatch at C0 is `tools/bash-witness-study.py`
   (observed `f2bb50c77a6b…` vs historical pin `49e9e5e20b73…`), not the runner
   `tools/mutate-and-run.sh`; that runner and `tools/pin-disposition.py` have drifted from their
   round-13 historical pins as well (`977de470…` vs `75ed934d…`, `c917bc41…` vs `29725397…`),
   but the tool reports only the first. Suggest the next revision say "because the recorded
   historical inputs moved (first reported: `tools/bash-witness-study.py`)". (Same minor wording
   gap was already recorded by round-18 seat CR42; see
   `.ufo/waves/round-18/w3/CR42.md`.)
2. **Historical case count.** "the six recorded cases at this write (seven since round 16)" is a
   snapshot of the round-15 write; `tools/registry.json` carries 57 rows at C0, so the number must
   not be read as a live total. Unchanged and correctly time-scoped.
3. **Un-pathed fixture name.** Row 1 names the negative fixture as `context-missing-env.json`
   without its path; the file is `.ufo/evidence/round-14/context-missing-env.json` (the path is
   given in the preceding section at `SKILL.md:1691-1694`). A reader holding only this section
   has to search for it.
4. **"before counterpart"** in row 2's pinned values resolves unambiguously to
   `.ufo/evidence/round-14/dispositions-before.json` (present at C0); naming the file would
   remove the ambiguity.
5. **Frozen replay recipe.** The "cwd = extracted `git archive 28aeef4` → 0" replay needs the
   lane tree extracted from that commit and `--root .` relative to it; both are stated, but the
   7-hex prefix is unique only in this repo — a future reader on a shallow clone may need the
   full SHA.
6. **Factual check of the round-18 errata.** The round-17 section says this section "grew from
   30 to 31 lines"; at C0 it is 31 lines (1719–1749) ✓.

## Cross-check outside this section (for the L1, not a finding of this seat)

The assignment's census expectation says "141 rows after this round's one new row". The tree
says otherwise: `corpus/SOURCES.md` holds **140** rows (max `S280`) at base `981c5e8b` and at the
freeze `c3e2ca9f`, and **142** rows (max `S282`) at C0 `c013745` — C0 added two rows
(`S281`, `S282`), not one. The requirement itself still holds:

```
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

Only `W01`/`W04` warnings are emitted (no `E`-codes); the 142 ids are unique. The "141" figure in
the assignment text is stale with respect to the C0 commit, not a census failure.

## Tools

No tool was installed or upgraded for this seat. The host already provided `python3` (3.14),
`git`, `strace` and `tar`; all were used as-is.
