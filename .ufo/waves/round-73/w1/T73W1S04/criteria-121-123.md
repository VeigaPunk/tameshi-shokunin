# QUALITY.md criteria 121–123 — draft (round 73, seat T73W1S04)

Draft text for `corpus/QUALITY.md`, appended after criterion 120 (the file's own
convention: no new `##` section heading — criterion 120, added in round 63
(`8616d47e`), also sits under `## Criteria appended — round 60`). Not applied by
this seat: the L1 lands every production byte.

Every command below was run by this seat on this host on 2026-11-03; its output
is pasted verbatim. Revisions named: `3664a6d3` is the round-72 report commit in
the fleet repo (`/home/vgpnk/Projects/shokunin`); `9b4ffe47` is the round-72
lane tip and `f20ba48` its round base in the lane repo
(`/home/vgpnk/Projects/shokunin/tameshi-shokunin`).

### Criterion 121 — a round record's execution claims are re-derivable from its committed wave artifacts; a printed count the artifacts contradict is a calibration defect

A record that prints how many seats a wave ran, how many seat reports the wave
committed, or which roles those seats held is making a claim about committed
artifacts, and the claim must survive re-derivation from those artifacts at
their own revision. The re-derivation reads the artifacts, not the record's
other sentences: the seat count is `seats`/`len(results[])` in the wave's
`w1-results.json`, the seat-report count is the `*.md` files at the top of the
wave directory at the artifact revision, and the role multiset is the `agent`
field of the same `results[]`. A printed figure the artifacts contradict is not
a rounding difference or a phrasing choice — it is the record running ahead of
the bytes, and the round's own instruments must be able to say so on every
sweep.

Lesson: `corpus/lessons/round-72-verifier-spotcheck.md` §1 and §6 routed
defects 1 and 2 (class record-runs-ahead-of-artifacts): the round-72 report
printed "12 seats, 11 reports" while twelve seat reports and twelve
`w1-results.json` seat records were committed at `9b4ffe47`, and the frozen
plan declared `1 labrat` while the executed wave ran `revenger`. The class is
why round 73's `tools/wave-reconcile.py` carries these two drifts as standing
red arms measured on every sweep.

Falsifier that must fail: `git -C /home/vgpnk/Projects/shokunin show
3664a6d3:.ufo/reports/round-72/tameshi.md | sed -n '56p'` prints

```
- **The wave** (see "Wave" below): 12 seats, 11 reports; three seats found real
```

while `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r
--name-only 9b4ffe47 -- .ufo/waves/round-72/w1 | grep -cE
'^\.ufo/waves/round-72/w1/[^/]+\.md$'` prints `12`, and the same revision's
`w1-results.json` prints `seats=12 results=12`
(`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show
9b4ffe47:.ufo/waves/round-72/w1-results.json | python3 -I -X utf8 -c
"import json,sys; d=json.load(sys.stdin); print('seats=%d results=%d' %
(d['seats'], len(d['results'])))"`) — the record's printed report count
contradicts the population the record itself names.

*Draft note (wording choice): binding the printed count to the artifacts read at
the artifact revision (`w1-results.json`, the top-level `*.md` population) rather
than to the record's other sentences is what makes the falsifier fail today —
"11 reports" against twelve committed reports needs no second reading of the
report.*

### Criterion 122 — a manifest's self-description (its `note`, totals or counts) equals the rows it carries, or carries no count

When an instrument's manifest states in its own `note` — or in any header field
carrying a total — how many rows of a class it carries, that sentence is a claim
like any other and must equal the rows present in the same manifest. The note
is exactly the field no census, gate or selftest parses, so a closure that reads
the note instead of the rows reaches the wrong figure. Either the count stays in
step with the rows it describes, or the manifest carries no count at all.

Lesson: `corpus/lessons/round-72-verifier-spotcheck.md` §6 routed defect 4
(class stale-self-description): `tools/pointer-recheck.json`'s note ended
"round 72 adds three green arms" while four round-72 green arms were present
(the fourth, `province-r72-sixleg-cut-88-93`, was added after the freeze and
disclosed elsewhere). The note is not append-only by contract, so the count is
corrected rather than pinned.

Falsifier that must fail: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin
show 9b4ffe47:tools/pointer-recheck.json | python3 -I -X utf8 -c
"import json,sys; n=json.load(sys.stdin)['note']; print(n[n.index('round 72
adds'):])"` prints

