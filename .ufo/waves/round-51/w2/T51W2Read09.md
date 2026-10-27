# T51W2Read09 — cold-read re-key reader: `### The tick, executed`

Seat `T51W2Read09` · round 51 wave 2 · read-only verification at candidate
`6d8c11e378aa90b12650808e1b79270742935f15` (base `9962033fd7a75aa2f2847e979dd687a5d28505a1`).
Method: re-resolved the heading at CAND (`### The tick, executed` at SKILL.md:1164; next heading
`### The receipt at this boundary` at 1212; section span 1164–1211), read the full section plus the
adjacent parent intro (1155–1163) and the two following sections for context, then opened every
cited surface against CAND bytes (`git show CAND:<path>` materialized into seat scratch; no live-lane
writes, no git mutations, no tools installed). The old READERS_JSON and the w1 fixture list were not
trusted; every verdict below is from CAND bytes read this seat.

## reads.json row

```json
{
  "seat": "T51W2Read09",
  "read_rev": "6d8c11e378aa90b12650808e1b79270742935f15",
  "heading": "### The tick, executed",
  "section_span_cand": [1164, 1211],
  "next_heading": {"line": 1212, "text": "### The receipt at this boundary"},
  "section_class": "record (timestamped round-9 tick observation; self-scoped 'never carried as a standing claim', SKILL.md:1188-1189)",
  "verdict": "holds-with-findings",
  "pointers": [
    {
      "raw": "recorded pins/revisions are the harness's `PIN_*`/`REV_*` for the four embedded legs (`tools/mutate-and-run.sh:511-518`)",
      "file": "tools/mutate-and-run.sh",
      "range": "511-518",
      "verdict": "moved",
      "located": "at CAND 511-518 is run_sweep's mutant-preparation loop ('local id line desc mutant aout fail=0' / 'cp -p \"$PRISTINE\" \"$mutant\"'); the PIN_*/REV_* block now sits at tools/mutate-and-run.sh:614-633 (PIN_JS=83016d45… at 614 … REV_DRIFTPINS=e64e81b8… at 633) and covers TEN legs, not four — the r51 tenth leg bash-drift-pins (PIN_DRIFTPINS/REV_DRIFTPINS 632-633, TABLE_DRIFTPINS 643, regression_case_git call 1504-1508). 'Four embedded legs' is tick-scoped (true at the r7-1 tool cf41efaa…, 1 341 L); at base (a7d3f2dd…, nine legs) the block already sat at 605-622, so the anchor was stale before r51 and moved further with the tenth leg + TMPDIR comment edits. All six table rows' recorded revs/pins still equal the CAND PIN_*/REV_* values exactly (175de6ba/83016d45, fecee874/275d8294, 165307fe/084951be, eead56b2/d7edaab4, fecee874/7e5ec98b, 175de6ba/e9a21b44)."
    },
    {
      "raw": "tool **held** at `cf41efaa…` (`sha256sum tools/mutate-and-run.sh`)",
      "file": "tools/mutate-and-run.sh",
      "range": null,
      "verdict": "holds-as-history",
      "located": "file exists at CAND (2 159 L); CAND blob sha256 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda, base a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 — neither is cf41efaa…. cf41efaa… is the tick-time sha, corroborated by ER-4 (ledger:320 'cf41efaa8be5f52d… (1 341 L / 61 632 B, r7-1): held') and the addendum's 20:02Z re-read (ledger:360). The section scopes the tick as a timestamped observation 'never carried as a standing claim' (SKILL.md:1188-1189); no current-state currency is claimed."
    },
    {
      "raw": "scratch `/tmp/w9-tameshi-t93/pin-read-final.txt`",
      "file": "/tmp/w9-tameshi-t93/pin-read-final.txt",
      "range": null,
      "verdict": "absent",
      "located": "path absent now (ls → ENOENT; /tmp/w9-tameshi-t91 also absent). Ephemeral 2026-10-14 scratch. Divergence: the ledger's record of the same tick names scratch `/tmp/w9-tameshi-t91/` (tick.log, pin-read.log; ledger:320) and workdirs `/tmp/w9-tameshi-t91/regression/` (ledger:341), while this page names t93 throughout. Repo-wide grep at CAND: 'w9-tameshi-t93' occurs only in SKILL.md and its round-16/18 snapshots/audits; 'w9-tameshi-t91' only in the ledger and round-20 coldread source dumps; plans/round-9*.md name neither root. Unadjudicable from repo bytes; prior-dispositioned (see falsifier)."
    },
    {
      "raw": "Falsifier, aimed at the reader (scratch copy, `/tmp/w9-tameshi-t93/falsifier/`)",
      "file": "/tmp/w9-tameshi-t93/falsifier/",
      "range": null,
      "verdict": "absent",
      "located": "gone. The falsifier's arithmetic was reproduced without the scratch by round-16 CR20 and round-27 Read17 from git objects: the js-kimi-census row with pin 084951be… has tip blob 83016d45… (differs) at recorded rev = tip, so the doctored row reads stale while the recorded row reads current — the reading follows the row's pin, as claimed. Mechanism consistent with ER-3's command set (ledger:301-303). Not re-executed this seat (scratch gone; harness since changed)."
    },
    {
      "raw": "**ER-4** (`corpus/knowledge/fleet-kill-rate-ledger.md:318-353`)",
      "file": "corpus/knowledge/fleet-kill-rate-ledger.md",
      "range": "318-353",
      "verdict": "holds",
      "located": "ER-4 header at ledger:318; block content 318-352 (tick command set + scratch 320; pin-read intro 'second raw pass 20:00:29Z' 322; six-row table 324-331; headline 'current=4 stale=2 drift=0' 333; drift-event bullets 335-339; regression receipt 341; leg table 343-350; caveats 351; closing 352). Every checked claim matches the section: same six readings cell for cell, second raw pass 20:00:29Z, both drift chains (084951be…→bba6cdf6…; d7edaab4…→7da4ec50…), appended 2026-10-14 by T9-1, plans/round-9.plan.md leg 1. Ledger blob sha256 13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e is byte-identical to the blob the round-18 audit opened (unchanged since round 18; unchanged base→CAND)."
    },
    {
      "raw": "(ER-4's addendum, `:354-360`, records the same continuation at 20:02Z with its then-current shas)",
      "file": "corpus/knowledge/fleet-kill-rate-ledger.md",
      "range": "354-360",
      "verdict": "holds",
      "located": "addendum header actually at ledger:356 (the cited range starts two lines early, on the ER-4 separator/blank); bullets at 358-359 (tsukuroi worktree 5d16378d… mtime 20:02:42Z; mado 5b6ace8e… mtime 20:02:38Z) and the 20:02Z tool re-read at 360 — all cited content ('same continuation at 20:02Z with its then-current shas') lies inside 354-360. 'Then-current' is honest: the addendum's shas differ from the page's 20:03:34Z shas (b54f5732…/31364115…), which have no surviving anchor (scratch gone)."
    },
    {
      "raw": "stays [U] (`:1019`)",
      "file": "SKILL.md",
      "range": "1019",
      "verdict": "holds",
      "located": "SKILL.md:1018-1019 'whether any fleet driver would ever invoke the command with no lane acting stays [U].' (parent-intro anchor, adjacent to the section)."
    },
    {
      "raw": "any re-sweep must pin the revision it measures (T3)",
      "file": "SKILL.md",
      "range": "1069",
      "verdict": "holds",
      "located": "trigger T3 is defined in the round-8 section (heading '### Triggers T1–T3 and the re-pin rule' at SKILL.md:1069); the ledger addendum (ledger:362) uses 'trigger T3' identically for the same rule."
    }
  ],
  "command_mentions_not_pointers": ["sha256sum tools/mutate-and-run.sh", "git status --porcelain"],
  "strongest_falsifier": {
    "claim": "the same regression receipt — two records of one tick, kept un-merged and agreeing (SKILL.md:1197-1201)",
    "attack": "the two records of the tick disagree on provenance fields: scratch root (page t93 vs ER-4 t91, ledger:320/341) and the regression receipt's REGRESSION_DATE (page 19:58:59Z, SKILL.md:1215, adjacent section; ER-4 19:58:18Z, ledger:341) — and the page's selftest stamp 19:58:49Z (SKILL.md:1214) postdates ER-4's REGRESSION_DATE, so the two records cannot describe one identical sequential selftest→regression run",
    "result": "divergence real at the provenance-field level; the readings and outcome agree (same six readings, same drift chains, same 4-leg PASS with kills 8/8/6/4, same tool sha). Prior rounds found and dispositioned exactly this: round-16 CR20 (.ufo/waves/round-16/w1/CR20.md:50,92 — 'two independent runs with an identical PASS outcome'; recommended rewording 'the same receipt outcome') and round-27 Read17 (.ufo/waves/round-27/w1/Read17.md gap 4 — 'the same result from two runs'). The proposed smallest corrections were never applied: the page text at CAND still reads 'the same regression receipt … agreeing'. Disclosed here, not smoothed; not novel."
  },
  "findings": [
    "pointer tools/mutate-and-run.sh:511-518 moved at CAND → now 614-633, and 'four embedded legs' superseded by ten (r51 tenth leg); tick-scoped historical statement, anchor stale (prior art: CR20 rec 2, Read17 gap 1)",
    "scratch-root divergence t93 (page) vs t91 (ER-4 ledger:320,341) for the same tick — prior-dispositioned as two independent runs; unadjudicable from repo bytes",
    "REGRESSION_DATE divergence 19:58:59Z (SKILL.md:1215) vs 19:58:18Z (ledger:341) — same disposition; 'the same regression receipt' (1201) still overstates identity at CAND",
    "'that in-flight edit is now committed as 7da4ec50…' (1187) overstates identity: the round-8 in-flight file was dc864c6a… at 99 716 B; the committed 7da4ec50… blob is 131 612 B — a later commit superseded it (ER-4:338 says 'resolved into'); prior art Read17 gap 3",
    "'six minutes later' (1186) is 5 min 15 s (19:15:14Z → 19:20:29Z, SKILL.md:1041/1055); prior art Read17 gap 6",
    "'the owners' own round-9 lanes are editing their gates' (1206) stated without its [I] label; ledger:356 marks it [I]; prior art Read17 gap 5",
    "20:03:34Z worktree shas (b54f5732…/31364115…) have no surviving anchor (scratch gone); ER-4's addendum records the 20:02Z continuation with different then-current shas, which the page itself flags"
  ],
  "no_impact_checks": [
    "four panel-tool updates (tools/tally-audit.py, tally-audit-v2.py, tally-audit-v3.py, tools/mte-interop.py changed base→CAND): none is cited in this section — no impact",
    "runner TMPDIR change (r51 honours TMPDIR; mktemp defaults now \"${TMPDIR:-/tmp}/tameshi-r4-2-*.XXXXXX\", runner:148-150,157,160,217,491,1432,1555): no statement in this section made false — its /tmp paths are historical tick observations, not runner defaults",
    "tenth leg: the section's four leg rows (cases 1-4) remain the first four of the ten CAND legs with unchanged pin/rev values; 'four embedded legs' is superseded only as a present-tense description of the harness"
  ],
  "prior_art_cited": [
    ".ufo/waves/round-16/w1/CR20.md:44-103 (section 1164 audit; receipts re-executed at r7-1 cf41efaa: selftest 67/67, regression 4 legs 8/8/6/4, exact closing line)",
    ".ufo/waves/round-27/w1/Read17.md:9-73 (section 1164 audit; six-row table verified against git objects; falsifier arithmetic reproduced by hand)",
    ".ufo/evidence/round-18/final/audit-1164.stdout (round-18 re-read of this section; ledger blob 13a11e46… identical to CAND's)"
  ]
}
```

