# X03RegistryCheck — tools/registry-check.py (contract B, R16-MON1)

## Deliverable

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py` (new file; new path, so written directly, not staged)
- sha256: `60b0f5032aade3d2d55f46e37a43ce0816c46a57ce992ee47d64a26e47237b51`
- Python stdlib only. `git` subprocess used only for `--rev` (and the selftest's `--rev` fixtures).

## Behaviour implemented (per contract B)

- Loads `tools/registry.json` (schema `tameshi-entry-registry-v1`) from the lane containing the script by default; `--root DIR` overrides the lane, `--registry PATH` overrides the file (resolved against caller cwd — usable with `--rev` to grade an old rev against the newer registry).
- Runs each `status == "active"` row with `cwd` = lane root, `shell=False`, `stdin` /dev/null, per-row `timeout_s`. Row holds iff `exit == expect.exit` AND every `expect.stdout_contains` needle appears in stdout (UTF-8, errors=replace). Non-active rows are schema-validated, printed `skipped`, and excluded from N/M.
- Output: `ROW <name> expect=<exit> got=<exit|timeout|unavailable> held|differs` + `REGISTRY_CHECK: held=N/M`. Exits: 0 all held, 1 any differs, 2 could-not-evaluate (unreadable/invalid registry incl. bad schema / duplicate names / non-list argv, `--only` miss, rev missing, clone failure), 64 usage.
- `--rev REV`: mkdtemp under /tmp, `fleet/` dir with a symlink per `*-shokunin` sibling of the lane (lane excluded), `git clone -q` of the lane + `git checkout -q REV` — matches the wave fleet-mirror recipe so tools resolving sibling lanes still work. Workdir removed in `finally` (verified: `ls -d /tmp/tameshi-registry-check-*` → no matches after the run).
- `--only NAME`, `--json` (report schema `tameshi-registry-check-report-v1` on stdout; human lines to stderr; report includes per-row got/held, skipped flags, held/total, exit).
- `--selftest`: hermetic under `tempfile.mkdtemp`, synthetic registries + a synthetic git lane; cleaned up in `finally`.

## Evidence

Selftest (covers every acceptance bullet):

    $ python3 tools/registry-check.py --selftest
    SELFTEST_CASE all-held PASS (exit=0 out=['REGISTRY_CHECK: held=2/2'])
    SELFTEST_CASE one-differs-exit PASS (exit=1)
    SELFTEST_CASE stdout-contains-missing PASS (exit=1)
    SELFTEST_CASE timeout-differs PASS (exit=1)
    SELFTEST_CASE invalid-schema PASS (exit=2)
    SELFTEST_CASE duplicate-names PASS (exit=2)
    SELFTEST_CASE shell-string-argv PASS (exit=2)
    SELFTEST_CASE unreadable-registry PASS (exit=2)
    SELFTEST_CASE rev-unknown PASS (exit=2)
    SELFTEST_CASE rev-clone-held PASS (exit=0)
    SELFTEST_CASE only-filter PASS (exit=0)
    SELFTEST_CASE only-missing PASS (exit=2)
    SELFTEST_CASE usage-unknown-flag PASS (exit=64)
    SELFTEST_CASE usage-selftest-extra PASS (exit=64)
    SELFTEST_CASE json-report PASS (exit=1)
    SELFTEST: PASS (15 cases)
    exit 0

`rev-unknown` uses rev `000...0`; `rev-clone-held` proves the fleet-mirror clone+checkout path end-to-end. `all-held` includes a `status="parked"` row printed `skipped` and excluded from `held=2/2`.

Real one-row run (`repeat-control.py --selftest` via `/tmp/tameshi-r17-one-row.json`, timeout 120, expects exit 0 + `SELFTEST: PASS`):

    $ python3 tools/registry-check.py --registry /tmp/tameshi-r17-one-row.json
    ROW repeat-control-selftest expect=0 got=0 held
    REGISTRY_CHECK: held=1/1
    exit 0

    $ python3 tools/registry-check.py --rev 98bea7da5801f4bc58e4187690ee1687c8a5061f \
          --registry /tmp/tameshi-r17-one-row.json
    ROW repeat-control-selftest expect=0 got=0 held
    REGISTRY_CHECK: held=1/1
    exit 0   (0.75s; clone is hardlinked, mkdtemp removed)

`--json` on the real row: stdout parses to `tameshi-registry-check-report-v1` with held=1 total=1 exit=0; human lines on stderr.

## Design decisions worth flagging to L1

- Rows missing required fields (name/kind/argv/expect/timeout_s/source/status) are invalid — the contract row shape is treated as all-present except `expect.stdout_contains`.
- `status != "active"` rows are validated but skipped and excluded from the denominator; a registry of only skipped rows yields `held=0/0` and exit 0 (vacuously all held).
- `got=unavailable` (OSError, e.g. argv[0] missing) is a `differs`, exit 1 — the command failed to return its registered outcome, which is what the monitor measures.
- Exit 2 vs 64 boundary: anything about the *inputs* (registry, rev, --only name) is 2; only CLI-shape errors are 64.

## Risks / blockers

- None blocking. The real `tools/registry.json` is being written in parallel; the tool was not run against it.
- If X-siblings write rows with `kind` values outside `gate|probe|selftest` or omit `source`, the schema check will 2 — coordinate the row shape.

## Tooling

- No installs. Python 3 stdlib + system git.

## Verdict

built — registry-check.py implements contract B; 15/15 selftest cases pass; live and `--rev` one-row runs held.

## Follow-up

Hardened per K04RegistrySelfFulfilling.md (P1-P8 where tool-side), R04ReviewContractB.md
(§1.1, 1.3, 1.5, 1.6, 2, 3.4-3.5) and N01TraceGitSafety.md (F1-F3, F7, F8, F15) plus the
L1 addendum (rev resolution, name regex, process groups, selftest env scrub).
No lane git writes were run. Final file sha256:
`0bf9d1d2971c9fe478823754c7b889315585b73361ee3146631f409c4c5a3765`.

### Mapping of the requested items

1. **GIT_* scrub.** `git_env()` copies `os.environ` minus every `GIT_*` key, then sets
   `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0`,
   `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1`, `GIT_PAGER=cat`, `LC_ALL=C`
   (same shape as `pin-disposition.py:197-211`). It is used by the tool's own git calls
   (`resolve_rev`, clone, checkout, HEAD verify) and by the selftest's fixture git calls;
   rows get `row_env()` = `git_env()` + `PYTHONDONTWRITEBYTECODE=1`.
   Selftest cases: `gitdir-scrub-rev` (GIT_DIR exported while `--rev` runs → canary HEAD and
   source HEAD unchanged), `gitdir-scrub-row` (GIT_DIR+GIT_WORK_TREE exported, row runs
   `git init/add/commit` in a fixture repo → canary HEAD unchanged, fixture repo gets its own
   `.git`).
2. **Process group.** Rows run via `Popen(start_new_session=True)`; on timeout `_kill_group`
   sends SIGTERM to the pgid, waits 5 s, SIGKILLs the pgid, then drains. Selftest case
   `timeout-kills-group`: row spawns a grandchild that writes a marker only after sleeping;
   after the timeout the marker is absent and the row reports `got=timeout`.
3. **`superseded`.** Status enum `{active, superseded}`; other values → exit 2. `superseded_by`
   is required and must name an existing **active** row (second validation pass) → otherwise 2.
   Superseded rows still RUN and print `ROW <name> superseded expect=<e> got=<g>`; they are
   excluded from N/M and reported as `REGISTRY_CHECK: held=N/M superseded=K` (K always printed).
   Cases: `superseded-runs-excluded`, `superseded-target-missing`, `superseded-target-not-active`,
   `superseded-by-required`.
4. **Tags.** Optional `tags: [str]`; `--tag TAG` repeatable, OR-selection; `superseded_by`
   targets resolve against the full registry (not the filtered set). `--only` + excluding
   `--tag` is exit 2, not an empty pass. Cases: `tag-selects-any`, `tag-repeatable`, `tag-miss`,
   `only-tag-conflict`.
5. **`source` format.** `^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$`, else exit 2. Case:
   `invalid-source` (free-text source). Existing smoke registry updated to
   `SKILL.md@98bea7da5801f4bc58e4187690ee1687c8a5061f:1503`.
6. **JSON provenance.** Report now carries `registry_sha256`, the resolved `registry` path,
   `root` actually graded, `rev` + `rev_resolved` (40-hex commit), `live`, `only`, `tags`,
   `held/total/superseded/exit`, and per row `elapsed_s`, `stdout_tail`, `stderr_tail`
   (last 4 KiB, UTF-8 errors=replace), `tags`, plus `superseded_by` / `non_hermetic_argv`
   where applicable. Cases: `rev-resolved-reported`, `json-report`.
7. **Live-root warning.** Every non-`--rev` run writes
   `registry-check: warning: live --root mode runs rows in the lane; rows may write into the
   root (use --rev to grade a throwaway clone)` to stderr. Case: `live-root-warning`
   (asserts the phrase on stderr, not stdout).

Addendum extras: `--rev` now resolves `REV^{commit}` with
`git rev-parse --verify --quiet --end-of-options`, clones with `--no-hardlinks`,
`-c core.hooksPath=/dev/null`, checks out `--detach <sha>` and asserts `rev-parse HEAD` equals
the resolved sha (cases `rev-path-like`, `rev-option-like`, `rev-unknown`,
`rev-clone-held`); row names must match `^[a-z0-9][a-z0-9-]*$` (case `invalid-name`).

Additional from R04/N01/K04 adopted tool-side: non-hermetic argv detection — under `--rev`,
an absolute argv token at/under the live fleet root marks the row `got=non-hermetic` and
differs **unless** the row declares `external: true` (K04 P7), in which case it still runs and
the tokens are reported in `non_hermetic_argv` (cases `rev-non-hermetic-argv`,
`rev-external-declared`); nonexistent `--root` → exit 2 `root_unavailable`; SIGTERM handler
raises `SystemExit` so the `finally` removes the clone.

### Commands / exits

    $ python3 -m py_compile tools/registry-check.py            # 0
    $ python3 tools/registry-check.py --selftest               # 0, "SELFTEST: PASS (34 cases)"
      (new cases: gitdir-scrub-rev, gitdir-scrub-row, timeout-kills-group,
       superseded-runs-excluded, superseded-target-missing, superseded-target-not-active,
       superseded-by-required, tag-selects-any, tag-repeatable, tag-miss,
       invalid-status, invalid-name, invalid-source, rev-path-like, rev-option-like,
       rev-resolved-reported, rev-non-hermetic-argv, rev-external-declared,
       only-tag-conflict, live-root-warning)

    # decoy-GIT_DIR acceptance (N01 F1 red-before): canary repo HEAD
    $ GIT_DIR=$S/canary/.git GIT_WORK_TREE=$S/canary \
        python3 tools/registry-check.py --selftest
      selftest_exit=0  canary_before=3a47ca8f… canary_after=3a47ca8f… stable=YES
      SELFTEST: PASS (34 cases)

    # real one-row registry (repeat-control --selftest), live root
    $ python3 tools/registry-check.py --registry /tmp/tameshi-r17-one-row.json
      registry-check: warning: ... (stderr)
      ROW repeat-control-selftest expect=0 got=0 held
      REGISTRY_CHECK: held=1/1 superseded=0      exit 0

    # same row at the pinned rev, JSON
    $ python3 tools/registry-check.py --rev 98bea7da5801f4bc58e4187690ee1687c8a5061f \
          --registry /tmp/tameshi-r17-one-row.json --json
      held=1 total=1 superseded=0 rev_resolved=98bea7da5801f4bc58e4187690ee1687c8a5061f
      registry_sha256=57c9dac341c9… got=0 elapsed_s=0.737      exit 0, 0.86 s
      (mkdtemp removed: `ls -d /tmp/tameshi-registry-check-*` → no matches)

### Coordination notes for the registry author / L1

- Rows whose argv keeps an absolute live-fleet path (e.g. `pin-disposition-read`'s
  `--root /home/vgpnk/Projects/shokunin`) must declare `"external": true` or they will report
  `got=non-hermetic` and count as differs under `--rev`. This is deliberate (N01 F8), and
  K04 P7's separate reporting is preserved via `non_hermetic_argv` in JSON.
- Every `source` must be `<file>@<7-40 hex>:<line>[-<line>]`; the free-text placeholders that
  R04 §4 flagged will now fail validation with exit 2.
- `--rev` without `--registry` reads the clone's own `tools/registry.json`; before this round
  lands that file does not exist at any rev, so the C2 counting command must pass `--registry`.
- K04 P1/P3/P4/P5/P8 are registry/manifest-side (fills, expectation citations, partition
  reporting, discriminating needles, historical_inputs minimality); they are not enforceable
  from this tool and remain with X04/X13/X02.
- `--rev` requires the commit to be reachable from a ref in the source lane (the clone fetches
  refs only); a dangling sha exits 2 with a clear checkout error.
- Row stdout is fully buffered for needle matching (`communicate`); only the report tails are
  bounded. If a noisy row is a concern, that is a separate change with a documented cap.

