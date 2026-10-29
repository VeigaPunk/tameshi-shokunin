import re, sys, html
def extract(path, out_txt):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    body = re.sub(r"(?is)<(h[1-6])[^>]*>(.*?)</\1>", lambda m: "\n\n== " + re.sub(r"\s+"," ",html.unescape(re.sub(r"(?s)<[^>]+>"," ",m.group(2)))).strip() + " ==\n\n", raw)
    body = re.sub(r"(?s)<br\s*/?>|</p>|</li>|</div>", "\n", body)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    body = html.unescape(body)
    body = re.sub(r"[ \t\r\f\v]+", " ", body)
    body = re.sub(r" ?\n ?", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    open(out_txt, "w", encoding="utf-8").write(body)
extract(sys.argv[1], sys.argv[2])
print("ok", sys.argv[2])
