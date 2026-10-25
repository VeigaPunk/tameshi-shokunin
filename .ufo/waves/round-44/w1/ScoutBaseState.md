# Round 44 base state facts

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse master`:
  ```
  315453b821e4c7732ea4de09f0478ff5976c2c42
  ```
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain`:
  ```
   M .ufo/waves/round-43/w1/RevC2Classes.md
  ```
- `grep -n '| S089 |' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` (raw result, line 98):
  ```
  98:| S089 | Equivalent mutants (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | docs | A | Stryker's own statement that equivalent mutants cannot be found or marked automatically | page body after the `10 ** 0` example @ page fetched 2026-10-22 (version unstated; html sha256 bc572676…e04d) | an equivalent mutant stays a survivor in the score; calling a survivor a test-suite hole needs an off-suite witness or an explicit equivalence argument | mined...
  ```
  (The grep display truncates the matched row after 512 bytes.)
- `safe_floor=S256` appears in the round-43 C3 receipt at SCORECARD.md line 2091; raw line from the displayed block:
  ```
  C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=24 selftest_failed=0 staged_rows=103 live_collisions=7 live_collisions_agree=1 live_held=3 live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=1 map_dedupe_live=1 held_refused=1 safe_floor=S256 staged_sha256=020fbeaa… naive_agree=1 substitute=0 rev=3c4003f6… C3_R43_PASS=true
  ```
  Raw line number/contents confirmed from `SCORECARD.md:2091`.
- Round-43 counter receipt at base, `.ufo/evidence/round-44/before/c2-old-at-base.stdout:1`:
  ```
  C2_R43: self_pin=1 classes=7 m6=0 m7=1 m8=0 m10=0 m11=0 m12=0 m13=0 total=1 records=4 sources_rows=114 standing=114 receipts=17 revisions=4 m13_probe=standing=7_column0=113_valid=114 rev=506e99c7b73c85711f066895984d501fcf7539cd freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=false first=m7:SCORECARD.md#round-43_unknown_S256
  ```
- Next-unused-id note at registry tail, `corpus/SOURCES.md:456`:
  ```
  - Next unused id: S160.
  ```
