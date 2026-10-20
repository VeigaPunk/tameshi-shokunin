#!/usr/bin/env python3
"""Mechanical recount of the js-kimi-census declared-witness split (read-only).

Inputs (kaika round-1 evidence, not modified):
  declared.tsv   defect<TAB>declared witness labels joined by ' | ' (or NONE...)
  case-labels.tsv defect<TAB>full_count<TAB>failed_count<TAB>failing labels joined by ' | '

Rule (SKILL/witness note): killed-on-witness iff >=1 declared label exactly equals a
failing label; accidental iff red and no declared label fails. Reproduces the
8 killed-on-witness / 0 accidental / 2 survived split. Exact-string matching only.
Run: python3 .ufo/evidence/round-12/ClaimSkeleton/witness_recount.py
"""
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[4] / ".ufo/evidence/kaika-round-1/witness"

decl = {}
for row in (BASE / "declared.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    cols = (row.split("\t") + ["", ""])[:3]
    decl[cols[0]] = [] if cols[1].startswith("NONE") else [x.strip() for x in cols[1].split(" | ")]

fail = {}
for row in (BASE / "case-labels.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    cols = row.split("\t")
    fail[cols[0]] = [x.strip() for x in cols[3].split(" | ")] if len(cols) > 3 and cols[3] not in ("", "—") else []

kw = ko = surv = 0
for d in sorted(fail, key=lambda x: int(x[1:])):
    f, w = set(fail[d]), decl.get(d, [])
    hits = [x for x in w if x in f]
    if not f:
        surv += 1; cls = "survived"
    elif hits:
        kw += 1; cls = "killed-on-witness"
    else:
        ko += 1; cls = "accidental"
    print(f"{d}: class={cls} failing={len(f)} declared={len(w)} exact_declared_hits={len(hits)} undeclared_failing={len(f - set(w))}")
print(f"TOTAL killed-on-witness={kw} accidental={ko} survived={surv}")
