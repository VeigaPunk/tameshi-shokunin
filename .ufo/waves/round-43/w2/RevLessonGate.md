# RevLessonGate — round 43, wave 2 (falsify)

Item: verify every quote in `## Gate` of `corpus/lessons/round-43.md` against the committed
snapshots under `.ufo/evidence/round-43/sources/` — byte count, sha256, line number, verbatim
presence in tag-stripped text at the cited line, word count > 25 — and answer whether the
Wikipedia revision carries an `Equivalent mutants` heading.

Lane access: read-only except this file. No counter was run at `c5335c70…`; C1/C2/C3 counters
were not executed at all (out of item). No tool installed or upgraded (python3 3.13,
coreutils, curl already present).

**Review window note.** The L1 landed lesson revision `e25cd2f` mid-review (fix commit +
uncommitted `considerthese` rewording). All findings below are stated against the **current**
text — which now carries Mistakes rows `asserted-digest-equality` (:134) and
`uncounted-quote-length` (:135) documenting this item's defect classes.

## Verdict

- 4 of 5 located quotes are verbatim at their cited lines; **the Stryker line-15 quote is
  still not verbatim** (`round-43.md:52-53`), and the Mistakes table now falsely claims it was
  "restored verbatim" (:135) — a fix claim that does not hold.
- Both snapshot byte counts, both sha256s, both `<title>`s, the revid, and both physical line
  counts are exactly as claimed.
- No quote exceeds 25 words (max 20). The two wrong counts are now **fixed** (16 and 15 at
  `round-43.md:25,28`).
- The Wikipedia heading claim is **correct**: `grep -c 'Equivalent_mutants'` → 0; no `h1`–`h6`
  contains "equivalent"; both quotes sit inside `Mutation testing overview` (h2 at line 762,
  next h2 at 800).
- **New defect introduced by the e25cd2f revision**: "the **eight** ids immediately above the
  registry maximum" (:87-88) — the naive map lands on **seven** (S160–S166); the sentence
  contradicts its own "cascade 7".
- The S089 byte-equality sentence is now **correct** ("drifted", :44-49); S089's own row still
  pins the stale digest (`corpus/SOURCES.md:98`).

## Snapshot facts (measured)

```
$ cd .ufo/evidence/round-43/sources
$ sha256sum wikipedia-mutation-testing.html stryker-equivalent-mutants.html
6e4a06c0863ca2b0f68c36a1e29ca1eeeb01d20ae5e1d9ed4534a81406decc43  wikipedia-mutation-testing.html
79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce  stryker-equivalent-mutants.html
170793 B / 1159 physical lines (wikipedia); 38687 B / 24 physical lines (stryker)
```

`sha256.txt` carries both digests verbatim. `wc -l` returns 1158 / 23 **because neither file
ends in a newline**; the Gate's 1159 / 24 are correct as *physical* lines.

Live re-fetch today (read-only, to `/tmp`): Wikipedia re-fetches `6e4a06c0…` / 170793 B /
revid 1373580212 (current revision per MediaWiki API, timestamp 2026-09-06). Titles:
`Mutation testing - Wikipedia` and `<title data-rh=true>Equivalent mutants | Stryker
Mutator</title>`.

## Quote-by-quote

| Gate line | cited at | verbatim at line (tag-stripped) | words claimed | words actual |
|---|---|---|---|---|
| `round-43.md:25-27` | `wikipedia…html:794` (`<p id="mw-Q">`) | **yes** (the `<i id="mw-g">` around "equivalent mutants" strips out cleanly) | 16 | **16** ✓ |
| `round-43.md:28-29` | `wikipedia…html:796` (`<p id="mw-w">`) | **yes** (span ends before the `<sup>` cite) | 15 | **15** ✓ |
| `round-43.md:51-52` | `stryker…html:16` | **yes** | 12 | 12 |
| `round-43.md:52-53` | `stryker…html:15` | **NO — "or" still deleted** | 20 | 19 as printed / 20 as source |
| `round-43.md:53-54` | `stryker…html:17` | **yes** | 9 | 9 |

