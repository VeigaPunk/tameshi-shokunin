#!/usr/bin/env python3
"""T91CN1-scan.py -- fleet impact of the seven SURVIVED sources-census selftest mutants (R91-C1).

READ-ONLY over the fleet. The gate under test is materialized from git objects at the
pinned revision; every mutant is a single-edit scratch copy under
/fast/scratch/hyaku/tameshi-r91/T91CN1 (removed on exit unless --keep).

Facts established, in order:
  P  pin        gate blob sha256 == spec .gate.sha256
  V  valid      every survivor's `old` occurs exactly once, new != old, `bash -n` clean
  C  control    a byte-identical pristine copy of the pinned gate reproduces the original
                output on every real registry in census|validate|overdue|shared
  D  diff       original vs each survivor mutant on every real registry (the 21
                *-shokunin/corpus/SOURCES.md under the fleet root), same four modes,
                --today 2026-11-08; output tuple (rc, stdout, stderr) compared
  S  shape      one gawk pass per registry that embeds the pinned gate's own parsing
                primitives verbatim (trim/symbolic/separator_row/url_of, 0-3 leading
                spaces, `## Registry` section only) and emits every table record; the
                class predicates are then evaluated row by row, with an E04/W04 replay of
                the gate's duplicate-URL state machine for C03 and C09.

Usage: python3 T91CN1-scan.py [--keep] [--json PATH] [--hits PATH] [--log PATH]
"""
import argparse
import concurrent.futures as cf
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

FLEET = "/home/vgpnk/Projects/shokunin"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
W1 = LANE + "/.ufo/waves/round-91/w1"
GATE_REV = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
GATE_SHA = "3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30"
SPEC = LANE + "/.ufo/evidence/round-91/c1/census-mutants.json"
SCRATCH = "/fast/scratch/hyaku/tameshi-r91/T91CN1"
TODAY = "2026-11-08"
SURVIVORS = ["C02", "C03", "C06", "C08", "C09", "C10", "C12"]
MODES = ["census", "validate", "overdue", "shared"]
OFS = "\x1f"

# Verbatim fragments asserted in the pinned gate
GATE_LINES = [
    r'function trim(s) { gsub(/^[ \t]+|[ \t]+$/,"",s); return s }',
    r'function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ }',
    r'    function separator_row(   i,c) {',
    r'      if (trim($2)=="id") return 1',
    r'      if (NF<3) return 0',
    r'      if (c !~ /^:?-+:?$/) return 0',
    r'    function url_of(s,   u,n) {',
    r'      if (match(s,/https?:\/\/[^[:space:]|]+/)) { u=substr(s,RSTART,RLENGTH)',
    r'        sub(/#[^ ]*$/,"",u); sub(/\/$/,"",u); sub(/^[A-Za-z]+:\/\//,"",u)',
    r'        n=index(u,"/"); if(n) u=tolower(substr(u,1,n-1)) substr(u,n); else u=tolower(u)',
    r'      if (line ~ /^ {0,3}##[ \t]/) {',
    r'        in_registry=(trim(substr(line,3))=="Registry")',
    r'      if (line ~ /^ {0,3}#[ \t]/) { in_registry=0; next }',
    r'      if (line !~ /^ {0,3}\|/) next',
    r'        sub(/^ {0,3}/,"",line)',
    r'      id=trim($2); source=trim($3); kind=trim($4); tier=trim($5); scope=trim($6)',
    r'      anchor=trim($7); teaches=trim($8); status=trim($9); opened=trim($10)',
    r'      recheck=trim($11); usedby=trim($12)',
    r'        if (status=="rejected" && length(teaches)<8)',
    r'            teaches !~ /supersedes S[0-9]{3}/)',
    r'        if (due!=INVALID_EPOCH && due<=today_s)',
    r'    for path in "${paths[@]}"; do',
    r'      path=$(trim_cell "$path")',
    r'      if [ ! -e "$dir/$path" ]; then',
    '    IFS=\',\' read -r -a paths <<< "$usedby"',
]

