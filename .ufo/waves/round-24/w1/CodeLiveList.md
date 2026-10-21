# CodeLiveList — round24 W1

Axis: `calibration`. Leaf member; no subagent dispatch. Scope: does the round24
replay's live-dependence accounting name exactly the rows that read live fleet
state?

## Verdict

**PARTIAL — the list is exactly what the two named detectors produce, but that
set is not the set of rows that read live fleet state.**

* The **list is arithmetically exact** against its stated rule. Recomputing
  `live_dependent` from `observations.json` under the rule at
  `tools/registry-replay.py:99` (`row.external is True or
  runner_result.non_hermetic_argv`) yields exactly
  `['pin-disposition-read', 'verify-round15']` — byte-identical to
  `.ufo/evidence/round-24/replay/live-dependent.json:2-5` and to the
  `live_dependent` field of the report embedded in
  `.ufo/evidence/round-24/replay-command.json` (last stdout line).
  `revision_pinned` recomputes to `43 - 2 = 41`, matching
  `live-dependent.json:6` and the report. `bundle_sha256` agrees across
  `bundle.json`, `expected.json` and the report
  (`4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`).
* **The rule itself is incomplete.** The registry's `external` flag marks
  *declared* live dependence, and the runner's `non_hermetic_argv` marks only
  *absolute argv tokens* under the live fleet root
  (`tools/registry-check.py:632-645`, applied at `:662-671`). Neither detector
  can see a row that reaches live fleet state through the **fleet-mirror
  symlinks** the replay itself creates (`tools/registry-replay.py:160-161`).
  Two replayed rows do exactly that and are counted among the 41
  "revision-pinned": `mutate-and-run-regression` and `round21-measure-selftest`.

No production file was edited. No registry battery, gate or selftest was run
inside the repository; all probes ran in `/tmp` against copies.

## Evidence

### 1. The list is exact against the stated rule

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 - <<'EOF'
import json
obs=json.load(open('.ufo/evidence/round-24/replay/observations.json'))
live=[r['requirement']['name'] for r in obs['rows']
      if r.get('external') is True or (r['runner_result'] or {}).get('non_hermetic_argv')]
ld=json.load(open('.ufo/evidence/round-24/replay/live-dependent.json'))
print('recomputed:',sorted(set(live)))
print('file      :',ld['live_dependent'])
print('MATCH     :',sorted(set(live))==ld['live_dependent'])
print('rev_pinned:',len(obs['rows'])-len(set(live)),'vs',ld['revision_pinned'])
EOF
recomputed: ['pin-disposition-read', 'verify-round15']
file      : ['pin-disposition-read', 'verify-round15']
MATCH     : True
rev_pinned: 41 vs 41
```

The two named rows are exactly the two `external: true` rows in the **source
registry** (`.ufo/evidence/round-23/registry-baseline.json`, the frozen
baseline the replay was bound to) and in the **current** `tools/registry.json`:
`pin-disposition-read` and `verify-round15` (`tools/registry.json` active rows
carrying `external: true`). No other active row in either registry declares
`external`, and no other row's `runner_result` carries `non_hermetic_argv`
(only `pin-disposition-read` does, at `observations.json:308`).

The two rows genuinely read live state — both are correctly classified:
* `pin-disposition-read` argv carries the live fleet root
  (`observations.json:283-308`, `non_hermetic_argv:
  ["/home/vgpnk/Projects/shokunin"]`), and its stdout enumerates live sibling
  paths (`/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh`,
  `.../kumitate-shokunin/scripts/claims-check.mjs`,
  `.../mado-shokunin/tools/mado-verify.sh`,
  `.../tsukuroi-shokunin/tools/tsukuroi-census.sh`).
* `verify-round15` reads the live fleet via the hardcoded
  `CENSUS_TOOL = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`
  (`.ufo/evidence/round-15/verify.py:105`, invoked at `:836` with
  `--root /home/vgpnk/Projects/shokunin`), and its stdout carries
  `sources-census: PASS exit=0` / `sources-census-ok-line: PASS ok line
  present`.

### 2. Two unlisted rows read live fleet state through the fleet-mirror symlinks

`tools/registry-replay.py:160-161` builds the replay's fleet mirror as
**symlinks into the live fleet**:

```
for sibling in layout['siblings']:
    (fleet / os.path.basename(sibling)).symlink_to(sibling, target_is_directory=True)
