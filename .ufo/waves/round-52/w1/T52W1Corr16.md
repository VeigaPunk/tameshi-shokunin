# T52W1Corr16 — correction record for round-51 cold-read re-key entry `### Round-16 gate/probe registry`

Round 52 wave 1, lane `tameshi-shokunin`, criterion **C2 m4** (calibration). Writes, all in
`.ufo/waves/round-52/w1/`: the deliverable `T52W1Corr16.json`, this report, and the verification transcript
`T52W1Corr16.verify.txt`. Nothing else was created or edited in the lane or the fleet root. No tool was
installed (`bash`, `git`, `python3` already present), so no tool/version/channel row is owed. No counter was
run as a verdict: only the frozen `check_findings` helper (`.ufo/evidence/round-52/c2/measure.py:82`) was
imported and exercised on the deliverable. One `git clone --shared` at `read_rev` under
`/fast/scratch/hyaku/tameshi-r52/T52W1Corr16` (toplevel asserted, `TMPDIR=$S`) served one `--bogus` probe; it
was deleted before yield, so no `/tmp` or scratch path is cited as evidence.

## Target

- Reader file: `.ufo/evidence/round-51/coldread/reads/T51W2Read16.md` — read in full (218 lines, sections
  `### P1`–`### P4`, `## 3`, `## 4`, `## 5`). At `read_rev` it is the working-tree bytes:
  `sha256 ad25e25f46f10e351824fa72f9e66882c54abf6b64300d8ea1ee29e594af899e` (both `sha256sum` of the file and
  `git show REV:<same path> | sha256sum`, transcript §2).
- Section text: `git -C LANE show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` lines 1806-1813
  (heading 1806, next heading `## Live-tree re-pin and entry-command monitor — round 17` at 1814, 8 lines).
  Its sha256 is `2642efc5147715676537ab35e1489742f4183b39c8a6ff0e51e25213695be843`, byte-identical to the
  reader's CAND section sha.
- Ledger entry corrected: `.ufo/evidence/round-21/coldread/ledger.json`, entry with
  `heading == "### Round-16 gate/probe registry"`, `read_rev` starting `02ec217c`, seats
  `["T51W2Read16", "L1 TameshiR51a3 integration (attempt 3)"]` — written by round 51's refresh as
  `wrong_expectations: 0`, `minor_gaps: 0`, `verdict: "verified-record"` (transcript §7). The lane's ledger
  has no `corrections` key at base (`'corrections' in ledger -> False`); this JSON is the record the round-52
  assembler appends to that top-level list.

## What the reader recorded as not holding

The reader's four pointer verdicts are all **holds**: P1 (`tools/mutate-and-run.sh`, including the first
end-to-end ten-leg regression), P2, P3, P4 — none is counted. Its §3 then states, verbatim:
"**Unsupported/incomplete premises found (all pre-existing, none round-51-introduced):** P2 omits its
selftest-1 exit and silently defaults `--repo` to the live lane path; P4 omits argparse exit 2; P3's
"(round 17)" tag is imprecise provenance." That is four distinct section statements, each recorded against
the section's own bytes; `wrong_expectations` is therefore **4**, not 0.

| # | class | skill_statement (SKILL.md at read_rev) | reader quote (T51W2Read16.md line) | command that shows it |
|---|---|---|---|---|
| 1 | unsupported | `0 measured · 2 rev/blob missing · 64 usage` (:1811) — the Exits map covers neither `--selftest` outcome | `Note (minor, pre-existing, not a round-51 falsification): the Exits cell omits the \`--selftest\` failure` (:92) | `git -C LANE show REV:.ufo/evidence/round-16/measure.py \| sed -n '626p'` → `return 0 if passed == len(checks) else 1`; the command cell names `--selftest` (:1811), so exit 1 is reachable and omitted (transcript §3). |
| 2 | unsupported | `` `python3 .ufo/evidence/round-16/measure.py --rev REV` `` (:1811) — implied premise: it measures the repo it runs in | `Note (premise, undisclosed in this section): the command cell has no \`--repo\`; the tool defaults` (:94) | `… measure.py \| grep -n DEFAULT_REPO` → `53:DEFAULT_REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'`, `634: parser.add_argument('--repo', default=DEFAULT_REPO,`; every measurement call uses `args.repo` (`:643-660`), never cwd (transcript §4). |
| 3 | unsupported | `0 corrected rule passes the oracle · 1 it fails` (:1813) — two-code map presented for an argparse tool | `Note (minor, pre-existing): the tool is argparse-based (:337) and \`--bogus\` → **exit 2**` (:128) | `… reattribute.py \| grep -n ArgumentParser` → `337: parser = argparse.ArgumentParser(description=__doc__)`; in a shared clone detached at REV, `python3 .ufo/evidence/round-16/attribution/reattribute.py --bogus` → usage + `error: unrecognized arguments: --bogus`, **exit 2** (transcript §5). |
| 4 | unsupported | `2 usage (argparse), an invalid override or a heading mismatch (round 17)` (:1812) — the `(round 17)` provenance tag | `Note (cosmetic): the "(round 17)" tag on "a heading mismatch" is imprecise provenance — the round-16` (:115) | `… assemble.py \| grep -n "heading mismatch\|except AsmError"` → `86:` AsmError docstring "heading mismatch", `1069-1071` `except AsmError: … return 2`; `git log -1 --format='%h %ci %s' REV -- .ufo/evidence/round-16/coldread/assemble.py` → `3490708 2026-10-20 … round-16: …` — the branch predates round 17, so the tag's attribution is unsupported (transcript §6). |

