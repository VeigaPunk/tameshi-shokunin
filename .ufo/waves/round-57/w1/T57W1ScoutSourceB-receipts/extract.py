#!/usr/bin/env python3
"""Extract readable text + heading anchors from fetched HTML pages (stdlib only)."""
import re, sys, html

def extract(path, out_txt, out_headings):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    heads = []
    def keep_h(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else ""
        text = html.unescape(re.sub(r"(?s)<[^>]+>", " ", inner))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            heads.append((tag.lower(), hid, text))
        return f"\n\n== {text} [#{hid}] ==\n\n"
    body = re.sub(r"(?is)<(h[1-6])((?:[^>\"]|\"[^\"]*\")*)>(.*?)</\1>", keep_h, raw)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    body = html.unescape(body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r" ?\n ?", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    open(out_txt, "w", encoding="utf-8").write(body)
    with open(out_headings, "w", encoding="utf-8") as f:
        for tag, hid, text in heads:
            f.write(f"{tag}\t#{hid}\t{text}\n")

base = "/fast/scratch/hyaku/tameshi-r57/T57W1ScoutSourceB"
for name in ("sre-book-postmortem-culture", "sre-workbook-postmortem-culture", "atlassian-postmortems"):
    extract(f"{base}/{name}.html", f"{base}/{name}.txt", f"{base}/{name}.headings")
    print(name, "ok")
