# T53W2Read06 — re-read of `## The operator's runbook and the six-leg regression (round 10, measured)` at C\*\*

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only; git objects only, never the working-tree `SKILL.md`)
- Content revision (C\*\*): `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`
- Section boundary, frozen sectionizer: **start 1287, end 1295**, `section_sha256 = 636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7`
- Verdict: **1 finding** (wave-1 F1 fixed, wave-1 F2's quotation fixed but the replacement introduced a provenance mislabel). Every other statement in the section holds at C\*\*.

## Fix verification (wave-1 findings first)

| # | wave-1 item | check | outcome |
|---|---|---|---|
| V1 | F1 `stale-pointer` — `:1226-1228` cited for the cases-5–6 debt | `git -C $lane show C**:SKILL.md \| sed -n '1287,1295p' \| grep -n '1226\|still not'` | **fixed** — `grep` exit 1, no `:1226-1228` and no `still not …` in the section bytes; the self-pointer is gone rather than re-pointed |
| V2 | F2 `non-verbatim-quote` — `"still not embedded — named debt"` presented as wording | same `grep` (exit 1) plus full-line read of `:1291` | **quotation repaired, provenance not** — the double quotes are gone, so the section no longer claims a verbatim quotation; the replacement parenthetical `(the round-9 receipt's wording; ER-4 caveat (a))` now asserts a *document* as the phrase's source, and that document does not carry the phrase (F1 below) |

The section at C\*\* (lines 1287–1294, line 1295 is the stripped trailing blank):

```
## The operator's runbook and the six-leg regression (round 10, measured)

Round 7 made `--regression` the ledger's replay gate; rounds 8–9 left two
named gaps: the registry ran four legs with cases 5–6 not yet embedded —
named debt (the round-9 receipt's wording; ER-4 caveat (a)), and the operator the arc was built for had no
single entry point. Round 10 closes both — the runbook lands (T10-1, this
round), and the leg cut resolves as an **embedding** of cases 5–6 (T10-2),
never a re-cut.
```

## Checks run

| # | check | command (lane = `/home/vgpnk/Projects/shokunin/tameshi-shokunin`) | outcome |
|---|---|---|---|
| 1 | SKILL.md size at C\*\* | `git -C $lane cat-file -s 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md` | 197 139 B |
| 2 | frozen sectionizer, imported not reimplemented | loaded C\*\*'s `.ufo/evidence/round-18/measure.py` via `importlib`, ran `sectionize(raw)` on the C\*\* blob | 64 sections, one hit: `{'start': 1287, 'end': 1295, 'sha256': '636e850f…'}` |
| 3 | independent recompute | manual split (fence-aware heading scan, trailing whitespace-only lines stripped, `'\n'.join`, no trailing newline, UTF-8 `surrogateescape`) | same digest `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7` |
| 4 | boundary lines | `git -C $lane show C**:SKILL.md \| awk 'NR>=1286 && NR<=1296'` | 1286 is the previous heading's last line, 1287 the heading, 1295 blank, 1296 the next heading `### The operator's runbook — corpus/knowledge/operator-runbook.md`; the split is confirmed before hashing |
| 5 | byte-exactness of the finding quote | `python3 -c "print(q in body, body.count(q))"` on the section bytes | `True 1` |
| 6 | C\*\* vs C\* section delta | sectionized both revisions, `diff -u` | only the two lines that are 1281–1282 at C\* (1290–1291 at C\*\*) differ — quoted `"still not embedded — named debt" (`:1226-1228`)` → unquoted wording plus `(the round-9 receipt's wording; ER-4 caveat (a))`; C\* digest `e52321d2…` |

## Holds (commands and their output)

Quoting convention in this section: inside a quoted source, ` / ` marks a line break and `…` marks elided text; every other character is byte-exact at C\*\*.

- **H1 — "Round 7 made `--regression` the ledger's replay gate".** `git -C $lane show C**:tools/mutate-and-run.sh | sed -n '8,10p'` → `# (TAMESHI-T7-1) turns --regression into the fleet leg ledger — every recorded / # mutation case replayed at its pinned original revision, materialized from its / # repo's git object store (`git show <rev>:<path>`, immune to working-tree drift), with each leg's recorded kill-rate as its expectation`. The round-7 label and the "replay gate" characterisation are the tool's own header words.
- **H2 — "the registry ran four legs with cases 5–6 not yet embedded" (rounds 8–9 state).** `git show C**:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '350p'` → ER-4 caveat (a): `the tool embeds **4** legs — cases 5/6 (checklist-run, claims-check) carry no `REGRESSION` line at `cf41efaa…``; ER-4's own regression receipt line reads `REGRESSION: PASS (cases=4 passed=4 …)`. Four legs is asserted for rounds 8–9 only, and the section is titled `(round 10, measured)`; the current ten-leg state (`tools/mutate-and-run.sh:84` at C\*\*: `--regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten)`) does not falsify a dated statement.
- **H3 — "the runbook lands (T10-1, this round)".** `git show C**:corpus/knowledge/operator-runbook.md | sed -n '1,3p'` → `# Operator runbook — the tameshi mutation service, end to end (round 10, T10-1)` (:1, whole line) / `Written 2026-10-14 by lane T10-1 (tameshi round 10).` (:3, the line's first sentence)
- **H4 — "the leg cut resolves as an **embedding** of cases 5–6 (T10-2), never a re-cut".** `git show C**:tools/mutate-and-run.sh | sed -n '11,15p'` → `r10-2 / (TAMESHI-T10-2) resolves the round-8 leg cut — cases 5/6 (kagi / corpus/checklist-run.sh, kumitate scripts/claims-check.mjs) embedded as / the fifth and sixth legs`; `:114-118` records `legs 5–6 are the recorded T8-1/T8-2 spec files`.
- **H5 — the second "named gap", "the operator the arc was built for had no single entry point".** `plans/round-10-record-draft.md:205` (blob identical at C\*\*) states the round-9 gap as `the operator had no single entry point`, and the runbook's role line closes it (`the mutation / service's single operator-facing document`).
- **H6 — the `ER-4 caveat (a)` label itself.** ER-4 (`fleet-kill-rate-ledger.md:318`) is the round-9 receipt (`this is the policy's first invocation at a round boundary — the receipt`) and its `:350` caveat (a) is the cases-5/6 caveat; the citation resolves to the right caveat, only the wording attribution fails (F1).
- **H7 — no scratch-directive statement in the section.** The section names no scratch path, so the `$HYAKU_SCRATCH` default / `/tmp`-under-50-MB rule has nothing to test here (`grep -n '/tmp\|scratch' <section>` → no match).

## Findings

### F1 — "the round-9 receipt's wording" names a document that does not carry the phrase

Quote (verbatim, byte-exact substring of the section at C\*\*):

```
named debt (the round-9 receipt's wording; ER-4 caveat (a))
```

Class: `misattributed-provenance`. The statement that fails: `named debt` is the round-9 **receipt's** wording, as ER-4 caveat (a) records it.

At C\*\*, the round-9 receipt is ER-4, and ER-4's caveat (a) reads:

```
Two measured caveats, stated not smoothed: (a) the tool embeds **4** legs — cases 5/6 (checklist-run, claims-check) carry no `REGRESSION` line at `cf41efaa…`; the leg-cut decision stands with the tool owner (ER-2's named hand-offs, `:282`), nothing re-cut to manufacture a line; (b) the legs replay recorded pins while live gates 3/4 read `stale` …
```

(`git -C $lane show C**:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '350p'`)

The phrase is absent from the receipt — and from the whole ledger file, at every revision:

```
$ git -C $lane grep -c "named debt" 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e -- corpus/knowledge/fleet-kill-rate-ledger.md
exit=1                     # no output: zero occurrences at C**
$ git -C $lane log --all --oneline -S"named debt" -- corpus/knowledge/fleet-kill-rate-ledger.md | wc -l
0                          # no commit of that file ever added or removed the string
```

The word the receipt does use is `named hand-offs`, inside `ER-2's named hand-offs, `:282``, and `:282` at C\*\* is ER-2's bullet header:

```
- **Named follow-ups (not edits, not written here).** Cases 5/6 are not embedded in `--regression`: T8-2 E3 records the … [truncated here]
```

Counting against the nearest true source (not a claim that no source exists): the phrase is a **round-9 record draft** line, and the draft is a different document from the receipt —

```
$ sed -n '283p;288p' plans/round-9-record-draft.md
  successor row, and cases 5/6 remain unembedded in `--regression` — carried
  re-sweep leg and the embedding of cases 5/6 stay **open, named debt**.
```

(`plans/round-9-record-draft.md` blob `2a8d3836d07e91e27585cd6731394bea0b6c3d4d`, byte-identical to the working tree; header line 1: `# Round-9 record draft — for the parent scribe to finalize (SCR-T9)` — a draft, not the receipt.)

The lane's own machine anchors agree with the draft/ER-2 lineage and not with the parenthetical — `tools/mutate-and-run.sh:24-27` at C\*\* (`git -C $lane show C**:tools/mutate-and-run.sh | sed -n '24,27p'`):

```
# the tool itself)"; r10-2 = the round-8/9 named hand-offs — the leg cut stands
# with the tool owner (fleet-kill-rate-ledger.md ER-2 named follow-ups;
# mutation-case-kagi-checklist.md U5; mutation-case-kumitate-claims.md E3;
# round-9 record draft: "cases 5/6 remain unembedded — named debt") and is
```

and SKILL.md's own attribution for the phrase in the same file is the ledger's ER-2 bullet, not the receipt — `SKILL.md:1235` at C\*\*: `line at this boundary — named debt, not smoothed (`fleet-kill-rate-ledger.md:282`; the debt was retired when the legs embedded).`

Why it matters for a cold reader: the parenthetical is the only provenance offered for the phrase, and following it to ER-4 caveat (a) yields a caveat with different wording (`carry no REGRESSION line`) and zero occurrences of `named debt`; the actual round-9 source (`plans/round-9-record-draft.md:283/:288`) is named nowhere in the section. The wave-1 fix removed the quotation marks but replaced them with a source label that does not resolve — the same defect class (unverifiable provenance) in a new form. The repair is a two-word re-label (`the round-9 record draft's wording`, `plans/round-9-record-draft.md:288`) with ER-4 caveat (a) kept as the *substance* citation; the section's underlying historical claim (rounds 8–9 left the cases-5/6 debt, closed at r10-2 by embedding) is unaffected and holds.

## Notes and limits

- Observation, not a finding of this seat: `SKILL.md:1362-1363` at C\*\* repeats the same label — `the round-9 caveat that cases 5–6 were / "named debt" (the round-9 receipt's cases-5–6 caveat; ER-4 caveat (a))`. That line is in the sibling section owned by another wave-2 seat; recorded here only so the L1 can fix both together.
- Read-only discipline: all section and source bytes came from `git show`/`git grep`/`git cat-file` at C\*\*; `corpus/`, `plans/`, `tools/` and `SKILL.md` were also opened in the working tree only to confirm byte-identity with C\*\* (`git diff --stat C** -- corpus/ tools/` → empty; record-draft sha256 match). No file outside `.ufo/waves/round-53/w2/` was written. No git/jj mutation anywhere; no task dispatch.
- No tools installed or upgraded (nothing was needed). Scratch `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read06/` held only extracted blobs and split scripts and is deleted before this seat yields; nothing was written under `/tmp`.
- Not re-run: the C1 cold-read counter and the deciding-run monitors (out of a re-read seat's scope; the section digest above is the monitor's own sectionizer imported at C\*\*, not a reimplementation).
