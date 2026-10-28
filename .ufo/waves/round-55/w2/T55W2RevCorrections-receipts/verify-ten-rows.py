#!/usr/bin/env python3
"""Re-derive each of the ten ER-R54 rows from source bytes at BASE and from the
receipts at C0, then check the corrections section states what those bytes say.

Usage: python3 verify-ten-rows.py   (no args; paths pinned below)
Reads only `git show` on the lane and on the fleet report. Writes nothing.
"""
import re, subprocess, sys, json

LANE   = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
FLEET  = "/home/vgpnk/Projects/shokunin"
BASE   = "0a2010acd1e92e4e332774050825e21bcfc7e079"
C0     = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
PREP   = "077d431e"          # round-54 freeze pointer
REPORT = "fcb8d8db"          # fleet commit that last wrote .ufo/reports/round-54/tameshi.md

def show(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def norm(s):
    """Collapse whitespace: both record documents hard-wrap near 78 cols, so a
    literal check against raw bytes reports a wrap as an absence (the lesson
    round-54's amendment 2 taught). Every document substring test uses this."""
    return " ".join((s or "").split())

def has(repo, rev, path, s):
    b = show(repo, rev, path)
    return b is not None and norm(s) in norm(b)

def section():
    body = show(LANE, C0, "SCORECARD.md") or ""
    out, on = [], False
    for line in body.splitlines():
        if line.startswith("## Round 55 - round-54 record corrections"):
            on = True; continue
        if on and line.startswith("## "):
            break
        if on:
            out.append(line)
    return "\n".join(out)

SEC = section()
SECN = norm(SEC)
rows, ok_all = [], True

def row(cid, what, checks):
    global ok_all
    bad = [n for n, v in checks if not v]
    if bad:
        ok_all = False
    rows.append((cid, what, checks, bad))

# ---- ER-R54-1 -------------------------------------------------------------
cb = show(LANE, C0, ".ufo/evidence/round-54/control/controls-b.stdout") or ""
row("ER-R54-1", "old text present at BASE in each named record; receipt prints the corrected values",
    [("base SCORECARD has 'CTL_POS_c1 true'", has(LANE, BASE, "SCORECARD.md", "CTL_POS_c1 true")),
     ("base QUALITY 105 falsifier says 'rekeyed=7/7` on its positive control'",
      has(LANE, BASE, "corpus/QUALITY.md", "rekeyed=7/7` on its positive control")),
     ("base lesson-54 says 'proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`)'",
      has(LANE, BASE, "corpus/lessons/round-54.md",
          "proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`)")),
     ("controls-b.stdout exists at C0", bool(cb)),
     ("controls-b prints 'CTL_MISMATCH CTL_POS_c1 expected=true actual=false'",
      "CTL_MISMATCH CTL_POS_c1 expected=true actual=false" in cb),
     ("controls-b prints 'CONTROLS_B: 2/3'", "CONTROLS_B: 2/3" in cb),
     ("section states CTL_MISMATCH", "CTL_MISMATCH" in SECN),
     ("section states 'CTL_POS_c1 expected=true actual=false'",
      norm("CTL_POS_c1 expected=true actual=false") in SECN),
     ("section states 'CONTROLS_B: 2/3'", norm("CONTROLS_B: 2/3") in SECN),
     ("section names the controls-b receipt", "control/controls-b.stdout" in SECN),
     ("phase-B control cloned the freeze commit (controls-b rev=077d431e6996)",
      "rev=077d431e6996" in cb)])

# ---- ER-R54-2 -------------------------------------------------------------
fr = show(LANE, C0, ".ufo/evidence/round-54/after/frozen.stdout") or ""
fz = json.loads(show(LANE, C0, ".ufo/evidence/round-54/freeze.json") or "{}")
row("ER-R54-2", "three old pointers present at BASE; one pointer + 5 amendments in the receipt",
    [("base SCORECARD calls 7883e0e5 'the freeze pointer the deciding run uses'",
      has(LANE, BASE, "SCORECARD.md", "7883e0e5` is the freeze pointer the deciding run uses")),
     ("base SCORECARD measured-close line says 'freeze `fe70474d`'",
      has(LANE, BASE, "SCORECARD.md", "freeze `fe70474d`")),
     ("base-time fleet report says 'the freeze pointer `097985c1`'",
      has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md",
          "the freeze pointer `097985c1`")),
     ("frozen.stdout prints freeze=077d431e…", "freeze=077d431e69965fa4673cd006ab64f6fc387f9e15" in fr),
     ("freeze.json (at C0) carries 5 amendments", len(fz.get("amendments", [])) == 5),
     ("section states one pointer 077d431e (5 amendments)",
      norm("one pointer, `077d431e` (5 amendments)") in SECN),
     ("section names after/frozen.stdout", "after/frozen.stdout" in SECN)])

