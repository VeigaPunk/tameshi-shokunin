seat: RevJudge04

C1 falsify re-judge of wave-1 ledger entries for rows S073, S074, S152. Inputs read at commit
ad5942c6e9858af19d00000b58439b321ddfa62b (lane HEAD 1f9266a is that commit's tree plus w1 reports).
Scratch: /tmp/tameshi-r45-RevJudge04/. No tools installed (python3/curl/gunzip/sha256sum already
present; pacman transactions paused host-wide, nothing needed).

Verdicts
--------
S073 agree — reviewer RevJudge04 — sha equal across live/ledger/snapshot (fd147b22…); the 22-token quote sits once in the PYTHONPYCACHEPREFIX entry body (§1.2 Environment variables, the row's anchor #envvar-PYTHONPYCACHEPREFIX) and states the mirror-tree .pyc redirect with "Added in version 3.8", which is exactly S073's teaches.
S074 agree — reviewer RevJudge04 — sha equal across live/ledger/snapshot (96154519…); the 18-token quote is the §NOTES exit-status sentence the anchor names (status 1 = not a symbolic ref, 128 = another error), the OPTIONS -q detached-HEAD line is also present in the same page, and together they ground the teaches' "branch on exit 1 rather than treat it as a failed read".
S152 agree — reviewer RevJudge04 — sha equal across live/ledger/snapshot (65f9603f…, matching the row anchor's sha256 prefix); the 13-token quote sits once in the thesis abstract (after the Abstract marker, abstract prose on either side) and states the fragility/lack-of-context → false-positives claim that the row's teaches asserts.

sha256 comparison (live fetched 2026-10-25, `curl -fsSL -A 'Mozilla/5.0' --max-time 90`)
---------------------------------------------------------------------------------------
S073  live fd147b22f36d8162649d7cb3ace6f3acf93a05e1bceb07c305d6962e8d3be9f6
      ledger fd147b22f36d8162649d7cb3ace6f3acf93a05e1bceb07c305d6962e8d3be9f6
      gunzip .ufo/evidence/round-45/freshness/sources/S073.raw.gz fd147b22f36d8162649d7cb3ace6f3acf93a05e1bceb07c305d6962e8d3be9f6   → EQUAL
S074  live 9615451998adf20b6a81c3a87969f460985c26b73d40e777c245f673c6c03b42
      ledger 9615451998adf20b6a81c3a87969f460985c26b73d40e777c245f673c6c03b42
      gunzip .ufo/evidence/round-45/freshness/sources/S074.raw.gz 9615451998adf20b6a81c3a87969f460985c26b73d40e777c245f673c6c03b42   → EQUAL
S152  live 65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703
      ledger 65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703
      gunzip .ufo/evidence/round-45/freshness/sources/S152.raw.gz 65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703   → EQUAL

Ledger `opened` is 2026-10-25 for all three (on/after the required date); byte equality with today's
live fetch corroborates. Ledger `author` fields (ExecRows13/ExecRows14/ExecRows22) match the w1
reports in .ufo/waves/round-45/w1/, each of which names its row and records `holds`. I am not any of
those authors.

Located context (measure.py --extract of the committed snapshot; quotes occur exactly once each)
-----------------------------------------------------------------------------------------------
S073 (22 tokens; body content, entry section — not title/nav/footer):
  BEFORE: "…to write .pyc files on the import of source modules. This is equivalent to specifying the -B option. PYTHONPYCACHEPREFIX ¶ If this is set, "
  QUOTE : "Python will write .pyc files in a mirror directory tree at this path, instead of in __pycache__ directories within the source tree."
  AFTER : " This is equivalent to specifying the -X pycache_prefix=PATH option. Added in version 3.8. PYTHONHASHSEED ¶ …"
  Overlap with teaches ≥ 2 content words (write, .pyc, mirror, tree, path, __pycache__, source tree); not copied verbatim from the row's cells.

S074 (18 tokens; body content, end of the §NOTES paragraph, immediately before SEE ALSO):
  BEFORE: "…are used by default. git symbolic-ref will exit with status 0 if the contents of the symbolic ref were printed correctly, "
  QUOTE : "with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs."
  AFTER : " SEE ALSO git-update-ref[1] GIT Part of the git[1] suite …"
  Same extract also carries the anchor's OPTIONS line: "-q --quiet Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently." Overlap ≥ 2 content words (status, symbolic, ref, error); not verbatim from the row's cells.

S152 (13 tokens; body content, thesis abstract):
  BEFORE: "…predominantly using the Jest testing framework. However, "   [Abstract block: title head of the extract reads "…Victor Pezzi Gazzinelli Cruz Understanding Snapshot Testing in Practice…"; "Abstract" marker precedes the quote]
  QUOTE : "drawbacks such as fragility and lack of context can lead to false positives"
  AFTER : ", making it challenging for developers to interpret test failures. To mitigate these issues, best practices like treating snapshot results …"
  Overlap ≥ 2 content words (fragility, lack, context, lead, false, positives); teaches wording ("the thesis says fragility and lack of context can lead to false positives") differs from the quote (prefix "drawbacks such as"), so the quote is located afresh, not copied from the cell.

Checks performed per row: registry row read at the frozen registry (corpus/SOURCES.md lines 82/83/122);
provenance via live sha256 vs ledger raw_sha256 vs gunzip(snapshot) sha256; quote located with
`python3 .ufo/evidence/round-45/freshness/measure.py --extract` on the committed snapshot (counter run
in --extract mode only, as authorized); token counts 22/18/13 all within 6–25; section and
teaches-support judged from the located context above. No dispute-worthy defect found; residual risk:
snapshot fetch timestamp is taken from the ledger's `opened` field (byte equality with today's fetch
corroborates but does not prove the original fetch time).
