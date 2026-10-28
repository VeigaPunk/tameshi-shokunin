# T54W1Read09 — cold read, round 54 wave 1

| field | value |
|---|---|
| heading | `## The operator's runbook and the six-leg regression (round 10, measured)` |
| cand | `59c38109bf119d0e9d4f878644a82babc937bc1e` |
| section_sha256 | `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7` |
| span at cand (round-18 sectionize) | `SKILL.md:1295-1303` (heading line through the last non-blank line, `\n`-joined, no trailing newline) |
| section bytes | 493 B |
| findings | **none** (`findings: []`) |

Reader command (run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, `TMPDIR=$HYAKU_SCRATCH/tameshi-r54/T54W1Read09`):

```
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf119d0e9d4f878644a82babc937bc1e "## The operator's runbook and the six-leg regression (round 10, measured)"
```

Output (verbatim):

```json
{"heading": "## The operator's runbook and the six-leg regression (round 10, measured)", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1295, "end": 1303, "section_sha256": "636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7"}
```

## Section bytes at cand (verbatim)

Copied from `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md` lines 1295-1302; the sha above is the sha256 of this exact text.

```text
## The operator's runbook and the six-leg regression (round 10, measured)

Round 7 made `--regression` the ledger's replay gate; rounds 8–9 left two
named gaps: the registry ran four legs with cases 5–6 not yet embedded —
named debt (the round-9 receipt's wording; ER-4 caveat (a)), and the operator the arc was built for had no
single entry point. Round 10 closes both — the runbook lands (T10-1, this
round), and the leg cut resolves as an **embedding** of cases 5–6 (T10-2),
never a re-cut.
```

## Findings

None. `findings: []`.

The section is eight lines of retrospective narrative with no table. Every claim it makes resolves at `59c38109bf119d0e9d4f878644a82babc937bc1e`; no cited anchor fails; no sentence contradicts another inside the section. I did not manufacture a defect: the claim-level checks follow, and any reader can re-run them.

## Claim-by-claim checks (all inputs are git objects at cand)

Quotations below are single-line byte-exact fragments of the file cited; where a statement continues past the quoted fragment the line cite carries the rest.

1. **"Round 7 made `--regression` the ledger's replay gate"**
   - `plans/round-7.plan.md:30` — "Claim: round 7 makes the method's outputs fleet-facing and replayable." `plans/round-7.plan.md:4` — "Leg ledger: `--regression` replays EVERY recorded case at its pinned" (the sentence continues on `:5`).
   - `SKILL.md:932` — "The leg ledger — replay, receipt, and how it is read (round 7, measured)". `SKILL.md:934-935` — "from the tool's two-case self-check into the" / "fleet's **leg ledger**".
   - `tools/mutate-and-run.sh:8` — "turns --regression into the fleet leg ledger"; `:4-5` records that `--regression` itself predates round 7 ("r4-2 (TAMESHI-R4-2) adds" / "--regression, this tool's own kill-rate regression gate").
   - Resolves.

