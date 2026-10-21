# CorpusErrataCarry — round24 W1 (critic, read-only)

Seat: TameshiR24-2.CorpusErrataCarry. Delivered revision c8c5b88c8e961a929cdc351b95a7074c76958909, base 6a1821a8897eea6e7d9669292160ec9593669409.
Target: round23 Errata A–D and the QUALITY47 limits (instrument-supplied argv/cwd/revision, 41+2 rows, bundle-declared requirements) are preserved, and no round24 text contradicts them.

## Verdict

No defect found. All four errata and every QUALITY47 limit are carried forward, and no round24 text contradicts them. The round24 replay's own artifacts reproduce the round23 limits exactly, so nothing relies on wording alone. There is one calibration risk, which is not a defect: the round24 lesson's after-record has not been written yet, and that record is where a contradiction could still appear (see the correction section).

## Evidence

Append-only and unchanged inputs:
- `git diff 6a1821a c8c5b88 -- corpus/QUALITY.md SKILL.md SCORECARD.md corpus/README.md corpus/SOURCES.md | grep -c '^-[^-]'` returns `0`, so no existing line was removed or edited.
- `git diff --quiet 6a1821a c8c5b88 -- .ufo/evidence/round-23 corpus/lessons/round-23.md` succeeds, so the round23 lesson (Errata A–D at lines 143–168) and all round23 evidence are byte-unchanged.
- `corpus/knowledge/required-command-binding.md` is not in the diff stat, so its knowledge erratum is unchanged.
- QUALITY46 and QUALITY47 (`corpus/QUALITY.md:457–485`) are untouched. QUALITY48 (`:488–502`) neither narrows nor widens them.

### Erratum A and QUALITY47: receipt argv, cwd and revision are invocation parameters

- In code, `tools/registry-replay.py:172–173` copies `argv` from the source row, sets `cwd=str(clone)` and sets `revision=head`. Lines 102–104 project those copies into the receipts. The docstring at `:16–17` states this limit.
- In the actual round24 replay bundle, every `receipt.argv` equals its `requirement.argv` (43/43, `True`). There is one cwd, `/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin`, and one revision, `d2eaecd…`. The `replay-gate.json` verdict of 0/[] therefore tests only exit and stdout, as Erratum A says.
- The round24 text agrees: `replay-projection-hardening.md:30–31` ("not observed process metadata"), the SKILL.md round24 addition ("Receipt argv, cwd and revision remain instrument-supplied") and the tool docstring.
- No round24 text cites the round24 replay as argv evidence. I grepped the added lines for `observed|isolated|authentic|R17-CMD-BIND|41|43`; the only hits are negations.
- Argv discrimination still rests on a substituted-command pair. `command-binding-source-read-red-pinned` (`tools/registry.json`, new row) keeps the round23 source-read argv with expect `1` / `ARGV_MISMATCH` and adds `bundle_sha256` `db620668…`. That value equals `sha256sum .ufo/evidence/round-23/source-read-bundle.json`. The round24 K1/K2 fixtures (`extra-cases.json:71,138`) are synthetic.
- The pinned frozen-clean row (`3d6c99b7…`, equal to `sha256sum .ufo/evidence/round-23/replay/bundle.json`) is not presented as argv discrimination anywhere.

### Erratum B and QUALITY47: 41 revision-pinned rows plus 2 live-dependent, not isolated

- `.ufo/evidence/round-24/replay/live-dependent.json` reads `{"live_dependent": ["pin-disposition-read", "verify-round15"], "revision_pinned": 41, "rows": 43}`. This is exactly the Erratum B partition.
- `observations.json` agrees: both rows have `external=True`, and `pin-disposition-read` also carries `non_hermetic_argv` `['/home/vgpnk/Projects/shokunin']`. All 43 rows hold.
- I tried to find a counterexample: a row among the 41 that reads live sibling content without a flag.
  - `bash-witness-count` reads kagi only through `git -C kagi show <40-hex rev>:corpus/surface-census.sh` (`tools/bash-witness-study.py:342–354`), so its content is pinned to a revision.
  - `defect-probes-selftest` clones the live kagi repo through the mirror, then requires the pinned `REV_BASH` commit (`.ufo/evidence/round-18/defect-probes.py:817–835`).
  - Neither row reads unpinned live content, so the 41+2 claim stands as a split by declared flag.
