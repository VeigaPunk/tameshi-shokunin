# T54W2Sent02 — sentinel attack: forge a trace input (round 54, wave 2)

Item: "in a scratch clone at C1, hand-bind an entry whose trace records a wrong sha for one
input and show the frozen C1 counter refuses to credit it (`trace-input-drift`). Then bind one
whose `live_lane_reads` names a live path at a wrong digest and show `live-lane-read` fires."

Result: **both guards fire, with exact reason strings, and a control shows the second guard is
digest-sensitive rather than path-sensitive.** One trust-boundary observation is reported below
(`.git/` namespace), plus a provenance measurement on arm 4 that is already superseded by the
lane's amendment 3 and one residual constraint it leaves.

## Pinned instrument (the lane moved while this seat ran)

The lane was live during the attack: `HEAD` advanced `097985c` → `4e2de731b5` (amendment 3) →
`fe70474dac`. To keep the receipts immune to that, all runs below use a copy of the counter
extracted from a single commit, and the copy is checked against the freeze manifest:

| file | sha256 of the bytes run | freeze.json at HEAD |
|---|---|---|
| `.ufo/evidence/round-54/c1/measure.py` (extracted from `4e2de731b5`) | `d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812` | `d7749f84…5812` — **match** |
| `.ufo/evidence/round-54/c1/lost-headings-at-base.json` | `a953d2e87116effc943f56a532b785cae8c8f44a104635083634c05fe0b8bb10` | same — **match** |
| `.ufo/evidence/round-18/measure.py` at C1 (the frozen credit rule arm 3 delegates to) | `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` | same — **match** |
| `.ufo/evidence/round-21/coldread/measure.py` at C1 (the selector that prints per-section reasons) | `657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb` | same — **match** |

`c1/measure.py` and `freeze.json` at HEAD are unchanged from `4e2de731b5`, so the pinned copy is
current (`git diff 4e2de731b5 HEAD -- .ufo/evidence/round-54/c1/measure.py` is empty).
`SKILL.md` is byte-identical at C1 `99c3bc88d704` and at `4e2de731b5`/`fe70474dac`.

## Verdicts

| run | change held constant vs. baseline | counter verdict |
|---|---|---|
| baseline | hand-bound re-key, no forgery | `credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 total=0 C1_R54_PASS=true` |
| **R1** | one trace input digest changed `…f992` → `…f990` | `credited=63 lost=1 rekeyed=6/7 readers=7/7 total=3 C1_R54_PASS=false` → `trace-input-drift:corpus/SOURCES.md` |
| **R2** | `live_lane_reads` names the live lane `SKILL.md` at a wrong digest | `credited=63 lost=1 rekeyed=6/7 readers=7/7 total=3 C1_R54_PASS=false` → `live-lane-read:/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md` |
| R3 (control) | same live path, digest of the bytes at REV | `credited=64 lost=0 rekeyed=7/7 readers=7/7 total=0 C1_R54_PASS=true` → `credited` |
| R4 (observation) | `live_lane_reads` names a **nonexistent** `.git/` path at all-zeros | `C1_R54_PASS=true` → accepted (see Observation C) |

## Fixture

Built only inside `D=$(mktemp -d /fast/scratch/hyaku/tameshi-r54/T54W2Sent02/pinned.XXXXXX)`:

```
git clone --shared --quiet --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin "$D/clone"
git -C "$D/clone" -c advice.detachedHead=false checkout --quiet 99c3bc88d704566197783f66b211ee0a830e0330
git -C "$D/clone" rev-parse --show-toplevel        # asserted == $D/clone before every mutation
python3 .ufo/waves/round-54/w2/T54W2Sent02-receipts/build-fixture.py "$D/clone" 99c3bc88d70… <lost-headings>
```

`build-fixture.py` appends one entry per SKILL.md section that the committed ledger does not
credit at C1 (23 of 64), each with `sha256` = the section sha at C1, `class: "instruction"`,
`verdict: "executed-ok"`, `commands_executed_count: 1`, `read_rev` = C1, `inputs`
`{"corpus/SOURCES.md": 4a466c10d6bb4935d20b8fb74a2d4ec08b315ceb67a2896a83f84e5d1258f992}`
(the real digest of that blob at C1), and a trace under
`.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/traces/`. It also writes the seven wave
reader reports for the frozen headings pinned to C1. Baseline fixture commit:
`e26cd9304a6a94decbbdbd881aeaafb64d6074eb`.

