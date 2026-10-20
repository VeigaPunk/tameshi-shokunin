# RGRecon — `kumitate scripts/round-gate.mjs --selftest` hermeticity

Scope: C1 recon only. No mutants were run (per contract). All work in scratch
`/tmp/tameshi-r16-RGRecon-io6Btu/` (retained for L1 inspection); lane repo and all sibling
repos read-only.

## Verdict

**Yes — the suite is hermetic in the sense the ledger leg needs: filesystem-confined to a
fresh `mkdtemp` root, zero reads under any project tree, zero network, and outcome-independent
of `cwd`, `HOME`, hostile git config, and the four `KUMITATE_*`/`UFO_SRC` variables.** Three
cold runs from a bare `/tmp` copy exit `0` with `60/60 pass`, ~3.3 s each, empty stderr.

Two bounded caveats matter to the sweep and to any claim drafted from it:

1. **Stdout is not byte-stable.** `mkdtempSync` randomness (line 690) is embedded in 9 PASS
   detail lines. Three runs produced three different full-stdout sha256 values; after
   normalizing only the 6-char suffix, all successful configurations are byte-identical
   (sha256 `f87f8d85…39ca`, 63 lines). Verdict must be read from exit code + tail lines,
   never from a stdout hash.
2. **"Polluted env cannot affect it" is narrower than the file's own header claims**
   (`scripts/round-gate.mjs:45-48`). It holds for the four named env vars and for path flags,
   but ambient `TMPDIR`, `PATH`, `GIT_DIR`, and a malformed `KUMITATE_LANE` do change the
   outcome (exit 1/64), and `HOME` git config is read by nested git children although it did
   not change any verdict in testing.

## 1. Pin materialization

```
git -C kumitate-shokunin cat-file -t 364f1d5954158ef8844bca4a5fef57b05d2f2ca5   -> commit
git -C kumitate-shokunin rev-parse 364f1d5...:scripts/round-gate.mjs           -> 1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3 (git blob id)
git show 364f1d5...:scripts/round-gate.mjs > /tmp/tameshi-r16-RGRecon-io6Btu/round-gate.mjs
sha256sum  -> f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9   MATCHES the declared pin
wc -l      -> 1511
```

Commit identity and working-tree agreement (read-only checks):

```
git log --oneline -1 364f1d5  -> "round-24: triage — 105/106 surfaced citation errors repaired ... --src derivation completes in cite-check (29/29) + round-gate (60/60) ..."
git merge-base --is-ancestor 364f1d5 HEAD        -> exit 0 (ancestor of HEAD 1770305fae20826b39905a8251ddeca6b4957ac4)
git diff --stat 364f1d5 HEAD -- scripts/round-gate.mjs -> empty (blob unchanged at HEAD)
sha256sum kumitate-shokunin/scripts/round-gate.mjs -> f890e277…d3e9 (working tree == pin)
git status --porcelain scripts/round-gate.mjs    -> empty (unmodified)
```

So the rev pin is immutable and currently redundant with HEAD; keeping the rev pin costs
nothing and survives future working-tree drift.

## 2. Primary runs (fresh `/tmp` dir, nothing else present)

`cd /tmp/tameshi-r16-RGRecon-io6Btu && node ./round-gate.mjs --selftest` ×3:

| run | exit | wall ms | stdout bytes | stdout sha256 | stderr bytes | last 3 lines |
|---|---|---|---|---|---|---|
| 1 | 0 | 3234 | 9663 | `d0c70160c3355c5ea7eb8b19d0fa122a78186aa1602b336572a8af7bf3c0d8b3` | 0 | `PASS  [60/60]  every declared finding kind fires in at least one fixture — 14 kinds observed` / `ROUND_GATE_SELFTEST: 60/60 pass` / `VERDICT: PASS` |
| 2 | 0 | 3298 | 9663 | `ea84ce518fd65078ceccb9c33a2b1f11ae7c669c16ff10c818b4fe17bb039d89` | 0 | same three lines |
| 3 | 0 | 3336 | 9663 | `5433547a8067a71f2c04a310d93ae7ebb8de678c4afe15f11be33389785c6710` | 0 | same three lines |

