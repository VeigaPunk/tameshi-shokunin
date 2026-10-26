seat: T47ExecObsA
item: C1 dependence observation — statements `sources-registry`, `depth`, `calibration`, `freshness`
milestone: C1 dependence observation sources-registry, depth, calibration, freshness
rev: 9acfbe21435e1976636a276448dee1d5e7155915
base: 0b5b7cd2b2c15d23086e811a0f0348d84261277b
contract: `.ufo/evidence/round-47/contract.json` (read, never edited)
statements pin: `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56` (re-hashed independently: matches)

## Axes
Calibration. This seat is an **observation** seat: it produces no counter, no SCORECARD edit and no verdict. Its only product is the measured dependence set of four frozen statements, obtained twice, with a root cause for every difference found — so the standing rows can carry a `deps` clause the deciding L1 run will accept.

## What was run (exact commands)

Probe 1 and probe 2, concurrently in one shell, both into empty work dirs, `&`-launched then `wait`ed:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
  --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
  --work /tmp/tameshi-r47-T47ExecObsA/w1 \
  --only "sources-registry,depth,calibration,freshness" --emit
```

(the second run is byte-identical with `--work /tmp/tameshi-r47-T47ExecObsA/w2`).

Independent checks, each read-only on the lane:

```
# shim inventory + dropped-tool availability, per profile
for p in P1 P2 P3 P4 P5; do env -i PATH=$W/$p/shim HOME=$W/$p/home TMPDIR=$W/$p/tmp LANG=C \
  sh -c 'printf "bwrap=%s jj=%s node=%s jq=%s " "$(command -v bwrap>/dev/null&&echo y||echo n)" "$(command -v jj>/dev/null&&echo y||echo n)" "$(command -v node>/dev/null&&echo y||echo n)" "$(command -v jq>/dev/null&&echo y||echo n)"'; done
# P5 decoy really substituted (same argv the counter builds)
env -i PATH=$W/P5/shim HOME=$W/P5/home TMPDIR=$W/P5/tmp LANG=C /usr/bin/bwrap --die-with-parent \
  --bind / / --dev-bind /dev /dev --bind $W/decoy /home/vgpnk/Projects/shokunin -- sh -c \
  'ls /home/vgpnk/Projects/shokunin; test -e /home/vgpnk/Projects/shokunin/MISSION.md && echo present || echo absent; head -1 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh'
# byte identity across the 6 profiles and the 2 runs
cmp -s $r/P0/obs-$id.stdout $r/$p/obs-$id.stdout   # r in {w1,w2}, p in {P1..P5}, id in the four
# exit codes per profile for the three axis statements (the counter does not compare them)
python3 /var/tmp/tameshi-r47-T47ExecObsA/receipts/exits.py
# tool digests, read from the clone at HEAD
for f in .ufo/evidence/kaika-round-1/sources-census-v2.sh tools/mutate-and-run.sh \
         .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-45/freshness/measure.py; do
  git -C <clone> show HEAD:$f | sha256sum | cut -c1-12; done
```

`$W` = the run's work root. Because `/tmp` was 100 % full host-wide, the two `--work` paths were symlinks from `/tmp/tameshi-r47-T47ExecObsA/w{1,2}` to `/var/tmp/tameshi-r47-T47ExecObsA/w{1,2}` (see *Blockers*); the counter's `os.path.abspath` therefore resolved the real bytes on the root filesystem.

## Profile model, and proof the six profiles were genuinely distinct

`profile_env` (`.ufo/evidence/round-47/calibration/measure.py:176-190`) gives P0 the host environment plus `REV`; P1-P5 get `PATH=<shim>`, fresh `HOME`, `TMPDIR`, `LANG=LC_ALL=C`, `TZ=UTC`, `REV`; `:181` drops `bwrap` from P2, `jj` from P3, `node` from P4; `:207-232` decorates P5 with `bwrap --bind / / --dev-bind /dev /dev --bind DECOY /home/vgpnk/Projects/shokunin`.

Measured, both runs (identical):

| probe | bwrap | jj | node | jq | pdftotext | bash | git | python3 | awk | grep |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | y | y | y | y | y | y | y | y | y | y |
| P2 | **n** | y | y | y | y | y | y | y | y | y |
| P3 | y | **n** | y | y | y | y | y | y | y | y |
| P4 | y | y | **n** | y | y | y | y | y | y | y |
| P5 | y | y | y | y | y | y | y | y | y | y |

`command -v` inside each shim confirms the dropped binary is genuinely unreachable (`P2 bwrap=n`, `P3 jj=n`, `P4 node=n`), so the three negative profiles really ran without the tool — the "no dependence" result below is not vacuous.

P5 decoy proof: inside the P5 bwrap argv, `/home/vgpnk/Projects/shokunin` contains **only** `scripts` (`MISSION.md: absent`, `scripts/sources-census.sh` = `#!/bin/sh` stub, `tameshi-shokunin` invisible), while the host root shows `MISSION.md present` and the full lane set. The fleet-root substitution was live during the probes.

