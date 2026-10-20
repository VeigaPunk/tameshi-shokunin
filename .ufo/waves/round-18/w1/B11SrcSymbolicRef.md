# B11SrcSymbolicRef — findings (round 18, wave 1)

## Behavior
Opened `https://git-scm.com/docs/git-symbolic-ref` with `read` (succeeded; no mirror needed). Also fetched raw HTML with `curl -sL --max-time 30 … -o /tmp/tameshi-r18w1-B11-raw.html` (exit 0, 1642 lines) and tag-stripped it to `/tmp/tameshi-r18w1-B11-norm.txt`.

Verbatim checks (`grep -qF` against the normalized text), all FOUND:
- "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently." (§OPTIONS `-q`, 24 words)
- "with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs." (§NOTES, 18 words)
- "Typically you would give HEAD as the <name> argument to see which branch your working tree is on." (§DESCRIPTION, 18 words)

## Duplicate / reject decision
- Duplicate check: `grep -n -i "symbolic\|git-scm.com/docs" corpus/SOURCES.md` returned S062 and S063 only. No existing row carries this URL → **not a duplicate**.
- Support check: the page supports P08 (attached vs detached HEAD: exit 0 = named branch, exit 1 with `-q` = detached, 128 = other error) → **not rejected**.

## Draft
Row S075 and Gate: `.ufo/waves/round-18/sources/S075-B11SrcSymbolicRef.md`. Status `mined`, tier A, kind docs, opened 2026-10-20, recheck on-release, used-by `.ufo/evidence/round-18/` (provisional).

## Flags
1. Id: registry says next unused is S065 (`corpus/SOURCES.md:122`); S075 used per assignment; L1 confirms.
2. `mined` requires a citing knowledge entry or lesson; the directory `used-by` is provisional. Set `queued` if no citation lands.
3. No edits to `corpus/SOURCES.md` or any other lane file. No installs; no git writes; no subagents.

## Verdict
built — row S075 drafted with Gate (URL, access date 2026-10-20, anchors, three verbatim quotes of 24/18/18 words); not a duplicate; not rejected.