SHAPE_AWK = r'''
BEGIN { OFS = "\037" }
function trim(s) { gsub(/^[ \t]+|[ \t]+$/,"",s); return s }
function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ }
function separator_row(   i,c) {
  if (trim($2)=="id") return 1
  if (NF<3) return 0
  for (i=2;i<NF;i++) {
    c=trim($i)
    if (c !~ /^:?-+:?$/) return 0
  }
  return 1
}
function url_of(s,   u,n) {
  if (match(s,/https?:\/\/[^[:space:]|]+/)) { u=substr(s,RSTART,RLENGTH)
    sub(/#[^ ]*$/,"",u); sub(/\/$/,"",u); sub(/^[A-Za-z]+:\/\//,"",u)
    n=index(u,"/"); if(n) u=tolower(substr(u,1,n-1)) substr(u,n); else u=tolower(u)
    return u }
  return "" }
function url_of_mut(s,   u,n) {
  if (match(s,/https?:\/\/[^[:space:]|]+/)) { u=substr(s,RSTART,RLENGTH)
    sub(/#[^ ]*$/,"&",u); sub(/\/$/,"",u); sub(/^[A-Za-z]+:\/\//,"",u)
    n=index(u,"/"); if(n) u=tolower(substr(u,1,n-1)) substr(u,n); else u=tolower(u)
    return u }
  return "" }
function raw_url(s) {
  if (match(s,/https?:\/\/[^[:space:]|]+/)) return substr(s,RSTART,RLENGTH)
  return "" }
function strip_frag(s,   t) { t=s; sub(/#[^ ]*$/,"",t); return t }
{
  line=$0
  if (line ~ /^ {0,3}##[ \t]/) { sub(/^ {0,3}/,"",line); in_registry=(trim(substr(line,3))=="Registry"); next }
  if (line ~ /^ {0,3}#[ \t]/) { in_registry=0; next }
  if (line !~ /^ {0,3}\|/) next
  sub(/^ {0,3}/,"",line)
  $0=line
  if (!in_registry) {
    if (line ~ /^\|[ \t]*S[0-9]{3,}[ \t]*\|/)
      printf "outside%s%s%s%d%s%s\n", OFS, lane, OFS, NR, OFS, trim($2)
    next
  }
  if (trim($2)=="id") { printf "hdr%s%s%s%d%s%d\n", OFS, lane, OFS, NR, OFS, NF; next }
  if (separator_row()) {
    colon=0
    for (i=2;i<NF;i++) if (index(trim($i),":")) colon=1
    printf "sep%s%s%s%d%s%d%s%d\n", OFS, lane, OFS, NR, OFS, NF, OFS, colon
    next
  }
  f["k"]="row"; f["lane"]=lane; f["line"]=NR; f["id"]=trim($2)
  f["kind"]=trim($4); f["tier"]=trim($5); f["scope"]=trim($6); f["anchor"]=trim($7)
  f["teaches"]=trim($8); f["tlen"]=length(f["teaches"]); f["status"]=trim($9)
  f["opened"]=trim($10); f["recheck"]=trim($11); f["usedby"]=trim($12); f["nf"]=NF
  f["sym"]=symbolic(f["recheck"]); f["space"]=(f["recheck"] ~ / /)
  f["raw"]=raw_url($3); f["old"]=url_of($3); f["new"]=url_of_mut($3)
  f["fragless"]=strip_frag(f["raw"])
  printf "%s", f["k"]
  n=split("lane line id kind tier scope anchor teaches tlen status opened recheck usedby nf sym space raw old new fragless", keys, " ")
  for (i=1;i<=n;i++) printf "%s%s", OFS, f[keys[i]]
  printf "\n"
}
'''

def die(msg):
    print("T91CN1_SCAN_FAIL: " + msg, file=sys.stderr)
    sys.exit(2)

