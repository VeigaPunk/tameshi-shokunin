import sys,subprocess,os
env=dict(os.environ)
p=subprocess.run([sys.executable,'-I','/fast/scratch/hyaku/tameshi-r100/R100E1b/tools-ref/tally-reconcile.py']+sys.argv[1:],capture_output=True,text=True,env=env)
out=p.stdout.splitlines(True)
if out: out=out[:-1]
sys.stdout.write(''.join(out))
if p.stderr: sys.stderr.write(p.stderr)
sys.exit(p.returncode)
