# T49SecMap — C1 section critic, `### The map` (SKILL.md:1380-1395 @ base `8ca67421`)

Scope: the section's self-assessment **beyond its line pointers** (pointer readers own those). Every
number, count, status sentence, command/file name and claim about what the lane holds got a verdict at
base. Deliverable: `T49SecMap.findings.json` (15 findings: 6 false, 9 true, 0 unverifiable).
Run as `--selftest` only; nothing here is a counter run or a verdict on C1.

## False (report order: falsities first)

### 1. `SKILL.md:1393` — completion pack "this wave, uncommitted at this write" (stale status)
Statement: "the completion pack (`plans/completion-evidence.md`, this wave, uncommitted at this write)
collects the per-round lines and debts".
At base the pack is **committed**, and has been since the round-11 closeout:

```
$ git cat-file -e 8ca67421:plans/completion-evidence.md; echo rc=$?     -> rc=0
$ git log --diff-filter=A --format='%h %s' -- plans/completion-evidence.md
284ab0f probation round 11 (training r10, FINAL): closeout — the 10-round arc complete; see closeout-r11.md + completion-evidence.md
$ git log --oneline --follow -- plans/completion-evidence.md           -> cd31c6b (last touch, fleet round 1); 284ab0f
```

The content half is true (`plans/completion-evidence.md:24` "## One line per round"; `:68` "## Debts";
189 lines). Fix: replace the status clause with "committed in the round-11 closeout"; keeps the
`plans/completion-evidence.md` pointer, adds none.

### 2. `SKILL.md:1385` — ledger "one row per gate" (8 rows, 9 measured gates)
```
$ git ls-tree -r --name-only 8ca67421 | grep -c 'corpus/knowledge/mutation-case-'      -> 9
$ git show 8ca67421:corpus/knowledge/fleet-kill-rate-ledger.md | grep -n '^## '
41:## 1. Measured — the four fleet sweeps      (rows :45-48)
   ER-2 blocks                                  (rows 5-6)
403:## Round 16 — seventh row appended
424:## Round 18 — eighth row appended            (no ninth heading)
$ git show 8ca67421:corpus/knowledge/fleet-kill-rate-ledger.md | grep -n '5/10'
410: round-gate   432: sources-check            (nothing for cite-check)
```
The round-26 ninth case records a measured **5/10** (`corpus/knowledge/mutation-case-kumitate-cite-check.md:44`)
and says the gap itself: "The standing ledger `fleet-kill-rate-ledger.md` still lists cite-check as a
four-defect probe (1/4) … The ledger file is not edited this round" (`:123-126`). So the cell's "one row
per gate" is false by one gate. **Preferred repair is substantive, not textual**: append the round-26 row
to the ledger; the cell then needs no edit. The JSON's `proposed_fix` is the fallback cell edit
("eight rows; the round-26 ninth case has no row yet").

### 3. `SKILL.md:1385` — "before quoting any rate — the row is the standing receipt" (same root)
`git show 8ca67421:corpus/knowledge/fleet-kill-rate-ledger.md | grep -n -i 'cite-check'` -> `:94` (round-6
probe 1/4), `:107` (queue row "probe only"); `grep -n 'round 26' <ledger>` -> no match. A reader quoting
the round-26 rate finds no standing row. `proposed_fix: null` — the ledger append proposed in #2 repairs
both cells; two independent text edits would be churn.

### 4. `SKILL.md:1387` — protocol holds "…, report shape, boundaries" (mislists the file)
```
$ git show 8ca67421:corpus/knowledge/service-optin-protocol.md | grep -n '^## '
54 §1 Request shape · 109 §2 Read-only guarantees · 142 §3 Owner-hardens discipline · 182 §4 Report shape
$ git show 8ca67421:corpus/knowledge/service-optin-protocol.md | grep -n -i boundar
168: 'a harness boundary'   177: 'harden the boundary classes'      (class terms, no held section)
```
"Boundaries" names no section or clause; **§3 owner-hardens is omitted**, and the lane's own artifact
table lists it as one of the protocol's four holds (`corpus/knowledge/service-standing-state.md:56`:
"request shape (§1), guarantees (§2), owner-hardens (§3), report shape (§4)"). Fix names the four holds
and keeps the re-pin rule (§1.1, `:60-63`).

### 5. `SKILL.md:1390` — case notes "reproduce sections" (3 of 9 have none)
```
$ for f in $(git ls-tree -r --name-only 8ca67421 | grep 'corpus/knowledge/mutation-case-'); do \
    git show 8ca67421:$f | grep -c -i '^## .*reproduce'; done
kagi-census 1 · kagi-checklist 1 · kimi-census 1 · kumitate-claims 1 · mado-verify 1 · tsukuroi-census 1
kumitate-round-gate 0 · kumitate-sources-check 0 · kumitate-cite-check 0
$ git show 8ca67421:corpus/knowledge/mutation-case-kumitate-cite-check.md | grep -n '^## '
15 §0 · 33 §1 Pre-registration · 44 §2 Result · 67 §3 · 85 §4 Survivors · 112 §5 Limits   (ends there)
```
The three round-16/18/26 notes carry pre-registration + a committed spec instead. Fix qualifies the cell;
the `mutation-case-*.md` glob pointer is untouched.

### 6. `SKILL.md:1392` — README "one row per note, holds + sources" (63 rows / 58 notes)
```
$ # parse every '| `note`' row of git show 8ca67421:corpus/README.md, diff against corpus/knowledge/*.md
rows 63 · distinct targets 58 · knowledge note files 58 · with a row 57
without a row: ['knowledge/r44-anchor-refresh-rule.md']
with two rows: gates-survey-kumitate · gates-survey-kagi · verification-patterns-fleet
               witness-scoped-kill-verdict · incremental-pin-disposition
```
Columns are `Note | Holds | Sources` (true), but the map is neither exactly one row per note (five notes
doubled by addenda) nor complete (one knowledge note uncarried). Fix states the shape and the partiality
in prose, adding no path pointer.

