# CorpusEntry — round24 w1 critic report

Target: `corpus/knowledge/replay-projection-hardening.md` (landed at d2eaecd, unchanged at c8c5b88).
Scope: overclaims about authentication, isolation and mutation adequacy; the provenance trio; S084/S085 citations.
Mode: read-only inspection only. I ran no ruler, selftest, gate or `--plan`. Tools installed or updated: none.

## Verdict

**Fixable defects found: 2 medium, 4 low. None needs the judge to reject a tradeoff.**

The authentication and write-isolation disclaimers are sound. The overclaims are in the hardening table:

- **Medium:** the stream-bound row claims more than the code does.
- **Medium:** the argv row lists two weakenings (stripping and de-duplication) that no ruler predicate measures. Under the entry's own QUALITY48, those two do not count as repaired.
- **Low:** the sibling-realpath row hides an untested renaming hazard.
- **Low:** citation scope gaps in both S084 and S085.
- **Low:** the "four mutants killed" bound states a result that no retained after-receipt backs yet.

## What holds (checked, no defect)

- **S085 provenance.** `git show 6a1821a:.ufo/waves/round-23/fresh-adjudication.json` is byte-identical to the worktree (130 lines).
  - Lines 53–104 run from the first to the last `defect` of `routed_not_executed`.
  - The lesson's located quote (line 66, "do not pin bundle_sha256 literals…") is present.
  - Base 6a1821a is a commit, and the SOURCES S085 row (SOURCES.md:94) matches the header.
- **S084 quote.** The quote is verbatim, a prefix of the `os.path.realpath` first paragraph (the rest is "(if they are supported by the operating system)").
  - The live page title reads "Python 3.15.1 documentation", which matches the row's version claim. I fetched https://docs.python.org/3/library/os.path.html on 2026-10-21.
- **Authentication.** Entry line 32–34 says "Neither the pin nor the gate authenticates the producer". This matches the registry-replay.py docstring (lines 16–18) and the lesson's Reject list. No overclaim.
- **Isolation.** Entry line 35–36 says "Realpath identity is not write isolation". This matches registry-replay.py:18–20.
  - The fleet root handed to the runner (registry-replay.py:170, `layout['fleet_root']`) is the live fleet.
  - registry-check.py:632–646 and :662–671 use it only to detect absolute live-fleet argv tokens (`non_hermetic_argv`), not as a cwd. So it does not widen the isolation claim.
- **Pins (K5/K6).**
  - `sha256sum` gives 3d6c99b7…a50b9 for `.ufo/evidence/round-23/replay/bundle.json` and db620668…80d3cf for `source-read-bundle.json`.
  - These equal the literals in registry.json:974 and :984.
  - The gate's sorted-key `--json` output shape `"bundle_sha256": "…"` is confirmed in `replay-gate.json` stdout.
- **Supersession.** "The runner still executes superseded rows; they do not count toward held" matches registry-check.py:30–35 and :877–884.
  - Successor rows and `superseded_by` targets are present (registry.json:933–956).
- **Runner digest.** `runner_sha256_clone_copy` is cba16646…44ad. That equals `git show d2eaecd:tools/registry-check.py | sha256sum` and the live file.
  - The row is correctly marked "— (recorded per run, not a ruler predicate)".
- **Live-dependent rows.** The actual replay lists `pin-disposition-read` (external, `non_hermetic_argv`=['/home/vgpnk/Projects/shokunin']) and `verify-round15` (external), with revision_pinned 41/43. This matches the round23 correction at fresh-adjudication.json:24.
- **Negative-exit fixtures.** extra-cases.json has an expected-0-receives-−9 mismatch and a declared −15 match with `finding_ids: []`, as the table says.

## Defects

### D1 (medium, isolation/retention): the stream bound refuses publication, not retention

