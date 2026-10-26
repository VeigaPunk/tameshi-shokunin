# T50ScribeEntryDraft — source and probe receipts

Seat: T50ScribeEntryDraft (scribe, round 50 wave 1). All commands run 2026-10-26 from
/home/vgpnk/Projects/shokunin with scratch `S=/fast/scratch/hyaku/tameshi-r50/T50ScribeEntryDraft`.
No counter was run; nothing under /home/vgpnk/.local/state was read; the lane checkout was not modified.

## 1. S_ZH (Zeller & Hildebrandt, IEEE TSE 28(2):183-200, 2002) — new row, opened this round

```
$ cd "$S" && curl -fsSL --max-time 60 -o delta.pdf 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf'
$ ls -l delta.pdf
-rw-r--r-- 1 vgpnk vgpnk 247738 Oct 26 19:18 delta.pdf
$ sha256sum delta.pdf
7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa  delta.pdf
$ pdftotext delta.pdf delta-raw.txt && sed -n '10,18p;64,72p' delta-raw.txt
line that caused the failure. The case study required 139 automated test
runs, or 35 minutes on a 500 MHz PC.
...
Simplification of test cases. Our minimizing delta debugging
algorithm ddmin is fed with a failing test case, which it simplifies by successive testing. It stops when a minimal test case
is reached, where removing any single input entity would cause
the failure to disappear.
```

Snapshot copied to `.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/delta-debugging.pdf`,
247738 B, sha256 `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`.

## 2. S022 (MacIver & Donaldson, ECOOP 2020) — held lane row, abstract re-read

```
$ curl -fsSL --max-time 60 -o ecoop.html 'https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13'
$ # title found on the page:
Test-Case Reduction via Test-Case Generation: Insights from the Hypothesis Reducer (Tool Insights Paper)
$ curl -fsSL 'https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13' | grep -c 'test-case validity problem'
3
```

Abstract sentences used, verbatim from the extracted page text
(`.ufo/waves/round-50/w1/T50ScribeEntryDraft.src/ecoop2020-abstract.txt`):

> The key idea of internal test-case reduction is that instead of applying test-case reduction
> externally to generated test cases, we apply it internally, to the sequence of random choices made
> during generation
> It also significantly mitigates the impact of the test-case validity problem, by ensuring that any
> reduced test case is one that could in principle have been generated.

## 3. S024 (The Fuzzing Book) — held lane row, snapshot re-read

```
$ sha256sum .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html
3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99  .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html
$ sed 's/<[^>]*>//g' .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html | tr -s ' \n' ' ' | grep -c 'every character contained is required to produce the error'
1
```

Raw HTML of the sentence (`grep -n` on the snapshot, tag-stripped):

> Its result is 1-minimal, meaning that every character contained is required to produce the error;
> removing any (as seen in tests #27 and #29, above) no longer makes the test fail.

The book's own text omits the noun after "removing any" in this snapshot; the entry quotes only the
clause before it.

## 4. Shrinker probes (tool selftest, not the frozen counter)

Tool under test: `.ufo/waves/round-50/w1/T50ExecShrinker.shrink-case.py` (629 lines, mode 755,
28590 B), the L1's copy source for `tools/shrink-case.py`.

```
$ export TMPDIR="$S"; cd <lane>/.ufo/waves/round-50/w1
$ python3 -I T50ExecShrinker.shrink-case.py --selftest   # beside it: no staged-id-guard.py
...
SELFTEST panel M02 end to end                                 skip (no staged-id-guard.py beside this tool)
SHRINK_SELFTEST: cases=14 failed=0
exit=0
```

```
$ # fixture layout mirroring the lane: $S/fake/tools/{shrink-case.py,staged-id-guard.py,pbt-staged-id.py}
$ # and $S/fake/.ufo/evidence/round-49/c2/panel.json
$ cd "$S/fake/tools" && python3 -I shrink-case.py --selftest
...
SELFTEST M02: the run count equals the logged invocations     ok
SHRINK_SELFTEST: cases=21 failed=0
exit=0
```

The frozen counter copies only `pbt-staged-id.py` beside the shrinker into its tool dir
(`.ufo/evidence/round-50/c2/measure.py:227-230`), which is the first layout, so the measured
`--selftest` exit is the 14-case run with the real-guard leg skipped.

## 5. Frozen control receipt quoted in the entry (last line only; no mutant ids or edits)

```
$ tail -1 .ufo/evidence/round-50/control/c2-CTL_REF.stdout
C2_R50: self=c3da7e59abf2 rev=1d8b0923f83f8e9fa552c1835dc610ccaf715304 mutants=20 ok=20 units_before=164 units_after=43 entry=1 readme_f6=1 shrinker_absent=0 gen_pin=0 guard_pin=0 panel_invalid=0 unfound=0 ok_short=0 no_reduction=0 records_bad=0 selftest_bad=0 total=0 C2_R50_PASS=true
$ cat .ufo/evidence/round-50/control/c2-selftest.stdout
C2_R50_SELFTEST: cases=9 failed=0
```

## 6. Pins re-checked on the lane tree (read-only)

```
$ sha256sum tools/staged-id-guard.py tools/pbt-staged-id.py
03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8  tools/staged-id-guard.py
0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05  tools/pbt-staged-id.py
$ sha256sum .ufo/evidence/round-49/c2/panel.json
d6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1  .ufo/evidence/round-49/c2/panel.json
```

## 7. Tooling

No tool installed or upgraded for this seat; `curl` (system), `pdftotext` (poppler, system) and
`python3` 3.14 were used as found.