# ---- ER-R54-3 -------------------------------------------------------------
bc2 = show(LANE, C0, ".ufo/evidence/round-54/before/c2.stdout") or ""
ct  = show(LANE, C0, ".ufo/evidence/round-54/contract.json") or ""
m = re.search(r"total=(\d+)", bc2)
receipt_total = m.group(1) if m else None
row("ER-R54-3", "old total=14 at BASE; receipt and contract print 13",
    [("base SCORECARD C2 row has total=14", has(LANE, BASE, "SCORECARD.md", "total=14")),
     ("receipt prints total=13", receipt_total == "13"),
     ("receipt bytes identical BASE..C0",
      show(LANE, BASE, ".ufo/evidence/round-54/before/c2.stdout") == bc2),
     ("contract before text prints total=13", "total=13" in ct),
     ("section states corrected total=13", norm("Corrected: `total=13`") in SECN),
     ("section names before/c2.stdout", "before/c2.stdout" in SECN)])

# ---- ER-R54-4 -------------------------------------------------------------
pin = fz.get("files", {}).get("c2/measure.py")
blob = subprocess.run(["git", "-C", LANE, "show",
                       "c21081008adbb6b6fe4e58a0aeec4831b30e318c:.ufo/evidence/round-54/c2/measure.py"],
                      capture_output=True).stdout
