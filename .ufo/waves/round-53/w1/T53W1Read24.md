# T53W1Read24 — cold read of `### The service's limits — what tameshi refuses to mutation-test`

Seat: T53W1Read24 (reader, axis `calibration`, milestone "C1 cold-read re-read").
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit read: `a41195dfc13a73958e4c5228ec196b28d03ded03` (C*).

## Section identity (frozen sectionizer, not a reimplementation)

`SKILL.md` at C* was extracted with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md` (2178 lines) into scratch, and `.ufo/evidence/round-18/measure.py` was extracted at the same commit and its `sectionize()` called on those bytes:

```
n sections: 64
hits: 1
{'start': 1248, 'end': 1277, 'heading': "### The service's limits — what tameshi refuses to mutation-test",
 'sha256': '37d63abf882e89d8103fb2618d8622c78da60aecfac75352851687e42eea7590'}
```

The heading is unique in the file (one hit). Section bytes = lines 1248–1277 (29 lines recorded, 2597 bytes, no trailing newline). The fence check is clean: 16 fence lines before line 1277 (even), so the heading at 1248 is outside a fence. `section_sha256` in the JSON is the sha256 of those UTF-8/surrogateescape bytes and matches the frozen sectionizer's own `sha256` field.

## Checks run (each read is a git object at C*; the working tree was never read)

| # | Check | Command (abbreviated) | Result |
|---|---|---|---|
| 1 | section boundary + hash | frozen `sectionize()` on `show C*:SKILL.md` | `start=1248 end=1277`, sha `37d63abf…7590` |
| 2 | cited files exist at C* | `git ls-tree -r --name-only C*` | `PROVINCE.md`, `corpus/knowledge/{service-limits,service-optin-protocol,fleet-kill-rate-ledger,fleet-suite-census}.md` all present |
| 3 | file lengths vs cited anchors | `git show C*:<path> \| wc -l` | service-limits 281 · optin-protocol 286 · ledger 441 · census 674 · PROVINCE 118 — every cited line number is in range |
| 4 | role quote | `show C*:corpus/knowledge/service-limits.md` 4–5 | line 4 ends `Role: the **refusal table the re-sweep cadence`, line 5 begins `applies at intake**` — the quoted clause spans exactly `:4-5` |
| 5 | negative cadence/ledger claim | `grep -n service-limits` on `show C*:SKILL.md` and on `show C*:corpus/knowledge/fleet-kill-rate-ledger.md` | SKILL hits only at 1251/1257 (this section), 1302, 1393, 1465 — none inside `:1010-1154`; the ledger has **zero** hits, so neither `:285` (ER-3) nor `:318` (ER-4) names the note |
| 6 | cadence anchors are cadence text | `show C*:…ledger.md` 285, 318 | 285 = `**ER-3 — the re-sweep cadence…**`; 318 = `**ER-4 — the cadence fires its first scheduled tick…**` |
| 7 | bare-anchor convention | `show C*:SKILL.md` 813–817, 823–825, 840–844, 879–881 | each is the section the row cites: hermetic-suite requirement; `The service never edits, repairs or re-pins the gate`; `MUTATE: SETUP (<reason>)`, exit 2 — no headline; `Sensitivity, not truth` |
| 8 | row (b) `MUTATE: SETUP` also covers a red control | `grep -n 'MUTATE: SETUP\|die_setup'` on `show C*:tools/mutate-and-run.sh` | `die_setup()` at :254 prints `MUTATE: SETUP (%s)`; the red-control path calls it at :542 — the row's compression is accurate, not an over-claim |
| 9 | rows (a),(d),(e),(f),(g),(h),(i),(j) anchors | `show C*:<note>` at the cited ranges | see the hold table below |
| 10 | "same rows" as the detail of record | `show C*:corpus/knowledge/service-limits.md` §1 table (lines 44–55) vs the section's table | both carry exactly rows `a`–`j`, same order, same refusal subjects; §2 details `(a)`–`(j)`; §3 is titled `## 3. The intake precondition — the re-pin rule (checked: present, cited)` and the §1 table's third column is `Trigger at intake` — the section's "trigger column and the intake-precondition check" exists |
| 11 | note identity | `show C*:…service-limits.md` line 1 | `# Service limits — what tameshi refuses to mutation-test, and why (T9-2, round 9)` — matches the section's `(T9-2, round 9)` |
| 12 | divergence hunting in the note's verbatim quotes | spot-check of the note's §2 quotes against the C* bytes of their targets | quotes resolve, with the drifts noted under "Dated drift" below |

## Holds — pointer-by-pointer (all verified against C* bytes)

