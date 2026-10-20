# PinProbe — round 13 · C1 explicit pin dispositions

Seat: `TameshiR13.PinProbe` (leaf executor). Status: implementation and
manifest landed. **No selftest, live probe, gate, build, lint or formatter was
executed by this seat** (contract: L1 owns integrated verification). No tool
install or upgrade was needed.

## Files written

| Path | Role |
|---|---|
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py` | standalone stdlib read-only probe + isolated `--selftest` |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json` | `pin-manifest-v1`: six recorded pins, source anchors, runner digest |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-13/w1/PinProbe.md` | this report |

No sibling path was written; no frozen declaration, lesson, LOG, registry cell
or runner line was edited. `tools/mutate-and-run.sh` is unmodified.

## Leg derivation (no invented pins)

The manifest copies the six ledger legs from `tools/mutate-and-run.sh`:

- `:84-89` leg names and fleet-relative paths;
- `:542-553` `PIN_*`/`REV_*` pairs;
- `:1112-1140` `regression_case_git` calls (repo = first path segment, path =
  the rest; the runner materializes `git show <rev>:<path>` at `:894-956`).

| leg | repo / path | pinned commit | expected sha256 |
|---|---|---|---|
| js-kimi-census | kumitate-shokunin/scripts/kimi-census.mjs | `175de6ba…` | `83016d45…` |
| bash-surface-census | kagi-shokunin/corpus/surface-census.sh | `fecee874…` | `275d8294…` |
| bash-tsukuroi-census | tsukuroi-shokunin/tools/tsukuroi-census.sh | `165307fe…` | `084951be…` |
| bash-mado-verify | mado-shokunin/tools/mado-verify.sh | `eead56b2…` | `d7edaab4…` |
| bash-checklist-run | kagi-shokunin/corpus/checklist-run.sh | `fecee874…` | `7e5ec98b…` |
| js-claims-check | kumitate-shokunin/scripts/claims-check.mjs | `175de6ba…` | `e9a21b44…` |

Full 64-hex values are in the manifest (each row also carries its
`pinned_source` line anchors). `derived_from` records
`tameshi-shokunin/tools/mutate-and-run.sh` sha256
`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`, so drift
in the shared runner node is detectable.

Per L1 scope, the committed manifest is the **configured pin authority**, not a
hardcoded adversarial baseline-authentication gate. The probe enforces the six
canonical leg IDs, exact repo/path, full 40-hex commit and full 64-hex digest
formats, but it does not embed production pins or re-derive them from the
runner at runtime. This preserves isolated synthetic-repo CLI fixtures. Main
cross-checks the delivered manifest against the unchanged runner and records
the runner sha256 at the measured commit; a changed manifest is a changed
baseline, not safe reuse.

Cross-check performed here (fact commands, not the selftest): the runner digest
equals `75ed934d…`; each of the six manifest `expected_sha256` values occurs in
`tools/mutate-and-run.sh`; the six `pinned_commit` values occur there too
(`mado`/`checklist` digests appear twice: `PIN_*` plus an embedded spec comment).

## CLI and output contract

```
pin-disposition.py --manifest PATH --root FLEET
pin-disposition.py --selftest
pin-disposition.py --help
```

One JSON document on stdout. Exit map: **0** for observations, including drift
and `unavailable` legs; **2** for could-not-evaluate input (usage, missing/
unreadable/schema-invalid manifest, fleet root not an existing directory), also
emitted as JSON (`.error.kind`, `.error.message`, empty `.legs`).

Document fields: `schema`, `tool`, `tool_sha256`, `status` (`ok` /
`invalid_input`), `observed_at` (one UTC instant), `manifest`, `root`,
`result_reuse` + `result_reuse_reason`, `not_compared`, `counts`, `legs[6]`.

Each row keeps the three observations separate:

- `pinned`: recorded `commit`, `expected_sha256`, the sha256 actually read at
  that commit (`blob_sha256`), `status` `verified|mismatch|unavailable`, reason.
  A wrong manifest digest is never silently accepted: the pinned blob is read
  from the repo object store and compared.
- `head`: current `commit`, sha256 of the path's blob at HEAD (`blob_sha256`),
  `status` `present|absent|not_blob|unavailable`, reason.
- `worktree`: absolute path, current bytes sha256, `status`/`reason`.
- `content_status`: `unchanged|changed|unavailable` (mirrors `worktree.status`).
- `result_reuse`: literal `not_established` on **every** row, including
  unchanged rows. There is no code path deriving it from status.

`unchanged` requires all three: readable regular worktree file, **verified**
pinned evidence, and byte equality with `expected_sha256`. Missing repo, path,
commit or blob, a pin mismatch, a symlink or a non-regular file can never be
`unchanged`; they are `unavailable` with the specific reason. HEAD differing
from the pin does not change a byte-equal worktree disposition; HEAD is reported
beside it, not substituted for it.

`not_compared` is a static literal list: mode/exec-bit, runner/defect-spec
version, suite command/harness, interpreter/toolchain, environment,
dependencies, fixture/companion files, timeouts. `content_status` is raw bytes
only; a chmod-only change with identical bytes stays `unchanged` while
`result_reuse` stays `not_established` and mode remains visibly unmeasured.
Main owns the mode caveat and the historical executable-bit counterexample.

## Read-only / identity guards

- Only read-only plumbing: `rev-parse`, `cat-file -t`, `cat-file blob`. No
  `status`, `diff`, `hash-object`, no index refresh, no filters/hooks.
- Inherited `GIT_*` env scrubbed; `GIT_CONFIG_NOSYSTEM=1`,
  `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0`,
  `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`; argv lists, no shell; 30 s
  timeout per git call.
- Repo identity is proven: `git rev-parse --show-toplevel` must equal the leg
  repo's real path. This is required because the fleet root is itself a git
  repo; a plain directory under it cannot borrow the super-repo HEAD.
- Manifest validation: exactly the six canonical IDs, exact recorded repo and
  path, full 40-hex commit, full 64-hex sha256, no duplicate, unknown, omitted
  or renamed leg → exit 2.
- Worktree bytes: `lstat` + `O_NOFOLLOW`, regular file only, real path must stay
  inside the leg repo, and the opened `fstat` must match the `lstat` identity
  (`st_dev`,`st_ino`) so an intermediate-component swap cannot escape; a
  symlink cannot leak an arbitrary file digest.
- No target/sibling repo or worktree write path exists.

## Selftest arms (isolated CLI; not executed here)

Fixtures are created under `tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir="/tmp")`
and exercised only through `sys.executable <tool> --manifest … --root …`.
Fixture fleet is a synthetic **super-repo** containing a nested kumitate repo, a
nested kagi repo, a non-repo `tsukuroi-shokunin/` directory, and no
`mado-shokunin/`; no real sibling path is read. Fixture git env is scrubbed;
hooks/templates directories are empty; global/system config bypassed. Expected
labels are literal constants (`SELFTEST_V1_SHA256` etc.).

| case | exit | literal expectation highlights |
|---|---|---|
| `unchanged` | 0 | content `unchanged`; pinned `verified`; head `present`; pin/head/worktree sha = V1 |
| `changed-head` | 0 | content `changed`; pinned commit ≠ head commit; pinned blob V1, head/worktree V2 |
| `dirty-worktree` | 0 | content `changed`; head blob V1, worktree DIRTY literal; head commit == pin |
| `missing-worktree-file` | 0 | content `unavailable`; pinned `verified`; head `absent`; worktree sha null, reason `worktree_missing` |
| `missing-repo` | 0 | all `unavailable`, reason `repo_missing`; worktree sha null |
| `foreign-repo-toplevel` | 0 | all `unavailable`, reason `repo_foreign`; worktree sha null (super-repo not borrowed) |
| `missing-pinned-blob` | 0 | pinned `pinned_path_missing`; content `unavailable`; worktree `pin_not_verified` though bytes = V1 |
| `missing-pinned-commit` | 0 | pinned `pinned_commit_missing`; worktree `pin_not_verified` |
| `pinned-blob-mismatch` | 0 | pinned `mismatch` + reason `pinned_blob_mismatch` (observed V1, expected V2); content `unavailable`; worktree `pin_not_verified` |
| `worktree-outside-repo` | 0 | intermediate `scripts` symlink to a temp dir outside the repo; content `unavailable`, worktree sha null, reason `worktree_outside_repo` |
| `worktree-symlink` | 0 | target file replaced by a symlink; content `unavailable`, worktree sha null, reason `worktree_symlink`; pinned `verified`, head `present` |
| `repo-symlink` | 0 | canonical repo name replaced by a symlink; all reasons `repo_symlink`, worktree sha null |
| `malformed-digest` | 2 | `invalid_manifest`, message contains `expected_sha256`, no rows |
| `duplicate-leg` | 2 | `invalid_manifest`, `duplicate leg` |
| `missing-leg` | 2 | `invalid_manifest`, `omits recorded leg` |
| `malformed-json` | 2 | `invalid_manifest`, `not valid JSON` |
| `missing-manifest` | 2 | `invalid_manifest`, `manifest not found` |
| `invalid-root` | 2 | `invalid_root`, `fleet root` |

Every successful arm additionally asserts six rows, `status=ok`, top-level and
all-row `result_reuse=not_established`, `not_compared` contains
`mode/exec-bit`, and `observed_at` ends in `Z`. Expected summary on success:
18 × `SELFTEST_CASE … PASS` and `SELFTEST: PASS (18/18)`, exit 0. On FAIL the
`/tmp` fixture root is kept and printed; on PASS it is removed.

## Exact checks L1 should run (not run here)

1. Syntax: `python3 -m py_compile /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py` → exit 0.
2. Selftest: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py --selftest` → exit 0, 18 PASS, `SELFTEST: PASS (18/18)`; the output must include `SELFTEST_CASE worktree-outside-repo PASS`, `worktree-symlink PASS`, `repo-symlink PASS` and `pinned-blob-mismatch PASS`.
3. Live read:
   `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`
   → exit 0; six canonical rows; counts sum 6; every row
   `result_reuse=not_established`; every pinned row `verified` unless that
   repo/rev is absent (then `unavailable` + reason, never `unchanged`); capture
   the JSON if it is to be committed as evidence.