stderr sha256 for all three: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
(empty). First stdout line: `kumitate round-gate --selftest (hermetic, node v24.21.0)` —
node version is part of the output.

Source facts backing the count: exactly 60 `check(` call sites (`grep -c`), 60 `PASS`,
0 `FAIL`, 0 `SKIP` in an ordinary run; results are flushed at
`scripts/round-gate.mjs:1498-1507`; fixture root is removed in `finally`
(`:1494-1495`, `rmSync(tmp, {recursive:true, force:true})`). 39 distinct fixture
subdirectories were observed under the root during the traced run.

## 3. Determinism

`diff run1.out run2.out` → 18 differing lines = 9 PASS lines whose detail embeds
`/tmp/kumitate-round-gate-selftest-<6 random chars>/`. Example (`run1` vs `run2`, line 31):

```
< PASS [30/60] REPORT_UNTRACKED ... in /tmp/kumitate-round-gate-selftest-EA05pY/26-report-untracked/main
> PASS [30/60] REPORT_UNTRACKED ... in /tmp/kumitate-round-gate-selftest-0zltfE/26-report-untracked/main
```

After `sed 's/selftest-[A-Za-z0-9]\{6\}/selftest-X/g'`, these all hash
`f87f8d85b18d70970651f37abc86d5ba845aa3551312f2053e1f330b25ce39ca` and `diff` empty:
run1, run2, run3, HOME-empty, cwd=/, renamed copy, subdir copy, bogus flags, both
concurrent runs, `TMPDIR=<custom existing>`, active `UFO_SRC`/`KUMITATE_*` poison, hostile
HOME. Exceptions:

- `TMPDIR=<custom>` differs only by the emitted absolute path (fixtures live under the
  chosen root); verdict identical.
- `KUMITATE_ROUND_GATE_NESTED=1` emits one `SKIP  [51/60]` line (`:1382`) and runs in
  1.84 s; still `60/60 pass`, `VERDICT: PASS` (skipped check is counted as ok).

## 4. File access (`strace -f -e trace=openat,execve`)

Traced run: `strace -f -e trace=openat,execve -o trace.txt node ./round-gate.mjs --selftest`
→ exit 0, 82,926 trace lines, 67,312 `openat`, 14,317 ENOENT (normal loader/git probing),
27,680 opens with an absolute path outside `/tmp`.

**Live trees: 0 opens under `/home/vgpnk/Projects` (and 0 under either repo name).** This is
the load-bearing hermeticity fact. It matches the source: `resolveSrcDefault` (`:161-169`,
which `existsSync`es the `$HOME` candidates) is called only at `:296` under
`if (!opts.selftest)`.

Absolute paths outside `/tmp` that were actually opened, by class:

| path | count | who |
|---|---|---|
| `/dev/null` | 10,302 (1,402 in write mode) | node spawn plumbing / git |
| `/usr/lib/libc.so.6`, `libz-ng`, `libpcre2-8`, `libstdc++`, `libpthread`, `/etc/ld.so.cache` | loader | node + git |
| `/usr/lib/locale/locale-archive`, `/usr/share/locale/**` | 1,188 + locale trees | node + git message catalogs |
| `/home/vgpnk/.config/git/config` | 804 successful opens | **git children** |
| `/home/vgpnk/.config/git/attributes`, `/etc/gitattributes` | 336 each | git children |
| `/etc/passwd`, `/etc/nsswitch.conf` | 22 each | git identity fallback |
| `/etc/ssl/openssl.cnf` | 118 | git binary's linked TLS init |
| `<fnm>/node-versions/v24.21.0/installation/bin/node` | 118 | nested `process.execPath` |
| `/dev/tty` | 22 (write) | git terminal probing |

No other absolute read path appeared: no `/root`, no ssh/netrc/curlrc, no `/etc/gitconfig`
(GIT_CONFIG_SYSTEM is pinned to `/dev/null` at `:704-711`). `/etc/ssl/openssl.cnf` is
loaded by the dynamically linked git binary, not used for any connection.

