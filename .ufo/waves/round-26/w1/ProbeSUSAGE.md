# Probe S_USAGE — C1 survivor probe (round-26, wave 1)

**Verdict: the pristine pin and the S_USAGE mutant ARE DISTINGUISHED by a hermetic, off-suite probe.**
The discriminator is the **process exit status of a CLI invocation with an unknown flag**:
pristine exits **64**, the mutant exits **65**. stderr is byte-identical in both builds
(observed sha256 `e02bb0aab0c5c9fe4d9ef809f2e4cab3c87f90acc0f2797948f76154feb169a4`), so the exit
status is the only observable that separates them.

---

## 1. Scope and provenance

* Pinned source (opened this session, 2026-10-22):
  `/home/vgpnk/Projects/shokunin/kumitate-shokunin` @ `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`,
  path `scripts/cite-check.mjs`.
  Materialized read-only with
  `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs`.
  Localized quote (pin, line 71): `*   64 usage error. No file text, env value, or symbol body is ever printed.`
* Materialized bytes verified against the pre-registered blob digest:
  `sha256sum` → `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, `wc -l` → 2537 lines.
  This matches the digest and line count recorded in
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/cite-check/cite-check.defects.spec:2-3`.
* Mutation spec consumed (read this session, 2026-10-22):
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/cite-check/cite-check.defects.spec:49-52`

  ```
  49:# PREDICT SURVIVED — no hermetic case passes an unknown flag, so the usage exit code is unasserted.
  50:@defect S_USAGE | usage error exit 64 becomes 65
  51:@old     return 64;
  52:@new     return 65;
  ```

* Everything below ran in `/tmp/probe-susage/` (own scratch dir). Nothing ran in the lane repo,
  in `/home/vgpnk/Projects/shokunin/kumitate-shokunin`, or in any other lane. No `jj` command was
  issued anywhere. No git write command was issued. No production file was edited.

## 2. The mutant

Applied the spec `@old`/`@new` edit verbatim, one line, in the scratch copy only.

```
$ diff -u pristine/cite-check.mjs mutant/cite-check.mjs
@@ -2509,7 +2509,7 @@
   let opts;
   try { opts = parseArgs(process.argv.slice(2)); } catch (e) {
     process.stderr.write(`cite-check: ${e.message}\n\n${USAGE}`);
-    return 64;
+    return 65;
   }
