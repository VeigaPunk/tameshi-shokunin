# T51ScribeRowBash — C2 source row S273 (GNU Bash manual, §The Set Builtin)

Seat: `T51ScribeRowBash`, round 51 (hyaku run 9), item **Milestone: C2 source row S273**.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at `9962033fd7a75aa2f2847e979dd687a5d28505a1`
(read-only from this seat: no lane file written, no index/jj touched, no commit in the lane or the
fleet). Scratch `/fast/scratch/hyaku/tameshi-r51/T51ScribeRowBash` (`S`), deleted at the end.
Tooling: nothing installed or upgraded this seat (no `pacman`, no `uv`, no download of a binary);
`curl`, `bash 5.3.20(1)-release`, `python3`, `git`, `awk` were already present.

Deliverable: this file, plus the drafts and receipts in `./T51ScribeRowBash/`
(`draft-S273.md`, `registry-with-S273.md`, `chet-bashref.html`, `fetch-receipt.txt`,
`bashref-texi-excerpt.txt`, `probe/`, `mutant-receipt.txt`, `base.out`, `draft.out`, `final.out`).

---

## 1. What was opened, and what would not open

| # | URL | result | bytes | sha256 | UTC |
|---|---|---|---|---|---|
| A | `https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html` (the item's URL) | **HTTP 000**, curl exit 28, connect timeout | 0 (no file) | — | 8 attempts, 2026-10-27T00:12Z … 00:22:10Z |
| B | `https://tiswww.case.edu/php/chet/bash/bashref.html` (author copy, Chet Ramey; Edition 5.3, last updated 18 May 2025) | **HTTP 200** | 1,040,870 | `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4` | 00:22:10Z and 00:22:12Z, byte-identical |
| C | `https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9…b303` (S097's pin) | **HTTP 200** | 415,804 | `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` | 00:22:14Z |

Receipt: `./T51ScribeRowBash/fetch-receipt.txt`; command shape
`curl -sS --max-time N -o FILE -w 'HTTP=%{http_code} bytes=%{size_download} …' URL`.

**F1 — the gnu.org host is unreachable from this machine, in every shape tried.** Eight attempts,
no HTTP status ever returned: node page over https (60 s twice), the single-page
`https://www.gnu.org/software/bash/manual/bash.html` (45 s), `-4` (20 s), `http://` port 80 (20 s),
`https://gnu.org/…` without `www` (15 s), `https://www.gnu.org/savannah-checkouts/…` (15 s), and
the authenticated receipt attempt A (20 s). `getent hosts www.gnu.org` returns only
`2001:470:142:5::116`. This is the class r32, r34 and r35 already recorded
(`corpus/SOURCES.md:426` r32: "the rendered gnu.org
page timed out"; `:430` S098's `Conditional-Constructs.html` "both addresses timed" out; `:453` r35: "the
gnu.org Bash manual Comments page timed out at 60 s"), so the row names the carrier that **opened** — precedent S097, whose
source cell carries the same disclosure for the `Exit-Status.html` node
(`corpus/SOURCES.md:106`).

## 2. The located quotes (≤25 words each) and where they sit

Manual text is identical in B and C: with C at S097's own digest (`f3d37d57…2be32d5`, the value
S097 records at `corpus/SOURCES.md:106`), the texi has not moved since 2026-10-23, so the anchors
transfer. Verbatim from B (`chet-bashref.html`) and C (`bashref.texi`), extracted to
`./T51ScribeRowBash/bashref-texi-excerpt.txt`:

| quote | words | B (single-page) | C (texi) |
|---|---|---|---|
| `Exit immediately if a pipeline … returns a non-zero status` | 9 | `:6548-6553` | `:5930-5935` |
| `The shell does not exit if the command that fails is … any command in a pipeline but the last` | 19 | `:6554-6560` | `:5936-5942` |
| `any command in a pipeline but the last (subject to the state of the pipefail shell option)` | 17 | `:6561` | `:5943` |
| `the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status` | 20 | `:6707-6709` | `:6063-6065` |
| `the exit status of the last command substitution performed` | 9 | `:4172-4173` | `:3675-3677` |

- `-e` (B `:6547-6582`, C `:5929-5948`): exits on "a pipeline … [that] returns a non-zero status", and the non-exit list
  is `while`/`until` lists, an `if` test, anything in `&&`/`||` except the last, every pipeline
  command but the last *subject to `pipefail`*, and `!`-inverted statuses. Also: "A trap on `ERR`,
  if set, is executed before the shell exits" (B `:6566`, C `:5948`) and "If a compound command or shell function executes
  in a context where `-e` is being ignored" nothing inside is affected (B `:6572-6580`, C `:5954-5962`).
- `pipefail` (B `:6706`): the pipeline's return value is the rightmost non-zero command's status,
  or zero; "disabled by default".
- The bridge the manual never states in one sentence: a command with no command name takes the
  status of its last command substitution (§Simple Commands, B `:4172-4173`).

## 3. Does `actual=$(grep -nE -m1 … | cut -d: -f1)` end `drift-pins.sh`, and with what status?

**Yes — status 1, silently, at the assignment.** Chain, each link cited above: `grep` returns 1 on
zero matches and `cut` returns 0, so under `pipefail` the pipeline's value is 1; the pipeline is the
command substitution; the assignment has no command name, so the command's status is the
substitution's (1); `-e` exits on a pipeline returning non-zero and the assignment is not one of the
listed contexts. Then `-e`'s exception list is what decides whether the *site* is protected, and it
is not: `verify()` is invoked as a plain simple command in a `case` arm
(`kagi-shokunin` `corpus/drift-pins.sh:449` at `e64e81b8`: `verify) verify ;;`), not in an
`if`/`&&`/`||`/`while` context. `set -euo pipefail` is at `:37`; the site in `verify` is `:238`;
the same assignment exists a second time in `pin()` at `:354`.

The manual's own caveat matters for the ledger: called as `verify || rc=$?` the whole body would be
inside a context where `-e` is ignored (`:6572-6576`), the assignment would merely set `actual=""`
and execution would continue. That is measured, not assumed (probe `p5_cond.sh`).

## 4. Empirical checks (scratch, `$S/probe`, transcript `./T51ScribeRowBash/probe/observed.txt`)

Bash `5.3.20(1)-release`; `f.txt` contains `alpha`/`beta`; ERE `^zzz$` matches nothing.

| probe | option line | call shape | observed | exit |
|---|---|---|---|---|
| `p1_top.sh` | `set -euo pipefail` | top-level `actual=$(grep … \| cut …)` | **no output at all** | **1** |
| `p2_func.sh` | `set -euo pipefail` | same inside a function called plainly (gate's shape) | **no output at all** | **1** |
| `p3_nopipefail.sh` | `set -eu` | same | `MOVED …:1->` + `DRIFT_PINS: DRIFT` printed, then dies on the function's `return 1` | 1 |
| `p4_noe.sh` | `set -uo pipefail` | same | `MOVED …:1->`, `DRIFT_PINS: DRIFT`, `REACHED-END` | 0 |
| `p5_cond.sh` | `set -euo pipefail` | `rc=0; verify \|\| rc=$?` | body continues, `MOVED …:1->`, `REACHED-END rc=1` | 0 |
| inline | `set -euo pipefail` / `set -eu` / `set -uo pipefail` on the bare pipeline | — | dies / `status=0 actual=[]` / `status=1 actual=[]` | 1 / 0 / 0 |

Reading: `pipefail` is the single switch that turns the miss into a failure (row 3 vs the `set -eu`
inline cell), and `-e` in a plain call context is the single switch that turns the failure into
death (rows 1–2 vs row 4), while the *call context* is the third switch (row 5).

## 5. The mutant, reproduced faithfully (receipt `./T51ScribeRowBash/mutant-receipt.txt`)

Pinned bytes `sha256 c138d34c…c70feb`, 19,088 B, 451 lines, `100755`
(`git -C kagi-shokunin show e64e81b8:corpus/drift-pins.sh`); one edit in scratch
(`if [[ "$n" -eq 0 ]]` → `-eq -1`), `count(@old)=1`, mutant `cba1467a…5b7a`.

| run | TMPDIR | observed | exit |
|---|---|---|---|
| pristine `--selftest` | neutral | `DRIFT_SELFTEST: PASS (13 cases)` | 0 |
| mutant `--selftest` | neutral | `drift-selftest: FAIL symbol gone: no /GONE/ in output` · `DRIFT_SELFTEST: FAIL (1/13 cases)` | **1** |
| mutant `--selftest` | `$S/sandbox-K_GONE_ARM` | `DRIFT_SELFTEST: PASS (13 cases)` | **0** |
| the "symbol gone" case alone, pristine | defect-named | `DRIFT …/b.txt sha 2c8b08da→d9f86d34` · `GONE …/b.txt:1 (pattern no longer present)` · `DRIFT_PINS: DRIFT (files_ok=1 files_bad=1 symbols_ok=1 symbols_bad=1)` | 1 |
| the "symbol gone" case alone, mutant | defect-named | **only** `DRIFT …/b.txt sha 2c8b08da→d9f86d34`, nothing else | 1 |

**F2 — the survival is an oracle artifact, and the mechanism is narrower than "the empty grep ends
the run".** The mutant's child process dies at `:238` *after* the file plane has already printed its
DRIFT line: there is no `GONE` line and, decisively, no `DRIFT_PINS:` summary line — that absence is
the signature of `-e` exiting mid-`verify`. The case then passes for two independent reasons that
have nothing to do with the gate: (i) the exit-status expectation `1` is satisfied by the death
itself (`drift-pins.sh:423`, `run "symbol gone" 1 'GONE'`), and (ii) the verdict-word check is
`elif ! grep -q "$3" <<< "$out"` (`drift-pins.sh:403`) — an unanchored, unquoted-context regex over
text that in the harness contains the sandbox path, and `K_GONE_ARM` **contains** `GONE`.
With a neutral TMPDIR the identical mutant is killed (`FAIL … no /GONE/ in output`, exit 1). This
corroborates `sweep.txt:10` (`DEFECT K_GONE_ARM: SURVIVED (exit=0)`) and the contract's note, and
supplies the missing link: the harness-side `TMPDIR = sandbox-$DEFECT_ID` is not a
cosmetic label, it is the input that flips the verdict. Scope: measured for **K_GONE_ARM only**;
`K_AMBIG_GT` and `K_SHAPE_OPTIN` share the `AMBIG`/`SHAPE` flavour of the same hole
(`sweep.txt:12,17`) but were not re-probed here.

## 6. Is S273 a new URL — W04/E04?

The census compares URLs, not documents: `scripts/sources-census.sh:600-609` (`url_of`) takes the
first `https?://…` in the source cell, strips fragment and trailing `/`, lowercases the host, and
`W04` fires (`:645`) when the same normalized URL already exists in another scope; `E04` when it repeats
within one scope without a `supersedes S…`.
`grep -n 'tiswww\|S272\|S273' corpus/SOURCES.md` → nothing. Held bash rows:
`corpus/SOURCES.md:106` (S097) and `:113` (S104) both hold the Savannah texi URL — S104's fragment
`#L494-L495` normalizes away, which is why the base registry already carries
`W04 … S104 duplicate url cgit.git.savannah.gnu.org/…` (`./T51ScribeRowBash/base.out`). S273's
`tiswww.case.edu/php/chet/bash/bashref.html` is a **new URL**: the draft's validation output is
byte-identical to the base's (`diff base.out final.out` → empty), so S273 adds no W04 and no E04.
Disclosed: it is the **same document** S097/S104 pin at the Savannah commit, presented by the
author as a rendered single-page copy; S160 set that precedent (a second row for a held document
when the carrier and the anchor differ: S160 at `corpus/SOURCES.md:130`, note at `:480`). The row
therefore claims a **new section scope** (§The Set Builtin, `errexit`/`pipefail`), not new text,
and cites the texi line ranges as corroboration.

**F3 — claim novelty.** No held row teaches this: `grep -n 'errexit\|pipefail' corpus/SOURCES.md` and
`grep -n 'set -e' corpus/SOURCES.md` both return nothing, S097 is "exit-status range and special statuses" (`corpus/SOURCES.md:106`) and S102 is POSIX
token recognition (`:110`). S273 is a new scope, not a re-open of a held claim.

**F4 — id space.** Last registry row `corpus/SOURCES.md:146` is `S271`; the registry's own line
`:498` says `- Next unused id: S272`. Per the assignment this row is `S273`; if no row takes S272
in this round the file has a one-id gap, which the census does not police (no contiguity code) but
the round note should state. The draft note says so.

**F5 — date skew, disclosed.** `opened` is `2026-10-26`, the lane's local round date (host clock
`Mon 26 Oct 2026 21:2x -03`); every fetch receipt is `2026-10-27T00:2xZ`. The UTC day boundary
falls inside this round. The counter requires exactly `2026-10-26`
(`.ufo/evidence/round-51/c2/measure.py:211`), and the census `E08` (opened not in the past) is
evaluated against the local date, so both hold; nothing is retro-dated silently.

## 7. Validation of the draft (pasted, scratch clone only)

`git clone -q --shared <lane> $S/lane`; `git -C $S/lane rev-parse --show-toplevel` →
`/fast/scratch/hyaku/tameshi-r51/T51ScribeRowBash/lane` → exactly the clone; registry copy `$S/lane/corpus/SOURCES.md`
with the row inserted after `:146` and the round note appended.

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$C/corpus/SOURCES.md"
# baseline (clone's own registry, untouched)
file    ok      …/lane/corpus/SOURCES.md
exit=0        # 0 × E, 14 × W04, 1 × W01

# draft row only (entry not yet written)
file    E11     S273 missing used-by corpus/knowledge/mutation-case-kagi-drift-pins.md
exit=1        # diff vs base: this one line only

# draft row + draft entry carrying the source: line
file    ok      …/lane/corpus/SOURCES.md
exit=0        # diff vs base: empty  → identical warning set (14 × W04, 1 × W01, 0 × E)

$ grep -c '^| S[0-9]' "$C/corpus/SOURCES.md"          → 132
$ grep '^| S273 |' … | awk -F'|' '{print NF}'        → 13   (11 cells; no pipe inside a cell)
```

Frozen-rule replay against those clone commits (**simulation, not a verdict**): importing
`.ufo/evidence/round-51/c2/measure.py` and calling its own `sourced_entry(lane=clone, rev=HEAD,
rel='kagi-shokunin/corpus/drift-pins.sh')` returned `(1, 1, 1)` and
`ENTRY corpus/knowledge/mutation-case-kagi-drift-pins.md source=S273 readme=1` — i.e. the entry is
seen as added, its `source:` line is at column 0 within `head[:8]`, it contains the target tail,
S273 is `mined`/`2026-10-26`/lists the entry, and the entry name is in the README bytes beyond base.

## 8. Deliverables and drafts

- Row S273 (11 cells, `kind docs`, tier `A`, `status mined`, `opened 2026-10-26`, `recheck 365d`,
  `used-by corpus/knowledge/mutation-case-kagi-drift-pins.md`) — `./T51ScribeRowBash/draft-S273.md` §1.
- `corpus/SOURCES.md` round note (rows 131 → 132, next-unused S274) — same file §2.
- Lesson `## Gate` paragraph for `corpus/lessons/round-51.md` — same file §3 (lane style: URL,
  access date, HTTP, bytes, sha256, tier, anchors, quotes with word counts, limits, and the
  gnu.org non-fetch recorded inside the claim).
- `source:` line the C2 entry must carry, with the counter's exact constraints — §4.
- Snapshot `chet-bashref.html` (1,040,870 B, `b91026ac…177a4`), texi excerpt (no full texi copy:
  the bytes are S097's own pin, digest equal, so copying 415 KB would add nothing).
- `probe/` (`p1_top.sh` … `p5_cond.sh`, `subcase.sh`, `observed.txt`), `mutant-receipt.txt`,
  `fetch-receipt.txt`, `base.out`, `draft.out`, `final.out`, `registry-with-S273.md` (the exact
  registry copy the validation ran on: base bytes + the row after `:146` + the round note).

## 9. Known limits

- The gnu.org page was never read: nothing here describes its bytes, headers or content; the row's
  primary URL is a mirror of the same manual by its author, which is why the texi is quoted for
  line-exact anchors.
- Measured on one host, one bash build (5.3.20), UTC-03 clock; `pipefail`/`-e` semantics are
  portable but the *harness* interaction (TMPDIR naming) is specific to `mutate-and-run.sh` as of
  the sweep revision `a7d3f2dd…d912eb9` (`sweep.txt:1`).
- Only K_GONE_ARM was re-probed; the sibling survivors rest on `sweep.txt` and the contract.
- This seat decides no claim: C1/C2/C3 verdicts belong to the deciding run. Nothing here was
  committed to the lane, and the clone's commits are scratch-only.

## Summary
1. `https://www.gnu.org/…/The-Set-Builtin.html` never answered: 8 attempts, HTTP 000, 0 bytes, all connect timeouts; the row names the author copy that did (`tiswww.case.edu`, HTTP 200, 1,040,870 B, `b91026ac…`), as S097 did for its own timeout.
2. The manual grounds the C2 leg in three separate sentences (`-e` exit rule, `pipefail` return value, assignments-only status) which compose to: a zero-match pin makes `actual=$(grep … | cut …)` itself the failing command.
3. Measured: that assignment ends `drift-pins.sh` with **status 1, silently**, and `pipefail` plus a plain call context (`verify) verify ;;`) are both required for it.
4. The K_GONE_ARM survival reproduces: mutant dies mid-`verify` (no `GONE`, no `DRIFT_PINS`), yet the suite passes only because the unanchored `grep -q 'GONE'` (`drift-pins.sh:403`) matches `K_GONE_ARM` inside the sandbox path; with a neutral TMPDIR the same mutant is KILLED.
5. S273 is a new URL — `tiswww.case.edu/php/chet/bash/bashref.html`; zero W04/E04 added (validated registry warns identically to base), same manual as S097/S104 disclosed, new section scope.
6. Draft row (11 cells, `docs`/A/`mined`/2026-10-26/365d, used-by the C2 entry), round note (131 → 132) and lesson `## Gate` paragraph are in `draft-S273.md`; the frozen `sourced_entry` replay returns `(1, 1, 1)` on a scratch clone.
7. No lane file, no fleet file, no sibling repo and no index was modified; scratch deleted.
