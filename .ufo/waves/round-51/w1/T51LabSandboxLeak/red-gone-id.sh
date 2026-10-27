#!/usr/bin/env bash
# T51LabSandboxLeak — minimal RED: K_GONE_ARM under the sweep's id-named
# sandbox (sandbox-$DEFECT_ID). The sandbox path embeds "GONE", so the gate's
# unanchored `grep -q GONE` over captured output (which prints scratch paths)
# is satisfied by the path itself: selftest reports PASS (13/13), exit 0.
set -u
MUTANT="${1:?usage: red-gone-id.sh <mutant.sh> <work-root>}"
WRAP="${2:?usage: red-gone-id.sh <mutant.sh> <work-root>}"
h="$WRAP/sandbox-K_GONE_ARM"
mkdir -p "$h/home" "$h/tmp"
cd "$h" || exit 99
exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C \
  GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" \
  bash "$MUTANT" --selftest
