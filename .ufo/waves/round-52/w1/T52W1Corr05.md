# T52W1Corr05 — correction record for the round-51 cold-read re-key entry `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`

Seat: T52W1Corr05 (scribe, C2 m4). Bounds honoured: lane checkout read-only except
`.ufo/waves/round-52/w1/T52W1Corr05.{json,md}`; no git/jj mutation anywhere; no fixture repo created;
no scratch dir needed beyond in-memory python (nothing written under `/tmp`); no agent://all.

Deliverable: `.ufo/waves/round-52/w1/T52W1Corr05.json` (6 keys exactly, `wrong_expectations: 2`).

## Entry identified

| Fact | Value | Command / locus |
|---|---|---|
| heading | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | `.ufo/evidence/round-21/coldread/ledger.json:40930` |
| entry block | `entries[515]`, `skill_sha256`=`sha256`=`b5dae2b8…c38ebc` | `ledger.json:40926-40954` |
| `read_rev` | `02ec217c4d0afabe727fde2e261b7951d28fb4e9` | `ledger.json:40938` |
| recorded verdict | `verified-record` (`:40933`), `wrong_expectations: 0` (`:40935`, written by `refresh.py`, routed defect 3) | `ledger.json:40933,40935` |
| reader seat | `T51W2Read05` (2nd seat entry is the L1 integration) | `ledger.json:40946-40949` |
| reader file | `.ufo/evidence/round-51/coldread/reads/T51W2Read05.md` (5,952 B, identical at base `ef19d8e1` and on disk) | `python3 -c "import subprocess;p='.ufo/evidence/round-51/coldread/reads/T51W2Read05.md';print('base==disk:',subprocess.run(['git','show','ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:'+p],capture_output=True,text=True).stdout==open(p).read())"` → `base==disk: True` |
| section | `SKILL.md:921-932` at `read_rev`, sha256 (trailing blank removed) `b5dae2b8…c38ebc` — equal to the reader's own declared section sha and to the entry's | `python3 -c` below |
| top-level `corrections` key | absent at base (`keys = schema, entries, carried_from, provenance, round21_provenance`) | `python3 -c "import json;print(list(json.load(open('.ufo/evidence/round-21/coldread/ledger.json'))))"` |
| r51 re-key entries | 20 (`read_rev` startswith `02ec217c`) | same parse |

```
$ python3 -c "
import subprocess,hashlib
s=subprocess.run(['git','show','02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md'],capture_output=True,text=True).stdout.split('\n')
sec='\n'.join(s[920:932]).rstrip('\n')
print('section_sha256_at_read_rev=',hashlib.sha256(sec.encode()).hexdigest())"
section_sha256_at_read_rev= b5dae2b85cd606e8d8db5d34922aa995763428934ea28f728bf372c308c38ebc
```

The reader's own header says it read candidate `6d8c11e3…` (`.ufo/evidence/round-51/coldread/reads/T51W2Read05.md:3`),
not `02ec217c…`. The two revisions carry byte-identical section text — the sha above equals the sha the reader
declared (`T51W2Read05.md:3` and `:10`) — so every recorded statement transfers without reinterpretation.
The entry's `inputs` digests also match its `read_rev`:
`git show 02ec217c:tools/mutate-and-run.sh | sha256sum` → `977de470…e0bda`, `…:corpus/knowledge/fleet-kill-rate-ledger.md | sha256sum` → `13a11e46…c21033`, both equal to `ledger.json:40940-40941`.

## Findings (2)

Section text at `read_rev` (`git -C tameshi-shokunin show 02ec217c:SKILL.md | sed -n '921,932p'`):

```
921 ## The leg ledger — replay, receipt, and how it is read (round 7, measured)
925 pinned original revision. Four legs at that revision (r7-1; seven since round 16; eight since round 18; nine since round 26) — `js-kimi-census`
929 (`tools/mutate-and-run.sh@9f1d3c3:72-109`, `:511-522`; at round 18 the recorded tables sit at `:597-620`). The ledger
```

### F1 — `stale-count`: the leg-count progression stops at nine

