# T53W1Read09 — cold-read of `## The operator's runbook and the six-leg regression (round 10, measured)`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Content revision (C\*): `a41195dfc13a73958e4c5228ec196b28d03ded03`
- Method: every byte read via git objects (`git -C <lane> show C*:SKILL.md`); the lane working
  tree was never read for section content.
- Section under test reproduces the frozen monitor boundary: **start 1278, end 1286** (exclusive;
  bytes are lines 1278–1285, 8 lines), `section_sha256 = e52321d2152b65c88894a72fd91b594dc7aabfb1c5bea9ed283cbdd81ec1664d`.
- Verdict: 2 findings (1 stale pointer, 1 non-verbatim quotation). All other statements in the
  section hold at C\*.

## Checks run

| # | check | command (lane = `/home/vgpnk/Projects/shokunin/tameshi-shokunin`) | outcome |
|---|---|---|---|
| 1 | SKILL.md size at C\* | `git -C $lane show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md \| wc -l` | 2178 lines |
| 2 | section split, frozen sectionizer | extracted `a41195dfc13a73958e4c5228ec196b28d03ded03:.ufo/evidence/round-18/measure.py` (its `sectionize()`, blob lines 209–253) and ran it on the C\* SKILL.md bytes | one section matching the heading: `{"start": 1278, "end": 1286, "sha256": "e52321d2152b65c88894a72fd91b594dc7aabfb1c5bea9ed283cbdd81ec1664d"}` |
| 3 | independent recompute | `lines[1277:1285]` of `raw.split('\n')` (terminal empty line dropped), trailing whitespace-only lines stripped, `'\n'.join`, sha256 over UTF-8 `surrogateescape`, no trailing newline | same digest `e52321d2152b65c88894a72fd91b594dc7aabfb1c5bea9ed283cbdd81ec1664d` — the frozen split is reproduced |
| 4 | heading-line provenance | `git -C $lane show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md \| sed -n '1278p'` | `## The operator's runbook and the six-leg regression (round 10, measured)` |

The heading's line range was reproduced before hashing (checks 2 and 3 agree on 1278–1285 and on
the digest), so the hash is over the section bytes the monitor would hash.

## Holds (pointers verified against C\* bytes)

- **H1 — "Round 7 made `--regression` the ledger's replay gate".** C\* `SKILL.md:921-927`: the
  round-7 section is `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`
  and :923–925 read `Round 7 turns --regression from the tool's two-case self-check into the /
  fleet's **leg ledger**: every recorded mutation case is a leg of this ledger, / replayed at its
  pinned original revision.` The section's paraphrase is faithful.
- **H2 — "the registry ran four legs" (rounds 8–9 state, dated).** C\* `SKILL.md:1221`:
  `- --regression → 4 legs, each match=10/10 … flips=0 (killed 8/8/6/4),`. Four legs is the
  recorded r7-1/round-9 boundary, and the sentence is dated to rounds 8–9, not offered as the
  current count (the current tool replays ten legs, `tools/mutate-and-run.sh:88-97` at C\*).
- **H3 — "the runbook lands (T10-1, this round)".** `git -C $lane ls-tree -l a41195dfc13a73958e4c5228ec196b28d03ded03 --
  corpus/knowledge/operator-runbook.md` → `100644 blob 54c72164fa76f0a00f3b0bf1a2af6a87518a326b
  33515 corpus/knowledge/operator-runbook.md`; the runbook is a blob at C\*.
- **H4 — "the leg cut resolves as an embedding of cases 5–6 (T10-2), never a re-cut".**
  C\* `tools/mutate-and-run.sh:116-118` records `legs 5–6 are the recorded T8-1/T8-2 spec files,
  their 25 @old strings re-verified count==1 against the pinned blobs at r10-2`, and the leg list
  at :88-97 holds ten legs (5–10 each an embedded pre-registered/recorded spec, not a re-cut of
  cases 1–4).
