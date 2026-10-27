# T53W1RevContract — kill-rule review of the frozen round-53 contract

Seat: T53W1RevContract (wave-1 reviewer, judged on calibration).
Reviewed: freeze commit `e62d99711a0dd5d92b83acb96dd53ff22b31cb75` — `.ufo/evidence/round-53/contract.json`, `c1/measure.py`, `c2/measure.py`, `deciding-run.sh`, `freeze.json`, `no-harm.sh`, `control/controls.py`, `control/break-fixtures.py`, `control/controls.{stdout,exit,stderr}`; content commit `C* = a41195dfc13a73958e4c5228ec196b28d03ded03`; base `6db1d220b3…`; floor `ef19d8e1e7…`.
Method: every frozen byte read via `git -C <lane> show e62d9971:…` (git objects, never the working tree); counters re-executed from freeze-extracted bytes into private scratch; no git/jj mutation anywhere; no fixture commits needed (all probes ran read-only against committed revisions).

## VERDICT: KILL-RULE-HOLE

Three concrete holes (F1–F3), one gate-width gap (F4). The do-nothing story is sound (verified independently); the kill rule fails in the opposite direction: **as frozen at e62d9971, no descendant revision can lawfully close green — and if patched naively it can close green over a false predicate sentence.**

---

## F1 — BLOCKER: the frozen kill rule is unsatisfiable (C2 grep arm vs no-harm `tools-scope`)

`c2/measure.py` requires **zero** matches of `dir\s*=\s*["']/tmp` under `tools/` at the measured revision. All nine hits exist already at the **floor** and sit in **seven** files:

```
$ git grep -nE 'dir\s*=\s*["'\'']/tmp' ef19d8e1 -- tools/
  bash-witness-study.py:1, context-capture.py:2, env-diff.py:1,
  evidence-disposition.py:1, pin-disposition.py:1, registry-check.py:2, repeat-control.py:1   (9 hits)
```

Zeroing them (as `C*` does — `git grep … a41195dfc13a -- tools/` → exit 1, zero hits) forces modifications to all seven files: `git diff --name-status ef19d8e1 a41195dfc13a -- tools` shows 9 modified paths (those 7 plus the round-52 pair `registry.json`, `round21-measure.py`).

But the frozen `no-harm.sh` `tools-scope` monitor allowlists only **four** paths:

```
case "$t" in M:tools/registry.json|M:tools/round21-measure.py|M:tools/registry-check.py|M:tools/env-diff.py) ;; *) s=RED;; esac
```

The comment freezes the assumption "the round-53 C2-declared tool edits M:tools/registry-check.py + M:tools/env-diff.py" — written when C2 was a 2-tool claim. The actual C2 surface is 7 tools (the goal text says so; freeze amendment 5 itself concedes "the round's own C2 tool edits" drifted 11 sections). Five patched paths (`bash-witness-study.py`, `context-capture.py`, `evidence-disposition.py`, `pin-disposition.py`, `repeat-control.py`) are outside the allowlist.

Consequence, mechanically: at any candidate passing C2's grep arm, `NOHARM tools-scope […] RED` prints → `grep -q RED` sets `rc=1` **and** the `^NOHARM .* ok$` count is 11 ≠ 12 → `deciding-run.sh` exits 1. Reverting the five tools instead restores their floor `/tmp` hits → C2 grep fails. **No revision descends from the freeze that passes both gates.** The `FROZEN_UNCHANGED` gate guarantees the blocking allowlist bytes at deciding time, so the conflict cannot be dodged from the decide side.

Repair (lawful, precedented): freeze amendment widening the `tools-scope` allowlist to the seven actually-patched tools — an implementation/scope-disclosure change like amendments 3–5, no predicate/target change. Must land **before** the single-shot deciding run.

## F2 — BLOCKER at C*: the frozen C2 counter is RED at the round's own content commit (cr47 arm)

Re-run of the freeze-extracted `c2/measure.py` at `C*`:

```
C2_R53: rev=a41195dfc13a tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)]
        envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=0 docs=ok total=2 C2_R53_PASS=false
PROBLEM cr47-zero-exit
PROBLEM cr47-no-scratch-message
```

Direct probe: `TMPDIR=<nonexistent> python3 tools/registry-check.py --selftest` (bytes at `C*`) → **exit 0, last line `SELFTEST: PASS (51 cases)`**. Mechanism: the fix changed the scratch calls to `dir=tempfile.gettempdir()` (`registry-check.py:766,917` at `C*`); `gettempdir()` silently **falls back to /tmp** when TMPDIR names a missing directory, so the selftest evaluates happily and prints its verdict line. The C2 predicate requires the missing-TMPDIR run to exit non-zero, name scratch creation (could-not-evaluate, round-18 CR47), and print no verdict line. False at `C*`. This is also cannot_see-C2(a)/​(c) materialized: the TMPDIR redirection does **not** isolate the run when TMPDIR is unusable — it silently uses `/tmp`.

Repair: a post-`C*` `tools/registry-check.py` commit adding the refusal. That is compatible with C1 (C1 never reads tool bytes) and with `tools-scope` (`registry-check.py` is allowlisted) — but F1 must still be amended first, and the SKILL.md tools-table cell (F3) will still be stale.

## F3 — MAJOR: C2 docs arm narrower than its predicate sentence — violated at `C*` with no gate noticing

