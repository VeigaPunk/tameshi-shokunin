seat: ExecRows24

Round 45, wave 1, C1 row re-verification: S156, S157, S158, S159 (author of these ledger entries). All four fetched live 2026-10-25, quoted afresh from `measure.py --extract` output, and accepted by the frozen counter `--rev 3310e7be803516ca5934b4e949d91bcec824b179 --check`.

Rows read from `corpus/SOURCES.md` lines 126-129 (grep `^ {0,3}\| S15[6-9] `). URLs taken byte-exact from each row's source cell. Fetches: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows24/S###.raw '<url>'` (all rc=0 on first try). Normalized via `python3 .ufo/evidence/round-45/freshness/measure.py --extract S###.raw`; passages located at anchors, quotes copied verbatim from extract output.

## Per-row evidence

### S156 — https://pitest.org/faq/
- curl exit 0, 20845 bytes, sha256 ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1 (byte-identical to round-42 snapshot prefix ccf6ac49)
- CHECK S156 verified ok
- note: PIT FAQ still states the two-factor determinism caveat (timeouts, static initializers) exactly as teaches claims.
- Fragment:
```json
{"id":"S156","url":"https://pitest.org/faq/","opened":"2026-10-25","verdict":"holds","raw_sha256":"ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1","quote":"two factors might cause the results to differ slightly between two runs with the same input","snapshot":".ufo/evidence/round-45/freshness/sources/S156.raw.gz","author":"ExecRows24","note":"PIT FAQ still states the two-factor determinism caveat (timeouts, static initializers) exactly as teaches claims; page byte-identical to the round-42 snapshot (ccf6ac49 prefix)."}
```

### S157 — https://docs.python.org/3/library/argparse.html
- curl exit 0, 328434 bytes, sha256 421e389138e80a47df36df8501df89e68fe55ee03dc04816b85cd15c955352e4 (docs page hash changed since round-42 snapshot prefix 3158c439)
- CHECK S157 verified ok
- note: live argparse doc still says dest is inferred from option strings; underscore replacement and parse_args attribute assignment remain.
- Fragment:
```json
{"id":"S157","url":"https://docs.python.org/3/library/argparse.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"421e389138e80a47df36df8501df89e68fe55ee03dc04816b85cd15c955352e4","quote":"For optional argument actions, the value of dest is normally inferred from the option strings","snapshot":".ufo/evidence/round-45/freshness/sources/S157.raw.gz","author":"ExecRows24","note":"Live argparse doc still says dest is inferred from option strings; underscore replacement (with underscores _ replacing hyphens -) and parse_args attribute assignment remain, so teaches holds (page hash changed since round-42)."}
```

### S158 — https://github.com/hcoles/pitest/blob/f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6/pitest/src/main/java/org/pitest/mutationtest/DetectionStatus.java
- curl exit 0, 276935 bytes, sha256 51deedf9340ac8d9ba9a59385d75bb56ccd9705e7f8a00f33d84577426587bfe (GitHub blob page HTML; extract yields rendered Java source)
- CHECK S158 verified ok
- note: isDetected() exposes the detected flag; enum declares RUN_ERROR/TIMED_OUT true; getForErrorExitCode mapping intact.
- Fragment:
```json
{"id":"S158","url":"https://github.com/hcoles/pitest/blob/f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6/pitest/src/main/java/org/pitest/mutationtest/DetectionStatus.java","opened":"2026-10-25","verdict":"holds","raw_sha256":"51deedf9340ac8d9ba9a59385d75bb56ccd9705e7f8a00f33d84577426587bfe","quote":"public boolean isDetected () { return this . detected ; }","snapshot":".ufo/evidence/round-45/freshness/sources/S158.raw.gz","author":"ExecRows24","note":"isDetected() exposes the detected flag, and the enum above still declares RUN_ERROR and TIMED_OUT with true flags; getForErrorExitCode mapping intact, so teaches holds."}
```

### S159 — https://en.wikipedia.org/wiki/Mutation_testing
- curl exit 0, 170794 bytes, sha256 616dd5a510906c44e40c92c839ea7f8e2ed225967cde29b13d197d1baf92d71f (revid/content changed since round-43 snapshot prefix 6e4a06c0)
- CHECK S159 verified ok
- note: Wikipedia still calls equivalent-mutant detection one of the biggest obstacles to practical mutation testing; behaviorally-equivalent definition present.
- Fragment:
```json
{"id":"S159","url":"https://en.wikipedia.org/wiki/Mutation_testing","opened":"2026-10-25","verdict":"holds","raw_sha256":"616dd5a510906c44e40c92c839ea7f8e2ed225967cde29b13d197d1baf92d71f","quote":"Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing","snapshot":".ufo/evidence/round-45/freshness/sources/S159.raw.gz","author":"ExecRows24","note":"Wikipedia still calls equivalent-mutant detection one of the biggest obstacles to practical mutation testing with the behaviorally-equivalent definition, so teaches holds (page revid changed since round-43)."}
```

## Check commands and output (one deciding-seat counter run per fragment, --check mode)
```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecRows24/S156.json --snapdir /tmp/tameshi-r45-ExecRows24
CHECK S156 verified ok
$ ... S157 ...
CHECK S157 verified ok
$ ... S158 ...
CHECK S158 verified ok
$ ... S159 ...
CHECK S159 verified ok
```
All rc=0. All verdicts `holds`; none drifted, none unreachable. Raw fetch files kept at /tmp/tameshi-r45-ExecRows24/{S156,S157,S158,S159}.raw for L1 integration (gzip into .ufo/evidence/round-45/freshness/sources/).

No tools installed (no install needed). No lane mutations performed; lane is read-only except this report.
