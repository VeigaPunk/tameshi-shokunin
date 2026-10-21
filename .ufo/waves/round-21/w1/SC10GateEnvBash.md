# SC10 — F5 sensitivity prediction, bash surfaces + tameshi runner (from source at pins)

Verdict: **done** — static prediction only, nothing executed (per assignment "Do not run them").
Scope: the 5 bash-interp surfaces of `.ufo/evidence/round-21/c2-contract.json` under the frozen F5 ruler
(7 profiles; tuple = (exit, sha256(stdout), sha256(stderr)); normalization "none"; invocation
`bash target.sh --selftest` inside bwrap `--ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind R /tmp/w --unshare-net --chdir /tmp/w`).

## Pins verified (read-only `git show`, byte-verified)

| surface | repo@rev | path | sha256 | contract match |
|---|---|---|---|---|
| bash-surface-census | kagi-shokunin@fecee874 | corpus/surface-census.sh | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | OK |
| bash-checklist-run | kagi-shokunin@fecee874 | corpus/checklist-run.sh | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` | OK |
| bash-tsukuroi-census | tsukuroi-shokunin@165307fe | tools/tsukuroi-census.sh | `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` | OK |
| bash-mado-verify | mado-shokunin@eead56b2 | tools/mado-verify.sh | `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` | OK |
| tameshi-runner | tameshi-shokunin@08175c6 | tools/mutate-and-run.sh | `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` | n/a (no contract pin; recorded here) |

Commands (exit 0 each):
`git -C /home/vgpnk/Projects/shokunin/<repo> show <rev>:<path>` × 5 into `/tmp/tameshi-r21-SC10GateEnvBash-x/surfaces/`;
`sha256sum /tmp/tameshi-r21-SC10GateEnvBash-x/surfaces/*.sh` → 5/5 hashes above.
No tool installs performed (none needed; no pacman touched).

## Ruler facts that shape every prediction

- **PATH is not an F5 axis**: clean sets `PATH=$PATH` (invoking PATH); host keeps it; the 5 deltas (tz/locale/home/columns) keep it. All 7 profiles run with byte-identical `command -v` resolutions. The janitor/sqlite3/python3 present-or-absent branch (surface-census:82-83,469,820-823; mado:114-116) therefore flips identically in every profile.
- **umask is not an env axis** (process attribute, inherited identically; also tsukuroi forces `umask 077` at :140, and `fx_hash` :735 hashes contents only).
- **Host = invoking env minus every `GIT_*`** → the runner's r17 attack class (`GIT_DIR` clobber, runner:253-261) is defused upstream; `git_clean`'s scrub list (built from live env, runner:262-273) is empty in host *and* clean.
- Only the **selftest path** matters; live/`--deep`/`--regression` modes are outside the ruler's invocation.

## Headline prediction

| surface | host | clean_repeat | tz | locale | home | columns | predicted class |
|---|---|---|---|---|---|---|---|
| bash-surface-census | =clean* | =clean | =clean | =clean* | =clean | =clean | `invariant`, sensitive_to=[] |
| bash-checklist-run | =clean* | =clean | =clean | =clean* | =clean | =clean | `invariant`, sensitive_to=[] |
| bash-tsukuroi-census | =clean* | =clean | =clean | =clean* | =clean | =clean | `invariant`, sensitive_to=[] |
| bash-mado-verify | =clean | =clean | =clean | =clean | =clean | =clean | `invariant`, sensitive_to=[] (highest confidence) |
| tameshi-runner | =clean* | =clean | =clean | =clean* | =clean | =clean | `invariant`, sensitive_to=[] |

`*` = carries the host-profile interpreter-passthrough caveat (§Host passthrough) — `BASH_ENV`/`GLOBIGNORE` inherited from the invoking env would change child-bash behavior; not expected on this workstation, unverified. `=clean*` under locale is the profile most likely to produce the first observed delta (unpinned `sort` collation, §per-surface tables) — predicted no-op on the frozen fixtures, medium-high confidence.

Predicted stderr: empty for all five (all failure chatter rides stdout via `2>&1` captures or `st_bad`-style stdout prints; nothing writes stderr on the pristine pass). Predicted exit: 0 for all five. Predicted clean == clean_repeat (no clock/random token reaches selftest stdout/stderr anywhere — §nondeterminism audit).

## Per-surface env dependencies (line citations into pinned blobs)

### bash-surface-census — corpus/surface-census.sh @ fecee874

| line | dependency | mechanism | predicted F5 effect |
|---|---|---|---|
| :79 | `$HOME` | `ROOT="${HOME}"` default | none — selftest re-invokes verify with `--root "$R/host"` (:779-781; `--root` parse :95); home profile (/nonexistent) never consulted |
| :125 | `$HOME` (literal in TSV) | `resolve` maps `$HOME`→`$ROOT` | none — fixture TSVs use `$HOME/...` literals mapped to the `--root` fixture |
| :82-83 | PATH lookup | `THE_JANITOR_BIN`/`SQLITE3_BIN` defaults | none across profiles (PATH constant); selftest case 10 pins `SQLITE3_BIN` to a bad path deliberately |
| :259 | LC_COLLATE | `find … -print0 \| sort -z` orders the unlisted scan | none predicted — selftest unlisted sets are single-element (:780-786 cases); multi-element ASCII order agrees C vs en_US.UTF-8 [INFERENCE] |
| :274, :696 | `TMPDIR` | `mktemp -d "${TMPDIR:-/tmp}/…"` honors TMPDIR | none — path never printed on success; writable in every profile (/tmp is bwrap tmpfs; clean TMPDIR=/tmp/w/tmp) |
| :325 | (data, not env) | stderr note for >5-field rows | none — fixture shapes rows are exactly 5 fields |
| :494 | locale-insensitive | Python `sorted()` (codepoint order) | none — immune by construction |
| :497 | env read | `ONEPASSWORD_BROWSER_SUPPORT:-/opt/1Password/1Password-BrowserSupport` | none — probe 1 writes the NMH from the same env the expectation reads; consistent in host/clean [INFERENCE] |
| :610, :614, :625 | clock, `$HOME` | `date +%s` wall, `REC="$HOME/…"` — probe 6/7 | none — `--deep`-only; selftest re-invokes verbs without `--deep` (:826) → SKIP prints |
| :820-823 | PATH | janitor-absent → `skip-case` prints | none across profiles (PATH constant) |
| — | TZ / COLUMNS / LINES / TERM / tput | no usage | none |

### bash-checklist-run — corpus/checklist-run.sh @ fecee874

| line | dependency | mechanism | predicted F5 effect |
|---|---|---|---|
| :72 | `CHECKLIST_TIMEOUT` | `ROW_TIMEOUT=${CHECKLIST_TIMEOUT:-240}` | none — selftest re-pins it per re-invocation: `CHECKLIST_TIMEOUT="${CT:-240}"` (:416); host value cannot leak into child runs; parent never executes rows in selftest mode |
| :181, :341 | `TMPDIR` | `mktemp -d` (honors TMPDIR) | none — paths never printed on success; `missing tsv` case prints no path (:342 `--tsv "$d/nope.tsv"` asserts text only) |
| :194, :234 | LC_COLLATE | `sort \| uniq -d` on row ids / by-hand reasons | none predicted — dup lists are empty on clean fixtures; the dup-id / dup-reason cases yield exactly one equal element, order-invariant [INFERENCE] |
| :111, :159 | LC_CTYPE | `[[:space:]]` class, `tr -d '[:space:]'` | none — ASCII fixture text; C and en_US.UTF-8 agree on ASCII space family |
| :261 | PATH, `cd "$ROOT"` | `timeout "$ROW_TIMEOUT" bash -c "<row>"` after `cd "$ROOT"` | none — rows are `printf`/`sleep`/`exit`/`true`; `ROOT` = script parent (writable /tmp/w); the `the-janitor run -- printenv` fixture row is POLICY-refused by `DENY_CHECK` before execution (:86, :149-151, :381) |
| — | `$HOME` / TZ / date / COLUMNS / tput | no usage | none |

### bash-tsukuroi-census — tools/tsukuroi-census.sh @ 165307fe

| line | dependency | mechanism | predicted F5 effect |
|---|---|---|---|
| :140 | umask | `umask 077` (self-set) | none — not an env axis; fx hashes contents only (:735) |
| :591 | LC_COLLATE | `sort -u \| head -n 6 \| paste` on failed-unit names (unpinned — contrasts with pinned `LC_ALL=C sort` at :735) | none predicted — the selftest arm asserting sorted names (`failedhist=2\[bar\.service,foo\.service\]`, :868-871) has b<f in both C and en_US.UTF-8; ≤2 entries ⇒ `head -6` truncation never bites [INFERENCE, medium] — this is the line most likely to move first if any profile ever deltas |
| :630 | `TMPDIR` | `mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX` — hardcoded /tmp | none by construction (TMPDIR-immune) |
| :640, :731-745 | TSUKUROI_* env | stub dispatcher + `env TSUKUROI_PACMAN=… TSUKUROI_HOSTNAME_FILE=…` override block | none — the selftest overrides **every** probe command and file (host substrate unreachable in all profiles); `check` asserts `host=fixture-host` specifically to catch a host read (:755-757) |
| :947-948 | clock (`date -u`), hostname | live banner | none — selftest dispatch returns before the banner (:955-957); `date -u` is TZ-immune anyway |
| — | `$HOME` / COLUMNS / LINES / TERM / tput | no usage | none |

### bash-mado-verify — tools/mado-verify.sh @ eead56b2

| line | dependency | mechanism | predicted F5 effect |
|---|---|---|---|
| :61 | LC_ALL | `export LC_ALL=C` — **pins its own locale for every child** | none — locale profile cannot reach python3/grep/awk/sort inside this gate; strongest invariant of the five |
| :64-65 | `$HOME`, `MADO_VERIFY_ROOT/LIVE` | `ROOT="${MADO_VERIFY_ROOT:-$HOME}"` default | none — selftest children always pass `--root` (A :368, B :436, C :406) or exit at arg-parse (D); `LIVE auto` `$ROOT = $HOME` test (:1048) never reached (selftest dispatch :1041-1043) |
| :340 | `TMPDIR` | `mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX` — hardcoded /tmp | none by construction |
| :341 | `BASH` | `BASH_BIN="${BASH:-/bin/bash}"` | none — `BASH` is set by bash itself (shell var), identical in env -i; not an env read in practice |
| :367-369, :209 | LC_COLLATE | `find \| sort` unpinned | none — children inherit `LC_ALL=C` from :61 |
| :402-406 | PATH | sandbox built from `command -v` under the *parent* PATH (constant); child runs `env PATH="$SANDBOX" MADO_VERIFY_LIVE=yes` | none — same sandbox contents every profile |
| :753-756, :767 | `HYPRLAND_INSTANCE_SIGNATURE`, hyprctl | live-plane UNKNOWN reasons | none — scenario C's child PATH lacks hyprctl ⇒ reason is always `"hyprctl not on PATH"` (:753 fires first); the HIS check (:754-756) is unreachable in selftest; the `live checks unverified` detail (:767) is reason-independent, so `st_has … "unverified"` (:411) is stable |
| — | TZ / date / COLUMNS / tput | no usage | none |

### tameshi-runner — tools/mutate-and-run.sh @ 08175c6

| line | dependency | mechanism | predicted F5 effect |
|---|---|---|---|
| :167, :170 | — | `set -u -o pipefail`; `SELF=$(readlink -f BASH_SOURCE)` = /tmp/w/target.sh | fixed in every profile |
| :253-273 | `GIT_*` | `git_clean` derives `-u` list from live env | none — host profile pre-strips `GIT_*`; clean has none; scrub list empty in both |
| :280-292 | git identity/config | `fixture_commit` passes `-c user.name/-c user.email/-c commit.gpgsign=false` through `git_clean` | none — no reliance on `$HOME/.gitconfig` or `EMAIL`/`USER` env |
| :307 | locale/encoding | `py_helper` python3 heredoc (spec parse/apply) | none — specs are ASCII; default text encoding differs C vs UTF-8 but decodes identically for ASCII [INFERENCE] |
| :446, :450 | clock | `date +%s%N` durations | none — consumed inside nested run outputs (`$root/runN.out`), never on selftest stdout; not asserted |
| :455-458, :1281-1284 | PATH | `command -v python3/sha256sum/timeout/mktemp/git` gates | none — PATH constant across profiles; all present on this host |
| :474, :1289, :1391 | `TMPDIR` | `mktemp -d /tmp/tameshi-r4-2-*.XXXXXX` — hardcoded /tmp | none by construction; random suffix printed only on FAIL (`VERDICT: FAIL (scratch kept: …)` :1914-1916) |
| :489-490 | clock | `MUTATE_TOOL`/`MUTATE_DATE` (`date -u`) | none — sweep mode only, into nested out files |
| :1346, :1351 | env construction | regression legs embed `env -i PATH="$PATH" HOME=… TMPDIR=… LC_ALL=C GIT_CONFIG_NOSYSTEM=1 …` | none — `--regression` mode, not selftest |
| :1891-1892 | LC_COLLATE | `cut -f1 \| sort \| tr` on ledger ids (unpinned) | none predicted — leg ids are `[A-Z][0-9]`-shaped alnum (`D1`,`B10`,`K`,`S`), whose C and en_US.UTF-8 order agree [INFERENCE, medium] |
| :1903-1917 | — | selftest stdout = fixed `PASS/FAIL` lines + `MUTATE_SELFTEST: n/n` + `VERDICT: PASS` | deterministic; no timestamps/host/paths on success |
| — | `$HOME` / TZ / COLUMNS / tput | no usage | none |

## Nondeterminism audit (clean vs clean_repeat)

No surface prints clock, random, PID, or mktemp paths on the selftest success path:
checklist asserts text-only matches (:417-421); surface numbers cases with `%02d` (:765-833); tsukuroi prints fixed `PASS <label>` + `TSUKUROI_CENSUS_SELFTEST: PASS (N cases, …)` (:912-914); mado prints `MADO_SELFTEST: n/n assertions passed` (:441); runner's nested outputs (which contain dates/durations/`$root` paths) stay in files, and scratch is removed on PASS (:1913). Timed behavior exists only in runner run5 (`sleep 30` under `--timeout 2` → exit 124 classified INCONCLUSIVE, :1503-1547) — verdict-deterministic. Predicted clean == clean_repeat for all five.

## Host-profile passthrough risks (interpreter level, not script level)

- `BASH_ENV`: non-interactive `bash <script>` / `bash -c` sources it if exported. Host profile passes the invoking env (minus `GIT_*`) to all five entries and every nested `bash` child (checklist rows :261; surface re-invocations :779-781, :826-840; mado A/B/C; runner nested sweeps). If the invoking env ever exports `BASH_ENV`, host tuples can diverge arbitrarily. Same class: `GLOBIGNORE`, `SHELL` (only informational), `ENV` (POSIX sh only — not used). `IFS` is safe (bash re-initializes it).
- On this workstation the invoking shell is a plain login shell — none of these set [INFERENCE, unverified]; if an F5 probe ever shows host≠clean, check `BASH_ENV`/`GLOBIGNORE` first.

## Couplings the F5 ruler cannot see (useful for C2 mutation targets)

These `${VAR:-default}` reads are invisible to the 7 frozen profiles (none sets the VAR) — flipping such a default survives the whole ruler today:
checklist `CHECKLIST_TIMEOUT` (:72, but selftest re-pins :416); surface `THE_JANITOR_BIN`/`SQLITE3_BIN` (:82-83), `ONEPASSWORD_BROWSER_SUPPORT` (:497), `MUSKETEER_CHROME_PROFILE` (probe-local, set by the probe itself); mado `MADO_VERIFY_ROOT`/`MADO_VERIFY_LIVE` (:64-65), `BASH` (:341); tsukuroi `TSUKUROI_*` override family (:731-745, selftest-set); runner `GIT_*` (scrubbed). Conversely the two already-killable-by-profile axes — mado's `LC_ALL=C` pin (:61) and the unpinned sorts (surface :259, checklist :194/:234, tsukuroi :591, runner :1891-1892) — are where a `locale`-profile-reliant mutant would be caught if fixtures ever carried collation-divergent strings.

## Residual unknowns

- All predictions are source-derived, not executed (assignment constraint). The `[INFERENCE]`-tagged collation claims (identical ASCII ordering C vs en_US.UTF-8 on each fixture's data) are the only medium-confidence items; everything else is read off the pinned bytes.
- Host-profile `[INFERENCE]` rests on the invoking env being free of `BASH_ENV`/`GLOBIGNORE`; verify at probe time with `env | grep -E '^(BASH_ENV|GLOBIGNORE)='` if a host tuple ever mismatches.

Evidence: pinned sources at `/tmp/tameshi-r21-SC10GateEnvBash-x/surfaces/*.sh` (byte-verified); this report.