- quote (reader `T51W2Read05.md:49`, 92 chars, one line): `Thus the section's progression is stale/incomplete at CAND: it omits the tenth round-51 leg.`
- class: `stale-count`
- `skill_statement` (`SKILL.md:925`): `(r7-1; seven since round 16; eight since round 18; nine since round 26)`
- substance at `read_rev`:
  - `git -C tameshi-shokunin show 02ec217c:tools/mutate-and-run.sh | sed -n '84p'` → `# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten) — the fleet's`
  - `… | sed -n '223,226p'` → the panel names ten legs, ending `bash-drift-pins) at its pinned`
  - `… | sed -n '632,633p;643p'` → `PIN_DRIFTPINS=c138d34c…`, `REV_DRIFTPINS=e64e81b8…`, `TABLE_DRIFTPINS='K_MODE_CMP:KILLED,…'`
  - the reader's calibration note repeats it: `T51W2Read05.md:62` "the prose progression ends at nine while CAND has ten legs".

### F2 — `stale-pointer`: the round-18 table pointer is a moved range

- quote (reader `T51W2Read05.md:53`, 154 chars, one line): `the historical round-18 pointer has moved; current TABLE_* assignments are :634-643. Treating the shorthand as an unqualified CAND pointer would be stale.`
- class: `stale-pointer`
- `skill_statement` (`SKILL.md:929`): ``at round 18 the recorded tables sit at `:597-620` ``
- substance at `read_rev`: the claim holds at `4b7c682` (round 18) but no longer holds at the read revision —
  `git -C tameshi-shokunin show 02ec217c:tools/mutate-and-run.sh | sed -n '597,620p'` prints only anchor comments and `PIN_JS`…`PIN_MADO` assignments, no `TABLE_*` line; `… | sed -n '634,643p'` prints the ten `TABLE_*` assignments (`TABLE_JS` at 634 … `TABLE_DRIFTPINS` at 643).
  The section's own qualifier ("at round 18") is what keeps this from being a `false`; the reader recorded it as a pointer a follower does not land on (reader `T51W2Read05.md:36-37`).

## Excluded, with reasons

| Reader item | Locus | Why not a finding |
|---|---|---|
| `tools/mutate-and-run.sh@9f1d3c3:72-109` | `T51W2Read05.md:13-19` | `verdict: holds`; pin is a real round-7 commit and the blob lists the four tables |
| `:511-522` | `T51W2Read05.md:22-28` | `verdict: holds` (PIN/REV + `TABLE_JS/BASH/TSUKUROI/MADO` at the pinned blob) |
| `corpus/knowledge/fleet-kill-rate-ledger.md`, "eight rows since its round-18 block" | `T51W2Read05.md:40-46` | `verdict: holds`; row count re-confirmed at `read_rev` at `:45-48`, `:276-277`, `:410`, `:432`. The queue cell `:119` still reads `unmeasured by sweep; hermetic` — a defect of that ledger file, routed separately as m5, not a statement of this section |
| TMPDIR / panel-tool checks | `T51W2Read05.md:51-52` | Reader states no such claim appears in this section; nothing fails |
| kill-rate expectations 8/10, 8/10, 6/10, 4/10 | `T51W2Read05.md:54` | Checked against the pinned tables, still correct |
| `rekey_parser_caveat` (targets.json `file=null`, `resolve_kind=null`) | `T51W2Read05.md:56` | Metadata of the round-51 parser, not a statement of the section; reader manually resolved and verified the ranges |
| trace path provenance | `ledger.json:40944` lists `.ufo/evidence/round-51/coldread/rekey-02ec217c/traces/section-5.json` | `git cat-file -e 02ec217c:…` → `fatal: … exists on disk, but not in '02ec217c'` (added after that revision). Observation only; it is not a section statement and does not change the count |

## Self-check (frozen counter rule)

`check_findings` imported from the frozen counter `.ufo/evidence/round-52/c2/measure.py` (same rule m4 applies),
run on the written deliverable and the reader file as committed:

