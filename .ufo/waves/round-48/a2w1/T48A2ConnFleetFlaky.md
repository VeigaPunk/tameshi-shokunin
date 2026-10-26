# T48A2ConnFleetFlaky — adjacency: the pinned tsukuroi leg's `printf | grep -q` flake across siblings

Seat: T48A2ConnFleetFlaky (round 48, attempt 2, wave a2w1; connector / adjacency). Read-only on every
sibling and on the lane (only this report written). No scratch dirs were needed — every probe below is
a read of a committed sibling file or `git show`/`git log` on a sibling repo. No installs; tooling
ledger empty. Attacks: the w1 claim (`.ufo/waves/round-48/w1/T48RevenRegression.md`) that the
six-leg regression ledger flake lives in the pinned tsukuroi leg blob
`084951be50bc…78c5` @ tsukuroi `165307fe`. Questions: does a sibling already know or fix it (which
revision)? Does the lane's pinned blob predate a sibling fix?

## Verdict (short)

1. **A sibling knows the exact class and has fixed it — in its own file, not the pinned one.**
   `mori-shokunin` diagnosed the `producer | grep -q` under `pipefail` SIGPIPE race on
   2026-10-15 against `tools/mori-census.sh` r5 (`390ab9cd…`), landed the fix at census revision
   `1c49238a` (commit `cffb37ef`, "selftest flake eliminated … race 15/8000 -> 0/60000"), and the fix
   persists at mori HEAD (`4548a34d`, round-50; current census `census-r6` greps one captured
   `$OUT_FILE`, fix comment at `tools/mori-census.sh:3300`).
2. **The pinned file's owner (tsukuroi) saw the symptom once and did not root-cause it.** tsukuroi's
   own round-35 receipt prints the exact fleet failure text in its own selftest
   (`.ufo/waves/round-35/l1/r35-st-after.txt:66`, "hostname override not honoured — possible host
   read"), recorded in `LOG.md:1341` as "under host load … passed on re-run". **No tsukuroi revision
   fixes it** — HEAD `8b7c413` (round-40) still carries the hazard at
   `tools/tsukuroi-census.sh:2175/2177/2181/2187/2192/2223` under `set -euo pipefail` (`:423`).
3. **The pin predates mori's fix by ~1 day, but no sibling fix exists for the pinned file's lineage.**
   The pinned blob was introduced by tsukuroi `9bcd162` (probation round 3) and the lane pins
   `165307fe` (probation round 4) — both 2026-10-14 era; mori fixed mori's census on 2026-10-15.
   Since the pin, tsukuroi has landed 12 first-parent commits on the file (rounds 5→40), several of
   which *extended* the `grep -q` sites (r12 `70fede2`, r32 `4ac5eba`, r35 `e2f97e6`). **There is no
   tsukuroi revision the lane could re-pin to.** The w1 revenger's "not removable without editing the
   tool" stands, sharpened: re-pinning cannot help either.

## Evidence, per sibling

### 1. mori-shokunin — knows the class, measured it, fixed its own census

- `mori-shokunin/corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md` (round 9, 2026-10-15,
  seat lessons-distiller): the exact mechanism the w1 revenger found in the pinned tsukuroi leg —
  `printf '%s\n' "$out" | grep -qE -- "$re" || miss=…` under `pipefail`: grep exits 0 on match and
  closes the pipe; the forked printf subshell dies of SIGPIPE (rc 141); `pipefail` promotes 141; the
  `||` branch records a present regex as missing — a false FAIL, green on rerun. The lesson's
  construct at its line 20 is character-for-character the pinned tsukuroi leg's `check()` idiom
  (pinned blob `:777` `printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss '$re'"`).
- Measured rates (mori, host load 85–110): ~1/1000–1/3000 per assertion for an early match on a
  2.3 KB payload, 16/300 at 60 KB, 100/100 at 1.2 MB; matches near the payload end never raced in
  300–5 000 reps. **One-sided: the race can only turn a green case red** — same one-sidedness the w1
  revenger measured (9/12 000 in the pinned leg, `grep` 0 / `printf` 141 in every false branch).
  strace shows the writer is a forked bash subshell emitting the payload in many small `write(2)`
  calls — the property that lets `grep -q` close mid-payload even at harness sizes.
- Fix: capture-then-grep — `printf '%s\n' "$out" > "$OUT_FILE"`, then grep the file (no live pipe).
  Landed as census revision `1c49238a` in commit `cffb37ef` ("round-9 evidence: selftest flake
  eliminated (census 1c49238a; capture-then-grep, race 15/8000 -> 0/60000; batteries 20/20 + 20/20
  loaded)"). The standalone fix sha `1c49238a` no longer exists as a commit (probation history was
  later squashed), but the fix bytes are in mori HEAD: `tools/mori-census.sh:3300` carries the
  "r9 FIX: every match below greps the ONE capture file, never a live pipe" comment block, and the
  harness greps `$OUT_FILE`. Current census VERSION is `census-r6`.
- Admission: `mori-shokunin/SCORECARD.md:428-432` — flaky-failure class, "grep-over-pipe SIGPIPE
  race at `tools/mori-census.sh:1783/:1809`; admission seat ~25% false-FAIL in one battery"; fix
  verified "receipt-backed 0-flake over a ≥20-run" battery (`:450-461`).
- Scope note: mori's knowledge and fix are about `tools/mori-census.sh`. Nothing in mori's lesson
  names tsukuroi's census; the transfer is by identical construct, not by citation. (The lane's own
  w1 `T48ConnSiblings.md` A5 already mined mori's SCORECARD admission; this seat adds the lesson
  file, the fix commit/revision, and the persisted-fix check.)

