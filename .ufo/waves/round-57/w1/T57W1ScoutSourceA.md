# T57W1ScoutSourceA — source candidate A: exit-status maps (round 57, wave 1)

Item: open ONE external primary source grounding C2's rule that a gate's registry row
pins an exit-code map (0 pass / a could-not-evaluate code / a refusal code) and that
exit 2 conventionally marks a usage or could-not-evaluate condition. Record bytes
sha256, URL, access date, section anchor, verbatim <=25-word quote with location;
state honestly how far it supports "exit 2 = could not evaluate, distinct from
exit 1 = answer is no"; confirm the URL is not already a SOURCES row and propose a tier.

## Source chosen

**GNU Grep Manual, §2.3 "Exit Status"** — <https://www.gnu.org/software/grep/manual/grep.html#Exit-Status>

Why this one over the named candidates: it is the only one whose documented contract
is exactly the tri-state a gate needs. `git diff --exit-code` documents only 0/1
(differences or none) and leaves trouble implicit; sysexits(3) uses codes 64+ with no
0/1/2 tri-state (EX_USAGE=64, not 2). Considered, not fetched (one-source scope).
grep is also the lane's daily predicate tool, so the analogy to a gate is direct:
a program that answers a yes/no question about content and must say "I could not run"
differently from "no".

## Receipt

- Fetched URL: `https://www.gnu.org/software/grep/manual/grep.html` (fragment `#Exit-Status`)
- Access date: 2026-10-28 (session date; fetch timestamp UTC `2026-10-29T00:06:23Z`)
- Bytes: 248,692; **sha256 `517177d02c39c446470c898273036a7616f705e4cbdcb6486b76a25700675f37`**
- Saved receipt: `.ufo/waves/round-57/w1/T57W1ScoutSourceA-receipts/gnu-grep-manual.html`
- Headers receipt: `.ufo/waves/round-57/w1/T57W1ScoutSourceA-receipts/gnu-grep-manual.headers.txt`
  (HTTP 200, Content-Length 248692 matches saved bytes; server sent no Last-Modified)
- Section anchor: `#Exit-Status` (section wrapper div, receipt line 1199; rendered heading
  "2.3 Exit Status", receipt line 1205 area — h3 `id="Exit-Status-1"`)

### Verbatim quote (23 words)

> "Normally the exit status is 0 if a line is selected, 1 if no lines
> were selected, and 2 if an error occurred."

Location: receipt line 1208-1209 (`<p>` opens at 1208); anchor `#Exit-Status`, §2.3.

## Does it support the claim?

**Supported (strong form, with one word of interpretation and two carve-outs):**

- Strong form "exit 2 = could not evaluate, distinct from exit 1 = answer is no":
  supported. The manual separates the check's *negative answer* (1, "no lines were
  selected") from *infrastructure trouble* (2, "an error occurred") in one sentence.
  "Could not evaluate" is the faithful reading of "an error occurred" for a gate —
  the manual itself does not use the phrase "could not evaluate".
- Weaker form "exit codes are a documented contract": trivially supported; this is
  grep's own manual stating the map normatively for grep.

**Not supported by this source (honest gaps):**

1. A distinct *refusal* code. grep's map is 0/1/2: pass / no / trouble. The gate row's
   third cell (a refusal code) is the lane's own design; nothing here grounds it.
   (sysexits(3) would be the natural second source; not fetched, one-source scope.)
2. Strict 0-vs-2 separation. grep carves out `-q`/`--quiet`/`--silent`: with a line
   selected the status is 0 "even if an error occurred" (success answer dominates
   trouble). A gate that wants "0 strictly means evaluated-and-passed" must NOT copy
   that precedence; the C2 map should state so if it cites this row.
3. Portability of 2. "Other grep implementations may exit with status greater than 2
   on error" — fine for a registry row about *this* gate, not a universal claim.

Net: the source grounds the 0 / could-not-evaluate / answer-is-no spine of the C2 map
in one primary sentence; it does not, and is not claimed to, ground the refusal code.

## SOURCES.md check

- URL not already a row: `grep gnu\.org/software/grep corpus/SOURCES.md` → **no matches**
  (the tool's grep tool, pattern `gnu\.org/software/grep`). Near hits are different pages:
  S280 is `gnu.org/prep/standards/.../Errors.html` (GNU Coding Standards error format), not grep.
- Id range free: last rows are S279-S282 (S282 = SLSA build-provenance, REFUSED, opened
  2026-10-28); the file's own tail states "Next unused id: S283". **S283 is the next free id.**

### Proposed row draft (for the L1 to stage; NOT installed by this seat)

`| S283 | GNU Grep Manual, §2.3 Exit Status — https://www.gnu.org/software/grep/manual/grep.html | docs | A | grep's own exit-status contract for a predicate program (0 selected / 1 none / 2 trouble) | §2.3 Exit Status @ fetched 2026-10-28 (sha256 517177d0…675f37; snapshot .ufo/waves/round-57/w1/T57W1ScoutSourceA-receipts/gnu-grep-manual.html) | one sentence pins the tri-state: 0 if a line is selected, 1 if none were, 2 if an error occurred — "answer is no" and "could not run" are distinct codes; -q collapses trouble into 0 when an answer exists, the precedence a strict gate must decline | mined | 2026-10-28 | 365d | round-57 C2 gate-registry claim |`

Tier rationale: **A**, scoped to "GNU grep's own documented exit statuses" — the
publisher's primary doc for its own tool, same standard as S001 (Stryker docs) and
S015 (cram docs). Not an A for "all Unix tools use 0/1/2" (gap 3 above).

## Tooling installs

None. curl (system) only; no pacman, no uv/npm installs.

## Honesty

Ran: fetch + headers (outputs above, receipts saved), sha256sum on the saved bytes,
grep checks on SOURCES.md as quoted. Did not run: any sysexits/git-doc fetch (declared
out of one-source scope); did not install or stage anything in lane production files.
