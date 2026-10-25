# Round 41 lesson

author: tameshi L1 (hyaku run 6, attempt 2)
date: 2026-10-25

## Gate

Theme: F4 write-path visibility — the two sources that let a census resolve a write
destination instead of matching a literal on one line. Both sources were opened this
round, access date 2026-10-25, and both are pinned to committed snapshots rather than to
live digests (the round-33/40 lesson: docs.python.org's footer clock moves within a day).

### Admit — `corpus/knowledge/r41-variable-destination-writes.md` (S153, S154)

- S153 — https://docs.python.org/3/library/ast.html — page title "Python 3.15.1 documentation", HTTP 200, 362029 bytes, snapshot
  `.ufo/evidence/round-41/sources/ast.html`, sha256 `183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317`.
  Located quote (15 words), §Abstract Syntax Trees, body prose: "The ast module helps
  Python applications to process trees of the Python abstract syntax grammar."
- S154 — https://docs.python.org/3/library/pathlib.html — page title "Python 3.15.1 documentation", HTTP 200, 271189 bytes, snapshot
  `.ufo/evidence/round-41/sources/pathlib.html`, sha256 `0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093`.
  Located quote (16 words), §Path.write_text: "Open the file pointed to in text mode,
  write data to it, and close the file:".
- Both quotes are ≤25 words and both were re-located by a second seat from the live page,
  where the digest reproduced the snapshot's. The entry states what the sources do not
  say (no static-analysis claim) and what the round does not claim (no universality, no
  dataflow guarantee, no gate coverage).

### Reject — the staged gate-census entries in the assimilation package

Read at `/home/vgpnk/Projects/shokuknow/merge/tameshi/`. The two staged F4 gate-census
entries (`r4-gate-write-path-audit`, `r5-gate-write-site-census-corrected`) carry
`source:` lines that point at the lane's own tree — https://github.com/VeigaPunk/tameshi-shokunin
at revision `31687496` — not at an external surface. Adopting them would add same-ground
rows, not expansion (CORPUS rule 4: expansion is knowledge, not rows). The staged row the
round-40 Gate already refused (`r4-gate-write-path-audit`) keeps that refusal: its flip
condition names `31687496`, and `git cat-file -e 31687496:tools/write-path-census.py`
still fails, so no write-path census artefact exists at that revision. Refused again, no
new reason invented. Assimilation this round: none adopted.

### Collision and census

- Registry ids: 109 (`S001` through `S154`) after this round's two rows; staged ids: 103,
  beginning at `S153` and running 103 ids past it. `comm -12` → `collisions` holds **2**
  ids, `S153` and `S154` — the package's first two ids now name the lane's own rows. No
  staged row was adopted, so no renumber map is applied; the collision is recorded as the
  hazard the next assimilation round must resolve in scratch before it appends.
- Round start (before either row): `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  exit 0, 107 rows, 9 × W04 + 1 × W01, zero E codes. Round end: exit 0, 109 rows, the same
  warning set, zero E codes. Each new row parses as 13 awk fields and carries no pipe.

### Correction — the round-40 quarantine summary

The round-40 closure's routed defect 1 stands: that lesson's closing sentence says seven
refused and nine present-but-not-appended, while the verdict table in the same file
counts one adopted, six refused, ten present-but-not-appended. The table is the record;
the summary sentence is the drift. This appended correction is the fix the closure asked
for ("append a correction in the round-41 lesson — do not rewrite the closed round-40
file in place"). The round-40 file is unchanged.

### Adjacency — sibling prior art, cited not absorbed

A connector seat found that two tools in `kotodama-shokunin/tools/harness/` already resolve
write destinations through assignments (`round_runner_conformance.py`, five-pass fixpoint,
depth 8; `receipt_guard_adoption.py`, depth 6), landing 2026-10-19. This round's tool is a
subset of that resolution machinery plus `os.symlink`, the expected/scratch classification
and scratch tracing. The entry records it as prior art and claims no novelty. Absorbing the
sibling's code is refused by `PROVINCE.md`; citing it is what Core allows. One lane is not
two independent lanes, so the fleet's general-pattern bar is not met and no general claim is
made.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| count-label-drift | this round's first draft of `corpus/knowledge/r41-variable-destination-writes.md` labelled the S153 quote "16 words" and the S154 quote "17 words"; the token counts are 15 and 16 (`python3 -c "print(len(s.split()))"` on both sentences) | the round-40 closure's routed defect 4 (a quote labelled "11 words" that has 13 tokens) — the same class, one round later, caught by re-counting instead of trusting the label | both labels corrected in the entry, and the wave's word-label seat re-counts every labelled quote in the round's drafts. The fix can fail: the label read 16 where the count reads 15, so a checker that recomputes tokens flags the pre-fix text |
| counter-silent-on-wrapped-prose | the first version of the C1 counter's m9 parser searched line by line, so the round-40 summary sentence — wrapped across three lines — parsed as `None` and m9 read 0 at the base | running the counter at the base revision before freezing anything; the contract's declared before-state expected m9=1 | the parser flattens whitespace before matching, and the base run then printed `m9=1 ... total=2`, which is the frozen before-state. A parser that cannot fail shows 0 at the base and would have made m9 decorative |

| replace-all-on-a-shared-closing-line | round 39 and round 40 each ended a LOG bullet with the same sentence; a `str.replace` without a count rewrote both of them with round-41 text, and the round-41 record landed with two deletions in an append-only file (`git diff --numstat a3d6c690 812ee0d1 -- LOG.md` → `95 2`) | none — no rule required an append-only check before landing; the `m6`/`m7`/`m8`/`m9` classes never look at earlier sections | the file was rebuilt from the base blob plus the round-41 section, and the numstat is now `74 0`. The fix can fail: the residual seat's `numstat` read `95 2` before the rebuild and `74 0` after, and the two restored bullets are the base bytes |
| in-place-row-restatement | the standing `sources-registry` row was edited in place, erasing the round-32/35 errata chain it carried (`git diff --numstat` showed `94 1`) | the residual seat proved the counter reads the *last* such row, so appending restates it; the old append chain was the audit trail | the base row was restored byte-identically and a new standing row with 109 rows was appended; numstat is now `95 0` and `m6=0` still holds |

## Holds

- v3 resolves destinations to depth four through assignment, `os.path.join`, `+`, `/`,
  f-strings and attribute chains. Aliases, closures over a reassigned name, attribute
  reassignment, conditional assignment, dictionary and list elements, and any path
  computed by a call that does not fold to a literal stay unresolved, and the docstring
  says so. This is not a dataflow analyser.
- `shutil.copy*`, `handle.write`, `os.remove/unlink` and shell redirects stay outside both the v2
  and v3 write forms. The round covers `os.symlink` destinations and nothing more.
- The tool's docstring reads stronger than the tool: the scope seat found that aliases, closures,
  attribute reassignment, conditional assignment and non-folding helpers are resolved *sometimes* —
  by name, at definition time, or through a stale binding. The knowledge entry states that
  inconsistency; the docstring's blanket "NOT resolved" is the sentence a reader should not trust.
  Correcting it means editing a sha-pinned tool, so it waits for the successor round.
- POSIX `diff` remains the only exit lattice this lane has pinned. `cmp` and
  `git diff --exit-code` stay unmeasured.
- The two live sites the round resolves are scratch fixtures. The capability is
  visibility of the destination; the round claims no new open write path in this lane's
  tools. Any non-scratch unflagged site a seat found is reported separately as a finding.
- The registry now ends at `S154` while the staged package starts at `S153`: the next
  assimilation round must renumber in scratch (document-anchored, never arithmetic) before
  it appends, and must say so in its Gate.
- The round-38 L0 question `d0531d78` is not re-filed.
- Sibling prior art exists for destination resolution (see the Adjacency block). This lane's
  tool is bounded, in-lane and a subset; a reader who needs depth-8 folding should use the
  sibling's, and this lane neither absorbs nor certifies it.
- The knowledge entry is 96 lines against the 60-line cap in the seat brief; the cap was a
  brief instruction, not a repo rule, and the extra length is the prior-art and
  false-positive disclosures. The cap is waived here, explicitly, rather than silently.

### C1 instrument

- The C1 counter has no self-pin clause: it does not hash its own bytes against
  `claims.C1.counter_sha256`, so the pin is enforced by a reader, not by the predicate. m7 and m8
  are vacuous without records (this round prints `records=3`), m8 resolves directories and covers
  four path prefixes plus a root-file list, and m9 reads the whole lesson rather than the round-41
  section. A successor counter with a self-pin and a `records >= 1` gate is routed to round 42.
- The coupling is one-way and textual: m8 makes C1's pass depend on the files that C2 landed (the
  tool path and the two snapshots) being committed at the measured revision, while C2 reads no C1
  file. C1's first deciding run failed on exactly that edge — a cited wave path not yet committed —
  and the receipt is retained.
- The C1 counter's predicates were re-pinned five times pre-data (A1–A5 in the contract). A5 (the
  m9 correction words derived from the round-40 table instead of two hardcoded strings) is a
  strictness change found by two seats before the first deciding run; it is not a narrowing.

### C2 instrument

- The C2 counter imports the measured tool in-process, reads its pin from the same revision's
  contract, and checks the live sites by `expected`/`scratch`/`kind`/`lineno` without reading the
  `resolved` text. A hostile tool could therefore satisfy it; an honest one does not, and a
  non-author should read the three mutants' FAIL lines rather than the pass bit alone. `killed` is a
  non-zero exit, so a traceback would count — the three real mutants die on `var_unflagged`,
  `symlink_unflagged` and the argument swap respectively, receipted in the wave reports.
- `--control` is a negative control by construction (`C2_R41_CONTROL_PASS=false` is the expected
  value, not a failure; `true` would mean v2 reached the target), it reads the fixtures from the
  working tree rather than from `--rev`, and `fixtures_sha256` is pinned but never verified.
- `os.replace`/`os.rename` are recorded with both arguments as destinations, so a read of an
  expected file can be listed beside its write; no measured count changes because every such live
  site resolves `expected=False`.
