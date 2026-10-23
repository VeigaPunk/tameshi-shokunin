# BuildF6A — F6 fixture for survivor B5 (round 29, wave 1, seat BuildF6A)

**Verdict: the frozen C2 v2 target is unreachable as specified, and my evidence
independently agrees with the control seat's Q5 argument.** The blocker is
inside the pinned kagi declaration itself, not in my fixture: every `exec` row
in `corpus/surface-census.tsv` at `REV_BASH` declares mode `755`, so a file that
lacks the execute bit necessarily *also* fails the gate's exact-mode check, and
the B5 mutant then exits 1 instead of 0. I did **not** use environment tricks
(noexec mounts, TMPDIR, ACLs, ownership) to force a kill.

I shipped two variants so the L1 can choose without re-running anything:

| variant | census | counter result at its commit |
|---|---|---|
| `original/` + `minimized/` (**primary**) | pinned declaration **+ 1 probe row** | `anchored=0 kill_original=1 units_original=100 units_minimized=2 ddmin_match=1 kill=1 one_minimal=1` |
| `anchored-original/` + `anchored-minimized/` | pinned declaration, **byte-identical** | `anchored=1 kill_original=0 units_original=98 units_minimized=98 ddmin_match=0 kill=0 one_minimal=0` |

Artifacts: `.ufo/evidence/round-29/f6/BuildF6A/{original,minimized,anchored-original,anchored-minimized,gen.py,receipts.txt}`.
Generator (`gen.py`) builds and reduces both variants using the **frozen counter's own**
`Oracle`, `ddmin`, `materialize` and `b5_mutant` — imported, never reimplemented.

## 1. The contradiction, measured

### 1.1 The declaration under test

`REV_BASH = fecee8743e52eb8fb5fbb40782934cb619a1a96e` (from `tools/mutate-and-run.sh:606`),
`PIN_BASH = 275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` (`:605`).

```
$ git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show \
    fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.tsv | sha256sum
4af0dbcc81fdb7229f816bf23920174b1d699ba279405272fb78c5922f368992   (4752 bytes, no trailing newline)

$ … | grep $'\texec\t'
$HOME/.config/the-janitor/client.py	asset	exec	755	HTTP client: session-id, request timeout (the flock is in the CLI)
$HOME/.local/bin/the-janitor	asset	exec	755	the CLI (env overrides: CONFIG_DIR/STATE_DIR/ENV/PORT)
$HOME/.local/bin/tac-check	asset	exec	755	offline receipt check; --register never replaces
```

All three `exec` rows declare mode `755`. No `exec` row in the declaration
carries the unchecked mode `-` (only the `chrome-profile` **dir** row does).

### 1.2 The two gate checks that collide

Pinned gate `corpus/surface-census.sh`, `verify_surfaces` (lines 205-223 verbatim):

```bash
205:    case "$kind" in
...
210:      file|exec) if [[ "$live" != "regular" ]]; then
...
214:           if [[ "$kind" == "exec" && ! -x "$abs" ]]; then
215:             printf 'SURFACE DIVERGED %s (declared exec, no execute bit)\n' "$p"
216:             N_DIVERGED=$((N_DIVERGED + 1)); FAILED=1; continue
217:           fi ;;
218:    esac
219:    lmode="$(stat_mode "$abs")"
220:    if [[ "$mode" != "-" ]] && [[ "$lmode" != "$mode" ]]; then
221:      printf 'SURFACE DIVERGED %s (mode %s, declared %s)\n' "$p" "$lmode" "$mode"
222:      N_DIVERGED=$((N_DIVERGED + 1)); FAILED=1; continue
223:    fi
```

The pristine hits the exec token at `:215` only when the live file lacks the
execute bit. Because `:216` does `continue`, the pristine never reaches `:220`
for that row. But the **B5 mutant deletes exactly the `:214-217` arm**, so the
mutant falls straight through to `:220` and compares the same live mode against
the declared `755`. A live mode of `644` therefore yields, in the mutant:
`(mode 644, declared 755)` → `FAILED=1` → exit 1.

### 1.3 Exhaustive sweep over every reachable live state

