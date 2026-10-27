import os, shutil, subprocess, sys
C="/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool26"
os.environ["TMPDIR"]=C+"/work"
MUTS = {
 "build_companion.purpose":      ('"purpose": (\n            "Digest-anchored', '"purpose": (\n            "MUT-Digest-anchored'),
 "build_companion.producer.note":('"note": (\n            "Historical producer identity', '"note": (\n            "MUT-Historical producer identity'),
 "build_companion.producer.source":('"source": "summary.json#/tool",', '"source": "MUT-source",'),
 "build_companion.runner.source":('"source": "declaration.json#/inputs/runner",', '"source": "MUT-source",'),
 "build_companion.measured_claim":('"measured_claim_unchanged": True,', '"measured_claim_unchanged": "MUT",'),
 "build_companion.frozen_bytes": ('"frozen_bytes_rewritten": False,', '"frozen_bytes_rewanged": "MUT",'),
 "expected.id literal":          ('EXPECTED_VERDICT_ID = "metadata_consistent"', 'EXPECTED_VERDICT_ID = "MUT_consistent"'),
 "kind_source rule":              ('"kind_source": "declaration.json#/kind (explicit frozen top-level field)",', '"kind_source": "MUT",'),
 "scope.disposition literal":     ('UNCOVERED_DISPOSITION = "named-residual-uncorrected"', 'UNCOVERED_DISPOSITION = "MUT"'),
 "companion_noncanonical check":  ('if companion != build_companion():', 'if False and companion != build_companion():'),
 "declaration top-level kind":    ('if declaration.get("kind") != EXPECTED_KIND:', 'if False and declaration.get("kind") != EXPECTED_KIND:'),
 "comp_decl kind check":          ('if comp_kind != EXPECTED_KIND:', 'if False and comp_kind != EXPECTED_KIND:'),
 "producer.checked_live check":   ('if producer.get("checked_live") is not False:', 'if False and producer.get("checked_live") is not False:'),
}
for name,(old,new) in MUTS.items():
    d=C+"/work/mut"
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(C+"/clone", d, symlinks=True)
    p=d+"/tools/witness-metadata.py"
    s=open(p).read()
    if old not in s:
        print(f"{name:34s} PATTERN-NOT-FOUND"); continue
    open(p,"w").write(s.replace(old,new,1))
    st=subprocess.run([sys.executable,"tools/witness-metadata.py","--selftest"],cwd=d,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=300)
    last=[l for l in st.stdout.splitlines() if l.strip()][-1] if st.stdout.strip() else ""
    ck=subprocess.run([sys.executable,"tools/witness-metadata.py","--check","--lane-root","."],cwd=d,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=300)
    print(f"{name:34s} selftest_exit={st.returncode} last={last[:44]:44s} check_exit={ck.returncode}")
shutil.rmtree(C+"/work/mut", ignore_errors=True)
