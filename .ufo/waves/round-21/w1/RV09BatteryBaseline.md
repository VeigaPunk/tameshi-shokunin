done

# Findings

- Full registered battery at frozen base: **36/36 active rows held**; registry-check exit **0**. The frozen `tools/registry.json` has 40 rows total: 36 active and 4 superseded. JSON reports `rev_resolved` as `33d03b716d3edcf1d8656d46d6df61801d232c52`.
- No active row failed. The three unheld observations are all `status: superseded` and excluded from the 36-row denominator: `evidence-disposition-round17` (expect 0, got 2), `evidence-disposition-round17-before` (expect 1, got 2), and `evidence-disposition-round14-superseded` (expect 0, got 2). Each output reports `expected_input_digest_mismatch` for `tools/bash-witness-study.py` (observed SHA-256 `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12`, expected `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`). The fourth superseded row, `trace-inputs-round17-selftest`, returned 0.
- The authoritative run used a branch-aligned scratch mirror with read-only links for sibling fleet entries. Parent-reported SM4 result (22/23, exit 2) came from a scratch clone without those links; that failure was not reproduced with the assigned dependency-available layout. The observed active baseline is 36/36, not a regression. The superseded digest mismatches above remain visible but are not active-row failures.

# Commands and exits

Scratch mirror creation (exit 0):

```sh
git clone -q --no-hardlinks --branch master /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-RV09BatteryBaseline-x/fleet/tameshi-shokunin
```

Clone HEAD was already `33d03b716d3edcf1d8656d46d6df61801d232c52`. Read-only sibling symlink setup exited 0:

```sh
cd /tmp/tameshi-r21-RV09BatteryBaseline-x/fleet
for p in /home/vgpnk/Projects/shokunin/*; do n=$(basename "$p"); if [ "$n" != "tameshi-shokunin" ] && [ ! -e "$n" ]; then ln -s "$p" "$n"; fi; done
```

Battery command (registry-check exit 0; GIT_* variables unset before invocation):

```sh
cd /tmp/tameshi-r21-RV09BatteryBaseline-x/fleet/tameshi-shokunin
for name in $(compgen -e); do case "$name" in GIT_*) unset "$name";; esac; done
TMPDIR=/tmp/tameshi-r21-RV09BatteryBaseline-scratch python3 tools/registry-check.py --root /tmp/tameshi-r21-RV09BatteryBaseline-x/fleet/tameshi-shokunin --rev 33d03b716d3edcf1d8656d46d6df61801d232c52 --json > /tmp/tameshi-r21-RV09BatteryBaseline-scratch/battery.stdout.json 2> /tmp/tameshi-r21-RV09BatteryBaseline-scratch/battery.stderr.txt
```

Captured trailer: `REGISTRY_CHECK: held=36/36 superseded=4`.

Superseded-row excerpt:

```text
ROW evidence-disposition-round17 superseded expect=0 got=2
"kind": "expected_input_digest_mismatch"
"message": "tools/bash-witness-study.py: observed 8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12 expects 49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80"
```

# Evidence and residual risk

- Full JSON report: `.ufo/waves/round-21/w1/battery-baseline.json` (`schema: tameshi-registry-check-report-v1`, active `held: 36`, `total: 36`, `superseded: 4`). Its SHA-256 matches the captured stdout: `5b2cc16f922f546ffd548dbfd26b4e7139fb47b209a45a7cf00e3fdf6a897bf4`.
- Captured stderr in scratch: `/tmp/tameshi-r21-RV09BatteryBaseline-scratch/battery.stderr.txt`; captured checker exit: `/tmp/tameshi-r21-RV09BatteryBaseline-scratch/battery.exit` (`0`).
- Residual: the three superseded evidence-disposition rows still emit the stale digest mismatch shown above; no active-row impact was observed. No tools were installed or updated.
