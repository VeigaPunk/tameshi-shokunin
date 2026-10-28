# T56W2Read04 — cold read

Heading: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`

Candidate: `c0137451f5b7f22d65f748fc69f1b181f55e1378`

Section range: `SKILL.md:159-273`; SHA-256 (frozen round-18 `sectionize`): `77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da`.

## Finding

- Step 4 says “two of the JS ten share a class — the :47-48 pair.” The cited Kimi table has two shared classes, not one: D1/D2 are both grouped under `off-by-one` (`:44-45`; tally `off-by-one 1/2`), and D4/D5 are grouped under `dropped arm` (`:47-48`; tally `dropped arm 2/2`). Thus four of the ten defects are in duplicated classes. The parenthetical names only the latter pair. The Kagi example is consistent with its tally: only `dropped branch 1/2` is duplicated (`:70-71`).

Command and output:
```text
python3 - <<'PY'
import re, collections
p='corpus/knowledge/mutation-case-kimi-census.md'
lines=open(p, encoding='utf-8').read().split('\n')
for i in (44,45,47,48,55,56,57): print(f'{i}: {lines[i-1]}')
PY
44: | D1 | off-by-one count | ...
45: | D2 | off-by-one count (findings cap) | ...
47: | D4 | dropped arm | ...
48: | D5 | dropped arm (presence gate) | ...
55: By class: off-by-one 1/2 · inverted condition 1/1 · dropped arm 2/2 · wrong mode pin 1/1 ·
56: weakened predicate 1/1 · wrong exit mapping 1/1 · weakened secrecy pin 1/1 · wrong
57: reported constant 0/1.
PY
```

## Notes

- Step 5 describes a historical `--check` gate and requires literal `all unique`; the cited `mutate_driver.py` is not in this tree, while `bash tools/mutate-and-run.sh --check` fails with exit 64 (`mutate-and-run: unknown argument: --check`). The maintained driver's apply path prints `APPLY OK`/`APPLY FAIL`, not `all unique`. Restore discipline item 6 discloses the historical driver is one-off/not in-tree, but this section does not identify a runnable replacement for a new sweep.
- The taxonomy section immediately following this one says “One defect per class per sweep” (`SKILL.md:276-278`), while this section says “at least one per class” and points to exemplars with repeated classes. Clarify which rule governs a new sweep.
- The repeated-class parenthetical omits Kimi D1/D2 (`:44-45`) despite the note's own `off-by-one 1/2` tally; the finding records the resulting undercount.
- The Kimi “model” citation names §1, §3-§6 but omits §2 (surviving-defect analysis), even though step 8 cites material from §2 (`:82-99`).
- The recipe's scratch path matches Standing rules (`$HYAKU_SCRATCH/<lane>-r<round>/<sub>/`); the older `/tmp/<lane>-r<round>-<n>-work/` form remains in the historical Kill-rate bands section and appendices.

## Commands run

- `python3` loaded `.ufo/evidence/round-18/measure.py` via `importlib`, loaded `SKILL.md` from C0 with `git show`, and called the frozen `sectionize`; result: `start=159 end=273 sha256=77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da`.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md` and read the section end-to-end.
- Read every cited line range in `corpus/knowledge/mutation-case-kimi-census.md`, `corpus/knowledge/mutation-case-kagi-census.md`, `corpus/knowledge/gates-survey-kumitate.md`, `corpus/knowledge/gates-survey-kagi.md`, `corpus/README.md`, and `tools/mutate-and-run.sh`; all cited ranges exist and resolve.
- `git status --porcelain -- SKILL.md` → exit 0, empty output.
- `bash tools/mutate-and-run.sh --check` → exit 64, `mutate-and-run: unknown argument: --check`.
- `timeout 240 bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`, `VERDICT: PASS`, exit 0.
- Ran a two-defect scratch fixture through `tools/mutate-and-run.sh`; it recorded `DEFECT D1: SURVIVED (exit=0)` when the mutant printed `SELFTEST: FAIL (1 cases)`, illustrating the exit-only verdict behavior described in notes.
- `python3 .ufo/evidence/kaika-round-1/coldread/check_uniqueness.py <spec> <target>` → `all unique`, exit 0; this is a frozen evidence script with a different CLI, not the maintained sweep driver's `--check` mode.
- `timeout 300 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0.
