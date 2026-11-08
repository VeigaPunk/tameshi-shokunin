#!/usr/bin/env python3
"""R97S1 independent re-open of the two Gate sources (S159 Wikipedia, S006 shmutant).

Renders with the lane's canonical convention (the round-93 tag-strip renderer):
script/style and comments removed, each tag to one space, entities unescaped,
lines right-trimmed. Locates the two lesson quotes and reports their spans.
"""
import hashlib
import html as htmlmod
import os
import re
import subprocess
import sys

WORK = os.path.realpath(sys.argv[1] if len(sys.argv) > 1 else ".")

TARGETS = [
    ("S159", "https://en.wikipedia.org/wiki/Mutation_testing", "s159.html",
     "Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing.",
     762),
    ("S006", "https://github.com/BWBama85/shmutant", "s006.html",
     "A row whose old literal occurs more than once in its target there is refused",
     490),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_tags(raw):
    s = re.sub(r"<script\b[^>]*>.*?</script\s*>", " ", raw, flags=re.S | re.I)
    s = re.sub(r"<style\b[^>]*>.*?</style\s*>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    s = s.replace("\u00a0", " ")
    return [ln.rstrip() for ln in s.split("\n")]


def _bare(tok):
    return tok.strip(".,;:!?\"'()[]")


def locate(lines, quote):
    joined, idx = [], []
    for i, ln in enumerate(lines, 1):
        for tok in ln.split():
            joined.append(_bare(tok))
            idx.append(i)
    qwords = [_bare(w) for w in quote.split()]
    hits, n = [], len(qwords)
    for j in range(len(joined) - n + 1):
        if joined[j:j + n] == qwords:
            hits.append((idx[j], idx[n - 1 + j]))
    out = []
    for h in hits:
        if not out or out[-1] != h:
            out.append(h)
    return out


def fetch(url, dest):
    hdr = dest + ".headers"
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "120",
                        "-D", hdr, "-o", dest, url], capture_output=True, text=True)
    if r.returncode != 0:
        print("FETCH-FAIL %s rc=%d %s" % (url, r.returncode, r.stderr[:200]))
        return False
    return True


def http_date(path):
    for line in open(path, "r", encoding="utf-8", errors="replace"):
        if line.lower().startswith("date:"):
            return line.split(":", 1)[1].strip()
    return ""


def main():
    os.makedirs(WORK, exist_ok=True)
    for sid, url, name, quote, lesson_line in TARGETS:
        dest = os.path.join(WORK, name)
        ok = fetch(url, dest)
        print("=== %s %s ===" % (sid, url))
        if not ok:
            print("  fetch failed")
            continue
        raw = open(dest, "r", encoding="utf-8", errors="replace").read()
        print("  bytes=%d sha256=%s" % (os.path.getsize(dest), sha256_file(dest)))
        print("  http_date=%s" % http_date(dest + ".headers"))
        lines = strip_tags(raw)
        hits = locate(lines, quote)
        print("  quote_words=%d (lesson says: %s)" % (len(quote.split()),
              "14" if sid == "S159" else "16"))
        print("  located_spans=%s" % hits)
        print("  lesson_line=%s" % lesson_line)
        for h in hits[:3]:
            print("  --- span %d-%d ---" % h)
            for i in range(h[0], h[1] + 1):
                print("   %d| %s" % (i, lines[i - 1]))
        # full sentence context for S006 (lesson cites lines 490-492 with a longer text)
        if sid == "S006":
            print("  -- lines 486-496 raw render --")
            for i in range(486, 497):
                if i <= len(lines):
                    print("   %d| %s" % (i, lines[i - 1]))


main()
