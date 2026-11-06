#!/usr/bin/env python3
"""T90SC1 probe: the fixture-absence facts behind the seven SURVIVED rows.

Reads ONLY committed bytes: the pinned gate blob and its fixture tree, both from
the fleet object store at `<fleet> <PIN>`. Writes nothing; prints one line per
fact. Re-runnable by the L1 from committed bytes.

Usage: python3 -I T90SC1-fixture-absence.py FLEET_ROOT PIN
       python3 -I T90SC1-fixture-absence.py /home/vgpnk/Projects/shokunin f47ad6ba8d306f8125597401cb2ce45c1297a593
"""
import re
import subprocess
import sys

FLEET = sys.argv[1]
PIN = sys.argv[2]
GATE = "scripts/sources-census.sh"
FIX = "scripts/fixtures/sources-census"

ROW = re.compile(r"(?:\|[^|\n]*){11}\|")          # 11 cells, trailing pipe
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NDAY = re.compile(r"^\d+d$")


def git(*a):
    p = subprocess.run(["git", "-C", FLEET, *a], capture_output=True, check=True)
    return p.stdout


def cells(m):
    return [c.strip() for c in m.group(0).split("|")[1:-1]]


def is_sep(c):
    return bool(c) and all(re.fullmatch(r":?-+:?", x) for x in c)


def rows_of(text, label):
    out = []
    for m in ROW.finditer(text):
        c = cells(m)
        if len(c) != 11:
            continue
        if c[0] == "id" or is_sep(c):
            continue
        out.append((label, c))
    return out


def seps_of(text):
    out = []
    for m in ROW.finditer(text):
        c = cells(m)
        if is_sep(c):
            out.append(c)
    return out


gate = git("show", f"{PIN}:{GATE}").decode()
fixfiles = [p for p in git("ls-tree", "-r", "--name-only", PIN, FIX).decode().split("\n") if p]
fixtures = {p: git("show", f"{PIN}:{p}").decode() for p in fixfiles}

fix_rows, gate_rows, fix_seps, gate_seps = [], [], [], []
for p, t in fixtures.items():
    fix_rows += rows_of(t, p)
    fix_seps += seps_of(t)
gate_rows = rows_of(gate, GATE)
gate_seps = seps_of(gate)

print(f"PIN {PIN} gate_blob_sha256 {__import__('hashlib').sha256(git('cat-file', 'blob', f'{PIN}:{GATE}')).hexdigest()}")
print(f"COUNT fixture_files {len(fixfiles)} fixture_rows {len(fix_rows)} gate_embedded_rows {len(gate_rows)}")

all_rows = fix_rows + gate_rows
print(f"SEP total {len(fix_seps) + len(gate_seps)} with_colon "
      f"{sum(1 for c in fix_seps + gate_seps if any(':' in x for x in c))}")

frag = [(lab, c[0], c[1]) for lab, c in all_rows if "#" in c[1]]
print(f"URL_FRAGMENT rows_with_fragment {len(frag)}" + (f" {frag}" if frag else " (no URL cell carries #)"))

sup_fix = sum(t.count("supersedes") for t in fixtures.values())
sup_gate = gate.count("supersedes")
print(f"SUPERSEDES fixture_occurrences {sup_fix} gate_occurrences {sup_gate} "
      f"(gate hits: comment line and regex line " +
      ",".join(str(i + 1) for i, l in enumerate(gate.split("\n")) if "supersedes" in l) + ")")

rej = [(lab.split(FIX + "/")[-1].split("/corpus/")[0] if lab.startswith(FIX) else lab,
        c[0], len(c[6]), c[6])
       for lab, c in all_rows if c[7] == "rejected"]
print(f"REJECTED rows {len(rej)} (lane,id,len,teaches): {rej}")
print(f"REJECTED exactly_7_chars {sum(1 for r in rej if r[2] == 7)}")

sym = sorted({c[9] for lab, c in all_rows
              if not DATE.match(c[9]) and not NDAY.match(c[9]) and c[9]})
print(f"SYMBOLIC_CADENCE distinct {sym} with_space {[s for s in sym if ' ' in s]}")

ub = {}
for lab, c in all_rows:
    v = c[10]
    if v in ("—", ""):
        continue
    ub.setdefault(v, set()).add(lab)
print(f"USED_BY distinct {sorted(ub)} with_comma {[v for v in ub if ',' in v]}")

# Resolve fixture used-by cells inside the pinned blob list: -e and -f differ only on directories.
def kind_of(key):
    if any(p == key for p in fixfiles):
        return "file"
    if any(p.startswith(key + "/") for p in fixfiles):
        return "dir"
    return "absent"


kinds = []
for lab, c in fix_rows:
    for v in c[10].split(","):
        v = v.strip()
        if v in ("", "—"):
            continue
        lane_dir = lab.rsplit("/corpus/", 1)[0]
        kinds.append((lane_dir.split(FIX + "/")[-1], c[0], v, kind_of(lane_dir + "/" + v)))
print(f"USED_BY_KIND fixture_cells (lane,id,path,file|dir|absent): {kinds}")
print(f"USED_BY_DIRECTORY fixture_cells_naming_a_directory {sum(1 for k in kinds if k[3] == 'dir')}")
