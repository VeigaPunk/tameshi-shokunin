# Read01 — cold read, section at line 6 (`# tameshi-shokunin`)

Lane revision 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, SKILL.md sha256
386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 (verified on a
fresh fleet-mirror clone, detached at the revision). Section spans lines 6–16,
ending before `## Standing rules` (line 17). Class: **record** (it states
provenance facts with pointers; it commands no run).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read01", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [{"start": 6, "heading": "# tameshi-shokunin", "class": "record", "verdict": "gap-minor",
    "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [
      "The 'fleet round 1' label on the re-run is corroborated but not stated inside the cited directory: the dir is named .ufo/evidence/kaika-round-1/coldread/, and the fleet-round-1 attribution rests on SHA256SUMS.txt recording every artifact under the fleet worktree /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tameshi-shokunin/..., on .ufo/waves/fleet-round-1-interactive/spec.json auditing 'the interrupted tameshi fleet round-1 calibration correction', and on the snapshot pinning a round-1-era SKILL.md blob (4eb4cf3, sha256 33e3009c...).",
      "'Every rule below earns a cited source' was spot-checked (Gate-shape table at SKILL.md:58-64, mutation-bar bullets at 94-130, Appendix A at 527-556 all carry note-line citations), not re-audited for all 50 remaining sections; 'Rounds 1-3 built the corpus' was checked via the round-2/round-3 case notes and plans references, not via a full corpus-history audit."
    ],
    "commands_executed": [
      "python3 tools/trace-inputs.py --root /tmp/read01-fleet/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read01-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/kaika-round-1/coldread/spec-A.txt .ufo/evidence/kaika-round-1/coldread/spec-B.txt .ufo/evidence/kaika-round-1/coldread/A-check.txt .ufo/evidence/kaika-round-1/coldread/B-check.txt .ufo/evidence/kaika-round-1/coldread/A-control.txt .ufo/evidence/kaika-round-1/coldread/B-control.txt .ufo/evidence/kaika-round-1/coldread/appendixA/results.tsv .ufo/evidence/kaika-round-1/coldread/appendixB/results.tsv .ufo/evidence/kaika-round-1/coldread/SKILL.snapshot.README",
      "python3 tools/trace-inputs.py --root /tmp/read01-fleet/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read01-2.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md"
    ],
    "opened": ["SKILL.md", ".ufo/evidence/kaika-round-1/coldread/spec-A.txt", ".ufo/evidence/kaika-round-1/coldread/spec-B.txt", ".ufo/evidence/kaika-round-1/coldread/A-check.txt", ".ufo/evidence/kaika-round-1/coldread/A-control.txt", ".ufo/evidence/kaika-round-1/coldread/B-check.txt", ".ufo/evidence/kaika-round-1/coldread/B-control.txt", ".ufo/evidence/kaika-round-1/coldread/appendixA/results.tsv", ".ufo/evidence/kaika-round-1/coldread/appendixB/results.tsv", ".ufo/evidence/kaika-round-1/coldread/SHA256SUMS.txt", ".ufo/evidence/kaika-round-1/coldread/SKILL.snapshot.README", "corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", ".ufo/waves/fleet-round-1-interactive/spec.json", ".ufo/waves/fleet-round-1-interactive/plan.stdout.json", ".ufo/waves/round-26/w1/ColdreadPilot.md"],
    "inputs": {
      ".ufo/evidence/kaika-round-1/coldread/spec-A.txt": "ae45bba52ce8a9fbed18378d1864e7f5b49c2fc3d2e61601d2b3696cc86a3eb1",
      ".ufo/evidence/kaika-round-1/coldread/spec-B.txt": "dd6142fc6530eaf4a693b693e3eecb7406e71859e2490265215506fd4886acb4",
      ".ufo/evidence/kaika-round-1/coldread/A-check.txt": "97a9d9b5b3fe0cacabdb45375d85a560df5b068679181eb6dc25d4abf43b6543",
      ".ufo/evidence/kaika-round-1/coldread/B-check.txt": "03f7bfbe5deba252548da8b055232a01af2fa96a3d076895706d8a0b821bd5d8",
      ".ufo/evidence/kaika-round-1/coldread/A-control.txt": "4e01b92d91eb3c645b987482b54e7008386a0afae1e3246d5cd1a051233ce28e",
      ".ufo/evidence/kaika-round-1/coldread/B-control.txt": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
      ".ufo/evidence/kaika-round-1/coldread/appendixA/results.tsv": "ea0915e653c294432b275db6e1df790f3b11b5f686fc7d500fbacd61a5ff4141",
      ".ufo/evidence/kaika-round-1/coldread/appendixB/results.tsv": "b1108cbfde25f5dee1a1646e32e65c20a35896b94bb6a7e5671dc638efd42d9e",
      ".ufo/evidence/kaika-round-1/coldread/SHA256SUMS.txt": "a3bf08251a3ea70e34d01d30b58100e445f1a9a659bfd1aaad9cc601554709fd",
      ".ufo/evidence/kaika-round-1/coldread/SKILL.snapshot.README": "3aa41c1f442774bb711cccaf463e977d48424b5f506c2351c82cee635061235a",
      "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
      "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
      ".ufo/waves/fleet-round-1-interactive/spec.json": "4e76986233f865d69f4acbbadd09f0321953894e4618c37289743ba6da341184",
      ".ufo/waves/fleet-round-1-interactive/plan.stdout.json": "34add49f44e6e26e695382df612ae96528c3097b02b5125da2c74cf00327f7a4",
      ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7"
    },
    "external_inputs": {},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read01-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read01-2.json"]}]}