### 2. tsukuroi-shokunin — the pinned file's owner: symptom seen, never root-caused, never fixed

- The owner self-observed the exact fleet failure text once, at its own then-current bytes:
  `.ufo/waves/round-35/l1/r35-st-after.txt:66` —
  `FAIL healthy: oom watch — external baseline file, both waves known (S9-2): hostname override not honoured — possible host read` —
  recorded in `LOG.md:1341` (round 35) as "one pre-existing oom case failing … under host load …
  and passed on re-run". The same message class the fleet ledger flake prints (w1 replay B evidence
  line; round-47 `T47ExecObsE.md:151`). tsukuroi attributed it to "host load"; no note in tsukuroi
  connects it to SIGPIPE/`grep -q`.
- The lane knows the SIGPIPE class in general: `corpus/knowledge/aur-risk-plane.md:333-335`
  (2026-10-14) records `… | tee qi-all.txt | head -120` truncating a capture when `tee` died on
  SIGPIPE. That knowledge was never applied to the census selftest's own `printf | grep -q` sites.
- No fix at any revision after the pin. HEAD `8b7c413` (round-40) `tools/tsukuroi-census.sh`
  (3 149 lines, sha256 `032faa8f…`): `set -euo pipefail` at `:423`; `check()` still asserts with
  `printf '%s\n' "$out" | grep -q 'host=fixture-host'` (`:2175`),
  `| grep -qE '^PLANE packages: …'` (`:2177`), `| grep -qE "^TSUKUROI_CENSUS: …"` (`:2181`),
  `| grep -qE -- "${re#ABSENT:}"` (`:2187`), and the fleet-flake construct
  `printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss '$re'"` (`:2192`, `:2223`).
- The `grep -q` sites were *extended* after the pin: `git log -G 'grep -q'` shows
  `70fede2` (round-12), `4ac5eba` (round-32), `e2f97e6` (round-35) all touched them; rounds 39-40
  hardened fixtures (FIFO/empty-table, mount-table literals — `a2d7aad`, `c707e35`) but not this
  determinism hazard (no `grep -q`/SIGPIPE content in `corpus/lessons/round-38..40.md`).
- tsukuroi knows the fleet pin: `corpus/knowledge/closeout-r11.md:361` records
  `bash-tsukuroi-census | tsukuroi@165307fe | 084951be | 6/10 = 60 %`; `SKILL.md:576` pins the
  round-5 hardening base at the same sha256. So the owner knows its round-3/4 bytes are what the
  fleet suite materializes, and has left them carrying the hazard.

### 3. kagi-shokunin — the other exposed leg (`bash-surface-census`): hazard unfixed, no knowledge

