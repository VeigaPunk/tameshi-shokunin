# X09AssembleV2 — round-17 coldread assemble.py (v2)

Built `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-17/coldread/assemble.py`
per interface contract C, ported from the round-16 assembler where sound.

File sha256: `d525c1807d5536983ff7cf154eb9849d24cc6373012720d23ba601a1df508aa3` (1637 lines, stdlib only).

## Behavior implemented

- **Reports**: `--reports DIR_OR_GLOB...` (dirs glob `*.md`; files/globs accepted).
  Each report must carry exactly one closed ```` ```json ```` block
  (zero or several → reject), schema `tameshi-coldread-report-v2`.
- **Validation → reject (exit 1 after assembly)**: unparsable JSON, `schema`
  present and wrong, missing/invalid `seat`/`skill_sha256` (64-hex)/
  `read_rev` (40-hex)/`sections`, unknown verdict/class, non-list gap or
  command fields, non-dict `inputs`/`external_inputs`, non-64-hex digests,
  `start` that is not a section start of the resolved page, heading text
  mismatch (preamble start=1 tolerates `""` or the page's first line, as v1).
- **Page resolution** (`--repo`, default the lane containing the script):
  `SKILL.md` at the report's `read_rev`; its sha256 must equal
  `skill_sha256`, else a `git ls-tree -r` + `cat-file --batch` scan at that
  rev looks for any matching blob. No match → `page-sha-mismatch` rejection;
  unresolvable `read_rev` → rejection.
- **Sectionizer**: ported verbatim — preamble + `#`/`##`/`###` headings
  outside ```` ``` ````/~~~ fences; section sha256 over lines joined by `\n`
  after stripping trailing blank lines.
- **Merging**: entries grouped by `(skill_sha256, start)` merge **only when
  `inputs` maps are identical**; `external_inputs` and `read_rev` are also
  group keys so scalar entry fields stay faithful (a stricter condition than
  the contract's "only when inputs agree" — satisfied). Within a group:
  strictest verdict wins after the v1 minor-gaps downgrade
  (executed-ok/verified-record with `minor_gaps` → `gap-minor`),
  `instruction` wins on class disagreement, gap/command lists are summed to
  counts, `seats`/`reports`/`traces` are order-preserving unions.
- **Ledger**: schema `tameshi-coldread-ledger-v2`; v1 entry fields plus
  `read_rev`, `inputs`, `external_inputs`, `traces` (when non-empty).
  `_meta` carries pages, loaded/rejected reports (with reasons), seats,
  read_revs, expect_skill_sha, uncovered.
- **Exits**: 0 written + every bucket of `--expect-skill-sha` page (or every
  observed page when the flag is absent) covered, no rejections; 1 uncovered
  bucket (headings printed) or any rejected report or unresolvable expected
  page; 2 argparse/operational errors (repo unusable, out unwritable).
- `--selftest` uses only synthetic fixtures: a scratch git repo in mkdtemp
  (git writes confined to /tmp; no lane repo writes anywhere in the tool —
  all lane access is read-only `cat-file`/`ls-tree`/`rev-parse`, each with
  every `GIT_*` variable scrubbed from the subprocess environment).

## Verification

- `python3 .ufo/evidence/round-17/coldread/assemble.py --selftest` →
  **59/59 checks, `SELFTEST: all checks passed`, exit 0** after the follow-up
  hardening (the pre-hardening build passed 36/36; the hardening section below
  lists the added cases).
- Dry run on two synthetic reports in
  `/tmp/tameshi-r17w1-X09AssembleV2-7hOgza/reports/` (seatA 28 sections,
  seatB 26 sections) against the real lane repo at rev
  `98bea7da5801f4bc58e4187690ee1687c8a5061f` (SKILL.md sha256
  `906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397`,
  54 buckets): `coverage: 54/54 buckets covered`, `rejected reports: none`,
  **exit 0**; ledger entry keeps `read_rev`, `inputs`, `external_inputs`,
  `seats`, section `sha256`/`end`.

## Design notes / retained decisions

- `read_rev` restricted to 40-hex (contract literal); revs never reach a
  shell (`subprocess` list form).
- A report-level `schema` field is optional; if present it must equal
  `tameshi-coldread-report-v2` (contract shows schema in prose, not as a
  required key).
- Multiple entries for one `(skill_sha256, start)` (inputs disagreement)
  are emitted verbatim — measure.py must handle the ambiguity per R05's
  review surface.
- The v1 "minor_gaps downgrade" and "instruction wins on class disagreement"
  merge rules are retained for verdict comparability with v1 ledgers.
- Ledger is written even when coverage fails/rejections exist (partial
  evidence is data, not a pass); exit code carries the verdict.

No tools installed (pacman paused; none needed — python3/git/strace present).

## Verdict

built — assemble.py contract-C complete, selftest 59/59 exit 0, dry run 54/54 exit 0.

## Follow-up

L1 follow-up (R05ReviewContractC.md §5 A4/A5 + N01TraceGitSafety F1). Read
`.ufo/waves/round-17/w1/R05ReviewContractC.md` §1 F1/F4/F6/F10, §3 step 5,
§5 A1/A4/A5, §8, §10, and N01's F1 note. Hardened
`.ufo/evidence/round-17/coldread/assemble.py`; no other lane file written.

Final file sha256: `d525c1807d5536983ff7cf154eb9849d24cc6373012720d23ba601a1df508aa3`
(1637 lines).

### What changed

1. **A4 trace binding** (F4). Each section `traces[]` entry is resolved
   (lane-relative against `--repo`'s worktree; absolute receipts taken as
   given because seats may emit them to `/tmp`), must exist, must carry
   `schema: tameshi-trace-inputs-v1` and `rev == read_rev`, and its
   `inputs`/`external` maps are unioned into the section's maps. A path
   declared with two different sha256 is rejected
   `trace-conflict:<path>`; the same sha is idempotent. Receipt keys in
   `DROPPED_INPUT_KEYS` are dropped there too. An observation that ran
   commands without any receipt is rejected (`trace-receipt-missing`), which
   closes the "seat hand-writes a smaller inputs map" hole.
2. **Exempt inputs** (F6/F10). `SKILL.md` and
   `.ufo/evidence/round-17/coldread/ledger.json` are dropped from declared
   inputs (before conflict checks) and from receipt inputs. Each entry records
   the dropped keys as `inputs_dropped` for audit; a page edit or the
   assembler's own output can no longer manufacture `input-drift`.
3. **Canonical inputs + A5 separation** (F9/A5). Input keys that are
   absolute, `./`-prefixed, contain `..`, a `.git` component, an empty
   component or NUL are rejected `noncanonical-input:<key> (<why>)`.
   `external_inputs` stays a separate map; a key must be an absolute path or
   `repo@rev:path`, and an absolute path under the lane root is rejected
   `external-input-lane`.
4. **Fail-closed entry separation** (F1). `is_failing(obs)` = verdict in
   {gap-blocking, wrong-expectation, not-executed} or non-empty
   blocking_gaps/wrong_expectations. Failing observations join the group key,
   so a failing observation is emitted as its own entry and can never be
   merged into (or hidden behind) a clean observation with identical inputs;
   the measure's fail-closed aggregation then vetoes the section.
5. **N01 F1 (lane-clobber class)**. Every git subprocess — `_git`, the
   `cat-file --batch` scan, page resolution and the selftest's `run_git` —
   runs with all `GIT_*` variables scrubbed (`_git_env()`), so an exported
   `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` cannot redirect reads or
   writes. `blob_at` now uses `git cat-file blob` (not `git show`, which
   prints a tree and exits 0 for a directory).

### Verification (commands, exits, key lines)

- `python3 .ufo/evidence/round-17/coldread/assemble.py --selftest` →
  **59/59 `[ok]`, `SELFTEST: all checks passed`, exit 0**. New cases:
  receipt union into `inputs`; `trace-receipt-missing:traces/absent.json`;
  `trace-receipt-schema:… != tameshi-trace-inputs-v1`;
  `trace-rev-mismatch:… receipt rev … != read_rev …`;
  `trace-conflict:tools/second.py: receipt traces/t1.json declares dddd…,
  section declares eeee…`; commands-without-trace rejection;
  `noncanonical-input:/etc/passwd (absolute)`;
  `noncanonical-input:tools/../x.py (parent-component)`;
  `external-input-lane:/tmp/…/repo/SKILL.md`; declared and receipt-side
  `SKILL.md` dropped with `inputs_dropped: ["SKILL.md"]`; failing entry kept
  separate (3 alpha entries: clean merged `gap-minor` with seats
  `["SeatA","SeatB"]` plus failing `gap-blocking` with seats `["SeatD"]`);
  `GIT_* scrubbed for reads`, `GIT_* scrubbed inside main` (code 1,
  rejected 0 with `GIT_DIR`/`GIT_WORK_TREE` pointing at a decoy repo), and
  `decoy repo untouched`.
- Dry run, two synthetic reports (seatA 28 sections, seatB 26 sections) plus
  two receipts in `/tmp/tameshi-r17w1-X09AssembleV2-7hOgza/`, against the real
  lane at `98bea7d…`:
  `coverage: 54/54 buckets covered`, `rejected reports: none`, exit 0.
  Entry `start=6` shows the effect: `inputs` =
  `tools/evidence-disposition.py` + receipt's `tools/second.py`,
  `inputs_dropped: ["SKILL.md"]`, `external_inputs` = `/tmp/outside.txt`,
  `traces` = absolute receipt, `read_rev` = `98bea7d…`; no entry keeps
  `SKILL.md` in `inputs`.
- `python3 -c "ast.parse(...)"` → `parse ok`.

### Notes / risks for L1

- The `rev == read_rev` receipt check is R05 A4's literal requirement and is
  enforced as a reject. `trace-inputs.py` permits `rev: null` when the traced
  root is not a git tree; such a receipt now rejects, which is the intended
  fail-closed consequence (an unbound trace cannot key credit). If L1 prefers
  a warning for null-only revs, that is a one-line relaxation.
- Receipt-side `external` keys are also unioned (kept out of `inputs`), subject
  to the same conflict and A5 checks.
- `inputs_dropped` is additive audit metadata (not in contract C's field list);
  measure.py ignores unknown fields.
- Absolute trace-receipt paths are accepted so wave-2 seats can keep receipts
  in `/tmp`; a lane-relative path is resolved against `--repo`'s worktree and
  must exist, per L1's wording.
- No git writes were run in the live lane; the hardened selftest's git writes
  are confined to its mkdtemp repo, and every git call scrubs `GIT_*`.
