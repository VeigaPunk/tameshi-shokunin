#!/usr/bin/env python3
"""SCRATCH ADVERSARIAL HARNESS C -- always-accept control (contrast).
Exits 0 with BOUND for every input. Used only to show the frozen counter
DOES gate always-accept behavior, in contrast to harnesses A/B which pass
24/24 despite being unsound on the empty-blob surface.
"""
import sys
print('EXECUTOR_SOURCE_BOUND')
sys.exit(0)
