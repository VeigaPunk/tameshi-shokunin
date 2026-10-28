# T54W1Read08 — cold read: `### The service's limits — what tameshi refuses to mutation-test`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (absolute paths only; no lane file was edited, no counter, contract, freeze, ledger, registry or wave spec touched).
- Content commit (cand): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- Section at C0: `SKILL.md` lines 1265-1294 (body 1265-1293, 29 lines), `section_sha256` `37d63abf882e89d8103fb2618d8622c78da60aecfac75352851687e42eea7590`
- Frozen re-read set: this heading is item 8 of 23 in `.ufo/evidence/round-54/c1/lost-headings-at-c0.json` (also in `lost-headings-at-base.json`).
- Mode: cold read as an executor with no oral context. Every stated artifact was opened at C0 from git objects (`git -C <lane> show <rev>:<path>`); the working tree was never the source of section bytes. No mutating git command (commit/add/fetch/reset/jj) was run anywhere.

## Reader command and output

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && \
  TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read08 \
  python3 .ufo/waves/round-54/reader-section.py \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    59c38109bf119d0e9d4f878644a82babc937bc1e \
    "### The service's limits — what tameshi refuses to mutation-test"
```

```
{"heading": "### The service's limits \u2014 what tameshi refuses to mutation-test", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1265, "end": 1294, "section_sha256": "37d63abf882e89d8103fb2618d8622c78da60aecfac75352851687e42eea7590"}
```

Independent recompute: the frozen round-18 `sectionize()` (blob of `.ufo/evidence/round-18/measure.py` at C0, loaded via `importlib`) over the C0 `SKILL.md` blob gives the same span (start 1265, end 1294) and the same sha `37d63abf…` over the heading-through-last-non-blank-line body.

## Findings (4)

One defect class with one cause: every **page-local** line anchor in this section is stale at C0. The section's own parenthetical fixes the meaning — "(Anchors `:…` are this page)" — and read at C0 none of `:813-817`, `:823-825`, `:840-844`, `:879-881`, `:1010-1154` lands on the sentence its row or clause paraphrases. Provenance is exact: the section was written 2026-10-14 in the round-9 commit `b8eb96e` ("probation round 9 (training r8)"), and at that commit each cited range is byte-exactly the intended text (checked line-by-line, drift table below); by C0 the same text has moved +11 (the page region the rows cite) and +13/+15 for the cadence span. All note-side anchors (`service-optin-protocol.md`, `fleet-suite-census.md`, `fleet-kill-rate-ledger.md`, `PROVINCE.md`, `service-limits.md`) still resolve and are listed under "Checked and resolving". The fix is line re-derivation, not re-wording.

### F1 — row (b): both page anchors land 11 lines early

Quote (byte-exact in the section):

```
| b | No one-command hermetic suite | refused before any suite runs — the request shape requires it; spec/control failures are `MUTATE: SETUP`, exit 2, no headline | `:813-817`; `:840-844` |
```

Why: at C0 `:813-817` is the round-6 contract paragraph — "the contract it satisfies is the round-6 plan's measure clause (`plans/round-6.plan.md:30-34`: pinned revision, one-command hermetic suite, recommendations-only)" plus the blank line and the `### The opt-in contract — what the lane brings` heading — and `:840-844` is the `tools/mutate-and-run.sh` preamble, the blank line and the opening bash code fence. Neither carries the two rules the row paraphrases: the opt-in contract's item 2 ("**A one-command hermetic suite** invocable against a copy … it must exercise the copy it is handed … print its own executed count and verdict … and read no live path") is now `:824-828`, and "Any spec failure is `MUTATE: SETUP (<reason>)`, exit 2 — no headline" plus the red-control exit-2 rule is now `:851-855`.