## Prose findings

1. **The section's load-bearing content verifies at CAND.** The six-row tick table matches ER-4
   (ledger:324-331) cell for cell — same recorded revs, pins, live HEADs, ancestor flags, worktree
   states, readings; the `4 × current · 2 × stale · 0 × drift` summary matches ER-4's headline
   (ledger:333); both drift chains match the ER-4 bullets; the tool sha `cf41efaa…` matches ER-4:320
   and the addendum's 20:02Z re-read (ledger:360). The ledger blob is byte-identical to the one the
   round-18 audit opened (sha `13a11e46…`), so these verdicts carry forward from two prior executed
   verifications (CR20 re-ran the receipts at r7-1; Read17 verified the table against git objects).

2. **One pointer moved; one count superseded.** `tools/mutate-and-run.sh:511-518` no longer resolves
   to the PIN_*/REV_* block at CAND: those lines are run_sweep's mutant-preparation loop; the block
   (now ten legs, after the r51 tenth leg `bash-drift-pins`) sits at 614-633. The anchor was already
   stale at base (block at 605-622, nine legs) and at every revision since r7-1 — a known, twice-
   dispositioned drift (CR20, Read17), now extended by the tenth leg and the TMPDIR comment edits.
   The phrase "the four embedded legs" is tick-scoped history; the six table values remain the
   harness's recorded PIN_*/REV_* values at CAND.

