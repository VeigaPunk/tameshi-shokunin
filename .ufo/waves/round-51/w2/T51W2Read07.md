# T51W2Read07 — cold-read re-key reader: `### Reading a receipt — the discipline`

- Seat: `T51W2Read07` · Round 51 wave 2 (falsify) · Lane `tameshi-shokunin`
- CAND `6d8c11e378aa90b12650808e1b79270742935f15` · BASE `9962033fd7a75aa2f2847e979dd687a5d28505a1`
- Read-only seat: no lane/fleet/sibling mutations; scratch `/fast/scratch/hyaku/tameshi-r51/T51W2Read07/` (deleted before yield); the only fixture git ops ran inside a `git clone --shared` whose `rev-parse --show-toplevel` was asserted before use.

## Section resolution (re-resolved at CAND; fixture list not trusted)

- Heading `### Reading a receipt — the discipline` — **monitor-authoritative range SKILL.md 965–1009** (round-18 monitor `sectionize`, the resolver round-51 `refresh.py` uses), section sha256 `ecd74f306a05b96d3f87227de52e6e2bdf74f243ebbd2da232bef0f29b3611c8`. The next boundary is the `##` heading at 1010 (`## The re-sweep cadence and the six-case confidence statement (round 8, measured)`), not the next `###` at 1021 — the fixture list's 965–1009 is correct; a `###`-only scan over-reads into 1010–1020.
- Section bytes are **identical at BASE and CAND** (`diff` of lines 965–1020 at both revs: empty). The round-51 runner edit did not touch this section's text — every staleness below is drift between unchanged prose and changed runner bytes.

## Row for `reads.json`

Schema follows round-49 (`tameshi-r49-reads-v1` row shape: heading/ordinal/raw/file/ranges/verdict/excerpt/reader/base_verdict/note). `verdict` is pointer resolution (holds/absent, per the seat spec); `claim_state` adds whether the claim the pointer supports still matches candidate bytes; `falsifier` records the strongest falsifier checked.

