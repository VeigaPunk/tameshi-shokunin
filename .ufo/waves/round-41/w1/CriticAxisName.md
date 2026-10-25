# CriticAxisName — round 41, C2 declared `depth`

Seat: critic, read-only. Assignment: attack the axis label of C2 (declared depth), name the
surface the round changes, decide whether the label is honest or a number-proxy.
Counters were **not** run (neither `calibration/measure.py` nor `census/measure.py`, at any
revision): the deciding runs belong to the L1. Everything below is read from committed bytes at
`a3d6c690bcbf8914551d4f4e8e1612784c1c2046` / `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`
and from the uncommitted round-41 working tree. No installs, no upgrades.

## Verdict

`depth` is **honest only conditionally**, and as frozen it is a **number-proxy**. Two surfaces
change this round; the claim's counter measures one of them, the label names the other, and the
label also happens to be carried by a homonym in the contract (`resolution to depth four` = the
resolver's fold distance, not the AXES.md axis). A tree with the depth artifact deleted still
scores `C2_R41_PASS=true`.

## The rule, quoted

`/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-41.md:371`:

> - Name the axis by the surface the round changes, not by the number it produces (kaidoku r29).

and `:372-375`:

> Re-scoring a rule the lane already holds on new inputs, or counting rows a sourceless
> fixture also counts, is quality work, never coverage or depth. A coverage claim names the
> surface it moves (frontier → core, a new tool, operation or edge class) and the command that
> would show it unmoved.

The axis definitions the rule points at, `/home/vgpnk/Projects/shokunin/AXES.md:11-12`:

> | **depth** | Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources | A reader can act on SKILL.md alone; no filler |
> | **coverage** | Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes) | PROVINCE.md lists every surface; none unexplored without reason |

and `AXES.md:41`: a capability acquisition "still lands a per-axis verdict".

## The two surfaces this round changes

**S1 — measured by C2's counter, and it is coverage, not depth.**
A new tool plus two write-destination edge classes v2 cannot see:
`tools/write-path-census-v3.py` resolves a destination held in a variable
(`tools/repeat-control.py:811`, `with open(duplicate_path, "wb")`) and an `os.symlink`
destination (`tools/repeat-control.py:820`). AXES.md:12 lists exactly "tools, edge classes",
and prompt:374 lists exactly "a new tool, operation or edge class" as the coverage sentence.
The unmoved-command is already inside the frozen predicate (`v2_var_expected=0
v2_symlink_sites=0`) and can be read directly without the counter:

```
grep -c 'os\.symlink' /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v2.py
→ 0
```

**S2 — the only depth surface, and it is outside the claim.**
`corpus/knowledge/r41-variable-destination-writes.md` is a genuine AXES.md:11 depth artifact: two
cited sources with located quotes (`:1-2`, S153 `ast` / S154 `Path.write_text`), a decision
table (`:33-36`), a named threshold ("to a depth of four", `:63`), and a "What is not claimed"
list. It is drafted (4,130 B, 78 lines, uncommitted) and will land in the same round — but it is
absent from the freeze (`git cat-file -e d4ee4e63…:corpus/knowledge/r41-variable-destination-writes.md`
→ `fatal: … exists on disk, but not in 'd4ee4e63…'`, exit 128), absent from the claim statement,
and absent from the claim's counter.

## Counterexample that makes the defect real

**C2_R41_PASS is invariant to the depth artifact.**

```
grep -nE 'entry|knowledge|SKILL|corpus|SOURCES' \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/census/measure.py
→ no match, exit 1
```

Every target field in `.ufo/evidence/round-41/contract.json` `claims.C2.target` is a tool/census
field (21 at the freeze, 22 as amended by A2 — the added field is `mutant_symlink_arg_killed`); not
one reads a knowledge path or SKILL.md. Checked against the live contract (`contract.json`
sha256 `529cb1606fe86d4dd9b78a3e08f92f14e1439be072544102e7409a98358aae35`, read 03:47), which
carries amendments A1–A5, all `rule_changed: false`, `before_data: true` — A1/A2/A4/A5 move C1/C2
counter bytes and pins, A3 record text; none touches `claims.C2.axis`. This is a command to
re-run, not a snapshot: after any further amendment re-run it, because the finding turns only on
`claims.C2.axis` still reading `depth` and on the target list still carrying no knowledge field.

```
python3 -c "import json;c=json.load(open('.ufo/evidence/round-41/contract.json'))['claims']['C2'];t=c['target'].split();print('axis=',c['axis'],'fields=',len(t));print([f for f in t if any(k in f.lower() for k in ('entry','knowledge','skill','corpus','source'))])"
→ axis= depth fields= 22
→ []
```

