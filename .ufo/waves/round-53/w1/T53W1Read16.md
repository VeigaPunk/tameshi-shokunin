# T53W1Read16 — cold read of `### Round-17 gate/probe registry — re-pin and monitor`

Seat: reader (wave 1, round 53). Content revision under test: **C\* = a41195dfc13a73958e4c5228ec196b28d03ded03**
(`round-53: C* content commit — fix pass, S275/S276 assimilation (re-opened this round), round-53 lesson, QUALITY 104, LOG r52+r53 entries, README F7 note`).

Deliverable JSON: `.ufo/waves/round-53/w1/T53W1Read16.json`.

## Section identity (frozen-monitor definition, not a hand split)

The section was not chosen by eye. I loaded the frozen splitter and ran it over the C\* blob bytes:

```
python3 -c 'import importlib.util; spec=importlib.util.spec_from_file_location("m18",
  "…/.ufo/evidence/round-18/measure.py"); m=…; m.sectionize(raw)'   # raw = git show C*:SKILL.md
```

`sectionize` (round-18 `measure.py:209-256`, the function the round-21 monitor delegates to) reports for this heading:

```
{"start": 1853, "end": 1861,
 "heading": "### Round-17 gate/probe registry — re-pin and monitor",
 "sha256": "ad2320cb7770e47aa5fa628f0a0aa96e751e42c821cff4fe9d0c9fe03af0dcd9"}
```

The section is 8 lines (heading, blank, table header, separator, four rows); line 1861 is the next heading (`## Input-keyed cold-read credit — round 17`), so `end=1861` is exclusive. Trailing whitespace-only lines stripped, joined with `\n`, no trailing newline.

Independent second check (same bytes, different code path — `sed -n 1853,1860p` of the `git show` dump, trailing newlines stripped, `sha256sum`):

```
ad2320cb7770e47aa5fa628f0a0aa96e751e42c821cff4fe9d0c9fe03af0dcd9
```

Both agree: **section_sha256 = ad2320cb7770e47aa5fa628f0a0aa96e751e42c821cff4fe9d0c9fe03af0dcd9**. Because 64 sections exist at C\*, the split is the monitor's, not mine, and it reproduces the heading's line range before hashing.

## Section text read (C\* bytes)

```
### Round-17 gate/probe registry — re-pin and monitor

| Name | Kind | Command | Exits |
|---|---|---|---|
| `tools/evidence-disposition.py` (v2 manifests) | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` (round 18; the round-17 manifest now exits 2) · `--selftest` | 0 clean · 1 failed expectations · 2 could not evaluate (invalid, missing, tampered or unprovenanced input) · 64 usage |
| `tools/registry-check.py` | gate | `python3 tools/registry-check.py --rev REV [--registry PATH] [--tag TAG] [--json]` · `--selftest` | 0 every active row held · 1 a row differs · 2 registry invalid, rev unresolvable or clone failed · 64 usage |
| `tools/mutate-and-run.sh` (guard + scrub) | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | as the round-16 row; a borrowed repo identity is SETUP 2 |
| `tools/pin-disposition.py` (branch tip) | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` · `--selftest` | as the round-13 row |
```

## Holds — pointers verified against C\* bytes

All object reads are `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C*:<path>`; the working tree was not used to establish any C\* fact.