- **Role sentence.** `service-limits.md:4-5` carries the quoted clause; the section states it as the note's claim and explicitly refuses to assert it as a cadence fact.
- **`no cadence or ledger text names it`.** Holds — the ledger never mentions `service-limits.md` anywhere in 441 lines, and `SKILL.md:1010-1154` (the round-8 cadence section and its subsections) does not either. The parent round-9 section (`## The cadence's first scheduled tick, and the service's limits (round 9, measured)`, line 1157) also does not name it, so the negative claim survives even against the enclosing section that the anchor range does not cover.
- **`Each refusal carries a measured anchor`.** Holds — all ten rows (a–j) carry at least one resolvable anchor; row g's anchor is a named ledger unknown (`- **U2** — coordinated multi-edit rewrites unmeasured everywhere (matrix §7).`), which supports the row's "no rate claimed" exactly.
- **Anchors `:…` are this page.** Holds — every bare `:N` in the table (`:813-817`, `:840-844`, `:823-825`, `:879-881`, `:1010-1154`) resolves in `SKILL.md` at C* to the content its row needs; `PROVINCE.md` is repo-relative and the remaining bare names are under `corpus/knowledge/`.
- **Rows a–j.**
  - a — `service-optin-protocol.md:25-30` carries `the standing default head is surface-probe, and a round with no opt-in records the no-opt-in line as its complete outcome` and embeds the census cite; `fleet-suite-census.md:277-286` is the queue projection.
  - b — `:813-817` (the one-command hermetic suite requirement) + `:840-844` (spec uniqueness `before any suite run`, `MUTATE: SETUP`, exit 2, red control exits 2); tool evidence at check 8 confirms the label covers the control path.
  - c — `:823-825` reads `The service never edits, repairs or re-pins the gate`.
  - d — `service-optin-protocol.md:129-132` reads `No live substrate read… a PATH-level stub, never the session`.
  - e — `PROVINCE.md:14-18` ends with `Credential material (→ kagi), endpoint health (→ kama).` and `PROVINCE.md:20` reads `**Out of province → report, never absorb.**`.
  - f — `:879-881` (`Sensitivity, not truth`) + `fleet-kill-rate-ledger.md:156-158` (`suite sensitivity ≠ gate truth`).
  - g — `fleet-kill-rate-ledger.md:220` (U2), see above.
  - h — `service-optin-protocol.md:267-269` (U4: `a harness that adjudicates by exit code alone cannot kill the exit-flatten family; a stdout-reading harness is a named future, not a measurement`) — "named, not fixed" is the same statement.
  - i — `fleet-kill-rate-ledger.md:35-36`: `is a **directed repair**, not an independent rate; it is recorded as such.`
  - j — `service-optin-protocol.md:86-91`: the mado run `kept exactly its own 8, and removed exactly those paths`.
- **Divergence rule.** The section's own rule (`a divergence between the two is the finding`) was applied: the two renderings differ only in anchor *depth* (the note adds `service-optin-protocol.md:199-201` for b, `SKILL.md:811-812`/`:1035`/`:1083-1086`/ledger `:293`/`:310` for c, `SKILL.md:860-861`/census `:288-289` for g, `:200-201`/ledger `:48` for h). Dropping a deeper anchor is compaction, not a divergent verdict; no row's stated meaning changes between the two.

## Dated drift (recorded, not promoted to findings)

- The section's closing line — `Anchors re-resolved 2026-10-14 on the live bytes; a reader on a differing revision re-resolves rather than trusts.` — is a dated observation that carries its own re-resolve rule; dated and self-protecting, so a hold, not a finding.
- The note (not this section) carries write-time cites that have since drifted: its §2(c) quote renders the re-pin rule with the parenthetical `(:811-812)`, while at C* that sentence instead carries the ledger cite (lines 1085-1086: `against the new bytes` then `fleet-kill-rate-ledger.md:310`, ER-3; `:318`, ER-4), and its §6 pins `SKILL.md` at 1249 lines where C* has 2178. The note records this itself (`ER-1`, which says to cite the round-9 SKILL section by heading, not by line) and the section's re-resolve clause covers it. Neither is a statement of this section failing at C*.
- The section contains no `/tmp` scratch path of its own, so the host scratch directive (`$HYAKU_SCRATCH` default `/fast/scratch/hyaku`; `/tmp` only < 50 MB) is not engaged by its text. Row j's anchor quotes the protocol's older lane scratch convention; the row itself states only `never removed`.

## Findings

**None.** `findings` is `[]`: every checkable statement in the section — the role quote and its anchor, the negative cadence/ledger claim, the anchor convention, the "same rows / trigger / intake-precondition" description of the note, and all ten refusal rows with their anchors — resolves at `a41195dfc13a73958e4c5228ec196b28d03ded03`. No stale count, no dead receipt, no unsupported premise, no self-contradiction, no scratch-directive violation was evidenced.

## Limits of this read

- Semantic fairness of the note's own quotes was spot-checked (§2 (a), (b), (c), (d), (e), (f), (g), (h), (i), (j) against their targets), not exhaustively re-derived; the note's §4 spot-check receipts were not re-executed (that would rerun work, not read it).
- `fleet-suite-census.md:277-286` was read as the queue projection the protocol's own text cites for that range; I did not test whether a reader who follows it cold infers "offer, not a schedule" from it alone.
- Tooling: no installs, no upgrades — `git`, `awk`/`grep` and the system `python3` sufficed. No pacman, no network.
- Scratch under `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read24/` was deleted before this seat returned.
