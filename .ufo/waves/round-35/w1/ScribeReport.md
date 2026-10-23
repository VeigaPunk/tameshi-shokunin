# ScribeReport — round 35 §4 contract audit
Axes: report-contract conformance and evidence calibration.

## Scope and result

Attacked the round-35 report marker contract against the round-34 report: required-section presence/order, the specified evidence types, and the marker's placeholder/evidence-pointer conditions. This is a text-level contract audit, not an audit of C1/C2 truth or the watchdog implementation. The round-35 frozen contract defines C1 (depth) and C2 (calibration) at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/contract.json:21-59`; neither measurement was run for this assignment.

**Result:** the round-34 report passes the §4 marker rule on the text inspected. It has all six report sections, in order, with evidence pointers; no placeholder token was detected. No round-34 section fails the marker rule today. This does not certify the underlying claims or report admission.

## Ranked findings

### CRITICAL — false claim

None found in this scoped marker audit. The result is supported by the static check below and the exact input hashes; no claim about round-34 work's factual correctness is made.

### BOUND — bounded negative / limit

- **B-1: Could not break the round-34 report's §4 marker presence/pointer conditions.** The required marker sections that are not exempt are `Work performed`, `Landed changes`, `Before → after measurements`, and `SHONEN`; all are present. `Sources & frontier` and `Trend verdicts` are also present, though §4 explicitly excludes both from the marker predicate. The marker check returned PASS (exact command/output below). Pointers are visible in the report at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/tameshi.md:17-67,71-85,90-99,103-124,128-151`.
- **B-2: The negative result is limited to the written §4 rule.** The watchdog/driver was not run, so this report does not claim the driver's actual implementation agrees with §4. No R35 C1 or C2 counting command was run; the frozen predicates and kill rules are at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/contract.json:23-41,44-58`.
- **Setup limitation:** no scratch clone/checkout was attempted because this scribe seat is barred from mutating Git; the audit used the specified read-only prompt/report/contract paths. No git/jj command or install was run. Only this report is created/changed.

### HYGIENE

- **H-1: The round-34 measurement command is not directly paste-runnable as printed.** It includes literal `REV` and `EMPTY_DIR` arguments at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/tameshi.md:89-99`. The after revision and result receipt are separately given at lines 94-99, so this is not a marker-rule failure; it is a reproducibility/copyability weakness in that section.

## Required round-35 report skeleton and evidence contract

The ordering and wording below follow `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-35.md:99-129`.

```markdown
# tameshi — round 35 (attempt 1)

## Work performed
- Open by naming the round's 1–3 declared claims and target axes or capability.
- One bullet per work item; each bullet has an evidence pointer: path:line, command output, or commit hash.

## Landed changes
- Every change is tied to a LOG.md entry and the commit hash carrying it.

## Before → after measurements
- One entry per claim; include the counting command and the commit measured against.

## Sources & frontier
- SOURCES.md rows before → after and counting command; rows added by tier; rows touched old → new; frontier rows advanced.
- If no corpus/: a line beginning `SOURCES: unchanged —` that names why; main-repo exact form is `SOURCES: unchanged — main-repo lanes hold no corpus/`.

## Trend verdicts
- One evidence-backed verdict each for expansion, quality, discernment; allowed values: improved, harmed, unchanged, unprovable-but-better. No scalar.

