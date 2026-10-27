# T52W1Corr09 — correction record: round-51 re-key entry `### The tick, executed`

Seat `T52W1Corr09` · round 52 wave 1 · C2 m4 (calibration). Deliverable:
`.ufo/waves/round-52/w1/T52W1Corr09.json` (heading `### The tick, executed`, read_rev
`02ec217c4d0afabe727fde2e261b7951d28fb4e9`, reader `T51W2Read09`, reader_file
`.ufo/evidence/round-51/coldread/reads/T51W2Read09.md`, `wrong_expectations: 8`, 8 findings).

## Defect being repaired

The round-21 ledger entry for this section records `wrong_expectations: 0`
(`.ufo/evidence/round-21/coldread/ledger.json:41045-41059`, the entry whose `read_rev` is
`02ec217c4d0afabe727fde2e261b7951d28fb4e9` and whose seats are `["T51W2Read09", "L1 TameshiR51a3
integration (attempt 3)"]`), because round 51's re-key wrote the value from code rather than from the
reader: `.ufo/evidence/round-51/coldread/refresh.py:227` (`'blocking_gaps': 0, 'wrong_expectations':
0, 'minor_gaps': 0,`). Routed as defect 3 in `corpus/lessons/round-51-verifier-spotcheck.md:128`
("Append a named correction to the round-21 ledger … so the calibration record does not claim zero
wrong expectations where a reader found some"). Command that shows both:

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 -c "import json;d=json.load(open('.ufo/evidence/round-21/coldread/ledger.json'));print([(e['read_rev'][:8],e['seats'],e['wrong_expectations']) for e in d['entries'] if e['heading']=='### The tick, executed' and e['read_rev'].startswith('02ec217c')])"
# -> [('02ec217c', ['T51W2Read09', 'L1 TameshiR51a3 integration (attempt 3)'], 0)]
grep -n "wrong_expectations': 0" .ufo/evidence/round-51/coldread/refresh.py
# -> 227:                'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
```

## Method

1. Read the reader file in full (`.ufo/evidence/round-51/coldread/reads/T51W2Read09.md`, 145 lines
   incl. the `reads.json` row and the five prose-findings paragraphs).
2. Resolved the section at the frozen read_rev: `git -C . show
   02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md`, lines 1164–1210. The section's sha256 at the
   read_rev is `6982b6494fc1998dd4625a0c94117896424bda73ca737d370ac8300a4dd00b16`, byte-identical to
   the `sha256` the ledger entry records for the same section, so the reader's verdicts were formed
   against the bytes this record cites.
3. Took every statement the reader recorded as *not holding* at its candidate: `moved` pointer
   (reader:28), the superseded leg count, and the seven bullets of the reader's `findings` array
   (reader:87-95), splitting the first reader bullet into its two independent defects (moved anchor
   and stale count) because the section makes two separate claims. Each finding quotes the reader
   byte-exactly from ONE reader line and cites the section text it concerns.
4. Not counted, and why:
   - `"verdict": "holds"` pointers (reader:56, 63, 70, 77: ER-4 `:318-353`, the `:354-360` addendum,
     `:1019`, T3) — the reader records them as holding.
   - `"verdict": "holds-as-history"` for the tick-time tool sha `cf41efaa…` (reader:35) — the reader
     states the section claims no current-state currency, so the divergence from the base/CAND blob
     sha is disclosed and accurate history, not a failing statement.
   - `"verdict": "absent"` for the two `/tmp/w9-tameshi-t93/…` scratch paths (reader:42, reader:49) —
     the reader scopes them as ephemeral 2026-10-14 scratch of a section that is itself a
     "timestamped observation … never carried as a standing claim"; the reader files them as absent
     pointers, not as false statements, and does not list them in `findings`. The underlying t93/t91
     divergence *is* counted (finding 3), because that one contradicts the section's "one tick"
     identity claim.
   - Notes the reader marks as consistent with the section: the `no_impact_checks` list (reader:96-98)
     — the four updated panel tools are not cited in this section and the runner TMPDIR change makes
     no statement here false.

## Findings (as delivered in `T52W1Corr09.json`)

| # | class | reader line | reader quote (byte-exact, one line) | section statement concerned (SKILL.md 1164-1210 at `02ec217c`) |
|---|---|---|---|---|
| 1 | stale-pointer | 88 | `pointer tools/mutate-and-run.sh:511-518 moved at CAND → now 614-633` | ``(`tools/mutate-and-run.sh:511-518`)`` — at CAND those lines are run_sweep's mutant-prep loop; the PIN_*/REV_* block sits at 614-633 |
| 2 | stale-count | 88 | `and 'four embedded legs' superseded by ten` | `` `PIN_*`/`REV_*` for the four embedded legs `` — the harness carries ten legs at base/CAND |
| 3 | unsupported | 89 | `scratch-root divergence t93 (page) vs t91 (ER-4 ledger:320,341) for the same tick` | ``scratch `/tmp/w9-tameshi-t93/pin-read-final.txt` `` — ER-4 records t91 for the same tick |
| 4 | false | 90 | `REGRESSION_DATE divergence 19:58:59Z (SKILL.md:1215) vs 19:58:18Z (ledger:341)` | `the same regression receipt — two records of one tick, kept un-merged and agreeing` |
| 5 | false | 91 | `'that in-flight edit is now committed as 7da4ec50…' (1187) overstates identity` | ``that in-flight edit is now committed as `7da4ec50…` `` — dc864c6a…/99 716 B was superseded by 7da4ec50…/131 612 B |
| 6 | stale-count | 92 | `'six minutes later' (1186) is 5 min 15 s` | ``and, six minutes later, `dc864c6a…` (dirty)`` — 19:15:14Z → 19:20:29Z |
| 7 | unsupported | 93 | `(1206) stated without its [I] label` | `the owners' own round-9 lanes are editing their gates` — ER-4:356 marks it [I] |
| 8 | unsupported | 94 | `20:03:34Z worktree shas (b54f5732…/31364115…) have no surviving anchor (scratch gone)` | ``tsukuroi's worktree `b54f5732…` vs its HEAD blob `bba6cdf6…` `` |

Commands behind the findings (all read-only):

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
sed -n '82,99p' .ufo/evidence/round-51/coldread/reads/T51W2Read09.md       # falsifier + findings bullets
git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | sed -n '1164,1210p'
git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:tools/mutate-and-run.sh | sed -n '511,518p;614,633p'
```

Reader verdicts carried, not re-executed: the reader located the PIN_*/REV_* block at 614-633 at CAND
and found the section's sha, the ledger rows and the ER-4 cells consistent. This seat did not re-run
the reader's git-object comparisons as a fresh judgement (a seat does not decide a claim) — it
transcribes what the reader recorded, byte-exactly.

## Self-check (frozen counter's rule, `check_findings` in `.ufo/evidence/round-52/c2/measure.py:82-95`)

Imported the frozen counter module and called its own `check_findings` on the delivered record, so the
result is the counter's rule and not a re-implementation:

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 - <<'PY'
import importlib.util, json
spec=importlib.util.spec_from_file_location('c2m','.ufo/evidence/round-52/c2/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rec=json.load(open('.ufo/waves/round-52/w1/T52W1Corr09.json'))
text=open(rec['reader_file'],encoding='utf-8').read()
print('keys:', sorted(rec))
print('findings=%d wrong_expectations=%d' % (len(rec['findings']), rec['wrong_expectations']))
print('check_findings ->', m.check_findings(rec['findings'], text, m.FLOORS.get(rec['reader'], ())))
PY
```

Observed output:

```
keys: ['findings', 'heading', 'read_rev', 'reader', 'reader_file', 'wrong_expectations']
findings=8 wrong_expectations=8
check_findings -> None
```

`None` is the counter's success (no quote shorter than 20 collapsed characters, every quote a verbatim
substring of the reader file after whitespace collapse, count equals `len(findings)`, no frozen floor
applies to this seat). Per-quote containment was also checked per *line*: all 8 quotes are substrings
of a single reader line (reader lines 88, 88, 89, 90, 91, 92, 93, 94) — the item's stricter rule, not
only the counter's collapse rule. Collapsed lengths: 67, 42, 81, 78, 78, 40, 35, 85 (all within
20–200).

