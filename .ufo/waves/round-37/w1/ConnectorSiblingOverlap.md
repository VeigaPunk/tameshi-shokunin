# ConnectorSiblingOverlap — round 37, wave 1

**Verdict: NO CONCRETE PROVINCE OR SKILL OVERLAP.** No sibling `PROVINCE.md` or `SKILL.md` owns the bounded ANSI-C `code_view` branch or the empty-panel replay. Absorb nothing. One depth note follows; it does not re-score C1 or C2.

Axes: this seat is judged on **depth**. The note stops a new intra-lane `W04` and three homonyms from being read as a sibling owner of `tools/tally-audit-v3.py` `code_view`. **Calibration** (C1 empty-panel replay) is untouched: no sibling skill names that adapter, and this note does not retarget it. No axis is re-measured here.

## What was attacked

Sibling lane repos under `/home/vgpnk/Projects/shokunin/`, read-only, against the two r37 surfaces:

- C2: `code_view` ANSI-C `$'...'` state in `tools/tally-audit-v3.py` (docstring at `:152-161`, branch at `:172-194`; S104).
- C1: committed empty-panel replay `.ufo/evidence/round-37/control/replay-empty-panel.py` (`EMPTY_PANEL` at `:18`).

Lane tip `e6185d5f0b63a6963205110cb098f2f1eca27622`. Contract `.ufo/evidence/round-37/contract.json`.

Conf lanes checked: audio, game-dev-2d, game-dev-3d, kaidoku, kasegi, kengaku, kake, kumitate, kotoba, kagi, kama, lore, revenger, mado, tsukuroi, tabi, mori, chousa, kotodama, souji, plus tameshi. Also on disk with no `PROVINCE.md` and no `SKILL.md`: `mori-shokukin`, `tameshi-shokukin`, `kaidoku-sh2`. Not treated as owners.

## Commands and the empty ownership scan

`GIT_OPTIONAL_LOCKS=0` on every git call. No mutating git/jj. No installs.

```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
# e6185d5f0b63a6963205110cb098f2f1eca27622

# per sibling, PROVINCE.md and SKILL.md only
git --no-optional-locks -C "$repo" grep -n -I \
  -e 'tally-audit' -e 'code_view' -e 'empty-panel' -e 'ANSI-C' -e 'ansi-c' \
  -- PROVINCE.md SKILL.md
# every sibling: no output (20 lanes)
```

| lane | HEAD (`rev-parse --short=12`, this run) | province/skill hits |
|---|---|---|
| audio | `7a2fcd4f0883` | none |
| chousa | `872bf3a35078` | none |
| game-dev-2d | `7753d49b1667` | none |
| game-dev-3d | `89dd182b7094` | none |
| kagi | `899c50b42634` | none |
| kaidoku | `f432c8e3bc58` | none |
| kake | `766f4610b64f` | none |
| kama | `7c35289da5f4` | none |
| kasegi | `1fafde8f1145` | none |
| kengaku | `1f3b0f1ec41e` | none |
| kotoba | `2a8eba56b3f9` | none |
| kotodama | `99fae3085ec8` | none |
| kumitate | `8c6f5b017d14` | none |
| lore | `380ef3abc7c7` | none |
| mado | `91862344b9fd` | none |
| mori | `c5326c61bd60` | none |
| revenger | `8362a23538b1` | none |
| souji | `4edb25dfe262` | none |
| tabi | `e3cf4e0d30bb` | none |
| tsukuroi | `564db0b614b2` | none |

Full HEADs observed for the lanes cited below: mado `91862344b9fddbb5b4c3a9977acc776632993799`, mori `c5326c61bd60244cc29d84169fd1dc585fca8cd7`, tsukuroi `564db0b614b2914de5452f9ebd537a0653ae1de5`, kengaku `1f3b0f1ec41ec297130e8944ff97968d32324632`, kotoba `2a8eba56b3f9321b70c569fa2816d42237ca49a2`, chousa `872bf3a3507875b382313f955d15960f9638256f`.

A tracked-tree `git grep` for `code_view`, `empty-panel`, `ANSI-C Quoting`, `tally-audit-v3`, and `ansi-c` found no implementation of either surface outside tameshi. The only `def code_view` / `empty-panel` paths are tameshi's (`tools/tally-audit-v3.py`, `.ufo/evidence/round-37/control/replay-empty-panel.py`, and this lane's own evidence). Nested `SKILL.md` files under skill directories: none within depth 3; the only skill-named dirs were game-dev-3d round reports (`reports/round-104/skill`, `reports/round-105/skill6`), not a shell-lexer skill.