**Writes.** Every write-mode `openat` with an absolute path is inside
`/tmp/kumitate-round-gate-selftest-*` except `/dev/null` and `/dev/tty`. The only relative
write paths are `.git/...` and `./logs/...`, written by git processes; every git argv carries
either `-C <fixture>` (864 of 886) or an absolute `/tmp/...` destination (`git init --bare`,
22) — `[INFERENCE]` therefore these resolve inside fixture dirs. No `.git` or other stray
entry appeared in the invocation dir. A forced-fatal run (`PATH=` without git) left 0
fixture dirs behind (`before=0 after=0`), so the `finally` cleanup holds on failure paths too.
At one poll 2 transient `kumitate-round-gate-selftest-*` dirs were visible while sibling lane
work was running; they were gone later — concurrent runs use distinct `mkdtemp` roots, and
two simultaneous invocations here both passed.

**Network.** Second trace `-e trace=network`, 20,825 lines, exit 0:
`0` `AF_INET`/`AF_INET6`, `0` `connect(`, `0` `sendto`/`recvfrom`/`getaddrinfo`. Only
`socketpair` (3,009 — node's spawn pipes), `setsockopt` (12,036), `getsockname`/`getsockopt`
(621 each), `shutdown` (1,003). The "zero network" claim holds.

## 5. Process dependencies

Successful `execve` targets in the traced run:

| binary | count | reason |
|---|---|---|
| `/usr/bin/git` | 886 | fixture construction/verification (`:212-215`, `:717-720`) |
| `/usr/lib/git-core/git` | 258 | git subcommand dispatch |
| `/usr/lib/git-core/git-receive-pack` | 22 | `git push` into fixture bare remotes |
| `/bin/sh` | 22 | git's receive-pack invocation (`/bin/sh -c "git-receive-pack '<abs /tmp path>'"`) |
| node (fnm install) | 117 | nested gate runs `[SELF, ...]` via `process.execPath` (`:725`) |

Versions observed: node `v24.21.0` (fnm multishell), git `2.56.0` (`/usr/bin/git`), strace
`7.2`. No tool installs or upgrades were performed.

## 6. Environment variables consulted

Source inventory (`grep -n 'process\.env\|envOr('`):

| var | read at | role | observed effect on `--selftest` |
|---|---|---|---|
| `KUMITATE_LANE` | `:276` | lane validation | valid value ignored; **malformed value (`"has space"`) → exit 64** before dispatch (`main` catches at `:629-635`) |
| `KUMITATE_MAIN_REPO` | `:283` | default dir | no effect (poisoned `/nonexistent/main` → identical pass) |
| `KUMITATE_REPORTS_DIR` | `:288` | default dir | no effect (poisoned) |
| `UFO_SRC` | `:162` via `:161-169` | origin default | not resolved under `--selftest` (`:296`); poisoned `/nonexistent/ufo` → identical pass |
| `KUMITATE_ROUND_GATE_NESTED` | `:1381` | recursion guard | `=1` skips only check 51; still 60/60, 1.84 s |
| `TMPDIR` (via `os.tmpdir()`) | `:690` | fixture root | custom existing dir → pass, paths change only; **nonexistent dir → exit 1** (`ENOENT … mkdtemp '/nonexistent/xyz/kumitate-round-gate-selftest-XXXXXX'`) |
| `PATH` | `:212`, `:717`, `:719` (`spawnSync('git')`) | locate git | `/usr/bin:/bin` → pass; **empty PATH → exit 1** (`fixture lane init failed: exit null`) |
| `HOME` | `:135` (`homedir()` for `SRC_CANDIDATES`, evaluated at module load) + git children | git global config | empty HOME → identical pass; hostile `.config/git/config` (`defaultBranch=trunk`, `commit.gpgsign=true`, `hooksPath`, `fsmonitor`) → identical pass |
| inherited `GIT_*` | `:713` (`cleanEnv` deletes only the 4 vars) | git children | **`GIT_DIR=/nonexistent` → exit 1** (`fixture lane init failed: exit 128 fatal: Invalid path '/nonexistent'`) |
| `process.execPath` | `:725` | nested node | absolute; not a PATH lookup |

`parseArgs(process.argv.slice(2))` is called with default `process.env` (`:628`), so env
validation runs before the `--selftest` short-circuit at `:635`. Flags *after* `--selftest`
are parsed but their dir values are not used: `--selftest --repo /nonexistent/repo
--reports-dir /nonexistent/reports --main-repo /nonexistent/main --origin /nonexistent/origin`
→ exit 0, 60/60 (also exercised by check 46, `:1393-1397`). `--bogus` → exit 64,
`unknown argument: --bogus`.

Sensitivity matrix (all runs from the pinned copy):

| configuration | exit | verdict | normalized stdout |
|---|---|---|---|
| default, runs 1-3 | 0 | 60/60 PASS | identical |
| `HOME=<empty dir>` | 0 | 60/60 PASS | identical |
| `HOME=<hostile .config/git/config>` | 0 | 60/60 PASS | identical |
| `HOME=<hostile> GIT_CONFIG_GLOBAL=<hostile>` | 0 | 60/60 PASS | identical |
| `cwd=/` (absolute script path) | 0 | 60/60 PASS | identical |
| renamed `m9.mjs`, same dir | 0 | 60/60 PASS | identical |
| `sub/nested-name.js`, any cwd | 0 | 60/60 PASS | identical |
| bogus dir flags after `--selftest` | 0 | 60/60 PASS | identical |
| two concurrent runs, same dir | 0/0 | 60/60 PASS ×2 | identical |
| `TMPDIR=<custom existing>` | 0 | 60/60 PASS | path text differs only |
| active `UFO_SRC`/`KUMITATE_*` poison | 0 | 60/60 PASS | identical |
| `KUMITATE_ROUND_GATE_NESTED=1` | 0 | 60/60 PASS | one SKIP line |
| `TMPDIR=<nonexistent>` | 1 | fatal mkdtemp | — |
| `GIT_DIR=<nonexistent>` | 1 | fatal fixture init | — |
| `PATH=` (no git) | 1 | fatal fixture init (`exit null`) | — |
| `KUMITATE_LANE='has space'` | 64 | usage error | — |
| `--bogus` | 64 | usage error | — |

Location/filename independence is what makes the mutation harness's `node "$MUTANT"
--selftest` contract work: `HERE`/`SELF` are derived from `import.meta.url` (`:139`, `:702`),
and `DEFAULT_MAIN_REPO`/`DEFAULT_REPORTS_DIR` (`:142-143`) are never consumed under
`--selftest`.

## 7. Contradiction with the file's own hermeticity claim

`scripts/round-gate.mjs:45-48` states the suite "never reads the live trees, `--repo` or the
environment: bogus flags and a polluted env cannot affect it." Observed, the live-tree half
is exactly true (0 opens under `/home/vgpnk/Projects`), and the flag half is true for path
flags; but the environment half holds only for `KUMITATE_LANE`/`KUMITATE_MAIN_REPO`/
`KUMITATE_REPORTS_DIR`/`UFO_SRC` (the list `cleanEnv` strips at `:712-716`). `TMPDIR`, `PATH`,
`GIT_DIR`, and malformed `KUMITATE_LANE` do change the outcome, and `HOME` git config is read
by git children. Suggest the precise claim be used in any record: *hermetic fixtures under a
fresh `mkdtemp` root, no live-tree reads, zero network, and outcome-independent of cwd,
HOME content, and the four named env vars.* This is a doc-vs-behaviour mismatch in a sibling
repo (read-only here) — recorded, not edited.

## 8. Bounded recommendations for the C1 sweep / ledger leg

- **R1 — verdict parsing only.** Read exit code plus the last two lines
  (`ROUND_GATE_SELFTEST: N/60 pass`, `VERDICT: PASS|FAIL`). Do not compare full stdout bytes
  or its sha256: the `mkdtemp` suffix makes every run unique. If a positional digest is wanted,
  pin the normalized form (`f87f8d85…39ca` today) and state the normalization.
- **R2 — sanitize ambient git env for the sweep.** At minimum leave `GIT_DIR`,
  `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR` unset; require
  `git` on PATH and a writable `TMPDIR`. The runner already fails closed if the control run
  is red (`tools/mutate-and-run.sh:470-472`), so a polluted environment would surface as
  `CONTROL: RED`/exit 2 rather than a false kill.
- **R3 — pre-register exit-flipping predictions.** The runner's verdict is exit-code only
  (`tools/mutate-and-run.sh:32-35`; per-defect `KILLED|SURVIVED|INCONCLUSIVE`). A mutant that
  only alters a detail string or a timing/path token can never be killed; predictions must
  name a check whose failure flips a `check()` to false (`ok:false` → `VERDICT: FAIL` → exit 1)
  or crashes the suite. Detail-text mutants will read SURVIVED by construction.
- **R4 — budget.** ~3.3 s/run cold; control + 10 mutants ≈ 36 s serial. Runner default
  timeout 300 s (`tools/mutate-and-run.sh:166`) is ample; no flake risk from timing.
- **R5 — two harness copies exist.** `tools/mutate-and-run.sh` sha256
  `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` (77,904 B) vs
  `.ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh` sha256
  `2e810b5dedbd21458eaebe0880d744c4565896388c7d8076b216ae45a723a7c6` (79,378 B). The w1 copy
  adds the leg-7 placeholders (`@@RG_KILLED@@/@@RG_PCT@@`) and doc lines; canonical tool
  remains `tools/mutate-and-run.sh`. L1 should confirm which copy executes the sweep before
  recording the leg.
- **R6 — run the suite from a neutral cwd.** Verified cwd-independent, but the runner's
  suite command runs from the caller's CWD; either is safe. Concurrent runs are safe
  (distinct `mkdtemp` roots) but produce transient `/tmp` dirs.

## 9. Unknowns / not tested

- Only git `2.56.0` and node `v24.21.0` were exercised. Whether older/newer git breaks any
  fixture (e.g. `init -b`, receive-pack messages) is untested.
- Locale sensitivity was not probed (`LC_ALL` untouched); git message catalogs are loaded but
  check details appear exit-code-driven.
- `HOME` influence was sampled with one hostile config; a config that changes `git`
  behavior more aggressively (aliases, `core.hooksPath` on the nested gate's repos) was not
  exhaustively searched. Empirically the outcome was insensitive.
- `chdir` was not traced; the "relative git writes stay in fixtures" conclusion rests on
  every git argv carrying `-C <fixture>` or an absolute `/tmp` path.

## 10. Reproduce

```bash
D=$(mktemp -d /tmp/tameshi-r16-RGRecon-XXXXXX)
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
  364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > "$D/round-gate.mjs"
sha256sum "$D/round-gate.mjs"          # f890e277…a834d3e9
cd "$D" && node ./round-gate.mjs --selftest; echo "exit=$?"
strace -f -e trace=openat,execve -o trace.txt node ./round-gate.mjs --selftest
strace -f -e trace=network        -o net.txt   node ./round-gate.mjs --selftest
```

Evidence files retained: `/tmp/tameshi-r16-RGRecon-io6Btu/{run1,run2,run3}.{out,err}`,
`trace.txt`, `net.txt`, `{home,hostile,hostile2,cwdroot,tmpd,poison,lane,unk,nested,m9,sub,subcwd,bogus,par1,par2,tmpbad,gitdir,pathmin,pathnone}.{out,err}`.

```text
# machine-readable recon summary (schema rg-recon-hermeticity-v1; not a cold-read block)
target= kumitate-shokunin/scripts/round-gate.mjs
rev= 364f1d5954158ef8844bca4a5fef57b05d2f2ca5
blob_sha256= f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
selftest_checks= 60
runs= 3 primary (exit 0, 60/60, stderr empty) + 15 variants
dur_ms= 3234,3298,3336 mean=3289
stdout_stable= false (mkdtemp suffix); normalized_stdout_sha256= f87f8d85b18d70970651f37abc86d5ba845aa3551312f2053e1f330b25ce39ca
stderr_sha256= e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
opens_under_projects= 0
writes_outside_mkdtemp= none (/dev/null,/dev/tty only)
network= none (0 AF_INET, 0 connect)
deps= git(2.56.0 on PATH), node(process.execPath), /bin/sh, writable TMPDIR
home_insensitive= true ; cwd_insensitive= true ; filename_location_insensitive= true
env_fatal= TMPDIR missing, PATH without git, GIT_DIR set ; env_parse_exit64= malformed KUMITATE_LANE, unknown flag
```

## Tools

No installs or upgrades were needed or performed. Versions used: node `v24.21.0`, git
`2.56.0`, strace `7.2`, coreutils `sha256sum`/`sed`/`diff`/`grep`.