```
$ python3 - <<'PY'
import json, importlib.util
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
d=json.load(open(LANE+'/.ufo/waves/round-52/w1/T52W1Corr05.json'))
spec=importlib.util.spec_from_file_location('c2', LANE+'/.ufo/evidence/round-52/c2/measure.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
reader=open(LANE+'/'+d['reader_file']).read()
print('keys:', sorted(d), '| wrong_expectations==len(findings):', d['wrong_expectations']==len(d['findings']))
print('check_findings ->', c2.check_findings(d['findings'], reader))
for f in d['findings']:
    print('quote=%d chars one-line=%s in-reader=%s class=%s' % (len(f['quote']),
          any(f['quote'] in l for l in reader.split('\n')), f['quote'] in c2.squash(reader), f['class']))
PY
keys: ['findings', 'heading', 'read_rev', 'reader', 'reader_file', 'wrong_expectations'] | wrong_expectations==len(findings): True
check_findings -> None
quote=92 chars one-line=True in-reader=True class=stale-count
quote=154 chars one-line=True in-reader=True class=stale-pointer
```

`None` is the pass value of `check_findings` (frozen counter: `if why is None and c.get('wrong_expectations') != len(c['findings'])`).
Both quotes are inside the 20–200 character window and are byte-exact substrings of a single reader line.
The matched ledger entry's seat is `T51W2Read05` and `reader_file` equals
`.ufo/evidence/round-51/coldread/reads/T51W2Read05.md`, the value m4 constructs from the seat
(`.ufo/evidence/round-52/c2/measure.py:157-160`).

## Integration contract (for the L1 writing the ledger edit)

- Append exactly one record to the new top-level `"corrections"` list with the 6 fields in
  `.ufo/waves/round-52/w1/T52W1Corr05.json`; do not alter the entry at `ledger.json:40926-40954`
  (`entries[515]`). m4 matches on `heading` + `read_rev` prefix + `reader` and requires `len(recs) == 1`
  (`measure.py:152-158`), so a second record with the same triple fails the check.
- Do not rewrite the entry's `wrong_expectations: 0`; the superset lives only in `corrections`
  (same shape as the m5 supersession precedent).
- Cold-read no-harm: the monitor keys sections by `skill_sha256`/`sha256` of the entry and its `inputs`;
  adding an unrelated top-level key leaves those digests untouched. Three credited sections are lost by
  the round's `tools/registry.json` and `tools/round21-measure.py` edits (contract `no_harm.coldread_note`),
  not by this record; the L1 re-keys those in wave 2.

## Limits

- I did not run any counter against the lane (`measure.py` only imported for its `check_findings`/`squash`
  helpers); no deciding-run evidence is claimed here.
- The count is the two statements the reader recorded as failing. I did not search for section statements the
  reader never addressed (the item scopes findings to the reader's record; the frozen counter cannot see
  completeness either — contract C2 `cannot_see`).
- `wrong_expectations` is `2`, not the round-51 `0`: this record supersedes that count for this heading only.

## Summary

- Deliverable `.ufo/waves/round-52/w1/T52W1Corr05.json`: heading `## The leg ledger — … (round 7, measured)`, `read_rev 02ec217c…`, reader `T51W2Read05`, `wrong_expectations: 2`.
- F1 `stale-count` (reader `:49`): section `SKILL.md:925` ends the progression at "nine since round 26"; `tools/mutate-and-run.sh:84` at `read_rev` says "r51 ten" and `:223-226` names ten legs.
- F2 `stale-pointer` (reader `:53`): ``SKILL.md:929`` `:597-620`; at `read_rev` that range holds only comments and `PIN_*` lines — the ten `TABLE_*` assignments are `:634-643`.
- Section bytes at `read_rev` sha `b5dae2b8…c38ebc`, equal to the reader's declared sha and the ledger entry's `sha256` (`ledger.json:40931`), so the reader's statements transfer.
- Excluded: the pointers the reader marked `holds` with no caveat (72-109, `:511-522`, the kill-rate-ledger file), the eight-row statement (holds; its `:119` cell is m5's job), the TMPDIR/panel-tool non-claims, and the parser caveat.
- Self-check with the frozen `check_findings`: `None` (pass), both quotes 92/154 chars, single-line, verbatim.
- No tools installed; no git/jj mutation; no scratch left behind; nothing citable under `/tmp`.