- **Claim** (entry line 18): "unbounded retained streams | `--max-stream-bytes` (default 1 MiB) refuses with STREAM_LIMIT".
- **Counterexample** (static):
  - `run_replay` writes `observations.json` with full `stdout`/`stderr` (registry-replay.py:181–183) before `project()` applies the bound (:184, check at :92–98).
  - The runner also collects whole streams in memory through `communicate()` with `retain_streams=True` (registry-check.py:693, :724–726).
  - So a row emitting 2 MiB gets STREAM_LIMIT and no bundle, but its 2 MiB is still retained under `--out/observations.json` inside the lane.
  - Evidence: the actual `.ufo/evidence/round-24/replay/observations.json` is 265,728 bytes of complete streams.
  - K9 only exercises `--project` on a synthetic fixture (measure.py:172–180), so the ruler cannot see this.
- **Also silently dropped:** fresh-adjudication.json:93 routes "without size bounds **or redaction**". The entry cites lines 53–104 but never says redaction is still absent.
- **Minor precision point:** the bound measures UTF-8 re-encoding of `errors="replace"`-decoded text (registry-replay.py:96, registry-check.py:717). That is not the raw stream bytes, because each invalid byte becomes a 3-byte U+FFFD.
- **Axes:** calibration, isolation honesty.

### D2 (medium, mutation adequacy): the argv row claims stripping and de-duplication with no predicate

- **Claim** (entry line 13): "argv compared name-insensitively, case-folded, **stripped or de-duplicated** | … | a weakened comparison lets the public selftest pass".
- **Counterexample:** the frozen ruler's MUTANTS (measure.py:27–36) contain only K1 (name-insensitive), K2 (casefold), K3 (negative exit) and K4 (any-token).
  - No strip mutant and no de-duplication mutant is ever applied.
  - The `argv-padded-token` and `argv-repeated-flag` fixtures exist, but whether they kill such mutants is [INFERENCE, unexecuted].
- **Own-rule conflict:** QUALITY48 (QUALITY.md:488–490) says a routed gap "does not count as repaired until a frozen predicate for it fails at the base revision and holds after the change".
  - The table presents these two as hardened weak links next to measured ones.
  - Entry line 38 ("Four specific mutants killed…") does not cancel this, because the argv row itself asserts the failure condition.
- **Axes:** mutation adequacy, calibration.

### D3 (low, identity): sibling realpath can rename the mirror entry; only the `..`/fleet-alias case is tested

- **Claim** (entry line 20): "`--plan` realpath-normalises lane, fleet root and siblings | a symlinked or `..` path alias changes identity".
- **Counterexample** (static, [INFERENCE, not executed per lane bounds]):
  - `plan()` stores `os.path.realpath(p)` for each sibling (registry-replay.py:66–67).
  - `run_replay` names each mirror link by `os.path.basename(sibling)` (:160–161).
  - Take a fleet entry `peer-shokunin -> /srv/peer`. The mirror gets `fleet/peer`, not `fleet/peer-shokunin`.
  - A row reading `../peer-shokunin/...` from the clone then breaks. Under `registry-check.py --rev` it would resolve, because that mirror keeps the `listdir` names (registry-check.py:773–782).
  - This is a second, divergent mirror-naming convention, and realpath is what changes the sibling's identity as seen from the clone.
  - The selftest (registry-replay.py:227–240) and K11 (measure.py:184–200) only alias the fleet directory and use `..`. They never use a symlinked sibling.
  - It is latent today: `find /home/vgpnk/Projects/shokunin -maxdepth 1 -type l` printed nothing.
- **Axes:** identity, calibration.

### D4 (low, provenance): S085 coverage is selective, and the any-token source is uncited

- The header cites S085 lines 53–104 as "routed defects". Three items in that range are neither hardened nor named in Bounds:
  - redaction (line 93);
  - the receipt schema still cannot carry a live-dependency marker (line 74). `live_dependent` lives only in the report and in `live-dependent.json`, which is not covered by `expected.json`'s digest (registry-replay.py:123–127);
  - the preexisting loose stdout substring tokens (lines 97–104).
- The any-token row (entry line 15) comes from MANIFEST rounds[421] closure notes (contract.json `sources`; lesson round-24.md:53), not from S085. The entry's `source:` line omits it.
- **Axes:** provenance, calibration.

### D5 (low, provenance): the S084 anchor is narrower than the claim attributed to it

