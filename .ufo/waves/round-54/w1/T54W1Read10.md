# T54W1Read10 — cold-read report

- Item: cold-read the SKILL.md section whose heading is ``### The operator's runbook — `corpus/knowledge/operator-runbook.md` `` (byte-exact as frozen)
- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- cand (C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- section span printed by `.ufo/waves/round-54/reader-section.py`: `start=1304 end=1324` (the hashed bytes are lines 1304–1323; the frozen round-18 `sectionize` strips the trailing blank line and joins with `\n`, no trailing newline)
- `section_sha256`: `c246d3743e0a441224ece3e2dcc195a359f365e23a9e757fe0441a5ea71055ed`
- Same value from the frozen round-18 `sectionize` loaded directly at C0 (cross-check below), so the JSON pin is the counter's own definition, not a reimplementation.
- Scratch: `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read10` (created, used, removed at the end).
- Lane files edited: **none**. This seat wrote only its two deliverables under `.ufo/waves/round-54/w1/`.

## Findings (2)

### F1 — the pin cell on the pointed-at document does not resolve at C0

Quote (byte-exact, `SKILL.md:1306`):

```
`e1e349b6…` / 511 L / 31 416 B,
```

Why: The pointer's governing digest `e1e349b6…` resolves to no git object and to no file at C0 (`sha256sum corpus/knowledge/operator-runbook.md` at C0 is `8b2e185f…` over 516 L / 33 515 B with a clean `git status`), and the pinned 511 L / 31 416 B matches only the 2026-10-14 version at `606716f7…`, so the cell cannot be checked against the file it names.

What I opened and checked:

- `git show 59c3810:corpus/knowledge/operator-runbook.md | sha256sum` and `| wc -lc` → `8b2e185f…`, `516 33515`; `git rev-parse 59c3810:corpus/knowledge/operator-runbook.md` → blob `54c72164…`; `git status --porcelain -- corpus/knowledge/operator-runbook.md` → empty.
- `git rev-parse --verify 'e1e349b6^{commit}'` and `'e1e349b6^{blob}'` → both fail ("not a commit" / "not a blob").
- Every version of the path from `git log --all -- corpus/knowledge/operator-runbook.md` (10 commits, five distinct blobs) hashed with `sha256sum` and counted with `wc -lc`: only `606716f703f7699af458476a31fc78ddc9bf552c` yields `e1e349b69d798acb1d037db9c437709f8b679fd46ac32c441304a9c26a05914c`, `511 31416` — i.e. the cell pins that version while the section points at the live path, and no command in the section maps the digest to a revision.
- The parenthetical's `uncommitted worktree file at this read` clause points the same way: at C0 the path is a committed blob in the C0 tree and the worktree is clean, so the status sentence no longer describes the file either (recorded as support for F1's currency, not filed as a separate finding).

### F2 — the rendering/divergence anchor lands on unrelated text

Quote (byte-exact, `SKILL.md:1319`):

```
`service-limits.md` (`:1250-1254`)
```

Why: Bare `:…` anchors are this page (`:1273`), and at C0 `SKILL.md:1250-1254` is the intake-precondition / re-pin text citing `corpus/knowledge/service-optin-protocol.md:59-62`, while the rendering/divergence rule for `service-limits.md` sits at `:1276-1277`, so the cited range does not resolve to the rule it names.

What I opened and checked:

- `git show 59c3810:SKILL.md | sed -n '1249,1256p'` → `:1250` "never an edit of the recorded table.", `:1251-1254` the intake-precondition bullet citing `service-optin-protocol.md:59-62`. No rendering/divergence sentence in the range.
- `git show 59c3810:SKILL.md | sed -n '1272,1277p'` → `:1276-1277` "this page is the compact rendering, and a divergence between the two is the finding, never smoothed." That is the rule the sentence names; `:1276-1277` is the resolving anchor at C0.
- The same drift exists at base `d33053f7552d` (`:1250-1254` there is the "What a re-sweep produces lands appended" passage), so the range is a standing stale cite, not a C0-only artefact.
- The runbook states the same rule at `operator-runbook.md:9-11` and cites `SKILL.md:1249-1254` for it — also stale at C0, which corroborates that the line range drifted while the rule text moved to `:1276-1277`.

## Sweep: claims opened and found sound (no finding filed)

