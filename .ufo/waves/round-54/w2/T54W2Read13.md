# T54W2Read13 — cold read at C1

- Heading: `## Pin disposition and provenance correction — round 13`
- Candidate: `99c3bc88d704566197783f66b211ee0a830e0330` (C1, round-54 fix pass)
- Section span: SKILL.md lines 1542–1572 at C1; effective body 1542–1571 (trailing blank stripped by the frozen round-18 `sectionize`)
- `section_sha256`: `1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31` (printed by `reader-section.py`; independently recomputed over the raw blob bytes with the round-18 `sectionize` and matched)
- Findings: **none** (empty `findings` list; section is clean at C1)

## Result

I cold-read the 30-line section as an executor with no oral context and could not
defend a single defect. Every rule/condition names an anchor that resolves at C1,
every table cell agrees with the artifact it cites, the two documented recipe
commands run as written, and no sentence contradicts another in the section. No
run-together token, missing space, or duplicate parenthetical was found.

## What the section asserts, and what I verified

| Claim in the section | Verification at C1 |
|---|---|
| `tools/pin-disposition.py:67-71` (unchanged semantics; pin must verify) | Lines 67–71 are exactly the "Content status semantics" paragraph: "`unchanged` requires a readable regular worktree file, / verified pinned evidence (the manifest digest equals the blob at the recorded / commit), and byte equality with expected_sha256…" |
| `tools/pin-disposition.py:563-567` | Lines 563–567 are exactly `elif pinned["status"] != "verified":` with the comment "A readable file cannot be called unchanged against unverified evidence." and `content_status="unavailable"`, `worktree["status"]="unavailable"`, `worktree["reason"]="pin_not_verified"` — it enforces the second conjunct of the row-1 condition. |
| Row 2 `changed` / row 3 `unavailable` arms | Lines 568–573: `worktree["sha256"] == expected` → `unchanged`, else `changed`; 561–567 → `unavailable`. Matches the table. |
| "All three content identities agree → Keep `result_reuse=not_established`" | Three identities are named in the cited `corpus/knowledge/incremental-pin-disposition.md:117`: "recorded pin = live file = HEAD blob, tree clean". The tool's `RESULT_REUSE = "not_established"` (line 118) and `USAGE` ("Every row carries result_reuse=not_established") match. |
| "Frozen summary kind is null but the frozen declaration's top-level kind is explicit" | `.ufo/evidence/round-12/BashWitness/summary.json` has `"kind": null` at `declaration.kind`; `declaration.json` line 6 carries the explicit top-level `"kind": "declared-witness mapping (not a blind preregistration)"`. |
| Sources S003, S047, S041 | `corpus/SOURCES.md` at C1: row 14 = S003 (StrykerJS incremental), row 50 = S041 (PIT docs, retained), row 56 = S047 ("precision correction … supersedes S041"). The "(historical S041 retained)" parenthetical is true. |
| "outside routed `corpus/lessons/round-12-verifier-spotcheck.md`, Routed defects item 3" | The file exists at C1; `## Routed defects and residuals` items 1–4 include item 3 ("Tameshi next round: replace brittle host-addendum line citations … Disclose/repair the already named nested `declaration.kind=null` metadata defect …"). |
| "runtime receipts in `.ufo/evidence/round-13/`" | The directory exists at C1 with `pin-manifest.json`, `witness-metadata.json`, `pin-dispositions.json`, `verification*.json`, etc. |
| Step 2 command | Ran verbatim from the lane root: exit 0, one JSON document on stdout with `status: "ok"`, `result_reuse: "not_established"`, `not_compared` present, per-leg `pinned`/`head` (branch + commit = the "sibling branch-tip commits")/`worktree`/`content_status`. It executes git only; normal mode has no sibling-gate invocation. |
| Step 3 command | Ran verbatim: exit 0, `WITNESS_METADATA: metadata_consistent reason=ok exit=0 … inputs=summary,declaration,declared,rerun_summary`. `--companion` exists in the parser; default `--lane-root` is the lane root. |
| Step 4 "summary and rerun summary retain their historical null fields" | `summary.json#/declaration/kind` and `rerun-20261020T035435Z/summary.json#/declaration/kind` are both `null` at C1. |
| Step 4 "companion normalizes the canonical summary only; the rerun null is explicitly outside its normalized scope" | Companion `scope.covered_null_observations` lists only `summary.json` (`field: declaration.kind`); `scope.uncovered_null_observations` lists the rerun summary with `disposition: named-residual-uncorrected`. |
| Step 4 "the producer's wrong-nesting bug is fixed separately … its regression selftest asserts the exact top-level exposed kind" | `tools/bash-witness-study.py` writes the declaration with a top-level `"kind"` (line 904) and `build_summary` mirrors `declaration.get("kind")` at `summary.json#/declaration/kind` (lines 813–817). Selftest lines 1699–1701: `check("summary preserves top-level exposed declaration kind", qsummary["declaration"]["kind"] == "declared-witness mapping (not a blind preregistration)")`. |
| Step 5 (no sibling-gate rerun for closure evidence) | Consistent with the section's own step 2 ("It executes no sibling gate") and with `corpus/lessons/round-12-verifier-spotcheck.md` item 2 ("does not execute a sibling gate"). |
| Companion digests claimed by `.ufo/evidence/round-13/witness-metadata.json` | Recomputed the blobs at C1: summary `acc01268…`, declaration `e8d2024a…`, declared `0def0d3b…`, rerun summary `6726421f…` — all four match the companion's recorded values (no stale pin). |