- No round24 text calls the replay isolated:
  - `replay-projection-hardening.md:35–37`: "Realpath identity is not write isolation".
  - SKILL.md round24 row, write scope: "fleet mirror symlinks live siblings".
  - `tools/registry-replay.py:18–20`: "not write-isolated from siblings".
  - Lesson `round-24.md:25` rejects "reading realpath identity as write isolation".
- Erratum B's write-scope fact still holds: the round24 `--out` was also inside the lane (`replay-command.json` argv). That matches the text and does not contradict it.
- The runner is still passed the live fleet root, as in round23. Round23 `replay.py:60` passes `args.repo.parent`; round24 `registry-replay.py:170` passes `layout['fleet_root']`, which resolves to `/home/vgpnk/Projects/shokunin` in `observations.json` `plan`.

### Erratum C and QUALITY47: the gate binds bundle-declared requirements, and the replay instrument freezes them

- The `tools/command-binding.py` diff touches only the selftest fixture loading (`:164–169`). Gate semantics are unchanged, so it still validates the requirements declared inside the bundle.
- The freeze check is still the instrument's comparison of two evidence-local files (`tools/registry-replay.py:137–146`):
  - `sha256sum .ufo/evidence/round-23/registry-baseline.json` gives `ebd2e69a…`, which equals `requirements.json` `registry_sha256` and observations `registry_sha256`.
  - `source_requirements_revision` is `28cae179…`, with 43 requirements.
- The text agrees. SKILL.md round24 row says "frozen requirement/registry digests come from the caller's files". The contract bounds and knowledge `:32–34` say that changing both the row and the bundle selects a new contract, which is the same as Erratum C's last sentence.
- Linkage is by digest, not by revision label:
  - The replay ran at `d2eaecd`, while the delivered revision is `c8c5b88`.
  - `git diff --stat d2eaecd c8c5b88 -- tools` is empty.
  - `git show <rev>:tools/registry-replay.py | sha256sum` gives `9fcd2dbb…` at both revisions and in the live tree, matching `replay-command.json`.
  - `command-binding.py` gives `9230c68e…` at both revisions, matching `replay-gate.json` `tool_sha256`.
  - The clone runner `cba16646…` equals `git show c8c5b88:tools/registry-check.py | sha256sum`.
  - The base gate digest is still `d533dc1e…` (`git show 6a1821a:tools/command-binding.py`), so round23's linkage is unaffected.

### Erratum D: route-mix citation

- No round24 file cites `route-mix-before.json` or `zai`. The grep of all added lines and of the round24 lesson, knowledge entry and contract found nothing.

### Supersession versus round23's "frozen argv/expect not silently altered" (round23 lesson :110–112)

- The three round23 rows change only `status` to `superseded` and add `superseded_by`. Their argv and expect are byte-identical.
- The stronger expectations live in new active rows, documented in SKILL.md, QUALITY48 and the knowledge entry. This is the registry's existing convention: the baseline already had 4 superseded rows, and `registry-check.py:30,875–883` runs superseded rows without counting them toward `held`, as the knowledge entry says.

## Smallest safe correction (calibration risk only)

`corpus/lessons/round-24.md` ends at line 53 with "The after measurement is recorded below once executed", and no after-record exists at c8c5b88. When L1 writes it, the record should do three things:
1. State that the round24 replay 0/[] (`replay-gate.json`, bundle `4f424023…`) tests only exit and stdout, because receipt argv, cwd and revision are instrument-supplied (Erratum A).
2. Report the 41 revision-pinned plus 2 live-dependent split from `replay/live-dependent.json`, and not call the replay isolated (Erratum B).
3. Cite the pre-execution freeze check on its own line, as QUALITY47 requires. `registry-replay.py --run` prints no line for that check; it is evidenced only by exit 0 together with `registry-replay.py:137–146` and observations `registry_sha256` `ebd2e69a…`, which equals `sha256(.ufo/evidence/round-23/registry-baseline.json)` and `requirements.json` (Erratum C).

## Scope notes

- Only read-only inspection was performed: Read/Grep, `sha256sum`, read-only `git show/diff/log` with `GIT_OPTIONAL_LOCKS=0`, and local JSON parsing.
- No gate, selftest, registry battery or replay was run, and nothing was written except this report.
- No tools were installed or updated.
- No claim is made of producer authentication, promotion, closure of historical R17-CMD-BIND, or numeric score uplift.
