#!/usr/bin/env python3
"""Re-verify every quote in T50ExecSrcZeller.json against the saved PDF bytes.

Usage: python3 verify-quotes.py   (run from this directory)
Each quote must appear, after whitespace collapse, on the printed page its
locator names; printed p.N is PDF page N-182 (folios are absent from the text
layer of this mirror). Also checks byte identity of the saved artifacts against
receipt-pdf.json. Exit 0 = every quote and hash verified.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "zeller-delta.pdf")
DELIV = os.path.join(HERE, "T50ExecSrcZeller.json")
RECEIPT = os.path.join(HERE, "receipt-pdf.json")


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def main():
    deliv = json.load(open(DELIV))
    receipt = json.load(open(RECEIPT))
    ok = True

    if sha(PDF) != receipt["sha256"]:
        print("HASH-MISMATCH zeller-delta.pdf")
        ok = False
    if sha(PDF) != deliv["sha256"]:
        print("HASH-MISMATCH deliverable sha256 vs pdf")
        ok = False
    for name, meta in receipt["derived"].items():
        if sha(os.path.join(HERE, name)) != meta["sha256"]:
            print("HASH-MISMATCH", name)
            ok = False

    for q in deliv["quotes"]:
        printed = int(re.search(r"printed p\. (\d+)", q["location"]).group(1))
        page = printed - 182
        text = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), PDF, "-"],
            capture_output=True, text=True, check=True).stdout
        hay = collapse(text)
        needle = collapse(q["quote"])
        words = len(needle.split())
        hit = needle in hay
        ok = ok and hit and words <= 25
        print(f"{'OK  ' if hit else 'MISS'} printed p.{printed} (pdf p.{page}) words={words}  {q['topic']}")

    print("VERIFY_QUOTES:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