## Artifacts opened

- `.ufo/waves/round-54/reader-section.py` (hash method inspected: reads the frozen round-18 `measure.py` `sectionize` and hashes the raw git blob section)
- `.ufo/evidence/round-18/measure.py` (copied out of the C1 blob; `sectionize` semantics: heading line through line before next heading, trailing blank lines stripped, no trailing newline)
- `SKILL.md` at `99c3bc88d704566197783f66b211ee0a830e0330`, lines 1535–1580 (section 1542–1572 in context)
- `tools/pin-disposition.py` at C1 (docstring 60–80, usage 148–165, constants 118–125, `git_run` 244–260, decision branch 555–580, selftest harness 780–812 / 940–960)
- `tools/witness-metadata.py` at C1 (usage 30–55, constants 63–70, parser 1220–1246, main 1249+)
- `tools/bash-witness-study.py` at C1 (declaration build 899–904, `build_summary` declaration mirror 813–819, selftest kind assertion 1688–1701)
- `corpus/knowledge/incremental-pin-disposition.md` at C1 (source line 1, source-correction line 5, identity vocabulary line 117, reuse inference lines 123–136)
- `corpus/SOURCES.md` at C1 (rows S003/S041/S047/S048; 139 rows counted)
- `corpus/lessons/round-12-verifier-spotcheck.md` at C1 (lines 138–150, `## Routed defects and residuals` items 1–4)
- `.ufo/evidence/round-13/pin-manifest.json` (schema, `derived_from`, source, 6 legs)
- `.ufo/evidence/round-13/witness-metadata.json` (expected, `frozen_declaration`, `producer`, `historical_runner`, `scope`, `declaration`, `original_nested`, `frozen_bytes_rewritten: false`)
- `.ufo/evidence/round-12/BashWitness/summary.json`, `declaration.json`, `declared.tsv`, `rerun-20261020T035435Z/summary.json`
- C0→C1 diff (`59c38109bf11..99c3bc88`) for `SKILL.md` (the only change in this section is the row-1 condition plus the `:67-71` / `:563-567` anchors; the fix commit did not touch `tools/pin-disposition.py`) and the diffstat for the whole fix pass

## Commands run

All from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless noted; scratch
`TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read13`.

```
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 99c3bc88d704566197783f66b211ee0a830e0330 "## Pin disposition and provenance correction — round 13"
# -> {"heading": "...", "cand": "99c3bc88...", "start": 1542, "end": 1572, "section_sha256": "1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31"}

git show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '1535,1580p' | cat -n
git show 99c3bc88d704566197783f66b211ee0a830e0330:.ufo/evidence/round-18/measure.py > r18.py   # then re-ran sectionize over the C1 blob
# -> start 1542 end 1572 sha256 1fa3130b... (matches reader-section.py; trailing blank lines stripped, 30 body lines)

git show 99c3bc88d704566197783f66b211ee0a830e0330:tools/pin-disposition.py | grep -n "" | sed -n '63,73p;559,570p'
git show 99c3bc88d704566197783f66b211ee0a830e0330:tools/witness-metadata.py | sed -n '30,55p'
git show 99c3bc88d704566197783f66b211ee0a830e0330:tools/witness-metadata.py | sed -n '1220,1262p'
git show 99c3bc88d704566197783f66b211ee0a830e0330:tools/bash-witness-study.py | grep -n "" | sed -n '1688,1715p'

git show 99c3bc88d704566197783f66b211ee0a830e0330:corpus/SOURCES.md | grep -nE "^\\| S0(03|41|47|48) "
git show 99c3bc88d704566197783f66b211ee0a830e0330:corpus/knowledge/incremental-pin-disposition.md | grep -n "recorded pin = live file"
git show 99c3bc88d704566197783f66b211ee0a830e0330:corpus/lessons/round-12-verifier-spotcheck.md | sed -n '138,152p'

# documented recipe commands, run as written
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin
# -> exit=0; status ok; result_reuse not_established; not_compared has 8 entries; 6 legs; head{ branch, commit } present per leg
python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json
# -> exit=0; WITNESS_METADATA: metadata_consistent reason=ok ... inputs=summary,declaration,declared,rerun_summary

# frozen digests vs companion claims
for f in summary.json declaration.json declared.tsv rerun-20261020T035435Z/summary.json; do
  git show 99c3bc88...:.ufo/evidence/round-12/BashWitness/$f | sha256sum
done
# -> acc01268… / e8d2024a… / 0def0d3b… / 6726421f… : all match witness-metadata.json

# style sweep over the section text (QUALITY 104)
grep -n "  " section.txt            # only recipe continuation indents; no inline double spaces
grep -nP "\t" section.txt           # none
# python checks: odd backticks 0, paren imbalance 0, doubled words 0, `` occurrences 0
```

## Limits of this read

- I read the section against C1 bytes only; I did not consult any wave-1 verdict,
  reader JSON, or adjudication note.
- I did not execute a full mutation sweep or any sibling gate; the two documented
  recipe commands are read-only and were run to check the recipe, not to obtain
  closure evidence.
- No tool was installed or upgraded for this seat.
- No lane file outside `.ufo/waves/round-54/w2/` was written; scratch lives under
  `/fast/scratch/hyaku/tameshi-r54/T54W2Read13`.