Raw markup proof (the "or" is plain text between two `<code>` elements — no tag-stripping
convention removes it):

```
$ python3 -c "raw=open('.ufo/evidence/round-43/sources/stryker-equivalent-mutants.html',encoding='utf-8').read();print(repr(raw[30613:30830]))"
'10 ** 0 = 1, so even if we change <code>>=</code> to <code>&lt;=</code> and even <code>&lt;</code> or <code>></code> we will get the same output each time!</p>\n<p>It is called <em>equivalent mutant</em>. There is no d'
```

Gate text (lines 52-53, current bytes): `"even if we change >= to <= and even < > we will get
the same output each time!"` — `raw.count(...)` of that string over the snapshot → 0.

## Findings (severity order)

### F1 — HIGH: Gate quote still non-verbatim, and the Mistakes table claims a fix that did not land

- `round-43.md:52-53` still prints `even < >` — the word `or` from `<code>&lt;</code> or
  <code>></code>` is still dropped.
- `round-43.md:135` (`uncounted-quote-length` row) says "the quotation restored verbatim" and
  names the exact defect (`even < >` for `even < or >`). The fix column is false: the Gate
  text at :52 is byte-for-byte the truncated string.
- Reproduce: `sed -n '52,53p' corpus/lessons/round-43.md` and the `repr(raw[30613:30830])`
  command above. The printed 20-word count is consistent with the *untruncated* source, so the
  count was computed from the true string while the displayed quote lost the word.
- Load-bearing: this quote is S089's "same output each time" example for the
  survivor-resolution rule; a quotation that omits the alternative operator weakens exactly the
  claim it cites.

### F2 — MEDIUM: "the eight ids" — new arithmetic error landed in e25cd2f (`round-43.md:86-88`)

Gate text: "the naive arithmetic map … lands on **the eight ids** immediately above the
registry maximum, which are themselves staged ids: refused, cascade 7."

Reproduce:

```
$ python3 tools/staged-id-guard.py --registry corpus/SOURCES.md \
    --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json
"naive_map": {"S153":"S160","S154":"S161","S155":"S162","S156":"S163","S157":"S164","S158":"S165","S159":"S166"}
```

The map lands on **seven** ids, `S160`–`S166` — and the sentence contradicts itself by naming
`cascade 7` two clauses later. The pre-revision text said `S160`–`S166`, which was correct.
Suggested text: "lands on the **seven** ids immediately above the registry maximum
(S160–S166)". Note the safe-floor phrasing in the same paragraph ("one above the larger of the
two maxima") is correct — max S159 registry vs S255 staged → S256, which the SOURCES.md tail
note still names (`corpus/SOURCES.md`, "the safe floor for a partial adoption is `S256`").

### F3 — MEDIUM-LOW: census `W04 S159` quote has no committed capture (`round-43.md:61`)

```
$ grep -rn 'S159 duplicate' /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/
.ufo/waves/round-43/w1/ScribeRows.md:102:  file\tW04\tS159 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
```

Its only occurrence is a wave-1 seat report describing Variant A2 — a scratch registry at
`/tmp/tameshi-r43-ScribeRows-validate/A2/corpus/SOURCES.md` (`ScribeRows.md:92-104`), not the
lane's own census of the withdrawn working-tree row. The committed captures cannot contain it:
`census-sources/start.stdout` is the 113-row baseline (9 × W04 + 1 × W01 + `ok`), and
`after.stdout` is **byte-identical to `start.stdout`** (`diff` → identical, 11 lines each), so
it evidences neither a 114-row count nor an S159 warning. `ExecCensus.md:22-34` lists only the
10 baseline warnings.

If the L1's working-tree run existed, its stdout was not committed. Cite `ScribeRows.md:102`
(labelled a scratch variant) or commit the capture; as written the Gate presents a seat's
synthetic-registry output as the lane census.

### F4 — LOW: S089's row still pins the stale digest (partial hold, honestly disclosed)