Class notes: the frozen taxonomy (`false | stale-pointer | unsupported | stale-count`) has no
"incomplete-map" or "provenance" value. Findings 1 and 3 are omissions from a declared exit map (nothing the
map declares is false), and 2 is an undisclosed default; all three assert a capability/coverage premise the
bytes do not support. Finding 4 is a provenance attribution — the precedent for a provenance statement that
does not hold is `unsupported` (round-52 `T52W1Corr01.json` finding 3, the nonexistent report path).

## Excluded on the item's rule

- The reader's P1/P2/P3/P4 "holds" verdicts, and its P1 note that the runner row "names no temp path, so
  nothing it claims is touched" — holds verdicts, not failures.
- The P2 side observation (the round-16 instrument reports `calibration_restraint_score` 6 at base and CAND
  because its own ledger pins predate base, T51W2Read16.md:99-101): it concerns the round-16 ledger's input
  drift, not a statement in this section; the section states no score.
- The reader's "not run-verified" remark on the runner's `1 FAIL` branch (T51W2Read16.md:39-41): the section's
  claim was confirmed by code + selftest vectors; the gap is in the reader's probing, not the section.
- The P3 note's clause "The behavior claim itself is accurate" (`:117`) — excluded as an accuracy verdict; the
  counted part of that note is the `(round 17)` provenance, which the reader calls imprecise.

## Self-check (frozen counter's rule)

`check_findings` from `.ufo/evidence/round-52/c2/measure.py:82` (20-character minimum after `squash`,
membership in the whitespace-collapsed reader file; `FLOORS` has no `T51W2Read16` key, so floors = `()`),
run against the reader bytes at `read_rev`, plus the item's one-line rule and a section-substring check on
each `skill_statement`:

```
len=103 lines=[92] | Note (minor, pre-existing, not a round-51 falsification): the Exits ce
len= 96 lines=[94] | Note (premise, undisclosed in this section): the command cell has no `
len= 88 lines=[128] | Note (minor, pre-existing): the tool is argparse-based (:337) and `--b
len=100 lines=[115] | Note (cosmetic): the "(round 17)" tag on "a heading mismatch" is impre
check_findings -> None
count -> 4 4 True
```

`None` is the helper's success return (`.ufo/evidence/round-52/c2/measure.py:95`). Each quote is a substring
of exactly one reader line (92, 94, 128, 115), verified after whitespace collapse; each `skill_statement` is a
verbatim substring of the 8-line section at `read_rev`.

## Artifacts

- `.ufo/waves/round-52/w1/T52W1Corr16.json` — deliverable: heading, read_rev, reader, reader_file,
  `wrong_expectations: 4`, four findings (`quote`, `class`, `skill_statement`).
- `.ufo/waves/round-52/w1/T52W1Corr16.verify.txt` — command transcript (sections 1-8 above).
- `.ufo/waves/round-52/w1/T52W1Corr16.md` — this report.

Scratch: `/fast/scratch/hyaku/tameshi-r52/T52W1Corr16` (one shared clone at `read_rev`, `TMPDIR` pointed
there) was deleted before yield; nothing was written under `/tmp` beyond the transient extracted
`reattribute.py`/section file used for the probes, both removed.

## Summary

- Rebuilt the correction record for `### Round-16 gate/probe registry` (read_rev `02ec217c…`, reader
  `T51W2Read16`): `wrong_expectations` 4, not the 0 round 51's refresh wrote.
- Four reader-recorded defects, each a verbatim one-line quote: P2's omitted `--selftest` exit 1
  (measure.py:626), P2's undisclosed live-lane `--repo` default (measure.py:53/634), P4's omitted argparse
  usage exit 2 (reattribute.py:337, probed exit 2), P3's unsupported `(round 17)` provenance tag
  (assemble.py:86/1069-1071, last committed `3490708`).
- Section bytes at read_rev are 1806-1813, sha256 `2642efc5…`, byte-identical to the reader's CAND section;
  reader file sha256 `ad25e25f…`, identical in the tree and at read_rev.
- `check_findings` → `None`; count 4 == len(findings); every quote single-line, 88-103 chars.
- All four reader pointer verdicts are holds and excluded; the side observation and the "not run-verified"
  remark are excluded with reasons above.
- Read-only on the lane; no counter was run as a verdict; deliverable, report and transcript are the only
  writes; scratch deleted.
