# T49W2CritGenOracle — generator independence & honesty at f181a961

Attacked: `tools/pbt-staged-id.py` at candidate `f181a961ae44061af486f600e5ea257d2baf78f8`
(git-archive copy in scratch; byte-identical to the lane blob — receipt
`T49W2CritGenOracle-receipts/guard-sha-check.txt`) against the pinned gate
`tools/staged-id-guard.py` sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`
(verified identical at f181a961, at the lane worktree, and in scratch). All runs were probes in
scratch; none is a verdict. Line numbers below are `pbt-staged-id.py@f181a961` (abbreviated GEN)
and `staged-id-guard.py` (abbreviated GRD).

Axes named: runtime independence (import/exec/copy/scrape, special-casing, file scope), oracle
fidelity vs documented contract, distribution honesty, kill sensitivity.

## F1 — HIGH (honesty): the oracle is a freeze-time transcription of the guard's implementation, while the docstring claims "written from the guard's *documented* contract"

- GEN:6-8 claims: "Nothing here imports, execs or re-reads the guard's source: the expected answer
  comes from an oracle written from the guard's *documented* contract". The first half is true at
  runtime (F4); the second half is not. The oracle is a line-by-line transcription of the guard's
  code, including rules that appear in no docstring:
  - GEN:56-59 `ROW_RE`/`COLUMN0_RE`/`URL_RE`/`SID_RE` are byte-identical to GRD:65-68.
  - GEN:126-167 `analyse_fields` is 39/42 non-comment lines identical to GRD:132-177 `analyse`
    (difflib ratio 0.89 — receipt `oracle-correspondence.txt`).
  - GEN:81-90 `document_key` reproduces GRD:99-113 verbatim, including the undocumented
    thresholds `len(head) > 8`, extension regex `\.[A-Za-z0-9]{2,6}$`, the no-space rule, and the
    `cells[1:6]` blob. The guard's documentation says only "its URL/DOI, else a path-like source
    head" (GRD:100) and "no URL/DOI and no path-like source head" (GRD:17-20) — no thresholds.
  - GEN:101-106 `id_number` transcribes the undocumented 12-char id cap (GRD:127-128) and admits
    it: "observed guard rule; not generated, kept for fidelity" (GEN:104).
  - GEN:170-243 `map_fields` mirrors GRD:180-270 `validate_map` refusal-for-refusal, and GEN:209-210
    admits the coupling: "reason order follows the guard's own order".
  - Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961:tools/pbt-staged-id.py`
    vs the pinned guard source; quantified in `T49W2CritGenOracle-receipts/oracle-correspondence.txt`.
- Consequence for C2: the predicate clause "finds no violation on the pristine guard"
  (contract.json:48) certifies transcription fidelity over the transcribed rules, not guard
  correctness; mutant kills measure divergence from the freeze-time implementation bytes rather
  than from the documented contract, so contract.json:57's "the generator is built against the
  guard's documented contract" is half true. NOT a violation of the frozen interface, which
  forbids only "imports or execs the guard's code except through its CLI" (contract.json:53) — no
  import/exec exists (F4).
