# [seat ColdReadLesson34] — r34-w1 cold-read re-crediting of `corpus/lessons/round-34.md`

Scope: Gate rows (S101 url/quote/digest vs committed snapshot; quote located in the snapshot body),
the Mistakes entry's evidence pointers, the Holds list vs `corpus/lessons/round-33.md`'s v3 list.
Lane tip under audit: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (detached clone, read-only).
No tool/counter edits; no deciding-run re-execution (kill rule consumed); the counter was not invoked.

## Verified pins (fresh sha256, this session)

```
git -C lane rev-parse HEAD                                   -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
git show 0b99d48:tools/tally-audit-v2.py > tool.py           -> sha256 7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  == PIN
git show 0b99d48:tools/mutate-and-run.sh > pristine.sh       -> sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  == PIN
sha256sum .ufo/evidence/round-33/c1/c1-measure.py            -> f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c        == PIN (amendment 6)
sha256sum corpus/lessons/round-34.md                         -> 737d4ff98e49dfa3531452ef10be12e231b519fa35374c3040e15bf8174477de
```

## Gate row S101 — AGREES, two cosmetic footnotes

- URL `https://mutation-testing.org/`: matches SOURCES.md:109 (`git -C lane show 0b99d48:corpus/SOURCES.md | grep '| S101'`).
- Digest claim: `sha256sum .ufo/evidence/round-34/src/s101-mutation-testing.html` -> `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420` == Gate row and SOURCES row; `wc -c` -> `4341` == "4,341 bytes".
- Quote located in snapshot body: committed bytes lines 44–46 inside `<h1 id="overview">Overview</h1>` ordered list (snapshot:40–48). The quote "exporting source-code mutants; suppressing equivalent mutants; computing the mutant-detection rate and the set of live mutants" is verbatim, joined across items 2–4; it is a prefix of item 4 which continues "for a given set of tests;". `grep -n 'mutant-detection\|live mutants\|suppressing' s101-mutation-testing.html` -> 44/45/46/53.
- Rejection claims: TLDP ABS copy present as evidence-only — `.ufo/evidence/round-34/src/s101b-abs-exit-status.html`, `wc -c` -> 9728, sha256 `60cebcc8c8d41ae936136a79f7b94f773fbf09399a31fb32ce722bde992bd291` — matches the row's `60cebcc8…d291`; confirmed not rowed (`grep -c '^| S' corpus/SOURCES.md` -> 98; only S101 added).
- "rows 97 -> 98": `git show 66e1fb44:corpus/SOURCES.md | grep -c '^| S'` -> 96 at base (r33 added S100 -> 97; r34 -> 98). "No other cell changed" verified: `git diff c17e593b..0b99d48 -- corpus/SOURCES.md` -> exactly one insertion, the S101 row.
- Knowledge entry cites S097 + S101 as claimed: `grep -n 'S097\|S101' corpus/knowledge/witness-equivalence-rule.md` -> lines 57, 61, 62, 65.
- Commit-order claims in the preamble verified by `git log --oneline 66e1fb44..0b99d48`: `6aaad5b` (amendment 6, set-aware witness gate) -> `9dd3174` (controls receipt at amended rev) -> `c17e593b` (sealed set 8+6) -> `0b99d48` (deciding-run receipt + lesson). `git merge-base --is-ancestor 66e1fb44 0b99d48; echo $?` -> 0.
- Deciding-run files byte-match the dispatched receipt: `.ufo/evidence/round-34/measure/c1-deciding-run.exit` = `0`; `.stdout` = `C1_R33: tool_present=1 ... C1_R33_PASS=true` (single line, identical to the receipt under verification).
- Census-end flags S101 as `tameshi W01 S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md` — the tier-C row is honestly flagged in `.ufo/evidence/round-34/census-end.stdout`, consistent with the row's tier.

### F1 (low): wrong-shaped receipt cited for the gnu.org timeout
Gate: "unreachable from this host (two timeouts, receipt `.ufo/evidence/round-34/src/s101-fetch.exit`)".
`cat` of that file -> `MUT_EXIT=0` (11 bytes): an exit-0 line for the *S101 mutation-testing.org fetch*, not a timeout record. The timeout itself is corroborated secondhand by SOURCES.md S097:106 ("rendered page … timed out on 2026-10-23"), so the rejection reason stands; only the cited receipt does not document the two timeouts. Reproduce: `cat .ufo/evidence/round-34/src/s101-fetch.exit`.

### F2 (low): quote word count 15 -> actual 16
Gate claims "(Overview feature list, 15 words)"; whitespace tokenization gives 16
(`echo 'exporting source-code mutants; suppressing equivalent mutants; computing the mutant-detection rate and the set of live mutants' | wc -w` -> 16). Same cosmetic class as the r33 routed defect 4 (S100 claimed 17, actual 14). ≤25-word contract satisfied; quote verbatim.