3. **The strongest falsifier — "two records of one tick … agreeing" — is half-true.** The readings
   agree; the provenance fields do not: scratch root t93 (page) vs t91 (ER-4), and REGRESSION_DATE
   19:58:59Z (page, adjacent section) vs 19:58:18Z (ER-4:341), with the page's selftest stamp
   (19:58:49Z) postdating ER-4's regression stamp. Prior rounds dispositioned this as two
   independent runs with an identical PASS outcome and proposed the smallest correction
   ("the same receipt outcome" / "the same result from two runs"); the page text was never amended,
   so at CAND the wording still overstates identity. Reported, not smoothed; not novel.

4. **Minor, prior-known wording defects re-confirmed at CAND:** "committed as `7da4ec50…`" overstates
   byte identity (superseded, not committed-as-was); "six minutes later" is 5 min 15 s; the
   owners-editing attribution drops its [I] label; the 20:03:34Z worktree shas rest on gone scratch.

5. **No impact from the r51 surfaces this section does not cite:** the four updated panel tools
   (tally-audit.py/-v2/-v3, mte-interop.py) are absent from the section; the runner's new TMPDIR
   default contradicts nothing in it.

Seat bounds honored: read-only everywhere except this report; scratch
`/fast/scratch/hyaku/tameshi-r51/T51W2Read09/` (candidate blobs only) deleted before yield; no /tmp
writes; no tools installed; no git/jj mutations.
