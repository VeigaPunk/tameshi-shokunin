seat: ScribeQuality

# QUALITY criteria 85–86 — drafts (round 45, wave 2)

Item: draft two new criteria for `corpus/QUALITY.md` in its current format (`### Criterion NN — …`
heading, rule paragraph, `Lesson:` line, `Falsifier that must fail (…)` fenced block). Drafts only:
the lane was not edited. Insertion point: end of `corpus/QUALITY.md` (1150 lines, last line
`echo "CRITERION-84-FALSIFIER-OK"`, file ends with a newline) under a new
`## Criteria appended — round 45 (2026-10-25)` heading.

Every claim below is either an executed command with its output or marked `[INFERENCE]`.

## Drafts (verbatim; paste as-is)

````markdown
## Criteria appended — round 45 (2026-10-25)

### Criterion 85 — a deciding receipt binds the revision it measured, never the tip that carries it

A round designates its content revision C — the commit that holds every change the round
cites (registry rows, knowledge entries, SCORECARD.md, LOG.md, lessons, tools and counters,
ledger and review inputs, seat and wave reports) — after the last record edit, and runs every
claim counter at C. The receipts are committed afterwards as a follow-up whose diff against C
names receipt paths only: `git diff --name-only C..tip` must list no content path, and the
commits between C and the tip are listed with the records they touch. A receipt written before
C measures an ancestor and certifies nothing about C; a receipt cannot sit inside the commit it
measures, because writing it moves the tip, so "re-run the counter at the final landing tip and
cite the landing-tip receipt" is not executable — the honest form is C measured, receipts after
C, and a drift listing between them that is empty of content. A content edit after C voids the
deciding runs and forces re-deciding at a new C that contains it. A no-harm monitor is cited
green only at a revision where its own frozen grading assumptions hold: the round-44
record-agreement counter grades the newest `## Round N` SCORECARD block against its contract
round, so at a tip whose newest block belongs to a later round it is reported red, never
re-interpreted or cited green.

Lesson: `considerthese/2026-10-25.md:66-68` (proposal 1, "Measured-to-landing drift check"),
grounded by `w1/ExecLiveDriftR43.md` and attacked by `w1/CritDriftClaim.md` (fixed point,
terminality, and the unsatisfiable round-44 monitor). Round 43 is the case the criterion is
written for: green at measured `3c4003f6e97e5c787e7538b2eb35d62f49783aaf`, red at landing
`718a1e987febd32eb78ebc65adfe939f23b3de63`, and the single commit between them —
`718a1e9 round-43: deciding-run receipts and verdict records` — carried the receipts *and* 37
added lines of `SCORECARD.md` plus 3 of `LOG.md`. Round 44 did not drift (green at
`ef990aaea3f6546db20feccbff89ac9ab78c5405` and at `df000ab79a4c526bcb5cbf03a356c1a44fb32e27`),
so the check is not vacuous by construction.

Falsifier that must fail (the round-43 shape; the criterion refuses it because content paths
lie between the measured revision and the tip; run from any cwd):

```
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
M=3c4003f6e97e5c787e7538b2eb35d62f49783aaf   # measured, green
T=718a1e987febd32eb78ebc65adfe939f23b3de63   # landing tip, red
F=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685   # round-43 freeze
git -C "$L" log --oneline "$M..$T"
git -C "$L" diff --name-only "$M" "$T" | tee /tmp/m85-paths.txt
python3 "$L/.ufo/evidence/round-43/calibration/measure.py" --lane "$L" --rev "$M" --freeze "$F"
echo "measured_exit=$?"
python3 "$L/.ufo/evidence/round-43/calibration/measure.py" --lane "$L" --rev "$T" --freeze "$F"
echo "landing_exit=$?"
d=$(grep -cE '^(SCORECARD|LOG)\.md$' /tmp/m85-paths.txt)
[ "$d" -eq 0 ] && { echo "CRITERION-85-FALSIFIER-VACUOUS"; exit 1; }
echo "CRITERION-85-FALSIFIER-OK drift_paths=$d"
```

Recorded output (round-45 `w1/ExecLiveDriftR43.md`; round-45 seats are barred from running the
round-43 counter at these revs, so the counter lines are quoted from that receipt, not re-run):