The manifest mode field is `re.fullmatch(r'[0-7]{3,4}', mode)`
(`c2-measure-v2.py`, `materialize`), so every reachable live mode is a 3- or
4-digit octal string. I swept **all** of them, per exec row, on the **full
anchored fixture** (all 55 census rows + 22 host nodes live), with the counter's
own `Oracle`:

```
manifest-valid mode strings: 4608 (3-digit 512 + 4-digit 4096)
  .config/the-janitor/client.py   declared=755  pristine_hit=256  mutant_exit0=1  KILL=0
  .local/bin/the-janitor          declared=755  pristine_hit=256  mutant_exit0=1  KILL=0
  .local/bin/tac-check            declared=755  pristine_hit=256  mutant_exit0=1  KILL=0
TOTAL fixture states tested: 4608   KILL states: 0
```

The single `mutant_exit0` state per row is live mode `755` — the mode at which
the pristine does **not** hit the exec token. The 256 `pristine_hit` states per
row are the modes without the owner-execute bit; every one of them also trips
`:220` in the mutant. **Zero states satisfy both halves.**

Isolating the two halves (declared mode × live mode, one exec row, the
counter's `Oracle`):

```
declared live     pris_exit hit     mut_exit  KILL
755      644      1         True    1         False   ← pristine hits, mutant reports (mode 644, declared 755)
755      755      0         False   0         False   ← mutant clean, pristine silent
644      644      1         True    0         True    ← kill, but the row is NOT in the pinned declaration
-        644      1         True    0         True    ← kill, but mode '-' is not a pinned exec row
```

The kill needs a declared mode of `644` or `-` on the `exec` row; the pinned
declaration has neither. (The `-` form is what the historical kaika probe used:
`.ufo/evidence/kaika-round-1/coldread/probe-fixtures/probe/census.tsv` line 1 is
`$HOME/bin/tool	asset	exec	-	probe no-x exec`, and
`B-probe-B5-mutant.txt` shows `SURFACE OK $HOME/bin/tool (exec 644)` — the mutant
stayed clean exactly because the declared mode was unchecked.)

### 1.4 Reachability of the escape hatches (all excluded by instruction)

* **Ownership**: a root-owned `0755` file still has `o+x`, so `[[ -x ]]` stays
  true (`access(X_OK)` honours `o+x`). Measured: root-owned `0755` → `-x` TRUE;
  root-owned `0700` → `-x` FALSE, but then `stat -c %a` is `700`, which is
  neither the declared `755` nor a mode the counter's own regex forbids, and the
  row's live mode would still differ from the declaration.
* **ACLs** (`setfacl` is installed at `/usr/bin/setfacl`) and **noexec mounts**
  could make `-x` false while `stat -c %a` still prints `755`. The L1 note
  excludes all three explicitly, and none of them is the claimed craft.

So: **no fixture whose `original/census.tsv` is byte-identical to the pinned
declaration can satisfy the frozen predicate.** The two clauses
"census byte-identical to the pinned declaration" and "the fixture kills B5" are
mutually exclusive under the pinned gate's own logic.

## 2. What I did build (both variants, fully reduced)

### 2.1 Primary: `original/` + `minimized/` (kills B5, ddmin-reducible)

`original/census.tsv` = the pinned declaration **plus one appended row**:

```
$HOME/.local/bin/b5-probe	asset	exec	644	F6 probe row: declared mode 644, live file lacks the execute bit
```

Declared mode `644` matches the live mode, so the mutant's `:220` check stays
silent (`644 == 644`) while the pristine's `:214` arm fires on the missing
execute bit. `original/shapes.tsv` is 6 verbatim lines of the pinned
`corpus/state-shape.tsv` (all `mode` assertions on runtime paths that are absent
in the fixture, so they report `SHAPE ABSENT`, which is informational);
`original/baseline.tsv` is all 15 lines of the pinned `corpus/drift-baseline.tsv`
verbatim; `original/host.tsv` materialises every asset row of the pinned
declaration with its declared mode, all four `# scan` dirs, and the probe file at
mode `644`.

The pinned kagi **gate bytes** are untouched and read-only; the mutant is built
by the counter's own `b5_mutant()` from the runner's `@defect B5` spec
(`tools/mutate-and-run.sh:717-719`), mutant sha256
`1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c`.

Reduction with the counter's **own** `ddmin(units, orc.kills)`:

```
units_original=100  →  units_minimized=2   (30 oracle tests, 0.4 s wall)
one_minimal=1
```

`minimized/` — the four files, verbatim (52 + 106 + 0 + 0 bytes):

`minimized/census.tsv`
```
$HOME/.local/bin/b5-probe	asset	exec	644	F6 probe row: declared mode 644, live file lacks the execute bit
```
`minimized/shapes.tsv` — empty (0 bytes)
`minimized/baseline.tsv` — empty (0 bytes)
`minimized/host.tsv`
```
.local/bin/b5-probe	file	644	F6 fixture placeholder
```

### 2.2 Secondary: `anchored-original/` + `anchored-minimized/` (clause-1 conformant)

`anchored-original/census.tsv` is **byte-identical** to the pinned declaration
(sha256 `4af0dbcc…2f368992`, 4752 bytes, no trailing newline). Its host manifest
makes the pristine report drift on exactly **one** `exec` row
(`$HOME/.config/the-janitor/client.py`) whose live file lacks the execute bit —
the required "drift ONLY for one exec row". But the mutant then reports
`(mode 644, declared 755)` and exits 1, so `kill_original=0`. `ddmin` on this
fixture cannot reduce it (no subset ever kills), which is why
`anchored-minimized/` is identical to `anchored-original/` (98 units).

## 3. Counter receipts (frozen counter, lane clone, no GIT_* leakage)

Clone: `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/buildf6a-r29`,
checked out at `09e4f273dd54edea382ea03f098eecb3628331c3`. Fixture commits are
mine, in the clone only. No `jj` command was run anywhere; no lane Git index,
lane worktree or lane jj state was touched.

### 3.1 Primary variant, commit `7257bad00c652937710219f161dce77d0d692494`

```
$ timeout 1800 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
    python3 .ufo/evidence/round-29/c2-measure-v2.py --repo /tmp/buildf6a-r29 --rev HEAD
  oracle tests run: 33
C2_F6_V2: fixture=present anchored=0 kill_original=1 units_original=100 units_minimized=2 ddmin_match=1 kill=1 one_minimal=1 entry_sourced=0 quote_located=0 rev=7257bad00c652937710219f161dce77d0d692494
PREDICATE: C2_F6_V2_PASS=false
EXIT=1
```

`entry_sourced=0 quote_located=0` are the L1's to land; `anchored=0` is the
clause-1 conflict of §1.

### 3.2 Anchored variant, commit `f715e46a57b78598b6a3a7a79a6066754172bd30`

```
$ timeout 1800 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
    python3 .ufo/evidence/round-29/c2-measure-v2.py --repo /tmp/buildf6a-r29 --rev f715e46a57b78598b6a3a7a79a6066754172bd30
  oracle tests run: 1
C2_F6_V2: fixture=present anchored=1 kill_original=0 units_original=98 units_minimized=98 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=f715e46a57b78598b6a3a7a79a6066754172bd30
PREDICATE: C2_F6_V2_PASS=false
EXIT=1
```

### 3.3 Baseline (no fixture at the frozen lane commit)

```
$ … -u GIT_INDEX_FILE python3 .ufo/evidence/round-29/c2-measure-v2.py --repo /tmp/buildf6a-r29 --rev 09e4f273dd54edea382ea03f098eecb3628331c3
C2_F6_V2: fixture=absent anchored=0 kill_original=0 units_original=0 units_minimized=0 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=09e4f273dd54edea382ea03f098eecb3628331c3
PREDICATE: C2_F6_V2_PASS=false
EXIT=1
```

### 3.4 Pristine vs mutant on the primary original (verbatim, `receipts.txt`)

pristine, exit 1 — the exec token fires, and no other row drifts:
```
SURFACE OK       $HOME/.config/the-janitor/client.py (exec 755)
…
SURFACE DIVERGED $HOME/.local/bin/b5-probe (declared exec, no execute bit)
SURFACE_CENSUS: DRIFT (diverged=1 gone=0 link=0 unlisted=0 crosscheck=0 shape=0 unverified=0 ok=22 absent=18 skipped=0)
```
B5 mutant, exit 0 — the same row is clean because its declared mode `644`
matches its live mode:
```
SURFACE OK       $HOME/.local/bin/b5-probe (exec 644)
SURFACE_CENSUS: CLEAN (assets=21 runtime=15 scanned=4 ok=23 absent=18 skipped=0)
```

For the anchored variant the two runs differ only in the *second* line of the
exec row: pristine `(declared exec, no execute bit)` (exit 1) vs mutant
`(mode 644, declared 755)` (exit 1) — the mutant's own exit stays 1, which is
the whole of §1.

## 4. Smallest safe correction (for the L1; I changed nothing frozen)

The counter's own words decide this: `c2-measure-v2.py` reads the pinned
declaration via `PINNED = {'census.tsv': 'corpus/surface-census.tsv', …}` and
`anchored` compares `show(repo, rev, '…/original/census.tsv') == pinned['census.tsv']`
byte-for-byte. Two minimal options, in order of preference:

1. **Let the fixture's census carry the probe row and anchor the *rows*, not the
   file.** Change the anchored clause from "byte-identical to the pinned
   declaration" to "the pinned declaration's rows are a subset of the fixture's
   census rows" (mirroring how `shapes.tsv`/`baseline.tsv` are already checked:
   `set(orig['shapes.tsv']) <= set(lines_of(pinned['shapes.tsv']))`). Then the
   primary fixture above passes as-is: `anchored=1`, `kill_original=1`,
   `ddmin_match=1`, `kill=1`, `one_minimal=1`, 100 → 2 units.
