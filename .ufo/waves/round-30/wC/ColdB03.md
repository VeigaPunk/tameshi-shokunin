# ColdB03 — cold reads of SKILL.md sections 8, 9, 10 at bb681566

Clone: `/tmp/ColdB03-DyLt/fleet/tameshi-shokunin` detached at `bb681566b18211adf8ae9c28df91e17678e3f545`; SKILL.md sha256 matches the stated `c46ec02e…`.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdB03", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
  "sections": [
    {"start": 1021, "heading": "### The tick and the pin read", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [],
    "commands_executed": ["cd /tmp/ColdB03-DyLt/fleet/tameshi-shokunin && python3 tools/trace-inputs.py --root /tmp/ColdB03-DyLt/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB03-8-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/mutate-and-run.sh"],
    "opened": ["tools/mutate-and-run.sh"],
    "inputs": {"tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"},
    "external_inputs": {
      "shokunin@17c1fadfddc5ecbfa5ef362ef44d111792fa3e94:scripts/shokunin-watchdog.sh": "b8b01a78b9f66e343a6d5eefd027622b3c3718f79db2c7c06bb69c047fbe2226",
      "shokunin@5efb4114e8a4f6ff17d0b1594cb0767b144e4f9c:shokunin.conf": "a42e8406082ebb9a4248d91df06cb331c365b94e3ce877a6d8652363baebc5ee",
      "/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh": "319a56f7f0641915bdb636d88b2d6b34987a20f430d7b06896150f8ae4c1e429",
      "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
      "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
      "tsukuroi-shokunin@aa136d69e0e4666b86782152cd1d1fa00f90a0b3:tools/tsukuroi-census.sh": "bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55",
      "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
      "mado-shokunin@0c20a76fa5ff985047c8ca2d455c75179c3dd0d1:tools/mado-verify.sh": "90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd",
      "mado-shokunin@12c8f08a35537b7d53b8e0252459dec16e550079:tools/mado-verify.sh": "7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB03-8-1.json"]},
    {"start": 1164, "heading": "### The tick, executed", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["line anchor tools/mutate-and-run.sh:511-518 has drifted: at bb681566 those lines are the spec-parse defect loop; the PIN_*/REV_* table the sentence names now sits at :602-631 (tool grew r7-1 cf41efaa -> r30, 2080 L). Content verified, anchor stale — the ledger's own ER-jj2 sets the cite-by-name precedent for this."],
    "commands_executed": ["cd /tmp/ColdB03-DyLt/fleet/tameshi-shokunin && python3 tools/trace-inputs.py --root /tmp/ColdB03-DyLt/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB03-9-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md"],
    "opened": ["tools/mutate-and-run.sh", "corpus/knowledge/fleet-kill-rate-ledger.md"],
    "inputs": {"tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e"},
    "external_inputs": {
      "tsukuroi-shokunin@72b038da9b2b1da2a37d35e3cce2d1d7650f70be:tools/tsukuroi-census.sh": "bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55",
      "mado-shokunin@12c8f08a35537b7d53b8e0252459dec16e550079:tools/mado-verify.sh": "7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB03-9-1.json"]},
    {"start": 1212, "heading": "### The receipt at this boundary", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["line anchor tools/mutate-and-run.sh:733-791 has drifted: at bb681566 those lines are embedded defect-spec heredocs (legs 3-4 specs); the git-materialization code (git show <rev>:<path>, repo-identity guard, pin-mismatch SETUP) now sits at :1154-1242. Historical claim stands; the cited range has moved with the tool's growth.", "the record's REGRESSION_DATE 19:58:59Z differs from ledger ER-4's 19:58:18Z, but the two receipts name different scratch dirs (t93 vs t91) — two independent runs, consistent, not a contradiction."],
    "commands_executed": ["cd /tmp/ColdB03-DyLt/fleet/tameshi-shokunin && python3 tools/trace-inputs.py --root /tmp/ColdB03-DyLt/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB03-10-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md", "cd /tmp/ColdB03-DyLt/fleet/tameshi-shokunin && timeout 300 python3 tools/trace-inputs.py --root /tmp/ColdB03-DyLt/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB03-10-2.json -- env GIT_OPTIONAL_LOCKS=0 bash tools/mutate-and-run.sh --selftest"],
    "opened": ["tools/mutate-and-run.sh", "corpus/knowledge/fleet-kill-rate-ledger.md"],
    "inputs": {"tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e"},
    "external_inputs": {
      "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
      "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
      "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB03-10-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB03-10-2.json"]}]}
