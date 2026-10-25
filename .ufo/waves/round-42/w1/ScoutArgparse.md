# ScoutArgparse — S157: Python argparse docs (dest derivation, Namespace)

Access date: 2026-10-25. Source: https://docs.python.org/3/library/argparse.html

## Capture

- Command: `curl -fsSL https://docs.python.org/3/library/argparse.html -o /tmp/tameshi-r42-ScoutArgparse-snap/argparse.html`
- Snapshot: /tmp/tameshi-r42-ScoutArgparse-snap/argparse.html
- sha256: `3158c439e504752c93f582ddec59483a75c890411c1d3ee3b733125950bf93b7`
- Bytes: 328434
- Title (line 20): "argparse — Parser for command-line options, arguments and subcommands — Python 3.15.1 documentation" (page documents Python 3.15.1)

## Finding 1 — dest derived from optional argument string (anchor `#dest`)

- Anchor: `#dest` — `<section id="dest">` at HTML line 1490; h3 heading "dest" at line 1491; section closes line 1540.
- Verbatim (lines 1504–1505, 15 words): "For optional argument actions, the value of `dest` is normally inferred from the option strings."
- Verbatim (lines 1513–1514, 19 words): "Any internal `-` characters will be converted to `_` characters to make sure the string is a valid attribute name."
- Mechanism (lines 1506–1513): strip initial `-` characters from the first double-dash long option string; if none, first single-dash long option string; if none, first short option string; internal `-` → `_`. Version note (line 1538): "Changed in version 3.15: Single-dash long option now takes precedence over short options."
- Example `--foo-bar` → `foo_bar` (line 1517): `parser.add_argument('-f', '--foo-bar', '--foo')` → (line 1521) `Namespace(foo_bar='1', quz='2', x='3')`. Also quickstart example (lines 945–946): `parser.parse_args(['--foo-bar', 'FOO-BAR'])` → `Namespace(foo_bar='FOO-BAR')`.

## Finding 2 — parse_args returns a Namespace whose attributes are the dests

- Section anchor `#the-parse-args-method` (line 1645); method signature id `argparse.ArgumentParser.parse_args` (line 1648).
- Verbatim (lines 1650–1651, 17 words): "Convert argument strings to objects and assign them as attributes of the namespace. Return the populated namespace."
- Namespace: anchor `#the-namespace-object` (span id="namespace", line 1825); class id `argparse.Namespace` (line 1827).
- Verbatim (lines 1829–1830, 15 words): "Simple class used by default by `parse_args()` to create an object holding attributes and return it."
- Linking quote: dest = "The name of the attribute to be added to the object returned by `parse_args()`" (line 898–899). Quickstart (lines 320–321): "The `ArgumentParser.parse_args()` method runs the parser and places the extracted data in a `argparse.Namespace` object:".

## Tooling / installs

None — no tools installed or upgraded (curl, sha256sum, wc already present).

## Not checked

Nothing relevant outstanding; the live lane checkout was not edited.