## True (verified; two carry a currency flag, not a falsity)

| skill line | statement | evidence |
|---|---|---|
| 1384 | runbook is the entry point (T10-1), §0/§2/§3/§4/§5/§6/§7/§10 named | `grep -n '^## '` on the runbook -> `:35 :93 :131 :180 :243 :269 :345 :462`; header `:1` "(round 10, T10-1)"; §6 reading map `:277`, T1/T2/T3 `:288/:290/:293`; §3 = exactly six rows `:149-154`. **Currency flag**: lane holds nine cases since round 26, so the runbook's six-case ledger is stale as a lane view (fix annotates the cell; preferred repair is updating the runbook) |
| 1385 | "§1–§4 byte-frozen, new rows appended below" | text between `## 1. Measured` and `## 5.` hashes `d2ae445332dd` at **all nine** commits that touch the ledger (`git rev-list --reverse 8ca67421 -- <ledger>` -> 9); appends at `:403`, `:424` below §4 (`:132`); rule stated at `:312` |
| 1386 | service-limits holds "the refusals, detail of record" | §1 decision table `:42`, rows a–j `:46-55`; "Row detail — the measured reasons, verbatim" `:57`; `service-standing-state.md:57` calls it "refusal detail of record". The `:1246-1270` clause is a pointer (readers' scope) |
| 1388 | census holds "the offer and the queue (surveyed-but-unmeasured pins)" | §5 "Tameshi's standing service offer" `:249`, offer `:269`, queue `:277-286`, R.4 `:594`; pins live in §1.1 `:75-84` and §6 `:293-305` — the §5 queue table itself has no pin column, so the parenthetical is right about the file, not the table |
| 1389 | standing-state holds fleet-visible/lane-owned, handoff conditions, SC1–SC3 | §1 `:49`, §2 `:70`, §3 "The handoff conditions" `:80`, SC1 `:159`, SC2 `:174`, SC3 `:181` |
| 1390 | "six at round 11; seven since round 16; eight since round 18; nine since round 26" | `for c in 284ab0f c699c8c 58e5d53 40a12bf 8ca67421; do git ls-tree -r --name-only $c \| grep -c 'corpus/knowledge/mutation-case-'; done` -> `6 7 8 9 9` |
| 1391 | instrument modes, nine-leg registry, git-materialized replay | tool `:83` "r10-2 six legs; r16 seven; r18 eight; r26 nine"; `:108` "All nine defect specs are embedded below"; `:115-120`, `:1209` (`git show > file`, target not read from the fleet tree). Observed: `TMPDIR=<scratch> bash tools/mutate-and-run.sh --selftest` -> `MUTATE_SELFTEST: 106/106 pass` / `VERDICT: PASS` (receipt `T49SecMap.selftest.txt`, scratch clone of lane HEAD `455b2cd`) |
| 1393 | plans/records by convention rounds 4–10; no round-11 record file | `git ls-tree -r --name-only 8ca67421 \| grep '^plans/'` -> plans and record-drafts for 4–10; `grep -i 'round-11'` -> only `plans/round-11.plan.md` (plans for rounds 2, 3, 11 exist as plans only, outside the stated convention, which the parenthetical scopes correctly) |
| 1394 | LOG round rows + SCORECARD move-log rows with counting commands | `SCORECARD.md:7` "## Move log"; row 1 at `:11` carries `git show 40f8e1f:SKILL.md \| wc -l` → 22 etc.; round sections to "## Round 48" `:2320`; `LOG.md:56` carries an executed selftest line, `:49` points at the scorecard commands |

## Notes for the integrator
- The two ledger cells (#2, #3) are one defect: the ledger's missing ninth row. A ledger append is the
  honest fix and would make the frozen pointer set (17 in this section) untouched; if the ledger is left
  alone, the fallback cell text in the JSON is the minimal true statement.
- No proposed fix removes a `file:N` pointer, a backticked path pointer or the heading, and none
  introduces a new pointer (the C1 extractor's per-section count stays 17).
- Runbook currency (#T1) is the same class of defect as #1: a "six-case" figure that the lane outgrew in
  round 26. Fixing the runbook is out of this section's scope; annotating the map cell is the fallback.
- Tooling: nothing installed or upgraded this round (no package, uv/npx or binary change). Scratch
  `/fast/scratch/hyaku/tameshi-r49/T49SecMap/` used for one `--shared` clone and deleted after use.

## Summary
- 15 statements judged in `### The map` (SKILL.md:1380-1395): 6 false, 9 true, 0 unverifiable.
- False: pack "uncommitted at this write" (:1393); ledger "one row per gate" and "the row is the standing receipt" (:1385, ninth case has no row); protocol "boundaries" + missing §3 (:1387); "reproduce sections" (:1390, 3 of 9 notes); README "one row per note" (:1392, 63/58, one note uncarried).
- Strongest: the ledger's missing round-26 row is a live receipt gap, not just stale prose — the round-26 case note states it (`mutation-case-kumitate-cite-check.md:123-126`).
- Second: a stale "uncommitted" status sentence is unreproducible at base — the pack has been committed since round 11 (`284ab0f`).
- Verified with history and counts: mutation-case windows (6/7/8/9), nine-leg registry, instrument selftest (106/106), §1–§4 immutability across all 9 ledger commits.
- Two true statements carry currency flags (runbook six-case ledger; census queue pin placement noted).
- Fixes are minimal cell edits, pointer-safe: no `file:N`/path pointer added or removed.
