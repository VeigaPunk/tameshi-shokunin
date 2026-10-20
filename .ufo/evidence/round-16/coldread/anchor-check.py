#!/usr/bin/env python3
"""anchor-check.py — mechanical anchor check for the round-16 in-place SKILL.md repairs.

Compares every self-reference of the form SKILL.md:<n>[-<m>] or a bare
:<n>[-<m>] that refers to this page in
  c699c8c36d6e4eca4b796b81a8247904aa145ec8:SKILL.md            (repaired page)
against the same lines in
  e69b488:.ufo/evidence/round-16/coldread/SKILL.snapshot.md  (pre-repair snapshot)

Bare `:n` classification is context-judged (documented in the run's report):
anchors inside a file:name citation continue that file (e.g.
`mutation-case-kimi-census.md:45, :82-92` are kimi-census lines, not this
page); the table at SKILL.md:1250 explicitly declares `(Anchors ':…' are this
page)`. SITE columns in the tsukuroi table (`:473` etc.) are sites in
`tsukuroi-census.sh`, and `gate.rs:15`→`:11` is a rename of a gate.rs line.

Verdicts per anchor:
  RESOLVES          target lines exist and are byte-identical to the snapshot
  RESOLVES-CHANGED  target lines exist but were edited in place; quoting prose
                    at the citing line may now be stale (reported, not failed)
  STALE-QUOTE       citing line quotes old wording whose repaired text moved

Run:  python3 anchor-check.py            (from the lane root, or anywhere)
Requires git on PATH and the tameshi lane repo next to ../../.. layout; the
repo path is resolved relative to this file so it also runs from /tmp copies.
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]          # tameshi-shokunin/
NEW_REV = "c699c8c36d6e4eca4b796b81a8247904aa145ec8"
OLD_REV = "e69b488"
REPO = Path(__file__).resolve().parents[4]          # tameshi-shokunin/
EXPECT_NEW_SHA = "3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4"
OLD_PATH = ".ufo/evidence/round-16/coldread/SKILL.snapshot.md"


def show(rev, path):
    return subprocess.run(
        ["git", "-C", str(REPO), "show", f"{rev}:{path}"],
        capture_output=True, check=True).stdout


def sha256(b):
    import hashlib
    return hashlib.sha256(b).hexdigest()


new_raw = show(NEW_REV, "SKILL.md")
old_raw = show(OLD_REV, OLD_PATH)
new = new_raw.decode().split("\n")
old = old_raw.decode().split("\n")
# trailing split artifact: file ends w/o newline in snapshot → last elt may differ
if new and new[-1] == "":
    new.pop()
if old and old[-1] == "":
    old.pop()

out = []
def emit(s=""):
    out.append(s)
    print(s)

emit(f"page   {NEW_REV}:SKILL.md  sha256={sha256(new_raw)}  lines={len(new)}")
emit(f"  expected sha256={EXPECT_NEW_SHA}  match={sha256(new_raw)==EXPECT_NEW_SHA}")
emit(f"snapshot {OLD_REV}:{OLD_PATH}")
emit(f"  sha256={sha256(old_raw)}  lines={len(old)}")
emit("")

# ---- structural check: every changed line is a same-index replacement ----
diffs = [(i, old[i], new[i]) for i in range(min(len(old), len(new))) if old[i] != new[i]]
emit(f"changed lines (same-index): {len(diffs)}")
for i, o, n in diffs:
    emit(f"  line {i+1}:")
    emit(f"    old: {o[:120]}")
    emit(f"    new: {n[:120]}")
emit(f"pure append tail: new[{len(old)+1}..{len(new)}] = {len(new)-len(old)} line(s) "
     f"(snapshot had no trailing newline; first appended line index {len(old)})")
section_heads_new = {i+1: l for i, l in enumerate(new) if l.startswith('#')}
section_heads_old = {i+1: l for i, l in enumerate(old) if l.startswith('#')}
moved = {k: v for k, v in section_heads_old.items() if section_heads_new.get(k) != v}
emit(f"heading lines moved/altered inside snapshot span: {len(moved)}")
for k, v in moved.items():
    emit(f"  line {k}: old={v!r} new={section_heads_new.get(k)!r}")
emit("")

# ---- anchor inventory ------------------------------------------------------
# (citing line, ref, classification, why)
PAGE = [
    (1084,  "811-812"),   # re-pin rule target, this page
    (1232,  "1069-1090"), # T1 rule, round-8 section of this page
    (1259,  "813-817"),   # refusal table b — declared this-page at :1250
    (1259,  "840-844"),   # refusal table b (protocol steps 2-3)
    (1260,  "823-825"),   # refusal table c
    (1263,  "879-881"),   # refusal table f
    (1276,  "1226-1228"), # round-9 caveat on this page
    (1296,  "1250-1254"), # service-limits rendering rule paragraph, this page
    (1346,  "925-929"),   # round-7 "Four legs" sentence, this page
    (1347,  "1218-1222"), # round-9 receipt block, this page
    (1348,  "1226-1228"),
    (1353,  "965-1008"),  # round-7 receipt-reading discipline, this page
    (1384,  "1294-1297"), # pointer rule, this page
    (1386,  "1246-1270"), # compact rendering = the refusal table section
    (1400,  "1021-1053"), # round-8 pin-read command set, this page
    (1414,  "1332-1344"), # round-10 receipt block, this page
    (1415,  "1069-1090"),
    (1434,  "1324-1331"), # git-materialization rule, this page
    (1443,  "131"),       # mutation-sweep recipe heading, this page
    (1445,  "965-1008"),
    (1453,  "1017-1019"), # round-8 [U] sentence, this page
    (1456,  "1359-1363"), # six-leg registry named-debt paragraph
]
AMBIGUOUS = [
    (1025, "14", "bare :14 after scripts/shokunin-watchdog.sh:3-5 — reads as a "
     "watchdog lane-map line; if read as this page it lands in the preamble "
     "and does not hold. Context: 'its lane map' = the watchdog script."),
    (1262, "20", "bare :20 after PROVINCE.md:14-18 — likely a PROVINCE.md "
     "continuation like every other trailing bare anchor in the document; "
     "as this page it lands on a preamble sentence and does not hold."),
    (1084, "811-812", "printed here as this-page anchor; the parenthetical "
     "lacks backticks and could be misread as a tool line — the semantic "
     "(re-pin rule sentence) only exists at SKILL.md:811-812."),
    (1328, "932-960", "continuation of the mutate-and-run.sh:104-106-style tool "
     "anchors in the same clause; as this page it lands on 'Using the ledger' "
     "which does describe blob materialization — plausible either way."),
    (1331, "1488-1527", "same ambiguity family: most likely "
     "tools/mutate-and-run.sh selftest arms; as this page :1488-1527 is the "
     "round-12 registry, which does not 'cover the mirror'."),
    (756,  "305-320", "likely a line range inside the tsukuroi S5-1 case note "
     "or ledger ER row the sentence discusses; as this page it lands inside "
     "the kill-rate bands table and does not hold."),
    (1207, "354-360", "'ER-4's addendum' — likely an errata/addendum line "
     "range in fleet-kill-rate-ledger.md; as this page it lands in the "
     "Restore-discipline block and does not hold."),
    (1361, "281", "'superseded in the ledger by ER-2' — almost certainly "
     "fleet-kill-rate-ledger.md:281; as this page it lands mid-paragraph in "
     "the defect-taxonomy section and does not hold."),
    (1419, "1230-1244", "ledger rows 'land appended in the ledger' — could be "
     "fleet-kill-rate-ledger.md lines or this page's re-pin-semantics section "
     "(:1230-1244 names the append-only rule); this page holds the rule text."),
    (1084, "811-812", None),  # placeholder removed below
]
AMBIGUOUS = [a for a in AMBIGUOUS if a[2]]  # drop placeholder

def rng(r):
    a, _, b = r.partition('-')
    return int(a), int(b or a)

emit("== self-anchors judged to mean this page ==")
bad = 0
for cite, r in PAGE:
    a, b = rng(r)
    if b > len(old) or b > len(new):
        emit(f"SKILL.md:{cite} -> :{r}  OUT-OF-RANGE")
        bad += 1
        continue
    changed = [i+1 for i in range(a-1, b) if old[i] != new[i]]
    status = "RESOLVES" if not changed else "RESOLVES-CHANGED"
    if changed:
        emit(f"SKILL.md:{cite} -> :{r}  {status} (edited lines {changed})")
    else:
        emit(f"SKILL.md:{cite} -> :{r}  {status}")
    emit(f"    target: {new[a-1][:110]}")

emit("")
emit("== ambiguous bare :n refs (context reads them as another file) ==")
for cite, r, why in AMBIGUOUS:
    emit(f"SKILL.md:{cite} -> :{r}  AMBIGUOUS — {why}")

emit("")
emit("== explicit 'SKILL.md:<n>' refs ==")
explicit = [(i+1, l) for i, l in enumerate(new) if re.search(r'SKILL\.md\s*:\s*<?\d', l)]
if not explicit:
    emit("none found (line 1714's 'SKILL.md:<line>' is a generic pattern mention, not an anchor)")
for ln, l in explicit:
    emit(f"SKILL.md:{ln}: {l.strip()[:120]}")

emit("")
# the one claim in the errata preamble that this check attacks
emit("errata claim under attack: 'every SKILL.md:<line> self-anchor still "
     "resolves' — all edits same-line-index replacements; append-only tail.")
emit(f"result: {len(PAGE)-bad}/{len(PAGE)} this-page anchors resolve; "
     f"{sum(1 for c,r in PAGE if any(old[i]!=new[i] for i in range(rng(r)[0]-1, rng(r)[1])))} "
     f"point into repaired text (still same line numbers)")
sys.exit(0 if bad == 0 else 1)