## SHONEN
- One line per SHONEN.md checklist box: `[x]` only with a named non-author verifier; `[~]` with a resolvable evidence pointer; `[ ]` if untouched.
```

Evidence types by section: **Work performed** requires the opening claim/axis-or-capability declaration plus a pointer on each work-item bullet; **Landed changes** requires a LOG.md entry and carrying commit for every change; **Before → after measurements** requires each claim's counting command and measured commit; **Sources & frontier** requires the registry counts/changes and census command (or the prescribed unchanged line); **Trend verdicts** requires the three named verdicts and evidence, without a scalar; **SHONEN** requires one checklist-box line with the prescribed verifier/pointer/untouched status. The latter two sections are required in the skeleton, but neither is a marker predicate. Sources & frontier is also explicitly not a marker predicate, although its own conformance obligations remain.

## Round-34 section-by-section marker comparison

The current marker text is `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-35.md:121-129`. It fails a report for placeholder/contentless text, a missing required section other than Sources & frontier or Trend verdicts, or no evidence pointers. Applied literally:

| Round-34 section | Evidence observed | Marker result |
|---|---|---|
| `Work performed` (report lines 3-67) | C1 and target are named; work bullets cite commits, paths, receipts, and wave evidence (lines 5-67). | Pass |
| `Landed changes` (lines 69-85) | Change list maps paths to commits and `LOG Round 34` (lines 71-85). | Pass |
| `Before → after measurements` (lines 87-99) | C1 counting command, before/after outcomes, measurement revision and receipt pointer (lines 89-99). `REV`/`EMPTY_DIR` are the H-1 copyability issue, not absence of a pointer. | Pass |
| `Sources & frontier` (lines 101-124) | Census command/outcomes, row addition/touch, frontier and rejection details, mistake/sourced-claim evidence (lines 103-124). | Present; not a marker predicate |
| `Trend verdicts` (lines 126-144) | Expansion, quality, and discernment each have a verdict and supporting evidence (lines 128-144). | Present; not a marker predicate |
| `SHONEN` (lines 146-151) | Four checklist lines use `[~]` and give evidence pointers (lines 148-151). | Pass |

All six headings occur in the required order, and none is placeholder content. Thus **no round-34 section fails the round-35 §4 marker rule**. Extra round-34 headings are outside the §4 required-section list and are not omissions.

## Commands, outcomes, and provenance

1. Input hashing command (exit 0):

   ```sh
   sha256sum /home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-35.md /home/vgpnk/Projects/shokunin/.ufo/reports/round-34/tameshi.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-34.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py
   ```

   Output:

   ```text
   6a7d03c375caefe959f146d6f575b4e37db2bcc59f12c08ef1f3ab547a07a0c2  /home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-35.md
   1129026a1d041768dec234fa606194576872034305c36788464bd82d9c34d3c9  /home/vgpnk/Projects/shokunin/.ufo/reports/round-34/tameshi.md
   914a7d773ab0d45955b93f3b62dd8bfafd84e4395aa1d9418448233c9b167f4b  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/contract.json
   b3756e50837b13144c0787202b2c2d35715967622b6d408c3f67a3a4e8bff857  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-34.md
   da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py
   ```

2. Static section/placeholder/pointer check (exit 0):

   ```sh
   python3 -c 'from pathlib import Path; import re; p=Path("/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/tameshi.md"); text=p.read_text(); headings=list(re.finditer(r"^## (.+)$", text, re.M)); names=[m.group(1) for m in headings]; required=["Work performed","Landed changes","Before → after measurements","SHONEN"]; missing=[name for name in required if name not in names]; placeholder=bool(re.search(r"(?i)\b(?:placeholder|TODO|TBD)\b", text)); pointer=bool(re.search(r"`[^`\n]*(?:/|\.[A-Za-z0-9_-]+|[0-9a-f]{7,40})[^`\n]*`", text)); print("required_present=" + ",".join(name for name in required if name in names)); print("required_missing=" + ",".join(missing)); print("sources_present=" + str("Sources & frontier" in names)); print("trends_present=" + str("Trend verdicts" in names)); print("placeholder_token=" + str(placeholder)); print("evidence_pointer_token=" + str(pointer)); print("marker_rule_static_result=" + ("PASS" if not missing and not placeholder and pointer else "FAIL")); raise SystemExit(0 if not missing and not placeholder and pointer else 1)'
   ```

   Output:

   ```text
   required_present=Work performed,Landed changes,Before → after measurements,SHONEN
   required_missing=
   sources_present=True
   trends_present=True
   placeholder_token=False
   evidence_pointer_token=True
   marker_rule_static_result=PASS
   ```

   This check is a supporting static query, not the driver's marker implementation. The source-file hashes above bind the inspected bytes; report line pointers identify the compared sections. The prompt defines C1/C2 and pins (including tool SHA-256 `da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f`) at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/contract.json:7-19,23-58`; the v3 tool's three fixes are described at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py:11-32`. These were context only, not executed or altered.

## Surfaces and exclusions

- Created: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w1/ScribeReport.md` only.
- Read-only inputs: round-35 prompt, round-34 report, round-35 frozen contract, round-34 lesson, and the pinned v3 tool docstring, at the paths above.
- Out of scope: product changes, claim measurement, runtime/selftest/watchdog execution, Git/jj mutation, installs, fleet/sibling/state edits, and edits to any frozen artifact. No install or update was performed.