```
718a1e9 round-43: deciding-run receipts and verdict records
.ufo/evidence/round-43/after/c1-at-3c4003f6.exit
.ufo/evidence/round-43/after/c1-at-3c4003f6.stdout
.ufo/evidence/round-43/after/c2-at-3c4003f6.exit
.ufo/evidence/round-43/after/c2-at-3c4003f6.stdout
.ufo/evidence/round-43/after/c3-at-3c4003f6.exit
.ufo/evidence/round-43/after/c3-at-3c4003f6.stdout
LOG.md
SCORECARD.md
C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=4 sources_rows=114 standing=114 receipts=17 revisions=3 m13_probe=standing=7_column0=113_valid=114 rev=3c4003f6e97e5c787e7538b2eb35d62f49783aaf freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=true
C2_R43: self_pin=1 classes=7 m6=0 m7=1 m8=0 m10=0 m11=0 m12=0 m13=0 total=1 records=4 sources_rows=114 standing=114 receipts=17 revisions=4 m13_probe=standing=7_column0=113_valid=114 rev=718a1e987febd32eb78ebc65adfe939f23b3de63 freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=false first=m7:SCORECARD.md#round-43_unknown_S256
```

A tip diff that lists receipt paths only is the compliant shape and does not exercise this
criterion; the block exits 1 rather than print OK on it.

### Criterion 86 — a quote's length is measured, never written by hand

Every record that labels a quote with a word or token count prints that count from a command
over the quote's own bytes, tokenized the way the accepting counter tokenizes it (the counter's
`fold`, then a whitespace split), and states the count the bar measures — the C1 bar is 6..25
whitespace tokens, so a letter-and-digit word count is a second number and never a substitute
for it. A label that disagrees with the measured count is a record defect fixed append-only
with an errata line naming the measured value, and admission is decided by the counter's grade,
not by the label: a hand-written "20 words" on a 28-token quote misreports the quantity the
6..25 bound tests. A count carried over from a sibling record is hand-written even when that
sibling's count was right.

Lesson: `corpus/lessons/round-44.md:26` labels the Stryker quote "20 words"; measured, it is 28
whitespace tokens (22 letter/digit words) and the round-45 C1 counter grades it
`('invalid', 'quote length 28')` — receipt
`.ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout`. The number is
`corpus/lessons/round-43.md:52`'s correct "20 words" for the shorter quote that is this quote's
suffix: the round-44 quote prepends 8 tokens and inherited the label. The round-44 spotcheck
called the label cosmetic (`corpus/lessons/round-44-verifier-spotcheck.md:73`) because the row's
grounding quote was compliant, and its own parenthetical "24 letter/digit words" is itself
unmeasured (measured: 22).

Falsifier that must fail (the round-44 label; prints the receipt's three lines, exits 0 only
when the hand-written label disagrees with the measured count; run from any cwd):

```
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
rc=0; python3 - "$L" <<'EOF' || rc=$?
import hashlib, importlib.util, re, sys
lane = sys.argv[1]
spec = importlib.util.spec_from_file_location(
    'c1', lane + '/.ufo/evidence/round-45/freshness/measure.py')
c1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
line = open(lane + '/corpus/lessons/round-44.md', encoding='utf-8').read().split('\n')[25]
label = int(re.search(r'(\d+) words', line).group(1))
quote = c1.fold(re.search(r'\u201c(.+?)\u201d', line).group(1))
print('lesson label: "%d words"; quote=%r' % (label, quote))
print('whitespace_tokens=%d letter_digit_words=%d'
      % (len(quote.split()), len(re.findall(r'[A-Za-z0-9]+', quote))))
raw = b'x'
row = {'url': 'https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/',
       'source': '', 'scope': '', 'anchor': '', 'teaches': ''}
entry = {'url': row['url'], 'opened': '2026-10-25', 'verdict': 'holds',
         'raw_sha256': hashlib.sha256(raw).hexdigest(), 'quote': quote}
print('C1 grade on the round-44 label quote: %r' % (c1.grade(entry, row, raw),))
sys.exit(0 if label != len(quote.split()) else 1)
EOF
[ "$rc" -eq 0 ] || { echo "CRITERION-86-FALSIFIER-VACUOUS"; exit 1; }
echo "CRITERION-86-FALSIFIER-OK"
```

Expected output (the committed receipt, reproduced byte-identically by this block):