## Handoff note for the integration seat

`measure.py` m4 reads the correction records from the ledger's **top-level** `corrections` list
(`.ufo/evidence/round-52/c2/measure.py:155-165`), matching on `heading` + `read_rev` prefix
`02ec217c` + `reader`. The ledger has no `corrections` key at base (`list(d)` is
`['schema','entries','carried_from','provenance','round21_provenance']`). This seat is read-only on the
lane, so the delivered JSON is the record to splice verbatim: it already carries exactly the six keys
m4 matches on and no others.

## Bounds / provenance

- Read-only on the lane; the only files written are `.ufo/waves/round-52/w1/T52W1Corr09.json` and this
  report. No git/jj mutation, no `git add`/`commit`/`checkout`, no write to the fleet repo, a sibling
  lane, `shokuknow`, or the lane's index.
- No counter was run as a verdict: no `measure.py --lane … --rev …` invocation, no scratch clone.
  The only execution of frozen counter code was `check_findings` on this seat's own record, which is a
  probe of the quote rule, not a claim verdict.
- No scratch root was needed (`/fast/scratch/hyaku/tameshi-r52/T52W1Corr09/` never created); no `/tmp`
  writes; no tools installed or upgraded; nothing to delete.
- No claim was decided; C2 m4's 20-record total is the deciding run's to score.

## Summary

- Repaired the round-51 overstatement for `### The tick, executed`: the ledger's `wrong_expectations: 0`
  came from `refresh.py:227` writing 0 from code, while reader `T51W2Read09` recorded 7 failing bullets.
- Delivered 8 correction findings (that reader bullet 1 split into its moved pointer and stale leg
  count): 1 stale-pointer, 2 stale-count, 3 unsupported, 2 false.
- Each quote is byte-exact from one reader line (88–94); the frozen `check_findings` returns `None`,
  `wrong_expectations == len(findings) == 8`.
- Excluded: `holds` / `holds-as-history` pointers and the two absent ephemeral `/tmp` scratch paths,
  which the reader scopes as historical and accurate.
- Section bytes confirmed identical to the ledger's recorded sha `6982b649…` at read_rev `02ec217c`.
- Ledger has no top-level `corrections` list yet; the integration seat splices the delivered JSON
  (six keys, m4 shape) read-only from this seat's side.
- No claim decided, no counter run as a verdict, no installs, no scratch left behind.