P0 host environment differed from P1 in `PATH`, `HOME` (host `/home/vgpnk` vs an empty fresh dir), `LANG`/`LC_ALL` (host vs `C`), `TZ` (`UTC`), `TMPDIR`. No `BASH_FUNC_*` entries were present in the host environment (`env | grep -c '^BASH_FUNC'` = 0), so the operator shell's builtin `grep`/`sort`/`sed`/`jq` wrappers could not leak into P0 as overrides.

## Observations — two independent runs (identical in every tuple)

Both runs printed, verbatim:

```
STATEMENT cap/sources-registry: claimed=- observed=rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0|b9b754713c9c (exit=0) UNPARSED declared_deps=- observed_deps=none DEPS-OK
PROFILES sources-registry: P0=rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P1=rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P2=rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P3=rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P4=rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P5=rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0
STATEMENT axis/depth: claimed=- observed=9|a7d3f2dd7d47 (exit=0) UNPARSED declared_deps=- observed_deps=none DEPS-OK
PROFILES depth: P0=9 P1=9 P2=9 P3=9 P4=9 P5=9
STATEMENT axis/calibration: claimed=- observed=6|657f009bdf1c (exit=0) UNPARSED declared_deps=- observed_deps=none DEPS-OK
PROFILES calibration: P0=6 P1=6 P2=6 P3=6 P4=6 P5=6
STATEMENT axis/freshness: claimed=- observed=9|ba64041f49ff (exit=0) UNPARSED declared_deps=- observed_deps=none DEPS-OK
PROFILES freshness: P0=9 P1=9 P2=9 P3=9 P4=9 P5=9
C1_R47_PARTIAL: self_pin=1 stmts_pin=1 statements=4 mismatches=0 unparsed=4 unobservable=0 dep_mismatch=0 unpinned=0 append_only=1 total=4 rev=9acfbe21435e1976636a276448dee1d5e7155915 C1_R47_PASS=false
```

Both runs exited 1. `C1_R47_PARTIAL` / `PASS=false` is the `--only` path by construction (`measure()`: `passed = … and not only`), and `unparsed=4` is expected at the freeze — the four standing rows have no `deps` clause yet (`claim_of` returns `None` when `DEPS_RE` misses). Neither is a reconciliation signal.

### Per statement

| statement | kind | six tuples P0/P1/P2/P3/P4/P5 | run1 = run2 | observed dependence set |
|---|---|---|---|---|
| `sources-registry` | cap | `rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`+exit 0, six times | yes, byte-identical | **none** (`deps none`) |
| `depth` | axis | `9` six times (exit 0 six times, measured separately) | yes, byte-identical | **none** (`deps none`) |
| `calibration` | axis | `6` six times (exit 0 six times) | yes, byte-identical | **none** (`deps none`) |
| `freshness` | axis | `9` six times (exit 0 six times) | yes, byte-identical | **none** (`deps none`) |

Determinism, stronger than tuple equality: each statement's `obs-*.stdout` has **exactly one distinct sha256 across all 12 files** (6 profiles × 2 runs).