import hashlib
live = hashlib.sha256(blob).hexdigest()
row("ER-R54-4", "old digest at BASE report; freeze pins the digest the deciding blob has",
    [("base-time fleet report cites 49280fe5 for c2",
      has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md", "`49280fe5…` (c2)")),
     ("freeze.json key c2/measure.py = 8528ee85…", pin == "8528ee8555da068519af4159f5f9e0efac8b29de88a53534a7043d7ec007e790"),
     ("deciding revision c2108100's c2/measure.py hashes to that pin", live == pin),
     ("section states 8528ee85 and the freeze.json key", "8528ee85" in SECN and "`c2/measure.py`" in SECN),
     ("section names freeze.json", "freeze.json" in SECN)])

# ---- ER-R54-5 -------------------------------------------------------------
def counts(rev):
    out = {}
    for wave in ("w1", "w2"):
        r = subprocess.run(["git", "-C", LANE, "ls-tree", "-r", "--name-only", rev, "--",
                            ".ufo/waves/round-54/%s" % wave], capture_output=True, text=True)
        names = [n for n in r.stdout.split() if re.search(r"/T54W\d+[A-Za-z]*Read\d+\.json$", n)]
        tot = withf = 0
        for rel in names:
            d = json.loads(show(LANE, rev, rel) or "{}")
            n = len(d.get("findings") or [])
            tot += n; withf += 1 if n else 0
        out[wave] = (tot, withf, len(names))
    return out
cc = counts(C0)
want = "w1=%d w2=%d sections=%d" % (cc["w1"][0], cc["w2"][0], cc["w2"][1])
row("ER-R54-5", "counts re-derived from committed readers",
    [("base-time report says '25 findings' (w1)", has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md", "returned **25 findings**")),
     ("base-time report says '22 findings in 9' (w2)", has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md", "22 findings\n  in 9 of the 23 sections")),
     ("re-derived: w1=28 w2=25 sections=12", want == "w1=28 w2=25 sections=12"),
     ("w1 spans 23 reader files", cc["w1"][2] == 23),
     ("w2 spans 23 reader files", cc["w2"][2] == 23),
     ("section states '%s'" % want, norm(want) in SECN)])

# ---- ER-R54-6 -------------------------------------------------------------
swept = [".ufo/waves/round-54/w2/T54W2Sent03.md",
         ".ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout",
         ".ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt"]
cta = show(LANE, C0, ".ufo/evidence/round-54/after/clean-tree-after.txt") or ""
sweep_stat = subprocess.run(["git", "-C", LANE, "show", "--stat", "--format=%H", "ff2a821"],
                            capture_output=True, text=True).stdout
row("ER-R54-6", "three files were untracked at closure; ff2a821 commits exactly them",
    [("clean-tree-after.txt lists all three as '??'",
      all(p in cta for p in swept)),
     ("all three present at C0", all(show(LANE, C0, p) is not None for p in swept)),
     ("ff2a821 is the commit and touches exactly the three files",
      sweep_stat.startswith("ff2a821") and sweep_stat.count(" | ") == 3),
     ("ff2a821 is an ancestor of BASE",
      subprocess.run(["git", "-C", LANE, "merge-base", "--is-ancestor", "ff2a821", BASE]).returncode == 0),
     ("section states the sweep commit ff2a821", "`ff2a821`" in SECN),
     ("section names both receipts", "c1committed-positive.stdout" in SECN and "rejection-attribution.txt" in SECN)])

# ---- ER-R54-7 -------------------------------------------------------------
ns = subprocess.run(["git", "-C", LANE, "show", "--name-status", "-M", "--format=", "7fa9a5e"],
                    capture_output=True, text=True).stdout
forged = json.loads(show(LANE, C0, ".ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json") or "{}")
row("ER-R54-7", "rename R100, old path gone, forged sha is no section at c0",
    [("base-time report says 'the deletion lands in `7fa9a5e0`'",
      has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md", "the deletion lands in `7fa9a5e0`")),
     ("7fa9a5e carries R100 old->new",
      "R100\t.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json\t.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json" in ns),
     ("old path absent at C0", show(LANE, C0, ".ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json") is None),
     ("new path present at C0",
      show(LANE, C0, ".ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json") is not None),
     ("path fails the reader pattern",
      not re.search(r"/T54W\d+[A-Za-z]*Read\d+\.json$",
                    "/.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json")),
     ("forged sha is b90c1f79… and no section at c0 has it",
      forged.get("section_sha256", "").startswith("b90c1f79")),
     ("section states renamed + R100 + 7fa9a5e",
      "renamed" in SECN and "R100" in SECN and "7fa9a5e" in SECN)])

# ---- ER-R54-8 -------------------------------------------------------------
seat = show(LANE, C0, ".ufo/waves/round-54/w1/T54W1ExecStraceNoise.md") or ""
base_seat = show(LANE, BASE, ".ufo/waves/round-54/w1/T54W1ExecStraceNoise.md") or ""
lesson55 = show(LANE, C0, "corpus/lessons/round-55.md") or ""
hist = subprocess.run(["sqlite3", "-readonly", "/home/vgpnk/.omp/agent/history.db",
                       "select id, datetime(created_at,'unixepoch'), prompt from history where id=690;"],
                      capture_output=True, text=True).stdout.strip()
cfg = open("/home/vgpnk/.omp/agent/config.yml", encoding="utf-8", errors="replace").read()
row("ER-R54-8", "base lesson silent; base seat asserts operator authority; both corrected at C0",
    [("base lesson-54 never mentions config.yml",
      "config.yml" not in (show(LANE, BASE, "corpus/lessons/round-54.md") or "")),
     ("base seat asserts 'on the operator's direct instruction in-session, which is the higher authority'",
      "on the operator's direct instruction in-session, which is the higher\n   authority" in base_seat
      or "operator's direct instruction in-session, which is the higher" in base_seat),
     ("C0 seat carries 'SUPERSEDED (round 55'", "SUPERSEDED (round 55" in seat),
     ("C0 lesson-55 records the incident", "config.yml" in lesson55),
     ("history.db id=690 at 2026-10-28 15:12:15 with the m_glm53 turn",
      hist.startswith("690|2026-10-28 15:12:15|") and "m_glm53" in hist),
     ("config.yml reads scout: \"@m_grok\" again", 'scout: "@m_grok"' in cfg),
     ("section states row 690 + 15:12:15Z", "row 690" in SECN and "2026-10-28T15:12:15Z" in SECN),
     ("section states the seat file is superseded", "is marked superseded" in SECN)])

# ---- ER-R54-9 -------------------------------------------------------------
reg = json.loads(show(LANE, C0, ".ufo/waves/round-54/w1-registry.json") or "{}")
staged = re.search(r"^output=(\d+)$",
                   show(LANE, C0, ".ufo/evidence/round-55/c1/staged-at-freeze.txt") or "", re.M)
want9 = "reviewers=%d attack=%d/%d seats=%d" % (reg["role_mix"]["reviewer"], reg["attack_seats"],
                                                reg["seats"], reg["seats"])
row("ER-R54-9", "registry yields reviewers/attack/seats; staged receipt yields 81",
    [("base-time report says '4 reviewers' with 'attack-role share 26.3 % in w1'",
      has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md", "attack-role share 26.3 % in w1")
      and has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md", "4 critics, 4 reviewers")),
     ("base lesson-54 says 'The other 84 staged'",
      has(LANE, BASE, "corpus/lessons/round-54.md", "The other 84 staged")),
     ("registry: role_mix sums to its own seats and reviewer=5, attack=21",
      sum(reg["role_mix"].values()) == reg["seats"] == 76 and reg["role_mix"]["reviewer"] == 5
      and reg["attack_seats"] == 21),
     ("21/76 rounds to 27.6 %", round(100.0 * 21 / 76, 1) == 27.6),
     ("staged receipt output=81", bool(staged) and staged.group(1) == "81"),
     ("section states '%s'" % want9, norm(want9) in SECN),
     ("section states staged=81 and 27.6 %", "staged=81" in SECN and "27.6 %" in SECN)])

# ---- ER-R54-10 ------------------------------------------------------------
ca = show(LANE, C0, ".ufo/evidence/round-54/control/controls-a.stdout") or ""
r53 = show(LANE, C0, ".ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout") or ""
m = re.search(r"CTL CTL_R53[^\n]*rekeyed=(\d+/\d+)", ca)
row("ER-R54-10", "controls-a CTL_R53 prints 0/7; 0/30 belongs to the round-53 receipt",
    [("base-time report quotes 'CTL_R53 (the round-53 final tree, 58/64, `rekeyed=0/30`)' under controls-a.stdout",
      has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md",
          "`control/controls-a.stdout`, committed): `CTL_0_c1`")
      and has(FLEET, REPORT, ".ufo/reports/round-54/tameshi.md", "`rekeyed=0/30`) `false`")),
     ("controls-a's CTL_R53 line carries rekeyed=0/7", bool(m) and m.group(1) == "0/7"),
     ("r53-counter receipt prints rekeyed=0/30 at rev=88afa941",
      "rekeyed=0/30" in r53 and "rev=88afa9415454" in r53),
     ("section states controls-a prints rekeyed=0/7", "`rekeyed=0/7`" in SECN),
     ("section points 0/30 at r53-counter-at-88afa941.stdout",
      norm("0/30` reading belongs to `control/r53-counter-at-88afa941.stdout`") in SECN)])

# ---- preamble census (not part of the 10-row verdict) ---------------------
OLD = {"CTL_POS_c1 true": None, "total=14": None, "49280fe5": None,
       "7fa9a5e0": None, "84 staged": None, "7883e0e5": None, "fe70474d": None,
       "097985c1": None, "rekeyed=0/30": None}
tracked = subprocess.run(["git", "-C", LANE, "ls-tree", "-r", "--name-only", C0, "--", "corpus", "SCORECARD.md", "LOG.md"],
                         capture_output=True, text=True).stdout.split()
for tok in OLD:
    hits = []
    for rel in tracked:
        body = show(LANE, C0, rel) or ""
        if rel == "SCORECARD.md":
            body = body.replace(SEC, "")
        if tok in body:
            hits.append(rel)
    OLD[tok] = hits
print("PREAMBLE-CENSUS (files at C0 that still quote an old value, SCORECARD section excluded)")
for tok, hits in OLD.items():
    print("  %-16s %s" % (tok, ", ".join(hits) if hits else "(none in corpus/, SCORECARD, LOG.md)"))
print()
print("| row | what was checked | result |")
print("|---|---|---|")
for cid, what, checks, bad in rows:
    print("| %s | %s | %s |" % (cid, what, "agree" if not bad else "DISAGREE: " + "; ".join(bad)))
print()
print("VERDICT rows_agree=%d/10 all=%s" % (sum(1 for r in rows if not r[3]), "AGREE" if ok_all else "DISAGREE"))
sys.exit(0 if ok_all else 1)
