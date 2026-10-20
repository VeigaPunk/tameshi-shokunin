# PinSecurity — round 13 w1 (sentinel, read-only)

Seat `TameshiR13.PinSecurity`. Surface: `tools/pin-disposition.py` (reviewed
bytes sha256 `1fea5b9efed5e114e9d33f516eec1b1bd02c85ba3483cd239866ef03866c09f2`,
1141 lines; line anchors below refer to these bytes) and
`.ufo/evidence/round-13/pin-manifest.json`. No selftest, probe run, gate,
build, lint or formatter executed. No tool installed/upgraded. Only
read-only git facts were run (version, `rev-parse --verify`, `--show-toplevel`,
local config keys, super-repo `ls-files`/`check-ignore`).

Axes: path traversal · git option/command execution · sibling writes/commands ·
secret disclosure · provenance honesty.

## Verdict

No High/Medium. Three Low defects (guards unpinned by selftest, zero-mutation
unproven, worktree TOCTOU), one report-accuracy defect, two Info. Defects were
routed to `TameshiR13.PinProbe` before and after landing; the pre-landing
guidance (super-repo discovery, `--output` injection, index/filter
side-effects, symlink digest leak, selftest git isolation) is reflected in the code.

**Remediation status (re-read, bytes sha256
`297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`, 1247 lines;
findings below keep their original-byte anchors):**
L1 resolved — arms `worktree-outside-repo` (intermediate `scripts` symlink to
`<scratch>/outside-scripts`), `worktree-symlink`, `repo-symlink` assert reason +
`sha256 None` + `unavailable` (:1056-1123). L3 resolved — post-open
`(st_dev, st_ino)` must equal the lstat entry, else `worktree_replaced`
(:386-391); that branch has no selftest arm (race not deterministically
fixturable; accepted). I1 resolved — `GIT_NO_LAZY_FETCH=1` (:206). R1 resolved —
`PinProbe.md:206-208`. **L2 open**, disclosed by the owner as a residual
(`PinProbe.md:203-205`); L1 checks 3-4 below are its only coverage this round.

## Closed surfaces (grounded)