- **H5 — the second of the "two named gaps", "the operator the arc was built for had no single
  entry point".** Anchored at C\*, not asserted bare: `plans/round-10.plan.md:38-44` names the
  operator as "the one reader left when the lanes stop" and cites the ledger's U9
  (`fleet-kill-rate-ledger.md:235-237` at C\*: "who runs the update is the dispatcher's call, not
  fixed here") and the opt-in protocol's U3 (`service-optin-protocol.md:264-266` at C\*: "the
  dispatch hand-off … is unmeasured"); the runbook section restates the aim at :1292 ("the loop
  runnable without oral context"). The gap is a round-8/9 record unknown closed by round 10, dated
  to round 10 — it holds.

## Findings

### F1 — stale self-pointer `:1226-1228`

Quote (verbatim, spans a newline):

```
"still not embedded —
named debt" (`:1226-1228`)
```

Class: `stale-pointer`. The statement that fails: the rounds 8–9 gap is evidenced at
`SKILL.md:1226-1228`, i.e. the cited statement lies inside that range.

At C\*, `git -C $lane show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md | sed -n '1226,1228p'` is exactly:

```
The legs replay their pinned blobs — git-materialized
(`tools/mutate-and-run.sh:1222-1303`), so the two `stale` substrates cannot move
them; re-verified at this boundary, since all four legs matched while cases 3–4
```

That range holds the git-materialization sentence and ends mid-clause (`while cases 3–4`); the
round-9 debt sentence it is cited for begins at :1229:

```
read `stale`. Cases 5–6 were not yet embedded at this boundary (they became legs 5–6 at r10-2; the current tool carries them at `tools/mutate-and-run.sh:88-97`): their rows carried no `REGRESSION`
line at this boundary — named debt, not smoothed (`fleet-kill-rate-ledger.md:282`; the debt was retired when the legs embedded).
```

So the pointer stops three lines short of its own subject, and the quoted debt phrase is not in
the pointed range at all.

Provenance of the drift (read for provenance only, `git show <rev>:SKILL.md`):
- floor `ef19d8e1…`: the debt statement sits at :1228 — `Cases 5–6 are still not embedded: their
  rows carry no REGRESSION / line — named debt, not smoothed` — inside `:1226-1228`.
- base `6db1d220…`: the same sentence, reworded, at :1227–1228 — `Cases 5–6 were still not
  embedded at this boundary (both are legs 5–6 since round 10-2 — tools/mutate-and-run.sh:92-93)
  …` — still inside `:1226-1228`.
- C\*: rewording plus insertion moved it to :1229–1230 (`were not yet embedded at this boundary
  (they became legs 5–6 at r10-2; the current tool carries them at tools/mutate-and-run.sh:88-97)`),
  leaving the pointer behind.

### F2 — the quoted wording does not exist at C\*

Quote (verbatim, spans a newline):

```
"still not embedded —
named debt"
```

Class: `non-verbatim-quote`. The statement that fails: the round-9 registry named cases 5–6
verbatim as "still not embedded — named debt".

At C\* that wording occurs in SKILL.md only at :1281 and :1354 — both are this quotation and its
repetition in the later six-leg section, never a source statement:

```
$ git -C $lane grep -n -F "still not embedded" a41195dfc13a73958e4c5228ec196b28d03ded03 -- SKILL.md
a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md:1281:named gaps: the registry ran four legs with cases 5–6 "still not embedded —
a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md:1354:  "still not embedded — named debt" (`:1226-1228`; ER-4 caveat (a)) is resolved
```

The sentence the pointer should reach reads `were not yet embedded` at C\*, not `still not embedded`:

```
$ git -C $lane grep -n -F "not yet embedded" a41195dfc13a73958e4c5228ec196b28d03ded03 -- SKILL.md
a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md:1229:read `stale`. Cases 5–6 were not yet embedded at this boundary (…)
```

The quotation is therefore authorial paraphrase presented in double quotes: it cannot be checked
against any line at C\*, which is exactly what a cold reader cannot do. (The rewording is the same
base→C\* edit that produced F1; the intro quotation was not carried along with it.)

## Deliverables

- `.ufo/waves/round-53/w1/T53W1Read09.json` — heading, `cand`, `section_sha256`, 2 findings
  (each `quote` verified as a byte-exact substring of the section bytes before writing).
- `.ufo/waves/round-53/w1/T53W1Read09.md` — this report.

## Limits / notes

- Only git objects at the frozen revisions were read; no working-tree SKILL.md read, no build, no
  counter run (no rerun of the C1 monitor — the section sha is the monitor's own sectionizer,
  extracted at C\* and imported, not reimplemented).
- No tools installed or upgraded. No git/jj mutation, no commit, no push. Scratch under
  `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read09/` was used only for the extracted blobs and was
  removed before yielding; no `/tmp` writes.
- Findings are limited to the section's own 8 lines; the neighbouring sections' pointers (e.g.
  :1354 repeating the same stale `:1226-1228` and the same quotation) are out of this seat's scope
  and were not scored.
