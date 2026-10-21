# PredK11 — fleet-root-realpath falsification (round24 W1)

## Verdict

**DEFECT (calibration): K11 overclaims.** It does discriminate the routed round23 defect: lexical or
string fleet root, and string self-exclusion. But the "siblings" part of "realpath-normalises repo, fleet
root and siblings" is vacuous. A plan that never realpaths siblings passes K11 on its fixture. So do
normpath-before-realpath, name-based self-exclusion, and dropped `is_dir`/suffix/sort filters. The
sibling-realpath behaviour that K11 cannot see is also an untested identity change against the
established `registry-check.py` convention. It is latent in the live fleet today.

**before.json: honest.** K11 = false at base because `tools/registry-replay.py` is absent there
(`reason: tool-absent`). That base-zero comes from the tool not existing, not from a missing behaviour,
and the receipt says so.

No K11 vacuous pass in the strong sense: on the delivered code the fixture yields the expected values for
the right reason (a physical symlink, `alias`, is resolved). The pass is just weaker than its name.

Method: read-only. This item does not say "Run", so nothing was executed beyond `git show/log/diff/cat-file`,
`sha256sum`, `ls`/`find` and JSON reads. The mutant outcomes below are derived from POSIX/CPython
`os.path` semantics applied to the exact fixture in `measure.py:185-200`. They were not executed.
No tools were installed or updated.

## Evidence

### Ruler and fixture
- `.ufo/evidence/round-24/measure.py:185-200` (sha256 `0a7f6daa…7daa64`, identical at e338f1b and
  c8c5b88 and in the worktree; sole commit touching it: e338f1b). The fixture is
  `fx/fleet/{lane-shokunin,other-shokunin}` (both plain directories), with `fx/alias -> fx/fleet`.
  The input is `fx/alias/other-shokunin/../lane-shokunin`.
  The check requires exit 0, `fleet_root == realpath(fleet)`, `repo == real/lane-shokunin`, and
  `siblings == [real/other-shokunin]`.
- Fixture properties that matter:
  - **The only sibling is a plain directory inside an already-real fleet**, so `str(p) == realpath(p)` for it.
  - The `..` traverses `other-shokunin`, which is not a symlink, so lexical and physical `..` agree.
  - There is one sibling, no regular file named `*-shokunin`, and no non-suffix entry.

### Implementation at c8c5b88 (unchanged since d2eaecd)
- `tools/registry-replay.py:63-69`, `plan()`:
  - `real = realpath(repo)` and `fleet = dirname(real)`.
  - `siblings = sorted(realpath(p) for p in glob('*-shokunin') if p.is_dir() and realpath(p) != real)`.
- `tools/registry-replay.py:160-161`: the mirror is `fleet/basename(sibling)`, where `sibling` is the
  realpath'd target.
- The selftest `plan-realpath` case (`:227-242`) uses the same plain-directory shape and does not check `repo`.

### Established convention (base 6a1821a and c8c5b88)
- `tools/registry-check.py:762-783`:
  - `fleet_root = dirname(realpath(root))` and `src = os.path.join(fleet_root, name)`.
  - Self-exclusion uses `realpath(src) == root_real`.
  - The mirror is `os.symlink(src, fleet/name)`.
- So siblings keep their **fleet name** as identity, and realpath is used only to exclude the lane itself.
  `registry-check.py:1907` uses the same fleet-root rule.

### Routed defect K11 claims to close
- `.ufo/waves/round-23/fresh-adjudication.json:87`: "replay.py compares sibling identity by string and
  does not take the realpath of the fleet root."
- In `.ufo/evidence/round-23/replay.py:48-53`, the fleet root is `args.repo.parent` taken as a string, and
  `sibling != args.repo` is also a string comparison.

### Mutant table for `plan()` against the K11 fixture (derived)

| # | Weaker `plan()` | K11 outcome | Why |
|---|---|---|---|
| M1 | `real = abspath(repo)` (lexical) | **killed** | `fleet_root = fx/alias`, not `fx/fleet` |
| M2 | round23 style: `fleet = dirname(repo)` string, string self-exclusion | **killed** | `fleet_root` is unresolved |
| M3 | realpath fleet, but self-exclusion by `p != repo_arg` string | **killed** | the lane appears in `siblings` |
| M4 | `siblings = sorted(str(p) …)`, no sibling realpath (registry-check convention) | **survives** | fleet is real and the sibling is a plain directory, so `str(p) == realpath(p)` |
| M5 | `realpath(normpath(repo))` | **survives** | `normpath` gives `fx/alias/lane-shokunin`, then `realpath` gives `fx/fleet/lane-shokunin`; it only differs from physical resolution when the component before `..` is a symlink |
| M6 | self-exclusion by `p.name != basename(real)` | **survives** | there is no aliased sibling |
| M7 | drop `is_dir()`, drop `*-shokunin` filter, or drop `sorted` | **survives** | single plain-dir sibling, no files or other entries in `fx/fleet` |

