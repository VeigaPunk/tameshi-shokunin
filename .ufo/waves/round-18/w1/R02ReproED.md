# R02 — P01/P02 before-state reproduction

## Finding

C2's claimed before-state is **not falsified** for either requested probe. At base `183f87b899e6cae46be98d251cbc87fb5118f6ca`, pristine `--selftest` passes, and each single guard-removal mutant also exits 0 with all 56 selftests passing. Under the assigned probe contract, both are `open`.

## Evidence

All mutations and selftests ran in `/tmp/tameshi-r18w1-R02ReproED-XfJ860/fleet/tameshi-shokunin`, a fleet-mirror clone. Setup used:

```sh
W=$(mktemp -d /tmp/tameshi-r18w1-R02ReproED-XXXXXX)
mkdir "$W/fleet"
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" "$W/fleet/"
done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$W/fleet/tameshi-shokunin"
git -C "$W/fleet/tameshi-shokunin" checkout -q --detach 183f87b899e6cae46be98d251cbc87fb5118f6ca
```

Observed `HEAD=183f87b899e6cae46be98d251cbc87fb5118f6ca`. The file hash was `f8f05c7aa601cf0b6f0907cc1ead2fc01acaad6a3c19e81888c084a969583e27`; `git diff --stat eb7838b16490ca7ba17ea3242ade76a61f744af2 183f87b899e6cae46be98d251cbc87fb5118f6ca -- tools/evidence-disposition.py` was empty, confirming the target file matches the round-17 source.

The two guards occur at `tools/evidence-disposition.py:445` and `:552`:

- **P01 / G3 tag-object guard, line 445:** `if proc.returncode != 0 or resolved != rev:` was replaced once with `if False:`. Match count: 1.
- **P02 / G5 symlink-mode guard, line 552:** `if kind != "blob" or mode not in TREE_MODES:` was replaced once with `if kind != "blob":`. Match count: 1.

Each mutated SHA-256 matched its round-17 recorded mutant hash, respectively `272d89cac17469344ff72223e5e94269fd468360e626425c17cafb8c863c9d45` and `6f01c1f9775c24cd4c15227978000f2ae0899d54540e2cb6af5e99d999a1b503`. The temporary harness restored the exact pristine bytes after each run; each restored hash returned to `f8f05c7aa601cf0b6f0907cc1ead2fc01acaad6a3c19e81888c084a969583e27`.

| Run | Command / mutation | Exit | Tally | Probe result |
|---|---|---:|---|---|
| Pristine | `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR timeout 300 python3 tools/evidence-disposition.py --selftest` | 0 | `SELFTEST: PASS (56/56)` | Baseline passes |
| P01 | Line 445 replacement above; same command | 0 | `SELFTEST: PASS (56/56)` | **open** (mutant survives) |
| P02 | Line 552 replacement above; same command | 0 | `SELFTEST: PASS (56/56)` | **open** (mutant survives) |

Each run had empty stderr and no `SELFTEST_CASE ... FAIL` lines. The Python harness removed every inherited `GIT_*` variable from the subprocess environment (none remained); the command also explicitly unset `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, and `GIT_COMMON_DIR`. Host tools observed: Python 3.14.8, Git 2.56.0. No tools installed.

Verdict: holds — at the pinned base, both P01 and P02 are open under the specified selftest-exit contract.