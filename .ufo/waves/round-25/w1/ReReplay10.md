# R23-REATTACK Replay10 — fresh falsification of registry row `evidence-disposition-round18`

Role: reviewer re-attack of the round-23 wave-2 seat that died before reporting. Audited ONLY the row
`evidence-disposition-round18` (requirements.json index 9; the sibling `-before` row is out of scope).
Lane state at audit time: worktree HEAD `5b69fb23a9c4a27ea13fabf966d131be169846a6`, which contains
contract revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df` as an ancestor; worktree files for every
file cited below are byte-identical to `c9ff09f` (verified with `git diff --stat c9ff09f HEAD` empty for
`tools/command-binding.py` and `tools/registry.json`, and `git status --porcelain` empty for the three tools).

Artifacts audited (all frozen, read-only):
- `.ufo/evidence/round-23/requirements.json:140-160` (row 9 `evidence-disposition-round18`)
- `.ufo/evidence/round-23/replay/bundle.json:140` (requirement) and `:745` (receipt)
- `.ufo/evidence/round-23/replay/observations.json:451` (per-row observation, full streams)
- `.ufo/evidence/round-23/replay/expected.json` (bundle digest pin)
- `tools/command-binding.py` (220 lines, read in full), `tools/evidence-disposition.py` (baseline blob at
  `28cae179…` = worktree, byte-identical), `tools/registry.json:252` (worktree == `c9ff09f`).

## 1. Static exact binding of the frozen row: CONFIRMED (no false acceptance in the frozen evidence)

Every pin checks out against observed bytes, not inferred values:

1. **Digest pin.** `sha256(replay/bundle.json)` = `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9`
   = `bundle_sha256` in `replay/expected.json`. `command-binding.py --check` on /tmp copies returned
   `{"exit": 0, "finding_ids": [], "bundle_sha256": "3d6c99b7…"}`. Duplicate JSON keys and nonfinite
   literals are rejected at decode (`command-binding.py:40-44`), so the pin covers the bytes as parsed.
2. **Requirement ↔ registry ↔ bundle argv/expect equality.** The bundle requirement (bundle.json:140) is
   field-identical to the frozen registry row at both `28cae179…` and `c9ff09f` (`kind: gate`, `status:
   active`, same `argv`, same three `stdout_contains` tokens). Receipt `argv` equals requirement `argv`
   by exact list equality (no shell normalization anywhere; `command-binding.py:109`).
3. **Invocation metadata, actually present.** Receipt (bundle.json:745): cwd
   `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin` (canonical absolute, equals bundle `cwd`),
   revision `496d212bc46789cdf8cafab72978bdb7f4182963` (equals bundle revision), exit `0`. The
   requirements pin `registry_sha256 ebd2e69a…`; `git show 28cae179…:tools/registry.json | sha256sum`
   and the same at `496d212b…` both give `ebd2e69a…` — the replay checkout carried the pinned registry.
4. **Full output, not tails.** Receipt stdout is 6904 chars and parses as a complete JSON document
   (`status: clean`, `findings: []`, 12 rows, counts `effective: 11 / superseded: 1 / passed: 11 /
   expected_checks: 12` — internally consistent, 11+1=12 rows). observations.json:451 retains the SAME
   full stdout byte-for-byte (6904 == 6904), same stderr (empty), plus `stdout_tail` of 4096 chars that
   is a true suffix of the full stream — tails are retained *in addition to*, not instead of, the full
   capture (capture field: "complete decoded stdout/stderr; original runner tails retained separately").
   Row measurement interval `2026-10-21T14:42:26.55→.65` sits inside the replay interval.
5. **Cross-artifact runner pin.** observations `runner_sha256 cba16646…` = `sha256(tools/registry-check.py
   @ 496d212b…)` (replay.py:78 hashes the clone's runner); the receipt's self-declared `tool_sha256
   39ee5c5e…` = `sha256(tools/evidence-disposition.py @ 496d212b…)` — the tool that self-identified in
   the output is the tool at the pinned revision.
6. **Expect tokens derive from real serialization, not retrofill.** Baseline
   `tools/evidence-disposition.py:1452` emits `json.dumps(payload, indent=2, sort_keys=True)`, which
   produces exactly the `"effective": 11` spacing the tokens expect; the receipt's 12 row names equal the
   12 `rows` in the pinned `.ufo/evidence/round-18/dispositions.json` (sha `9caa2f76…` at every checked
   revision: `28cae179`, `496d212b`, `c9ff09f`, worktree) in the same order. Provenance anchor
   `SKILL.md@58e5d53:1923-1932` exists and contains the round-18 gate table naming
   `tools/evidence-disposition.py` — the citation is real, not retrofitted.
7. **Honest scope statement (present vs inferred).** Present: retained declarations, full captured
   streams, digest pins. NOT present and not claimed: any proof the processes actually ran (no syscall
   trace, no env capture, outer driver `replay.py` is referenced by path in observations argv but not
   itself digest-pinned inside the artifacts). The tool's own docstring (`command-binding.py:9-11`)
   declares exactly this: it "validates retained declarations, not their producer authenticity". I
   reject producer authentication as a claim: nothing here establishes execution, and I did not run the
   registry command to compare.

## 2. FINDING — field-level false acceptance in the row's stdout expect (concrete counterexample, executed)

`tools/command-binding.py:111` checks `any(token not in receipt['stdout'] …)` — plain substring
containment. The row's tokens are meant to pin JSON field *values* (`"effective": 11`, `"superseded": 1`),
but a substring token also matches a longer number sharing the prefix:

- `"effective": 11` ⊂ `"effective": 110` (verified: `'"effective": 11' in '"effective": 110'` → True)
- `"superseded": 1` ⊂ `"superseded": 12`

Counterexample (run in /tmp/rereplay10, no repo writes): took the frozen bundle, replaced
`"effective": 11,` with `"effective": 110,` in the round-18 receipt's stdout (one byte-class edit,
argv/cwd/revision/exit untouched), re-pinned a fresh expected.json to the new bytes, and ran
`command-binding.py`:

```
$ python3 tools/command-binding.py --bundle forgeA-effective110-bundle.json \
      --expected forgeA-effective110-expected.json --json
{"bundle_sha256": "2b1ac45e…", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}
```

Exit 0, no findings: a receipt (or a drifted tool emitting 110 effective rows) satisfies a gate whose
entire purpose, per its `kind: "gate"` and token set, is to fail unless exactly 11 effective / 1
superseded. That is a field-level false acceptance. The supplemental fixture sets
(`.ufo/evidence/round-23/extra-cases.json`: 19 cases; `round-24/extra-cases.json`: 6 cases) cover
argv permutations, stderr non-supply, surrounding text, all-tokens-required and token padding — none
covers numeric-prefix collision, so `selftest` passes while this hole stays open.

Two bounded notes for fairness: (a) contradictory-content acceptance is *declared* design — fixture
`stdout-surround-clean` expects exit 0 for `prefix\nPASS\nsuffix`, so my second forge (prepending
`"status": "failed"` while keeping `"status": "clean"`, also exit 0) is within documented semantics, not
a defect claim; (b) the defect is in enforcement strength of the expect, not in the round-23 evidence
itself — the frozen receipt is internally consistent and every pin in §1 verifies.

## 3. Concrete adversarial delta

An adversary who can alter the retained receipt bytes of any future replay (or a code change to
`evidence-disposition.py` that inflates the counts — the file is not hash-pinned by the *binding*, only
self-reported via `tool_sha256`) gets the gate to accept `effective: 110, superseded: 12` with the
unchanged three-token expect, because token matching cannot distinguish 11 from 110. The mutation
survives the full binding including digest pinning, since the caller-owned expected file re-pins
whatever bundle bytes exist — and within that documented trust model the token check is the only thing
standing between a drifted count and a passing gate, and it does not stand.

## 4. Does the finding still apply at c9ff09f? YES

- `tools/registry.json` at `c9ff09f`/worktree (sha `a8f255f1…`) differs from the round-23 pin
  (`ebd2e69a…`) only by 74 ADDED lines: six command-binding rows (r23 versions now `superseded`, r24
  `-pinned` replacements) and `registry-replay-selftest`. The audited row
  (`tools/registry.json:252`) is byte-identical, `status: active`, NOT superseded.
- `tools/command-binding.py`: byte-identical at `28cae179…`, `c9ff09f`, and worktree (`git diff` empty).
- `tools/evidence-disposition.py`: identical `28cae179…` → worktree.
- `.ufo/evidence/round-18/dispositions.json`: sha `9caa2f76…` at all revisions checked.
So the substring false acceptance, and the row it weakens, are both live at the contract revision.

## 5. Installations

None. No tools were installed or upgraded (existing python3/git sufficed).

## 6. Residual risk and verification gaps

- The original command was not executed (original item forbids running the registry command; superseded
  only for the write-ban), so "the tool emits these counts for the pinned dispositions file today" is
  inferred from the retained full output plus byte-identical inputs, not from a fresh run.
- `replay.py` (outer driver) is not digest-pinned inside the artifacts; its worktree sha is
  `adb41716…`. Everything it recorded internally is pinned/cross-checked; the driver itself is not.
- I did not audit the `-before` sibling row (out of scope per item).

R23-REATTACK Replay10: FINDING