```json
{
  "schema": "tameshi-r49-reads-v1",
  "candidate": "6d8c11e378aa90b12650808e1b79270742935f15",
  "rows": [
    {
      "heading": "### Reading a receipt — the discipline",
      "ordinal": 0,
      "raw": "REGRESSION_TOOL · REGRESSION_DATE · REGRESSION_BAND · REGRESSION_EXPECT · one REGRESSION_PIN per leg · per leg one REGRESSION_SWEEP + REGRESSION_TABLE + REGRESSION_CASE · REGRESSION_DEFECT rows for differences · REGRESSION_WORKDIR · the closing REGRESSION: PASS|FAIL|SETUP line.",
      "file": "tools/mutate-and-run.sh",
      "ranges": [[1442, 1446], [1302, 1327], [1357, 1400], [1520, 1546]],
      "verdict": "holds",
      "claim_state": "holds",
      "excerpt": "printf 'REGRESSION_TOOL: %s sha256=%s\\n' (:1442); 'REGRESSION_DATE: %s\\n' (:1443); 'REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact); fixture-mode default killed-delta<=%s flips<=%s' (:1444); 'REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=… bash-drift-pins=%s/%s' listing ten legs (:1446); 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s mode=%s sha256=%s' (:1302); 'REGRESSION_SWEEP %s: %s\\n' (:1324); REGRESSION_DEFECT built per differing row incl. ABSENT on either side (:1357 'measured=$v recorded=ABSENT', :1360 'measured=$v recorded=$want', :1371 'measured=ABSENT recorded=…', printed :1391); 'REGRESSION_TABLE %s: match=%s/%s … flips=%s' (:1392); 'REGRESSION_WORKDIR %s: %s' (:1394); 'REGRESSION_CASE %s: PASS (band: killed-delta<=%s flips<=%s inconclusive=0 defects=%s)' (:1396); closing 'REGRESSION: PASS (:1540) | FAIL (:1520) | SETUP (:1526, :1535)'.",
      "reader": "T51W2Read07",
      "base_verdict": "holds",
      "note": "Every named field is emitted by the candidate runner; the same field set exists at base (base printfs :1230–1324). Actual per-leg print order is PIN, SWEEP, DEFECT rows, TABLE, WORKDIR, CASE — the section's '·' list is an enumeration of the block, not an order claim; no falsification. Shown by: git -C LANE show CAND:tools/mutate-and-run.sh | sed -n '1442,1447p;1391,1400p;1520,1546p'.",
      "falsifier": "Strictest reading tried — that the section asserts print ORDER (…SWEEP+TABLE+CASE · DEFECT · WORKDIR): the runner prints DEFECT rows just before TABLE (:1391 before :1392) and WORKDIR between TABLE and CASE (:1394). Rejected as a falsifier: the section enumerates fields with '·' and claims no order; the field set itself is complete and exact at CAND."
    },
    {
      "heading": "### Reading a receipt — the discipline",
      "ordinal": 1,
      "raw": "Measured instance (T7-1, 2026-10-14; replayed by this lane under the same revision `cf41efaa…`): four legs, all `match=10/10 … flips=0`, `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0.",
      "file": "tools/mutate-and-run.sh (content sha256 pin `cf41efaa…`)",
      "ranges": [],
      "verdict": "holds",
      "claim_state": "holds",
      "excerpt": "corpus/knowledge/mutation-case-kumitate-claims.md:315-322: 'bash tools/mutate-and-run.sh --regression … at 19:14:16Z, tool `cf41efaa…` → REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0), rc 0 … every leg `match=10/10 flips=0`'; corpus/knowledge/fleet-kill-rate-ledger.md:281 ('the harness at `cf41efaa8be5f52d…` (r7-1; 1 341 L / 61 632 B) carries four materialized legs … every leg `match=10/10 flips=0`'); commit 9f1d3c339a7094968041c7708a65dbf7eab9fae6 ('probation round 7', 2026-10-14) carries tools/mutate-and-run.sh at 1341 lines / 61632 bytes / sha256 prefix cf41efaa8be5f52d — the pin resolves and matches.",
      "reader": "T51W2Read07",
      "base_verdict": "holds",
      "note": "Historical, correctly qualified by the tool sha. `cf41efaa…` is the runner's sha256, not a git revision (round-16 snapshot .ufo/evidence/round-16/coldread/SKILL.snapshot.md:1039: '`cf41efaa…` (`sha256sum tools/mutate-and-run.sh`)'); as a git rev it resolves in no fleet repo (21/21 fail) — the section's word 'revision' is loose, the pin itself verifies. Cross-record label nuance: the ledger attributes the run to 'T8-2's run 2026-10-14T19:14:16Z' (:281) while the section says T7-1; the measured content (four legs, cases=4, cf41efaa, 2026-10-14) agrees across records. Shown by: git -C LANE show 9f1d3c33:tools/mutate-and-run.sh | wc -l && git -C LANE show 9f1d3c33:tools/mutate-and-run.sh | sha256sum.",
      "falsifier": "Strongest falsifier tried: resolve `cf41efaa…` as a commit or blob in all 21 fleet repos — fails everywhere; had the pin been a git revision the measured instance would be unverifiable from the repo. Resolved by the ledger's own gloss (1 341 L / 61 632 B = a file state) and the round-16 snapshot's sha256sum note; then verified the sha against the round-7 commit's runner bytes (exact match, 1341 L / 61632 B)."
    },
    {
      "heading": "### Reading a receipt — the discipline",
      "ordinal": 2,
      "raw": "the closing line's `cases=N passed=N` (D is 15 for checklist-run, 10 for other current legs; N=8 since round 18, N=9 since round 26)",
      "file": "tools/mutate-and-run.sh",
      "ranges": [[2033, 2048], [1446, 1446], [1540, 1540]],
      "verdict": "holds",
      "claim_state": "stale-at-cand",
      "excerpt": "selftest leg-count agreement: '[[ \"$lcalls\" -eq 10 && \"$lfiles\" -eq 10 && \"$lnlegs\" -eq 10 ]]' (:2033); ten leg tuples, bash-checklist-run 15 defects, the other nine 10 each (:2039-2048); REGRESSION_EXPECT lists ten legs ending bash-drift-pins (:1446); closing 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)' (:1540).",
      "reader": "T51W2Read07",
      "base_verdict": "holds",
      "note": "D values hold at CAND (15 for checklist-run, 10 for each of the other nine legs). The N chain is stale: the runner now wires ten legs (r51 leg 10, bash-drift-pins), so a full replay at CAND prints cases=10 — the round's own C2 counter requires exactly `REGRESSION: PASS (cases=10 passed=10` (.ufo/evidence/round-51/c2/measure.py:18,187). The section's 'N=8 since round 18, N=9 since round 26' lacks the round-51 term; the section bytes were left unchanged while the runner gained the leg. Shown by: git -C LANE show CAND:tools/mutate-and-run.sh | sed -n '2033,2048p'.",
      "falsifier": "This is the section's strongest falsifier and it STANDS: a reader applying the section at CAND expects cases=9 and gets cases=10. Checked whether 'other current legs' could exclude the new leg — it cannot: the runner's own selftest counts ten legs and the round's C2 predicate is built on cases=10."
    },
    {
      "heading": "### Reading a receipt — the discipline",
      "ordinal": 3,
      "raw": "(negative run, `/tmp/w7-tameshi-1/flip-run.out`)",
      "file": "/tmp/w7-tameshi-1/flip-run.out",
      "ranges": [],
      "verdict": "absent",
      "claim_state": "absent",
      "excerpt": "ls: cannot access '/tmp/w7-tameshi-1/flip-run.out': No such file or directory — re-confirmed by this seat 2026-10-26; identical absence recorded at CAND in .ufo/evidence/round-18/coldread/traces/CR18/8.out.txt:1 and CR18-r3/5.out.txt:1.",
      "reader": "T51W2Read07",
      "base_verdict": "absent",
      "note": "Volatile /tmp record, gone; flagged dead by the round-16 reader (.ufo/waves/round-16/w1/CR17.md:95 and :172, 'M4 (minor, dead evidence anchor)') and still carried unchanged. The doctored-table MECHANISM the example illustrates is corroborated at CAND without the dead path: reports/r7-aud-t7.md §3 F4 (table flip → 'REGRESSION_DEFECT bash-tsukuroi-census B7: measured=SURVIVED recorded=KILLED'; 'match=9/10 … flips=1'; 'FAIL (out of band: killed-delta=1 flips=1…)'; exit 1) and the runner selftest's doctored-table arms (:1720-1725, :2005-2007). No preserved copy of the js-kimi-census D1 negative run exists in the CAND tree (git grep 'w7-tameshi-1|flip-run' at CAND → only round-16/18 records of its absence).",
      "falsifier": "Checked for any preserved copy of the cited receipt in the candidate tree — none; the pointer is dead and unrecoverable, though the claim it evidences is independently corroborated by two committed surfaces."
    },
    {
      "heading": "### Reading a receipt — the discipline",
      "ordinal": 4,
      "raw": "The rates live in `fleet-kill-rate-ledger.md` with their composition and revision — and a rate is never implied to hold at a later revision than its sweep pin.",
      "file": "corpus/knowledge/fleet-kill-rate-ledger.md",
      "ranges": [[14, 14], [27, 28], [43, 43]],
      "verdict": "holds",
      "claim_state": "holds",
      "excerpt": ":14 'a rate is never implied to hold at a later revision.'; :27-28 'per sweep, **composition-bound**: the rate is only comparable across sweeps of similar composition'; :43 header '| # | Gate (owner · file) | Suite (at sweep) | Kill-rate (composition) | Survivors (measured classes) | Hardened | Last sweep · target pin · driver |'.",
      "reader": "T51W2Read07",
      "base_verdict": "holds",
      "note": "The section's unqualified filename resolves uniquely: only corpus/knowledge/fleet-kill-rate-ledger.md is a live path at CAND (the .ufo/waves/round-18/staged copy is a staged record, not the live path). Shown by: git -C LANE show CAND:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '14p;27,28p;43p'.",
      "falsifier": "Tried: a second live file of the same basename that would make the unqualified pointer ambiguous — none at CAND."
    },
    {
      "heading": "### Reading a receipt — the discipline",
      "ordinal": 5,
      "raw": "the sibling's note is never edited (`plans/round-7.plan.md:11-15`)",
      "file": "plans/round-7.plan.md",
      "ranges": [[11, 15]],
      "verdict": "holds",
      "claim_state": "holds",
      "excerpt": "plans/round-7.plan.md:11-15: '(2) Leg fleet-run case: mado's round-6 self-service sweep (harness consumed read-only; `mado-shokunin/plans/round-6.plan.md:8-26`; declared evidence `corpus/knowledge/gate-mutation-proof.md`) is ATTESTED read-only: reproduced by tameshi from its pins, or its missing piece named. The lane operates; tameshi attests.'",
      "reader": "T51W2Read07",
      "base_verdict": "holds",
      "note": "Supports 'replay the declared pins read-only, return the receipt — or name the missing piece'. 'The sibling's note is never edited' is the section's gloss of 'harness consumed read-only / ATTESTED read-only' — not verbatim in :11-15, corroborated by reports/r7-aud-t7.md §4 (no-write proof: sibling porcelain unchanged through the audited run). Shown by: git -C LANE show CAND:plans/round-7.plan.md | sed -n '11,15p'.",
      "falsifier": "Tried: read :11-15 as NOT covering the never-edited clause (the words 'never edited' appear nowhere in the range) — the range says 'read-only' twice, which is the same commitment; recorded as a supported gloss, not a quote."
    },
    {
      "heading": "### Reading a receipt — the discipline",
      "ordinal": 6,
      "raw": "`bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 at `cf41efaa…`",
      "file": "tools/mutate-and-run.sh",
      "ranges": [[2125, 2125]],
      "verdict": "holds",
      "claim_state": "stale-at-cand",
      "excerpt": "This seat, first-hand at CAND (shared scratch clone checked out at 6d8c11e, TMPDIR=scratch): 'MUTATE_SELFTEST: 107/107 pass' / 'VERDICT: PASS', rc 0, ~8 s wall. Wave-1 at BASE: 'MUTATE_SELFTEST: 106/106 pass' / 'VERDICT: PASS' (.ufo/waves/round-51/w1/T51CritRekey-selftest.log). Counter printf 'MUTATE_SELFTEST: %s/%s pass' at :2125.",
      "reader": "T51W2Read07",
      "base_verdict": "holds",
      "note": "The command exists, exits 0 and prints VERDICT: PASS at CAND — but the tally is stale: 67/67 was the count at the cf41efaa tool sha (round-16 snapshot :1003 and :1218 pin the same tally to the same tool rev; the tool was held at cf41efaa through round 16, snapshot :1181), while the candidate runner prints 107/107 (this seat) and the base runner printed 106/106 (wave-1). Wave-1's rekey seat pre-registered exactly this check: 'flag the 67/67 quotes as stale regardless of C2' (T51CritRekey.md:92). Shown by: cd <shared clone at CAND> && TMPDIR=<scratch> bash tools/mutate-and-run.sh --selftest; echo rc=$?.",
      "falsifier": "Ran the command the section tells readers to run — the strongest possible falsifier — and the printed tally (107/107) does not match the section's 67/67. The historical qualification ('at cf41efaa…') keeps the sentence literally true as history, but as a reader expectation it is stale at CAND; the tally also moved 106→107 between base and CAND, so the printed count is revision-dependent, not a constant."
    },
    {
      "heading": "### Reading a receipt — the discipline",
      "ordinal": 7,
      "raw": "including a git-materialized replay passing at exact tolerance, a drifted working tree not moving a git-pinned leg, pin mismatch / unresolvable revision as SETUP, and a single flipped entry failing loudly. The r4-2 tolerance (`killed-delta<=1 flips<=1`) remains the fixture-mode default and is exercised by the selftest only.",
      "file": "tools/mutate-and-run.sh",
      "ranges": [[1830, 1858], [2005, 2007], [196, 197], [1444, 1445], [1711, 1711], [1767, 1767]],
      "verdict": "holds",
      "claim_state": "holds",
      "excerpt": ":1830 'ledger leg: git-materialized replay PASSes at exact tolerance'; :1840 'drifted working tree does not move a git-pinned leg'; :1848 'ledger leg pin mismatch is SETUP (exit 2)'; :1856 'ledger leg unresolvable revision is SETUP (exit 2)'; :2005-2007 'exact expectation: one flipped entry FAILs loudly' + 'REGRESSION_DEFECT fixture S: measured=SURVIVED recorded=KILLED' + 'REGRESSION_CASE fixture: FAIL (out of band: killed-delta=1 flips=1;'; BAND_KILLED=1 / BAND_FLIPS=1 (:196-197) printed as 'fixture-mode default' (:1444-1445); fixture legs assert 'PASS (band: killed-delta<=1 flips<=1 inconclusive=0 defects=2)' (:1711, :1767).",
      "reader": "T51W2Read07",
      "base_verdict": "holds",
      "note": "All four named arms exist in the candidate selftest, and the r4-2 tolerance is still the fixture-mode default exercised only there (ledger legs run the exact 0/0 band, :1444). Shown by: git -C LANE show CAND:tools/mutate-and-run.sh | sed -n '1830,1858p;2005,2007p;196,197p'.",
      "falsifier": "Tried: find a named arm missing from the candidate selftest — none missing; also tried 'exercised by the selftest only' against the ledger legs (they use the exact band) — holds."
    }
  ]
}
```

## Findings, strongest first

1. **STALE-AT-CAND — the N chain (ordinal 2), made false by the tenth leg.** The section teaches readers that a full replay's closing line reads `cases=N passed=N` with "N=8 since round 18, N=9 since round 26". At CAND the runner wires ten legs (selftest leg-count agreement demands 10, `:2033`; REGRESSION_EXPECT lists ten, `:1446`; C2's counter requires `REGRESSION: PASS (cases=10 passed=10`). The section bytes are identical at BASE and CAND — the round-51 runner edit left this reader-facing expectation one leg behind. This is the drift the re-key exists to carry: the natural fix is appending the round-51 term to the chain (wave-1's rekey seat already flagged the chain as at-risk, `T51CritRekey.md:91`).
2. **STALE-AT-CAND — the selftest tally (ordinal 6).** "`MUTATE_SELFTEST: 67/67 pass`" was true at the pinned tool sha `cf41efaa…` (corroborated by the round-16 snapshot, which pins the same tally to the same tool rev) but the candidate runner prints **107/107** — measured first-hand by this seat in a shared scratch clone at CAND, rc 0, `VERDICT: PASS` (wave-1 measured 106/106 at base). The historical qualification keeps the sentence literally true as history; as a reader expectation it is stale, and the count is revision-dependent (106→107 between base and CAND), so any re-key fix should state the tally with its revision, not as a constant.
3. **ABSENT pointer, known-dead since round 16 and still carried (ordinal 3).** `/tmp/w7-tameshi-1/flip-run.out` does not exist; the round-16 reader flagged it ("M4 minor, dead evidence anchor", `CR17.md:172`) and round-18's committed cold-read traces re-confirmed the absence at CAND. No preserved copy exists in the tree. The doctored-table mechanism the dead path once evidenced is independently corroborated at CAND (`reports/r7-aud-t7.md` §3 F4; selftest arms `:1720-1725`, `:2005-2007`), so the claim survives — but the pointer should be re-anchored to a committed record when the section is re-keyed.
4. **Holds-with-nuance — `cf41efaa…` is a content sha, not a revision (ordinal 1).** The section's word "revision" is loose: the pin is `sha256sum tools/mutate-and-run.sh` at the round-7 commit (verified: commit `9f1d3c33`, 1341 L / 61632 B, sha256 prefix `cf41efaa8be5f52d`). As a git rev it resolves nowhere in the fleet (21/21 repos fail). The measured instance itself (four legs, `cases=4`, all `match=10/10 flips=0`, 2026-10-14) is corroborated by two committed records (`mutation-case-kumitate-claims.md` §6; ledger `:281`). Minor cross-record label nuance: ledger `:281` attributes the run to "T8-2's run", the section says "T7-1"; the measured content agrees.
5. **TMPDIR change: no claim in this section is falsified by it.** The section makes no scratch-location claim; `REGRESSION_WORKDIR` is still emitted per leg and in the closing block (`:1394`, `:1522-1546`); the runner honours TMPDIR (`:148-160`, "r51 honours TMPDIR"). The only `/tmp` reference in the section is the dead historical record path (finding 3).
6. **Four panel-tool updates: no impact on this section.** The section cites none of tally-audit{,-v2,-v3}.py / mte-interop.py; nothing in it is made false by the panel-tool allowlist widening (contract amendment 2).
7. **What holds, verified against candidate bytes:** the receipt field list (ordinal 0, complete and exact at CAND and base); "PASS is exact for ledger legs" case-line and TABLE formats (`:1392`, `:1396`, closing `:1540`); "FAIL names its rows" incl. ABSENT on either side (`:1357`, `:1360`, `:1371`); "SETUP is not a verdict" — missing repo/rev/blob, pin mismatch, refused sub-sweep all emit SETUP and exit 2 (`:1268`, `:1272`, `:1314`, `:1327`); the D values (15 checklist-run, 10 other legs, `:2039-2048`); the ledger pointer (ordinal 4); the round-7 plan pointer (ordinal 5); all four named selftest arms and the r4-2 fixture-mode tolerance (ordinal 7).

## Verification log (exercised by this seat)

- Section bytes: `diff <(sed -n '965,1020p' BASE:SKILL.md) <(sed -n '965,1020p' CAND:SKILL.md)` → empty; monitor `sectionize` (round-18 measure.py loaded from a CAND clone) → `{start: 965, end: 1009, sha256: ecd74f30…}`.
- Selftest first-hand: `git clone --shared` lane → assert `rev-parse --show-toplevel` = clone → `checkout --detach 6d8c11e` → `TMPDIR=<scratch>/tmp bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, rc 0.
- Tool-sha pin: `git show 9f1d3c33:tools/mutate-and-run.sh | wc -l` → 1341; `| wc -c` → 61632; `| sha256sum` → `cf41efaa8be5f52d…`.
- Dead pointer: `ls /tmp/w7-tameshi-1/flip-run.out` → No such file or directory; `git grep 'w7-tameshi-1|flip-run' CAND` → only round-16/18 absence records.
- All other pointers: `git show`/`git grep` at CAND as cited in each row's "Shown by".
