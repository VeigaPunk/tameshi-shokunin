#!/usr/bin/env python3
"""Argv-preservation stub: prints repr(sys.argv), exits 0 with BOUND token.
Used to evidence how the frozen counter's list-argv invocation delivers the
space-containing path to the tool."""
import sys
print('ARGV_REPR=' + repr(sys.argv))
print('EXECUTOR_SOURCE_BOUND')
sys.exit(0)
