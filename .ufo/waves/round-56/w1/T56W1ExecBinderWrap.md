# T56W1ExecBinderWrap — re-key bind wrapper (`bind.sh` for C1)

Axis: operability (milestone: re-key bind wrapper). Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`,
frozen instruments `c3e2ca9f020776b3d66c7af854fb82c834674fcf`. Everything below ran in `git clone
--shared` fixtures under `/fast/scratch/hyaku/tameshi-r56/T56W1ExecBinderWrap/`; the lane's
production files and the frozen `.ufo/evidence/round-56/` instruments were never edited. The only
lane paths written are this report, its receipts dir, and the deliverable below.

## Deliverable

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/bind.sh`
(`sha256 2d23f78bb8970df72f96c845857ddbc00c49c316cc5b848097d6a2ce75ea1030`, `set -euo pipefail`).
The exact command the L1 should run at bind time:

```bash
C0=<full 40-hex commit the readers read> PIN=<full 40-hex content-final commit> \
  bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/bind.sh
```

Optional env overrides: `WAVES` (default `.ufo/waves/round-56/w2`), `BIND_REV` (skip the script's
commit and measure an L1-made revision instead), `RESOLUTIONS` (opt into a findings-adjudication
file; default is a nonexistent path = strict zero-findings), `W` (receipt dir, default
`$HYAKU_SCRATCH/tameshi-r56/L1-bind`).

Sequence implemented: guards → (1) drift set at PIN via the round-21 monitor at floor
`0a2010acd1e9` and at PIN, **refuse (exit 3) unless it is exactly the 18 frozen headings** →
(1b) refuse any stale `rekey-r56-*` dir (C1 arm 3 counts `rekey-r56-*` dirs at REV and requires
exactly one) → (2) the round-55 binder with `--headings`, `--waves`, `--resolutions`, `--label`,
OUT=`rekey-r56-<C0:0:12>` → (3) refuse (exit 4) on binder non-zero exit, any `SKIP` line, a
`REFRESH` line ≠ `rekeyed=18 skipped=0 headings=18`, or wrong trace count → (3b) commit
`git add -A .ufo/evidence/round-21/coldread` (refuses exit 5 if anything outside that tree is dirty)
→ (3c) refuse (exit 6) if any input pinned in the emitted traces moved between PIN and the bound
revision → (4) the frozen round-48 precheck, `lost=0 ok` required (exit 7) → (5) the round-21
monitor: must read `64/64 score=8 box3=True` (exit 8); prints `BIND_PASS`.

### One deliberate deviation from the seat wording, with the reason

The item's step 4 says "re-run the precheck **at PIN**". The precheck — like every instrument —
reads git objects at a revision, and the binder writes `ledger.json` into the *working tree*, so a
precheck at PIN measures the *unbound* ledger and reads the same `lost=18 RED` step 1 just computed
(the drift-set computation IS the precheck's own mechanism: monitor at floor, monitor at cand,
credited-set difference). The script therefore commits the binder's output (the L1's own commit —
round-55's sequence did the same) and runs the precheck at the resulting `BIND_REV`; `BIND_REV=<rev>`
lets the L1 substitute its own commit. The wording is preserved in the header comment.

## Demonstrated, end to end

Scratch clone of the lane at the freeze rev `c3e2ca9f` (`--shared`), synthetic reader set of
18 JSON+MD pairs under `.ufo/waves/round-56/w2` named `T56W2DemoRead-NN.*` (the C1 arm-4 pattern
`T56W\d+.*Read.*\.json$`), `cand`=C0 and `section_sha256` computed with the frozen round-18
sectionize from the C0 blob. Commits (fixture only): C0 `07ba7ae349161d…`, PIN `b8ab3c4ae29313…`,
bind commit `f52ef5bb3e50d554c2b9dd2803266c128c8f7882` (receipts: `demo-a-bind.stdout`, `demo-a2-bind.stdout`):

| step | output |
|---|---|
| drift at PIN | `DRIFT headings=18 frozen=18 extra=0 missing=0` |
| binder | `REKEY` ×18 (inputs 11–7702 each, `dropped=0`) · `REFRESH rekeyed=18 skipped=0 headings=18` |
| pinned guard | `PINNED inputs=7721 changed=20 pinned-changed=0` |
| precheck at BIND_REV | `COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=f52ef5bb3e50 cand_credited=64 lost=0 ok` |
| monitor at BIND_REV | `MONITOR covered=64/64 score=8 box3=True trace_gate=strict overrides=False` |
| final | `BIND_PASS … headings=18`, exit 0 |

