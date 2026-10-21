# Secret-shape review — 2026-10-21

## Scope and source
Reviewed only the round-18 §5 correction inputs present beneath `/home/vgpnk/Projects/shokunin/tameshi-shokunin`:

- `corpus/knowledge/guard-kill-closure.md`
- `corpus/knowledge/mutation-case-kumitate-sources-check.md`
- `corpus/SOURCES.md`
- `corpus/lessons/round-18.md`
- `.ufo/evidence/round-18/final/checks.json`
- `.ufo/evidence/round-18/final/bash-witness.stdout`
- `.ufo/evidence/round-18/final/measure-final-60.json`

Input list source: `corpus/lessons/round-18-verifier-spotcheck.md` §5, lines 180–205; reviewed 2026-10-21. Short source quote: “Routed defects (lane to fix next round)” (§5 heading).

## Command and observed outcome
Command: read-only inline Python Eval rooted at the absolute lane path above; read only the seven listed files; count matches without printing matched text. Credential-shape detectors covered provider-token forms, bearer/basic values, JWTs, URL userinfo, and non-placeholder values assigned to credential-like keys. A second detector counted explicit `refs/{heads,remotes,tags,replace,notes}/...` shapes. No subprocess, private config, or receipt argv was used or executed.

- Credential-shape candidates: **0 across 7 files**.
- Git-ref-shaped mentions: **4 occurrences / 3 unique** in `corpus/knowledge/guard-kill-closure.md`; **0** in each of the other six files.
- Of those unique refs, **2** are outside the scanner's common-ref allowlist. These are counts only; no ref names or matched values are reproduced. “Outside allowlist” does not establish that a ref is private.

## Finding
**Severity: Low, unconfirmed private-ref exposure.** A reader of `corpus/knowledge/guard-kill-closure.md` can observe ref-shaped identifiers. If the two non-common identifiers are private refs, the note discloses their names and may help correlate internal work. The assigned evidence does not establish their confidentiality, and this review did not inspect private refs/config. No credential-shaped value was observed.

**Smallest remediation:** if the two identifiers are private by policy, replace only those literal identifiers with neutral pinned-revision wording; otherwise record that they are public. Re-run the same bounded count after any change.

**Limit:** this was a pattern scan over the named inputs, not proof that arbitrary or encoded secrets are absent.