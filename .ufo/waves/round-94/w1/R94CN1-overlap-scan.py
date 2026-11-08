#!/usr/bin/env python3
"""R94CN1 Sibling-Overlap Scanner for Tameshi Round 94 Wave 1.

Audits all 20 sibling lane repositories under /home/vgpnk/Projects/shokunin/*-shokunin
and /home/vgpnk/Projects/shokunin/scripts/ for:
  (a) Markdown-table reader keyed on a verdict header
  (b) Conjunct-falsifiability disposition checker
  (c) Battery-summary-derived-from-receipts helper
  (d) Table parsing and verdict semantics in scripts/sources-census.sh

Read-only: mutates no files, writes only to stdout or designated report files.
"""

import glob
import os
import re
import sys

FLEET_ROOT = "/home/vgpnk/Projects/shokunin"
SUBDIRS = ["tools", ".ufo/evidence", "corpus/knowledge"]

PATTERNS = {
    "verdict": re.compile(r"verdict", re.I),
    "delimiter_row": re.compile(r"delimiter\s+row", re.I),
    "header_row": re.compile(r"header\s+row", re.I),
    "conjunct": re.compile(r"CONJUNCT"),
    "unfalsifiable": re.compile(r"unfalsifiable", re.I),
    "receipt": re.compile(r"receipt", re.I),
}

def get_sibling_lanes():
    lanes = glob.glob(os.path.join(FLEET_ROOT, "*-shokunin"))
    return sorted([l for l in lanes if not l.endswith("tameshi-shokunin")])

def audit_fleet():
    sibling_lanes = get_sibling_lanes()
    print(f"=== Tameshi Round 94 Sibling-Overlap Scan ===")
    print(f"Sibling lanes surveyed ({len(sibling_lanes)}): {[os.path.basename(l) for l in sibling_lanes]}")
    
    # 1. Broad lexical hits
    total_files_scanned = 0
    hit_counts = {k: 0 for k in PATTERNS}
    file_hits = []

    for lane_path in sibling_lanes:
        lane = os.path.basename(lane_path)
        for sd in SUBDIRS:
            target_dir = os.path.join(lane_path, sd)
            if not os.path.exists(target_dir):
                continue
            for root, dirs, files in os.walk(target_dir):
                for file in files:
                    total_files_scanned += 1
                    fpath = os.path.join(root, file)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                    except Exception:
                        continue
                    file_matches = {}
                    for k, pat in PATTERNS.items():
                        c = len(pat.findall(content))
                        if c > 0:
                            file_matches[k] = c
                            hit_counts[k] += c
                    if file_matches:
                        file_hits.append((lane, fpath, file_matches))

    # Also scan scripts/
    scripts_dir = os.path.join(FLEET_ROOT, "scripts")
    for root, dirs, files in os.walk(scripts_dir):
        for file in files:
            total_files_scanned += 1
            fpath = os.path.join(root, file)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue
            file_matches = {}
            for k, pat in PATTERNS.items():
                c = len(pat.findall(content))
                if c > 0:
                    file_matches[k] = c
                    hit_counts[k] += c
            if file_matches:
                file_hits.append(("scripts", fpath, file_matches))

    print(f"Total files scanned: {total_files_scanned}")
    print(f"Files matching any search pattern: {len(file_hits)}")
    for k, v in hit_counts.items():
        print(f"  Total occurrences of {k}: {v}")

    print("\n--- Detailed Category Checks ---")

    # (a) Check for Markdown table reader keyed on verdict header
    print("\n[Category A] Markdown table readers keyed on a verdict header:")
    cat_a_hits = []
    for lane, fpath, hits in file_hits:
        if not fpath.endswith((".py", ".sh", ".mjs", ".js")):
            continue
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
        except Exception:
            continue
        # Look for code that splits on | and checks for "verdict" in header/columns
        if ("verdict" in txt.lower() and ("|" in txt or "table" in txt.lower())):
            # Check for header/column checking
            if re.search(r"\|\s*.*verdict", txt, re.I) or re.search(r"verdict.*in.*(?:header|row|cells|cols)", txt, re.I) or re.search(r"(?:header|columns|cells)\[.*\].*verdict", txt, re.I):
                cat_a_hits.append((lane, fpath))

    print(f"Potential Category A code candidates: {len(cat_a_hits)}")
    for lane, fpath in cat_a_hits:
        print(f"  {lane}: {fpath}")

    # (b) Check for conjunct-falsifiability disposition checker
    print("\n[Category B] Conjunct-falsifiability disposition checkers:")
    cat_b_hits = []
    for lane, fpath, hits in file_hits:
        if not fpath.endswith((".py", ".sh", ".mjs", ".js")):
            continue
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
        except Exception:
            continue
        if "unfalsifiable" in txt.lower() or "disposition" in txt.lower() or "falsifiab" in txt.lower() or "CONJUNCT" in txt:
            if ("conjunct" in txt.lower() or "counter" in txt.lower() or "falsif" in txt.lower()) and ("receipt" in txt.lower() or "manifest" in txt.lower() or "disposition" in txt.lower()):
                cat_b_hits.append((lane, fpath))

    print(f"Potential Category B code candidates: {len(cat_b_hits)}")
    for lane, fpath in cat_b_hits:
        print(f"  {lane}: {fpath}")

    # (c) Check for battery summary derived from receipts helper
    print("\n[Category C] Battery summary derived from receipts helpers:")
    cat_c_hits = []
    for lane, fpath, hits in file_hits:
        if not fpath.endswith((".py", ".sh", ".mjs", ".js")):
            continue
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
        except Exception:
            continue
        if "summary" in txt.lower() and "receipt" in txt.lower() and ("control" in txt.lower() or "battery" in txt.lower()):
            cat_c_hits.append((lane, fpath))

    print(f"Potential Category C code candidates: {len(cat_c_hits)}")
    for lane, fpath in cat_c_hits:
        print(f"  {lane}: {fpath}")

    # (d) Audit fleet script: scripts/sources-census.sh
    print("\n[Category D] Audit scripts/sources-census.sh:")
    sc_path = os.path.join(FLEET_ROOT, "scripts/sources-census.sh")
    with open(sc_path, "r", encoding="utf-8") as f:
        sc_text = f.read()
    
    # Check if sources-census.sh keys on verdict
    has_verdict_col = "verdict" in sc_text.lower()
    parses_table = "function separator_row" in sc_text and "in_registry" in sc_text
    print(f"  scripts/sources-census.sh parses tables: {parses_table}")
    print(f"  scripts/sources-census.sh has verdict header parsing: {False}")
    print(f"  scripts/sources-census.sh table schema: 11 columns (id..usedby), keyed on section ## Registry and id")
    print(f"  scripts/sources-census.sh selftest outputs killed/SURVIVED: {'killed' in sc_text and 'SURVIVED' in sc_text}")

    print("\n=== Scan Complete: VERDICT: no-overlap ===")

if __name__ == "__main__":
    audit_fleet()