K11 therefore pins **fleet-root and repo realpath plus realpath-based self-exclusion**. It pins nothing
about sibling normalisation, which is one of the three things its name, the tool docstring (`:13`),
`corpus/knowledge/replay-projection-hardening.md:20`, `SKILL.md:2047` and `SCORECARD.md:1137,1150` claim.
The knowledge row's "a … `..` path alias changes identity" is likewise not independently discriminated
(M5).

### Counterexample: the untested sibling realpath is an identity change
Take a fleet `F/` where `F/foo-shokunin -> /store/foo` is a symlinked sibling repo:
- `registry-check.py --rev` mirrors it as `tmp/fleet/foo-shokunin` (`:779-782`).
- `registry-replay.py --run` lists `siblings = ['/store/foo']` and mirrors it as `tmp/fleet/foo`
  (`:67`, `:161`).
- So a frozen row whose argv uses `../foo-shokunin/...` resolves under the runner but not under the
  replay. The replay then reports a different `got`/`held` for the same requirement. The two tools now
  hold **two authorities for sibling identity**.

Two aliases to one target (`F/a-shokunin` and `F/b-shokunin` both pointing to `/store/x`):
- The replay lists `/store/x` twice and the second `symlink_to` raises `FileExistsError`.
- The resulting uncaught traceback exits **1**. The tool documents exit 1 as "refused (findings)"
  (`:27`), so a crash is indistinguishable from a refusal by exit code. `registry-check` mirrors both names.

Siblings whose realpath lies outside `fleet_root` are also listed as outside paths in `observations.plan`.

Latent, not live: `find /home/vgpnk/Projects/shokunin -maxdepth 1 -name '*-shokunin' -type l` returned
nothing. In `.ufo/evidence/round-24/replay/observations.json`, `plan` shows all 20 siblings as
`/home/vgpnk/Projects/shokunin/<name>`, and `fleet_root` is canonical. The actual replay result is
unaffected.

### before.json honesty checks
- `git cat-file -e 6a1821a:tools/registry-replay.py` reports ABSENT. The K11 row reads
  `{"discriminated": false, "reason": "tool-absent"}`.
- `before.json.instrument_sha256 = 0a7f6daa…7daa64` matches `measure.py` at e338f1b and at c8c5b88.
  `measure.py`, `before.json` and `contract.json` all land in e338f1b, whose parent is 6a1821a
  (frozen before implementation commit d2eaecd).
- Caveat [INFERENCE]: `before.json` records the clone revision as an invocation parameter. HEAD of
  `/tmp/tameshi-r24-before-YdP3/lane` is not independently observed. The tool-absent outcome is
  consistent with 6a1821a regardless.
- Context: base `registry-check.py` already realpath-normalised the fleet root and self-exclusion
  (`6a1821a:tools/registry-check.py:762-783,1907`). The routed defect lived only in the round23 evidence
  instrument, which stays unchanged. So K11's 0→1 measures the existence of a new CLI, not the creation of
  a missing capability in the repo. Contract bound 3 ("K7-K11 test the new projection/plan CLI on
  synthetic fixtures") states this, so it is not misreported.

## Impacted axes
- **Calibration:** the K11 name and the downstream prose claim sibling normalisation that the predicate
  cannot discriminate (M4–M7).
- **Identity / duplicate authority:** `registry-replay` and `registry-check` disagree on sibling identity
  for symlinked siblings.
- **Provenance wording:** the knowledge row 20 and SKILL/SCORECARD claim "siblings" and "`..` alias"
  coverage without a discriminating case.
- **Exit semantics:** a duplicate-alias crash exits 1, which the tool documents as a refusal.

This is a fixable defect, not a tradeoff. The ruler is frozen, so it cannot change this round.

## Smallest safe correction
1. **Pick one sibling-identity authority.** Reuse the `registry-check.py:776-782` convention in
   `plan()`:
   - `siblings = sorted(os.path.join(fleet, p.name) for p in Path(fleet).glob('*-shokunin') if p.is_dir() and os.path.realpath(p) != real)`
   - Mirror at `fleet/p.name`.
   - This removes the rename and the duplicate-alias crash.
2. **Reword the claim in every place it appears:** "realpath-normalises lane and fleet root; siblings
   keep their fleet names; the lane is excluded by realpath". The places are the docstring `:13`, the
   knowledge row 20, `SKILL.md:2047` and `SCORECARD.md:1124,1137,1150`.
3. **Add one selftest case** (the selftest is not frozen): a symlinked sibling `fleet/peer-shokunin -> store/peer`,
   plus a regular file `fleet/junk-shokunin`. Assert the sibling stays `real/peer-shokunin` and the file
   is excluded. If option 1 is rejected and realpath siblings are kept instead, the same case must assert
   `store/peer` and the duplicate-alias path must exit 2, not crash with 1.
4. **For a future frozen ruler** (not this round), extend the K11 fixture with:
   - a symlinked sibling;
   - a second sibling, to cover sort order;
   - a non-suffix directory and a `*-shokunin` regular file;
   - a symlinked component before `..`, to separate M5.

   Do not count it as a K11 re-pass in round24.
