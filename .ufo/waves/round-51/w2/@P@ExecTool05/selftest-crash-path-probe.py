import importlib.util, sys, tempfile, traceback
spec=importlib.util.spec_from_file_location("ed","/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool05/evidence-disposition.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def boom(*a,**k): raise PermissionError("simulated: scratch root not writable")
m.tempfile.mkdtemp=boom
try:
    m.selftest()
except Exception:
    traceback.print_exc()
    print("UNCAUGHT -> python exit code would be 1 (traceback, not a declared 'could-not-evaluate' 2)")
    sys.exit(1)
