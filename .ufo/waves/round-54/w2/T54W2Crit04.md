# T54W2Crit04 — falsify the sourced claim (scratch-root-contract vs S277–S279 @ C1)

Seat: `T54W2Crit04` (critic). Target rev: `99c3bc88d704566197783f66b211ee0a830e0330`.
Artifact under attack: `corpus/knowledge/scratch-root-contract.md`.
Sources: S277 (POSIX TMPDIR), S278 (CPython `_candidate_tempdir_list`), S279 (`tempfile.gettempdir` docs).
Receipts: `.ufo/waves/round-54/w2/T54W2Crit04-receipts/` (assertions.txt + extracts).
No lane production files edited; all probes read `git show` at C1 or ran under `$HYAKU_SCRATCH/tameshi-r54/T54W2Crit04/`.

## Axes

1. **Source fidelity** — every external claim in the note ⊆ the cited row's located content; no claim outruns its source (lesson Gate QUALITY bar @ C1).
2. **Empty-arm hygiene** — `TMPDIR=""` stays a *declared lane rule*, not a fact attributed to S277–S279.
3. **Cite completeness** — sentences that assert resolver/standard behavior name the row that actually carries them.

## Verdict

**Falsified on axis 1 (source fidelity).** One note sentence attributes empty-TMPDIR fallthrough to **S279**; the S279 assimilation text contains no `empty` / `unset` / `missing` / `falls through` language at all. Empty-skip is **S278-only**.

**Axis 2 partially holds:** the note does contain an explicit lane-declaration sentence for the empty arm. That sentence survives. The S279 overreach still *sources* empty fallthrough through the back door, so declaration hygiene is incomplete.

**Axis 3:** S278 and S277 positive quotes match; the S277 *negative* ("not its empty-string handling") is silence-inference, labeled well enough by the following declaration sentence.

`c2/measure.py` arm 5 only checks that the note cites a mined S-id whose Gate names URL + `2026-10-28`. It cannot see this overreach — counter blind spot, not a clean bill of health for the sourced claim.

---

## Overreach 1 (kills source fidelity) — S279 cited for empty fallthrough

**Exact sentence (byte-exact from C1 note, whitespace-normalized for the prose clause):**

> so an empty `TMPDIR` never becomes a candidate directory; the documented list also starts at "the directory named by the TMPDIR environment variable" and then falls through (S279).

**Why overreach:** the clause "and then falls through (S279)" is attached to the empty-TMPDIR claim. S279 documents only the ordered search list. It never states what happens when TMPDIR is empty, missing, or unset, and never says "falls through".

### Command + output (A1)

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  99c3bc88d704566197783f66b211ee0a830e0330:corpus/knowledge/scratch-root-contract.md
# → contains the sentence above with trailing "(S279)."
```

### Command + output (A2) — S279 has zero empty/fallthrough language

```
# text-extract assimilation S279; scan gettempdir list block
'empty' in gettempdir-block=False in_full_doc=False
'unset' in gettempdir-block=False in_full_doc=False
'missing' in gettempdir-block=False in_full_doc=False
'falls through' in gettempdir-block=False in_full_doc=False
'fall through' in gettempdir-block=False in_full_doc=False
```

S279 *does* contain the quoted opener ("The directory named by the TMPDIR environment variable") and the rest of the ordered list. That is all it can support. Fallthrough for the empty string is not in the doc.

### Command + output (A3) — empty skip lives in S278

```
163	    for envname in 'TMPDIR', 'TEMP', 'TMP':
164	        dirname = _os.getenv(envname)
165	        if dirname: dirlist.append(dirname)
```

### Command + output (A4) — SOURCES.md S279 located-quote cell already overreaches

```
| S279 | … | "The list is: The directory named by the TMPDIR environment variable" then TEMP, TMP and platform locations — the documented order a missing or empty TMPDIR falls through | mined | …
```

The editorial tail "a missing or empty TMPDIR falls through" is not in the assimilation HTML. The note mines that overreach into prose via `(S279)`.

---

## Overreach 2 (mild) — S277 negative scope as if stated

**Exact sentence:**

> The standard fixes only the variable's meaning, not its empty-string handling: `TMPDIR` "shall represent a pathname of a directory made available for programs that need a place to create temporary files" (S277).

**Why mild overreach:** the quoted positive text is exact (A6). The leading claim "not its empty-string handling" is not in the POSIX TMPDIR paragraph (A6: `empty/unset/null/absent` all False). It is a silence inference. The *next* sentence correctly converts that into a lane declaration — so this is labeled, not smuggled as a POSIX mandate. Keep as a discernment nick, not the kill.

### Command + output (A6)

```
'TMPDIR\nThis variable shall represent a pathname of a directory made available for programs that need a place to create temporary\nfiles.'
empty False
unset False
null False
absent False
```

---

## Empty-arm declaration check (axis 2)

**Exact declaration sentence (survives):**

> The empty arm is therefore a lane declaration that follows the resolver the lane actually calls, and the registry rows say so.

Also: "which is why the arm is declared rather than left to whatever `os.path.isdir("")` happens to return."

So the note *does* name the empty arm as a declaration. That part of the frozen intent holds.

**Remaining hygiene defect:** table row + S279 sentence still present empty-fallthrough as sourced behavior:

```
| empty | `""` | **unset**: Python's resolver skips an empty candidate, so the next candidate wins (S278) and the platform default applies | — |
```

S278 legitimately supports "skips an empty candidate / next candidate wins". The arm's normative status (tools treat `""` as unset, exit —) is the declaration — and must not lean on S279.

### Command + output (A5)

```
28:… (S277). The empty arm is therefore
29:a lane declaration that follows the resolver the lane actually calls, and the
```

### Empiric side-check (not an S-row; supports the declaration rationale)

`tempfile.mkdtemp(dir="")` under the seat scratch created a directory under cwd (`under_cwd True`); `os.path.isdir("")` is `False`. The cwd-allocation sentence is empirically holdable for a `dir=""` call shape and is *not* attributed to S277–S279 — no source-fidelity kill there.

---

## Sentences that need no S277–S279 cite

Intro (round-53/54 helper history), unusable-arm exit class, "Why the class is uniform" (R53.6), "What measures it", "Falsifier" — lane/history/instrument text. They are not sourced-claim sentences against S277–S279. Not counted as overreach.

## What the frozen counter still cannot see

`.ufo/evidence/round-54/c2/measure.py` arm 5 (`note`/`sources`) regex-finds `S\d{3,}` in the note ∩ mined `used-by` rows, then checks Gate for `S{id}` + `2026-10-28` + `http`. A false S279 attribution still yields `sources≥1`. This attack is against the note's fidelity to S277–S279, not against the counter's weak cite gate.

## Impacted axes

- **discernment** — note outruns S279; SOURCES located-quote cell already poisoned the mine.
- **calibration** — C2 "sourced claim" looks green under the counter while the QUALITY bar ("no claim outruns its source") fails on the S279 sentence.

## Smallest safe correction

1. In `scratch-root-contract.md`, rewrite the S279 clause to cite *only* the ordered-list opener, e.g. end the empty-skip sentence at S278 and add a separate sentence: the docs list begins at "the directory named by the TMPDIR environment variable" (S279) — **no** "falls through" / empty/missing language under that cite.
2. In `corpus/SOURCES.md` S279 located-quote cell, drop the editorial tail "a missing or empty TMPDIR falls through"; keep the list-opener quote only.
3. Leave the "empty arm is therefore a lane declaration…" sentence untouched.

## Tools

None installed this seat (pacman paused; no uv/npx needed). Host `python3` + `git` only.
