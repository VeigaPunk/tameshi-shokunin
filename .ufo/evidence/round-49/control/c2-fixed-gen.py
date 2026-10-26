#!/usr/bin/env python3
"""Round-49 C2 control CTL_FIX: the cheapest generator that skips generation.

It implements the frozen generator interface but only replays the guard's own selftest fixtures
(the 4 analysis fixtures and 10 map cases of tools/staged-id-guard.py's selftest) through the CLI,
comparing each output with a golden recorded from the pristine guard (embedded FIXTURES, also
kept as c2-fixed-fixtures.json).
Scored by the frozen C2 counter with --generator-path, it shows how many panel mutants a
fixture-only test confirms; it must not reach the C2 target.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

FIXTURES = json.loads(r'''[
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n  | S002 | Gamma docs \u2014 https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n| S004 | Delta docs \u2014 https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": null,
  "golden_exit": 1,
  "golden": "{\"cascade\": [\"S004\"], \"cascade_count\": 1, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [], \"column0_miss\": [\"S002\"], \"extractor\": \"0-3space\", \"held\": {}, \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S005\", \"staged_max\": \"S004\", \"staged_rows\": 2, \"unmapped\": [], \"verdict\": \"refused\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S002 | EXAMPLE.test/alpha \u2014 Alpha again | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": null,
  "golden_exit": 0,
  "golden": "{\"cascade\": [], \"cascade_count\": 0, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [\"S002\"], \"column0_miss\": [], \"extractor\": \"0-3space\", \"held\": {\"S002\": \"S001\"}, \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": false, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S004\", \"staged_max\": \"S002\", \"staged_rows\": 1, \"unmapped\": [], \"verdict\": \"answered\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S002 | nothing here | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": null,
  "golden_exit": 1,
  "golden": "{\"cascade\": [], \"cascade_count\": 0, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [\"S002\"], \"column0_miss\": [], \"extractor\": \"0-3space\", \"held\": {}, \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S004\", \"staged_max\": \"S002\", \"staged_rows\": 1, \"unmapped\": [\"S002\"], \"verdict\": \"refused\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source |\n|---|---|\n| S002 | x |\n",
  "map": null,
  "golden_exit": 2,
  "golden": "{\"reason\": \"staged:3 malformed row S002 (2 cells)\", \"verdict\": \"setup_refusal\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n  | S002 | Gamma docs \u2014 https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n| S004 | Delta docs \u2014 https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S010"
   }
  },
  "golden_exit": 0,
  "golden": "{\"analysis_refused\": true, \"cascade\": [\"S004\"], \"cascade_count\": 1, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [], \"column0_miss\": [\"S002\"], \"extractor\": \"0-3space\", \"held\": {}, \"map_below_floor\": [], \"map_clash\": [], \"map_dedupe\": {}, \"map_entries\": 1, \"map_floor\": \"S005\", \"map_held_moved\": [], \"map_ok\": true, \"map_reasons\": [], \"map_staged_clash\": [], \"map_targets\": 1, \"map_uncovered\": [], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": false, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S005\", \"staged_max\": \"S004\", \"staged_rows\": 2, \"unmapped\": [], \"verdict\": \"admitted\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n  | S002 | Gamma docs \u2014 https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n| S004 | Delta docs \u2014 https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S001"
   }
  },
  "golden_exit": 1,
  "golden": "{\"analysis_refused\": true, \"cascade\": [\"S004\"], \"cascade_count\": 1, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [], \"column0_miss\": [\"S002\"], \"extractor\": \"0-3space\", \"held\": {}, \"map_below_floor\": [], \"map_clash\": [\"S001\"], \"map_dedupe\": {}, \"map_entries\": 1, \"map_floor\": \"S005\", \"map_held_moved\": [], \"map_ok\": false, \"map_reasons\": [\"map targets collide with registry ids: S001\"], \"map_staged_clash\": [], \"map_targets\": 1, \"map_uncovered\": [], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S005\", \"staged_max\": \"S004\", \"staged_rows\": 2, \"unmapped\": [], \"verdict\": \"inadmissible\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n  | S002 | Gamma docs \u2014 https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n| S004 | Delta docs \u2014 https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S004"
   }
  },
  "golden_exit": 1,
  "golden": "{\"analysis_refused\": true, \"cascade\": [\"S004\"], \"cascade_count\": 1, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [], \"column0_miss\": [\"S002\"], \"extractor\": \"0-3space\", \"held\": {}, \"map_below_floor\": [], \"map_clash\": [], \"map_dedupe\": {}, \"map_entries\": 1, \"map_floor\": \"S005\", \"map_held_moved\": [], \"map_ok\": false, \"map_reasons\": [\"map targets are still staged ids: S004\"], \"map_staged_clash\": [\"S004\"], \"map_targets\": 1, \"map_uncovered\": [], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S005\", \"staged_max\": \"S004\", \"staged_rows\": 2, \"unmapped\": [], \"verdict\": \"inadmissible\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n  | S002 | Gamma docs \u2014 https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n| S004 | Delta docs \u2014 https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S010",
    "S004": "S011"
   }
  },
  "golden_exit": 0,
  "golden": "{\"analysis_refused\": true, \"cascade\": [\"S004\"], \"cascade_count\": 1, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [], \"column0_miss\": [\"S002\"], \"extractor\": \"0-3space\", \"held\": {}, \"map_below_floor\": [], \"map_clash\": [], \"map_dedupe\": {}, \"map_entries\": 2, \"map_floor\": \"S005\", \"map_held_moved\": [], \"map_ok\": true, \"map_reasons\": [], \"map_staged_clash\": [], \"map_targets\": 2, \"map_uncovered\": [], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": false, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S005\", \"staged_max\": \"S004\", \"staged_rows\": 2, \"unmapped\": [], \"verdict\": \"admitted\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S002 | EXAMPLE.test/alpha \u2014 Alpha again | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S001"
   }
  },
  "golden_exit": 0,
  "golden": "{\"analysis_refused\": false, \"cascade\": [], \"cascade_count\": 0, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [\"S002\"], \"column0_miss\": [], \"extractor\": \"0-3space\", \"held\": {\"S002\": \"S001\"}, \"map_below_floor\": [], \"map_clash\": [], \"map_dedupe\": {\"S002\": \"S001\"}, \"map_entries\": 1, \"map_floor\": \"S004\", \"map_held_moved\": [], \"map_ok\": true, \"map_reasons\": [], \"map_staged_clash\": [], \"map_targets\": 1, \"map_uncovered\": [], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": false, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S004\", \"staged_max\": \"S002\", \"staged_rows\": 1, \"unmapped\": [], \"verdict\": \"admitted\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S002 | EXAMPLE.test/alpha \u2014 Alpha again | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S010"
   }
  },
  "golden_exit": 1,
  "golden": "{\"analysis_refused\": false, \"cascade\": [], \"cascade_count\": 0, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [\"S002\"], \"column0_miss\": [], \"extractor\": \"0-3space\", \"held\": {\"S002\": \"S001\"}, \"map_below_floor\": [], \"map_clash\": [], \"map_dedupe\": {}, \"map_entries\": 1, \"map_floor\": \"S004\", \"map_held_moved\": [\"S002\"], \"map_ok\": false, \"map_reasons\": [\"map moves a held document off its registry id: S002 -> S010 (registry S001)\"], \"map_staged_clash\": [], \"map_targets\": 1, \"map_uncovered\": [], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S004\", \"staged_max\": \"S002\", \"staged_rows\": 1, \"unmapped\": [], \"verdict\": \"inadmissible\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S002 | nothing here | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S010"
   }
  },
  "golden_exit": 1,
  "golden": "{\"analysis_refused\": true, \"cascade\": [], \"cascade_count\": 0, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [\"S002\"], \"column0_miss\": [], \"extractor\": \"0-3space\", \"held\": {}, \"map_below_floor\": [], \"map_clash\": [], \"map_dedupe\": {}, \"map_entries\": 1, \"map_floor\": \"S004\", \"map_held_moved\": [], \"map_ok\": false, \"map_reasons\": [\"map decides an undocumented row: S002\"], \"map_staged_clash\": [], \"map_targets\": 1, \"map_uncovered\": [], \"map_undocumented\": [\"S002\"], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S004\", \"staged_max\": \"S002\", \"staged_rows\": 1, \"unmapped\": [\"S002\"], \"verdict\": \"inadmissible\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n  | S002 | Gamma docs \u2014 https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n| S004 | Delta docs \u2014 https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S003",
    "S004": "S003"
   }
  },
  "golden_exit": 1,
  "golden": "{\"analysis_refused\": true, \"cascade\": [\"S004\"], \"cascade_count\": 1, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [], \"column0_miss\": [\"S002\"], \"extractor\": \"0-3space\", \"held\": {}, \"map_below_floor\": [], \"map_clash\": [\"S003\", \"S003\"], \"map_dedupe\": {}, \"map_entries\": 2, \"map_floor\": \"S005\", \"map_held_moved\": [], \"map_ok\": false, \"map_reasons\": [\"map is not injective (two staged rows share a target)\", \"map targets collide with registry ids: S003,S003\"], \"map_staged_clash\": [], \"map_targets\": 1, \"map_uncovered\": [], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S005\", \"staged_max\": \"S004\", \"staged_rows\": 2, \"unmapped\": [], \"verdict\": \"inadmissible\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n  | S002 | Gamma docs \u2014 https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n| S004 | Delta docs \u2014 https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {}
  },
  "golden_exit": 1,
  "golden": "{\"analysis_refused\": true, \"cascade\": [\"S004\"], \"cascade_count\": 1, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [], \"column0_miss\": [\"S002\"], \"extractor\": \"0-3space\", \"held\": {}, \"map_below_floor\": [], \"map_clash\": [], \"map_dedupe\": {}, \"map_entries\": 0, \"map_floor\": \"S005\", \"map_held_moved\": [], \"map_ok\": false, \"map_reasons\": [\"map does not cover every collision: S002\"], \"map_staged_clash\": [], \"map_targets\": 0, \"map_uncovered\": [\"S002\"], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S005\", \"staged_max\": \"S004\", \"staged_rows\": 2, \"unmapped\": [], \"verdict\": \"inadmissible\"}"
 },
 {
  "registry": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S001 | Alpha docs \u2014 https://example.test/alpha | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S002 | Beta docs \u2014 https://example.test/beta | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n| S003 | Kappa docs \u2014 https://example.test/kappa | docs | A | x | y | z | mined | 2026-01-01 | 180d | \u2014 |\n",
  "staged": "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n  | S002 | Gamma docs \u2014 https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n| S004 | Delta docs \u2014 https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | \u2014 |\n",
  "map": {
   "map": {
    "S002": "S010",
    "S003": "S010"
   }
  },
  "golden_exit": 1,
  "golden": "{\"analysis_refused\": true, \"cascade\": [\"S004\"], \"cascade_count\": 1, \"collision_count\": 1, \"collisions\": [\"S002\"], \"column0_collisions\": [], \"column0_miss\": [\"S002\"], \"extractor\": \"0-3space\", \"held\": {}, \"map_below_floor\": [], \"map_clash\": [], \"map_dedupe\": {}, \"map_entries\": 2, \"map_floor\": \"S005\", \"map_held_moved\": [], \"map_ok\": false, \"map_reasons\": [\"map is not injective (two staged rows share a target)\", \"map names a row the package does not carry: S003\"], \"map_staged_clash\": [], \"map_targets\": 1, \"map_uncovered\": [], \"map_undocumented\": [], \"naive_map\": {\"S002\": \"S004\"}, \"next_free\": \"S004\", \"refused\": true, \"registry_docs\": 3, \"registry_max\": \"S003\", \"registry_rows\": 3, \"safe_floor\": \"S005\", \"staged_max\": \"S004\", \"staged_rows\": 2, \"unmapped\": [], \"verdict\": \"inadmissible\"}"
 }
]''')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--guard', required=True)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--cases', type=int, required=True)
    ap.add_argument('--dump', required=True)
    a = ap.parse_args()
    fixtures = FIXTURES
    run = 0
    bad = None
    with open(a.dump, 'w', encoding='utf-8') as dump, tempfile.TemporaryDirectory() as d:
        for i in range(a.cases):
            f = fixtures[i % len(fixtures)]
            dump.write(json.dumps({'index': i, 'registry': f['registry'], 'staged': f['staged'],
                                   'map': f['map']}) + '\n')
            run += 1
            rp, sp = os.path.join(d, 'r'), os.path.join(d, 's')
            open(rp, 'w', encoding='utf-8').write(f['registry'])
            open(sp, 'w', encoding='utf-8').write(f['staged'])
            argv = [sys.executable, '-I', a.guard, '--registry', rp, '--staged', sp]
            if f['map'] is not None:
                mp = os.path.join(d, 'm')
                json.dump(f['map'], open(mp, 'w'))
                argv += ['--map', mp]
            p = subprocess.run(argv + ['--json'], capture_output=True)
            try:
                js = json.loads(p.stdout)
                js = {k: v for k, v in js.items() if k not in ('registry_sha256', 'staged_sha256')}
                got = json.dumps(js, sort_keys=True)
            except ValueError:
                got = p.stdout.decode()
            if p.returncode != f['golden_exit'] or got != f['golden']:
                bad = i
                break
    print('PBT_STAGED_ID: cases=%d violations=%d counterexample=%s control=CTL_FIX'
          % (run, 0 if bad is None else 1, 'none' if bad is None else bad))
    return 0 if bad is None else 1


if __name__ == '__main__':
    sys.exit(main())
