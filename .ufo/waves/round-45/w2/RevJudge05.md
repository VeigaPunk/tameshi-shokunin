seat: RevJudge05

C1 falsify re-judgment of the wave-1 ledger entries for S101 and S160 (I am not their author). Inputs at ad5942c6e9858af19d00000b58439b321ddfa62b: `.ufo/evidence/round-45/freshness/ledger.json` and the committed snapshots it names; author reports read from disk `.ufo/waves/round-45/w1/ExecRows19.md` and `.ufo/waves/round-45/w1/ExecRows16.md`. Live fetches done 2026-10-25 with `curl -fsSL -A 'Mozilla/5.0' --max-time 90`.

S101 agree — reviewer RevJudge05 — live sha256 equals the ledger raw_sha256 and the committed snapshot digest (byte-identical static page, 4,341 B), and the 13-token quote locates afresh in the Overview feature-list body at the row's anchor, enumerating exactly the teaches claim (suppressing equivalent mutants + mutant-detection rate + live-mutant set), 8 content words shared, none of it copied from the row cells.

S160 agree — reviewer RevJudge05 — live sha256 equals the ledger raw_sha256, the committed snapshot digest and the row anchor's `79f6501a` round-44 re-open pin (byte-identical, 38,687 B, so the cited sentences survive at the same offsets), and the 11-token quote locates afresh exactly once in the Equivalent-mutant body immediately after the `10 ** 0` example, spanning "It is called equivalent mutant ." into "There is no definitive way [for Stryker to find and ignore them.]", the very sentence the row cites; 3 content words shared, and the quote deliberately stops short of the sentence quoted verbatim in the anchor cell so it is not copied from the row.

## Provenance (sha256sum)

- S101 live: `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420` (4,341 B) — equals entry `raw_sha256`, equals `gunzip -c .ufo/evidence/round-45/freshness/sources/S101.raw.gz | sha256sum`, equals the anchor's 2026-10-23 pin. All equal.
- S160 live: `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce` (38,687 B) — equals entry `raw_sha256`, equals `gunzip -c .ufo/evidence/round-45/freshness/sources/S160.raw.gz | sha256sum`, equals the anchor's `79f6501a` pin. All equal.
- Both committed `.gz` files in the worktree are byte-equal to their blobs at ad5942c (`cmp` clean), so the judged inputs are the committed ones.
- `entry.opened` = 2026-10-25 for both rows; snapshot digest and size match the anchor cells (S101 4,341 B; S160 38687 B).

## Located context (measure.py --extract of the committed snapshot, a few words either side)

- S101 (single occurrence, Overview body — the row's anchor section; page title/nav sit ahead of it): "Major is an efficient and flexible mutation analysis framework that supports: generating and embedding mutants during compilation; exporting source-code mutants; [suppressing equivalent mutants; computing the mutant-detection rate and the set of live mutants] for a given set of tests; computing a complete mutant-test detection matrix…"
- S160 (single occurrence at extract index 1681, well past the title/nav head "Equivalent mutants | Stryker Mutator Skip to main content…", in the §Equivalent mutant body): "…Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time! [It is called equivalent mutant . There is no definitive way] for Stryker to find and ignore them. There is currently also no way yet to mark them to be ignored…" — body prose carrying the 10**0 example and the no-definitive-way sentence the anchor cites; not a `<title>`, nav, footer, cookie banner or bare code fragment.

## Frozen-predicate cross-check (measure.py rules, lines 18–31 and 149–162, applied in-process via grade())

- S101: 13 whitespace tokens (6–25 ok); quote present in normalized snapshot text; not a substring of source/scope/anchor/teaches cells; shared content words = computing, detection, equivalent, live, mutant, mutants, rate, suppressing; `grade` → `('verified', 'ok')`.
- S160: 11 whitespace tokens (6–25 ok); quote present (1 occurrence); not a substring of any cell — the author report states the quote intentionally stops before the anchor-cell sentence, verified; shared content words = definitive, equivalent, mutant; `grade` → `('verified', 'ok')`.
- Author reports match their ledger entries (same URL, digest, quote, snapshot path, `verdict: holds`).

reviews.json: /tmp/tameshi-r45-RevJudge05/reviews.json

Tooling: none installed — curl, coreutils (sha256sum/gunzip/cmp) and the lane's own counter functions sufficed; no pacman/uv/npx transaction performed.
