# T57D4Rows6 — documentary review of R55.1 and R55.3

Axes: original-item fidelity; revision/commit identity; base-versus-current status; evidence completeness. Documentary review only; no admission recommendation.

## Findings (severity order)

### High — R55.1 aggregate candidate substitutes a round-56 verdict for the missing round-55 verdict

**Unsupported** in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/attack-ledger.json:1856` (`status=fixed`, `status_at_base=fixed`, commit `18bbdab73b26422e33186076be6be433b3358bc1`). The original item requires the round-55 counter verdict at `4c04c1d3`, or an explicit claim restatement at C0: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-55-verifier-spotcheck.md:118-122`.

Read-only command executed:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 18bbdab73b26422e33186076be6be433b3358bc1:.ufo/evidence/round-56/after/c2.stdout
```

Output ends:

```text
EXPLAIN arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT
EXPLAIN arm5-own exit=0 verdict=PASS
EXPLAIN arm6-docs 4/4
C2_R56: rev=1b44bace0974 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=PASS docs=4/4 total=0 C2_R56_PASS=true
```

This is expressly another round and another revision. It even preserves the missing round-55 verdict as a red arm. Read-only command executed:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:.ufo/evidence/round-55/after/c2.stdout
```

Output contains only 28 EXPLAIN lines, ending `EXPLAIN usable repeat-control --selftest          rc=0  ok`, with no C2_R55 verdict. Existing panel evidence also examines the alternate C0-restatement remedy and finds none: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR5410R551.md:110-142`.

**Writer correction supported:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR551xR553/rows.json:3-14` changes this to open/open without a commit. Its staged ledger has the same correction. The writer independently distinguishes forward prevention from historical repair at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR551xR553.md:63-71`. Do not retain the aggregate candidate's fixed assertion.

### High — R55.3 current fixed status is unsupported at C0b; the base-only panel does not establish current repair

**Supported at base; unsupported as an unqualified current closure.** The writer row (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR551xR553/rows.json:17-29`) sets both statuses fixed and cites `c1dd23b3f83f5dff676c4a4482498e87345375ef`. Original scope requires both the 18-heading re-key and a truthful score restatement: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-55-verifier-spotcheck.md:127-130`.

The panel explicitly judges BASE only, not C0b: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR552R553.md:4,79-137`. It identifies three complementary historical commits: c1dd23b3 (re-key), 2f5512a8 (scorecard restatement), 8c20d5c (predicate case correction). Thus c1dd23b3 is supported as the re-key commit, not as the sole commit implementing both halves.

Read-only commands executed:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --stat c1dd23b3f83f5dff676c4a4482498e87345375ef
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=short --unified=2 2f5512a8ab0771fb2eee463ec16db359174f5edd -- SCORECARD.md
```

Output: c1dd23b3 changes 21 files (ledger, refresh receipt, 18 traces, binder stdout), no SCORECARD. 2f5512a8 adds the standing calibration row `| calibration | 8 | Round-21 cold-read monitor ... 64/64 ... box3=true | c1dd23b3... | 56 |`.

Existing writer measurement receipt, read rather than rerun: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR551xR553-receipts/coldread-monitor.txt:1-18` records command `python3 .ufo/evidence/round-21/coldread/measure.py --repo $S/clone --rev <rev>` and these outputs:

```text
BASE 5e356996...: score=8, sections_covered=64, box3_full_page=true
C0b adf87899...: score=6, sections_covered=46, box3_full_page=false
```

The writer itself says the standing row still asserts 8/64 at C0b and master, then treats the regression as outside the row: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR551xR553.md:131-137`. A counter restriction on status combinations is not semantic evidence that the current defect is fixed. Preserve the supported historical/base verdict, but current closure requires actual deciding-revision repair evidence. Eighteen reader plans alone do not establish it.

## Candidate identity and residual risk

The actual production ledger read contains only the older 49-row corpus, with neither assigned id. Read-only `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- corpus/routed-defects.json` returned no output. Therefore the aggregate candidate and writer-staged correction are reported separately; neither is represented here as integrated production content.

No candidate gate/counter, tests, builds, exploit, or alternate runtime was executed. Historical command output is attributed to existing receipts, not a fresh measurement. No deciding-revision restoration receipt was established in this scoped review; integration remains UNVERIFIED. No tools installed or upgraded. LSP device lookup returned `No such tool: xd://lsp`; literal searches and git-object reads are documentary evidence, not semantic LSP proof. Resume/runtime/saturation invariants are outside these two documentary ledger rows.

Self-evaluation (1–5): accuracy 4 (historical outputs not freshly measured); completeness 4 (deciding revision unavailable in the reviewed evidence); clarity 4 (separate candidate variants necessary); actionability 4 (retain R55.1 correction and demand current R55.3 evidence); conciseness 4 (command evidence retained). Overall 4.0. Highest-impact improvement: bind any later integration claim to its exact revision and existing monitor receipt; not performed here because no code execution or admission is authorized.