Sibling provinces that name tameshi assign the craft here, they do not split it:

- `kotoba-shokunin/PROVINCE.md:66` — tameshi row, class `adjacent`: "tameshi owns the fixture and mutation method (tameshi `PROVINCE.md` Domain line)". The rest of that cell is the round-50 checklist-run ruling, not ANSI-C quoting and not the empty panel. Pin in that cell is `3b20f073…`, older than this tip; this seat does not edit kotoba.
- `kengaku-shokunin/SKILL.md:3` — "tameshi owns verification-fixture craft."
- `tameshi-shokunin/PROVINCE.md:3-5,14-20` — verification-fixture craft; every sibling gate stays that lane's; out of province is reported, not absorbed.

## Not overlap (path and citation)

These are the collisions a token scan will raise. None is ownership of the two surfaces.

**(1) Intra-lane W04, not a sibling share.** Census `url_of` (`scripts/sources-census.sh:600-604`) strips the `#…` fragment and keeps the query. S104's URL (`corpus/SOURCES.md:113`, fragment `#L489-L493`) therefore normalizes to the same string as S097 (`corpus/SOURCES.md:106`, `?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303`, no fragment). Committed validate already recorded that and only that:

- `.ufo/evidence/round-37/census/start.stdout` — no S104 line; `ok`; before the row.
- `.ufo/evidence/round-37/census/end.stdout:10` — `tameshi W04 S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes`.
- `.ufo/evidence/round-37/census/end.exit` — `0`. `end.stdout:11` is `ok`. W04 is across scopes, not E04.

S097's scope is exit status (`bashref.texi` lines 3890–3916) and `case` (lines 1044–1084). S104's scope is §ANSI-C Quoting, lines 489–493. Same blob, different sections. The warning does not say a sibling owns line 489.

**(2) Same Bash 5.3 tree, other sections, other lanes — not in `shared`.** Re-derived `url_of` (fragment stripped, query kept):

| row | normalized URL | section the row actually teaches |
|---|---|---|
| tameshi S104 / S097 | `cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9…` | 489–493 vs 3890–3916 and 1044–1084 |
| mado S110 (`mado-shokunin/corpus/SOURCES.md:122`) | `…/bashref.texi?h=bash-5.3` | §The Set Builtin `-e`, lines 5929–5958, commit `b8c60bc9…`, file sha256 `f3d37d57…` (same bytes S097 records) |
| mori S075 (`mori-shokunin/corpus/SOURCES.md:81`) | `ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` | pipefail 6063–6064 and PIPESTATUS 7490–7492; status `queued` |
| tsukuroi S175 (`tsukuroi-shokunin/corpus/SOURCES.md:181`) | `git.savannah.gnu.org/cgit/bash.git/plain/doc/bash.1?h=bash-5.3` | `doc/bash.1` `BASH_ENV` / `ENV`, not `bashref.texi` |

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin
# rc 0; 55 lines; 0 lines matching bash / savannah / ftp.gnu.org/gnu/bash
```

Mado's province (`PROVINCE.md:3-16`) is the Hyprland/waybar plane. Mori's (`PROVINCE.md:3-16`) is fleet observability. Tsukuroi's (`PROVINCE.md:3-14`) is host operability. None of those skills contains `code_view` or `ANSI-C`. Mado S107 (`corpus/SOURCES.md:119`) is CPython `shlex.join`, a pure formatter — not Bash `$'...'`.

**(3) The word `replay` is three other crafts.**

- `kengaku-shokunin/PROVINCE.md:19` and `SKILL.md:515` — `grader.py` replays four committed eval probe trees (r8/r9/r11/r12). `SKILL.md:3` calls this "offline replay grading".
- `mado-shokunin/SKILL.md:548` — digest-pinned replay of incident transcript lines (`mado-tripwire-frozen`). `SKILL.md:1020-1022` replays `mado-verify.sh --regression` and points `MADO_VERIFY_HARNESS` at tameshi's `mutate-and-run.sh`. That is the runner this lane audits, not `code_view`, and not the empty-panel tree.
- `game-dev-2d-shokunin/PROVINCE.md:24-26` — frontier "reusable input replay" and "host-scoped physics replay".

**(4) Substring hits that are not the function.**

- `mori-shokunin/corpus/evidence/recheck-r32/S012.src:59` — GitHub `featureFlags` includes `code_view_raf_sticky_lines`. A saved HTML page, not a scanner.
- `mori-shokunin/sd-main.c:22` — `#include "ansi-color.h"`. The `ansi-c` grep matches `ansi-color`.
- `tsukuroi-shokunin/.ufo/waves/round-36/w1/ConnSiblings/ConnSiblings.md:57,129` — cites tameshi `tally-audit-v3.py:332` as a different program from tsukuroi's env allowlist: "None is a before-state, an after-state, or a kill-rule witness." That citation is the child-env lines, not the new `ansi-c` branch, and it disclaims the tool.
- `kake-shokunin/.ufo/waves/round-44/w2/ScoutSiblingOverlap.md:81` — the one `witness-class` file is tameshi's `SimplifyCodeView.md`. Kake is pointing at this lane.
- `kumitate-shokunin/.ufo/waves/round-52/w1/ConnOverlap.md:49` and `kotoba-shokunin/.ufo/waves/round-62/w2/FalsifyConnector.md:74` — name `tally-audit-v3.py` as tameshi's, and say no / not their shape.