| statement | obs size (every profile) | sha256 (first 16) | content |
|---|---|---|---|
| `sources-registry` | 1865 B | `680be5dce7ef869c` | full census report |
| `depth` | 31 B | `d3143a6827097dbc` | `recorded_cases=9 depth_score=9` |
| `calibration` | 200000 B | `830385b6b4f4932b` | coldread JSON (truncated to the retained tail, see flag 5) |
| `freshness` | 231 B | `fb1a9fe3c21a1f22` | `C1_R45` verdict tail |

Tool digests (read from the clone's `HEAD` blob, both runs, all profiles): `b9b754713c9c` = `sources-census-v2.sh`; `a7d3f2dd7d47` = `tools/mutate-and-run.sh`; `657f009bdf1c` = `coldread/measure.py`; `ba64041f49ff` = `freshness/measure.py`. Independent `git show HEAD:<file> | sha256sum` reproduces all four.

Supporting values inside the observations (identical everywhere): census `rows=120`, tiers `A=108 B=9 C=3`, status `mined=92 queued=22 rejected=6`, B1 informational `count=25` (never a violation), B2 empty, verdict `CLEAN`; freshness `self_pin=1 population=73 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 … C1_R45_PASS=true`; calibration `score=6, box3_full_page=false, sections_covered=60, trace_gate=strict`; depth `recorded_cases=9 depth_score=9`.

## Root causes: why every dependence trigger is inert for these four

An absence is only worth writing down if the mechanism is named. Each of the five triggers (`env`, `bwrap`, `jj`, `node`, `fleet-root`) is structurally dead for these statements, for these reasons.

**`sources-registry`** — the command is `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` with `cwd=clone` (`.ufo/evidence/round-47/calibration/statements.json:4-18`). The script's entire input is `corpus/SOURCES.md` relative to the clone (`sources-census-v2.sh:9`) and the used-by files named in its mined rows, which it tests with `[ -e "$p" ]` and greps by id or basename, all relative to that same cwd (`:17-19`). Its tool set is `grep`, `awk`, `sort`, `uniq`, `while read` (`:10-19`); no `jj`, `node`, `bwrap`, `jq`, `HOME`, `LANG` or `TMPDIR` token appears anywhere in the 20-line script (grep: zero matches). Hence:
- `bwrap`/`jj`/`node` — no such process is ever spawned;
- `env` — the only locale-sensitive operation is `sort | uniq -d` (`:14`) and the result is empty, so no ordering can surface; the row count and verdict are digit/string constants of the committed file;
- `fleet-root` — the census never addresses `/home/vgpnk/Projects/shokunin`. The literal fleet paths in the registry (`corpus/SOURCES.md:450,461,466,473`) sit in prose columns (census/lesson notes), and an extraction of field 12 (used-by) over every 13-field row yields **zero** absolute paths. Empirically the same fact is stronger: under P5 the census still prints `CLEAN` with `== A mined used-by missing (must print nothing)` empty, i.e. nothing it tested lies outside the clone.

**`depth`** — the command is `bash -c 'git show "$REV:tools/mutate-and-run.sh" | python3 -c …'` (`statements.json:310-324`). The one variable it reads is `REV`, which `profile_env` sets to the same revision in all six profiles (`measure.py:176-190`). The file `tools/mutate-and-run.sh` is only ever **read through git's object store**; the statement never executes it. That matters because that file is where `jj` and `node` appear — `tools/mutate-and-run.sh:62,263,1029,1087,1186,1388,1413,1418,1423,1428,1845` are comments, suite strings and audit prose. Dropping `node` (P4) or `jj` (P3) therefore changes nothing, and the observed `recorded_cases=9` count is a property of bytes at REV. `bash`, `git` and `python3` are `/usr/bin` symlinks in every shim, and `P0` and `P1` resolve to the same binaries (`/usr/bin/bash`, `/usr/bin/git`, `/usr/bin/python3`).

**`calibration`** — the command is `python3 .ufo/evidence/round-21/coldread/measure.py --repo {clone} --rev {rev}` (`statements.json:326-343`), which pins the ledger paths and delegates to the round-18 selector (`coldread/measure.py:104-110`). That selector touches the host in exactly one way: `subprocess.run(['git', '-C', repo, *args])` (`round-18/measure.py:155`) plus `os.path.isdir(repo)` on the clone (`:1558`); it has no network, no `datetime`/`time` call (grep empty → `TZ=UTC` is inert) and no locale-dependent formatting. Its only absolute host constant is `LIVE_LANE_ROOT = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'` (`round-18/measure.py:137`), consumed by `under_live_lane` (`:369`) and `live_read_bound` (`:443`): both compare `os.path.realpath` strings and verify committed blobs at REV, and neither requires the path to exist, so the P5 decoy cannot shift them — and the code is not even entered, because `.ufo/evidence/round-21/coldread/ledger.json` (497 entries) carries **zero** `live_lane_reads`/`external` keys. The wrapper's own `env['HOME'] = tmp` (`coldread/measure.py:41`) is selftest-only. Direct re-runs under the exact P1 and P5 environments agree: exit 0, stdout 247746 B, **stderr 0 B**, `score=6 box3_full_page=False sections=60 trace_gate=strict`.

**`freshness`** — the command is `python3 .ufo/evidence/round-45/freshness/measure.py --lane {clone} --rev {rev}` (`statements.json:345-362`). The measurement path is git-blob reads only (`freshness/measure.py:72`) plus gzip/JSON/hash; `pdftotext` is spawned only for `.pdf` snapshots (`:114-118`) and `curl` only under `--live` (`:305-311`, docstring `:36-39`). All 73 ledger snapshots are `.gz`, so neither tool runs — and both resolve inside `/usr/bin`, which every shim exposes anyway. No `jj`, `node`, `bwrap`, `jq`, `HOME`, `LANG` or `TMPDIR` token appears in the file.

Conclusion for the standing rows: the honest clause for all four statements is **`deps none`**, which is exactly what the counter's `--emit` output proposes (`EMIT_CAP … deps `none``, three `EMIT_AXIS … deps `none``).

## Flags requested by the item

1. **P1-vs-P0 path/timestamp artefacts:** none — no statement's P1 tuple differs from P0 at all, let alone by a printed path or clock. The picked values are pure numbers (`9`, `6`, `9`), a count plus a fixed verdict string (`rows=120 SOURCES_CENSUS: CLEAN…`), so a cosmetic path/timestamp print could not have been mistaken for a dependence.
2. **Timeouts:** none in any profile. Measured wall time: census ≈ 0.25 s (300 s cap), depth < 0.1 s (300 s), freshness 1.0-1.4 s (300 s), calibration 30.0-61.7 s (900 s). Calibration's runtime varies run to run while its output is byte-stable; its timeout headroom is >14×.
3. **Crash before reaching the tool:** none. Across all 48 obs files (4 statements × 6 profiles × 2 runs) there is zero `Traceback`, `command not found`, `No such file`, `Permission denied` or `fatal:`; every profile produced the tool's own structured output (complete census report, the `depth_score` line, a JSON body closing with `"trace_gate": "strict"` — `json.loads` accepted it in all six profiles, which is also proof stderr was empty, since `observe` concatenates stderr into the parsed text).
4. **The counter does not compare exits for axis statements.** `comparable()` returns `obs[:2]` for `cap` but `obs[:1]` for `axis` (`measure.py:234-240`), so an exit-only dependence of `depth`/`calibration`/`freshness` would be invisible to the counter. I closed that gap independently: all three exit **0** in all six profiles in both runs (`receipts/exits.py` output). No hidden exit dependence exists, so `deps none` survives the stricter definition too.
5. **The tool sha256 column cannot produce a dependence.** `observe()` computes it with `git -C clone show HEAD:<sha_file>`, i.e. from the committed blob, not from the running environment (`measure.py:207-232`). It is invariant by construction and also excluded from `comparable()`.
6. **obs truncation.** `observe()` stores only `out[-200000:]` (`measure.py:220`). The `calibration` obs hits that cap exactly (200000 B in all 12 files). The byte-identity result therefore covers the retained tail — which contains the picked score — not the full JSON header. The counter's own parsing uses the untruncated text, so the tuples are unaffected.
7. **`--only` semantics.** `--only` forces `C1_R47_PARTIAL` and `PASS=false` (`passed = … and not only`). Two independent seat probes therefore cannot be read as a verdict, as required.

## Blockers encountered (environmental, resolved)

The first attempt of both probes exited 2 with `C1_R47: clone/checkout failed`, before any statement ran. Root cause is host capacity, not the counter: `/tmp` (128 GB scratch partition) was 100 % full host-wide, and `setup_profile`'s `git clone -q --no-hardlinks` died with `error: unable to create file .ufo/evidence/round-20/coldread/source-*.stdout: No space left on device` / `fatal: cannot create directory at '.ufo/evidence/round-20/coldread/traces'` (`clone succeeded, but checkout failed`). Per the L1's host-wide note, the runs were re-pointed at `/var/tmp` via symlinks from the mandated `/tmp/tameshi-r47-T47ExecObsA/w{1,2}` paths, and both completed. A full deciding run clones 12 repos (~2.3 GB per work dir), so **the deciding L1 run needs ~2.3 GB free** in its `--work` root (one work dir is enough); if `/tmp` is still saturated it will fail the same way with the same message.

## Residual risks (latent dependence triggers, none active today)

These are the edits that *would* create a dependence and are therefore the ones to avoid when the standing rows are written or the registry is touched later:

- **`fleet-root` for `sources-registry`:** a mined row whose used-by cell names an absolute path under `/home/vgpnk/Projects/shokunin` would be tested by `[ -e "$p" ]` (`sources-census-v2.sh:17`) and reported `missing:` under P5, flipping the verdict to `VIOLATIONS` (`:20`). Currently zero such cells; regression check is cheap (extract field 12, assert no leading `/`).
- **`node`/`jj` for `depth`:** if the statement were ever changed from *reading* the runner to *executing* it, the `node --selftest` suites and the jj-audit prose inside `tools/mutate-and-run.sh` become live prerequisites.
- **`freshness`:** adding a `.pdf` snapshot to a counted row makes `pdftotext` (`freshness/measure.py:117`) a real host prerequisite, and any use of `--live` adds `curl` (`:310`) and the network; neither is covered by the five declared variants (they would surface only as an `env` diff if the tool were missing from the shim).
- **`calibration`:** `LIVE_LANE_ROOT` (`round-18/measure.py:137`) is inert only because (a) no ledger receipt records live-lane reads and (b) `/home/vgpnk/Projects/shokunin/tameshi-shokunin` is a real directory, not a symlink (`ls -ld`, `readlink -f` = itself). If a future receipt recorded a live-lane read *and* the lane root became a symlink, `os.path.realpath` would diverge under the P5 decoy and the clause would have to grow `fleet-root`.
- **P0's inherited environment:** the five variants cannot see overrides that P0 inherits and P1 discards except as the `env` diff. In this session the host exported no `BASH_FUNC_*` (count 0), so the shell's builtin `grep`/`sort`/`sed`/`jq` wrappers stayed out of P0.

## Evidence retained

Scratch root `/var/tmp/tameshi-r47-T47ExecObsA/` (2.5 MB after cleanup):

- `receipts/w1.run.log`, `receipts/w2.run.log` — the two full probe transcripts, including the PROFILES lines quoted above;
- `receipts/w1/P{0..5}/obs-*.stdout`, `receipts/w2/P{0..5}/obs-*.stdout` — 48 observation files, the byte-identity evidence;
- `receipts/exits.py` — the per-profile exit sweep for the three axis statements.

The 4.6 GB of clones under `w1`/`w2` were deleted after the receipts were extracted (L1's `/tmp` capacity note); the `/tmp/tameshi-r47-T47ExecObsA` symlink directory was removed with them.

## Tooling

Nothing installed or upgraded: no gap required it, and all host pacman transactions remain paused.

## What the L1 can adopt

The four `deps` clauses are `none`, for these four statements, under the frozen definition *and* under the stricter definition that also compares exit codes. Nothing in `statements.json`, the counter, `SCORECARD.md`, the jj state or the Git index was edited; no counter was run as a verdict.
