# T49Read15 — C1 reader: `## Pin disposition and provenance correction — round 13`, pointer ordinals 0–4

Base `8ca67421111fa354b47b803358391d0b07fc6db9`. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Counter/contract were read, never edited and never invoked as a verdict; only the two non-counter tools'
`--selftest` modes were executed. No claim is decided here.

Deliverable: `.ufo/waves/round-49/w1/T49Read15.rows.json` (5 rows, schema-free wrapper `{"rows": [...]}` as
the item specifies). Every row was machine-checked before writing: claim is a verbatim substring of the
whitespace-collapsed SKILL.md, excerpt is a 24–400-character verbatim slice of the collapsed pointed text
(the counter's own `norm`/`pointed_text` rule, `ranges: null` → whole file, reproduced literally).

## Counted section boundary (matters for the L1's edits)

`## Pin disposition and provenance correction — round 13` is `SKILL.md:1517-1546` at base (sectionizer
`.ufo/evidence/round-18/measure.py:209-239` splits at any `#`/`##`/`###`, so the section ends before
`### Round-13 gate/probe registry` at `SKILL.md:1548`). Its sha256 prefix `eb9c487be851` equals
`section_sha256` in `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`.
Consequence: the registry rows at `SKILL.md:1550-1551` are **not** part of the counted section, and none of
this section's 9 pointers (floor 9) lives there. Pointers 5–8 (`witness-metadata.json`, S003/S047/S041) are
other seats' rows.

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca674211:SKILL.md | sed -n '1517,1546p'
python3 -c 'import importlib.util;s=importlib.util.spec_from_file_location("m",".ufo/evidence/round-18/measure.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)'  # sectionize -> start 1517 end 1547
```

## Verdicts

| ord | pointer (raw) | skill_line | base_verdict | one-line reasoning |
|---|---|---|---|---|
| 0 | `corpus/knowledge/incremental-pin-disposition.md` | 1520 | **holds** | The entry is exactly the six-leg content-disposition method the section's table and steps 1–2 use: read-only classification, `unchanged/changed/unavailable`, `result_reuse=not_established`, and the required `not_compared` disclosure; it also carries the S048 precision correction the section names (`:5`). |
| 1 | `corpus/lessons/round-12-verifier-spotcheck.md` | 1521 | **holds** | `## Routed defects and residuals` item 3 (`:146`) is the tameshi direction that names the nested `declaration.kind=null` defect and forbids rewriting the frozen declaration — the thing the section's table row 5 and step 4 act on; the file's author line (`:1`) is the outside hyaku closure, so "outside routed" is supported. |
| 2 | `tools/pin-disposition.py` | 1535 | **holds** | CLI is `--manifest PATH --root FLEET` (`:1336-1366`), verbatim as the recipe writes it; read-only guarantee block `:82-90`; every subprocess is git plumbing (`:227-235`, selftest `:770-790`) so "executes no sibling gate" holds; observed selftest PASS 19/19 exit 0. |
| 3 | `.ufo/evidence/round-13/pin-manifest.json` | 1535 | **holds** | File exists at base, `schema: pin-manifest-v1`, six legs; all six `expected_sha256` equal the base runner's `PIN_*` (`tools/mutate-and-run.sh:605-622`) and all six `pinned_commit` equal `REV_*` — i.e. the file really is the current hash/commit baseline the clause names. |
| 4 | `tools/witness-metadata.py` | 1538 | **holds** | `--check` + `--companion` exist (`:1220-1247`), `DEFAULT_COMPANION_REL` is exactly the recipe's path (`:68`), and the pinned input digests (`:73-89`) equal the base blobs of `summary.json`/`declaration.json`/`declared.tsv`; observed selftest PASS 39/39 exit 0. |

Tally: holds 5, stale 0, unresolved 0, absent 0. Because no row is non-`holds`, the deliverable has no
`proposed_fix` entries; there is no section text this seat proposes to change, and floors stay intact.

## Findings

F1. **Target-side line drift in `.ufo/evidence/round-13/pin-manifest.json` (routed, not a pointer verdict).**
`pin-manifest.json:7` claims `tools/mutate-and-run.sh:84-89 (leg/path table), :542-553 (PIN_*/REV_* pairs),
:1112-1140 (six ledger leg calls)`, and `:16,24,32,40,48,56` repeat `:542-543 … :552-553` style anchors. At
base those anchors are wrong: the leg comment table is `:85-95` (now nine legs), the `PIN_*`/`REV_*` pairs are
`:605-622`, and the six ledger calls start at `:1386` (`js-kimi-census` `:1386`, `js-claims-check` `:1412`).
It is not a stale *value*: the runner at round 13 was `75ed934d` and its tables sat at the cited lines
(`git -C … show 4acc607:tools/mutate-and-run.sh | sed -n '542,553p'` returns the `PIN_*` block there).
Commands: `git -C … show 8ca67421111fa354b47b803358391d0b07fc6db9:.ufo/evidence/round-13/pin-manifest.json`
and `git -C … show 8ca67421111fa354b47b803358391d0b07fc6db9:tools/mutate-and-run.sh | grep -n 'PIN_'`.
Routed for a lesson/errata note, not for editing the frozen round-13 receipt. I did **not** call the pointer
stale, because the section's clause is about the pinned values, which are correct and current.

F2. **Same drift inside the knowledge entry.** `corpus/knowledge/incremental-pin-disposition.md:1` cites
`tools/mutate-and-run.sh:80-89, 540-553 @ 4eb4cf3`, and `:108`, `:114`, `:141`, `:146`, `:230` repeat
`:81-83`, `:1113-1140`, `:109-114`, `:104-106`. Those anchors were valid when written and drifted as the
runner grew: at `4acc607` the leg table is `:84-89` and the `js-kimi-census` ledger call is `:1112-1116`
(verified), while at base they are `:85-95` and `:1386-1390`. The values the entry reports still reproduce.
Command: `git -C … show <BASE>:corpus/knowledge/incremental-pin-disposition.md |
grep -n 'mutate-and-run.sh:'`. This is the same defect class that round-12 lesson `:146` routed ("brittle …
line citations … the document's lines moved"), which is why the entry was treated as `holds` with a note and
not as a pointer fault.

F3. **`derived_from.sha256` is a derivation-time digest, and nothing verifies it.**
`pin-manifest.json:3-5` carries `derived_from.sha256 = 75ed934dc8…`, equal to the runner blob at the round-13
content commit `4acc607` and to `tools/witness-metadata.py:120` `HISTORICAL_RUNNER_SHA256`; the base runner
blob is `a7d3f2dd7d47…`. `grep -n derived_from tools/pin-disposition.py` returns nothing, so the recipe command
is unaffected and the field cannot make the section's clause false. Commands:
`git -C … show 4acc607:tools/mutate-and-run.sh | sha256sum` → `75ed934d…`;
`git -C … show <BASE>:tools/mutate-and-run.sh | sha256sum` → `a7d3f2dd…`.

F4. **Only one of the two tools changed since round 13 (relevant to the L1 re-key).**
`.ufo/evidence/round-13/verification.json` `measured_input_sha256` records `tools/pin-disposition.py`
`297253971dab…` and `tools/witness-metadata.py` `df3390682a04…`; at base they are `331529eadafe…` and
`df3390682a04…` (byte-identical). `.ufo/evidence/round-13/pin-manifest.json` is also unchanged
(`64eaa43e…` both). So the section's steps 2 and 3 trace-bind to live files, and a re-key that binds the
section to `tools/pin-disposition.py` will bind *today's* bytes, not the round-13 receipt's digest —
which the counter's durability check accepts (it reads non-record files from the REV tree) but a reader
should not misreport as "round-13 tool". Commands: `git -C … show <BASE>:<path> | sha256sum` for each path.

F5. **Selftest temp-dir asymmetry (bound for seat runs, not a defect of any clause).**
`tools/pin-disposition.py:706` hardcodes `tempfile.mkdtemp(..., dir="/tmp")`, so `TMPDIR` does not redirect
it (fixtures are removed on pass, `:1328`); `tools/witness-metadata.py:1122` uses `tempfile.mkdtemp()` and
does honour `TMPDIR`. Observed with `TMPDIR=/fast/scratch/hyaku/tameshi-r49/T49Read15`:
`python3 -B tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0, no `/tmp` leftover;
`python3 -B tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exit 0.

F6. **Registry cells are outside the counted section** (see boundary note). Both registry rows remain accurate
as read: `SKILL.md:1550` verdict map ("0 observations … 2 invalid input … selftest 1 failed") matches
`tools/pin-disposition.py` (`:667-691` run exit 0, `:1320-1330` selftest 0/1); `SKILL.md:1551` matches
`tools/witness-metadata.py:44-56` exit map. No correction proposed, and none is needed for the counter, since
those cells are not part of the seven target sections.

## Bounds and limits

- Read-only on the lane: only `.ufo/waves/round-49/w1/T49Read15.rows.json` and this report were written.
  Nothing under `/home/vgpnk/.local/state/`, no C2 witness/control stdout, no sibling lane or fleet-repo edit.
- All target text was read from base blobs (`git show 8ca674211…:<path>`), never from the mutable worktree.
- I did not execute `tools/pin-disposition.py` in run mode (it would read sibling lanes; reading its source
  and the committed round-13 receipts was sufficient to decide the clause) and did not execute
  `tools/witness-metadata.py --check` (gate execution is the L1's/decider's; committed receipt
  `.ufo/evidence/round-13/verification.json` was inspected instead).
- Semantic limit inherited from the contract: this row set proves the quoted text is really at the pointed
  place and that I judge it to support the clause; it is not a mechanical proof of support.
- No tool installed or upgraded (no pacman, no uv/npx). Scratch root
  `/fast/scratch/hyaku/tameshi-r49/T49Read15` was created, used, and removed before this report was written.

## Summary

- Five pointers read at base `8ca67421`: all five `holds`; stale 0, unresolved 0, absent 0; no `proposed_fix`.
- Section text at base is `SKILL.md:1517-1546` (sha prefix `eb9c487be851`); the `### Round-13 gate/probe
  registry` rows (`:1550-1551`) sit outside it, so this section's 9 pointers are all in the Sources line and
  recipe steps 2–3.
- Every row's claim is a verbatim substring of collapsed SKILL.md and every excerpt (236–313 collapsed chars)
  was tested against the counter's collapse rule before writing.
- `tools/pin-disposition.py` and `tools/witness-metadata.py` both selftest green at base (19/19 and 39/39,
  exit 0); the manifest's six pins equal the runner's current `PIN_*`/`REV_*` (`:605-622`).
- Routed target-side drift, not pointer staleness: `pin-manifest.json:7,16,24,32,40,48,56` and
  `incremental-pin-disposition.md:1,108,114,141,146,230` cite runner lines that moved (pins now `:605-622`,
  ledger calls now `:1386-1412`); values are unaffected, and frozen round-13 bytes should not be rewritten.
- `derived_from.sha256=75ed934d…` is the derivation-time runner digest (round-13 commit `4acc607`), not the
  base runner `a7d3f2dd…`; the tool never reads that field.
- `tools/pin-disposition.py` changed since round 13 (`331529ea…` vs receipt `29725397…`),
  `tools/witness-metadata.py` did not (`df339068…` both) — relevant to how the L1 trace-binds the section.
- Deliverable: `.ufo/waves/round-49/w1/T49Read15.rows.json` (5 rows); no claim decided, no counter verdict run.