Post-bind ledger (fixture, `demo-a-ledger.txt`): 609 entries (= 591 + 18), exactly one `rekey-r56-*`
entry per frozen heading, all `read_rev=07ba7ae34916` (full C0), zero LOG.md/SCORECARD.md inputs
(arm 5 clean), 11,188 total bound input paths, re-key dir = 1.4 MB of traces.

The frozen C1 counter itself at the bound revision (`demo-a-c1.stdout`): `arm1-precheck exit=0
lost=0 ok`, `arm2 covered=64 score=8 box3=True`, `arm3 dirs=['rekey-r56-07ba7ae34916']`, `arm4
readers=18/18`, `unstable=0`, and `total=1` — the only failing arm is `arm6-restate`, which is the
L1's own SCORECARD row (a separate wave item, not the binder's output). Everything the wrapper
produces is arm-1..5 clean.

Second invocation of `bind.sh` over the same clone (same C0/PIN): `REFRESH rekeyed=18 skipped=0`,
ledger stayed at 609 entries — the replace rule holds; re-runs are safe and cheap (~170 s).

## Fragilities, each measured

1. **`--resolutions` default silently re-adjudicates with round-54's findings** — without the flag
   the binder reads `.ufo/evidence/round-54/integrate/resolutions.json`, which exists and grants
   1–11 findings to **ten of the eighteen** frozen headings (`## Standing rules` n=1,
   `## Mutation-sweep recipe` n=2, `### Round-21 gate/probe registry` n=11, `### Triggers T1–T3`
   n=1, `## The leg ledger` n=1, `## Effective expectation reconciliation` n=2,
   `### Round-15 gate/probe registry` n=1, `## Live-tree re-pin` n=1, `## Pin disposition` n=1,
   `### Round-13 gate/probe registry` n=1…). Demonstrated (`demo-b`): a reader with one finding is
   `SKIP reader-has-findings:1>0` under a nonexistent resolutions path (exit 1) but
   `REKEY … verdict=gap-minor minor_gaps=1` under the bare default (exit 0). `bind.sh` therefore
   defaults `RESOLUTIONS` to a nonexistent path (strict); a finding must be adjudicated by the L1
   explicitly, matching the contract's kill rule. **The L1 should keep this default** unless it
   deliberately opts in.
2. **Reader selection is first-match in sorted filename order and abandons the heading on the
   first problematic match.** A findings reader named `…-00` beats a clean reader `…-01` for the
   same heading: the binder SKIPs rather than binding the clean one (demo-d, `SKIP
   reader-has-findings`, exit 1). Same for `reader-md-missing`. Keep exactly one reader JSON per
   heading per wave dir, or be prepared to adjudicate.
3. **The binder writes the ledger even when it SKIPs.** On exit 1 the successful subset is already
   persisted to `ledger.json` and `OUT` — a partial bind exists that never committed. `bind.sh`'s
   error text says to restore or re-run; a second pass replaces, never grows (verified).
4. **`TMPDIR` must be set or the extracted `r18-binder.py` lands in `OUT`** and `git add -A` would
   commit it into the evidence tree. `bind.sh` exports `TMPDIR=$W/binder-tmp` for the binder call.
5. **`--waves` takes a single directory.** If the 18 readers land split across w2 and w3, one pass
   sees only one dir → `SKIP no-clean-reader`. Run `bind.sh` per wave (`WAVES=.ufo/waves/round-56/w3`)
   — the second pass binds the remainder under the same `rekey-r56-<c0>` dir (replace is per-heading).
   Readers must be committed and named `T56W*Read*.json` (arm 4); the binder's own glob is wider
   (`*.json`), so any other JSON carrying a `heading` key in the wave dir is a hazard — keep the
   reader-shape fields off non-reader reports.