- The SOURCES S084 anchor cell (SOURCES.md:93) and the header both point to the realpath **first paragraph**.
- The entry's non-strict claim at line 37 ("may still leave missing components unresolved (S084)") rests on the second and third paragraphs. Those say: "By default, the path is evaluated up to the first component that does not exist, is a symlink loop… appended unchanged" and "may still contain links or loops".
- The lesson (round-24.md:33–35) quotes the third-paragraph phrase, but the row anchor does not include it.

### D6 (low, provenance trio): the verified-at line backs only "before"; "killed" is unretained

- `verified-at` names only the 1/11 base result. It defers after-results to the lesson and SCORECARD.
- Neither the lesson nor SCORECARD records an after-measurement yet. The lesson says "recorded below once executed", the SCORECARD says "Measured results are recorded below only after execution", and `.ufo/evidence/round-24/` contains no after receipt.
- Entry line 38 still asserts "Four specific mutants killed". At base only K4 was killed (before.json note). So "killed" for K1–K3 is currently [INFERENCE].
- The `recheck:` line has no re-open instruction for the S084 URL. Its peer `guard-kill-closure.md:3` includes one.

## Smallest safe correction (text-only unless noted)

1. **Entry line 18 (D1):** "`--max-stream-bytes` (default 1 MiB) refuses **bundle publication** with STREAM_LIMIT; `--out/observations.json` still retains complete streams and nothing is redacted." Also add a Bounds bullet for retention and redaction.
2. **Entry line 13 (D2):** narrow to "argv compared name-insensitively or case-folded (K1, K2)". Then add: "padded-token and repeated-flag fixtures exist; no strip or de-duplication mutant is measured". Alternatively, add the strip and de-duplication mutants to a future ruler; the frozen ruler must not be edited this round.
3. **Entry line 20 (D3):** replace "a symlinked or `..` path alias" with "a `..` or fleet-directory symlink alias". Add: "a symlinked sibling is mirrored under its realpath basename, unlike `registry-check --rev`".
   - Code fix, routed rather than applied: name mirror links by the fleet entry name while comparing by realpath.
4. **Header and Bounds (D4):**
   - Add the MANIFEST rounds[421] closure-notes pointer for the any-token row.
   - Add a Bounds bullet: "Still open from S085: redaction (line 93); no live-dependency marker in the gate-bound bundle, and `live-dependent.json` is outside the expected digest (line 74); loose frozen stdout tokens (lines 97–104)."
5. **S084 anchor (D5):** extend the SOURCES S084 anchor cell to cover the realpath first three paragraphs, as an append-only correction note per the round-18 rule, not a row edit. Alternatively, cite only the first paragraph and drop "(S084)" from entry line 37.
6. **Entry line 38 and the trio (D6):** change to "Three mutants (K1–K3) plus the K4 control; kills are claimed only by the retained after-receipt", until RunRulerAfter's receipt lands. Add `re-open S084 and confirm the realpath quote` to `recheck:`.

## Evidence index (commands, all read-only)

- `git rev-parse HEAD` → c8c5b88…; `git cat-file -t 6a1821a…` → commit. The S085 file at 6a1821a equals the worktree (`diff` returned nothing, so SAME_AS_WORKTREE).
- `sha256sum` of the two frozen bundles: 3d6c99b7… and db620668…, equal to registry.json:974 and :984.
- `git show d2eaecd:tools/registry-check.py | sha256sum` → cba16646…, equal to `observations.json` `runner_sha256_clone_copy`.
- `git show d2eaecd:tools/registry-replay.py | sha256sum` → 9fcd2dbb…, equal to `replay-command.json` `instrument_sha256`.
- `replay/live-dependent.json` → `["pin-disposition-read","verify-round15"]`, revision_pinned 41, rows 43; `observations.json` is 265,728 bytes.
- `find /home/vgpnk/Projects/shokunin -maxdepth 1 -type l` printed nothing, so the D3 hazard is latent.
- WebFetch of the os.path docs: page title "Python 3.15.1 documentation"; quote and non-strict paragraphs as cited in D5.
