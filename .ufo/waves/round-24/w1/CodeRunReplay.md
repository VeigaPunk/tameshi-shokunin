# CodeRunReplay — review of `run_replay()` (`tools/registry-replay.py`), round 24

Scope (as assigned): the clone HEAD check, the sibling symlink set derived from
`plan()`, the runner digest taken from the clone copy, and the observations
content; compared against
`.ufo/evidence/round-24/replay/observations.json` and the round-23 instrument
`.ufo/evidence/round-23/replay.py`. Lane: leaf reviewer, read-only, no
subagents, no execution of the tool (my item is not a "Run" item). Every
execution claim below is cited from a recorded receipt or from read-only
git/JSON inspection — nothing was re-run.

## Verdict

**Conditional pass on the four named surfaces; the published replay/bundle pair
over-claims in three concrete ways (F1, F2, F3) and the whole `--run` path is
outside the frozen counter's reach.**

The four surfaces I was asked to review are implemented as documented, and the
recorded evidence is internally consistent with the code: the clone HEAD check
is real and the recorded revision matches the requested one; the sibling set is
exactly the fleet's 20 `*-shokunin` lanes; the runner digest is taken from the
clone copy and equals the bytes that executed; the observations carry a
complete, well-formed row set (43/43 held, no cleanup error, no stream over
limit).

What is *not* supported by the evidence:

* the published bundle certifies two rows that are **not** revision-pinned, and
  the certifying consumer cannot see that (F1);
* the replayed requirement set is the **round-23** frozen set (43 rows) while
  the delivered registry requires **47**, and the replay ran at `d2eaecd`, not
  the delivered `c8c5b88` (F2);
* a refusal leaves the **previous** run's `bundle.json`/`expected.json` in
  `--out`, so a consumer can read a passing binding for a refused replay (F3).

