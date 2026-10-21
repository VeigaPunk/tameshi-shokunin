# Audit1436 — round-19 w1 BUILD advisory (C1 boundary: historical-evidence audit)

Seat: TameshiR19-2.Audit1436 (read-only reviewer). Scope honored: only the assigned receipt
pair, its trace, the coldread ledger entry, the ledger-referenced report block, and the C1
lessons file were read. No reexecution, no production edits, no tests/builds/lints. Tools
installed: none.

Axes (godspeed): (1) stdout/stderr hash fidelity, (2) trace argv↔receipt binding,
(3) revision/input facts established vs asserted, (4) C1-repair invalidation risk.

## Established facts (all observation, commands shown)

Files (absolute under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/`):
- `.ufo/evidence/round-18/final/audit-1436.stdout` — 7067 B, sha256
  `b0168f4c646af9453713a6058afe813da385b34ed20b3db517496b9531360bea` (`sha256sum`, this session).
- `.ufo/evidence/round-18/final/audit-1436.stderr` — 0 B, sha256 `e3b0c442…7852b855` (empty-string hash).
- `.ufo/evidence/round-18/coldread/traces/L1/audit-1436.json` — schema `tameshi-trace-inputs-v1`.
- Ledger entry: `.ufo/evidence/round-18/coldread/ledger.json` (entry whose `traces` contains
  `audit-1436.json`; ~lines 12201–12247).

| # | Check | Command (abridged) | Observed |
|---|---|---|---|
| 1 | Git retention | `git ls-files`, `git log -1`, `git diff --stat HEAD -- .ufo/evidence/round-18/` | All three files tracked; last touched `a134a09 2026-10-20T18:47:13-03:00`; diff vs HEAD empty — retained bytes are the committed bytes. |
| 2 | Rev identity | `git cat-file -e a9c94c5…^{commit}`; `git merge-base --is-ancestor a9c94c5… refs/heads/master` | rc 0 both. Trace `rev` == ledger `read_rev` == `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`. |
| 3 | Input binding | `git show <rev>:<path>` + sha256, for all 17 `trace.inputs` | 17/17 match recorded hashes — inputs are established against the recorded revision, not just the worktree. |
| 4 | Section binding | sha256 of SKILL.md@rev lines 1436–1447 and 1436–1448 | `441858d2ff55a2dc…` == ledger section `sha256` **and** == the exact range the trace spec read; `01b54e28…` for 1436–1448 is not the recorded value. |
| 5 | stdout structure | parse stdout; compare first 13 lines to `git show rev:SKILL.md` | Line 1 `SECTION 1436 1447` == spec; content lines byte-equal SKILL 1436–1447; 16 `OPEN <path> sha256=… bytes=…` lines; final line starts `VERIFIED actual execution receipts`. |
| 6 | OPEN↔trace↔disk | compare each OPEN hash/bytes to `trace.inputs` and current files | 16/16 equal, zero drift: OPEN hashes == trace inputs == rev blobs == current disk. |
| 7 | argv binding | read full argv (trace lines 33–34, raw) | `bwrap --ro-bind / / … --unshare-net --die-with-parent` → `env -i` (GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1, JJ_CONFIG=, LC_ALL=C, sandboxed HOME/TMPDIR) → `python3 -c <script> <spec>`; spec `{"start":1436,"end":1447,"paths":[5 knowledge files + 11 final receipts]}` — path list == OPEN set. Script is pure read/assert/print (no writes). |
| 8 | Assert passage | argv script text + `exit: 0` + VERIFIED tail line | Script prints VERIFIED only after 8 asserts (registry `held==total==31`; probes `open=0 closed=11 total=11`; regression `cases=8 passed=8`; historical `cases=4 passed=4`; case7/case8 `killed=5 survived=5 …kill-rate=50%`; disposition `status==clean`; before `status==failed`; repeat `controls_match`). exit 0 + empty stderr + VERIFIED present ⇒ asserts held at run time. This is the C1/C2 receipt-content binding. |
| 9 | Ledger coherence | compare entry fields | `skill_sha256` 1334c512… == trace SKILL.md input == `_meta.expect_skill_sha`; ledger inputs == trace inputs − SKILL.md with `inputs_dropped:["SKILL.md"]`; `verdict:"gap-minor"`, `commands_executed_count:1` == the one recorded command. |
| 10 | Report coherence | `.ufo/waves/round-18/w3/L1Residual.md:302-362` | Same start/heading/class/verdict, same opened list, same input hashes, same trace path; its `minor_gaps` honestly discloses that ancestor-pinned receipts (921ef807/5923d89) differ from the read revision only by citation/receipt files. |
| 11 | "Same instrument blobs" corroboration | cross-hash vs `.ufo/evidence/round-18/final/checks.json` | `probes.stdout` d37c99e3… == checks.json probes row whose argv pinned `--rev 921ef807…` (exit 0); `registry-branch-aligned.stdout` 6502cb38… == the rev-5923d89 receipt cited in corpus/lessons/round-18-verifier-spotcheck.md §2. Claim established, not asserted. |

## Findings by severity

**Blocker / Major: none.** The receipt pair, trace, and ledger entry are mutually consistent;
revision and input facts are established against pinned blobs, and every claim the audit's
argv makes is checkable from retained bytes.

**Minor F1 — the stdout hash is claimed nowhere.** `b0168f4c…` appears in no ledger field, no
trace field (schema records inputs/exit only), not in `L1Residual.md`, `checks.json`,
`measure-final-60.json`, or `assemble-final.stdout` (grep over `.ufo`, this session). Receipt↔trace
binding rests on basename + full content agreement + git tracking. Failing criterion: a
tampered-but-content-consistent stdout would be undetectable without re-deriving from git
history; one recorded pin (e.g. a ledger output-hash field) would close it. Same hygiene family
as routed defect lessons §5.4, but distinct and not among the five.

**Minor F2 — end-convention trap (observation, no repair owed).** Ledger entry `end: 1448` vs
trace spec `end: 1447`. Proven identical section: ledger `sha256` 441858d2… == SKILL lines
1436–1447 (end-exclusive convention) and the spec's `lines[1435:1447]` slice reads the same 12
lines. Recorded only so future readers do not misread this as a mismatch. Cross-entry
convention uniformity was not checked (out of scope; no extrapolated completeness).

**Info — `rev_reason: null`** in the trace; reason for choosing `a9c94c5` unrecorded by the
harness. Ledger `read_rev` and report corroborate the choice. Cause unknown, impact nil.

## Can C1 repairs invalidate this historical evidence?

No — provided repairs stay append/supersede. Reasoning grounded in what was verified:

1. The evidence's truth conditions are (a) retained bytes (git-tracked at `a134a09`, worktree
   clean) and (b) input hashes at `read_rev a9c94c5`. Git blobs at that revision are immutable;
   no later edit of any input file can make the recorded 17/17 binding false *for that revision*.
2. The one C1 repair that touches an input of this audit is lessons §5.4 (mis-invoked
   `bash-witness-selftest` row, exit 64, in `final/checks.json`, hash `fed3c8e6…`). checks.json is
   opened+hashed by this audit but **no argv assert reads the defective row** — the asserts cover
   registry/probes/regression/historical/case7/case8/disposition/before/repeat only. Repairing or
   superseding checks.json therefore cannot retroactively falsify anything audit-1436 asserted.
   After a checks.json fix, a present-day re-verifier resolving inputs against the new tip will
   see `fed3c8e6…` drift and must resolve via `read_rev` — a usability cost, not invalidation.
   Recommended (advisory): any checks.json repair should append a dated erratum naming the
   superseded input hash so auditors resolve it to `a9c94c5` without re-derivation.
3. §5.1/§5.2/§5.3/§5.5 target `guard-kill-closure.md`, `mutation-case-kumitate-sources-check.md`,
   `corpus/lessons/round-18.md:79`, and the 60/60-receipt claim — none is an input here.
   Appending errata to knowledge files that ARE inputs (e.g. `fleet-kill-rate-ledger.md`,
   13a11e46…) changes current-tip comparability only; the ledger's `read_rev` +
   `carry_coverage_basis: section_sha256` is the designed resolution path.
4. Invalidation would require rewriting `audit-1436.stdout/.stderr`, its trace, the ledger, or
   git history — i.e., laundering round-18 evidence. That is outside the declared C1 scope
   (metadata/receipt defects, append-only corrections) and would contradict the lane's own
   retained-v1 precedent (spotcheck §2: "v1 is retained, not laundered"). [INFERENCE from the
   append-only discipline cited in lessons §8 and corpus/QUALITY.md conventions; the discipline
   itself was not re-audited here.]

The C1 claim itself (5/5 defect repairs, calibration stays 8) is measurable without touching
this receipt pair; this audit's evidence neither supports nor constrains that count beyond the
single checks.json interaction above.

## Residual risk and verification gaps

- Did not open the other 10 receipts' contents (registry, probes, regression, …); their
  integrity here rests on the audit's OPEN hashes matching trace inputs, rev blobs, and disk —
  three independent records agreeing — plus spotcheck §2, not on my re-reading of their text.
- Did not re-execute the audit command (prohibited); "asserts held at run time" is established
  from retained exit status, empty stderr, VERIFIED tail, and the argv's assert-then-print order.
- End-convention uniformity across the other 16 ledger entries: unknown (out of scope).
- `rev_reason` null: cause unknown.
- Sandbox scratch `/tmp/tameshi-r18-L1-final-a2vitd82` is ephemeral; not checked, irrelevant to
  the retained binding (argv cwd/root are recorded, inputs hash-pinned).
