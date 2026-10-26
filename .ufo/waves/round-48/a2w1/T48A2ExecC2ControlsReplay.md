# T48A2ExecC2ControlsReplay — C2 controls replay (round 48, a2w1)

Seat: T48A2ExecC2ControlsReplay (leaf). Item: replay the C2 controls and attack CTL_H.
Lane repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `473336d9d789f6081195e7376d17836a24666bc3`,
content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17`, date 2026-10-26.
Read-only on the lane; the only file written is this report.

## 0. Verdict

- **Replay reproduces the committed receipt exactly.** After normalising only `rev=<40-hex>` the replay
  output and `.ufo/evidence/round-48/control/c2-controls.stdout` are byte-identical
  (sha256 `382e31554108c523f32839a9dde60d1cc9ae68b29dec839f9abb0164be639869` for both). `CTL_F=0`,
  `CTL_G=0`, `CTL_H=2`, `CONTROLS ... ok=true`, exit 0 — as committed.
- **CTL_H fails only for the phrase rule.** For S048 and S093 every check graded before `phrases` prints
  `ok`, and `entries` (graded after `phrases`) also prints `ok`; counterfactual probes that change only
  the phrase-bearing inputs flip each NOT to REFRESHED. No second failure reason exists at the frozen
  counter bytes.
- **The control's pass/fail is much weaker than its receipt text.** The scored condition at
  `control/c2-controls.py:265` reads only `refreshed`, is one-sided (`<= 2`), and ignores
  `census_exit`; S026/S108 are not discriminated at all (their round-45 quotes already carry the
  required phrases) and S093's quote sits exactly on the 25-word ceiling. Three mutants below pass the
  control while changing what the control means (F1-F3). The receipt-line diff is the real gate; the
  script's exit code is not.

## 1. Command, pins, provenance

Replay command (as assigned; `TMPDIR=$S`):

```
S=/fast/scratch/hyaku/tameshi-r48/T48A2ExecC2ControlsReplay
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/control/c2-controls.py \
  --work "$S/c2" \
  --measure /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/freshness/measure.py
```

Pins verified (sha256):

| artifact | worktree | at freeze `7552984` | at content rev `c7586b9` |
|---|---|---|---|
| `.ufo/evidence/round-48/freshness/measure.py` | `faefe9b4…` | `faefe9b4…` | `faefe9b4…` |
| `.ufo/evidence/round-48/control/c2-controls.py` | `46b8c039…` | `46b8c039…` | `46b8c039…` |
| `c2-controls.stdout` | `18ff473d…` | — | `18ff473d…` (identical) |
| `c2-controls.meta` | `fb0e9a7e…` | — | `fb0e9a7e…` (identical) |
| `c2-controls.exit` | `9a271f2a…` | — | `9a271f2a…` (identical) |

`c2-controls.meta:1` records `scored_at_freeze_bytes=7552984 (… measure.py sha256 faefe9b4)`. The receipt,
meta and exit landed in the content-revision commit `c7586b9`, i.e. before this wave, exactly as the item
states. The counter and the control script we replayed are the frozen bytes.

## 2. Replay output and comparison

```
  F | TARGET S026 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
  F | TARGET S048 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
  F | TARGET S093 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
  F | TARGET S108 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
  F | C2_R48: self_pin=0 targets=4 refreshed=0 census_exit=0 live=off rev=473336d9d789f6081195e7376d17836a24666bc3 C2_R48_PARTIAL=false
CTL_F refreshed=0
  G | TARGET S026 row=S265 snapshot=absent receipt=- quote=- phrases=- entries=- live=skipped NOT
  G | TARGET S048 row=S266 snapshot=absent receipt=- quote=- phrases=- entries=- live=skipped NOT
  G | TARGET S093 row=S267 snapshot=absent receipt=- quote=- phrases=- entries=- live=skipped NOT
  G | TARGET S108 row=S268 snapshot=absent receipt=- quote=- phrases=- entries=- live=skipped NOT
  G | C2_R48: self_pin=1 targets=4 refreshed=0 census_exit=0 live=off rev=3b7c7bbb2dd219006352d5e084dfad62fc0b9b97 C2_R48_PARTIAL=false
CTL_G refreshed=0
  H | TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
  H | TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=missing entries=ok live=skipped NOT
  H | TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=missing entries=ok live=skipped NOT
  H | TARGET S108 row=S268 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
  H | C2_R48: self_pin=1 targets=4 refreshed=2 census_exit=0 live=off rev=ec6de59c5d10870886550435c04f700adedddd8c C2_R48_PARTIAL=false