2. **"rounds 8–9 left two named gaps: the registry ran four legs with cases 5–6 not yet embedded — named debt (the round-9 receipt's wording; ER-4 caveat (a))"**
   - `corpus/knowledge/fleet-kill-rate-ledger.md:350` (ER-4, the round-9 receipt) — "(a) the tool embeds **4** legs — cases 5/6 (checklist-run, claims-check) carry no `REGRESSION` line at `cf41efaa…`"; the same line reads "nothing re-cut to manufacture a line". Caveat (a) exists, is labelled (a), and states both the four-leg count and the cases-5/6 non-embedding.
   - `plans/round-9-record-draft.md:283` — "cases 5/6 remain unembedded in `--regression`"; `:288` — "stay **open, named debt**" ("re-sweep leg and the embedding of cases 5/6 stay **open, named debt**."). So "named debt" is the round-9 record's own wording.
   - `SKILL.md:1242` — "Cases 5–6 were not yet embedded at this boundary"; `:1243` — "named debt, not smoothed".
   - `tools/mutate-and-run.sh:1510` — "local nlegs=10 npass=0 nfail=0 nsetup=0 st" (today's count). The section's "four legs" is past tense ("the registry ran") and the heading dates it `(round 10, measured)`, so it is a dated reading, not a live claim.
   - Resolves.

3. **"and the operator the arc was built for had no single entry point"** (the second gap)
   - `plans/round-10.plan.md:40` — "operator is the one reader left when the lanes stop, and both records end at"; `:49` — "operator's entry point, sibling of `SKILL.md`/`PROVINCE.md`"; `:167` — "The gap is named"; `:169` — "the operator is the seat left".
   - `plans/round-10-record-draft.md:205` — "the operator had no single entry point"; `:210` — "no operator entry point"; `:234` — "the operator's single entry point".
   - The round-10 plan is a round-9-wave artifact (`plans/round-10.plan.md:3` — "Design lane: PREP-T10 (2026-10-14, round-9 32-lane wave"), so the gap the sentence attributes to rounds 8–9 is named within that span.
   - Resolves.

4. **"Round 10 closes both — the runbook lands (T10-1, this round)"**
   - `corpus/knowledge/operator-runbook.md:1` — "Operator runbook — the tameshi mutation service, end to end (round 10, T10-1)"; `:3` — "Written 2026-10-14 by lane T10-1 (tameshi round 10)"; `:7` — "Landed at `corpus/knowledge/operator-runbook.md` per the round-10 dispatch".
   - `plans/round-10-record-draft.md:40` — "**The handoff landed — relocated.**"; `:41` — "`e1e349b6…`, 511 `wc -l` / 31 416 B".
   - `corpus/knowledge/closeout-r11.md:234` — "operator's entry point (`operator-runbook.md`)".
   - Resolves. (The runbook's own §3/§7 still carry four-leg text — `corpus/knowledge/operator-runbook.md:374` — but that is the runbook's recorded staleness, named by AUD-T10 in `plans/round-10-record-draft.md:106` and flagged in the *next* subsection of `SKILL.md`; this section makes no four-leg claim about the runbook.)

5. **"the leg cut resolves as an **embedding** of cases 5–6 (T10-2), never a re-cut"**
   - `tools/mutate-and-run.sh:12` — "resolves the round-8 leg cut — cases 5/6"; `:14` — "the fifth and sixth legs" ("embedded as" closes `:13`); `:28` — "resolved here as an embedding, not a re-cut." Its usage block (`:203-235`) lists all ten legs at cand, `bash-checklist-run` and `js-claims-check` included.
   - `plans/round-10-record-draft.md:78` — "**The round-8 4-vs-6 leg cut resolved — an embedding, not a re-cut"; the sentence continues on `:79` with the task ids.
   - Resolves.

6. **Heading count "six-leg regression" (round 10)**
   - `SKILL.md:1362` — "`--regression` → six legs at r10-2 (ten at CAND0), all exact". The heading dates the count to round 10; the same page carries the ten-leg milestone.
   - Resolves.

## What was checked and found clean

- **In-section contradictions:** none. The quantities are "two named gaps", "four legs" (past), "cases 5–6", "six-leg" (round-10 heading), `T10-1`, `T10-2`; each is consistent with the others and with the artifacts above.
- **Table cells:** the section contains no table, so no cell can be stale.
- **Cited commands/paths:** the only command named is `--regression`, present at cand (usage `tools/mutate-and-run.sh:206`; wiring `:1510`). The evidence ids named (`ER-4 caveat (a)`, `T10-1`, `T10-2`, "the round-9 receipt") resolve at the lines above.
- **Rule anchors:** the narrative names its evidence ids inline (`ER-4 caveat (a)`, `T10-1`, `T10-2`); the two unattributed clauses (round 7, and the entry-point gap) resolve through `plans/round-7.plan.md` and `plans/round-10.plan.md`. I do not report anchor absence as a defect where the anchor resolves through the doc's own round paths — the round-53 re-key credited these same bytes with `blocking_gaps: 0`, `wrong_expectations: 0`.

## Why this heading sits in `lost-headings-at-c0.json` (evidence, not a finding)

Context for the re-key arm; **not** a defect in the section text.

- The section's bytes are unchanged since the last credited read: the section sha at cand is `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7`, and `.ufo/evidence/round-21/coldread/ledger.json` carries the same `sha256` (`636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7`) for this heading with `read_rev = 651773ab9e3295777a087c033e620ea81b9717b6`, `verdict = gap-minor`, `blocking_gaps = 0`, `wrong_expectations = 0`, `minor_gaps = 0`.
- That ledger entry pins these inputs: `SKILL.md`, `corpus/knowledge/closeout-r11.md`, `corpus/knowledge/fleet-kill-rate-ledger.md`, `corpus/knowledge/incremental-pin-disposition.md`, `corpus/knowledge/mutation-case-kagi-checklist.md`, `corpus/knowledge/mutation-case-kumitate-claims.md`, `corpus/knowledge/operator-runbook.md`, `plans/round-10.plan.md`, `plans/round-9.plan.md`, `tools/mutate-and-run.sh`, `tools/registry.json`, `tools/trace-inputs.py`.
- C0 (`59c38109bf119d0e9d4f878644a82babc937bc1e`) edits `tools/registry.json` (C0's `git show --stat` lists that path with a `7 +` change row), one of those pinned inputs. The round-52/53 prechecks already recorded this heading as LOST with `tools/registry.json` among the drifted inputs (`.ufo/evidence/round-52/integrate/precheck-cand0.stdout:4`, `.ufo/evidence/round-53/before/coldread-precheck-at-tip.stdout:4`).
- Conclusion: the C0 loss is **input drift against the ledger entry's pins**, not a content defect in the section. Re-crediting is the re-key arm's job (re-bind at C0 with input hashes re-read at C0).

## Artifacts opened (git objects at cand unless stated)

| artifact | lines read | why |
|---|---|---|
| `SKILL.md` | 1295-1303 (section), 918-1000 (round-7 section), 1155-1294 (round-9 section), 1340-1400 (round-10 receipts/notes), 1362 | section bytes; the round-7/9/10 claims the section restates |
| `tools/mutate-and-run.sh` | 1-30 (header), 200-235 (usage), grep `TAMESHI-T10-2`/`nlegs`/`--regression` | r7-1 leg-ledger provenance, r10-2 embedding, current leg count |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | 270-300 (ER-2), 316-368 (ER-4 + addendum) | ER-4 caveat (a), four legs, cases 5/6 |
| `corpus/knowledge/operator-runbook.md` | 1-10, 160-200, 340-400 | T10-1 landing, the runbook's own four-leg status (outside this section) |
| `plans/round-7.plan.md` | grep `leg ledger`/`Claim: round 7` | round-7 replay-gate claim |
| `plans/round-9.plan.md` | 1-60 | round-9 frame, four legs, "not embedded" row rule |
| `plans/round-9-record-draft.md` | 270-300, 395-425 | "named debt" wording, carried debt |
| `plans/round-10.plan.md` | 1-200 | operator entry-point gap, T10-1/T10-2 framing |
| `plans/round-10-record-draft.md` | 40-45, 78-82, 100-110, 160-260 | T10-1 landing, T10-2 embedding, state rows |
| `corpus/knowledge/closeout-r11.md` | 228-240 | operator's entry point handed across |
| `tools/registry.json` | 1-30 | checked "the registry" against the entry registry (7 rows with `scratch_root` cells — not legs) |
| `.ufo/evidence/round-21/coldread/ledger.json` | this heading's entries | prior credit, sha/input pins, rekey trace path |
| `.ufo/evidence/round-21/coldread/rekey-r53-651773ab9e32/traces/section-09.json` | whole | prior read's pinned input set and read_rev |
| `.ufo/evidence/round-54/c1/lost-headings-at-base.json`, `lost-headings-at-c0.json` | whole | confirms this heading is in the C0 re-read set |
| `.ufo/evidence/round-52/integrate/precheck-cand0.stdout`, `.ufo/evidence/round-53/before/coldread-precheck-at-tip.stdout` | lines 4, 14 | prior LOST lines with drifted input lists |
| `.ufo/waves/round-54/w1/swarm-registry.json` | this member entry | seat scope/reportDir |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | whole run | conformance |

## Commands executed

```
python3 .ufo/waves/round-54/reader-section.py <lane> <cand> "<heading>"        # span + sha
git -C <lane> show <cand>:SKILL.md | sed -n '1295,1302p'                       # section bytes
python3 -c '<sha256 of the sectionize body>'                                   # sha reproduction
git -C <lane> show <cand>:SKILL.md | grep -n 'T10-1\|T10-2\|ER-4\|round-9\|round 10\|round-10'
git -C <lane> show <cand>:SKILL.md | grep -n 'named debt, not smoothed\|six legs at r10-2'
git -C <lane> show <cand>:SKILL.md | sed -n '918,1000p;1155,1295p;1355,1400p'
git -C <lane> show <cand>:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '270,300p;316,368p'
git -C <lane> show <cand>:corpus/knowledge/operator-runbook.md | sed -n '1,10p;160,200p;340,400p'
git -C <lane> show <cand>:tools/mutate-and-run.sh | sed -n '1,30p;200,235p'
git -C <lane> show <cand>:tools/mutate-and-run.sh | grep -n 'TAMESHI-T10-2\|local nlegs=\|--regression'
git -C <lane> show <cand>:plans/round-7.plan.md | grep -n 'leg ledger\|Claim: round 7'
git -C <lane> show <cand>:plans/round-9.plan.md | sed -n '1,60p'
git -C <lane> show <cand>:plans/round-9-record-draft.md | sed -n '270,300p;395,425p'
git -C <lane> show <cand>:plans/round-10.plan.md | sed -n '1,200p'
git -C <lane> show <cand>:plans/round-10-record-draft.md | sed -n '40,45p;78,82p;160,260p'
git -C <lane> show <cand>:corpus/knowledge/closeout-r11.md | sed -n '228,240p'
git -C <lane> show <cand>:tools/registry.json | head -30
git -C <lane> show <cand> --stat
git -C <lane> grep -n 'T10-1' <cand> -- .
git -C <lane> grep -n 'T10-2' <cand> -- .
git -C <lane> grep -n 'named debt' <cand> -- .
git -C <lane> grep -n -i 'single entry\|entry point' <cand> -- LOG.md plans/ corpus/
python3 -c '<ledger.json entry lookup for this heading>'
python3 -c '<rekey-r53 trace read>'
python3 -c '<sha256 verification of the embedded section text>'
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi   # exit 0
```

Read-only throughout: no mutating git/jj command, no lane file edited, no fixture created (this seat writes only the two deliverables).

## Scratch and conformance

- Scratch root `$HYAKU_SCRATCH/tameshi-r54/T54W1Read09` was the `TMPDIR` for the reader helper's mkdtemp; it is removed at exit. Nothing was written under `/tmp`.
- No tool install or upgrade was needed, so nothing is recorded there.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → "tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md", exit **0**.