4. No-write check (only coverage for the absent zero-mutation arm): before and
   after check 3, record the four sibling repos' `rev-parse HEAD` and a `.git`
   snapshot (e.g. `find .git -newer <marker>` or index/objects counts); nothing
   in any `.git` or worktree may change.
5. Env-scrub check: rerun check 3 with
   `GIT_DIR=/home/vgpnk/Projects/shokunin/.git` exported; the six rows must
   match check 3 exactly apart from `observed_at`.
6. Provenance: `sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` → `75ed934d…` matching `derived_from`; confirm each manifest `expected_sha256` still occurs in the runner.
7. Confirm the live document's six `pinned.commit`/`expected_sha256` pairs equal
   the manifest (the tool validates manifest repo/path and formats but treats
   the committed manifest as the configured pin authority; L1 should eyeball
   the pins against `mutate-and-run.sh:542-553` once).

Peer-reported coordinates at differing instants (not executed or retained by
this seat, offered only for L1 reconciliation): kimi/tsukuroi/mado peer seats
report `changed`; surface/checklist/claims peer seats report `unchanged`; all
report `result_reuse=not_established`. The live read above is authoritative.

## Deliberate omissions / residual unknowns

- Mode/exec-bit is **not measured** (raw-byte disposition only; listed in
  `not_compared`). A 100755→100644 chmod with identical bytes reads
  `unchanged`; no reuse is implied. The round-10 executable-bit counterexample
  is documented by Main, not claimed here.