```
round 72 adds three green arms: the S303 §4.2 supersession pointer and the two corrected PROVINCE spans (:88-94 seven-leg cut, :88-97 ten-leg ledger), each paired with a control row in .ufo/evidence/round-72/control-manifest.json that must read miss without the correction.
```

while the same manifest, diffed over the round-72 range
`f20ba48`→`9b4ffe47`, gains four rows, all green
(`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff f20ba48 9b4ffe47
-- tools/pointer-recheck.json | grep -c '^+.*"expect": "hit"'` prints `4`, and
the added ids are `sources-s303-sed-4-2`, `province-r72-tenleg-88-97`,
`province-r72-sevenleg-cut-88-94`, `province-r72-sixleg-cut-88-93`) — the
note's count and the rows' count disagree at the same bytes.

*Draft note (wording choice): scoping the sentence to the manifest's own
self-description against its own rows, with the falsifier pinned at `9b4ffe47`,
is what makes it fail today — the note's "three" against four green rows — while
the corrected round-73 note passes unchanged.*

### Criterion 123 — a prose sentence about a counter's behaviour is measured on the real input, not only on a fixture; a mechanism true only of a same-scope fixture is stated as such

A record's sentence about what a gate prints — an error code, a warning, an
exit status — is a measurement of the input it names. A fixture that reaches a
code path by aligning two strings the real input keeps apart establishes the
construction, not the live behaviour. When the demonstration is a construction,
the sentence says so and names the alignment; a mechanism stated as live
behaviour that the real input does not exhibit is a defect of the sentence even
when the code path is real and the fixture faithful.

Lesson: `corpus/lessons/round-72-verifier-spotcheck.md` §4 and §6 routed
defect 3 (class fixture-only-mechanism): the round-72 report's "the counter-run
without the prefix prints E04" holds only when the superseding row's scope
string equals the superseded row's. On the real registry S303's scope is
restated, so the same removal prints `W04 duplicate url … across scopes` and
the lane validates clean; the correction of record is `corpus/lessons/round-73.md`
`## Gate — the census sentence`.

Falsifier that must fail: `git -C /home/vgpnk/Projects/shokunin show
3664a6d3:.ufo/reports/round-72/tameshi.md | sed -n '192,194p'` prints

```
  opens `supersedes S302 —`; `used-by corpus/lessons/round-72.md`; census E04
  exemption exercised (the counter-run without the prefix prints E04 — critic
  seat T72W1S08).
```

while the real row at `9b4ffe47` takes the warning path.

```
d=$(mktemp -d) && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive 9b4ffe47 -- corpus tools | tar -x -C "$d"
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$d/corpus/SOURCES.md" > "$d/a.out"; echo "EXIT=$?"
grep S303 "$d/a.out"; grep -cP '\tE04\t' "$d/a.out"; rm -rf "$d"
```

prints

```
EXIT=0
file	W04	S303 duplicate url www.gnu.org/software/sed/manual/sed.html across scopes
0
```

— and the counter-run the sentence names, performed on that same real row
(its `teaches` cell's `supersedes S302 — ` removed; the string occurs once in
the registry, `grep -c 'supersedes S302 — '` on the archived file prints `1`),
prints the same `W04`, exit 0, `E04` count `0`:

```
d=$(mktemp -d) && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive 9b4ffe47 -- corpus tools | tar -x -C "$d"
awk '/^\| S303 /{sub(/supersedes S302 — /,"")} {print}' "$d/corpus/SOURCES.md" > "$d/corpus/SOURCES-B.md"
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$d/corpus/SOURCES-B.md" > "$d/b.out"; echo "EXIT=$?"
grep S303 "$d/b.out"; grep -cP '\tE04\t' "$d/b.out"; rm -rf "$d"
```

```
EXIT=0
file	W04	S303 duplicate url www.gnu.org/software/sed/manual/sed.html across scopes
0
```

`E04` is reachable only after S303's scope cell is replaced by S302's (the
fixture's alignment): that run prints `E04 S303 duplicate url
www.gnu.org/software/sed/manual/sed.html within scope …`, exit 1 — the
mechanism is the scope equality, not the prefix.

*Draft note (wording choice): separating "measured on the real input" from "true
only of a same-scope fixture", with the alignment required to be named, is what
makes the falsifier fail today — the real row's `W04` contradicts the E04
sentence, and E04 appears only once the two scope cells are made equal.*
