# ConnectorSibling — golden-file update-flag overlap

## Finding

none

No sibling `PROVINCE.md` owns golden-file update flags. Do not route F4's explicit update-flag rule to another lane.

## Evidence

Scan surface: the 21 `PROVINCE.md` files directly under `/home/vgpnk/Projects/shokunin/*-shokunin/` (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi). `tameshi-shokukin/` has no `PROVINCE.md`.

Command (full-file line scan; pattern covers golden / `--update` / bless / `.expected` / expected-file / snapshot update-or-diff / visual regression / fixture update / regenerate):

```
python3 - <<'PY'
import os, re
root = "/home/vgpnk/Projects/shokunin"
pat = re.compile(r"(golden|update_golden|update-golden|--update|bless|INSTA_|\\.snap\\b|\\.expected|expected[- ]file|expected value|snapshot (test|updat|diff)|visual regression|fixture updat|regenerat)", re.I)
n = 0
for name in sorted(os.listdir(root)):
    p = os.path.join(root, name, "PROVINCE.md")
    if not os.path.isfile(p):
        continue
    n += 1
    for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
        if pat.search(line):
            print(f"{name}/PROVINCE.md:{i}")
print(f"provinces={n}")
PY
```

Observed hits: `provinces=21`, and only two lines:

- `game-dev-3d-shokunin/PROVINCE.md:62` — Frontier, not ownership: "Godot visual capture and visual regression need a real render path"; the Blender case is "only a bounded PNG hash". No update flag, no expected-file write.
- `tameshi-shokunin/PROVINCE.md:46` — this lane's own Adjacent refusal: "visual/UI snapshot diffing (rejected row S030 — the adjacent UI lanes)". A refusal is not a sibling Owns clause. game-dev-2d's province has no golden/snapshot/update-flag line.

A wider pass (golden|snapshot|bless|`.expected`|write path|expected value|regenerate) also hit evidence-bundle `--snapshot`, kake `scripts/live_snapshot.py` (GET HTML), kama probe snapshots, mado `expected.json` readers that write nothing (`mado-shokunin/PROVINCE.md:24-27`), mori PSI snapshots, souji "superseded config snapshots", and tsukuroi "pinned sibling snapshot". None names an explicit flag that updates a golden or expected file.

## Axes

- depth: improved as a no-harm clearance. F4's update-flag census stays lane-owned method; no sibling province already holds that flag.
- calibration: untouched. No predicate, guard regex, or SCORECARD command D change.

## Proposed move

Record the overlap as **none**. Keep the round-39 write-path census inside tameshi. Do not add a sibling owner, and do not treat `game-dev-3d-shokunin/PROVINCE.md:62` or `tameshi-shokunin/PROVINCE.md:46` as a concrete overlap.

## Risks

- The scan is current province bytes only. A later sibling append could claim the flag; this file would then be stale.
- `SKILL.md` and gate scripts were out of scope. A flag that exists only in a sibling tool, with no province Owns line, is not an overlap under this question.
- "Snapshot" collisions above are easy to misread as golden-file ownership. They are not.

## Verification

Re-run the command above. Pass condition: `provinces=21` and no line whose text says that lane owns an explicit golden / `.expected` update flag. The two printed lines must remain the visual-regression frontier sentence and tameshi's own adjacent refusal.