1. **Every named path exists at C\*** (`git cat-file -e`): `tools/evidence-disposition.py` PRESENT, `tools/registry-check.py` PRESENT, `tools/mutate-and-run.sh` PRESENT, `tools/pin-disposition.py` PRESENT, `.ufo/evidence/round-18/dispositions.json` PRESENT, `.ufo/evidence/round-13/pin-manifest.json` PRESENT. (`.ufo/evidence/round-17/pin-manifest.json` is ABSENT, but the section never names it; the round-17 *dispositions* manifests it does allude to are present: `.ufo/evidence/round-17/dispositions.json`, `.ufo/evidence/round-17/dispositions-before.json`.)
2. **Documented flags exist in the shipped tools at C\*.** `registry-check.py`: `[--root DIR] [--rev REV] [--registry PATH] [--only NAME] [--tag TAG]... [--json]` and `--selftest` (docstring :11-13, USAGE :117-121). `pin-disposition.py`: `--manifest PATH --root FLEET` and `--selftest` (:148-149). `evidence-disposition.py`: `--root/--dispositions/--json/--selftest` (:167-168). `mutate-and-run.sh`: `--selftest`, `--regression` (:207, :1238-1240).
3. **Row 1 outcome map holds, measured with the C\* tool bytes** (`git show C*:tools/evidence-disposition.py` copied to scratch, `--root` = the lane):
   - `.ufo/evidence/round-18/dispositions.json` → **exit 0**, `status=clean`, `counts={effective:11, superseded:1, failed:0}` — matches "0 clean" and the registry row's needles.
   - `.ufo/evidence/round-18/dispositions-before.json` → **exit 1**, `status=failed`, `failed:1, findings:1` — matches "1 failed expectations".
   - The parenthetical "(round 18; **the round-17 manifest now exits 2**)" is **true at C\***: `.ufo/evidence/round-17/dispositions.json` → **exit 2**, `{"kind":"expected_input_digest_mismatch","message":"tools/bash-witness-study.py: observed cca77724… expects 49e9e5e2…"}`, and `.ufo/evidence/round-17/dispositions-before.json` → exit 2 for the same digest reason. This also corroborates line 1844's "round 17's two now exit 2".
   - Measurement fidelity: `HEAD` is `ace79e3df61266e9474e5c02086c0f7c79664580`, not C\*, but `git diff --stat C* HEAD -- .ufo/evidence/round-13/ .ufo/evidence/round-14/dispositions.json tools/mutate-and-run.sh tools/pin-disposition.py tools/registry.json .ufo/evidence/round-17/dispositions*.json .ufo/evidence/round-18/dispositions*.json tools/evidence-disposition.py` is **empty**, so every input these gates read is byte-identical between C\* and HEAD; the tool bytes are C\*'s.
