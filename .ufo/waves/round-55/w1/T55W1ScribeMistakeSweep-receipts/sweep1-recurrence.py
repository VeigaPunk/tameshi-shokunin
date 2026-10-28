#!/usr/bin/env python3
"""Sweep 1: recurrence of a routed defect CLASS across rounds 50-54.

Counting rule, fixed before the run:
 * Population P = every routed-defect item in corpus/lessons/round-NN-verifier-spotcheck.md
   (NN=50..54) — both the `N. **Rnn.k ...**` form and the older bare `N. **...**` form,
   plus every `- **class: ...**` entry in corpus/lessons/round-NN.md, for the same range.
 * Class = keyword family listed below. Assignment is mechanical (regex over the item's
   own text); the matched substring is printed for audit.
 * "Recurs" = present in >= 2 DISTINCT round numbers.
Usage: sweep1-recurrence.py LANE REV OUT.json
"""
import re, subprocess, sys, json

LANE, REV, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

def show(p):
    r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{p}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

FAMILIES = [
 ("uncommitted-work-at-closure",
  r"untracked|uncommitted round work|carry uncommitted|left uncommitted"),
 ("record-quotes-a-value-its-receipt-does-not-print",
  r"quote does not match|does not match its cited receipt|no receipt contains|"
  r"quote does not match the counter|under the wrong receipt|cited for a value|"
  r"does not match the committed receipt"),
 ("stale-freeze-pointer",
  r"freeze pointer|stale freeze"),
 ("count-vs-committed-artifacts",
  r"finding counts do not match|counts? do not match the committed|wave-table numbers"),
]

items = []
for n in range(50, 55):
    sc = f"corpus/lessons/round-{n}-verifier-spotcheck.md"
    t = show(sc)
    if t:
        for sec in re.finditer(r"\n## [^\n]*[Rr]outed[^\n]*\n(.*?)(?=\n## |\Z)", t, re.S):
            body = sec.group(1)
            for m in re.finditer(r"\n(?:\d+\.\s+)?\*\*([^*\n]{3,200})\*\*(.*?)(?=\n(?:\d+\.\s+)?\*\*[^*\n]|\n## |\Z)", body, re.S):
                items.append({"round": n, "src": sc, "id": m.group(1).strip(), "text": m.group(0)})
    les = f"corpus/lessons/round-{n}.md"
    t = show(les)
    if t:
        for m in re.finditer(r"\n- \*\*class: ([^*\n]+)\*\*(.*?)(?=\n- \*\*class:|\n## |\n- \*\*[A-Z0-9]|\Z)", t, re.S):
            items.append({"round": n, "src": les, "id": "class: " + m.group(1).strip(), "text": m.group(0)})

print(f"REV={REV}")
print(f"POPULATION defect-items={len(items)}")
per = {}
for it in items:
    per.setdefault(it["round"], []).append(it["id"])
for k in sorted(per):
    print(f"  round {k}: {len(per[k])} items")
print()
recurring = []
for cid, pat in FAMILIES:
    hits = []
    for it in items:
        m = re.search(pat, it["text"], re.I)
        if m:
            hits.append((it["round"], it["id"], m.group(0)[:60], it["src"]))
    rounds = sorted({h[0] for h in hits})
    verdict = "RECURS" if len(rounds) >= 2 else ("single-round only" if rounds else "absent")
    print(f"CLASS {cid}")
    print(f"  rounds={rounds} hits={len(hits)} verdict={verdict}")
    for r, i, ms, src in hits:
        print(f"    r{r} {src}: {i[:70]}")
        print(f"        matched: {ms!r}")
    print()
    if len(rounds) >= 2:
        recurring.append({"class": cid, "rounds": rounds,
                          "hits": [{"round": r, "id": i, "src": s} for r, i, _, s in hits]})
print(f"RECURRING_CLASSES={len(recurring)}")
for c in recurring:
    print(f"  {c['class']}: rounds={c['rounds']} n={len(c['hits'])}")
json.dump({"rev": REV, "population": len(items), "recurring": recurring,
           "items": [{"round": i["round"], "id": i["id"], "src": i["src"]} for i in items]},
          open(OUT, "w"), indent=1)
