#!/usr/bin/env python3
"""T92R1 review probes (run against a copy of the frozen counter). Read-only.
Usage: python3 -I T92R1-probe.py <path-to-measure-v92.py> [variant-dir]
"""
import importlib.util, sys, re, hashlib, subprocess, os

def load(p):
    s = importlib.util.spec_from_file_location("c1", p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m

def main():
    counter = sys.argv[1]
    c1 = load(counter)
    ids = {f"C{i:02d}" for i in range(1,13)}
    H = "| id | arm targeted | edit | verdict | witness |"
    S = "|---|---|---|---|---|"
    def tbl(rows): return "\n".join([H,S]+[f"| {cid} | a | e | {v} | w |" for cid,v in rows])
    honest = tbl([(cid, "KILLED") for cid in sorted(ids)])
    rows,bad,h = c1.parse_note(honest, ids)
    print("honest:", len(rows), bad, h)
    # fenced contradiction (backticks) -> skipped entirely
    inv = ["```", H, S] + [f"| {cid} | a | e | SURVIVED | w |" for cid in sorted(ids)] + ["```"]
    r2,b2,h2 = c1.parse_note(honest+"\n"+"\n".join(inv), ids)
    print("fenced-contradiction:", len(r2), b2, h2)  # expected 12 rows no bad headers=1
    # tilde fence -> counted, dup
    tilde = ["~~~", H, S] + [f"| {cid} | a | e | SURVIVED | w |" for cid in sorted(ids)] + ["~~~"]
    print("tilde-fenced headers:", c1.parse_note(honest+"\n"+"\n".join(tilde), ids)[2:])
    # indented code table (4 spaces) -> counted, dup
    tbl11 = [f"| {cid} | a | e | KILLED | w |" for cid in sorted(ids)]
    r11,b11,h11 = c1.parse_note(honest+"\n    | C01 | a | e | SURVIVED | w |", ids)
    print("indented-contradictory:", b11, len(r11))
    # witness-cell exact 'verdict' inflates header count
    t6 = [H,S]+[f"| {cid} | a | e | KILLED | w |" for cid in sorted(ids)]
    t6[2] = "| C01 | a | e | KILLED | verdict |"
    print("witness==verdict headers:", c1.parse_note("\n".join(t6), ids)[2])
    # measured regex is fence-blind
    nt12 = "measured: 12/12 killed\n```\nmeasured: 6/12 killed\n```\n"
    print("measured heads:", re.findall(r"^measured: (\d+)/(\d+) killed\s*$", nt12, re.M))
    # escaped pipe
    t8 = [H,S]+[f"| {cid} | a | e | KILLED | w |" for cid in sorted(ids)]
    t8[3] = "| C02 | a | e | KILLED \\| junk | w |"
    print("escaped-pipe-in-verdict:", c1.parse_note("\n".join(t8), ids)[1])
    # measured spacing strictness
    for s in ["measured:  12/12 killed","measured: 12/12 killed ","measured: +12/12 killed","measured: 03/12 killed"]:
        print("measured:", repr(s), re.findall(r"^measured: (\d+)/(\d+) killed\s*$", s, re.M))
    # self-pin arithmetic: duplicated / moved pin lines keep normalized digest
    src = open(counter,"rb").read()
    PIN = c1.SELF_SHA256
    pinline = (b'SELF_SHA256 = "' + PIN.encode() + b'"\n')
    import re as _re
    def digest(b): return hashlib.sha256(_re.sub(c1.SELF_PIN_RE, b"", b, flags=_re.M)).hexdigest() == PIN
    print("pin self-check:", digest(src))
    print("pin duplicated:", digest(src.replace(pinline, pinline+pinline)))
    parts = src.split(pinline)
    print("pin moved-to-end:", digest(parts[0]+parts[1]+pinline))
    print("pin hex-zeroed (still 'true' arithmetically):", digest(src.replace(PIN.encode(), b"0"*64)))
    print("done")

if __name__ == "__main__":
    main()
