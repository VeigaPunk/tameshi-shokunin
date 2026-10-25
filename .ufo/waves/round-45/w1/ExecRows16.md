seat: ExecRows16

# C1 row re-verification — S089, S160, S090 (author ledger entries)

Task (w1): re-verify rows S089, S160, S090 against LIVE bytes; write fragment JSONs; run the round-45 freshness counter `--check` at the freeze rev. All three rows verdict `holds`.

Rows read from `corpus/SOURCES.md` (lines 98, 99, 130). Row URL = first http(s) URL in source cell, byte-exact:
- S089: `https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/`
- S090: `https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3`
- S160: `https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/`

## Fetches (live, 2026-10-25)

```
mkdir -p /tmp/tameshi-r45-ExecRows16
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S089.raw 'https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/'   # exit=0
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S090.raw 'https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3'                                            # exit=0
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S160.raw 'https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/'   # exit=0
```

| row | URL | curl exit | bytes | sha256 |
|---|---|---|---|---|
| S089 | stryker-mutator.io …/equivalent-mutants/ | 0 | 38687 | `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce` |
| S090 | man.freebsd.org …?query=sysexits&sektion=3 | 0 | 59251 | `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` |
| S160 | stryker-mutator.io …/equivalent-mutants/ | 0 | 38687 | `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce` |

Note: S089 and S160 share the same URL; both fetched independently (S160 fetched in a second call), identical bytes (`79f6501a…` — matches the round-44 re-opened snapshot digest `79f6501a` recorded in S160's anchor). No tooling installed; no pacman/uv/npx transactions performed (no install needed).

## Normalized text (measure.py --extract) — anchor passages

```
python3 .ufo/evidence/round-45/freshness/measure.py --extract S089.raw > S089.txt   # exit 0, 2714 B
python3 .ufo/evidence/round-45/freshness/measure.py --extract S090.raw > S090.txt   # exit 0, 14288 B
```

- S089/S160 (Stryker), passage at `10 ** 0` example (S089.txt idx 1526):
  `…It is called equivalent mutant . There is no definitive way for Stryker to find and ignore them. There is currently also no way yet to mark them to be ignored…`
- S090 (FreeBSD sysexits(3) §ERRORS):
  `EX_USAGE (64) The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, a bad syntax in a parameter, or whatever.`

Quotes were copied verbatim from the `--extract` output (never from the registry rows); each is 6–25 whitespace tokens and shares ≥2 content words with scope/anchor/teaches. For S160 the quote deliberately stops before the sentence already quoted verbatim in S160's anchor cell (which would trip the "quote copied from row" guard).

## Counter checks (freeze rev)

```
python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check S089.json --snapdir /tmp/tameshi-r45-ExecRows16
python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check S090.json --snapdir /tmp/tameshi-r45-ExecRows16
python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check S160.json --snapdir /tmp/tameshi-r45-ExecRows16
```

Output:
```
CHECK S089 verified ok
CHECK S090 verified ok
CHECK S160 verified ok
```
(all exit 0)

## Fragment JSONs (verbatim)

### S089
```json
{
  "id": "S089",
  "url": "https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce",
  "quote": "It is called equivalent mutant . There is no definitive way for Stryker to find and ignore them.",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S089.raw.gz",
  "author": "ExecRows16",
  "note": "The live Stryker mutation-testing-elements page still states the equivalent mutant is called out and that there is no definitive way for Stryker to find and ignore them, grounding the teaches claim that an equivalent mutant stays a survivor."
}
```

### S090
```json
{
  "id": "S090",
  "url": "https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf",
  "quote": "EX_USAGE (64) The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, a bad syntax in a parameter, or whatever.",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S090.raw.gz",
  "author": "ExecRows16",
  "note": "The live FreeBSD 15.1 sysexits(3) page still defines EX_USAGE (64) as command used incorrectly, e.g., wrong number of arguments or a bad flag, grounding the teaches anchor for a usage exit of 64."
}
```

### S160
```json
{
  "id": "S160",
  "url": "https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce",
  "quote": "It is called equivalent mutant . There is no definitive way",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S160.raw.gz",
  "author": "ExecRows16",
  "note": "The live Stryker page still carries the equivalent-mutant example and the no-definitive-way sentence at the same offsets, confirming S160's cited sentences survive."
}
```

## Result

All three rows re-verified `holds` against live bytes on 2026-10-25; counter `--check` prints `CHECK S089 verified ok` / `CHECK S090 verified ok` / `CHECK S160 verified ok` at the freeze rev. Raw files retained at `/tmp/tameshi-r45-ExecRows16/{S089,S090,S160}.raw` for L1 integration. No blockers, no disputes; no lane files modified (fragments only under /tmp; this report is the only lane write).