Baseline run (instrument `d7749f84…`):

```
$ python3 /fast/scratch/hyaku/tameshi-r54/T54W2Sent02/code/c1/measure.py \
    --lane "$D/clone" --rev e26cd9304a6a94decbbdbd881aeaafb64d6074eb --work "$D/w-base2" --explain
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=e26cd9304a6a cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor exit=0 covered=64 score=8
EXPLAIN arm3-rekey dirs=['rekey-r54-99c3bc88d704'] c0=99c3bc88d704566197783f66b211ee0a830e0330
EXPLAIN arm4-readers 7/7
C1_R54: rev=e26cd9304a6a c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
EXIT=0
```

The baseline matters: the forgery is refused **against a tree the counter otherwise passes**, so
the refusal is attributable to the forged byte and not to some other arm.

## Attack A — `trace-input-drift`

Frozen rule, `.ufo/evidence/round-18/measure.py` at C1, lines 415–417:

```python
        for key in sorted(rec_inputs, key=str):
            ...
            if view[key] != rec_inputs[key]:
                return 'trace-input-drift:%s' % key
```

`view` is the entry's `inputs` (the digest the frozen input gate has just verified against the
blob at REV); `rec_inputs` is the trace receipt's own claim. The attack changes **one hex digit
of the receipt's claim only** — the entry still pins the true digest:

trace `.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/traces/section-03.json`
(entry `## Standing rules`), baseline bytes:

```json
{
 "inputs": {
  "corpus/SOURCES.md": "4a466c10d6bb4935d20b8fb74a2d4ec08b315ceb67a2896a83f84e5d1258f992"
 },
 "schema": "tameshi-trace-inputs-v1"
}
```

R1 bytes (`…f990`, last digit flipped):

```json
{
 "inputs": {
  "corpus/SOURCES.md": "4a466c10d6bb4935d20b8fb74a2d4ec08b315ceb67a2896a83f84e5d1258f990"
 },
 "schema": "tameshi-trace-inputs-v1"
}
```

`sha256(git cat-file blob 99c3bc88d704:corpus/SOURCES.md)` = `4a466c10…f992`, so `…f990` is a
well-formed but false digest for a real input.

R1 verdict (fixture commit `ee6a527d86b5d3fcb37ec818653cfb0bcb7bfac5`):

```
$ python3 …/code/c1/measure.py --lane "$D/clone" --rev ee6a527d86b5d3fcb37ec818653cfb0bcb7bfac5 --work "$D/w-R1" --explain
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=ee6a527d86b5 cand_credited=63 lost=1 RED
EXPLAIN arm2-monitor exit=0 covered=63 score=6
EXPLAIN arm3-rekey dirs=['rekey-r54-99c3bc88d704'] c0=99c3bc88d704566197783f66b211ee0a830e0330
EXPLAIN arm4-readers 7/7
C1_R54: rev=ee6a527d86b5 c0=99c3bc88d704 credited=63 lost=1 rekeyed=6/7 readers=7/7 monitor=6/63 unstable=0 total=3 C1_R54_PASS=false
```

Per-section reason from the unchanged round-21 selector at the same rev:

```
$ python3 "$D/clone/.ufo/evidence/round-21/coldread/measure.py" --repo "$D/clone" --rev ee6a527d86b5 --explain
covered=63/64 score=6
    section '## Standing rules' credited=False vetoed=False reasons=['trace-input-drift:corpus/SOURCES.md']
    MISSING '## Standing rules' reason=trace-input-drift:corpus/SOURCES.md
```

**Verdict A: PASS — the frozen counter refuses to credit the forgery, `rekeyed` drops 7/7 → 6/7,
and the reason string is exactly `trace-input-drift:corpus/SOURCES.md`.** Note the forgery is
caught independently by arm 1's frozen round-48 precheck (`cand_credited=63 lost=1 RED`), and by
source inspection the `NOHARM coldread-floor` monitor (`no-harm.sh:16`, requires
`credited>=64`) would also go RED; I did not execute `no-harm.sh`.

## Attack B — `live-lane-read`

Frozen rule, same file, lines 420–422 and 432–456:

```python
            for key in sorted(live_reads, key=str):
                if not live_read_bound(repo, rev, key, live_reads[key]):
                    return 'live-lane-read:%s' % key
...
def live_read_bound(repo, rev, path, digest):
    ...
    rel = os.path.relpath(real, root).replace(os.sep, '/')
    if rel == '.git' or rel.startswith('.git/'):
        return True
    ...
    raw = cat_file_blob(repo, rev, rel)
    return raw is not None and hashlib.sha256(raw).hexdigest() == digest
```

R2 makes the receipt *claim* a live read of the lane's real `SKILL.md` at a digest that is not
its digest (`a7a12053…a46d` = sha256 of an unrelated string; `sha256(SKILL.md at C1)` =
`b5ff9727…a195`):

```json
{
 "inputs": {
  "corpus/SOURCES.md": "4a466c10d6bb4935d20b8fb74a2d4ec08b315ceb67a2896a83f84e5d1258f992"
 },
 "live_lane_reads": {
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md": "a7a12053c4b7f700e1373ed00679b0d60c1f9dd6018e8cf42ce95067c92da46d"
 },
 "schema": "tameshi-trace-inputs-v1"
}
```

R2 verdict (fixture commit `94e862a86120b3e5bbbbab55837fdaf1c76042cc`):

```
C1_R54: rev=94e862a86120 c0=99c3bc88d704 credited=63 lost=1 rekeyed=6/7 readers=7/7 monitor=6/63 unstable=0 total=3 C1_R54_PASS=false
covered=63/64 score=6
    MISSING '## Standing rules' reason=live-lane-read:/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md
```

**Verdict B: PASS — `live-lane-read` fires on exactly the named live path.**

Control R3 (`dc1f10bea41468906220e108efd51920349f27d7`) binds the *same* live path to the digest
of the bytes at REV (`b5ff9727…a195`) and is credited again:

```
C1_R54: rev=dc1f10bea414 c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
    section '## Standing rules' credited=True vetoed=False reasons=['credited']
```

So the guard is digest-sensitive, not path-sensitive: the same absolute live path passes or fails
purely on the recorded digest. That is what the claim says it does.

## Observation C (low) — the `.git/` namespace accepts any digest, including a path that does not exist