```

What I checked.

- **Section 8 (The tick and the pin read) — verified-record.** The fleet-driver claims resolve: `scripts/shokunin-watchdog.sh` at fleet `17c1fad` lines 3–5 state the round ends when `.ufo/reports/round-<N>/<lane>.md` lands and `Tick 450s` (`INTERVAL=450`); its lane map at :14 (`LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"`) does not name tameshi. Commit `5efb4114` (2026-10-19) is the v4→v5 cutover that sources `shokunin.conf` for lanes; `shokunin.conf` names tameshi at :55. `scripts/hyaku/jj-lane.sh` `state` prints `branch=$branch` (:182), reads `git config lane.branch` first (`lane_branch_git`, :103-104), and falls back to `detect_branch()` (:165, :118). Every blob sha256 in the round-8 executed-instance table verified byte-exact against the sibling repos' object stores at the recorded revisions (83016d45, 275d8294, e9a21b44, 7e5ec98b current; tsukuroi 084951be→bba6cdf6 at aa136d69 and mado d7edaab4→90d50cdd at 0c20a76f stale), matching the 4-current/2-stale/0-drift headline.
- **Section 9 (The tick, executed) — gap-minor.** The pin-read table agrees with ledger ER-4 (`fleet-kill-rate-ledger.md:318-353`: same six readings, second raw pass 20:00:29Z, both drift-event chains `084951be→bba6cdf6` and `d7edaab4→7da4ec50`, same regression receipt) and the addendum `:354-360` records the 20:02Z stale+drift continuation the section cites with "its then-current shas" (the addendum's 5d16378d/5b6ace8e differ from the section's later 20:03:34Z b54f5732/31364115 — correctly not equated). New HEAD blobs verified: tsukuroi @72b038da→bba6cdf6, mado @12c8f08a→7da4ec50. Minor gap: the `PIN_*`/`REV_*` anchor `:511-518` no longer lands on that table at this revision (it is the defect-spec parse loop); the table is at `:602-631` — drifted anchor, content still there.
- **Section 10 (The receipt at this boundary) — gap-minor.** Ran the tool's `--selftest` under the collector: `MUTATE_SELFTEST: 106/106 pass` / `VERDICT: PASS`, rc 0 — including the r30 tally-harness arms (`case-tally mismatch -> SETUP exit 2`, all nine leg statuses → correct PASS/FAIL/SETUP first lines), the doctored-pin refusal family section 8 cites (67/67 at r7-1), and the drift-immunity arms section 10 cites ("drifted working tree does not move a git-pinned leg"). Also ran `--regression` under the collector; it was killed at the 330s bound after 7/9 legs each `match=N/N … flips=0` PASS (>6 min for all nine legs — skipped per the instruction bound; the killed run wrote no receipt so it is not in `traces`). Ledger `:282` carries the named-debt line for cases 5/6 with no `REGRESSION` line, as cited. Minor gap: the git-materialization anchor `:733-791` is drifted (now spec heredocs; code at `:1154-1242`); the section's `REGRESSION_DATE 19:58:59Z` vs ER-4's `19:58:18Z` is consistent (different scratch dirs, two runs).

No wrong expectations found; every checkable recorded sha256 matches the sibling object stores. No tools installed (none needed).
COLDREAD ColdB03: verified-record, gap-minor, gap-minor