def git_blob(rev, path):
    p = subprocess.run(["git", "-C", FLEET, "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode != 0:
        die(f"git show failed for {rev}:{path}: {p.stderr.decode(errors='replace')}")
    return p.stdout

def run_gate(gate, mode, reg):
    p = subprocess.run(
        ["bash", gate, mode, "--file", reg, "--today", TODAY],
        capture_output=True, text=True, cwd=SCRATCH, timeout=180,
    )
    return (p.returncode, p.stdout, p.stderr)

def parse_records(text, lane):
    out = []
    for raw in text.splitlines():
        if not raw:
            continue
        f = raw.split(OFS)
        if f[0] == "row":
            keys = "lane line id kind tier scope anchor teaches tlen status opened recheck usedby nf sym space raw old new fragless".split()
            d = dict(zip(keys, f[1:]))
            d["kindrec"] = "row"
            d["line"] = int(d["line"])
            d["nf"] = int(d["nf"])
            d["tlen"] = int(d["tlen"])
        elif f[0] == "sep":
            d = {"kindrec": "sep", "lane": f[1], "line": int(f[2]), "nf": int(f[3]), "colon": int(f[4])}
        elif f[0] == "hdr":
            d = {"kindrec": "hdr", "lane": f[1], "line": int(f[2]), "nf": int(f[3])}
        else:
            d = {"kindrec": "outside", "lane": f[1], "line": int(f[2]), "id": f[3]}
        out.append(d)
    return out

def replay(rows, url_field):
    url_seen = set()
    scope_seen = set()
    scope_nonrejected = set()
    out = {}
    for r in rows:
        if r["nf"] != 13:
            continue
        u = r[url_field]
        scope = r["scope"]
        skey = (u, scope)
        codes = []
        if u and u in url_seen and skey not in scope_seen:
            codes.append("W04")
        if u and skey in scope_seen and r["status"] != "rejected" and skey in scope_nonrejected:
            if not re.search(r"supersedes S[0-9]{3}", r["teaches"]):
                codes.append("E04")
        if u:
            url_seen.add(u)
            scope_seen.add(skey)
            if r["status"] != "rejected":
                scope_nonrejected.add(skey)
        out[r["line"]] = codes
    return out

def replay_exempt(rows):
    url_seen = set()
    scope_seen = set()
    scope_nonrejected = set()
    out = {}
    for r in rows:
        if r["nf"] != 13:
            continue
        u = r["old"]
        scope = r["scope"]
        skey = (u, scope)
        codes = []
        if u and u in url_seen and skey not in scope_seen:
            codes.append("W04")
        if u and skey in scope_seen and r["status"] != "rejected" and skey in scope_nonrejected:
            if not re.search(r"supersedes S[0-9]{4}", r["teaches"]):
                codes.append("E04")
        if u:
            url_seen.add(u)
            scope_seen.add(skey)
            if r["status"] != "rejected":
                scope_nonrejected.add(skey)
        out[r["line"]] = codes
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--json", default=W1 + "/T91CN1-scan.out.json")
    ap.add_argument("--hits", default=W1 + "/T91CN1-hits.tsv")
    ap.add_argument("--log", default=W1 + "/T91CN1-scan.log")
    args = ap.parse_args()

    os.makedirs(SCRATCH, exist_ok=True)
    log = []

    def emit(msg):
        print(msg)
        log.append(msg)

    try:
        spec = json.load(open(SPEC))
        if spec["gate"]["sha256"] != GATE_SHA or spec["gate"]["commit"] != GATE_REV:
            die("spec pin disagrees with this script's constants")

        gate_bytes = git_blob(GATE_REV, "scripts/sources-census.sh")
        got = hashlib.sha256(gate_bytes).hexdigest()
        if got != GATE_SHA:
            die(f"pinned gate sha256 mismatch: {got}")
        emit(f"PIN ok gate={GATE_REV[:12]} sha256={got} bytes={len(gate_bytes)}")

        gate_text = gate_bytes.decode()
        orig = SCRATCH + "/gate.orig.sh"
        with open(orig, "wb") as fh:
            fh.write(gate_bytes)
        os.chmod(orig, 0o755)

        pristine = SCRATCH + "/gate.pristine.sh"
        shutil.copyfile(orig, pristine)
        os.chmod(pristine, 0o755)

        missing = [ln for ln in GATE_LINES if ln not in gate_text]
        if missing:
            die("shape scan cross-check failed; lines absent from pinned gate: " + repr(missing[:3]))
        emit(f"SHAPECHECK ok {len(GATE_LINES)}/{len(GATE_LINES)} gate fragments present verbatim")

        shape_awk = SCRATCH + "/shape.awk"
        with open(shape_awk, "w") as fh:
            fh.write(SHAPE_AWK)

        mutants = {}
        for m in spec["mutants"]:
            if m["id"] not in SURVIVORS:
                continue
            n = gate_text.count(m["old"])
            if n != 1:
                die(f"{m['id']}: old string occurs {n} times")
            if m["old"] == m["new"]:
                die(f"{m['id']}: new == old")
            text = gate_text.replace(m["old"], m["new"], 1)
            path = SCRATCH + f"/gate.{m['id']}.sh"
            with open(path, "w") as fh:
                fh.write(text)
            os.chmod(path, 0o755)
            p = subprocess.run(["bash", "-n", path], capture_output=True, text=True)
            if p.returncode != 0:
                die(f"{m['id']}: bash -n failed: {p.stderr}")
            mutants[m["id"]] = path
        if sorted(mutants) != SURVIVORS:
            die(f"survivor set mismatch: {sorted(mutants)}")
        emit(f"VALID ok {len(mutants)} survivors built as single-edit scratch copies and bash -n clean")

        regs = sorted(glob.glob(FLEET + "/*-shokunin/corpus/SOURCES.md"))
        regs = [r for r in regs if os.path.isfile(r)]
        if not regs:
            die("no registries found")
        lanes = {r: os.path.basename(os.path.dirname(os.path.dirname(r))) for r in regs}
        emit(f"FLEET registries={len(regs)} lanes={sorted(set(lanes.values()))}")

        # ---- C: pristine copy control (all registries, all modes) -----------------
        tasks = [(g, mode, r) for r in regs for mode in MODES for g in (orig, pristine)]
        results = {}
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(run_gate, g, mode, r): (g, mode, r) for g, mode, r in tasks}
            for fut in cf.as_completed(futs):
                g, mode, r = futs[fut]
                results[(g, mode, r)] = fut.result()
        control_bad = [r for r in regs for mode in MODES
                       if results[(orig, mode, r)] != results[(pristine, mode, r)]]
        if control_bad:
            die(f"pristine copy control failed on {len(control_bad)} registry/mode pairs")
        emit(f"CONTROL ok pristine copy reproduces original on {len(regs)}x{len(MODES)} runs")

        # ---- D: differential runs -------------------------------------------------
        tasks = [(mid, mode, r) for mid in SURVIVORS for r in regs for mode in MODES]
        diffs = {mid: {} for mid in SURVIVORS}
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(run_gate, mutants[mid], mode, r): (mid, mode, r) for mid, mode, r in tasks}
            for fut in cf.as_completed(futs):
                mid, mode, r = futs[fut]
                base = results[(orig, mode, r)]
                got = fut.result()
                if got != base:
                    diffs[mid].setdefault(r, {})[mode] = {
                        "rc": [base[0], got[0]],
                        "added": [ln for ln in got[1].splitlines() if ln not in base[1].splitlines()],
                        "removed": [ln for ln in base[1].splitlines() if ln not in got[1].splitlines()],
                        "stderr_changed": base[2] != got[2],
                    }
        for mid in SURVIVORS:
            modes = {}
            for r, per in diffs[mid].items():
                for mode in per:
                    modes[mode] = modes.get(mode, 0) + 1
            emit(f"DIFF {mid} lanes_diff={len(diffs[mid])} by_mode={json.dumps(modes, sort_keys=True)}")

        # ---- S: shape scan --------------------------------------------------------
        recs = {}
        for r in regs:
            p = subprocess.run(["gawk", "-F|", "-f", shape_awk, "-v", f"lane={lanes[r]}", r],
                               capture_output=True, text=True, timeout=120)
            if p.returncode != 0:
                die(f"shape gawk failed on {r}: {p.stderr}")
            recs[r] = parse_records(p.stdout, lanes[r])

        classes = {}
        extras = {c: {} for c in SURVIVORS}
        hit_rows = []

        def bump(key, n=1):
            extras[key[0]][key[1]] = extras[key[0]].get(key[1], 0) + n

        def record(cls, reg, rec, detail, effective=True):
            rel = reg[len(FLEET) + 1:]
            classes[cls].append({"lane": lanes[reg], "registry": rel,
                                 "line": rec["line"], "id": rec.get("id", ""),
                                 "detail": detail, "effective": effective})
            hit_rows.append((cls, rel, rec["line"], rec.get("id", ""), effective, detail))

        for c in SURVIVORS:
            classes[c] = []

        for r in regs:
            lane = lanes[r]
            lane_dir = os.path.dirname(os.path.dirname(r))
            rows = [x for x in recs[r] if x["kindrec"] == "row"]
            seps = [x for x in recs[r] if x["kindrec"] == "sep"]

            # C06: separator rows carrying alignment colons
            for rec in seps:
                if rec["colon"]:
                    record("C06", r, rec, f"colon separator nf={rec['nf']}")

            # C02: rejected rows whose trimmed teaches is exactly 7 chars
            for rec in rows:
                if rec["nf"] == 13 and rec["status"] == "rejected" and int(rec["tlen"]) == 7:
                    record("C02", r, rec, f"teaches={rec['teaches']!r} len=7")

            # C03 shape + E04 replay effect
            old3 = re.compile(r"supersedes S[0-9]{3}")
            new4 = re.compile(r"supersedes S[0-9]{4}")
            shape3 = [x for x in rows if x["nf"] == 13 and x["status"] != "rejected"
                      and old3.search(x["teaches"]) and not new4.search(x["teaches"])]
            if shape3:
                base = replay(rows, "old")
                mut = replay_exempt(rows)
                for rec in shape3:
                    detail = "teaches=" + rec["teaches"][:60]
                    if "E04" in mut[rec["line"]] and "E04" not in base[rec["line"]]:
                        record("C03", r, rec, "E04-flip " + detail, True)
                    else:
                        record("C03", r, rec, "shape-only " + detail, False)

            # C09: fragment-only URL collisions, same-scope (literal class) and cross-scope
            # (W04 surface), plus any other row whose E04/W04 verdict the mutant changes.
            base9 = replay(rows, "old")
            mut9 = replay(rows, "new")
            by_scope = {}
            for rec in rows:
                if rec["raw"]:
                    by_scope.setdefault(rec["scope"], []).append(rec)
            frag_hit = {}
            for scope, group in by_scope.items():
                if len(group) < 2:
                    continue
                keyed = {}
                for rec in group:
                    keyed.setdefault(rec["fragless"], []).append(rec)
                for key, same in keyed.items():
                    raws = {x["raw"] for x in same}
                    if len(same) >= 2 and len(raws) >= 2:
                        for rec in same:
                            frag_hit[rec["line"]] = (scope, key)
            by_key = {}
            for rec in rows:
                if rec["raw"]:
                    by_key.setdefault(rec["fragless"], []).append(rec)
            cross_hit = {}
            for key, same in by_key.items():
                if len({x["scope"] for x in same}) >= 2 and len({x["raw"] for x in same}) >= 2:
                    for rec in same:
                        cross_hit[rec["line"]] = key
            for rec in rows:
                flip = base9[rec["line"]] != mut9[rec["line"]]
                if rec["line"] in frag_hit:
                    arm = "same-scope"
                elif rec["line"] in cross_hit:
                    arm = "cross-scope"
                elif flip:
                    arm = "cascade"
                else:
                    continue
                detail = f"arm={arm} flip={int(flip)} scope={rec['scope']} url={rec['raw']}"
                record("C09", r, rec, detail, flip)
                bump(("C09", "arm_" + arm))
                bump(("C09", f"arm_{arm}_flip"), 1 if flip else 0)

            # C10: symbolic cadence containing a space
            for rec in rows:
                if rec["sym"] == "1" and rec["space"] == "1":
                    detail = f"recheck={rec['recheck']!r} nf={rec['nf']}"
                    record("C10", r, rec, detail)

            # C08: mined row whose used-by names a directory on disk
            for rec in rows:
                if int(rec["nf"]) < 12 or rec["status"] != "mined":
                    continue
                segs = [s.strip() for s in rec["usedby"].split(",")]
                segs = [s for s in segs if s and s != "\u2014"]
                dirs = [s for s in segs if os.path.isdir(os.path.join(lane_dir, s))]
                if dirs:
                    record("C08", r, rec, "dir used-by " + ",".join(dirs))

            # C12: mined used-by cell with >=2 paths where a raw segment needs trimming
            for rec in rows:
                if int(rec["nf"]) < 12 or rec["status"] != "mined":
                    continue
                raw_segs = rec["usedby"].split(",")
                keep = [(i, s) for i, s in enumerate(raw_segs) if s.strip() and s.strip() != "\u2014"]
                if len(keep) >= 2:
                    padded = [s for _, s in keep if s != s.strip()]
                    if padded:
                        present = sum(1 for p in padded
                                      if os.path.exists(os.path.join(lane_dir, p.strip())))
                        record("C12", r, rec,
                               f"paths={len(keep)} padded={len(padded)} present={present} "
                               f"first={padded[0][:60]!r}")
                        bump(("C12", "rows"))
                        bump(("C12", "padded_segments"), len(padded))
                        bump(("C12", "padded_present"), present)

        # ---- summary --------------------------------------------------------------
        summary = {}
        for c in SURVIVORS:
            rows_c = classes[c]
            lanes_c = sorted({x["lane"] for x in rows_c})
            eff = [x for x in rows_c if x["effective"]]
            lanes_eff = sorted({x["lane"] for x in eff})
            lanes_diff = sorted({lanes[r] for r in diffs[c]})
            ex = eff[0] if eff else (rows_c[0] if rows_c else None)
            summary[c] = {
                "lanes_hit": lanes_c,
                "n_lanes": len(lanes_c),
                "rows_hit": len(rows_c),
                "effective_rows": len(eff),
                "lanes_effective": lanes_eff,
                "n_lanes_effective": len(lanes_eff),
                "lanes_diff": lanes_diff,
                "n_lanes_diff": len(lanes_diff),
                "extras": extras[c],
                "example": f"{ex['registry']}:{ex['line']} ({ex['detail']})" if ex else None,
                "differential": {lanes[r]: diffs[c][r] for r in diffs[c]},
            }
            emit(f"CLASS {c} lanes_shape={len(lanes_c)} rows_shape={len(rows_c)} "
                 f"rows_effective={len(eff)} lanes_effective={len(lanes_eff)} "
                 f"lanes_diff={len(lanes_diff)} extras={json.dumps(extras[c], sort_keys=True)}")
            emit(f"  EXAMPLE {c} {summary[c]['example']}")
            if sorted(set(lanes_c)) != lanes_eff:
                emit(f"  NOTE {c}: shape-only lanes {sorted(set(lanes_c) - set(lanes_eff))}")
            if lanes_eff != lanes_diff:
                emit(f"  NOTE {c}: shape-vs-diff lane mismatch eff={lanes_eff} diff={lanes_diff}")

        with open(args.json, "w") as fh:
            json.dump({"gate": {"rev": GATE_REV, "sha256": GATE_SHA},
                       "today": TODAY, "registries": [r[len(FLEET) + 1:] for r in regs],
                       "summary": summary}, fh, indent=1, sort_keys=True)
        with open(args.hits, "w") as fh:
            fh.write("class\tregistry\tline\tid\teffective\tdetail\n")
            for cls, rel, line, sid, effective, detail in hit_rows:
                fh.write(f"{cls}\t{rel}\t{line}\t{sid}\t{int(effective)}\t{detail}\n")
        with open(args.log, "w") as fh:
            fh.write("\n".join(log) + "\n")
        emit(f"WROTE {args.json} {args.hits} {args.log}")
        emit("T91CN1_SCAN_OK")
    finally:
        if args.keep:
            print(f"kept {SCRATCH}")
        else:
            shutil.rmtree(SCRATCH, ignore_errors=True)
            print(f"scratch removed {SCRATCH}")

if __name__ == "__main__":
    main()