| Axis | Evidence |
|---|---|
| Path traversal | repo/path are constants `CANONICAL_LEGS` (:122-130); manifest repo/path must equal them (:516-530); `repo_identity` refuses symlinked repo and requires `dirname(realpath)==root_real` (:241-247). `--root` cannot steer outside `<root>/<fixed name>`. |
| Super-repo borrowing | Fleet root `/home/vgpnk/Projects/shokunin` is itself a git repo (HEAD `168fcf6`; siblings ignored via `.gitignore:1 *-shokunin/`). Guard: `--show-toplevel` must equal repo realpath (:248-257); selftest arm `foreign-repo-toplevel` (:969-986) uses a synthetic super-repo. |
| Git option injection | `pinned_commit` must fullmatch 40-hex (:531); objects are `<hex>:<constant path>` (:280,321); `--end-of-options` before revs (:273,311) — confirmed accepted by local git 2.55.0 (`rev-parse --verify --quiet --end-of-options 175de6…^{commit}` → rc 0). No `git show` (`--output=<file>` write vector absent). |
| Command execution / sibling writes | Only `rev-parse` and `cat-file -t/blob` (:248,273,281,289,311,322,334): no index refresh, fsmonitor, filters (global `filter.lfs.process` is configured on this host), hooks, or lock writes; `GIT_OPTIONAL_LOCKS=0`, inherited `GIT_*` scrubbed, global/system config bypassed, argv list, no shell, 30 s timeout (:191-225). No gate/suite execution; probe's only output is stdout (:165-166). |
| Selftest isolation | `mkdtemp(dir="/tmp")` (:593); fixture git with `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `HOME=scratch`, empty `init.templateDir`/`core.hooksPath`, `commit.gpgsign=false` (:638-677); CLI cases `cwd=scratch` (:812-821). No fleet path read. |
| Secret disclosure | Output is digests, commits, absolute paths, reasons; no file bytes; JSON errors give line/column only (:478-482). Worktree: lstat refuses symlink/non-regular, realpath containment, `O_NOFOLLOW`, `fstat` regular (:350-380). |
| Provenance | All six manifest `pinned_commit`/`expected_sha256` equal `REV_*`/`PIN_*` in `tools/mutate-and-run.sh:542-553` (recomputed here); `derived_from.sha256` `75ed934d…adc5` equals the runner's current bytes. Fixture constants `SELFTEST_*_SHA256` (:586-588) equal sha256 of their literal bytes. |

## Findings

**L1 · Low — security guards unpinned by `--selftest`.** Exploit path: a later
edit drops the lstat/containment checks (:241-242, :358-366); `--selftest`
still reports 14/14 because no arm creates a symlink. Then a sibling-tree
symlink `scripts/kimi-census.mjs -> ~/.config/<secret>` or an intermediate
`scripts -> /elsewhere` publishes an arbitrary file's sha256 (offline-guessable
for low-entropy secrets) and could label it `changed`. Impact: silent loss of
the stated "a symlink cannot leak an arbitrary file digest" guarantee
(docstring :75-76). Remediation: three arms — final-component symlink →
`worktree_symlink`, intermediate dir symlink to `<scratch>/outside` →
`worktree_outside_repo`, symlinked repo dir → `repo_symlink`; each asserts
`sha256 == None`, `content_status == "unavailable"`.

**L2 · Low — read-only claim and env scrub unproven.** Docstring :67-72
asserts no writes and scrubbed `GIT_*`; no arm proves either. Exploit path: a
regression to `git status`/`diff` (index refresh writes `.git/index`) or
dropping the scrub (inherited `GIT_DIR` redirects every leg to one repo,
fabricating HEAD provenance) passes selftest. Remediation: hash each fixture
repo's `.git` tree (refs, index presence/bytes, object list) before/after the
CLI cases and assert equal; run one case with `GIT_DIR=<fleet>/.git` in the
child env and assert rows identical to the base run.

**L3 · Low — TOCTOU between containment check and open.** `realpath` check
(:364) precedes `os.open` (:369); `O_NOFOLLOW` protects only the last
component, so swapping an intermediate directory to a symlink in that window
escapes containment. Needs a concurrent writer in a sibling tree (operator
trust zone), hence Low. Remediation: after open, require
`(st_dev, st_ino)` of `os.fstat(fd)` equal the `lstat` entry from :351.

**R1 · Report accuracy (owner report, not code).** `PinProbe.md:177-179`
states that with git absent the probe "still hash[es] readable worktree bytes"
and the selftest reports `CANNOT_EVALUATE`. Code: `repo_identity` returns
`git_unavailable` before any hash and `evaluate_leg` emits `sha256: None`
(:248-250, :401-424); selftest prints `SELFTEST: COULD_NOT_EVALUATE` (:1069).
Fail-closed either way; the prose overstates observed behavior.

**I1 · Info — lazy fetch.** In a partial clone, `cat-file` of a missing object
triggers a promisor fetch (network + writes to sibling `.git/objects`). No
sibling currently carries `remote.*.promisor`/`extensions.*` (checked
kumitate/kagi/tsukuroi/mado local config), so no live exposure. Hardening: add
`GIT_NO_LAZY_FETCH=1` to `git_env` (:194-203).

**I2 · Info — operator-chosen input echo.** Duplicate-key (:457) and
repo/path mismatch (:520-529) messages echo manifest key/values; `git` resolves
via inherited `PATH`. Both require the operator's own `--manifest`/env; no
change needed.

## Checks for L1 (not executed here)

1. `python3 -m py_compile /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py`
2. `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py --selftest` → exit 0, `SELFTEST: PASS`, and no `/tmp/tameshi-r13-pin-disposition-selftest.*` left behind on PASS.
3. Zero-mutation around the live read: record `git -C <repo> rev-parse HEAD`, `stat -c '%Y %s' <repo>/.git/index`, and `find <repo>/.git -newer <marker>` for the four sibling repos; run
   `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`
   → exit 0, six rows, every `result_reuse == "not_established"`; re-record and require identical values and no newer files.
4. Env-scrub spot check: the same live command with `GIT_DIR=/home/vgpnk/Projects/shokunin/.git` exported must produce rows identical to check 3 (minus `observed_at`).
5. Invalid input: `--manifest /dev/null --root /home/vgpnk/Projects/shokunin` → exit 2, `status: invalid_input`, `legs: []`.
6. In check 2 output, confirm `SELFTEST_CASE worktree-outside-repo PASS`, `SELFTEST_CASE worktree-symlink PASS`, `SELFTEST_CASE repo-symlink PASS` are present; checks 3-4 are mandatory because L2 has no selftest arm.
