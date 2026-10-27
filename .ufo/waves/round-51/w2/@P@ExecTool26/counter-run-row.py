import importlib.util, os, shutil, json
spec = importlib.util.spec_from_file_location("m", "/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool26/measure_c3.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LANE="/home/vgpnk/Projects/shokunin/tameshi-shokunin"; REV="6d8c11e378aa90b12650808e1b79270742935f15"
W="/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool26/work/runrow"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
clone=os.path.join(W,"tameshi-shokunin")
subprocess_env=m.env()
import subprocess
subprocess.run(['git','clone','-q','--shared','--no-checkout',LANE,clone],check=True,env=subprocess_env,capture_output=True)
subprocess.run(['git','-C',clone,'checkout','-q','--detach',REV],check=True,env=subprocess_env,capture_output=True)
skill=m.show(LANE,REV,'SKILL.md').decode('utf-8','surrogateescape')
rows=m.registry_rows(skill)
for n,c in rows:
    if "tools/witness-metadata.py" not in c[2]: continue
    why,argv=m.row_reason(LANE,REV,"tools/witness-metadata.py",c)
    if why: print("line",n,"row_reason FAIL:",why); continue
    r=m.run_row(clone,W,argv)
    print("line",n,"run_row ->",r)