CTL_H refreshed=2
CONTROLS: F=0 G=0 H=2 expected=F0,G0,H<=2 ok=true
```

- Every `TARGET`, `C2_R48`, `CTL_` and `CONTROLS` line matches the committed receipt
  (`.ufo/evidence/round-48/control/c2-controls.stdout:1-19`) after `sed -E 's/rev=[0-9a-f]{40}/rev=<SHA>/g'`
  on both sides (`diff -u` empty; both normalised files hash to `382e3155…`).
- Differences are exactly the three `rev=` shas the item allows: G `3b7c7bbb…` vs committed `a865909b…`,
  H `ec6de59c…` vs `b83f2424…`. Both committed shas are clone-local: `git -C LANE cat-file -t` reports
  "could not get object info" for each, while `473336d…` is a commit. F's rev is BASE and matches exactly.
- `CTL_F self_pin=0` is correct and not a discrepancy: `.ufo/evidence/round-48/freshness/measure.py` does
  not exist at BASE (`git cat-file -t BASE:.ufo/evidence/round-48/freshness/measure.py` → "exists on disk,
  but not in `473336d…`"). F is driven by `row=none` anyway.
- Determinism: a second independent replay into `$S/c2b` produced a byte-identical normalised output
  (`diff` empty). The receipt is reproducible.

## 3. Attack on CTL_H

### 3.1 What H builds, and what it leaves alone

H commits, on top of BASE in the scratch clone (`control/c2-controls.py:224-263`): the four rows S265-S268
(`teaches` opens `supersedes T —`, opened 2026-10-26, status mined, source+anchor URL set ⊇ T's base URL,
anchor carries `sha256 <12hex>`), the round-45 `.raw.gz` bytes re-labelled
`sources/T.snapshot.html.gz` (`:238`), receipts it writes itself with `fetched_at 2026-10-26T00:00:00Z`,
`http_status 200`, `sha256` = those bytes (`:247-250`), the four gate lines whose quotes are the round-45
ledger quotes verbatim (`:98-103`), the entries re-pointed to the new row with `verified-at: 2026-10-26`
(`:105-127`), and the counter itself at `SELF_PATH`.

### 3.2 Per-target mechanism at H

| target | row | quote (collapsed) | words | required phrase(s) present |
|---|---|---|---|---|
| S026 | S265 | `about 84% of the transitions we observe from pass to fail involve a flaky test` | 15 | `84%` **yes** |
| S048 | S266 | `If a mutation was previously killed, but the class or killing test has changed` | 14 | `should therefore be prioritised` **no** |
| S093 | S267 | `< option >--unshare-user-try</ option > …` (five option groups) | **25** | `--unshare-all` no, `--unshare-cgroup-try` no |
| S108 | S268 | `可以通过使用参数 --test_arg=--update_goldens … .expected 文件。…` | 6 | `--update_goldens` **yes** |

This matches the contract line `contract.json:122` verbatim: "the round-45 quotes re-used verbatim
(S048 and S093 lack their required phrases) -> refreshed<=2". H lands on the ceiling exactly, `2`.

### 3.3 Does it fail for anything other than the phrase rule? No.

Evidence 1 — field by field. `phrases` is only evaluated when `quote == 'ok'` (`freshness/measure.py:426-427`),
and `entries` is evaluated unconditionally after it (`:428`), so for S048/S093 the printed
`quote=ok … phrases=missing entries=ok` means: noline/line/empty/word-count/located all passed, the phrase
rule failed, and the entry re-pointing (source names R, verified-at 2026-10-26, used-by set unchanged)
passed. `row`, `snapshot`, `receipt` passed for all four.

Evidence 2 — counterfactual probes with the frozen counter (`faefe9b4…`), H tree cloned into `$S/probe/lane`,
`--no-live`:

- **P1 (S048 only).** Replace the `- C2-QUOTE S266 S048: …` line with the content revision's S048 quote
  `then it is likely that the last killing test will still kill it and it should therefore be prioritised above others`
  (21 words; a literal substring of the same round-45 snapshot text). Nothing else changed.
  Result: `TARGET S048 … quote=ok phrases=ok entries=ok … REFRESHED`, `refreshed=3`.
- **P2 (S093 only).** The H snapshot's extraction cannot hold both S093 flags inside 25 words (minimal
  token window is 34, because the rendered GitHub page yields `< option >`/`</ option >` tokens after the
  strip-tags-then-unescape order of `measure.py:243-252`). So P2 replaces the S093 snapshot with the content
  revision's `.ufo/evidence/round-48/freshness/sources/S093.xml` (sha256 `2cb77df2f4be…`, 33,289 bytes,
  committed at `c7586b9`), names it `S093.snapshot.xml`, updates the S267 anchor sha12 and the receipt
  sha256/bytes to match, and sets the S267 gate quote to the content revision's 25-word quote.
  Result: `TARGET S093 … snapshot=ok receipt=ok quote=ok phrases=ok entries=ok REFRESHED`, `refreshed=3`.
  (An earlier attempt kept the `.gz` name over raw XML and printed `snapshot=gzip` at
  `measure.py:255-259` — the selftest's `snapshot_bad_gzip` behaviour, not a control defect.)
- **P3 (P1+P2).** `refreshed=4`, `C2_R48_PARTIAL=true`, exit 0 — i.e. H's fixture passes the whole predicate
  once the phrase-bearing inputs are correct.

P2 is a compound probe (it swaps the bytes the quote must be located in); P1 is single-field. Together they
show that no other rule blocks either failing target. `--no-live` throughout: probes, never verdicts.

### 3.4 Two structural limits of the H signal

1. **Half the control is not exercised.** S026's and S108's round-45 quotes already contain their required
   phrases (table 3.2), so those two targets pass every rule. H discriminates only S048/S093, and it
   saturates its ceiling (`2`) exactly — there is no headroom. Any future change that also drops S026 or
   S108 is invisible in the scored number.
2. **S093's quote sits on the word-count boundary.** It is exactly 25 whitespace tokens (five
   `< option >`, `--unshare-…</`, `option`, `>` groups), i.e. exactly `MAX_WORDS` (`measure.py:100`). A
   counter with `MAX_WORDS = 24` produces `H | TARGET S093 … quote=25w phrases=- … NOT`, `CTL_H refreshed=2`,
   `CONTROLS … ok=true`, exit 0 (mutant M4). H's *scored* outcome therefore cannot name the mechanism that
   fired; only the receipt-line diff can.

## 4. Findings

Each finding names the artifact and the command that shows it. All mutants are scratch copies of the
frozen counter under `$S/mut`; the frozen bytes were never modified.

### F1 (medium) — the control's pass condition is one-sided, so over-rejection passes

`control/c2-controls.py:265`:
`ok = f_refreshed == 0 and g_refreshed == 0 and 0 <= h_refreshed <= 2`.
Any counter that rejects S026 and/or S108 for an unrelated reason still satisfies it. Witness M1: in
`measure.py:86-91` set `REQUIRED['S026'] = ('84%', 'zzz-unreachable-phrase')` and
`REQUIRED['S108'] = ('--update_goldens', 'zzz-unreachable-phrase')`; the H branch then prints
`H | TARGET S026 … phrases=missing`, `H | TARGET S108 … phrases=missing`, `CTL_H refreshed=0`,
`CONTROLS: F=0 G=0 H=0 … ok=true`, exit 0. A counter that rejects all four (e.g. the phrase check made
impossible) is indistinguishable from the intended "rejects exactly the two phrase-less quotes".

```
python3 .ufo/evidence/round-48/control/c2-controls.py --work "$S/mutwork-m1" --measure "$S/mut/m1_overreject.py"
```

### F2 (medium) — H cannot separate the phrase rule from the word-count rule at S093

`control/c2-controls.py:12` (H expected `refreshed<=2`), `freshness/measure.py:100` (`MAX_WORDS = 25`),
`freshness/measure.py:292-308` (quote grading) and `:243-259` (extraction order). The H S093 quote is exactly
25 tokens composed of markup artifacts, so it is simultaneously a phrase-rule fixture and a boundary fixture.
Witness M4: `MAX_WORDS = 25 → 24` yields
`H | TARGET S093 row=S267 snapshot=ok receipt=ok quote=25w phrases=- entries=ok live=skipped NOT`,
`CTL_H refreshed=2`, `CONTROLS … ok=true`, exit 0 — the S093 failure reason moved off the phrase rule with no
change to the control's verdict.

```
python3 .ufo/evidence/round-48/control/c2-controls.py --work "$S/mutwork-m4" --measure "$S/mut/m4_maxwords24.py"
```

### F3 (low-medium) — the harness never reads `census_exit` (or `self_pin`)

`control/c2-controls.py:185-190` parses only `refreshed=(\d+)` from the counter's text, and `:265` scores only
that number. The counter's own verdict requires `census_exit == 0` and `self_pin == 1`
(`freshness/measure.py:446-448`). Witness M3: `measure.py:96` `CENSUS` → `/nonexistent/sources-census.sh`;
all three controls print `census_exit=127` in their `C2_R48` line and the script still prints
`CONTROLS … ok=true`, exit 0. Consequence for this round: the committed receipt does show `census_exit=0`,
so the receipt is sound, but the harness exit code cannot attest that a future run had a working census.

```
python3 .ufo/evidence/round-48/control/c2-controls.py --work "$S/mutwork-m3" --measure "$S/mut/m3_nocensus.py"
```

### F4 (low) — the script's default counter path does not exist

`control/c2-controls.py:40-41` defaults `--measure` to `control/T48ExecC2Counter.measure.py`; that directory
contains only `c2-controls.py` and `run-controls.py`. A bare invocation exits before cloning:

```
$ python3 .ufo/evidence/round-48/control/c2-controls.py --work "$S/bare"
measure not found: /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/control/T48ExecC2Counter.measure.py
exit=1
```

The committed stdout never names the counter; identity lives only in `c2-controls.meta:1`
(`freshness/measure.py sha256 faefe9b4`, `scored_at_freeze_bytes=7552984`). The assigned replay is possible
because the item and the meta name the path — not because the artifact is self-describing.

### F5 (risk, not a control failure) — H shows the snapshot/receipt pair is self-pinned

H commits round-45 bytes as the round-48 snapshot and writes the receipt fields itself
(`control/c2-controls.py:238-250`). The counter prints `snapshot=ok receipt=ok` for all four (receipt lines
13-16) because `check_receipt` (`measure.py:257-289`) compares only against the row's own anchor/url and
`check_live` (`measure.py:336-350`) only asks whether the quote still occurs at the URL — it never compares
the live bytes to the snapshot digest. So a stale snapshot plus a fabricated 2026-10-26 receipt plus a quote
that is still live would pass even the deciding invocation. What C2 proves is "the quote is still live at
that URL", not "this snapshot is this run's fetch". For H this is by design; recorded so H's
`snapshot=ok receipt=ok` is not read as provenance evidence. Show it with the replay itself:
`git -C "$S/c2/lane" show <H>:.ufo/evidence/round-48/freshness/sources/S026.receipt.json` reports
`sha256 29db1f1c…`, the sha256 of BASE's `.ufo/evidence/round-45/freshness/sources/S026.raw.gz`.

## 5. Clean negatives (things checked and not findings)

- No other-reason failure in any control line; `entries` really did run after the phrase failure
  (`measure.py:428`), so its `ok` is evidence, not a skipped default.
- CTL_F and CTL_G reproduce exactly, including `row=none` / `snapshot=absent` and the G `self_pin=1`.
- Two independent replays agree byte-for-byte; the receipt is deterministic.
- Lane untouched: `c2-controls.py` writes only under `--work` (clone at `:167-174`, commits at `:181-190`);
  every lane access is `git -C LANE show` or `git clone --shared LANE`. The lane's `control/` bytes and
  `freshness/measure.py` still hash to their committed values after the replay. Nothing was written under
  `corpus/`, `tools/` or `SCORECARD.md`.
- `c2-controls.exit` = `0` matches the replay exit 0, and `c2-controls.stderr` is empty (replay stderr empty).

## 6. Environment, bounds, cleanup

- Scratch: `S=/fast/scratch/hyaku/tameshi-r48/T48A2ExecC2ControlsReplay`, `TMPDIR=$S`; clones via
  `git clone -q --shared`; no fixture repos were needed beyond the clones; nothing under `/tmp`.
- Disk guard before the passes: `/fast` 25% used, 602.4 GB free; no ENOSPC.
- Every counter run was `--no-live`, into scratch trees. The deciding invocation is the L1's; no verdict is
  claimed here.
- Tools: none installed or upgraded (nothing was needed).
- Scratch directory deleted before this report was finalised; the only retained artifact is this file
  (`.ufo/waves/round-48/a2w1/T48A2ExecC2ControlsReplay.md`).