6. **A pinned input that moves between PIN and the bound revision kills the section at REV** —
   the round-53/55 mechanism. `bind.sh` computes the intersection and refuses (exit 6).
   Demonstrated (demo-e): a SOURCES.md byte change committed after the bind → `PINNED
   inputs=7721 changed=21 pinned-changed=1 / PINNED-CHANGED corpus/SOURCES.md`, exit 6.
   Bound inputs total **7,721 distinct paths** — post-bind, the L1 may touch only LOG.md,
   SCORECARD.md, SKILL.md (dropped/ignored) and new files until the deciding revision.
7. **The drift guard stays exactly 18 under the round's own content edits** — measured (demo-c):
   SOURCES row + QUALITY criterion + registry cell + new knowledge file + `## Standing rules`
   rewrite committed at `d9d89ec2…` leaves `DRIFT headings=18 extra=0 missing=0 exact=True`
   (`## Standing rules` flips to `no-ledger-entry` because its bytes changed — expected; the other
   17 stay `input-drift`). Analytic check at base: no credited section's full crediting-entry set
   pins `corpus/SOURCES.md`, `corpus/QUALITY.md`, `tools/registry.json`, `SCORECARD.md`, or
   `LOG.md` — so the mandated C2 content does not widen the set. But `tools/mutate-and-run.sh`
   (17 sections), `SHONEN.md` (1), and `corpus/README.md` (1) **would** kill credit if edited at or
   before PIN; the exit-3 guard will name them if anyone does.
8. **`set -e` ordering**: the binder's pipe to `tee` must run under `set +e` or the script dies with
   the binder's exit 1 *before* the SKIP-classifying message — fixed in the delivered file (first
   version had it). Also: a mid-run edit of bind.sh while it executes shifted byte offsets and
   produced a spurious `line 184: syntax error` — rerun cleanly, not a defect.
9. **Untracked wave artifacts refuse the commit** (exit 5): `git status --porcelain` must show only
   `.ufo/evidence/round-21/coldread/` paths at commit time — this deliberately prevents the R55.6
   class (uncommitted round work) and means the L1 must commit w2 deliverables *before* binding.

## What the L1 must do before running it

- `PIN` must carry every content edit to any of the ~7,700 input paths (`corpus/SOURCES.md`,
  `corpus/QUALITY.md`, `tools/registry.json`, `tools/*` — the frozen heading reasons name the
  drifted sets; new files are inert, LOG/SCORECARD/SKILL are dropped).
- 18 reader reports committed at or before PIN in `--waves` dir: `heading`, `cand` = full C0,
  `section_sha256` = section sha at C0 (not at PIN — the bytes must be the same anyway; a SKILL.md
  section-byte change between C0 and PIN invalidates both reader sha and bound entry sha).
- After the bind: SCORECARD's last `| calibration |` row must state `8`, name a commit ≤ REV whose
  monitor score is 8, cite the round-21 monitor, and name round 56 (arm 6; the L1's remaining work).
- Reader findings must be adjudicated to zero or explicitly opted into via `RESOLUTIONS=<file>`.

## Sweep / hygiene

- Nothing written outside the assigned paths: `bind.sh`, this report, `T56W1ExecBinderWrap-receipts/`.
- No lane mutation: all `git add`/`commit` ran inside `git clone --shared` fixtures after asserting
  `git -C <clone> rev-parse --show-toplevel == <clone>`.
- Frozen instruments read only; `tools/receipt-revision-gate.py` untouched.
- Census (context, not this seat's gate): `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → exit 0, `tameshi ok`.
- No tools installed or upgraded; no pacman transaction attempted.
- One inbound IRC `DISALLOWED` from `C2Floor` (not my L1, no question) — recorded, not acted on.
- Lane bounds held: no subagent dispatched; the absent labrat key respected (no spawn needed — all
  falsifiers ran locally).
- Timing on this host: full `bind.sh` pass ~170–310 s; the binder alone ~40–60 s for 18 headings
  (~11k path probes ×2 git calls); each monitor run ~15–45 s; the precheck ~60–200 s.

## Residual risks

- Arm 4 cannot see whether a reader actually read its section (the contract's `cannot_see`); the
  synthetic reader set proves binding mechanics, not reading. Real readers land in wave 2.
- If wave-3 carries more content edits, the L1 re-runs the whole script over the new PIN; the
  replace rule keeps the ledger stable.
- `rekey-r56-*` uniqueness is enforced at PIN and in the working tree; a second dir created between
  PIN and REV by hand would still break arm 3 — nothing guards REV after BIND_REV; re-run before
  deciding.