The Gate now correctly says "drifted … `last-modified: Sat, 24 Oct 2026 15:08:38 GMT` … the
round-44 recheck should move S089's anchor to this snapshot" (:44-49). But
`corpus/SOURCES.md:98` still pins `html sha256 bc572676…e04d` as S089's anchor — that digest no
longer reproduces (two live fetches today, default UA and `Mozilla/5.0`, both `79f6501a…` /
38687 B; last-modified postdates the 2026-10-22 anchor). Prose is unmoved:
`raw.find('10 ** 0 = 1') == 30613` and `raw.find('no definitive way for Stryker') == 30826`,
matching round-26's recorded offsets (`.ufo/waves/round-26/w1/DraftSourcesRows.md:129-131`).
The Gate flags the staleness itself, so this is a disclosed residual, not a hidden defect —
note it so the "recheck unchanged" at :55 is not read as "anchor still reproduces".

### F5 — INFO: Wikipedia section claim verified

`grep -c 'Equivalent_mutants'` → 0 (exit 1); `grep -iE '<h[1-6][^>]*>[^<]*equivalent'` → no
match. Heading inventory: h2 `Mutation testing overview` at line 762, next h2 `Mutation
operators` at line 800; both cited paragraphs (794, 796) fall inside, and paragraph ids
`mw-Q`/`mw-w` match the raw tags. "No equivalent-mutant section of its own" and "both in the
`Mutation testing overview` section" are both true.

Caveat: absence of a heading ≠ absence of coverage — `Equivalent Mutant Problem` appears at
line 796 and `In addition to equivalent mutants…` at 798. The Gate does not overclaim.

Survivor vocabulary claim holds: `grep -c -iE 'surviv|unreach|unkilled|undetected'` → 0 over
the whole artifact.

## Claims that check out (no action)

- `:78-80` — registry 114 rows, S159 the only new row, `Next unused id: S160` at the
  SOURCES.md tail (`grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` → 114; tail line
  verified).
- `:83-90` — collisions: guard `--json` gives `collision_count=7` (S153–S159),
  `held={S153:S105, S154:S106, S159:S155}`, `cascade_count=7`, `next_free=S160`,
  `safe_floor=S256`, `staged_rows=103`, `staged_max=S255`. Registry labels match
  (`corpus/SOURCES.md:117` S105 POSIX diff, `:118` S106 google/golden, `:125` S155 PIT basic
  concepts).
- `:96-103` — census attribution is now honestly qualified ("the receipts carry the validate
  lines and the exit code …, not a row count, which is what `grep -cE` above is for"); the
  earlier over-attribution is repaired.
- `:70-73` — `merge/tameshi/knowledge/corpus/knowledge/mutation-score-semantics-cjk.md` exists
  and its `:56` is the `CANNOT-ANSWER.md §3.7` pointer; `corpus/lessons/round-42.md:99`
  records "Both gates said admit", so "gates admit in round 42" is accurate.
- Mistakes row `asserted-digest-equality` (:134) — its stated fix is true of the Gate text
  (the drift wording is now correct); F1 here is the residual, not that row.
- Byte counts, both sha256s, both titles, revid 1373580212, ≤25-word rule.

## Residual risk / verification gaps

- The two "second fetch byte-identical" claims are not auditable from the repository: no fetch
  log or second capture is committed. I reproduced identical digests today; the committed
  record cannot prove the same-day second fetch.
- The S089 2026-10-22 capture is not in evidence (`/tmp/equivalent-mutants.html`, round 26);
  "same prose, same offsets" reproduces only against the round-26 offset note — which does
  match today's bytes (30613/30826).
- `after.stdout` byte-identical to `start.stdout` means nothing in the committed capture
  distinguishes "round end" from "round start"; the 114-row claim rests on the SOURCES.md
  grep (which I verified).
- `round-43.md:139` still says "the two new rows (S159 only, after the withdrawal)" — the
  parenthetical already flags it, but "two" is wrong in the delivered text (ScribeLessonGate
  noted it; a cosmetic leftover outside the Gate).
- Scope: C1/C2/C3 counters and the deciding run were deliberately not executed here.