2. **Anchor on the pinned `exec` row's *kind* rather than its mode.** The pinned
   declaration's `exec` rows all say `755`; if the anchored comparison ignored
   the mode column for `exec` rows, the anchored variant would still fail to
   kill (the mutant's `:220` still fires), so this option alone does not work —
   option 1 is the one that does.

I am not applying either: the counter is frozen before data, the amendment
route belongs to the L1, and re-scaling the claim is the L1's call, not mine.

## 5. Reproduce

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/buildf6a-r29
git -C /tmp/buildf6a-r29 checkout -q --detach 09e4f273dd54edea382ea03f098eecb3628331c3
python3 /tmp/buildf6a/artifacts/gen.py --out /tmp/buildf6a/rebuilt     # rebuilds + reduces both variants
# primary variant, as committed:
cp -r /tmp/buildf6a/rebuilt/probe/original    /tmp/buildf6a-r29/.ufo/evidence/round-29/f6/original
cp -r /tmp/buildf6a/rebuilt/probe/minimized   /tmp/buildf6a-r29/.ufo/evidence/round-29/f6/minimized
git -C /tmp/buildf6a-r29 add .ufo/evidence/round-29/f6
git -C /tmp/buildf6a-r29 -c user.name=b -c user.email=b@x commit -q -m "F6 fixture"
timeout 1800 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  python3 /tmp/buildf6a-r29/.ufo/evidence/round-29/c2-measure-v2.py --repo /tmp/buildf6a-r29 --rev HEAD
```

`gen.py` imports the frozen counter from
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/c2-measure-v2.py`
(sha256 `adc721f9260c87f34d444b7481c45db8e469178237a9e0f198d29cef440ada4c`, the
frozen value in `contract-amendment-1.json`) and reads the pinned kagi objects
read-only via `git show`.

## 6. Scope notes

* Writes: only `.ufo/evidence/round-29/f6/BuildF6A/**` and this report in the
  lane. No production file, corpus entry, contract or counter was edited. No
  `jj` command anywhere. Lane Git index and lane jj state untouched; all
  commits are in the private clone `/tmp/buildf6a-r29`.
* Tools: no installs were needed or performed. `setfacl`/`getfacl` were present
  already and were deliberately **not** used to force a kill.
* `entry_sourced` and `quote_located` are the L1's to land; I did not create
  `corpus/knowledge/survivor-fixture-minimization.md` or touch
  `corpus/SOURCES.md` / `corpus/lessons/round-29.md`.
* Peer note: builder B reported the same conclusion independently; my sweeps
  and receipts are separate runs of the frozen counter's own `Oracle`.