`live_read_bound` returns `True` for every path under the lane's `.git/` **before** any digest
comparison (`round-18/measure.py:448-449`, quoted above). R4 records a live read of
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.git/objects/does/not/exist` at
`0000…0000` (64 zeros) and the counter still passes (commit `6a2dae9743812e1cc2f0d448a9abb43759ad2b45`):

```
EXPLAIN arm3-rekey dirs=['rekey-r54-99c3bc88d704'] c0=99c3bc88d704566197783f66b211ee0a830e0330
EXPLAIN arm4-readers 7/7
C1_R54: rev=6a2dae974381 c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
EXIT=0
```

This is documented intent ("object-store/ref reads … are accepted as such"), so it is not a
contradiction of the frozen text; the finding is narrower: **the `live_lane_reads` digest is
never verified for `.git/` paths, and even a nonexistent path is accepted**, so a receipt's
claim about *which* object-store bytes it read is unverifiable. It does not defeat credit on its
own — the entry's own `inputs` must still verify at REV — so severity is low. If the L1 wants the
claim to mean "the bytes read are the measured bytes" for every live read, the `.git/` arm needs
the ref/object name resolved and compared, or the receipt must not record a digest it will not
check.

## Observation D (informational) — arm 4 provenance, and the `c0` constraint it leaves

I probed arm 4 before noticing the lane had already amended it. Committed the 23 honest wave-1
reports (all `cand = 59c38109bf11…bc1e`, all pinning C0 section bytes) into `w1/` of a baseline
that otherwise passes:

- `c0 = C1` (`rekey-r54-99c3bc88d704`): `rekeyed=7/7 readers=0/7 … C1_R54_PASS=false`
- `c0 = C0` (`rekey-r54-59c38109bf11`): `rekeyed=7/7 readers=2/7 … C1_R54_PASS=false`

Cause: arm 4 requires `cand == c0` **and** `section_sha256 == ` sha of the section at REV
(`c1/measure.py:241`); 5 of the 7 frozen sections changed between C0 and C1, so no C0-produced
report can satisfy both. Amendment 3 (`4e2de731b5`, `WAVE_DIRS = (…/w1, …/w2)`, freeze.json
amendment 3: "found by wave-2 seat T54W2Exec04") removes the unsatisfiability by letting wave-2
reports count.

**Residual constraint the fix leaves:** arm 4 still pairs `cand == c0` with the sha at REV, so
the re-key directory must be named for **C1** (`rekey-r54-99c3bc88d704`). Naming it for C0 keeps
`readers=2/7` even after amendment 3, because every C1-pinned wave-2 report would fail
`cand == c0`. My E2 measurement is the receipt for that.

## Sweep — what I tested and did not find

- Entry-side input verification is independent and stayed honest in every run: the entry kept the
  true `corpus/SOURCES.md` digest, so only the receipt's claim was ever false.
- The `.git/` observation is the only live-read path that skips the digest; a normal live file is
  compared (`SKILL.md` R2 vs R3), and a live path outside the lane root is rejected outright
  (`live_read_bound` first guard). I did not attempt to weaken `LIVE_LANE_ROOT`.
- I did not re-run the frozen `round-18/measure.py --selftest`; the cases it asserts
  (`trace-missing`, `trace-invalid`, `trace-input-unrecorded`, `trace-input-drift`,
  `live-lane-read`, live-read-bound) are covered above end-to-end through the C1 counter.
- Real-lane context (not a finding): at C1 `99c3bc88d704` and at `097985c` the counter reads
  `credited=41 lost=23 … C1_R54_PASS=false` with `rekeyed=0/7`, because no `rekey-r54-*`
  directory and no committed reader report exist there yet. The round is pre-binder, so this is
  the expected pre-deciding state, not a claim failure; it is why the baseline above had to be
  hand-bound before the guard could be isolated.

## Bounds and tooling

- Lane writes: only `.ufo/waves/round-54/w2/T54W2Sent02.md` and
  `.ufo/waves/round-54/w2/T54W2Sent02-receipts/`. `git status` in the lane at the end of the seat
  showed the pre-existing untracked wave outputs plus `M .ufo/evidence/round-54/integrate/binder.py`
  and `M .ufo/evidence/round-21/coldread/ledger.json`; neither is mine — the L1/binder was working
  concurrently (HEAD moved `097985c` → `4e2de731b5` → `fe70474dac` during the seat).
- All git mutations (`add`, `commit`) were inside the `mktemp -d` clone; every call named
  `-C "$D/clone"` and `git rev-parse --show-toplevel` was asserted equal to the fixture before
  mutating. No mutating git command touched the lane or any other repo.
- No tools installed or upgraded (nothing needed); pacman untouched.
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Sent02/`.

## Receipts

- `T54W2Sent02-receipts/build-fixture.py` — fixture builder (writes only inside the clone).
- `T54W2Sent02-receipts/attack-driver.py` — R1/R2/R3 driver.
- `T54W2Sent02-receipts/arm4-probe.py` — arm-4 provenance probe (E1/E2).
- `T54W2Sent02-receipts/pinned-baseline.out` — baseline PASS under `d7749f84…`.
- `T54W2Sent02-receipts/pinned-attack.out` — R1/R2/R3 full transcripts.
- `T54W2Sent02-receipts/pinned-R4.out` — `.git/` observation.
- `T54W2Sent02-receipts/pinned-arm4.out` — E1/E2.
- `T54W2Sent02-receipts/attack-R1-R2-R3.out`, `R4-git-namespace.out` — first pass (unpinned
  counter; same reasons, kept for completeness).
- `T54W2Sent02-receipts/frozen-digests.txt` — digest checks (superseded by the pinned table above).

## Artifacts opened

`.ufo/evidence/round-54/contract.json`, `freeze.json`, `deciding-run.sh`, `no-harm.sh`,
`c1/measure.py`, `c1/lost-headings-at-base.json`, `c1/lost-headings-at-base.json`,
`c2/measure.py`, `.ufo/evidence/round-18/measure.py` (C1 blob),
`.ufo/evidence/round-21/coldread/measure.py` (C1 blob),
`.ufo/evidence/round-48/quality/coldread-precheck.sh` (C1 blob), `.ufo/waves/round-54/spec-w2.json`,
`.ufo/waves/round-54/w1/*Read*.json` (23 reports), `SHONEN.md` at C1.