```
lesson label: "20 words"; quote='Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!'
whitespace_tokens=28 letter_digit_words=22
C1 grade on the round-44 label quote: ('invalid', 'quote length 28')
CRITERION-86-FALSIFIER-OK
```

The synthetic `entry`/`raw` pair exists only to reach the counter's length conjunct: it passes
the url, opened, snapshot and sha256 tests, so `quote length 28` is the first rule that fires.
The counter is imported, not invoked as a counter (`--lane/--rev`); no measurement is taken.
````

## Gates run (with output)

1. Receipt reproduction — the reconstruction is byte-identical to the committed receipt.

```
$ python3 /tmp/tameshi-r45-ScribeQuality/producer.py > producer.stdout
lesson label: "20 words"; quote='Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!'
whitespace_tokens=28 letter_digit_words=22
C1 grade on the round-44 label quote: ('invalid', 'quote length 28')
$ diff producer.stdout .ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout && echo IDENTICAL
IDENTICAL
```

2. Criterion 86 falsifier block, run exactly as drafted:

```
$ bash /tmp/tameshi-r45-ScribeQuality/block86.sh
lesson label: "20 words"; quote='Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!'
whitespace_tokens=28 letter_digit_words=22
C1 grade on the round-44 label quote: ('invalid', 'quote length 28')
CRITERION-86-FALSIFIER-OK
block86_exit=0
$ bash block86.sh | sed '/CRITERION-86-FALSIFIER-OK/d' | diff - .ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout
RECEIPT-LINES-IDENTICAL
```

Vacuity path (label rewritten to the measured 28 in a /tmp copy): the same predicate returns
`falsifier exit 1`, i.e. the block prints `CRITERION-86-FALSIFIER-VACUOUS` instead of OK.

2b. The block extracted back out of this report is byte-identical to the tested block and runs
green, so "paste verbatim" is checked, not asserted:

```
$ python3 - <<'EOF'   # extract the fence after "Falsifier that must fail (the round-44 label"
...
EOF
extracted 86 bytes: 1273
$ diff /tmp/tameshi-r45-ScribeQuality/from-report-86.sh /tmp/tameshi-r45-ScribeQuality/block86.sh
REPORT-86-BLOCK==TESTED-BLOCK
$ bash /tmp/tameshi-r45-ScribeQuality/from-report-86.sh
lesson label: "20 words"; quote='Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!'
whitespace_tokens=28 letter_digit_words=22
C1 grade on the round-44 label quote: ('invalid', 'quote length 28')
CRITERION-86-FALSIFIER-OK
from_report_86_exit=0
```

3. Criterion 85 falsifier, git half only (read-only):

```
$ git -C "$L" log --oneline 3c4003f6..718a1e98
718a1e9 round-43: deciding-run receipts and verdict records
$ git -C "$L" diff --name-only 3c4003f6 718a1e98
.ufo/evidence/round-43/after/c1-at-3c4003f6.exit
.ufo/evidence/round-43/after/c1-at-3c4003f6.stdout
.ufo/evidence/round-43/after/c2-at-3c4003f6.exit
.ufo/evidence/round-43/after/c2-at-3c4003f6.stdout
.ufo/evidence/round-43/after/c3-at-3c4003f6.exit
.ufo/evidence/round-43/after/c3-at-3c4003f6.stdout
LOG.md
SCORECARD.md
CRITERION-85-FALSIFIER-OK drift_paths=2
```

The counter half of the same block was not executed (bounds); the block extracted from this
report passes `bash -n` (`SYNTAX-OK`) and its git half is the run above.

4. Both labelled quotes measured under the counter's own tokenizer (`corpus/lessons/round-43.md:52`
   and `corpus/lessons/round-44.md:26`):

```
round-43.md:52 label "20 words"    whitespace_tokens=20 letter_digit_words=16
round-44.md:26 label "20 words"    whitespace_tokens=28 letter_digit_words=22
r43 token list: ['even','if','we','change','>=','to','<=','and','even','<','or','>','we','will','get','the','same','output','each','time!']
delta tokens: ['Notice','that','10','**','0','=','1,','so']
suffix_shared= True
```

## Findings

