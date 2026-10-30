# T57W3Read05: cold-read certification

Heading: `### The service's limits — what tameshi refuses to mutation-test`

Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`. Frozen round-18 sectionizer: lines 1282–1311, SHA-256 `7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6`.

Axes: calibration, pointer correctness, refusal-policy agreement, lane non-mutation.

## Finding (low)

**SKILL.md:1299–1303: page-relative citations for rows b, c and f point to the wrong content.** Row b's `:824-828` is the service introduction and `:851-855` is the no-edit clause/protocol heading, not hermetic-suite or SETUP/control requirements. Row c's `:834-836` is the contract heading/start of the pin item, not the never-edit/repair/re-pin clause. Row f's `:890-892` covers hermetic/read-only bounds, not sensitivity versus truth.

Command: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read05-receipts/audit.py` (exit 0, detached scratch clone).

Output excerpts:
```text
ANCHOR SKILL.md:824-828 exists
824: Rounds 2–5 measured three fleet gates at tameshi's hand; round 6 turns the
ANCHOR SKILL.md:851-855 exists
851: 4. Nothing else. The service never edits, repairs or re-pins the gate; a
855: ### The protocol — ordered, fail-closed
ANCHOR SKILL.md:834-836 exists
834: ### The opt-in contract — what the lane brings
836: 1. **A pinned revision** — committed bytes of the gate with sha256, size, line
ANCHOR SKILL.md:890-892 exists
890: - **Hermetic suites only** — no substrate-drift claim; results are
892: - **Read-only** — target sha before = after (`MUTATE_RESTORE`); the tool emits no tree-clean check, so porcelain-clean is an opt-in precondition at open (SKILL.md:819-820).
```

Correct C0b locations: b `841-845`, `868-872`; c `851-853` (re-pin context `840`); f `907-909`. The refusal statements remain true and agree with the detail note. Correction is deferred to round 58; no SKILL edit staged.

## Executed sweep

- Imported the frozen `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py`, read `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md`, called `m.sectionize(raw)`, and printed the matching section's start/end/hash above.
- `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read05 clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r57/T57W3Read05/clone`; asserted the clone's Git top-level before `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read05/clone checkout --detach adf87899c70d616140a81185a8f9acbbdfb30392`. Output: `HEAD is now at adf87899 ...`.
- `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read05-receipts/audit.py`: exit 0. Full command/output: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read05-receipts/audit.py` and `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read05-receipts/audit.out`. The audit prints the complete section, 17 cited anchor ranges, corrected page-relative ranges, matching a–j row IDs, and literal name-search results. Output: `CLONE_SKILL_MATCH true`, `CADENCE_NAMES_SERVICE_LIMITS False`, `LEDGER_NAMES_SERVICE_LIMITS False`, `PAGE_ROW_IDS a,b,c,d,e,f,g,h,i,j`, `NOTE_ROW_IDS a,b,c,d,e,f,g,h,i,j`.
- End-to-end reader inspection covered the refusal detail table, protocol anchors, province boundaries, census queue, ledger anchors, and cadence span. All direct file pointers exist. No runnable command appears in the assigned section.

## Residual risk / gaps

`xd://lsp` returned `No such tool`; name searches are literal fallback, not semantic proof. No mutation sweep or unrelated runtime/resume/routing certification was performed. Dated measurements were read as historical, not rerun as present claims. No tool installation, monitored-content edit, or frozen-evidence edit occurred. Scratch clone is removed after recording evidence; recreate with the commands above to replay.

Verdict: **gap-minor** (citation-only defect).

Self-evaluation: accuracy 4 (literal fallback, no LSP); completeness 4 (policy inspection, not an unrelated mutation run); clarity 4 (full output separated into receipt); actionability 5 (exact replacements and reproducible audit); conciseness 4 (machine report repeats full evidence). Overall 4.2. Highest-impact improvement: stable heading-based citations in round 58. User-facing judgment remains L1's.
