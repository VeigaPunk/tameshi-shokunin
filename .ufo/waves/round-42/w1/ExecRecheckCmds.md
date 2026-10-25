# ExecRecheckCmds — recheck commands for candidate rows S155/S156/S157

Access date: 2026-10-25. Three recheck commands written and run now; each
returns count 1, exit 0. No `|` inside any grep string. Snapshots saved under
/tmp/tameshi-r42-ExecRecheckCmds-snap/ (sha256 + bytes below).

## Findings

### S155 — PIT basic concepts (`https://pitest.org/quickstart/basic_concepts/`)
- Command (run now):
  `curl -fsSL 'https://pitest.org/quickstart/basic_concepts/' | grep -c 'there were no tests that exercised the line of code'`
- Output: `1`; pipeline exit: `0`.
- Located quote (verbatim, §"No coverage"): "No coverage is the same as
  Survived except there were no tests that exercised the line of code where the
  mutation was created." — raw snapshot line 179 (snapshot sha256
  c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a, 12155 B;
  title "Basic concepts").
- Census-schema recheck cell: `180d` (valid cadence per corpus/SOURCES.md
  recheck column; matches e.g. S001/S003).

### S156 — PIT FAQ (`https://pitest.org/faq/`)
- Command (run now):
  `curl -fsSL 'https://pitest.org/faq/' | grep -c 'two factors might cause the results to differ slightly between two runs'`
- Output: `1`; pipeline exit: `0`.
- Located quote (verbatim, §"Is it random?" → §Timeouts): "Pitest works hard
  to be fully deterministic, but two factors might cause the results to differ
  slightly between two runs with the same input." — raw snapshot line 293
  (snapshot sha256 ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1,
  20845 B; title "FAQ").
- Census-schema recheck cell: `180d`.

### S157 — Python argparse docs (`https://docs.python.org/3/library/argparse.html`)
- Command (run now):
  `curl -fsSL 'https://docs.python.org/3/library/argparse.html' | grep -c 'The name of the attribute to be added to the object returned'`
- Output: `1`; pipeline exit: `0`.
- Located quote (verbatim, anchor `#dest`): "The name of the attribute to be
  added to the object returned by `parse_args()`" — raw snapshot line 898
  (snapshot sha256 3158c439e504752c93f582ddec59483a75c890411c1d3ee3b733125950bf93b7,
  328434 B; title "argparse — Parser for command-line options, arguments and
  subcommands — Python 3.15.1 documentation"; identical sha256 to sibling
  ScoutArgparse snapshot).
- Census-schema recheck cell: `180d`.

## Census-schema recheck cells (summary)
| row | source | recheck cell |
|---|---|---|
| S155 | https://pitest.org/quickstart/basic_concepts/ | 180d |
| S156 | https://pitest.org/faq/ | 180d |
| S157 | https://docs.python.org/3/library/argparse.html | 180d |

`180d` is a valid cadence in the 11-column corpus/SOURCES.md registry schema
(recheck column; values in the registry include 90d/180d/365d/730d/on-release/
on-change). No `|` appears in any cell.

## Could not check
- The lane's live corpus/SOURCES.md does not yet hold rows S155-S157 (they are
  drafted by the ScribeRows seat this wave); command strings above are chosen
  to keep working once those rows land.