1. **The label's provenance is now measured, not inferred.** `corpus/lessons/round-44.md:26`
   labels 28 tokens as "20 words"; the 20 is `corpus/lessons/round-43.md:52`'s correct count for
   the shorter quote, and the round-44 quote is that quote verbatim as a suffix plus 8 prepended
   tokens (`suffix_shared= True`, gate 4). Criterion 86's rule text carries this mechanism
   ("a count carried over from a sibling record is hand-written even when that sibling's count
   was right") because a rule that only says "measure the quote" would not have caught it.
2. **The round-44 spotcheck's own number is wrong.**
   `corpus/lessons/round-44-verifier-spotcheck.md:73` says "~28 (24 letter/digit words)";
   measured letter/digit words = 22. The record that flagged the defect hand-estimated the
   replacement number, so the defect class survived its own correction — evidence that criterion
   86 must demand a printed count, not a more careful estimate.
3. **Criterion 85 cannot be written as "re-run at the landing tip".** `w1/CritDriftClaim.md` D1
   (fixed point) is decisive: a receipt cannot be inside the commit it measures. The draft
   therefore names a content revision C, requires `git diff --name-only C..tip` to list receipt
   paths only, and voids the deciding runs on any later content edit. This also supplies the
   half of proposal 1 that `contract.json:46` dropped — the drift listing
   (`considerthese/2026-10-25.md:66-68` lists "the commits between the measured commit and the
   landing tip that touch records").
4. **The monitor clause is required for the criterion to be satisfiable.** `w1/CritDriftClaim.md`
   D3: `.ufo/evidence/round-44/calibration/measure.py` grades the newest SCORECARD block against
   its contract round (round 44), so at any round-45 tip it is red by construction. A criterion
   that mandated "every counter green at the tip" would force either a non-tip run or a false
   green; the draft's last sentence states the narrower, executable rule. [INFERENCE] from the
   code path quoted in that report; I did not re-run the round-44 counter (bounds: only
   `--rev 3310e7b…`/`5891bdb…` are permitted, and its before-receipt already records the
   PASS=true-at-round-44 shape).
5. **The 85 falsifier is partly unexecutable for this round's seats, by design of the bounds.**
   Its counter half targets `3c4003f6`/`718a1e98` under the round-43 freeze, which no round-45
   seat may run; the draft quotes those two lines from `w1/ExecLiveDriftR43.md` and labels them
   as recorded. The git half was executed here (gate 3). A criteria owner running it later
   should see the two exact counter lines reprinted.

## Known limits

- The receipt's producer command is **not committed anywhere**: `grep -rn 'whitespace_tokens|letter_digit_words|quote-token'`
  over the lane matches only the receipt itself and the dispatch specs. The block in criterion 86
  is a **reconstruction** that reproduces the receipt byte-for-byte (gate 1) — identical output
  is evidence of an equivalent command, not proof of the original one. The criterion text says
  so only implicitly ("reproduced byte-identically"); a future round may want the original.
- `c1.grade` is reached with a synthetic `raw=b'x'` so that the length rule is the first
  conjunct to fire; the block therefore grades the *length*, not the quote's presence. That is
  the quantity the label misreports.
- No round-45 claim counter was run at any revision. The C1 module was imported read-only
  (`importlib`, `__name__ != '__main__'`, so `main()` never ran).

## Out of scope / not done

- `corpus/QUALITY.md` not edited (drafts only, per item). No other lane file written; the only
  write is this report.
- No git/jj mutation, no counter deciding run, no `agent://all` message, no tool installed or
  upgraded (pacman is host-wide paused; nothing was needed, so `RULES.md` was not consulted).
- Scratch: `/tmp/tameshi-r45-ScribeQuality/` (`producer.py`, `producer.stdout`, `block86.sh`,
  `block85-git.sh`, `vac/round-44.md`).

## Artifacts

- Drafts: this file, section "Drafts (verbatim)".
- Receipt reproduced: `.ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout`.
- Grounds: `considerthese/2026-10-25.md:66-68`; `.ufo/waves/round-45/w1/ExecLiveDriftR43.md`;
  `.ufo/waves/round-45/w1/CritDriftClaim.md`; `corpus/lessons/round-43.md:52`;
  `corpus/lessons/round-44.md:26`; `corpus/lessons/round-44-verifier-spotcheck.md:73`;
  `corpus/lessons/round-43-verifier-spotcheck.md:28`;
  `.ufo/evidence/round-45/freshness/measure.py:100` (`fold`), `:132` (`grade`),
  `:151-152` (the 6..25 length rule);
  `.ufo/evidence/round-45/contract.json:46`.
