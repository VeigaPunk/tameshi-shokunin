# T52W1Corr13 — correction record for round-51 cold-read re-key entry `### The map — where a reader enters, artifact by artifact`

Seat: T52W1Corr13 (scribe). Item: C2 m4 correction record for reader `T51W2Read13`, read_rev `02ec217c4d0afabe727fde2e261b7951d28fb4e9`.
Deliverable: `.ufo/waves/round-52/w1/T52W1Corr13.json` (written; this report is the second deliverable).

No claim is decided here. Nothing in the lane checkout was edited: this seat read blobs via `git -C <lane> show REV:path` and wrote only its two wave-1 files.

## What the section says, and what the entry claimed

- The section resolves at read_rev to `SKILL.md:1380-1395`, next heading at `:1396` — command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | grep -n '^### The map\|^### Boundary readings'` → `1380:### The map — where a reader enters, artifact by artifact`, `1396:### Boundary readings, executed by this lane`. The entry's own `start`/`end` (`1380`/`1395`) match the ledger block at `.ufo/evidence/round-21/coldread/ledger.json:41160-41168`.
- The ledger block for this entry (`.ufo/evidence/round-21/coldread/ledger.json:41160` heading, `:41163` verdict `verified-record`, `:41165` `"wrong_expectations": 0`, `:41168` read_rev `02ec217c…`) carries `0` because round 51's refresh wrote the literal: `.ufo/evidence/round-51/coldread/refresh.py:227` — `'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,` — inside the entry dict appended to `working['entries']` just before the ledger write at `refresh.py:241-242`. That is routed defect 3, `corpus/lessons/round-51-verifier-spotcheck.md:128`.
- The reader's own file records six statements of this section that do not hold at its candidate `6d8c11e378aa90b12650808e1b79270742935f15` (which reads the same section bytes as read_rev — `diff <(git show 6d8c11e3:SKILL.md | sed -n '1380,1395p') <(git show 02ec217c:SKILL.md | sed -n '1380,1395p')` printed nothing). The record below transcribes them; `wrong_expectations` is therefore 6, not 0.

## Findings (each quote byte-exact from ONE line of `.ufo/evidence/round-51/coldread/reads/T51W2Read13.md`)

1. `:16` — quote "map says the lane held nine cases since round 26, while candidate runner records ten at round 51" · class **stale-count** · section text: "§3 the six-case ledger (six rows; the lane has held nine cases since round 26)". Reader's pointer row `.ufo/evidence/round-51/coldread/reads/T51W2Read13.md:16`; confirmed at read_rev — `git show 02ec217c:tools/mutate-and-run.sh | sed -n '84p'` → `# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten)`.
2. `:16` — quote "runbook §7 says default scratch is `mktemp -d /tmp/...` (:349-351), while candidate runner explicitly honors TMPDIR" · class **stale-pointer** (the cited runbook §7 detail is stale against the runner; the cell's pointer resolves but its content no longer describes the runner's scratch default) · section text: "§7 the regression mode". Confirmed — `git show 02ec217c:corpus/knowledge/operator-runbook.md | sed -n '349,351p'` → "Default scratch is a fresh `/mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, removed on PASS unless …" with no TMPDIR clause; the reader's `:25` shows runner `:149-150` honours TMPDIR.
3. `:18` — quote "the map's `one row per gate measured so far` premise is false at CAND" · class **false** · section text: "one row per gate measured so far — suite, rate + composition, survivors, last sweep + pin (eight rows; the round-26 ninth case has no row yet)". Confirmed at read_rev — ledger blob is identical at base and read_rev (`git rev-parse 02ec217c:corpus/knowledge/fleet-kill-rate-ledger.md 9962033fd7a75aa2f2847e979dd687a5d28505a1:corpus/knowledge/fleet-kill-rate-ledger.md` → `bd6aae4e8d4afed21b2645dcb0e35af7b1648e33` twice), its only `drift-pins` row is `:119` "unmeasured by sweep; hermetic", and the round-8 supersession note at `:280` does not cover drift-pins.
4. `:24` — quote "The map's `nine since round 26` count is stale at CAND (case 10 was added in round 51)." · class **stale-count** · section text: "`corpus/knowledge/mutation-case-*.md` (six at round 11; seven since round 16; eight since round 18; nine since round 26)". Confirmed — `git ls-tree --name-only 02ec217c corpus/knowledge/ | grep -c 'mutation-case-.*\.md$'` → `10`.
5. `:25` — quote "The map's nine-leg endpoint is false at CAND." · class **stale-count** · section text: "six-leg registry at round 11, seven since round 16, eight since round 18, nine since round 26" (the `tools/mutate-and-run.sh` cell). Same instrument, separate cell — the cell must be corrected separately, so it is a separate record from finding 4.
6. `:26` — quote "so the universal `addenda ... same shape` gloss is not demonstrated by this new entry" · class **unsupported** · section text: "round addenda append further tables of the same shape". The reader does not call the note absent; it reports the round-51 admission row does not carry the `Note | Holds | Sources` header shape — `git show 02ec217c:corpus/README.md | sed -n '630,634p'` → `## Round 51 — tenth recorded mutation case (depth)` with header `| Entry / ground | Admission and exact scope | Evidence |`. Classed **unsupported**, not false: the premise is undemonstrated, not refuted.

