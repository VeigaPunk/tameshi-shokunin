# E04R19Workflow — round-19 lesson §Workflow mistake — late in-place edits

Godspeed axes: (1) evidence fidelity — exact line-anchored quotes, no paraphrase drift; (2) scope discipline — report only the four asked items, no judgment of the claim; (3) reproducibility — every finding re-derivable from the recorded commands/outputs; (4) speed — parallel anchor-locate then targeted reads, no whole-file reads.

## Findings (all from `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-19.md`; read-only, no lane files modified)

### 1. Disclosed edit interval (lines 291–295, verbatim)

> "L1 first edited the live ruler for wave2 findings after all three
> authorized execution probes had returned, but while other read-only
> wave2 seats were still active. That still violates QUALITY20's
> no-in-place-edit rule; it is a conformance defect."

Interval: **after all three authorized execution probes had returned, but while other read-only wave2 seats were still active.** The lesson itself labels it a QUALITY20 no-in-place-edit conformance defect (disclosure text, not my judgment).

### 2. Frozen SHA restored (lines 295–296, verbatim)

> "The live instrument was restored to the exact frozen55e1 SHA
> `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`"

Restored SHA-256: **`bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`** — the "frozen55e1" live ruler.

Name disambiguation from the round-20 erratum in the same file (lines 361–362, verbatim):

> "The separate wave-2 frozen ruler at `55e1d312c4e8ac67aefad80099bd27581ff805c9`
> is `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`."

So "frozen55e1" is the ruler identified by **`55e1d312c4e8ac67aefad80099bd27581ff805c9`** whose bytes hash to `bb651eef…ff5053`. The erratum further supersedes line 299's singular "the frozen SHA": the three executor probes recorded **distinct** instruments (`96a68b60…` round-19 wave-1 ruler; `8dfaa25a…` witness tool; `d22c4025…` witness runner; `7ca87a7c…` round-18 measure — lines 353–360 table), and "No claim is made that all three probes pinned that ruler" (line 363).

### 3. What was staged separately (lines 297–298, verbatim)

> "late repairs were moved to a separate `/tmp/tameshi-r19-late-stage-*`
> file and will be installed only after the wave's readers finish."

Staged separately: **late repairs in `/tmp/tameshi-r19-late-stage-*`**, install deferred until the wave's readers finish. Lines 299–300 add: "The three actual execution probes pin the frozen SHA; no mixed execution receipt was observed." Later observed outcome (line 341): "Late staging was installed at329b6dd and the temporary stage removed."

### 4. Residual code-reading race (lines 300–302, verbatim)

> "Code-reading race risk is not erased.
> Final measurements apply one installed final ruler to both endpoints;
> the wave is not claimed to have reviewed those later bytes wholesale."

Residual race: **not erased**. Final measurements apply one installed final ruler to both endpoints, and the wave does **not** claim wholesale review of those later bytes. Cross-reference the lesson cites (lines 363–365, not judged here): "The outside round-19 review §QUALITY20 records why the final same-ruler measurements remain valid despite the disclosed code-reading race."

## Commands and observed outputs

- `grep -n` (via grep tool), pattern `Workflow mistake|late in-place|in-place edit` on `corpus/lessons/round-19.md` → section header at line **289**.
- `read corpus/lessons/round-19.md:285-345` → §Workflow mistake body lines 291–302; next section `## Captured-by erratum — FMistakesDraft` at line 304.
- `grep -n`, pattern `late in-place edits|bb651eef|tameshi-r19-late-stage|Code-reading race|Captured-by erratum|wholesale|installed at` → anchors at 289, 296, 297, 300, 302, 304, 341, 361–362.
- `read corpus/lessons/round-19.md:352-368` → `## Round-20 erratum — distinct instrument identities and date bases (2026-10-21)`, instrument-SHA table (lines ~353–360), 55e1↔bb651eef mapping (361–362), QUALITY20 cross-reference (363–365), S049 date-basis note (366–368).

No tools installed or updated (none needed); no code executed; no lane production file touched.

## Agree/disagree

- Agree (observed, textual): the section is self-consistent — edit interval, restored SHA, staging path, and residual-race disclosure appear verbatim at lines 291–302; the round-20 erratum at 352–365 resolves the "frozen55e1" label to the `55e1d312…`/`bb651eef…` instrument pair and narrows the three probes to distinct instruments.
- Note: line 299's singular "the frozen SHA" is superseded wording per the erratum ("Supersedes only line 299's …", line 352); current reading is the four-distinct-instrument table above. Reported as disclosure content, not adjudicated.

## Defects

None observed within scope: the asked four items are all disclosed in the lesson; no contradiction between §Workflow mistake and the round-20 erratum was found. Unresolved by design of this seat: whether the outside round-19 review §QUALITY20 argument is sound (explicitly not judged here).