4. **Row 2's `--selftest` and its exit-0/exit-1/64 clauses hold.** `registry-check.py --selftest` → `SELFTEST: PASS (51 cases)`, exit 0 (hermetic, TMPDIR bound to my scratch). Fixture registry with one active holding row → `REGISTRY_CHECK: held=1/1 superseded=1`, **exit 0**; unknown flag → `registry-check: unknown argument '--bogus-flag'`, **exit 64**. The code confirms the active-only tally: `held = sum(1 for f in active if f["held"]) … return (0 if held == len(active) else 1)` (:880, :884).
5. **Row 3's "as the round-16 row" resolves and its SETUP claim holds.** `tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`, `VERDICT: PASS`, exit 0. The borrowed-identity clause is real code: `printf 'REGRESSION_CASE %s: SETUP (repo_identity_mismatch: %s is not its own repository; toplevel=%s)\n'` (:1263), and a SETUP-only tally prints `REGRESSION: SETUP …` then `exit 2` (:1525-1529); usage is 64 (:250-254). The round-16 row it points at is `SKILL.md:1817`, whose exit map reads "selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage" — consistent.
6. **Row 4's "as the round-13 row" resolves and the documented invocation works.** The round-13 row is `SKILL.md:1559` ("0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate; selftest 1 failed"). Running the documented probe from C\*'s tool bytes, `--manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`: **exit 0**, 6 legs, `counts: {changed: 5, unavailable: 0, legs: 6}` and the literal needle `"unavailable": 0` appears in the JSON — i.e. exit 0 *including* changed observations, exactly as the round-13 row says. `pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0. That the row hard-codes the host fleet root instead of `FLEET` is not a violation here: the same absolute root is used by the round-13 rows (:1542, :1559) and by current rows at :1942-1943, :1957-1958, :1984-1985, :2143, and the tool's output carries it back as `"root"`.
7. **`evidence-disposition.py --selftest`** → `SELFTEST: PASS (66/66)`, exit 0 (matches the "66/66 cases" note at :2153).

## Finding (1)

Quote (byte-exact substring of the section, verified present once):

```
2 registry invalid, rev unresolvable or clone failed
```

**Class:** incomplete exit map — a documented flag's failure mode is missing.

**The statement that fails:** that exit 2 of `tools/registry-check.py` has only the causes *registry invalid*, *rev unresolvable* or *clone failed*. At C\* the same row publishes `--tag TAG` as part of the documented command, and a `--tag` selection that matches nothing exits **2** with a valid registry and no rev or clone in play:

```
$ python3 <C*:tools/registry-check.py> --root <fixture> --registry <fixture>/reg.json --tag nosuchtag --json
{
  "error": "--tag ['nosuchtag'] selects no registry row",
  "exit": 2,
  ...
}
REGISTRY_CHECK: could-not-evaluate (--tag ['nosuchtag'] selects no registry row)
exit=2
```

`--only NAME` (also published by the tool, `--only no-such-row` → exit 2) is the same case. The tool itself classifies these under 2 and distinguishes them from an empty pass — docstring at C\*, `tools/registry-check.py:53`: `2 could-not-evaluate (registry unreadable/invalid, root or rev missing, clone failure, --only/--tag miss)`, implemented at `:864-871` (`report["error"] = f"--tag {sorted(wanted)!r} selects no registry row"; return 2`). The SKILL cell is a stale abridgement of that map: it drops the `--only/--tag miss` cause for a flag it publishes one column earlier, so a cold reader who filters by tag and gets 2 is told the registry is invalid, the rev unresolvable or the clone failed — none of which happened.

Reproduce: any scratch fixture registry with one matching row, run the tool with `--tag <unmatched>`; exit 2 and the message above.

## Examined, not filed (recorded so the next reader does not re-open it blind)

- **"0 every active row held" vs "1 a row differs" asymmetry.** Only active rows decide the exit: a fixture whose sole active row holds and whose *superseded* row differs (`expect=0`, got=2) returns `REGISTRY_CHECK: held=1/1 superseded=1`, **exit 0**, and prints the superseded row without the `differs` token. Since the cell's subject is fixed in the first clause ("every **active** row held") and the tool prints `held|differs` only on active rows, I read "a row differs" as the tool's active-row token rather than an unqualified cause, and did **not** file it. It is, however, the exact state of this section's own round-17 row (superseded, `expect=0`, measured got=2), so the asymmetry is worth watching in wave 2.
- Row 1's parenthetical "2 could not evaluate (invalid, missing, tampered or unprovenanced input)" abbreviates the tool's fuller list ("invalid schema/type, or an unexpected internal failure", `:110-112`). Heading the list with the category name keeps it true; not filed.
- The heading says "Round-17" while the first row documents round-18 manifests. The heading names the section's origin and the row dates its own state ("round 18; …"), which the round's own rule (dated historical milestones are holds) covers.

## Limits of this read

- I did **not** replay the live registry (`registry-check.py --rev` over all 56 rows) or `mutate-and-run.sh --regression`: those execute the lane's rows (including ten regression legs) and belong to the executor seats; nothing here upgrades their claims into evidence. Consequently "0 every active row held" was verified as a *mapping* (fixtures + code), not as a fresh measurement of the live registry at C\*.
- `--tag`/`--only` miss behaviour was measured on synthetic fixture registries with C\*'s tool bytes, not on the live registry file (a `--tag` that matches nothing is not reachable against `tools/registry.json` without an exotic tag).
- No network, no repository writes, no pacman, no installs (python3 + git only). Scratch `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read16/` was used for every extracted blob, fixture and TMPDIR and is removed before this seat yields.
