# QUALITY criteria 20–21

Source: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md`.

## Verbatim criteria

**Criterion 20 (lines 102–105):**
> 20. An instrument that seats execute in a wave is not edited in place during
>     that wave. Changes are staged at a separate path and installed after the
>     readers finish, and every receipt names the instrument sha it ran.
>     (`lessons/round-16.md`, scope mistake)

**Criterion 21 (lines 107–115):**
> 21. Supersedes criterion 20's last clause ("every receipt names the instrument
>     sha it ran"). A retained receipt carries the instrument's sha256 beside it
>     in the same file, because the runner's `--selftest` prints none
>     (`.ufo/evidence/round-16/round-gate/runner-selftest.txt` ends with the
>     sha line). Criterion 20's no-in-place-edit rule stands; it recurred once
>     in wave 2 (`measure.py` repaired after dispatch), and that wave's
>     attackers read the committed bytes, so no verdict mixed the two.
>     (`lessons/round-16.md`, scope and vacuous rows; w2 QualityReview,
>     MistakeAudit)

## Finding

Criterion 20 forbids editing in place, during a wave, an instrument used by seats executing in that wave. It requires staging changes at a separate path and installing them only after the readers finish; it also says each receipt names the instrument SHA it ran (lines 102–105).

Criterion 21 adds a stronger, concrete receipt-location requirement: the retained receipt itself must carry the instrument's SHA-256 beside it in that same file, since `--selftest` prints no SHA (lines 107–110). It supersedes only criterion 20's final receipt clause, “every receipt names the instrument sha it ran” (lines 104, 107–108). The prohibition on in-place edits and the staging/install-after-readers rule remain; criterion 21 expressly says the no-in-place-edit rule stands (lines 111–113).

**Verdict:** Agree with the criteria as written. No contradiction found in the assigned text. **Defects:** None observed within this scope. **Confidence:** High; both criteria were read verbatim from the cited source lines. No additional unresolved question for this assignment.

## Commands and observed outputs

- `functions.grep(path="/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md", pattern="^#+ *(20|21)\\b")` → `No matches found` (the criterion labels are numbered list entries, not headings).
- `functions.grep(path="/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md", pattern="20|21")` → output located criterion 20 at line 102 and criterion 21 at line 107.
- `functions.read(path="/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md:102-114")` → returned the exact criterion text quoted above (including its continuation through line 115).
- `wc -l /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md && sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md` → `386 /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md`; `e65edf6148742ab91f1713c224d646886a90a7c33c95abc7e11e792200601385  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md`.
