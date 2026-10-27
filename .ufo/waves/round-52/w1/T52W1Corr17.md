# T52W1Corr17 — correction record for round-51 cold-read re-key `T51W2Read17`

Seat T52W1Corr17 (scribe, calibration). L1 TameshiR52, wave 1. Milestone: C2 m4 correction record.
Section `## Live-tree re-pin and entry-command monitor — round 17`, read_rev
`02ec217c4d0afabe727fde2e261b7951d28fb4e9`, reader `T51W2Read17`. Deliverable written:
`.ufo/waves/round-52/w1/T52W1Corr17.json`.

## Behavior

Read the contract first (`.ufo/evidence/round-52/contract.json`, read, never edited), the C2 counter
(`.ufo/evidence/round-52/c2/measure.py`, `check_findings` :82-95, `FLOORS` :36, `m4` :141-166), the routed defect
(`corpus/lessons/round-51-verifier-spotcheck.md`, "Routed defects" item 3), then in full — no elisions — the
reader file `.ufo/evidence/round-51/coldread/reads/T51W2Read17.md` (`awk 'END{print NR}'` → 414 lines) and the
section at read_rev.

**Result: `findings: []`, `wrong_expectations: 0`.** The reader recorded no statement of the section as
failing at its candidate. The zero in the record is now derived from the reader file, not inherited from
round 51's `refresh.py` write-from-code (`.ufo/evidence/round-51/coldread/refresh.py:227-228` writes
`'wrong_expectations': 0, 'minor_gaps': 0` and `'commands_executed_count': 1` literally for every re-key
entry) — that distinction is the whole of routed defect 3, and here the reader-derived count genuinely is 0.

## Section identity (re-established independently, not taken from the fixture list)

```
$ git -C . show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | sed -n '1814,1845p' | wc -l
32
$ git -C . show 02ec217c…:SKILL.md | sed -n '1846p'
### Round-17 gate/probe registry — re-pin and monitor
$ python3 - <<'EOF'   # sha256 of SKILL.md lines 1814-1845 + trailing newline
import subprocess, hashlib
for rev in ['02ec217c…','6d8c11e3…','ef19d8e1…']:
    lines=subprocess.run(['git','-C','.','show',f'{rev}:SKILL.md'],capture_output=True).stdout.decode().split('\n')
    span='\n'.join(lines[1813:1845])+'\n'
    print('%-12s %s  lines=%d' % (rev[:12], hashlib.sha256(span.encode()).hexdigest(), span.count('\n')))
EOF
02ec217c4d0a 07a598f065c8d3dd5719068e8852069be85129795188069fe2d46e0670844e26  lines=32
6d8c11e378aa 07a598f065c8d3dd5719068e8852069be85129795188069fe2d46e0670844e26  lines=32
ef19d8e1e7ba 07a598f065c8d3dd5719068e8852069be85129795188069fe2d46e0670844e26  lines=32
```

All three are byte-equal and equal the reader's recorded `section_sha256` (`T51W2Read17.md:14`), so the reader
read the same bytes this record is keyed to. The ledger entry for this heading exists from base onward
(`git show ef19d8e1:…/ledger.json` → 531 entries, 20 with `read_rev` prefix `02ec217c`; at read_rev itself
the ledger still holds 511 entries and 0 re-keyed, i.e. the entry post-dates the read it records).

## Statement audit — every statement of the section against the reader's recorded verdict

Reader verdicts are 15/15 `"verdict": "holds"` (`grep -o '"verdict": "[a-z -]*"' …T51W2Read17.md | sort |
uniq -c` → `15 "verdict": "holds"`; no `false`/`absent`/`stale` verdict token anywhere in the file).