## Bounded proposal (one)

**Leave the W04 as an across-scope warning against S097. Do not retarget S104 at a sibling URL, and do not import another Bash section or another lane's replay into either frozen predicate.**

Contradiction, stated separately (not averaged):

- The new validate line is real. `end.stdout:10` names S104 and the `?id=b8c60bc9…` URL. `start.stdout` does not. The normalizer's fragment strip is why S104 and S097 compare equal.
- That line is not a sibling contest. `shared` (55 lines, rc 0) contains no Bash URL. Mado's `?h=bash-5.3`, mori's tarball, and tsukuroi's `bash.1` stay unequal after `url_of`.
- The sections are not the claim. `code_view`'s docstring (`tools/tally-audit-v3.py:157-161`) cites §ANSI-C Quoting only, and says nested substitutions and unquoted backslash-newline continuations stay outside the view. S097 does not teach lines 489–493. Mado S110 teaches `set -e` exceptions. Teaching those from this row, or scanning them in `code_view`, would exceed the two frozen fixtures.

Move: leave `tools/tally-audit-v3.py`, S104, S097, `replay-empty-panel.py`, and every sibling province and skill byte-identical. Do not "clear" W04 by switching S104 to mado's `?h=bash-5.3` (that would create the cross-lane `shared` row this scan did not find). Do not fold S104's scope into S097's exit-status scope. Do not point the empty-panel adapter at kengaku's grader, mado's tripwire replay, or game-dev-2d's input replay. Chousa owns research method (`chousa-shokunin/PROVINCE.md:3-8`); that does not move the located quote out of tameshi's registry.

## Second-order effects

- **Runtime:** no `code_view` measurement, no empty-panel replay, no sibling gate. The census `shared` run only reads registries.
- **Contract:** C2's kill rule freezes the two fixtures and forbids a code-view edit after the tool pin. Editing `code_view` or S104's URL to absorb mado's `set -e` section would break that bound. C1's kill rule is the committed empty specification plus v1/v2 receipts; swapping in another lane's replay would change the input.
- **Substrate:** siblings stayed read-only. No `shlex` row, no `set -e` row, no grader copied in.
- **Calibration:** the empty-panel path is unnamed in every sibling province and skill. This note does not change receipts or the mismatch counter.

## Risks

A later seat can misread `end.stdout:10` as "S104 is not new" or as "mado already opened this manual, so the branch is theirs." It is neither: W04 is across scopes inside tameshi, and mado's query string does not join `shared`. The other misread is treating `code_view_raf_sticky_lines`, `ansi-color.h`, or the word `replay` as a contest. They are not. Copying mado S110's URL into S104 would add a fleet `shared` row that does not exist today. Kotoba's adjacency pin is stale relative to `e6185d5f`; refreshing that pin is kotoba's table, not this claim.

## Verification

L1 can re-run the province/skill `git grep` (expected: empty) and `sources-census.sh shared` (expected: no Bash URL). Confirm `end.stdout:10` is still the only S104 warning and `end.exit` is 0 before anyone treats that warning as a sibling owner. Do not re-run the C1 calibration counter or the C2 deciding command for this note.

Only discovery reads, read-only `git grep` / `rev-parse`, one read-only `shared` census, and this report were produced. No production edits, no Git/jj writes, no `code_view` or replay runs, no model calls, no other agent runtime. Tools installed or updated: none.

Report: .ufo/waves/round-37/w1/ConnectorSiblingOverlap.md