- **Section map §0–§10 + append-only errata.** `grep -n '^#\{1,3\} '` over the C0 runbook lists `## 0.`…`## 10.` and `## Errata (append-only)`; every named row (quick start, service in one page, the tool, six-case ledger, opt-in protocol, limits, cadence, regression mode, full loop, executed receipts, unknowns carried) exists with the stated content.
- **"§6 the cadence (… triggers T1–T3)".** `operator-runbook.md:288-293` defines T1/T2/T3 inside §6. Resolves.
- **"`cf41efaa…` (r7-1, four legs)".** ER-R1 (`operator-runbook.md:486-500`) names tool `cf41efaa8be5f52d…` (r7-1); §7's executed receipt (`:378`) and §9 (`:446`, `cases=4 passed=4`) give the four legs. `cf41efaa…` is a sha256 of `tools/mutate-and-run.sh` (the runbook's stamp table `:22` pins `cf41efaa8be5f52d`, 1341 L / 61 632 B), not a git revision — `git rev-parse cf41efaa` fails as expected for a file digest, and the section's phrasing is consistent with ER-R1's "tool `cf41efaa8be5…` (r7-1)".
- **"errata ER-R1/ER-R2 record the r10-2 edit in motion".** `operator-runbook.md:486-512`: ER-R1 records `4b3dfed5…` (VERSION r10-2, uncommitted, +217/−49 vs `b8eb96e`), ER-R2 records `5807fd38…` still in motion, "remedy is unchanged".
- **"name the T2 remedy (re-run under the new revision, record both pins)".** ER-R1 `:497-500` says exactly "T2 is the fix — when the edit lands, re-run `--selftest` and `--regression` under the new revision and record both pins". Resolves.
- **"The receipt below is that T2 record."** The next section (`SKILL.md:1355-1375`) records `--selftest` `80/80` and a six-leg `--regression` at tool `75ed934d…`, and restates the superseded pin `cf41efaa…` (`:1370`) — both pins are present, so the T2 identification is defensible.
- **"It adds no gate measurement of its own; every line restates an anchored source."** The runbook states the same rule for itself at `:8-11` and `:459-460`; no counter-claim found in §0–§10 while reading the headings and the §7/§9 receipts.
- **Cross-reference to `lost-headings-at-base.json` / `lost-headings-at-c0.json`.** This heading is in both lists, so it is in the frozen re-read set; no lane file was touched.

## Commands and outputs (receipt)

Reader span and digest:

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read10 \
  python3 .ufo/waves/round-54/reader-section.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  59c38109bf119d0e9d4f878644a82babc937bc1e \
  "### The operator's runbook — `corpus/knowledge/operator-runbook.md`"
{"heading": "### The operator's runbook — `corpus/knowledge/operator-runbook.md`", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1304, "end": 1324, "section_sha256": "c246d3743e0a441224ece3e2dcc195a359f365e23a9e757fe0441a5ea71055ed"}
```

Frozen round-18 sectionize cross-check at C0 (same `sha`, `start 1304 end 1324`):

```
sha c246d3743e0a441224ece3e2dcc195a359f365e23a9e757fe0441a5ea71055ed
start 1304 end 1324
```

F1 evidence:

```
=== E1: live pointer target at C0 ===
8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859  -
    516   33515
blob:
54c72164fa76f0a00f3b0bf1a2af6a87518a326b
status:
(end status)

=== E2: the pinned digest is an older version ===
e1e349b6 not a commit
e1e349b6 not a blob
e1e349b69d798acb1d037db9c437709f8b679fd46ac32c441304a9c26a05914c  -
    511   31416
```

(The E2 block's last two lines are `git show 606716f703f7699af458476a31fc78ddc9bf552c:corpus/knowledge/operator-runbook.md | sha256sum` and `| wc -lc`.)

F2 evidence:

```
=== E3: SKILL 1249-1256 at C0 (what :1250-1254 lands on) ===
  1249	  re-measure at the live revision, or record the STALE cell with its reason —
  1250	  never an edit of the recorded table.
  1251	- **The intake precondition round 8 named is present, not errata.** The opt-in
  1252	  protocol carries the re-pin rule — "A moved substrate needs a re-pin, never a
  1253	  re-interpretation of the old table"
  1254	  (`corpus/knowledge/service-optin-protocol.md:59-62`) — cited here.
  1255	- **What a re-sweep produces lands appended.** The outcome lands as an appended
  1256	  row or errata block in

=== E4: the rendering/divergence rule for service-limits.md is at 1272-1277 ===
  1272	a refusal without an anchor is not written; the table states refusals, it does not
  1273	adjudicate them. (Anchors `:…` are this page; `PROVINCE.md` is repo-relative; other bare note names are under `corpus/knowledge/`.) The
  1274	standalone note `corpus/knowledge/service-limits.md` (T9-2, round 9) carries
  1275	the same rows as the detail of record — verbatim anchor quotes, the trigger column
  1276	and the intake-precondition check; this page is the compact rendering, and a
  1277	divergence between the two is the finding, never smoothed.
```

Runbook heading map at C0:

```
1:# Operator runbook — the tameshi mutation service, end to end (round 10, T10-1)
35:## 0. Quick start — the operator loop in one block
65:## 1. The service in one page
93:## 2. The tool — `tools/mutate-and-run.sh`
131:## 3. The six-case ledger — the standing view
180:## 4. The opt-in protocol — running/commissioning a sweep
243:## 5. The limits — what the service refuses
269:## 6. The cadence — the tick, the reading map, the triggers
345:## 7. The regression mode — replaying the recorded legs
408:## 8. The operator's full loop — commissioning to append
438:## 9. Receipts from this writing — what was actually executed
462:## 10. Unknowns carried — the service's open questions
481:## Errata (append-only)
```

Tooling: no install or upgrade was needed; the pacman pause was not approached and nothing was filed. The linux host toolchain already present (`git`, `python3`, `sha256sum`, `wc`, `sed`, `grep`) covered every check.