| Section statement (SKILL.md:read_rev) | Reader record | Counted? |
|---|---|---|
| :1816 `corpus/lessons/round-16-verifier-spotcheck.md` §3/§6, R16-OP1, R16-MON1 | P1 `:98` **holds**; precision note `:104-105` "the source sentence is accurate as written" | no — holds |
| :1817-1818 S062 / S063 / S061 glosses | P12-P14 `:189` **hold** (`corpus/SOURCES.md:70-72`) | no — holds |
| :1819-1822 "restores the round-14 capability's live verdict and adds the monitor…"; "claims no new mutation case and no promotion credit" | not contested; §3 `:210-223` shows the monitor catching the round-51 stale row | no — nothing recorded as failing |
| :1824 v2 manifest / 40-hex ancestor / waive only moved (`historical_input_unneeded`, `historical_input_forbidden`) | P6 `:139` **holds, executed** (`:142-147`), `(round 18; round 17's two now exit 2)` verified | no — holds |
| :1825 waived path differs from `<anchor>:<path>` → exit 2 `historical_input_uncommitted` | P6 `:139` **holds, executed** (`:142-147`: round-17 manifests exit 2); P7/P8 `:149` | no — holds |
| :1826 waiver rev tree id/dangling/not ancestor/shallow → exit 2; `:368-390`; selftests `v2-historical-replace-ref`, `v2-gitdir-env`; grafts by code reading only; round-27 Read32 | P0 `:84` **holds** (`:86-96`, `--selftest` exit 0) | no — holds; see nuance (a) |
| :1828 registered command's outcome changes → re-pin or supersede, sweep every mention | vindicated live: §3 `:219-220` "the mechanism claim is confirmed by a live instance" | no — recorded as confirmed |
| :1829 row stops holding → `differs`, exit 1; leaves `active` only as `superseded` with `superseded_by`, still runs | P3 `:115` **holds as prose**, `differs` observed `:117-118`, 56 rows/7 superseded `:119-122`, registry parse `:173-180` | no — holds |
| :1830 every lane tool scrubs `GIT_*`; round 18 adds `bash-witness-study.py`; historical `.ufo/evidence/round-16/measure.py` still does not; run only through `registry-check` | P4 `:125` **holds as prose**, P5 `:131` **holds** (`:135` "still does not [scrub] is true") | no — holds |
| :1831 runner regression leg SETUP `repo_identity_mismatch`, exit 2 | `### Runner claim…` `:197` **holds at CAND bytes** (`:199-203`; runner :1263) | no — holds |
| :1835-1836 recipe step 1 → 1 `failed`, `producer_before` | P6 `:139` **holds, executed at CAND bytes** | no — holds |
| :1837-1838 step 2 → 0 `clean`, `"effective": 11`, `"superseded": 1`; one `HISTORICAL` line per waived instrument | P7/P8 `:149` **holds, executed**; `:151` effective 11 / superseded 1; `:153` exactly 3 HISTORICAL lines | no — holds |
| :1839-1842 step 3 replays every row, ends `REGISTRY_CHECK: held=N/M superseded=K`; `--registry`; never on the live tree | P9 `:158` **holds, executed end-to-end** (613 s, 56 rows, `held=48/49 superseded=7`, exit 1 on one differs row) | no — holds |
| :1843-1844 step 4 branch tip `refs/heads/<branch>`, `branch`/`head_differs_from_branch`, never at `HEAD` | P11 `:182` **holds, executed** (`:185-186` fields observed) | no — holds; see nuance (a) |

## Why the count is zero — the four exclusions, each with the reader's own token

(a) **`:1826` "not `HEAD`" / step 4 "never at `HEAD`" is flat** — reader `:228-230`:
":1826's \"not `HEAD`\" is flat — the docstring (:51-53) allows a HEAD fallback… (Read32 flagged the same)".
Confirmed at read_rev: `git show 02ec217c…:tools/pin-disposition.py | sed -n '51,53p'` → "`branch` the
resolved name (null when no local branch exists; then commit stays raw HEAD and head_differs_from_branch is
null)". This is an over-general qualifier the reader filed under **"Pre-existing nuances (disclosed or
immaterial)"** (`:228`) and marked historically disclosed ("Read32 flagged the same"); its pointer row P11
is `"verdict": "holds"`. Excluded by the item's rule (a `holds` verdict, a pre-existing/historical note).

(b) **Bare tokens `registry-check.py` (:1829), `bash-witness-study.py` (:1830), generic `expected.json`
(:1825)** — reader headings `:108`, `:115`, `:125` read **"holds as prose; bare token unresolved"** /
"token resolves to no file; sentence holds", and `:231-232` / `:390` say the files "exist at their real
paths". Re-checked at read_rev:
`git ls-tree --name-only 02ec217c…:tools | grep -E '^(registry-check|bash-witness-study)\.py$'` → both
present; `git ls-tree -r --name-only 02ec217c… | grep expected.json` → only `.ufo/evidence/round-*/…`
(the reader's named referent `.ufo/evidence/round-13/expected.json` present). These are prose names whose
sentences hold; the reader recorded no pointer as stale, moved or absent.

(c) **The one live inconsistency the reader found** — `tools/registry.json` row `mte-interop-check` still
expects `legs_conforming=9/9` while `tools/mte-interop.py` prints 10/10 (`:210-223`, `:389`). Reader:
"It falsifies no sentence in this section (the section claims the monitor catches such a row, which it
did)." It is a round-51 lane defect, routed as R51.1 to C1's surface — not a false statement here.

(d) **Re-key cause** — input-drift on five paths incl. `tools/mte-interop.py` (entry 343, ReRead01) is the
monitor's reason for re-reading, not a defect in the section's text: `:207` "**No stale or moved pointer.**
All eight resolved files exist at CAND at the cited paths and are byte-unchanged base→CAND."