What I opened: `SKILL.md`@C0 806-830 (contract paragraph, opt-in contract items 1-2), 838-860 (protocol block, spec/control rules); `SKILL.md`@`b8eb96e` 806-825 and 838-845 (where `:813-817` is exactly item 2 and `:840-844` exactly protocol items 2-3); `corpus/knowledge/service-limits.md`@C0 44-55 and 69-78 — the note's §1 row (b) cites the same `SKILL.md:813-817`, `:840-844` and its §2 verbatim detail pins `:813-817` to "must exercise the copy it is handed…" and `:840-842`/`:843-844` to the spec/red-control rules, the receipt that those numbers were correct when written.

### F2 — row (c): the paraphrase's sentence moved 11 lines down

Quote (byte-exact in the section):

```
| c | A moved substrate without a re-pin | a recommendation, never an edit — the service never edits, repairs or re-pins a gate | `:823-825` |
```

Why: at C0 `:823-825` opens mid-sentence at "moved substrate needs a re-pin, never a re-interpretation of the old table." (the sentence's opening "A" ends `:822`) and then covers the next numbered item, so it does not carry "The service never edits, repairs or re-pins the gate; a needed change is a recommendation to the owner", which is `:834-836`; the meaning-cell is a near-verbatim rendering of those moved lines, and the anchor range's own start is cut mid-sentence — the signature of having been written before 11 lines were inserted above it.

What I opened: `SKILL.md`@C0 818-837; `SKILL.md`@`b8eb96e` 806-826 (where `:823-825` is exactly item 4, "4. Nothing else. The service never edits, repairs or re-pins the gate…"); `service-limits.md`@C0 80-85 (§2 (c) quotes `SKILL.md:823-825` as that sentence).

### F3 — row (f): the page anchor is the kill-rate bullet now

Quote (byte-exact in the section):

```
| f | Product semantics — whether a gate's verdicts are right | never measured — sensitivity ≠ truth | `:879-881`; `fleet-kill-rate-ledger.md:156-158` |
```

Why: at C0 `:879-881` is the "Findings kept, never smoothed" bullet — a low kill rate is a report, mado's 40 % is the first point below the 50-80 band, the reading is composition (4 in-surface + 6 out-of-surface, measured 4/4 and 0/6) — while the rule the row renders, "- **Sensitivity, not truth** — a sweep measures what the suite can detect, never whether the gate's verdicts are right", is `:890-892`; the ledger half of the cell (`fleet-kill-rate-ledger.md:156-158`, "suite sensitivity ≠ gate truth (nothing here measures whether a gate's verdicts about the real world are right)") still resolves, so only the page half is stale.

What I opened: `SKILL.md`@C0 876-893; `SKILL.md`@`b8eb96e` 874-882 (where `:879-881` is exactly the Sensitivity bullet); `fleet-kill-rate-ledger.md`@C0 152-162.

### F4 — the "no cadence … names it" locator no longer matches the cadence section

Quote (byte-exact in the section):

```
(`:1010-1154`, `fleet-kill-rate-ledger.md:285`, `fleet-kill-rate-ledger.md:318`)
```

Why: `:1010-1154` was exactly the round-8 cadence section's span at `b8eb96e` — that file's heading `## The re-sweep cadence and the six-case confidence statement (round 8, measured)` at 1010 and the next `##` (the round-9 section) at 1155 — while at C0 the same section spans `:1023-1169` (headings at 1023 and 1170), so the cited range now opens 13 lines early inside the round-7 ledger-leg list (`:1010` reads "rate is never implied to hold at a later revision than its sweep pin.") and stops 15 lines before the cadence section ends, omitting the six-case bullets at 1155-1169.

What I opened: `SKILL.md`@C0 1005-1026 (the ledger-leg items 5-6 tail the range now starts in, then the cadence heading at 1023), 1140-1170 (the six-case bullets the range now ends inside, the round-9 heading at 1170); `SKILL.md`@`b8eb96e` heading list 1000-1180 (cadence heading 1010, next heading 1155) and lines 1005-1020.

## Drift table (round-9 write `b8eb96e` → C0 `59c3810`)

| cited range | text it was written for | lines at `b8eb96e` | lines at C0 | shift |
|---|---|---|---|---|
| `:813-817` | opt-in contract item 2, "A one-command hermetic suite invocable against a copy…" | 813-817 | 824-828 | +11 |
| `:823-825` | opt-in contract item 4, "The service never edits, repairs or re-pins the gate…" | 823-825 | 834-836 | +11 |
| `:840-844` | protocol items 2-3, "`MUTATE: SETUP (<reason>)`, exit 2 — no headline" + red control | 840-844 | 851-855 | +11 |
| `:879-881` | "**Sensitivity, not truth** — a sweep measures what the suite can detect…" | 879-881 | 890-892 | +11 |
| `:1010-1154` | round-8 cadence section (heading line through the line before the next `##`) | 1010-1154 | 1023-1169 | +13 / +15 |

The shift is not one constant because text was also inserted inside the round-9 section after its write: `### The service's limits — what tameshi refuses to mutation-test` sat at line 1246 at `b8eb96e` and at 1265 at C0 (+19), which is why the sub-section's own body is longer than the cited page region's drift would suggest.

## Checked and resolving (no finding)

- **Row (a)** `service-optin-protocol.md:25-30` — opened @C0 20-35: "The queue (`fleet-suite-census.md:277-286`) is an offer, not a schedule: at round-7 dispatch it drains only under a fresh opt-in naming a pinned target + a hermetic suite … a round with no opt-in records the no-opt-in line as its complete outcome". `fleet-suite-census.md:277-286` — opened @C0 270-292: "Queue (projection, ordered by expected yield — most static protection last):" at 277 and its six-row table through 286. Both resolve.
- **Row (d)** `service-optin-protocol.md:129-132` — opened @C0 125-135: "**No live substrate read.** Hermetic suites by construction; where a probe needs a live-plane branch it is a PATH-level stub, never the session". Resolves.
- **Row (e)** `PROVINCE.md:14-18`, `PROVINCE.md:20` — opened @C0 10-24: 14-18 "**Refuses:** product domains … Never edits a sibling's gate code (read-only probes; recommendations travel in round reports). Credential material (→ kagi), endpoint health (→ kama)."; 20 "**Out of province → report, never absorb.**" Resolves.
- **Row (g)** `fleet-kill-rate-ledger.md:220` (U2) — opened @C0 216-224: "- **U2** — coordinated multi-edit rewrites unmeasured everywhere (matrix §7)." Resolves.
- **Row (h)** `service-optin-protocol.md:267-269` — opened @C0 262-272: U4 "a harness that adjudicates by exit code alone cannot kill the exit-flatten family; a stdout-reading harness is a named future, not a measurement". Resolves.
- **Row (i)** `fleet-kill-rate-ledger.md:35-36` — opened @C0 32-40: "A post-hardening re-run of the same spec is a **directed repair**, not an independent rate; it is recorded as such." Resolves.
- **Row (j)** `service-optin-protocol.md:86-91` — opened @C0 82-95: "**Scratch namespace per lane.** … the mado run saw ≥37 foreign `/tmp/w5-mado-m52-selftest.*` directories, kept exactly its own 8, and removed exactly those paths". Resolves.
- **The note's self-description** `service-limits.md:4-5` — opened @C0 1-23: "Role: the **refusal table the re-sweep cadence / applies at intake**" (the quote crosses the note's own line break). Resolves, and the attribution "(T9-2, round 9)" matches the note header.
- **"carries the same rows as the detail of record"** — opened `service-limits.md`@C0 42-55 (its §1 table): rows a-j, same letters, same refusal topics, and a "Trigger at intake" column at 44; §2 (57-171) holds the verbatim anchor quotes; §3 (172-195) is "The intake precondition — the re-pin rule (checked: present, cited)", which is the "intake-precondition check" the section names. No row-level divergence between the two tables, so the section's own "a divergence between the two is the finding" rule fires nothing.
- **"no cadence or ledger text names it"** — `grep -n "service-limits"` over `SKILL.md`@C0 returns only 1268 and 1274 (this section), 1319 (the round-10 runbook section), 1410 (a registry row), 1483 (an open-items list); none is inside the cadence section. The same grep over `fleet-kill-rate-ledger.md`@C0 returns nothing at all. The claim is true; only its page locator is stale (F4).
- **Table integrity** — header `| # | Refusal | What it means | Anchor |`, separator `|---|---|---|---|`, ten rows a-j, four cells each, no duplicate or missing letter; every row carries at least one anchor, consistent with "a refusal without an anchor is not written".
- **Closing line** "Anchors re-resolved 2026-10-14 on the live bytes; a reader on a differing revision re-resolves rather than trusts" — a dated statement about a past pass, not a contradiction, and it is the instruction under which F1-F4 are re-derived rather than "trusted". Independent corroboration that this section's write-time line cites are known-stale: the standalone note's §7 errata at `service-limits.md`@C0 line 271 records "The round-9 section was **edited in place**, not merely appended: its internal lines shifted. Write-time cites inside that section are therefore superseded" and directs readers to "Cite the round-9 SKILL section by heading, not by line while the round is live".
- **Self-contradiction sweep** — the 29-line body was read twice for pairwise contradiction (role-as-stated vs the page's own assertion; refusals vs adjudication; compact rendering vs detail of record; table vs closing rule). None found. The only mismatch is between the table and the C0 bytes, which is factual and is F1-F4.

## Sweep and method

- Section bytes and every cited artifact were read from git objects: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <rev>:<path>` for `SKILL.md`, `corpus/knowledge/service-limits.md`, `corpus/knowledge/service-optin-protocol.md`, `corpus/knowledge/fleet-suite-census.md`, `corpus/knowledge/fleet-kill-rate-ledger.md`, `PROVINCE.md`. Extraction kept under `/fast/scratch/hyaku/tameshi-r54/T54W1Read08/co/` only.
- Full anchor enumeration of the section: page-local `:1010-1154`, `:813-817`, `:840-844`, `:823-825`, `:879-881`; note-side `service-limits.md:4-5`, `service-optin-protocol.md:25-30`, `fleet-suite-census.md:277-286`, `service-optin-protocol.md:129-132`, `PROVINCE.md:14-18`, `PROVINCE.md:20`, `fleet-kill-rate-ledger.md:156-158`, `fleet-kill-rate-ledger.md:220`, `service-optin-protocol.md:267-269`, `fleet-kill-rate-ledger.md:35-36`, `service-optin-protocol.md:86-91`, plus the prose `fleet-kill-rate-ledger.md:285`, `fleet-kill-rate-ledger.md:318` (the ER-3 / ER-4 headers, opened 281-324 — the cadence policy the negative claim is about).
- Provenance proof of the shift: `git log -S` names `b8eb96e` (round 9, 2026-10-14) as the last writer of the cited passages; in that blob the strings sit at exactly the cited lines — `Sensitivity, not truth` → 879, `MUTATE: SETUP (<reason>)` → 842, `never edits, repairs or re-pins` → 823, `one-command hermetic suite` → 813 — and at C0 at 890, 853, 834, 824.
- Heading scans at both revisions (`awk` over `^#`) fixed the section bounds used above: C0 cadence section 1023-1169; `b8eb96e` cadence section 1010-1154.
- Census conformance (round boundary): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, final line `tameshi\tok\t/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`; 139 registry rows (`| S001` … `| S279`), next unused id S280 as the file states. Output carries duplicate-URL and one tierC warning lines, no failures.
- No fixture and no `-receipts/` directory: this is a read item, and writing one would be an unrequested artifact.
- No tool was installed or upgraded (pacman is paused host-wide; nothing was needed).
- Nothing was written outside the two deliverables. Scratch `/fast/scratch/hyaku/tameshi-r54/T54W1Read08` (including the `mkdtemp` that `reader-section.py` creates under `TMPDIR`) was removed at exit; no file was created under `/tmp`.
- Residual risk: the round-9 write revision is identified by `git log -S` on the four quoted sentences and by the note's own dated errata, not by a round-9 tag; if a later commit re-inserted identical bytes the drift attribution could name a different writer, but the C0 mismatch itself is measured directly and does not depend on the attribution.

COLDREAD T54W1Read08: gap-blocking (4 findings)