- Smallest safe correction (L1's call): reword GEN:6-8 (and any narrative echoing it) to state
  that the oracle transcribes the guard's freeze-time implementation, naming the undocumented
  quirks it carries (12-char cap, `len>8` head, 2–6-char extension, `cells[1:6]` blob, reason
  order). Doc-only; no behavior change.

## F2 — MEDIUM: `reason_classes` substring projection silently discards confirmable kills on prose rewrites

- GEN:267-293 projects the guard's reason prose onto `(class, ids)` by matching exact substrings
  taken from the guard's reason strings (GRD:213-254: 'does not carry', 'collide with registry
  ids', 'still staged ids', 'below the safe floor', 'does not cover', 'on itself', 'undocumented
  row', 'held document off', 'injective').
- Observed counterexample (scratch mutant, receipt `run-m2-prose.stdout`): rewording GRD:213
  `'map is not injective (two staged rows share a target)'` → `'the map is not injective'`
  SURVIVED: `PBT_STAGED_ID: cases=120 violations=0 counterexample=none` (exit 0), because
  `'injective' in text` still matches (GEN:273). That mutant's stdout differs from the pristine
  guard's on every injective-reason case, so the counter's differential-confirm path
  (measure.py:338-344, `comparable(a) != comparable(b)`) would have confirmed the kill had the
  generator flagged it. The leniency is one-directional: a rewrite that removes every recognized
  substring falls to `('unknown', text)` (GEN:292) and is killed.
- Panel risk: a hidden mutant of exactly this shape is unkillable by design; kill_target is 11/12
  (contract.json:59), leaving one permitted miss. Nothing in wave 2 can check which shape the
  panel holds (reading the panel voids the claim).

## F3 — MEDIUM: structural blind spots — guard behaviors the generator cannot emit

- Duplicate-key map JSON: the generator writes maps only via `json.dumps(case['map'])` from a
  dict (GEN:768), so the guard's duplicate-key refusal GRD:406-413 (wired at GRD:443) is
  unreachable. Observed (receipt `run-m3-dupkeys.stdout`): scratch mutant `if bare in seen:` →
  `if False and bare in seen:` SURVIVED 120 cases, exit 0, `violations=0`.
- Size/regular-file/UTF-8 refusals: no recipe emits input over `MAX_TEXT`/`MAX_MAP` (GRD:69-70),
  a non-regular file, or non-UTF-8 bytes (GRD:416-445); every recipe builds small UTF-8 text
  (GEN:373-727). The setup-refusal surface is exercised only for short rows, duplicate ids and
  malformed map JSON (GEN:483-504, 718-727).
- Consequence: any panel mutant inside `_no_duplicate_keys` or the read/limit path is structurally
  unkillable. Same single-miss budget as F2 applies.

## F4 — INFO (verified honest): runtime independence, no special-casing, CLI-only kill path

- No import/exec/scrape of guard code at runtime: imports are stdlib-only and exclude `hashlib`
  (GEN:45-54); the guard is reached only as `[sys.executable, '-I', guard, …]` (GEN:762-770).
  strace of a 10-case run (receipts `traceD-guard-tmpdir-paths.txt`,
  `traceD-parent-never-read-guard.txt`): the guard file was opened `O_RDONLY` only by the per-case
  child interpreters; the generator process itself never opened it; 0 `socket`/`connect` calls; no
  path under `/home`, `~/.local/state`, or the lane was touched; case files and work dir confined
  to TMPDIR (`…/tmpD/pbt-staged-id-*/case/{registry.md,staged.md,map.json}`).
- No byte/sha/path special-casing: `--guard` accepts any regular file (GEN:981-983 checks isfile
  only). Observed: a renamed copy of the guard ran clean (`run-ren.stdout`: exit 0, 40 cases,
  `violations=0`); a stub guard (`raise SystemExit(0)`) produced `VIOLATION index=0 exit 0, oracle
  expects 1`, exit 1 (`run-stub.stdout`).
- Kill path through the CLI works: scratch mutant `safe_floor` off-by-one
  (`max(top, staged_top)+1` → `+2`, GRD:172) killed at index 0 with a field-level reason
  (`run-m1-safefloor.stdout`: `VIOLATION index=0 field safe_floor: guard 'S024', oracle 'S023'`,
  exit 1, `cases=1`). Actual kill sensitivity lives in `check()`'s strict grading — exit, verdict,
  exact field-set equality (GEN:296-323, 312-316), with only `registry_sha256`/`staged_sha256`
  tolerated (GEN:68, 312).

## F5 — INFO (verified honest): the distribution is observed, not padded

- Printed counts equal an independent recompute: I re-ran the pristine guard on all 400 dumped
  cases with my own runner and classifier and got identical counts for all 12 classes
  (receipt `recompute-classes.txt`: e.g. collision 204/204, refusal 61/61, map 104/104; exit
  histogram 232×0, 107×1, 61×2; `ALL MATCH`). Dump had exactly 400 lines with indexes 0..399.
- The generator's classifier (GEN:329-367) is semantically identical to the counter's frozen
  `case_classes` (measure.py:117-158) — identifier renames only, so the scored distribution and
  the printed one are the same predicates.
- Counts are organic, not floor-driven: collision=204 vs no_collision=62; indent_1_3=248 arises
  incidentally from `rnd.randint(0, 3)` indents in unrelated recipes; map=104 reconciles as 31
  admissible + 31 inadmissible + ~30 map-setup-refusal + ~12 from `rec_path_document`'s 50% map
  (GEN:712-714). All 12 classes ≥ 30 against the contract floor 10 (contract.json:55) and the
  generator's own stricter CLASS_MIN 20 with `SHORT` marking (GEN:66, 825-827).
- Shape scheduling is disclosed in-code (Cycle, GEN:384-399: "scheduled, not sampled") and the
  scheduled object is the 13 recipes, not the class counts — classes are still measured from the
  generated bytes plus the guard's answers.
- Deterministic from the seed: two seed-4949 runs produced byte-identical dumps,
  sha256 `ca62402bc6125cb8003b3854a30bef829d29d5c6656be1f8a516ca2828a7cd28`
  (receipt `dump-determinism.sha256`), from a single `random.Random(seed)` (GEN:785).
- `--selftest` passes 31/31, exit 0 (receipt `selftest.stdout`).

## F6 — LOW (recorded, no defect): TMPDIR must exist; exit-semantics deviation is pre-registered

- `tempfile.mkdtemp(prefix='pbt-staged-id-')` (GEN:789) honors TMPDIR only if the directory
  exists; with a nonexistent TMPDIR python silently falls back to `/tmp` (my first trace pass
  tripped on this — operator error, re-run clean). The frozen counter creates its TMPDIR before
  invoking the generator (measure.py:81-86), so the deciding run is unaffected.
- The oracle grades exit 1 for refused analysis (GEN:255), contra the guard docstring GRD:38-39 —
  this follows the contract's pre-registered `guard_exit_semantics_observed` (contract.json:54),
  matches GRD:491-493, and is disclosed in GEN:22-27. Honest deviation, no action.

## Method note

All probes ran in `/fast/scratch/hyaku/tameshi-r49/T49W2CritGenOracle` (git-archive of f181a961;
`TMPDIR` under it; mutants and stub built only in scratch). No lane file was read or written
outside this report and its receipts directory; the frozen counters were never run against the
lane; the hidden panel and the named control stdouts were never opened.

## Summary

- HIGH: the "oracle written from the guard's documented contract" claim (GEN:6-8) is false in detail — it is a verbatim transcription of the guard's implementation (regexes byte-identical, analyse 89% identical, undocumented 12-char cap and len>8/2–6-ext thresholds carried); no interface violation, doc-only fix suggested.
- MEDIUM: reason-substring projection (GEN:267-293) let a prose-rewrite mutant survive whose kill the counter would have confirmed (run-m2-prose.stdout).
- MEDIUM: unreachable guard behaviors (duplicate-key map JSON, size/regular-file/UTF-8 refusals) are structural kill blind spots (run-m3-dupkeys.stdout survivor).
- Verified clean: runtime independence (strace: parent never reads guard bytes; 0 sockets; TMPDIR-confined), no byte/sha/path special-casing (stub→VIOLATION, renamed→clean), CLI kill path works (safe_floor mutant killed at index 0).
- Verified honest: printed class counts equal an independent recompute over all 400 dumped cases; classifier identical to the frozen counter's; deterministic dumps (sha256 ca62402b…); floors exceeded ≥3×.
- Panel exposure: at most one of the F2/F3 survivor shapes fits the 11/12 kill budget; if both shapes are in the hidden panel, C2 fails — the L1's deciding run decides.