```

`layout['siblings']` are `os.path.realpath` of the live
`/home/vgpnk/Projects/shokunin/*-shokunin` directories
(`tools/registry-replay.py:67-68`).

**`mutate-and-run-regression`** (`observations.json:853-900`, `external: false`,
no `non_hermetic_argv`, `held: true`, counted among the 41) resolves its fleet
root from its own location — `FLEET_ROOT=$(dirname "$(dirname "$(dirname
"$SELF")")")` (`tools/mutate-and-run.sh:1287`) — so it reads
`$FLEET_ROOT/<sibling>` (`tools/mutate-and-run.sh:1269`), i.e. the **live**
siblings through the mirror. Its own stdout proves it
(`observations.json:883`):

```
REGRESSION_PIN js-kimi-census: source=git repo=/tmp/tameshi-registry-replay-dzo3ypiq/fleet/kumitate-shokunin rev=175de6ba2e9e904010411b19cab27e0af9aad3d4 path=scripts/kimi-census.mjs ... sha256=83016d45049b009a...
```

All eight ledger legs point at `/tmp/tameshi-registry-replay-.../fleet/<sibling>`.
The mirror symlink resolves to the live repo, and the materialised bytes are
the **live** repos' bytes. Verified against the live tree:

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 175de6ba:scripts/kimi-census.mjs | sha256sum
83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426   # == recorded pin
$ git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show fecee874:corpus/surface-census.sh | sha256sum
275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f   # == recorded pin
```

A symlinked mirror path resolves to the live repo for git purposes:

```
$ ln -s /home/vgpnk/Projects/shokunin/kumitate-shokunin fleet-kumitate
$ git -C fleet-kumitate rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kumitate-shokunin
```

The r17 `repo_identity` guard (`tools/mutate-and-run.sh:1116-1123`) does **not**
catch this: it compares `realpath` of the repo against `realpath` of the git
toplevel, and the symlink makes both resolve to the same live path. It only
rejects a lane dir that is not its own repository.

The leg outcome is genuinely contingent on live fleet state. If the live
sibling does not carry the pinned rev, the guard at
`tools/mutate-and-run.sh:1128` (`git cat-file -e`) fails and the leg returns
SETUP → `run_regression` exits 2 → the row's `expect.exit 0` is missed →
`held: false` → the projection refuses and publishes **no** bundle. Demonstrated
on a scratch repo pair:

```
(a) repo WITH the pinned rev : cat-file -e OK  -> leg materialises -> PASS path
(b) repo WITHOUT the pinned rev: cat-file -e FAILS -> "REGRESSION_CASE
    js-sources-check: SETUP (path not in revision: ...)" -> return 2 ->
    "REGRESSION: SETUP" -> exit 2 -> held=false -> RUNNER_NOT_HELD -> no bundle
```

**`round21-measure-selftest`** (`observations.json`, `external: false`, no
`non_hermetic_argv`, `held: true`) reads live siblings the same way. Its
selftest materialises the pinned surfaces from
`ROOT.parent / surface["repo"]` (`tools/round21-measure.py:74`), where `ROOT`
is the clone lane root and `ROOT.parent` is the fleet mirror whose sibling
entries are the live symlinks. The pinned surfaces name live siblings
(`.ufo/evidence/round-21/c2-contract.json`: `kumitate-shokunin`,
`kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`). Reproduced under the
replay's exact topology (clone at `d2eaecd`, siblings symlinked to live):

```
$ python3 tools/round21-measure.py --selftest
MEASURE_CASE c2-complete PASS
...
ROUND21_MEASURE_SELFTEST: 13/13 pass
$ realpath fleet/kumitate-shokunin
/home/vgpnk/Projects/shokunin/kumitate-shokunin
$ git -C fleet/kumitate-shokunin show 175de6ba:scripts/kimi-census.mjs | sha256sum | cut -c1-16
83016d45049b009a
```

(The same script fails hard — `CalledProcessError ... exit status 128` — when
the mirror lacks the sibling, confirming the read is the load-bearing part.)

### 3. K10 does not discriminate either disjunct

`tools/registry-replay.py:99` implements the union as a single `or`. The
frozen ruler exercises it with **one fixture row carrying both signals at once**
(`measure.py:181`: `obs(external=True, non_hermetic_argv=['/live/root'])`), so
the predicate cannot tell which disjunct did the work. Mutation probe in `/tmp`
against the real tool:

```
K10 predicate on mutant [drop-non_hermetic-branch]: still passes = True
K10 predicate on mutant [drop-external-branch]    : still passes = True

REAL observations, pristine      live_dependent = ['pin-disposition-read', 'verify-round15']
REAL observations, drop-non-herm  live_dependent = ['pin-disposition-read', 'verify-round15']
REAL observations, drop-external  live_dependent = ['pin-disposition-read']
```

Dropping the `external` disjunct silently un-lists `verify-round15` — a row
that reads the live fleet census tool — while K10 still reports
`discriminated: true`. This is the frozen ruler's own recorded weakness
(`corpus/lessons/round-24.md:107`, Erratum F: "K10: dropping either
live-dependent disjunct — the selftest only"); I confirm it independently with
a live mutation probe rather than citing the lesson.

### 4. What I ruled out

* **Every other replayed row is clone-local.** Systematic scan of the script
  each row invokes (at the replay revision `d2eaecd`, the revision the
  observations were captured at — `observations.json:872`) for
  `/home/vgpnk`, `ROOT.parent`, `parents[n]`, `fleet_root`, `FLEET_ROOT`:
  only `tools/mutate-and-run.sh` and `tools/round21-measure.py` reach outside
  the clone.
* **Selftests that embed fleet legs do not read live state.**
  `mutate-and-run-selftest` produced zero `REGRESSION_PIN` lines and zero
  `/home/vgpnk` strings (its embedded legs use `$fx` fixtures);
  `round21-measure-selftest` is the exception above.
* **`pin-disposition-selftest`** is hermetic by construction
  (`tools/pin-disposition.py:705`: "Hermetic fixtures under /tmp: no fleet
  repo, no sibling repo is read").
* **The four `round-17`/`18`/`19` measure-and-assemble scripts** carry a
  `LIVE_LANE_ROOT` constant (`/home/vgpnk/.../tameshi-shokunin`) but use it
  only as a *string prefix* for classifying recorded trace receipts
  (`.ufo/evidence/round-18/measure.py:369-370`, `:443-444`,
  `.ufo/evidence/round-18/coldread/assemble.py:576`) — they read the clone's
  own object store, and the constant names the live lane only in expected
  error strings. No live bytes are read.
* **`bash-witness-count`** does not materialise the kagi target
  (`materialize_target` is called only from `cmd_declare`/`cmd_rerun`, at
  `tools/bash-witness-study.py:864`, `:933`); `cmd_count` reads only the
  clone's committed `declared.tsv`/`summary.json`.
* **`context-capture-frozen`** validates the *recorded* `lane_root`/
  `fleet_root` strings and their declared digests
  (`tools/context-capture.py:500-511`, `:650-670`); it does not open the live
  paths. It is nonetheless correctly listed, because the registry declares it
  `external: true`.
* **The two listed rows are not over-claimed.** `pin-disposition-read` and
  `verify-round15` both genuinely read live state; `live-dependent.json` is
  right to list them and right to exclude the other 39 clone-local rows.

## Residual risk and verification gaps

* **The 41/2 split in `live-dependent.json` is a declaration count, not a
  hermeticity count.** `revision_pinned: 41` reads as "41 rows reproduce from
  the frozen revision alone". Two of those 41 read the live fleet. The field
  name overstates what the two detectors establish.
* **`live-dependent.json` is not digest-covered.** `expected.json` pins only
  `bundle_sha256`; the split lives in an unpinned sidecar and in the report's
  stdout, so a consumer of `bundle.json` cannot see which receipts are live.
  Already recorded as Erratum M (`corpus/lessons/round-24.md:160-165`).
* **The replay was bound to the round23 43-row set at `d2eaecd`, not the 47
  active rows at `c8c5b88`.** `tools/registry.json` now has 47 active rows
  (four added: `command-binding-frozen-clean-pinned`,
  `command-binding-selftest-r24`, `command-binding-source-read-red-pinned`,
  `registry-replay-selftest`); none of the four declares `external` and none
  carries a live absolute argv token, so the *set* would be unchanged if they
  were replayed — but the *count* would be 47/45, not 43/41. Already recorded
  as Erratum M's second bullet.
* **No registry row pins the round24 replay bundle** — `grep -c round-24
  tools/registry.json` → 0. Erratum L (`corpus/lessons/round-24.md:158`).
* **I did not execute the round24 replay or the registry battery.** My probes
  were: (a) recomputation of the projection in `/tmp` from the retained
  `observations.json`; (b) two mutation probes of `tools/registry-replay.py`
  copied to `/tmp`; (c) a byte-digest comparison of the eight ledger pins
  against the live sibling repos; (d) a reproduction of the replay's fleet
  topology in `/tmp` (clone at `d2eaecd`, siblings symlinked to live) to
  confirm the symlink resolves to live and to make the pinned rev absent; (e)
  a scratch-repo pair to demonstrate the SETUP→exit-2→held=false chain.
  I did not verify that a *pruned* live sibling actually breaks the held row at
  `c8c5b88` in situ — only that the guard chain makes it so.

## Smallest safe correction

Two independent changes; neither requires touching the frozen ruler or the
published receipts.

1. **Make the mirror honest about live-ness.** In `tools/registry-replay.py`,
   record per-row whether the row's fleet root resolved through a symlink
   into the live fleet, and surface it as a third disjunct in the same
   `live_dependent` computation at `:99`. Minimal form: the replay already
   knows each row's `cwd` and each mirror entry's realpath, so
   `realpath(row.cwd).startswith(realpath(live_fleet_root))` plus a check of
   the row's `FLEET_ROOT`-style resolution is enough to add
   `mutate-and-run-regression` and `round21-measure-selftest`. Cheaper and
   equally honest: rename the sidecar fields from `revision_pinned` to
   `not_declared_live` and add `live_dependent_undeclared` — but a rename
   alone leaves the gap.

2. **Give the two flags separate registry rows, or split the K10 fixture.**
   The cheapest change that makes K10 discriminating without editing the
   frozen ruler is in the *registry*, not the tool: nothing in the registry
   currently distinguishes "external because argv names the live root" from
   "external because the script reaches live state". Adding an explicit
   per-row `external` for the two symlink-mediated rows is a source change to
   `tools/registry.json` and a re-run — expensive. The cheaper, already-routed
   option (Erratum F: "split single-trigger fixtures for K7–K11") is to add a
   second K10 fixture row carrying `external: true` **without**
   `non_hermetic_argv` and a third carrying `non_hermetic_argv` **without**
   `external`; then dropping either disjunct flips the report and K10
   discriminates. That is a round25 ruler change, not a round24 one, and it
   does not invalidate the frozen before/after pair.

I recommend (1) as the smallest correction that makes the *shipped* artifact
honest: it changes one line in `tools/registry-replay.py` plus the sidecar
field names, requires one replay re-run, and touches no frozen receipt.

## Tooling

No tools were installed or updated for this review; every check used the
already-present `git`, `python3` and `sha256sum`. No network access, no
`sudo`, no host service touched. All probes ran under `/tmp`
(`/tmp/k10-probe`, `/tmp/legprobe`, `/tmp/legsetup`, `/tmp/r21probe`,
`/tmp/r21probe2`, `/tmp/livelink-probe`) and left the repository, the fleet
root and the sibling lanes unmodified.
