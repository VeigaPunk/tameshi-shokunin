# RGSpecA — C1 class A: verdict-line paths and their pin style (wave-1 draft)

Seat: TameshiR16.RGSpecA. Scratch: `/tmp/tameshi-r16-RGSpecA-7lyrkj/`.
Spec fragment written: `.ufo/waves/round-16/w1/RGSpecA.spec` (3 defects, spec v1).

## Materialization & pin verification

```
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > /tmp/tameshi-r16-RGSpecA-7lyrkj/round-gate.mjs
sha256sum → f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  ✓ matches pin
wc -l → 1511
```

## Baseline (pristine control, the one allowed run)

`node /tmp/tameshi-r16-RGSpecA-7lyrkj/round-gate.mjs --selftest` → exit 0,
`ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS` (node v24.21.0, ~3.3 s).
No mutant was run; all predictions below are pre-registered projections from
`corpus/knowledge/arm-class-matrix.md` §13 plus pinned-byte reads.

## Class A surface (from the pinned blob)

Four verdict-line families, four pin styles (§13.2):
- audit/close emit `:676-679`; `parseVerdict` anchored full-line regex `:863`;
  verdict read as **last non-empty stdout line** `:861`; 10 `parseVerdict`
  call sites: `:879 :891 :900 :979 :1010 :1051 :1059 :1131 :1297 :1311`.
- tracked emit `:575-576`; full-line regexes rt1 `:1411`, rt2 `:1426`;
  **prefix-only** regex rt8 `:1481`.
- FAIL-CLOSED emit `:617`; token-only pins `:1188 :1193 :1198 :1206 :1218`,
  rt3 `:1435`, rt5 `:1450`; detail probes fcE `:1212`, rt3 `:1436`.
- selftest tail `:1505-1506`; shape + `VERDICT: PASS` equality `:1399-1400`.

## Candidates (all @old verified count==1 with a Python literal `str.count` on the pinned bytes)

### A1 — KILLED (predicted)
`round-gate.mjs:677` — swap `lane=`/`checks=` in the audit/close verdict line.
`@old (round=${round} lane=${opts.lane} checks=${items.length}` count=1.
`@new (round=${round} checks=${items.length} lane=${opts.lane}`.
Reason: `parseVerdict` `:863` demands `lane=` immediately after `round=N `;
regex no longer matches → `v === null` in every parseVerdict assert
(`:882 :892 :901 :981 :1012 :1053 :1060 :1134 :1299 :1313`). Exit codes and
`parseFindings` kindsEq are unaffected. Probes the anchored-equality pin —
the strongest of the four styles.

### A2 — SURVIVED (predicted)
`round-gate.mjs:617` — decorate the FAIL-CLOSED detail tail:
`@old ROUND_GATE: FAIL-CLOSED (${token}) ${detail}` count=1.
`@new ROUND_GATE: FAIL-CLOSED (${token}) detail: ${detail}`.
Reason: every fail-closed assert needs only the `(TOKEN)` literal or a bare
token (`:1188 :1193 :1198 :1206 :1218 :1435 :1450`), and fcE/rt3's detail
probes (`/no upstream|exit 128/` `:1212`, `/filed=1 round-<N>\/kumitate\.md/`
`:1436`) are substring tests whose needles survive the `detail: ` prefix.
Exit `2` (`:618`), stderr (`:615`, unread by any check), and the `--json` path
(`:616`, jFc `:1279-1285`) untouched. Probes the §13.2/§13.5 "asserted stem,
unasserted remainder" echo on the refusal path.

### A3 — KILLED, differential (predicted)
`round-gate.mjs:575-576` — reorder the tracked verdict tail fields.
`@old lines.push(\`ROUND_GATE: ${verdict} (mode=tracked checked=${checked}\`\n      + \` errors=${errors} warnings=${warnings})\`);` count=1.
`@new` swaps `errors=`/`warnings=` on the second segment.
Reason: emitted line becomes `… checked=2 warnings=0 errors=0)` / `… warnings=0 errors=1)`.
rt1's full-line regex `^ROUND_GATE: CLEAN \(mode=tracked checked=(\d+) errors=(\d+) warnings=(\d+)\)$` `:1411` → `m === null` → rt1 fails;
rt2's `^ROUND_GATE: DRIFT \(mode=tracked checked=2 errors=1 warnings=0\)$` `:1426` → fails.
rt8's prefix-only regex `^ROUND_GATE: CLEAN \(mode=tracked checked=2 ` `:1481` still matches → **rt8 stays green**,
and rt7 reads `--json` `:1468-1475` → green. Kill signature is exactly {rt1, rt2}:
probes the full-line vs prefix pin-width gradient inside one verdict family (§13.2).

## Bounded recommendations

- If the ledger wants one more class-A leg, a `VERDICT: ` → `VERDICT:  ` edit at
  `:1506` is a fourth-family probe (predicted KILLED by hermeticity `:1399-1400`
  exact-equality only — narrowest kill signature in the class); declined here to
  hold the 3-candidate budget.
- `verdictLine`'s last-non-empty-line convention (`:861`) is itself a single-edit
  KILLED candidate (`lines.push` → `lines.unshift` at `:677`; fails exactly the
  parseVerdict-on-run-with-findings checks r3/r11/r14/r19/r20) — noted for a
  sibling class if positional-pin coverage is wanted.
- No defects overlap sibling classes (enum kinds, token emit sites, constants);
  all three are inside the four named verdict-line families.

## Evidence not taken

- No mutant was executed (pre-registration precedes the sweep; L1 runs it).
- Counts: `grep -F -c` and `str.count` both = 1 for each @old; `parseVerdict`
  call-site list is complete (10 sites, grep `:879..1311`).
- §13 is projection; line numbers cited were re-verified against the pinned blob
  this session.
```
Tool installs: none.
```