Excluded, per the item's rule: the reader's "holds" verdicts on the other pointer rows; its note that the runbook's six-case presentation "is historical" (`:16`) — a disclosed/historical-accurate note, not a live failure; and its review-note observation that the four panel-tool updates are not pointers in this section (`:48-50`).

## Self-check (frozen rule `.ufo/evidence/round-52/c2/measure.py:82` `check_findings`, whitespace-collapsed substring)

Command (`python3 -` heredoc, run in the lane; imports the frozen module and applies its own function to the delivered record):

```
check_findings -> None
count==findings -> True 6 6
reader_file path check -> True
heading present in ledger r51 entries -> True
len= 96 line=16  in_flat=True class=stale-count   map says the lane held nine cases since
len=115 line=16  in_flat=True class=stale-pointer runbook §7 says default scratch is `mkte
len= 69 line=18  in_flat=True class=false         the map's `one row per gate measured so
len= 87 line=24  in_flat=True class=stale-count   The map's `nine since round 26` count is
len= 45 line=25  in_flat=True class=stale-count   The map's nine-leg endpoint is false at
len= 85 line=26  in_flat=True class=unsupported   so the universal `addenda ... same shape
```

`check_findings` returning `None` means: every quote is at least 20 characters after whitespace collapse and is a verbatim substring of the reader file; the record's `wrong_expectations` equals `len(findings)`; `reader_file` equals `.ufo/evidence/round-51/coldread/reads/T51W2Read13.md`; and `heading`+`read_rev`+`reader` select exactly one round-51 re-key entry. No floors apply to this seat (`FLOORS` names only `T51W2Read20` and `T51W2Read01`).

All six `skill_statement` strings were also checked as substrings of the section blob at read_rev (all `True`).

## Touched surfaces

- Written: `.ufo/waves/round-52/w1/T52W1Corr13.json`, `.ufo/waves/round-52/w1/T52W1Corr13.md`.
- Read only: `.ufo/evidence/round-52/contract.json`, `.ufo/evidence/round-52/c2/measure.py`, `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-51/coldread/reads/T51W2Read13.md`, `.ufo/evidence/round-51/coldread/refresh.py`, `corpus/lessons/round-51-verifier-spotcheck.md`, and blobs at `02ec217c…` (`SKILL.md`, `tools/mutate-and-run.sh`, `corpus/knowledge/fleet-kill-rate-ledger.md`, `corpus/knowledge/operator-runbook.md`, `corpus/README.md`).
- No tool installs (nothing was needed; no pacman, no network fetch). No scratch directory was created — no fixture, clone or counter run was required, so nothing to delete.

## Out of scope here

- The ledger's top-level `corrections` list does not exist yet at base (`'corrections' in ledger` → False as of this read); m4 reads `.ufo/evidence/round-21/coldread/ledger.json`'s top-level `corrections` at REV and wants exactly one record per round-51 re-key entry, so this JSON is a wave-1 input for whoever assembles the ledger list. m4, C2 and the deciding run were **not** run by this seat; the `check_findings` invocation above is the frozen quote rule applied to one record, not a claim verdict.
- The other 19 round-51 re-key records; SKILL.md edits; the kill-rate-ledger supersession line (m5); wave-2 re-keys (m6).

## Summary

1. Delivered `.ufo/waves/round-52/w1/T52W1Corr13.json` for `### The map — where a reader enters, artifact by artifact` @ `02ec217c…`, reader `T51W2Read13`, `wrong_expectations: 6`.
2. Six recorded failures: three stale-count cells (runbook nine cases; mutation-case glob; runner leg registry), one false premise (kill-rate ledger "one row per gate"), one stale cited detail (runbook §7 `/tmp` scratch vs runner TMPDIR), one unsupported premise (README addenda "same shape").
3. Each quote is byte-exact from one reader line (`:16`, `:18`, `:24`, `:25`, `:26`) and passes the frozen `check_findings` (→ `None`); count equals `len(findings)`.
4. All six `skill_statement` quotes verified as substrings of `SKILL.md:1380-1395` at read_rev.
5. Each reader claim was spot-checked at read_rev (runner `:84` "r51 ten", 10 `mutation-case-*` files, ledger blob `bd6aae4e…` unchanged with only `:119` drift-pins row, runbook `:349-351` `/tmp` default, README `:630-634` header triple).
6. Root of the `0`: `.ufo/evidence/round-51/coldread/refresh.py:227` writes `wrong_expectations: 0` from code (routed defect 3, lesson `:128`).
7. Blockers: none. The ledger's `corrections` list is still absent at base, so m4 assembly is someone else's step.
8. Out of scope: C2/m4/deciding-run execution, SKILL.md edits, m5, wave-2 re-keys.