### F3 (observation): S101 used-by convention
S100's row lists `corpus/lessons/round-33.md` in used-by; S101's row omits `corpus/lessons/round-34.md` though the r34 lesson cites it. The Gate text only claims the witness-equivalence-rule used-by, which matches the row — no lesson-vs-row drift; a registry-convention asymmetry between rows.

## Mistakes entry — AGREES, one pointer lands on a rewritten file

- Mechanism: shipped sealed copy `.ufo/evidence/round-33/heldout/ho-kill-vector-setup-threshold.json` edits `if [[ $nsetup -gt 0 ]]` -> `-gt 1` with witness `vector [2,0,0,0,0,0,0,0,0]` — the fixed single-setup vector the entry describes (`cat` output quoted: `"old": "  if [[ $nsetup -gt 0 ]]; then\n", "new": "  if [[ $nsetup -gt 1 ]]; then\n"`, `"vector": [2,0,0,0,0,0,0,0,0]`). With one setup leg, pristine prints SETUP while the mutant prints PASS => tool FAIL => KILL (committed `authoring-receipts.json` shows `["KILL",1,"TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)"], as_expected:true`); two setups `[2,2,0,...]` tie on SETUP => `(False,'vector')` reject — consistent with the set-aware gate's `KV-block-identical -> (False, 'block-identical')`-style refusals in `witness-probes.json`.
- The caught first generation IS preserved in-repo, but in the sibling transcript, not the cited file: `.ufo/evidence/round-34/dev/authoring.stdout` line 8 records `{"id": "ho-kill-vector-setup-threshold", ... "witness": [false, "vector"], ... "as_expected": false}` and the run's tail `SEALED: kill=8 accept=6 all_as_expected=False`. Committed `authoring-receipts.json` contains only the final generation (all 14 `as_expected: true`) — the entry's pointer "`authoring-receipts.json` first generation, preserved in the scratch transcript" lands on a file that was overwritten; the evidence resolves via `authoring.stdout`. Reproduce: `grep -n 'as_expected.: false' .ufo/evidence/round-34/dev/authoring.stdout` and `python3 -c 'import json;print(sum(not r["as_expected"] for r in json.load(open(".ufo/evidence/round-34/dev/authoring-receipts.json"))))'` -> 0.
- "captured-by: the pre-data authoring harness (witness gate + real tool per copy)": corroborated — the stdout line pairs the rejected witness with the real tool result in the same record, pre-commit (sealed copies were committed at c17e593b after this).

## Holds (routed to round 35) — AGREES, nothing dropped, nothing invented

Byte-level compare of the v3 residue classes:

- r34 Holds: "Guard-2 divisibility, TallyArms-02 coexistence, quoted case subject, helper-function refactors, per-index record parsing, preamble seeding, nonzero-leg stress, all-pairs nlegs recompute".
- r33 append (round-33.md:155-158) NOT-adopted list: identical eight classes, same order — verbatim match.
- r34 adds "whole-stdout comparison already landed as the r33 DevPrintf fix" — consistent: r33's own v3 list (round-33.md:132) appended "whole-stdout comparison (DevPrintf ninth fix)" and the r33 lesson's DevPrintf bullet records the landed fix. Present-but-annotated-landed, not dropped.
- "tool pin frozen at `7b11ba25…8d10`" == verified pin sha256 above.
- Cold-read hold carried verbatim-in-substance from r33 ("LedgerAudit sized ~19 SOURCES-citing sections + 3 all-four in r33" == r33:134); this seat consumes the lessons portion.
- Calibration hold ("r33 baseline 64/64 restraint 8") == r33:89 ("monitor baseline 64/64 restraint 8").

## Residual risk / gaps

- The gnu.org timeout is asserted, not receipted: F1's mis-pointed file leaves the claim resting on S097's secondhand note; an `exit=124`-style receipt would close it.
- `authoring.stdout` records the rejection pair but not the rejected `[2,2,0,...]` vector itself (the JSON it prints lacks the witness array) — the first-witness detail remains scratch-transcript-only.
- SCORECARD.md/LOG.md appends landed in the same commit (0b99d48 stat: +36/+28) are outside this seat's envelope; another seat owns them.

Verdict: lesson AGREES with landed bytes on every substantive claim (digests, byte counts, row diffs, sealed-copy mechanism, holds parity, receipt text, commit order). Findings are cosmetic/pointer-quality only: F1 wrong-shaped receipt citation, F2 word count off-by-one, F3 used-by asymmetry; Mistakes pointer drift noted but evidence resolves via `authoring.stdout`.