The amended counter is equally blind to the entry (`grep -nE 'entry|knowledge|SKILL|corpus|SOURCES'
.ufo/evidence/round-41/census/measure.py` → no match, exit 1). Therefore a tree that keeps the tool
and fixtures but deletes the entry still prints `C2_R41_PASS=true`. The depth label would then
rest on nothing the claim can re-derive — which is the number-proxy case the rule forbids: the
axis is named by an artifact the counter produces (the tool's own resolution), while the depth
artifact rides unmeasured.

The numeric move is also zero on the lane's own pinned depth instrument:

```
for REV in a3d6c690bcbf8914551d4f4e8e1612784c1c2046 d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937; do
  printf "%s " "${REV:0:8}"
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show "$REV:tools/mutate-and-run.sh" |
    python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
done
→ a3d6c690 recorded_cases=9 depth_score=9
→ d4ee4e63 recorded_cases=9 depth_score=9
```

and no SKILL.md / knowledge / SCORECARD / LOG byte was touched by the freeze commit
(`git log --oneline a3d6c69..d4ee4e6 --name-only | grep -E 'SKILL.md|corpus/knowledge|SCORECARD|LOG'`
→ `none`).

The homonym is explicit in the contract's `declared_scope_limit`: "one-hop-ish resolution to
**depth four**". That is `env`-fold depth, not the depth axis; it is what makes the label look
self-justifying when nothing about it is measured.

## Is there a reading that saves `depth`?

Yes, and it is the strongest available defence: the round does ship S2, and the lane's previous
closure accepted exactly this label shape — `corpus/lessons/round-40-verifier-spotcheck.md:255-256`
records "depth: **improved** … numeric depth stays 9" for the analogous v2 capability, and the
lane's own precedent for a capability row carrying several per-axis verdicts is
`SCORECARD.md:169` (round-1 K2, axis cell "— (per-axis verdicts below)"). So `depth` is neither
invented nor unprecedented. What is missing is not the axis, it is the **link**: the round never
declares that the depth verdict rides the entry, and the predicate cannot see the entry. Absent
that link the label is the number-proxy; with it the label is honest.

## Impacted axes

| Axis | Impact of leaving the label as-is |
|---|---|
| depth | labeled "improved" with no in-claim artifact and no numeric move (command D 9 → 9); an honest reader cannot re-derive the verdict |
| coverage | a new tool + two new edge classes is silently absorbed under `depth`, so the coverage surface is neither named nor scored — no harm to an existing number, but an unreported move |
| calibration | the record asserts an axis move its own evidence cannot show; that is the self-assessment-versus-observed-state class the lane audits elsewhere |

No axis is *harmed* in the scorable sense (depth stays 9, coverage is unpinned); this is a label
defect, not a data defect. The predicate, kill rule and receipts stand as frozen.

## Smallest safe correction (label + one appended command; nothing else)

1. **Claim row / SCORECARD axis cell** — replace the bare `depth` with the surfaces, using the
   lane's own K2 shape (`SCORECARD.md:169`) or naming both inline:
   `depth (surface: corpus/knowledge/r41-variable-destination-writes.md — table :33-36, depth-4
   threshold :63, S153/S154) + coverage (surface: tools/write-path-census-v3.py; the variable and
   os.symlink destination classes; unmoved: grep -c 'os\.symlink' tools/write-path-census-v2.py → 0)`.
2. **One re-derivation line for the depth surface**, since the claim's counter cannot see it —
   run against the same measured revision as the claim:
   ```sh
   git show "$REV:corpus/knowledge/r41-variable-destination-writes.md" | grep -cE '^source: S15[34]'   # 2
   git show "$REV:corpus/knowledge/r41-variable-destination-writes.md" | grep -c '^| '                  # 3 (header + 2 live-site rows)
   ```
   Both read 2 and 3 in the working tree now; they must be re-run at the round commit, because the
   entry is not in the freeze.
3. **One guardrail sentence, carried verbatim** — "numeric depth 9 → 9 under command D
   (`recorded_cases=9 depth_score=9` at `a3d6c69` and `d4ee4e6`); `C2_R41_PASS` is the capability's
   instrument, not the depth measure." This is the r40 closure's own wording
   (`round-40-verifier-spotcheck.md:256`), so no new standard is introduced.

Cost of the correction: one table cell, two pasted commands, one sentence. No counter edit, no
predicate edit, no claim dropped, no post-freeze rule change, no contradiction with the round-40
closure. If the L1 prefers a single axis instead, `coverage` is the honest one for the claim as
frozen — but that reads the entry as documentation rather than as the axis, and `coverage` is
unpinned, so it is the more expensive of the two paths.

Secondary note (not part of the correction, to avoid duplicating `ReviewEntry`'s authority): the
entry's `:28` sentence "At the round-41 freeze revision" is about the tools, both of which do
exist at the freeze, so it is accurate; but any SCORECARD/LOG line that cites the entry must cite
it at the measured revision, not at `d4ee4e6`, or C1's m8 class
(`.ufo/evidence/round-41/calibration/measure.py:237-241`, `PATH_PREFIXES` at `:46-51`) counts a
repo path that does not resolve at that revision.
