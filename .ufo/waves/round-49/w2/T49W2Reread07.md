# T49W2Reread07 — C1 map semantic reread

Reviewed candidate `f181a961ae44061af486f600e5ea257d2baf78f8`. The candidate `reads.json` contains map ordinals 9–17 (no ordinals 18–20); all nine are recorded in `T49W2Reread07.json`.

## Unsupported excerpt findings

- **Ordinal 9 — `tools/mutate-and-run.sh`**: `SKILL.md:1391` describes `--selftest`, `--regression`, the six/seven/eight/nine-leg progression, and git-materialized replay. The row excerpt only quotes the regression leg list and git-show replay; it does not support `--selftest` or the historical progression. The target contains those details elsewhere, but this row's excerpt does not. Show the section and excerpt with:
  ```sh
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:SKILL.md | nl -ba | sed -n '1391p'
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:tools/mutate-and-run.sh | nl -ba | sed -n '215,220p'
  ```
  Observed: SKILL line 1391 names both modes and historical leg counts; tool lines 215–220 quote only `--regression`, nine legs, and the git-show materialization.
- **Ordinal 10 — `corpus/README.md`**: `SKILL.md:1392` claims a row per carried note, holds/sources, appended addenda, partial coverage, and one uncarried knowledge note. The excerpt is only the Coverage map heading and `Note | Holds | Sources` header, so it does not establish the row coverage/addendum/partial-coverage claims. Show the section and excerpt with:
  ```sh
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:SKILL.md | nl -ba | sed -n '1392p'
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:corpus/README.md | nl -ba | sed -n '3,5p'
  ```
  Observed: README lines 3–5 are just the map heading and table header. A candidate-tree inventory independently confirms the correction's factual disclosure: 59 knowledge Markdown files, one unmentioned (`corpus/knowledge/r44-anchor-refresh-rule.md`).

## Corrections reviewed

- **`SKILL.md:1392` — OK.** The wording qualifies coverage as partial and explicitly names the one uncarried note. Candidate README has the stated table columns and an appended addendum; inventory shows exactly one unmentioned knowledge note (`corpus/knowledge/r44-anchor-refresh-rule.md`). The amendment makes the earlier universal “one row per note” claim appropriately bounded.
- **`SKILL.md:1393` — OK.** The added `plans/round-11.plan.md` concrete pointer resolves and its opening identifies round 11 as the final round. `N` plan/record-draft placeholders do not resolve; all round-4 through round-10 plan/record-draft pairs exist. `plans/completion-evidence.md` is present and candidate history attributes it to the round-11 closeout commit. The correction clarifies the existing map rather than changing its purpose. Show the plan inventory and completion-pack history with:
  ```sh
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only f181a961ae44061af486f600e5ea257d2baf78f8 -- plans/
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%h %s' f181a961ae44061af486f600e5ea257d2baf78f8 -- plans/completion-evidence.md
  ```
  Observed: round-11 plan and completion pack are present; the history names the closeout commit. Neither `plans/round-N.plan.md` nor `plans/round-N-record-draft.md` exists in the candidate tree.

Other rows 11–17 (except unsupported ordinal 10) support their corresponding map assertion or are correctly marked `absent` for the `N` placeholders. Full row-by-row reasoning is in the JSON deliverable.

## Summary
- Reread candidate map ordinals 9–17; ordinals 18–20 are absent.
- Unsupported excerpts: ordinal 9 (`tools/mutate-and-run.sh`) and ordinal 10 (`corpus/README.md`).
- Both in-range corrections (SKILL.md:1392–1393) are factually sound and preserve meaning.