```

```
$ sha256sum pristine/cite-check.mjs mutant/cite-check.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  pristine/cite-check.mjs
0ec5fff61e3c91e13a3b87b71106921633ebdf107e2e6fbb33a018cddfe3afcd  mutant/cite-check.mjs
```

`grep -c "return 64;"` on the pinned bytes → **1** (line 2512), so the `@old` anchor is unique and
the edit is unambiguous.

### Why an unknown flag reaches that line

Located in the pinned bytes (read this session, 2026-10-22):

* `scripts/cite-check.mjs:270` — `else throw new Error(\`unknown argument: ${a}\`);`
  (any argv token that is not one of the known flags throws here, inside the argv loop).
* `scripts/cite-check.mjs:2509-2513` — the catch block in `main()` that writes the message plus
  `USAGE` to stderr and returns the usage exit code.
* `scripts/cite-check.mjs:272-281` — `opts.fleet` defaulting and `resolveSrcDefault()` happen
  **after** the argv loop, so an unknown-flag throw fires before any filesystem resolution.
  The probe therefore needs no real source tree at all; the temp tree is pure scaffolding.

## 3. The probe (pasted verbatim)

Path: `/tmp/probe-susage/probe-susage.sh`

```bash
#!/usr/bin/env bash
# probe-susage.sh — hermetic OFF-SUITE probe for the S_USAGE mutant of
# kumitate scripts/cite-check.mjs @ rev 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a.
#
# S_USAGE: the usage-error exit code changes 64 -> 65.
#   cite-check.mjs:2510-2512 (pinned bytes)
#     try { opts = parseArgs(process.argv.slice(2)); } catch (e) {
#       process.stderr.write(`cite-check: ${e.message}\n\n${USAGE}`);
#       return 64;                 # mutant: return 65;
#     }
#
# parseArgs() throws `unknown argument: <arg>` for any flag it does not know
# (cite-check.mjs:270), so an UNKNOWN FLAG reaches that catch block without
# touching the filesystem at all: the throw happens during the argv loop, i.e.
# before resolveSrcDefault() is ever called (cite-check.mjs:280-281).
# The usage exit code is therefore observable with an empty temp tree and no
# --src/--self, which keeps the probe hermetic AND off-suite (never --selftest).
#
# The discriminator is the PROCESS EXIT STATUS (64 vs 65); stderr text is
# byte-identical between the two builds, so stderr alone cannot tell them apart.
#
# usage: bash probe-susage.sh <pristine.cite-check.mjs> <mutant.cite-check.mjs>

set -u

PRISTINE=${1:?path to pristine cite-check.mjs}
MUTANT=${2:?path to mutant cite-check.mjs}
NODE=${NODE_BIN:-$(command -v node)}

# --- hermetic temp tree -----------------------------------------------------
TREE=$(mktemp -d "${TMPDIR:-/tmp}/probe-susage.XXXXXXXX")
trap 'rm -rf "$TREE"' EXIT
mkdir -p "$TREE/self/corpus"
printf '# probe doc\n\nSee `scripts/cite-check.mjs` for details.\n' > "$TREE/self/SKILL.md"
printf '# corpus doc\n\nA citation to `scripts/cite-check.mjs:1` here.\n' > "$TREE/self/corpus/a.md"
mkdir -p "$TREE/src"
printf 'fn main() {}\n' > "$TREE/src/main.rs"

run() { # run <label> <script> <args...>
  local label=$1 script=$2; shift 2
  local out err status
  out=$(mktemp); err=$(mktemp)
  # env -i: no inherited env, no UFO_SRC, no HOME-dependent default resolution.
  env -i PATH=/usr/bin:/bin HOME="$TREE" "$NODE" "$script" "$@" >"$out" 2>"$err"
  status=$?
  printf '  %-8s argv=[%s]\n' "$label" "$*"
  printf '    exit   : %s\n' "$status"
  printf '    stdout : %s\n' "$(wc -c <"$out") bytes"
  printf '    stderr : %s\n' "$(head -n 1 "$err")"
  printf '    sha256(stderr) : %s\n' "$(sha256sum "$err" | cut -d' ' -f1)"
  rm -f "$out" "$err"
  return 0
}

echo "=== PROBE S_USAGE (off-suite, unknown flag) ==="
echo "node        : $NODE ($("$NODE" --version))"
echo "pristine    : $PRISTINE"
echo "mutant      : $MUTANT"
echo "temp tree   : $TREE"

echo
echo "--- case 1: unknown flag (discriminator) ---"
run pristine "$PRISTINE" --no-such-flag
run mutant   "$MUTANT"   --no-such-flag

echo
echo "--- case 2: unknown flag with a valid --src/--self pair (still a usage error) ---"
run pristine "$PRISTINE" --src "$TREE/src" --self "$TREE/self" --bogus-flag
run mutant   "$MUTANT"   --src "$TREE/src" --self "$TREE/self" --bogus-flag

echo
echo "--- case 3: flag missing its directory argument (same catch block) ---"
run pristine "$PRISTINE" --src
run mutant   "$MUTANT"   --src

echo
echo "--- case 4: control, --help (exit 0 in both builds, not a usage error) ---"
run pristine "$PRISTINE" --help
run mutant   "$MUTANT"   --help
```

## 4. Observed output — both builds (verbatim)

```
$ cd /tmp/probe-susage && bash probe-susage.sh "$PWD/pristine/cite-check.mjs" "$PWD/mutant/cite-check.mjs"
=== PROBE S_USAGE (off-suite, unknown flag) ===
node        : /run/user/1000/fnm_multishells/3758_1792655796355/bin/node (v24.21.0)
pristine    : /tmp/probe-susage/pristine/cite-check.mjs
mutant      : /tmp/probe-susage/mutant/cite-check.mjs
temp tree   : /tmp/probe-susage.HiykxuQG

--- case 1: unknown flag (discriminator) ---
  pristine argv=[--no-such-flag]
    exit   : 64
    stdout : 0 bytes
    stderr : cite-check: unknown argument: --no-such-flag
    sha256(stderr) : e02bb0aab0c5c9fe4d9ef809f2e4cab3c87f90acc0f2797948f76154feb169a4
  mutant   argv=[--no-such-flag]
    exit   : 65
    stdout : 0 bytes
    stderr : cite-check: unknown argument: --no-such-flag
    sha256(stderr) : e02bb0aab0c5c9fe4d9ef809f2e4cab3c87f90acc0f2797948f76154feb169a4

--- case 2: unknown flag with a valid --src/--self pair (still a usage error) ---
  pristine argv=[--src /tmp/probe-susage.HiykxuQG/src --self /tmp/probe-susage.HiykxuQG/self --bogus-flag]
    exit   : 64
    stdout : 0 bytes
    stderr : cite-check: unknown argument: --bogus-flag
    sha256(stderr) : c0f082204a8229d61a3ac98cbe00e2660460736a578c65cfee66ae883512616b
  mutant   argv=[--src /tmp/probe-susage.HiykxuQG/src --self /tmp/probe-susage.HiykxuQG/self --bogus-flag]
    exit   : 65
    stdout : 0 bytes
    stderr : cite-check: unknown argument: --bogus-flag
    sha256(stderr) : c0f082204a8229d61a3ac98cbe00e2660460736a578c65cfee66ae883512616b

--- case 3: flag missing its directory argument (same catch block) ---
  pristine argv=[--src]
    exit   : 64
    stdout : 0 bytes
    stderr : cite-check: --src requires a directory
    sha256(stderr) : 716a9e57974aea274af59dad54170ba815961d64f7cbcf86c1782ce7ad80d396
  mutant   argv=[--src]
    exit   : 65
    stdout : 0 bytes
    stderr : cite-check: --src requires a directory
    sha256(stderr) : 716a9e57974aea274af59dad54170ba815961d64f7cbcf86c1782ce7ad80d396

--- case 4: control, --help (exit 0 in both builds, not a usage error) ---
  pristine argv=[--help]
    exit   : 0
    stdout : 1103 bytes
    stderr : 
    sha256(stderr) : e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  mutant   argv=[--help]
    exit   : 0
    stdout : 1103 bytes
    stderr : 
    sha256(stderr) : e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### 4b. The two discriminating invocations, run separately (verbatim)

```
$ TREE=$(mktemp -d /tmp/probe-susage-run.XXXX)
$ for s in pristine mutant; do env -i PATH=/usr/bin:/bin HOME="$TREE" node /tmp/probe-susage/$s/cite-check.mjs --no-such-flag; echo "exit=$?"; done

===== pristine =====
cite-check: unknown argument: --no-such-flag

usage: node scripts/cite-check.mjs [options]
... (usage text, 1103 bytes, identical in both runs) ...
exit=64

===== mutant =====
cite-check: unknown argument: --no-such-flag

usage: node scripts/cite-check.mjs [options]
... (usage text, 1103 bytes, identical in both runs) ...
exit=65
```

## 5. Why the suite misses it (confirmation, not inference)

The mutant survives the hermetic suite, as the pre-registered prediction states:

```
$ env -i PATH=/usr/bin:/bin HOME=/tmp/probe-susage node /tmp/probe-susage/mutant/cite-check.mjs --selftest
...
62/62 cases passed (hermetic)
VERDICT: PASS
selftest-exit=0
```

(`grep -c "^PASS"` → 62, `grep -c "^FAIL"` → 0.)

A scan of the pinned bytes for any assertion on the usage exit code finds only the doc comment and
the return itself — the two occurrences of `64` that matter are `scripts/cite-check.mjs:71`
(`64 usage error.`) and `scripts/cite-check.mjs:2512` (`return 64;`). No hermetic case spawns the
CLI with an unknown flag, so the exit status is never observed by the suite. That is precisely the
hole the pre-registered spec predicted at `cite-check.defects.spec:49`.

Note (secondary observation): the mutant also silently breaks the header contract at
`scripts/cite-check.mjs:71`, which still documents `64 usage error` while the binary now returns 65.
The header is prose, so no machine check catches that either.

## 6. Smallest safe correction (for the lane integrator; not applied by this seat)

No production file was edited by this seat. The smallest safe correction is to make the usage exit
code a machine-checked value rather than an inline literal, so the hermetic suite can assert it:

1. Name the code once, e.g. `const EXIT_USAGE = 64;` next to `USAGE`
   (`scripts/cite-check.mjs:227`), and `return EXIT_USAGE;` at `scripts/cite-check.mjs:2512`.
2. Add one hermetic case that runs the CLI with an unknown flag in a temp tree and asserts
   `status === EXIT_USAGE` — the probe in section 3 is exactly that case, minus the mutant.

If the lane prefers no source change, the equivalent fix is a single hermetic case that spawns the
script with `--no-such-flag` and asserts exit status 64, with the expected code kept as a literal
in the case. Either way the assertion must live in the hermetic group so it runs under
`node "$MUTANT" --selftest`.

## 7. Evidence index (all opened this session, 2026-10-22)

| Fact | Where |
| --- | --- |
| Pinned blob digest `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines | `git show` of kumitate rev `1205c662…` → sha256sum/wc -l, observed above |
| `return 64;` occurs exactly once, at line 2512 | `grep -c "return 64;"` → 1 |
| Unknown flag throws inside the argv loop | `scripts/cite-check.mjs:270` (pin) |
| Usage exit returned from `main()` catch | `scripts/cite-check.mjs:2509-2513` (pin) |
| Default src resolution happens after the argv loop | `scripts/cite-check.mjs:272-281` (pin) |
| Mutation spec S_USAGE @old/@new | `.ufo/evidence/round-26/cite-check/cite-check.defects.spec:49-52` |
| Mutant passes the hermetic suite (62/62) | `node mutant/cite-check.mjs --selftest` in `/tmp/probe-susage` |

## 8. Risks and blockers

* Risk: none to the lane — this seat wrote only this report file, plus scratch bytes under
  `/tmp/probe-susage/` (pristine copy, mutant copy, probe script, captured selftest output).
* Risk for the integrator: the suggested correction touches `scripts/cite-check.mjs` in the
  sibling lane `/home/vgpnk/Projects/shokunin/kumitate-shokunin`, which is read-only for this
  fleet wave. That change is the lane integrator's call, not this seat's.
* Blockers: none. The probe runs entirely in `/tmp` with `env -i`, node v24.21.0 already present.
* Tooling: no package was installed or upgraded in this session; no tooling change was needed
  (node v24.21.0 already on PATH).

PROBE S_USAGE: DISTINGUISHED