```

## What I checked (plain English)

- **Clone integrity.** Fresh fleet-mirror clone with sibling symlinks, detached
  at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647; `git rev-parse HEAD` matched and
  the whole-page SKILL.md sha256 matched the given 386de44b...95e95. All reads
  and traces ran inside that clone; the live lane was only touched for the two
  trace receipt writes and this report.
- **"The first two mutation cases — round 2 JS, round 3 bash, both 8/10 killed
  — are worked here."** Verified. `corpus/knowledge/mutation-case-kimi-census.md`
  (TAMESHI-R2-1, round 2, JS `kimi-census.mjs`) states "kill rate 8/10 (80 %);
  survivors D2, D10"; `corpus/knowledge/mutation-case-kagi-census.md`
  (TAMESHI-R3-1, round 3, bash `surface-census.sh`) states "kill rate 8/10
  (80 %); survivors B5, B10". Appendix A (SKILL.md:527) and Appendix B
  (SKILL.md:594) exist and are complete reproduce specs: artifact pin with
  sha256, ordered commands, driver contract, survivor probes, expected
  8/10 outcome.
- **"(seven recorded since round 16; eight since round 18; nine since round
  26)."** Verified against the page's own register row (SKILL.md:1390:
  "six at round 11; seven since round 16; eight since round 18; nine since
  round 26") and against git history: the case-7 note
  (`mutation-case-kumitate-round-gate.md`, headed "round 16") landed in commit
  c699c8c "round-16: land js-round-gate case 7"; the case-8 note
  (`...-sources-check.md`, "round 18") in 58e5d53 "round-18"; the case-9 note
  (`...-cite-check.md`, self-described "the ninth recorded mutation case",
  verified-at 2026-10-22) in 40a12bf "round-26: content landing — ninth-case
  entry". Nine files match `corpus/knowledge/mutation-case-*.md` at the rev.
- **"this page carries the method as an executable recipe..."** Verified by
  section headers: numbered recipe (line 131), defect templates with
  exact-string guidance (246), kill-rate bands (314), restore discipline (375),
  measured bash-vs-JS divergence (405), Appendices A/B (527/594).
- **"fleet round 1 re-ran all 10+10 Appendix A/B mutants
  (`.ufo/evidence/kaika-round-1/coldread/`)."** The cited directory exists at
  the rev and holds a complete 10+10 re-run: spec-A.txt (defects D1–D10) and
  spec-B.txt (B1–B10) transcribed from the executed snapshot; per-mutant
  outputs `appendixA/D1..D10.out` + `control.out` and `appendixB/B1..B10.out` +
  `control.out`; `results.tsv` in each shows exactly 8 KILLED / 2 SURVIVED with
  the survivors D2/D10 and B5/B10 matching the census notes; `A-check.txt` /
  `B-check.txt` show each old-string occurred exactly once ("all unique");
  controls are green (43/43 JS; 16-case bash); SHA256SUMS.txt hashes every
  artifact and records the run under the fleet worktree
  `.tower/worktrees/kaika/tameshi-shokunin/...`; SKILL.snapshot.README pins the
  executed revision to blob 4eb4cf3 (sha256 33e3009c...) and documents the
  intentional pre-commit removal of the snapshot byte copy. The round-16
  errata row for snapshot line 15 ("cold-read proof covers one JS mutant only"
  → "points here") is consistent with this dir being the expanded proof. The
  only soft spot is the "fleet round 1" label itself (see minor_gaps).
- **"round 16 adds a full-page cold-read (Errata — round 16)."** Verified:
  SKILL.md:1707 `## Errata — round 16 full-page cold-read` documents a 51-bucket
  full-page cold-read (30 seats, CR01–CR27 + a/b replicas) with reports and a
  ledger, plus a per-line repair table.
- **No forbidden files opened:** SCORECARD.md, LOG.md, and
  `.ufo/evidence/round-21/coldread/ledger.json` were never read under the
  collector or by path; no sibling repo bytes were read, so `external_inputs`
  is empty. Both receipts carry `rev` equal to `read_rev`
  (tameshi-trace-inputs-v1).

No tool installs were needed or performed.

COLDREAD Read01: gap-minor
