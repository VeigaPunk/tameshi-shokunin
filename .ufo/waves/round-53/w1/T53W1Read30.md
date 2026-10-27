# T53W1Read30 — cold read: `### What stays open — named, never closed by prose`

Lane: tameshi-shokunin · round 53 (hyaku run 10, L1 TameshiR53a2), wave 1 · seat T53W1Read30.
Substrate read: `SKILL.md` at content commit **C\* = `a41195dfc13a73958e4c5228ec196b28d03ded03`** (`SKILL.md` blob `6da7a3a566366e6f3c3345bc5b0c7e1e7388f857`, identical to round-53's fix-pass commit `218bc6b`), read through git objects only — the working tree was never read.

Section per the frozen monitor: heading line **1456**, next heading (outside fences) at 1471, section = lines 1456–1470, trailing whitespace-only lines stripped, joined with `\n`, no trailing newline → **789 bytes**, `sha256 = 6716afc89e85379975438fe58a3ac23288a393fdd0d4058139cf9b1fafb352ff`. The split was reproduced by two independent implementations (fence-aware Python scanner; `git show | awk | sed | awk`) and both agree on the range and the digest.

## Checks run

1. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195df…:SKILL.md` → 2178 lines; fence-aware heading scan → `(1456, '### What stays open — named, never closed by prose')`, next `(1471, '## Promotion-evidence calibration — fleet round-1')`.
2. Section extraction + `sha256` (two implementations) → `6716afc8…` (789 B). Independent run before stripping the trailing blank line gave 790 B / `50bd6cc0…`; after the spec's trailing-blank strip both implementations converge on `6716afc8…`.
3. Every pointer in the section resolved against the C\* bytes: `:1017-1019`, `:1359-1363`, the "above" reference (lines 1447–1448), `service-limits.md` §5, `service-optin-protocol.md` U1–U6, the ledger U-list.
4. Drift attribution: `git diff -U2 7ff81a5 a41195df… -- SKILL.md` (39 insertions / 32 deletions) to test whether a failing pointer was already wrong at round 52 or was shifted by round-53's own fix pass; the same two lines were then read at `7ff81a5:SKILL.md` for comparison.
5. Cross-checks of the registry leg count: `:1363-1364`, `:1368`, `:1398`, and the page's own round-16 repair table at `:1747`.

## Holds (verified at C\*)

- `- **The interval** — the operator's `[U]` (above).` — the "above" target resolves: `:1447-1448` reads "No lane declares a clock interval — the ticks so far are boundary-bound, and the interval is that seat's `[U]`." HOLDS.
- `Whether the operator adopts the schedule — `[U]`, recorded as such.` — `:1446-1447` records the round-11 schedule additions landing in `corpus/knowledge/closeout-r11.md:155-213`. HOLDS as an open `[U]`.
- `The two successor rows (T1 fired again at this read)` — supported by `:1419-1426`: two `stale` cells (`bash-tsukuroi-census`, `bash-mado-verify`) → T1 fired → "successor rows land appended in the ledger (`:1230-1244`) — open at this write". Two cells, two rows. HOLDS.
- `the ledger's U-list` — `corpus/knowledge/fleet-kill-rate-ledger.md` §8 "Unknowns" at that file's line 216, U1–U9 at 218–235 (read at C\*). HOLDS.
- `the protocol's U1–U6` — `corpus/knowledge/service-optin-protocol.md` U1–U6 at that file's lines 259–273 (read at C\*). HOLDS.
- `service-limits.md §5` — `corpus/knowledge/service-limits.md` §5 is "Unknowns" (file line 218, U1 "driver invocation"), the home the section names. HOLDS.
- `Append-only to the last line: nothing above this section was edited by this write` — a claim about the write that introduced the section, not about C\*; later appends below it (round-1, 12, 13 … registries) are consistent with append-only. No command output falsifies it, so it is **not** reported as a finding.
- `the recorded tables stand at their revisions` / `a reader on a differing revision re-resolves rather than trusts` — self-descriptive discipline statements, no pointer to resolve. HOLDS as stated.

## Findings (3)

### F1 — stale pointer: the round-8 `[U]` is no longer at `:1017-1019`

```
8's own `[U]` (`:1017-1019`), unchanged.
```

At C\* lines 1017–1019 read "tick\*\* — three readings per case, three triggers, one re-pin rule — and the same / tick read is the ground the six-case confidence statement below stands on. No / daemon, no timer: "standing" is the ledger + the policy + an executed command at" — the range stops mid-sentence and contains no `[U]`. The statement the pointer names ("whether any fleet driver would ever invoke the command with no lane acting stays `[U]`") is at **`:1020-1021`**.

Provenance: at round 52 (`7ff81a5:SKILL.md`) the phrase `no lane acting stays [U]` sat at line 1019, i.e. the last line of the cited range, so the anchor was valid then; round-53's own fix pass inserted two lines above it (`diff -U2 7ff81a5 a41195df… -- SKILL.md`, hunk `@@ -922,6 +922,8 @@`), moving it to 1021. The pointer was not re-resolved in the same commit — the exact class of self-anchor drift this re-read hunts.

### F2 — stale pointer: `:1359-1363` no longer holds the six-leg registry ledger row

```
(`:1359-1363`) — open at this write.
```

At C\* `:1359-1363` is the **"Reading a receipt"** bullet ("read the block, not the last line; PASS is exact for ledger legs … The runbook's §7 is the operator's rendering of this command as of round 10"). The statement the section names — "a ledger row recording the six-leg (ten-leg since round 51) registry is the ledger owner's follow-on" — is at **`:1366-1370`**.

Provenance: at round 52 (`7ff81a5:SKILL.md`) that bullet sat exactly at 1359–1363, so the range was correct at the write and was shifted by round-53's insertions above it: hunk `@@ -1246,5 +1248,9 @@` (+4, the service-limits intake paragraph), hunk `@@ -1355,5 +1361,6 @@` (+1, the runbook sentence "as of round 10 (four legs then; the tool embeds ten since round 51)"), plus the +2 of F1. Net +7.

### F3 — stale count: "six-leg registry" with no date, at ten legs

```
row for the six-leg registry**
```

The bullet names the registry "six-leg" with no date, while at C\* the registry carries ten legs and the page dates it everywhere else: `:1363-1364` "the tool embeds ten since round 51"; `:1368` "a ledger row recording the six-leg (ten-leg since round 51) registry"; `:1398` "the instrument: `--selftest`, `--regression` (six-leg registry at round 11, seven since round 16, eight since round 18, nine since round 26, ten since round 51 …)". The page's own round-16 repair table already records this identical bare token as a stale count needing a date — `:1747`: `| 1391 | "six-leg registry" | six at round 11, seven since round 16 | RR08, RR11 (w2) |` — so an undated "six-leg registry" fails the page's own convention as well as the current measurement. (This defect is inherited from round 52, not introduced by the round-53 fix pass; it is reported because it fails at C\*.)

## Not reported (considered, rejected for lack of evidence)

- `unchanged` in F1's sentence — the round-8 `[U]` text is substantively identical at `7ff81a5` and C\*; no failure.
- `the two successor rows … — open at this write` — scoped to its write; whether the rows landed later does not falsify the dated claim.
- `Append-only to the last line` — see Holds; nothing in the object store falsifies "this write".

## Limits

- Read scope: `SKILL.md` at C\*, plus `corpus/knowledge/{fleet-kill-rate-ledger,service-optin-protocol,service-limits}.md` at C\*, plus `SKILL.md` at `7ff81a5` for drift attribution. No working-tree file was read, no sibling lane was touched.
- Line numbers in this report are C\* line numbers of the file named in each sentence.
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read30/` (working copies `SKILL.md`, `prev.md`, `ledger.md`, `proto.md`, `sl.md`, `d.diff`, `sec_indep.bin`); deleted before this report was yielded — no residue on disk.
- Tools installed/upgraded for this seat: none.
