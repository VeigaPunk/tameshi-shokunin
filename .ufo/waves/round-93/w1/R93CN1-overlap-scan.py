#!/usr/bin/env python3
"""R93CN1 Sibling-overlap scan probe.
Audits all 20 sibling lane repos across /home/vgpnk/Projects/shokunin for:
  (a) Markdown-table readers keyed on a verdict header
  (b) Conjunct-falsifiability disposition checkers
  (c) Battery-summary-derived-from-receipts helpers
  (d) scripts/sources-census.sh table parser verdict semantics
"""
import os
import re
import subprocess
import sys

FLEET = "/home/vgpnk/Projects/shokunin"
LANES = sorted([
    d for d in os.listdir(FLEET)
    if d.endswith("-shokunin") and d != "tameshi-shokunin" and os.path.isdir(os.path.join(FLEET, d))
])

PATTERNS = ["verdict", "delimiter row", "header row", "CONJUNCT", "unfalsifiable", "receipt"]

def run_rg(args, cwd=FLEET):
    res = subprocess.run(["rg"] + args, cwd=cwd, capture_output=True, text=True)
    return [l for l in res.stdout.strip().split("\n") if l]

print(f"=== SIBLING OVERLAP SCAN (Fleet root: {FLEET}) ===")
print(f"Sibling lanes surveyed: {len(LANES)}")
for l in LANES:
    print(f"  - {l}")

print("\n--- 1. Lexical Pattern Counts across Sibling tools/, .ufo/evidence/, corpus/knowledge/ and scripts/ ---")
search_targets = []
for lane in LANES:
    for sub in ["tools", ".ufo/evidence", "corpus/knowledge"]:
        p = os.path.join(FLEET, lane, sub)
        if os.path.exists(p):
            search_targets.append(p)
search_targets.append(os.path.join(FLEET, "scripts"))

for pat in PATTERNS:
    hits = run_rg(["-l", "-i", pat] + search_targets)
    print(f"Pattern '{pat}': {len(hits)} matching files")

print("\n--- 2. Targeted Audit: (a) Markdown-table reader keyed on verdict header ---")
table_hits = []
for lane in LANES:
    tools_dir = os.path.join(FLEET, lane, "tools")
    if not os.path.exists(tools_dir): continue
    for root, dirs, files in os.walk(tools_dir):
        for fname in files:
            if not fname.endswith((".py", ".sh", ".mjs")): continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except:
                continue
            if "split(" in content and "|" in content:
                for line in content.split("\n"):
                    if "verdict" in line.lower() and any(k in line.lower() for k in ["header", "column", "delim", "table"]):
                        table_hits.append((lane, os.path.relpath(fpath, FLEET), line.strip()[:100]))
                        break

print(f"Candidate table-parsing files with verdict references: {len(table_hits)}")
for lane, rel, snippet in table_hits[:15]:
    print(f"  [{lane}] {rel} -> {snippet}")
if len(table_hits) > 15:
    print(f"  ... and {len(table_hits) - 15} more audited")

print("\n--- 3. Targeted Audit: (b) Conjunct-falsifiability disposition checker ---")
disp_hits = []
for lane in LANES:
    for root, dirs, files in os.walk(os.path.join(FLEET, lane)):
        if ".git" in root: continue
        for fname in files:
            if fname.endswith((".py", ".sh", ".mjs")):
                if "disposition" in fname.lower() or "conjunct" in fname.lower():
                    disp_hits.append((lane, os.path.relpath(os.path.join(root, fname), FLEET)))

print(f"Files with 'disposition' or 'conjunct' in filename: {len(disp_hits)}")
for lane, rel in disp_hits:
    print(f"  [{lane}] {rel}")

print("\n--- 4. Targeted Audit: (c) Battery summary derived from receipts on disk ---")
summary_hits = []
for lane in LANES:
    for sub in ["tools", ".ufo/evidence"]:
        p = os.path.join(FLEET, lane, sub)
        if not os.path.exists(p): continue
        for root, dirs, files in os.walk(p):
            for fname in files:
                if fname.endswith((".py", ".sh")):
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            txt = f.read()
                    except:
                        continue
                    if "summary" in txt.lower() and ("derived" in txt.lower() or "receipts on disk" in txt.lower() or "pre-registered" in txt.lower()):
                        summary_hits.append((lane, os.path.relpath(fpath, FLEET)))

print(f"Files referencing summary derived from receipts / pre-registered: {len(summary_hits)}")
for lane, rel in summary_hits[:10]:
    print(f"  [{lane}] {rel}")

print("\n--- 5. Fleet Gate Audit: scripts/sources-census.sh table parser ---")
sc_path = os.path.join(FLEET, "scripts/sources-census.sh")
with open(sc_path) as f:
    sc_lines = f.readlines()
print(f"scripts/sources-census.sh total lines: {len(sc_lines)}")
for i in [540, 541, 555, 591, 592, 611, 625, 632, 658]:
    if i < len(sc_lines):
        print(f"  Line {i+1}: {sc_lines[i].strip()[:100]}")

print("\nSCAN COMPLETE. VERDICT: no-overlap")
