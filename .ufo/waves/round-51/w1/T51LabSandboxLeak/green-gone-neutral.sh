#!/usr/bin/env bash
# T51LabSandboxLeak — minimal GREEN: K_GONE_ARM under a neutral sandbox name
# (sandbox-n2). The sandbox path contains no verdict word, so the gate's
# unanchored `grep -q GONE` cannot be satisfied by a printed scratch path:
# selftest reports FAIL (1/13, "symbol gone: no /GONE/ in output"), exit 1.
# The mutant is killed — the survival in RED is a suite artifact.
set -u
MUTANT="${1:?usage: green-gone-neutral.sh <mutant.sh> <work-root>}"
WRAP="${2:?usage: green-gone-neutral.sh <mutant.sh> <work-root>}"
h="$WRAP/sandbox-n2"
mkdir -p "$h/home" "$h/tmp"
cd "$h" || exit 99
exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C \
  GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" \
  bash "$MUTANT" --selftest
