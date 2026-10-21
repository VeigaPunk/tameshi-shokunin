# A06 — Receipt-window gate identity recomputation

## Findings

- Recomputed SHA-256 for `.ufo/evidence/round-20/stage/receipt-window.py`: `f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc`.
- The contract's `instruments.receipt-window.frozen_sha256` is the same value: `f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc`. Identity matches; difference: none.
- Copied the staged file to `/tmp/tameshi-r20-a06.fH79ko/receipt-window.py` and ran the requested `--selftest` from that sandbox. Full tally: `RECEIPT_WINDOW_SELFTEST: 20/20 pass`; reported selftest exit: `0`; difference from 20/20: `0` cases.

## Command and observed output

Command:

```sh
src=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py; sandbox=$(mktemp -d /tmp/tameshi-r20-a06.XXXXXX) && cp "$src" "$sandbox/receipt-window.py" && printf 'SOURCE_SHA256\n' && sha256sum "$src" && printf 'SANDBOX=%s\n' "$sandbox" && cd "$sandbox" && python3 receipt-window.py --selftest; rc=$?; printf 'SELFTEST_EXIT=%d\n' "$rc"; exit 0
```

Observed output:

```text
SOURCE_SHA256
f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py
SANDBOX=/tmp/tameshi-r20-a06.fH79ko
PASS [ 1/18] frozen receipt before the edit window is clean — CLEAN
PASS [ 2/18] installed receipt after the edit window is clean — CLEAN
PASS [ 3/18] missing instrument sha is refused — FAIL
PASS [ 4/18] unknown sha is refused — FAIL
PASS [ 5/18] missing interval is refused — FAIL
PASS [ 6/18] reversed interval is refused — FAIL
PASS [ 7/18] naive timestamp is refused — FAIL
PASS [ 8/18] frozen sha after the edit starts is refused — FAIL
PASS [ 9/18] installed sha before the edit ends is refused — FAIL
PASS [10/18] duplicate id is refused — FAIL
PASS [11/18] empty receipts is refused — FAIL
PASS [12/18] historical sha is classified, not gated — CLEAN
PASS [13/18] second historical sha is classified — CLEAN
PASS [14/18] identity instrument accepts a wave-time receipt — CLEAN
PASS [15/18] declared instrument mismatch is refused — FAIL
PASS [16/18] multi-receipt one-bad row fails the file — FAIL
PASS [17/18] frozen-sha receipt ending exactly at edit start is clean — CLEAN
PASS [18/18] installed-sha receipt starting exactly at edit end is clean — CLEAN
PASS [19/20] malformed contract is refused — CONTRACT_INVALID
PASS [20/20] malformed receipts is refused — RECEIPTS_INVALID
RECEIPT_WINDOW_SELFTEST: 20/20 pass
SELFTEST_EXIT=0
```

## Agreement and defects

**Agree** with the frozen receipt-window identity: recomputed and contract SHA-256 values match. The specified sandbox selftest passed all 20 cases with exit 0. No defects observed in this scoped identity check or selftest run. No production/evidence files were edited and no tools were installed.

## Follow-up — private measurement runner

### Findings

- Added `/tmp/tameshi-r20-a06-1Svz7G/lane/tools/receipt-measure.py` in a private clone checked out at the assigned frozen commit. Wrapper SHA-256: `a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa`; `wc -l` reported 318 lines.
- The wrapper delegates ordinary arguments to the unchanged staged `measure.py`, scrubbing inherited `GIT_*` variables and setting `PYTHONDONTWRITEBYTECODE=1` for the child. Its selftest creates isolated fixture Git repositories and exercises the public CLI with JSON output, stable six-item IDs, expected exits, clean 6/6, an independent negative case for each population item, malformed contract JSON, usage, and the historical `--check` rejection.
- `--check` is deliberately not shimmed. The effective published counting invocation is `python3 tools/receipt-measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --json`. The contract's older `stage/measure.py ... --check` command remains frozen historical command-error evidence.
- No installed or staged instrument, contract, or live production file was edited. No tests/build/lint were run, as directed; the wrapper selftest remains for L1's post-integration gate.

### Commands and observed output

Private clone command:

```sh
base=$(mktemp -d /tmp/tameshi-r20-a06-XXXXXX) && env -i HOME="$HOME" PATH="$PATH" LANG=C.UTF-8 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git clone --quiet --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin "$base/lane" && env -i HOME="$HOME" PATH="$PATH" LANG=C.UTF-8 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$base/lane" checkout --quiet --detach 6fd220bce3705498d1d1054e99e3cae73c203751 && printf 'PRIVATE_CLONE=%s/lane\n' "$base" && env -i HOME="$HOME" PATH="$PATH" LANG=C.UTF-8 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$base/lane" rev-parse HEAD
```

```text
PRIVATE_CLONE=/tmp/tameshi-r20-a06-1Svz7G/lane
6fd220bce3705498d1d1054e99e3cae73c203751
```

Runner identity command and output:

```sh
sha256sum /tmp/tameshi-r20-a06-1Svz7G/lane/tools/receipt-measure.py && wc -l /tmp/tameshi-r20-a06-1Svz7G/lane/tools/receipt-measure.py
```

```text
a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa  /tmp/tameshi-r20-a06-1Svz7G/lane/tools/receipt-measure.py
318 /tmp/tameshi-r20-a06-1Svz7G/lane/tools/receipt-measure.py
```

### Agreement and defects

**Agree** with the parent interface decision: keep the stage instrument bytes and predicates unchanged, omit `--check` compatibility, and distinguish the wrapper's `runner_sha256` from the underlying round20-measure instrument SHA (`f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d`). No runtime defects were observed because execution was intentionally deferred; the required L1 post-integration selftest is the outstanding verification.
