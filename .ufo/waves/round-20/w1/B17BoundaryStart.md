# B17 — frozen receipt at edit-window start

## Findings

- **Axes:** boundary correctness, fixture isolation, reproducible evidence.
- Built a private `/tmp` fixture with a distinct frozen SHA (`a…a`) and installed SHA (`b…b`), with an edit interval of `2026-10-21T09:00:00Z`–`2026-10-21T09:30:00Z`. Its frozen-SHA receipt measured `08:30Z`–`09:00Z`, ending exactly at the edit-window start.
- Ran the staged gate `.ufo/evidence/round-20/stage/receipt-window.py` against those fixture files. **Exit: 0; verdict: CLEAN.** No production files were changed.
- **Agree:** the boundary is admissible. The gate rejects a frozen receipt only when its measurement end is *after* the edit start (`end > edit_start`, lines 189–192); equality does not satisfy that rejection condition. It therefore reports `WINDOW_OK` for the equality case.
- **Disagree:** none for this scoped boundary case.
- **Defects observed:** none in this case. This result covers only the frozen-SHA equality boundary, not the broader receipt population.

## Fixture paths

- `/tmp/tameshi-r20-b17-boundary-start-contract.json`
- `/tmp/tameshi-r20-b17-boundary-start-receipts.json`

## Command and observed output

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py --contract /tmp/tameshi-r20-b17-boundary-start-contract.json --receipts /tmp/tameshi-r20-b17-boundary-start-receipts.json --json; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"
```

```text
{"findings": [], "infos": [{"detail": "gate: frozen window respected", "id": "WINDOW_OK", "receipt": "frozen-at-edit-start"}], "receipts": 1, "schema": "tameshi-receipt-window-v1", "verdict": "CLEAN"}
EXIT=0
```

## Files and tooling

- Repository file written: `.ufo/waves/round-20/w1/B17BoundaryStart.md` (this report only).
- Temporary fixture files are under `/tmp`; staged instrument and lane production files were not edited.
- No tools were installed or updated. No blockers.