Predicate clause: "**SKILL.md names no /tmp scratch path for either tool**". The counter implements this as four fixed stale patterns (`/tmp/tameshi-f5.json`, `/tmp/tameshi-r21-envdiff`, `mkdir -p /tmp/<lane>-r<round>`, `` Scratch for a sweep: `/tmp/ ``) — amendment 3 narrowed the check "to stale /tmp forms" while declaring "same predicate". At `C*`:

```
a41195dfc13a:SKILL.md:2161: | entry-registry walk | … | selftest and --rev fixture trees via mkdtemp
  under /tmp (hardcoded, TMPDIR ignored), removed afterwards; …
```

That names a `/tmp` scratch path **for registry-check** (one of "either tool") **and** describes the pre-fix behavior, which `C*` superseded (`dir=tempfile.gettempdir()` now honours TMPDIR) — stale and false. The frozen counter prints `docs=ok` at `C*` (observed in the F2 run). A round closing on these receipts would print `C2_R53_PASS=true` under a predicate clause that is false at the measured revision.

Three-way squeeze that makes this hard to repair honestly:
- Fixing SKILL.md:2161 after `C*` changes the section **"### Round-26 gate/probe registry — report interop"** — which is one of the 30 C1-anchored headings in `c1/lost-headings.json` (verified). Every wave-1 reader JSON pinned that section's `section_sha256` at `C*`; a post-`C*` edit breaks the C1 readers arm at the measured revision (30/30 → 29/30 → C1 false), unless a fresh re-read + re-key is done at the new revision.
- Leaving SKILL.md untouched keeps the false sentence under green receipts (this hole).
- Amending the docs clause wording post-data is a predicate change after wave-1 evidence — legal via amendment but exactly what `T53W2CritContract` is primed to flag.

The clean path: tools-only CR47 fix (F2) + freeze amendment that either extends the docs patterns to this cell class (then fix SKILL.md + re-read that one section) or honestly re-scopes the docs clause and routes the stale cell. Either way it must be **declared**, not absorbed.

## F4 — MAJOR: the five break-one controls are pre-registered but never gated, and have not run

`contract.json` pre-registers `CTL_NOTRACE`, `CTL_BADREADER`, `CTL_WRONGREV` (C1) and `CTL_TMP`, `CTL_CR47` (C2); `control/break-fixtures.py` implements them as "phase B … after the re-key has landed, before wave 2". But `deciding-run.sh` gates only `CONTROLS="$E/control/controls.stdout $E/control/controls.exit"` (phase A); no phase-B receipt is required, and at wave 1 **none exists** (`control/` holds only phase-A files; no `after/` yet). As frozen, the round can close with counter break-sensitivity asserted but never evidenced. Wave-2 coverage is partial: `T53W2MutLedger` re-implements wrong_expectations-flip, trace-sha tamper, rekey-dir rename (+ a quote-honesty probe); `T53W2RevC2Counter(e)` attacks read-only TMPDIR; `T53W2RevC1Counter` hand-verifies 3 entries. **Not re-run anywhere: NOTRACE (trace blob removed), BADREADER (reader sha corrupted), WRONGREV, C2_TMP (planted `dir="/tmp"`).** Either run phase B and commit its receipt before deciding, or extend the deciding gate to require it.

---

## Predicate sentence identity (plan / counter / receipt)

- **C1: identical.** The full predicate (contract.json:14) — precheck `cand_credited=64 lost=0 ok` exit 0; 30 frozen headings each with ≥1 ledger entry with traces under `rekey-r53-<C0>/`, `read_rev` the commit named by `<C0>`, `wrong_expectations`/`blocking_gaps` 0; ≥1 committed reader JSON per heading with matching `section_sha256` — is implemented clause-for-clause by `c1/measure.py`, which is strictly **stronger** (adds: unique rekey dir, `<C0>` ancestry, trace blobs exist at REV, reader `cand` prefix match, sha via the frozen round-18 sectionize). The single looser spot — `read_rev` checked by `startswith(c0)` rather than commit resolution — is immaterial (a bare `a41195dfc13a` prefix still names the required commit; any other commit fails). The only predicate copy in the frozen tree is contract.json itself (`git grep '64 of 64' e62d9971` → 1 hit), so plan≡contract≡counter with no divergent duplicate.
- **C2: clauses 1–3 identical** (regex byte-identical to the predicate's; selftests with TMPDIR bound to the counter's scratch; cr47 arm checks non-zero + scratch message + no `REGISTRY_CHECK` verdict line). **Clause 4 is narrower than its sentence — see F3.**
- **Receipts:** phase-A receipts match the contract's control semantics; cosmetic drift: contract names the C1 base control `CTL_0`, the receipt prints `CTL_C1_BASE`.

## Do-nothing reachability: NO for both — reproduced independently

I re-ran the freeze-extracted counters at BASE `6db1d220` (own scratch, GIT_* env stripped by the counters themselves — same-identity rerun):

```
C1_R53: rev=6db1d220b337 credited=45 lost=19 rekeyed=0/0 readers=0/0 total=3 C1_R53_PASS=false  (exit 1)
  PROBLEM precheck-not-green … cand_credited=45 lost=19 RED / rekey-dir-count=0 / lost-headings-missing-at-rev
C2_R53: rev=6db1d220b337 tmp_hits=9 … docs=stale-patterns=4 total=4 C2_R53_PASS=false  (exit 1)
  PROBLEM tmp-hits 9 / cr47-zero-exit / cr47-no-scratch-message / skill-doc-stale [×4]
```

Matches the committed phase-A receipt (`CONTROLS: total=2 pass=2`, exit 0) and the contract's CTL_0/CTL_BASE text — including the `lost=19` the receipt's 110-char truncation hides. A do-nothing round cannot reach either target. (The inversion is F1: as frozen, *nothing* can reach C2 together with no-harm.)

## cannot_see routes and wave-2 coverage grades

| # | Route (counter blind spot) | In contract cannot_see? | Wave-2 coverage | Grade |
|---|---|---|---|---|
| C1-a | semantic fairness of fresh reader findings | yes | T53W2CritSemantic (6 of 30 sections), ReadersA–E (mechanical) | PARTIAL |
| C1-b | recorded inputs = right citation set | yes | T53W2RevC1Counter (3 of 30 hand-verified), MutLedger(c) | PARTIAL |
| C1-c | fixed statements true beyond frozen checks | yes | CritSemantic + RevQuality + RevLesson | PARTIAL |
| C1-d | ledger/trace **fabrication** (trace content never validated; only existence as blobs) | no (broader than "citation set") | 3/30 hand check + mutants (a),(c),(d) | PARTIAL |
| C1-e | reader JSONs written by the round itself (provenance-of-reader unverifiable from artifacts) | no | mechanical audits cannot rule this out | NOT COVERED (inherent) |
| C2-a | TMPDIR redirection truly isolates | yes | CritTools (a–d), RevC2Counter (e,f) | GOOD — and realized at `C*` (F2: silent `/tmp` fallback on unusable TMPDIR) |
| C2-b | tools/counters outside `tools/` | yes (disclosed as routed, not claimed) | none — honestly out of claim | NOT COVERED (disclosed) |
| C2-c | hosts where TMPDIR itself is ignored | yes | CritTools (d) empty TMPDIR, (e) read-only | PARTIAL |
| C2-d | stale `/tmp` scratch prose for either tool beyond the 4 patterns | **no — missing from cannot_see** | **none** (RevC2Counter(g) attacks `tools/` grep only) | **HOLE — instantiated at SKILL.md:2161 (F3)** |
| KILL-a | FREEZE arg is caller-supplied to deciding-run.sh | no | T53W2RevFreeze + CritContract re-verify against `e62d9971` post-hoc | COVERED post-hoc |
| KILL-b | phase-B receipts ungated (F4) | no | partial | PARTIAL |

## What is sound (verified, not assumed)

- Freeze integrity: all 8 frozen files' sha256 at `e62d9971` match `freeze.json` exactly (recomputed over `git show` bytes). `FROZEN_UNCHANGED` therefore binds the bytes this review read.
- Gate-0 refusals in `deciding-run.sh`: control receipts must exist at REV in a commit descending from FREEZE; second invocation refused via `$k.start`; dirty-tree witness; counters/no-harm/precheck run from freeze-extracted bytes (safe under the clean-tree gate they sit behind); 12/12 `^NOHARM .* ok$` required (12 monitors counted in no-harm.sh — matches); both `C*_R53_PASS=true` greps required.
- C1 counter strictly stronger than its predicate (see above); lost-headings count = 30 (predicate wording matches the file, amendment 5 honest).
- `C*` is not an ancestor of the freeze (fix pass post-freeze, as declared); both counters resolve and verify revisions via `rev-parse --verify --end-of-options`.
- No resume path exists in this contract: the deciding run is single-shot and refuses re-invocation rather than resuming; there is no `resume_continuity_v1` surface here to check. (Role requirement noted; nothing to verify beyond the refusal.)

## Residual risk / verification gaps

- The C2-at-REV verdict depends on a post-`C*` registry-check commit that does not exist yet (F2); the deciding receipts will arbitrate. No wave-2 seat re-runs the 12 no-harm monitors, so F1 will first manifest at the L1's single-shot deciding run — flag it now, while an amendment is still cheap.
- I did not audit all 30 ledger entries (wave-2 samples 3), did not run the deciding run (L1-owned single shot), did not re-run the precheck at `C*` (wave-2 precheck seats own it).
- LSP device unavailable for this review (no server answers the lane's Python files here); caller/definition checks were done by direct byte reads of the frozen objects — recorded per role rules, not presented as semantic proof beyond what the bytes show.

## Minor findings

- Contract C2 `before` names 2 hardcodes ("registry-check.py:766 and env-diff.py:61"); BASE actually has **9** hits across 7 files (listed under F1). Frozen prose under-describes the surface — the same under-description that let the `tools-scope` allowlist go stale. No soundness impact (do-nothing control is stronger, not weaker).
- Cosmetic: `CTL_0` (contract) vs `CTL_C1_BASE` (receipt); `deciding-run.sh` header says OUTDIR must be EMPTY but the code only refuses on existing `$k.start`; `env-diff.py:44` at `C*` keeps `"/tmp/w/home"`/`"/tmp/w/tmp"` literals inside selftest fixture env (out of predicate scope).

## Tooling record

No tools installed or upgraded (operator 2026-10-19 authorization unused): system `python3` and `git` only; pacman untouched per host guard. Scratch `/fast/scratch/hyaku/tameshi-r53/w1/T53W1RevContract/` deleted before yield.