- No `head_vs_pin`, `head_vs_worktree` or ancestry fields. The three SHAs are
  emitted separately so L1 can derive stale-vs-drift without a second
  vocabulary; adding them was outside the assigned minimal three-way disposition.
  A `changed` row must not be called stale without a separate ancestry read.
- Multi-repo read is not atomic: `observed_at` is stamped after the rows are
  read (end-of-window marker); per-row `head.commit` is the exact commit read,
  and a sibling HEAD can move during the window.
- The committed manifest is the configured pin authority; the probe does not
  authenticate it against the runner at runtime. Main cross-checks the delivered
  manifest against the unchanged runner (`derived_from.sha256` is provenance,
  not enforced by the probe). A changed manifest is a changed baseline, not safe
  reuse.
- Canonical repo/path is embedded in the tool and enforced against the
  manifest. If `mutate-and-run.sh` changes a leg, tool + manifest must update
  together.
- A nonzero `git cat-file -t` is classed as path-absent (`pinned_path_missing`
  / `head_path_absent`); a corrupt object-store error would share that reason.
  Content is `unavailable` either way, so this is reason precision only.
- A symlinked or out-of-root repo/worktree file is `unavailable` by design; the
  selftest arms exercise repo/worktree symlinks and intermediate-directory
  escape. There is no zero-mutation/`.git`-snapshot arm and no env-scrub arm
  (an inherited `GIT_DIR` is scrubbed in code but not asserted by `--selftest`).
- If git is absent, repo identity cannot be proven: git-derived fields and the
  worktree hash are `unavailable` (the probe does not hash worktree bytes
  without repo identity), and `--selftest` prints `COULD_NOT_EVALUATE` exit 2.