- The leg file lives at `corpus/surface-census.sh` (not `tools/`). At the fleet pin `fecee874`
  (round-18): `set -euo pipefail` at `:73` and the same class at
  `:681` `printf '%s\n' "$out" | grep -q "^$k" || missing+="$k "`. At kagi HEAD `69b61db`
  (round-28) the construct persists (`:73`, `:682`). No fix, no flake note in kagi's corpus/LOG/
  SCORECARD (grep for the hazard family returned nothing).

### 4. Other siblings — no hits

- Fleet grep for the failure signature `hostname override not honoured` across
  mado/mori/kumitate/souji/revenger/kaidoku/tabi/kasegi/chousa/kengaku corpora and top-level docs:
  no hits outside tsukuroi's own waves. `TSUKUROI_CENSUS_SELFTEST: FAIL` appears only in tsukuroi's
  own wave evidence (r25 forged-FAIL control, r38 malformed-fixture and namespace-TMPDIR cases —
  all intentional reds, not this flake). No sibling lesson on the `grep -q`-over-pipe class exists
  outside mori's.

## Does the lane's pinned blob predate a sibling fix? — yes, and it matters less than this: no fix exists in the pinned file's lineage

- Blob introduction: `084951be…` is produced by tsukuroi `9bcd162` (probation round 3); the lane's
  runner pins rev `165307fe` (probation round 4), which inherited it. `git merge-base --is-ancestor
  165307fe HEAD` → true; 12 first-parent commits touch the file after the pin (rounds 5→40).
- Mori's diagnosis+fix (2026-10-15) postdates the pin's bytes by ~1 day, but it is on
  `tools/mori-census.sh` — it never existed in tsukuroi's history. The only sibling fix therefore
  cannot be obtained by re-pinning.
- The owner's HEAD is hazard-identical in kind (six `printf | grep -q` sites under `pipefail`,
  more than the pinned blob's four). The pinned blob is not uniquely stale — the hazard is the
  owner's current design, and tsukuroi's own round-35 receipt shows the symptom in its live bytes
  too.

## What this changes for the round's declared axes (C1 calibration feed)

- **Corroboration, not contradiction:** mori's independently measured rates (1/1000–1/3000 per
  early-match assertion at harness sizes; strictly one-sided) and one-sidedness match the w1
  revenger's pinned-leg measurements (0.075 %/invocation; `grep`=0/`printf`=141 in every false
  branch). Two lanes' evidence now bound the same class.
- **The `nondeterministic` class is the ceiling the sibling frontier supports.** mori's response to
  the same class was quantify → root-cause → fix its own file; the lane cannot fix the pinned file
  (read-only on fleet/siblings; re-pinning has no clean target). The w1 class verdict stands.
- **Receipt-level cross-check available to falsifiers:** tsukuroi `.ufo/waves/round-35/l1/r35-st-after.txt:66`
  is a committed, organic instance of the exact fleet failure message in the owner's live bytes —
  usable as adjacency evidence that the message is a known scheduling flake, not a semantic
  regression of the leg.

## Commands that show it (all read-only)

```bash
# mori knows + fixed its own census
sed -n '1,60p' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show --stat cffb37ef | head
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show HEAD:tools/mori-census.sh | sed -n '3295,3310p'
sed -n '428,432p' /home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md

# tsukuroi: symptom seen, not fixed
sed -n '66p' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/l1/r35-st-after.txt
grep -n 'host load' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/LOG.md   # -> line 1341
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show HEAD:tools/tsukuroi-census.sh | grep -n 'grep -q\|pipefail'
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 165307fe:tools/tsukuroi-census.sh | sha256sum   # 084951be…

# kagi's surface-census leg: hazard at pin and HEAD
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show fecee874:corpus/surface-census.sh | grep -n 'grep -q\|pipefail'
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show 69b61db:corpus/surface-census.sh | grep -n 'grep -q\|pipefail'
```

## Compliance

Lane checkout and all siblings read-only; the only write is this report. No sibling edited, no
scratch tree created (nothing to delete), no installs, no git/jj mutation anywhere. Tooling ledger:
empty. Findings are adjacency evidence only; the counters and the verdict remain the seats named in
the contract.
