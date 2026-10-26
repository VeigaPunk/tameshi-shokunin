# T48A2CritAssimilationNone — critic, `Assimilation: none` (round 48, attempt 2)

Item attacked: `corpus/lessons/round-48.md:8-9` — "Assimilation: none (`.ufo/waves/round-48/w1/T48ScoutPackage.md`: every staged
row touching the four C2 documents is already held or adopted)" — plus the package recommendation it cites (`T48ScoutPackage.md:5`,
reasons 1-4) and the C2 reject block it rests on (`round-48.md:91-96`). Read-only; no counter executed; no tool installed; no scratch
directory created (nothing left on disk).

## Verdict

**The decision is defensible; the stated ground is not fully honest.**

- The decision (adopt nothing this round) survives the strongest counterexample I could build: neither C1 nor C2 needs package
  material, and 30 of the 35 unheld F3-ground entries are own-work rows whose sources are lane receipts absent from this lane.
- The ground is (a) **C2-only**, so it cannot carry the C1 half of the decision; (b) **not backed by its own table** at the granularity
  it is written in (two staged rows on S026's document are "not adopted" per that table; two more are not in the table at all); and
  (c) the C2 reject cites **`CORPUS.md` rule 2, which does not say "dedupe by document"**.
- A theme that fits C1 (flaky classification / environment-scoped verdict) was **skipped with no stated reason**, and the skip had a
  real but unrecorded reason (unresolvable provenance). Per the item, that is a finding, not a failure.

Nothing here touches a row, a counter, a predicate or a lane file: no duplicate authority, no identity change, no false provenance in
the committed tree. This is a two-line statement fix, not a design defect the canonical judge must reject.

## Artifacts read (sha256 prefixes, bytes)

| artifact | sha256 | bytes/lines |
|---|---|---|
| `corpus/lessons/round-48.md` | `a6d5fd94e0933610` | 382 lines |
| `.ufo/waves/round-48/w1/T48ScoutPackage.md` | `b0931f2031fc22ff` | 71 lines |
| `/home/vgpnk/Projects/shokuknow/merge/tameshi/MERGE-REPORT.md` | `c1094af5d9f741d0` | 86 entries, 103 rows |
| `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` | `5afe1810a6c3d62f` | 375 lines |
| staged `japanese-flaky-verdict-and-environment.md` | `f14dfc29e0126259` | 106 lines |
| staged `r12-flaky-mitigation-and-quarantine.md` | `74a3a21babe75d25` | 58 lines |
| `/home/vgpnk/Projects/shokunin/CORPUS.md` (fleet, read-only) | — | rules 1-6 at `:110-130` |

No counter was run in any mode. The lane, its jj state and its Git index were not written.

## The tameshi quarantine slice (asked by the item)

Derived from `absent-defect-register.md`, data rows whose lane cell is `tameshi` — the file has two tables, `payload-absent` and
`unreachable`; the slice is both:

- **14 `payload-absent`** (`:215-228`): S105, S109, S110, S118, S119, S124, S126, S129, S131, S132, S137, S140, S141, S143 — matches the
  by-lane total at `:240` (`| \`tameshi\` | 14 |`).
- **3 `unreachable`** (`:363-365`): S113, S123, S134.
- **17 rows total**, all `payload-absent`/unreachable, none of any other class.

**Does any slice row concern S026, S048, S093 or S108? No — by id and by document.** The cited sources are opengroup.org (S105),
doi 10.21105/joss.01891 (S109), mir.cs.illinois.edu Lam NDOD (S110), zenn.dev (S118), Purdue/Delta (S119), `github.com/VeigaPunk/
tameshi-shokunin` (S124, S126, S131, S132, S137, S140, S141, S143), t.kyoto-u.ac.jp (S129), doi 10.1145/3540250.3558911 (S113),
doi 10.1109/TSE.2026.3685588 (S123), doi 10.1145/351240.351266 (S134). None is the Google blog, pitest.org, bubblewrap or the TFF
zh-cn page.

Two join facts a consumer of this slice must know (both are register-side defects, not lane defects):

1. **The slice cannot be consumed by id.** Only 2 of the 17 ids resolve to a registry row in the lane:
   `grep -c -E '^\| S105 ' corpus/SOURCES.md` → 1, `S132` → 1; every other id (`S109 S110 S113 S118 S119 S123 S124 S126 S129 S131
   S134 S137 S140 S141 S143`) → 0. The register's ids are the campaign-era tameshi numbering, not the lane's post-merge registry
   (`T48ScoutPackage.md:46` lists the lane's id ranges: S001-S037, S040-S097, S099-S108, S132, S152-S160, S256-S264).
2. **The one slice row on this round's C1 axis is already discharged, and the slice is silent about it.** S110's quote (`one can use
   ≤ 5 reruns … ≥ 82% of the time`) is the same sentence the lane holds at `corpus/knowledge/flaky-aware-verdict-evidence.md:30`,
   sourced to **S262** on the identical URL (`corpus/SOURCES.md:137`, `mir.cs.illinois.edu/marinov/publications/
   LamETAL20ManyFlakyTestsAreNDOD.pdf`) with a committed camera-ready snapshot. So the slice's only flaky-classification row was
   re-anchored in rounds 46-47; the slice predates that fix and cannot be used to argue against mining more F3 rows.
   And S123's DOI (`10.1109/TSE.2026.3685588`) is exactly the paper behind the C1-fitting staged entry in finding A3 below.

So the slice supplies **no** reason to reject assimilation and **no** row concerning the four C2 documents.

## Findings

Ordered by strength. Each names what it attacks, the evidence with `file:line`, and the exact command that shows it.

### A1 — the header's parenthetical is not what the scout's own table says (C2 axis; attacks the honesty of the stated ground)

`corpus/lessons/round-48.md:8-9` states "every staged row touching the four C2 documents is already **held or adopted**". The scout's
table says otherwise for two of those rows, in its own words:

`T48ScoutPackage.md:31` — S212 (S026 feed list): "**S216 is already adopted as lane S260** … **S212 is a second row for the same
document with a different carrier: not adopted**".
`T48ScoutPackage.md:34` — S210 (S108 zh-cn archive carrier): "**S209 held (S107). S210 not adopted**".

The sentence is true only under a *document-level* reading ("the lane holds a row for that document"), and under that reading it is
vacuous: it would be just as true if the lane held nothing of the staged row's claim. The lesson also narrowed the scout's own wording
("every staged row **or entry**", `T48ScoutPackage.md:7`) to "every staged row", dropping entries — where the decision actually bites —
without recording why. The two-line C2 reject at `:91-96` does give the substantive reason for S212/S210 (same document, alternative
carrier); the header does not, and the header is the sentence a reader lands on.

```sh
sed -n '8,9p' corpus/lessons/round-48.md
sed -n '31p;34p' .ufo/waves/round-48/w1/T48ScoutPackage.md
```

Smallest safe correction: replace the parenthetical with the checkable row-level claim the Reject block already supports, e.g.
"Assimilation: none — C1 and C2 need no package material (`.ufo/waves/round-48/w1/T48ScoutPackage.md:5`); the staged rows for the four
C2 documents are same-document carriers of held rows (S212/S210 alt carriers; S225/S229 the S026 feed held as S260) and are rejected at
`:91-96`". Cost: one sentence, no counted surface.

### A2 — the S026 table misses two staged rows that cite the identical carrier (C2 axis)

The package's S026 table (`T48ScoutPackage.md:31`) enumerates S212, S216, `r10-blog-carrier-reachability`, `r13-flaky-false-red-rate`,
`r9-false-red-rate`, `r13-f7-cadence-and-floor`. It omits two entries whose `source:` is the **same per-post feed URL the lane holds as
S260**:

- `r11-flaky-definition-and-carrier.md:2` → `source: S225 - https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json`
- `r12-flaky-mitigation-and-quarantine.md:2` → `source: S229 - https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json`

Neither is in `corpus/knowledge/` (`ls corpus/knowledge | grep -c 'r11-flaky-definition-and-carrier\|r12-flaky-mitigation-and-quarantine'`
→ 0). Mapping command (staged entries → source rows → the four documents):

```sh
cd /home/vgpnk/Projects/shokuknow/merge/tameshi && python3 - <<'EOF'
import re,os
row={}
for l in open('SOURCES.append.md',encoding='utf-8',errors='replace'):
    m=re.match(r'\|\s*(S\d{3})\s*\|(.*)',l)
    if m: row[m.group(1)]=m.group(2)
for d in ['knowledge/corpus/knowledge','amendments/corpus/knowledge']:
    for f in sorted(os.listdir(d)):
        t=open(os.path.join(d,f),encoding='utf-8',errors='replace').read()
        hits=[i for i in set(re.findall(r'^source:\s*(S\d{3})',t,re.M))
              if 'feeds/posts/default/6277555988217606236' in row.get(i,'')]
        if hits: print(f, sorted(hits))
EOF
```

Output: `r10-blog-carrier-reachability.md ['S216']`, `r11-flaky-definition-and-carrier.md ['S225']`,
`r12-flaky-mitigation-and-quarantine.md ['S229']`, `r13-flaky-false-red-rate.md ['S235']`.

Substance check (this is what keeps the finding a ground defect, not a decision defect): the *aspects* those two entries carry are
already held — the 16%/mitigation-menu reading is in `corpus/knowledge/r9-false-red-rate.md:14` and the lane explicitly declines to
transfer the mechanisms at `:38` ("The post's mitigation strategies are reported, not adopted: no claim is made that quarantine,
declared-flaky flags or automatic reruns transfer to this lane's corpus"). So the *outcome* (adopt nothing for S026) survives; the
completeness claim in `T48ScoutPackage.md:7` and the header do not.

Smallest safe correction: add S225/S229 to the `:31` table with the holding entry named (`r9-false-red-rate.md:14,38`), and keep the
reject.

### A3 — a C1-fitting theme was skipped with **no stated reason**, and the skip's real reason is unrecorded (C1 axis) — the item's core question

`japanese-flaky-verdict-and-environment.md` (staged; MERGE-REPORT lists it twice, `:37` r13 amendment and `:38` r2 folded):

- `:5` — `ground: F3 (determinism precondition, flaky-aware verdicts) - a flaky verdict is valid only for the project, and the
  environment, it was measured in`. That is C1's value-class rationale stated by an external source: a verdict's class depends on the
  profile it was observed under, which is exactly what a `stable`/`nondeterministic` class plus a deps set is for.
- `:66` — the folded r2 half's claim: "A flaky rate is a property of the environment and of the project, not of the test" (S169's
  environment-only 5.5x spread, S171's cross-project scope).
- Not held: `ls corpus/knowledge | grep -c 'japanese-flaky'` → **0**; the lane holds neither id —
  `grep -c '10.1109/TSE.2026.3685588' corpus/SOURCES.md` → 0, `grep -c '2602.09311'` → 0.
- Not named anywhere in the scout package: `grep -c 'japanese-flaky-verdict-and-environment' .ufo/waves/round-48/w1/T48ScoutPackage.md`
  → 0. Its only possible shelter is the theme row at `T48ScoutPackage.md:19` ("CJK / Japanese literature (r1, r2, r3, r7, r16)"), whose
  verdict cell gives a reason for **S202/S203 only** and groups by language, not by claim axis — which is how an F3-ground entry ends up
  judged "off-axis" without ever being judged.
- It is **not** covered by the own-work group reason ("staged rows cite `lanes/tameshi/roundN/evidence/*` receipts that are not in this
  lane", `T48ScoutPackage.md:21`): its primary source is an external arXiv record (S237) with a one-command recheck
  (`aaron papers fetch 10.48550/arXiv.2602.09311`).

And the skip had a real reason the round never records — the entry is **not adoptable as filed**:

- `:11-12` — "This entry already existed in the lane's corpus, citing the JUSE workshop paper (S121) and the staged row S123."
  The lane has no such entry (0 files) and **neither id resolves in either registry**:
  `for id in S121 S123; do grep -c -E "^\| $id " corpus/SOURCES.md; grep -c -E "^\| $id " merge/tameshi/SOURCES.append.md; done` → `0 0`
  four times. Adopting it verbatim would create a file asserting a pre-existing corpus entry and citing two unopened rows.
- It is also the reachable re-anchor of a document the register classes `unreachable` (`absent-defect-register.md:364`, tameshi S123,
  doi 10.1109/TSE.2026.3685588) — a C2-type re-anchoring sitting inside a C1-type claim.

Smallest safe correction: one row in the Gate's reject list (beside `:91`), naming the entry and the reason —
"`japanese-flaky-verdict-and-environment.md` refused: its r2 folded passage asserts a pre-existing lane entry and cites S121/S123, which
resolve in neither registry (`grep -c -E '^\| S121 ' corpus/SOURCES.md` → 0); flip: a staged copy that names only S169/S171/S237 and
drops the 'already existed' clause." Cost: one table row; keeps `Assimilation: none` and makes it checkable.

### A4 — the C2 reject cites a rule that does not say what it is cited for (C2 axis)

`corpus/lessons/round-48.md:93` — "dedupe by document, CORPUS.md rule 2: a correction is a new row that supersedes, never a second
copy". The rule, at the fleet root (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`):

```
2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change
   is logged old→new in the round lesson. A correction is a new row whose `teaches` opens
   `supersedes S0NN —`.
```

Rule 2 governs corrections and append-only edits; it says nothing about one row per document. Rule 1, immediately above
(`CORPUS.md:112-115`), says the opposite of document dedupe: "**A row is a claim.** Wrap it only after opening the source in the round
that writes the row." The lane's own entry reads rule 2 the same way the fleet writes it — `corpus/knowledge/r44-anchor-refresh-rule.md:9`:
"`CORPUS.md`'s SOURCES.md rule 2 makes the registry append-only … A stale `anchor` cell … is therefore repaired by a **new supersede
[row]**". And the package itself warns against the shortcut: `MERGE-REPORT.md:116` — "A page often supports several distinct claims, so
this is not automatically a duplicate".

Impact: the stated reason for rejecting S212/S210/S225/S229 is not the reason cited. The *decision* still stands on a better ground
(the specific claim is held by a named entry: S229's aspect at `r9-false-red-rate.md:14,38`; S212's at the same entry; S216 already lane
S260), but "dedupe by document" is a policy the corpus does not carry, and a later round could cite `round-48.md:93` as precedent for
collapsing two claims into one document.

Smallest safe correction: at `:93`, cite rule 1 and the holding entry per row ("S229's mitigation/quarantine claim is held by
`r9-false-red-rate.md:14,38`"), not rule 2.

### A5 — a group reason applied to entries it is false for (C1/C2 axis, low)

`T48ScoutPackage.md:21` puts every r2, r4-r7, r9-r15 entry in one bucket with one reason: "Staged rows cite `lanes/tameshi/roundN/
evidence/*` receipts that are not in this lane". Three unheld F3/F7 entries carry **external** primary sources and are therefore
adoptable without any lane receipt:

- `r11-flaky-definition-and-carrier.md:2` → S225, an external feed URL (the S026 carrier).
- `r12-flaky-mitigation-and-quarantine.md:2` → S229, the same external feed URL (single source; nothing else to stage).
- `r14-quarantine-threshold-is-a-policy.md` → S241 `testing.googleblog.com/2017/04/`, S243 qam-hub, S244 flakyguard, plus one lane
  receipt (S242). Three of four sources are external.

The reason is also **incomplete in scope**: r8 is excluded from the list "(r2, r4–r7, r9–r15)", yet `r8-width-sweep-and-race.md:5`
(`ground: F5 … and F3`) states the single most C1-relevant own finding in the package — "The lane's own classification was a coin flip,
and the leaking token is a git commit SHA" (title) — and it appears nowhere in the scout. Its source is a lane receipt (S208), so the
group reason would cover it if the enumeration had said r8.

Smallest safe correction: change the group cell to list the rounds as "r2, r4-r15 (all)" and add the exception clause for entries whose
`sources:` are external URLs (S225, S229, S241/S243/S244) — their refusal must rest on the claim being off-axis or already held, not on a
missing receipt.

### A6 — what the decision has on its side (not a finding; recorded so the correction is minimal)

- C1 needs no package material: the 22 statements are the lane's own, restated from the counter's own observation (amendment 4 forbids
  package material as attestation anyway: `.ufo/evidence/round-48/contract.json` amendment 4, "Committed files under
  `.ufo/evidence/round-48/calibration/observations/` are evidence for the report only, never attestation").
- C2's craft is already held: `corpus/knowledge/r44-anchor-refresh-rule.md` (anchor refresh by supersede row) and
  `corpus/knowledge/repeated-control-precondition.md` exist; the S026 carrier defect is documented in the lane
  (`r9-false-red-rate.md:3` rechecks through the feed URL, digest pinned).
- The staged C2 documents' absence claims verify: `grep -ci bwrap merge/tameshi/SOURCES.append.md` → 0;
  `grep -ci 'quickstart/incremental'` → 0.

## Coverage numbers (so the claim can be re-derived)

| quantity | value | command |
|---|---|---|
| staged entries (files) | 81 (+4 amendment files whose targets are all held) | `ls merge/tameshi/knowledge/corpus/knowledge/*.md \| wc -l` |
| named anywhere in `T48ScoutPackage.md` | 23 | name-substring scan per entry |
| **unnamed** | **58** | same |
| entries with `ground:` F3/flaky/determinism | 41 | `ground:` scan |
| of those, held in `corpus/knowledge/` | 6 | basename scan |
| of those, unheld | 35 | — |
| of those unheld, unnamed | 28 | — |
| entries whose staged row's document is a C2 target | 5 (r10-blog-carrier, r11-flaky-definition, r12-flaky-mitigation, r13-flaky-false-red-rate, r9-false-red-rate[held]) | python map above |
| named in the S026 table | 3 of 5 | `T48ScoutPackage.md:31` |

So the scout accounts for the package by **23 named entries + group labels**; the header then converts that into one row-level C2
sentence. The gap is not a large omission in volume — it is one C1-fitting theme (A3) and one carrier-table omission (A2) that the record
does not state.

## Is this fixable, or a tradeoff the judge must reject?

- **Fixable, statement-level.** A1, A3 and A4 are edits to `corpus/lessons/round-48.md:8-9`, the Gate's reject list and one reason cell
  — no counted surface, no row, no predicate, no control. A2/A5 are one-row corrections to the wave-1 scout package, which is a report,
  not a counted surface.
- **Not a tradeoff to reject the round for**: no counter reads the assimilation sentence (C1 reads `SCORECARD.md` rows; C2 reads Gate
  lines, snapshots and receipts — verified by reading `contract.json` amendments 1-10; none names a package artifact), the four new rows
  S265-S268 are not affected, and no lane file claims an adopted entry it does not hold.
- **What would make it a verdict-level defect**: if `Assimilation: none` were later cited as proof that the package's C1 material was
  assessed and found off-axis. On this record it was not assessed; it was grouped by language (A3) and by round range (A5).

## Bounds kept

Read-only on the lane checkout: I wrote only this report. Nothing written in `/home/vgpnk/Projects/shokunin` (fleet) or
`/home/vgpnk/Projects/shokuknow`; no mutating git/jj command; `corpus/`, `tools/`, `SCORECARD.md` untouched; the deciding run's
cleanliness check is unaffected. No counter run in any mode; no network fetch; no tool installed or upgraded; no scratch directory was
created, so none is left on disk.