Section-level verdicts, verbatim: `:207` "No stale or moved pointer"; `:222` "It falsifies no sentence in
this section"; `:224` "**Nothing is made false by** the tenth leg, the runner TMPDIR change, or the panel
updates in this section's own sentences". `findings: []` follows from the reader's record, not from a
missing inspection.

## Self-check (frozen counter's rule: whitespace-collapsed substring, `c2/measure.py` `check_findings` :82-95)

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 - <<'EOF'
import json, subprocess, importlib.util
lane='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
rev='ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'   # base bytes; deciding REV not yet chosen
show=lambda p: subprocess.run(['git','-C',lane,'show',f'{rev}:{p}'],capture_output=True).stdout
spec=importlib.util.spec_from_file_location('c2',lane+'/.ufo/evidence/round-52/c2/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rec=json.load(open(lane+'/.ufo/waves/round-52/w1/T52W1Corr17.json'))
led=json.loads(show('.ufo/evidence/round-21/coldread/ledger.json'))
r51=[e for e in led['entries'] if str(e.get('read_rev','')).startswith(m.R51_REKEY_REV)]
e=[x for x in r51 if x.get('heading')==rec['heading']]
got=[c for c in [rec] if c['heading']==e[0]['heading'] and str(c['read_rev']).startswith(m.R51_REKEY_REV)
     and c['reader']==e[0]['seats'][0]]
print('r51-entries=%d entries-for-heading=%d records-matched=%d' % (len(r51),len(e),len(got)))
c=got[0]; want='.ufo/evidence/round-51/coldread/reads/T51W2Read17.md'
print('reader_file-exact=%s' % (c['reader_file']==want))
print('check_findings ->', m.check_findings(c['findings'], show(want).decode(), m.FLOORS.get('T51W2Read17',())))
print('count==len(findings) ->', c['wrong_expectations']==len(c['findings']))
EOF
r51-entries=20 entries-for-heading=1 records-matched=1
reader_file-exact=True
check_findings -> None
count==len(findings) -> True
```

`check_findings` returns `None` (pass) on the empty list: with no quotes the substring loop is vacuous and
no floor exists for `T51W2Read17` (`FLOORS` in `c2/measure.py:36` names only `T51W2Read20` and
`T51W2Read01`). `python3 .ufo/evidence/round-52/c2/measure.py --selftest` → `C2_SELFTEST: cases=8 failed=0`,
exit 0 (the same rule checked positive and negative on synthetic quotes).

## Gates and scope

- No claim counter was run against the lane: only `measure.py --selftest` (8/8, exit 0) and the pure
  `check_findings`/`squash` functions were imported. No clone, fixture, or registry replay was needed; no
  counter verdict is asserted here.
- Writes: `.ufo/waves/round-52/w1/T52W1Corr17.json` and this report only. No scratch dir was created
  (`/fast/scratch/hyaku/tameshi-r52/T52W1Corr17` unused); one small `/tmp` extraction file was removed.
  No git/jj mutation, no LANE/ledger/SKILL.md edit, no tool install.
- Out of scope, for the L1: the same ledger entry still carries the synthesized `minor_gaps: 0` and
  `commands_executed_count: 1` (`refresh.py:227-228`) although the reader file records three pre-existing
  nuances (`:228-232`) and a dozen heavy executions (`:407-410`). m4's frozen predicate covers
  `wrong_expectations` only; this record does not change those cells.

## Summary

- Deliverable `.ufo/waves/round-52/w1/T52W1Corr17.json`: `findings: []`, `wrong_expectations: 0`.
- Section bytes at read_rev `02ec217c` are `SKILL.md:1814-1845`, sha256 `07a598f0…`, identical at CAND
  `6d8c11e3` and base — the reader read exactly these bytes.
- All 15 pointer verdicts in `T51W2Read17.md` are `holds`; the file has no `false`/`absent`/`stale` verdict.
- Excluded, with the reader's token: the flat "not `HEAD`" (`:228`, pre-existing, Read32-flagged), the three
  bare prose tokens (`:108/:115/:125`, "holds as prose"), and the round-51 `mte-interop-check` staleness,
  which the reader states "falsifies no sentence in this section" (`:222`) and routes to C1.
- Zero is reader-derived: the frozen `check_findings` returns `None`, count equals `len(findings)`, and the
  m4 record shape matches the ledger entry (1 record, exact `reader_file`).
- Recorded conflict for the judge: the entry's `minor_gaps: 0` / `commands_executed_count: 1`
  (`refresh.py:227-228`) contradict the reader file's three nuances and heavy executions; not in m4's scope.