Calibration: `measure.py` drives only `--project` and `--plan` on synthetic
fixtures (`measure.py:161-200`; the contract's own bound says "K7-K11 test the
new projection/plan CLI on synthetic fixtures; an actual replay run is separate
evidence"). **Every surface named in my assignment therefore sits outside the
eleven frozen predicates**; the only evidence for them is one unrepeated
execution (`replay-command.json`, 2026-10-21T15:56:41→16:01:02Z) at a
non-delivered revision. The 11/11 count should not be read as "the replay path
is hardened end-to-end".

Axes I priced (kept any move that improves one and harms none):
A. fidelity — does the code produce what `observations.json` says?
B. honesty — does the artifact under certification match its own claims?
C. coverage — is the named surface measured by the frozen counter?
D. failure hygiene — exit codes and stale artifacts.

## Findings by severity

### F1 — HIGH — live-dependent rows are published into the binding bundle indistinguishably from revision-pinned receipts

Code: `tools/registry-replay.py:100` (live list), `:101-104` (**every** row is
appended to `requirements`/`receipts`), `:107` (`revision_pinned` = receipts −
live), `:116-129` (`publish` writes `bundle.json`/`expected.json` whenever a
bundle exists — the live set does not shrink the bundle).

Evidence (all read from the shipped files):

* `.ufo/evidence/round-24/replay/live-dependent.json` →
  `live_dependent: ["pin-disposition-read","verify-round15"]`,
  `revision_pinned: 41`, `rows: 43`.
* `.ufo/evidence/round-24/replay/bundle.json` → **43** receipts, including
  `pin-disposition-read` with
  `argv: ["python3","tools/pin-disposition.py","--manifest",".ufo/evidence/round-13/pin-manifest.json","--root","/home/vgpnk/Projects/shokunin"]`,
  `exit: 0`, `cwd: "/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin"`,
  `revision: "d2eaecd443bf5f4e387e7e5331282e3d11dea047"`.
* The same row's `runner_result` in `observations.json` carries
  `non_hermetic_argv: ["/home/vgpnk/Projects/shokunin"]` — i.e. the command
  read the **live fleet root**, not the clone.
* `tools/command-binding.py:105-120` checks only `receipt['revision'] ==
  bundle['revision']` and `receipt['cwd'] == bundle['cwd']`; it never reads
  `live-dependent.json`. `.ufo/evidence/round-24/replay-gate.json` records
  `exit: 0`, `finding_ids: []` over exactly that bundle.

So one `--out` directory simultaneously asserts "41 revision-pinned" (side
file) and "43 revision-bound receipts, all at `d2eaecd`, all in the clone cwd"
(bundle), and the gate certifies all 43. The tool docstring
(`tools/registry-replay.py:16-18`) claims live-dependent rows are "listed in
`live_dependent` **instead of** being silently reported as revision-pinned" —
true of the report, false of the artifact the report's bundle feeds.

K10 (`measure.py:186-190`) only inspects the *report* surface
(`report.get('live_dependent')`), so the frozen predicate cannot discriminate
this: it would still be 11/11 with the bundle defect in place.

Smallest safe correction: in `project()`, exclude the live-dependent names from
**both** `requirements` and `receipts` (identical name sets, so
`command-binding.py`'s `MEMBERSHIP_MISMATCH` cannot fire) and keep the excluded
names in `live-dependent.json`; or, if the bundle must retain them, refuse
publication with a new finding (e.g. `RUNNER_LIVE_DEPENDENT`) instead of
publishing a bundle whose revision claim is false for 2 of 43 receipts.

### F2 — MEDIUM-HIGH — the replayed set is the round-23 baseline (43), not the delivered registry's active set (47); and the run predates the delivered revision

* `tools/registry.json` at HEAD `c8c5b88`: 54 rows, **47 active**. The
  round-23 baseline (`.ufo/evidence/round-23/registry-baseline.json`) has **43**
  active, all still active at HEAD. Active at HEAD but **not** in the replayed
  set: `command-binding-frozen-clean-pinned`, `command-binding-selftest-r24`,
  `command-binding-source-read-red-pinned`, `registry-replay-selftest`.
* The replayed requirement names are exactly the 43 baseline names
  (`observations.json` `rows[].requirement.name`).
* `observations.json` `revision` = `d2eaecd443bf5f4e387e7e5331282e3d11dea047`;
  the delivered implementation revision is `c8c5b88c8e96…`. `git diff --stat
  d2eaecd HEAD -- tools/` is **empty**, and
  `runner_sha256_clone_copy` = `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad`
  equals `sha256sum tools/registry-check.py` and both
  `git show d2eaecd:tools/registry-check.py` and
  `git show HEAD:tools/registry-check.py`. So the **runner bytes are identical**
  and only the *requirement set* and the *revision label* lag.
* No active registry row references `.ufo/evidence/round-24/replay/bundle.json`
  (the two pinned rows bind the **round-23** bundle,
  `.ufo/evidence/round-23/replay/bundle.json`,
  `tools/registry.json` argv scan). The new round-24 bundle is published but
  pinned by nothing.

Consequence: the wave's binding evidence covers 43 of the 47 currently
required commands, at a revision one wave behind the delivered one, and the
new tool's own `registry-replay-selftest` row is neither replayed nor bound.
The gate receipt (`replay-gate.json`, exit 0) therefore certifies a *stale
subset* as a clean binding.

Smallest safe correction: re-run `--run` at `c8c5b88` with a baseline
regenerated from the delivered `tools/registry.json` (47 active rows) and add
one active registry row pinning the resulting `bundle.json` +
`expected.json` digest; until then, state the bound set explicitly as "43
round-23 rows at `d2eaecd`".

### F3 — MEDIUM — the refusal path leaves the previous run's bundle in `--out`; a consumer reads a passing binding for a refused replay

Code: `tools/registry-replay.py:116-118` — `publish()` returns immediately when
`bundle is None`, writing nothing and removing nothing; `:182-186` writes
`observations.json` and then publishes.

Counterexample (no run needed to establish the code path): invoke
`tools/registry-replay.py --run … --out DIR` twice against the same `DIR`.
The second run hits `RUNNER_NOT_HELD` / `RUNNER_CLEANUP_FAILED` /
`STREAM_LIMIT` (`registry-replay.py:88-96`), exits 1, and leaves `DIR/bundle.json`
plus `DIR/expected.json` from run 1 in place. Those two files are mutually
digest-consistent, so
`python3 tools/command-binding.py --bundle DIR/bundle.json --expected DIR/expected.json --json`
still exits **0** — a stale, passing binding for a refused replay, sitting next
to an `observations.json` that records the refusal.

The K7/K8/K9 predicates cannot see this: `measure.py:167-176` uses a fresh
`out = fx / (name + '-out')` per case, so the stale-artifact path is never
exercised.

Smallest safe correction: in `publish()`, when `bundle is None`, remove any
pre-existing `bundle.json`/`expected.json` under `--out` (or write a refusal
marker beside them); add one selftest case that reuses an out dir across a
success then a refusal.

### F4 — LOW-MEDIUM — git failures escape as tracebacks and exit 1, colliding with the documented "1 refused (findings)"

Code: `tools/registry-replay.py:135-136` (`git rev-parse --verify`,
`check=True`), `:153-154` (`git clone`, `git checkout --detach`, `check=True`),
`:162` (`runner_path.read_bytes()` — `FileNotFoundError` if the requested
revision predates `tools/registry-check.py`). None is wrapped.

Counterexample: `--run --rev deadbeef…` → `rev-parse` fails →
`subprocess.CalledProcessError` traceback → process exit **1**, which the
documented map (`tools/registry-replay.py:29-31`, `SKILL.md:2052`) reserves for
"refused (findings)"; an unavailable input should be **2**. The same shape
applies to a clone/checkout failure.

Smallest safe correction: wrap those calls in
`except (subprocess.CalledProcessError, OSError)` → stderr message → `return 2`,
matching the existing "frozen registry digest mismatch" path (`:143`).

### F5 — LOW — the sibling mirror is named after the realpath basename and targets the realpath, unlike the runner's own mirror

Code: `tools/registry-replay.py:63-70` (`plan()` realpaths every `*-shokunin`
entry), `:160-161` (`(fleet / os.path.basename(sibling)).symlink_to(sibling)`).
Runner reference: `tools/registry-check.py:772-782` symlinks the **literal**
fleet entry name to the **literal** path
(`src = os.path.join(fleet_root, name); os.symlink(src, os.path.join(fleet, name))`);
`:786` names the clone dir after `basename(root_real)` — registry-replay
matches that part.

Present impact: **none in this fleet** — all 21 `*-shokunin` entries are real
directories (the stray `mori-shukin` / `tameshi-shukin` typo dirs match
neither tool's `-shokunin` rule), so `basename(realpath) == name`, and the
recorded `observations.json` `plan.siblings` lists exactly the 20 non-tameshi
lanes, matching the fleet.

Latent: a lane entry that is a symlink whose target basename differs (a jj
worktree alias) is mirrored under the **target's** basename, so a row using
`../<entry-name>/…` would not resolve where registry-check's mirror would.
Note also that the mirror is **inert for the current registry**: no row argv in
`tools/registry.json` contains `../` or any `<lane>-shokunin` token, so the
recorded 43-row run gained nothing from the sibling symlink set.

Smallest safe correction: keep a `name → realpath` map in `plan()` and create
the mirror link under the literal fleet name, matching `registry-check` exactly.

### F6 — LOW — the clone omits the runner's `-c core.hooksPath=/dev/null`

Code: `tools/registry-replay.py:153` vs `tools/registry-check.py:786-792`
(clone with `-c core.hooksPath=/dev/null`).

Impact today: **none** — `git config --get core.hooksPath` (local and global)
is unset, `.git/hooks` contains only `*.sample` files (git ignores `*.sample`),
and a clone does not copy the source repo's hooks. Residual: on a host with a
global `core.hooksPath`, registry-replay's clone/checkout would consult it while
registry-check's clone would not.

Smallest safe correction: add the same `-c core.hooksPath=/dev/null` to the
clone (and ideally the checkout).

### F7 — INFORMATIONAL (disclosed, not a defect) — receipts assert a cwd that no longer exists

`observations.json` `cwd` = `/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin`,
written **after** the `TemporaryDirectory` was removed
(`tools/registry-replay.py:148-186`); every receipt repeats it.
`tools/command-binding.py:53-54` (`canonical_cwd`) only requires an absolute
normalized path, so `replay-gate.json`'s `exit 0` certifies receipts whose cwd
cannot exist. This is disclosed in the tool docstring (`:21-23`) and in
`SKILL.md:2058-2059` ("Receipt argv, cwd and revision remain
instrument-supplied"), so I record it as residual risk only.

## What I checked and found correct (no defect found)

* **Clone HEAD check** — `tools/registry-replay.py:154-159`: `checkout --detach
  <revision>` then `rev-parse HEAD` compared with the resolved revision;
  mismatch → exit 2. Recorded `observations.json` `revision` and all 43
  `rows[].revision` equal the `--rev` passed
  (`d2eaecd443bf5f4e387e7e5331282e3d11dea047`, matching
  `replay-command.json` `argv`). The check is tautological after a successful
  checkout (`rev-parse HEAD` cannot differ), so it is defensive rather than
  load-bearing — but it is real and the claim is not overstated.
* **Runner digest from the clone copy** — `:162-163` hashes
  `clone/tools/registry-check.py` *after* the checkout and before
  `exec_module`. The recorded `runner_sha256_clone_copy`
  `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad` equals
  `sha256sum tools/registry-check.py` and the blobs of that path at both
  `d2eaecd` and `HEAD` — i.e. the digested bytes are the bytes that executed.
  This is strictly better than the round-23 instrument, which digested the
  **live** copy (`.ufo/evidence/round-23/replay.py:95`).
* **Sibling set from `plan()`** — `observations.json` `plan.siblings` (20
  entries) equals the fleet's 20 non-tameshi `*-shokunin` lanes, all realpath
  form; `plan.fleet_root` = `/home/vgpnk/Projects/shokunin`,
  `plan.repo` = the realpath of the lane. Consistent with `plan()`'s code and
  with the K11 predicate's semantics (identity, not isolation — and the lesson
  already forbids reading it as isolation, `corpus/lessons/round-24.md`).
* **Observations content** — schema `registry-replay-observations-v1`; keys
  `argv, cwd, measurement_interval, plan, registry_sha256, revision, rows,
  runner_sha256_clone_copy, schema, source_requirements_revision`; per row
  `requirement, external, argv, cwd, revision, measurement_interval,
  runner_result` (with complete `stdout`/`stderr` plus the runner's tails,
  `elapsed_s`, `got`, `held`, `kind`, `expect`, `tags`, and `non_hermetic_argv`
  where present). 43/43 rows `held: true`, zero `cleanup_error`, max stdout
  8110 B, max stderr 2391 B (far under the 1 MiB default `--max-stream-bytes`),
  every row interval `start < end`, overall interval
  2026-10-21T15:56:41.156Z → 16:01:01.739Z. The requirement freeze is real
  (`:140-147` re-derives requirements from the caller's baseline and refuses on
  mismatch), the baseline digest is pinned in the observations
  (`registry_sha256`), and `source_requirements_revision` `28cae179e4dc…`
  matches `refs/jj/keep/28cae179e4dc…` in the lane repo.
* **Round-23 comparison** — every difference the successor's docstring claims
  is present in the code and none of the round-23 behaviours were silently
  kept: refusal semantics (`RUNNER_NOT_HELD`, `RUNNER_CLEANUP_FAILED`),
  `--max-stream-bytes`, `live_dependent` classification, realpath fleet
  identity, clone-copy runner digest. The round-23 instrument itself remains
  unchanged (`.ufo/evidence/round-23/replay.py`).

## Calibration assessment (the judged axis)

1. **The frozen counter does not measure my surfaces.** `measure.py` reaches
   `tools/registry-replay.py` only through `--project` (`:161-190`) and
   `--plan` (`:191-199`). `--run` is never invoked; the clone HEAD check, the
   mirror construction, the clone-copy digest and the observations writer have
   **no predicate, no mutant and no repeat**. The contract acknowledges this
   ("an actual replay run is separate evidence"), so the honest reading of
   11/11 is: *the projection and plan CLI discriminate eleven named
   weakenings*. It is **not** evidence that the replay path is hardened.
2. **The single actual run is unrepeated and pre-delivery.** One execution,
   2026-10-21T15:56:41Z, at `d2eaecd`; the delivered revision is `c8c5b88`.
   `tools/` is byte-identical between them (empty `git diff --stat` over
   `tools/`), so the runner behaviour is the delivered one — but the receipts'
   revision label and the requirement set are a wave behind (F2).
3. **Predicate surface vs certified artifact.** K10 is satisfied on the report
   while the bundle keeps the live rows (F1). A predicate that only inspects
   the report cannot see the artifact divergence; the 11/11 count therefore
   must not be read as "the required-command binding is hardened end-to-end".
4. **The saturation claim is honest about its own limits.** The contract's
   bounds (K1-K4 not general mutation adequacy; K5-K6 self-consistent
   substitution; K7-K11 synthetic fixtures; no promotion) are respected by the
   code and by the lesson's reject list ("reading realpath identity as write
   isolation", "reading pinned digests as producer authentication").
5. **Net:** the wave's *numeric* calibration story is defensible; the
   *replay-artifact* story is one step ahead of the evidence. My recommendation
   is to keep the 11/11 predicate count but to record the replay path as
   "executed once at `d2eaecd` over the round-23 frozen 43-row set, with F1/F2
   open", and to fix F1/F2 before any artifact of this wave is described as a
   certified binding of the delivered registry.

## Residual risk and verification gaps

* I did not execute `tools/registry-replay.py` (lane bound: read-only item).
  All execution statements are cited from the recorded receipts
  (`.ufo/evidence/round-24/replay-command.json`, `replay-gate.json`) or from
  read-only git/JSON inspection. The F1/F2/F3 code paths are established by
  reading `tools/registry-replay.py:88-104,116-129,182-186` and the shipped
  JSON, not by a new run.
* Not verified: whether `git clone --no-hardlinks` of this jj-colocated repo
  transfers objects reachable only from `refs/jj/keep/*`. The jj working-copy
  commit `7cb1e25d49d9…` is in **no** `refs/heads`
  (`git for-each-ref --contains 7cb1e25…` lists only
  `refs/jj/keep/7cb1e25…`; `git ls-remote` shows a clone-visible world of
  `refs/heads/master` + `refs/remotes/origin/*`), yet
  `git rev-parse --verify 7cb1e25…^{commit}` succeeds in the live repo. If a
  request names such a revision, the observable failure is the F4 traceback
  (exit 1), not a clean exit 2.
* Not verified (other lanes own them): the `extra-cases.json` fixture loader
  and the K5/K6 substitution pins.
* Environment note: no tool installs were needed or performed for this review
  (`git`, `python3` were already present); nothing outside this report file was
  written, and no git/jj write command was run in the lane repo.

## Smallest safe correction, in order

1. **F1** — filter the live-dependent names out of the published bundle's
   `requirements` and `receipts` (same names on both sides), or refuse with a
   new finding; re-issue `bundle.json`/`expected.json` and the gate receipt.
2. **F2** — re-run `--run` at `c8c5b88` over a baseline regenerated from the
   delivered `tools/registry.json` (47 active rows) and add one active registry
   row pinning the new bundle digest; meanwhile, label the bound set as
   "43 round-23 rows at `d2eaecd`".
3. **F3** — on refusal, remove stale `bundle.json`/`expected.json` under
   `--out`; add one selftest case that reuses an out dir across success then
   refusal.
4. **F4** — map the three git failures and the runner read to exit 2 with a
   stderr message.
5. **F5/F6** — mirror sibling links under their literal fleet names; add
   `-c core.hooksPath=/dev/null` to the clone.
