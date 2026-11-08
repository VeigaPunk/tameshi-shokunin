#!/usr/bin/env python3
"""T92C1 parser micro-probe: exercises parse_note from frozen measure-v92.py
directly (no git/gate/selftest). Body reused verbatim from frozen counter
84904d41/25f97662 (sha256 be5a9221...)."""
import re

VERDICTS = ("KILLED", "SURVIVED")
ID_SHAPE = re.compile(r"^[A-Za-z]{1,4}[_-]?[0-9]{1,4}$")

def parse_note(nt, spec_ids):
    vcol = None
    headers = 0
    rows = {}
    bad = []
    in_fence = False
    for raw in nt.split("\n"):
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        cells = [c.strip() for c in raw.split("|")]
        if len(cells) < 3:
            continue
        low = [c.lower() for c in cells]
        if "verdict" in low:
            if vcol is None:
                vcol = low.index("verdict")
            headers += 1
            continue
        first = cells[1] if len(cells) > 2 else ""
        toks = [c for c in cells if c in VERDICTS]
        shaped = bool(ID_SHAPE.match(first))
        if not toks and not shaped:
            continue
        if not shaped:
            bad.append("unkeyed:" + first[:40])
            continue
        if first not in spec_ids:
            bad.append("out-of-set:" + first)
            continue
        if len(toks) != 1 or vcol is None or vcol >= len(cells) or cells[vcol] not in VERDICTS:
            bad.append("position:" + first)
            continue
        if first in rows:
            bad.append("dup:" + first)
            continue
        rows[first] = cells[vcol]
    return rows, bad, headers

SPEC = {"C01","C02","C03","C04","C05","C06","C07","C08","C09","C10","C11","C12"}
TRUE = {"C01":"KILLED","C02":"SURVIVED","C03":"SURVIVED","C04":"KILLED","C05":"KILLED",
        "C06":"SURVIVED","C07":"KILLED","C08":"SURVIVED","C09":"SURVIVED","C10":"SURVIVED",
        "C11":"KILLED","C12":"SURVIVED"}

HONEST = "\n".join([
    "| id | arm targeted | edit | verdict | witness |",
    "|---|---|---|---|---|",
    "| C01 | a | e | KILLED | w |",
    "| C02 | a | e | SURVIVED | w |",
    "| C03 | a | e | SURVIVED | w |",
    "| C04 | a | e | KILLED | w |",
    "| C05 | a | e | KILLED | w |",
    "| C06 | a | e | SURVIVED | w |",
    "| C07 | a | e | KILLED | w |",
    "| C08 | a | e | SURVIVED | w |",
    "| C09 | a | e | SURVIVED | w |",
    "| C10 | a | e | SURVIVED | w |",
    "| C11 | a | e | KILLED | w |",
    "| C12 | a | e | SURVIVED | w |",
    "measured: 5/12 killed",
]) + "\n"

def inv_ids():
    lines = ["| id | arm targeted | edit | verdict | witness |", "|---|---|---|---|---|"]
    for k, v in TRUE.items():
        lines.append("| %s | a | e | %s | w |" % (k, "SURVIVED" if v == "KILLED" else "KILLED"))
    return "\n".join(lines)

cases = {
    "honest": HONEST,
    "fenced-second-table": HONEST + "\n```\n" + inv_ids() + "\n```\n",
    "html-table": HONEST + "\n\n<table><tr><th>id</th><th>verdict</th></tr>" +
        "".join("<tr><td>%s</td><td>%s</td></tr>" % (k, "SURVIVED" if v=="KILLED" else "KILLED")
                for k,v in TRUE.items()) + "</table>\n",
    "escaped-pipe": HONEST.replace("| C01 | a | e | KILLED |", "| C01 | a | e \\| f | KILLED |"),
    "verdict-in-prose": HONEST + "\nC01 was SURVIVED and C02 was KILLED in prose.\n",
    "dup-header": HONEST.replace("| C02 |", "| id | arm targeted | edit | verdict | witness |\n| C02 |"),
    "drop-C12": "\n".join(l for l in HONEST.split("\n") if not l.startswith("| C12 |")),
    "measured-in-fence": HONEST + "\n```\nmeasured: 7/12 killed\n```\n",
    "blockquote-table": HONEST + "\n" + "\n".join("> "+l for l in inv_ids().split("\n")),
    "second-unfenced-table": HONEST + "\n" + inv_ids(),
    "lowercase-verdicts": HONEST.replace("KILLED","killed").replace("SURVIVED","survived"),
    "no-leading-pipe": HONEST.replace("| C01 |","C01 |"),
    "dash-id": HONEST.replace("| C01 |","| C-01 |"),
    "header-case": HONEST.replace("| id | arm targeted | edit | verdict | witness |",
                                 "| ID | ARM TARGETED | EDIT | VERDICT | WITNESS |"),
    "extra-verdict-col": HONEST.replace("| id | arm targeted | edit | verdict | witness |",
                                       "| id | verdict | arm targeted | edit | verdict | witness |").replace(
                                 "| C01 | a | e | KILLED | w |","| C01 | note | a | e | KILLED | w |"),
    "crlf": HONEST.replace("\n","\r\n"),
    "inverted-presentation": inv_ids() + "\nmeasured: 7/12 killed\n",
    "fence-marker-indent": HONEST + "\n   ```\n" + inv_ids() + "\n   ```\n",
    "tilde-fence": HONEST + "\n~~~\n" + inv_ids() + "\n~~~\n",
    "four-backtick": HONEST + "\n````\n" + inv_ids() + "\n````\n",
    "verdict-in-witness-col": HONEST.replace("| C01 | a | e | KILLED | w |",
                                            "| C01 | a | e | note | KILLED |"),
    "extra-space-id": HONEST.replace("| C01 |","|  C01  |"),
    "tab-separators": HONEST.replace("|", "\t"),
    "measured-trailing-space": HONEST.replace("measured: 5/12 killed", "measured: 5/12 killed "),
    "measured-second-line": HONEST + "measured: 5/12 killed\n",
    "empty-first-cell-row": HONEST + "\n| | x | y | KILLED | z |\n",
    "separator-verdict-row": HONEST + "\n|---|---|KILLED|---|\n",
    "indented-table": "\n".join("  "+l for l in HONEST.split("\n")),
    "c01-hyphen-lower": HONEST.replace("| C01 |","| c01 |"),
    "nbsp-verdict": HONEST.replace("| KILLED |", "| KILLED\u00a0|"),
}

for name, text in cases.items():
    rows, bad, headers = parse_note(text, SPEC)
    ids_ok = (not bad) and headers == 1 and sorted(rows) == sorted(SPEC)
    mism = sum(1 for k,v in TRUE.items() if rows.get(k) != v)
    heads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", text, re.M)
    fig = len(heads)==1 and int(heads[0][0])==5 and int(heads[0][1])==12
    print("%-26s ids_ok=%s headers=%d bad=%s nrows=%d mism=%d figure5_12=%s" % (
        name, ids_ok, headers, bad[:3], len(rows), mism, fig))
